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


def fee_cents_mem(O, p1="right", hz2="right", hz1="right"):
    fixed = {"right": 80, "jan": 95, "old": 70}[hz1]
    price = O.asking.to_numpy() if hz2 == "asking" else np.where(O.inperson.to_numpy(), O.asking.to_numpy(),
                                                                   O.paid.to_numpy())
    f = fixed + 5 * price.astype(int)
    if p1 == "right":
        f = np.where(O.inperson.to_numpy(), 0, f)
    return f


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
    w = _window(W)
    gold = grid_mem(W, fee_cents_mem(W.O), w)
    combos = {}
    for key in itertools.product(("right", "wrong"), ("right", "asking"), ("right", "jan")):
        if key == ("right", "right", "right"):
            continue
        combos[key] = grid_mem(W, fee_cents_mem(W.O, *key), w)
    # the natural read: every device mishandled, in-session orders only
    ins = W.O.kind.isin(["insession_new", "insession_watched"]).to_numpy()
    combos["natural"] = grid_mem(W, fee_cents_mem(W.O, "wrong", "asking", "jan"), w & ins)
    return gold, combos


def bin_pos(v_euros):
    """Position of a one-decimal figure inside its bin: 0 at the lower edge, 1 at the upper."""
    x = v_euros * 10
    return x - np.floor(x + 0.5) + 0.5


COMBOS = [("right", "right", "jan"), ("right", "asking", "right"), ("right", "asking", "jan"),
          ("wrong", "right", "right"), ("wrong", "right", "jan"), ("wrong", "asking", "right"),
          ("wrong", "asking", "jan"), "natural"]


def place_fee_cells(W):
    """Place each policy-cell fee figure (euros per 1,000 sessions) inside its bin, at least 0.035 from
    both edges, and make every combination of the three formula devices carry it out of the bin.

    Three levers, each a whole euro on one order of the cell's own group, so the incumbent's figures
    never move: the price of a plain order (no offer, shipped, paid through checkout; asking and paid
    together) moves the figure and every reading of it alike; the asking price of an order bought on
    an accepted offer (paid through checkout, price paid unchanged) moves only the readings that price
    on the asking price; the price of an order collected and paid in person moves only the readings
    that charge those orders a fee. The search takes the smallest set of moves that clears every
    combination by the most, up to 0.05."""
    S, O = W.S, W.O
    w = _window(W)
    gold, combos = combo_grids(W)
    rng = P.stream("place-fee")
    kind = O.kind.to_numpy()
    otype = O.otype.to_numpy()
    inperson = O.inperson.to_numpy().astype(bool)
    asking, paid = O.asking.to_numpy(), O.paid.to_numpy()
    plain = ((kind == "insession_new") & (otype == "none") & (O.delivery.to_numpy() == "shipped") & ~inperson &
             (asking >= 6) & (asking <= 70))
    ins = np.isin(kind, ["insession_new", "insession_watched"])
    offer_lever = ins & (otype == "used") & ~inperson & (asking <= 90)
    person_lever = ins & inperson & (otype == "none") & (asking >= 3) & (asking <= 90)
    cell = S.cell.to_numpy()[O.sid.to_numpy()]
    arm = S.arm.to_numpy()[O.sid.to_numpy()]
    ca, cp = O.columns.get_loc("asking"), O.columns.get_loc("paid")
    J = np.arange(-40, 41)
    moved = {}
    for (k, c), v in gold.items():
        m = int(((S.cell == c) & (S.arm == k)).sum())
        u = 0.05 * 1000 / m                  # euros per 1,000 sessions for one euro on one order
        sh = np.array([combos[key][(k, c)] / 100 - v / 100 for key in COMBOS])
        grp = (cell == c) & (arm == k) & w
        idx_off = np.flatnonzero(offer_lever & grp)
        idx_per = np.flatnonzero(person_lever & grp)
        idx_off_dn = idx_off[(asking[idx_off] - paid[idx_off]) >= 2]
        H = np.arange(-min(30, len(idx_off_dn)), min(30, len(idx_off)) + 1)
        Pp = np.arange(-min(30, len(idx_per)), min(30, len(idx_per)) + 1)
        x = v / 100 + J * u                                       # (J,)
        pos = bin_pos(x)
        ok = (pos >= 0.35) & (pos <= 0.65)
        lo = x - pos / 10
        hi = lo + 0.1
        X, Hh, PP = np.meshgrid(x, H, Pp, indexing="ij")
        LO, HI = np.meshgrid(lo, H, Pp, indexing="ij")[0], np.meshgrid(hi, H, Pp, indexing="ij")[0]
        OK = np.meshgrid(ok, H, Pp, indexing="ij")[0]
        hu, pu = Hh * u, PP * u
        shifts = [sh[0] + 0 * hu, sh[1] + hu, sh[2] + hu, sh[3] + pu, sh[4] + pu, sh[5] + hu + pu, sh[6] + hu + pu,
                  sh[7] + hu + pu]
        clear = np.min([np.maximum(X + s_ - HI, LO - (X + s_)) for s_ in shifts], axis=0)
        cost = np.abs(Hh) + np.abs(PP) + np.abs(np.meshgrid(J, H, Pp, indexing="ij")[0])
        score = np.where(OK, np.minimum(clear, 0.05) * 2e3 - cost, -1e18)
        i = np.unravel_index(int(np.argmax(score)), score.shape)
        j, h, pp = int(J[i[0]]), int(H[i[1]]), int(Pp[i[2]])
        if j != 0:
            idx = np.flatnonzero(plain & grp)
            pick = rng.choice(idx, size=abs(j), replace=abs(j) > len(idx))
            for t in pick:
                O.iat[t, ca] += int(np.sign(j))
                O.iat[t, cp] += int(np.sign(j))
        if h != 0:
            pool = idx_off if h > 0 else idx_off_dn
            pick = rng.choice(pool, size=abs(h), replace=False)
            for t in pick:
                O.iat[t, ca] += int(np.sign(h))
        if pp != 0:
            pick = rng.choice(idx_per, size=abs(pp), replace=False)
            for t in pick:
                O.iat[t, ca] += int(np.sign(pp))
                O.iat[t, cp] += int(np.sign(pp))
        moved[(k, c)] = (j, h, pp, round(float(clear[i]), 4))
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
    pooled lift on the planned total, the natural read, and for the fee every subset of the five
    devices. Every total is linear in the factors, so 200,000 candidate factor vectors are scored at
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
    rows, golden_of = [], []
    for k in range(1, 7):
        lo = np.array([orders_g[(k, c)] for c in range(8)]) / 1000
        g_idx = len(rows)
        rows.append(lo * arm["cur"])
        golden_of.append(-1)
        pooled_k = float((wlog * lo).sum())
        pooled_in = float((wlog * np.array([in_g[(k, c)] for c in range(8)]) / 1000).sum())
        for v in (lo * arm["r1"], lo * arm["cur12"], lo * arm["r1_12"], pooled_k * arm["cur"],
                  pooled_in * arm["r1_12"]):
            rows.append(v)
            golden_of.append(g_idx)
        fg = np.array([fee_g[(k, c)] for c in range(8)]) / 1000
        g_idx = len(rows)
        rows.append(fg * arm["cur"])
        golden_of.append(-1)
        grids = [gold_c] + [combos_c[key] for key in COMBOS if key != "natural"]
        for p2, hz3 in itertools.product((False, True), repeat=2):
            a = arm[{(False, False): "cur", (True, False): "r1", (False, True): "cur12", (True, True): "r1_12"}[(p2, hz3)]]
            for gi, g in enumerate(grids):
                if not p2 and not hz3 and gi == 0:
                    continue
                rows.append(np.array([g[(k, c)] for c in range(8)]) / 100 / 1000 * a)
                golden_of.append(g_idx)
    V = np.array(rows)                                   # (readings, 8)
    gof = np.array(golden_of)
    is_g = gof < 0
    rng = P.stream("place-traffic")

    def scored(Fc):
        tot = Fc @ V.T                                   # (cands, readings)
        G = tot[:, is_g]
        edge = 50 - np.abs(np.mod(G + 50, 100) - 50)
        sg = np.minimum(edge - 20, 45 - edge).min(axis=1)
        gl = np.floor(tot / 100 + 0.5) * 100 - 50       # lower edge of each total's own bin
        ref = gl[:, np.where(is_g, np.arange(len(gof)), gof)]
        out = np.maximum(ref - tot, tot - (ref + 100))[:, ~is_g]
        sw = (out - 5).min(axis=1)
        score = np.minimum(sg, sw)
        i = int(np.argmax(score))
        return float(score[i]), Fc[i].copy(), float(edge[i].min()), float(out[i].min())

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
