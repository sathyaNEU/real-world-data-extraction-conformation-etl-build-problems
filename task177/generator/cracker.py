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


def reader_b_a(P):
    """reader B's quoted path for ask A (round 1): "legacy DISC lines whose applied_ref is an offers-engine acceptance
    (OE26; codes STAY50 and LNT-APP-JAN26, the latter being the app route), summed by invoice month and the plan of the
    SUB line on the same invoice ... Takers = distinct subscriptions with such a discount (duplicate acceptances
    collapsed)", as quoted."""
    refs = set(P.offers.acceptance_ref)
    disc = P.lbs[(P.lbs.line_type == "DISC") & P.lbs.applied_ref.isin(refs)]
    sub = P.lbs[P.lbs.line_type == "SUB"]
    code_plan = {v: k for k, v in C.PLAN_CODE.items()}
    sub = sub.assign(pl=sub.item_code.map(code_plan)).dropna(subset=["pl"]).drop_duplicates("invoice_no")
    inv_plan = sub.set_index("invoice_no").pl
    disc = disc.assign(pl=disc.invoice_no.map(inv_plan), m=disc.date.dt.month, y=disc.date.dt.year)
    out = {}
    for m in (2, 3):
        for pl in C.PLANS:
            out[("disc", m, pl)] = -disc[(disc.y == 2026) & (disc.m == m) & (disc.pl == pl)].amt.sum()
    tk = disc.drop_duplicates("subscription_ref")
    for pl in C.PLANS:
        out[("takers", pl)] = int((tk.pl == pl).sum())
    return out


def reader_b_b(P, credits="none"):
    """reader B's quoted path for ask B (round 1): "platform invoice lines for list subscription ids, plan items only
    (puzzles add-on excluded), goodwill credit lines (LOYAL-CR) netted, month = UK date of issue"; with credits="header"
    the credit notes are also netted at their totals against the subscription they are filed under, and with
    credits="covers" the legacy 1 October bills are added through the crosswalk and each bill a credit note covers is
    taken off at its own amount (the golden's October handling)"""
    lst = P.lst.set_index("subscription_id")
    ids = set(lst.index)
    plan = lst.plan
    inv = P.spinv[P.spinv.doc_type == "invoice"][["invoice_id", "uk"]]
    ln = P.spline.merge(inv, on="invoice_id")
    ln = ln[ln.subscription_id.isin(ids) & (ln.item_code != C.ADDON_CODE)]
    ln = ln.assign(ym=[(t.year, t.month) for t in ln.uk], pl=ln.subscription_id.map(plan))
    cn = P.spinv[(P.spinv.doc_type == "credit_note") & P.spinv.subscription_id.isin(ids)]
    cn = cn.assign(ym=[(t.year, t.month) for t in cn.uk], pl=cn.subscription_id.map(plan))
    x = P.xwalk.set_index("legacy_subscription_ref").platform_subscription_id
    lb = P.lbs[P.lbs.line_type == "SUB"].copy()
    lb["sp"] = lb.subscription_ref.map(x)
    lb = lb[lb.sp.isin(ids) & (lb.date >= "2026-10-01")]
    allcn = P.spinv[P.spinv.doc_type == "credit_note"]
    covered = set(";".join(allcn.covers).split(";")) if len(allcn) else set()
    out = {}
    for (y, m) in C.ASK_B_MONTHS:
        for pl in C.PLANS:
            v = ln[(ln.ym == (y, m)) & (ln.pl == pl)].amt.sum()
            if credits == "header":
                v += cn[(cn.ym == (y, m)) & (cn.pl == pl)].amt.sum()
            elif credits == "covers":
                g = lb[(lb.date.dt.year == y) & (lb.date.dt.month == m) & (lb.sp.map(plan) == pl)]
                v += g.amt.sum() - g[g.invoice_no.isin(covered)].amt.sum()
            out[("billed", y, m, pl)] = v
    return out


def hit(golden, v, key):
    if key[0] == "takers":
        return int(round(v)) == int(golden)
    return abs(v - golden) < 50 or C.hundred(v) == C.hundred(golden)


def sheet(target):
    P, c, ga, gb, ly, ty = K.figures(target)
    paths = {"cracker": (cracker_a(P), cracker_b(P)), "mirror": (mirror_a(P), mirror_b(P)),
             "reader B as quoted": (reader_b_a(P), reader_b_b(P)),
             "reader B, credit notes at their totals": (reader_b_a(P), reader_b_b(P, "header")),
             "reader B, legacy bills and covered bills": (reader_b_a(P), reader_b_b(P, "covers"))}
    rows, keeps = [], {}
    for name, (pa, pb) in paths.items():
        k = 0
        for ask, g, p in (("A", ga, pa), ("B", gb, pb)):
            for key in g:
                h = hit(g[key], p[key], key)
                k += h
                rows.append((name, ask, key, g[key], p[key], h))
        keeps[name] = k
    n = len(ga) + len(gb)
    lc, lm = keeps["cracker"] / n, keeps["mirror"] / n
    cscore = W_CALL + W_INSTR + W_ASKS * lc
    sscore = R_MISS + W_INSTR + W_ASKS * lm
    return rows, dict(n=n, keeps=keeps, cracker_keeps=keeps["cracker"], mirror_keeps=keeps["mirror"],
                      pair=(cscore + sscore) / 2, mirror_leakage=100 * lm, call_golden=c["share"], call_mirror=c["pooled"])


def main(target):
    rows, s = sheet(target)
    print("%-42s %-3s %-30s %13s %13s %5s" % ("path", "ask", "figure", "golden", "path", "hit"))
    for name, ask, k, g, p, h in rows:
        print("%-42s %-3s %-30s %13.2f %13.2f %5s" % (name, ask, str(k), g, p, "HIT" if h else "miss"))
    print("call: golden %.2f (%d), mirror %.2f (%d)" % (s["call_golden"], C.pct5(s["call_golden"] / 100),
                                                      s["call_mirror"], C.pct5(s["call_mirror"] / 100)))
    for name, k in s["keeps"].items():
        print("ask figures kept by %s: %d of %d" % (name, k, s["n"]))
    print("Pair ceiling: %.1f   Mirror leakage: %.1f per cent of ask weight" % (s["pair"], s["mirror_leakage"]))
    return s


if __name__ == "__main__":
    main(sys.argv[1])
