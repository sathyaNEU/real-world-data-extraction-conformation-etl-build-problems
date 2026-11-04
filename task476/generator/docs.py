"""The pack's documents: the pump test reports (two contractors' layouts), the agency's allocation notice, the
utility's schedule book and its rate change letter (PDF), the well register and the totalizer reads (XLSX)."""
import datetime as dt
import math

import numpy as np
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                       # noqa: E402
from openpyxl.styles import Alignment, Font                         # noqa: E402

import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.5, spaceAfter=6)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8.2, leading=10.4, spaceAfter=3)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14.5, leading=18, spaceAfter=4)
SUB = ParagraphStyle("u", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)


def _doc(path, title, owner):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                          topMargin=0.85 * inch, bottomMargin=0.85 * inch, title=title, author=owner,
                          creator=owner, producer=owner, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, owner)
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def _table(rows, widths, font=9.0, head=True):
    t = Table(rows, colWidths=widths)
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", font), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (-1, -1), 2.5)]
    if head:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", font), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black)]
    t.setStyle(TableStyle(st))
    return t


def _grid(rows, widths, font=8.8):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", font), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("FONT", (0, 0), (0, -1), "Helvetica-Bold", font), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3)]))
    return t


# ----------------------------------------------------------------------------------------------- pump tests
def test_values(t):
    """Derived figures exactly as the reports print them, from the field measurements."""
    dh = round(t["psi"] * 2.31, 1)
    th = round(t["pwl"] + dh + t["col"], 1)
    whp = t["q"] * th / 3960.0
    ihp = t["kw"] / 0.746
    ope = 100.0 * whp / ihp
    kwh_af = 1.0241 * th / (ope / 100.0)
    return dict(dh=dh, th=th, whp=whp, ihp=ihp, ope=ope, kwh_af=kwh_af, afd=t["q"] * 1440 / W.AF_GAL)


def write_test_a(path, w, t, sa, superseded=False):
    """Gutierrez Pump Testing's one-page report."""
    p = W.P[w]
    v = test_values(t)
    d, frame = _doc(path, "Pump Efficiency Test %s" % t["job"], W.TESTER_A)
    story = [Paragraph("GUTIERREZ PUMP TESTING", TITLE),
             Paragraph("Pump efficiency test report &nbsp;&nbsp; Job %s &nbsp;&nbsp; Test date %s, %s" % (
                 t["job"], t["t"].astimezone(W.LA).strftime("%B %-d, %Y"), t["t"].astimezone(W.LA).strftime("%-I:%M %p")), SUB),
             _grid([["Customer", W.COMPANY.upper(), "Pump", p["name"].split(" (")[0] if not superseded else t["pump_name"]],
                    ["Electric account", sa, "Motor", "%d HP, 460 V" % (t.get("hp") or p["hp"])],
                    ["Well location", "Sec %s, T18S R21E" % p["swn"].split("-")[1][:2], "Discharge", "Pressurized (micro / drip)"]],
                   [1.15 * inch, 2.45 * inch, 0.75 * inch, 2.15 * inch], font=8.2),
             Spacer(1, 8),
             _table([["Measurement", "Value", "Measurement", "Value"],
                     ["Standing water level (ft)", "%.1f" % t["swl"], "Flow rate (gpm)", "%.0f" % t["q"]],
                     ["Pumping water level (ft)", "%.1f" % t["pwl"], "Input kW", "%.1f" % t["kw"]],
                     ["Drawdown (ft)", "%.1f" % (t["pwl"] - t["swl"]), "Input horsepower", "%.1f" % v["ihp"]],
                     ["Discharge pressure (psi)", "%.1f" % t["psi"], "Water horsepower", "%.1f" % v["whp"]],
                     ["Discharge head (ft)", "%.1f" % v["dh"], "Overall plant efficiency (%)", "%.1f" % v["ope"]],
                     ["Column and fittings loss (ft)", "%.1f" % t["col"], "kWh per acre-foot", "%.0f" % v["kwh_af"]],
                     ["Total head (ft)", "%.1f" % v["th"], "Acre-feet per 24 hours", "%.2f" % v["afd"]]],
                    [1.9 * inch, 0.95 * inch, 2.15 * inch, 1.0 * inch]),
             Spacer(1, 8),
             Paragraph("Levels are measured from ground surface with an electric sounder through the access port. "
                       "Total head = pumping water level + discharge head (psi x 2.31) + column and fittings loss. "
                       "Water horsepower = gpm x total head / 3,960. Overall plant efficiency = water horsepower / "
                       "input horsepower. kWh per acre-foot = 1.0241 x total head / overall plant efficiency.", SMALL),
             Paragraph("Tested by R. Gutierrez. Results are for the conditions measured on the test date.", SMALL)]
    if superseded:
        story.append(Paragraph("Bowl assembly: %s." % t["bowls"], SMALL))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_test_b(path, w, t, sa, superseded=False):
    """Basin Hydrotech's report: state well number first, capacity in acre-feet a day, TDH."""
    p = W.P[w]
    v = test_values(t)
    d, frame = _doc(path, "Pumping Plant Test %s" % t["job"], W.TESTER_B)
    story = [Paragraph("Basin Hydrotech Services", TITLE),
             Paragraph("Pumping plant performance test, ref %s" % t["job"], SUB),
             _table([["Owner", W.COMPANY], ["State well no.", p["swn"]], ["Site", t.get("pump_name") or p["name"]],
                     ["Utility SA", sa], ["Date / time", t["t"].astimezone(W.LA).strftime("%m/%d/%Y %H:%M")],
                     ["Motor", "%d hp" % (t.get("hp") or p["hp"])]], [1.4 * inch, 4.6 * inch], head=False),
             Spacer(1, 8),
             _table([["Item", "Reading"],
                     ["SWL, ft bgs", "%.1f" % t["swl"]], ["PWL, ft bgs", "%.1f" % t["pwl"]],
                     ["Discharge, psi", "%.1f" % t["psi"]], ["Column friction allowance, ft", "%.1f" % t["col"]],
                     ["TDH, ft", "%.1f" % v["th"]], ["Capacity, AF/day", "%.3f" % v["afd"]],
                     ["Capacity, gpm", "%.0f" % t["q"]], ["Motor input, kW", "%.1f" % t["kw"]],
                     ["OPE, %", "%.1f" % v["ope"]], ["Energy, kWh/AF", "%.1f" % v["kwh_af"]]],
                    [3.0 * inch, 1.6 * inch]),
             Spacer(1, 8),
             Paragraph("Definitions. TDH = PWL + discharge psi x 2.31 + column friction. OPE = (gpm x TDH / 3960) / "
                       "(kW / 0.746). Energy per acre-foot (kWh/AF) = 1.0241 x TDH / (OPE / 100). SWL and PWL are "
                       "depths below ground surface; the sounder reads from the top of the sounding tube and the "
                       "tube height is taken off.", SMALL),
             Paragraph("Field crew: D. Coleman, B. Freeman.", SMALL)]
    if superseded:
        story.append(Paragraph("Note: %s." % t["bowls"], SMALL))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def superseded_tests():
    """The 2023 reports on the three pumps the ranch replaced in early 2024 (old bowls, worn)."""
    rng = np.random.default_rng(W.SEED + 404)
    out = {}
    for i, (w, when) in enumerate(sorted(W.REPLACED_2024.items())):
        p = W.P[w]
        t = dt.datetime(2023, 8, 22 + 3 * i, 10, 15, tzinfo=W.PST)
        swl = round(p["base"] + p["amp"] - 2 * p["trend"] + rng.normal(0, 2), 1)
        q = p["q_bep"] * rng.uniform(0.80, 0.88)
        pwl = round(swl + q / p["sc"], 1)
        psi = round(p["disch"] / 2.31 + rng.normal(0, 1.0), 1)
        th = pwl + psi * 2.31 + p["col"]
        ope = rng.uniform(0.54, 0.60)
        kw = round(q * th / 3960.0 * 0.746 / ope, 1)
        out[w] = dict(t=t, swl=swl, pwl=pwl, psi=psi, col=round(p["col"], 1), q=q, kw=kw, hp=p["hp"],
                      job=("GPT-23-%04d" % (611 + 9 * i)) if i != 1 else "BHS-1874",
                      tester=W.TESTER_A if i != 1 else W.TESTER_B, pump_name=p["name"].split(" (")[0],
                      bowls="original bowls, 1998 installation; rebuild recommended")
    return out


# ----------------------------------------------------------------------------------------------- the notice
def write_notice(path, available):
    d, frame = _doc(path, "Water Year 2026 Allocation and True-Up Notice", W.AGENCY)
    alloc_rows = [["APN", "Gross acres", "Sustainable yield (AF)", "Transitional (AF)", "Allocation (AF)"]]
    t_ac = t_sy = t_tr = t_al = 0
    for apn, ac in W.PARCELS:
        # each column to a tenth, the row's allocation the sum of its two printed parts, the totals their columns' sums
        ac10, sy10, tr10 = int(round(ac * 10)), int(round(ac * W.SY_RATE * 10)), int(round(ac * W.TR_RATE * 10))
        alloc_rows.append([apn, "%.1f" % (ac10 / 10), "%.1f" % (sy10 / 10), "%.1f" % (tr10 / 10), "%.1f" % ((sy10 + tr10) / 10)])
        t_ac, t_sy, t_tr, t_al = t_ac + ac10, t_sy + sy10, t_tr + tr10, t_al + sy10 + tr10
    alloc_rows.append(["Total", "%.1f" % (t_ac / 10), "%.1f" % (t_sy / 10), "%.1f" % (t_tr / 10), "%.1f" % (t_al / 10)])
    wells = [["Agency well ID", "State well no.", "APN", "Aquifer"]] + \
        [[W.P[w]["gid"], W.P[w]["swn"], W.P[w]["apn"], W.P[w]["aq"]] for w in sorted(W.WELLS, key=lambda k: W.P[k]["gid"])]
    story = [Paragraph(W.AGENCY.upper(), TITLE),
             Paragraph("Water Year 2026 Allocation and True-Up Notice &nbsp;|&nbsp; Issued October 15, 2026", SUB),
             Paragraph("To: %s, attn. %s, Water Manager" % (W.COMPANY, W.WATER_MANAGER), BODY),
             Paragraph("1. Dates", HEAD),
             Paragraph("This notice opens the water year 2026 true-up for the landowner named above. The extraction "
                       "return for water year 2026 is due November 30, 2026. Any transfer needed under section 4 must "
                       "be recorded with the Agency by December 15, 2026.", BODY),
             Paragraph("2. Allocation and carryover", HEAD),
             Paragraph("Under the Agency's allocation ordinance the water year 2026 groundwater allocation is 1.10 "
                       "acre-feet per gross acre of sustainable yield plus 1.75 acre-feet per gross acre of transitional "
                       "pumping, on the parcels below. Your water year 2025 carryover, as confirmed in the Agency's "
                       "letter of February 9, 2026, is %d acre-feet. The water available to you for water year 2026 "
                       "is the allocation plus the carryover." % W.CARRYOVER, BODY),
             _table(alloc_rows, [1.3 * inch, 1.0 * inch, 1.5 * inch, 1.3 * inch, 1.2 * inch]),
             Paragraph("3. Extraction to report", HEAD),
             Paragraph("Water year 2026 runs from October 1, 2025 through September 30, 2026, local time. Report, for "
                       "every well listed below, the volume of groundwater the well pumped in each month of the water "
                       "year and in the water year, in whole acre-feet. The Agency sums the wells' reported water year "
                       "volumes to give your extraction.", BODY),
             Paragraph("A well with a flow meter reports the difference between its meter readings taken nearest the "
                       "start and the end of each month and of the water year, allowing for any meter exchange. A well "
                       "without a meter reports the volume it pumped, calculated from the well's own records; attach "
                       "the records and the calculation to the return.", BODY),
             _table(wells, [1.4 * inch, 1.6 * inch, 1.3 * inch, 1.0 * inch]),
             Paragraph("4. Transfers and charges", HEAD),
             Paragraph("Extraction above the water available must be covered by a transfer from another landowner in the "
                       "Subbasin, recorded with the Agency by the date in section 1 in whole blocks of %d acre-feet, the "
                       "smallest transfer the Agency records. Extraction "
                       "not covered by December 15, 2026 is charged USD 1,500 per acre-foot and is deducted from the "
                       "water year 2027 allocation. The Agency's posted reference price for intra-basin transfers this "
                       "fall is USD %s per acre-foot." % (W.TRANSFER_BLOCK, "{:,}".format(W.TRANSFER_PRICE)), BODY),
             Paragraph("5. Water levels", HEAD),
             Paragraph("Report each well's spring and fall static depth to water: the depth to water below ground "
                       "surface at the well at the first reading in the window at which the well's pump has been off "
                       "for at least the preceding 24 hours, counted from the end of the last interval in which the "
                       "utility's data for the well's service record energy. The spring window is February 1 to March "
                       "31, 2026 and the fall window October 1 to October 31, 2026, local time. Report feet to one "
                       "decimal.", BODY),
             Paragraph("6. Return format", HEAD),
             Paragraph("Use the Agency's template, one row per well, months in acre-feet and depths in feet, with the "
                       "measurement method (METER or CALCULATED). Questions to %s, Program Manager." % W.AGENCY_PM, BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ----------------------------------------------------------------------------------------------- the utility
def write_tariff(path):
    d, frame = _doc(path, "Agricultural Time-of-Use Schedules AG-2T and AG-3T", W.UTILITY)
    rows = [["Schedule", "Season", "Peak", "Part-peak", "Off-peak"]]
    for sch in ("AG-2T", "AG-3T"):
        for season in ("summer", "winter"):
            r = W.TARIFF[sch][season]
            rows.append([sch, season.capitalize(), ("%.5f" % r["peak"]) if "peak" in r else "", "%.5f" % r["part"],
                         "%.5f" % r["off"]])
    story = [Paragraph(W.UTILITY.upper(), TITLE),
             Paragraph("Electric Schedules AG-2T and AG-3T, Agricultural Power, Time of Use. Rates effective March 1, 2026", SUB),
             Paragraph("Applicability", HEAD),
             Paragraph("Schedules AG-2T and AG-3T apply to agricultural pumping and related end uses. AG-3T is available to "
                       "accounts with a maximum demand of 35 kW or more and carries a demand charge in addition to the "
                       "energy charges; AG-2T carries energy charges only. A customer may change schedule once in any "
                       "twelve months; the change takes effect on the date in the Company's confirmation.", BODY),
             Paragraph("Time periods", HEAD),
             Paragraph("Summer season: June 1 through September 30. Winter season: October 1 through May 31. Summer: "
                       "peak 12:00 noon to 6:00 p.m., part-peak 8:30 a.m. to 12:00 noon and 6:00 p.m. to 9:30 p.m., "
                       "Monday through Friday except holidays; off-peak all other hours. Winter: part-peak 8:30 a.m. to "
                       "9:30 p.m. Monday through Friday except holidays; off-peak all other hours. Times are local "
                       "time. Holidays: New Year's Day, Presidents' Day, Memorial Day, Independence Day, Labor Day, "
                       "Veterans Day, Thanksgiving Day and Christmas Day; a holiday falling on a Saturday is observed "
                       "the Friday before and on a Sunday the Monday after.", BODY),
             Paragraph("Energy charges (USD per kWh)", HEAD),
             _table(rows, [1.0 * inch, 1.0 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch]),
             Paragraph("Demand charge, AG-3T only: USD 9.84 per kW of maximum demand in the billing period, plus USD "
                       "13.66 per kW of maximum peak-period demand in summer billing periods. Customer charge: USD "
                       "0.83 per meter per day. Demand and customer charges are not energy charges.", BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_rate_letter(path):
    d, frame = _doc(path, "Rate Schedule Change Confirmation", W.UTILITY)
    rows = [["Service agreement", "Service address", "From", "To", "Effective"]]
    for w in W.SWITCHED:
        rows.append([W.SA_NEW[w], "%s, Ochre Flats" % W.P[w]["name"].split(" (")[0], "AG-2T", "AG-3T", "June 1, 2026"])
    story = [Paragraph(W.UTILITY.upper(), TITLE), Paragraph("Customer Energy Solutions &nbsp;|&nbsp; May 14, 2026", SUB),
             Paragraph("%s<br/>Attn. %s<br/>6120 W Sallow Plains Rd<br/>Ochre Flats, CA" % (W.COMPANY, W.WATER_MANAGER), BODY),
             Paragraph("Re: Rate schedule change, account 7735102846", BODY),
             Paragraph("This letter confirms the rate schedule change you requested on April 28, 2026 following your "
                       "rate analysis review. The service agreements below will be billed on the schedule shown from "
                       "the effective date. Service agreements on your account that are not listed stay on their "
                       "present schedule.", BODY),
             _table(rows, [1.2 * inch, 1.8 * inch, 0.7 * inch, 0.7 * inch, 1.2 * inch]),
             Paragraph("Thank you for being a %s customer." % W.UTILITY, BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ----------------------------------------------------------------------------------------------- workbooks
def write_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Wells"
    head = ["Well", "Ranch name", "State well no.", "Agency well ID", "APN", "Aquifer", "Total depth (ft)",
            "Pump installed", "Motor (hp)", "Bowl setting (ft below discharge head)",
            "Electric SA (to Mar 31, 2026)", "Electric SA (from Apr 1, 2026)", "Rate schedule", "Flow meter",
            "Level logger", "Logger S/N", "Sensor depth (ft below MP)", "MP height above ground (ft)", "Notes"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    installed = {"W-08": "2024-02-21", "W-11": "2024-03-06", "W-13": "2024-02-28"}
    for w in W.WELLS:
        p = W.P[w]
        meter = {"W-01": "McCrometer MO310, S/N 21-40977, acre-feet", "W-02": "McCrometer MO310, S/N 21-40983, gal x 1000",
                 "W-03": "Seametrics AG3000, S/N 3118842 (to Jun 17, 2026); S/N 3302157 from Jun 17, 2026, gal x 1000",
                 "W-04": "McCrometer MO310, S/N 22-01155, acre-feet"}.get(w, "none")
        if p["metered"]:
            lg = "Solinst Levelogger 5 (absolute pressure; shop barologger S/N %s)" % W.BARO
        else:
            lg = "In-Situ Level TROLL 500 vented (depth to water below MP)"
        notes = {"W-03": "Totalizer on old meter read in gal x 100", "W-07": "Sounding tube 1.25 in.",
                 "W-12": "Booster on separate service, not this SA"}.get(w, "")
        ws.append([w, p["name"], p["swn"], p["gid"], p["apn"], p["aq"], p["depth"],
                   installed.get(w, "2016-05-11" if p["aq"] == "Upper" else "2009-04-02"), p["hp"], p["bowl"],
                   W.SA_OLD[w], W.SA_NEW[w], "AG-2T" if w not in W.SWITCHED else "AG-3T", meter, lg, W.LOGGER_NOW[w],
                   p["sensor"], p["stick"], notes or None])
    for col, wd in zip("ABCDEFGHIJKLMNOPQRS", (7, 22, 16, 13, 12, 8, 9, 12, 8, 13, 15, 15, 9, 38, 44, 10, 11, 10, 30)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "B2"
    wb.save(path)


def write_meters(path, reads):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reads"
    ws.append(["Well", "Meter S/N", "Read date", "Read time", "Totalizer", "Units", "Read by", "Note"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in reads:
        ws.append([None if v == "" else v for v in r])
    for col, wd in zip("ABCDEFGH", (7, 13, 11, 9, 12, 13, 9, 44)):
        ws.column_dimensions[col].width = wd
    wb.save(path)
