"""The Office on Aging's service records for the area plan's service table: the home-delivered meal clients and their
episodes, the state participant registry's identifiers and its death match, and the route tablets' delivery log for
FY2026 (1 October 2025 to 30 September 2026).

How the records come to be:
- A client is enrolled by the provider whose area the client lives in at enrolment; the roster keeps that enrolling
  provider. The 2023 redraw moved the town edges to the rural areas, so a client enrolled before July 2023 on a moved
  block is now another provider's responsibility while the roster still shows the enrolling provider.
- The state registry issues a participant number at registration; a client who left the program for more than a year
  and came back was registered again under a new number, and the registry links the old number to the new one. The
  state's monthly death match runs against every number the registry ever issued and reports the number it matched,
  which for a re-registered client is often the old one. Case workers close an episode when the family calls or at the
  quarterly review, so a death can sit in the match file for weeks before the episode closes.
- Drivers record every stop on a route tablet that uploads in batches. After the January 2026 app update some tablets
  re-sent a whole day's stops on reconnecting, under new delivery numbers; clients on the two-meal plan get two hot
  meals at one stop, recorded as two rows. In spring 2026 a Wickmoor route covered a North Kelvane route while its
  driver was out; the log records the route's provider.
"""
import datetime as dt

import numpy as np

import world as W

PROVIDERS = [  # code, name, provider area, routes
    ("WMS", "Wickmoor Senior Services", "Wickmoor City", 9),
    ("FCC", "Fallowmere Community Center", "Fallowmere Town", 4),
    ("NKS", "North Kelvane Senior Center", "North Kelvane", 2),
    ("EKS", "East Kelvane Senior Center", "East Kelvane", 2),
    ("SKS", "South Kelvane Senior Center", "South Kelvane", 2),
    ("WKS", "West Kelvane Senior Center", "West Kelvane", 2),
]
CODE = {a: c for c, n, a, r in PROVIDERS}
MEALS = {"HOT": 1, "FRZ2": 2, "FRZ7": 7, "SHS3": 3}
HOLIDAYS = [dt.date(2025, 10, 13), dt.date(2025, 11, 11), dt.date(2025, 11, 27), dt.date(2025, 12, 25),
            dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25),
            dt.date(2026, 7, 3), dt.date(2026, 9, 7)]
STORM_PACKS = [dt.date(2025, 12, 10), dt.date(2026, 1, 23)]     # shelf-stable packs before forecast storms
REPLAY_FIRST, REPLAY_LAST = dt.date(2026, 1, 12), dt.date(2026, 4, 3)
LOAN_FIRST, LOAN_LAST = dt.date(2026, 3, 30), dt.date(2026, 5, 22)  # a Wickmoor route covers a North Kelvane route


def days(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


REVIEWS = [dt.date(y, m, 15) for y in range(2017, 2028) for m in (1, 4, 7, 10)]
SUSPENDED = [dt.date(2026, 7, 15)]          # the July 2026 case review was not held (two case managers out)


def close_after_death(death, rng):
    """A family's call closes the episode within two weeks; otherwise the next quarterly case review does. An episode
    closed after the planning department's pull is still open in the roster it pulled."""
    if rng.random() < 0.55:
        closed = death + dt.timedelta(days=int(rng.integers(2, 15)))
    else:
        closed = min(r for r in REVIEWS if r > death and r not in SUSPENDED)
    if closed > W.PULL:
        return None, ""
    return closed, "Deceased"


def match_run(death):
    """The state's death match runs on the 5th of each month and finds deaths up to three days before the run."""
    d = dt.date(death.year, death.month, 5)
    while d < death + dt.timedelta(days=3):
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 5)
    return d


def simulate(blocks, old_area, rng):
    """Clients, episodes, registry links, death match rows and the delivery log. old_area maps a block index to its
    provider area before the 2023 redraw."""
    sen = np.array([sum(b["cells"][s * 23 + a] for s in (0, 1) for a in W.A60) for b in blocks], float)
    ok = np.array([b["hu"] > 0 for b in blocks])
    clients, episodes, links, deaths = [], [], [], []
    sid = iter(range(4100000, 4999999, 7))
    kid = iter(range(10001, 99999, 3))
    for area in W.AREAS:
        idx = np.where(ok & np.array([b["area"] == area for b in blocks]))[0]
        w = sen[idx] / sen[idx].sum()
        rate = 0.034 if area in W.TOWN_AREAS else 0.052
        n = int(round(sen[idx].sum() * rate * 1.45))       # clients served at some time since FY2025
        for _ in range(n):
            j = int(idx[rng.choice(len(idx), p=w)])
            cid = "K%05d" % next(kid)
            frozen = rng.random() < (0.32 if area in W.RURAL_AREAS else 0.09)
            plan = 2 if (not frozen and rng.random() < 0.16) else 1
            weekend = (not frozen) and rng.random() < 0.42
            enrolled = dt.date(2017, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3500)))
            lapse = enrolled < dt.date(2021, 6, 1) and rng.random() < 0.45
            prior = None
            if lapse:   # an earlier registration and a lapse of more than a year before this episode
                prior = "SP%07d" % next(sid)
                enrolled = max(enrolled, dt.date(2022, 3, 1)) + dt.timedelta(days=int(rng.integers(0, 900)))
            current = "SP%07d" % next(sid)
            if prior:
                links.append(dict(prior_id=prior, current_id=current,
                                  linked_on=enrolled + dt.timedelta(days=int(rng.integers(1, 20)))))
            # the episode's end: still open, closed for a reason, or ended by a death (hazard 14 per cent a year)
            end, reason = None, ""
            if rng.random() < 0.27:
                end = enrolled + dt.timedelta(days=int(rng.integers(60, 1600)))
                reason = str(rng.choice(["Moved to nursing facility", "Declined service", "Moved out of county",
                                         "No longer eligible"]))
            death = enrolled + dt.timedelta(days=int(rng.exponential(365.25 / 0.14)))
            if death > W.PULL or (end and end <= death):
                death = None
            if end and end > W.PULL:
                end, reason = None, ""
            closed = end
            if death:
                closed, reason = close_after_death(death, rng)
                matched = prior if (prior and rng.random() < 0.75) else current
                deaths.append(dict(state_id=matched, date_of_death=death, match_run=match_run(death)))
            enrol_area = old_area[j] if enrolled < W.REDRAW else blocks[j]["area"]
            clients.append(dict(client_id=cid, block=j, area=blocks[j]["area"], enrol_provider=CODE[enrol_area],
                                state_id=current, prior_id=prior, plan=plan, frozen=frozen, weekend=weekend,
                                birth_year=int(rng.integers(1924, 1965))))
            episodes.append(dict(client_id=cid, enrolled=enrolled, closed=closed, reason=reason,
                                 provider=CODE[enrol_area], meals_per_day=plan,
                                 schedule="Weekly frozen" if frozen else ("Weekday hot + weekend pack" if weekend
                                                                           else "Weekday hot"),
                                 death=death))
    place_unreported_deaths(clients, episodes, links, deaths, rng)
    return clients, episodes, links, deaths


def place_unreported_deaths(clients, episodes, links, deaths, rng, need=None):
    """Every provider carries at least one re-registered client who died in August or September 2026, whose family
    did not call and whose death the state matched to the client's earlier registry number: with the July review not
    held, the episode is still open in the roster on 30 September."""
    need = need or {a: (2 if a in W.TOWN_AREAS else 1) for a in W.AREAS}
    ep = {e["client_id"]: e for e in episodes}
    have = {a: 0 for a in W.AREAS}
    prior_ids = {d["state_id"] for d in deaths}
    for c in clients:
        e = ep[c["client_id"]]
        if (c["prior_id"] and c["prior_id"] in prior_ids and e["death"] and e["death"] <= W.AS_OF
                and (e["closed"] is None or e["closed"] > W.AS_OF)):
            have[c["area"]] += 1
    sid = iter(range(4100003, 4999999, 7))
    for a in W.AREAS:
        pool = [c for c in clients if c["area"] == a and not ep[c["client_id"]]["death"]
                and ep[c["client_id"]]["enrolled"] < dt.date(2025, 6, 1) and ep[c["client_id"]]["closed"] is None]
        pool.sort(key=lambda c: c["client_id"])
        order = [pool[i] for i in rng.permutation(len(pool))]
        for c in order[:max(0, need[a] - have[a])]:
            e = ep[c["client_id"]]
            if not c["prior_id"]:
                c["prior_id"] = "SP%07d" % (next(sid) + 1)
                links.append(dict(prior_id=c["prior_id"], current_id=c["state_id"],
                                  linked_on=e["enrolled"] + dt.timedelta(days=int(rng.integers(1, 20)))))
            death = dt.date(2026, 8, 1) + dt.timedelta(days=int(rng.integers(0, 55)))
            e["death"], e["closed"], e["reason"] = death, None, ""
            deaths.append(dict(state_id=c["prior_id"], date_of_death=death, match_run=match_run(death)))


def place_october_deaths(clients, episodes, deaths, rng, n=2):
    """Clients alive and served on 30 September who died on 1 or 2 October 2026: the state matched them in its October
    run, after the day the area plan counts."""
    ep = {e["client_id"]: e for e in episodes}
    pool = [c for c in sorted(clients, key=lambda c: c["client_id"]) if ep[c["client_id"]]["closed"] is None
            and not ep[c["client_id"]]["death"] and ep[c["client_id"]]["enrolled"] < dt.date(2026, 6, 1)]
    areas = []
    for k in rng.permutation(len(pool)):
        c = pool[int(k)]
        if c["area"] in areas:
            continue
        e = ep[c["client_id"]]
        death = dt.date(2026, 10, 1) + dt.timedelta(days=int(rng.integers(0, 2)))
        e["death"] = death
        e["closed"], e["reason"] = close_after_death(death, rng)
        deaths.append(dict(state_id=c["state_id"], date_of_death=death, match_run=match_run(death)))
        areas.append(c["area"])
        if len(areas) == n:
            break


def statewide_noise(rng, taken, n=5200, last_run=dt.date(2026, 10, 5)):
    """Death match rows for participants of other counties: the state file is statewide. No number the registry gave
    a Kelvane client is used."""
    out = []
    sid = iter(range(4000003, 4999999, 11))
    while len(out) < n:
        s = "SP%07d" % next(sid)
        if s in taken:
            continue
        d = dt.date(2025, 6, 1) + dt.timedelta(days=int(rng.integers(0, 490)))
        run = match_run(d)
        if run < dt.date(2025, 7, 5) or run > last_run:
            continue
        out.append(dict(state_id=s, date_of_death=d, match_run=run))
    return out


def deliveries(clients, episodes, rng):
    """The tablets' delivery log for FY2026: one row per meal item handed over, plus the replayed days."""
    rows = []
    routes = {}
    for code, name, area, nr in PROVIDERS:
        routes[code] = ["%s-%02d" % (code, k + 1) for k in range(nr)]
    ep = {e["client_id"]: e for e in episodes}
    route_of = {}
    for c in clients:
        route_of[c["client_id"]] = routes[CODE[c["area"]]][int(rng.integers(0, len(routes[CODE[c["area"]]])))]
    loan_route = "WMS-%02d" % len(routes["WMS"])
    did = iter(range(1000001, 9999999))
    for d in days(W.FY_FIRST, W.FY_LAST):
        if d.weekday() >= 5 or d in HOLIDAYS:
            continue
        for c in clients:
            e = ep[c["client_id"]]
            stop = e["closed"] if e["closed"] else dt.date(2099, 1, 1)
            if e["death"]:
                stop = min(stop, e["death"])
            if not (e["enrolled"] <= d < stop):
                continue
            route = route_of[c["client_id"]]
            if route == "NKS-01" and LOAN_FIRST <= d <= LOAN_LAST:
                route = loan_route
            items = []
            if d in STORM_PACKS:
                items.append("SHS3")
            if c["frozen"]:
                if d.weekday() == 1:
                    items.append("FRZ7")
            else:
                items += ["HOT"] * c["plan"]
                if c["weekend"] and d.weekday() == 4:
                    items.append("FRZ2")
            for it in items:
                rows.append(dict(client_id=c["client_id"], route=route, provider_code=route[:3], date=d, item=it))
    # tablet upload times and the replayed days. A stop's items upload with the stop; a second hot meal is logged with
    # the first or, on some routes, at the end of the run; a tablet out of signal uploads the day when it reconnects;
    # after the January 2026 update a tablet that lost its session re-sent the day, sometimes minutes later, sometimes
    # the next morning.
    out = []
    by_day = {}
    for r in rows:
        by_day.setdefault((r["route"], r["date"]), []).append(r)
    tablet = {}
    for (route, d), rs in sorted(by_day.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        tab = tablet.setdefault(route, "TB-%04d" % (2100 + 37 * len(tablet)))
        base = dt.datetime.combine(d, dt.time(10, 20)) + dt.timedelta(minutes=int(rng.integers(0, 150)))
        offline = rng.random() < 0.12
        reconnect = dt.datetime.combine(d, dt.time(15, 40)) + dt.timedelta(minutes=int(rng.integers(0, 260)))
        late_entry = rng.random() < 0.3
        stamped = []
        seen = {}
        for k, r in enumerate(rs):
            nth = seen.get((r["client_id"], r["item"]), 0)
            seen[(r["client_id"], r["item"])] = nth + 1
            up = base + dt.timedelta(minutes=3 * k + int(rng.integers(0, 2)), seconds=int(rng.integers(0, 60)))
            if nth and late_entry:
                up = base + dt.timedelta(minutes=3 * len(rs) + int(rng.integers(5, 70)), seconds=int(rng.integers(0, 60)))
            if offline:
                up = max(up, reconnect + dt.timedelta(seconds=k))
            stamped.append((r, up))
        for r, up in stamped:
            out.append(dict(r, delivery_id="D%07d" % next(did), uploaded_at=up, tablet=tab, replay=False))
        if REPLAY_FIRST <= d <= REPLAY_LAST and rng.random() < 0.075:
            last = max(up for _, up in stamped)
            again = last + dt.timedelta(minutes=int(rng.choice([2, 4, 7, 15, 40, 95, 240, 600, 1100])))
            for k, (r, up) in enumerate(stamped):
                out.append(dict(r, delivery_id="D%07d" % next(did), uploaded_at=again + dt.timedelta(seconds=k),
                                tablet=tab, replay=True))
    return out


# ---------------------------------------------------------------- the two asks, by route
def meals(rows, clients, by="client", dedup="plan"):
    """FY2026 home-delivered meals by provider area. by: 'client' (the provider responsible for the client) or
    'route' (the provider operating the route); dedup: 'plan' (a client-day item counted up to the plan's meals),
    'none' (every row) or 'all' (one row per client, day and item)."""
    plan = {c["client_id"]: c["plan"] for c in clients}
    area = {c["client_id"]: c["area"] for c in clients}
    route_area = {code: a for code, n, a, r in PROVIDERS}
    groups = {}
    for r in rows:
        k = (r["client_id"], r["date"], r["item"])
        groups.setdefault(k, []).append(r)
    out = dict.fromkeys(W.AREAS, 0)
    for (cid, d, item), rs in groups.items():
        if dedup == "none":
            n = len(rs)
        elif dedup == "all":
            n = 1
        else:
            n = min(len(rs), plan[cid] if item == "HOT" else 1)
        for r in rs[:n]:
            a = area[cid] if by == "client" else route_area[r["provider_code"]]
            out[a] += MEALS[item]
    return out


def active(clients, episodes, links, deaths, by="area", chain=True, cutoff=True):
    """Clients with an open home-delivered meal episode on 30 September 2026 who were alive that day, by provider
    area. by: 'area' (the block's provider area as drawn since July 2023) or 'roster' (the enrolling provider);
    chain: follow a death matched to a prior registry number to the client; cutoff: a death counts only if on or
    before 30 September 2026."""
    code_area = {code: a for code, n, a, r in PROVIDERS}
    to_current = {l["prior_id"]: l["current_id"] for l in links}
    died = {}
    for d in deaths:
        sid = d["state_id"]
        if chain and sid in to_current:
            sid = to_current[sid]
        if cutoff and d["date_of_death"] > W.AS_OF:
            continue
        died[sid] = d["date_of_death"]
    ep = {e["client_id"]: e for e in episodes}
    out = dict.fromkeys(W.AREAS, 0)
    for c in clients:
        e = ep[c["client_id"]]
        if not (e["enrolled"] <= W.AS_OF and (e["closed"] is None or e["closed"] > W.AS_OF)):
            continue
        if c["state_id"] in died:
            continue
        a = c["area"] if by == "area" else code_area[e["provider"]]
        out[a] += 1
    return out
