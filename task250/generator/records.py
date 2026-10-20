"""The records the consortium keeps: the quality control as it ran over 2025 to 2027 (historical limits, the alerts it
raised, the drift faults it found and the repairs), the stations' daily export, and the register.

    R = recorded(W)     the record: anomalies with the faults as repaired, the QC's residuals, statistic and alerts
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

D = P.DAYS


def day(k):
    return P.START + dt.timedelta(days=int(k))


# ------------------------------------------------------------------ the drifts and the visits that found them
FOUND = 0.2                 # a check adjusts the sensor when its as-found error passes 0.2 degrees
N_DRIFTS = 42               # sensors that drifted over 2025 to 2027 at stations the network keeps
N_DRIFTS_CLOSING = 3        # and at stations that close
RATE = (0.008, 0.025)       # degrees a day
RATIO = 0.7                 # a drift sits only where it cannot carry a neighbour's statistic over that neighbour's limit
LOOKBACK = 90               # no alert at any setting at a drifting station from 90 days before its drift began to a
                            # fortnight before the alert that sent its visit
PASSES = 80
ROUND_WINDOWS = [((dt.date(y, 3, 1) - P.START).days, 106) for y in (2025, 2026, 2027)]   # the spring rounds


def workday(k):
    while day(k).weekday() >= 5:
        k += 1
    return k


def rounds(W, seed):
    """each station's calibration-round day in the spring rounds of 2025 to 2027"""
    rr = np.random.default_rng(seed + 105)
    return {i: [workday(c0 + int(rr.integers(0, n))) for (c0, n) in ROUND_WINDOWS] for i in range(W["N"])}


def breakdowns(W, seed):
    """an outage of two days or more opens a breakdown order on its second day, visited one to four days later"""
    rb = np.random.default_rng(seed + 106)
    av = W["avail"]
    out = []
    for i in range(W["N"]):
        k = 1
        while k < P.DAYS:
            if not av[k, i] and not av[k - 1, i] and (k < 2 or av[k - 2, i]):
                v = workday(k + int(rb.integers(1, 5)))
                if v < P.DAYS:
                    out.append((i, k, v))
                k += 5
            k += 1
    return out


def limits_2025_2027(W, seed):
    """the limits in force each year, configured from the three years before 2025 (the in-control spread of the
    statistic stands for them here), each year's own configuration"""
    N = W["N"]
    a_ic, _ = sim.anomalies(dict(W, faults=[]))
    _, D_ic, _ = sim.qc(W, a_ic, np.ones(N, bool))
    sd_ic = np.nanstd(D_ic, axis=0, ddof=1)
    rf = np.random.default_rng(seed + 9).lognormal(0, 0.05, (3, N))
    sd_year = np.round(sd_ic[None, :] * rf, 3)
    limit = np.zeros((D, N))
    for y in range(3):
        limit[y * 365:(y + 1) * 365] = np.round(P.SETTING_2025_2027 * sd_year[y], 3)[None, :]
    return limit, sd_year, D_ic


def checks_noise(W, seed):
    """each sensor's standing offset against the transfer standard (small: none passes the adjustment threshold) and
    the mean error of a check's three as-found readings on each day"""
    ro = np.random.default_rng(seed + 108)
    offset = np.clip(ro.normal(0, 0.05, W["N"]), -0.12, 0.12)
    e = ro.normal(0, 0.02, (D, W["N"]))
    return offset, e


def as_found(f, v, offset, e):
    return float(offset[f["i"]] + f["rate"] * (v - f["start"] + 1) + e[v, f["i"]]) if v < D else 0.0


def run_policy(W, faults, limit, pool, rnd, lag, export=False, noise=None):
    """the record under a limit (D x N): each drift runs until the first check that finds it, the visit answering an
    alert whose check finds the sensor off by more than FOUND, or the station's round visit if its check does.
    `export`: the quality control computed at the precision its export carries (anomalies to 0.01, the register's
    coordinates), the statistic compared as computed, as the 2028 estimate reads it.
    Returns how each drift ended, the drift ends, the stored statistic, the alerts and whether the run settled."""
    import solve
    Wf = dict(W, faults=faults)
    ends = None
    stations = np.where(pool)[0]
    xy = np.c_[np.round(W["st"]["x_km"] * 1000), np.round(W["st"]["y_km"] * 1000)]
    for _ in range(12):
        a, T = sim.anomalies(Wf, ends)
        if export:
            R, S = solve.rerun(np.round(a, 2), xy, pool)
            NB = None
        else:
            R, Dst, NB = sim.qc(Wf, a, pool)
            S = np.round(Dst, 3)
        al = sim.alerts(S, limit, stations)
        by = {}
        for (i, t) in al:
            by.setdefault(i, []).append(t)
        new, how = {}, []
        for f in faults:
            i, t0, r = f["i"], f["start"], f["rate"]
            best = (D, "open", None)
            for t in by.get(i, []):
                if t <= t0:
                    continue
                v = workday(t + int(lag[t, i]))
                if v < D and abs(as_found(f, v, *noise)) > FOUND:
                    best = min(best, (v, "alert", t))
                    break
            for v in rnd[i]:
                if v > t0 and abs(as_found(f, v, *noise)) > FOUND:
                    best = min(best, (v, "round", -1))
                    break
            new.setdefault(i, {})[t0] = min(best[0], D)
            how.append({"i": i, "start": t0, "rate": r, "repair": min(best[0], D), "how": best[1],
                        "alert": best[2] if best[1] == "alert" else None})
        if new == ends:
            return {"how": how, "ends": ends, "a": a, "T": T, "R": R, "S": S, "NB": NB, "alerts": al, "settled": True}
        ends = new
    return {"how": how, "ends": new, "a": a, "T": T, "R": R, "S": S, "NB": NB, "alerts": al, "settled": False}


def _weights(W, pool):
    """each station's usual neighbours under `pool` and the largest weight each neighbour carries in its estimate"""
    N = W["N"]
    a, _ = sim.anomalies(dict(W, faults=[]))
    _, Dst, NB = sim.qc(W, a, pool)
    sd = np.nanstd(Dst, axis=0, ddof=1)
    wmax = np.zeros((N, N))
    used = [set() for _ in range(N)]
    for i in range(N):
        nb = NB[:, i, :]
        ok = nb[:, 0] >= 0
        if not ok.any():
            continue
        rows, cnt = np.unique(nb[ok], axis=0, return_counts=True)
        for row, c in zip(rows, cnt):
            w = 1 / W["dist"][i, row] ** 2
            w = w / w.sum()
            for j, ww in zip(row, w):
                wmax[i, j] = max(wmax[i, j], ww)
            used[i] |= set(int(x) for x in row)
    return sd, wmax, used


def drift_sites(W):
    """the stations a drift may sit at: where it cannot carry a neighbour over its limit before its own alert, in
    either network, and (at the stations kept) where no usual neighbour closes"""
    N = W["N"]
    closing = set(W["closing"])
    keep = np.array([i not in closing for i in range(N)])
    sd0, w0, used0 = _weights(W, np.ones(N, bool))
    _, w1, _ = _weights(W, keep)
    r0 = np.array([max(w0[i, j] * sd0[j] / sd0[i] for i in range(N)) for j in range(N)])
    r1 = np.array([max((w1[i, j] * sd0[j] / sd0[i]) if keep[i] else 0.0 for i in range(N)) for j in range(N)])
    kept = [i for i in range(N) if keep[i] and not (used0[i] & closing) and r0[i] < RATIO and r1[i] < RATIO]
    shut = [i for i in sorted(closing) if r0[i] < RATIO]
    return kept, shut


def export_rerun(rec_a, S_rec, W, pool):
    """what the quality control's export carries (anomalies to 0.01, the statistic to 0.001) re-run with `pool`"""
    import solve
    xy = np.c_[np.round(W["st"]["x_km"] * 1000), np.round(W["st"]["y_km"] * 1000)]
    A = np.round(rec_a, 2)
    _, S28 = solve.rerun(A, xy, pool)
    return S28


def audit(W, faults, run, limit, rnd, lag, bk, noise):
    """the drifts that break the record's clean reading, by index: a drift still open at the end; a breakdown visit
    with a check while it ran; an alert-found drift at a kept station whose station's next round, or the record's end,
    comes before it could have crossed 4.5; an alert at any setting at its station in the 90 days before it began;
    and a station whose count at any setting under the 2028 network, run with the drifts left to grow, departs from
    the export re-run plus the drifts the re-run never alerted before their repair"""
    import solve
    N = W["N"]
    closing = set(W["closing"])
    keep = np.array([i not in closing for i in range(N)])
    S = run["S"]
    sd = np.nanstd(S, axis=0, ddof=1)
    S28 = export_rerun(run["a"], S, W, keep)
    bad = set()
    newc = [(i, k, v) for (i, k, v) in bk if day(v) >= P.CONTRACT_SWITCH]
    by = {}
    for (i, t) in run["alerts"]:
        by.setdefault(i, []).append(t)
    for n, h in enumerate(run["how"]):
        i = h["i"]
        if h["how"] == "open":
            bad.add(n)
        seen = [workday(t + int(lag[t, i])) for t in by.get(i, []) if h["start"] < t] + \
               [v for v in rnd[i] if v > h["start"]]
        if any(v <= h["repair"] and v < D and abs(abs(as_found(faults[n], v, *noise)) - FOUND) < 0.015 for v in seen):
            bad.add(n)
        if any(i == j and h["start"] - 5 <= v <= h["repair"] + 120 for (j, k, v) in newc):
            bad.add(n)
        if h["how"] == "alert" and keep[i]:
            gap = (4.5 * sd[i] - abs(S[h["alert"], i])) / abs(h["rate"]) + 30
            nxt = [x for x in rnd[i] if x > h["repair"]]
            if (nxt and nxt[0] - h["repair"] < gap) or h["repair"] + gap > D:
                bad.add(n)
    depart = set()
    detail = {}
    for k in P.SETTINGS:
        lim = k * sd
        per = {}
        for i in np.where(keep)[0]:
            last = -10 ** 6
            s = S28[:, i]
            for t in np.where(~np.isnan(s) & (np.abs(np.nan_to_num(s)) > lim[i]))[0]:
                if t - last > P.HOLD_DAYS:
                    per.setdefault(i, []).append(int(t))
                    last = t
        form = {i: len(v) for i, v in per.items()}
        for n, h in enumerate(run["how"]):
            i = h["i"]
            if h["how"] != "alert" or not keep[i]:
                continue
            if any(h["start"] - LOOKBACK <= x < h["alert"] - 14 for x in per.get(i, [])):
                bad.add(n)
            if not any(h["start"] <= x <= h["repair"] for x in per.get(i, [])):
                form[i] = form.get(i, 0) + 1
        cf = run_policy(W, faults, np.tile(lim, (D, 1)), keep, rnd, lag, export=True, noise=noise)
        c = {}
        for (i, t) in cf["alerts"]:
            c[i] = c.get(i, 0) + 1
        dep = {i for i in set(form) | set(c) if form.get(i, 0) != c.get(i, 0)}
        if not cf["settled"]:
            dep |= {f["i"] for f in faults}
        depart |= dep
        detail[k] = (sum(form.values()), sum(c.values()))
    for j in depart:
        # the drifts at a departing station, else at its nearest stations, else within 30 km of it
        for reach in (1, 9):
            near = set(int(x) for x in np.argsort(W["dist"][j])[:reach])
            hit = {n for n, f in enumerate(faults) if f["i"] in near}
            if hit:
                break
        else:
            hit = {n for n, f in enumerate(faults) if W["dist"][j, f["i"]] <= 30}
        bad |= hit
    return bad, depart, detail


def golden_totals(W, run):
    """each setting's 2025 to 2027 count as the golden reads it off the export: the re-run with the 2028 network plus
    every drift the history shows adjusted after a drift alert at a kept station that the re-run never alerted from a
    fortnight before that alert to the adjustment"""
    import solve
    N = W["N"]
    closing = set(W["closing"])
    keep = np.array([i not in closing for i in range(N)])
    S = run["S"]
    sd = np.nanstd(S, axis=0, ddof=1)
    S28 = export_rerun(run["a"], S, W, keep)
    rep = [(h["i"], h["alert"], h["repair"]) for h in run["how"] if h["how"] == "alert"]
    out = {}
    for k in P.SETTINGS:
        days = solve.alert_days_by_station(S28, k * sd, np.where(keep)[0])
        out[k] = sum(len(v) for v in days.values()) + len(solve.cut_short(days, rep, keep))
    return out


def recorded(W, seed=250, verbose=False):
    """the record: the drifts (placed, then redrawn until the record reads cleanly), the quality control as it ran
    over 2025 to 2027 at 3.0 with each year's limits, the alerts it raised and the visits that found the drifts"""
    N = W["N"]
    limit, sd_year, _ = limits_2025_2027(W, seed)
    rnd = rounds(W, seed)
    bk = breakdowns(W, seed)
    lag = np.random.default_rng(seed + 107).integers(1, 6, (D, N))
    noise = checks_noise(W, seed)
    kept, shut = drift_sites(W)
    r4 = np.random.default_rng(seed + 104)
    faults = []
    for i in list(r4.choice(kept, N_DRIFTS, replace=False)) + list(r4.choice(shut, N_DRIFTS_CLOSING, replace=False)):
        faults.append({"i": int(i), "start": int(r4.integers(30, D - 130)),
                       "rate": float(r4.uniform(*RATE)) * float(r4.choice([-1, 1]))})
    rs = np.random.default_rng(seed + 777)
    pool = np.ones(N, bool)
    closing = set(W["closing"])

    def settle(faults, passes):
        """redraw the drifts that break the record's clean reading until none does"""
        for p in range(passes):
            run = run_policy(W, faults, limit, pool, rnd, lag, noise=noise)
            bad, depart, detail = audit(W, faults, run, limit, rnd, lag, bk, noise)
            if verbose:
                print("  pass %d: %d drifts redrawn, %d stations depart, settled %s"
                      % (p, len(bad), len(depart), run["settled"]), flush=True)
            if not bad and not depart and run["settled"]:
                tot = golden_totals(W, run)
                assert all(tot[k] == detail[k][0] for k in P.SETTINGS), (tot, detail)
                return run, detail, tot
            for n in sorted(bad):
                faults[n]["start"] = int(rs.integers(30, D - 130))
        return None

    out = settle(faults, PASSES)
    clean = out is not None and all(t % 3 == 0 for t in out[2].values())
    # every setting's three-year count a multiple of three, so each figure a year is a whole number: each drift a
    # kept station's alert found adds one alert at every setting, so when the four counts share a remainder one drift
    # more or one fewer clears it (tried in a fixed order, kept only where the record still reads cleanly)
    if out is not None and not clean:
        res = {t % 3 for t in out[2].values()}
        if len(res) == 1:
            r = res.pop()
            used = {f["i"] for f in faults}
            trials = []
            if r == 1:
                trials += [("drop", n) for n in reversed(range(len(faults))) if faults[n]["i"] not in closing]
            for i in [x for x in kept if x not in used]:
                for _ in range(3):
                    trials.append(("add", {"i": int(i), "start": int(rs.integers(30, D - 130)),
                                           "rate": float(rs.uniform(*RATE)) * float(rs.choice([-1, 1]))}))
            if r == 2:
                trials = [t for t in trials if t[0] == "add"]
            for kind, x in trials:
                cand = [dict(f) for f in faults]
                if kind == "drop":
                    cand.pop(x)
                else:
                    cand.append(dict(x))
                run = run_policy(W, cand, limit, pool, rnd, lag, noise=noise)
                if not run["settled"] or any(t % 3 for t in golden_totals(W, run).values()):
                    continue
                bad, depart, detail = audit(W, cand, run, limit, rnd, lag, bk, noise)
                if bad or depart:
                    continue
                faults[:] = cand
                out = (run, detail, golden_totals(W, run))
                clean = True
                break
    run, detail = (out[0], out[1]) if out is not None else (run_policy(W, faults, limit, pool, rnd, lag, noise=noise), {})
    found = [dict(h) for h in run["how"]]
    return {"a": run["a"], "T": run["T"], "R": run["R"], "D": run["S"], "NB": run["NB"], "limit": limit,
            "sd_year": sd_year, "alerts": run["alerts"], "faults": found, "pool": pool, "rounds": rnd,
            "breakdowns": bk, "lag": lag, "noise": noise, "clean": clean, "detail": detail, "ends": run["ends"]}


def config_2028(rec):
    """the January 2028 configuration: each station's spread of the recorded statistic over 2025 to 2027"""
    return np.nanstd(rec["D"], axis=0, ddof=1)


# ------------------------------------------------------------------ station codes, names and the register
NAME_A = ["Paridera", "Corral", "Mas", "Casa", "Val", "Saso", "Plana", "Torre", "Huerta", "Soto", "Pardina", "Venta",
          "Llano", "Cabezo", "Paúl", "Balsa", "Ermita", "Fuente", "Loma", "Raso"]
NAME_B = ["Alta", "Baja", "del Molino", "de Arriba", "del Cierzo", "Nueva", "Vieja", "de la Sarda", "del Pino",
          "de los Frailes", "del Royo", "de Santa Ana", "Larga", "del Conde", "de la Laguna", "del Prior", "Redonda",
          "de las Viñas", "del Saladar", "de Valfría", "Blanca", "del Tozal", "de San Juan", "del Ebro"]
TOWNS = {
    "CV": ["Ejea de los Caballeros", "Tauste", "Sádaba", "Uncastillo", "Biota", "Castejón de Valdejasa", "Luna",
           "Erla", "Sierra de Luna", "Valpalmas"],
    "RA": ["Alagón", "Pedrola", "Gallur", "Figueruelas", "Remolinos", "Cabañas de Ebro", "Luceni", "Pleitas",
           "Torres de Berrellén", "Grisén"],
    "VJ": ["La Almunia de Doña Godina", "Épila", "Ricla", "Calatorao", "Morata de Jalón", "Lumpiaque", "Rueda de Jalón",
           "Lucena de Jalón", "Urrea de Jalón", "Salillas de Jalón"],
    "HH": ["Almudévar", "Gurrea de Gállego", "Zuera", "Ayerbe", "Montmesa", "Vicién", "Tardienta", "Lupiñén",
           "Alcalá de Gurrea", "Leciñena"],
    "MO": ["Sariñena", "Grañén", "Lanaja", "Bujaraloz", "Peñalba", "Castejón de Monegros", "Alcubierre", "Perdiguera",
           "Farlete", "Monegrillo"],
    "SB": ["Barbastro", "Berbegal", "Peralta de Alcofea", "Castejón del Puente", "Ilche", "Laluenga", "Pozán de Vero",
           "Azara", "Estadilla", "Salas Altas"],
    "CM": ["Monzón", "Binaced", "Alcolea de Cinca", "Albalate de Cinca", "Pueyo de Santa Cruz", "Binéfar", "Esplús",
           "San Esteban de Litera", "Tamarite de Litera", "Altorricón"],
    "BC": ["Fraga", "Candasnos", "Ballobar", "Zaidín", "Velilla de Cinca", "Torrente de Cinca", "Belver de Cinca",
           "Osso de Cinca", "Ontiñena", "Chalamera"],
}


def register(W, seed=250):
    st = W["st"].copy()
    rng = np.random.default_rng(seed + 20)
    st["code"] = ["EM%03d" % (i + 1) for i in range(len(st))]
    used = set()
    names, towns = [], []
    for i, r in st.iterrows():
        while True:
            nm = "%s %s" % (rng.choice(NAME_A), rng.choice(NAME_B))
            if nm not in used:
                used.add(nm)
                break
        names.append(nm)
        towns.append(rng.choice(TOWNS[r["district"]]))
    st["name"] = names
    st["municipality"] = towns
    st["x_utm"] = np.round(st["x_km"] * 1000).astype(int)
    st["y_utm"] = np.round(st["y_km"] * 1000).astype(int)
    inst = []
    for g in st["group"]:
        if g == "core":
            inst.append(dt.date(int(rng.integers(2004, 2016)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))
        elif g == "programme":
            inst.append(dt.date(int(rng.integers(2022, 2024)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))
        else:
            inst.append(dt.date(int(rng.integers(2019, 2022)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))
    st["installed"] = inst
    closing = set(W["closing"])
    # the programme's stations an irrigation community took over carry its funding from 2028
    st["funding"] = ["programme 2021-2027" if i in closing else
                     ("comunidad de regantes" if g == "programme" else "Consorcio")
                     for i, g in enumerate(st["group"])]
    st["closes"] = [dt.date(2027, 12, 31) if i in closing else None for i in range(len(st))]
    # five-minute logging after a firmware upgrade at some stations
    up = rng.random(len(st)) < 0.35
    st["five_min_from"] = [dt.date(2026, int(rng.integers(5, 12)), int(rng.integers(1, 28))) if u else None for u in up]
    return st


ACTION_ADJUST, ACTION_REPLACE = "Ajuste de calibración", "Sustitución del sensor"
REASON = {"drift": "Alerta de deriva", "scheduled": "Campaña de calibración", "breakdown": "Avería"}


def adjustments(W, rec, reg, truth, seed=250):
    """the register's history of work on each station's temperature sensor: every adjustment a check made (the
    as-found error, a sensor off by more than a degree replaced rather than adjusted), and the sensors replaced or
    shields cleaned at breakdown and round visits for other reasons"""
    rng = np.random.default_rng(seed + 21)
    rows = []
    for t in truth:
        if t.get("adjusted"):
            rows.append({"codigo": reg["code"][t["i"]], "fecha": day(t["v"]),
                         "actuacion": ACTION_REPLACE if abs(t["as_found"]) > 1.0 else ACTION_ADJUST,
                         "motivo": REASON[t["kind"]], "error_encontrado_C": round(t["as_found"], 2),
                         "observaciones": ""})
    other = [t for t in truth if t["status"] == "visit" and t["v"] is not None and not t.get("adjusted")
             and t["kind"] in ("breakdown", "scheduled") and not t["combined"]]
    for n in rng.choice(len(other), 30, replace=False):
        t = other[int(n)]
        if t["kind"] == "breakdown":
            rows.append({"codigo": reg["code"][t["i"]], "fecha": day(t["v"]), "actuacion": ACTION_REPLACE,
                         "motivo": REASON["breakdown"], "error_encontrado_C": None,
                         "observaciones": rng.choice(["sonda sin lectura", "cable dañado", "sensor golpeado", "humedad en conector"])})
        else:
            rows.append({"codigo": reg["code"][t["i"]], "fecha": day(t["v"]), "actuacion": "Limpieza de la garita",
                         "motivo": REASON["scheduled"], "error_encontrado_C": None,
                         "observaciones": rng.choice(["nido", "polvo", "telaraña", ""])})
    df = pd.DataFrame(rows).sort_values(["fecha", "codigo"], kind="stable").reset_index(drop=True)
    return df


# ------------------------------------------------------------------ the loggers' daily export
DST = {dt.date(2025, 3, 30): 23, dt.date(2025, 10, 26): 25, dt.date(2026, 3, 29): 23, dt.date(2026, 10, 25): 25,
       dt.date(2027, 3, 28): 23, dt.date(2027, 10, 31): 25}


def scheduled(d, five):
    """the records a local civil day should hold"""
    return (288 if five else 144) * DST.get(d, 24) // 24


def accept_min(d, five):
    """the completeness rule: at least 90 per cent of the records the day should hold"""
    return int(np.ceil(0.9 * scheduled(d, five) - 1e-9))


def daily_export(W, rec, reg, seed=250):
    """one row per station and day the logger delivered anything; a day the quality control could not read is a
    partial day (too few records) or a day with no row. Re-sent rows after a link drops are repeated as delivered."""
    rng = np.random.default_rng(seed + 30)
    avail = W["avail"]
    T = rec["T"]
    doy = W["doy"]
    dtr = 11.5 + 4.0 * np.sin(2 * np.pi * (doy - 110) / 365)
    rows = []
    for i, r in reg.iterrows():
        five_from = r["five_min_from"]
        for k in range(P.DAYS):
            d = day(k)
            five = five_from is not None and d >= five_from
            sch = scheduled(d, five)
            lo = accept_min(d, five)
            if avail[k, i]:
                if d in DST and rng.random() < 0.30:
                    # the clock change confuses some loggers: a spring day short by up to an hour, an autumn day
                    # with the repeated hour written over
                    n = int(rng.integers(lo, min(sch, lo + 6))) if DST[d] == 23 else int(rng.integers(lo, lo + 5))
                elif rng.random() < 0.06:
                    n = int(rng.integers(lo, sch))
                else:
                    n = sch
            else:
                # an outage day: nothing delivered, or a part day the rule rejects
                prev_ok = k > 0 and avail[k - 1, i]
                nxt_ok = k < P.DAYS - 1 and avail[k + 1, i]
                if (prev_ok or nxt_ok) and rng.random() < 0.6:
                    n = int(rng.integers(max(1, sch // 8), lo))
                elif d in DST and rng.random() < 0.5:
                    n = int(rng.integers(lo - 6, lo)) if DST[d] == 25 else int(rng.integers(max(1, lo - 30), lo))
                else:
                    continue
            t = T[k, i]
            rows.append((r["code"], d, round(float(t), 1) + 0.0, round(float(t + dtr[k] / 2 + rng.normal(0, 0.9)), 1) + 0.0,
                         round(float(t - dtr[k] / 2 + rng.normal(0, 0.9)), 1) + 0.0, n))
    df = pd.DataFrame(rows, columns=["estacion", "fecha", "tmed", "tmax", "tmin", "n_registros"])
    # re-sent rows after the link drops (exact repeats)
    rep = df.sample(frac=0.004, random_state=seed + 31)
    df = pd.concat([df, rep]).sort_values(["estacion", "fecha"], kind="stable").reset_index(drop=True)
    return df


def accepted_mask(W, reg):
    """the station-days the quality control reads (the sim's availability): the rule's acceptance on the export"""
    return W["avail"]


# ------------------------------------------------------------------ the quality control's daily export
def qc_export(W, rec, reg):
    code = list(reg["code"])
    a, R, Dst, NB, lim = rec["a"], rec["R"], rec["D"], rec["NB"], rec["limit"]
    al = set(rec["alerts"])
    rows = []
    for i in range(W["N"]):
        for k in range(P.DAYS):
            if np.isnan(a[k, i]):
                continue
            nb = " ".join(code[j] for j in NB[k, i]) if NB[k, i, 0] >= 0 else ""
            r = R[k, i]
            s = Dst[k, i]
            rows.append((code[i], day(k), round(float(a[k, i]), 2) + 0.0,
                         None if np.isnan(r) else round(float(a[k, i] - r), 2) + 0.0,
                         None if np.isnan(r) else round(float(r), 2) + 0.0, nb,
                         None if np.isnan(s) else round(float(s), 3) + 0.0, round(float(lim[k, i]), 3) + 0.0,
                         "S" if (i, k) in al else ""))
    return pd.DataFrame(rows, columns=["estacion", "fecha", "anomalia", "estimacion", "residuo", "vecinos",
                                       "estadistico_14d", "limite", "alerta"])


# ------------------------------------------------------------------ the field team's work orders and the checks
def field_records(W, rec, reg, seed=250, daily=None):
    """the field visits (drift alerts, breakdowns, the calibration rounds) and the transfer-standard checks the
    consortium's calibration database holds, a check at a station read in the station's air, inside the day's range its
    logger recorded (`daily`), and the new contractor's workshop checks of a spare sensor at two fixed points before it
    goes out. Returns the visits, the checks and the truth per visit."""
    rng = np.random.default_rng(seed + 40)
    lag, rnd = rec["lag"], rec["rounds"]
    offset, e = rec["noise"]
    code = list(reg["code"])
    span = {}
    if daily is not None:
        for s_, d_, lo_, hi_ in zip(daily["estacion"], daily["fecha"], daily["tmin"], daily["tmax"]):
            span.setdefault((s_, d_), (float(lo_), float(hi_)))
    fault_at = {}
    for f in rec["faults"]:
        fault_at.setdefault(f["i"], []).append(f)

    def drift_at(i, k):
        """the drift's error on day k, its repair visit's as-found included"""
        for f in fault_at.get(i, []):
            if f["start"] <= k <= f["repair"]:
                return f["rate"] * (k - f["start"] + 1)
        return 0.0

    def standing(i, k):
        """the sensor's standing offset, set right when its drift was repaired"""
        return 0.0 if any(f["repair"] < k for f in fault_at.get(i, [])) else float(offset[i])

    def near_drift(i, k, pad):
        return any(f["start"] - pad <= k <= f["repair"] + pad for f in fault_at.get(i, []))

    visits = []
    # drift alerts: each opens an order on the next office day; the visit answering it comes on the workday the
    # quality control's record gives; some orders are cancelled before anyone goes and some closed from the office
    ro = np.random.default_rng(seed + 43)
    for (i, t) in sorted(rec["alerts"], key=lambda x: (x[1], x[0])):
        v = workday(t + int(lag[t, i]))
        u = ro.random()
        status = "visit"
        if not near_drift(i, t, 0):
            if u < CANCEL:
                status = "cancelled"
            elif u < CANCEL + OFFICE:
                status = "office"
        if status == "visit" and v >= D:
            continue
        closed = workday(t + int(ro.integers(1, 5))) if status == "office" else None
        if closed is not None and closed >= D:
            continue
        visits.append({"i": i, "v": v if status == "visit" else None, "kind": "drift", "opened": workday(t),
                       "alert": t, "status": status, "combined": False, "closed": closed})
    def alone_near(x, d0, d1):
        """another visit at x's station between d0 and d1 (days), which would sit inside x's order while it was open"""
        return any(y is not x and y["i"] == x["i"] and y["v"] is not None and y["status"] == "visit" and d0 <= y["v"] <= d1
                   for y in visits) or any(d0 <= v <= d1 for (i, k, v) in rec["breakdowns"] if i == x["i"])

    # every district has drift orders closed from the office in 2027 (the alert judged a false one from the desk)
    for dc, _ in P.DISTRICTS:
        mine = [x for x in visits if W["st"]["district"][x["i"]] == dc and day(x["opened"]).year == 2027]
        if any(x["status"] == "office" for x in mine):
            continue
        pool = [x for x in mine if x["status"] == "visit" and not near_drift(x["i"], x["alert"], 60)
                and not any(x["opened"] - 2 <= r <= x["opened"] + 23 for r in rnd[x["i"]]) and x["v"] < D - 5
                and not alone_near(x, x["opened"] - 5, x["alert"] + 22)]
        for x in [pool[int(ro.integers(len(pool)))]] if pool else []:
            x["status"], x["v"] = "office", None
            x["closed"] = workday(x["alert"] + int(ro.integers(1, 5)))
    # and the new contractor's desk, from July 2027, closes a false alert without a visit in every district that had one
    for dc, _ in P.DISTRICTS:
        mine = [x for x in visits if W["st"]["district"][x["i"]] == dc and day(x["opened"]).year == 2027
                and day(x["opened"]) >= P.CONTRACT_SWITCH]
        if any(x["status"] == "office" for x in mine):
            continue
        pool = [x for x in mine if x["status"] == "visit" and not near_drift(x["i"], x["alert"], 60)
                and not any(x["opened"] - 2 <= r <= x["opened"] + 23 for r in rnd[x["i"]]) and x["v"] < D - 5
                and not alone_near(x, x["opened"] - 5, x["alert"] + 22)]
        for x in [pool[int(ro.integers(len(pool)))]] if pool else []:
            x["status"], x["v"] = "office", None
            x["closed"] = workday(x["alert"] + int(ro.integers(1, 5)))
    for (i, k, v) in rec["breakdowns"]:
        visits.append({"i": i, "v": v, "kind": "breakdown", "opened": k, "alert": None, "status": "visit",
                       "combined": False, "closed": None})
    for n, x in enumerate(visits):
        x["vid"], x["route"] = n, None
    # the new contractor's desk puts a breakdown opened at a station between a drift alert there and that alert's visit
    # on the drift order: one order, one visit (the logger is looked at when the technician comes for the alert)
    for x in visits:
        if x["kind"] != "breakdown" or day(x["v"]) < P.CONTRACT_SWITCH:
            continue
        if any(y["kind"] == "drift" and y["status"] == "visit" and y["i"] == x["i"] and y["alert"] - 1 <= x["opened"] <= y["v"]
               for y in visits):
            x["status"] = "absorbed"
    # the new contractor puts two correctives opened within a day of each other at stations 40 km apart or less on one
    # route, visited on one day once both are open (never at a station with a drift running)
    xy = np.c_[W["st"]["x_km"], W["st"]["y_km"]]
    corr = [x for x in visits if x["status"] == "visit" and x["v"] is not None and day(x["v"]) >= P.CONTRACT_SWITCH
            and not near_drift(x["i"], x["v"], 30)]
    taken = set()
    for a_ in corr:
        for b_ in corr:
            if a_ is b_ or id(a_) in taken or id(b_) in taken:
                continue
            if abs(a_["opened"] - b_["opened"]) > 1 or a_["i"] == b_["i"] or np.hypot(*(xy[a_["i"]] - xy[b_["i"]])) > 40:
                continue
            d_ = max(a_["v"], b_["v"])
            if d_ < max(a_["opened"], b_["opened"]) or d_ >= D or near_drift(a_["i"], d_, 30) or near_drift(b_["i"], d_, 30):
                continue
            a_["v"] = b_["v"] = d_
            a_["route"], b_["route"] = b_["vid"], a_["vid"]
            taken.update({id(a_), id(b_)})
            break
    # a drift alert answered at the station's spring round visit when that visit fell within three weeks of the order
    # opening: the check under the round's order. In 2027 every district with such an alert has one
    rc = np.random.default_rng(seed + 42)
    cand = {}
    for x in visits:
        if x["status"] != "visit" or x["route"] is not None or near_drift(x["i"], x["opened"], 60):
            continue
        if not (x["kind"] == "drift" or (x["kind"] == "breakdown" and day(x["v"]) >= P.CONTRACT_SWITCH)):
            continue
        for w, r in enumerate(rnd[x["i"]]):
            if x["opened"] <= r <= x["opened"] + 21 and (x["kind"] == "drift" or day(r) >= P.CONTRACT_SWITCH):
                cand.setdefault((w, x["i"]), []).append(x)
    chosen = {}
    for kind_ in ("drift", "breakdown"):
        for dc, _ in P.DISTRICTS:
            pool = [(w, i, x) for (w, i), xs in sorted(cand.items()) for x in xs
                    if w in (2, 3) and x["kind"] == kind_ and reg["district"][i] == dc and (w, i) not in chosen
                    and (kind_ == "drift" or i not in set(W["closing"]))]
            if pool:
                w, i, x = pool[int(rc.integers(len(pool)))]
                chosen[(w, i)] = x
    for (w, i), xs in sorted(cand.items()):
        if (w, i) not in chosen and rc.random() < COMBINE:
            chosen[(w, i)] = xs[0]
    for (w, i), x in chosen.items():
        x["v"] = rnd[i][w]
        x["combined"] = True
    for i in range(W["N"]):
        for w, r in enumerate(rnd[i]):
            visits.append({"i": i, "v": r, "kind": "scheduled", "opened": None, "alert": None, "status": "visit",
                           "combined": (w, i) in chosen, "closed": None, "vid": len(visits), "route": None})
    # remote resets: the new contractor clears some breakdowns from the office (no visit, no check); every district has
    # them at the stations it keeps
    rr = np.random.default_rng(seed + 41)
    can = [x for x in visits if x["kind"] == "breakdown" and x["status"] == "visit" and day(x["v"]) >= P.CONTRACT_SWITCH
           and not x["combined"] and x["route"] is None
           and not any(x["opened"] - 6 <= r <= x["v"] + 9 for r in rnd[x["i"]])
           and not any(y is not x and y["i"] == x["i"] and y["v"] is not None and y["status"] == "visit"
                       and x["opened"] - 6 <= y["v"] <= x["v"] + 9 for y in visits)]
    remote = [x for x in can if rr.random() < REMOTE]
    for dc, _ in P.DISTRICTS:
        pool = [x for x in can if reg["district"][x["i"]] == dc and x["i"] not in set(W["closing"])]
        if pool and not any(x in remote for x in pool):
            remote.append(pool[int(rr.integers(len(pool)))])
    # the new contractor checks a spare sensor at the workshop while a breakdown order is open; in every district where
    # the logger delivered a day it could be done on, one reset remotely at a kept station had one
    for dc, _ in P.DISTRICTS:
        pool = [x for x in can if reg["district"][x["i"]] == dc and x["i"] not in set(W["closing"])
                and _bench_days(W, x["i"], x["opened"], x["v"] + 2, span, code, ())]
        if pool and not any(x in remote for x in pool):
            remote.append(pool[int(rr.integers(len(pool)))])
    for x in remote:
        x["status"] = "remote"
    # each visit with a check: three as-found readings at ten-minute intervals; an adjustment when their error passes
    # 0.2 degrees, then three as-left readings once the sensor has settled
    checks, truth = [], []
    for x in visits:
        i, v = x["i"], x["v"]
        new_contractor = v is not None and day(v) >= P.CONTRACT_SWITCH
        if (x["status"] != "visit" or (x["kind"] == "breakdown" and not new_contractor)
                or (x["combined"] and x["kind"] != "scheduled")):
            truth.append(dict(x, as_found=None, adjusted=False))
            continue
        err = standing(i, v) + drift_at(i, v) + float(e[v, i])
        t0 = dt.datetime.combine(day(v), dt.time(int(rng.integers(8, 14)), int(rng.choice([0, 10, 20, 30, 40, 50]))))
        temp = float(rec["T"][v, i]) + float(rng.normal(0, 2.5))
        if (code[i], day(v)) in span:
            # the morning's air lies inside the day's range the station's logger recorded, both readings with it
            lo_, hi_ = span[(code[i], day(v))]
            lo_, hi_ = lo_ + 0.6 + max(0.0, -err), hi_ - 1.1 - max(0.0, err)
            temp = min(max(temp, lo_), hi_) if lo_ <= hi_ else (lo_ + hi_) / 2
        z = rng.normal(0, 0.03, 3)
        rows = []
        for j in range(3):
            std = round(temp + j * rng.normal(0.05, 0.08), 2)
            rows.append((t0 + dt.timedelta(minutes=10 * j), round(std + err + float(z[j] - z.mean()), 2), std))
        adjusted = abs(err) > FOUND
        if adjusted:
            t1 = t0 + dt.timedelta(minutes=20 + int(rng.integers(20, 46)))
            for j in range(3):
                std = round(temp + 0.3 + j * rng.normal(0.05, 0.08), 2)
                rows.append((t1 + dt.timedelta(minutes=10 * j), round(std + float(rng.normal(0, 0.04)), 2), std))
        found = round(float(np.mean([round(s - p, 2) for (_, s, p) in rows[:3]])), 3)
        truth.append(dict(x, as_found=found, adjusted=adjusted))
        for (ts, s, p) in rows:
            checks.append({"i": i, "ts": ts, "t_station": s, "t_standard": p, "kind": x["kind"], "v": v})
    # the new contractor checks a spare sensor at the workshop, at the ice point and the dry block's 40 degrees, before a
    # technician goes out on an order: on the order the desk then closed as a false alert, on a breakdown then reset
    # remotely, and before some drift-alert visits. Entered in the calibration database under the station's order, on a
    # workday the station's logger delivered, on no day a technician read the station's sensor there
    rb = np.random.default_rng(seed + 44)
    busy = {}
    for c_ in checks:
        busy.setdefault(c_["i"], set()).add(c_["v"])
    by_vid = {t["vid"]: t for t in truth}
    closing = set(W["closing"])
    h2 = [t for t in truth if t["kind"] in ("drift", "breakdown") and t["route"] is None and not t["combined"]
          and (t["v"] if t["v"] is not None else t["closed"]) is not None
          and day(t["v"] if t["v"] is not None else t["closed"]) >= P.CONTRACT_SWITCH]
    for t in truth:
        t["bench"] = None

    def window(t):
        if t["status"] == "office":
            return max(t["opened"], t["alert"] + 1), t["closed"]
        if t["status"] == "remote":
            return t["opened"], t["v"] + 2
        return t["opened"], t["v"] - 1

    def place(t):
        d0, d1 = window(t)
        ks = _bench_days(W, t["i"], d0, min(d1, D - 1), span, code, busy.get(t["i"], ()))
        if not ks:
            return False
        k = ks[int(rb.integers(len(ks)))]
        t["bench"] = k
        if t["status"] == "remote":
            t["v"] = max(t["v"], k)          # the order closes once the workshop's check is in
        busy.setdefault(t["i"], set()).add(k)
        checks.extend(_bench_rows(rb, t, k))
        return True

    office = [t for t in h2 if t["kind"] == "drift" and t["status"] == "office"]
    remote_k = [t for t in h2 if t["kind"] == "breakdown" and t["status"] == "remote" and t["i"] not in closing]
    went = [t for t in h2 if t["kind"] == "drift" and t["status"] == "visit" and t["v"] > t["opened"]]
    for t in office:                                    # every false alert the desk closed
        place(t)
    for dc, _ in P.DISTRICTS:                           # one breakdown reset remotely a district
        pool = [t for t in remote_k if reg["district"][t["i"]] == dc]
        for n in rb.permutation(len(pool)):
            if place(pool[int(n)]):
                break
    for dc, _ in P.DISTRICTS:                           # before a drift-alert visit, in every district with no closure
        pool = [t for t in went if reg["district"][t["i"]] == dc]
        if any(t["bench"] is not None for t in office if reg["district"][t["i"]] == dc) and rb.random() < 0.6:
            continue
        for n in rb.permutation(len(pool)):
            if place(pool[int(n)]):
                break
    checks.sort(key=lambda c_: (c_["ts"], c_["i"]))
    return visits, checks, truth


SET_POINTS = (0.0, 40.0)        # the workshop's two-point check: the ice point and the dry block at 40 degrees
BENCH_MARGIN = 3.0              # each point at least this far outside the day's range at the station


def _bench_days(W, i, d0, d1, span, code, busy):
    """the workdays from d0 to d1 on which the station's logger delivered a day the quality control read, both of the
    workshop's points lie well outside the range it recorded, and no technician read the station's sensor there"""
    out = []
    for k in range(d0, min(d1, D - 1) + 1):
        if day(k).weekday() >= 5 or k in busy or not W["avail"][k, i]:
            continue
        r_ = span.get((code[i], day(k)))
        if r_ is not None and r_[0] >= SET_POINTS[0] + BENCH_MARGIN and r_[1] <= SET_POINTS[1] - BENCH_MARGIN:
            out.append(k)
    return out


def _bench_rows(rb, t, k):
    """three paired readings at each point, ten minutes apart, the spare's own small error in both"""
    t0 = dt.datetime.combine(day(k), dt.time(int(rb.integers(8, 13)), int(rb.choice([0, 10, 20, 30, 40, 50]))))
    e0 = float(rb.normal(0, 0.05))
    rows = []
    for p, sp in enumerate(SET_POINTS):
        tp = t0 + dt.timedelta(minutes=0 if p == 0 else 30 + int(rb.integers(0, 16)))
        for j in range(3):
            std = round(sp + float(rb.normal(0, 0.02)), 2)
            rows.append({"i": t["i"], "ts": tp + dt.timedelta(minutes=10 * j), "kind": t["kind"], "v": k,
                         "t_station": round(std + e0 + float(rb.normal(0, 0.02)), 2), "t_standard": std,
                         "bench": t["vid"]})
    return rows


def complete_daily(daily, checks, reg, rec, seed=250):
    """a day a technician read the station's sensor holds a row in the loggers' export (the logger restarted at the visit,
    a part day when it had been down), its range taking in the visit's readings"""
    rng = np.random.default_rng(seed + 32)
    code = list(reg["code"])
    five_from = dict(zip(reg["code"], reg["five_min_from"]))
    lo_hi = {}
    for c_ in checks:
        if c_.get("bench") is not None:
            continue
        key = (code[c_["i"]], day(c_["v"]))
        a, b = lo_hi.get(key, (np.inf, -np.inf))
        lo_hi[key] = (min(a, c_["t_station"], c_["t_standard"]), max(b, c_["t_station"], c_["t_standard"]))
    df = daily.copy()
    first = ~df.duplicated(["estacion", "fecha"])
    pos = {(s_, d_): n for n, (s_, d_) in enumerate(zip(df["estacion"], df["fecha"])) if first.iloc[n]}
    add = []
    for (s_, d_), (a, b) in sorted(lo_hi.items()):
        if (s_, d_) in pos:
            n = pos[(s_, d_)]
            lo_, hi_ = df.at[df.index[n], "tmin"], df.at[df.index[n], "tmax"]
            if lo_ > a - 0.2 or hi_ < b + 0.2:
                mask = (df["estacion"] == s_) & (df["fecha"] == d_)
                df.loc[mask, "tmin"] = round(min(lo_, a - 0.2 - float(rng.uniform(0, 0.6))), 1) + 0.0
                df.loc[mask, "tmax"] = round(max(hi_, b + 0.2 + float(rng.uniform(0, 0.6))), 1) + 0.0
            continue
        k = (d_ - P.START).days
        five = five_from[s_] is not None and d_ >= five_from[s_]
        n_rec = int(rng.integers(max(1, scheduled(d_, five) // 3), accept_min(d_, five)))
        t = float(rec["T"][k, code.index(s_)])
        add.append((s_, d_, round(t + float(rng.normal(0, 0.6)), 1) + 0.0,
                    round(max(t + 2.5, b + 0.2) + float(rng.uniform(0, 1.5)), 1) + 0.0,
                    round(min(t - 2.5, a - 0.2) - float(rng.uniform(0, 1.5)), 1) + 0.0, n_rec))
    if add:
        df = pd.concat([df, pd.DataFrame(add, columns=df.columns)])
    return df.sort_values(["estacion", "fecha"], kind="stable").reset_index(drop=True)


# ------------------------------------------------------------------ the exports of the work orders and the checks
OLD_EXPORT_TO = dt.date(2027, 6, 30)     # the old contractor's export for the handover
CANCEL, OFFICE = 0.06, 0.07              # drift orders cancelled before any visit; closed from the office without one
REMOTE, COMBINE = 0.30, 0.5


def orders_and_checks(W, rec, reg, visits, checks, truth, seed=250):
    rng = np.random.default_rng(seed + 50)
    code = list(reg["code"])
    tv = sorted(truth, key=lambda t: ((t["v"] if t["v"] is not None else (t["closed"] or t["opened"])), t["i"], t["kind"]))
    alert_at = {}
    for (i, k) in rec["alerts"]:
        alert_at.setdefault(i, []).append(k)
    rs = np.random.default_rng(seed + 51)
    for dc, _ in P.DISTRICTS:          # every district has drift orders closed from the office, without a visit, in 2027
        pool = [t for t in tv if t["kind"] == "drift" and reg["district"][t["i"]] == dc and t["status"] == "office"
                and day(t["closed"]).year == 2027]
        if not pool:
            alt = [t for t in tv if t["kind"] == "drift" and reg["district"][t["i"]] == dc and t["status"] == "cancelled"
                   and day(t["opened"]).year == 2027 and t.get("bench") is None]
            if alt:
                t = alt[int(rs.integers(len(alt)))]
                t["status"] = "office"
                t["closed"] = workday(t["alert"] + 2)
    route_ref = {}
    old_rows, new_rows, ref_of = [], [], {}
    seq = {}
    notes_old = {"drift": ["revisión sensor T", "aviso CC", "comprobación con patrón", "", ""],
                 "breakdown": ["sin comunicación", "batería", "módem", "panel solar", "sin datos", ""],
                 "scheduled": ["campaña primavera", "", ""]}
    notes_new = ["", "", "", "visit done", "checked station", "sensor check", "logger checked", "site tidied"]
    # an order nobody went out on carries no note saying someone did: the office closures, the true cancellations and
    # the new contractor's remote resets take a plain note instead (blank or "closed", which visits carry too)
    rq = np.random.default_rng(seed + 53)
    went_old, went_new = {"revisión sensor T", "comprobación con patrón"}, set(notes_new[3:])
    for t in tv:
        if t["status"] == "absorbed":
            continue
        when = day(t["v"]) if t["v"] is not None else day(t["closed"] or t["opened"])
        if when < P.CONTRACT_SWITCH:
            y = when.year % 100
            seq[("TM", y)] = seq.get(("TM", y), 0) + 1
            ref = "TM-%02d-%04d" % (y, seq[("TM", y)])
            ref_of[id(t)] = ref
            if when > OLD_EXPORT_TO:
                continue
            tipo = {"drift": "Alerta deriva", "breakdown": "Avería", "scheduled": "Revisión anual"}[t["kind"]]
            gone = t["status"] == "cancelled"
            visita = None if (gone or t["v"] is None) else day(t["v"])     # the office closes an order without a visit blank
            note = "alerta cerrada" if gone else rng.choice(notes_old[t["kind"]])
            if t["status"] == "office" and note in went_old:
                note = str(rq.choice(["aviso CC", ""]))
            old_rows.append({"Nº orden": ref, "Estación": code[t["i"]], "Tipo": tipo,
                             "Aviso": day(t["opened"]) if t["opened"] is not None else None,
                             "Visita": visita, "Estado": "Anulada" if gone else "Cerrada",
                             "Observaciones": note})
        else:
            partner = None
            if t["route"] is not None:
                partner = next(b for b in tv if b["vid"] == t["route"])
                if partner["vid"] in route_ref:
                    ref_of[id(t)] = route_ref[partner["vid"]]
                    continue
            seq[("SA", 27)] = seq.get(("SA", 27), 0) + 1
            ref = "SA-27-%04d" % seq[("SA", 27)]
            ref_of[id(t)] = ref
            route_ref[t["vid"]] = ref
            st = code[t["i"]]
            opened = t["opened"]
            if partner is not None:
                st = "%s / %s" % (st, code[partner["i"]])
                opened = max(opened, partner["opened"])
            close = None
            base = t["v"] if t["v"] is not None else t["closed"]
            if base is not None:
                close = day(base) + dt.timedelta(days=int(rng.choice([0, 1, 1, 1, 2, 2, 3])))
                while close.weekday() >= 5:
                    close += dt.timedelta(days=1)
            gone = t["status"] == "cancelled"
            note = rng.choice(notes_new)
            nobody = t["status"] in ("office", "remote", "cancelled") and (partner is None
                                                                          or partner["status"] in ("office", "remote", "cancelled"))
            if nobody and note in went_new:
                note = str(rq.choice(["", "closed"]))
            elif not nobody and note == "" and rq.random() < 0.15:
                note = "closed"
            new_rows.append({"order_ref": ref, "station": st,
                             "work_type": "Preventive" if t["kind"] == "scheduled" else "Corrective",
                             "opened": day(opened) if opened is not None else None,
                             "visit_date": None if gone else close,
                             "status": "Cancelled" if gone else "Closed",
                             "notes": note})
    # the calibration database's entry form fills in the last order used at the station: at some drift-alert and
    # breakdown visits of 2027 the readings went in under the station's previous order, the visit's own order closed
    # with its date and nothing under it. A drift-alert visit a district; since July 2027 only where the desk's closures
    # carry no workshop check, and none or two or three breakdown visits a district, so the readings a tablet moved never
    # number the orders that hold only a workshop check
    exported = {r["Nº orden"] for r in old_rows} | {r["order_ref"] for r in new_rows}
    reads = [t for t in tv if t["v"] is not None and t["status"] == "visit" and t["as_found"] is not None]
    at = {}
    for t in reads:
        at.setdefault(t["i"], []).append(t)
    rk = np.random.default_rng(seed + 52)
    for t in tv:
        t["miskeyed"] = None
    closing = set(W["closing"])
    sw = (P.CONTRACT_SWITCH - P.START).days
    desk_bench = {reg["district"][t["i"]] for t in tv if t["kind"] == "drift" and t["status"] == "office"
                  and t.get("bench") is not None}
    carried = set()          # the orders a tablet carried forward: each holds its own visit's readings and one more

    def pool_of(kind_, dc):
        pool = []
        for t in reads:
            if (t["kind"] != kind_ or reg["district"][t["i"]] != dc or day(t["v"]).year != 2027 or t["combined"]
                    or ref_of[id(t)] not in exported or t["miskeyed"] is not None
                    or (kind_ == "breakdown" and t["i"] in closing) or ref_of[id(t)] in carried
                    or (kind_ == "drift" and dc in desk_bench and t["v"] >= sw)):
                continue
            prev = [x for x in at[t["i"]] if x["v"] < t["v"] and ref_of[id(x)] in exported and x["route"] is None]
            if not prev or any(x is not t and t["opened"] - 5 <= x["v"] <= t["v"] + 8 for x in at[t["i"]]):
                continue
            a = max(prev, key=lambda x: x["v"])
            if a["miskeyed"] is not None or ref_of[id(a)] in carried:
                continue
            pool.append((t, a))
        return pool

    for kind_ in ("drift", "breakdown"):
        for dc, _ in P.DISTRICTS:
            n = 1 if kind_ == "drift" else int(rk.choice([0, 2, 2, 3]))
            if kind_ == "breakdown" and len(pool_of(kind_, dc)) < 2:
                n = 0
            got = []
            for _ in range(n):
                pool = pool_of(kind_, dc)
                if not pool:
                    break
                t, a = pool[int(rk.integers(len(pool)))]
                t["miskeyed"] = ref_of[id(a)]
                carried.add(ref_of[id(a)])
                got.append(t)
            if kind_ == "breakdown" and len(got) == 1:      # never one: undo it
                got[0]["miskeyed"] = None
                carried.discard(ref_of[id(max([x for x in at[got[0]["i"]] if x["v"] < got[0]["v"]
                                              and ref_of[id(x)] in exported and x["route"] is None],
                                             key=lambda x: x["v"]))])
    # the checks, each under its visit's order (or the order the tablet carried forward)
    vis_key = {}
    by_vid = {}
    for t in tv:
        by_vid[t["vid"]] = t
        if t["v"] is not None and t["status"] == "visit":
            vis_key[(t["i"], t["v"], t["kind"])] = t["miskeyed"] or ref_of[id(t)]
    ck = sorted(checks, key=lambda c: (c["ts"], c["i"]))
    rows = []
    for n, c in enumerate(ck, 1):
        if c.get("bench") is not None:
            t = by_vid[c["bench"]]
            key = (t["miskeyed"] or ref_of[id(t)]) if t["status"] == "visit" else ref_of[id(t)]
        else:
            key = vis_key[(c["i"], c["v"], c["kind"])]
        rows.append({"id_lectura": 100000 + n, "estacion": code[c["i"]], "fecha_hora": c["ts"].strftime("%Y-%m-%d %H:%M"),
                     "t_estacion": c["t_station"] + 0.0, "t_patron": c["t_standard"] + 0.0,
                     "orden": key,
                     "tecnico": "T%02d" % (1 + (c["i"] + c["v"]) % 2 + (2 if day(c["v"]) >= P.CONTRACT_SWITCH else 0))})
    return pd.DataFrame(old_rows), pd.DataFrame(new_rows), pd.DataFrame(rows), ref_of
