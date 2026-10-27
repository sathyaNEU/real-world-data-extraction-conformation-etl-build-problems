"""The operating systems' exports: the legacy billing system to February 2023, the subscription register from the
December 2022 to February 2023 dual run, the CRM's customer accounts, the product's user directory, Sales Operations'
territory map and Marketing Operations' spend workbook.

build(W) turns the world into the organisation's records (companies with names, states, billing accounts and
workspaces; people with names, mobiles and emails; subscriptions, voids, divisions, reactivations, returns and plan
changes); write_all(out, B) writes the files. Every draw comes from a stream keyed by its component, so the world's
own draws never move."""
from __future__ import annotations

import datetime as dt
import math
import os
import re
import string

import numpy as np

import common as K
import world as WD

F_LEGACY = "billing_legacy_subscriptions_2015-2023.csv"
F_REG = "billing_subscription_register_2022-12_2026-09.xlsx"
F_CRM = "crm_accounts_2026-10-01.csv"
F_DIR = "product_user_directory_2026-10-01.csv"
F_TERR = "sales_territories_2024-03.csv"
F_SPEND = "marketing_spend_FY2020-FY2028.xlsx"

DUAL0 = dt.date(2022, 12, 1)        # the subscription register's first day (dual run with the legacy system)
MIGR = dt.date(2023, 3, 1)          # the legacy system's last subscriptions migrated; the register alone from here
INCLUDED = {"Core": 5, "Pro": 15, "Enterprise": 40}
PER_SEAT = {"Core": 38.0, "Pro": 48.0, "Enterprise": 44.0}
TIER = ["Core", "Pro", "Enterprise"]
# rate plan SKUs: numbered in launch order until the billing platform's new catalog of 1 July 2026 renumbered them in
# price order; a subscription keeps the SKU its plan was sold or last changed under
CUTOVER = dt.date(2026, 7, 1)
SKU_OLD = {"Pro": "PLW-100", "Enterprise": "PLW-200", "Core": "PLW-300"}
SKU_NEW = {"Core": "PLW-100", "Pro": "PLW-200", "Enterprise": "PLW-300"}
F_CATALOG = "product_catalog_2026-07-01.csv"


def sku(plan, set_on):
    return (SKU_NEW if set_on >= CUTOVER else SKU_OLD)[plan]


def plan_set_on(c, d):
    """the date the plan in force on d was sold or last changed"""
    on = c["first_inv"]
    for h in c.get("amend", []):
        if h["date"] <= d and h["change"] in ("Upgrade", "Downgrade"):
            on = h["date"]
    return on
B62 = string.digits + string.ascii_uppercase + string.ascii_lowercase
# implementation partners whose consultants run onboarding for some customers: name, billing state, created in the CRM
PARTNERS = [("Brackenridge Field Technology LLC", "TX", dt.date(2019, 4, 15), 0.35),
            ("Sandoval & Kerr Implementation Group", "CO", dt.date(2020, 2, 3), 0.25),
            ("Whitcomb Jobsite Systems", "NJ", dt.date(2021, 6, 21), 0.20),
            ("Larkin Ruiz Project Controls", "TN", dt.date(2022, 9, 12), 0.20)]


def _day(r, t):
    y, m = K.ym(t)
    return dt.date(y, m, int(r.integers(1, K.days_in(y, m) + 1)))


def acv_of(plan, seats, disc):
    extra = max(0, seats - INCLUDED[plan])
    return round((K.PLANS[plan] + extra * PER_SEAT[plan]) * 12 * (1 - disc), 2)


def anniversary(d):
    try:
        return d.replace(year=d.year + 1)
    except ValueError:
        return d.replace(year=d.year + 1, day=28)


def price_of(c, plan, seats, d):
    """the contract value of a plan and seats on date d: the first year's price where the subscription was sold on one,
    then the company's own terms"""
    fy = c.get("first_year")
    if fy and d < fy["end"]:
        return acv_of("Core", seats, 0.0) if fy["kind"] == "offer" else acv_of(plan, seats, fy["disc"])
    return acv_of(plan, seats, c["disc"])


# a 2025 sales offer sold Pro at Core's list price for its first year, on Pro's own rate plan; other new subscriptions
# were sold at an introductory discount for their first year; either price steps up on the first anniversary
OFFER = (dt.date(2025, 3, 1), dt.date(2025, 6, 30))


def first_year_pricing(B, cases, rate_offer=0.2, rate_intro=0.06, floor=3, intro_stream=54):
    ro, ri = K.rng(41), K.rng(intro_stream)          # own streams, so no other draw moves

    def eligible(c):
        end = anniversary(c["first_inv"])
        return (c["kind"] != "gc" and not c.get("booked") and c["first_inv"] <= K.DATA_END
                and not any(h["date"] < end and h["change"] in ("Upgrade", "Downgrade") for h in c.get("amend", []))
                and not any(h["date"] == end for h in c.get("amend", [])))
    offer, spare = [], []
    for c in B["comps"]:
        u, v = ro.random(), ri.random()
        if not eligible(c) or c["first_inv"] < MIGR:
            continue
        if OFFER[0] <= c["first_inv"] <= OFFER[1] and c["plan0"] == "Pro":
            (offer if u < rate_offer else spare).append(c)
        elif v < rate_intro and c["disc"] <= 0.10:
            c["first_year"] = dict(kind="intro", disc=round(c["disc"] + 0.05, 2), end=anniversary(c["first_inv"]))
    for reg in range(6):
        have = sum(1 for c in offer if c["region"] == reg)
        for c in sorted((c for c in spare if c["region"] == reg), key=lambda c: (c["first_inv"], c["crm"]))[:max(0, floor - have)]:
            offer.append(c)
    for c in offer:
        c["first_year"] = dict(kind="offer", end=anniversary(c["first_inv"]))
    acv_case = {}
    for c in B["comps"]:
        fy = c.get("first_year")
        if not fy:
            continue
        c["acv0"] = price_of(c, c["plan0"], c["seats0"], c["first_inv"])
        for h in c.get("amend", []):
            h["acv"] = price_of(c, h["plan"], h["seats"], h["date"])
        if (c["cancel"] is None or c["cancel"] > fy["end"]) and fy["end"] <= K.DATA_END:
            plan, seats = c["plan0"], c["seats0"]
            for h in c.get("amend", []):
                if h["date"] < fy["end"]:
                    plan, seats = h["plan"], h["seats"]
            c["amend"].append(dict(date=fy["end"], plan=plan, seats=seats, acv=acv_of(plan, seats, c["disc"]),
                                   change="Price change", k=0))
            c["amend"].sort(key=lambda h: h["date"])
        acv_case[id(c)] = c["acv0"]
    for cs in cases:
        if cs["kind"] == "new" and id(cs["comp"]) in acv_case:
            cs["acv"] = acv_case[id(cs["comp"])]
    return offer


def build(W):
    """Companies, people and every record the exports carry, from the world W."""
    acc = W["accounts"]
    champ = {e["acct"] for e in W["seed_events"]}
    rc = K.rng(10)                                   # company identities
    used_names, used_ws, used_crm, used_reg = set(), set(), set(), set()

    def company_name():
        while True:
            v = rc.random()
            L1, L2 = K.LAST[int(rc.integers(len(K.LAST)))], K.LAST[int(rc.integers(len(K.LAST)))]
            A, B = K.CO_A[int(rc.integers(len(K.CO_A)))], K.CO_B[int(rc.integers(len(K.CO_B)))]
            if v < 0.34:
                nm = f"{L1} {B}"
            elif v < 0.62:
                nm = f"{A} {B}"
            elif v < 0.80:
                nm = f"{L1} & {L2} {B}"
            elif v < 0.90:
                nm = f"{L1} Brothers {B}"
            else:
                nm = f"{A} {L1} {B}"
            if nm not in used_names:
                used_names.add(nm)
                return nm

    def uid_ws():
        while True:
            w = "ws_" + "".join(rc.choice(list("abcdefghjkmnpqrstuvwxyz23456789"), 10))
            if w not in used_ws:
                used_ws.add(w)
                return w

    def uid_crm():
        while True:
            c = "0018c0000" + "".join(B62[int(i)] for i in rc.integers(0, 62, 6))
            if c not in used_crm:
                used_crm.add(c)
                return c

    def uid_reg():
        while True:
            a = "A-%06d" % int(rc.integers(100000, 999999))
            if a not in used_reg:
                used_reg.add(a)
                return a

    def new_company(region, kind):
        st = K.pick(rc, K.STATES[K.REGIONS[region]])
        nm = company_name()
        suffix = " LLC" if rc.random() < 0.35 else (" Inc." if rc.random() < 0.3 else "")
        dom = re.sub(r"[^a-z]", "", nm.lower().replace("&", "and"))[:22] + str(rc.choice([".com", ".com", ".com", ".net", ".us", "co.com"]))
        return dict(region=region, state=st, name=nm + suffix, domain=dom, ws=uid_ws(), crm=uid_crm(), kind=kind,
                    legacy_code=None, reg_acct=None, subs=[], divisions=[], parent=None)

    # ---------------------------------------------------------------- one company per world account
    # the team a company signs up with (its users in the first three months, the first nine for a large contractor)
    # decides the plan it buys and the seats on its order
    team0 = {}
    for u in W["users"]:
        a = acc[u["acct"] - 1]
        if u["created_t"] <= a["start_t"] + (8 if a["gc"] else 2):
            team0[u["acct"]] = team0.get(u["acct"], 0) + 1

    def plan_mix(n):
        if n <= 4:
            return [("Core", 80), ("Pro", 18), ("Enterprise", 2)]
        if n <= 8:
            return [("Core", 52), ("Pro", 40), ("Enterprise", 8)]
        if n <= 14:
            return [("Core", 20), ("Pro", 60), ("Enterprise", 20)]
        return [("Core", 5), ("Pro", 45), ("Enterprise", 50)]

    comps = []
    by_acct = {}
    for a in acc:
        c = new_company(a["region"], "champion" if a["id"] in champ else ("gc" if a["gc"] else a["kind"]))
        c["acct"] = a["id"]
        c["start_t"], c["close_t"] = a["start_t"], a["close_t"]
        c["first_inv"] = _day(rc, a["start_t"])
        c["trial_days"] = int(rc.integers(10, 46))
        c["cancel"] = _day(rc, a["close_t"]) if a["close_t"] is not None else None
        if c["cancel"] is not None and c["cancel"] <= c["first_inv"]:
            c["cancel"] = c["first_inv"] + dt.timedelta(days=int(rc.integers(20, 40)))
        n0 = team0.get(a["id"], 1)
        p = K.pick(rc, plan_mix(n0)) if not a["gc"] else "Enterprise"
        seats = (max(INCLUDED[p], n0 + int(rc.integers(0, 12)) // 4) if not a["gc"]
                 else max(INCLUDED[p], n0 + (int(rc.integers(150, 420)) - 150) // 6))
        disc = float(rc.choice([0.0, 0.0, 0.05, 0.10, 0.15]))
        c["plan0"], c["seats0"], c["disc"] = p, seats, disc
        c["acv0"] = acv_of(p, seats, disc)
        c["lead"] = K.pick(rc, K.LEAD_CH if a["id"] in champ else K.LEAD_ORG)
        if a["gc"]:
            c["lead"] = K.pick(rc, [("Outbound - SDR", 60), ("Trade show", 25), ("Partner - association", 15)])
        comps.append(c)
        by_acct[a["id"]] = c

    # ---------------------------------------------------------------- returns after more than 12 months (new customers)
    rr = K.rng(11)
    closed = sorted([c for c in comps if c["close_t"] is not None], key=lambda c: c["close_t"])
    taken = set()
    for c in comps:
        if c["kind"] != "organic" or c["start_t"] < -24 or c["start_t"] > K.T_OBS or rr.random() > 0.025:
            continue
        cands = [o for o in closed if o["region"] == c["region"] and o["acct"] not in taken and o is not c
                 and o["close_t"] is not None and 13 <= c["start_t"] - o["close_t"] <= 40]
        if not cands:
            continue
        o = cands[int(rr.integers(len(cands)))]
        taken.add(o["acct"])
        c["returning_of"] = o["acct"]
        c["name"], c["state"], c["domain"], c["crm"] = o["name"], o["state"], o["domain"], o["crm"]
        o["returned_as"] = c["acct"]

    # ---------------------------------------------------------------- voided first invoices
    rv = K.rng(12)
    for c in comps:
        if c["start_t"] >= -40 and rv.random() < 0.045:
            gap = int(rv.integers(15, 76))
            c["void"] = dict(date=c["first_inv"] - dt.timedelta(days=gap),
                             note=K.pick(rv, [("refunded inside 14 days", 55), ("card declined, reissued", 25), ("duplicate checkout", 20)]),
                             plan=K.pick(rv, [("Core", 55), ("Pro", 35), ("Enterprise", 10)]))
    phantom = []
    for t in range(-40, K.T_OBS + 1):
        for r in range(6):
            lam = 0.02 * float(W["new"][r, W["ix"][t]])
            for _ in range(rv.poisson(lam)):
                p = new_company(r, "void_only")
                p["first_inv"] = _day(rv, t)
                p["trial_days"] = int(rv.integers(10, 46))
                p["void"] = dict(date=p["first_inv"], note=K.pick(rv, [("refunded inside 14 days", 60), ("card declined", 25), ("duplicate checkout", 15)]),
                                 plan=K.pick(rv, [("Core", 60), ("Pro", 32), ("Enterprise", 8)]))
                p["start_t"], p["close_t"], p["cancel"], p["acct"] = None, None, None, None
                phantom.append(p)

    # ---------------------------------------------------------------- divisions and reactivations
    rd = K.rng(13)
    divisions = []
    for c in comps:
        end_t = c["close_t"] if c["close_t"] is not None else K.T_OBS
        if c["start_t"] + 3 >= min(end_t, K.T_OBS) or rd.random() > (0.07 if c["kind"] != "gc" else 0.35):
            continue
        t = int(rd.integers(c["start_t"] + 3, min(end_t, K.T_OBS) + 1))
        d = dict(parent=c, start_t=t, first_inv=_day(rd, t), crm=uid_crm(), legacy_code=None, reg_acct=None,
                 name=re.sub(r" (LLC|Inc\.)$", "", c["name"]) + " - " + str(rd.choice(["Service Division", "Civil Division", "Special Projects",
                                                                                    "Residential", "North", "Commercial", "Industrial"])),
                 plan=K.pick(rd, [("Core", 60), ("Pro", 35), ("Enterprise", 5)]))
        d["seats"] = INCLUDED[d["plan"]] + int(rd.integers(0, 8))
        d["acv"] = acv_of(d["plan"], d["seats"], float(rd.choice([0.0, 0.05, 0.10])))
        d["cancel"] = c["cancel"] if c["cancel"] is not None else None
        divisions.append(d)
        c["divisions"].append(d)
    reacts = []
    for c in comps:
        if c["cancel"] is None or c["cancel"] > dt.date(2026, 6, 1) or c.get("returned_as") or rd.random() > 0.10:
            continue
        back = c["cancel"] + dt.timedelta(days=int(rd.integers(55, 335)))
        if back > K.DATA_END:
            continue
        c["react"] = dict(date=back, plan=c["plan0"], seats=c["seats0"], acv=c["acv0"])
        reacts.append(c)

    # ---------------------------------------------------------------- plan and seat changes after the first invoice
    ra = K.rng(14)
    rs2 = K.rng(25)          # seats added in the same change as a plan move (own stream, so the history above never moves)
    for c in comps:
        plan, seats, acv = c["plan0"], c["seats0"], c["acv0"]
        hist = []
        end_t = c["close_t"] if c["close_t"] is not None else K.T_OBS
        for t in range(c["start_t"] + 1, min(end_t, K.T_OBS) + 1):
            u = ra.random()
            if u < 0.008 and plan != "Enterprise":
                plan = TIER[TIER.index(plan) + 1]
                seats = max(seats, INCLUDED[plan])
                change, k = "Upgrade", 0
            elif u < 0.011 and plan != "Core" and c["kind"] != "gc":
                plan = TIER[TIER.index(plan) - 1]
                seats = max(INCLUDED[plan], min(seats, INCLUDED[plan] + 6))
                change, k = "Downgrade", 0
            elif u < 0.021:
                k = int(ra.integers(3, 16)) if c["kind"] != "gc" else int(ra.integers(10, 60))
                seats += k
                change = "Add seats"
            else:
                continue
            acv = acv_of(plan, seats, c["disc"])
            hist.append(dict(date=_day(ra, t), plan=plan, seats=seats, acv=acv, change=change, k=k))
            u2, k2 = rs2.random(), int(rs2.integers(2, 9)) if c["kind"] != "gc" else int(rs2.integers(10, 40))
            if change != "Add seats" and u2 < 0.65:
                # the customer took seats in the same change: the platform applies the plan, then the seats
                seats += k2
                acv = acv_of(plan, seats, c["disc"])
                hist.append(dict(date=hist[-1]["date"], plan=plan, seats=seats, acv=acv, change="Add seats", k=k2))
        c["amend"] = hist

    # ---------------------------------------------------------------- administrative amendments and same-day booking
    # corrections (their own streams, so the plan and seat history above never moves)
    rm = K.rng(21)
    for c in comps:
        adm = []
        end_t = c["close_t"] if c["close_t"] is not None else K.T_OBS
        for t in range(c["start_t"] + 1, min(end_t, K.T_OBS) + 1):
            if rm.random() < 0.006:
                adm.append(dict(date=_day(rm, t), change=K.pick(rm, [("Bill-to contact", 55), ("PO number", 30),
                                                                     ("Payment terms", 15)])))
        c["amend_admin"] = adm
    rk = K.rng(22)
    for c in comps:
        u = rk.random()
        if u >= 0.11:
            continue
        p0, s0 = c["plan0"], c["seats0"]
        v = rk.random()
        if v < 0.50 and p0 != "Core":
            pb = TIER[TIER.index(p0) - 1]                    # booked a tier low, upgraded on the first invoice date
            sb, change = max(INCLUDED[pb], min(s0, INCLUDED[pb] + int(rk.integers(0, 8)))), "Upgrade"
        elif v < 0.72 and p0 != "Enterprise":
            pb = TIER[TIER.index(p0) + 1]
            sb, change = max(s0, INCLUDED[pb]), "Downgrade"
        else:
            pb = p0
            k = int(rk.integers(2, 11)) if c["kind"] != "gc" else int(rk.integers(10, 40))
            sb, change = s0 - k, "Add seats"
            if sb < INCLUDED[pb]:
                continue
        c["booked"] = dict(plan=pb, seats=sb, acv=acv_of(pb, sb, c["disc"]), change=change)

    rq = K.rng(23)
    used = {c["crm"] for c in comps} | {d["crm"] for d in divisions} | {p["crm"] for p in phantom}
    partners = []
    for name, st, created, share in PARTNERS:
        while True:
            cid = "0018c0000" + "".join(B62[int(i)] for i in rq.integers(0, 62, 6))
            if cid not in used:
                used.add(cid)
                break
        partners.append(dict(crm=cid, name=name, state=st, created=created, share=share))
    B = dict(W=W, comps=comps, by_acct=by_acct, phantom=phantom, divisions=divisions, reacts=reacts,
             uid_reg=uid_reg, rc=rc, partners=partners)
    _billing(B)
    _people(B)
    return B


def rechain(c):
    """Recompute the terms after each plan and seat amendment in date order (after a later system adds one)."""
    plan, seats = c["plan0"], c["seats0"]
    out = []
    for h in sorted(c.get("amend", []), key=lambda h: h["date"]):
        if h["change"] == "Upgrade":
            if plan == "Enterprise":
                continue
            plan = TIER[TIER.index(plan) + 1]
            seats = max(seats, INCLUDED[plan])
        elif h["change"] == "Downgrade":
            if plan == "Core":
                continue
            plan = TIER[TIER.index(plan) - 1]
            seats = max(INCLUDED[plan], min(seats, INCLUDED[plan] + 6))
        else:
            seats += h["k"]
        out.append(dict(h, plan=plan, seats=seats, acv=price_of(c, plan, seats, h["date"])))
    c["amend"] = out


def _state_at(c, d):
    """plan, seats and ACV in force on date d"""
    plan, seats, acv, last = c["plan0"], c["seats0"], c["acv0"], None
    for h in c.get("amend", []):
        if h["date"] <= d:
            plan, seats, acv, last = h["plan"], h["seats"], h["acv"], h["date"]
    return plan, seats, acv, last


def _billing(B):
    """Legacy and register subscriptions, with the dual run and the migration."""
    rb = K.rng(15)
    leg, reg = [], []
    n_leg = [0]
    n_sub = [0]

    def leg_code(c):
        if c.get("legacy_code") is None:
            n_leg[0] += 1
            c["legacy_code"] = "PLW-%s-%05d" % (c["state"], 10000 + n_leg[0] * 3 + int(rb.integers(0, 3)))
        return c["legacy_code"]

    def reg_acct(c):
        if c.get("reg_acct") is None:
            c["reg_acct"] = B["uid_reg"]()
        return c["reg_acct"]

    def sub_no():
        n_sub[0] += 1
        return "SUB-%07d" % (1040000 + n_sub[0] * 7 + int(rb.integers(0, 7)))

    def add_sub(c, first, status, cancel, plan, seats, acv, note="", parent=None, kind="main", last_amend=None, cur=None):
        """One subscription, written to the system(s) its dates reach."""
        in_leg = first < MIGR
        in_reg = first >= DUAL0 or (cancel is None or cancel >= MIGR)
        legacy_sid = None
        if in_leg:
            legacy_sid = "S%06d" % (200000 + len(leg) * 3 + int(rb.integers(0, 3)))
            mig = in_reg and status == "paid"
            leg.append(dict(code=leg_code(c), sid=legacy_sid, company=c["name"], state=c["state"], plan=plan,
                            mrr_cents=int(round(acv / 12 * 100)), created=first - dt.timedelta(days=c.get("trial_days", 14)),
                            first=first, status=status, cancelled=cancel if (cancel is not None and cancel < MIGR) else None,
                            note=note if note else ("migrated 2023-03-01" if mig else ""), kind=kind, comp=c))
        if in_reg and not (status == "voided" and first < DUAL0):
            cp, cs, ca = (cur if cur is not None else (plan, seats, acv))
            reg.append(dict(acct=reg_acct(c), sub=sub_no(), parent=parent, name=c["name"], state=c["state"], plan=cp, seats=cs,
                            acv=ca, first=first, inv_status="Paid" if status == "paid" else "Voided",
                            svc_start=(max(first, MIGR) if first < DUAL0 else first),
                            status="Cancelled" if (cancel is not None and cancel <= K.DATA_END) else "Active",
                            cancel=cancel if (cancel is not None and cancel <= K.DATA_END) else None,
                            last_amend=last_amend, migrated=legacy_sid if first < MIGR else "", kind=kind, comp=c))

    for c in B["comps"] + B["phantom"]:
        if c.get("void") and c["void"]["date"] <= K.DATA_END:     # nothing invoiced after the pull's data end
            v = c["void"]
            p = v["plan"]
            add_sub(c, v["date"], "voided", v["date"] + dt.timedelta(days=int(rb.integers(2, 14))), p, INCLUDED[p],
                    acv_of(p, INCLUDED[p], 0.0), note=v["note"], kind="void")
        if c["kind"] == "void_only":
            continue
        if c["first_inv"] > K.DATA_END:
            continue
        if c.get("returning_of"):
            o = B["by_acct"][c["returning_of"]]
            c["legacy_code"] = c.get("legacy_code") or o.get("legacy_code")
            c["reg_acct"] = c.get("reg_acct") or o.get("reg_acct")
        cancel = c["cancel"] if (c["cancel"] is not None and c["cancel"] <= K.DATA_END) else None
        plan, seats, acv, last = _state_at(c, K.DATA_END if cancel is None else cancel)
        add_sub(c, c["first_inv"], "paid", cancel, c["plan0"], c["seats0"], c["acv0"], kind="main", last_amend=last,
                cur=(plan, seats, acv))
        if c.get("react"):
            r = c["react"]
            add_sub(c, r["date"], "paid", None, r["plan"], r["seats"], r["acv"], kind="react")
        for d in c["divisions"]:
            if d["first_inv"] > K.DATA_END:
                continue
            dc = dict(name=d["name"], state=c["state"], legacy_code=None, reg_acct=None, trial_days=10)
            d["bill"] = dc
            parent_acct = None
            if d["first_inv"] >= DUAL0 or (d["cancel"] is None or d["cancel"] >= MIGR):
                parent_acct = reg_acct(c)
            dcancel = d["cancel"] if (d["cancel"] is not None and d["cancel"] <= K.DATA_END) else None
            add_sub(dc, d["first_inv"], "paid", dcancel, d["plan"], d["seats"], d["acv"], parent=parent_acct, kind="division")
            d["legacy_code"], d["reg_acct"] = dc.get("legacy_code"), dc.get("reg_acct")
    B["legacy"], B["register"] = leg, reg


def _people(B):
    """Names, mobiles and emails of everyone on a workspace, and the directory rows."""
    W = B["W"]
    rp = K.rng(16)
    persons = {}
    users = W["users"]
    comp_of = B["by_acct"]
    seen = {}
    rows = []
    emails = {}
    for u in users:
        c = comp_of[u["acct"]]
        pid = u["pid"]
        if pid not in persons:
            st = c["state"]
            digits = "%d%03d%04d" % (K.AREA[st][int(rp.integers(len(K.AREA[st])))], int(rp.integers(200, 1000)), int(rp.integers(0, 10000)))
            persons[pid] = dict(first=K.FIRST[int(rp.integers(len(K.FIRST)))], last=K.LAST[int(rp.integers(len(K.LAST)))],
                                digits=digits if rp.random() > 0.12 else None, style=int(rp.choice(6, p=[0.40, 0.20, 0.15, 0.05, 0.12, 0.08])),
                                mid="ABCDEFGHJKLMRSTW"[int(rp.integers(16))], mobile=digits)
        p = persons[pid]
        k = seen.get(pid, 0)
        seen[pid] = k + 1
        first = p["first"]
        if k > 0 and rp.random() < 0.25 and first in K.NICK:
            first = K.NICK[first]
        name = f"{first} {p['mid']}. {p['last']}" if (k > 0 and rp.random() < 0.15) else f"{first} {p['last']}"
        if rp.random() < 0.65:
            local = f"{first}.{p['last']}".lower()
        else:
            local = f"{first[0]}{p['last']}".lower()
        local = re.sub(r"[^a-z.]", "", local)
        key = (c["domain"], local)
        if key in emails and emails[key] != pid:
            local = local + str(int(rp.integers(2, 9)))
        emails[(c["domain"], local)] = pid
        if p["digits"] and not (k > 0 and rp.random() < 0.06):
            style = p["style"] if (k == 0 or rp.random() > 0.15) else int(rp.integers(0, 6))
            phone = K.fmt_phone(p["digits"], style)
        else:
            phone = K.fmt_phone(p["mobile"], p["style"])     # the field app signs every user in by mobile number
        u["name"], u["email"], u["phone"] = name, f"{local}@{c['domain']}", phone
        u["title"] = K.TITLES[u["role"]][int(rp.integers(len(K.TITLES[u["role"]])))]
    B["persons"] = persons
    # timestamps (UTC) and reasons
    for u in users:
        c = comp_of[u["acct"]]
        st = c["state"]
        trial0 = (c["void"]["date"] if c.get("void") else c["first_inv"]) - dt.timedelta(days=c["trial_days"])
        if u["uid"] == B["W"]["accounts"][u["acct"] - 1]["founder_uid"]:
            d = trial0
            ca = K.local_to_utc(st, d, int(rp.integers(7, 18)), int(rp.integers(0, 60)))
        else:
            y, m = K.ym(u["created_t"])
            d = dt.date(y, m, int(rp.integers(1, K.days_in(y, m) + 1)))
            ca = K.local_to_utc(st, d, int(rp.integers(6, 19)), int(rp.integers(0, 60)))
            floor = K.local_to_utc(st, trial0, 7, 0) + dt.timedelta(days=int(rp.integers(1, 4)), hours=float(rp.uniform(0, 9)))
            if ca < floor:
                ca = floor
        u["created_at"] = ca.replace(microsecond=0)
        if u["deact_t"] is not None:
            if u["reason"] == "Account closed" and c["cancel"] is not None:
                da = dt.datetime.combine(c["cancel"], dt.time(0)) + dt.timedelta(hours=float(rp.uniform(5, 30)))
            else:
                y, m = K.ym(u["deact_t"])
                d = dt.date(y, m, int(rp.integers(1, K.days_in(y, m) + 1)))
                da = K.local_to_utc(st, d, int(rp.integers(6, 20)), int(rp.integers(0, 60)))
            da = max(da, ca + dt.timedelta(days=1)).replace(microsecond=0)
            u["deact_at"] = da
            if u["reason"] == "Left company":
                u["reason_txt"] = K.pick(rp, [("Removed by admin", 52), ("Left company", 27), ("SSO deprovisioned", 21)])
            else:
                u["reason_txt"] = K.pick(rp, [("Account closed", 1)])
        else:
            u["deact_at"], u["reason_txt"] = None, ""
        last = u["deact_at"] or dt.datetime(2026, 9, 30, 23, 0)
        la = last - dt.timedelta(hours=float(rp.uniform(1, 420)))
        u["last_active"] = min(max(la, u["created_at"] + dt.timedelta(hours=2)), dt.datetime(2026, 9, 30, 23, 0)).replace(microsecond=0)
    # reactivated companies: their workspace is reopened and a few of the old team re-invited
    extra = []
    by_acct_users = {}
    for u in users:
        by_acct_users.setdefault(u["acct"], []).append(u)
    for c in B["reacts"]:
        team = by_acct_users.get(c["acct"], [])[:int(rp.integers(2, 6))]
        for j, u0 in enumerate(team):
            when = K.local_to_utc(c["state"], c["react"]["date"] + dt.timedelta(days=j), int(rp.integers(7, 17)), int(rp.integers(0, 60)))
            extra.append(dict(uid=None, pid=u0["pid"], acct=c["acct"], role=u0["role"], name=u0["name"], email=u0["email"],
                              phone=u0["phone"], title=u0["title"], created_at=when, deact_at=None, reason_txt="",
                              last_active=min(when + dt.timedelta(days=float(rp.uniform(3, 200))), dt.datetime(2026, 9, 30, 22, 0)),
                              admin=(j == 0)))
    B["react_users"] = extra
    _trials(B)


def _trials(B):
    """Workspaces of trials: open trials of companies that pay after the export, and trials that never converted."""
    W = B["W"]
    rt = K.rng(17)
    out = []
    used = set(c["ws"] for c in B["comps"])
    # open trials: world companies whose first paid invoice falls after the export but whose trial began by then
    for c in B["comps"]:
        trial0 = (c["void"]["date"] if c.get("void") else c["first_inv"]) - dt.timedelta(days=c["trial_days"])
        c["trial0"] = trial0
    # trials that never converted, about four in five of all trials
    for t in range(-30, K.T_OBS + 1):
        for r in range(6):
            lam = 0.8 * float(W["new"][r, W["ix"][t]])
            for _ in range(rt.poisson(lam)):
                st = K.pick(rt, K.STATES[K.REGIONS[r]])
                y, m = K.ym(t)
                d = dt.date(y, m, int(rt.integers(1, K.days_in(y, m) + 1)))
                if d > K.DATA_END:
                    continue
                while True:
                    w = "ws_" + "".join(rt.choice(list("abcdefghjkmnpqrstuvwxyz23456789"), 10))
                    if w not in used:
                        used.add(w)
                        break
                dom = re.sub(r"[^a-z]", "", (K.LAST[int(rt.integers(len(K.LAST)))] + K.CO_B[int(rt.integers(len(K.CO_B)))]).lower())[:20] + ".com"
                n = 1 + int(rt.random() < 0.35) + int(rt.random() < 0.12)
                for j in range(n):
                    first, last = K.FIRST[int(rt.integers(len(K.FIRST)))], K.LAST[int(rt.integers(len(K.LAST)))]
                    digits = "%d%03d%04d" % (K.AREA[st][int(rt.integers(len(K.AREA[st])))], int(rt.integers(200, 1000)), int(rt.integers(0, 10000)))
                    ca = K.local_to_utc(st, d + dt.timedelta(days=j * int(rt.integers(0, 5))), int(rt.integers(7, 19)), int(rt.integers(0, 60)))
                    if ca.date() > K.DATA_END:
                        continue
                    role = "OWNER" if (j == 0 and rt.random() < 0.5) else str(rt.choice(["PM", "SUPER", "PE", "OFFICE"]))
                    local = re.sub(r"[^a-z.]", "", (f"{first}.{last}" if rt.random() < 0.6 else f"{first[0]}{last}").lower())
                    out.append(dict(ws=w, name=f"{first} {last}", email=f"{local}@{dom}",
                                    phone=K.fmt_phone(digits, int(rt.choice(6))) if rt.random() > 0.15 else K.fmt_phone(digits, 0),
                                    title=K.TITLES[role][int(rt.integers(len(K.TITLES[role])))], created_at=ca.replace(microsecond=0),
                                    last_active=min(ca + dt.timedelta(days=float(rt.uniform(0.2, 40))), dt.datetime(2026, 9, 30, 22, 0)).replace(microsecond=0),
                                    admin=(j == 0)))
    B["trial_users"] = out


# ==================================================================================================== writers
def write_all(out, B):
    import openpyxl
    n = {}
    W = B["W"]
    comps = B["comps"]
    # ---------------------------------------------------------------- territory map
    rows = []
    for reg, sts in K.STATES.items():
        for st, _ in sts:
            rows.append([st, K.STATE_NAMES[st], reg, K.region_of_state(st, dt.date(2024, 2, 1))])
    rows.sort(key=lambda r: r[0])
    n[F_TERR] = K.write_csv(os.path.join(out, F_TERR), ["state", "state_name", "sales_region", "sales_region_before_2024_03_01"], rows)
    # ---------------------------------------------------------------- legacy billing
    leg = sorted(B["legacy"], key=lambda r: (r["first"], r["sid"]))
    n[F_LEGACY] = K.write_csv(os.path.join(out, F_LEGACY),
        ["customer_code", "subscription_id", "company", "billing_state", "plan", "currency", "mrr_cents", "subscription_created",
         "first_invoice_date", "first_invoice_status", "cancelled_on", "notes"],
        [[r["code"], r["sid"], r["company"], r["state"], r["plan"], "USD", r["mrr_cents"], r["created"].isoformat(),
          r["first"].isoformat(), r["status"], r["cancelled"].isoformat() if r["cancelled"] else "", r["note"]] for r in leg])
    # ---------------------------------------------------------------- subscription register
    reg = sorted(B["register"], key=lambda r: (r["first"], r["sub"]))
    amend_rows = []
    for r in reg:
        if r["kind"] != "main":
            r["plan"] = sku(r["plan"], r["first"])
            continue
        c = r["comp"]
        end = r["cancel"] if r["cancel"] is not None else K.DATA_END
        plan, seats, acv, last = _state_at(c, end)
        dates = [last] if last else []
        dates += [a["date"] for a in c.get("amend_admin", []) if a["date"] <= end]
        bk = c.get("booked") if (c.get("booked") and c["first_inv"] >= DUAL0) else None
        if bk:
            dates.append(c["first_inv"])
        r["plan"], r["seats"], r["acv"], r["last_amend"] = (sku(plan, plan_set_on(c, end)), seats, acv,
                                                            (max(dates) if dates else None))
        if bk:
            amend_rows.append([c["first_inv"], 0, r["sub"], bk["change"], sku(bk["plan"], c["first_inv"]),
                               sku(c["plan0"], c["first_inv"]), bk["seats"], c["seats0"], bk["acv"], c["acv0"]])
        prev = (c["plan0"], c["seats0"], c["acv0"], c["first_inv"])
        for h in c.get("amend", []):
            set_on = h["date"] if h["change"] in ("Upgrade", "Downgrade") else prev[3]
            if h["date"] <= end and h["date"] >= DUAL0:
                amend_rows.append([h["date"], 1, r["sub"], h["change"], sku(prev[0], prev[3]), sku(h["plan"], set_on),
                                   prev[1], h["seats"], prev[2], h["acv"]])
            prev = (h["plan"], h["seats"], h["acv"], set_on)
        for a in c.get("amend_admin", []):
            if DUAL0 <= a["date"] <= end:
                p_, s_, v_, _ = _state_at(c, a["date"])
                k_ = sku(p_, plan_set_on(c, a["date"]))
                amend_rows.append([a["date"], 2, r["sub"], a["change"], k_, k_, s_, s_, v_, v_])
    for x in amend_rows:
        # the billing platform records a change of rate plan as a plan change, whichever way it goes
        x[3] = {"Upgrade": "Plan change", "Downgrade": "Plan change"}.get(x[3], x[3])
    amend_rows.sort(key=lambda x: (x[0], x[2], x[1]))
    # billing staff key a day's changes to one subscription in either order; the platform applies a plan move before the
    # seats taken with it, and each line's terms either side are as applied, while the reference follows the keying
    rkey = K.rng(26)
    i = 0
    while i < len(amend_rows):
        j = i
        while j + 1 < len(amend_rows) and amend_rows[j + 1][0] == amend_rows[i][0] and amend_rows[j + 1][2] == amend_rows[i][2]:
            j += 1
        grp = [x for x in amend_rows[i:j + 1] if x[1] == 1]
        if len(grp) > 1:
            order = [int(v) for v in rkey.permutation(len(grp))]
            rest = [x for x in amend_rows[i:j + 1] if x[1] != 1]
            amend_rows[i:j + 1] = [x for x in amend_rows[i:j + 1] if x[1] == 0] + [grp[o] for o in order] + \
                                  [x for x in rest if x[1] == 2]
        i = j + 1
    ram = K.rng(24)
    k = 0
    for x in amend_rows:
        k += 1 + int(ram.integers(0, 3))
        x[1] = "AMD-%07d" % (3100000 + k)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Subscriptions"
    ws.append(["Plinthwise subscription register: every subscription with a service period on or after 1 Dec 2022. Extracted 1 Oct 2026 07:15 MT."])
    ws.append(["Account Number", "Subscription Number", "Parent Account Number", "Account Name", "Bill To State", "Rate Plan SKU", "Seats",
               "ACV (USD)", "First Invoice Date", "First Invoice Status", "Service Start", "Subscription Status", "Cancellation Date",
               "Last Amended", "Migrated From (legacy subscription)"])
    for r in reg:
        ws.append([r["acct"], r["sub"], r["parent"] or None, r["name"], r["state"], r["plan"], r["seats"], r["acv"], r["first"],
                   r["inv_status"], r["svc_start"], r["status"], r["cancel"], r["last_amend"], r["migrated"] or None])
    for col, w in zip("ABCDEFGHIJKLMNO", [13, 16, 14, 40, 8, 12, 7, 12, 14, 12, 12, 12, 14, 12, 18]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=3):
        for cell in row:
            if isinstance(cell.value, dt.date):
                cell.number_format = "yyyy-mm-dd"
            elif cell.column_letter == "H":
                cell.number_format = "#,##0.00"
    ws.freeze_panes = "A3"
    wa = wb.create_sheet("Amendments")
    wa.append(["Plinthwise subscription register: amendments recorded from 1 Dec 2022. Extracted 1 Oct 2026 07:15 MT."])
    wa.append(["Effective Date", "Amendment Number", "Subscription Number", "Change", "SKU Before", "SKU After", "Seats Before",
               "Seats After", "ACV Before (USD)", "ACV After (USD)"])
    for x in amend_rows:
        wa.append(x)
    for col, w in zip("ABCDEFGHIJ", [14, 16, 18, 16, 12, 12, 12, 12, 16, 16]):
        wa.column_dimensions[col].width = w
    for row in wa.iter_rows(min_row=3):
        for cell in row:
            if isinstance(cell.value, dt.date):
                cell.number_format = "yyyy-mm-dd"
            elif cell.column_letter in "IJ":
                cell.number_format = "#,##0.00"
    wa.freeze_panes = "A3"
    wb.save(os.path.join(out, F_REG))
    n[F_REG] = len(reg) + len(amend_rows)
    # ---------------------------------------------------------------- the product catalog (the new platform's)
    n[F_CATALOG] = K.write_csv(os.path.join(out, F_CATALOG),
        ["sku", "plan", "list_price_month_usd", "seats_included", "extra_seat_month_usd", "in_catalog_from"],
        [[SKU_NEW[p_], p_, "%.2f" % K.PLANS[p_], INCLUDED[p_], "%.2f" % PER_SEAT[p_], CUTOVER.isoformat()] for p_ in TIER])
    # ---------------------------------------------------------------- CRM accounts
    rc = K.rng(18)
    crm = []
    seen_crm = set()
    for c in comps:
        if c["first_inv"] > K.DATA_END or c["crm"] in seen_crm:
            continue
        if c.get("returned_as"):
            continue                                   # the returning company's row carries the account
        seen_crm.add(c["crm"])
        orig = B["by_acct"].get(c.get("returning_of")) if c.get("returning_of") else None
        first_c = orig if orig else c
        created = first_c["trial0"] - dt.timedelta(days=int(rc.integers(0, 21)))
        region = K.region_of_state(c["state"], created)
        active = c["cancel"] is None or c["cancel"] > K.DATA_END or bool(c.get("react"))
        crm.append([c["crm"], c["name"], "", c["state"], region, "Customer" if active else "Former Customer", first_c["lead"],
                    created.isoformat(), c.get("reg_acct") or first_c.get("reg_acct") or "", first_c.get("legacy_code") or c.get("legacy_code") or "", c["ws"]])
        for d in c["divisions"]:
            if d["first_inv"] > K.DATA_END:
                continue
            dcreated = d["first_inv"] - dt.timedelta(days=int(rc.integers(3, 20)))
            dactive = d["cancel"] is None or d["cancel"] > K.DATA_END
            crm.append([d["crm"], d["name"], c["crm"], c["state"], K.region_of_state(c["state"], dcreated),
                        "Customer" if dactive else "Former Customer", "Expansion", dcreated.isoformat(), d.get("reg_acct") or "",
                        d.get("legacy_code") or "", c["ws"]])
    for p_ in B["partners"]:
        crm.append([p_["crm"], p_["name"], "", p_["state"], K.region_of_state(p_["state"], p_["created"]), "Partner", "",
                    p_["created"].isoformat(), "", "", ""])
    crm.sort(key=lambda r: (r[7], r[0]))
    n[F_CRM] = K.write_csv(os.path.join(out, F_CRM),
        ["Account ID", "Account Name", "Parent Account ID", "Billing State", "Sales Region", "Type", "Lead Source", "Created Date",
         "Billing Account Number", "Legacy Customer Code", "Product Workspace ID"], crm)
    # ---------------------------------------------------------------- product user directory
    ru = K.rng(19)
    drows = []
    cut = dt.datetime(2026, 9, 30, 23, 59, 59)
    for u in W["users"]:
        c = B["by_acct"][u["acct"]]
        if u["created_at"] > cut:
            continue
        deact = u["deact_at"] if (u["deact_at"] is not None and u["deact_at"] <= cut) else None
        la = u["last_active"] if (deact is None or u["last_active"] < deact) else deact - dt.timedelta(hours=3)
        founder = u["uid"] == W["accounts"][u["acct"] - 1]["founder_uid"]
        drows.append([u["created_at"], c["ws"], u["name"], u["email"], u["phone"], u["title"],
                      "Admin" if founder or ru.random() < 0.06 else "Member", la, deact, u["reason_txt"] if deact else ""])
    for x in B["react_users"]:
        if x["created_at"] > cut:
            continue
        c = B["by_acct"][x["acct"]]
        drows.append([x["created_at"], c["ws"], x["name"], x["email"], x["phone"], x["title"], "Admin" if x["admin"] else "Member",
                      x["last_active"], None, ""])
    for x in B["trial_users"]:
        drows.append([x["created_at"], x["ws"], x["name"], x["email"], x["phone"], x["title"], "Admin" if x["admin"] else "Member",
                      x["last_active"], None, ""])
    drows.sort(key=lambda r: (r[0], r[1], r[3]))
    fmt = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ") if d else ""
    out_rows = []
    for i, r in enumerate(drows):
        out_rows.append(["u%07d" % (1100000 + i * 3 + (K.skey(r[3]) % 3)), r[1], r[2], r[3], r[4], r[5], r[6], fmt(r[0]), fmt(r[7]),
                         fmt(r[8]), r[9]])
    n[F_DIR] = K.write_csv(os.path.join(out, F_DIR),
        ["user_id", "workspace_id", "full_name", "email", "mobile", "job_title", "workspace_role", "created_at", "last_active_at",
         "deactivated_at", "deactivation_reason"], out_rows)
    # ---------------------------------------------------------------- marketing spend
    _spend(out, W)
    n[F_SPEND] = None
    return n


def _spend(out, W):
    import openpyxl
    rs = K.rng(20)
    ts, spend = W["ts"], W["spend"]
    CH = [("Paid search", 0.38), ("Paid social", 0.17), ("Events and trade shows", 0.21), ("Associations and partners", 0.12),
          ("Content and webinars", 0.12)]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Actuals"
    ws.append(["Fiscal Year", "Period", "Month", "Sales Region", "Channel", "Spend ($K)"])
    for i, t in enumerate(ts):
        if t < 1 or t > K.T_OBS:
            continue
        fy, p = K.fiscal_label(int(t))
        y, m = K.ym(int(t))
        for r in range(6):
            tot = float(spend[r, i])
            w = np.array([c[1] for c in CH]) * np.exp(rs.normal(0, 0.12, len(CH)))
            parts = np.round(tot * w / w.sum(), 1)
            parts[-1] = round(tot - parts[:-1].sum(), 1)
            for (ch, _), v in zip(CH, parts):
                ws.append(["FY%d" % fy, "P%02d" % p, "%d-%02d" % (y, m), K.REGIONS[r], ch, float(v)])
    ws.freeze_panes = "A2"
    for col, wdt in zip("ABCDEF", [11, 8, 9, 14, 26, 11]):
        ws.column_dimensions[col].width = wdt
    ws2 = wb.create_sheet("Plan Oct-2026 to Jan-2028")
    ws2.append(["Fiscal Year", "Period", "Month", "Sales Region", "Planned Spend ($K)"])
    for i, t in enumerate(ts):
        if t <= K.T_OBS or t > 108:
            continue
        fy, p = K.fiscal_label(int(t))
        y, m = K.ym(int(t))
        for r in range(6):
            ws2.append(["FY%d" % fy, "P%02d" % p, "%d-%02d" % (y, m), K.REGIONS[r], float(spend[r, i])])
    ws2.freeze_panes = "A2"
    for col, wdt in zip("ABCDE", [11, 8, 9, 14, 18]):
        ws2.column_dimensions[col].width = wdt
    wb.save(os.path.join(out, F_SPEND))
