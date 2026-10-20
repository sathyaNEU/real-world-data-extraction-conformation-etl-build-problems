"""The ask layer measured on the cut pack: each ask path a response could take, the figures it keeps against the golden,
the cracker (on the call, hygiene battery, every filed rule executed on the fields it names) and the mirror (off the
call, the same care on the asks), and the pair ceiling.   python3 pair.py [target]   (--ladder prints the call's rungs)"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import routes as RT
import solve as S

TASK = os.path.dirname(HERE)


def ask_a_paths(target):
    rec = S.record(target)
    raw = pd.read_parquet(os.path.join(target, S.FILES["record"]))
    reg = pd.read_excel(os.path.join(target, S.FILES["register"])).set_index("station")
    log = pd.read_csv(os.path.join(target, S.FILES["log"]), keep_default_na=False)
    sw = log[log["visit"] == "sensor replaced"].set_index("station")
    end = pd.Timestamp("2027-01-01", tz="UTC")
    out = {k: {} for k in ("golden", "literal_letters", "any_flag", "register_sonde", "flagged_rows")}
    for code in sorted(rec["station"].unique()):
        r = S.station_series(rec, code)
        r = r[r.index < end]
        swap = pd.to_datetime("%s %s" % (sw.loc[code, "date"], sw.loc[code, "sonde_out"]),
                              format="%d.%m.%Y %H:%M").tz_localize("Europe/Oslo").tz_convert("UTC")
        miss = r["turbidity_fnu"].isna()
        fl = r["flag"].fillna("")
        ceil = (r.index < swap) & (r["turbidity_fnu"] >= 1000.0)
        h = lambda m: int(round(m.sum() / 4))
        out["golden"][code] = h(miss | fl.isin(["F", "M", "G", "O"]) | ceil)
        out["literal_letters"][code] = h(miss | fl.isin(["F", "M"]) | ceil)
        out["any_flag"][code] = h(miss | (fl != "") | ceil)
        out["register_sonde"][code] = h(miss | fl.isin(["F", "M", "G", "O"]) | (r["turbidity_fnu"] >= 4000.0))
        g = raw[(raw["station"] == code) & (raw["time_utc"] < end)]
        out["flagged_rows"][code] = int(round(g["flag"].isin(["F", "M", "G", "O"]).sum() / 4))
    return out


def ask_b_paths(target):
    out = {"golden": S.ask_b(target)[0],
           "export_nominal": S.ask_b(target, lots={"KS-26-11": 50.0, "KS-27-06": 50.0})[0]}
    return out


def score(path, golden):
    return sum(path[c] == golden[c] for c in golden)


def main(target):
    A = ask_a_paths(target)
    B = ask_b_paths(target)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    assert A["golden"] == fig["asks"]["hours_without_usable_reading"]
    assert B["golden"] == fig["asks"]["samples_in_failed_batches"]
    n = len(A["golden"]) + len(B["golden"])
    print("Ask A paths (stations kept of 14):")
    for k, v in A.items():
        print("  %-16s %2d" % (k, score(v, A["golden"])))
    print("Ask B paths (stations kept of 14):")
    for k, v in B.items():
        print("  %-16s %2d" % (k, score(v, B["golden"])))
    # the cracker: the filed letters F and M and the export's control column, as the fields name them
    kc = score(A["literal_letters"], A["golden"]) + score(B["export_nominal"], B["golden"])
    # the mirror: the same ask paths, off the call
    ks = kc
    lc, ls = kc / n, ks / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("cracker keeps %d of %d ask figures; mirror keeps %d" % (kc, n, ks))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % ((c + s) / 2, c, s, 100 * ls))
    if "--ladder" in sys.argv:
        tab = RT.all_routes(target)
        for r in RT.REFLEXES + RT.GOLDEN_FAMILY:
            print("  %-34s %s" % (r, RT.flagged(tab, r)))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else os.path.join(TASK, "target"))
