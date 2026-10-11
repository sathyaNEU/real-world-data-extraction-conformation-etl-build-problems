"""Red Cedar Valley School District's health plan: the fixed facts of the world (dates, people, plan
design, the provider and drug vocabularies). Everything stochastic lives in sim.py."""
import datetime as dt

SEED = 101050

D = dt.date
SIM_START = D(2023, 1, 1)              # a year of history before the first claims anyone uses
SIM_END = D(2028, 3, 31)
CONVERSION = D(2025, 1, 1)            # Ellery Benefit Administrators takes over from Bramwell Plan Services
PAID_THROUGH = D(2027, 2, 28)         # the extracts' paid cut-off
DRAFT_PAID = D(2026, 12, 31)
LETTER_PAID = D(2027, 1, 31)          # the renewal letter's experience cut-off
BID_PAID = D(2024, 12, 31)            # data book: 2024 incurred, paid through December 2024
BID_ELIG = D(2025, 1, 1)
DRAFT_ELIG = D(2027, 1, 1)
FINAL_ELIG = D(2027, 3, 1)
PROG_START, PROG_END = D(2027, 4, 1), D(2028, 3, 31)
ANALOG_START, ANALOG_END = D(2025, 4, 1), D(2026, 3, 31)
ASOF = D(2027, 3, 12)
BOARD = D(2027, 3, 25)

TREND_MED, TREND_RX = 1.065, 1.09
LIST_SIZE = 140
TIERS = ((1, 53.5), (2, 45.5), (3, 40.0), (4, 0.0))   # tier t holds scores at or above its floor

DISTRICT = "Red Cedar Valley School District"
DISTRICT_SHORT = "Red Cedar Valley Schools"
DISTRICT_NO = "ISD 2817"
VENDOR = "Northcourt Care Partners"
CONSULT = "Lindqvist Benefits Consulting"
TPA_OLD = "Bramwell Plan Services"
TPA_NEW = "Ellery Benefit Administrators"
PBM = "Quarrystone Rx"
STOPLOSS = "Wyecliff Life Assurance Company"

PEOPLE = {
    "requester": "Joyce Salinas",        # director of risk management and benefits
    "chair": "Deborah Johnson",          # school board chair
    "cfo": "Anthony Olsen",              # chief financial officer
    "actuary": "Michael Perry",          # consulting actuary, Lindqvist
    "vendor_lead": "Allison Santiago",   # Northcourt account lead
    "analyst": "Tiffany Barrett",        # benefits analyst
    "vendor_officer": "Phillip Alvarado",  # Northcourt chief operating officer, signs the agreement
    "vendor_analyst": "Amy Kelley",      # Northcourt clinical analytics
    "pbm_rep": "Michelle Peterson",      # Quarrystone Rx client account executive
    "carrier_officer": "Jonathan Hoffman",  # Wyecliff, vice president, stop-loss underwriting
    "superintendent": "Sandra Lopez",    # superintendent, countersigns the agreement
}

# plan design (per member, plan year 1 July to 30 June)
PLANS = {
    "PPO": dict(ded=500.0, coins=0.20, oop=3600.0, pcp_copay=25.0, spec_copay=40.0, er_copay=200.0, uc_copay=50.0,
                rx=dict(G=10.0, P=40.0, N=70.0, S=(0.20, 250.0))),
    "HDHP": dict(ded=3300.0, coins=0.10, oop=6500.0, pcp_copay=None, spec_copay=None, er_copay=None, uc_copay=None,
                 rx=None),
}
PLAN_CODE = {"PPO": "RCV-PPO", "HDHP": "RCV-HSA"}


def month_index(d):
    return (d.year - SIM_START.year) * 12 + d.month - 1


def month_start(i):
    y, m = divmod(SIM_START.month - 1 + i, 12)
    return D(SIM_START.year + y, m + 1, 1)


def month_end(i):
    return month_start(i + 1) - dt.timedelta(days=1)


N_MONTHS = month_index(SIM_END) + 1


def add_months(d, k):
    y, m = divmod(d.month - 1 + k, 12)
    return D(d.year + y, m + 1, 1)


def npi_check(base9):
    """Luhn check digit over the NPI with its 80840 prefix."""
    digits = "80840" + base9
    total = 0
    for i, ch in enumerate(reversed(digits)):
        v = int(ch)
        if i % 2 == 0:
            v *= 2
            if v > 9:
                v -= 9
        total += v
    return str((10 - total % 10) % 10)


def make_npi(base9):
    return base9 + npi_check(base9)


# ------------------------------------------------------------------ calendars
def _nth_weekday(y, m, wd, n):
    """n-th weekday wd (Monday 0) of a month; n = -1 for the last"""
    if n > 0:
        d = D(y, m, 1)
        while d.weekday() != wd:
            d += dt.timedelta(days=1)
        return d + dt.timedelta(days=7 * (n - 1))
    d = D(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else D(y, 12, 31)
    while d.weekday() != wd:
        d -= dt.timedelta(days=1)
    return d


def _observed(d):
    return d - dt.timedelta(days=1) if d.weekday() == 5 else d + dt.timedelta(days=1) if d.weekday() == 6 else d


def _holidays():
    clinic, reduced, bank = set(), set(), set()
    for y in range(2023, 2030):
        ny, j4, xm = _observed(D(y, 1, 1)), _observed(D(y, 7, 4)), _observed(D(y, 12, 25))
        mem, lab, thx = _nth_weekday(y, 5, 0, -1), _nth_weekday(y, 9, 0, 1), _nth_weekday(y, 11, 3, 4)
        clinic |= {D(y, 1, 1), D(y, 7, 4), D(y, 12, 25), ny, j4, xm, mem, lab, thx}
        reduced |= {D(y, 12, 24), D(y, 12, 31), thx + dt.timedelta(days=1), _nth_weekday(y, 1, 0, 3),
                    _nth_weekday(y, 2, 0, 3)}
        bank |= {ny, _nth_weekday(y, 1, 0, 3), _nth_weekday(y, 2, 0, 3), mem, _observed(D(y, 6, 19)), j4, lab,
                 _nth_weekday(y, 10, 0, 2), _observed(D(y, 11, 11)), thx, xm}
    return clinic, reduced - clinic, bank


CLINIC_CLOSED, CLINIC_REDUCED, BANK_HOLIDAYS = _holidays()


def _check_runs():
    """Ellery releases the District's claim payments once a week, on Thursday, or on the next business day when the
    Thursday is a bank holiday"""
    out = []
    d = D(2023, 12, 7)
    while d <= D(2029, 12, 31):
        r = d
        while r in BANK_HOLIDAYS or r.weekday() >= 5:
            r += dt.timedelta(days=1)
        out.append(r)
        d += dt.timedelta(days=7)
    return out


CHECK_RUNS = _check_runs()


def next_check_run(d):
    import bisect
    return CHECK_RUNS[bisect.bisect_left(CHECK_RUNS, d)]


def next_business_day(d):
    while d.weekday() >= 5 or d in BANK_HOLIDAYS:
        d += dt.timedelta(days=1)
    return d
