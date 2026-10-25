"""The 2026 performance tests: one announced test per scrubber between April and October, run by one of two
accredited laboratories on a day the boiler fires near its rating and the scrubber runs (a test is not started
on bypass). Concentrations are dry, at the laboratory's reference oxygen."""
import numpy as np

import world as W

LABS = {"Iverstow Emission Testing": 6.0, "Jarrness Stack Testing": 3.0}
LAB_OF = {"S01": "Iverstow Emission Testing", "S02": "Jarrness Stack Testing", "S03": "Iverstow Emission Testing",
          "S04": "Jarrness Stack Testing", "S05": "Jarrness Stack Testing", "S06": "Iverstow Emission Testing",
          "S07": "Iverstow Emission Testing", "S08": "Jarrness Stack Testing", "S09": "Iverstow Emission Testing",
          "S10": "Iverstow Emission Testing", "S11": "Jarrness Stack Testing", "S12": "Iverstow Emission Testing",
          "S13": "Jarrness Stack Testing", "S14": "Jarrness Stack Testing", "S15": "Iverstow Emission Testing",
          "S16": "Jarrness Stack Testing"}
VFG6 = 0.350  # Nm3 of dry flue gas at 6 per cent oxygen per MJ of gross heat input


def run(w):
    w.tests = []
    for b in w.B:
        rng = W.stream(41, *W.key(b))
        lab = LAB_OF[b["site"]]
        o2ref = LABS[lab]
        lo, hi = (112, 148) if b["role"] == "conc" else (95, 290)
        win = b["load"][lo:hi]
        hi_load = float(np.quantile(win[win > 0], 0.6))
        ok = [d for d in range(lo, hi) if b["load"][d] >= hi_load and b["off"][d] == 0 and W.day(d).weekday() < 5]
        d = int(rng.choice(ok))
        coal_h = b["coal_day"][d] / 24                      # t per hour
        gcv = b["gcv_day"][d]
        heat = coal_h * gcv * 1000                          # MJ per hour
        flow6 = heat * VFG6                                 # Nm3 per hour at 6 per cent O2, dry
        so2_in = b["S_gas_true"][d] / 24 * W.MSO2 / W.MS * 1e9 / flow6     # mg per Nm3 at 6 per cent
        eff = float(np.clip(b["eff_day"][d] + rng.normal(0, 0.0018), 0.88, 0.99))
        so2_out = so2_in * (1 - eff)
        k = (21 - o2ref) / 15.0
        o2_meas = float(np.round(rng.uniform(6.4, 8.2), 1))
        flow_ref = flow6 / k
        w.tests.append(dict(boiler=b["id"], site=b["site"], unit=b["unit"], lab=lab, o2ref=o2ref, day=d,
                            load=float(np.round(100 * b["load"][d], 0)), o2=o2_meas,
                            flow=float(np.round(flow_ref, -2)), so2_in=float(np.round(so2_in * k, 0)),
                            so2_out=float(np.round(so2_out * k, 0)), removal=float(np.round(100 * eff, 1)),
                            hours=float(np.round(rng.uniform(5.5, 7.5), 1))))
    return w.tests
