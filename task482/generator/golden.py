"""The golden: every owed figure computed from the cut pack (bundle.py), written to generator/figures.json, and the two
deliverables, priority_stations_2027q1.xlsx and station_availability_2026q4.html."""
import html
import io
import json
import os

import numpy as np

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = "priority_stations_2027q1.xlsx"
HTML = "station_availability_2026q4.html"
MONTH = {10: "October", 11: "November", 12: "December"}
KEY = {10: "oct", 11: "nov", 12: "dec"}


def label(I, no):
    return "W-%02d %s" % (no, I.name[no])


def compute(target):
    I = B.Inputs(target)
    g = B.golden(I)
    d = B.default(I)
    pr = B.designated(g)
    dp = B.designated(d)
    nb, margin = B.nearest_clear(g)
    nb_mo = min(B.MONTHS, key=lambda mo: g[nb][mo])
    sales = B.sales(I)
    down = B.downtime(I)
    fig = {
        "call": {"priority": [label(I, no) for no in pr], "count": len(pr), "of": len(I.nos)},
        "stations": {},
        "components": {
            "nearest": {"station": "W-%02d" % nb, "name": I.name[nb], "month": MONTH[nb_mo],
                        "availability": int(B.hround(g[nb][nb_mo], 0)), "margin_points": B.hround(margin)},
        },
        "default": {"priority": [label(I, no) for no in dp], "count": len(dp),
                    "lowest": {"W-%02d" % no: int(B.hround(min(d[no].values()), 0)) for no in I.nos}},
        "stated": {"line_per_cent": 90, "linden_avenue_feed_ids": [117, 125], "service_hours": "6:00 to midnight Eastern", "quarter": "Q4 2026",
                   "next_quarter": "Q1 2027", "notice_by": "15 January 2027", "fares_cad": {"single": 3.25, "day": 11.50}},
        "_unrounded": {"availability": {"W-%02d" % no: {KEY[mo]: round(g[no][mo], 6) for mo in B.MONTHS} for no in I.nos},
                       "default": {"W-%02d" % no: {KEY[mo]: round(d[no][mo], 6) for mo in B.MONTHS} for no in I.nos},
                       "hours_no_card": {"W-%02d" % no: down[no] for no in I.nos},
                       "margin": round(margin, 6)},
    }
    for no in I.nos:
        lo = min(B.MONTHS, key=lambda mo: g[no][mo])
        fig["stations"]["W-%02d" % no] = {
            "name": I.name[no], "oct": B.hround(g[no][10]), "nov": B.hround(g[no][11]), "dec": B.hround(g[no][12]),
            "lowest": int(B.hround(g[no][lo], 0)), "lowest_month": MONTH[lo], "priority": no in pr,
            "sales_cad": round(sales[no], 2), "hours_no_card": int(B.hround(down[no], 0))}
    return fig


def write_xlsx(path, f):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Priority stations"
    bold = Font(bold=True)
    ws["A1"] = "Wellhaven Bike Share: Schedule C priority stations for Q1 2027"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Availability in each month of Q4 2026: the share of the month's service minutes (6:00 to midnight) "
                "that began with at least one bike in working order docked at the station.")
    ws.append([])
    ws.append(["Station", "Name", "October 2026 (%)", "November 2026 (%)", "December 2026 (%)", "Lowest month",
               "Lowest month (%)", "Priority station for Q1 2027"])
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    shade = PatternFill("solid", fgColor="FCE8D8")
    for k in sorted(f["stations"]):
        s = f["stations"][k]
        ws.append([k, s["name"], s["oct"], s["nov"], s["dec"], s["lowest_month"], s["lowest"],
                   "Yes" if s["priority"] else "No"])
        if s["priority"]:
            for c in ws[ws.max_row]:
                c.fill = shade
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in row[2:5]:
            c.number_format = "0.0"
        row[6].number_format = "0"
    ws.append([])
    nb = f["components"]["nearest"]
    ws.append(["Priority stations", ", ".join(f["call"]["priority"])])
    ws.append(["Nearest station above the line", "%s %s: %d per cent in %s, %.1f points above 90 per cent"
               % (nb["station"], nb["name"], nb["availability"], nb["month"], nb["margin_points"])])
    for r in (ws.max_row - 1, ws.max_row):
        ws.cell(row=r, column=1).font = bold
    for i, w in enumerate((9, 20, 12, 12, 12, 11, 11, 14)):
        ws.column_dimensions[get_column_letter(i + 1)].width = w
    ws.freeze_panes = "C5"

    s2 = wb.create_sheet("Pay stations")
    s2["A1"] = "Pay stations, Q4 2026"
    s2["A1"].font = Font(bold=True, size=12)
    s2["A2"] = ("Card sales are approved sales less voids, at the pay station where each sale was made; hours are the "
                "service hours (6:00 to midnight) in which the pay station could not take a card payment.")
    s2.append([])
    s2.append(["Station", "Name", "Card sales (CAD)", "Service hours unable to take a card"])
    for c in s2[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for k in sorted(f["stations"]):
        s = f["stations"][k]
        s2.append([k, s["name"], s["sales_cad"], s["hours_no_card"]])
    for row in s2.iter_rows(min_row=5, max_row=s2.max_row):
        row[2].number_format = "#,##0.00"
        row[3].number_format = "0"
    for i, w in enumerate((9, 20, 15, 18)):
        s2.column_dimensions[get_column_letter(i + 1)].width = w

    s3 = wb.create_sheet("Method")
    notes = [
        ("Bikes in working order",
         "The status feed counts a docked bike as available until Northlane marks it out of service, so a bike that "
         "broke on a ride and was docked unreported stayed in the available count. Each bike's time at each station "
         "was rebuilt from the trips and the fleet moves; a docked bike is taken as out of working order from the end "
         "of the ride that left it until the van took it to the depot, when it then stayed at the depot a day or more "
         "for repair (every other van pickup was back on the street within hours)."),
        ("Minutes", "A minute counts when a bike in working order was docked at its start; Linden Avenue's two feed IDs "
                    "are one station; the trips' repeated week of 16 November is counted once."),
        ("Pay-station sales", "The sales export names each sale's pay station from where its terminal is now; sales "
                              "are placed at the pay station the terminal was in when the sale was made, from the "
                              "terminal replacements in the work orders."),
        ("Card downtime", "A card-stopping alarm (COMMS_LOST, READER_FAULT) runs from its raise to its clear or to the "
                          "pay station's next restart, after which it is raised again if the fault is still there; "
                          "overlapping alarms are counted once, inside service hours."),
    ]
    for a, b in notes:
        s3.append([a, b])
    for row in s3.iter_rows():
        row[0].font = bold
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    s3.column_dimensions["A"].width = 22
    s3.column_dimensions["B"].width = 100
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, "Transportation Services", "Transportation Services", "2027-01-12T14:20:00Z",
                       "2027-01-14T21:37:44Z", excel=True, company="City of Wellhaven")


def chart_svg(f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    matplotlib.rcParams["svg.hashsalt"] = "task482-wellhaven"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    un = f["_unrounded"]["availability"]
    st = f["stations"]
    keys = sorted(st, key=lambda k: (min(un[k].values()), k))
    vals = [min(un[k].values()) for k in keys]
    on = [st[k]["priority"] for k in keys]
    accent, grey, ink, muted = "#c2562b", "#b9c1ca", "#1f2328", "#59636e"
    fig, ax = plt.subplots(figsize=(8.8, 8.6), dpi=100)
    ys = np.arange(len(keys))[::-1]
    ax.barh(ys, [v - 80 for v in vals], left=80, height=0.62, color=[accent if o else grey for o in on],
            edgecolor="white", linewidth=1.5, zorder=3)
    for y, k, v, o in zip(ys, keys, vals, on):
        ax.text(v + 0.15, y, "%d" % st[k]["lowest"], ha="left", va="center", fontsize=8.5,
                color=ink if o else muted, fontweight="bold" if o else "normal")
    ax.axvline(90, color=ink, linewidth=1.3, linestyle=(0, (4, 3)), zorder=4)
    ax.text(90.12, ys[0] + 0.7, "90 per cent", color=ink, fontsize=8.5, va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s %s (%s)" % (k, st[k]["name"], st[k]["lowest_month"][:3]) for k in keys], fontsize=8.5,
                       color=ink)
    ax.set_xlabel("Availability in the station's lowest month of Q4 2026 (per cent of service minutes)", fontsize=9,
                  color=muted)
    ax.set_xlim(80, 100.9)
    ax.set_ylim(-0.7, len(keys) - 0.1)
    ax.tick_params(axis="x", labelsize=8.5, colors=muted)
    ax.grid(axis="x", color="#e6e8eb", linewidth=0.8, zorder=0)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#9aa1a9")
    ax.legend(handles=[Patch(color=accent, label="Priority station for Q1 2027"),
                       Patch(color=grey, label="90 per cent or more in every month")], loc="upper right",
              frameon=False, fontsize=8.5)
    fig.subplots_adjust(left=0.27, right=0.97, top=0.98, bottom=0.07)
    buf = io.StringIO()
    fig.savefig(buf, format="svg", metadata={"Date": None, "Creator": "Transportation Services"})
    plt.close(fig)
    svg = buf.getvalue().replace('id="matplotlib.', 'id="').replace("'DejaVu Sans'",
                                                                   "'DejaVu Sans', Arial, Helvetica, sans-serif")
    svg = svg[svg.index("<svg"):]
    assert "matplotlib" not in svg.lower()
    return svg


def write_html(path, f):
    svg = chart_svg(f)
    n = f["call"]["count"]
    word = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}.get(n, str(n))
    nb = f["components"]["nearest"]
    rows = []
    for k in sorted(f["stations"]):
        s = f["stations"][k]
        rows.append("<tr%s><td>%s</td><td>%s</td><td>%.1f</td><td>%.1f</td><td>%.1f</td><td>%s</td></tr>" % (
            ' class="p"' if s["priority"] else "", k, html.escape(s["name"]), s["oct"], s["nov"], s["dec"],
            "Priority" if s["priority"] else ""))
    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Station availability, Q4 2026</title>
<style>
body {{ font-family: Arial, Helvetica, sans-serif; color: #1f2328; background: #ffffff; margin: 24px auto; max-width: 900px; padding: 0 16px; }}
h1 {{ font-size: 20px; margin: 0 0 6px; }}
p {{ font-size: 14px; line-height: 1.45; color: #3a4148; margin: 0 0 10px; }}
figure {{ margin: 12px 0 18px; }}
figure svg {{ width: 100%; height: auto; }}
table {{ border-collapse: collapse; font-size: 13px; width: 100%; }}
th, td {{ text-align: left; padding: 4px 8px; border-bottom: 1px solid #e3e6ea; }}
th {{ border-bottom: 1px solid #1f2328; }}
td:nth-child(n+3):not(:last-child) {{ text-align: right; font-variant-numeric: tabular-nums; }}
tr.p td {{ background: #fce8d8; }}
.src {{ font-size: 12px; color: #59636e; }}
</style>
</head>
<body>
<h1>{word} stations fell under 90 per cent availability in a month of Q4 2026</h1>
<p>Each bar is a station's availability in its lowest month: the share of that month's service minutes (6:00 to midnight)
that began with at least one bike in working order docked. Stations under 90 per cent in any month are Schedule C
priority stations for Q1 2027. The nearest station above the line is {nbs} {nbn}, {nbv:d} per cent in {nbm}.</p>
<figure>
{svg}
</figure>
<table>
<thead><tr><th>Station</th><th>Name</th><th>October (%)</th><th>November (%)</th><th>December (%)</th><th>Q1 2027</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<p class="src">City of Wellhaven, Transportation Services, from Northlane Mobility's trip records and fleet moves
log and the City's archive of the station status feed, 23 September 2026 to 10 January 2027.</p>
</body>
</html>
""".format(word=word, nbs=nb["station"], nbn=html.escape(nb["name"]), nbv=nb["availability"], nbm=nb["month"],
           svg=svg, rows="\n".join(rows))
    open(path, "w", encoding="utf-8", newline="\n").write(page)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    f = compute(target)
    json.dump(f, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    out = os.path.join(os.path.dirname(HERE), "golden")
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out):
        os.remove(os.path.join(out, fn))
    write_xlsx(os.path.join(out, XLSX), f)
    write_html(os.path.join(out, HTML), f)
    return f


if __name__ == "__main__":
    import sys
    f = main(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps({k: v for k, v in f.items() if not k.startswith("_")}, indent=1)[:3000])
