"""The golden from the pack: each region's share of sampled members who worked 80 hours or more in March 2026 from the
callback model fitted to every sampled member's call history (answer rates by work class and calling window, pooled
across regions; class shares by region), the four lowest regions, and the two planning figures for 1 October 2026."""
import datetime as dt

import common as K
import models as M
import pack as P

D1 = K.ROSTER_DATE
PARENT_ROLES = ("HOH", "SPOUSE", "CARETAKER_RELATIVE")


def age_on(born, on):
    return on.year - born.year - ((on.month, on.day) < (born.month, born.day))


def call(target):
    S = P.survey(target)
    hist = P.histories(S)
    SS = M.summarise(hist)
    share, p, it = M.em(SS)
    order = sorted(range(10), key=lambda i: share[i])
    return dict(S=S, hist=hist, SS=SS, share=share, p=p, iterations=it, four=sorted(order[:4]), fifth=order[4],
                order=order)


def covered_oct1(target):
    """Each member covered on 1 October 2026 and aged 19 to 64 that day, with the county lived in that day. A member
    is covered if the roster's enrollment began by 1 October and has not ended before it, or if a termination in the
    log ended coverage on or after 1 October without an October enrollment before it; the county that day is the
    roster's, or the county before the first move logged after 1 October, or the county on the termination."""
    roster, log, cases = P.enrollment(target)
    ev = {}
    for r in sorted(log, key=lambda r: (r["at"], r["member_id"], r["change"])):
        ev.setdefault(r["member_id"], []).append(r)
    people = {}
    on_roster = {r["member_id"]: r for r in roster}
    for mid, r in on_roster.items():
        evs = ev.get(mid, [])
        adds = [e for e in evs if e["change"] == "ADD"]
        terms = [e for e in evs if e["change"] == "TERM" and e["eff"] >= D1]
        reinstated = any(e["change"] == "REINSTATE" for e in evs)
        early_term = [e for e in evs if e["change"] == "TERM" and e["eff"] < D1]
        cov = (r["begin"] <= D1 and (r["end"] is None or r["end"] >= D1)
               and (not early_term or reinstated))
        if not cov and adds and terms and min(terms, key=lambda e: e["at"])["at"] < min(adds, key=lambda e: e["at"])["at"]:
            cov = True                         # covered on 1 October, ended in October, enrolled again since
        if not cov:
            continue
        moves = sorted((e for e in evs if e["change"] == "ADDRESS" and e["eff"] > D1), key=lambda e: e["eff"])
        county = moves[0]["county_before"] if moves else r["county"]
        people[mid] = dict(p1=r["p1_client_id"], born=r["born"], county=county)
    for mid, evs in ev.items():
        if mid in on_roster:
            continue
        terms = [e for e in evs if e["change"] == "TERM" and e["eff"] >= D1]
        adds = [e for e in evs if e["change"] == "ADD"]
        if not terms or adds:
            continue                           # ended before 1 October, or joined in October
        e = terms[0]
        people[mid] = dict(p1=e["p1_client_id"], born=e["born"], county=e["county_before"])
    return {mid: v for mid, v in people.items() if 19 <= age_on(v["born"], D1) <= 64}


def planning(target, people=None):
    """Ask A: members covered by region of the county they lived in on 1 October. Ask B: of them, case heads, spouses
    and caretaker relatives in a case with a child under 14 in it on 1 October."""
    region_of = P.regions(target)
    people = covered_oct1(target) if people is None else people
    roster, log, cases = P.enrollment(target)
    by_case = {}
    for r in cases:
        by_case.setdefault(r["case_id"], []).append(r)
    parent_cases = {}
    for r in cases:
        if r["case_role"] in PARENT_ROLES and r["begin"] <= D1 and (r["end"] is None or r["end"] >= D1):
            parent_cases.setdefault(r["p1_client_id"], set()).add(r["case_id"])

    def child_under_14(case):
        return any(k["case_role"] == "CHILD" and k["begin"] <= D1 and (k["end"] is None or k["end"] >= D1)
                   and k["born"] <= D1 and age_on(k["born"], D1) < 14 for k in by_case[case])

    a = {c: 0 for c in K.CODES}
    b = {c: 0 for c in K.CODES}
    for mid, v in people.items():
        code = region_of[v["county"]]
        a[code] += 1
        if any(child_under_14(c) for c in parent_cases.get(v["p1"], ())):
            b[code] += 1
    return a, b


def run(target):
    c = call(target)
    a, b = planning(target)
    return dict(call=c, a=a, b=b)
