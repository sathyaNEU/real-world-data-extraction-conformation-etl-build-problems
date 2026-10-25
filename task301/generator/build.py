"""Cut the task301 pack from the world, the asks' records and the documents."""
import csv
import os

import numpy as np
import pandas as pd

import asks as A
import docs
import params as P
import world as Wd

FILES = P.FILES
PACK = list(FILES)
DISTRACTORS = ("terms", "datasheets")
CONTEXT = ("note",)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def build(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    W = Wd.world()
    days = W.days
    k0 = W.k0
    ds = [d.strftime("%Y-%m-%d") for d in days]
    # the register
    rows = []
    for nm, dc, comm, mod, pf, ws, amt, td, E0, N0 in P.SITES:
        lay = P.LAYOUT["KP" if nm == "Knowle Park" else mod]
        rows.append([nm, "operating", "%.1f" % dc, comm.isoformat(), P.MODN[mod], lay, E0, N0])
    for nm, dc, comm, mod, pf, ws, amt, td, E0, N0 in P.CAND:
        rows.append([nm, "candidate", "%.1f" % dc, "", P.MODN[mod], P.LAYOUT["KP"], E0, N0])
    _csv(F["register"], ["site", "status", "dc_capacity_mwp", "commissioned", "module", "mounting",
                         "centroid_easting", "centroid_northing"], rows)
    # the weather record: satellite-derived irradiation in the plane of the array and reanalysis rain, air temperature
    # and wind direction, one row a site a day
    rows = []
    for nm in P.OPERATING + P.CANDIDATES:
        S = W.site[nm]
        for i in range(len(days)):
            rows.append([ds[i], nm, "%.3f" % S["poa_sat"][i], "%.1f" % S["rain"][i], "%.1f" % S["temp"][i],
                         int(S["wind"][i])])
    _csv(F["weather"], ["date", "site", "poa_irradiation_kwh_m2", "rainfall_mm", "air_temperature_c", "wind_from_deg"], rows)
    # the fiscal meters
    rows = []
    for nm in P.OPERATING:
        ex = W.site[nm]["export"]
        for i in range(W.site[nm]["k_start"], len(days)):
            rows.append([ds[i], nm, "%.2f" % ex[i]])
    _csv(F["export"], ["date", "site", "export_mwh"], rows)
    # the inverter SCADA
    recs = {"date": [], "site": [], "inverter": [], "ac_energy_mwh": []}
    for nm in P.OPERATING:
        for b, B in enumerate(W.site[nm]["blocks"]):
            inv = "INV%02d" % (b + 1)
            for i in range(W.site[nm]["k_start"], len(days)):
                recs["date"].append(ds[i])
                recs["site"].append(nm)
                recs["inverter"].append(inv)
                recs["ac_energy_mwh"].append(round(float(B["energy"][i]), 3))
    sc = pd.DataFrame(recs)
    sc.to_parquet(F["scada"], index=False, engine="pyarrow", compression="snappy")
    # the layout: every block of every operating farm and every candidate's planned blocks
    rows = []
    for nm in P.OPERATING + P.CANDIDATES:
        S = W.site[nm]
        nb = len(S["blocks"])
        for b, B in enumerate(S["blocks"]):
            rows.append([nm, "INV%02d" % (b + 1), "%.3f" % (S["dc"] / nb), int(round(S["E0"] + B["x"])),
                         int(round(S["N0"] + B["y"]))])
    _csv(F["layout"], ["site", "inverter", "dc_mwp", "block_easting", "block_northing"], rows)
    # the environs
    env = Wd.environs()
    env.to_csv(F["environs"], index=False, lineterminator="\n")
    # the O&M log
    ev = sorted(W.events, key=lambda r: (r[0], P.OPERATING.index(r[1]), r[2]))
    _csv(F["omlog"], ["date", "site", "inverter", "event", "share_of_day_available"],
         [[d.isoformat(), s, i, e, "%.2f" % f] for d, s, i, e, f in ev])
    # the asks' records
    A.write(W, F, _csv)
    # the documents
    docs.write(W, F)
    return W
