"""task167 world: the Brandvold Foundation (Saint Paul, Minnesota) and its private-markets programme.

The clean truth lives here: every manager, fund and vehicle, each fund's financing class (whether it bridges its
first year of deals on a subscription line), its deal stream and its schedule. records.py turns it into cash flows,
pack.py into the files the investment office holds. Nothing in here ships."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

SEED = 167                      # the task number, fixed before any outcome was seen
AS_OF = dt.date(2026, 12, 31)   # the administrator's year-end file runs to this date
BOARD_MEETING = dt.date(2027, 1, 21)
ADMIN_FILE_DATE = dt.date(2027, 1, 13)      # the current administrator's year-end extract
LEGACY_CUTOFF = dt.date(2016, 6, 30)        # the legacy administrator's last day of record
HANDOVER_START = dt.date(2016, 4, 1)        # the current administrator re-keyed the second quarter of 2016
FORECAST_YEAR = 2027
ORG = "Brandvold Foundation"

STRATS = ("Buyout", "Growth equity", "Venture capital", "Private credit")
STRAT_P = (0.45, 0.20, 0.20, 0.15)
# speed of the deal clock by strategy (1.0 = buyout); venture invests over a longer period, credit faster
SPEED = {"Buyout": 1.0, "Growth equity": 0.95, "Venture capital": 0.85, "Private credit": 1.15}
# investment period in years, management fee during it (per cent of commitment a year) and after it
IP_YEARS = {"Buyout": 5, "Growth equity": 5, "Venture capital": 6, "Private credit": 4}
FEE_IP = {"Buyout": 0.0175, "Growth equity": 0.0175, "Venture capital": 0.0200, "Private credit": 0.0125}
FEE_POST_SHARE = 0.55            # the post-period fee as a share of the period fee (on a stepped-down basis)
EXP_RATE = 0.0012                # partnership expenses a year, called half-yearly
ORG_RATE = 0.0035                # organisational expenses, called with the first notice
# deal volume by year of age, share of commitment, for every fund whatever its financing (the seed deal inside year 1)
DEAL_YEARS = (0.32, 0.15, 0.13, 0.10, 0.06, 0.03, 0.02, 0.01)
SEED_DEAL = 0.10                 # the warehoused deal(s) a fund takes over at its first close
DEALS_PER_YEAR = 24.0           # capital-call events for portfolio investments a year, add-ons included
DEAL_CV = 0.35
PACE_SD = 0.05                   # a fund's own pace, persistent through its life
CALL_CAP = 0.97                  # no fund calls more than this share of its commitment
LINE_YEAR1_DELAY = 12            # months a line-bridged fund carries a first-year deal before calling it
LINE_LATER_DELAY = 3             # months it carries later deals
# a line-bridged fund still calls equity for part of its first deal in its first months (share of commitment)
LINE_FIRST_CALL = (0.035, 0.050)
# some ordinary funds start slowly: no warehoused deal and a thin first year of deals (investment calls in the first
# twelve months as a share of commitment); the deals they did not make in year one are not made up
SLOW_P = 0.10
SLOW_Y1 = (0.085, 0.160)
SLOW_CATCHUP = 0.0               # share of the year-one shortfall made up in year two

# the share of funds by vintage that bridge their first-year deals on a subscription line
P_LINE_EARLY = 0.05              # vintages 2006 to 2013
P_LINE_LATE = 0.27               # vintages 2014 to 2022
FUNDS_EARLY = 8                  # commitments a vintage year, 2006 to 2013
FUNDS_LATE = 12                  # 2014 to 2022
PROG_N = 14
PROG_LINE = 12                   # the 2026 programme's funds that bridge their first year
PROG_TOTAL_USD = 1150.0          # $ million committed in the 2026 programme (euro funds at the approval rate)

EUR_SHARE = {"Buyout": 0.22, "Growth equity": 0.15, "Venture capital": 0.0, "Private credit": 0.25}
PARALLEL_N = 8                   # funds held through a main vehicle and a parallel vehicle
PARALLEL_SPLIT = 0.70            # the main vehicle's share

PREFIX = ("Ald", "Bran", "Cor", "Dal", "Esk", "Fal", "Gar", "Hal", "Ing", "Kel", "Lor", "Mar", "Nor", "Ost",
          "Pel", "Quin", "Ros", "Sel", "Tor", "Ulv", "Var", "Wex", "Hol", "Ash", "Sten", "Bel", "Tal", "Rav")
SUFFIX = ("mere", "brook", "wick", "holt", "stead", "ford", "dale", "moor", "crest", "haven", "ridge", "field",
          "gate", "bury", "worth", "ley")
FIRM_WORD = {"Buyout": ("Capital Partners", "Equity Partners", "Capital"),
             "Growth equity": ("Growth Partners", "Growth Equity", "Partners"),
             "Venture capital": ("Ventures", "Venture Partners"),
             "Private credit": ("Credit Partners", "Capital Credit", "Lending Partners")}
FUND_WORD = {"Buyout": ("Fund", "Partners", "Capital Partners"), "Growth equity": ("Growth Fund", "Fund"),
             "Venture capital": ("Fund", "Ventures Fund"), "Private credit": ("Credit Fund", "Direct Lending Fund",
                                                                                "Senior Loan Fund")}
# drawn roots too close to a real firm or brand, renamed after the draw (the draw itself is unchanged)
RENAME = {"Halley": "Halwyn", "Holley": "Holvane", "Norbrook": "Norholt", "Stenford": "Stenholt"}
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")


def month_index(d):
    return (d.year - 2006) * 12 + (d.month - 1)


def month_start(m):
    return dt.date(2006 + m // 12, m % 12 + 1, 1)


def add_months(d, k):
    m = d.month - 1 + k
    y = d.year + m // 12
    m = m % 12 + 1
    last = [31, 29 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return dt.date(y, m, min(d.day, last))


class Fund:
    """One fund the Foundation committed to (its vehicles share one deal stream and one financing class)."""

    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.vehicles = []

    def __repr__(self):
        return "Fund(%s %s %s %s)" % (self.name, self.vintage, self.strategy, self.cls)


class Vehicle:
    def __init__(self, fund, code, name, commitment, share, parallel):
        self.fund, self.code, self.name, self.commitment, self.share, self.parallel = \
            fund, code, name, commitment, share, parallel


def _manager_names(rng, n):
    seen, out = set(), []
    while len(out) < n:
        a, b = PREFIX[int(rng.integers(len(PREFIX)))], SUFFIX[int(rng.integers(len(SUFFIX)))]
        root = a + b
        if root in seen or root.lower().endswith(("dalemoor",)):
            continue
        seen.add(root)
        out.append(root)
    return out


def build_world():
    rng = np.random.default_rng([SEED, 1])
    # managers: a strategy each, a fund numbering, a currency
    roots = [RENAME.get(r, r) for r in _manager_names(rng, 64)]
    managers = []
    for i, root in enumerate(roots):
        s = STRATS[int(rng.choice(4, p=STRAT_P))]
        ccy = "EUR" if rng.random() < EUR_SHARE[s] else "USD"
        managers.append(dict(root=root, strategy=s, ccy=ccy, firm=root + " " + FIRM_WORD[s][int(rng.integers(len(FIRM_WORD[s])))],
                             fund_word=FUND_WORD[s][int(rng.integers(len(FUND_WORD[s])))],
                             next_no=int(rng.integers(1, 5)), last_vintage=None, line_user=False, used=False))
    funds = []

    def take_manager(vy, strategy=None):
        # a re-up when one of the Foundation's managers is back in market (three or more years since its last fund)
        ok = (lambda m: strategy is None or m["strategy"] == strategy)
        cands = [m for m in managers if m["used"] and m["last_vintage"] is not None and vy - m["last_vintage"] >= 3
                 and ok(m)]
        if cands and rng.random() < 0.62:
            m = cands[int(rng.integers(len(cands)))]
        else:
            fresh = [m for m in managers if not m["used"] and ok(m)]
            if not fresh:
                pool = [m for m in managers if ok(m) and (m["last_vintage"] is None or vy - m["last_vintage"] >= 3)]
                m = min(pool, key=lambda x: (x["last_vintage"] or 0))
            else:
                m = fresh[int(rng.integers(len(fresh)))]
        m["used"] = True
        m["last_vintage"] = vy
        return m

    def make_fund(m, vy, first_close, commitment, cls, programme):
        no = m["next_no"]
        m["next_no"] += 1
        m["last_vintage"] = vy
        name = "%s %s %s" % (m["root"], m["fund_word"], ROMAN[no - 1])
        f = Fund(id=len(funds), manager=m["firm"], root=m["root"], name=name, number=no, strategy=m["strategy"],
                 ccy=m["ccy"], vintage=vy, first_close=first_close, commitment=commitment, cls=cls,
                 programme=programme, pace=float(math.exp(rng.normal(0.0, PACE_SD))))
        funds.append(f)
        return f

    for vy in range(2006, 2023):
        n = FUNDS_EARLY if vy < 2014 else FUNDS_LATE
        p_line = P_LINE_EARLY if vy < 2014 else P_LINE_LATE
        for _ in range(n):
            m = take_manager(vy)
            # commitments grew with the endowment: about $15 to 30 million in 2006, $25 to 50 million by 2022
            lo = 14.0 + (vy - 2006) * 0.7
            size = float(rng.uniform(lo, lo * 1.9))
            if m["ccy"] == "EUR":
                size = size / 1.15
            size = round(size * 4) / 4.0
            fc = dt.date(vy, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            cls = "line" if rng.random() < p_line else "steady"
            make_fund(m, vy, fc, size, cls, False)
    # the 2026 programme: fourteen funds holding first closes between mid-January and the end of March 2026
    prog_cls = ["line"] * PROG_LINE + ["steady"] * (PROG_N - PROG_LINE)
    rng.shuffle(prog_cls)
    raw = rng.uniform(55, 95, PROG_N)
    prog = []
    prog_strats = ["Buyout"] * 6 + ["Growth equity"] * 3 + ["Venture capital"] * 3 + ["Private credit"] * 2
    for k in range(PROG_N):
        m = take_manager(2026, prog_strats[k])
        d0 = dt.date(2026, 1, 12) + dt.timedelta(days=int(rng.integers(0, 78)))
        prog.append((m, d0, float(raw[k]), prog_cls[k]))
    # scale so the programme totals $1,000 million with euro commitments at the approval rate
    eur_rate = 1.08
    usd = [(r * (1.0 if m["ccy"] == "USD" else 1.0)) for m, d0, r, c in prog]
    scale = PROG_TOTAL_USD / sum(usd)
    for (m, d0, r, c) in prog:
        amt = r * scale
        if m["ccy"] == "EUR":
            amt = amt / eur_rate
        amt = round(amt * 2) / 2.0
        make_fund(m, 2026, d0, amt, c, True)
    # the first-year draw traits, on their own stream so the world above is unchanged by them
    rng_t = np.random.default_rng([SEED, 31])
    for f in funds:
        u = rng_t.random(3)
        f.slow = f.cls == "steady" and u[0] < SLOW_P
        f.first_call = LINE_FIRST_CALL[0] + (LINE_FIRST_CALL[1] - LINE_FIRST_CALL[0]) * u[1] if f.cls == "line" else 0.0
        f.slow_y1 = SLOW_Y1[0] + (SLOW_Y1[1] - SLOW_Y1[0]) * u[2] if f.slow else None
    # vehicles: most funds one, a few a main and a parallel vehicle
    # parallel vehicles, chosen by rule: per strategy one fund from each of two vintage bands, the latest-vintage and
    # then largest commitment in the band (a euro fund where the band has one, for buyout and credit)
    par_ids = set()
    rules = {"Buyout": ((2019, 2022, True), (2015, 2018, False)), "Growth equity": ((2015, 2018, False), (2019, 2022, False)),
             "Venture capital": ((2011, 2014, False), (2019, 2022, False)), "Private credit": ((2019, 2022, True), (2015, 2018, False))}
    for s, picks in rules.items():
        for lo, hi, want_eur in picks:
            pool = [f for f in funds if not f.programme and f.strategy == s and lo <= f.vintage <= hi and f.id not in par_ids]
            if want_eur and any(f.ccy == "EUR" for f in pool):
                pool = [f for f in pool if f.ccy == "EUR"]
            pool.sort(key=lambda f: (-f.vintage, -f.commitment, f.name))
            if pool:
                par_ids.add(pool[0].id)
    code_no = 4100
    for f in funds:
        stem = "".join(w[0] for w in f.root.split()) if " " in f.root else f.root[:3].upper()
        if f.id in par_ids:
            c_main = round(f.commitment * PARALLEL_SPLIT * 4) / 4.0
            c_par = round((f.commitment - c_main) * 4) / 4.0
            f.commitment = c_main + c_par
            f.vehicles.append(Vehicle(f, "%s%02d-%d" % (stem, f.number, code_no), f.name + ", L.P.", c_main,
                                      c_main / f.commitment, False))
            code_no += 7
            f.vehicles.append(Vehicle(f, "%s%02d-%d" % (stem, f.number, code_no), f.name + " Parallel, L.P.", c_par,
                                      c_par / f.commitment, True))
            code_no += 7
        else:
            f.vehicles.append(Vehicle(f, "%s%02d-%d" % (stem, f.number, code_no), f.name + ", L.P.", f.commitment, 1.0,
                                      False))
            code_no += 7
    return funds


def deal_rate(age_m, strategy):
    """expected deal volume in month of age `age_m`, share of commitment, outside the seed deal"""
    k = SPEED[strategy]
    y = int(age_m * k / 12.0)
    if y >= len(DEAL_YEARS):
        return 0.0
    v = DEAL_YEARS[y] - (SEED_DEAL if y == 0 else 0.0)
    return v / 12.0 * k


def fee_rate_month(age_m, strategy):
    ip = IP_YEARS[strategy] * 12
    if age_m < ip:
        return FEE_IP[strategy] / 12.0
    if age_m < 120:
        return FEE_IP[strategy] * FEE_POST_SHARE / 12.0
    if age_m < 144:
        return FEE_IP[strategy] * FEE_POST_SHARE * 0.5 / 12.0
    return 0.0


if __name__ == "__main__":
    fs = build_world()
    print(len(fs), "funds;", sum(len(f.vehicles) for f in fs), "vehicles")
    for v in range(2006, 2027):
        sub = [f for f in fs if f.vintage == v]
        if sub:
            print(v, len(sub), "line", sum(1 for f in sub if f.cls == "line"), "commit %.0f" % sum(f.commitment for f in sub),
                  "eur", sum(1 for f in sub if f.ccy == "EUR"))
    for f in fs:
        if f.programme:
            print(" ", f.name, f.strategy, f.ccy, f.commitment, f.first_close, f.cls, [v.code for v in f.vehicles])
    print("managers used", len(set(f.manager for f in fs)))
