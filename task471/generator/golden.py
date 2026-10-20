"""The golden deliverables, computed from the shipped pack alone: nitrate_assistance_counties_2027.xlsx (the sixteen
counties, the six qualifying, the retests and the notes), nitrate_assistance_counties_2027.png, and
generator/figures.json with every figure the write-up states."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402
import openpyxl                          # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bundle as B   # noqa: E402
import world as W    # noqa: E402

GOLDEN = {"workbook": "nitrate_assistance_counties_2027.xlsx", "chart": "nitrate_assistance_counties_2027.png"}
W.GOLDEN = GOLDEN
TEAL = "1D4F5C"
FILL_H = PatternFill("solid", fgColor="DDE7EC")
FILL_Q = PatternFill("solid", fgColor="E3EFE6")
THIN = Side(style="thin", color="9AA0A6")
WORDS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def pct(a, b):
    return float(np.floor(1000.0 * a / b + 0.5) / 10.0)


def compute(target):
    pk = B.Pack(target)
    ret = pk.retests()
    rows = []
    for k in pk.codes:
        L, s = pk.link[k], pk.sample[k]
        est = pk.estimate(k)
        alt = [pk.estimate(k, r, **kw) for r, kw in B.GOLD_ROUTES]
        cnt = pk.counts(k)
        both = sum(1 for w in s["wells"].values() if w["onP"] and w["onQ"])
        rows.append(dict(code=k, name=pk.name[k], union=L["union"], NP=L["NP"], NQ=L["NQ"], NB=L["NB"],
                         nP=s["nP"], nQ=s["nQ"], fP=round(100 * s["fP"], 1), fQ=round(100 * s["fQ"], 1),
                         tested=cnt["tested"], tested_above=cnt["above"], tested_both=both,
                         estimate=int(np.floor(est + 0.5)), estimate_exact=est,
                         estimate_low=int(np.floor(min(alt) + 0.5)), estimate_high=int(np.floor(max(alt) + 0.5)),
                         qualifies=est >= W.QUALIFY, retested=ret[k][0], still_above=ret[k][1],
                         routes={r: int(np.floor(pk.estimate(k, r) + 0.5)) for r in B.WRONG_ROUTES}))
    q = [r for r in rows if r["qualifies"]]
    nq = [r for r in rows if not r["qualifies"]]
    lowest = min(q, key=lambda r: r["estimate_exact"])
    highest = max(nq, key=lambda r: r["estimate_exact"])
    tested = sum(r["tested"] for r in rows)
    nP, nQ = sum(r["nP"] for r in rows), sum(r["nQ"] for r in rows)
    NP, NQ = sum(r["NP"] for r in rows), sum(r["NQ"] for r in rows)
    rungs = {r: [pk.name[k] for k in pk.qualifying(r)] for r in B.WRONG_ROUTES}
    qo = [w for k in pk.codes for w in pk.sample[k]["wells"].values() if w["onQ"] and not w["onP"]]
    rest = [w for k in pk.codes for w in pk.sample[k]["wells"].values() if w["onP"]]
    out = dict(
        call=[r["name"] for r in q], call_codes=[r["code"] for r in q], qualifying_count=len(q), counties=rows,
        lowest_qualifier=dict(name=lowest["name"], estimate=lowest["estimate"], low=lowest["estimate_low"]),
        highest_short=dict(name=highest["name"], estimate=highest["estimate"], high=highest["estimate_high"]),
        union_total=sum(r["union"] for r in rows), tested_total=tested,
        tested_above_total=sum(r["tested_above"] for r in rows),
        tested_both_total=sum(r["tested_both"] for r in rows),
        parcel_only_tested=len(qo), parcel_only_above=sum(1 for w in qo if w["y"]),
        parcel_only_share=pct(sum(1 for w in qo if w["y"]), len(qo)),
        others_tested=len(rest), others_above=sum(1 for w in rest if w["y"]),
        others_share=pct(sum(1 for w in rest if w["y"]), len(rest)),
        permit_rate=pct(nP, NP), parcel_rate=pct(nQ, NQ), nP_total=nP, nQ_total=nQ, NP_total=NP, NQ_total=NQ,
        retested_total=sum(r["retested"] for r in rows), still_above_total=sum(r["still_above"] for r in rows),
        rungs=rungs, rung_counts={k: len(v) for k, v in rungs.items()},
        union={r["code"]: r["union"] for r in rows},
        ask={r["code"]: dict(retested=r["retested"], still_above=r["still_above"]) for r in rows},
        standard=W.STANDARD_N, line=W.QUALIFY, no3_factor=W.NO3_PER_N, retests_close="June 30, 2026")
    return out


def write_workbook(path, fig):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Counties 2027"
    ws["A1"] = "%s of sixteen counties qualify for the 2027 Well Water Assistance allocation" % WORDS[
        fig["qualifying_count"]]
    ws["A1"].font = Font(bold=True, size=13, color=TEAL)
    ws["A2"] = ("2025-26 Private Well Nitrate Survey, WWA-2027-01 section 3.1: an estimated 250 or more wells in the "
                "county's survey population above 10 mg/L nitrate as nitrogen. Private Well Program, August 2026.")
    ws["A2"].font = Font(italic=True, size=9, color="5B6067")
    head = ["Code", "County", "Private domestic wells on the survey's lists", "Qualifies for 2027",
            "Wells first tested above the standard and retested by June 30, 2026", "Of those, still above on retest"]
    ws.append([])
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    for r in fig["counties"]:
        ws.append([r["code"], r["name"], r["union"], "Yes" if r["qualifies"] else "No", r["retested"],
                   r["still_above"]])
        if r["qualifies"]:
            for c in ws[ws.max_row]:
                c.fill = FILL_Q
    ws.append([])
    ws.append([None, "All sixteen counties", fig["union_total"], "%d qualify" % fig["qualifying_count"],
               fig["retested_total"], fig["still_above_total"]])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=5, min_col=3, max_col=6):
        for c in row:
            if isinstance(c.value, int):
                c.number_format = "#,##0"
    for row in ws.iter_rows(min_row=5, min_col=4, max_col=4):
        for c in row:
            c.alignment = Alignment(horizontal="center")
    for col, wdt in zip("ABCDEF", (7, 17, 15, 11, 19, 13)):
        ws.column_dimensions[col].width = wdt
    ws.row_dimensions[4].height = 58
    ws.freeze_panes = "C5"
    ws.print_title_rows = "4:4"
    nt = wb.create_sheet("Notes")
    rows = fig["counties"]
    lines = [
        ("How these figures were made", True),
        ("Survey population: each county's private domestic wells on the permit list (active domestic wells drilled "
         "under permit from January 1, 1986, as the permit database stood on August 31, 2025) or the parcel list "
         "(residential parcels the 2025 roll records as served by a private well). A permit and a parcel are one well "
         "when the permit's parcel number is the parcel's or, on a permit without one, when its site address is the "
         "parcel's situs address. %s wells in all, %s on the permit list and %s on the parcel list." % (
             "{:,}".format(fig["union_total"]), "{:,}".format(fig["NP_total"]), "{:,}".format(fig["NQ_total"])),
         False),
        ("First tests: the final result for each kit in the draw manifest's TESTED rows, nitrate as nitrogen "
         "(Kinsale's NO3 results divided by 4.427), the later report standing where a sample was reanalysed. "
         "%s wells were tested, %s of them above 10 mg/L." % ("{:,}".format(fig["tested_total"]),
                                                             "{:,}".format(fig["tested_above_total"])), False),
        ("Estimate: each list was sampled at its own rate (%.1f per cent of the permit list and %.1f per cent of the "
         "parcel list across the state), and %s of the tested wells are on both lists, so each tested well counts for "
         "the wells it stands for: one over its chance of selection from either list, 1 - (1 - f permit)(1 - f "
         "parcel) for a well on both. The county's estimate is the sum over its tested wells above the standard. "
         "Hartley's dual-frame estimator at any split of the wells on both lists, and post-stratifying by which lists "
         "a well is on, put the same %s counties at or above 250." % (
             fig["permit_rate"], fig["parcel_rate"], "{:,}".format(fig["tested_both_total"]),
             WORDS[fig["qualifying_count"]].lower()), False),
        ("Retests: a request is matched to its well through the first kit it names or, for a phone request, the "
         "address it ships to. Each well counts in the county the survey tested it in, whatever county the kit "
         "vendor routed the request to; a retest counts when its sample was collected on or before June 30, 2026 "
         "(WWA-2027-01 section 4.2). Requests from households outside the survey, and retests of wells first tested "
         "at or below the standard, are not counted.", False),
        ("Counts are whole wells.", False)]
    for i, (t, b) in enumerate(lines, 1):
        c = nt.cell(row=i, column=1, value=t)
        c.font = Font(bold=b, size=12 if b else 10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 118
    est = wb.create_sheet("Estimates")
    est.append(["Code", "County", "Tested wells", "Tested wells above the standard", "Estimated wells above the "
                "standard", "Permit list sampled (%)", "Parcel list sampled (%)"])
    for c in est[1]:
        c.font = Font(bold=True)
        c.fill = FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        est.append([r["code"], r["name"], r["tested"], r["tested_above"], r["estimate"], r["fP"], r["fQ"]])
    for row in est.iter_rows(min_row=2, min_col=6, max_col=7):
        for c in row:
            c.number_format = "0.0"
    for col, wdt in zip("ABCDEFG", (7, 17, 10, 14, 14, 12, 12)):
        est.column_dimensions[col].width = wdt
    est.row_dimensions[1].height = 44
    est.freeze_panes = "C2"
    wb.save(path)


def write_chart(path, fig):
    rows = sorted(fig["counties"], key=lambda r: r["estimate_exact"])
    names = [r["name"] for r in rows]
    vals = [r["estimate_exact"] for r in rows]
    colors = ["#1d6b5c" if r["qualifies"] else "#a7b1b8" for r in rows]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    f, ax = plt.subplots(figsize=(8.6, 6.6), dpi=120)
    y = np.arange(len(rows))
    ax.barh(y, vals, color=colors, height=0.66)
    ax.axvline(W.QUALIFY, color="#1b1d1f", lw=1.2, ls="--")
    ax.text(W.QUALIFY + 8, 0.2, "250 wells: qualifies at or above the line", fontsize=8.5, va="center")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlim(0, max(vals) * 1.08)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _p: "{:,.0f}".format(v)))
    ax.set_xlabel("Estimated private domestic wells above 10 mg/L nitrate as nitrogen (2025-26 survey population)")
    ax.set_title("%s counties qualify for 2027 Well Water Assistance" % WORDS[fig["qualifying_count"]], loc="left",
                 fontsize=11, fontweight="bold", color="#1D4F5C")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0, -0.1, "Each tested well counts for one over its chance of selection from either list. Private Well "
            "Program, August 2026.", transform=ax.transAxes, fontsize=7.5, color="#5b6067")
    f.tight_layout()
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fig = compute(target)
    write_workbook(os.path.join(gdir, GOLDEN["workbook"]), fig)
    write_chart(os.path.join(gdir, GOLDEN["chart"]), fig)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, GOLDEN["workbook"]), W.PROGRAM, W.PROGRAM, "2026-08-12T14:02:00Z",
                       "2026-08-14T16:47:31Z", excel=True, company="%s, %s" % (W.DEPT, W.OFFICE))
    fig = {k: v for k, v in fig.items()}
    for r in fig["counties"]:
        r["estimate_exact"] = round(r["estimate_exact"], 2)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    return fig
