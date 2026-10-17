"""task236 parameters: a state health department's influenza surveillance in the southern winter of 2027, its ten
health regions, the testing changes of the winter, the sentinel general practice network and the laboratories.
Dates are Australian Eastern Standard Time (UTC+10, no daylight saving in winter) unless a name says UTC."""
import datetime as dt

SEED = 236
WORLD_SEED = 63                      # infections, care, tests (sim.World)
RECORD_SEED = SEED * 7 + 3           # ids, keys, receipt times, distractors (records.Records)

PEOPLE = {"epi": "Heidi Sparks", "sentinel": "Brendan Davis", "lab": "Jane Suarez"}
BRANCH = "Communicable Diseases Branch"
DEPT = "Department of Health"

D0 = dt.date(2027, 4, 5)             # Monday of ISO week 14
D1 = dt.date(2027, 9, 12)            # Sunday of ISO week 36
REPORT_WEEK = 36
CUTOFF = dt.datetime(2027, 9, 13, 9, 0)        # Monday 09:00 local: the report counts what had arrived by then
PULL = dt.datetime(2027, 9, 14, 6, 30)         # the extract was pulled on the Tuesday morning (local)
UTC_OFFSET = dt.timedelta(hours=10)
BOUNDARY_DATE = dt.date(2027, 6, 28)           # postcodes moved between regions (MOVED) from Monday of week 26
WINDOW = 4                                     # report weeks either side of a change
LINE = 0.25                                    # a change of more than a quarter in the share notified

# regions: code, name, population (30 June 2026), flu peak (ISO week, fractional), flu symptomatic infections over the
# season (thousands), flu spread (days, sd), RSV peak week, RSV symptomatic infections (thousands), RSV spread (days),
# other respiratory illness per day per 1,000 people, drive-through clinics before any change (share of ill who use them)
REGIONS = [
    ("FN", "Far North",     292_400, 31.4, 17.5, 19.0, 30.6, 19.0, 11.0, 1.30, 0.05),
    ("NC", "North Coast",   518_900, 31.6, 26.0, 19.5, 30.0, 25.0, 11.0, 1.25, 0.09),
    ("TB", "Tablelands",    214_300, 32.6, 12.0, 20.0, 25.0, 5.2, 10.0, 1.20, 0.06),
    ("CW", "Central West",  377_600, 32.4, 19.0, 21.0, 25.6, 8.5, 10.5, 1.20, 0.07),
    ("MN", "Metropolitan North", 1_151_800, 31.2, 62.0, 18.5, 24.1, 30.0, 9.5, 1.40, 0.12),
    ("MS", "Metropolitan South", 1_024_700, 32.0, 54.0, 19.0, 24.8, 26.0, 9.5, 1.40, 0.14),
    ("MW", "Metropolitan West",    963_200, 31.8, 50.0, 19.0, 25.0, 24.0, 10.0, 1.40, 0.08),
    ("SC", "South Coast",   409_500, 33.2, 19.5, 21.0, 26.0, 8.0, 10.5, 1.25, 0.08),
    ("SW", "South West",    262_800, 33.0, 11.5, 21.0, 26.4, 4.6, 10.5, 1.20, 0.06),
    ("FW", "Far West",       61_900, 34.0, 2.6, 22.0, 27.0, 1.0, 11.0, 1.15, 0.03),
]

# care: the share of the ill who see a general practitioner, attend an emergency department; drive-through is per region
CARE = {"flu": {"gp": 0.30, "ed": 0.035}, "rsv": {"gp": 0.26, "ed": 0.042}, "oth": {"gp": 0.17, "ed": 0.014}}
# testing before any change: general practice referral to a laboratory (PCR), emergency department (influenza PCR on
# clinical suspicion), drive-through clinic (everyone who comes is swabbed)
TEST = {"gp": {"flu": 0.21, "rsv": 0.10, "oth": 0.06},
        "ed": {"flu": 0.56, "rsv": 0.42, "oth": 0.11},
        "dt": {"flu": 0.96, "rsv": 0.96, "oth": 0.96}}
SENS = {"pcr": 0.97, "panel": 0.97, "poc": 0.72}
FALSE_POS = {"pcr": 0.0008, "panel": 0.0008, "poc": 0.005}

# the testing changes the register logged: region, date (local), kind, register text
CHANGES = {
    "FN": (dt.date(2027, 7, 26), "poc", "Point-of-care influenza testing program, wave 1: funded rapid antigen testing in 38 Far North general practices; positive and negative results reported through the notification gateway"),
    "NC": (dt.date(2027, 7, 26), "hours", "Respiratory clinics at the two North Coast base hospitals extend to evenings and weekends (to 9 pm on weekdays, 9 am to 5 pm on weekends)"),
    "TB": (dt.date(2027, 8, 2), "panel", "Tablelands emergency departments (the base hospital and two district hospitals) test every respiratory presentation with the multiplex respiratory panel"),
    "CW": (dt.date(2027, 8, 2), "merger", "Coolabah West Pathology and Inland Diagnostic Laboratories merge as Western Pathology Network on one laboratory information system"),
    "MN": (dt.date(2027, 7, 26), "panel", "Metropolitan North emergency departments (four hospitals) move from influenza PCR on request to the multiplex respiratory panel for every respiratory presentation"),
    "MS": (dt.date(2027, 8, 2), "closure", "Metropolitan South's three drive-through respiratory testing clinics close at the end of their funding"),
    "MW": (dt.date(2027, 7, 26), "poc", "Point-of-care influenza testing program, wave 1: funded rapid antigen testing in 71 Metropolitan West general practices; positive and negative results reported through the notification gateway"),
    "SC": (dt.date(2027, 8, 9), "poc", "Point-of-care influenza testing program, wave 2: 33 South Coast general practices begin funded rapid antigen testing; results reported through the notification gateway"),
}
POC = {"flu": 0.62, "rsv": 0.60, "oth": 0.56}  # general practice patients given a point-of-care test once funded
POC_PCR_DROP = 0.50                             # referral to PCR among general practice patients once POC is funded
POC_CONFIRM = 0.25                              # point-of-care positives also sent for PCR
PANEL = {"flu": 0.93, "rsv": 0.93, "oth": 0.80}  # emergency department patients given the panel
CLOSURE_TO_GP = 0.35                            # drive-through users who see a general practitioner instead
HOURS_DT = 1.10                                 # extended clinic hours: clinic use

# sentinel general practice network: practices per region, the protocol swab cap per practice-week, the share of ill
# patients seen in general practice who meet the influenza-like-illness definition
SENTINEL_PRACTICES = {"FN": 12, "NC": 15, "TB": 9, "CW": 11, "MN": 22, "MS": 20, "MW": 19, "SC": 11, "SW": 9, "FW": 4}
SWAB_CAP = 10
ILI_DEF = {"flu": 0.70, "rsv": 0.40, "oth": 0.18}
SENTINEL_MISS = 0.03                            # practice-weeks with no return

# reporting services: code, name, kind, region(s) served; Central West's two laboratories merge on its change date
LABS = {
    "PHL": ("Public Health Laboratory", "laboratory"),
    "SLT": ("Saltmarsh Pathology Services", "laboratory"),
    "NGD": ("Northgate Diagnostics", "laboratory"),
    "HRB": ("Harbourline Pathology", "laboratory"),
    "CWP": ("Coolabah West Pathology", "laboratory"),
    "IDL": ("Inland Diagnostic Laboratories", "laboratory"),
    "WPN": ("Western Pathology Network", "laboratory"),
    "STH": ("Southern Districts Pathology", "laboratory"),
}
REGION_LABS = {"FN": ["NGD", "PHL"], "NC": ["NGD", "SLT"], "TB": ["IDL", "PHL"], "CW": ["CWP", "IDL"],
               "MN": ["SLT", "HRB", "PHL"], "MS": ["HRB", "STH"], "MW": ["SLT", "HRB"], "SC": ["STH", "SLT"],
               "SW": ["STH", "IDL"], "FW": ["IDL"]}
MERGED = ("CWP", "IDL", "WPN")                  # from Central West's change date both report as WPN
FLU_B_SHARE = 0.24                              # of influenza positives, type B
REPEAT = 0.02                                   # positives with a repeat specimen within five days
MISSING_POSTCODE = 0.012                        # no residential address on the request (blank, or 0000 at some services)
INTERSTATE = 0.004                              # people living outside the state who were tested here
PRELIM_SERVICES = ("PHL",)                      # services that send a preliminary positive for every positive
PRELIM_ED = True                                # every laboratory sends a preliminary positive for emergency specimens
FINAL_AFTER = (8.0, 40.0)                       # hours from the preliminary to the final report (PHL: subtyping, 20 to 60)
SUBTYPE_A = {"A(H3N2)": 0.68, "A(H1N1)pdm09": 0.32}
# inpatients re-swabbed while they shed: share of emergency positives admitted and re-swabbed (65 and over, under 65),
# days between swabs, shedding from the first positive (days: a floor plus a gamma tail)
RESWAB = {"65+": 0.34, "<65": 0.05}
RESWAB_GAP = (3, 7)
SHED = (4.0, 2.0, 5.0)
POSTCODES_PER_REGION = {"FN": 9, "NC": 12, "TB": 7, "CW": 10, "MN": 22, "MS": 20, "MW": 19, "SC": 11, "SW": 8, "FW": 4}
# postcodes moved on BOUNDARY_DATE under the 2027 boundary review: from, to, and which of the receiving region's
# postcodes (ranks by population, largest first)
MOVED = [("NC", "FN", (2,)), ("CW", "TB", (1, 5)), ("MN", "MW", (0,)), ("SC", "MS", (1,))]
