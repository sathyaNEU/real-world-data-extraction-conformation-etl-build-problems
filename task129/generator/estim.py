"""task129 estimators, reading only the shipped bundle: outages from the restoration steps, one outage per device
interruption, the major event days (IEEE 1366 2.5 beta), the tree-caused outage rate per 100 miles in service, the
regrowth clock behind each outage and each mile-day, the drivers' shares of the cooperative's rise, and the asks"""
import os
from datetime import date

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

DISTRICTS = ("North", "East", "South")
BASE = (2021, 2022, 2023)
YEAR = 2025
OUTGOING = "Hollenbeck Line Clearance, Inc."
INCOMING = "Garrity Vegetation Services, LLC"
HANDOVER = {"North": pd.Timestamp("2024-01-01"), "East": pd.Timestamp("2025-04-01")}
FT = 5280.0


def load(target):
    f = lambda n: os.path.join(target, n)
    rd = lambda n: pd.read_csv(f(n), dtype=str, keep_default_na=False)
    return dict(X=rd("oms_outage_export_2016-2025.csv"), R=rd("trim_unit_register.csv"),
                T=rd("row_trim_completions_2012-2025.csv"),
                S=pq.read_table(f("row_tree_survey_2023-2024.parquet")).to_pandas(),
                W=rd("weather_daily_2016-2025.csv"), M=rd("member_counts_2015-2025.csv"),
                I=rd("ap_invoices_row_trimming_2024-12_2025-12.csv"))


# ------------------------------------------------------------------------------------------------ outages
def outage_table(X):
    """one row per outage record, its customer-minutes added over the restoration steps"""
    x = X.copy()
    x["start"] = pd.to_datetime(x.start_local)
    x["rest"] = pd.to_datetime(x.step_restored_local)
    x["mins"] = (x.rest - x.start).dt.total_seconds() / 60.0
    x["cm"] = x.members_restored.astype(int) * x.mins
    g = x.groupby("outage_id", sort=False)
    O = g.agg(start=("start", "first"), end=("rest", "max"), level=("level", "first"),
              district=("service_area", "first"), circuit=("circuit", "first"), unit_id=("unit_id", "first"),
              device_type=("device_type", "first"), device_id=("device_id", "first"), cause=("cause_code", "first"),
              members=("members_out", "first"), cm=("cm", "sum"), steps=("step", "count")).reset_index()
    O["members"] = O.members.astype(int)
    O["dur"] = (O.end - O.start).dt.total_seconds() / 60.0
    O["cm_naive"] = O.members * O.dur
    O["sustained"] = O.dur > 5
    O["date"] = O.start.dt.normalize()
    O["year"] = O.start.dt.year
    return O


def one_per_interruption(O, mode="golden"):
    """the outage records that are separate interruptions: a record of a device whose interruption is already open
    (it starts before that interruption's last restoration) is the same outage; the wrong modes keep every record,
    or keep one record per device and day"""
    if mode == "records":
        return O
    if mode == "device_day":
        return O.sort_values(["start", "outage_id"]).drop_duplicates(["device_id", "date"])
    O = O.sort_values(["device_id", "start", "outage_id"])
    keep = np.ones(len(O), bool)
    last = {}
    for i, (dev, s, e) in enumerate(zip(O.device_id.values, O.start.values, O.end.values)):
        open_end = last.get(dev)
        if open_end is not None and s <= open_end:
            keep[i] = False
            last[dev] = max(open_end, e)
        else:
            last[dev] = e
    return O[keep].sort_values(["start", "outage_id"])


def members_served(M):
    m = M.copy()
    m["members"] = m.members_at_year_end.astype(int)
    m["year"] = m.year.astype(int)
    return m.groupby("year").members.sum(), m.set_index(["district", "year"]).members


def daily_saidi(O, M, cm="cm"):
    sys_m, _ = members_served(M)
    u = O[(O.cause != "PLANNED") & O.sustained]
    d = u.groupby("date")[cm].sum()
    return d / d.index.year.map(sys_m).values


def major_event_days(O, M, years=range(2021, 2026), ddof=1, cm="cm"):
    """IEEE 1366 2.5 beta: each year's threshold from the logs of the five prior years' non-zero daily SAIDI"""
    s = daily_saidi(O, M, cm)
    out = {}
    for y in years:
        h = s[(s.index.year >= y - 5) & (s.index.year <= y - 1)]
        h = h[h > 0]
        lg = np.log(h.values)
        t = float(np.exp(lg.mean() + 2.5 * lg.std(ddof=ddof)))
        cur = s[s.index.year == y]
        out[y] = (t, sorted(cur[cur > t].index))
    return out


def med_set(meds):
    return {d for y in meds for d in meds[y][1]}


def threshold_margin(O, M, meds, cm="cm"):
    """the nearest day to a threshold, as a ratio of its SAIDI to the threshold (major event days above, others below)"""
    s = daily_saidi(O, M, cm)
    above, below = [], []
    for y, (t, days) in meds.items():
        cur = s[s.index.year == y]
        above += list(cur[cur > t].values / t)
        below += list(cur[cur <= t].values / t)
    return min(above), max(below)


# ------------------------------------------------------------------------------------------------ miles in service
def register(R):
    r = R.copy()
    r["miles"] = r.miles.astype(float)
    r["ins"] = pd.to_datetime(r.in_service_date)
    r["ret"] = pd.to_datetime(r.retired_date.replace("", "2099-12-31"))
    return r


def miles_avg(R, year, basis="days"):
    r = register(R)
    y0, y1 = pd.Timestamp(year, 1, 1), pd.Timestamp(year + 1, 1, 1)
    if basis == "year_end":
        on = (r.ins <= pd.Timestamp(year, 12, 31)) & (r.ret > pd.Timestamp(year, 12, 31))
        return r[on].groupby("district").miles.sum()
    if basis == "year_start":
        on = (r.ins <= y0) & (r.ret > y0)
        return r[on].groupby("district").miles.sum()
    days = (y1 - y0).days
    a = r.ins.clip(lower=y0)
    b = (r.ret + pd.Timedelta(days=1) if basis == "inclusive" else r.ret).clip(upper=y1)
    frac = ((b - a).dt.days.clip(lower=0)) / days
    return (r.miles * frac).groupby(r.district).sum()


def miles_end(R, year=YEAR, mode="golden"):
    r = register(R)
    end = pd.Timestamp(year, 12, 31)
    if mode == "blank_only":
        on = (r.ins <= end) & (r.retired_date == "")
    elif mode == "every_unit":
        on = r.ins <= end
    else:
        on = (r.ins <= end) & (r.ret > end)
    return r[on].groupby("district").miles.sum()


# ------------------------------------------------------------------------------------------------ the rate
def tree_outages(D, mode="golden", meds=None):
    O = outage_table(D["X"])
    Ou = one_per_interruption(O, "records" if mode == "records" else "golden")
    if meds is None:
        meds = major_event_days(Ou, D["M"])
    md = med_set(meds)
    t = Ou[(Ou.cause == "TREE") & Ou.sustained & (Ou.level == "PRIMARY")]
    if mode == "with_secondary":
        t = Ou[(Ou.cause == "TREE") & Ou.sustained]
    if mode == "with_med":
        return t
    if mode == "with_momentary":
        t = Ou[(Ou.cause == "TREE") & (Ou.level == "PRIMARY")]
    return t[~t.date.isin(md)]


def rates(D, mode="golden", basis="days", meds=None):
    t = tree_outages(D, mode, meds)
    out = {}
    for y in range(2021, 2026):
        mi = miles_avg(D["R"], y, basis)
        c = t[t.year == y].groupby("district").size().reindex(list(DISTRICTS)).fillna(0)
        out[y] = {d: 100.0 * c[d] / mi[d] for d in DISTRICTS}
        out[y]["all"] = 100.0 * c.sum() / mi.sum()
    return out


def components(rt):
    base = float(np.mean([rt[y]["all"] for y in BASE]))
    return dict(rate_2025=rt[YEAR]["all"], rate_base=base)


# ------------------------------------------------------------------------------------------------ the regrowth clock
def trim_history(D, basis="completed"):
    """the dates each unit's trims reset its regrowth clock: accepted trims (by completion date, or by acceptance date),
    and a rebuilt unit's in-service date (left out under the no_rebuild reading)"""
    T = D["T"]
    a = T[T.audit_status == "ACCEPTED"].copy()
    a["d"] = pd.to_datetime(a.accepted_date if basis == "accepted" else a.completed_date)
    hist = {u: (np.sort(g.d.values), g.sort_values("d").contractor.values) for u, g in a.groupby("unit_id")}
    r = register(D["R"])
    for u, ins in zip(r.unit_id, r.ins):
        if ins.year >= 2024 and basis != "no_rebuild":
            d, c = hist.get(u, (np.array([], "datetime64[ns]"), np.array([], object)))
            d = np.concatenate([d, [np.datetime64(ins, "ns")]])
            c = np.concatenate([c, ["(rebuilt)"]])
            o = np.argsort(d, kind="stable")
            hist[u] = (d[o], c[o])
        elif u not in hist:
            hist[u] = (np.array([np.datetime64(ins, "ns")]), np.array(["(new)"], object))
    return hist


BANDS = [1, 2, 3, 4]
BAND_NAMES = ["0-1", "1-2", "2-3", "3-4", "past cycle"]


def exposure(D, hist, years=range(2021, 2026)):
    """mile-years each unit spent in each time-since-trim band, by year, with the contractor of its last trim"""
    r = register(D["R"])
    y0 = min(years)
    days = pd.date_range("%d-01-01" % y0, "%d-12-31" % max(years), freq="D")
    dv = days.values
    yi = days.year.values - y0
    rows = []
    for u, d, mi, ins, ret in zip(r.unit_id, r.district, r.miles, r.ins, r.ret):
        alive = (dv >= np.datetime64(ins, "ns")) & (dv < np.datetime64(ret, "ns"))
        if not alive.any():
            continue
        cd, cc = hist[u]
        p = np.maximum(np.searchsorted(cd, dv, side="right") - 1, 0)
        t = (dv - cd[p]).astype("timedelta64[D]").astype(float) / 365.25
        key = ((yi * 5 + np.digitize(t, BANDS)) * len(cd) + p)[alive]
        cnt = np.bincount(key)
        for k in np.nonzero(cnt)[0]:
            yb, pi = divmod(int(k), len(cd))
            rows.append((u, d, y0 + yb // 5, yb % 5, cc[pi], cnt[k] / 365.25 * mi))
    return pd.DataFrame(rows, columns=["unit_id", "district", "yr", "band", "con", "mi_yr"])


def clock_at(t_out, hist):
    """each outage's time since its unit's last trim and the contractor of that trim"""
    tt, cc = [], []
    for u, s in zip(t_out.unit_id.values, t_out.start.values):
        cd, con = hist[u]
        p = np.searchsorted(cd, s, side="right") - 1
        tt.append(float((s - cd[max(p, 0)]) / np.timedelta64(1, "D")) / 365.25)
        cc.append(con[max(p, 0)])
    return np.array(tt), np.array(cc, object)


def ash_share(D):
    """share of the trees within falling distance that are ash, by unit, from each unit's latest survey"""
    S = D["S"]
    ash = S[S.species_code.isin(["FRAX", "ASH"])].groupby("unit_id").trees_within_falling_distance.sum()
    tot = S.groupby("unit_id").trees_within_falling_distance.sum()
    return (ash.reindex(tot.index).fillna(0) / tot)


def ash_gradient(t, E, sh, district="North"):
    """a district's tree-caused outage rate by year and quartile of its units' ash share"""
    nu = E[E.district == district].unit_id.unique()
    q = pd.qcut(sh.reindex(nu).fillna(0), 4, labels=False)
    n = t[t.district == district].assign(aq=lambda x: x.unit_id.map(q)).groupby(["year", "aq"]).size()
    m = E[E.district == district].assign(aq=lambda x: x.unit_id.map(q)).groupby(["yr", "aq"]).mi_yr.sum()
    return (n / m.rename_axis(["year", "aq"]) * 100.0).unstack()


def evidence(D, basis="completed"):
    """the comparisons the call stands on: rates by district, year and time since trim; North's 2025 rate on units
    each contractor trimmed in the same months; the rise by ash share; each driver's share of the rise"""
    t = tree_outages(D)
    t = t[t.year >= 2021].copy()
    hist = trim_history(D, basis)
    E = exposure(D, hist)
    tt, cc = clock_at(t, hist)
    t["band"] = np.digitize(tt, BANDS)
    t["con"] = cc
    t["yr"] = t.year
    rate = lambda F, X, keys: (F.groupby(keys).size() / X.groupby(keys).mi_yr.sum() * 100.0)
    by_band = {d: rate(t[t.district == d], E[E.district == d], ["yr", "band"]).unstack() for d in DISTRICTS}
    base = {d: by_band[d].loc[list(BASE)].mean() for d in DISTRICTS}
    rise = {d: (by_band[d].loc[YEAR] - base[d]) for d in DISTRICTS}
    # North 2025: units last trimmed by the outgoing firm against the new firm's, and against their own baseline
    n25 = t[(t.district == "North") & (t.year == YEAR)]
    En = E[(E.district == "North") & (E.yr == YEAR)]
    by_con = rate(n25, En, ["con"])
    by_con_band = rate(n25, En, ["con", "band"]).unstack()
    # each contractor's 2025 outages on the North units it last trimmed, against the count North's 2025 rates at each
    # time since trim would give its units (indirect standardisation)
    mis = En.groupby(["con", "band"]).mi_yr.sum().unstack().fillna(0.0)
    cnt = n25.groupby(["con", "band"]).size().unstack().reindex(index=mis.index, columns=mis.columns).fillna(0.0)
    pool = cnt.sum() / mis.sum()
    std = {}
    for c in (OUTGOING, INCOMING):
        o, e = float(cnt.loc[c].sum()), float((mis.loc[c] * pool).sum())
        std[c] = (int(o), e, o / e)
    # the same months: North units each contractor trimmed during 2024, read over 2025
    T = D["T"]
    h1 = T[(T.audit_status == "ACCEPTED") & (T.completed_date >= "2024-01-01") & (T.completed_date <= "2024-12-31")]
    h1 = h1[h1.unit_id.str.startswith("N")]
    grp = h1.drop_duplicates("unit_id").set_index("unit_id").contractor
    same = {}
    for c in (OUTGOING, INCOMING):
        us = grp[grp == c].index
        mi = float(E[(E.yr == YEAR) & E.unit_id.isin(us)].mi_yr.sum())
        n = int(t[(t.year == YEAR) & t.unit_id.isin(us)].shape[0])
        same[c] = (n, mi, 100.0 * n / mi if mi else float("nan"))
    # the shift no trim removes: the rise on units in their first two years since trim (growth-in near zero there)
    young = {d: float((t[(t.district == d) & (t.year == YEAR) & (t.band <= 1)].shape[0]
                       / E[(E.district == d) & (E.yr == YEAR) & (E.band <= 1)].mi_yr.sum()
                       - np.mean([t[(t.district == d) & (t.year == y) & (t.band <= 1)].shape[0]
                                  / E[(E.district == d) & (E.yr == y) & (E.band <= 1)].mi_yr.sum() for y in BASE])) * 100)
             for d in DISTRICTS}
    # ash: the North rise by quartile of ash share
    by_ash = ash_gradient(t, E, ash_share(D))
    # each driver's share of the cooperative's rise (counts above the 2021 to 2023 rate, at 2025's mile-years)
    mi25 = E[E.yr == YEAR].groupby("district").mi_yr.sum()
    total = 0.0
    parts = {}
    for d in DISTRICTS:
        tot_rise = float((t[(t.district == d) & (t.year == YEAR)].shape[0] / mi25[d]
                          - np.mean([t[(t.district == d) & (t.year == y)].shape[0]
                                     / E[(E.district == d) & (E.yr == y)].mi_yr.sum() for y in BASE])) * mi25[d])
        shift = young[d] / 100.0 * mi25[d]
        past = E[(E.district == d) & (E.yr == YEAR) & (E.band == 4)].mi_yr.sum()
        past_base = np.mean([E[(E.district == d) & (E.yr == y) & (E.band == 4)].mi_yr.sum() for y in BASE])
        yrs = list(BASE) + [YEAR]
        n4 = t[(t.district == d) & t.yr.isin(yrs) & (t.band == 4)].shape[0]
        m4 = E[(E.district == d) & E.yr.isin(yrs) & (E.band == 4)].mi_yr.sum()
        r_past = 100.0 * n4 / m4 if m4 else 0.0              # past-cycle units' rate, pooled over the years' exposure
        r_young = float(base[d][[0, 1]].mean())
        backlog = (past - past_base) * (r_past - r_young) / 100.0
        parts[d] = dict(rise=tot_rise, shift=shift, backlog=backlog, rest=tot_rise - shift - backlog)
        total += tot_rise
    shares = {"trees beyond the right-of-way (North)": parts["North"]["shift"] / total,
              "units past the cycle (East)": parts["East"]["backlog"] / total,
              "weather (South)": max(parts["South"]["rise"], 0.0) / total}
    return dict(by_band=by_band, base=base, rise=rise, by_con=by_con, by_con_band=by_con_band, std=std, young=young, same=same,
                by_ash=by_ash, parts=parts, total=total, shares=shares, E=E, t=t, hist=hist)


# ------------------------------------------------------------------------------------------------ the call and its rungs
PROGRAMMES = {"contractor": "a re-bid of the trimming contract", "cycle": "catch-up trimming",
              "beyond": "hazard-tree removal beyond the right-of-way", "weather": "nothing new"}


def default_path(D, rt):
    """the district rise read against the contract register: the districts carrying the rise are the ones whose
    trimming changed hands, and each rise starts with its handover"""
    rise = {d: rt[YEAR][d] - np.mean([rt[y][d] for y in BASE]) for d in DISTRICTS}
    lead = max(rise, key=rise.get)
    return "contractor" if lead in HANDOVER else "weather", rise


def golden_call(ev):
    s = ev["shares"]
    top = max(s, key=s.get)
    return {"trees beyond the right-of-way (North)": "beyond", "units past the cycle (East)": "cycle",
            "weather (South)": "weather"}[top]


# ------------------------------------------------------------------------------------------------ the asks
def ask_billing(D, mode="golden"):
    """miles each contractor billed for trimming done in each quarter of 2025; a credit memo carries the service
    month of the invoice it reverses"""
    I = D["I"].copy()
    I["q"] = I.quantity.astype(float)
    trim = I[I.item_code.str.startswith("TRIM")].copy()
    trim["mi"] = np.where(trim.uom == "LF", trim.q / FT, trim.q)
    if mode == "golden":
        month_of = dict(zip(I.invoice_no, I.service_month))
        trim["svc"] = [m if m else month_of.get(a, "") for m, a in zip(trim.service_month, trim.applies_to_invoice)]
    elif mode == "positive":
        trim = trim[trim.doc_type == "INVOICE"]
        trim["svc"] = trim.service_month
    elif mode == "signed_by_month":
        trim["svc"] = trim.service_month
    elif mode == "wo_month":
        trim = trim[trim.doc_type == "INVOICE"].drop_duplicates(["vendor", "work_order", "service_month"])
        trim["svc"] = trim.service_month
    elif mode == "invoice_date":
        trim["svc"] = trim.invoice_date.str[:7]
    trim = trim[trim.svc.str.startswith(str(YEAR))]
    trim["quarter"] = "Q" + ((trim.svc.str[5:7].astype(int) - 1) // 3 + 1).astype(str)
    g = trim.groupby(["vendor", "quarter"]).mi.sum()
    return {(v, q): float(g.get((v, q), 0.0)) for v in (OUTGOING, INCOMING) for q in ("Q1", "Q2", "Q3", "Q4")}


def ask_med(D, mode="golden"):
    """for each district: outages, members interrupted and customer-minutes on 2025's major event days (unplanned
    sustained outages on primary and secondary)"""
    O = outage_table(D["X"])
    Ou = one_per_interruption(O)
    meds = major_event_days(Ou, D["M"])
    days = set(meds[YEAR][1])
    base = O if mode in ("records", "naive") else Ou
    u = base[(base.cause != "PLANNED") & base.sustained & base.date.isin(days)]
    if mode == "primary_only":
        u = u[u.level == "PRIMARY"]
    if mode == "tree_only":
        u = u[u.cause == "TREE"]
    cm = "cm_naive" if mode in ("naive", "outage_minutes") else "cm"
    out = {}
    for d in DISTRICTS:
        x = u[u.district == d]
        out[d] = (int(len(x)), int(x.members.sum()), int(round(x[cm].sum())))
    return out, sorted(days)


def ask_miles(D, mode="golden"):
    m = miles_end(D["R"], YEAR, mode)
    return {d: float(m.get(d, 0.0)) for d in DISTRICTS}
