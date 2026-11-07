"""task490 world: the Coldmere Canals Trust's three summits, their summit locks, reservoirs and abstraction licences.

Everything here is a fixed parameter of the invented world. Times are local clock time (Europe/London) unless a
name says UTC."""
from datetime import date, datetime, timedelta

SEASON_START = date(2026, 4, 1)
SEASON_END = date(2026, 10, 31)
DAYS = [SEASON_START + timedelta(days=i) for i in range((SEASON_END - SEASON_START).days + 1)]
BST_START_UTC = datetime(2026, 3, 29, 1, 0)   # clocks go forward
BST_END_UTC = datetime(2026, 10, 25, 1, 0)    # clocks go back
EXPORT_DATE = date(2026, 11, 3)
ASOF = date(2026, 11, 6)


def to_utc(t):
    """local clock time to UTC (the season holds no ambiguous hour that a boat uses)."""
    u = t - timedelta(hours=1)
    if BST_START_UTC <= u < BST_END_UTC:
        return u
    return t


def to_local(u):
    return u + timedelta(hours=1) if BST_START_UTC <= u < BST_END_UTC else u


SUMMITS = ["Kelsby", "Harnock", "Tilsey"]

# asset id, lock name, summit, canal, broad, chamber length m, width m, rise m, fill min, empty min,
# historic number, historic length ft-in, width ft-in, rise ft-in, camera site code, firmware switch (local)
LOCKS = [
    dict(asset="KC/L12", name="Kelsby Top Lock", summit="Kelsby", canal="Kelsby Canal", broad=False,
         L=22.10, W=2.16, R=3.04, fill=7.5, empty=6.0, old_no=12, ft=("72' 6\"", "7' 1\"", "9' 11\""),
         site="LCM-0417", fw=datetime(2026, 6, 9, 10, 42), side="east"),
    dict(asset="KC/L13", name="Wharf Lock", summit="Kelsby", canal="Kelsby Canal", broad=False,
         L=21.95, W=2.18, R=2.74, fill=7.0, empty=5.5, old_no=13, ft=("72' 0\"", "7' 2\"", "9' 0\""),
         site="LCM-0418", fw=datetime(2026, 6, 9, 12, 15), side="west"),
    dict(asset="HN/L31", name="Harnock Top Lock", summit="Harnock", canal="Harnock Navigation", broad=True,
         L=22.25, W=4.34, R=1.93, fill=9.0, empty=8.0, old_no=31, ft=("73' 0\"", "14' 3\"", "6' 4\""),
         site="LCM-0522", fw=datetime(2026, 6, 16, 9, 58), side="north"),
    dict(asset="HN/L32", name="Steward's Lock", summit="Harnock", canal="Harnock Navigation", broad=True,
         L=22.10, W=4.32, R=1.84, fill=8.5, empty=7.5, old_no=32, ft=("72' 6\"", "14' 2\"", "6' 0\""),
         site="LCM-0523", fw=datetime(2026, 6, 16, 11, 31), side="south"),
    dict(asset="TC/L08", name="Tilsey Top Lock", summit="Tilsey", canal="Tilsey Canal", broad=False,
         L=21.90, W=2.17, R=2.18, fill=6.5, empty=5.0, old_no=8, ft=("71' 10\"", "7' 1\"", "7' 2\""),
         site="LCM-0609", fw=datetime(2026, 6, 23, 10, 6), side="east"),
    dict(asset="TC/L09", name="Engine Lock", summit="Tilsey", canal="Tilsey Canal", broad=False,
         L=21.95, W=2.16, R=2.09, fill=6.5, empty=5.0, old_no=9, ft=("72' 0\"", "7' 1\"", "6' 10\""),
         site="LCM-0610", fw=datetime(2026, 6, 23, 11, 49), side="west"),
]
for _l in LOCKS:
    _l["lockful"] = round(_l["L"] * _l["W"] * _l["R"], 1)
LOCK = {l["asset"]: l for l in LOCKS}
SUMMIT_LOCKS = {s: [l["asset"] for l in LOCKS if l["summit"] == s] for s in SUMMITS}

# Steward's Lock bottom gate repair, and the Tilsey Top lock-side equipment restriction (local clock).
CLOSURES = {"HN/L32": [(datetime(2026, 5, 12, 8, 0), datetime(2026, 5, 29, 17, 0))]}
TILSEY_CAMERA_OUT = (datetime(2026, 8, 3, 11, 52, 40), datetime(2026, 8, 23, 15, 7, 15))
TILSEY_RESTRICTION = (datetime(2026, 8, 3, 12, 0), datetime(2026, 8, 23, 15, 30))
RESTRICTED_HOURS = (9, 18)

# Kelsby: the Kelsby Ring runs up Kelsby Top Lock and down Wharf Lock for most crews; the hire base at Kelsby
# Wharf lies on the summit pound. Harnock and Tilsey carry through traffic both ways.
TRAFFIC = {
    "Kelsby": dict(through=28.5, ring_main="KC/L12", ring_share=0.84, turn=2.2, moor=0.18, hire_fleet=22),
    "Harnock": dict(through=27.0, turn=3.0, moor=0.22, partner_wait=15.0, company=0.28),
    "Tilsey": dict(through=44.0, turn=4.5, moor=0.15),
}
MONTH_W = {4: 0.62, 5: 0.86, 6: 0.97, 7: 1.12, 8: 1.30, 9: 0.93, 10: 0.58}
DOW_W = [0.86, 0.84, 0.88, 0.95, 1.10, 1.24, 1.13]

# Reservoirs. Rates in Ml a day, the keepers' water day ending at 09:00.
RESERVOIRS = ["Upper Kelsby Reservoir", "Lower Kelsby Reservoir", "Coldmere Reservoir", "Tilsey Reservoir"]
COLDMERE_OLD_B, COLDMERE_NEW_B = 0.75, 0.60
COLDMERE_PLATE_UTC = datetime(2026, 6, 16, 10, 30)
COLDMERE_RATING_LOADED_UTC = datetime(2026, 8, 4, 9, 0)
FOX_HARNOCK_B, FOX_TILSEY_B, FOX_TILSEY_CREST = 0.50, 0.35, 0.060


def weir_q(b, h):
    """sharp-crested rectangular notch with two end contractions, Francis: cubic metres a second."""
    if h <= 0:
        return 0.0
    return 1.84 * (b - 0.2 * h) * h ** 1.5


# Abstraction licences: ref, holder, summit, point, annual licensed quantity (m3), meter digits, use profile
LICENCES = [
    dict(ref="KA/014", holder="Hollins Farm (R. and P. Ashdown)", summit="Kelsby", point="KS-AP03", annual=42000,
         use="irrigation", scale=30500, digits=6),
    dict(ref="KA/022", holder="Kelsby Golf Club Ltd", summit="Kelsby", point="KS-AP07", annual=26000,
         use="greens", scale=17800, digits=6),
    dict(ref="KA/031", holder="Kelsby Wharf Marina Ltd", summit="Kelsby", point="KS-AP11", annual=9500,
         use="marina", scale=6100, digits=6),
    dict(ref="HA/007", holder="Harnock Mill Trout Farm", summit="Harnock", point="HS-AP01", annual=980000,
         use="fishery", scale=468000, digits=5),
    dict(ref="HA/019", holder="Glebe Farm Partnership", summit="Harnock", point="HS-AP05", annual=38000,
         use="irrigation", scale=27300, digits=6),
    dict(ref="HA/026", holder="Carver's Brewery Ltd", summit="Harnock", point="HS-AP09", annual=21000,
         use="process", scale=12900, digits=6),
    dict(ref="TA/003", holder="Tilsey Hall Estate", summit="Tilsey", point="TS-AP02", annual=31000,
         use="lake", scale=19400, digits=6),
    dict(ref="TA/011", holder="Brook Farm (J. Mallender)", summit="Tilsey", point="TS-AP04", annual=34000,
         use="irrigation", scale=24100, digits=6),
    dict(ref="TA/018", holder="Tilsey Quarry Products Ltd", summit="Tilsey", point="TS-AP08", annual=18000,
         use="dust", scale=11200, digits=6),
]
# meter exchanges: licence ref, local datetime of the exchange
EXCHANGES = {"KA/022": datetime(2026, 6, 17, 11, 20), "HA/019": datetime(2026, 7, 8, 10, 5), "HA/026": datetime(2026, 9, 9, 10, 40),
             "TA/011": datetime(2026, 5, 20, 14, 40)}

PEOPLE = {
    "planner": "Katy Wilkinson", "head": "Elaine Freeman", "keeper_lead": "Keith Rahman",
    "volunteers": "Kim Hussain", "asset": "Louis Carey", "counters": "Gillian Walsh",
}
KEEPERS = ["KR", "KH", "PM", "BD", "DA", "RJ"]
ORG = "Coldmere Canals Trust"
