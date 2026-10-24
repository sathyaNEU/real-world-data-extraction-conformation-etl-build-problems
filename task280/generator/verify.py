"""Independent verifier for task280 (pandas, its own code path): recomputes the call, every hub's share and both asks
from target/ and compares them with generator/figures.json."""
from __future__ import annotations

import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd

HUBS = ["BW", "CM", "DF", "EH", "GH", "KB", "LM", "SC"]
W0, W1 = dt.date(2026, 9, 14), dt.date(2026, 11, 13)


def _utc(local, off_hours):
    return local - pd.to_timedelta(off_hours, unit="h")


def call(t):
    hh = pd.read_csv(os.path.join(t, "panel_households.csv"), dtype=str).fillna("")
    hh = hh[(pd.to_datetime(hh.enrolled_on).dt.date < W0) & (hh.withdrawn_on == "")]
    units = pd.read_csv(os.path.join(t, "panel_units.csv"), dtype=str)
    addr = pd.read_csv(os.path.join(t, "tollard_address_node_table.csv"), dtype=str).fillna("")
    reg = pd.read_csv(os.path.join(t, "tollard_node_register.csv"), dtype=str).fillna("")
    hub_of = dict(zip(reg.node_id, reg.hub_code))
    subs = pd.read_csv(os.path.join(t, "tollard_subscription_history.csv"), dtype=str).fillna("")
    plans = pd.read_csv(os.path.join(t, "tollard_plan_catalogue.csv"))
    mbps = dict(zip(plans.plan_code, plans.download_mbps.astype(float)))
    util = pd.read_csv(os.path.join(t, "tollard_node_utilisation_2026q3q4.csv"))
    util["t"] = pd.to_datetime(util.interval_start_utc.str.replace("Z", ""))
    U = {(n, ts): v / 100.0 for n, ts, v in zip(util.node_id, util.t, util.ds_util_pct)}
    tests = pd.read_csv(os.path.join(t, "panel_download_tests_2026_evening.csv"))
    tests = tests.drop_duplicates(["unit_id", "test_start_local", "bytes_received"])
    tests = tests.merge(units[["unit_id", "household_id"]], on="unit_id")
    tests = tests[tests.household_id.isin(hh.household_id)]
    tests["local"] = pd.to_datetime(tests.test_start_local)
    tests["off"] = tests.utc_offset.str[:3].astype(int)
    tests["slot"] = _utc(tests.local, tests.off).dt.floor("15min")
    tests["day"] = tests.local.dt.date
    peak = (tests.local.dt.weekday < 5) & (tests.local.dt.hour >= 19) & (tests.local.dt.hour < 23)
    tests = tests[peak]
    days = [W0 + dt.timedelta(days=i) for i in range((W1 - W0).days + 1) if (W0 + dt.timedelta(days=i)).weekday() < 5]
    out = {}
    for _, H in hh.iterrows():
        a = addr[addr.service_address_id == "SA-%07d" % int(H.service_address)]
        s = subs[subs.account_number == H.tollard_account]

        def node_on(d):
            for _, r in a.iterrows():
                if pd.Timestamp(r.effective_from).date() <= d and (r.effective_to == "" or
                                                                  d <= pd.Timestamp(r.effective_to).date()):
                    return r.node_id

        def plan_on(d):
            for _, r in s.iterrows():
                if pd.Timestamp(r.effective_from).date() <= d and (r.effective_to == "" or
                                                                  d <= pd.Timestamp(r.effective_to).date()):
                    return r.plan_code
        nodes = {d: node_on(d) for d in days}
        plan = {d: plan_on(d) for d in days}
        T = tests[tests.household_id == H.household_id]
        loads = np.array([U[(nodes[d], s0)] for d, s0 in zip(T.day, T.slot)])
        down = np.array([mbps[plan[d]] for d in T.day])
        below = (T.throughput_kbps.values / 1000.0) < 0.8 * down
        hits, total = 0, 0
        for p in sorted(set(plan.values())):
            q = []
            for d in days:
                if plan[d] != p:
                    continue
                off = 4 if d < dt.date(2026, 11, 1) else 5
                for k in range(16):
                    ts = pd.Timestamp(dt.datetime.combine(d, dt.time(19)) + dt.timedelta(minutes=15 * k + 60 * off))
                    q.append(U[(nodes[d], ts)])
            q = np.array(q)
            total += len(q)
            sel = down == mbps[p]
            if not sel.any():
                continue
            l, b = loads[sel], below[sel]
            o = np.argsort(l, kind="stable")
            l, b = l[o], b[o]
            best, cut = -1, None
            for j in range(len(l) + 1):
                sc = int((~b[:j]).sum() + b[j:].sum())
                if sc > best:
                    best, cut = sc, j
            thr = (l[cut - 1] + l[cut]) / 2 if 0 < cut < len(l) else (-1.0 if cut == 0 else 2.0)
            hits += int((q > thr).sum())
        out[H.household_id] = (hub_of[nodes[days[0]]], hits / total)
    share = {h: 100 * np.mean([v for hb, v in out.values() if hb == h]) for h in HUBS}
    return share


def credits(t):
    xl = pd.read_excel(os.path.join(t, "tollard_node_subscriber_counts_2026.xlsx"), sheet_name=0)
    reg = pd.read_csv(os.path.join(t, "tollard_node_register.csv"), dtype=str).fillna("")
    hub_of = dict(zip(reg.node_id, reg.hub_code))
    cnt = {}
    for c in xl.columns[2:]:
        me = dt.date.fromisoformat(c.split("_")[1])
        for n, v in zip(xl.node_id, xl[c]):
            if not pd.isna(v):
                cnt[(n, me)] = int(v)
    o = pd.read_csv(os.path.join(t, "tollard_outage_reports_2026.csv"))
    o = o[o.work_type == "Unplanned"]
    o["s"] = pd.to_datetime(o.outage_start_utc)
    o["e"] = pd.to_datetime(o.service_restored_utc)
    res = {h: 0 for h in HUBS}
    for n, g in o.groupby("node_id"):
        iv = sorted(zip(g.s, g.e))
        merged = [list(iv[0])]
        for s, e in iv[1:]:
            if s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        for s, e in merged:
            local = s - pd.Timedelta(hours=4 if s < pd.Timestamp("2026-11-01 06:00") else 5)
            d = local.date()
            if not (W0 <= d <= W1):
                continue
            hrs = (e - s).total_seconds() / 3600
            if hrs < 4:
                continue
            me = dt.date(d.year, d.month, 1) - dt.timedelta(days=1)
            res[hub_of[n]] += math.ceil(hrs / 24 - 1e-12) * cnt[(n, me)]
    return res


def capacity_added(t):
    reg = pd.read_csv(os.path.join(t, "tollard_node_register.csv"), dtype=str).fillna("")
    xl = pd.read_excel(os.path.join(t, "tollard_node_subscriber_counts_2026.xlsx"), sheet_name=0)
    counted = set(xl.node_id[xl.iloc[:, 2:].notna().any(axis=1)])
    drop = set()
    for parent, g in reg[reg.split_from != ""].groupby("split_from"):
        starts = sorted(set(g.in_service_from))
        if len(starts) == 2:
            later = g[g.in_service_from == starts[1]]
            if not later.node_id.isin(counted).any():
                drop |= set(later.node_id)
    reg = reg[~reg.node_id.isin(drop)]

    def cap(d):
        live = reg[(pd.to_datetime(reg.in_service_from).dt.date <= d) &
                   ((reg.in_service_to == "") | (pd.to_datetime(reg.in_service_to.replace("", None)).dt.date >= d))]
        return live.groupby("hub_code").ds_capacity_mbps.apply(lambda s: s.astype(int).sum()).to_dict()
    a, b = cap(W0), cap(W1)
    return {h: int(b.get(h, 0) - a.get(h, 0)) for h in HUBS}


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    share = call(t)
    bad = 0
    des = [h for h in HUBS if share[h] > 20.0]
    print("verify: designated", des, "figures", fig["call"]["designated"])
    bad += des != fig["call"]["designated"]
    for h in HUBS:
        v = int(math.floor(share[h] + 0.5))
        if v != fig["hubs"][h]["share"]:
            print("  share differs", h, share[h], fig["hubs"][h]["share"])
            bad += 1
    cr = credits(t)
    for h in HUBS:
        if cr[h] != fig["hubs"][h]["outage_credit_subscriber_days"]:
            print("  credits differ", h, cr[h], fig["hubs"][h]["outage_credit_subscriber_days"])
            bad += 1
    ca = capacity_added(t)
    for h in HUBS:
        if ca[h] != fig["hubs"][h]["capacity_added_mbps"]:
            print("  capacity added differs", h, ca[h], fig["hubs"][h]["capacity_added_mbps"])
            bad += 1
    print("verify: %s (%d figures compared, %d differ)" % ("PASS" if not bad else "FAIL", 1 + 3 * len(HUBS), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    raise SystemExit(run(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if len(sys.argv) < 2
                         else sys.argv[1]))
