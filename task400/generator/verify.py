"""Independent verifier: recomputes every graded figure from target/ alone, with no generator code, and compares it
with figures.json. Exit 1 on any difference.

    python3 task400/generator/verify.py
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    got = {}
    reg = pd.read_excel(os.path.join(T, "incident_register_2025-01_2026-10.xlsx"))
    vi = reg[reg["Classification"].str.strip().isin(["VI-COL", "VI-SPI"])].copy()
    vi["t"] = pd.to_datetime(vi["Occurred"])
    for y in (2025, 2026):
        got["vi_jul_oct_%d" % y] = int(((vi["t"].dt.year == y) & (vi["t"].dt.month >= 7) & (vi["t"].dt.month <= 10)).sum())
    ym = vi["t"].dt.strftime("%Y%m").astype(int).value_counts()
    got["monthly"] = [[k, int(ym.get(k, 0))] for k in sorted(set(int("%d%02d" % (y, m)) for y in (2025, 2026)
                                                                for m in range(1, 13)) - {202611, 202612})]
    # units on trucks, by dated install
    dev = pd.read_excel(os.path.join(T, "cas_device_register_2026-10-31.xlsx"), sheet_name="Devices")
    dev = dev[dev["Asset"].astype(str).str.startswith("DT")].copy()
    dev["truck"] = dev["Asset"].str.replace("-", "", regex=False)
    dev["inst"] = pd.to_datetime(dev["Installed"])
    dev["rem"] = pd.to_datetime(dev["Removed"]).fillna(pd.Timestamp("2099-01-01"))
    fw = pd.read_excel(os.path.join(T, "cas_device_register_2026-10-31.xlsx"), sheet_name="Firmware")
    fw["loc"] = pd.to_datetime(fw["Applied (UTC)"]) + pd.Timedelta(hours=8)
    up = fw.merge(dev[["Serial", "inst"]], on="Serial")
    up = up[up["Version"].str.startswith("5") & (up["loc"].dt.normalize() > up["inst"])]
    lo, hi = up["loc"].min(), up["loc"].max()
    got["rollout_days"] = "%d and %d June 2026" % (lo.day, hi.day)
    al = pd.read_parquet(os.path.join(T, "cas_alert_events_2025-01_2026-10.parquet"))
    al = al[(al["alert_level"] == "CRIT") & al["unit_serial"].isin(dev["Serial"])].copy()
    al["loc"] = pd.to_datetime(al["onset_utc"].str.replace("Z", "", regex=False)) + pd.Timedelta(hours=8)
    al = al.merge(dev[["Serial", "truck", "inst", "rem"]], left_on="unit_serial", right_on="Serial")
    al = al[(al["loc"] >= al["inst"]) & (al["loc"] < al["rem"])]
    al = al[(al["loc"] >= pd.Timestamp("2026-06-02")) & (al["loc"] < pd.Timestamp("2026-06-24"))].sort_values("loc")
    fws = fw.sort_values("loc")
    al = pd.merge_asof(al, fws[["Serial", "Version", "loc"]].rename(columns={"loc": "fw_at", "Serial": "unit_serial"}),
                       left_on="loc", right_on="fw_at", by="unit_serial")
    fm = pd.read_parquet(os.path.join(T, "fms_event_windows_2025-2026.parquet"))
    fm = fm[fm["trigger"] == "CAS_CRITICAL"]
    w = fm.pivot_table(index=["event_ref", "truck_no", "trigger_time_awst"], columns="t_offset_s", values="speed_kmh").reset_index()
    w["tt"] = pd.to_datetime(w["trigger_time_awst"])
    w["truck"] = w["truck_no"].str.replace("-", "", regex=False)
    al["truck"] = al["truck"].astype(object)
    w["truck"] = w["truck"].astype(object)
    m = pd.merge_asof(al, w.sort_values("tt")[["truck", "tt", 0, 6]], left_on="loc", right_on="tt", by="truck",
                      direction="forward", tolerance=pd.Timedelta(seconds=3))
    m = m[m[0].notna() & m[6].notna()]
    m["acted"] = m[6] <= m[0] - 6
    fam = np.where(m["Version"].str.startswith("5"), "5", "4")
    got["resp_window_v43_pct"] = int(5 * round(m[fam == "4"]["acted"].mean() * 20))
    got["resp_window_v5_pct"] = int(5 * round(m[fam == "5"]["acted"].mean() * 20))
    # gate trips: the two North readers read one passage seconds apart
    g = pd.read_csv(os.path.join(T, "pit_gate_reads_2026-07_2026-10.csv"), keep_default_na=False)
    g = g[g["direction"] == "IN"].copy()
    g["t"] = pd.to_datetime(g["read_time_awst"])
    n = g[g["reader"].str.startswith("NG")].sort_values(["t", "reader"]).reset_index(drop=True)
    drop = set()
    for i in range(1, len(n)):
        if n.at[i, "reader"] == "NG-2" and n.at[i - 1, "reader"] == "NG-1" and \
                2 <= (n.at[i, "t"] - n.at[i - 1, "t"]).total_seconds() <= 13 and (i - 1) not in drop:
            drop.add(i)
    trips = pd.concat([g[g["reader"] == "SG-IN"], n.drop(index=list(drop))])
    for mo in (7, 8, 9, 10):
        x = trips[trips["t"].dt.month == mo]
        got["trips_%02d" % mo] = int(len(x))
        got["trips_notag_%02d" % mo] = int((x["cas_tag"] == "").sum())
    # ramp times over the limit in force: a window that opens on the sample closing the same truck's previous window on
    # that ramp, with the truck still over the limit there, continues that run
    f = pd.read_parquet(os.path.join(T, "fms_event_windows_2025-2026.parquet"))
    f = f[(f["trigger"] == "OVERSPEED") & f["segment"].isin(["NRP", "SRP"]) & f["truck_no"].str.startswith("DT")]
    f = f.copy()
    f["at"] = pd.to_datetime(f["trigger_time_awst"]) + pd.to_timedelta(f["t_offset_s"], unit="s")
    lim = pd.read_csv(os.path.join(T, "haul_road_speed_limits.csv"))
    lim["eff"] = pd.to_datetime(lim["effective_from"])
    w = f.groupby("event_ref").agg(truck=("truck_no", "first"), seg=("segment", "first"), t0=("trigger_time_awst", "first"),
                                   start=("at", "min"), end=("at", "max"), peak=("speed_kmh", "max")).reset_index()
    edge = f.set_index(["event_ref", "at"])["speed_kmh"]
    w["t0"] = pd.to_datetime(w["t0"])
    w["lim"] = [float(lim[(lim["segment"] == s_) & (lim["eff"] <= t.normalize())].sort_values("eff")["limit_kmh"].iloc[-1])
                for s_, t in zip(w["seg"], w["t0"])]
    w = w.sort_values(["truck", "seg", "t0"]).reset_index(drop=True)
    run, k = [], 0
    for i in range(len(w)):
        if i and w.at[i, "truck"] == w.at[i - 1, "truck"] and w.at[i, "seg"] == w.at[i - 1, "seg"] and \
                w.at[i, "start"] == w.at[i - 1, "end"] and edge[(w.at[i, "event_ref"], w.at[i, "start"])] > w.at[i, "lim"]:
            pass
        else:
            k += 1
        run.append(k)
    w["run"] = run
    rr = w.groupby("run").agg(seg=("seg", "first"), t0=("t0", "first"), peak=("peak", "max"), lim=("lim", "first"))
    for s_ in ("NRP", "SRP"):
        for mo in (7, 8, 9, 10):
            x = rr[(rr["seg"] == s_) & (rr["t0"].dt.year == 2026) & (rr["t0"].dt.month == mo)]
            got["os_%s_%02d" % (s_, mo)] = int(len(x))
            got["os5_%s_%02d" % (s_, mo)] = int((x["peak"] > x["lim"] + 5).sum())
    bad = [k for k in got if F.get(k) != got[k]]
    for k in sorted(got):
        if k != "monthly":
            print("%-22s figures %-22s verify %s%s" % (k, F.get(k), got[k], "" if k not in bad else "   MISMATCH"))
    print("monthly", "match" if "monthly" not in bad else "MISMATCH")
    print("verify: %d figures, %d mismatch" % (len(got), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
