"""The generator's assertions on the cut pack and on the world behind it: the golden equals the truth, every licensed
method files it, the ladder's rungs file their named wrong lists, the semantic forks are closed (SF1 to SF22), the asks
equal their truth and every device sits where the design puts it, the separation line holds, and the input gates."""
import os
import sys

import numpy as np
import pandas as pd

import build as B
import ladder as L
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
    e, listed, par = S.call(D, "pl", Sr)
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
    ok(all(S.listed(f) == listed for f in fam.values()), "SF3 every licensed estimate files the golden list",
       sorted(fam))
    low = min(min(abs(f[s]) for s in listed) for f in fam.values())
    high = max(max(abs(v) for s, v in f.items() if s not in listed) for f in fam.values())
    ok(low > 0.06 and high < 0.045, "the margin holds over the whole family: listed beyond 6, others within 4.5",
       "%.4f %.4f" % (low, high))
    ok(min(abs(T_cnt[s]) for s in listed) > 0.06 and max(abs(v) for s, v in T_cnt.items() if s not in listed) < 0.045,
       "the truth sits inside the same margin")

    # the licensed family: every curve form, sensitivity per direction or pooled, the error inverted
    bh = S.bhat(D)
    x, y = S.pair_points(D, bh, Sr)
    for f in S.FAMILY:
        ef = S.errors(D, bh, S.fit(x, y, f)[0], Sr)
        ok(S.listed(ef) == listed, "SF3 curve form %s files the golden list" % f)
    bp = S.bhat(D, per_direction=False)
    xp, yp = S.pair_points(D, bp, Sr)
    ep = S.errors(D, bp, S.fit(xp, yp, "pl")[0], Sr)
    ok(S.listed(ep) == listed, "SF7 one sensitivity per station (directions pooled) files the golden list")
    inv = {s: 1 / (1 + v) - 1 for s, v in e.items()}
    ok(S.listed(inv) == listed, "SF4 the error read as passed over counted files the same list")
    cut = {}
    for c in (22.0, 25.0, 28.0):
        lq = float(np.mean(y[x > c]))
        ec = S.errors(D, bh, lambda o, c=c, lq=lq: np.where(np.asarray(o) > c, lq, 0.0), Sr)
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

    # the ladder on the pack: the default path, the bridge-only route
    v = S.validation_errors(D)
    default = S.listed(v)
    ok(default != listed, "default path (validation day) files another list", default)
    ok(len(set(listed) - set(default)) >= 2 and len(set(default) - set(listed)) >= 1,
       "the default path misses two or more and keeps one or more", (sorted(set(listed) - set(default)),
                                                                   sorted(set(default) - set(listed))))
    # analyst test on the clean world: the validation day files the wrong list, the loss construction the truth
    bw = L.bhat(W)
    xw, yw = L.pair_points(W, bw)
    Gw = L.errors(W, bw, L.fit(xw, yw, "pl"))
    ok(L.listed(L.validation_errors(W)) != L.listed(sim.truth(W)), "analyst test: the easy route on the clean world "
       "files a wrong list", L.listed(L.validation_errors(W)))
    ok(L.listed(Gw) == L.listed(sim.truth(W)), "analyst test: the loss construction on the clean world files the truth")
    vq = sum(int(W["true"][(s["code"], d)]["queued"][L.vhours(W, s)].sum()) for s in W["st"] for d in s["dirs"])
    ok(vq == 0, "no validation day holds a queued hour", vq)
    vd = set(zip(D["validation"]["station"], D["validation"]["date"].astype(str).str[:10]))
    h = D["hourly"]
    on = np.array([(s, d) in vd for s, d in zip(h["station"], h["local_start"].str[:10])])
    ok(h.loc[on, "occ"].max() < 20, "validation days' occupancy below 20 per cent", h.loc[on, "occ"].max())
    ok(len(D["validation"]) == 30 * 2 * 96, "SF12 every station filmed 96 quarter hours each direction, midnight to "
       "midnight", len(D["validation"]))

    # the separation line: the asks' devices never touch the call
    full = sim.world(P.SEED)
    eW = L.errors(full, L.bhat(full), L.fit(*L.pair_points(full, L.bhat(full)), "pl"))
    eW = {cur(k): val for k, val in eW.items()}
    ok(S.listed(eW) == listed and max(abs(eW[s] - e[s]) for s in e) < 0.002,
       "separation: the call on the record with no hour lost files the same list, every error within 0.2 points")
    ok(all(not os.path.basename(f).startswith(("trafficvault_station_events", "Carrick_work_orders"))
           for f in [B.FILES[k] for k in ("hourly", "validation", "register", "network")]),
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
    ok(S.call(D1, "pl")[1] == listed, "SF8 R2 every occupancy read at one decimal files the same list")

    # R1, R2, R3: the client's three rules executed (dataset-generation 7.1)
    cols = set()
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols |= set(pd.read_csv(os.path.join(target, f), nrows=2).columns)
        elif f.endswith(".xlsx"):
            for sh in pd.read_excel(os.path.join(target, f), sheet_name=None, nrows=2).values():
                cols |= set(sh.columns)
    ok({"vehicles", "occupancy", "video", "loops"} <= cols and not any("error" in str(x).lower() or "flag" in
                                                                      str(x).lower() for x in cols),
       "R1 the field's raw material ships (hourly vehicles and occupancy, the filmed counts) and no column holds an "
       "error or a flag")
    hn = D["hourly"].copy()
    hn["t"] = pd.to_datetime(hn["local_start"]).dt.tz_localize("UTC")
    Dn = dict(D)
    Dn["hourly"] = hn
    ok(S.call(Dn, "pl")[1] == listed, "R2 the local clock read without its offset files the same list")
    hr = D["hourly"].copy()
    raw_codes = pd.read_csv(os.path.join(target, B.FILES["hourly"]), usecols=["station"])["station"]
    keep = ~raw_codes.isin(D["hist"]["old_station"]).to_numpy()
    Dr = dict(D)
    Dr["hourly"] = hr[keep]
    ok(S.call(Dr, "pl")[1] == listed, "R2 the old numbers' hours dropped files the same list")
    ok(set(eW) == set(e), "R2 the hours lost from the record leave the call (the separation assertion above)")
    ok(L.listed(L.validation_errors(W)) == tuple(default) and default != listed,
       "R3a the easy route on the clean world and on the pack files the validation list")
    br = L.listed(L.bridge_only(W, bw))
    ok(br != L.listed(sim.truth(W)) and L.listed(Gw) == L.listed(sim.truth(W)),
       "R3b the decisive step alone reaches the truth; the bridge-only correction leaves a wrong list", br)
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
    ok(listed != default and "R08-05" in listed, "SF9 a renumbered station is on the golden list")
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
    t2 = {}
    for o in O["outs"]:
        for c in o["stations"]:
            if ops.controller(sx[c], o["start"].date()) == "TCX-2":
                k = (sx[c]["district"], ops.quarter(o["start"].date()))
                t2[k] = t2.get(k, 0) + len(o["parts"])
    ok(all(t2.get(c, 0) >= 1 for c in cells), "ask B device: a TCX-2 failure in every cell", [t2.get(c, 0) for c in cells])
    retrip = [(o["district"], ops.quarter(o["start"].date())) for o in O["outs"] if len(o["parts"]) == 2 and
              any(ops.controller(sx[c], o["start"].date()) == "TCX-2" for c in o["stations"])]
    ok(len(set(retrip)) >= 4, "ask B device: re-trips at TCX-2 stations in four or more cells", sorted(set(retrip)))
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
