"""The fixed world of task186: the Provincial Statistics Bureau's fuel price monitor, which finds station by station
where the 1 January 2026 rise of the provincial carbon levy was passed on in excess and recommends to the Fuel Price
Commissioner the brand the pass-through inquiry examines before the 1 January 2027 rise. Every other module reads its
constants here."""
import datetime as dt

SEED = 186
BUREAU = "Provincial Statistics Bureau"
DIVISION = "Prices Division"
COMMISSIONER = "Office of the Fuel Price Commissioner"
ACT = "Fuel Price Transparency Act"

LOG_START = dt.date(2025, 1, 1)          # the price-change log runs from here
LOG_END = dt.date(2026, 11, 15)          # to the end of this day (local time)
AS_OF = dt.date(2026, 11, 16)            # the extracts were pulled
MEMO_DATE = dt.date(2026, 11, 27)
PREV_CHANGE = dt.date(2025, 1, 1)
CHANGE = dt.date(2026, 1, 1)             # the levy change the inquiry is judged on
NEXT_CHANGE = dt.date(2027, 1, 1)
WINDOW = 28                              # days each side of a change
MIN_DAYS = 20                            # days with a price in each window for a station to be examined
DAY_FROM, DAY_TO = 6 * 60, 22 * 60       # the daily price window, local minutes
SALES_TAX = 0.05
FDR = 0.05
INQUIRY_SHARE = 0.10
RENUMBER = dt.date(2026, 6, 8)           # the reporting platform's new station numbers take effect
SCOPE_DATE = dt.date(2026, 12, 1)        # the date the inquiry's information request would speak to

# the levy schedule, cents a litre (the regulation's per-litre rates); dollars a tonne of CO2e
LEVY_PER_TONNE = {2025: 95, 2026: 110, 2027: 125}
FACTOR = {"gasoline": 2.307, "diesel": 2.681}       # kg CO2e a litre
LEVY = {fuel: {y: round(t * f / 10.0, 2) for y, t in LEVY_PER_TONNE.items()} for fuel, f in FACTOR.items()}


def levy_regular(d):
    return LEVY["gasoline"][d.year]


BRANDS = [  # code, brand, registered owner, head office
    ("TAL", "Tallis Petroleum", "Tallis Petroleum Holdings Inc.", "Brackwater"),
    ("HBL", "Harbourline Fuels", "Harbourline Energy Ltd.", "Port Ostley"),
    ("PEL", "Pellow Gas", "Pellow Distribution Corp.", "Kellow"),
    ("WEX", "Wexcombe Petroleum", "Wexcombe Petroleum Ltd.", "Greyford"),
    ("OXB", "Oxbury Fuels", "Oxbury Retail Fuels Inc.", "Tamsford"),
    ("STL", "Strathlowe Energy", "Strathlowe Energy Partners LP", "Hollinsby"),
    ("GAR", "Garrow Fuels", "Garrow Fuels Co-operative Ltd.", "Duncarrow"),
]
CODES = [b[0] for b in BRANDS]
NAME = {b[0]: b[1] for b in BRANDS}
INDEPENDENT = "IND"                     # unbranded stations: on the register, not monitored brands

AREAS = [  # code, name
    ("BRK", "Brackwater"), ("POS", "Port Ostley"), ("KEL", "Kellow"), ("TAM", "Tamsford"), ("LIN", "Lindmere"),
    ("TRF", "Torrin Falls"), ("HOL", "Hollinsby"), ("GRY", "Greyford"), ("DUN", "Duncarrow"), ("MRB", "Marrowby"),
    ("QUA", "Quarrow"), ("SAL", "Sallowfield"), ("BRC", "Brindlecote"), ("WYN", "Wyndale"), ("ELV", "Elverton"),
    ("REN", "Rendle Junction"),
]
AREA_CODES = [a[0] for a in AREAS]
AREA_NAME = dict(AREAS)

PEOPLE = {
    "commissioner": ("Theodore Ellis", "Fuel Price Commissioner"),
    "director": ("Kendra Andrews", "Director, Prices Division, " + BUREAU),
    "analyst": ("Kristin Cline", "Senior Analyst, Fuel Price Monitor"),
}

# days the provincial terminal does not publish a rack price (weekends aside)
HOLIDAYS = {dt.date(2025, 1, 1), dt.date(2025, 2, 17), dt.date(2025, 4, 18), dt.date(2025, 5, 19),
            dt.date(2025, 7, 1), dt.date(2025, 8, 4), dt.date(2025, 9, 1), dt.date(2025, 10, 13),
            dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 2, 16),
            dt.date(2026, 4, 3), dt.date(2026, 5, 18), dt.date(2026, 7, 1), dt.date(2026, 8, 3),
            dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2024, 12, 25), dt.date(2024, 12, 26)}


def _nth_sunday(year, month, n):
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def dst_bounds(year):
    """daylight time from 02:00 local on the second Sunday of March to 02:00 local on the first Sunday of November"""
    return _nth_sunday(year, 3, 2), _nth_sunday(year, 11, 1)


def utc_offset_hours(day, minute):
    """local = UTC + offset; standard time UTC-5, daylight time UTC-4"""
    start, end = dst_bounds(day.year)
    if start < day < end or (day == start and minute >= 120) or (day == end and minute < 120):
        return -4
    return -5


def to_utc(day, minute):
    """a local wall-clock minute on a day to a naive UTC datetime"""
    local = dt.datetime.combine(day, dt.time()) + dt.timedelta(minutes=int(minute))
    return local - dt.timedelta(hours=utc_offset_hours(day, minute))


def days_between(d0, d1):
    return [d0 + dt.timedelta(days=k) for k in range((d1 - d0).days + 1)]


DAYS = days_between(LOG_START, LOG_END)
DAY_INDEX = {d: k for k, d in enumerate(DAYS)}
