"""The golden's figures, read from the shipped pack only (target/), and the golden deliverables."""
import datetime as dt
import os

import numpy as np
import pandas as pd

VI = ("VI-COL", "VI-SPI")
ROLLOUT = (dt.datetime(2026, 6, 2), dt.datetime(2026, 6, 24))


def load(target):
    P = {}
    P["alerts"] = pd.read_parquet(os.path.join(target, "cas_alert_events_2025-01_2026-10.parquet"))
    P["fms"] = pd.read_parquet(os.path.join(target, "fms_event_windows_2025-2026.parquet"))
    P["disp"] = pd.read_csv(os.path.join(target, "dispatch_shift_summary_2025-2026.csv"))
    P["reg"] = pd.read_excel(os.path.join(target, "incident_register_2025-01_2026-10.xlsx"), sheet_name="Register")
    P["dev"] = pd.read_excel(os.path.join(target, "cas_device_register_2026-10-31.xlsx"), sheet_name="Devices")
    P["fw"] = pd.read_excel(os.path.join(target, "cas_device_register_2026-10-31.xlsx"), sheet_name="Firmware")
    P["gate"] = pd.read_csv(os.path.join(target, "pit_gate_reads_2026-07_2026-10.csv"), keep_default_na=False)
    P["limits"] = pd.read_csv(os.path.join(target, "haul_road_speed_limits.csv"))
    return P


# ----------------------------------------------------------------------------------------------- the call's counts
def vi_incidents(P):
    reg = P["reg"]
    x = reg[reg["Classification"].isin(VI)].copy()
    x["when"] = pd.to_datetime(x["Occurred"])
    return x


def window_counts(P):
    x = vi_incidents(P)
    m = x["when"].dt.month
    out = {}
    for y in (2025, 2026):
        out[y] = int(((x["when"].dt.year == y) & (m >= 7) & (m <= 10)).sum())
    return out


def monthly_counts(P):
    x = vi_incidents(P)
    k = x["when"].dt.year * 100 + x["when"].dt.month
    c = k.value_counts()
    months = [y * 100 + m for y in (2025, 2026) for m in range(1, 13) if y * 100 + m <= 202610]
    return [(ym, int(c.get(ym, 0))) for ym in months]


def incident_shifts(P):
    """Each vehicle interaction incident placed on its haul truck's dispatch shift (the truck named first in the
    register's vehicles, the shift that was running at the time, Western Australian time)."""
    x = vi_incidents(P).copy()
    x["truck_no"] = x["Vehicles"].astype(str).str.split(" / ").str[0].astype(object)
    d = P["disp"].copy()
    d["truck_no"] = d["truck_no"].astype(object)
    d["start"] = pd.to_datetime(d["shift_date"]) + pd.to_timedelta(np.where(d["shift"] == "DAY", 6, 18), unit="h")
    x = x.sort_values("when")
    m = pd.merge_asof(x, d.sort_values("start")[["start", "truck_no", "route", "shift"]], left_on="when", right_on="start",
                      by="truck_no", direction="backward", tolerance=pd.Timedelta(hours=12))
    return m, d


def route_rates(P):
    m, d = incident_shifts(P)
    out = {}
    for y in (2025, 2026):
        dm = pd.to_datetime(d["shift_date"])
        dd = d[(dm.dt.year == y) & (dm.dt.month >= 7) & (dm.dt.month <= 10)]
        mm = m[(m["when"].dt.year == y) & (m["when"].dt.month >= 7) & (m["when"].dt.month <= 10)]
        for rt, n in dd["route"].value_counts().items():
            out[(rt, y)] = (int((mm["route"] == rt).sum()), int(n))
        out[("night", y)] = (int((mm["shift"] == "NIGHT").sum()), int(len(mm)))
    return out


# ----------------------------------------------------------------------------------------------- the decisive read
def truck_of_unit(P):
    d = P["dev"]
    d = d[d["Device type"] == "Vehicle unit V3"].copy()
    d["truck"] = d["Asset"].str.replace("-", "", regex=False)
    d = d[d["truck"].str.startswith("DT")]
    return d


def crit_responses(P, slow=6.0, at=6, fallback=()):
    """Each critical alert on a haul truck unit, with the truck's speed change from the FMS window that opened on it
    and the unit's firmware at onset."""
    a = P["alerts"]
    a = a[a["alert_level"] == "CRIT"].copy()
    a["onset"] = pd.to_datetime(a["onset_utc"], format="%Y-%m-%dT%H:%M:%SZ")
    units = truck_of_unit(P)
    rows = []
    for _, u in units.iterrows():
        inst = pd.Timestamp(u["Installed"])
        rem = pd.Timestamp(u["Removed"]) if pd.notna(u["Removed"]) else pd.Timestamp("2100-01-01")
        sel = a[(a["unit_serial"] == u["Serial"]) & (a["onset"] + pd.Timedelta(hours=8) >= inst) &
                (a["onset"] + pd.Timedelta(hours=8) < rem)].copy()
        sel["truck"] = u["truck"]
        rows.append(sel)
    a = pd.concat(rows).sort_values("onset")
    a["local"] = a["onset"] + pd.Timedelta(hours=8)
    # firmware at onset
    fw = P["fw"].copy()
    fw["applied"] = pd.to_datetime(fw["Applied (UTC)"])
    fw = fw.sort_values("applied")
    a = pd.merge_asof(a.sort_values("onset"), fw[["Serial", "Version", "applied"]].rename(columns={"Serial": "unit_serial"}),
                      left_on="onset", right_on="applied", by="unit_serial", direction="backward")
    # FMS windows on critical alerts
    f = P["fms"]
    f = f[f["trigger"] == "CAS_CRITICAL"]
    piv = f.pivot_table(index=["event_ref", "truck_no", "trigger_time_awst"], columns="t_offset_s", values="speed_kmh",
                        aggfunc="first").reset_index()
    piv["tt"] = pd.to_datetime(piv["trigger_time_awst"], format="%Y-%m-%d %H:%M:%S")
    piv = piv.sort_values("tt")
    cols = ["truck", "tt", 0, at] + [c for c in fallback if c not in (0, at)]
    a = pd.merge_asof(a.sort_values("local"), piv.rename(columns={"truck_no": "truck"})[cols],
                      left_on="local", right_on="tt", by="truck", direction="forward", tolerance=pd.Timedelta(seconds=3))
    v = a[at]
    for c in fallback:
        v = v.fillna(a[c])
    a["v_at"] = v
    a["has_window"] = a["tt"].notna() & a[0].notna() & a["v_at"].notna()
    a["slowed"] = (a["v_at"] <= a[0] - slow)
    return a


def response_summary(a):
    w = a[a["has_window"]]
    fam = np.where(w["Version"].str.startswith("5"), "5.0.2", "4.3")
    out = {}
    for f in ("4.3", "5.0.2"):
        x = w[fam == f]
        out[f] = (float(x["slowed"].mean()), int(len(x)))
    inwin = w[(w["local"] >= ROLLOUT[0]) & (w["local"] < ROLLOUT[1])]
    famw = np.where(inwin["Version"].str.startswith("5"), "5.0.2", "4.3")
    out["window"] = {f: (float(inwin[famw == f]["slowed"].mean()), int((famw == f).sum())) for f in ("4.3", "5.0.2")}
    ym = w["local"].dt.year * 100 + w["local"].dt.month
    out["monthly"] = {int(k): float(v) for k, v in w.groupby(ym)["slowed"].mean().items()}
    return out


# ----------------------------------------------------------------------------------------------- ask A: gate trips
def gate_trips(P):
    g = P["gate"].copy()
    g["t"] = pd.to_datetime(g["read_time_awst"], format="%Y-%m-%d %H:%M:%S")
    g["gate"] = g["reader"].str[:2]
    g = g[g["direction"] == "IN"]
    trips = []
    s = g[g["reader"] == "SG-IN"]
    trips += [(t, tag) for t, tag in zip(s["t"], s["cas_tag"])]
    n = g[g["reader"].isin(["NG-1", "NG-2"])].sort_values(["t", "reader"])
    pending = None
    for t, reader, tag in zip(n["t"], n["reader"], n["cas_tag"]):
        if reader == "NG-1":
            if pending is not None:
                trips.append(pending)
            pending = (t, tag)
        else:
            if pending is not None and pd.Timedelta(seconds=2) <= t - pending[0] <= pd.Timedelta(seconds=13):
                trips.append(pending)
                pending = None
            else:
                if pending is not None:
                    trips.append(pending)
                    pending = None
                trips.append((t, tag))
    if pending is not None:
        trips.append(pending)
    out = {}
    for m in (7, 8, 9, 10):
        xs = [tg for t, tg in trips if t.month == m]
        out[m] = (len(xs), sum(1 for tg in xs if tg == ""))
    return out


# ----------------------------------------------------------------------------------------------- ask B: overspeed
def limit_in_force(P):
    lim = P["limits"].copy()
    lim["eff"] = pd.to_datetime(lim["effective_from"])

    def in_force(seg, day):
        x = lim[(lim["segment"] == seg) & (lim["eff"] <= day)].sort_values("eff")
        return float(x["limit_kmh"].iloc[-1])
    return in_force


def overspeed_windows(P):
    """One row per OVERSPEED window on the two ramps for a haul truck: its first, last and highest recorded speeds."""
    f = P["fms"]
    f = f[(f["trigger"] == "OVERSPEED") & f["segment"].isin(["NRP", "SRP"]) & f["truck_no"].str.startswith("DT")]
    g = f.groupby(["event_ref", "truck_no", "segment", "trigger_time_awst"])
    ev = g["speed_kmh"].max().rename("peak").reset_index()
    first = f[f["t_offset_s"] == f["t_offset_s"].min()].set_index("event_ref")["speed_kmh"]
    last = f[f["t_offset_s"] == f["t_offset_s"].max()].set_index("event_ref")["speed_kmh"]
    ev["first"] = ev["event_ref"].map(first)
    ev["last"] = ev["event_ref"].map(last)
    ev["tt"] = pd.to_datetime(ev["trigger_time_awst"], format="%Y-%m-%d %H:%M:%S")
    in_force = limit_in_force(P)
    ev["limit"] = [in_force(sg, t.normalize()) for sg, t in zip(ev["segment"], ev["tt"])]
    return ev.sort_values(["truck_no", "segment", "tt"]).reset_index(drop=True)


def overspeed_runs(ev, joins=None):
    """Windows into runs. A window continues the run before it when it opens on the sample that closed that run's last
    window (ten seconds after it, same truck and ramp) and the truck was still over the limit at that instant.
    `joins` replaces the rule with a plain gap in seconds (the reflex merges measured in checks.py)."""
    run_id, runs = [], -1
    prev = None
    for row in ev.itertuples():
        cont = False
        if prev is not None and row.truck_no == prev.truck_no and row.segment == prev.segment:
            gap = (row.tt - prev.tt).total_seconds()
            if joins is None:
                cont = gap == 10 and row.first > row.limit
            else:
                cont = gap <= joins
        if not cont:
            runs += 1
        run_id.append(runs)
        prev = row
    ev = ev.copy()
    ev["run"] = run_id
    return ev.groupby("run").agg(segment=("segment", "first"), tt=("tt", "first"), peak=("peak", "max"),
                                 limit=("limit", "first")).reset_index(drop=True)


def overspeed(P, joins=None):
    r = overspeed_runs(overspeed_windows(P), joins)
    r["over5"] = r["peak"] > r["limit"] + 5
    out = {}
    for seg in ("NRP", "SRP"):
        for m in (7, 8, 9, 10):
            x = r[(r["segment"] == seg) & (r["tt"].dt.year == 2026) & (r["tt"].dt.month == m)]
            out[(seg, m)] = (int(len(x)), int(x["over5"].sum()), [float(v - l) for v, l in zip(x["peak"], x["limit"])])
    return out
