"""Write tune_table.py: the bin-centring adjustments. Run after any change upstream of the claim amounts.

    python3 tune.py SCRATCH_DIR

Builds the pack without centring, reads every graded figure from the files, and for each figure that sits within
0.20 of a whole-dollar rounding boundary picks one clean claim in the figure's own population and window and moves
its allowed amount by the few dollars that put the figure a quarter of a dollar from the nearest whole dollar.
Medical and pharmacy figures move independently; the programme baseline is then brought clear of its boundaries,
with both rounding paths of the total agreeing and each programme figure at least a dollar from the persistence
rung's, by moving the tier baselines inside their own comfortable zones. Only facility claims (paid at a rate or a
share of charges) and pharmacy claims are moved, never a fee-schedule line, and none by more than 4 per cent of its
allowed amount (2.5 per cent for a fill)."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import build as B
import estimators as E

TM2, TR2 = W.TREND_MED ** 2, W.TREND_RX ** 2


def comfortable(v):
    return abs(v - round(v)) <= 0.30 and abs(v - round(v)) >= 0.12


def target_for(v):
    if comfortable(v):
        return v
    lo = int(v // 1)
    cands = [lo - 0.75, lo - 0.25, lo + 0.25, lo + 0.75, lo + 1.25]
    return min(cands, key=lambda c: abs(c - v))


def main(scratch):
    S, L, P = B.build(scratch, verbose=True, tune=False)
    G, F = E.figures(os.path.join(scratch, "target"))
    pid_of = {p.member_id: p.pid for p in S.people if p.member_id}
    bid = {t: set(pid_of[m] for m in ms) for t, ms in G["members"]["bid"].items()}
    fin = {t: set(pid_of[m] for m in ms) for t, ms in G["members"]["final"].items()}
    an_mm = {t: G["an_detail"][t][1] for t in bid}
    f_mm = {t: G["f26_detail"][t][1] for t in fin}
    used = set()
    table = {}

    def pick_med(pids, a, b, delta):
        # facility claims only: a professional line is at the fee schedule and stays there
        cands = [c for c in P.med if c["clean"] and c["ct"] == "I" and c["pid"] in pids and a <= c["d0"] <= b
                 and c["key"] not in used and sum(l[5] for l in c["lines"]) >= 25 * abs(delta)
                 and max(l[5] for l in c["lines"]) + delta > 0
                 and all(l[5] + delta < l[4] for l in c["lines"] if l[4] == max(x[4] for x in c["lines"]))]
        cands.sort(key=lambda c: (c["d0"], c["key"]))
        c = cands[len(cands) // 2]
        used.add(c["key"])
        orig = sum(l[5] for l in c["lines"])
        return c["key"] + (orig,)

    def pick_rx(pids, a, b, delta):
        cands = [i for i, ev in enumerate(P.fills) if i in P.rx_clean and ev[0] in pids and a <= ev[1] <= b
                 and ev[5][0][2] * 100 >= 40 * abs(delta) and ("rx", i) not in used]
        cands.sort(key=lambda i: (P.fills[i][1], P.fills[i][0]))
        i = cands[len(cands) // 2]
        used.add(("rx", i))
        ev = P.fills[i]
        return (ev[0], ev[1].isoformat(), ev[4], 0, int(round(ev[5][0][2] * 100)))

    base = {t: list(G["base"][t]) for t in G["base"]}
    f26 = {t: list(G["f26"][t]) for t in G["f26"]}
    n = G["n"]
    targets = {}
    for t in (1, 2, 3, 4):
        for k in (0, 1):
            targets[("base", t, k)] = target_for(base[t][k])
            targets[("f26", t, k)] = target_for(f26[t][k])

    # the persistence rung (each tier's own 2026 PMPM carried 15 months at trend) is the natural wrong answer: its programme
    # medical and pharmacy figures must not round to the golden's
    r0prog = [sum(n[t] * targets[("f26", t, k)] * (W.TREND_MED if k == 0 else W.TREND_RX) ** 1.25 for t in (1, 2, 3, 4)) / 140
              for k in (0, 1)]

    def cands(v, m=21):
        """points a comfortable distance from a whole dollar, nearest first"""
        pts = []
        for k in range(int(v // 1) - 1, int(v // 1) + 3):
            for d in (0.14, 0.18, 0.22, 0.26, 0.30):
                pts += [k + d, k - d]
        pts = sorted(set(round(p, 2) for p in pts), key=lambda p: abs(p - v))
        return pts[:m]

    def solve(k):
        import itertools
        opts = [cands(base[t][k]) for t in (1, 2, 3, 4)]
        sols = []
        for combo in itertools.product(*opts):
            val = sum(n[t] * combo[t - 1] for t in (1, 2, 3, 4)) / 140
            if comfortable(val) and abs(val - r0prog[k]) >= 1.0:
                sols.append((sum(abs(combo[t - 1] - base[t][k]) * an_mm[t] for t in (1, 2, 3, 4)), combo, val))
        sols.sort()
        return sols

    best = None
    sm, sr = solve(0), solve(1)
    for cm, comb_m, m in sm:
        if best is not None and cm >= best[0]:
            break
        for cr, comb_r, r in sr:
            if best is not None and cm + cr >= best[0]:
                break
            if comfortable(m + r) and round(m) + round(r) == round(m + r):
                best = (cm + cr, comb_m, comb_r)
    assert best is not None
    for t in (1, 2, 3, 4):
        targets[("base", t, 0)] = best[1][t - 1]
        targets[("base", t, 1)] = best[2][t - 1]
    import copy
    import acuity as AC
    events0 = list(S.events)
    sig = lambda LL: {k: [r[:5] for r in LL[k]] for k in ("bid", "draft", "final")}
    L0 = sig(AC.lists(S))
    for (kind, t, k), tv in sorted(targets.items()):
        cur = base[t][k] if kind == "base" else f26[t][k]
        if abs(tv - cur) < 1e-9:
            continue
        while True:
            if kind == "base":
                delta = int(round((tv - cur) * an_mm[t] / (TM2 if k == 0 else TR2) * 100))
                key = pick_med(bid[t], W.ANALOG_START, dt.date(2025, 12, 31), delta) if k == 0 else \
                    pick_rx(bid[t], W.ANALOG_START, dt.date(2025, 12, 31), delta)
            else:
                delta = int(round((tv - cur) * f_mm[t] * 100))
                key = pick_med(fin[t], dt.date(2026, 1, 1), dt.date(2026, 10, 31), delta) if k == 0 else \
                    pick_rx(fin[t], dt.date(2026, 1, 1), dt.date(2026, 12, 31), delta)
            trial = dict(table)
            trial[key] = trial.get(key, 0) + delta
            S.events = list(events0)
            B.apply_tune(S, trial)
            moved = sig(AC.lists(S)) != L0
            S.events = list(events0)
            if not moved:
                break
            print("  candidate %s moves a list, trying the next" % (key,))
        table = trial
        print("%-4s tier %d %s: %.4f -> %.4f, %+d cents on %s" % (kind, t, "med" if k == 0 else "rx", cur, tv, delta, key))
    with open(os.path.join(HERE, "tune_table.py"), "w") as f:
        f.write('"""Bin-centring adjustments written by tune.py: (member index, first date of service, event kind, claim '
                'component,\noriginal allowed in cents) -> change in cents. Each moves one clean claim by a few per cent at most."""\n')
        f.write("TUNE = {\n")
        for k in sorted(table):
            f.write("    %r: %d,\n" % (k, table[k]))
        f.write("}\n")
    print("wrote %d adjustments" % len(table))


if __name__ == "__main__":
    main(sys.argv[1])
