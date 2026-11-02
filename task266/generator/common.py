"""Constants for task266: the Fund, its register's window, the program's settings, the towns and road network, the
pack's file names and the people."""
import datetime as dt
import math

SEED = 277
FUND = "Dust Diseases Compensation Fund"
ACT = "Dust Diseases Compensation Act 2003"
PROGRAM = "Former Asbestos Workers Review Program"
UNIT = "Mobile Review Unit"
REGISTRY = "State Cancer Registry"
PEOPLE = {"manager": "Caitlin Holland", "registrar": "Veronica Wagner"}

# the register's window and its close
REG_START = dt.date(2004, 7, 1)          # the Fund began; the register holds every mesothelioma diagnosed from this day
REG_END = dt.date(2026, 6, 30)           # the 2025-26 register holds the diagnoses to this day
REG_CLOSE = dt.date(2026, 9, 30)         # the day the 2025-26 register closed
LEGACY_END = dt.date(2012, 12, 31)       # cases notified to this day were kept on the first system
COHORT_END = dt.date(1986, 1, 1)         # the program's workforce: first exposed at work before this day
YEAR = 365.25
SETTINGS = [40, 45, 50, 55, 60, 65, 70]
ASK_SETTINGS = [45, 50, 55, 60, 65, 70]
COVER = 0.90
TERM_START = dt.date(2027, 7, 1)
FY_START, FY_END = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
APPT_START = dt.date(2023, 7, 1)
ASOF = dt.date(2027, 2, 12)

FILES = {
    "register": "ddcf_mesothelioma_register_2013-2026.csv",
    "legacy": "ddcf_mesothelioma_register_2004-2012_legacy.xlsx",
    "histories": "ddcf_occupational_histories_2026-09-30.csv",
    "terms": "review_program_terms_2027-2031.pdf",
    "report": "ddcf_annual_report_2025-26.pdf",
    "members": "review_program_members_2026-06-30.csv",
    "appointments": "review_appointments_2023-07_to_2026-06.csv",
    "schedule": "mobile_review_unit_visit_schedule_2025-26.pdf",
    "card": "mobile_review_unit_card_statement_2025-26.xlsx",
    "qa": "mobile_review_unit_xray_qa_log_2025-26.xlsx",
    "roads": "review_sites_road_distances.xlsx",
    "registry": "state_cancer_registry_mesothelioma_1982-2024.xlsx",
    "workplaces": "asbestos_workplace_register_2024.csv",
}
DISTRACTORS = ["registry", "workplaces"]
DELIVERABLES = ["review_horizon_board_paper_2027.docx", "review_horizon_workbook_2027.xlsx"]

# The State's towns on a plane (km east, km north of the capital); the road network is the plane's distance times
# a winding factor per pair. The capital and four regional cities hold the fixed clinics; the unit is based at
# Hawksmere and visits the fourteen circuit towns; the rest are towns it passes through.
CITIES = {"Port Ellery": (0, 0), "Hawksmere": (182, 214), "Carrowby": (-246, 158), "Lindenvale": (318, -96),
          "Murrell Heads": (-118, -204)}
CIRCUIT = {"Quillerton": (296, 412), "Tarramore": (88, 486), "Dorrabee": (436, 338), "Kellowie": (-312, 402),
           "Haskesford": (512, 118), "Brinalong": (-58, 362), "Lathardine": (402, 566), "Wennobank": (-468, 254),
           "Corrinbar": (244, 302), "Fenalong": (-386, -58), "Strathowie": (566, -232), "Pellandra": (128, -342),
           "Garrock": (-186, 548), "Ostlebury": (-524, 96)}
WAYPOINTS = {"Mallin Junction": (348, 248), "Ferngate Gap": (-168, 284), "Thornbush Flat": (402, -12),
             "Bellwether Ridge": (-312, 182), "Sallow Creek": (196, 380)}
# localities a short drive from a circuit town, where the crew sometimes stays
LOCALITIES = {"Saltbush Flat": (424, 588), "Pellandra Beach": (146, -366), "Kellowie Heights": (-296, 426),
              "Ostlebury Point": (-548, 74), "Fenalong Bridge": (-402, -36)}
CLINIC_SITES = {"PEH": ("Port Ellery", "Port Ellery Thoracic Clinic"), "HWK": ("Hawksmere", "Hawksmere Base Hospital, Imaging"),
                "CRW": ("Carrowby", "Carrowby Health Centre"), "LDV": ("Lindenvale", "Lindenvale Hospital Radiology"),
                "MHD": ("Murrell Heads", "Murrell Heads Community Health")}
UNIT_SITE = "MRU"
UNIT_BASE = "Hawksmere"


def all_towns():
    d = {}
    d.update(CITIES)
    d.update(CIRCUIT)
    d.update(WAYPOINTS)
    d.update(LOCALITIES)
    return d


def _wind(a, b):
    """A fixed winding factor per road link, from the names (1.25 to 1.38)."""
    key = "|".join(sorted((a, b)))
    h = 0
    for ch in key:
        h = (h * 131 + ord(ch)) % 1000003
    return 1.25 + (h % 131) / 1000.0


_ROADS = {}


def _network():
    """The State's road network: a road joins every pair of places within 320 km of each other and each place to
    its three nearest, each road its straight line times a winding factor; distances are the shortest routes."""
    if _ROADS:
        return _ROADS
    t = all_towns()
    names = list(t)
    inf = float("inf")
    d = {a: {b: (0.0 if a == b else inf) for b in names} for a in names}

    def eu(a, b):
        (x1, y1), (x2, y2) = t[a], t[b]
        return math.hypot(x1 - x2, y1 - y2)
    for a in names:
        near = sorted(names, key=lambda b: eu(a, b))[1:4]
        for b in names:
            if b != a and (eu(a, b) <= 320 or b in near):
                w = eu(a, b) * _wind(a, b)
                d[a][b] = min(d[a][b], w)
                d[b][a] = min(d[b][a], w)
    for k in names:
        dk = d[k]
        for i in names:
            dik = d[i][k]
            if dik == inf:
                continue
            di = d[i]
            for j in names:
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    for a in names:
        _ROADS[a] = {b: int(round(d[a][b])) for b in names}
    return _ROADS


def road_km(a, b):
    if a == b:
        return 0
    return _network()[a][b]


def years(days):
    return days / YEAR


def fmt_legacy(d):
    """The first system's date text, as its export writes it (03-Feb-1965)."""
    return d.strftime("%d-%b-%Y")
