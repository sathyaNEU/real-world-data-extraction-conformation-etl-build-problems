"""Kilbourne Payroll's own records, January 2022 to December 2025: every payroll account opened, the wages each account
ran each quarter, each account's state tax registrations, the payroll tax team's register of successor employers, and
the June 2024 move from the legacy client system to the current account system.

A business is one employer. It runs payroll on an account, and an account carries one EIN. Four things make an
account differ from a business in these files, each the way a payroll platform's systems write them:
- a business that changes legal entity (a sole proprietorship that incorporates, a partnership that becomes an LLC)
  takes a new EIN, so Kilbourne closes its account and opens a new one under the new EIN; the payroll tax team records
  the predecessor and the successor in its successor-employer register, because the state unemployment wage base and
  experience carry over;
- a business that cancels and comes back is given a new account under its old EIN;
- the account file keeps a business's current address; the state tax registrations keep each state the account
  withheld for, with the liability date the state holds;
- until 18 November 2024 the onboarding form asked whether this was the client's first payroll, which a new entity of
  an existing employer, and a business that had run its own payroll, often answered yes; from that Monday it asks
  whether the business has paid employees before, under any EIN, by itself or through a provider.
Accounts opened before the migration carry legacy client numbers; the legacy system's quarterly wages run to the last
legacy pay date (Friday 14 June 2024), in cents, one row per pay group with the client's company-level group 00 holding
the client's totals; the current system's start with the first pay date after the move (Monday 17 June 2024)."""
from __future__ import annotations

import calendar
import datetime as dt
from dataclasses import dataclass, field

import numpy as np

import common as K
import names as NM
import world as WD

MIGRATION = dt.date(2024, 6, 17)          # Monday: first pay date on the current account system
LEGACY_LAST_PAY = dt.date(2024, 6, 14)    # Friday: last pay date the legacy system ran
MIGRATED_AT = dt.datetime(2024, 6, 15, 7, 40)   # Eastern: the migration load (Saturday morning)
EXTRACT_PULLED = dt.datetime(2026, 1, 9, 14, 20)   # Eastern: the year-end planning extract
SHARE_TARGET = dict(OH=0.0460, PA=0.0290, MI=0.0310, IN=0.0140, MN=0.0070, WI=0.0090, KY=0.0160, WV=0.0120,
                    TN=0.0050, MO=0.0050, IA=0.0080, VA=0.0040)
SWITCHER_RATIO = 2.6      # businesses moving their payroll to Kilbourne from another provider, per first-time employer
INHOUSE_RATIO = 0.34      # businesses that ran their own payroll moving it to Kilbourne, per first-time employer
EXT_SUCCESSOR = 0.05      # new entities continuing a payroll run elsewhere, per first-time employer
QUESTION_CHANGE = dt.date(2024, 11, 18)   # Monday: the onboarding question asks about the business, under any EIN
SUCC_FLAGGED = 0.62       # successor accounts answering the older question yes
INHOUSE_FLAGGED = 0.62    # self-run businesses answering the older question yes
MOVE_AFTER = 365          # days on payroll before a business relocates
SUCCESSOR_RATE = 0.036    # entity changes per employer-year
MOVE_RATE = 0.024         # businesses relocating to another state per employer-year
CANCEL_RATE = 0.105       # cancellations per employer-year (leaving Kilbourne or closing)
RETURN_RATE = 0.14        # cancelled businesses that come back within the window
SEASONAL_SHARE = 0.05     # employers with no payroll in the fourth quarter (seasonal trades)
TWO_GROUPS = 0.42         # legacy clients of two or more people paying an officer or salaried group apart from hourly staff
DOWNGRADE_Q = 0.012       # accounts a quarter moving to tax filing only (the client runs its own payroll, we file)
UPGRADE_Q = 0.018         # accounts a quarter adding the HR bundle
PRODUCT_FROM = dt.date(2024, 7, 1)       # product changes take effect at a quarter's start, on the current system
END = dt.date(2025, 12, 31)
NO_PAY = (dt.date(2024, 6, 15), dt.date(2024, 6, 16))   # the migration weekend

# lag from an application to the first payroll, months 0 to 11, among formations within four quarters
LAG4 = np.array([0.205, 0.168, 0.139, 0.112, 0.090, 0.073, 0.060, 0.050, 0.039, 0.029, 0.020, 0.015])
LAG4 = LAG4 / LAG4.sum()

NEIGHBOURS = {"OH": ["KY", "IN", "PA", "MI", "WV"], "PA": ["OH", "WV", "VA"], "MI": ["OH", "IN", "WI"],
              "IN": ["OH", "KY", "MI"], "MN": ["WI", "IA"], "WI": ["MN", "MI", "IA"], "KY": ["OH", "IN", "TN", "WV"],
              "WV": ["OH", "PA", "VA", "KY"], "TN": ["KY", "VA", "MO"], "MO": ["IA", "TN", "KY"], "IA": ["MN", "MO", "WI"],
              "VA": ["WV", "TN", "PA"]}
OUT_OF_FOOTPRINT = ["FL", "TX", "AZ", "NC", "SC", "GA", "IL", "NY", "NJ", "MD", "KS", "CO"]

# the legacy client system's referral source codes; the migration mapped the current ones to the current channel list
# and loaded the two older codes (CPA from the 2022 referral form, BP from the bank branch programme) as the current
# system's default channel
LEGACY_CODES = {"accountant referral": (("ACCT", 0.66), ("CPA", 0.34)), "bank partner": (("BANK", 0.62), ("BP", 0.38)),
                "web sign-up": (("WEB", 1.0),), "outbound": (("OUT", 0.60), ("TEL", 0.40)),
                "partner marketplace": (("MKT", 0.60), ("APX", 0.40))}
CODE_TO_CHANNEL = {"ACCT": "accountant referral", "BANK": "bank partner", "WEB": "web sign-up", "OUT": "outbound",
                   "MKT": "partner marketplace", "CPA": "web sign-up", "BP": "web sign-up", "TEL": "web sign-up",
                   "APX": "web sign-up"}
# a business that ran its own payroll usually comes to us through its accountant
INHOUSE_CHANNELS = (("accountant referral", 0.50), ("web sign-up", 0.33), ("bank partner", 0.07), ("outbound", 0.05),
                    ("partner marketplace", 0.05))


@dataclass
class Spell:
    k: int
    legacy: str | None
    ein: str
    opened: dt.datetime          # UTC
    start: dt.date               # first pay date on this account
    stop: dt.date | None         # last day on this account (None: still on payroll at the extract)
    flag_first: bool
    prev_provider: str
    channel: str
    state: str                   # state of the business on the first pay date of this account
    acct: str = ""
    legacy_code: str = ""        # legacy referral source code (accounts opened on the legacy system)
    product: str = "Payroll"
    product_since: dt.date | None = None

    @property
    def channel_shown(self):
        return CODE_TO_CHANNEL[self.legacy_code] if self.legacy_code else self.channel

    def paid_by_us(self, d):
        """False once the account has moved to tax filing only (the client pays its own employees)."""
        return not (self.product == "Tax filing only" and self.product_since is not None and d >= self.product_since)


@dataclass
class Business:
    bid: int
    kind: str                    # "first", "switch", "inhouse", "succ_ext", "successor"
    state0: str
    first_pay: dt.date
    name: str
    dba: str
    entity: str
    naics: str
    employees0: int
    wage_q: float                # gross wages a quarter per employee at the start
    growth: float                # yearly growth in headcount
    seasonal: bool
    key: str = ""                # stable identity for the business's random streams (state, month, kind, number)
    liable0: dt.date | None = None   # the date the business first paid wages in its first state
    groups: int = 1              # legacy pay groups
    split: float = 1.0           # share of wages in group 01 when there are two
    pred: int | None = None      # the Kilbourne business this one succeeds
    pred_ein: str = ""           # a predecessor outside Kilbourne's 2022-2025 book
    basis: str = ""              # how a successor came about (change of entity, reorganisation, acquisition)
    succ: int | None = None
    moves: list = field(default_factory=list)       # [(date, state)]
    spans: list = field(default_factory=list)       # [[start, stop]] payroll spans with Kilbourne, one per account
    spells: list = field(default_factory=list)      # [Spell]
    ein: str = ""

    def state_on(self, d):
        s = self.state0
        for when, st in self.moves:
            if when <= d:
                s = st
        return s


class Company:
    def __init__(self):
        self.business = {}
        self.successors = []        # (pred bid or None, succ bid, effective date, state)
        self.eins = set()           # every EIN in use (Kilbourne's clients and outside predecessors): never reissued
        self._next = 0

    def new_ein(self, r, b, old=False):
        e = NM.ein(r, b, old=old)
        while e in self.eins:
            e = NM.ein(r, b, old=old)
        self.eins.add(e)
        return e

    def new_bid(self):
        self._next += 1
        return self._next


def calendar_first_payrolls(W):
    """Expected first payrolls a month in each state's market: formations within four quarters, spread over the lag."""
    out = {}
    for s in WD.STATES:
        f = W.F4[s.usps].astype(float)
        c = np.zeros(K.NM + 12)
        for t in range(K.NM):
            c[t:t + 12] += f[t] * LAG4
        out[s.usps] = c[:K.NM]
    return out


def pay_day(r, y, m):
    """A pay date inside a month: payrolls fall on weekdays, more often on Fridays and on the 1st and 15th."""
    n = calendar.monthrange(y, m)[1]
    while True:
        d = int(r.integers(1, n + 1))
        day = dt.date(y, m, d)
        wd = day.weekday()
        if wd >= 5 or day in NO_PAY:
            continue
        w = 1.0 + (1.4 if wd == 4 else 0.0) + (1.2 if d in (1, 15) else 0.0)
        if r.random() < w / 3.6:
            return day


def build(W, scale=1.0):
    """Simulate the businesses, their lives and their accounts. `scale` multiplies every state's share; build.py fixes
    it by rule so the plan figure sits inside its bin (a calibration of the company's size, never a seed search)."""
    C = Company()
    market = calendar_first_payrolls(W)
    for s in WD.STATES:
        theta = SHARE_TARGET[s.usps] * scale
        for t in range(K.midx(2022, 1), K.midx(2025, 12) + 1):
            y, m = K.mfrom(t)
            lam = theta * market[s.usps][t]
            cells = (("first", lam), ("switch", lam * SWITCHER_RATIO * (1.18 if m == 1 else 1.0)),
                     ("inhouse", lam * INHOUSE_RATIO * (1.25 if m == 1 else 1.0)), ("succ_ext", lam * EXT_SUCCESSOR))
            for kind, mean in cells:
                # one uniform per state, month and kind, read through the Poisson quantile: a larger company adds
                # businesses at the margin and keeps every other business as it was
                n = poisson_quantile(float(K.rng("count", s.usps, t, kind).random()), mean)
                for j in range(n):
                    key = "%s-%d-%s-%d" % (s.usps, t, kind, j)
                    rs = K.rng("business", key)
                    info = NM.business(rs, s.usps, kind if kind in ("first", "inhouse") else "switch")
                    b = Business(C.new_bid(), kind, s.usps, pay_day(rs, y, m), info["name"], info["dba"],
                                 info["entity"], info["naics"], info["employees"], info["wage"], info["growth"],
                                 bool(rs.random() < SEASONAL_SHARE), key=key)
                    if kind == "first":
                        b.liable0 = b.first_pay
                    elif kind == "succ_ext":
                        b.liable0 = b.first_pay
                        # the predecessor ran its payroll elsewhere: its EIN is on the tax team's register only
                        b.pred_ein = C.new_ein(rs, b, old=True)
                        b.basis = "acquisition"
                        C.successors.append((None, b.bid, b.first_pay, s.usps))
                    else:
                        b.liable0 = b.first_pay - dt.timedelta(days=int(rs.integers(200, 365 * 16)))
                    _groups(rs, b)
                    C.business[b.bid] = b
    done, queue = set(), sorted(C.business)
    while queue:
        bid = queue.pop(0)
        if bid in done:
            continue
        before = set(C.business)
        _life(C, C.business[bid])
        done.add(bid)
        queue.extend(sorted(set(C.business) - before))
    for b in sorted(C.business.values(), key=lambda x: (x.first_pay, x.bid)):
        _accounts(C, b)
    _number(C)
    return C


def poisson_quantile(u, mean):
    """The smallest n with P(N <= n) >= u for N Poisson with the given mean."""
    import math
    p = math.exp(-mean)
    c, n = p, 0
    while c < u and n < 100000:
        n += 1
        p *= mean / n
        c += p
    return n


def _groups(r, b):
    if b.employees0 >= 2 and r.random() < TWO_GROUPS:
        b.groups, b.split = 2, float(0.52 + 0.33 * r.random())


def _next_workday(d):
    while d.weekday() >= 5 or d in NO_PAY:
        d += dt.timedelta(days=1)
    return d


def _life(C, b):
    """Moves, an entity change (a successor business continues the payroll), or a cancellation with a possible return.
    Successors live their own lives in turn (created here, processed when the caller reaches their bid)."""
    rb = K.rng("life", b.key)
    cur, state = b.first_pay, b.state0
    rates = (("move", MOVE_RATE), ("succ", SUCCESSOR_RATE), ("cancel", CANCEL_RATE))
    total = sum(v for _, v in rates)
    returned = False
    b.spans = [[b.first_pay, None]]
    while True:
        when = cur + dt.timedelta(days=max(25, int(rb.exponential(365.25 / total))))
        if when > END:
            break
        u = rb.random() * total
        if u < MOVE_RATE and (when - b.first_pay).days < MOVE_AFTER:
            cur = when
            continue
        if u < MOVE_RATE:
            cand = [x for x in NEIGHBOURS[state] if x != state] if state in NEIGHBOURS else list(WD.REFORM)
            if rb.random() < 0.28:
                cand = OUT_OF_FOOTPRINT
            state = cand[int(rb.integers(0, len(cand)))]
            b.moves.append((when, state))
            cur = when
        elif u < MOVE_RATE + SUCCESSOR_RATE:
            when = _next_workday(when)
            if when > END:
                break
            info = NM.successor_of(rb, b)
            years = (when - b.first_pay).days / 365.25
            s2 = Business(C.new_bid(), "successor", state, when, info["name"], info["dba"], info["entity"], b.naics,
                          max(1, int(round(b.employees0 * (1 + b.growth) ** years))),
                          b.wage_q * (1.03 ** years), b.growth, b.seasonal, key=b.key + "/s", liable0=when,
                          pred=b.bid)
            s2.groups, s2.split = b.groups, b.split
            s2.basis = info["basis"]
            b.succ = s2.bid
            b.spans[-1][1] = when - dt.timedelta(days=1)
            C.business[s2.bid] = s2
            C.successors.append((b.bid, s2.bid, when, state))
            break
        else:
            b.spans[-1][1] = when
            if not returned and rb.random() < RETURN_RATE:
                back = _next_workday(when + dt.timedelta(days=int(rb.integers(75, 320))))
                if back <= END:
                    b.spans.append([back, None])
                    returned = True
                    cur = back
                    continue
            break


def _accounts(C, b):
    ra = K.rng("acct", b.key)
    b.ein = C.new_ein(ra, b)
    for k, (start, stop) in enumerate(b.spans):
        lead = int(ra.integers(5, 38))
        local = dt.datetime.combine(start - dt.timedelta(days=lead), dt.time(0, 0)) + \
            dt.timedelta(minutes=int(ra.integers(8 * 60, 23 * 60 + 40)))
        opened = local + dt.timedelta(hours=_et_offset(local))          # UTC
        legacy = "pending" if local < MIGRATED_AT else None
        succ = b.kind in ("successor", "succ_ext")
        older_form = local.date() < QUESTION_CHANGE
        if k > 0:
            flag = False
        elif b.kind == "first":
            flag = True
        elif succ:
            flag = older_form and ra.random() < SUCC_FLAGGED
        elif b.kind == "inhouse":
            flag = older_form and ra.random() < INHOUSE_FLAGGED
        else:
            flag = False
        if flag:
            prov = ""
        elif k > 0:
            prov = "Kilbourne (prior account)"
        elif b.kind == "inhouse":
            prov = "self-run (desktop software)" if ra.random() < 0.55 else "self-run (manual checks)"
        elif succ:
            prov = "predecessor entity" if ra.random() < 0.7 else NM.provider(ra, b, 0)
        else:
            prov = NM.provider(ra, b, 0)
            while prov.startswith("self-run"):
                prov = NM.provider(ra, b, 0)
        ch = NM.channel(ra, b)
        if b.kind == "inhouse":
            u, acc = ra.random(), 0.0
            for name, w in INHOUSE_CHANNELS:
                acc += w
                if u < acc:
                    ch = name
                    break
        sp = Spell(k, legacy, b.ein, opened, start, stop, flag, prov, ch, b.state_on(start))
        if legacy:
            u, acc = ra.random(), 0.0
            for code, w in LEGACY_CODES[sp.channel]:
                acc += w
                if u < acc:
                    sp.legacy_code = code
                    break
            sp.legacy_code = sp.legacy_code or LEGACY_CODES[sp.channel][-1][0]
        _product(b, sp)
        b.spells.append(sp)


def _product(b, sp):
    """At most one product change per account, effective at the start of a quarter at least two quarters after the
    account's first pay date: the HR bundle added, or a move to tax filing only."""
    rp = K.rng("product", b.key, sp.k)
    stop = sp.stop
    first_ok = qbounds(*quarters(sp.start, sp.start)[0])[1] + dt.timedelta(days=1)
    first_ok = qbounds(*quarters(first_ok, first_ok)[0])[1] + dt.timedelta(days=1)
    for y in (2024, 2025, 2026):
        for m in (1, 4, 7, 10):
            q0 = dt.date(y, m, 1)
            if q0 < max(PRODUCT_FROM, first_ok) or q0 > dt.date(2026, 1, 1):
                continue
            if stop is not None and stop < q0:
                return
            u = rp.random()
            if u < DOWNGRADE_Q:
                sp.product, sp.product_since = "Tax filing only", q0
                return
            if u < DOWNGRADE_Q + UPGRADE_Q:
                sp.product, sp.product_since = "Payroll + HR", q0
                return


def _number(C):
    """Legacy client numbers in opening order (the legacy system numbered clients from 418000 in 2022); current-system
    account numbers KP plus seven digits: the migration load numbered every legacy client in client-number order, and
    accounts opened after the move take the next number."""
    spells = sorted(((sp.opened, b.bid, sp.k, sp) for b in C.business.values() for sp in b.spells),
                    key=lambda x: (x[0], x[1], x[2]))
    r = K.rng("numbers")
    no = 418000
    legacy = []
    for opened, bid, k, sp in spells:
        if sp.legacy is not None:
            no += 1 + int(r.random() < 0.08)
            sp.legacy = "%d" % no
            legacy.append(sp)
    acct = 2061400
    for sp in legacy:
        acct += 1
        sp.acct = "KP%07d" % acct
    acct += 37
    for opened, bid, k, sp in spells:
        if sp.legacy is None:
            acct += 1 + int(r.random() < 0.03)
            sp.acct = "KP%07d" % acct


def _et_offset(t):
    """Hours Eastern time sits behind UTC at naive local time t (US rules since 2007)."""
    y = t.year
    mar = dt.date(y, 3, 1)
    start = dt.datetime.combine(mar + dt.timedelta(days=(6 - mar.weekday()) % 7 + 7), dt.time(2, 0))
    nov = dt.date(y, 11, 1)
    stop = dt.datetime.combine(nov + dt.timedelta(days=(6 - nov.weekday()) % 7), dt.time(2, 0))
    return 4 if start <= t < stop else 5


def quarters(a, b):
    out = []
    y, q = a.year, (a.month - 1) // 3 + 1
    while (y, q) <= (b.year, (b.month - 1) // 3 + 1):
        out.append((y, q))
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


def qbounds(y, q):
    a = dt.date(y, 3 * q - 2, 1)
    z = dt.date(y + (1 if q == 4 else 0), 1 if q == 4 else 3 * q + 1, 1) - dt.timedelta(days=1)
    return a, z


PAYS_Q = {"w": 13, "b": 6.5, "s": 6, "m": 3}


def segments(b, sp):
    """The wages an account ran, by quarter and by system: (system, year, quarter, pay dates, employees, gross wages in
    dollars). A quarter that straddles the move has a legacy part (pay dates to 14 June 2024) and a current part."""
    rq = K.rng("quarters", b.key, sp.k)
    rows = []
    stop = sp.stop or END
    freq = NM.frequency(b)
    for (y, q) in quarters(sp.start, stop):
        a, z = qbounds(y, q)
        a2, z2 = max(a, sp.start), min(z, stop)
        if a2 > z2:
            continue
        if b.seasonal and q == 4:
            continue
        years = (a2 - b.first_pay).days / 365.25
        emp = max(1, int(round(b.employees0 * (1 + b.growth) ** max(0.0, years) * (0.9 + 0.2 * rq.random()))))
        level = emp * b.wage_q * (1.03 ** max(0.0, years)) * (0.94 + 0.12 * rq.random())
        parts = []
        if a2 <= LEGACY_LAST_PAY:
            parts.append(("legacy", a2, min(z2, LEGACY_LAST_PAY)))
        if z2 >= MIGRATION:
            parts.append(("current", max(a2, MIGRATION), z2))
        for system, u, v in parts:
            frac = ((v - u).days + 1) / ((z - a).days + 1)
            pays = max(1, int(round(frac * PAYS_Q[freq])))
            rows.append((system, y, q, pays, emp, round(level * frac, 2)))
    return rows


# ------------------------------------------------------------------------------------------------- the truth
def first_time(C):
    """Businesses whose first payroll ever ran with Kilbourne (the counting notes' first-time employer)."""
    return [b for b in C.business.values() if b.kind == "first"]


def chain(C, b):
    """The business and every successor that continued its payroll."""
    out = [b]
    while out[-1].succ is not None:
        out.append(C.business[out[-1].succ])
    return out


def paid_in(C, b, y, q):
    """True when Kilbourne paid wages for the business (any account, any successor) with a pay date in the quarter."""
    a, z = qbounds(y, q)
    for x in chain(C, b):
        for sp in x.spells:
            if not sp.paid_by_us(a):
                continue
            for row in segments(x, sp):
                if (row[1], row[2]) == (y, q) and row[5] > 0:
                    return True
    return False
