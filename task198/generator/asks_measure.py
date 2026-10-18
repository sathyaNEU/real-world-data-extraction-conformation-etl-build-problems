#!/usr/bin/env python3
"""task198 ask-layer measurement: solves the pair ceiling rather than asserting one.

    python3 task198/generator/asks_measure.py

Scores two responses on the generated rubric's Part 0 weights (38 recommendation and critical
components, 7 instruction-following, 55 asks) and prints one row per response with both ask
columns scored from their own readings:

  cracker  lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched
           joins, fan-out, count ties), executes every filed rule the pack points at and matches
           every control and published figure it carries.
  mirror   stops at the most attractive wrong rung (rung 2, the load-per-staffed-position match)
           and does not run the battery.

It also prints, per ask device, the natural read's value beside the golden's and the gap against
the asking sentence's stated rounding, and the list of graded figures the prompt's rounding
sentence governs with the precision each is printed at.

Exit 0 when the pair is at or under 40 and the mirror's ask leakage under 35 per cent.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402

W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_WRONG_CALL = 5.0          # recommendation weight a wrong call keeps, from the generated rubric
N_SCHEMES = 10


def truth():
    cases, panel = core.build()
    sch = core.assign_schemes(cases)
    part = {c: p for c, nm, w, p, m in sch}
    for c in cases:
        c["part"] = part[c["scheme"]]
    rows, big = core.billing_lines(cases, sch)
    reg, tru = core.register_and_trustee()
    return cases, panel, rows, reg, tru


def ask1(cases):
    """1 figure: the FY2026 breach share for the whole member-service operation, per cent."""
    f26 = [c for c in cases if core.FY26[0] <= c["qi"] <= core.FY26[1]]
    return {"operation breach share": round(100.0 * sum(c["late"] for c in f26) / len(f26), 1)}


def ask1_elapsed(cases):
    """The same figure read on elapsed working days, not the standard's netted clock."""
    f26 = [c for c in cases if core.FY26[0] <= c["qi"] <= core.FY26[1]]
    late = sum(1 for c in f26 if (c["gross"] > c["tgt"] if not c["open"] else True))
    return {"operation breach share": round(100.0 * late / len(f26), 1)}


def ask2(rows, read):
    """4 figures: per FY2026 fiscal quarter, the chargeable cases the billing extract covers.
    read='cases' divides each line's fee by the schedule rate; read='rows' counts lines."""
    out = {}
    for r in rows:
        fy, q = core.fiscal_quarter(r["billed"])
        if (fy, q) == (2026, 0):
            continue
        key = "FY2026 Q%d chargeable cases covered" % q
        out[key] = out.get(key, 0) + (r["cases"] if read == "cases" else 1)
    return {k: out[k] for k in sorted(out)}


def ask3(cases, reg, tru, source):
    """2 x N figures: the N largest participating schemes by FY2026 cases received, each with its
    active members at 31 March 2026 and its FY2026 cases per 1,000 active members.
    source='trustee' is the golden; source='register' is the figure as returned."""
    f26 = [c for c in cases if core.FY26[0] <= c["qi"] <= core.FY26[1]]
    cnt = {}
    for c in f26:
        cnt[c["part"]] = cnt.get(c["part"], 0) + 1
    order = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:N_SCHEMES]
    R = {r["scheme_code"]: r["active_members"] for r in reg}
    T = {t["scheme_code"]: t["active_members_31mar2026"] for t in tru}
    out = {}
    for code, n in order:
        mem = T[code] if source == "trustee" else R[code]
        out["%s active members" % code] = mem
        out["%s cases per 1,000" % code] = round(1000.0 * n / mem, 1)
    return out, order, cnt


def score(golden, response, unit):
    """A hit is within half the stated rounding unit of the golden."""
    hits = []
    for k, g in golden.items():
        r = response.get(k)
        ok = r is not None and abs(float(r) - float(g)) <= unit.get(k, 0.05)
        hits.append((k, g, r, ok))
    return hits


def main():
    cases, panel, rows, reg, tru = truth()

    g1 = ask1(cases)
    g2 = ask2(rows, "cases")
    g3, order, cnt = ask3(cases, reg, tru, "trustee")
    n1 = ask1_elapsed(cases)
    n2 = ask2(rows, "rows")
    n3, _, _ = ask3(cases, reg, tru, "register")

    units = {}
    units.update({k: 0.05 for k in g1})                      # per cent to one decimal
    units.update({k: 0.5 for k in g2})                       # whole cases
    for k in g3:
        units[k] = 0.5 if k.endswith("active members") else 0.05

    golden = {}
    golden.update(g1); golden.update(g2); golden.update(g3)

    # The cracker: correct on ask 1 and ask 2 (it divides each line's fee by the schedule rate,
    # because the line fees are exact multiples of it), and on ask 3 it takes the members register,
    # which is self-consistent, passes the battery and carries no total to reconcile.
    cracker = {}
    cracker.update(g1); cracker.update(g2); cracker.update(n3)
    # The mirror: rebuilt the metric so ask 1 holds, counts billing lines on ask 2, register on ask 3.
    mirror = {}
    mirror.update(g1); mirror.update(n2); mirror.update(n3)

    print("task198 ask layer, solved on Part 0 weights (%.0f recommendation and components, "
          "%.0f instruction, %.0f asks)\n" % (W_REC, W_INSTR, W_ASK))
    print("asks: A1 %d figure, A2 %d figures, A3 %d figures, %d graded ask figures in all"
          % (len(g1), len(g2), len(g3), len(golden)))

    labels = {"cracker": cracker, "mirror": mirror}
    keeps = {}
    for nm in ("cracker", "mirror"):
        hits = score(golden, labels[nm], units)
        kept = [h for h in hits if h[3]]
        keeps[nm] = len(kept)
        per = {}
        for k, g, r, ok in hits:
            a = "A1" if k in g1 else ("A2" if k in g2 else "A3")
            per.setdefault(a, [0, 0])
            per[a][1] += 1
            per[a][0] += 1 if ok else 0
        print("\n%-8s keeps %2d of %2d ask figures  (%s)"
              % (nm, len(kept), len(hits), ", ".join("%s %d/%d" % (a, v[0], v[1]) for a, v in sorted(per.items()))))
        for k, g, r, ok in hits:
            if ok:
                print("           keeps  %-34s golden %s" % (k, g))

    Lc, Ls = keeps["cracker"] / len(golden), keeps["mirror"] / len(golden)
    C = W_REC + W_INSTR + W_ASK * Lc
    S = R_WRONG_CALL + W_INSTR + W_ASK * Ls
    pair = (C + S) / 2.0
    print("\n  cracker (lands the call) : %.1f  = %.0f + %.0f + %.0f x %.4f" % (C, W_REC, W_INSTR, W_ASK, Lc))
    print("  mirror  (stops at rung 2): %.1f  = %.0f + %.0f + %.0f x %.4f" % (S, R_WRONG_CALL, W_INSTR, W_ASK, Ls))
    print("  PAIR CEILING             : %.1f   (bar 40)" % pair)
    print("  MIRROR LEAKAGE           : %.1f per cent of ask weight   (bar 35)" % (100 * Ls))

    print("\nask device forcing, measured on the clean truth")
    print("  A2 bundled billing lines: natural read %d lines against %d cases covered, "
          "a gap of %d on a figure stated in whole cases"
          % (sum(n2.values()), sum(g2.values()), sum(g2.values()) - sum(n2.values())))
    for k in sorted(g2):
        print("     %-34s golden %5d   natural read %5d" % (k, g2[k], n2[k]))
    print("  A3 grouped sponsor returns: %d of the %d largest participating schemes carry a group "
          "figure in the register" % (sum(1 for c, n in order if reg[[r['scheme_code'] for r in reg].index(c)]['return_basis'] == 'group return'), len(order)))
    worst = 0.0
    for code, n in order:
        rm = {r["scheme_code"]: r["active_members"] for r in reg}[code]
        tm = {t["scheme_code"]: t["active_members_31mar2026"] for t in tru}[code]
        gr, nr = round(1000.0 * n / tm, 1), round(1000.0 * n / rm, 1)
        worst = max(worst, abs(gr - nr))
        print("     %-9s cases %5d  golden rate %6.1f  register rate %6.1f  gap %6.1f" % (code, n, gr, nr, gr - nr))
    print("     smallest gap on a rate stated to one decimal: %.1f against a 0.05 bin half-width"
          % min(abs(round(1000.0 * n / {t['scheme_code']: t['active_members_31mar2026'] for t in tru}[c], 1)
                    - round(1000.0 * n / {r['scheme_code']: r['active_members'] for r in reg}[c], 1))
                for c, n in order if {r['scheme_code']: r['return_basis'] for r in reg}[c] == "group return"))

    print("\nmembership boundary of the graded set (the %dth against the %dth largest)" % (N_SCHEMES, N_SCHEMES + 1))
    allo = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    print("  %s %d cases against %s %d cases, a gap of %d"
          % (allo[N_SCHEMES - 1][0], allo[N_SCHEMES - 1][1], allo[N_SCHEMES][0], allo[N_SCHEMES][1],
             allo[N_SCHEMES - 1][1] - allo[N_SCHEMES][1]))

    print("\nfigures the prompt's rounding sentence governs, and the precision each is printed at")
    print("  one decimal place in percentage points or per 1,000:")
    for k in sorted(list(g1) + [k for k in g3 if k.endswith("per 1,000")]):
        v = golden[k]
        print("     %-34s %s   (one decimal)" % (k, ("%.1f" % v)))
    print("  whole counts, no rounding sentence applies:")
    for k in sorted(list(g2) + [k for k in g3 if k.endswith("active members")]):
        print("     %-34s %d" % (k, golden[k]))

    ok = pair <= 40.0 and 100 * Ls < 35.0
    print("\n%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
