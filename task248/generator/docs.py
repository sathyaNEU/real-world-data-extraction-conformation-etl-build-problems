"""task248 documents: the coordinator's request (eml); the dashboard's methods note, the paired study's field report,
the network modeller's travel-time memo, the historian export note and the laboratory's export notes (pdf); the
contract laboratory's report, the dashboard's winter 2027 export and the laboratory's quality assessment returns
(xlsx); the data dictionary and the folder's contents list (md)."""
import datetime as dt
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess
import records as RC

CONTRACT_LAB = "Rangeview Analytical"


def _addr(who, domain=P.DOMAIN):
    name, user = who
    return "%s <%s@%s>" % (name, user, domain)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
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


# ------------------------------------------------------------------ the request (eml)
def request(path, F):
    text = f"""From: {_addr(P.COORDINATOR)}
To: Surveillance analytics <surveillance.analytics@{P.DOMAIN}>
Cc: {_addr(P.SCIENTIST)}
Date: Tue, 11 Apr 2028 16:42:07 +1200
Subject: Winter 2028 desk rota
Message-ID: <20280411164207.5521@{P.DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Hi all,

The surveillance manager signs off the verification desk's rota for May to
September on 20 April. As every year, I size it on last winter's samples read the
way the dashboard will read them this winter, and from 1 May that means the shed
load (methods note, version 4, section 6). Last winter the desk checked every
episode on the published levels. Please tell me how many episodes last winter's
samples raise on the shed load, the total on each basis, and whether any plant's
count moves.

Two more things land on the desk from 1 May. The dashboard takes each composite's
flow from Southern Plains Water's historian, so I need each plant's hours from 1
April 2027 to 31 March 2028 with no valid inlet flow reading in the historian;
and the faecal-strength check starts, so I need each plant's composites from 4
October 2027 to 30 March 2028 that the check flags. Both go in the rota note
beside the episodes.

Everything is in the folder: Luke's results export and its notes, the contract
laboratory's report for the January closure, the historian export and its note,
the site register, Craig's travel-time memo, Alana's paired study and her field
report, and the dashboard's export for last winter.

Thanks,
Fiona

--
{P.COORDINATOR[0]}
Wastewater surveillance coordinator
{P.SERVICE}
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# ------------------------------------------------------------------ the dashboard's methods note (pdf)
def methods(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "%s: methods note, version 4" % P.DASHBOARD, P.SERVICE, "Methods note")
    s = [Paragraph("%s, surveillance team" % P.SERVICE, small),
         Paragraph("%s: methods note" % P.DASHBOARD, h1),
         Paragraph("Version 4, March 2028. Replaces version 3 (April 2026). Section 6 takes effect on 1 May 2028.",
                   small), Spacer(1, 4)]
    sec = [
        ("1. Purpose",
         ["The dashboard follows SARS-CoV-2 in the wastewater of the region's 24 treatment plants (the site register, "
          "%s). It gives each plant a weekly level against the plant's own baseline, and the service's verification desk "
          "checks every alert episode the dashboard raises before the public health team acts on it." % F["register"]]),
        ("2. Samples and results",
         ["Each plant's autosampler takes a 24-hour flow-paced composite of the plant's inflow, ending at 08:00 on "
          "Mondays and Thursdays. The %s analyses each sample for the N1 gene of SARS-CoV-2 and for pepper mild mottle "
          "virus (PMMoV), a faecal marker, and reports gene copies per litre of wastewater. A sample's result for a "
          "target is the laboratory's accepted analysis (export notes, %s)." % (P.LAB, F["labnote"])]),
        ("3. The load per person",
         ["A sample's load per person is its N1 concentration times the composite's flow (the volume the plant received "
          "over the composite's 24 hours, in cubic metres) times 1,000, divided by the population the plant serves (the "
          "site register), in gene copies per person per day. Until 30 April 2028 the dashboard takes the composite's "
          "flow from the chain-of-custody form; from 1 May 2028 it takes the plant's inflow over the composite's 24 hours "
          "from %s's historian (export note, %s)." % (P.WATER, F["scadanote"])]),
        ("4. Weekly values, baselines and levels",
         ["A sample counts in the week, Monday to Sunday, of the day its composite ended. A plant's weekly value is the "
          "mean of the log10 loads per person of the week's samples. A plant's baseline for a winter is the 10th "
          "percentile (PERCENTILE.INC) of its weekly values over the 52 weeks starting on the first Monday of April of "
          "the year before; for winter 2027, the weeks starting 6 April 2026 to 29 March 2027. A plant's level in a "
          "week is its weekly value less its baseline, in log10 units."]),
        ("5. Bands and alert episodes",
         ["Low is a level below 0.5; Moderate 0.5 to below 1.0; High 1.0 to below 1.5; Very high 1.5 or more. An alert "
          "episode opens in the first week a plant's level is at High or above and closes in the first week after that "
          "in which its level is back at Low; a plant does not open another episode while one is open. A winter's "
          "episodes are those that open in the weeks starting from the first Monday of May to the last Monday of "
          "September; for winter 2027, the weeks starting 3 May to 27 September 2027. The verification desk checks "
          "each episode in the week it opens."]),
        ("6. From 1 May 2028",
         ["<b>6.1 The shed load.</b> The dashboard reads every sample on its shed load: the load the town shed into the "
          "sewer, that is, the load reaching the plant with the RNA the sewer destroyed on the way from the town to the "
          "plant restored. The restoration rests on the paired upstream study (field report, %s), which measured the "
          "RNA lost between the heads of four plants' trunk sewers and the plants, and on each plant's "
          "population-weighted travel time from the network model (%s). Weekly values, baselines, levels and episodes "
          "are computed on the shed load per person exactly as sections 4 and 5 compute them on the load per person."
          % (F["studyreport"], F["travel"]),
          "<b>6.2 The flow.</b> Each composite's flow is the plant's inflow over the composite's 24 hours from the "
          "historian (section 3).",
          "<b>6.3 The faecal-strength check.</b> A composite's PMMoV load per person is its PMMoV concentration times "
          "the composite's flow from the historian times 1,000, divided by the population served. A composite whose "
          "PMMoV load per person is more than 0.5 log10 above or below the median of the plant's PMMoV loads per person "
          "over its composites collected in the 365 days before the composite's day fails the check, and the desk "
          "checks it before its N1 result enters the plant's level."]),
    ]
    _sections(s, sec, body, h2)
    s.append(Paragraph("Document history", h2))
    rows = [["Version", "Date", "Change"],
            ["1", "October 2021", "First issue: weekly concentrations for nine plants."],
            ["2", "May 2023", "Loads per person and baselines for all 24 plants."],
            ["3", "April 2026", "Bands and alert episodes; the verification desk."],
            ["4", "March 2028", "The shed load, the historian's flow and the faecal-strength check (section 6)."]]
    s.append(_grid(rows, [20 * mm, 25 * mm, 125 * mm], cell))
    _build(doc, s, "%s: %s, methods note v4" % (P.SERVICE_SHORT, P.DASHBOARD))
    postprocess.scrub(path, P.SERVICE, "2028-03-21")


# ------------------------------------------------------------------ the paired study's field report (pdf)
def study_report(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Paired upstream sampling study, 2026: field report", P.SERVICE, "Field report")
    s = [Paragraph("%s, surveillance team" % P.SERVICE, small),
         Paragraph("Paired upstream sampling study, 2026: field report", h1),
         Paragraph("%s, field scientist. May 2027." % P.FIELD[0], small), Spacer(1, 4)]
    sec = [
        ("1. Purpose",
         ["To measure how much of the SARS-CoV-2 RNA in a town's sewage reaches the treatment plant, so that the "
          "dashboard can read every sample on the load the town shed."]),
        ("2. Design",
         ["Four plants whose towns enter a single trunk sewer that takes in nothing else on its way to the plant, chosen "
          "to span the region's travel times: Dunkerley, Netherleigh, Ardenmouth South and Cleaveland Flat. Every second "
          "Monday from 2 February 2026 to 25 January 2027 the field team set a 24-hour flow-paced composite sampler at "
          "the head of the trunk sewer, where the town's sewage enters it, ending at 08:00, and the plant's own "
          "composite was set to start later by the plant's travel time in the network model (%s), so that the two "
          "composites hold the same sewage." % F["travel"],
          "The %s analysed both composites of each pair in triplicate (three extractions) for the N1 gene and PMMoV."
          % P.LAB]),
        ("3. Field measurements",
         ["At each composite's collection the team read the water's temperature, pH and conductivity at the sampling "
          "point with a handheld meter."]),
        ("4. Visits",
         ["Twenty-six visits were planned at each plant. Three were missed: Netherleigh on 8 June 2026 (the trunk's "
          "access chamber was flooded), Ardenmouth South on 26 October 2026 (sampler fault) and Dunkerley on 21 December "
          "2026 (holiday staffing)."]),
        ("5. The results file",
         ["%s gives one row per plant, visit, sampling point and replicate, with the composite's start and end, the "
          "laboratory's results as reported to the study in gene copies per millilitre, and the field measurements. The "
          "file is complete; the study's analysis is to be reported with the dashboard's shed-load method." % F["study"]]),
    ]
    _sections(s, sec, body, h2)
    rows = [["Plant", "Trunk sewer sampled at", "Travel time (min)"]]
    tt = {p[0]: p[4] for p in P.PLANTS}
    heads = {"DNK": "Dunkerley pump station outlet", "NTL": "Pell Valley Road chamber",
             "ADS": "South Ardenmouth interceptor head", "CLF": "Cleaveland Flat rising main outlet"}
    for code in ("DNK", "NTL", "ADS", "CLF"):
        name = [p[1] for p in P.PLANTS if p[0] == code][0]
        rows.append([name, heads[code], tt[code]])
    s.append(Spacer(1, 4))
    s.append(_grid(rows, [45 * mm, 85 * mm, 35 * mm], cell))
    _build(doc, s, "%s: paired upstream sampling study, field report" % P.SERVICE_SHORT)
    postprocess.scrub(path, P.SERVICE, "2027-05-07")


# ------------------------------------------------------------------ the network modeller's travel-time memo (pdf)
def travel_memo(path, F, rows):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Population-weighted travel times to the treatment plants", P.WATER, "Memo")
    s = [Paragraph("%s, network modelling" % P.WATER, small),
         Paragraph("Population-weighted travel times to the treatment plants", h1),
         Paragraph("Memo to the %s surveillance team. %s, network modeller. 17 November 2025." % (P.SERVICE_SHORT,
                                                                                              P.MODELLER[0]), small),
         Spacer(1, 4)]
    sec = [
        ("Method",
         ["Each plant's catchment is divided into the sub-catchments of the calibrated network model. For each "
          "sub-catchment the hydraulic model gives the time the sewage takes from the sub-catchment's centroid to the plant's "
          "inlet at average dry-weather flow; the plant's travel time is the mean of these times weighted by each "
          "sub-catchment's population at the 2023 census."]),
        ("Table",
         ["Travel times in minutes, with the shortest and longest sub-catchment times."]),
    ]
    _sections(s, sec, body, h2)
    t = [["Plant", "Code", "Sub-catchments", "Population-weighted (min)", "Shortest (min)", "Longest (min)"]]
    for code, name, nsub, tt, lo, hi in rows:
        t.append([name, code, nsub, tt, lo, hi])
    s.append(_grid(t, [42 * mm, 14 * mm, 25 * mm, 36 * mm, 26 * mm, 26 * mm], cell))
    _build(doc, s, "%s network modelling: population-weighted travel times" % P.WATER)
    postprocess.scrub(path, P.WATER, "2025-11-17")


# ------------------------------------------------------------------ the historian export note (pdf)
def scada_note(path, F, R):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Inlet historian export: note", P.WATER, "Export note")
    s = [Paragraph("%s, operations technology" % P.WATER, small),
         Paragraph("Inlet historian export for the %s" % P.SERVICE, h1),
         Paragraph("Export of 10 April 2028.", small), Spacer(1, 4)]
    sec = [
        ("The export",
         ["%s spans 00:00 on 5 January 2026 to 23:00 on 9 April 2028, %s hours, with a row for each plant and hour "
          "the historian holds: the plant's inlet flow (cubic metres an hour, the mean over the hour) and its inlet "
          "temperature (degrees Celsius, the probe in the inlet channel). Timestamps are New Zealand local time, the "
          "start of each hour." % (F["scada"], "{:,}".format(R.span_hours()))]),
        ("Inlet channels",
         ["From 18 October 2027 the inlet works at Kestrel Bay, Pellingham and Upper Waldon have a second inlet channel. "
          "The historian's inlet flow at these plants is the plant's total over both channels."]),
        ("Readings since October 2027",
         ["In October 2027 the plants' outstations moved to the new cellular network, and since then the historian has "
          "missed readings. An hour without a row is an hour the historian received nothing for. An outstation that "
          "loses its link repeats its last reading until the link returns, so in a run of four or more identical "
          "consecutive flow readings every reading after the first is held, not measured. A blank flow is a reading the "
          "outstation marked as bad, and a flow of zero or below is a meter fault. A valid inlet flow reading is one "
          "that is none of these."]),
    ]
    _sections(s, sec, body, h2)
    _build(doc, s, "%s: inlet historian export note" % P.WATER)
    postprocess.scrub(path, P.WATER, "2028-04-10")


# ------------------------------------------------------------------ the laboratory's export notes (pdf)
def lab_note(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Wastewater results export: notes for users", P.LAB, "Export notes")
    s = [Paragraph("%s, molecular section" % P.LAB, small),
         Paragraph("Wastewater results export: notes for users", h1),
         Paragraph("%s, scientist. April 2028." % P.SCIENTIST[0], small), Spacer(1, 4)]
    sec = [
        ("Rows",
         ["%s gives one row per sample, target and analysis run. The sample id is the plant code and the date the "
          "composite ended. The targets are N1 (the SARS-CoV-2 N1 gene) and PMMoV, in gene copies per litre of "
          "wastewater." % F["lab"]]),
        ("Runs",
         ["Each day's samples are extracted and analysed on two plates. A run whose extraction control (BCoV) recovers "
          "below 1 per cent is inhibited: it is rejected, and the sample is extracted again and analysed on a later "
          "plate. A high N1 result may be repeated from the same extract as a check. The accepted run is the sample's "
          "result for the target; rejected and check runs are kept for the record."]),
        ("The composite's flow",
         ["composite_flow_m3 is the flow the plant operator writes on the chain-of-custody form: the autosampler "
          "controller's flow total over the composite, in cubic metres."]),
        ("The January closure",
         ["The laboratory closed from 23 December 2027 to 9 January 2028 and the composites of those days went to %s; "
          "their results are in the contract laboratory's report (%s), not in this export." % (CONTRACT_LAB,
                                                                                              F["contract"])]),
    ]
    _sections(s, sec, body, h2)
    _build(doc, s, "%s: wastewater results export, notes" % P.LAB)
    postprocess.scrub(path, "Public Health Laboratory", "2028-04-10")


# ------------------------------------------------------------------ workbooks
def _head(ws, row, head, widths):
    for j, h in enumerate(head, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w


def contract_report(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"
    lines = ["%s: test report WL-2801" % CONTRACT_LAB,
             "Client: %s, wastewater surveillance" % P.SERVICE,
             "Samples: 24-hour wastewater composites received 24 December 2027 to 7 January 2028",
             "Method: %d mL of each composite concentrated by PEG precipitation; the pellet resuspended in %d mL of "
             "phosphate-buffered saline, of which %d uL was extracted and the nucleic acids eluted in %d uL; RT-qPCR "
             "for the SARS-CoV-2 N1 gene and PMMoV in duplicate wells. Results are gene copies per uL of extract, the "
             "mean of the wells." % (RC.CONTRACT_ML, RC.CONTRACT_RESUSP_ML, RC.CONTRACT_ALIQ_UL, RC.CONTRACT_UL),
             "Report date: 14 January 2028"]
    for k, t in enumerate(lines, 1):
        ws.cell(row=k, column=1, value=t).font = Font(bold=(k == 1))
    _head(ws, 7, ["Lab ref", "Client site", "Sampled", "Received", "Analyte", "Result", "Flow on CoC (m3)"],
          [11, 26, 11, 11, 15, 10, 15])
    r = 8
    for lab_ref, site, d, rec, tgt, v, flow in rows:
        for j, x in enumerate([lab_ref, site, d, rec, tgt, v, flow], 1):
            c = ws.cell(row=r, column=j, value=x)
            if isinstance(x, dt.date):
                c.number_format = "dd/mm/yyyy"
        r += 1
    ws.freeze_panes = "A8"
    wb.save(path)
    postprocess.scrub(path, CONTRACT_LAB, "2028-01-14")
    postprocess.finish_office(path, "2028-01-13T21:12:00Z", "2028-01-13T23:40:00Z", CONTRACT_LAB)


def dashboard_workbook(path, lev_rows, eps):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly levels"
    ws.cell(row=1, column=1, value="%s: winter 2027 export (published levels)" % P.DASHBOARD).font = Font(bold=True)
    ws.cell(row=2, column=1, value="The levels the dashboard published for the weeks of winter 2027, on each sample's "
                                   "N1 load per person (methods note v3). Weekly value: mean log10 N1 load per person "
                                   "per day of the week's samples. Level: the weekly value less the plant's baseline.")
    ws.cell(row=3, column=1, value="Export of 19 October 2027, surveillance team.")
    _head(ws, 4, ["Plant", "Week starting", "Samples", "Weekly value", "Baseline", "Level", "Band"],
          [8, 13, 9, 12, 10, 8, 11])
    r = 5
    for code, w, n, wv, base, lev, band in lev_rows:
        for j, x in enumerate([code, w, n, wv, base, lev, band], 1):
            c = ws.cell(row=r, column=j, value=x)
            if isinstance(x, dt.date):
                c.number_format = "yyyy-mm-dd"
        r += 1
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Alert episodes")
    ws2.cell(row=1, column=1, value="Alert episodes the dashboard raised in winter 2027 on its published levels, as the "
                                    "verification desk checked them").font = Font(bold=True)
    _head(ws2, 3, ["Episode", "Plant", "Opened (week starting)", "Closed (week starting)", "Peak level", "Checked by",
                   "Referred on"], [9, 8, 14, 14, 10, 10, 12])
    staff = ["FC", "MT", "JR"]
    r = 4
    for k, (code, start, end, peak) in enumerate(eps, 1):
        ref = start + dt.timedelta(days=3 + (k % 2))
        vals = ["E27-%02d" % k, code, start, end, peak, staff[k % 3], ref]
        for j, x in enumerate(vals, 1):
            c = ws2.cell(row=r, column=j, value=x)
            if isinstance(x, dt.date):
                c.number_format = "yyyy-mm-dd"
        r += 1
    wb.save(path)
    postprocess.scrub(path, P.SERVICE, "2027-10-20")
    postprocess.finish_office(path, "2027-10-19T20:05:00Z", "2027-10-19T21:31:00Z", P.SERVICE)


def eqa_workbook(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Returns"
    ws.cell(row=1, column=1, value="%s: external quality assessment returns, wastewater SARS-CoV-2" % P.LAB).font = \
        Font(bold=True)
    ws.cell(row=2, column=1, value="Assigned value and result in log10 gene copies per litre; z-score on the scheme's "
                                   "standard deviation for proficiency of 0.28.")
    _head(ws, 4, ["Round", "Dispatched", "Sample", "Analyte", "Assigned", "Result", "z-score"],
          [11, 12, 11, 14, 10, 9, 9])
    r = 5
    for row in rows:
        for j, x in enumerate(row, 1):
            c = ws.cell(row=r, column=j, value=x)
            if isinstance(x, dt.date):
                c.number_format = "yyyy-mm-dd"
        r += 1
    wb.save(path)
    postprocess.scrub(path, "Public Health Laboratory", "2027-12-08")
    postprocess.finish_office(path, "2026-03-11T02:10:00Z", "2027-12-07T22:45:00Z", P.SERVICE)


# ------------------------------------------------------------------ the registers
def dictionary(F):
    return f"""# Data dictionary

## {F["register"]}
The service's register of the plants it samples, one row per plant: plant_code; plant_name; serves (the towns the plant
serves); population_served (people served, the register's figure).

## {F["lab"]}
The {P.LAB}'s wastewater results, one row per sample, target and analysis run: sample_id; plant_code; composite_end
(the composite's end, local date and time); target (N1 or PMMoV); plate; analysed (the date the run was analysed);
result_gc_per_l (gene copies per litre of wastewater); status (accepted, rejected or check); composite_flow_m3 (the flow
on the chain-of-custody form, cubic metres); comment.

## {F["contract"]}
{CONTRACT_LAB}'s report of the composites it analysed during the laboratory's January closure, one row per sample and
analyte under a header that describes the method: lab ref; client site; sampled (the date the composite ended);
received; analyte; result; flow on the chain-of-custody form (cubic metres).

## {F["scada"]}
{P.WATER}'s inlet historian, one row per plant and hour: plant_code; timestamp_local (yyyy-mm-dd hh:mm, the start of
the hour); inlet_flow_m3h (cubic metres an hour); inlet_temperature_c (degrees Celsius).

## {F["study"]}
The paired upstream sampling study, one row per plant, visit, sampling point and replicate: plant_code; visit_date;
point (upstream, at the head of the trunk sewer, or plant); composite_start and composite_end (local time);
replicate (1 to 3); n1_copies_per_ml and pmmov_copies_per_ml (gene copies per millilitre); water_temperature_c (degrees
Celsius), ph and conductivity_us_cm (microsiemens per centimetre), read at the composite's collection.

## {F["dashboard"]}
The dashboard's export for winter 2027 on the levels it published: a sheet of each plant's weekly value, baseline,
level and band for the weeks of the winter, and a sheet of the alert episodes the desk checked.

## {F["rain"]}
Daily rainfall at six gauges: gauge; date_9am (the date at the end of the 24 hours to 9 am); rainfall_mm.

## {F["eqa"]}
The laboratory's returns in the national external quality assessment scheme: round, dispatch date, sample, analyte,
assigned value, the laboratory's result and its z-score.
"""


def contents(F):
    return f"""# Folder contents

Files gathered by the {P.SERVICE} surveillance team for the verification desk's winter 2028 rota.

- {F["request"]}: the wastewater surveillance coordinator's request.
- {F["methods"]}: the {P.DASHBOARD}'s methods note (version 4).
- {F["register"]}: the site register.
- {F["lab"]}: the {P.LAB}'s results export, composites of 8 January 2026 to 6 April 2028.
- {F["labnote"]}: notes on the results export.
- {F["contract"]}: the contract laboratory's report for the January 2028 closure.
- {F["scada"]}: {P.WATER}'s inlet historian export, 5 January 2026 to 9 April 2028.
- {F["scadanote"]}: {P.WATER}'s note on the export.
- {F["travel"]}: the network modeller's memo on travel times.
- {F["study"]}: the paired upstream sampling study's results, February 2026 to January 2027.
- {F["studyreport"]}: the paired upstream sampling study's field report.
- {F["dashboard"]}: the dashboard's export of its published levels and alert episodes, winter 2027.
- {F["rain"]}: daily rainfall at six gauges.
- {F["eqa"]}: the laboratory's external quality assessment returns, 2026 and 2027.
- {F["dict"]}: the fields of each data file.
"""


def write_all(target, F, R):
    p = lambda k: os.path.join(target, F[k])
    request(p("request"), F)
    methods(p("methods"), F)
    study_report(p("studyreport"), F)
    travel_memo(p("travel"), F, R.travel())
    scada_note(p("scadanote"), F, R)
    lab_note(p("labnote"), F)
    contract_report(p("contract"), R.contract_rows())
    lev, eps = R.dashboard()
    dashboard_workbook(p("dashboard"), lev, eps)
    eqa_workbook(p("eqa"), R.proficiency())
    with open(p("dict"), "w") as fh:
        fh.write(dictionary(F))
    with open(p("contents"), "w") as fh:
        fh.write(contents(F))
