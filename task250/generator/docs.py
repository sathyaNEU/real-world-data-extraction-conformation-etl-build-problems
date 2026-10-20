"""task250 documents: the coordinator's request (eml); the quality-control procedure, the 2028 field plan and the
quality control's 2027 alert summary (pdf); the station register and the work orders (xlsx); the dictionary (md)."""
import datetime as dt

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.0, leading=9.8)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _sections(s, sec, body, h2):
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))


def _build(doc, s, foot):
    doc.build(s, onFirstPage=_footer(foot), onLaterPages=_footer(foot))


def _mail(who, local):
    return "%s <%s@%s>" % (who, local, P.DOMAIN)


# ------------------------------------------------------------------ the request (eml)
def request(path, F, n_close, n_taken, per_year):
    text = f"""From: {_mail(P.COORDINATOR[0], "c.hernando")}
To: {_mail("Análisis de datos", "analisis")}
Cc: {_mail(P.FIELD_LEAD[0], "t.falco")}, {_mail(P.QC_ADMIN[0], "i.davila")}
Date: Wed, 5 Jan 2028 09:41:07 +0100
Subject: Drift-alert setting for 2028
Message-ID: <20280105094107.5521@{P.DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Hola,

Inés loads the 2028 configuration of the quality control on 15 January, and
this year I need the setting decided before then rather than carried over. The
irrigation communities took over {n_taken} of the programme's stations and the other
{n_close} closed on 31 December; the second technician's post went with the
programme's funding, so Teodoro's plan for 2028 (in the folder) leaves
{P.BUDGET_YEAR} visits for drift alerts in the year, against the {per_year} or so a year
the alerts have been sending him.

So: which of the four settings in QC-02 should the quality control run in 2028,
the most sensitive one whose drift alerts in the year fit those {P.BUDGET_YEAR} visits, and
how many alerts a year will it raise? Section 7 says how we choose.

The review sheet also carries, as every January, the 2027 drift-alert visits by
district with the days their alerts waited for them, and this year the 2027
breakdown visits at the stations we keep, by district, to set beside the plan's
breakdown allowance.

Everything is in the folder: the loggers' daily export, the quality control's
export, the register, both contractors' work orders, the calibration database's
checks, the procedure, the plan and the 2027 alert summary.

Gracias,
Celia

--
{P.COORDINATOR[0]}
Network quality coordinator, {P.NETWORK}
{P.ORG}
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# ------------------------------------------------------------------ the procedure (pdf)
def procedure(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "QC-02 Air temperature quality control, version 4", P.ORG, "Procedure")
    s = [Paragraph("%s, %s" % (P.ORG, P.NETWORK), small),
         Paragraph("QC-02 Air temperature quality control", h1),
         Paragraph("Version 4, November 2024, in force from 1 January 2025 with the network's 2015 to 2024 normals. "
                   "Replaces version 3 (March 2021). Owner: the network quality coordinator.", small), Spacer(1, 4)]
    sec = [
        ("1. Purpose", [
            "The quality control reads every station's daily air temperature against its neighbours each morning, "
            "so that a sensor drifting out of calibration is visited before its data reach the irrigation advice. "
            "Each drift alert it raises is a field visit (section 8)."]),
        ("2. Daily means", [
            "A station's daily mean is the mean of its logger's records over the local civil day. A day is read when "
            "the logger delivered at least 90 per cent of the records the day should hold: 144 for a logger "
            "recording every ten minutes and 288 for one recording every five over a 24-hour day, and in proportion "
            "over the 23-hour and 25-hour days the clocks change (138 and 150, 276 and 300). A day the logger "
            "did not deliver, or delivered short, is not read (" + F["daily"] + ")."]),
        ("3. Anomaly", [
            "A station's daily anomaly is its daily mean less its normal for the calendar month (the network's "
            "2015 to 2024 normals; a station installed later carries normals interpolated from its neighbours until "
            "the next ten-year update)."]),
        ("4. Estimate and residual", [
            "Each read day, a station's anomaly is estimated from the three stations of the network nearest to it "
            "that have an anomaly that day and lie within 75 km, as the mean of their anomalies weighted by the "
            "inverse square of their distance. Distances are straight-line distances between the register's UTM "
            "coordinates (ETRS89, zone 30). The residual is the station's anomaly less the estimate. A station with "
            "fewer than three such stations that day has no residual that day."]),
        ("5. Drift statistic", [
            "A station's drift statistic on a read day is the mean of its residuals over the 14 days ending that "
            "day, when at least 10 of those days have a residual."]),
        ("6. Limits", [
            "Each January the quality control sets every station's limit for the year: the year's setting times "
            "the standard deviation (n − 1) of the drift statistic the quality control recorded for the station "
            "over the three previous calendar years, or over the days it has since installation if fewer."]),
        ("7. Settings", [
            "The setting is 3.0, 3.5, 4.0 or 4.5. A lower setting catches a drift sooner and raises more alerts. "
            "The setting for a year is chosen in January: the most sensitive setting whose drift alerts in the year "
            "fit the visits the field plan sets aside for drift alerts in that year, planned on the three previous "
            "calendar years with the year's limits applied to each of them."]),
        ("8. Alerts", [
            "The quality control raises a drift alert for a station on a day its drift statistic lies beyond its "
            "limit, either side, unless it raised one for the station on any of the 14 days before; a new year's "
            "configuration does not lift that hold. Each alert opens a "
            "drift-alert work order. The quality control's daily export (" + F["qc"] + ") carries each read day's "
            "anomaly, estimate, residual, the three stations the estimate used, the drift statistic, the limit in "
            "force and the alert."]),
        ("9. Field checks", [
            "At the visit a drift alert calls, and at the spring round, the technician reads the station's sensor "
            "against the transfer standard (an aspirated platinum thermometer, calibrated each year) in three paired "
            "readings ten minutes apart. The as-found "
            "error is the mean of the station's reading less the standard's over the paired readings taken before "
            "any adjustment. A sensor whose as-found error is within 0.3 °C either way is within tolerance; one "
            "beyond 0.2 °C is adjusted and read again, and one more than 1.0 °C out is replaced. A sensor's drift does "
            "not stop on its own: its error goes on growing at the sensor's own rate until a check sets it right. "
            "The consortium's "
            "calibration database holds every reading (" + F["checks"] + "); every adjustment and every sensor "
            "replaced is entered in the station's sensor history in the register (" + F["register"] + ")."]),
    ]
    _sections(s, sec, body, h2)
    _build(doc, s, "QC-02 v4  |  " + P.ORG)


# ------------------------------------------------------------------ the 2028 field plan (pdf)
def field_plan(path, F, n_cont, n_close, n_taken, breakdown_allow):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Field plan 2028", P.ORG, "Field plan")
    s = [Paragraph("%s, %s" % (P.ORG, P.NETWORK), small),
         Paragraph("Field plan 2028", h1),
         Paragraph("%s, field team lead. 20 December 2027." % P.FIELD_LEAD[0], small), Spacer(1, 4)]
    rows = [["Work", "Visits in 2028", "Notes"],
            ["Spring campaign (scheduled checks)", "%d" % n_cont, "March to June, every station once"],
            ["Breakdowns", "%d" % breakdown_allow, "the 2025 and 2026 average for the stations that stay"],
            ["Drift alerts", "%d" % P.BUDGET_YEAR, "the visits left for drift alerts in the year"],
            ["New installations", "0", ""]]
    _sections(s, [("The year", [
        "From 1 January 2028 the field team is one technician with the contractor's support for the campaign. Of "
        "the %d stations installed under %s, the irrigation communities took over %d; the other %d closed on 31 "
        "December 2027 with the programme's funding, which also paid the second technician's post. The network runs "
        "%d stations in 2028." % (n_close + n_taken, P.PROGRAMME, n_taken, n_close, n_cont),
        "The table gives the visits the plan can carry, counted by station: a visit is a day a technician is at a "
        "station, so a day's route that takes in two stations is two visits. Drift alerts take what is left once "
        "the campaign and a "
        "breakdown allowance are in. As under the maintenance contract since July 2027, every visit includes a "
        "check of the station's temperature sensor in place, the sensor and the transfer standard reading the "
        "station's air side by side (QC-02 section 9)."])], body, h2)
    s.append(_grid(rows, [62 * mm, 30 * mm, 78 * mm], cell))
    _build(doc, s, "Field plan 2028  |  " + P.ORG)


# ------------------------------------------------------------------ the 2027 alert summary (pdf), the context artifact
def alert_summary(path, F, qcx, reg):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Drift alerts 2027", P.ORG, "Quality control summary")
    q = qcx[(qcx["alerta"] == "S") & (pd.to_datetime(qcx["fecha"]).dt.year == 2027)]
    dist = dict(zip(reg["code"], reg["district"]))
    names = dict(P.DISTRICTS)
    q = q.assign(d=q["estacion"].map(dist), m=pd.to_datetime(q["fecha"]).dt.month)
    rows = [["District"] + ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"] + ["Year"]]
    for c, nm in P.DISTRICTS:
        g = q[q["d"] == c]
        rows.append([nm] + [str(int((g["m"] == m).sum())) for m in range(1, 13)] + [str(len(g))])
    rows.append(["Network"] + [str(int((q["m"] == m).sum())) for m in range(1, 13)] + [str(len(q))])
    s = [Paragraph("%s, %s" % (P.ORG, P.NETWORK), small),
         Paragraph("Drift alerts raised in 2027", h1),
         Paragraph("Quality control summary, generated 2 January 2028 from %s. Setting 3.0 all year." % F["qc"], small),
         Spacer(1, 4),
         Paragraph("Alerts the quality control raised in 2027 by district and month, at the setting in force. It "
                   "counts alerts, not visits: an alert can be closed before a visit, and a visit can follow from "
                   "another order.", body),
         _grid(rows, [36 * mm] + [9.2 * mm] * 12 + [13 * mm], cell)]
    _build(doc, s, "QC summary 2027  |  " + P.ORG)


# ------------------------------------------------------------------ the register (xlsx)
def register_xlsx(path, reg, hist):
    wb = Workbook()
    ws = wb.active
    ws.title = "Estaciones"
    head = ["codigo", "nombre", "municipio", "comarca", "x_utm", "y_utm", "altitud_m", "alta", "financiacion",
            "baja_prevista", "registro_5min_desde"]
    ws.append(head)
    names = dict(P.DISTRICTS)
    for _, r in reg.iterrows():
        ws.append([r["code"], r["name"], r["municipality"], names[r["district"]], int(r["x_utm"]), int(r["y_utm"]),
                   int(r["z_m"]), r["installed"], r["funding"], r["closes"], r["five_min_from"]])
    for j, w in enumerate([9, 24, 26, 22, 10, 10, 10, 12, 20, 14, 18], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in (row[7], row[9], row[10]):
            if c.value is not None:
                c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Historial sensor T")
    ws2.append(list(hist.columns))
    for r in hist.itertuples(index=False):
        ws2.append([None if (isinstance(v, float) and v != v) else v for v in r])
    for row in ws2.iter_rows(min_row=2):
        row[1].number_format = "dd/mm/yyyy"
        if row[4].value is not None:
            row[4].number_format = "+0.00;-0.00;0.00"
    for j, w in enumerate([9, 11, 24, 24, 19, 22], 1):
        ws2.column_dimensions[get_column_letter(j)].width = w
    for sh in (ws, ws2):
        for c in sh[1]:
            c.font = Font(bold=True)
        sh.freeze_panes = "A2"
    wb.save(path)


# ------------------------------------------------------------------ the dictionary (md)
def dictionary(path, F):
    text = f"""# Network folder: data dictionary

{P.NETWORK}, {P.ORG}. Prepared for the January 2028 configuration.

## {F["daily"]}

The loggers' daily export, 2025 to 2027, as the data platform delivers it (semicolon-separated, decimal commas):
one row per station and local civil day the logger delivered.

| Column | Meaning |
|---|---|
| estacion | station code (register) |
| fecha | local civil day, dd/mm/yyyy |
| tmed, tmax, tmin | daily mean, maximum and minimum air temperature, degrees C |
| n_registros | records the logger delivered for the day |

## {F["qc"]}

The quality control's daily export, one row per station and read day (QC-02 sections 3 to 8): estacion, fecha,
anomalia, estimacion, residuo (degrees C), vecinos (the three stations the estimate used), estadistico_14d (the
drift statistic as the quality control recorded it), limite (the limit in force), alerta (S on a day it raised an
alert).

## {F["orders"]}

The maintenance contractors' work orders. Sheet {P.OLD_CONTRACTOR.split()[2]}: the contractor to 30 June 2027, as
exported for the handover. Sheet {P.NEW_CONTRACTOR.split()[2]}: the contractor from 1 July 2027. Each order carries
the day it was opened (Aviso, opened). Visita is the day the technician visited, blank on a cancelled order (Anulada)
and on one closed without a visit; visit_date is the date the order was closed on the contractor's app, blank on a
cancelled order.

## {F["checks"]}

The consortium's calibration database: every paired reading of a temperature sensor against the transfer standard,
with the station and the work order the entry form recorded (fecha_hora local time, degrees C).

## Other files

- {F["register"]}: the station register (sheet Estaciones; comarca is the district) and each station's
  temperature-sensor history (sheet Historial sensor T: every adjustment with its as-found error in degrees C,
  every sensor replaced, every shield cleaned, with the kind of visit it was done at).
- {F["procedure"]}: the quality-control procedure.
- {F["plan"]}: the field team's plan for 2028.
- {F["summary"]}: the quality control's summary of the alerts raised in 2027.
- {F["request"]}: the request.
- {F["delivery"]}: the data platform's delivery log for 2027 (when each station's day reached the server).
- {F["et0"]}: the weekly reference evapotranspiration the consortium published to irrigators in 2027, by district.
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
