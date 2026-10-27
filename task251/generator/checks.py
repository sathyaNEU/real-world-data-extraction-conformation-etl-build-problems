"""The generator's assertions on the cut pack and on the world behind it: the golden equals the truth, every licensed
method files it, the ladder's rungs file their named wrong lists, the semantic forks are closed (SF1 to SF26), the asks
equal their truth and every device sits where the design puts it, the separation line holds, and the input gates."""
import os
import sys

import numpy as np
import pandas as pd

import build as B
import ladder as L
import ladder5 as L5
import ops
import params as P
import sim
import solve as S

FAILS = []


def ok(cond, name, detail=""):
    print("%s  %s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


def pct(x):
    return int(round(100 * float(x)))


def main(target):
    del FAILS[:]
    W = sim.world(P.SEED)
    O = ops.ops(W)
    D = S.load(target, B.FILES)
    D = S.load_ops(target, B.FILES, D)
    Sr = S.series(D)
    e, listed, par = S.call(D, S=Sr)
    cur = lambda c: P.RENUMBERED[c][0] if c in P.RENUMBERED else c

    # the truth over the hours each station counted, and over every hour
    T_all = {cur(k): v for k, v in sim.truth(W).items()}
    T_cnt = {}
    for x in W["st"]:
        lost = O["lost"].get(x["code"], set())
        keep = np.array([i not in lost for i in range(sim.NH)])
        num = sum(W["rec"][(x["code"], d)][keep].sum() for d in x["dirs"])
        den = sum(W["true"][(x["code"], d)]["q"][keep].sum() for d in x["dirs"])
        T_cnt[cur(x["code"])] = num / den - 1
    ok(listed == S.listed(T_cnt), "golden list is the truth over the hours counted", listed)
    ok(S.listed(T_all) == S.listed(T_cnt), "SF6 the truth over every hour files the same list")
    margin = min(abs(abs(v) - P.TOLERANCE) for v in e.values())
    ok(margin >= 0.010, "SF5 no station within 1.0 point of the line", "%.4f" % margin)
    fam = S.wide_family(D, Sr)
    ok(len(fam) >= 40 and all(S.listed(f) == listed for f in fam.values()),
       "SF3 SF23 SF24 every licensed estimate (five loss forms under nine readings of the cold miss, edges out, two-hour "
       "blocks, weights, the pairs' own free-flow ratio, pooled sensitivity) files the golden list", len(fam))
    low = min(min(abs(f[s]) for s in listed) for f in fam.values())
    high = max(max(abs(v) for s, v in f.items() if s not in listed) for f in fam.values())
    ok(low > 0.065 and high < 0.045, "the margin holds over the whole family: listed beyond 6.5, others within 4.5",
       "%.4f %.4f" % (low, high))
    ok(min(abs(T_cnt[s]) for s in listed) > 0.06 and max(abs(v) for s, v in T_cnt.items() if s not in listed) < 0.045,
       "the truth sits inside the same margin")
    ok(S.listed(fam[("pl_pooled_sensitivity", "mean_knee")]) == listed,
       "SF7 one sensitivity per station (directions pooled) files the golden list")
    inv = {s: 1 / (1 + v) - 1 for s, v in e.items()}
    ok(S.listed(inv) == listed, "SF4 the error read as passed over counted files the same list")
    bh = S.bhat(D)
    cday = S.by_day(D, S.cold_fit(*S.cold_points(D, bh, Sr), "knee")[0])
    x, y = S.pair_points(D, bh, Sr, cday)
    mh = S.fit(x, y, "pl")[0]
    cut = {}
    for c in (22.0, 25.0, 28.0):
        lq = float(np.mean(y[x > c]))
        ec = S.errors(D, bh, lambda o, c=c, lq=lq: np.where(np.asarray(o) > c, lq, 0.0), cday, Sr)
        cut[c] = S.listed(ec)
    ok(all(v == listed for v in cut.values()), "SF3 a constant loss above 22, 25 or 28 per cent files the golden list",
       cut)
    ys = []
    for b in S.bridges(D):
        for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
            j = Sr[(up, d)].join(Sr[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
            ys.append(len(j))
    ok(len(S.bridges(D)) == 5 and min(ys) > 8000, "SF11 five bridges, each approach pair with no junction between",
       ys)
    # the loss read on a subset of the pairs: each direction alone, the bridges of one generation, the mixed bridges
    import datetime as _dt
    jan = [_dt.date(P.YEAR, 1, 5)]
    same = [b["name"] for b in S.bridges(D) if S.is_tcx2(D, b["south"], jan)[0] == S.is_tcx2(D, b["north"], jan)[0]]
    sub = {}
    for name, dirs, names in (("NB", ("NB",), None), ("SB", ("SB",), None), ("one generation", ("NB", "SB"), same),
                              ("mixed", ("NB", "SB"), [b["name"] for b in S.bridges(D) if b["name"] not in same])):
        xs, yv = [], []
        for b in S.bridges(D):
            if names and b["name"] not in names:
                continue
            for d, up, dn in (("NB", b["south"], b["north"]), ("SB", b["north"], b["south"])):
                if d not in dirs:
                    continue
                j = Sr[(up, d)].join(Sr[(dn, d)], lsuffix="_u", rsuffix="_d", how="inner")
                j = j[(j["vehicles_u"] > 50) & (j["vehicles_d"] > 50)]
                days = j["day_u"].tolist()
                cu, cd = S.chour(D, up, days, cday), S.chour(D, dn, days, cday)
                xs.append(j["occ_u"].to_numpy())
                yv.append((1 - (j["vehicles_u"] / ((1 + bh[(up, d)]) * (1 - cu))) /
                           (j["vehicles_d"] / ((1 + bh[(dn, d)]) * (1 - cd)))).to_numpy())
        sub[name] = S.listed(S.errors(D, bh, S.fit(np.concatenate(xs), np.concatenate(yv), "pl")[0], cday, Sr))
    ok(len(same) == 2 and all(v == listed for v in sub.values()),
       "SF3 the loss from each direction alone, from the two one-generation bridges or from the three mixed ones files "
       "the golden list", sub)

    # SF23: the generation that misses vehicles in the cold. The TCX-2s' occupancy per counted vehicle climbs in the
    # winter while the TCX-4s' holds flat, so the pairs' ratio falls because the TCX-2 counts fewer, not because the
    # TCX-4 counts more
    h = D["hourly"].copy()
    h["day"] = pd.to_datetime(h["local_start"].str[:10]).dt.date
    h["m"] = pd.to_datetime(h["local_start"].str[:10]).dt.month
    t2 = np.zeros(len(h), bool)
    for s, g in h.groupby("station"):
        t2[g.index.to_numpy()] = S.is_tcx2(D, s, g["day"].tolist())
    h["t2"] = t2
    ff = h[(h["occ"] < 12) & (h["vehicles"] > 100)]
    opv = ff.groupby(["t2", "m"]).apply(lambda g: (g["occ"] / g["vehicles"]).mean())
    r2 = opv[(True, 1)] / opv[(True, 7)]
    r4 = opv[(False, 1)] / opv[(False, 7)]
    ok(r2 > 1.05 and abs(r4 - 1) < 0.015, "SF23 occupancy per counted vehicle: TCX-2 January over July %.3f, TCX-4 %.3f"
       % (r2, r4))
    # SF24: the day's temperature. Mean, maximum or minimum, a curve or bins, the occupancy channel: in the family
    names = {k[1] for k in fam}
    ok({"mean_knee", "mean_knee2", "mean_bins", "max_knee", "max_bins", "min_knee", "min_bins", "occupancy_daily",
        "occupancy_curve"} <= names, "SF24 every reading of the cold miss sits in the licensed family")
    # SF25: the day the airport's temperature record is missing
    w = D["weather"]
    miss = w[w["Mean Temp Flag"].astype(str) == "M"]
    ok(len(miss) == 1 and miss["Mean Temp (°C)"].isna().all(), "layer 1: one day's temperatures missing, flagged M",
       list(miss["Date/Time"]))
    md = pd.Timestamp(miss["Date/Time"].iloc[0]).date()
    alt = {}
    zero_day = lambda days: np.where(np.array([d == md for d in days]), 0.0, cday(days))
    xz, yz = S.pair_points(D, bh, Sr, zero_day)
    alt["no miss that day"] = S.listed(S.errors(D, bh, S.fit(xz, yz, "pl")[0], zero_day, Sr))
    Sd = {k: g[[d != md for d in g["day"]]] for k, g in Sr.items()}
    alt["day's hours dropped"] = S.listed(S.errors(D, bh, S.fit(*S.pair_points(D, bh, Sd, cday), "pl")[0], cday, Sd))
    ok(all(v == listed for v in alt.values()), "SF25 R2 the missing day taken as no miss, or its hours dropped, files "
       "the same list", alt)
    # SF26: the controller in force each day. The register's current controller all year moves no station across
    D2 = dict(D)
    D2["hist"] = D["hist"].iloc[0:0]
    l2 = S.call(D2, S=Sr)[1]
    ok(l2 == listed, "SF26 R2 the register's current controller read for the whole year files the same list", l2)

    # SF27 to SF30: the four free parameters the determinism block found, each closed on the record's own arithmetic.
    # The instrument under all four is the occupancy a station reports per vehicle it counts, read at matched
    # free-flowing counted flow: a vehicle covers the loop whether the controller counts it or not, so the ratio moves
    # one for one with a change in the station's counting and not at all with the traffic.
    ctl = dict(zip(D["reg"]["station"], D["reg"]["controller"]))
    swapd = {r["new_station"]: pd.Timestamp(r["from_date"]).date() for _, r in D["hist"].iterrows()}
    all4 = [s for s in D["reg"]["station"] if ctl[s] == "TCX-4" and s not in swapd]
    all2 = [s for s in D["reg"]["station"] if ctl[s] == "TCX-2" and s not in swapd]
    mfw = S.matched_table(D, Sr, (12, 1, 2))
    r4 = np.array([mfw[s] for s in all4])
    r2 = np.array([mfw[s] for s in all2])
    tmd = S.tmean(D)
    ddw = float(np.mean([max(0.0, P.COLD_KNEE - tmd[d]) for d in tmd if d.month in (12, 1, 2)]))
    cold_w = float(np.mean(cday([d for d in sorted(tmd) if d.month in (12, 1, 2)])))
    ok(len(all4) == 13 and len(all2) == 15 and r4.max() < 1.010 and abs(r4.mean() - 1) < 0.006,
       "SF27 SF29 the stations that ran one controller all year: at a TCX-4 the occupancy per counted vehicle at "
       "matched free flow holds through the winter (max %.4f, mean %.4f, sd %.4f), so nothing the two generations "
       "share moves a count" % (r4.max(), r4.mean(), r4.std(ddof=1)))
    ok(abs((1 - 1 / r2.mean()) - cold_w) < 0.006 and r2.min() > 1.07,
       "SF27 SF28 at a TCX-2 the same ratio is the cold miss the mixed pairs give: %.4f against the pooled curve's "
       "%.4f over the same days" % (1 - 1 / r2.mean(), cold_w))
    drift_bound = (r4.max() - 1) / ddw
    mfun1 = lambda s, occ: mh(occ)
    cfun1 = lambda s, days: S.chour(D, s, days, cday)
    drift = lambda k: (lambda s, days, k=k: S.chour(D, s, days, cday) +
                       np.clip(k * np.array([P.COLD_KNEE - tmd[x] for x in days]), min(0, k * 40), max(0, k * 40)))
    held = {k: S.listed(S.errors_g(D, bh, mfun1, drift(k), Sr)) for k in (-0.008, -0.004, 0.0025, 0.005)}
    broke = {k: S.listed(S.errors_g(D, bh, mfun1, drift(k), Sr)) for k in (0.006, -0.012)}
    ok(all(v == listed for v in held.values()) and all(v != listed for v in broke.values()) and
       drift_bound < 0.001 and 0.005 * ddw / (r4.max() - 1) > 5,
       "SF29 a drift common to both generations: the record allows at most %.5f per degree (%.2f per cent over "
       "December to February) and the list needs 0.006 (%.2f per cent) to move, %.1f times as much"
       % (drift_bound, 100 * (r4.max() - 1), 100 * 0.006 * ddw, 0.006 / drift_bound))
    bl = S.bridge_losses(D, bh, Sr, cday)
    bv = np.array([v[0] for v in bl.values()])
    site_sd = float(bv.std(ddof=1) / bv.mean())
    scale = {f: S.listed(S.errors_g(D, bh, lambda s, occ, f=f: f * mh(occ), cfun1, Sr))
             for f in (0.5, 0.6, 0.8, 1.2, 1.35)}
    sbroke = {f: S.listed(S.errors_g(D, bh, lambda s, occ, f=f: f * mh(occ), cfun1, Sr)) for f in (0.4, 1.4)}
    ok(len(bl) == 5 and site_sd < 0.03 and all(v == listed for v in scale.values()) and
       all(v != listed for v in sbroke.values()),
       "SF28 the loss is one function of occupancy at five separate sites (%.4f to %.4f at 40 per cent, sd %.1f per "
       "cent of the mean) and the list is invariant over a per-station scale of 0.5 to 1.35, twelve times that spread"
       % (bv.min(), bv.max(), 100 * site_sd))
    cs = S.cold_station(D, Sr)
    own = S.listed(S.errors_g(D, bh, mfun1, lambda s, days: cs[s](days), Sr))
    ok(own == listed, "SF28 SF30 the cold miss read at every station from its own occupancy channel, with no bridge "
                      "pair, no register and no temperature, files the golden list", own)
    cscale = {f: S.listed(S.errors_g(D, bh, mfun1, lambda s, days, f=f: f * S.chour(D, s, days, cday), Sr))
              for f in (0.7, 1.3)}
    ok(all(v == listed for v in cscale.values()), "SF28 the list is invariant over a per-station cold scale of 0.7 "
                                                  "to 1.3")
    vday1 = D["validation"].groupby("station")["date"].first().dt.date.to_dict()
    unf = lambda f: (lambda s, d, days, f=f: np.where(
        np.array([(x < swapd[s]) == (vday1[s] >= swapd[s]) for x in days]) if s in swapd else False,
        (1 + bh[(s, d)]) * f, 1 + bh[(s, d)]))
    reg_held = {f: S.listed(S.errors_g(D, bh, mfun1, cfun1, Sr, unf(f))) for f in (0.90, 0.95, 1.03, 1.05)}
    reg_broke = {f: S.listed(S.errors_g(D, bh, mfun1, cfun1, Sr, unf(f))) for f in (1.12,)}
    mf8 = S.matched_ratio(D, "R08-05", (1, 2, 3, 4), (7, 8), Sr)
    c2 = np.array([S.matched_ratio(D, s, (1, 2, 3, 4), (7, 8), Sr) for s in all2])
    mf19 = S.matched_ratio(D, "R19-03", (10, 11, 12), (7, 8), Sr)
    c4 = np.array([S.matched_ratio(D, s, (10, 11, 12), (7, 8), Sr) for s in all4])
    ok(abs(mf8 / c2.mean() - 1) < 0.015 and abs(mf19 / c4.mean() - 1) < 0.015 and
       all(v == listed for v in reg_held.values()) and all(v != listed for v in reg_broke.values()),
       "SF30 the regime no filmed day covers: R08-05 before its replacement reads %.4f against the all-year TCX-2 "
       "stations' %.4f and R19-03 after its replacement %.4f against the all-year TCX-4 stations' %.4f, so each "
       "matches its own generation to %.1f per cent, while the list needs 10 per cent to move"
       % (mf8, c2.mean(), mf19, c4.mean(), 100 * max(abs(mf8 / c2.mean() - 1), abs(mf19 / c4.mean() - 1))))
    imb = S.imbalance(D, bh, Sr, cday)
    ok(imb["queued"] > 0.15 and imb["free"] < 0.02 and imb["queued"] / imb["queued_se"] > 100,
       "the pairs refute no correction at all: the upstream approach counts %.2f per cent fewer vehicles than the "
       "downstream one above 30 per cent occupancy (se %.3f, t %.0f) against %.2f per cent in free flow, with "
       "nothing joining or leaving between them"
       % (100 * imb["queued"], 100 * imb["queued_se"], imb["queued"] / imb["queued_se"], 100 * imb["free"]))
    bad = D["orders"][D["orders"]["resolution"].str.contains("detector|card", case=False, na=False)]
    lp = D["orders"][D["orders"]["resolution"].str.contains("loop", case=False, na=False)]
    ok(len(bad) == 0 and len(lp) >= 12 and lp["resolution"].str.contains("tested", case=False).all(),
       "SF27 no work order of the year replaces anything on the counting path (the inspections test the loops at "
       "every station twice), so the filmed day's sensitivity is the sensitivity of every hour of its regime",
       (len(bad), len(lp)))

    # SF3: the cold pairs' free-flow threshold, and the loss fitted before the cold miss is taken out
    thr = {}
    for fo in (12.0, 25.0):
        cd2 = S.by_day(D, S.cold_fit(*S.cold_points(D, bh, Sr, free_occ=fo), "knee")[0])
        thr[fo] = S.listed(S.errors(D, bh, S.fit(*S.pair_points(D, bh, Sr, cd2), "pl")[0], cd2, Sr))
    thr["loss first"] = S.listed(S.errors(D, bh, S.fit(*S.pair_points(D, bh, Sr, S.ZDAY), "pl")[0], cday, Sr))
    ok(all(v == listed for v in thr.values()), "SF3 the cold pairs' free flow below 12 or 25 per cent, or the loss "
       "fitted before the cold miss is taken out, files the golden list", thr)
    oc = {k: S.listed(v) for k, v in S.overcount_routes(D, Sr).items()}
    ok(all(v != listed for v in oc.values()), "SF23 the cold effect read as a TCX-4 overcount files another list "
       "(ruled out by the occupancy channel above)", oc)

    # the ladder on the pack: the validation day, the queue loss alone, the cold miss alone
    R = S.routes(D, Sr)
    default, qonly, conly = S.listed(R["D"]), S.listed(R["A"]), S.listed(R["B"])
    ok(R["G"] == e, "routes: the golden route is the call")
    ok(len({tuple(default), tuple(qonly), tuple(conly), tuple(listed)}) == 4,
       "the four rungs file four different lists", (default, qonly, conly))
    ok(len(set(listed) - set(default)) >= 4 and len(set(listed) - set(qonly)) >= 2 and
       len(set(listed) - set(conly)) >= 2, "each wrong rung misses two or more of the golden",
       (sorted(set(listed) - set(default)), sorted(set(listed) - set(qonly)), sorted(set(listed) - set(conly))))
    both = sorted(set(listed) - set(qonly) - set(conly))
    ok(len(both) >= 1, "a station only the two corrections together bring in", both)
    # analyst test on the clean world: the validation day, either correction alone files a wrong list; both the truth
    Rw = L5.routes(W)
    Tw = L.listed(sim.truth(W))
    ok(L.listed(Rw["D"]) != Tw and L.listed(Rw["A"]) != Tw and L.listed(Rw["B"]) != Tw,
       "analyst test: on the clean world the easy route and either correction alone file wrong lists",
       (L.listed(Rw["D"]), L.listed(Rw["A"]), L.listed(Rw["B"])))
    ok(L.listed(Rw["G"]) == Tw, "analyst test: both corrections on the clean world file the truth", Tw)
    vq = sum(int(W["true"][(s["code"], d)]["queued"][L.vhours(W, s)].sum()) for s in W["st"] for d in s["dirs"])
    ok(vq == 0, "no validation day holds a queued hour", vq)
    vc = sum(float(W["cmiss"][s["code"]][L.vhours(W, s)].sum()) for s in W["st"])
    ok(vc == 0, "no validation day holds a cold miss", vc)
    vd = set(zip(D["validation"]["station"], D["validation"]["date"].astype(str).str[:10]))
    hh = D["hourly"]
    on = np.array([(s, d) in vd for s, d in zip(hh["station"], hh["local_start"].str[:10])])
    ok(hh.loc[on, "occ"].max() < 20, "validation days' occupancy below 20 per cent", hh.loc[on, "occ"].max())
    ok(len(D["validation"]) == 30 * 2 * 96, "SF12 every station filmed 96 quarter hours each direction, midnight to "
       "midnight", len(D["validation"]))

    # the separation line: the asks' devices never touch the call
    full = sim.world(P.SEED)
    eW = {cur(k): val for k, val in L5.routes(full)["G"].items()}
    ok(S.listed(eW) == listed and max(abs(eW[s] - e[s]) for s in e) < 0.003,
       "separation: the call on the record with no hour lost files the same list, every error within 0.3 points",
       "%.4f" % max(abs(eW[s] - e[s]) for s in e))
    ok(all(not os.path.basename(f).startswith(("trafficvault_station_events", "Carrick_work_orders"))
           for f in [B.FILES[k] for k in ("hourly", "validation", "register", "network", "weather")]),
       "separation: the call reads no file an ask device sits in")

    # SF2, SF9, SF10, layer 1: the year, the renumbering, the site codes, the clock
    h = D["hourly"]
    ok(h["local_start"].min() == "2027-01-01 00:00" and h["local_start"].max() == "2027-12-31 23:00",
       "SF2 the export runs over the local calendar year")
    spring = h[h["local_start"] == "2027-03-14 02:00"]
    autumn = h[h["local_start"] == "2027-11-07 01:00"]
    ok(spring.empty and autumn.groupby(["station", "direction"]).size().max() == 2,
       "layer 1: the spring hour missing, the autumn hour twice")
    ok(set(D["hist"]["new_station"]) <= set(D["reg"]["station"]) and not ({"R08-01", "R19-01"} & set(D["hourly"]["station"])),
       "SF9 the renumbered stations sit under their current numbers once joined")
    raw = pd.read_csv(os.path.join(target, B.FILES["hourly"]), usecols=["station"])
    ok({"R08-01", "R08-05", "R19-01", "R19-03"} <= set(raw["station"]), "layer 1: both numbers of each renumbered "
       "station in the export")
    ok(D["validation"]["station"].notna().all() and D["validation"]["station"].nunique() == 30,
       "SF10 every site code maps to a station")
    occ = pd.read_csv(os.path.join(target, B.FILES["hourly"]), usecols=["occupancy"], dtype=str)["occupancy"]
    dec = occ.str.split(".").str[1].str.len()
    ok(set(dec.unique()) == {1, 2}, "SF8 occupancy in per cent at one decimal (TCX-2) and two (TCX-4)")
    h1 = D["hourly"].copy()
    D1 = dict(D)
    h1["occ"] = h1["occ"].round(1)
    D1["hourly"] = h1
    ok(S.call(D1)[1] == listed, "SF8 R2 every occupancy read at one decimal files the same list")

    # R1, R2, R3: the client's three rules executed (dataset-generation 7.1)
    cols = set()
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols |= set(pd.read_csv(os.path.join(target, f), nrows=2).columns)
        elif f.endswith(".xlsx"):
            for sh in pd.read_excel(os.path.join(target, f), sheet_name=None, nrows=2).values():
                cols |= set(sh.columns)
    ok({"vehicles", "occupancy", "video", "loops", "Mean Temp (°C)"} <= cols and
       not any("error" in str(x).lower() or "flag" == str(x).lower() for x in cols),
       "R1 the field's raw material ships (hourly vehicles and occupancy, the filmed counts, the day's temperatures) "
       "and no column holds an error or a station flag")
    hn = D["hourly"].copy()
    hn["t"] = pd.to_datetime(hn["local_start"]).dt.tz_localize("UTC")
    Dn = dict(D)
    Dn["hourly"] = hn
    ok(S.call(Dn)[1] == listed, "R2 the local clock read without its offset files the same list")
    hr = D["hourly"].copy()
    raw_codes = pd.read_csv(os.path.join(target, B.FILES["hourly"]), usecols=["station"])["station"]
    keep = ~raw_codes.isin(D["hist"]["old_station"]).to_numpy()
    Dr = dict(D)
    Dr["hourly"] = hr[keep]
    ok(S.call(Dr)[1] == listed, "R2 the old numbers' hours dropped files the same list")
    ok(set(eW) == set(e), "R2 the hours lost from the record leave the call (the separation assertion above)")
    ok(L.listed(Rw["D"]) == tuple(default) and default != listed,
       "R3a the easy route on the clean world and on the pack files the validation list")
    cl = lambda r: sorted(cur(k) for k in L.listed(r))
    ok(cl(Rw["A"]) == qonly and cl(Rw["B"]) == conly and cl(Rw["G"]) == listed,
       "R3b on the clean world and the pack, the queue loss alone and the cold miss alone each leave a wrong list; "
       "the decisive step, both, reaches the truth")
    # R3c and the realism sweep: no copied block, no constant stream, no repeated day
    days = {}
    dup = 0
    for (s, d), g in D["hourly"].groupby(["station", "direction"]):
        v24 = g["vehicles"].to_numpy()
        n = len(v24) // 24
        for k in range(n):
            key = tuple(v24[24 * k:24 * (k + 1)])
            if key in days:
                dup += 1
            days[key] = 1
    ok(dup == 0, "R3c no station-day repeats another's 24 counts", dup)
    ok(D["hourly"].groupby(["station", "direction"])["vehicles"].std().min() > 50, "R3c no constant stream")
    vt = D["validation"].groupby(["station", "direction"])["video"].sum()
    ok(vt.nunique() == len(vt) and sum(x % 100 == 0 for x in vt) <= 2 and not any(x % 1000 == 0 for x in vt),
       "realism: no repeated validation total, round ones at no more than chance")
    desc = D["orders"]["description"].value_counts()
    ok(desc.iloc[0] <= 0.4 * len(D["orders"]), "realism: no work order text recurring beyond a real rate",
       desc.iloc[0])
    ok("R08-05" in listed, "SF9 a renumbered station is on the golden list")
    ok(all(len(set(g["station"])) == 1 for _, g in D["validation"].groupby("site")), "SF10 one station per site code")

    # the asks
    vis, fail = S.visits(D), S.failures(D)
    vt, ft = ops.visits_truth(W, O["work"]), ops.failures_truth(W, O["outs"])
    cells = sorted(vis)
    ok(all(vis[c] == vt.get(c, 0) for c in cells), "ask A: visits equal the truth", [vis[c] for c in cells])
    ok(all(fail[c] == ft.get(c, 0) for c in cells), "ask B: failures equal the truth", [fail[c] for c in cells])
    sx = {x["code"]: x for x in W["st"]}
    rem = {}
    for w in O["work"]:
        for c, at, how in w["resets"]:
            if how == "REMOTE":
                k = (sx[c]["district"], ops.quarter(w["labour"][0][0]))
                rem[k] = rem.get(k, 0) + 1
    ok(all(rem.get(c, 0) >= 2 for c in cells), "ask A device: two or more office resets in every cell",
       [rem.get(c, 0) for c in cells])
    od = D["orders"].assign(station=D["orders"]["stations"].str.split("; ")).explode("station")
    od["station"] = od["station"].map(lambda c: S.current(c, D))
    od["day"] = pd.to_datetime(od["opened"]).dt.date
    t2rows = od[[not S.tcx4_on(D, s_, d_) for s_, d_ in zip(od["station"], od["day"])]]
    t2comms = t2rows[t2rows["description"].str.startswith("No data from controller")]
    ok(not t2rows["resolution"].str.startswith("Controller reset").any() and len(t2comms) > 0 and
       t2comms["resolution"].str.contains("Modem|Antenna").all(),
       "SF14 a TCX-2 has no remote reset: every TCX-2 communications fault is cleared at the cabinet and says so",
       len(t2comms))
    t2 = {}
    for o in O["outs"]:
        for c in o["stations"]:
            if ops.controller(sx[c], o["start"].date()) == "TCX-2":
                k = (sx[c]["district"], ops.quarter(o["start"].date()))
                t2[k] = t2.get(k, 0) + len(o["parts"])
    ok(all(t2.get(c, 0) >= 1 for c in cells), "ask B device: a TCX-2 failure in every cell", [t2.get(c, 0) for c in cells])
    retrip = [(o["district"], ops.quarter(o["start"].date())) for o in O["outs"] if len(o["parts"]) == 2 and
              any(ops.controller(sx[c], o["start"].date()) == "TCX-2" for c in o["stations"])]
    ok(len(set(retrip)) >= 7, "ask B device: re-trips at TCX-2 stations in seven or more cells", sorted(set(retrip)))
    silent = set()
    for r in O["power"]:
        o = r["outage"]
        if o.get("momentary") and r["controller"] == "TCX-2" and not any(ev == "COMMS_LOST" for t, by, ev in r["events"]):
            silent.add((o["district"], ops.quarter(o["start"].date())))
    ok(len(silent) >= 10, "ask B device: a momentary interruption at a TCX-2 that no poll caught (a break with no "
       "COMMS_LOST) in ten or more cells", len(silent))
    mom = [o for o in O["outs"] if o.get("momentary")]
    ok(all(any(ops.controller(sx[c], o["start"].date()) == "TCX-4" for c in o["stations"]) for o in mom),
       "SF15 every momentary interruption also reaches a TCX-4, whose MAINS_FAIL and MAINS_OK in the same hour "
       "corroborate the TCX-2's break")
    ok(all((o["end"] - o["start"]).total_seconds() < 300 for o in mom) and
       any(any(ev == "COMMS_LOST" for t, by, ev in r["events"]) for r in O["power"] if r["outage"].get("momentary")),
       "ask B device: every momentary interruption under five minutes, some of them caught by a poll (no marker)",
       len(mom))
    # every re-trip at a TCX-2 left two COMMS_LOST inside one break, every single loss at most one
    ev = S._events(D)
    lost = ev[ev["event"] == "COMMS_LOST"]
    good = True
    for s, t0, n in S._missing_runs(D):
        d0 = t0.tz_convert(S.TZ).date()
        if S.tcx4_on(D, s, d0):
            continue
        k = int(((lost["station"] == s) & (lost["t"] >= t0) & (lost["t"] < t0 + pd.Timedelta(hours=n))).sum())
        o = [o for o in O["outs"] if any(cur(c) == s for c in o["stations"]) and o["start"].date() == d0]
        if o and k != (len(o[0]["parts"]) if len(o[0]["parts"]) == 2 else min(k, 1)):
            good = False
    ok(good, "SF15 a break holds one COMMS_LOST per loss a poll fell in, two for every re-trip")
    # alternative exact handlings agree
    alt = {}
    lab = S._labour_days(D)
    resets = ev[ev["event"] == "RESET"]
    doors = ev[ev["event"].isin(["DOOR_OPEN", "DOOR_CLOSE"])]
    rs = set(zip(resets["station"], resets["day"])) - set(zip(doors["station"], doors["day"]))
    pairs = [(s, d) for s, d in zip(lab["station"], lab["day"]) if (s, d) not in rs]
    alt = S._cells(pairs, D)
    ok(alt == vis, "SF14 the office resets read as a RESET with the cabinet shut give the same visits")
    ok(S.visits(D, door_days="utc") != vis, "SF22 the door log read on UTC dates moves a visit (device aimed)")
    ok(S.failures(D, quarter_clock="utc") != fail, "SF16 quarters on UTC dates move a failure (device aimed)")
    # no fault, outage or region check within a day of a validation day; no work on a replacement day but the swap
    for o in O["outs"]:
        for c in o["stations"]:
            assert abs((sx[c]["vday"] - o["start"].date()).days) > 1
    ok(True, "no outage within a day of a hit station's validation day")
    ok(all(abs((sx[c]["vday"] - a.date()).days) > 1 for w in O["work"] for c, a, b in w["onsite"]),
       "no maintenance visit within a day of the station's validation day")
    ok(all(not (o["start"].date() <= dt_ <= o["end"].date()) for o in O["outs"] for w in O["work"]
           for c, dt_, how in [(c, at.date(), how) for c, at, how in w["resets"]] if c in o["stations"]),
       "no office reset during an outage at its station")

    # SF1, SF13, SF17 to SF21
    ok(len(D["reg"]) == 30 and len(D["hist"]) == 2 and set(D["hist"]["new_station"]) <= set(D["reg"]["station"]),
       "SF1 thirty stations in the register, each renumbered station one row under its current number")
    import json
    fj = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    if os.path.exists(fj):
        ok("error_pct" not in json.load(open(fj))["call"], "SF13 no station's error is a graded figure")
    ok(D["reg"].groupby("station")["district"].nunique().max() == 1, "SF17 one district per station")
    crew = {(cur(c), a.date()) for c, a, b in O["crew"]} | {(cur(c), b.date()) for c, a, b in O["crew"]}
    seen_days = {(cur(c), a.date()) for w in O["work"] for c, a, b in w["onsite"]}
    ok(crew and not (crew & seen_days), "SF18 the validation crew's nights at the cabinets are no maintenance visit")
    swapv = {(cur(c), d) for c, (n, d) in P.RENUMBERED.items()}
    ok(swapv <= seen_days, "SF19 each controller replacement is a maintenance visit")
    ok(all(not any(cur(c) == n and o["start"].date() == d for o in O["outs"] for c in o["stations"])
           for c, (n, d) in P.RENUMBERED.items()), "SF19 no power failure on a replacement day")
    raw_ev = pd.read_csv(os.path.join(target, B.FILES["events"]))
    y2k = raw_ev[raw_ev["logged_utc"].str.startswith("2000")]
    ok(len(y2k) >= 4 and set(y2k["event"]) <= {"COLD_START", "MAINS_OK", "DOOR_OPEN"},
       "SF20 the cold starts' events carry the unset clock; no MAINS_FAIL does", sorted(set(y2k["event"])))
    ok(raw_ev.duplicated().sum() > 0 and (raw_ev[raw_ev.duplicated()]["event"] == "MAINS_FAIL").any(),
       "SF21 the log repeats some events after a lost poll, a MAINS_FAIL among them", int(raw_ev.duplicated().sum()))

    # input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "input gate: ten or more files", len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gate: three or more formats",
       sorted({f.rsplit(".", 1)[1] for f in files}))
    ok(len(D["hourly"]) >= 25000, "input gate: a file of 25,000 rows or more", len(D["hourly"]))
    ok(len(B.DISTRACTORS) >= 2, "input gate: two distractors", B.DISTRACTORS)
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "solve.py")).read()
    ok(all('"%s"' % k not in src for k in B.DISTRACTORS), "the distractors are unused by the golden")
    print("%d checks failed" % len(FAILS))
    return FAILS


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           "target")
    sys.exit(1 if main(t) else 0)
