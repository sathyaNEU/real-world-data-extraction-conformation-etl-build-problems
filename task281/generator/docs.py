"""The four governing documents, each in its issuer's own genre: the network's clinical AI governance standard, the
local validation study's protocol, the vendor's operating point guide and the reading center's 2027 agreement."""
import os

import params as P
from pack import write_pdf


def standard(path):
    b = [
        ("title", "Clinical AI Governance Standard CAI-03, version 3"),
        ("small", "%s. Clinical AI Oversight Committee. Approved 17 June 2026, effective 1 July 2026. Owner: Director "
                  "of Quality and Clinical AI. Supersedes version 2 (March 2025)." % P.ORG),
        ("h", "1. Purpose and scope"),
        ("p", "This standard governs the clinical AI tools in use at %s clinics. Section 3 applies to the autonomous "
              "diabetic retinal screening service (%s), under which a patient with diabetes is photographed at a "
              "primary care visit and the AI returns a result without a clinician reading the images." %
              (P.ORG_SHORT, P.PRODUCT)),
        ("h", "2. Definitions"),
        ("p", "<b>2.1 Reference year.</b> The twelve months from 1 October to 30 September that end before a contract "
              "year opens. A screening belongs to the reference year by the clinic's local calendar date of capture."),
        ("p", "<b>2.2 Clinic.</b> A %s primary care clinic offering AI screening. A screening belongs to the clinic "
              "where it was captured, whichever clinic is the patient's home clinic." % P.ORG_SHORT),
        ("p", "<b>2.3 Referable diabetic retinopathy.</b> Moderate non-proliferative diabetic retinopathy or worse, or "
              "diabetic macular edema, in either eye, as graded under the reference standard of the network's local "
              "validation study."),
        ("p", "<b>2.4 Sensitivity.</b> Of the screenings in which the patient has referable diabetic retinopathy, the "
              "share the AI refers. The AI refers a screening when it returns a Referable or an Ungradable result."),
        ("p", "<b>2.5 Operating point.</b> One of the vendor's published settings of the AI's referral threshold. A "
              "clinic runs a single operating point for the whole of a contract year."),
        ("p", "<b>2.6 Contract year.</b> The calendar year for which the reading center agreement and the vendor "
              "subscription are signed; for this cycle, 1 January to 31 December 2027."),
        ("h", "3. Autonomous retinal screening: operating points"),
        ("p", "<b>3.1</b> For each clinic, the operating point for the contract year is the least sensitive vendor "
              "operating point at which the AI's sensitivity for referable diabetic retinopathy among that clinic's "
              "reference-year screenings is at least 85 per cent. The estimate is compared with the floor as it "
              "stands; its precision is reported to the Committee separately."),
        ("p", "<b>3.2</b> The referrals the chosen operating points imply, counted on the reference year's screenings at "
              "every clinic, may not exceed the overread capacity in the reading center agreement for the contract "
              "year."),
        ("p", "<b>3.3</b> Where no vendor operating point meets 3.1 at a clinic, that clinic suspends autonomous "
              "screening for the contract year and every screening is sent for a reading center overread."),
        ("p", "<b>3.4</b> The Director of Quality and Clinical AI presents each clinic's operating point to the "
              "Committee by 1 December, with the evidence it rests on. Operating points are configured in the vendor "
              "portal before the contract year opens and are not changed during it."),
        ("h", "4. Monitoring"),
        ("p", "<b>4.1</b> Each quarter the Committee reviews the reading center's overreads of the AI's referrals "
              "from the screenings captured in the quarter before: by clinic, the referrals read and the share whose "
              "closing grade is Referable, and for the network the average calendar days from the screening's local "
              "date to the local date of the closing grade."),
        ("p", "<b>4.2</b> A camera fault is reported to Biomedical Engineering on the day it occurs. The Committee "
              "reviews, for each camera fault, the clinic days on which no AI screening was captured at the clinic "
              "because its camera was out of service."),
        ("small", "CAI-03 v3. Next review June 2027."),
    ]
    write_pdf(path, "Clinical AI Governance Standard CAI-03 v3", "%s Clinical AI Oversight Committee" % P.ORG_SHORT, b,
              stamp_date="D:20260617141500+00'00'")


def protocol(path):
    b = [
        ("title", "Local Validation of %s: Study Protocol" % P.PRODUCT),
        ("small", "Protocol CVCH-QI-2025-01, version 1.2, 6 January 2025. Principal investigator: %s, Director of "
                  "Quality and Clinical AI. Grading lead: %s, %s. Approved by the %s Quality Committee as a quality "
                  "improvement project." % (P.PEOPLE["quality"], P.PEOPLE["grader"], P.READING_CENTER, P.ORG_SHORT)),
        ("h", "1. Objective"),
        ("p", "To estimate, in the network's own patients, the sensitivity and specificity of %s for referable "
              "diabetic retinopathy against a reading center reference standard, at each of the vendor's operating "
              "points, before the service is extended beyond the pilot clinics." % P.PRODUCT),
        ("h", "2. Design and participants"),
        ("p", "Prospective, consecutive enrolment of adults with diabetes attending for AI screening at the three pilot "
              "clinics from 13 January to 27 June 2025. Patients already diagnosed with diabetic retinopathy are not "
              "eligible. Each participant is photographed once (two fields per eye, non-mydriatic) and the AI is run "
              "at the Standard operating point; the DR score is kept, so that the result at every other operating "
              "point can be derived from it."),
        ("table", [["Study site", "Clinic"], ["Site A", "Wendmere Primary Care"], ["Site B", "Quarry Hill"],
                   ["Site C", "Yarrowby Medical"]]),
        ("h", "3. Reference standard"),
        ("p", "Two certified graders at %s grade each participant's photographs independently, masked to the AI "
              "result, on the international clinical diabetic retinopathy severity scale (no DR, mild NPDR, moderate "
              "NPDR, severe NPDR, PDR) and for diabetic macular edema. Where the two graders differ on referability, "
              "a retina specialist adjudicates and the adjudicated level stands. Where they agree on referability "
              "but differ in level, the more severe level is recorded. Referable diabetic retinopathy is moderate "
              "NPDR or worse, or diabetic macular edema." % P.READING_CENTER),
        ("h", "4. Sample size"),
        ("p", "About 1,100 participants a site. At an expected 10 per cent prevalence of referable disease this "
              "gives about 330 referable participants, enough to estimate a sensitivity near 90 per cent to within "
              "about 3.5 percentage points (95 per cent confidence)."),
        ("h", "5. Analysis plan"),
        ("p", "Sensitivity and specificity with Wilson 95 per cent intervals at each operating point, overall and by "
              "site. Pre-specified subgroups: age group, sex, diabetes type, HbA1c group and ethnicity. An Ungradable "
              "AI result counts as a referral, as it does in service."),
        ("h", "6. Data handling"),
        ("p", "The study record holds no names or medical record numbers; each participant has a study identifier "
              "and the site letter. The record is kept by the Quality department for six years."),
    ]
    write_pdf(path, "RetinaCheck local validation protocol", "%s Quality Department" % P.ORG_SHORT, b,
              stamp_date="D:20250106102000+00'00'")


def opspec(path):
    rows = [["Operating point", "Refer at DR score", "Positioning"]]
    pos = {"Standard": "Default for new sites", "Enhanced": "More referrals than Standard",
           "High": "More referrals than Enhanced", "Maximum": "Highest referral volume"}
    for nm, cut in P.OPS:
        rows.append([nm, "%d or above" % cut, pos[nm]])
    b = [
        ("title", "%s Operating Points: Site Configuration Guide" % P.PRODUCT),
        ("small", "%s. Document KHS-RC-OP, revision C, for software 4.2 and 4.3. Customer Success." % P.VENDOR),
        ("h", "1. How a result is formed"),
        ("p", "For each screening, %s first checks the image quality of the photographs. If quality is too low to "
              "assess, the result is Ungradable and the patient should be referred. Otherwise the AI assigns a DR "
              "score from 0 to 100. The result is Referable when the score is at or above the threshold of the "
              "site's operating point, and Not referable when it is below." % P.PRODUCT),
        ("h", "2. Operating points"),
        ("table", rows),
        ("p", "A lower threshold refers more patients. Every result in the portal and in the result export carries its "
              "DR score, so the result a screening would have had at any other operating point can be read from its "
              "score. Scores from software 4.2 and 4.3 are on the same scale."),
        ("h", "3. Changing a site's operating point"),
        ("p", "A customer administrator changes the operating point in Portal, Sites, Settings. The change applies to "
              "screenings captured from the next local day. One operating point applies to a site at a time. The "
              "current configuration of every site can be exported from Portal, Sites, Export configuration."),
        ("h", "4. Result export"),
        ("p", "The result export lists every screening in the period selected, with timestamps in UTC."),
    ]
    write_pdf(path, "RetinaCheck operating points guide", P.VENDOR, b, stamp_date="D:20260402161000+00'00'")


def agreement(path):
    b = [
        ("title", "Overread Services Agreement, Contract Year 2027"),
        ("small", "Between %s and %s. Agreement PERC-CV-2027, signed 14 October 2026." % (P.READING_CENTER, P.ORG)),
        ("h", "1. Services"),
        ("p", "1.1 The Center overreads the photographs of every screening that %s refers at a %s clinic. "
              "The network places a referral order for each referred screening and the Center opens a case on it." %
              (P.PRODUCT, P.ORG_SHORT)),
        ("p", "1.2 The Center grades each case for diabetic retinopathy and diabetic macular edema and returns one of "
              "Referable, Not referable or Insufficient for grading. Where photographs are insufficient for grading, "
              "the Center asks the clinic for new photographs under the same referral and opens a new case for them. "
              "A referral is closed by a grade of Referable or Not referable."),
        ("p", "1.3 Target turnaround: five business days from receipt of the photographs to the grade."),
        ("h", "2. Capacity"),
        ("p", "2.1 The Center will overread up to 7,200 referrals in the contract year (1 January to 31 December "
              "2027). A referral counts once against capacity however many cases it takes to close."),
        ("p", "2.2 Referrals above capacity are read only as the Center's workload allows and without the turnaround "
              "target."),
        ("h", "3. Fees"),
        ("p", "3.1 USD 31.50 for each referral closed, invoiced monthly in arrears. No fee for a case that ends "
              "Insufficient for grading."),
        ("h", "4. Term"),
        ("p", "4.1 The agreement runs for the contract year and may be renewed by written agreement before 1 October "
              "2027."),
        ("small", "Signed for the Center: Medical Director. Signed for the network: Chief Medical Officer."),
    ]
    write_pdf(path, "Overread services agreement 2027", P.READING_CENTER, b, stamp_date="D:20261014093000+00'00'")


def write_all(out):
    standard(os.path.join(out, P.FILES["standard"]))
    protocol(os.path.join(out, P.FILES["protocol"]))
    opspec(os.path.join(out, P.FILES["opspec"]))
    agreement(os.path.join(out, P.FILES["agreement"]))
