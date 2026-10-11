"""The golden solve, from target/ alone. Loads and cleans the network extract (identities through the register,
feet, measuring points in force, pumped and duplicate dips, logger compensation and Queensland days), computes
each bore's September 2026 assessment level and baseline level, every naive rung, the answer grid and the asks.
deliver.py writes the deliverables from solve(); checks.py asserts on it; verify.py recomputes on its own path."""
import datetime as dt
import os
import re

import numpy as np
import openpyxl
import pandas as pd
import pyarrow.parquet as pq

import analysis as A
import models as M

FT = 0.3048
KPA_PER_M = 9.80665
AEST_OFFSET = np.timedelta64(10, "h")
DIPS = "water_level_dips_2012-2026.csv"
LOGGERS = "logger_pressure_2015-2026.parquet"
INSTALLS = "logger_installations.csv"
BARO = "barometric_logger_2015-2026.csv"
CLIMATE = "daily_climate_1990-2026.csv"
TAKE = "pit_dewatering_2022-2026.csv"
REGISTER = "landholder_bore_register.xlsx"
PUMPED = re.compile(r"\bpump(ed|ing)?\b", re.I)
NOT_PUMPED = re.compile(r"\bpump off\b", re.I)
PRIMARY = ("gammac", "first", "daily", "logger")   # the continuous gamma fit; the grid keeps the coarse one


# ------------------------------------------------------------------ the register

def unit_of(aquifer):
    a = aquifer.lower()
    return "alluvium" if "alluvium" in a else ("basalt" if "basalt" in a else "coal")


def load_register(target):
    wb = openpyxl.load_workbook(os.path.join(target, REGISTER), read_only=True, data_only=True)
    ws = wb["Landholder bores"]
    rows = list(ws.iter_rows(min_row=4, values_only=True))
    head = rows[0]
    bores = {}
    for r in rows[1:]:
        if not r[0] or not str(r[0]).startswith("KV-"):
            continue
        x = dict(zip(head, r))
        bores[x["Bore"]] = dict(code=x["Bore"], rn=str(x["Registered number"]), name=x["Landholder's name for the bore"],
                                prop=x["Property"], owner=x["Owner"], aquifer=x["Aquifer"], unit=unit_of(x["Aquifer"]),
                                cls=x["Aquifer class"], base_date=_date(x["Baseline assessment"]),
                                base_depth=float(x["Baseline static water level (m below MP)"]),
                                complaint=_date(x["Complaint received (MG-02 7.1)"]), kind="landholder")
    net = {}
    rows = list(wb["Network bores"].iter_rows(min_row=4, values_only=True))
    head = rows[0]
    for r in rows[1:]:
        if not r[0] or not str(r[0]).startswith("KV-"):
            continue
        x = dict(zip(head, r))
        net[x["Bore"]] = dict(code=x["Bore"], rn=str(x["Registered number"]), aquifer=x["Aquifer"],
                              unit=unit_of(x["Aquifer"]), cls=x["Aquifer class"],
                              kind="reference" if "reference" in x["Type"] else "mine")
    mps = {}
    rows = list(wb["Measuring points"].iter_rows(min_row=4, values_only=True))
    head = rows[0]
    for r in rows[1:]:
        if not r[0] or not str(r[0]).startswith("KV-"):
            continue
        x = dict(zip(head, r))
        mps.setdefault(x["Bore"], []).append((_date(x["In force from"]), _date(x["In force to"]),
                                              float(x["MP elevation (m AHD)"])))
    return bores, net, mps


def _date(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.datetime.strptime(str(v), "%d/%m/%Y").date()


def mp_on(mps, code, day, latest=False):
    rows = sorted(mps[code], key=lambda x: x[0])
    if latest:
        return rows[-1][2]
    for fr, to, elev in rows:
        if fr <= day and (to is None or day <= to):
            return elev
    raise ValueError("no measuring point for %s on %s" % (code, day))


def identity(bores, net):
    """Every way a bore is written in the extract, normalised, to its code."""
    out = {}
    for code, b in list(bores.items()) + list(net.items()):
        short = code.split("-", 1)[1]
        for key in (code, code.replace("-", ""), short, code.replace("-", " ", 1), b["rn"], "RN" + b["rn"]):
            out[norm_site(key)] = code
    return out


def norm_site(s):
    return re.sub(r"[\s\-]", "", str(s)).upper()


# ------------------------------------------------------------------ dips

def load_dips(target, bores, net, mps, ids, pumped="remark", dedupe=True, feet=True, mp_history=True):
    """Static dips as reduced levels. pumped: 'remark' (drop dips whose remarks say the pump was on), 'outlier' (drop
    by the robust rule) or 'keep'. The other switches undo one cleaning step each (for the mess checks)."""
    d = pd.read_csv(os.path.join(target, DIPS), dtype=str, keep_default_na=False)
    d["code"] = [ids.get(norm_site(s)) for s in d["site"]]
    if d["code"].isna().any():
        raise ValueError("unmapped sites: %s" % sorted(set(d.loc[d["code"].isna(), "site"])))
    if dedupe:
        d = d.drop_duplicates(subset=["code", "reading_date", "reading_time", "dtw", "units", "remarks", "officer"])
    d["day"] = pd.to_datetime(d["reading_date"]).dt.date
    v = d["dtw"].astype(float)
    if feet:
        v = np.where(d["units"] == "ft", v * FT, v)
    d["depth_m"] = v
    d["mp"] = [mp_on(mps, c, x, latest=not mp_history) for c, x in zip(d["code"], d["day"])]
    d["rl"] = d["mp"] - d["depth_m"]
    d["dn"] = [M.dnum(x) for x in d["day"]]
    d["pump_remark"] = [bool(PUMPED.search(r)) and not NOT_PUMPED.search(r) for r in d["remarks"]]
    d["pump_outlier"] = outliers(d)
    if pumped == "remark":
        d = d[~d["pump_remark"]]
    elif pumped == "outlier":
        d = d[~d["pump_outlier"]]
    return d


def outliers(d, drop=1.2, days=50):
    """The robust rule: a dip more than drop metres below the median of the bore's readings up to two either side of
    it, those within days of it."""
    out = np.zeros(len(d), bool)
    order = np.lexsort((d["reading_time"].values, d["dn"].values.astype(int), d["code"].values))
    rl, dn, code = d["rl"].values.astype(float), d["dn"].values.astype(int), d["code"].values
    for c in sorted(set(code)):
        ii = order[code[order] == c]
        for pos, j in enumerate(ii):
            nb = [ii[p] for p in (pos - 2, pos - 1, pos + 1, pos + 2) if 0 <= p < len(ii) and abs(dn[ii[p]] - dn[j]) <= days]
            if len(nb) >= 2 and rl[j] < np.median(rl[nb]) - drop:
                out[j] = True
    return out


# ------------------------------------------------------------------ loggers

def load_loggers(target, mps, compensate=True, day_basis="aest", density=KPA_PER_M):
    """Logger daily levels: {code: (day numbers, levels)}. Each hour's compensated level is the measuring point
    in force less the sensor depth plus (logger kPa - barometric kPa) / 9.80665; the day is Queensland's."""
    inst = pd.read_csv(os.path.join(target, INSTALLS), dtype=str, keep_default_na=False)
    baro = pd.read_csv(os.path.join(target, BARO), dtype=str)
    bt = pd.to_datetime(baro["timestamp_utc"].str.replace("Z", "", regex=False)).values.astype("datetime64[s]")
    bp = baro["pressure_kpa"].astype(float).values
    border = np.argsort(bt)
    bt, bp = bt[border], bp[border]
    t = pq.read_table(os.path.join(target, LOGGERS))
    serial = np.array(t.column("logger_serial").to_pylist())
    ts = t.column("timestamp_utc").to_numpy().astype("datetime64[s]")
    kpa = t.column("pressure_kpa").to_numpy()
    out = {}
    for _, row in inst.iterrows():
        if not row["sensor_depth_below_mp_m"]:
            continue
        code, s = row["site"], row["logger_serial"]
        sel = serial == s
        tt, pp = ts[sel], kpa[sel]
        pos = np.searchsorted(bt, tt)
        pos = np.clip(pos, 0, len(bt) - 1)
        has = bt[pos] == tt
        tt, pp, b = tt[has], pp[has], bp[pos[has]]
        local = tt + AEST_OFFSET if day_basis == "aest" else tt
        days = local.astype("datetime64[D]")
        dnum = (days - np.datetime64("1990-01-01")).astype(int)
        mp = np.array([mp_on(mps, code, M.D0 + dt.timedelta(days=int(x))) for x in np.unique(dnum)])
        mp_by_day = dict(zip(np.unique(dnum), mp))
        mpv = np.array([mp_by_day[x] for x in dnum])
        column = (pp - b) / density if compensate else pp / density
        level = mpv - float(row["sensor_depth_below_mp_m"]) + column
        u, inv = np.unique(dnum, return_inverse=True)
        mean = np.bincount(inv, level) / np.bincount(inv)
        if code in out:
            u0, m0 = out[code]
            keep = ~np.isin(u0, u)
            u, mean = np.concatenate([u0[keep], u]), np.concatenate([m0[keep], mean])
            order = np.argsort(u)
            u, mean = u[order], mean[order]
        out[code] = (u, mean)
    return out


# ------------------------------------------------------------------ climate and take

def load_climate(target):
    c = pd.read_csv(os.path.join(target, CLIMATE))
    assert c["date"].iloc[0] == "1990-01-01"
    take = pd.read_csv(os.path.join(target, TAKE))
    tot = take.groupby("date")["volume_ml"].sum()
    q = np.zeros(len(c))
    pos = {x: i for i, x in enumerate(c["date"])}
    for day, v in tot.items():
        if day in pos:
            q[pos[day]] = v
    return M.Climate(c["rain_mm"].values, c["morton_apet_mm"].values, q), c, take


# ------------------------------------------------------------------ assembling the bores

def observations(target, pumped="remark", dedupe=True, feet=True, mp_history=True, compensate=True, day_basis="aest",
                 drop_feet=False, density=KPA_PER_M):
    bores, net, mps = load_register(target)
    ids = identity(bores, net)
    dips = load_dips(target, bores, net, mps, ids, pumped=pumped, dedupe=dedupe, feet=feet, mp_history=mp_history)
    if drop_feet:
        dips = dips[dips["units"] != "ft"]
    logs = load_loggers(target, mps, compensate=compensate, day_basis=day_basis, density=density)
    obs = {}
    for code, b in list(bores.items()) + list(net.items()):
        sub = dips[dips["code"] == code].sort_values(["dn", "reading_time"], kind="stable")
        o = dict(unit=b["unit"], cls=b["cls"], kind=b["kind"],
                 dips=(sub["dn"].values.astype(int), sub["rl"].values.astype(float)),
                 logger=logs.get(code), baseline=None)
        if b["kind"] == "landholder":
            o["baseline"] = mp_on(mps, code, b["base_date"], latest=not mp_history) - b["base_depth"]
        obs[code] = o
    return obs, bores, net, mps, dips


# ------------------------------------------------------------------ the solve

def solve(target, with_grid=True, **kw):
    cl, climate_df, take_df = load_climate(target)
    obs, bores, net, mps, dips = observations(target, **kw)
    LH = sorted(bores)
    REF = sorted(k for k, v in net.items() if v["kind"] == "reference")
    MINEB = sorted(k for k, v in net.items() if v["kind"] == "mine")
    rungs, info = A.rungs(obs, LH, REF, cl)
    g = dict(cl=cl, obs=obs, bores=bores, net=net, mps=mps, dips=dips, LH=LH, REF=REF, MINE=MINEB, rungs=rungs,
             info=info)
    g["levels"] = info["levels"]
    prim = {}
    fits = {}
    for k in LH:
        prim[k], fits[k] = A.cell(obs, k, cl, *PRIMARY)
    g["drawdown"] = prim
    g["fits"] = fits
    g["impaired"] = {k: prim[k] > A.TRIGGER[obs[k]["cls"]] for k in LH}
    g["answer"] = sorted(k for k in LH if g["impaired"][k])
    g["change"] = {k: g["levels"][k] - obs[k]["baseline"] for k in LH}
    owners = {}
    for k in g["answer"]:
        owners.setdefault(bores[k]["owner"], []).append(k)
    g["offers"] = owners
    g["complainants"] = sorted((k for k in LH if bores[k]["complaint"]), key=lambda k: bores[k]["complaint"])
    if with_grid:
        g["grid"] = A.grid(obs, LH, cl)
    return g


def evidence(g):
    """The facts the pack carries beside the call: the coal-measure bores rising before July 2022, the per-bore
    model tracking the reference bores to September 2026, the cone at the mine's coal-measure bores."""
    obs, cl = g["obs"], g["cl"]
    out = {}
    for k in g["LH"]:
        if obs[k]["unit"] != "coal":
            continue
        u, v = A.monthly(obs[k])
        t = np.array([A.month_mid_day(x) for x in u]) / 365.25
        sel = t >= M.dnum(dt.date(2021, 1, 1)) / 365.25
        out.setdefault("rise_2021_22", {})[k] = float(np.polyfit(t[sel], v[sel], 1)[0])
    track = {}
    for k in g["REF"]:
        days, lev = A.series(obs[k], "logger")
        pre = days <= M.dnum(A.CAL_END)
        model, info = M.fit_gamma_continuous(cl, "daily", days[pre], lev[pre])
        post = (days > M.dnum(A.CAL_END)) & (days <= M.dnum(A.SEP[1]))
        mi = np.array([M.month_index(M.D0 + dt.timedelta(days=int(x))) for x in days[post]])
        res = lev[post] - model[days[post]]
        u, inv = np.unique(mi, return_inverse=True)
        monthly_res = np.bincount(inv, res) / np.bincount(inv)
        track[k] = float(np.abs(monthly_res).max())
    out["ref_tracking_max_abs"] = track
    cone = {}
    for k in g["MINE"]:
        if obs[k]["unit"] != "coal":
            continue
        days, lev = A.series(obs[k], "logger")
        before = float(lev[(days >= M.dnum(dt.date(2022, 4, 1))) & (days <= M.dnum(dt.date(2022, 6, 30)))].mean())
        cone[k] = before - A.assessment_level(obs[k])
    out["mine_coal_decline"] = cone
    return out
