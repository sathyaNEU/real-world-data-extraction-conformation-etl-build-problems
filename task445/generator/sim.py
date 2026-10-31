"""The clean truth: every death of an Ellesmoor resident from 2021 to the extract, the non-residents who died in the
board's area once the medical examiner system began, each death's certification route and registration date, the
registrations and corrections on the register, and the two medical examiner offices' cases. Seeded and
deterministic; pack.py writes the files from this and nothing else."""
import datetime as dt
import math

import numpy as np

import world as W

D = dt.timedelta
SA_F = ["Shamim", "Rukhsana", "Nasreen", "Parveen", "Gurmeet", "Surinder", "Bilquis", "Zubeida", "Kulwant", "Sakina"]
SA_M = ["Mohammed", "Abdul", "Mohammad", "Gurdev", "Mushtaq", "Bashir", "Harbans", "Iqbal", "Ghulam", "Rashid"]
SA_SURNAMES = {"Khanom", "Singh", "Begum", "Ali", "Hussain", "Ahmed", "Kaur"}


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += D(days=1)


def season(d):
    doy = d.timetuple().tm_yday
    return 1.0 + 0.17 * math.cos(2 * math.pi * (doy - 15) / 365.25)


def covid(d):
    if dt.date(2021, 1, 1) <= d <= dt.date(2021, 2, 28):
        return 1.22
    if dt.date(2021, 3, 1) <= d <= dt.date(2021, 3, 31):
        return 1.06
    return 1.0


def lam(place, d):
    yrs = (d - dt.date(2025, 7, 1)).days / 365.25
    base = W.POP[place] * W.RATE[place] / 365.25 * (1.004 ** yrs) * (0.995 ** yrs)
    m = season(d) * covid(d)
    if W.HEAT22[0] <= d <= W.HEAT22[1] + D(days=1):
        m *= 1.07
    return base * m


class Truth:
    pass


def business_days_after(d, n):
    out = d
    k = 0
    while k < n:
        out += D(days=1)
        if out.weekday() < 5:
            k += 1
    return out


def build():
    rng = np.random.default_rng(W.SEED)
    T = Truth()

    # ---------------------------------------------------------------- postcodes and the lookup
    pcs = {}
    letters = "ABDEFGHJLNPQRSTUWXYZ"
    for p in W.NAMES:
        lst = []
        for dno in W.DISTRICTS[p]:
            for sec in range(1, 10):
                for _ in range(5):
                    lst.append("EL%d %d%s%s" % (dno, sec, letters[rng.integers(20)], letters[rng.integers(20)]))
        lst = sorted(set(lst))
        pcs[p] = lst
    lookup = []      # (postcode, place, introduced, terminated, replaced_by)
    usual_pool = {}
    for p in W.NAMES:
        pool = []
        for pc in pcs[p]:
            if rng.random() < 0.05:
                term = dt.date(2023, 1, 1) + D(days=int(rng.integers(0, 1080)))
                dno = pc.split()[0]
                newpc = "%s %d%s%s" % (dno, int(rng.integers(1, 10)), letters[rng.integers(20)], letters[rng.integers(20)])
                while newpc in pcs[p] or any(newpc == x[0] for x in lookup):
                    newpc = "%s %d%s%s" % (dno, int(rng.integers(1, 10)), letters[rng.integers(20)], letters[rng.integers(20)])
                lookup.append((pc, p, dt.date(1998, 6, 1), term, newpc))
                lookup.append((newpc, p, term, None, ""))
                pool.append((pc, newpc, term))
            else:
                lookup.append((pc, p, dt.date(1998, 6, 1), None, ""))
                pool.append((pc, None, None))
        usual_pool[p] = pool
    T.lookup = sorted(lookup)
    care_pc = {p: [x[0] for x in usual_pool[p][::23]][:8] for p in W.NAMES}
    hosp_pc = {"North": "EL2 4HR", "South": "EL31 2HG"}
    hospice_pc = {"North": "EL14 7HW", "South": "EL37 3HS"}
    for a, pc in list(hosp_pc.items()) + list(hospice_pc.items()):
        pl = W.HOSPITAL_PLACE[a] if pc in hosp_pc.values() else W.HOSPICE_PLACE[a]
        if not any(x[0] == pc for x in T.lookup):
            T.lookup.append((pc, pl, dt.date(1998, 6, 1), None, ""))
    T.lookup = sorted(T.lookup)
    outside_pc = ["KX%d %d%s%s" % (int(rng.integers(1, 30)), int(rng.integers(1, 10)), letters[rng.integers(20)],
                                    letters[rng.integers(20)]) for _ in range(400)]

    # ---------------------------------------------------------------- daily counts
    days = list(daterange(W.START, W.LAST_DEATH))
    counts = {}
    for p in W.NAMES:
        for d in days:
            if W.W0 <= d <= W.W1:
                continue
            counts[(p, d)] = int(rng.poisson(lam(p, d)))
    # the expected deaths the fund files: the mean of the 2021 to 2025 summers' deaths, raised by 0.4 per cent a
    # year of population growth to 2026
    for p in W.NAMES:
        for y in range(2021, 2026):
            a, b = W.summer(y)
            for d in daterange(a, b):
                counts.setdefault((p, d), int(rng.poisson(lam(p, d))))
    T.summer_final = {(p, y): sum(counts[(p, d)] for d in daterange(*W.summer(y))) for p in W.NAMES
                      for y in range(2021, 2026)}
    T.expected = {}
    for p in W.NAMES:
        mean = sum(T.summer_final[(p, y)] for y in range(2021, 2026)) / 5.0
        growth = sum(1.004 ** (2026 - y) for y in range(2021, 2026)) / 5.0
        T.expected[p] = int(round(mean * growth))
    T.total26 = {p: int(round(T.expected[p] * (1 + W.EXCESS[p]))) for p in W.NAMES}
    heatdays = list(daterange(W.HEAT26[0], W.HEAT26[1] + D(days=2)))
    T.heat_excess = {}
    for p in W.NAMES:
        wdays = list(daterange(W.W0, W.W1))
        lw = np.array([lam(p, d) for d in wdays])
        base_total = int(round(T.expected[p] * float(lw.sum()) / float(lw.sum())))
        heat = T.total26[p] - base_total
        T.heat_excess[p] = heat
        base = rng.multinomial(base_total, lw / lw.sum())
        hw = np.array([1.0 if d <= W.HEAT26[1] else 0.5 for d in heatdays])
        hx = rng.multinomial(max(heat, 0), hw / hw.sum())
        for d, c in zip(wdays, base):
            counts[(p, d)] = int(c)
        T.heatx = getattr(T, "heatx", {})
        for d, c in zip(heatdays, hx):
            T.heatx[(p, d)] = int(c)

    # ---------------------------------------------------------------- deaths of residents
    seen = set()
    deaths = []

    def draw_name(sex):
        while True:
            sur = W.SURNAMES[int(rng.integers(len(W.SURNAMES)))]
            if sur in SA_SURNAMES:
                fn = (SA_F if sex == "F" else SA_M)[int(rng.integers(10))]
            else:
                fn = (W.FORENAMES_F if sex == "F" else W.FORENAMES_M)[int(rng.integers(50))]
            if rng.random() < 0.42 and sur not in SA_SURNAMES:
                mid = W.MIDDLE[int(rng.integers(0, 10)) if sex == "F" else int(rng.integers(10, 20))]
                if mid != fn:
                    fn = fn + " " + mid
            return sur, fn

    age_bands = [(18, 59, 0.07), (60, 69, 0.12), (70, 79, 0.22), (80, 89, 0.35), (90, 103, 0.24)]
    aw = np.array([b[2] for b in age_bands])

    def one_death(p, d, heat):
        sex = "F" if rng.random() < 0.51 else "M"
        bi = int(rng.choice(5, p=aw / aw.sum()))
        lo, hi, _ = age_bands[bi]
        if p == "Ashwold" and bi < 4 and rng.random() < 0.15:
            lo, hi, _ = age_bands[bi + 1]
        age = int(rng.integers(lo, hi + 1))
        dob = d - D(days=int(age * 365.25 + rng.integers(0, 365)))
        sur, fn = draw_name(sex)
        while (sur.lower(), fn.lower(), dob) in seen:
            sur, fn = draw_name(sex)
        seen.add((sur.lower(), fn.lower(), dob))
        upc, newpc, term = usual_pool[p][int(rng.integers(len(usual_pool[p])))]
        if newpc and term and d >= term and rng.random() < 0.7:
            upc = newpc
        home_share = W.HOME[p]
        if heat:
            home_share = {"Ashwold": 0.78, "Hollinsgate": 0.46}.get(p, 0.30)
        r = rng.random()
        if r < home_share:
            pod = "Home"
        elif r < home_share + 0.21:
            pod = "Care home"
        elif r < home_share + 0.21 + 0.06:
            pod = "Hospice"
        elif r < home_share + 0.21 + 0.06 + 0.02:
            pod = "Other"
        else:
            pod = "Hospital"
        area = W.OFFICE[p]
        u = rng.random()
        if pod == "Hospital" and u < 0.08:
            area = "Outside"
        elif pod == "Hospital" and u < 0.14:
            area = "South" if area == "North" else "North"
        if pod == "Home":
            pdpc, podname = upc, "Usual address"
        elif pod == "Care home":
            pdpc, podname = care_pc[p][int(rng.integers(len(care_pc[p])))], "Care home"
            if pdpc == upc:
                pass
            if rng.random() < 0.8:
                upc = pdpc
        elif pod == "Hospice":
            pdpc, podname = hospice_pc[area if area != "Outside" else W.OFFICE[p]], W.HOSPICE[area if area != "Outside" else W.OFFICE[p]]
            area = area if area != "Outside" else W.OFFICE[p]
        elif pod == "Hospital":
            if area == "Outside":
                pdpc = outside_pc[int(rng.integers(len(outside_pc)))]
                podname = W.OUTSIDE_HOSPITALS[int(rng.integers(3))]
            else:
                pdpc, podname = hosp_pc[area], W.HOSPITAL[area]
        else:
            pdpc, podname = upc, "Other private address"
        return dict(place=p, dod=d, sex=sex, age=age, dob=dob, surname=sur, forenames=fn, usual_pc=upc,
                    pod=pod, pod_name=podname, pod_pc=pdpc, area=area, heat=heat, resident=True,
                    marital=W.MARITAL[int(rng.integers(5))] if age > 25 else "Single",
                    occupation=W.OCCUPATIONS[int(rng.integers(0, 15)) if age >= 65 else int(rng.integers(14, 20))])

    for d in days:
        for p in W.NAMES:
            for _ in range(counts.get((p, d), 0)):
                deaths.append(one_death(p, d, False))
            for _ in range(getattr(T, "heatx", {}).get((p, d), 0)):
                deaths.append(one_death(p, d, True))

    # non-residents dying in the board's area once the medical examiners began (they reach the logs only)
    for d in daterange(W.ME_START, W.LAST_DEATH):
        for area in ("North", "South"):
            n = int(rng.poisson(1.6 if area == "North" else 1.3))
            for _ in range(n):
                sex = "F" if rng.random() < 0.5 else "M"
                age = int(rng.integers(45, 99))
                dob = d - D(days=int(age * 365.25 + rng.integers(0, 365)))
                sur, fn = draw_name(sex)
                while (sur.lower(), fn.lower(), dob) in seen:
                    sur, fn = draw_name(sex)
                seen.add((sur.lower(), fn.lower(), dob))
                hosp = rng.random() < 0.8
                deaths.append(dict(place=None, dod=d, sex=sex, age=age, dob=dob, surname=sur, forenames=fn,
                                   usual_pc=outside_pc[int(rng.integers(len(outside_pc)))],
                                   pod="Hospital" if hosp else "Hospice",
                                   pod_name=W.HOSPITAL[area] if hosp else W.HOSPICE[area],
                                   pod_pc=hosp_pc[area] if hosp else hospice_pc[area], area=area, heat=False,
                                   resident=False, marital="Married", occupation="Retired"))

    deaths.sort(key=lambda x: (x["dod"], x["surname"], x["forenames"], x["dob"]))

    # ---------------------------------------------------------------- certification and registration
    held_left = dict(W.HELD)
    for x in deaths:
        d = x["dod"]
        me = d >= W.ME_START and x["area"] in ("North", "South")
        alone_home = x["pod"] == "Home"
        found_late = False
        if x["heat"] and alone_home and x["resident"] and held_left.get(x["place"], 0) > 0:
            found_late = True
            held_left[x["place"]] -= 1
        x["found_late"] = found_late
        if found_late:
            route = "inquest"
        else:
            ref = 0.26 if me else 0.28
            if alone_home:
                ref = 0.45
            if rng.random() < ref:
                v = rng.random()
                route = "100A" if v < 0.36 else ("100B" if v < 0.82 else "inquest")
            else:
                route = "mccd"
            if W.W0 <= d <= W.W1 and d.year == 2026 and x["area"] == "Outside" and route == "inquest":
                route = "100B"
        x["route"] = route
        # registration
        if route == "mccd":
            delay = int(min(40, 1 + rng.gamma(2.2, 1.9 if me else 1.4)))
        elif route == "100A":
            delay = int(8 + rng.integers(0, 20))
        elif route == "100B":
            delay = int(14 + rng.integers(0, 34))
        else:
            med = 200 if (x["area"] == "North" or (x["area"] == "Outside" and W.OFFICE.get(x["place"]) == "North")) else 150
            dur = int(rng.lognormal(math.log(med), 0.45))
            if found_late:
                dur = max(dur, (W.EXTRACT - d).days + 25 + int(rng.integers(0, 60)))
            delay = dur + int(rng.integers(1, 6))
            x["inquest_opened"] = d + D(days=int(5 + rng.integers(0, 16)))
            x["inquest_concluded"] = d + D(days=delay - int(rng.integers(1, 4)))
        x["misaddr"] = None
        if (d.year == 2025 and x["resident"] and x["pod"] == "Care home" and x["area"] != "Outside"
                and x["place"] in ("Thornley Vale", "Moorbridge") and route in ("mccd", "100A")
                and rng.random() < 0.30):
            # a care home resident registered at the family's address in another place, by the care home's manager
            fam = "Hollinsgate" if x["place"] == "Thornley Vale" else "Calderholt"
            x["misaddr"] = (usual_pool[fam][int(rng.integers(len(usual_pool[fam])))][0], fam)
            delay = int(1 + rng.integers(0, 3))
        x["reg_date"] = d + D(days=delay)
        x["registered"] = x["reg_date"] <= W.EXTRACT
        # the coroner's steps
        if route in ("100A", "100B", "inquest"):
            x["referred"] = d + D(days=int(rng.integers(0, 4)))
            if route == "100A":
                x["decision"] = x["referred"] + D(days=int(1 + rng.integers(0, 5)))
            elif route == "100B":
                x["decision"] = x["referred"] + D(days=int(1 + rng.integers(0, 4)))
            else:
                x["decision"] = x["inquest_opened"]
        x["me"] = me
    T.deaths = deaths

    # ---------------------------------------------------------------- the medical examiner offices' cases
    seq = {"North": {}, "South": {}}
    cref = {"North": {}, "South": {}}
    cases = []

    def next_ref(area, y):
        seq[area][y] = seq[area].get(y, 0) + 1
        return ("N%02d-%05d" if area == "North" else "SE-%02d-%05d") % (y % 100, seq[area][y])

    def next_cref(area, y):
        cref[area][y] = cref[area].get(y, 0) + 1
        return ("NE/%02d/%04d" if area == "North" else "SC%02d-%04d") % (y % 100, cref[area][y])

    for x in deaths:
        if not x["me"]:
            continue
        area = x["area"]
        d = x["dod"]
        if x["route"] == "mccd":
            comp = business_days_after(d, int(1 + rng.integers(0, 4)))
            if rng.random() < 0.06:
                # the medical examiner asked the coroner's officer for advice and certified: one row, a reference
                cases.append(dict(death=x, area=area, ref=next_ref(area, comp.year), completed=comp, outcome="MCCD",
                                  decision="Advice only", decision_date=comp, cref=next_cref(area, comp.year),
                                  relog=False, forenames=x["forenames"]))
            else:
                cases.append(dict(death=x, area=area, ref=next_ref(area, comp.year), completed=comp, outcome="MCCD",
                                  decision=None, decision_date=None, cref="", relog=False, forenames=x["forenames"]))
            continue
        comp = x["referred"]
        cr = next_cref(area, comp.year)
        x["cref"] = cr
        fn = x["forenames"]
        first = fn.split()[0]
        relog_variant = False
        if x["route"] == "100A" and first in W.VARIANT and not (W.W0 <= d <= W.W1 + D(days=40)) \
                and rng.random() < 0.55:
            fn = W.VARIANT[first] + fn[len(first):]
            relog_variant = True
        dec = {"100A": "100A", "100B": "Post-mortem", "inquest": "Inquest opened"}[x["route"]]
        dd = x["decision"]
        if x["route"] == "inquest" and x.get("inquest_opened") and x["inquest_opened"] > W.EXTRACT:
            dec, dd = "Awaiting decision", None
        if dd is not None and dd > W.EXTRACT:
            dec, dd = "Awaiting decision", None
        cases.append(dict(death=x, area=area, ref=next_ref(area, comp.year), completed=comp, outcome="Referred",
                          decision=dec, decision_date=dd, cref=cr, relog=False, forenames=fn, variant=relog_variant))
        if x["route"] == "100A" and dd is not None:
            rc = business_days_after(dd, int(1 + rng.integers(0, 2)))
            if W.quarter_fy(rc) != W.quarter_fy(comp) or rc.year != comp.year:
                # keep a returned death inside the quarter its referral was completed in
                rc = comp + D(days=0)
            if rc <= W.EXTRACT:
                cases.append(dict(death=x, area=area, ref=next_ref(area, rc.year), completed=rc, outcome="MCCD",
                                  decision="100A", decision_date=dd, cref=cr, relog=True,
                                  forenames=x["forenames"]))
    cases.sort(key=lambda c: (c["area"], c["completed"], c["ref"]))
    T.cases = cases

    # ---------------------------------------------------------------- register rows (residents only)
    rows = []
    for x in deaths:
        if not x["resident"] or not x["registered"]:
            continue
        cert = {"mccd": "Medical certificate", "100A": "Medical certificate", "100B": "Coroner (post-mortem)",
                "inquest": "Coroner (inquest)"}[x["route"]]
        if x["route"] in ("mccd", "100A") and x["dod"] >= W.ME_START:
            cert = "Medical certificate (medical examiner)"
        if x["area"] == "Outside":
            dist = "Kexley"
        else:
            dplace = x["place"] if x["pod"] in ("Home", "Care home", "Other") else (
                W.HOSPITAL_PLACE[x["area"]] if x["pod"] == "Hospital" else W.HOSPICE_PLACE[x["area"]])
            dist = W.DISTRICT_OF_PLACE[dplace]
        x["district"] = dist
        if x["misaddr"]:
            # registered at the family's address; corrected to the care home in the district's March 2026 review
            rows.append(dict(death=x, kind="Registration", date=x["reg_date"], marital=x["marital"],
                             occupation=x["occupation"], cert=cert, usual_pc=x["misaddr"][0], place=x["misaddr"][1]))
            cd = dt.date(2026, 3, 16) + D(days=int(rng.integers(0, 5)))
            rows.append(dict(death=x, kind="Correction", date=cd, marital=x["marital"], occupation=x["occupation"],
                             cert=cert, usual_pc=x["usual_pc"], place=x["place"]))
            continue
        rows.append(dict(death=x, kind="Registration", date=x["reg_date"], marital=x["marital"],
                         occupation=x["occupation"], cert=cert, usual_pc=x["usual_pc"], place=x["place"]))
        if rng.random() < 0.026:
            cd = x["reg_date"] + D(days=int(10 + rng.integers(0, 290)))
            if cd <= W.EXTRACT:
                field = "occupation" if rng.random() < 0.6 else "marital"
                occ, mar = x["occupation"], x["marital"]
                if field == "occupation":
                    occ = W.OCCUPATIONS[(W.OCCUPATIONS.index(occ) + 3) % len(W.OCCUPATIONS)]
                else:
                    mar = W.MARITAL[(W.MARITAL.index(mar) + 1) % len(W.MARITAL)]
                rows.append(dict(death=x, kind="Correction", date=cd, marital=mar, occupation=occ, cert=cert,
                                 usual_pc=x["usual_pc"], place=x["place"]))
    rows.sort(key=lambda r: (r["date"], r["death"]["district"], r["kind"], r["death"]["surname"]))
    # entry numbers run on through the years in each district; a correction repeats the entry's number
    nums = {}
    entry = {}
    for r in rows:
        x = r["death"]
        k = id(x)
        if r["kind"] == "Registration":
            nums[x["district"]] = nums.get(x["district"], 0) + 1
            entry[k] = nums[x["district"]]
        r["entry"] = entry.get(k)
    rows = [r for r in rows if r["entry"] is not None]
    T.rows = rows
    T.pcs = pcs
    T.outside_pc = outside_pc
    return T
