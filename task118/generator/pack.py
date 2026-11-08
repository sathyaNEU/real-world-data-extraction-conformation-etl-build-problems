"""Writes target/: every file as its own system exports it."""
import csv
import datetime as dt
import io
import os
import re
import zipfile

import docx
from docx.shared import Pt
import numpy as np
import openpyxl
from openpyxl.styles import Font

import params as P
import world as Wd
import asks as A

HM = P.HM
FILES = {
    "running": "train_running_autumn_2026.csv",
    "wtt": "working_timetable_autumn_2026.xlsx",
    "census": "passenger_census_2026-10-13.csv",
    "stations": "station_register.csv",
    "brief": "dispatch_team_brief_2027.docx",
    "perf": "performance_summary_autumn_2026.xlsx",
    "gates": "gateline_readings_2026-10-12_to_16.csv",
    "repay": "delay_repay_claims_extract_2027-01-15.csv",
    "incidents": "incident_log_autumn_2026.csv",
    "usage": "station_usage_estimates_2025-26.csv",
}
DISTRACTORS = ["incidents", "usage"]
RAIL = "Ravelstoke Rail"
CARDALE = "Cardale Railways Ltd"


def clock(t_hm):
    """hh:mm:ss on the half-minute grid."""
    s = int(round(t_hm * 30))
    return "%02d:%02d:%02d" % (s // 3600, (s // 60) % 60, s % 60)


def xl_time(t_hm):
    """A booked time as the planning system exports it to Excel: a time of day to the second."""
    sec = int(round(t_hm * 30))
    return dt.time(sec // 3600, (sec // 60) % 60, sec % 60)


def wtt_time(t_hm):
    """Working timetable style: hh:mm with H for the half minute."""
    m = t_hm // HM
    return "%02d:%02d%s" % (m // 60, m % 60, "H" if t_hm % HM else "")


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------------------------------------------------
# OOXML containers written as Office saves them
# ---------------------------------------------------------------------------------------------------------

CORE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxml'
        'formats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms='
        '"http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/'
        'XMLSchema-instance">{title}<dc:creator>{creator}</dc:creator><cp:lastModifiedBy>{editor}</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDT'
        'F">{modified}</dcterms:modified></cp:coreProperties>')
APP_DOCX = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.o'
            'rg/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
            'docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>{mins}</TotalTime><Pages>{pages}</Pages><Words>'
            '{words}</Words><Characters>{chars}</Characters><Application>Microsoft Office Word</Application><DocSecurity>'
            '0</DocSecurity><Lines>{lines}</Lines><Paragraphs>{paras}</Paragraphs><ScaleCrop>false</ScaleCrop><Company>'
            '{company}</Company><LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>{charsp}</CharactersWithSpaces>'
            '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion>'
            '</Properties>')
APP_XLSX = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.o'
            'rg/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
            'docPropsVTypes"><Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false'
            '</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr>'
            '</vt:variant><vt:variant><vt:i4>{n}</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector'
            ' size="{n}" baseType="lpstr">{parts}</vt:vector></TitlesOfParts><Company>{company}</Company><LinksUpToDate>'
            'false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>'
            '16.0300</AppVersion></Properties>')


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def ooxml_finish(raw, path, kind, creator, editor, company, created, modified, title=None, sheets=None, text=""):
    src = zipfile.ZipFile(io.BytesIO(raw))
    words = len(text.split())
    chars = len(text.replace(" ", ""))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = CORE.format(title=("<dc:title>%s</dc:title>" % title) if title else "", creator=creator,
                                   editor=editor, created=_iso(created), modified=_iso(modified)).encode()
            elif info.filename == "docProps/app.xml":
                if kind == "docx":
                    data = APP_DOCX.format(mins=37 + words % 23, pages=max(1, words // 420 + 1), words=words,
                                           chars=chars, lines=max(1, chars // 70), paras=max(1, text.count("\n") + 1),
                                           company=company, charsp=len(text)).encode()
                else:
                    parts = "".join("<vt:lpstr>%s</vt:lpstr>" % s for s in sheets)
                    data = APP_XLSX.format(n=len(sheets), parts=parts, company=company).encode()
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def write_xlsx(path, sheets, creator, editor, company, created, modified, widths=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold_rows in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
            for c in ws[ws.max_row]:
                if isinstance(c.value, dt.time):
                    c.number_format = "hh:mm:ss"
        for i in bold_rows:
            for c in ws[i + 1]:
                c.font = Font(bold=True)
        for col, wdt in zip("ABCDEFGHIJKLMNOP", widths or [14] * 16):
            ws.column_dimensions[col].width = wdt
    buf = io.BytesIO()
    wb.save(buf)
    ooxml_finish(buf.getvalue(), path, "xlsx", creator, editor, company, created, modified,
                 sheets=[s[0] for s in sheets])


def write_docx(path, blocks, creator, editor, company, created, modified, title):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    text = []
    for kind, val in blocks:
        if kind == "h":
            d.add_heading(val, level=1)
        elif kind == "h2":
            d.add_heading(val, level=2)
        elif kind == "p":
            d.add_paragraph(val)
        elif kind == "b":
            d.add_paragraph(val, style="List Bullet")
        elif kind == "t":
            rows = val
            tb = d.add_table(rows=len(rows), cols=len(rows[0]))
            tb.style = "Table Grid"
            for i, r in enumerate(rows):
                for j, c in enumerate(r):
                    tb.cell(i, j).text = str(c)
            text.extend(" ".join(map(str, r)) for r in rows)
            continue
        text.append(val)
    buf = io.BytesIO()
    d.save(buf)
    ooxml_finish(buf.getvalue(), path, "docx", creator, editor, company, created, modified, title=title,
                 text="\n".join(text))


# ---------------------------------------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------------------------------------

def running_rows(W):
    trains = W["trains"]
    rows = []
    for d in W["days"]:
        rec = W["records"][d]
        for tr in sorted(trains, key=lambda t: t["bdep"][0]):
            r = rec[tr["id"]]
            for k, st in enumerate(tr["stops"]):
                name = P.STATIONS[tr["line"]][st]
                a = r["arr"][k]
                dp = r["dep"][k]
                rows.append((d.isoformat(), tr["headcode"], r["unit"], P.TIPLOC[name],
                             clock(a) if a is not None else "", clock(dp) if dp is not None else ""))
    return rows


def wtt_sheets(W):
    trains = W["trains"]
    sheets = []
    for line in P.LINES:
        rows = [("Headcode", "Origin", "Destination", "Location", "TIPLOC", "Arr", "Dep", "Allowance")]
        for tr in sorted([t for t in trains if t["line"] == line], key=lambda t: t["bdep"][0]):
            o = P.STATIONS[line][tr["stops"][0]]
            de = P.STATIONS[line][tr["stops"][-1]]
            for k, st in enumerate(tr["stops"]):
                name = P.STATIONS[line][st]
                allow = ""
                if k > 0:
                    _, al = Wd._run_between(line, tr["stops"][k - 1], st, tr["dir"])
                    if al:
                        allow = "[%s]" % ({1: "½", 2: "1", 3: "1½", 4: "2"}[al])
                rows.append((tr["headcode"], o, de, name, P.TIPLOC[name],
                             xl_time(tr["barr"][k]) if tr["barr"][k] is not None else None,
                             xl_time(tr["bdep"][k]) if tr["bdep"][k] is not None else None, allow))
        sheets.append((P.LINE_NAME[line], rows, [0]))
    rules = [("Planning rules, autumn 2026 timetable", "", "", ""),
             ("", "", "", ""),
             ("Sectional running times (minutes), each direction", "", "", ""),
             ("Line", "From", "To", "SRT")]
    for line in P.LINES:
        for j in range(10):
            rules.append((P.LINE_NAME[line], P.STATIONS[line][j], P.STATIONS[line][j + 1],
                          P.SRT[line][j] / HM))
    rules += [("", "", "", ""),
              ("Station working", "", "", ""),
              ("Dwell at a calling point", "as booked; half a minute at least", "", ""),
              ("Allowance shown in brackets", "added to the running time of the section ending at that timing point", "", ""),
              ("Departure", "No train leaves a timing point before its booked departure time", "", ""),
              ("Planning headway, all three lines", "2 minutes", "", "")]
    sheets.append(("Planning rules", rules, [0, 3]))
    return sheets


def census_rows(W):
    rows = []
    for tr in sorted(W["trains"], key=lambda t: (t["bdep"][0], t["headcode"])):
        ons, offs = W["census"][tr["id"]]
        for k, st in enumerate(tr["stops"]):
            name = P.STATIONS[tr["line"]][st]
            rows.append((tr["headcode"], clock(tr["bdep"][0]), P.CRS[name], name, int(ons[k]), int(offs[k])))
    return rows


def station_rows():
    rows = []
    plat = {"Ravelstoke Central": 8, "Saltgate": 3, "Pellingham": 2, "Ambrey Parkway": 3, "Brathwick Road": 2,
            "Ravelstoke Airport": 2, "Hartlow": 3, "Holm Ferry": 2, "Crossmoor": 2}
    seen = set()
    for line in P.LINES:
        for i, name in enumerate(P.STATIONS[line]):
            if name in seen:
                continue
            seen.add(name)
            lines = "Crossmoor; Ambrey; Holm Ferry" if name == "Ravelstoke Central" else P.LINE_NAME[line].split(" ")[0] \
                if line != "S" else "Holm Ferry"
            gated = "Y" if (name in P.GATED or name == "Ravelstoke Central") else "N"
            rows.append((P.CRS[name], P.TIPLOC[name], name, lines, plat.get(name, 2), gated,
                         "06:00-20:00" if name in plat else ("07:00-10:00" if i % 3 == 0 else "")))
    return rows


def perf_sheets(W):
    trains = W["trains"]
    months = [("September 2026", 9), ("October 2026", 10), ("November 2026", 11)]
    rows = [("Weekday performance, Ravelstoke Rail network, by line and month", "", "", "", "", ""),
            ("Source: Cardale train running record. Refreshed 4 December 2026.", "", "", "", "", ""),
            ("Month", "Line", "Weekdays", "Trains run", "Station stops on time (per cent)",
             "Trains at destination within 5 minutes (per cent)")]
    for mname, m in months:
        ds = [d for d in W["days"] if d.month == m]
        for line in P.LINES:
            run = within5 = stops = on_time = 0
            for d in ds:
                rec = W["records"][d]
                for tr in trains:
                    if tr["line"] != line:
                        continue
                    r = rec[tr["id"]]
                    run += 1
                    within5 += r["arr"][-1] - tr["barr"][-1] < 5 * HM
                    for k in range(1, len(tr["stops"])):
                        stops += 1
                        on_time += r["arr"][k] - tr["barr"][k] < 1 * HM
            rows.append((mname, P.LINE_NAME[line], len(ds), run, round(100.0 * on_time / stops, 1),
                         round(100.0 * within5 / run, 1)))
    return [("Weekday performance", rows, [0, 2])]


def gate_rows(W):
    rows, truth = A.gate_readings(W)
    out = []
    for st, a, t, en, ex in rows:
        out.append((P.CRS[st], a, t.strftime("%Y-%m-%d %H:%M:%S"), en, ex))
    return out, truth


def repay_rows(W):
    claims, truth = A.delay_repay(W)
    out = []
    for c in claims:
        out.append((c["claim_ref"], c["channel"], c["submitted"].strftime("%Y-%m-%d %H:%M"), c["ticket"],
                    c["ticket_ref"], c["journey_date"].isoformat(), c["origin"], c["destination"],
                    wtt_time(c["booked_dep"]).replace("H", ""), c["claimed"], c["decision"], c["band_paid"],
                    c["paid_on"].isoformat() if c["paid_on"] else "", "%.2f" % c["amount"] if c["decision"] == "APPROVED" else "",
                    c["method"]))
    return out, truth


def incident_rows(W):
    rows = []
    n = 1000
    for (d, line, direction, t_from, sec, mins) in P.DISRUPTIONS:
        n += 37
        loc = P.STATIONS[line][sec]
        rows.append(("RR%05d" % n, d.isoformat(), wtt_time(t_from)[:5], P.LINE_NAME[line], loc,
                     ["Signal failure", "Trespass", "Points failure", "Overhead line", "Track circuit failure",
                      "Fatality", "Track circuit failure"][n % 7], len(mins), sum(mins)))
    rng = np.random.default_rng([P.SEED, 339])
    causes = ["Train fault", "Station overrun", "Crew late", "Signal failure", "Passenger illness", "Trespass",
              "Points failure", "Level crossing fault", "Possession overrun"]
    for d in W["days"]:
        for _ in range(int(rng.integers(1, 5))):
            n += int(rng.integers(5, 30))
            line = P.LINES[int(rng.integers(3))]
            loc = P.STATIONS[line][int(rng.integers(11))]
            t = int(rng.integers(6 * 60, 22 * 60))
            rows.append(("RR%05d" % n, d.isoformat(), "%02d:%02d" % (t // 60, t % 60), P.LINE_NAME[line], loc,
                         causes[int(rng.integers(len(causes)))], int(rng.integers(1, 4)), int(rng.integers(3, 14))))
    rows.sort(key=lambda r: (r[1], r[2]))
    return rows


def usage_rows():
    rng = np.random.default_rng([P.SEED, 444])
    rows = []
    for line in P.LINES:
        for name in P.STATIONS[line]:
            if name == "Ravelstoke Central" and line != "N":
                continue
            base = Wd.STATION_WEIGHT[name] * 410000
            if name == "Ravelstoke Central":
                base = 6.1e6
            e = int(base * rng.uniform(0.85, 1.15))
            rows.append((P.CRS[name], name, e, int(e * rng.uniform(0.03, 0.09)), "2025-26"))
    return rows


BRIEF_DATES = (dt.datetime(2026, 12, 2, 9, 14, 0), dt.datetime(2026, 12, 9, 16, 41, 0))


def brief_blocks():
    short = list(P.SHORTLIST)
    return [
        ("h", "Platform dispatch team, 2027: siting brief"),
        ("p", "Ravelstoke Rail, Performance and Planning. Issued by Julia Clayton, Head of Rail Performance, "
              "9 December 2026."),
        ("h2", "1. Purpose"),
        ("p", "The 2027 Rail Plan funds one platform dispatch team on the suburban network from the May 2027 "
              "timetable change. This brief sets out how the station that receives it is chosen. Cardale Railways "
              "will employ the team under the concession and roster it at the chosen station."),
        ("h2", "2. The shortlist"),
        ("p", "Stations put forward by Cardale and by the three line partnerships, and shortlisted by the rail "
              "executive in November 2026: " + ", ".join(short[:-1]) + " and " + short[-1] + "."),
        ("h2", "3. How a station is valued"),
        ("p", "A team at a station is worth the passenger lateness it takes off the network's weekday trains. "
              "Passenger lateness is each passenger's minutes after the booked arrival at the station where they "
              "leave the train, with none for an early or on-time arrival, summed over every weekday passenger "
              "train. It is valued on the autumn 2026 weekdays as they ran, Monday 7 September to Friday "
              "27 November 2026, averaged per weekday, with passengers as counted in the autumn 2026 passenger "
              "census on Tuesday 13 October 2026."),
        ("p", "The team works the station's platforms on weekdays from 06:30 to 19:30. For planning purposes it "
              "removes three fifths of the time each train's dwell at its station runs over the booked dwell, for "
              "every train booked to depart the station from 06:30 up to 19:30. This is the planning assumption "
              "Cardale took from its 2025 dispatch trial at Quayside."),
        ("h2", "4. What the rail executive needs"),
        ("p", "The station that would take the most passenger lateness off the network, the saving there, the "
              "runner-up and the gap between them. The 2027 timetable keeps the autumn 2026 train plan on all three "
              "lines, so the autumn weekdays stand for 2027."),
    ]


def build(target):
    os.makedirs(target, exist_ok=True)
    W = Wd.build_world()
    _csv(os.path.join(target, FILES["running"]), ["date", "headcode", "unit", "tiploc", "arr", "dep"],
         running_rows(W))
    write_xlsx(os.path.join(target, FILES["wtt"]), wtt_sheets(W), CARDALE, "Leon Ross", CARDALE,
               dt.datetime(2026, 7, 28, 10, 2, 0), dt.datetime(2026, 8, 25, 14, 37, 0), [10, 18, 18, 18, 10, 9, 9, 10])
    _csv(os.path.join(target, FILES["census"]),
         ["headcode", "origin_dep", "crs", "station", "boarders", "alighters"], census_rows(W))
    _csv(os.path.join(target, FILES["stations"]),
         ["crs", "tiploc", "station", "lines", "platforms", "gated", "booking_office_hours"], station_rows())
    write_docx(os.path.join(target, FILES["brief"]), brief_blocks(), RAIL, "Julia Clayton", RAIL,
               BRIEF_DATES[0], BRIEF_DATES[1], "Platform dispatch team, 2027: siting brief")
    write_xlsx(os.path.join(target, FILES["perf"]), perf_sheets(W), CARDALE, "Leon Ross", CARDALE,
               dt.datetime(2026, 12, 3, 8, 50, 0), dt.datetime(2026, 12, 4, 11, 26, 0), [22, 18, 10, 11, 26, 30])
    g, gt = gate_rows(W)
    _csv(os.path.join(target, FILES["gates"]), ["crs", "array", "reading_utc", "entries", "exits"], g)
    rp, rt = repay_rows(W)
    _csv(os.path.join(target, FILES["repay"]),
         ["claim_ref", "channel", "submitted", "ticket", "ticket_ref", "journey_date", "origin_crs", "destination_crs",
          "booked_departure", "delay_claimed", "decision", "band_paid", "paid_on", "amount_gbp", "payment_method"], rp)
    _csv(os.path.join(target, FILES["incidents"]),
         ["incident", "date", "time", "line", "location", "cause", "trains_delayed", "delay_minutes"], incident_rows(W))
    _csv(os.path.join(target, FILES["usage"]),
         ["crs", "station", "entries_and_exits", "interchanges", "year"], usage_rows())
    return W, gt, rt
