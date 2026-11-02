"""Readers for the pack as a solver meets it (target/ only): the two goods-in exports conformed to one UK-time
delivery record, the processing log, the refund ledger with each return refund's made date, and the ask files. Used
by golden.py, checks.py and ceiling.py; verify.py has its own readers."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import world as W

_C = {}


def path(target, key):
    return os.path.join(target, W.FILES[key])


def _cache(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def goods(target):
    """Every goods-in scan in UK local time (naive), with the class each export gives it."""
    def load():
        a = pd.read_csv(path(target, "goods2025"), dtype=str)
        a = pd.DataFrame({"t": pd.to_datetime(a.scanned_at_uk), "barcode": a.barcode,
                          "cls": a.item_type.map({"RETURN": "RET", "STOCK TRANSFER": "TRF", "SUPPLIER SAMPLE": "SMP",
                                                  "MISDELIVERED": "MIS"}), "door": a.door})
        b = pd.read_parquet(path(target, "goods2026"))
        b = pd.DataFrame({"t": pd.to_datetime(b.event_ts_uk),
                          "barcode": b.parcel_barcode, "cls": b.parcel_class, "door": "D" + b.dock_door.astype(str)})
        return pd.concat([a, b], ignore_index=True).sort_values(["t", "barcode"], kind="stable").reset_index(drop=True)
    return _cache(("goods", target), load)


def deliveries(target, keep="first"):
    """Return parcels delivered to the centre: one per barcode, at its first scan (keep='last' for the rung)."""
    g = goods(target)
    g = g[g.cls == "RET"]
    g = g.drop_duplicates("barcode", keep=keep)
    return g.sort_values(["t", "barcode"], kind="stable").reset_index(drop=True)


def processing(target, refunds_only=False):
    def load():
        p = pd.read_csv(path(target, "processing"), dtype=str, keep_default_na=False)
        return pd.DataFrame({"t": pd.to_datetime(p.processed_at_uk), "order": p.order_ref, "label": p.return_label,
                             "outcome": p.outcome, "id": p.process_id})
    p = _cache(("proc", target), load)
    if refunds_only:
        p = p[p.outcome == "REFUND"]
    return p.sort_values(["t", "id"], kind="stable").reset_index(drop=True)


def refunds(target):
    def load():
        r = pd.read_parquet(path(target, "refunds"))
        r["t"] = r.initiated_at_utc.dt.tz_convert(W.TZ_NAME).dt.tz_localize(None)
        r["day"] = r.t.dt.date
        r["value"] = np.where(r.amount.notna(), r.amount, r.amount_pence / 100.0)
        return r
    return _cache(("refunds", target), load)


def return_refunds_made(target):
    """Each return refund once: its order and the day it was made (the payment that succeeded)."""
    r = refunds(target)
    r = r[(r.reason == "RETURN") & (r.status == "PAID")]
    assert r.order_ref.is_unique
    return r[["order_ref", "day", "t", "refund_id", "reissue_of", "currency"]].reset_index(drop=True)


def replay(target, discipline="newest", start=None, keep="first", refunds_only=False):
    """Pair every opened parcel with a delivered one through the hall: 'newest' takes the newest parcel still waiting
    at the moment of opening, 'oldest' the oldest (arrival order). start drops every delivery and opening before it
    (the rung that ignores the hall's content). Returns {process id: delivery time}."""
    d = deliveries(target, keep=keep)
    p = processing(target, refunds_only=refunds_only)
    if start is not None:
        d = d[d.t >= start]
        p = p[p.t >= start]
    dt_ = d.t.values.astype("datetime64[s]").astype(np.int64)
    pt_ = p.t.values.astype("datetime64[s]").astype(np.int64)
    ev = np.concatenate([np.stack([dt_, np.zeros(len(dt_), np.int64), np.arange(len(dt_))], 1),
                         np.stack([pt_, np.ones(len(pt_), np.int64), np.arange(len(pt_))], 1)])
    ev = ev[np.lexsort((ev[:, 2], ev[:, 1], ev[:, 0]))]
    out = {}
    stack, head = [], 0
    pid = p.id.values
    for t, kind, i in ev:
        if kind == 0:
            stack.append(i)
        elif discipline == "newest":
            out[pid[i]] = stack.pop() if stack else None
        else:
            out[pid[i]] = stack[head] if head < len(stack) else None
            head += 1
    dts = d.t.values
    return {k: (pd.Timestamp(dts[v]) if v is not None else None) for k, v in out.items()}


def refund_table(target, pairing):
    """Each return refund made, with the delivery time its parcel gets under a pairing {process id: delivery time}."""
    rf = return_refunds_made(target)
    p = processing(target)
    p = p[p.outcome == "REFUND"]
    assert p.order.is_unique
    m = rf.merge(p[["order", "id", "t", "label"]].rename(columns={"order": "order_ref", "t": "opened"}), on="order_ref",
                 how="left")
    m["delivered"] = m.id.map(pairing)
    return m


def monthly(m, late_day=W.LATE_DAY, hours=False):
    """Refunds made, late and the late share by month made, January to June 2026."""
    out = {}
    for (y, mo) in W.WINDOW_MONTHS:
        sel = m[(pd.to_datetime(m.day).dt.year == y) & (pd.to_datetime(m.day).dt.month == mo)]
        if hours:
            late = int(((sel.t - sel.delivered).dt.total_seconds() > 14 * 86400).sum())
        else:
            days = (pd.to_datetime(sel.day) - pd.to_datetime(sel.delivered.dt.date)).dt.days
            late = int((days >= late_day).sum())
        out["%d-%02d" % (y, mo)] = (int(len(sel)), late)
    return out


def orders(target):
    return _cache(("orders", target), lambda: pd.read_parquet(path(target, "orders")))


def vouchers(target):
    def load():
        v = pd.read_csv(path(target, "vouchers"), dtype=str, keep_default_na=False)
        v["value"] = v.value.astype(float)
        v["issued"] = pd.to_datetime(v.issued_at, utc=True).dt.tz_convert(W.TZ_NAME).dt.tz_localize(None)
        return v
    return _cache(("vouchers", target), load)


def redemptions(target):
    def load():
        r = pd.read_csv(path(target, "redemptions"), dtype=str, keep_default_na=False)
        r["applied"] = r.amount_applied.astype(float)
        r["t"] = pd.to_datetime(r.redeemed_at, utc=True).dt.tz_convert(W.TZ_NAME).dt.tz_localize(None)
        return r
    return _cache(("redemptions", target), load)


def cases(target):
    def load():
        c = pd.read_csv(path(target, "cases"), dtype=str, keep_default_na=False)
        c["opened"] = pd.to_datetime(c.opened_at_utc, utc=True).dt.tz_convert(W.TZ_NAME).dt.tz_localize(None)
        return c
    return _cache(("cases", target), load)
