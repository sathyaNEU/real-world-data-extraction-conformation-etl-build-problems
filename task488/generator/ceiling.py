"""The pair ceiling on the cut pack (supplemental-stumping Parts 0, 1.1 and 5), every figure read by solve.py from
target/ alone. The cracker lands the call (the per-segment front) and takes the careful route on the refuellers: each
tank mixed, the rack line carried, but Northgarth's tractor tickets keyed to the equipment register's usual trailer
and the RF-23 transfer, which only Corbel's equipment log records, not booked. The mirror stops at rung 0 (one line
fill through the pump station's meter) and reads the refuellers the cracker's way with the rack by its line-up times.
Each figure is a hit when it equals the golden at the prompt's rounding; planning weights 38 / 7 / 55, the refuellers
to drain counted in the call (each named and the rest clear) and their litres, uplifts and airline litres in the asks.

    python3 task488/generator/ceiling.py [target_dir]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import solve as S   # noqa: E402

CRACKER = "the equipment register's pairing, the transfer unbooked, the rack line carried"


def ask_figures(rf):
    held = {k: S.rnd(v, 10) for k, v in rf["held"].items() if v > 0}
    air = {}
    for key, (b, airline, *_r) in rf["delivered"].items():
        air[airline] = air.get(airline, 0) + b
    air = {k: S.rnd(v, 10) for k, v in air.items()}
    return held, len(rf["delivered"]), air


def rows(gold, other):
    gh, gn, ga = gold
    oh, on, oa = other
    out = []
    for k in sorted(gh):
        out.append(("A: %s batch litres" % k, oh.get(k, 0), gh[k]))
    out.append(("B: refueller uplifts that delivered batch fuel", on, gn))
    for k in sorted(set(ga) | set(oa)):
        out.append(("C: %s" % k, oa.get(k, 0), ga.get(k, 0)))
    return out


def main(target):
    gold_rf = S.refuellers(target)
    crack_rf = S.refuellers(target, pairing="register", transfer=False)
    mirror_rf = S.refuellers(target, pairing="register", transfer=False, header=False)
    g, cr, mi = ask_figures(gold_rf), ask_figures(crack_rf), ask_figures(mirror_rf)
    crows, mrows = rows(g, cr), rows(g, mi)
    print("| Ask figure | Cracker (%s) | Golden | Cracker |" % CRACKER)
    print("|---|---|---|---|")
    kept_c = 0
    for name, got, want in crows:
        hit = got == want
        kept_c += hit
        fmt = lambda v: "{:,}".format(v) if isinstance(v, int) else v
        print("| %s | %s | %s | %s |" % (name, fmt(got), fmt(want), "hit" if hit else "miss"))
    kept_m = sum(1 for _, got, want in mrows if got == want)
    n = len(crows)
    hy = S.hydrant(target)
    r0 = S.reckoning(target, hy)
    gold_sections = sorted(s for s, v in hy["standing"].items() if v > 0)
    gold_litres = {s: S.rnd(hy["standing"][s], 100) for s in gold_sections}
    # the main call's criteria: each holding section named, the other sections clear, each holding section's litres,
    # the hydrant uplifts that took the batch; each refueller to drain named and the other refuellers clear (the
    # refuellers are part of the call: the prompt asks where the batch stands refueller by refueller)
    gold_tanks = sorted(g[0])

    def tank_hits(view):
        held = set(view[0])
        return sum(1 for k in gold_tanks if k in held) + (1 if held <= set(gold_tanks) else 0)
    main_n = len(gold_sections) * 2 + 2 + len(gold_tanks) + 1
    mirror_sections = []                       # the reckoning clears the whole hydrant by the suspension
    m_main = sum(1 for s in gold_sections if s in mirror_sections) * 2 + (1 if not mirror_sections else 0) \
        + (1 if r0["uplifts"] == len(hy["took"]) else 0) + tank_hits(mi)
    c_main = len(gold_sections) * 2 + 2 + tank_hits(cr)
    r = 38.0 * m_main / main_n
    rc = 38.0 * c_main / main_n
    lc, lm = kept_c / float(n), kept_m / float(n)
    crk = rc + 7 + 55 * lc
    mir = r + 7 + 55 * lm
    print()
    print("asks: the cracker keeps %d of %d ask figures, the mirror %d of %d" % (kept_c, n, kept_m, n))
    print("main call: golden %s (%s), %d hydrant uplifts and refuellers %s; the cracker keeps %d of %d call criteria "
          "(it misses RF-24); the mirror clears the hydrant at %s, notifies %d and names %s, keeping %d of %d"
          % (", ".join(gold_sections), ", ".join("%s %s L" % (s, "{:,}".format(v)) for s, v in gold_litres.items()),
             len(hy["took"]), ", ".join(gold_tanks), c_main, main_n, r0["edges"][1].strftime("%H:%M"), r0["uplifts"],
             ", ".join(sorted(mi[0])), m_main, main_n))
    print("Pair ceiling: %.1f (cracker %.1f on the hydrant call, mirror %.1f off it; call shares %.2f and %.2f)"
          % ((crk + mir) / 2, crk, mir, rc, r))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    return {"pair": (crk + mir) / 2, "cracker": crk, "mirror": mir, "leak": 100 * lm, "kept_c": kept_c, "n": n,
            "rows": crows}


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
