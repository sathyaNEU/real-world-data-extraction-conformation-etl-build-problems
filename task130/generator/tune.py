"""Write tune_table.py: the bin-centring adjustments. Run after any change upstream of the claim amounts.

    python3 tune.py SCRATCH_DIR

Builds the pack without centring and reads every graded figure from the files. Each graded figure is aimed at an
irregular point inside its whole-dollar bin: between 0.12 and 0.30 from the whole dollar, so at least 0.20 from the
rounding boundary, at an offset drawn for that figure from a seeded generator and kept clear of every cent multiple. A
figure that came out exact (on a cent, a quarter-dollar or a round fraction of a dollar) would confirm the method that
produced it, so none is aimed at one. A figure already inside the band and clear of the cent grid stays where it is.
One clean claim in the figure's own population and window moves by the few dollars that put the figure on its target.
Medical and pharmacy figures move independently; the programme baseline is brought inside the same band, clear of the
cent grid, with both rounding paths of the total agreeing and each programme figure at least a dollar from the
persistence rung's, by a draw among the cheapest combinations of the tier baselines' targets. Only facility claims
(paid at a rate or a share of charges) and pharmacy claims are moved, never a fee-schedule line, and none by more than
4 per cent of its allowed amount (2.5 per cent for a fill).

Each draw is built and measured before it is kept: every graded figure as built inside its band and at least 0.001
from every cent multiple, every rung's and fork's programme total at least 0.0005 from one (so no reading of the ladder
lands on a round value either), and the ladder's whole-dollar separations that checks.py asserts. The first draw that
passes is written, with its number."""
import copy
import datetime as dt
import itertools
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import build as B
import estimators as E
import extracts as X
import acuity as AC
import sim as SM

TM2, TR2 = W.TREND_MED ** 2, W.TREND_RX ** 2
T = (1, 2, 3, 4)
DRAW_SEED = 52389       # draw j takes its offsets from default_rng(DRAW_SEED + j)
DRAWS = 40
PAIRS = 30              # a draw's programme baseline: one of the 30 cheapest medical and pharmacy combinations that fit
BAND = (0.12, 0.30)     # a graded figure's distance from its whole dollar
SUB = 0.0012            # a target's distance from every cent multiple
GRADED_MIN = 0.001      # as built, a graded figure's distance from every cent multiple
RUNG_MIN = 0.0005       # as built, a rung's or fork's programme total's distance from every cent multiple
gap = E.grid_gap


def comfortable(v):
    return BAND[0] <= abs(v - round(v)) <= BAND[1] and gap(v, 0.01) >= SUB


def offsets(rng, m=5):
    """m distances from a whole dollar inside the band, none near a cent multiple"""
    out = []
    while len(out) < m:
        d = float(rng.uniform(*BAND))
        if gap(d, 0.01) >= SUB:
            out.append(d)
    return out


def cands(v, offs, m=21, avoid=None):
    """the drawn points either side of the whole dollars around v, nearest first, none on the whole dollar `avoid`;
    v itself leads when it is already comfortable"""
    pts = [v] if comfortable(v) else []
    for k in range(int(v // 1) - 1, int(v // 1) + 3):
        for d in offs:
            pts += [k + d, k - d]
    pts = sorted(set(p for p in pts if avoid is None or round(p) != avoid), key=lambda p: abs(p - v))
    return pts[:m]


def accept(G, targets):
    """the bins and the ladder's separations on one draw as built: what checks.py asserts on them"""
    bad = []
    n, base, f26 = G["n"], G["base"], G["f26"]
    m_, r_ = G["prog"]
    g = G["prog_total"]
    lab = lambda k: "medical" if k == 0 else "pharmacy"
    graded = [("%s tier %d %s" % (kind, t, lab(k)), (base if kind == "base" else f26)[t][k])
              for kind in ("f26", "base") for t in T for k in (0, 1)]
    graded += [("programme medical", m_), ("programme pharmacy", r_), ("programme total", g)]
    for name, v in graded:
        if not BAND[0] - 1e-3 <= abs(v - round(v)) <= BAND[1] + 1e-3:
            bad.append("%s %.5f outside its band" % (name, v))
        if gap(v, 0.01) < GRADED_MIN:
            bad.append("%s %.5f near a cent multiple" % (name, v))
    for (kind, t, k), tv in targets.items():
        v = (base if kind == "base" else f26)[t][k]
        if abs(v - tv) > 1e-4:
            bad.append("%s tier %d %s missed its target (%.5f against %.5f)" % (kind, t, lab(k), v, tv))
    if round(m_) + round(r_) != round(g):
        bad.append("the rounded parts do not add to the rounded total")
    rk, fk = G["rungs"], G["forks"]
    for k, v in sorted(rk.items()) + sorted(fk.items()):
        if gap(v, 0.01) < RUNG_MIN:
            bad.append("%s's programme total %.5f near a cent multiple" % (k, v))

    def exempt(name, t):
        # a rung equal to the golden by construction in a tier where every member counted stayed the year
        return ((name == "R4a" and G["an_detail"][t][1] == 12 * G["bid_tiers"][t])
                or (name == "R4b" and G["an_detail"][t][1] == 12 * G["r4b_n"][t])
                or (name == "R4c" and G["an_detail"][t][1] == G["r4c_n"][t]))

    for name, tab in G["rung_tiers"].items():
        for t in T:
            for k in (0, 1):
                if not exempt(name, t) and round(tab[t][k]) == round(base[t][k]):
                    bad.append("%s lands on the golden tier %d %s" % (name, t, lab(k)))
        for k in (0, 1):
            if round(sum(n[t] * tab[t][k] for t in T) / 140) == round(G["prog"][k]):
                bad.append("%s lands on the golden programme %s" % (name, lab(k)))
    for k in ("R3b", "R5b", "R6c", "pooled", "regression", "R0c", "R4c", "R7", "R9"):
        if round(rk[k]) == round(g):
            bad.append("%s lands on the golden total" % k)
    FK = G["fork_tiers"]
    if any(round(FK["R0p"][t][1]) == round(base[t][1]) for t in T):
        bad.append("pharmacy persistence lands on a tier cell")
    mx = FK["R10"]
    mxp = [sum(n[t] * mx[t][k] for t in T) / 140 for k in (0, 1)]
    if round(mxp[0]) == round(m_) or round(mxp[1]) == round(r_) or round(fk["R10"]) == round(g):
        bad.append("R10 lands on a programme figure")
    if any(round(mx[t][k]) == round(base[t][k]) for t in G["overlap"]["touched"] for k in (0, 1)):
        bad.append("R10 lands on a tier cell")
    r0 = G["rung_tiers"]["R0"]
    if any(abs(G["prog"][k] - sum(n[t] * r0[t][k] for t in T) / 140) < 1.0 for k in (0, 1)):
        bad.append("a programme figure within a dollar of persistence's")
    t4 = 1.1342
    if any(round(base[t][0] / TM2 * t4) != round(base[t][0]) for t in T) or \
            round(sum(n[t] * base[t][0] / TM2 * t4 for t in T) / 140) != round(m_):
        bad.append("a trend factor shown to four places rounds a medical figure apart")
    return bad


def main(scratch):
    S, L, P = B.build(scratch, verbose=True, tune=False)
    src = os.path.join(scratch, "target")
    G, F = E.figures(src)
    pid_of = {p.member_id: p.pid for p in S.people if p.member_id}
    bid = {t: set(pid_of[m] for m in ms) for t, ms in G["members"]["bid"].items()}
    fin = {t: set(pid_of[m] for m in ms) for t, ms in G["members"]["final"].items()}
    allbid = set().union(*bid.values())
    an_mm = {t: G["an_detail"][t][1] for t in bid}
    f_mm = {t: G["f26_detail"][t][1] for t in fin}
    # counting only the bid members enrolled all twelve months (R4c) differs from the baseline only through the members
    # who were enrolled for part of the year: a baseline cell is kept off R4c's whole dollar and moved on a part-year
    # member's claim, which leaves R4c where it is
    part = {t: set(pid_of[m] for m in ms if 0 < F.mm(m, W.ANALOG_START, W.ANALOG_END) < 12)
            for t, ms in G["members"]["bid"].items()}
    r4c = G["rung_tiers"]["R4c"]
    protect = set(r[1] for k in ("bid", "draft", "final") for r in L[k])
    used = set()

    def pick_med(pids, a, b, delta):
        # facility claims only: a professional line is at the fee schedule and stays there. The line that moves is
        # the one build.adjust moves (the first with the largest charge); it stays above zero, under its charge and
        # clear of every other line's allowed amount on the claim
        def fits(c):
            ls = c["lines"]
            if any(l[5] is None for l in ls):
                return False
            top_line = max(range(len(ls)), key=lambda i: ls[i][4])
            new = ls[top_line][5] + delta
            return (sum(l[5] for l in ls) >= 25 * abs(delta) and 0 < new < ls[top_line][4]
                    and all(l[5] != new for i, l in enumerate(ls) if i != top_line))
        cands_ = [c for c in P.med if c["clean"] and c["ct"] == "I" and c["pid"] in pids and a <= c["d0"] <= b
                  and c["key"] not in used and fits(c)]
        cands_.sort(key=lambda c: (c["d0"], c["key"]))
        c = cands_[len(cands_) // 2]
        used.add(c["key"])
        orig = sum(l[5] for l in c["lines"])
        return c["key"] + (orig,)

    def pick_rx(pids, a, b, delta):
        cands_ = [i for i, ev in enumerate(P.fills) if i in P.rx_clean and ev[0] in pids and a <= ev[1] <= b
                  and ev[5][0][2] * 100 >= 40 * abs(delta) and ("rx", i) not in used]
        cands_.sort(key=lambda i: (P.fills[i][1], P.fills[i][0]))
        i = cands_[len(cands_) // 2]
        used.add(("rx", i))
        ev = P.fills[i]
        return (ev[0], ev[1].isoformat(), ev[4], 0, int(round(ev[5][0][2] * 100)))

    base = {t: list(G["base"][t]) for t in G["base"]}
    f26 = {t: list(G["f26"][t]) for t in G["f26"]}
    n = G["n"]
    events0 = list(S.events)
    sig = lambda LL: {k: [r[:5] for r in LL[k]] for k in ("bid", "draft", "final")}
    L0 = sig(AC.lists(S))
    keys = sorted((kind, t, k) for kind in ("base", "f26") for t in T for k in (0, 1))

    # a draw is built on a second run of the simulation, its coder's generator put back each time where the build's
    # pack finds it (straight after the simulation), so the files a draw is measured on are the files the build ships
    S2 = SM.simulate()
    events2 = list(S2.events)
    coder2 = copy.deepcopy(S2.coder.r.bit_generator.state)

    def measure(table):
        """the claims files built with `table`, beside the untouched eligibility, conversion and list files, and every
        figure read from them"""
        d = os.path.join(scratch, "draw")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        S2.events = list(events2)
        S2.coder.r.bit_generator.state = copy.deepcopy(coder2)
        B.apply_tune(S2, table)
        PP = X.Pack(S2, W.SEED, protect)
        PP.price()
        PP.medical_versions()
        PP.pharmacy_rows()
        X.write_csv(os.path.join(d, B.FILES["med"]), X.MED_COLS, PP.medical_rows())
        X.write_csv(os.path.join(d, B.FILES["rx"]), X.PBM_COLS, PP.pbm_rows())
        for f in ("elig", "xwalk", "bid", "draft", "final"):
            os.symlink(os.path.join(src, B.FILES[f]), os.path.join(d, B.FILES[f]))
        return E.figures(d)[0]

    for j in range(DRAWS):
        rng = np.random.default_rng(DRAW_SEED + j)
        offs = {key: offsets(rng) for key in keys}
        targets = {}
        for t in T:
            for k in (0, 1):
                v = f26[t][k]
                targets[("f26", t, k)] = v if comfortable(v) else cands(v, offs[("f26", t, k)], m=1)[0]
        # the persistence rung (each tier's own 2026 PMPM carried 15 months at trend) is the natural wrong answer: its
        # programme medical and pharmacy figures must not round to the golden's
        r0prog = [sum(n[t] * targets[("f26", t, k)] * (W.TREND_MED if k == 0 else W.TREND_RX) ** 1.25 for t in T) / 140
                  for k in (0, 1)]

        def solve(k):
            opts = [cands(base[t][k], offs[("base", t, k)], avoid=round(r4c[t][k]) if part[t] else None) for t in T]
            sols = []
            for combo in itertools.product(*opts):
                val = sum(n[t] * combo[t - 1] for t in T) / 140
                if comfortable(val) and abs(val - r0prog[k]) >= 1.0:
                    sols.append((sum(abs(combo[t - 1] - base[t][k]) * an_mm[t] for t in T), combo, val))
            sols.sort()
            return sols

        # the draw takes one of the cheapest combinations that fit, not always the cheapest: the rungs built on the bid
        # members' year (their calendar 2025, the year untrended, the draft's weights) move with the programme figures,
        # and the cheapest combination leaves those figures, and so those rungs, in nearly the same place every draw
        top, bound = [], float("inf")
        sm, sr = solve(0), solve(1)
        for cm, comb_m, m in sm:
            if cm >= bound:
                break
            for cr, comb_r, r in sr:
                if cm + cr >= bound:
                    break
                if comfortable(m + r) and round(m) + round(r) == round(m + r):
                    top.append((cm + cr, comb_m, comb_r))
                    if len(top) >= PAIRS:
                        top = sorted(top)[:PAIRS]
                        bound = top[-1][0]
        if not top:
            print("draw %d: no programme combination fits" % j)
            continue
        top.sort()
        best = top[int(rng.integers(len(top)))]
        for t in T:
            targets[("base", t, 0)] = best[1][t - 1]
            targets[("base", t, 1)] = best[2][t - 1]
        used.clear()
        table = {}
        for (kind, t, k), tv in sorted(targets.items()):
            cur = base[t][k] if kind == "base" else f26[t][k]
            if kind == "base":
                delta = int(round((tv - cur) * an_mm[t] / (TM2 if k == 0 else TR2) * 100))
            else:
                delta = int(round((tv - cur) * f_mm[t] * 100))
            if delta == 0:
                continue
            while True:
                if kind == "base":
                    pick = pick_med if k == 0 else pick_rx
                    try:
                        key = pick(part[t] or bid[t], W.ANALOG_START, dt.date(2025, 12, 31), delta)
                    except IndexError:
                        print("  no part-year claim fits tier %d %s, moving a full-year member's" % (t, "med" if k == 0 else "rx"))
                        key = pick(bid[t], W.ANALOG_START, dt.date(2025, 12, 31), delta)
                else:
                    # a 2026 claim of a member who is not on the bid list, so no baseline moves with it
                    key = pick_med(fin[t] - allbid, dt.date(2026, 1, 1), dt.date(2026, 10, 31), delta) if k == 0 else \
                        pick_rx(fin[t] - allbid, dt.date(2026, 1, 1), dt.date(2026, 12, 31), delta)
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
            print("%-4s tier %d %s: %.5f -> %.5f, %+d cents on %s" % (kind, t, "med" if k == 0 else "rx", cur, tv, delta, key))
        G1 = measure(table)
        bad = accept(G1, targets)
        if bad:
            print("draw %d (seed %d) rejected: %s" % (j, DRAW_SEED + j, "; ".join(bad)))
            continue
        graded = [G1["f26"][t][k] for t in T for k in (0, 1)] + [G1["base"][t][k] for t in T for k in (0, 1)] + \
            list(G1["prog"]) + [G1["prog_total"]]
        rungs = list(G1["rungs"].values()) + list(G1["forks"].values())
        print("draw %d (seed %d) kept: graded figures at least %.4f from a cent and %.4f from a quarter-dollar, rung and "
              "fork totals at least %.4f from a cent" % (j, DRAW_SEED + j, min(gap(v, 0.01) for v in graded),
                                                       min(gap(v, 0.25) for v in graded), min(gap(v, 0.01) for v in rungs)))
        with open(os.path.join(HERE, "tune_table.py"), "w") as f:
            f.write('"""Bin-centring adjustments written by tune.py, draw %d (seed %d): (member index, first date of '
                    'service, event kind,\nclaim component, original allowed in cents) -> change in cents. Each moves one '
                    'clean claim by a few per cent at most."""\n' % (j, DRAW_SEED + j))
            f.write("TUNE = {\n")
            for k in sorted(table):
                f.write("    %r: %d,\n" % (k, table[k]))
            f.write("}\n")
        print("wrote %d adjustments" % len(table))
        return
    raise SystemExit("no draw of %d passed" % DRAWS)


if __name__ == "__main__":
    main(sys.argv[1])
