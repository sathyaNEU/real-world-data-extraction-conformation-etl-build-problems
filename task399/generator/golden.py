"""The golden: every graded figure from the clean truth into generator/figures.json, then the two deliverables
(remand_gap_drill.xlsx and remand_gap_briefing.pdf) into <task>/golden, built from those figures alone."""
import json
import os

import figs as F
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CALL = "Duty lawyer roster: a second rostered duty lawyer at Kestrel Bay District Court on every sitting day"
LEVEL1 = ["region_gap_2025", "region_gap_2026"] + ["gap_%s_%s" % (c, y) for c in W.COURTS for y in ("2025", "2026")]
LEVEL2 = ["kb_avl_gap", "kb_other_gap", "kb_avl_mag_gap", "kb_avl_judges_gap", "kb_other_mag_gap",
          "kb_other_judges_gap", "kb_avl_unrepresented"]


def figures(w):
    f = F.main_figures(w["first"])
    out = {k: (round(v, 6) if isinstance(v, float) else v) for k, v in f.items()}
    em = F.em_month_means(w["em"])
    bh = F.bh_month_nights(w["bh_place"], w["bh_abs"])
    for (y, m), v in em.items():
        out["em_%d_%02d" % (y, m)] = round(v, 6)
    for (y, m), v in bh.items():
        out["bh_%d_%02d" % (y, m)] = int(v)
    units = {k: 0.1 for k in F.GRADED_MAIN}
    units["kb_avl_unrepresented"] = 1
    units.update({k: 0.1 for k in out if k.startswith("em_")})
    units.update({k: 1 for k in out if k.startswith("bh_")})
    out["_units"] = units
    out["_critical"] = LEVEL1 + LEVEL2
    out["_default_path_same"] = LEVEL1
    out["call"] = CALL
    out["em_orders_p2"] = int(((w["em"].order_date >= W.P2_START) & (w["em"].order_date <= W.END)).sum())
    return out


def write_figures(w):
    out = figures(w)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    return out
