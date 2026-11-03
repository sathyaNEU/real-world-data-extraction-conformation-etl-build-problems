"""Write the shipped files from the world, each through its producing system's own habits."""
import csv
import datetime as dt
import io
import os
import random

import pandas as pd

import office as O
import params as P
import world as Wd

D = dt.timedelta
HUB_NAME = {h[0]: h[1] for h in P.HUBS}
FILES = {
    "roster": "roster/front_line_driving_roster_2026-10-01.csv",
    "crosswalk": "hr/vennerley_staff_number_crosswalk.xlsx",
    "measure": "occupational_health/cab_fit_measurements_2025_26.xlsx",
    "standard": "policy/cab_fit_standard_issue2.docx",
    "posture": "policy/driver_posture_model_ellisand_2025.pdf",
    "seat": "fleet/seat_dimension_sheet_brevin_as7.pdf",
    "pkg_pennick": "fleet/package_drawing_data_pennick.pdf",
    "pkg_wrenfold": "fleet/package_drawing_data_wrenfold.pdf",
    "pkg_ostrel": "fleet/package_drawing_data_ostrel.pdf",
    "kpi": "policy/fleet_performance_reporting_standard_issue4.pdf",
    "register": "fleet/front_line_fleet_register_2026-10-01.xlsx",
    "disposals": "fleet/vehicle_disposals_2025_26.xlsx",
    "assets": "fleet/vennerley_asset_list_2025-06-27.xlsx",
    "units": "fleet/telematics_unit_changes.xlsx",
    "odometer": "fleet/telematics_daily_odometer_2025_26.csv",
    "jobs": "fleet/workshop_jobs_2025_26.csv",
    "legacy_jobs": "fleet/vennerley_workshop_jobs_apr_jun_2025.csv",
    "codemap": "fleet/workshop_code_map.xlsx",
    "prices": "procurement/tender_prices_2027_shortlist.xlsx",
    "reference": "reference/adult_body_dimensions_reference_tables.pdf",
}
DISTRACTORS = ["prices", "reference"]


def _p(root, key):
    path = os.path.join(root, FILES[key])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def _csv(path, header, rows, crlf=True, bom=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    data = buf.getvalue().encode("utf-8")
    with open(path, "wb") as fh:
        fh.write((b"\xef\xbb\xbf" if bom else b"") + data)


def _uk(d):
    return d.strftime("%d/%m/%Y")


def _dt(d):
    return dt.datetime(d.year, d.month, d.day)


# ----------------------------------------------------------------------------------------------- people
def write_people(root, W):
    rnd = random.Random(P.SEED + 11)
    staff = W["staff"]
    roster = [s for s in staff if s["on_roster"]]
    for s in roster:
        s["line"] = "L%02d" % rnd.randint(1, 16)
    rows = sorted(roster, key=lambda s: (s["hub"], s["line"], s["service"]))
    _csv(_p(root, "roster"), ["Staff number", "Hub code", "Hub", "Role", "Contract", "Sex", "Rota line"],
         [[s["service"], s["hub"], HUB_NAME[s["hub"]], s["role"], s["contract"], s["sex"], s["line"]] for s in rows],
         crlf=True, bom=True)
    cw = sorted([s for s in staff if s["legacy"]], key=lambda s: s["legacy"])
    extra = []
    # former Vennerley staff who left before the programme still sit in the crosswalk
    pool = Wd._numbers(rnd, 260, 10000, 99999)
    used = {s["legacy"] for s in cw}
    svc = Wd._numbers(rnd, 260, 20000000, 79999999)
    have = {s["service"] for s in staff}
    for a, b in zip(pool, svc):
        lg = "VAS%05d" % a
        if lg in used or str(b) in have:
            continue
        extra.append((lg, str(b)))
        if len(extra) >= 117:
            break
    df = pd.DataFrame([(s["legacy"], s["service"], _dt(P.HR_MIGRATION)) for s in cw] +
                      [(a, b, _dt(P.HR_MIGRATION)) for a, b in extra],
                      columns=["Former Vennerley staff number", "Service staff number", "Effective from"])
    df = df.sort_values("Former Vennerley staff number").reset_index(drop=True)
    O.xlsx(_p(root, "crosswalk"), [("Crosswalk", df)], author="Liam Jackson", created="2025-08-28T10:14:00Z",
           modified="2025-08-29T15:02:00Z", widths={"Crosswalk": [30, 24, 16]}, title="Vennerley staff numbers")
    # measurements
    initials = {"Strakemoor": ["JKe", "RMo", "TSa", "ABi", "HCo"], "Vennerley": ["PWh", "LHa", "DNo", "SGr"]}
    refs = Wd._numbers(rnd, 4000, 100000, 999999)
    hubs_area = {a: [h[0] for h in P.HUBS if h[2] == a] for a in ("Strakemoor", "Vennerley")}
    out = []
    k = 0
    for s in staff:
        for r in s["records"]:
            hub = s["hub"] if rnd.random() < 0.94 else rnd.choice(hubs_area[s["area"]])
            row = {"Ref": "CF%06d" % refs[k], "Staff number": r["key"], "Date measured": _dt(r["date"]),
                   "Hub where measured": HUB_NAME[hub],
                   "Form": "Vennerley paper form" if r["units"] == "imperial" else "OH e-form",
                   "Stature (mm)": None, "Stature (ft)": None, "Stature (in)": None, "Sitting eye height (mm)": None,
                   "Sitting eye height (in)": None, "Weight (kg)": None, "Weight (st)": None, "Weight (lb)": None,
                   "Measured by": rnd.choice(initials[s["area"]])}
            if r["units"] == "imperial":
                row.update({"Stature (ft)": r["ft"], "Stature (in)": r["in"], "Sitting eye height (in)": r["seh_in"],
                            "Weight (st)": r["st"], "Weight (lb)": r["lb"]})
            else:
                row.update({"Stature (mm)": int(r["stature"]), "Sitting eye height (mm)": int(r["seh"]),
                            "Weight (kg)": r["weight"]})
            out.append(row)
            k += 1
    df = pd.DataFrame(out).sort_values(["Date measured", "Ref"]).reset_index(drop=True)
    O.xlsx(_p(root, "measure"), [("Measurements", df)], author="Occupational Health", created="2025-03-03T08:40:00Z",
           modified="2026-10-02T09:26:00Z", last="Liam Jackson",
           widths={"Measurements": [11, 15, 14, 18, 20, 12, 11, 11, 14, 14, 11, 10, 10, 11]},
           number_formats={"Measurements": {"Weight (kg)": "0.0", "Stature (in)": "0.00", "Sitting eye height (in)": "0.00"}},
           title="Cab fit measurement programme")


# ----------------------------------------------------------------------------------------------- documents
def _styles():
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    O.word_fonts()
    base = ParagraphStyle("b", fontName="Calibri", fontSize=10.5, leading=13.4, spaceAfter=6)
    return {"body": base,
            "h1": ParagraphStyle("h1", parent=base, fontName="Calibri-Bold", fontSize=15, leading=19, spaceAfter=10,
                                 textColor=colors.HexColor("#1F3864")),
            "h2": ParagraphStyle("h2", parent=base, fontName="Calibri-Bold", fontSize=11.5, leading=15, spaceBefore=8,
                                 spaceAfter=4, textColor=colors.HexColor("#1F3864")),
            "small": ParagraphStyle("s", parent=base, fontSize=8.5, leading=10.5, textColor=colors.HexColor("#444444")),
            "cell": ParagraphStyle("c", parent=base, fontSize=9, leading=11, spaceAfter=0)}


def _table(rows, widths, st, head=True):
    from reportlab.platypus import Paragraph, Table, TableStyle
    from reportlab.lib import colors
    data = [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8C8C8C")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E1F2")))
    t.setStyle(TableStyle(style))
    return t


def _pdf(root, key, title, author, created, story, producer="Microsoft® Word for Microsoft 365", footer=None,
         modified=None):
    O.pdf(_p(root, key), story, title=title, author=author, created_pdf=created, modified_pdf=modified, producer=producer,
          creator=producer, footer=footer, footer_font="Calibri")


def posture_report(root):
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.units import mm
    m = P.POSTURE

    def story():
        st = _styles()
        s = [Paragraph("Driver posture model for front-line ambulance cabs", st["h1"]),
             Paragraph("Prepared for Hallowfen Ambulance Service Fleet Services by Ellisand Human Factors. Report EHF-2507, "
                       "issue 1, 21 July 2025.", st["small"]), Spacer(1, 4 * mm),
             Paragraph("1. Purpose", st["h2"]),
             Paragraph("The service asked for a model that predicts where each of its drivers sits at the wheel of a "
                       "front-line ambulance, so that cabs offered for future orders can be assessed against the service's "
                       "own drivers rather than against published percentile manikins. The model was fitted to the seat "
                       "trial run in May and June 2025 in the service's current cabs.", st["body"]),
             Paragraph("2. What the model predicts", st["h2"]),
             Paragraph("For a driver of given stature, body mass index and sitting eye height, in a cab whose seat height "
                       "(H30, the hip point's height above the accelerator heel point) is known, the model predicts the "
                       "driver's own driving posture: the hip point (H-point) aft of the accelerator heel point, the torso "
                       "angle from vertical, and the eye point. Distances are in millimetres along the vehicle's length "
                       "(positive rearward) and height (positive upward) from the accelerator heel point.", st["body"]),
             _table([["Quantity", "Prediction"],
                     ["Hip point aft of the heel point (mm)",
                      "%.0f + %.2f x (stature - %d) + %.1f x (BMI - %d) %s %.2f x (H30 - %d)" % (
                          m["hx0"], m["hx_s"], m["s0"], m["hx_b"], m["b0"], "-", -m["hx_h"], m["h0"])],
                     ["Torso angle from vertical (degrees)",
                      "%.1f + %.3f x (stature - %d) + %.2f x (BMI - %d)" % (m["t0"], m["t_s"], m["s0"], m["t_b"], m["b0"])],
                     ["Eye point, along the vehicle", "%d mm forward of the hip point" % (-m["ex"])],
                     ["Eye point, height above the heel point", "H30 + %.3f x sitting eye height" % m["ez"]]],
                    [62 * mm, 104 * mm], st),
             Spacer(1, 3 * mm),
             Paragraph("Stature and sitting eye height are in millimetres, sitting eye height measured seated erect; body "
                       "mass index is weight in kilograms divided by the square of stature in metres.", st["body"]),
             Paragraph("3. Trial and validation", st["h2"]),
             Paragraph("One hundred and eighty drivers from all nine hubs, chosen to span the service's range of stature, "
                       "sat in four current cab types, set the seat as they would for a shift and drove a fixed route. The "
                       "seat's track position and recline were then read off and converted to the hip point and torso "
                       "angle. Predictions from the model above against the positions the drivers chose:", st["body"]),
             _table([["Current cab", "Drivers", "Hip point, mean difference (mm)", "Hip point, s.d. (mm)",
                      "Torso angle, mean difference (deg)", "Torso angle, s.d. (deg)"],
                     ["Pennick FD35 (2019 build)", "52", "+1.8", "17.6", "-0.2", "2.1"],
                     ["Ostrel FD35 (2021 build)", "47", "-2.4", "18.9", "+0.3", "2.3"],
                     ["Corvane FD35", "41", "+0.9", "19.4", "+0.1", "2.0"],
                     ["Corvane RD43", "40", "-1.1", "18.2", "-0.4", "2.4"]],
                    [36 * mm, 15 * mm, 30 * mm, 24 * mm, 32 * mm, 26 * mm], st),
             Spacer(1, 3 * mm),
             Paragraph("No cab type shows a systematic difference, and the spread is what repeated sittings by the same "
                       "driver show. The model is suitable for assessing cabs offered for the 2027 order.", st["body"]),
             Paragraph("4. Limits", st["h2"]),
             Paragraph("The model was fitted to drivers between 1,480 mm and 2,010 mm tall with body mass index between 18 "
                       "and 47, and to seat heights between 380 mm and 440 mm. It predicts posture only; it says nothing "
                       "about comfort over a shift.", st["body"])]
        return s
    _pdf(root, "posture", "Driver posture model for front-line ambulance cabs", "Ellisand Human Factors", "20250721113500",
         story, footer="Ellisand Human Factors  EHF-2507 issue 1")


def seat_sheet(root):
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.units import mm
    si = P.SEAT_IN

    def story():
        st = _styles()
        rows = [["Ref", "Dimension", "inches"],
                ["S1", "Overall height, cushion base to top of backrest", "39.37"],
                ["S2", "Cushion width", "19.29"],
                ["S3", "Cushion depth, front edge to backrest at the H-point", "18.70"],
                ["S4", "Backrest, from the H-point along the torso line to the top rear corner", "%.2f" % si["backrest_along"]],
                ["S5", "Backrest rear face behind the torso line at the top rear corner", "%.2f" % si["backrest_behind"]],
                ["S6", "Backrest width at the shoulders", "20.47"],
                ["S7", "Recline range, torso line from vertical (degrees)", "%d to %d" % (si["recline_min"], si["recline_max"])],
                ["S8", "Slide length, standard slide", "%.2f" % si["slide_standard"]],
                ["S9", "Slide length, long slide", "%.2f" % si["slide_long"]],
                ["S10", "Slide length, extended slide", "%.2f" % si["slide_extended"]],
                ["S11", "Suspension stroke", "3.15"],
                ["S12", "Height adjustment range", "2.36"],
                ["S13", "Mass with long slide (lb)", "66.1"]]
        return [Paragraph("AS-7 suspension driver seat: dimension sheet", st["h1"]),
                Paragraph("Brevin Seating. Sheet AS7-D, revision C, March 2024. Dimensions in inches unless stated.",
                          st["small"]), Spacer(1, 4 * mm),
                _table(rows, [14 * mm, 120 * mm, 26 * mm], st), Spacer(1, 4 * mm),
                Paragraph("The H-point is the hip point of the seated occupant as located by the SAE J826 manikin. The torso "
                          "line runs from the H-point parallel to the backrest. Slides are interchangeable on the AS-7 "
                          "base; the converter sets the slide's position in the cab.", st["body"]),
                Paragraph("Approved for road ambulance use with integrated three-point belt. Recline by lever, infinitely "
                          "adjustable within S7.", st["body"])]
    _pdf(root, "seat", "AS-7 suspension driver seat dimension sheet", "Brevin Seating", "20240314092200", story,
         footer="Brevin Seating  AS7-D rev C")


def _pkg_rows(cab, sgrp=None):
    ch = P.CHASSIS[cab["chassis"]]

    def pt(x, z):
        if sgrp:
            return x - sgrp[0], z - sgrp[1]
        return x, z
    t0, t1 = cab["travel"]
    b0, b1 = cab["bulkhead"]
    hx, hz = ch["header"]
    bx, bz = ch["bonnet"]
    wheel = {"FD35": (472, 735), "RD43": (455, 752)}[cab["chassis"]]
    roof = {"FD35": 1622, "RD43": 1658}[cab["chassis"]]
    saloon = {"PEN": 3040, "WRE": 3190, "OST": 3010}[cab["id"][:3]]
    rows = []
    if sgrp:
        rows += [["Seat height H30 (SgRP above the accelerator heel point)", "%d" % cab["h30"]],
                 ["H-point travel, front limit (x)", "%+d" % pt(t0, 0)[0]], ["H-point travel, rear limit (x)", "%+d" % pt(t1, 0)[0]],
                 ["Bulkhead trim face at floor (x, z)", "%+d, %+d" % pt(b0, 0)],
                 ["Bulkhead trim face 1,700 above floor (x, z)", "%+d, %+d" % pt(b1, 1700)],
                 ["Windscreen header, lower edge of clear area (x, z)", "%+d, %+d" % pt(hx, hz)],
                 ["Lowest road sight point over bonnet (x, z)", "%+d, %+d" % pt(bx, bz)],
                 ["Steering wheel centre (x, z)", "%+d, %+d" % pt(*wheel)], ["Steering wheel diameter", "400"],
                 ["Roof lining above floor at SgRP", "%d" % roof], ["Driver door aperture height", "1,184"],
                 ["Saloon interior length, bulkhead to rear doors", "%s" % format(saloon, ",")],
                 ["Saloon interior height", "1,905"], ["Bulkhead walk-through door width", "560"]]
    else:
        rows += [["Seat height H30 (H-point above the accelerator heel point)", "%d" % cab["h30"]],
                 ["H-point travel, front limit aft of the heel point", "%d" % t0], ["H-point travel, rear limit aft of the heel point", "%d" % t1],
                 ["Bulkhead trim face at floor, aft of the heel point", "%d" % b0],
                 ["Bulkhead trim face 1,700 above floor, aft of the heel point", "%d" % b1],
                 ["Windscreen header, lower edge of clear area (x, z)", "%d, %d" % (hx, hz)],
                 ["Lowest road sight point over bonnet (x, z)", "%d, %d" % (bx, bz)],
                 ["Steering wheel centre (x, z)", "%d, %d" % wheel], ["Steering wheel diameter", "400"],
                 ["Roof lining above floor at the H-point", "%d" % roof], ["Driver door aperture height", "1,184"],
                 ["Saloon interior length, bulkhead to rear doors", "%s" % format(saloon, ",")],
                 ["Saloon interior height", "1,905"], ["Bulkhead walk-through door width", "560"]]
    return rows


def package(root, key, converter, cabs, sgrp, created, issue):
    from reportlab.platypus import Paragraph, Spacer, PageBreak
    from reportlab.lib.units import mm
    short = converter.split()[0]

    def story():
        st = _styles()
        s = [Paragraph("%s: cab package data for Hallowfen Ambulance Service tender HAS-F-2026-04" % converter, st["h1"]),
             Paragraph("Driver's side package, issue %s. Dimensions in millimetres. Seat: Brevin AS-7 with the %s slide." %
                       (issue, cabs[0]["slide"]), st["small"]), Spacer(1, 4 * mm)]
        if sgrp:
            s.append(Paragraph("All x and z dimensions are given from each cab's seating reference point (SgRP), the design "
                               "H-point, located as stated for each chassis. x is positive rearward and z positive upward.",
                               st["body"]))
        else:
            s.append(Paragraph("x is measured rearward and z upward from the accelerator heel point, the heel of the "
                               "driver's right shoe on the depressed floor covering at the accelerator.", st["body"]))
        for i, cab in enumerate(cabs):
            s.append(Paragraph("%s conversion on the %s chassis-cab" % (short, cab["chassis"]), st["h2"]))
            sg = sgrp[cab["chassis"]] if sgrp else None
            if sg:
                s.append(Paragraph("SgRP located %d mm aft of and %d mm above the accelerator heel point." % sg, st["body"]))
            s.append(_table([["Dimension", "Value"]] + _pkg_rows(cab, sg), [118 * mm, 48 * mm], st))
            s.append(Spacer(1, 3 * mm))
        s.append(Paragraph("Windscreen and bonnet points are taken from the chassis maker's body builder data for the "
                           "%s. Saloon dimensions are for the stretcher-side wall." % " and ".join(sorted({c["chassis"] for c in cabs})),
                           st["small"]))
        return s
    _pdf(root, key, "%s cab package data, tender HAS-F-2026-04" % converter, converter, created, story,
         producer="Microsoft® Excel® for Microsoft 365", footer="%s  tender HAS-F-2026-04  package issue %s" % (short, issue))


def kpi_doc(root):
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.units import mm

    def story():
        st = _styles()
        return [Paragraph("Fleet performance reporting standard", st["h1"]),
                Paragraph("Hallowfen Ambulance Service, Fleet Services. Issue 4, 18 August 2025. Owner: Head of Fleet.",
                          st["small"]), Spacer(1, 4 * mm),
                Paragraph("These definitions apply to every fleet figure reported to the Fleet and Estates Committee and to "
                          "the Board. Figures are reported by financial year (1 April to 31 March) and by financial quarter.",
                          st["body"]),
                _table([["Term", "Definition"],
                        ["Front-line fleet", "The double-crewed ambulances the service operates on emergency work, whatever "
                                             "their conversion or chassis. A vehicle is in the front-line fleet from the date "
                                             "it entered front-line service up to the date it was disposed of, the disposal "
                                             "date not counted."],
                        ["Vehicle-year", "365 days in the front-line fleet."],
                        ["Converter and chassis", "The converter that built the vehicle's conversion and the chassis-cab it is "
                                                  "built on."],
                        ["Miles run", "The distance a vehicle's telematics unit recorded while fitted to the vehicle. A "
                                      "unit is fitted from the date it was fitted up to the date it was removed, that "
                                      "date not counted."],
                        ["Off the road", "A vehicle is off the road from the date it is declared off the road up to the date "
                                         "it returns to service, that date not counted."],
                        ["Seat and cab-structure defect jobs", "Workshop jobs for a defect in a driver or passenger seat, or "
                                                               "in the cab's structure, trim or bulkhead (fleet job codes B12 "
                                                               "and B30)."],
                        ["Job", "A job counts in the quarter in which it was first raised."]],
                       [44 * mm, 122 * mm], st), Spacer(1, 4 * mm),
                Paragraph("Systems", st["h2"]),
                Paragraph("The Vennerley workshop system closed on 30 June 2025. From 1 July 2025 every vehicle's jobs are "
                          "raised in the fleet management system, and the former Vennerley vehicles carry service fleet "
                          "numbers from that date.", st["body"])]
    _pdf(root, "kpi", "Fleet performance reporting standard", "Brenda Ward", "20250818101200", story,
         footer="Fleet Services  performance reporting standard  issue 4")


def standard(root):
    cabs = P.CABS
    blocks = [
        ("Heading1", "Cab fit standard for front-line ambulances"),
        (None, "Fleet Services. Issue 2, approved by the Fleet and Estates Committee on 8 July 2026. Owner: Head of Fleet."),
        ("Heading2", "1. Purpose"),
        (None, "This standard sets how the service decides whether a cab fits its drivers. It applies to the cab specified "
               "for the 2027 front-line ambulance order."),
        ("Heading2", "2. Who must fit"),
        (None, "Every member of staff on the front-line driving roster to be published on 1 October 2026."),
        ("Heading2", "3. When a driver fits a cab"),
        (None, "A driver fits a cab when they can be seated in the driving posture the service's driver posture model "
               "(Ellisand Human Factors, report EHF-2507) predicts for them in that cab, with their eye point in that posture "
               "inside the vision zone in section 4. A driver who does not fit a cab fails it."),
        ("Heading2", "4. Vision zone"),
        (None, "The sight line from the eye point to the lower edge of the windscreen header's clear area rises at least %s "
               "degrees above horizontal, and the sight line from the eye point over the bonnet to the lowest road sight "
               "point falls at least %s degrees below horizontal. The points are those in the converter's package data for "
               "the chassis." % (int(P.VISION["up_deg"]), int(P.VISION["down_deg"]))),
        ("Heading2", "5. Measurements"),
        (None, "A driver's stature, sitting eye height and weight are those recorded in the cab fit measurement programme run "
               "by Occupational Health from March 2025 to September 2026. Where a driver was measured more than once, the "
               "latest measurement stands. Measurements recorded on the former Vennerley paper forms in feet and inches, "
               "and stones and pounds, are converted to millimetres and kilograms."),
        ("Heading2", "6. The 2027 shortlist"),
        (None, "The tender evaluation of 2 June 2026 shortlisted these cabs:"),
        ("TABLE", ([["Converter", "Chassis-cab", "Package data"]] +
                   [[c["converter"], c["chassis"], "Tender HAS-F-2026-04"] for c in cabs], [3600, 2200, 3200])),
        ("Heading2", "7. Decision"),
        (None, "The Committee will specify the shortlisted cab that the fewest drivers fail."),
        ("Heading2", "Document control"),
        ("TABLE", ([["Issue", "Date", "Change"], ["1", "14 March 2025", "First issue, for the measurement programme"],
                    ["2", "8 July 2026", "Shortlist added; vision zone points taken from the package data"]],
                   [1000, 2200, 5800])),
    ]
    O.docx(_p(root, "standard"), blocks, author="Brenda Ward", created="2026-06-12T08:51:00Z",
           modified="2026-07-09T14:37:00Z", revision=7, total_time=214)


def reference_doc(root):
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.units import mm

    def story():
        st = _styles()
        rows = [["Dimension", "Sex", "5th", "50th", "95th"],
                ["Stature (mm)", "Women", "1,522", "1,629", "1,741"], ["", "Men", "1,640", "1,758", "1,874"],
                ["Sitting eye height (mm)", "Women", "709", "762", "818"], ["", "Men", "752", "811", "868"],
                ["Buttock-knee length (mm)", "Women", "541", "586", "634"], ["", "Men", "568", "617", "668"],
                ["Weight (kg)", "Women", "54.1", "71.8", "101.6"], ["", "Men", "64.3", "86.2", "116.0"]]
        return [Paragraph("Working-age adult body dimensions: reference tables", st["h1"]),
                Paragraph("Summary tables from the 2019 Working Population Body Size Survey, adults aged 18 to 64 in "
                          "employment, measured in light clothing without shoes. Third printing, 2021.", st["small"]),
                Spacer(1, 4 * mm), _table(rows, [62 * mm, 24 * mm, 24 * mm, 24 * mm, 24 * mm], st), Spacer(1, 4 * mm),
                Paragraph("Percentiles are estimated from the weighted survey sample of 4,912 adults. Values for "
                          "occupational groups differ from these population values and should be measured where a design "
                          "decision depends on them.", st["body"])]
    _pdf(root, "reference", "Working-age adult body dimensions: reference tables", "Working Population Body Size Survey",
         "20210609160400", story, footer="Working Population Body Size Survey 2019  reference tables")


def prices(root):
    rows = [("Pennick Coachbuild", "FD35", 118450, 46200, 34, 3), ("Pennick Coachbuild", "RD43", 121980, 51700, 38, 3),
            ("Wrenfold Bodies", "FD35", 116300, 46200, 30, 5), ("Wrenfold Bodies", "RD43", 119750, 51700, 33, 5),
            ("Ostrel Vehicle Conversions", "FD35", 114900, 46200, 41, 3)]
    df = pd.DataFrame([(a, b, c, d, c + d, e, f) for a, b, c, d, e, f in rows],
                      columns=["Converter", "Chassis-cab", "Conversion price per vehicle (GBP)", "Chassis-cab price (GBP)",
                               "Total per vehicle (GBP)", "Delivery lead time (weeks)", "Conversion warranty (years)"])
    O.xlsx(_p(root, "prices"), [("Shortlist prices", df)], author="Procurement", created="2026-05-27T13:20:00Z",
           modified="2026-06-02T09:05:00Z", widths={"Shortlist prices": [28, 12, 22, 18, 18, 16, 16]},
           number_formats={"Shortlist prices": {"Conversion price per vehicle (GBP)": "#,##0",
                                                "Chassis-cab price (GBP)": "#,##0", "Total per vehicle (GBP)": "#,##0"}},
           title="Tender HAS-F-2026-04 shortlist prices")


def documents(root):
    standard(root)
    posture_report(root)
    seat_sheet(root)
    by = {}
    for c in P.CABS:
        by.setdefault(c["converter"], []).append(c)
    package(root, "pkg_pennick", "Pennick Coachbuild", by["Pennick Coachbuild"], None, "20260417151900", "B")
    package(root, "pkg_wrenfold", "Wrenfold Bodies", by["Wrenfold Bodies"], P.WRENFOLD_SGRP, "20260422104100", "2")
    package(root, "pkg_ostrel", "Ostrel Vehicle Conversions", by["Ostrel Vehicle Conversions"], None, "20260424085300", "1.1")
    kpi_doc(root)
    reference_doc(root)
    prices(root)


# ----------------------------------------------------------------------------------------------- fleet
def write_fleet(root, W):
    rnd = random.Random(P.SEED + 21)
    V = W["vehicles"]
    fy0, fy1 = P.FY
    cut = P.WORKSHOP_CUTOVER
    status_pick = ["In service"] * 14 + ["Spare"] * 2 + ["Workshop"]
    # register: vehicles in the fleet at the roster date
    reg = []
    for v in V:
        if v["disposed"]:
            continue
        held = cut if v["legacy_no"] else v["in_service"]
        reg.append({"Fleet number": v["fleet_no"], "Former fleet number": v["legacy_no"] or "",
                    "Chassis-cab": v["chassis"], "Converter": v["converter"], "Base hub": HUB_NAME[v["hub"]],
                    "In service": _dt(held), "Telematics unit": v["units"][-1]["unit"],
                    "Status": rnd.choice(status_pick)})
    df = pd.DataFrame(reg).sort_values("Fleet number").reset_index(drop=True)
    O.xlsx(_p(root, "register"), [("Register", df)], author="Fleet Services", created="2026-10-01T06:00:00Z",
           modified="2026-10-01T06:00:00Z", last="Liam Jackson", widths={"Register": [13, 17, 12, 28, 15, 12, 15, 11]},
           title="Front-line fleet register")
    # disposals in the year
    dis = []
    for v in V:
        if not v["disposed"]:
            continue
        before = bool(v["legacy_no"]) and v["disposed"] < cut
        held = v["in_service"] if (before or not v["legacy_no"]) else cut
        dis.append({"Fleet number": v["legacy_no"] if before else v["fleet_no"],
                    "Former fleet number": "" if before else (v["legacy_no"] or ""), "Chassis-cab": v["chassis"],
                    "Converter": v["converter"], "In service": _dt(held), "Disposed": _dt(v["disposed"]),
                    "Reason": rnd.choice(["End of life", "End of life", "End of life", "Accident damage"])})
    df = pd.DataFrame(dis).sort_values("Disposed").reset_index(drop=True)
    O.xlsx(_p(root, "disposals"), [("Disposals", df)], author="Fleet Services", created="2025-05-02T11:31:00Z",
           modified="2026-04-08T10:47:00Z", last="Brenda Ward", widths={"Disposals": [13, 17, 12, 28, 12, 12, 16]},
           title="Vehicle disposals 2025-26")
    # Vennerley asset list at 27 June 2025
    snap = dt.date(2025, 6, 27)
    al = []
    for v in V:
        if v["legacy_no"] and v["in_service"] <= snap and (v["disposed"] is None or v["disposed"] > snap):
            al.append({"Vehicle": v["legacy_no"], "Chassis": v["chassis"], "Conversion": v["converter"].split()[0].upper(),
                       "In service": _dt(v["in_service"]), "Station": HUB_NAME[v["hub"]].upper(), "Status": "ACTIVE"})
    df = pd.DataFrame(al).sort_values("Vehicle").reset_index(drop=True)
    O.xlsx(_p(root, "assets"), [("ASSETS", df)], author="vwfleet", created="2025-06-27T15:58:00Z",
           modified="2025-06-27T15:58:00Z", company="Vennerley Ambulance Service", widths={"ASSETS": [10, 9, 12, 12, 16, 9]},
           title="")
    # telematics units: one row per unit, labelled with the vehicle's fleet number as the provider holds it
    ur = []
    for v in V:
        for i, u in enumerate(v["units"]):
            removed = u["removed"] or (v["disposed"] if i == len(v["units"]) - 1 else None)
            label_legacy = v["legacy_no"] and removed is not None and removed < cut
            ur.append({"Unit ID": u["unit"], "Fleet number": v["legacy_no"] if (label_legacy or v["fleet_no"] is None)
                       else v["fleet_no"], "Fitted": _dt(u["fitted"]), "Removed": _dt(removed) if removed else None,
                       "Odometer entered at fitting (miles)": u.get("entered_show")})
            u["removed_final"] = removed
    df = pd.DataFrame(ur)
    O.xlsx(_p(root, "units"), [("Units", df)], author="Fleet Services", created="2026-10-05T12:12:00Z",
           modified="2026-10-05T12:12:00Z", widths={"Units": [11, 13, 12, 12, 22]}, title="Telematics unit changes",
           number_formats={"Units": {"Odometer entered at fitting (miles)": "#,##0"}})
    return reg, dis, al, ur


def odometer(root, W):
    """daily end-of-day readings per unit; a swapped-out unit kept reporting until it was collected"""
    rnd = random.Random(P.SEED + 31)
    rows = []
    fy0, fy1 = P.FY
    lo, hi = fy0 - D(days=1), fy1
    for v in W["vehicles"]:
        days = sorted(v["miles"])
        cum = {}
        run = v["odo_start"]
        for d in days:
            run += v["miles"][d]
            cum[d] = run
        for i, u in enumerate(v["units"]):
            start = max(u["fitted"], days[0]) if days else u["fitted"]
            stop = u["removed_final"]
            linger = u.get("lingers", 0)
            last = (stop + D(days=linger - 1)) if stop else hi
            if u["fitted"] < fy0:
                base = 0.0
                u["entered_show"] = None
            elif i == 0:
                entered = round(v["odo_start"])
                u["entered_show"] = entered
                base = entered - v["odo_start"]
            else:
                prev = max([d for d in days if d < u["fitted"]], default=None)
                true_odo = cum[prev] if prev else v["odo_start"]
                if rnd.random() < 0.7:
                    entered = round(true_odo)
                else:
                    entered = 0
                u["entered_show"] = entered
                base = entered - true_odo
            for d in days:
                if d < start or d > last or d < lo or d > hi:
                    continue
                edge = d in (lo, hi, start, last) or (stop and d == stop - D(days=1))
                if rnd.random() < 0.012 and not edge:
                    continue
                rows.append((u["unit"], d.isoformat(), "%.1f" % (cum[d] + base)))
    rows.sort(key=lambda r: (r[1], r[0]))
    _csv(_p(root, "odometer"), ["unit_id", "reading_date", "odometer_miles"], rows, crlf=False)
    return len(rows)


def jobs(root, W):
    rnd = random.Random(P.SEED + 41)
    cut = P.WORKSHOP_CUTOVER
    fy0, fy1 = P.FY
    merged, legacy = [], []
    nums = Wd._numbers(rnd, 12000, 100000, 999999)
    lnum = Wd._numbers(rnd, 2500, 1000, 9999)
    ni = li = 0
    for v in W["vehicles"]:
        for j in v["jobs"]:
            if not (fy0 <= j["raised"] <= fy1):
                continue
            south_legacy = v["legacy_no"] and j["raised"] < cut
            if south_legacy:
                open_at_cut = j["done"] >= cut
                legacy.append({"ref": "VJ/25/%04d" % lnum[li], "veh": v["legacy_no"], "in": j["raised"],
                               "out": None if open_at_cut else j["done"], "code": Wd.LEGACY_CODE[j["code"]],
                               "notes": j["desc"].upper(), "off": "Y" if j["vor"] else "N",
                               "status": "TRANSFERRED" if open_at_cut else "CLOSED", "vor_from": j.get("vor_from")})
                li += 1
                if open_at_cut:
                    merged.append({"job": "WO%06d" % nums[ni], "fleet": v["fleet_no"], "raised": cut, "done": j["done"],
                                   "code": j["code"], "desc": j["desc"], "vor": j["vor"],
                                   "from": cut if j["vor"] else None, "to": j.get("vor_to") if j["vor"] else None})
                    ni += 1
                continue
            merged.append({"job": "WO%06d" % nums[ni], "fleet": v["fleet_no"], "raised": j["raised"], "done": j["done"],
                           "code": j["code"], "desc": j["desc"], "vor": j["vor"], "from": j.get("vor_from"),
                           "to": j.get("vor_to")})
            ni += 1
    merged.sort(key=lambda r: (r["raised"], r["job"]))
    _csv(_p(root, "jobs"), ["job_no", "fleet_no", "raised", "completed", "job_code", "description", "off_road",
                            "off_road_from", "back_on_road"],
         [[r["job"], r["fleet"], r["raised"].isoformat(), r["done"].isoformat(), r["code"], r["desc"],
           "Y" if r["vor"] else "N", r["from"].isoformat() if r["from"] else "", r["to"].isoformat() if r["to"] else ""]
          for r in merged], crlf=True)
    legacy.sort(key=lambda r: (r["in"], r["ref"]))
    _csv(_p(root, "legacy_jobs"), ["Job ref", "Vehicle", "Date in", "Date out", "Defect code", "Notes", "Off road", "Status"],
         [[r["ref"], r["veh"], r["in"].strftime("%d/%m/%y"), r["out"].strftime("%d/%m/%y") if r["out"] else "", r["code"],
           r["notes"], r["off"], r["status"]] for r in legacy], crlf=True)
    rows = [(Wd.LEGACY_CODE[c], {"SEAT": "Seats", "CABST": "Cab structure", "BODY": "Body", "ELEC": "Electrical",
                                 "BLUE": "Blue lights and sirens", "BRAKE": "Brakes", "SUSP": "Suspension/steering",
                                 "TYRE": "Tyres", "SERV": "Service", "TEST": "Annual test", "EQPT": "Equipment mounts",
                                 "LIFT": "Tail lift/ramp"}[Wd.LEGACY_CODE[c]], c, Wd.CODES[c]) for c in Wd.CODES]
    df = pd.DataFrame(rows, columns=["Vennerley defect code", "Vennerley description", "Fleet job code", "Fleet job description"])
    O.xlsx(_p(root, "codemap"), [("Code map", df)], author="Liam Jackson", created="2025-06-19T09:44:00Z",
           modified="2025-06-23T16:10:00Z", widths={"Code map": [20, 24, 15, 30]}, title="Vennerley codes to fleet job codes")
    return merged, legacy


def run(root, W):
    write_people(root, W)
    documents(root)
    write_fleet(root, W)
    n_odo = odometer(root, W)
    # the unit changes sheet carries the entered odometer, known only once the readings are drawn
    write_fleet(root, W)
    merged, legacy = jobs(root, W)
    return {"odometer_rows": n_odo, "merged_jobs": len(merged), "legacy_jobs": len(legacy)}
