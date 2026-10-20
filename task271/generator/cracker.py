"""The cracker and the mirror on the cut pack's planning figures, scored against figures.json.

The cracker lands the call and runs the hygiene battery on the enrollment files (one roster row per member, the change
log's lines by member, the extract's rows by person), then rebuilds 1 October the careful way: the roster's members
whose enrollment began by 1 October and has not ended, each at the county before any move logged after 1 October, aged
on 1 October, plus the members the log terminated on or after 1 October who are no longer on the roster; for the
parents and caretakers it reads the extract's count of children under 14 for each case head, spouse and caretaker
relative. The mirror stops off the call and reads the roster as it stands (its county and region, the roster's members
whose enrollment began by 1 October) and the extract's count.

Weights are the skill's: 38 for the call and its components, 7 for instruction-following, 55 for the asks, a figure a
hit at its stated rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import common as K      # noqa: E402
import pack as P        # noqa: E402

D1 = K.ROSTER_DATE


def careful_people(target):
    roster, log, cases = P.enrollment(target)
    ev = {}
    for r in sorted(log, key=lambda r: (r["at"], r["member_id"])):
        ev.setdefault(r["member_id"], []).append(r)
    people = {}
    on = {r["member_id"]: r for r in roster}
    for mid, r in on.items():
        if not (r["begin"] <= D1 and (r["end"] is None or r["end"] >= D1)):
            continue
        moves = sorted((e for e in ev.get(mid, []) if e["change"] == "ADDRESS" and e["eff"] > D1), key=lambda e: e["eff"])
        people[mid] = dict(p1=r["p1_client_id"], born=r["born"], county=moves[0]["county_before"] if moves else r["county"])
    for mid, evs in ev.items():
        if mid in on:
            continue
        terms = [e for e in evs if e["change"] == "TERM" and e["eff"] >= D1]
        if terms and not any(e["change"] == "ADD" for e in evs):
            people[mid] = dict(p1=terms[0]["p1_client_id"], born=terms[0]["born"], county=terms[0]["county_before"])
    return {m: v for m, v in people.items() if 19 <= A.age_on(v["born"], D1) <= 64}


def roster_people(target):
    roster, log, cases = P.enrollment(target)
    out = {}
    for r in roster:
        if r["begin"] <= D1 and 19 <= A.age_on(r["born"], D1) <= 64:
            out[r["member_id"]] = dict(p1=r["p1_client_id"], born=r["born"], county=r["county"])
    return out


def column_parents(target, people):
    """Parents and caretakers by the extract's own count of children under 14 in the case."""
    region_of = P.regions(target)
    roster, log, cases = P.enrollment(target)
    has = {}
    for r in cases:
        if r["case_role"] in A.PARENT_ROLES and int(r["children_under_14_in_case"]) > 0:
            has[r["p1_client_id"]] = True
    b = {c: 0 for c in K.CODES}
    for v in people.values():
        if has.get(v["p1"]):
            b[region_of[v["county"]]] += 1
    return b


def count_a(target, people):
    region_of = P.regions(target)
    a = {c: 0 for c in K.CODES}
    for v in people.values():
        a[region_of[v["county"]]] += 1
    return a


def score(fig, a, b):
    hits = sum(int(a[c] == fig["ask_a"][K.NAME[c]]) for c in K.CODES) + \
        sum(int(b[c] == fig["ask_b"][K.NAME[c]]) for c in K.CODES)
    return hits


def run(target, fig):
    cp = careful_people(target)
    ca, cb = count_a(target, cp), column_parents(target, cp)
    _, cb2 = A.planning(target, cp)                       # the careful population, the children's own dates
    rp = roster_people(target)
    ma, mb = count_a(target, rp), column_parents(target, rp)
    total = 20
    cr, mi = score(fig, ca, cb), score(fig, ma, mb)
    # the pair: the cracker lands the call (38 + 7 + 55 x its ask share), the mirror misses it (about 5 + 7 + ...)
    pair = ((38 + 7 + 55 * cr / total) + (5 + 7 + 55 * mi / total)) / 2
    return dict(cracker=dict(a=ca, b=cb, b_dates=cb2), mirror=dict(a=ma, b=mb), cracker_hits=cr, mirror_hits=mi,
                total=total, pair=pair, b_dates_hits=sum(int(cb2[c] == fig["ask_b"][K.NAME[c]]) for c in K.CODES))


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    out = run(os.path.join(task, "target"), fig)
    print(json.dumps({k: v for k, v in out.items() if k in ("cracker_hits", "mirror_hits", "total", "pair",
                                                            "b_dates_hits")}, indent=1))
