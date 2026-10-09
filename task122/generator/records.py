"""task122 generator: turn the world's outcomes into the records the platform's systems hold.

Identities, dates and clock times, the ranking served in each logged session (six tiles, the age
of each listing, the buyer's watch list at the start), the render log, and every order, accepted
offer and payment for the enrolled buyers from 1 June to 11 October 2026.
"""
from collections import defaultdict
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

import params as P
import world as Wm

REGIONS = ["NH", "ZH", "UT", "NB", "GE", "OV", "LI", "GR", "FR", "DR", "FL", "ZE"]
REGION_P = [0.17, 0.21, 0.08, 0.15, 0.12, 0.07, 0.06, 0.03, 0.04, 0.03, 0.03, 0.01]
WEEKDAY_W = np.array([1.00, 0.92, 0.95, 1.00, 0.90, 1.06, 1.24])   # Monday .. Sunday
EPOCH = datetime(2025, 1, 1)


def _days(d0, d1):
    out = []
    d = d0
    while d <= d1:
        out.append(d)
        d += timedelta(days=1)
    return out


def assign_identities(W):
    S = W.S
    rng = P.stream("ids")
    N = len(S)
    bid = rng.choice(np.arange(11_000_000, 69_000_000), size=N, replace=False)
    S["buyer_id"] = bid
    hexs = rng.integers(0, 16 ** 10, size=N, dtype=np.int64)
    sids = np.array([f"hc{h:010x}" for h in hexs])
    assert len(set(sids)) == N
    S["session_id"] = sids
    lo = np.array([P.BAND_DAYS[c % 4][0] for c in S.cell])
    hi = np.array([P.BAND_DAYS[c % 4][1] for c in S.cell])
    u = rng.random(N)
    span = hi - lo
    # tenure within band: more mass at the young end of each band
    S["tenure"] = (lo + np.floor(span * u ** 1.35)).astype(int)
    S["platform"] = np.where(S.cell < 4, "app", "web")
    S["region"] = rng.choice(REGIONS, size=N, p=REGION_P)
    S["pool_id"] = np.array([f"cp{v:07d}" for v in rng.integers(1_000_000, 9_999_999, size=N)])


def _split_group(x1, x2, key, m0, t1, t2, rng):
    """Two halves of one (cell, ranker) group, m0 sessions in half 0, with the half-0 sum minus the
    half-1 sum of x1 and of x2 equal to t1 and t2: sort, alternate, then swap pairs of sessions across
    the halves until both hold."""
    m = len(x1)
    order = np.lexsort((key, x1, x2))
    flip = 0 if m0 == (m + 1) // 2 else 1
    if m % 2 == 0:
        flip = int(rng.integers(2))
    h = np.empty(m, int)
    h[order] = (np.arange(m) + flip) % 2
    assert (h == 0).sum() == m0
    for _ in range(400):
        d1 = int(x1[h == 0].sum() - x1[h == 1].sum())
        d2 = int(x2[h == 0].sum() - x2[h == 1].sum())
        cost = abs(d1 - t1) + abs(d2 - t2)
        if cost == 0:
            return h
        types = [defaultdict(list), defaultdict(list)]
        for i in range(m):
            types[h[i]][(int(x1[i]), int(x2[i]))].append(i)
        best = None
        for a, I in types[0].items():
            for b, J in types[1].items():
                n1 = d1 - 2 * (a[0] - b[0])
                n2 = d2 - 2 * (a[1] - b[1])
                c = abs(n1 - t1) + abs(n2 - t2)
                if c < cost and (best is None or c < best[0]):
                    best = (c, I, J)
        if best is None:
            break
        i = best[1][int(rng.integers(len(best[1])))]
        j = best[2][int(rng.integers(len(best[2])))]
        h[i], h[j] = 1, 0
    raise AssertionError("halves: no exact split")


def _parity_near(x, parity):
    """The two integers of the given parity nearest x."""
    lo = int(np.floor(x))
    if lo % 2 != parity:
        lo -= 1
    return [lo, lo + 2] if abs(x - lo) > 1e-12 else [lo]


def _half_options(m, T1, T2):
    """Per group: (sessions in half 0, d1, d2) choices that keep both half means level to within one
    order, d = half-0 sum minus half-1 sum."""
    out = []
    for dm in ((0,) if m % 2 == 0 else (1, -1)):
        for d1 in _parity_near(T1 * dm / m, T1 % 2):
            for d2 in _parity_near(T2 * dm / m, T2 % 2):
                out.append(((m + dm) // 2, d1, d2))
    return out


def _half_gap(pi, groups, choice):
    """First-half minus second-half level (per 1,000 sessions, self-normalised session weights) of
    one ranker on both readings, for one choice of option per cell."""
    num = np.zeros((2, 2))
    den = np.zeros(2)
    for c, (m, T1, T2, opts) in groups.items():
        m0, d1, d2 = opts[choice[c]]
        w = 1.0 / pi[c]
        den += w * np.array([m0, m - m0])
        num[0] += w * np.array([(T1 + d1) / 2, (T1 - d1) / 2])
        num[1] += w * np.array([(T2 + d2) / 2, (T2 - d2) / 2])
    lv = num / den
    return (lv[:, 0] - lv[:, 1]) * 1000


def _choose_half_options(pi, groups, ref, rng):
    """Local search over the per-cell options for the choice that brings this ranker's gap on both
    readings nearest the incumbent's (ref), from several starts."""
    cells = sorted(groups)
    best = None
    for start in range(12):
        ch = {c: (0 if start == 0 else int(rng.integers(len(groups[c][3])))) for c in cells}
        cur = np.abs(_half_gap(pi, groups, ch) - ref).max()
        improved = True
        while improved:
            improved = False
            for c in cells:
                for o in range(len(groups[c][3])):
                    if o == ch[c]:
                        continue
                    trial = dict(ch)
                    trial[c] = o
                    v = np.abs(_half_gap(pi, groups, trial) - ref).max()
                    if v < cur - 1e-12:
                        ch, cur, improved = trial, v, True
        if best is None or cur < best[0]:
            best = (cur, ch)
    return best[1], _half_gap(pi, groups, best[1])


def assign_dates(W):
    """Halves first: inside each (cell, ranker) the two halves of the window hold the same mean
    in-session orders and the same mean orders within 21 days per session (to one order, the odd
    ones placed so the halves' levels match the incumbent's across cells), so each half of the window
    carries the same outcomes on either reading; then a day inside the half (weekday weighted), a
    start time, render gaps and an end time."""
    S, WL, BG = W.S, W.WL, W.BG
    rng = P.stream("dates")
    b = WL[WL.bought]
    wb = np.bincount(b.sid, minlength=len(S))
    wbi = np.bincount(b[b.intent].sid, minlength=len(S))
    n_int = np.bincount(WL[WL.intent].sid, minlength=len(S))
    day, late = BG.day.to_numpy(), BG.late.to_numpy()
    inwin = ((day >= 1) & (day <= P.WINDOW_DAYS - 1)) | ((day == 0) & late) | ((day == P.WINDOW_DAYS) & ~late)
    bg_in = np.bincount(BG.sid.to_numpy()[inwin], minlength=len(S))
    y_in = S.nw_orders.to_numpy() + wb
    y_kept = y_in - wbi + n_int + bg_in
    W.mem_y_in, W.mem_y_kept = y_in, y_kept
    cell, arm = S.cell.to_numpy(), S.arm.to_numpy()
    plan = {}
    ref = np.zeros(2)
    W.half_gaps = {}
    for k in range(7):
        groups = {}
        for c in range(8):
            g = (cell == c) & (arm == k)
            m, T1, T2 = int(g.sum()), int(y_in[g].sum()), int(y_kept[g].sum())
            groups[c] = (m, T1, T2, _half_options(m, T1, T2))
        ch, gap = _choose_half_options(P.PI[:, k], groups, ref, rng)
        if k == 0:
            ref = gap
        W.half_gaps[P.RANKERS[k]] = gap - (ref if k else 0)
        for c in range(8):
            plan[(c, k)] = groups[c][3][ch[c]]
    half = np.zeros(len(S), int)
    key = S.n.to_numpy() * 16 + np.minimum(S.w.to_numpy(), 15)
    for c in range(8):
        for k in range(7):
            idx = np.flatnonzero((cell == c) & (arm == k))
            m0, d1, d2 = plan[(c, k)]
            half[idx] = _split_group(y_in[idx], y_kept[idx], key[idx], m0, d1, d2, rng)
    S["half"] = half
    first = _days(P.LOG_START, P.HALF_SPLIT - timedelta(days=1))
    second = _days(P.HALF_SPLIT, P.LOG_END)
    out = np.empty(len(S), dtype=object)
    for h, days in ((0, first), (1, second)):
        w = WEEKDAY_W[[d.weekday() for d in days]]
        idx = np.flatnonzero(half == h)
        pick = rng.choice(len(days), size=len(idx), p=w / w.sum())
        out[idx] = [days[i] for i in pick]
    S["date"] = out
    N = len(S)
    mix = rng.random(N)
    t = np.where(mix < 0.30, rng.normal(12.6, 1.4, N), np.where(mix < 0.80, rng.normal(20.4, 1.3, N),
                                                                    rng.uniform(7.0, 22.5, N)))
    start = np.clip(t * 3600, 6 * 3600, 22.75 * 3600).astype(int)
    S["start_s"] = start
    # render offsets: first at 0, then gaps of 12-75 seconds
    nmax = S.n.max()
    gaps = rng.integers(12, 76, size=(N, nmax))
    gaps[:, 0] = 0
    offs = np.cumsum(gaps, axis=1)
    W.render_offsets = offs
    last = offs[np.arange(N), S.n.to_numpy() - 1]
    S["end_s"] = start + last + rng.integers(20, 241, size=N)


def _age_fresh(rng, k):
    return np.round(rng.uniform(0.6, 45.4, k), 1)


def _age_old(rng, k):
    return np.round(50.5 + np.exp(rng.normal(np.log(210), 0.95, k)), 1)


def assign_tiles(W):
    """Six tiles per served ranking: pinned watched listings at tiles 1 and 2 for the velocity boost,
    fresh listings (E prefers tiles 3 and 6), and the ordered positions."""
    S, WL = W.S, W.WL
    rng = P.stream("tiles")
    N = len(S)
    role = np.zeros((N, 6), dtype=np.int64)      # -1 new listing, >=0 watched-listing wid
    role[:] = -1
    fresh = np.zeros((N, 6), bool)
    ordered = np.zeros((N, 6), bool)
    shown = WL[WL.shown].sort_values(["sid", "bought"], ascending=[True, False], kind="stable")
    arms = S.arm.to_numpy()
    for sid, g in shown.groupby("sid"):
        wids = g.wid.to_numpy()
        if arms[sid] == Wm.B_IDX:
            for i, w in enumerate(wids[:2]):
                role[sid, i] = w
        else:
            pos = int(rng.integers(6))
            role[sid, pos] = wids[0]
    # fresh tiles on new-listing tiles
    f = S.fresh.to_numpy()
    pref_e = [2, 5, 4, 1, 3, 0]
    for sid in np.flatnonzero(f > 0):
        free = [p for p in range(6) if role[sid, p] < 0]
        if arms[sid] == Wm.E_IDX:
            order = [p for p in pref_e if p in free]
        else:
            order = list(rng.permutation(free))
        for p in order[: f[sid]]:
            fresh[sid, p] = True
        assert fresh[sid].sum() == f[sid], (sid, f[sid], free)
    # ordered positions
    bought = WL[WL.bought]
    for sid, w in zip(bought.sid.to_numpy(), bought.wid.to_numpy()):
        p = np.flatnonzero(role[sid] == w)
        assert len(p) == 1
        ordered[sid, p[0]] = True
    nw = S.nw_orders.to_numpy()
    for sid in np.flatnonzero(nw > 0):
        free = [p for p in range(6) if role[sid, p] < 0 and not ordered[sid, p]]
        pick = rng.choice(free, size=nw[sid], replace=False)
        ordered[sid, pick] = True
    W.role, W.fresh, W.ordered = role, fresh, ordered
    # ages at serve time
    age = np.where(fresh, 0.0, 0.0)
    nf = int(fresh.sum())
    age[fresh] = _age_fresh(rng, nf)
    newmask = (role < 0) & ~fresh
    age[newmask] = _age_old(rng, int(newmask.sum()))
    wmask = role >= 0
    age[wmask] = WL.listed_h.to_numpy()[role[wmask]]
    W.age = age


def assign_listing_ids(W, extra_created):
    """Listing ids are allocated in creation order. Every listing in the pack (tiles, watch lists,
    orders) gets an id from its creation time; extra_created are creation times of order-only
    listings, returned ids in the same order."""
    S, WL = W.S, W.WL
    rng = P.stream("listing-ids")
    serve = np.array([(datetime(d.year, d.month, d.day) - EPOCH).total_seconds() for d in S.date]) + S.start_s.to_numpy()
    # tile listings that are not watched
    newmask = W.role < 0
    t_new = (serve[:, None] - W.age * 3600)[newmask]
    t_w = serve[WL.sid.to_numpy()] - WL.listed_h.to_numpy() * 3600
    t_all = np.concatenate([t_new, t_w, np.asarray(extra_created, float)])
    order = np.argsort(t_all, kind="stable")
    base = 4_310_000_000 + (t_all[order] * 0.21).astype(np.int64)
    ids = np.empty(len(t_all), np.int64)
    gaps = rng.integers(1, 9, size=len(t_all))
    run = np.maximum.accumulate(base + np.cumsum(gaps))
    ids[order] = run
    assert len(np.unique(ids)) == len(ids)
    n1 = int(newmask.sum())
    tile_ids = np.zeros(W.role.shape, np.int64)
    tile_ids[newmask] = ids[:n1]
    WL["listing_id"] = ids[n1:n1 + len(WL)]
    wmask = ~newmask
    tile_ids[wmask] = WL.listing_id.to_numpy()[W.role[wmask]]
    W.tile_ids = tile_ids
    return ids[n1 + len(WL):]


# ------------------------------------------------------------------ orders

ORDER_COLS = ["kind", "sid", "t", "channel", "session_id", "platform", "cat", "asking", "offer", "otype", "paid",
              "delivery", "inperson", "wallet", "wid", "pos", "bgrow"]


def _frame(kind, sid, t, channel, session_id, platform, a, wid=None, pos=None, wallet=None, bgrow=None):
    k = len(sid)
    return pd.DataFrame(dict(kind=kind, sid=np.asarray(sid, np.int64), t=np.asarray(t, np.int64),
                             channel=np.asarray(channel, object), session_id=np.asarray(session_id, object),
                             platform=np.asarray(platform, object), cat=np.asarray(a["cat"], int),
                             asking=np.asarray(a["asking"], int), offer=np.asarray(a["offer"], int),
                             otype=np.asarray(a["otype"], object), paid=np.asarray(a["paid"], int),
                             delivery=np.asarray(a["delivery"], object), inperson=np.asarray(a["inperson"], bool),
                             wallet=np.zeros(k, bool) if wallet is None else np.asarray(wallet, bool),
                             wid=np.full(k, -1, np.int64) if wid is None else np.asarray(wid, np.int64),
                             pos=np.full(k, -1, np.int64) if pos is None else np.asarray(pos, np.int64),
                             bgrow=np.full(k, -1, np.int64) if bgrow is None else np.asarray(bgrow, np.int64)))[ORDER_COLS]


def _wallet_exact(rng, delivery):
    """Balance-paid flags for one group's in-session orders: exactly the share's nearest count of the
    shipped orders, at random among them."""
    ship = np.flatnonzero(np.asarray(delivery) == "shipped")
    k = int(np.floor(P.WALLET_SHARE * len(ship) + 0.5))
    out = np.zeros(len(delivery), bool)
    if k:
        out[rng.choice(ship, size=k, replace=False)] = True
    return out


def build_orders(W):
    S, WL, BG = W.S, W.WL, W.BG
    rng = P.stream("orders")
    N = len(S)
    day0 = np.array([(datetime(d.year, d.month, d.day) - EPOCH).total_seconds() for d in S.date], np.int64)
    start = day0 + S.start_s.to_numpy()
    end = day0 + S.end_s.to_numpy()
    plat = S.platform.to_numpy()
    sess = S.session_id.to_numpy()
    arms = S.arm.to_numpy()
    frames = []
    # --- in-session orders, one per ordered tile
    sid, pos = np.nonzero(W.ordered)
    n = S.n.to_numpy()[sid]
    j = (rng.random(len(sid)) * n).astype(int)
    t = start[sid] + W.render_offsets[sid, j] + rng.integers(5, 40, size=len(sid))
    t = np.minimum(t, end[sid] - 3)
    w = W.role[sid, pos]
    iw = w >= 0
    a = {key: WL[key].to_numpy()[w[iw]] for key in ("cat", "asking", "offer", "otype", "paid", "delivery", "inperson")}
    frames.append(_frame("insession_watched", sid[iw], t[iw], np.full(iw.sum(), "carousel"), sess[sid[iw]],
                         plat[sid[iw]], a, wid=w[iw], pos=pos[iw], wallet=WL.wallet.to_numpy()[w[iw]]))
    nsid, npos, nt = sid[~iw], pos[~iw], t[~iw]
    for k in range(7):
        sel = arms[nsid] == k
        if not sel.any():
            continue
        for c in range(8):
            sc = sel & (S.cell.to_numpy()[nsid] == c)
            if not sc.any():
                continue
            a = Wm.stratified_attrs(P.stream(f"insession-attrs{k}-{c}"), int(sc.sum()), P.RANKERS[k])
            wal = _wallet_exact(P.stream(f"insession-wallet{k}-{c}"), a["delivery"])
            frames.append(_frame("insession_new", nsid[sc], nt[sc], np.full(sc.sum(), "carousel"),
                                 sess[nsid[sc]], plat[nsid[sc]], a, pos=npos[sc], wallet=wal))
    # --- watched listings their watcher buys later (not bought in the session)
    later = WL[WL.intent & ~WL.bought]
    sd = later.sid.to_numpy()
    u = rng.random(len(later))
    et, st = S.end_s.to_numpy()[sd], S.start_s.to_numpy()[sd]
    clock = np.where(later.alate.to_numpy(), et + 60 + u * (86_399 - 60 - et), u * (st - 60)).astype(np.int64)
    t = day0[sd] + later.aday.to_numpy() * 86400 + clock
    a = {key: later[key].to_numpy() for key in ("cat", "asking", "offer", "otype", "paid", "delivery", "inperson")}
    # a listing shown on the buyer's carousel stays off it in later sessions for seven days, so a shown
    # watched listing bought later comes through the watch list, never a carousel tile
    chan = Wm.LATER_CHANNELS[later.achan.to_numpy()].astype(object)
    chan[later.shown.to_numpy() & (chan == "carousel")] = "favourites"
    frames.append(_frame("anyway", sd, t, chan, np.full(len(sd), None), plat[sd],
                         a, wid=later.wid.to_numpy(), wallet=later.wallet.to_numpy()))
    # --- background orders in the 21 days either side (identical in every block copy)
    sd = BG.sid.to_numpy()
    u = rng.random(len(BG))
    et, st = S.end_s.to_numpy()[sd], S.start_s.to_numpy()[sd]
    clock = np.where(BG.late.to_numpy(), et + 60 + u * (86_399 - 60 - et), u * (st - 60)).astype(np.int64)
    t = day0[sd] + BG.day.to_numpy() * 86400 + clock
    oth = np.where(plat[sd] == "app", "web", "app")
    bplat = np.where(BG.same_platform.to_numpy(), plat[sd], oth)
    a = {key: BG[key].to_numpy() for key in ("cat", "asking", "offer", "otype", "paid", "delivery", "inperson")}
    frames.append(_frame("bg_window", sd, t, Wm.BG_CHANNELS[BG.chan.to_numpy()], np.full(len(sd), None), bplat, a,
                         wallet=BG.wallet.to_numpy(), bgrow=np.arange(len(BG))))
    # --- other orders across the extract, away from the 43-day window around the session
    t0 = int((datetime(P.ORDERS_FROM.year, P.ORDERS_FROM.month, P.ORDERS_FROM.day) - EPOCH).total_seconds())
    t1 = int((datetime(P.EXTRACT.year, P.EXTRACT.month, P.EXTRACT.day) - EPOCH).total_seconds()) + 86399
    lo_a = np.full(N, t0)
    hi_a = day0 - P.WINDOW_DAYS * 86400            # before the start of day -21
    lo_b = day0 + (P.WINDOW_DAYS + 1) * 86400      # from the start of day +22
    hi_b = np.full(N, t1)
    wa = np.maximum(0, hi_a - lo_a)
    wb = np.maximum(0, hi_b - lo_b)
    rate = P.BG_RATE[S.cell.to_numpy()]
    k = rng.poisson(rate * (wa + wb) / 86400)
    sd = np.repeat(np.arange(N), k)
    x = rng.random(len(sd)) * (wa[sd] + wb[sd])
    t = np.where(x < wa[sd], lo_a[sd] + x, lo_b[sd] + (x - wa[sd])).astype(np.int64)
    a = Wm.draw_order_attrs(rng, len(sd), offer_share=P.BG_OFFER_SHARE)
    chan = Wm.BG_CHANNELS[rng.choice(len(Wm.BG_CHANNELS), size=len(sd), p=Wm.BG_P)]
    oth = np.where(plat[sd] == "app", "web", "app")
    pl = np.where(rng.random(len(sd)) < 0.82, plat[sd], oth)
    wal = (a["delivery"] == "shipped") & (P.stream("wallet-outside").random(len(sd)) < P.WALLET_SHARE)
    frames.append(_frame("bg_outside", sd, t, chan, np.full(len(sd), None), pl, a, wallet=wal))
    O = pd.concat(frames, ignore_index=True)
    comeback(W, O, end)
    # carousel orders outside the logged session come from other, unlogged home sessions
    m = ((O.channel == "carousel") & O.session_id.isna()).to_numpy()
    hx = rng.integers(0, 16 ** 10, size=int(m.sum()), dtype=np.int64)
    other = np.array([f"hc{h:010x}" for h in hx], dtype=object)
    assert not (set(other) & set(sess))
    O.loc[m, "session_id"] = other
    O["listing_id"] = np.int64(-1)
    W.O = O
    return O


def comeback(W, O, end):
    """Come-back tile orders. In every (cell, ranker) group a fixed
    count of the group's sessions (COMEBACK_PER_1000 per 1,000 sessions, nearest whole order) have one of
    their background orders from the session's own evening, or failing that the next morning, become an
    order the buyer placed from a tile still on screen after the session closed: channel carousel, the
    listing on a tile the buyer did not order from in the session and was not watching, 2 minutes to 4
    hours after the session ended, placed in the new (unlogged) home session the buyer's return opened.
    The order keeps every attribute it had (price, offer, delivery, payment), so no order enters or leaves
    any window and no lift, half or fee figure moves; only its channel, its listing and its clock change.
    The session-sequence model's buyers mostly come back to the item through favourites or search
    (COMEBACK_SCALE), so its groups get a fraction of the count."""
    S, BG = W.S, W.BG
    bg = (O.kind == "bg_window").to_numpy()
    rows = np.flatnonzero(bg)
    br = O.bgrow.to_numpy()[rows]
    day, late = BG.day.to_numpy()[br], BG.late.to_numpy()[br]
    pref = np.where((day == 0) & late, 0, np.where((day == 1) & ~late, 1, 9))
    cand = pd.DataFrame(dict(row=rows, sid=O.sid.to_numpy()[rows], pref=pref))
    cand = cand[cand.pref < 9].sort_values(["sid", "pref", "row"], kind="stable").drop_duplicates("sid")
    cell, arm = S.cell.to_numpy(), S.arm.to_numpy()
    cand["cell"], cand["arm"] = cell[cand.sid.to_numpy()], arm[cand.sid.to_numpy()]
    W.comeback_counts = {}
    ci = {k: O.columns.get_loc(k) for k in ("kind", "channel", "platform", "pos", "t")}
    for c in range(8):
        for k in range(7):
            m = int(((cell == c) & (arm == k)).sum())
            n = int(np.floor(P.COMEBACK_PER_1000[c] * P.COMEBACK_SCALE.get(P.RANKERS[k], 1.0) * m / 1000 + 0.5))
            rng = P.stream(f"comeback{c}-{k}")
            g = cand[(cand.cell == c) & (cand.arm == k)]
            first = g[g.pref == 0]
            pool = first if len(first) >= n else g
            if len(pool) < n:
                raise AssertionError(f"come-back: group {c},{k} has {len(pool)} candidate sessions for {n}")
            pick = pool.iloc[np.sort(rng.choice(len(pool), size=n, replace=False))]
            for r_, s in zip(pick.row.to_numpy(), pick.sid.to_numpy()):
                free = [p for p in range(6) if not W.ordered[s, p] and W.role[s, p] < 0]
                O.iat[r_, ci["kind"]] = "comeback"
                O.iat[r_, ci["channel"]] = "carousel"
                O.iat[r_, ci["platform"]] = S.platform.iat[s]
                O.iat[r_, ci["pos"]] = int(free[int(rng.integers(len(free)))])
                O.iat[r_, ci["t"]] = int(end[s] + rng.integers(120, P.COMEBACK_MAX_S + 1))
            W.comeback_counts[(c, k)] = n


def checkout3(W):
    """Checkout 3 (21 September 2026): every order is paid when it is placed, pickups included. A pickup
    placed from that day that the order template had collected and paid to the seller is paid at checkout
    instead, so it reaches the provider's capture file and carries the fee. Only orders after the logger window
    are touched (every in-session and come-back order is earlier), the order keeps every other attribute, and no
    order enters or leaves any window, so no lift, half or count moves."""
    O = W.O
    t3 = int((datetime(P.CHECKOUT3.year, P.CHECKOUT3.month, P.CHECKOUT3.day) - EPOCH).total_seconds())
    late = (O.t.to_numpy() >= t3) & O.inperson.to_numpy().astype(bool)
    assert not np.isin(O.kind.to_numpy()[late], ["insession_new", "insession_watched", "comeback"]).any()
    O.loc[late, "inperson"] = False
    W.checkout3_moved = int(late.sum())


def finish_orders(W, new_ids):
    """Order-only listings get ids; watched listings and tiles carry theirs; orders get ids in time
    order."""
    O = W.O
    WL = W.WL
    ins = O.kind.isin(["insession_new", "comeback"]).to_numpy()
    O.loc[ins, "listing_id"] = W.tile_ids[O.sid.to_numpy()[ins], O.pos.to_numpy()[ins]]
    wl = (O.wid >= 0).to_numpy()
    O.loc[wl, "listing_id"] = WL.listing_id.to_numpy()[O.wid.to_numpy()[wl]]
    need = (O.listing_id < 0).to_numpy()
    O.loc[need, "listing_id"] = new_ids
    assert (O.listing_id > 0).all()
    O.sort_values(["t", "sid", "listing_id"], kind="stable", inplace=True)
    O.reset_index(drop=True, inplace=True)
    rng = P.stream("order-ids")
    O["order_id"] = 30_418_000_000 + np.cumsum(rng.integers(3, 40, size=len(O)))
    O["category"] = np.array(P.CATEGORIES, dtype=object)[O.cat.to_numpy()]
    W.O = O


def order_only_creation_times(W):
    """Creation times for the listings bought outside the watch lists and tiles (before the order)."""
    O = W.O
    rng = P.stream("order-listing-age")
    need = ((O.listing_id < 0) & (O.wid < 0) & ~O.kind.isin(["insession_new", "comeback"])).to_numpy()
    t = O.loc[need, "t"].to_numpy().astype(float)
    age = 3600 * (2 + np.exp(rng.normal(np.log(180), 1.0, len(t))))
    return t - age


def build_offers_payments(W):
    O = W.O
    rng = P.stream("offers")
    rows = []
    has = O.otype.isin(["used", "lapsed"]).to_numpy()
    sub = O[has]
    tt = sub.t.to_numpy()
    lapsed = (sub.otype == "lapsed").to_numpy()
    # accepted offers are valid for 48 hours; a lapsed one expired before the checkout
    acc = np.where(lapsed, tt - rng.integers(49 * 3600, 140 * 3600, len(sub)),
                   tt - rng.integers(4 * 60, 46 * 3600, len(sub)))
    offered = acc - rng.integers(60, 20 * 3600, len(sub))
    expires = acc + 48 * 3600
    assert (expires[lapsed] < tt[lapsed]).all() and (expires[~lapsed] > tt[~lapsed]).all()
    F = pd.DataFrame(dict(listing_id=sub.listing_id.to_numpy(), buyer_sid=sub.sid.to_numpy(),
                          offered=offered, accepted=acc, expires=expires, offer_eur=sub.offer.to_numpy(),
                          order_row=np.flatnonzero(has)))
    F.sort_values(["offered", "listing_id"], kind="stable", inplace=True)
    F["offer_id"] = 7_200_000 + np.cumsum(rng.integers(1, 6, size=len(F)))
    W.F = F
    # payments: every order paid through checkout and captured by the payment provider; an order collected
    # and paid in person carries no payment, and one paid from a Vouwlijn balance is settled inside the
    # platform, so neither reaches the provider's capture file
    prot_mask = ~O.inperson.to_numpy().astype(bool)
    psp_mask = prot_mask & ~O.wallet.to_numpy().astype(bool)
    PM = O[psp_mask][["order_id", "t", "paid", "delivery", "category"]].copy()
    PM["captured"] = PM.t + rng.integers(3, 51, size=len(PM))
    cap_dates = [(EPOCH + timedelta(seconds=int(x))).date() for x in PM.captured]
    fixed = np.array([70 if d < P.TARIFF_CHANGE else 80 for d in cap_dates])
    PM["fee_cents"] = fixed + 5 * PM.paid.to_numpy().astype(int)
    PM["ship_cents"] = np.where(PM.delivery == "shipped",
                                [int(round(P.SHIPPING[c] * 100)) for c in PM.category], 0)
    PM["amount_cents"] = PM.paid.to_numpy().astype(int) * 100 + PM.fee_cents + PM.ship_cents
    rngp = P.stream("payment-ids")
    PM["payment_id"] = [f"pay_{v:012x}" for v in rngp.integers(16 ** 11, 16 ** 12, size=len(PM), dtype=np.int64)]
    assert PM.payment_id.is_unique
    W.PM = PM
    # every protected purchase as Finance books it: provider captures at their capture time, balance
    # purchases at the order time; the fee at the tariff in force then, VAT included
    WB = O[prot_mask & O.wallet.to_numpy().astype(bool)][["order_id", "t", "paid", "platform"]].copy()
    WB["booked"] = WB.t
    wdates = [(EPOCH + timedelta(seconds=int(x))).date() for x in WB.booked]
    WB["fee_cents"] = np.array([70 if d < P.TARIFF_CHANGE else 80 for d in wdates]) + 5 * WB.paid.to_numpy().astype(int)
    pm = PM[["order_id", "captured", "paid", "fee_cents"]].rename(columns={"captured": "booked"})
    pm["platform"] = pm.order_id.map(O.set_index("order_id").platform)
    W.PROT = pd.concat([pm, WB[["order_id", "booked", "paid", "fee_cents", "platform"]]], ignore_index=True)


def build_records(W):
    assign_identities(W)
    Wm.tune_main(W)
    assign_dates(W)
    assign_tiles(W)
    # a watched listing is never collected and paid to the seller at the handover (a buyer who saves a listing
    # pays for it through checkout, pickup or not), so a brought-forward purchase and the purchase it replaces sit
    # on the same cover under either checkout
    W.WL["inperson"] = False
    build_orders(W)
    checkout3(W)
    extra = order_only_creation_times(W)
    new_ids = assign_listing_ids(W, extra)
    finish_orders(W, new_ids)
    import place
    place.place_fee_cells(W)
    place.fix_vat_rounding(W)
    build_offers_payments(W)
    return W
