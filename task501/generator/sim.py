"""task501 world and simulation: a Swiss pension fund's private-markets programme.

Everything is simulated forward in fund currency at monthly resolution, then written by pack.py.
Nothing here reads a target file. All graded figures are computed afterwards by solve.py from the
shipped files alone.
"""
import math
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

SEED = 118
EXTRACT = date(2026, 9, 30)            # plan date and extract date
FIRST_MONTH = (2015, 1)
LAST_MONTH = (2026, 9)

STRATEGIES = {"BO": "Buyout", "GR": "Growth", "PC": "Private credit", "IN": "Infrastructure"}
RECYCLE_MONTHS = 18                      # the unstated recycling rule
HOLD_GAP = (515, 585)                    # no realised hold lands in this many days (convergence)
CALL_CAP_SHARE = 0.965                   # no fund's cumulative calls pass this share of commitment
# deployment pace by fund code: fast deployers are the private-credit managers whose 2024-25 loans prepaid in 2026
PACE = {"EBE-IV": 1.3, "KAL-IV": 1.3, "PEL-II": 1.2, "TES-I": 1.3, "HAL-II": 1.05, "HAL-III": 1.0,
        "EBE-III": 0.85, "HAL-I": 0.85, "KAL-III": 0.85, "PEL-I": 0.85, "EBE-II": 0.9,
        "ALD-V": 1.25, "GOS-IV": 1.2, "ALD-IV": 0.85, "COR-VII": 0.9, "JUN-II": 0.85, "DUN-IV": 0.9}
# managers close most deals in the first half: calls run well ahead of an even spread until June and fall away after
SEASON = {1: 1.6, 2: 1.5, 3: 1.5, 4: 1.4, 5: 1.35, 6: 1.25, 7: 0.6, 8: 0.45, 9: 0.5, 10: 0.55, 11: 0.6, 12: 0.5}
WAVE_FUNDS = {"EBE-IV", "KAL-IV", "PEL-II", "TES-I", "HAL-II"}
HIST_FLIPPERS = {"ALD-V": 0.50, "GOS-IV": 0.32}   # quick flips in 2024-25, inside the audited record
IP_LIMB_CASES = {"EBE-III", "KAL-III", "ALD-IV"}   # a late investment exited after the investment period ended
QUICK_LATE = {"BO": 0.03, "GR": 0.05, "PC": 0.06, "IN": 0.01}

PEOPLE = {
    "treasury": "Serena Sidler",
    "cio": "Luciano Hotz",
    "pm": "Othmar Suter",
    "bank": "Enrique Hofer",
    "accounting": "Noelia Amrein",
    "president": "Marino Imhof",
}
ORG = "Pensionskasse Werdinsel"
BANK = "Privatbank Lindenhof AG"


def month_index(y, m):
    return (y - 2015) * 12 + (m - 1)


def ym(idx):
    return 2015 + idx // 12, idx % 12 + 1


def month_start(idx):
    y, m = ym(idx)
    return date(y, m, 1)


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
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def bday_back(d):
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


# ------------------------------------------------------------------ managers and funds
MANAGERS = [
    ("Aldringen Capital", "ALD", "BO", "USD", "DE"),
    ("Brantwood Partners", "BRW", "BO", "USD", "GB"),
    ("Corvisart Equity", "COR", "BO", "EUR", "FR"),
    ("Loschwitz Equity", "LOS", "BO", "EUR", "DE"),
    ("Rosenthal Buyout Partners", "ROS", "BO", "USD", "US"),
    ("Quendel Partners", "QUE", "BO", "CHF", "CH"),
    ("Marignane Capital", "MAR", "BO", "EUR", "FR"),
    ("Gossamer Growth", "GOS", "GR", "USD", "US"),
    ("Norrland Growth", "NOR", "GR", "EUR", "SE"),
    ("Stavanger Growth Capital", "STA", "GR", "EUR", "NO"),
    ("Isenring Private Capital", "ISE", "GR", "CHF", "CH"),
    ("Ebersol Credit", "EBE", "PC", "USD", "US"),
    ("Halvorsen Credit Partners", "HAL", "PC", "EUR", "DK"),
    ("Kalmar Mezzanine", "KAL", "PC", "EUR", "SE"),
    ("Pellworm Credit", "PEL", "PC", "USD", "DE"),
    ("Tessin Private Credit", "TES", "PC", "EUR", "CH"),
    ("Dunmore Infrastructure", "DUN", "IN", "EUR", "IE"),
    ("Juno Infrastructure Partners", "JUN", "IN", "USD", "US"),
    ("Ostermalm Infrastructure", "OST", "IN", "EUR", "SE"),
    ("Ulmenhof Capital", "ULM", "IN", "CHF", "CH"),
]

# (manager idx, fund number, vintage first close, commitment in fund ccy millions)
FUND_SPECS = [
    (0, "III", (2015, 4), 60), (0, "IV", (2019, 2), 75), (0, "V", (2023, 5), 120),
    (1, "II", (2016, 1), 45), (1, "III", (2020, 9), 55), (1, "IV", (2025, 3), 100),
    (2, "VI", (2015, 9), 50), (2, "VII", (2019, 11), 70), (2, "VIII", (2024, 2), 110),
    (3, "II", (2017, 6), 40), (3, "III", (2022, 3), 55),
    (4, "I", (2018, 3), 65), (4, "II", (2022, 10), 85),
    (5, "III", (2016, 10), 35), (5, "IV", (2021, 6), 45),
    (6, "IV", (2018, 9), 50), (6, "V", (2024, 9), 100),
    (7, "II", (2016, 5), 30), (7, "III", (2019, 8), 40), (7, "IV", (2023, 1), 70),
    (8, "I", (2017, 11), 35), (8, "II", (2021, 10), 50),
    (9, "III", (2020, 4), 40), (9, "IV", (2025, 6), 70),
    (10, "II", (2018, 6), 30),
    (11, "II", (2016, 8), 70), (11, "III", (2020, 2), 90), (11, "IV", (2023, 9), 170),
    (12, "I", (2018, 1), 60), (12, "II", (2022, 6), 85),
    (13, "III", (2019, 5), 65), (13, "IV", (2023, 10), 160),
    (14, "I", (2021, 3), 70), (14, "II", (2025, 1), 110),
    (15, "I", (2023, 8), 120),
    (16, "II", (2015, 7), 80), (16, "III", (2020, 6), 100), (16, "IV", (2025, 9), 150),
    (17, "I", (2017, 4), 90), (17, "II", (2022, 1), 120),
    (18, "I", (2019, 9), 70),
    (19, "II", (2016, 3), 55), (19, "III", (2021, 11), 60),
    (4, "III", (2025, 10), 110), (17, "III", (2026, 3), 130), (8, "III", (2026, 1), 70),
    (12, "III", (2026, 9), 120),      # committed, no first call yet
]

IP_MONTHS = {"BO": 60, "GR": 60, "PC": 48, "IN": 60}
TERM_MONTHS = {"BO": 120, "GR": 120, "PC": 96, "IN": 144}
CALL_PROB = {"BO": 0.46, "GR": 0.46, "PC": 0.48, "IN": 0.46}
CALL_SIZE = {"BO": (0.016, 0.05), "GR": (0.016, 0.05), "PC": (0.017, 0.052), "IN": (0.016, 0.05)}
POST_IP_PROB = {"BO": 0.10, "GR": 0.09, "PC": 0.07, "IN": 0.08}
FEE_Q = {"BO": 0.00375, "GR": 0.00375, "PC": 0.0025, "IN": 0.0030}
FEE_Q_POST = {"BO": 0.0020, "GR": 0.0020, "PC": 0.0015, "IN": 0.0020}
HOLD = {"BO": (66, 18, 14, 108), "GR": (56, 18, 10, 96), "PC": (38, 12, 7, 66), "IN": (88, 24, 24, 150)}
QUICK_SHARE = {"BO": 0.045, "GR": 0.08, "PC": 0.11, "IN": 0.012}
NEAR_SHARE = {"BO": 0.05, "GR": 0.06, "PC": 0.07, "IN": 0.02}
MULT = {"BO": (1.75, 0.45), "GR": (2.1, 0.8), "PC": (1.04, 0.03), "IN": (1.35, 0.25)}
LOSS_SHARE = {"BO": 0.12, "GR": 0.16, "PC": 0.05, "IN": 0.05}
INCOME_Q = {"BO": 0.0, "GR": 0.0, "PC": 0.021, "IN": 0.013}

LEI_PREFIX = {"DE": "5299", "GB": "2138", "FR": "9695", "US": "5493", "CH": "5067", "SE": "5493", "NO": "5967", "DK": "5299", "IE": "6354"}


def lei_for(seed_rng, country):
    body = LEI_PREFIX.get(country, "5493") + "00" + "".join(seed_rng.choice(list("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"), 12))
    # ISO 17442 check digits (mod 97)
    s = "".join(str(int(c, 36)) for c in body) + "00"
    chk = 98 - int(s) % 97
    return body + f"{chk:02d}"


COMPANY_PRE = ["Nor", "Vel", "Kar", "Bel", "Tam", "Ost", "Lir", "Fen", "Mar", "Sol", "Hal", "Dor", "Rav", "Tor",
               "Quin", "Ald", "Bran", "Cor", "Dun", "Eber", "Gal", "Hel", "Ira", "Jor", "Kel", "Lun", "Mol", "Nev",
               "Orl", "Pal", "Ren", "Sab", "Tal", "Ulm", "Var", "Wen", "Yor", "Zel", "Ant", "Bor"]
COMPANY_SUF = ["tek", "mat", "vion", "dyne", "core", "line", "works", "sys", "med", "logis", "pharma", "grid",
               "net", "fab", "form", "wave", "steel", "pack", "data", "care", "build", "fleet", "hydro", "optic"]
LEGAL = {"DE": "GmbH", "FR": "SAS", "NL": "B.V.", "GB": "Ltd", "US": "Inc.", "CH": "AG", "IT": "S.p.A.", "ES": "S.L.",
         "SE": "AB", "DK": "A/S", "AT": "GmbH", "BE": "NV", "IE": "Ltd", "FI": "Oy", "NO": "AS", "PL": "Sp. z o.o."}
COUNTRIES = list(LEGAL)
SECTORS = ["C Manufacturing", "J Information and communication", "M Professional services", "Q Human health",
           "G Wholesale and retail", "H Transportation and storage", "D Energy supply", "N Administrative services",
           "F Construction", "K Financial services", "E Water and waste", "I Accommodation and food"]
INSTR = {"BO": "Equity", "GR": "Preferred equity", "PC": "Senior secured loan", "IN": "Equity"}


@dataclass
class Investment:
    ref: str
    company: str
    country: str
    sector: str
    instrument: str
    initial_date: date
    cost: float = 0.0
    tranches: list = field(default_factory=list)      # (date, amount)
    hold_days: int = 0
    exit_date: date = None
    multiple: float = 1.0
    status: str = "HELD"
    realised_roc: float = 0.0
    realised_gain: float = 0.0
    recallable: float = 0.0


@dataclass
class Fund:
    fund_id: str
    code: str
    name: str
    manager: str
    strategy: str
    ccy: str
    domicile: str
    vintage: int
    commitment: float
    first_close: date
    final_close: date
    ip_end: date
    term_end: date
    lei: str
    first_call_month: int = None
    cum_calls: float = 0.0
    cum_dist: float = 0.0
    recallable: float = 0.0
    investments: list = field(default_factory=list)
    notices: list = field(default_factory=list)     # dicts
    nav_q: dict = field(default_factory=dict)       # (y, q) -> nav
    n_inv: int = 0

    @property
    def unfunded_true(self):
        return self.commitment - self.cum_calls + self.recallable


def build_funds():
    rng = np.random.RandomState(SEED * 7)
    funds = []
    for i, (mi, num, (vy, vm), cm) in enumerate(FUND_SPECS):
        mname, code, strat, ccy, dom = MANAGERS[mi]
        fc = date(vy, vm, int(rng.randint(5, 26)))
        f = Fund(
            fund_id=f"PKW-F-{101 + i:03d}", code=f"{code}-{num}", name=f"{mname} {num}", manager=mname,
            strategy=strat, ccy=ccy, domicile=dom, vintage=vy, commitment=cm * 1_000_000.0,
            first_close=fc, final_close=add_months(fc, int(rng.randint(6, 15))),
            ip_end=add_months(fc, IP_MONTHS[strat]), term_end=add_months(fc, TERM_MONTHS[strat]),
            lei=lei_for(rng, dom),
        )
        funds.append(f)
    return funds


# ------------------------------------------------------------------ FX
def build_fx():
    """Daily custodian reference rates, business days 2015-01-02 .. 2026-09-30."""
    rng = np.random.RandomState(SEED * 11)
    rows = []
    usd, eur = 0.995, 1.203
    d = date(2015, 1, 2)
    # yearly drift targets for realism
    while d <= EXTRACT:
        if d.weekday() < 5:
            t = (d - date(2015, 1, 1)).days / 365.25
            usd_target = 0.995 - 0.018 * t
            eur_target = 1.20 - 0.024 * t if t < 1 else 1.10 - 0.015 * (t - 1)
            usd += 0.08 * (usd_target - usd) / 60 + rng.normal(0, 0.0032)
            eur += 0.08 * (eur_target - eur) / 60 + rng.normal(0, 0.0022)
            rows.append((d, round(usd, 4) + (0.0001 if d in (date(2026, 9, 30), date(2023, 3, 31)) else 0.0),
                         round(eur, 4) + (0.0002 if d.year == 2026 and d.month == 2 else 0.0) + (0.0001 if d == date(2025, 12, 31) else 0.0)))
        d += timedelta(days=1)
    return rows


# ------------------------------------------------------------------ simulation
def simulate():
    funds = build_funds()
    fx = build_fx()
    last_idx = month_index(*LAST_MONTH)
    company_names = set()
    for fi, f in enumerate(funds):
        rng = np.random.RandomState(SEED * 1000 + fi)
        s = f.strategy
        fc_idx = month_index(f.first_close.year, f.first_close.month)
        f.first_call_month = fc_idx + int(rng.randint(1, 3))
        if f.first_call_month > last_idx:
            continue                       # committed, no first call yet
        ip_end_idx = month_index(f.ip_end.year, f.ip_end.month)
        cn = dn = 0
        call_cap = f.commitment * float(rng.uniform(0.925, 0.992))
        fund_pace = float(rng.uniform(0.72, 1.32))
        pending_exits = []
        for m in range(f.first_call_month, last_idx + 1):
            y, mo = ym(m)
            in_ip = m <= ip_end_idx
            lines = []
            # ---------------- capital call
            if mo == 1 or m == f.first_call_month:
                year_pace = float(np.exp(rng.normal(0.0, 0.38)))     # each fund's year has its own rhythm
            pace = PACE.get(f.code, 1.0) * fund_pace * year_pace * SEASON[mo]
            want = (m == f.first_call_month) or (rng.rand() < min(0.95, (CALL_PROB[s] if in_ip else POST_IP_PROB[s]) * pace))
            amt = 0.0
            if want and f.unfunded_true > f.commitment * 0.004:
                lo, hi = CALL_SIZE[s]
                amt = f.commitment * rng.uniform(lo, hi) * (1.0 if in_ip else 0.35)
                amt = min(amt, f.unfunded_true * 0.97, max(0.0, call_cap - f.cum_calls))
                if y == 2026 and f.code in WAVE_FUNDS:
                    amt = min(amt, max(0.0, f.commitment * 0.955 - f.cum_calls))   # redeployment pipeline is 2027
                amt = math.floor(amt / 1000) * 1000.0
                if amt < f.commitment * 0.003:
                    amt = 0.0
            if amt > 0:
                notice_date = bday(date(y, mo, int(rng.randint(2, 24))))
                due = bday(notice_date + timedelta(days=int(rng.randint(9, 15))))
                if due.month != notice_date.month and notice_date.month == 12:
                    due = bday_back(date(y, 12, 30))
                n_parts = 1 if amt < f.commitment * 0.02 else int(rng.choice([1, 2, 2, 3, 3]))
                parts = rng.dirichlet(np.ones(n_parts) * 3) * amt if n_parts > 1 else np.array([amt])
                parts = [math.floor(p / 1000) * 1000.0 for p in parts]
                parts = [p for p in parts if p >= f.commitment * 0.003]
                if not parts:
                    parts = [amt]
                amt = float(sum(parts))
                for part in parts:
                    # new company or follow-on
                    held = [iv for iv in f.investments if iv.status == "HELD"]
                    follow = held and rng.rand() < 0.28 and in_ip
                    if follow:
                        iv = held[int(rng.randint(len(held)))]
                        iv.cost += part
                        iv.tranches.append((due, part))
                    else:
                        f.n_inv += 1
                        while True:
                            ctry = COUNTRIES[int(rng.randint(len(COUNTRIES)))] if rng.rand() < 0.7 else f.domicile
                            nm = COMPANY_PRE[int(rng.randint(len(COMPANY_PRE)))] + COMPANY_SUF[int(rng.randint(len(COMPANY_SUF)))]
                            nm = nm[0].upper() + nm[1:] + " " + LEGAL[ctry]
                            if nm not in company_names:
                                company_names.add(nm)
                                break
                        iv = Investment(ref=f"{f.code}-{f.n_inv:02d}", company=nm, country=ctry,
                                        sector=SECTORS[int(rng.randint(len(SECTORS)))], instrument=INSTR[s],
                                        initial_date=due, cost=part, tranches=[(due, part)])
                        # hold and outcome
                        mean, sd, lo_m, hi_m = HOLD[s]
                        u = rng.rand()
                        qs = QUICK_SHARE[s] if due >= date(2023, 1, 1) else 0.002
                        if due >= date(2023, 1, 1):
                            qs = QUICK_LATE[s]
                        if f.code in WAVE_FUNDS:
                            qs = 0.02
                        if f.code in HIST_FLIPPERS and due <= date(2025, 6, 30):
                            qs = HIST_FLIPPERS[f.code]
                        quick = u < qs
                        near = (not quick) and u < qs + NEAR_SHARE[s]
                        wave = (f.code in WAVE_FUNDS and date(2025, 1, 1) <= due <= date(2025, 12, 15) and rng.rand() < 0.9)
                        if wave:
                            exit_d = date(2026, 1, 5) + timedelta(days=int(rng.randint(0, 262)))
                            hold_days = (exit_d - due).days
                            if hold_days > 505:
                                hold_days = int(rng.randint(400, 505))
                            if hold_days < 200:
                                hold_days = int(rng.randint(200, 260))
                            if (due + timedelta(days=hold_days)) > date(2026, 9, 25):
                                wave = False
                                quick = False
                        elif quick:
                            hold_days = int(rng.randint(215, 505))
                        elif near:
                            hold_days = int(rng.randint(590, 720))
                        else:
                            months = float(np.clip(rng.normal(mean, sd), lo_m, hi_m))
                            hold_days = int(months * 30.44 + rng.randint(0, 28))
                            if hold_days <= HOLD_GAP[1]:
                                hold_days = HOLD_GAP[1] + 20 + int(rng.randint(0, 120))
                        if f.code in IP_LIMB_CASES and add_months(f.ip_end, -10) <= due <= f.ip_end and not any(i.exit_date and i.exit_date > f.ip_end and i.hold_days < 540 for i in f.investments):
                            hold_days = (f.ip_end - due).days + int(rng.randint(25, 150))
                            if HOLD_GAP[0] <= hold_days <= HOLD_GAP[1]:
                                hold_days = HOLD_GAP[0] - 5
                        exit_try = due + timedelta(days=hold_days)
                        if abs((exit_try - f.ip_end).days) <= 25:
                            hold_days += 45
                            exit_try = due + timedelta(days=hold_days)
                        if exit_try.month == 12 and exit_try.day >= 16:
                            hold_days += 24                      # no realisation straddles a year-end between sale, notice and payment
                            exit_try = due + timedelta(days=hold_days)
                        if HOLD_GAP[0] <= hold_days <= HOLD_GAP[1]:
                            hold_days = HOLD_GAP[1] + 20
                        iv.hold_days = hold_days
                        iv.exit_date = due + timedelta(days=hold_days)
                        mmean, msd = MULT[s]
                        if rng.rand() < LOSS_SHARE[s]:
                            iv.multiple = float(rng.uniform(0.3, 0.93)) if s != "PC" else float(rng.uniform(0.55, 0.93))
                        else:
                            iv.multiple = float(max(1.0, rng.normal(mmean, msd))) if s != "PC" else float(rng.uniform(1.0, 1.06))
                        if quick or wave:
                            iv.multiple = float(rng.uniform(1.0, 1.12)) if s == "PC" else float(rng.uniform(1.15, 2.4))
                        f.investments.append(iv)
                        pending_exits.append(iv)
                    lines.append(("INVESTMENT", iv.ref, f"Investment in {iv.company}" + (" (follow-on)" if follow else ""), part))
            if amt > 0:
                f.cum_calls += amt
            # fees quarterly
            if mo in (1, 4, 7, 10) and f.unfunded_true > 0:
                fee = f.commitment * (FEE_Q[s] if in_ip else FEE_Q_POST[s])
                fee = round(min(fee, f.unfunded_true, max(0.0, call_cap - f.cum_calls)), 2)
                if fee > 0:
                    lines.append(("MANAGEMENT_FEE", "", f"Management fee Q{(mo - 1) // 3 + 1} {y}", fee))
                    f.cum_calls += fee
                if rng.rand() < 0.35:
                    ex = round(f.commitment * rng.uniform(0.0002, 0.0007), 2)
                    ex = min(ex, f.unfunded_true, max(0.0, call_cap - f.cum_calls))
                    if ex > 0:
                        lines.append(("PARTNERSHIP_EXPENSES", "", "Partnership expenses", ex))
                        f.cum_calls += ex
            if lines:
                nd = bday(date(y, mo, int(rng.randint(2, 24)))) if amt == 0 else notice_date
                due_d = bday(nd + timedelta(days=int(rng.randint(9, 15)))) if amt == 0 else due
                if due_d.month != nd.month and nd.month == 12:
                    due_d = bday_back(date(y, 12, 30))
                cn += 1
                f.notices.append(dict(notice_id=f"{f.code}-CN-{cn:03d}", type="CAPITAL_CALL", notice_date=nd,
                                      value_date=due_d, lines=lines, status="ISSUED"))
            # ---------------- exits this month
            dlines = []
            exits = [iv for iv in pending_exits if iv.exit_date is not None and iv.exit_date.year == y and iv.exit_date.month == mo]
            for iv in exits:
                pending_exits.remove(iv)
                iv.status = "REALISED"
                proceeds = iv.cost * iv.multiple
                roc = min(iv.cost, proceeds)
                gain = max(0.0, proceeds - iv.cost)
                roc = round(roc, 2)
                gain = round(gain, 2)
                iv.realised_roc, iv.realised_gain = roc, gain
                dlines.append(("RETURN_OF_CAPITAL", iv.ref, f"Realisation of {iv.company}: return of capital", roc))
                if gain > 0:
                    dlines.append(("REALISED_GAIN", iv.ref, f"Realisation of {iv.company}: realised gain", gain))
                hold_ok = iv.exit_date <= add_months(iv.initial_date, RECYCLE_MONTHS)
                if hold_ok and iv.exit_date <= f.ip_end and roc > 0:
                    iv.recallable = roc
                    f.recallable += roc
                f.cum_dist += roc + gain
            # income quarterly on held cost
            if mo in (3, 6, 9, 12) and INCOME_Q[s] > 0:
                for iv in f.investments:
                    if iv.status == "HELD" and iv.initial_date <= date(y, mo, 1):
                        inc = round(iv.cost * INCOME_Q[s] * rng.uniform(0.85, 1.15), 2)
                        if inc > 0:
                            dlines.append(("INCOME", iv.ref, f"Income distribution Q{(mo - 1) // 3 + 1} {y}: {iv.company}", inc))
                            f.cum_dist += inc
            elif INCOME_Q[s] == 0 and rng.rand() < 0.025 and any(iv.status == "HELD" for iv in f.investments):
                held = [iv for iv in f.investments if iv.status == "HELD"]
                iv = held[int(rng.randint(len(held)))]
                inc = round(iv.cost * rng.uniform(0.04, 0.12), 2)
                dlines.append(("INCOME", iv.ref, f"Dividend recapitalisation: {iv.company}", inc))
                f.cum_dist += inc
            if dlines:
                if exits:
                    nd = bday(exits[0].exit_date + timedelta(days=int(rng.randint(3, 12))))
                else:
                    nd = bday(date(y, mo, int(rng.randint(3, 26))))
                vd = bday(nd + timedelta(days=int(rng.randint(5, 10))))
                if vd.month != nd.month and nd.month == 12:
                    vd = bday_back(date(y, 12, 30))
                dn += 1
                f.notices.append(dict(notice_id=f"{f.code}-DN-{dn:03d}", type="DISTRIBUTION", notice_date=nd,
                                      value_date=vd, lines=dlines, status="ISSUED"))
            # ---------------- quarterly NAV
            if mo in (3, 6, 9, 12):
                qe = month_end(m)
                nav = 0.0
                for iv in f.investments:
                    if iv.status == "HELD" and iv.initial_date <= qe:
                        elapsed = (qe - iv.initial_date).days
                        prog = min(1.0, elapsed / max(iv.hold_days, 1))
                        mult = 1.0 + (iv.multiple - 1.0) * prog ** 1.3
                        nav += iv.cost * mult
                f.nav_q[(y, (mo - 1) // 3 + 1)] = round(nav, 2)
        assert f.cum_calls <= f.commitment + 1e-6, f.fund_id
    mark_in_kind(funds)
    return funds, fx


def mark_in_kind(funds):
    """Three growth exits settled in listed shares: the ROC and gain lines become one IN_KIND line.
    All three are long-held (never recallable) and none sits inside the two NAV-bridge windows."""
    wanted = [(date(2023, 2, 1), date(2024, 5, 31)), (date(2024, 8, 1), date(2025, 5, 31)), (date(2026, 7, 1), date(2026, 9, 20))]
    for lo, hi in wanted:
        done = False
        for f in funds:
            if f.strategy != "GR" or done:
                continue
            for n in f.notices:
                if n["type"] != "DISTRIBUTION" or not (lo <= n["notice_date"] <= hi):
                    continue
                refs = [l[1] for l in n["lines"] if l[0] == "RETURN_OF_CAPITAL"]
                for ref in refs:
                    iv = next(i for i in f.investments if i.ref == ref)
                    if iv.hold_days > 640 and iv.realised_gain > 0:
                        total = round(iv.realised_roc + iv.realised_gain, 2)
                        n["lines"] = [l for l in n["lines"] if l[1] != ref] + [("IN_KIND", ref, f"Distribution in specie: listed shares of {iv.company}", total)]
                        iv.status = "REALISED_IN_KIND"
                        done = True
                        break
                if done:
                    break
