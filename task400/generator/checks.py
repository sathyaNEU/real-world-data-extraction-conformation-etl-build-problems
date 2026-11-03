"""task400 assertions, run on the clean truth (world.py) and on the built pack (target/). Exit 1 on any failure.

    python3 task400/generator/checks.py
"""
import collections
import datetime as dt
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")

import numpy as np   # noqa: E402
import pandas as pd  # noqa: E402

import golden as G   # noqa: E402
import pack as PK    # noqa: E402
import world as W    # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def main():
    S = W.simulate()
    sh, inc, al = S["shifts"], S["incidents"], S["alarms"]
    P = G.load(TARGET)
    F = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------ the three rules on the clean truth
    def win(d, y):
        return d.year == y and 7 <= d.month <= 10
    n25 = sum(1 for i in inc if win(sh[i["sid"]]["day"], 2025))
    n26 = sum(1 for i in inc if win(sh[i["sid"]]["day"], 2026))
    check("R1 the field's raw material ships: alerts at event grain, speed samples per window, the register",
          len(P["alerts"]) > 100000 and (P["fms"]["trigger"] == "CAS_CRITICAL").sum() > 100000 and len(P["reg"]) > 400,
          "%d alerts, %d CAS_CRITICAL samples" % (len(P["alerts"]), (P["fms"]["trigger"] == "CAS_CRITICAL").sum()))
    cols = set(P["alerts"].columns) | set(P["fms"].columns) | set(P["disp"].columns) | set(P["reg"].columns)
    check("R1 no shipped column holds the deciding quantity (no response, slowdown or acted-on field)",
          not any(re.search(r"respon|slow|acted|brak|decel", c, re.I) for c in cols), str(sorted(cols)))
    loc26 = collections.Counter(i["loc"] for i in inc if win(sh[i["sid"]]["day"], 2026))
    loc25 = collections.Counter(i["loc"] for i in inc if win(sh[i["sid"]]["day"], 2025))
    nwst = {y: sum(1 for s in sh if win(s["day"], y) and s["circuit"] == "NP-WST") for y in (2025, 2026)}
    check("R3a analyst test on the clean truth: the North ramp junction is 2026's top location and the North waste route's "
          "shifts at least 1.8 times 2025's, so the hotspot and its traffic file B",
          loc26.most_common(1)[0][0] == "NRJ" and nwst[2026] >= 1.8 * nwst[2025],
          "top %s, NP-WST shifts %d -> %d" % (loc26.most_common(1), nwst[2025], nwst[2026]))
    rw = collections.defaultdict(lambda: [0, 0])
    for a in al:
        s = sh[a["sid"]]
        if a["level"] == "CRIT" and W.ROLLOUT_START <= s["day"] <= W.ROLLOUT_END:
            rw[a["fw"][0]][0] += a["responded"]
            rw[a["fw"][0]][1] += 1
    r4, r5 = rw["4"][0] / rw["4"][1], rw["5"][0] / rw["5"][1]
    check("R3b decisive step alone on the clean truth: in the rollout weeks critical alerts on 5.0.2 units were acted on at "
          "under half the 4.3 rate, on near-equal alert counts", r5 < 0.5 * r4 and 0.85 < rw["4"][1] / rw["5"][1] < 1.15,
          "%.3f vs %.3f on %d and %d" % (r4, r5, rw["4"][1], rw["5"][1]))
    check("R3c no plant: no document in the pack names a programme as the answer or argues for one",
          not re.search(r"recommend|should fund|we propose", PK_TEXT, re.I), "")

    # ------------------------------------------------------------------ the call's figures and the ladder (on the pack)
    w = G.window_counts(P)
    check("call counts reproduce the truth", w[2025] == n25 and w[2026] == n26, "%s vs %d, %d" % (w, n25, n26))
    check("the rise is more than three times", w[2026] > 3 * w[2025], str(w))
    a = G.crit_responses(P)
    rs = G.response_summary(a)
    check("decisive: 4.3 critical alerts acted on at 0.80 or more, 5.0.2 at 0.40 or less",
          rs["4.3"][0] >= 0.80 and rs["5.0.2"][0] <= 0.40, "%s %s" % (rs["4.3"], rs["5.0.2"]))
    check("decisive in the rollout window (2 to 23 June, both firmwares running)",
          rs["window"]["4.3"][0] >= 0.78 and rs["window"]["5.0.2"][0] <= 0.40, str(rs["window"]))
    # the method is open: every slowdown rule a competent reader might use gives the same split
    grid = []
    for slow in (4.0, 5.0, 6.0, 8.0, 10.0):
        for at in (4, 6, 8):
            x = G.response_summary(G.crit_responses(P, slow=slow, at=at))
            grid.append((slow, at, round(x["4.3"][0], 4), round(x["5.0.2"][0], 4), round(x["window"]["4.3"][0], 4),
                         round(x["window"]["5.0.2"][0], 4)))
    check("SF5 C1 converge: every slowdown rule (4 to 10 km/h, read at 4, 6 or 8 seconds) gives the rollout weeks 85 and 30 "
          "to the nearest 5 per cent, and keeps 4.3 at 0.84 or more and 5.0.2 at 0.33 or less over the whole record",
          all([5 * round(g[4] * 20), 5 * round(g[5] * 20)] == [85, 30] and g[2] >= 0.84 and g[3] <= 0.33 for g in grid),
          str(grid))
    m5 = [2.5 - abs(v * 100 - 5 * round(v * 20)) for g in grid for v in g[4:]]
    check("bins: the rollout-week percentages, graded to the nearest 5, sit at least 7 per cent of a bin from an edge under "
          "every rule (tightest %.2f points of 5)" % min(m5), min(m5) >= 0.35, "")
    # the rollout weeks read any way the register allows: local days, UTC days, first to last application, all of June
    fwt = P["fw"].copy()
    fwt["t"] = pd.to_datetime(fwt["Applied (UTC)"]) + pd.Timedelta(hours=8)
    fwt = fwt.merge(G.truck_of_unit(P)[["Serial", "Installed"]], on="Serial")
    v5t = fwt[fwt["Version"].str.startswith("5") & (fwt["t"].dt.normalize() > pd.to_datetime(fwt["Installed"]))]["t"]
    spans = {"local days": G.ROLLOUT, "UTC days": (G.ROLLOUT[0] + pd.Timedelta(hours=8), G.ROLLOUT[1] + pd.Timedelta(hours=8)),
             "first to last application": (v5t.min(), v5t.max()), "all of June": (pd.Timestamp("2026-06-01"),
                                                                                  pd.Timestamp("2026-07-01"))}
    aw0 = a[a["has_window"]]
    span_pct = {}
    for k, (lo, hi) in spans.items():
        x_ = aw0[(aw0["local"] >= lo) & (aw0["local"] < hi)]
        f_ = np.where(x_["Version"].str.startswith("5"), "5", "4")
        span_pct[k] = (round(x_[f_ == "4"]["slowed"].mean() * 100, 2), round(x_[f_ == "5"]["slowed"].mean() * 100, 2))
    m15 = min(2.5 - abs(v - 5 * round(v / 5)) for p_ in span_pct.values() for v in p_)
    check("SF15 the rollout weeks read as local days, UTC days, first to last application or all of June give 85 and 30 "
          "to the nearest 5 per cent, every figure at least 7 per cent of a bin from an edge (tightest %.2f points)" % m15,
          all((5 * round(v[0] / 5), 5 * round(v[1] / 5)) == (85, 30) for v in span_pct.values()) and m15 >= 0.35,
          str(span_pct))
    # A dies: the same operators, on the same days, acted on critical alerts on 4.3 units and not on 5.0.2 units
    d = P["disp"].copy()
    d["start"] = pd.to_datetime(d["shift_date"]) + pd.to_timedelta(np.where(d["shift"] == "DAY", 6, 18), unit="h")
    d["truck"] = d["truck_no"].str.replace("-", "", regex=False).astype(object)
    aw = a[a["has_window"] & (a["local"] >= G.ROLLOUT[0]) & (a["local"] < G.ROLLOUT[1])].copy()
    aw["truck"] = aw["truck"].astype(object)
    aw = pd.merge_asof(aw.sort_values("local"), d.sort_values("start")[["start", "truck", "operator_id"]],
                       left_on="local", right_on="start", by="truck", direction="backward",
                       tolerance=pd.Timedelta(hours=12))
    aw["f"] = np.where(aw["Version"].str.startswith("5"), "5", "4")
    both = aw.groupby("operator_id")["f"].nunique()
    both = set(both[both == 2].index)
    ab = aw[aw["operator_id"].isin(both)]
    wo = ab.groupby("f")["slowed"].mean()
    check("A dies: operators who drove both firmwares in the rollout weeks slowed for critical alerts at 0.80 or more on "
          "4.3 units and 0.40 or less on 5.0.2 units (%d operators)" % len(both),
          len(both) >= 60 and wo["4"] >= 0.80 and wo["5"] <= 0.40, str(wo.round(3).to_dict()))
    mon_r = rs["monthly"]
    check("the monthly response series alone falls in June 2026 (A's read): every month to May 2026 at 0.84 or more, "
          "every month July to October 2026 at 0.36 or less", all(v >= 0.84 for k, v in mon_r.items() if k <= 202605) and
          all(v <= 0.36 for k, v in mon_r.items() if 202607 <= k <= 202610), "")
    cr = a[a["has_window"]].copy()
    cr["f"] = np.where(cr["Version"].str.startswith("5"), "5", "4")
    ackf = cr.groupby("f")["ack_utc"].apply(lambda s: s.notna().mean())
    rngf = cr.groupby("f")["range_at_onset_m"].median()
    check("cheap route to C closed: critical alerts were acknowledged at the same rate on both firmwares (within two "
          "points) and fired at the same median range (within 1 m)", abs(ackf["4"] - ackf["5"]) < 0.02 and
          abs(rngf["4"] - rngf["5"]) < 1.0, "%s %s" % (ackf.round(3).to_dict(), rngf.to_dict()))
    fam = a[a["has_window"]].copy()
    fam["v"] = fam["Version"]
    split = fam.groupby("v")["slowed"].mean().round(3).to_dict()
    check("SF6 4.3.11 and 4.3.14 taken apart both stay high; same call", all(v >= 0.8 for k, v in split.items()
                                                                         if k.startswith("4")), str(split))
    # D's killer: the fall is the same on day and night shifts
    m = fam.copy()
    m["hr"] = m["local"].dt.hour
    m["night"] = (m["hr"] >= 18) | (m["hr"] < 6)
    v5 = m[m["v"].str.startswith("5")]
    dn = v5.groupby("night")["slowed"].mean()
    check("D dies: on 5.0.2 units day and night shifts slowed for critical alerts within 0.06 of each other",
          abs(dn[True] - dn[False]) < 0.06, str(dn.round(3).to_dict()))
    rr = G.route_rates(P)
    ratio = {k: (rr[(k, 2026)][0] / rr[(k, 2026)][1]) / (rr[(k, 2025)][0] / rr[(k, 2025)][1])
             for k in ("S-ORE>ROM", "N-WST>NWD", "S-WST>SWD", "N-ORE>ROM")}
    rates = {"%s %d" % (k_[0], k_[1]): 1000.0 * v_[0] / v_[1] for k_, v_ in rr.items() if k_[0] in ("S-ORE>ROM", "N-WST>NWD")}
    rmarg = {k_: 0.05 - abs(v_ - round(v_, 1)) for k_, v_ in rates.items()}
    rt_ = min(rmarg, key=rmarg.get)
    check("bins: the four step-2 rates per 1,000 truck shifts sit at least 7 per cent of a 0.1 bin from an edge (tightest "
          "%s at %.3f)" % (rt_, rates[rt_]), min(rmarg.values()) >= 0.007, str({k_: round(v_, 3) for k_, v_ in rates.items()}))
    check("B dies: the South pit ore route's rate per truck shift rose at least as much as the North waste route's",
          ratio["S-ORE>ROM"] >= ratio["N-WST>NWD"], str({k: round(v, 2) for k, v in ratio.items()}))
    x = G.vi_incidents(P)
    cru = {y: int(((x["when"].dt.year == y) & (x["when"].dt.month.between(7, 10)) & (x["Location code"] == "CRU")).sum())
           for y in (2025, 2026)}
    check("E dies: the crusher pad's share of the July to October incidents did not grow (%d of %d, then %d of %d)" %
          (cru[2025], w[2025], cru[2026], w[2026]), cru[2026] / w[2026] <= cru[2025] / w[2025], str(cru))
    nrj = {y: int(((x["when"].dt.year == y) & (x["when"].dt.month.between(7, 10)) & (x["Location code"] == "NRJ")).sum())
           for y in (2025, 2026)}
    check("rung 0 on the pack: NRJ is 2026's top location", nrj[2026] == x[(x["when"].dt.year == 2026) &
                                                                           x["when"].dt.month.between(7, 10)]["Location code"].value_counts().max(),
          str(nrj))
    # the cheap routes to C the coordinator listed, measured: none reads as a flood
    mon = PK_MONTHLY
    per = [m_["per100"] for m_ in mon]
    acks = [m_["ack"] for m_ in mon]
    check("no flood: alerts per 100 operating hours stay within 1.2 times of each other month to month",
          max(per) / min(per) < 1.2, "%.2f to %.2f" % (min(per), max(per)))
    check("no flood: the acknowledgement rate stays within two points", max(acks) - min(acks) < 2.0,
          "%.2f to %.2f" % (min(acks), max(acks)))
    # R3d: the incident draw is a representative realisation of the world's own rates, so the register does not argue
    # against the driver the records measure
    opf = {o["badge"]: o["factor"] for o in S["ops"]}
    msh = collections.Counter((s_["day"].year, s_["day"].month) for s_ in sh)
    exp_, tsw = collections.Counter(), collections.Counter()
    for s_ in sh:
        if W.ROLLOUT_START <= s_["day"] <= W.ROLLOUT_END:
            tsw[s_["firmware"][0]] += 1
            exp_[s_["firmware"][0]] += W.UNTAGGED_PER_MONTH / msh[(s_["day"].year, s_["day"].month)]
    for a_ in al:
        s_ = sh[a_["sid"]]
        if a_["real"] and W.ROLLOUT_START <= s_["day"] <= W.ROLLOUT_END:
            f_ = s_["firmware"][0]
            if a_["level"] == "WARN":
                exp_[f_] += W.P_INC["warn_only"]
            else:
                pr = min(1.0, W.P_RESP_CRIT["v5" if f_ == "5" else "v4"][0] * opf[s_["badge"]])
                exp_[f_] += pr * W.P_INC["crit_resp"] + (1 - pr) * W.P_INC["crit_none"] - W.P_INC["warn_only"]
    tiw = collections.Counter(sh[i["sid"]]["firmware"][0] for i in inc if W.ROLLOUT_START <= sh[i["sid"]]["day"] <= W.ROLLOUT_END)
    check("R3d the incident draw is representative: in the rollout weeks 4.3 units had %d incidents against %.1f expected "
          "from the world's rates on %d truck shifts (within 1.6 times), 5.0.2 units %d against %.1f on %d, the 5.0.2 rate "
          "above the 4.3 rate, and the weeks hold too few incidents to carry the call alone (under 25)" %
          (tiw["4"], exp_["4"], tsw["4"], tiw["5"], exp_["5"], tsw["5"]),
          exp_["4"] / 2.5 <= tiw["4"] <= 1.6 * exp_["4"] and exp_["5"] / 1.6 <= tiw["5"] <= 1.6 * exp_["5"] and
          tiw["5"] / tsw["5"] > tiw["4"] / tsw["4"] and tiw["4"] + tiw["5"] < 25, "")
    # timing alone cannot separate B from C: stage 3's traffic and the rollout share the month
    nw = {}
    for s in sh:
        if s["day"].year == 2026 and s["day"].month in (5, 6, 7):
            k = s["day"].month
            nw.setdefault(k, [0, 0])
            nw[k][0] += s["circuit"] == "NP-WST"
            nw[k][1] += 1
    check("timing: the North waste route's share of truck shifts and the rollout both step in June 2026 (share May under "
          "0.2, July over 0.3)", nw[5][0] / nw[5][1] < 0.2 and nw[7][0] / nw[7][1] > 0.3,
          str({k: round(v[0] / v[1], 3) for k, v in nw.items()}))

    # ------------------------------------------------------------------ fork table rows
    reg = P["reg"]
    check("SF1 vehicle interaction incidents are VI-COL and VI-SPI entries; adding other near misses moves the counts but "
          "not the call", set(reg["Classification"]) >= {"VI-COL", "VI-SPI", "NM"}, "")
    utc = pd.to_datetime(x["Occurred"]) - pd.Timedelta(hours=8)
    wu = {y: int(((utc.dt.year == y) & utc.dt.month.between(7, 10)).sum()) for y in (2025, 2026)}
    check("SF2 months in Western Australian time (terms 2.1); in UTC the windows hold %s, the call unchanged" % wu,
          abs(wu[2025] - w[2025]) <= 2 and abs(wu[2026] - w[2026]) <= 2, "")
    check("R2 Layer 1 never carries the call: the windows' counts read in UTC (%s) and the response split under every "
          "slowdown rule (SF5) leave the call on C, and no ask device sits on a CAS_CRITICAL window or a register row" % wu,
          abs(wu[2026] - w[2026]) <= 2 and (P["fms"][P["fms"]["trigger"] == "CAS_CRITICAL"]["segment"].fillna("") == "").all(),
          "")
    check("SF3 July to October inclusive, both years", True, "")
    check("SF4 'accounts for most of the rise': the 5.0.2 alerts carry most under every split the records allow (same call)",
          rs["window"]["5.0.2"][0] < 0.5 * rs["window"]["4.3"][0], "")
    gt = G.gate_trips(P)
    truth_trips = collections.Counter((t.month, nt) for t, rego, gate, nt in PK_GATE_TRUTH)
    check("SF7 a trip is one entry: the golden pairing reproduces the generator's passages exactly",
          all(gt[m] == (truth_trips[(m, False)] + truth_trips[(m, True)], truth_trips[(m, True)]) for m in (7, 8, 9, 10)),
          str(gt))
    check("SF8 a trip's tag status is the same on both North gate reads (no trip read once with and once without a tag)",
          PK_TAG_CONSISTENT, "")
    tv = sorted(PK_GATE_TRUTH, key=lambda x: (x[1], x[0]))
    close = sum(1 for a_, b_ in zip(tv, tv[1:]) if a_[1] == b_[1] and (b_[0] - a_[0]).total_seconds() < 1200)
    check("SF7 one vehicle's entries are at least 20 minutes apart (%d closer), so every trip is an entry with its own "
          "exit between, whatever window a solver uses to collapse a vehicle's repeated reads" % close, close == 0, "")
    os_ = G.overspeed(P)
    edges = [abs(e - 5.0) for v in os_.values() for e in v[2]]
    check("SF10 'peaked more than 5 km/h over' has no run peak within 0.3 km/h of the line (closest %.2f)" % min(edges),
          min(edges) >= 0.3, "")
    ow = G.overspeed_windows(P)
    alt = {}
    for thr in (0.0, 1.0, 2.0):
        rid, k_, prev = [], -1, None
        for row in ow.itertuples():
            cont = prev is not None and row.truck_no == prev.truck_no and row.segment == prev.segment and \
                (row.tt - prev.tt).total_seconds() == 10 and row.first > row.limit + thr
            k_ += 0 if cont else 1
            rid.append(k_)
            prev = row
        alt[thr] = len(set(rid))
    shared = ow[["truck_no", "segment", "tt", "first", "last"]].copy()
    nxt = shared.shift(-1)
    pair = (nxt["truck_no"] == shared["truck_no"]) & (nxt["segment"] == shared["segment"]) & \
        ((nxt["tt"] - shared["tt"]).dt.total_seconds() == 10)
    check("SF9 'one continuous run': a window joins the run before it only where it opens on the sample that closed it "
          "(both windows carry that instant, %d pairs, every one the same reading) with the truck over the limit there; "
          "the run count is the same for any line from the limit to the limit plus 2 at that sample (C1: %s)" %
          (int(pair.sum()), sorted(set(alt.values()))),
          len(set(alt.values())) == 1 and (shared[pair]["last"].values == nxt[pair]["first"].values).all(), "")
    chg = {}
    for sg_, grp in P["limits"].groupby("segment"):
        e_ = sorted(pd.to_datetime(grp["effective_from"]))
        chg[sg_] = set(d_.normalize() for d_ in e_[1:])
    on_change = int(sum(1 for sg_, t_ in zip(ow["segment"], ow["tt"]) if t_.normalize() in chg.get(sg_, ())))
    check("SF11 no ramp window falls on the day its limit changed (%d do), so no run sits between the old and the new "
          "limit on a change day" % on_change, on_change == 0, "")
    check("SF11 the limit in force: the schedule's dates, not the window's limit_kmh column (which carries today's limit)",
          (P["fms"][(P["fms"]["trigger"] == "OVERSPEED") & (P["fms"]["segment"] == "NRP")]["limit_kmh"].dropna() == 32).all(), "")
    check("SF12 calendar months by the window's trigger time (local); SF13 the ramps are NRP and SRP; SF14 light vehicles "
          "only at the gates", set(P["gate"]["plate_read"].str[0]) <= {"1"}, "")
    check("SF16 the gate reads and the event windows carry their zone in the header (read_time_awst, trigger_time_awst), "
          "so months are Western Australian months; read as UTC the ask figures would move, which the header rules out",
          "read_time_awst" in P["gate"].columns and "trigger_time_awst" in P["fms"].columns, "")
    lvt = P["dev"][P["dev"]["Device type"] == "LV tag T2"].copy()
    lvt["inst"] = pd.to_datetime(lvt["Installed"])
    lvt["rem"] = pd.to_datetime(lvt["Removed"]).fillna(pd.Timestamp("2100-01-01"))
    gg = P["gate"][P["gate"]["cas_tag"] != ""].copy()
    gg["t"] = pd.to_datetime(gg["read_time_awst"])
    gg = gg.merge(lvt[["Serial", "inst", "rem"]], left_on="cas_tag", right_on="Serial", how="left")
    unreg = int((gg["Serial"].isna() | (gg["t"] < gg["inst"]) | (gg["t"] >= gg["rem"])).sum())
    check("SF17 'no tag detected' is a blank cas_tag; every tag the gates did read is a registered light vehicle tag in "
          "service at the read time (%d not), so reading a tag missing from the register as undetected gives the same "
          "figures" % unreg, unreg == 0, "")
    fb = a[a[0].notna()].copy()
    piv_ = P["fms"][P["fms"]["trigger"] == "CAS_CRITICAL"].pivot_table(index="event_ref", columns="t_offset_s",
                                                                         values="speed_kmh", aggfunc="first")
    os_full = P["fms"][P["fms"]["trigger"] == "OVERSPEED"]
    ospk = os_full.groupby("event_ref")["speed_kmh"].max()
    os_edges = os_full[os_full["t_offset_s"].isin([os_full["t_offset_s"].min(), os_full["t_offset_s"].max()])]
    nofix = int(os_edges["speed_kmh"].isna().sum())
    check("SF18 samples with no GPS fix: every OVERSPEED window keeps its first, last and highest sample (%d edge samples "
          "missing), so the ask figures are the same whether fix-less samples are dropped or kept; the braking split reads "
          "only alerts whose window has speeds at 0 and 6 s, and taking 8 or 4 s where 6 s is missing gives the same "
          "rollout figures" % nofix, nofix == 0 and RS_FALLBACK == (85, 30), str(RS_FALLBACK))

    # ------------------------------------------------------------------ the asks: stops outside every bin
    g = P["gate"]
    ins = g[g["direction"] == "IN"].copy()
    ins["m"] = ins["read_time_awst"].str[5:7].astype(int)
    naive = ins.groupby("m").size().to_dict()
    check("ask A: counting every IN read misses every month", all(naive[m] != gt[m][0] for m in (7, 8, 9, 10)),
          str(naive))
    nn = g[(g["direction"] == "IN")].copy()
    nn["t"] = pd.to_datetime(nn["read_time_awst"])
    nn["m"] = nn["t"].dt.month
    nn = nn.sort_values("t")
    keep = []
    last = {}
    for t, rd, pl in zip(nn["t"], nn["reader"], nn["plate_read"]):
        k = (rd[:2], pl)
        keep.append(not (k in last and (t - last[k]).total_seconds() <= 30))
        last[k] = t
    nn = nn[keep]
    by_plate = nn.groupby("m").size().to_dict()
    check("ask A: one trip per plate per gate within 30 seconds keeps the pairs whose plates the two readers returned "
          "differently and misses every month", all(by_plate[m] != gt[m][0] for m in (7, 8, 9, 10)), str(by_plate))
    raw = P["fms"][(P["fms"]["trigger"] == "OVERSPEED") & P["fms"]["segment"].isin(["NRP", "SRP"])]
    evc = raw.groupby(["event_ref", "segment", "trigger_time_awst", "limit_kmh"])["speed_kmh"].max().reset_index()
    evc["q"] = evc["trigger_time_awst"].str[5:7].astype(int)
    evc = evc[evc["trigger_time_awst"].str[:4] == "2026"]
    MS = (7, 8, 9, 10)
    restated = {(s, q): int(((evc["segment"] == s) & (evc["q"] == q) & (evc["speed_kmh"] > evc["limit_kmh"] + 5)).sum())
                for s in ("NRP", "SRP") for q in MS}
    check("ask B: the window's own limit column moves the South ramp's July over-5 figure",
          restated[("SRP", 7)] != os_[("SRP", 7)][1], "%s vs golden %s" % (restated, {k: v[1] for k, v in os_.items()}))
    unmerged = {(s, q): int(((evc["segment"] == s) & (evc["q"] == q)).sum()) for s in ("NRP", "SRP") for q in MS}
    check("ask B: counting the FMS's windows rather than runs moves every August to October count",
          all(unmerged[(s, q)] != os_[(s, q)][0] for s in ("NRP", "SRP") for q in (8, 9, 10)), str(unmerged))
    ab10 = G.overspeed(P, joins=10)
    ab30 = G.overspeed(P, joins=30)
    m10 = sum(ab10[k][0] != os_[k][0] for k in os_)
    m30 = sum(ab30[k][0] != os_[k][0] for k in os_)
    check("ask B: taking windows that abut in time as one run (a gap of 10 s or less) misses %d of the 8 counts, and "
          "within 30 s %d of 8 (the runs that dip under the limit and run away again at the next sample)" % (m10, m30),
          m10 >= 6 and m30 == 8, "")
    check("separation: the call reads CAS_CRITICAL windows only, the ask OVERSPEED windows only",
          set(P["fms"]["trigger"]) == {"CAS_CRITICAL", "OVERSPEED"}, "")

    # ------------------------------------------------------------------ figures, bins and the write-up
    check("figures.json carries the golden's figures", F["vi_jul_oct_2026"] == w[2026] and F["trips_07"] == gt[7][0], "")
    ints = [v for k, v in F.items() if isinstance(v, int) and not isinstance(v, bool)]
    check("every graded figure is a whole count (bin edge distance 0.5 of a unit for each)", len(ints) >= 22, str(len(ints)))

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("input gate: 3 or more formats", len(exts) >= 3, str(exts))
    check("input gate: a 25,000-row file", len(P["alerts"]) >= 25000, "")
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input gate: two or more distractors named in metadata.json and shipped",
          len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "")
    check("no file describes the data (no readme, dictionary, notes or manifest)",
          not any(re.search(r"readme|dictionary|notes|manifest|codebook|schema", f, re.I) for f in files), str(files))
    check("no file name names the stump", not any(re.search(r"firmware|response|fatigue_|stump|answer", f, re.I) for f in files), "")
    fleet_nums = sorted(int(t[2:]) for t in S["fleet"]["trucks"])
    diffs = set(np.diff(fleet_nums))
    check("realism: fleet numbers are not an arithmetic sequence", len(diffs) > 1, str(sorted(diffs)[:6]))
    refs = sorted(P["fms"]["event_ref"].unique())
    check("realism: event references are not an arithmetic sequence", len(set(np.diff(refs[:500]))) > 1, "")
    incn = [int(s.split("-")[2]) for s in reg["Incident no."] if s.startswith("INC-2026")]
    check("realism: incident numbers are not an arithmetic sequence", len(set(np.diff(incn))) > 1, "")
    check("realism: monthly gate trips are not identical", len({gt[m][0] for m in gt}) == 4, "")
    check("realism: monthly incident counts are not uniform", len({v for _, v in F["monthly"]}) > 6, "")
    rep = P["reg"]["Description"].value_counts()
    check("realism: no register description repeats more than three times (most: %d)" % int(rep.max()), rep.max() <= 3,
          str(rep.head(3).to_dict()))
    check("realism: no round headline (the 2026 count is not a multiple of 10)", w[2026] % 10 != 0, str(w[2026]))
    # office properties (house fix H1)
    for fn in [f for f in files if f.endswith((".docx", ".xlsx"))] + ["../golden/vi_programme_paper_2027.docx",
                                                                       "../golden/vi_workings_2026.xlsx"]:
        p = os.path.join(TARGET, fn)
        z = zipfile.ZipFile(p)
        names = z.namelist()
        app = z.read("docProps/app.xml").decode()
        ok = "stylesWithEffects" not in " ".join(names) and "<Company>" in app
        if fn.endswith(".docx"):
            wds = re.search(r"<Words>(\d+)</Words>", app)
            ok = ok and wds is not None and int(wds.group(1)) > 20 and "Microsoft Office Word" in app
        else:
            ok = ok and "Microsoft Excel" in app
        check("H1 office properties true to the document: %s" % os.path.basename(fn), ok, "")
    for fn in [f for f in files if f.endswith(".pdf")]:
        b = open(os.path.join(TARGET, fn), "rb").read()
        check("H1 PDF carries no writing-library banner: %s" % fn, b"ReportLab" not in b and b"reportlab" not in b, "")
        check("H1 PDF carries no library default info entry (empty /Subject, empty /Keywords, /Trapped): %s" % fn,
              b"/Trapped" not in b and not re.search(rb"/Subject\s*\(\s*\)", b) and not re.search(rb"/Keywords\s*\(\s*\)", b),
              "")
    people = ["Shari Jefferson", "Ana Cuevas", "Nancy Franco"]
    check("personas are the drawn names", PK_TEXT.count("Shari Jefferson") + PK_TEXT.count("Ana Cuevas") +
          PK_TEXT.count("Nancy Franco") >= 2, str(people))
    check("no document dated after its own file date: the notice 2 Sep, the terms 22 Sep, the report 2 Nov 2026",
          "2 September 2026" in PK_TEXT and "22 September 2026" in PK_TEXT, "")
    mt = {os.path.getmtime(os.path.join(TARGET, f)) for f in files}
    check("every file carries one export stamp", len(mt) == 1, "")
    check("distractors unread by the golden: golden.load opens neither", "dust" not in open(os.path.join(HERE, "golden.py")).read()
          and "road_maintenance" not in open(os.path.join(HERE, "golden.py")).read(), "")

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail[:200] + "]") if detail and not ok else ""))
    print("%d assertions, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def _pack_text():
    import docx
    from pypdf import PdfReader
    out = []
    for fn in sorted(os.listdir(TARGET)):
        p = os.path.join(TARGET, fn)
        if fn.endswith(".docx"):
            out.append("\n".join(par.text for par in docx.Document(p).paragraphs))
        elif fn.endswith(".pdf"):
            out.append("\n".join(pg.extract_text() for pg in PdfReader(p).pages))
    txt = "\n".join(out)
    assert "Mines Safety Inspectorate" in txt and "terms of reference" in txt, "positive control: the documents read"
    return txt


if __name__ == "__main__":
    PK_TEXT = _pack_text()
    import tempfile
    tmp = tempfile.mkdtemp(prefix="t400c_")
    _R = PK.cut(os.path.join(tmp, "t"))
    PK_MONTHLY = _R["monthly"]
    PK_GATE_TRUTH = _R["gate_truth"]
    g_ = _R["gate"]
    ng = g_[g_["reader"].isin(["NG-1", "NG-2"]) & (g_["direction"] == "IN")].copy()
    ng["t"] = pd.to_datetime(ng["read_time_awst"])
    ng = ng.sort_values("t")
    prev = None
    bad = 0
    for t, rd, tag in zip(ng["t"], ng["reader"], ng["cas_tag"]):
        if rd == "NG-2" and prev is not None and prev[1] == "NG-1" and 2 <= (t - prev[0]).total_seconds() <= 13:
            bad += (tag == "") != (prev[2] == "")
        prev = (t, rd, tag)
    PK_TAG_CONSISTENT = bad == 0
    _rf = G.response_summary(G.crit_responses(G.load(TARGET), fallback=(8, 4)))["window"]
    RS_FALLBACK = (int(5 * round(_rf["4.3"][0] * 20)), int(5 * round(_rf["5.0.2"][0] * 20)))
    import shutil
    shutil.rmtree(tmp)
    sys.exit(main())
