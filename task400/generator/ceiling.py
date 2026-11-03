"""The pair ceiling on the cut pack. Shares no code with the generator: it reads target/ and figures.json only.

The cracker lands the call (it reads each critical alert against the truck's speed and splits the alerts by the
unit's firmware), runs the hygiene battery and executes every filed statement, the prompt's two counted units
included: it reads the register's VI-COL and VI-SPI entries by month in Western Australian time; it counts one trip
per vehicle entering a pit, taking a vehicle read twice at one gate within 30 seconds under the same plate as one
entry; it keeps haul trucks' OVERSPEED windows on the two ramps, takes the limit in force on the day from the speed
limit schedule, and takes windows that abut in time on one truck and ramp (the next opening on or before the
moment the last one closed) as one continuous run. The mirror stops on the North ramp junction (programme B) and
handles the asks the same way.
"""
import hashlib
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
W_MAIN, W_IF, W_ASK = 38.0, 7.0, 55.0


def cracker_asks(t):
    out = {}
    g = pd.read_csv(os.path.join(t, "pit_gate_reads_2026-07_2026-10.csv"), keep_default_na=False)
    g = g[g["direction"] == "IN"].copy()
    g["t"] = pd.to_datetime(g["read_time_awst"])
    g = g.sort_values("t")
    last, keep = {}, []
    for tt, rd, pl in zip(g["t"], g["reader"], g["plate_read"]):
        k = (rd[:2], pl)
        keep.append(not (k in last and (tt - last[k]).total_seconds() <= 30))
        last[k] = tt
    g = g[keep]
    for m in (7, 8, 9, 10):
        x = g[g["t"].dt.month == m]
        out["trips_%02d" % m] = int(len(x))
        out["trips_notag_%02d" % m] = int((x["cas_tag"] == "").sum())
    f = pd.read_parquet(os.path.join(t, "fms_event_windows_2025-2026.parquet"))
    f = f[(f["trigger"] == "OVERSPEED") & f["segment"].isin(["NRP", "SRP"]) & f["truck_no"].str.startswith("DT")]
    ev = f.groupby(["event_ref", "truck_no", "segment", "trigger_time_awst"])["speed_kmh"].max().reset_index()
    ev["tt"] = pd.to_datetime(ev["trigger_time_awst"])
    lim = pd.read_csv(os.path.join(t, "haul_road_speed_limits.csv"))
    lim["eff"] = pd.to_datetime(lim["effective_from"])

    def in_force(seg, day):
        x = lim[(lim["segment"] == seg) & (lim["eff"] <= day)].sort_values("eff")
        return float(x["limit_kmh"].iloc[-1])
    ev["lim"] = [in_force(s, d.normalize()) for s, d in zip(ev["segment"], ev["tt"])]
    ev = ev.sort_values(["truck_no", "segment", "tt"]).reset_index(drop=True)
    gap = ev.groupby(["truck_no", "segment"])["tt"].diff().dt.total_seconds()
    ev["run"] = (~(gap <= 10)).cumsum()
    runs = ev.groupby("run").agg(segment=("segment", "first"), tt=("tt", "first"), peak=("speed_kmh", "max"),
                                 lim=("lim", "first"))
    for seg in ("NRP", "SRP"):
        for m in (7, 8, 9, 10):
            x = runs[(runs["segment"] == seg) & (runs["tt"].dt.year == 2026) & (runs["tt"].dt.month == m)]
            out["os_%s_%02d" % (seg, m)] = int(len(x))
            out["os5_%s_%02d" % (seg, m)] = int((x["peak"] > x["lim"] + 5).sum())
    return out


def main_side(t):
    reg = pd.read_excel(os.path.join(t, "incident_register_2025-01_2026-10.xlsx"), sheet_name="Register")
    vi = reg[reg["Classification"].isin(["VI-COL", "VI-SPI"])].copy()
    vi["when"] = pd.to_datetime(vi["Occurred"])
    n = {y: int(((vi["when"].dt.year == y) & vi["when"].dt.month.between(7, 10)).sum()) for y in (2025, 2026)}
    loc = vi[(vi["when"].dt.year == 2026) & vi["when"].dt.month.between(7, 10)]["Location code"].value_counts()
    # the mirror's stop: the 2026 hotspot, the notice's collision, the North waste route's traffic since June
    return {"vi_jul_oct_2025": n[2025], "vi_jul_oct_2026": n[2026], "mirror_call": "B" if loc.index[0] == "NRJ" else "?"}


def main():
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    zp = os.path.join(TASK, "target.zip")
    stamp = hashlib.md5(open(zp, "rb").read()).hexdigest()[:8] if os.path.exists(zp) else "no zip"
    ask_keys = sorted(k for k in figs if k.startswith(("trips", "os")))
    cr = cracker_asks(t)
    kept = [k for k in ask_keys if cr.get(k) == figs[k]]
    per_ask = {"A": [0, 0], "B": [0, 0]}
    for k in ask_keys:
        a = "A" if k.startswith("trips") else "B"
        per_ask[a][1] += 1
        per_ask[a][0] += k in kept
    ms = main_side(t)
    # the call side: the call, the two counts, the rollout weeks, the two response shares, the chart's bars and labels
    main_items = ["call", "vi_jul_oct_2025", "vi_jul_oct_2026", "rollout", "resp_43", "resp_5", "chart_bars", "chart_labels"]
    m_kept = ["chart_bars", "chart_labels"] + [k for k in ("vi_jul_oct_2025", "vi_jul_oct_2026") if ms[k] == figs[k]]
    cracker = W_MAIN + W_IF + W_ASK * len(kept) / len(ask_keys)
    mirror = W_MAIN * len(m_kept) / len(main_items) + W_IF + W_ASK * len(kept) / len(ask_keys)
    print("ceiling.py on %s (target.zip %s)" % (t, stamp))
    for a, (k, n) in per_ask.items():
        print("  ask %s cracker keeps %d of %d" % (a, k, n))
    for k in ask_keys:
        print("    %-14s golden %-6s cracker %s" % (k, figs[k], cr.get(k)))
    print("  mirror's call %s; main side keeps %d of %d: %s" % (ms["mirror_call"], len(m_kept), len(main_items),
                                                               ", ".join(m_kept)))
    print("  cracker %.1f, mirror %.1f, pair ceiling %.1f" % (cracker, mirror, (cracker + mirror) / 2))
    print("  mirror leakage %.1f per cent of ask weight" % (100.0 * len(kept) / len(ask_keys)))


if __name__ == "__main__":
    main()
