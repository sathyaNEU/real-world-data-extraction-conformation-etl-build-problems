"""task271 analysis on the shipped pack: the golden call and its estimator family, the ladder's wrong rungs, and the
two asks. Every graded figure is computed here from target/ and nowhere else."""
from __future__ import annotations

import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd

import common as K
import records as R

THG = {"THGD": "THGD", "THGM": "THGD"}
POINT_SECS = [9 * 3600 + 30 * 60, 12 * 3600, 14 * 3600 + 30 * 60]
CUTOFF = 15 * 60


def load(target):
    p = lambda f: os.path.join(target, f)
    H = pd.read_csv(p(R.F_HESS), dtype={"broker_exec_id": str, "isin": str})
    A = pd.read_csv(p(R.F_ASHL), dtype=str)
    xl = pd.read_excel(p(R.F_PEMB), sheet_name=None, dtype=str)
    B = pd.concat(xl.values(), ignore_index=True)
    O = pd.read_csv(p(R.F_OMS), dtype={"quantity": float})
    M = pd.read_csv(p(R.F_MASTER))
    CA = json.load(open(p(R.F_CA)))
    CAL = pd.read_csv(p(R.F_CAL))
    W = pd.read_csv(p(R.F_ORDERS), dtype={"shares": "Int64"})
    N = pd.read_csv(p(R.F_NOTES), dtype={"note_ref": str})
    return dict(H=H, A=A, B=B, O=O, M=M, CA=CA, CAL=CAL, W=W, N=N)


# ------------------------------------------------------------------------------------------------- the call
def fills(P, drop_busts=True, dedupe=True):
    """Continuous-trading executions with a 60-second mid, one row per execution, busts out; each with its adverse
    moves and the desk's other executions in the same line around it."""
    H = P["H"].copy()
    if dedupe:
        H = H.drop_duplicates("broker_exec_id", keep="first")
    busted = set(P["A"].loc[P["A"]["exec_type"] == "BUST", "ref_exec_id"]) | \
        set(P["B"].loc[P["B"]["Status"] == "Busted", "Orig Exec Ref"])
    H["busted"] = H["broker_exec_id"].isin(busted)
    H["t"] = pd.to_datetime(H["exec_time_utc"], utc=True)
    H["ts"] = (H["t"] - pd.Timestamp("2026-01-01", tz="UTC")).dt.total_seconds()
    H["venue"] = H["last_mkt"].map(lambda v: THG.get(v, v))
    sgn = np.where(H["side"] == "BUY", 1.0, -1.0)
    for h, col in ((60, "mid_plus_60s"), (1, "mid_plus_1s"), (5, "mid_plus_5s"), (30, "mid_plus_30s")):
        H["adv%d" % h] = -sgn * (H[col] - H["mid_at_exec"]) / H["mid_at_exec"] * 1e4
    # the desk's executions in the same line in the 60 seconds after, and before, each execution (busts included:
    # a busted execution was still a trade when it printed)
    H = H.sort_values(["isin", "ts", "broker_exec_id"]).reset_index(drop=True)
    after_n = np.zeros(len(H), dtype=int)
    after_q = np.zeros(len(H))
    before_n = np.zeros(len(H), dtype=int)
    for isin, idx in H.groupby("isin").indices.items():
        ts = H["ts"].values[idx]
        q = H["shares"].values[idx].astype(float)
        hi = np.searchsorted(ts, ts + 60.0, side="right")
        lo = np.searchsorted(ts, ts - 60.0, side="left")
        cq = np.concatenate([[0.0], np.cumsum(q)])
        pos = np.arange(len(idx))
        after_n[idx] = hi - pos - 1
        after_q[idx] = cq[hi] - cq[pos + 1]
        before_n[idx] = pos - lo
    H["after_n"], H["after_q"], H["before_n"] = after_n, after_q, before_n
    adv = dict(zip(P["M"]["isin"], P["M"]["adv_shares_2026"]))
    for ev in P["CA"]["events"]:
        if ev["event_type"] == "CONSOLIDATION":
            adv[ev["isin"]] = adv[ev["new_isin"]] * 10
    H["after_pct"] = H["after_q"] / H["isin"].map(adv) * 100.0
    keep = (H["session"] == "CONT") & H["mid_plus_60s"].notna()
    if drop_busts:
        keep &= ~H["busted"]
    return H[keep].copy()


def by_venue(F, col="adv60", how="mean"):
    g = F.groupby("venue")[col]
    v = g.mean() if how == "mean" else g.median()
    n = g.size()
    return {k: (float(v.get(k, np.nan)), int(n.get(k, 0))) for k in K.VENUES}


def golden(P, F=None):
    """Each venue's adverse move for the platform's orders: its fills that no desk execution in the same line followed
    within 60 seconds, the lone-order evidence the platform's whole, single-execution orders resemble."""
    F = fills(P) if F is None else F
    return by_venue(F[F["after_n"] == 0])


def excluded(est):
    return tuple(v for v in K.VENUES if est[v][1] > 0 and est[v][0] > K.LINE)


def whole_bp(x):
    return int(math.floor(x + 0.5))


def family(P, F=None):
    """The constructions that keep the desk's following trades out of each fill's move."""
    F = fills(P) if F is None else F
    out = {}
    out["after_none"] = by_venue(F[F["after_n"] == 0])
    out["lone"] = by_venue(F[(F["after_n"] == 0) & (F["before_n"] == 0)])
    X = np.column_stack([np.array([(F["venue"] == v).values for v in K.VENUES]).T.astype(float),
                         F["after_pct"].values])
    b = np.linalg.lstsq(X, F["adv60"].values, rcond=None)[0]
    out["regression"] = {v: (float(b[i]), int((F["venue"] == v).sum())) for i, v in enumerate(K.VENUES)}
    out["_slope"] = float(b[-1])
    # fills outside each order's opening ninety seconds (the release time from the OMS)
    rel = dict(zip(P["O"]["order_id"], pd.to_datetime(P["O"]["released_utc"], utc=True)))
    H = P["H"].drop_duplicates("broker_exec_id")
    rel_s = F["client_order_id"].map(rel)
    late = (F["t"] - rel_s).dt.total_seconds() > 90
    out["after_opening"] = by_venue(F[late & (F["after_n"] == 0) | late & (F["after_n"] >= 0) & (F["after_n"] == 0)])
    out["outside_opening"] = by_venue(F[late])
    return out


def rungs(P, F=None):
    F = fills(P) if F is None else F
    out = {}
    out["R0_every_fill"] = by_venue(F)
    out["R0b_median"] = by_venue(F, how="median")
    out["R1_one_second"] = by_venue(F, col="adv1")
    out["R1b_five_seconds"] = by_venue(F, col="adv5")
    strat = dict(zip(P["O"]["order_id"], P["O"]["strategy"]))
    dma = F["client_order_id"].map(strat) == "DMA"
    single = by_venue(F[dma])
    every = out["R0_every_fill"]
    out["R2_single_orders"] = {v: single[v] if single[v][1] > 0 else every[v] for v in K.VENUES}
    pm = F.groupby("client_order_id")["adv60"].transform("mean")
    pn = F.groupby("client_order_id")["adv60"].transform("size")
    G = F[pn > 1].copy()
    G["fe"] = G["adv60"] - pm[pn > 1] + F["adv60"].mean()
    out["R3_parent_effects"] = by_venue(G, col="fe")
    return out


# ------------------------------------------------------------------------------------------------- Ask A
def london_point(ts_utc, closed):
    """The dealing day and point an order placed at a UTC instant joins, per the dealing plan."""
    loc = ts_utc.tz_convert("Europe/London")
    d = loc.date()
    sec = loc.hour * 3600 + loc.minute * 60 + loc.second
    if d not in closed:
        for i, ps in enumerate(POINT_SECS):
            if sec < ps - CUTOFF:
                return d, i
    d = d + dt.timedelta(days=1)
    while d in closed:
        d += dt.timedelta(days=1)
    return d, 0


def effective_notes(P):
    """Gresmere's notes as dealt: cancelled notes out, reissues in, and the new system's second issue of a trade the
    old system had already noted (same order, trade date, time and shares, settling after the migration) out."""
    N = P["N"].copy()
    N = N[N["note_status"] != "CANCELLED"].copy()
    N["trade_day"] = pd.to_datetime(N["trade_date"], format="%d/%m/%Y").dt.date
    N["new_sys"] = N["note_ref"].str.startswith("CN26-")
    key = ["client_order_ref", "trade_date", "trade_time", "shares", "side"]
    dup = N.duplicated(key, keep=False)
    drop = dup & N["new_sys"] & (N["trade_day"] < K.GRESMERE_MIGRATION)
    return N[~drop].copy()


def ask_a(P):
    """The 2027 plan's market orders from the client orders Gresmere dealt in 2026 by trade date (any note dated 1 January
    to 30 October): each order at the point its placing time gives under the plan's cut-offs, whole (every part it was
    dealt in), in the line's current shares."""
    closed = set(pd.to_datetime(P["CAL"].loc[P["CAL"]["uk_market"] == "CLOSED", "date"]).dt.date)
    N = effective_notes(P)
    dealt_sh = N.groupby("client_order_ref")["shares"].sum()
    in_2026 = set(N.loc[(N["trade_day"] >= dt.date(2026, 1, 1)) & (N["trade_day"] <= K.DATA_END), "client_order_ref"])
    W = P["W"][P["W"]["client_order_ref"].isin(in_2026)].copy()
    W["q"] = W["client_order_ref"].map(dealt_sh).astype(float)
    ts = pd.to_datetime(W["placed_at"]).dt.tz_localize("UTC")      # the platform stores UTC without a marker
    pts = [london_point(t, closed) for t in ts]
    W["pday"] = [x[0] for x in pts]
    W["point"] = [x[1] for x in pts]
    W["signed"] = np.where(W["side"] == "BUY", W["q"], -W["q"])
    G = W.groupby(["pday", "point", "isin"])["signed"].sum().reset_index()
    G = G[G["signed"] != 0].copy()
    adv = dict(zip(P["M"]["isin"], P["M"]["adv_shares_2026"]))
    conv = {}
    for ev in P["CA"]["events"]:
        if ev["event_type"] == "CONSOLIDATION":
            conv[ev["isin"]] = (ev["new_isin"], 10)
    def pct(row):
        isin, q = row["isin"], abs(row["signed"])
        if isin in conv:
            ni, r = conv[isin]
            return q / r / adv[ni] * 100.0
        return q / adv[isin] * 100.0
    G["pct"] = G.apply(pct, axis=1)
    # the consolidating line: the order book carries the new line's code on every order and the shares as dealt,
    # old shares before the consolidation date
    for ev in P["CA"]["events"]:
        if ev["event_type"] == "CONSOLIDATION":
            eff = dt.date.fromisoformat(ev["ex_date"])
            m = (G["isin"] == ev["new_isin"]) & (G["pday"] < eff)
            G.loc[m, "pct"] = G.loc[m, "pct"] / 10.0
    counts = {pi: int((G["point"] == pi).sum()) for pi in range(3)}
    sizes = {pi: float(G.loc[G["point"] == pi, "pct"].mean()) for pi in range(3)}
    return dict(counts=counts, sizes=sizes, n=len(G), G=G)


# ------------------------------------------------------------------------------------------------- Ask B
def ask_b(P):
    N = effective_notes(P)
    N = N[(N["trade_day"] >= dt.date(2026, 1, 1)) & (N["trade_day"] <= K.DATA_END)]
    N["m"] = N["trade_day"].map(lambda d: d.month)
    N["gross"] = (N["shares"] * N["price_gbx"] / 100.0).round(2)
    g = N.groupby(["m", "side"])["gross"].sum()
    return {m: (float(g.get((m, "BUY"), 0.0)) - float(g.get((m, "SELL"), 0.0))) / 1e6 for m in range(1, 11)}
