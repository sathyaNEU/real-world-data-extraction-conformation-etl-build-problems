"""The golden deliverables: the boardings workbook and the investment committee note with its chart, written from
the analysis of target/ alone, plus figures.json."""
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402

BOOK = "rathgarvan_boardings_2029.xlsx"
MEMO = "rathgarvan_demand_note.docx"
ZONE_NAMES = {"KW01": "Kilcarrow city centre", "KW02": "Kilcarrow Docklands", "KW03": "University Hospital campus",
              "KW04": "Kilcarrow University", "KW05": "Carrigboy business park", "KW06": "Port of Kilcarrow, Ringcurran",
              "KW07": "Ballymurragh retail park", "KW08": "Airport business park", "KW09": "Lisnagry and Ardnagree",
              "KW10": "Rathgarvan", "KW11": "Rest of County Kilcarrow"}
STATION_NAMES = {"ARD": "Ardnagree", "LSG": "Lisnagry", "KCN": "Kilcarrow Central", "KDK": "Kilcarrow Docklands",
                 "KUH": "University Hospital", "CBY": "Carrigboy", "LINE": "Ardnagree line"}
ORDER = ["ARD", "LSG", "KCN", "KDK", "KUH", "CBY", "LINE"]


def r10(x):
    return int(round(x / 10.0)) * 10


def r100(x):
    return int(round(x / 100.0)) * 100


def pct(x):
    return int(round(100 * x))


def figures(R):
    zones = [z for z in sorted(R["shares"]) if R["shares"][z] > 0]
    b_zones = [z for z in sorted(R["shares"]) if R["shares"][z] >= 0.10]
    f = {
        "total_boardings": r100(R["golden"]), "total_boardings_exact": round(R["golden"], 1),
        "scope": "reduced scheme", "threshold": R["threshold"],
        "zone_boardings": {z: r10(R["boardings"][z]) for z in zones},
        "zone_commuters": {z: R["census"][z] for z in zones},
        "zone_share": {z: R["shares"][z] for z in zones},
        "zone_weekday_share": {z: round(100 * R["freq"][z], 1) for z in zones},
        "zone_days_per_week": {z: round(5 * R["freq"][z], 2) for z in zones},
        "arrival_share": {z: pct(R["arrivals"][z]) for z in b_zones},
        "station_ratio": {s: pct(R["station_ratios"][s]) for s in ORDER},
        "station_means_2027": {s: int(round(R["station_means"][s][0])) for s in ORDER},
        "station_means_2019": {s: int(round(R["station_means"][s][1])) for s in ORDER},
        "ordinary_weekdays": R["ordinary_days"],
        "census_daily_route": round(R["census_daily"], 1), "census_daily_route_rounded": r100(R["census_daily"]),
        "pooled_route": round(R["pooled_route"], 1), "network_route": round(R["network_route"], 1),
        "lisnagry_route": round(R["lisnagry_route"], 1), "network_ratio_pct": round(100 * R["network_ratio"], 1),
        "pooled_weekday_share_pct": round(100 * R["f_pooled"], 1),
        "gap_to_threshold": int(round(R["threshold"] - R["golden"])),
        "census_commuters_served": sum(R["census"][z] for z in zones),
    }
    return f


def chart(R, path):
    zones = [z for z in sorted(R["shares"]) if R["shares"][z] > 0]
    zones.sort(key=lambda z: -R["boardings"][z])
    vals = [r10(R["boardings"][z]) for z in zones]
    names = [ZONE_NAMES[z] for z in zones]
    fig, ax = plt.subplots(figsize=(7.4, 4.1), dpi=150)
    ax.barh(range(len(zones))[::-1], vals, color="#2f6b8f", height=0.62)
    for i, v in enumerate(vals):
        ax.text(v + 4, len(zones) - 1 - i, "{:,}".format(v), va="center", fontsize=8.5, color="#1d2b33")
    ax.set_yticks(range(len(zones))[::-1])
    ax.set_yticklabels(names, fontsize=8.5)
    ax.set_xlabel("Commuter boardings at Rathgarvan, average ordinary weekday, 2029", fontsize=8.5)
    ax.set_title("Rathgarvan: weekday commuter boardings by workplace zone (total %s)"
                 % "{:,}".format(r100(R["golden"])), fontsize=9.5, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, max(vals) * 1.15)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None, "Creation Time": None})
    plt.close(fig)


def write_book(R, F, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Boardings 2029"
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DDE7EE")
    ws["A1"] = "Rathgarvan station: commuter boardings on an average ordinary weekday, 2029"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Census 2022 commuters (final release) by workplace zone x station share (2026 model) x share of "
                "ordinary weekdays the zone's commuters travel to work there (resident mobility panel, 6 Sep to "
                "26 Nov 2027, ordinary weekdays only).")
    hdr = ["Zone code", "Workplace zone", "Census commuters", "Station share", "Ordinary weekdays travelled (%)",
           "Days a week", "Boardings (exact)", "Boardings (nearest 10)"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    zones = [z for z in sorted(R["shares"]) if R["shares"][z] > 0]
    r = 5
    for z in zones:
        vals = [z, ZONE_NAMES[z], R["census"][z], R["shares"][z], round(100 * R["freq"][z], 1),
                round(5 * R["freq"][z], 2), round(R["boardings"][z], 1), r10(R["boardings"][z])]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=v)
        r += 1
    ws.cell(row=r, column=2, value="Total").font = bold
    ws.cell(row=r, column=3, value=sum(R["census"][z] for z in zones))
    ws.cell(row=r, column=7, value=round(R["golden"], 1))
    ws.cell(row=r, column=8, value=r100(R["golden"])).font = bold
    ws.cell(row=r + 1, column=2, value="Total, nearest 100")
    ws.cell(row=r + 1, column=8, value=r100(R["golden"]))
    ws.cell(row=r + 3, column=2, value="Scope test (full scheme at %s or more)" % "{:,}".format(R["threshold"])).font = bold
    ws.cell(row=r + 3, column=8, value="Reduced scheme")
    ws.cell(row=r + 4, column=2, value="Counting every census commuter as a boarding every weekday would give")
    ws.cell(row=r + 4, column=8, value=round(R["census_daily"], 1))
    for col, w in zip("ABCDEFGH", (10, 30, 12, 10, 16, 10, 13, 13)):
        ws.column_dimensions[col].width = w

    ws2 = wb.create_sheet("Arrival 0730-0930")
    ws2["A1"] = "Share of journeys to work reaching the workplace between 07:30 and 09:30 (Irish time), ordinary weekdays"
    ws2["A1"].font = Font(bold=True)
    for j, h in enumerate(["Zone code", "Workplace zone", "Station share", "Journeys to work in the panel",
                           "Share 07:30-09:30 (%)"], 1):
        c = ws2.cell(row=3, column=j, value=h)
        c.font = bold
        c.fill = head
    rr = 4
    for z in sorted(F["arrival_share"]):
        for j, v in enumerate([z, ZONE_NAMES[z], R["shares"][z], R["arrival_days"][z], F["arrival_share"][z]], 1):
            ws2.cell(row=rr, column=j, value=v)
        rr += 1
    ws2.column_dimensions["B"].width = 30
    ws2.column_dimensions["D"].width = 16

    ws3 = wb.create_sheet("Stations 2027 v 2019")
    ws3["A1"] = ("Average ordinary-weekday gate entries, September to November, 2027 against 2019 (all gatelines of "
                 "each station; University Hospital with UHK, Carrigboy with Carrigboy Halt)")
    ws3["A1"].font = Font(bold=True)
    for j, h in enumerate(["Station", "2019 average", "2027 average", "2027 as share of 2019 (%)"], 1):
        c = ws3.cell(row=3, column=j, value=h)
        c.font = bold
        c.fill = head
    rr = 4
    for s in ORDER:
        for j, v in enumerate([STATION_NAMES[s], F["station_means_2019"][s], F["station_means_2027"][s],
                               F["station_ratio"][s]], 1):
            ws3.cell(row=rr, column=j, value=v)
        rr += 1
    ws3.column_dimensions["A"].width = 24
    wb.save(path)
    IO.repack_ooxml(path, "Rail Planning", "Rail Planning", "2027-12-06T15:10:00Z", "2027-12-06T17:42:00Z",
                    "Rathgarvan boardings 2029", "Kilcarrow Metropolitan Transport Authority")


def write_memo(R, F, path, png):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
    doc.add_heading("Rathgarvan station: commuter demand for the scope decision", level=1)
    doc.add_paragraph("To: Investment Committee, 14 December 2027. From: Rail Planning.")
    p = doc.add_paragraph()
    p.add_run("Recommendation. ").bold = True
    p.add_run("Rathgarvan will carry about %s commuter boardings on an average ordinary weekday in 2029, below the "
              "%s that justifies the full scheme, so build the reduced scheme (four-car platforms, 90-space car park, "
              "passive provision for extension)." % ("{:,}".format(F["total_boardings"]), "{:,}".format(R["threshold"])))
    p = doc.add_paragraph()
    p.add_run("Basis. ").bold = True
    p.add_run("The census counts each worker once, at a usual workplace. A boarding is a journey made on the day, and "
              "the operator's resident panel shows how many ordinary weekdays the catchment's commuters to each zone "
              "actually go in: about %s days a week to the Docklands offices, %s to the hospital campus and %s to "
              "Carrigboy, where most staff work twelve-hour rosters. Taking each commuter as a boarding every weekday "
              "would give about %s and the full scheme."
              % ("%.1f" % (5 * R["freq"]["KW02"]), "%.1f" % (5 * R["freq"]["KW03"]), "%.1f" % (5 * R["freq"]["KW05"]),
                 "{:,}".format(r100(R["census_daily"]))))
    doc.add_picture(png, width=Cm(15.5))
    t = doc.add_table(rows=1, cols=3)
    t.style = "Light List Accent 1"
    for j, h in enumerate(["Workplace zone", "Census commuters x station share", "Boardings"]):
        t.rows[0].cells[j].text = h
    zones = [z for z in sorted(R["shares"]) if R["shares"][z] > 0]
    zones.sort(key=lambda z: -R["boardings"][z])
    for z in zones:
        c = t.add_row().cells
        c[0].text = ZONE_NAMES[z]
        c[1].text = "{:,}".format(int(round(R["census"][z] * R["shares"][z])))
        c[2].text = "{:,}".format(F["zone_boardings"][z])
    c = t.add_row().cells
    c[0].text, c[2].text = "Total", "{:,}".format(F["total_boardings"])
    doc.add_paragraph("")
    doc.add_paragraph("The existing stations show the same pattern: in autumn 2027 the line carried %d per cent of "
                      "its autumn 2019 ordinary-weekday entries, from %d per cent at Kilcarrow Docklands to %d per cent "
                      "at University Hospital. Station figures count every gateline at each station, including the "
                      "secondary entrances recorded under their own location codes."
                      % (F["station_ratio"]["LINE"], F["station_ratio"]["KDK"], F["station_ratio"]["KUH"]))
    doc.core_properties.author = "Rail Planning"
    doc.save(path)
    IO.repack_ooxml(path, "Rail Planning", "Rail Planning", "2027-12-06T15:30:00Z", "2027-12-06T18:05:00Z",
                    "Rathgarvan commuter demand", "Kilcarrow Metropolitan Transport Authority")


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    R = A.run(target)
    F = figures(R)
    png = os.path.join(gen, "boardings_by_zone.png")
    chart(R, png)
    write_book(R, F, os.path.join(golden, BOOK))
    write_memo(R, F, os.path.join(golden, MEMO), png)
    json.dump(F, open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump({k: v for k, v in R.items() if k not in ("variants",)}, open(os.path.join(gen, "results.json"), "w"),
              indent=1, sort_keys=True, default=str)
    json.dump(R["variants"], open(os.path.join(gen, "variants.json"), "w"), indent=1, sort_keys=True)
    return R, F
