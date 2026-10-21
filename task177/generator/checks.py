"""task177 checks: the generator's own assertions on the built pack and on the clean truth behind it.

    python3 task177/generator/checks.py <target>

The three-rules block (R1 to R3), the golden and its family, the one-sigma move, every semantic-fork row (SF), the
Layer 1 items mishandled one at a time (R2), the ladder, the ask devices against the world's truth, the separation
line, every graded figure's distance to its cell's edge, the distractors, the input gates and the realism sweep.
Exit 1 on any FAIL."""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import sys
import warnings
import zipfile

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K        # noqa: E402
import common as C      # noqa: E402
import cracker as CR    # noqa: E402
import docs as DOC      # noqa: E402
import ladder as L      # noqa: E402
import pack as PK       # noqa: E402
import world as W       # noqa: E402

ROWS = []
G = 20          # the golden's cell, nearest 5 per cent
DEFAULT = 10    # the default path's cell


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))
    print("%-4s %-70s %s" % ("PASS" if ok else "FAIL", label, detail), flush=True)


def cell(v):
    return C.pct5(v / 100)


# ------------------------------------------------------------------------------------- readings of the call
def ly_reading(P, ended_inclusive=False, ignore_restart=False, day_from="jan", late="feb28", arms="assign",
               outcome="access"):
    """last year's test under one reading of each convention the call needs; returns the frame with Y and d"""
    a = P.assign.merge(P.profile.drop(columns=["customer_no"]), on="subscription_ref", how="left")
    if arms == "assign":
        a["T"] = (a.arm == "offer").astype(int)
    else:                                   # the arm read off the email log: delivered (bounces count as not sent)
        got = set(P.email[P.email.event == "delivered"].customer_no)
        a["T"] = a.customer_no.isin(got).astype(int)
    ev = P.events[P.events.system == "legacy"]
    hz = pd.Timestamp(C.LY_HORIZON)
    if outcome == "access":
        ended = a.subscription_ref.map(ev[ev.event == "access_ended"].groupby("subscription_key").date.min())
        gone = ended.notna() & ((ended <= hz) if ended_inclusive else (ended < hz))
    else:                                   # read by the cancellation request
        req = a.subscription_ref.map(ev[ev.event == "cancel_requested"].groupby("subscription_key").date.min())
        gone = req.notna() & (req <= hz)
    back = a.subscription_ref.map(ev[ev.event == "restarted"].groupby("subscription_key").date.min())
    back = back.notna() & (back <= hz) & (not ignore_restart)
    a["Y"] = (~gone | back).astype(int)
    sub = P.lbs[P.lbs.line_type == "SUB"]
    if day_from == "jan":
        day = sub[(sub.date >= "2026-01-01") & (sub.date <= "2026-01-31")].groupby("subscription_ref").date.max().dt.day
        dd = a.subscription_ref.map(day)
    elif day_from == "dec":
        day = sub[(sub.date >= "2025-12-01") & (sub.date <= "2025-12-31")].groupby("subscription_ref").date.max().dt.day
        dd = a.subscription_ref.map(day)
    else:
        dd = pd.to_datetime(a.started_on).dt.day
    nb = []
    for k in dd.astype(int):
        if late == "mar1" and k > 28:
            nb.append(dt.date(2026, 3, 1))
        else:
            nb.append(C.month_day(2026, 2, int(k)))
    a["d"] = [(x - C.LY_LIST).days for x in nb]
    return a


def fortnight(a):
    return K.diff(a, (a.d >= 1) & (a.d <= 14))


# ------------------------------------------------------------------------------------- the world's truth
def ask_a_truth(R):
    ly = R.ly
    pays_mar = (ly.end_bill.values < 0) | (ly.end_bill.values >= 4)
    acc = ly.accepted.values
    out = {}
    for pl in C.PLANS:
        dpl = int(round(int(round(C.PRICE[pl] * 100)) * C.OFFER_SHARE)) / 100.0
        sel = ly.plan.values == pl
        out[("disc", 2, pl)] = round(dpl * (acc & sel).sum(), 2)
        out[("disc", 3, pl)] = round(dpl * (acc & sel & pays_mar).sum(), 2)
        out[("takers", pl)] = int((acc & sel).sum())
    return out


def ask_b_truth(R):
    T = R.ty
    out = {("billed", y, m, pl): 0.0 for (y, m) in C.ASK_B_MONTHS for pl in C.PLANS}
    for mi, (run, pend) in enumerate(PK.RUNS):
        for i in range(len(T)):
            s = dict(sub=T.sp_sub.iat[i], plan=T.plan.iat[i], start=T.start.iat[i], dom=int(T.dom.iat[i]), kind="list")
            r = PK.bill_line(s, mi, run, pend)
            if r is None:
                continue
            v = r[0][5] + (-2.0 if T.loyal_month.iat[i] == mi else 0.0)
            out[("billed", run.year, run.month, T.plan.iat[i])] += v
    return {k: round(v, 2) for k, v in out.items()}


# the call side as the stage 4 round 1 readers and judge saw it (target.zip 4827dc5d): every row the call reads, hashed
FROZEN = {
    "file:" + C.F_ASSIGN: "aa021af0dfdd60f8d932b097c67125fd5647480cb43c065b029e38d63b02b90c",
    "file:" + C.F_PROFILE: "65ea5193e3ed4c0b8647c2bd0e104e05fd5757535738b97b5caaec3715ba99b6",
    "file:" + C.F_LIST: "3ee4c6bb228565d5c8242f20274df22d46c7d53d180b9e6ee85d1ce459b38615",
    "events_access_restart": "2b2f460c050fe1d1ab9a7539f88babccf3136dbff774b3e46a84dfbde4e09aec",
    "lbs_jan_sub": "24e25533571419c4d71378f6180315bb050545e05ff8880addf4693fa2d3b4a5",
    "ty_last_to": "918ce4f1e7d614e17e849f3b2d5bef33f65498d50924ab009b2e9994b2a73428",
    "ly_Y_d": "d55845151d5da853f7327131660685d02786c39395f4d3fad131db1cd8b14784",
}
FROZEN_SHARE, FROZEN_POOLED = 19.882009365668562, 9.645895635950868


def _h(rows):
    import hashlib
    m = hashlib.sha256()
    for r in rows:
        m.update(("|".join(map(str, r)) + "\n").encode())
    return m.hexdigest()


def call_side(P, ly, target):
    import hashlib
    out = {}
    for f in (C.F_ASSIGN, C.F_PROFILE, C.F_LIST):
        out["file:" + f] = hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest()
    ev = P.events[P.events.event.isin(["access_ended", "restarted"])]
    out["events_access_restart"] = _h(sorted(zip(ev.subscription_key, ev.system, ev.event, ev.event_date)))
    jan = P.lbs[(P.lbs.line_type == "SUB") & (P.lbs.date >= "2026-01-01") & (P.lbs.date <= "2026-01-31")]
    out["lbs_jan_sub"] = _h(sorted(zip(jan.subscription_ref, jan.invoice_date, jan.line_type, jan.item_code,
                                       jan.amount_pence)))
    inv = P.spinv[P.spinv.doc_type == "invoice"][["invoice_id"]]
    ln = P.spline.merge(inv, on="invoice_id")
    last = ln[ln.subscription_id.isin(set(P.lst.subscription_id))].groupby("subscription_id").service_to.max()
    out["ty_last_to"] = _h(sorted(last.items()))
    out["ly_Y_d"] = _h(sorted(zip(ly.subscription_ref, ly.Y, ly.d, ly["T"])))
    return out


def main(target):
    P = K.Pack(target)
    c, ly, ty = K.call(P)
    ga, gb = K.ask_a(P), K.ask_b(P)
    R = PK.records()
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------------------ FROZEN: the call side
    cs = call_side(P, ly, target)
    for k_, v_ in FROZEN.items():
        check("FROZEN call side unchanged since round 1: %s" % k_, cs[k_] == v_)
    check("FROZEN the call's share and default to the last digit", c["share"] == FROZEN_SHARE and c["pooled"] == FROZEN_POOLED,
          "%r, %r" % (c["share"], c["pooled"]))

    # ------------------------------------------------------------------------------ R: the three rules
    w = R.ly
    wly = pd.DataFrame(dict(T=w["T"].values, Y=w.subscribed_h.astype(int).values, d=w.d.values))
    w_pooled = K.diff(wly)
    w_fort = K.diff(wly, wly.d <= 14)
    w_rest = K.diff(wly, wly.d > 14)
    tyw = R.ty.copy()
    tyw["d"] = 6.0
    w_truth = 100 * W.true_uplift(tyw).mean()
    check("R1 the effect lives in the fortnight before the bill (clean truth)", w_fort >= 15 and abs(w_rest) <= 3,
          "days 1-14 %.2f, days 15-28 %.2f" % (w_fort, w_rest))
    check("R1 every subscription on this year's list bills six days after the send (world and pack)",
          set(R.ty.d) == {6.0} and c["ty_days"] == [6] and c["ty_inside"] == c["n_ty"] == 48000,
          "pack days %s on %d of %d" % (c["ty_days"], c["ty_inside"], c["n_ty"]))
    check("R3 analyst test on the clean truth: the pooled arms file the default", cell(w_pooled) == DEFAULT,
          "%.2f -> %d" % (w_pooled, cell(w_pooled)))
    check("R3 analyst test on the clean truth: the fortnight's arms file the golden", cell(w_fort) == G,
          "%.2f -> %d" % (w_fort, cell(w_fort)))
    check("R3 the forecast's truth (expected share kept on this year's list) sits in the golden's cell",
          cell(w_truth) == G, "%.2f" % w_truth)
    check("R3 on the pack: the pooled arms file the default, the fortnight the golden",
          cell(c["pooled"]) == DEFAULT and cell(c["share"]) == G, "%.2f, %.2f" % (c["pooled"], c["share"]))

    # ------------------------------------------------------------------------------ the golden and its family
    gs = c["share"]
    check("golden: 20 per cent of the list kept to 31 March 2027", cell(gs) == G and figs["call_share"] == G,
          "%.2f" % gs)
    check("golden: distance to the cell's edge", C.edge(gs, 5) >= 2.0, "%.2f" % C.edge(gs, 5))
    t = ly["T"] == 1
    f = (ly.d >= 1) & (ly.d <= 14)
    p1, p0 = ly.Y[t & f].mean(), ly.Y[~t & f].mean()
    se = 100 * math.sqrt(p1 * (1 - p1) / (t & f).sum() + p0 * (1 - p0) / (~t & f).sum())
    check("one sigma either way stays in the cell", cell(gs - se) == G and cell(gs + se) == G,
          "se %.2f: %.2f to %.2f" % (se, gs - se, gs + se))
    routes = L.routes(P, c, ly, ty)
    for name, v in routes.items():
        grp = L.group(name)
        if grp == "with the step":
            check("family: %s" % name, cell(v) == G, "%.2f" % v)
        elif grp == "without the step":
            want = {"difference over the open rate": 35, "difference over the acceptance rate": 75,
                    "accepters against the holdout": 45}.get(name, DEFAULT)
            check("rival: %s" % name, cell(v) == want and cell(v) != G, "%.2f -> %d" % (v, cell(v)))
        else:
            ok = cell(v) != DEFAULT
            check("days built wrongly: %s" % name, ok, "%.2f -> %d" % (v, cell(v)))
    fam = [v for k, v in routes.items() if L.group(k) == "with the step"]
    nos = [v for k, v in routes.items() if L.group(k) == "without the step" and cell(v) == DEFAULT]
    check("lever: the step moves the call by far more than the family's spread",
          min(fam) - max(nos) > 3 * (max(fam) - min(fam)),
          "with %.2f to %.2f, without %.2f to %.2f" % (min(fam), max(fam), min(nos), max(nos)))

    # ------------------------------------------------------------------------------ SF: semantic fork rows
    note = " ".join(DOC.note_text())
    plan = " ".join(DOC.plan_text())
    fields = {(f_, k): v for f_, k, _, v in DOC.FIELDS}
    prompt = open(os.path.join(os.path.dirname(HERE), "prompt.txt"), encoding="utf-8").read()
    check("SF1 the share is of the 48,000 subscriptions on the list: the prompt",
          "48,000 subscriptions" in prompt and "share" in prompt.lower())
    check("SF2 subscribed on a day: its paid period covers it, access_ended is the last day: dictionary",
          "last day of access" in fields[(C.F_EVENTS, "event_date")])
    v = fortnight(ly_reading(P, ended_inclusive=True))
    check("SF2 access_ended read as the first day without access: same call", cell(v) == G, "%.2f" % v)
    v = fortnight(ly_reading(P, ignore_restart=True))
    check("SF3 a subscription restarted by 31 March counts; restarts ignored: same call", cell(v) == G, "%.2f" % v)
    check("SF4 kept because they are sent the offer: the prompt (sent, not taken)",
          "because they are sent" in prompt and cell(routes["accepters against the holdout"]) != G)
    check("SF5 every subscription on this year's list is sent the offer: the plan",
          "Every subscription on the list is sent the offer; nobody is held back this year." in plan)
    check("SF6 last January's arms as randomised: the plan and the assignment file",
          "The same offer went on 31 January 2026 to a random half of that day's at-risk list" in plan
          and set(P.assign.arm) == {"offer", "holdout"})
    v = fortnight(ly_reading(P, arms="email"))
    check("SF6 the arms read off the email log (bounces as not sent): same call", cell(v) == G, "%.2f" % v)
    v = fortnight(ly_reading(P, day_from="dec"))
    check("SF7 the billing day from the December 2025 bill: same call", cell(v) == G, "%.2f" % v)
    v = fortnight(ly_reading(P, day_from="start"))
    check("SF7 the billing day read off started_on: same call", cell(v) == G, "%.2f" % v)
    v = fortnight(ly_reading(P, late="mar1"))
    check("SF8 bills on the 29th to 31st falling on 1 March: same call", cell(v) == G, "%.2f" % v)
    check("SF9 the days to the bill counted from the send date (31 January, 26 January): same call (every TY day 1-14)",
          all(1 <= d_ <= 14 for d_ in (6, 7)), "6 from the send, 7 from the list cut")
    check("SF10 this year's next bill is the 1st: note 1.2 and every list subscription's last line ends 31 January",
          "From 1 November 2026 every monthly digital subscription is billed on the 1st of the month." in note
          and [str(x) for x in c["ty_next"]] == ["2027-02-01"])
    check("SF11 two bills inside each horizon: 1 February and 1 March 2027; February and March 2026",
          all(dt.date(2026, 2, 1) <= C.month_day(2026, 2, k) <= C.LY_HORIZON and
              C.month_day(2026, 3, k) <= C.LY_HORIZON for k in range(1, 32)))
    check("SF12 rounding once at the end, to the nearest 5 per cent: the prompt", "nearest 5 per cent" in prompt)
    check("SF13 the same offer both years: the plan", "The same offer went on 31 January 2026" in plan)
    v = fortnight(ly_reading(P, outcome="request"))
    check("SF14 the outcome read by the cancellation request, not by access: same call", cell(v) == G, "%.2f" % v)
    check("SF15 the unit is the subscription in both lists, one per customer number: the prompt and the files",
          P.assign.subscription_ref.is_unique and P.lst.subscription_id.is_unique and P.assign.customer_no.is_unique
          and P.lst.customer_no.is_unique)

    # ------------------------------------------------------------------------------ R2: Layer 1 one at a time
    for label, kw in (("access_ended inclusive", dict(ended_inclusive=True)), ("restarts ignored", dict(ignore_restart=True)),
                      ("arms from the email log", dict(arms="email")), ("bill day from December", dict(day_from="dec")),
                      ("bill day from started_on", dict(day_from="start")), ("29th to 31st on 1 March", dict(late="mar1"))):
        a_ = ly_reading(P, **kw)
        check("R2 %s: default still the default, step still the golden" % label,
              cell(K.diff(a_)) == DEFAULT and cell(fortnight(a_)) == G,
              "%.2f / %.2f" % (K.diff(a_), fortnight(a_)))

    # ------------------------------------------------------------------------------ ask A
    ta = ask_a_truth(R)
    check("ask A golden equals the world's truth (offer discounts and takers by plan)",
          all(abs(ga[k] - ta[k]) < 0.005 for k in ta), "; ".join("%s %s" % (k, ga[k]) for k in ta))
    cra, mia = CR.cracker_a(P), CR.mirror_a(P)
    check("ask A: the cracker (CRM and app keys through the profile) misses every figure",
          not any(CR.hit(ga[k], cra[k], k) for k in ga))
    check("ask A: the mirror (the offer's web code off the discount lines) misses every figure",
          not any(CR.hit(ga[k], mia[k], k) for k in ga))
    refs = set(P.offers.acceptance_ref)
    disc = P.lbs[P.lbs.line_type == "DISC"]
    desk = disc[disc.applied_ref.str.startswith("CS-") & disc.date.dt.month.isin([2, 3]) & (disc.date.dt.year == 2026)]
    plan_ly = P.profile.set_index("subscription_ref").plan
    hold = set(P.assign[P.assign.arm == "holdout"].subscription_ref)
    check("ask A device D5: the save desk's STAY50 on February and March bills, in both arms",
          len(desk) > 500 and desk.subscription_ref.isin(hold).sum() > 200 and (desk.item_code == C.DESK_CODE).all(),
          "%d lines, %d on held-back subscriptions" % (len(desk), desk.subscription_ref.isin(hold).sum()))
    moved = all(abs(-desk[(desk.date.dt.month == m) & (desk.subscription_ref.map(plan_ly) == pl)].amt.sum()) > 50
                for m in (2, 3) for pl in C.PLANS)
    check("ask A device D5 moves every discount cell by more than 50 pounds", moved)
    prof = P.profile
    app_keys = set(prof.app_user_id[prof.app_user_id != ""])
    app_acc = P.offers[P.offers.channel == "app"]
    unmatched = (~app_acc.customer_key.isin(app_keys)).sum()
    check("ask A device D7: app acceptances keyed by an app user id the profile no longer holds",
          unmatched > 300 and len(R.rekeyed) == unmatched, "%d of %d app acceptances" % (unmatched, len(app_acc)))
    applied = set(disc.applied_ref)
    check("ask A fair: every offer discount line's applied_ref is an acceptance; those never applied are the second "
          "acceptances and the app acceptances the engine did not apply",
          set(disc[disc.applied_ref.str.startswith("OE26-")].applied_ref) <= refs
          and len(refs - applied) == int(R.ly.also_email.sum()) + len(R.fallback),
          "%d never applied: %d second, %d app fallback" % (len(refs - applied), int(R.ly.also_email.sum()),
                                                              len(R.fallback)))
    sub = P.lbs[P.lbs.line_type == "SUB"]
    rate = sub[sub.item_code.isin(set(C.RATE_CODE.values()))]
    regular = sub[sub.item_code.isin(set(C.PLAN_CODE.values()))]
    jan_amt = regular[(regular.date >= "2026-01-01") & (regular.date <= "2026-01-31")].groupby("subscription_ref").amt.max()
    half = {pl: int(round(int(round(C.PRICE[pl] * 100)) * C.OFFER_SHARE)) / 100.0 for pl in C.PLANS}
    rplan = rate.subscription_ref.map(plan_ly)
    offer_arm = set(P.assign[P.assign.arm == "offer"].subscription_ref)
    disc_subs = set(disc[disc.applied_ref.isin(refs)].subscription_ref)
    check("ask A primary: the app acceptances the engine never applied are billed at the app's half-price rate on "
          "their February and March bills, with no discount line",
          rate.subscription_ref.nunique() == len(R.fallback) and rate.date.dt.month.isin([2, 3]).all()
          and (rate.date.dt.year == 2026).all() and rate.subscription_ref.isin(offer_arm).all()
          and not (set(rate.subscription_ref) & disc_subs),
          "%d subscriptions, %d bills" % (rate.subscription_ref.nunique(), len(rate)))
    check("ask A fair: each rate charge is the subscription's own January charge less the offer's half",
          all(abs(jan_amt[r_] - a_ - half[p_]) < 0.005 for r_, a_, p_ in zip(rate.subscription_ref, rate.amt, rplan)))
    rba = CR.reader_b_a(P)
    check("ask A: reader B's quoted path (discount lines with an acceptance ref, the plan of the bill's SUB line) "
          "misses every figure", not any(CR.hit(ga[k], rba[k], k) for k in ga),
          "nearest %.0f" % min(abs(ga[k] - rba[k]) for k in ga))
    moved_rate = {k: (-(rate[(rate.date.dt.month == k[1]) & (rplan == k[2])].amt.sum()
                        - jan_amt.reindex(rate[(rate.date.dt.month == k[1]) & (rplan == k[2])].subscription_ref).sum()))
                  for k in ga if k[0] == "disc"}
    check("ask A primary moves every discount cell by more than 50 pounds",
          all(abs(v_) > 50 for v_ in moved_rate.values()), str({k[1:]: round(v_) for k, v_ in moved_rate.items()}))
    check("ask A primary moves every takers count", all(
        (rate.drop_duplicates("subscription_ref").subscription_ref.map(plan_ly) == pl).sum() > 0 for pl in C.PLANS))
    by_acc = {}
    crm_plan, app_plan = dict(zip(prof.customer_no, prof.plan)), dict(zip(prof.app_user_id, prof.plan))
    for k in P.offers.customer_key:
        pl = crm_plan.get(k) or app_plan.get(k)
        by_acc[pl] = by_acc.get(pl, 0) + 1
    check("ask A device D1: acceptances counted as takers (both channels, rekeyed dropped) miss every plan",
          all(by_acc.get(pl, 0) != ga[("takers", pl)] for pl in C.PLANS), str(by_acc))
    app_code = disc[(disc.item_code == C.OFFER_CODE_APP)]
    check("ask A hazard: the app's own discount code on February and March bills",
          len(app_code) > 1000 and app_code.applied_ref.str.startswith("OE26-").all(), "%d lines" % len(app_code))

    # ------------------------------------------------------------------------------ ask B
    tb = ask_b_truth(R)
    check("ask B golden equals the world's truth (list subscriptions' own plan lines and goodwill credits)",
          all(abs(gb[k] - tb[k]) < 0.01 for k in tb), "max gap %.4f" % max(abs(gb[k] - tb[k]) for k in tb))
    crb, mib = CR.cracker_b(P), CR.mirror_b(P)
    check("ask B: the cracker (invoices filed under the list, plan lines, UK time, legacy bills and credit notes) "
          "misses every figure", not any(CR.hit(gb[k], crb[k], k) for k in gb),
          "nearest %.0f" % min(abs(gb[k] - crb[k]) for k in gb))
    check("ask B: the mirror (invoice totals by issued_at) misses every figure", not any(CR.hit(gb[k], mib[k], k) for k in gb))
    lst = P.lst.set_index("subscription_id")
    ids = set(lst.index)
    inv = P.spinv[P.spinv.doc_type == "invoice"]
    sl = P.spline.merge(inv[["invoice_id", "subscription_id", "account_id"]].rename(
        columns={"subscription_id": "head_sub"}), on="invoice_id")
    foreign = sl[sl.subscription_id.isin(ids) & ~sl.head_sub.isin(ids)]
    others = sl[sl.head_sub.isin(ids) & ~sl.subscription_id.isin(ids) & sl.item_code.isin(C.PLAN_CODE.values())]
    check("ask B device D7/D6: list subscriptions billed on another account's invoice",
          foreign.subscription_id.nunique() > 1000, "%d subscriptions" % foreign.subscription_id.nunique())
    check("ask B hazard D7/D6: other plans on the list's accounts' invoices, filed under a list subscription",
          others.subscription_id.nunique() > 800, "%d subscriptions" % others.subscription_id.nunique())
    hh_ex = R.ex[R.ex.household]
    seen_line = set(sl.subscription_id)
    seen_xw = set(P.xwalk.platform_subscription_id)
    acct_of = dict(zip(P.xwalk.platform_subscription_id, P.xwalk.platform_account_id))
    vis = [(s_ in seen_line) or (s_ in seen_xw and acct_of[s_] == a_) for s_, a_ in zip(hh_ex.sp_sub, hh_ex.sp_acct)]
    check("ask B fair: every household's second subscription is in the pack under its own id (its own line before the "
          "lines merge, or the crosswalk on the same account)", all(vis),
          "%d households, %d with their own line, %d set up together" % (len(hh_ex), sum(s_ in seen_line for s_ in
                                                                                       hh_ex.sp_sub),
                                                                         int(hh_ex.together.sum())))
    shared = sl[sl.subscription_id.isin(ids) & (sl.n_subs > 1)]
    by_month = {}
    for t_, iid in zip(inv.uk, inv.invoice_id):
        by_month[iid] = (t_.year, t_.month)
    shared = shared.assign(ym=shared.invoice_id.map(by_month))
    per = shared.groupby("ym").size().to_dict()
    check("ask B primary: a household's two subscriptions on one line under the list subscription, every month",
          all(per.get(ym_, 0) > 200 for ym_ in C.ASK_B_MONTHS), str({"%d-%02d" % k: v for k, v in sorted(per.items())}))
    price_of = {C.PLAN_CODE[p_]: C.PRICE[p_] for p_ in C.PLANS}
    hh_subs = set(R.ex[R.ex.household].sp_sub)
    trow = {s_: i for i, s_ in enumerate(R.ty.sp_sub.values)}

    def single(sub_id, f2):
        """the list subscription's own line for the period that starts on f2, from the world"""
        i, T_ = trow[sub_id], R.ty
        s_ = dict(sub=sub_id, plan=T_.plan.iat[i], start=T_.start.iat[i], dom=int(T_.dom.iat[i]), kind="list")
        f_ = dt.date.fromisoformat(f2)
        for mi, (run, pend) in enumerate(PK.RUNS):
            if run <= f_ <= pend:
                r_ = PK.bill_line(s_, mi, run, pend)
                return r_[0][5] if r_ else float("nan")
        return float("nan")
    check("ask B fair: every shared line counts 2 in its text and bills exactly twice the list subscription's own "
          "charge for the period; the account's other subscription is not on the list",
          (shared.n_subs == 2).all() and shared.text.str.contains(" x 2").all() and not (hh_subs & ids)
          and all(abs(a_ - 2 * single(s_, f2)) < 0.011
                  for s_, a_, f2 in zip(shared.subscription_id, shared.amt, shared.service_from)),
          "%d shared lines" % len(shared))
    rbb = CR.reader_b_b(P)
    check("ask B: reader B's quoted path (the list's lines, plan items, goodwill netted, UK date) misses every figure",
          not any(CR.hit(gb[k], rbb[k], k) for k in gb), "nearest %.0f" % min(abs(gb[k] - rbb[k]) for k in gb))
    for how in ("header", "covers"):
        rbx = CR.reader_b_b(P, how)
        check("ask B: reader B's path with the credit notes (%s) misses every figure" % how,
              not any(CR.hit(gb[k], rbx[k], k) for k in gb), "nearest %.0f" % min(abs(gb[k] - rbx[k]) for k in gb))
    check("ask B fair: every line names its own subscription; header subscription_id is the first line's",
          all(json.loads(lj)[0]["subscription_id"] == s for s, lj in zip(inv.subscription_id.values[:5000],
                                                                          inv.lines.values[:5000])))
    # the UK date against UTC: the 1 October run sits on 30 September in UTC
    oct_run = inv[inv.period_start == "2026-10-01"]
    check("ask B hazard D8: the 1 October run issued at 23:05 to 23:59 UTC on 30 September (BST)",
          (oct_run.utc.dt.month == 9).mean() > 0.98 and (oct_run.uk.dt.month == 10).all())
    cn = P.spinv[P.spinv.doc_type == "credit_note"]
    covers = [x for s in cn.covers for x in s.split(";")]
    in_pull = set(P.lbs.invoice_no)
    check("ask B hazard D1/D2: credit notes cover each account's 1 October legacy bills, add-ons and other plans in",
          len(cn) > 300 and sum(1 for x in covers if x in in_pull) < len(covers),
          "%d notes, %d bills covered, %d in the pull" % (len(cn), len(covers), sum(1 for x in covers if x in in_pull)))
    # the duplicate bills and their credits cancel exactly on the list's plans: ignoring both is the same figure
    alt = {}
    lines = P.spline.merge(inv[["invoice_id", "uk"]], on="invoice_id")
    lines = lines[lines.subscription_id.isin(ids)]
    lines = lines.assign(ym=[(t_.year, t_.month) for t_ in lines.uk])
    for (y, m) in C.ASK_B_MONTHS:
        for pl in C.PLANS:
            sel_ = lines[(lines.ym == (y, m)) & (lines.subscription_id.map(lst.plan) == pl)]
            alt[("billed", y, m, pl)] = (sel_.amt / sel_.n_subs).sum()
    check("ask B convergent reading: the platform's lines alone, a shared line counted once (no legacy bill, no credit "
          "note), give the golden", all(abs(alt[k] - gb[k]) < 0.01 for k in gb))
    hdr = {}
    for (y, m) in C.ASK_B_MONTHS:
        for pl in C.PLANS:
            s_ = inv[inv.subscription_id.isin(ids) & (inv.subscription_id.map(lst.plan) == pl)]
            hdr[("billed", y, m, pl)] = s_[[(t_.year, t_.month) == (y, m) for t_ in s_.uk]].amt.sum()
    check("ask B: invoice totals filed under the list (UK time) miss every figure",
          not any(CR.hit(gb[k], hdr[k], k) for k in gb))
    no_gw = {k: alt[k] - lines[(lines.item_code == C.LOYAL_CODE) & (lines.ym == (k[1], k[2])) &
                                (lines.subscription_id.map(lst.plan) == k[3])].amt.sum() for k in gb}
    check("ask B hazard: the goodwill credits left out miss every figure", not any(CR.hit(gb[k], no_gw[k], k) for k in gb))

    # ------------------------------------------------------------------------------ the separation line
    jan = P.lbs[(P.lbs.date >= "2026-01-01") & (P.lbs.date <= "2026-01-31")]
    ly_refs = set(P.assign.subscription_ref)
    js = jan[jan.subscription_ref.isin(ly_refs)]
    check("SEPARATION: every test subscription has exactly one January 2026 bill and no discount on it",
          (js[js.line_type == "SUB"].groupby("subscription_ref").size() == 1).all()
          and js.subscription_ref.nunique() == len(ly_refs) and set(js.line_type) <= {"SUB", "CRED"},
          "%d goodwill credits on January bills" % (js.line_type == "CRED").sum())
    ev = P.events
    check("SEPARATION: the events carry last January's list only", set(ev[ev.system == "legacy"].subscription_key) <= ly_refs)
    jan_head = set(inv[inv.subscription_id.isin(ids) & (inv.period_end == "2027-01-31")].subscription_id)
    jan_lines = sl[(sl.service_to == "2027-01-31") & sl.subscription_id.isin(ids)]
    elsewhere = set(jan_lines[~jan_lines.head_sub.isin(ids) | (jan_lines.head_sub != jan_lines.subscription_id)]
                    .subscription_id) - jan_head
    check("SEPARATION: this year's next bill is 1 February under every reading (note 1.2; every list subscription's "
          "own January line; the January invoices filed under it, the rest billed on another account's)",
          set(jan_lines.subscription_id) == ids and len(jan_head) + len(elsewhere) == len(ids),
          "%d filed under the subscription, %d on another account's invoice" % (len(jan_head), len(elsewhere)))

    # ------------------------------------------------------------------------------ edges and figures.json
    for k, v in ga.items():
        if k[0] == "disc":
            check("edge: ask A %s" % (k,), C.edge(v, 100) >= 25, "%.2f, edge %.2f" % (v, C.edge(v, 100)))
    for k, v in gb.items():
        check("edge: ask B %s" % (k,), C.edge(v, 100) >= 25, "%.2f, edge %.2f" % (v, C.edge(v, 100)))
    check("figures.json carries the call and every ask figure as computed",
          figs["call_share"] == cell(gs) and figs["call_whole_list"] == cell(c["pooled"])
          and figs["call_fortnight_kept"] == cell(c["fortnight"]) and figs["call_ty_days"] == 6
          and all(figs["ask_a_discount"]["%s %s" % (C.MONTH_NAME[m], pl)] == C.hundred(ga[("disc", m, pl)])
                  for m in (2, 3) for pl in C.PLANS)
          and all(figs["ask_a_takers"][pl] == ga[("takers", pl)] for pl in C.PLANS)
          and all(figs["ask_b_billed"]["%s %d %s" % (C.MONTH_NAME[m], y, pl)] == C.hundred(gb[("billed", y, m, pl)])
                  for (y, m) in C.ASK_B_MONTHS for pl in C.PLANS))

    # ------------------------------------------------------------------------------ distractors and gates
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    src = open(os.path.join(HERE, "calc.py")).read()
    check("distractors named in metadata.json, unread by every figure",
          set(meta["distractor_files"]) == set(C.DISTRACTORS) and not any(d.split(".")[0] in src for d in C.DISTRACTORS)
          and "F_SURVEY" not in src and "F_VALID" not in src)
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[-1] for f in files}
    check("input gates: 10 or more files, 3 or more formats, one of 25,000 rows or more",
          len(files) >= 10 and len(fmts) >= 3 and meta["input_gates"]["largest_file_rows"] >= 25000,
          "%d files, %s, %d rows" % (len(files), sorted(fmts), meta["input_gates"]["largest_file_rows"]))
    check("no file name names a distractor, a trap or the answer",
          not any(re.search(r"distract|decoy|trap|golden|answer|stump|uplift", f, re.I) for f in files))

    # ------------------------------------------------------------------------------ realism sweep
    texts = {}
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            texts[f] = open(p, encoding="utf-8").read()
        elif f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(p) as z:
                texts[f] = " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))
        else:
            texts[f] = open(p, "rb").read().decode("latin-1")
    dash = [f for f, t_ in texts.items() if "\u2014" in t_ or "\u2013" in t_]
    check("realism: no em or en dash in any file", not dash, ", ".join(dash))
    tells = [f for f, t_ in texts.items() if re.search(r"task177|generator|golden|stump|distractor|claude|openai|"
                                                      r"python-docx|openpyxl|ReportLab", t_, re.I)]
    check("realism: no build or toolchain tell in any file", not tells, ", ".join(tells))
    late = []
    for f in files:
        if f.endswith(".csv"):
            for y, mo, dd_ in re.findall(r"\b(20\d\d)-(\d\d)-(\d\d)", texts[f][:5_000_000]):
                if (int(y), int(mo), int(dd_)) > (2027, 1, 31):
                    late.append(f)
                    break
    check("realism: no date after the pull's month in any export", not late, ", ".join(late))
    names = set(re.findall(r"\b(?:Bernard|Natalie) [A-Z][a-z]+", " ".join(texts.values())))
    check("realism: the only people named are the card's personas", names <= {"Bernard Peacock", "Natalie Taylor"},
          ", ".join(sorted(names)))

    # ------------------------------------------------------------------------------ house fixes wired in
    dict_files = {f_ for f_, _, _, _ in DOC.FIELDS}
    check("H9 the data dictionary names every CSV in the pack, and nothing else",
          dict_files == {f for f in files if f.endswith(".csv")})
    pull = C.PULL
    last = {
        C.F_EVENTS: P.events.date.max(), C.F_LBS: P.lbs.date.max(),
        C.F_SPINV: P.spinv.utc.max(), C.F_OFFERS: pd.to_datetime(P.offers.accepted_at.str.replace("Z", "")).max(),
        C.F_EMAIL: pd.to_datetime(P.email.event_at.str.replace("Z", "")).max(),
    }
    late = {k: str(v) for k, v in last.items() if v > pd.Timestamp(pull)}
    check("H16 no export holds a record after the pull (25 January 2027, 18:40)", not late, str(late))
    import subprocess
    from pypdf import PdfReader
    from pdfminer.high_level import extract_text
    for f, must in ((C.F_NOTE, ("billed on the 1st of the month", "Billing Operations reports each bill")),
                    (C.F_VALID, ("validation summary", "Calibration by band"))):
        p_ = os.path.join(target, f)
        a1 = " ".join((pg.extract_text() or "") for pg in PdfReader(p_, strict=True).pages)
        a2 = extract_text(p_)
        a3 = subprocess.run(["pdftotext", "-q", p_, "-"], capture_output=True, text=True).stdout
        norm = lambda s: re.sub(r"\s+", " ", s)
        ok = all(m in norm(t_) for m in must for t_ in (a1, a2, a3))
        check("H25 %s reads in pypdf (strict), pdfminer and pdftotext with its key sentences" % f, ok)

    fails = [r for r in ROWS if not r[1]]
    print("%s: %d checks, %d FAIL" % ("PASS" if not fails else "FAIL", len(ROWS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
