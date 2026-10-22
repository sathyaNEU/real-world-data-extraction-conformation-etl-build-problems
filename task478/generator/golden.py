"""The golden: every owed figure computed from the cut pack (bundle.py), written to generator/figures.json, and the three
deliverables, ctpa_vws_sections_2027.xlsx, ctpa_section_overweight_2026.csv and ctpa_overweight_share_2026.svg."""
import csv
import io
import json
import os

import numpy as np

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = "ctpa_vws_sections_2027.xlsx"
CSV = "ctpa_section_overweight_2026.csv"
SVG = "ctpa_overweight_share_2026.svg"
WORDS = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def pct_off(f):
    """A station's reading against the static scale, whole per cent heavy (+) or light (-)."""
    return B.hround(abs(f - 1) * 100) * (1 if f >= 1 else -1)


def compute(target):
    df = B.class9(B.read_wim(target))
    tk = B.read_tickets(target)
    fa = B.factors(df, tk, "loaded")
    sh = B.shares(df, fa)
    raw = B.shares(df)
    pooled = B.shares(df, B.factors(df, tk, "pooled"))
    rank = sorted(B.CODES, key=lambda c: -sh[c])
    five = rank[:5]
    tsteer = tk["Axle 1 (lb)"].astype(float).to_numpy()
    tgross = tk[["Axle %d (lb)" % i for i in range(1, 6)]].astype(float).sum(axis=1).to_numpy()
    ref = float(np.median(tsteer[tgross > 50000]))
    wk = B.weekday_entries(target)
    ci = B.citations_by_section(target)
    n9 = df.groupby("section").size()
    f = {
        "call": {"equip": [B.NAMES[c] for c in B.CODES if c in five], "count": 5, "of": 12},
        "sections": {B.NAMES[c]: {"section": c, "share_pct": B.hround(sh[c]), "equip": "Yes" if c in five else "No",
                                  "weekday_entries": B.hround(wk[c]), "gross_citations": ci[c],
                                  "raw_share_pct": B.hround(raw[c]), "reads_pct": pct_off(fa[c])}
                     for c in B.CODES},
        "components": {"fifth": {"name": B.NAMES[rank[4]], "share_pct": B.hround(sh[rank[4]])},
                       "sixth": {"name": B.NAMES[rank[5]], "share_pct": B.hround(sh[rank[5]])},
                       "ticket_loaded_steer_lb": int(round(ref)),
                       "factor_low": {"name": B.NAMES[min(B.CODES, key=lambda c: fa[c])],
                                      "factor": "%.3f" % min(fa.values())},
                       "factor_high": {"name": B.NAMES[max(B.CODES, key=lambda c: fa[c])],
                                       "factor": "%.3f" % max(fa.values())},
                       "class9_weighed": int(len(df)),
                       "entries_weekday_total": B.hround(sum(wk.values())),
                       "gross_citations_total": int(sum(ci.values()))},
        "default": {"equip": [B.NAMES[c] for c in B.five(raw)]},
        "pooled": {"equip": [B.NAMES[c] for c in B.five(pooled)]},
        "rank": [B.NAMES[c] for c in rank],
        "stated": {"limit_lb": "80,000", "loaded_line_lb": "50,000", "weekdays_2026": B.WEEKDAYS_2026,
                   "program_clauses": ["3.2", "5", "6.2"]},
        "_unrounded": {"share": {c: round(sh[c], 4) for c in B.CODES}, "factor": {c: round(fa[c], 5) for c in B.CODES},
                       "weekday": {c: round(wk[c], 4) for c in B.CODES}, "raw": {c: round(raw[c], 4) for c in B.CODES},
                       "class9": {c: int(n9.get(c, 0)) for c in B.CODES}},
    }
    return f


def write_csv(path, f):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["section", "section_name", "share_over_80000_lb_pct"])
    for c in B.CODES:
        w.writerow([c, B.NAMES[c], f["sections"][B.NAMES[c]]["share_pct"]])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def write_xlsx(path, f):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sites 2027"
    bold = Font(name="Calibri", size=11, bold=True)
    thin = Side(style="thin", color="808080")
    ws["A1"] = "Virtual weigh station sites, 2027 contract"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True)
    ws["A2"] = "Office of Freight Operations. Freight Compliance Program 2027, section 3. Prepared 12 February 2027."
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")
    head = ["Section", "Name", "From milepost", "To milepost", "Share of class 9 trucks over 80,000 lb"]
    ws.append([])
    ws.append(head)
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    secs = {s[0]: s for s in B.SECTIONS}
    for name in f["call"]["equip"]:
        x = f["sections"][name]
        s = secs[x["section"]]
        ws.append([x["section"], name, s[2], s[3], x["share_pct"] / 100.0])
    for row in ws.iter_rows(min_row=5, max_row=9):
        row[0].number_format = "@"
        row[2].number_format = row[3].number_format = "0.0"
        row[4].number_format = "0%"
    c6 = f["components"]["sixth"]
    ws["A11"] = ("West to east. Sixth: %s, %d%%. Shares are of each station's 2026 class 9 weighings, on the static "
                 "scale's basis." % (c6["name"], c6["share_pct"]))
    ws["A11"].font = Font(name="Calibri", size=9, color="555555")
    for col, wd in zip("ABCDE", (9, 15, 10, 10, 18)):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "A5"

    s2 = wb.create_sheet("Sections")
    head = ["Section", "Name", "From milepost", "To milepost", "Share of class 9 trucks over 80,000 lb",
            "Equip 2027", "Five-axle entries a weekday", "Gross overweight citations"]
    s2.append(head)
    for c in s2[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    fill = PatternFill("solid", fgColor="DDEBF7")
    for code in B.CODES:
        name = B.NAMES[code]
        x = f["sections"][name]
        s = secs[code]
        s2.append([code, name, s[2], s[3], x["share_pct"] / 100.0, x["equip"], x["weekday_entries"],
                   x["gross_citations"]])
        if x["equip"] == "Yes":
            for c in s2[s2.max_row]:
                c.fill = fill
    tot = s2.max_row + 1
    s2.append(["Turnpike", None, 0.0, 284.0, None, None, f["components"]["entries_weekday_total"],
               f["components"]["gross_citations_total"]])
    for c in s2[tot]:
        c.font = bold
        c.border = Border(top=thin)
    for row in s2.iter_rows(min_row=2, max_row=tot):
        row[0].number_format = "@"
        row[2].number_format = row[3].number_format = "0.0"
        row[4].number_format = "0%"
        row[6].number_format = row[7].number_format = "#,##0"
        row[5].alignment = Alignment(horizontal="center")
    for col, wd in zip("ABCDEFGH", (9, 15, 10, 10, 18, 10, 13, 13)):
        s2.column_dimensions[col].width = wd
    s2.row_dimensions[1].height = 45
    s2.freeze_panes = "C2"
    s2.print_title_rows = "1:1"

    s3 = wb.create_sheet("Notes")
    notes = [
        ("Share over 80,000 lb", "Program 3.2: of the class 9 trucks the section's weigh-in-motion station weighed in "
         "2026 (valid weighings, every lane, both directions), the share whose gross vehicle weight exceeded 80,000 lb. "
         "Gross vehicle weight is the static scale's (program 2.2): each station's weights were put on that basis by "
         "the median steer axle of its loaded class 9 trucks (gross over 50,000 lb) against the scale houses' loaded "
         "tickets' before counting."),
        ("Five-axle entries a weekday", "Program 5: entries by five-axle trucks at the section's toll plazas, barrier "
         "plazas included, on the 261 weekdays of 2026 by local date, averaged. Each plaza moved to the new toll host "
         "on its own day in May or June and the new host backfilled its last days from the lane logs, so a backfilled "
         "entry is counted once; the old host's stamps are local time, the new host's own UTC; plaza code P23 is "
         "Brannock Road until 30 April and Halbrook East from 1 September."),
        ("Gross overweight citations", "Program 6: violation code G, placed at the toll entry of the trip on which the "
         "scale house weighed the truck (the tag's last entry before the stop, the old host's entries read in local "
         "time), not the log's entry plaza, which the toll system returned when the citation was keyed. A truck cited "
         "for gross weight usually comes back through the barrier after offloading; that entry is a new trip."),
        ("Rounding", "Shares to the whole per cent from the unrounded share; entries and citations in whole numbers."),
        ("Sources", "WIM piezoelectric and bending-plate exports 2026, WIM station list, scale house tickets 2026, toll "
         "entries 2026 (exported 4 February 2027), toll plaza list, toll schedule 2025, citation log 2026."),
    ]
    s3.append(["Item", "Note"])
    for c in s3[1]:
        c.font = bold
    for k, v in notes:
        s3.append([k, v])
    for row in s3.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    s3.column_dimensions["A"].width = 26
    s3.column_dimensions["B"].width = 96
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, "Anna Haynes", "Anthony Hale", "2027-02-11T15:02:00Z", "2027-02-12T19:47:31Z",
                       excel=True, company=PP.COMPANY)


def write_svg(path, f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task478-ctpa"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    names = [B.NAMES[c] for c in B.CODES]
    vals = [f["_unrounded"]["share"][c] for c in B.CODES]
    on = [f["sections"][n]["equip"] == "Yes" for n in names]
    blue, grey, ink, muted = "#2a6fb0", "#c3c8ce", "#1f2328", "#59636e"
    fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=100)
    xs = np.arange(len(names))
    ax.bar(xs, vals, width=0.68, color=[blue if o else grey for o in on], edgecolor="white", linewidth=2, zorder=3)
    for x, v, o in zip(xs, vals, on):
        ax.text(x, v + 0.35, "%d%%" % B.hround(v), ha="center", va="bottom", fontsize=9,
                color=ink if o else muted, fontweight="bold" if o else "normal")
    ax.set_xticks(xs)
    ax.set_xticklabels(names, rotation=35, ha="right", fontsize=9, color=ink)
    ax.set_ylabel("Share of class 9 trucks over 80,000 lb (%)", fontsize=9, color=muted)
    ax.set_ylim(0, max(vals) * 1.18)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "%d" % v))
    ax.tick_params(axis="y", labelsize=8.5, colors=muted)
    ax.grid(axis="y", color="#e6e8eb", linewidth=0.8, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#9aa1a9")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=blue, label="Equip in 2027 (five sections)"), Patch(color=grey, label="Not equipped")],
              loc="upper left", frameon=False, fontsize=8.5)
    c6 = f["components"]["sixth"]
    low = min(f["sections"][n]["share_pct"] for n in f["call"]["equip"])
    fig.suptitle("Five sections ran the highest shares of class 9 trucks over 80,000 lb in 2026", x=0.012, ha="left",
                 fontsize=11.5, fontweight="bold", color=ink)
    ax.set_title("Share of the five-axle tractor-semitrailers each section's station weighed that were over the gross "
                 "limit,\nstation weights on the static scale's basis. Lowest of the five %d%%; sixth, %s, %d%%."
                 % (low, c6["name"], c6["share_pct"]), loc="left", fontsize=8.5, color=muted, pad=10)
    fig.text(0.012, 0.012, "Source: CTPA weigh-in-motion exports and scale house tickets, 2026.", fontsize=7.5,
             color=muted)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.83, bottom=0.25)
    buf = io.StringIO()
    fig.savefig(buf, format="svg", metadata={"Date": None, "Creator": "Office of Freight Operations"})
    plt.close(fig)
    svg = buf.getvalue().replace('id="matplotlib.', 'id="').replace("'DejaVu Sans'", "'DejaVu Sans', Arial, Helvetica, sans-serif")
    assert "matplotlib" not in svg.lower()
    open(path, "w", encoding="utf-8", newline="\n").write(svg)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    f = compute(target)
    json.dump(f, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    out = os.path.join(os.path.dirname(HERE), "golden")
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out):
        os.remove(os.path.join(out, fn))
    write_xlsx(os.path.join(out, XLSX), f)
    write_csv(os.path.join(out, CSV), f)
    write_svg(os.path.join(out, SVG), f)
    return f


if __name__ == "__main__":
    import sys
    f = main(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps({k: v for k, v in f.items() if not k.startswith("_")}, indent=1)[:4000])
