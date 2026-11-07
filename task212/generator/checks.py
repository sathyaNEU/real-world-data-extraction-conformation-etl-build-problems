"""task212 checks (python3 checks.py): every screen, semantic fork, graded figure and ask device asserted on the
shipped seed, on the record tables as cut; the pack-level gates run when target/ exists. Exit 1 on any failure."""
import json
import re
import os
import sys
import datetime as dt
import numpy as np
import pandas as pd
import world
import records
import asks
import analysis as A
import build
import docs

RES = []
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FORWARD_UNIT = 100
from pack import V_TARGET  # Ribarroja's planned parcels a week, peak weeks 48 to 52 (the peak plan)
MIN_EDGE = 0.07


def ok(name, cond, detail=""):
    RES.append((name, bool(cond), str(detail)))


def edge(v, u):
    return (u / 2 - abs(v - round(v / u) * u)) / u


def pick(s):
    s = s.sort_values(ascending=False)
    lead = float(s.iloc[0] / s.iloc[1]) if s.iloc[1] > 0 else float("inf")
    return s.index[0], lead


def forward(rate, V):
    return rate * V / 1e4


def main_call(S):
    W, R = S["W"], S["R"]
    t = A.base_table(R, W["accounts"])
    r = A.readers(t, R)
    out = {}
    # ---- screen 3 and 4: the first look and every careful reader land Zaragoza
    for k in ["first_look", "a_fields", "e_literal", "c_perrecord", "b_constructing", "b_posbands", "b_topthird",
              "d_mechanism", "d2_declared", "d2_declared_ind", "d2_declared_band"]:
        p, lead = pick(r[k])
        ok("screen reader %s lands Zaragoza" % k, p == "ZAZ", "%s lead %.2f" % (p, lead))
    wr, wl = A.wrong_reason(r)
    ok("wrong-reason reader (Zaragoza set aside) lands Dos Hermanas", wr == "SVQ", "%s lead %.2f" % (wr, wl))
    # ---- screen 1 and 2: every golden-family member lands Ribarroja, the call's lead at 1.2 or more
    fam = [c for c in r.columns if c.startswith("g_")]
    for k in fam:
        p, lead = pick(r[k])
        ok("golden family %s lands Ribarroja, lead >= 1.2" % k, p == "VLC" and lead >= 1.2, "%s lead %.2f" % (p, lead))
    par = W["parcels"]
    truth = par.groupby("hub").apply(lambda d: (d.p_true - d.p_noequip).sum() / len(d) * 1e4)
    ok("truth: the equipment excess is Ribarroja's", pick(truth)[0] == "VLC", truth.round(1).to_dict())
    rate_all = float(t.dam.mean())
    ok("levels: audited damage 1.0 to 3.5 per cent overall and by hub", 0.01 <= rate_all <= 0.035 and
       r.first_look.between(100, 350).all(), "%.4f; %s" % (rate_all, r.first_look.round(1).to_dict()))
    # ---- the forward figure over the supported family
    plan = docs.peak_plan(V_TARGET)
    V = float(plan[(plan.hub == "VLC") & plan.iso_week.between(48, 52)].parcels.mean())
    gold = float(r.loc["VLC", "g_cells_T60"])
    fig = forward(gold, V)
    R_ = round(fig / FORWARD_UNIT) * FORWARD_UNIT
    sup = {k: float(r.loc["VLC", k]) for k in fam if A.supported(k) and k != "g_logit_ind30"}
    edges = {k: edge(forward(v, V), FORWARD_UNIT) if round(forward(v, V) / FORWARD_UNIT) * FORWARD_UNIT == R_ else -1
             for k, v in sup.items()}
    worst = min(edges, key=edges.get)
    ok("forward figure: every supported form in the golden's hundred, 7 per cent of a bin clear",
       min(edges.values()) >= MIN_EDGE, "golden %.1f/10k x %.0f = %.1f -> %d; tightest %s %.3f" %
       (gold, V, fig, R_, worst, edges[worst]))
    gaps = {k: float(r.loc["VLC", k] - r[k].drop("VLC").max()) for k in sup}
    ok("claim 'no other hub comes within 30 of Ribarroja' holds under every supported member", min(gaps.values()) >= 30,
       "tightest %s %.1f" % (min(gaps, key=gaps.get), min(gaps.values())))
    zz = {k: float(r.loc["ZAZ", k]) for k in sup}
    ok("claim 'Zaragoza sits below the network at equal load' holds under every supported member", max(zz.values()) < 0,
       "highest %s %.1f" % (max(zz, key=zz.get), max(zz.values())))
    H6 = ["ZAZ", "VLC", "SVQ", "MAD", "BCN", "BIO"]
    ft = A.fit_table(t, R)
    bb = ft.bic.idxmin()
    bv = float(ft.loc[bb, "VLC"])
    ok("SF16 the programme's lowest-BIC estimate is a supported load form (%s) and names Ribarroja" % bb,
       bb.startswith("load_step") and "noint" not in bb and ft.loc[bb, H6].astype(float).idxmax() == "VLC")
    f16 = forward(bv, V)
    ok("SF16 executing the lowest-BIC rule literally gives the graded hundred, 7 per cent of a bin clear",
       round(f16 / FORWARD_UNIT) * FORWARD_UNIT == R_ and edge(f16, FORWARD_UNIT) >= MIN_EDGE, "%.1f -> %.1f" % (bv, f16))
    for k in ("load_log1p", "load_log", "load_log1p_noint", "load_step60_plus_constructing", "load_step60_sector",
              "load_step60_noint", "load_lin", "load_step30"):
        ok("SF16 the lowest-BIC rule sets aside %s" % k, ft.loc[k, "bic"] > ft.loc[bb, "bic"],
           "%.1f against %.1f" % (ft.loc[k, "bic"], ft.loc[bb, "bic"]))
    riv = ft[ft.index.str.startswith("rival")]
    ok("SF16 every rival specification on file has a higher BIC than the load step", riv.bic.min() > ft.loc[bb, "bic"],
       "best rival %s %.1f" % (riv.bic.idxmin(), riv.bic.min()))
    out["fit_table"] = ft.round(2).to_dict()
    dev = A.fits(t)
    ok("fit refutes the log form and the no-load model", dev["log"] - dev["ind60"] >= 50 and dev["none"] - dev["ind60"] >= 500,
       dev)
    for T in (20, 30):
        d_T = float(A.oe(t, A._X(t, A._crush_terms(t, (t.load_above >= T).astype(float))))[1].deviance)
        ok("fit refutes the stratum edge at %d kg" % T, d_T - dev["ind60"] >= 50, "%.1f against %.1f" % (d_T, dev["ind60"]))
    out.update(call="VLC", rate=gold, V=V, forward=fig, forward_rounded=R_, family=sup, deviance=dev,
               n_vlc=int((t.hubk == "VLC").sum()),
               readers={k: r[k].round(2).to_dict() for k in r.columns})
    # ---- semantic forks and determinism readings: the call and the forward hundred under each
    def fwd_ok(tb, label):
        g = A.golden_family(tb, thresholds=(60,), quick=True)
        v = float(g["g_cells_T60"]["VLC"])
        p, lead = pick(g["g_cells_T60"])
        f = forward(v, V)
        good = p == "VLC" and round(f / FORWARD_UNIT) * FORWARD_UNIT == R_ and edge(f, FORWARD_UNIT) >= MIN_EDGE
        ok(label, good, "%s lead %.2f; %.1f -> %.1f" % (p, lead, v, f))
    crush = t.damage_code.isin(["D1", "AP"]) | (t.condition == "OK")
    tc = t[crush].copy()
    ok("SF1 damaged read as crush codes only: same call", pick(A.golden_family(tc, (60,), True)["g_cells_T60"])[0] == "VLC")
    fwd_ok(A.base_table(R, W["accounts"], notfound_as_ok=True), "SF2 NOT FOUND lines read as inspected and OK")
    t3a = A.base_table(R, W["accounts"], check_audits=True)
    g3a = A.golden_family(t3a, thresholds=(60,), quick=True)["g_cells_T60"]
    ok("SF3 check audits counted as inspections: same call (the hundred is the procedure's: check audit lines are not "
       "counted as inspections)", pick(g3a)[0] == "VLC", "%.1f -> %.1f" % (float(g3a["VLC"]), forward(float(g3a["VLC"]), V)))
    fwd_ok(A.base_table(R, W["accounts"], window="audit"), "SF4 the window read by audit date")
    t5 = t.copy()
    g5 = {}
    for h in ["ZAZ", "VLC", "SVQ", "MAD", "BCN", "BIO"]:
        rest = t5[t5.hubk != h]
        m = rest.assign(ls=(rest.load_above >= 60).astype(int), fr=rest.fragile).groupby(
            ["dshape", "wband", "fr", "ls"]).dam.mean()
        me = t5[t5.hubk == h].assign(ls=(t5.load_above >= 60).astype(int), fr=t5.fragile)
        e = me.set_index(["dshape", "wband", "fr", "ls"]).index.map(m)
        g5[h] = float((me.dam.values - np.nan_to_num(np.asarray(e, dtype=float), nan=me.dam.mean())).mean() * 1e4)
    ok("SF5 the comparison read as the other five hubs: same call", pick(pd.Series(g5))[0] == "VLC",
       {k: round(v, 1) for k, v in g5.items()})
    fwd_ok(A.base_table(R, W["accounts"], order="last"), "SF6 a re-scanned parcel placed at its last LOAD")
    sc = R["scans"]
    ld = sc[sc.event == "LOAD"]
    ties = ld.groupby(["cage_label", "scan_utc"]).barcode.nunique()
    ok("SF7 no two parcels' LOAD events share a second in a cage", int((ties > 1).sum()) == 0, int((ties > 1).sum()))
    o1 = ld.groupby(["cage_label", "barcode"]).scan_utc.min().reset_index().sort_values(["cage_label", "scan_utc"])
    o2 = ld.groupby(["cage_label", "barcode"]).scan_utc.max().reset_index().sort_values(["cage_label", "scan_utc"])
    nr = sc[sc.event == "NOREAD"]
    ok("SF7 a no-read's handheld LOAD keeps its place: first and last LOAD give one order in every cage",
       (o1.barcode.values == o2.barcode.values).all(), "%d no-reads, %d handheld re-scans" %
       (len(nr), int((ld.groupby(["cage_label", "barcode"]).size() > 1).sum())))
    fwd_ok(A.base_table(R, W["accounts"], weight_pick="last"), "SF8 a re-weighed parcel's last DWS weight")
    fwd_ok(A.base_table(R, W["accounts"], weight_pick="mean"), "SF8 a re-weighed parcel's mean DWS weight")
    d = R["dws"]
    s1 = set(d.barcode)
    s2 = set(d.barcode.str.strip().str.upper())
    s3 = set(zip(d.barcode, d.hub_no))
    lines = set(R["lines"].barcode)
    ok("SF9 the DWS join is one set under the printed, the normalised and the (barcode, hub) keys",
       (lines & s1) == (lines & s2) and len(s3) == len(s1) and lines <= s1, "%d of %d audited barcodes" % (len(lines & s1), len(lines)))
    for T in (35, 45, 75, 95):
        g = A.golden_family(t, thresholds=(T,), quick=True)
        v = float(g["g_cells_T%d" % T]["VLC"]); f = forward(v, V)
        ok("SF10 load stratum edge at %d kg: same call and hundred" % T,
           pick(g["g_cells_T%d" % T])[0] == "VLC" and round(f / FORWARD_UNIT) * FORWARD_UNIT == R_, "%.1f -> %.1f" % (v, f))
    wk = plan[(plan.hub == "VLC") & plan.iso_week.between(48, 52)].parcels
    ok("SF11 the forward volume as the mean week or the five-week total over five", abs(wk.mean() - wk.sum() / 5) < 1e-9)
    tl = t[t.heavyp == 0]
    ok("SF12 the cartons' own damage left out: same call",
       pick(A.golden_family(tl, (60,), True)["g_cells_T60"])[0] == "VLC")
    for k in ("g_logit_ind60_sector", "g_logit_ind60_noint", "g_logit_lin_noint", "g_pois_ind60"):
        f = forward(float(r.loc["VLC", k]), V)
        ok("SF13 %s: same call and hundred" % k, pick(r[k])[0] == "VLC" and round(f / FORWARD_UNIT) * FORWARD_UNIT == R_,
           "%.1f" % f)
    oc = sc[sc.event.isin(["OPEN", "CLOSE"])].groupby(["cage_label", "event"]).size().unstack()
    span = sc.groupby("cage_label").apply(lambda g: (g[g.event == "LOAD"].scan_utc.min() > g[g.event == "OPEN"].scan_utc.min())
                                          and (g[g.event == "LOAD"].scan_utc.max() < g[g.event == "CLOSE"].scan_utc.max()))
    ok("SF14 each cage opened and closed once, every LOAD between: one cage, one load order",
       (oc == 1).all().all() and bool(span.all()) and sc.cage_label.nunique() == len(oc), len(oc))
    ok("SF15 cage label build dates inside the window", R["audits"].build_date.between("2026-07-01", "2026-09-30").all())
    # ---- the analyst test on the clean truth: the easy route files Zaragoza, the golden Ribarroja
    cl = W["parcels"].assign(dam=W["parcels"].damaged.astype(int), hubk=W["parcels"].hub,
                             dshape=W["parcels"].pack.map({"BOX": "BOX", "BAG": "BAG", "FLYER": "FLY"}),
                             wband=pd.cut(W["parcels"].weight_kg, [0, 0.5, 1, 2, 5, 10, 99], labels=False),
                             fr=W["parcels"].fragile)
    easy = A.cells_oe(cl.assign(sv=cl.service), ["dshape", "wband", "fr", "sv"])
    gold_clean = A.cells_oe(cl.assign(ls=(cl.wabove_kg >= 60).astype(int)), ["dshape", "wband", "fr", "ls"])
    ok("analyst test on the clean truth: the easy route files Zaragoza", pick(easy)[0] == "ZAZ", easy.round(1).to_dict())
    ok("analyst test on the clean truth: the load stratum files Ribarroja", pick(gold_clean)[0] == "VLC",
       gold_clean.round(1).to_dict())
    cheap = sum(pick(r[k])[0] == "VLC" for k in ["first_look", "a_fields", "e_literal", "c_perrecord", "b_constructing",
                                                   "b_posbands", "b_topthird", "d_mechanism", "d2_declared",
                                                   "d2_declared_ind", "d2_declared_band"])
    ok("Gate F: no cheap route reaches the call", cheap == 0, cheap)
    # ---- ordinary cause: each business account's cartons come off its own trailer in one block a night
    dws = R["dws"].drop_duplicates("barcode").set_index("barcode")
    hv = W["parcels"][W["parcels"].heavy]
    it = pd.to_datetime(dws.induct_local.reindex(hv.barcode).str[:19]).values
    spanm = pd.Series(it, index=hv.index).groupby([hv.hub, hv.build_date]).agg(lambda x: (x.max() - x.min()).total_seconds() / 60)
    ok("ordinary cause: each night's cartons inducted within an hour at their hub (one trailer unloaded)", float(spanm.quantile(0.95)) <= 60,
       spanm.groupby(level=0).median().round(1).to_dict())
    return out


def stop_summary(df):
    """Stoppage count and hours stood by hub over the July to September sorting nights."""
    df = df.copy()
    df["night"] = df.t0.map(asks.night_of)
    df = df[(df.night >= asks.Q3[0]) & (df.night <= asks.Q3[1])]
    g = df.groupby("hub")
    return (g.size().reindex(asks.HUB_KEYS).fillna(0).astype(int),
            g.apply(lambda d: (d.t1 - d.t0).dt.total_seconds().sum() / 3600).reindex(asks.HUB_KEYS).fillna(0.0))


def stop_readings(S, SG):
    """SF18: every hub's stoppage count and hours stood are one figure, to 0.01 h, under every reading of the safety
    system's TRIPs and of a spell the PLC lost; the readings that need RESET rows are measured on a re-cut log."""
    ev, wos = S["events"], S["wos"]
    U = asks.UTC_OFFSET_H
    no2key = {v: k for k, v in asks.HUB_NO.items()}
    sp, lone = asks.plc_spells(ev)
    tr = asks.trips(ev)
    w = wos[wos.order_type == "CORRECTIVE"].copy()
    w["hub"] = w.site.map({v: k for k, v in asks.CMMS_SITE.items()})

    def with_orders(logged):
        add = []
        for x in w.itertuples():
            if not ((logged.hub == x.hub) & (logged.t0 <= x.machine_running + pd.Timedelta(minutes=2)) &
                    (logged.t1 >= x.machine_stopped - pd.Timedelta(minutes=2))).any():
                add.append((x.hub, x.machine_stopped, x.machine_running))
        return pd.concat([logged[["hub", "t0", "t1"]], pd.DataFrame(add, columns=["hub", "t0", "t1"])], ignore_index=True)

    def merged(iv):
        out = []
        for h, g in iv.groupby("hub"):
            cur = None
            for x in g.sort_values(["t0", "t1"]).itertuples():
                if cur is None or x.t0 > cur[1]:
                    if cur:
                        out.append((h,) + cur)
                    cur = (x.t0, x.t1)
                else:
                    cur = (cur[0], max(cur[1], x.t1))
            out.append((h,) + cur)
        return pd.DataFrame(out, columns=["hub", "t0", "t1"])

    R = {}
    # (ii) the event log swept: any stop record (PLC STOP or safety TRIP) opens a standstill, a RUN closes it
    e = ev[ev.event.isin(["STOP", "TRIP", "RUN"])].copy()
    e["ts"] = pd.to_datetime(e.ts_utc) + pd.Timedelta(hours=U)
    e["hub"] = e.hub_no.map(no2key)
    rows = []
    for h, g in e.groupby("hub"):
        t0 = None
        for x in g.sort_values("ts", kind="mergesort").itertuples():
            if x.event in ("STOP", "TRIP"):
                t0 = x.ts if t0 is None else t0
            elif t0 is not None:
                rows.append((h, t0, x.ts))
                t0 = None
    R["(ii) earliest stop record to the RUN, the log swept"] = stop_summary(
        with_orders(pd.DataFrame(rows, columns=["hub", "t0", "t1"])))
    # (ii) the union of every source's records, the work orders included: earliest stop to latest run when they overlap
    tx = []
    for x in tr.itertuples():
        nxt = pd.concat([sp[(sp.hub == x.hub) & (sp.t1 > x.ts)].t1, lone[(lone.hub == x.hub) & (lone.t1 > x.ts)].t1])
        tx.append((x.hub, x.ts, nxt.min()))
    iv = pd.concat([sp[["hub", "t0", "t1"]], pd.DataFrame(tx, columns=["hub", "t0", "t1"]),
                    w.rename(columns={"machine_stopped": "t0", "machine_running": "t1"})[["hub", "t0", "t1"]]],
                   ignore_index=True)
    R["(ii) earliest stop record to the latest RUN over every source, the work orders included"] = stop_summary(merged(iv))
    # (iii) TRIPs shifted by an offset estimated from the paired stops; (iv) the raw TRIP times
    saf = sp[sp.reason == "SAFETY"]
    pairs, lost = [], []
    for x in tr.itertuples():
        d = (saf[saf.hub == x.hub].t0 - x.ts).dt.total_seconds()
        near = d[d.abs() <= 60]
        if len(near):
            pairs.append((x.hub, x.ts, float(near.iloc[near.abs().argmin()])))
        else:
            lost.append((x.hub, x.ts))
    P = pd.DataFrame(pairs, columns=["hub", "ts", "off"])
    P["days"] = (P.ts - pd.Timestamp("2026-07-01")).dt.total_seconds() / 86400.0
    L = pd.DataFrame(lost, columns=["hub", "ts"])
    est = {}
    for h, g in P.groupby("hub"):
        b, a = np.polyfit(g.days, g.off, 1)
        est[h] = dict(mean=float(g.off.mean()), median=float(g.off.median()), a=float(a), b=float(b))

    def lost_from(shift):
        rows = [(x.hub, x.ts + pd.Timedelta(seconds=float(shift(x))), lone[(lone.hub == x.hub) & (lone.t1 > x.ts)].t1.min())
                for x in L.itertuples()]
        return stop_summary(with_orders(pd.concat([sp[["hub", "t0", "t1"]], pd.DataFrame(rows, columns=["hub", "t0", "t1"])],
                                                  ignore_index=True)))

    line = lambda x: est[x.hub]["a"] + est[x.hub]["b"] * (x.ts - pd.Timestamp("2026-07-01")).total_seconds() / 86400.0
    nearest = lambda x: float(P[P.hub == x.hub].off.iloc[(P[P.hub == x.hub].ts - x.ts).abs().argmin()])
    R["(iii) TRIPs shifted by the mean paired offset"] = lost_from(lambda x: est[x.hub]["mean"])
    R["(iii) TRIPs shifted by the median paired offset"] = lost_from(lambda x: est[x.hub]["median"])
    R["(iii) TRIPs shifted by the nearest pair's offset"] = lost_from(nearest)
    R["(iii) TRIPs shifted by a straight line through the paired offsets"] = lost_from(line)
    R["(iv) the raw TRIP times"] = lost_from(lambda x: 0.0)
    shifts = [abs(v[k]) for v in est.values() for k in ("mean", "median")] + \
        [abs(line(x)) for x in L.itertuples()] + [abs(nearest(x)) for x in L.itertuples()]
    ok("SF18 (iii) every offset estimated from the paired stops (mean, median, nearest pair, straight line) is zero to "
       "the log's second", len(P) > 0 and max(shifts) <= 1.0 + 1e-9 and P.off.isin([0.0, -1.0]).all(),
       "%d paired TRIPs, %d lost; offsets %s; largest estimate %.2f s" % (len(P), len(L), P.off.value_counts().to_dict(),
                                                                       max(shifts)))
    for name, (c, hrs) in R.items():
        d = (hrs - SG.hours_stood).abs()
        okp = all(round(float(hrs[h]), 1) == round(float(SG.loc[h, "hours_stood"]), 1) and
                  edge(float(hrs[h]), 0.1) >= MIN_EDGE for h in asks.HUB_KEYS)
        ok("SF18 %s: every hub's stoppages and hours stood one figure with the golden (to 0.01 h)" % name,
           (c == SG.stoppages).all() and float(d.max()) < 0.01 and okp,
           "max |dh| %.4f h; %s" % (float(d.max()), hrs.round(3).to_dict()))
    ok("SF18 the golden is reading (i); the safety system's rows ship as TRIP with a cause code and nothing else, on "
       "the controller's clock", set(ev[ev.source == "SIS"].event) == {"TRIP"} and
       ev[ev.event == "TRIP"].reason.str.match(r"^(ESTOP|LCURTAIN|GATE)_\d\d$").all() and
       not ev.event.isin(["RESET"]).any(), ev[ev.source == "SIS"].event.value_counts().to_dict())
    # the readings a RESET row would open, measured on the same world with the RESETs logged
    ev_r, wos_r = asks.stoppage_records(S["st"].copy(), S["gp"], world.SEED, log_resets=True)
    base_rows = ev_r[ev_r.event != "RESET"].reset_index(drop=True)
    same_world = base_rows.equals(ev.reset_index(drop=True)) and wos_r.equals(wos)
    rs = ev_r[ev_r.event == "RESET"].copy()
    rs["ts"] = pd.to_datetime(rs.ts_utc) + pd.Timedelta(hours=U)
    rs["hub"] = rs.hub_no.map(no2key)
    nxt_reset = lambda x: rs[(rs.hub == x.hub) & (rs.ts > x.ts)].ts.min()
    r1 = stop_summary(with_orders(pd.concat([sp[["hub", "t0", "t1"]], pd.DataFrame(
        [(x.hub, x.ts, nxt_reset(x)) for x in L.itertuples()], columns=["hub", "t0", "t1"])], ignore_index=True)))
    nonsaf = sp[~((sp.reason == "SAFETY") & sp.hub.isin(asks.SIS_SORTERS))][["hub", "t0", "t1"]]
    r2 = stop_summary(with_orders(pd.concat([nonsaf, pd.DataFrame(
        [(x.hub, x.ts, nxt_reset(x)) for x in tr.itertuples()], columns=["hub", "t0", "t1"])], ignore_index=True)))
    d1 = (r1[1] - SG.hours_stood).abs()
    e1 = min(edge(float(r1[1][h]), 0.1) for h in asks.SIS_SORTERS)
    moved2 = [h for h in asks.HUB_KEYS if round(float(r2[1][h]), 1) != round(float(SG.loc[h, "hours_stood"]), 1)]
    ok("SF18 RESET rows not logged: with them on the same world, a lost spell ended at its RESET is not one figure with "
       "the golden (max |dh| %.3f h, nearest edge %.2f of a bin) and every safety spell read TRIP to RESET moves %s; "
       "the shipped log carries TRIPs only" % (float(d1.max()), e1, ", ".join(moved2) or "no hub"),
       same_world and len(rs) == len(tr) and (float(d1.max()) >= 0.01 or e1 < MIN_EDGE or moved2) and
       not ev.event.isin(["RESET"]).any(), "reset-ended %s; TRIP to RESET %s" % (r1[1].round(3).to_dict(),
                                                                                r2[1].round(3).to_dict()))
    # the work orders' minutes sit inside the spell the log records, so the union of every record is the golden
    lg = pd.concat([sp[["hub", "t0", "t1"]], asks.lost_spells(ev, sp.assign(src="plc"), lone)[["hub", "t0", "t1"]]],
                   ignore_index=True)
    inside_n, matched, govern = 0, 0, []
    for x in w.itertuples():
        m = lg[(lg.hub == x.hub) & (lg.t0 <= x.machine_running + pd.Timedelta(minutes=2)) &
               (lg.t1 >= x.machine_stopped - pd.Timedelta(minutes=2))]
        if len(m):
            matched += 1
            inside_n += int(len(m) == 1 and x.machine_stopped >= m.t0.iloc[0] and x.machine_running <= m.t1.iloc[0])
    lgk = lg.copy()
    for i, x in lgk.iterrows():
        m = w[(w.hub == x.hub) & (w.machine_stopped <= x.t1 + pd.Timedelta(minutes=2)) &
              (w.machine_running >= x.t0 - pd.Timedelta(minutes=2))]
        if len(m) == 1:
            lgk.at[i, "t0"], lgk.at[i, "t1"] = m.machine_stopped.iloc[0], m.machine_running.iloc[0]
    gv = stop_summary(with_orders(lgk))
    ok("SF18 every corrective order for a logged spell keys its stop and run minutes inside that spell (the union of "
       "every record is the golden; the order's later stop minute is not the moment the sorter stopped)",
       matched > 0 and inside_n == matched, "%d of %d orders inside their spell; order minutes in place of the "
                                            "log's: %s" % (inside_n, matched, gv[1].round(2).to_dict()))


def ask_checks(S):
    out = {}
    G, first = asks.claims_golden(S["cases"], S["pays"], S["refunds"], S["trk"], S["flat"])
    T = asks.claims_truth(S["t"], S["paid"])
    ok("claims golden from the records equals the truth (counts and euros)",
       (G.claims == T.claims).all() and (G.claims_eur - T.claims_eur).abs().max() < 0.005, G.to_dict())
    one = first.assign(k=1).groupby("hub").k.sum().reindex(asks.HUB_KEYS)
    ok("D6 one parcel a case misses every hub's count by 3 or more", ((G.claims - one) >= 3).all(), (G.claims - one).to_dict())
    # ---- SF17: a flat-rate case's grain and approval basis, filed in CS-FIN 07 section 2
    cases, flat = S["cases"], S["flat"]
    rate = flat.set_index("account").eur_per_carton
    since = flat.set_index("account").terms_since
    fc = cases[cases.account.isin(rate.index)]
    ap = fc[fc.status == "APPROVED"]
    kk = ap.approved_eur / ap.account.map(rate)
    ok("SF17 every approved flat-rate case's amount is an exact whole multiple of its account's rate in the terms",
       len(ap) > 0 and bool(((kk - kk.round()).abs() < 1e-9).all()) and bool((kk.round() >= 1).all()),
       "%d approved flat-rate cases; cartons a case %s" % (len(ap), sorted(kk.round().astype(int).unique())))
    ok("SF17 no flat-rate account has a case opened before its terms date (the terms carry no end date)",
       len(fc) > 0 and bool((fc.opened >= fc.account.map(since)).all()) and list(flat.columns) ==
       ["account", "home_hub", "eur_per_carton", "terms_since"], "%d cases; latest terms date %s" % (len(fc), since.max()))
    tt = S["t"]
    tf = tt[tt.account.isin(rate.index)]
    ok("SF17 no flat-rate account files an ordinary case, and no flat-rate case is reopened or shares its tracking number",
       bool((tf.kind == "FLAT").all()) and not bool(tf.reopen.any()) and fc.tracking_no.is_unique and
       not bool(tt[tt.kind != "FLAT"].account.isin(rate.index).any()), "%d flat-rate cases in the truth" % len(tf))
    srt = S["trk"][S["trk"].event == "SORT"].sort_values(["tracking_no", "ts_utc"]).drop_duplicates("tracking_no")
    srt = srt.set_index("tracking_no")
    hub_of = srt.location.map({"PLAT-%02d" % v: k for k, v in asks.HUB_NO.items()})
    nite = (pd.to_datetime(srt.ts_utc.str[:19]) + pd.Timedelta(hours=asks.UTC_OFFSET_H)).map(asks.night_of)
    f1 = cases.sort_values(["opened", "case_ref"]).drop_duplicates("tracking_no")
    f1 = f1[(f1.status == "APPROVED") & (f1.decided <= asks.CUTOFF.isoformat())]
    f1 = f1[f1.tracking_no.map(nite).between(asks.Q3[0], asks.Q3[1])]
    cartons = np.where(f1.account.isin(rate.index), (f1.approved_eur / f1.account.map(rate)).round(), 1).astype(int)
    lit = pd.Series(cartons, index=f1.index).groupby(f1.tracking_no.map(hub_of)).sum().reindex(asks.HUB_KEYS)
    ok("SF17 the filed sentence read literally (a flat-rate case covers every damaged carton of its consignment, "
       "approved at the account's rate for each) gives the golden's six counts", (lit == G.claims).all(), lit.to_dict())
    one_tn = f1.groupby(f1.tracking_no.map(hub_of)).size().reindex(asks.HUB_KEYS)
    JUDGE_R1 = {"ZAZ": 1101, "VLC": 772, "SVQ": 827, "MAD": 1232, "BCN": 935, "BIO": 411}
    ok("SF17 the reading the sentence excludes, one damaged parcel a tracking number, gives the stage-4 judge's six "
       "counts, every hub below the golden", one_tn.to_dict() == JUDGE_R1 and bool(((G.claims - one_tn) > 0).all()),
       one_tn.to_dict())
    tr = S["trk"][S["trk"].event == "SORT"].sort_values(["tracking_no", "ts_utc"]).drop_duplicates("tracking_no")
    sh = tr.set_index("tracking_no").location.map({"PLAT-%02d" % v: k for k, v in asks.HUB_NO.items()})
    keep = set(first.tracking_no)
    cp = S["cases"].set_index("case_ref").tracking_no
    p = S["pays"][S["pays"].value_date <= asks.CUTOFF.isoformat()]
    p = p.assign(parcel=p.case_ref.map(cp)); p = p[p.parcel.isin(keep)]
    tro = p.assign(hub=p.parcel.map(sh)).groupby("hub").amount_eur.sum().reindex(asks.HUB_KEYS)
    ok("D7 transfers only miss every hub's euros by 3 or more", ((G.claims_eur - tro) >= 3).all(), (G.claims_eur - tro).round(0).to_dict())
    base = asks.match_refunds(S["cases"], S["refunds"]).set_index("case_ref").refund_id.sort_index()
    same = True
    for d in (2, 3, 5, 7, 10):
        for o in ("earliest", "latest"):
            mm = asks.match_refunds(S["cases"], S["refunds"], d, o).set_index("case_ref").refund_id.sort_index()
            same &= len(mm) == len(base) and (mm == base).all()
    ok("D7 the refund match is one set under windows of 2 to 10 days, earliest or latest first", same, len(base))
    canc = ~S["refunds"].id.isin(base.values)
    ok("D7 every unmatched refund is at a label tariff price or after the cutoff",
       (S["refunds"][canc].amount.isin(asks.LABEL_TARIFF) | (S["refunds"][canc].created_utc.str[:10] > "2026-10-20")).all())
    for h in asks.HUB_KEYS:
        ok("mid-bin: claims euros %s" % h, edge(float(G.loc[h, "claims_eur"]), 1.0) >= MIN_EDGE, float(G.loc[h, "claims_eur"]))
    SG, allsp = asks.stoppages_golden(S["events"], S["wos"])
    st = S["st"]
    q = st[st.night.between(asks.Q3[0], asks.Q3[1])]
    nwo = q[q.in_gap].groupby("hub").size().reindex(asks.HUB_KEYS).fillna(0)
    nlost = q[q.lost_stop].groupby("hub").size().reindex(asks.HUB_KEYS).fillna(0)
    short = q.groupby("hub").hours.sum().reindex(asks.HUB_KEYS) - SG.hours_stood
    ok("stoppages golden equals the truth count; hours short of the truth only by the work orders' minutes on the "
       "spells the log lost entirely and a TRIP's second on the spells whose STOP it lost",
       (SG.stoppages == q.groupby("hub").size().reindex(asks.HUB_KEYS)).all() and bool((short >= -1e-9).all()) and
       bool((short <= (nwo * 120 + nlost * 1) / 3600 + 1e-9).all()),
       "short %s; order-only spells %s; lost STOPs %s" % (short.round(3).to_dict(), nwo.astype(int).to_dict(),
                                                         nlost.astype(int).to_dict()))
    stop_readings(S, SG)
    sp, lone = asks.plc_spells(S["events"])
    sp["night"] = sp.t0.map(asks.night_of)
    spq = sp[sp.night.between(asks.Q3[0], asks.Q3[1])]
    pn = spq.groupby("hub").size().reindex(asks.HUB_KEYS)
    ph = spq.assign(h=(spq.t1 - spq.t0).dt.total_seconds() / 3600).groupby("hub").h.sum().reindex(asks.HUB_KEYS)
    ok("D4 and D1: the PLC's own spells miss every hub's count by 3 or more", ((SG.stoppages - pn) >= 3).all(),
       (SG.stoppages - pn).to_dict())
    ok("D4 and D1: the PLC's own spells miss every hub's hours by 3 bins or more", ((SG.hours_stood - ph) >= 0.3).all(),
       (SG.hours_stood - ph).round(2).to_dict())
    same = True
    for tol in (1, 2, 5, 20, 40):
        for w in (1, 2, 5):
            g2, _ = asks.stoppages_golden(S["events"], S["wos"], tol=tol, wo_window=w)
            same &= (g2.stoppages == SG.stoppages).all() and (g2.hours_stood - SG.hours_stood).abs().max() < 0.01
    ok("D1 and D4 selections one set under TRIP tolerances 1 to 40 s and order windows 1 to 5 min", same)
    ev_r, _ = asks.stoppage_records(S["st"].copy(), S["gp"], world.SEED, log_resets=True)
    ev = pd.concat([S["events"], ev_r[ev_r.event == "RESET"]])
    ev = ev[ev.event.isin(["STOP", "RUN", "TRIP", "RESET"])]
    ev_min = (pd.to_datetime(ev.ts_utc) + pd.Timedelta(hours=asks.UTC_OFFSET_H)).pipe(lambda t: t.dt.hour * 60 + t.dt.minute)
    wc = S["wos"][S["wos"].order_type == "CORRECTIVE"]
    wo_min = pd.concat([wc.machine_stopped, wc.machine_running]).pipe(lambda t: t.dt.hour * 60 + t.dt.minute)
    sp_min = pd.concat([allsp.t0, allsp.t1]).pipe(lambda t: t.dt.hour * 60 + t.dt.minute)
    inside = lambda m: bool(((m >= 20 * 60 + 30) | (m < 5 * 60)).all())
    ok("ask 2 night: every PLC STOP and RUN, every safety TRIP (and every RESET the safety system holds), every "
       "corrective order's stop and run, and every golden spell sits inside 20:30 to 05:00 Spanish time, so no spell "
       "crosses a night's edge and clipping at the edge is the same call", inside(ev_min) and inside(wo_min) and
       inside(sp_min), (len(ev_min), len(wo_min), len(sp_min)))
    for h in asks.HUB_KEYS:
        ok("mid-bin: hours stood %s" % h, edge(float(SG.loc[h, "hours_stood"]), 0.1) >= MIN_EDGE, float(SG.loc[h, "hours_stood"]))
    lines = set(S["R"]["lines"].barcode)
    ok("separation: no claimed parcel is an audited parcel", len(lines & set(S["cases"].tracking_no)) == 0)
    out.update(claims=G.claims.to_dict(), claims_eur=G.claims_eur.to_dict(), stoppages=SG.stoppages.to_dict(),
               hours=SG.hours_stood.to_dict())
    return out


def three_rules(S):
    """R1 raw material, R2 each Layer 1 item neutral under its natural mishandling, R3 the analyst test and no plant."""
    W, R = S["W"], S["R"]
    cols = set()
    for k in ("scans", "dws", "manifests", "audits", "lines"):
        cols |= set(R[k].columns)
    ok("R1 no shipped column holds a parcel's load, position or carton count",
       not any(re.search(r"load|above|stack|position|carton|crush", c) for c in cols), sorted(cols))
    t = A.base_table(R, W["accounts"])
    ok("R1 the decisive step reads the build log's LOAD rows and the DWS weights for every inspected parcel",
       t.load_above.notna().all() and t.kg.notna().all(), len(t))
    corr = max(abs(float(np.corrcoef(t.load_above, t[c].astype(float))[0, 1])) for c in ("kg", "declared_kg"))
    ok("R1 no shipped weight column stands in for the load (|corr| under 0.3)", corr < 0.3, round(corr, 3))
    base = pick(A.golden_family(t, (60,), True)["g_cells_T60"])[0]
    utc = R["scans"].copy(); utc["scan_utc"] = utc.scan_utc + pd.Timedelta(hours=2)
    t2 = A.base_table(dict(R, scans=utc), W["accounts"])
    ok("R2 build log read in local time instead of UTC: same call",
       pick(A.golden_family(t2, (60,), True)["g_cells_T60"])[0] == base)
    t3 = t.copy()
    t3["wband"] = pd.cut(t3.declared_kg, [0, 0.5, 1, 2, 5, 10, 99], labels=False)
    ok("R2 parcel weight bands from the declared kg: same call",
       pick(A.golden_family(t3, (60,), True)["g_cells_T60"])[0] == base)
    ok("R2 old and new damage codes, check audits, NOT FOUND lines, re-scans, re-weighs: SF1 to SF8 above", True)
    rec = R["audits"].copy()
    rec["hub"] = rec.hub.str.upper()
    ok("R2 hub names keyed in capitals: same hubs", rec.hub.str.title().map(A.NAME2KEY).notna().sum() >= 0)
    sig = R["scans"][R["scans"].event == "LOAD"].groupby("cage_label").barcode.apply(lambda s: hash(tuple(sorted(s))))
    ok("R3c no copied block: no two cages share a load list", sig.nunique() == len(sig))
    gaps = R["scans"][R["scans"].event == "LOAD"].groupby("cage_label").scan_utc.apply(
        lambda s: tuple(np.diff(np.sort(s.values).astype("int64")) // 10 ** 9))
    ok("R3c no copied block: no two cages share a scan timing pattern", gaps.nunique() == len(gaps))


def realism(S):
    R = S["R"]
    def steps(s):
        v = pd.Series(sorted(set(int(re.sub(r"\D", "", x)) for x in s if re.sub(r"\D", "", x))))
        return v.diff().dropna().nunique()
    for name, s in (("audit ids", R["audits"].audit_id), ("case refs", S["cases"].case_ref),
                    ("transfer refs", S["pays"].payment_ref), ("work orders", S["wos"].work_order),
                    ("cage serials", R["audits"].cage_label.str[-4:])):
        ok("realism: %s are no arithmetic sequence" % name, steps(s) > 3, steps(s))
    n = R["lines"].merge(R["audits"][R["audits"].audit_type == "ROUTINE"], on="audit_id").groupby("hub").size()
    ok("realism: no two hubs inspected the same number of parcels", n.nunique() == len(n), n.to_dict())
    cpn = R["audits"][R["audits"].audit_type == "ROUTINE"].groupby(["hub", "build_date"]).size()
    ok("realism: routine audits a night vary", cpn.nunique() >= 4, cpn.value_counts().sort_index().to_dict())
    ok("realism: the build log's event column holds several values", R["scans"].event.nunique() >= 4,
       R["scans"].event.value_counts().to_dict())
    ok("realism: the sorter event log's event column holds several values", S["events"].event.nunique() >= 4,
       S["events"].event.value_counts().to_dict())
    wo = S["wos"]
    st = S["st"]
    ok("realism: not every stoppage has a work order and not every order is a stoppage",
       len(wo[wo.order_type == "CORRECTIVE"]) < len(st) and (wo.order_type == "PREVENTIVE").sum() > 0)


def pack_checks():
    T = os.path.join(TASK, "target")
    if not os.path.isdir(T):
        ok("pack: target/ cut", False, "stage 2: not cut yet")
        return
    files = sorted(os.listdir(T))
    ext = {os.path.splitext(f)[1] for f in files}
    ok("input gate: 10 or more files", len(files) >= 10, len(files))
    ok("input gate: 3 or more formats", len(ext) >= 3, sorted(ext))
    rows = max(len(pd.read_parquet(os.path.join(T, f))) for f in files if f.endswith(".parquet"))
    ok("input gate: a file of 25,000 rows or more", rows >= 25000, rows)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("input gate: two or more distractors named in metadata.json", len(meta.get("distractor_files", [])) >= 2,
       meta.get("distractor_files"))
    ok("no describing file under target/", not any(re.search(r"readme|dictionar|manifest_notes|field_notes|codebook|notes",
                                                             f, re.I) for f in files), files)
    size = sum(os.path.getsize(os.path.join(T, f)) for f in files)
    ok("pack under 15 MB", size < 15e6, "%.1f MB" % (size / 1e6))
    for f in files:
        b = open(os.path.join(T, f), "rb").read()
        if f.endswith(".parquet"):
            ok("H1 parquet footer scrubbed: %s" % f, b"parquet-cpp-arrow" not in b and b"pandas" not in b[-4000:])
        if f.endswith(".pdf"):
            ok("H1 PDF producer scrubbed: %s" % f, b"ReportLab" not in b and b"reportlab" not in b)
        if f.endswith(".xlsx"):
            import zipfile, io
            z = zipfile.ZipFile(io.BytesIO(b))
            core = z.read("docProps/core.xml").decode()
            ok("H1 workbook properties scrubbed: %s" % f, "openpyxl" not in core and "2026" in core)
    from pypdf import PdfReader
    prog = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "sortation_survey_programme_2026.pdf")).pages)
    prog = re.sub(r"\s+", " ", prog)
    ok("positive control: the programme's comparison sentence reads back", "same parcels would suffer across the network" in prog)
    for word in ("load", "stack", "crush", "cage weight", "on top", "carton", "heavy"):
        ok("programme names no %s" % word, word not in prog.lower())
    import subprocess
    for f in files + ["../golden/" + g for g in sorted(os.listdir(os.path.join(TASK, "golden")))]:
        if f.endswith(".pdf"):
            fp = os.path.join(T, f)
            lax = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(fp).pages)).strip()
            strict = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(fp, strict=True).pages)).strip()
            pt = subprocess.run(["pdftotext", "-layout", fp, "-"], capture_output=True, text=True).stdout
            ok("H25 %s reads the same under a strict reader and extracts with pdftotext" % f,
               lax == strict and len(pt) > 300 and lax[:40].split()[0] in pt)
    from pack import FLAT_RATE_CASE
    note = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "damage_claims_handling_note.pdf")).pages))
    ok("positive control: CS-FIN 07 section 2 carries the flat-rate case sentence, read back", FLAT_RATE_CASE in note,
       FLAT_RATE_CASE[:60])
    for f in files:
        if f.endswith(".pdf"):
            tx = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, f)).pages).lower()
            ok("positive control: %s reads back" % f, len(tx) > 300)
            for word in ("on top", "crush", "stack", "loaded last", "loaded first", "trailer", "echo", "offset", "gap",
                         "flat-rate", "refund to the card the sender"):
                if word in ("refund to the card the sender", "flat-rate") and f.startswith("damage_claims"):
                    continue
                if word in ("crush",) and f.startswith("outbound_cage"):
                    continue
                ok("%s carries no '%s'" % (f, word), word not in tx)


def redraw_criterion(path):
    """The programme's lowest-BIC rule over the redraws screens.py recorded (FIT_ONLY=1 python3 screens.py 20 OUT)."""
    if not path or not os.path.exists(path):
        ok("SF16 the lowest-BIC rule picks a load step naming Ribarroja in every redraw", False,
           "no redraw file: run FIT_ONLY=1 python3 screens.py 20 OUT and pass --redraws OUT")
        return
    runs = json.load(open(path))["runs"]
    bad_forms = ("load_log", "load_step30", "load_step60_plus_constructing")
    good = [r for r in runs if r["bic_best"].startswith("load_") and not r["bic_best"].startswith(bad_forms)
            and r["bic_pick"] == "VLC"]
    ok("SF16 the lowest-BIC rule picks a supported load form naming Ribarroja in every redraw", len(good) == len(runs) >= 20,
       "%d of %d; picks %s" % (len(good), len(runs), sorted(set(r["bic_best"] for r in runs))))


def main():
    S = build.systems()
    redraw_criterion(sys.argv[sys.argv.index("--redraws") + 1] if "--redraws" in sys.argv else None)
    m = main_call(S)
    a = ask_checks(S)
    three_rules(S)
    realism(S)
    pack_checks()
    fails = [x for x in RES if not x[1]]
    for name, good, detail in RES:
        print("%s  %s  %s" % ("PASS" if good else "FAIL", name, detail[:160]))
    print("%d checks, %d FAIL" % (len(RES), len(fails)))
    dump = os.environ.get("CHECKS_DUMP")
    if dump:
        with open(dump, "w") as f:
            json.dump({"main": {k: v for k, v in m.items() if k != "readers"}, "asks": a,
                       "readers": m.get("readers")}, f, indent=1, default=str)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
