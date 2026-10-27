#!/usr/bin/env python3
"""task464: every graded answer, computed from the generator's own truth.

`golden.py`, `checks.py` and `writeup.py` all read this module, so one arithmetic produces the
deliverables, the assertions and the write-up. `verify.py` recomputes the same answers from the shipped
bundle alone, on its own code path.
"""
import collections
import datetime as dt

import world

H1 = (dt.date(2026, 1, 1), dt.date(2026, 6, 30))
H2 = (dt.date(2026, 7, 1), dt.date(2026, 12, 31))


def call(sites, by_area):
    L = world.ladder(sites, by_area)
    areas = []
    for c in world.CODES:
        slots, req = L["cap"]["R3"][c], L["req"][c]
        areas.append(dict(code=c, name=world.AREA[c]["name"], slots=slots, required=req,
                          meets=slots >= req, shortfall=max(0, req - slots)))
    short = [a for a in areas if not a["meets"]]
    nearest = min(short, key=lambda a: (a["shortfall"], a["code"])) if short else None
    return dict(network=L["tot"]["R3"], areas=areas, short=[a["code"] for a in short],
                nearest=nearest["code"] if nearest else None,
                nearest_shortfall=nearest["shortfall"] if nearest else 0, ladder=L)


def per_site(sites):
    return [dict(site=s["site"], name=s["name"], area=s["area"],
                 area_name=world.AREA[s["area"]]["name"], slots=s["R3"]) for s in
            sorted(sites, key=lambda x: (x["area"], x["site"]))]


def ask_a(sites, extra, rows, oon_main, oon_runout):
    """Out-of-network treatments by the area of the site treated, and the share of all the area's
    treatments in that half. Service-date basis, the run-out supplement included."""
    area_of_site = {}
    for e in extra:
        if e["kind"] == "dropped":
            area_of_site[e["name"]] = e["area"]
    oon = collections.Counter()
    for r in list(oon_main) + list(oon_runout):
        sd = dt.date.fromisoformat(r[3])
        if sd.year != 2026:
            continue
        half = "H1" if sd <= H1[1] else "H2"
        oon[(area_of_site[r[4]], half)] += int(r[11])
    inn = collections.Counter()
    site_area = {s["site"]: s["area"] for s in sites}
    for r in rows:
        if r["date"].year != 2026 or r.get("status", "completed") != "completed":
            continue
        half = "H1" if r["date"] <= H1[1] else "H2"
        inn[(site_area[r["site"]], half)] += 1
    out = []
    for c in world.CODES:
        for half in ("H1", "H2"):
            n = oon[(c, half)]
            tot = n + inn[(c, half)]
            out.append(dict(code=c, name=world.AREA[c]["name"], half=half, treatments=n,
                            all_treatments=tot, share=round(n * 100.0 / tot, 1) if tot else 0.0))
    return out


def ask_b(licence_rows, asof=world.ASOF):
    """Licensed dialysis and infusion sites on the register at the as-of date, and their stations.

    One row per licence number covers the as-of date; corporate umbrella rows are not sites; rows whose
    effective span has closed are not current."""
    best = {}
    for r in licence_rows:
        lic, holder, kind, addr, loc, area, cat, stations, eff, to, status = r
        if kind != "facility" or area not in world.AREA:
            continue
        f = dt.date.fromisoformat(eff)
        t = dt.date.fromisoformat(to) if to else None
        if f > asof or (t is not None and t <= asof):
            continue
        best[lic] = (area, int(stations))
    agg = collections.defaultdict(lambda: [0, 0])
    for lic, (area, st) in best.items():
        agg[area][0] += 1
        agg[area][1] += st
    return [dict(code=c, name=world.AREA[c]["name"], sites=agg[c][0], stations=agg[c][1])
            for c in world.CODES]


def ask_c(sites, extra, filing_rows, licence_rows, directory_rows, position=None):
    """Sites the 2026 filing counted that carry no 2027 contract intent, by their current service area,
    with the stations they were licensed for then.

    The filing keys on licence number at its own position date, so the register row covering that date
    names the facility; two sites are filed twice, once under their operator's corporate number."""
    import pack
    position = position or pack.FILING_POSITION
    cover = {}
    for r in licence_rows:
        lic, holder, kind, addr, loc, area, cat, stations, eff, to, status = r
        if kind != "facility":
            continue
        f = dt.date.fromisoformat(eff)
        t = dt.date.fromisoformat(to) if to else None
        if f > position or (t is not None and t <= position):
            continue
        cover[lic] = addr
    cur = {}
    for r in directory_rows:
        if int(r[0]) != 2026:
            continue
        cur[r[5]] = (r[7], r[12])           # service_address -> (area, contract intent)
    seen, agg = set(), collections.defaultdict(lambda: [0, 0])
    for r in filing_rows:
        lic, name, addr, loc, a26, a26n, cat, stations, status = r
        key = addr
        if key in seen:
            continue
        seen.add(key)
        hit = cur.get(cover.get(lic, addr), cur.get(addr))
        if hit is None or hit[1] != "none":
            continue
        agg[hit[0]][0] += 1
        agg[hit[0]][1] += int(stations)
    return [dict(code=c, name=world.AREA[c]["name"], sites=agg[c][0], stations=agg[c][1])
            for c in world.CODES]


def components(sites, by_area, rows):
    """The intermediate results every valid method computes for the main call."""
    L = world.ladder(sites, by_area)
    pos = sum(s["ceiling"] for s in sites)
    att = sum(s["attested"] for s in sites)
    demand = sum(L["week"][c] for c in world.CODES)
    return dict(
        deliverable_positions=pos,
        attested_stations=att,
        positions_short_of_attested=att - pos,
        sites_short_of_attested=sum(1 for s in sites if s["attested"] > s["ceiling"]),
        projected_weekly_demand_2027=int(round(sum(L["req"][c] for c in world.CODES) / world.CUSHION)),
        required_weekly_slots_network=sum(L["req"][c] for c in world.CODES),
        treatments_2026=sum(s["vol_2026"] for s in sites),
        weekly_treatments_2026=round(demand, 1),
    )
