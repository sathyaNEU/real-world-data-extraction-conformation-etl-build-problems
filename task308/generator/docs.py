"""task308 documents: the board paper's extract (pdf), the Harbour pilot's operations note (pdf), the fare schedule
(pdf), the data dictionary (xlsx) and the e-bike vendor's quotation (pdf, a distractor)."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P

F = P.FILES


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.4, leading=17, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=14,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(letter[0] - 18 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.2):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E4EAF0")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _pdf(path, title, subject, story, foot, author):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=P.ORG, subject=subject,
                            invariant=1)
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))


def board(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("%s | Board of Directors | 9 December 2026" % P.ORG, small),
         Paragraph("Item 7. The 2027 e-bike deployment (extract)", h1),
         Paragraph("Paper by %s, e-bike product lead, with %s, director of operations. For decision." %
                   (P.PEOPLE["lead"], P.PEOPLE["ops"]), small), Spacer(1, 4),
         Paragraph("1. What the board is asked to decide", h2),
         Paragraph("The 2027 capital plan includes %d e-bikes. They go to one of our five classic networks, Central, "
                   "University, Riverside, Old Town or Hillcrest, for the 2027 season. The board is asked to choose the "
                   "network and to note what the e-bikes are expected to add there. Harbour keeps the e-bikes of the "
                   "2025 pilot and is not a candidate." % P.DEPLOY_EBIKES, body),
         Paragraph("2. The measure", h2),
         Paragraph("Each network is judged on the net fare revenue the e-bikes would add there in a year: the fares "
                   "riders would pay in that network in a year with the e-bikes, less the fares they paid in that "
                   "network in 2025, at 2025 demand. Rides on e-bikes pay the e-bike fare and rides on classic bikes the "
                   "classic fare, as in the 2025 fare schedule. Annual pass fees are not fares and are left out.", body),
         Paragraph("3. How the e-bikes would run", h2),
         Paragraph("As on the Harbour pilot (%s): every station in the chosen network gets charging points, with extra "
                   "dock points where a station is short of room, and the e-bikes are spread over its stations and "
                   "moved with the classic fleet on the van runs and at the night restock, so that every station holds "
                   "e-bikes through the day. The classic fleet and its allocation stay as they are. An e-bike can only "
                   "be returned to a station in its own network." % F["pilot"], body),
         Paragraph("4. Timing", h2),
         Paragraph("The order has to be placed by 15 January 2027 for delivery in March, ahead of the season opening "
                   "on 1 April 2027. The vendor's quotation is on file (%s)." % F["quote"], body),
         Paragraph("5. Records behind the paper", h2),
         Paragraph("The 2025 trip exports (the old trip system to 30 June, the new platform from 1 July), the dispatch "
                   "log, the 03:00 audit, the station feeds, the account register, the Harbour charging sessions and "
                   "the workshop jobs. Field descriptions are in %s." % F["dictionary"], body)]
    _pdf(path, "Board item 7: 2027 e-bike deployment", "Board paper extract", s,
         "%s | Board 9 December 2026 | item 7 (extract)" % P.ORG_SHORT, P.PEOPLE["lead"])


def pilot(path, st):
    body, h1, h2, small = _styles()
    rows = [["Station", "Name", "In the pilot as"]]
    for x in sorted((x for x in st if x["programme"]), key=lambda x: x["code"]):
        rows.append([x["code"], x["name"], "pilot station" if x["programme"] == "e-bike pilot" else "comparison station"])
    s = [Paragraph("%s | Operations" % P.ORG, small),
         Paragraph("E-bike pilot on the Harbour network, January to December 2025", h1),
         Paragraph("%s, director of operations. Issued 20 January 2025; station table checked 3 November 2026." %
                   P.PEOPLE["ops"], small), Spacer(1, 4),
         Paragraph("What ran", h2),
         Paragraph("From 1 January to 31 December 2025, %d of the 36 Harbour stations had %d charging points each and "
                   "held %d e-bikes after the e-bike crew's night restock. The restock moves e-bikes between the pilot "
                   "stations and the depot, and the crew swaps out any e-bike flagged with a fault for a charged spare. "
                   "The other %d Harbour stations were the comparison stations: on the same streets, matched to the "
                   "pilot stations on capacity and on 2024 trips a day, within 5 per cent, and kept to classic bikes."
                   % (P.PILOT_N, P.POINTS, P.EB_PILOT, P.MATCHED_N), body),
         Paragraph("At a pilot station a rider can take either kind of bike; the app shows each e-bike's charge. An "
                   "e-bike can only be returned to a pilot station, where it charges on a charging point if one is free "
                   "and sits on an ordinary dock point, without charging, if not. Classic bikes ran as everywhere "
                   "else: the 02:30 night run, the 06:00 and 14:00 van runs.", body),
         Paragraph("Fares", h2),
         Paragraph("USD 1.00 to unlock and USD 0.17 a started minute on an e-bike, against USD 0.12 on a classic bike "
                   "(%s)." % F["fares"], body),
         Paragraph("Records", h2),
         Paragraph("E-bike rides are in the trip exports with every other ride. Each charging point meters what it "
                   "delivers, and the station controllers' sessions are in %s. The pilot's e-bikes stay at Harbour in "
                   "2026 and 2027." % F["charging"], body),
         Spacer(1, 4), _table(rows, [24, 92, 40])]
    _pdf(path, "E-bike pilot, Harbour, 2025", "Operations note", s,
         "%s | Operations | Harbour e-bike pilot 2025" % P.ORG_SHORT, P.PEOPLE["ops"])


def fares(path):
    body, h1, h2, small = _styles()
    rows = [["", "Classic bike", "E-bike (Harbour pilot)"],
            ["Unlock, every ride", "USD 1.00", "USD 1.00"],
            ["Each started minute", "USD 0.12", "USD 0.17"]]
    s = [Paragraph("%s" % P.ORG, small), Paragraph("Fares, in force from 1 March 2024", h1), Spacer(1, 3),
         _table(rows, [60, 50, 50], 9), Spacer(1, 6),
         Paragraph("A ride is charged to the card on the account when the bike is docked. Minutes are counted from "
                   "undocking to docking, and a part minute counts as a minute.", body),
         Paragraph("A bike undocked and docked again at the same station within 60 seconds is not charged.", body),
         Paragraph("Annual pass: USD 20 a year. Pass holders pay the same ride fares; the pass gives monthly "
                   "statements, ride history and priority support.", body),
         Paragraph("Fares are reviewed each winter; there was no change for 2025.", small)]
    _pdf(path, "Fares", "Fare schedule", s, "%s | Fares from 1 March 2024" % P.ORG_SHORT, "Customer Services")


def quote(path):
    body, h1, h2, small = _styles()
    rows = [["Item", "Qty", "Unit price, USD", "Lead time"],
            ["Shared e-bike HV-S2, 500 Wh battery, dock-lock kit", "300", "2,385.00", "9 weeks from order"],
            ["Dock-integrated charging point, 250 W, installed", "per point", "1,140.00", "6 weeks"],
            ["Spare battery 500 Wh", "per unit", "410.00", "3 weeks"],
            ["Station controller (up to 16 points)", "per station", "2,960.00", "6 weeks"]]
    s = [Paragraph(P.VENDOR, small), Paragraph("Quotation HVS-Q-26-0418", h1),
         Paragraph("To %s, attn. %s. 2 October 2026. Valid until 31 January 2027." % (P.ORG, P.PEOPLE["lead"]), small),
         Spacer(1, 4), _table(rows, [80, 20, 32, 40], 8.6), Spacer(1, 6),
         Paragraph("Prices exclude sales tax and freight. Warranty: two years on frame and motor, one year on battery. "
                   "Payment 30 per cent with order, balance on delivery. Charging points are installed by our "
                   "contractor on the operator's existing stations; station power upgrades are quoted separately "
                   "after a site survey.", body)]
    _pdf(path, "Quotation HVS-Q-26-0418", "Quotation", s, "%s | Quotation HVS-Q-26-0418" % P.VENDOR, P.VENDOR)


DICT = {
    "Read me": [
        ("Times", "The trip exports carry the trip system's local time (Central Time, America/Chicago) without an "
                  "offset. The dispatch log, the charging sessions and the workshop jobs are in UTC. The audit is taken "
                  "at 03:00 local time. Our reporting days, months and quarters run on Central Time."),
        ("Trip platform", "On 1 July 2025 trips moved from the old trip system to the new platform. The exports for "
                          "January to June come from the old system (%s, %s) and those for July to December from the "
                          "new platform (%s, %s). Ride ids, station identifiers, vehicle ids, account ids and fare "
                          "units differ; see each sheet. The account register carries both account ids."
                          % (F["q1"], F["q2"], F["q3"], F["q4"])),
        ("False starts", "A record of under 60 seconds that ends at the station it started from is a false start: "
                         "the rider put the bike straight back. It is in the trip exports but is not a ride and is not "
                         "charged."),
        ("Stations", "%s and %s are the public GBFS feeds as at 1 November 2026. station_id is the station's asset "
                     "number, used by the dispatch log and the audit; short_name is the station code, used by the new "
                     "platform and the charging sessions; name is used by the old trip system." % (F["stations"], F["regions"])),
        ("Vehicles", "A bike keeps its number across systems: B-00123 on the old trip system, 100123 on the new "
                     "platform and BK00123 in the workshop; e-bikes E-0045, 500045 and EB0045."),
    ],
    F["q1"]: [("trip_id", "Old trip system ride id."), ("start_time", "Undocked, local time."),
              ("end_time", "Docked, local time."), ("start_station", "Station name."), ("end_station", "Station name."),
              ("bike_no", "Bike number."), ("bike_type", "classic or electric."),
              ("account_no", "Old trip system account number (legacy_account_no in the account register)."),
              ("member_type", "Member (annual pass) or Casual."), ("duration_sec", "Seconds from undock to dock."),
              ("fare_usd", "Fare charged, USD.")],
    F["q3"]: [("ride_id", "New platform ride id."), ("started_at", "Undocked, local time."),
              ("ended_at", "Docked, local time."), ("start_station_code", "Station code."),
              ("end_station_code", "Station code."), ("vehicle_id", "Vehicle id."), ("vehicle_type", "CLASSIC or EBIKE."),
              ("account_id", "Account id."), ("plan", "annual or payg."), ("duration_s", "Seconds from undock to dock."),
              ("fare_cents", "Fare charged, US cents.")],
    F["moves"]: [("move_id", "Dispatch task."), ("completed_utc", "When the bikes were dropped, UTC."),
                 ("from_station", "Asset number, or DEPOT."), ("to_station", "Asset number, or DEPOT."),
                 ("qty", "Bikes moved."), ("bike_class", "classic or e-bike."), ("van", "Van or crew.")],
    F["audit"]: [("audit_date", "Date of the 03:00 count."), ("station_id", "Asset number."),
                 ("classic_docked", "Classic bikes docked at 03:00."), ("ebikes_docked", "E-bikes docked at 03:00.")],
    F["accounts"]: [("account_id", "Account id (new platform)."),
                    ("legacy_account_no", "Old trip system account number; blank for accounts opened after the switch."),
                    ("created_at", "Account opened, local time."), ("plan", "annual or payg at the extract date."),
                    ("home_area", "Where the rider lives, as given at sign-up."),
                    ("card_fingerprint", "Token of the payment card on the account (not the card number)."),
                    ("status", "active or closed at the extract date."), ("closed_at", "When closed, local time.")],
    F["charging"]: [("session_id", "Controller session, numbered as received."), ("station_code", "Station code."),
                    ("point", "Charging point, 1 to %d." % P.POINTS), ("vehicle_tag", "E-bike tag."),
                    ("plug_in_utc", "UTC."), ("plug_out_utc", "UTC."),
                    ("meter_start_wh", "The point's energy register at plug-in, Wh."),
                    ("meter_stop_wh", "The point's energy register at plug-out, Wh."),
                    ("energy_kwh", "Energy the point delivered over the session. A session counts in the local day "
                                   "its plug-out falls.")],
    F["workshop"]: [("job_no", "Job card."), ("asset_tag", "Bike tag."), ("asset_class", "Classic or E-bike."),
                    ("opened_utc", "Job opened when the bike reached the workshop, UTC."),
                    ("closed_utc", "Job closed when the mechanic signed it off, UTC."), ("fault_code", "Fault code."),
                    ("fault", "Fault."), ("outcome", "Returned to service or Scrapped."), ("bay", "Bench."),
                    ("technician", "Initials.")],
    F["opendata"]: [("area", "Service area."), ("month", "Month."),
                    ("trips", "Trips starting in the area, as published by the City; counts under 10,000 are "
                              "published as suppressed.")],
}


def dictionary(path):
    wb = Workbook()
    for i, (sheet, rows) in enumerate(DICT.items()):
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = sheet[:31] if sheet == "Read me" else sheet.rsplit(".", 1)[0][:31]
        if sheet != "Read me":
            ws.append(["File", sheet])
            ws["A1"].font = Font(bold=True)
        ws.append(["Field" if sheet != "Read me" else "Topic", "Description"])
        r = ws.max_row
        for c in ws[r]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DCE4EC")
        for a, b in rows:
            ws.append([a, b])
        ws.column_dimensions["A"].width = 22
        ws.column_dimensions["B"].width = 100
        for row in ws.iter_rows(min_row=1):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.properties.creator = "Data team"
    wb.properties.lastModifiedBy = "Data team"
    wb.save(path)
