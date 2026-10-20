"""The city's own records the asks read: the parcel file, the housing code case export and its event history, and
the fund's payment journal. Built on the 2020 blocks of the city's tracts; nothing here touches a Bureau table."""
import datetime as dt

import geo as G
import world as W

END = dt.date(2026, 12, 31)
EXPORT = dt.date(2027, 3, 15)
REKEY = dt.date(2025, 7, 1)            # the county re-keyed parcel numbers; older cases keep the old number
RES = {"R1": "SINGLE FAMILY", "R2": "TWO FAMILY", "R3": "THREE OR FOUR FAMILY", "RM": "MULTIFAMILY 5+",
       "RC": "RESIDENTIAL CONDOMINIUM"}
OTHER = {"C1": "COMMERCIAL", "C2": "MIXED USE COMMERCIAL", "I1": "INDUSTRIAL", "EX": "EXEMPT", "VL": "VACANT LAND"}
CITY_OTHER_TRACTS = 26


def city_tracts(ts):
    """The candidate tracts and the next city tracts in code order."""
    cand = [t for t in ts if t.nbhd]
    rest = sorted([t for t in ts if not t.nbhd], key=lambda t: t.code10)[:CITY_OTHER_TRACTS]
    return cand + rest


class Parcel:
    __slots__ = ("pid", "old", "addr", "use", "block", "tract20", "nbhd", "street", "num")


def parcels(ts, blks):
    city = {t.code10 for t in city_tracts(ts)}
    nb_of = {}
    for t in ts:
        for code, _ in t.children:
            nb_of[code] = t.nbhd
    streets = ["Ash", "Beacon", "Calder", "Delmar", "Elston", "Fairview", "Grover", "Hawthorn", "Ivers", "Juniper",
               "Kenmore", "Larch", "Marsh", "Norland", "Orchard", "Pruitt", "Quarry", "Rowan", "Sumner", "Tilden",
               "Upland", "Vesper", "Walnut", "Yates", "Alden", "Brook", "Cedar Hill", "Dover", "Easton", "Fulton"]
    sfx = ["St", "Ave", "Ct", "Pl", "Dr"]
    out = []
    serial = 0
    for blk in blks:
        if blk.bg.tract10 not in city:
            continue
        for code20, land, water in blk.parts:
            rng = G.rng_for("parcels", code20)
            share = land / max(1, blk.land)
            nres = int(round(blk.pop10 * share / float(rng.uniform(3.4, 4.6))))
            ncom = int(rng.integers(0, 3)) if rng.random() < 0.35 else 0
            st = "%s %s" % (streets[int(rng.integers(0, len(streets)))], sfx[int(rng.integers(0, len(sfx)))])
            base = int(rng.integers(1, 40)) * 100
            for k in range(nres + ncom):
                serial += 1
                p = Parcel()
                tr = code20[5:11]
                p.tract20 = tr[:4] + "." + tr[4:]
                p.block, p.nbhd = code20, nb_of.get(p.tract20)
                p.pid = "%s-%s-%04d-%03d" % (W.COUNTY_FIPS, tr, int(code20[11:]), k + 1)
                p.old = "%010d" % (1400000000 + serial * 7 + int(rng.integers(0, 7)))
                if k < nres:
                    p.use = str(rng.choice(["R1", "R1", "R1", "R2", "R3", "RM", "RC"], p=[.3, .2, .12, .14, .1, .09, .05]))
                else:
                    p.use = str(rng.choice(list(OTHER)))
                p.num = base + 2 * k + (1 if rng.random() < 0.5 else 0)
                p.street = st
                p.addr = "%d %s" % (p.num, st)
                out.append(p)
    return out


class Case:
    __slots__ = ("no", "parcel", "ctype", "opened", "events", "inspector", "reopen")


INSPECTORS = ["K. Ostrowski", "D. Amaya", "R. Bellweather", "T. Nguyen", "S. Pickett", "J. Marrow", "L. Haddad"]
TYPES = [("HOUSING", "Housing code"), ("NUISANCE", "Property nuisance"), ("ZONING", "Zoning"),
         ("BUILDING", "Building without permit")]


def cases(ps):
    """Every code case 2019 to the export, with its event history. A case is closed by compliance or otherwise; the
    January 2027 release added reopening, and the inspectors reopened some cases closed late in 2026 when the
    violation recurred (before it, a recurrence opened a new case)."""
    out = []
    seq = {}
    start, stop = dt.date(2019, 1, 1), EXPORT
    days = (stop - start).days
    for p in ps:
        rng = G.rng_for("cases", p.pid)
        res = p.use in RES
        rate = (0.016 if res else 0.008) * (1.5 if p.nbhd else 1.0)
        n = int(rng.poisson(rate * days / 365.25))
        for _ in range(n):
            o = start + dt.timedelta(days=int(rng.integers(0, days)))
            ct = TYPES[int(rng.choice(4, p=[.55, .3, .08, .07] if res else [.2, .45, .2, .15]))][0]
            seq[o.year] = seq.get(o.year, 0) + 1
            c = Case()
            c.no = "CE%02d-%05d" % (o.year % 100, seq[o.year])
            c.parcel, c.ctype, c.opened, c.reopen = p, ct, o, False
            c.inspector = INSPECTORS[int(rng.integers(0, len(INSPECTORS)))]
            ev = [(o, "CASE OPENED")]
            d = o + dt.timedelta(days=int(rng.integers(3, 15)))
            ev.append((d, "INSPECTION"))
            if rng.random() < 0.8:
                d = d + dt.timedelta(days=int(rng.integers(2, 10)))
                ev.append((d, "NOTICE OF VIOLATION"))
            dur = int(rng.lognormal(4.7, 0.9))
            close = o + dt.timedelta(days=max(20, dur))
            t = d
            while True:
                t = t + dt.timedelta(days=int(rng.integers(25, 75)))
                if t >= close or t > stop:
                    break
                ev.append((t, "REINSPECTION"))
            if close <= stop:
                ev.append((close, "CASE CLOSED - COMPLIANCE" if rng.random() < 0.82 else "CASE CLOSED - OTHER"))
            c.events = [e for e in ev if e[0] <= stop]
            out.append(c)
    out.sort(key=lambda c: (c.opened, c.no))
    return out


def reopen(cs):
    """Reopen, in January to March 2027, housing cases closed between September and December 2026 on residential
    parcels: in each candidate neighbourhood two to four, on properties with no other open housing case then, and a
    scatter elsewhere in the city."""
    by_nb = {}
    for c in cs:
        last = c.events[-1]
        if c.ctype == "HOUSING" and c.parcel.use in RES and last[1].startswith("CASE CLOSED") and \
                dt.date(2026, 9, 1) <= last[0] <= END:
            by_nb.setdefault(c.parcel.nbhd, []).append(c)
    for nb, lst in by_nb.items():
        rng = G.rng_for("reopen", nb)
        lst.sort(key=lambda c: (G.rng_for("ro", c.no).random(), c.no))
        k = int(rng.integers(2, 5)) if nb else max(3, len(lst) // 6)
        busy = {x.parcel.pid for x in cs if x.ctype == "HOUSING" and open_on(x, END)}
        done = 0
        for c in lst:
            if done >= k:
                break
            if c.parcel.pid in busy:
                continue
            when = dt.date(2027, 1, 4) + dt.timedelta(days=int(G.rng_for("rod", c.no).integers(0, 65)))
            c.events.append((when, "CASE REOPENED"))
            c.events.append((when + dt.timedelta(days=int(G.rng_for("roi", c.no).integers(3, 10))), "REINSPECTION"))
            c.events = [e for e in c.events if e[0] <= EXPORT]
            c.reopen = True
            busy.add(c.parcel.pid)
            done += 1


def open_on(c, day):
    """Whether the case was open at the end of the day, from its history."""
    state = False
    for d, e in c.events:
        if d > day:
            break
        if e == "CASE OPENED" or e == "CASE REOPENED":
            state = True
        elif e.startswith("CASE CLOSED"):
            state = False
    return state


def header(c):
    """The export's current record: status and dates as of the export (a reopened case shows open and its closed
    date cleared)."""
    status = "OPEN" if open_on(c, EXPORT) else "CLOSED"
    closed = None
    if status == "CLOSED":
        closed = max(d for d, e in c.events if e.startswith("CASE CLOSED"))
    return status, closed


def ask_a(cs):
    """Each candidate neighbourhood's residential properties with a housing code case open on 31 December 2026, and
    the average days those cases had then been open (from each case's opening)."""
    out = {}
    for nb in W.NEIGHBOURHOODS:
        props, ages = set(), []
        for c in cs:
            if c.parcel.nbhd != nb or c.ctype != "HOUSING" or c.parcel.use not in RES:
                continue
            if open_on(c, END):
                props.add(c.parcel.pid)
                ages.append((END - c.opened).days)
        out[nb] = (len(props), sum(ages) / float(len(ages)))
    return out


class Entry:
    __slots__ = ("no", "date", "grant", "parcel", "payee", "check", "amount", "ref", "desc")


CONTRACTORS = ["Brightline Home Repair LLC", "Tri-County Roofing", "Hollis Habitat Builders", "J & M Exteriors",
               "Northgate Construction", "Carrow Community Builders", "Prairie Lead Abatement", "Keller & Sons"]


def journal(ps):
    """The fund's payment journal, July 2022 to the export: progress, final and retainage payments on each grant; a
    voided check is reversed by a negative entry on its void date that cites the original entry and a new check is
    issued. In each candidate neighbourhood one or two checks of October to December 2026 are voided in January or
    February 2027 and reissued then, and one check of late 2025 is voided and reissued in January 2026."""
    res = [p for p in ps if p.use in RES]
    rng = G.rng_for("grants")
    out = []
    no = 0
    gno = 0
    start = dt.date(2022, 7, 1)
    pays = []
    for k in range(560):
        p = res[int(rng.integers(0, len(res)))]
        if p.nbhd is None and rng.random() < 0.55:
            continue
        gno += 1
        g = "NSF-%d-%03d" % (2022 + (gno * 5) // 380, gno % 1000)
        award = int(rng.integers(90, 450)) * 100
        first = start + dt.timedelta(days=int(rng.integers(0, (dt.date(2027, 2, 20) - start).days)))
        draws = [0.4, 0.5, 0.1] if rng.random() < 0.6 else [0.9, 0.1]
        t = first
        for j, f in enumerate(draws):
            if t > dt.date(2027, 3, 12):
                break
            amt = round(award * f + float(rng.integers(-150, 150)), 2)
            desc = "Retainage release" if f == 0.1 else ("Final payment" if j == len(draws) - 2 or len(draws) == 1
                                                         else "Progress payment %d" % (j + 1))
            pays.append([t, g, p, CONTRACTORS[int(rng.integers(0, len(CONTRACTORS)))], amt, desc])
            t = t + dt.timedelta(days=int(rng.integers(20, 95)))
    pays.sort(key=lambda r: (r[0], r[1]))
    check = 104000
    for t, g, p, payee, amt, desc in pays:
        no += 1
        check += 1
        e = Entry()
        e.no, e.date, e.grant, e.parcel, e.payee, e.check, e.amount, e.ref, e.desc = \
            no, t, g, p, payee, check, amt, "", desc
        out.append(e)
    # the voids
    voids = []
    paid26 = {}
    for e in out:
        if e.date.year == 2026:
            paid26[e.parcel.pid] = paid26.get(e.parcel.pid, 0) + 1
    for nb in W.NEIGHBOURHOODS:
        r2 = G.rng_for("voids", nb)
        # the voided check is the property's only 2026 payment, so the voids move the properties as well as the dollars
        late = [e for e in out if e.parcel.nbhd == nb and dt.date(2026, 10, 1) <= e.date <= dt.date(2026, 12, 20)
                and paid26.get(e.parcel.pid) == 1]
        late.sort(key=lambda e: e.no)
        for e in late[:2]:
            voids.append((e, dt.date(2027, 1, 6) + dt.timedelta(days=int(r2.integers(0, 40)))))
        early = [e for e in out if e.parcel.nbhd == nb and dt.date(2025, 11, 1) <= e.date <= dt.date(2025, 12, 22)
                 and not paid26.get(e.parcel.pid)]
        early.sort(key=lambda e: e.no)
        for e in early[:1]:
            voids.append((e, dt.date(2026, 1, 5) + dt.timedelta(days=int(r2.integers(0, 20)))))
    for e, when in voids:
        check += 1
        r = Entry()
        r.no, r.date, r.grant, r.parcel, r.payee, r.check, r.amount, r.ref, r.desc = \
            0, when, e.grant, e.parcel, e.payee, e.check, -e.amount, "REV %d" % e.no, "Void check %d" % e.check
        n = Entry()
        n.no, n.date, n.grant, n.parcel, n.payee, n.check, n.amount, n.ref, n.desc = \
            0, when + dt.timedelta(days=2), e.grant, e.parcel, e.payee, check, e.amount, "REISSUE %d" % e.no, \
            "Reissue of check %d" % e.check
        out.extend([r, n])
    out.sort(key=lambda e: (e.date, e.no == 0, e.grant))
    for i, e in enumerate(out):
        e.no = 10001 + i if e.no == 0 else e.no
    # renumber so entry numbers rise with posting order
    order = sorted(out, key=lambda e: (e.date, e.no))
    old_to_new = {}
    for i, e in enumerate(order):
        old_to_new[e.no] = 50001 + i
    for e in order:
        e.no = old_to_new[e.no]
        if e.ref:
            kind, num = e.ref.split()
            e.ref = "%s %d" % (kind, old_to_new[int(num)])
    return order


def ask_b(entries):
    """Each candidate neighbourhood's grant dollars paid in calendar 2026 and the properties paid: checks dated in
    2026 that were not voided (whenever voided)."""
    voided = {int(e.ref.split()[1]) for e in entries if e.ref.startswith("REV")}
    out = {}
    for nb in W.NEIGHBOURHOODS:
        amt, props = 0.0, set()
        for e in entries:
            if e.parcel.nbhd != nb or e.amount <= 0 or e.date.year != 2026 or e.no in voided:
                continue
            amt += e.amount
            props.add(e.parcel.pid)
        out[nb] = (round(amt, 2), len(props))
    return out
