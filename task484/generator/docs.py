"""The documents and side files: the Council's terms note, the mapping round's scope note, the network
operations log, the expansion factor review, the streetworks permits and the school term dates."""
import datetime as dt
import os

import numpy as np

import common as C
import world as WD


def pdf(path, title, meta, blocks, author):
    C.pdf_invariant()
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors
    st_t = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    st_m = ParagraphStyle("m", fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#444444"), spaceAfter=8)
    st_h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=7, spaceAfter=3)
    st_p = ParagraphStyle("p", fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="Wrenford Borough Council publishing", producer="Wrenford Borough Council publishing")
    story = [Paragraph(title, st_t), Paragraph(meta, st_m)]
    for kind, val in blocks:
        if kind == "h":
            story.append(Paragraph(val, st_h))
        elif kind == "p":
            story.append(Paragraph(val, st_p))
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            story.append(Spacer(1, 5))
    doc.build(story)


def terms_note(out):
    blocks = [
        ("h", "1. Scope"),
        ("p", "This note sets out the terms the Council uses when it publishes traffic estimates for roads in the borough and when "
              "it supplies traffic figures to other bodies. It replaces edition 2024.1."),
        ("h", "2. Count points and sections"),
        ("p", "Each count point in the Council's count point register stands for one section of road: the length of the named road "
              "between the two junctions given in the register as its start and end junctions. A figure given for a count point is a "
              "figure for that whole section."),
        ("h", "3. Motor vehicles"),
        ("p", "Motor vehicles are all vehicles counted except pedal cycles: two-wheeled motor vehicles, cars and taxis, buses and "
              "coaches, light goods vehicles and heavy goods vehicles. Heavy goods vehicles are goods vehicles over 3.5 tonnes gross "
              "vehicle weight, rigid or articulated."),
        ("h", "4. Annual traffic"),
        ("p", "The annual traffic of a section is the number of motor vehicles passing along it, both directions together, on all the "
              "days of the calendar year. The annual average daily flow is the annual traffic divided by the number of days in the "
              "year."),
        ("h", "5. Counting programme, 2025"),
        ("p", "Manual classified counts are taken on one weekday at each section in the year's programme, between March and October, "
              "outside school holidays and bank holidays. Each count covers 07:00 to 19:00 in both directions and is recorded by hour "
              "and direction in the Department for Transport's vehicle classes. The permanent automatic counters record every day of "
              "the year."),
        ("h", "6. Urban and rural"),
        ("p", "Each count point and each permanent counter is recorded as urban or rural in its register. A section is urban when it "
              "lies within the built-up area boundary adopted in the Local Plan."),
        ("h", "7. Presentation"),
        ("p", "Annual traffic is shown in millions of vehicles to one decimal place; daily flows are shown to the nearest ten vehicles "
              "unless a table says otherwise."),
    ]
    pdf(os.path.join(out, "traffic_estimate_terms_2025.pdf"),
        "Traffic estimates: terms and counting programme",
        "Wrenford Borough Council, Transport Data and Monitoring. Edition 2025.2, issued 3 February 2026. Owner: Irene Griffiths, "
        "Head of Transport Data and Monitoring.", blocks, "Irene Griffiths")


def scope_note(out):
    blocks = [
        ("h", "1. Round"),
        ("p", "The 2026 round of strategic noise mapping models road traffic noise in the borough for the calendar year 2025."),
        ("h", "2. Roads mapped"),
        ("p", "Every road section in the borough that carried more than three million vehicle passages in 2025 is mapped. A vehicle "
              "passage is one motor vehicle passing along the section in either direction, so a section's passages in 2025 are its "
              "annual traffic for 2025 as defined in the Council's note on traffic estimate terms (edition 2025.2)."),
        ("h", "3. What the Council supplies"),
        ("p", "For every section it counted in 2025 the Council supplies the count point, the road and the junctions at each end, the "
              "section length, its 2025 annual traffic, and whether it carried more than three million vehicle passages. Sections "
              "the Council did not count in 2025 are taken by the contractor from the national dataset."),
        ("h", "4. Contract"),
        ("p", "The mapping contractor's scope is fixed on the sections over three million vehicle passages. The supply is due to the "
              "contract manager by 31 March 2026, with the sections over the line marked."),
        ("table", [["Item", "Detail"], ["Contract", "WBC/EP/2026/014, strategic noise mapping, roads"],
                   ["Contract manager", "Beth King, Environmental Protection"],
                   ["Traffic supply", "Irene Griffiths, Transport Data and Monitoring"],
                   ["Supply due", "31 March 2026"]]),
    ]
    pdf(os.path.join(out, "noise_mapping_2026_scope.pdf"),
        "Strategic noise mapping, 2026 round: road traffic supply",
        "Wrenford Borough Council, Environmental Protection. Scope note for the mapping contract, issued 26 January 2026.",
        blocks, "Beth King")


def ops_log(W, out):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    doc.add_heading("Transport Data and Monitoring: network operations log, 2025", level=1)
    doc.add_paragraph("Permanent counters (ATC) and urban traffic control (UTC) assets. Entries by the team on the day of the event "
                      "or the day it was reported.")
    rows = []
    atc_name = {a["name"]: W.atc_id[a["name"]] for a in W.atcs}
    rows.append((dt.date(2025, 1, 9), "Network", "Snow from early morning; gritting on priority routes, Grange Road school closed.", "MW"))
    rows.append((dt.date(2025, 1, 10), "Network", "Snow clearing; traffic light until midday.", "MW"))
    lname = W.atc_outage[0]
    rows.append((dt.date(2025, 1, 27), "%s (%s)" % (atc_name[lname], lname),
                 "Outstation not answering polls since 20 January. Site visit found the modem failed; logger memory had wrapped, so "
                 "20 to 25 January could not be recovered. Modem replaced.", "MW"))
    notes = ["Loops tested, commissioned the same day.", "Loops tested; lane 2 feeder re-jointed. Commissioned the same day.",
             "New cabinet base; loops tested and commissioned the same day.", "Commissioned the same day; old outstation returned to stores.",
             "Loops retained and tested. Commissioned the same day.", "Spare duct used for the new feeder; commissioned the same day.",
             "Commissioned after a battery change; first poll 16:00.", "Loops tested. Commissioned the same day, polling confirmed next morning.",
             "Traffic management on site 09:30 to 13:00; commissioned the same day.", "Loop 1 re-cut ahead of the swap; commissioned the same day.",
             "Commissioned the same day; GPRS signal weak, aerial moved."]
    for k, a in enumerate(W.atcs):
        rows.append((a["installed"], "%s (%s)" % (W.atc_id[a["name"]], a["name"]),
                     "TX-200 outstation installed under the counter renewal programme, Ardent LC4 removed. " + notes[k % len(notes)], "MW"))
    rows.append((dt.date(2025, 9, 8), "ATC network", "Firmware 4.2.1 deployed to all TX-200 outstations by remote push (change ref CM-2291).", "MW"))
    names = {j["id"]: j for j in W.junctions}
    for jid, sw in sorted(WD.REFURBISHED.items(), key=lambda x: x[1]):
        j = names[jid]
        rows.append((sw, "WRN%s (%s)" % (W.refs[jid], j["name"]),
                     "Controller replaced under the signal renewal contract. Junction on all-red flashing and police control %s to %s; "
                     "detectors re-terminated to the new controller and recommissioned %s." % (
                         (sw - dt.timedelta(1)).strftime("%d %B").lstrip("0"), (sw + dt.timedelta(1)).strftime("%d %B").lstrip("0"),
                         (sw + dt.timedelta(1)).strftime("%d %B").lstrip("0")), "CD"))
    # longer loop faults on channels away from the counted sections
    for c in W.detectors:
        av = c["avail"]
        if c["section"] is None and c["junction"] not in WD.REFURBISHED:
            z = np.where(av == 0)[0]
            if len(z) >= 9:
                runs, start = [], z[0]
                for k in range(1, len(z) + 1):
                    if k == len(z) or z[k] != z[k - 1] + 1:
                        runs.append((start, z[k - 1]))
                        if k < len(z):
                            start = z[k]
                for a0, a1 in runs:
                    if a1 - a0 >= 8:
                        rows.append((WD.DAYS[a0], "WRN%s channel %d" % (W.refs[c["junction"]], c["channel"]),
                                     "Loop fault reported by the UTC fault monitor; repaired by the maintenance contractor %s." %
                                     WD.DAYS[a1 + 1].strftime("%d %B").lstrip("0") if a1 + 1 < 365 else "repaired in the new year", "CD"))
    rows.append((dt.date(2025, 3, 3), "Count programme", "2025 manual classified count programme starts (Heathside Survey Services).", "MW"))
    rows.append((dt.date(2025, 10, 24), "Count programme", "2025 count programme complete; count sheets received and keyed.", "MW"))
    rows.append((dt.date(2025, 12, 19), "UTC", "Christmas timing plans loaded at the shopping centre and retail park junctions.", "CD"))
    rows.sort(key=lambda r: (r[0], r[1]))
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for i, h in enumerate(["Date", "Asset", "Entry", "By"]):
        hdr[i].text = h
    for d, asset, entry, by in rows:
        cells = t.add_row().cells
        cells[0].text = d.strftime("%d/%m/%Y")
        cells[1].text = asset
        cells[2].text = entry
        cells[3].text = by
    C.save_docx(doc, os.path.join(out, "network_operations_log_2025.docx"), dt.datetime(2026, 1, 9, 16, 40), "Melanie Watts")


def factor_review(W, out):
    """Context artifact: how well each counter group's same-day ratio reproduces a counter's own AADF."""
    import openpyxl
    holidays = set(WD.BANK_HOLIDAYS)
    test_days = [i for i, d in enumerate(WD.DAYS) if dt.date(2025, 3, 1) <= d <= dt.date(2025, 10, 31)
                 and d.weekday() <= 3 and d not in holidays and not WD.in_ranges(d, WD.SCHOOL_HOLIDAYS)]
    res = []
    for setting in ("urban", "rural"):
        grp = [a for a in W.atcs if a["setting"] == setting]
        for a in grp:
            others = [b for b in grp if b is not a]
            own = float(np.nanmean(a["obs24"]))
            errs = []
            for i in test_days:
                if np.isnan(a["obs12"][i]) or any(np.isnan(b["obs12"][i]) for b in others):
                    continue
                f = sum(float(np.nanmean(b["obs24"])) for b in others) / sum(float(b["obs12"][i]) for b in others)
                errs.append(abs(a["obs12"][i] * f / own - 1.0) * 100.0)
            res.append((W.atc_id[a["name"]], a["name"], setting, len(errs), round(float(np.mean(errs)), 1), round(float(np.max(errs)), 1)))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(["Expansion factor group review, 2025"])
    ws.append(["Question", "How closely does a group's same-day ratio of annual traffic to 07:00-19:00 traffic reproduce a permanent "
                           "counter's own annual average daily flow, with the counter itself left out of its group?"])
    ws.append(["Scope", "Permanent counters only; the review does not test count point sections."])
    ws.append(["Version", "2025.1"])
    ws.append(["Refreshed", dt.date(2026, 2, 10)])
    ws.append(["Owner", "Melanie Watts"])
    ws.append([])
    ws.append(["group", "counters", "weekdays tested", "mean absolute error %", "largest error %", "within 10% target"])
    for setting in ("urban", "rural"):
        rr = [r for r in res if r[2] == setting]
        n = sum(r[3] for r in rr)
        mae = sum(r[3] * r[4] for r in rr) / n
        mx = max(r[5] for r in rr)
        ws.append([setting, len(rr), n, round(mae, 1), mx, "yes" if mx < 10 else "no"])
    ws2 = wb.create_sheet("Counters")
    ws2.append(["site_id", "road", "group", "weekdays tested", "mean absolute error %", "largest error %"])
    for r in sorted(res):
        ws2.append(list(r))
    ws["B5"].number_format = "dd/mm/yyyy"
    C.save_workbook(wb, os.path.join(out, "expansion_factor_review_2025.xlsx"), dt.datetime(2026, 2, 10, 11, 15), "Melanie Watts")
    W.factor_review = res


def streetworks(W, out):
    rng = np.random.default_rng([WD.SEED, 131])
    streets = [s["name"] for s in W.sections] + ["Ring Road", "Western Avenue", "Coventry Road", "Birmingham Road", "Market Way",
                                                   "Canal Street", "Lea Road", "Northgate Road", "Ashby Road", "Fenwick Road"]
    promoters = ["Severn Valley Water", "Midland Gas Networks", "Openreach", "Western Power Networks", "Wrenford BC Highways",
                 "Virgin Media O2", "CityFibre"]
    tm = ["give and take", "two-way signals", "lane closure", "footway only", "multi-way signals", "road closure"]
    count_days = {s["name"]: W.count_day[s["name"]] for s in W.sections}
    rows = []
    used = set()
    for k in range(74):
        st = streets[int(rng.integers(0, len(streets)))]
        while True:
            start = WD.DAYS[int(rng.integers(0, 350))]
            dur = int(rng.integers(1, 15))
            end = start + dt.timedelta(dur - 1)
            cd = count_days.get(st)
            if cd is None or not (start - dt.timedelta(2) <= cd <= end + dt.timedelta(2)):
                break
        while True:
            ref = "WR%02d%05d" % (start.month, int(rng.integers(10000, 99999)))
            if ref not in used:
                used.add(ref)
                break
        rows.append([ref, st, promoters[int(rng.integers(0, len(promoters)))], start.isoformat(), end.isoformat(),
                     tm[int(rng.integers(0, len(tm)))]])
    rows.sort(key=lambda r: (r[3], r[0]))
    C.write_csv(os.path.join(out, "streetworks_permits_2025.csv"),
                ["permit_ref", "street", "promoter", "works_start", "works_end", "traffic_management"], rows)


def term_dates(out):
    rows = [["2024-25", "Spring", "2025-01-06", "2025-04-04", "2025-02-17", "2025-02-21"],
            ["2024-25", "Summer", "2025-04-22", "2025-07-22", "2025-05-26", "2025-05-30"],
            ["2025-26", "Autumn", "2025-09-03", "2025-12-19", "2025-10-27", "2025-10-31"]]
    C.write_csv(os.path.join(out, "school_term_dates.csv"),
                ["school_year", "term", "term_starts", "term_ends", "half_term_starts", "half_term_ends"], rows)


def write_docs(W, out):
    terms_note(out)
    scope_note(out)
    ops_log(W, out)
    factor_review(W, out)
    streetworks(W, out)
    term_dates(out)
