"""task161 cracker sheet: the pair ceiling measured on the built world (or the cut pack).

Two responses that land the call are scored on every ask criterion, and one that stops on a wrong
rung of the main call:
  C1  the cracker of supplemental-stumping 1.1: lands the call, runs the hygiene battery (so it
      collapses repeated box numbers), executes every filed definition, reads the pallet-level export
      for the off-rack count and counts no 53ft trailer as a port box (nothing files them as one);
  C2  a thorough solver beyond C1: also reconciles the pallet export to the nightly snapshot (so it
      finds the yard pallets) and reads the transload partner's manifest for the trailers' source
      boxes, but collapses repeated box numbers as the battery does;
  M   the mirror: stops on the per-account monthly fall (one block) and handles the asks as C1.
Weights follow supplemental-stumping Part 0: 38 for the call and its components, 7 for instruction
following, 55 spread over the 29 ask criteria (A1 four figures, A2 twenty, the chart five).

    python3 cracker.py            # runs on target/ when it exists, else on the in-memory world
"""
import os
import sys
import datetime as dt
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks       # noqa: E402
import records    # noqa: E402

W_CALL, W_INSTR, W_ASKS = 38.0, 7.0, 55.0
N_ASK = 29
R_WRONG = 5.0      # what a wrong call keeps of the 38


def load():
    target = os.path.join(os.path.dirname(HERE), "target")
    if os.path.isdir(target) and os.path.exists(os.path.join(HERE, "read.py")):
        import read
        return read.ask_inputs(target), "target/"
    import core
    import world as W
    Wd = core.build_world()
    site = {}
    for c, p in Wd["split_asof"].items():
        for s, v in records.site_totals(p).items():
            site[s] = site.get(s, 0) + v
    rec = [r for r in Wd["receipts"] if r["day"] >= dt.date(2022, 9, 12)]
    return {"site_onhand": site, "lpn": Wd["lpn"], "receipts": rec, "manifest": Wd["manifest"],
            "LA": Wd["LA"], "LB": Wd["LB"], "to_local": records.utc_to_pacific_date}, "in-memory world"


def score(inp):
    g1 = asks.a1_golden(inp["site_onhand"], inp["lpn"])
    teu, share = asks.a2_golden(inp["receipts"], inp["manifest"], inp["LA"], inp["LB"], inp["to_local"])
    gT = {k: int(round(v)) for k, v in teu.items()}
    gS = {k: round(v, 3) for k, v in share.items()}

    def a2(**kw):
        t, s = asks.a2_rows(inp["receipts"], inp["manifest"], inp["LA"], inp["LB"], inp["to_local"], **kw)
        return {k: int(round(v)) for k, v in t.items()}, {k: round(v, 3) for k, v in s.items()}

    paths = {
        "C1": {"a1": asks.a1_lpn_only(inp["lpn"]), "a2": a2(dedup="global", trailers="exclude")},
        "C2": {"a1": g1, "a2": a2(dedup="global", trailers="manifest")},
        "M": {"a1": asks.a1_lpn_only(inp["lpn"]), "a2": a2(dedup="global", trailers="exclude")},
    }
    out = {}
    for name, p in paths.items():
        a1_hits = sum(1 for s in asks.BUILDINGS if p["a1"][s] == g1[s])
        t_hits = sum(1 for k in asks.MONTHS_2026 if p["a2"][0][k] == gT[k])
        s_hits = sum(1 for k in asks.MONTHS_2026 if abs(p["a2"][1][k] - gS[k]) < 0.0005)
        # chart: one page, ten months in order, per-cent axis are structure; the bars' heights and
        # their TEU labels carry the figures, so they score only when every month's figures do
        chart = 3 + (1 if s_hits == 10 else 0) + (1 if t_hits == 10 else 0)
        hits = a1_hits + t_hits + s_hits + chart
        call = W_CALL if name != "M" else R_WRONG
        total = call + W_INSTR + W_ASKS * hits / N_ASK
        out[name] = {"a1": a1_hits, "teu": t_hits, "share": s_hits, "chart": chart, "hits": hits,
                     "kept": hits / N_ASK, "score": total}
    return out, g1, gT, gS


def main():
    inp, where = load()
    res, g1, gT, gS = score(inp)
    print("cracker sheet on the %s" % where)
    for name in ("C1", "C2", "M"):
        r = res[name]
        print("  %-3s A1 %d/4  A2 TEU %d/10  A2 share %d/10  chart %d/5  ask weight kept %.1f%%  score %.1f"
              % (name, r["a1"], r["teu"], r["share"], r["chart"], 100 * r["kept"], r["score"]))
    p1 = (res["C1"]["score"] + res["M"]["score"]) / 2
    p2 = (res["C2"]["score"] + res["M"]["score"]) / 2
    print("pair ceiling C1 with the mirror %.1f; C2 with the mirror %.1f; gated figure %.1f" % (p1, p2, max(p1, p2)))
    print("mirror leakage %.1f per cent of ask weight" % (100 * res["M"]["kept"]))
    return 0 if max(p1, p2) <= 40.0 else 1


if __name__ == "__main__":
    sys.exit(main())
