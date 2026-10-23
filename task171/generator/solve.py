"""The golden solution of task171, computed from the shipped pack (target/) only, with the rivals the design note
names. Used by build.py (figures.json, the golden workbook), checks.py and cracker.py."""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

import common as C

ASOF = pd.Timestamp(C.ASOF)


def frames(tdir):
    L = pd.read_parquet(os.path.join(tdir, C.F_LINES))
    IV = pd.read_csv(os.path.join(tdir, C.F_INV), parse_dates=["issued_on", "due_on"])
    pay = pd.read_csv(os.path.join(tdir, C.F_PAY), parse_dates=["posted_on"], keep_default_na=False, na_values=[""])
    H = pd.read_csv(os.path.join(tdir, C.F_MVD), parse_dates=["requested_on", "released_on"], keep_default_na=False, na_values=[""])
    A = pd.read_csv(os.path.join(tdir, C.F_AGY), parse_dates=["placed_on", "closed_on"], keep_default_na=False, na_values=[""])
    TT = pd.read_parquet(os.path.join(tdir, C.F_TAG))
    L["crossed_at"] = L.crossed_at.astype("datetime64[ns]"); TT["posted_at"] = TT.posted_at.astype("datetime64[ns]")
    plan = C.PLAN_TOLL
    return dict(L=L, IV=IV, pay=pay, H=H, A=A, TT=TT, plan=plan)


def toll_paid(F, cut=ASOF, whole_account=True, by_day=None):
    """Toll collected on each invoice by `cut` (posted dates), payments applied toll first. A violation agency
    remittance larger than the invoice it names covers the plate's other invoices the agency closed as collected that
    day, applied oldest first (policy 3.3). `by_day` limits each invoice's payments to its first N days."""
    IV, pay, A = F["IV"], F["pay"], F["A"]
    p = pay[pay.posted_on <= cut]
    named = p[p.invoice_no.notna()]
    if by_day is not None:
        iss = IV.set_index("invoice_no").issued_on
        named = named[(named.posted_on - named.invoice_no.map(iss)).dt.days <= by_day]
    got = named.groupby("invoice_no").amount.sum()
    got = IV.invoice_no.map(got).fillna(0.0).clip(lower=0.0).to_numpy(copy=True)
    if whole_account and by_day is None:
        bal = (IV.toll_billed + IV.invoice_fee + IV.late_fee + IV.collection_fee).to_numpy()
        pos = {k: i for i, k in enumerate(IV.invoice_no)}
        col = A[(A.status == "COLLECTED") & A.invoice_no.str.startswith("V")].copy()
        col["plate"] = col.invoice_no.map(IV.set_index("invoice_no").plate)
        col["state"] = col.invoice_no.map(IV.set_index("invoice_no").plate_state)
        grp = {k: v for k, v in col.groupby(["plate", "state", "closed_on"])}
        for r in p[(p.channel == "AGENCY") & p.invoice_no.str.startswith("V", na=False)].itertuples():
            i = pos[r.invoice_no]
            excess = got[i] - bal[i]
            if excess <= 0.01:
                continue
            got[i] = bal[i]
            k = (IV.plate.iat[i], IV.plate_state.iat[i], r.posted_on)
            if k not in grp:
                continue
            others = grp[k][grp[k].invoice_no != r.invoice_no]
            others = others.assign(iss=others.invoice_no.map(IV.set_index("invoice_no").issued_on)).sort_values(["iss", "invoice_no"])
            for kk in others.invoice_no:
                j = pos[kk]
                take = min(excess, max(bal[j] - got[j], 0.0))
                got[j] += take; excess -= take
    return np.minimum(got, IV.toll_billed.values)


def call_shares(F, cut=ASOF):
    IV, H = F["IV"], F["H"]
    tp = toll_paid(F, cut)
    t60 = toll_paid(F, cut, by_day=60)
    age = (cut - IV.issued_on).dt.days.values
    tbm = (IV.invoice_type == "TOLL-BY-MAIL").values
    home = (IV.plate_state == C.HOME).values
    hold = IV.invoice_no.map(H.set_index("invoice_no").response).values
    exp = IV.invoice_no.map(H.set_index("invoice_no").reg_expires).values
    exp_end = np.array([pd.Timestamp("%s-%s-01" % (e[3:], e[:2])) + pd.offsets.MonthEnd(0) if isinstance(e, str) and e else pd.NaT
                        for e in exp])
    toll = IV.toll_billed.values
    out = {}
    m = tbm & home & (age >= 61)
    early = t60[m].sum() / toll[m].sum()
    unpaid = m & (t60 < toll - 0.005)
    w_hold = toll[unpaid & (hold == "HOLD PLACED")].sum() / toll[unpaid].sum()
    fin = tbm & home & (hold == "HOLD PLACED") & np.array([pd.notna(e) and e <= cut for e in exp_end])
    renew = tp[fin].sum() / toll[fin].sum()
    nr = tbm & home & (hold == "NO RECORD") & (age >= 365)
    norec = tp[nr].sum() / toll[nr].sum()
    out["IS"] = early + (1 - early) * (w_hold * renew + (1 - w_hold) * norec)
    mo = tbm & ~home & (age >= 365)
    out["OS"] = tp[mo].sum() / toll[mo].sum()
    out["parts"] = dict(early=early, w_hold=w_hold, renew=renew, norec=norec, n_fin=int(fin.sum()), n_os=int(mo.sum()), n_nr=int(nr.sum()))
    return out


def golden(F):
    s = call_shares(F)
    plan = F["plan"]
    collected = plan["IS"] * s["IS"] + plan["OS"] * s["OS"]
    return dict(IS=s["IS"], OS=s["OS"], collected=collected, parts=s["parts"])


def rivals(F):
    IV = F["IV"]; plan = F["plan"]
    tp = toll_paid(F)
    age = (ASOF - IV.issued_on).dt.days.values
    tbm = (IV.invoice_type == "TOLL-BY-MAIL").values
    home = (IV.plate_state == C.HOME).values
    toll = IV.toll_billed.values
    R = {}
    for lab, a in [("observed, every invoice", 0), ("invoices 180 days old", 180), ("invoices a year old", 365), ("invoices 15 months old", 450)]:
        mi = tbm & home & (age >= a); mo = tbm & ~home & (age >= max(a, 0))
        si = tp[mi].sum() / toll[mi].sum(); so = tp[mo].sum() / toll[mo].sum()
        R[lab] = (si, so, plan["IS"] * si + plan["OS"] * so)
    # no leakage: every billed dollar collected
    R["no leakage"] = (1.0, 1.0, plan["IS"] + plan["OS"])
    # the renewal construction on every toll-by-mail and violation invoice pooled
    F2 = dict(F); IV2 = IV.copy(); IV2["invoice_type"] = "TOLL-BY-MAIL"; F2["IV"] = IV2
    s = call_shares(F2)
    R["renewal-matured, violations pooled in"] = (s["IS"], s["OS"], plan["IS"] * s["IS"] + plan["OS"] * s["OS"])
    return R


# ---------------------------------------------------------------- asks
def straddle_and_phantom(F):
    """Flags on the violation lines: the second read of a straddle, and a read 0.4 s or less behind a commercial
    posting in the same lane (a trailer or towed car the classifier split off a tag-paying truck)."""
    L = F["L"]
    V = L[L.invoice_no.str.startswith("V")].copy()
    V = V.sort_values(["plate", "plate_state", "plaza", "direction", "crossed_at"], kind="mergesort")
    same = (V.plate.eq(V.plate.shift()) & V.plate_state.eq(V.plate_state.shift()) & V.plaza.eq(V.plaza.shift())
            & V.direction.eq(V.direction.shift()) & ((V.crossed_at - V.crossed_at.shift()) <= pd.Timedelta(seconds=1)))
    V["straddle"] = same.values
    TT = F["TT"]
    key = ["plaza", "direction", "lane"]
    v = V.reset_index().sort_values("crossed_at")
    t = TT[key + ["posted_at"]].sort_values("posted_at")
    m = pd.merge_asof(v, t, left_on="crossed_at", right_on="posted_at", by=key, direction="backward")
    m["phantom"] = (m.crossed_at - m.posted_at) <= pd.Timedelta(milliseconds=400)
    V["phantom"] = m.set_index("index").phantom.reindex(V.index).fillna(False).values
    return V


def ask_A(F, V=None):
    V = straddle_and_phantom(F) if V is None else V
    ok = V[~V.straddle & ~V.phantom]
    ok = ok[(ok.crossed_at >= "2026-01-01") & (ok.crossed_at < "2026-10-01")]
    g = ok.groupby(ok.crossed_at.dt.month).agg(n=("toll", "size"), toll=("toll", "sum"))
    return {int(mo): (int(r.n), float(r.toll)) for mo, r in g.iterrows()}


QUARTERS = [("2025Q2", "2025-04-01", "2025-07-01"), ("2025Q3", "2025-07-01", "2025-10-01"),
            ("2025Q4", "2025-10-01", "2026-01-01"), ("2026Q1", "2026-01-01", "2026-04-01")]


def ask_B(F, V=None, whole_account=True):
    V = straddle_and_phantom(F) if V is None else V
    IV = F["IV"]
    owed = V[~V.straddle & ~V.phantom].groupby("invoice_no").toll.sum()
    tp = toll_paid(F, whole_account=whole_account)
    d = IV.assign(owed=IV.invoice_no.map(owed).fillna(0.0), tp=tp)
    d["got"] = np.minimum(d.tp, d.owed)
    d = d[(d.invoice_type == "VIOLATION") & (d.plate_state != C.HOME)]
    out = {}
    for q, a, b in QUARTERS:
        s = d[(d.issued_on >= a) & (d.issued_on < b)]
        out[q] = float(s.got.sum() / s.owed.sum())
    return out
