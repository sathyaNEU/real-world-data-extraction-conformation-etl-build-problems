"""task177 calculations from the shipped pack only: the call, its components, the two asks, and every rival route the
ladder and the cracker name. deliver.py, checks.py and cracker.py read the pack through here; verify.py has its own
code."""
from __future__ import annotations

import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import common as C

FORTNIGHT = (1, 14)          # the days before the next bill in which the test's offer kept would-be leavers


class Pack:
    def __init__(self, target):
        self.t = target
        rd = lambda f, **k: pd.read_csv(os.path.join(target, f), dtype=str, keep_default_na=False, **k)
        self.assign = rd(C.F_ASSIGN)
        self.profile = rd(C.F_PROFILE)
        self.lst = rd(C.F_LIST)
        self.lbs = rd(C.F_LBS)
        self.spinv = rd(C.F_SPINV)
        self.xwalk = rd(C.F_XWALK)
        self.events = rd(C.F_EVENTS)
        self.offers = rd(C.F_OFFERS)
        self.email = rd(C.F_EMAIL)
        self.lbs["date"] = pd.to_datetime(self.lbs.invoice_date, format="%d/%m/%Y")
        self.lbs["amt"] = self.lbs.amount_pence.astype(int) / 100.0
        self.events["date"] = pd.to_datetime(self.events.event_date)
        self.spinv["utc"] = pd.to_datetime(self.spinv.issued_at.str.replace("Z", ""))
        self.spinv["uk"] = [C.to_local(t.to_pydatetime()) for t in self.spinv.utc]
        self.spinv["amt"] = self.spinv.amount_gbp.astype(float)
        rows = []
        for iid, lj in zip(self.spinv.invoice_id, self.spinv.lines):
            for x in json.loads(lj):
                rows.append((iid, x["line"], x["subscription_id"], x["item"], x["text"], x["from"], x["to"],
                             float(x["amount"]), int(x["qty"])))
        self.spline = pd.DataFrame(rows, columns=["invoice_id", "line_no", "subscription_id", "item_code", "text",
                                                  "service_from", "service_to", "amt", "n_subs"])


# --------------------------------------------------------------------------------------------------- the call
def ly_frame(P):
    """last year's list: arm, features, subscribed on 31 March 2026, and the days from the send to each one's next bill"""
    a = P.assign.merge(P.profile.drop(columns=["customer_no"]), on="subscription_ref", how="left")
    a["T"] = (a.arm == "offer").astype(int)
    ev = P.events[P.events.system == "legacy"]
    ended = ev[ev.event == "access_ended"].groupby("subscription_key").date.min()
    restarted = ev[ev.event == "restarted"].groupby("subscription_key").date.min()
    a["ended"] = a.subscription_ref.map(ended)
    a["restarted"] = a.subscription_ref.map(restarted)
    hz = pd.Timestamp(C.LY_HORIZON)
    gone = a.ended.notna() & (a.ended < hz)
    back = a.restarted.notna() & (a.restarted <= hz)
    a["Y"] = (~gone | back).astype(int)
    jan = P.lbs[(P.lbs.line_type == "SUB") & (P.lbs.date >= "2026-01-01") & (P.lbs.date <= "2026-01-31")]
    day = jan.groupby("subscription_ref").date.max().dt.day
    a["bill_day"] = a.subscription_ref.map(day)
    a["next_bill"] = [C.month_day(2026, 2, int(k)) for k in a.bill_day]
    a["d"] = [(nb - C.LY_LIST).days for nb in a.next_bill]
    return a


def ty_frame(P):
    """this year's list and each subscription's next bill: the day after the end of the last period it was billed
    for (its own lines, wherever the account's invoice files them)"""
    t = P.lst.copy()
    inv = P.spinv[P.spinv.doc_type == "invoice"][["invoice_id"]]
    ln = P.spline.merge(inv, on="invoice_id")
    last = ln.groupby("subscription_id").service_to.max()
    t["next_bill"] = [dt.date.fromisoformat(x) + dt.timedelta(1) for x in t.subscription_id.map(last)]
    t["d"] = [(nb - C.TY_LIST).days for nb in t.next_bill]
    return t


def diff(df, mask=None):
    if mask is not None:
        df = df[mask]
    return 100.0 * (df.Y[df["T"] == 1].mean() - df.Y[df["T"] == 0].mean())


def call(P):
    ly, ty = ly_frame(P), ty_frame(P)
    lo, hi = FORTNIGHT
    fort = (ly.d >= lo) & (ly.d <= hi)
    out = dict(
        n_ly=len(ly), n_offer=int(ly["T"].sum()), n_hold=int((1 - ly["T"]).sum()),
        n_ty=len(ty), ty_days=sorted(set(ty.d)), ty_next=sorted(set(ty.next_bill)),
        pooled=diff(ly), fortnight=diff(ly, fort), rest=diff(ly, ~fort),
        n_fort=int(fort.sum()), share_fort=fort.mean(),
        kept_offer=100 * ly.Y[ly["T"] == 1].mean(), kept_hold=100 * ly.Y[ly["T"] == 0].mean(),
    )
    # this year's list is all inside the fortnight, so its share is the test's fortnight difference
    inside = (ty.d >= lo) & (ty.d <= hi)
    out["ty_inside"] = int(inside.sum())
    out["share"] = out["fortnight"] if inside.all() else np.nan
    return out, ly, ty


# ---------------------------------------------------------------------------------------------------- ask A
def offer_discounts(P):
    """every bill line last January's offer discounted: the discount lines an acceptance applied, and the bills of
    the app acceptances the engine never applied, which charge the plan at the app's half-price rate (their discount
    is the subscription's own regular charge less the rate)"""
    refs = set(P.offers.acceptance_ref)
    # the offer's half price is a discount line, or a credit posted against the acceptance once the bill was raised
    disc = P.lbs[P.lbs.line_type.isin(["DISC", "CRED"]) & P.lbs.applied_ref.isin(refs)]
    disc = disc.assign(off=-disc.amt)
    sub = P.lbs[P.lbs.line_type == "SUB"]
    rate = sub[sub.item_code.isin(set(C.RATE_CODE.values()))]
    regular = sub[sub.item_code.isin(set(C.PLAN_CODE.values()))]
    jan = regular[(regular.date >= "2026-01-01") & (regular.date <= "2026-01-31")].groupby("subscription_ref").amt.max()
    rate = rate.assign(off=rate.subscription_ref.map(jan) - rate.amt)
    both = pd.concat([disc[["subscription_ref", "date", "off"]], rate[["subscription_ref", "date", "off"]]])
    plan = P.profile.set_index("subscription_ref").plan
    return both.assign(plan=both.subscription_ref.map(plan), m=both.date.dt.month, y=both.date.dt.year)


def ask_a(P):
    """the discount last January's offer gave on bills raised in February and March 2026, by plan; how many
    subscriptions took it, by plan"""
    d = offer_discounts(P)
    out = {}
    for (y, m) in ((2026, 2), (2026, 3)):
        for pl in C.PLANS:
            out[("disc", m, pl)] = round(d[(d.y == y) & (d.m == m) & (d.plan == pl)].off.sum(), 2)
    takers = d.drop_duplicates("subscription_ref")
    for pl in C.PLANS:
        out[("takers", pl)] = int((takers.plan == pl).sum())
    return out


# ---------------------------------------------------------------------------------------------------- ask B
def ask_b(P):
    """what the subscriptions on this year's list were billed for their plans in October, November and December 2026
    and January 2027, after credits, by plan: each list subscription's own lines (the account's invoice may carry other
    subscriptions' lines, and a list subscription may sit on another account's invoice) by the UK date the bill was
    raised, its legacy 1 October bill through the crosswalk, less each covered legacy bill at its own amount"""
    lst = P.lst.set_index("subscription_id")
    ids = set(lst.index)
    inv = P.spinv[P.spinv.doc_type == "invoice"][["invoice_id", "uk"]]
    lines = P.spline.merge(inv, on="invoice_id")
    lines = lines[lines.subscription_id.isin(ids)]
    lines = lines.assign(ym=[(t.year, t.month) for t in lines.uk])
    x = P.xwalk.set_index("legacy_subscription_ref").platform_subscription_id
    lb = P.lbs[(P.lbs.line_type == "SUB")].copy()
    lb["sp"] = lb.subscription_ref.map(x)
    lb = lb[lb.sp.isin(ids) & (lb.date >= "2026-10-01")]
    # credits: each covered legacy invoice reversed at its own amount, against its own subscription
    cn = P.spinv[P.spinv.doc_type == "credit_note"]
    covered = set(";".join(cn.covers).split(";")) if len(cn) else set()
    lb_rev = lb[lb.invoice_no.isin(covered)]
    out = {}
    plan = lst.plan
    for (y, m) in C.ASK_B_MONTHS:
        for pl in C.PLANS:
            sel = lines[(lines.ym == (y, m)) & (lines.subscription_id.map(plan) == pl)]
            sl = (sel.amt / sel.n_subs).sum()        # a line's qty counts the subscriptions it bills: one share
            lg = lb[(lb.date.dt.year == y) & (lb.date.dt.month == m) & (lb.sp.map(plan) == pl)].amt.sum()
            rv = lb_rev[(lb_rev.date.dt.year == y) & (lb_rev.date.dt.month == m) & (lb_rev.sp.map(plan) == pl)].amt.sum()
            out[("billed", y, m, pl)] = round(sl + lg - rv, 2)
    return out


def figures(target):
    P = Pack(target)
    c, ly, ty = call(P)
    return P, c, ask_a(P), ask_b(P), ly, ty
