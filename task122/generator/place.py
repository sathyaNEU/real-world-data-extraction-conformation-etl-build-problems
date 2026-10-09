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
    return gold, combos


def bin_pos(v_euros):
    """Position of a one-decimal figure inside its bin: 0 at the lower edge, 1 at the upper."""
    x = v_euros * 10
    return x - np.floor(x + 0.5) + 0.5


def place_fee_cells(W):
    """Move each policy-cell fee figure (euros per 1,000 sessions) to the position inside its bin
    that keeps it at least 0.035 from both edges and as far as possible toward the edge every
    formula device pushes it across."""
    S, O = W.S, W.O
    w = _window(W)
    gold, combos = combo_grids(W)
    rng = P.stream("place-fee")
    plain = ((O.kind == "insession_new") & (O.otype == "none") & (O.delivery == "shipped") &
             (~O.inperson.astype(bool)) & (O.asking >= 6) & (O.asking <= 70)).to_numpy()
    cell = S.cell.to_numpy()[O.sid.to_numpy()]
    arm = S.arm.to_numpy()[O.sid.to_numpy()]
    moved = {}
    for (k, c), v in gold.items():
        m = int(((S.cell == c) & (S.arm == k)).sum())
        step = 0.05 / m * 1000          # one euro on one order's price moves the cell by this much (euros)
        shifts = [combos[key][(k, c)] / 100 - v / 100 for key in combos]
        cur = v / 100
        best = None
        for j in range(-40, 41):
            nv = cur + j * step
            pos = bin_pos(nv)
            if pos < 0.35 or pos > 0.65:
                continue
            # margin: the smallest amount by which any formula-device shift clears the bin
            lo_edge = nv - pos / 10
            hi_edge = lo_edge + 0.1
            clear = min(max(nv + s - hi_edge, lo_edge - (nv + s)) for s in shifts)
            score = (clear, -abs(j))
            if best is None or score > best[0]:
                best = (score, j)
        j = best[1]
        if j != 0:
            idx = np.flatnonzero(plain & (cell == c) & (arm == k) & w)
            pick = rng.choice(idx, size=abs(j), replace=abs(j) > len(idx))
            for i in pick:
                O.iat[i, O.columns.get_loc("asking")] += int(np.sign(j))
                O.iat[i, O.columns.get_loc("paid")] += int(np.sign(j))
        moved[(k, c)] = j
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
    policy's slot totals (extra orders and extra fee income) at least 25 inside their hundred. The
    totals are linear in the factors, so 200,000 candidate factor vectors are scored at once."""
    base_tbl = Tr.true_table()
    cur = base_tbl[(base_tbl.year == 2026) & (base_tbl.week <= 26)]
    arm0 = Tr.arm_sessions(cur)
    rng = P.stream("place-traffic")
    Ao = np.array([[orders_g[(k, c)] for c in range(8)] for k in range(1, 7)]) / 1000
    Af = np.array([[fee_g[(k, c)] for c in range(8)] for k in range(1, 7)]) / 1000
    F = 1 + rng.uniform(-0.015, 0.015, size=(200_000, 8))
    F[0] = 1.0
    arms = F * arm0[None, :]
    tot = np.hstack([arms @ Ao.T, arms @ Af.T])          # (trials, 12)
    margin = 50 - np.abs(np.mod(tot, 100) - 50)
    worst = margin.min(axis=1)
    i = int(np.argmax(worst))
    return F[i], float(worst[i])
