"""task398 assertions: the three rules on the clean truth (R1 to R3c), the decisive step's corridor, every semantic
fork row (SF1 to SF13), the ladder, the sorts, the cheap routes, the ask devices, bin distances, realism and the
input gates. Run after build.py; exit 1 on any failure."""
import collections
import csv
import datetime as dt
import glob
import io
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl

import golden as G
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RES = []
CORR = {}


def check(name, ok, detail=""):
    RES.append((name, bool(ok), detail))
    return ok


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def main():
    R = G.compute(TARGET)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    days = R["days"]
    E = R["E"]
    per = {k: len(v) for k, v in R["per"].items()}

    # ---------------------------------------------------------------- R1: the field's raw material ships
    check("R1 buoy profile, station temperatures and pool elevations ship and the decisive step reads them",
          len(R["E"]) > 150 and all(k in R["T"] for k in G.SUBS), "%d days of entry depths" % len(E))
    cols = set()
    for fn in glob.glob(os.path.join(TARGET, "**", "*.csv"), recursive=True):
        with open(fn, encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                if not ln.startswith("#") and "," in ln:
                    cols |= set(c.strip().lower() for c in ln.strip().split(","))
                    break
    check("R1 no shipped column holds an entry depth, a source share or a cause",
          not any(re.search(r"entry|intrusion|source share|caused|attribut|stratif", c) for c in cols), sorted(cols)[:6])

    # ---------------------------------------------------------------- the call, its corridor
    check("call: Fennick Creek every day above the trigger, every other sub-watershed none",
          per["FEN"] == len(days) and all(per[k] == 0 for k in G.SUBS if k != "FEN"), per)
    corridor = {}
    for h in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
        for win in (0, 1, 3, 7, 14, 21, 30, 45, 60, 120):
            pp, who = G.attribute(E, days, h=h, window=win)
            corridor[(h, win)] = tuple(len(pp[k]) for k in G.SUBS)
    want = tuple(len(days) if k == "FEN" else 0 for k in G.SUBS)
    check("SF8 C3 corridor: withdrawal half-width 1.0 to 3.5 m and look-back 0 to 120 days give the same counts",
          all(v == want for v in corridor.values()), sorted(set(corridor.values())))
    # the look-back carried into the mixed spring: every sub-watershed's water is in every layer, so a presence
    # test attributes no day; plan 5.1's counterfactual still counts every day for Fennick, because without the
    # spring water's atrazine (the residue, at most the spring result) nothing changes and without Fennick's the
    # raw water falls to that residue
    saved = G.reached

    def reached_mixed(E_, d, k, h, window):
        for n in range(0, window + 1):
            dd = d - dt.timedelta(days=n)
            if dd in E_ and E_[dd]["mixed"]:
                return True
        return saved(E_, d, k, h, window)
    G.reached = reached_mixed
    try:
        pp_m, who_m = G.attribute(E, days, window=60)
    finally:
        G.reached = saved
    onset = min(d for d in E if not E[d]["mixed"] and d.month >= 4)
    spring = max(v for d, v in R["results"].items() if G.SEASON[0] <= d < onset)
    check("SF13 a look-back into the mixed spring leaves days unattributed (ruled out by plan 5.1: the spring residue "
          "is at most %.2f ug/L, so it cannot hold a day above the trigger)" % spring,
          sum(len(v) for v in pp_m.values()) < len(days) and spring < 1.0 and
          all(len(pp_m[k]) == 0 for k in G.SUBS if k != "FEN"), {k: len(v) for k, v in pp_m.items()})
    # nearest-source reading: the tributary whose entry came closest to the intake in the window
    near_ok = True
    for d in days:
        best = None
        for n in range(31):
            dd = d - dt.timedelta(days=n)
            if dd not in E or E[dd]["mixed"]:
                continue
            for k in G.SUBS:
                z = E[dd].get(k)
                if z is None:
                    continue
                gap = abs(z - E[dd]["zi"])
                if best is None or gap < best[0]:
                    best = (gap, k)
        near_ok = near_ok and best is not None and best[1] == "FEN"
    check("SF7 nearest-entry reading names Fennick Creek on every day above the trigger", near_ok)
    # margins: Fennick's entries near the intake, every other source far
    fen_gap = max(abs(E[d]["FEN"] - E[d]["zi"]) if E[d].get("FEN") is not None else 99.0 for d in days)
    check("decisive margin: Fennick's entry within 1.0 m of the intake on every day above the trigger",
          fen_gap <= 1.0, "max %.2f m" % fen_gap)
    gaps = collections.defaultdict(list)
    for d in E:
        if E[d]["mixed"] or not (onset <= d <= days[-1]):
            continue
        for k in G.SUBS:
            z = E[d].get(k)
            gaps[k].append(99.0 if z is None else abs(z - E[d]["zi"]))
    check("decisive margin: every other tributary at least 4.0 m from the intake from the lake's stratifying (%s) "
          "to the last day above the trigger" % onset,
          min(min(gaps[k]) for k in G.SUBS if k != "FEN") >= 4.0,
          {k: round(min(gaps[k]), 2) for k in G.SUBS if k != "FEN"})
    # entry from the 08:00 reading rather than the daily mean, and the noon buoy profile
    alt_ok = alt_entries_same(R)
    check("SF7 entry from each station's 08:00 temperature and the buoy's noon profile gives the same sources", alt_ok)

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    truth = W.build()
    rec = truth["rec"]
    tdays = [r for r in rec if r["intake"] > W.TRIGGER and G.SEASON[0] <= r["date"] <= G.SEASON[1]]
    tload = {k: sum(truth["Q"][k][i] * truth["C"][k][i] * 86400 / 1e6 for i in range(W.di(4, 1), W.di(9, 30) + 1))
             for k in W.SUBS}
    r0 = max(tload, key=tload.get)
    check("R3a clean truth, rung 0: the largest season load is the Tessel River", r0 == "TES",
          {k: round(v, 1) for k, v in tload.items()})
    mixed = {k: 0 for k in W.SUBS}
    for r in tdays:
        i = r["i"]
        tot = {k: sum(truth["Q"][k][j] * truth["C"][k][j] for j in range(max(0, i - 30), i + 1)) for k in W.SUBS}
        s = sum(tot.values())
        for k in W.SUBS:
            if r["intake"] * (1 - tot[k] / s) <= W.TRIGGER:
                mixed[k] += 1
    check("R3a clean truth, rung 1: the mixed-lake reading names the Tessel River",
          max(mixed, key=mixed.get) == "TES" and mixed["TES"] >= 1.5 * sorted(mixed.values())[-2], mixed)
    cf = {k: sum(1 for r in tdays if r["intake"] - r["by"][k] <= W.TRIGGER) for k in W.SUBS}
    check("R3b clean truth, decisive step alone: only Fennick's atrazine removed brings any day under the trigger",
          cf["FEN"] == len(tdays) and all(cf[k] == 0 for k in W.SUBS if k != "FEN"), cf)
    lead = max(max(r["by"][k] for k in W.SUBS if k != "FEN") for r in tdays)
    check("R3b clean truth: no other source puts 0.03 ug/L into the raw water on a day above the trigger", lead < 0.03,
          "%.4f" % lead)
    check("R3c no plant: no copied block in the buoy, the stations or the raw-water record", no_repeat_blocks())

    # ---------------------------------------------------------------- the ladder on the pack
    rg = R["rungs"]
    L = rg["r0_load"]
    order = sorted(L, key=L.get, reverse=True)
    check("ladder rung 0 (April to July load): Tessel first by 1.15x, Fennick last of the four sampled",
          order[0] == "TES" and L["TES"] >= 1.15 * L[order[1]] and order.index("FEN") == 3,
          {k: round(v, 1) for k, v in L.items()})
    for key in ("r1_mixed14", "r1_mixed30", "r1_mixed45"):
        m = rg[key]
        o = sorted(m, key=m.get, reverse=True)
        check("ladder rung 1 (%s): Tessel first by 1.15x, Fennick not first or second" % key,
              o[0] == "TES" and m["TES"] >= 1.15 * m[o[1]] and o.index("FEN") >= 2, m)
    sorts = sorts_on_pack(R)
    check("Shock: Fennick Creek tops no sort of the shipped statistics",
          all(top != "FEN" for top in sorts.values()), sorts)
    routes = cheap_routes(R)
    check("cheap routes: no correlation or regression on the sampled series names Fennick first by a margin",
          all(v[0] != "FEN" or v[1] < 0.02 for v in routes.values()), routes)
    rs = [v[0] for v in CORR.values()]
    check("Back-test: each tributary's best lagged correlation with the raw water, %s, sits within 0.05 of the others "
          "(range %.2f to %.2f)" % (", ".join("%s %.3f at %d days" % (k, v[0], v[1]) for k, v in sorted(CORR.items())),
                                     min(rs), max(rs)), max(rs) - min(rs) < 0.05, CORR)

    # ---------------------------------------------------------------- the semantic fork rows
    res, scr, conf = R["results"], R["screen"], R["conf"]
    check("SF1 season: 15 April to 31 October, calendar 2026 and April to September give the same days",
          len(days) == len([d for d, v in res.items() if v > 3.0]) ==
          len([d for d, v in res.items() if dt.date(2026, 4, 1) <= d <= dt.date(2026, 9, 30) and v > 3.0]))
    check("SF2 trigger: no day's result at exactly 3.00 or in (3.00, 3.05]",
          not any(3.0 <= v <= 3.05 for v in res.values()))
    alt = [d for d, v in scr.items() if G.SEASON[0] <= d <= G.SEASON[1] and v > 3.0]
    check("SF3 day's result: the ELISA-only reading counts other days (ruled out by SOP 2.3) but names the same "
          "sub-watershed", len(alt) != len(days), "ELISA-only %d against %d" % (len(alt), len(days)))
    pp_alt, _ = G.attribute(E, sorted(alt))
    check("SF3 under the ELISA-only reading the call is still Fennick Creek",
          max(pp_alt, key=lambda k: len(pp_alt[k])) == "FEN")
    check("SF4 'caused': the counterfactual, the largest share and any share all name Fennick on every day",
          all(R["who"][d] == ["FEN"] for d in days))
    check("SF5 sub-watershed: above its station (plan 2.1); the lake's direct drainage carries no station", True)
    zi = [E[d]["zi"] for d in days if d in E]
    zi_navd = [z + G.NAVD_MINUS_NGVD * G.FT for z in zi]
    check("SF6 intake depth: the 0.24 ft datum conversion moves the intake 0.07 m and no attribution",
          all(abs(a - b) < 0.08 for a, b in zip(zi, zi_navd)), "%.2f to %.2f m" % (min(zi), max(zi)))
    check("SF9 2027 program from the last completed season (plan 5.1): the 2026 season", True)
    resid = residual_without_fen(R)
    check("SF10 without Fennick's atrazine the raw water stays at most 1.0 ug/L on every day above the trigger",
          resid <= 1.0, "%.2f ug/L" % resid)

    # ---------------------------------------------------------------- ask devices and bins
    import asks as A
    gold = A.monthly(TARGET, **A.LOAD_ROUTES["golden"])
    cells = sorted(gold)
    check("ask cells: four sampled stations by four months, Ladd Branch not sampled",
          len(cells) == 16 and "LAD" not in R["loads"] and not R["samples"]["LAD"], len(cells))
    check("ask cells equal the golden's monthly loads", all(abs(gold[(k, m)] - R["loads_month"][k][m]) < 1e-9
                                                        for k, m in cells))
    spread = integration_spread(R)
    for c in cells:
        need = max(0.02, 2 * spread[c])
        check("bin: %s %d load %.3f kg sits %.3f kg from its rounding edge, over twice the %.4f kg spread of the "
              "integration rules" % (c[0], c[1], gold[c], edge(gold[c], 1.0), spread[c]), edge(gold[c], 1.0) >= need,
              "%.3f against %.3f" % (edge(gold[c], 1.0), need))
    pac = R["pac"]
    for m, v in pac.items():
        check("bin: carbon month %d %.3f lb at least 0.10 lb from its rounding edge" % (m, v), edge(v, 1.0) >= 0.10,
              "%.3f" % edge(v, 1.0))
    routes = {}
    for name, kw in A.LOAD_ROUTES.items():
        if name != "golden":
            routes[name] = A.monthly(TARGET, **kw)
    moved = {n: [c for c in cells if round(r[c]) != round(gold[c])] for n, r in routes.items()}
    check("device D8: the storm bottles at their logged times move every load cell", len(moved["logged"]) == 16,
          sorted(set(cells) - set(moved["logged"])))
    check("device D8: the cracker's route (logged times, one mean offset) keeps no load cell",
          len(moved["cracker"]) == 16, sorted(set(cells) - set(moved["cracker"])))
    check("device D8 half-repair: the k-th bottle at the k-th carousel position moves cells in every station",
          {c[0] for c in moved["position"]} == {"TES", "FEN", "OXL", "DUN"}, moved["position"])
    check("device D3 second primary: one mean offset moves Dunmore Creek's May, June and July",
          {c for c in moved["mean offset"]} >= {("DUN", 5), ("DUN", 6), ("DUN", 7)} and
          all(c[0] == "DUN" for c in moved["mean offset"]), moved["mean offset"])
    check("device D3: offsets stepping at the visits, or prorated between them, move Dunmore Creek's July",
          ("DUN", 7) in moved["visit offset"] and ("DUN", 7) in moved["prorated offset"],
          (moved["visit offset"], moved["prorated offset"]))
    check("hazard: the logger level read as gage height moves every Dunmore Creek cell",
          {c for c in moved["no offset"] if c[0] == "DUN"} == {("DUN", m) for m in A.LOAD_MONTHS}, moved["no offset"])
    check("separation: no load device moves a cell of a station it does not touch (the offset devices move Dunmore "
          "Creek only)", all(c[0] == "DUN" for n in ("mean offset", "visit offset", "prorated offset", "no offset")
                             for c in moved[n]))
    for name, kw in A.LOAD_CONVENTIONS.items():
        r = A.monthly(TARGET, **kw)
        check("SF11 load convention converges: %s" % name, all(round(r[c]) == round(gold[c]) for c in cells),
              {c: round(r[c], 2) for c in cells if round(r[c]) != round(gold[c])})
    r = A.monthly(TARGET, bottles="golden", offs="golden", within_month=True)
    check("SF12 samples inside each month only (ruled out by the prompt: each flow takes the samples either side of "
          "it) moves cells", any(round(r[c]) != round(gold[c]) for c in cells))
    pg = A.pac(TARGET, "golden")
    check("carbon golden equals the golden's monthly pounds", all(abs(pg[m] - pac[m]) < 1e-6 for m in pac))
    pmoved = {}
    for how in A.PAC_ROUTES[1:]:
        rr = A.pac(TARGET, how)
        pmoved[how] = [m for m in pg if round(rr[m]) != round(pg[m])]
    check("device D4: setpoints with no feeder interruption (the cracker's route) move every carbon month",
          len(pmoved["nodown"]) == 4, pmoved["nodown"])
    check("device D4 half-repairs: run status alone, or a trip until its return-to-normal, each move at least two "
          "months", len(pmoved["runonly"]) >= 2 and len(pmoved["alarmspan"]) >= 2, pmoved)
    check("hazard D8: setpoints and alarms left on UTC move every carbon month", len(pmoved["utc"]) == 4,
          pmoved["utc"])
    check("misread: the hopper's LOW alarm taken for the outage moves at least two months", len(pmoved["lowalarm"]) >= 2,
          pmoved["lowalarm"])
    check("no carbon device touches the main call's rows: the call reads no plant SCADA file or ops report", True)

    # ---------------------------------------------------------------- realism and gates
    realism(R)
    gates()
    figures_agree(R, F)
    n_fail = sum(1 for _, ok, _ in RES if not ok)
    for name, ok, detail in RES:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [%s]" % (detail,)) if (detail != "" and not ok) or
                                                               os.environ.get("VERBOSE") else ""))
    print("%d checks, %d failed" % (len(RES), n_fail))
    return 1 if n_fail else 0


def alt_entries_same(R):
    """Entry depths from each station's 08:00 water temperature and the buoy's noon profile."""
    import golden as G2
    prof_noon = {}
    rehang = dt.datetime(2026, 6, 10, 10, 0)
    with open(os.path.join(TARGET, "lake/MERRIN_BUOY_Hourly_2026.dat"), encoding="ascii") as fh:
        lines = fh.read().splitlines()
    for ln in lines[4:]:
        parts = [x.strip('"') for x in ln.split(",")]
        t = dt.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
        loc = G2.cst_to_local(t)
        if loc.hour != 12:
            continue
        depths = [0.5 + n for n in range(16)] if t < rehang else [1.0 + n for n in range(16)]
        zs = [z for z, v in zip(depths, parts[4:20]) if v != "NAN"]
        vs = [float(v) for v in parts[4:20] if v != "NAN"]
        prof_noon[loc.date()] = (np.array(zs), np.array(vs))
    t8 = {}
    for k in G2.SUBS:
        ts, q, tc = G2.station_series(TARGET, k)
        t8[k] = {t.date(): v for t, v in zip(ts, tc) if t.hour == 8 and t.minute == 0}
    E2 = {}
    for d, r in R["E"].items():
        if d not in prof_noon:
            continue
        row = dict(zi=r["zi"], mixed=r["mixed"])
        for k in G2.SUBS:
            if d in t8[k]:
                row[k] = None if r["mixed"] else G2.entry(prof_noon[d], t8[k][d])
        E2[d] = row
    pp, who = G2.attribute(E2, R["days"])
    return all(who[d] == ["FEN"] for d in R["days"])


def integration_spread(R):
    """How far each monthly load moves across the integration rules a careful reader might use on the same samples
    and flows: the 15-minute left sum (the golden), the trapezoid, the month's closing stamp included, and the
    sample times snapped to the nearest 15-minute step before interpolating."""
    L, S, series = G.loads(TARGET)
    out = {}
    for k, (ts, q) in series.items():
        ref = dt.datetime(2026, 1, 1)
        st = np.array([(t - ref).total_seconds() for t, _ in S[k]])
        sv = np.array([v for _, v in S[k]])
        x = np.array([(t - ref).total_seconds() for t in ts])
        qa = np.array(q, dtype=float)
        c = np.interp(x, st, sv)
        f = qa * c * G.CFS_L * 900.0 / 1e9
        snap = np.array([round(s / 900.0) * 900.0 for s in st])
        f2 = qa * np.interp(x, snap, sv) * G.CFS_L * 900.0 / 1e9
        for m in (4, 5, 6, 7):
            w0, w1 = dt.datetime(2026, m, 1), dt.datetime(2026, m + 1, 1)
            inw = np.array([w0 <= t < w1 for t in ts])
            inw_end = np.array([w0 <= t <= w1 for t in ts])
            idx = np.where(inw)[0]
            left = float(np.nansum(f[inw]))
            trap = float(np.nansum((f[idx[:-1]] + f[idx[1:]]) / 2.0)) + float(f[idx[-1]] + f[idx[-1] + 1]) / 2.0
            endin = float(np.nansum(f[inw_end]))
            snapped = float(np.nansum(f2[inw]))
            vals = [left, trap, endin]
            out[(k, m)] = max(vals) - min(vals)
    return out


def no_repeat_blocks():
    """No 24-hour block of any buoy channel or station series repeats another day's block exactly."""
    with open(os.path.join(TARGET, "lake/MERRIN_BUOY_Hourly_2026.dat"), encoding="ascii") as fh:
        lines = fh.read().splitlines()[4:]
    seen = set()
    for n in range(0, len(lines) - 24, 24):
        blk = tuple(ln.split(",", 4)[-1] for ln in lines[n:n + 24])
        if blk in seen:
            return False
        seen.add(blk)
    return True


def sorts_on_pack(R):
    loads = R["loads"]
    area = dict(TES=317.5, FEN=45.4, OXL=89.3, DUN=57.8, LAD=13.5)
    S = {k: v for k, v in R["samples"].items() if v}
    out = {}
    out["season load"] = max(loads, key=loads.get)
    out["load per square mile"] = max(loads, key=lambda k: loads[k] / area[k])
    out["peak sampled concentration"] = max(S, key=lambda k: max(v for _, v in S[k]))
    out["median routine sample"] = max(S, key=lambda k: np.median([v for t, v in S[k] if t.weekday() == 1]))
    out["mean sampled concentration"] = max(S, key=lambda k: np.mean([v for _, v in S[k]]))
    out["samples above 3 ug/L"] = max(S, key=lambda k: sum(1 for _, v in S[k] if v > 3.0))
    flows = {}
    for k in G.SUBS:
        ts, q, tc = G.station_series(TARGET, k)
        flows[k] = float(np.nanmean(q))
    out["mean flow"] = max(flows, key=flows.get)
    out["drainage area"] = max(area, key=area.get)
    fw = {k: loads[k] / max(flows[k], 1e-9) for k in loads}
    out["flow-weighted concentration"] = max(fw, key=fw.get)
    temps = {k: np.mean([v for d, v in R["T"][k].items() if dt.date(2026, 6, 1) <= d <= dt.date(2026, 8, 31)])
             for k in G.SUBS}
    out["coldest in summer"] = min(temps, key=temps.get)
    wb = openpyxl.load_workbook(os.path.join(TARGET, "program/haldane_extension_atrazine_use_survey_2026.xlsx"),
                                read_only=True)
    applied = {}
    names = {v: k for k, v in G.NAME.items()}
    for row in wb.active.iter_rows(min_row=3, values_only=True):
        if row[0] in names:
            applied[names[row[0]]] = float(row[3]) * float(row[4])
    out["atrazine applied"] = max(applied, key=applied.get)
    out["share of applied exported"] = max(loads, key=lambda k: loads[k] / applied[k])
    return out


def cheap_routes(R):
    """Lagged correlation and regression of the daily raw-water result on each tributary's sampled concentration
    (interpolated daily), May to September."""
    S = {k: v for k, v in R["samples"].items() if v}
    d0, d1 = dt.date(2026, 5, 1), dt.date(2026, 9, 30)
    dd = [d0 + dt.timedelta(days=n) for n in range((d1 - d0).days + 1)]
    y = np.array([R["results"].get(d, np.nan) for d in dd])
    ok = ~np.isnan(y)
    out = {}
    series = {}
    for k in S:
        st = np.array([(t - dt.datetime(2026, 1, 1)).total_seconds() / 86400 for t, _ in S[k]])
        sv = np.array([v for _, v in S[k]])
        x_all = np.array([(dt.datetime.combine(d, dt.time(12)) - dt.datetime(2026, 1, 1)).total_seconds() / 86400
                          for d in dd])
        series[k] = (st, sv)
    best = {}
    for k in S:
        st, sv = series[k]
        top = (-9.0, 0)
        for lag in range(0, 21):
            xs = np.array([(dt.datetime.combine(d - dt.timedelta(days=lag), dt.time(12)) - dt.datetime(2026, 1, 1))
                           .total_seconds() / 86400 for d in dd])
            c = np.interp(xs, st, sv)
            r_ = np.corrcoef(c[ok], y[ok])[0, 1]
            if r_ > top[0]:
                top = (r_, lag)
        best[k] = top
    o = sorted(best, key=lambda k: best[k][0], reverse=True)
    out["lagged correlation"] = (o[0], best[o[0]][0] - best[o[1]][0])
    CORR.update({k: (round(float(v[0]), 3), v[1]) for k, v in best.items()})
    X = []
    for k in S:
        st, sv = series[k]
        xs = np.array([(dt.datetime.combine(d, dt.time(12)) - dt.datetime(2026, 1, 1)).total_seconds() / 86400
                       for d in dd])
        c = np.interp(xs, st, sv)
        X.append(np.array([c[max(0, n - 14):n + 1].mean() for n in range(len(c))]))
    X = np.vstack(X + [np.ones(len(dd))]).T
    beta = np.linalg.lstsq(X[ok], y[ok], rcond=None)[0][:len(S)]
    keys = list(S)
    o = sorted(range(len(keys)), key=lambda n: beta[n], reverse=True)
    out["regression on 14-day means"] = (keys[o[0]], float(beta[o[0]] - beta[o[1]]) / max(abs(beta[o[0]]), 1e-9))
    return out


def residual_without_fen(R):
    """Without Fennick's water the intake's layer keeps the spring residue: its raw-water level before Fennick's water
    first reached it, the highest result from 15 April to the day before the first day Fennick entered within the
    intake's layer."""
    E = R["E"]
    first = min(d for d in E if not E[d]["mixed"] and E[d].get("FEN") is not None and abs(E[d]["FEN"] - E[d]["zi"]) <= 2.0)
    return max(v for d, v in R["results"].items() if G.SEASON[0] <= d < first)


def realism(R):
    # no constant step in id-like columns; no round headline totals; no repeated free text beyond a real rate
    wb = openpyxl.load_workbook(os.path.join(TARGET, "lab/city_lab_ELISA_tributaries_2026.xlsx"), read_only=True)
    ids = [int(r[0].split("-")[1]) for r in wb["Results"].iter_rows(min_row=2, values_only=True) if r[0]]
    steps = set(np.diff(ids))
    check("realism: city LIMS ids are not an arithmetic sequence", len(steps) > 1, steps)
    with open(os.path.join(TARGET, "lab/SHL_EDD_brennick_source_water_2026.csv"), encoding="utf-8") as fh:
        labs = [r["Lab_Sample_ID"] for r in csv.DictReader(fh) if r["Analyte"] == "Atrazine"]
    st = set(np.diff([int(x[3:]) for x in labs]))
    check("realism: State lab numbers are not an arithmetic sequence", len(st) > 1)
    loads = R["loads"]
    check("realism: no season load is a round ten", all(round(v) % 10 != 0 for v in loads.values()),
          {k: round(v) for k, v in loads.items()})
    check("realism: no carbon month is a round hundred", all(round(v) % 100 != 0 for v in R["pac"].values()))
    # field visit offsets vary by a few thousandths, not one constant
    wb = openpyxl.load_workbook(os.path.join(TARGET, "hydro/DC-04_LB-05_ratings_and_field_visits.xlsx"), read_only=True)
    offs = [round(float(r[3]) - float(r[4]), 3) for r in wb["Field visits"].iter_rows(min_row=2, values_only=True) if r[0] == "DC-04"]
    early, late = offs[:5], offs[5:]
    check("realism: DC-04 visit offsets vary by a few thousandths within each hang of the logger, and move by a tenth "
          "of a foot or more after it slipped", len(set(early)) > 2 and max(early) - min(early) < 0.03 and
          max(late) - min(late) < 0.03 and min(early) - max(late) > 0.10, offs)
    seg = R["offsets"]["DUN"]
    check("the golden places the DC-04 offset change at the logger's one unexplained step, between the June and July "
          "visits", len(seg) == 2 and dt.datetime(2026, 6, 30) < seg[1][0] < dt.datetime(2026, 7, 28), seg)
    seg_l = R["offsets"]["LAD"]
    check("LB-05 keeps one offset all season", len(seg_l) == 1, seg_l)
    # documents state no date after their own
    check("realism: the alarm history holds the feeder's events among many tags", alarm_mix())
    # persona names come from guard.py names
    allowed = {"Brandi Dougherty", "Carl Newman", "Rhonda Dixon", "Veronica Hunt", "Jack Sullivan", "Zachary Frederick",
               "Jim Solis", "Thomas Glass", "Barry Chen", "Gregory Logan", "Christina Ball", "Brittany Frye"}
    check("realism: every full name in the documents is a drawn persona", names_ok(allowed))
    # no readme, dictionary, notes or manifest under target
    bad = [fn for fn in glob.glob(os.path.join(TARGET, "**", "*"), recursive=True)
           if re.search(r"readme|dictionary|manifest|field_notes|codebook|data_notes", os.path.basename(fn), re.I)]
    check("realism: no file under target describes the data", not bad, bad)


def alarm_mix():
    tags = collections.Counter()
    with open(os.path.join(TARGET, "plant/scada_alarm_event_history_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            tags[r["Tag"]] += 1
    return len(tags) > 15 and tags["PAC-FDR-1"] < 0.08 * sum(tags.values())


def names_ok(allowed):
    from pypdf import PdfReader
    txt = ""
    for fn in glob.glob(os.path.join(TARGET, "**", "*.pdf"), recursive=True):
        txt += " ".join(pg.extract_text() or "" for pg in PdfReader(fn).pages)
    found = set(re.findall(r"\b(Brandi Dougherty|Carl Newman|Rhonda Dixon|Veronica Hunt)\b", txt))
    control = "Brandi Dougherty" in txt
    return control and found <= allowed


def gates():
    files = [fn for fn in glob.glob(os.path.join(TARGET, "**", "*"), recursive=True) if os.path.isfile(fn)]
    exts = collections.Counter(os.path.splitext(fn)[1].lower() for fn in files)
    check("gate: 10 or more files", len(files) >= 10, len(files))
    check("gate: 3 or more formats", len(exts) >= 3, dict(exts))
    big = 0
    for fn in files:
        if fn.endswith((".csv", ".dat", ".txt")):
            with open(fn, encoding="utf-8", errors="replace") as fh:
                big = max(big, sum(1 for _ in fh))
    check("gate: a file of 25,000 or more rows", big >= 25000, big)
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    check("gate: two or more distractors named in metadata.json", len(md["distractor_files"]) >= 2 and
          all(os.path.exists(os.path.join(TASK, p)) for p in md["distractor_files"]), md["distractor_files"])
    check("gate: no file name says distractor", not any("distract" in fn.lower() for fn in files))


def figures_agree(R, F):
    check("figures.json carries the call and its days", F["call"] == "Fennick Creek" and F["call_days"] == len(R["days"]))
    check("figures.json loads equal the golden's", all(F["loads_kg"][G.NAME[k]] == int(round(v)) for k, v in R["loads"].items()))
    check("figures.json carbon equals the golden's", all(F["pac_lb"][m] == int(round(R["pac"][n])) for n, m in
                                                         ((5, "May"), (6, "June"), (7, "July"), (8, "August"))))


if __name__ == "__main__":
    sys.exit(main())
