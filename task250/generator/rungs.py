"""The competent wrong routes, each run on the cut pack: the main call's rungs (the plan's hub, the share imputation,
the complete-case cut, the excess over the base rate) and the asks' stops (exact, near-exact, same-day and fixed-shift
duplicates; the pickup anti-joins). Used by checks.py for the ladder and by ceiling.py for the cracker and mirror."""
import collections
import datetime as dt

import pandas as pd

import golden as GD


# ------------------------------------------------------------------ the main call
def plan_lookup(plan, revised=True):
    rows = []
    for r in plan.itertuples():
        if not revised and r.plan_issue != "Q4-1":
            continue
        rows.append((r.delivery_depot, str(r.first_sort_night), str(r.last_sort_night) if revised else "2026-12-31",
                     r.sort_hub))
    return rows


def plan_hub(rows, depot, night):
    for d, a, b, h in rows:
        if d == depot and a <= night <= b:
            return h
    raise KeyError((depot, night))


def assign_plan(arr, sh, plan, revised=True):
    rows = plan_lookup(plan, revised)
    out = {}
    for t, d, ts in zip(arr["tracking_no"], arr["depot_code"], arr["scanned_at"]):
        if t in sh:
            out[t] = sh[t]
        else:
            night = (dt.date.fromisoformat(ts[:10]) - dt.timedelta(days=1)).isoformat()
            out[t] = plan_hub(rows, d, night)
    return out


def rates_fractional(arr, sh, weights):
    """rates when each unscanned parcel is split across hubs by weights {tracking: {hub: w}}"""
    n, m = collections.Counter(), collections.Counter()
    for t in arr["tracking_no"]:
        if t in sh:
            n[sh[t]] += 1
        else:
            for h, w in weights[t].items():
                n[h] += w
                m[h] += w
    return {h: {"parcels": n[h], "missed": m[h], "rate": 100.0 * m[h] / n[h]} for h in n}


def share_weights(arr, sh, grain=("depot_code", "day")):
    a = arr.copy()
    a["day"] = a["scanned_at"].str[:10]
    a["hub"] = a["tracking_no"].map(sh)
    sc = a[a["hub"].notna()].groupby(list(grain))["hub"].value_counts(normalize=True)
    share = collections.defaultdict(dict)
    for k, v in sc.items():
        share[k[:-1]][k[-1]] = v
    w = {}
    for r in a[a["hub"].isna()].itertuples():
        w[r.tracking_no] = share[tuple(getattr(r, g) for g in grain)]
    return w


def mixed_days(arr, sh):
    a = arr.copy()
    a["day"] = a["scanned_at"].str[:10]
    a["hub"] = a["tracking_no"].map(sh)
    k = a[a["hub"].notna()].groupby(["depot_code", "day"])["hub"].nunique()
    return set(k[k > 1].index)


def complete_case(arr, sh, plan):
    """the depot-mornings whose sorted parcels came from two hubs left out, the rest on the plan"""
    mx = mixed_days(arr, sh)
    a = arr[[(d, ts[:10]) not in mx for d, ts in zip(arr["depot_code"], arr["scanned_at"])]]
    return GD.hub_rates(assign_plan(a, sh, plan), a, sh)


def excess(arr, sh, plan):
    """the mixed mornings' unscanned parcels above the plan hub's rate on its other mornings, charged to the second
    hub on those mornings"""
    mx = mixed_days(arr, sh)
    base = assign_plan(arr, sh, plan)
    r = GD.hub_rates(base, arr, sh)
    a = arr.copy()
    a["day"] = a["scanned_at"].str[:10]
    a["mixed"] = [(d, x) in mx for d, x in zip(a["depot_code"], a["day"])]
    a["plan"] = a["tracking_no"].map(base)
    a["scanned"] = a["tracking_no"].isin(sh.keys())
    out = {h: dict(v) for h, v in r.items()}
    for (d, x), g in a[a["mixed"]].groupby(["depot_code", "day"]):
        hubs = collections.Counter(sh[t] for t in g["tracking_no"] if t in sh)
        home = max(hubs, key=lambda h: (hubs[h], h))
        other = [h for h in hubs if h != home][0]
        rest = a[(~a["mixed"]) & (a["plan"] == home)]
        br = (~rest["scanned"]).mean()
        home_scanned = hubs[home]
        unscanned = int((~g["scanned"]).sum())
        exp_home = br * home_scanned / (1 - br)
        moved = max(0.0, unscanned - exp_home)
        out[home]["parcels"] -= moved
        out[home]["missed"] -= moved
        out[other]["parcels"] += moved
        out[other]["missed"] += moved
    for h in out:
        out[h]["rate"] = 100.0 * out[h]["missed"] / out[h]["parcels"]
    return out


def alerts(r, tol=GD.TOLERANCE):
    return sorted(h for h, v in r.items() if v["rate"] > tol)


def main_rungs(d):
    arr = GD.arrivals(d["depot"])
    sh = GD.sort_hub(d["hub"])
    gold, _, _, _ = GD.golden_assign(arr, sh)
    out = {
        "golden": GD.hub_rates(gold, arr, sh),
        "R0 plan": GD.hub_rates(assign_plan(arr, sh, d["plan"]), arr, sh),
        "R0 plan, first issue": GD.hub_rates(assign_plan(arr, sh, d["plan"], revised=False), arr, sh),
        "R1 shares by depot-morning": rates_fractional(arr, sh, share_weights(arr, sh)),
        "R1 shares by hub of the depot's month": rates_fractional(arr, sh, share_weights(arr, sh, ("depot_code",))),
        "R2 mixed mornings left out": complete_case(arr, sh, d["plan"]),
        "R3 excess over the base rate": excess(arr, sh, d["plan"]),
    }
    return out, arr, sh, gold


# ------------------------------------------------------------------ ask A: courier events sent twice
def a_exact(cou):
    k = ["tracking_no", "depot_code", "courier_id", "device_id", "event_code", "event_time", "customer_ref"]
    c = cou.copy()
    c["customer_ref"] = c["customer_ref"].fillna("")
    return c[c.duplicated(k)].groupby("depot_code").size().to_dict()


def a_near_exact(cou):
    """same parcel, event, courier and handheld in the same minute (the battery's near-exact duplicate)"""
    c = cou.copy()
    c["m"] = c["event_time"].str[:16]
    c = c.sort_values("received_at_utc")
    return c[c.duplicated(["tracking_no", "event_code", "courier_id", "device_id", "m"])].groupby("depot_code").size().to_dict()


def a_same_day(cou, with_device=True):
    c = cou.copy()
    c["day"] = c["event_time"].str[:10]
    k = ["tracking_no", "event_code", "day"] + (["courier_id", "device_id"] if with_device else [])
    c = c.sort_values("received_at_utc")
    return c[c.duplicated(k)].groupby("depot_code").size().to_dict()


def a_window(cou, minutes):
    """same parcel, event and handheld within a window either side"""
    c = cou.copy()
    c["t"] = pd.to_datetime(c["event_time"])
    c = c.sort_values(["tracking_no", "event_code", "device_id", "received_at_utc"])
    out = collections.Counter()
    for _, g in c[c.duplicated(["tracking_no", "event_code", "device_id"], keep=False)].groupby(
            ["tracking_no", "event_code", "device_id"]):
        ts = list(g["t"])
        dep = list(g["depot_code"])
        for j in range(1, len(ts)):
            if any(abs((ts[j] - ts[i]).total_seconds()) <= minutes * 60 for i in range(j)):
                out[dep[j]] += 1
    return dict(out)


def a_fixed_shift(cou, handhelds, hours=2):
    """the TC51 re-sends found with one shift for the month (the summer offset), the rest near-exact"""
    model = dict(zip(handhelds["device_id"], handhelds["model"]))
    c = cou.copy()
    c["model"] = c["device_id"].map(model)
    c["m"] = c["event_time"].str[:16]
    c["shift"] = (pd.to_datetime(c["event_time"]) - pd.Timedelta(hours=hours)).dt.strftime("%Y-%m-%d %H:%M")
    key = ["tracking_no", "event_code", "courier_id", "device_id"]
    out = collections.Counter()
    for _, g in c[c.duplicated(key, keep=False)].sort_values("received_at_utc").groupby(key):
        rows = g.to_dict("records")
        for j in range(1, len(rows)):
            b = rows[j]
            if b["event_time"][17:19] != "00":
                continue
            if any(a["m"] == b["m"] or (b["model"] == "TC51" and a["shift"] == b["m"]) for a in rows[:j]):
                out[b["depot_code"]] += 1
    return dict(out)


# ------------------------------------------------------------------ ask B: pre-advised, never picked up
def b_route(d, versions=True, window=True, remap=True, events=("PICKED_UP",), pieces=True, prefix=True,
            cardinality=True, downstream=False):
    pre = d["pre"].copy()
    if versions:
        pre["v"] = pre["version"].astype(int)
        pre = pre.sort_values(["consignment_id", "v"]).groupby("consignment_id").tail(1)
    if window:
        pre = pre[(pre["collection_date"] >= GD.MONTH[0]) & (pre["collection_date"] <= GD.MONTH[1])]
    pre = pre.copy()
    if remap:
        rep = GD.replaced_codes(d["depots"])
        pre["depot"] = [rep[c][0] if c in rep and x >= rep[c][1] else c
                        for c, x in zip(pre["collection_depot"], pre["collection_date"])]
    else:
        pre["depot"] = pre["collection_depot"]
    pre["pieces"] = pre["pieces"].astype(int)
    cou = d["courier"]
    ev = cou if events is None else cou[cou["event_code"].isin(events)]
    seen = set(ev["tracking_no"])
    if downstream:
        seen |= set(cou["tracking_no"]) | set(d["hub"]["tracking_no"]) | set(d["depot"]["tracking_no"])
    lab = collections.Counter()
    if prefix:
        for t in seen:
            if len(t) == 16 and t.isdigit():
                lab[t[:13]] += 1
    out = collections.Counter()
    for r in pre[pre["tracking_no"] != ""].itertuples():
        got = (1 if r.tracking_no in seen else 0) + lab.get(r.tracking_no, 0)
        if pieces:
            out[r.depot] += max(0, r.pieces - got)
        else:
            out[r.depot] += 0 if got else r.pieces
    pu = cou[(cou["event_code"] == "PICKED_UP") & cou["customer_ref"].notna()]
    mk = pre[pre["tracking_no"] == ""].copy()
    if prefix:
        mk["key"] = mk["customer_ref"].str[:20]
        if cardinality:
            picked = pu.groupby("customer_ref")["tracking_no"].nunique().to_dict()
            for (key, dep), g in mk.groupby(["key", "depot"]):
                out[dep] += max(0, int(g["pieces"].sum()) - picked.get(key, 0))
        else:
            have = set(pu["customer_ref"])
            for r in mk.itertuples():
                out[r.depot] += 0 if r.key in have else r.pieces
    else:
        have = set(pu["customer_ref"])
        for r in mk.itertuples():
            out[r.depot] += 0 if r.customer_ref in have else r.pieces
    return dict(out)


def ask_rungs(d):
    cou, hh = d["courier"], d["handhelds"]
    gold_a = GD.sent_twice(cou, hh).groupby("depot_code").size().to_dict()
    gold_b, _ = GD.never_picked(d["pre"], d["depots"], cou, d["hub"], d["depot"])
    A = {"golden": gold_a,
         "A0 exact duplicates": a_exact(cou),
         "A1 near-exact, same minute": a_near_exact(cou),
         "A2 same parcel, event, handheld and day": a_same_day(cou),
         "A2b same parcel, event and day": a_same_day(cou, with_device=False),
         "A3 within 5 minutes": a_window(cou, 5),
         "A3b within 3 hours": a_window(cou, 180),
         "A4 TC51 at a fixed two hours": a_fixed_shift(cou, hh, 2)}
    B = {"golden": gold_b,
         "B0 every line, exact keys": b_route(d, versions=False, window=False, remap=False, pieces=False, prefix=False),
         "B1 latest versions, exact keys": b_route(d, pieces=False, prefix=False),
         "B2 piece labels and reference prefixes, any match": b_route(d, pieces=False, cardinality=False),
         "B3 pieces and references counted, pickups only": b_route(d),
         "B4 every courier event, pieces and references counted": b_route(d, events=None),
         "B4b every courier event but a failed pickup": b_route(
             d, events=("PICKED_UP", "OUT_FOR_DELIVERY", "DELIVERY_ATTEMPTED", "DELIVERED")),
         "B4c delivery evidence, consignments any match": b_route(
             d, events=("PICKED_UP", "OUT_FOR_DELIVERY", "DELIVERY_ATTEMPTED", "DELIVERED"), pieces=False,
             cardinality=False),
         "B5 the cracker without the replaced code": b_route(d, remap=False),
         "B6 the cracker on every version": b_route(d, versions=False)}
    return A, B
