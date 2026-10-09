"""task122 generator: place every graded ask figure inside its rounding bin, before the files are
written. The asserted figures are recomputed from the written files by checks.py and the verifier.

Fee cells move by a whole euro on the price of plain in-session orders (no offer, shipped, paid
through checkout) in the cell's own group, asking and paid price together, so no device's effect
on the cell changes. Slot totals move by scaling a cell's planned traffic on the 2026-W01 to W12
weeks by a few parts in ten thousand.
"""
import itertools
from datetime import datetime

import numpy as np

import params as P
import traffic as Tr

EPOCH = datetime(2025, 1, 1)


def _window(W):
    S, O = W.S, W.O
    day0 = np.array([(datetime(d.year, d.month, d.day) - EPOCH).total_seconds() for d in S.date], np.int64)
    start = day0 + S.start_s.to_numpy()
    dt = O.t.to_numpy() - start[O.sid.to_numpy()]
    return (dt >= 0) & (dt <= 21 * 86400)


DEVICES = ("f1", "f2", "p1", "hz2", "hz1")       # VAT, balance-paid, in person, price paid, January row
SUBSETS = [s for s in itertools.product(("right", "wrong"), repeat=5) if "wrong" in s]
NATURAL = ("wrong", "right", "wrong", "wrong", "wrong")   # every order priced on the formula, gross, asking, January


def _scale(f1):
    return 1.0 if f1 == "wrong" else 1.0 / (1.0 + P.VAT_RATE)


def fee_cents_mem(O, f1="right", f2="right", p1="right", hz2="right", hz1="right"):
    """Fee income in cents per order under one reading of the five fee devices: f1 wrong books the fee
    with its VAT; f2 wrong charges nothing on a purchase with no payment record (balance-paid included);
    p1 wrong charges a pickup paid in person; hz2 wrong prices on the asking price; hz1 wrong takes the
    register's January 2027 row."""
    fixed = {"right": 80, "jan": 95, "wrong": 95, "old": 70}[hz1]
    inperson = O.inperson.to_numpy().astype(bool)
    wallet = O.wallet.to_numpy().astype(bool)
    price = O.asking.to_numpy() if hz2 == "wrong" else O.paid.to_numpy()
    f = (fixed + 5 * price.astype(int)).astype(float)
    if p1 == "right":
        f = np.where(inperson, 0.0, f)
    if f2 == "wrong":
        f = np.where(wallet, 0.0, f)
    return f * _scale(f1)


def grid_mem(W, values, mask):
    S, O = W.S, W.O
    v = np.where(mask, values, 0).astype(float)
    tot = np.bincount(O.sid.to_numpy(), weights=v, minlength=len(S))
    out = {}
    cell = S.cell.to_numpy()
    arm = S.arm.to_numpy()
    for c in range(8):
        base = tot[(cell == c) & (arm == 0)].mean()
        for k in range(1, 7):
            g = (cell == c) & (arm == k)
            out[(k, c)] = (tot[g].mean() - base) * 1000
    return out


def combo_grids(W):
    """The golden fee grid (cents per 1,000 sessions) and every reading the ask ledger names: the 31
    subsets of the five devices mishandled, the natural read (every order priced on the formula, VAT in,
    asking price, January row, in-session orders only) and the golden with VAT taken off order by order
    to the cent."""
    w = _window(W)
    gold = grid_mem(W, fee_cents_mem(W.O), w)
    combos = {key: grid_mem(W, fee_cents_mem(W.O, *key), w) for key in SUBSETS}
    ins = W.O.kind.isin(["insession_new", "insession_watched"]).to_numpy()
    combos["natural"] = grid_mem(W, fee_cents_mem(W.O, *NATURAL), w & ins)
    gross = fee_cents_mem(W.O, f1="wrong")
    combos["vat_per_order"] = grid_mem(W, np.round(gross / (1 + P.VAT_RATE)), w)
    return gold, combos


def bin_pos(v_euros):
    """Position of a one-decimal figure inside its bin: 0 at the lower edge, 1 at the upper."""
    x = v_euros * 10
    return x - np.floor(x + 0.5) + 0.5


READINGS = SUBSETS + ["natural"]


def place_fee_cells(W):
    """Place each policy-cell fee figure (euros per 1,000 sessions, VAT excluded) inside its bin, at least
    0.035 from both edges, and make every subset of the five fee devices, and the natural read, carry it
    out of the bin.

    Four levers on the cell's own in-session orders, so the incumbent's figures never move: the price of
    a plain order (no offer, shipped, paid through the provider; asking and paid together) moves the
    figure and every reading alike; the asking price of an order bought on an accepted offer (price paid
    unchanged) moves only the readings priced on the asking price; the price of an order collected and
    paid in person moves only the readings that charge those orders; and paying a plain order from a
    balance instead of through the provider (or the reverse) moves only the readings that charge nothing
    without a payment record. The search takes the smallest set of moves that clears every reading by the
    most, up to 0.05."""
    S, O = W.S, W.O
    w = _window(W)
    gold, combos = combo_grids(W)
    rng = P.stream("place-fee")
    kind = O.kind.to_numpy()
    otype = O.otype.to_numpy()
    inperson = O.inperson.to_numpy().astype(bool)
    wallet = O.wallet.to_numpy().astype(bool)
    asking, paid = O.asking.to_numpy(), O.paid.to_numpy()
    plain_any = ((kind == "insession_new") & (otype == "none") & (O.delivery.to_numpy() == "shipped") &
                 ~inperson & (asking >= 6) & (asking <= 70))
    ins = np.isin(kind, ["insession_new", "insession_watched"])
    offer_lever = ins & (otype == "used") & ~inperson & ~wallet & (asking <= 90)
    person_lever = ins & inperson & (otype == "none") & (asking >= 3) & (asking <= 90)
    cell = S.cell.to_numpy()[O.sid.to_numpy()]
    arm = S.arm.to_numpy()[O.sid.to_numpy()]
    ca, cp, cw = O.columns.get_loc("asking"), O.columns.get_loc("paid"), O.columns.get_loc("wallet")
    J = np.arange(-40, 41)
    flags = np.array([[k[i] == "wrong" for i in range(5)] for k in SUBSETS + [NATURAL]])   # (R, 5)
    sc = np.where(flags[:, 0], 1.0, 1.0 / (1.0 + P.VAT_RATE))
    fixed_r = np.where(flags[:, 4], 95.0, 80.0)
    moved = {}
    for (k, c), v in gold.items():
        m = int(((S.cell == c) & (S.arm == k)).sum())
        kk = 1000.0 / m / 100.0                   # cents on one order -> euros per 1,000 sessions
        base = np.array([combos[key][(k, c)] for key in READINGS]) / 100.0
        g0 = v / 100.0
        grp = (cell == c) & (arm == k) & w
        idx_off = np.flatnonzero(offer_lever & grp)
        idx_per = np.flatnonzero(person_lever & grp)
        idx_off_dn = idx_off[(asking[idx_off] - paid[idx_off]) >= 2]
        plain_free = np.flatnonzero(plain_any & ~wallet & grp)
        plain_wal = np.flatnonzero(plain_any & wallet & grp)
        order_free = plain_free[rng.permutation(len(plain_free))]
        tpos = order_free[:min(12, max(0, len(order_free) - 45))]      # toggled to balance-paid
        jpool = order_free[len(tpos):]                                 # repriced (never toggled)
        tneg = plain_wal[rng.permutation(len(plain_wal))][:12]         # balance-paid toggled back
        H = np.arange(-min(30, len(idx_off_dn)), min(30, len(idx_off)) + 1)
        Pp = np.arange(-min(30, len(idx_per)), min(30, len(idx_per)) + 1)
        T = np.arange(-len(tneg), len(tpos) + 1)
        # per-reading shift for t toggles (only readings that charge nothing without a payment record)
        def cum(ids, sign):
            f = (fixed_r[None, :] + 5.0 * paid[ids][:, None]) * sc[None, :] * kk * flags[None, :, 1]
            return sign * np.vstack([np.zeros((1, len(sc))), np.cumsum(f, axis=0)])
        tshift = np.vstack([cum(tneg, +1.0)[::-1][:-1], cum(tpos, -1.0)])        # rows match T
        dj = 5.0 * sc * kk
        dh = dj * flags[:, 3]
        dp = dj * flags[:, 2]
        gj = g0 + J * 5.0 * kk / (1.0 + P.VAT_RATE)
        pos = bin_pos(gj)
        okj = (pos >= 0.35) & (pos <= 0.65)
        best = None
        for ji in np.flatnonzero(okj):
            lo = gj[ji] - pos[ji] / 10
            hi = lo + 0.1
            # readings (R,) + h (H) + p (P) + t (T)
            R = base + J[ji] * dj
            X = (R[None, None, None, :] + H[:, None, None, None] * dh[None, None, None, :] +
                 Pp[None, :, None, None] * dp[None, None, None, :] + tshift[None, None, :, :])
            clear = np.maximum(X - hi, lo - X).min(axis=3)
            cost = (np.abs(H)[:, None, None] + np.abs(Pp)[None, :, None] + np.abs(T)[None, None, :] + abs(J[ji]))
            score = np.minimum(clear, 0.05) * 2e3 - cost
            i = np.unravel_index(int(np.argmax(score)), score.shape)
            cand = (score[i], ji, int(H[i[0]]), int(Pp[i[1]]), int(T[i[2]]), float(clear[i]))
            if best is None or cand[0] > best[0]:
                best = cand
        _, ji, h, pp, t, clr = best
        j = int(J[ji])
        if j != 0:
            pick = rng.choice(jpool, size=abs(j), replace=abs(j) > len(jpool))
            for q in pick:
                O.iat[q, ca] += int(np.sign(j))
                O.iat[q, cp] += int(np.sign(j))
        if h != 0:
            pool = idx_off if h > 0 else idx_off_dn
            for q in rng.choice(pool, size=abs(h), replace=False):
                O.iat[q, ca] += int(np.sign(h))
        if pp != 0:
            for q in rng.choice(idx_per, size=abs(pp), replace=False):
                O.iat[q, ca] += int(np.sign(pp))
                O.iat[q, cp] += int(np.sign(pp))
        if t > 0:
            for q in tpos[:t]:
                O.iat[q, cw] = True
        elif t < 0:
            for q in tneg[:-t]:
                O.iat[q, cw] = False
        moved[(k, c)] = (j, h, pp, t, round(clr, 4))
    W.fee_moves = moved
    return moved


def fee_grid_now(W):
    gold, _ = combo_grids(W)
    return {k: v / 100 for k, v in gold.items()}


def orders_grid_now(W):
    w = _window(W)
    return grid_mem(W, np.ones(len(W.O)), w)


def choose_traffic_adjust(W, orders_g, fee_g):
    """Per-cell factors on the 2026-W01 to W12 traffic (each within 1.5 per cent of 1) that put every
    policy's slot totals (extra orders and extra fee income) between 20 and 45 from the edges of their
    hundred, well inside it and never on the round hundred itself, and every wrong reading of them at
    least 5 outside that hundred: the first release, all twelve weeks on the app, both together, the
    natural read, and for the fee every subset of the five fee devices under each of those traffic
    readings. The pooled readings (one lift on the logged mix times the planned total, which the capacity
    note's cell-by-cell line refuses) sit at least 5 from the golden hundred's edges on whichever side
    they fall. Every total is linear in the factors, so 200,000 candidate factor vectors are scored at
    once."""
    tt = Tr.true_table()
    r1 = Tr.first_release(tt)
    arm = {"cur": Tr.arm_sessions(tt), "r1": Tr.arm_sessions(r1),
           "cur12": Tr.arm_sessions(tt, app_weeks=P.ISO_WEEKS_SLOT),
           "r1_12": Tr.arm_sessions(r1, app_weeks=P.ISO_WEEKS_SLOT)}
    wlog = P.N_CELL / P.N_CELL.sum()
    w = _window(W)
    ins = W.O.kind.isin(["insession_new", "insession_watched"]).to_numpy()
    in_g = grid_mem(W, np.ones(len(W.O)), w & ins)
    gold_c, combos_c = combo_grids(W)
    STOP, EITHER = 0, 1
    rows, golden_of, kind = [], [], []

    def add(v, g, k):
        rows.append(v)
        golden_of.append(g)
        kind.append(k)
    for k in range(1, 7):
        lo = np.array([orders_g[(k, c)] for c in range(8)]) / 1000
        g_idx = len(rows)
        add(lo * arm["cur"], -1, -1)
        pooled_in = float((wlog * np.array([in_g[(k, c)] for c in range(8)]) / 1000).sum())
        for v in (lo * arm["r1"], lo * arm["cur12"], lo * arm["r1_12"], pooled_in * arm["r1_12"]):
            add(v, g_idx, STOP)
        add(float((wlog * lo).sum()) * arm["cur"], g_idx, EITHER)          # pooled kept lift x planned total
        fg = np.array([fee_g[(k, c)] for c in range(8)]) / 1000
        g_idx = len(rows)
        add(fg * arm["cur"], -1, -1)
        add(float((wlog * fg).sum()) * arm["cur"], g_idx, EITHER)          # pooled fee lift x planned total
        nat = np.array([combos_c["natural"][(k, c)] for c in range(8)]) / 100 / 1000
        add(nat * arm["r1_12"], g_idx, STOP)
        grids = [gold_c] + [combos_c[key] for key in SUBSETS]
        for p2, hz3 in itertools.product((False, True), repeat=2):
            a = arm[{(False, False): "cur", (True, False): "r1", (False, True): "cur12", (True, True): "r1_12"}[(p2, hz3)]]
            for gi, g in enumerate(grids):
                if not p2 and not hz3 and gi == 0:
                    continue
                add(np.array([g[(k, c)] for c in range(8)]) / 100 / 1000 * a, g_idx, STOP)
    V = np.array(rows)                                   # (readings, 8)
    gof = np.array(golden_of)
    kd = np.array(kind)
    is_g = gof < 0
    # a wrong reading that sits under 30 from its golden total on the unadjusted traffic cannot be carried
    # out of the hundred while the golden sits 20 from the edges: it is placed at least 5 from the edges
    # on whichever side it falls, and the record names it
    t0 = V.sum(axis=1)
    near = (kd == STOP) & (np.abs(t0 - t0[np.where(is_g, np.arange(len(gof)), gof)]) < 30)
    kd[near] = EITHER
    W.traffic_near = [int(i) for i in np.flatnonzero(near)]
    is_s, is_e = kd == STOP, kd == EITHER
    rng = P.stream("place-traffic")

    def scored(Fc):
        tot = Fc @ V.T                                   # (cands, readings)
        G = tot[:, is_g]
        edge = 50 - np.abs(np.mod(G + 50, 100) - 50)
        sg = np.minimum(edge - 20, 45 - edge).min(axis=1)
        gl = np.floor(tot / 100 + 0.5) * 100 - 50       # lower edge of each total's own bin
        ref = gl[:, np.where(is_g, np.arange(len(gof)), gof)]
        out = np.maximum(ref - tot, tot - (ref + 100))    # > 0 outside the golden's hundred, < 0 inside
        sw = (out[:, is_s] - 5).min(axis=1)
        se = (np.abs(out[:, is_e]) - 5).min(axis=1)
        score = np.minimum(np.minimum(sg, sw), se)
        i = int(np.argmax(score))
        return float(score[i]), Fc[i].copy(), float(edge[i].min()), float(out[i][is_s].min())

    best = None
    for s0 in range(10):
        Fc = 1 + rng.uniform(-0.015, 0.015, size=(20_000, 8))
        if s0 == 0:
            Fc[0] = 1.0
        b = scored(Fc)
        if best is None or b[0] > best[0]:
            best = b
    # local refinement around the best vector, inside the same 1.5 per cent box
    for step in (0.004, 0.002, 0.001, 0.0005):
        for _ in range(5):
            Fc = np.clip(best[1] + rng.normal(0, step, size=(20_000, 8)), 0.985, 1.015)
            b = scored(Fc)
            if b[0] > best[0]:
                best = b
    W.traffic_score = best
    return best[1], best[2]
