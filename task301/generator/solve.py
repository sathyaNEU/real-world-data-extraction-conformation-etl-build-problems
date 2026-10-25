"""Every owed figure from the pack alone: the call (the golden route and the ladder of easier routes), the standing family
for Hallam Down's deposit, and the two asks with their wrong paths.

    python3 solve.py <pack dir>
"""
import datetime as dt
import os
import sys
import zoneinfo

import numpy as np
import pandas as pd

UK = zoneinfo.ZoneInfo("Europe/London")
CANDS = ["Hallam Down", "Kingsley Fields", "Larkhill Common", "Marston Vale"]
ENERGISED = {"Hallam Down": dt.date(2027, 9, 30), "Kingsley Fields": dt.date(2027, 8, 31),
             "Larkhill Common": dt.date(2027, 10, 29), "Marston Vale": dt.date(2027, 7, 30)}
LO, HI, CAP, WASH_LO, WASH_HI = 4.0, 10.0, 0.25, 0.55, 0.08


class Pack:
    def __init__(self, p):
        self.p = p
        rd = lambda f, **k: pd.read_csv(os.path.join(p, f), **k)
        self.reg = rd("site_register.csv")
        self.w = rd("site_weather_daily_2016-2025.csv", parse_dates=["date"])
        self.ex = rd("fleet_daily_export_2022-2025.csv", parse_dates=["date"])
        self.sc = pd.read_parquet(os.path.join(p, "inverter_daily_energy_2022-2025.parquet"))
        self.sc["date"] = pd.to_datetime(self.sc.date)
        self.lay = rd("array_layout_blocks.csv")
        self.env = rd("site_environs_2km.csv")
        self.om = rd("om_event_log_2022-2025.csv", parse_dates=["date"], keep_default_na=False)
        self.dc = self.reg.set_index("site").dc_capacity_mwp
        self.comm = pd.to_datetime(self.reg.set_index("site").commissioned)


# ---------------------------------------------------------------- the call
def site_pr(K, site, years=(2022, 2025)):
    x = K.ex[K.ex.site == site].merge(K.w[K.w.site == site], on=["date", "site"])
    x = x[(x.date.dt.year >= years[0]) & (x.date.dt.year <= years[1])]
    return x.export_mwh.sum() / (K.dc[site] * x.poa_irradiation_kwh_m2.sum())


def mean_age(K, site, d0=dt.date(2022, 1, 1), d1=dt.date(2025, 12, 31)):
    days = pd.date_range(max(pd.Timestamp(d0), K.comm[site]), d1, freq="D")
    return float(((days - K.comm[site]).days / 365.25).values.mean())


def bifacial_degradation(K):
    """the four bifacial farms' annual ratio of export to irradiation, log-linear in age with a level for each farm"""
    rows = []
    for s in ["Ivy Cross", "Furzedown", "Jessop's Farm", "Knowle Park"]:
        for y in range(2022, 2026):
            if (K.ex[K.ex.site == s].date.dt.year == y).sum() < 300:
                continue
            a = mean_age(K, s, dt.date(y, 1, 1), dt.date(y, 12, 31))
            rows.append((s, a, np.log(site_pr(K, s, (y, y)))))
    df = pd.DataFrame(rows, columns=["s", "age", "lpr"])
    X = pd.get_dummies(df.s).astype(float)
    X["age"] = df.age
    b = np.linalg.lstsq(X.values, df.lpr.values, rcond=None)[0]
    return float(1 - np.exp(b[-1]))


def avg_year_poa(K, site):
    w = K.w[K.w.site == site]
    return w.poa_irradiation_kwh_m2.sum() / 10.0


def age_2028(site):
    return ((dt.date(2028, 7, 2) - ENERGISED[site]).days) / 365.25


def clean_export(K, site, pr=None, deg=None):
    pr = site_pr(K, "Knowle Park") if pr is None else pr
    deg = bifacial_degradation(K) if deg is None else deg
    f = (1 - deg) ** (age_2028(site) - mean_age(K, "Knowle Park"))
    return 11.0 * avg_year_poa(K, site) * pr * f


def run_deposit(rain, rate, lo=LO, hi=HI, cap=CAP):
    """the deposit each day for one daily step or an array of them (one column a step)"""
    rate = np.atleast_1d(np.asarray(rate, dtype=float))
    o = np.zeros((len(rain), len(rate)))
    v = np.zeros(len(rate))
    for i, r in enumerate(rain):
        if r >= hi:
            v = v * WASH_HI
        elif r >= lo:
            v = v * WASH_LO
        else:
            v = np.minimum(v + rate, cap)
        o[i] = v
    return o[:, 0] if o.shape[1] == 1 else o


def run_full_wash(rain, rate, thr, cap=CAP):
    """the textbook alternative: the deposit builds by the same daily step and any rain of thr mm or more removes all of it"""
    rate = np.atleast_1d(np.asarray(rate, dtype=float))
    o = np.zeros((len(rain), len(rate)))
    v = np.zeros(len(rate))
    for i, r in enumerate(rain):
        v = np.zeros(len(rate)) if r >= thr else np.minimum(v + rate, cap)
        o[i] = v
    return o[:, 0] if o.shape[1] == 1 else o


def fit_full_wash(K, s, thr, near=320):
    wx = K.w[K.w.site == "Wexcombe"].set_index("date").sort_index()
    rain = wx.rainfall_mm.values
    out, tot = {}, 0.0
    grid = RATES
    dep = run_full_wash(rain, grid, thr)
    for inv, d in s[s.d < near].groupby("inverter"):
        d = d.sort_values("date")
        e, rate = _best_rate(d, dep[wx.index.get_indexer(d.date)], grid)
        out[inv] = (float(d.d.iloc[0]), rate)
        tot += e * len(d)
    return out, tot


def hallam_loss_full_wash(K, f, thr):
    L = block_distances(K, "Hallam Down")
    h = K.w[K.w.site == "Hallam Down"].sort_values("date")
    poa, rain = h.poa_irradiation_kwh_m2.values, h.rainfall_mm.values
    dep = run_full_wash(rain, [f(d) for d in L.d], thr)
    return float(np.mean((poa[:, None] * dep).sum(axis=0) / poa.sum()))


def block_distances(K, site):
    r = K.env[(K.env.site == site) & (K.env.feature == "Poultry unit")].sort_values("distance_m").iloc[0]
    c = K.reg.set_index("site").loc[site]
    b = np.radians(r.bearing_from_site_deg)
    sx = c.centroid_easting + r.distance_m * np.sin(b)
    sy = c.centroid_northing + r.distance_m * np.cos(b)
    L = K.lay[K.lay.site == site].copy()
    L["d"] = np.hypot(L.block_easting - sx, L.block_northing - sy)
    return L


def wexcombe_blocks(K, ref="far"):
    L = block_distances(K, "Wexcombe")
    s = K.sc[K.sc.site == "Wexcombe"].merge(L[["inverter", "dc_mwp", "d"]], on="inverter")
    ev = K.om[K.om.site == "Wexcombe"]
    drop = set(zip(ev.date, ev.inverter.replace("", "ALL")))
    s = s[[(d, i) not in drop and (d, "ALL") not in drop for d, i in zip(s.date, s.inverter)]].copy()
    s["y"] = s.ac_energy_mwh / s.dc_mwp
    if ref == "far":
        base = s[s.d > 450].groupby("date").y.median()
    else:
        base = s.groupby("date").y.median()
    s["rel"] = s.y / s.date.map(base)
    return s


RATES = np.arange(0.0005, 0.0301, 0.0005)


def _best_rate(d, sl, grid):
    """the daily step whose deposit best explains a block's output against the reference, with a level for the block"""
    rel = d.rel.values[:, None]
    k = np.median(rel / (1 - sl), axis=0)
    e = np.mean((rel - k * (1 - sl)) ** 2, axis=0)
    j = int(np.argmin(e))
    return float(e[j]), float(grid[j])


def fit_rates(K, s, lo=LO, hi=HI, near=320, sse=False):
    """each near block's daily deposit, fitted to its daily output against the reference blocks"""
    wx = K.w[K.w.site == "Wexcombe"].set_index("date").sort_index()
    rain = wx.rainfall_mm.values
    out = {}
    tot = 0.0
    grid = RATES
    dep = run_deposit(rain, grid, lo, hi)
    for inv, d in s[s.d < near].groupby("inverter"):
        d = d.sort_values("date")
        e, rate = _best_rate(d, dep[wx.index.get_indexer(d.date)], grid)
        out[inv] = (float(d.d.iloc[0]), rate)
        tot += e * len(d)
    return (out, tot) if sse else out


WASH_GRID = [(lo, hi) for lo in (2, 3, 4, 5, 6) for hi in (6, 8, 10, 12, 15, 20) if hi > lo]


def fit_wash(K, s):
    """the rain that washes the deposit, chosen by the near blocks' own fit"""
    fits = sorted((fit_rates(K, s, lo, hi, sse=True)[1], lo, hi) for lo, hi in WASH_GRID)
    return fits


def rate_fn(per, form):
    dd = np.array([v[0] for v in per.values()])
    rr = np.array([v[1] for v in per.values()])
    if form == "exp":
        b, a = np.polyfit(dd, np.log(rr), 1)
        return lambda d: float(np.exp(a + b * d))
    if form == "power":
        b, a = np.polyfit(np.log(dd), np.log(rr), 1)
        return lambda d: float(np.exp(a + b * np.log(d)))
    o = np.argsort(dd)
    return lambda d: float(np.interp(d, dd[o], rr[o]))


def hallam_loss(K, f, lo=LO, hi=HI):
    L = block_distances(K, "Hallam Down")
    h = K.w[K.w.site == "Hallam Down"].sort_values("date")
    poa, rain = h.poa_irradiation_kwh_m2.values, h.rainfall_mm.values
    dep = run_deposit(rain, [f(d) for d in L.d], lo, hi)
    return float(np.mean((poa[:, None] * dep).sum(axis=0) / poa.sum()))


def family(K):
    """the deposit family: two references, two wash models (partial washes at two thresholds, the best fits and
    neighbours; one full wash at a threshold, the best fits), three decay forms with distance"""
    out = []
    for ref in ("far", "farm"):
        s = wexcombe_blocks(K, ref)
        for sse, lo, hi in fit_wash(K, s)[:4]:
            per = fit_rates(K, s, lo, hi)
            for form in ("exp", "power", "interp"):
                out.append((ref, "partial %d/%d" % (lo, hi), form, sse, hallam_loss(K, rate_fn(per, form), lo, hi)))
        fw = sorted((fit_full_wash(K, s, t)[1], t) for t in (2, 3, 4, 5, 6, 8, 10))
        for sse, t in fw[:3]:
            per, _ = fit_full_wash(K, s, t)
            for form in ("exp", "power", "interp"):
                out.append((ref, "full %d" % t, form, sse, hallam_loss_full_wash(K, rate_fn(per, form), t)))
    return out


def call(K):
    pr = site_pr(K, "Knowle Park")
    deg = bifacial_degradation(K)
    clean = {c: clean_export(K, c, pr, deg) for c in CANDS}
    s = wexcombe_blocks(K, "far")
    wash = fit_wash(K, s)
    lo, hi = wash[0][1], wash[0][2]
    per = fit_rates(K, s, lo, hi)
    loss = hallam_loss(K, rate_fn(per, "exp"), lo, hi)
    gold = dict(clean)
    gold["Hallam Down"] = clean["Hallam Down"] * (1 - loss)
    # the ladder of easier routes
    peers = np.mean([site_pr(K, x) for x in ["Ashcombe", "Bramble Hill", "Coldharbour"]])
    farm_ratio = site_pr(K, "Wexcombe") / peers
    near = s[s.d < 320].groupby("inverter").agg(rel=("rel", "mean"), d=("d", "first")).sort_values("d")
    L = block_distances(K, "Hallam Down")
    flat_blocks = float(np.mean([max(0.0, 1 - np.interp(d, near.d.values, near.rel.values)) for d in L.d]))
    return dict(pr_kp=pr, deg=deg, clean=clean, loss=loss, gold=gold, rates=per, farm_ratio=farm_ratio, wash=wash,
                flat_blocks=flat_blocks, lead=avg_year_poa(K, "Hallam Down") / avg_year_poa(K, "Kingsley Fields") - 1,
                near=near)


# ---------------------------------------------------------------- ask A
def ask_a(K):
    met = pd.read_csv(os.path.join(K.p, "met_station_daily_2025.csv"), parse_dates=["date"])
    reg = pd.read_csv(os.path.join(K.p, "pyranometer_register.csv"), parse_dates=["installed"]).set_index("site")
    cert = pd.read_excel(os.path.join(K.p, "pyranometer_calibration_certificates.xlsx"), sheet_name="Certificates")
    cert["calibration_date"] = pd.to_datetime(cert.calibration_date)
    cs = cert.sort_values("calibration_date")
    w = K.w[K.w.date.dt.year == 2025]
    x = met.merge(w[["date", "site", "poa_irradiation_kwh_m2"]], on=["date", "site"])

    def asof(serial, d):
        c = cs[(cs.serial == serial) & (cs.calibration_date <= d)]
        return float(c.sensitivity_uv_per_w_m2.iloc[-1])
    latest = cs.groupby("serial").sensitivity_uv_per_w_m2.last()
    out = {}
    for f, d in x.groupby("site", sort=False):
        r = reg.loc[f]
        # the sensor that came down from this mast in 2025, by the laboratory's record of where it was sent from
        down = cs[(cs.sent_from == "%s MET1" % f) & (cs.calibration_date >= r.installed)].serial.iloc[0]
        in_mast = np.where(d.date < r.installed, down, r.sensor_serial)
        s_gold = np.array([asof(a, b) for a, b in zip(in_mast, d.date)])
        s_label = np.array([asof(a, b) for a, b in zip(d.sensor_serial, d.date)])
        sat = d.poa_irradiation_kwh_m2.sum()
        allsat = w[w.site == f].poa_irradiation_kwh_m2.sum()
        out[f] = dict(gold=(d.poa_signal_mvh / s_gold).sum() / sat,
                      register=(d.poa_signal_mvh / r.sensitivity_uv_per_w_m2).sum() / sat,
                      label_asof=(d.poa_signal_mvh / s_label).sum() / sat,
                      label_latest=(d.poa_signal_mvh / d.sensor_serial.map(latest)).sum() / sat,
                      all_days=(d.poa_signal_mvh / s_gold).sum() / allsat,
                      gold_latest=(d.poa_signal_mvh / pd.Series(in_mast).map(latest).values).sum() / sat,
                      days=len(d), down=down, label=d.sensor_serial.iloc[0])
    return out


# ---------------------------------------------------------------- ask B
def ask_b(K):
    to_utc = lambda t: pd.Timestamp(t).tz_localize(UK).tz_convert("UTC").tz_localize(None)
    al = pd.read_csv(os.path.join(K.p, "scada_alarm_log_2025.csv"), parse_dates=["raised_utc", "cleared_utc"])
    wo = pd.read_csv(os.path.join(K.p, "cmms_work_orders_2025.csv"), parse_dates=["raised", "attended", "completed"])
    gf = pd.read_csv(os.path.join(K.p, "van_tracker_site_visits_2025.csv"), parse_dates=["entered", "left"])
    vans = pd.read_csv(os.path.join(K.p, "technician_vans_2025.csv"), parse_dates=["from", "to"])
    gf["entered_utc"] = [to_utc(t) for t in gf.entered]
    wo = wo[wo.alarm_ref.notna()].copy()
    wo["alarm_ref"] = wo.alarm_ref.astype(int)
    j = wo.merge(al, left_on="alarm_ref", right_on="alarm_id", suffixes=("", "_al"))
    j["attended_utc"] = [to_utc(t) for t in j.attended]
    j["wo_raised_utc"] = [to_utc(t) for t in j.raised]
    j["raised_local"] = [pd.Timestamp(t).tz_localize("UTC").tz_convert(UK).tz_localize(None) for t in j.raised_utc]

    def van_on(t, d):
        v = vans[(vans.technician == t) & (vans["from"] <= d) & (vans["to"].isna() | (vans["to"] >= d))]
        return v.sort_values("from").vehicle.iloc[-1]

    arr, arr_any, arr_raw, arr_local = [], [], [], []
    for r in j.itertuples():
        v = van_on(r.assigned_to, pd.Timestamp(r.raised_local.date()))
        g = gf[(gf.vehicle == v) & (gf.site == r.site) & (gf.entered_utc >= r.raised_utc)]
        arr.append(g.entered_utc.min())
        arr_local.append(g.sort_values("entered_utc").entered.iloc[0])
        arr_any.append(gf[(gf.site == r.site) & (gf.entered_utc >= r.raised_utc)].entered_utc.min())
        arr_raw.append(gf[(gf.vehicle == v) & (gf.site == r.site) & (gf.entered >= r.raised_utc)].entered.min())
    j["arrived_utc"] = arr
    hrs = lambda a, b: (a - b).dt.total_seconds() / 3600
    j["h_gold"] = hrs(j.arrived_utc, j.raised_utc)
    j["h_wall"] = hrs(pd.Series(arr_local, index=j.index), j.raised_local)
    j["h_attended"] = hrs(j.attended_utc, j.raised_utc)
    j["h_cmms"] = hrs(j.attended, j.raised)
    j["h_mixed"] = hrs(j.attended, j.raised_utc)
    j["h_tracker_raw"] = hrs(pd.Series(arr_raw, index=j.index), j.raised_utc)
    j["h_from_wo"] = hrs(j.arrived_utc, j.wo_raised_utc)
    j["h_any_van"] = hrs(pd.Series(arr_any, index=j.index), j.raised_utc)
    j["possible"] = j.attended_utc <= j.cleared_utc
    out = {}
    for f, d in j.groupby("site", sort=False):
        out[f] = dict(gold=d.h_gold.mean(), wall=d.h_wall.mean(), attended=d.h_attended.mean(), cmms=d.h_cmms.mean(),
                      mixed=d.h_mixed.mean(),
                      tracker_raw=d.h_tracker_raw.mean(), from_wo=d.h_from_wo.mean(), any_van=d.h_any_van.mean(),
                      possible_only=d[d.possible].h_attended.mean(), n=len(d), impossible=int((~d.possible).sum()))
    return out


if __name__ == "__main__":
    K = Pack(sys.argv[1])
    c = call(K)
    print("PR Knowle Park %.4f, degradation %.4f, Hallam lead %.4f, loss %.4f, farm ratio %.4f, flat blocks %.4f"
          % (c["pr_kp"], c["deg"], c["lead"], c["loss"], c["farm_ratio"], c["flat_blocks"]))
    print("clean", {k: round(v) for k, v in c["clean"].items()})
    print("gold ", {k: round(v) for k, v in c["gold"].items()})
    a = ask_a(K)
    for f, v in a.items():
        print("A %-16s gold %.5f register %.4f label-asof %.4f label-latest %.4f all-days %.4f gold-latest %.4f"
              % (f, v["gold"], v["register"], v["label_asof"], v["label_latest"], v["all_days"], v["gold_latest"]))
    b = ask_b(K)
    for f, v in b.items():
        print("B %-16s n %2d gold %6.3f att %5.2f cmms %5.2f mixed %5.2f raw %5.2f fromwo %5.2f anyvan %5.2f poss %5.2f (imp %d)"
              % (f, v["n"], v["gold"], v["attended"], v["cmms"], v["mixed"], v["tracker_raw"], v["from_wo"], v["any_van"],
                 v["possible_only"], v["impossible"]))
