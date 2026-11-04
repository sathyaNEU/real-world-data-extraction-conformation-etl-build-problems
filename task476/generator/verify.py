"""Independent verifier: reads only target/ and golden/ on its own code path (pandas, openpyxl via pandas, pdfplumber
words, python-docx) and recomputes the deviation periods, the shortfall, the spring volumes and every daily mean, then
compares them with the golden files and figures.json."""
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
import pdfplumber
from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))


def recompute(target):
    raw = open(os.path.join(target, "gauge", "bp1_stage_2026.csv"), encoding="utf-8").read().splitlines()
    k = [i for i, l in enumerate(raw) if l.startswith("Date Time")][0]
    st = pd.read_csv(os.path.join(target, "gauge", "bp1_stage_2026.csv"), skiprows=k)
    st.columns = ["t", "h"]
    st["t"] = pd.to_datetime(st["t"]) + pd.Timedelta(hours=1)          # PST clock to local daylight time
    tab = pd.read_excel(os.path.join(target, "gauge", "bp1_station_register.xlsx"), sheet_name="Rating 7")
    gh, qq = tab.iloc[:, 0].to_numpy(float), tab.iloc[:, 1].to_numpy(float)
    words = []
    with pdfplumber.open(os.path.join(target, "gauge", "bp1_rating7_report_2023.pdf")) as pdf:
        for pg in pdf.pages:
            words += [w["text"] for w in pg.extract_words()]
    s = " ".join(words)
    m = re.search(r"Q = (\d+\.\d) \+ (\d+) \(GH - (\d\.\d\d)\)\^(\d\.\d\d)", s)
    base, kk, top, pw = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))

    def q(h):
        h = np.asarray(h, float)
        lo = np.interp(h, gh, qq)
        hi = base + kk * np.clip(h - top, 0, None) ** pw
        return np.where(h <= top, lo, hi)
    vis = pd.read_csv(os.path.join(target, "gauge", "bp1_field_visits_2026.csv"))
    fine = np.linspace(1.0, 7.5, 65001)
    qf = q(fine)
    vis["shift"] = [fine[np.searchsorted(qf, qm)] - g for qm, g in zip(vis.meas_discharge_cfs, vis.meas_mean_gh_ft)]
    t_s = pd.to_datetime(vis.visit_date + " " + vis.meas_start_pdt)
    t_e = pd.to_datetime(vis.visit_date + " " + vis.meas_end_pdt)
    vis["when"] = t_s + (t_e - t_s) / 2
    vis["pct"] = vis.meas_discharge_cfs / q(vis.meas_mean_gh_ft.to_numpy()) - 1
    off = vis[vis["pct"].abs() >= 0.05]
    t1 = off["when"].min()
    t0 = vis[vis["when"] < t1]["when"].max()
    win = st[(st.t >= t0) & (st.t <= t1)]
    peak = win.loc[win.h.idxmax(), "t"]
    s_mean = vis[vis["when"] > peak]["shift"].mean()
    st["q"] = np.where(st.t >= peak, q(st.h + s_mean), q(st.h))
    st["day"] = st.t.dt.date
    daily = st.groupby("day").q.mean()
    daily = daily[(daily.index >= dt.date(2026, 5, 1)) & (daily.index <= dt.date(2026, 10, 31))]
    mins = pd.Series([50.0 if dt.date(2026, 7, 1) <= x <= dt.date(2026, 9, 30) else 30.0 for x in daily.index],
                     index=daily.index)
    dev = daily[daily < mins]
    shortfall = ((mins - daily)[daily < mins]).sum() * 1.98347
    may = daily[[x.month == 5 for x in daily.index]].sum() * 1.98347
    june = daily[[x.month == 6 for x in daily.index]].sum() * 1.98347
    return dict(daily=daily, dev=list(dev.index), shortfall=shortfall, may=may, june=june, s_mean=s_mean, peak=peak)


def _r(v, u):
    return int(math.floor(v / u + 0.5) * u)


def main(target=None, gdir=None):
    task = os.path.dirname(HERE)
    target = target or os.path.join(task, "target")
    gdir = gdir or os.path.join(task, "golden")
    v = recompute(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    fails = []

    def chk(name, ok, detail=""):
        print("%s  V %s %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            fails.append(name)

    runs = []
    for k in v["dev"]:
        if runs and (k - runs[-1][1]).days == 1:
            runs[-1][1] = k
        else:
            runs.append([k, k])
    chk("deviation periods", [[a.isoformat(), b.isoformat()] for a, b in runs] == fig["deviation_periods"], str(runs))
    chk("shortfall", "{:,}".format(_r(v["shortfall"], 100)) == fig["shortfall_af"], "%.1f" % v["shortfall"])
    chk("May and June volumes", "{:,}".format(_r(v["may"], 100)) == fig["may_af"] and
        "{:,}".format(_r(v["june"], 100)) == fig["june_af"], "%.0f, %.0f" % (v["may"], v["june"]))
    dd = {k.isoformat(): _r(x, 1) for k, x in v["daily"].items() if k.month >= 7}
    agree = sum(1 for k in dd if dd[k] == fig["daily_cfs"][k])
    chk("daily means", agree == len(dd), "%d of %d" % (agree, len(dd)))
    rec = pd.read_excel(os.path.join(gdir, "bypass_flow_record_2026.xlsx"), sheet_name="Daily record", skiprows=3)
    rec = rec.dropna(subset=["Daily mean flow (cfs)"])
    rec = rec[rec["Article 403 minimum (cfs)"].apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))]
    chk("golden workbook read back (positive control)", len(rec) == 123, "%d rows" % len(rec))
    ok = all(int(r["Daily mean flow (cfs)"]) == fig["daily_cfs"][pd.Timestamp(r["Date"]).date().isoformat()] for _, r in
             rec.iterrows())
    chk("golden workbook daily means", ok)
    doc = Document(os.path.join(gdir, "minimum_flow_deviation_report_2026.docx"))
    txt = " ".join(p.text for p in doc.paragraphs)
    chk("golden report read back (positive control)", "Article 403" in txt)
    chk("golden report states the periods, the shortfall and both volumes",
        all(s in txt for s in fig["deviation_periods_text"]) and fig["shortfall_af"] in txt and fig["may_af"] in txt and
        fig["june_af"] in txt)
    with pdfplumber.open(os.path.join(target, "license", "license_order_excerpt_2019.pdf")) as pdf:
        lic = " ".join((pg.extract_text() or "") for pg in pdf.pages)
    chk("license carries Article 403's minimums (positive control)", "50 cubic feet per second" in re.sub(r"\s+", " ", lic))
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
