"""Constants for task266: the college, its programs, courses and terms, the pack's file names and the people."""
import datetime as dt

COLLEGE = "Quenlow County Community College"
SHORT = "QCCC"
CAMPUS = {"QNL": "Quenlow", "TRV": "Tarvelly", "HOL": "Hollenby"}
LEGACY_CAMPUS = {"QNL": "Q", "TRV": "T", "HOL": "H"}
EXCHANGE = "Pennsylvania Enrollment Exchange"
PEOPLE = {"ir": "Tammy Weaver", "vpaa": "Derek Collier", "registrar": "Colleen Fisher"}
FLOOR = 30.0
WINDOW = 9                      # terms, the entering fall counted first, summers included
FTE_HOURS = 15
SMALL = 10                      # a class with fewer students than this at the census is a small class
EXTRACT = dt.date(2027, 5, 28)  # the registrar's extracts for the June 2027 review
CLASSES = (2023, 2024, 2025)

# code, new system code, legacy code, name, award, CIP, transfer-oriented, subjects the program owns
PROGRAMS = [
    ("GS", "AA.GENS", "GEN-AA", "General Studies", "AA", "24.0102", True, ["IDS"]),
    ("BIO", "AS.BIOL", "BIO-AS", "Biological Sciences", "AS", "26.0101", True, ["BIO"]),
    ("BUS", "AS.BUSA", "BUS-AS", "Business Administration", "AS", "52.0201", True, ["BUS", "ACC"]),
    ("PSY", "AA.PSYC", "PSY-AA", "Psychology", "AA", "42.0101", True, ["PSY"]),
    ("MA", "AAS.MEDA", "MAS-AAS", "Medical Assisting", "AAS", "51.0801", False, ["MDA"]),
    ("ECE", "AAS.ECED", "ECE-AAS", "Early Childhood Education", "AAS", "13.1210", False, ["ECE"]),
    ("CJ", "AAS.CRJU", "CRJ-AAS", "Criminal Justice", "AAS", "43.0104", False, ["CRJ"]),
    ("HVR", "AAS.HVAC", "HVA-AAS", "Heating, Ventilation, Air Conditioning and Refrigeration Technology", "AAS",
     "47.0201", False, ["HVR"]),
    ("NUR", "AAS.NURS", "NUR-AAS", "Nursing", "AAS", "51.3801", False, ["NUR"]),
]
CODES = [p[0] for p in PROGRAMS]
SIS = {p[0]: p[1] for p in PROGRAMS}
LEGACY = {p[0]: p[2] for p in PROGRAMS}
NAME = {p[0]: p[3] for p in PROGRAMS}
AWARD = {p[0]: p[4] for p in PROGRAMS}
CIP = {p[0]: p[5] for p in PROGRAMS}
TRANSFER = [p[0] for p in PROGRAMS if p[6]]
OWNS = {p[0]: p[7] for p in PROGRAMS}
SHORTNAME = {"GS": "General Studies", "BIO": "Biological Sciences", "BUS": "Business Administration",
             "PSY": "Psychology", "MA": "Medical Assisting", "ECE": "Early Childhood Education",
             "CJ": "Criminal Justice", "HVR": "HVAC-R Technology", "NUR": "Nursing"}
# programs outside the review: certificates, dual enrolment and non-degree study
OTHER = [("CERT.PHLB", "PHB-CT", "Phlebotomy", "Certificate", "51.1009"),
         ("CERT.HVTC", "HVT-CT", "HVAC-R Technician", "Certificate", "47.0201"),
         ("CERT.CDAP", "CDA-CT", "Child Development Associate Preparation", "Certificate", "19.0708"),
         ("CERT.WELD", "WLD-CT", "Welding Technology", "Certificate", "48.0508"),
         ("CERT.ACCT", "ACC-CT", "Accounting Clerk", "Certificate", "52.0302"),
         ("DE.HSDE", "HSD-DE", "High School Dual Enrollment", "None", ""),
         ("ND.NDEG", "NON-ND", "Non-Degree Studies", "None", "")]
CERTS = [o[0] for o in OTHER if o[0].startswith("CERT")]


# ---------------------------------------------------------------------------------------------- terms
def _monday_on_or_after(d):
    return d + dt.timedelta(days=(7 - d.weekday()) % 7)


def term_list():
    """Every term from fall 2018 to summer 2027: (code, legacy code or '', season, calendar year, dates)."""
    out = []
    for y in range(2018, 2027 + 1):
        for season in ("FA", "SP", "SU"):
            if season == "FA":
                if y > 2026:
                    continue
                code, cal = (y + 1) * 100 + 10, y
                start = _monday_on_or_after(dt.date(y, 8, 22))
                census = start + dt.timedelta(days=15)
                end = start + dt.timedelta(days=109)
                confer = end + dt.timedelta(days=4)
            elif season == "SP":
                if y == 2018:
                    continue
                code, cal = y * 100 + 20, y
                start = _monday_on_or_after(dt.date(y, 1, 15))
                census = start + dt.timedelta(days=15)
                end = start + dt.timedelta(days=116)
                confer = end + dt.timedelta(days=3)
            else:
                if y == 2018:
                    continue
                code, cal = y * 100 + 30, y
                start = _monday_on_or_after(dt.date(y, 5, 26))
                census = start + dt.timedelta(days=8)
                end = start + dt.timedelta(days=67)
                confer = end + dt.timedelta(days=4)
            legacy = "%d%s" % (cal, season) if code <= 202430 else ""
            out.append(dict(code=str(code), legacy=legacy, season=season, year=cal, start=start, census=census,
                            end=end, confer=confer))
    out.sort(key=lambda t: t["code"])
    return out


TERMS = term_list()
TERM = {t["code"]: t for t in TERMS}
CODES_IN_ORDER = [t["code"] for t in TERMS]
SEASON_NAME = {"FA": "Fall", "SP": "Spring", "SU": "Summer"}


def term_name(code):
    t = TERM[code]
    return "%s %d" % (SEASON_NAME[t["season"]], t["year"])


def fall(y):
    return str((y + 1) * 100 + 10)


def nth(code, k):
    """The term k terms after code (k=0 is code itself)."""
    i = CODES_IN_ORDER.index(code)
    return CODES_IN_ORDER[i + k]


def index_of(entry, code):
    """1 for the entering term, 2 for the next term and so on."""
    return CODES_IN_ORDER.index(code) - CODES_IN_ORDER.index(entry) + 1


LAST = "202720"         # spring 2027, the last term the extracts cover
FALL26 = "202710"
CONVERSION = "202510"   # fall 2024, the first term run in the new student system

# ---------------------------------------------------------------------------------------------- the pack
FILES = {
    "policy": "policy_3-12_program_review.pdf",
    "notes": "registrar_extract_notes_2027-05.pdf",
    "cohorts": "ir_fall_entering_students_2023-2025.xlsx",
    "admissions": "sis_admissions_exits_202410-202720.csv",
    "conferrals": "associate_degree_conferrals_2023-12_to_2027-05.csv",
    "idmap": "sis_conversion_student_id_map_2024.txt",
    "terms": "term_calendar_2018-2027.xlsx",
    "registrations": "fall2026_census_registrations.csv",
    "history": "program_of_record_history.csv",
    "schedule": "fall2026_section_schedule.xlsx",
    "register": "program_register_2026-27.xlsx",
    "success": "course_success_rates_fa2021-sp2026.xlsx",
    "outlook": "service_area_occupational_outlook_2024-2034.csv",
    "manifest": "export_manifest.csv",
}
DISTRACTORS = ["success", "outlook"]
MAIN_FILES = ["policy", "notes", "cohorts", "admissions", "conferrals", "idmap", "terms"]
ASK_FILES = ["registrations", "history", "schedule"]
