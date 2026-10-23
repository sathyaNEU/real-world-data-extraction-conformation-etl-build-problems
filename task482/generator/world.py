"""The truth behind task482's pack: fourteen printing and converting plants in the Kestle Valley ozone nonattainment
area, their 2026 press operations, the regenerative thermal oxidizers on ten of them, the oxidizers' performance tests
since 2017 and the records each plant returned to the Department of Environmental Quality's information request of
12 January 2027. pack.py writes the files from this module; checks.py compares the cut pack with it.

An oxidizer's outlet holds at a floor (FLOOR, ppmv as carbon) below a knee and passes a fixed share (PASS) of its inlet
above it: outlet = max(FLOOR, PASS x inlet). Every test runs at the maximum production of the presses then installed.
A fixed-speed fan draws its rated air through every press's duct whatever the presses run, so on a part-production day
the inlet is dilute; a variable-speed fan follows the presses down to its minimum speed."""
import datetime as dt

import numpy as np

SEED = 482
K = 3.1173e-8            # lb of carbon per standard cubic foot per ppmv as carbon (68 F, 29.92 inHg)
K_PROPANE = 3.8150e-8    # lb of propane per standard cubic foot per ppmv as carbon (44.097 / 36.033 of K)
FLOOR = 45.0             # ppmv as carbon
PASS = 0.0180            # share of the inlet passed above the knee
RUN_NOISE = 0.015        # a test run's outlet against the relation
YEAR = 2026
DST_START, DST_END = dt.datetime(2026, 3, 8, 2), dt.datetime(2026, 11, 1, 2)   # US Central

AGENCY = "Department of Environmental Quality"
DIVISION = "Air Quality Division"
SECTION = "Emissions Inventory Section"
COUNCIL = "Environmental Quality Council"
AREA = "Kestle Valley ozone nonattainment area"
RULE = "Rule 18-4"
RULE_TITLE = "Printing and Converting Operations"
PEOPLE = {"rules": "Jeremy Cortez", "inventory": "Audrey Bautista"}
REQUEST_DATE = dt.date(2027, 1, 12)
RETURNS_DUE = dt.date(2027, 2, 12)
VOTE_DATE = dt.date(2027, 3, 25)
ACQUIRED = dt.date(2026, 5, 1)               # Kelvedon Laminates acquired Thameside Laminating
TAG_RENAMED = dt.datetime(2026, 6, 16, 0)    # the oxidizer vendor renamed the historian tags (UTC)
REFORMULATED = dt.date(2026, 6, 1)           # HW-CS-210 revision 4
RENUMBERED = dt.date(2026, 4, 1)             # Haldane's catalog renumbering
WASHER_SWITCH = dt.date(2026, 7, 1)          # six plants moved their parts washers to Ostrander
KG_FROM = dt.date(2026, 9, 1)                # the hauler's new manifest system at two plants

VENDORS = {"ARD": "Arden Thermal Systems", "PEL": "Pellham Environmental"}
FIRMS = {"A": ("Marlow Stack Testing", "propane"), "B": ("Prairieline Source Evaluation", "carbon")}
SUPPLIERS = {"A": "Corvane Inks", "B": "Haldane Coatings & Adhesives"}
HAULER = "Cantrell Bend Environmental"
WASHERS = {"KL": "Wexcombe Parts Washer Service", "SS": "Ostrander Solvent Recovery"}

# ---------------------------------------------------------------------------------------------------------------------
# Products on the safety data sheet master. code: (name, supplier, type, density lb/gal, basis, value, water vol %,
# exempt vol %, exempt compound, sold by). basis WT: VOC per cent by weight; LWE: lb VOC per gallon less water and
# exempt compounds.
PRODUCTS = {
    "CV-SF-1201": ("Solvent flexo ink, process cyan", "A", "INK", 7.92, "WT", 61.5, 0, 0, "", "GAL"),
    "CV-SF-1202": ("Solvent flexo ink, process magenta", "A", "INK", 7.98, "WT", 60.8, 0, 0, "", "GAL"),
    "CV-SF-1203": ("Solvent flexo ink, process yellow", "A", "INK", 7.85, "WT", 62.4, 0, 0, "", "GAL"),
    "CV-SF-1204": ("Solvent flexo ink, process black", "A", "INK", 8.06, "WT", 59.9, 0, 0, "", "GAL"),
    "CV-SF-1210": ("Solvent flexo ink, opaque white", "A", "INK", 9.41, "WT", 47.2, 0, 0, "", "GAL"),
    "CV-SG-2201": ("Solvent gravure ink, cyan", "A", "INK", 7.64, "WT", 66.3, 0, 0, "", "GAL"),
    "CV-SG-2202": ("Solvent gravure ink, magenta", "A", "INK", 7.70, "WT", 65.7, 0, 0, "", "GAL"),
    "CV-SG-2203": ("Solvent gravure ink, yellow", "A", "INK", 7.58, "WT", 67.1, 0, 0, "", "GAL"),
    "CV-SG-2204": ("Solvent gravure ink, black", "A", "INK", 7.81, "WT", 64.6, 0, 0, "", "GAL"),
    "CV-SG-2210": ("Solvent gravure ink, white", "A", "INK", 9.12, "WT", 52.0, 0, 0, "", "GAL"),
    "CV-WF-3201": ("Water flexo ink, cyan", "A", "INK", 8.72, "LWE", 1.84, 56.0, 0, "", "GAL"),
    "CV-WF-3202": ("Water flexo ink, magenta", "A", "INK", 8.75, "LWE", 1.92, 55.0, 0, "", "GAL"),
    "CV-WF-3203": ("Water flexo ink, yellow", "A", "INK", 8.70, "LWE", 1.76, 57.0, 0, "", "GAL"),
    "CV-WF-3204": ("Water flexo ink, black", "A", "INK", 8.81, "LWE", 2.05, 54.0, 0, "", "GAL"),
    "CV-UV-4201": ("UV flexo ink, process set", "A", "INK", 9.38, "WT", 0.8, 0, 0, "", "GAL"),
    "HC-OPV-510": ("Solvent overprint varnish, gloss", "B", "COATING", 7.74, "WT", 49.0, 0, 0, "", "GAL"),
    "HC-OPV-520": ("Heat-resistant lacquer", "B", "COATING", 7.88, "WT", 44.5, 0, 0, "", "GAL"),
    "HC-WOP-530": ("Water overprint varnish", "B", "COATING", 8.61, "LWE", 1.12, 63.0, 0, "", "GAL"),
    "HC-PRM-540": ("Solvent primer, film", "B", "COATING", 7.46, "WT", 71.2, 0, 0, "", "GAL"),
    "HA-SB-610": ("Solvent-based laminating adhesive", "B", "ADHESIVE", 7.82, "WT", 57.0, 0, 0, "", "LB"),
    "HA-SB-620": ("Solvent-based adhesive, high solids", "B", "ADHESIVE", 8.14, "WT", 41.0, 0, 0, "", "LB"),
    "HA-WB-650": ("Water-based laminating adhesive", "B", "ADHESIVE", 8.93, "LWE", 0.91, 54.0, 0, "", "LB"),
    "HA-SL-680": ("Solventless laminating adhesive", "B", "ADHESIVE", 9.31, "WT", 0.3, 0, 0, "", "LB"),
    "HW-PW-710": ("Automatic press wash", "B", "PRESS WASH", 6.91, "WT", 92.0, 0, 0, "", "GAL"),
    "HW-PW-720": ("Press wash, low VOC", "B", "PRESS WASH", 6.74, "LWE", 6.20, 0, 47.0, "acetone", "GAL"),
    "HW-CS-210": ("Equipment cleaning solvent", "B", "CLEANING", 6.80, "WT", 47.0, 0, 0, "acetone", "GAL"),
    "HW-RC-240": ("Anilox and roll cleaner", "B", "CLEANING", 7.40, "WT", 86.0, 0, 0, "", "GAL"),
    "HW-IK-260": ("Ink kitchen wash solvent", "B", "CLEANING", 6.95, "WT", 100.0, 0, 0, "", "GAL"),
    "WX-MS-100": ("Parts washer solvent (mineral spirits)", "KL", "CLEANING", 6.45, "WT", 100.0, 0, 0, "", "GAL"),
    "OS-MS-7": ("Recycled parts washer solvent", "SS", "CLEANING", 6.50, "WT", 100.0, 0, 0, "", "GAL"),
}
# HW-CS-210 before revision 4: the all-solvent formula
CS210_REV3 = (7.10, "WT", 100.0, 0, 0, "")
REVISIONS = [  # code, revision, effective from, what changed (old values), VOC changed
    ("HW-CS-210", 4, REFORMULATED, "reformulated with acetone; density 7.10 lb/gal and VOC 100.0 per cent by weight "
     "under revision 3", True),
    ("HW-CS-210", 3, dt.date(2023, 2, 1), "section 8 exposure limits updated", False),
    ("CV-SF-1210", 6, dt.date(2026, 3, 16), "section 2 hazard statements updated to GHS revision 9", False),
    ("CV-SG-2203", 5, dt.date(2026, 8, 3), "emergency telephone number changed", False),
    ("HA-SB-610", 4, dt.date(2026, 2, 9), "section 14 transport information updated", False),
    ("HC-PRM-540", 3, dt.date(2026, 10, 19), "supplier address changed", False),
    ("HW-PW-710", 7, dt.date(2026, 5, 4), "section 11 toxicology data added", False),
    ("CV-WF-3204", 4, dt.date(2025, 11, 10), "section 9 pH range corrected", False),
    ("HW-RC-240", 2, dt.date(2026, 9, 14), "label elements updated", False),
    ("HC-OPV-520", 5, dt.date(2026, 1, 12), "section 15 regulatory information updated", False),
]
CURRENT_REV = {"HW-CS-210": 4, "CV-SF-1210": 6, "CV-SG-2203": 5, "HA-SB-610": 4, "HC-PRM-540": 3, "HW-PW-710": 7,
               "CV-WF-3204": 4, "HW-RC-240": 2, "HC-OPV-520": 5}


def voc_per_gal(code, d=None):
    """lb of VOC per gallon of the product as used on date d (None: the current revision)."""
    if code == "HW-CS-210" and d is not None and d < REFORMULATED:
        den, basis, val, wv, ev, _ = CS210_REV3
    else:
        _, _, _, den, basis, val, wv, ev, _, _ = PRODUCTS[code]
    if basis == "WT":
        return den * val / 100.0
    return val * (1 - (wv + ev) / 100.0)


def density(code):
    return PRODUCTS[code][3]


# ---------------------------------------------------------------------------------------------------------------------
# The plants. ox: unit tag, vendor, fan (FIXED or VFD), rated scfm, minimum speed share, historian logs FLOW or SPEED,
# testing firm, capture method (PTE or TEST), capture efficiency, carbon content of the VOC (lb C per lb VOC).
# prof: ("unif", lo, hi) | ("beta", a, b, lo, hi) | ("mix", share of full days, full level, low level).
PLANTS = [
    dict(code="ASH", name="Ashcombe Flexible Packaging", fac="0213", town="Ashcombe", what="flexographic printing of "
         "flexible packaging (film and foil)", presses=["F1", "F2", "F3", "F4"], log="SHIFT", shifts=2, sat=True,
         down=4, R=568.2, prof=("unif", 0.49, 0.925),
         ox=dict(tag="ASH-RTO1", vendor="ARD", fan="FIXED", Q=80298.5, qmin=1.0, logs="FLOW", firm="B", cap="PTE",
                 CE=1.0, cf=0.550, installed=2014),
         mix={"N": [("CV-SF-1201", .17), ("CV-SF-1202", .16), ("CV-SF-1203", .14), ("CV-SF-1204", .12),
                    ("CV-SF-1210", .11), ("HC-OPV-510", .22), ("HW-PW-710", .08)]}),
    dict(code="BRI", name="Brinsley Label Works", fac="0236", town="Brinsley", what="narrow-web flexographic printing of "
         "pressure-sensitive labels", presses=["L1", "L2", "L3"], log="SHIFT", shifts=2, sat=False, down=5,
         target=10.555, ox=None,
         mix={"N": [("CV-WF-3201", .14), ("CV-WF-3202", .14), ("CV-WF-3203", .12), ("CV-WF-3204", .15),
                    ("CV-UV-4201", .05), ("HC-WOP-530", .15), ("HW-PW-720", .25)]}),
    dict(code="CAR", name="Carrow Gravure", fac="0327", town="Carrow", what="rotogravure printing of flexible "
         "packaging", presses=["G1", "G2", "G3", "G4", "G5"], log="JOB", shifts=3, sat=True, down=3, R=413.2,
         prof=("beta", 6.0, 2.5, 0.35, 1.0),
         ox=dict(tag="CAR-RTO1", vendor="PEL", fan="VFD", Q=28468.7, qmin=0.35, logs="SPEED", firm="A", cap="TEST",
                 CE=0.985, cf=0.560, installed=2012),
         mix={"N": [("CV-SG-2201", .17), ("CV-SG-2202", .17), ("CV-SG-2203", .15), ("CV-SG-2204", .15),
                    ("CV-SG-2210", .14), ("HC-OPV-520", .14), ("HW-PW-710", .08)]}),
    dict(code="DUN", name="Dunsford Folding Cartons", fac="0355", town="Dunsford", what="flexographic printing and "
         "coating of folding cartons", presses=["F1", "F2"], log="SHIFT", shifts=2, sat=False, down=6, target=7.401,
         ox=None,
         mix={"N": [("CV-WF-3201", .15), ("CV-WF-3202", .15), ("CV-WF-3203", .14), ("CV-WF-3204", .16),
                    ("HC-WOP-530", .25), ("HW-PW-720", .15)]}),
    dict(code="ELS", name="Elsworth Film Converting", fac="0388", town="Elsworth", what="flexographic printing and "
         "priming of shrink and barrier films", presses=["F1", "F2", "F3", "F4"], log="SHIFT", shifts=2, sat=False,
         down=5, R=702.0, prof=("beta", 4.0, 3.5, 0.30, 1.0),
         ox=dict(tag="ELS-RTO1", vendor="ARD", fan="VFD", Q=51300.0, qmin=0.35, logs="FLOW", firm="B", cap="PTE",
                 CE=1.0, cf=0.550, installed=2011, vfd_from=2019),
         mix={"N": [("CV-SF-1201", .17), ("CV-SF-1202", .17), ("CV-SF-1203", .15), ("CV-SF-1204", .13),
                    ("CV-SF-1210", .10), ("HC-PRM-540", .18), ("HW-PW-710", .10)]}),
    dict(code="GAR", name="Garrowby Printing", fac="0451", town="Garrowby", what="flexographic printing of paper and "
         "film packaging", presses=["F1", "F2", "F3"], log="SHIFT", shifts=2, sat=False, down=6, R=142.5,
         prof=("unif", 0.73, 0.955),
         ox=dict(tag="GAR-RTO1", vendor="PEL", fan="FIXED", Q=26715.2, qmin=1.0, logs="FLOW", firm="A", cap="TEST",
                 CE=0.950, cf=0.530, installed=2009),
         mix={"N": [("CV-SF-1201", .15), ("CV-SF-1202", .14), ("CV-SF-1203", .13), ("CV-SF-1204", .13),
                    ("CV-WF-3201", .07), ("CV-WF-3204", .08), ("HC-WOP-530", .10), ("HW-PW-720", .20)]}),
    dict(code="HAR", name="Hartmoor Packaging", fac="0476", town="Hartmoor", what="flexographic printing of flexible "
         "packaging", presses=["F1", "F2", "F3"], log="SHIFT", shifts=2, sat=True, down=4, R=221.4,
         prof=("beta", 5.0, 3.0, 0.30, 1.0),
         ox=dict(tag="HAR-RTO1", vendor="ARD", fan="VFD", Q=22315.0, qmin=0.35, logs="SPEED", firm="B", cap="TEST",
                 CE=0.970, cf=0.550, installed=2015),
         mix={"N": [("CV-SF-1201", .18), ("CV-SF-1202", .17), ("CV-SF-1203", .15), ("CV-SF-1204", .13),
                    ("CV-SF-1210", .07), ("HC-OPV-510", .20), ("HW-PW-710", .10)]}),
    dict(code="IVE", name="Ivers Lane Press", fac="0427", town="Ivers Lane", what="flexographic printing of labels, tags "
         "and wraps", presses=["F1", "F2", "F3"], log="SHIFT", shifts=2, sat=False, down=5, target=12.873, ox=None,
         mix={"N": [("CV-WF-3201", .12), ("CV-WF-3202", .12), ("CV-WF-3203", .11), ("CV-WF-3204", .15),
                    ("CV-SF-1204", .13), ("CV-SF-1210", .12), ("HW-PW-720", .25)]}),
    dict(code="KEL", name="Kelvedon Laminates", fac="0142", old_fac="0117", old_name="Thameside Laminating",
         town="Kelvedon", what="adhesive lamination and coating of flexible packaging", presses=["L1", "L2", "C1"],
         log="SHIFT", old_log="JOB", shifts=2, sat=True, down=4, R=931.1, prof=("mix", 0.40, 0.915, 0.255),
         ox=dict(tag="KVL-RTO1", old_tag="TLAM-RTO", vendor="PEL", fan="FIXED", Q=64138.8, qmin=1.0, logs="FLOW",
                 firm="A", cap="PTE", CE=1.0, cf=0.545, installed=2013),
         low_presses=["L2", "C1"],
         mix={"F": [("HA-SB-610", .74), ("HC-PRM-540", .20), ("HW-PW-710", .06)],
              "L": [("HA-SB-620", .42), ("HA-SL-680", .02), ("HC-PRM-540", .50), ("HW-PW-710", .06)]}),
    dict(code="LAR", name="Larkmoor Graphics", fac="0503", town="Larkmoor", what="rotogravure and flexographic printing "
         "of cartons and wraps", presses=["G1", "G2", "F1"], log="SHIFT", shifts=2, sat=True, down=5, R=809.5,
         prof=("mix", 0.22, 0.90, 0.255),
         ox=dict(tag="LAR-RTO1", vendor="ARD", fan="FIXED", Q=54127.8, qmin=1.0, logs="SPEED", firm="B", cap="PTE",
                 CE=1.0, cf=0.560, installed=2016),
         low_presses=["F1"],
         mix={"F": [("CV-SG-2201", .20), ("CV-SG-2202", .20), ("CV-SG-2203", .19), ("CV-SG-2204", .21),
                    ("HC-OPV-520", .12), ("HW-PW-710", .08)],
              "L": [("CV-SF-1201", .19), ("CV-SF-1202", .19), ("CV-SF-1203", .17), ("CV-SF-1204", .17),
                    ("HC-OPV-510", .20), ("HW-PW-710", .08)]}),
    dict(code="MER", name="Merrion Flexibles", fac="0539", town="Merrion", what="flexographic printing of flexible "
         "packaging", presses=["F1", "F2", "F3", "F4"], log="SHIFT", shifts=3, sat=True, down=3, R=302.1,
         prof=("beta", 6.0, 2.5, 0.35, 1.0),
         ox=dict(tag="MER-RTO1", vendor="PEL", fan="VFD", Q=23758.3, qmin=0.35, logs="SPEED", firm="A", cap="TEST",
                 CE=0.980, cf=0.550, installed=2010, vfd_from=2019),
         mix={"N": [("CV-SF-1201", .18), ("CV-SF-1202", .18), ("CV-SF-1203", .15), ("CV-SF-1204", .13),
                    ("CV-SF-1210", .10), ("HC-OPV-510", .18), ("HW-PW-710", .08)]}),
    dict(code="NOR", name="Norhaven Converting", fac="0562", town="Norhaven", what="flexographic printing of paper bags "
         "and wraps", presses=["F1", "F2", "F3"], log="SHIFT", shifts=2, sat=False, down=6, R=126.6,
         prof=("unif", 0.70, 0.955),
         ox=dict(tag="NOR-RTO1", vendor="ARD", fan="FIXED", Q=24705.3, qmin=1.0, logs="FLOW", firm="B", cap="TEST",
                 CE=0.950, cf=0.550, installed=2008),
         mix={"N": [("CV-SF-1201", .14), ("CV-SF-1202", .13), ("CV-SF-1203", .12), ("CV-SF-1204", .11),
                    ("CV-WF-3202", .12), ("CV-WF-3204", .13), ("HC-WOP-530", .10), ("HW-PW-720", .15)]}),
    dict(code="PEL", name="Pellworth Label", fac="0580", town="Pellworth", what="narrow-web UV and water flexographic "
         "printing of labels", presses=["L1", "L2"], log="SHIFT", shifts=2, sat=False, down=6, target=4.835, ox=None,
         mix={"N": [("CV-UV-4201", .10), ("CV-WF-3201", .13), ("CV-WF-3202", .13), ("CV-WF-3203", .11),
                    ("CV-WF-3204", .13), ("HW-PW-720", .40)]}),
    dict(code="RAV", name="Ravensbrook Gravure Packaging", fac="0604", town="Ravensbrook", what="rotogravure printing of "
         "flexible packaging", presses=["G1", "G2", "G3", "G4", "G5", "G6"], log="JOB", shifts=3, sat=True, down=3,
         R=695.0, prof=("beta", 7.0, 2.0, 0.35, 1.0),
         ox=dict(tag="RAV-RTO1", vendor="PEL", fan="VFD", Q=40771.7, qmin=0.35, logs="FLOW", firm="A", cap="TEST",
                 CE=0.990, cf=0.570, installed=2012),
         mix={"N": [("CV-SG-2201", .17), ("CV-SG-2202", .17), ("CV-SG-2203", .16), ("CV-SG-2204", .16),
                    ("CV-SG-2210", .14), ("HC-OPV-520", .12), ("HW-PW-710", .08)]}),
]
BY = {p["code"]: p for p in PLANTS}
CODES = [p["code"] for p in PLANTS]
CONTROLLED = [p["code"] for p in PLANTS if p["ox"]]
TESTS = [  # plant, date, production basis note, inlet factor on the plant's full-production inlet (None: at maximum)
    ("ASH", dt.date(2018, 5, 15), "two presses (F1, F2) installed", 0.505),
    ("ASH", dt.date(2021, 6, 9), None, 0.957),
    ("ASH", dt.date(2025, 4, 22), None, 0.968),
    ("CAR", dt.date(2019, 3, 19), None, 0.972),
    ("CAR", dt.date(2022, 9, 13), None, 1.035),
    ("CAR", dt.date(2025, 10, 7), None, 0.991),
    ("ELS", dt.date(2017, 8, 22), "fixed-speed fan; two presses (F1, F2) installed", 0.425),
    ("ELS", dt.date(2020, 11, 4), None, 1.028),
    ("ELS", dt.date(2024, 6, 18), None, 0.979),
    ("GAR", dt.date(2018, 2, 27), "two presses (F1, F2) installed", 0.665),
    ("GAR", dt.date(2021, 9, 21), None, 0.963),
    ("GAR", dt.date(2025, 5, 13), None, 0.952),
    ("HAR", dt.date(2020, 4, 28), None, 0.984),
    ("HAR", dt.date(2025, 8, 12), None, 1.030),
    ("KEL", dt.date(2019, 7, 16), None, 0.962),
    ("KEL", dt.date(2022, 5, 24), None, 0.977),
    ("KEL", dt.date(2025, 3, 11), None, 0.995),
    ("LAR", dt.date(2020, 9, 29), None, 0.978),
    ("LAR", dt.date(2024, 10, 15), None, 0.961),
    ("MER", dt.date(2018, 6, 5), "fixed-speed fan; two presses (F1, F2) installed", 0.585),
    ("MER", dt.date(2021, 10, 26), None, 0.986),
    ("MER", dt.date(2024, 12, 3), None, 1.022),
    ("NOR", dt.date(2017, 4, 18), "two presses (F1, F2) installed", 0.630),
    ("NOR", dt.date(2020, 6, 23), None, 0.974),
    ("NOR", dt.date(2024, 9, 10), None, 0.958),
    ("RAV", dt.date(2019, 5, 7), None, 0.966),
    ("RAV", dt.date(2023, 2, 14), None, 1.041),
    ("RAV", dt.date(2026, 3, 24), None, 1.004),
]
HOLIDAYS = {dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 11, 26),
            dt.date(2026, 11, 27)}
FIRST_DAY, LAST_DAY = dt.date(2026, 1, 5), dt.date(2026, 12, 23)


def rng_for(*keys):
    return np.random.default_rng([SEED] + [abs(hash_key(k)) for k in keys])


def hash_key(k):
    if isinstance(k, int):
        return k
    h = 0
    for ch in str(k):
        h = (h * 131 + ord(ch)) % 2147483647
    return h


def utc_offset(local):
    """Hours to add to local US Central time to get UTC."""
    return 5 if DST_START <= local < DST_END else 6


def to_utc(local):
    return local + dt.timedelta(hours=utc_offset(local))


def to_local(utc):
    """UTC to US Central: daylight time from 08:00 UTC on 8 March to 07:00 UTC on 1 November 2026."""
    if dt.datetime(2026, 3, 8, 8) <= utc < dt.datetime(2026, 11, 1, 7):
        return utc - dt.timedelta(hours=5)
    return utc - dt.timedelta(hours=6)


def hours_of(p):
    return 8.0 * p["shifts"]


def production_days(p):
    """The plant's 2026 production days: weekdays (and Saturdays where it runs them) from 5 January to 23 December,
    less the holidays and the plant's maintenance outages."""
    r = rng_for("cal", p["code"])
    out = []
    d = FIRST_DAY
    while d <= LAST_DAY:
        if d not in HOLIDAYS and (d.weekday() < 5 or (p["sat"] and d.weekday() == 5)):
            out.append(d)
        d += dt.timedelta(days=1)
    weekdays = [d for d in out if d.weekday() < 5]
    down = set()
    for _ in range(p["down"]):
        start = weekdays[int(r.integers(5, len(weekdays) - 8))]
        for k in range(int(r.integers(1, 3))):
            down.add(start + dt.timedelta(days=k))
    return [d for d in out if d not in down], sorted(down)


def utilization(p, days):
    r = rng_for("util", p["code"])
    n = len(days)
    prof = p["prof"]
    if prof[0] == "unif":
        return r.uniform(prof[1], prof[2], n), ["N"] * n
    if prof[0] == "beta":
        _, a, b, lo, hi = prof
        return lo + (hi - lo) * r.beta(a, b, n), ["N"] * n
    _, share, uf, ul = prof
    # runs of full days (a customer's solvent jobs) and low days, a few days each
    kinds, cur = [], "L"
    for i in range(n):
        if i == 0 or r.random() < (0.30 if cur == "F" else 0.30 * share / (1 - share)):
            cur = "F" if (i == 0 and r.random() < share) or (i and cur == "L") else ("L" if i else "L")
        kinds.append(cur)
    kinds = np.array(kinds)
    u = np.where(kinds == "F", r.normal(uf, 0.025, n).clip(0.84, 0.975), r.normal(ul, 0.010, n).clip(0.240, 0.28))
    return u, ["F" if k == "F" else "L" for k in kinds]


def air_share(p, u):
    """The fan's share of its rated air on each day: a fixed-speed fan draws it all; a variable-speed fan follows the
    presses' exhaust demand (the jobs' VOC per unit of air varies) down to its minimum speed."""
    ox = p["ox"]
    if ox["fan"] == "FIXED":
        return np.ones_like(u)
    r = rng_for("air", p["code"])
    return np.clip(u * r.normal(1.0, 0.045, len(u)), ox["qmin"], 1.0)


# ---------------------------------------------------------------------------------------------------------------------
def press_rows(p, days, u, kinds, target_lb=None):
    """The plant's 2026 press log rows and each production day's VOC used (lb), from the rows as logged."""
    r = rng_for("press", p["code"])
    hrs = hours_of(p)
    ce = p["ox"]["CE"] if p["ox"] else 1.0
    rows, used = [], {}
    np_ = len(p["presses"])
    for i, d in enumerate(days):
        if p["ox"]:
            lb = u[i] * p["R"] * hrs / ce
        else:
            lb = target_lb[i]
        mix = p["mix"][kinds[i]] if kinds[i] in p["mix"] else p["mix"]["N"]
        nrun = max(1, min(np_, int(round(u[i] * np_ + r.normal(0, 0.35))))) if p["ox"] else max(1, np_ - int(r.random() < 0.3))
        run = sorted(r.choice(np_, nrun, replace=False))
        if kinds[i] == "L" and p.get("low_presses"):
            run = [p["presses"].index(x) for x in p["low_presses"]]
            nrun = len(run)
        split = r.dirichlet([8.0] * nrun)
        voc = 0.0
        basis = p["log"]
        fac, pname = p["fac"], p["name"]
        if p.get("old_fac") and d < ACQUIRED:
            fac, pname, basis = p["old_fac"], p["old_name"], p["old_log"]
        for j, pi in enumerate(run):
            press = p["presses"][pi]
            plb = lb * split[j]
            if basis == "SHIFT":
                segs = [(s + 1, dt.datetime.combine(d, dt.time(6)) + dt.timedelta(hours=8 * s), 8.0)
                        for s in range(p["shifts"])]
            else:
                segs, t, k = [], dt.datetime.combine(d, dt.time(6)), 0
                end = t + dt.timedelta(hours=hrs)
                while t < end:
                    dur = min(float(r.choice([6.0, 8.0, 8.0, 10.0, 12.0])), (end - t).total_seconds() / 3600)
                    k += 1
                    segs.append((k, t, dur))
                    t += dt.timedelta(hours=dur)
            wts = r.dirichlet([10.0] * len(segs)) * 0.5 + np.array([s[2] for s in segs]) / hrs * 0.5
            for (sk, st, dur), w in zip(segs, wts):
                slb = plb * w
                inks = [m for m in mix if PRODUCTS[m[0]][2] == "INK"]
                others = [m for m in mix if PRODUCTS[m[0]][2] != "INK"]
                pick = inks if len(inks) <= 2 else [inks[q] for q in sorted(r.choice(len(inks), 2, replace=False))]
                share_ink = sum(m[1] for m in inks)
                sel = [(m[0], m[1] * share_ink / sum(x[1] for x in pick)) for m in pick] + others
                for code, sh in sel:
                    kind = PRODUCTS[code][2]
                    if kind == "PRESS WASH" and sk != 1:
                        continue
                    qlb = slb * sh * r.normal(1.0, 0.06)
                    vpg = voc_per_gal(code, d)
                    if PRODUCTS[code][9] == "LB" and p["code"] == "KEL" and not (p.get("old_fac") and d < ACQUIRED):
                        qty = round(qlb / vpg * density(code))
                        uom = "LB"
                        v = qty / density(code) * vpg
                    else:
                        qty = round(qlb / vpg, 1)
                        uom = "GAL"
                        v = qty * vpg
                    if qty <= 0:
                        continue
                    if basis == "JOB":
                        job = "%s%02d%03d%s" % (p["code"][:1], d.month, d.timetuple().tm_yday, press[-1] + str(sk))
                        rows.append(dict(fac=fac, plant=pname, press=press, basis="JOB", date=d, shift="", job=job,
                                         start=st, end=st + dt.timedelta(hours=dur), material=code, qty=qty, uom=uom))
                    else:
                        rows.append(dict(fac=fac, plant=pname, press=press, basis="SHIFT", date=d, shift=str(sk),
                                         job="", start=st, end=st + dt.timedelta(hours=dur), material=code, qty=qty,
                                         uom=uom))
                    voc += v
        used[d] = voc
    # a plant's year of ink, coating and adhesive gallons is logged to the tenth; keep its tenths off five
    ab = [x for x in rows if PRODUCTS[x["material"]][2] in ("INK", "COATING", "ADHESIVE") and x["uom"] == "GAL"]
    tot = sum(x["qty"] for x in ab)
    if ab and abs((tot % 1.0) - 0.5) < 0.15:
        x = ab[-1]
        x["qty"] = round(x["qty"] + 0.3, 1)
        used[x["date"]] += 0.3 * voc_per_gal(x["material"], x["date"])
    return rows, used


def uncontrolled_daily(p, days):
    """Daily VOC targets for a plant without an oxidizer, scaled to its year."""
    r = rng_for("unc", p["code"])
    w = r.uniform(0.6, 1.0, len(days))
    return w / w.sum() * p["target"] * 2000.0


# ---------------------------------------------------------------------------------------------------------------------
def historian(p, days, a, kinds):
    """Hourly rows of the plant's oxidizer historian (UTC hour beginning) and, per production day, the process hours and
    the mean airflow (scfm) over them."""
    ox = p["ox"]
    r = rng_for("hist", p["code"])
    hrs = int(hours_of(p))
    prod = {}
    for i, d in enumerate(days):
        st = dt.datetime.combine(d, dt.time(6))
        for h in range(hrs):
            prod[st + dt.timedelta(hours=h)] = i
    _, down = production_days(p)
    down = set(down)
    rows = []
    t = dt.datetime(2026, 1, 1, 0)
    agg = {}
    while t.year == 2026:
        lo = to_local(t)
        ld = lo.date()
        i = prod.get(lo)
        if i is not None:
            mode = "PROCESS"
            share = a[i] * (r.normal(1.0, 0.012) if ox["fan"] == "VFD" else 1.0)
            share = min(1.0, max(ox["qmin"], share))
            flow = ox["Q"] * share * (r.normal(1.0, 0.004) if ox["fan"] == "FIXED" else 1.0)
            temp = 1550 + r.normal(0, 6)
        elif ld < FIRST_DAY or ld > LAST_DAY + dt.timedelta(days=1) or ld in down or ld in HOLIDAYS:
            mode, share, flow, temp = "OFF", 0.0, 0.0, 180 + r.normal(0, 25)
        else:
            mode = "IDLE"
            share = 1.0 if ox["fan"] == "FIXED" else ox["qmin"]
            flow = ox["Q"] * (0.62 if ox["fan"] == "FIXED" else share) * r.normal(1.0, 0.01)
            temp = 1480 + r.normal(0, 12)
        tag = ox["tag"]
        if ox.get("old_tag") and t < TAG_RENAMED:
            tag = ox["old_tag"]
        if ox["logs"] == "FLOW":
            rows.append((tag, t, mode, round(temp), round(flow), ""))
            logged = round(flow)
        else:
            sp = round(100.0 * flow / ox["Q"], 1) if mode != "OFF" else 0.0
            rows.append((tag, t, mode, round(temp), "", sp))
            logged = ox["Q"] * sp / 100.0
        if mode == "PROCESS":
            g = agg.setdefault(days[i], [0, 0.0])
            g[0] += 1
            g[1] += logged
        t += dt.timedelta(hours=1)
    daily = {d: (g[0], g[1] / g[0]) for d, g in agg.items()}
    return rows, daily


# ---------------------------------------------------------------------------------------------------------------------
def full_inlet(p):
    """The plant's inlet (ppmv as carbon) at full production with the fan as it is now."""
    ox = p["ox"]
    q = ox["Q"] * (1.0 if ox["fan"] == "FIXED" else 1.0)
    return p["R"] * ox["cf"] / (q * 60 * K)


def tests():
    out = []
    for n, (code, d, note, fac) in enumerate(TESTS):
        p = BY[code]
        ox = p["ox"]
        r = rng_for("test", code, d.isoformat())
        firm = ox["firm"]
        c0 = full_inlet(p) * fac
        fixed_then = ox["fan"] == "FIXED" or (ox.get("vfd_from") and d.year < ox["vfd_from"])
        prod = 0.95 if note is None else 1.0
        if fixed_then:
            q0 = ox["Q"]
            c0 = c0 * (0.95 if note is None else 1.0) / (1.0 if note is None else 1.0)
        else:
            q0 = ox["Q"] * 0.95
        runs = []
        hour = 9
        for k in range(3):
            ci = c0 * r.normal(1.0, 0.022)
            co = max(FLOOR, PASS * ci) * r.normal(1.0, RUN_NOISE)
            qi = q0 * r.normal(1.0, 0.008)
            qo = qi * r.normal(1.0, 0.004)
            runs.append(dict(run=k + 1, start="%02d:%02d" % (hour, int(r.integers(0, 4)) * 5), ci=ci, co=co, qi=qi, qo=qo))
            hour += 1 + int(r.integers(1, 2))
        out.append(dict(no=n, plant=code, date=d, note=note, firm=firm, prod=prod, runs=runs,
                        tag=(ox.get("old_tag") if code == "KEL" else ox["tag"]),
                        name=(p.get("old_name") if code == "KEL" else p["name"]),
                        report="%s-%s-%02d" % ("MST" if firm == "A" else "PSE", d.strftime("%y%m"), 11 + n)))
    return out


# ---------------------------------------------------------------------------------------------------------------------
def everything():
    e = {"plants": {}, "tests": tests()}
    for p in PLANTS:
        days, down = production_days(p)
        rec = {"days": days, "down": down}
        if p["ox"]:
            u, kinds = utilization(p, days)
            a = air_share(p, u)
            rows, used = press_rows(p, days, u, kinds)
            hist, daily = historian(p, days, a, kinds)
            rec.update(u=u, kinds=kinds, a=a, rows=rows, used=used, hist=hist, daily=daily)
        else:
            tl = uncontrolled_daily(p, days)
            rows, used = press_rows(p, days, np.full(len(days), 0.8), ["N"] * len(days), tl)
            rec.update(rows=rows, used=used)
        e["plants"][p["code"]] = rec
    import asks
    asks.build(e)
    return e


# ---------------------------------------------------------------------------------------------------------------------
def outlet(c, F=FLOOR, p=PASS):
    return np.maximum(F, p * c)


def truth_summary(e, F=FLOOR, p=PASS):
    """Each plant's 2026 press VOC under the generator's own relation (tons), and the default path's."""
    out = {}
    for code in CODES:
        pl = BY[code]
        rec = e["plants"][code]
        used = sum(rec["used"].values()) / 2000.0
        if not pl["ox"]:
            out[code] = dict(used=used, captured=0.0, golden=used)
            continue
        ox = pl["ox"]
        cap = used * ox["CE"]
        ctl = 0.0
        for d in rec["days"]:
            h, q = rec["daily"][d]
            lbhr = rec["used"][d] * ox["CE"] / h
            c = lbhr * ox["cf"] / (q * 60 * K)
            ctl += outlet(c, F, p) * q * 60 * K / ox["cf"] * h
        out[code] = dict(used=used, captured=cap, golden=used - cap + ctl / 2000.0)
    return out
