"""Independent verifier: unzip target.zip into a scratch folder and recompute every graded figure from the bundle with
code that shares nothing with solve.py, then compare with figures.json and the write-up's answers.

    python3 task301/generator/verify.py [target.zip]
"""
import datetime as dt
import json
import os
import re
import sys
import tempfile
import zipfile
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LONDON = ZoneInfo("Europe/London")
CANDS = ["Hallam Down", "Kingsley Fields", "Larkhill Common", "Marston Vale"]


def energised(T):
    from docx import Document
    d = Document(os.path.join(T, "build_decision_note_2027.docx"))
    out = {}
    for row in d.tables[0].rows[1:]:
        cells = [x.text for x in row.cells]
        out[cells[0]] = dt.datetime.strptime(cells[3], "%d %B %Y").date()
    return out


def wash_series(rain, steps, lo, hi, keep_lo=0.55, keep_hi=0.08, cap=0.25):
    steps = np.asarray(steps, float)
    v = np.zeros(len(steps))
    out = np.empty((len(rain), len(steps)))
    for i, r in enumerate(rain):
        v = v * keep_hi if r >= hi else (v * keep_lo if r >= lo else np.minimum(v + steps, cap))
        out[i] = v
    return out


def the_call(T):
    reg = pd.read_csv(os.path.join(T, "site_register.csv")).set_index("site")
    wx = pd.read_csv(os.path.join(T, "site_weather_daily_2016-2025.csv"), parse_dates=["date"])
    ex = pd.read_csv(os.path.join(T, "fleet_daily_export_2022-2025.csv"), parse_dates=["date"])
    sc = pd.read_parquet(os.path.join(T, "inverter_daily_energy_2022-2025.parquet"))
    sc["date"] = pd.to_datetime(sc["date"])
    lay = pd.read_csv(os.path.join(T, "array_layout_blocks.csv"))
    env = pd.read_csv(os.path.join(T, "site_environs_2km.csv"))
    om = pd.read_csv(os.path.join(T, "om_event_log_2022-2025.csv"), parse_dates=["date"], keep_default_na=False)
    comm = pd.to_datetime(reg.commissioned)
    m = ex.merge(wx, on=["date", "site"])

    def ratio(s, y0=2022, y1=2025):
        q = m[(m.site == s) & m.date.dt.year.between(y0, y1)]
        return q.export_mwh.sum() / (reg.loc[s, "dc_capacity_mwp"] * q.poa_irradiation_kwh_m2.sum())

    def mean_age(s, a=dt.date(2022, 1, 1), b=dt.date(2025, 12, 31)):
        idx = pd.date_range(max(pd.Timestamp(a), comm[s]), b)
        return float(np.mean((idx - comm[s]).days) / 365.25)
    kp = ratio("Knowle Park")
    rows = []
    for s in reg.index[(reg.status == "operating") & reg.module.str.contains("bifacial")]:
        for y in range(2022, 2026):
            if (ex[(ex.site == s)].date.dt.year == y).sum() >= 300:
                rows.append((s, mean_age(s, dt.date(y, 1, 1), dt.date(y, 12, 31)), np.log(ratio(s, y, y))))
    d = pd.DataFrame(rows, columns=["s", "a", "l"])
    X = np.column_stack([pd.get_dummies(d.s).astype(float).values, d.a.values])
    deg = 1 - np.exp(np.linalg.lstsq(X, d.l.values, rcond=None)[0][-1])
    en = energised(T)
    out = {}
    for k in CANDS:
        age = (dt.date(2028, 7, 2) - en[k]).days / 365.25
        poa = wx[wx.site == k].poa_irradiation_kwh_m2.sum() / 10.0
        out[k] = 11.0 * poa * kp * (1 - deg) ** (age - mean_age("Knowle Park"))

    def sheds(s):
        r = env[(env.site == s) & (env.feature == "Poultry unit")].sort_values("distance_m").iloc[0]
        b = np.radians(r.bearing_from_site_deg)
        return (reg.loc[s, "centroid_easting"] + r.distance_m * np.sin(b),
                reg.loc[s, "centroid_northing"] + r.distance_m * np.cos(b))

    def dist(s):
        x0, y0 = sheds(s)
        q = lay[lay.site == s].copy()
        q["d"] = np.hypot(q.block_easting - x0, q.block_northing - y0)
        return q
    wl = dist("Wexcombe")
    w = sc[sc.site == "Wexcombe"].merge(wl[["inverter", "dc_mwp", "d"]], on="inverter")
    evw = om[om.site == "Wexcombe"]
    gone = set(zip(evw.date, evw.inverter))
    w = w[[(a, i) not in gone and (a, "") not in gone for a, i in zip(w.date, w.inverter)]].copy()
    w["y"] = w.ac_energy_mwh / w.dc_mwp
    w["rel"] = w.y / w.date.map(w[w.d > 450].groupby("date").y.median())
    rain_w = wx[wx.site == "Wexcombe"].sort_values("date")
    dates_w, rw = rain_w.date.values, rain_w.rainfall_mm.values
    grid = np.arange(0.0005, 0.0301, 0.0005)
    best = None
    for lo in (2, 3, 4, 5, 6):
        for hi in (6, 8, 10, 12, 15, 20):
            if hi <= lo:
                continue
            series = wash_series(rw, grid, lo, hi)
            tot, fit = 0.0, {}
            for inv, g in w[w.d < 320].groupby("inverter"):
                g = g.sort_values("date")
                sl = series[np.searchsorted(dates_w, g.date.values)]
                rel = g.rel.values[:, None]
                lev = np.median(rel / (1 - sl), axis=0)
                e = np.mean((rel - lev * (1 - sl)) ** 2, axis=0)
                j = int(np.argmin(e))
                fit[inv] = (g.d.iloc[0], grid[j])
                tot += e[j] * len(g)
            if best is None or tot < best[0]:
                best = (tot, lo, hi, fit)
    _, lo, hi, fit = best
    dd = np.array([v[0] for v in fit.values()])
    rr = np.array([v[1] for v in fit.values()])
    sl_, ic = np.polyfit(dd, np.log(rr), 1)
    hd = dist("Hallam Down")
    h = wx[wx.site == "Hallam Down"].sort_values("date")
    dep = wash_series(h.rainfall_mm.values, np.exp(ic + sl_ * hd.d.values), lo, hi)
    hp = h.poa_irradiation_kwh_m2.values
    loss = float(np.mean((hp[:, None] * dep).sum(axis=0) / hp.sum()))
    clean = dict(out)
    out["Hallam Down"] *= 1 - loss
    return out, clean, loss, (lo, hi), kp


def ask_a(T):
    met = pd.read_csv(os.path.join(T, "met_station_daily_2025.csv"), parse_dates=["date"])
    reg = pd.read_csv(os.path.join(T, "pyranometer_register.csv"), parse_dates=["installed"]).set_index("site")
    cert = pd.read_excel(os.path.join(T, "pyranometer_calibration_certificates.xlsx"), sheet_name=0)
    cert["calibration_date"] = pd.to_datetime(cert.calibration_date)
    wx = pd.read_csv(os.path.join(T, "site_weather_daily_2016-2025.csv"), parse_dates=["date"])
    q = met.merge(wx, on=["date", "site"])
    out = {}
    for s, g in q.groupby("site"):
        up = reg.loc[s, "sensor_serial"]
        down = cert[(cert.sent_from == s + " MET1") & (cert.calibration_date >= reg.loc[s, "installed"])].serial
        assert len(down) == 1 and down.iloc[0] == g.sensor_serial.iloc[0], s
        sens = []
        for day in g.date:
            ser = down.iloc[0] if day < reg.loc[s, "installed"] else up
            cs = cert[(cert.serial == ser) & (cert.calibration_date <= day)].sort_values("calibration_date")
            sens.append(cs.sensitivity_uv_per_w_m2.iloc[-1])
        out[s] = float((g.poa_signal_mvh / np.array(sens)).sum() / g.poa_irradiation_kwh_m2.sum())
    return out


def ask_b(T):
    al = pd.read_csv(os.path.join(T, "scada_alarm_log_2025.csv"), parse_dates=["raised_utc"])
    wo = pd.read_csv(os.path.join(T, "cmms_work_orders_2025.csv"))
    vt = pd.read_csv(os.path.join(T, "van_tracker_site_visits_2025.csv"), parse_dates=["entered"])
    vans = pd.read_csv(os.path.join(T, "technician_vans_2025.csv"), parse_dates=["from", "to"])
    vt["utc"] = vt.entered.dt.tz_localize(LONDON).dt.tz_convert("UTC").dt.tz_localize(None)
    wo = wo[wo.alarm_ref.notna()]
    j = al.merge(wo.assign(alarm_ref=wo.alarm_ref.astype(int)), left_on="alarm_id", right_on="alarm_ref",
                 suffixes=("", "_wo"))
    hrs = []
    for r in j.itertuples():
        day = pd.Timestamp(r.raised_utc).tz_localize("UTC").tz_convert(LONDON).tz_localize(None).normalize()
        v = vans[(vans.technician == r.assigned_to) & (vans["from"] <= day) & (vans["to"].isna() | (vans["to"] >= day))]
        van = v.sort_values("from").vehicle.iloc[-1]
        t = vt[(vt.vehicle == van) & (vt.site == r.site) & (vt.utc >= r.raised_utc)].utc.min()
        hrs.append((t - r.raised_utc).total_seconds() / 3600)
    j["h"] = hrs
    return j.groupby("site").h.mean().to_dict()


def main(zp):
    fails = []

    def ok(label, cond, detail=""):
        print("%-4s %s %s" % ("PASS" if cond else "FAIL", label, detail))
        if not cond:
            fails.append(label)
    T = tempfile.mkdtemp()
    with zipfile.ZipFile(zp) as z:
        z.extractall(T)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    out, clean, loss, wash, kp = the_call(T)
    site = max(out, key=out.get)
    ok("call site", site == F["call_site"], site)
    ok("call export", int(round(out[site] / 100) * 100) == F["call_export_mwh"], "%.1f" % out[site])
    for k in ("Larkhill Common", "Marston Vale"):
        ok("%s export" % k, int(round(out[k] / 100) * 100) == F["export_mwh"][k], "%.1f" % out[k])
    ok("Hallam Down before dust", int(round(clean["Hallam Down"] / 100) * 100) == F["hallam_clean_export_mwh"])
    ok("Hallam Down loss", round(100 * loss, 1) == F["hallam_loss_pct"], "%.3f" % (100 * loss))
    ok("wash thresholds", list(wash) == F["wash_mm"], str(wash))
    ok("Knowle Park ratio", round(kp, 3) == F["knowle_ratio"], "%.4f" % kp)
    lead = 100 * (clean["Hallam Down"] / clean["Kingsley Fields"] - 1)
    ok("Hallam Down lead", round(lead, 1) == F["hallam_lead_pct"], "%.3f" % lead)
    for s, v in ask_a(T).items():
        ok("A %s" % s, round(v, 3) == F["ask_a"][s] and ("%s: %.3f" % (s, v)) in sub, "%.5f" % v)
    for s, v in ask_b(T).items():
        ok("B %s" % s, round(v, 1) == F["ask_b"][s] and ("%s: %.1f" % (s, v)) in sub, "%.3f" % v)
    ok("write-up states the call", "Build Kingsley Fields in 2027" in sub and "9,700 MWh" in sub)
    ok("no em or en dash in the write-up", not re.search("[–—]", sub))
    print("%d failures" % len(fails))
    return fails


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target.zip")) else 0)
