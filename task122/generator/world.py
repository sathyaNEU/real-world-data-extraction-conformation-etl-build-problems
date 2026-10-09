"""task122 generator: the logged carousel window and every order its buyers placed.

Construction, in the order it runs:

1. A block template per cell (BLOCK[c] sessions): the renders each session draws, the watch lists
   at session start (each watched listing with whether its watcher buys it within six days, the day
   and the price it would be bought at), and the orders the buyer places in the 21 days either side of
   the session that have nothing to do with the carousel. Every cell is 100 exact copies of its
   block, shuffled inside each copy, and each ranker takes whole copies, so every arm in a cell has the
   same renders, the same watch lists and the same background orders to the cent. That is what lets a
   difference between arms be read as the ranker's effect, by any estimator and over any window.
2. The rankers' in-session outcomes per (cell, ranker, renders): the incumbent's base rate, each
   policy's solved lift, the velocity boost's pinned watched listings.
3. Tiles, fresh listings, dates, clock times, and every order, offer and payment record.

Nothing here writes a file; writers.py does, and every figure the build asserts is recomputed from
the files as written.
"""
from collections import defaultdict
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P

ARM = {r: i for i, r in enumerate(P.RANKERS)}
B_IDX = ARM[P.STUMP]
D_IDX = ARM["HC-36"]
E_IDX = ARM["HC-37"]


def largest_remainder(weights, total):
    w = np.asarray(weights, float)
    if total == 0 or w.sum() == 0:
        return np.zeros(len(w), int)
    raw = w / w.sum() * total
    out = np.floor(raw).astype(int)
    rem = int(total - out.sum())
    order = np.argsort(-(raw - out), kind="stable")
    out[order[:rem]] += 1
    return out


def round8(x):
    return int(8 * round(x / 8.0))


def fee_cents(price_paid, inperson, fixed_cents=P.SLOT_FIXED_CENTS, pct=P.SLOT_PCT):
    """Slot-tariff fee in cents on a whole-euro price paid; nothing on a pickup paid in person."""
    return np.where(inperson, 0, fixed_cents + pct * np.asarray(price_paid, int))


# ------------------------------------------------------------------ block templates

def block_renders(c):
    u = int(P.BLOCK[c])
    H = P.render_dist(P.NBAR[c])
    counts = largest_remainder(H, u)
    return np.repeat(np.arange(1, P.NMAX + 1), counts)


def draw_order_attrs(rng, k, policy=None, offer_share=P.OFFER_SHARE):
    """Category, asking price, offer use, price paid, delivery and payment for k orders."""
    cat = rng.choice(len(P.CATEGORIES), size=k, p=P.CAT_P)
    asking = rng.choice(P.PRICE_POINTS, size=k, p=P.PRICE_W / P.PRICE_W.sum())
    u = rng.random(k)
    used = u < offer_share * (1 - P.OFFER_LAPSE)
    lapsed = (u >= offer_share * (1 - P.OFFER_LAPSE)) & (u < offer_share)
    disc = rng.uniform(*P.OFFER_DISC, size=k)
    offer = np.maximum(1, np.minimum(asking - 1, np.round(asking * (1 - disc)))).astype(int)
    offer = np.where(asking <= 4, asking, offer)
    used = used & (asking > 4)
    lapsed = lapsed & (asking > 4)
    paid = np.where(used, offer, asking).astype(int)
    key = policy if policy in P.PICKUP_INPERSON else "default"
    v = rng.random(k)
    inperson = v < P.PICKUP_INPERSON[key]
    inapp = (v >= P.PICKUP_INPERSON[key]) & (v < P.PICKUP_INPERSON[key] + P.PICKUP_INAPP[key])
    delivery = np.where(inperson | inapp, "pickup", "shipped")
    otype = np.where(used, "used", np.where(lapsed, "lapsed", "none"))
    return dict(cat=cat, asking=asking.astype(int), offer=np.where(used | lapsed, offer, 0).astype(int),
                otype=otype, paid=paid, delivery=delivery, inperson=inperson)


def _strata(n, probs):
    """Counts per category for n items by largest remainder (an exact replica of the shares)."""
    return largest_remainder(np.asarray(probs, float), n)


def stratified_attrs(rng, k, policy=None):
    """The same attributes as draw_order_attrs, but every share (asking price points, offers,
    discounts, pickups, categories) is a largest-remainder replica of its target for these k orders,
    so a group's fee per order sits on the cell's norm and a fee change tracks the orders added."""
    if k == 0:
        return draw_order_attrs(rng, 0, policy)
    pw = P.PRICE_W / P.PRICE_W.sum()
    asking = np.repeat(P.PRICE_POINTS, _strata(k, pw))
    cat = np.repeat(np.arange(len(P.CATEGORIES)), _strata(k, P.CAT_P))
    n_used = int(round(k * P.OFFER_SHARE * (1 - P.OFFER_LAPSE)))
    n_lapsed = int(round(k * P.OFFER_SHARE * P.OFFER_LAPSE))
    key = policy if policy in P.PICKUP_INPERSON else "default"
    n_ip = int(round(k * P.PICKUP_INPERSON[key]))
    n_ia = int(round(k * P.PICKUP_INAPP[key]))
    # offers go to orders spread evenly over the price range; discounts are evenly spaced
    order = np.argsort(asking, kind="stable")
    asking = asking[order]
    otype = np.array(["none"] * k, dtype=object)
    slots = np.floor((np.arange(n_used + n_lapsed) + 0.5) * k / max(1, n_used + n_lapsed)).astype(int)
    kinds = np.array(["used"] * n_used + ["lapsed"] * n_lapsed, dtype=object)
    kinds = kinds[rng.permutation(len(kinds))]
    otype[slots] = kinds
    disc = OFFER_DISC_GRID(len(slots), rng)
    offer = np.zeros(k, int)
    for j, s in enumerate(slots):
        if asking[s] > 4:
            offer[s] = int(max(1, min(asking[s] - 1, round(asking[s] * (1 - disc[j])))))
        else:
            otype[s] = "none"
    paid = np.where(otype == "used", offer, asking).astype(int)
    v = np.array(["shipped"] * k, dtype=object)
    inperson = np.zeros(k, bool)
    pslots = rng.permutation(k)
    inperson[pslots[:n_ip]] = True
    v[pslots[:n_ip + n_ia]] = "pickup"
    perm = rng.permutation(k)
    return dict(cat=cat[rng.permutation(k)], asking=asking[perm].astype(int), offer=offer[perm],
                otype=otype[perm], paid=paid[perm], delivery=v[perm], inperson=inperson[perm])


def OFFER_DISC_GRID(m, rng):
    lo, hi = P.OFFER_DISC
    g = lo + (hi - lo) * (np.arange(m) + 0.5) / max(1, m)
    return g[rng.permutation(m)]


LATER_CHANNELS = np.array(["favourites", "alerts", "search", "carousel"])
LATER_P = [0.45, 0.25, 0.20, 0.10]
BG_CHANNELS = np.array(["search", "carousel", "favourites", "alerts", "shop"])
BG_P = [0.45, 0.18, 0.15, 0.07, 0.15]


def block_watch(c, rng, rend, carry=None):
    """Watch-list sizes per slot and the block's watched-listing profiles, listed slot by slot. The
    block total is a multiple of 8 and exactly five in eight of its watched listings are bought by
    their watcher within six days of the session, allotted by largest remainder across strata of the
    slot's renders (1, 2, 3, 4, 5 or more) and watch-list size (1, 2, 3 or more), so the share is five
    in eight in any segment a reader can form from the logged sessions."""
    u = int(P.BLOCK[c])
    lam = P.WATCH_LAMBDA[c]
    q = (np.arange(u) + 0.5) / u
    # Poisson quantiles give a block whose size distribution is the Poisson's, shuffled later
    from scipy.stats import poisson
    sizes = rng.permutation(poisson.ppf(q, lam).astype(int))
    total = int(sizes.sum())
    target = max(8, round8(total))
    diff = target - total
    order = rng.permutation(u)
    i = 0
    while diff != 0:
        s = order[i % u]
        if diff > 0:
            sizes[s] += 1
            diff -= 1
        elif sizes[s] > 0:
            sizes[s] -= 1
            diff += 1
        i += 1
    W = int(sizes.sum())
    a = draw_order_attrs(rng, W)
    # exact intent: 5/8 of W, allotted to (renders class, watch-list size class) strata by largest
    # remainder, then at random within each stratum
    cat = a["cat"]
    slot_of = np.repeat(np.arange(u), sizes)
    ncls = np.minimum(rend[slot_of], 5)
    wcls = np.minimum(sizes[slot_of], 3)
    strat = ncls * 10 + wcls
    keys = np.unique(strat)
    counts = np.array([(strat == k).sum() for k in keys])
    n_int = W * P.ANYWAY_NUM // P.ANYWAY_DEN
    # each stratum's rounding residual carries into the next block, so the pooled share per stratum
    # (every cell, every copy) stays on five in eight while each block's total is exact
    carry = {} if carry is None else carry
    tgt = counts * P.ANYWAY_NUM / P.ANYWAY_DEN + np.array([carry.get(int(k), 0.0) for k in keys])
    tgt = np.clip(tgt, 0, counts)
    per = largest_remainder(np.maximum(tgt, 1e-9), n_int)
    per = np.minimum(per, counts)
    while per.sum() < n_int:          # a clipped stratum hands its share to the one furthest under target
        j = int(np.argmax(np.where(per < counts, tgt - per, -1e9)))
        per[j] += 1
    for k, cnt_k, nk in zip(keys, counts, per):
        carry[int(k)] = carry.get(int(k), 0.0) + cnt_k * P.ANYWAY_NUM / P.ANYWAY_DEN - nk
    intent = np.zeros(W, bool)
    for k, nk in zip(keys, per):
        idx = np.flatnonzero(strat == k)
        intent[rng.choice(idx, size=int(nk), replace=False)] = True
    assert intent.sum() == n_int, (intent.sum(), n_int)
    day = rng.choice(np.arange(1, 7), size=W, p=P.ANYWAY_DAY_P)
    late = rng.random(W) < 0.5
    chan = rng.choice(len(LATER_CHANNELS), size=W, p=LATER_P)
    listed_h = np.round(np.exp(rng.normal(np.log(260), 0.8, W)) + 52, 1)
    prof = pd.DataFrame(dict(cat=cat, asking=a["asking"], offer=a["offer"], otype=a["otype"], paid=a["paid"],
                             delivery=a["delivery"], inperson=a["inperson"], intent=intent, aday=day,
                             alate=late, achan=chan, listed_h=listed_h))
    return sizes, prof


def block_background(c, rng):
    """Background orders in the 21 days either side of the session for one block: (day offset,
    before-or-after the session's clock time, order attributes)."""
    u = int(P.BLOCK[c])
    days = np.arange(-P.WINDOW_DAYS, P.WINDOW_DAYS + 1)
    lam = P.BG_RATE[c]
    cnt = rng.poisson(lam * u, size=len(days))
    D = np.repeat(days, cnt)
    k = len(D)
    a = draw_order_attrs(rng, k, offer_share=P.BG_OFFER_SHARE)
    late = rng.random(k) < 0.5
    chan = rng.choice(len(BG_CHANNELS), size=k, p=BG_P)
    same_platform = rng.random(k) < 0.82
    return pd.DataFrame(dict(day=D, late=late, chan=chan, cat=a["cat"], asking=a["asking"], offer=a["offer"],
                             otype=a["otype"], paid=a["paid"], delivery=a["delivery"], inperson=a["inperson"],
                             same_platform=same_platform))


# ------------------------------------------------------------------ the world

class World:
    pass


def mu_total(k, c, n):
    """Expected in-session carousel orders per 1,000 sessions for ranker k in cell c at n renders."""
    nb = P.NBAR[c]
    base = P.KAPPA[c] * (P.ALPHA + (1 - P.ALPHA) * n / nb)
    r = P.RANKERS[k]
    if k == 0:
        return base
    if r == P.STUMP:
        bnew = P.B_BNEW_YOUNG if c % 4 in (0, 1) else P.B_BNEW_OLD
        return base + P.B_ANEW[c] + bnew * (n - nb) + pinned_rate(c, n)
    a, b = P.LIFT[r]
    if (r, c) in P.NO_SLOPE:
        b = 0.0
    return base + a[c] + b * (n - nb)


def _pinned_per_session(c):
    lam = P.WATCH_LAMBDA[c]
    p0 = np.exp(-lam)
    p1 = lam * p0
    return p1 + 2 * (1 - p0 - p1)


def _eg(c):
    H = P.render_dist(P.NBAR[c])
    return sum(H[n - 1] * g for n, g in P.G_OF_N.items())


def pinned_rate(c, n):
    """Velocity boost's pinned watched-listing purchases per 1,000 sessions at n renders (its
    session-weighted mean in cell c is B_R * pinned_per_session * E_c[g])."""
    return P.B_R * _pinned_per_session(c) * P.G_OF_N.get(int(n), 0.0)


def group_size(c, k):
    return int(round(P.N_CELL[c] * P.PI[c, k]))


def expected_watched_buys(c, k):
    """Expected in-session purchases of watched listings in group (c, k)."""
    m = group_size(c, k)
    if P.RANKERS[k] != P.STUMP:
        return 0.0          # the other rankers' candidate pools leave the buyer's watched listings out
    H = np.bincount(block_renders(c), minlength=P.NMAX + 1) * (m / P.BLOCK[c])
    return sum(pinned_rate(c, n) * H[n] / 1000 for n in range(1, P.NMAX + 1))


def choose_octets():
    """Octet counts (eight in-session purchases of watched listings each, five of them listings the
    watcher would have bought within six days) per (cell, ranker). The incumbent takes the nearest
    count; every policy takes the floor or the ceiling in each cell, whichever combination puts its
    pooled borrowed orders nearest its target, with the two cells that breach the guardrail kept at
    or above the incumbent's watched-purchase rate (their kept lift no better than in-session)."""
    import itertools
    s = P.N_CELL / P.N_CELL.sum()
    nb = np.array([block_renders(c).mean() for c in range(8)])
    om = P.N_CELL * nb / (P.N_CELL * nb).sum()
    q = P.ANYWAY_NUM / P.ANYWAY_DEN
    out = {}
    for c in range(8):
        for k in range(7):
            out[(c, k)] = 0
    r0 = np.zeros(8)
    for k in [P.RANKERS.index(P.STUMP)]:
        r = P.RANKERS[k]
        ex = np.array([expected_watched_buys(c, k) / 8 for c in range(8)])
        opts = [sorted({int(np.floor(e)), int(np.ceil(e))}) for e in ex]
        best = None
        for combo in itertools.product(*opts):
            rate = np.array([8 * combo[c] / group_size(c, k) * 1000 for c in range(8)])
            cell_b = q * (rate - r0)
            if r == "HC-31" and cell_b[7] < 0:
                continue
            if r == "HC-34" and cell_b[0] < 0:
                continue
            pooled = float((s * cell_b).sum())
            rpooled = float((om * cell_b).sum())
            if r != P.STUMP and rpooled < 0.02:
                continue
            loss = 50 * (pooled - P.BORROWED_TARGET[r]) ** 2 + (0.0 if r == P.STUMP else 0.001 * float((cell_b ** 2).sum()))
            if best is None or loss < best[0]:
                best = (loss, combo)
        for c in range(8):
            out[(c, k)] = int(best[1][c])
    return out


def build_world():
    W = World()
    rng_cells = {c: P.stream(f"block{c}") for c in range(8)}
    blocks = []
    carry = {}
    for c in range(8):
        rng = rng_cells[c]
        rend = rng.permutation(block_renders(c))
        sizes, wprof = block_watch(c, rng, rend, carry)
        bg = block_background(c, rng)
        # the block's slot profiles are joint: slot s has its renders, its watch list and its background
        # orders together, and every copy repeats them, so any weighting of sessions (by session or by
        # render) sees the same buyers in every arm
        bslot = rng.integers(0, int(P.BLOCK[c]), size=len(bg))
        blocks.append(dict(rend=rend, sizes=sizes, wprof=wprof, bg=bg, bslot=bslot))
    W.blocks = blocks

    # ---- sessions: 100 copies per cell, each copy one ranker
    rows = []
    wrows = []
    brows = []
    sid = 0
    for c in range(8):
        rng = P.stream(f"copies{c}")
        u = int(P.BLOCK[c])
        arms = np.repeat(np.arange(7), np.round(P.PI[c] * 100).astype(int))
        assert len(arms) == 100
        arms = rng.permutation(arms)
        blk = blocks[c]
        nW = len(blk["wprof"])
        nB = len(blk["bg"])
        for j in range(100):
            rend = blk["rend"]
            sizes = blk["sizes"]
            wperm = np.arange(nW)
            starts = np.concatenate([[0], np.cumsum(sizes)[:-1]])
            bslot = blk["bslot"]
            for s in range(u):
                rows.append((sid + s, c, j, s, int(arms[j]), int(rend[s]), int(sizes[s])))
                for t in range(sizes[s]):
                    wrows.append((sid + s, int(wperm[starts[s] + t])))
            for b in range(nB):
                brows.append((sid + int(bslot[b]), b))
            sid += u
    S = pd.DataFrame(rows, columns=["sid", "cell", "copy", "slot", "arm", "n", "w"])
    WL = pd.DataFrame(wrows, columns=["sid", "prof"])
    BG = pd.DataFrame(brows, columns=["sid", "prof"])
    # attach watched-listing profiles
    parts = []
    for c in range(8):
        sub = WL[S.cell.to_numpy()[WL.sid.to_numpy()] == c]
        prof = blocks[c]["wprof"].iloc[sub.prof.to_numpy()].reset_index(drop=True)
        prof.insert(0, "sid", sub.sid.to_numpy())
        parts.append(prof)
    WL = pd.concat(parts, ignore_index=True).sort_values(["sid"], kind="stable").reset_index(drop=True)
    WL["wid"] = np.arange(len(WL))
    WL["cell"] = S.cell.to_numpy()[WL.sid.to_numpy()]
    WL["arm"] = S.arm.to_numpy()[WL.sid.to_numpy()]
    WL["n"] = S.n.to_numpy()[WL.sid.to_numpy()]
    WL["fee"] = fee_cents(WL.paid.to_numpy(), WL.inperson.to_numpy())
    WL["fclass"] = WL.paid.astype(str) + np.where(WL.inperson, "p", "s")
    parts = []
    for c in range(8):
        sub = BG[S.cell.to_numpy()[BG.sid.to_numpy()] == c]
        prof = blocks[c]["bg"].iloc[sub.prof.to_numpy()].reset_index(drop=True)
        prof.insert(0, "sid", sub.sid.to_numpy())
        parts.append(prof)
    BG = pd.concat(parts, ignore_index=True).sort_values(["sid", "day"], kind="stable").reset_index(drop=True)
    W.S, W.WL, W.BG = S, WL, BG

    # ---- outcomes per (cell, ranker)
    WL["shown"] = False
    WL["pinned"] = False
    WL["bought"] = False
    S["nw_orders"] = 0
    S["fresh"] = 0
    W.octets = choose_octets()
    for c in range(8):
        for k in range(7):
            outcomes_group(W, c, k)
    return W


# ------------------------------------------------------------------ per-group outcomes

def select_octets(cand, n_oct, rng, prefer=None):
    """Pick n_oct octets of watched listings to be bought in-session: each octet five listings
    their watchers would have bought within six days and three they would not, all with the same
    slot-tariff fee, from sessions that have no purchase yet. prefer: list of render values to
    draw from first (the velocity boost's pinned purchases happen in short sessions). The five
    listings bought anyway are drawn toward the population's mix of purchase day and time of day, so
    what a shorter follow-up window would catch matches how watched listings sell."""
    chosen = []
    used = set()
    target = {(d, l): P.ANYWAY_DAY_P[d - 1] * 0.5 for d in range(1, 7) for l in (False, True)}
    have = {k: 0 for k in target}
    passes = ([set([n]) for n in prefer] if prefer else []) + [None]
    for ns in passes:
        while len(chosen) < 8 * n_oct:
            pool = cand[~cand.sid.isin(used) & ~cand.wid.isin(chosen)]
            if ns is not None:
                pool = pool[pool.n.isin(ns)]
            if pool.empty:
                break
            # one listing per session within an octet
            pool = pool.drop_duplicates(["sid", "intent"])
            g = pool.groupby(["fclass", "intent"]).sid.nunique().unstack(fill_value=0)
            if True not in g.columns or False not in g.columns:
                break
            ok = g[(g[True] >= 5) & (g[False] >= 3)]
            if ok.empty:
                break
            score = np.minimum(ok[True] // 5, ok[False] // 3).to_numpy()
            fc = ok.index.to_numpy()[np.flatnonzero(score == score.max())]
            pick_fc = fc[rng.integers(len(fc))]
            cls = pool[pool.fclass == pick_fc]
            ints = cls[cls.intent].drop_duplicates("sid")
            ints = ints.iloc[rng.permutation(len(ints))]
            picked = []
            for _ in range(5):
                tot = sum(have.values()) + 1
                deficit = np.array([target[(d, l)] * tot - have[(d, l)] for d, l in zip(ints.aday, ints.alate)])
                deficit[[i for i in range(len(ints)) if ints.index[i] in picked]] = -1e9
                j = int(np.argmax(deficit))
                picked.append(ints.index[j])
                have[(int(ints.aday.iloc[j]), bool(ints.alate.iloc[j]))] += 1
            ints = ints.loc[picked]
            nons = cls[~cls.intent & ~cls.sid.isin(ints.sid)].drop_duplicates("sid")
            if len(nons) < 3:
                break
            nons = nons.iloc[rng.permutation(len(nons))[:3]]
            chosen.extend(ints.wid.tolist() + nons.wid.tolist())
            used.update(ints.sid.tolist() + nons.sid.tolist())
    if len(chosen) < 8 * n_oct:
        raise AssertionError(f"octets: wanted {n_oct}, built {len(chosen) // 8}")
    return chosen


def outcomes_group(W, c, k):
    S, WL = W.S, W.WL
    rng = P.stream(f"group{c}-{k}")
    gm = (S.cell.to_numpy() == c) & (S.arm.to_numpy() == k)
    sids = np.flatnonzero(gm)
    m = len(sids)
    ns = S.n.to_numpy()[sids]
    mn = np.bincount(ns, minlength=P.NMAX + 1)
    wsel = (WL.cell.to_numpy() == c) & (WL.arm.to_numpy() == k)
    cand = WL[wsel][["wid", "sid", "n", "intent", "fclass", "aday", "alate"]]
    r = P.RANKERS[k]
    # --- watched purchases (in-session), a multiple of 8, five in eight would have been bought anyway
    prefer = [1, 2] if r == P.STUMP else None
    n_oct = W.octets[(c, k)]
    bought = select_octets(cand, n_oct, rng, prefer) if n_oct > 0 else []
    WL.loc[bought, "bought"] = True
    WL.loc[bought, "shown"] = True
    # --- shown watched listings (only the velocity boost's build reads saves and shows them)
    if r == P.STUMP:
        pin_velocity(W, c, k, sids, rng)
    # --- non-watched in-session orders per renders value
    wb = np.bincount(WL.loc[bought, "n"].to_numpy(), minlength=P.NMAX + 1) if bought else np.zeros(P.NMAX + 1, int)
    carry = 0.0
    # long sessions first, so the rounding residual settles where a render weight amplifies it least
    for n in range(P.NMAX, 0, -1):
        if mn[n] == 0:
            continue
        tgt = mu_total(k, c, n) * mn[n] / 1000 - wb[n] + carry
        cnt = max(0, int(np.floor(tgt + 0.5)))
        carry = tgt - cnt
        if cnt == 0:
            continue
        pool = sids[ns == n]
        # a session takes at most two non-watched orders; about one ordering session in sixteen takes two
        two = min(cnt // 2, int(round(cnt * 0.06)))
        one = cnt - 2 * two
        pick = rng.choice(pool, size=one + two, replace=False)
        S.loc[pick[:two], "nw_orders"] = 2
        S.loc[pick[two:], "nw_orders"] = 1
    # --- fresh tiles per session
    fresh_tiles(W, c, k, sids, ns, rng)


def pin_velocity(W, c, k, sids, rng):
    """The velocity boost pins up to two of the buyer's watched listings to tiles 1 and 2 (the
    purchased one always among them). The shown total is then trimmed to a multiple of 8 with five
    in eight of the shown listings ones their watchers buy anyway, by leaving the second pin off in a
    few sessions or swapping which watched listing is pinned."""
    WL = W.WL
    sub = WL[WL.sid.isin(sids)]
    pinned = []
    # forced pins first (a buyer watching one or two listings gets them all), then the choices in
    # sessions with three or more, each made to keep its renders class's shown share on five in eight
    cls_of = lambda n: min(int(n), 5)
    tally = defaultdict(lambda: [0, 0])          # renders class -> [intent shown, shown]
    choice = []
    for sid, g in sub.groupby("sid"):
        b = g[g.bought]
        rest = g[~g.bought]
        take = list(b.wid)
        k2 = min(2, len(g)) - len(take)
        cl = cls_of(g.n.iloc[0])
        if len(g) <= 2:
            take += list(rest.wid)
        elif k2 > 0:
            choice.append((sid, cl, rest, k2))
        for w in take:
            tally[cl][0] += int(WL.intent.iat[w])
            tally[cl][1] += 1
        pinned += take
    for i in rng.permutation(len(choice)):
        sid, cl, rest, k2 = choice[i]
        ints = list(rest[rest.intent].wid)
        nons = list(rest[~rest.intent].wid)
        best = None
        for ni in range(0, min(k2, len(ints)) + 1):
            nn = k2 - ni
            if nn > len(nons):
                continue
            ti, ts = tally[cl][0] + ni, tally[cl][1] + k2
            score = abs(ti - ts * P.ANYWAY_NUM / P.ANYWAY_DEN)
            if best is None or score < best[0]:
                best = (score, ni, nn)
        _, ni, nn = best
        take = ints[:ni] + nons[:nn]
        tally[cl][0] += ni
        tally[cl][1] += k2
        pinned += take
    pinned = np.array(sorted(pinned))
    flag = np.zeros(len(WL), bool)
    flag[pinned] = True
    intent = WL.intent.to_numpy()
    bought = WL.bought.to_numpy()
    S_ = int(flag[pinned].sum())
    I_ = int(intent[pinned].sum())
    # candidates for dropping: pinned, not bought, in sessions with two pins (keep the first pin)
    sidv = WL.sid.to_numpy()

    def droppable(want_intent):
        out = []
        cnt = defaultdict(int)
        for w in np.flatnonzero(flag & np.isin(sidv, sids)):
            cnt[sidv[w]] += 1
        for w in np.flatnonzero(flag & ~bought & np.isin(sidv, sids) & (intent == want_intent)):
            if cnt[sidv[w]] >= 2:
                out.append(w)
        return out

    d = S_ % 8
    for _ in range(200):
        S_ = int(flag.sum() if False else flag[np.isin(sidv, sids)].sum())
        I_ = int((flag & intent & np.isin(sidv, sids)).sum())
        d = S_ % 8
        need_I = (S_ - d) * P.ANYWAY_NUM // P.ANYWAY_DEN
        x = I_ - need_I               # intents to drop among the d drops
        if d == 0 and x == 0:
            break
        if 0 <= x <= d:
            di = droppable(True)
            dn = droppable(False)
            if len(di) >= x and len(dn) >= d - x:
                for w in list(rng.permutation(di)[:x]) + list(rng.permutation(dn)[:d - x]):
                    flag[w] = False
                continue
        # swap: in a session with an unpinned watched listing of the other kind, swap one pin
        want_more_intent = x < 0
        done = False
        for sid in rng.permutation(sids):
            ws = np.flatnonzero(sidv == sid)
            if len(ws) < 3:
                continue
            pin_ws = [w for w in ws if flag[w] and not bought[w] and intent[w] != want_more_intent]
            free_ws = [w for w in ws if not flag[w] and intent[w] == want_more_intent]
            if pin_ws and free_ws:
                flag[pin_ws[0]] = False
                flag[free_ws[0]] = True
                done = True
                break
        if not done:
            # drop a whole octet's worth instead: remove 8 more pins later by widening d
            raise AssertionError(f"pin balancing failed in cell {c}")
    sel = np.isin(sidv, sids)
    WL.loc[sel, "pinned"] = flag[sel]
    WL.loc[sel, "shown"] = flag[sel] | WL.loc[sel, "bought"].to_numpy()
    shown = WL[sel & WL.shown.to_numpy()]
    assert len(shown) % 8 == 0 and shown.intent.sum() * P.ANYWAY_DEN == len(shown) * P.ANYWAY_NUM


def fresh_tiles(W, c, k, sids, ns, rng):
    """Fresh tiles (listings under 48 hours old) per session: a fixed share of the six tiles for
    every ranker but the local pickup boost, whose fresh local listings surface in long sessions."""
    S = W.S
    r = P.RANKERS[k]
    for n in np.unique(ns):
        pool = sids[ns == n]
        mcount = len(pool)
        if r == "HC-36":
            share = P.D_FRESH_BY_N[min(int(n), 5)]
        else:
            share = P.FRESH_SHARE[r]
        total = int(np.floor(6 * share * mcount + 0.5))
        cap = 3 if r == "HC-37" else 4
        base = np.zeros(mcount, int)
        # spread: draw a random allotment with the exact total, at most cap per session
        left = total
        order = rng.permutation(mcount)
        i = 0
        while left > 0:
            s = order[i % mcount]
            if base[s] < cap and (rng.random() < 0.55 or i >= mcount):
                base[s] += 1
                left -= 1
            i += 1
        S.loc[pool, "fresh"] = base


# ------------------------------------------------------------------ placing the graded figures

def pooled(W, arm, kept=True):
    """Session-weighted lift (per 1,000 sessions) of ranker arm against the incumbent, in-session or
    kept, from the in-memory outcomes. Used only to place figures; the asserted figures are
    recomputed from the written files."""
    S, WL = W.S, W.WL
    b = WL[WL.bought]
    wb = np.bincount(b.sid, minlength=len(S))
    wbi = np.bincount(b[b.intent].sid, minlength=len(S))
    y = S.nw_orders.to_numpy() + wb - (wbi if kept else 0)
    cell = S.cell.to_numpy()
    arms = S.arm.to_numpy()
    N = len(S)

    def level(k):
        g = arms == k
        return (y[g] / P.PI[cell[g], k]).sum() / N * 1000
    return level(arm) - level(0)


def tune_main(W):
    """Add or remove new-listing in-session orders so the call's figures sit inside their bins:
    the answer's kept lift at 5.698 and the runner-up's at 3.302 (a gap of 2.396). One order in cell
    c moves a pooled lift by 1000 / (N * pi[c]); the change is the smallest integer combination over
    the distinct step sizes that lands within 0.002 of the target. Orders go to or come from
    single-render or two-render sessions, where a render weight moves least."""
    import itertools
    S = W.S
    W.tuned = {}
    for k, tgt in ((E_IDX, 5.698), (B_IDX, 3.302)):
        rng = P.stream(f"tune{k}")
        steps = {}
        for c in range(8):
            steps.setdefault(round(1000.0 / (len(S) * P.PI[c, k]), 9), []).append(c)
        keys = sorted(steps)
        gap = tgt - pooled(W, k)
        best = None
        rngs = [range(-14, 15)] * len(keys)
        for xs in itertools.product(*rngs):
            res = gap - sum(x * st for x, st in zip(xs, keys))
            cost = (round(abs(res), 3), sum(abs(x) for x in xs))
            if best is None or cost < best[0]:
                best = (cost, xs)
        assert best[0][0] < 0.006, ("no combination within 0.006", k, gap, best)
        for x, st in zip(best[1], keys):
            cells = steps[st]
            for i in range(abs(x)):
                c = cells[i % len(cells)]
                g = np.flatnonzero((S.cell.to_numpy() == c) & (S.arm.to_numpy() == k) & (S.n.to_numpy() <= 2))
                have = S.nw_orders.to_numpy()[g]
                if x > 0:
                    s = rng.choice(g[have == 0])
                    S.loc[s, "nw_orders"] = 1
                else:
                    s = rng.choice(g[have == 1])
                    S.loc[s, "nw_orders"] = 0
        W.tuned[P.RANKERS[k]] = pooled(W, k)
