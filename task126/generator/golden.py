"""FY2022 headline pendency: python3 golden.py [target_dir] [out_dir]

Reads only the shipped extract under target/ and writes the two files the headline section needs into golden/:
fy2022_pendency_headline.docx (the section as the report will print it) and fy2022_time_to_decision.svg (the chart
printed beside it). Prints the headline, the cohort and the group table.
"""
import datetime as dt
import html
import math
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, MultipleLocator  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "target"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "golden"

# Performance Reporting Charter, section 2: days from filing to the final decision, months of 30.4375 days,
# percentages to one decimal; the FY2026 report carries the filings of FY2022 (1 Oct 2021 to 30 Sep 2022).
MONTH = 30.4375
EXTRACT = pd.Timestamp("2026-09-30")
FY_LO, FY_HI = pd.Timestamp("2021-10-01"), pd.Timestamp("2022-09-30")
WITHIN = 36
DECISIONS = ("NOA", "REF", "ABN")      # the notices that decide a docket; GRT follows a NOA and decides nothing


def half_up(x, k=1):
    f = 10 ** k
    return math.floor(x * f + 0.5) / f


# ============================================================================ the extract
dk = pd.read_parquet(TARGET / "examination_dockets_FY2016_FY2026.parquet",
                     columns=["docket_no", "docketed_on", "art_unit"])
dk["docketed_on"] = pd.to_datetime(dk["docketed_on"])
links = pd.read_csv(TARGET / "docket_links.csv", dtype=str)
acts = pd.read_parquet(TARGET / "office_actions_FY2016_FY2026.parquet")
acts["served_on"] = pd.to_datetime(acts["served_on"])
ledger = pd.read_parquet(TARGET / "examiner_production_ledger_FY2016_FY2026.parquet",
                         columns=["action_id", "credit_class"])
xfer = pd.read_csv(TARGET / "docket_transfers.csv", dtype=str)
units = pd.read_csv(TARGET / "art_unit_groups.csv", dtype=str, keep_default_na=False)

notices = acts[acts["action_code"].isin(DECISIONS)]
assert not notices["docket_no"].duplicated().any(), "a docket with two decision notices"
NOTICE = dict(zip(notices["docket_no"], notices["served_on"]))

# The production standard credits the first action on the merits on each docket once: 1N when it is the first in an
# application, 1R when it follows a refusal set aside on a request for re-examination.
exr = acts[acts["action_code"] == "EXR"].sort_values(["served_on", "action_id"]).drop_duplicates("docket_no")
klass = ledger[ledger["credit_class"].isin(["1N", "1R"])]
assert not klass["action_id"].duplicated().any()
first = exr.merge(klass, on="action_id", how="left")
assert first["credit_class"].notna().all(), "a first action on the merits with no 1N or 1R credit"
FIRST = dict(zip(first["docket_no"], first["credit_class"]))

cx = links[links["link_type"] == "CX"]
NEXT = dict(zip(cx["parent_docket"], cx["child_docket"]))
TRANSFERRED_IN = set(cx["child_docket"])
START = dict(zip(dk["docket_no"], dk["docketed_on"]))


def final_decision(d):
    """Follow the file through re-examinations; stop at a refusal whose file became a continuing application."""
    while d in NEXT:
        nxt = NEXT[d]
        if FIRST.get(nxt) == "1N":       # a new application on the transferred file: the refusal was final
            return NOTICE.get(d)
        d = nxt
    return NOTICE.get(d)


fy = dk[(dk["docketed_on"] >= FY_LO) & (dk["docketed_on"] <= FY_HI)]
new_filings = [d for d in fy["docket_no"] if d not in TRANSFERRED_IN]
continuing = [d for d in fy["docket_no"] if d in TRANSFERRED_IN and FIRST.get(d) == "1N"]
apps = pd.DataFrame({"app": new_filings + continuing})
apps["filed"] = apps["app"].map(START)
apps["decided_on"] = [final_decision(a) for a in apps["app"]]
apps["decided"] = apps["decided_on"].notna() & (apps["decided_on"] <= EXTRACT)
apps["days"] = np.where(apps["decided"], (apps["decided_on"] - apps["filed"]).dt.days,
                        (EXTRACT - apps["filed"]).dt.days).astype(int)
assert not apps["app"].duplicated().any()
assert (apps.loc[apps["decided"], "days"] > 0).all()

# Tables by technology group (report table notes): the group, on the structure in force at the extract, of the art
# unit that docketed the application. The docket row carries the art unit at close, so a docket moved between art
# units was docketed by the from_au of its first transfer.
current = units[units["valid_to"] == ""].set_index("art_unit")
first_move = xfer.sort_values(["transferred_on", "docket_no"]).drop_duplicates("docket_no")
DOCKETING_AU = dict(zip(first_move["docket_no"], first_move["from_au"]))
AU_AT_CLOSE = dict(zip(dk["docket_no"], dk["art_unit"]))
apps["art_unit"] = [DOCKETING_AU.get(a, AU_AT_CLOSE[a]) for a in apps["app"]]
apps["tg"] = apps["art_unit"].map(current["tg"])
assert apps["tg"].notna().all()
GROUP_NAME = current.drop_duplicates("tg").set_index("tg")["tg_name"].to_dict()


def km_quantile(days, decided, q):
    """Kaplan-Meier: the first decision time at which the share still waiting falls to 1 - q or below."""
    s = 1.0
    d, e = np.asarray(days), np.asarray(decided)
    for t in np.unique(d[e]):
        s *= 1 - np.sum((d == t) & e) / np.sum(d >= t)
        if s <= 1 - q + 1e-12:
            return int(t)
    raise ValueError("quantile not reached")


def summary(frame):
    d, e = frame["days"].to_numpy(), frame["decided"].to_numpy()
    lq, med = km_quantile(d, e, 0.25), km_quantile(d, e, 0.5)
    w = ((d <= WITHIN * MONTH) & e).sum()
    return {"n": len(frame), "lq_days": lq, "median_days": med, "lq": half_up(lq / MONTH),
            "median": half_up(med / MONTH), "within": half_up(100 * w / len(frame)),
            "undecided": half_up(100 * (~e).sum() / len(frame)), "undecided_n": int((~e).sum())}


HEAD = summary(apps)
GROUPS = {g: summary(apps[apps["tg"] == g]) for g in sorted(apps["tg"].unique())}
OLDEST_WAIT_FLOOR = int(apps.loc[~apps["decided"], "days"].min())
assert len(GROUPS) == 8
# every application still waiting is older than every graded quantile and than 36 months, so censoring moves nothing
assert OLDEST_WAIT_FLOOR > max([HEAD["median_days"]] + [g["median_days"] for g in GROUPS.values()] + [WITHIN * MONTH])


# ============================================================================ the chart
INK, INK_2, MUTED, GRID, SERIES = "#1f1f1d", "#52514e", "#8a8984", "#e4e3df", "#2a78d6"
FONT = ["Liberation Sans", "DejaVu Sans"]


def pct_tick(v, _):
    return "{:.0f}%".format(v)


def write_svg(path):
    """Share of FY2022 filings finally decided by each month after filing, every filing in the denominator."""
    dec = np.sort(apps.loc[apps["decided"], "days"].to_numpy())
    # one step per completed month after filing, then the last decision before the extract
    x = np.append(np.arange(0, math.floor(dec[-1] / MONTH) + 1), dec[-1] / MONTH)
    share = 100 * np.searchsorted(dec, np.floor(x * MONTH + 1e-9), side="right") / HEAD["n"]
    med_x = HEAD["median_days"] / MONTH
    end_x, end_y = x[-1], share[-1]
    assert half_up(100 - end_y) == HEAD["undecided"]

    plt.rcParams.update({"font.family": FONT, "font.size": 9, "svg.fonttype": "none", "svg.hashsalt": "mpo-apr-2026",
                         "axes.edgecolor": MUTED, "axes.linewidth": 0.8, "xtick.color": INK_2, "ytick.color": INK_2,
                         "xtick.major.size": 3, "ytick.major.size": 0})
    fig, ax = plt.subplots(figsize=(7.4, 4.3), dpi=100)
    fig.subplots_adjust(left=0.085, right=0.8, top=0.83, bottom=0.17)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    ax.step(x, share, where="post", color=SERIES, linewidth=2, solid_joinstyle="miter", zorder=3)
    ax.axhline(50, color=INK_2, linewidth=1, linestyle=(0, (4, 3)), zorder=2)
    ax.text(0.6, 51.5, "50% decided", color=INK_2, fontsize=8.5, va="bottom")

    ax.plot([med_x, med_x], [0, 50], color=INK, linewidth=0.8, zorder=2)
    ax.plot([med_x], [50], marker="o", markersize=7, markerfacecolor=SERIES, markeredgecolor="white",
            markeredgewidth=1.5, zorder=4)
    ax.annotate("Median {:.1f} months".format(HEAD["median"]), xy=(med_x, 50), xytext=(med_x + 2.2, 38),
                fontsize=9.5, fontweight="bold", color=INK,
                arrowprops={"arrowstyle": "-", "color": INK_2, "linewidth": 0.8, "shrinkA": 0, "shrinkB": 4})

    # the bracket from the curve's last point at the extract to 100 per cent: the filings still undecided
    bx = end_x + 0.9
    ax.plot([end_x, end_x], [end_y, end_y], marker="o", markersize=4, color=SERIES, zorder=4)
    ax.plot([bx, bx + 0.6, bx + 0.6, bx], [end_y, end_y, 100, 100], color=INK_2, linewidth=0.9, clip_on=False)
    ax.text(bx + 1.4, (end_y + 100) / 2, "{:.1f}% still undecided\nat the 30 September\n2026 extract"
            .format(HEAD["undecided"]), fontsize=8.5, color=INK, va="center", ha="left")
    ax.text(end_x, end_y - 7, "{:.1f}% decided".format(100 - HEAD["undecided"]), fontsize=8.5,
            color=INK_2, ha="right", va="top")

    ax.set_xlim(0, 61)
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_locator(MultipleLocator(6))
    ax.yaxis.set_major_locator(MultipleLocator(25))
    ax.yaxis.set_major_formatter(FuncFormatter(pct_tick))
    ax.set_xlabel("Months from filing to the office's final decision", color=INK_2, fontsize=9)
    ax.tick_params(axis="y", pad=2)

    fig.text(0.085, 0.94, "FY2022 filings: median pendency {:.1f} months from filing to final decision"
             .format(HEAD["median"]), fontsize=12, fontweight="bold", color=INK, ha="left")
    fig.text(0.085, 0.885, "Share of applications filed 1 October 2021 to 30 September 2022 finally decided, "
             "by completed months after filing", fontsize=8.5, color=INK_2, ha="left")
    fig.text(0.085, 0.035, "Source: examination production extract at 30 September 2026. Months of 30.4375 days. "
             "Every FY2022 filing counts in the denominator.", fontsize=7.5, color=MUTED, ha="left")
    fig.savefig(path, format="svg", metadata={"Date": "2026-11-23", "Title": "FY2022 time to final decision",
                                               "Creator": "Performance Statistics Unit, Morvane Patent Office"})
    plt.close(fig)
    svg = path.read_text(encoding="utf-8")
    # the report's house face first, with the renderer's fallbacks after it
    svg = svg.replace("font-family: 'Liberation Sans', 'DejaVu Sans'", "font-family: Arial, 'Liberation Sans', sans-serif")
    svg = svg.replace('id="matplotlib.', 'id="')
    assert "DejaVu" not in svg and "atplotlib" not in svg
    path.write_text(svg, encoding="utf-8")


# ============================================================================ the headline section
DRAFTED = dt.datetime(2026, 11, 23, 16, 10)          # the draft the deputy commissioner receives
STARTED = dt.datetime(2026, 11, 16, 9, 35)


def footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("Morvane Patent Office | Annual Performance Report 2026 | Draft for sign-off | Page ")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    r = p.add_run()
    r.font.size = Pt(8)
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        r._r.append(el)


def shade(cell, fill):
    pr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), fill)
    pr.append(sh)


def para(doc, text="", size=10, bold=False, italic=False, after=6, color=None, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if align:
        p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.size, r.bold, r.italic = Pt(size), bold, italic
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
    return p


def runs(p, parts, size=10):
    """Plain strings, (text, 'b') for bold, (text, 'sup') for a note mark."""
    for t in parts:
        text, kind = t if isinstance(t, tuple) else (t, "")
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = kind == "b"
        r.font.superscript = kind == "sup"
    return p


def write_docx(path):
    h = HEAD
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    st.font.size = Pt(10)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(1.8)
    footer(sec)

    para(doc, "MORVANE PATENT OFFICE", size=9, bold=True, after=0, color="1F3A5F")
    para(doc, "Annual Performance Report 2026  |  Section 1: Headline pendency", size=9, after=0, color="404040")
    para(doc, "Draft for the Deputy Commissioner for Operations  |  Stephen Brewer  |  23 November 2026", size=9,
         after=12, color="404040")

    para(doc, "Half of FY2022 filings had their final decision within {:.1f} months".format(h["median"]),
         size=15, bold=True, after=10, color="1F1F1D")

    p = para(doc, after=10)
    runs(p, ["The median pendency of applications filed in FY2022, from filing to the office's final decision, "
             "was ", ("{:.1f} months".format(h["median"]), "b"), ".", ("1", "sup")], size=12)

    p = para(doc, after=8)
    runs(p, ["The headline is the Charter's measure for the filings of the fiscal year that ended four years before "
             "the reporting year: here applications filed from 1 October 2021 to 30 September 2022. Each application "
             "is timed from the date the office received it to the notice that decided it, an allowance, a refusal "
             "or an abandonment. The grant that follows an allowance is not the decision. ",
             "At the 30 September 2026 extract {:.1f}% of FY2022 filings were still undecided and are counted as "
             "still waiting. None of them had waited less than {} months, so no decision still to come can move the "
             "median or any figure in Table 1.1.".format(h["undecided"], round(OLDEST_WAIT_FLOOR / MONTH))])

    p = para(doc, after=8)
    runs(p, ["The headline counts applications, not examination dockets. When a refused file passes to a new "
             "docket the production system closes the old docket with end code CX whichever way the file goes. "
             "If the applicant asked for the refusal to be set aside and the file re-examined, the new docket is the "
             "same application and its decision is the application's final decision, timed from the original "
             "filing. If the applicant filed a continuing application on the file instead, the new docket is a new "
             "application with its own filing date, and the refusal was the final decision on its parent. The "
             "production ledger tells the two apart: the first action on the merits of a new application is "
             "credited 1N, once per application, and a first action after a refusal set aside on re-examination "
             "is credited 1R.", ("2", "sup")])

    p = para(doc, after=12)
    runs(p, ["Our decision dates agree to the day with the Saravel IPO's acknowledgements for every work-sharing "
             "application filed FY2019 to FY2022, open cases included. Examiner docket pendency stays in the "
             "production tables as Table P1; it times dockets, not applications, and is not a measure of this "
             "headline."])

    para(doc, "Table 1.1  FY2022 filings by technology group", size=10, bold=True, after=4)
    cols = ["Technology group", "Lower quartile\n(months)", "Median\n(months)", "Decided within\n36 months (%)"]
    t = doc.add_table(rows=1, cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    widths = (Cm(8.4), Cm(2.8), Cm(2.4), Cm(2.8))
    for i, c in enumerate(cols):
        cell = t.rows[0].cells[i]
        cell.text = ""
        r = cell.paragraphs[0].add_run(c)
        r.bold, r.font.size = True, Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        shade(cell, "1F3A5F")
    rows = [("{}  {}".format(g, GROUP_NAME[g]), v) for g, v in GROUPS.items()] + [("All FY2022 filings", h)]
    for k, (label, v) in enumerate(rows):
        cells = t.add_row().cells
        last = k == len(rows) - 1
        vals = [label, "{:.1f}".format(v["lq"]), "{:.1f}".format(v["median"]), "{:.1f}".format(v["within"])]
        for i, val in enumerate(vals):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(val)
            r.font.size, r.bold = Pt(9), last
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            if last:
                shade(cells[i], "E8ECF2")
    t.autofit = False
    grid = t._tbl.tblGrid
    for i, w in enumerate(widths):
        t.columns[i].width = w
        grid.gridCol_lst[i].w = w
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w
    p = para(doc, after=10, size=8)
    runs(p, ["Source: examination production extract at 30 September 2026, Performance Statistics Unit. Groups on "
             "the structure in force at the extract.", ("3", "sup")], size=8)

    p = para(doc, after=14)
    runs(p, ["Still undecided at the 30 September 2026 extract: ", ("{:.1f}%".format(h["undecided"]), "b"),
             " of all FY2022 filings."])

    para(doc, "Chart 1.1, printed beside this section, shows the share of FY2022 filings decided by each month after "
              "filing.", size=9.5, italic=True, after=16, color="404040")

    notes = [
        "Performance Reporting Charter, section 2. Months are days divided by 30.4375. Quartiles and medians are "
        "Kaplan-Meier estimates with undecided applications counted as still waiting at the extract.",
        "Examiner Production Standard EPD/PS/2019, section 2. The first action on the merits on a docket opened on "
        "a transferred file carries one of the two classes; continuing applications are timed from their own docketing date, "
        "which a benefit claim on the parent does not move (Charter, section 2).",
        "Report table notes: each application is counted in the group, at the extract, of the art unit that "
        "docketed it at filing. Group codes recorded on FY2022 dockets predate the 1 October 2023 restatement and "
        "are not used. Shares decided within 36 months count every application in the group, decided or not.",
    ]
    for i, n in enumerate(notes, 1):
        para(doc, "{}  {}".format(i, n), size=8, color="404040", after=3)

    cp = doc.core_properties
    cp.author = cp.last_modified_by = "Stephen Brewer"
    cp.title = "APR 2026 Section 1 headline pendency"
    cp.comments = cp.subject = cp.keywords = ""
    cp.created, cp.modified, cp.revision = STARTED, DRAFTED, 1
    doc.save(path)


def word_stats(data, pages=1):
    """Word's own statistics in docProps/app.xml, counted from the body text; the template thumbnail dropped."""
    body = data["word/document.xml"].decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", body, flags=re.S):
        txt = html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)))
        if txt.strip():
            paras.append(txt)
    stats = (("Pages", pages), ("Words", sum(len(p.split()) for p in paras)),
             ("Characters", sum(len(re.sub(r"\s", "", p)) for p in paras)),
             ("Lines", sum(max(1, math.ceil(len(p) / 90)) for p in paras)), ("Paragraphs", len(paras)),
             ("CharactersWithSpaces", sum(len(p) for p in paras)))
    app = data["docProps/app.xml"].decode("utf-8")
    for tag, val in stats:
        app = re.sub(r"<%s>\d+</%s>" % (tag, tag), "<%s>%d</%s>" % (tag, val, tag), app)
    data["docProps/app.xml"] = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0000</AppVersion>",
                                      app).encode("utf-8")
    data.pop("docProps/thumbnail.jpeg", None)
    data["_rels/.rels"] = re.sub(rb'<Relationship [^>]*Target="docProps/thumbnail.jpeg"/>', b"", data["_rels/.rels"])
    data["[Content_Types].xml"] = data["[Content_Types].xml"].replace(
        b'<Default Extension="jpeg" ContentType="image/jpeg"/>', b"")


def repack(path):
    """Fixed entry times and the draft's own created and saved stamps, so a rebuild is byte-identical."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    word_stats(data)
    core = data["docProps/core.xml"]
    for tag, val in ((rb"dcterms:created", STARTED), (rb"dcterms:modified", DRAFTED)):
        core = re.sub(rb"(<" + tag + rb"[^>]*>)[^<]*",
                      lambda m: m.group(1) + val.strftime("%Y-%m-%dT%H:%M:%SZ").encode(), core)
    data["docProps/core.xml"] = core
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i in infos:
            if i.filename not in data:
                continue
            zi = zipfile.ZipInfo(i.filename, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[i.filename])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    svg, docx = OUT / "fy2022_time_to_decision.svg", OUT / "fy2022_pendency_headline.docx"
    write_svg(svg)
    write_docx(docx)
    scrub = HERE.parents[1] / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
    subprocess.run([sys.executable, str(scrub), str(OUT), "--apply", "--producer", "Morvane Patent Office",
                    "--stamp", "2026-11-23"], capture_output=True, text=True)
    repack(docx)
    audit = subprocess.run([sys.executable, str(scrub), str(OUT), "--floor", "2026-11-01", "--ceiling", "2026-11-23"],
                           capture_output=True, text=True)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    ts = (DRAFTED - dt.datetime(1970, 1, 1)).total_seconds()
    for f in (svg, docx):
        os.utime(f, (ts, ts))

    h = HEAD
    print("FY2022 applications  %s  (%s first dockets on new filings, %s continuing applications credited 1N)"
          % ("{:,}".format(h["n"]), "{:,}".format(len(new_filings)), "{:,}".format(len(continuing))))
    print("HEADLINE median  %.1f months  (%d days)" % (h["median"], h["median_days"]))
    print("lower quartile   %.1f months  (%d days)" % (h["lq"], h["lq_days"]))
    print("decided within 36 months  %.1f%%" % h["within"])
    print("undecided at the extract  %.1f%%  (%s; none waiting under %d days, %.1f months)"
          % (h["undecided"], "{:,}".format(h["undecided_n"]), OLDEST_WAIT_FLOOR, OLDEST_WAIT_FLOOR / MONTH))
    print("\n%-48s %8s %8s %10s" % ("technology group", "LQ", "median", "<=36m %"))
    for g, v in GROUPS.items():
        print("%-48s %8.1f %8.1f %10.1f" % (g + "  " + GROUP_NAME[g], v["lq"], v["median"], v["within"]))


if __name__ == "__main__":
    main()
