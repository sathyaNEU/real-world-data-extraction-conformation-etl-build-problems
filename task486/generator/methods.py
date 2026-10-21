"""The ways an analyst turns the linkage unit's findings and the sources' activity into the people served in FY2026,
each attributed to one recipient, and the 2027 fund split on them.

The golden resolves the unit's LINK findings into people by taking them strongest first and refusing any that would
put two records of one source in one person (each source holds a person once), so a chain that would join two clients
one source keeps apart is cut at its weakest finding. The default path merges every chain (connected components)."""
import collections
import datetime as dt

import numpy as np

import world as W


def components(n, links):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for i, j, s in links:
        a, b = f(i), f(j)
        if a != b:
            par[a] = b
    groups = collections.defaultdict(list)
    for i in range(n):
        groups[f(i)].append(i)
    return [g for g in groups.values() if len(g) > 1]


def resolve(records, links, constrained=True, order=None, min_score=None):
    """Root of each record. Links taken strongest first (ties by key order unless an order is given); with
    constrained, a link that would put two records of one source in one person is refused."""
    n = len(records)
    par = list(range(n))
    srcs = [{records[i]["src"]} for i in range(n)]

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    seq = order if order is not None else sorted(links, key=lambda t: (-t[2], t[0], t[1]))
    for i, j, s in seq:
        if min_score is not None and s < min_score:
            continue
        a, b = f(i), f(j)
        if a == b:
            continue
        if constrained and (srcs[a] & srcs[b]):
            continue
        par[a] = b
        srcs[b] |= srcs[a]
    return [f(i) for i in range(n)]


def quarantine(records, links):
    """Over-cleaning: every record in a chain that would join two records of one source loses all its links."""
    comps = components(len(records), links)
    bad = set()
    for comp in comps:
        by_src = collections.Counter(records[i]["src"] for i in comp)
        if any(v > 1 for v in by_src.values()):
            deg = collections.Counter()
            for i, j, s in links:
                if i in comp and j in comp:
                    deg[i] += 1
                    deg[j] += 1
            # records linked to two records of one source
            nb = collections.defaultdict(set)
            for i, j, s in links:
                nb[i].add(j)
                nb[j].add(i)
            for i in comp:
                srcs = collections.Counter(records[k]["src"] for k in nb[i])
                if any(v > 1 for v in srcs.values()):
                    bad.add(i)
    kept = [l for l in links if l[0] not in bad and l[1] not in bad]
    return resolve(records, kept, constrained=False)


# ---------------------------------------------------------------------------------------------- activity
def record_activity(world):
    """Per record: whether it shows service in FY2026, and what attribution reads from it."""
    lo, hi = W.FY26
    key = {(r["src"], r["pid"]): i for i, r in enumerate(world.records)}
    act = [dict(active=False, hmis_entry=None, hmis_coc=None, dv=False, last_other=None, other_coc=None)
           for _ in world.records]
    for e in world.enrollments:
        i = key[("HMIS-" + e["coc"], e["pid"])]
        if e["entry"] <= hi and (e["exit"] is None or e["exit"] >= lo):
            a = act[i]
            a["active"] = True
            if a["hmis_entry"] is None or e["entry"] > a["hmis_entry"]:
                a["hmis_entry"], a["hmis_coc"] = e["entry"], e["coc"]
    for s in world.dv_stays:
        i = key[("DVC", s["pid"])]
        if s["start"] <= hi and s["end"] >= lo:
            act[i]["active"] = True
            act[i]["dv"] = True
    site_coc = {"VSM-01": "CAL", "VSM-02": "CAL", "VSM-05": "CAL", "VSM-03": "MAR", "VSM-04": "OST", "VSM-MP": "PEL"}
    for e in world.encounters:
        if lo <= e["date"] <= hi and e.get("homeless", True):
            i = key[("VSM", e["pid"])]
            a = act[i]
            a["active"] = True
            if a["last_other"] is None or e["date"] > a["last_other"]:
                a["last_other"], a["other_coc"] = e["date"], site_coc[e["site"]]
    for c in world.contacts:
        if lo <= c["date"] <= hi:
            i = key[("HOT", c["pid"])]
            a = act[i]
            a["active"] = True
            if a["last_other"] is None or c["date"] > a["last_other"]:
                a["last_other"], a["other_coc"] = c["date"], "CAL"
    return act


def people_served(world, roots, act):
    """The people active in FY2026 (by root) and the recipient each is attributed to."""
    groups = collections.defaultdict(list)
    for i, r in enumerate(roots):
        groups[r].append(i)
    out = {}
    for root, idx in groups.items():
        if not any(act[i]["active"] for i in idx):
            continue
        hm = [(act[i]["hmis_entry"], act[i]["hmis_coc"]) for i in idx if act[i]["hmis_entry"] is not None]
        if hm:
            out[root] = max(hm)[1]
        elif any(act[i]["dv"] for i in idx):
            out[root] = "DVC"
        else:
            ot = [(act[i]["last_other"], act[i]["other_coc"]) for i in idx if act[i]["last_other"] is not None]
            out[root] = max(ot)[1]
    return out


def counts(served):
    c = collections.Counter(served.values())
    return {k: c.get(k, 0) for k in W.RECIPIENTS}


def allocation(cnt):
    pool = W.FUND_2027 * (1 - W.ADMIN_SHARE)
    total = sum(cnt.values())
    return {k: int(round(pool * cnt[k] / total)) for k in W.RECIPIENTS}


def _local_resolve(records, comp, sub, order):
    pos = {g: k for k, g in enumerate(comp)}
    par = list(range(len(comp)))
    srcs = [{records[g]["src"]} for g in comp]

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for i, j, s in order:
        a, b = f(pos[i]), f(pos[j])
        if a == b or (srcs[a] & srcs[b]):
            continue
        par[a] = b
        srcs[b] |= srcs[a]
    return {g: comp[f(pos[g])] for g in comp}


def tie_sensitive(world, links, trials=12):
    """People whose identity should be redrawn because the golden's people or recipients in their component depend
    on how equal links are ordered, or differ from the people actually served."""
    act = record_activity(world)
    rng = np.random.default_rng(7)
    comps = components(len(world.records), links)
    by_rec = collections.defaultdict(list)
    for l in links:
        by_rec[l[0]].append(l)
    bad = []
    for comp in comps:
        by_src = collections.Counter(world.records[i]["src"] for i in comp)
        if all(v == 1 for v in by_src.values()):
            continue
        cset = set(comp)
        sub = [l for i in comp for l in by_rec[i] if l[1] in cset]
        truth = {i: world.records[i]["pid"] for i in comp}
        ref = tuple(sorted(people_served_sub(world, truth, act, comp).values()))
        seen = set()
        base = sorted(sub, key=lambda t: (-t[2], t[0], t[1]))
        seen.add(tuple(sorted(people_served_sub(world, _local_resolve(world.records, comp, sub, base), act,
                                                comp).values())))
        for t in range(trials):
            order = sorted(sub, key=lambda l: (-l[2], rng.random()))
            seen.add(tuple(sorted(people_served_sub(world, _local_resolve(world.records, comp, sub, order), act,
                                                    comp).values())))
        if len(seen) > 1 or next(iter(seen)) != ref:
            cnt = collections.Counter(world.records[i]["pid"] for i in comp)
            top = cnt.most_common(1)[0][0]
            bad.extend(q for q in cnt if q != top)
    return bad


def people_served_sub(world, roots, act, comp):
    groups = collections.defaultdict(list)
    for i in comp:
        groups[roots[i]].append(i)
    out = {}
    for root, idx in groups.items():
        if not any(act[i]["active"] for i in idx):
            continue
        hm = [(act[i]["hmis_entry"], act[i]["hmis_coc"]) for i in idx if act[i]["hmis_entry"] is not None]
        if hm:
            out[root] = max(hm)[1]
        elif any(act[i]["dv"] for i in idx):
            out[root] = "DVC"
        else:
            ot = [(act[i]["last_other"], act[i]["other_coc"]) for i in idx if act[i]["last_other"] is not None]
            out[root] = max(ot)[1]
    return out


# ---------------------------------------------------------------------------------------------- the asks
def shelter_nights(world, dedup=True, nbn_by_beds=True, inclusive_exit=False):
    """Nights people spent in each Continuum's emergency shelters and safe havens in FY2026. A stay's nights run from
    its entry date to the night before its exit (an open stay to the night of 30 September 2026); at the
    night-by-night shelter a night is a bed-night record."""
    lo, hi = W.FY26
    nights = collections.defaultdict(set) if dedup else collections.Counter()
    for e in world.enrollments:
        if e["kind"] not in ("ES", "SH", "NBN"):
            continue
        if e["kind"] == "NBN" and nbn_by_beds:
            continue
        end = (e["exit"] + dt.timedelta(days=1 if inclusive_exit else 0)) if e["exit"] else hi + dt.timedelta(days=1)
        a, b = max(e["entry"], lo), min(end, hi + dt.timedelta(days=1))
        if b <= a:
            continue
        if dedup:
            for k in range((b - a).days):
                nights[e["coc"]].add((e["pid"], a + dt.timedelta(days=k)))
        else:
            nights[e["coc"]] += (b - a).days
    if nbn_by_beds:
        for n in world.bed_nights:
            if lo <= n["date"] <= hi:
                if dedup:
                    nights[n["coc"]].add((n["pid"], n["date"]))
                else:
                    nights[n["coc"]] += 1
    out = {c: (len(nights[c]) if dedup else nights[c]) for c in W.COCS}
    out["ALL"] = sum(out[c] for c in W.COCS)
    return out


def rrh_move_ins(world, follow_transfers=True, rows="hoh"):
    """For each Continuum, the households that moved into housing from rapid re-housing in FY2026 and the average days
    from each household's entry into rapid re-housing to its move-in (a same-day move from one rapid re-housing
    project to another continues the stay)."""
    lo, hi = W.FY26
    rrh = [e for e in world.enrollments if e["kind"] == "RRH"]
    by_hoh = collections.defaultdict(list)
    for e in rrh:
        if e["rel"] == 1:
            by_hoh[(e["coc"], e["pid"])].append(e)
    days = collections.defaultdict(list)
    for e in rrh:
        mi = e["move_in"] if e["rel"] == 1 else world.member_move_in.get(e["eid"])
        if mi is None or not (lo <= mi <= hi):
            continue
        if rows == "hoh" and e["rel"] != 1:
            continue
        start = e["entry"]
        if follow_transfers:
            hoh = e["pid"] if e["rel"] == 1 else None
            if hoh is not None:
                prev = {x["exit"]: x for x in by_hoh[(e["coc"], hoh)] if x["exit"] is not None}
                while start in prev:
                    start = prev[start]["entry"]
        days[e["coc"]].append((mi - start).days)
    out = {}
    for c in W.COCS:
        out[c] = (len(days[c]), round(sum(days[c]) / len(days[c]), 1) if days[c] else None)
    allv = [d for c in W.COCS for d in days[c]]
    out["ALL"] = (len(allv), round(sum(allv) / len(allv), 1))
    return out
