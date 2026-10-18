#!/usr/bin/env python3
"""task198 ask-layer measurement, solved on the cut pack.

    python3 task198/generator/asks_measure.py

Every figure here is read through verify.py's own bundle pipeline, so the ceiling is measured on
what ships rather than on the generator's truth. Two responses are scored on the generated rubric's
Part 0 weights (38 recommendation and critical components, 7 instruction-following, 55 asks), each
from its own readings, and both ask columns are printed:

  cracker  lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched
           joins, fan-out, count ties), executes every filed rule the pack points at and matches
           every control and published figure it carries.
  mirror   stops at the most attractive wrong rung, the load-per-staffed-position match, and does
           not run the battery.

Exit 0 when the pair is at or under 40 and the mirror's ask leakage under 35 per cent.
"""
import contextlib
import io
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_WRONG_CALL = 5.0


def pipeline():
    src = open(os.path.join(HERE, "verify.py")).read().split('print("\\n%d assertions')[0]
    ns = {"__name__": "asks", "__file__": os.path.join(HERE, "verify.py")}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "verify", "exec"), ns)
    return ns


def main():
    ns = pipeline()
    cases, crows, FEE = ns["cases"], ns["crows"], ns["FEE"]
    rrows, TRU, PARENT = ns["rrows"], ns["TRU"], ns["PARENT"]
    REG = {r[0]: (int(r[3]) if r[3] else 0) for r in rrows}
    fqtr = ns["fqtr"]

    # ---- ask 1, one figure, free by design: it sits in the call's own population
    g1 = {"FY2026 cases answered later than target": sum(1 for c in cases.values()
                                                         if c["fy"] == 2026 and c["late"])}
    n1 = dict(g1)   # both responses rebuild the metric, so both hold it

    # ---- ask 2, four figures: the chargeable cases the scheme charging covers
    def ask2(read):
        out = {}
        for r in crows:
            d = date.fromisoformat(r[1])
            y, q = fqtr(d)
            if y != 2026:
                continue
            per = 1 if d >= date(2025, 10, 1) else 0
            cov = round(float(r[5]) / FEE[r[3]][per]) if read == "cases" else 1
            k = "FY2026 Q%d chargeable cases covered" % q
            out[k] = out.get(k, 0) + cov
        return {k: out[k] for k in sorted(out)}
    g2, n2 = ask2("cases"), ask2("lines")

    # ---- ask 3, twenty figures: the ten largest participating schemes
    cnt = {}
    for c in cases.values():
        if c["fy"] != 2026:
            continue
        p = PARENT.get(c["scheme"], c["scheme"])
        cnt[p] = cnt.get(p, 0) + 1
    top = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:10]

    def ask3(src):
        out = {}
        for p, n in top:
            mem = TRU[p] if src == "trustee" else (REG[p] or TRU[p])
            out["%s active members" % p] = mem
            out["%s cases per 1,000" % p] = round(1000.0 * n / mem, 1)
        return out
    g3, n3 = ask3("trustee"), ask3("register")

    golden = {}
    golden.update(g1); golden.update(g2); golden.update(g3)
    units = {k: 0.05 for k in g1}
    units.update({k: 0.5 for k in g1})
    units.update({k: 0.5 for k in g2})
    for k in g3:
        units[k] = 0.5 if k.endswith("active members") else 0.05
    units.update({k: 0.5 for k in g1})

    cracker = {}; cracker.update(g1); cracker.update(g2); cracker.update(n3)
    mirror = {}; mirror.update(n1); mirror.update(n2); mirror.update(n3)

    print("task198 ask layer, solved on the CUT PACK, Part 0 weights "
          "(%.0f recommendation and components, %.0f instruction, %.0f asks)\n"
          % (W_REC, W_INSTR, W_ASK))
    print("A1 %d figure, A2 %d figures, A3 %d figures: %d graded ask figures"
          % (len(g1), len(g2), len(g3), len(golden)))

    keeps = {}
    for nm, resp in (("cracker", cracker), ("mirror", mirror)):
        per, kept = {}, []
        for k, g in golden.items():
            r = resp.get(k)
            ok = r is not None and abs(float(r) - float(g)) <= units[k]
            a = "A1" if k in g1 else ("A2" if k in g2 else "A3")
            per.setdefault(a, [0, 0])
            per[a][1] += 1
            if ok:
                per[a][0] += 1
                kept.append((k, g))
        keeps[nm] = len(kept)
        print("\n%-8s keeps %2d of %2d  (%s)" % (nm, len(kept), len(golden),
              ", ".join("%s %d/%d" % (a, v[0], v[1]) for a, v in sorted(per.items()))))
        for k, g in kept:
            print("           keeps  %-36s golden %s" % (k, g))

    Lc, Ls = keeps["cracker"] / len(golden), keeps["mirror"] / len(golden)
    C = W_REC + W_INSTR + W_ASK * Lc
    S = R_WRONG_CALL + W_INSTR + W_ASK * Ls
    pair = (C + S) / 2.0
    print("\n  cracker (lands the call) : %.1f  = %.0f + %.0f + %.0f x %.4f" % (C, W_REC, W_INSTR, W_ASK, Lc))
    print("  mirror  (stops at rung 2): %.1f  = %.0f + %.0f + %.0f x %.4f" % (S, R_WRONG_CALL, W_INSTR, W_ASK, Ls))
    print("  PAIR CEILING             : %.1f   (bar 40)" % pair)
    print("  MIRROR LEAKAGE           : %.1f per cent of ask weight   (bar 35)" % (100 * Ls))

    print("\nask device forcing, measured on the cut pack")
    print("  A2 bundled charge lines: %d lines against %d cases covered, a gap of %d on figures "
          "stated in whole cases" % (sum(n2.values()), sum(g2.values()),
                                     sum(g2.values()) - sum(n2.values())))
    for k in sorted(g2):
        print("     %-36s golden %5d   natural read %5d   gap %5d" % (k, g2[k], n2[k], g2[k] - n2[k]))
    grouped = [p for p, _ in top if (REG[p] or TRU[p]) != TRU[p]]
    print("  A3 grouped sponsor returns: %d of the %d largest carry a group figure" % (len(grouped), len(top)))
    gaps = []
    for p, n in top:
        gr, nr = round(1000.0 * n / TRU[p], 1), round(1000.0 * n / (REG[p] or TRU[p]), 1)
        gaps.append(abs(gr - nr))
        print("     %-9s cases %5d  golden %6.1f  register %6.1f  gap %6.1f" % (p, n, gr, nr, gr - nr))
    print("     smallest gap on a grouped scheme: %.1f per 1,000 against a 0.05 bin half-width"
          % min(g for g in gaps if g > 0))

    print("\nfigures the prompt's rounding sentence governs, and the precision each prints at")
    pr = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    print("  rounding sentence: %s" % pr.strip().split(". ")[-1].strip())
    print("  one decimal place: the call's breach share %.1f; %d scheme rates %s"
          % (ns["CALL_FIG"], len([k for k in g3 if k.endswith("per 1,000")]),
             ", ".join("%.1f" % g3[k] for k in sorted(g3) if k.endswith("per 1,000"))[:60] + " ..."))
    print("  whole counts, ungoverned: ask 1 %d; ask 2 %s; ten membership figures"
          % (g1["FY2026 cases answered later than target"],
             ", ".join(str(g2[k]) for k in sorted(g2))))

    allc = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    print("\ngraded-set boundary: tenth %s %d against eleventh %s %d, a gap of %d"
          % (allc[9][0], allc[9][1], allc[10][0], allc[10][1], allc[9][1] - allc[10][1]))

    ok = pair <= 40.0 and 100 * Ls < 35.0
    print("\n%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
