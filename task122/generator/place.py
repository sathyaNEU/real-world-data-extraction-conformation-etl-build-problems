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


DEVICES = ("f1", "f2", "fc", "hz2", "hz1")       # VAT, balance-paid, the checkout in force, price paid, newest row
HAZ = list(itertools.product(("right", "wrong"), repeat=4))          # (f1, f2, hz2, hz1)
# FC, the checkout the slot runs on: "new" is Checkout 3 (every order paid at checkout, so every order carries the
# fee; the golden's), "old" the logged window's checkout (a pickup paid to the seller at the handover carries none)
FC = ("new", "old")
GOLD = ("right", "right", "new", "right", "right")
READ_KEYS = [(h[0], h[1], fc, h[2], h[3]) for fc in FC for h in HAZ if (h[0], h[1], fc, h[2], h[3]) != GOLD]
NATURAL = ("wrong", "right", "new", "wrong", "wrong")   # every order priced on the formula, gross, asking, newest row


def _scale(f1):
    return 1.0 if f1 == "wrong" else 1.0 / (1.0 + P.VAT_RATE)


def fee_cents_mem(O, f1="right", f2="right", cover="new", hz2="right", hz1="right"):
    """Fee income in cents per order under one checkout and one reading of the four hazards: cover new charges every
    order (Checkout 3, the slot's), cover old leaves a pickup paid in person uncharged (the logged window's checkout);
    f1 wrong books the fee with its VAT; f2 wrong charges nothing on a purchase with no payment record (balance-paid);
    hz2 wrong prices on the asking price; hz1 wrong takes the register's newest row."""
    fixed = {"right": P.SLOT_FIXED_CENTS, "wrong": P.LATEST_FIXED_CENTS}[hz1]
    inperson = O.inperson.to_numpy().astype(bool)
    wallet = O.wallet.to_numpy().astype(bool)
    price = O.asking.to_numpy() if hz2 == "wrong" else O.paid.to_numpy()
    f = (fixed + 5 * price.astype(int)).astype(float)
    if cover == "old":
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


def reading_grid(G, key):
    f1, f2, cov, hz2, hz1 = key
    return G[((f1, f2, hz2, hz1), cov)]


def combo_grids(W):
    """The golden fee grid (cents per 1,000 sessions) and every reading the ask ledger names: the checkout's two
    states by the 16 readings of the four hazards (31 wrong ones), the natural read (every order priced on the
    formula, VAT in, asking price, the register's newest row, in-session orders only) and the golden with VAT taken
    off order by order to the cent. The per-cover grids are kept on W for the traffic placement."""
    w = _window(W)
    G = {}
    for h in HAZ:
        for cov in FC:
            G[(h, cov)] = grid_mem(W, fee_cents_mem(W.O, h[0], h[1], cov, h[2], h[3]), w)
    gold = reading_grid(G, GOLD)
    combos = {key: reading_grid(G, key) for key in READ_KEYS}
    ins = W.O.kind.isin(["insession_new", "insession_watched"]).to_numpy()
    combos["natural"] = grid_mem(W, fee_cents_mem(W.O, *NATURAL), w & ins)
    combos["vat_per_order"] = grid_mem(W, np.round(fee_cents_mem(W.O, f1="wrong", cover="new") / (1 + P.VAT_RATE)),
                                       w)
    W.fee_cover_grids = G
    return gold, combos


def bin_pos(v_euros):
    """Position of a one-decimal figure inside its bin: 0 at the lower edge, 1 at the upper."""
    x = v_euros * 10
    return x - np.floor(x + 0.5) + 0.5


READINGS = READ_KEYS + ["natural"]


def place_fee_cells(W):
    """Place each policy-cell fee figure (euros per 1,000 sessions, VAT excluded, every order charged as under
    Checkout 3) inside its bin, at least 0.035 from both edges and 0.005 from the round one-decimal value, and make
    every one of the 31 wrong readings, and the natural read, carry it out of the bin.

    Four levers on the cell's own in-session orders, so the incumbent's figures never move: the price of a plain
    order (no offer, shipped, paid through the provider; asking and paid together) moves the figure and every
    reading alike; the asking price of an order bought on an accepted offer (price paid unchanged) moves only the
    readings priced on the asking price; the price of an order collected and paid in person moves the golden and
    every reading on Checkout 3 and none on the logged window's checkout; and paying a plain order from a balance
    instead of through the provider (or the
    reverse) moves only the readings that charge nothing without a payment record. The search takes the smallest
    set of moves that clears every reading by the most, up to 0.05."""
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
    keys = READ_KEYS + [NATURAL]
    f1w = np.array([k[0] == "wrong" for k in keys])
    f2w = np.array([k[1] == "wrong" for k in keys])
    fxs = np.array([k[2] for k in keys])
    hz2w = np.array([k[3] == "wrong" for k in keys])
    hz1w = np.array([k[4] == "wrong" for k in keys])
    sc = np.where(f1w, 1.0, 1.0 / (1.0 + P.VAT_RATE))
    fixed_r = np.where(hz1w, float(P.LATEST_FIXED_CENTS), float(P.SLOT_FIXED_CENTS))
    moved = {}
    for (k, c), v in gold.items():
        m = int(((S.cell == c) & (S.arm == k)).sum())
        kk = 1000.0 / m / 100.0                   # cents on one order -> euros per 1,000 sessions
        base = np.array([combos[key][(k, c)] for key in READINGS]) / 100.0
        g0 = v / 100.0
        cov = np.where(fxs == "new", 1.0, 0.0)
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
        Pp = np.arange(-min(60, 3 * len(idx_per)), min(60, 3 * len(idx_per)) + 1)   # up to three euros an order
        T = np.arange(-len(tneg), len(tpos) + 1)

        def cum(ids, sign):
            f = (fixed_r[None, :] + 5.0 * paid[ids][:, None]) * sc[None, :] * kk * f2w[None, :]
            return sign * np.vstack([np.zeros((1, len(sc))), np.cumsum(f, axis=0)])
        tshift = np.vstack([cum(tneg, +1.0)[::-1][:-1], cum(tpos, -1.0)])        # rows match T
        dj = 5.0 * sc * kk
        dh = dj * hz2w
        dp = dj * cov
        dj_g = 5.0 * kk / (1.0 + P.VAT_RATE)
        dp_g = dj_g
        best = None
        for pi_, pp in enumerate(Pp):
            gj = g0 + J * dj_g + pp * dp_g
            pos = bin_pos(gj)
            okj = (pos >= 0.35) & (pos <= 0.65) & (np.abs(pos - 0.5) >= 0.05)   # mid-bin, never on the round value
            for ji in np.flatnonzero(okj):
                lo = gj[ji] - pos[ji] / 10
                hi = lo + 0.1
                R = base + J[ji] * dj + pp * dp
                X = R[None, None, :] + H[:, None, None] * dh[None, None, :] + tshift[None, :, :]
                clear = np.maximum(X - hi, lo - X).min(axis=2)
                cost = np.abs(H)[:, None] + np.abs(T)[None, :] + abs(int(J[ji])) + abs(int(pp))
                score = np.minimum(clear, 0.05) * 2e3 - cost
                i = np.unravel_index(int(np.argmax(score)), score.shape)
                cand = (score[i], ji, int(H[i[0]]), int(pp), int(T[i[1]]), float(clear[i]))
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
            order_p = idx_per[rng.permutation(len(idx_per))]
            for u in range(abs(pp)):
                q = order_p[u % len(order_p)]
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


def _vat_err(price):
    """Rounding error (cents) of a slot-tariff fee taken off its VAT order by order: round(f / 1.21) - f / 1.21."""
    f = 80.0 + 5.0 * np.asarray(price, float)
    return np.round(f / (1 + P.VAT_RATE)) - f / (1 + P.VAT_RATE)


def fix_vat_rounding(W, need=0.012):
    """Make VAT taken off order by order to the cent file the same grid as VAT taken off the cell's total. In any
    cell where that per-order reading sits within `need` of the golden bin's edge (or outside it), reprice pairs of
    the cell's plain in-session orders by plus and minus one euro: the golden and every device reading move by +5
    and -5 cents and so stay where they are, and only the per-order rounding moves."""
    S, O = W.S, W.O
    w = _window(W)
    gold, combos = combo_grids(W)
    vp = combos["vat_per_order"]
    kind, otype = O.kind.to_numpy(), O.otype.to_numpy()
    inperson = O.inperson.to_numpy().astype(bool)
    wallet = O.wallet.to_numpy().astype(bool)
    asking = O.asking.to_numpy()
    plain = ((kind == "insession_new") & (otype == "none") & (O.delivery.to_numpy() == "shipped") & ~inperson &
             ~wallet & (asking >= 7) & (asking <= 69))
    cell = S.cell.to_numpy()[O.sid.to_numpy()]
    arm = S.arm.to_numpy()[O.sid.to_numpy()]
    ca, cp = O.columns.get_loc("asking"), O.columns.get_loc("paid")
    fixes = {}
    for (k, c), g in gold.items():
        gv, x = g / 100.0, vp[(k, c)] / 100.0
        lo = (np.floor(gv * 10 + 0.5) - 0.5) / 10
        hi = lo + 0.1
        if min(x - lo, hi - x) >= need:
            continue
        m = int(((S.cell == c) & (S.arm == k)).sum())
        kk = 1000.0 / m / 100.0
        want = ((lo + need + 0.003) - x) if (x - lo) < (hi - x) else ((hi - need - 0.003) - x)
        idx = np.flatnonzero(plain & (cell == c) & (arm == k) & w)
        pr = O.paid.to_numpy()[idx].astype(float)
        up = _vat_err(pr + 1) - _vat_err(pr)
        dn = _vat_err(pr - 1) - _vat_err(pr)
        sgn = np.sign(want)
        a_ord = np.argsort(-sgn * up)
        b_ord = np.argsort(-sgn * dn)
        used, done, pairs = set(), 0.0, 0
        ia = ib = 0
        while sgn * done < sgn * want / kk and ia < len(a_ord) and ib < len(b_ord):
            a = a_ord[ia]
            b = b_ord[ib]
            if a in used:
                ia += 1
                continue
            if b in used or b == a:
                ib += 1
                continue
            gain = up[a] + dn[b]
            if sgn * gain <= 0:
                break
            used.update((a, b))
            done += gain
            pairs += 1
            O.iat[idx[a], ca] += 1
            O.iat[idx[a], cp] += 1
            O.iat[idx[b], ca] -= 1
            O.iat[idx[b], cp] -= 1
            ia += 1
            ib += 1
        fixes[(k, c)] = (pairs, round(done * kk, 4), round(want, 4))
    W.vat_fixes = fixes
    return fixes


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
    tabs = {"cur": (tt, P.APP_WEEKS), "r1": (r1, P.APP_WEEKS), "cur12": (tt, P.ISO_WEEKS_SLOT),
            "r1_12": (r1, P.ISO_WEEKS_SLOT)}
    arm = {k: Tr.arm_sessions(tab, app_weeks=aw) for k, (tab, aw) in tabs.items()}
    wlog = P.N_CELL / P.N_CELL.sum()
    w = _window(W)
    ins = W.O.kind.isin(["insession_new", "insession_watched"]).to_numpy()
    in_g = grid_mem(W, np.ones(len(W.O)), w & ins)
    gold_c, combos_c = combo_grids(W)
    G = W.fee_cover_grids
    STOP, EITHER = 0, 1
    rows, golden_of, kind, names = [], [], [], []

    def add(v, g, k, nm=""):
        rows.append(v)
        golden_of.append(g)
        kind.append(k)
        names.append(nm)

    def fee_row(k, key, tk):
        """Per-cell coefficients (EUR) of a fee total: the planned sessions on the reading's traffic times the
        reading's fee per session in the cell."""
        A_ = np.array([reading_grid(G, key)[(k, c)] for c in range(8)]) / 100 / 1000
        return arm[tk] * A_
    for k in range(1, 7):
        lo = np.array([orders_g[(k, c)] for c in range(8)]) / 1000
        g_idx = len(rows)
        add(lo * arm["cur"], -1, -1, f"{k}|orders")
        pooled_in = float((wlog * np.array([in_g[(k, c)] for c in range(8)]) / 1000).sum())
        for nm, v in (("r1", lo * arm["r1"]), ("cur12", lo * arm["cur12"]), ("r1_12", lo * arm["r1_12"]),
                      ("natural", pooled_in * arm["r1_12"])):
            add(v, g_idx, STOP, f"{k}|orders|{nm}")
        add(float((wlog * lo).sum()) * arm["cur"], g_idx, EITHER, f"{k}|orders|pooled")
        fg = np.array([fee_g[(k, c)] for c in range(8)]) / 1000
        g_idx = len(rows)
        add(fee_row(k, GOLD, "cur"), -1, -1, f"{k}|fee")
        add(float((wlog * fg).sum()) * arm["cur"], g_idx, EITHER, f"{k}|fee|pooled")
        nat = np.array([combos_c["natural"][(k, c)] for c in range(8)]) / 100 / 1000
        add(nat * arm["r1_12"], g_idx, STOP, f"{k}|fee|natural")
        for tk in ("cur", "r1", "cur12", "r1_12"):
            for key in [GOLD] + READ_KEYS:
                if tk == "cur" and key == GOLD:
                    continue
                add(fee_row(k, key, tk), g_idx, STOP, f"{k}|fee|{tk}|{'-'.join(key)}")
    V = np.array(rows)                                   # (readings, 8)
    gof = np.array(golden_of)
    kd = np.array(kind)
    is_g = gof < 0
    # a wrong reading that sits under 56 from its golden total on the unadjusted traffic cannot always be carried
    # out of the hundred while the golden sits 20 from the edges (two readings 52 above and 55 below one golden
    # cannot both clear a hundred-wide bin by 5): it is placed at least 5 from the edges on whichever side it
    # falls, and the record names it
    t0 = V.sum(axis=1)
    near = (kd == STOP) & (np.abs(t0 - t0[np.where(is_g, np.arange(len(gof)), gof)]) < 56)
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
    for step in (0.004, 0.002, 0.001, 0.0005, 0.00025, 0.000125):
        for _ in range(10):
            Fc = np.clip(best[1] + rng.normal(0, step, size=(20_000, 8)), 0.985, 1.015)
            b = scored(Fc)
            if b[0] > best[0]:
                best = b
    W.traffic_score = best
    tot = best[1] @ V.T
    gl = np.floor(tot / 100 + 0.5) * 100 - 50
    ref = gl[np.where(is_g, np.arange(len(gof)), gof)]
    out = np.maximum(ref - tot, tot - (ref + 100))
    order = np.argsort(np.where(is_s, out, np.abs(out)))
    W.traffic_binding = [(names[i], round(float(out[i]), 2), "stop" if is_s[i] else "either") for i in order[:6]
                         if not is_g[i]]
    W.traffic_near_names = [names[i] for i in W.traffic_near]
    return best[1], best[2]
