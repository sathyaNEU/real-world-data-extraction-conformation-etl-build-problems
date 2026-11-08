"""task482 architecture 17: the golden. The main call from the generator's truth (checks.py and verify.py recompute
it from the shipped files), the asks' figures, and figures.json."""
import json
import os

import numpy as np

import core as C
import params as P
import rasch as RA
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def compute(w=None):
    w = w or W.world()
    pl = w["pool"]
    items = pl["items"]
    drafts = C.compose(pl)
    b_bank, _ = C.bank_run(w)
    b_gold, T = C.golden_b(w, b_bank)
    bank = C.marks(b_bank, drafts)
    gold = C.marks(b_gold, drafts)
    pick = C.pick(gold)
    dist = {d: abs(v - P.TARGET) for d, v in gold.items()}
    runner = sorted((x for x in dist if x != pick), key=lambda x: dist[x])[0]
    taught_n = {}
    resp = w["M"] > 0
    for i in pl["t3"]:
        taught_n[items[i]["code"]] = int((T[:, i] & resp[:, i]).sum())
    a = w["asks"]
    t3 = pl["t3"]
    untaught = 1.0 - (T[:, t3] & resp[:, t3]).sum() / resp[:, t3].sum()
    return dict(w=w, drafts=drafts, b_bank=b_bank, b_gold=b_gold, T=T, bank=bank, gold=gold, pick=pick,
                runner=runner, dist=dist, taught_n=taught_n, untaught_pct=int(round(100 * untaught)),
                taught_min=min(taught_n.values()), taught_max=max(taught_n.values()),
                t3_count={d: sum(1 for i in ix if items[i]["term"] == 3) for d, ix in drafts.items()},
                entered=a["entered"], sat=a["sat"], makeup_mean=a["makeup_mean"], makeup_n=a["makeup_n"],
                bank_pick=C.pick(bank))


def figures(res):
    f = {"call": "Paper " + res["pick"], "runner_up": "Paper " + res["runner"],
         "expected_achieved_mark": {d: int(round(v)) for d, v in res["gold"].items()},
         "expected_achieved_mark_2dp": {d: "%.2f" % v for d, v in res["gold"].items()},
         "distance_from_25_2dp": {d: "%.2f" % v for d, v in res["dist"].items()},
         "bank_expected_achieved_mark_2dp": {d: "%.2f" % v for d, v in res["bank"].items()},
         "bank_expected_achieved_mark": {d: int(round(v)) for d, v in res["bank"].items()},
         "term3_items": res["t3_count"],
         "achieved_ability": "%.2f" % P.THETA_ACHIEVED, "target": 25, "paper_marks": 50,
         "entered": res["entered"], "sat": res["sat"],
         "makeup_mean": {r: "%.1f" % v for r, v in res["makeup_mean"].items()},
         "makeup_candidates": res["makeup_n"],
         "taught_responses_min": res["taught_min"], "taught_responses_max": res["taught_max"],
         "untaught_share_pct": res["untaught_pct"],
         "entered_fmt": {r: "{:,}".format(v) for r, v in res["entered"].items()},
         "sat_fmt": {r: "{:,}".format(v) for r, v in res["sat"].items()},
         "entered_total": sum(res["entered"].values()), "sat_total": sum(res["sat"].values())}
    return f


def write_figures(res, path=os.path.join(HERE, "figures.json")):
    with open(path, "w") as fh:
        json.dump(figures(res), fh, indent=1, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    r = compute()
    write_figures(r)
    print(json.dumps(figures(r), indent=1, sort_keys=True))
