"""The five go/no-go screens over redraws of the clean truth (python3 screens.py N OUT.json [first_seed]).

Each redraw is a fresh world and record cut; every reader and every golden-family member runs on the record tables.
"""
import json
import os
import sys
from multiprocessing import Pool
import numpy as np
import pandas as pd
import world
import records
import analysis as A


def one(seed):
    w = world.simulate(seed)
    rec = records.cut(w, seed)
    t = A.base_table(rec, w["accounts"])
    if os.environ.get("FIT_ONLY"):
        ft = A.fit_table(t, rec)
        b = ft.bic.idxmin()
        H = ["ZAZ", "VLC", "SVQ", "MAD", "BCN", "BIO"]
        return {"seed": seed, "bic_best": b, "bic_pick": ft.loc[b, H].astype(float).idxmax(),
                "vlc": round(float(ft.loc[b, "VLC"]), 2),
                "bic_gap_log1p": round(float(ft.loc["load_log1p", "bic"] - ft.loc[b, "bic"]), 1),
                "bic_gap_sink": round(float(ft.loc["load_step60_plus_constructing", "bic"] - ft.loc[b, "bic"]), 1),
                "bic_gap_rival": round(float(ft[ft.index.str.startswith("rival")].bic.min() - ft.loc[b, "bic"]), 1)}
    r = A.readers(t, rec)
    par = w["parcels"]
    r["truth_equip"] = par.groupby("hub").apply(lambda d: (d.p_true - d.p_noequip).sum() / len(d) * 1e4)
    sm = A.summarise(r).set_index("reader")
    wr, wr_lead = A.wrong_reason(r)
    return {"seed": seed, "pick": sm.pick.to_dict(), "lead": sm.lead.to_dict(), "second": sm.second.to_dict(),
            "vlc": r.loc["VLC"].round(2).to_dict(), "wrong_reason": wr, "wrong_reason_lead": round(wr_lead, 2),
            "fits": A.fits(t)}


def tally(res):
    readers = list(res[0]["pick"].keys())
    out = {}
    for k in readers:
        picks = pd.Series([x["pick"][k] for x in res]).value_counts().to_dict()
        leads = [x["lead"][k] for x in res]
        out[k] = {"picks": picks, "min_lead": float(min(leads)), "median_lead": float(np.median(leads))}
    out["wrong_reason"] = {"picks": pd.Series([x["wrong_reason"] for x in res]).value_counts().to_dict(),
                           "min_lead": float(min(x["wrong_reason_lead"] for x in res))}
    return out


if __name__ == "__main__":
    n = int(sys.argv[1])
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    with Pool(int(os.environ.get("SCREEN_WORKERS", "2")), maxtasksperchild=1) as p:
        res = p.map(one, [first + i for i in range(n)])
    if os.environ.get("FIT_ONLY"):
        with open(sys.argv[2], "w") as f:
            json.dump({"runs": res}, f, indent=1, default=str)
        print("lowest-BIC picks", pd.Series([r["bic_best"] for r in res]).value_counts().to_dict(),
              "hub", pd.Series([r["bic_pick"] for r in res]).value_counts().to_dict(),
              "min gaps log1p %.1f sink %.1f rival %.1f" % (min(r["bic_gap_log1p"] for r in res),
                                                             min(r["bic_gap_sink"] for r in res),
                                                             min(r["bic_gap_rival"] for r in res)))
        sys.exit(0)
    out = {"runs": res, "tally": tally(res)}
    with open(sys.argv[2], "w") as f:
        json.dump(out, f, indent=1, default=str)
    for k, v in out["tally"].items():
        print("%-22s %s min-lead %.2f" % (k, v["picks"], v["min_lead"]))
