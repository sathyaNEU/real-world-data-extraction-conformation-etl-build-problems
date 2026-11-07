"""task286 golden: the figures the deliverables and the write-up state, computed the way the golden reads the pack,
and the two deliverables (the workbook and the chart)."""
import os
from datetime import datetime

import numpy as np

import world as W
import records as R

USE_MARGIN = 50          # a day counts as somebody's when it rises this far above the week's quietest day


def observed_daily(h):
    """one total per meter day: the two rows of an exchange day added."""
    x = np.zeros(W.NDAYS, dtype=np.int64)
    for _serial, i, l, _t in R.meter_rows(h):
        x[i] += l
    return x


def weeks_without_use(x, margin=USE_MARGIN):
    """weeks of the 52 in which no day rose above the week's own steady level by more than the margin."""
    wk = x[W.W0:W.W1 + 1].reshape(W.NWEEKS, 7)
    return int(((wk.max(1) - wk.min(1)) <= margin).sum())


def area_of(h, by_uprn, by_pc):
    if h.match != "UNMATCHED":
        return by_uprn[h.uprn]
    return by_pc[h.postcode]


def figures(homes, entries, oas, n_rows):
    by_uprn = {h.uprn: h.area for h in homes}
    by_pc = {}
    for h in homes:
        by_pc.setdefault(h.postcode, set()).add(h.area)
    assert all(len(v) == 1 for v in by_pc.values()), "a postcode spans two areas"
    by_pc = {k: next(iter(v)) for k, v in by_pc.items()}
    per = {a: {"homes": 0, "left_empty": 0, "w26_38": 0, "w39_51": 0, "w52": 0} for a in W.AREA_CODES}
    for h in homes:
        a = area_of(h, by_uprn, by_pc)
        assert a == h.area
        per[a]["homes"] += 1
        e = weeks_without_use(observed_daily(h))
        assert e == h.empty_weeks, (h.i, e, h.empty_weeks)
        if e >= 26:
            per[a]["left_empty"] += 1
            per[a]["w26_38" if e <= 38 else ("w39_51" if e <= 51 else "w52")] += 1
    lte = {a: 0 for a in W.AREA_CODES}
    for h in homes:
        if R.lte_on(h):
            lte[h.area] += 1
    lets = R.ndr_homes_on(entries)
    ranked = sorted(W.AREA_CODES, key=lambda a: -per[a]["left_empty"])
    call, ru = ranked[0], ranked[1]
    figs = {
        "call": W.AREA_NAME[call],
        "call_count": per[call]["left_empty"],
        "runner_up": W.AREA_NAME[ru],
        "runner_up_count": per[ru]["left_empty"],
        "gap": per[call]["left_empty"] - per[ru]["left_empty"],
        "window": "Monday 29 September 2025 to Sunday 27 September 2026",
        "meter_rows": n_rows,
        "areas": {W.AREA_NAME[a]: {"district": W.AREA_DISTRICT[a], "homes": per[a]["homes"],
                                   "left_empty": per[a]["left_empty"], "w26_38": per[a]["w26_38"],
                                   "w39_51": per[a]["w39_51"], "w52": per[a]["w52"],
                                   "lte_ctb": lte[a], "holiday_let_homes": lets[a]} for a in W.AREA_CODES},
        "total_left_empty": sum(per[a]["left_empty"] for a in W.AREA_CODES),
        "total_homes": sum(per[a]["homes"] for a in W.AREA_CODES),
        "use_margin_l": USE_MARGIN,
        "margin_corridor_l": [30, 75],
        "weeks": W.NWEEKS,
        "min_weeks": 26,
        "band_edges": [38, 39, 51],
    }
    return figs


# --------------------------------------------------------------------------------------------- deliverables
def write_golden(folder, figs):
    write_workbook(os.path.join(folder, "homes_in_use_pilot_2027.xlsx"), figs)
    write_chart(os.path.join(folder, "empty_homes_by_area_2026.png"), figs)


def write_workbook(path, figs):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    import build as B
    wb = B.wb_new("Toby Hunt", "Homes in Use pilot 2027: area evidence", datetime(2026, 10, 21, 9, 38, 17),
                  datetime(2026, 10, 23, 16, 14, 42))
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DCE6F1")
    thin = Side(style="thin", color="A6A6A6")
    ws = wb.active
    ws.title = "Recommendation"
    ws["A1"] = "Orrimouth has the most homes nobody used for half the year or more: %d, %d more than %s" % (
        figs["call_count"], figs["gap"], figs["runner_up"])
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "National Homes Agency, Housing Evidence. Prepared by Toby Hunt, 23 October 2026. OFFICIAL"
    ws["A2"].font = Font(italic=True, size=9, color="595959")
    rows = [
        ("Recommended pilot area", figs["call"]),
        ("Homes nobody used for 26 or more of the 52 weeks", figs["call_count"]),
        ("Runner-up", figs["runner_up"]),
        ("Runner-up's homes nobody used for 26 or more weeks", figs["runner_up_count"]),
        ("Gap (homes)", figs["gap"]),
        ("Weeks counted", figs["window"]),
    ]
    for i, (k, v) in enumerate(rows, start=4):
        ws.cell(row=i, column=1, value=k).font = bold
        ws.cell(row=i, column=2, value=v)
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 54
    ws["A11"] = ("Terms of reference 3.1 to 3.3: the pilot goes to the shortlisted area with the most homes nobody "
                 "lived in, stayed at or used on any day of at least 26 of the 52 weeks.")
    ws["A11"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A11:B12")
    ws.row_dimensions[11].height = 30

    ws2 = wb.create_sheet("By area")
    hdr = ["Community area", "District", "Homes on the gazetteer", "Homes nobody used for 26+ weeks",
           "of which 26 to 38 weeks", "of which 39 to 51 weeks", "of which all 52 weeks",
           "Long-term empty homes on the council tax records, 27 Sep 2026 (CTB basis)",
           "Homes on the business rates list as self-catering lets, 27 Sep 2026"]
    ws2.append(hdr)
    for c in ws2[1]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    order = sorted(figs["areas"], key=lambda n: -figs["areas"][n]["left_empty"])
    for n in order:
        a = figs["areas"][n]
        ws2.append([n, a["district"], a["homes"], a["left_empty"], a["w26_38"], a["w39_51"], a["w52"],
                    a["lte_ctb"], a["holiday_let_homes"]])
    last = ws2.max_row
    tot = [sum(figs["areas"][n][k] for n in order) for k in ("homes", "left_empty", "w26_38", "w39_51", "w52",
                                                              "lte_ctb", "holiday_let_homes")]
    ws2.append(["All shortlisted areas", ""] + tot)
    for row in ws2.iter_rows(min_row=2, min_col=3, max_col=9):
        for c in row:
            c.number_format = "#,##0"
    ws2.print_title_rows = "1:1"
    ws2.page_setup.orientation = "landscape"
    ws2.page_setup.fitToWidth = 1
    ws2.sheet_properties.pageSetUpPr.fitToPage = True
    for c in ws2[ws2.max_row]:
        c.font = bold
        c.border = Border(top=thin)
    for col, wdt in zip("ABCDEFGHI", [18, 11, 13, 15, 12, 12, 12, 24, 22]):
        ws2.column_dimensions[col].width = wdt
    ws2.row_dimensions[1].height = 62
    ws2.freeze_panes = "B2"

    ws3 = wb.create_sheet("Notes")
    notes = [
        "Notes",
        "",
        "1. Homes: every self-contained dwelling on the county gazetteer extract in the eight shortlisted areas "
        "(parent shells for blocks and holiday sites left out). Every home has its own Pennimouth Water smart meter.",
        "2. Meter data: daily consumption from Pennimouth Water (PW-DSA-2026-014), cut to the 52 Monday-to-Sunday "
        "weeks from 29 September 2025 to 27 September 2026. Exchange days carry two rows (old and new meter) and are "
        "added. Estimated days (read type E) are kept: the head end spreads the next index read across the gap.",
        "3. Area: by the water company's UPRN match to the gazetteer; properties the company left unmatched placed "
        "by postcode (every postcode in the extract sits in one community area).",
        "4. A week of use: a week in which the home's daily totals rise above that home's own steady level. Some "
        "homes register the same litres every day whether or not anyone is there (a cistern or supply pipe running "
        "on); that steady flow is not use. A day with anyone in the home draws at least %d litres more than its "
        "quietest day in the same week; a week with nobody in varies by no more than a few litres. The count is "
        "the same for any margin between about 20 and 70 litres." % figs["use_margin_l"],
        "5. Council tax column: dwellings unoccupied and substantially unfurnished for more than six months on "
        "27 September 2026 and not exempt, the Council Taxbase return's definition, each dwelling's empty period "
        "followed across changes of owner and, in Teversby, across the May 2026 move to the new revenues system.",
        "6. Business rates column: homes covered by a self-catering entry in effect on 27 September 2026; an "
        "entry for a holiday site counts each cottage on the site.",
    ]
    for i, t in enumerate(notes, start=1):
        c = ws3.cell(row=i, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            c.font = Font(bold=True, size=12)
    ws3.column_dimensions["A"].width = 120
    for i in range(3, len(notes) + 1):
        ws3.row_dimensions[i].height = 46
    B.wb_save(wb, path, "2026-10-23T16:14:42Z", (2026, 10, 23, 16, 14, 42))


def write_chart(path, figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = sorted(figs["areas"], key=lambda n: -figs["areas"][n]["left_empty"])
    a = figs["areas"]
    s1 = [a[n]["w26_38"] for n in order]
    s2 = [a[n]["w39_51"] for n in order]
    s3 = [a[n]["w52"] for n in order]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task286"})
    fig, ax = plt.subplots(figsize=(9.2, 5.4), dpi=110)
    cols = ["#3a93d4", "#155aa8", "#082f66"]
    x = np.arange(len(order))
    b1 = ax.bar(x, s1, color=cols[0], width=0.62, label="26 to 38 weeks", edgecolor="white", linewidth=1.5)
    b2 = ax.bar(x, s2, bottom=s1, color=cols[1], width=0.62, label="39 to 51 weeks", edgecolor="white",
                linewidth=1.5)
    b3 = ax.bar(x, s3, bottom=[p + q for p, q in zip(s1, s2)], color=cols[2], width=0.62, label="All 52 weeks",
                edgecolor="white", linewidth=1.5)
    for bars, vals, bottoms, tc in ((b1, s1, [0] * len(s1), "white"), (b2, s2, s1, "white"),
                                    (b3, s3, [p + q for p, q in zip(s1, s2)], "white")):
        for rect, v, b in zip(bars, vals, bottoms):
            if v >= 10:
                ax.text(rect.get_x() + rect.get_width() / 2, b + v / 2, str(v), ha="center", va="center",
                        fontsize=8, color=tc)
            elif v > 0:      # a thin part is labelled beside its bar
                ax.text(rect.get_x() + rect.get_width() + 0.04, b + v / 2, str(v), ha="left", va="center",
                        fontsize=7.5, color="#404040")
    for i, n in enumerate(order):
        ax.text(i, a[n]["left_empty"] + 3, str(a[n]["left_empty"]), ha="center", va="bottom", fontsize=9,
                fontweight="bold", color="#252525")
    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_ylabel("Homes")
    ax.set_ylim(0, max(a[n]["left_empty"] for n in order) * 1.22)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Orrimouth has the most homes nobody used for 26 or more of the 52 weeks to 27 September 2026",
                 fontsize=10.5, loc="left")
    top = order[0]
    ax.annotate("Pilot area", xy=(0, a[top]["left_empty"] + 14), ha="center", va="bottom", fontsize=8.5,
                color="#252525", fontweight="bold")
    h, l = ax.get_legend_handles_labels()
    ax.legend(h[::-1], l[::-1], title="Weeks nobody used the home", frameon=False, loc="upper right", fontsize=8,
              title_fontsize=8)
    fig.text(0.01, 0.01, "Source: Pennimouth Water daily meter reads (PW-DSA-2026-014), county address gazetteer. "
             "National Homes Agency, Housing Evidence, October 2026.", fontsize=7, color="#595959")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)
