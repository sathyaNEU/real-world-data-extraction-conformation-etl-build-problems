"""task251 generator checks: the input gates, the call against the world's truth with its ladder and margins, the
closure across every estimator form, the three rules on the clean truth, every semantic fork row, the separation line
and the deletion tests, the asks against the database's truth with their devices, the documents read back, the
realism sweep and the dates.
    C.run(target, world, fig, golden) -> number of assertions passed"""
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd
from pypdf import PdfReader

import build as B
import params as P
import records as RC
import routes as RT
import sim
import solve as S

N_OK = [0]
MARGIN = 0.01                       # every converter at least a point from 95 per cent under every licensed form
GOLD = ["BP01", "BP02", "BP03", "BP04", "BP05", "BP08", "BP13"]


def ok(cond, msg):
    assert cond, msg
    N_OK[0] += 1


def _pdf_text(path):
    return " ".join("\n".join(p.extract_text() for p in PdfReader(path).pages).split())


def _truth_call(W, years=(2025, 2026, 2027)):
    """each station analyzer's converter at its 2028 service on the world's own curve: its true NO2 reduced to the end of
    2027 plus the station's true NO2 over the same days of the given years"""
    out = {}
    for i, st in enumerate(sim.STATIONS):
        a = W["analyzers"][st[5]]
        cur = a["converters"][-1]
        d_now = float(a["D"][sim.HOURS - 1])
        until = W["svc"][st[0]]["scheduled"][3]
        per = []
        for y in years:
            k0 = (dt.date(y, 1, 1) - P.START).days
            k1 = (dt.date(y, until.month, until.day) - P.START).days
            per.append(W["no2"][i, k0 * 24:k1 * 24].sum() / P.UGM3_PER_PPB_NO2 / 1000.0)
        out[st[0]] = float(sim.eta(d_now + np.mean(per), cur["s"]))
    return out


def _age_route(W):
    """the default path on the world's own checks: every titration against its converter's age, pooled, a quadratic,
    each converter in service carried to its service at its age then"""
    inst = {s: [c["installed"] for c in a["converters"]] for s, a in W["analyzers"].items()}
    ages = np.array([t[0] - inst[t[1]][t[7]] for t in W["titrations"]])
    eff = np.array([t[5] for t in W["titrations"]])
    b = np.polyfit(ages, eff, 2)
    out = []
    for st in sim.STATIONS:
        k_svc = (W["svc"][st[0]]["scheduled"][3] - P.START).days
        if np.polyval(b, k_svc - inst[st[5]][-1]) < P.THRESHOLD:
            out.append(st[0])
    return sorted(out)


def _dose_route(W, years=(2025, 2026, 2027)):
    """the decisive step alone on the world's own checks: the same titrations against the NO2 their converter had
    reduced, the curve with its knee, each converter carried on its station's load"""
    tD = np.array([t[3] for t in W["titrations"]])
    tE = np.array([t[5] for t in W["titrations"]])
    best = None
    for kn in np.arange(30.0, 220.0, 2.5):
        X = np.c_[np.ones_like(tD), tD, np.maximum(0, tD - kn) ** 2]
        c, *_ = np.linalg.lstsq(X, tE, rcond=None)
        r = ((X @ c - tE) ** 2).sum()
        if best is None or r < best[0]:
            best = (r, kn, c)
    _, kn, c = best
    out = []
    for i, st in enumerate(sim.STATIONS):
        a = W["analyzers"][st[5]]
        d_now = float(a["D"][sim.HOURS - 1])
        until = W["svc"][st[0]]["scheduled"][3]
        per = []
        for y in years:
            k0 = (dt.date(y, 1, 1) - P.START).days
            k1 = (dt.date(y, until.month, until.day) - P.START).days
            per.append(W["no2"][i, k0 * 24:k1 * 24].sum() / P.UGM3_PER_PPB_NO2 / 1000.0)
        x = d_now + np.mean(per)
        if c[0] + c[1] * x + c[2] * max(0.0, x - kn) ** 2 < P.THRESHOLD:
            out.append(st[0])
    return sorted(out)


def run(target, world, fig, golden):
    N_OK[0] = 0
    F = {k: os.path.join(target, v) for k, v in B.FILES.items()}
    W, R = world["W"], world["R"]
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "metadata.json")))

    # ---------------------------------------------------------------- input gates
    ok(len(files) == len(B.FILES) >= 10, "ten or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    n_arc = sum(1 for _ in open(F["archive"], encoding="utf-8")) - 1
    ok(n_arc >= 25000, "a file of 25,000 rows or more (%d)" % n_arc)
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors shipped")
    ok(not any(w in f.lower() for f in files for w in ("distract", "decoy", "trap", "golden")), "no file named for its role")

    # ---------------------------------------------------------------- the call against the truth
    D = S.load(target, B.FILES)
    call = S.call(D)
    T = call["table"].set_index("station")
    gold = call["goes"]
    ok(gold == GOLD, "the golden list: %s" % gold)
    truth = _truth_call(W)
    t_set = sorted(s for s, e in truth.items() if e < P.THRESHOLD)
    ok(t_set == gold, "the golden list is the world's truth: %s" % t_set)
    ok(min(abs(e - P.THRESHOLD) for e in truth.values()) >= 0.015, "every true efficiency at service 1.5 points or "
       "more from 95 per cent")
    for yrs in ((2026, 2027), (2027,)):
        ok(sorted(s for s, e in _truth_call(W, yrs).items() if e < P.THRESHOLD) == gold,
           "the truth under the %s load holds the list" % (yrs,))
    ok(fig["call"]["bench"] == gold and fig["call"]["count"] == 7 and fig["call"]["stays"] == 9,
       "figures.json carries the list")
    ok(len(T) == 16 and T["serial"].is_unique, "sixteen station analyzers, one converter in service each")
    ok(all(abs(T.loc[s, "eta_service"] - truth[s]) < 0.03 for s in T.index), "every estimate within 3 points of truth")

    # ---------------------------------------------------------------- the ladder and the closure
    r, TR = RT.all_routes(D)
    for nm in RT.GOLDEN_FAMILY:
        ok(r[nm] == gold, "closure: %s files the golden list" % nm)
    for nm in RT.REFLEXES:
        ok(r[nm] != gold, "ladder: %s files another list %s" % (nm, r[nm]))
    ok(r["latest_titration"] == [], "the latest titration books none")
    ok(r["pooled_age_quadratic"] == ["BP08"], "the default path: the age curve books BP08 alone")
    ok(r["own_trend_in_time"] == ["BP02", "BP04"], "each converter's own line in time books BP02 and BP04")
    ok(r["pooled_line_in_NO2_converted"] == ["BP01", "BP02"], "a straight line in NO2 converted books BP01 and BP02")
    ok(r["efficiency_today"] == ["BP01"], "the efficiency today books BP01 alone")
    ok(r["pooled_curve_recent_rate"] == sorted(gold + ["BP14"]), "the last 90 days' rate adds BP14")
    marg = 1.0
    for v in S.VARIANTS:
        C = S.call(D, **v)
        ok(C["goes"] == gold, "closure: variant %s" % v)
        marg = min(marg, float((C["table"]["eta_service"] - S.TH).abs().min()))
    ok(marg >= MARGIN, "every converter %.1f points or more from 95 per cent under every form (%.4f)" % (100 * MARGIN,
                                                                                                       marg))
    # the further forms: exponential, power, the quarterly checks alone, the dose corrected for the converter's loss
    P_ = call["points"]
    x, y = P_["D"].to_numpy(), P_["eta"].to_numpy()

    def fit_form(kind):
        best = None
        grid = np.arange(20, 400, 2.0) if kind == "exp" else np.arange(1.0, 6.0, 0.05)
        for g in grid:
            X = np.c_[np.ones_like(x), (np.exp(x / g) - 1) if kind == "exp" else x ** g]
            c, *_ = np.linalg.lstsq(X, y, rcond=None)
            rr = ((X @ c - y) ** 2).sum()
            if best is None or rr < best[0]:
                best = (rr, g, c)
        _, g, c = best
        return (lambda z: c[0] + c[1] * (np.exp(z / g) - 1)) if kind == "exp" else (lambda z: c[0] + c[1] * z ** g)

    for kind in ("exp", "pow"):
        f = fit_form(kind)
        e = np.array([f(d) for d in T["D_service"]])
        ok(sorted(T.index[e < S.TH]) == gold and np.abs(e - S.TH).min() >= MARGIN, "closure: the %s form" % kind)
    q = P_[P_["kind"] == "trimestrale"]
    f = S.fit(q, "pw", True)
    e = np.array([f(d) for d in T["D_service"]])
    ok(sorted(T.index[e < S.TH]) == gold, "closure: the quarterly checks alone")
    ser = S.series(D)
    ch = S.changes(D)
    f0 = call["curve"]

    def dose_corr(serial, t0, t1):
        t, v = ser[serial]
        i0, i1 = np.searchsorted(t, np.datetime64(t0)), np.searchsorted(t, np.datetime64(t1))
        dc = 0.0
        for val in v[i0:i1]:
            dc += val / 1000.0 / max(0.5, float(f0(dc)))
        return dc

    pts = []
    for p in P_.itertuples(index=False):
        if p.kind == "post-sostituzione":
            pts.append(0.0)
            continue
        inst = [c for c in ch[p.serial] if S.change_time(c) <= p.start]
        pts.append(dose_corr(p.serial, S.change_time(inst[-1]), p.start))
    f2 = S.fit(P_.assign(D=pts), "pw", True)
    e = np.array([f2(dose_corr(T.loc[s, "serial"], S.change_time(T.loc[s, "installed"]), call["t_end"]) +
                     T.loc[s, "D_future"] / 0.97) for s in T.index])
    ok(sorted(T.index[e < S.TH]) == gold, "closure: the dose corrected for each converter's own loss")

    # ---------------------------------------------------------------- the three rules on the clean truth
    ok(_age_route(W) == ["BP08"], "analyst test: the age curve on the world's own checks books BP08 alone")
    ok(_dose_route(W) == gold, "analyst test: turning the clock to NO2 converted alone books the seven")

    # ---------------------------------------------------------------- semantic fork rows
    tb = pd.read_csv(F["titr_b"])
    eb = ((tb.nox_finale_ppb - tb.no_finale_ppb) - (tb.nox_iniziale_ppb - tb.no_iniziale_ppb)) / \
        (tb.no_iniziale_ppb - tb.no_finale_ppb)
    ok((eb - tb.efficienza).abs().max() < 1e-4, "SF1 Delta's efficienza repeats the computed ratio")
    pa = P_[P_["who"] == "A"]
    ok((pa["eta"] - pa["eta_printed"]).abs().max() < 6e-4, "SF1 Tecnoaria's percentage rounds the ratio")
    ok(S.call(D, col="eta_printed")["goes"] == gold, "SF1 the printed efficiencies hold the call")
    ok(marg >= MARGIN, "SF2 no converter within a point of 0.95 on any golden form")
    plan = D["plan"].copy()
    D3 = dict(D, plan=plan.assign(manutenzione_2028=[d - dt.timedelta(days=1) for d in plan["manutenzione_2028"]]))
    ok(S.call(D3)["goes"] == gold, "SF3 the day before the service holds the call")
    p4 = plan.copy()
    p4.loc[p4["stazione"] == "BP08", "manutenzione_2028"] = dt.date(2027, 10, 13) + dt.timedelta(days=365)
    ok(S.call(dict(D, plan=p4))["goes"] == gold, "SF4 BP08 goes on its anniversary too")
    ok(plan.set_index("stazione").loc["BP08", "manutenzione_2028"] == dt.date(2028, 2, 15), "SF4 BP08 on 15 February")
    spare = W["analyzers"][sim.SPARE]
    e_sp = float(sim.eta(spare["D"][sim.HOURS - 1], spare["converters"][-1]["s"]))
    ok(e_sp > 0.98 and sim.SPARE not in set(T["serial"]), "SF5 the spare is out and its converter far from 95")
    for serial in T["serial"]:
        for c in ch[serial][1:]:
            ok(((P_["serial"] == serial) & (P_["kind"] == "post-sostituzione") &
                (P_["start"].dt.date == c)).any(), "SF6 %s's change on %s carries a post titration" % (serial, c))
    ok(S.call(D, stato0=True)["goes"] == gold, "SF7 measuring hours only")
    raw = pd.read_csv(F["archive"], dtype={"matricola": str})
    raw["t"] = pd.to_datetime(raw["data_ora_utc"], format="%Y-%m-%d %H:%M")
    raw = raw.sort_values(["matricola", "t"], kind="mergesort")
    ok(len(raw) > len(D["arc"]) and S.call(dict(D, arc=raw))["goes"] == gold, "SF8 the raw rows summed hold the call")
    for v in (dict(years=(2027,)), dict(years=(2026, 2027))):
        ok(S.call(D, **v)["goes"] == gold, "SF9 %s" % v)
    ok(r["pooled_curve_year_rate"] == gold, "SF9 the year's mean rate")
    for v in (dict(form="p3"), dict(form="p2")):
        ok(S.call(D, **v)["goes"] == gold, "SF10 %s" % v)
    for v in (dict(at=0), dict(at=23)):
        ok(S.call(D, **v)["goes"] == gold, "SF11 %s" % v)
    tit = D["tit"].copy()
    for off in (1, 2):
        D12 = dict(D, tit=tit.assign(start=tit["start"] + dt.timedelta(hours=off), end=tit["end"] + dt.timedelta(hours=off)))
        ok(S.call(D12)["goes"] == gold, "SF12 the sheets read %d hour(s) off" % off)
    ok(D["arc"]["t"].max() == dt.datetime(2027, 12, 31, 22, 0), "SF13 the archive ends with 2027")
    ok(S.call(D, post=False)["goes"] == gold, "SF14 the fresh converters' checks left out")
    ok(len(gold) <= 10, "SF15 the laboratory's ceiling of ten does not bind")
    ok(T.loc["BP01", "eta_now"] < S.TH and T.loc["BP01", "service"] == dt.date(2028, 1, 20) and "BP01" in gold,
       "SF16 SF17 BP01 below 95 already, its service in the bench week, booked")
    mail = open(F["mail"], encoding="utf-8").read()
    ok("Date: Tue, 04 Jan 2028" in mail and "17 al 21 gennaio" in mail and "dieci" in mail, "SF18 the as-of and bench")
    short = 0
    for v in R["visits"] + R["service_windows"]:
        s0, e0 = v["start"], v["end"]
        h = s0.replace(minute=0)
        while h < e0:
            if (min(e0, h + dt.timedelta(hours=1)) - max(s0, h)).total_seconds() / 60 <= 15:
                short += 1
            h += dt.timedelta(hours=1)
    ok(short == 0, "SF19 every hour a visit touches holds 16 minutes of it or more")
    dic = open(F["dictionary"], encoding="utf-8").read()
    ok("R valido" in dic and "N misura per meno di 45 minuti" in dic, "SF20 R valid, N under 45 minutes")
    db = D["db"]
    mag = db[db["stazione"] == "MAG"]
    ok(mag["t"].min() >= dt.datetime(2027, 2, 8) and mag["t"].max() < dt.datetime(2027, 3, 2),
       "SF21 MAG rows only inside the BP07 stint")
    bp07 = db[(db["stazione"] == "BP07") & db["t"].isin(set(mag["t"]))]
    ok(len(bp07) == len(mag) and (bp07["codice"] == "F").all(), "SF21 BP07 not received in every MAG hour")
    A0 = S.asks(D)
    A1 = S.asks(D, logger="archive")
    old = S.UGL
    S.UGL = 1.91 * 293.15 / 273.15
    A2 = S.asks(D)
    S.UGL = old

    def edge(x, nd):
        s_ = x * 10 ** nd
        return abs(s_ - np.floor(s_) - 0.5)

    for s in A0:
        ok(len({round(a[s]["mean"], 1) for a in (A0, A1, A2)}) == 1, "SF22 %s mean agrees on every route" % s)
        ok(len({round(a[s]["p19"]) for a in (A0, A1, A2)}) == 1, "SF22 %s 19th agrees on every route" % s)
        ok(min(edge(a[s]["mean"], 1) for a in (A0, A1, A2)) >= 0.1, "%s mean clear of its rounding edge" % s)
        ok(min(edge(a[s]["p19"], 0) for a in (A0, A1, A2)) >= 0.07, "%s 19th clear of its rounding edge" % s)
    H = S.station_hours(D)
    for s, h in H.items():
        v = np.sort(h["v"].to_numpy())[::-1]
        ok(abs(v[18] - A0[s]["p19"]) < 1e-9, "SF23 %s 19th by value" % s)
    ok(not ((P_["eta"] - 0.965).abs() < 6e-4).any() and not ((P_["eta"] - 0.975).abs() < 6e-4).any(),
       "components: no titration at the 96.5 or 97.5 per cent edges")

    # ---------------------------------------------------------------- separation and deletion
    Dn = dict(D, db=None)
    ok(S.call(Dn)["goes"] == gold, "the call never reads the database")
    db_cols = set(pd.read_csv(F["database"], sep=";", nrows=2).columns)
    ok(not (db_cols & {"matricola", "no2_ppb"}), "the database carries no analyzer column the call reads")

    # ---------------------------------------------------------------- the asks against the truth
    tr = R["database_truth"].copy()
    tr.loc[tr["stazione"] == "MAG", "stazione"] = "BP07"
    val = tr[tr["kind"].isin(["air", "spare"])]
    for s in sim.STATIONS:
        code = s[0]
        g = val[val["stazione"] == code]["no2_20c"].to_numpy(dtype=float)
        g = np.sort(g)[::-1]
        ok(len(g) == fig["asks"]["valid_hours_2027"][code], "ask A %s: %d valid hours, the truth" % (code, len(g)))
        ok(round(g.mean(), 1) == fig["asks"]["mean_2027_ugm3"][code], "ask B %s: mean %.3f, the truth" % (code,
                                                                                                         g.mean()))
        ok(int(round(g[18])) == fig["asks"]["p19_2027_ugm3"][code], "ask C %s: 19th %.2f, the truth" % (code, g[18]))

    def moved(p, key, nd=None):
        return sum(1 for s in A0 if (round(p[s][key], nd) if nd is not None else p[s][key]) !=
                   (round(A0[s][key], nd) if nd is not None else A0[s][key]))

    nat = S.asks(D, gpt=False, spare=False, logger=None)
    ok(moved(nat, "valid") == 16 and moved(nat, "mean", 1) >= 13 and moved(nat, "p19", 0) >= 13,
       "the database as delivered misses every valid hour and most means and 19th values")
    ok(moved(S.asks(D, gpt=False), "valid") == 16, "the titration hours move every station's valid hours")
    nsp = S.asks(D, spare=False)
    ok(moved(nsp, "valid") == 1 and nsp["BP07"]["valid"] < A0["BP07"]["valid"] - 400, "MAG moves BP07's valid hours")
    ok(moved(S.asks(D, logger=None), "mean", 1) == 6, "the 0 degrees C loggers move six means")
    ok(moved(S.asks(D, r_valid=False), "valid") >= 10, "R read as not valid moves most stations")
    ok(sum(R["database"].duplicated()) == 72, "three re-sent days, exact")

    # ---------------------------------------------------------------- documents, realism, dates
    man = _pdf_text(F["manual"])
    for w in ("45 minuti", "95 per cento", "manutenzione programmata", "19", "1,91"):
        ok(w in man, "the manual files %r" % w)
    for w in (r"ppm", r"consum\w*", r"convertit[oa]", r"caric\w*", r"età", r"scorta che", r"MAG"):
        ok(re.search(r"\b%s\b" % w, man) is None, "the manual never says %r" % w)
    ok(re.search(r"(?<![\d,])0 °C", man) is None, "the manual never names 0 degrees C")
    for w in (r"(?<![\d,])0 °C", r"senza modo taratura", r"spare"):
        ok(re.search(w, dic) is None, "the dictionary never says %r" % w)
    ok("MAG" not in dic.split("## " + B.FILES["database"])[1].split("## ")[0], "the database's entry never names MAG")
    arc_txt = open(F["archive"], encoding="utf-8").read(2_000_000)
    ok("-0.00" not in arc_txt and "nan" not in arc_txt.lower(), "no negative zero or nan in the archive")
    db_txt = open(F["database"], encoding="utf-8").read()
    ok(re.search(r";\d+,\d;", db_txt) is not None and re.search(r";\d+\.\d;", db_txt) is None,
       "the database's values carry a decimal comma")
    ok(max(pd.to_datetime(R["service_log"]["data"])) <= pd.Timestamp("2027-12-31"), "no intervention after 2027")
    ok(all(d <= dt.date(2028, 12, 31) for d in D["plan"]["manutenzione_2028"]), "the plan within 2028")
    ok(fig["components"]["latest_checks_below_95"] == 0, "no converter in service below 95 at its latest check")
    return N_OK[0]
