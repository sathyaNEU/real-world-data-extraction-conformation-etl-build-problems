"""task304 architecture 4: every figure the write-up and the goldens state, computed from target/ by analysis.py and
written to generator/figures.json (the single source for submission.md and the goldens)."""
import json
import os

import analysis as AN
import params as P


def compute(target):
    pk, tab, c, best, second = AN.golden(target)
    r0 = pk.rung_jobbased(tab)
    r1 = pk.rung_signed_on(tab)
    r2 = pk.rung_title_average(tab)
    vend = pk.vending()
    sts = pk.audiometry()
    hubs = AN.HUBS
    r0_best = max(hubs, key=lambda h: r0[h]["below"])
    r1_best = max(hubs, key=lambda h: r1[h]["below"])
    pool_best = max(hubs, key=lambda h: r0[h]["pool"])
    kew = tab[tab["site"] == best]
    F = {
        "hubs": hubs,
        "call_hub": best,
        "call_below": c[best]["below"],
        "runner_up": second,
        "runner_up_below": c[second]["below"],
        "pool": {h: c[h]["pool"] for h in hubs},
        "below": {h: c[h]["below"] for h in hubs},
        "workers": {h: c[h]["workers"] for h in hubs},
        "standard_db": P.STANDARD,
        "ref_start": "12 October", "ref_end": "8 November 2026",
        "default_hub": r0_best,
        "default_below": r0[r0_best]["below"],
        "default_call_hub_below": r0[best]["below"],
        "default_pool_hub": pool_best,
        "default_pool": r0[pool_best]["pool"],
        "r1_hub": r1_best,
        "r1_below": r1[r1_best]["below"],
        "r2_call_hub_below": r2[best]["below"],
        "best_lex_pre_median": round(float(kew[kew["pre"] >= 85]["pre"].median()), 1),
        "best_lex_post_median": round(float(kew[kew["pre"] >= 85]["post"].median()), 1),
        "best_induct_hours_median": round(float(kew[kew["pre"] >= 85]["t"].median()), 1),
        "levels": pk.levels,
        "pairs": {h: {str(m): int(vend.get((h, m), 0)) for m in (7, 8, 9)} for h in hubs},
        "sts": {h: int(sts[h]) for h in hubs},
        "seven_hour_post_call_hub": round(AN.lex(7.0, pk.levels[best]["Lp"], pk.levels[best]["Lf"], pk.levels[best]["La"]), 1),
        "clauses_cited": _clauses(target),
    }
    return F, pk, tab


def _clauses(target):
    """The undertaking's own numbers for the clauses the write-up cites, read from the schedule."""
    import re
    from io_util import pdf_text
    txt = " ".join(pdf_text(os.path.join(target, "noise_enforceable_undertaking_schedule_2027.pdf")).split())
    out = {}
    for key, opening in (("population", "The workers of a hub"), ("exposure", "A worker's exposure is")):
        m = re.search(r"(\d\.\d) " + re.escape(opening), txt)
        out[key] = m.group(1)
    return out


def write(target, path):
    F, pk, tab = compute(target)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    return F
