"""task501 world: a Swiss pension foundation's private-markets programme and its 2027 standby facility.

Facts only: the calendar, the managers and fund commitments, the pacing parameters of the simulation, the
facility's terms and the people. Nothing here reads a shipped file.
"""
from datetime import date, timedelta

SEED = 501

PLAN_DATE = date(2026, 12, 31)          # the plan date and the extract's close
EXTRACT_RUN = date(2027, 1, 5)           # the extract run
ELECTION_DUE = date(2027, 1, 15)         # the lender's election date
FIRST_YEAR = 2015
LAST_MONTH = (2026, 12)
FORWARD_END = (2027, 12)                 # simulated beyond the extract for the record only, never shipped

ORG = "Pensionskasse Werdinsel"
ORG_SHORT = "PK Werdinsel"
BANK = "Privatbank Lindenhof AG"
CUSTODIAN = "Privatbank Lindenhof AG, Global Custody"
PEOPLE = {
    "treasury": "Domenica Hürlimann",      # Leiterin Treasury & Liquidität
    "pm": "Torsten Sigrist",               # Leiter Portfolio Management Privatmärkte
    "accounting": "Noémie Hess",           # Rechnungswesen
    "president": "Jeremias Ritter",        # Präsident des Stiftungsrats
    "bank": "Lazar Marti",                 # Relationship manager, Privatbank Lindenhof
}

STRATEGIES = {"BO": "Buyout", "GR": "Growth", "PC": "Private credit", "IN": "Infrastructure"}
STRATEGY_DE = {"BO": "Buyout", "GR": "Wachstumskapital", "PC": "Privatkredit", "IN": "Infrastruktur"}

# facility terms (directive RL-PM-05 and the lender's term sheet)
RESERVE = 150_000_000.0
MIN_BALANCE = 5_000_000.0                # the programme account's operating minimum, below which the facility is drawn
MARGIN = 0.10
MENU = list(range(50, 401, 25))          # CHF million
COMMIT_FEE = 0.0030                      # per annum on the facility amount, drawn or not
ARRANGE_FEE = 0.0015                     # flat on the facility amount

# (name, code, strategy, currency, domicile, paying agent, on the custodian's CF-PM portal)
MANAGERS = [
    ("Aldringen Capital", "ALD", "BO", "USD", "DE", "Aldringen Fund Services S.a r.l.", False),
    ("Brantwood Partners", "BRW", "BO", "USD", "GB", "Brantwood Fund Administration Ltd", True),
    ("Corvisart Equity", "COR", "BO", "EUR", "FR", "Corvisart Equity Gestion SAS", False),
    ("Loschwitz Equity", "LOS", "BO", "EUR", "DE", "Loschwitz Equity Verwaltungs GmbH", False),
    ("Rosenthal Buyout Partners", "ROS", "BO", "USD", "US", "Rosenthal Fund Services LLC", True),
    ("Quendel Partners", "QUE", "BO", "CHF", "CH", "Quendel Partners AG", False),
    ("Marignane Capital", "MAR", "BO", "EUR", "FR", "Marignane Gestion SAS", False),
    ("Gosford Growth Partners", "GOS", "GR", "USD", "US", "Gosford Fund Administration LLC", True),
    ("Norrland Growth", "NOR", "GR", "EUR", "SE", "Norrland Fund Services AB", True),
    ("Stavanger Growth Capital", "STA", "GR", "EUR", "NO", "Stavanger Fondsforvaltning AS", False),
    ("Isenring Private Capital", "ISE", "GR", "CHF", "CH", "Isenring Private Capital AG", False),
    ("Ebersol Credit", "EBE", "PC", "USD", "US", "Ebersol Credit Administration LLC", True),
    ("Halvorsen Credit Partners", "HAL", "PC", "EUR", "DK", "Halvorsen Fondsadministration A/S", False),
    ("Kalmar Mezzanine", "KAL", "PC", "EUR", "SE", "Kalmar Fund Services AB", True),
    ("Pellworm Credit", "PEL", "PC", "USD", "DE", "Pellworm Credit Services GmbH", False),
    ("Tessin Private Credit", "TES", "PC", "EUR", "CH", "Tessin Private Credit AG", False),
    ("Dunmore Infrastructure", "DUN", "IN", "EUR", "IE", "Dunmore Fund Administration DAC", True),
    ("Juneau Infrastructure Partners", "JUN", "IN", "USD", "US", "Juneau Fund Services LLC", False),
    ("Ostermalm Infrastructure", "OST", "IN", "EUR", "SE", "Ostermalm Fondadministration AB", True),
    ("Ulmenhof Capital", "ULM", "IN", "CHF", "CH", "Ulmenhof Capital AG", False),
]
MGR = {m[1]: i for i, m in enumerate(MANAGERS)}

# (manager code, fund number, first close (y, m), commitment in fund currency millions, pace factor)
# pace below one: a slow deployer; the record's slow starters (BRW II, ULM II, QUE III, COR VI, ISE II) and the four
# funds whose investment periods end in late 2027 (LOS III, JUN II, ROS II, TES I).
FUNDS = [
    ("ALD", "III", (2015, 4), 60, 1.00), ("DUN", "II", (2015, 7), 80, 1.00), ("COR", "VI", (2015, 9), 50, 0.42),
    ("BRW", "II", (2016, 1), 45, 0.34), ("ULM", "II", (2016, 3), 55, 0.34), ("GOS", "II", (2016, 5), 30, 1.00),
    ("EBE", "II", (2016, 8), 70, 1.00), ("QUE", "III", (2016, 10), 35, 0.40),
    ("JUN", "I", (2017, 4), 90, 1.00), ("LOS", "II", (2017, 6), 40, 1.00), ("NOR", "I", (2017, 11), 35, 1.10),
    ("HAL", "I", (2018, 1), 60, 1.10), ("ROS", "I", (2018, 3), 65, 1.10), ("ISE", "II", (2018, 6), 30, 0.38),
    ("MAR", "IV", (2018, 9), 50, 1.10),
    ("ALD", "IV", (2019, 2), 75, 1.30), ("KAL", "III", (2019, 5), 65, 1.30), ("GOS", "III", (2019, 8), 40, 1.30),
    ("OST", "I", (2019, 9), 70, 1.25), ("COR", "VII", (2019, 11), 70, 1.30),
    ("STA", "III", (2020, 4), 40, 1.30), ("DUN", "III", (2020, 6), 100, 1.30), ("BRW", "III", (2020, 9), 55, 1.35),
    ("EBE", "III", (2020, 12), 90, 1.35),
    ("QUE", "IV", (2021, 6), 45, 1.40), ("PEL", "I", (2021, 9), 70, 1.40), ("ISE", "III", (2021, 9), 40, 1.40),
    # investment periods ending January to August 2027, on schedule
    ("NOR", "II", (2022, 1), 50, 1.30), ("ULM", "III", (2022, 3), 60, 1.25), ("STA", "IV", (2022, 5), 40, 1.20),
    ("OST", "II", (2022, 7), 45, 1.25), ("HAL", "II", (2023, 2), 85, 1.30), ("KAL", "IV", (2023, 5), 50, 1.20),
    # investment periods ending September to December 2027, far behind schedule
    ("LOS", "III", (2022, 9), 80, 0.36), ("JUN", "II", (2022, 10), 160, 0.36), ("ROS", "II", (2022, 11), 110, 0.36),
    ("TES", "I", (2023, 12), 170, 0.35),
    # later vintages (no first close from December 2022 to June 2023 for five-year funds, or in the first half of
    # 2024 for four-year credit funds: the programme paused new commitments while it was over its allocation)
    ("GOS", "IV", (2023, 7), 70, 1.00), ("ALD", "V", (2023, 10), 100, 1.00), ("COR", "VIII", (2024, 2), 90, 1.10),
    ("EBE", "IV", (2024, 9), 120, 1.10), ("MAR", "V", (2024, 9), 80, 1.10), ("KAL", "V", (2024, 10), 110, 1.10),
    ("PEL", "II", (2025, 1), 70, 1.10), ("BRW", "IV", (2025, 3), 65, 1.10), ("STA", "V", (2025, 6), 50, 1.10),
    ("DUN", "IV", (2025, 9), 90, 1.10), ("ROS", "III", (2025, 10), 70, 1.00), ("NOR", "III", (2026, 1), 50, 1.00),
    ("JUN", "III", (2026, 3), 80, 1.00), ("HAL", "III", (2026, 9), 70, 1.00),
]
DEADLINE_GROUP = ("LOS-III", "JUN-II", "ROS-II", "TES-I")

IP_MONTHS = {"BO": 60, "GR": 60, "PC": 48, "IN": 60}
TERM_MONTHS = {"BO": 120, "GR": 120, "PC": 96, "IN": 144}
TAU_TARGET = 0.926                                                # the drawn share (investments, fees, expenses) managers aim for at the IP end
IOTA_SD = 0.0015                                                  # each fund's spread around that aim (share of commitment)
H = {"BO": 0.060, "GR": 0.060, "PC": 0.065, "IN": 0.055}         # monthly pacing hazard on the investable balance
FEE_IP = {"BO": 0.016, "GR": 0.016, "PC": 0.009, "IN": 0.012}    # management fee p.a. on commitment in the IP
FEE_POST = {"BO": 0.012, "GR": 0.012, "PC": 0.008, "IN": 0.010}  # p.a. on net invested cost after the IP
DRAWDOWN_MONTHS = 6                                               # a fund draws its balance in its last six IP months

# holds and outcomes of investments
HOLD = {"BO": (62, 16, 30, 110), "GR": (54, 16, 24, 100), "PC": (34, 10, 14, 66), "IN": (84, 22, 40, 150)}
MULT = {"BO": (1.80, 0.45), "GR": (2.05, 0.75), "PC": (1.035, 0.03), "IN": (1.40, 0.25)}
LOSS_SHARE = {"BO": 0.12, "GR": 0.16, "PC": 0.05, "IN": 0.05}
INCOME_Q = {"BO": 0.0, "GR": 0.0, "PC": 0.021, "IN": 0.013}      # quarterly income on held cost

# the custodian's CF-PM feed and the clerks' parallel keying of the same managers' distribution notices in 2026
FEED_START = {"BRW": date(2026, 1, 1), "ROS": date(2026, 1, 1), "GOS": date(2026, 1, 1), "NOR": date(2026, 1, 1),
              "EBE": date(2026, 1, 1), "DUN": date(2026, 1, 1), "OST": date(2026, 1, 1), "KAL": date(2026, 4, 1)}
CLERK_STOP = {"EBE": date(2026, 7, 1), "DUN": date(2026, 7, 1)}  # the clerks stopped keying these managers in July
PARALLEL_END = date(2026, 9, 30)                                  # the clerks stopped keying every feed manager
DIST_STREAM = 360                                                  # random stream of the 2025-26 distribution timings


def market(y, m):
    """Deal environment: the 2020 pause, the 2021 boom, the 2023-24 drought."""
    if y < 2020:
        return 1.0
    if y == 2020:
        return 0.30 if 3 <= m <= 9 else 1.0
    if y == 2021:
        return 1.25
    if y == 2022:
        return 1.05 if m <= 6 else 0.90
    if y == 2023:
        return 0.80
    if y == 2024:
        return 0.85
    return 0.95


def month_index(y, m):
    return (y - FIRST_YEAR) * 12 + (m - 1)


def ym(idx):
    return FIRST_YEAR + idx // 12, idx % 12 + 1


def month_end(idx):
    y, m = ym(idx)
    nxt = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return nxt - timedelta(days=1)


def add_months(d, n):
    y, m = d.year, d.month + n
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    last = (date(y + (m == 12), 1 if m == 12 else m + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, last))


def bday(d):
    while d.weekday() >= 5 or (d.month, d.day) in ((1, 1), (12, 25), (12, 26), (1, 2), (8, 1)):
        d += timedelta(days=1)
    return d


def bday_back(d):
    while d.weekday() >= 5 or (d.month, d.day) in ((1, 1), (12, 25), (12, 26), (1, 2), (8, 1)):
        d -= timedelta(days=1)
    return d


def add_bdays(d, n):
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5 and (d.month, d.day) not in ((1, 1), (12, 25), (12, 26), (1, 2), (8, 1)):
            n -= 1
    return d
