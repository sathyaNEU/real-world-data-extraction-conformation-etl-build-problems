"""Assertion regime for task180. Run after build.py: python3 checks.py  (exit 1 on any failure)."""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

import golden as G

FAILS, PASSES = [], []
RESULTS = {}


def check(name, cond, detail=""):
    (PASSES if cond else FAILS).append((name, detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def lead(d):
    o = sorted(d, key=lambda k: -d[k])
    return o[0], d[o[0]], o[1], d[o[1]]


def rank_of(d, p):
    o = sorted(d, key=lambda k: -d[k])
    return o.index(p) + 1


def main():
    gold = G.solve()
    ref = gold["referrals"]
    RESULTS["golden"] = gold
    w, wv, r, rv = lead(ref)
    check("answer is Caithness", w == "CAI", str(ref))
    check("runner-up is Elgin", r == "ELG")
    check("answer margin >= 1.2x", wv / rv >= 1.2, f"{wv}/{rv}={wv / rv:.2f}")

    # rung 0: the filed screen on the mart's account totals ------------------------------------
    acct = G.referrals(grain="system")
    RESULTS["rung_account"] = acct
    a, av, a2, a2v = lead(acct)
    check("rung system (mart) names Elgin", a == "ELG", str(acct))
    check("rung account margin >= 1.2x", av / a2v >= 1.2, f"{av}/{a2v}")
    check("Caithness ranks 4th or 5th on the mart rung", rank_of(acct, "CAI") in (4, 5),
          f"rank {rank_of(acct, 'CAI')}")
    prem = G.referrals(grain="premises")
    RESULTS["rung_premises_summed"] = prem
    check("supplies summed to premises before screening names Elgin", lead(prem)[0] == "ELG", str(prem))
    check("premises-summed equals the mart rung", prem == acct)

    # the belief rung: past confirmation rate -----------------------------------------------------
    hist = gold["history"]
    rates = {p: v[2] for p, v in hist.items()}
    b, bv, b2, b2v = lead(rates)
    check("best past confirmation rate is Lochaber", b == "LOC", str(rates))
    check("Lochaber has the fewest referrals", min(ref, key=ref.get) == "LOC")
    check("Caithness does not lead the rate rung", b != "CAI")

    # grid cells ---------------------------------------------------------------------------------
    cells = {
        "supply_no_heating_exclusion": dict(use_heat=False),
        "supply_no_cot_exclusion": dict(use_cot=False),
        "system_no_cot_exclusion": dict(grain="system", use_cot=False),
        "system_no_heating_exclusion": dict(grain="system", use_heat=False),
        "primaries_only_from_reads": dict(related=False),
        "supply_no_exclusions": dict(use_cot=False, use_heat=False),
    }
    expect = {"supply_no_heating_exclusion": "SPY", "supply_no_cot_exclusion": "INV",
              "system_no_cot_exclusion": "INV", "system_no_heating_exclusion": "ELG",
              "primaries_only_from_reads": "ELG",
              "supply_no_exclusions": "INV"}
    for k, kw in cells.items():
        res = G.referrals(**kw)
        RESULTS[k] = res
        c, cv, c2, c2v = lead(res)
        check(f"cell {k} names {expect[k]}", c == expect[k], str(res))
        if k == "supply_no_exclusions":   # two filed rules skipped at once; only needs to miss the answer
            check(f"cell {k} misses Caithness", c != "CAI")
        else:
            check(f"cell {k} margin >= 1.2x", cv / c2v >= 1.2, f"{cv}/{c2v}={cv / c2v:.2f}")

    # convergence: readings that must not move the answer or any count -------------------------
    conv = {
        "hdd base 14C": dict(base=14.0), "hdd base 16.5C": dict(base=16.5),
        "gap booked to later week": dict(alloc="later"), "total only, not every week": dict(every_week=False),
        "count premises not supplies": dict(count="premises"), "prepayment left in": dict(credit_only=False),
        "threshold 0.25": dict(threshold=0.25), "threshold 0.33": dict(threshold=0.33),
    }
    for k, kw in conv.items():
        res = G.referrals(**kw)
        RESULTS["conv " + k] = res
        check(f"converges: {k}", res == ref, str(res) if res != ref else "")

    # history ask ladder ---------------------------------------------------------------------------
    stops = {"no dedupe": dict(dedupe=False), "no appeals": dict(appeals=False),
             "all visits as denominator": dict(access_only=False),
             "no dedupe, no appeals": dict(dedupe=False, appeals=False)}
    for k, kw in stops.items():
        h = G.history(**kw)
        RESULTS["history " + k] = h
        moved = [p for p in G.PATCH_ORDER if h[p] != hist[p]]
        check(f"history stop '{k}' moves figures", len(moved) >= 2 or k == "UTC dates", f"{len(moved)} patches move")

    # capacity ask ladder --------------------------------------------------------------------------
    days, cap, vpd = gold["officer_days"], gold["capacity"], gold["visits_per_day"]
    for k, kw in {"England and Wales holidays": dict(scotland=False),
                  "new officer counted all quarter": dict(honour_start=False),
                  "standby treated as leave": dict(standby_is_field=False)}.items():
        d2, c2, _ = G.capacity(**kw)
        RESULTS["capacity " + k] = d2
        check(f"capacity stop '{k}' differs", d2 != days, f"{d2} vs {days}")
    check("capacity never binds", all(cap[p] > 3 * ref[p] for p in G.PATCH_ORDER))
    check("visits per day not on an integer boundary",
          all(abs(450 / (70 + m) - round(450 / (70 + m))) > 0.04 for m in
              [12, 21, 26, 17, 33, 44, 39, 52]))

    # rates mid-bin -------------------------------------------------------------------------------
    for p, (acc, conf, rate) in hist.items():
        x = 100 * conf / acc * 10
        check(f"rate {p} not near a rounding edge", abs(x - np.floor(x) - 0.5) > 0.03, f"{100 * conf / acc:.4f}")

    # input gates -----------------------------------------------------------------------------------
    files = sorted(os.listdir(G.TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("10 or more files", len(files) >= 10, str(len(files)))
    check("3 or more formats", len(exts) >= 3, str(sorted(exts)))
    nreads = len(pd.read_parquet(os.path.join(G.TARGET, G.find("smart_daily_reads")), columns=["read_type"]))
    check("a file of 25,000+ rows", nreads >= 25_000, str(nreads))
    for f in files:
        check(f"no 'distractor' in {f}", "distractor" not in f.lower())
    # distractors unused: golden never opens them
    import inspect
    src = inspect.getsource(G)
    for dname in ("prepayment_vends", "dno_feeder_loss"):
        check(f"distractor {dname} unused by the golden", dname not in src)

    # separation: the ask files are never read by the referral screen
    rsrc = inspect.getsource(G.referrals) + inspect.getsource(G.load_exclusions) + \
        inspect.getsource(G.supply_weekly_from_reads)
    for f in ("fieldlink", "fieldops", "tamper_appeals", "rp_field_rota", "FW-3"):
        check(f"main screen never reads {f}", f not in rsrc)

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    with open(os.environ.get("T180_RESULTS", "/tmp/task180_checks.json"), "w") as fh:
        json.dump(RESULTS, fh, indent=1, default=str)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
