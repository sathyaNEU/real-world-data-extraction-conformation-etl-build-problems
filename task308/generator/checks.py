"""task308 checks, run on every build: the three rules on the clean truth (R1 to R3c), the estimator family and the
ladder of the call, the semantic fork grid (SF rows) as a cross product, the asks' truths, ladders and separation,
the distractors' deletion test, the input gates and the realism sweep. main() returns the number of failures."""
import collections
import datetime as dt
import itertools
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import params as P
import records as R
import solve as SV
import world as Wd

FAILS = []
NETS = SV.NETS
CODE = {"Central": "CEN", "University": "UNI", "Riverside": "RIV", "Old Town": "OLD", "Hillcrest": "HIL"}


def ok(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + (("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(label)


def bin25(x):
    return SV.r25(x)


def margin25(vals):
    """distance from the family's range to the edges of the 25,000 bin its first member rounds into"""
    b = bin25(vals[0])
    return min(min(vals) - (b - 12500), (b + 12500) - max(vals))


# ---------------------------------------------------------------------------------------------------- the call
def family(G):
    S, T, rb, pl = G["S"], G["T"], G["rb"], G["pilot"]
    H, Mo, Wk, Dw = G["keys"]
    net_of = dict(zip(S.station_id, S.network))
    term = np.isin(Mo, [0, 1, 2, 3, 8, 9, 10, 11])
    keys = {"station x month x weekday-or-weekend x hour": Mo * 48 + Wk * 24 + H,
            "station x month x day of week x hour": Mo * 168 + Dw * 24 + H,
            "station x teaching-or-break months x weekday-or-weekend x hour": np.where(term, 0, 1) * 48 + Wk * 24 + H}
    Us = {k: SV.turned_away(S, rb, v) for k, v in keys.items()}
    out = {k: SV.net_revenue(S, T, U, pl) for k, U in Us.items()}
    out["induced on the rides served"] = SV.net_revenue(S, T, Us["station x month x weekday-or-weekend x hour"], pl,
                                                          induced_on="rides")
    return out, Us


def lower_rungs(G):
    S, T, rb, pl = G["S"], G["T"], G["rb"], G["pilot"]
    H, Mo, Wk, Dw = G["keys"]
    out = {"no month (weekday-or-weekend x hour over the year)": SV.net_revenue(S, T, SV.turned_away(S, rb, Wk * 24 + H), pl)}
    # whole network pooled into one rate per cell
    pool = {}
    for n, g in S.groupby("network"):
        for sid in g.station_id:
            pool[sid] = list(g.station_id)
    out["one rate per network and cell"] = SV.net_revenue(S, T, SV.turned_away(S, rb, Mo * 48 + Wk * 24 + H, pool), pl)
    # hours empty from start to end only
    U = {}
    key = Mo * 48 + Wk * 24 + H
    for sid in S.station_id:
        s, e, d = rb[sid]
        full = (s > 0) & (e == 0)
        cnt = np.bincount(key, weights=full.astype(float)); dd = np.bincount(key, weights=d * full)
        lam = np.divide(dd, cnt, out=np.zeros_like(dd), where=cnt > 0)
        U[sid] = float((lam[key] * ((s == 0) & (e > 0))).sum())
    out["whole empty hours only"] = SV.net_revenue(S, T, U, pl)
    return out


def ten_minute_steps(G, M, A):
    """the discrete construction: stock at each ten-minute step's start; the mean undocks of steps that start with a
    bike, imputed to the steps that start empty"""
    S, T = G["S"], G["T"]
    steps = np.arange(SV.T0, SV.T1, 600)
    loc = pd.to_datetime(steps, unit="s", utc=True).tz_convert(SV.TZ)
    key = (loc.month.values - 1) * 48 + (loc.weekday.values >= 5).astype(int) * 24 + loc.hour.values
    cl = T[~T.ebike]; mv = M[M.bike_class == "classic"]
    U = {}
    for sid in S.station_id:
        dep = cl[cl.s0 == sid]; arr = cl[cl.s1 == sid]
        vo = mv[mv.from_station == sid]; vi = mv[mv.to_station == sid]
        t = np.concatenate([dep.t0.values, arr.t1.values, vo.t.values, vi.t.values])
        d = np.concatenate([-np.ones(len(dep)), np.ones(len(arr)), -vo.qty.values, vi.qty.values])
        pr = np.concatenate([np.zeros(len(dep)), np.ones(len(arr) + len(vo) + len(vi))])
        o = np.lexsort((pr, t)); t, d = t[o], d[o]; cs = np.concatenate([[0], np.cumsum(d)])
        c = A[A.station_id == sid].sort_values("t"); ct = c.t.values; cv = c.classic_docked.values
        ai = np.searchsorted(ct, steps, "right") - 1; good = ai >= 0
        a = ct[np.maximum(ai, 0)]
        lo = np.searchsorted(t, a, "right"); hi = np.searchsorted(t, steps, "left")
        stock = np.where(good, cv[np.maximum(ai, 0)] + cs[hi] - cs[lo], -1)
        real = dep[~dep["false"]]
        dps = np.bincount(((real.t0.values - SV.T0) // 600).astype(int), minlength=len(steps))[:len(steps)]
        st, em = good & (stock > 0), good & (stock == 0)
        n = np.bincount(key[st], minlength=576).astype(float); sm = np.bincount(key[st], weights=dps[st], minlength=576)
        lam = np.divide(sm, n, out=np.zeros_like(sm), where=n > 0)
        U[sid] = float(lam[key[em]].sum())
    return SV.net_revenue(S, T, U, G["pilot"])


def pilot_variants(G):
    """other constructions of the pilot's three measures: per-station and per-day ratios, e-bike premium against the
    system's classic fare"""
    S, T, pl = G["S"], G["T"], G["pilot"]
    Rr = T[~T["false"]]
    rp = Rr[Rr.s0.isin(pl["pilot"])]; rc = Rr[Rr.s0.isin(pl["comparison"])]
    per_station = rp.groupby("s0").size().mean() / rc.groupby("s0").size().mean() - 1
    day = lambda x: pd.to_datetime(x.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.date
    dp = rp.groupby(day(rp)).size() / len(pl["pilot"]); dc = rc.groupby(day(rc)).size() / len(pl["comparison"])
    per_day = float((dp / dc).mean() - 1)
    sys_c = Rr[~Rr.ebike].fare.mean()
    out = {"uplift as the mean of per-station rides": dict(pl, i=float(per_station)),
           "uplift as the mean of daily ratios": dict(pl, i=per_day),
           "premium against the system's classic fare": dict(pl, delta=float(pl["f_e"] - sys_c))}
    return out


def main(target, built=None, fig=None, G=None):
    del FAILS[:]
    if built is None:
        import build as B
        tmp = tempfile.mkdtemp()
        built = B.build(tmp)
        shutil.rmtree(tmp)
    if G is None:
        import figs as FG
        fig, G = FG.compute(target)
    W = built["W"]
    S, T = G["S"], G["T"]
    M = pd.read_csv(os.path.join(target, SV.FN["moves"]), dtype={"from_station": str, "to_station": str})
    M["t"] = SV._secs(pd.to_datetime(M.completed_utc))
    A = pd.read_excel(os.path.join(target, SV.FN["audit"]), dtype={"station_id": str})
    A["t"] = [int(dt.datetime.combine(pd.Timestamp(d).date(), dt.time(3, 0), tzinfo=SV.TZ).timestamp()) for d in A.audit_date]
    nr = G["net"]
    code_of = {r["station_id"]: r["k"] for r in built["st"]}

    # ---------------------------------------------------------------- R1: the field's raw material ships
    heads = set()
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads |= set(open(os.path.join(target, f)).readline().strip().lower().split(","))
    bad = [h for h in heads if re.search(r"turn|unmet|demand|request|lost|empty|stockout|availab", h)]
    ok("R1a no shipped column holds the deciding quantity (turned-away requests, demand or availability)", not bad, str(bad))
    ok("R1b the golden reads row-level undocks, docks, van moves and the 03:00 audit",
       len(T) > 900000 and len(M) > 50000 and len(A) == W.ND * 365, "%d trips, %d moves, %d audit rows" % (len(T), len(M), len(A)))
    truthU = {n: float(W.turned[W.area == CODE[n]].sum()) for n in NETS}
    for n in NETS:
        ok("R1c rebuilt turned-away requests within 10 per cent or 300 of the world's for %s" % n,
           abs(nr[n]["turned_away"] - truthU[n]) <= max(0.10 * truthU[n], 300),
           "%.0f against %.0f" % (nr[n]["turned_away"], truthU[n]))

    # ---------------------------------------------------------------- R3a, R3b: the analyst test and the decisive step
    dflt = max(NETS, key=lambda n: nr[n]["default"])
    ok("R3a the easy route (the pilot's uplift on each network's 2025 rides) names Central", dflt == "Central",
       ", ".join("%s %.0f" % (n, nr[n]["default"]) for n in NETS))
    ok("R3a the easy route clears every other network by USD 10,000 or more",
       nr["Central"]["default"] - max(nr[n]["default"] for n in NETS if n != "Central") >= 10000)
    ok("R3b the easy route with only the turned-away requests added files University", G["best"] == "University")
    best_net = nr["University"]["net"]
    ok("R3b University clears every other network by USD 40,000 or more",
       best_net - max(nr[n]["net"] for n in NETS if n != "University") >= 40000,
       "%.0f against %.0f" % (best_net, max(nr[n]["net"] for n in NETS if n != "University")))
    ok("R3b the golden figure is University USD 125,000 to the nearest 25,000", fig["net_revenue"]["University"] == 125000)

    # ---------------------------------------------------------------- the family (Gate C) and its margins
    fam, Us = family(G)
    pv = pilot_variants(G)
    U0 = Us["station x month x weekday-or-weekend x hour"]
    for name, p in pv.items():
        fam[name] = SV.net_revenue(S, T, U0, p)
    # the world with the e-bikes on University: classic-preferring riders take an e-bike when the classic bikes are out
    E = Wd.World(P.SEED_WORLD, eworld="UNI", eb_e=1000).run()
    er = [r for r in E.rides if r[6] == 0 and E.area[r[2]] == "UNI"]
    fare = lambda r: P.UNLOCK + (P.PER_MIN_EBIKE if r[4] == "ebike" else P.PER_MIN_CLASSIC) * np.ceil((r[1] - r[0]) / 60)
    sim_net = sum(fare(r) for r in er) - sum(fare(r) for r in W.rides if r[6] == 0 and W.area[r[2]] == "UNI" and r[4] == "classic")
    ok("SF11 the simulated e-bike world on University (riders take an e-bike when the classic bikes are out) rounds to "
       "the golden", bin25(sim_net) == fig["net_revenue"]["University"], "USD %.0f" % sim_net)
    for n in NETS:
        vals = [nr[n]["net"]] + [f[n]["net"] for f in fam.values()] + ([sim_net] if n == "University" else [])
        m = margin25(vals)
        ok("C1 every standing construction rounds %s to USD %s, clear of the bin's edges" % (n, "{:,}".format(fig["net_revenue"][n])),
           all(bin25(v) == fig["net_revenue"][n] for v in vals) and m >= 2000, "range %.0f to %.0f, margin %.0f" % (min(vals), max(vals), m))
    for name, f in fam.items():
        ok("C2 %s files University" % name, max(NETS, key=lambda n: f[n]["net"]) == "University")
    # the ladder's lower rungs
    lr = lower_rungs(G)
    lr["ten-minute steps, empty-start steps imputed"] = ten_minute_steps(G, M, A)
    for name, f in lr.items():
        pick = max(NETS, key=lambda n: f[n]["net"])
        wrong = pick != "University" or bin25(f["University"]["net"]) != fig["net_revenue"]["University"]
        ok("L1 lower rung '%s' misses (call %s, University USD %.0f)" % (name, pick, f["University"]["net"]), wrong,
           ", ".join("%s %.0f" % (n, f[n]["net"]) for n in NETS))
    ok("L2 the rung that imputes whole empty hours only stays on Central",
       max(NETS, key=lambda n: lr["whole empty hours only"][n]["net"]) == "Central")

    # ---------------------------------------------------------------- R2: every mess item neutral on the call
    # (a) the repeated November hour read at the later offset
    T2 = T.copy()
    amb = pd.to_datetime(T2.t0, unit="s", utc=True).dt.tz_convert(SV.TZ)
    mask = (amb.dt.month == 11) & (amb.dt.day == 2) & (amb.dt.hour == 1)
    ok("R2a the repeated hour of 2 November holds a handful of undocks only", int(mask.sum()) < 60, "%d" % int(mask.sum()))
    # (b) false starts counted as requests
    Tf = T.assign(false=False)
    rbf = SV.rebuild(S, Tf, M, A)[1]
    nf = SV.net_revenue(S, Tf, SV.turned_away(S, rbf, G["keys"][1] * 48 + G["keys"][2] * 24 + G["keys"][0]), G["pilot"])
    ok("R2b false starts read as requests leave the call and every network's figure where they were",
       all(bin25(nf[n]["net"]) == fig["net_revenue"][n] for n in NETS))
    # (c) the dispatch log read as local time breaks the rebuild loudly
    M2 = M.copy(); M2["t"] = M2.t + 6 * 3600
    loud = False
    try:
        SV.rebuild(S, T, M2, A)
    except AssertionError:
        loud = True
    ok("R2c the dispatch log read as local time drives a station's stock below zero (a loud failure)", loud)
    # (d) cents read as dollars on the new platform
    ok("R2d the new platform's fares in cents average over USD 100 when read as dollars (loud)",
       pd.read_csv(os.path.join(target, SV.FN["q3"]), usecols=["fare_cents"]).fare_cents.mean() > 100)
    # (e) every station name and code resolves through the GBFS feed
    ok("R2e every trip's stations resolve through station_information.json", T.s0.notna().all() and T.s1.notna().all())

    # ---------------------------------------------------------------- R3c: no plant
    from pypdf import PdfReader
    txt = {f: "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, f)).pages)
           for f in os.listdir(target) if f.endswith(".pdf")}
    board = txt[P.FILES["board"]]
    ok("R3c the board paper carries no figure for any network and ranks none",
       not re.search(r"USD\s*[\d,]+", board) and "Operations would" not in board)
    ok("R3c no document carries a turned-away, unmet or lost-demand figure",
       not any(re.search(r"turned away|unmet|lost demand|stock-?out", t, re.I) for t in txt.values()))
    days = collections.Counter()
    hourly = T.groupby([pd.to_datetime(T.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.date, "s0"]).size()
    sig = hourly.groupby(level=0).apply(lambda s: tuple(s.values))
    ok("R3c no day of trips repeats another day's station counts (no copied block)", sig.nunique() == len(sig))

    # ---------------------------------------------------------------- SF rows: the fork grid as a cross product
    base = dict(G["pilot"])
    sysc = T[(~T["false"]) & (~T.ebike)].fare.mean()
    grid = []
    for ind, fc_kind, i_kind in itertools.product(["requests", "rides"], ["network", "pilot", "system"],
                                                  ["totals", "per-station", "per-day"]):
        p = dict(base)
        if i_kind == "per-station":
            p["i"] = pv["uplift as the mean of per-station rides"]["i"]
        elif i_kind == "per-day":
            p["i"] = pv["uplift as the mean of daily ratios"]["i"]
        f = SV.net_revenue(S, T, U0, p, induced_on=ind)
        if fc_kind != "network":
            fcv = base["f_c_pilot"] if fc_kind == "pilot" else sysc
            for n in NETS:
                x = f[n]
                base_q = x["requests"] if ind == "requests" else x["rides"]
                x["net"] = (x["turned_away"] + p["i"] * base_q) * fcv + p["X"] * x["requests"] * (1 + p["i"]) * p["delta"]
        grid.append(((ind, fc_kind, i_kind), {n: bin25(f[n]["net"]) for n in NETS}, max(NETS, key=lambda n: f[n]["net"])))
    ok("SF6 SF7 SF8 every cell of the 18-cell grid (induced base x classic fare x uplift construction) keeps the call "
       "and all five figures", all(g[2] == "University" and g[1] == fig["net_revenue"] for g in grid),
       "%d cells" % len(grid))
    gross = {n: nr[n]["requests"] * (1 + base["i"]) * base["X"] * base["f_e"] for n in NETS}
    ok("SF1 net fare revenue read as the e-bikes' gross fares names another network or another figure",
       max(NETS, key=gross.get) != "University" or bin25(gross["University"]) != fig["net_revenue"]["University"])
    ok("SF2 2025 demand read as the rides served names Central (the stump, refuted by the rebuilt stock)",
       max(NETS, key=lambda n: nr[n]["default"]) == "Central")
    ok("SF3 the year is calendar 2025: every trip export starts on or after 1 January and before 1 January 2026",
       T.t0.min() >= SV.T0 and T.t0.max() < SV.T1)
    ok("SF4 fares charged as the fare schedule bills them (USD 1.00 and a started minute at 0.12 or 0.17)",
       np.allclose(T[~T["false"]].fare, 1 + np.where(T[~T["false"]].ebike, 0.17, 0.12) * np.ceil(T[~T["false"]].dur / 60)))
    ok("SF5 the pilot's e-bike share read among rides with an e-bike docked is the same share (an e-bike is docked at a "
       "pilot station for all but a sliver of the year)", W.maxeb.max() >= 8)
    ok("SF9 the rounding is once, at the end: the network figures round from unrounded parts",
       all(fig["net_revenue"][n] == bin25(nr[n]["net"]) for n in NETS))
    ok("SF10 false starts (under 60 seconds back at the same station) are not rides: none bills a fare",
       (T[T["false"]].fare == 0).all() and not ((T.dur < 60) & (T.s0 != T.s1)).any())
    ok("SF12 the pilot's stations come from its note: 24 pilot and 12 comparison stations",
       len(G["pilot"]["pilot"]) == 24 and len(G["pilot"]["comparison"]) == 12)
    ok("SF13 every request served with the e-bikes: the board paper's deployment holds e-bikes at every station",
       "every station holds e-bikes through the day" in re.sub(r"\s+", " ", board))

    # ---------------------------------------------------------------- the asks
    persons = built["persons"]
    truthP = collections.Counter(P.AREA_NAME[p["home"]] for p in persons if any(W.rides[j][6] == 0 for j in p["rides"]))
    ok("A1 people by home area equal the world's riders exactly",
       all(fig["people"][n] == truthP[n] for n in NETS), str({n: (fig["people"][n], truthP[n]) for n in NETS}))
    pa, _ = SV.people(target, T, "accounts"); pc, _ = SV.people(target, T, "cards")
    ok("A2 counting accounts misses every district (re-registrations counted twice)", all(pa.get(n) != fig["people"][n] for n in NETS))
    ok("A3 counting payment cards misses every district (households merged)", all(pc.get(n) != fig["people"][n] for n in NETS))
    ok("A4 the device rows sit in the account register only: re-registrations and shared household cards",
       len(built["rereg"]) > 500 and len(built["house"]) > 100, "%d re-registrations, %d households" % (len(built["rereg"]), len(built["house"])))
    gen = collections.Counter()
    for s in built["sessions"]:
        if not s["replay"]:
            gen[R.loc(s["t1"]).month] += (s["me"] - s["ms"]) / 1000.0
    ok("B1 energy by month equals the genuine sessions exactly",
       all(abs(fig["energy_kwh_exact"][SV_M] - gen[m]) < 0.01 for m, SV_M in enumerate(MONTHS, 1)))
    ea, em = SV.charging(target, "all"), SV.charging(target, "monotone")
    ok("B2 summing every session misses every month", all(int(round(ea[m])) != fig["energy_kwh"][MONTHS[m - 1]] for m in range(1, 13)))
    hits = [m for m in range(1, 13) if int(round(em[m])) == fig["energy_kwh"][MONTHS[m - 1]]]
    ok("B3 a register-must-rise filter misses every month (the first controller was replaced in January)",
       not hits, "hits %s" % hits)
    ok("B4 the re-sent sessions and the controller swaps sit in the charging export only",
       sum(s["replay"] for s in built["sessions"]) > 1000 and len(built["swap"]) == 3)
    Rr = T[~T["false"]]
    qrides = collections.Counter(zip(Rr.ebike.map({True: "ebike", False: "classic"}),
                                     (pd.to_datetime(Rr.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.month - 1) // 3 + 1))
    tj = collections.Counter((j["typ"], (R.loc(j["open"]).month - 1) // 3 + 1) for j in built["jobs"] if not j["retest"])
    ok("C3 workshop jobs per 10,000 rides equal the world's jobs less the road-test retests exactly",
       all(abs(G["workshop"][k][2] - 1e4 * tj[k] / qrides[k]) < 1e-9 for k in G["workshop"]))
    wa, ww = SV.workshop(target, T, "all"), SV.workshop(target, T, "window30")
    ok("C4 counting every job misses every cell", all(round(wa[k][2], 1) != round(G["workshop"][k][2], 1) for k in wa))
    ok("C5 one job per bike and fault within 30 days misses every cell", all(round(ww[k][2], 1) != round(G["workshop"][k][2], 1) for k in ww))
    ridx = collections.defaultdict(list)
    for r in W.rides:
        if r[6] == 0:
            ridx[R.bike_tag(r[5]) if hasattr(R, "bike_tag") else r[5]].append(r[0])
    gaps_ret, gaps_gen, last = [], [], {}
    for j in sorted(built["jobs"], key=lambda j: j["open"]):
        p = last.get(j["bike"])
        if p is not None and p[1] == j["code"]:
            (gaps_ret if j["retest"] else gaps_gen).append((j["open"] - p[0]) / 3600.0)
        last[j["bike"]] = (j["close"], j["code"])
    ok("C6 no time window separates retests from genuine repeats: retests reopen up to %.0f hours after the close, and "
       "%d genuine same-fault repeats come back inside that" % (max(gaps_ret), sum(g <= max(gaps_ret) for g in gaps_gen)),
       len(gaps_ret) > 100 and sum(g <= max(gaps_ret) for g in gaps_gen) >= 5)

    # ---------------------------------------------------------------- the asks' fork rows
    acc = pd.read_csv(os.path.join(target, SV.FN["accounts"]), dtype=str)
    ok("SF14 people are people: accounts on one card riding through the same months stay two, an account opened after "
       "another's last ride on the same card joins it (A1 to A3)", all(fig["people"][n] == truthP[n] for n in NETS))
    ok("SF15 living in: every account's home_area maps to one of seven areas once case and spaces are set aside",
       acc.home_area.str.strip().str.lower().map(SV.AREAS).notna().all())
    fs_only = [a for a in built["accounts"] if a["rides"] and not any(W.rides[j][6] == 0 for j in a["rides"])]
    ok("SF16 rode with us in 2025: accounts whose only records are false starts did not ride (%d of them)" % len(fs_only),
       len(fs_only) > 0)
    cs = pd.read_csv(os.path.join(target, SV.FN["charging"]))
    utc_m = cs.groupby(pd.to_datetime(cs.plug_out_utc).dt.month).energy_kwh.sum()
    ok("SF17 each month is the local month of plug-out (the dictionary): read by UTC month, the natural sum misses "
       "every month", all(int(round(utc_m.get(m, 0))) != fig["energy_kwh"][MONTHS[m - 1]] for m in range(1, 13)))
    zero = cs[cs.meter_start_wh == cs.meter_stop_wh]
    ok("SF18 zero-energy sessions with a repeated register move no month whether kept or dropped",
       abs(zero.energy_kwh.sum()) < 1e-9 and len(zero) > 0)
    jb = pd.read_csv(os.path.join(target, SV.FN["workshop"]))
    o = pd.to_datetime(jb.opened_utc)
    cross = int(((o.dt.tz_convert(SV.TZ).dt.month - 1) // 3 != (o.dt.month - 1) // 3).sum())
    ok("SF19 each quarter runs on Central Time (the dictionary): %d job opens in another quarter by UTC" % cross, cross <= 2)
    ok("SF20 a scrapped bike's job is a job: scrapped jobs are in the golden's count",
       (jb.outcome == "Scrapped").sum() > 0)
    ok("SF21 rides exclude false starts (the dictionary) in the workshop's denominator",
       all(G["workshop"][k][1] == int(((T.ebike == (k[0] == "ebike")) & (~T["false"]) &
                                       ((pd.to_datetime(T.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.month - 1) // 3 + 1 == k[1])).sum())
           for k in G["workshop"]))

    # ---------------------------------------------------------------- separation
    tmp = tempfile.mkdtemp()
    for f in os.listdir(target):
        if f not in (P.FILES["accounts"], P.FILES["charging"], P.FILES["workshop"], P.FILES["opendata"], P.FILES["quote"]):
            shutil.copy(os.path.join(target, f), tmp)
    S2, T3, M3, A3 = SV.load(tmp)
    hrs, rb3 = SV.rebuild(S2, T3, M3, A3)
    H3, Mo3, Wk3, Dw3 = SV.calendar_keys(hrs)
    n3 = SV.net_revenue(S2, T3, SV.turned_away(S2, rb3, Mo3 * 48 + Wk3 * 24 + H3), SV.pilot(S2, T3, tmp))
    shutil.rmtree(tmp)
    ok("S1 the call reads none of the asks' files and neither distractor: deleted, every network's figure is unchanged",
       all(abs(n3[n]["net"] - nr[n]["net"]) < 1e-6 for n in NETS))
    ok("S2 no device row sits in the call's files: the trip exports hold the world's rides and false starts exactly, the "
       "dispatch log its moves", len(T) == len(W.rides) and len(M) == len(W.moves), "%d trips, %d moves" % (len(T), len(M)))

    # ---------------------------------------------------------------- input gates and realism
    files = os.listdir(target)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok("G1 ten or more files in three or more formats", len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3,
       "%d files, %s" % (len(files), sorted({f.rsplit(".", 1)[1] for f in files})))
    ok("G2 a file of 25,000 rows or more", meta["input_gates"]["largest_file_rows"] >= 25000)
    ok("G3 two distractors named in metadata.json and in no file name of the pack as such",
       len(meta["distractor_files"]) >= 2 and all("distract" not in f for f in files))
    caps = {r["station_id"]: r["capacity"] for r in built["st"]}
    ok("G4 no station ever holds more bikes than its capacity", all(W.maxstock[r["k"]] <= r["capacity"] for r in built["st"]))
    ok("G5 the 2027 deployment's e-bikes and the pilot's are separate fleets: Harbour is not a candidate",
       "Harbour keeps the e-bikes of the 2025 pilot" in re.sub(r"\s+", " ", board))
    ok("G6 no em or en dash in any shipped text file",
       not any(re.search("[–—]", open(os.path.join(target, f), encoding="utf-8").read())
               for f in files if f.endswith((".csv", ".json"))) and not any(re.search("[–—]", t) for t in txt.values()))
    # ---------------------------------------------------------------- the realism sweep
    Rr = T[~T["false"]]
    net_of = dict(zip(S.station_id, S.network))
    nm = Rr.groupby([Rr.s0.map(net_of), pd.to_datetime(Rr.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.month]).size()
    ok("RS1 no two months of a network carry the same ride count", all(g.nunique() == len(g) for _, g in nm.groupby(level=0)))
    heads_ = ([nr[n]["rides"] for n in NETS] + [G["pilot"]["rides_pilot"], G["pilot"]["rides_comparison"],
              fig["constants"]["energy_year_kwh"]] + [fig["people"][n] for n in NETS])
    ok("RS2 no headline total is a round thousand", not any(int(x) % 1000 == 0 for x in heads_))
    Mv = pd.read_csv(os.path.join(target, SV.FN["moves"]), dtype=str)
    Ch = pd.read_csv(os.path.join(target, SV.FN["charging"]), dtype=str)
    spread = lambda col: col.str[17:19].value_counts().reindex(["%02d" % i for i in range(60)], fill_value=0)
    flat = {name: spread(col) for name, col in (("dispatch completed", Mv.completed_utc), ("charging plug-in", Ch.plug_in_utc),
                                               ("charging plug-out", Ch.plug_out_utc))}
    ok("RS3 no clock grid: every second of the minute carries 1 to 2.5 per cent of the dispatch and charging stamps",
       all(v.min() / v.sum() > 0.01 and v.max() / v.sum() < 0.025 for v in flat.values()),
       "; ".join("%s %.2f-%.2f%%" % (k, 100 * v.min() / v.sum(), 100 * v.max() / v.sum()) for k, v in flat.items()))
    ek = Mv[Mv.van.str.startswith("E-crew")].copy()
    ek["t"] = pd.to_datetime(ek.completed_utc)
    gaps = ek.groupby(ek.t.dt.tz_convert(SV.TZ).dt.date).t.apply(lambda s: s.sort_values().diff().dt.total_seconds().dropna())
    ok("RS3 the e-bike crew's moves keep no fixed pace (no gap between moves is a third of the gaps)",
       gaps.value_counts(normalize=True).iloc[0] < 1 / 3, "%.1f per cent" % (100 * gaps.value_counts(normalize=True).iloc[0]))
    pts = Ch.point.astype(int).value_counts()
    ok("RS3 riders spread over a station's charging points (busiest point under twice the quietest)",
       pts.max() < 2 * pts.min(), "%d to %d sessions" % (pts.min(), pts.max()))
    modal = A.groupby("station_id").classic_docked.agg(lambda s: s.value_counts(normalize=True).iloc[0])
    ok("RS3 the 03:00 audit is no constant stream: no station shows one count on 85 per cent of mornings",
       modal.max() < 0.85, "busiest count %.0f per cent at most" % (100 * modal.max()))
    first = (Ch.plug_in_utc == pd.Timestamp(SV.T0, unit="s", tz="UTC").strftime("%Y-%m-%dT%H:%M:%SZ")).sum()
    ok("RS3 no pile of sessions at the turn of the year: the e-bikes docked on New Year's Eve carry their own plug-in times",
       first <= 2, "%d at local midnight" % first)
    Jb = pd.read_csv(os.path.join(target, SV.FN["workshop"]), dtype=str)
    ok("RS4 no free text: the workshop's fault column is the label of its fault code",
       Jb.groupby("fault_code").fault.nunique().max() == 1 and Jb.groupby("fault").fault_code.nunique().max() == 1)
    import postprocess
    scr = postprocess._scrubber()
    gold = os.path.join(os.path.dirname(target), "golden")
    bins = [os.path.join(d, f) for d in (target, gold) if os.path.isdir(d) for f in sorted(os.listdir(d))
            if f.endswith((".pdf", ".xlsx", ".docx"))]
    dirty = [(os.path.basename(b), scr.audit(b, postprocess.FLOOR, postprocess.CEILING)) for b in bins]
    ok("RS5 containers scrubbed: no writer's name and no stamp outside the fiction's band in any pack or golden binary",
       all(not n and not b for _, (n, b) in dirty), str([x for x in dirty if x[1][0] or x[1][1]])[:300])
    asof = dt.datetime.combine(P.AS_OF, dt.time(23, 59), tzinfo=SV.TZ)
    late = []
    for f, cols in ((SV.FN["moves"], ["completed_utc"]), (SV.FN["charging"], ["plug_in_utc", "plug_out_utc"]),
                    (SV.FN["workshop"], ["opened_utc", "closed_utc"])):
        X = pd.read_csv(os.path.join(target, f), usecols=cols)
        late += [(f, c) for c in cols if pd.to_datetime(X[c]).max() > asof]
    Ac = pd.read_csv(os.path.join(target, SV.FN["accounts"]), usecols=["created_at", "closed_at"])
    late += [(SV.FN["accounts"], c) for c in ("created_at", "closed_at")
             if pd.to_datetime(Ac[c].dropna()).max() > pd.Timestamp("2025-12-31 23:59:59")]
    months = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                          "September", "October", "November", "December"], 1)}
    allow = {(9, 12, 2026), (15, 1, 2027), (1, 4, 2027), (31, 1, 2027)}   # the meeting, the order, the season, the quote's validity
    for f, t_ in txt.items():
        for d_, m_, y_ in re.findall(r"\b(\d{1,2}) (%s) (\d{4})\b" % "|".join(months), t_):
            when = dt.date(int(y_), months[m_], int(d_))
            if when > P.AS_OF and (int(d_), months[m_], int(y_)) not in allow:
                late.append((f, "%s %s %s" % (d_, m_, y_)))
    ok("RS6 dates coherent: no record after its extract and no document date after the folder's, but the forward dates "
       "the paper and the quotation name", not late, str(late))
    for n in NETS:
        print("     %-10s golden %9.0f  rounded %7d  recorded-route %8.0f" % (n, nr[n]["net"], fig["net_revenue"][n], nr[n]["default"]))
    print("%d failure(s)" % len(FAILS))
    return len(FAILS)


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

if __name__ == "__main__":
    import sys
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target")) else 0)
