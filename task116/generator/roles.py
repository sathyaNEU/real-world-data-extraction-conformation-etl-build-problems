"""Which real trusts play which part, and how much of each Tallybridge already holds.

Central trusts bought for their academies at a purchase date (and some for their primaries only), so the
academies that joined later are uncovered. Devolved trusts have a few heads who bought for their own school.
"""
import datetime as dt

import numpy as np
import pandas as pd

from world import (RATE, SIGN_RATE_DEN, SIGN_RATE_NUM, annual_value, band_of, rng, term_for, AS_AT,
                   PILOT_PRICED)


def profiles(reg):
    e = reg.est
    sell = reg.open_state()
    sell_urns = set(sell["URN"])
    tc = e[e["Trusts (code)"].isin(reg.mat_uids)].copy()
    tc["uid"] = tc["Trusts (code)"].astype(int)
    status = tc["EstablishmentStatus (name)"]
    pend = tc[status.isin(["Open, but proposed to close", "Proposed to open"])].groupby("uid").size()
    op = tc[status == "Open"].copy()
    op["pup_ok"] = op["NumberOfPupils"].notna() & (op["NumberOfPupils"] > 0)
    op["cen_ok"] = op["CensusDate"].eq("15-01-2026")
    op["sell"] = op["URN"].isin(sell_urns)
    op["has_pred"] = op["URN"].map(lambda u: u in reg.pred_of)
    g = op.groupby("uid").agg(n_open=("URN", "size"), P_all=("NumberOfPupils", "sum"),
                              pup_ok=("pup_ok", "all"), cen_ok=("cen_ok", "all"), n_sell=("sell", "sum"),
                              n_pred=("has_pred", "sum"),
                              region=("GOR (name)", lambda s: s.mode().iloc[0]),
                              n_prim=("PhaseOfEducation (name)", lambda s: (s == "Primary").sum()))
    g["pending"] = g.index.map(lambda u: u in pend.index)
    g["stable"] = ~g.index.isin(reg.moved_since_june)
    g["clean"] = g["pup_ok"] & g["cen_ok"] & ~g["pending"] & (g["n_sell"] == g["n_open"])
    g["name"] = g.index.map(reg.group_name)
    # trusts whose names differ only by a leading THE, or an end word, are left out of every role
    norm = g["name"].fillna("").str.upper().str.replace(r"^THE ", "", regex=True).str.replace(
        r"[^A-Z ]", "", regex=True).str.split().str[:3].str.join(" ")
    dup = norm.duplicated(keep=False)
    g["clean"] = g["clean"] & ~dup
    g["h"] = g.index.map(lambda u: rng("order", u).random())
    return g.sort_values("h"), op


_AF = {}


def academy_frame(reg, op, uid):
    if uid in _AF:
        return _AF[uid]
    a = op[op["uid"] == uid].copy()
    a["band"] = a["PhaseOfEducation (name)"].map(band_of)
    m = reg.members
    mm = m[(m["Group UID"] == uid) & m["Date Left Group"].isna()][["URN", "Date Joined Group"]]
    a = a.merge(mm, on="URN", how="left")
    a["joined"] = pd.to_datetime(a["Date Joined Group"], format="%Y-%m-%d", errors="coerce")
    a["joined"] = a["joined"].fillna(a["open_d"])
    a = a.sort_values("URN").reset_index(drop=True)
    _AF[uid] = a
    return a


def pupils_billed(urn, pupils, term_start):
    r = rng("billed", urn, term_start.isoformat())
    return int(round(pupils * (1 + r.uniform(-0.05, 0.03))))


def pred_eligible(reg, urn, start):
    """A subscription can sit under the maintained-school URN if the academy converted after it started."""
    preds = reg.pred_of.get(urn, [])
    if len(preds) != 1:
        return None
    p = int(preds[0])
    old = reg.info.get(p)
    if old is None or old["EstablishmentStatus (name)"] != "Closed":
        return None
    if old["EstablishmentTypeGroup (name)"] != "Local authority maintained schools":
        return None
    conv = reg.info[int(urn)]["open_d"]
    if pd.isna(conv) or conv.date() <= start:
        return None
    return int(p)


def candidate_net(acads, subs):
    """Licence value on every open academy, less the agreements in force it replaces."""
    lic = RATE * acads["NumberOfPupils"].sum()
    return lic - sum(s["annual_value"] for s in subs)


def planned(net):
    return int(round(net * SIGN_RATE_NUM / SIGN_RATE_DEN))
