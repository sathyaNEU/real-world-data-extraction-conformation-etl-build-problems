"""The answer, computed from the shipped bundle and nothing else."""
import datetime as dt
import json
import os

import pandas as pd

import world as W

STANDARD_HOURS = 4
OUTSIDE = ("access network", "transit provider", "customer premises", "power or facility")
PCTL_RANK = 1296                  # clause 7.1: the 1,296th highest five-minute sample


def load(target):
    rd = lambda n: pd.read_csv(os.path.join(target, n), dtype=str, keep_default_na=False)
    return (rd("panel_throughput_minutes.csv"), rd("evening_quality_daily.csv"),
            rd("interconnect_register.csv"), rd("maintenance_windows.csv"),
            rd("collector_health_log.csv"), rd("edge_traffic_5min.csv"),
            rd("peering_commitments.csv"), rd("commitment_amendments.csv"),
            rd("client_sdk_sessions.csv"), rd("rebuffer_events_daily.csv"),
            rd("incident_log.csv"), rd("incident_restoration_extract.csv"),
            json.load(open(os.path.join(target, "sdk_release_log.json"), encoding="utf-8")))


def port_now(register):
    """the port code a record carries, resolved to the interconnect in service at the quarter end"""
    cur = {r.port_code: r.port_code for r in register.itertuples()
           if r.status == "in service" and r.port_type != "transit"}
    out = dict(cur)
    for r in register.itertuples():
        if r.current_port_code in cur:
            out[r.port_code] = r.current_port_code
    return out


def offset(day):
    return 2 if day >= W.DST_SPRING else 1


def shortfalls(rollup, register, maintenance):
    """every interconnect, evening and window of every quarter, with the booked evenings dropped"""
    nm = port_now(register)
    booked = set()
    for r in maintenance.itertuples():
        frm, to = int(r.window_from[:2]), int(r.window_to[:2])
        if to > W.EVENING_BAND[0] and frm < W.EVENING_BAND[1]:
            booked.add((nm.get(r.port_code, r.port_code), r.work_date_local))
    d = rollup[rollup["port_code"].isin(nm)].copy()
    d["line"] = [nm[x] for x in d["port_code"]]
    d["shortfall"] = pd.to_numeric(d["reference_median_kbps"]) - \
        pd.to_numeric(d["evening_median_kbps"])
    d["booked"] = [(a, b) in booked for a, b in zip(d["line"], d["evening_date_local"])]
    return d[~d["booked"]].copy(), d


def assess(target):
    (panel, rollup, register, maint, health, edge, commit, amend,
     sessions, rebuf, inc, res, releases) = load(target)
    kept, every = shortfalls(rollup, register, maint)
    q = W.Q_FROM.strftime("%YQ") + str((W.Q_FROM.month - 1) // 3 + 1)
    this = kept[kept["reporting_quarter"] == q]
    prior = kept[kept["reporting_quarter"] != q]

    # the figure the framework takes the decision on, and the record at the same selection
    worst = this.loc[this["shortfall"].idxmax()]
    by_q = prior.groupby("reporting_quarter")["shortfall"].max().sort_values(ascending=False)
    record = float(by_q.iloc[0])
    decided = float(worst["shortfall"])
    rank = int((by_q > decided).sum()) + 1

    # the per interconnect, per window grid the bulletin carries
    grid = {}
    for line, g in this.groupby("line"):
        for win, gg in g.groupby("window_from"):
            r = gg.loc[gg["shortfall"].idxmax()]
            grid[(line, win)] = (int(r["shortfall"]), r["evening_date_local"])
    closest = max(((v[0], l) for (l, w), v in grid.items()), key=lambda x: x[0])

    # the rungs
    rung0 = every[every["reporting_quarter"] == q]
    r0 = rung0.loc[rung0["shortfall"].idxmax()]
    means = this.groupby("line")["shortfall"].mean().sort_values(ascending=False)
    own99 = {l: float(g["shortfall"].quantile(0.99)) for l, g in this.groupby("line")}

    return {"decided_shortfall": decided, "decided_port": worst["line"],
            "decided_evening": worst["evening_date_local"], "decided_window": worst["window_from"],
            "record_shortfall": record, "record_quarter": by_q.index[0], "rank_of_nine": rank,
            "quarterly_worst": {k: int(v) for k, v in by_q.items()},
            "grid": grid, "closest_port": closest[1], "closest_shortfall": closest[0],
            "rung0_port": r0["line"], "rung0_shortfall": float(r0["shortfall"]),
            "rung2_port": means.index[0], "rung2_mean": float(means.iloc[0]),
            "rung2_next": float(means.iloc[1]),
            "own_99th": own99,
            "fund": None}, (panel, rollup, register, maint, health, edge, commit, amend,
                            sessions, rebuf, inc, res, releases)


def ask_peers(target):
    """A1: per peer, the quarter's billable percentile, the commitment billed on, the overage"""
    (_, _, register, _, _, edge, commit, amend, *_rest) = load(target)
    ports = {}
    for r in register.itertuples():
        if r.status == "in service":
            ports.setdefault(r.peer, []).append(r.port_code)
    e = edge.copy()
    e["mbps"] = pd.to_numeric(e["out_mbps"])
    billed = {r.peer: (float(r.commitment_mbps), float(r.rate_eur_per_mbps))
              for r in commit.itertuples()}
    for a in amend.itertuples():
        if a.status.startswith("accepted") and a.effective_from <= W.Q_TO.isoformat() \
                and a.peer in billed:
            billed[a.peer] = (float(a.commitment_mbps_after), billed[a.peer][1])
    out = {}
    for peer, (commitment, rate) in sorted(billed.items()):
        own = e[e["port_code"].isin(ports.get(peer, []))]
        # the peer's traffic, so the ports are added at each sample instant before the percentile
        per = own.groupby("sampled_at_utc")["mbps"].sum().sort_values(ascending=False)
        p95 = int(round(float(per.iloc[PCTL_RANK - 1])))
        over = max(0, p95 - int(round(commitment)))
        out[peer] = {"percentile_mbps": p95, "commitment_mbps": int(round(commitment)),
                     "overage_eur": int(round(over * rate))}
    return out


def ask_builds(target):
    """A2: per client build, the sessions and the share of them that rebuffered"""
    (*_a, sessions, rebuf, _i, _r, releases) = load(target)
    s = sessions.copy()
    s["n"] = pd.to_numeric(s["sessions"])
    rb = rebuf.copy()
    rb["n"] = pd.to_numeric(rb["sessions_with_rebuffer"])
    out = {}
    for b in releases["builds"]:
        lo, hi, v = b["rolled_out_from"], b["rolled_out_to"], b["build_version"]
        sel = s[(s["build_version"] == v) & (s["session_date_local"] >= lo) &
                (s["session_date_local"] <= hi)]
        rsel = rb[(rb["build_version"] == v) & (rb["session_date_local"] >= lo) &
                  (rb["session_date_local"] <= hi)]
        n = int(sel["n"].sum())
        out[b["build_ref"]] = {"build_version": v, "sessions": n,
                               "rebuffered_pct": round(100.0 * int(rsel["n"].sum()) / n, 1)}
    return out


def ask_incidents(target):
    """A3: per month, incidents opened, restored inside the standard, cause outside the platform"""
    (*_a, inc, res, _rel) = load(target)
    rest = {r.incident_ref: r.service_restored_at_utc for r in res.itertuples()}
    out = {}
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
        out[key] = {"opened": len(g), "restored_inside_standard": inside,
                    "cause_outside_platform": int(g["cause_category"].isin(OUTSIDE).sum())}
    return out


def compute(target):
    a, loaded = assess(target)
    a["fund"] = "none" if a["decided_shortfall"] <= a["record_shortfall"] else a["decided_port"]
    a["evenings_in_quarter"] = (W.Q_TO - W.Q_FROM).days + 1
    a["windows_assessed"] = len(W.PATHS) * a["evenings_in_quarter"] * len(W.WINDOWS)
    own = a["own_99th"][a["closest_port"]]
    a["closest_over_own_99th_pct"] = int(round(100 * (a["closest_shortfall"] / own - 1)))
    a["closest_below_record_pct"] = int(round(
        100 * (1 - a["closest_shortfall"] / a["record_shortfall"])))
    a["a1_peers"] = ask_peers(target)
    a["a2_builds"] = ask_builds(target)
    a["a3_incidents"] = ask_incidents(target)
    return a
