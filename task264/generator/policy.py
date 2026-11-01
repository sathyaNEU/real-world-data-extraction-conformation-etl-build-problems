"""The board's contracting policy (the governing document): the estimand and the reporting definitions,
in the board's own voice. Two pages and two appendices."""
from io_util import write_pdf, esc
from common import BOARD, CASEMIX

BODY = [
    ("t", "Elective spinal surgery: placing the 2027-28 additional lumbar activity"),
    ("s", "%s | Contracting policy | Version 1.0, approved by the Planned Care Committee on 17 September 2026 | "
          "Owner: Director of Planned Care | Review due September 2027" % BOARD),
    ("h", "1. Purpose"),
    ("p", "The board will commission 1,250 additional elective lumbar decompression and discectomy operations for its "
          "residents in 2027-28, on top of each provider's baseline contract. This policy sets how that volume is placed "
          "with providers, on the outcomes their patients reported after the same operations in 2023-24 and 2024-25, and "
          "how the board reports the waiting list and questionnaire participation that sit beside the placement in its "
          "board paper."),
    ("h", "2. Index operations"),
    ("p", "An index operation is an elective admission (admission method 11, 12 or 13) whose primary procedure is in "
          "Appendix A, for a patient who had no Appendix A procedure in the 365 days before it. It is dated by the day of "
          "the procedure and belongs to the hospital that carried it out; a hospital that has changed owner or code is the "
          "same provider throughout. Where a spell has been submitted more than once, its latest submission stands."),
    ("h", "3. The outcome measure"),
    ("p", "A provider's outcome is the case-mix adjusted mean change in the Oswestry Disability Index (ODI) between the "
          "pre-operative questionnaire and the 12-month questionnaire, over every eligible index operation the provider "
          "carried out from 1 April 2023 to 31 March 2025, whether or not the patient returned the 12-month questionnaire. "
          "An index operation is eligible when the patient completed a scored pre-operative questionnaire in the 90 days "
          "up to and including the day of the operation and was alive 12 months after it."),
    ("p", "The change is the pre-operative score minus the 12-month score, so a fall in disability is a positive change. "
          "The 12-month questionnaire is the one the patient completed from 48 to 64 weeks after the day of the operation."),
    ("p", "Each of the ten ODI sections is scored from 0 to 5. A questionnaire is scored when at least eight sections are "
          "answered; its score is the total of the answered sections divided by five times the number answered, "
          "multiplied by 100."),
    ("p", "The case-mix adjusted mean is the mean expected change over the eligible index operations of all providers, "
          "plus the provider's mean of the observed change minus the expected change. The expected change for an "
          "operation comes from the model in Appendix B."),
    ("h", "4. Placing the 2027-28 volume"),
    ("p", "A provider whose outcome is at least 14.5 points is offered volume. Offers are made in descending order of "
          "outcome, each up to the additional operations the provider offered in its 2027-28 capacity return, until the "
          "1,250 operations are placed. A provider below 14.5 points is not offered volume in 2027-28, and volume not "
          "placed is held for in-year commissioning."),
    ("h", "5. Waiting list reporting"),
    ("p", "The board reports each provider's lumbar decompression and discectomy waiting list on the last day of the "
          "month under the national referral to treatment rules. A patient's clock starts on the day the board's "
          "musculoskeletal triage service received the referral, where the patient was referred through it, and "
          "otherwise on the day the provider received the referral; the clock keeps running when the board moves a "
          "patient's care to another provider. A patient is counted once, at the provider responsible for their care on "
          "that day. A wait is the number of days from the clock start to the reporting day; a wait of more than 364 days is "
          "reported as more than 52 weeks, and a wait of 126 days or fewer as within 18 weeks."),
    ("h", "6. Pre-operative questionnaire participation"),
    ("p", "A provider's participation for a financial year is the share of its index operations in that year whose "
          "patient completed a scored pre-operative questionnaire in the 90 days up to and including the day of the "
          "operation."),
    ("h", "Appendix A. Index procedures (OPCS-4)"),
    ("table", [["Code", "Procedure"],
               ["V25.3", "Primary posterior laminectomy decompression of lumbar spine"],
               ["V25.4", "Primary posterior decompression of lumbar spine NEC"],
               ["V25.5", "Primary lateral foraminotomy of lumbar spine"],
               ["V25.6", "Primary lateral recess decompression of lumbar spine"],
               ["V33.1", "Primary laminectomy excision of lumbar intervertebral disc"],
               ["V33.2", "Primary fenestration excision of lumbar intervertebral disc"],
               ["V33.7", "Primary microdiscectomy of lumbar intervertebral disc"]]),
    ("h", "Appendix B. Expected 12-month change in ODI points"),
    ("table", [["Term", "Points"],
               ["Constant", "%.1f" % CASEMIX["intercept"]],
               ["Per point of pre-operative ODI score, measured from 45", "%+.2f" % CASEMIX["pre_odi_minus_45"]],
               ["Per year of age on admission, measured from 55", "%+.2f" % CASEMIX["age_minus_55"]],
               ["Female", "%+.1f" % CASEMIX["female"]],
               ["Current smoker", "%+.1f" % CASEMIX["smoker"]],
               ["Previous lumbar spinal surgery", "%+.1f" % CASEMIX["previous_lumbar_surgery"]],
               ["Symptoms for more than 12 months", "%+.1f" % CASEMIX["symptoms_over_12_months"]],
               ["Disc herniation (primary diagnosis M51.1 or M51.2)", "%+.1f" % CASEMIX["disc_herniation"]]]),
    ("p", "Smoking, previous surgery and symptom duration are taken from the pre-operative questionnaire; age, sex and "
          "primary diagnosis from the hospital record of the index operation."),
]


def write_policy(path):
    write_pdf(path, "Elective spinal surgery contracting policy 2027-28", BOARD, "Microsoft Word for Microsoft 365",
              BODY, "%s | Elective spinal contracting policy 2027-28 | Version 1.0" % BOARD,
              "D:20260917142200+01'00'", "D:20260917142200+01'00'")
