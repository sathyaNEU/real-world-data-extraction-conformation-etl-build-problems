"""The golden deliverables, computed from the pack alone (bundle.py): the pilot workbook (the fourteen counties' expected
claim rates with the five and the county next in line, the chart, the 2026 losses and the mitigation pipeline) and the
conformed table of the elevated insured buildings; and generator/figures.json for figures_check.py."""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

XLSX = "tsrfa_2027_private_flood_pilot.xlsx"
NOTES = [
    "Notes",
    "Prepared by Samantha Walter, Flood Insurance Program, for the Board's designation of the 2027 pilot counties.",
    "Sources: FEMA's NFIP policy history and claims extracts for the Authority's communities, pulled 2 October 2026; "
    "the Authority's grants management export of 30 September 2026; the vertical datum offsets by county.",
    "Elevated insured building (guidelines 2.1, 2.2): a dwelling, general property or condominium association policy "
    "with building coverage in force on 30 September 2026 whose lowest floor elevation is at or above its base flood "
    "elevation. Unit owners' and contents policies, and buildings with no base flood elevation, are not counted.",
    "Building-years (2.4): each day of building cover from 1 January 2001 to 31 December 2025 counted once, a policy "
    "covering to the day before its expiration or cancellation date, over 365.25.",
    "Paid building claims as they stand (3.1): each claim under the building's policies with a loss in 2001 to 2025, "
    "counted where its water (the lowest floor elevation the claim was rated on plus the recorded depth) stands an "
    "inch or more above the building's lowest floor on 30 September 2026; elevations on NAVD 1988, NGVD 1929 records "
    "converted with the county offset. For a building never raised this is its paid building claims.",
    "2026 losses: claims Gulfline Mutual had open on 1 July 2026 and NFIP Direct re-entered under the replacing "
    "policies are counted once, at the payments to date on NFIP Direct's record; unit owners' claims included.",
    "Mitigation pipeline: properties not withdrawn whose final inspection had not passed by 30 September 2026, each at "
    "its approved cost times the project's federal cost-share percentage, by the county of the property's community.",
]
CSV = "tsrfa_pilot_elevated_buildings_2026-09-30.csv"


def r1(v):
    return float("%.1f" % (v + 1e-9))


def compute(target):
    D = B.load(target)
    nm = D["names"]
    res = B.rates(target, "golden")
    five, nxt = B.slate(res)
    order = sorted(res, key=lambda f: res[f][2])
    pop = B.population(target)
    cl = B.building_claims(target, pop)
    per_b = []
    for bid in sorted(pop, key=lambda b: (pop[b]["fips"], b)):
        b = pop[bid]
        n = sum(1 for c in cl.get(bid, []) if B.replay_counts(c, b))
        per_b.append((bid, b["fips"], b["days"] / B.YEAR, n))
    counts = {f: sum(1 for b in pop.values() if b["fips"] == f) for f in nm}
    again = {f: 0 for f in nm}
    for bid, b in pop.items():
        for c in cl.get(bid, []):
            if c["dol"].year == 2016 and c["lfe"] < b["lfe"] - 0.45 and B.replay_counts(c, b):
                again[b["fips"]] += 1
    a = B.losses_2026(target, "golden")
    bp = B.pipeline(target, "golden")
    e1 = B.rates(target, "E1")
    return dict(nm=nm, res=res, five=five, nxt=nxt, order=order, per_b=per_b, counts=counts, a=a, b=bp,
                again=again, e1=e1)


def write_xlsx(path, g):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    from openpyxl.drawing.text import CharacterProperties
    from openpyxl.styles import Alignment, Font, PatternFill
    nm, res = g["nm"], g["res"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pilot counties"
    five_names = [nm[f] for f in g["order"] if f in g["five"]]
    ws.append(["2027 pilot: %s and %s, with %s next in line" % (", ".join(five_names[:-1]), five_names[-1],
                                                                 nm[g["nxt"]])])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Expected claim rate: paid building claims the floods of 2001 to 2025 would bring each county's elevated "
               "insured buildings as they stood on 30 September 2026, per 1,000 building-years (see Notes)"])
    ws["A2"].font = Font(italic=True, size=9)
    ws.append([])
    head = ["County", "FIPS", "Expected claim rate per 1,000 building-years", "Pilot"]
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    fill = PatternFill("solid", fgColor="D9E7F1")
    for f in g["order"]:
        n, yrs, rate = res[f]
        mark = "Pilot" if f in g["five"] else ("Next in line" if f == g["nxt"] else None)
        ws.append([nm[f], f, r1(rate), mark])
        row = ws.max_row
        ws.cell(row=row, column=3).number_format = "0.0"
        if f in g["five"]:
            for col in range(1, 5):
                ws.cell(row=row, column=col).fill = fill
    for col, w in zip("ABCD", (16, 8, 18, 13)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 44
    ws.freeze_panes = "A5"
    ch = BarChart()
    ch.type = "bar"
    ch.title = "The five lowest expected claim rates take the 2027 pilot (in blue)"
    ch.y_axis.title = "Paid building claims per 1,000 building-years"
    ch.x_axis.title = None
    ch.gapWidth = 60
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="E3E2DE", w=6350))
    ch.y_axis.numFmt = "0"
    ch.y_axis.delete = False
    ch.x_axis.delete = False
    data = Reference(ws, min_col=3, min_row=4, max_row=4 + len(g["order"]))
    cats = Reference(ws, min_col=1, min_row=5, max_row=4 + len(g["order"]))
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.legend = None
    s = ch.series[0]
    s.graphicalProperties.solidFill = "BDBCB5"
    s.graphicalProperties.line.noFill = True
    for i, f in enumerate(g["order"]):
        if f in g["five"]:
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = "2A78D6"
            pt.graphicalProperties.line.noFill = True
            s.dPt.append(pt)
    ch.x_axis.scaling.orientation = "maxMin"
    ch.y_axis.crosses = "max"
    ch.x_axis.tickLblSkip = 1
    ch.title.tx.rich.p[0].r[0].rPr = CharacterProperties(sz=1100, b=True)
    ch.height, ch.width = 10.5, 16
    ws.add_chart(ch, "F4")
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "4:4"
    ws2 = wb.create_sheet("2026 losses")
    ws2.append(["Claims on losses in 2026 with a building payment, and the building payments made on them, as of the "
                "extract of 2 October 2026 (unit owners' claims included)"])
    ws2["A1"].font = Font(bold=True)
    ws2.append([])
    ws2.append(["County", "FIPS", "Claims with a building payment", "Building payments ($)"])
    for c in ws2[3]:
        c.font = Font(bold=True)
    for f in sorted(nm, key=lambda f: nm[f]):
        ws2.append([nm[f], f, g["a"][f][0], int(round(g["a"][f][1]))])
        ws2.cell(row=ws2.max_row, column=4).number_format = "#,##0"
    ws2.append(["All counties", None, sum(v[0] for v in g["a"].values()), int(round(sum(v[1] for v in g["a"].values())))])
    ws2.cell(row=ws2.max_row, column=4).number_format = "#,##0"
    ws2.cell(row=ws2.max_row, column=1).font = Font(bold=True)
    for col, w in zip("ABCD", (16, 8, 16, 18)):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "A4"
    ws3 = wb.create_sheet("Mitigation pipeline")
    ws3.append(["Buildings in the Authority's elevation and acquisition projects not completed on 30 September 2026, "
                "and the federal share obligated to them"])
    ws3["A1"].font = Font(bold=True)
    ws3.append([])
    ws3.append(["County", "FIPS", "Buildings not completed", "Federal share obligated ($)"])
    for c in ws3[3]:
        c.font = Font(bold=True)
    for f in sorted(nm, key=lambda f: nm[f]):
        ws3.append([nm[f], f, g["b"][f][0], g["b"][f][1]])
        ws3.cell(row=ws3.max_row, column=4).number_format = "#,##0"
    ws3.append(["All counties", None, sum(v[0] for v in g["b"].values()), sum(v[1] for v in g["b"].values())])
    ws3.cell(row=ws3.max_row, column=4).number_format = "#,##0"
    ws3.cell(row=ws3.max_row, column=1).font = Font(bold=True)
    for col, w in zip("ABCD", (16, 8, 14, 20)):
        ws3.column_dimensions[col].width = w
    ws3.freeze_panes = "A4"
    ws4 = wb.create_sheet("Notes")
    for line in NOTES:
        ws4.append([line])
    ws4["A1"].font = Font(bold=True)
    ws4.column_dimensions["A"].width = 120
    for row in ws4.iter_rows(min_row=2):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_csv(path, g):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["nfip_building_id", "county_fips", "county", "building_years", "paid_building_claims_as_it_stands"])
        for bid, f, yrs, n in g["per_b"]:
            w.writerow([bid, f, g["nm"][f], "%.1f" % (yrs + 1e-9), n])


def figures(g):
    nm, res = g["nm"], g["res"]
    return {
        "conventions": {"rate_per_building_years": "1,000", "days_per_building_year": "365.25"},
        "rate_order": [nm[f] for f in g["order"]],
        "call": {"five": sorted(nm[f] for f in g["five"]), "next": nm[g["nxt"]],
                 "excluded_by_the_replay": sorted(nm[f] for f in ("58007", "58027"))},
        "components": {
            "rates": {nm[f]: "%.1f" % r1(res[f][2]) for f in res},
            "claims_as_they_stand": {nm[f]: res[f][0] for f in res},
            "building_years": {nm[f]: "%.1f" % r1(res[f][1]) for f in res},
            "elevated_insured_buildings": {nm[f]: g["counts"][f] for f in res},
        },
        "default_path": {"five": sorted(nm[f] for f in B.slate(g["e1"])[0]), "next": nm[B.slate(g["e1"])[1]],
                         "rates": {nm[f]: "%.1f" % r1(g["e1"][f][2]) for f in ("58007", "58027")}},
        "replayed_2016": {nm[f]: g["again"][f] for f in ("58007", "58027")},
        "a_losses": {nm[f]: {"claims": g["a"][f][0], "payments": int(round(g["a"][f][1]))} for f in g["a"]},
        "b_pipeline": {nm[f]: {"buildings": g["b"][f][0], "federal_share": g["b"][f][1]} for f in g["b"]},
        "csv": {"rows": len(g["per_b"]), "claims": sum(r[3] for r in g["per_b"]),
                "buildings_with_a_claim": sum(1 for r in g["per_b"] if r[3] > 0)},
    }


def main(target, gdir, fig_path):
    g = compute(target)
    os.makedirs(gdir, exist_ok=True)
    write_xlsx(os.path.join(gdir, XLSX), g)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, XLSX), "Samantha Walter", "Samantha Walter", "2026-10-13T15:02:00Z",
                       "2026-10-19T20:41:17Z", excel=True, company="Tarrow Sound Regional Flood Authority")
    write_csv(os.path.join(gdir, CSV), g)
    fig = figures(g)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    main(t, sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(HERE), "golden"),
         os.path.join(HERE, "figures.json"))
