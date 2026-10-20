"""The fixed world: Prairie Hills Health Plan, a Medicaid managed care plan in an unnamed state, its primary care
provider groups, the first half of 2026, the members each group is assigned, the annual renewal that some members
lose and regain retroactively, and the state's capitation. Every other module reads its parameters from here."""
import datetime as dt

PLAN = "Prairie Hills Health Plan"
STATE_AGENCY = "State Department of Health Services, Medicaid Managed Care Unit"
DEPT = "Provider Performance"
PEOPLE = {"analyst": ("Paula Watts", "Senior Provider Performance Analyst"),
          "director": ("Derrick Warren", "Director, Network Contracting")}
SEED = 4740
RX_SEED = SEED + 21                                       # the pharmacy draw
YEAR = 2026
MONTHS = [dt.date(2026, m, 1) for m in range(1, 7)]        # the period: January to June 2026
PAID_BY = dt.date(2026, 10, 31)                            # claims paid by this date count
BENCHMARK = 412.00                                         # paid medical cost per member-month; at or above designates
RULES_DATE = "2 March 2026"
MEMO_DATE = "18 November 2026"

# provider groups: id, name, county, members assigned at January, base cost per member-month, share of a renewal
# cohort that lapses and is reinstated back to the lapse, share of members who die in the half year (aged, blind and
# disabled panels), share of renewers who leave for good
GROUPS = {
    "PG01": ("Cedar Valley Family Medicine", "Harlan", 2100, 391.07, .05, .004, .02),
    "PG02": ("Millbrook Community Clinics", "Ross", 2550, 413.23, .32, .003, .03),
    "PG03": ("North Fork Pediatrics", "Harlan", 1900, 309.79, .08, .000, .02),
    "PG04": ("Bluestem Internal Medicine", "Dade", 1300, 423.34, .06, .032, .02),
    "PG05": ("Sandhill Health Partners", "Ross", 2300, 405.51, .30, .004, .03),
    "PG06": ("Two Rivers Medical Group", "Lyon", 1750, 415.26, .10, .006, .02),
    "PG07": ("Prairie Gate Primary Care", "Dade", 1450, 404.41, .07, .040, .02),
    "PG08": ("Oak Hollow Physicians", "Lyon", 2050, 485.13, .28, .005, .03),
    "PG09": ("Westfield Family Health", "Morton", 1650, 409.81, .06, .004, .02),
    "PG10": ("Riverside Geriatric Associates", "Morton", 1200, 418.81, .05, .045, .01),
    "PG11": ("Summit Community Health Center", "Ross", 2400, 409.75, .27, .004, .03),
    "PG12": ("Lakeshore Medical Associates", "Harlan", 1600, 406.86, .06, .005, .02),
}
# the golden's cost per member-month each group is tuned to (tune.py scales each group's base cost)
DESIRED = {"PG01": 371.37, "PG02": 403.62, "PG03": 290.81, "PG04": 467.94, "PG05": 381.26, "PG06": 394.71,
           "PG07": 417.83, "PG08": 431.18, "PG09": 385.42, "PG10": 418.29, "PG11": 405.13, "PG12": 392.07}
# months a death stays on the roster after the month of death, by group (death reports reach the state late for
# members in long-term care)
LAG = {"PG07": (2, 3, 4), "PG10": (2, 3, 4), "PG04": (1, 2, 3)}

FILES = {
    "claims": "medical_claims_paid_2026h1.csv",
    "roster": "enrollment_roster_2026h1.csv",
    "remit": "capitation_remittance_2026.csv",
    "notes": "data_extract_notes.txt",
    "groups": "provider_group_register_2026.xlsx",
    "rules": "cost_performance_program_rules_2027.pdf",
    "rx": "pharmacy_claims_2026h1.csv",
    "classes": "drug_class_crosswalk.xlsx",
    "quality": "hedis_quality_scores_2025.xlsx",
    "survey": "member_experience_survey_2025.csv",
}
GOLDEN = {"workbook": "provider_group_pmpm_2026h1.xlsx", "memo": "provider_group_designations_2027.pdf"}
