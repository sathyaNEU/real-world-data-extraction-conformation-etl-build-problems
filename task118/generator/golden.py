"""Headline squad 2027 placement: the paper and its workbook.

python3 golden.py [target_dir] [out_dir]

Reads the planning-folder exports in target_dir and writes squad_placement_2027.docx and
squad_placement_2027.xlsx to out_dir. Prints the figures the paper rests on.
"""
import csv
import datetime as dt
import html
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
from matplotlib.lines import Line2D  # noqa: E402
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
AEST_OFFSET = dt.timedelta(hours=10)     # Brisbane, no daylight saving
BACKTEST_TOL = 0.02
FIX_AND_NOTE = 10       # minutes: a fix and its note go on one save or two saves this far apart (standards 7.3)


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


def vertical_lift(v):
    """The experimentation dashboard's figure for a vertical, from the archive: the mean winning lift over the
    vertical's tests concluded in the twelve months to September 2026 (AEST)."""
    lo, hi = "2025-09-30T14:00:00Z", "2026-09-30T14:00:00Z"
    ids = [t for t, pk in tests.items()
           if desks[pk[0]["desk_code"]]["vertical"] == v and lo <= pk[0]["concluded_at"] < hi]
    return 100 * float(np.mean([win(t, False) for t in ids]))

# Every test at a shortlisted desk was created by that desk's own editors (staff list team), never the squad.
assert all(team[meta[t][3]] == meta[t][1] for d in SHORTLIST for t in by_desk[d])
assert len({m[2] for m in meta.values()}) == len(meta), "one test per article"

# --------------------------------------------------------------------------- the pages a shipped headline sits on
# Each page's click-through is the share of its views that end in an article click, over the twelve months (clicks
# over views). A shipped headline that wins a click on a page where the view would have ended in some other article
# click has moved that click, not added one: only the views that would otherwise have ended with no article click
# give Bightline a click it did not have.
page_views, page_clicks = defaultdict(int), defaultdict(int)
for r in csv.DictReader(open(find("page_performance_monthly"), encoding="utf-8")):
    page_views[r["page"]] += int(r["page_views"])
    page_clicks[r["page"]] += int(r["article_clickthroughs"])
CTR = {pg: page_clicks[pg] / page_views[pg] for pg in page_views}


def page_of(d, src):
    """The page on which a desk's article is clicked from one of Bightline's own surfaces."""
    dk = desks[d]
    metro = dk["edition"] == "Brisbane"
    name = dk["desk_name"].split("\u00b7")[0] if dk["distribution"] == "app only" else dk["vertical"]
    return {"home_web": "bightline.com.au/brisbane/" if metro else "bightline.com.au/",
            "section_web": "bightline.com.au/%s%s/" % ("brisbane/" if metro else "", name.lower()),
            "feed_app": "Home feed",
            "section_app": "Tab: %s%s" % ("Brisbane " if metro else "", name),
            "related_links": "Related stories (article pages)"}[src]


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
    chain[d] = {"planned": int(total), "platform": int(p or 0), "platform_tested": int(pt or 0), "articles": n_win,
                "by_source": {}}
for d, src, n in con.execute(f"""
        SELECT v.desk_code, source_code, sum(pageviews) FROM pv v LEFT JOIN tested t USING (article_id)
        WHERE source_code IN ({plat}) AND t.article_id IS NULL GROUP BY 1, 2""").fetchall():
    chain[d]["by_source"][src] = int(n)
for d in SHORTLIST:
    c = chain[d]
    assert c["planned"] == planned[d], d  # the plan carries the base year forward to the click
    c["untested"] = c["platform"] - c["platform_tested"]
    assert sum(c["by_source"].values()) == c["untested"], d
    c["lift"] = shr[d]
    c["won"] = shr[d] * c["untested"]       # the clicks the desk's shipped headlines would win, article by article
    c["new"] = sum(n * (1 - CTR[page_of(d, s)]) for s, n in c["by_source"].items())
    c["pass"] = c["new"] / c["untested"]    # the share of a won click that is new to Bightline
    c["extra"] = shr[d] * c["new"]
    c["new_won"] = c["extra"]

order = sorted(SHORTLIST, key=lambda d: chain[d]["extra"], reverse=True)
CALL, RUNNER = order[0], order[1]
GAP = chain[CALL]["extra"] - chain[RUNNER]["extra"]
MEASURED = sorted(SHORTLIST, key=lambda d: chain[d]["won"], reverse=True)

# --------------------------------------------------------------------------- back-test on the change log
erows = list(load_workbook(find("headline_squad_change_log"), read_only=True, data_only=True)["Embeddings"]
             .iter_rows(values_only=True))
emb = [dict(zip(erows[0], r)) for r in erows[1:] if r[0] is not None]
app_tests = defaultdict(list)
for t, m in meta.items():
    if m[0] == "app":
        app_tests[(m[1], int(m[4][:4]))].append(t)
app_mix = defaultdict(dict)
for d, src, n in con.execute(f"""
        SELECT desk_code, source_code, sum(pageviews) FROM pv WHERE source_code IN ({plat}) GROUP BY 1, 2""").fetchall():
    app_mix[d][src] = int(n)


def pass_through(d):
    mix = app_mix[d]
    return sum(n * (1 - CTR[page_of(d, s)]) for s, n in mix.items()) / sum(mix.values())


backtest = []
for e in emb:
    ids = app_tests[(e["desk_code"], e["started"].year)]
    assert len(ids) == e["tests_run"]
    lift = float(np.mean([win(t) for t in ids]))
    real = float(e["realised_holdback_lift_pct"]) / 100
    won = e["planned_clicks"] * real
    rho = pass_through(e["desk_code"])
    backtest.append({"n": e["embedding"], "desk": e["desk"], "code": e["desk_code"], "year": e["started"].year,
                     "tests": e["tests_run"], "observed": float(e["avg_winning_lift_pct"]), "shrunk": lift,
                     "realised": real, "diff": lift / real - 1, "planned": int(e["planned_clicks"]),
                     "won": won, "pass": rho, "predicted": won * rho, "extra": int(e["extra_clicks_vs_holdback"]),
                     "clicks_diff": won * rho / int(e["extra_clicks_vs_holdback"]) - 1,
                     "kept": int(e["extra_clicks_vs_holdback"]) / won})
HITS = sum(abs(b["diff"]) <= BACKTEST_TOL for b in backtest)
RAW_HITS = sum(abs(float(np.mean([win(t, False) for t in app_tests[(e["desk_code"], e["started"].year)]]))
                   / (float(e["realised_holdback_lift_pct"]) / 100) - 1) <= BACKTEST_TOL for e in emb)
CLICK_HITS = sum(abs(b["clicks_diff"]) <= BACKTEST_TOL for b in backtest)
AVG_KEPT = float(np.mean([b["kept"] for b in backtest]))     # one share kept for every embedding
AVG_HITS = sum(abs(b["won"] * AVG_KEPT / b["extra"] - 1) <= BACKTEST_TOL for b in backtest)
AVG_WORST = max(abs(b["won"] * AVG_KEPT / b["extra"] - 1) for b in backtest)

# --------------------------------------------------------------------------- headline corrections (CMS)
docs, info = defaultdict(list), {}
for r in csv.DictReader(open(find("cms_revisions_web_desks"), encoding="utf-8")):
    # an autosave of a live article's working copy is saved while the article is live but publishes nothing
    status = "autosave" if r["save_type"] == "autosave" else r["status"]
    docs[r["doc_id"]].append((int(r["revision"]), r["saved_at"], status, r["publish_at_aest"], r["headline_sha1"],
                              r["correction_note"]))
    info[r["doc_id"]] = (r["desk_code"], r["doc_type"], r["parent_doc"], r["restored_from_doc"], r["migrated_from"])
restored_copy = {v[3]: k for k, v in info.items() if v[3]}
when = lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%MZ")  # noqa: E731
# a scheduled publish time is the Brisbane time the editor set: every article the CMS published went live at it,
# minutes before its first live save, once it is read on the saves' clock
when_set = lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%M") - AEST_OFFSET  # noqa: E731

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
    # what readers saw: each live save, and a scheduled version the CMS published at publish_at, which it does only if
    # the article is still scheduled when that time comes (one set back to draft first went live at its first live save)
    published, went_live = live, when(live[0][1])
    scheduled = [r for r in revs if r[2] == "scheduled" and r[0] < live[0][0]]
    if scheduled and scheduled[-1][3] and when_set(scheduled[-1][3]) < went_live:
        due = when_set(scheduled[-1][3])
        held = [r for r in revs if r[0] < live[0][0] and when(r[1]) <= due][-1]
        if held[2] == "scheduled" and held[3] == scheduled[-1][3]:
            published, went_live = [scheduled[-1]] + live, due
    first, fixed_alone = None, None     # a corrected headline published before its note, since the last note change
    shown, paired_later = {published[0][5]}, set()
    for k in range(1, len(published)):
        prev, cur = published[k - 1], published[k]
        t = when(cur[1])
        # a note carries forward until cleared, so a correction is a new note on a published version; a note the
        # article had already shown, put back after a save that left it off, is not a new one
        put_back = cur[5] in shown
        shown.add(cur[5])
        if not cur[5] or cur[5] == prev[5] or put_back:
            if cur[5] != prev[5]:
                fixed_alone = None
            elif cur[4] != prev[4] and k not in paired_later:
                fixed_alone = t
            continue
        apart = dt.timedelta(minutes=FIX_AND_NOTE)
        entries = [f for f in entry_fixed.get(did, []) if t - apart <= f <= t + apart]
        later = None
        if cur[4] == prev[4]:
            for j in range(k + 1, len(published)):
                if when(published[j][1]) - t > apart or published[j][5] != published[j - 1][5]:
                    break
                if published[j][4] != published[j - 1][4]:
                    later = j
                    break
        if cur[4] != prev[4]:
            at = t
        elif fixed_alone is not None and t - fixed_alone <= apart:
            at = fixed_alone        # the corrected headline went up on a save just before its note (7.4)
        elif later is not None:
            at = when(published[later][1])      # or on a save just after it (7.4)
            paired_later.add(later)
        elif entries:
            at = min(entries)       # an entry's corrected headline, its note on the live blog (7.5)
        else:
            at = None
        fixed_alone = None
        if at is not None:
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
    asks[d] = {"extra": r50k(chain[d]["extra"]),
               "corrections": corr[d], "corrected": len(mins[d]), "median": int(statistics.median(mins[d])),
               "hour": sum(m <= 60 for m in mins[d]), "three": sum(m > 180 for m in mins[d])}
    # no first correction sits on the hour or the three-hour mark, so "within" and "more than" read one way
    assert not any(58 <= m <= 62 or 178 <= m <= 182 for m in mins[d]), (d, sorted(mins[d]))

# ============================================================================ the chart
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
WON_C, NEW_C = "#2a78d6", "#1baf7a"
HILITE = "#f1f0ec"


def tick(x, _):
    return "{:,.0f}k".format(x / 1e3) if x else "0"


def chart_png():
    """Each desk's clicks its shipped headlines would win (ring) against the clicks that are new to Bightline (dot),
    desks in order of the new clicks."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=200)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ys = {d: len(order) - 1 - i for i, d in enumerate(order)}
    for d in (CALL, RUNNER):
        ax.axhspan(ys[d] - 0.42, ys[d] + 0.42, color=HILITE, zorder=0, lw=0)
    for d in order:
        c = chain[d]
        ax.plot([c["new_won"], c["won"]], [ys[d]] * 2, color="#c9c8c2", lw=1.6, zorder=1, solid_capstyle="round")
        ax.scatter([c["won"]], [ys[d]], s=52, facecolor=SURF, edgecolor=WON_C, linewidth=1.4, zorder=2)
        ax.scatter([c["extra"]], [ys[d]], s=64, color=NEW_C, edgecolor=SURF, linewidth=1.6, zorder=3)
        ax.text(c["extra"] - 2.2e4, ys[d], "{:,}".format(asks[d]["extra"]), ha="right", va="center", fontsize=8.5,
                color=INK, fontweight="bold" if d == CALL else "normal")
        ax.text(c["won"] + 2.2e4, ys[d], "{:,}".format(r50k(c["won"])), ha="left", va="center", fontsize=7.5,
                color=INK2)
    labels = [NAME[d] + ("\nrecommended" if d == CALL else "\nrunner-up" if d == RUNNER else "") for d in order]
    ax.set_yticks([ys[d] for d in order])
    ax.set_yticklabels(labels)
    for t, d in zip(ax.get_yticklabels(), order):
        t.set_color(INK if d in (CALL, RUNNER) else INK2)
        if d == CALL:
            t.set_fontweight("bold")
    ax.set_xlim(-1.2e5, 1.5e6)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.xaxis.set_major_formatter(FuncFormatter(tick))
    ax.set_xticks([0, 2.5e5, 5e5, 7.5e5, 1e6, 1.25e6])
    ax.set_xlabel("Article clicks, 2027", color=INK2)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", which="both", colors=INK2, length=0)
    keys = [Line2D([], [], ls="none", marker="o", ms=6.5, mfc=SURF, mec=WON_C, mew=1.4,
                   label="clicks the squad's winning headlines would win"),
            Line2D([], [], ls="none", marker="o", ms=7.5, mfc=NEW_C, mec=SURF, mew=1.2,
                   label="of which new to Bightline (extra clicks)")]
    ax.legend(handles=keys, loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=2, frameon=False, fontsize=7.5,
              handletextpad=0.3, columnspacing=1.2)
    fig.suptitle("{} adds the most clicks new to Bightline: {:,} in 2027".format(NAME[CALL], asks[CALL]["extra"]),
                 x=0.02, ha="left", y=0.985, fontsize=10.5, fontweight="bold", color=INK)
    fig.text(0.02, 0.012, "Desks ordered by extra clicks. Source: 2027 audience plan; pageviews by source; page "
             "performance; headline test archive.", fontsize=7, color=MUTED)
    fig.subplots_adjust(left=0.22, right=0.98, top=0.80, bottom=0.17)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


# ============================================================================ the workbook
PAGE_ORDER = ["bightline.com.au/", "bightline.com.au/brisbane/"]


def write_xlsx(path):
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    head_fill = PatternFill("solid", fgColor="1F3A5F")
    head_font = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    body = Font(name="Calibri", size=10)
    note_font = Font(name="Calibri", size=9, color="595959")
    pick_fill = PatternFill("solid", fgColor="FDF0E8")

    def header(ws, row, cols, widths):
        for j, (h, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=j, value=h)
            c.font, c.fill = head_font, head_fill
            c.alignment = Alignment(horizontal="center" if j > 1 else "left", vertical="center", wrap_text=True)
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[row].height = 42

    def put(ws, row, vals, fmts, bold_first=False, fill=None):
        for j, (v, f) in enumerate(zip(vals, fmts), 1):
            c = ws.cell(row=row, column=j, value=v)
            c.font = Font(name="Calibri", size=10, bold=(bold_first and j == 1))
            c.border = Border(bottom=thin)
            if f:
                c.number_format = f
                c.alignment = Alignment(horizontal="right")
            if fill:
                c.fill = fill

    # ---- Desks: the workbook row for every shortlisted desk
    ws = wb.active
    ws.title = "Desks"
    ws["A1"] = "Headline squad 2027: shortlisted desks"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = ("Corrections: articles first published from October 2025 to September 2026 whose headline was "
                "corrected.")
    ws["A2"].font = Font(name="Calibri", italic=True, size=9, color="595959")
    cols = ["Desk", "Code",
            "Median minutes to first headline correction", "First corrections within an hour",
            "First corrections after more than three hours"]
    header(ws, 4, cols, [22, 8, 17, 14, 15])
    fmts = [None, None, "#,##0", "#,##0", "#,##0"]
    for i, d in enumerate(SHORTLIST):
        a = asks[d]
        put(ws, 5 + i, [NAME[d], d, a["median"], a["hour"], a["three"]], fmts,
            bold_first=(d == CALL), fill=pick_fill if d == CALL else None)
    r = 5 + len(SHORTLIST) + 1
    ws.cell(row=r, column=1, value="Recommended: {}, {:,} extra article clicks in 2027. Runner-up {}, {:,} behind."
            .format(NAME[CALL], asks[CALL]["extra"], NAME[RUNNER], r50k(GAP))).font = Font(name="Calibri", size=10,
                                                                                         bold=True)
    ws.cell(row=r + 1, column=1, value="Extra clicks for every desk are on the Click chain sheet.").font = note_font
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = "A4:E%d" % (4 + len(SHORTLIST))
    ws.print_area = "A1:E%d" % (r + 1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # ---- Click chain
    ws = wb.create_sheet("Click chain")
    ws["A1"] = "From each desk's 2027 clicks to the clicks the squad adds to Bightline"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    cols = ["Desk", "2027 planned clicks", "From Bightline's own pages", "of which on headlines the desk tests",
            "On headlines the desk does not test", "Shrunk winning lift", "Clicks the winning headlines win",
            "Share new to Bightline", "Extra article clicks 2027"]
    header(ws, 3, cols, [22, 15, 15, 15, 15, 11, 14, 11, 14])
    fmts = [None, "#,##0", "#,##0", "#,##0", "#,##0", "0.00%", "#,##0", "0.0%", "#,##0"]
    for i, d in enumerate(order):
        c = chain[d]
        put(ws, 4 + i, [NAME[d], r50k(c["planned"]), r50k(c["platform"]), r50k(c["platform_tested"]),
                        r50k(c["untested"]), c["lift"], r50k(c["won"]), c["pass"], r50k(c["extra"])], fmts,
            bold_first=(d == CALL), fill=pick_fill if d == CALL else None)
    n = 4 + len(order) + 1
    notes = ["Bightline's own pages: the web home pages and section fronts, the app home feed and tabs, and the "
             "related-story links on article pages. Search, Discover-style cards, partner apps, social cards, "
             "newsletters and alerts keep the headline stored at publication.",
             "The squad takes the headlines a desk has not put under test itself; a desk's own winners already ship "
             "inside the clicks the plan carries forward.",
             "A winning headline's extra clicks on a page are new to Bightline only in the share of that page's views "
             "that would otherwise end with no article click (one minus the page's click-through, Pages sheet); the "
             "rest are clicks the headlines beside it lose.",
             "Extra clicks = shrunk winning lift x each page's untested clicks x (1 - that page's click-through), on "
             "unrounded clicks. Click columns rounded to the nearest 50,000."]
    for k, t in enumerate(notes):
        ws.cell(row=n + k, column=1, value=t).font = note_font
    ws.freeze_panes = "B4"

    # ---- Pages
    ws = wb.create_sheet("Pages")
    ws["A1"] = "Page click-through, October 2025 to September 2026"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    cols = ["Page", "Page views", "Article click-throughs", "Click-through", "Share of views new clicks can come from"]
    header(ws, 3, cols, [36, 16, 16, 12, 14])
    pages = sorted(CTR, key=lambda pg: (pg.startswith("Tab") or pg.startswith("Home") or pg.startswith("Related"), pg))
    for i, pg in enumerate(pages):
        put(ws, 4 + i, [pg, page_views[pg], page_clicks[pg], CTR[pg], 1 - CTR[pg]],
            [None, "#,##0", "#,##0", "0.0%", "0.0%"])
    ws.cell(row=5 + len(pages), column=1, value="Click-through = article click-throughs over page views, twelve "
            "months summed (page performance export).").font = note_font
    ws.freeze_panes = "B4"

    # ---- Back-test
    ws = wb.create_sheet("Back-test")
    ws["A1"] = "The method against the squad's seven finished embeddings"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    cols = ["Embedding", "Desk", "Year", "Tests", "Observed winning lift", "Shrunk winning lift",
            "Realised holdback lift", "Lift: prediction against realised", "Planned clicks",
            "Share new to Bightline", "Predicted extra clicks", "Extra clicks against holdback",
            "Clicks: prediction against measured"]
    header(ws, 3, cols, [11, 12, 7, 7, 11, 11, 11, 13, 14, 11, 14, 14, 13])
    for i, b in enumerate(backtest):
        vals = [b["n"], b["desk"], b["year"], b["tests"], round(b["observed"] / 100, 4), b["shrunk"], b["realised"],
                b["diff"], b["planned"], b["pass"], round(b["predicted"]), b["extra"], b["clicks_diff"]]
        f = ["0", None, "0", "0", "0.0%", "0.00%", "0.00%", "+0.0%;-0.0%;0.0%", "#,##0", "0.0%", "#,##0", "#,##0",
             "+0.0%;-0.0%;0.0%"]
        for j, (v, fm) in enumerate(zip(vals, f), 1):
            cell = ws.cell(row=4 + i, column=j, value=v)
            cell.font = body
            cell.border = Border(bottom=thin)
            if fm:
                cell.number_format = fm
            cell.alignment = Alignment(horizontal="left" if j == 2 else "right")
    n = 4 + len(backtest)
    ws.cell(row=n, column=1, value="Within 2%").font = Font(name="Calibri", size=10, bold=True)
    for col, hits in ((8, HITS), (13, CLICK_HITS)):
        ws.cell(row=n, column=col, value="{} of 7".format(hits)).font = Font(name="Calibri", size=10, bold=True)
        ws.cell(row=n, column=col).alignment = Alignment(horizontal="right")
    for k, t in enumerate([
            "Lift: the shrunk winning lift of the embedding's tests against the change log's realised lift over the "
            "5 per cent reader holdback. The raw winning lift is within 2% for {} of 7.".format(RAW_HITS or "none"),
            "Clicks: planned clicks x realised lift x the desk's share new to Bightline (its pages' click-through, "
            "weighted by where its clicks start) against the extra clicks measured against the holdback. One share "
            "for every embedding, their average {:.1%}, is within 2% for {} of 7 and misses by up to {:.0%}."
            .format(AVG_KEPT, AVG_HITS, AVG_WORST)]):
        ws.cell(row=n + 2 + k, column=1, value=t).font = note_font
    ws.freeze_panes = "A4"

    head_rows = {"Desks": "4:4", "Click chain": "3:3", "Pages": "3:3", "Back-test": "3:3"}
    for w in wb.worksheets:
        w.page_margins = PageMargins(left=0.5, right=0.5, top=0.6, bottom=0.6)
        w.sheet_view.showGridLines = False
        w.print_title_rows = head_rows[w.title]
        if w.title != "Desks":
            w.print_area = "A1:%s%d" % (get_column_letter(w.max_column), w.max_row)
            w.page_setup.orientation = "landscape"
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
    cul = chain["CUL-N"]
    pct = lambda x, k=0: ("{:.%df}%%" % k).format(100 * x)  # noqa: E731
    tested_share = {d: chain[d]["platform_tested"] / chain[d]["platform"] for d in SHORTLIST}
    src_share = lambda d, src: chain[d]["by_source"].get(src, 0) / chain[d]["untested"]  # noqa: E731

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
    para(doc, "Distribution: Lisa Jennings, Kayla Torres, Nina Franklin, Willie Smith; editors of the six "
         "shortlisted desks", size=9, color="595959", space_after=12)

    p = para(doc, space_after=8)
    r = p.add_run("Recommendation. The squad should join {} in January. It would add {:,} article clicks to "
                  "Bightline there in 2027.".format(NAME[CALL], asks[CALL]["extra"]))
    r.bold, r.font.size = True, Pt(11)
    runs(p, [" The runner-up is {}, at {:,}, which sits {:,} behind.".format(NAME[RUNNER], asks[RUNNER]["extra"],
                                                                         r50k(GAP))], size=11)

    doc.add_heading("How the number is built", level=2)
    runs(para(doc), [
        "The brief judges the squad the way Experimentation closes an embedding: on the clicks readers make in its "
        "year that they would not have made without it. Three steps take a desk's 2027 clicks to that figure."])
    runs(para(doc), [
        "First, the lift. A desk's average winning lift over-reads what a winning headline is worth, because the "
        "variant that wins a small test is usually the one that drew a lucky sample. Each shipped variant is shrunk "
        "toward one prior fitted on every package in the test archive, and the desk's lift is the mean over its "
        "tests: {} for {}. The same rule comes within 2% of the realised holdback lift for {} of the squad's 7 "
        "finished embeddings; the raw lift does so for {}."
        .format(pct(c["lift"], 2), NAME[CALL], HITS, RAW_HITS or "none"), ("1",)])
    runs(para(doc), [
        "Second, the clicks a shipped headline can reach. It replaces the old headline only on Bightline's own pages: "
        "the home pages, section fronts, app feed and tabs, and the related-story links. The squad also takes only "
        "the headlines a desk has not put under test itself. That leaves {:,} of {}'s 2027 clicks; at its lift, its "
        "winning headlines would win {:,} clicks."
        .format(r50k(c["untested"]), NAME[CALL], r50k(c["won"]))])
    runs(para(doc), [
        "Third, how many of those clicks are new to Bightline. A page shows a fixed set of headlines. When a better "
        "headline wins a click from a reader who would have clicked something else on the page, Bightline has moved "
        "a click, not gained one. Only views that would otherwise end with no article click can give a new one, and "
        "the page analytics show how many those are. About four in five views of the Culture front and the Culture "
        "tab already end in a click ({} and {}), against fewer than one in eight on the related-story links ({}). "
        "{} of {}'s reachable clicks come through related-story links, so {} of what its headlines win is new. "
        "Culture·national's come mostly through its own front and tab, so only {} of its are. The change log bears "
        "this out: planned clicks times the realised lift times each desk's new share comes within 2% of the extra "
        "clicks measured against the holdback for {} of 7 embeddings. One average share for every desk is within 2% "
        "for {} and misses by up to {}."
        .format(pct(CTR["bightline.com.au/culture/"]), pct(CTR["Tab: Culture"]),
                pct(CTR["Related stories (article pages)"]), pct(src_share(CALL, "related_links")), NAME[CALL],
                pct(c["pass"]), pct(cul["pass"]), CLICK_HITS, AVG_HITS or "none", pct(AVG_WORST)), ("2",)])

    doc.add_picture(png, width=Cm(16.4))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, "Chart: for each desk, the clicks its winning headlines would win and the share of them that is new "
         "to Bightline. Desks ordered by extra clicks.", size=8.5, italic=True, color="595959", space_after=10)

    doc.add_heading("Why not the other five", level=2)
    why = {
        "LOC-M": "the strongest lift on the list ({}), but its readers reach it through the Brisbane home page, where "
                 "nearly half the views already end in a click, and its own front, where more than two thirds do, and "
                 "its editors already test the headlines behind {} of its own-page clicks."
                 .format(pct(shr["LOC-M"], 2), pct(tested_share["LOC-M"])),
        "CUL-N": "its winning headlines would win the most clicks of any desk ({:,}), because its editors test very "
                 "few of them. But {} of those would be taken from the stories beside them on the Culture front and "
                 "tab, so it adds {:,} clicks to Bightline.".format(r50k(cul["won"]), pct(1 - cul["pass"]),
                                                                 asks["CUL-N"]["extra"]),
        "SPT-N": "a large audience, but a modest lift ({}) and half its own-page clicks already on headlines its "
                 "editors test.".format(pct(shr["SPT-N"], 2)),
        "POL-N": "leads on the dashboard's Politics figure ({:.2f}%), but that average is pulled up by Politics·metro's "
                 "small Brisbane tests; Politics·national's own tests shrink to {}, and most of its clicks arrive "
                 "through search, partner apps and social cards, which keep the stored headline."
                 .format(vertical_lift("Politics"), pct(shr["POL-N"], 2)),
        "SPT-M": "the highest raw winning lift in the archive ({}), drawn from very small tests; shrunk, it is "
                 "{}.".format(pct(raw["SPT-M"], 1), pct(shr["SPT-M"], 2)),
    }
    for d in order[1:]:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run("{} ({:,}): ".format(NAME[d], asks[d]["extra"]))
        r.bold, r.font.size = True, Pt(10.5)
        runs(p, [why[d]])

    doc.add_heading("Headline corrections", level=2)
    runs(para(doc), [
        "Politics·national has the most readers on the panel, but readers do not change how many new clicks a "
        "headline can bring. When one of {}'s headlines is wrong, the first correction comes a median {} minutes "
        "after the article goes live: {} of its {} corrected articles within the hour and {} after more than three "
        "hours. The full set is below and in the workbook."
        .format(NAME[CALL], asks[CALL]["median"], asks[CALL]["hour"], asks[CALL]["corrected"], asks[CALL]["three"]),
        ("3",)])

    cols = ["Desk", "Extra clicks 2027", "Median minutes to first headline "
            "correction", "Within an hour", "After more than three hours"]
    t = doc.add_table(rows=1, cols=len(cols))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for j, h in enumerate(cols):
        cell = t.rows[0].cells[j]
        cell.text = ""
        rr = cell.paragraphs[0].add_run(h)
        rr.bold, rr.font.size = True, Pt(8)
        rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade(cell, "1F3A5F")
    for d in order:
        a = asks[d]
        vals = [NAME[d], "{:,}".format(a["extra"]),
                str(a["median"]), str(a["hour"]), str(a["three"])]
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
    t.autofit = False
    for j, w in enumerate([Cm(4.2), Cm(2.6), Cm(3.2), Cm(2.4), Cm(3.0)]):
        t.columns[j].width = w
        for row in t.rows:
            row.cells[j].width = w
    para(doc, "Source: 2027 audience plan; pageviews by source; page performance; headline test archive; CMS "
         "revisions for the web desks. Corrections cover October 2025 to September 2026.", size=8, italic=True,
         color="595959", space_after=10)

    doc.add_heading("Notes", level=3)
    notes = [
        "Prior fitted by maximum likelihood on all {:,} variant packages; a control that is kept counts as zero "
        "lift. The workbook's Back-test sheet has both tests embedding by embedding.".format(N_PACKAGES),
        "Click-through is each page's article click-throughs over its views across the twelve months. A desk's "
        "clicks from the home page are on its edition's home page; from the front and the tab, on its own; the "
        "Pages sheet lists all {} pages. The 2027 plan holds every desk at its October 2025 to September 2026 "
        "clicks.".format(len(CTR)),
        "A headline correction is a new note on a published version that went up with a corrected headline, the fix and the note on one save or on saves up to ten minutes apart, a "
        "live-blog entry's headline included (editorial standards 7.3 to 7.5); a note carried forward, or put back "
        "after a save that left it off, is not a new correction. Articles are stories and live blogs first published "
        "October 2025 to September 2026; live-blog entries and restored copies are not separate articles. An "
        "article goes live when it is first published, at its scheduled time (Brisbane) if the CMS published it "
        "then; a restored copy keeps its original's.",
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


PAPER_PAGES = 2     # the paper prints on two A4 pages


def word_stats(data, pages):
    """Word's own statistics in docProps/app.xml, counted from the body text; the template's thumbnail dropped."""
    body = data["word/document.xml"].decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", body, flags=re.S):
        txt = html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)))
        if txt.strip():
            paras.append(txt)
    stats = (("Pages", pages), ("Words", sum(len(p.split()) for p in paras)),
             ("Characters", sum(len(re.sub(r"\s", "", p)) for p in paras)),
             ("Lines", sum(max(1, math.ceil(len(p) / 92)) for p in paras)), ("Paragraphs", len(paras)),
             ("CharactersWithSpaces", sum(len(p) for p in paras)))
    app = data["docProps/app.xml"].decode("utf-8")
    for tag, val in stats:
        app = re.sub(r"<%s>\d+</%s>" % (tag, tag), "<%s>%d</%s>" % (tag, val, tag), app)
    data["docProps/app.xml"] = app.encode("utf-8")
    data.pop("docProps/thumbnail.jpeg", None)
    data["_rels/.rels"] = re.sub(rb'<Relationship [^>]*Target="docProps/thumbnail.jpeg"/>', b"", data["_rels/.rels"])
    if not any(n.endswith((".jpeg", ".jpg")) for n in data):
        data["[Content_Types].xml"] = data["[Content_Types].xml"].replace(
            b'<Default Extension="jpeg" ContentType="image/jpeg"/>', b"")


AEST = dt.timedelta(hours=10)
# (creator, last saved by, first created, last saved), AEST: each file was started after the folder was handed over
# on 16 October and last saved on the morning of the 19th, the date the paper carries.
GOLDEN_PROPS = {
    "squad_placement_2027.xlsx": ("Newsroom planning", "Corey Cox", dt.datetime(2026, 10, 16, 14, 20),
                                  dt.datetime(2026, 10, 19, 8, 52)),
    "squad_placement_2027.docx": ("Corey Cox", "Corey Cox", dt.datetime(2026, 10, 16, 15, 5),
                                  dt.datetime(2026, 10, 19, 9, 0)),
}


def repack(path):
    """Office's own record: who made the file and who saved it last, created and last saved in UTC, the
    1980-01-01 entry time Office writes, and the file dated at its last save, so a rebuild is byte-identical."""
    creator, last_by, created, modified = GOLDEN_PROPS[Path(path).name]
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    if "word/document.xml" in data:
        word_stats(data, PAPER_PAGES)
        infos = [i for i in infos if i.filename in data]
    core = data["docProps/core.xml"]
    for tag, val in ((rb"dcterms:created", created - AEST), (rb"dcterms:modified", modified - AEST)):
        core = re.sub(rb"(<" + tag + rb"[^>]*>)[^<]*", lambda m: m.group(1) + val.strftime("%Y-%m-%dT%H:%M:%SZ").encode(), core)
    core = re.sub(rb"(<dc:creator[^>]*>)[^<]*", lambda m: m.group(1) + creator.encode(), core)
    core = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*", lambda m: m.group(1) + last_by.encode(), core)
    data["docProps/core.xml"] = core
    # openpyxl writes its own version as AppVersion; the paper's Office 14 build number instead
    if "docProps/app.xml" in data:
        data["docProps/app.xml"] = re.sub(rb"<AppVersion>\d\.\d{1,2}</AppVersion>", b"<AppVersion>14.0300</AppVersion>",
                                          data["docProps/app.xml"])
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[i.filename])
    ts = (modified - AEST - dt.datetime(1970, 1, 1)).total_seconds()
    os.utime(path, (ts, ts))


def write_figures(path):
    """Every figure the write-up states, as it states it (figures_check.py reads this)."""
    c, cul = chain[CALL], chain["CUL-N"]
    pct = lambda x, k=1: ("{:.%df}" % k).format(100 * x)  # noqa: E731
    fig = {
        "call": NAME[CALL], "call_figure": "{:,}".format(asks[CALL]["extra"]), "runner_up": NAME[RUNNER],
        "runner_up_figure": "{:,}".format(asks[RUNNER]["extra"]), "gap": "{:,}".format(r50k(GAP)),
        "components": {
            "call_shrunk_lift_pct": pct(c["lift"], 2),
            "call_untested_own_page_clicks": "{:,}".format(r50k(c["untested"])),
            "call_won_clicks": "{:,}".format(r50k(c["won"])),
            "call_new_share_pct": pct(c["pass"]),
            "call_related_links_share_pct": pct(c["by_source"].get("related_links", 0) / c["untested"]),
            "culture_won_clicks": "{:,}".format(r50k(cul["won"])),
            "culture_new_share_pct": pct(cul["pass"]),
            "culture_extra": "{:,}".format(asks["CUL-N"]["extra"]),
            "runner_up_new_share_pct": pct(chain[RUNNER]["pass"]),
            "ctr_culture_front_pct": pct(CTR["bightline.com.au/culture/"]),
            "ctr_culture_tab_pct": pct(CTR["Tab: Culture"]),
            "ctr_related_pct": pct(CTR["Related stories (article pages)"]),
        },
        "backtest": {"hits": str(HITS), "of": "7", "raw_hits": str(RAW_HITS), "tolerance_pct": "2",
                     "click_hits": str(CLICK_HITS), "average_share_pct": pct(AVG_KEPT),
                     "average_share_hits": str(AVG_HITS), "average_share_worst_pct": pct(AVG_WORST, 0),
                     "packages": "{:,}".format(N_PACKAGES)},
        "extra_by_desk": {NAME[d]: "{:,}".format(asks[d]["extra"]) for d in SHORTLIST},
        "rows": {NAME[d]: {
                           "median_minutes": str(asks[d]["median"]), "within_hour": str(asks[d]["hour"]),
                           "over_three_hours": str(asks[d]["three"]), "corrected": str(asks[d]["corrected"])}
                 for d in SHORTLIST},
        "write_up": {"policy_clauses": ["7.3", "7.4", "7.5", "7.8"], "pairing_minutes": "10", "aest_offset_hours": "10",
                     "rounding": ["50,000"],
                     "pages": str(len(CTR))},
    }
    import json
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write_xlsx(OUT / "squad_placement_2027.xlsx")
    write_docx(OUT / "squad_placement_2027.docx", chart_png())
    # the writing libraries stamp their own names into docProps; replace with the newsroom's own
    scrub = HERE.parents[1] / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
    subprocess.run([sys.executable, str(scrub), str(OUT), "--apply", "--producer", "Bightline News",
                    "--stamp", "2026-10-19"], capture_output=True, text=True)
    for f in ("squad_placement_2027.xlsx", "squad_placement_2027.docx"):
        repack(OUT / f)
    audit = subprocess.run([sys.executable, str(scrub), str(OUT), "--floor", "2026-01-01", "--ceiling", "2026-10-19"],
                           capture_output=True, text=True)
    assert audit.returncode == 0, audit.stdout + audit.stderr

    write_figures(HERE / "figures.json")
    print("prior: maximum likelihood on %d packages, mean %.3f%%, sd %.3f%%" % (N_PACKAGES, 100 * MU, 100 * TAU2 ** .5))
    print("\nCALL  %s  %s extra article clicks in 2027 (unrounded %s)"
          % (NAME[CALL], "{:,}".format(asks[CALL]["extra"]), "{:,.0f}".format(chain[CALL]["extra"])))
    print("RUNNER-UP  %s  %s; gap %s (unrounded %s)" % (NAME[RUNNER], "{:,}".format(asks[RUNNER]["extra"]),
          "{:,}".format(r50k(GAP)), "{:,.0f}".format(GAP)))
    print("REFEREE  March 2026 headline and text corrections, seven web desks: %d and %d (bulletin %d and %d)"
          % (MARCH, MARCH_TEXT, MARCH_FILED, MARCH_TEXT_FILED))
    print("BACK-TEST  lift %d of 7 within 2%% (raw %d); clicks %d of 7 (one average share %.1f%%: %d of 7, worst %.0f%%)"
          % (HITS, RAW_HITS, CLICK_HITS, 100 * AVG_KEPT, AVG_HITS, 100 * AVG_WORST))
    print("\n%-18s %8s %13s %12s %8s %10s" % ("desk", "shrunk", "untested", "won", "new", "extra"))
    for d in order:
        c = chain[d]
        print("%-18s %7.2f%% %13s %12s %7.1f%% %10s" % (NAME[d], 100 * c["lift"], "{:,}".format(r50k(c["untested"])),
              "{:,}".format(r50k(c["won"])), 100 * c["pass"], "{:,}".format(asks[d]["extra"])))
    print("\nworkbook rows")
    for d in SHORTLIST:
        a = asks[d]
        print("%-18s median %3d min  within an hour %2d  over three hours %d  (of %d)" % (
            NAME[d], a["median"], a["hour"], a["three"],
            a["corrected"]))


if __name__ == "__main__":
    main()
