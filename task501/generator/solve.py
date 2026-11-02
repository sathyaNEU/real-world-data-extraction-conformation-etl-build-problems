"""The golden's method, run on the shipped pack: each trunk main's hourly flow rebuilt from the district meters
through the arrangement the valve log shows in force, its highest hourly flow in the reference year, its highest
hourly flow under the relining arrangement on the same dates a year earlier, and the asks. The ladder's easy routes
are here too, so every rung is computed by the same code from the same files."""
import datetime as dt

import numpy as np
import pandas as pd

import bundle as B

WORKS_JUNCTION = "Copt Hill works outlet"
REPLAY = (dt.date(2026, 3, 15), dt.date(2026, 9, 15))
WINDOW = (pd.Timestamp("2025-11-01 00:00"), pd.Timestamp("2026-10-31 23:00"))


class Network:
    def __init__(self, target):
        mains, valves, dmas = B.register(target)
        self.mains = {m["Main"]: m for m in mains}
        self.valves = {v["Valve"]: v for v in valves}
        self.dmas = {d["DMA"]: d for d in dmas}
        self.normal_valve = {v["Valve"]: v["Normal position"] for v in valves}
        self.by_main = {}
        for v in valves:
            self.by_main.setdefault(v["Main"], []).append(v["Valve"])

    def in_service(self, state):
        """Mains in service under a valve state (valve -> Open/Shut): every valve on the main open."""
        return frozenset(m for m, vs in self.by_main.items() if all(state[v] == "Open" for v in vs))

    def normal(self):
        return self.in_service(dict(self.normal_valve))

    def paths(self, in_service):
        adj = {}
        for m in sorted(in_service):
            a, b = self.mains[m]["From"], self.mains[m]["To"]
            adj.setdefault(a, []).append((m, b))
            adj.setdefault(b, []).append((m, a))
        path = {WORKS_JUNCTION: []}
        q, used = [WORKS_JUNCTION], set()
        while q:
            u = q.pop(0)
            for m, v in adj.get(u, []):
                if m in used:
                    continue
                used.add(m)
                if v in path:
                    raise ValueError("loop")
                path[v] = path[u] + [m]
                q.append(v)
        return path

    def routing(self, in_service, dma_order):
        """Main x district 0/1 matrix: which districts' inflow each main carries."""
        path = self.paths(in_service)
        mains = sorted(self.mains)
        R = np.zeros((len(mains), len(dma_order)))
        for j, d in enumerate(dma_order):
            node = self.dmas[d]["Inlet junction"]
            for m in path[node]:
                R[mains.index(m), j] = 1.0
        return mains, R


def _is_tree(net, s):
    """A state the routing can carry: no two routes in parallel and every district inlet fed."""
    try:
        p = net.paths(s)
    except ValueError:
        return False
    return all(d["Inlet junction"] in p for d in net.dmas.values())


def arrangement_by_hour(net, log, hours, at="majority", shift_hours=0):
    """In-service set for each UTC hour from the valve log, starting from the register's normal positions. Valves not
    in the register are distribution valves and are left out; exercising changes nothing. In an hour with valve
    operations: at='majority' takes the arrangement in force for most of the hour, 'start' the one at its start and
    'end' the one at its end; minutes with two routes open in parallel count under the arrangement before them."""
    ops = log[log["valve_no"].isin(net.valves) & log["action"].isin(["OPEN", "CLOSE"])].sort_values("utc")
    changes = [(pd.Timestamp(t) + pd.Timedelta(hours=shift_hours), v, "Open" if a == "OPEN" else "Shut")
               for t, v, a in zip(ops["utc"], ops["valve_no"], ops["action"])]
    state = dict(net.normal_valve)
    cur = net.in_service(state)
    out = []
    k = 0
    for h in hours:
        h1 = h + pd.Timedelta(hours=1)
        if k >= len(changes) or changes[k][0] >= h1:
            out.append(cur)
            continue
        counts, seq = {}, []
        start_set = cur
        for mnt in range(60):
            t = h + pd.Timedelta(minutes=mnt, seconds=30)
            while k < len(changes) and changes[k][0] <= t:
                state[changes[k][1]] = changes[k][2]
                k += 1
            s_ = net.in_service(state)
            if _is_tree(net, s_):
                cur = s_
            counts[cur] = counts.get(cur, 0) + 1
            seq.append(cur)
        while k < len(changes) and changes[k][0] < h1:
            state[changes[k][1]] = changes[k][2]
            k += 1
            s_ = net.in_service(state)
            if _is_tree(net, s_):
                cur = s_
        if at == "majority":
            out.append(max(counts, key=lambda s_: (counts[s_], -seq.index(s_))))
        elif at == "start":
            out.append(start_set)
        else:
            out.append(seq[-1])
    return out


def trunk_flows(net, inflow, sets):
    """Hourly flow (l/s) in every main: inflow is an hour x district frame, sets the in-service set per hour."""
    dma_order = list(inflow.columns)
    X = inflow.values
    mains = sorted(net.mains)
    F = np.full((len(inflow), len(mains)), np.nan)
    groups = {}
    for i, s in enumerate(sets):
        groups.setdefault(s, []).append(i)
    for s, ii in groups.items():
        _, R = net.routing(s, dma_order)
        ii = np.array(ii)
        F[ii] = X[ii] @ R.T
    return pd.DataFrame(F, index=inflow.index, columns=mains)


def replay_mask(index):
    d = (index + pd.to_timedelta([1 if _bst(t) else 0 for t in index], unit="h")).date
    return np.array([REPLAY[0] <= x <= REPLAY[1] for x in d])


def _bst(t):
    return any(a <= t.to_pydatetime() < b for a, b in B.UK_BST)


def plan_set(net, plan_ops):
    state = dict(net.normal_valve)
    for v, op in plan_ops:
        state[v] = op
    return net.in_service(state)


def call(target, gaps="drop", at="majority", shift_hours=0, model="operated"):
    """The call on the shipped pack. model='operated' rebuilds the reference through the logged arrangements (the
    golden); 'normal' through the register's normal valve states (the default path); 'bursts' through the logged
    arrangements of emergency jobs only (remarks marked BURST); 'planned' through the planned jobs only."""
    net = Network(target)
    inflow, _ = B.flows(target)
    if gaps == "fill":
        inflow = inflow.interpolate(limit_direction="both")
    log = B.valve_log(target)
    pl = B.plan(target)
    hours = inflow.index
    if model == "operated":
        sets = arrangement_by_hour(net, log, hours, at, shift_hours)
    elif model == "normal":
        sets = [net.normal()] * len(hours)
    else:
        burst_jobs = set(log.loc[log["remarks"].str.upper().str.contains("BURST"), "job_ref"])
        keep = log["job_ref"].isin(burst_jobs) if model == "bursts" else ~log["job_ref"].isin(burst_jobs)
        sets = arrangement_by_hour(net, log[keep], hours, at, shift_hours)
    ok = inflow.notna().all(axis=1) if gaps == "drop" else pd.Series(True, index=hours)
    F = trunk_flows(net, inflow.fillna(0.0), sets)
    ref = F[ok.values].max()
    rm = replay_mask(hours)
    ps = plan_set(net, pl["ops"])
    P = trunk_flows(net, inflow.fillna(0.0), [ps] * len(hours))
    N0 = trunk_flows(net, inflow.fillna(0.0), [net.normal()] * len(hours))
    use = rm & ok.values
    peak = P[use].max()
    normal_peak = N0[use].max()
    rises = [m for m in sorted(net.mains) if (P[use][m] > N0[use][m] + 1e-9).all()]
    falls_or_same = [m for m in sorted(net.mains) if (P[use][m] <= N0[use][m] + 1e-9).all()]
    flush = [m for m in rises if peak[m] > ref[m]]
    return dict(rises=rises, flush=flush, peak=peak, ref=ref, normal_peak=normal_peak, F=F, P=P, N0=N0, ok=ok,
                sets=sets, use=use, falls_or_same=falls_or_same, net=net)


# ------------------------------------------------------------------------------------------------ ask A
def ask_a(target, how="golden"):
    """Water per 100 m of main flushed, by diameter and year of the night. how: 'golden' (a night whose readings run
    on is differenced; the hydrants run together on one section are one flush, its length counted once), 'plain'
    (volume_m3 and section_length_m by their plain meaning, re-sent rows dropped), 'gauge' (gauge flow times the
    flush's minutes), 'diff_all' (every night differenced), 'dedup' (one row per section kept), 'running_only'
    (running nights differenced, every row's length kept), 'twin_only' (twin rows summed, length once, readings as
    written)."""
    df = B.jobs(target).drop_duplicates().reset_index(drop=True)
    df["night"] = [pd.Timestamp(dt.date.fromisoformat(x)) if "-" in x else pd.Timestamp(dt.datetime.strptime(
        x, "%d/%m/%Y")) for x in df["night_of"]]
    df["year"] = df["night"].dt.year
    df["dn"] = df["main_dn_mm"].astype(int)
    df["L"] = df["section_length_m"].astype(float)
    df["vol"] = df["volume_m3"].astype(float)
    df["g"] = df["gauge_flow_l_s"].astype(float)
    st = pd.to_datetime(df["start"], format="%H:%M")
    fi = pd.to_datetime(df["finish"], format="%H:%M")
    mins = (fi - st).dt.total_seconds() / 60.0
    df["mins"] = mins.where(mins > 0, mins + 1440)
    df["gxt"] = df["g"] * df["mins"] * 0.06
    df["key"] = df["night_of"] + "|" + df["crew"]
    # a night runs on where its readings climb section by section beyond each flush's own gauge-and-minutes figure
    first = ~df.duplicated(["key"])
    df["prev"] = df.groupby("key")["vol"].shift(1)
    df["step"] = df["vol"] - df["prev"]
    df["runs_on"] = (df["vol"] > 1.2 * df["gxt"]) & ~first
    night_runs = df.groupby("key")["runs_on"].any()
    df["night_runs"] = df["key"].map(night_runs)
    if how in ("golden", "running_only"):
        df["w"] = np.where(df["night_runs"] & ~first, df["step"], df["vol"])
    elif how == "diff_all":
        df["w"] = np.where(~first, df["step"].clip(lower=0), df["vol"])
    elif how == "gauge":
        df["w"] = df["gxt"]
    else:
        df["w"] = df["vol"]
    if how in ("golden", "twin_only"):
        sec = df.groupby(["night_of", "crew", "section_ref"]).agg(w=("w", "sum"), L=("L", "first"), dn=("dn", "first"),
                                                                   year=("year", "first")).reset_index()
    elif how == "dedup":
        sec = df.drop_duplicates(["night_of", "section_ref"])[["w", "L", "dn", "year"]]
    else:
        sec = df[["w", "L", "dn", "year"]]
    g = sec.groupby(["dn", "year"]).agg(w=("w", "sum"), L=("L", "sum"))
    return (g["w"] / g["L"] * 100.0).to_dict(), df


# ------------------------------------------------------------------------------------------------ ask B
def ask_b(target, how="golden", districts=None):
    """Non-household water (Ml) from November 2025 to October 2026 by supplying district. how: 'golden' (a supply
    point whose own logged use passes its recorded district's whole inflow in some hour is supplied from the district
    whose inflow carries its load), 'plain' (the recorded DMA), 'corr' (every logged supply point moved to the district
    whose inflow its use tracks best)."""
    sp = B.supply(target)
    con = B.consumption(target)
    con = con[(con["month"] >= "2025-11") & (con["month"] <= "2026-10")]
    vol = con.groupby("spid")["consumption_m3"].sum()
    sp["vol"] = sp["SPID"].map(vol).fillna(0.0)
    sp["home"] = sp["DMA"]
    moved = {}
    if how in ("golden", "corr"):
        inflow, _ = B.flows(target)
        a = B.amr(target)
        a["local"] = pd.to_datetime(a["read_start_local"], format="%d/%m/%Y %H:%M")
        # the local clock's repeated autumn hour: the second reading is the GMT hour
        a["rep"] = a.groupby(["logger_id", "local"]).cumcount()
        a["utc"] = [B.local_to_utc(t.to_pydatetime()) for t in a["local"]]
        a.loc[a["rep"] == 1, "utc"] = a.loc[a["rep"] == 1, "utc"] + pd.Timedelta(hours=1)
        a["l_s"] = a["volume_m3"] / 3.6
        for lid, g in a.groupby("logger_id"):
            row = sp[sp["AMR logger"] == lid]
            if row.empty:
                continue
            rec = row["DMA"].iloc[0]
            q = pd.Series(g["l_s"].values, index=pd.to_datetime(g["utc"])).reindex(inflow.index)
            if how == "golden":
                over = int((q > inflow[rec] + 1e-9).sum())
                if over:
                    dq = q.diff()
                    cs = {d: dq.corr(inflow[d].diff()) for d in inflow.columns if d != rec}
                    moved[lid] = (rec, max(cs, key=cs.get), over, cs)
            else:
                cs = {d: q.corr(inflow[d]) for d in inflow.columns}
                best = max(cs, key=cs.get)
                if best != rec:
                    moved[lid] = (rec, best, 0, cs)
        for lid, (rec, new, _, _) in moved.items():
            sp.loc[sp["AMR logger"] == lid, "home"] = new
    out = sp.groupby("home")["vol"].sum() / 1000.0
    ds = districts or sorted(out.index)
    return {d: float(out.get(d, 0.0)) for d in ds}, moved


# ------------------------------------------------------------------------------------------------ the back-test
def turbidity_backtest(target, c=None, rise=0.05, lift=0.12, burn_days=60):
    """Lesson 12: the inlet turbidity record against each flow model. An observed event day at a monitor is a day with
    two consecutive hours whose median reading stands more than `lift` NTU above that monitor's rolling seven-day
    median. A model predicts an event day where a main on the monitor's supply path that hour (lined mains aside)
    passes the highest flow it carried since the year began by more than `rise`, after a burn-in of `burn_days`; an
    observed day counts as explained when the model predicts that monitor a day within one day of it."""
    c = c or call(target)
    net = c["net"]
    tb = B.turbidity(target)
    tb = tb[tb["status"] == "OK"].copy()
    tb["hour"] = tb["t"].dt.floor("h")
    hm = tb.groupby(["dma", "hour"])["ntu"].median().unstack(0)
    base = hm.rolling(24 * 7, min_periods=24, center=True).median()
    start = hm.index[0] + pd.Timedelta(days=burn_days)
    obs = {}
    for d in hm.columns:
        e = (hm[d] - base[d]) > lift
        e2 = e & e.shift(1, fill_value=False)
        obs[d] = {x for x, t in zip(hm.index[e2.values].date, hm.index[e2.values]) if t >= start}
    lined = {m for m, row in net.mains.items() if str(row["Lining"]).startswith("Cement")}

    def predicted(Fm, sets):
        mains = list(Fm.columns)
        vals = Fm.values
        cur = Fm.iloc[:24 * burn_days].max().values.copy()
        fl = np.zeros_like(vals, dtype=bool)
        for i in range(len(vals)):
            fl[i] = (vals[i] > cur * (1 + rise)) & (vals[i] > 5)
            cur = np.maximum(cur, vals[i])
        out = {}
        cache = {}
        for d in hm.columns:
            node = net.dmas[d]["Inlet junction"]
            days = set()
            for i, s in enumerate(sets):
                if not fl[i].any():
                    continue
                if s not in cache:
                    cache[s] = net.paths(s)
                if any(fl[i][mains.index(m)] for m in cache[s][node] if m not in lined):
                    days.add(Fm.index[i].date())
            out[d] = days
        return out

    po = predicted(c["F"], c["sets"])
    pn = predicted(c["N0"], [net.normal()] * len(c["N0"]))
    n_obs = sum(len(v) for v in obs.values())
    near = lambda x, days: any(abs((x - y).days) <= 1 for y in days)
    hit = lambda pr: sum(sum(near(x, pr[d]) for x in obs[d]) for d in obs) / max(n_obs, 1)
    july = lambda pr, d: {x for x in pr[d] if x.month == 7}
    t109 = [d for d in hm.columns if net.dmas[d]["Inlet junction"] in ("North Lodge", "Highfield Top")]
    false_nm = sum(len(july(pn, d) - obs[d]) for d in t109)
    false_op = sum(len(july(po, d) - obs[d]) for d in t109)
    return dict(obs=obs, pred_op=po, pred_nm=pn, n_obs=n_obs, recall_op=hit(po), recall_nm=hit(pn), false_nm=false_nm,
                false_op=false_op, sites=t109)
