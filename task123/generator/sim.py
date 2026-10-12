"""Simulate the region's residential gas premises through the 2025-26 winter: premises and their counties,
occupancy (accounts, move-outs and move-ins), Pine Harbor's October 2025 AMI conversion, daily use, each
utility's read calendar, the bills, Pine Harbor's MDMS daily reads and the meter history.

Every premise draws from its own seeded stream (world.rng with the premise key), so trimming a county's
premise list for bin placement leaves every other premise's records unchanged.
"""
from datetime import timedelta

import numpy as np

import events as EV
import world as W

D = W.D
TD = timedelta


class Premise:
    __slots__ = ("pid", "pk", "util", "county", "town", "size", "bmul", "hmul", "ami", "cycle", "route", "group",
                 "install", "accounts", "use", "reads", "street", "meter_old", "meter_new", "cls", "events", "nil",
                 "closed")


def _premise_id(util, county, k):
    """Premise numbers embed the county's two-digit district and a scrambled sequence: unique by construction."""
    ci = W.COUNTY_ORDER.index(county) + 1
    seq = (k * 7919 + 3301) % 100000
    if util == "KVG":
        return "KV%02d%05d" % (ci, seq)
    if util == "NNG":
        return "P%02d%05d" % (ci, seq)
    return "PH-%02d%05d" % (ci, seq)


STREETS = ["Birch", "Cedar", "Hemlock", "Tamarack", "Spruce", "Maple", "Lakeview", "Ridge", "Mill", "Orchard",
           "Pine", "School", "Church", "Railroad", "Harbor", "Bay", "Hillcrest", "Sunset", "Forest", "River",
           "Elm", "Oak", "Willow", "Aspen", "Poplar", "Juniper", "Marquette", "Huron", "Superior", "Erie"]
SUFFIX = ["St", "Ave", "Rd", "Dr", "Ln", "Ct", "Trl", "Hwy"]


def meter_ids(p):
    """Pine Harbor's meters: the dial meter at every premise, and the AMI meter with its shutoff valve at the
    converted ones. Scrambled sequences, unique by construction."""
    ci = W.COUNTY_ORDER.index(p.county) + 1
    n = ci * 20000 + p.pk
    p.meter_old = "D%08d" % ((n * 7919 + 2203) % 100000000)
    p.meter_new = "AV%07d" % ((n * 104729 + 7013) % 10000000) if p.ami else None


def build_premises(trim=None, pool=False):
    """All residential premises, county by county; trim[county] removes that many of the county's last
    non-AMI premises (bin placement)."""
    trim = trim or {}
    out = []
    for county, (util, n, fac, centre, spread, amish) in W.COUNTIES.items():
        made = []
        for k in range(n + 80):
            r = W.rng("prem", county, k)
            p = Premise()
            p.util, p.county, p.pk = util, county, k
            p.pid = _premise_id(util, county, k)
            p.town = W.TOWNS[county][int(r.integers(0, len(W.TOWNS[county])))]
            p.street = "%d %s %s" % (int(r.integers(100, 9900)), STREETS[int(r.integers(0, len(STREETS)))],
                                     SUFFIX[int(r.integers(0, len(SUFFIX)))])
            p.ami = bool(util == "PHE" and r.random() < amish)
            p.size = float(r.lognormal(0, 0.30)) * fac * (W.AMI_SIZE if p.ami else 1.0)
            p.bmul = float(r.lognormal(0, 0.05))
            p.hmul = float(r.lognormal(0, 0.04))
            if util == "KVG":
                p.cycle = int(np.clip(round(r.normal(centre, spread)), 1, 21))
            elif util == "PHE":
                p.cycle = int(np.clip(round(r.normal(centre, spread)), 1, 20))
            else:
                p.route = int(np.clip(round(r.normal(centre, spread)), 1, 20))
                p.group = "A" if r.random() < 0.5 else "B"
            p.cls = "RES"
            if util == "PHE":
                meter_ids(p)
            else:
                p.meter_old = p.meter_new = None
            made.append(p)
        keep = made[:n]
        extra = trim.get(county, 0)
        if extra > 0:
            keep = keep + [p for p in made[n:] if not p.ami][:extra]
        elif extra < 0:
            idx = set([i for i in range(len(keep) - 1, -1, -1) if not keep[i].ami][:-extra])
            keep = [p for i, p in enumerate(keep) if i not in idx]
        if pool:
            for p in made:
                p.cls = "RES" if (made.index(p) < n or not p.ami) else "POOL-AMI"
            out.extend(made)
        else:
            out.extend(keep)
    # Kestrel Valley's Tillery corner, read on the late cycles
    for k in range(W.TILLERY_KVG):
        r = W.rng("prem", "Tillery-KVG", k)
        p = Premise()
        p.util, p.county, p.pk = "KVG", "Tillery", 50000 + k
        p.pid = _premise_id("KVG", "Tillery", 50000 + k)
        p.town = "North Tillery"
        p.street = "%d %s %s" % (int(r.integers(100, 9900)), STREETS[int(r.integers(0, len(STREETS)))],
                                 SUFFIX[int(r.integers(0, len(SUFFIX)))])
        p.ami = False
        p.size = float(r.lognormal(0, 0.30)) * 0.95
        p.bmul, p.hmul = float(r.lognormal(0, 0.05)), float(r.lognormal(0, 0.04))
        p.cycle = int(np.clip(round(r.normal(19, 1.5)), 1, 21))
        p.cls = "RES"
        p.meter_old = p.meter_new = None
        out.append(p)
    return out


def account_numbers(p, j):
    """The j-th account at premise p, unique by construction (district, scrambled premise and occupancy)."""
    ci = W.COUNTY_ORDER.index(p.county) + 1
    n = p.pk * 11 + j
    if p.util == "KVG":
        body = "%02d%07d" % (ci, (n * 7919 + 17) % 10000000)
        chk = sum(int(c) * (i % 3 + 1) for i, c in enumerate(body)) % 10
        return body + str(chk)
    if p.util == "NNG":
        return "4%02d%05d" % (ci, (n * 7919 + 29) % 100000)
    return "70%02d%06d" % (ci, (n * 7919 + 41) % 1000000)


def ami_account(p, j):
    ci = W.COUNTY_ORDER.index(p.county) + 1
    return "88%02d%06d" % (ci, ((p.pk * 11 + j) * 104729 + 53) % 1000000)


def occupancy(p):
    """Accounts at the premise: list of (account, start gas day, end gas day inclusive or None)."""
    r = W.rng("occ", p.pid)
    acc = []
    start = D(2024, 1, 1) + TD(int(r.integers(0, 600)))
    j = 0
    cur = account_numbers(p, j)
    if p.ami:
        p.install = W.AMI_INSTALL_FROM + TD(int(r.integers(0, (W.AMI_INSTALL_TO - W.AMI_INSTALL_FROM).days + 1)))
        while p.install.weekday() >= 5:
            p.install += TD(1)
    else:
        p.install = None
    moves = []
    d = W.SIM_START
    while d <= W.SIM_END:
        if r.random() < 0.0125:   # move-outs per month
            day = d + TD(int(r.integers(0, 28)))
            while day.weekday() >= 5:
                day += TD(1)
            if day <= W.SIM_END:
                moves.append(day)
        d = (d.replace(day=1) + TD(32)).replace(day=1)
    moves = sorted(set(m for m in moves if not (p.install and abs((m - p.install).days) < 5)))
    for m in moves:
        acc.append([cur, start, m])
        j += 1
        cur = account_numbers(p, j)
        start = m + TD(1)
    acc.append([cur, start, None])
    if p.ami:
        # the October conversion: the account active at install ends on the install day and the same customer
        # continues under a new calendar-billed account number from the next gas day
        out = []
        for jj, (a, s, e) in enumerate(acc):
            if s <= p.install and (e is None or e > p.install):
                out.append([a, s, p.install])
                out.append([ami_account(p, jj), p.install + TD(1), e])
            elif s > p.install:
                out.append([ami_account(p, jj), s, e])
            else:
                out.append([a, s, e])
        acc = out
    p.accounts = acc
    return acc


def daily_use(prem):
    """therms used on each gas day, one row per premise (float64)."""
    n = len(prem)
    U = np.empty((n, W.NDAY))
    for i, p in enumerate(prem):
        r = W.rng("use", p.pid)
        z = r.normal(0, W.DAY_NOISE, W.NDAY)
        U[i] = p.size * (W.BASE * p.bmul + W.HEAT * p.hmul * W.HDD) * (1 + z)
    U = np.maximum(U, 0.02)
    for d, h in W.DST_HOURS.items():
        U[:, W.IDX[d]] *= h / 24.0
    for i, p in enumerate(prem):
        EV.apply_nil(U[i], p.nil)
    return U


def account_on(p, day):
    for a, s, e in p.accounts:
        if s <= day and (e is None or day <= e):
            return a
    return None


def schedule_reads(p):
    """Scheduled read dates (the meter is read during the day; that gas day belongs to the bill read then)."""
    reads = set()
    if p.util in ("KVG", "PHE"):
        n = 21 if p.util == "KVG" else 20
        for y, m in W.MONTHS:
            d = W.cycle_day(y, m, p.cycle, n)
            if not p.ami or d <= p.install:
                reads.add(d)
    elif p.util == "NNG":
        months = [(2025, 9), (2025, 11), (2026, 1), (2026, 3), (2026, 5)] if p.group == "A" else \
            [(2025, 10), (2025, 12), (2026, 2), (2026, 4)]
        for y, m in months:
            reads.add(W.cycle_day(y, m, p.route, 20))
    for a, s, e in p.accounts:
        if e is not None and W.SIM_START <= e <= W.SIM_END:
            reads.add(e)          # final read on the move-out day
    if p.ami and p.install:
        reads.add(p.install)      # the conversion read on the old meter
    return sorted(d for d in reads if W.SIM_START <= d <= W.SIM_END)


def intervals(p):
    """Read-to-read intervals (prior read, read], each with its account; for AMI premises after the
    install, calendar-month bills split at account changes."""
    out = []
    if p.ami:
        reads = [d for d in schedule_reads(p) if d <= p.install]
        for a, b in zip(reads[:-1], reads[1:]):
            out.append(("CYCLE", a, b, account_on(p, b)))
        # calendar months from the day after the install
        d = p.install + TD(1)
        while d <= W.SIM_END:
            mend = (d.replace(day=1) + TD(32)).replace(day=1) - TD(1)
            seg_start = d
            cur = account_on(p, d)
            x = d
            while x <= mend:
                a2 = account_on(p, x)
                if a2 != cur:
                    out.append(("CALENDAR", seg_start - TD(1), x - TD(1), cur))
                    seg_start, cur = x, a2
                x += TD(1)
            out.append(("CALENDAR", seg_start - TD(1), mend, cur))
            d = mend + TD(1)
        return out
    reads = schedule_reads(p)
    for a, b in zip(reads[:-1], reads[1:]):
        out.append(("CYCLE", a, b, account_on(p, b)))
    return out


class Bill:
    __slots__ = ("util", "pid", "county", "account", "basis", "start", "end", "therms", "ccf", "reg0", "reg1",
                 "read_type", "txn", "bill_no", "posted", "true")


EST_OK = lambda d: d <= D(2025, 11, 30) or d >= D(2026, 3, 1)


def make_bills(prem, U):
    """Every bill rendered for a read between 1 October 2025 and the 15 April 2026 pull, with the
    utilities' own conventions. Returns the bill records and Pine Harbor's MDMS daily reads."""
    bills, mdms = [], {}
    cum = np.cumsum(U, axis=1)

    def tsum(i, a, b):   # therms on gas days (a, b]
        ia, ib = W.IDX[a], W.IDX[b]
        return cum[i, ib] - cum[i, ia]

    for i, p in enumerate(prem):
        r = W.rng("bill", p.pid)
        ivs = intervals(p)
        if p.ami:
            # MDMS daily reads in CCF from the install, a few estimated days from communication gaps
            day0 = W.IDX[p.install] + 1
            ccf = U[i, day0:] / W.HV_PHE
            qual = np.array(["V"] * len(ccf), dtype=object)
            gaps = r.random(len(ccf)) < 0.004
            if gaps.any():
                ccf = ccf.copy()
                ccf[gaps] = ccf[gaps] * (1 + r.normal(0, 0.06, gaps.sum()))
                qual[gaps] = "E"
            ccf = np.round(ccf, 2)
            # the export carries a meter's reads only while a residential account is on it
            for k in range(len(ccf)):
                if account_on(p, W.DAYS[day0 + k]) is None:
                    ccf[k] = np.nan
            mdms[p.pid] = (day0, ccf, qual)
        reg = float(r.integers(1000, 60000))   # Northbank register start (CCF)
        if p.util == "NNG":
            hv = np.array([W.HV_NNG_MONTH[(d.year, d.month)] for d in W.DAYS])
            vcum = np.cumsum(U[i] / hv)
        reg_at = {}
        est = {}
        for basis, a, b, acct in ivs:
            if b < D(2025, 10, 1) or b > W.BILL_PULL - TD(1) or acct is None:
                continue
            bl = Bill()
            bl.util, bl.pid, bl.county, bl.account, bl.basis = p.util, p.pid, p.county, acct, basis
            bl.start, bl.end = a, b
            true = tsum(i, a, b)
            bl.true = true
            bl.read_type, bl.txn, bl.ccf, bl.reg0, bl.reg1 = "A", "BILL", None, None, None
            bl.bill_no, bl.posted = None, None
            if p.util == "NNG":
                r0 = reg + vcum[W.IDX[a]]
                r1 = reg + vcum[W.IDX[b]]
                bl.reg0, bl.reg1 = int(np.floor(r0)), int(np.floor(r1))
                bl.ccf = bl.reg1 - bl.reg0
                bl.therms = int(round(bl.ccf * W.HV_NNG_MONTH[(b.year, b.month)]))
            elif p.ami and basis == "CALENDAR":
                day0, ccf, _ = mdms[p.pid]
                lo, hi = W.IDX[a] + 1 - day0, W.IDX[b] + 1 - day0
                bl.therms = int(round(float(np.nansum(ccf[max(lo, 0):hi])) * W.HV_PHE))
            else:
                carry = est.pop("carry", 0.0)
                val = true + carry
                if p.util == "KVG" and EST_OK(b) and r.random() < 0.03:
                    e = float(r.normal(0, 0.10))
                    est["carry"] = -true * e
                    val = true * (1 + e) + carry
                    bl.read_type = "E"
                bl.therms = int(round(val))
            bills.append(bl)
            if p.util == "KVG" and r.random() < 0.005 and bl.read_type == "A":
                # a misread corrected: the original, its cancel and the rebill, under one bill number
                delta = int(round(bl.therms * float(r.normal(0, 0.02)))) or 1
                orig = Bill()
                for f in Bill.__slots__:
                    setattr(orig, f, getattr(bl, f))
                orig.therms, orig.txn = bl.therms + delta, "BILL"
                cncl = Bill()
                for f in Bill.__slots__:
                    setattr(cncl, f, getattr(orig, f))
                cncl.therms, cncl.txn = -(bl.therms + delta), "CNCL"
                bl.txn = "RBIL"
                bills.pop()
                bills.extend([orig, cncl, bl])
    return bills, mdms


def build(trim=None, pool=False):
    if trim is None and not pool:
        trim = W.TRIM
    prem = build_premises(trim, pool)
    for p in prem:
        occupancy(p)
        p.events, p.nil = EV.draw(p)
        p.events = EV.close_unpaid(p, p.events)
    U = daily_use(prem)
    bills, mdms = make_bills(prem, U)
    return prem, U, bills, mdms
