"""Depreciation engine: Yacaaba's legacy conventions, the group ledger after cutover, and every wrong
path a solver can take (the variants). Money is Decimal, rounded half up to the cent per asset per
month, the last month taking the remainder."""
from decimal import Decimal, ROUND_HALF_UP

from params import LIFE_MONTHS, IT_OLD_LIFE, IT_CHANGE

CENT = Decimal("0.01")
ZERO = Decimal("0")


def r2(x):
    return Decimal(x).quantize(CENT, rounding=ROUND_HALF_UP)


def mi(y, m):
    return y * 12 + (m - 1)


def mdate(d):
    return mi(d.year, d.month)


def ym(i):
    return (i // 12, i % 12 + 1)


def label(i):
    y, m = ym(i)
    return "%04d-%02d" % (y, m)


REPLAY = list(range(mi(2025, 7), mi(2026, 9) + 1))
JUN25 = mi(2025, 6)
SEP26 = mi(2026, 9)
DEC26 = mi(2026, 12)
JAN27 = mi(2027, 1)
H2 = [mi(2027, m) for m in range(1, 7)]
Q4 = [mi(2026, m) for m in (10, 11, 12)]
CHANGE = mi(*IT_CHANGE)

TRUTH = dict(upgrade="host", it="prospective", impair=True, transfer="continue")


def sl(dep, life, start):
    """{month: amount}: straight line over `life` months from `start`."""
    dep = Decimal(dep)
    if life <= 0 or dep <= 0:
        return {}
    mon = r2(dep / life)
    out, acc = {}, ZERO
    for k in range(life):
        amt = mon if k < life - 1 else dep - acc
        out[start + k] = amt
        acc += amt
    return out


def taken_through(s, m):
    return sum((a for k, a in s.items() if k <= m), ZERO)


class Engine:
    """Schedules for one register under one variant. `assets` is the list of asset dicts."""

    def __init__(self, assets, variant=None):
        self.assets = assets
        self.by_id = {a["id"]: a for a in assets}
        self.v = dict(TRUTH)
        if variant:
            self.v.update(variant)
        self._cache = {}

    # ---------------------------------------------------------------- legacy schedules
    def schedule(self, a):
        if a["id"] in self._cache:
            return self._cache[a["id"]]
        s = self._schedule(a)
        if a.get("disposed"):
            d = mdate(a["disposed"])
            s = {k: x for k, x in s.items() if k <= d}            # Yacaaba charges the month of disposal
        self._cache[a["id"]] = s
        return s

    def host_end(self, a):
        return max(self.schedule(self.by_id[a["host"]]))

    def _schedule(self, a):
        v = self.v
        cat = a["category"]
        cost = a["cost"]
        st = mdate(a["acquired"])
        if a["kind"] == "upgrade":
            if v["upgrade"] in ("host",):
                life = self.host_end(a) - st + 1
                return sl(cost, life, st)
            if v["upgrade"] in ("five", "endhost"):
                return sl(cost, 60, st)
            if v["upgrade"] == "ten":
                return sl(cost, 120, st)
            if v["upgrade"] == "host_full":                       # the host's full class life from the upgrade
                return sl(cost, LIFE_MONTHS[self.by_id[a["host"]]["category"]], st)
            if v["upgrade"] == "host_less1":                      # remaining months counted without the upgrade month
                life = self.host_end(a) - st
                return sl(cost, life, st)
            if v["upgrade"] == "min60":                           # five years unless the system runs out sooner
                life = min(60, self.host_end(a) - st + 1)
                return sl(cost, life, st)
            if v["upgrade"] in ("host_years_floor", "host_years_round"):   # the host's remaining life in whole years
                r = self.host_end(a) - st + 1
                yrs = r // 12 if v["upgrade"] == "host_years_floor" else int((r + 6) // 12)
                return sl(cost, max(12, yrs * 12), st)
            raise ValueError(v["upgrade"])
        if a["kind"] == "transfer_in":
            t = a["transfer"]
            if v["transfer"] == "continue":
                return sl(cost - t["bf_accum"], t["source_end"] - st + 1, st)
            if v["transfer"] == "new":                             # the register row read as a new asset
                return sl(cost, LIFE_MONTHS[cat], st)
            raise ValueError(v["transfer"])
        if cat == "Computer equipment":
            if v["it"] == "prospective":
                if st >= CHANGE:
                    return sl(cost, LIFE_MONTHS[cat], st)
                old = sl(cost, IT_OLD_LIFE, st)
                before = {k: x for k, x in old.items() if k < CHANGE}
                if len(before) >= IT_OLD_LIFE:
                    return before
                acc = sum(before.values(), ZERO)
                rem = LIFE_MONTHS[cat] - len(before)
                out = dict(before)
                out.update(sl(cost - acc, rem, CHANGE))
                return out
            if v["it"] == "retro48":
                return sl(cost, LIFE_MONTHS[cat], st)
            if v["it"] == "old36":
                return sl(cost, IT_OLD_LIFE, st)
            raise ValueError(v["it"])
        s = sl(cost, LIFE_MONTHS[cat], st)
        if a.get("impair") and v["impair"]:
            m0, amt = a["impair"]
            before = {k: x for k, x in s.items() if k <= m0}
            acc = sum(before.values(), ZERO) + amt
            rem = max(s) - m0
            out = dict(before)
            out.update(sl(cost - acc, rem, m0 + 1))
            return out
        return s

    # ---------------------------------------------------------------- balances
    def impairment(self, a):
        return a["impair"][1] if (a.get("impair") and self.v["impair"]) else ZERO

    def brought_forward(self, a):
        if a["kind"] == "transfer_in" and self.v["transfer"] == "continue":
            return a["transfer"]["bf_accum"]
        return ZERO

    def accumulated(self, a, m):
        """Accumulated depreciation (and impairment) carried on the asset at the end of month m."""
        s = self.schedule(a)
        acc = taken_through(s, m) + self.brought_forward(a)
        if a.get("impair") and self.v["impair"] and m >= a["impair"][0]:
            acc += a["impair"][1]
        return acc

    def end_month(self, a):
        s = self.schedule(a)
        return max(s) if s else None

    def remaining_at_cutover(self, a):
        """Months the group ledger depreciates over from January 2027."""
        e = self.end_month(a)
        if e is None:
            return 0
        if a["kind"] == "upgrade" and self.v["upgrade"] == "endhost":
            e = min(e, self.host_end(a))
        return max(0, e - DEC26)

    def nbv(self, a, m):
        return a["cost"] - self.accumulated(a, m)

    def group_schedule(self, a):
        """The group ledger from cutover: straight line from loaded NBV over loaded remaining months."""
        rem = self.remaining_at_cutover(a)
        nb = self.nbv(a, DEC26)
        if rem <= 0 or nb <= 0:
            return {}
        return sl(nb, rem, JAN27)

    def h2(self, a):
        g = self.group_schedule(a)
        return sum((g[m] for m in H2 if m in g), ZERO)

    def q4(self, a):
        s = self.schedule(a)
        return sum((s[m] for m in Q4 if m in s), ZERO)

    def posting(self, a, m):
        return self.schedule(a).get(m, ZERO)
