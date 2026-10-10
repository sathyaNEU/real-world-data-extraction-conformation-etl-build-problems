"""Turn the simulated truth plus the tuning knobs into the tables the pack ships, exactly as written.

Knobs only move records: they drop basket-exit sessions (which carry no order, payment or address),
scale the net order values of an account class, and re-code or add one payment attempt."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

import params as P
import world as W

FMT = "%Y-%m-%d %H:%M:%S"


def empty_knobs():
    return {"remove": set(), "scale": {}, "flip": {}, "extra": {}, "oscale": {}}


def _ts(x):
    return [t.strftime(FMT) for t in pd.to_datetime(pd.Series(x)).dt.to_pydatetime()]


def sessions_table(T, K):
    sk = T["sk"]
    keep = ~sk.session_id.isin(K["remove"])
    s = sk[keep]
    out = pd.DataFrame({
        "session_id": s.session_id.to_numpy(),
        "started_at": _ts(s.t),
        "device": s.device.to_numpy(),
        "traffic_source": s.source.to_numpy(),
        "landing_url": s.landing_url.to_numpy(),
        "signed_in": s.signed_in.to_numpy(),
        "account_id": [a if si else None for a, si in zip(s.acct, s.signed_in)],
        "new_visitor": s.new_visitor.to_numpy(),
        "furthest_step": s.step.to_numpy(),
        "basket_skus": s.basket.to_numpy(),
        "order_id": s.order_id.to_numpy(),
        "address_fp": s.address_fp.to_numpy(),
    })
    return out.sort_values(["started_at", "session_id"], kind="mergesort").reset_index(drop=True)


def net_amounts(T, K):
    sk = T["sk"]
    sc = K["scale"]
    amt = {}
    for i in np.flatnonzero(sk.order.to_numpy()):
        key = W.aov_key(sk.seg[i], sk.klass[i], sk.mixed[i])
        f = sc.get(key, 1.0) if key else 1.0
        f *= K["oscale"].get(int(i), 1.0)
        amt[i] = round(float(sk.amount_base[i]) * f, 2)
    return amt


def finance_table(T, K):
    sk = T["sk"]
    amt = net_amounts(T, K)
    rows = []
    for i, v in amt.items():
        t = sk.t[i]
        oid = sk.order_id[i]
        exp = dt.datetime(t.year, t.month, t.day, 5, 40) + dt.timedelta(days=1)
        nship = 2 if W.is_mixed_asof(sk.basket[i], t) else 1
        gross = exp < P.FINANCE_NET_FROM
        shown = round(v * (1 + P.VAT), 2) if gross else v
        for j in range(nship):
            rows.append((oid, f"SH{oid[2:]}-{j + 1}", t.strftime(FMT), exp.strftime(FMT), shown))
        if i in T["refund"]:
            v2 = round(v * (1 - T["refund"][i]), 2)
            for j in range(nship):
                rows.append((oid, f"SH{oid[2:]}-{j + 1}", t.strftime(FMT),
                             dt.datetime(2026, 8, 17, 14, 10).strftime(FMT), v2))
    f = pd.DataFrame(rows, columns=["order_id", "shipment_id", "order_placed_at", "exported_at", "order_total_eur"])
    return f.sort_values(["exported_at", "order_id", "shipment_id"], kind="mergesort").reset_index(drop=True)


def _dup(ref):
    return int(hashlib.sha1(("resend" + ref).encode()).hexdigest()[:6], 16) % 1000 < 41


def auth_table(T, K):
    sk = T["sk"]
    a = T["attempts"].copy()
    a = a[~a.sidx.map(lambda i: sk.session_id[i]).isin(K["remove"])]
    a["outcome"] = [K["flip"].get(r, o) for r, o in zip(a.attempt_ref, a.outcome)]
    extra = []
    for ref, (sidx, outcome) in sorted(K["extra"].items()):
        r0 = a[a.sidx == sidx].sort_values("seq").iloc[0]
        extra.append(dict(sidx=sidx, attempt_ref=ref, seq=-1, outcome=outcome, authorised="N",
                          card_fp=r0.card_fp, bin6=r0.bin6, issuer=r0.issuer,
                          sent_at=r0.sent_at - dt.timedelta(seconds=95), amount_eur=r0.amount_eur))
    if extra:
        a = pd.concat([a, pd.DataFrame(extra)], ignore_index=True)
    rows = []
    for r in a.itertuples():
        base = (r.attempt_ref, sk.session_id[r.sidx], r.sent_at.strftime(FMT), r.card_fp, r.bin6, r.amount_eur,
                r.outcome, r.authorised)
        rows.append(base)
        if r.outcome in ("C", "D") and _dup(r.attempt_ref):
            rows.append((r.attempt_ref, sk.session_id[r.sidx],
                         (r.sent_at + dt.timedelta(seconds=17 + int(r.attempt_ref[-2:], 16) % 23)).strftime(FMT),
                         r.card_fp, r.bin6, r.amount_eur, r.outcome, r.authorised))
    out = pd.DataFrame(rows, columns=["attempt_ref", "session_id", "sent_at", "card_fp", "bin6", "amount_eur",
                                      "three_ds_status", "authorised"])
    return out.sort_values(["sent_at", "attempt_ref"], kind="mergesort").reset_index(drop=True)


def assemble(T, K):
    sk = T["sk"]
    tk = T["tokens"]
    aug = tk[tk.issued_at < dt.datetime(2026, 9, 1)]
    sep = tk[tk.issued_at >= dt.datetime(2026, 9, 1)]
    tok = lambda d: pd.DataFrame({"token": d.token.to_numpy(), "member_no": d.member_no.astype(int).to_numpy(),
                                  "issued_at": _ts(d.issued_at), "price_list": "SOCIOS-2026"})
    ab = T["address"].copy()
    ab["changed_at"] = _ts(ab.changed_at)
    cards = T["cards"].copy()
    cards["added_at"] = _ts(cards.added_at)
    cards = cards.sort_values(["account_id", "added_at", "card_id"]).reset_index(drop=True)
    ch = T["card_changes"].copy()
    old_default = {}
    c0 = T["cards"]
    for acct in T["switches"]:
        x = c0[(c0.account_id == acct) & c0.issuer.isin([P.ISSUER_X, P.ISSUER_Y])]
        old_default[acct] = x.card_id.iloc[0]
    ch["previous_default_card_id"] = [old_default[a] if ev == "set_default" else None
                                      for a, ev in zip(ch.account_id, ch.event)]
    ch["at"] = _ts(ch["at"])
    prof = T["profiles"].copy()
    prof["club_member_no"] = prof.club_member_no.astype("Int64")
    edge = T["edge"].copy()
    edge["first_seen"] = _ts(edge.first_seen)
    ch_h = T["cat_hist"].merge(T["cat"], on="sku")
    ch_h["valid_from"] = _ts(ch_h.valid_from)
    ch_h = ch_h[["sku", "product_name", "category", "status", "valid_from"]].sort_values(
        ["sku", "valid_from"]).reset_index(drop=True)
    promo = T["promo"].copy()
    promo["redeemed_at"] = _ts(promo.redeemed_at)
    return {
        "promo": promo,
        "sessions": sessions_table(T, K),
        "edge": edge,
        "tokens_aug": tok(aug),
        "tokens_sep": tok(sep),
        "profiles": prof,
        "address": ab,
        "flags": T["flags"],
        "cards": cards,
        "card_changes": ch,
        "auth": auth_table(T, K),
        "finance": finance_table(T, K),
        "catalogue": ch_h,
    }
