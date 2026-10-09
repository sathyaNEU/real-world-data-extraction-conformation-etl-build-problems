"""Headline squad 2027 placement: the paper and its workbook.

python3 golden.py [target_dir] [out_dir]

Reads the planning-folder exports in target_dir and writes squad_placement_2027.docx and
squad_placement_2027.xlsx to out_dir. Prints the figures the paper rests on.
"""
import csv
import datetime as dt
import io
import math
import os
import re
import statistics
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import duckdb
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from scipy.optimize import minimize_scalar

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, NullFormatter  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "target"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "golden"

# The 2027 shortlist as the placement brief lists it.
SHORTLIST = ["POL-N", "SPT-M", "BUS-N", "SPT-N", "LOC-M", "CUL-N"]
# Surfaces that render Bightline's own headline (field reference); every other source code shows the
# canonical headline stored at publication, which a test never changes.
PLATFORM = ("home_web", "section_web", "feed_app", "section_app", "related_links")
WINDOW_START = dt.date(2025, 10, 1)
BACKTEST_TOL = 0.02


def r50k(x):
    return int(math.floor(x / 50_000 + 0.5) * 50_000)


def r1k(x):
    return int(math.floor(x / 1_000 + 0.5) * 1_000)


def one_dp(x):
    return math.floor(x * 10 + 0.5) / 10


def find(prefix):
    hit = [p for p in TARGET.iterdir() if p.name.startswith(prefix)]
    assert len(hit) == 1, prefix
    return hit[0]


# --------------------------------------------------------------------------- inputs
desks = {r["desk_code"]: r for r in csv.DictReader(open(find("desk_register"), encoding="utf-8"))}
NAME = {d: desks[d]["desk_name"] for d in desks}

rows = list(load_workbook(find("audience_plan_2027"), read_only=True, data_only=True)["Plan 2027"]
            .iter_rows(values_only=True))
planned = {r[0]: int(r[4]) for r in rows[1:] if r[0] and r[0] != "Total"}

srows = list(load_workbook(find("newsroom_staff_list"), read_only=True, data_only=True)["Staff"]
             .iter_rows(values_only=True))
team = {r[0]: r[2] for r in srows[1:]}

tests = defaultdict(list)
for r in csv.DictReader(open(find("headline_tests_archive"), encoding="utf-8")):
    tests[r["test_id"]].append(r)
meta = {t: (pk[0]["engine"], pk[0]["desk_code"], int(pk[0]["article_id"]), pk[0]["owner_staff_id"],
            pk[0]["started_at"]) for t, pk in tests.items()}

# --------------------------------------------------------------------------- winning lift, shrunk
# Each variant's lift over its control with its sampling variance (delta method on the CTR ratio).
L, S2, per_test = [], [], {}
for tid, pk in tests.items():
    ctl = next(p for p in pk if p["variant"] == "control")
    n0, c0 = int(ctl["impressions"]), int(ctl["clicks"])
    p0 = c0 / n0
    per_test[tid] = []
    for p in pk:
        if p["variant"] == "control":
            continue
        n, c = int(p["impressions"]), int(p["clicks"])
        pv = c / n
        rr = pv / p0
        s2 = rr * rr * ((1 - pv) / (n * pv) + (1 - p0) / (n0 * p0))
        L.append(rr - 1)
        S2.append(s2)
        per_test[tid].append((rr - 1, s2, p["shipped"] == "Y"))
L, S2 = np.array(L), np.array(S2)
N_PACKAGES = len(L)


def neg_loglik(tau2):
    w = 1 / (tau2 + S2)
    mu = np.sum(w * L) / np.sum(w)
    return 0.5 * np.sum(np.log(tau2 + S2) + (L - mu) ** 2 * w)


# One normal prior across every variant in the archive, fitted by maximum likelihood.
TAU2 = float(minimize_scalar(neg_loglik, bounds=(1e-7, 0.05), method="bounded",
                             options={"xatol": 1e-13}).x)
W = 1 / (TAU2 + S2)
MU = float(np.sum(W * L) / np.sum(W))


def win(tid, shrink=True):
    """The shipped headline's lift; zero when the control was kept."""
    for lift, s2, shipped in per_test[tid]:
        if shipped:
            return MU + TAU2 / (TAU2 + s2) * (lift - MU) if shrink else lift
    return 0.0


by_desk = defaultdict(list)
for tid, m in meta.items():
    by_desk[m[1]].append(tid)
raw = {d: float(np.mean([win(t, False) for t in by_desk[d]])) for d in SHORTLIST}
shr = {d: float(np.mean([win(t) for t in by_desk[d]])) for d in SHORTLIST}

# Every test at a shortlisted desk was created by that desk's own editors (staff list team), never the squad.
assert all(team[meta[t][3]] == meta[t][1] for d in SHORTLIST for t in by_desk[d])
assert len({m[2] for m in meta.values()}) == len(meta), "one test per article"

# --------------------------------------------------------------------------- 2027 clicks by surface
con = duckdb.connect()
con.execute("CREATE TABLE pv AS SELECT * FROM read_parquet(?)", [str(find("pageviews_by_source_age"))])
con.execute("CREATE TABLE tested AS SELECT unnest(?::BIGINT[]) AS article_id", [sorted({m[2] for m in meta.values()})])
plat = ",".join("'%s'" % s for s in PLATFORM)
chain = {}
for d, total, p, pt, n_win in con.execute(f"""
        SELECT v.desk_code, sum(pageviews),
               sum(pageviews) FILTER (WHERE source_code IN ({plat})),
               sum(pageviews) FILTER (WHERE source_code IN ({plat}) AND t.article_id IS NOT NULL),
               count(DISTINCT v.article_id) FILTER (WHERE published_date >= DATE '{WINDOW_START}')
        FROM pv v LEFT JOIN tested t USING (article_id) GROUP BY v.desk_code""").fetchall():
    chain[d] = {"planned": int(total), "platform": int(p or 0), "platform_tested": int(pt or 0), "articles": n_win}
for d in SHORTLIST:
    c = chain[d]
    assert c["planned"] == planned[d], d  # the plan carries the base year forward to the click
    c["untested"] = c["platform"] - c["platform_tested"]
    c["lift"] = shr[d]
    c["extra"] = shr[d] * c["untested"]

order = sorted(SHORTLIST, key=lambda d: chain[d]["extra"], reverse=True)
CALL, RUNNER = order[0], order[1]
GAP = chain[CALL]["extra"] - chain[RUNNER]["extra"]

# --------------------------------------------------------------------------- back-test on the change log
erows = list(load_workbook(find("headline_squad_change_log"), read_only=True, data_only=True)["Embeddings"]
             .iter_rows(values_only=True))
emb = [dict(zip(erows[0], r)) for r in erows[1:] if r[0] is not None]
app_tests = defaultdict(list)
for t, m in meta.items():
    if m[0] == "app":
        app_tests[(m[1], int(m[4][:4]))].append(t)
backtest = []
for e in emb:
    ids = app_tests[(e["desk_code"], e["started"].year)]
    assert len(ids) == e["tests_run"]
    lift = float(np.mean([win(t) for t in ids]))
    pred = lift * float(e["planned_clicks_m"]) * 1e6
    real = float(e["realised_incremental_clicks"])
    backtest.append({"n": e["embedding"], "desk": e["desk"], "year": e["started"].year, "tests": e["tests_run"],
                     "observed": float(e["avg_winning_lift_pct"]), "shrunk": lift,
                     "planned_m": float(e["planned_clicks_m"]), "diff": pred / real - 1})
HITS = sum(abs(b["diff"]) <= BACKTEST_TOL for b in backtest)
RAW_HITS = sum(abs(float(np.mean([win(t, False) for t in app_tests[(e["desk_code"], e["started"].year)]]))
                   * float(e["planned_clicks_m"]) * 1e6 / float(e["realised_incremental_clicks"]) - 1) <= BACKTEST_TOL
               for e in emb)

# --------------------------------------------------------------------------- readers (panel)
# A release's section codes belong to the section list it was issued on: the first release on the 2026 content
# taxonomy and every release after it use the 2026 list. The latest release for a month and section is the record.
pwb = load_workbook(find("panel_reference_workbook"), read_only=True, data_only=True)
hist = list(pwb["Section history"].iter_rows(values_only=True))[1:]
rlog = [r for r in list(pwb["Release log"].iter_rows(values_only=True))[1:] if r[0]]
rel = {r[0]: r[1] for r in rlog}
issued_2026 = min(r[1] for r in rlog if (r[3] or "").startswith("First release on the 2026 content taxonomy"))
sections = {"2026": {(h[0], h[1]): (h[2], h[5]) for h in hist if h[4] is None},
            "2024": {(h[0], h[1]): (h[2], h[5]) for h in hist if h[4] is not None}}
latest = {}
for r in csv.DictReader(open(find("panel_monthly_audience"), encoding="utf-8")):
    name, desk = sections["2026" if rel[r["release"]] >= issued_2026 else "2024"][(r["site_code"], int(r["section_code"]))]
    key = (r["period"], r["site_code"], name)
    if key not in latest or rel[r["release"]] > rel[latest[key][0]["release"]]:
        latest[key] = (r, desk)  # a later release of the same month replaces the earlier one
monthly = defaultdict(dict)
for (period, site, name), (r, desk) in latest.items():
    if desk:
        monthly[desk][period] = int(r["unique_audience"])
readers = {}
for d in SHORTLIST:
    assert len(monthly[d]) == 12, d
    readers[d] = statistics.mean(monthly[d].values())

# --------------------------------------------------------------------------- headline corrections (CMS)
docs, info = defaultdict(list), {}
for r in csv.DictReader(open(find("cms_revisions_web_desks"), encoding="utf-8")):
    docs[r["doc_id"]].append((int(r["revision"]), r["saved_at"], r["status"], r["publish_at"], r["headline_sha1"],
                              r["correction_note"]))
    info[r["doc_id"]] = (r["desk_code"], r["doc_type"], r["parent_doc"], r["restored_from_doc"], r["migrated_from"])
restored_copy = {v[3]: k for k, v in info.items() if v[3]}
when = lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%MZ")  # noqa: E731

# Entries of a live blog that published a changed headline (an entry's error is fixed in the entry, and its
# correction note goes on the live blog, editorial standards 7.5).
entry_fixed = defaultdict(list)
for did, (desk, typ, parent, restored_from, migrated_from) in info.items():
    if typ != "post" or restored_from:
        continue
    revs = sorted(docs[did]) + (sorted(docs[restored_copy[did]]) if did in restored_copy else [])
    shown = [r for r in revs if r[2] == "live"]
    blog = info[parent][3] or parent
    entry_fixed[blog] += [when(b[1]) for a, b in zip(shown, shown[1:]) if b[4] != a[4]]

corr, arts, mins, corr_at, text_at = defaultdict(int), defaultdict(int), defaultdict(list), [], []
for did, revs in docs.items():
    desk, typ, parent, restored_from, migrated_from = info[did]
    # live-blog posts are not articles; restored and migrated copies continue an earlier document
    if restored_from or migrated_from or typ == "post":
        continue
    revs = sorted(revs)
    if did in restored_copy:
        revs += sorted(docs[restored_copy[did]])
    live = [r for r in revs if r[2] == "live"]
    if not live:
        continue
    arts[desk] += 1
    # what readers saw: each live save, and a scheduled version the CMS published at publish_at
    published, went_live = live, when(live[0][1])
    scheduled = [r for r in revs if r[2] == "scheduled" and r[0] < live[0][0]]
    if scheduled and scheduled[-1][3] and when(scheduled[-1][3]) < went_live:
        published, went_live = [scheduled[-1]] + live, when(scheduled[-1][3])
    first = None
    for prev, cur in zip(published, published[1:]):
        # a note carries forward until cleared, so a correction is a new note on a published version
        if not cur[5] or cur[5] == prev[5]:
            continue
        t = when(cur[1])
        entries = [f for f in entry_fixed.get(did, []) if t - dt.timedelta(minutes=2) <= f <= t]
        if cur[4] != prev[4] or entries:
            at = t if cur[4] != prev[4] else min(entries)
            corr[desk] += 1
            corr_at.append(at)
            first = at if first is None else min(first, at)
        else:
            text_at.append(t)
    if first is not None:
        mins[desk].append(int((first - went_live).total_seconds() // 60))

# The correction rule back-tested on the record: the standards bulletin's March 2026 count for the web desks.
bulletin = " ".join(p.text for p in Document(str(find("standards_bulletin"))).paragraphs)
FILED = re.search(r"logged (\d+) headline corrections and (\d+) corrections to article text", bulletin)
MARCH_FILED, MARCH_TEXT_FILED = int(FILED.group(1)), int(FILED.group(2))
lo_m, hi_m = dt.datetime(2026, 2, 28, 14), dt.datetime(2026, 3, 31, 14)      # March 2026 in AEST, as UTC
MARCH = sum(lo_m <= t < hi_m for t in corr_at)
MARCH_TEXT = sum(lo_m <= t < hi_m for t in text_at)
assert (MARCH, MARCH_TEXT) == (MARCH_FILED, MARCH_TEXT_FILED), (MARCH, MARCH_TEXT, MARCH_FILED, MARCH_TEXT_FILED)

asks = {}
for d in SHORTLIST:
    assert arts[d] == chain[d]["articles"], d
    assert len(mins[d]) % 2 == 1, d
    asks[d] = {"extra": r50k(chain[d]["extra"]), "readers": r1k(readers[d]),
               "per_reader": one_dp(chain[d]["extra"] / readers[d]), "corrections": corr[d],
               "rate": one_dp(1000 * corr[d] / arts[d]), "median": int(statistics.median(mins[d]))}

# ============================================================================ the chart
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
STAGES = [("planned", "2027 clicks (plan)", "#86b6ef"),
          ("platform", "from Bightline's own surfaces", "#3987e5"),
          ("untested", "on headlines the desk does not test", "#1c5cab"),
          ("extra", "extra clicks from the squad", "#0d366b")]
HILITE = "#fdf0e8"


def tick(x, _):
    if x >= 1e6:
        return "%gm" % (x / 1e6)
    return "{:,.0f}".format(x)


def chart_png():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ys = {d: len(order) - 1 - i for i, d in enumerate(order)}
    for d in (CALL, RUNNER):
        ax.axhspan(ys[d] - 0.42, ys[d] + 0.42, color=HILITE, zorder=0, lw=0)
    for d in order:
        xs = [chain[d][k] for k, _, _ in STAGES]
        ax.plot(xs, [ys[d]] * 4, color="#c9c8c2", lw=1.6, zorder=1, solid_capstyle="round")
        for (k, label, col), x in zip(STAGES, xs):
            ax.scatter([x], [ys[d]], s=46, color=col, edgecolor=SURF, linewidth=1.6, zorder=3,
                       label=label if d == order[0] else None)
        ax.text(chain[d]["extra"] / 1.22, ys[d], "{:,}".format(asks[d]["extra"]), ha="right", va="center",
                fontsize=8.5, color=INK, fontweight="bold" if d == CALL else "normal")
    labels = []
    for d in order:
        tag = "\nrecommended" if d == CALL else "\nrunner-up" if d == RUNNER else ""
        labels.append(NAME[d] + tag)
    ax.set_yticks([ys[d] for d in order])
    ax.set_yticklabels(labels)
    for t, d in zip(ax.get_yticklabels(), order):
        t.set_color(INK if d in (CALL, RUNNER) else INK2)
        if d == CALL:
            t.set_fontweight("bold")
    # the gap between the recommended desk and the runner-up, on the extra-clicks stage
    xb = 1.5e5
    yc, yr = ys[CALL], ys[RUNNER]
    ax.plot([xb * 1.12, xb, xb, xb * 1.12], [yc, yc, yr, yr], color=INK2, lw=1)
    ax.text(xb / 1.1, (yc + yr) / 2, "gap\n{:,}".format(r50k(GAP)), ha="right", va="center", fontsize=8, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(1.6e4, 8e8)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.xaxis.set_major_formatter(FuncFormatter(tick))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticks([1e5, 1e6, 1e7, 1e8])
    ax.set_xlabel("Article clicks, 2027 (log scale)", color=INK2)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", which="both", colors=INK2, length=0)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=2, frameon=False, fontsize=7.5,
              handletextpad=0.2, columnspacing=1.0)
    fig.suptitle("{} gains most from the squad: {:,} extra article clicks in 2027"
                 .format(NAME[CALL], asks[CALL]["extra"]),
                 x=0.02, ha="left", y=0.985, fontsize=10.5, fontweight="bold", color=INK)
    fig.text(0.02, 0.012, "Desks ordered by extra clicks. Source: 2027 audience plan; pageviews by source, "
             "Oct 2025 to Sep 2026; headline test archive.", fontsize=7, color=MUTED)
    fig.subplots_adjust(left=0.22, right=0.98, top=0.80, bottom=0.17)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


# ============================================================================ the workbook
def write_xlsx(path):
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    head_fill = PatternFill("solid", fgColor="1F3A5F")
    head_font = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    body = Font(name="Calibri", size=10)
    pick_fill = PatternFill("solid", fgColor="FDF0E8")

    def header(ws, row, cols, widths):
        for j, (h, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=j, value=h)
            c.font, c.fill = head_font, head_fill
            c.alignment = Alignment(horizontal="center" if j > 1 else "left", vertical="center", wrap_text=True)
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[row].height = 42

    # ---- Desks
    ws = wb.active
    ws.title = "Desks"
    ws["A1"] = "Headline squad 2027: shortlisted desks"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = "Extra clicks are for calendar 2027. Readers, corrections and minutes cover October 2025 to September 2026."
    ws["A2"].font = Font(name="Calibri", italic=True, size=9, color="595959")
    cols = ["Desk", "Code", "Extra article clicks 2027", "Average monthly readers", "Extra clicks per reader",
            "Headline corrections", "Corrections per 1,000 articles", "Median minutes to first headline correction"]
    header(ws, 4, cols, [22, 8, 14, 14, 12, 13, 14, 17])
    fmts = [None, None, "#,##0", "#,##0", "0.0", "#,##0", "0.0", "#,##0"]
    for i, d in enumerate(order):
        a = asks[d]
        vals = [NAME[d], d, a["extra"], a["readers"], a["per_reader"], a["corrections"], a["rate"], a["median"]]
        for j, (v, f) in enumerate(zip(vals, fmts), 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.font = Font(name="Calibri", size=10, bold=(d == CALL and j == 1))
            c.border = Border(bottom=thin)
            if f:
                c.number_format = f
                c.alignment = Alignment(horizontal="right")
            if d == CALL:
                c.fill = pick_fill
    r = 5 + len(order) + 1
    ws.cell(row=r, column=1, value="Recommended: {}. Runner-up {}, {:,} extra clicks behind."
            .format(NAME[CALL], NAME[RUNNER], r50k(GAP))).font = Font(name="Calibri", size=10, bold=True)
    ws.cell(row=r + 1, column=1, value="Back-test: the method gets {} of the squad's 7 finished embeddings within 2% of "
            "the clicks each actually added (Back-test sheet).".format(HITS)).font = body
    ws.cell(row=r + 2, column=1, value="Desks in order of extra clicks. Click totals to the nearest 50,000; readers to the "
            "nearest thousand; definitions on the Notes sheet.").font = Font(name="Calibri", size=9, color="595959")
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = "A4:H%d" % (4 + len(order))
    ws.print_area = "A1:H%d" % (r + 2)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # ---- Click chain
    ws = wb.create_sheet("Click chain")
    ws["A1"] = "From each desk's 2027 clicks to the clicks the squad adds"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    cols = ["Desk", "2027 planned clicks", "Clicks from Bightline surfaces", "of which on headlines the desk tests",
            "On headlines the desk does not test", "Shrunk winning lift", "Extra article clicks 2027"]
    header(ws, 3, cols, [22, 15, 15, 15, 15, 11, 14])
    for i, d in enumerate(order):
        c = chain[d]
        vals = [NAME[d], r50k(c["planned"]), r50k(c["platform"]), r50k(c["platform_tested"]), r50k(c["untested"]),
                c["lift"], r50k(c["extra"])]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=4 + i, column=j, value=v)
            cell.font = Font(name="Calibri", size=10, bold=(d == CALL and j == 1))
            cell.border = Border(bottom=thin)
            if j > 1:
                cell.number_format = "0.00%" if j == 6 else "#,##0"
                cell.alignment = Alignment(horizontal="right")
            if d == CALL:
                cell.fill = pick_fill
    n = 4 + len(order) + 1
    notes = ["Bightline surfaces: web home, web section fronts, app home feed, app section tabs and related links. "
             "Search, Discover, partner apps, social, newsletters and alerts show the headline stored at publication.",
             "A desk's own tests ship their winners inside the clicks the plan carries forward, so the squad's gain is "
             "counted only on headlines the desk does not already test.",
             "Extra clicks = shrunk winning lift x clicks on headlines the desk does not test, on unrounded clicks. "
             "Click columns rounded to the nearest 50,000."]
    for k, t in enumerate(notes):
        ws.cell(row=n + k, column=1, value=t).font = Font(name="Calibri", size=9, color="595959")
    ws.freeze_panes = "B4"

    # ---- Back-test
    ws = wb.create_sheet("Back-test")
    ws["A1"] = "The method against the squad's seven finished embeddings"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    cols = ["Embedding", "Desk", "Year", "Tests", "Observed winning lift", "Shrunk winning lift",
            "Planned clicks (m)", "Prediction against realised", "Within 2%"]
    header(ws, 3, cols, [11, 12, 7, 7, 11, 11, 11, 13, 9])
    for i, b in enumerate(backtest):
        vals = [b["n"], b["desk"], b["year"], b["tests"], round(b["observed"] / 100, 4), b["shrunk"], b["planned_m"],
                b["diff"], "Yes" if abs(b["diff"]) <= BACKTEST_TOL else "No"]
        f = ["0", None, "0", "0", "0.0%", "0.00%", "0.0", "+0.0%;-0.0%;0.0%", None]
        for j, (v, fm) in enumerate(zip(vals, f), 1):
            cell = ws.cell(row=4 + i, column=j, value=v)
            cell.font = body
            cell.border = Border(bottom=thin)
            if fm:
                cell.number_format = fm
            cell.alignment = Alignment(horizontal="left" if j == 2 else "right")
    n = 4 + len(backtest)
    ws.cell(row=n, column=1, value="Within 2%").font = Font(name="Calibri", size=10, bold=True)
    ws.cell(row=n, column=9, value="{} of 7".format(HITS)).font = Font(name="Calibri", size=10, bold=True)
    ws.cell(row=n, column=9).alignment = Alignment(horizontal="right")
    ws.cell(row=n + 2, column=1, value="Prediction = shrunk winning lift x the desk's planned clicks for the year; realised "
            "incremental clicks from the change log, measured against matched desks.").font = Font(name="Calibri", size=9,
                                                                                                   color="595959")
    ws.freeze_panes = "A4"

    # ---- Notes
    ws = wb.create_sheet("Notes")
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 100
    ws["A1"] = "Definitions and sources"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    defs = [
        ("Prepared", "19 October 2026, for the planning meeting on 4 November 2026"),
        ("Extra article clicks 2027", "Clicks the squad would add in the twelve months after it embeds, counted at the "
         "owning desk. 2027 clicks are the audience plan's, which holds each desk at October 2025 to September 2026."),
        ("Winning lift", "Shipped headline's click-through over the control's, minus one; zero when the control is kept "
         "(field reference). Shrunk with one normal prior fitted by maximum likelihood on all {:,} variant packages "
         "in the archive; a desk's lift is the mean over its tests.".format(N_PACKAGES)),
        ("Average monthly readers", "Panel unique audience for the desk's section, mean of October 2025 to September "
         "2026. Each release's section codes are read on the section list it was issued on, so the November 2025 to "
         "February 2026 history release uses the 2026 list; a later release of a month replaces the earlier one."),
        ("Extra clicks per reader", "Extra article clicks 2027 over average monthly readers."),
        ("Headline corrections", "A new correction note on a version readers saw that published a corrected headline, "
         "the article's own or a live-blog entry's (editorial standards 7.4 and 7.5). Versions readers saw are live "
         "saves and a scheduled version the CMS published; drafts saved while an article is live are not published. "
         "Notes carry forward on later saves and are not counted again; body-text corrections are excluded."),
        ("Articles", "Articles first published October 2025 to September 2026 that went live. Live-blog posts, "
         "copies restored after the 14 November 2025 Brisbane outage and documents carried across at the "
         "1 October 2025 CMS migration are not separate articles; a restored copy continues its original."),
        ("Median minutes", "Minutes from an article going live (for a scheduled article the CMS published, its "
         "publish time) to its first headline correction, over corrected articles."),
        ("Sources", "2027 audience plan; pageviews by source and age, Oct 2025 to Sep 2026; headline test archive "
         "2019 to 2026; newsroom staff list; headline squad change log; panel monthly audience and reference "
         "workbook; CMS revisions for the web desks."),
    ]
    for i, (k, v) in enumerate(defs):
        a = ws.cell(row=3 + i, column=1, value=k)
        a.font = Font(name="Calibri", size=10, bold=True)
        a.alignment = Alignment(vertical="top")
        b = ws.cell(row=3 + i, column=2, value=v)
        b.font = body
        b.alignment = Alignment(wrap_text=True, vertical="top")
    head_rows = {"Desks": "4:4", "Click chain": "3:3", "Back-test": "3:3"}
    for w in wb.worksheets:
        w.page_margins = PageMargins(left=0.5, right=0.5, top=0.6, bottom=0.6)
        w.sheet_view.showGridLines = w.title == "Notes"
        if w.title in head_rows:
            w.print_title_rows = head_rows[w.title]
        if w.title != "Desks":
            w.print_area = "A1:%s%d" % (get_column_letter(w.max_column), w.max_row)
            w.page_setup.orientation = "portrait" if w.title == "Notes" else "landscape"
            w.page_setup.fitToWidth = 1
            w.page_setup.fitToHeight = 0
            w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.properties.creator = "Newsroom planning"
    wb.properties.lastModifiedBy = "Newsroom planning"
    wb.properties.title = "Headline squad 2027 placement"
    stamp = dt.datetime(2026, 10, 19, 9, 0)
    wb.properties.created = stamp
    wb.properties.modified = stamp
    wb.save(path)


# ============================================================================ the paper
def footer_page_number(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Bightline News | Internal | Page ")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
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


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexfill)
    tcPr.append(sh)


def para(doc, text="", size=10.5, bold=False, italic=False, space_after=6, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        r.font.size, r.bold, r.italic = Pt(size), bold, italic
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
    return p


def runs(p, parts, size=10.5):
    for t in parts:
        sup = isinstance(t, tuple)
        r = p.add_run(t[0] if sup else t)
        r.font.size = Pt(size)
        r.font.superscript = sup
    return p


def write_docx(path, png):
    c, rn = chain[CALL], chain[RUNNER]
    pct = lambda x, k=1: ("{:.%df}%%" % k).format(100 * x)  # noqa: E731
    tested_share = {d: chain[d]["platform_tested"] / chain[d]["platform"] for d in SHORTLIST}
    plat_share = {d: chain[d]["platform"] / chain[d]["planned"] for d in SHORTLIST}
    dash = {}
    lines = open(find("experimentation_dashboard_export"), encoding="utf-8").read().splitlines()
    h = lines.index("vertical,tests_concluded,tests_with_variant_shipped,avg_winning_lift_pct")
    for row in csv.reader(lines[h + 1:]):
        dash[row[0]] = float(row[3])

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    hp = sec.header.paragraphs[0]
    hr = hp.add_run("Newsroom planning | Paper for the planning meeting, Wednesday 4 November 2026")
    hr.font.size = Pt(8)
    hr.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    footer_page_number(sec)

    para(doc, "Headline squad 2027: send the squad to {}".format(NAME[CALL]), size=16, bold=True, space_after=2)
    para(doc, "Owner: Corey Cox, Managing editor | Version 1, 19 October 2026 | Internal", size=9,
         color="595959", space_after=2)
    para(doc, "Distribution: Lisa Jennings, Kayla Torres, Nina Franklin, Jason Anderson; editors of the six "
         "shortlisted desks", size=9, color="595959", space_after=12)

    p = para(doc, space_after=8)
    r = p.add_run("Recommendation. The squad should join {} in January. It would add {:,} extra article "
                  "clicks there in 2027.".format(NAME[CALL], asks[CALL]["extra"]))
    r.bold, r.font.size = True, Pt(11)
    runs(p, [" The runner-up is {}, at {:,}, which sits {:,} behind.".format(NAME[RUNNER], asks[RUNNER]["extra"], r50k(GAP))], size=11)

    doc.add_heading("How the number is built", level=2)
    runs(para(doc), [
        "The brief judges the squad on incremental article clicks in the twelve months after it embeds, counted at "
        "the owning desk. Three things stand between a desk's 2027 clicks and what the squad would add to them."])
    runs(para(doc), [
        "First, the lift. A desk's average winning lift over-reads what a winning headline is worth, because the "
        "variant that wins a small test is usually the one that drew a lucky sample. Each shipped variant is shrunk "
        "toward one prior fitted on every package in the test archive, and the desk's lift is the mean over its "
        "tests. On that basis {} lifts clicks by {} on the headlines it tests. The same rule gets {} of the "
        "squad's 7 finished embeddings within 2% of the clicks each actually added; the raw lift gets {} of them."
        .format(NAME[CALL], pct(c["lift"], 2), HITS, RAW_HITS), ("1",)])
    runs(para(doc), [
        "Second, where the click starts. A tested headline only shows on Bightline's own surfaces: the web and app "
        "home pages, section fronts and related links. Search, Discover, partner apps, social cards, newsletters and "
        "alerts carry the headline stored at publication, which a test does not change. {} of {}'s 2027 clicks "
        "start on our own surfaces, against {} for {}."
        .format(pct(plat_share[CALL]), NAME[CALL], pct(plat_share[RUNNER]), NAME[RUNNER]), ("2",)])
    runs(para(doc), [
        "Third, the tests each desk already runs. Every test in the archive at a shortlisted desk was set up by that "
        "desk's own staff, and their winners are already live inside the clicks the plan carries into 2027. The "
        "squad cannot add that gain a second time. {}'s editors already test the headlines behind {} of its "
        "platform clicks, so most of its large reachable base is spoken for. {}'s editors ran {} tests in the year, on "
        "articles carrying {} of its platform clicks, which leaves the squad {:,} clicks on untested headlines. "
        "At {} that is {:,}."
        .format(NAME[RUNNER], pct(tested_share[RUNNER]), NAME[CALL], len(by_desk[CALL]), pct(tested_share[CALL]),
                r50k(c["untested"]), pct(c["lift"], 2), asks[CALL]["extra"])])

    doc.add_picture(png, width=Cm(16.4))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, "Chart: each desk from its 2027 clicks to the extra clicks the squad would add. Desks ordered by extra "
         "clicks.", size=8.5, italic=True, color="595959", space_after=10)

    doc.add_heading("Why not the other five", level=2)
    why = {
        "LOC-M": "the largest reachable base on the list ({} of its clicks start on our surfaces), but its own "
                 "editors already test the headlines behind {} of them.".format(pct(plat_share["LOC-M"]),
                                                                          pct(tested_share["LOC-M"])),
        "BUS-N": "big, steady tests and the strongest shrunk lift on the national list ({}), but {} of its clicks "
                 "arrive on surfaces that show the stored headline.".format(pct(shr["BUS-N"], 2),
                                                                           pct(1 - plat_share["BUS-N"])),
        "SPT-N": "a large audience, but a modest lift ({}) and half its platform clicks already on tested "
                 "headlines.".format(pct(shr["SPT-N"], 2)),
        "POL-N": "leads on the dashboard's Politics figure ({:.2f}%), but that average is pulled up by Politics·metro's "
                 "small Brisbane tests; Politics·national's own tests shrink to {}.".format(dash["Politics"],
                                                                                          pct(shr["POL-N"], 2)),
        "SPT-M": "the highest raw winning lift in the archive ({}), drawn from very small tests; shrunk, it is "
                 "{}.".format(pct(raw["SPT-M"]), pct(shr["SPT-M"], 2)),
    }
    for d in order[1:]:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run("{} ({:,}): ".format(NAME[d], asks[d]["extra"]))
        r.bold, r.font.size = True, Pt(10.5)
        runs(p, [why[d]])

    doc.add_heading("Readers and the standards record", level=2)
    runs(para(doc), [
        "Kayla's case is that the squad belongs where the readers are. Politics·national has the most, {:,} a "
        "month, but readers do not change which headlines the squad can still move. Per reader, {} returns {:.1f} "
        "extra clicks, behind only {} ({:.1f}). {} also carries a light corrections record: {} headline corrections "
        "in the year, {:.1f} per 1,000 articles. The full set is below and in the workbook."
        .format(asks["POL-N"]["readers"], NAME[CALL], asks[CALL]["per_reader"], NAME[RUNNER],
                asks[RUNNER]["per_reader"], NAME[CALL], asks[CALL]["corrections"], asks[CALL]["rate"]), ("3",)])

    cols = ["Desk", "Extra clicks 2027", "Monthly readers", "Extra per reader", "Headline corrections",
            "Per 1,000 articles", "Median minutes"]
    t = doc.add_table(rows=1, cols=len(cols))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for j, h in enumerate(cols):
        cell = t.rows[0].cells[j]
        cell.text = ""
        rr = cell.paragraphs[0].add_run(h)
        rr.bold, rr.font.size = True, Pt(8.5)
        rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade(cell, "1F3A5F")
    for d in order:
        a = asks[d]
        vals = [NAME[d], "{:,}".format(a["extra"]), "{:,}".format(a["readers"]), "{:.1f}".format(a["per_reader"]),
                str(a["corrections"]), "{:.1f}".format(a["rate"]), str(a["median"])]
        cells = t.add_row().cells
        for j, v in enumerate(vals):
            cells[j].text = ""
            pp = cells[j].paragraphs[0]
            rr = pp.add_run(v)
            rr.font.size = Pt(9)
            rr.bold = d == CALL and j == 0
            if j:
                pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if d == CALL:
                shade(cells[j], "FDF0E8")
    for row in t.rows:
        row.cells[0].width = Cm(3.6)
    para(doc, "Source: 2027 audience plan; pageviews by source; headline test archive; panel monthly audience "
         "(restated releases); CMS revisions for the web desks. Readers, corrections and minutes cover October 2025 "
         "to September 2026.", size=8, italic=True, color="595959", space_after=10)

    doc.add_heading("Notes", level=3)
    notes = [
        "Prior fitted by maximum likelihood on all {:,} variant packages; a control that is kept counts as zero "
        "lift. Embedding-by-embedding results are on the workbook's Back-test sheet.".format(N_PACKAGES),
        "Source codes as defined in the audience warehouse field reference. The 2027 plan holds every desk at its "
        "October 2025 to September 2026 clicks, with no change in where they come from.",
        "Readers are the panel's unique audience for the desk's section, each release read on the section list it "
        "was issued on; the history release for November 2025 to February 2026 and the restated April to June "
        "release replace the earlier ones. A headline correction is counted on the version that published the "
        "corrected headline, a live-blog entry's included (editorial standards 7.4 and 7.5); an article goes live "
        "when it is first published, at its publish time if the CMS published it.",
    ]
    for i, n in enumerate(notes, 1):
        para(doc, "{}  {}".format(i, n), size=8.5, color="404040", space_after=3)

    cp = doc.core_properties
    cp.author = "Corey Cox"
    cp.last_modified_by = "Corey Cox"
    cp.title = "Headline squad 2027 placement"
    cp.comments = ""
    cp.created = dt.datetime(2026, 10, 19, 9, 0)
    cp.modified = dt.datetime(2026, 10, 19, 9, 0)
    cp.revision = 1
    doc.save(path)


def repack(path, when=dt.datetime(2026, 10, 19, 9, 0)):
    """Fixed entry times and the paper's own date in docProps, so a rebuild is byte-identical."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    iso = when.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    data["docProps/core.xml"] = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*", rb"\g<1>" + iso,
                                       data["docProps/core.xml"])
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[i.filename])
    os.utime(path, (when.timestamp(), when.timestamp()))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write_xlsx(OUT / "squad_placement_2027.xlsx")
    write_docx(OUT / "squad_placement_2027.docx", chart_png())
    # the writing libraries stamp their own names into docProps; replace with the newsroom's own
    scrub = HERE.parents[1] / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
    subprocess.run([sys.executable, str(scrub), str(OUT), "--apply", "--producer", "Bightline News",
                    "--stamp", "2026-10-19"], capture_output=True, text=True)
    audit = subprocess.run([sys.executable, str(scrub), str(OUT), "--floor", "2026-01-01", "--ceiling", "2026-10-19"],
                           capture_output=True, text=True)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    for f in ("squad_placement_2027.xlsx", "squad_placement_2027.docx"):
        repack(OUT / f)

    print("prior: maximum likelihood on %d packages, mean %.3f%%, sd %.3f%%" % (N_PACKAGES, 100 * MU, 100 * TAU2 ** .5))
    print("\nCALL  %s  %s extra article clicks in 2027 (unrounded %s)"
          % (NAME[CALL], "{:,}".format(asks[CALL]["extra"]), "{:,.0f}".format(chain[CALL]["extra"])))
    print("RUNNER-UP  %s  %s; gap %s (unrounded %s)" % (NAME[RUNNER], "{:,}".format(asks[RUNNER]["extra"]),
          "{:,}".format(r50k(GAP)), "{:,.0f}".format(GAP)))
    print("RAW LIFT BACK-TEST  %d of 7 within 2%%" % RAW_HITS)
    print("REFEREE  March 2026 headline and text corrections, seven web desks: %d and %d (bulletin %d and %d)"
          % (MARCH, MARCH_TEXT, MARCH_FILED, MARCH_TEXT_FILED))
    print("BACK-TEST  %d of 7 within 2%%  (worst %.2f%%)" % (HITS, 100 * max(abs(b["diff"]) for b in backtest)))
    print("\ncritical components")
    print("%-18s %10s %14s %14s %16s %12s" % ("desk", "shrunk", "platform shr", "desk-tested", "untested clicks",
                                             "extra"))
    for d in order:
        c = chain[d]
        print("%-18s %9.2f%% %13.1f%% %13.1f%% %16s %12s" % (
            NAME[d], 100 * c["lift"], 100 * c["platform"] / c["planned"], 100 * c["platform_tested"] / c["platform"],
            "{:,}".format(r50k(c["untested"])), "{:,}".format(asks[d]["extra"])))
    print("\nworkbook rows")
    for d in order:
        a = asks[d]
        print("%-18s extra %9s  readers %9s  per reader %.1f  corrections %d  rate %.1f  median %d min" % (
            NAME[d], "{:,}".format(a["extra"]), "{:,}".format(a["readers"]), a["per_reader"], a["corrections"],
            a["rate"], a["median"]))
    print("\nback-test")
    for b in backtest:
        print("#%d %-9s %d  %d tests  shrunk %.2f%%  %+.2f%%" % (b["n"], b["desk"], b["year"], b["tests"],
                                                                100 * b["shrunk"], 100 * b["diff"]))


if __name__ == "__main__":
    main()
