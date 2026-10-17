"""The site's noise management plan, and the monitoring technician's notes on the survey."""
import os

from reportlab import rl_config
rl_config.invariant = 1
rl_config.useA85 = 0
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack as PK
import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)


def plan(target):
    path = os.path.join(target, PK.FILES["plan"])
    d = SimpleDocTemplate(path, pagesize=A4, title="Noise management plan", author="", subject="",
                          creator="", leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                          bottomMargin=18 * mm)
    f = [
        Paragraph("%s %s: noise management plan" % (W.OPERATOR, W.SITE), H1),
        Paragraph("Revision 4, effective 01/06/2026. Supersedes revision 3. Parts 8 to 10 (training, "
                  "records retention, review) are not reproduced in this extract.", SMALL),
        Paragraph("1 Purpose and scope", H2),
        Paragraph("1.1 This plan sets out how the site measures and manages the sound its plant makes at "
                  "the dwellings around it, and how the site decides where to spend the mitigation "
                  "programme.", BODY),
        Paragraph("1.2 The plan covers sound. Odour, dust and discharges are managed under their own "
                  "plans and are outside it.", BODY),
        Paragraph("2 Monitoring positions and surveys", H2),
        Paragraph("2.1 Monitoring is carried out at the positions listed in the monitoring position "
                  "schedule the environmental engineer holds. A position is one dwelling. Positions are "
                  "added to the schedule when a dwelling is named in a complaint or when the site judges "
                  "a dwelling to be exposed.", BODY),
        Paragraph("2.2 A survey places a logging sound level meter at each position for two deployments of "
                  "one week. A meter logs the A-weighted equivalent continuous sound level and the "
                  "statistical levels for every minute, and the one-third-octave band levels for every "
                  "quarter hour where it carries the module. The meter stamps its records in UTC, each "
                  "record at the start of the interval it measures.", BODY),
        Paragraph("3 The specific sound level", H2),
        Paragraph("3.1 The specific sound level of the plant at a position is the position's measured "
                  "sound level over the assessment period, less the residual sound, both in dB LAeq. The "
                  "measured sound level is the energy-equivalent level of the position's valid minutes in "
                  "the assessment period. The residual sound is the sound at the position from sources "
                  "other than the plant. Levels are combined and subtracted in energy, not in decibels.",
                  BODY),
        Paragraph("3.2 The assessment period is 07:00 to 19:00 on weekdays, in local time.", BODY),
        Paragraph("3.3 The environmental engineer determines the specific sound level at each position in "
                  "the schedule and reports it to one decimal place.", BODY),
        Paragraph("4 Measurement conditions", H2),
        Paragraph("4.1 Each deployment is checked against the acoustic calibrator before it starts and "
                  "after it ends. A deployment's deviation is the mean of its two field checks less the "
                  "calibrator's reference level. Where that deviation is more than 0.3 dB away from zero, "
                  "every level the deployment recorded is corrected by taking the deviation off it. A "
                  "deployment whose two checks differ from each other by more than 1.0 dB is not used.",
                  BODY),
        Paragraph("4.2 A minute is not valid where the met mast's record for the ten minutes the minute "
                  "falls in counted rain on the gauge or shows wind above 5 m a second, or where the "
                  "meter recorded no measurement for that minute. Invalid minutes are left out of every "
                  "level.", BODY),
        Paragraph("4.3 A tone is prominent in a one-third-octave band where that band's level over the "
                  "assessment period exceeds the mean of the levels in the two adjacent bands by 5 dB or "
                  "more. A band's level over the assessment period is the energy-equivalent level of its "
                  "quarter-hour records in that period, both deployments together. The test is taken on "
                  "the unweighted band levels.", BODY),
        Paragraph("5 Process records", H2),
        Paragraph("5.1 The plant's figures for a week are read from the process meters' own counters: the "
                  "counter reading stamped at 00:00 on the Monday the week begins, taken from the reading "
                  "stamped at 00:00 on the Monday after it, with the counter's roll-over added back where "
                  "it has passed it. A spell the historian did not record leaves those two readings as "
                  "they stand.", BODY),
        Paragraph("5.2 A centrifuge run is one start of a centrifuge in the equipment log and the first "
                  "stop the log records for the same machine after it. A start the log does not stop "
                  "before that machine starts again is not a run. A week's runs are the runs that start "
                  "in that week.", BODY),
        Paragraph("6 Complaints", H2),
        Paragraph("6.1 Every noise complaint is logged in the complaints register with the dwelling it "
                  "came from, and the dwelling's reference is carried on the monitoring position "
                  "schedule. A complaint is a record of what a neighbour heard and is not a measurement.",
                  BODY),
        Paragraph("7 The mitigation programme", H2),
        Paragraph("7.1 The mitigation programme offers acoustic treatment to the dwellings the plant "
                  "contributes most sound to, taken in order of the specific sound level at the position, "
                  "highest first, as far as the quarter's slot with the acoustic contractor reaches. The "
                  "number of dwellings the slot covers is set when the slot is ordered.", BODY),
        Paragraph("7.2 Treatment is secondary glazing with acoustic trickle vents to the habitable rooms "
                  "facing the plant, or a close-boarded screen where the site and the occupier agree one.",
                  BODY),
        Paragraph("Revision history: 1 (14/08/2019), 2 (02/11/2021), 3 (19/05/2024), 4 (01/06/2026), "
                  "issued after the effluent plant upgrade entered service.", SMALL),
    ]
    d.build(f)
    return path


NOTES = """# Drumlorne noise survey, autumn 2026: monitoring notes

%(tech)s, monitoring technician. Written up 12 October 2026, with the folder handed to the environmental
engineer on 16 October.

## How it went

Fourteen positions, two deployments of a week each, from Monday 31 August to the collection round on
Monday 12 October. Five logging meters, lifted and set down again on the Monday mornings, one round for
the five of them, starting between half four and five and finishing before the works woke up. Every
position in the schedule was covered twice. The deployment table says which meter stood where, when it was
set running and stopped, the height it stood at and the field checks either side.

Mounting was free field on a tripod, 3.5 m off the facade where there was room for it. At NSL08 the cattle
were in the field the first week and the tripod had to go three metres west of the pegged spot; at NSL13
the garden wall was being rebuilt in the second week and the mic came down to 1.2 m to clear the scaffold.
Both are on the deployment record.

## Access

NSL03, NSL05 and NSL12 are through the farm yards and the occupiers hold the gate keys; ring ahead. The
dog at NSL09 is loose in the yard most days. NSL10 is up the lane past the quarry entrance and the lane is
not passable in the dark after rain. Nobody minded the tripod once they had seen it.

## Weather

A wet first fortnight: showers most afternoons in the first week and a wet Thursday in the second. It
blew hard from the Tuesday of the third week to the Friday, 20 to 35 km an hour at the mast most of those
days, and the last fortnight was settled and cool. The mast on the blower house roof logs the wind, the
rain gauge and the air temperature, and the anemometer was replaced on 20 September after the old one
started sticking.

## What went wrong

The card in one meter threw a read error when it was collected and the download was repeated to get it
off, so part of that day came through twice. One logger reset itself mid-week and wrote nothing until the
mid-week visit, and two meters dropped their measurement channel for half an hour each. All of it is on
the deployment record.

On the plant side the radio link from the PLC to the historian dropped several times over the survey, the
longest spell from the Friday evening of the fourth week to the Saturday afternoon. When that link goes
the interface writes nothing for a while, and sometimes it writes the last value it had again until the
link is back.

## Also in the folder

The complaints register for 2026, and the final effluent monitoring results for the same period. Neither
was collected for this survey.
"""


def notes(target):
    path = os.path.join(target, PK.FILES["notes"])
    txt = NOTES % {
        "tech": W.PEOPLE["technician"][0],
        "levels": PK.FILES["levels"], "bands": PK.FILES["bands"], "cal": PK.FILES["calibration"],
        "weather": PK.FILES["weather"], "events": PK.FILES["events"], "scada": PK.FILES["scada"],
        "band_serials": ", ".join(m["serial"] for m in W.METERS if m["bands"]),
    }
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return path
