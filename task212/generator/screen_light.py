"""Twenty-redraw screen of the key readers on the generator's world (python3 screen_light.py N OUTFILE)."""
import sys
from multiprocessing import Pool
import numpy as np
import pandas as pd
import world, records, analysis as A


def one(seed):
    w = world.simulate(seed)
    rec = records.cut(w, seed)
    t = A.base_table(rec, w["accounts"])
    box = (t["dshape"] == "BOX").astype(float); bag = (t["dshape"] == "BAG").astype(float); hv = t.heavyp.astype(float)
    out = {"first_look": t.groupby("hubk").dam.mean() * 1e4}
    out["e_literal"], _ = A.oe(t, A._X(t))
    ex = {"fill": t.groupby("cage_label").barcode.transform("size").astype(float), "box_lkg": box * t.lkg}
    out["c_perrecord"], _ = A.oe(t, A._X(t, ex))
    exd = {"ch": t.cage_heavy, "cw": t.cage_kg / 50, "box_ch": box * t.cage_heavy, "box_cw": box * t.cage_kg / 50}
    out["d_mechanism"], _ = A.oe(t, A._X(t, exd))
    exb = {"fa": t.frac_after, "cw": t.cage_kg / 50, "fa_cw": t.frac_after * t.cage_kg / 50, "box_fa": box * t.frac_after,
           "box_fa_cw": box * t.frac_after * t.cage_kg / 50}
    out["b_constructing"], _ = A.oe(t, A._X(t, exb))
    decl = rec["manifests"].set_index("barcode").declared_kg
    la2 = t.barcode.map(A.crush_load(rec["scans"], decl).load_above)
    out["d2_declared"], _ = A.oe(t, A._X(t, {"f": la2 / 50, "box_f": box * la2 / 50, "bag_f": bag * la2 / 50}))
    out["g_cells_T60"] = A.cells_oe(t.assign(ls=(t.load_above >= 60).astype(int), fr=t.fragile), ["dshape", "wband", "fr", "ls"])
    ind = (t.load_above >= 60).astype(float)
    out["g_logit_ind"], _ = A.oe(t, A._X(t, {"f": ind, "box_f": box * ind, "bag_f": bag * ind, "hv_f": hv * ind}))
    f = np.log1p(t.load_above)
    out["g_logit_log"], _ = A.oe(t, A._X(t, {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}))
    f = t.load_above / 50
    out["g_logit_lin"], _ = A.oe(t, A._X(t, {"f": f, "box_f": box * f, "bag_f": bag * f, "hv_f": hv * f}))
    df = pd.DataFrame(out)
    return seed, A.summarise(df).set_index("reader")[["pick", "second", "lead", "top"]], float(df.loc["VLC", "g_cells_T60"])


if __name__ == "__main__":
    n = int(sys.argv[1])
    with Pool(4) as p:
        res = p.map(one, [3000 + i for i in range(n)])
    lines = []
    for c in res[0][1].index:
        picks = pd.Series([r[1].loc[c, "pick"] for r in res]).value_counts().to_dict()
        secs = pd.Series([r[1].loc[c, "second"] for r in res]).value_counts().to_dict()
        leads = [r[1].loc[c, "lead"] for r in res]
        lines.append("%-15s picks %s second %s min-lead %.2f" % (c, picks, secs, min(leads)))
    lines.append("VLC g_cells_T60 per 10,000 over redraws: " + ", ".join("%.1f" % r[2] for r in res))
    open(sys.argv[2], "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
