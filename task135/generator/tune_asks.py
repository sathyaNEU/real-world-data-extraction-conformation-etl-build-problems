"""The ask layer's tuning for a fixed market world.

For the world's market seed it draws the November 2025 dividends' level and a shift in the REITs' property income
distribution share (book knobs that move no return), takes each candidate grants world, and solves for the portfolio's
size and the running costs total so that:
  - every golden ask figure (nine incomes, the grant payments, nine releases) sits within MARGIN_BIN of its stated
    thousand, and the releases round the same way from rounded parts as from unrounded ones;
  - the chart's title step has 2.5 per cent of income on each side, and every release is 30,000 pounds or more;
  - every mishandling in asks.stop_combos() that moves a figure lands at least MARGIN_STOP from the stated golden figure;
  - the income's fall from one step to the next sits at least 200 pounds from a whole thousand, so the stated figures do
    not step down by one repeated round sum.
The portfolio's size scales every income (the book is scale-free), so the solve runs on rates; the chosen size is then
built exactly and checked again by checks.py. Prints the parameters world.py records.

    python3 tune_asks.py <market seed> [tries] [title step]
"""
import sys

import numpy as np

import world as W
import book as BK
import grants as GR
import files as FL
import asks as A
import load as LO
import observe as O
import tune as T

STEPS = A.STEPS
GRANT_CANDIDATES = [(117, 1.2), (179, 1.1), (492, 1.2), (496, 1.2), (811, 1.2), (1180, 1.2), (1985, 1.2), (2067, 1.2),
                    (326, 1.2), (1142, 1.1), (715, 1.2), (1024, 1.1), (2203, 1.2), (2311, 1.15), (2477, 1.2),
                    (2590, 1.15)]
MARGIN_BIN = 340
MARGIN_STOP = 680
DY = W.DIV_SCALE                       # the mandate's dividend scale for the final book (the market polish uses W.DIV_SCALE)
GOLD_I = ("position", 12, "history")
GOLD_G = ("lag", True, True, 50)


def r1000(x):
    return np.floor(np.asarray(x) / 1000.0 + 0.5) * 1000.0


def income_side(M, fp, start_total, knobs):
    """the income variants at the base size, the portfolio's value and the lot lines' inflation"""
    B = BK.run(M, W.SEED, fp, keep_rows=True, start_total=start_total, knobs=knobs)
    val = O.valuation(B)
    val = val[val["valuation_date"] == W.VAL_DATE.isoformat()]
    F = LO.typed({"val": val, "ent": O.entitlements(B, M), "static": O.static(B)}, keys=("val", "ent", "static"))
    F["kest"] = O.kestwick_history(B, M)
    P = FL.pack_for_asks(dict(F, reg=None, inst=None, pays=None), 0, 0)
    iv = A.income_variants(P)
    inc, info = A.income(P)
    e = P.ent
    em = e[(e["ex_date"] >= A.INC_FROM.isoformat()) & (~e["security_code"].str.startswith("KWC"))]
    pos = em.drop_duplicates(["sub_account", "security_code", "event_ref"])["entitlement_gbp"].sum()
    return iv, info, em["entitlement_gbp"].sum() / pos - 1


def grant_side(gseed, gscale):
    g, i = GR.make(gseed, {"scale": gscale})
    p = GR.settle(g, i, gseed, {})
    reg, ins, pay = FL.grant_frames(g, i, p, gseed)
    F = LO.typed({"reg": reg, "inst": ins, "pays": pay}, keys=("reg", "inst", "pays"))
    return A.grant_variants(A.Pack(reg=F["reg"], inst=F["inst"], pays=F["pays"]))


def solve(iv, total, gv, capital, base_running, title_step=40, rc_span=15000, v_step=20.0, combos=None, v_range=None):
    """every (portfolio value, running costs) meeting the targets, best first"""
    combos = combos or A.stop_combos()
    ki = list(iv)
    rates = np.array([[iv[k][s] for s in STEPS] for k in ki]) / total
    gi = ki.index(GOLD_I)
    kg = list(gv)
    Gk = np.array([gv[k] for k in kg])
    G = Gk[kg.index(GOLD_G)]
    oG = float(G - r1000(G))
    if abs(oG) > MARGIN_BIN:
        return []
    ci = np.array([ki.index(c[0]) for c in combos])
    cg = np.array([kg.index(c[1]) for c in combos])
    cf = np.array([capital if c[2] else 0.0 for c in combos])
    dG = Gk[cg] - G                                                         # per combo
    movedG = np.abs(dG) >= 0.5
    if np.any(np.abs(G + dG[movedG] - r1000(G)) < MARGIN_STOP):
        return []
    t = STEPS.index(title_step)
    r = rates[gi]
    v_lo, v_hi = G / (0.975 * r[t]), G / (1.025 * r[t + 1])
    if v_range is not None:
        if not (v_lo <= v_range[0] <= v_hi):
            return []
        v_lo, v_hi = v_range
    out = []
    oRC = np.arange(-500, 500)
    Vs = np.arange(v_lo, v_hi, v_step)
    inc_rows = sorted(set(ci.tolist()) - {gi})
    Iall = Vs[:, None, None] * rates[None, :, :]
    Igall = Iall[:, gi, :]
    oIall = Igall - r1000(Igall)
    ok = np.all(np.abs(oIall) <= MARGIN_BIN, axis=1)
    sub = Iall[:, inc_rows, :]
    dIsub = sub - Igall[:, None, :]
    distI = np.where(np.abs(dIsub) >= 0.5, np.abs(sub - r1000(Igall)[:, None, :]), np.inf)
    ok &= distI.reshape(len(Vs), -1).min(axis=1) >= MARGIN_STOP
    for V, I, Ig, oI in zip(Vs[ok], Iall[ok], Igall[ok], oIall[ok]):
        # the income falls by the same amount at every step; that amount sits away from a whole thousand, so the stated
        # figures do not fall by one repeated round sum
        dec = Ig[0] - Ig[1]
        if abs(dec - r1000(dec)) < 200:
            continue
        oR = oG + oRC[:, None] - oI[None, :]
        okb = np.where(np.all(np.abs(oR) <= MARGIN_BIN, axis=1))[0]
        if not len(okb):
            continue
        D = dG[:, None] + cf[:, None] - (I[ci] - Ig[None, :])                  # combos x 9
        Dm = np.where(np.abs(D) >= 0.5, D, np.inf)
        dist = np.abs(Dm[None, :, :] + oR[okb][:, None, :]).min(axis=(1, 2))
        good = dist >= MARGIN_STOP
        if not good.any():
            continue
        score = np.minimum.reduce([dist - MARGIN_STOP, MARGIN_BIN - np.abs(oR[okb]).max(axis=1),
                                   np.full(len(okb), MARGIN_BIN - np.abs(oI).max()), np.full(len(okb), MARGIN_BIN - abs(oG))])
        score = np.where(good, score, -np.inf)
        b = int(np.argmax(score))
        orc = int(oRC[okb[b]])
        rc = int(round((base_running - orc) / 1000.0)) * 1000 + orc
        if (G + rc - Ig).min() < 30000 or abs(rc - base_running) > rc_span:
            continue
        out.append(dict(score=float(score[b]), V=float(V), running=rc, stop_min=float(dist[b]),
                        title_lo=float(Ig[t] - G), title_hi=float(G - Ig[t + 1])))
    out.sort(key=lambda d: -d["score"])
    return out


def exact(M, fp, mseed, d, title_step=40):
    """the solution built exactly at its size and knobs: the call's conditions on the final book, then the running costs
    solved again on the exact incomes; returns the solution with its exact score, or None"""
    capital = sum(v for _, v in W.CAPITAL_CHARGES)
    base_running = sum(v for _, v in W.RUNNING_COSTS)
    B = BK.run(M, W.SEED, fp, keep_rows=False, start_total=d["start_total"], knobs=d["knobs"])
    X, dates = T.returns(M, B, fp)
    c, Tb, r2 = T.conditions(X, dates, T.index_returns(M, B.days))
    fails = [k for k, v in c.items() if not v]
    if fails:
        return dict(d, exact="call conditions fail: %s" % fails)
    iv, info, infl = income_side(M, fp, d["start_total"], d["knobs"])
    gv = grant_side(*d["grants"])
    sols = solve_at(iv, info["total"], gv, capital, base_running, title_step)
    if not sols:
        return dict(d, exact="no running costs total meets the targets at the exact size (V %.0f)" % info["total"])
    s = sols[0]
    return dict(d, running=s["running"], V=round(info["total"], 2), stop_min=round(s["stop_min"], 1), exact_score=s["score"],
                title=(round(s["title_lo"]), round(s["title_hi"])), inflation=round(infl, 3), exact="ok")


def solve_at(iv, total, gv, capital, base_running, title_step=40):
    """solve() at the one portfolio value the book gives (no size search)"""
    global MARGIN_BIN, MARGIN_STOP
    saved = (MARGIN_BIN, MARGIN_STOP)
    out = []
    try:
        for mb, ms in ((340, 680), (370, 640), (390, 610)):
            MARGIN_BIN, MARGIN_STOP = mb, ms
            out = solve(iv, total, gv, capital, base_running, title_step, v_step=1.0, v_range=(total, total + 0.5))
            if out:
                break
    finally:
        MARGIN_BIN, MARGIN_STOP = saved
    return out


def search(mseed, tries=60, title_step=40, seed=0, want=8):
    M, fp, B0, X, dates, drift = T.build_world(mseed, iters=3)
    capital = sum(v for _, v in W.CAPITAL_CHARGES)
    base_running = sum(v for _, v in W.RUNNING_COSTS)
    rng = np.random.default_rng(1000 + mseed + seed)
    gsides = {gc: grant_side(*gc) for gc in GRANT_CANDIDATES}
    found = []
    for k in range(tries):
        knobs = {"nov25": round(float(rng.uniform(0.85, 1.25)), 4), "pid_shift": round(float(rng.uniform(-0.08, 0.06)), 4),
                 "dy": DY}
        iv, info, infl = income_side(M, fp, BK.START_TOTAL, knobs)
        if not 0.28 <= infl <= 0.48:
            print("knobs", knobs, "inflation %.3f out of range" % infl, flush=True)
            continue
        for gc, gv in gsides.items():
            sols = solve(iv, info["total"], gv, capital, base_running, title_step)
            if sols:
                s = sols[0]
                found.append((s["score"], dict(start_total=round(BK.START_TOTAL * s["V"] / info["total"], 2), knobs=knobs,
                                               grants=gc, running=s["running"], V=round(s["V"], 2),
                                               stop_min=round(s["stop_min"], 1),
                                               title=(round(s["title_lo"]), round(s["title_hi"])), inflation=round(infl, 3),
                                               solutions=len(sols))))
                print("found score %.0f" % s["score"], found[-1][1], flush=True)
        print("try", k, knobs, "found so far", len(found), flush=True)
        if len(found) >= want:
            break
    found.sort(key=lambda x: -x[0])
    return found


if __name__ == "__main__":
    ms = int(sys.argv[1])
    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    ts = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    if len(sys.argv) > 4:
        DY = float(sys.argv[4])
    found = search(ms, tries, ts)
    M, fp, B0, X, dates, drift = T.build_world(ms, iters=3)
    for score, d in found[:8]:
        print("CANDIDATE %.0f" % score, d)
        print("   EXACT", exact(M, fp, ms, d, ts), flush=True)
