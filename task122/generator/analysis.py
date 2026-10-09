"""task122 generator: every construction a solver can run on the main call, computed from the
files as written (read back from disk). checks.py asserts on these; the independent verifier
recomputes them on its own code path.
"""
import os

import numpy as np
import pandas as pd

import params as P
import writers as Wr

BAND_EDGES = [30, 180, 730]


def band_index(days):
    d = np.asarray(days)
    return np.searchsorted(BAND_EDGES, d, side="right")


class Main:
    pass


def load_main(tgt):
    M = Main()
    R = pd.read_csv(os.path.join(tgt, Wr.F_RENDER), dtype={"ordered_tiles": str, "session_id": str},
                    keep_default_na=False)
    R["y_row"] = R.ordered_tiles.map(lambda s: len(s.split()) if s else 0)
    M.R = R
    g = R.groupby("session_id", sort=True)
    S = g.agg(platform=("platform", "first"), tenure=("buyer_tenure_days", "first"), ranker=("ranker", "first"),
              p=("propensity", "first"), n=("render_seq", "size"), y=("y_row", "first")).reset_index()
    S["band"] = band_index(S.tenure)
    S["cell"] = np.where(S.platform == "app", 0, 4) + S.band
    SR = pd.read_parquet(os.path.join(tgt, Wr.F_RANKINGS))
    S = S.merge(SR, on="session_id", how="left", validate="one_to_one")
    M.S = S
    O = pd.read_parquet(os.path.join(tgt, Wr.F_ORDERS))
    M.O = O
    return M


def tile_orders(M, timed=False, hours=None):
    """Orders placed from the tiles each logged session served: carousel orders by the session's buyer
    whose listing was on one of the session's six tiles, placed after the session started (the charter's
    carousel order rate; a listing shown on a buyer's carousel stays off it in later sessions for seven
    days, so the listing names the tile). timed=True keeps only those placed before the session ended,
    which is what the render log's ordered_tiles counts; hours keeps those placed no later than that many
    hours after the session ended."""
    S, O = M.S, M.O
    tiles = S.melt(id_vars=["session_id", "buyer_id", "started_at", "ended_at"],
                   value_vars=[f"tile_{i}" for i in range(1, 7)], value_name="listing_id")
    c = O[O.channel == "carousel"][["buyer_id", "listing_id", "ordered_at"]].merge(
        tiles[["session_id", "buyer_id", "listing_id", "started_at", "ended_at"]], on=["buyer_id", "listing_id"],
        how="inner")
    c = c[c.ordered_at >= c.started_at]
    if timed:
        c = c[c.ordered_at <= c.ended_at]
    elif hours is not None:
        c = c[(c.ordered_at - c.ended_at).dt.total_seconds() <= hours * 3600]
    n = c.groupby("session_id").size()
    return S.session_id.map(n).fillna(0).astype(int).to_numpy()


def session_orders(M):
    """Carousel orders the orders extract credits to each logged session (the session they were placed in)."""
    S, O = M.S, M.O
    n = O[O.channel == "carousel"].groupby("home_session_id").size()
    return S.session_id.map(n).fillna(0).astype(int).to_numpy()


def in_session_from_orders(M):
    """In-session carousel orders per logged session, from the orders extract (placed in the session)."""
    return session_orders(M)


def carousel_window(M, days):
    """Carousel orders (any home session) each logged session's buyer placed from the session start to
    `days` days after it: the reading that counts tiles the arm never served."""
    S, O = M.S, M.O
    m = O[O.channel == "carousel"][["buyer_id", "ordered_at"]].merge(S[["buyer_id", "started_at"]], on="buyer_id")
    dt = (m.ordered_at - m.started_at).dt.total_seconds()
    cnt = m[(dt >= 0) & (dt <= days * 86400)].groupby("buyer_id").size()
    return S.buyer_id.map(cnt).fillna(0).astype(int).to_numpy()


def followup(M, hours=None, calendar_days=None):
    """Orders (every channel) each logged session's buyer placed from the session start to the
    window's end, by 24-hour periods or by calendar days after the session date."""
    S, O = M.S, M.O
    m = O[["buyer_id", "ordered_at"]].merge(S[["buyer_id", "started_at"]], on="buyer_id", how="inner")
    dt = (m.ordered_at - m.started_at).dt.total_seconds()
    if hours is not None:
        ok = (dt >= 0) & (dt <= hours * 3600)
    else:
        dd = (m.ordered_at.dt.normalize() - m.started_at.dt.normalize()).dt.days
        ok = (dt >= 0) & (dd <= calendar_days)
    cnt = m[ok].groupby("buyer_id").size()
    return S.buyer_id.map(cnt).fillna(0).astype(int).to_numpy()


def watch_frame(M):
    S = M.S
    rows = []
    for sid, s in zip(S.session_id.to_numpy(), S.watchlist_at_start.to_numpy()):
        if s:
            for x in s.split():
                rows.append((sid, int(x)))
    W = pd.DataFrame(rows, columns=["session_id", "listing_id"])
    tiles = S.melt(id_vars=["session_id"], value_vars=[f"tile_{i}" for i in range(1, 7)], value_name="listing_id")
    W["shown"] = W.set_index(["session_id", "listing_id"]).index.isin(
        tiles.set_index(["session_id", "listing_id"]).index)
    return W


def route2(M, q_window_hours=21 * 24):
    """In-session orders netted for the watched listings bought in the session, at the rate watched
    listings the session did not show are bought by their watcher within the window."""
    S, O = M.S, M.O
    W = watch_frame(M)
    buyer = S.set_index("session_id").buyer_id
    start = S.set_index("session_id").started_at
    W["buyer_id"] = W.session_id.map(buyer).to_numpy()
    W["start"] = W.session_id.map(start).to_numpy()
    ob = O[["buyer_id", "listing_id", "ordered_at", "channel", "home_session_id"]]
    m = W.merge(ob, on=["buyer_id", "listing_id"], how="left")
    dt = (m.ordered_at - m.start).dt.total_seconds()
    insess = (m.home_session_id == m.session_id) & (m.channel == "carousel")
    m["bought_in_session"] = insess.fillna(False)
    m["bought_later"] = (~m.bought_in_session) & (dt > 0) & (dt <= q_window_hours * 3600)
    un = m[~m.shown]
    q = float(un.bought_later.mean())
    wis = m[m.bought_in_session].groupby("session_id").size()
    S_w = S.session_id.map(wis).fillna(0).to_numpy()
    return q, S_w, m


def est(S, y, kind, arm_col="ranker"):
    """Value per 1,000 sessions of each ranker under one estimator; returns dict ranker->level."""
    out = {}
    N = len(S)
    p = S.p.to_numpy()
    n = S.n.to_numpy()
    for r in P.RANKERS:
        g = (S[arm_col] == r).to_numpy()
        if kind == "replay_rows":
            out[r] = (y[g] * n[g]).sum() / n[g].sum()
        elif kind == "replay_sessions":
            out[r] = y[g].mean()
        elif kind == "render_weights":
            out[r] = (y[g] * n[g] / p[g]).sum() / (n[g] / p[g]).sum()
        elif kind == "session_ipw":
            out[r] = (y[g] / p[g]).sum() / N
        elif kind == "session_snipw":
            out[r] = (y[g] / p[g]).sum() / (1 / p[g]).sum()
        elif kind == "session_clipped":
            w = 1 / np.maximum(p[g], 0.05)
            out[r] = (y[g] * w).sum() / N
        elif kind == "cell_stratified":
            tot = 0.0
            for c in range(8):
                cm = (S.cell == c).to_numpy()
                tot += cm.sum() / N * y[g & cm].mean()
            out[r] = tot
        else:
            raise ValueError(kind)
    return {r: (out[r] - out["HC-24"]) * 1000 for r in P.POLICIES}


SESSION_GRAIN = ("session_ipw", "session_snipw", "session_clipped", "cell_stratified")
FAMILY = ("replay_rows", "render_weights") + SESSION_GRAIN + ("replay_sessions",)


def per_cell(S, y, weighted_by_renders=False):
    """Per-cell value per 1,000 sessions for every ranker (propensity is constant within a cell, so
    any IPS reading reduces to a mean within the cell)."""
    out = {}
    n = S.n.to_numpy()
    for c in range(8):
        cm = (S.cell == c).to_numpy()
        for r in P.RANKERS:
            g = cm & (S.ranker == r).to_numpy()
            out[(r, c)] = ((y[g] * n[g]).sum() / n[g].sum() if weighted_by_renders else y[g].mean()) * 1000
    return out


def guardrail(S, y_count, weighted_by_renders=False, coarse=None):
    """Per cent change in each cell against the incumbent's carousel order rate there, both counted on
    y_count (per session). coarse: None for the eight cells, or 'platform' / 'tenure' / 'pooled'."""
    base = per_cell(S, y_count, weighted_by_renders)
    val = base
    Nc = np.array([(S.cell == c).sum() for c in range(8)], float)
    if coarse is None:
        groups = {c: [c] for c in range(8)}
    elif coarse == "platform":
        groups = {"app": [0, 1, 2, 3], "web": [4, 5, 6, 7]}
    elif coarse == "tenure":
        groups = {b: [b, b + 4] for b in range(4)}
    else:
        groups = {"all": list(range(8))}
    res = {}
    for r in P.POLICIES:
        for key, cs in groups.items():
            w = Nc[cs] / Nc[cs].sum()
            lift = sum(w[i] * (val[(r, c)] - val[("HC-24", c)]) for i, c in enumerate(cs))
            b = sum(w[i] * base[("HC-24", c)] for i, c in enumerate(cs))
            res[(r, key)] = 100 * lift / b
    return res


def fresh_counts(S):
    ages = S[[f"tile_{i}_age_h" for i in range(1, 7)]].to_numpy()
    return (ages < 48).sum(axis=1)


def floors(S):
    f = fresh_counts(S)
    n = S.n.to_numpy()
    p = S.p.to_numpy()
    out = {}
    for r in P.RANKERS:
        g = (S.ranker == r).to_numpy()
        out[(r, "per_ranking")] = 100 * f[g].sum() / (6 * g.sum())
        out[(r, "per_ranking_ipw")] = 100 * (f[g] / p[g]).sum() / (6 * (1 / p[g]).sum())
        out[(r, "rendered_tiles")] = 100 * (f[g] * n[g]).sum() / (6 * n[g].sum())
        out[(r, "rendered_tiles_ipw")] = 100 * (f[g] * n[g] / p[g]).sum() / (6 * (n[g] / p[g]).sum())
    return out


def leader(values, eligible):
    elig = [r for r in P.POLICIES if eligible[r]]
    ranked = sorted(elig, key=lambda r: -values[r])
    if not ranked:
        return None, None, None
    first = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    margin = values[first] / values[second] if second and values[second] > 0 else float("inf")
    return first, second, margin


def conditions(S, y_guard, values, est_kind, guard_read, floor_grain):
    """Which policies clear the three launch conditions under one reading; y_guard is the per-session
    carousel order count the guardrail is read on."""
    rw = est_kind in ("replay_rows", "render_weights")
    if guard_read == "eight":
        g = guardrail(S, y_guard, weighted_by_renders=rw)
        guard_ok = {r: all(g[(r, c)] >= -1.5 for c in range(8)) for r in P.POLICIES}
    else:
        g = guardrail(S, y_guard, weighted_by_renders=rw, coarse="platform")
        guard_ok = {r: all(g[(r, k)] >= -1.5 for k in ("app", "web")) for r in P.POLICIES}
    fl = floors(S)
    key = {"rendered": "rendered_tiles" if est_kind == "replay_rows" else "rendered_tiles_ipw",
           "ranking": "per_ranking"}[floor_grain]
    floor_ok = {r: fl[(r, key)] >= 12.0 for r in P.POLICIES}
    bar_ok = {r: values[r] >= 2.0 for r in P.POLICIES}
    return {r: guard_ok[r] and floor_ok[r] and bar_ok[r] for r in P.POLICIES}, guard_ok, floor_ok, bar_ok
