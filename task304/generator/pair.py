"""The ask layer measured on the cut pack: every stop of each ask's ladder (the natural read, each half-handled device,
the over-repairs) against the golden, the cracker's and the mirror's keep, and the pair ceiling."""
import os
import sys

import numpy as np
import pandas as pd

import params as P
import solve as S

F = P.FILES
OO = P.ORDER[:3]


def lit_stops(target, books=None):
    """ask A under each handling: the golden (orders at hearings, a re-sealed copy counted once; claims closed by the
    register); the re-sealed copies counted as orders; every order line counted (no defendant dedup); a repeated
    order with the same terms dropped even after a hearing; the claims open without the register, or on the book"""
    books = S.account_books(target) if books is None else books
    gold = S.ask_a(target, books)
    oc, _ = S.hearing_orders(target, books, reseal_is_new=True)
    on, _ = S.hearing_orders(target, books, reseal_is_new=True, dedupe=False)
    lit = pd.read_csv(os.path.join(target, F["litigation"]), dtype={"account_number": str})
    lit = lit.drop_duplicates(["claim_number", "action_date", "action", "detail"]).copy()
    lit["d"] = pd.to_datetime(lit.action_date)
    lit = lit.sort_values(["claim_number", "d"], kind="stable")
    # a later order with the same terms read as a duplicate whatever came between
    rows = []
    for claim, g in lit.groupby("claim_number", sort=False):
        last = None
        for d, act, det in zip(g.d, g.action, g.detail.fillna("")):
            if act in S.ORDER_ACTIONS:
                if det != last and pd.Timestamp("2025-10-01") <= d <= pd.Timestamp("2026-09-30"):
                    rows.append((g.account_number.iloc[0], det))
                last = det
    T = pd.DataFrame(rows, columns=["acct", "detail"])
    T["book"] = T.acct.map(books)
    nd = {b: {"orders": int((T.book == b).sum()), "suspended": int(((T.book == b) & T.detail.str.startswith("Suspended")).sum())}
          for b in OO}
    # open claims without the possession register, and that check made against the book instead
    noreg, onb = [], []
    bk = pd.read_parquet(os.path.join(target, F["book"]), columns=["account_number", "book", "recovery_stage"])
    onbook = set(bk.account_number)
    for claim, g in lit.groupby("claim_number", sort=False):
        if g.action.isin(["Claim withdrawn", "Order discharged", "Eviction carried out"]).any():
            continue
        noreg.append(g.account_number.iloc[0])
        if g.account_number.iloc[0] in onbook:
            onb.append(g.account_number.iloc[0])
    cnt = lambda accts: {b: int((pd.Series(accts, dtype=str).map(books) == b).sum()) for b in OO}
    nr, ob = cnt(noreg), cnt(onb)
    snap = {b: int(((bk.book == b) & (bk.recovery_stage == "Litigation")).sum()) for b in OO}

    def mix(orders, opn):
        return {b: {"orders": orders[b]["orders"], "suspended": orders[b]["suspended"], "open": opn[b]} for b in OO}
    gopen = {b: gold[b]["open"] for b in OO}
    return {"golden": gold, "reseal_counted": mix(oc, gopen), "every_line": mix(on, gopen),
            "same_terms_dropped": mix(nd, gopen), "no_register": mix(gold, nr), "on_book_no_register": mix(gold, ob),
            "careful": mix(oc, gopen), "snapshot_stage_open": snap}


def loss_stops(target, books=None):
    """ask B under each handling: the golden (one possession per account and completion, every loan part's debt);
    each statement read as a sale with the register's repeated account read as a re-sent row (the last kept), or
    summed; one sale per account with the register's last row; the register's old first-time buyer label read as
    the 2019-21 book; both statements of a corrected sale kept"""
    books = S.account_books(target) if books is None else books
    gold, s = S.losses(target, books)
    raw = pd.read_csv(os.path.join(target, F["sales"]), dtype={"account_number": str, "receiver_ref": str})
    rv = pd.read_csv(os.path.join(target, F["receivers"]), dtype={"account_number": str})
    reg = S.register(target)
    last = reg.drop_duplicates("account_number", keep="last").set_index("account_number")
    summed = reg.groupby("account_number").debt_at_possession.sum()

    def run(keep="last", debt="last", unit="statement", label=None):
        x = raw.copy()
        if keep == "last":
            x = x.sort_values(["sale_ref", "statement"]).drop_duplicates("sale_ref", keep="last")
        x["acct"] = x.account_number.fillna(x.receiver_ref.map(rv.set_index("receiver_ref").account_number))
        x["d"] = pd.to_datetime(x.completion_date)
        x = x[(x.d >= "2025-10-01") & (x.d <= "2026-09-30") & x.acct.notna()].copy()
        if unit == "account":
            x = x.groupby(["acct", "d"], as_index=False).agg(sale_price=("sale_price", "first"),
                                                               selling_costs=("selling_costs", "first"))
        x["debt"] = x.acct.map(last.debt_at_possession if debt == "last" else summed)
        x["loss"] = (x.debt - (x.sale_price - x.selling_costs)).clip(lower=0)
        if label is None:
            x["book"] = x.acct.map(books)
        else:
            x["book"] = x.acct.map(last.book).replace({P.OLD_FTB: P.BOOKNAME["FTB"]})
        return {b: {"sold": int((x.book == b).sum()), "at_loss": int(((x.book == b) & (x.loss > 0)).sum()),
                    "avg_loss": float(x.loc[x.book == b, "loss"].mean()) if (x.book == b).any() else float("nan")}
                for b in P.ORDER}

    return {"golden": gold, "statement_register_last": run(), "statement_register_summed": run(debt="summed"),
            "account_register_last": run(unit="account"), "register_label_renamed": run(unit="account", debt="summed",
                                                                                        label="renamed"),
            "both_statements": run(keep="all", unit="account", debt="summed")}


def show(target):
    a = lit_stops(target)
    for k, v in a.items():
        print("A %-22s %s" % (k, v))
    b = loss_stops(target)
    for k, v in b.items():
        print("B %-22s %s" % (k, {bk[:5]: (x["sold"], x["at_loss"], None if x["avg_loss"] != x["avg_loss"] else round(x["avg_loss"]))
                                  for bk, x in v.items()}))


if __name__ == "__main__" and len(sys.argv) == 2:
    show(sys.argv[1])


def r100(v):
    return None if v != v else int(round(v / 100.0) * 100)


def ask_figures(a, b):
    """the graded ask figures, keyed as figures.json keys them"""
    f = {}
    for bk in OO:
        k = P.SHORT[bk]
        f["askA.%s.orders" % k] = a[bk]["orders"]
        f["askA.%s.suspended" % k] = a[bk]["suspended"]
        f["askA.%s.open" % k] = a[bk]["open"]
    for bk in OO:
        k = P.SHORT[bk]
        f["askB.%s.sold" % k] = b[bk]["sold"]
        f["askB.%s.at_loss" % k] = b[bk]["at_loss"]
        f["askB.%s.avg_loss" % k] = r100(b[bk]["avg_loss"])
    return f


def keep(path, golden):
    hits = [k for k in golden if path.get(k) == golden[k]]
    return hits, len(hits) / len(golden)


def ceiling(target, books=None, r=5.0):
    """the cracker lands the call and runs the battery and every filed rule: on ask A it drops the second defendant's
    lines and closes claims through the register, but counts a re-sealed order as made again; on ask B it reads each
    completion statement as a sale and the register's repeated account as a re-sent row, keeping the last. The mirror
    stops at the default path's call and handles the asks the same way."""
    A, Bs = lit_stops(target, books), loss_stops(target, books)
    gold = ask_figures(A["golden"], Bs["golden"])
    crack = ask_figures(A["careful"], Bs["statement_register_last"])
    hits, lc = keep(crack, gold)
    c = 38 + 7 + 55 * lc
    s = r + 7 + 55 * lc
    return {"golden": gold, "cracker": crack, "hits": hits, "keep": lc, "pair": (c + s) / 2, "C": c, "S": s,
            "stops": {"A": A, "B": Bs}}


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "--ceiling":
    res = ceiling(sys.argv[1])
    print("ask figures %d; cracker keeps %d (%s)" % (len(res["golden"]), len(res["hits"]), ", ".join(res["hits"])))
    print("Pair ceiling: %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % (
        res["pair"], res["C"], res["S"], 100 * res["keep"]))
