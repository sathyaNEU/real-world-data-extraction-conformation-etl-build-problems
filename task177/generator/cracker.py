"""task177 cracker and mirror sheet, run on the cut pack.

The cracker lands the call and works every ask the careful way: it executes every filed definition (the dictionary's
UTC and pence conventions, the note's credits), runs the hygiene battery (duplicate keys, unmatched joins) and joins the
obvious keys. The mirror stops at the most attractive wrong rung: the call from last January's whole-list difference,
the asks read straight off the files. Each graded ask figure is a hit when it is within half a unit of its stated
rounding (pounds to the nearest hundred: within 50; counts: exact).

    python3 cracker.py <target>        prints the sheet and the pair ceiling on Part 0's weights (38, 7, 55)"""
from __future__ import annotations

import datetime as dt
import sys

import numpy as np
import pandas as pd

import calc as K
import common as C

W_CALL, W_INSTR, W_ASKS, R_MISS = 38.0, 7.0, 55.0, 5.0


def cracker_a(P):
    """takers from the offers engine joined to subscriptions on the CRM's keys; every discount on their February and
    March bills"""
    prof = P.profile
    by_crm = dict(zip(prof.customer_no, prof.subscription_ref))
    by_app = dict(zip(prof.app_user_id[prof.app_user_id != ""], prof.subscription_ref[prof.app_user_id != ""]))
    subs = set()
    for k in P.offers.customer_key:
        s = by_crm.get(k) or by_app.get(k)
        if s:
            subs.add(s)
    plan = prof.set_index("subscription_ref").plan
    disc = P.lbs[(P.lbs.line_type == "DISC") & P.lbs.subscription_ref.isin(subs)]
    disc = disc.assign(plan=disc.subscription_ref.map(plan), m=disc.date.dt.month, y=disc.date.dt.year)
    out = {}
    for m in (2, 3):
        for pl in C.PLANS:
            out[("disc", m, pl)] = -disc[(disc.y == 2026) & (disc.m == m) & (disc.plan == pl)].amt.sum()
    tk = pd.Series(sorted(subs)).map(plan)
    for pl in C.PLANS:
        out[("takers", pl)] = int((tk == pl).sum())
    return out


def mirror_a(P):
    """the offer's code read off the discount lines; takers as the engine's distinct customers"""
    plan = P.profile.set_index("subscription_ref").plan
    disc = P.lbs[(P.lbs.line_type == "DISC") & (P.lbs.item_code == C.OFFER_CODE_WEB)]
    disc = disc.assign(plan=disc.subscription_ref.map(plan), m=disc.date.dt.month, y=disc.date.dt.year)
    out = {}
    for m in (2, 3):
        for pl in C.PLANS:
            out[("disc", m, pl)] = -disc[(disc.y == 2026) & (disc.m == m) & (disc.plan == pl)].amt.sum()
    prof = P.profile
    plan_crm = dict(zip(prof.customer_no, prof.plan))
    plan_app = dict(zip(prof.app_user_id, prof.plan))
    keys = P.offers.drop_duplicates("customer_key").customer_key
    pls = [plan_crm.get(k) or plan_app.get(k) for k in keys]
    for pl in C.PLANS:
        out[("takers", pl)] = int(sum(1 for x in pls if x == pl))
    return out


def cracker_b(P):
    """the platform's invoices filed under the list's subscriptions, by UK month; their plan lines from the lines
    column with the add-on left out and the goodwill credits kept; the legacy system's October bills through the
    crosswalk; each credit note netted against the subscription it is filed under"""
    lst = P.lst.set_index("subscription_id")
    ids = set(lst.index)
    plan = lst.plan
    head = P.spinv[P.spinv.subscription_id.isin(ids)][["invoice_id", "subscription_id", "doc_type", "uk", "amt"]]
    ln = P.spline.merge(head[head.doc_type == "invoice"].drop(columns=["amt", "doc_type"])
                        .rename(columns={"subscription_id": "head_sub"}), on="invoice_id")
    ln = ln[ln.item_code != C.ADDON_CODE]
    ln = ln.assign(ym=[(t.year, t.month) for t in ln.uk], pl=ln.head_sub.map(plan))
    cn = head[head.doc_type == "credit_note"]
    cn = cn.assign(ym=[(t.year, t.month) for t in cn.uk], pl=cn.subscription_id.map(plan))
    x = P.xwalk.set_index("legacy_subscription_ref").platform_subscription_id
    lb = P.lbs[P.lbs.line_type == "SUB"].copy()
    lb["sp"] = lb.subscription_ref.map(x)
    lb = lb[lb.sp.isin(ids) & (lb.date >= "2026-10-01")]
    out = {}
    for (y, m) in C.ASK_B_MONTHS:
        for pl in C.PLANS:
            v = ln[(ln.ym == (y, m)) & (ln.pl == pl)].amt.sum()
            v += cn[(cn.ym == (y, m)) & (cn.pl == pl)].amt.sum()
            v += lb[(lb.date.dt.year == y) & (lb.date.dt.month == m) & (lb.sp.map(plan) == pl)].amt.sum()
            out[("billed", y, m, pl)] = v
    return out


def mirror_b(P):
    """the invoice totals filed under the list's subscriptions, by the month of issued_at"""
    lst = P.lst.set_index("subscription_id")
    inv = P.spinv[P.spinv.subscription_id.isin(set(lst.index)) & (P.spinv.doc_type == "invoice")]
    inv = inv.assign(ym=[(t.year, t.month) for t in inv.utc], pl=inv.subscription_id.map(lst.plan))
    return {("billed", y, m, pl): inv[(inv.ym == (y, m)) & (inv.pl == pl)].amt.sum()
            for (y, m) in C.ASK_B_MONTHS for pl in C.PLANS}


def hit(golden, v, key):
    if key[0] == "takers":
        return int(round(v)) == int(golden)
    return abs(v - golden) < 50 or C.hundred(v) == C.hundred(golden)


def sheet(target):
    P, c, ga, gb, ly, ty = K.figures(target)
    rows = []
    for name, g, cr, mi in (("A", ga, cracker_a(P), mirror_a(P)), ("B", gb, cracker_b(P), mirror_b(P))):
        for k in g:
            rows.append((name, k, g[k], cr[k], hit(g[k], cr[k], k), mi[k], hit(g[k], mi[k], k)))
    n = len(rows)
    kc = sum(1 for r in rows if r[4])
    km = sum(1 for r in rows if r[6])
    lc, lm = kc / n, km / n
    cscore = W_CALL + W_INSTR + W_ASKS * lc
    sscore = R_MISS + W_INSTR + W_ASKS * lm
    return rows, dict(n=n, cracker_keeps=kc, mirror_keeps=km, pair=(cscore + sscore) / 2, mirror_leakage=100 * lm,
                      call_golden=c["share"], call_mirror=c["pooled"])


def main(target):
    rows, s = sheet(target)
    print("%-3s %-34s %14s %14s %5s %14s %5s" % ("ask", "figure", "golden", "cracker", "hit", "mirror", "hit"))
    for a, k, g, cr, hc, mi, hm in rows:
        print("%-3s %-34s %14.2f %14.2f %5s %14.2f %5s" % (a, str(k), g, cr, "HIT" if hc else "miss", mi, "HIT" if hm else "miss"))
    print("call: golden %.2f (%d), mirror %.2f (%d)" % (s["call_golden"], C.pct5(s["call_golden"] / 100),
                                                      s["call_mirror"], C.pct5(s["call_mirror"] / 100)))
    print("ask figures %d; cracker keeps %d, mirror keeps %d" % (s["n"], s["cracker_keeps"], s["mirror_keeps"]))
    print("Pair ceiling: %.1f   Mirror leakage: %.1f per cent of ask weight" % (s["pair"], s["mirror_leakage"]))
    return s


if __name__ == "__main__":
    main(sys.argv[1])
