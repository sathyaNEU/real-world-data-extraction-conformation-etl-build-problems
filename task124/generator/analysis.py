"""Every rung of the main call, computed from the inventory and the verification log in the form they ship.

The inputs are plain frames with the shipped columns already parsed (sl_id resolved through the crosswalk, result
codes normalised to LEAD, GRR, NON-LEAD); records.py produces them from the files and verify.py has its own
parser. Nothing here reads the ground truth."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

import common as K


def era_series(years: pd.Series) -> pd.Series:
    return years.map(K.era_of)


def sample(inv: pd.DataFrame, ver: pd.DataFrame) -> pd.DataFrame:
    """Verified lines that had no usable tap card record and were built before 1989: one row per line, its first
    result, its segment's coverage. inv columns: sl_id, zone, segment, year_built, record, cls. ver columns: sl_id,
    date, result."""
    first = ver.sort_values(["date", "sl_id"]).groupby("sl_id", as_index=False).first()
    lines_per_seg = inv.groupby("segment").sl_id.size()
    verified_per_seg = inv[inv.sl_id.isin(first.sl_id)].groupby("segment").sl_id.size()
    cov = (verified_per_seg / lines_per_seg).fillna(0.0)
    s = first.merge(inv[["sl_id", "zone", "segment", "year_built", "record"]], on="sl_id", how="inner")
    s = s[(s.record.fillna("") == "") & (s.year_built > 0) & (s.year_built < K.AGE_RULE_YEAR)].copy()
    s["era"] = era_series(s.year_built)
    s["hit"] = s.result.isin(["LEAD", "GRR"])
    s["coverage"] = s.segment.map(cov).fillna(0.0)
    return s



def street_class(inv: pd.DataFrame) -> pd.Series:
    """main segment -> LG when any tap card on it reads LEAD or GALV, else C (cards only COPPER or PLASTIC)."""
    carded = inv[inv.record != ""]
    lg = carded.groupby("segment").record.apply(lambda s: bool(s.isin(["LEAD", "GALV"]).any()))
    return lg.map({True: "LG", False: "C"})


def lg_card_share(inv: pd.DataFrame) -> pd.Series:
    """main segment -> the share of its tap cards that read LEAD or GALV."""
    carded = inv[inv.record != ""]
    return carded.groupby("segment").record.apply(lambda s: float(s.isin(["LEAD", "GALV"]).mean()))


def class_shares(s: pd.DataFrame, cls: pd.Series, mask=None) -> dict:
    """Share of the verified no-tap-card lines found lead or GRR, by the class of the main they tap."""
    t = s if mask is None else s[mask]
    t = t.assign(sc=t.segment.map(cls))
    return {k: float(t[t.sc == k].hit.mean()) for k in ("LG", "C")}


def unknown_by_class(inv: pd.DataFrame, cls: pd.Series) -> dict:
    """{era: {class: Lead Status Unknown lines}} over the whole district."""
    u = inv[inv.cls == "LEAD STATUS UNKNOWN"]
    e = u.year_built.map(K.era_of)
    c = u.segment.map(cls)
    return {k: {x: int(((e == k) & (c == x)).sum()) for x in ("LG", "C")} for k in range(3)}


def class_era_shares(inv: pd.DataFrame, s: pd.DataFrame, cls: pd.Series, mask=None) -> dict:
    """The share of lead or GRR expected among the district's Lead Status Unknown lines of each era: each unknown line
    carries the share found on the verified no-tap-card lines of mains of its class, averaged over the era's unknown
    lines."""
    sh = class_shares(s, cls, mask)
    ub = unknown_by_class(inv, cls)
    return {e: sum(ub[e][x] * sh[x] for x in ("LG", "C")) / sum(ub[e].values()) for e in range(3)}


def unknown_shares(inv: pd.DataFrame, ver: pd.DataFrame, p) -> dict:
    """The share of lead or GRR expected among the district's Lead Status Unknown lines of each era: every line of the
    era with no usable tap card is expected to prove lead or GRR at the whole-segment share p, the verifications have
    already found some of them, and the unknown lines carry the rest. Returns {era: (share, lines with no tap card,
    verified, found lead or GRR, unknown)}."""
    first = ver.sort_values(["date", "sl_id"]).groupby("sl_id").result.first()
    nr = inv[(inv.record == "") & (inv.year_built > 0) & (inv.year_built < K.AGE_RULE_YEAR)]
    era = nr.year_built.map(K.era_of)
    out = {}
    for e in range(3):
        t = nr[era == e]
        res = t.sl_id.map(first)
        n, d = len(t), int(res.notna().sum())
        h = int(res.isin(["LEAD", "GRR"]).sum())
        out[e] = ((n * p[e] - h) / (n - d), n, d, h, n - d)
    return out

def coverage(inv: pd.DataFrame, ver: pd.DataFrame) -> pd.Series:
    seen = set(ver.sl_id)
    g = inv.assign(v=inv.sl_id.isin(seen)).groupby("segment").v
    return g.mean()


def shares(s: pd.DataFrame, mask=None, by="era") -> dict:
    t = s if mask is None else s[mask]
    if by == "era":
        return {e: float(t[t.era == e].hit.mean()) for e in range(3)}
    raise ValueError(by)


def remaining(inv: pd.DataFrame) -> pd.DataFrame:
    """Per plan zone: lines classified lead or GRR, and unknown lines by era."""
    rows = []
    for z in K.PLAN_ORDER:
        t = inv[inv.zone == z]
        lgrr = int(t.cls.isin(["LEAD", "GRR"]).sum())
        unk = t[t.cls == "LEAD STATUS UNKNOWN"]
        ue = era_series(unk.year_built)
        rows.append((z, lgrr, int((ue == 0).sum()), int((ue == 1).sum()), int((ue == 2).sum()),
                     int((ue < 0).sum() + (ue == 3).sum())))
    return pd.DataFrame(rows, columns=["zone", "lgrr", "u0", "u1", "u2", "u_other"])


def zone_costs(rem: pd.DataFrame, p, appropriation=K.APPROPRIATION, prices=None, mobilisation=K.MOBILISATION
               ) -> pd.DataFrame:
    """Expected replacements, non-lead digs, cost, running total and finish year, zones in plan order."""
    prices = prices or K.ZONE_PRICES
    p = [p[0], p[1], p[2]] if isinstance(p, dict) else list(p)
    out = []
    cum = 0.0
    for r in rem.itertuples():
        exp_unk = r.u0 * p[0] + r.u1 * p[1] + r.u2 * p[2]
        unk = r.u0 + r.u1 + r.u2
        repl = r.lgrr + exp_unk
        digs = unk - exp_unk
        uf, ud = prices[r.zone]
        cost = repl * uf + digs * ud + mobilisation
        cum += cost
        years = cum / appropriation
        finish = K.FIRST_YEAR + math.ceil(years - 1e-9) - 1
        out.append((r.zone, r.lgrr, unk, exp_unk, repl, digs, cost, cum, years, finish))
    return pd.DataFrame(out, columns=["zone", "lgrr", "unknown", "exp_unknown", "replacements", "digs", "cost",
                                      "cum_cost", "years", "finish_year"])


def schedule_summary(z: pd.DataFrame) -> dict:
    last = int(z.finish_year.max())
    return {"last_year": last, "meets": last <= K.LAST_YEAR, "total": float(z.cum_cost.iloc[-1]),
            "finish": dict(zip(z.zone, z.finish_year.astype(int)))}
