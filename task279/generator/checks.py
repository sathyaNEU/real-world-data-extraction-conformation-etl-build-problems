"""task279 checks: the three rules executed on the generator's clean truth (R1 to R3), the ladder's separation, the
licensed family, rounding margins, the asks' devices, the separation line, the input gates and the realism sweep.
Every failure prints and counts; run() returns the count."""
from __future__ import annotations

import csv
import os
import shutil
import tempfile

import numpy as np

import analysis as A
import common as K
import world as W

FAILS = []


def ok(label, cond, detail=""):
    print("%s  %-44s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def clean_routes(w):
    """Every route on the world's true slices, no laboratory error: the clean truth the client's rules run on."""
    out = {}
    for code, u in w.units.items():
        rs = []
        for pt in u["points"]:
            q = dict(pt)
            s97, s24 = pt["s97"], pt["s24"]
            bd97 = s97[:, 0] / (K.SLICE97 * 10.0)
            bd24 = s24[:, 0] / (K.SLICE24 * 10.0)
            q["m97"] = (bd97, 100 * (1 - s97[:, 1] / s97[:, 0]), 100 * s97[:, 2] / s97[:, 0])
            q["m24"] = (bd24, 100 * (1 - s24[:, 1] / s24[:, 0]), 100 * s24[:, 2] / s24[:, 0])
            rs.append(W.point_routes(q))
        out[code] = {k: float(np.mean([r[k] for r in rs])) for k in rs[0]}
    return out


def top3(units, key):
    return set(sorted(units, key=lambda c: -units[c][key])[:3])


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    rc = b["rc"]
    w = rc.w
    gold = set(fig["call"]["codes"])
    units = res["units"]
    print("== R1, R2, R3: the client's three rules on the clean truth")
    head24 = open(os.path.join(target, K.FILES["core24"]), encoding="utf-8").readline().lower()
    ok("R1 raw slices ship, no loss column", all(x in head24 for x in ("dry_bulk_density", "loi_550", "total_c"))
       and "loss" not in head24)
    shipped_cols = []
    for k, fn in K.FILES.items():
        if fn.endswith(".csv"):
            shipped_cols += open(os.path.join(target, fn), encoding="utf-8").readline().lower().split(",")
    ok("R1 no shipped column carries a carbon loss", not any("carbon_loss" in c or "c_loss" in c for c in shipped_cols))
    cl = clean_routes(w)
    ok("R3a ANALYST subsidence route files a wrong three", top3(cl, "subsidence") != top3(cl, "truth"),
       str(sorted(K.UNIT_NAME[c] for c in top3(cl, "subsidence"))))
    ok("R3a ANALYST level-aligned cores file a wrong three", top3(cl, "level") != top3(cl, "truth"),
       str(sorted(K.UNIT_NAME[c] for c in top3(cl, "level"))))
    ok("R3a ANALYST equal total mass files a wrong three", top3(cl, "mass") != top3(cl, "truth"),
       str(sorted(K.UNIT_NAME[c] for c in top3(cl, "mass"))))
    ok("R3b DECISIVE the ash anchor alone files the golden", top3(cl, "ash") == gold == top3(cl, "truth"),
       str(sorted(K.UNIT_NAME[c] for c in top3(cl, "ash"))))
    ok("R3b DECISIVE on the pack", top3(units, "ash") == gold)
    # R2: each Layer 1 item mishandled leaves the call where it was
    pts, c97, c24 = A.load(target)
    ok("R2 LAYER1 the 1997 printout parses whole (720 slices, 36 cores)",
       sum(len(v) for v in c97.values()) == 720 and len(c97) == 36)
    ok("R2 LAYER1 the LIMS export has one row a point and slice",
       len({(k, s["top"]) for k, v in c24.items() for s in v}) == sum(len(v) for v in c24.values()) == 468)
    near = {}
    for p in pts:
        d = [(np.hypot(float(p["x_rd_1996"]) - float(q["x_rd_2023"]), float(p["y_rd_1996"]) - float(q["y_rd_2023"])),
              q["point_2024"]) for q in pts]
        near[p["point_1997"]] = min(d)[1]
    ok("R2 LAYER1 pairing by position equals the crosswalk", all(near[p["point_1997"]] == p["point_2024"] for p in pts))
    ok("R2 LAYER1 the datum offset never reaches the call (golden reads no level)",
       top3(units, "ash") == gold)
    # ---------------------------------------------------------------------------------------------- ladder
    print("== the ladder on the pack")
    L = {k: A.ranking(units, k) for k in ("ash", "subsidence", "level", "mass", "fixed", "fixed_50", "ash_pchip",
                                          "subsidence_20", "subsidence_24")}
    comp = {c for c, r in W.ROLE_OF.items() if r in ("D", "A", "F3")}
    clay = {c for c, r in W.ROLE_OF.items() if r in ("C", "F2", "F6")}
    g1 = sorted(units, key=lambda c: -units[c]["ash"])[0]
    ok("LADDER golden line >= 1.30", L["ash"]["line"] >= 1.30, "%.3f" % L["ash"]["line"])
    for k, want in (("subsidence", comp), ("subsidence_20", comp), ("subsidence_24", comp), ("level", comp),
                    ("mass", clay)):
        ok("LADDER %s names its own three" % k, set(L[k]["top3"]) == want and not (set(L[k]["top3"]) & gold),
           "%s line %.2f" % (sorted(K.UNIT_NAME[c] for c in L[k]["top3"]), L[k]["line"]))
        ok("LADDER %s line >= 1.15" % k, L[k]["line"] >= 1.15, "%.3f" % L[k]["line"])
    ok("LADDER golden first is 4th or 5th on the subsidence route", L["subsidence"]["order"].index(g1) in (3, 4),
       "#%d" % (L["subsidence"]["order"].index(g1) + 1))
    ok("LADDER fixed depth never files the golden three", set(L["fixed"]["top3"]) != gold and
       set(L["fixed_50"]["top3"]) != gold)
    ok("FAMILY monotone cubic files the golden three", set(L["ash_pchip"]["top3"]) == gold)
    same = all(A.half_up(units[c]["ash"], 1) == A.half_up(units[c]["ash_pchip"], 1) for c in K.UNIT_CODES)
    ok("FAMILY every unit's figure rounds alike under both readings", same)
    # pooled per unit: one mean profile per unit, then the ash anchor
    pooled = {}
    for code in K.UNIT_CODES:
        mine = [p for p in pts if p["unit_code"] == code]
        e97, m97, a97, k97 = [np.mean([A.profile(c97[p["point_1997"]])[i] for p in mine], axis=0) for i in range(4)]
        e24, m24, a24, k24 = [np.mean([A.profile(c24[p["point_2024"]])[i] for p in mine], axis=0) for i in range(4)]
        yrs = np.mean([A.point_routes(p, c97[p["point_1997"]], c24[p["point_2024"]])["years"] for p in mine])
        z = A.depth_at(e24, a24, a97.sum())
        pooled[code] = {"x": (k97.sum() - A.amount_to(e24, k24, z)) * 10 / yrs}
    ok("FAMILY the unit-pooled profile files the golden three", top3(pooled, "x") == gold)
    # the semantic fork table, each row asserted
    ok("SF1 the 2024 top metre files another set", set(L["fixed"]["top3"]) != gold)
    ok("SF2 carbon above the 1997 base level files another set", set(L["level"]["top3"]) != gold)
    sf3 = {}
    for p in pts:
        r = A.point_routes(p, c97[p["point_1997"]], c24[p["point_2024"]])
        sf3.setdefault(p["unit_code"], []).append(r["ash"] * r["years"] / 27.0)
    ok("SF3 27 years for every point, same call", top3({c: {"x": np.mean(v)} for c, v in sf3.items()}, "x") == gold)
    ok("SF4 one pooled profile per unit, same call", top3(pooled, "x") == gold)
    sf5 = {}
    for p in pts:
        s97 = [dict(x, c=0.55 * x["loi"]) for x in c97[p["point_1997"]]]
        s24 = [dict(x, c=0.55 * x["loi"]) for x in c24[p["point_2024"]]]
        sf5.setdefault(p["unit_code"], []).append(A.point_routes(p, s97, s24)["ash"])
    ok("SF5 carbon as 0.55 of the loss on ignition, same call", top3({c: {"x": np.mean(v)} for c, v in sf5.items()},
                                                                      "x") == gold)
    ok("SF6 a monotone cubic, same call", set(L["ash_pchip"]["top3"]) == gold and same)
    mean_loss = np.mean([units[c]["ash"] for c in K.UNIT_CODES])
    ok("SF7 the units above the mean loss are the three", {c for c in K.UNIT_CODES if units[c]["ash"] > mean_loss} == gold)
    margin = min(abs(units[c]["ash"] * 10 - np.floor(units[c]["ash"] * 10) - 0.5) for c in K.UNIT_CODES) / 10
    ok("ROUNDING every unit's loss clears its rounding boundary", margin > 0.004, "%.4f" % margin)
    # --------------------------------------------------------------------------------------------- the asks
    print("== the asks")
    low_g = A.ask_lowering(target)
    low_m = A.ask_lowering(target, None)
    low_n = A.ask_lowering(target, 1.0, 0.0)
    ok("ASK A primary moves every unit by >= 0.3 mm/yr", all(abs(low_g[c] - low_m[c]) >= 0.3 for c in K.UNIT_CODES),
       "min %.2f" % min(abs(low_g[c] - low_m[c]) for c in K.UNIT_CODES))
    ok("ASK A the datum offset moves every unit by >= 1.5", all(abs(low_g[c] - low_n[c]) >= 1.5 for c in K.UNIT_CODES))
    grid = rc.grid()
    d_moved = [np.hypot(g["x97"] - g["x24"], g["y97"] - g["y24"]) for g in grid if g["moved"]]
    d_same = [np.hypot(g["x97"] - g["x24"], g["y97"] - g["y24"]) for g in grid if not g["moved"] and not g["lost"]]
    ok("ASK A forcing: re-shot points stand >= 10 m off, all others <= 1 m", min(d_moved) >= 10 and max(d_same) <= 1,
       "moved %.1f to %.1f m, others max %.2f m" % (min(d_moved), max(d_moved), max(d_same)))
    glg_g, _ = A.ask_glg(target)
    glg_m, _ = A.ask_glg(target, tube_history=False)
    glg_n, _ = A.ask_glg(target, hand_fill=False)
    ok("ASK B primary moves every unit by >= 2 cm", all(abs(glg_g[c] - glg_m[c]) >= 2 for c in K.UNIT_CODES),
       "min %.1f" % min(abs(glg_g[c] - glg_m[c]) for c in K.UNIT_CODES))
    gap_units = [c for c in K.UNIT_CODES if abs(glg_g[c] - glg_n[c]) >= 0.5]
    ok("ASK B the logger gap moves its unit", len(gap_units) >= 1, str(gap_units))
    ok("ASK rounding margins", all(abs(low_g[c] * 10 - np.floor(low_g[c] * 10) - 0.5) > 0.02 for c in K.UNIT_CODES)
       and all(abs(glg_g[c] - np.floor(glg_g[c]) - 0.5) > 0.05 for c in K.UNIT_CODES))
    # separation: the call with the ask files gone
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in (K.FILES["grid"], K.FILES["dw_series"], K.FILES["dw_meta"], K.FILES["dw_maint"]):
                shutil.copy(os.path.join(target, f), tmp)
        _, u2 = A.routes(tmp)
        ok("SEPARATION the call without the ask files", top3(u2, "ash") == gold and
           all(abs(u2[c]["ash"] - units[c]["ash"]) < 1e-12 for c in K.UNIT_CODES))
    finally:
        shutil.rmtree(tmp)
    # --------------------------------------------------------------------------------------- gates, realism
    print("== input gates and realism")
    files = os.listdir(target)
    ok("GATE ten or more files", len(files) >= 10, str(len(files)))
    ok("GATE three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8", errors="ignore"))
              for f in files if f.endswith(".csv"))
    ok("GATE a file of 25,000 rows", big >= 25000, str(big))
    ok("GATE two or more distractors", len(K.DISTRACTORS) >= 2)
    n_grid = {}
    for g in grid:
        n_grid[g["unit"]] = n_grid.get(g["unit"], 0) + 1
    ok("REALISM grid sizes differ across units", len(set(n_grid.values())) >= 6, str(sorted(n_grid.values())))
    vals = [r[3] for r in rc.dipwell_series_rows()[1][:5000]]
    ok("REALISM no constant dipwell stream", len(set(vals)) > 500)
    losses = [fig["units"][c]["carbon_loss_t_c_ha_yr"] for c in K.UNIT_CODES]
    ok("REALISM losses within the drained-peat range", 1.0 < min(losses) and max(losses) < 9.0, str(losses))
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)
