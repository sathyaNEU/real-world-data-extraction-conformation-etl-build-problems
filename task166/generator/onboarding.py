"""The onboarding team's two exports: the case list from its onboarding tool (one case per new paying subscription it
onboards, with the order form's plan, seats and contract value at handoff) and the session log from its scheduling tool
(one row per booking per host: a customer booking a group webinar gets its own row, and a specialist shadowing a
colleague is a second host on the same booking). Also the post-onboarding satisfaction survey.

Specialists work in three pods (West: Southwest and Pacific; Central: Texas & Gulf and Midwest; East: Southeast and
Northeast). Every new customer, division and returning customer gets a kickoff, an admin setup session, a seat in the
region's weekly field app webinar and a go-live review; a pod's regions each have a weekly drop-in office hour."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np

import common as K
import records as RC

F_CASES = "onboarding_cases_2024-01_2026-09.csv"
F_SESSIONS = "onboarding_sessions_2024-01_2026-09.csv"
F_CSAT = "onboarding_csat_responses_2024-2026.csv"
F_ROSTER = "onboarding_team_roster_2026-10-01.csv"
POD = {K.SW: "West", K.PA: "West", K.TX: "Central", K.MW: "Central", K.SE: "East", K.NE: "East"}
START = dt.date(2024, 1, 1)
# specialists: pods (each from a date), first day, last day (None if still on the team); names are drawn below. The team
# was rebalanced twice: one Central specialist moved to West on 1 July 2025, and on 1 April 2026 one East specialist moved
# to Central and one West specialist to East.
_SPEC = [
    ((("West", None),), dt.date(2021, 3, 1), None),
    ((("West", None), ("East", dt.date(2026, 4, 1))), dt.date(2022, 6, 6), None),
    ((("West", None),), dt.date(2023, 1, 9), None),
    ((("West", None),), dt.date(2025, 8, 4), None),
    ((("Central", None),), dt.date(2020, 9, 14), None),
    ((("Central", None), ("West", dt.date(2025, 7, 1))), dt.date(2022, 2, 7), None),
    ((("Central", None),), dt.date(2023, 5, 1), None),
    ((("Central", None),), dt.date(2025, 2, 3), None),
    ((("East", None), ("Central", dt.date(2026, 4, 1))), dt.date(2021, 8, 2), None),
    ((("East", None),), dt.date(2022, 10, 3), dt.date(2025, 6, 13)),
    ((("East", None),), dt.date(2023, 3, 6), None),
    ((("East", None),), dt.date(2025, 6, 23), None),
]


def _roster():
    r_ = K.rng(29)
    out, firsts, lasts = [], set(), set()
    for spans, d0, d1 in _SPEC:
        while True:
            f, l = K.FIRST[int(r_.integers(len(K.FIRST)))], K.LAST[int(r_.integers(len(K.LAST)))]
            if f not in firsts and l not in lasts:
                firsts.add(f)
                lasts.add(l)
                break
        out.append((f + " " + l, spans, d0, d1))
    return out


def pod_at(s, d):
    pod = s[1][0][0]
    for p_, since in s[1][1:]:
        if d >= since:
            pod = p_
    return pod


ROSTER = _roster()
SHADOW_WEEKS = 6
OH_TURN = int(os.environ.get("T166_OH_TURN", 2))      # where each region's office-hour rota starts
WEBINAR_DAY = {K.SW: 1, K.PA: 3, K.TX: 1, K.MW: 3, K.SE: 1, K.NE: 3}      # Tuesday or Thursday
WEBINAR_HOUR = {K.SW: 10, K.PA: 10, K.TX: 13, K.MW: 10, K.SE: 13, K.NE: 10}
# each region's office hour runs on its pod partner's webinar day, starting half an hour into that webinar
PARTNER = {K.SW: K.PA, K.PA: K.SW, K.TX: K.MW, K.MW: K.TX, K.SE: K.NE, K.NE: K.SE}
OFFICE_DAY = {r: WEBINAR_DAY[PARTNER[r]] for r in PARTNER}
REGION_TZ = {K.SW: "AZ", K.PA: "CA", K.TX: "TX", K.MW: "IL", K.SE: "GA", K.NE: "NY"}   # the clock a regional session is set in
POD_TZ = {"West": "CA", "Central": "TX", "East": "NY"}                                # the clock a pod's group sessions are set in


def specialists(pod, d):
    return [s for s in ROSTER if pod_at(s, d) == pod and s[2] <= d and (s[3] is None or d <= s[3])]


def by_name(name):
    return next(s for s in ROSTER if s[0] == name)


def seniors(pod, d):
    team = specialists(pod, d)
    return [s for s in team if (d - s[2]).days >= 7 * SHADOW_WEEKS] or team


class Calendar:
    """Each specialist's booked time in UTC, so no one hosts two sessions at once."""

    def __init__(self):
        self.busy = {}

    def free(self, host, start, minutes):
        end = start + dt.timedelta(minutes=minutes)
        for a, b in self.busy.get((host, start.date()), []):
            if start < b + dt.timedelta(minutes=15) and a < end + dt.timedelta(minutes=15):
                return False
        return True

    def take(self, host, start, minutes):
        self.busy.setdefault((host, start.date()), []).append((start, start + dt.timedelta(minutes=minutes)))


def build(B):
    """Cases and sessions from the billing companies in B (records.build)."""
    r_ = K.rng(30)
    cases = []
    for c in B["comps"]:
        reg = c["region"]
        if START <= c["first_inv"] <= K.DATA_END:
            plan, seats, acv = c["plan0"], c["seats0"], c["acv0"]
            pb = "Re-onboarding" if c.get("returning_of") else "New logo"
            cases.append(dict(comp=c, crm=c["crm"], name=c["name"], region=reg, playbook=pb, d0=c["first_inv"], plan=plan,
                              seats=seats, acv=acv, cancel=c["cancel"], kind="new"))
        if c.get("react") and START <= c["react"]["date"] <= K.DATA_END:
            rr = c["react"]
            cases.append(dict(comp=c, crm=c["crm"], name=c["name"], region=reg, playbook="Re-onboarding", d0=rr["date"],
                              plan=rr["plan"], seats=rr["seats"], acv=rr["acv"], cancel=None, kind="react"))
        for d in c["divisions"]:
            if START <= d["first_inv"] <= K.DATA_END:
                cases.append(dict(comp=c, crm=d["crm"], name=d["name"], region=reg, playbook="Expansion", d0=d["first_inv"],
                                  plan=d["plan"], seats=d["seats"], acv=d["acv"], cancel=d["cancel"], kind="division"))
    cases.sort(key=lambda x: (x["d0"], x["crm"]))
    for i, cs in enumerate(cases):
        cs["case_id"] = "OB-%05d" % (31000 + i * 2 + int(r_.integers(0, 2)))
        cs["opened"] = min(K.business_day(cs["d0"] + dt.timedelta(days=int(r_.integers(0, 3)))), K.DATA_END)
        senior = seniors(POD[cs["region"]], cs["opened"])
        cs["owner"] = senior[int(r_.integers(len(senior)))][0]
    # implementation partners run the one-to-one sessions of some customers' onboarding, booking them as themselves
    rp = K.rng(32)
    shares = np.array([p["share"] for p in B["partners"]])
    for cs in cases:
        u = rp.random()
        j = int(rp.choice(len(shares), p=shares / shares.sum()))
        rate = {"Enterprise": 0.24, "Pro": 0.12, "Core": 0.05}[cs["plan"]]
        cs["partner"] = B["partners"][j] if u < rate else None
    sessions = []
    nb = [0]
    cal = Calendar()
    # the regional webinars and office hours hold their hosts' slots every week, booked or not
    fixed = {}
    rcov = K.rng(34)                  # a specialist from another pod covers a session now and then (own stream)

    def cover(pod, d, start, minutes, rate=0.05):
        """a senior specialist of another pod, free at the start, or None"""
        u, k = rcov.random(), int(rcov.integers(0, 1000))
        if u >= rate:
            return None
        others = sorted(s_[0] for p_ in ("West", "Central", "East") if p_ != pod for s_ in seniors(p_, d))
        others = [h for h in others if cal.free(h, start, minutes)]
        return others[k % len(others)] if others else None

    def rota(team, turn, start, minutes):
        """the slot's turn on the pod's rota, passed down to the next senior when that one is already hosting, and to a
        free senior of another pod when the whole pod is"""
        for j in range(len(team)):
            h = team[(turn + j) % len(team)][0]
            if cal.free(h, start, minutes):
                return h
        pod = pod_at(team[0], start.date())
        others = sorted(s_[0] for p_ in ("West", "Central", "East") if p_ != pod for s_ in seniors(p_, start.date())
                        if cal.free(s_[0], start, minutes))
        return others[turn % len(others)] if others else team[turn % len(team)][0]

    d = START
    while d <= K.DATA_END:
        if d not in K.HOLIDAYS:
            for reg in range(6):
                if d.weekday() == WEBINAR_DAY[reg]:
                    team = sorted(seniors(POD[reg], d))
                    start = K.local_to_utc(POD_TZ[POD[reg]], d, WEBINAR_HOUR[reg], 0)
                    host = rota(team, d.toordinal() // 7 + reg, start, 90)
                    host = cover(POD[reg], d, start, 90, 0.10) or host
                    cal.take(host, start, 90)
                    fixed[("web", reg, d)] = (host, start)
            for reg in range(6):
                if d.weekday() == OFFICE_DAY[reg]:
                    team = sorted(seniors(POD[reg], d))
                    start = K.local_to_utc(POD_TZ[POD[reg]], d, WEBINAR_HOUR[PARTNER[reg]], 30)
                    host = rota(team, d.toordinal() // 7 + 2 * reg + OH_TURN, start, 60)
                    host = cover(POD[reg], d, start, 60, 0.10) or host
                    cal.take(host, start, 60)
                    fixed[("oh", reg, d)] = (host, start)
        d += dt.timedelta(days=1)
    rre = K.rng(35)

    def keep_owner(cs, day):
        """a case passes to another senior of its pod when its owner has moved pod or left"""
        s_ = by_name(cs["owner"])
        if pod_at(s_, day) != POD[cs["region"]] or (s_[3] is not None and day > s_[3]):
            team = sorted(seniors(POD[cs["region"]], day))
            cs["owner"] = team[int(rre.integers(len(team)))][0]

    def booking(cs, typ, start, minutes, host, status, attendees, group_key=None):
        nb[0] += 1
        acct = cs["partner"]["crm"] if (cs.get("partner") and group_key is None) else cs["crm"]
        sessions.append(dict(bk="BK-%08d" % (20400000 + nb[0] * 5 + int(r_.integers(0, 5))), case=cs, typ=typ, start=start,
                             minutes=minutes, host=host, status=status, attendees=attendees, group=group_key, acct=acct))
        return sessions[-1]

    def one_to_one(cs, typ, day, minutes):
        """Book a one-to-one, rebooking after a no-show, cancellation or reschedule; returns the held session's day."""
        st = REGION_TZ[cs["region"]]
        for attempt in range(4):
            start = None
            for _ in range(12):
                day = K.business_day(day)
                if day > K.DATA_END:
                    return None
                keep_owner(cs, day)
                for _ in range(6):
                    hour = int(r_.choice([8, 9, 10, 11, 13, 14]))
                    cand = K.local_to_utc(st, day, hour, int(r_.choice([0, 0, 30])))
                    if cal.free(cs["owner"], cand, minutes):
                        start = cand
                        break
                if start is not None:
                    break
                day = day + dt.timedelta(days=1)
            if start is None:
                return None
            host = cover(POD[cs["region"]], day, start, minutes) or cs["owner"]
            cal.take(host, start, minutes)
            u = r_.random()
            status = "Completed" if (u < 0.90 or attempt == 3) else ("No-show" if u < 0.94 else ("Rescheduled" if u < 0.98 else "Cancelled by customer"))
            s = booking(cs, typ, start, minutes, host, status, int(r_.integers(1, 4)))
            if status == "Completed":
                # a specialist in the first weeks on the pod co-hosts
                pod = POD[cs["region"]]
                for sp in specialists(pod, day):
                    if (0 <= (day - sp[2]).days < 7 * SHADOW_WEEKS and sp[0] != host and r_.random() < 0.6
                            and cal.free(sp[0], start, minutes)):
                        cal.take(sp[0], start, minutes)
                        sessions.append(dict(s, host=sp[0], shadow=True))
                return day
            day = day + dt.timedelta(days=int(r_.integers(2, 8)))
        return None

    webinar_seats = {}
    for cs in cases:
        d0 = cs["opened"]
        mins_kick = 60 if cs["kind"] == "new" else 45
        kick = one_to_one(cs, "Kickoff", d0 + dt.timedelta(days=int(r_.integers(2, 16))), mins_kick)
        if kick is None:
            continue
        if cs["cancel"] is not None and cs["cancel"] < kick + dt.timedelta(days=20):
            cs["status"] = "Closed - cancelled"
            continue
        if cs["kind"] != "react":
            setup = one_to_one(cs, "Admin setup", kick + dt.timedelta(days=int(r_.integers(5, 13))), 45)
            if setup is not None:
                # the region's next field app webinar, three or more days on
                d = setup + dt.timedelta(days=3)
                while d.weekday() != WEBINAR_DAY[cs["region"]] or d in K.HOLIDAYS:
                    d += dt.timedelta(days=1)
                if d <= K.DATA_END:
                    webinar_seats.setdefault((cs["region"], d), []).append(cs)
        go = one_to_one(cs, "Go-live review", d0 + dt.timedelta(days=int(r_.integers(35, 80))), 30)
        cs["go_live"] = go
    # true-ups agreed at go-live: seats for the users added during onboarding, or a plan change (own stream)
    rt = K.rng(33)
    rt2 = K.rng(37)          # seats taken in the same go-live change as a plan move (own stream)
    for cs in cases:
        u, v, lead = rt.random(), rt.random(), int(rt.integers(0, 6))
        k = int(rt.integers(3, 14)) if cs["comp"]["kind"] != "gc" else int(rt.integers(15, 60))
        w, k2 = rt2.random(), int(rt2.integers(2, 10))
        if cs["kind"] != "new" or not cs.get("go_live"):
            continue
        c = cs["comp"]
        day = max(cs["go_live"] - dt.timedelta(days=lead), c["first_inv"] + dt.timedelta(days=7))
        if c["cancel"] is not None and c["cancel"] <= day:
            continue
        plan_now = RC._state_at(c, day)[0]
        if u < 0.09 and plan_now != "Enterprise":
            c["amend"].append(dict(date=day, change="Upgrade", k=0, plan=None, seats=None, acv=None))
        elif u < 0.12 and plan_now != "Core" and c["kind"] != "gc":
            c["amend"].append(dict(date=day, change="Downgrade", k=0, plan=None, seats=None, acv=None))
        elif v < 0.16:
            c["amend"].append(dict(date=day, change="Add seats", k=k, plan=None, seats=None, acv=None))
        else:
            continue
        if c["amend"][-1]["change"] != "Add seats" and w < 0.85:
            # seats for the users added during onboarding, in the same change as the plan move
            c["amend"].append(dict(date=day, change="Add seats", k=k2, plan=None, seats=None, acv=None))
        RC.rechain(c)
    # the first year's prices and their step at the first anniversary (own streams)
    B["offer"] = RC.first_year_pricing(B, cases)
    # the weekly webinars: one booking per customer, each carrying the webinar's own start and length
    for (reg, d), seats in sorted(webinar_seats.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        host, start = fixed[("web", reg, d)]
        any_held = False
        rows = []
        for cs in seats:
            u = r_.random()
            status = "Completed" if u < 0.88 else ("No-show" if u < 0.97 else "Cancelled by customer")
            any_held |= status == "Completed"
            rows.append((cs, status))
        if not any_held:
            rows[0] = (rows[0][0], "Completed")
        for cs, status in rows:
            booking(cs, "Field app training", start, 90, host, status, int(r_.integers(1, 7)), group_key=(reg, d))
    # weekly drop-in office hours, booked by customers in onboarding
    open_cases = {}
    for cs in cases:
        if cs.get("go_live"):
            open_cases.setdefault(cs["region"], []).append(cs)
    d = START
    while d <= K.DATA_END:
        for reg in range(6):
            if d.weekday() != OFFICE_DAY[reg] or d in K.HOLIDAYS:
                continue
            live = [cs for cs in open_cases.get(reg, []) if cs["opened"] <= d <= cs["go_live"]]
            k = min(len(live), int(r_.poisson(1.6)))
            if not k:
                continue
            host, start = fixed[("oh", reg, d)]
            idx = r_.choice(len(live), size=k, replace=False)
            for j in idx:
                booking(live[int(j)], "Office hours", start, 60, host, "Completed" if r_.random() < 0.93 else "No-show", 1,
                        group_key=("oh", reg, d))
        d += dt.timedelta(days=1)
    for cs in cases:
        if "status" in cs:
            continue
        if cs["cancel"] is not None and cs["cancel"] <= K.DATA_END:
            cs["status"] = "Closed - cancelled"
        elif cs.get("go_live"):
            cs["status"] = "Live"
        elif (K.DATA_END - cs["opened"]).days > 120:
            cs["status"] = "Closed - no response"
        else:
            cs["status"] = "In onboarding"
    sessions.sort(key=lambda s: (s["start"], s["bk"], s["host"]))
    handovers(sessions)
    # the export lists a booking's specialists in the order they were assigned to it
    sessions.sort(key=lambda s: (s["start"], s["bk"], 0 if s.get("declined") else (2 if s.get("shadow") else 1)))
    return dict(cases=cases, sessions=sessions)


def _region(b):
    g = b["group"]
    return b["case"]["region"] if g is None else (g[1] if g[0] == "oh" else g[0])


def handovers(sessions, rate=0.04):
    """A session first assigned to a specialist who then took a longer session of their own over it is handed to a
    colleague, and the scheduling tool keeps the first specialist on the booking's host list (own stream). The handed
    booking lies wholly inside the specialist's own session, which no one else hosts, and the colleague holds nothing
    else then."""
    rh = K.rng(38)
    units = {}
    hosts_of = {}
    for s in sessions:
        units.setdefault((s["host"], s["start"]), []).append(s)
        hosts_of.setdefault(s["bk"], set()).add(s["host"])
    single = {u for u, bs in units.items() if all(len(hosts_of[b["bk"]]) == 1 for b in bs)}
    held = {u for u, bs in units.items() if any(b["status"] == "Completed" for b in bs)}

    def span(u):
        return u[1], u[1] + dt.timedelta(minutes=units[u][0]["minutes"])

    def over(a, b, m=None):
        (a0, a1), (b0, b1) = span(a), span(b)
        gap = min(a1, b1) - max(a0, b0)
        return gap >= dt.timedelta(minutes=m) if m else gap > dt.timedelta(0)

    def inside(v, u):
        """v lies wholly within u and does not start with it"""
        (u0, u1), (v0, v1) = span(u), span(v)
        return u0 < v0 and v1 <= u1
    by_day, own = {}, {}
    for u in units:
        by_day.setdefault(u[1].date(), []).append(u)
        own.setdefault((u[0], u[1].date()), []).append(u)
    taken = set()
    listed = {}                                   # host -> the bookings they are listed on and did not host

    def candidates(u):
        h, t1 = u
        pod = pod_at(by_name(h), t1.date())
        out = []
        for v in by_day.get(t1.date(), []):
            h2 = v[0]
            if h2 == h or v[1] == t1 or v in taken or v not in single or v not in held or not inside(v, u):
                continue
            if POD[_region(units[v][0])] != pod:
                continue
            # h is on v only through u, and v touches nothing h2 or h already shares or is listed on
            if any(w != u and over(w, v) for w in own.get((h, t1.date()), [])):
                continue
            if any(over(w, v) for w in listed.get(h2, [])) or any(over(w, v) for w in listed.get(h, [])):
                continue
            out.append(v)
        return out

    def add(u, v):
        taken.update((u, v))
        listed.setdefault(u[0], []).append(v)
        for b in units[v]:
            sessions.append(dict(b, host=u[0], declined=True))

    def kind(v):
        return "group" if units[v][0]["group"] is not None else "one-to-one"

    triggers = [u for u in sorted(units, key=lambda u: (u[1], u[0])) if u in single and u in held]
    def across(u, vs):
        """the sessions a colleague of another pod took over"""
        pod = pod_at(by_name(u[0]), u[1].date())
        return [v for v in vs if pod_at(by_name(v[0]), v[1].date()) != pod]

    for u in triggers:
        if rh.random() >= rate or u in taken:
            continue
        cands = candidates(u)
        if not cands:
            continue
        grp = [v for v in cands if kind(v) == "group"]
        one = [v for v in cands if kind(v) == "one-to-one"]
        pool = grp if (grp and (not one or rh.random() < 0.75)) else one
        pool = (across(u, pool) or pool) if rh.random() < 0.8 else pool
        if pool:
            add(u, sorted(pool, key=lambda v: (v[1], v[0]))[int(rh.integers(len(pool)))])
    # every pod's specialists are reassigned now and then in each quarter, on both kinds of session, and in each quarter some
    # session of every pod goes to or comes from a colleague of another pod
    cell = lambda u, v: (pod_at(by_name(u[0]), u[1].date()), (u[1].month - 1) // 3, kind(v))
    cell2 = lambda u, v: (pod_at(by_name(v[0]), v[1].date()), (u[1].month - 1) // 3, kind(v))
    want = {(p, q, k) for p in ("West", "Central", "East") for q in range(4) for k in ("one-to-one", "group")}
    have = {cell((h, v[1]), v) for h, vs in listed.items() for v in vs if v[1].year == 2025}
    both = {c for h, vs in listed.items() for v in vs if v[1].year == 2025 and cell((h, v[1]), v) != cell2((h, v[1]), v)
            for c in (cell((h, v[1]), v), cell2((h, v[1]), v))}
    both |= {(pod_at(by_name(s["host"]), s["start"].date()), (s["start"].month - 1) // 3,
              "group" if s["group"] is not None else "one-to-one") for s in sessions if s.get("shadow") and s["start"].year == 2025}
    rf = K.rng(39)
    for u in triggers:
        if not (want - have) and not (want - both):
            break
        if u[1].year != 2025 or u in taken:
            continue
        cs_ = candidates(u)
        cands = [v for v in cs_ if cell(u, v) in want - have] or \
                [v for v in across(u, cs_) if {cell(u, v), cell2(u, v)} & (want - both)]
        cands = across(u, cands) or cands
        if cands:
            v = sorted(cands, key=lambda v: (v[1], v[0]))[int(rf.integers(len(cands)))]
            add(u, v)
            have.add(cell(u, v))
            if cell(u, v) != cell2(u, v):
                both.update((cell(u, v), cell2(u, v)))


def write_all(out, O):
    n = {}
    rows = []
    for cs in O["cases"]:
        plan, seats, acv = RC.sku(cs["plan"], cs["d0"]), cs["seats"], cs["acv"]
        if cs["kind"] == "new":
            # the onboarding tool keeps the case's plan, seats and value in step with the subscription while the case is open
            c = cs["comp"]
            if cs["status"] == "Live":
                closed = cs["go_live"]
            elif cs["status"] == "Closed - cancelled":
                closed = min(c["cancel"], K.DATA_END) if c["cancel"] is not None else K.DATA_END
            elif cs["status"] == "Closed - no response":
                closed = cs["opened"] + dt.timedelta(days=120)
            else:
                closed = K.DATA_END
            plan, seats, acv, _ = RC._state_at(c, closed)
            plan = RC.sku(plan, RC.plan_set_on(c, closed))
        rows.append([cs["case_id"], cs["crm"], cs["name"], cs["playbook"], cs["opened"].isoformat(), cs["owner"], plan,
                     seats, "%.2f" % acv, cs["go_live"].isoformat() if cs.get("go_live") else "", cs["status"]])
    n[F_CASES] = K.write_csv(os.path.join(out, F_CASES),
        ["case_id", "crm_account_id", "account_name", "playbook", "opened_on", "owner", "rate_plan_sku", "seats", "contract_acv_usd",
         "go_live_on", "status"], rows)
    rows = []
    for s in O["sessions"]:
        rows.append([s["bk"], s["case"]["case_id"], s["acct"], s["typ"], s["host"], s["start"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                     s["minutes"], s["status"], s["attendees"]])
    n[F_SESSIONS] = K.write_csv(os.path.join(out, F_SESSIONS),
        ["booking_id", "case_id", "crm_account_id", "session_type", "host", "start_utc", "duration_min", "status", "attendees"], rows)
    # the team roster as HR holds it: a row for each pod a specialist has worked in, with its dates
    rr_ = K.rng(36)
    rows = []
    for name, spans, d0, d1 in ROSTER:
        eid = "E%04d" % (1000 + int(rr_.integers(0, 9000)))
        title = "Senior Implementation Specialist" if (K.DATA_END - d0).days >= 3 * 365 else "Implementation Specialist"
        for i, (pod, since) in enumerate(spans):
            frm = since or d0
            to = spans[i + 1][1] - dt.timedelta(days=1) if i + 1 < len(spans) else d1
            rows.append([eid, name, pod, frm.isoformat(), to.isoformat() if to else "", title, d0.isoformat(),
                         d1.isoformat() if d1 else ""])
    rows.sort(key=lambda r: (r[6], r[1], r[3]))
    n[F_ROSTER] = K.write_csv(os.path.join(out, F_ROSTER), ["employee_id", "name", "pod", "pod_from", "pod_to", "title",
                                                             "started_on", "left_on"], rows)
    # satisfaction survey after go-live (a distractor for the pod decision)
    r_ = K.rng(31)
    rows = []
    k = 0
    for cs in O["cases"]:
        if not cs.get("go_live") or r_.random() > 0.62:
            continue
        sent = cs["go_live"] + dt.timedelta(days=int(r_.integers(1, 4)))
        if sent > K.DATA_END:
            continue
        resp = sent + dt.timedelta(days=int(r_.integers(0, 12)))
        if resp > K.DATA_END:
            continue
        k += 1
        score = int(r_.choice([5, 4, 3, 2, 1], p=[0.46, 0.33, 0.12, 0.06, 0.03]))
        nps = int(np.clip(round(score * 2 + r_.normal(0, 1.2)), 0, 10))
        rows.append(["R%06d" % (500000 + k * 3 + int(r_.integers(0, 3))), cs["case_id"], sent.isoformat(), resp.isoformat(), score, nps])
    n[F_CSAT] = K.write_csv(os.path.join(out, F_CSAT),
        ["response_id", "case_id", "survey_sent_on", "responded_on", "onboarding_score_1_5", "likely_to_recommend_0_10"], rows)
    return n
