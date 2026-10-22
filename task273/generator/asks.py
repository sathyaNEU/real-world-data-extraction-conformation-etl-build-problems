"""The records behind the two supplementary questions, on populations the call never reads.

Ask A, each endpoint's forecast peak-hour volume for January 2027 under the readiness standard's section 4: the requests
the endpoint served customers in its busiest clock hour of January 2026 at the edge, times its growth factor (the
employers whose plan includes it on 1 November 2026 over those on 1 January 2026). The edge counts every request it
answers: the platform's own synthetic checks are in its counts, and the three routes renamed in January kept answering
their old paths with a permanent redirect, which the edge counts on the old path while the client's follow-up is
counted on the new one. The employer accounts are the CRM's snapshot on 1 November (each account's current plan and the
start of its current subscription); the year's subscription events are in the billing system's log.

Ask B, each endpoint's service credits for breaches from 1 January to 31 October 2026, net of reversals. A credit
references the incident it is for, and the status page's register says when each incident began and which route it
hit (the route as named that day). Billing moved to a new system on 1 May: the old system's export holds amounts in
cents, and the credits still open on 30 April were carried into the new system at their unapplied balance."""
import datetime as dt
import math

import numpy as np

import common as K

PLANS = ["Starter", "Standard", "Professional", "Enterprise"]
# the plans that include each endpoint (the endpoint register's Plans column)
ENDPOINT_PLANS = {
    "EP01": PLANS, "EP02": PLANS, "EP03": PLANS, "EP04": PLANS, "EP05": PLANS[1:], "EP06": PLANS[1:],
    "EP07": PLANS[2:], "EP08": PLANS[2:], "EP09": PLANS, "EP10": PLANS, "EP11": PLANS[1:], "EP12": PLANS[1:],
    "EP13": PLANS, "EP14": PLANS[1:], "EP15": PLANS[2:], "EP16": PLANS, "EP17": PLANS, "EP18": PLANS,
    "EP19": PLANS[2:], "EP20": PLANS[2:], "EP21": PLANS[3:], "EP22": PLANS[2:], "EP23": PLANS[2:], "EP24": PLANS[1:],
}
# endpoint: (former route, first clock hour (UTC) on the current route, last day the old path redirected)
RENAMED = {
    "EP24": ("GET /v2/tax-rates/local", dt.datetime(2026, 1, 14, 15, 0), dt.date(2026, 2, 28)),
    "EP09": ("GET /v1/employees", dt.datetime(2026, 1, 19, 15, 0), dt.date(2026, 3, 31)),
    "EP19": ("GET /v1/search", dt.datetime(2026, 1, 21, 15, 0), dt.date(2026, 3, 31)),
}
REDIRECT_SHARE0 = 0.78         # share of an endpoint's customer requests still sent to the old path just after a rename
REDIRECT_DECAY_H = 24 * 13.0   # its decay (hours)
JAN0 = dt.datetime(2026, 1, 1)
HOURS = [JAN0 + dt.timedelta(hours=h) for h in range(31 * 24)]
DAY_JAN1 = dt.date(2026, 1, 1)
DAY_NOV1 = dt.date(2026, 11, 1)
EST = dt.timedelta(hours=-5)

# The uptime monitors (the monitoring repository's edge_uptime_monitors.yaml): each run of a monitor sends its steps once
# from every location. (name, every seconds, locations, steps, created)
LOC3 = ["us-east-1", "us-east-2", "us-west-2"]
LOC2 = ["us-east-1", "us-west-2"]
SYNTH_CHECKS = [
    ("auth-token", 30, LOC3, ["EP18"], dt.date(2023, 5, 9)),
    ("payroll-run-preview", 60, LOC3, ["EP18", "EP01", "EP02"], dt.date(2023, 5, 9)),
    ("employee-directory", 60, LOC3, ["EP18", "EP09", "EP10"], dt.date(2023, 6, 14)),
    ("time-and-approvals", 120, LOC3, ["EP18", "EP12", "EP11"], dt.date(2023, 6, 14)),
    ("pay-stubs-and-deposits", 120, LOC3, ["EP18", "EP13", "EP16"], dt.date(2023, 8, 2)),
    ("deductions-and-garnishments", 300, LOC2, ["EP18", "EP14", "EP15"], dt.date(2024, 2, 20)),
    ("year-end-forms", 120, LOC3, ["EP18", "EP03", "EP04"], dt.date(2025, 11, 3)),
    ("filings", 300, LOC3, ["EP18", "EP05", "EP06", "EP23"], dt.date(2024, 1, 8)),
    ("payroll-register-report", 300, LOC2, ["EP18", "EP07"], dt.date(2024, 4, 15)),
    ("companies-and-search", 120, LOC3, ["EP18", "EP17", "EP19"], dt.date(2023, 9, 27)),
    ("documents-upload", 300, LOC2, ["EP18", "EP20"], dt.date(2024, 9, 3)),
    ("webhooks-register", 600, LOC2, ["EP18", "EP21"], dt.date(2024, 9, 3)),
    ("accounting-sync-export", 300, LOC2, ["EP18", "EP22"], dt.date(2025, 3, 11)),
    ("local-taxes-lookup", 300, LOC3, ["EP18", "EP24"], dt.date(2025, 1, 6)),
    ("tax-liability-report", 300, LOC2, ["EP18", "EP08"], dt.date(2026, 3, 10)),
    ("search-by-document-type", 600, LOC3, ["EP18", "EP19"], dt.date(2026, 6, 22)),
]


def synthetic_per_hour(on=JAN0.date()):
    """Requests the synthetic checks running on a day send each endpoint in a clock hour."""
    out = {c: 0 for c in K.CODES}
    for name, every, locs, steps, created in SYNTH_CHECKS:
        if created <= on:
            for c in steps:
                out[c] += (3600 // every) * len(locs)
    return out


# ------------------------------------------------------------------------------------------------ employers (Ask A)
STATES = ["NY", "NJ", "PA", "OH", "MI", "IL", "MA", "CT", "MD", "VA", "NC", "GA", "FL", "TX", "CO", "WA", "CA", "MN",
          "WI", "IN"]
STATE_P = np.array([10, 7, 8, 6, 5, 6, 6, 3, 4, 5, 5, 5, 7, 6, 3, 3, 4, 3, 2, 2], float)
FREQ = ["biweekly", "semimonthly", "weekly", "monthly"]
FREQ_P = [0.46, 0.31, 0.17, 0.06]
P_PLAN0 = [0.38, 0.33, 0.19, 0.10]
P_PLAN_NEW = [0.42, 0.33, 0.17, 0.08]
PAYMENT_RUN = dt.date(2026, 3, 2)          # the card processor change: subscriptions whose saved card failed ended
N_PAYMENT = 118
N_RESIGN = 97


def business_days(a, b, r, k=1):
    """k random weekdays from a to b inclusive."""
    days = [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    return [days[int(i)] for i in r.integers(0, len(days), k)]


def employer_world(seed):
    """The accounts active on 1 January 2026, every subscription event of 2026 to 31 October, and each account's state
    on 1 November. Returns dict(start, events, snapshot, accounts)."""
    r = np.random.default_rng([seed, 0, 81])
    acc = {}
    n0 = 4960
    first = dt.date(2017, 9, 1)
    span = (dt.date(2025, 12, 19) - first).days
    for i in range(n0):
        eid = "EMP-%05d" % (10000 + i)
        start = first + dt.timedelta(days=int(span * (1 - r.random() ** 1.6)))
        while start.weekday() >= 5:
            start -= dt.timedelta(days=1)
        acc[eid] = dict(active=True, plan=PLANS[int(r.choice(4, p=P_PLAN0))], since=start,
                        hc=int(max(2, round(np.exp(r.normal(3.0, 1.1))))),
                        state=STATES[int(r.choice(len(STATES), p=STATE_P / STATE_P.sum()))],
                        freq=FREQ[int(r.choice(4, p=FREQ_P))])
    start_state = {e: dict(plan=a["plan"], since=a["since"]) for e, a in acc.items()}
    events = []
    nxt = 10000 + n0

    def ev(day, eid, kind, pb="", pa="", hb="", ha="", why=""):
        events.append(dict(date=day, employer=eid, kind=kind, plan_before=pb, plan_after=pa, hc_before=hb,
                           hc_after=ha, reason=why))

    for m in range(1, 11):
        a_m = dt.date(2026, m, 2 if m == 1 else 1)
        b_m = (dt.date(2026, m + 1, 1) - dt.timedelta(days=1)) if m < 10 else dt.date(2026, 10, 30)
        cand = []
        for eid in sorted(acc):
            if not acc[eid]["active"]:
                continue
            u = r.random()
            if u < 0.0046:
                cand.append((business_days(a_m, b_m, r)[0], 2, eid, "cancel"))
            elif u < 0.0046 + 0.0062:
                cand.append((business_days(a_m, b_m, r)[0], 1, eid, "plan"))
            if r.random() < 0.055:
                cand.append((business_days(a_m, b_m, r)[0], 3, eid, "hc"))
        for _ in range(int(r.poisson(72))):
            eid = "EMP-%05d" % nxt
            nxt += 1
            acc[eid] = dict(active=False, plan=PLANS[int(r.choice(4, p=P_PLAN_NEW))], since=None,
                            hc=int(max(2, round(np.exp(r.normal(2.8, 1.0))))),
                            state=STATES[int(r.choice(len(STATES), p=STATE_P / STATE_P.sum()))],
                            freq=FREQ[int(r.choice(4, p=FREQ_P))])
            cand.append((business_days(a_m, b_m, r)[0], 0, eid, "new"))
        if m == 3:
            pool = [e for e in sorted(acc) if acc[e]["active"] and acc[e]["since"] < dt.date(2026, 2, 20)]
            hit = sorted(r.choice(pool, N_PAYMENT, replace=False))
            back = set(r.choice(hit, N_RESIGN, replace=False))
            for eid in hit:
                cand.append((PAYMENT_RUN, -1, eid, "payfail"))
                if eid in back:
                    cand.append((business_days(dt.date(2026, 3, 4), dt.date(2026, 4, 24), r)[0], 0, eid, "resign"))
        cand.sort(key=lambda x: (x[0], x[1], x[2]))
        for day, _, eid, kind in cand:
            a = acc[eid]
            if kind in ("new", "resign"):
                if a["active"]:
                    continue
                if kind == "resign" and r.random() < 0.1:
                    k = PLANS.index(a["plan"])
                    a["plan"] = PLANS[min(3, k + 1)] if r.random() < 0.6 else PLANS[max(0, k - 1)]
                a["active"], a["since"] = True, day
                ev(day, eid, "new_subscription", "", a["plan"], "", a["hc"])
            elif not a["active"]:
                continue
            elif kind in ("cancel", "payfail"):
                if kind == "payfail" and any(e["employer"] == eid and e["date"] == day for e in events):
                    continue
                why = "payment_failed" if kind == "payfail" else str(r.choice(
                    ["customer_request", "switched_provider", "business_closed", "customer_request", "merged"]))
                ev(day, eid, "cancellation", a["plan"], "", a["hc"], "", why)
                a["active"] = False
            elif kind == "plan":
                k = PLANS.index(a["plan"])
                to = PLANS[min(3, k + 1)] if r.random() < 0.8 else PLANS[max(0, k - 1)]
                if to == a["plan"]:
                    continue
                ev(day, eid, "plan_change", a["plan"], to)
                a["plan"] = to
            elif kind == "hc":
                h2 = int(max(1, round(a["hc"] * np.exp(r.normal(0.0, 0.18)))))
                if h2 == a["hc"]:
                    h2 += 1
                ev(day, eid, "headcount_change", a["plan"], a["plan"], a["hc"], h2)
                a["hc"] = h2
    snapshot = {e: dict(plan=a["plan"], since=a["since"], hc=a["hc"], state=a["state"], freq=a["freq"])
                for e, a in acc.items() if a["active"]}
    by_emp = {}
    for e in events:
        by_emp.setdefault(e["employer"], []).append(e)
    return dict(start=start_state, events=events, snapshot=snapshot, accounts=acc, by_emp=by_emp)


def growth_truth(emp):
    """Per endpoint (employers on its plans on 1 November, on 1 January)."""
    out = {}
    for c in K.CODES:
        pl = set(ENDPOINT_PLANS[c])
        num = sum(1 for s in emp["snapshot"].values() if s["plan"] in pl)
        den = sum(1 for s in emp["start"].values() if s["plan"] in pl)
        out[c] = (num, den)
    return out


def plan_on(emp, eid, day):
    """An account's plan on a day from the generator's own history (None when not a customer that day)."""
    st = emp["start"].get(eid)
    active, plan = (True, st["plan"]) if st else (False, None)
    for e in emp["by_emp"].get(eid, []):
        if e["date"] > day:
            break
        if e["kind"] == "new_subscription":
            active, plan = True, e["plan_after"]
        elif e["kind"] == "cancellation":
            active = False
        elif e["kind"] == "plan_change":
            plan = e["plan_after"]
    return plan if active else None


# -------------------------------------------------------------------------------------------- edge counts (Ask A)
PAYDAYS = {dt.date(2026, 1, 2): 1.50, dt.date(2026, 1, 15): 1.38, dt.date(2026, 1, 16): 1.42,
           dt.date(2026, 1, 30): 1.46, dt.date(2026, 1, 14): 1.18, dt.date(2026, 1, 29): 1.24}


def day_weight(code, d):
    """An endpoint's January traffic on a day (Eastern), relative to a plain weekday."""
    wd = d.weekday()
    base = 0.07 if wd == 5 else (0.05 if wd == 6 else 1.0)
    if d == dt.date(2026, 1, 1):
        base = 0.09
    if d == dt.date(2026, 1, 19):
        base = 0.62
    x = (d.day - 1) / 30.0
    if code in ("EP01", "EP02", "EP11", "EP12", "EP13", "EP14", "EP15", "EP16"):
        f = PAYDAYS.get(d, 1.0)
    elif code in ("EP03", "EP04", "EP05", "EP06", "EP08", "EP20", "EP23"):
        f = 1.0 + 0.85 * x ** 1.5 + (0.35 if 26 <= d.day <= 30 else 0.0)
    elif code == "EP07":
        f = max(PAYDAYS.get(d, 1.0), 1.55 if d.day in (5, 6) else 1.0)
    elif code in ("EP09", "EP10"):
        f = 1.62 - 0.62 * x
    elif code == "EP19":
        f = 1.0 + 0.75 * x ** 2
    elif code == "EP22":
        f = 1.5 if 5 <= d.day <= 9 else 1.0
    elif code == "EP24":
        f = 1.6 if 5 <= d.day <= 9 else (1.15 if d.day <= 13 else 1.0)
    else:
        f = 1.0 + 0.12 * PAYDAYS.get(d, 1.0)
    return base * f


def hour_weight(hr):
    """Eastern hour of day (the hour's midpoint)."""
    return math.exp(-0.5 * ((hr - 11.0) / 2.4) ** 2) + 0.55 * math.exp(-0.5 * ((hr - 15.0) / 1.6) ** 2) + 0.02


def edge_hourly(seed, achieved, growth):
    """Customer requests each endpoint served in each clock hour of January 2026 (UTC), calibrated so the forecast for
    January 2027 sits under the throughput its November test achieved; the redirects the renamed routes' old paths
    answered after each rename. Returns (customers {code: [count per hour]}, redirects {code: [count per hour]})."""
    r = np.random.default_rng([seed, 0, 82])
    cust, redir = {}, {}
    for c in K.CODES:
        shape = []
        for h in HOURS:
            loc = h + EST
            shape.append(day_weight(c, loc.date()) * hour_weight(loc.hour + 0.5))
        shape = np.array(shape)
        num, den = growth[c]
        target = achieved[c] * r.uniform(0.72, 0.90) * 3600.0 * den / num
        lam = target * shape / shape.max()
        noise = np.exp(0.035 * r.standard_normal(len(HOURS)))
        cust[c] = [int(x) for x in r.poisson(lam * noise)]
        if c in RENAMED:
            old, t, _ = RENAMED[c]
            red = []
            for i, h in enumerate(HOURS):
                if h < t:
                    red.append(0)
                else:
                    share = REDIRECT_SHARE0 * math.exp(-(h - t).total_seconds() / 3600.0 / REDIRECT_DECAY_H)
                    red.append(int(r.binomial(cust[c][i], share)))
            redir[c] = red
    return cust, redir


EXTRA_ROUTES = {   # routes the edge serves that are not public API endpoints: (requests an hour, bytes a request)
    "GET /healthz": (7200, 46), "GET /v2/status": (2400, 310), "GET /v1/openapi.json": (30, 118000),
}
BYTES = {c: b for c, b in zip(K.CODES, [3100, 9800, 21400, 18800, 1400, 900, 41200, 38800, 26100, 2400, 700, 600,
                                         15600, 3300, 1100, 900, 2100, 1300, 12800, 1900, 800, 2600, 1500, 4400])}


def edge_rows(seed, cust, redir):
    """The edge's hourly export: one row per clock hour (UTC) and route with any traffic."""
    r = np.random.default_rng([seed, 0, 83])
    synth = synthetic_per_hour()
    rows = []
    for i, h in enumerate(HOURS):
        stamp = h.strftime("%Y-%m-%dT%H:00:00Z")
        for c in K.CODES:
            served = cust[c][i] + synth[c]
            if c in RENAMED and h < RENAMED[c][1]:
                route = RENAMED[c][0]
            else:
                route = K.PATH[c]
            err = int(r.binomial(served, 0.0006))
            rows.append((stamp, route, served, err, int(served * BYTES[c] * r.uniform(0.93, 1.07))))
            if c in RENAMED and h >= RENAMED[c][1] and redir[c][i] > 0:
                rows.append((stamp, RENAMED[c][0], redir[c][i], 0, int(redir[c][i] * r.uniform(172, 186))))
        for route, (n, b) in EXTRA_ROUTES.items():
            k = n if route == "GET /healthz" else int(r.poisson(n * (0.4 + 0.6 * hour_weight((h + EST).hour + 0.5))))
            rows.append((stamp, route, k, 0, int(k * b * r.uniform(0.97, 1.03))))
    return [x for x in rows if x[2] > 0]


def ask_a_truth(cust, growth):
    """Per endpoint: (busiest hour's customer requests, its hour, the forecast in whole requests an hour)."""
    out = {}
    for c in K.CODES:
        v = cust[c]
        i = int(np.argmax(v))
        assert sorted(v)[-1] > sorted(v)[-2], "tie for the busiest hour on %s" % c
        num, den = growth[c]
        x = v[i] * num / den
        assert abs(x - math.floor(x) - 0.5) > 1e-6
        out[c] = (v[i], HOURS[i], int(math.floor(x + 0.5)))
    return out


# --------------------------------------------------------------------------------------- incidents and credits (Ask B)
FEE_RANGE = {"Starter": (18, 95), "Standard": (55, 280), "Professional": (160, 780), "Enterprise": (420, 2400)}
OTHER_COMPONENTS = ["Web app", "Mobile app", "Employee portal", "Tax e-file gateway"]


def incident_world(seed, emp):
    """Incidents from December 2025 to mid-November 2026 (UTC starts) and the credits issued for them."""
    r = np.random.default_rng([seed, 0, 84])
    inc = []

    def start_on(day):
        return dt.datetime.combine(day, dt.time(int(r.integers(13, 23)), int(r.integers(0, 60)), int(r.integers(0, 60))))

    for c in K.CODES:
        # one incident in the weeks before the billing migration, credited in the legacy system
        days = business_days(dt.date(2026, 2, 23), dt.date(2026, 3, 13), r)
        days += business_days(dt.date(2026, 1, 6), dt.date(2026, 10, 28), r, int(r.integers(2, 6)))
        for day in days:
            inc.append(dict(code=c, start=start_on(day)))
        if r.random() < 0.5:
            inc.append(dict(code=c, start=start_on(business_days(dt.date(2025, 12, 8), dt.date(2025, 12, 29), r)[0])))
        if r.random() < 0.35:
            inc.append(dict(code=c, start=start_on(business_days(dt.date(2026, 11, 2), dt.date(2026, 11, 6), r)[0])))
    for comp in OTHER_COMPONENTS:
        for day in business_days(dt.date(2026, 1, 6), dt.date(2026, 10, 28), r, int(r.integers(1, 4))):
            inc.append(dict(code=None, comp=comp, start=start_on(day)))
    inc.sort(key=lambda x: x["start"])
    seq = {}
    for x in inc:
        y = x["start"].year
        seq[y] = seq.get(y, 0) + 1
        x["key"] = "INC-%d-%04d" % (y, seq[y] + (180 if y == 2025 else 0))
        x["minutes"] = int(r.integers(12, 141))
        x["sev"] = "SEV2" if r.random() < 0.35 else "SEV3"
        x["kind"] = str(r.choice(["latency", "errors", "latency", "unavailable"]))
        if x["code"]:
            c = x["code"]
            x["comp"] = RENAMED[c][0] if (c in RENAMED and x["start"] < RENAMED[c][1]) else K.PATH[c]
    # credits: each affected account on a plan that includes the endpoint
    credits = []
    for x in inc:
        day = (x["start"] + EST).date()
        if x["code"]:
            pl = set(ENDPOINT_PLANS[x["code"]])
        else:
            pl = set(PLANS)
        k = int(r.integers(2, 10))
        pool = [e for e in sorted(emp["accounts"]) if (plan_on(emp, e, day) or "") in pl] if day.year == 2026 else \
            [e for e in sorted(emp["start"]) if emp["start"][e]["plan"] in pl]
        for eid in r.choice(pool, k, replace=False):
            plan = plan_on(emp, eid, day) if day.year == 2026 else emp["start"][eid]["plan"]
            lo, hi = FEE_RANGE[plan]
            amt = round(float(r.uniform(lo, hi)) * (1.6 if x["sev"] == "SEV2" else 1.0), 2)
            issued = day + dt.timedelta(days=int(r.integers(3, 20)))
            credits.append(dict(incident=x["key"], code=x["code"], account=str(eid), amount=amt, issued=issued,
                                in_window=K.WINDOW_FROM <= day <= K.WINDOW_TO))
    return inc, credits


def billing(seed, credits):
    """The two billing systems' records: legacy (to 30 April, cents) and new (from 1 May), with the open legacy credits
    carried into the new system at their unapplied balance, and the new system's reversals."""
    r = np.random.default_rng([seed, 0, 85])
    legacy, new = [], []
    n1, n2 = 4210, 100000
    order = sorted(credits, key=lambda x: (x["issued"], x["incident"], x["account"]))
    for x in order:
        if x["issued"] < K.MIGRATION:
            n1 += 1
            void = r.random() < 0.04
            row = dict(credit_no="BC-%06d" % n1, issued=x["issued"], account=x["account"], incident=x["incident"],
                       cents=int(round(x["amount"] * 100)), status="void" if void else "issued", code=x["code"],
                       amount=x["amount"], balance=0.0, in_window=x["in_window"])
            if not void:
                # the legacy system applied credits to the invoice of the 1st of the next month; a credit larger than
                # that invoice carried its remainder on
                if x["issued"] >= dt.date(2026, 4, 1):
                    row["balance"] = x["amount"]
                elif r.random() < (0.35 if x["issued"] >= dt.date(2026, 3, 1) else 0.05):
                    row["balance"] = round(x["amount"] * float(r.uniform(0.12, 0.88)), 2)
            legacy.append(row)
    # every endpoint carries at least one partly applied credit across the migration
    for c in K.CODES:
        mine = [x for x in legacy if x["code"] == c and x["status"] == "issued" and x["issued"] < dt.date(2026, 4, 1)
                and x["in_window"]]
        if not any(0 < x["balance"] < x["amount"] for x in mine):
            x = max(mine, key=lambda y: (y["amount"], y["credit_no"]))
            x["balance"] = round(x["amount"] * float(r.uniform(0.25, 0.75)), 2)
    carried = sorted([x for x in legacy if x["balance"] > 0], key=lambda y: y["credit_no"])
    for x in carried:
        n2 += int(r.integers(1, 3))
        new.append(dict(id="CR-%06d" % n2, created=dt.datetime(2026, 5, 1, 4, 0, 0) + dt.timedelta(seconds=n2 % 97),
                        account=x["account"], incident=x["incident"], kind="credit", amount=x["balance"],
                        memo="Balance carried forward from legacy billing", reverses=None, code=x["code"], native=False))
    native = [x for x in order if x["issued"] >= K.MIGRATION and x["issued"] <= K.CREDITS_TO]
    rows = []
    for x in native:
        t = dt.datetime.combine(x["issued"], dt.time(int(r.integers(13, 22)), int(r.integers(0, 60)),
                                                      int(r.integers(0, 60))))
        rows.append(dict(created=t, account=x["account"], incident=x["incident"], kind="credit", amount=x["amount"],
                         code=x["code"], native=True,
                         memo=str(r.choice(["Service credit, %s" % x["incident"], "SLA credit: %s" % x["incident"],
                                            "Credit for incident %s" % x["incident"]]))))
        if r.random() < 0.07:
            t2 = t + dt.timedelta(days=int(r.integers(5, 41)), hours=int(r.integers(0, 5)))
            if t2.date() <= K.CREDITS_TO:
                rows.append(dict(created=t2, account=x["account"], incident=x["incident"], kind="reversal",
                                 amount=-x["amount"], code=x["code"], native=True, ref_of=len(rows) - 1,
                                 memo=str(r.choice(["Reversal: account not affected", "Reversed, duplicate request",
                                                    "Reversal: outside service schedule"]))))
    idx = sorted(range(len(rows)), key=lambda i: (rows[i]["created"], i))
    ids = {}
    for i in idx:
        n2 += int(r.integers(1, 4))
        ids[i] = "CR-%06d" % n2
    for i in idx:
        x = rows[i]
        new.append(dict(id=ids[i], created=x["created"], account=x["account"], incident=x["incident"], kind=x["kind"],
                        amount=x["amount"], memo=x["memo"], reverses=ids[x["ref_of"]] if "ref_of" in x else None,
                        code=x["code"], native=True))
    new.sort(key=lambda x: (x["created"], x["id"]))
    return legacy, new


def eastern_day(t):
    return (t + EST).date()


def ask_b_truth(inc, legacy, new):
    """Per endpoint, dollars: every credit once at the amount issued (a legacy credit carried forward is counted in
    the legacy record), reversals netted, for incidents that began from 1 January to 31 October 2026 (Eastern)."""
    start = {x["key"]: x for x in inc}
    tot = {c: 0.0 for c in K.CODES}
    for x in legacy:
        i = start[x["incident"]]
        if x["status"] == "issued" and i["code"] and K.WINDOW_FROM <= eastern_day(i["start"]) <= K.WINDOW_TO:
            tot[i["code"]] += x["cents"] / 100.0
    for x in new:
        i = start[x["incident"]]
        if x["native"] and i["code"] and K.WINDOW_FROM <= eastern_day(i["start"]) <= K.WINDOW_TO:
            tot[i["code"]] += x["amount"]
    out = {}
    for c, v in tot.items():
        assert abs(v - math.floor(v) - 0.5) > 0.004, "credits on %s sit on a rounding tie" % c
        out[c] = int(math.floor(v + 0.5))
    return out
