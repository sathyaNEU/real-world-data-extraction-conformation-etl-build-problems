"""Independent verifier: reads only the shipped bundle (no generator state, its own code path) and recomputes the
call, every district's at-risk count, the default path, both asks and the filed sentences, then compares them with
generator/figures.json.

    python3 verify.py <target>"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OK = []


def say(label, ok, detail):
    OK.append(ok)
    print("%s  %-12s %s" % ("PASS" if ok else "FAIL", label, detail))


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    return " ".join(out.split())


def main(target):
    rd = lambda f, **k: pd.read_csv(os.path.join(target, f), **k)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    reg = rd("gis_service_transformers.csv")
    reg["n"] = reg.xfmr_loc_id.str.replace("T", "", regex=False).astype(np.int64)
    reg = reg.set_index("n")
    t24 = rd("tlm_summer_peaks_2024.csv", dtype={"LOC_NO": str})
    peaks = {2024: pd.DataFrame({"n": t24.LOC_NO.astype(np.int64), "kva_pk": t24.PEAK_KVA,
                                 "day": pd.to_datetime(t24.PEAK_DT, format="%m/%d/%Y")}).set_index("n")}
    for y in (2025, 2026):
        t = rd("tlm_summer_peaks_%d.csv" % y)
        peaks[y] = pd.DataFrame({"n": t.xfmr_loc_id, "kva_pk": t.peak_kva, "day": pd.to_datetime(t.peak_date)}).set_index("n")
    sp = rd("service_points.csv", usecols=["sp_id", "xfmr_loc_id"])
    sp_n = pd.Series(sp.xfmr_loc_id.str[1:].astype(np.int64).values, index=sp.sp_id.values)
    ev = rd("rate_schedule_changes.csv")
    ev = ev[ev.to_schedule == "R-EV2"].groupby("sp_id")["effective_date"].min()
    ev = pd.to_datetime(ev)
    dm = rd("dmv_pev_notifications.csv", dtype={"matched_sp_id": "float64"})
    dm = dm[dm.matched_sp_id.notna()].copy()
    dm["sp"] = dm.matched_sp_id.astype(np.int64)
    dm["n"] = dm.sp.map(sp_n)
    dm = dm[dm.n.notna()]
    dm["n"] = dm.n.astype(np.int64)
    dm["a"] = pd.to_datetime(dm.reg_start_date)
    dm["b"] = pd.to_datetime(dm.status_date.where(dm.reg_status != "CURRENT"))
    dm["evd"] = dm.sp.map(ev)
    locs = reg.index.values

    def counts_on(day_of):
        d = dm.n.map(day_of)
        here = (dm.a <= d) & (dm.b.isna() | (dm.b > d))
        on = dm.evd.notna() & (dm.evd <= d)
        k = dm[here & ~on].groupby("n").size().reindex(locs, fill_value=0)
        e = dm[here & on].groupby("n").size().reindex(locs, fill_value=0)
        return k.values, e.values

    st = {y: counts_on(peaks[y].day) for y in (2024, 2025, 2026)}
    st["rec"] = counts_on(pd.Series(pd.Timestamp("2027-03-31"), index=locs))
    kva = reg.kva_rating.astype(float).values
    grp = np.where(kva <= 15, "S", np.where(kva <= 37.5, "M", "L"))
    dist = reg.district.values
    pk = {y: peaks[y].kva_pk.reindex(locs).values for y in (2024, 2025, 2026)}
    # transitions: weather by the district median ratio on transformers whose vehicles did not change
    tou, evr = [], []
    for y0, y1 in ((2024, 2025), (2025, 2026)):
        dk = st[y1][0] - st[y0][0]
        de = st[y1][1] - st[y0][1]
        flat = (dk == 0) & (de == 0)
        med = pd.Series(pk[y1][flat] / pk[y0][flat]).groupby(dist[flat]).median()
        adj = pk[y1] - pd.Series(dist).map(med).values * pk[y0]
        pos = np.minimum(st[y0][0], 2) + 1
        m1 = (dk == 1) & (de == 0)
        tou.append(pd.DataFrame({"g": grp[m1], "pos": pos[m1], "adj": adj[m1]}))
        evr.append(adj[(de == 1) & (dk == 0)])
    tou = pd.concat(tou)
    e_inc = float(np.concatenate(evr).mean())
    t_inc = float(tou["adj"].mean())          # OP 4: one figure for every default-rate vehicle, one for every R-EV2 one
    fc = pk[2026] + t_inc * (st["rec"][0] - st[2026][0]) + e_inc * (st["rec"][1] - st[2026][1])
    say("V-effects", round(t_inc, 1) == F["increment_default_kva"] and round(e_inc, 1) == F["increment_ev_kva"],
        "per-schedule effects %.3f and %.3f kVA" % (t_inc, e_inc))
    risk = pd.Series(fc > 1.2 * kva).groupby(dist).sum()
    names = list(F["at_risk"])
    risk = risk.reindex(names).astype(int)
    share = 400 * risk / risk.sum()
    base = np.floor(share).astype(int)
    left = 400 - int(base.sum())
    extra = (share - base).sort_values(ascending=False).index[:left]
    alloc = base.copy()
    alloc[extra] += 1
    say("V-atrisk", all(int(risk[d]) == F["at_risk"][d] for d in names), "at-risk counts %s" % dict(risk))
    say("V-call", all(int(alloc[d]) == F["call"][d] for d in names), "allocation %s" % dict(alloc))
    say("V-foothill", int(alloc["Foothill"]) == F["foothill_replacements"], "Foothill %d" % alloc["Foothill"])
    # the default path from the load study parquet
    I = pd.read_parquet(os.path.join(target, "ev_load_study_2026_intervals.parquet"))
    lp = rd("ev_load_study_2026_participants.csv").set_index("participant_id")["rate_schedule"]
    h = I.interval_ending.dt.hour * 60 + I.interval_ending.dt.minute
    w = I[(h >= 975) & (h <= 1260)]
    avg = (w.kwh * 4 / 0.95).groupby(w.participant_id.map(lp)).mean()
    f0 = pk[2026] + (st["rec"][0] - st[2026][0]) * avg["R-TOU4"] + (st["rec"][1] - st[2026][1]) * avg["R-EV2"]
    r0 = pd.Series(f0 > 1.2 * kva).groupby(dist).sum().reindex(names)
    s0 = 400 * r0 / r0.sum()
    b0 = np.floor(s0).astype(int)
    b0[(s0 - b0).sort_values(ascending=False).index[:400 - int(b0.sum())]] += 1
    say("V-default", int(b0["Foothill"]) == F["default_path_foothill"] and round(avg["R-TOU4"], 2) == F["load_study_avg_default_kva"],
        "load study %.2f kVA, default path Foothill %d" % (avg["R-TOU4"], b0["Foothill"]))
    # ask A
    chg = rd("gis_unit_changes_2024-2027.csv", dtype={"wo_number": str})
    chg["district"] = chg.xfmr_loc_id.str[1:].astype(np.int64).map(reg.district)
    d = pd.to_datetime(chg.change_date)
    ptr = chg[(chg.reason_code == "PTR") & (d >= "2025-10-06") & (d <= "2026-04-24") & (chg.removed_serial != chg.installed_serial)]
    wo = pd.read_excel(os.path.join(target, "ptr_pilot_work_orders.xlsx"))
    cost = rd("ptr_pilot_cost_lines.csv", dtype={"wo_number": str})
    cost["district"] = cost.wo_number.map(dict(zip(wo["Work Order"].astype(str), wo["District"])))
    okA = True
    for dn in ("Railyard", "Canal", "Brookside"):
        g = ptr[ptr.district == dn]
        n = len(g)
        kv = float((g.installed_kva - g.removed_kva).sum())
        cp = cost[cost.district == dn].amount_usd.astype(float).sum() / n
        a = F["ask_a"][dn]
        okA &= (n == a["replaced"] and abs(kv - a["kva_added"]) < 1e-9 and int(round(cp)) == a["cost_per_replacement"])
    say("V-askA", okA, "pilot replaced, kVA added and cost per replacement")
    # ask B
    om = rd("oms_transformer_outages_summer2026.csv")
    s = pd.to_datetime(om.outage_start_utc) - pd.Timedelta(hours=7)
    e = pd.to_datetime(om.restored_utc) - pd.Timedelta(hours=7)
    keep = (om.cause_code == "EQ-XFMR") & (s >= "2026-06-01") & (s < "2026-10-01")
    nsp = sp.groupby("xfmr_loc_id").size()
    hrs = ((e - s).dt.total_seconds() / 3600)[keep]
    cust = om.xfmr_loc_id[keep].map(nsp)
    dd = om.xfmr_loc_id[keep].str[1:].astype(np.int64).map(reg.district)
    chs = (cust * hrs).groupby(dd).sum()
    o8 = cust[hrs > 8].groupby(dd[hrs > 8]).sum()
    okB = all(int(round(chs[dn])) == F["ask_b"][dn]["customer_hours"] and int(o8.get(dn, 0)) == F["ask_b"][dn]["customers_over_8h"]
              for dn in names)
    say("V-askB", okB, "customer-hours and customers out more than eight hours, twelve districts")
    # the filed sentences, through a second extractor
    dec = pdf_text(os.path.join(target, "decision_26-11-019_excerpt.pdf"))
    say("V-dec", "largest fractional parts" in dec and "on the day of its recorded 2026 peak" in dec and
        "exceeds 120 percent of its nameplate rating" in dec and "March 31, 2027" in dec, "decision OP 2 to OP 5 (pdftotext)")
    tar = pdf_text(os.path.join(target, "residential_rate_schedules_excerpt.pdf"))
    say("V-tariff", "4:00 p.m. to 9:00 p.m." in tar and "next regular meter reading date" in tar, "tariff periods and effective-date rule")
    dic = pd.read_excel(os.path.join(target, "data_dictionary.xlsx"), sheet_name="Fields")
    say("V-dict", dic.Definition.str.contains("0.95").any() and dic.Definition.str.contains("UTC").any(), "dictionary basis and clock")
    say("V-xlsx", len(wo) > 200 and set(wo.District) == {"Railyard", "Canal", "Brookside"}, "work order workbook read")
    print("%d verifier checks, %d FAIL" % (len(OK), OK.count(False)))
    return 0 if all(OK) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
