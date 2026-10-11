"""Simulate the Corran world: weather, premises, supplies, accounts and daily recorded kWh.

Deterministic for a given world.SEED. Returns plain Python / numpy structures; the writers in
build.py turn them into the shipped files.
"""
import datetime as dt
import numpy as np
import world as W

D0 = W.MART_START                       # day index 0 for every daily array
NDAYS = (W.EXTRACT_DATE - D0).days      # through Sunday 6 Dec 2026


def day_index(d):
    return (d - D0).days


def mpan_check_digit(first12):
    primes = [3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    return str(sum(int(c) * p for c, p in zip(first12, primes)) % 11 % 10)


def make_hdd(rng):
    """Daily heating degree days (15.5C base) per station from HDD_START to the extract."""
    start = W.HDD_START
    n = (W.EXTRACT_DATE - start).days
    days = [start + dt.timedelta(i) for i in range(n)]
    doy = np.array([d.timetuple().tm_yday for d in days])
    out = {}
    for k, (station, (mean, amp, a25, a26)) in enumerate(W.STATIONS.items()):
        srng = np.random.default_rng(W.SEED + 1000 + k)
        clim = mean - amp * np.cos(2 * np.pi * (doy - 18) / 365.25)
        # weather noise: AR(1) daily anomaly
        e = np.zeros(n)
        z = srng.normal(0, 1.9, n)
        for i in range(1, n):
            e[i] = 0.72 * e[i - 1] + z[i]
        anom = np.zeros(n)
        for i, d in enumerate(days):
            if dt.date(2025, 9, 15) <= d <= dt.date(2025, 12, 31):
                anom[i] = a25
            if dt.date(2026, 9, 15) <= d <= dt.date(2026, 12, 31):
                anom[i] = a26
        tmean = clim + e + anom
        hdd = np.clip(W.HDD_BASE_C - tmean, 0, None)
        out[station] = {"days": days, "tmean": np.round(tmean, 1), "hdd": hdd}
    return out


def build_world():
    rng = np.random.default_rng(W.SEED)
    hdd_all = make_hdd(rng)
    # daily hdd aligned on D0 for each station, recomputed from the rounded tmean so the shipped
    # file (which carries rounded mean temperatures and degree days) is the exact model input
    off = (D0 - W.HDD_START).days
    station_hdd = {}
    for s, v in hdd_all.items():
        h = np.round(np.clip(W.HDD_BASE_C - v["tmean"], 0, None), 1)
        v["hdd"] = h
        station_hdd[s] = h[off:off + NDAYS]

    premises, supplies, accounts = [], [], []
    uprn_seq = rng.choice(np.arange(130_004_000_000, 130_009_999_999), size=4000, replace=False)
    uprn_seq.sort()
    rng.shuffle(uprn_seq)
    acct_seq = iter(rng.choice(np.arange(40_100_000, 49_999_999), size=8000, replace=False))
    mpan_body = iter(rng.choice(np.arange(10_000_000, 99_999_999), size=8000, replace=False))
    serial_seq = iter(rng.choice(np.arange(100_000, 999_999), size=9000, replace=False))
    u_i = 0

    def new_mpan():
        first12 = "17" + "00" + f"{next(mpan_body):08d}"
        return first12 + mpan_check_digit(first12)

    def new_serial(kind):
        pre = {"main": "21L", "heat": "19K", "x": "23M"}[kind]
        return f"{pre}{next(serial_seq):07d}"

    for p in W.PATCHES:
        P = dict(zip(W.PATCH_COLS, p))
        prng = np.random.default_rng(W.SEED + sum(ord(c) * 31 ** k for k, c in enumerate(P["code"])))
        n = P["n"]
        n_heat = int(round(n * P["heat"]))
        idx = np.arange(n)
        heat_flags = np.zeros(n, bool)
        heat_flags[prng.choice(idx, n_heat, replace=False)] = True
        # roles are assigned to disjoint premises
        single = [i for i in idx if not heat_flags[i]]
        heated = [i for i in idx if heat_flags[i]]
        prng.shuffle(single)
        prng.shuffle(heated)
        role = {}
        # prepayment premises take no diversion, void or retrofit role
        n_pp = int(round(n * P["prepay"]))
        pp = set(single[:int(n_pp * 0.8)]) | set(heated[:n_pp - int(n_pp * 0.8)])
        single_c = [i for i in single if i not in pp]
        heated_c = [i for i in heated if i not in pp]
        k = 0
        for i in single_c[k:k + P["whole"]]:
            role[i] = "whole"
        k += P["whole"]
        spare_heated = len(heated_c) - P["heatdiv"] - P["retrofit"] - 3
        nv_heated = max(0, min(P["voids"] // 3, spare_heated))
        nv_single = P["voids"] - nv_heated
        for i in single_c[k:k + nv_single]:
            role[i] = "void"
        k += nv_single
        hist_single = single_c[k:k + 6]          # change of occupier in the baseline weeks only
        for i in hist_single:
            role[i] = "histvoid"
        k += 6
        j = 0
        for i in heated_c[j:j + P["heatdiv"]]:
            role[i] = "heatdiv"
        j += P["heatdiv"]
        for i in heated_c[j:j + nv_heated]:
            role[i] = "void"
        j += nv_heated
        for i in heated_c[j:j + P["retrofit"]]:
            role[i] = "retrofit"
        j += P["retrofit"]
        for i in heated_c[j:j + 3]:
            role[i] = "histretro"               # heat pump fitted in spring 2025, inside the baseline
        j += 3

        for i in idx:
            uprn = int(uprn_seq[u_i]); u_i += 1
            prem = {
                "uprn": uprn, "patch": P["code"], "heat": bool(heat_flags[i]),
                "prepay": i in pp, "role": role.get(i, "ordinary"),
                "base": float(prng.lognormal(np.log(P["base"]), 0.28)),
                "sens": float(max(0.0, prng.normal(P["sens"], 0.06))),
                "hsens": float(prng.uniform(*W.HEAT_SENS)) if heat_flags[i] else 0.0,
                "drift": float(prng.uniform(*W.LEGIT_DRIFT)),
                "drift_day": dt.date(2025, 3, 1) + dt.timedelta(int(prng.integers(0, 560))),
            }
            if prem["heat"]:
                # storage-heated premises: day-to-day use carries less direct heating
                prem["sens"] *= 0.45
            r = prem["role"]
            if r in ("whole", "heatdiv"):
                prem["f"] = float(prng.uniform(*(W.WHOLE_DIV_F if r == "whole" else W.HEAT_DIV_F)))
                span = (W.DIV_ONSET[1] - W.DIV_ONSET[0]).days
                prem["onset"] = W.DIV_ONSET[0] + dt.timedelta(int(prng.integers(0, span + 1)))
                prem["drift"] = 1.0 + (prem["drift"] - 1.0) * 0.4
            if r == "void":
                prem["out"] = dt.date(2026, 8, 10) + dt.timedelta(int(prng.integers(0, 55)))
                prem["in"] = None          # still empty at the extract; the next occupier is not yet known
                prng.random()
                prem["vf"] = float(prng.uniform(*W.VOID_FACTOR))
            if r == "histvoid":
                prem["out"] = dt.date(2025, 4, 1) + dt.timedelta(int(prng.integers(0, 160)))
                prem["in"] = prem["out"] + dt.timedelta(int(prng.integers(14, 70)))
                prem["vf"] = float(prng.uniform(*W.VOID_FACTOR))
            if r == "retrofit":
                span = (W.RETROFIT_WINDOW[1] - W.RETROFIT_WINDOW[0]).days
                prem["hp_day"] = W.RETROFIT_WINDOW[0] + dt.timedelta(int(prng.integers(0, span + 1)))
            if r == "histretro":
                prem["hp_day"] = dt.date(2025, 3, 2) + dt.timedelta(int(prng.integers(0, 80)))
            premises.append(prem)

    # supplies ---------------------------------------------------------------------------------
    for prem in premises:
        main = {"mpan": new_mpan(), "uprn": prem["uprn"], "kind": "main",
                "serial": new_serial("main")}
        prem["supplies"] = [main]
        supplies.append(main)
        if prem["heat"]:
            h = {"mpan": new_mpan(), "uprn": prem["uprn"], "kind": "heat",
                 "serial": new_serial("heat"), "related": main["mpan"]}
            main["related"] = h["mpan"]
            prem["supplies"].append(h)
            supplies.append(h)

    # accounts: one live account per occupancy; voids sit on a deemed occupier account ---------
    for prem in premises:
        a0 = f"CE{next(acct_seq):08d}"
        periods = []
        if prem["role"] in ("void", "histvoid"):
            periods.append((a0, dt.date(2019, 1, 1), prem["out"] - dt.timedelta(1), "named"))
            occ = f"CE{next(acct_seq):08d}"
            end = (prem["in"] - dt.timedelta(1)) if prem["in"] else None
            periods.append((occ, prem["out"], end, "occupier"))
            if prem["in"]:
                periods.append((f"CE{next(acct_seq):08d}", prem["in"], None, "named"))
        else:
            periods.append((a0, dt.date(2019, 1, 1), None, "named"))
        prem["accounts"] = periods
        for a in periods:
            accounts.append({"account_ref": a[0], "uprn": prem["uprn"], "start": a[1],
                             "end": a[2], "kind": a[3]})

    # daily recorded consumption ------------------------------------------------------------------
    days = np.array([D0 + dt.timedelta(i) for i in range(NDAYS)])
    patch_station = {p[0]: p[2] for p in W.PATCHES}
    for prem in premises:
        srng = np.random.default_rng(prem["uprn"] % (2 ** 32))
        hdd = station_hdd[patch_station[prem["patch"]]]
        di = day_index(prem["drift_day"])
        level = np.ones(NDAYS)
        level[di:] = prem["drift"]
        # weekday texture
        wk = np.array([1.06 if d.weekday() >= 5 else 0.975 for d in days])
        main_true = (prem["base"] * wk + prem["sens"] * hdd) * level
        main_true *= srng.lognormal(0, W.DAILY_NOISE_MAIN, NDAYS)
        heat_true = None
        if prem["heat"]:
            heat_true = (prem["hsens"] * hdd + 0.15) * level
            heat_true *= srng.lognormal(0, W.DAILY_NOISE_HEAT, NDAYS)
        rec_main = main_true.copy()
        rec_heat = heat_true.copy() if heat_true is not None else None
        r = prem["role"]
        if r == "whole":
            rec_main[day_index(prem["onset"]):] *= (1 - prem["f"])
        if r == "heatdiv":
            rec_heat[day_index(prem["onset"]):] *= (1 - prem["f"])
        if r in ("void", "histvoid"):
            a = day_index(prem["out"])
            b = day_index(prem["in"]) if prem["in"] else NDAYS
            rec_main[a:b] *= prem["vf"]
            if rec_heat is not None:
                rec_heat[a:b] *= prem["vf"] * 0.6
        if r in ("retrofit", "histretro"):
            a = day_index(prem["hp_day"])
            moved = heat_true[a:] / W.HP_COP
            rec_main[a:] += moved
            rec_heat[a:] *= 0.035
        prem["supplies"][0]["kwh"] = np.round(rec_main, 3)
        if prem["heat"]:
            prem["supplies"][1]["kwh"] = np.round(rec_heat, 3)

    return {"days": days, "hdd": hdd_all, "station_hdd": station_hdd, "premises": premises,
            "supplies": supplies, "accounts": accounts}
