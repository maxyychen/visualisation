"""
Build the visualization library.

Source of truth (edit these):
    src/families.yaml                    chart families, in display order
    src/<family>/<slug>/meta.yaml        title, purpose, when to use, avoid, tips, ...
    src/<family>/<slug>/chart.py         the code, split into cells by `# %% <name>` markers:
        # %% setup        imports; `from vizlib.<x>_style import *` is replaced by the inlined style
        # %% data         example (synthetic, offline) data                      [required]
        # %% plot         the chart; must define `fig`                           [required]
        # %% real-data    optional: same variables from a real dataset (meta: real_data)
        # %% alt:<lib>    optional: the same chart in another library (plotly / altair / seaborn)
        # %% html         optional: defines `html`, a standalone interactive page (e.g. pydeck)
    meta keys: engine (mpl | plotly | altair), level (basic | intermediate | advanced),
        reference: [{text, url, year}]  ->  the paper(s) that introduced the method
        animated: true  ->  mpl plot defines `anim` (FuncAnimation); plotly fig has frames.
                           Either way a GIF preview is written.
    vizlib/*_style.py                    shared styles

Generated (do not edit by hand):
    <family>/<slug>/<slug>.py | .ipynb | .png | .html,  README.md,  gallery/

Usage:
    python build_library.py                        # build everything, run scripts, execute notebooks
    python build_library.py --only 04 11           # selected families (by number prefix)
    python build_library.py --slug kaplan_meier    # selected charts
    python build_library.py --no-exec              # write files only
    python build_library.py --check                # CI: validate + run every script in a temp dir
    python build_library.py --new 04 my_chart      # scaffold a new chart
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import nbformat
import yaml
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
STYLE_DIR = ROOT / "vizlib"

REQUIRED_META = ["title", "engine", "purpose", "when_to_use", "avoid", "example"]
ENGINES = {"mpl": "matplotlib / seaborn", "plotly": "plotly", "altair": "Altair (Vega-Lite)"}
PLOT_VAR = {"mpl": "fig", "plotly": "fig", "altair": "chart"}
STYLE_FOR = {"mpl": "mpl_style", "plotly": "plotly_style", "altair": "altair_style"}
LEVELS = {"basic": "Basic", "intermediate": "Intermediate", "advanced": "Advanced"}
ALT_LIBS = {"plotly", "altair", "seaborn", "matplotlib"}
# "What data do you have?" vocabulary for the gallery's chart chooser (meta: data_shape).
DATA_SHAPES = {
    "categories": "Categories & groups",
    "numeric": "Numeric variables",
    "time": "Time series",
    "prices": "Prices & returns",
    "geo": "Geographic",
    "hierarchy": "Hierarchy",
    "flows": "Flows & networks",
    "sets": "Sets & overlaps",
    "text": "Text",
    "events": "Time-to-event",
    "model": "Model output",
    "uncertainty": "Estimates & uncertainty",
}
LIB_IMPORT = re.compile(r"^\s*(from|import) vizlib\.(?!\w+_style\b)", re.M)
BOOTSTRAP = ("# This example uses the reusable vizlib package from this repository\n"
             "# (or `pip install -e .` at the repo root).\n"
             "sys.path.insert(0, str(Path({base}).resolve().parents[1]))")
STYLE_IMPORT = re.compile(r"^from vizlib\.(\w+) import \*.*$", re.M)
SECTION = re.compile(r"^# %% (\S+)\s*$", re.M)


# --------------------------------------------------------------------------- loading
def load_families():
    fams = yaml.safe_load((SRC / "families.yaml").read_text())
    return {f["folder"]: f for f in fams}


def style_source(module):
    return (STYLE_DIR / f"{module}.py").read_text().strip("\n")


def parse_sections(text):
    parts = SECTION.split(text)
    out = {}
    for name, body in zip(parts[1::2], parts[2::2]):
        out[name] = body.strip("\n")
    return out


def load_charts(families, only=None, slugs=None):
    charts = []
    for folder in families:
        if only and not any(folder.startswith(o.lstrip("c").zfill(2)) for o in only):
            continue
        for d in sorted((SRC / folder).glob("*/")):
            if not (d / "meta.yaml").exists():
                continue
            if slugs and d.name not in slugs:
                continue
            meta = yaml.safe_load((d / "meta.yaml").read_text())
            sections = parse_sections((d / "chart.py").read_text())
            charts.append(dict(meta, slug=d.name, family=folder, src=d, sections=sections))
    charts.sort(key=lambda c: (c["family"], c.get("order", 999), c["slug"]))
    return charts


def validate(charts, families):
    errors = []
    seen = {}
    for c in charts:
        where = f"{c['family']}/{c['slug']}"
        for k in REQUIRED_META:
            if k not in c:
                errors.append(f"{where}: meta.yaml missing '{k}'")
        if c.get("engine") not in ENGINES:
            errors.append(f"{where}: engine must be one of {list(ENGINES)}")
        for s in ("data", "plot"):
            if s not in c["sections"]:
                errors.append(f"{where}: chart.py missing '# %% {s}' section")
        var = PLOT_VAR.get(c.get("engine"), "fig")
        if var not in c["sections"].get("plot", ""):
            errors.append(f"{where}: plot section must define `{var}`")
        if c.get("animated") and c.get("engine") == "mpl" and "anim" not in c["sections"].get("plot", ""):
            errors.append(f"{where}: animated mpl chart must define `anim` (FuncAnimation)")
        if c.get("animated") and c.get("engine") == "altair":
            errors.append(f"{where}: animated charts must use mpl or plotly")
        if c.get("level", "basic") not in LEVELS:
            errors.append(f"{where}: level must be one of {list(LEVELS)}")
        if "html" in c["sections"] and "html" not in c["sections"]["html"]:
            errors.append(f"{where}: '# %% html' section must define `html`")
        if ("real-data" in c["sections"]) != ("real_data" in c):
            errors.append(f"{where}: '# %% real-data' section and meta 'real_data' must go together")
        for s in c["sections"]:
            if s.startswith("alt:") and s[4:] not in ALT_LIBS:
                errors.append(f"{where}: unknown alt library '{s}'")
            elif s not in ("setup", "data", "plot", "real-data", "html") and not s.startswith("alt:"):
                errors.append(f"{where}: unknown section '# %% {s}'")
        for k in ("when_to_use", "avoid", "alternatives", "tips"):
            items = c.get(k, [])
            if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
                errors.append(f"{where}: '{k}' must be a list of strings "
                              "(quote items that contain ': ' so YAML does not read them as mappings)")
        refs = c.get("reference", [])
        if not isinstance(refs, list) or not all(isinstance(r, dict) and isinstance(r.get("text"), str)
                                                 and isinstance(r.get("year"), int) for r in refs):
            errors.append(f"{where}: 'reference' must be a list of {{text: str, url: str, year: int}}")
        bad = [x for x in c.get("data_shape", []) if x not in DATA_SHAPES]
        if bad:
            errors.append(f"{where}: unknown data_shape {bad}; use {list(DATA_SHAPES)}")
        if c["slug"] in seen:
            errors.append(f"{where}: duplicate slug (also in {seen[c['slug']]})")
        seen[c["slug"]] = c["family"]
    return errors


# --------------------------------------------------------------------------- code assembly
def setup_code(c, extra_styles=()):
    setup = c["sections"].get("setup", "")
    modules = STYLE_IMPORT.findall(setup) or [STYLE_FOR[c["engine"]]]
    modules += [m for m in extra_styles if m not in modules]
    rest = STYLE_IMPORT.sub("", setup).strip("\n")
    code = "\n\n".join(style_source(m) for m in modules)
    return code + ("\n\n" + rest if rest else "")


def out_dir(c):
    return ROOT / c["family"] / c["slug"]


def bar_(t):
    return f"# --- {t} " + "-" * (72 - len(t))


PLOTLY_GIF = """\
try:  # animated: also write a GIF preview from the frames (kaleido + Pillow)
    import io
    from PIL import Image
    still = go.Figure(fig)
    still.layout.updatemenus, still.layout.sliders = (), ()  # no play controls in a GIF
    step = max(1, len(fig.frames) // 40)
    images = []
    for frame in fig.frames[::step]:
        still.update(data=list(frame.data), layout=frame.layout)
        png = still.to_image(format="png", width=900, height=560)
        images.append(Image.open(io.BytesIO(png)).convert("P", palette=Image.ADAPTIVE))
    images[0].save(out.with_suffix(".gif"), save_all=True, append_images=images[1:],
                   duration=int(1000 / 6), loop=0)
except Exception as exc:
    print(f"GIF preview skipped: {exc}")
"""


def script_text(c, families):
    fam = families[c["family"]]
    wrap = lambda x, ind="  - ": textwrap.fill(x, 78, initial_indent=ind, subsequent_indent="    ")
    doc = [f"{c['title']}  -  family: {fam['name']}", "", "DESIGN PURPOSE",
           textwrap.fill(c["purpose"], 78), "", "WHEN TO USE",
           *map(wrap, c["when_to_use"]), "", "AVOID WHEN", *map(wrap, c["avoid"])]
    if c.get("alternatives"):
        doc += ["", "ALTERNATIVES", *map(wrap, c["alternatives"])]
    if c.get("reference"):
        doc += ["", "REFERENCE"] + [wrap(r["text"] + (f" {r['url']}" if r.get("url") else ""))
                                    for r in c["reference"]]
    doc += ["", "EXAMPLE", textwrap.fill(c["example"], 78)]
    if fam.get("note"):
        doc += ["", textwrap.fill("NOTE: " + fam["note"], 78)]
    doc += ["", f"Run:  python {c['slug']}.py"]
    real = "real-data" in c["sections"]
    if real:
        doc.append(f"      python {c['slug']}.py --real-data   (real dataset: {c['real_data']['source']})")
    alts = [s[4:] for s in c["sections"] if s.startswith("alt:")]
    if alts:
        doc += ["", f"The notebook also shows this chart built with: {', '.join(alts)}."]

    data = c["sections"]["data"]
    if real:
        data += ("\n\nREAL_DATA = \"--real-data\" in sys.argv\nif REAL_DATA:  # " +
                 c["real_data"]["source"] + "\n" + textwrap.indent(c["sections"]["real-data"], "    "))
        stem = 'Path(__file__).stem + ("_real" if REAL_DATA else "")'
    else:
        stem = "Path(__file__).stem"
    gif = PLOTLY_GIF if (c.get("animated") and c["engine"] == "plotly") else ""
    if c["engine"] == "altair":
        save = (f"out = Path(__file__).with_name({stem} + \".html\")\n"
                "chart.save(out)\n"
                "chart.save(out.with_suffix(\".png\"), scale_factor=2)  # static preview (vl-convert)\n"
                "print(f\"saved {out}\")\n"
                "if \"--no-show\" not in sys.argv:\n"
                "    import webbrowser\n    webbrowser.open(out.resolve().as_uri())")
    elif c["engine"] == "plotly":
        save = (f"out = Path(__file__).with_name({stem} + \".html\")\n"
                f"fig.write_html(out, include_plotlyjs=\"cdn\", div_id=\"{c['slug']}\")\n"
                "try:  # static preview; needs kaleido + a local Chrome\n"
                "    fig.write_image(out.with_suffix(\".png\"), width=1000, height=620, scale=1.5)\n"
                "except Exception:\n    pass\n" + gif +
                "print(f\"saved {out}\")\n"
                "if \"--no-show\" not in sys.argv:\n    fig.show()")
    else:
        save = (f"out = Path(__file__).with_name({stem} + \".png\")\n"
                "fig.savefig(out, dpi=150, bbox_inches=\"tight\")\n"
                + (f"anim.save(out.with_suffix(\".gif\"), writer=\"pillow\", fps={c.get('fps', 8)}, dpi=80)\n"
                   if c.get("animated") else "")
                + "print(f\"saved {out}\")\n"
                "if \"--no-show\" not in sys.argv:\n    plt.show()")
    if "html" in c["sections"]:
        save = (bar_("Interactive page") + "\n" + c["sections"]["html"] + "\n"
                f"Path(__file__).with_name({stem} + \".html\").write_text(html)\n\n" + save)
    bar = bar_
    boot = [BOOTSTRAP.format(base="__file__").replace("parents[1]", "parents[2]"), ""] \
        if LIB_IMPORT.search(c["sections"].get("setup", "")) else []
    return "\n".join(['"""', *doc, '"""', "import sys", "from pathlib import Path", "", *boot,
                      setup_code(c), "", bar("Example data"), data, "",
                      bar("Plot"), c["sections"]["plot"], "", bar("Save / show"), save, ""])


def notebook(c, families):
    fam = families[c["family"]]
    bullets = lambda xs: "\n".join(f"- {x}" for x in xs)
    plotly = c["engine"] == "plotly"
    show = {"plotly": "fig.show()", "altair": "chart", "mpl": "plt.show()"}[c["engine"]]
    if c.get("animated") and c["engine"] == "mpl":
        show = (f"plt.close(fig)  # show the animation instead of the last frame\n"
                f"anim.save(\"{c['slug']}.gif\", writer=\"pillow\", fps={c.get('fps', 8)}, dpi=80)\n"
                f"from IPython.display import Image\nImage(\"{c['slug']}.gif\")")
    alts = {s[4:]: body for s, body in c["sections"].items() if s.startswith("alt:")}
    extra = []
    if "plotly" in alts and not plotly:
        extra.append("plotly_style")
    if "altair" in alts:
        extra.append("altair_style")
    setup = setup_code(c, extra)
    setup = ("%matplotlib inline\n" if c["engine"] == "mpl" else "") + setup
    if LIB_IMPORT.search(c["sections"].get("setup", "")):
        setup = ("import sys\nfrom pathlib import Path\n" + BOOTSTRAP.format(base='"."') + "\n") + setup
    if plotly or "plotly" in alts:
        setup += '\npio.renderers.default = "plotly_mimetype+notebook_connected"'

    md = (f"# {c['title']}\n\n**Family:** {fam['name']} &nbsp;|&nbsp; **Library:** {ENGINES[c['engine']]}"
          f" &nbsp;|&nbsp; **Level:** {LEVELS[c.get('level', 'basic')]}\n\n"
          f"> *{fam['name']}:* {fam['description']}\n\n"
          + (f"> ⚠️ {fam['note']}\n\n" if fam.get("note") else "")
          + f"## Design purpose\n\n{c['purpose']}")
    when = f"## When to use\n\n{bullets(c['when_to_use'])}\n\n## Avoid when\n\n{bullets(c['avoid'])}"
    if c.get("alternatives"):
        when += f"\n\n## Alternatives\n\n{bullets(c['alternatives'])}"
    if c.get("tips"):
        when += f"\n\n## Design tips\n\n{bullets(c['tips'])}"
    cells = [new_markdown_cell(md), new_markdown_cell(when),
             new_markdown_cell(f"## Example\n\n{c['example']}\n\n### Setup"), new_code_cell(setup),
             new_markdown_cell("### Data"), new_code_cell(c["sections"]["data"]),
             new_markdown_cell("### Plot"), new_code_cell(c["sections"]["plot"] + "\n" + show)]
    if "html" in c["sections"]:
        cells += [new_markdown_cell("### Interactive version\n\nThe same data as a standalone interactive page "
                                    "(also saved next to the script as an `.html` file)."),
                  new_code_cell(c["sections"]["html"] + "\nimport html as _html\n"
                                "from IPython.display import HTML\n"
                                "HTML(f'<iframe srcdoc=\"{_html.escape(html)}\" width=\"100%\" height=\"560\" "
                                "style=\"border:0\"></iframe>')")]
    if c.get("read"):
        cells.append(new_markdown_cell(f"## How to read it\n\n{c['read']}"))
    if c.get("reference"):
        refs = "\n".join(f"- {r['text']}" + (f" <{r['url']}>" if r.get("url") else "") for r in c["reference"])
        cells.append(new_markdown_cell(f"## Reference\n\nThis method comes from the research literature:\n\n{refs}"))
    if alts:
        cells.append(new_markdown_cell(
            "## The same chart in other libraries\n\nEach version uses the example data above. Pick the "
            "library that fits your stack: matplotlib/seaborn for static and print figures, "
            "plotly for interactive HTML, Altair for concise declarative specs."))
        for lib, body in alts.items():
            cells += [new_markdown_cell(f"### {lib}"), new_code_cell(body)]
    if "real-data" in c["sections"]:
        rd = c["real_data"]
        offline = rd.get("offline", False)
        note = ("The dataset ships with an installed package, so this runs offline."
                if offline else "This downloads the dataset, so it is **not executed** in the "
                                "saved notebook. Run it yourself when online.")
        cells.append(new_markdown_cell(
            f"## Try it with real data\n\n**Source:** {rd['source']}\n\n{note} "
            "It defines the same variables as the example data, so the plot code is unchanged."))
        meta = {} if offline else {"tags": ["skip-execution"]}
        cells += [new_code_cell(c["sections"]["real-data"], metadata=meta),
                  new_code_cell(c["sections"]["plot"] + "\n" + show, metadata=meta)]
    cells.append(new_markdown_cell(
        f"---\nStandalone script: [`{c['slug']}.py`]({c['slug']}.py) &nbsp;·&nbsp; "
        "[Catalogue](../../README.md) &nbsp;·&nbsp; [Gallery](../../gallery/index.html)"))
    for i, cell in enumerate(cells):  # stable ids -> clean git diffs on rebuild
        cell["id"] = f"{c['slug'][:56]}-{i:02d}"
    return new_notebook(cells=cells, metadata={
        "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
        "language_info": {"name": "python"}})


# --------------------------------------------------------------------------- execution
def run_script(path, *args):
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONPATH="")
    r = subprocess.run([sys.executable, path.name, "--no-show", *args], cwd=path.parent,
                       capture_output=True, text=True, env=env, timeout=300)
    return path, r.returncode, (r.stderr or r.stdout)[-1500:]


RANDOM_IDS = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
                        r"|(?<=altair-viz-)[0-9a-f]{32}|(?<=T_)[0-9a-f]{5}(?![0-9a-f])|(?<= at 0x)[0-9a-f]+(?=>)")


def stable_ids(text, seed):
    """Replace random ids that plotly/Altair/pandas put in HTML outputs with deterministic ones."""
    import hashlib
    seen = {}

    def sub(m):
        old = m.group(0)
        if old not in seen:
            h = hashlib.md5(f"{seed}-{len(seen)}".encode()).hexdigest()
            seen[old] = (f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}" if "-" in old
                         else h[:len(old)])
        return seen[old]
    return RANDOM_IDS.sub(sub, text)


def execute_notebook(path):
    from nbclient import NotebookClient
    nb = nbformat.read(path, as_version=4)
    try:
        NotebookClient(nb, timeout=300, kernel_name="python3",
                       resources={"metadata": {"path": str(path.parent)}}).execute()
        for cell in nb.cells:  # drop timestamps so rebuilds give clean git diffs
            cell.metadata.pop("execution", None)
        path.write_text(stable_ids(nbformat.writes(nb), path.stem))
        return path, 0, ""
    except Exception as e:
        return path, 1, str(e)[-1500:]


# --------------------------------------------------------------------------- docs
def rel(c, ext):
    return f"{c['family']}/{c['slug']}/{c['slug']}.{ext}"


def github_repo():
    """(owner, repo, branch) from the `origin` remote when it is on GitHub, else None."""
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                                capture_output=True, text=True).stdout.strip() or "main"
    except OSError:
        return None
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    return (m.group(1), m.group(2), branch) if m else None


def pages_url():
    gh = github_repo()
    return f"https://{gh[0].lower()}.github.io/{gh[1]}/" if gh else None


def has_html(c):
    return c["engine"] in ("plotly", "altair") or "html" in c["sections"]


def preview(c):
    return rel(c, "gif" if c.get("animated") else "png")


def write_readme(charts, families):
    n = len(charts)
    site = pages_url()
    live = (lambda path: site + path) if site else (lambda path: path)
    lines = [
        "# Data Visualization Library", "",
        f"A catalogue of **{n} chart types** in Python. Each entry explains the chart's design purpose, "
        "when to use it and when to avoid it, and shows a worked example. Every chart ships as a "
        "**Jupyter notebook** (explanation and rendered output) and a **standalone Python script**.", "",
        (f"**Browse visually:** open the [interactive gallery]({site}gallery/) (GitHub Pages): search, filter by "
         "goal, data and level, and open interactive charts live. github.com shows `.html` files as source code, "
         "so use that link, or open `gallery/index.html` from a local copy. On this page, the tables below show "
         "static previews and link to notebooks, which GitHub renders." if site else
         "**Browse visually:** open [`gallery/index.html`](gallery/index.html) in a browser for a searchable, "
         "filterable gallery."), "",
        "**Not sure which chart?** Read [How to Choose a Chart](HOW_TO_CHOOSE_A_CHART.md): a step-by-step "
        "guideline with a decision path, a finance quick reference and a pre-publication checklist.", "",
        "**Using AI to make charts?** Read [Agentic AI and Data Visualization](AGENTIC_AI_AND_VISUALIZATION.md).", "",
        "Families 01–09 follow the Financial Times "
        "[Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary), "
        "which groups charts by the *relationship in the data you want to show*. The other families are "
        + ", ".join(f"**{v['name']}**" for k, v in list(families.items())[9:]) + ".", "",
        "## Quick start", "", "```bash",
        "python3 -m venv .venv && source .venv/bin/activate",
        "pip install -r requirements.txt",
        "jupyter lab                                   # browse the notebooks",
        "python 01_deviation/diverging_bar/diverging_bar.py",
        "python 04_distribution/violin_plot/violin_plot.py --real-data   # charts marked ★ have real data",
        "```", "",
        "## How to choose a chart", "",
        "1. **Decide what the reader should notice:** a difference from a baseline, a relationship, an order, "
        "a shape, a trend, a size, a share, a place, or a movement. That picks the family.",
        "2. **Pick the simplest form in that family** that shows the message. If the story is one number, "
        "use a stat tile.",
        "3. **Add color last**, and only by the job it does: identity (categorical), magnitude (one-hue "
        "sequential), or polarity (two-hue diverging with a neutral midpoint).",
        "4. **Avoid the classic mistakes.** See " + next(
            (f"[{k[:2]} · {v['name']}](#{k.replace('_', '-')})" for k, v in families.items() if "bad_vs_good" in k),
            "the bad-vs-good family") + ".", "",
        "**Chart chooser:** see [What data do you have?](#chooser) below, or filter by data type in the gallery.", "",
        "Legend: 📄 method from a research paper (see [Methods from the research literature](#research)) · ★ real-dataset variant · 🔀 also shown in other libraries (plotly / Altair / seaborn) · "
        "<sub>intermediate</sub> / <sub>advanced</sub> level (unmarked = basic) · animated charts preview as GIFs", "",
        "| Family | Charts | Question it answers |", "|---|---|---|"]
    for folder, f in families.items():
        k = sum(c["family"] == folder for c in charts)
        if k:
            lines.append(f"| [{f['name']}](#{folder.replace('_', '-')}) | {k} | {f['description']} |")
    for folder, f in families.items():
        group = [c for c in charts if c["family"] == folder]
        if not group:
            continue
        lines += ["", f"<a id=\"{folder.replace('_', '-')}\"></a>", f"## {folder[:2]} · {f['name']}", "",
                  f"*{f['description']}*", "", "| Chart | Use it to… | Files | Preview |", "|---|---|---|---|"]
        for c in group:
            marks = ("📄" if c.get("reference") else "") + ("★" if "real-data" in c["sections"] else "") + \
                    ("🔀" if any(s.startswith("alt:") for s in c["sections"]) else "")
            use = c["when_to_use"][0].replace("|", "\\|")
            files = f"[ipynb]({rel(c, 'ipynb')}) · [py]({rel(c, 'py')})"
            if has_html(c):
                files += f" · [interactive]({live(rel(c, 'html'))})"
            level = c.get("level", "basic")
            tag = "" if level == "basic" else f"<br><sub>{LEVELS[level].lower()}</sub>"
            lines.append(f"| **{c['title']}** {marks}{tag} | {use} | {files} | "
                         f"<img src=\"{preview(c)}\" width=\"170\"> |")
    research = sorted((c for c in charts if c.get("reference")), key=lambda c: -c["reference"][0]["year"])
    if research:
        lines += ["", "<a id=\"research\"></a>", "## Methods from the research literature", "",
                  "Peer-reviewed visualization methods, newest first. Each notebook has a **Reference** section.", "",
                  "| Year | Chart | Family | Reference |", "|---|---|---|---|"]
        for c in research:
            r = c["reference"][0]
            cite = f"[{r['text']}]({r['url']})" if r.get("url") else r["text"]
            lines.append(f"| {r['year']} | [{c['title']}]({rel(c, 'ipynb')}) | {families[c['family']]['name']} | "
                         f"{cite.replace('|', '/')} |")
    lines += ["", "<a id=\"chooser\"></a>", "## Chart chooser: what data do you have?", "",
              "| Your data | Charts that fit |", "|---|---|"]
    for key, label in DATA_SHAPES.items():
        fit = [c for c in charts if key in c.get("data_shape", [])]
        if fit:
            links = ", ".join(f"[{c['title'].split(' (')[0]}]({rel(c, 'ipynb')})" for c in fit)
            lines.append(f"| **{label}** ({len(fit)}) | {links} |")
    lines += ["", "## Reusable finance toolkit: `vizlib.finance`", "",
              "Tested functions for returns, drawdowns, CAGR, volatility, Sharpe, Sortino, Calmar, VaR/CVaR, beta, alpha, "
              "tracking error, information ratio, rolling metrics and monthly-return tables, plus a one-page `tear_sheet()`.", "",
              "```python", "from vizlib.finance import to_returns, summary_stats, tear_sheet",
              "r, b = to_returns(prices[\"Fund\"]), to_returns(prices[\"Index\"])",
              "summary_stats(r, b, rf=0.03)            # tidy table of statistics",
              "tear_sheet(r, b, title=\"My fund\").savefig(\"report.pdf\")", "```", "",
              "From the command line, with your own CSV of prices:", "", "```bash",
              "pip install -e .     # once, at the repo root",
              "python -m vizlib.finance prices.csv --price Fund --benchmark Index --rf 0.03 -o report.png",
              "pytest               # unit tests for the metrics", "```",
              "", "## Reusable healthcare toolkit: `vizlib.health`", "",
              "Tested statistics behind the healthcare charts: Kaplan–Meier with Greenwood confidence bands "
              "(checked against `lifelines`), median survival and RMST; run-chart rules, p- and u-chart limits, exact "
              "funnel-plot limits, VLAD and risk-adjusted CUSUM; epidemic-curve binning and time-varying Rt "
              "(Cori et al. 2013); reference-range flags.", "",
              "```python", "from vizlib.health import kaplan_meier, run_chart_signals, p_chart, estimate_rt",
              "km = kaplan_meier(df[\"months\"], df[\"died\"])     # survival table with 95% CI",
              "run_chart_signals(monthly_rate)                      # shifts, trends, runs",
              "estimate_rt(daily_cases, serial_interval)            # Rt with 95% credible interval", "```", "",
              "> Use de-identified data. Executed notebooks store their outputs, including any patient-level values."]
    lines += ["", "## Advanced extras", "",
              "Large-data, 3-D map and time-series charts use optional packages:", "", "```bash",
              "pip install -r requirements-advanced.txt   # or: pip install -e \".[advanced]\"", "```", "",
              "Interactive charts (plotly, Altair, pydeck) save a standalone `.html` page next to the script. "
              "Open it in a browser, or use the **Live** button in the gallery. Animated charts also save a `.gif`."]
    if site:
        lines += ["", "## Publishing the gallery (GitHub Pages)", "",
                  "`.github/workflows/pages.yml` publishes `gallery/` and the generated chart folders to "
                  f"{site} on every push to the default branch. One-time setup: **Settings → Pages → Build and "
                  "deployment → Source: GitHub Actions**. On Pages, the gallery's *Notebook* and *Script* links "
                  "open on github.com (which renders notebooks); *Live* opens the interactive page itself."]
    lines += ["", "## Agentic AI and data visualization", "",
              "AI agents can now turn a plain-language request into working chart code in seconds, and most of this "
              "library was itself written by agents. Research shows their charts are uneven in quality, and that AI "
              "models are easily fooled by misleading designs, so judgement, explicit rules and tests matter more than "
              "ever. [Agentic AI and Data Visualization](AGENTIC_AI_AND_VISUALIZATION.md) covers how the workflow "
              "changes, what the research says, lessons from building this library, and a checklist for using an "
              "agent to make a chart."]
    lines += ["", "## Extending the library", "",
              "Everything above is generated. Edit the sources in `src/` and rebuild:", "", "```bash",
              "python build_library.py --new 04 my_chart   # scaffold src/04_.../my_chart/{meta.yaml,chart.py}",
              "python build_library.py --slug my_chart     # build just that chart, then look at the PNG",
              "python build_library.py --check             # validate + run every script (what CI runs)",
              "python build_library.py                     # full rebuild: notebooks, README, gallery",
              "```", "",
              "`chart.py` is plain Python split into cells by `# %% setup`, `# %% data`, `# %% plot` and the optional "
              "`# %% real-data` and `# %% alt:<library>` cells. Its first line imports the shared style from `vizlib/`, "
              "so you can lint it and run it from the repo root (`PYTHONPATH=. python src/<family>/<slug>/chart.py`). The build inlines that style, so every generated script is standalone. "
              "To add a family, append it to `src/families.yaml`.", "",
              "## Sources", "", "### Guides and catalogues", "",
              "- Financial Times, *Visual Vocabulary*: https://github.com/Financial-Times/chart-doctor",
              "- The Data Visualisation Catalogue: https://datavizcatalogue.com",
              "- From Data to Viz (including its *caveats* collection): https://www.data-to-viz.com",
              "- The Python Graph Gallery: https://python-graph-gallery.com",
              "- data.europa.eu, *Choosing charts: the message*: "
              "https://data.europa.eu/apps/data-visualisation-guide/choosing-charts-the-message"]
    papers = {}
    for c in charts:  # generated from each chart's meta.yaml `reference`, so it never drifts
        for r in c.get("reference", []):
            papers.setdefault((r["text"], r.get("url")), []).append(c)
    if papers:
        lines += ["", "### Research papers", "",
                  f"The {len(papers)} papers behind specific charts in this library, generated from each chart's "
                  "`reference` in `meta.yaml`. Each notebook repeats its citation in a **Reference** section.", ""]
        for (text, url), used in sorted(papers.items(), key=lambda kv: kv[0][0].lower()):
            charts_md = ", ".join(f"[{c['title'].split(' (')[0]}]({rel(c, 'ipynb')})" for c in used)
            lines.append(f"- {text}" + (f" <{url}>" if url else "") + f" Used in: {charts_md}.")
    lines += [""]
    (ROOT / "README.md").write_text("\n".join(lines))


def write_gallery(charts, families):
    from PIL import Image
    gdir = ROOT / "gallery"
    tdir = gdir / "thumbs"
    tdir.mkdir(parents=True, exist_ok=True)
    items = []
    for c in charts:
        src = ROOT / preview(c)
        thumb = tdir / f"{c['slug']}.{src.suffix[1:]}"
        if src.exists() and (not thumb.exists() or thumb.stat().st_mtime < src.stat().st_mtime):
            im = Image.open(src)
            if c.get("animated"):
                from PIL import ImageSequence
                frames = []
                for fr in ImageSequence.Iterator(im):
                    fr = fr.convert("RGB")
                    fr.thumbnail((560, 400))
                    frames.append(fr.convert("P", palette=Image.ADAPTIVE))
                frames[0].save(thumb, save_all=True, append_images=frames[1:],
                               duration=im.info.get("duration", 150), loop=0, optimize=True)
            else:
                im = im.convert("RGB")
                im.thumbnail((560, 400))
                im.save(thumb, optimize=True)
        items.append({
            "slug": c["slug"], "title": c["title"], "family": c["family"],
            "familyName": families[c["family"]]["name"], "purpose": c["purpose"],
            "use": c["when_to_use"], "avoid": c["avoid"], "engine": c["engine"],
            "real": "real-data" in c["sections"], "shapes": c.get("data_shape", []),
            "alts": [s[4:] for s in c["sections"] if s.startswith("alt:")],
            "level": c.get("level", "basic"), "animated": bool(c.get("animated")),
            "refs": [dict(text=r["text"], url=r.get("url"), year=r["year"]) for r in c.get("reference", [])],
            "thumb": f"thumbs/{c['slug']}.{'gif' if c.get('animated') else 'png'}",
            "ipynb": "../" + rel(c, "ipynb"), "py": "../" + rel(c, "py"),
            "html": "../" + rel(c, "html") if has_html(c) else None,
        })
    fams = [{"folder": k, "name": v["name"], "n": sum(i["family"] == k for i in items)}
            for k, v in families.items()]
    page = (Path(__file__).parent / "vizlib" / "gallery_template.html").read_text()
    page = page.replace("/*DATA*/", "const CHARTS = " + json.dumps(items, ensure_ascii=False)
                        + ";\nconst FAMILIES = " + json.dumps(fams, ensure_ascii=False)
                        + ";\nconst SHAPES = " + json.dumps(DATA_SHAPES, ensure_ascii=False)
                        + ";\nconst LEVELS = " + json.dumps(LEVELS)
                        + ";\nconst REPO = " + json.dumps(dict(zip(("owner", "repo", "branch"), github_repo()))
                                                         if github_repo() else None) + ";")
    (gdir / "index.html").write_text(page)


# --------------------------------------------------------------------------- commands
NEW_META = """\
title: {title}
engine: mpl            # mpl | plotly | altair
level: basic           # basic | intermediate | advanced
order: 999             # position within the family
data_shape: [numeric]  # what data it needs; keys in DATA_SHAPES (build_library.py)
# animated: true       # mpl: plot defines `anim` (FuncAnimation); plotly: fig.frames -> GIF preview
purpose: >-
  What the chart is and the perceptual job it does.
when_to_use:
  - ...
avoid:
  - ...
alternatives:
  - ...
tips:
  - ...
example: One sentence describing the example data.
read: How to read the example.
# real_data:           # pair with a '# %% real-data' cell in chart.py
#   source: sklearn.datasets.load_wine
#   offline: true      # false = downloads; the notebook cell is then not executed
"""
NEW_CHART = """\
# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(0)
df = pd.DataFrame({"x": np.arange(10), "y": rng.normal(size=10).cumsum()})
df.head()

# %% plot
fig, ax = plt.subplots()
ax.plot(df["x"], df["y"])
ax.set_title("Title that states the message")
fig.tight_layout()
"""


def cmd_new(families, prefix, slug):
    folder = next((f for f in families if f.startswith(prefix.lstrip("c").zfill(2))), None)
    if not folder:
        raise SystemExit(f"no family starting with {prefix!r}; see src/families.yaml")
    d = SRC / folder / slug
    if d.exists():
        raise SystemExit(f"{d} already exists")
    d.mkdir(parents=True)
    (d / "meta.yaml").write_text(NEW_META.format(title=slug.replace("_", " ").title()))
    (d / "chart.py").write_text(NEW_CHART)
    print(f"created {d.relative_to(ROOT)}/meta.yaml and chart.py\n"
          f"next: edit them, then  python build_library.py --slug {slug}")


def cmd_check(charts, families, jobs):
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "vizlib").symlink_to(STYLE_DIR)  # same layout as the repo for vizlib imports
        runs = []
        for c in charts:
            d = Path(tmp) / c["family"] / c["slug"]
            d.mkdir(parents=True)
            p = d / f"{c['slug']}.py"
            p.write_text(script_text(c, families))
            compile(p.read_text(), str(p), "exec")
            for sec, body in c["sections"].items():
                if sec.startswith("alt:"):
                    compile(body, f"{c['slug']}:{sec}", "exec")
            runs.append((p,))
            if "real-data" in c["sections"] and c["real_data"].get("offline"):
                runs.append((p, "--real-data"))
        with ThreadPoolExecutor(jobs) as ex:
            res = list(ex.map(lambda a: run_script(*a), runs))
    fails = [(p, e) for p, code, e in res if code]
    for p, e in fails:
        print(f"\nFAILED {p.name}\n{e}")
    print(f"\ncheck: {len(charts)} charts, {len(runs)} script runs, {len(fails)} failures")
    return not fails


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", help="family number prefixes, e.g. 04 11")
    ap.add_argument("--slug", nargs="*", help="chart slugs")
    ap.add_argument("--no-exec", action="store_true", help="write files, skip running")
    ap.add_argument("--check", action="store_true", help="validate and run scripts in a temp dir")
    ap.add_argument("--new", nargs=2, metavar=("FAMILY", "SLUG"), help="scaffold a new chart")
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()

    families = load_families()
    if args.new:
        return cmd_new(families, *args.new)
    every = load_charts(families)
    errors = validate(every, families)
    if errors:
        raise SystemExit("invalid sources:\n  " + "\n  ".join(errors))
    selected = load_charts(families, args.only, args.slug)
    if args.check:
        sys.exit(0 if cmd_check(selected, families, args.jobs) else 1)

    scripts, notebooks = [], []
    for c in selected:
        d = out_dir(c)
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{c['slug']}.py").write_text(script_text(c, families))
        nbformat.write(notebook(c, families), d / f"{c['slug']}.ipynb")
        scripts.append(d / f"{c['slug']}.py")
        notebooks.append(d / f"{c['slug']}.ipynb")
    print(f"wrote {len(selected)} charts")

    failures = []
    if not args.no_exec:
        with ThreadPoolExecutor(args.jobs) as ex:
            failures += [(p, e) for p, code, e in ex.map(run_script, scripts) if code]
            failures += [(p, e) for p, code, e in ex.map(execute_notebook, notebooks) if code]
    write_readme(every, families)
    write_gallery(every, families)
    for p, e in failures:
        print(f"\nFAILED {p.relative_to(ROOT)}\n{e}")
    print(f"\n{len(selected)} charts built, {len(failures)} failures")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
