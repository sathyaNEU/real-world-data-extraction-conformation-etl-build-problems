"""An independent reader of the shipped bundle: it knows figures.json and target/ and nothing else."""
import datetime as dt
import json
import os

import pandas as pd

K = [0]
STANDARD_HOURS = 4
OUTSIDE = ("access network", "transit provider", "customer premises", "power or facility")
RANK = 1296
WINDOWS = ("19:00", "20:00", "21:00")
BAND = (19, 22)


def ok(cond, msg):
    K[0] += 1
    if not cond:
        raise AssertionError("verify: " + msg)


def run(target, figures):
    K[0] = 0
    fig = json.load(open(figures, encoding="utf-8"))
    rd = lambda n: pd.read_csv(os.path.join(target, n), dtype=str, keep_default_na=False)
    rollup = rd("evening_quality_daily.csv")
    panel = rd("panel_throughput_minutes.csv")
    register = rd("interconnect_register.csv")
    maint = rd("maintenance_windows.csv")
    edge = rd("edge_traffic_5min.csv")
    commit = rd("peering_commitments.csv")
    amend = rd("commitment_amendments.csv")
    sess = rd("client_sdk_sessions.csv")
    reb = rd("rebuffer_events_daily.csv")
    inc = rd("incident_log.csv")
    res = rd("incident_restoration_extract.csv")
    man = rd("telemetry_handover_inventory.csv")
    rel = json.load(open(os.path.join(target, "sdk_release_log.json"), encoding="utf-8"))

    ok(len(panel) >= 25000, "the panel holds %d rows" % len(panel))
    ok(int(man.loc[man["extract"] == "panel_throughput_minutes.csv",
                   "rows_handed_over"].iloc[0]) == len(panel),
       "the handover inventory disagrees on the panel")

    # the interconnect in service at the quarter end, for every code the records carry
    live = {r.port_code for r in register.itertuples()
            if r.status == "in service" and r.port_type != "transit"}
    now = {r.port_code: r.current_port_code for r in register.itertuples()
           if r.current_port_code in live}
    ok(len(set(now.values())) == 7, "%d interconnects resolve" % len(set(now.values())))

    booked = set()
    for r in maint.itertuples():
        if int(r.window_to[:2]) > BAND[0] and int(r.window_from[:2]) < BAND[1]:
            booked.add((now.get(r.port_code, r.port_code), r.work_date_local))
    ok(len(booked) == 9, "%d booked evenings reach an evening window" % len(booked))

    d = rollup[rollup["port_code"].isin(now)].copy()
    d["line"] = [now[x] for x in d["port_code"]]
    d["s"] = pd.to_numeric(d["reference_median_kbps"]) - pd.to_numeric(d["evening_median_kbps"])
    d = d[[(a, b) not in booked for a, b in zip(d["line"], d["evening_date_local"])]]

    this = d[d["reporting_quarter"] == "2027Q1"]
    prior = d[d["reporting_quarter"] != "2027Q1"]
    w = this.loc[this["s"].idxmax()]
    ok(int(w["s"]) == fig["decided_shortfall_kbps"], "the decided shortfall")
    ok(w["line"] == fig["decided_port"], "the decided interconnect")
    ok(w["evening_date_local"] == fig["decided_evening"], "the decided evening")
    ok(w["window_from"] == fig["decided_window"], "the decided window")
    by_q = prior.groupby("reporting_quarter")["s"].max().sort_values(ascending=False)
    ok(int(by_q.iloc[0]) == fig["flip_shortfall_kbps"], "the flip figure")
    ok(by_q.index[0] == fig["flip_quarter"], "the quarter the record comes from")
    ok(int((by_q > int(w["s"])).sum()) + 1 == fig["rank_of_nine"], "the rank of nine")
    ok(fig["call"] == ("none" if int(w["s"]) <= int(by_q.iloc[0]) else w["line"]), "the call")
    for qq, v in fig["quarterly_worst_kbps"].items():
        ok(int(by_q[qq]) == int(v), "the worst window of %s" % qq)

    # the grid the deliverable carries
    seen = 0
    for line, gl in this.groupby("line"):
        for win, gw in gl.groupby("window_from"):
            r = gw.loc[gw["s"].idxmax()]
            want = fig["grid"]["%s %s" % (line, win)]
            ok(int(r["s"]) == want["worst_kbps"], "the grid at %s %s" % (line, win))
            ok(r["evening_date_local"] == want["evening"], "the grid evening at %s %s" % (line, win))
            seen += 1
    ok(seen == 21, "the grid holds %d cells" % seen)

    # the panel's own medians agree with the rollup for the quarter it covers
    p = panel.copy()
    p["t"] = pd.to_datetime(p["measured_at_utc"].str[:19])
    p["v"] = pd.to_numeric(p["median_kbps"])
    off = p["t"].dt.date.map(lambda x: 2 if x >= dt.date(2027, 3, 28) else 1)
    p["local"] = p["t"] + pd.to_timedelta(off, unit="h")
    p["lday"] = p["local"].dt.date.astype(str)
    p["lh"] = p["local"].dt.hour
    p["line"] = [now.get(x, x) for x in p["port_code"]]
    checked = 0
    for (line, day, hr), gg in p[p["lh"].isin([19, 20, 21])].groupby(["line", "lday", "lh"]):
        if checked >= 60:
            break
        row = rollup[(rollup["evening_date_local"] == day) &
                     (rollup["window_from"] == "%02d:00" % hr) &
                     (rollup["port_code"].isin([k for k, v in now.items() if v == line] + [line]))]
        if len(row) != 1:
            continue
        ok(abs(gg["v"].median() - float(row["evening_median_kbps"].iloc[0])) <= 1.0,
           "the panel and the rollup disagree at %s %s %02d" % (line, day, hr))
        checked += 1
    ok(checked >= 40, "only %d window medians were cross checked" % checked)

    # A1
    ports = {}
    for r in register.itertuples():
        if r.status == "in service":
            ports.setdefault(r.peer, []).append(r.port_code)
    billed = {r.peer: (float(r.commitment_mbps), float(r.rate_eur_per_mbps))
              for r in commit.itertuples()}
    for a in amend.itertuples():
        if a.status.startswith("accepted") and a.effective_from <= "2027-03-31" and a.peer in billed:
            billed[a.peer] = (float(a.commitment_mbps_after), billed[a.peer][1])
    e = edge.copy()
    e["m"] = pd.to_numeric(e["out_mbps"])
    for peer, (c, rate) in billed.items():
        own = e[e["port_code"].isin(ports.get(peer, []))]
        per = own.groupby("sampled_at_utc")["m"].sum().sort_values(ascending=False)
        p95 = int(round(float(per.iloc[RANK - 1])))
        want = fig["a1_peers"][peer]
        ok(p95 == want["percentile_mbps"], "A1 percentile at %s" % peer)
        ok(int(round(c)) == want["commitment_mbps"], "A1 commitment at %s" % peer)
        ok(int(round(max(0, p95 - int(round(c))) * rate)) == want["overage_eur"],
           "A1 overage at %s" % peer)

    # A2
    s = sess.copy(); s["n"] = pd.to_numeric(s["sessions"])
    rb = reb.copy(); rb["n"] = pd.to_numeric(rb["sessions_with_rebuffer"])
    for b in rel["builds"]:
        sel = s[(s["build_version"] == b["build_version"]) &
                (s["session_date_local"] >= b["rolled_out_from"]) &
                (s["session_date_local"] <= b["rolled_out_to"])]
        rs = rb[(rb["build_version"] == b["build_version"]) &
                (rb["session_date_local"] >= b["rolled_out_from"]) &
                (rb["session_date_local"] <= b["rolled_out_to"])]
        want = fig["a2_builds"][b["build_ref"]]
        ok(int(sel["n"].sum()) == want["sessions"], "A2 sessions at %s" % b["build_ref"])
        ok(round(100.0 * int(rs["n"].sum()) / int(sel["n"].sum()), 1) == want["rebuffered_pct"],
           "A2 rebuffer share at %s" % b["build_ref"])

    # A3
    rest = {r.incident_ref: r.service_restored_at_utc for r in res.itertuples()}
    for m in (1, 2, 3):
        key = "2027-%02d" % m
        g = inc[inc["opened_at_utc"].str[:7] == key]
        inside = 0
        for r in g.itertuples():
            t = rest.get(r.incident_ref)
            if not t:
                continue
            a = dt.datetime.strptime(r.opened_at_utc, "%Y-%m-%dT%H:%M:%SZ")
            b = dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
            if (b - a).total_seconds() <= STANDARD_HOURS * 3600:
                inside += 1
        want = fig["a3_incidents"][key]
        ok(len(g) == want["opened"], "A3 opened in %s" % key)
        ok(inside == want["restored_inside_standard"], "A3 inside the standard in %s" % key)
        ok(int(g["cause_category"].isin(OUTSIDE).sum()) == want["cause_outside_platform"],
           "A3 causes outside in %s" % key)
    return K[0]
