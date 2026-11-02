"""task129 estimators, reading only the shipped bundle: outages from the restoration steps, one outage per device
interruption, the major event days (IEEE 1366 2.5 beta), the tree-caused outage rate per 100 miles in service, the
regrowth clock behind each outage and each mile-day, the drivers' shares of the cooperative's rise, and the asks"""
import os
import re
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
                I=rd("ap_trimming_invoice_lines_2024-12_2026-01.csv"))


# ------------------------------------------------------------------------------------------------ outages
def outage_table(X):
    """one row per outage record, its customer-minutes added over the restoration steps"""
    x = X.copy()
    x["start"] = pd.to_datetime(x.start_local)
    x["rest"] = pd.to_datetime(x.step_restored_local)
    x["mins"] = (x.rest - x.start).dt.total_seconds() / 60.0
    x["cm"] = x.members_restored.astype(int) * x.mins
    g = x.groupby("ticket_no", sort=False)
    O = g.agg(start=("start", "first"), end=("rest", "max"), level=("level", "first"),
              district=("service_area", "first"), circuit=("circuit", "first"), unit_id=("unit_id", "first"),
              device_type=("device_type", "first"), device_id=("device_id", "first"), cause=("cause_code", "first"),
              members=("members_out", "first"), cm=("cm", "sum"), steps=("step", "count")).reset_index()
    O = O.rename(columns={"ticket_no": "outage_id"})
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
MONTHS = {m: i + 1 for i, m in enumerate(("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV",
                                           "DEC"))}
SLASH_PERIOD = re.compile(r"(\d{2})/(\d{2})/(\d{4})-(\d{2})/(\d{2})/(\d{4})")
MONTH_PERIOD = re.compile(r"\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) (\d{4})\b")


def stated_month(text):
    """the month of the work a line states in its own text, where the firm typed one"""
    m = SLASH_PERIOD.search(text)
    if m:
        return "%s-%s" % (m.group(3), m.group(1))
    m = MONTH_PERIOD.search(text)
    if m:
        return "%s-%02d" % (m.group(2), MONTHS[m.group(1)])
    return ""


def trim_lines(D, mode="golden"):
    """the trimming lines in miles, each with the month of the work it bills under the reading named by mode:
    golden, the month the line states, else the keyed service month, a paper credit memo at its reversed invoice's
    month; service_month (the cracker), every credit memo netted against the invoice it reverses and the rest at their
    service month; own_month, every signed line at its own service month (a blank credit at its invoice's); lag, the
    invoice month less one with credits netted; positive, invoices only at their service month"""
    I = D["I"].copy()
    I["q"] = I.quantity.astype(float)
    tr = I[I.item_code.str.startswith("TRIM")].copy()
    tr["mi"] = np.where(tr.uom == "LF", tr.q / FT, tr.q)
    reversed_ = set(tr.applies_to_invoice[tr.doc_type == "CREDIT MEMO"])
    if mode == "golden":
        stated = tr.description.map(stated_month)
        own = np.where(stated != "", stated, tr.service_month)
        month_of = dict(zip(tr.invoice_no, own))
        tr["svc"] = [o if o else month_of.get(a, "") for o, a in zip(own, tr.applies_to_invoice)]
    elif mode == "service_month":
        tr = tr[(tr.doc_type != "CREDIT MEMO") & ~tr.invoice_no.isin(reversed_)].copy()
        tr["svc"] = tr.service_month
    elif mode == "own_month":
        month_of = dict(zip(tr.invoice_no, tr.service_month))
        tr["svc"] = [m if m else month_of.get(a, "") for m, a in zip(tr.service_month, tr.applies_to_invoice)]
    elif mode == "lag":
        tr = tr[(tr.doc_type != "CREDIT MEMO") & ~tr.invoice_no.isin(reversed_)].copy()
        p = pd.to_datetime(tr.invoice_date).dt.to_period("M") - 1
        tr["svc"] = p.astype(str)
    elif mode == "positive":
        tr = tr[tr.doc_type == "INVOICE"].copy()
        tr["svc"] = tr.service_month
    return tr


def ask_billing(D, mode="golden"):
    """miles each contractor billed for trimming done in each quarter of 2025"""
    tr = trim_lines(D, mode)
    tr = tr[tr.svc.str.startswith(str(YEAR))].copy()
    tr["quarter"] = "Q" + ((tr.svc.str[5:7].astype(int) - 1) // 3 + 1).astype(str)
    g = tr.groupby(["vendor", "quarter"]).mi.sum()
    return {(v, q): float(g.get((v, q), 0.0)) for v in (OUTGOING, INCOMING) for q in ("Q1", "Q2", "Q3", "Q4")}


def wo_district(D):
    """each work order's district, through its trimmed units in the completions and the unit register"""
    T = D["T"][["work_order", "unit_id"]].drop_duplicates()
    m = T.merge(D["R"][["unit_id", "district"]], on="unit_id", how="left")
    return m.groupby("work_order").district.agg(lambda s: sorted(set(s)))


def ask_district(D, mode="golden"):
    """miles billed for trimming done in each district in 2025"""
    tr = trim_lines(D, mode)
    tr = tr[tr.svc.str.startswith(str(YEAR))]
    wd = wo_district(D)
    dist = tr.work_order.map(lambda w: wd[w][0] if w in wd.index and len(wd[w]) == 1 else "")
    g = tr.mi.groupby(dist).sum()
    return {d: float(g.get(d, 0.0)) for d in DISTRICTS}


def openings(X, mode="golden"):
    """the device openings an export's tickets hold, each with its ticket, device, start, end, members and
    customer-minutes. golden: a ticket's steps split at each step whose members restored are negative (the device off
    again after its members were restored: a new opening, its members the step's, its minutes from that step);
    literal: one opening a ticket, customer-minutes added over every step as the steps stand; net: a negative step
    netted against the restoration it reverses (the battery's reading of a reversal); drop: negative steps dropped"""
    x = X[["ticket_no", "start_local", "level", "service_area", "device_id", "cause_code", "members_out", "step",
           "step_restored_local", "members_restored"]].copy()
    x["s"] = pd.to_datetime(x.start_local)
    x["t"] = pd.to_datetime(x.step_restored_local)
    x["r"] = x.members_restored.astype(int)
    x["k"] = x.step.astype(int)
    x = x.sort_values(["ticket_no", "k"])
    out = []
    for tk, g in x.groupby("ticket_no", sort=False):
        f = g.iloc[0]
        head = dict(ticket=tk, level=f.level, district=f.service_area, device_id=f.device_id, cause=f.cause_code)
        steps = list(zip(g.t, g.r))
        if mode == "drop":
            steps = [(t, r) for t, r in steps if r >= 0]
        if mode == "net":
            kept = []
            for t, r in steps:
                if r < 0:
                    for j in range(len(kept) - 1, -1, -1):
                        if kept[j][1] == -r:
                            kept.pop(j)
                            break
                else:
                    kept.append((t, r))
            steps = kept
        if mode == "golden":
            segs, cur = [], [(f.s, int(f.members_out), [])]
            for t, r in steps:
                if r < 0:
                    cur.append((t, -r, []))
                else:
                    cur[-1][2].append((t, r))
            segs = cur
        else:
            segs = [(f.s, int(f.members_out), steps)]
        for start, mem, st in segs:
            end = max(t for t, _ in st) if st else start
            cm = sum(r * (t - start).total_seconds() / 60.0 for t, r in st)
            out.append(dict(head, start=start, end=end, members=mem, cm=cm))
    O = pd.DataFrame(out)
    O["dur"] = (O.end - O.start).dt.total_seconds() / 60.0
    O["sustained"] = O.dur > 5
    O["date"] = O.start.dt.normalize()
    return O


def fold(O):
    """policy 2.1: a device is in one outage at a time, so an opening that starts before its device's latest
    restoration so far is that outage"""
    O = O.sort_values(["device_id", "start", "ticket"])
    keep = np.ones(len(O), bool)
    last = {}
    for i, (dev, s, e) in enumerate(zip(O.device_id.values, O.start.values, O.end.values)):
        open_end = last.get(dev)
        if open_end is not None and s <= open_end:
            keep[i] = False
            last[dev] = max(open_end, e)
        else:
            last[dev] = e
    return O[keep]


def ask_med(D, mode="golden"):
    """for each district: outages, members interrupted and customer-minutes 2025's major event days took out of the
    reliability figures (unplanned sustained outages on primary and secondary). Stops: cracker (folded, a negative
    step netted as a reversal), literal (folded, one outage a ticket, steps as they stand), drop (negative steps
    dropped), records (every ticket, steps as they stand), primary_only, tree_only, outage_minutes (members times the
    last restoration's minutes)"""
    O = outage_table(D["X"])
    Ou = one_per_interruption(O)
    meds = major_event_days(Ou, D["M"])
    days = set(meds[YEAR][1])
    X = D["X"][pd.to_datetime(D["X"].start_local).dt.normalize().isin(days)]
    how = {"golden": "golden", "cracker": "net", "literal": "literal", "drop": "drop", "records": "literal",
           "primary_only": "golden", "tree_only": "golden", "outage_minutes": "literal"}[mode]
    P_ = openings(X, how)
    if mode != "records":
        P_ = fold(P_)
    u = P_[(P_.cause != "PLANNED") & P_.sustained & P_.date.isin(days)]
    if mode == "primary_only":
        u = u[u.level == "PRIMARY"]
    if mode == "tree_only":
        u = u[u.cause == "TREE"]
    out = {}
    for d in DISTRICTS:
        x = u[u.district == d]
        cm = (x.members * x.dur).sum() if mode == "outage_minutes" else x.cm.sum()
        out[d] = (int(len(x)), int(x.members.sum()), int(round(cm)))
    return out, sorted(days)
