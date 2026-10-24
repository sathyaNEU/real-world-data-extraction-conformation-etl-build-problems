"""task279 independent verifier: recompute every graded figure from target/ with its own parsing and interpolation
(pandas-free, np.interp on the cumulative curves) and compare with generator/figures.json."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def run(task):
    tgt = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def f(name):
        return os.path.join(tgt, name)

    reg = list(csv.DictReader(open(f("meetpunten_veenmonitoring.csv"), encoding="utf-8")))
    s97 = {}
    rx = re.compile(r"^97-0412-\d{4}\s+(\S+)\s+(\d\d)-(\d\d)-(\d{4})\s+(\d+)\s*-\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+)")
    for ln in open(f("veenkernen_1997_bodemlab_wageveld.txt"), encoding="latin-1"):
        m = rx.match(ln)
        if m:
            g = m.groups()
            s97.setdefault(g[0], []).append((int(g[4]), int(g[5]), *[float(x.replace(",", ".")) for x in g[6:9]],
                                             dt.date(int(g[3]), int(g[2]), int(g[1]))))
    s24 = {}
    for r in csv.DictReader(open(f("lims_export_veenkernen_2024.csv"), encoding="utf-8"), delimiter=";"):
        s24.setdefault(r["point_code"], []).append((int(r["depth_top_cm"]), int(r["depth_bottom_cm"]),
                                                    float(r["dry_bulk_density_kg_m3"]) / 1000,
                                                    float(r["loi_550_pct_dm"].replace(",", ".")),
                                                    float(r["total_c_pct_dm"].replace(",", ".")),
                                                    dt.date.fromisoformat(r["sampling_date"])))

    def curves(rows):
        rows = sorted(rows)
        z = np.array([rows[0][0]] + [x[1] for x in rows], float)
        mass = np.array([x[2] * (x[1] - x[0]) * 10 for x in rows])
        ash = np.concatenate([[0], np.cumsum(mass * (1 - np.array([x[3] for x in rows]) / 100))])
        car = np.concatenate([[0], np.cumsum(mass * np.array([x[4] for x in rows]) / 100)])
        return z, ash, car, rows[0][5]

    unit_loss = {}
    for p in reg:
        z7, a7, c7, d7 = curves(s97[p["point_1997"]])
        z4, a4, c4, d4 = curves(s24[p["point_2024"]])
        zstar = np.interp(a7[-1], a4, z4)
        loss = (c7[-1] - np.interp(zstar, z4, c4)) * 10 / ((d4 - d7).days / 365.25)
        unit_loss.setdefault(p["unit_code"], []).append(loss)
    for c, v in unit_loss.items():
        x = float(np.floor(np.mean(v) * 10 + 0.5)) / 10
        if abs(x - fig["units"][c]["carbon_loss_t_c_ha_yr"]) > 1e-9:
            bad.append(("loss", c, x, fig["units"][c]["carbon_loss_t_c_ha_yr"]))
    first = sorted(unit_loss, key=lambda c: -np.mean(unit_loss[c]))[:3]
    if set(first) != set(fig["call"]["codes"]):
        bad.append(("call", first))
    # ask A
    rows = list(csv.DictReader(open(f("waterpassing_raster_1997_2024.csv"), encoding="utf-8")))
    by = {}
    for r in rows:
        by.setdefault((r["unit_code"], r["grid_point"]), {})[r["campaign"]] = r
    low = {}
    for (u, gp), d in by.items():
        if len(d) < 2:
            continue
        a, b = d["1997"], d["2024"]
        if np.hypot(float(a["x_rd"]) - float(b["x_rd"]), float(a["y_rd"]) - float(b["y_rd"])) > 1.0:
            continue
        yrs = (dt.date.fromisoformat(b["survey_date"]) - dt.date.fromisoformat(a["survey_date"])).days / 365.25
        low.setdefault(u, []).append((float(a["level_m"]) - 0.054 - float(b["level_m"])) * 1000 / yrs)
    for c, v in low.items():
        x = float(np.floor(np.mean(v) * 10 + 0.5)) / 10
        if abs(x - fig["units"][c]["surface_lowering_mm_yr"]) > 1e-9:
            bad.append(("lowering", c, x, fig["units"][c]["surface_lowering_mm_yr"]))
    # ask B
    meta = {r["dipwell_id"]: r for r in csv.DictReader(open(f("peilbuizen_metadata.csv"), encoding="utf-8"))}
    old = {}
    for r in csv.DictReader(open(f("peilbuizen_onderhoud.csv"), encoding="utf-8")):
        m = re.search(r"\(was ([\d.]+) m\)", r["note"])
        if r["action"] == "tube replaced" and m:
            old[r["dipwell_id"]] = (r["date"], float(m.group(1)))
    logger, hand = {}, {}
    for r in csv.DictReader(open(f("peilbuizen_reeksen_2014_2026.csv"), encoding="utf-8")):
        d = r["date_time"][:10]
        if d[8:10] in ("14", "28"):
            (logger if r["source"] == "logger" else hand)[(r["dipwell_id"], d)] = float(r["depth_below_tube_top_cm"])
    read = dict(hand)
    read.update(logger)
    glg = {}
    for dw, m in meta.items():
        yrs = []
        for y in range(2017, 2025):
            vals = []
            for (k_dw, day), v in read.items():
                if k_dw != dw or not (dt.date(y, 4, 1).isoformat() <= day <= dt.date(y + 1, 3, 31).isoformat()):
                    continue
                top = float(m["tube_top_above_surface_m"])
                if dw in old and day < old[dw][0]:
                    top = old[dw][1]
                vals.append(v - 100 * top)
            yrs.append(np.mean(sorted(vals)[-3:]))
        glg.setdefault(m["unit_code"], []).append(np.mean(yrs))
    for c, v in glg.items():
        x = int(np.floor(np.mean(v) + 0.5))
        if x != fig["units"][c]["glg_cm_below_surface"]:
            bad.append(("glg", c, x, fig["units"][c]["glg_cm_below_surface"]))
    print("verify: %s" % ("PASS" if not bad else "FAIL %s" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
