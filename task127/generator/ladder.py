"""task127 generator: the ladder, computed from the files as written (never from generator state).

Every rung, rival reading and fork-grid cell is a function of the frames load() reads out of target/.
checks.py asserts on these; verify_pack.py recomputes the same figures on its own code path.
"""
import math
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

import params as P
from world import holidays, workdays

F = P.F
QUAL_CODES = {"PF": "D", "ER": "E", "PB": "H"}
LABEL_SYS = {"propane furnace (ducted)": "D", "electric resistance": "E", "propane boiler (hydronic)": "H"}
BATCH_DAY = "2025-07-07"
AS_OF = P.AS_OF


def load(tgt):
    tgt = Path(tgt)
    sv = pd.read_csv(tgt / F["survey"])
    pl = pd.read_excel(tgt / F["pilot"], sheet_name="rebates", dtype={"premises_id": str, "rebate_id": str})
    host = pd.read_excel(tgt / F["hosting"], sheet_name="feeders", header=4)
    fmap = pd.read_csv(tgt / F["fmap"])
    fo = pd.read_csv(tgt / F["orders"], dtype=str, keep_default_na=False)
    tabs = {k: pd.read_excel(tgt / F["tables"], sheet_name=k, header=3) for k in ("H1", "H2", "H3", "H4")}
    code = {v: k for k, v in P.COOP_NAME.items()}
    for df in (sv, pl, host, fmap, fo):
        df["coop"] = df["coop"].map(code)
        assert df.coop.notna().all()
    return dict(sv=sv, pl=pl, host=host, fmap=fmap, fo=fo, tabs=tabs)


# ------------------------------------------------------------------ households and rates

def qualifying(sv):
    q = sv[(sv.tenure == "owner") & (sv.structure == P.STRUCT[0]) & sv.income_band.isin(P.IN_BAND)
           & sv.heating_system.isin(list(QUAL_CODES))].copy()
    q["sys"] = q.heating_system.map(QUAL_CODES)
    return q


def rates(D, by=("sys",)):
    """Install rates from the pilot log over the survey's qualifying households in the pilot neighbourhoods."""
    q = qualifying(D["sv"])
    pl = D["pl"].copy()
    pl["sys"] = pl.heating_system_replaced.map(LABEL_SYS)
    pn = set(pl.neighbourhood)
    qp = q[q.neighbourhood.isin(pn)]
    by = list(by)
    if not by:
        return {(): len(pl) / qp.weight.sum()}
    den = qp.groupby(by).weight.sum()
    num = pl.groupby(by).size()
    return {k if isinstance(k, tuple) else (k,): num.get(k, 0) / v for k, v in den.items()}


def backtest(D, by):
    """Predicted against actual pilot installs per pilot neighbourhood, under rates by `by`."""
    q = qualifying(D["sv"])
    pl = D["pl"]
    r = rates(D, by)
    out = {}
    for nb, g in q[q.neighbourhood.isin(set(pl.neighbourhood))].groupby("neighbourhood"):
        if by:
            pred = sum(w * r[tuple(row[b] for b in by)] for (_, row), w in zip(g.iterrows(), g.weight))
        else:
            pred = g.weight.sum() * r[()]
        act = int((pl.neighbourhood == nb).sum())
        out[nb] = (pred, act, pred / act - 1)
    return out


def nbhd_buyers(D, rate="system"):
    q = qualifying(D["sv"])
    pn = set(D["pl"].neighbourhood)
    q = q[~q.neighbourhood.isin(pn)]
    if rate == "system":
        r = rates(D, ("sys",))
        q = q.assign(b=q.weight * q.sys.map(lambda s: r[(s,)]))
    else:
        q = q.assign(b=q.weight * rates(D, ())[()])
    return q.groupby(["coop", "neighbourhood"]).b.sum()


def joint_counts(D):
    q = qualifying(D["sv"])
    q = q[~q.neighbourhood.isin(set(D["pl"].neighbourhood))]
    return q.groupby("coop").weight.sum().reindex(P.COOPS)


def product_counts(D):
    t = D["tabs"]
    h1 = t["H1"].set_index(t["H1"].columns[0])
    h2, h3, h4 = t["H2"], t["H3"], t["H4"].set_index(t["H4"].columns[0])
    out = {}
    for c in P.COOPS:
        name = P.COOP_NAME[c]
        row = h1.loc[name]
        hh = row.sum()
        pe = row["bottled, tank or LP gas"] + row["electricity"]
        g2 = h2[h2.iloc[:, 0] == name]
        own = g2[g2.iloc[:, 1] == "owner"].iloc[:, 2:].sum(axis=1).sum()
        g3 = h3[h3.iloc[:, 0] == name]
        det = g3[P.STRUCT[0]].sum()
        inc = h4.loc[name, P.IN_BAND].sum()
        out[c] = hh * (pe / hh) * (own / hh) * (det / hh) * (inc / hh)
    return pd.Series(out)


def largest_remainder(vals, total=P.SLOTS_TOTAL):
    s = sum(vals.values())
    quota = {k: v / s * total / 10 for k, v in vals.items()}
    base = {k: math.floor(v) for k, v in quota.items()}
    left = total // 10 - sum(base.values())
    order = sorted(quota, key=lambda k: -(quota[k] - base[k]))
    for k in order[:left]:
        base[k] += 1
    return {k: 10 * v for k, v in base.items()}


def allocate(expected):
    """The filed allocation rule: nearest ten each; shared by largest remainder where the total exceeds 1,800."""
    if sum(expected.values()) > P.SLOTS_TOTAL:
        return largest_remainder(expected)
    return {k: int(math.floor(v / 10 + 0.5)) * 10 for k, v in expected.items()}


def placeable(D, buyers=None, cap="feeder"):
    b = nbhd_buyers(D) if buyers is None else buyers
    host = D["host"].set_index("feeder")
    fm = D["fmap"].set_index(["coop", "neighbourhood"]).feeder
    out = {}
    for c in P.COOPS:
        bc = b.loc[c]
        if cap == "none":
            out[c] = bc.sum()
            continue
        if cap == "coop":
            slots = sum(int(host.loc[f, "hosting_capacity_remaining_kw"]) // P.KW_PER_HP
                        for f in host.index if host.loc[f, "coop"] == c)
            out[c] = min(bc.sum(), slots)
            continue
        per = {}
        for nb, v in bc.items():
            per.setdefault(fm.loc[(c, nb)], 0.0)
            per[fm.loc[(c, nb)]] += v
        out[c] = sum(min(v, int(host.loc[f, "hosting_capacity_remaining_kw"]) // P.KW_PER_HP) for f, v in per.items())
    return out


# ------------------------------------------------------------------ crews

def crew_record(D, c):
    fo = D["fo"]
    d = fo[(fo.coop == c) & (fo.completed_date != "")]
    batch = (d.order_type == "MXCH") & (d.requested_date == BATCH_DAY)
    std = d[(d.order_type != "HPRM") & ~batch]
    days = sorted(set(d.completed_date))
    days = [x for x in days if "2025-01-01" <= x <= "2026-12-10"]
    tot = d.groupby("completed_date").size()
    sc = std.groupby("completed_date").size()
    b = d[batch]
    out = dict(days=days, total=tot, standing=sc, batch_n=int(batch.sum()))
    if len(b):
        first, last = b.completed_date.min(), b.completed_date.max()
        plateau = [x for x in days if first <= x < last]
        out["plateau"] = plateau
        out["ceiling"] = float(np.mean([tot.get(x, 0) for x in plateau]))
    return out


def standing_level(R, d0, d1, exclude=None):
    days = [x for x in R["days"] if d0 <= x <= d1 and (exclude is None or not exclude(x))]
    return float(np.mean([R["standing"].get(x, 0) for x in days])), len(days)


def spare_of(D, c, std_window=None):
    R = crew_record(D, c)
    a, b = std_window or ((AS_OF - timedelta(days=364)).isoformat(), "2026-12-10")
    s, _ = standing_level(R, a, b)
    return R["ceiling"] - s, R["ceiling"], s


# ------------------------------------------------------------------ the 2027 queue

def forward_arrivals(D, coop=None, mapping="date"):
    pl = D["pl"]
    if coop is not None:
        pl = pl[pl.coop == coop]
    dates = pd.to_datetime(pl.install_date).dt.date
    n = len(pl)
    out = {}
    for x in dates:
        y = date(2027, x.month, x.day) if mapping == "date" else x + timedelta(days=364)
        out[y] = out.get(y, 0) + 1.0 / n
    return out


def crew_days_2027(four_day=True, thanksgiving=True):
    hol = holidays(2027)
    if not thanksgiving:
        hol = set()
    return set(workdays(date(2027, 1, 1), date(2027, 12, 31), hol, four_day=four_day))


def fluid_sets(P_c, spare, arr, wdays, weekly=False):
    """Meter sets by 31 December 2027: orders arrive on the mapped install dates and are worked from the
    crew's next working day, at `spare` a working day (or 4 x spare a week)."""
    q, done, served_week = 0.0, 0.0, {}
    d = date(2027, 1, 1)
    spring_left = None
    while d <= date(2027, 12, 31):
        if weekly:
            wk = d.isocalendar()[:2]
            if d.weekday() == 0 or (d == date(2027, 1, 1)):
                served_week[wk] = 0.0
            if d.weekday() < 4:
                cap = 4 * spare - served_week.get(wk, 0.0)
                s = min(q, cap if d.weekday() == 3 else min(cap, spare))
                served_week[wk] = served_week.get(wk, 0.0) + s
                q -= s
                done += s
        elif d in wdays:
            s = min(q, spare)
            q -= s
            done += s
        q += P_c * arr.get(d, 0.0)
        if d == date(2027, 8, 31):
            spring_left = q
        d += timedelta(days=1)
    return done, spring_left


def queue_sets(D, plc, spare, mapping="date", thanksgiving=True, weekly=False, per_coop=False):
    out = {}
    for c in P.COOPS:
        if c in spare:
            arr = forward_arrivals(D, c if per_coop else None, mapping)
            wd = crew_days_2027(True, thanksgiving)
            out[c], _ = fluid_sets(plc[c], spare[c], arr, wd, weekly)
        else:
            out[c] = plc[c]
    return out


def fcfs_sets(D, plc, c, ceiling, standing):
    """One queue in request order across standing and programme orders (the rival reading)."""
    arr = forward_arrivals(D)
    wd = crew_days_2027()
    q = []  # [kind, amount]
    done = 0.0
    d = date(2027, 1, 1)
    while d <= date(2027, 12, 31):
        if d in wd:
            capd = ceiling
            while capd > 1e-12 and q:
                k, a = q[0]
                s = min(a, capd)
                capd -= s
                if k == "p":
                    done += s
                if s >= a - 1e-12:
                    q.pop(0)
                else:
                    q[0][1] = a - s
            q.append(["s", standing])
        a = plc[c] * arr.get(d, 0.0)
        if a:
            q.append(["p", a])
        d += timedelta(days=1)
    return done


def slots(sets):
    return {c: int(math.floor(v / 10 + 0.5)) * 10 for c, v in sets.items()}


def golden(D):
    plc = placeable(D)
    sp = {c: spare_of(D, c)[0] for c in P.FOUR_DAY}
    sets = queue_sets(D, plc, sp)
    sl = slots(sets)
    placed = sum(sl.values())
    lead = max(sl, key=sl.get)
    second = sorted(sl.values())[-2]
    return dict(placeable=plc, spare=sp, sets=sets, slots=sl, placed=placed, unallocated=P.SLOTS_TOTAL - placed,
                leader=lead, lead_by=sl[lead] - second)
