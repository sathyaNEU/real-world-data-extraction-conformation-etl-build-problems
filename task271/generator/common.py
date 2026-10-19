"""Constants shared by the task271 generator: the plan, the hospital data consortium, the hospitals that operate on the
pancreas, the window the programme reads, the code lists, the release dates and the shipped file names."""
import datetime as dt

PLAN = "Corrisbrook Health Cooperative"
PLAN_SHORT = "Corrisbrook"
PROGRAMME = "Pancreatic Surgery Centres"
CONSORTIUM = "Upper Lakes Hospital Data Consortium"
CONS_SHORT = "ULHDC"
PEOPLE = {"requester": "Katrina Newman", "analyst": "Luis Thomas"}

# The hospitals that operate on the pancreas. Code, name today, the consortium's hospital number before and after
# the 2023 renumbering, the NPI the plan's claims carry, and whether the programme lists it as eligible.
# Maplewick Community Hospital joined Ferncastle Health on 1 July 2024 and reports under Ferncastle's licence from
# then; its pancreatic surgery moved to the Ferncastle campus, which is the eligible hospital.
HOSPITALS = [
    # code  name today                               old no.  new no.   NPI          eligible
    ("A", "Aldermoor University Hospital",           "0104", "550104", "1295830411", True),
    ("B", "Brackwell Medical Center",                "0217", "550217", "1386741902", True),
    ("C", "Farrowmere Regional Medical Center",      "0331", "550331", "1477652013", True),
    ("D", "Kestwick Memorial Hospital",              "0412", "550412", "1568563124", True),
    ("E", "Netherfold Medical Center",               "0506", "550506", "1659474235", True),
    ("F", "Yarrowdale Regional Hospital",            "0623", "550623", "1740385346", True),
    ("G", "Ferncastle Health",                       "0745", "550745", "1831296457", True),
    ("H", "Elmhaven Memorial Hospital",              "0858", "550858", "1922107568", True),
    ("G2", "Maplewick Community Hospital",           "0749", "550749", "1013218679", False),
    ("S01", "Fenmoor Hospital",                      "0911", "550911", "1104129780", False),
    ("S02", "Ulverby Medical Center",                "0924", "550924", "1195030891", False),
    ("S03", "Hallowmere Hospital",                   "0937", "550937", "1285941902", False),
    ("S04", "Iversley Community Hospital",           "0946", "550946", "1376852013", False),
    ("S05", "Mossgrove Medical Center",              "0958", "550958", "1467763124", False),
    ("S06", "Gorsemere Hospital",                    "0963", "550963", "1558674235", False),
    ("S07", "Orrinsby Regional Hospital",            "0971", "550971", "1649585346", False),
    ("S08", "Juddmore Hospital",                     "0982", "550982", "1730496457", False),
    ("S09", "Thistlemere Medical Center",            "0994", "550994", "1821307568", False),
    ("S10", "Vellacott Hospital",                    "1003", "551003", "1912218679", False),
    ("S11", "Bramblecote Community Hospital",        "1015", "551015", "1003129780", False),
    ("S12", "Quillmere Hospital",                    "1027", "551027", "1094030891", False),
    ("S13", "Hawkmere Medical Center",               "1038", "551038", "1184941902", False),
    ("S14", "Sherwick Hospital",                     "1046", "551046", "1275852013", False),
]
CODES = [h[0] for h in HOSPITALS]
NAME = {h[0]: h[1] for h in HOSPITALS}
OLD_NO = {h[0]: h[2] for h in HOSPITALS}
NEW_NO = {h[0]: h[3] for h in HOSPITALS}
NPI = {h[0]: h[4] for h in HOSPITALS}
ELIGIBLE = [h[0] for h in HOSPITALS if h[5]]
MERGER = dt.date(2024, 7, 1)          # Maplewick joins Ferncastle Health
RENUMBER_YEAR = 2023                  # the consortium's six-digit hospital numbers from the 2023 files

WINDOW = (dt.date(2023, 1, 1), dt.date(2025, 12, 31))     # operations the programme reads
FOLLOW = 90                                               # days after the operation
CLAUSE = {"population": "3.2", "deaths": "3.3", "expected": "3.4", "comparison": "3.5"}   # the criteria's clauses
HISTORY_FROM = 2016                                       # the earliest file the consortium releases
H1_2026 = (dt.date(2026, 1, 1), dt.date(2026, 6, 30))     # the first half of 2026, the preliminary and revised releases
PRELIM_RELEASED = dt.date(2026, 5, 15)                    # quarter 1, preliminary
REVISED_RELEASED = dt.date(2026, 9, 18)                   # quarters 1 and 2, revised
DEATHS_LINKED = dt.date(2026, 8, 31)                      # the death index linkage run
ASSEMBLED = dt.datetime(2026, 10, 9, 14, 20)              # the pack put together for the board paper
CRITERIA_DATE = dt.date(2026, 9, 30)                      # the programme criteria, version 2
BOARD = dt.date(2026, 11, 17)                             # the board votes the centres
PLAN_CLAIMS_THROUGH = dt.date(2026, 9, 30)                # the plan's claims paid through

# ICD-10-PCS: the programme's pancreatic resection codes (its Appendix A)
RESECTION = {
    "0FBG0ZZ": "Excision of pancreas, open approach",
    "0FBG4ZZ": "Excision of pancreas, percutaneous endoscopic approach",
    "0FTG0ZZ": "Resection of pancreas, open approach",
    "0FTG4ZZ": "Resection of pancreas, percutaneous endoscopic approach",
}
BIOPSY = {"0FBG0ZX": "Excision of pancreas, open approach, diagnostic",
          "0FBG3ZX": "Excision of pancreas, percutaneous approach, diagnostic",
          "0FBG8ZX": "Excision of pancreas, via natural or artificial opening endoscopic, diagnostic"}
# the other parts of a pancreaticoduodenectomy, coded beside the pancreas
WHIPPLE_PARTS = {
    "0DT90ZZ": "Resection of duodenum, open approach",
    "0FT40ZZ": "Resection of gallbladder, open approach",
    "0F190ZB": "Bypass common bile duct to small intestine, open approach",
    "0D160ZA": "Bypass stomach to jejunum, open approach",
    "0F1G0ZC": "Bypass pancreas to large intestine, open approach",
}
# earlier operations on the pancreas or bile ducts (the operations a re-operation follows)
EARLIER_OPS = {
    "0FBG0ZZ": "Excision of pancreas, open approach",
    "0FBG4ZZ": "Excision of pancreas, percutaneous endoscopic approach",
    "0F1D0ZB": "Bypass pancreatic duct to small intestine, open approach",
    "0F190ZB": "Bypass common bile duct to small intestine, open approach",
    "0F190Z3": "Bypass common bile duct to duodenum, open approach",
    "0FB90ZZ": "Excision of common bile duct, open approach",
    "0FCG0ZZ": "Extirpation of matter from pancreas, open approach",
    "0FC90ZZ": "Extirpation of matter from common bile duct, open approach",
}
# harmless earlier procedures on the same organs
CHOLE = {"0FT44ZZ": "Resection of gallbladder, percutaneous endoscopic approach",
         "0FT40ZZ": "Resection of gallbladder, open approach"}
ERCP = {"0F798DZ": "Dilation of common bile duct with intraluminal device, via natural or artificial opening endoscopic",
        "0FC98ZZ": "Extirpation of matter from common bile duct, via natural or artificial opening endoscopic",
        "0FJD8ZZ": "Inspection of pancreatic duct, via natural or artificial opening endoscopic"}
OTHER_OPS = {"0FB00ZZ": "Excision of liver, open approach", "0FT00ZZ": "Resection of liver, open approach",
             "0FB04ZZ": "Excision of liver, percutaneous endoscopic approach",
             "0DT60ZZ": "Resection of stomach, open approach", "0FB24ZZ": "Excision of right lobe liver, percutaneous endoscopic approach"}

FILES = {
    "d2016": "ulhdc_hbp_discharges_2016.txt", "d2017": "ulhdc_hbp_discharges_2017.txt",
    "d2018": "ulhdc_hbp_discharges_2018.txt",
    "d2019_2022": "ulhdc_hbp_discharges_2019_2022.csv",
    "d2023_2025": "ulhdc_hbp_discharges_2023_2025.csv",
    "prelim": "ulhdc_hbp_2026q1_preliminary.csv",
    "revised": "ulhdc_hbp_2026q1q2_revised.csv",
    "deaths": "ulhdc_death_linkage_2016_2026.csv",
    "hospitals": "ulhdc_hospital_directory.xlsx",
    "codes": "ulhdc_procedure_classes.csv",
    "guide": "ulhdc_research_file_guide_2026.pdf",
    "criteria": "corrisbrook_pancreatic_centres_criteria_v2.pdf",
    "claims": "corrisbrook_facility_claims_pancreas_2023_2025.csv",
    "stars": "hospital_overall_star_ratings_2026.csv",
    "costs": "corrisbrook_travel_benefit_estimates_2026.xlsx",
    "contents": "contents.txt",
}
