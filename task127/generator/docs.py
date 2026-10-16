"""The documents: the board's Winter Discharge Fund 2026/27 note, the notes that came with the three extracts, and
the System Flow team's data request log."""
import io

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate

import core
import postprocess as PP

GUIDANCE = [
    ("t", "Winter Discharge Fund 2026/27: discharge-to-assess packages"),
    ("s", "Allocation note SF-2026-14. Issued 28 September 2026 by Lauren Simpson, Head of System Flow, for the "
          "system coordination centre, the two acute trusts and Marchshire County Council."),
    ("h", "1. The fund"),
    ("p", "The board's winter discharge fund for 2026/27 buys 1,200 discharge-to-assess packages from the providers on "
          "Marchshire County Council's home care framework, under the council's call-off contract. The packages run "
          "from 1 December 2026 to 28 February 2027."),
    ("h", "2. What a package is"),
    ("p", "A discharge-to-assess package is up to four weeks of home care from a framework provider, available from "
          "the day a patient is medically optimised for discharge, so that waiting for a care provider to start does "
          "not keep the patient in hospital. The patient's longer-term care needs are assessed at home while the "
          "package runs, by the council's reablement and social work teams. Each package is used once, for one "
          "patient's discharge."),
    ("h", "3. Who the fund covers"),
    ("p", "Patients aged 65 and over discharged from Royal Marchford Hospital, Wendlebury Hospital, Ashby Vale "
          "Hospital, Cleeve Park Hospital or Holmford Infirmary on discharge pathway 1 who need a new package of home "
          "care to go home and who are registered with a general practice in Marchshire. A patient whose existing "
          "package of care restarts when they go home does not need a new package and is not covered."),
    ("h", "4. How the packages are split"),
    ("p", "The split is sized on last winter. For each hospital the board takes the patients the fund would have "
          "covered who were medically optimised for discharge from 1 December 2025 to 28 February 2026."),
    ("p", "Each hospital's packages are valued at the average, over those patients, of the number of nights by which "
          "a package would have shortened their stay."),
    ("p", "No hospital receives more packages than it had of those patients."),
    ("p", "The 1,200 packages are split between the hospitals to free as many occupied bed-days as possible. The "
          "occupied bed-days a hospital's packages free are its packages times their value; values are carried "
          "unrounded and the bed-days rounded to whole bed-days."),
    ("h", "5. Call-off and use"),
    ("p", "The board names each hospital's packages in the call-off to the framework providers by 30 October 2026. At "
          "each hospital, packages are offered to covered patients in the order they become medically optimised, "
          "until the hospital's packages are used. Packages a hospital has not used by 28 February 2027 lapse."),
    ("h", "6. Monitoring"),
    ("p", "The trusts report the packages used each week to the system coordination centre alongside the national "
          "discharge collection. The board reviews the split at the end of January 2027."),
]


def _styles():
    ss = getSampleStyleSheet()
    blue = colors.HexColor("#005EB8")
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.5, spaceAfter=7),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            spaceAfter=3, spaceBefore=6, textColor=blue),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=19,
                             spaceAfter=5),
        small=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=8.8, leading=11.5,
                             spaceAfter=12),
        lh=ParagraphStyle("lh", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=12,
                          textColor=blue, alignment=2),
        lh2=ParagraphStyle("lh2", parent=ss["Normal"], fontName="Helvetica", fontSize=8.5, leading=10.5,
                           textColor=blue, alignment=2, spaceAfter=16),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(2.0 * cm, 1.2 * cm, text)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def guidance_pdf(path):
    st = _styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.6 * cm,
                            bottomMargin=2.0 * cm, title="Winter Discharge Fund 2026/27: discharge-to-assess packages",
                            author="System Flow, NHS Marchshire ICB", creator="System Flow, NHS Marchshire ICB",
                            producer="System Flow, NHS Marchshire ICB")
    story = [Paragraph(core.ICB, st["lh"]), Paragraph("System Flow, Marchford House, 14 Castle Street, Marchford",
                                                      st["lh2"])]
    for kind, text in GUIDANCE:
        sty = {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"])
        story.append(Paragraph(text, sty))
    foot = _footer("Winter Discharge Fund 2026/27, allocation note SF-2026-14, 28 September 2026")
    doc.build(story, onFirstPage=foot, onLaterPages=foot)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, b"D:20260928101347+01'00'", "System Flow, NHS Marchshire ICB")


def guidance_text():
    return "\n".join(t for _, t in GUIDANCE)


def acute_notes():
    return """NHS Marchshire ICB data warehouse: acute discharges, patients aged 65 and over
Extract run 5 October 2026 07:40 for the System Flow team from the two trusts' monthly submissions.

acute_discharges_65plus_2024-12_2026-09.csv
One row per spell submission, for spells ending in a discharge from 1 December 2024 to 30 September 2026. A trust
that corrects a spell after submitting it submits the spell again under a new submission_id; the warehouse keeps
every submission.

submission_id          warehouse submission number
submitted_on           date the trust submitted the row
provider_code          RMC Marchshire Hospitals NHS Trust; RSM South Marches Healthcare NHS Foundation Trust
site_code              the site that discharged the patient (ward_reference.csv)
spell_number           the trust's hospital provider spell number
nhs_number             NHS number
local_patient_id       the trust's hospital number
age_on_admission       age in years
gp_practice_code       the practice the patient was registered with at admission
postcode_district      outward code of the patient's home postcode
admission_method       Emergency or Elective
admission_datetime     date and time of admission
discharge_ready_date   the date the patient was medically optimised for discharge (no longer met the criteria to
                       reside)
discharge_datetime     date and time the patient left hospital
discharge_destination  where the patient went
discharge_pathway      0 home with no new support; 1 home with care support; 2 rehabilitation or reablement bed;
                       3 care home
p1_care_package        pathway 1 only: New package, or Restart of existing package (the patient's care package from
                       before admission restarted)

Nights after the discharge ready date: a patient still in hospital at midnight after their discharge ready date
has spent a night in hospital after being ready to leave. The national discharge collection counts these nights
from the discharge ready date to the day of discharge and dates each night to the evening it begins. A patient
counts as delayed in a month when at least one of these nights is dated in that month.

acute_ward_stays_2024-12_2026-09.csv
One row per ward stay in the spells above: the ward the patient was on from ward_start to ward_end. A spell's ward
stays run from its admission to its discharge.

provider_code, spell_number   as in the discharges extract
ward_code                     ward_reference.csv
ward_start, ward_end          date and time the patient arrived on and left the ward

ward_reference.csv
The trusts' wards with their site, specialty and base beds.

Times are UK local time.
"""


def ices_notes():
    return """Marchshire Integrated Community Equipment Service (ICES): order lines
Export run 5 October 2026 for NHS Marchshire ICB. The service is run by Marchshire County Council for the council
and the ICB from two depots, North (Marchford) and South (Ashby). Severnside residents are served by Severnside's
own equipment service and are not in this export.

ices_order_lines_2024-12_2026-09.csv
One row per order line, for orders due for delivery from 1 December 2024 to 30 September 2026.

order_no            order reference; the lines of one order share it
line_no             line within the order
nhs_number          as recorded by the prescriber
delivery_postcode   address the items go to
item                equipment item
route               who prescribed the order: Hospital discharge (a hospital ward or discharge team, for
                    equipment the patient needs at home from the day they go home), Community nursing,
                    Occupational therapy, Reablement, Physiotherapy
ordered_date        date the order was placed
required_by         date the prescriber asked for delivery by
delivered_date      date the item was delivered (blank if it was not)
collected_date      date the item was collected back (blank if it was not)
depot               North or South
status              Ordered (not yet delivered), Delivered, Collected or Cancelled
"""


def council_notes():
    return """Marchshire County Council: extracts for NHS Marchshire ICB (System Flow), 5 October 2026

brokerage_referrals_2024-12_2026-09.csv
One row per referral for home care the brokerage team handled from 1 December 2024 to 30 September 2026. Referrals
for patients in hospital come from the wards and discharge teams; the rest come from the community.

referral_no      brokerage referral number
received_at      date and time the brokerage received the referral
source           Hospital discharge, GP practice, District nursing, Family or carer, Self-referral, Adult social care
                 team
referring_site   for a hospital referral, the hospital
person_id        council person identifier
nhs_number       as held on the person's record; not always recorded for community referrals
care_postcode    postcode of the address where care is to be delivered, as entered on the referral
status           Started (the provider started the package), Open (a provider has taken the package and care has
                 not yet started), Closed (the brokerage closed the referral), Cancelled (the referrer withdrew the
                 referral)
provider         the framework provider that took the package
start_date       date the provider's care started; for a hospital referral, the day the patient went home

The brokerage reports its referrals by the month they were received and measures the wait for care in calendar
days from the date a referral was received to the date care started.

spot_care_invoice_lines_2025-26.csv
Finance (Unit4) extract: invoice lines for home care bought from providers outside the home care framework (spot
purchases), invoiced weekly, April 2025 to March 2026. Dates are dd/mm/yyyy.

invoice_no      supplier invoice number
supplier        the spot provider
brokerage_ref   the brokerage referral the purchase was made for
client_id       council person identifier
service_start   the day care started under the purchase; where care was suspended and resumed, the lines
                after the break carry the day it resumed
week_ending     the week the line invoices (weeks end on Sunday)
hours           hours of care delivered in the week
rate            hourly rate in pounds
amount          hours times rate, in pounds

postcode_districts_marchshire.csv
The council's postcode lookup: every unit postcode in Marchshire with its electoral ward and district.
"""


LOG_HEAD = ["file", "supplied_by", "extract_run", "covers", "notes"]


def log_rows(files, counts):
    return [
        [files["spells"], "NHS Marchshire ICB data warehouse", "2026-10-05",
         "Discharges 1 Dec 2024 to 30 Sep 2026, patients 65 and over, both trusts",
         "%s rows; resubmitted spells kept as submitted" % format(counts["spells"], ",")],
        [files["wards"], "NHS Marchshire ICB data warehouse", "2026-10-05", "Ward stays of the same spells",
         "%s rows" % format(counts["wards"], ",")],
        [files["wardref"], "Marchshire Hospitals NHS Trust; South Marches Healthcare NHS FT", "2026-09-30",
         "Wards at the five acute sites", ""],
        [files["acute_notes"], "NHS Marchshire ICB data warehouse", "2026-10-05", "Field notes for the two extracts",
         ""],
        [files["practices"], "NHS Marchshire ICB primary care team", "2026-09-30",
         "GP practices of Marchshire and Severnside ICBs, with practices closed by merger since 2024", ""],
        [files["ices"], "Marchshire ICES (Marchshire County Council)", "2026-10-05",
         "Orders due for delivery 1 Dec 2024 to 30 Sep 2026", "%s rows" % format(counts["ices"], ",")],
        [files["ices_notes"], "Marchshire ICES (Marchshire County Council)", "2026-10-05", "Field notes", ""],
        [files["brokerage"], "Marchshire County Council, brokerage team", "2026-10-05",
         "Referrals handled 1 Dec 2024 to 30 Sep 2026", "%s rows" % format(counts["brokerage"], ",")],
        [files["spot"], "Marchshire County Council, finance", "2026-10-05", "Invoice lines April 2025 to March 2026",
         "%s rows" % format(counts["spot"], ",")],
        [files["postcodes"], "Marchshire County Council, information team", "2026-09-30", "Marchshire unit postcodes",
         ""],
        [files["council_notes"], "Marchshire County Council", "2026-10-05", "Field notes for the council extracts", ""],
        [files["guidance"], "NHS Marchshire ICB, System Flow", "2026-09-28", "Allocation note SF-2026-14", ""],
        [files["weekly"], "NHS Marchshire ICB data warehouse", "2026-10-05",
         "National discharge collection as submitted by the two trusts, weeks ending 8 Dec 2024 to 27 Sep 2026", ""],
        [files["census"], "System coordination centre", "2026-10-02", "Daily bed state, 1 Dec 2024 to 30 Sep 2026", ""],
        [files["reablement"], "Marchshire County Council, adult social care performance", "2026-08-14",
         "Reablement outcomes by quarter, Oct 2024 to Mar 2026", ""],
    ]
