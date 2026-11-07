"""task286 records: what each organisation's system holds about the homes of world.py.

Addresses and the county gazetteer, Pennimouth Water's properties, meters and daily reads (with its communication
gaps and meter exchanges), the two councils' council tax records (Teversby's across its May 2026 move to a new
revenues system), the business rates list's self-catering entries and the 2021 census by output area.
Deterministic: every draw comes from a stream seeded by (SEED, purpose, home or area).
"""
from datetime import date, timedelta

import numpy as np

import world as W

UNIT_LETTERS = "ABDEFGHJLNPQRSTUWXYZ"
H0 = date(2014, 4, 1)                     # the councils' extracts reach back to this liability date
EXTRACT_TDC = date(2026, 10, 5)           # Teversby's new-system extract
EXTRACT_SBC = date(2026, 10, 6)           # Swanholt's extract
FAILED_LETS_BACK = date(2026, 4, 1)       # lets that missed the letting test returned to council tax
SITE_NAMES = {"TV01": ["Mill Farm Cottages"], "TV02": ["Hall Farm Barns"], "TV03": ["Grange Farm Cottages"],
              "TV04": ["Coastguard Cottages", "Harbour Lights Cottages", "Gull Rock Cottages"],
              "SW01": ["Pilot House Cottages"], "SW02": ["Moorside Barns"], "SW03": ["Dunes Holiday Lodges"],
              "SW04": ["Kittlesea Farm Cottages", "Old Forge Cottages", "Coombe Barns"]}
KIND_CLASS = {"terrace": ("RD04", "Terraced"), "semi": ("RD03", "Semi-Detached"), "detached": ("RD02", "Detached"),
              "flats": ("RD06", "Self Contained Flat (Includes Maisonette / Apartment)"),
              "flats_old": ("RD06", "Self Contained Flat (Includes Maisonette / Apartment)"),
              "flats_new": ("RD06", "Self Contained Flat (Includes Maisonette / Apartment)"),
              "site": ("RD04", "Terraced")}
TYPE_KIND_WEIGHT = {
    W.MAIN: {"terrace": 1.0, "semi": 1.0, "detached": 0.6, "flats": 0.55, "flats_old": 0.5, "flats_new": 0.35},
    W.WEEKENDER: {"terrace": 1.0, "semi": 0.3, "detached": 0.8, "flats": 0.4, "flats_old": 0.4, "flats_new": 1.3},
    W.SEASONAL: {"terrace": 1.0, "semi": 0.3, "detached": 0.8, "flats": 0.4, "flats_old": 0.4, "flats_new": 1.3},
    W.LET: {"terrace": 1.4, "semi": 0.3, "detached": 0.5, "flats": 0.3, "flats_old": 0.3, "flats_new": 0.7},
    W.EMPTY: {"terrace": 1.2, "semi": 0.4, "detached": 0.3, "flats": 0.5, "flats_old": 1.3, "flats_new": 2.2},
    W.PARTYEAR: {"terrace": 1.0, "semi": 0.9, "detached": 0.5, "flats": 0.7, "flats_old": 0.7, "flats_new": 0.5},
}
ABBR = {"Street": "ST", "Road": "RD", "Lane": "LN", "Avenue": "AVE", "Close": "CL", "Crescent": "CRES",
        "Drive": "DR", "Terrace": "TER", "Court": "CT", "Square": "SQ", "Parade": "PDE", "Grove": "GRV"}


def rng_for(*key):
    return np.random.default_rng([W.SEED] + list(key))


# --------------------------------------------------------------------------------------------- addresses
def addresses(homes):
    """street, number, flat, building, postcode and UPRN for every home; parent shells for blocks and sites."""
    by_area = {}
    for h in homes:
        by_area.setdefault(h.area, []).append(h)
    parents = []
    for k, a in enumerate(W.AREA_CODES):
        rng = rng_for(10, k)
        hs = by_area[a]
        streets = list(W.STREETS[a])
        sites = []
        if a in SITE_NAMES:
            lets = [h for h in hs if h.typ == W.LET]
            rng.shuffle(lets)
            names = SITE_NAMES[a]
            j = 0
            for nm in names:
                size = int(rng.integers(3, 7))
                grp = lets[j:j + size]
                if len(lets) - (j + size) < 2 and nm != names[0]:
                    break
                j += size
                if len(grp) >= 2:
                    sites.append((nm, grp))
                    for h in grp:
                        h.street, h.kind, h.site = nm, "site", nm
        placed = {id(h) for _nm, g in sites for h in g}
        street_homes = {s: [] for s, _k in streets}
        kinds = dict(streets)
        for h in hs:
            if id(h) in placed:
                continue
            h.site = None
            wts = np.array([TYPE_KIND_WEIGHT[h.typ][kinds[s]] for s, _k in streets])
            s = streets[int(rng.choice(len(streets), p=wts / wts.sum()))][0]
            street_homes[s].append(h)
            h.street, h.kind = s, kinds[s]
        # postcodes: each street gets units of 10 to 24 addresses within one sector of the area
        sector_of = {}
        used_units = set()
        for si, (s, kd) in enumerate(streets + [(nm, "site") for nm, _g in sites]):
            sector_of[s] = int(rng.integers(1, 6))
        uprn = W.AREA_UPRN[a] * 1000000 + int(rng.integers(1000, 9000))
        new_uprn = 10094100000 + k * 1000000 + int(rng.integers(1000, 90000))

        def next_uprn(new=False):
            nonlocal uprn, new_uprn
            if new:
                new_uprn += int(rng.integers(1, 4))
                return new_uprn
            uprn += int(rng.integers(1, 9))
            return uprn

        def unit(s):
            while True:
                u = "%s %d%s%s" % (W.AREA_PC[a], sector_of[s], UNIT_LETTERS[int(rng.integers(0, 20))],
                                   UNIT_LETTERS[int(rng.integers(0, 20))])
                if u not in used_units:
                    used_units.add(u)
                    return u

        for s, kd in streets:
            grp = street_homes[s]
            rng.shuffle(grp)
            if kd.startswith("flats"):
                # blocks of 6 to 24 flats, each block a parent shell with its own name and street number
                nb = 0
                i = 0
                no = int(rng.integers(1, 6))
                while i < len(grp):
                    size = min(len(grp) - i, int(rng.integers(6, 25)))
                    nb += 1
                    stem = s.split()[0] if kd != "flats_new" else s.split()[-1]
                    bname = "%s %s" % (stem if stem not in ("The",) else s.split()[-1],
                                       W.BLOCK_NAMES[kd][int(rng.integers(0, len(W.BLOCK_NAMES[kd])))])
                    if kd == "flats_old":
                        bname = "%d-%d %s" % (no, no + 2, s)
                    pc = unit(s)
                    parent = {"uprn": next_uprn(new=(kd == "flats_new")), "area": a, "street": s, "number": no,
                              "name": None if kd == "flats_old" else bname, "postcode": pc, "kind": "block"}
                    parents.append(parent)
                    for fl, h in enumerate(grp[i:i + size], start=1):
                        h.number = no
                        h.flat = "Flat %d" % fl if kd != "flats_old" else ("Flat %s" % "ABCDEFGHJKLMNPQRSTUVWXYZ"[fl - 1])
                        h.building = parent["name"]
                        h.postcode = pc
                        h.parent_uprn = parent["uprn"]
                        h.uprn = next_uprn(new=(kd == "flats_new"))
                        h.ptype = "RD06"
                    i += size
                    no += int(rng.choice([2, 2, 4, 6]))
            else:
                nums = []
                n = 1
                while len(nums) < len(grp):
                    if rng.random() > 0.08:
                        nums.append(n)
                    n += 1
                grp.sort(key=lambda h: h.i)
                pcs = []
                left = len(grp)
                while left > 0:
                    size = min(left, int(rng.integers(10, 25)))
                    pcs += [unit(s)] * size
                    left -= size
                for h, n, pc in zip(grp, nums, pcs):
                    h.number, h.flat, h.building, h.postcode, h.parent_uprn = n, None, None, pc, None
                    h.uprn = next_uprn()
                    h.ptype = KIND_CLASS[kd][0]
        for nm, grp in sites:
            pc = unit(nm)
            parent = {"uprn": next_uprn(), "area": a, "street": nm, "number": None, "name": nm, "postcode": pc,
                      "kind": "site"}
            parents.append(parent)
            for no, h in enumerate(sorted(grp, key=lambda x: x.i), start=1):
                h.number, h.flat, h.building, h.postcode = no, None, None, pc
                h.parent_uprn = parent["uprn"]
                h.uprn = next_uprn()
                h.ptype = "RD04"
    return parents


def address_line(h):
    parts = []
    if h.flat:
        parts.append(h.flat)
    if h.building:
        parts.append(h.building)
    if h.kind == "site":
        parts.append("%d %s" % (h.number, h.street))
    elif h.kind == "flats_old":
        parts.append("%d %s" % (h.number, h.street))
    else:
        parts.append("%d %s" % (h.number, h.street))
    return ", ".join(parts)


def billing_address(h):
    """the water company's billing style: capitals, its own abbreviations, no comma after a flat."""
    s = address_line(h).upper()
    for k, v in ABBR.items():
        s = s.replace(" " + k.upper(), " " + v)
    return s.replace(",", "")


# ------------------------------------------------------------------------------------------ water company
def water(homes):
    """property references, meters, the UPRN match, communication gaps and exchanges; h.rows holds the reads."""
    order = sorted(homes, key=lambda h: (h.area, h.postcode, h.street, h.number, h.flat or ""))
    ref = 310004000
    for h in order:
        rng = rng_for(20, h.i)
        ref += int(rng.integers(1, 12))
        h.prop_ref = str(ref)
        yy = int(rng.choice([19, 20, 21, 22, 23, 24], p=[0.08, 0.12, 0.25, 0.25, 0.2, 0.1]))
        h.serial = "%02d%s%06d" % (yy, "BCDFGHKM"[int(rng.integers(0, 8))], int(rng.integers(10000, 999999)))
        # the July 2026 matching run left some properties unmatched (odd billing addresses); none of them stood
        # empty for long, so their place in an area never moves a count
        unmatched = rng.random() < 0.025 and h.empty_weeks < 20
        h.match = "UNMATCHED" if unmatched else ("MANUAL" if rng.random() < 0.06 else "AUTO")
    for h in homes:
        rng = rng_for(21, h.i)
        obs = h.total.astype(np.int64).copy()
        rtype = np.array(["ACTUAL"] * W.NDAYS, dtype=object)
        # communication gaps: the head end apportions the next actual read flat over the missed days
        h.gaps = []
        if rng.random() < 0.05:
            for _ in range(int(rng.integers(1, 4))):
                for _try in range(20):
                    n = int(rng.integers(2, 7))
                    s = int(rng.integers(1, W.NDAYS - n - 1))
                    seg = h.present[s:s + n]
                    if (seg.all() or (~seg).all()) and not (rtype[s - 1:s + n + 1] == "ESTIMATED").any():
                        tot = int(obs[s:s + n].sum())
                        base, rem = divmod(tot, n)
                        vals = [base + (1 if j < rem else 0) for j in range(n)]
                        trial = obs.copy()
                        trial[s:s + n] = vals
                        tr_type = rtype.copy()
                        tr_type[s:s + n] = "ESTIMATED"
                        if _week_ok(h, trial) and _weeks_same_without_estimates(h, trial, tr_type):
                            obs = trial
                            rtype[s:s + n] = "ESTIMATED"
                            h.gaps.append((s, n))
                            break
        h.obs = obs
        h.rtype = rtype
        # meter exchanges on a day somebody is in, in a week somebody spends wholly in the home
        h.exchange = None
        if rng.random() < 0.018:
            cands = [i for i in range(W.W0 + 7, W.W1 - 7) if i % 7 == 2 and h.present[i - 2:i + 5].all()
                     and rtype[i] == "ACTUAL"]
            if cands:
                i = int(cands[int(rng.integers(0, len(cands)))])
                f = float(rng.uniform(0.25, 0.75))
                old = int(round(obs[i] * f))
                yy = int(rng.choice([25, 26]))
                new_serial = "%02d%s%06d" % (yy, "BCDFGHKM"[int(rng.integers(0, 8))], int(rng.integers(10000, 999999)))
                h.exchange = (i, old, int(obs[i]) - old, new_serial)


def _week_ok(h, obs):
    """every window week somebody used the home still varies by 80 litres or more, and no empty week by 20."""
    x = obs[W.W0:W.W1 + 1].reshape(W.NWEEKS, 7)
    tw = W.window_weeks_true(h)
    rg = x.max(1) - x.min(1)
    return bool((rg[tw] >= 80).all() and (rg[~tw] <= 30).all())


def _weeks_same_without_estimates(h, obs, rtype):
    """the week-of-use reading is unchanged when the estimated days are left out (a week keeps an actual day
    with somebody in it whenever anybody was in)."""
    x = obs[W.W0:W.W1 + 1].reshape(W.NWEEKS, 7).astype(float)
    t = rtype[W.W0:W.W1 + 1].reshape(W.NWEEKS, 7)
    tw = W.window_weeks_true(h)
    for w in range(W.NWEEKS):
        act = x[w][t[w] == "ACTUAL"]
        if len(act) == 0:
            return False
        if ((act.max() - act.min()) > 50) != bool(tw[w]):
            return False
    return True


def meter_rows(h):
    """(serial, day index, litres, read type) rows for one property, two rows on an exchange day."""
    rows = []
    serial = h.serial
    for i in range(W.NDAYS):
        if h.exchange and i == h.exchange[0]:
            rows.append((serial, i, h.exchange[1], "ACTUAL"))
            serial = h.exchange[3]
            rows.append((serial, i, h.exchange[2], "ACTUAL"))
            continue
        rows.append((serial, i, int(h.obs[i]), h.rtype[i]))
    return rows


# --------------------------------------------------------------------------------------------- council tax
def _d(rng, lo, hi):
    return lo + timedelta(days=int(rng.integers(0, max(1, (hi - lo).days + 1))))


def _band(rng, h):
    if h.ptype == "RD06":
        return str(rng.choice(["A", "B", "C"], p=[0.45, 0.4, 0.15] if h.kind != "flats_new" else [0.1, 0.5, 0.4]))
    if h.ptype == "RD04":
        return str(rng.choice(["A", "B", "C"], p=[0.5, 0.35, 0.15]))
    if h.ptype == "RD03":
        return str(rng.choice(["B", "C", "D"], p=[0.3, 0.45, 0.25]))
    return str(rng.choice(["D", "E", "F", "G"], p=[0.35, 0.35, 0.2, 0.1]))


def declared(homes):
    """each home's council tax timeline as the councils hold it: (start, end or None, state, exempt class, acct)."""
    for h in homes:
        rng = rng_for(30, h.i)
        a = h.area
        built = date(2022, 3, 1) + timedelta(days=int(rng.integers(0, 900))) if h.kind == "flats_new" else H0
        h.built = built
        start0 = max(H0, built)
        segs = []
        acct = [0]

        def add(s, e, st, ex=None, new=True):
            if new:
                acct[0] += 1
            segs.append([s, e, st, ex, acct[0]])

        p_sh = {"SW04": 0.96, "SW03": 0.55}.get(a, 0.78)
        if h.typ == W.MAIN:
            if rng.random() < 0.4:
                c = _d(rng, max(start0, date(2015, 1, 1)), date(2026, 9, 1))
                add(start0, c - timedelta(days=1), W.OCC)
                add(c, None, W.OCC)
            else:
                add(start0, None, W.OCC)
        elif h.typ in (W.WEEKENDER, W.SEASONAL):
            pdate = _d(rng, max(start0, date(2008, 1, 1)), date(2024, 12, 31))
            if pdate > start0:
                add(start0, pdate - timedelta(days=1), W.OCC)
            add(max(pdate, start0), None, W.SECOND if rng.random() < p_sh else W.OCC)
        elif h.typ == W.LET:
            pdate = _d(rng, max(start0, date(2010, 1, 1)), date(2022, 12, 31))
            if pdate > start0:
                add(start0, pdate - timedelta(days=1), W.OCC)
            rated = bool(h.site) or rng.random() < 0.8
            h.rated = rated
            h.failed = False
            if rated:
                lo_t = max(pdate + timedelta(days=60), date(2017, 4, 1))
                t = _d(rng, lo_t, max(lo_t, date(2024, 6, 30)))
                h.rated_from = t
                add(max(pdate, start0), t - timedelta(days=1), W.SECOND)
                if (not h.site) and rng.random() < 0.15:
                    h.failed = True
                    add(FAILED_LETS_BACK, None, W.SECOND)
            else:
                add(max(pdate, start0), None, W.SECOND)
        elif h.typ == W.EMPTY:
            if h.neglect:
                st = W.OCC if rng.random() < (0.95 if a == "SW01" else 0.85) else W.UNF
            else:
                r = rng.random()
                st = W.UNF if r < 0.65 else (W.FUR if r < 0.75 else (W.EXEMPT if r < 0.95 else W.OCC))
            ex = None
            if st == W.EXEMPT:
                ex = str(rng.choice(["F", "E", "G", "L"], p=[0.6, 0.3, 0.05, 0.05]))
            # Orrimouth's homes emptied after the fish dock's processing plant closed in December 2021
            first = date(2022, 1, 10) if a == "SW01" else date(2014, 6, 1)
            lo = date(2024, 6, 1) if ex == "F" else max(start0 + timedelta(days=30), first)
            e0 = _d(rng, lo, date(2025, 7, 31))
            if e0 <= start0:
                e0 = start0 + timedelta(days=30)
            if st == W.OCC:
                add(start0, None, W.OCC)
                h.empty_from = None
            else:
                add(start0, e0 - timedelta(days=1), W.OCC)
                h.empty_from = e0
                if st in (W.UNF, W.FUR) and rng.random() < 0.16:
                    # the empty home changes hands and the new owner leaves it as it is
                    if rng.random() < 0.6:
                        s = _d(rng, date(2026, 4, 6), date(2026, 9, 11))
                    else:
                        s = _d(rng, max(e0 + timedelta(days=120), date(2018, 1, 1)), date(2026, 3, 13))
                    add(e0, s - timedelta(days=1), st, ex)
                    add(s, None, st, ex)
                else:
                    add(e0, None, st, ex)
        elif h.typ == W.PARTYEAR:
            k, di = h.pinfo["kind"], h.pinfo["day"]
            d = W.DAYS[di]
            r = rng.random()
            st = W.UNF if r < 0.50 else (W.FUR if r < 0.65 else (W.EXEMPT if r < 0.80 else W.OCC))
            ex = "F" if st == W.EXEMPT else None
            if k == "in":
                e0 = _d(rng, d - timedelta(days=600), d - timedelta(days=40))
                if st == W.OCC:
                    add(start0, d - timedelta(days=1), W.OCC)
                else:
                    add(start0, e0 - timedelta(days=1), W.OCC)
                    add(e0, d - timedelta(days=1), st, ex)
                add(d, None, W.OCC)
            else:
                if st == W.OCC:
                    add(start0, None, W.OCC)
                else:
                    add(start0, d - timedelta(days=1), W.OCC)
                    add(d, None, st, ex)
        for sg in segs:
            if sg[1] is not None and sg[1] < sg[0]:
                raise ValueError(("bad segment", h.i, sg))
        h.ctax_segs = segs
        h.band = _band(rng, h)


def spring_sales(homes):
    """the spring 2026 market: empty homes left unfurnished that changed hands after 27 March 2026, so the new
    owner's liability is under six months old on 27 September while the dwelling has stood empty for years.
    In Teversby three such sales in each area completed in April, before the new system went live."""
    for k, a in enumerate(W.AREA_CODES):
        rng = rng_for(32, k)
        cands = [h for h in homes if h.area == a and h.typ == W.EMPTY and len(h.ctax_segs) == 2
                 and h.ctax_segs[-1][2] == W.UNF and h.ctax_segs[-1][1] is None
                 and h.ctax_segs[-1][0] < date(2025, 9, 1)]
        cands.sort(key=lambda h: h.i)
        rng.shuffle(cands)
        tev = W.AREA_DISTRICT[a] == "Teversby"
        for h in cands[:3 if tev else 2]:
            if tev:
                s = _d(rng, date(2026, 3, 30), date(2026, 5, 1))
            else:
                s = _d(rng, date(2026, 4, 6), date(2026, 9, 11))
            e0 = h.ctax_segs[-1][0]
            last = h.ctax_segs.pop()
            h.ctax_segs.append([e0, s - timedelta(days=1), W.UNF, None, last[4]])
            h.ctax_segs.append([s, None, W.UNF, None, last[4] + 1])
            h.spring_sale = s


def state_on(h, d):
    """the declared state of a home on day d: (state, exempt class) or (NDR, None) when off the list."""
    for s, e, st, ex, _a in h.ctax_segs:
        if s <= d and (e is None or d <= e):
            return st, ex
    return W.NDR, None


def lte_on(h, d=W.ASOF, cut=W.SIX_MONTHS_BEFORE):
    """a long-term empty home as the Council Tax Base return counts it: unoccupied and substantially unfurnished
    on d, not exempt, and so for more than six months (the dwelling's own spell, whoever was liable)."""
    st, ex = state_on(h, d)
    if st != W.UNF:
        return False
    start = None
    prev_end = None
    for s, e, st2, ex2, _a in sorted(h.ctax_segs, key=lambda x: x[0]):
        if s > d:
            break
        if st2 == W.UNF:
            if start is None or (prev_end is not None and (s - prev_end).days > 1):
                start = s
        else:
            start = None
        prev_end = e
    return start is not None and start < cut


def second_on(h, d=W.ASOF):
    st, ex = state_on(h, d)
    return st in (W.SECOND, W.FUR)


def ctax_refs(homes):
    """the councils' own references: Teversby's legacy property numbers, its new property ids, the valuation
    list (VOA) references both councils hold, Swanholt's property references; account numbers per system."""
    for k, a in enumerate(W.AREA_CODES):
        rng = rng_for(31, k)
        hs = sorted([h for h in homes if h.area == a], key=lambda h: (h.street, h.number, h.flat or ""))
        if W.AREA_DISTRICT[a] == "Teversby":
            base_l = 4100000 + k * 90000 + int(rng.integers(0, 5000))
            base_n = 200000000 + k * 3000000 + int(rng.integers(0, 90000))
            for h in hs:
                base_l += int(rng.integers(1, 6))
                base_n += int(rng.integers(3, 40))
                h.legacy_ref = "%07d" % base_l
                h.new_id = "P%09d" % base_n
                h.voa_ref = "%05d%08d" % (31045, int(rng.integers(10000000, 99999999)))
        else:
            base = 6200000 + k * 70000 + int(rng.integers(0, 5000))
            for h in hs:
                base += int(rng.integers(1, 7))
                h.sbc_ref = "SW%07d" % base
                h.voa_ref = "%05d%08d" % (31050, int(rng.integers(10000000, 99999999)))


# ------------------------------------------------------------------------------------------ business rates
def rating_entries(homes, parents):
    """self-catering entries on the business rates list: one per rated let, one per site covering its cottages."""
    entries = []
    site_parent = {p["name"]: p for p in parents if p["kind"] == "site"}
    sites = {}
    for h in homes:
        if h.typ == W.LET and getattr(h, "rated", False):
            if h.site:
                sites.setdefault(h.site, []).append(h)
            else:
                entries.append({"homes": [h], "site": None})
    for nm, grp in sorted(sites.items()):
        entries.append({"homes": sorted(grp, key=lambda x: x.i), "site": site_parent[nm]})
    rng = rng_for(40)
    order = sorted(entries, key=lambda e: (e["homes"][0].area, e["homes"][0].postcode, e["homes"][0].i))
    ref = 5100000
    for e in order:
        ref += int(rng.integers(1, 30))
        e["ba_ref"] = "%s%07d%s" % ("31045" if W.AREA_DISTRICT[e["homes"][0].area] == "Teversby" else "31050",
                                     ref, "%02d" % int(rng.integers(0, 99)))
        n = len(e["homes"])
        e["rv"] = int(round(float(rng.uniform(2300, 8400)) * (1 if n == 1 else n * 0.9), -1))
        e["from"] = min(getattr(h, "rated_from", date(2019, 4, 1)) for h in e["homes"])
        e["to"] = date(2026, 3, 31) if (n == 1 and e["homes"][0].failed) else None
        e["area"] = e["homes"][0].area
    return order


def ndr_homes_on(entries, d=W.ASOF):
    out = {a: 0 for a in W.AREA_CODES}
    for e in entries:
        if e["from"] <= d and (e["to"] is None or d <= e["to"]):
            out[e["area"]] += len(e["homes"])
    return out


# -------------------------------------------------------------------------------------------------- census
CENSUS_DAY = date(2021, 3, 21)


def census(homes):
    """2021 output areas (groups of streets), the household spaces each held and how many had no usual residents."""
    oas = []
    rng = rng_for(50)
    for k, a in enumerate(W.AREA_CODES):
        hs = sorted([h for h in homes if h.area == a and h.built <= CENSUS_DAY], key=lambda h: (h.street, h.number))
        i = 0
        while i < len(hs):
            size = min(len(hs) - i, int(rng.integers(95, 160)))
            if len(hs) - (i + size) < 60:
                size = len(hs) - i
            grp = hs[i:i + size]
            oas.append({"code": "E00%06d" % int(rng.integers(150000, 189999)), "area": a, "homes": grp})
            i += size
    # two output areas in each district straddle a community area boundary: their homes split between areas
    for dist in ("Teversby", "Swanholt"):
        da = [o for o in oas if W.AREA_DISTRICT[o["area"]] == dist]
        for j in range(2):
            o1, o2 = da[2 * j + 1], da[2 * j + 2]
            if o1["area"] != o2["area"]:
                move = o2["homes"][:int(len(o2["homes"]) * 0.35)]
                o2["homes"] = o2["homes"][len(move):]
                o1["homes"] = o1["homes"] + move
    for o in oas:
        nur = 0
        for h in o["homes"]:
            r = rng_for(51, h.i).random()
            if h.typ == W.LET:
                nur += 1 if r < 0.97 else 0
            elif h.typ in (W.WEEKENDER, W.SEASONAL):
                # spring 2021: many owners sat out the lockdown in their second homes
                nur += 1 if r < (0.45 if h.typ == W.WEEKENDER else 0.50) else 0
            elif h.typ == W.EMPTY:
                nur += 1 if (h.empty_from is not None and h.empty_from <= CENSUS_DAY) or (r < 0.06) else 0
            else:
                nur += 1 if r < 0.025 else 0
        o["spaces"] = len(o["homes"])
        o["nur"] = nur
        cnt = {}
        for h in o["homes"]:
            cnt[h.area] = cnt.get(h.area, 0) + 1
        o["bestfit"] = max(sorted(cnt), key=lambda x: cnt[x])
    return oas


def town(h):
    return W.AREA_NAME[h.area]


def ctax_tables(homes):
    """the three council tax extracts as each system writes them (Teversby's legacy archive closed at go-live,
    Teversby's new system from go-live, Swanholt's one system), one row per liability on a property."""
    leg, new, sbc = [], [], []
    rl, rn, rs = rng_for(33, 1), rng_for(33, 2), rng_for(33, 3)
    acc_l, acc_n, acc_s = 70100000, 3004100000, 51200000
    go = W.GO_LIVE
    order = sorted(homes, key=lambda h: (h.area, h.street, h.number, h.flat or ""))
    for h in order:
        tev = W.AREA_DISTRICT[h.area] == "Teversby"
        for s, e, st, ex, _k in h.ctax_segs:
            if st == W.NDR:
                continue
            if tev:
                legacy_no = None
                if s < go:
                    acc_l += int(rl.integers(1, 40))
                    legacy_no = str(acc_l)
                    to = e if (e is not None and e < go) else go - timedelta(days=1)
                    reason = "MIGRATED" if (e is None or e >= go) else (
                        "TRANSFERRED TO NDR" if (h.typ == W.LET and getattr(h, "rated", False)
                                                 and e == h.rated_from - timedelta(days=1)) else "LIABILITY ENDED")
                    leg.append({"PROP_REF": h.legacy_ref, "VO_REF": h.voa_ref,
                                "ADDR_1": (h.flat + " " + (h.building or "")).strip().upper() if h.flat else "",
                                "ADDR_2": ("%d %s" % (h.number, h.street)).upper(), "ADDR_3": town(h).upper(),
                                "POSTCODE": h.postcode, "BAND": h.band, "ACC_NO": legacy_no,
                                "FROM_DATE": s, "TO_DATE": to,
                                "STATUS": {W.OCC: "OCCUPIED", W.SECOND: "SECOND HOME", W.FUR: "UNOCCUPIED FURNISHED",
                                           W.UNF: "UNOCCUPIED UNFURNISHED", W.EXEMPT: "EXEMPT"}[st],
                                "EXEMPT_CLASS": ex or "", "CLOSE_REASON": reason})
                if e is None or e >= go:
                    acc_n += int(rn.integers(3, 60))
                    carried = s < go
                    occ = {W.OCC: "Occupied", W.SECOND: "Second home", W.FUR: "Unoccupied", W.UNF: "Unoccupied",
                           W.EXEMPT: "Exempt"}[st]
                    furn = "" if (carried or st not in (W.FUR, W.UNF)) else ("Y" if st == W.FUR else "N")
                    new.append({"Property ID": h.new_id, "UPRN": h.uprn, "Valuation List Ref": h.voa_ref,
                                "Address": address_line(h) + ", " + town(h), "Postcode": h.postcode, "Band": h.band,
                                "Account": str(acc_n), "Legacy Account": legacy_no if carried else "",
                                "Liability From": go if carried else s, "Liability To": e,
                                "Occupation": occ, "Furnished": furn, "Exemption Class": ex or ""})
            else:
                acc_s += int(rs.integers(1, 25))
                lag = int(rs.choice([0, 0, 1, 2, 3, 5, 8, 13, 21, 34]))
                ent = min(s + timedelta(days=lag), EXTRACT_SBC)
                if ent < H0:
                    ent = H0
                sbc.append({"PROPERTY_REF": h.sbc_ref, "UPRN": h.uprn, "VOA_REF": h.voa_ref,
                            "ADDRESS": (address_line(h) + ", " + town(h)).upper(), "POSTCODE": h.postcode,
                            "BAND": h.band, "ACCOUNT_REF": "%d" % acc_s, "LIAB_START": s, "LIAB_END": e,
                            "OCC_STATUS": {W.OCC: "OCCUPIED", W.SECOND: "SECOND HOME", W.FUR: "UNOCC FURNISHED",
                                           W.UNF: "UNOCC UNFURNISHED",
                                           W.EXEMPT: "EXEMPT"}[st],
                            "EX_CLASS": ex or "", "ENTERED_ON": ent})
    return leg, new, sbc


def build_all():
    homes = W.build()
    parents = addresses(homes)
    water(homes)
    declared(homes)
    spring_sales(homes)
    ctax_refs(homes)
    entries = rating_entries(homes, parents)
    oas = census(homes)
    return homes, parents, entries, oas
