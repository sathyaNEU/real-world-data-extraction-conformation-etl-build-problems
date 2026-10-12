"""Fixed facts of the world: dates, markets, presentations, risks, laboratories."""
import datetime as dt

D = dt.date
LOCK = D(2026, 9, 30)            # PSUR 6 data lock point
EXPORT = D(2026, 10, 6)          # safety database and supply extraction runs
LAUNCH = D(2023, 4, 3)           # first commercial supply (Denmark)
EU_AUTH = D(2023, 2, 14)         # EU marketing authorisation, EU/1/23/1754
INTERVAL_START = D(2025, 10, 1)  # PSUR 6 reporting interval
FIRST_WEEK = D(2023, 4, 3)
LAST_WEEK = D(2026, 9, 28)
RAMP_WEEKS = 43.0
PHI = 0.6180339887498949
SQ2 = 0.4142135623730951
SQ3 = 0.7320508075688772
SQ5 = 0.2360679774997898
SQ7 = 0.6457513110645906

# market: launch Monday, steady weekly starts, ISO name
MARKETS = {
    "DK": (D(2023, 4, 3), 21, "Denmark"),
    "DE": (D(2023, 5, 8), 200, "Germany"),
    "SE": (D(2023, 6, 5), 36, "Sweden"),
    "NO": (D(2023, 6, 12), 18, "Norway"),
    "FI": (D(2023, 9, 4), 16, "Finland"),
    "NL": (D(2024, 3, 4), 50, "Netherlands"),
    "BE": (D(2024, 6, 3), 34, "Belgium"),
    "AT": (D(2024, 9, 2), 26, "Austria"),
    "FR": (D(2025, 2, 3), 240, "France"),
    "IT": (D(2025, 5, 5), 205, "Italy"),
    "ES": (D(2025, 9, 1), 165, "Spain"),
    "PL": (D(2025, 11, 3), 110, "Poland"),
    "PT": (D(2026, 1, 5), 34, "Portugal"),
}
MARKET_ORDER = list(MARKETS)
HOSPITAL_MARKETS = ("FR", "IT", "ES")

RISKS = ["ild", "zoster", "infection", "vte", "hepatic", "neutropenia"]
RISK_LABEL = {
    "ild": "Interstitial lung disease",
    "zoster": "Herpes zoster",
    "infection": "Serious infections",
    "vte": "Venous thromboembolism",
    "hepatic": "Hepatotoxicity",
    "neutropenia": "Neutropenia",
}


def weeks():
    out, d = [], FIRST_WEEK
    while d <= LAST_WEEK:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def weekly_starts(week, market):
    launch, size, _ = MARKETS[market]
    k = (week - launch).days // 7
    if k < 0:
        return 0.0
    return size * min(1.0, (k + 1) / RAMP_WEEKS)


def trunc_days(start):
    """Days from a course's first dose (day 1) to the data lock point, inclusive."""
    return (LOCK - start).days + 1


def frac(v):
    return v - int(v // 1)
