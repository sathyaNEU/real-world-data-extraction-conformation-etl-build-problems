"""The world's people and the records the agencies hold about them, simulated from task471/generator/world.py.

national(seed)  births by sex since 1925, deaths and border movements by year, sex and age at the event, and the people
                usually resident on census day by sex and single year of age (births less deaths plus net movements,
                cohort by cohort: the population demographic analysis rebuilds exactly)
regional(...)   those people spread over the 16 regions by each region type's age and sex profile, the unsettled men
counts(...)     the census's counted, erroneous and imputed records by cell, the survey's sampled meshblocks with
                person-level census and survey capture, and the roll on census day
"""
import numpy as np

import world as W

YEARS = range(1925, 2025)
AGES = range(0, 101)          # 100 is "100 and over"
Q1 = 62.0 / 365.0             # share of a year before census day (1 January to 3 March)


def rng_for(seed, k):
    return np.random.default_rng(seed * 1000 + k)


# ------------------------------------------------------------------ national demography

def births_total(y):
    """live births in a year, a smooth history with a baby boom and a 1970s fall"""
    if y < 1946:
        b = 30000 + 450 * (y - 1925)
    elif y < 1962:
        b = 44000 + 1500 * (y - 1946)
    elif y < 1972:
        b = 68000 - 300 * (y - 1962)
    elif y < 1980:
        b = 65000 - 1600 * (y - 1972)
    elif y < 1992:
        b = 52200 + 700 * (y - 1980)
    elif y < 2002:
        b = 60600 - 450 * (y - 1992)
    elif y < 2009:
        b = 56100 + 800 * (y - 2002)
    else:
        b = 61700 - 380 * (y - 2009)
    return b


def mortality(age, sex, year):
    """annual probability of death: Gompertz with an infant term and a young-adult accident hump, men higher, improving"""
    imp = np.exp(-0.0115 * (year - 1950))
    a = age + 0.5
    g = (0.00006 if sex == "F" else 0.00010) * np.exp(0.092 * a) * imp
    infant = (0.020 if sex == "F" else 0.025) * np.exp(-2.2 * a) * imp
    hump = 0.0
    if 15 <= age <= 35:
        hump = (0.0003 if sex == "F" else 0.0011) * np.exp(-((age - 22) / 6.0) ** 2) * (0.6 + 0.4 * imp)
    return float(min(0.6, g + infant + hump))


def departure_rate(age, sex, year):
    """share of residents leaving the country for good in a year: young adults, young men most"""
    era = 0.55 if year < 1970 else 0.8 if year < 1990 else 1.0
    base = 0.0018
    young = 0.0115 * np.exp(-((age - 25) / 6.5) ** 2)
    if sex == "M":
        young *= 1.22
    child = 0.0035 * np.exp(-((age - 3) / 4.0) ** 2)
    return era * (base + young + child)


def arrivals_by_age(year, sex, rng):
    """arrivals for good in a year by age at arrival: young adults and their children"""
    era = 0.35 if year < 1970 else 0.65 if year < 1990 else 1.0
    total = era * (24000 + 4000 * np.sin((year - 1950) / 7.0))
    w = np.array([0.6 * np.exp(-((a - 4) / 5.0) ** 2) + np.exp(-((a - 28) / 7.5) ** 2) + 0.25 * np.exp(-((a - 45) / 12.0) ** 2)
                  for a in AGES])
    w = w / w.sum()
    n = rng.poisson(total * (0.52 if sex == "M" else 0.48) * w)
    return n


def national(seed):
    """flows by year, sex and year of birth from 1925, the first weeks of 2025 to census day, and the people living in
    the country on census day by sex and single year of age (100 holds 100 and over); demographic analysis over these
    flows rebuilds the census-day population exactly"""
    rng = rng_for(seed, 1)
    births = {}
    deaths, deps, arrs = {}, {}, {}      # (year, sex, birth year) -> n; year "2025Q" is 1 January to 3 March 2025
    cohort = {"M": {}, "F": {}}
    for y in list(YEARS) + ["2025Q"]:
        part = Q1 if y == "2025Q" else 1.0
        yy = 2025 if y == "2025Q" else y
        if y != "2025Q":
            srb = 1.055 + rng.normal(0, 0.006)
            b = rng.poisson(births_total(y))
            bm = rng.binomial(b, srb / (1 + srb))
            births[(y, "M")], births[(y, "F")] = bm, b - bm
        for sex in ("M", "F"):
            if y != "2025Q":
                cohort[sex][y] = births[(y, sex)]
            arr = arrivals_by_age(yy, sex, rng)
            for c in sorted(cohort[sex]):
                n = cohort[sex][c]
                if n <= 0:
                    continue
                age = min(max(yy - c, 0), 100)
                newborn = (c == yy)
                q = mortality(age, sex, yy) * part * (0.5 if newborn else 1.0)
                d = rng.binomial(n, min(q, 0.95))
                e = rng.binomial(n - d, min(departure_rate(age, sex, yy) * part * (0.5 if newborn else 1.0), 0.5))
                cohort[sex][c] = n - d - e
                if d:
                    deaths[(y, sex, c)] = deaths.get((y, sex, c), 0) + d
                if e:
                    deps[(y, sex, c)] = deps.get((y, sex, c), 0) + e
            for a in AGES:
                k = int(rng.poisson(arr[a] * part)) if y == "2025Q" else int(arr[a])
                if not k:
                    continue
                lo = rng.binomial(k, 0.5)
                for c, kk in ((yy - a - 1, lo), (yy - a, k - lo)):
                    if kk <= 0 or c > yy or (y == "2025Q" and c > 2024):
                        continue
                    if c not in cohort[sex]:
                        continue
                    cohort[sex][c] += kk
                    arrs[(y, sex, c)] = arrs.get((y, sex, c), 0) + kk
    # census day: the cohort born in year c is aged 2024 - c, or 2025 - c if born 1 January to 3 March; the babies of
    # the first weeks of 2025 are aged 0
    pop = {"M": np.zeros(101, int), "F": np.zeros(101, int)}
    for sex in ("M", "F"):
        for c, n in cohort[sex].items():
            if n <= 0:
                continue
            older = rng.binomial(n, Q1)
            for k, age in ((n - older, 2024 - c), (older, 2025 - c)):
                if age >= 0:
                    pop[sex][min(age, 100)] += k
        newborn = rng.poisson(births_total(2025) * Q1 * (0.513 if sex == "M" else 0.487))
        pop[sex][0] += newborn
        births[("2025Q", sex)] = int(newborn)
    return {"births": births, "deaths": deaths, "departures": deps, "arrivals": arrs, "pop": pop, "cohort": cohort}


# ------------------------------------------------------------------ regions

def profile(rtype, sex, age):
    """relative weight of a region type at a sex and age"""
    a = age
    base = np.exp(-((a - 38) / 30.0) ** 2) + 0.35
    if rtype == "metro":
        base *= 1 + 0.45 * np.exp(-((a - 30) / 9.0) ** 2) - 0.15 * (a > 65)
    elif rtype == "college":
        base *= 1 + 0.9 * np.exp(-((a - 21) / 3.5) ** 2) + 0.1 * np.exp(-((a - 30) / 8.0) ** 2)
    elif rtype == "coastal":
        base *= 1 + 0.55 * np.exp(-((a - 70) / 11.0) ** 2) - 0.25 * np.exp(-((a - 26) / 7.0) ** 2)
    elif rtype == "rural":
        base *= 1 + 0.2 * np.exp(-((a - 8) / 6.0) ** 2) + 0.2 * np.exp(-((a - 55) / 10.0) ** 2) \
            - 0.3 * np.exp(-((a - 24) / 5.0) ** 2)
    elif rtype == "resource":
        base *= 1 + (0.55 if sex == "M" else 0.15) * np.exp(-((a - 33) / 10.0) ** 2) - 0.15 * (a > 65)
    return base


def regional(nat, seed):
    """people by region, sex and single age; and the unsettled men aged 18 to 49 among them"""
    rng = rng_for(seed, 2)
    pop = {c: {"M": np.zeros(101, int), "F": np.zeros(101, int)} for c in W.CODES}
    jit = {c: rng.uniform(0.94, 1.06) for c in W.CODES}
    for sex in ("M", "F"):
        for a in AGES:
            w = np.array([W.SIZE[c] * profile(W.TYPE[c], sex, a) * jit[c] for c in W.CODES], float)
            draw = rng.multinomial(int(nat["pop"][sex][a]), w / w.sum())
            for c, k in zip(W.CODES, draw):
                pop[c][sex][a] = k
    unsettled = {}
    share = {c: W.UNSETTLED[W.TYPE[c]] * rng.uniform(0.93, 1.07) for c in W.CODES}
    for c in W.CODES:
        u = np.zeros(101, int)
        for a in range(18, 50):
            u[a] = rng.binomial(pop[c]["M"][a], share[c])
        unsettled[c] = u
    return {"pop": pop, "unsettled": unsettled, "unsettled_share": share}


# ------------------------------------------------------------------ census, survey and roll

def coverage(seed):
    """region-level coverage and enrolment rates for everyone but the unsettled men"""
    rng = rng_for(seed, 3)
    pc, pp, en, imp = {}, {}, {}, {}
    for c in W.CODES:
        t = W.TYPE[c]
        pc[c] = W.P_CENSUS[t] + rng.normal(0, 0.006)
        pp[c] = W.P_PES[t] + rng.normal(0, 0.006)
        en[c] = W.ENROL[t] + rng.normal(0, 0.016)
        imp[c] = W.IMPUTED[t] * rng.uniform(0.8, 1.2)
    return {"pc": pc, "pp": pp, "enrol": en, "imputed": imp}


def p_census(cov, c, sex, age, unsettled):
    if unsettled:
        return W.P_CENSUS_UNSETTLED
    g = W.age_group(age)
    return cov["pc"][c] - W.YOUNG_ADULT_DROP.get(g, 0.0)


def p_pes(cov, c, sex, age, unsettled):
    if unsettled:
        return W.P_PES_UNSETTLED
    g = W.age_group(age)
    return cov["pp"][c] - W.YOUNG_ADULT_DROP.get(g, 0.0)


def counts(reg, cov, seed):
    """census tables by cell (region, sex, age), the survey's person records and the roll on census day"""
    rng = rng_for(seed, 4)
    census = {}                       # (region, sex, age) -> dict(counted=correct+erroneous incl. imputed, imputed=)
    p_sample, e_sample = [], []       # person-level records in sampled meshblocks
    mb_count = {}
    for c in W.CODES:
        n_res = sum(int(reg["pop"][c][s].sum()) for s in ("M", "F"))
        mb_count[c] = max(60, int(round(n_res / 92.0)))
    sampled_mb = {c: [m for m in range(1, mb_count[c] + 1) if m % W.MB_SAMPLE == 7 % W.MB_SAMPLE] for c in W.CODES}
    pid = 0
    for c in W.CODES:
        mbs = sampled_mb[c]
        frac = len(mbs) / float(mb_count[c])
        for sex in ("M", "F"):
            for a in AGES:
                n = int(reg["pop"][c][sex][a])
                u = int(reg["unsettled"][c][a]) if sex == "M" else 0
                correct = 0
                for cls, k in ((1, u), (0, n - u)):
                    if k <= 0:
                        continue
                    pc = p_census(cov, c, sex, a, cls)
                    pp = p_pes(cov, c, sex, a, cls)
                    ks = rng.binomial(k, frac)                     # living in a sampled meshblock
                    correct += rng.binomial(k - ks, pc)
                    if ks:
                        inc = rng.random(ks) < pc
                        inp = rng.random(ks) < pp
                        mb = rng.choice(mbs, ks)
                        for i in range(ks):
                            pid += 1
                            p_sample.append((c, int(mb[i]), sex, a, cls, bool(inc[i]), bool(inp[i]), pid))
                        correct += int(inc.sum())
                g = W.age_group(a)
                ee = rng.poisson(correct * W.EE_RATE[g] * W.EE_TYPE[W.TYPE[c]].get(g, 1.0))
                ee_s = rng.binomial(ee, frac)
                for _ in range(ee_s):
                    pid += 1
                    e_sample.append((c, int(rng.choice(mbs)), sex, a, pid))
                census[(c, sex, a)] = {"correct": correct, "erroneous": ee}
        # records imputed for dwellings the census could not contact, spread over the region's cells
        tot = sum(v["correct"] + v["erroneous"] for (cc, s, a), v in census.items() if cc == c)
        n_imp = rng.poisson(tot * cov["imputed"][c])
        cells = [(c, s, a) for s in ("M", "F") for a in AGES]
        w = np.array([census[k]["correct"] + census[k]["erroneous"] for k in cells], float)
        draw = rng.multinomial(n_imp, w / w.sum())
        for k, d in zip(cells, draw):
            census[k]["imputed"] = int(d)
    return {"census": census, "p_sample": p_sample, "e_sample": e_sample, "mb_count": mb_count,
            "sampled_mb": sampled_mb}


def roll(reg, cov, seed):
    """electors enrolled on census day at an address in each region, by sex and age"""
    rng = rng_for(seed, 5)
    out = {}
    for c in W.CODES:
        for sex in ("M", "F"):
            for a in range(18, 101):
                n = int(reg["pop"][c][sex][a])
                u = int(reg["unsettled"][c][a]) if sex == "M" else 0
                g = W.age_group(a)
                pe = min(0.995, cov["enrol"][c] + W.ENROL_AGE[g])
                k = rng.binomial(n - u, pe) + rng.binomial(u, W.ENROL_UNSETTLED)
                k += rng.poisson(k * W.STALE_ROLL)
                out[(c, sex, a)] = k
    return out


# ------------------------------------------------------------------ the roll's transaction log after census day

import datetime as _dt


def local_to_utc(t):
    """the country's time to UTC: UTC+13 in daylight time (the last Sunday in September to the first Sunday in April),
    UTC+12 otherwise"""
    return t - _dt.timedelta(hours=13 if W.daylight(t) else 12)


def utc_to_local(u):
    for off in (13, 12):
        t = u + _dt.timedelta(hours=off)
        if W.daylight(t) == (off == 13):
            return t
    return u + _dt.timedelta(hours=12)


def _workday(d):
    return d.weekday() < 5


def roll_log(reg, roll_counts, seed):
    """enrolments, removals and reinstatements processed from census day to the extract's close (23:59:59 UTC on 30
    September 2026): one row a transaction, [txn_id, stamp as stored, type, reason, source, status, elector_no,
    person_ref, electorate number, address_type, sex, birth_year, ref_txn, local_time, platform, kind, electorate code,
    the removal it puts right]; the two platforms are described in world.py"""
    rng = rng_for(seed, 6)
    start = _dt.datetime.combine(W.CENSUS_DAY, _dt.time(0, 0))
    end_local = utc_to_local(W.EXTRACT_CLOSE_UTC)
    switch = _dt.datetime.combine(W.PLATFORM_SWITCH, _dt.time(0, 0))
    days = [(W.CENSUS_DAY + _dt.timedelta(days=i)) for i in range((end_local.date() - W.CENSUS_DAY).days + 1)]
    elec_by_region = {c: [e for e in W.ELECTORATES if e[2] == c] for c in W.CODES}
    # electors on the census-day roll by electorate (residents only)
    electors = {}
    for c in W.CODES:
        n = sum(k for (cc, s, a), k in roll_counts.items() if cc == c)
        es = elec_by_region[c]
        w = rng.uniform(0.85, 1.15, len(es))
        draw = rng.multinomial(n, w / w.sum())
        for e, k in zip(es, draw):
            electors[e[0]] = int(k)
    rows = []
    next_no = [W.CENSUS_DAY_FIRST_NO]          # the next elector number at census day
    used_refs = set()

    def new_ref():
        while True:
            r = "P%08d" % int(rng.integers(10000000, 99999999))
            if r not in used_refs:
                used_refs.add(r)
                return r

    def new_no():
        next_no[0] += int(rng.integers(1, 6))
        return "%08d" % next_no[0]

    used_nos = set()

    def existing():
        """an elector enrolled before census day: their record and their number"""
        while True:
            no = "%08d" % int(rng.integers(10000000, W.CENSUS_DAY_FIRST_NO))
            if no not in used_nos:
                used_nos.add(no)
                return new_ref(), no

    serial = [0]

    def stamp(local):
        serial[0] += 1
        tid = "tmp%09d" % serial[0]
        if local < switch:
            return tid, local.strftime("%Y-%m-%d %H:%M:%S"), "old"
        return tid, local_to_utc(local).strftime("%Y-%m-%d %H:%M:%S"), "new"

    def business(d):
        return _dt.datetime.combine(d, _dt.time(8, 0)) + _dt.timedelta(seconds=int(rng.integers(0, 9 * 3600 + 1800)))

    def overnight(d):
        """the old platform's duplicate check, run from 02:00 the night after"""
        return _dt.datetime.combine(d + _dt.timedelta(days=1), _dt.time(2, 0)) + _dt.timedelta(
            seconds=int(rng.integers(0, 5400)))

    def add(local, typ, reason, source, status, eno, ref, elec, addr, sex, by, ref_txn="", kind="", fixes=""):
        if local < start or local > end_local:
            return None
        tid, st, plat = stamp(local)
        rows.append([tid, st, typ, reason, source, status, eno, ref, elec, addr, sex, by, ref_txn, local, plat, kind, elec,
                     fixes])
        return tid

    def put_right(bt, removal, removal_old, eno, ref, e, sex, by, addr="R", kind=""):
        """a removal made in error put right: on the old platform by enrolling the person again under a new record,
        pointing at the removal; on the new by reinstating the record, pointing at the removal by the new platform's
        key, which for a removal the old platform made is the key the migration gave it"""
        if bt < switch:
            return add(bt, "NEW", "", "PAP", "A", eno, new_ref(), e, addr, sex, by, ref_txn=removal, kind=kind,
                       fixes=removal)
        return add(bt, "REI", "", "", "A", eno, ref, e, addr, sex, by, ref_txn="ORPHAN_NEW" if removal_old else removal,
                   kind=kind, fixes=removal)

    all_elec = [e[0] for e in W.ELECTORATES]
    size = np.array([electors[e] for e in all_elec], float)
    # moves to another electorate on the old platform: an enrolment at the new address under a new record and the
    # elector's own number, then overnight the removal of the older record as a duplicate
    for d in days:
        if not (_workday(d) and d < W.PLATFORM_SWITCH):
            continue
        for e in all_elec:
            c = W.ELECTORATE_REGION[e]
            k = rng.poisson(electors[e] * 0.036 / 250.0)
            for _ in range(k):
                ref, eno = existing()
                same = [x[0] for x in elec_by_region[c] if x[0] != e]
                if same and rng.random() < 0.55:
                    dest = same[int(rng.integers(0, len(same)))]
                else:
                    dest = all_elec[int(rng.choice(len(all_elec), p=size / size.sum()))]
                    if dest == e:
                        continue
                sex = "M" if rng.random() < 0.49 else "F"
                by = int(rng.integers(1940, 2006))
                src = "ONL" if rng.random() < 0.7 else "PAP"
                add(business(d), "NEW", "", src, "A", eno, new_ref(), dest, "R", sex, by, kind="move_new")
                add(overnight(d), "DEL", "03", "", "A", eno, ref, e, "R", sex, by, kind="move_del")
    # deaths, by electorate, spread over the extract and removed later: by the death registration match (old platform:
    # monthly on the first working day; new: weekly, Wednesdays at 07:30) or on a family's notification during the day;
    # a match made in error is put right when the elector or the family comes forward
    death_rate = 0.0078

    def first_working(y, m):
        dd = _dt.date(y, m, 1)
        while not _workday(dd):
            dd += _dt.timedelta(days=1)
        return dd
    for e in all_elec:
        n = electors[e]
        k = rng.poisson(n * death_rate * (len(days) / 365.0) * 1.05)
        for _ in range(k):
            died = start + _dt.timedelta(days=float(rng.uniform(-40, len(days))))
            ref, eno = existing()
            sex = "M" if rng.random() < 0.5 else "F"
            by = int(rng.integers(1925, 1990))
            notified = rng.random() < 0.18
            if notified:
                dd = (died + _dt.timedelta(days=int(rng.integers(3, 30)))).date()
                while not _workday(dd):
                    dd += _dt.timedelta(days=1)
                t = business(dd)
            else:
                reg_day = (died + _dt.timedelta(days=int(rng.integers(5, 25)))).date()
                if reg_day < W.PLATFORM_SWITCH:
                    nxt = first_working(reg_day.year + (reg_day.month == 12), reg_day.month % 12 + 1)
                else:
                    nxt = reg_day + _dt.timedelta(days=(2 - reg_day.weekday()) % 7 or 7)
                t = _dt.datetime.combine(nxt, _dt.time(7, 30)) + _dt.timedelta(seconds=int(rng.integers(0, 900)))
            reason = "01" if t < switch else ("12" if notified else "11")
            tid = add(t, "DEL", reason, "", "A", eno, ref, e, "R", sex, by, kind="death")
            old = t < switch
            if tid and not notified and rng.random() < (0.024 if old else 0.010):
                back = (t + _dt.timedelta(days=int(rng.integers(20, 150) if old else rng.integers(6, 150)))).date()
                if _workday(back):
                    put_right(business(back), tid, old, eno, ref, e, sex, by, kind="death_rev")
    # removals made before census day in error and put right after it: matches of the old platform's December to March
    # runs, and removals from the December 2024 overseas batch (overseas electors, put back at their overseas address)
    pre_runs = [first_working(2024, 12), first_working(2025, 1), first_working(2025, 2), first_working(2025, 3)]
    for e in all_elec:
        n = electors[e]
        for run in pre_runs:
            k = rng.poisson(n * death_rate / 12.0 * 1.05 * 0.82 * 0.024)
            for _ in range(k):
                ref, eno = existing()
                sex = "M" if rng.random() < 0.5 else "F"
                by = int(rng.integers(1925, 1990))
                t0 = _dt.datetime.combine(run, _dt.time(7, 30)) + _dt.timedelta(seconds=int(rng.integers(0, 900)))
                back = (t0 + _dt.timedelta(days=int(rng.integers(20, 150)))).date()
                if _workday(back):
                    put_right(business(back), ("ORPHAN_OLD", t0), True, eno, ref, e, sex, by, kind="pre_rev")
        k = rng.poisson(n * 0.0012 * 0.04)
        for _ in range(k):
            ref, eno = existing()
            sex = "M" if rng.random() < 0.5 else "F"
            by = int(rng.integers(1950, 2003))
            t0 = _dt.datetime(2024, 12, 3, 21, 15) + _dt.timedelta(seconds=int(rng.integers(0, 2400)))
            back = (t0 + _dt.timedelta(days=int(rng.integers(30, 540)))).date()
            if _workday(back):
                put_right(business(back), ("ORPHAN_OLD", t0), True, eno, ref, e, sex, by, addr="O", kind="pre_rev_o")
        # the roll canvass of January and February 2025: electors found not living at their address were removed under
        # objection, and those removed in error are put back when they come forward
        k = rng.poisson(n * 0.006 * 0.015)
        for _ in range(k):
            ref, eno = existing()
            sex = "M" if rng.random() < 0.5 else "F"
            by = int(rng.integers(1940, 2006))
            d0 = _dt.date(2025, 1, 13) + _dt.timedelta(days=int(rng.integers(0, 40)))
            while not _workday(d0):
                d0 += _dt.timedelta(days=1)
            t0 = business(d0)
            back = (t0 + _dt.timedelta(days=int(rng.integers(30, 540)))).date()
            if _workday(back):
                put_right(business(back), ("ORPHAN_OLD", t0), True, eno, ref, e, sex, by, kind="pre_rev")
    # other removals: overseas for three years (a December batch), duplicates, objections, and on the new platform
    # removals at the elector's own request under the reused code 01
    for e in all_elec:
        n = electors[e]
        for reason, rate, plat in (("03", 0.0006, None), ("04", 0.0001, None), ("01", 0.0006, "new")):
            k = rng.poisson(n * rate * (len(days) / 365.0))
            for _ in range(k):
                d = days[int(rng.integers(0, len(days)))]
                if not _workday(d) or (plat == "new" and d < W.PLATFORM_SWITCH):
                    continue
                ref, eno = existing()
                add(business(d), "DEL", reason, "", "A", eno, ref, e, "R", "M" if rng.random() < 0.5 else "F",
                    int(rng.integers(1945, 2006)), kind="other_del")
        k = rng.poisson(n * 0.0012)
        batch = _dt.datetime(2025, 12, 3, 21, 15)
        for _ in range(k):
            ref, eno = existing()
            add(batch + _dt.timedelta(seconds=int(rng.integers(0, 2400))), "DEL", "02", "", "A", eno, ref, e, "O",
                "M" if rng.random() < 0.5 else "F", int(rng.integers(1950, 2003)), kind="other_del")

    def second_form(tid, ref1, d, e, sex, by):
        """an elector enrolled on the old platform sends a second form: a new record under their number, and overnight
        the first record removed as a duplicate"""
        d2 = d + _dt.timedelta(days=int(rng.integers(3, 45)))
        while not _workday(d2):
            d2 += _dt.timedelta(days=1)
        if d2 + _dt.timedelta(days=1) >= W.PLATFORM_SWITCH:
            return
        add(business(d2), "NEW", "", "CAM" if rng.random() < 0.6 else "PAP", "A", ("SAME", tid), new_ref(), e, "R", sex,
            by, kind="dup_new")
        add(overnight(d2), "DEL", "03", "", "A", ("SAME", tid), ref1, e, "R", sex, by, kind="dup_del")
    # new enrolments: provisional enrolments transferred at 18 (old platform: the first of the month at 06:00 for the
    # month's birthdays; new: every day at 06:00 for that day's), direct enrolments, campaign enrolments
    for e in all_elec:
        n = electors[e]
        turning = n * 0.0185                     # electors' worth of 18th birthdays a year in the electorate
        for d in days:
            if d < W.PLATFORM_SWITCH:
                if d.day == 1:
                    k = rng.poisson(turning * 0.56 / 12.0)
                    t0 = _dt.datetime.combine(d, _dt.time(6, 0))
                else:
                    k = 0
            else:
                k = rng.poisson(turning * 0.56 / 365.0)
                t0 = _dt.datetime.combine(d, _dt.time(6, 0))
            for _ in range(k):
                add(t0 + _dt.timedelta(seconds=int(rng.integers(0, 1500))), "NEW", "", "PRV", "A", "NEW_NO", new_ref(), e,
                    "R", "M" if rng.random() < 0.51 else "F", 2007 + (d.year - 2025), kind="new")
            # direct enrolments: online ones are processed overnight, paper and campaign ones in office hours
            k_on = rng.poisson(n * 0.0215 / 365.0)
            for _ in range(k_on):
                t = _dt.datetime.combine(d, _dt.time(0, 30)) + _dt.timedelta(seconds=int(rng.integers(0, 4 * 3600)))
                status = "R" if rng.random() < 0.045 else "A"
                addr = "O" if rng.random() < 0.02 else "R"
                sex, by, ref1 = "M" if rng.random() < 0.5 else "F", int(rng.integers(1950, 2007)), new_ref()
                tid = add(t, "NEW", "", "ONL", status, "NEW_NO" if status == "A" else "", ref1, e, addr, sex, by,
                          kind="new")
                if tid and status == "A" and addr == "R" and d < W.PLATFORM_SWITCH and rng.random() < 0.022:
                    second_form(tid, ref1, d, e, sex, by)
            if _workday(d):
                k_p = rng.poisson(n * 0.0075 / 250.0)
                for _ in range(k_p):
                    status = "R" if rng.random() < 0.06 else "A"
                    src = "PAP" if rng.random() < 0.8 else "CAM"
                    sex, by, ref1 = "M" if rng.random() < 0.5 else "F", int(rng.integers(1945, 2007)), new_ref()
                    tid = add(business(d), "NEW", "", src, status, "NEW_NO" if status == "A" else "", ref1, e, "R", sex,
                              by, kind="new")
                    if tid and status == "A" and d < W.PLATFORM_SWITCH and rng.random() < 0.022:
                        second_form(tid, ref1, d, e, sex, by)
    # re-enrolments of electors removed in the window (overseas removals who came back, objections followed by a new
    # application), all on the new platform: the same record and number
    removed = [r for r in rows if r[2] == "DEL" and r[3] in ("02", "04")]
    for r in removed:
        if rng.random() < 0.06:
            back = r[13] + _dt.timedelta(days=int(rng.integers(20, 200)))
            if _workday(back.date()) and back.date() >= W.PLATFORM_SWITCH:
                add(business(back.date()), "NEW", "", "ONL", "A", r[6], r[7], r[16], "R", r[10], r[11], kind="reenrol")
    rows.sort(key=lambda r: (r[13], r[0]))
    # transaction ids in processing order: the old platform's running numbers, the new platform's random hex keys;
    # elector numbers for new electors issued in the same order
    by_tmp = {r[0]: r for r in rows}
    ids, used_hex = {}, set()

    def hexkey():
        while True:
            k = "%016x" % int(rng.integers(1 << 60, (1 << 63) - 1))
            if k not in used_hex:
                used_hex.add(k)
                return k
    seq = 132001
    for r in rows:
        if r[14] == "old":
            nid = "R25-%07d" % seq
            seq += int(rng.integers(1, 4))
        else:
            nid = hexkey()
        ids[r[0]] = nid
        r[0] = nid
        if r[2] == "NEW" and r[5] == "A" and r[6] == "NEW_NO":
            r[6] = new_no()
    per_day = (seq - 132001) / float((switch - start).days)
    old_used = set()

    def old_key(t0):
        """the old platform's running number of a transaction before the extract, at its daily pace"""
        k = 132001 - int((start - t0).total_seconds() / 86400.0 * per_day) - int(rng.integers(1, 40))
        while k in old_used:
            k -= 1
        old_used.add(k)
        return "R25-%07d" % k
    for r in rows:
        if isinstance(r[6], tuple):
            r[6] = by_tmp[r[6][1]][6]
        x = r[12]
        if isinstance(x, tuple):
            r[12] = old_key(x[1])
        elif x == "ORPHAN_NEW":
            r[12] = hexkey()
        elif x:
            r[12] = ids[x]
        r[17] = ids[r[17]] if isinstance(r[17], str) and r[17] else ""
        r[8] = (W.NUMBER_2020 if r[14] == "old" else W.NUMBER)[r[16]]
    return rows, electors
