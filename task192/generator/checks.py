"""Assertions on the cut pack, the goldens and the clean truth. Exit 1 on any failure."""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl
from pypdf import PdfReader

import build
import golden as G
import pack as PK
import sim
import truth
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), str(detail)[:300]))


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def ranked(L, k):
    return sorted(L, key=lambda f: -L[f][k])


def groups(recs, band, days=True, use_ig=False):
    if use_ig:
        recs = [dict(r, current=r["ig"]) if (r.get("ig") is not None and len(r["phases"]) == 1) else r for r in recs]
    best = G.largest_group(recs, band=band, days=days)
    return {f: v[0] for f, v in best.items()}


def const_step(xs):
    d = {b - a for a, b in zip(xs, xs[1:])}
    return len(d) == 1


def main():
    res = G.compute(T)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    net = res["net"]
    files = []
    for root, _, fs in os.walk(T):
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), T))
    files.sort()

    # ------------------------------------------------------------------ input gates
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    big = {f: sum(1 for _ in open(os.path.join(T, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a file of 25,000 or more rows", max(big.values()) >= 25000, max(big.items(), key=lambda kv: kv[1]))
    ok("gate: two or more distractors declared", len(md["distractor_files"]) >= 2, md["distractor_files"])
    ok("gate: every declared distractor ships", all(os.path.exists(os.path.join(TASK, p)) for p in md["distractor_files"]))
    ok("gate: no distractor named as one", not [f for f in files if re.search(r"distract|decoy|noise", f, re.I)])
    bad = [f for f in files if re.search(r"readme|dictionar|manifest|notes|schema|field.?guide|about", f, re.I)]
    ok("gate: no file describes the pack by name", not bad, bad)
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(T, f), read_only=True)
            sheets += wb.sheetnames
            wb.close()
    ok("gate: no sheet describes the pack", not [s for s in sheets if re.search(r"readme|dictionar|notes|about|how to|legend",
                                                                                 s, re.I)], sheets)
    ok("gate: provenance for every file", all(("target/" + f) in md["files"] for f in files))
    ok("gate: metadata names no method", not re.search(r"current|phase|group|repeat|cluster", json.dumps(md["decision"]), re.I))

    # ------------------------------------------------------------------ the call
    ok("call: MLR-2 from the pack", res["call"] == "MLR-2", res["call"])
    ok("call: runner-up SYC-3 from the pack", res["runner_up"] == "SYC-3", res["runner_up"])
    sc, sr = res["sep"]["MLR-2"], res["sep"]["SYC-3"]
    ok("call: eleven momentary faults on phase C recorded by the MLR-2 breaker", sc["n"] == 11 and sc["phase"] == "C"
       and sc["device"] == "MLR-F2-52", sc)
    ok("call: seven on phase A recorded by recloser R-3114", sr["n"] == 7 and sr["phase"] == "A" and sr["device"] == "R-3114", sr)
    others = max(v[0] for f, v in res["best"].items() if f not in ("MLR-2", "SYC-3"))
    ok("call: no other feeder above five at one phase and one current since 1 August", others <= 5, others)
    ok("call: final margin 11 to 7, 1.57x", sc["n"] / sr["n"] >= 1.5, sc["n"] / sr["n"])
    ok("call: the stretch is the breaker's zone to R-2207 at MLR2-P071", sc["zone_to"] == [("R-2207", "MLR2-P071")],
       sc["zone_to"])
    ok("call: figures.json carries the call", F["call"] == "MLR-2" and F["runner_up"] == "SYC-3")

    recs = res["recs"]
    win_all = [e for e in res["ev"] if W.WIN0 <= e["day"] <= W.WIN1]
    recs_trip = G.fault_records(T, net, win_all)
    yr = [e for e in res["ev"] if W.REP0 <= e["day"] <= W.REP1]
    recs_yr = G.fault_records(T, net, yr)
    so = [e for e in res["ev"] if dt.date(2026, 9, 1) <= e["day"] <= W.WIN1]
    recs_so = G.fault_records(T, net, so)
    sf10 = []
    for band in (1.02, 1.03, 1.04, 1.06, 1.08, 1.10):
        for days in (True, False):
            for ig in (False, True):
                for name, rr in (("aug-oct", recs), ("jan-oct", recs_yr), ("sep-oct", recs_so)):
                    g = groups(rr, band, days, ig)
                    top = max(g, key=lambda f: g[f])
                    sf10.append((band, days, ig, name, top, g["MLR-2"], g.get("SYC-3", 0),
                                 max(v for f, v in g.items() if f not in ("MLR-2", "SYC-3"))))
    ok("SF10 every licensed grouping names MLR-2", all(x[4] == "MLR-2" for x in sf10),
       [x for x in sf10 if x[4] != "MLR-2"][:4])
    a1 = [x for x in sf10 if x[3] == "aug-oct" and x[0] >= 1.03]
    ok("SF10 since 1 August, every band from 1.5 to 5 per cent: MLR-2 by 1.3x or more",
       all(x[5] >= 1.3 * max(x[6], x[7]) for x in a1), [x for x in a1 if x[5] < 1.3 * max(x[6], x[7])][:4])
    a2 = [x for x in sf10 if x[3] == "jan-oct" and x[0] <= 1.06]
    ok("SF10 over the whole of 2026, every band to 3 per cent: MLR-2 by 1.3x or more",
       all(x[5] >= 1.3 * max(x[6], x[7]) for x in a2), [x for x in a2 if x[5] < 1.3 * max(x[6], x[7])][:4])
    a3 = [x for x in sf10 if x[3] == "sep-oct"]
    ok("SF10 September and October alone, every band: MLR-2 first", all(x[5] > max(x[6], x[7]) for x in a3),
       [x for x in a3 if x[5] <= max(x[6], x[7])][:4])
    sf11 = [x for x in sf10 if x[0] <= 1.06 and x[3] == "aug-oct"]
    ok("SF11 SYC-3 is second under every grouping to a three per cent band", all(x[6] > x[7] for x in sf11),
       [x for x in sf11 if x[6] <= x[7]][:4])
    ok("SF11 SYC-3 is second over the whole year at a two per cent band, separate days",
       all(x[6] > x[7] for x in sf10 if x[3] == "jan-oct" and x[0] <= 1.04 and x[1]))
    ok("SF12 MLR-2 leads SYC-3 on every patrol criterion: count, customers behind, onset, latest",
       sc["n"] > sr["n"] and sc["behind"] > sr["behind"] and sc["first"] < sr["first"] and sc["last"] >= sr["last"],
       (sc["n"], sr["n"], sc["behind"], sr["behind"], sc["first"], sr["first"], sc["last"], sr["last"]))
    ok("SF13 the patrol stretch is the recording device's zone (DRP-04 5.4)",
       F["stretch"]["device"] == "MLR-F2-52" and F["stretch"]["to"] == ["R-2207"])
    # the group's records: one device, on separate mornings, each cleared on the first reclose
    g = sorted((r for r in recs if r["feeder"] == "MLR-2" and r["phases"] == "C" and 1400 <= r["current"] <= 1480),
               key=lambda r: r["t"])
    ok("call: the eleven are single operations on separate days at dawn", len(g) == 11 and all(r["ops"] == 1 for r in g)
       and len({r["day"] for r in g}) == 11 and all(5 <= G.local(r["t"]).hour <= 7 for r in g), [(r["day"], r["ops"]) for r in g])
    damp = G.damp_days(T)
    ok("call: every one on a damp morning at the airport (RH 97 per cent or more)", all(r["day"] in damp for r in g))
    # the available fault current places the eleven between two devices on the main line inside the zone
    afc = []
    for d, rows in net.rows.items():
        r = net.row(d, W.REP1)
        if r and r["feeder"] == "MLR-2" and r["type"] in ("FUSE", "RECLOSER"):
            pass
    with open(os.path.join(T, PK.FILES["devices"])) as fh:
        for r in csv.DictReader(fh):
            if r["feeder"] == "MLR-2" and r["device_type"] in ("FUSE", "RECLOSER"):
                afc.append((int(r["pole"].split("-P")[1]), int(r["available_fault_slg_a"])))
    afc.sort()
    lo_side = [a for p, a in afc if a >= sc["hi"]]
    hi_side = [a for p, a in afc if a <= sc["lo"]]
    ok("call: the register's available fault currents fall along the feeder and bracket the eleven",
       all(b <= a for (_, a), (_, b) in zip(afc, afc[1:])) and lo_side and hi_side, afc[:6])

    # ------------------------------------------------------------------ the ladder and the stump
    L = G.ladder(T, res)
    ok("R0 raw momentary events Aug-Oct 2026 name another feeder, MLR-2 fifth or lower",
       ranked(L, "raw")[0] != "MLR-2" and ranked(L, "raw").index("MLR-2") + 1 >= 5,
       [(f, L[f]["raw"]) for f in ranked(L, "raw")[:3]])
    ok("R0b change on 2025 names NYD-3, MLR-2 not in the top five", ranked(L, "chg")[0] == "NYD-3"
       and ranked(L, "chg").index("MLR-2") >= 5)
    ok("R1 non-storm events name NYD-3", ranked(L, "ns")[0] == "NYD-3" and L["NYD-3"]["ns"] >= 1.5 * L["MLR-2"]["ns"])
    ok("R2 non-storm events per overhead mile name NYD-3", ranked(L, "nsmi")[0] == "NYD-3")
    ok("R3 the default path (non-storm per overhead mile against 2025) names NYD-3 at 2.5 a mile",
       ranked(L, "dflt")[0] == "NYD-3" and L["NYD-3"]["dflt"] >= 1.5 * L[ranked(L, "dflt")[1]]["dflt"],
       [(f, round(L[f]["dflt"], 2)) for f in ranked(L, "dflt")[:3]])
    ok("R3 the default path per thousand customers names NYD-3", ranked(L, "per_cust")[0] == "NYD-3")
    ok("R4 damp-morning non-storm events name NYD-2", ranked(L, "damp")[0] == "NYD-2"
       and L["NYD-2"]["damp"] >= 1.5 * L["MLR-2"]["damp"])
    ok("R5 phase skew (chi-square, share) names BLV-3", ranked(L, "chi")[0] == "BLV-3" and ranked(L, "share")[0] == "BLV-3"
       and L["BLV-3"]["share"] >= 1.2 * L["MLR-2"]["share"] and L["BLV-3"]["chi"] >= 1.3 * L["MLR-2"]["chi"])
    for k in ("raw", "chg", "ns", "nsmi", "dflt", "damp", "chi", "share", "per_cust", "nsd"):
        order = ranked(L, k)
        ok("position: MLR-2 never first and never second within 1.2x on %s" % k,
           order[0] != "MLR-2" and not (order[1] == "MLR-2" and L["MLR-2"][k] * 1.2 > L[order[0]][k]), order[:3])
    # the worst-performing-circuit reflex: the asks' own indices, over the year and over the weeks since August
    ix = {f: res["idx"][f] for f in res["idx"]}
    mom3 = collections.Counter()
    for e in res["ev"]:
        if W.WIN0 <= e["day"] <= W.WIN1:
            mom3[e["feeder"]] += e["n"]
    for key, val in (("SAIDI", lambda f: ix[f]["saidi"]), ("MAIFI-E", lambda f: ix[f]["maifi"]),
                     ("CEMI-2", lambda f: ix[f]["cemi"]), ("CEMI-2 share", lambda f: ix[f]["cemi"] / ix[f]["nt"]),
                     ("MAIFI-E since August", lambda f: mom3[f] / ix[f]["nt"])):
        order = sorted(ix, key=lambda f: -val(f))
        ok("position: the %s ranking does not single out MLR-2" % key,
           order[0] != "MLR-2" and not (order[1] == "MLR-2" and val("MLR-2") * 1.2 > val(order[0])),
           [(f, round(val(f), 2)) for f in order[:3]])
    ok("dominance: the decisive group outruns the default path's carried edge",
       (sc["n"] - sr["n"]) / sr["n"] >= 1.2 * 0 and sc["n"] >= 1.5 * others)
    ok("figures.json carries the ladder", F["ladder"]["NYD-3"]["dflt"] == round(L["NYD-3"]["dflt"], 4))

    # ------------------------------------------------------------------ the asks: golden from the pack = clean truth
    net0, wx, stk, S, TR, added = build.world()
    per = collections.Counter()
    for sp, k in TR["per_sp"].items():
        if k > truth.CEMI_N and truth.active(net0["sps"][sp], W.REP1):
            per[truth.sp_feeder(net0, sp, W.REP1)] += 1
    diffs = []
    for f in W.FID:
        t_, g_ = TR["idx"][f], res["idx"][f]
        if not (t_["nt"] == g_["nt"] and abs(t_["saidi"] - g_["saidi"]) < 1e-6 and abs(t_["maifi"] - g_["maifi"]) < 1e-9
                and per[f] == g_["cemi"]):
            diffs.append(f)
    ok("asks: SAIDI, MAIFI-E, CEMI-2 and customers served from the pack equal the clean truth", not diffs, diffs)
    ok("asks: major event days from the pack equal the clean truth", res["meds"] == TR["meds"] ==
       [dt.date(2026, 5, 19), dt.date(2026, 6, 27)], res["meds"])
    ok("asks: the filed threshold and denominator are the generator's", abs(res["tmed"] - W.T_MED_2026) < 1e-9
       and res["nsys"] == TR["n_sys"])
    nonmed = sorted((v, d) for d, v in res["daily"].items() if d.year == 2026 and d not in set(res["meds"]))
    ok("SF2 every other 2026 day sits under 0.6 of the threshold", nonmed[-1][0] < 0.6 * res["tmed"], nonmed[-1])
    ok("SF2 the major event days sit over twice the threshold", min(res["daily"][d] for d in res["meds"]) > 2 * res["tmed"])
    ok("asks: workbook figures equal figures.json", wb_matches(F))
    edges = []
    for f, v in F["feeders"].items():
        if edge(v["saidi_raw"], 0.1) < 0.01 or edge(v["maifi_raw"], 0.01) < 0.001:
            edges.append(f)
    ok("SF9 every graded figure clears its rounding edge by a tenth of a unit", not edges, edges)
    ok("asks: CEMI-2 is zero on at most two feeders (the blind nil response keeps under a quarter)",
       sum(1 for v in F["feeders"].values() if v["cemi"] == 0) <= 2)
    ok("asks: no two feeders share a customers-served count", len({v["nt"] for v in F["feeders"].values()}) == 16)

    # the conventions each ask turns on
    items = res["items"]
    leg = [o for o in items if o["src"] == "legacy"]
    inc = [o for o in items if o["src"] == "incident"]
    oms_cnt = [o for o in leg + inc if o["oms_customers"] != len(o["reach"])]
    ok("SF1 the connectivity reproduces every OMS customer count at the ticket's date", not oms_cnt,
       [(o["id"], o["oms_customers"], len(o["reach"])) for o in oms_cnt[:5]])
    end_ok = all(net.feeder(sp, W.REP1) == v["feeder"] for sp, v in net.sp.items() if net.active(sp, W.REP1))
    ok("SF1 customers served by the extract's feeder column equal those by the register's tree", end_ok)
    tcs = [o for o in items if o["src"] == "scada"]
    medset = set(res["meds"])
    tcs_w = [o for o in tcs if W.REP0 <= o["day"] <= W.REP1 and o["day"] not in medset]
    ok("SF15 sustained openings with no ticket sit open between 5.7 and 13.6 minutes from the lockout",
       all(5.6 * 60000 < o["restore"] - o["lockout_open"] < 13.7 * 60000 for o in tcs),
       [(o["id"], o["restore"] - o["lockout_open"]) for o in tcs if not 5.6 * 60000 < o["restore"] - o["lockout_open"] < 13.7 * 60000][:4])
    ok("SF15 they reach four feeders in the window", len({o["feeder"] for o in tcs_w}) >= 4, sorted({o["feeder"] for o in tcs_w}))
    gaps = []
    for dev, seq in res["soe"].items():
        for a, b in G.open_intervals(seq):
            if 4.5 * 60000 <= b - a <= 5.6 * 60000:
                gaps.append((dev, a))
    ok("SF4 no SCADA opening lasts between 4.5 and 5.6 minutes", not gaps, gaps[:3])
    stepped = [o for o in items if o["steps"]]
    ok("SF5 every stepped restoration reached all its customers (nothing nested in it)",
       all(len(o["hit"]) == o["oms_customers"] for o in stepped))
    leg_steps = [o for o in stepped if o["src"] == "legacy" and W.REP0 <= o["day"] <= W.REP1]
    ok("SF18 stepped legacy tickets in 2026 on four or more feeders", len({o["feeder"] for o in leg_steps}) >= 4,
       sorted({o["feeder"] for o in leg_steps}))
    nest = [o for o in items if o["continues"] is None and len(o["hit"]) < len(o["reach"])]
    ok("SF16 customers already without supply are left out of a later outage's count, the OMS counting them in",
       nest and all(o["oms_customers"] in (None, len(o["reach"])) for o in nest), len(nest))
    cont = [o for o in items if o["continues"] is not None]
    ok("SF14 continuation tickets begin at the minute the device above closed, on ten or more feeders",
       len({o["feeder"] for o in cont if W.REP0 <= o["day"] <= W.REP1 and o["day"] not in medset}) >= 10,
       len(cont))
    ok("SF3 a continuation belongs to the day its outage began", all(o["day"] == G.lday(o["began"]) for o in cont))
    absb = [e for e in res["ev"] if e["n_abs"]]
    ok("SF17 momentary events absorbed by a sustained interruption on twelve or more feeders",
       len({e["feeder"] for e in absb if W.REP0 <= e["day"] <= W.REP1}) >= 12)
    amb = []
    starts = sorted((o["start"], o["id"]) for o in items)
    for e in res["ev"]:
        em = G.floor_min(e["t"])
        for o in items:
            if em - 3 * 60000 <= o["start"] < em and (o["reach"] & net.customers(e["device"], e["day"])):
                if not (o["start"] < em and e["t"] < o["restore"]):
                    amb.append((e["device"], e["t"]))
    ok("SF17 no sustained interruption begins in the minutes just before a momentary event", not amb, amb[:3])
    # SF17: absorption is read at the outage system's minute; a sustained start after an event's minute and inside
    # its five minutes comes only from a later fault inside a multi-fault event, which leaves the first momentary
    late_abs, odd = [], []
    for e in res["ev"]:
        if not (W.REP0 <= e["day"] <= W.REP1) or e["day"] in medset:
            continue
        em = G.floor_min(e["t"])
        reach = net.customers(e["device"], e["day"])
        for o in items:
            if em + 60000 <= o["start"] <= e["t"] + 5 * 60000 and reach & o["dark"]:
                late_abs.append((e["feeder"], str(e["day"]), o["id"]))
                if not (e["end"] - e["t"] > 60000 and o["start"] <= G.floor_min(e["end"])):
                    odd.append((e["feeder"], str(e["day"]), o["id"]))
    ok("SF17 a sustained start after an event's minute and inside its five minutes falls in a later fault's "
       "operations of a multi-fault event (the event's first momentary stands)", not odd and len(late_abs) <= 2,
       (late_abs, odd))
    blown = []
    for e in res["ev"]:
        reach = net.customers(e["device"], e["day"])
        for o in items:
            if (o["dtype"] in ("FUSE", "TRANSFORMER") and G.floor_min(e["t"]) <= o["start"] <= e["t"] + 20000
                    and reach & o["dark"] and o["start"] != G.floor_min(e["t"])):
                blown.append((e["feeder"], str(e["day"]), o["id"]))
    ok("SF17 a fuse that blew on the reclose carries its operation's minute in the OMS", not blown, blown[:3])
    # SF22: where the OMS and the SCADA log both record an interruption the OMS's times govern (DRP-04 2.7), and the
    # two records pair without a judgment: every SCADA opening over five minutes has its ticket within a minute or
    # none within a day
    proc = G.procedure_constants(T)[2]
    ok("SF22 DRP-04 2.7 files the interruption clock: the OMS's times, the SCADA log where the OMS has no record",
       "times the outage management system records for it" in proc and "SCADA sequence-of-events log" in proc)
    tk = collections.defaultdict(list)
    for o in items:
        if o["src"] != "scada":
            tk[o["device"]].append(o["start"])
    pair_bad = []
    for dev, seq in res["soe"].items():
        for a, b in G.open_intervals(seq):
            if b - a <= 5 * 60000:
                continue
            dmin = min((abs(x - a) for x in tk.get(dev, [])), default=None)
            if dmin is not None and 60000 < dmin < 86400000:
                pair_bad.append((dev, a, dmin))
    ok("SF22 every SCADA opening over five minutes pairs with its ticket within a minute or has none within a day",
       not pair_bad, pair_bad[:3])
    # SF23: planned interruptions count (DRP-04 2.2)
    planned = [o for o in items if o["src"] != "scada" and str(o["cause"]).upper().startswith("PLAN")
               and W.REP0 <= o["day"] <= W.REP1 and o["day"] not in medset]
    ok("SF23 DRP-04 2.2 counts planned interruptions, and the window holds planned tickets on several feeders",
       "Planned interruptions" in proc and len({o["feeder"] for o in planned}) >= 5, len(planned))
    # SF24: no service point is connected or retired on the period's last day or after it
    edge_sp = [sp for sp, v in net.sp.items() if v["con"] >= W.REP1 or (v["dis"] and v["dis"] >= W.REP1)]
    ok("SF24 no service point is connected or retired on 31 October 2026 or after it", not edge_sp, edge_sp[:3])
    # SF25: a sustained interruption the OMS does not record runs from the opening that locked out its breaker or
    # recloser (DRP-04 2.7, the closing sentence), as the OMS times every lockout it records (the corroboration)
    ok("SF25 DRP-04 2.7 pins the start of an unrecorded sustained interruption at the opening that locked out its "
       "breaker or recloser, with 2.5 left to the counting",
       "does not record runs, for the indices, from the opening that locked out its breaker or recloser" in proc
       and "are part of it under 2.5, not momentary interruption events, and do not move its start" in proc)
    cross, cross_bad = 0, []
    for o in items:
        if o["src"] == "scada" or o["dtype"] not in ("BREAKER", "RECLOSER"):
            continue
        if o["device"] in res["soe"]:
            opens = sorted(t for t, st in res["soe"][o["device"]] if st == "OPEN"
                           and o["start"] - 2 * 60000 <= t <= o["start"] + 2 * 60000)
        else:
            opens = sorted(x["t"] for x in res["log"].get(o["device"], []) if x["ev"] == "TRIP"
                           and o["start"] - 2 * 60000 <= x["t"] <= o["start"] + 2 * 60000)
        if len(opens) < 2 or G.floor_min(opens[0]) == G.floor_min(opens[-1]):
            continue
        cross += 1
        if o["start"] != G.floor_min(opens[-1]):
            cross_bad.append(o["id"])
    ok("SF25 corroboration: every ticketed lockout whose first opening and lockout fall in different minutes carries "
       "the lockout's minute in the OMS (twenty or more)", cross >= 20 and not cross_bad, (cross, cross_bad[:3]))
    seq_bad = []
    for o in items:
        if o["src"] != "scada":
            continue
        ops_ = res["soe"][o["device"]]
        seq = [t for t, st in ops_ if st == "OPEN" and o["start"] - 5 * 60000 <= t <= o["start"]]
        before = [t for t, st in ops_ if st == "OPEN" and min(seq) - 5 * 60000 <= t < min(seq)]
        if o["start"] != o["lockout_open"] or before or not (0 < o["start"] - min(seq) < 30000):
            seq_bad.append((o["device"], str(o["day"])))
    ok("SF25 every unticketed lockout runs from its lockout opening, the last of a sequence under half a minute with "
       "no other opening in the five minutes before it", not seq_bad, seq_bad[:3])
    want = {"BLV-1": 308.4, "BLV-2": 83.2, "BLV-3": 169.5, "CTR-1": 146.6, "CTR-2": 209.8, "CTR-3": 76.8,
            "MLR-1": 301.4, "MLR-2": 139.8, "MLR-3": 87.9, "NYD-1": 23.6, "NYD-2": 412.9, "NYD-3": 64.2,
            "NYD-4": 113.9, "SYC-1": 153.2, "SYC-2": 127.5, "SYC-3": 356.4}
    got = {f: F["feeders"][f]["saidi"] for f in want}
    ok("SF25 the minutes of interruption per customer with unrecorded lockouts from their lockout opening",
       got == want, {f: (got[f], want[f]) for f in want if got[f] != want[f]})
    near = []
    ev_by_f = collections.defaultdict(list)
    for e in res["ev"]:
        if W.REP0 <= e["day"] <= W.REP1 and e["day"] not in medset:
            ev_by_f[e["feeder"]].append(e)
    for f, es in ev_by_f.items():
        es.sort(key=lambda e: e["t"])
        for a, b in zip(es, es[1:]):
            if a["device"] != b["device"] and 0 < b["t"] - a["t"] <= 5 * 60000:
                if net.customers(a["device"], a["day"]) & net.customers(b["device"], b["day"]):
                    near.append((a["device"], b["device"], b["t"]))
    merged = sum(e.get("n_merged", 0) for e in res["ev"] if W.REP0 <= e["day"] <= W.REP1 and e["day"] not in medset)
    ok("SF6 a customer's momentary interruptions within five minutes of the first count once, whichever devices "
       "opened (the few such pairs are merged per customer)", len(near) <= 6 and (merged > 0) == bool(near), (len(near), merged))
    crew = [o for o in items if o["src"] != "scada" and o["dtype"] in ("BREAKER", "RECLOSER")]
    pre = [o["id"] for o in crew if any(e["device"] == o["device"] and o["start"] - 5 * 60000 <= e["t"] <= o["start"] + 60000
                                        for e in res["ev"])]
    ok("SF21 the trips before a lockout are part of the sustained interruption, not momentary events", not pre, pre[:3])
    moved = [l for l, rows in net.rows.items() if len({r["feeder"] for r in rows}) > 1 and rows[0]["type"] == "FUSE"
             and len(rows) >= 2]
    ok("SF19 the moved taps' tickets before the move sit with the old feeder", moved_ok(res, net), len(moved))
    ok("SF7 a feeder's interruptions are those of its devices when each began (3.2)",
       all(o["feeder"] == net.feeder(o["device"], o["day"]) or o["continues"] is not None for o in items))
    ok("SF8 the window is local January to October 2026", all(W.REP0 <= o["day"] for o in items if o["day"].year == 2026))
    end_ms = G.ms(dt.datetime(2026, 11, 1, 5, tzinfo=dt.timezone.utc))
    late_items = [o["id"] for o in items if W.REP0 <= o["day"] <= W.REP1 and o["restore"] > end_ms]
    ok("axis 12: no interruption in the window runs past 31 October", not late_items, late_items[:3])
    tidy = tidy_ok(res, net)
    ok("SF20 no service point is connected or retired on a day an interruption reached it", not tidy, tidy[:3])

    # ------------------------------------------------------------------ the three rules on the clean truth
    ok("R1 the relays' records carry each trip's faulted phase and per-phase currents",
       open(os.path.join(T, PK.FILES["relay"])).readline().strip().split(",")[3:9] ==
       ["event_type", "shot", "ia_a", "ib_a", "ic_a", "ig_a"])
    ok("R1 the controls' logs carry fault terminals and kA, the register their phasing",
       "fault_terminals" in open(os.path.join(T, PK.FILES["recloser"])).readline()
       and "terminal_phasing" in open(os.path.join(T, PK.FILES["devices"])).readline())
    ok("R1 the OMS ships device-level tickets and the GIS service points", len(leg) > 500 and len(net.sp) > 30000)
    clean = clean_truth_call(S)
    ok("R2 clean-data test: on the clean truth the decisive grouping names MLR-2 and the default path NYD-3",
       clean == ("MLR-2", "NYD-3"), clean)
    ok("R2 the decisive population carries no ask device: every Aug-Oct breaker opening has its relay record",
       relay_complete(res, net))
    ok("R2 clocks differ by system (relay UTC, SCADA Central, controls CST)",
       open(os.path.join(T, PK.FILES["relay"])).readlines()[1].split(",")[2].endswith("Z")
       and open(os.path.join(T, PK.FILES["soe"])).readlines()[1].split(",")[0][-3:] in ("CDT", "CST")
       and "time_cst" in open(os.path.join(T, PK.FILES["recloser"])).readline())
    text = G.procedure_constants(T)[2]
    ok("R3a no file names a feeder for the patrol or ranks the feeders", no_ranking(text))
    hits = [w for w in ("current", "phase", "repeat", "recur", "impedance", "distance", "fault", "location", "same")
            if re.search(r"\b%s" % w, text, re.I)]
    ok("R3c DRP-04 names no current, phase, repeat, distance or fault", not hits, hits)
    ok("R3b reading every field right still files NYD-3 on the procedure's indices and screen",
       ranked(L, "dflt")[0] == "NYD-3")
    ok("R3c executing every filed rule names no patrol feeder (DRP-04 files purposes, definitions, thresholds)",
       "5.2" in text and "breaking down" in text and not re.search(r"most momentary|highest|rank", text, re.I))

    # ------------------------------------------------------------------ realism sweep
    wb = openpyxl.load_workbook(os.path.join(T, PK.FILES["oms"]), read_only=True)
    tk = [r[0] for r in wb["Legacy tickets"].iter_rows(min_row=2, values_only=True) if r[0] and not r[1]]
    incs = [r[0] for r in wb["Incidents"].iter_rows(min_row=2, values_only=True) if r[0]]
    wb.close()
    ok("realism: ticket numbers are not an arithmetic sequence", not const_step([int(x.split("-")[1]) for x in tk if x.startswith("T26")]))
    ok("realism: incident numbers are not an arithmetic sequence", not const_step([int(x.split("-")[2]) for x in incs]))
    with open(os.path.join(T, PK.FILES["relay"])) as fh:
        ev_no = collections.defaultdict(list)
        for r in csv.DictReader(fh):
            ev_no[r["relay"]].append(int(r["event_no"]))
    ok("realism: relay event numbers run with gaps", all(not const_step(sorted(v)) for v in ev_no.values() if len(v) > 3))
    ok("realism: service point ids are not sequential", not const_step(sorted(int(x) for x in list(net.sp)[:500])))
    ok("realism: the eleven are a minority of the relay file", 11 / sum(len(v) for v in ev_no.values()) < 0.02)
    ok("realism: personas from guard.py names", "Kelsey Sanford" in text and "Shawn Hartman" in text)
    ok("realism: the procedure issued before the year it governs", "12 January 2026" in text)
    scrub = []
    for f in files:
        p = os.path.join(T, f)
        b = open(p, "rb").read()
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                b = b"".join(z.read(n) for n in z.namelist())
        if re.search(rb"openpyxl|ReportLab|reportlab|python", b):
            scrub.append(f)
    ok("realism: containers scrubbed of the writing libraries", not scrub, scrub)
    late = []
    with open(os.path.join(T, PK.FILES["soe"])) as fh:
        for r in csv.DictReader(fh):
            if G.scada_t(r["time"]) >= G.ms(dt.datetime(2026, 11, 1, 5, tzinfo=dt.timezone.utc)):
                late.append(r["time"])
    ok("realism: no operation after the period", not late, late[:2])
    ok("realism: SCADA openings are stamped apart from the relays' trips (two observers)", soe_offsets(T, net))
    ok("realism: phases spread across the relay file", len({r["phases"] for r in recs_trip}) >= 6)
    for f, n in sorted(big.items()):
        pass
    tree = sorted(os.path.relpath(os.path.join(r, f), T).replace(os.sep, "/") for r, _, fs in os.walk(T) for f in fs)
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
        members = z.namelist()
        same = all(z.read(m) == open(os.path.join(T, m), "rb").read() for m in members if m in tree)
    ok("H4: target.zip holds the tree's files at its root, no enclosing folder or directory entries",
       members == tree and not any(m.endswith("/") or m.startswith("target/") for m in members), members[:3])
    ok("H7: target.zip agrees with the tree by content", same)
    fails = [r for r in RES if not r[1]]
    for label, good, detail in RES:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [" + detail + "]") if (detail and not good) else ""))
    print("%d checks, %d failed" % (len(RES), len(fails)))
    return 1 if fails else 0


def wb_matches(F):
    wb = openpyxl.load_workbook(os.path.join(TASK, "golden", "line_patrol_2026-11-09.xlsx"), read_only=True)
    ws = wb["Feeders Jan-Oct 2026"]
    good = True
    seen = 0
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r[0] not in F["feeders"]:
            continue
        seen += 1
        v = F["feeders"][r[0]]
        good &= (r[1] == v["nt"] and abs(r[2] - v["saidi"]) < 1e-9 and abs(r[3] - v["maifi"]) < 1e-9 and r[4] == v["cemi"])
    wb.close()
    return good and seen == 16


def moved_ok(res, net):
    for o in res["items"]:
        if o["dtype"] == "FUSE":
            rows = net.rows[o["device"]]
            if len({r["feeder"] for r in rows}) > 1 and o["feeder"] != net.row(o["device"], o["day"])["feeder"]:
                return False
    return True


def tidy_ok(res, net):
    days = collections.defaultdict(set)
    for o in res["items"]:
        d = o["day"]
        for sp in o["reach"]:
            days[sp].add(lday_safe(o["start"]))
    out = []
    for sp, v in net.sp.items():
        for k in ("con", "dis"):
            d = v[k]
            if d and d in days.get(sp, ()):
                out.append((sp, k, d))
    return out


def lday_safe(t):
    return G.lday(t)


def clean_truth_call(S):
    """The decisive grouping and the default path on the simulation's own operations, no file read."""
    ops = [o for o in S["ops"] if W.WIN0 <= o["day"] <= W.WIN1 and (not o["lockout"] or o.get("test_close"))]
    by = collections.defaultdict(list)
    for o in ops:
        by[(o["feeder"], o["device"], o["phases"])].append((o["rec"][0][o["phases"][0]], o["day"]))
    best = collections.Counter()
    for k, xs in by.items():
        xs.sort()
        for i in range(len(xs)):
            best[k[0]] = max(best[k[0]], len({d for c, d in xs if xs[i][0] <= c <= xs[i][0] * 1.04}))
    call = max(best, key=lambda f: best[f])
    return call, clean_default(S)


def clean_default(S):
    """The default path on the clean truth: momentary events, the storm screen, per overhead mile, against 2025."""
    net = build.world_cache["net"]
    wx = build.world_cache["wx"]
    stk = build.world_cache["stk"]
    TR = build.world_cache["TR"]
    gust = {sim.local_day(int(h)) for j, h in enumerate(wx["hours"]) if wx["gust"][j] >= 34.76}
    near = collections.defaultdict(set)
    for (t, x, y, amp, kind) in stk:
        if kind == "CG":
            for sid, v in W.SUBS.items():
                if math.hypot(x - v[1], y - v[2]) <= 8.047:
                    near[sid].add(sim.local_day(t))
    rate = {}
    for f in W.FID:
        F = net["feeders"][f]
        sd = near[F["sub"]] | gust
        a = sum(1 for e in TR["events"] if e["feeder"] == f and W.WIN0 <= e["day"] <= W.WIN1 and e["day"] not in sd)
        b = sum(1 for e in TR["events"] if e["feeder"] == f and W.BASE0 <= e["day"] <= W.BASE1 and e["day"] not in sd)
        rate[f] = (a - b) / round(F["main"] + F["lat_mi"], 1)
    return max(rate, key=lambda f: rate[f])


def relay_complete(res, net):
    rel = collections.defaultdict(list)
    with open(os.path.join(T, PK.FILES["relay"])) as fh:
        for r in csv.DictReader(fh):
            rel[net.nb(r["relay"])].append(G.utc_iso(r["utc_time"]))
    for dev, seq in res["soe"].items():
        if net.rows[dev][0]["type"] != "BREAKER":
            continue
        ts_ = sorted(rel.get(dev, []))
        for t, s in seq:
            if s == "OPEN" and W.WIN0 <= G.lday(t) <= W.WIN1:
                i = __import__("bisect").bisect_left(ts_, t - 200)
                if i >= len(ts_) or ts_[i] > t:
                    return False
    return True


def no_ranking(text):
    bad = []
    for f in ("vegetation/line_clearance_work_2023_2026.csv", "customers/blinking_lights_contacts_2025_2026.csv"):
        h = open(os.path.join(T, f)).readline()
        if re.search(r"rank|score|priority|patrol", h, re.I):
            bad.append(f)
    return not bad and not re.search(r"MLR-2|NYD-3|SYC-3", text)


def soe_offsets(T_, net):
    rel = []
    with open(os.path.join(T_, PK.FILES["relay"])) as fh:
        for r in csv.DictReader(fh):
            rel.append(G.utc_iso(r["utc_time"]))
    rel = set(rel)
    n = same = 0
    with open(os.path.join(T_, PK.FILES["soe"])) as fh:
        for r in csv.DictReader(fh):
            if r["state"] == "OPEN":
                n += 1
                same += G.scada_t(r["time"]) in rel
    return n > 0 and same == 0


if __name__ == "__main__":
    sys.exit(main())
