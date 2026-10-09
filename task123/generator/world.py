"""True income paths, portal return versions and annual returns for the task123 world.

Totals first: every organisation's discrete quarterly income is generated in whole dollars, then
its filing behaviour (original returns, corrections, management fourth quarters and their true-up,
annual returns reaching the register) is laid over the totals. Lines and payments are added in
lines.py once the published rounds have fixed the Steady Ground instalments.
"""
import datetime as dt
from dataclasses import dataclass, field

import numpy as np

from common import (SEED, NQ, SPINE_FIRST, LAST_Q, MARCH_CENSUSES, SEPT_CENSUS, EXTRACT_DATE,
                    qend, fyq, fy_q4)
from roster import Q

CENSUS_DATES = MARCH_CENSUSES + [SEPT_CENSUS]


def hash_key(k):
    """Stable integer from a string or int (Python's hash() is salted per process)."""
    if isinstance(k, (int, np.integer)):
        return int(k)
    h = 7
    for ch in str(k):
        h = (h * 131 + ord(ch)) % 2_147_483_647
    return h


def rng_for(*keys):
    return np.random.default_rng([SEED] + [hash_key(k) for k in keys])


# ----------------------------------------------------------------------------- true totals

def seasonal(o):
    r = rng_for("season", o.key)
    s = 1 + 0.05 * r.standard_normal(4)
    return s / s.mean()


def true_totals(o, eps_seed=0):
    """Discrete quarterly total income, whole dollars, internal quarters 0..36."""
    r = rng_for("eps", o.key, eps_seed)
    eps = r.standard_normal(NQ) * o.sigma
    s = seasonal(o)
    base = o.income / 4.0
    out = np.zeros(NQ, dtype=np.int64)
    for i in range(NQ):
        t = (i - Q(2024, 6)) / 4.0
        c = (qend(i).month // 3) - 1
        v = base * (1 + o.growth) ** t * s[c] * o.dips.get(i, 1.0) * (1 + eps[i])
        out[i] = int(round(v))
    return out


# ----------------------------------------------------------------------------- calendar helpers

def at(d, hh=10, mm=0):
    return dt.datetime(d.year, d.month, d.day, hh, mm)


def near_census(d):
    return any(abs((d - c).days) <= 1 for c in CENSUS_DATES)


def clear_of_census(d):
    """Move a date forward off any census day and the day either side of it."""
    while near_census(d):
        d += dt.timedelta(days=1)
    return d


def business(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def ok_day(d):
    return clear_of_census(business(d))


@dataclass
class Version:
    ref: str            # grant reference
    org: str            # org key
    q: int              # internal quarter
    no: int             # version number
    status: str         # accepted | rejected | withdrawn
    submitted: dt.datetime
    accepted: dt.datetime   # None unless accepted
    ytd: int            # total income, year to date
    kind: str           # original | mgmt | trueup | correction | linesplit | coding | withdrawn
    shift: dict = field(default_factory=dict)   # line misclassification carried by this version
    lines: dict = None  # filled in lines.py: code -> (ytd, prior-year comparative)
    err_line: str = None  # the line a total-income error sits on (None: spread, as management figures are)


@dataclass
class AnnualReturn:
    org: str
    q4: int
    received: dt.date          # None if it had not reached the register by the extract
    total: int
    eventual: dt.date = None   # outstanding at the extract: when it later arrived (never shipped)


# ----------------------------------------------------------------------------- annual returns

SPECIAL_JUNE = {
    "J1": {2022: dt.date(2023, 4, 18)},
    "J2": {2023: dt.date(2024, 5, 9)},
    "J3": {2022: dt.date(2023, 3, 31)},
    "J4": {2025: dt.date(2026, 3, 31)},
}
D2_PLAN = {2018: dt.date(2019, 2, 14), 2019: dt.date(2020, 2, 18), 2020: dt.date(2021, 2, 16),
           2021: dt.date(2022, 4, 21), 2022: dt.date(2023, 2, 9), 2023: dt.date(2024, 5, 14),
           2024: dt.date(2025, 3, 31), 2025: dt.date(2026, 2, 12)}


def received_date(o, q4, r):
    fye = qend(q4)
    if o.bal == 12:
        y = fye.year + 1
        if o.key == "D1":
            return dt.date(y, 5, 5) + dt.timedelta(days=int(r.integers(0, 18)))
        if o.key == "D2":
            return D2_PLAN[fye.year]
        if o.key == "D3":
            return dt.date(y, 2, 2) + dt.timedelta(days=int(r.integers(0, 18)))
        return dt.date(y, 4, 1) + dt.timedelta(days=int(r.integers(0, 80)))
    if o.bal == 6:
        if o.key in SPECIAL_JUNE and fye.year in SPECIAL_JUNE[o.key]:
            return SPECIAL_JUNE[o.key][fye.year]
        if fye.year == 2026:
            return None
        if r.random() < 0.14:
            return dt.date(fye.year + 1, 1, 6) + dt.timedelta(days=int(r.integers(0, 60)))
        return dt.date(fye.year, 9, 25) + dt.timedelta(days=int(r.integers(0, 96)))
    # 31 March
    if fye.year == 2026:
        st = o.sept_status
        if st == "deadline":
            return dt.date(2026, 9, 30)
        if st in ("oct", "later"):
            return None
        return dt.date(2026, 7, 13) + dt.timedelta(days=int(r.integers(0, 75)))
    if r.random() < 0.10:
        return dt.date(fye.year, 10, 2) + dt.timedelta(days=int(r.integers(0, 75)))
    return dt.date(fye.year, 7, 8) + dt.timedelta(days=int(r.integers(0, 84)))


def first_fy_q4(o):
    if o.first_q <= SPINE_FIRST:
        return None
    return fy_q4(o.first_q, o.bal)


def build_annual(orgs, tot):
    out = {}
    for o in orgs:
        r = rng_for("annual", o.key)
        f4 = first_fy_q4(o)
        for q4 in range(3, NQ):
            if fyq(q4, o.bal) != 4 or qend(q4).year < 2018:
                continue
            if f4 is not None and q4 < f4:
                continue
            if q4 > o.last_q + 2:
                continue
            total = int(tot[o.key][q4 - 3:q4 + 1].sum())
            rec = received_date(o, q4, r)
            out[(o.key, q4)] = AnnualReturn(o.key, q4, rec, total)
    octs = sorted(o.key for o in orgs if o.bal == 3 and o.sept_status == "oct")
    for k, key in enumerate(octs):
        out[(key, Q(2026, 3))].received = dt.date(2026, 10, [1, 2, 5, 6, 6, 7][k])
    for o in orgs:
        r = rng_for("eventual", o.key)
        if o.bal == 3 and o.sept_status == "later":
            out[(o.key, Q(2026, 3))].eventual = dt.date(2026, 10, 13) + dt.timedelta(
                days=int(r.integers(0, 70)))
        if o.bal == 6 and (o.key, Q(2026, 6)) in out:
            out[(o.key, Q(2026, 6))].eventual = dt.date(2026, 10, 21) + dt.timedelta(
                days=int(r.integers(0, 70)))
    return out


# ----------------------------------------------------------------------------- portal versions

def org_refs(o):
    refs = [("op", o.og_ref, o.first_q, o.last_q)]
    if o.dual:
        refs.append(("pg", o.pg_ref, o.pg_first_q, o.last_q))
    return refs


def ytd_true(tot_o, o, q):
    k = fyq(q, o.bal)
    return int(tot_o[q - k + 1:q + 1].sum())


def original_dates(o, ref, q, r):
    qe = qend(q)
    k = fyq(q, o.bal)
    lag = int(r.integers(26, 52)) if k == 4 else int(r.integers(16, 44))
    sub = business(qe + dt.timedelta(days=lag))
    acc = ok_day(sub + dt.timedelta(days=int(r.integers(1, 9))))
    return (at(sub, int(r.integers(8, 18)), int(r.integers(0, 60))),
            at(acc, int(r.integers(9, 17)), int(r.integers(0, 60))))


def q4_plan(orgs, annual, plan):
    """Decide, for every fourth-quarter return, whether the management figure is exact and when the
    true-up lands. A return that reached the register by a census has its true-up accepted by that
    census or an exact management figure."""
    out = {}
    for o in orgs:
        r = rng_for("q4plan", o.key)
        for (key, q4), ar in annual.items():
            if key != o.key:
                continue
            spec = plan.get((o.key, q4), {})
            exact = spec.get("mgmt_exact")
            eps = float(np.clip(r.normal(0, 0.011), -0.028, 0.028))
            if abs(eps) < 0.003:
                eps = 0.003 if eps >= 0 else -0.003
            lag = int(r.integers(5, 26))
            if exact is None:
                exact = r.random() < 0.2
            rec = ar.received
            tu = None
            if not exact and rec is not None:
                tu = ok_day(rec + dt.timedelta(days=lag))
                if any(rec <= c < tu for c in CENSUS_DATES):
                    if "mgmt_exact" in spec:
                        raise AssertionError(f"designed inexact Q4 {o.key} {q4} straddles a census")
                    exact, tu = True, None
                elif tu > EXTRACT_DATE:
                    tu = None
            out[(o.key, q4)] = {"exact": exact, "eps": spec.get("mgmt_eps", eps), "trueup": tu}
    return out


def build_versions(orgs, tot, annual, plan, q4p):
    versions = []
    for o in orgs:
        r = rng_for("filing", o.key)
        for kind, ref, f, l in org_refs(o):
            for q in range(max(f, SPINE_FIRST), min(l, LAST_Q) + 1):
                versions.extend(file_quarter(o, kind, ref, q, tot[o.key], annual, plan, q4p, r))
    return versions


def file_quarter(o, rkind, ref, q, tot_o, annual, plan, q4p, r):
    out = []
    k = fyq(q, o.bal)
    true = ytd_true(tot_o, o, q)
    s_dt, a_dt = original_dates(o, ref, q, r)
    spec = plan.get((o.key, q), {})
    v1 = true
    kind1 = "original"
    if k == 4:
        kind1 = "mgmt"
        p = q4p.get((o.key, q))
        if p is not None and not p["exact"]:
            v1 = int(round(true * (1 + p["eps"])))
    e1 = spec.get("v1_error", {}).get(rkind, 0)
    v1 += e1
    first = Version(ref, o.key, q, 1, "accepted", s_dt, a_dt, v1, kind1,
                    shift=dict(spec.get("v1_shift", {}).get(rkind, {})),
                    err_line=spec.get("err_line", "other") if e1 else None)
    out.append(first)
    events = []
    if k == 4:
        p = q4p.get((o.key, q))
        if p is not None and p["trueup"] is not None and v1 != true:
            events.append({"date": p["trueup"], "kind": "trueup", "refs": "both", "ytd": true})
    for ev in spec.get("events", []):
        e = dict(ev)
        e.setdefault("ytd", true + e.pop("error_after", 0))
        events.append(e)
    events.sort(key=lambda e: e["date"])
    cur, no, last = v1, 1, a_dt
    cur_shift = dict(first.shift)
    cur_err = first.err_line
    for e in events:
        if e["refs"] != "both" and e["refs"] != rkind:
            continue
        no += 1
        d = e["date"]
        sd = at(d, int(r.integers(8, 12)), int(r.integers(0, 60)))
        shift = dict(e.get("shift", {}))
        if e["kind"] in ("coding", "withdrawn"):
            status = "rejected" if e["kind"] == "coding" else "withdrawn"
            if e["kind"] == "withdrawn":
                shift = dict(cur_shift)
            out.append(Version(ref, o.key, q, no, status, sd, None, cur, e["kind"], shift=shift,
                               err_line=cur_err))
            continue
        acc = ok_day(d + dt.timedelta(days=int(e.get("review_days", r.integers(0, 4)))))
        ad = at(acc, int(r.integers(12, 18)), int(r.integers(0, 60)))
        if ad <= last:
            ad = last + dt.timedelta(hours=3)
        ytd = cur if e["kind"] == "linesplit" else e["ytd"]
        err = cur_err if ytd == cur and e["kind"] == "linesplit" else None
        out.append(Version(ref, o.key, q, no, "accepted", sd, ad, ytd, e["kind"], shift=shift, err_line=err))
        cur, last, cur_shift, cur_err = ytd, ad, shift, err
    return out
