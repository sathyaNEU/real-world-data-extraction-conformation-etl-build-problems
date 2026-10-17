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
        Paragraph("Revision 4, effective 01/06/2026. Supersedes revision 3. Parts 7 to 9 (training, "
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
                  "quarter hour where it carries the module. The meter stamps its records in UTC.", BODY),
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
                  "after it ends. Where the mean of a deployment's two field checks differs from the "
                  "calibrator's reference level by more than 0.3 dB, every level that deployment recorded "
                  "is corrected by subtracting that difference. A deployment whose checks differ from each "
                  "other by more than 1.0 dB is not used.", BODY),
        Paragraph("4.2 A minute is not valid where the met mast records rain above 0.5 mm an hour or wind "
                  "above 5 m a second for the ten minutes the minute falls in. Invalid minutes are left "
                  "out of every level.", BODY),
        Paragraph("4.3 A tone is prominent in a one-third-octave band where that band's level over the "
                  "assessment period exceeds the mean of the levels in the two adjacent bands by 5 dB or "
                  "more. The test is taken on the unweighted band levels.", BODY),
        Paragraph("5 Complaints", H2),
        Paragraph("5.1 Every noise complaint is logged in the complaints register with the dwelling it "
                  "came from, and the dwelling's reference is carried on the monitoring position "
                  "schedule. A complaint is a record of what a neighbour heard and is not a measurement.",
                  BODY),
        Paragraph("6 The mitigation programme", H2),
        Paragraph("6.1 The mitigation programme offers acoustic treatment to the dwellings the plant "
                  "contributes most sound to, taken in order of the specific sound level at the position, "
                  "highest first, as far as the quarter's slot with the acoustic contractor reaches. The "
                  "number of dwellings the slot covers is set when the slot is ordered.", BODY),
        Paragraph("6.2 Treatment is secondary glazing with acoustic trickle vents to the habitable rooms "
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

## What was measured

Fourteen positions, two deployments of a week each, from Monday 31 August to Sunday 11 October. Five
logging meters, moved on Monday mornings. Every position in the schedule was covered twice. The deployment
table says which meter stood where, with the mast height and the field checks either side.

## The meter files

`%(levels)s` is the five meters' own download, concatenated. One row a minute per meter, with the
A-weighted equivalent level for the minute and the statistical levels LA90, LAmax and LAmin from the same
minute. **The meters stamp in UTC**; the field sheets and everything the plant logs are in local time, which
was Irish Standard Time for the whole survey. The download of one deployment was repeated after the card
threw a read error on collection, so part of that day appears twice in the file; the remarks column in the
deployment table names it.

`%(bands)s` holds the one-third-octave band levels, one row a quarter hour, from the three meters that
carry the band module (%(band_serials)s). The band levels are unweighted. The other two meters log
broadband only, so the positions they stood at have no band rows.

## Calibration

`%(cal)s` carries the certificates and the field check each deployment started and finished with, against
the 94.0 dB calibrator. The plan says what to do where the checks sit away from the reference.

## The met mast

`%(weather)s` is the mast on the blower house roof, ten-minute means, stamped UTC. The anemometer was
replaced on 20 September; **the one fitted since reports in kilometres an hour, the one before it in metres a
second**, and the column was not renamed. The rain gauge reports its tip count since midnight, one tip to
0.2 mm, and the count resets at midnight rather than running on.

## The plant's own records

`%(events)s` is the process operator's equipment log in local time: a row whenever a blower, a centrifuge
or the gas engine was started or stopped, with the reason the shift wrote. `%(scada)s` is the
fifteen-minute channel log off the plant PLC, also local time. The biogas channel is the meter's own
counter and wraps at 99,999 m3; the engine's hour counter was replaced on 18 September and starts again
from zero; and the link to the PLC was down from the afternoon of 24 September to the morning of the 25th,
so there are no rows for that spell.

## Identities

Positions carry three names: the position code NSL01 to NSL14 in the schedule and in the meter paperwork,
the dwelling reference DW-1xx the complaints register uses, and whatever the crew wrote on the field sheet
("the cottage at the gable", "Glasha bridge"). The schedule maps all three.

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
