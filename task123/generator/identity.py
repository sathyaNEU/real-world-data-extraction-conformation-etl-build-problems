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
    # The balance-date movers (hardening loop 2) are given their identities after the rest of the book,
    # from their own stream, so that every earlier name, charity number and grant reference is unchanged.
    late = [o for o in orgs if o.role in ("bal_change", "gap")]
    book = [o for o in orgs if o.role not in ("bal_change", "gap")]
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
        if len(names) >= len(book) + 10:
            break
    ccs = rng.choice(np.arange(20140, 59870), size=len(book), replace=False)
    seq_op = 400
    seq_pg = 60
    by = {o.key: o for o in orgs}
    for n, o in enumerate(sorted(book, key=lambda o: o.key)):
        p, k = names[n]
        o.name = f"{p} {k}"
        o.district = PLACE_DISTRICT[p]
        o.sector = KIND_SECTOR[k]
        o.cc = f"CC{int(ccs[n]):05d}"
    taken_names = {o.name for o in book}
    taken_cc = {o.cc for o in book}
    r2 = np.random.default_rng([SEED, 9])
    spare = [(p, k) for p, k in pairs if f"{p} {k}" not in taken_names]
    pick = r2.permutation(len(spare))
    j = 0
    for o in sorted(late, key=lambda o: o.key):
        p, k = spare[int(pick[j])]
        j += 1
        o.name = f"{p} {k}"
        o.district = PLACE_DISTRICT[p]
        o.sector = KIND_SECTOR[k]
        while True:
            c = int(r2.integers(20140, 59870))
            if f"CC{c:05d}" not in taken_cc:
                break
        o.cc = f"CC{c:05d}"
        taken_cc.add(o.cc)
    # grant dates and references, in order of start (the movers last, so earlier references hold)
    for o in sorted(book, key=lambda o: (o.first_q, o.key)) + sorted(late, key=lambda o: o.key):
        r = np.random.default_rng([SEED, 8, sum(ord(c) for c in o.key)])
        start_month = {3: 5, 6: 8, 12: 2}[o.bal_app or o.bal]   # the balance date when the grant was let
        fq_end = qend(o.first_q)
        if o.role == "gap":
            # let on 1 August 2017, three-year terms from then: the term to 31 July 2026 lapsed and the
            # grant was renewed from 1 November 2026 for the balance of the cycle (to 31 July 2029)
            int(r.integers(2012, 2018))
            o.og_start = dt.date(2017, 8, 1)
        elif o.first_q <= 5:
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
    assign_gaps(orgs)
    return orgs


# Census dates the lapse twins must stay clear of (every March census and the September census)
_CENSUSES = [dt.date(y, 3, 31) for y in range(2021, 2027)] + [dt.date(2026, 9, 30)]


def assign_gaps(orgs):
    """Hardening loop 3. GT's term to 31 July 2026 lapsed; the renewal, approved on 16 September 2026, runs
    from 1 November 2026, so no term was in force at the September census. Three steady grantees had a
    lapse of the same kind at an earlier renewal, none spanning a census or within 20 days of one, so the
    pattern is ordinary grants administration and the corpus sees no grantee between terms at a census."""
    by = {o.key: o for o in orgs}
    g = by.get("GT")
    if g is not None:
        g.gaps = [(dt.date(2026, 7, 31), dt.date(2026, 11, 1), dt.date(2026, 9, 16))]
    plans = [  # (balance month, renewal year, months lapsed, approval day of the month before the restart)
        (3, 2020, 2, 12), (6, 2021, 2, 9), (3, 2022, 3, 14)]
    taken = set()
    rng = np.random.default_rng([SEED, 31])
    for bal, year, lapse, appr in plans:
        cands = []
        for o in sorted(orgs, key=lambda o: o.key):
            if o.key in taken or o.role != "steady" or o.bal != bal or o.dual or o.notes:
                continue
            b = o.og_start
            while b.year < year:
                b = dt.date(b.year + 3, b.month, b.day)
            if b.year != year or not (o.og_start < b <= o.og_end):
                continue
            end = b - dt.timedelta(days=1)
            m = b.month + lapse
            restart = dt.date(b.year + (m - 1) // 12, (m - 1) % 12 + 1, 1)
            if any(end - dt.timedelta(days=20) <= c <= restart + dt.timedelta(days=20) for c in _CENSUSES):
                continue
            cands.append((o, end, restart))
        o, end, restart = cands[int(rng.integers(0, len(cands)))]
        pm = restart.month - 1 or 12
        py = restart.year if restart.month > 1 else restart.year - 1
        o.gaps = [(end, restart, dt.date(py, pm, appr))]
        taken.add(o.key)
    return orgs
