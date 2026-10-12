"""The ask layer's tuning: for a fixed market world, the grants world, the portfolio's size, the November 2025 dividends,
the REITs' distribution split and the running costs, chosen so that every golden ask figure sits inside its
thousand-pound bin, the title has its margins, every release is positive and no mishandling combination lands within
600 pounds of a golden figure. Prints the parameters world.py records."""
import itertools
import sys

import numpy as np

import world as W
import sim as SM
import book as BK
import grants as GR
import files as FL
import asks as A
import tune as T

GRANT_CANDIDATES = [(117, 1.2), (179, 1.1), (492, 1.2), (496, 1.2), (811, 1.2), (1180, 1.2), (1985, 1.2), (2067, 1.2),
                    (326, 1.2), (1142, 1.1), (715, 1.2), (1024, 1.1)]
STEPS = A.STEPS


def ask_state(M, fp, start_total, knobs, gseed, gscale, running, capital_total):
    B = BK.run(M, W.SEED, fp, keep_rows=True, start_total=start_total, knobs=knobs)
    g, i = GR.make(gseed, {"scale": gscale})
    p = GR.settle(g, i, gseed, {})
    F = FL.frames(M, fp, B, g, i, p, gseed)
    P = FL.pack_for_asks(F, running, capital_total)
    return B, F, P


def lot_inflation(P):
    e = P.ent
    e = e[(e["ex_date"] >= A.INC_FROM.isoformat()) & (~e["security_code"].str.startswith("KWC"))]
    pos = e.drop_duplicates(["sub_account", "security_code", "event_ref"])["entitlement_gbp"].sum()
    return e["entitlement_gbp"].sum() / pos - 1


def evaluate(P, running, capital_total, verbose=False):
    inc, info = A.income(P)
    G, parts = A.grant_payments(P)
    rel = A.release(P, inc, G, running)
    gold = [inc[s] for s in STEPS] + [G] + [rel[s] for s in STEPS]
    stated = [A.r1000(x) for x in gold]
    fails = []
    for x, r in zip(gold, stated):
        if abs(x - r) > 400:
            fails.append("bin")
            break
    t = A.title(inc, G)
    if t is None or t == 100 or not (inc[t] - G >= 0.025 * inc[t] and G - inc[t + 10] >= 0.025 * inc[t + 10]):
        fails.append("title")
    if min(rel.values()) < 30000:
        fails.append("release")
    stops = A.all_stops(P, running, capital_total)
    worst = 1e18
    for key, (i2, g2, r2, t2) in stops.items():
        vals = [i2[s] for s in STEPS] + [g2] + [r2[s] for s in STEPS]
        for x, gv, r in zip(vals, gold, stated):
            if abs(x - gv) < 0.005:
                continue
            worst = min(worst, abs(x - r))
    if worst < 600:
        fails.append("stop %.0f" % worst)
    li = lot_inflation(P)
    if not 0.28 <= li <= 0.48:
        fails.append("lots %.2f" % li)
    if verbose:
        print("V %.0f G %.0f title %s inc40 %.0f inc50 %.0f worst stop %.0f lots %.3f" % (
            info["total"], G, t, inc[40], inc[50], worst, li))
    return fails, dict(inc=inc, G=G, rel=rel, title=t, worst=worst, total=info["total"], lots=li)


def search(mseed, tries=400):
    M, fp, B0, X, dates, drift = T.build_world(mseed, iters=3)
    capital_total = sum(v for _, v in W.CAPITAL_CHARGES)
    rng = np.random.default_rng(mseed)
    base_running = sum(v for _, v in W.RUNNING_COSTS)
    for gseed, gscale in GRANT_CANDIDATES:
        g, i = GR.make(gseed, {"scale": gscale})
        GR.settle(g, i, gseed, {})
        Gv = GR.summary(g, i)["G"]
        # the size that centres the 2027 grant payments between the incomes at 40 and 50 per cent
        _, F, P = ask_state(M, fp, BK.START_TOTAL, {}, gseed, gscale, base_running, capital_total)
        inc, info = A.income(P)
        c40, c50 = inc[40] / info["total"], inc[50] / info["total"]
        V = Gv / ((0.975 * c40 + 1.025 * c50) / 2)
        st0 = BK.START_TOTAL * V / info["total"]
        for k in range(tries // len(GRANT_CANDIDATES)):
            st = st0 * (1 + rng.uniform(-0.004, 0.004))
            knobs = {"nov25": float(rng.uniform(0.8, 1.3)), "pid": float(rng.uniform(0.70, 0.86))}
            _, F, P = ask_state(M, fp, st, knobs, gseed, gscale, base_running, capital_total)
            for adj in rng.integers(-4000, 9000, 12):
                running = base_running + int(adj)
                fails, res = evaluate(P, running, capital_total)
                if not fails:
                    print("FOUND", dict(mseed=mseed, start_total=round(st, 2), knobs=knobs, gseed=gseed, gscale=gscale,
                                        running_adj=int(adj)), flush=True)
                    evaluate(P, running, capital_total, verbose=True)
                    return
            print(gseed, k, fails, flush=True)


if __name__ == "__main__":
    search(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 400)
