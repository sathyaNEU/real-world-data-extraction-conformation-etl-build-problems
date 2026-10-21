"""task177 world: Daily Lantern Media's monthly digital subscriptions.

Last year's test: the 31 January 2026 at-risk list, half sent the half-price offer, half held back, every subscription
billed by the legacy billing system on its own day of the month. A subscriber weighs whether to keep paying as each bill
comes up; an offer that lands in the fortnight before the next bill catches them deciding (they accept it and stay),
one that lands earlier is mostly forgotten by then. This year's list (26 January 2027) is billed by the subscriptions
platform on the 1st, so every bill falls six days after the send.

Everything here is the clean truth the pack is cut from; calc.py reads only the pack."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as C

P = dict(
    n_ly=160000,          # last year's list
    n_ty=48000,           # this year's list
    a=0.75,               # risk intercept (per-bill intention to leave, logit)
    r_high=0.82,          # share of would-be leavers the offer keeps when it lands in the fortnight before the bill
    r_low=0.02,           # ... when it lands earlier
    mid=14.5, width=0.5,  # where the fortnight ends (days before the bill)
    q_sure=0.10,          # subscribers deciding to stay who take the discount anyway, in the fortnight
    r2=0.75,              # at the second (still half-price) bill, share of accepters' would-be leavers kept
    f_call=0.10,          # would-be leavers who phone the save desk instead of cancelling online
    s_desk=0.30,          # callers the save desk keeps with its own half-price (same billing code)
    later=0.50,           # later bills' intention as a share of the at-risk intention
    restart=0.025,        # leavers who restart within four weeks
    open_rate=0.30,       # offer emails opened
    app_accept=0.34,      # accepters who accept in the app (its own discount code and customer key)
    app_fallback=0.15,    # app acceptances the offers engine did not apply; the app put the subscription on a half-price
                          # rate for its next two bills instead of a discount line
    household=0.40,       # second subscriptions on the list subscription's plan, billed on its account
    together=0.65,        # ... of which set up the same day as the list subscription (same billing day)
    both_channels=0.06,   # app accepters who also accept from the email (a second acceptance, another key)
    moved_day=0.10,       # subscriptions whose bill day moved from their start day (a recovered failed payment)
    addon=0.13,           # this year's accounts that also hold the Puzzles add-on
    overlap=0.12,         # this year's list members who were on last year's list
    loyalty=0.02,         # bills carrying a goodwill credit
    second_sub=0.05,      # this year's accounts that also pay for a second plan subscription (not on the list)
    paid_by_other=0.035,  # this year's list subscriptions paid from another subscriber's account
)

REGIONS = ("London", "South East", "Midlands", "North West", "North East and Yorkshire", "Scotland",
           "Wales and South West")
REGION_P = (0.19, 0.17, 0.15, 0.13, 0.13, 0.11, 0.12)
DEVICES = ("web", "ios", "android", "mixed")
PAY = ("card", "direct debit", "paypal")


def r_of_d(d):
    return P["r_low"] + (P["r_high"] - P["r_low"]) / (1.0 + np.exp((np.asarray(d, float) - P["mid"]) / P["width"]))


def people(n, rng, asof, start_lo, start_hi):
    span = (start_hi - start_lo).days
    start = np.array([start_lo + dt.timedelta(int(x)) for x in rng.integers(0, span, n)])
    plan = rng.choice(np.array(C.PLANS), n, p=[0.55, 0.30, 0.15])
    region = rng.choice(np.array(REGIONS), n, p=REGION_P)
    device = rng.choice(np.array(DEVICES), n, p=[0.36, 0.26, 0.20, 0.18])
    arts = rng.poisson(np.exp(rng.normal(2.0, 0.9, n)))
    news = rng.binomial(4, 0.35, n)
    supp = rng.poisson(0.32, n)
    pay = rng.choice(np.array(PAY), n, p=[0.62, 0.30, 0.08])
    ten = np.array([(asof - s).days / 30.44 for s in start])
    z = (P["a"] - 0.30 * np.log(ten) - 0.20 * np.log1p(arts) + 0.30 * supp - 0.08 * news
         + pd.Series(plan).map({"Digital": 0.10, "Digital Plus": 0.0, "Family": -0.25}).values
         + pd.Series(device).map({"web": 0.0, "ios": 0.05, "android": 0.08, "mixed": -0.05}).values
         + rng.normal(0, 0.35, n))
    p = 1 / (1 + np.exp(-z))
    resp = np.clip(1.2 - 0.010 * ten, 0.7, 1.2)
    dom = np.array([s.day for s in start])
    moved = rng.random(n) < P["moved_day"]
    dom = np.where(moved, rng.integers(1, 29, n), dom)
    score = np.clip(p + rng.normal(0, 0.06, n), 0.20, 0.97)
    band = np.where(score >= 0.55, "A", np.where(score >= 0.40, "B", "C"))
    return pd.DataFrame(dict(start=start, plan=plan, region=region, device=device, arts=arts, news=news, supp=supp,
                             pay=pay, ten=ten, p=p, resp=resp, dom=dom, moved=moved, score=np.round(score, 3),
                             band=band))


def ids(rng, n, prefix, width, lo, span=None):
    span = span or 20 * n
    assert lo + span < 10 ** width
    v = rng.choice(np.arange(lo, lo + span), n, replace=False)
    return np.array(["%s%0*d" % (prefix, width, x) for x in v])


# --------------------------------------------------------------------------------------------- last year's test
def last_year():
    rng = C.stream("ly")
    ly = people(P["n_ly"], rng, C.LY_LIST, dt.date(2018, 1, 1), dt.date(2025, 11, 30))
    ly["lbs"] = ids(rng, len(ly), "L", 7, 1200000)
    ly["crm"] = ids(rng, len(ly), "C", 7, 3400000)
    ly["app_user"] = np.where(np.isin(ly.device, ["ios", "android", "mixed"]) & (rng.random(len(ly)) < 0.8),
                              ids(rng, len(ly), "U", 8, 50000000), "")
    ly["T"] = (rng.random(len(ly)) < 0.5).astype(int)
    b1 = [C.next_bill_after(k, C.LY_LIST) for k in ly.dom]
    ly["b1"] = b1
    ly["d"] = np.array([(b - C.LY_LIST).days for b in b1], float)
    # the bills from December 2025 to January 2027 on each subscription's day
    bills = []
    for k in ly.dom.values:
        row = []
        y, m = 2025, 12
        for i in range(10):                    # the legacy system's bills to September 2026
            row.append(C.month_day(y, m, k))
            y, m = C.add_months(dt.date(y, m, 1), 1)
        row += [dt.date(2026, 10, 1), dt.date(2026, 11, 1), dt.date(2026, 12, 1), dt.date(2027, 1, 1)]
        bills.append(row)
    ly["bills"] = bills   # index 0 December 2025, 1 January 2026, 2 February (= b1), 3 March (= b2) ...
    n = len(ly)
    p = ly.p.values; T = ly["T"].values; d = ly.d.values; resp = ly.resp.values
    r1 = np.clip(r_of_d(d) * resp, 0, 0.95)
    mode = d <= 14
    alive = np.ones(n, bool)
    end_bill = np.full(n, -1)                 # index of the bill they did not pay (access ends the day before)
    accepted = np.zeros(n, bool)
    disc_bills = [set() for _ in range(n)]    # bill indexes carrying the offer's half price
    desk_bills = [set() for _ in range(n)]    # bill indexes carrying the save desk's half price
    acc_day = np.array([None] * n, dtype=object)
    restart_day = np.array([None] * n, dtype=object)
    rr = C.stream("ly_decisions")
    for j in range(2, 14):                    # decisions at February 2026 ... January 2027 bills
        pj = p if j <= 3 else p * P["later"]
        c = (rr.random(n) < pj) & alive
        if j == 2:
            c2 = c.copy()
            pers = (T == 1) & c & (rr.random(n) < r1)
            sure = (T == 1) & ~c & alive & mode & (rr.random(n) < P["q_sure"] * resp)
            accepted = pers | sure
            for i in np.where(accepted)[0]:
                disc_bills[i].update((2, 3))
            stay = pers
        elif j == 3:
            c3 = c.copy()
            stay = accepted & c & (rr.random(n) < P["r2"])
        else:
            stay = np.zeros(n, bool)
        # the save desk keeps some callers with its own half price; an accepter already on half price at the
        # second bill is not offered it again
        call = c & ~stay & ~(accepted & (j == 3)) & (rr.random(n) < P["f_call"]) & (rr.random(n) < P["s_desk"])
        for i in np.where(call)[0]:
            desk_bills[i].update((j, j + 1))
        leave = c & ~stay & ~call
        end_bill = np.where(leave & (end_bill < 0), j, end_bill)
        alive = alive & ~leave
    # re-centre last January's graded discount cells inside their hundreds: acceptance moves only for subscribers in
    # the offer arm who were deciding at neither bill (they pay both bills either way), so nothing the call reads moves
    acc0 = accepted.copy()
    rc = C.stream("ly_recentre")
    plan_v = ly.plan.values
    pays_mar = (end_bill < 0) | (end_bill >= 4)
    ly_shift = {}
    for pl in C.PLANS:
        dpl = int(round(int(round(C.PRICE[pl] * 100)) * C.OFFER_SHARE)) / 100.0
        sel = plan_v == pl
        feb, mar = dpl * (accepted & sel).sum(), dpl * (accepted & sel & pays_mar).sum()
        ks = sorted(range(-25, 26), key=lambda k: (abs(k), k))
        good = [k for k in ks if min(C.edge(feb + k * dpl, 100), C.edge(mar + k * dpl, 100)) >= 30]
        k = good[0] if good else max(ks, key=lambda k: min(C.edge(feb + k * dpl, 100), C.edge(mar + k * dpl, 100)))
        if k < 0:
            pool = np.where(sel & accepted & ~pers & ~c3)[0]
            for i in rc.choice(pool, -k, replace=False):
                accepted[i] = False
                disc_bills[i] = set()
        elif k > 0:
            pool = np.where(sel & (T == 1) & mode & ~c2 & ~c3 & ~accepted)[0]
            for i in rc.choice(pool, k, replace=False):
                accepted[i] = True
                disc_bills[i].update((2, 3))
        ly_shift[pl] = k
    ly.attrs["recentre"] = ly_shift
    ly["accepted"] = accepted
    ly["end_bill"] = end_bill
    # acceptance times: in the days before the first bill, never before the send
    for i in np.where(acc0)[0]:
        b = ly.bills.iat[i][2]
        lag = int(rr.integers(1, int(min(7, d[i])) + 1)) if d[i] >= 1 else 0
        if accepted[i]:
            acc_day[i] = max(b - dt.timedelta(lag), C.LY_LIST)
    for i in np.where(accepted & ~acc0)[0]:
        b = ly.bills.iat[i][2]
        lag = int(rc.integers(1, int(min(7, d[i])) + 1)) if d[i] >= 1 else 0
        acc_day[i] = max(b - dt.timedelta(lag), C.LY_LIST)
    ly["acc_day"] = acc_day
    # restarts: a few leavers come back within four weeks, under the same subscription
    for i in np.where(end_bill >= 0)[0]:
        if rr.random() < P["restart"]:
            b = ly.bills.iat[i][end_bill[i]]
            restart_day[i] = b + dt.timedelta(int(rr.integers(3, 28)))
    ly["restart_day"] = restart_day
    ly["disc_bills"] = disc_bills
    ly["desk_bills"] = desk_bills
    ly["channel"] = np.where(accepted & (ly.app_user != "") & (rr.random(n) < P["app_accept"] / 0.6), "app",
                             np.where(accepted, rr.choice(np.array(["email", "web"]), n, p=[0.7, 0.3]), ""))
    ly["also_email"] = (ly.channel == "app") & (rr.random(n) < P["both_channels"])
    ly["opened"] = (T == 1) & (rr.random(n) < P["open_rate"])
    ly["loyal_bill"] = np.where(rr.random(n) < P["loyalty"] * 5, rr.integers(1, 6, n), -1)
    ly["subscribed_h"] = ~((end_bill == 2) | (end_bill == 3)) | np.array(
        [rd is not None and rd <= C.LY_HORIZON for rd in restart_day])
    return ly


def true_uplift(df):
    """expected kept share at the two bills after the send, offer against none, for each subscription"""
    p = df.p.values
    r1 = np.clip(r_of_d(df.d.values) * df.resp.values, 0, 0.95)
    q = np.where(df.d.values <= 14, P["q_sure"] * df.resp.values, 0.0)
    fs = P["f_call"] * P["s_desk"]
    acc = p * r1 + (1 - p) * q
    stay1_noacc = (1 - p) * (1 - q) + p * (1 - r1) * fs
    treated = acc * (1 - p * (1 - P["r2"]) * (1 - fs)) + stay1_noacc * (1 - p * (1 - fs))
    control = (1 - p * (1 - fs)) ** 2
    return treated - control


# ------------------------------------------------------------------------------------------------ this year's list
def this_year(ly):
    rng = C.stream("ty")
    n = P["n_ty"]
    n_over = int(round(n * P["overlap"]))
    # last year's members still subscribed in January 2027 and still on the at-risk list
    alive = ly[(ly.end_bill < 0)].copy()
    pick = rng.choice(alive.index.values, n_over, replace=False)
    over = alive.loc[pick]
    fresh = people(n - n_over, rng, C.TY_LIST, dt.date(2019, 1, 1), dt.date(2026, 11, 30))
    fresh["lbs"] = ids(rng, len(fresh), "L", 7, 4500000)
    fresh["crm"] = ids(rng, len(fresh), "C", 7, 7000000)
    keep = ["start", "plan", "region", "device", "arts", "news", "supp", "pay", "ten", "p", "resp", "dom", "moved",
            "score", "band", "lbs", "crm"]
    o = over[keep].copy()
    # a year on: their tenure and reading moved, their risk is this year's
    o["ten"] = o["ten"] + 12.0
    ro = C.stream("ty_overlap")
    o["arts"] = ro.poisson(np.exp(ro.normal(2.0, 0.9, len(o))))
    z = np.log(o.p / (1 - o.p)) - 0.30 * np.log(o.ten / (o.ten - 12.0)) + ro.normal(0, 0.15, len(o))
    o["p"] = 1 / (1 + np.exp(-z))
    o["score"] = np.round(np.clip(o.p + ro.normal(0, 0.06, len(o)), 0.20, 0.97), 3)
    o["band"] = np.where(o.score >= 0.55, "A", np.where(o.score >= 0.40, "B", "C"))
    o["from_ly"] = True
    fresh["from_ly"] = False
    ty = pd.concat([o, fresh[keep + ["from_ly"]]], ignore_index=True)
    ty = ty.iloc[rng.permutation(len(ty))].reset_index(drop=True)
    ty["sp_sub"] = ids(rng, len(ty), "S", 9, 400000000)
    ty["sp_acct"] = ids(rng, len(ty), "A", 8, 61000000)
    ty["d"] = 6.0
    ty["has_addon"] = rng.random(len(ty)) < P["addon"]
    ty["addon_lbs"] = np.where(ty.has_addon, ids(rng, len(ty), "L", 7, 5400000), "")
    ty["addon_sp"] = np.where(ty.has_addon, ids(rng, len(ty), "S", 9, 700000000), "")
    ty["addon_dom"] = np.where(ty.has_addon, rng.integers(1, 29, len(ty)), 0)
    ty["batch"] = np.array(["MIG-%02d" % x for x in rng.integers(1, 13, len(ty))])
    # the legacy system's 1 October run still held some batches of day-1 subscriptions
    held = set(rng.choice(["MIG-%02d" % x for x in range(1, 13)], 7, replace=False))
    legacy = np.array([x < C.MOVE for x in ty.start])           # joined before the platform took over billing
    ty["legacy"] = legacy
    ty["dup_news"] = legacy & (ty.dom == 1) & ty.batch.isin(held)
    ty["dup_addon"] = legacy & ty.has_addon & (ty.addon_dom == 1) & ty.batch.isin(held)
    ty["loyal_month"] = np.where(rng.random(len(ty)) < P["loyalty"] * 4, rng.integers(0, 4, len(ty)), -1)
    # accounts: a list subscription is usually its account's only plan; some accounts also pay for a second plan
    # subscription (a partner's, a student's) that is not on the list, and some list subscriptions are paid from
    # another subscriber's account, whose own subscription is not on the list
    ra = C.stream("ty_accounts")
    m = len(ty)
    other = ra.random(m) < P["paid_by_other"]
    second = (ra.random(m) < P["second_sub"]) & ~other
    ty["paid_by_other"] = other
    ty["second"] = second
    ty.loc[other, "has_addon"] = False
    ty.loc[other, "addon_lbs"] = ""
    ty.loc[other, "addon_sp"] = ""
    ty.loc[other, "addon_dom"] = 0
    ty["dup_addon"] = ty.legacy & ty.has_addon & (ty.addon_dom == 1) & ty.batch.isin(held)
    k = int((other | second).sum())
    ex = pd.DataFrame(dict(owner=np.where(other | second)[0]))
    ex["kind"] = np.where(other[ex.owner.values], "payer", "second")
    # an account holder paying for someone else's subscription was a subscriber before the move
    span = np.where(ex.kind == "payer", (dt.date(2026, 9, 30) - dt.date(2018, 6, 1)).days,
                    (dt.date(2026, 11, 30) - dt.date(2018, 6, 1)).days)
    ex["start"] = [dt.date(2018, 6, 1) + dt.timedelta(int(x)) for x in (ra.random(k) * span).astype(int)]
    ex["plan"] = ra.choice(np.array(C.PLANS), k, p=[0.62, 0.26, 0.12])
    dom = np.array([s.day for s in ex.start])
    ex["dom"] = np.where(ra.random(k) < P["moved_day"], ra.integers(1, 29, k), dom)
    ex["sp_sub"] = ids(ra, k, "S", 9, 430000000)
    ex["legacy"] = np.array([s < C.MOVE for s in ex.start])
    lbs_all = ids(ra, k, "L", 7, 7000000)
    ex["lbs"] = np.where(ex.legacy, lbs_all, "")
    ex["batch"] = ty.batch.values[ex.owner.values]
    ex["dup"] = ex.legacy & (ex.dom == 1) & ex.batch.isin(held)
    payer_acct = ids(ra, k, "A", 8, 69000000)
    ex["sp_acct"] = np.where(ex.kind == "payer", payer_acct, ty.sp_acct.values[ex.owner.values])
    # households: a second subscription set up with the list subscription takes its plan, its start and its billing
    # day, so the two are billed together; a payer's own subscription is on another plan than the one it pays for
    rh = C.stream("ty_household")
    own = ex.owner.values
    hh = (ex.kind.values == "second") & (rh.random(k) < P["household"])
    ex["household"] = hh
    ex.loc[hh, "plan"] = ty.plan.values[own[hh]]
    tog = hh & legacy[own] & (C.stream("ty_household_together").random(k) < P["together"])
    ex["together"] = tog
    ex.loc[tog, "start"] = pd.Series(ty.start.values[own[tog]], index=ex.index[tog])
    ex.loc[tog, "dom"] = ty.dom.values[own[tog]]
    same = (ex.kind.values == "payer") & (ex.plan.values == ty.plan.values[own])
    alt = rh.random(k)
    for j in np.where(same)[0]:
        others = [p for p in C.PLANS if p != ty.plan.iat[own[j]]]
        ex.iat[j, ex.columns.get_loc("plan")] = others[int(alt[j] * 2)]
    ex["legacy"] = np.array([s < C.MOVE for s in ex.start])
    ex["lbs"] = np.where(ex.legacy, lbs_all, "")
    ex["dup"] = ex.legacy & (ex.dom == 1) & ex.batch.isin(held)
    # a list subscription paid from another account carries that account's id
    pay_rows = ex[ex.kind == "payer"]
    ty.loc[pay_rows.owner.values, "sp_acct"] = pay_rows.sp_acct.values
    return ty, held, ex
