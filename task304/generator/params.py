"""task304 architecture 4: fixed parameters of the world (Brolga Parcel Network's sortation hubs)."""
import datetime as dt

SEED = 304

# The reference weeks the undertaking's schedule names: shifts that began 12 October to 8 November 2026.
REF_START = dt.date(2026, 10, 12)
REF_END = dt.date(2026, 11, 8)
# The sorter control system export covers two weeks before the reference weeks as well.
LOG_START = dt.date(2026, 9, 28)
LOG_END = dt.date(2026, 11, 8)
EXPORT_DATE = dt.date(2026, 11, 16)
AS_OF = dt.date(2026, 11, 27)

SHIFTS = {"AM": 5, "PM": 13, "NT": 21}     # local start hour; every shift is eight hours
SHIFT_HOURS = 8.0
BREAK_HOURS = 1.0                          # two 15-minute breaks and a 30-minute meal, taken in the amenities
MEAL_AT = 3.75                             # hours after shift start the line stops for the 30-minute meal
MEAL_LEN = 0.5
STANDARD = 85.0                            # dB(A), LAeq,8h exposure standard
PROGRAM_COST_AUD = 438                     # the hearing program's annual cost per enrolled worker (undertaking 4.3)

# Hubs. Li: induct-area LAeq before; Lp: induct-area LAeq the supplier predicts after the enclosure;
# Lf: sort and dock floor; La: amenities (meal room). Levels are the 2026 survey's, to 0.1 dB.
HUBS = [
    dict(code="LAR", name="Larapinta", city="Brisbane", state="QLD", tz="Australia/Brisbane", vendor="V1",
         stations=16, Li=93.6, Lp=84.1, Lf=81.9, La=64.6, scheme="dedicated",
         loaders=46, sorters=30, forklift=5, leads=2, agency=7, spares=4),
    dict(code="ECR", name="Eastern Creek", city="Sydney", state="NSW", tz="Australia/Sydney", vendor="V1",
         stations=20, Li=96.6, Lp=88.2, Lf=82.8, La=65.3, scheme="am_rotation",
         loaders=58, sorters=36, forklift=6, leads=2, agency=10, spares=6),
    dict(code="TRU", name="Truganina", city="Melbourne", state="VIC", tz="Australia/Melbourne", vendor="V2",
         stations=12, Li=95.1, Lp=84.4, Lf=81.4, La=63.9, scheme="sorter_relief",
         loaders=30, sorters=40, forklift=4, leads=2, agency=6, spares=4),
    dict(code="WFD", name="Wingfield", city="Adelaide", state="SA", tz="Australia/Adelaide", vendor="V3",
         stations=10, Li=91.4, Lp=82.9, Lf=80.6, La=63.4, scheme="break_buddies",
         loaders=40, sorters=22, forklift=4, leads=1, agency=5, spares=3),
    dict(code="KEW", name="Kewdale", city="Perth", state="WA", tz="Australia/Perth", vendor="V2",
         stations=12, Li=94.9, Lp=86.4, Lf=81.8, La=64.8, scheme="half_shift",
         loaders=34, sorters=24, forklift=4, leads=2, agency=6, spares=4),
    dict(code="BFD", name="Beresfield", city="Newcastle", state="NSW", tz="Australia/Sydney", vendor="V3",
         stations=8, Li=92.9, Lp=84.0, Lf=81.3, La=64.1, scheme="agency_pm",
         loaders=22, sorters=16, forklift=3, leads=1, agency=8, spares=3),
]

# Job titles as each hub's HR records write them.
TITLES = {
    "LAR": dict(induct="Inductor", relief="Relief Inductor", loader="Loader", sorter="Sort Operator",
                forklift="Forklift Driver", lead="Team Leader"),
    "ECR": dict(induct="Induction Operator", relief="Induction Relief", loader="Loader", sorter="Sort Operator",
                forklift="Forklift Operator", lead="Shift Lead"),
    "TRU": dict(induct="Sorter - Induct", relief="Sorter - Relief", loader="Dock Operator", sorter="Sorter - Chute",
                forklift="MHE Driver", lead="Team Leader"),
    "WFD": dict(induct="Inductor", relief=None, loader="Loader", sorter="Floor Operator",
                forklift="Forklift Driver", lead="Team Leader"),
    "KEW": dict(induct="Inductor", relief="Relief Inductor", loader="Loader", sorter="Sort Operator",
                forklift="Forklift Driver", lead="Team Leader"),
    "BFD": dict(induct="Induction Operator", relief=None, loader="Loader", sorter="Sort Operator",
                forklift="Forklift Operator", lead="Shift Lead"),
}

ABSENCE = 0.07          # chance an employee is off (leave or sick) on a rostered shift
AGENCY_SHOW = 0.80      # chance a labour-hire operative on a hub's call list works a given shift

# ---- ask A: the PPE vending supplier's machines (July to September 2026)
VEND_START = dt.date(2026, 7, 1)
VEND_END = dt.date(2026, 9, 30)
PAIRS_PER_WORKER_SHIFT = 0.36
VEND_SEED = 315
RANGE_CHANGE_SUNDAYS = (dt.date(2026, 8, 2), dt.date(2026, 8, 9))   # EP-01 moves from one pair to a pack of five
EP_PACK_AFTER = 5
# machine swaps between hubs: (date the machine leaves, days offline, (hub_a, hub_b))
RELOCATIONS = [
    (dt.date(2026, 8, 15), ("ECR", "WFD")), (dt.date(2026, 8, 15), ("LAR", "BFD")), (dt.date(2026, 8, 15), ("TRU", "KEW")),
    (dt.date(2026, 9, 12), ("ECR", "KEW")), (dt.date(2026, 9, 12), ("LAR", "WFD")), (dt.date(2026, 9, 12), ("TRU", "BFD")),
]

# ---- ask B: audiometry (the program enrols the induct titles and team leaders)
AUDIO_YEAR = 2026
AUDIO_EXPORT = dt.date(2026, 11, 6)        # ClearTone's client list export
STS_DB = 10.0           # average worsening at 2, 3 and 4 kHz in either ear
RETEST_DAYS = 30
