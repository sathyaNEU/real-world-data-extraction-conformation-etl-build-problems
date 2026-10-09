"""Names, charity numbers, grant references, sectors and grant dates for every organisation."""
import datetime as dt

import numpy as np

from common import SEED, qend
from roster import PLACES, KINDS, SECTORS, PLACE_DISTRICT, Q


KIND_SECTOR = {
    "Community Rooms Trust": "Community development", "Household Budgeting Trust": "Social services",
    "Youth Collective": "Social services", "Family Support Trust": "Social services",
    "Surplus Kai Network": "Social services", "Older Persons Club": "Community development",
    "Arts Trust": "Arts and culture", "Adult Literacy Project": "Education and learning",
    "Learning Centre Trust": "Education and learning", "Community Gardens Society": "Environment",
    "Play Resource Library Society": "Community development", "Hospital Transport Trust": "Health and disability",
    "Neighbourhood Hub Trust": "Community development", "Whanau Support Services": "Social services",
    "Men's Workshop Collective": "Health and disability", "Parenting Network": "Social services",
    "Newcomers Network": "Social services", "Disability Recreation Society": "Health and disability",
    "Community Transport Trust": "Health and disability", "Carer Respite Network": "Health and disability",
    "Te Reo Learning Trust": "Education and learning", "Village Hall Society": "Community development",
    "Sports Education Trust": "Recreation and sport", "Mental Wellbeing Collective": "Health and disability",
    "Tenancy Advocacy Service": "Social services", "Kai Share Cooperative": "Social services",
    "Volunteer Exchange Trust": "Community development", "Day Programme Trust": "Health and disability",
    "Heritage Society": "Arts and culture", "Environmental Restoration Trust": "Environment",
    "Music School Trust": "Arts and culture", "After School Care Society": "Education and learning",
}


def assign_identity(orgs):
    rng = np.random.default_rng([SEED, 7])
    pairs = [(p, k) for p in PLACES for k in KINDS]
    order = rng.permutation(len(pairs))
    used_place_kind = set()
    names = []
    for idx in order:
        p, k = pairs[idx]
        if (p, k) in used_place_kind:
            continue
        names.append((p, k))
        used_place_kind.add((p, k))
        if len(names) >= len(orgs) + 10:
            break
    ccs = rng.choice(np.arange(20140, 59870), size=len(orgs), replace=False)
    seq_op = 400
    seq_pg = 60
    by = {o.key: o for o in orgs}
    for n, o in enumerate(sorted(orgs, key=lambda o: o.key)):
        p, k = names[n]
        o.name = f"{p} {k}"
        o.district = PLACE_DISTRICT[p]
        o.sector = KIND_SECTOR[k]
        o.cc = f"CC{int(ccs[n]):05d}"
    # grant dates and references, in order of start
    for o in sorted(orgs, key=lambda o: (o.first_q, o.key)):
        r = np.random.default_rng([SEED, 8, sum(ord(c) for c in o.key)])
        start_month = {3: 5, 6: 8, 12: 2}[o.bal]
        fq_end = qend(o.first_q)
        if o.first_q <= 5:
            y = int(r.integers(2012, 2018))
            o.og_start = dt.date(y, start_month, 1)
        else:
            # entrants: the grant starts in the first month after the quarter before the first return
            y = fq_end.year if o.bal != 12 else fq_end.year
            o.og_start = dt.date(y, start_month, 1)
            if o.og_start > fq_end:
                o.og_start = dt.date(y - 1, start_month, 1)
        if o.role == "exit":
            o.og_end = qend(o.last_q)
        else:
            # current term end, three-yearly from the start
            end = o.og_start
            while end <= dt.date(2026, 12, 31):
                end = dt.date(end.year + 3, end.month, 1)
            o.og_end = end - dt.timedelta(days=1)
        seq_op += int(r.integers(3, 17))
        o.og_ref = f"APT-OG-{o.og_start.year}-{seq_op:04d}"
        if o.dual:
            pq = qend(o.pg_first_q)
            if o.pg_first_q <= 5:
                ys = int(r.integers(2015, 2018))
                o.pg_start = dt.date(ys, start_month, 1)
            else:
                o.pg_start = dt.date(pq.year, start_month, 1)
                if o.pg_start > pq:
                    o.pg_start = dt.date(pq.year - 1, start_month, 1)
            o.pg_end = dt.date(2027, 4, 30) if o.bal == 3 else dt.date(2027, 7, 31)
            seq_pg += int(r.integers(2, 9))
            o.pg_ref = f"APT-PG-{o.pg_start.year}-{seq_pg:04d}"
    # the twins share every grants-register column but their names, numbers and references
    ta, tb = by.get("TA"), by.get("TB")
    if ta and tb:
        kind_b = next(k for k in KINDS if tb.name.endswith(k))
        place_b = tb.name[: -len(kind_b) - 1]
        for p in PLACES:
            if p != place_b and PLACE_DISTRICT[p] == tb.district and (p, kind_b) not in used_place_kind:
                ta.name = f"{p} {kind_b}"
                used_place_kind.add((p, kind_b))
                break
        ta.sector, ta.district = tb.sector, tb.district
        ta.og_start, ta.og_end = tb.og_start, tb.og_end
    return orgs
