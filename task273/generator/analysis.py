"""Every rung, the golden and the ask figures, computed from the files under target/ alone."""
import csv
import math
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

MONTHS = [12, 1, 2, 3]
MONTH_NAME = {12: "December", 1: "January", 2: "February", 3: "March"}
DROUGHT = {12: (2019, 12), 1: (2020, 1), 2: (2020, 2), 3: (2020, 3)}
EXISTING = ["PB%d" % k for k in range(1, 9)]
ALL = EXISTING + ["PB9"]


def _preamble_csv(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    k = 0
    while lines[k].strip() and not lines[k].startswith(("Date,", "MeterID,", "date_local,")):
        k += 1
    while not lines[k].strip():
        k += 1
    return list(csv.reader(lines[k:]))


class Pack:
    def __init__(self, target):
        self.t = target
        f = {n: os.path.join(target, n) for n in os.listdir(target)}
        self.f = f
        self._register()
        self._daily()
        self._mb1()
        self._test()
        self._plan()

    def path(self, prefix):
        return [v for k, v in self.f.items() if k.startswith(prefix)][0]

    def _register(self):
        wb = load_workbook(self.path("kaitanga_bore_register"), data_only=True)
        ws = wb["Bores"]
        rows = list(ws.iter_rows(values_only=True))
        h = rows[0]
        reg = pd.DataFrame(rows[1:], columns=h).set_index("Bore")
        self.reg = reg
        self.mp_rl = (reg["Ground RL (m, Moturiki 1953)"] + reg["MP above ground (m)"]).astype(float)
        self.mol = reg["Minimum operating level (m bmp)"].astype(float)
        self.xy = reg[["Easting (NZTM2000)", "Northing (NZTM2000)"]].astype(float)
        pumps = pd.DataFrame(list(wb["Pumps"].iter_rows(values_only=True))[1:],
                             columns=list(wb["Pumps"].iter_rows(values_only=True))[0]).set_index("Bore")
        self.kw = pumps["Motor (kW)"].astype(float)

    def _daily(self):
        d = pd.read_csv(self.path("kaitanga_bores_daily"), dtype={"pwl_mbmp": float})
        d = d.drop_duplicates()
        d["bore"] = d["tag"].str.replace("KTG-BH0", "PB", regex=False).str.replace("KTG-BH", "PB", regex=False)
        d["date"] = pd.to_datetime(d["date_local"])
        d["q"] = d["take_m3"] / 1000.0
        self.daily = d
        self.Q = d.pivot(index="date", columns="bore", values="q")
        self.L = d.pivot(index="date", columns="bore", values="pwl_mbmp")
        self.H = d.pivot(index="date", columns="bore", values="pump_run_h")

    def _mb1(self):
        rows = _preamble_csv(self.path("MRC_MB1"))
        m = pd.DataFrame(rows[1:], columns=rows[0])
        m["date"] = pd.to_datetime(m["Date"], format="%d/%m/%Y")
        self.mb = m.set_index("date")["Value"].astype(float)

    def _test(self):
        rows = _preamble_csv(self.path("PB9_logger"))
        t = pd.DataFrame(rows[1:], columns=rows[0])
        t["utc"] = pd.to_datetime(t["Date"] + " " + t["Time"])
        t["local"] = t["utc"] + pd.Timedelta(hours=13)
        t["level"] = t["Level_m_bmp"].astype(float)
        t["q"] = t["Q_L_s"].astype(float)
        self.test = t
        # PB9's take on each local day of the test, ML
        self.q9 = t.set_index("local")["q"].resample("D").sum() * 3600 / 1e6

    def _plan(self):
        wb = load_workbook(self.path("kaitanga_summer_bore_plan"), data_only=True)
        ws = wb.active
        plan = {m: {} for m in MONTHS}
        for r in ws.iter_rows(values_only=True):
            if r and r[0] in ALL:
                for k, m in enumerate(MONTHS):
                    plan[m][r[0]] = float(r[k + 1])
        self.plan = plan

    # ------------------------------------------------------------ shared pieces
    def drought_min(self, m):
        y, mm = DROUGHT[m]
        s = self.mb[(self.mb.index.year == y) & (self.mb.index.month == mm)]
        return float(s.min())

    def frame(self, with9=True):
        """Days with every existing bore's take and level, PB9's test take where it ran, MB1 that day."""
        Q = self.Q[EXISTING].copy()
        Q["PB9"] = 0.0
        if with9:
            for d, v in self.q9.items():
                if d in Q.index:
                    Q.at[d, "PB9"] = v
        df = Q.join(self.L[EXISTING].add_prefix("L_"), how="inner").join(self.mb.rename("mb"), how="inner")
        return df.dropna()

    def c9_static(self):
        """PB9's own drawdown per ML/d and its static level, from the constant-rate stage of its test."""
        t = self.test
        cr = t[t["Stage"] == "constant rate"]
        pre = t[t["Stage"] == "static"]
        static = float(pre["level"].iloc[:2].mean())
        late = cr[cr["local"] >= cr["local"].max() - pd.Timedelta(hours=24)]
        q = float(late["q"].mean()) * 86400 / 1e6
        return (float(late["level"].mean()) - static) / q, static, pre["local"].iloc[0].normalize()


def fit_full(P, with9=True, window=None):
    """Each existing bore's level (m RL, Moturiki) less MB1 on every bore's take, PB9's test take included."""
    df = P.frame(with9)
    if window:
        df = df[(df.index >= window[0]) & (df.index <= window[1])]
    cols = EXISTING + (["PB9"] if with9 else [])
    X = np.column_stack([np.ones(len(df))] + [df[c].values for c in cols])
    coef = {}
    for i in EXISTING:
        y = (P.mp_rl[i] - df["L_" + i].values) - df["mb"].values
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        coef[i] = dict(zip(["const"] + cols, b))
    return coef


def fit_own(P, window=None):
    """The default drought curve: each bore's level less MB1 on its own take alone."""
    df = P.frame(False)
    if window:
        df = df[(df.index >= window[0]) & (df.index <= window[1])]
    coef = {}
    for i in EXISTING:
        X = np.column_stack([np.ones(len(df)), df[i].values])
        y = (P.mp_rl[i] - df["L_" + i].values) - df["mb"].values
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        coef[i] = {"const": b[0], i: b[1]}
    return coef


def distance_model(P, coef):
    """Interference against log distance, fitted on the existing pairs; returns PB9's predicted coefficients."""
    xs, ys = [], []
    for i in EXISTING:
        for j in EXISTING:
            if i < j:
                r = math.hypot(*(P.xy.loc[i].values - P.xy.loc[j].values))
                v = -(coef[i][j] + coef[j][i]) / 2.0
                xs.append(math.log(r))
                ys.append(v)
    A = np.column_stack([np.ones(len(xs)), xs])
    b, *_ = np.linalg.lstsq(A, np.array(ys), rcond=None)
    out = {}
    for i in EXISTING:
        r = math.hypot(*(P.xy.loc[i].values - P.xy.loc["PB9"].values))
        out[i] = max(0.0, b[0] + b[1] * math.log(r))
    return out, b


def pb9_level(P, m, a9, plan, reciprocity=True):
    """PB9's lowest level in month m (m bmp): its test static carried to the drought level, less its own drawdown
    at the planned take and, by reciprocity, its neighbours' planned takes beyond those on the static day."""
    c9, static, day = P.c9_static()
    mb_day = float(P.mb.get(day, P.mb[P.mb.index <= day].iloc[-1]))
    nb = 0.0
    if reciprocity:
        q_day = P.Q.loc[day, EXISTING]
        nb = sum(a9.get(j, 0.0) * (plan[j] - q_day[j]) for j in EXISTING)
    rl_static = P.mp_rl["PB9"] - static
    rl = rl_static + (P.drought_min(m) - mb_day) - c9 * plan["PB9"] - nb
    return P.mp_rl["PB9"] - rl


def forecast(P, coef, a9_on, plan_override=None, reciprocity=True):
    """Lowest pumping water level (m bmp) per bore and month under the plan in the design drought.
    coef: per existing bore {const, own and neighbour coefficients}; a9_on: PB9's drawdown on each existing bore
    per ML/d (negative coefficients in the regression's sign), or None to leave PB9's draw out."""
    plan = plan_override or P.plan
    out = {}
    for m in MONTHS:
        q = plan[m]
        mb = P.drought_min(m)
        for i in EXISTING:
            c = coef[i]
            rl = mb + c["const"] + sum(c.get(j, 0.0) * q[j] for j in EXISTING)
            if a9_on is not None:
                rl -= a9_on[i] * q["PB9"]
            out[(i, m)] = P.mp_rl[i] - rl
        a9 = a9_on or {}
        out[("PB9", m)] = pb9_level(P, m, a9, q, reciprocity)
    return out


def verdict(P, lev):
    fails = [(i, m) for (i, m), v in lev.items() if v > P.mol[i]]
    return sorted(fails, key=lambda x: (ALL.index(x[0]), MONTHS.index(x[1])))


def golden(P):
    coef = fit_full(P, True)
    a9 = {i: -coef[i]["PB9"] for i in EXISTING}
    lev = forecast(P, coef, a9)
    return lev, coef, a9


def rung0(P):
    coef = fit_own(P)
    return forecast(P, coef, None)


def rung1(P):
    """The interference correction on the existing bores, with PB9 still left out."""
    coef = fit_full(P, False)
    return forecast(P, coef, None), coef


def rung2(P):
    """PB9's interference taken from distance through the existing pairs' log-distance relation."""
    coef = fit_full(P, False)
    a9, b = distance_model(P, coef)
    return forecast(P, coef, a9), a9, b


# ---------------------------------------------------------------- the permit meters
QUARTERS = [("2025-07-01", "2025-09-30"), ("2025-10-01", "2025-12-31"), ("2026-01-01", "2026-03-31"),
            ("2026-04-01", "2026-06-30")]
SCHEDULE = {"WM-30455": "PB1", "WM-30456": "PB2", "WM-31690": "PB3", "WM-31702": "PB4", "WM-33119": "PB5",
            "WM-33120": "PB6", "WM-35873": "PB7", "WM-35874": "PB8"}


def nz_dst(nzst):
    y = nzst.year
    d = pd.Timestamp(y, 9, 30)
    start = d - pd.Timedelta(days=(d.weekday() + 1) % 7) + pd.Timedelta(hours=2)
    d = pd.Timestamp(y, 4, 1)
    end = d + pd.Timedelta(days=(6 - d.weekday()) % 7) + pd.Timedelta(hours=2)
    return nzst >= start or nzst < end


def nzst_to_local(nzst):
    return pd.DatetimeIndex([x + pd.Timedelta(hours=1) if nz_dst(x) else x for x in nzst])


def utc_to_local(utc):
    return nzst_to_local(pd.DatetimeIndex(utc) + pd.Timedelta(hours=12))


def meter_increments(P, roll=True):
    """Each council meter's volume in each quarter-hour, placed at the quarter-hour's local start."""
    rows = _preamble_csv(P.path("MRC_permit_meter"))
    t = pd.DataFrame(rows[1:], columns=rows[0])
    t["nzst"] = pd.to_datetime(t["ReadingTime"])
    t["v"] = t["Totaliser_m3"].astype(float)
    out = []
    for mid, g in t.groupby("MeterID"):
        g = g.sort_values("nzst")
        dv = g["v"].diff()
        if roll:
            dv = dv.where(dv >= -1000, dv + 1_000_000.0)
        else:
            dv = dv.where(dv >= 0, 0.0)
        loc = nzst_to_local(g["nzst"]) - pd.Timedelta(minutes=15)
        out.append(pd.DataFrame({"meter": mid, "local": loc, "v": dv.fillna(0.0).values}))
    return pd.concat(out)


def meter_map(P, inc, match=True):
    """Which bore each meter reads. The golden matches every meter to the production bore whose SCADA daily take it
    tracks over the meter's own days; the permit's Schedule 1 is the literal list."""
    if not match:
        return dict(SCHEDULE)
    daily = inc.assign(date=inc["local"].dt.normalize()).groupby(["meter", "date"])["v"].sum() / 1000.0
    out = {}
    for mid in daily.index.get_level_values(0).unique():
        s = daily.loc[mid]
        s = s.iloc[1:-1]
        best = None
        for b in EXISTING:
            q = P.Q[b].reindex(s.index)
            ok = q.notna()
            r = float(np.corrcoef(s[ok], q[ok])[0, 1])
            if best is None or r > best[0]:
                best = (r, b)
        out[mid] = best[1]
    return out


def ask_meters(P, match=True, roll=True):
    inc = meter_increments(P, roll)
    mp = meter_map(P, inc, match)
    inc = inc[inc["meter"].isin(mp)]
    inc = inc.assign(bore=inc["meter"].map(mp))
    out = {}
    for qi, (a, b) in enumerate(QUARTERS):
        a, b = pd.Timestamp(a), pd.Timestamp(b) + pd.Timedelta(days=1)
        s = inc[(inc["local"] >= a) & (inc["local"] < b)].groupby("bore")["v"].sum() / 1000.0
        for k in EXISTING:
            out[(k, qi + 1)] = float(s.get(k, 0.0))
    return out


# ---------------------------------------------------------------- Ask A: pump electricity per ML by quarter
def ask_energy(P, multiplier=True, split="hours_kw", meters=None):
    e = pd.read_csv(P.path("pump_icp_interval"))
    reg = pd.read_csv(P.path("kaitanga_icp_meter_register"))
    mult = dict(zip(reg["meter_serial"], reg["multiplier"]))
    e["local"] = utc_to_local(pd.to_datetime(e["interval_start_utc"].str.replace("Z", "")))
    e["kwh"] = e["reg_advance"] * (e["meter_serial"].map(mult) if multiplier else 1.0)
    e["date"] = e["local"].dt.normalize()
    icp_bore = {}
    for _, r in reg.iterrows():
        txt = r["installation"]
        if "Bore 5 and Bore 6" in txt:
            icp_bore[r["icp"]] = ["PB5", "PB6"]
        elif "Bore 7 and Bore 8" in txt:
            icp_bore[r["icp"]] = ["PB7", "PB8"]
        elif txt.startswith("PB"):
            icp_bore[r["icp"]] = [txt.split()[0]]
    daily = e.groupby(["icp", "date"])["kwh"].sum()
    ml = meters if meters is not None else ask_meters(P)
    out = {}
    for qi, (a, b) in enumerate(QUARTERS):
        a, b = pd.Timestamp(a), pd.Timestamp(b)
        for icp, bores in icp_bore.items():
            kwh = daily.loc[icp]
            kwh = kwh[(kwh.index >= a) & (kwh.index <= b)]
            if len(bores) == 1:
                shares = {bores[0]: float(kwh.sum())}
            else:
                H = P.H.reindex(kwh.index)[bores].fillna(0.0)
                if split == "hours_kw":
                    wgt = H * P.kw[bores]
                elif split == "hours":
                    wgt = H
                else:
                    wgt = P.Q.reindex(kwh.index)[bores].fillna(0.0)
                tot = wgt.sum(axis=1).replace(0, np.nan)
                shares = {k: float((kwh * wgt[k] / tot).fillna(0.0).sum()) for k in bores}
            for k, v in shares.items():
                out[(k, qi + 1)] = v / ml[(k, qi + 1)] if ml[(k, qi + 1)] > 0 else float("nan")
    return out
