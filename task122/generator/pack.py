"""Cut the pack: the FDPS crossing list, the STCA log, the planner workstation log, the configuration log, the
acceptance criteria, the planner guide, the safety performance report, the request, and the context files."""
import csv
import datetime as dt
import io
import os
import re
import zipfile
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np
import openpyxl
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import world as W

FILES = {
    "crossings": "fdps_sector_crossings_2026-04_2026-09.csv",
    "stca": "stca_activations_2026-04_2026-09.csv",
    "probe": "probe_m_planner_workstation_log_2026-04_2026-09.csv",
    "config": "sector_configuration_log_2026-04_2026-09.csv",
    "criteria": "probe_m_trial_acceptance_criteria.pdf",
    "guide": "probe_m_planner_guide_v2.1.pdf",
    "report": "safety_performance_report_2024-25.pdf",
    "request": "probe_m_decision_paper_request.eml",
    "sigmet": "sigmets_nzzc_2026-04_2026-09.csv",
    "forecast": "traffic_forecast_2027.xlsx",
    "training": "probe_m_training_plan_2027.xlsx",
}
DISTRACTORS = ["sigmet", "forecast", "training"]
WS = {"KPA": "WS-11", "HKI": "WS-12", "WKO": "WS-21", "TKI": "WS-22", "TPO": "WS-31", "KPT": "WS-32"}


def utc_s(sec):
    return (P.T0 + dt.timedelta(seconds=int(sec))).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_s(sec):
    return (P.T0 + dt.timedelta(seconds=int(sec))).astimezone(P.NZ).strftime("%Y-%m-%d %H:%M:%S")


def opname(sec_name, comb):
    if not comb:
        return sec_name
    for a, b in P.PAIRS:
        if sec_name in (a, b):
            return "%s/%s" % (a, b)
    return sec_name


def _csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def _xlsx(path, sheets, creator, created, modified, app="Microsoft Excel", widths=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for i in bold:
            for c in ws[i]:
                c.font = Font(bold=True)
        for col, width in zip("ABCDEFGHIJKLMN", widths or (16, 16, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14)):
            ws.column_dimensions[col].width = width
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    wb.properties.title = None
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                              b"\\g<1>" + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                        b'<Application>' + app.encode() + b'</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.4, leading=12.8, alignment=TA_LEFT, spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3),
            "s": ParagraphStyle("s", parent=base, fontSize=8.2, leading=10.6, textColor=colors.HexColor("#4f5b66")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.2, leading=13.6, spaceBefore=7),
            "p": base,
            "cell": ParagraphStyle("c", parent=base, fontSize=7.9, leading=9.6, spaceAfter=0),
            "cellb": ParagraphStyle("cb", parent=base, fontName="Helvetica-Bold", fontSize=7.9, leading=9.6, spaceAfter=0)}


def pdf(path, blocks, title, author, created, modified, footer, first_col=0.30):
    """Each table cell is a wrapped paragraph; each document carries its own creation and modification stamps."""
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(colors.HexColor("#5b6670"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=17 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "table":
            width = A4[0] - 38 * mm
            n = len(val[0])
            widths = [width * first_col] + [width * (1 - first_col) / (n - 1)] * (n - 1) if n > 1 else [width]
            rows = [[Paragraph(str(c).replace("&", "&amp;"), st["cellb" if i == 0 else "cell"]) for c in r]
                    for i, r in enumerate(val)]
            t = Table(rows, colWidths=widths, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                                   ("TOPPADDING", (0, 0), (-1, -1), 1.5)]))
            story += [t, Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)


# ------------------------------------------------------------------------------------------------- records

def crossing_rows(Wd):
    """The FDPS crossing list: every revision's crossings; each revision re-issues the flight's whole list."""
    r = W.rng("crossings-out")
    rows = []
    for f in Wd["flights"]:
        revs = f["revisions"] + [("flown", f["cross"])]
        first_entry = min(c[1] for c in f["cross"])
        issue = first_entry - int(r.integers(80, 200)) * 60
        for k, (kind, cross) in enumerate(revs, start=1):
            if k > 1:
                issue = min(c[1] for c in revs[k - 1][1]) - int(r.integers(5, 60)) * 60
                issue = min(issue, min(c[1] for c in cross) - 300)
            for sec, a, b, fin, fout, ph in cross:
                if a < 0 or a >= P.MINUTES * 60:
                    continue
                rows.append((a, f["ifps"], f["callsign"], f["adep"], f["ades"], f["type"], sec, utc_s(a), utc_s(b),
                             fin, fout, k, utc_s(issue)))
    rows.sort(key=lambda x: (x[0], x[1], x[11], x[6]))
    return [x[1:] for x in rows]


def stca_rows(Wd):
    """The STCA log: every live activation, the record the system opens when an alert carries into the next sector,
    activations inside the approach inhibition volumes, and the nightly test activations."""
    r = W.rng("stca-out")
    fl = Wd["flights"]
    comb = Wd["comb"]
    recs = []
    for a in Wd["acts"]:
        fa, ca = a["a"]
        fb, cb = a["b"]
        A, B = fl[fa], fl[fb]
        sec = a["sector"]
        t = a["t"]
        end = t + a["dur"]
        cont = None
        exit_a = A["cross"][ca][2]
        if ca + 1 < len(A["cross"]) and t <= exit_a <= t + 90 and r.random() < 0.9:
            nxt = A["cross"][ca + 1][0]
            if nxt != sec:
                end = exit_a
                cs = exit_a + int(r.integers(0, 3))
                cont = (nxt, cs, cs + int(r.integers(5, 41)))
        status = "INHIBITED" if a["inhibited"] else "LIVE"
        m = int(t // 60)
        recs.append([t, opname(sec, bool(comb[min(m, P.MINUTES - 1)])), t, max(end, t + 4), A["callsign"], B["callsign"],
                     a["hsep"], a["vsep"], status])
        if cont:
            nxt, cs, ce = cont
            mm = min(int(cs // 60), P.MINUTES - 1)
            c1, c2 = (A["callsign"], B["callsign"]) if r.random() < 0.5 else (B["callsign"], A["callsign"])
            recs.append([cs, opname(nxt, bool(comb[mm])), cs, ce, c1, c2, round(a["hsep"] + float(r.uniform(-0.3, 0.3)), 1),
                         a["vsep"], status])
    # nightly system test activations in each combined sector (about 03:10 New Zealand time)
    for k, (m0, dd) in enumerate(Wd["frame"]["edges"][:-1]):
        for (x, y) in P.PAIRS:
            t = (m0 + 3 * 60 + 10) * 60 + int(r.integers(0, 600))
            if 0 <= t < P.MINUTES * 60 and comb[min(int(t // 60), P.MINUTES - 1)]:
                recs.append([t, "%s/%s" % (x, y), t, t + 20, "TST01", "TST02", 1.0, 0, "TEST"])
    recs.sort(key=lambda x: (x[0], x[1]))
    out = []
    seq = {}
    for rec in recs:
        mon = (P.T0 + dt.timedelta(seconds=rec[2])).astimezone(P.NZ).strftime("%y%m")
        seq[mon] = seq.get(mon, 0) + 1
        out.append(("STCA-%s-%05d" % (mon, seq[mon]), rec[1], utc_s(rec[2]), utc_s(rec[3]), rec[4], rec[5],
                    "%.1f" % rec[6], rec[7], rec[8]))
    return out


def probe_rows(Wd):
    r = W.rng("probe-out")
    rows = []
    for pos, a, b in Wd["sessions"]:
        sa = a * 60
        sb = b * 60
        sec = "/".join(pos)
        ws = WS[pos[0]]
        rows.append((sa, ws, "PLN", sec, local_s(sa)[:16], local_s(sb)[:16]))
    rows.sort()
    return [x[1:] for x in rows]


def config_rows(Wd):
    r = W.rng("config-out")
    out = []
    for m, kind in Wd["changes"]:
        t = m * 60
        if kind == "NIGHT":
            out.append((local_s(t)[:16], "NIGHT-3", "KPA/HKI WKO/TKI TPO/KPT"))
        else:
            out.append((local_s(t)[:16], "DAY-6", "KPA HKI WKO TKI TPO KPT"))
    return out


def sigmet_rows():
    r = W.rng("sigmet")
    areas = ["NZZC FIR N OF S3800", "NZZC FIR W OF E17430", "NZZC FIR S OF S4000", "NZZC FIR E OF E17600",
             "NZZC FIR N OF S3730 W OF E17500", "NZZC FIR S OF S3830 E OF E17530"]
    phen = ["EMBD TS", "SEV TURB", "SEV ICE", "SEV MTW", "OBSC TS"]
    rows = []
    t = 0
    k = 0
    while True:
        t += int(r.exponential(26 * 3600))
        if t >= P.MINUTES * 60:
            break
        k += 1
        dur = int(r.choice([4, 4, 6, 6, 8])) * 3600
        lo = int(r.choice([100, 150, 180, 200, 250]))
        hi = lo + int(r.choice([100, 150, 200, 240]))
        rows.append(("NZZC %s %02d" % ("SIGMET", k % 99 + 1), utc_s(t), utc_s(t + dur), str(r.choice(phen)),
                     str(r.choice(areas)), "FL%03d/%03d" % (lo, min(hi, 450)), str(r.choice(["MOV E 15KT", "STNR",
                                                                                          "MOV NE 20KT", "MOV SE 10KT"]))))
    return rows


# ------------------------------------------------------------------------------------------------- documents

def criteria_pdf(path):
    b = [("t", "PROBE-M operational trial: acceptance criteria"),
         ("s", "Safety Review Board paper SRB 2026/04, version 1.0, approved 17 March 2026. Tasman Air Navigation, "
               "Area Control Centre."),
         ("h", "1 Purpose"),
         ("p", "This paper sets the criterion on which the executive team will decide whether PROBE-M becomes "
               "mandatory at every en-route planner position from 1 April 2027."),
         ("h", "2 The trial"),
         ("p", "PROBE-M is available at the planner positions of the six en-route sectors, KAIPARA (KPA), HAURAKI "
               "(HKI), WAIKATO (WKO), TARANAKI (TKI), TAUPO (TPO) and KAPITI (KPT), from 1 April to 30 September "
               "2026, New Zealand time, in every sector configuration. Planners use it at their own discretion. "
               "Procedures, sectorisation and staffing do not change for the trial."),
         ("h", "3 Criterion"),
         ("p", "3.1 PROBE-M becomes mandatory if, over the trial, its use prevented at least one in five (20 per "
               "cent) of the STCA activations the trial sectors would have raised in the time it was running."),
         ("p", "3.2 Activations are counted as the Safety Performance Report counts them."),
         ("p", "3.3 The time it was running is the time the probe display was on at the sector's planner position, "
               "as the planner workstation records it. In a combined configuration the combined position's display "
               "covers both sectors."),
         ("h", "4 Also before the Board"),
         ("p", "The planners' feedback survey and the training plan inform how a mandate would be introduced. They "
               "are not part of the decision."),
         ("h", "5 Decision"),
         ("p", "The executive team decides at its November 2026 meeting on the human factors lead's paper. The Board "
               "will be told the outcome."),
         ("h", "Document control"),
         ("table", [["Version", "Date", "Change", "By"],
                    ["0.1", "24 February 2026", "Draft for the Board", "Tessa Freeman"],
                    ["0.2", "6 March 2026", "Combined configurations added to 3.3", "Tessa Freeman"],
                    ["1.0", "17 March 2026", "Approved", "Safety Review Board"]])]
    pdf(path, b, "PROBE-M operational trial: acceptance criteria", "Tasman Air Navigation", "D:20260224093112+13'00'",
        "D:20260317161548+13'00'", "SRB 2026/04 v1.0  |  Tasman Air Navigation  |  Uncontrolled when printed",
        first_col=0.14)


def guide_pdf(path):
    b = [("t", "PROBE-M Medium-Term Conflict Probe: planner guide"),
         ("s", "Version 2.1, March 2026. Area Control Centre operations. For the operational trial from 1 April 2026."),
         ("h", "1 What PROBE-M does"),
         ("p", "PROBE-M predicts conflicts between the aircraft in the sector and those about to enter it, up to twenty "
               "minutes ahead, from the system trajectories. It lists each predicted conflict at the planner position "
               "with the pair, the time to closest approach and the predicted separation. The planner can also enter "
               "a trajectory change (a level, a route or a speed) and see it tested against the other traffic before "
               "the clearance is issued."),
         ("p", "PROBE-M is advisory. It does not replace the short-term conflict alert (STCA), which stays the safety "
               "net for the executive controller."),
         ("h", "2 Using it during the trial"),
         ("p", "Switch the display on and off from the planner workstation's tool bar. Use it at your discretion; there "
               "is no requirement to have it on, and the executive controller's working method does not change."),
         ("h", "3 Combined configurations"),
         ("p", "When sectors are combined, the combined planner position runs one probe display for the whole combined "
               "sector."),
         ("h", "4 Records"),
         ("p", "The planner workstation logs each time the probe display is switched on and off, with the workstation, "
               "the position and the operational sector in force at the time, in New Zealand time."),
         ("h", "5 Known limitations"),
         ("table", [["Item", "Note"],
                    ["Trajectory source", "FDPS system trajectories; a flight plan revision updates the prediction within 30 seconds"],
                    ["Military areas", "Activated restricted areas are shown but not probed"],
                    ["Display", "The conflict list is limited to the 12 nearest predicted conflicts"]])]
    pdf(path, b, "PROBE-M planner guide", "ACC Operations", "D:20260302141907+13'00'", "D:20260326102233+13'00'",
        "PROBE-M planner guide v2.1  |  ACC Operations", first_col=0.25)


def report_pdf(path, rep):
    b = [("t", "Safety Performance Report 2024/25"),
         ("s", "Tasman Air Navigation. Year to 30 June 2025. Published 21 October 2025."),
         ("h", "1 About this report"),
         ("p", "The report sets out the safety indicators the provider monitors for its en-route and approach "
               "services. This extract covers the en-route sectors' traffic and short-term conflict alert (STCA) "
               "activity."),
         ("h", "2 Definitions"),
         ("p", "<b>Flight hours.</b> The time each flight spends in a sector, from sector entry to sector exit as the "
               "flight data processing system (FDPS) records it, counted in the month in which it is flown."),
         ("p", "<b>Flights handled.</b> Each flight is counted once in each sector it enters, however many times it "
               "enters it."),
         ("p", "<b>STCA activations.</b> An activation is one alert for one pair of aircraft, from the time the alert "
               "starts until it ends. Where the alert continues as one of the aircraft passes into the next sector, "
               "the system opens a record in that sector; the activation is counted once, in the sector where it "
               "began. In a combined configuration it is counted in the elementary sector that held the first-named "
               "aircraft when the alert began. Inhibited and test activations are not counted."),
         ("p", "<b>Rates.</b> Activations per 1,000 flight hours, by sector. STCA is tuned sector by sector, so "
               "rates are compared within a sector, not across sectors."),
         ("p", "<b>Months.</b> New Zealand calendar months."),
         ("h", "3 En-route traffic"),
         ("table", [["Sector"] + rep["months"][:6]] +
                   [[s] + ["{:,}".format(v) for v in rep["fh"][s][:6]] for s in P.SECTORS]),
         ("table", [["Sector"] + rep["months"][6:]] +
                   [[s] + ["{:,}".format(v) for v in rep["fh"][s][6:]] for s in P.SECTORS]),
         ("s", "Flight hours by sector and month."),
         ("h", "4 STCA activity"),
         ("table", [["Sector"] + rep["months"][:6]] +
                   [[s] + ["%.1f" % v for v in rep["rate"][s][:6]] for s in P.SECTORS]),
         ("table", [["Sector"] + rep["months"][6:]] +
                   [[s] + ["%.1f" % v for v in rep["rate"][s][6:]] for s in P.SECTORS]),
         ("s", "STCA activations per 1,000 flight hours by sector and month."),
         ("table", [["Sector", "Flights handled", "Flight hours", "Activations", "Per 1,000 flight hours"]] +
                   [[s, "{:,}".format(rep["flights"][s]), "{:,}".format(sum(rep["fh"][s])), "{:,}".format(rep["acts"][s]),
                     "%.1f" % rep["year_rate"][s]] for s in P.SECTORS]),
         ("s", "Year to 30 June 2025."),
         ("h", "5 Commentary"),
         ("p", "Activation rates were steady across the year and no sector's rate moved outside its control band. "
               "Losses of separation are reported separately to the regulator.")]
    pdf(path, b, "Safety Performance Report 2024/25", "Tasman Air Navigation", "D:20251008112030+13'00'",
        "D:20251020171455+13'00'", "Safety Performance Report 2024/25  |  Tasman Air Navigation", first_col=0.12)


def request_eml(path):
    m = EmailMessage()
    m["From"] = "Tessa Freeman <tessa.freeman@tasmanair.example.nz>"
    m["To"] = "Kieran McMurray <kieran.mcmurray@tasmanair.example.nz>"
    m["Cc"] = "Neil Hoskins <neil.hoskins@tasmanair.example.nz>"
    m["Subject"] = "PROBE-M trial: paper for the executive team"
    m["Date"] = format_datetime(dt.datetime(2026, 10, 9, 8, 47, tzinfo=dt.timezone(dt.timedelta(hours=13))))
    m["Message-ID"] = "<20261009084712.4f1c@tasmanair.example.nz>"
    m.set_content(
        "Kieran,\n\n"
        "The trial closed on 30 September and the executive team takes the PROBE-M decision at its November "
        "meeting, so I need the paper by the end of the month. Please write it against the acceptance criteria "
        "(SRB 2026/04, attached): the call, and the figure it rests on.\n\n"
        "For the safety performance pack I also need the trial tables in the report's format: each sector's "
        "flight hours and STCA activations per 1,000 flight hours by month, and the flights each sector handled "
        "over the trial.\n\n"
        "The extracts are attached: the FDPS crossing list, the STCA log, the planner workstation log and the "
        "configuration log for April to September, with last year's report for the definitions. Neil has the "
        "planners' survey if you want it, and the training plan is in the folder.\n\n"
        "Thanks,\nTessa\n\n"
        "Tessa Freeman\nHuman Factors Lead, Area Control Centre\nTasman Air Navigation\n")
    with open(path, "wb") as f:
        f.write(bytes(m))


def forecast_xlsx(path, Wd):
    r = W.rng("forecast")
    base = {s: int(sum(1 for f in Wd["flights"] for c in f["cross"] if c[0] == s) / 6) for s in P.SECTORS}
    rows = [("Tasman Air Navigation: en-route traffic forecast 2027 (flights handled)",), (),
            ("Sector",) + tuple("%s 2027" % mn for mn in ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                                                        "Sep", "Oct", "Nov", "Dec")) + ("Growth on 2026",)]
    seas = [1.10, 1.06, 1.04, 1.00, 0.97, 0.95, 1.04, 0.99, 1.02, 1.05, 1.07, 1.12]
    for s in P.SECTORS:
        g = float(r.uniform(0.025, 0.048))
        rows.append((s,) + tuple(int(round(base[s] * (1 + g) * k / 10.0) * 10) for k in seas) + ("%.1f%%" % (100 * g),))
    rows += [(), ("Base: FDPS flights handled April to September 2026; growth from the airline schedules filed for 2027.",)]
    _xlsx(path, [("Forecast", rows, [3])], "Planning and Performance", dt.datetime(2026, 9, 14, 1, 12, 0),
          dt.datetime(2026, 9, 22, 4, 40, 0), widths=(12, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 14))


def training_xlsx(path):
    rows = [("PROBE-M mandatory use: training plan and cost estimate (if mandated)",), (),
            ("Item", "Detail", "Planners", "Hours each", "Rate (NZD/h)", "Cost (NZD)")]
    lines = [("Classroom module", "Probe principles and working method", 64, 4, 145),
             ("Simulator sessions", "Two two-hour sessions per planner", 64, 4, 210),
             ("Instructor time", "Two instructors, 16 days", 2, 128, 165),
             ("Backfill overtime", "Roster cover for planners in training", 64, 8, 118),
             ("Assessment", "Competency check at the position", 64, 1, 210)]
    tot = 0
    for it, de, n, h, rate in lines:
        c = n * h * rate
        tot += c
        rows.append((it, de, n, h, rate, c))
    rows += [("Total", "", "", "", "", tot), (), ("Schedule: January to March 2027, before a 1 April 2027 start.",)]
    _xlsx(path, [("Training", rows, [3])], "ACC Training", dt.datetime(2026, 9, 2, 22, 5, 0),
          dt.datetime(2026, 9, 29, 3, 18, 0), widths=(22, 38, 10, 11, 12, 12))


def report_figures(Wd):
    """The 2024/25 year's published figures: traffic a little below the trial's, rates at the sectors' probe-free
    levels, the published series only."""
    r = W.rng("report")
    months = ["July 2024", "August 2024", "September 2024", "October 2024", "November 2024", "December 2024",
              "January 2025", "February 2025", "March 2025", "April 2025", "May 2025", "June 2025"]
    seas = [1.04, 0.99, 1.01, 1.04, 1.06, 1.12, 1.10, 1.05, 1.03, 1.00, 0.96, 0.94]
    fh = {}
    rate = {}
    acts = {}
    flights = {}
    yr = {}
    n = Wd["n"]
    on = Wd["on"]
    for i, s in enumerate(P.SECTORS):
        mfh = n[i].sum() / 60.0 / 6.0 * 0.955
        off_rate = sum(1 for a in Wd["acts"] if a["sector"] == s and not a["probe"]) / max((n[i] * ~on[i]).sum() / 60.0, 1) * 1000
        fh[s] = [int(round(mfh * k * float(r.uniform(0.98, 1.02)))) for k in seas]
        rate[s] = [round(off_rate * (k ** 0.9) * float(r.uniform(0.93, 1.07)), 1) for k in seas]
        acts[s] = int(round(sum(f * x / 1000.0 for f, x in zip(fh[s], rate[s]))))
        yr[s] = round(acts[s] / sum(fh[s]) * 1000, 1)
        flights[s] = int(round(sum(fh[s]) * 60 / float(r.uniform(13.2, 14.6))))
    return {"months": months, "fh": fh, "rate": rate, "acts": acts, "flights": flights, "year_rate": yr}


# ------------------------------------------------------------------------------------------------- the pack

def build(target):
    os.makedirs(target, exist_ok=True)
    Wd = W.build()
    p = lambda k: os.path.join(target, FILES[k])
    _csv(p("crossings"), ["ifps_id", "callsign", "adep", "ades", "aircraft_type", "sector", "entry_utc", "exit_utc",
                          "entry_fl", "exit_fl", "plan_revision", "revision_issued_utc"], crossing_rows(Wd))
    _csv(p("stca"), ["alert_id", "sector", "start_utc", "end_utc", "callsign_1", "callsign_2", "pred_min_hsep_nm",
                     "pred_min_vsep_ft", "status"], stca_rows(Wd))
    _csv(p("probe"), ["workstation", "position", "sector", "display_on", "display_off"], probe_rows(Wd))
    _csv(p("config"), ["effective", "configuration", "operational_sectors"], config_rows(Wd))
    _csv(p("sigmet"), ["sigmet", "valid_from_utc", "valid_to_utc", "phenomenon", "area", "levels", "movement"],
         sigmet_rows())
    criteria_pdf(p("criteria"))
    guide_pdf(p("guide"))
    report_pdf(p("report"), report_figures(Wd))
    request_eml(p("request"))
    forecast_xlsx(p("forecast"), Wd)
    training_xlsx(p("training"))
    return Wd


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    build(out)
    for k, fn in FILES.items():
        print("%-10s %-48s %9d bytes" % (k, fn, os.path.getsize(os.path.join(out, fn))))
