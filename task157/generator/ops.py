"""The operating layer, built from the world with its own streams: each account's first trip, legacy driver number
and new driver id, the migration crosswalk and its merged registrations; the accounts register; the guarantee's
payments for 2025 and 2026 (main runs, later runs, bank returns, each payout's events, merged two-account drivers);
the onboarding tool's applications from its go-live and the screening vendor's orders; the referral programme's 2026
bonuses; and the activity extract's monthly cells (completed trips, driver cancellations, online time, and the
months a driver went online without completing a trip)."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as WD

TOOL_LIVE = dt.date(2025, 6, 2)          # the onboarding tool's first day; earlier applications are not in it
APPROVAL_LAPSE_DAYS = 90
HOME = [("Minneapolis", 0.44), ("Saint Paul", 0.22), ("Bloomington", 0.06), ("Brooklyn Park", 0.05),
        ("Eagan", 0.04), ("Maple Grove", 0.04), ("Burnsville", 0.035), ("Plymouth", 0.035), ("Roseville", 0.03),
        ("Coon Rapids", 0.03), ("Richfield", 0.025), ("Woodbury", 0.025)]
RETURN_CODES = [("R02", "Account closed", 0.41), ("R03", "No account/unable to locate account", 0.33),
                ("R04", "Invalid account number structure", 0.19), ("R20", "Non-transaction account", 0.07)]
P_RETURN = 0.031
P_RESEND = 0.63
P_RETURN_AGAIN = 0.08
P_RESUBMIT = 0.22                        # applications sent back for a document and resubmitted
FED_HOLIDAYS = {dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26),
                dt.date(2025, 6, 19), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 10, 13),
                dt.date(2025, 11, 11), dt.date(2025, 11, 27), dt.date(2025, 12, 25), dt.date(2026, 1, 1),
                dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25), dt.date(2026, 6, 19),
                dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2026, 11, 11),
                dt.date(2026, 11, 26), dt.date(2026, 12, 25)}
ADJ_RUNS = {2025: [dt.date(2025, 3, 7), dt.date(2025, 4, 11)],
            2026: [dt.date(2026, 3, 6), dt.date(2026, 4, 10), dt.date(2026, 6, 12)]}
LATE_2025_RECOVERY = 1                   # a 2025 recovery found in the 2025 audit and booked in the March 2026 run


class Ops:
    pass


class Pay:
    pass


def bday(d, k=1):
    """k banking days after d (weekends and Federal Reserve holidays skipped)."""
    while k > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in FED_HOLIDAYS:
            k -= 1
    return d


def _pick(r, table):
    p = np.array([t[-1] for t in table], dtype=float)
    return table[int(r.choice(len(table), p=p / p.sum()))]


def _office(d, r, back=False):
    """A decision by the onboarding team: a working day (Monday to Saturday), 8:30 to 18:30 Central; a Sunday's
    decision is taken on the Monday (or, for an approval dated back from a first trip, on the Saturday)."""
    while d.weekday() == 6:
        d += dt.timedelta(days=-1 if back else 1)
    return dt.datetime.combine(d, dt.time(8, 30)) + dt.timedelta(minutes=int(r.integers(0, 600)))


def _local(d, r, lo=6.0, hi=23.0):
    h = float(r.uniform(lo, hi))
    return dt.datetime.combine(d, dt.time(0)) + dt.timedelta(hours=h)


# ------------------------------------------------------------------------------------------------- first trips
def first_trips(W, ml, M, O):
    """The day and time of each account's first completed trip, inside the first week with a trip and inside the
    calendar month the extract puts that week's first trips in."""
    midx = {m: j for j, m in enumerate(ml)}
    first_m = (M > 0).argmax(1)
    O.first_trip = []
    for k in range(W.n):
        r = K.rng("first", k)
        d0 = K.wdate(W.first_week[k])
        days = [d0 + dt.timedelta(days=j) for j in range(7)]
        mon = ml[int(first_m[k])]
        cand = [j for j in range(7) if K.ym(days[j]) == mon]
        if not cand:
            cand = list(range(7))
        p = WD.WEEKDAY_W[cand] / WD.WEEKDAY_W[cand].sum()
        j = cand[int(r.choice(len(cand), p=p))]
        O.first_trip.append(_local(days[j], r, 6.5, 22.5))
    O.last_week = np.array([int(np.nonzero(W.has[k])[0][-1]) for k in range(W.n)])


# ------------------------------------------------------------------------------------------------- onboarding
def onboarding(W, O):
    """Applications through the onboarding tool from its go-live: every account whose first trip came after it (the
    rental programme's drivers were onboarded by the partner in early 2025), the approved applicants who never took a
    trip, the rejected and the withdrawn, and the screening vendor's order at each application's first submission."""
    apps = []                            # dicts; 'k' is the world account for started drivers, None otherwise
    r0 = K.rng("onb", "started")
    for k in range(W.n):
        ft = O.first_trip[k]
        if W.src[k] == "rental":
            continue
        r = K.rng("onb", k)
        start_lag = dt.timedelta(days=int(r.geometric(0.28)) - 1, hours=float(r.uniform(-6, 6)))
        day = (ft - start_lag - dt.timedelta(hours=float(r.uniform(2, 20)))).date()
        approved = _office(day, r, back=True)
        if approved >= ft - dt.timedelta(minutes=40):
            approved = _office(day - dt.timedelta(days=1), r, back=True)
        resub = r.random() < P_RESUBMIT
        review = dt.timedelta(days=int(r.integers(1, 6)), hours=float(r.uniform(1, 30)))
        if resub:
            req = dt.timedelta(days=int(r.integers(1, 4)), hours=float(r.uniform(0, 8)))
            doc = dt.timedelta(days=int(r.geometric(0.13)) + 1, hours=float(r.uniform(0, 12)))
            post = dt.timedelta(days=int(r.integers(1, 4)), hours=float(r.uniform(1, 20)))
            resubmitted = approved - post
            first_sub = resubmitted - doc - req
        else:
            resubmitted = None
            first_sub = approved - review
        if first_sub.date() < TOOL_LIVE:
            continue
        a = dict(k=k, first_sub=first_sub, resubmitted=resubmitted, decision=approved, outcome="approved",
                 first_trip=ft, vehicle="own" if W.src[k] != "campaign" or r.random() < 0.9 else "lease")
        if r.random() < 0.05:
            # applied before and was turned down: a second application under the same screening candidate
            gap = dt.timedelta(days=int(r.integers(35, 160)), hours=float(r.uniform(0, 20)))
            if (first_sub - gap).date() >= TOOL_LIVE:
                a["prior"] = first_sub - gap
        apps.append(a)
    # the approved who never took a trip, the rejected, the withdrawn and the expired: in proportion to each week's
    # approvals of drivers who went on to drive
    wk = {}
    for a in apps:
        w = K.widx(a["decision"].date())
        wk[w] = wk.get(w, 0) + 1
    lo, hi = K.widx(TOOL_LIVE), K.widx(K.AS_OF)
    for w in range(lo, hi + 1):
        base = wk.get(w, 0)
        r = K.rng("onb", "week", w)
        d0 = K.wdate(w)
        for outcome, rate in (("never_started", 0.17), ("rejected", 0.21), ("withdrawn", 0.13), ("expired", 0.10)):
            for _ in range(int(r.poisson(rate * max(base, 25)))):
                day = d0 + dt.timedelta(days=int(r.integers(0, 7)))
                first_sub = _local(day, r, 5.0, 23.9)
                resub = outcome in ("never_started", "rejected") and r.random() < P_RESUBMIT
                resubmitted = None
                if resub:
                    resubmitted = first_sub + dt.timedelta(days=int(r.integers(1, 4)) + int(r.geometric(0.13)) + 1,
                                                           hours=float(r.uniform(0, 12)))
                last = resubmitted or first_sub
                if outcome == "never_started":
                    decision = _office((last + dt.timedelta(days=int(r.integers(1, 6)))).date(), r)
                    oc = "approved"
                elif outcome == "rejected":
                    decision = _office((last + dt.timedelta(days=int(r.integers(3, 12)))).date(), r)
                    oc = "rejected"
                elif outcome == "withdrawn":
                    decision = first_sub + dt.timedelta(days=int(r.integers(1, 20)), hours=float(r.uniform(0, 20)))
                    oc = "withdrawn"
                else:
                    decision = dt.datetime.combine(first_sub.date() + dt.timedelta(days=30), dt.time(3, 10)) + \
                        dt.timedelta(seconds=int(r.integers(0, 240)))
                    oc = "expired"
                if decision.date() > K.AS_OF:
                    oc, decision = "in_review", None
                apps.append(dict(k=None, first_sub=first_sub, resubmitted=resubmitted, decision=decision, outcome=oc,
                                 first_trip=None, vehicle="own" if r.random() < 0.93 else "lease"))
    # application ids in order of first submission; screening candidates per person
    apps.sort(key=lambda a: (a["first_sub"], -1 if a["k"] is None else a["k"]))
    out, orders = [], []
    seq = 0
    for a in apps:
        items = []
        if "prior" in a:
            items.append(dict(a, first_sub=a["prior"], resubmitted=None, outcome="rejected",
                              decision=_office((a["prior"] + dt.timedelta(
                                  days=int(K.rng("onb", "prior", a["k"]).integers(4, 12)))).date(),
                                  K.rng("onb", "prior_t", a["k"])),
                              first_trip=None, k_person=a["k"], k=None, is_prior=True))
        items.append(a)
        cand = "C" + K.token("cand", a["k"] if a["k"] is not None else seq, a["first_sub"].isoformat(), n=9,
                             alphabet=K.B32)
        for it in items:
            seq += 1
            it["app_id"] = "APP-%s" % K.token("app", seq, it["first_sub"].isoformat(), n=8, alphabet=K.B32)
            it["candidate"] = cand
            rr = K.rng("order", seq)
            it["ordered"] = it["first_sub"] + dt.timedelta(seconds=int(rr.integers(25, 240)))
            done = it["ordered"] + dt.timedelta(days=int(rr.integers(1, 5)), hours=float(rr.uniform(0, 20)))
            res = "consider" if it["outcome"] == "rejected" and rr.random() < 0.7 else "clear"
            if it["outcome"] in ("withdrawn", "expired") and rr.random() < 0.35:
                res, done = "canceled", None
            if done is not None and done.date() > K.AS_OF:
                res, done = "pending", None
            it["check_result"], it["check_done"] = res, done
            it["order_id"] = "ORD-%s" % K.token("ordid", seq, n=10, alphabet="0123456789")
            out.append(it)
    O.apps = out
    # approvals lapse after 90 days without a first trip
    for it in O.apps:
        if it["outcome"] == "approved" and it["first_trip"] is None:
            if (K.AS_OF - it["decision"].date()).days > APPROVAL_LAPSE_DAYS:
                it["outcome"] = "approval_lapsed"
                it["lapsed_on"] = it["decision"].date() + dt.timedelta(days=APPROVAL_LAPSE_DAYS)
    for it in O.apps:
        if it["first_trip"] is not None and it["first_trip"].date() > K.AS_OF:
            it["first_trip_seen"] = None
        else:
            it["first_trip_seen"] = it["first_trip"]


# ------------------------------------------------------------------------------------------------- accounts
def accounts(W, O):
    """Every account: the world's drivers, and the approved applicants who never took a trip (an account is opened at
    approval). Legacy driver numbers for registrations on the old dispatch platform, the crosswalk to new ids, and the
    re-registrations merged at the migration."""
    n_extra = [a for a in O.apps if a["k"] is None and a["outcome"] in ("approved", "approval_lapsed")
               and not a.get("is_prior")]
    O.n_acc = W.n + len(n_extra)
    O.extra_app = n_extra
    created = []
    app_of = {a["k"]: a for a in O.apps if a["k"] is not None}
    for k in range(W.n):
        if k in app_of:
            created.append(app_of[k]["decision"])
        else:
            r = K.rng("created", k)
            created.append(O.first_trip[k] - dt.timedelta(days=int(r.integers(2, 22)), hours=float(r.uniform(0, 9))))
    for a in n_extra:
        created.append(a["decision"])
    O.created = created
    ids, seen = [], set()
    for k in range(O.n_acc):
        j = 0
        while True:
            t = K.token("driver", k, j, n=8, alphabet=K.B32)
            if t not in seen:
                break
            j += 1
        seen.add(t)
        ids.append(t)
    O.driver_id = ids
    for i, a in enumerate(n_extra):
        a["acc"] = W.n + i
    for a in O.apps:
        if a["k"] is not None:
            a["acc"] = a["k"]
    # signup channel, home, vehicle
    O.channel, O.home, O.vehicle = [], [], []
    for k in range(O.n_acc):
        r = K.rng("acct", k)
        src = W.src[k] if k < W.n else "organic"
        if src == "campaign":
            ch = "campaign_winter26"
        elif src == "rental":
            ch = "rental_partner"
        else:
            yr = created[k].year
            ch = "referral" if r.random() < (0.12 if yr < 2023 else 0.24) else "app"
        O.channel.append(ch)
        O.home.append(_pick(r, HOME)[0])
        O.vehicle.append("rental" if src == "rental" else ("lease" if r.random() < 0.06 else "own"))
    # legacy registrations: every account opened before the migration, numbered in order of opening, with the numbers
    # of registrations that never completed a trip skipped
    pre = sorted([k for k in range(W.n) if created[k].date() < K.MIGRATION], key=lambda k: (created[k], k))
    O.legacy_no = {}
    no = 10117
    r = K.rng("legacy", "numbers")
    for k in pre:
        no += 1 + (int(r.geometric(0.55)) - 1 if r.random() < 0.22 else 0)
        O.legacy_no[k] = no
    # re-registrations: drivers who came back after a long break on the old platform under a second number
    O.legacy_second = {}
    mig_w = K.widx(K.MIGRATION)
    cands = []
    for k in pre:
        if W.kind[k] not in ("R", "I"):
            continue
        act = np.nonzero(W.has[k, :mig_w])[0]
        if len(act) < 6:
            continue
        gaps = np.diff(act)
        big = np.nonzero(gaps >= 14)[0]
        if len(big):
            cands.append((k, int(act[big[-1] + 1])))
    r = K.rng("legacy", "rereg")
    pick = sorted(r.choice(len(cands), size=min(38, len(cands)), replace=False))
    for j in pick:
        k, w2 = cands[int(j)]
        O.legacy_second[k] = (w2, None)
    nos = sorted(O.legacy_no.values())
    top = nos[-1]
    for k in sorted(O.legacy_second, key=lambda k: (O.legacy_second[k][0], k)):
        w2 = O.legacy_second[k][0]
        # the second number sits among the numbers issued around the second registration
        before = [O.legacy_no[x] for x in pre if created[x].date() <= K.wdate(w2)]
        base = max(before) if before else top
        n2 = base + 1
        while n2 in nos:
            n2 += 1
        nos.append(n2)
        nos.sort()
        O.legacy_second[k] = (w2, n2)


# ------------------------------------------------------------------------------------------------- payments
def payments(W, O):
    """The guarantee's payouts for 2025 and 2026: the main run pays every account the payments system counted at 40
    completed trips at its review cut; later runs pay the late credits and book recoveries (trips refunded as
    fraudulent, a second account of a driver already paid); the bank returns some payouts, most are sent again under
    the same payout id once the driver updates their payout details."""
    O.pay = {}
    O.eligible_qual = {}
    for y in K.GUARANTEE_YEARS:
        O.eligible_qual[y] = W.qual[y] & np.array([O.created[k] <= dt.datetime.combine(K.ELIGIBLE_BY[y], dt.time(23, 59, 59))
                                                   for k in range(W.n)])
    for y in (2025, 2026):
        P = Pay()
        T = W.wtrips[y]
        elig = np.array([O.created[k] <= dt.datetime.combine(K.ELIGIBLE_BY[y], dt.time(23, 59, 59))
                         for k in range(W.n)])
        Q = W.qual[y] & elig
        r = K.rng("pay", y)
        ws = K.widx(K.WINDOW[y][0])
        late_c = np.nonzero(Q & (T <= 41))[0]
        late = sorted(int(x) for x in r.choice(late_c, WD.LATE_CREDIT[y], replace=False))
        fr_c = np.nonzero(~W.qual[y] & elig & (T >= 36))[0]
        fraud = sorted(int(x) for x in r.choice(fr_c, WD.FRAUD[y], replace=False))
        main = sorted((set(int(x) for x in np.nonzero(Q)[0]) - set(late)) | set(fraud))
        # second accounts: opened shortly before the window, gone soon after, merged into the driver's first account
        last_w = O.last_week
        b_c = [int(x) for x in np.nonzero(Q)[0] if W.first_week[x] >= ws - 10 and last_w[x] <= ws + 10
               and int(x) not in late and int(x) not in fraud]
        a_c = [int(x) for x in np.nonzero(Q)[0] if W.first_week[x] < ws - 30 and last_w[x] > ws + 30
               and int(x) not in late and int(x) not in fraud]
        bs = sorted(int(x) for x in r.choice(b_c, WD.DUP_PERSONS[y], replace=False))
        as_ = [int(x) for x in r.choice(a_c, WD.DUP_PERSONS[y], replace=False)]
        dups = list(zip(as_, bs))
        P.year, P.late, P.fraud, P.main, P.dups = y, late, fraud, main, dups
        run = K.MAIN_RUN[y]
        P.payouts = {}
        def new_payout(k, date, kind):
            pid = "po_" + K.token("payout", y, kind, k, n=14, alphabet="0123456789abcdefghjkmnpqrstvwxyz")
            P.payouts[pid] = dict(k=k, date=date, kind=kind, amount=K.AMOUNT, events=[], year=y)
            return pid
        P.main_ids = {k: new_payout(k, run, "main") for k in main}
        P.late_ids = {k: new_payout(k, ADJ_RUNS[y][0], "late") for k in late}
        # recoveries
        P.recoveries = []
        for j, k in enumerate(fraud):
            when = ADJ_RUNS[y][1]
            if y == 2025 and j == len(fraud) - LATE_2025_RECOVERY:
                when = ADJ_RUNS[2026][0]
            P.recoveries.append(dict(k=k, date=when, reason="fraud_recovery", reverses=P.main_ids[k]))
        merge_on = {}
        for i, (a, b) in enumerate(dups):
            md = K.wdate(int(last_w[b])) + dt.timedelta(days=int(r.integers(14, 45)))
            merge_on[b] = (a, md)
            if y == 2026 and i == len(dups) - 1:
                # merged in December; its recovery has not been booked
                merge_on[b] = (a, dt.date(2026, 12, 9))
                continue
            when = next((d for d in ADJ_RUNS[y] if d > md), ADJ_RUNS[y][-1])
            pid = P.main_ids.get(b) or P.late_ids.get(b)
            P.recoveries.append(dict(k=b, date=when, reason="duplicate_account", reverses=pid))
        P.merge_on = merge_on
        reversed_ids = {x["reverses"] for x in P.recoveries}
        # the payments system's events: each run creates its payouts in sequence and submits them as one ACH batch;
        # the bank settles a batch the next banking day and its return file posts each morning; a driver who updates
        # their payout details is picked up by that afternoon's daily batch
        P.returns = []
        rb = K.rng("batch", y)
        runs = {}
        for pid, po in P.payouts.items():
            runs.setdefault(po["date"], []).append(pid)
        for day, pids in sorted(runs.items()):
            pids.sort(key=lambda p: (P.payouts[p]["k"], p))
            t0 = dt.datetime.combine(day, dt.time(7, 31)) + dt.timedelta(seconds=int(rb.integers(0, 50)))
            acc = 0.0
            for pid in pids:
                acc += float(rb.uniform(0.22, 0.61))
                P.payouts[pid]["events"].append(("created", t0 + dt.timedelta(seconds=int(acc)), ""))
            sub = t0 + dt.timedelta(seconds=int(acc) + int(rb.integers(140, 420)))
            for pid in pids:
                P.payouts[pid]["events"].append(("submitted", sub, ""))
        def posted(d):
            return dt.datetime.combine(d, dt.time(6, 5)) + dt.timedelta(seconds=int(K.rng("post", d.isoformat()).integers(0, 90)))
        def returned_at(d):
            return dt.datetime.combine(d, dt.time(5, 40)) + dt.timedelta(seconds=int(K.rng("retf", d.isoformat()).integers(0, 90)))
        def daily_batch(d):
            return dt.datetime.combine(d, dt.time(14, 30)) + dt.timedelta(seconds=int(K.rng("daily", d.isoformat()).integers(0, 90)))
        for pid in sorted(P.payouts):
            po = P.payouts[pid]
            rr = K.rng("bank", pid)
            settle = bday(po["date"], 1)
            can_return = pid not in reversed_ids and po["k"] not in merge_on
            if can_return and rr.random() < P_RETURN:
                code = _pick(rr, RETURN_CODES)
                rd = bday(settle, int(rr.integers(1, 3)))
                po["events"].append(("returned", returned_at(rd), code[0]))
                P.returns.append(dict(pid=pid, date=rd, code=code, settle=settle, n=1))
                if rr.random() < P_RESEND:
                    rs = rd + dt.timedelta(days=int(rr.geometric(0.12)) + 1)
                    while rs.weekday() >= 5 or rs in FED_HOLIDAYS:
                        rs += dt.timedelta(days=1)
                    po["events"].append(("submitted", daily_batch(rs), "payout details updated"))
                    s2 = bday(rs, 1)
                    if rr.random() < P_RETURN_AGAIN:
                        code2 = _pick(rr, RETURN_CODES)
                        rd2 = bday(s2, int(rr.integers(1, 3)))
                        po["events"].append(("returned", returned_at(rd2), code2[0]))
                        P.returns.append(dict(pid=pid, date=rd2, code=code2, settle=s2, n=2))
                        po["final"] = "returned"
                    else:
                        po["events"].append(("settled", posted(s2), ""))
                        po["final"] = "settled"
                else:
                    po["final"] = "returned"
            else:
                po["events"].append(("settled", posted(settle), ""))
                po["final"] = "settled"
        O.pay[y] = P
    # the merge record: second accounts merged into the driver's first account
    O.merged_into = {}
    for y in (2025, 2026):
        for b, (a, md) in O.pay[y].merge_on.items():
            O.merged_into[b] = (a, md)


# ------------------------------------------------------------------------------------------------- referrals
def referrals(W, O):
    """The referral programme: a driver whose referred friend completes 50 trips in their first 30 days is paid a
    bonus ($250 in 2026). Rows for 2026's qualifying referrals."""
    out = []
    pool = [k for k in range(W.n) if O.created[k].date() < dt.date(2026, 1, 1) and O.last_week[k] >= K.widx(
        dt.date(2025, 10, 1))]
    for k in range(W.n):
        if O.channel[k] != "referral":
            continue
        ft = O.first_trip[k]
        if not (dt.date(2025, 12, 2) <= ft.date() <= dt.date(2026, 11, 30)):
            continue
        w = int(W.first_week[k])
        t30 = int(W.trips[k, w:w + 4].sum()) + int(round(W.trips[k, w + 4] * 2 / 7)) if w + 4 < K.NW else 0
        if t30 < 50:
            continue
        r = K.rng("ref", k)
        ref = pool[int(r.integers(0, len(pool)))]
        q_on = (ft + dt.timedelta(days=int(r.integers(9, 30)))).date()
        if q_on > dt.date(2026, 12, 31):
            continue
        paid = q_on + dt.timedelta(days=(3 - q_on.weekday()) % 7 + 1)
        if paid.year != 2026:
            continue
        out.append(dict(referrer=ref, referred=k, first_trip=ft.date(), qualified=q_on, paid=paid))
    O.referrals = out


# ------------------------------------------------------------------------------------------------- activity cells
def activity(W, O):
    """Monthly cells per account, the legacy platform's weeks (to Sunday 14 July 2024) and the new platform's (from
    Monday 15 July 2024 to the extract run on Sunday 3 January 2027) aggregated apart; driver cancellations at each
    driver's own rate; and months inside a short break when the driver went online without completing a trip."""
    mig = K.widx(K.MIGRATION)
    end = K.ASOF_W[2027] + 1
    O.ml_old, O.T_old = _monthly(W.trips, 0, mig)
    _, O.H_old = _monthly(W.hours, 0, mig, float_=True)
    O.ml_new, O.T_new = _monthly(W.trips, mig, end)
    _, O.H_new = _monthly(W.hours, mig, end, float_=True)
    canc = np.array([K.rng("canc", k).beta(2.0, 58.0) for k in range(W.n)])
    O.cancel_rate = canc
    O.idle = {}
    for tag, ml, T in (("old", O.ml_old, O.T_old), ("new", O.ml_new, O.T_new)):
        A = T > 0
        r = K.rng("idle", tag)
        u = r.random(A.shape)
        mins = r.integers(4, 80, A.shape)
        cells = set()
        for k in range(W.n):
            act = np.nonzero(A[k])[0]
            if len(act) < 2:
                continue
            for a, b in zip(act[:-1], act[1:]):
                if 2 <= b - a <= 3:
                    for j in range(a + 1, b):
                        if u[k, j] < 0.3:
                            cells.add((k, j))
        O.idle[tag] = {c: int(mins[c]) for c in cells}


def _monthly(V, w_lo, w_hi, float_=False):
    mlist = K.months(K.wdate(w_lo), K.wdate(w_hi - 1) + dt.timedelta(days=6))
    midx = {m: j for j, m in enumerate(mlist)}
    out = np.zeros((V.shape[0], len(mlist)), dtype=np.float64 if float_ else np.int32)
    for i in range(w_lo, w_hi):
        d0 = K.wdate(i)
        days = [d0 + dt.timedelta(days=j) for j in range(7)]
        m_a, m_b = K.ym(days[0]), K.ym(days[6])
        col = V[:, i]
        if m_a == m_b:
            out[:, midx[m_a]] += col
            continue
        p = float(sum(WD.WEEKDAY_W[j] for j in range(7) if K.ym(days[j]) == m_a) / WD.WEEKDAY_W.sum())
        if not float_:
            first = K.rng("split", i).binomial(col.astype(np.int64), p)
            out[:, midx[m_a]] += first
            out[:, midx[m_b]] += col - first
        else:
            out[:, midx[m_a]] += col * p
            out[:, midx[m_b]] += col * (1 - p)
    return mlist, out


def build(W):
    O = Ops()
    ml, M = WD.monthly(W)
    O.ml, O.M = ml, M
    first_trips(W, ml, M, O)
    onboarding(W, O)
    accounts(W, O)
    payments(W, O)
    referrals(W, O)
    activity(W, O)
    return O
