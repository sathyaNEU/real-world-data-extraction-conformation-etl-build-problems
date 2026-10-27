"""task271 constants and helpers shared by every generator module.

Fenmarsh Investment Management runs a central dealing desk in London that works its funds' UK equity orders through
two brokers' algorithms (Ashlowe Securities and Pemberwick & Co) on eight execution venues. Its wealth arm, Fenmarsh
Wealth Limited, runs a platform for retail clients whose dealing in UK shares Gresmere Stockbrokers has executed; from
Monday 4 January 2027 the central desk deals for the platform. The platform nets its clients' orders at three dealing
points a day and sends one order per stock, whole, to one venue on its venue list. The order execution policy keeps a
venue off a client flow's list when the fills that flow's orders would receive there meet an average adverse move
above 1.5 basis points in the 60 seconds after the fill. The wealth board approves the list on 9 December 2026.

The seed was fixed by rule before any data was generated: the task number, then the pull's month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 2711102

FIRM = "Fenmarsh Investment Management"
WEALTH = "Fenmarsh Wealth"
WEALTH_LTD = "Fenmarsh Wealth Limited"
TCA = "Hessenby Analytics"
BROKER_A = "Ashlowe Securities"
BROKER_B = "Pemberwick & Co"
GRESMERE = "Gresmere Stockbrokers"

PEOPLE = {
    "dealing": "Owen Porter",        # head of dealing: the requester, signs the router configuration and the venue list paper
    "research": "Declan Davies",     # head of execution research: the review's analysis
    "coo": "Oliver Hamilton",        # Fenmarsh Wealth's chief operating officer: the dealing plan
}

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
DATA_START = dt.date(2026, 1, 2)
DATA_END = dt.date(2026, 10, 30)
PULL = dt.date(2026, 11, 2)              # the cost provider's export and the brokers' files were pulled
PAPER_DATE = dt.date(2026, 11, 20)
BOARD_DATE = dt.date(2026, 12, 9)
CUTOVER = dt.date(2027, 1, 4)
POLICY_DATE = dt.date(2025, 9, 15)
PLAN_DATE = dt.date(2026, 10, 12)
ROUTER_DATE = dt.date(2026, 1, 5)
THURSGATE_SWITCH = dt.date(2026, 6, 1)   # Thursgate's midpoint book moved to a new segment code
GRESMERE_MIGRATION = dt.date(2026, 7, 1) # Gresmere's back office moved to a new contract note system
BANK_HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4),
                 dt.date(2026, 5, 25), dt.date(2026, 8, 31), dt.date(2026, 12, 25), dt.date(2026, 12, 28),
                 dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2027, 1, 1)}
BST_START = dt.datetime(2026, 3, 29, 1, 0, tzinfo=UTC)
BST_END = dt.datetime(2026, 10, 25, 1, 0, tzinfo=UTC)
OPEN_S = 8 * 3600                        # continuous trading 08:00 to 16:30 London time
CLOSE_S = 16 * 3600 + 30 * 60
UNCROSS_S = 16 * 3600 + 35 * 60          # the closing auction's uncrossing

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ------------------------------------------------------------------------------------------------- venues
# code: name, operator, kind, adverse move a lone fill meets at 60 seconds (bp), seconds over which it builds
VENUES = ["XWEX", "AWKL", "DLVL", "AWKM", "DLVM", "THGD", "BDSI", "QTSI"]
VENUE = {
    "XWEX": dict(name="Wexcombe Stock Exchange", short="Wexcombe", operator="Wexcombe Stock Exchange plc",
                 kind="lit order book", alpha=0.10, tau=4.0),
    "AWKL": dict(name="Ardenwick MTF lit book", short="Ardenwick lit", operator="Ardenwick Markets Ltd",
                 kind="lit order book", alpha=0.90, tau=4.0),
    "DLVL": dict(name="Delvenne MTF lit book", short="Delvenne lit", operator="Delvenne Exchange Ltd",
                 kind="lit order book", alpha=2.20, tau=3.0),
    "AWKM": dict(name="Ardenwick MTF midpoint book", short="Ardenwick mid", operator="Ardenwick Markets Ltd",
                 kind="midpoint book", alpha=3.00, tau=35.0),
    "DLVM": dict(name="Delvenne Midpoint", short="Delvenne Midpoint", operator="Delvenne Exchange Ltd",
                 kind="midpoint book", alpha=1.00, tau=30.0),
    "THGD": dict(name="Thursgate MTF midpoint book", short="Thursgate mid", operator="Thursgate Trading Ltd",
                 kind="midpoint book", alpha=2.00, tau=40.0),
    "BDSI": dict(name="Brindock Securities SI", short="Brindock SI", operator="Brindock Securities Ltd",
                 kind="systematic internaliser", alpha=0.10, tau=9.0),
    "QTSI": dict(name="Quintrell Markets SI", short="Quintrell SI", operator="Quintrell Markets Ltd",
                 kind="systematic internaliser", alpha=2.20, tau=8.0),
}
THURSGATE_NEW = "THGM"
LINE = 1.5                              # the policy's line, basis points
HORIZON = 60                            # seconds
DARK = ["AWKM", "DLVM", "THGD"]
LIT = ["XWEX", "AWKL", "DLVL"]
SI = ["BDSI", "QTSI"]

# broker B's own names for the venues in its execution reports
PEMBERWICK_VENUE = {"XWEX": "WEXCOMBE", "AWKL": "ARDENWICK LIT", "DLVL": "DELVENNE LIT", "AWKM": "ARDENWICK MID",
                    "DLVM": "DELVENNE MID", "THGD": "THURSGATE MID", "BDSI": "BRINDOCK SI", "QTSI": "QUINTRELL SI"}

# ------------------------------------------------------------------------------------------------- algorithms
ALGOS = ["ASL-ARR", "ASL-VOL", "ASL-CLS", "PEM-SF", "PEM-VW", "PEM-IN"]
ALGO = {
    "ASL-ARR": dict(broker="ASHL", name="Ashlowe Arrival", style="IS", share=0.22),
    "ASL-VOL": dict(broker="ASHL", name="Ashlowe Volume", style="VWAP", share=0.16),
    "ASL-CLS": dict(broker="ASHL", name="Ashlowe Close", style="CLOSE", share=0.08),
    "PEM-SF": dict(broker="PEMB", name="Pemberwick Shortfall", style="IS", share=0.24),
    "PEM-VW": dict(broker="PEMB", name="Pemberwick VWAP", style="VWAP", share=0.18),
    "PEM-IN": dict(broker="PEMB", name="Pemberwick Inline", style="POV", share=0.12),
}
# routing tables: the share of child orders each style sends to each venue in each phase
ROUTE = {
    "burst": dict(XWEX=.04, AWKL=.03, DLVL=.03, AWKM=.31, DLVM=.24, THGD=.29, BDSI=.03, QTSI=.03),
    "work":  dict(XWEX=.20, AWKL=.16, DLVL=.15, AWKM=.06, DLVM=.07, THGD=.06, BDSI=.14, QTSI=.16),
    "vwap":  dict(XWEX=.20, AWKL=.15, DLVL=.14, AWKM=.07, DLVM=.08, THGD=.07, BDSI=.13, QTSI=.16),
    "single": dict(XWEX=.30, AWKL=.25, DLVL=.20, AWKM=0., DLVM=0., THGD=0., BDSI=.12, QTSI=.13),
}
LAMBDA = 14.0                           # permanent impact of the desk's own trades, bp per 1 per cent of ADV


# ------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12):
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=16).hexdigest()[:n]


def trading_days(a=DATA_START, b=DATA_END):
    out, d = [], a
    while d <= b:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def next_business_day(d):
    d += dt.timedelta(days=1)
    while d.weekday() >= 5 or d in BANK_HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def london_offset(t_utc):
    """Hours London is ahead of UTC at a UTC instant."""
    return 1 if BST_START <= t_utc < BST_END else 0


def utc_of(day, sec_london):
    """The UTC instant of a London wall-clock second of the day."""
    naive = dt.datetime(day.year, day.month, day.day) + dt.timedelta(seconds=float(sec_london))
    probe = naive.replace(tzinfo=UTC)
    off = london_offset(probe - dt.timedelta(hours=1))
    return probe - dt.timedelta(hours=off)


def iso_ms(t):
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def uk_date(d):
    return "%d %s %d" % (d.day, MONTH_NAMES[d.month], d.year)
