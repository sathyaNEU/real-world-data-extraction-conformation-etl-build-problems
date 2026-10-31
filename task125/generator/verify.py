"""An independent recompute of every graded figure from target.zip alone, with pandas and none of the generator's
modules: the call (each unit's load as its inflows carry it in), the discharges by quarter and the loggers' hours.

    python3 task125/generator/verify.py
"""
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FAIL = []


def check(label, cond, detail=""):
    print(("ok    " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))
    if not cond:
        FAIL.append(label)


def main():
    z = zipfile.ZipFile(os.path.join(TASK, "target.zip"))
    rd = lambda n: pd.read_csv(io.BytesIO(z.read(n)), dtype=str)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    reg = pd.read_excel(io.BytesIO(z.read("umzimela_monitoring_network_register.xlsx")), sheet_name=None, dtype=str)
    sites, weirs, units = reg["Sites"], reg["Weirs"], reg["Resource units"]
    bmon = {r.resource_unit: r.site_code for r in sites.itertuples() if str(r.purpose).startswith("boundary")}
    stn = dict(zip(weirs.weir, weirs.station))
    lab = rd("umzimela_wq_lab_results_2025_26.csv")
    s = lab[lab.analyte == "SO4"].copy()
    s["rr"] = s.lab_sample_id.str.endswith("-R")
    s = s.sort_values(["site_code", "sample_date", "rr", "analysed_date"]).groupby(["site_code", "sample_date"]).tail(1)
    so4 = {(a, b): float(c) for a, b, c in zip(s.site_code, s.sample_date, s.result)}
    gq = rd("umzimela_gauges_daily_2025_26.csv")
    flow = {(a, b): float(c) for a, b, c in zip(gq.station, gq.date, gq.mean_flow_m3s)}
    dates = sorted({d for d in s.sample_date if "2026-05-01" <= d <= "2026-09-30"})
    check("eleven dry-season runs", len(dates) == 11, len(dates))
    up = {r.resource_unit: [x.strip() for x in str(r.upstream_units).split(",") if x.strip() and x != "nan"]
          for r in units.itertuples()}
    weir = dict(zip(units.resource_unit, units.lower_boundary_weir))
    alloc = fig["allocations_t_per_day"]

    def load(u, d):
        if not up[u]:
            return so4[(bmon[u], d)] * flow[(stn[weir[u]], d)] * 0.0864
        return sum(load(i, d) for i in up[u])
    loads = {u: np.mean([load(u, d) for d in dates]) for u in up}
    over = sorted(u for u in loads if loads[u] > alloc[u])
    check("the call: the units over their allocations", over == fig["call"]["over"], over)
    check("each unit's load in whole tonnes a day", all(int(round(loads[u])) == fig["loads_whole"][u] for u in loads))
    # ask A
    rt = rd("wul_discharge_returns_2025_26.csv").sort_values("submitted_on").groupby(["discharge_point", "month"]).tail(1)
    ins = rd("cma_compliance_inspections_2025_26.csv")
    swap = {}
    for r in ins.itertuples():
        m = re.search(r"final reading ([0-9]+)", r.findings)
        if m:
            swap[r.discharge_point] = (r.date[:7], float(m.group(1)))
    out = {}
    for pt, g in rt.groupby("discharge_point"):
        g = g.sort_values("month")
        prev = None
        mon = {}
        for r in g.itertuples():
            tot = float(r.totaliser_m3)
            if prev is not None:
                v = (swap[pt][1] - prev + tot) if (pt in swap and swap[pt][0] == r.month) else tot - prev
                c = float(r.sulphate_mg_l)
                if pt.split("-")[0] in ("KHC", "NCH", "MMC") and r.month >= "2025-11":
                    c *= 96.06 / 32.06
                mon[r.month] = v * c / 1e6
            prev = tot
        for q, ms in {"Q1": ("2025-10", "2025-11", "2025-12"), "Q2": ("2026-01", "2026-02", "2026-03"),
                      "Q3": ("2026-04", "2026-05", "2026-06"), "Q4": ("2026-07", "2026-08", "2026-09")}.items():
            out["%s %s" % (pt, q)] = int(round(sum(mon[m] for m in ms), -1))
    check("ask A: every discharge point and quarter", out == fig["ask_a_tonnes"],
          {k: (out[k], fig["ask_a_tonnes"][k]) for k in out if out[k] != fig["ask_a_tonnes"].get(k)})
    # ask B
    ec = rd("umzimela_ec_loggers_hourly_2025_26.csv")
    ec["local"] = pd.to_datetime(ec.timestamp.str.replace("Z", "")) + pd.Timedelta(hours=2)
    mem = rd("ec_logger_memory_downloads_2025_26.csv")
    mem["local"] = pd.to_datetime(mem.reading_local)
    allr = pd.concat([ec[["logger_id", "local", "ec_uS_cm"]], mem[["logger_id", "local", "ec_uS_cm"]]])
    allr = allr.drop_duplicates(["logger_id", "local"])
    allr["v"] = allr.ec_uS_cm.astype(float)
    sv = rd("ec_logger_service_visits_2025_26.csv")
    sv["t"] = pd.to_datetime(sv.visit_local)
    trig = {r.ec_logger: float(r.ec_trigger_uS_cm) for r in sites.itertuples() if str(r.ec_logger) not in ("nan", "")}
    res = {}
    for lid, g in allr.groupby("logger_id"):
        vs = sv[sv.logger_id == lid].sort_values("t")
        tt = vs.t.tolist()
        dd = [(float(a) - float(b)) if str(a) not in ("nan", "") else 0.0 for a, b in
              zip(vs.reading_before_clean_uS_cm, vs.reading_after_clean_uS_cm)]
        g = g.sort_values("local")
        k = np.searchsorted(np.array(tt, dtype="datetime64[ns]"), g.local.values, side="right")
        corr = []
        for t, kk, v in zip(g.local, k, g.v):
            if 0 < kk < len(tt):
                frac = (t - tt[kk - 1]).total_seconds() / (tt[kk] - tt[kk - 1]).total_seconds()
                v = v - dd[kk] * frac
            corr.append(v)
        g = g.assign(c=corr, m=g.local.dt.strftime("%Y-%m"))
        for m in ("2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"):
            res["%s %s" % (lid, m)] = int(((g.m == m) & (g.c > trig[lid])).sum())
    check("ask B: every logger and month", res == fig["ask_b_hours"],
          {k: (res[k], fig["ask_b_hours"][k]) for k in res if res[k] != fig["ask_b_hours"].get(k)})
    print("verify: %s" % ("all passed" if not FAIL else "%d failed" % len(FAIL)))
    return len(FAIL)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
