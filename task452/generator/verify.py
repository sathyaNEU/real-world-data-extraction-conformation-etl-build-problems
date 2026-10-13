"""Independent verifier for task452: reads only target/ (and figures.json to compare), imports nothing from the
generator, and recomputes the call (each day's concentration from a seasonal log-log rating curve fitted to every
accepted routine sample of water years 2024 to 2026, retransformed by smearing), the default path's slate (samples
interpolated across the water year), each tributary's upstream permitted wastewater phosphorus and its 2026 cover crop
acres."""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FAILS = []
KG = 0.028316846592 * 86400 * 1000 / 1e6


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def offset(t):
    """Eastern time's hours behind UTC at a UTC instant (daylight from 2am local on the second Sunday of March to 2am
    local on the first Sunday of November)"""
    for a, b in ((dt.datetime(2025, 3, 9, 7), dt.datetime(2025, 11, 2, 6)), (dt.datetime(2026, 3, 8, 7), dt.datetime(2026, 11, 1, 6))):
        if a <= t < b:
            return 4
    return 5


def main(target, golden=None):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    import openpyxl
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, "brannoch_lake_phosphorus_agreement.pdf")).pages)
    wb = openpyxl.load_workbook(os.path.join(target, "blc_station_register.xlsx"), read_only=True)
    st = [r for r in wb["Stations"].iter_rows(min_row=5, values_only=True) if r[0]]
    A = {}
    for r in st:
        m = re.search(re.escape(r[0]) + r"\s+" + re.escape(r[1]) + r"\s+([\d,]+)", txt)
        A[r[0]] = float(m.group(1).replace(",", ""))
    check(len(A) == 10, "Schedule 1 lists ten tributaries")
    sid = {}
    for r in st:
        sid[r[1]] = r[0]
        sid[r[2]] = r[0]
    w = pd.read_csv(os.path.join(target, "blc_water_quality_results_2027-01-08.csv"), dtype=str)
    tp = w[w["ResultSampleFractionText"].eq("Total") & w["CharacteristicName"].str.contains("Phosphorus")
           & w["ActivityTypeCode"].eq("Sample-Routine") & w["ResultStatusIdentifier"].eq("Accepted")]
    v = tp["ResultMeasureValue"].astype(float) / np.where(tp["ResultMeasure/MeasureUnitCode"].eq("ug/L"), 1000.0, 1.0)
    samp = {n: [] for n in A}
    for loc, d, c in zip(tp["MonitoringLocationIdentifier"], tp["ActivityStartDate"], v):
        samp[sid[loc]].append((dt.date.fromisoformat(d), c))
    uv = pd.read_csv(os.path.join(target, "merrifield_unit_values_wy2026_approved.csv"), comment="#", dtype={"gage_id": str})
    t = pd.to_datetime(uv["datetime_utc"])
    off = np.array([offset(x) for x in t.dt.to_pydatetime()])
    uv["day"] = (t - pd.to_timedelta(off, unit="h")).dt.date
    dq = uv.groupby(["gage_id", "day"])["discharge_cfs"].mean()
    dv = pd.read_csv(os.path.join(target, "merrifield_daily_values_wy2024-wy2025.csv"), comment="#", dtype={"gage_id": str})
    days = [dt.date(2025, 10, 1) + dt.timedelta(days=i) for i in range(365)]
    G1, R0, VAR, INFO = {}, {}, {}, {}
    for r in st:
        name, gage, ratio = r[0], str(r[3]), float(r[4]) / float(r[5])
        q = {dt.date.fromisoformat(a): b * ratio for a, b in zip(dv.loc[dv["gage_id"].eq(gage), "date"], dv.loc[dv["gage_id"].eq(gage), "discharge_cfs"])}
        for d, x in dq.loc[gage].items():
            q[d] = x * ratio
        s = [(d, c) for d, c in samp[name] if d in q]
        def X(dd, season=True, quad=False):
            lq = np.log([q[d] for d in dd])
            cols = [np.ones(len(dd)), lq] + ([lq ** 2] if quad else [])
            if season:
                a = np.array([2 * np.pi * d.timetuple().tm_yday / 365.25 for d in dd])
                cols += [np.sin(a), np.cos(a)]
            return np.column_stack(cols)
        y = np.log([c for d, c in s])
        qd = np.array([q[d] for d in days])
        loads = []
        for season, quad, corr in ((True, False, "smear"), (True, False, "mle"), (False, False, "smear"), (True, True, "smear")):
            Xs = X([d for d, c in s], season, quad)
            b, *_ = np.linalg.lstsq(Xs, y, rcond=None)
            res = y - Xs @ b
            f = float(np.mean(np.exp(res))) if corr == "smear" else float(np.exp(np.sum(res ** 2) / (len(y) - Xs.shape[1]) / 2))
            pred = np.exp(X(days, season, quad) @ b) * qd
            loads.append(float(np.sum(pred) * KG * f))
            if (season, quad, corr) == (True, False, "smear"):
                top = qd > np.quantile(qd, 0.9)
                s26d = [d for d, c in s if d >= days[0]]
                INFO[name] = dict(slope=float(b[1]), smear=f, n=len(y), top_load=100 * float(pred[top].sum() / pred.sum()),
                                  top_samp=100 * float(np.mean([q[d] > np.quantile(qd, 0.9) for d in s26d])))
        G1[name] = loads[0]
        VAR[name] = (min(loads), max(loads))
        s26 = [(d, c) for d, c in s if d >= days[0]]
        R0[name] = float(np.sum(np.interp([d.toordinal() for d in days], [d.toordinal() for d, c in s26], [c for d, c in s26]) * qd) * KG)
    k10 = lambda x: int(round(x / 10.0)) * 10
    out10 = lambda lo, hi: [int(np.floor(lo / 10.0)) * 10, int(np.ceil(hi / 10.0)) * 10]
    check(all(out10(*VAR[n]) == F["load_range_full_record_kg"][n] for n in A),
          "every tributary's load range over the four full-record curves recomputes (rounded outward)")
    check(all(out10(VAR[n][0] - A[n], VAR[n][1] - A[n]) == F["excess_range_full_record_kg"][n] for n in A),
          "every tributary's range above or below its allocation recomputes (rounded outward)")
    check(all(round(INFO[n]["slope"], 2) == F["slope"][n] and round(INFO[n]["smear"], 3) == F["smearing"][n] and INFO[n]["n"] == F["n_samples"][n] for n in A),
          "slopes, smearing factors and sample counts recompute")
    check(all(round(INFO[n]["top_load"]) == F["top_tenth_load_pct"][n] and round(INFO[n]["top_samp"]) == F["top_tenth_samples_pct"][n] for n in A),
          "the top tenth of days' load and sample shares recompute")
    check(all(k10(A[n] - R0[n]) == v for n, v in F["default_below_kg"].items()), "the default's shortfalls for the funded rivers recompute")
    check(k10(sum(G1.values())) == F["basin_load_kg"], "the basin load recomputes")
    def slate(L):
        ex = {n: L[n] - A[n] for n in L}
        return sorted(sorted((n for n in ex if ex[n] > 0), key=lambda n: -ex[n])[:3])
    check(slate(G1) == sorted(F["call"]), "the rating curve funds %s (figures.json %s)" % (slate(G1), sorted(F["call"])))
    check(all(int(round(G1[n] / 10.0)) * 10 == F["load_kg"][n] for n in A), "every tributary's load recomputes to the nearest 10 kg")
    check(slate(R0) == sorted(F["default_slate"]) and slate(R0) != slate(G1), "interpolation funds %s" % slate(R0))
    # Ask A: permitted facilities upstream of each compliance station
    streams = {r[0]: (r[1], float(r[2])) for r in wb["Streams"].iter_rows(min_row=4, values_only=True) if r[0]}
    outf = {(r[0], r[2]): (r[3], float(r[4])) for r in wb["Facilities"].iter_rows(min_row=4, values_only=True) if r[0]}
    rkm = {r[0]: float(r[6]) for r in st}
    dm = pd.read_csv(os.path.join(target, "npdes_dmr_phosphorus_wy2026.csv"), dtype=str)
    dm = dm[dm["STATISTICAL_BASE"].eq("MO AVG")].sort_values("RECEIVED_DATE").groupby(
        ["PERMIT_ID", "OUTFALL", "MONITORING_PERIOD_END_DATE", "PARAMETER_DESC"]).tail(1)
    ww = {n: 0.0 for n in A}
    for (pid, of, start, end), g in dm.groupby(["PERMIT_ID", "OUTFALL", "MONITORING_PERIOD_START_DATE", "MONITORING_PERIOD_END_DATE"]):
        rw, pos = outf[(pid, of)]
        while rw not in A:
            rw, pos = streams[rw]
        if pos <= rkm[rw]:
            continue
        p_ = g[g["PARAMETER_DESC"].str.startswith("Phosphorus")].iloc[0]
        f_ = g[g["PARAMETER_DESC"].str.startswith("Flow")].iloc[0]
        nd = (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days + 1
        ww[rw] += float(p_["DMR_VALUE"]) * 0.45359237 * nd if p_["DMR_UNIT"] == "lb/d" else float(p_["DMR_VALUE"]) * float(f_["DMR_VALUE"]) * 3.785411784 * nd
    check(all(int(round(ww[n] / 10.0)) * 10 == F["wastewater_stated"][n] for n in A), "every tributary's upstream wastewater phosphorus recomputes to the nearest 10 kg")
    # Ask B: the acres of each enrolled field lying in each watershed, for the contracts in force for crop year 2026
    c = pd.read_csv(os.path.join(target, "farm_practice_contracts_2024-2027.csv"), dtype=str, comment="#")
    c["n"] = c["amendment_no"].astype(int)
    c = c[c["n"].eq(c.groupby("contract_id")["n"].transform("max"))]
    c = c[(c["first_crop_year"].astype(int) <= 2026) & (c["last_crop_year"].astype(int) >= 2026)]
    fm = pd.read_csv(os.path.join(target, "practice_field_watershed_acres.csv"), dtype=str)
    cov = {n: 0.0 for n in A}
    for fid in c["field_id"]:
        part = fm[fm["field_id"].eq(fid)]
        for ws, fa, sh in zip(part["watershed"], part["field_acres"].astype(float), part["share_of_field"].astype(float)):
            cov[ws] += fa * sh
    check(all(int(round(cov[n] / 10.0)) * 10 == F["cover_stated"][n] for n in A), "every watershed's cover crop acres recompute to the nearest 10")
    print("verify: %d failed" % len(FAILS))
    return not FAILS


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")) else 1)
