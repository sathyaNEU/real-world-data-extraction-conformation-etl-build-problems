"""Everything owed, computed from the shipped pack alone.

The main call: each book's borrowers reaching two payments in arrears in 2027 (first time in the year, from fewer
than two, accounts on the book at 30 September 2026 and not in litigation or with a receiver), forecast with a monthly
arrears chain (0, 1, 2 or more payments behind) whose transition rates are read by cells from the 2024 to 2026
history and carried month by month from October 2026; possessions avoided are 15 per cent of the expected borrowers
taken on times the book's planning rate in the plan paper. The golden carries each account's months since a term increase as a
state; the routes below drop it (the easy route) or replace it with the rate rise at the switch."""
import os
import re

import numpy as np
import pandas as pd

import params as P

F = P.FILES
M0, SNAPM = 2024 * 12, 2026 * 12 + 8
Y27 = (2027 * 12, 2027 * 12 + 11)


def load(target, dedupe=True, strip=True, extra=()):
    cols = ["account_number", "book", "period", "remaining_term_months", "contractual_payment", "arrears_balance",
            "account_status", "product_code", "interest_rate"] + list(extra)
    H = pd.read_parquet(os.path.join(target, F["history"]), columns=cols)
    if dedupe:
        H = H.drop_duplicates()
    H["m"] = (H.period.str[:4].astype(np.int32) * 12 + H.period.str[5:7].astype(np.int32) - 1).astype(np.int32)
    H = H.drop(columns=["period"]).sort_values(["account_number", "m"]).reset_index(drop=True)
    pia = np.floor(H.arrears_balance / H.contractual_payment.where(H.contractual_payment > 0) + 1e-9).fillna(0)
    H["pia"] = np.minimum(pia, 2).astype(np.int8)
    same = H.account_number.eq(H.account_number.shift()).to_numpy()
    rem_prev = np.where(same, H.remaining_term_months.shift().fillna(0), H.remaining_term_months)
    H["ext_m"] = np.where(same & (H.remaining_term_months.to_numpy() > rem_prev), H.m, np.nan)
    H["ext_m"] = H.groupby("account_number").ext_m.ffill()
    code = H.product_code.str.replace("-", "", regex=False) if strip else H.product_code
    switch = same & (code.to_numpy() != code.shift().to_numpy())
    pay_prev = np.where(same, H.contractual_payment.shift().fillna(0), H.contractual_payment)
    rate_prev = np.where(same, H.interest_rate.shift().fillna(0), H.interest_rate)
    H["shock"] = np.where(switch, H.contractual_payment / np.maximum(pay_prev, 1) - 1, np.nan)
    H["shock"] = H.groupby("account_number").shock.ffill().fillna(0)
    H["rshock"] = np.where(switch, H.interest_rate - rate_prev, np.nan)
    H["rshock"] = H.groupby("account_number").rshock.ffill().fillna(0)
    H["sw_m"] = np.where(switch, H.m, np.nan)
    H["sw_m"] = H.groupby("account_number").sw_m.ffill()
    H["live"] = (H.account_status == "Live").to_numpy()
    nxt = np.r_[same[1:], False]
    H["pia_next"] = np.where(nxt, np.r_[H.pia.to_numpy()[1:], 0], -1).astype(np.int8)
    H["live_next"] = np.where(nxt, np.r_[H.live.to_numpy()[1:], False], False)
    B = pd.read_parquet(os.path.join(target, F["book"]))
    return H, B


def plan_rates(target):
    """the planning rates as printed in the plan paper, section 3"""
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, F["plan"])).pages)
    txt = re.sub(r"\s+", " ", txt)
    out = {}
    for b in P.ORDER:
        mm = re.search(re.escape(b) + r" (\d+\.\d) per cent", txt)
        out[b] = float(mm.group(1)) / 100
    return out


EXT_BANDS = {"golden": [8, 16], "fine": [4, 8, 12, 16, 24], "coarse": [12]}


def keyframe(df, m, route, bands=None):
    k = pd.DataFrame({"book": df.book.astype(str).to_numpy()})
    if route in ("default", "ext", "ext_noshock", "ext_mixed", "ext_pooled"):
        if route != "ext_noshock":
            k["sh"] = np.digitize(df.shock.to_numpy(), [0.05, 0.2, 0.4]).astype(np.int8)
        if route != "default":
            since = m - df.ext_m.to_numpy()
            cuts = bands or EXT_BANDS["golden"]
            lab = np.digitize(np.nan_to_num(since, nan=-1), cuts)
            k["ex"] = np.where(np.isnan(since), -1, lab)
            if route == "ext_mixed":         # the switch's payment rise read only where the term was not extended
                k["sh"] = np.where(np.isnan(since), k["sh"], -1).astype(np.int8)
            if route == "ext_pooled":        # one curve by months since the increase for every extended account
                ext = ~np.isnan(since)
                k["book"] = np.where(ext, "extended", k["book"])
                k["sh"] = np.where(ext, -1, k["sh"]).astype(np.int8)
    elif route == "rate":
        k["sh"] = np.digitize(df.rshock.to_numpy(), [0.5, 1.5, 2.5]).astype(np.int8)
        ssw = m - df.sw_m.to_numpy()
        k["sw"] = np.where(np.isnan(ssw), -1, np.digitize(np.nan_to_num(ssw, nan=-1), [8, 16]))
    elif route == "book":
        pass
    return k


def fit(H, route, bands=None, start=M0, end=SNAPM, prior=20, censor=True):
    sel = (H.m.to_numpy() >= start) & (H.m.to_numpy() < end) & H.live.to_numpy() & (H.pia_next.to_numpy() >= 0)
    if censor:          # a month in which the account closes is not a move between arrears states
        sel &= H.live_next.to_numpy()
    W = H[sel]
    K = keyframe(W, W.m.to_numpy(), route, bands)
    keys = list(K.columns)
    K["fr"], K["to"] = W.pia.to_numpy(), W.pia_next.to_numpy()
    tabs = {}
    for fr, to, name in ((0, 1, "01"), (0, 2, "02"), (1, 2, "12"), (1, 0, "10"), (2, 0, "20"), (2, 1, "21")):
        s = K[K.fr == fr].assign(y=lambda d, to=to: (d.to >= 2) if to == 2 else (d.to == to))
        tabs[name] = (s.groupby(keys).y.agg(["sum", "count"]), s.groupby("book").y.mean())
    return keys, tabs, prior


def _rate(model, name, K):
    keys, tabs, prior = model
    tab, bk = tabs[name]
    idx = pd.MultiIndex.from_frame(K[keys]) if len(keys) > 1 else pd.Index(K[keys[0]])
    s = tab["sum"].reindex(idx).fillna(0).to_numpy()
    c = tab["count"].reindex(idx).fillna(0).to_numpy()
    b = bk.reindex(K.book).to_numpy()
    # a cell with no account-months at all takes its book's rate
    return np.where(c + prior > 0, (s + prior * b) / np.maximum(c + prior, 1e-12), b)


def closure_rates(H, start=M0, end=SNAPM):
    """the monthly share of live accounts that close (redeemed or sold) by book and payments in arrears"""
    sel = (H.m.to_numpy() >= start) & (H.m.to_numpy() < end) & H.live.to_numpy()
    W = H[sel]
    gone = (W.pia_next.to_numpy() < 0) | ~W.live_next.to_numpy()
    return pd.Series(gone).groupby([W.book.astype(str).to_numpy(), W.pia.to_numpy()]).mean()


def project(H, B, route, bands=None, start=M0, prior=20, attrition=False, once=True, recoveries_out=True,
            censor=True):
    """expected first 2027 entries per account (the chain carried from October 2026, an account counted once)"""
    model = fit(H, route, bands, start=start, prior=prior, censor=censor)
    cr = closure_rates(H, start) if attrition else None
    S = H[(H.m.to_numpy() == SNAPM) & H.live.to_numpy()]
    if recoveries_out:
        stage = B.set_index("account_number").recovery_stage
        S = S[S.account_number.map(stage).to_numpy() == "None"]
    p = np.zeros((len(S), 3))
    p[np.arange(len(S)), S.pia.to_numpy().astype(int)] = 1.0
    ent = np.zeros(len(S))
    for t in range(SNAPM + 1, Y27[1] + 1):
        if cr is not None:
            bk = S.book.astype(str).to_numpy()
            for j in range(3):
                p[:, j] *= 1 - cr.reindex(pd.MultiIndex.from_arrays([bk, np.full(len(S), j)])).fillna(0).to_numpy()
        K = keyframe(S, t, route, bands)
        a01, a02, a12 = _rate(model, "01", K), _rate(model, "02", K), _rate(model, "12", K)
        a10, a20, a21 = _rate(model, "10", K), _rate(model, "20", K), _rate(model, "21", K)
        new = p[:, 0] * a02 + p[:, 1] * a12
        n0 = p[:, 0] * (1 - a01 - a02) + p[:, 1] * a10 + p[:, 2] * a20
        n1 = p[:, 0] * a01 + p[:, 1] * (1 - a12 - a10) + p[:, 2] * a21
        n2 = p[:, 2] * (1 - a20 - a21) + new
        if t >= Y27[0]:
            ent += new
            if once:
                n2 = n2 - new       # an account is taken on once: its first entry in 2027 leaves the chain
        p = np.stack([n0, n1, n2], axis=1)
    out = S[["account_number", "book", "ext_m"]].copy()
    out["entries"] = ent
    return out


def main_call(target, H=None, B=None, route="ext", bands=None, start=M0, prior=20, attrition=False, once=True,
              recoveries_out=True, censor=True):
    if H is None:
        H, B = load(target)
    rates = plan_rates(target)
    S = project(H, B, route, bands, start, prior, attrition, once, recoveries_out, censor)
    g = S.groupby("book").entries.sum()
    avoided = {b: P.EFFECT * g.get(b, 0.0) * rates[b] for b in P.ORDER}
    ext26 = S[(S.book == P.BOOKNAME["FTB"]) & (S.ext_m >= 2026 * 12) & (S.ext_m <= SNAPM)].shape[0]
    return {"entries": {b: float(g.get(b, 0.0)) for b in P.ORDER}, "avoided": avoided, "rates": rates,
            "book": max(avoided, key=avoided.get), "ftb_extended_2026": int(ext26), "S": S}


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1]
    H, B = load(tgt)
    for route, bands, start in (("default", None, M0), ("rate", None, M0), ("book", None, M0), ("ext", None, M0),
                                ("ext", EXT_BANDS["fine"], M0), ("ext", EXT_BANDS["coarse"], M0),
                                ("ext", None, 2023 * 12 + 6), ("ext_noshock", None, M0)):
        r = main_call(tgt, H, B, route, bands, start)
        print("%-12s %-22s start %d  ->  %s  | avoided %s | entries %s" % (
            route, bands, start, r["book"], {k[:5]: round(v, 1) for k, v in r["avoided"].items()},
            {k[:5]: round(v) for k, v in r["entries"].items()}), flush=True)
    print("FTB accounts with a term increase in 2026:", r["ftb_extended_2026"])


# ---------------------------------------------------------------- the workbook's two asks
def account_books(target):
    """every account's lending book as the payment history carries it (the current books, closed accounts included)"""
    h = pd.read_parquet(os.path.join(target, F["history"]), columns=["account_number", "book"])
    return h.drop_duplicates("account_number").set_index("account_number").book


def register(target):
    reg = pd.read_csv(os.path.join(target, F["possessions"]), dtype={"account_number": str})
    reg["date"] = pd.to_datetime(reg.possession_date, format="%d/%m/%Y")
    return reg


def litigation_state(target, books=None, asof=P.ASOF):
    """Ask A: the possession claims open at 30 September 2026 in each owner-occupied book and the order in force on
    each. A claim closes when it is withdrawn, its order discharged or set aside, or the property is taken into
    possession (the possession register, since one panel firm does not report evictions); the order in force is the
    latest made or varied; one panel firm reports each action once per defendant."""
    if books is None:
        books = account_books(target)
    lit = pd.read_csv(os.path.join(target, F["litigation"]), dtype={"account_number": str})
    lit = lit.drop_duplicates(["claim_number", "action_date", "action", "detail"]).copy()
    lit["d"] = pd.to_datetime(lit.action_date)
    lit = lit[lit.d <= pd.Timestamp(asof)].sort_values(["claim_number", "d"], kind="stable")
    reg = register(target)
    possd = reg[reg.date <= pd.Timestamp(asof)].groupby("account_number").date.max()
    out = []
    for claim, g in lit.groupby("claim_number", sort=False):
        acct = g.account_number.iloc[0]
        issued = g.d.min()
        if g.action.isin(["Claim withdrawn", "Order discharged", "Eviction carried out"]).any():
            continue
        pdt = possd.get(acct)
        if pdt is not None and pdt >= issued:
            continue
        orders = g[g.action.isin(["Possession order made", "Possession order varied"])]
        state = "none" if orders.empty else ("outright" if orders.detail.iloc[-1].startswith("Outright") else "suspended")
        out.append((claim, acct, books.get(acct), state))
    S = pd.DataFrame(out, columns=["claim_number", "account_number", "book", "state"])
    res = {}
    for b in P.ORDER[:3]:
        s = S[S.book == b]
        res[b] = {"open": int(len(s)), "outright": int((s.state == "outright").sum()),
                  "suspended": int((s.state == "suspended").sum())}
    return res, S


ORDER_ACTIONS = ("Possession order made", "Possession order varied")
HEARING_ACTIONS = ("Hearing listed", "Hearing adjourned")


def hearing_orders(target, books=None, lo="2025-10-01", hi="2026-09-30", reseal_is_new=False, dedupe=True):
    """Ask A, first two figures: the possession orders made or varied at hearings from October 2025 to September 2026
    in each owner-occupied book, and how many of them were suspended on terms. An order line that follows the claim's
    previous order with the same terms and no hearing between is the same order sent again, not a second order."""
    if books is None:
        books = account_books(target)
    lit = pd.read_csv(os.path.join(target, F["litigation"]), dtype={"account_number": str})
    if dedupe:
        lit = lit.drop_duplicates(["claim_number", "action_date", "action", "detail"])
    lit = lit.assign(d=pd.to_datetime(lit.action_date)).sort_values(["claim_number", "d"], kind="stable")
    rows = []
    for claim, g in lit.groupby("claim_number", sort=False):
        last, heard = None, False
        for d, act, det in zip(g.d, g.action, g.detail.fillna("")):
            if act in HEARING_ACTIONS:
                heard = True
            elif act in ORDER_ACTIONS:
                again = last is not None and not heard and det == last
                if (reseal_is_new or not again) and pd.Timestamp(lo) <= d <= pd.Timestamp(hi):
                    rows.append((claim, g.account_number.iloc[0], d, act, det))
                last, heard = det, False
    O = pd.DataFrame(rows, columns=["claim_number", "account_number", "d", "action", "detail"])
    O["book"] = O.account_number.map(books)
    return {b: {"orders": int((O.book == b).sum()),
                "suspended": int(((O.book == b) & O.detail.str.startswith("Suspended")).sum())}
            for b in P.ORDER[:3]}, O


def ask_a(target, books=None):
    if books is None:
        books = account_books(target)
    o, _ = hearing_orders(target, books)
    c, _ = litigation_state(target, books)
    return {b: {"orders": o[b]["orders"], "suspended": o[b]["suspended"], "open": c[b]["open"]} for b in P.ORDER[:3]}


def losses(target, books=None, lo="2025-10-01", hi="2026-09-30"):
    """Ask B: the possessions sold with completion from October 2025 to September 2026, how many at a loss and the
    average loss per possession sold (the debt at possession less the sale price net of selling costs, nil where the
    sale covers it), by the account's lending book. Receivers sell under their own reference; a corrected completion
    statement replaces the one before it."""
    if books is None:
        books = account_books(target)
    s = pd.read_csv(os.path.join(target, F["sales"]), dtype={"account_number": str, "receiver_ref": str})
    s = s.sort_values(["sale_ref", "statement"]).drop_duplicates("sale_ref", keep="last")
    rv = pd.read_csv(os.path.join(target, F["receivers"]), dtype={"account_number": str})
    s["acct"] = s.account_number.fillna(s.receiver_ref.map(rv.set_index("receiver_ref").account_number))
    s["d"] = pd.to_datetime(s.completion_date)
    s = s[(s.d >= pd.Timestamp(lo)) & (s.d <= pd.Timestamp(hi))].copy()
    # a property sold is one possession: the sale completes once, the register and the Society's completion
    # statements carry a row for each loan part, so the debt is every part's and the proceeds are taken once
    debt = register(target).groupby("account_number").debt_at_possession.sum()
    s = s.groupby(["acct", "d"], as_index=False).agg(sale_price=("sale_price", "first"),
                                                       selling_costs=("selling_costs", "first"))
    s["debt"] = s.acct.map(debt)
    # the debt at possession less the net proceeds, nil where the sale covers it (policy, section 8)
    s["loss"] = (s.debt - (s.sale_price - s.selling_costs)).clip(lower=0)
    s["book"] = s.acct.map(books)
    res = {}
    for b in P.ORDER:
        x = s[s.book == b]
        res[b] = {"sold": int(len(x)), "at_loss": int((x.loss > 0).sum()),
                  "avg_loss": float(x.loss.mean()) if len(x) else float("nan")}
    return res, s


# ---------------------------------------------------------------- the ladder's lower rungs and the facts the paper cites
def entries_table(H):
    """every entry: a live month at two or more payments in arrears after a month below two"""
    same = H.account_number.eq(H.account_number.shift()).to_numpy()
    prev = np.where(same, H.pia.shift().fillna(0), 0)
    return H[(H.pia.to_numpy() >= 2) & (prev < 2) & H.live.to_numpy()]


def rung_stock(H, B, rates):
    """R0: the accounts already two or more behind at 30 September 2026 (not in litigation) as the caseload"""
    S = H[(H.m.to_numpy() == SNAPM) & H.live.to_numpy()]
    stage = B.set_index("account_number").recovery_stage
    S = S[S.account_number.map(stage).to_numpy() == "None"]
    n = S[S.pia >= 2].groupby("book").size()
    return {b: P.EFFECT * float(n.get(b, 0)) * rates[b] for b in P.ORDER}


def rung_pace(H, rates):
    """R1: this year's pace, the January to September 2026 entries annualised"""
    E = entries_table(H)
    n = E[(E.m >= 2026 * 12) & (E.m <= SNAPM)].groupby("book").size()
    return {b: P.EFFECT * float(n.get(b, 0)) * 12 / 9 * rates[b] for b in P.ORDER}


def ext_facts(H, B):
    """the term increases the paper cites: the first-time buyer accounts on the book at 30 September 2026 whose
    remaining term rose in 2026, the payment change at their 2026 switch against the switchers on the book who kept
    their term, and the accounts whose term rose in 2024 with how many were two payments or more behind at a month
    end within eight months of the increase and by September 2026"""
    same = H.account_number.eq(H.account_number.shift()).to_numpy()
    rose = same & (H.remaining_term_months.to_numpy() > np.where(same, H.remaining_term_months.shift().fillna(0), 0))
    R = H[rose]
    onbook = set(B.account_number)
    ftb = P.BOOKNAME["FTB"]
    r26 = R[(R.m >= 2026 * 12) & (R.book == ftb) & R.account_number.isin(onbook)]
    prev_rem = np.where(same, H.remaining_term_months.shift().fillna(0), 0)
    added = (H.remaining_term_months.to_numpy() - prev_rem + 1)[rose]
    add26 = added[((R.m >= 2026 * 12) & (R.book == ftb) & R.account_number.isin(onbook)).to_numpy()]
    sw = H[(H.book == ftb) & (H.m >= 2026 * 12) & (H.sw_m == H.m) & H.account_number.isin(onbook)]
    ext = (sw.ext_m == sw.m).to_numpy()
    r24 = R[(R.m >= 2024 * 12) & (R.m < 2025 * 12)][["account_number", "m"]]
    E = entries_table(H)
    em = E.groupby("account_number").m.apply(np.array)

    def behind(a, lo, hi):
        x = em.get(a)
        return bool(x is not None and ((x >= lo) & (x <= hi)).any())
    early = sum(behind(a, m0 + 1, m0 + 8) for a, m0 in zip(r24.account_number, r24.m))
    by_asof = sum(behind(a, m0 + 1, SNAPM) for a, m0 in zip(r24.account_number, r24.m))
    return {"ftb_raised_2026": int(r26.account_number.nunique()),
            "ftb_on_book": int((B.book == ftb).sum()),
            "years_added_median": float(np.median(add26) / 12.0),
            "pay_rise_extended": float(np.median(sw.shock.to_numpy()[ext]) * 100),
            "pay_rise_kept": float(np.median(sw.shock.to_numpy()[~ext]) * 100),
            "raised_2024": int(r24.account_number.nunique()),
            "behind_8m": int(early), "behind_by_asof": int(by_asof)}


FAMILY = [("golden", {}), ("bands fine", {"bands": EXT_BANDS["fine"]}), ("bands 12", {"bands": [12]}),
          ("bands 6 12 18", {"bands": [6, 12, 18]}), ("bands every 3", {"bands": [3, 6, 9, 12, 15, 18, 24]}),
          ("bands monthly", {"bands": list(range(1, 25))}), ("bands to 30", {"bands": [4, 8, 12, 16, 20, 24, 30]}),
          ("window from 2023-07", {"start": 2023 * 12 + 6}), ("window from 2025", {"start": 2025 * 12}),
          ("no payment rise", {"route": "ext_noshock"}), ("rise only where not extended", {"route": "ext_mixed"}),
          ("no smoothing", {"prior": 0}), ("heavy smoothing", {"prior": 100}),
          ("no smoothing, bands monthly", {"prior": 0, "bands": list(range(1, 25))}),
          ("heavy smoothing, bands fine", {"prior": 100, "bands": EXT_BANDS["fine"]}),
          ("rise only where not extended, bands fine", {"route": "ext_mixed", "bands": EXT_BANDS["fine"]}),
          ("no payment rise, bands fine", {"route": "ext_noshock", "bands": EXT_BANDS["fine"]}),
          ("closing months read as up to date", {"censor": False}),
          ("one curve for every extended account", {"route": "ext_pooled"}),
          ("one curve, by month", {"route": "ext_pooled", "bands": list(range(1, 25))}),
          ("one curve, by month, no smoothing", {"route": "ext_pooled", "bands": list(range(1, 25)), "prior": 0}),
          ("one curve, bands fine", {"route": "ext_pooled", "bands": EXT_BANDS["fine"]})]
EASY = [("book and arrears", {"route": "book"}), ("payment rise (default path)", {"route": "default"}),
        ("rate rise by months since the switch", {"route": "rate"})]
