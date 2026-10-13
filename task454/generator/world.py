"""The fixed world of task454: an unnamed US state's Medicaid fee-for-service pharmacy program. Its claims are processed
by a contracted pharmacy benefit administrator, which also keeps the State Maximum Allowable Cost (SMAC) list and
proposes one drug class a year for it. The State pays the ingredient at the lesser of the usual and customary charge,
the State actual acquisition cost (AAC) rate in effect for the NDC or, where no rate is in effect, the WAC, plus a
professional dispensing fee. A survey contractor sets the AAC rates monthly from the invoices sampled community
pharmacies submit; the long-term care pharmacies that dispense unit-dose cartons are not sampled, so most carton NDCs
carry no rate and are paid at WAC, and a carton costs more per unit than the retail bottle of the same product."""
import datetime as dt

SEED = 4541009
ADMIN = "Corvane Pharmacy Solutions"
SURVEY = "Halvering Pratt Survey Services"
DEPARTMENT = "Department of Health Coverage"
PROGRAM = "State Medicaid Pharmacy Program"
PEOPLE = {"director": "Sonya Burton", "account": "Todd Allen", "pricing": "Carrie Arellano", "survey": "Jeff Strickland"}

WINDOW = (dt.date(2026, 4, 1), dt.date(2027, 3, 31))
PRIOR = (dt.date(2025, 4, 1), dt.date(2026, 3, 31))
EXTRACT_DATE = dt.date(2027, 4, 21)
PAID_THROUGH = dt.date(2027, 4, 20)
EXTRACT_FROM = dt.date(2026, 4, 1)           # the extract's first paid date
SUMMARY_PAID_THROUGH = dt.date(2026, 4, 20)  # the FY2026 summary's last paid date
# claims pharmacies submit long after the fill (retroactive eligibility, a rebill after a rejection): the share of
# paid claims and the lag in days
LATE_SHARE = 0.021
LATE_LAG = (30, 200)
REVISION_DATE = dt.date(2027, 1, 1)          # the State's class list revision
SUMMARY_DATE = dt.date(2026, 4, 24)          # the administrator's FY2026 utilization summary
REQUEST_DATE = dt.date(2027, 3, 8)
PROPOSAL_DUE = dt.date(2027, 5, 3)
UPDATE_DATE = dt.date(2027, 7, 1)
FEE = {"retail": 10.64, "ltc": 12.31}

# a carton costs more per unit than the retail bottle of the same product (product by product, about this much)
UD_PREMIUM = 1.9
# product to product the premium varies little (repackagers price off the same bottles), and labelers of one
# product and package sell within a narrow band
PREMIUM_SD = 0.005
LABELER_SD = 0.006
# the WAC over acquisition cost: a new entrant's bottles, and the unit-dose cartons
W_NEW = (2.6, 3.2)
W_UD = (1.32, 1.44)

# the twelve shortlisted classes, as the class list in force from 1 January 2027 defines them. Each product:
# (generic name, strength, dosage form, pricing unit, acquisition per unit of the retail bottle in April 2026,
#  units dispensed in the window (thousands, before the class scale), share dispensed by long-term care pharmacies,
#  share of the retail bottles' units on a new entrant's NDCs not yet priced, yearly price drift)
SHORTLIST = [
    ("Anticonvulsants", [
        ("levetiracetam", "500 mg", "tablet", "EA", 0.061, 3000, 0.08, 0.02, -0.03),
        ("levetiracetam", "750 mg", "tablet", "EA", 0.088, 1100, 0.07, 0.02, -0.03),
        ("levetiracetam", "100 mg/mL", "oral solution", "ML", 0.019, 3000, 0.12, 0.00, -0.02),
        ("lamotrigine", "100 mg", "tablet", "EA", 0.043, 1500, 0.05, 0.03, -0.04),
        ("topiramate", "50 mg", "tablet", "EA", 0.041, 1200, 0.05, 0.02, -0.02),
        ("oxcarbazepine", "300 mg", "tablet", "EA", 0.21, 600, 0.06, 0.05, -0.05),
        ("lacosamide", "100 mg", "tablet", "EA", 0.38, 260, 0.05, 0.62, -0.05),
        ("lacosamide", "150 mg", "tablet", "EA", 0.47, 120, 0.05, 0.58, -0.05),
        ("lacosamide", "200 mg", "tablet", "EA", 0.55, 200, 0.05, 0.60, -0.05),
        ("divalproex sodium", "500 mg", "delayed-release tablet", "EA", 0.16, 1000, 0.10, 0.03, -0.02),
        ("clonazepam", "0.5 mg", "tablet", "EA", 0.021, 1800, 0.10, 0.02, -0.01),
    ]),
    ("Antipsychotics", [
        ("clozapine", "100 mg", "tablet", "EA", 0.42, 700, 0.55, 0.03, -0.02),
        ("quetiapine fumarate", "25 mg", "tablet", "EA", 0.034, 2600, 0.62, 0.02, -0.02),
        ("quetiapine fumarate", "100 mg", "tablet", "EA", 0.058, 2200, 0.55, 0.02, -0.02),
        ("quetiapine fumarate", "300 mg", "extended-release tablet", "EA", 0.36, 500, 0.45, 0.04, -0.04),
        ("risperidone", "0.5 mg", "tablet", "EA", 0.036, 1800, 0.66, 0.02, -0.01),
        ("risperidone", "1 mg", "tablet", "EA", 0.041, 1400, 0.58, 0.02, -0.01),
        ("risperidone", "1 mg/mL", "oral solution", "ML", 0.29, 150, 0.70, 0.00, -0.02),
        ("olanzapine", "5 mg", "tablet", "EA", 0.072, 1600, 0.52, 0.02, -0.02),
        ("olanzapine", "10 mg", "tablet", "EA", 0.10, 1000, 0.48, 0.02, -0.02),
        ("aripiprazole", "5 mg", "tablet", "EA", 0.081, 1400, 0.40, 0.03, -0.03),
        ("paliperidone", "6 mg", "extended-release tablet", "EA", 1.55, 120, 0.45, 0.03, -0.06),
        ("haloperidol", "5 mg", "tablet", "EA", 0.09, 500, 0.60, 0.02, -0.01),
    ]),
    ("Dementia agents", [
        ("donepezil", "5 mg", "tablet", "EA", 0.052, 900, 0.78, 0.02, -0.01),
        ("donepezil", "10 mg", "tablet", "EA", 0.066, 1300, 0.80, 0.02, -0.01),
        ("memantine", "10 mg", "tablet", "EA", 0.11, 1100, 0.76, 0.03, -0.02),
        ("memantine", "2 mg/mL", "oral solution", "ML", 0.21, 200, 0.85, 0.00, -0.02),
        ("galantamine", "8 mg", "tablet", "EA", 0.42, 150, 0.70, 0.04, -0.03),
        ("rivastigmine", "3 mg", "capsule", "EA", 0.58, 160, 0.72, 0.04, -0.03),
    ]),
    ("Antidepressants, SSRI", [
        ("sertraline", "50 mg", "tablet", "EA", 0.018, 3200, 0.12, 0.03, -0.02),
        ("sertraline", "20 mg/mL", "oral concentrate", "ML", 0.12, 300, 0.30, 0.00, -0.02),
        ("citalopram", "20 mg", "tablet", "EA", 0.022, 2600, 0.14, 0.03, -0.02),
        ("escitalopram", "10 mg", "tablet", "EA", 0.025, 2100, 0.10, 0.02, -0.02),
        ("fluoxetine", "20 mg", "capsule", "EA", 0.03, 1500, 0.08, 0.04, -0.02),
        ("fluvoxamine", "100 mg", "tablet", "EA", 0.29, 260, 0.10, 0.05, -0.03),
    ]),
    ("Beta blockers", [
        ("metoprolol tartrate", "25 mg", "tablet", "EA", 0.016, 3600, 0.24, 0.03, -0.01),
        ("metoprolol succinate", "50 mg", "extended-release tablet", "EA", 0.11, 2500, 0.18, 0.04, -0.03),
        ("carvedilol", "6.25 mg", "tablet", "EA", 0.019, 2200, 0.24, 0.03, -0.01),
        ("propranolol", "20 mg/5 mL", "oral solution", "ML", 0.09, 300, 0.20, 0.00, -0.02),
        ("atenolol", "25 mg", "tablet", "EA", 0.024, 1400, 0.20, 0.03, -0.01),
    ]),
    ("Loop diuretics", [
        ("furosemide", "20 mg", "tablet", "EA", 0.014, 3000, 0.42, 0.03, -0.01),
        ("furosemide", "40 mg", "tablet", "EA", 0.021, 2600, 0.40, 0.03, -0.01),
        ("furosemide", "10 mg/mL", "oral solution", "ML", 0.046, 800, 0.55, 0.00, -0.02),
        ("bumetanide", "1 mg", "tablet", "EA", 0.12, 700, 0.40, 0.04, -0.02),
        ("torsemide", "20 mg", "tablet", "EA", 0.16, 500, 0.35, 0.05, -0.03),
    ]),
    ("Benzodiazepines", [
        ("lorazepam", "0.5 mg", "tablet", "EA", 0.024, 1700, 0.36, 0.03, -0.01),
        ("lorazepam", "2 mg/mL", "oral concentrate", "ML", 0.62, 60, 0.70, 0.00, -0.02),
        ("alprazolam", "0.5 mg", "tablet", "EA", 0.019, 1300, 0.20, 0.03, -0.01),
        ("diazepam", "5 mg", "tablet", "EA", 0.022, 900, 0.22, 0.02, -0.01),
        ("temazepam", "15 mg", "capsule", "EA", 0.068, 500, 0.30, 0.03, -0.01),
    ]),
    ("Antiparkinson agents", [
        ("carbidopa-levodopa", "25-100 mg", "tablet", "EA", 0.09, 1300, 0.55, 0.03, -0.02),
        ("ropinirole", "1 mg", "tablet", "EA", 0.048, 700, 0.35, 0.03, -0.02),
        ("pramipexole", "0.25 mg", "tablet", "EA", 0.072, 500, 0.38, 0.04, -0.02),
        ("amantadine", "100 mg", "capsule", "EA", 0.34, 420, 0.42, 0.04, -0.03),
        ("amantadine", "50 mg/5 mL", "oral solution", "ML", 0.07, 300, 0.60, 0.00, -0.02),
        ("benztropine", "1 mg", "tablet", "EA", 0.11, 600, 0.50, 0.03, -0.01),
        ("carbidopa-levodopa", "50-200 mg", "extended-release tablet", "EA", 0.28, 500, 0.50, 0.03, -0.02),
        ("rasagiline", "1 mg", "tablet", "EA", 0.52, 260, 0.45, 0.04, -0.04),
        ("entacapone", "200 mg", "tablet", "EA", 0.46, 300, 0.50, 0.04, -0.03),
    ]),
    ("Urinary antispasmodics", [
        ("oxybutynin chloride", "5 mg", "tablet", "EA", 0.05, 900, 0.48, 0.03, -0.01),
        ("oxybutynin chloride", "5 mg/5 mL", "oral solution", "ML", 0.034, 300, 0.55, 0.00, -0.02),
        ("oxybutynin chloride", "10 mg", "extended-release tablet", "EA", 0.19, 600, 0.38, 0.04, -0.03),
        ("tolterodine", "2 mg", "tablet", "EA", 0.31, 300, 0.42, 0.05, -0.03),
        ("trospium chloride", "20 mg", "tablet", "EA", 0.36, 260, 0.44, 0.05, -0.03),
        ("solifenacin succinate", "5 mg", "tablet", "EA", 0.21, 600, 0.45, 0.04, -0.03),
        ("darifenacin", "7.5 mg", "extended-release tablet", "EA", 0.58, 200, 0.40, 0.05, -0.04),
    ]),
    ("Skeletal muscle relaxants", [
        ("cyclobenzaprine", "10 mg", "tablet", "EA", 0.024, 1900, 0.10, 0.04, -0.01),
        ("tizanidine", "4 mg", "tablet", "EA", 0.031, 1500, 0.20, 0.04, -0.01),
        ("methocarbamol", "750 mg", "tablet", "EA", 0.058, 900, 0.12, 0.04, -0.02),
        ("metaxalone", "800 mg", "tablet", "EA", 0.62, 150, 0.06, 0.06, -0.04),
    ]),
    ("Antiemetics", [
        ("ondansetron", "4 mg", "orally disintegrating tablet", "EA", 0.052, 1000, 0.30, 0.05, -0.03),
        ("ondansetron", "8 mg", "tablet", "EA", 0.061, 700, 0.22, 0.05, -0.03),
        ("ondansetron", "4 mg/5 mL", "oral solution", "ML", 0.11, 300, 0.40, 0.00, -0.03),
        ("prochlorperazine maleate", "10 mg", "tablet", "EA", 0.13, 400, 0.30, 0.04, -0.02),
        ("meclizine", "25 mg", "tablet", "EA", 0.041, 600, 0.35, 0.03, -0.01),
    ]),
    ("Oral corticosteroids", [
        ("prednisone", "10 mg", "tablet", "EA", 0.028, 1500, 0.34, 0.03, -0.01),
        ("prednisolone sodium phosphate", "15 mg/5 mL", "oral solution", "ML", 0.06, 600, 0.22, 0.00, -0.02),
        ("methylprednisolone", "4 mg", "tablet", "EA", 0.11, 500, 0.28, 0.04, -0.02),
        ("dexamethasone", "4 mg", "tablet", "EA", 0.21, 300, 0.38, 0.04, -0.03),
        ("fludrocortisone", "0.1 mg", "tablet", "EA", 0.36, 120, 0.42, 0.05, -0.03),
    ]),
]
SHORTLIST_NAMES = [c for c, _ in SHORTLIST]

# each class's volume scale: the units listed above are multiplied by it (calibrated so the class spreads sit where
# the design needs them; see the design note's Ladder)
SCALE = {"Anticonvulsants": 0.1800, "Antipsychotics": 0.0951, "Dementia agents": 0.1130, "Antidepressants, SSRI": 0.0913,
         "Beta blockers": 0.0941, "Loop diuretics": 0.1126, "Benzodiazepines": 0.1123, "Antiparkinson agents": 0.1001,
         "Urinary antispasmodics": 0.136, "Skeletal muscle relaxants": 0.1683, "Antiemetics": 0.1736,
         "Oral corticosteroids": 0.1728}
# the products outside the shortlist: their volume scale in the FY2026 summary
OTHER_SCALE = 0.11
# each product's FY2026 volume against FY2027 (growth from the prior year), drawn per product in sim.prior_year
# each class's ingredient spread on the golden fill, before the claim-level draw (calibration targets, dollars)
TARGET = {"Anticonvulsants": 42000, "Antipsychotics": 29400, "Dementia agents": 24000, "Antidepressants, SSRI": 2600,
          "Beta blockers": 3100, "Loop diuretics": 8600, "Benzodiazepines": 3300, "Antiparkinson agents": 24000,
          "Urinary antispasmodics": 14800, "Skeletal muscle relaxants": 1800, "Antiemetics": 4600,
          "Oral corticosteroids": 1900}

# the class list revision of 1 January 2027: products whose class changed (old label, new class)
MOVES = {
    ("gabapentin", "300 mg"): ("Anticonvulsants", "Neuropathic pain agents"),
    ("gabapentin", "600 mg"): ("Anticonvulsants", "Neuropathic pain agents"),
    ("clonazepam", "0.5 mg"): ("Benzodiazepines", "Anticonvulsants"),
    ("prochlorperazine maleate", "10 mg"): ("Antipsychotics", "Antiemetics"),
    ("memantine", "10 mg"): ("Antiparkinson agents", "Dementia agents"),
    ("memantine", "2 mg/mL"): ("Antiparkinson agents", "Dementia agents"),
    ("fluvoxamine", "100 mg"): ("Obsessive-compulsive disorder agents", "Antidepressants, SSRI"),
    ("sotalol", "80 mg"): ("Beta blockers", "Antiarrhythmics"),
    ("torsemide", "20 mg"): ("Diuretics, other", "Loop diuretics"),
    ("bethanechol", "25 mg"): ("Urinary antispasmodics", "Urinary retention agents"),
    ("baclofen", "10 mg"): ("Skeletal muscle relaxants", "Antispasticity agents"),
    ("baclofen", "5 mg/5 mL"): ("Skeletal muscle relaxants", "Antispasticity agents"),
    ("promethazine", "25 mg"): ("Antiemetics", "Antihistamines"),
    ("amantadine", "100 mg"): ("Antivirals", "Antiparkinson agents"),
    ("amantadine", "50 mg/5 mL"): ("Antivirals", "Antiparkinson agents"),
    ("fludrocortisone", "0.1 mg"): ("Mineralocorticoids", "Oral corticosteroids"),
}

# products outside the shortlist (the summary and the class list carry them; the claims extract does not)
OTHERS = [
    ("Neuropathic pain agents", [("gabapentin", "300 mg", "capsule", "EA", 0.029, 5200, 0.22),
                                 ("gabapentin", "600 mg", "tablet", "EA", 0.062, 2400, 0.18),
                                 ("pregabalin", "75 mg", "capsule", "EA", 0.07, 1200, 0.15)]),
    ("Antiarrhythmics", [("sotalol", "80 mg", "tablet", "EA", 0.12, 400, 0.25),
                         ("amiodarone", "200 mg", "tablet", "EA", 0.09, 700, 0.35)]),
    ("Urinary retention agents", [("bethanechol", "25 mg", "tablet", "EA", 0.21, 300, 0.45)]),
    ("Antispasticity agents", [("baclofen", "10 mg", "tablet", "EA", 0.035, 1700, 0.35),
                               ("baclofen", "5 mg/5 mL", "oral solution", "ML", 0.15, 300, 0.45)]),
    ("Antihistamines", [("promethazine", "25 mg", "tablet", "EA", 0.04, 900, 0.20),
                        ("hydroxyzine hydrochloride", "25 mg", "tablet", "EA", 0.03, 1800, 0.15)]),
    ("HMG-CoA reductase inhibitors", [("atorvastatin", "20 mg", "tablet", "EA", 0.035, 5600, 0.20),
                                      ("simvastatin", "20 mg", "tablet", "EA", 0.017, 2400, 0.22)]),
    ("ACE inhibitors", [("lisinopril", "10 mg", "tablet", "EA", 0.012, 5200, 0.20)]),
    ("Biguanides", [("metformin", "500 mg", "tablet", "EA", 0.011, 7000, 0.14)]),
]
# the classes already on the SMAC list (not candidates)
SMAC_LISTED = ["HMG-CoA reductase inhibitors", "ACE inhibitors", "Biguanides", "Antihistamines"]

# labelers: (name, labeler code, kind, ten-digit NDC configuration) where kind is M (manufacturer, retail bottles), U
# (unit-dose cartons) or N (a new entrant whose NDCs the survey has not yet priced); a four-digit labeler code takes
# the 4-4-2 configuration, a five-digit code 5-3-2 or 5-4-1
LABELERS = [
    ("Halcyon Generics", "2591", "M", "442"), ("Northbrook Pharmaceuticals", "62135", "M", "532"),
    ("Veridian Laboratories", "64980", "M", "541"), ("Castellan Pharmaceuticals", "4683", "M", "442"),
    ("Morrow Pharma", "67877", "M", "532"), ("Pinecrest Laboratories", "70436", "M", "541"),
    ("Altamira Pharma", "72888", "M", "532"), ("Brightwater Generics", "75834", "M", "541"),
    ("Kestrel Pharmaceuticals", "59736", "M", "532"), ("Lindell Laboratories", "51862", "M", "532"),
    ("Calder Unit Dose", "3086", "U", "442"), ("Sentry Packaging Services", "76385", "U", "532"),
    ("Avalon Unit Dose", "77333", "U", "541"), ("Marlow Institutional Pharmacy Services", "78206", "U", "532"),
    ("Tessaro Pharma", "79739", "N", "541"), ("Ravenna Laboratories", "80425", "N", "532"),
    ("Quillfield Generics", "46219", "N", "541"),
]

FILES = {
    "claims": "corvane_ffs_claims_paid_2026-04_2027-04.csv",
    "aac": "state_aac_rates_2025-04_2027-03.csv",
    "drugs": "state_drug_file_2027-04.xlsx",
    "classes": "state_drug_class_list_2027.xlsx",
    "summary": "corvane_generic_utilization_fy2026.xlsx",
    "terms": "smac_program_terms_2026.pdf",
    "method": "state_aac_survey_methodology_2026.pdf",
    "request": "smac_update_request_2027-03-08.pdf",
    "dict": "corvane_extract_record_layout.csv",
    "trans": "corvane_data_delivery_note_2027-04-21.docx",
    "mco": "mco_pharmacy_encounter_summary_2026.csv",
    "pdl": "state_pdl_status_2027-01.xlsx",
}
DISTRACTORS = ("mco", "pdl")
DELIVERABLES = ("smac_class_addition_2027-07.docx", "smac_candidate_classes_fy2026.xlsx")
