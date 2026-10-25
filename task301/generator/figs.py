"""figures.json: every figure the write-up and the goldens state, computed once from the pack."""
import json
import os

import numpy as np
import pandas as pd

import params as P
import solve as SV


def r100(x):
    return int(round(x / 100.0) * 100)


def compute(target):
    K = SV.Pack(target)
    c = SV.call(K)
    gold = c["gold"]
    order = sorted(SV.CANDS, key=lambda k: -gold[k])
    win = order[0]
    fam = SV.family(K)
    loss_lo, loss_hi = min(r[4] for r in fam), max(r[4] for r in fam)
    hd_clean = c["clean"]["Hallam Down"]
    a = SV.ask_a(K)
    b = SV.ask_b(K)
    near = c["near"]
    corner = near.sort_values("d").head(3)
    L = SV.block_distances(K, "Hallam Down")
    rain = K.w.groupby("site").rainfall_mm.sum() / 10.0
    wex = K.lay[K.lay.site == "Wexcombe"]
    lo, hi = c["wash"][0][1], c["wash"][0][2]
    F = {
        "call_site": win,
        "call_export_mwh": r100(gold[win]),
        "export_mwh": {k: r100(gold[k]) for k in SV.CANDS if k != "Hallam Down"},
        "irradiation_kwh_m2": {k: int(round(SV.avg_year_poa(K, k))) for k in SV.CANDS},
        "energised": {k: v.isoformat() for k, v in SV.ENERGISED.items()},
        "hallam_clean_export_mwh": r100(hd_clean),
        "hallam_export_mwh": r100(gold["Hallam Down"]),
        "hallam_export_range_mwh": [r100(hd_clean * (1 - loss_hi)), r100(hd_clean * (1 - loss_lo))],
        "hallam_loss_pct": round(100 * c["loss"], 1),
        "hallam_loss_range_pct": [round(100 * loss_lo, 1), round(100 * loss_hi, 1)],
        "hallam_loss_whole_pct": [int(np.floor(100 * loss_lo)), int(np.ceil(100 * loss_hi))],
        "hallam_lead_pct": round(100 * c["lead"], 1),
        "hallam_blocks": int(len(L)),
        "hallam_block_range_m": [int(round(L.d.min())), int(round(L.d.max()))],
        "hallam_rain_mm": int(round(rain["Hallam Down"] / 10.0) * 10),
        "wexcombe_rain_mm": int(round(rain["Wexcombe"] / 10.0) * 10),
        "knowle_ratio": round(c["pr_kp"], 3),
        "knowle_ratio_2dp": round(c["pr_kp"], 2),
        "fleet_degradation_pct": round(100 * c["deg"], 2),
        "wexcombe_blocks": int(len(wex)),
        "wexcombe_near_blocks": int((near.d < 320).sum()),
        "corner_blocks": [[i, int(round(r.d)), round(100 * (1 - r.rel), 1)] for i, r in corner.iterrows()],
        "corner_range_m": [int(round(corner.d.min())), int(round(corner.d.max()))],
        "corner_loss_range_pct": [round(100 * (1 - corner.rel.max()), 1), round(100 * (1 - corner.rel.min()), 1)],
        "build_mwp": P.BUILD_MWP,
        "knowle_mwp": float(K.dc["Knowle Park"]),
        "knowle_start": "%d January 2024" % K.comm["Knowle Park"].day,
        "wash_keep_pct": [int(round(100 * SV.WASH_LO)), int(round(100 * SV.WASH_HI))],
        "deposit_cap_pct": int(round(100 * SV.CAP)),
        "far_ref_m": 450,
        "near_m": 320,
        "wash_mm": [int(lo), int(hi)],
        "wexcombe_meter_vs_peers_pct": round(100 * (c["farm_ratio"] - 1), 1),
        "ask_a": {f: round(v["gold"], 3) for f, v in a.items()},
        "ask_a_days": {f: int(v["days"]) for f, v in a.items()},
        "ask_a_swap": {},
        "ask_b": {f: round(v["gold"], 1) for f, v in b.items()},
        "ask_b_alarms": {f: int(v["n"]) for f, v in b.items()},
    }
    reg = pd.read_csv(os.path.join(target, "pyranometer_register.csv"))
    F["ask_a_swap"] = dict(zip(reg.site, reg.installed))
    F["ask_a_down"] = {f: v["down"] for f, v in a.items()}
    F["ask_a_up"] = dict(zip(reg.site, reg.sensor_serial))
    return F, dict(call=c, fam=fam, a=a, b=b, K=K)


def write(target, path):
    F, _ = compute(target)
    with open(path, "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=False)
    return F


if __name__ == "__main__":
    import sys
    print(json.dumps(compute(sys.argv[1])[0], indent=1))
