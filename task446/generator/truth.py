"""Generator-side truth: obligor-group resolution under the policy, exposures, projections.
Used by make.py (limits, RM codes) and checks.py (assertions). solve.py re-derives everything from
target/ on its own code path."""
import math
from world import QE, PROJ_DATE, CCF_COMMITTED

FX = {"EUR": [1.1462, 1.1531, 1.1598, 1.1689, 1.1452], "USD": [1.3415, 1.3087, 1.3256, 1.3519, 1.3381],
      "GBP": [1.0] * 5}
CONS = ("IS_DIRECTLY_CONSOLIDATED_BY", "IS_ULTIMATELY_CONSOLIDATED_BY")


def active(r, d):
    return r["start"] <= d and (r["end"] is None or d < r["end"])


class Resolver:
    """Obligor group top at date d under the policy (consolidation incl. lapsed records, branch to head
    office, funds stand alone, merged LEIs to their successor)."""

    def __init__(self, w, d, follow_funds=False, drop_lapsed_rr=False, branches=True, successors=True,
                 known_at=None):
        self.w, self.d = w, d
        known_at = known_at or d
        self.parent = {}
        self.branch = {}
        self.fundmgr = {}
        for r in w.rel:
            if r["reg"] > known_at or not active(r, d):
                continue
            if drop_lapsed_rr and r["lapsed_from"] is not None and r["lapsed_from"] <= known_at:
                continue
            if r["type"] == "IS_ULTIMATELY_CONSOLIDATED_BY":
                self.parent[r["child"]] = r["parent"]
            elif r["type"] == "IS_DIRECTLY_CONSOLIDATED_BY":
                self.parent.setdefault(("direct", r["child"]), r["parent"])
            elif r["type"] == "IS_INTERNATIONAL_BRANCH_OF":
                self.branch[r["child"]] = r["parent"]
            elif r["type"] == "IS_FUND-MANAGED_BY":
                self.fundmgr[r["child"]] = r["parent"]
        self.follow_funds, self.branches, self.successors = follow_funds, branches, successors

    def top(self, lei):
        seen = set()
        cur = lei
        while cur not in seen:
            seen.add(cur)
            e = self.w.ent.get(cur)
            if self.successors and e is not None and e["merged_on"] is not None and e["merged_on"] <= self.d:
                cur = e["successor"]
                continue
            if self.branches and cur in self.branch:
                cur = self.branch[cur]
                continue
            if cur in self.parent:
                cur = self.parent[cur]
                continue
            if ("direct", cur) in self.parent:
                cur = self.parent[("direct", cur)]
                continue
            if self.follow_funds and cur in self.fundmgr:
                cur = self.fundmgr[cur]
                continue
            return cur
        return cur


_MS = {}


def migration_sources(facs):
    key = id(facs)
    if key not in _MS:
        _MS[key] = {(g.migrated_from, t) for g in facs if g.migrated_from for t in range(5)
                    if g.limit[t] is not None}
    return _MS[key]


def fac_exposure(f, t, dedup_migration=True, ccf=CCF_COMMITTED, fx=True, all_facilities=None):
    lim, dr = f.limit[t], f.drawn[t]
    if lim is None or dr is None:
        return 0.0
    if dedup_migration and all_facilities is not None:
        # the source facility of a migration is not counted while the receiving one is on the book
        if (f.ref, t) in migration_sources(all_facilities):
            return 0.0
    rate = FX[f.ccy][t] if fx else 1.0
    drawn = dr / rate
    undrawn = max(0.0, lim * 1e6 - dr) / rate
    if f.ftype == "OVD":
        return drawn
    return drawn + ccf * undrawn


def sec_exposure(s, t, fx=True):
    v = s["cv"][t]
    if v is None:
        return 0.0
    return v / (FX[s["ccy"]][t] if fx else 1.0)


def drv_exposure(n, t, thousands=True, collateral=True):
    m = n["mtm_k"][t] * (1000.0 if thousands else 1.0)
    c = 0.0
    if collateral and n["coll"] is not None:
        c = n["coll"][t] / FX[n["coll_ccy"]][t]
    return max(0.0, m - c)


def group_exposures(w, assign, t, **kw):
    """assign(lei, t) -> group top; returns dict top -> exposure (GBP) at QE t, by book."""
    out = {}
    def add(top, book, v):
        d = out.setdefault(top, {"loans_drawn": 0.0, "undrawn": 0.0, "securities": 0.0, "derivatives": 0.0})
        d[book] += v
    for f in w.fac:
        if f.limit[t] is None:
            continue
        tot = fac_exposure(f, t, all_facilities=w.fac, dedup_migration=kw.get("dedup", True),
                           fx=kw.get("fx", True))
        if tot == 0.0:
            continue
        rate = FX[f.ccy][t] if kw.get("fx", True) else 1.0
        drawn = f.drawn[t] / rate
        top = assign(f.lei, t)
        add(top, "loans_drawn", drawn)
        add(top, "undrawn", tot - drawn)
    for s in w.sec:
        v = sec_exposure(s, t, fx=kw.get("fx", True))
        if v:
            add(assign(s["lei"], t), "securities", v)
    for n in w.drv:
        v = drv_exposure(n, t, thousands=kw.get("thousands", True), collateral=kw.get("collateral", True))
        if v:
            add(assign(n["lei"], t), "derivatives", v)
    return out


def ls_slope(series):
    xs = [1, 2, 3, 4, 5]
    xm = 3.0
    ym = sum(series) / 5.0
    return sum((x - xm) * (y - ym) for x, y in zip(xs, series)) / 10.0


def approvable(limit_m, projected, req_m, ccf):
    """largest multiple of 0.1m <= request with projected + ccf*amount <= limit"""
    room = limit_m * 1e6 - projected
    if room <= 0:
        return 0.0
    amt = math.floor(round(room / ccf / 1e5, 9)) / 10.0
    return min(req_m, amt)
