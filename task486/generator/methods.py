"""The ways an analyst turns the linkage unit's findings and the sources' activity into the people served in FY2026,
each attributed to one recipient, and the 2027 fund split on them.

The golden resolves the unit's LINK findings into people by taking them strongest first and refusing any that would
put two records of one source in one person (each source holds a person once), so a chain that would join two clients
one source keeps apart is cut at its weakest finding. The default path merges every chain (connected components)."""
import collections
import datetime as dt

import numpy as np

import world as W

HOMELESS_STATUS = ("Street", "Homeless Shelter", "Transitional")     # the policy's street, shelter or transitional
QUARTERS = [(dt.date(2025, 10, 1), dt.date(2025, 12, 31)), (dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            (dt.date(2026, 4, 1), dt.date(2026, 6, 30)), (dt.date(2026, 7, 1), dt.date(2026, 9, 30))]


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
        # a stay's nights run from its first night to the night before the day it ended
        if s["start"] <= hi and s["end"] > lo:
            act[i]["active"] = True
            act[i]["dv"] = True
    site_coc = {"WSH-01": "HAL", "WSH-02": "HAL", "WSH-05": "HAL", "WSH-03": "MEL", "WSH-04": "OND", "WSH-MP": "PYR"}
    for e in world.encounters:
        if lo <= e["date"] <= hi and e["status"] in HOMELESS_STATUS:
            i = key[("WSH", e["pid"])]
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
                a["last_other"], a["other_coc"] = c["date"], "HAL"
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


def partitions(records, comp, sub):
    """Every split of a linked group into people that puts no two records of one source in one person and keeps each
    person joined by the unit's links: the space every licensed resolution chooses from."""
    m = len(comp)
    src = [records[g]["src"] for g in comp]
    pos = {g: k for k, g in enumerate(comp)}
    adj = [set() for _ in range(m)]
    for i, j, s in sub:
        adj[pos[i]].add(pos[j])
        adj[pos[j]].add(pos[i])
    out, lab, used = [], [0] * m, []

    def joined():
        for c in range(len(used)):
            mem = [k for k in range(m) if lab[k] == c]
            seen, todo = {mem[0]}, [mem[0]]
            while todo:
                x = todo.pop()
                for y in adj[x]:
                    if lab[y] == c and y not in seen:
                        seen.add(y)
                        todo.append(y)
            if len(seen) != len(mem):
                return False
        return True

    def rec(k):
        if k == m:
            if joined():
                out.append(tuple(lab))
            return
        for c in range(len(used) + 1):
            if c < len(used) and src[k] in used[c]:
                continue
            lab[k] = c
            if c == len(used):
                used.append({src[k]})
                rec(k + 1)
                used.pop()
            else:
                used[c].add(src[k])
                rec(k + 1)
                used[c].discard(src[k])
    rec(0)
    return out


def family(records, comp, sub, score, rng, trials=12):
    """The licensed resolutions of one linked group, each as the people it returns (record to root): strongest first
    under every order of equal links, and every optimum of three objectives over the constrained splits (the summed
    score of the links kept inside people, the summed score less the threshold of every pair returned inside people
    with an unreturned pair at the floor less the threshold, and the fewest people)."""
    out = []
    base = sorted(sub, key=lambda t: (-t[2], t[0], t[1]))
    out.append(("strongest first", _local_resolve(records, comp, sub, base)))
    for t in range(trials):
        order = sorted(sub, key=lambda l: (-l[2], rng.random()))
        out.append(("strongest first, ties shuffled", _local_resolve(records, comp, sub, order)))
    parts = partitions(records, comp, sub)
    m = len(comp)
    floor = 4.0 - W.THRESHOLD
    pos = {g: k for k, g in enumerate(comp)}
    pair_v = {}
    for a in range(m):
        for b in range(a + 1, m):
            sc = score.get((min(comp[a], comp[b]), max(comp[a], comp[b])))
            pair_v[(a, b)] = (sc - W.THRESHOLD) if sc is not None and sc >= 4.0 else floor
    objectives = {
        "most link score kept": lambda lab: sum(s for i, j, s in sub if lab[pos[i]] == lab[pos[j]]),
        "most pair evidence kept": lambda lab: sum(v for (a, b), v in pair_v.items() if lab[a] == lab[b]),
        "fewest people": lambda lab: -len(set(lab)),
    }
    for name, f in objectives.items():
        vals = [f(lab) for lab in parts]
        top = max(vals)
        for lab, v in zip(parts, vals):
            if v >= top - 1e-9:
                out.append((name, {comp[k]: comp[lab.index(lab[k])] for k in range(m)}))
    return out


def family_sensitive(world, links, pairs, act=None, trials=12, max_records=10):
    """People whose identity is redrawn because some licensed resolution of their linked group returns other people
    served, or other recipients, than the people actually served there."""
    act = act or record_activity(world)
    rng = np.random.default_rng(7)
    score = {(min(i, j), max(i, j)): s for i, j, s, c in pairs}
    comps = components(len(world.records), links)
    by_rec = collections.defaultdict(list)
    for l in links:
        by_rec[l[0]].append(l)
    bad = []
    for comp in comps:
        by_src = collections.Counter(world.records[i]["src"] for i in comp)
        if all(v == 1 for v in by_src.values()):
            continue
        cnt = collections.Counter(world.records[i]["pid"] for i in comp)
        top = cnt.most_common(1)[0][0]
        if len(comp) > max_records:
            bad.extend(q for q in cnt if q != top)
            continue
        cset = set(comp)
        sub = [l for i in comp for l in by_rec[i] if l[1] in cset]
        truth = {i: world.records[i]["pid"] for i in comp}
        ref = tuple(sorted(people_served_sub(world, truth, act, comp).values()))
        members = family(world.records, comp, sub, score, rng, trials)
        # the same resolution over only the records that show FY2026 service
        live = [i for i in comp if act[i]["active"]]
        lset = set(live)
        lsub = sorted((l for l in sub if l[0] in lset and l[1] in lset), key=lambda t: (-t[2], t[0], t[1]))
        lroots = {i: i for i in comp}
        if live:
            lroots.update(_local_resolve(world.records, live, lsub, lsub))
        members.append(("strongest first, FY2026 records only", lroots))
        for name, roots in members:
            if tuple(sorted(people_served_sub(world, roots, act, comp).values())) != ref:
                bad.extend(q for q in cnt if q != top)
                break
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
def _quarter(d):
    for q, (a, b) in enumerate(QUARTERS):
        if a <= d <= b:
            return q
    return None


def shelter_nights(world, dedup=True, nbn_by_beds=True, drop_earlier=False):
    """Nights people spent in each Continuum's emergency shelters (night by night included) and safe havens in each
    quarter of FY2026. A stay's nights run from its entry date to the night before its exit (an open stay to the
    night of 30 September 2026); at the night-by-night shelter a night is a bed-night service. A person spends a night
    in one place, so a night two of a person's stays both cover (a stay left open after the client moved on) counts
    once. drop_earlier is the over-cleaning read: the earlier of two overlapping stays is dropped as a duplicate."""
    lo, hi = W.FY26
    stays = [e for e in world.enrollments if e["kind"] in ("ES", "SH") or (e["kind"] == "NBN" and not nbn_by_beds)]
    if drop_earlier:
        by = collections.defaultdict(list)
        for e in stays:
            by[(e["coc"], e["pid"])].append(e)
        gone = set()
        for lst in by.values():
            lst.sort(key=lambda e: (e["entry"], e["eid"]))
            for a, b in zip(lst, lst[1:]):
                if a["exit"] is None or a["exit"] > b["entry"]:
                    gone.add(a["eid"])
        stays = [e for e in stays if e["eid"] not in gone]
    nights = collections.defaultdict(set) if dedup else collections.Counter()
    for e in stays:
        end = e["exit"] if e["exit"] is not None else hi + dt.timedelta(days=1)
        a, b = max(e["entry"], lo), min(end, hi + dt.timedelta(days=1))
        for k in range((b - a).days):
            d = a + dt.timedelta(days=k)
            if dedup:
                nights[e["coc"]].add((e["pid"], d))
            else:
                nights[(e["coc"], _quarter(d))] += 1
    if nbn_by_beds:
        for n in world.bed_nights:
            if lo <= n["date"] <= hi:
                if dedup:
                    nights[n["coc"]].add((n["pid"], n["date"]))
                else:
                    nights[(n["coc"], _quarter(n["date"]))] += 1
    out = {}
    for c in W.COCS:
        if dedup:
            q = collections.Counter(_quarter(d) for p, d in nights[c])
            out[c] = [q.get(k, 0) for k in range(4)]
        else:
            out[c] = [nights.get((c, k), 0) for k in range(4)]
    return out


def rrh_waits(world, chain="pid", rows="hoh"):
    """For each Continuum and the region, the average days from a household's entry into rapid re-housing to its
    move-in, over the households that moved in during FY2026. A household that leaves one rapid re-housing project
    and enters another of the Continuum on the same day has not left rapid re-housing, so its entry is the first
    project's. chain None reads each move-in from its own enrollment's entry; chain "hoh" follows a move only through
    the head of household's own earlier enrollments as head; chain "pid" follows it through the same person's earlier
    enrollment in any role. rows "all" counts every enrollment carrying a move-in date (Ondrava writes the household's
    date on every member)."""
    lo, hi = W.FY26
    rrh = [e for e in world.enrollments if e["kind"] == "RRH"]
    exits = collections.defaultdict(list)
    for e in rrh:
        if e["exit"] is not None:
            exits[(e["coc"], e["pid"], e["exit"])].append(e)
    waits = collections.defaultdict(list)
    for e in rrh:
        mi = e["move_in"] if e["rel"] == 1 else (world.member_move_in.get(e["eid"]) if rows == "all" else None)
        if mi is None or not (lo <= mi <= hi):
            continue
        start = e["entry"]
        if chain is not None:
            cur = e
            while True:
                prev = [x for x in exits.get((cur["coc"], cur["pid"], start), ())
                        if x["eid"] != cur["eid"] and (chain == "pid" or (x["rel"] == 1 and cur["rel"] == 1))]
                if not prev:
                    break
                cur = prev[0]
                start = cur["entry"]
        waits[e["coc"]].append((mi - start).days)
    out = {c: round(sum(waits[c]) / len(waits[c]), 6) for c in W.COCS}
    allw = [d for c in W.COCS for d in waits[c]]
    out["ALL"] = round(sum(allw) / len(allw), 6)
    out["n"] = {c: len(waits[c]) for c in W.COCS}
    return out
