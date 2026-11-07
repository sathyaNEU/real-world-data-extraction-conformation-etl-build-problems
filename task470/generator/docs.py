"""The two governing documents: the ministry's regulation for the 2027 grant (the population, what vacant means, the
fortnight, the share and the threshold, the certification) and the ministry's assignment to the statistics office
(the certification's deadline and the two annex tables the ministry wants for its follow-up)."""
import datetime as dt
import email.message
import email.utils

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

import world as W

SECTIONS = [
    ("Section 1. Purpose",
     "The grant helps municipalities where many dwellings stand empty to bring them back into use. This regulation "
     "governs the pilot in %s county for 2027." % W.COUNTY),
    ("Section 2. Municipalities",
     "The pilot covers the ten municipalities of %s county as they stood on 1 January 2026." % W.COUNTY),
    ("Section 3. The dwellings counted",
     "The dwellings counted in a municipality are the dwelling units the cadastre (matrikkelen) registers in the "
     "municipality with the unit type Bolig and a date of taking into use on or before 1 November 2026. Holiday homes, "
     "units of any other type and dwellings not taken into use by that date are not counted."),
    ("Section 4. Vacant dwellings",
     "A counted dwelling is vacant when nobody lived in it on any day of the reference fortnight, 9 to 22 November "
     "2026. Whether anyone was registered as resident in the dwelling in the population register does "
     "not decide whether it was vacant."),
    ("Section 5. Evidence",
     "The national statistics office establishes for each counted dwelling whether it was vacant from the "
     "metered electricity values the meter data hub holds for the dwelling's metering points in the reference "
     "fortnight, read with the cadastre."),
    ("Section 6. Vacancy share and qualification",
     "A municipality's vacancy share is the number of its counted dwellings that were vacant as a percentage of the "
     "number of its counted dwellings, rounded to one decimal. A municipality qualifies for the grant when its vacancy "
     "share is 5.0 per cent or more."),
    ("Section 7. Certification",
     "By 15 January 2027 the office sends the ministry a certification letter naming the qualifying municipalities and "
     "giving each municipality's vacant dwellings and vacancy share, with a chart of the shares against the threshold "
     "in Section 6, together with a file listing each counted dwelling and whether it was vacant."),
    ("Section 8. Payment",
     "Each qualifying municipality receives NOK 40,000 for each of its vacant counted dwellings. The ministry pays the "
     "grant in March 2027 on the certified figures."),
    ("Section 9. Entry into force",
     "This regulation enters into force on 15 October 2026."),
]


def write_regulation(path):
    st_t = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=4)
    st_s = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor="#444444", spaceAfter=10)
    st_h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=3)
    st_p = ParagraphStyle("p", fontName="Helvetica", fontSize=10, leading=14, alignment=TA_LEFT)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=22 * mm,
                            bottomMargin=20 * mm, title="Regulation on the 2027 vacant dwelling activation grant",
                            author=W.MINISTRY, subject="Pilot, %s county" % W.COUNTY, creator=W.MINISTRY,
                            producer=W.MINISTRY, invariant=1)
    story = [Paragraph("Regulation on the 2027 grant for activating vacant dwellings, pilot in %s county" % W.COUNTY,
                       st_t),
             Paragraph("Laid down by the %s on 14 October 2026 under the Act on state grants to municipalities, "
                       "section 4." % W.MINISTRY, st_s)]
    for h, p in SECTIONS:
        story += [Paragraph(h, st_h), Paragraph(p, st_p)]
    story.append(Spacer(1, 10))
    doc.build(story)


def regulation_text():
    return " ".join("%s %s" % (h, p) for h, p in SECTIONS)


ASSIGNMENT = (
    "Dear %s,\n\n"
    "Under Section 7 of the regulation on the 2027 grant for activating vacant dwellings, please send the ministry the "
    "certification for the %s pilot by 15 January 2027.\n\n"
    "For our follow-up of the pilot we would also like two tables in the certification letter. For each municipality, "
    "the persons the population register held as resident in its counted dwellings on 1 November 2026, by their age "
    "on that day: under 18, 18 to 66, and 67 and over. And for each municipality, how many of its counted dwellings "
    "were held on the land register on 1 November 2026 by the municipality or by a company the municipality owns; by "
    "a company the municipality owns we mean, as in the ministry's register of municipal companies, a municipal "
    "enterprise of the municipality or a company in which the municipality holds all the shares, itself or through "
    "such a company.\n\n"
    "Best regards,\n%s\n%s\n%s\n")


def write_assignment(path):
    m = email.message.EmailMessage()
    sh, mi = W.PEOPLE["section_head"], W.PEOPLE["ministry"]
    m["From"] = "%s <%s>" % (mi[0], "eirik.haug@kdd.dep.example")
    m["To"] = "%s <%s>" % (sh[0], "martine.strom@statoffice.example")
    m["Subject"] = "Certification for the 2027 vacant dwelling grant, %s pilot" % W.COUNTY
    m["Date"] = email.utils.format_datetime(dt.datetime(2026, 12, 1, 10, 42, tzinfo=dt.timezone(dt.timedelta(hours=1))))
    m["Message-ID"] = "<20261201094211.4470@kdd.dep.example>"
    m.set_content(ASSIGNMENT % (sh[0].split()[0], W.COUNTY, mi[0], mi[1], W.MINISTRY))
    with open(path, "wb") as fh:
        fh.write(bytes(m))


def assignment_text():
    sh, mi = W.PEOPLE["section_head"], W.PEOPLE["ministry"]
    return ASSIGNMENT % (sh[0].split()[0], W.COUNTY, mi[0], mi[1], W.MINISTRY)
