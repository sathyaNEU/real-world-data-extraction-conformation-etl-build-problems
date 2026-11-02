"""task129 verifier: recomputes every figure the write-up states from the shipped bundle alone, with its own code (never
the generator's estimators), and compares each with figures.json at the stated rounding

    python3 task129/generator/verify.py <target dir> <figures.json>
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

DIST = ["North", "East", "South"]
OC, NC = "Hollenbeck Line Clearance, Inc.", "Garrity Vegetation Services, LLC"


def f1(x):
    return "{:,.1f}".format(x)


def read(target, name):
    return pd.read_csv(os.path.join(target, name), dtype=str, keep_default_na=False)


def outages(target):
    """one row per outage record (ENG-REL-02 2.1, 3.1), then the records of a device already out folded into its
    interruption: a record starting before the device's latest restoration so far is the same outage"""
    X = read(target, "oms_outage_export_2016-2025.csv")
    s = pd.to_datetime(X.start_local)
    r = pd.to_datetime(X.step_restored_local)
    X = X.assign(s=s, r=r, cmin=X.members_restored.astype(int) * (r - s).dt.total_seconds() / 60.0)
    O = X.groupby("ticket_no").agg(s=("s", "min"), e=("r", "max"), dev=("device_id", "first"), lvl=("level", "first"),
                                   d=("service_area", "first"), cause=("cause_code", "first"), unit=("unit_id", "first"),
                                   mem=("members_out", "first"), cm=("cmin", "sum")).reset_index()
    O["mem"] = O.mem.astype(int)
    O = O.sort_values(["dev", "s", "ticket_no"]).reset_index(drop=True)
    prior = O.groupby("dev").e.transform(lambda z: z.cummax().shift())
    O = O[~(O.s <= prior)].copy()
    O["sus"] = (O.e - O.s).dt.total_seconds() > 300
    O["day"] = O.s.dt.normalize()
    O["yr"] = O.s.dt.year
    return O


def meds(O, target):
    """IEEE 1366 2.5 beta per ENG-REL-02 3.2"""
    M = read(target, "member_counts_2015-2025.csv")
    served = M.assign(n=M.members_at_year_end.astype(int)).groupby(M.year.astype(int)).n.sum()
    u = O[(O.cause != "PLANNED") & O.sus]
    daily = u.groupby("day").cm.sum()
    saidi = daily / np.array([served[d.year] for d in daily.index])
    out = {}
    for y in range(2021, 2026):
        h = saidi[(saidi.index.year >= y - 5) & (saidi.index.year < y) & (saidi > 0)]
        th = np.exp(np.log(h).mean() + 2.5 * np.log(h).std(ddof=1))
        out[y] = sorted(saidi[(saidi.index.year == y) & (saidi > th)].index)
    return out


def register(target):
    R = read(target, "trim_unit_register.csv")
    R["mi"] = R.miles.astype(float)
    R["a"] = pd.to_datetime(R.in_service_date)
    R["b"] = pd.to_datetime(R.retired_date.where(R.retired_date != "", "2200-01-01"))
    return R


def miles_in_year(R, y):
    """miles averaged over the days of the year (ENG-REL-02 2.2): a unit is in service from its in-service date to
    the day before its retirement date"""
    lo, hi = pd.Timestamp(y, 1, 1), pd.Timestamp(y + 1, 1, 1)
    days = (np.minimum(R.b, hi) - np.maximum(R.a, lo)).dt.days.clip(lower=0)
    return (R.mi * days / (hi - lo).days).groupby(R.district).sum()


def clocks(target, R):
    """each unit's regrowth clock resets: accepted trims by completion date (OPS-ROW-01 3.1, 4.2), and a unit built
    from 2024 on from its in-service date (3.2)"""
    T = read(target, "row_trim_completions_2012-2025.csv")
    T = T[T.audit_status == "ACCEPTED"]
    resets = {u: sorted(zip(pd.to_datetime(g.completed_date), g.contractor)) for u, g in T.groupby("unit_id")}
    for u, a in zip(R.unit_id, R.a):
        if a.year >= 2024 or u not in resets:
            resets[u] = sorted(resets.get(u, []) + [(a, "(new)")])
    return resets


def main(target, fig_path):
    fig = json.load(open(fig_path))
    bad = []

    def eq(label, got, want):
        if got != want:
            bad.append("%s: got %s, figures.json %s" % (label, got, want))

    O = outages(target)
    md = meds(O, target)
    allmed = {d for y in md for d in md[y]}
    eq("major event days 2025", [d.strftime("%-d %B %Y") for d in md[2025]], fig["med_days"])
    R = register(target)
    tree = O[(O.cause == "TREE") & (O.lvl == "PRIMARY") & O.sus & ~O.day.isin(allmed)]
    rate = {}
    for y in range(2021, 2026):
        mi = miles_in_year(R, y)
        n = tree[tree.yr == y].groupby("d").size().reindex(DIST, fill_value=0)
        rate[y] = {d: 100.0 * n[d] / mi[d] for d in DIST}
        rate[y]["all"] = 100.0 * n.sum() / mi[DIST].sum()
    eq("rate 2025", f1(rate[2025]["all"]), fig["rate_2025"])
    eq("rate 2021 to 2023", f1(np.mean([rate[y]["all"] for y in (2021, 2022, 2023)])), fig["rate_base"])
    for d in DIST:
        for y in range(2021, 2026):
            eq("rate %s %d" % (d, y), f1(rate[y][d]), fig["district_rates"][d][str(y)])
    eq("North 2025", f1(rate[2025]["North"]), fig["north_rate_2025"])
    eq("North 2021 to 2023", f1(np.mean([rate[y]["North"] for y in (2021, 2022, 2023)])), fig["north_rate_base"])
    # the regrowth clock: North's mile-years and tree-caused outages by year, time since the last reset (whole years,
    # four and over together) and the contractor of that reset
    resets = clocks(target, R)
    north = R[R.district == "North"]
    days = pd.date_range("2021-01-01", "2025-12-31", freq="D")
    yr = days.year.values
    expo = {}
    for u, mi, a, b in zip(north.unit_id, north.mi, north.a, north.b):
        on = (days >= a) & (days < b)
        if not on.any():
            continue
        rd = np.array([x[0] for x in resets[u]], "datetime64[ns]")
        who = np.array([x[1] for x in resets[u]], object)
        k = np.maximum(np.searchsorted(rd, days.values, side="right") - 1, 0)
        band = np.minimum(((days.values - rd[k]) / np.timedelta64(1, "D") / 365.25).astype(int), 4)
        df = pd.DataFrame({"y": yr[on], "b": band[on], "c": who[k][on]})
        for key, n in df.groupby(["y", "b", "c"]).size().items():
            expo[key] = expo.get(key, 0.0) + mi * n / 365.25
    expo = pd.Series(expo)
    nt = tree[(tree.d == "North") & (tree.yr >= 2021)]
    ob = {}
    for u, s_, y in zip(nt.unit, nt.s, nt.yr):
        prior = [x for x in resets[u] if x[0] <= s_]
        key = (y, min(int((s_ - prior[-1][0]).days / 365.25), 4), prior[-1][1])
        ob[key] = ob.get(key, 0) + 1
    ob = pd.Series(ob).reindex(expo.index, fill_value=0)
    young = {}
    for y in range(2021, 2026):
        sel = [k for k in expo.index if k[0] == y and k[1] <= 1]
        young[y] = 100.0 * ob[sel].sum() / expo[sel].sum()
    eq("North young shift", f1(young[2025] - np.mean([young[y] for y in (2021, 2022, 2023)])), fig["north_young_shift"])
    # each contractor's units against North's 2025 rates at the same time since trim
    k25 = [k for k in expo.index if k[0] == 2025]
    e25, o25 = expo[k25], ob[k25]
    pooled = o25.groupby(level=1).sum() / e25.groupby(level=1).sum()
    for c in (OC, NC):
        kc = [k for k in k25 if k[2] == c]
        expected = sum(expo[k] * pooled[k[1]] for k in kc)
        eq("contractor ratio %s" % c, "{:.2f}".format(o25[kc].sum() / expected), fig["contractor_ratio"][c])
    # ask A: trimming miles billed by contractor and quarter of the work: a portal line's own stated period, a paper
    # line's keyed service month, a paper credit memo at the month of the invoice it reverses
    I = read(target, "ap_trimming_invoice_lines_2024-12_2026-01.csv")
    mon = {m: k + 1 for k, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}

    def said(t):
        a = re.search(r"(\d\d)/\d\d/(\d{4})-\d\d/\d\d/\d{4}", t)
        if a:
            return "%s-%s" % (a.group(2), a.group(1))
        b = re.search(r"\b([A-Z]{3}) (20\d\d)\b", t)
        return "%s-%02d" % (b.group(2), mon[b.group(1)]) if b and b.group(1) in mon else ""

    tr = I[I.item_code.str.startswith("TRIM")].copy()
    tr["own"] = [said(t) or sm for t, sm in zip(tr.description, tr.service_month)]
    inv_month = tr[tr.doc_type == "INVOICE"].groupby("invoice_no").own.first()
    tr["m"] = [o if o else inv_month.get(a, "") for o, a in zip(tr.own, tr.applies_to_invoice)]
    tr["mi"] = tr.quantity.astype(float) / np.where(tr.uom == "LF", 5280.0, 1.0)
    tr = tr[tr.m.str.startswith("2025")].copy()
    tr["q"] = "Q" + ((tr.m.str[5:].astype(int) + 2) // 3).astype(str)
    g = tr.groupby(["vendor", "q"]).mi.sum()
    for v in (OC, NC):
        for q in ("Q1", "Q2", "Q3", "Q4"):
            eq("billing %s %s" % (v, q), f1(g.get((v, q), 0.0)), fig["billing"]["%s %s" % (v, q)])
    # ask C: the same lines by the district of each work order's trimmed units
    T = read(target, "row_trim_completions_2012-2025.csv")
    unit_d = dict(zip(R.unit_id, R.district))
    wo_d = T.assign(d=T.unit_id.map(unit_d)).groupby("work_order").d.agg(lambda z: z.iloc[0] if z.nunique() == 1 else "?")
    gd = tr.mi.groupby(tr.work_order.map(wo_d)).sum()
    for d in DIST:
        eq("district billing %s" % d, f1(gd.get(d, 0.0)), fig["district_billing"][d])
    # ask B: 2025's major event days by district (unplanned sustained outages, primary and secondary): each ticket's
    # steps split where the members restored go negative (the device off again after restoration, ENG-REL-02 2.1),
    # then an opening of a device already out folded into that outage
    X = read(target, "oms_outage_export_2016-2025.csv")
    X["s"] = pd.to_datetime(X.start_local)
    X["t"] = pd.to_datetime(X.step_restored_local)
    X = X[X.s.dt.normalize().isin(set(md[2025]))]
    X = X.assign(n=X.members_restored.astype(int), k=X.step.astype(int)).sort_values(["ticket_no", "k"])
    ops = []
    for tk, z in X.groupby("ticket_no", sort=False):
        top = z.iloc[0]
        cur = [top.s, int(top.members_out), 0.0, top.s]
        for t, n in zip(z.t, z.n):
            if n < 0:
                ops.append(cur)
                cur = [t, -n, 0.0, t]
            else:
                cur[2] += n * (t - cur[0]).total_seconds() / 60.0
                cur[3] = max(cur[3], t)
        ops.append(cur)
        for o in ops[len(ops) - (z.n < 0).sum() - 1:]:
            o += [top.device_id, top.service_area, top.cause_code]
    B = pd.DataFrame(ops, columns=["s", "mem", "cm", "e", "dev", "d", "cause"]).sort_values(["dev", "s"])
    prior = B.groupby("dev").e.transform(lambda z: z.cummax().shift())
    B = B[~(B.s <= prior)]
    B = B[(B.cause != "PLANNED") & ((B.e - B.s).dt.total_seconds() > 300) & B.s.dt.normalize().isin(set(md[2025]))]
    for d in DIST:
        x = B[B.d == d]
        eq("MED outages %s" % d, "{:,}".format(len(x)), fig["med"][d]["outages"])
        eq("MED members %s" % d, "{:,}".format(int(x.mem.sum())), fig["med"][d]["members"])
        eq("MED customer-minutes %s" % d, "{:,}".format(int(round(x.cm.sum()))), fig["med"][d]["customer_minutes"])
    # the call: North carries the rise, and its 2025 shift on units within two years of a trim is most of it
    rise = {d: rate[2025][d] - np.mean([rate[y][d] for y in (2021, 2022, 2023)]) for d in DIST}
    if max(rise, key=rise.get) != "North":
        bad.append("the rise does not sit in North")
    mi25 = miles_in_year(R, 2025)
    total = sum(rise[d] * mi25[d] for d in DIST)
    share = (young[2025] - np.mean([young[y] for y in (2021, 2022, 2023)])) * mi25["North"] / total
    if share < 0.5:
        bad.append("North's shift is %.2f of the rise" % share)
    if fig["call"] != "hazard-tree removal beyond the right-of-way":
        bad.append("call: %s" % fig["call"])
    if bad:
        raise SystemExit("verify FAILED:\n  " + "\n  ".join(bad))
    print("verify: every stated figure recomputes from the bundle (North's shift %.2f of the rise)" % share)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
