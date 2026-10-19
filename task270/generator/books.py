"""The mutual's books built from the world: policy and term numbers on the legacy system and the platform, full
postcodes where the platform keeps them, the mid-term adjustments, the claims as each claims system holds them (the
legacy system for notifications to 30 June 2025, run off there, the platform from 1 July 2025), the glass partner's
jobs, the thefts with their police references and the salvage agent's sales. Every record keeps its world key, so
the checks can tie it back to the truth."""
import datetime as dt

import numpy as np

import common as K
import world as W

FORCE = {"NEC": ["NTH", "CUM", "DUR", "CLE"], "NWE": ["GMP", "MER", "LAN", "CHE"], "YHU": ["WYP", "SYP", "HUM", "NYP"],
         "EMI": ["NOT", "LEI", "DER", "LIN", "NHA"], "WMI": ["WMP", "WAR", "STA", "WME"],
         "EOE": ["CAM", "NOR", "SUF", "ESX", "BED"], "SEA": ["TVP", "SUR", "SUX", "KNT", "HAM"],
         "SWW": ["ASP", "DEV", "GLO", "SWP", "WWP"]}
INWARD = "ABDEFGHJLNPQRSTUWXYZ"
BST = {2022: (dt.date(2022, 3, 27), dt.date(2022, 10, 30)), 2023: (dt.date(2023, 3, 26), dt.date(2023, 10, 29)),
       2024: (dt.date(2024, 3, 31), dt.date(2024, 10, 27)), 2025: (dt.date(2025, 3, 30), dt.date(2025, 10, 26)),
       2026: (dt.date(2026, 3, 29), dt.date(2026, 10, 25))}


def utc(local):
    """A UK local time as UTC (British Summer Time one hour ahead)."""
    a, b = BST[local.year]
    return local - dt.timedelta(hours=1) if a <= local.date() < b else local


def term_on(term, day):
    """The garaging district, cover and registration a term carries on a day (mid-term adjustments applied)."""
    d, c, r = term["district"], term["cover"], term["reg"]
    for m in term["mtas"]:
        if m["day"] <= day:
            if m["kind"] == "Change of address":
                d = m["district"]
            elif m["kind"] == "Change of cover":
                c = m["cover"]
            else:
                r = m["reg"]
    return d, c, r


GLASS_SALT, THEFT_SALT = 2, 0      # the glass and theft streams, apart from the accident claims
# glass by region: the partner's price level and the share of jobs that are replacements (older cars, motorway miles)
GLASS_PRICE = {"NEC": 0.93, "NWE": 0.99, "YHU": 0.95, "EMI": 0.97, "WMI": 1.02, "EOE": 1.05, "SEA": 1.11, "SWW": 1.00}
GLASS_REPL = {"NEC": 0.43, "NWE": 0.49, "YHU": 0.45, "EMI": 0.47, "WMI": 0.50, "EOE": 0.46, "SEA": 0.52, "SWW": 0.44}


def plate(reg):
    """A plate clear of the letter run the leak sweep reserves (LLM): the few drawn that way take the next series."""
    return reg[:-3] + "LLN" if reg.endswith("LLM") else reg


def books(w, seed=W.SEED):
    for t in w["terms"]:
        t["reg"] = plate(t["reg"])
    rng = np.random.default_rng([seed, 11])
    trng = np.random.default_rng([seed, 12, THEFT_SALT])
    grng = np.random.default_rng([seed, 13, GLASS_SALT])
    srng = np.random.default_rng([seed, 14])
    terms = w["terms"]
    by_pid = {}
    for i, t in enumerate(terms):
        by_pid.setdefault(t["pid"], []).append(i)
    for pid in by_pid:
        by_pid[pid].sort(key=lambda i: terms[i]["start"])
    # ---------------------------------------------------------------- vehicles and postcodes
    inward = {}

    def new_inward(key):
        if key not in inward:
            inward[key] = "%d%s%s" % (rng.integers(1, 10), INWARD[rng.integers(20)], INWARD[rng.integers(20)])

    for pid in sorted(by_pid):
        for i in by_pid[pid]:
            t = terms[i]
            new_inward((pid, t["district"]))
            for m in t["mtas"]:
                if m["kind"] == "Change of vehicle":
                    m["reg"] = plate(W.registration(rng, int(min(m["day"].year, t["veh_year"] + rng.integers(1, 7)))))
                    m["veh_group"] = int(min(48, max(3, t["veh_group"] + rng.integers(-8, 9))))
                elif m["kind"] == "Change of address":
                    new_inward((pid, m["district"]))
    # ---------------------------------------------------------------- policy numbers
    legacy_no, platform_no, first_plat, term_seq = {}, {}, {}, {}
    order = sorted(by_pid, key=lambda p: (terms[by_pid[p][0]]["start"], p))
    leg = rng.choice(np.arange(1, 9000000), size=len(order), replace=False)
    plat = rng.choice(np.arange(1, 9000000), size=len(order), replace=False)
    for k, pid in enumerate(order):
        idx = by_pid[pid]
        seq0 = int(rng.integers(1, 12)) if terms[idx[0]]["start"] < K.FIRST_INCEPTION else 1
        for j, i in enumerate(idx):
            term_seq[i] = seq0 + j
        if terms[idx[0]]["start"] < K.MIGRATION:
            legacy_no[pid] = "FM%07d" % leg[k]
        on_platform = [i for i in idx if terms[i]["start"] >= K.MIGRATION]
        if on_platform:
            platform_no[pid] = "FNM-%07d" % plat[k]
            first_plat[pid] = terms[on_platform[0]]["start"]

    def term_ref(i):
        t = terms[i]
        return legacy_no[t["pid"]] if t["start"] < K.MIGRATION else platform_no[t["pid"]]

    def quoted_ref(i, day):
        """The number a policyholder quotes on a day: the platform number once the policy has renewed onto it."""
        pid = terms[i]["pid"]
        if pid in first_plat and day >= first_plat[pid]:
            return platform_no[pid]
        return term_ref(i)

    # ---------------------------------------------------------------- terms
    leg_terms, plat_terms = [], []
    for i, t in enumerate(terms):
        if t["start"] < K.FIRST_INCEPTION or t["start"] > K.EXTRACT:
            continue
        prem_net = t["base"] * K.REL[t["step"]] * (1.11 if t["protected"] else 1.0)
        cancelled = t["cancelled"] if (t["cancelled"] and t["cancelled"] < K.EXTRACT) else None
        row = dict(i=i, pid=t["pid"], ref=term_ref(i), seq=term_seq[i], start=t["start"], end=t["end"],
                   cancelled=cancelled, district=t["district"], inward=inward[(t["pid"], t["district"])],
                   step=t["step"], protected=t["protected"], cover=t["cover"], reg=t["reg"],
                   veh_group=t["veh_group"], veh_year=t["veh_year"], age=W.AGE_BANDS[t["age"]],
                   channel=str(t["channel"]), prem_net=round(prem_net, 2), ipt=round(prem_net * K.IPT, 2),
                   extras=[e for e, p in (("LEGAL", 0.42), ("BREAKDOWN", 0.31), ("COURTESY", 0.27))
                           if rng.random() < p])
        (leg_terms if t["start"] < K.MIGRATION else plat_terms).append(row)
    crosswalk = sorted((legacy_no[p], platform_no[p], first_plat[p]) for p in legacy_no if p in platform_no)
    mtas = []
    for i, t in enumerate(terms):
        if t["start"] < K.FIRST_INCEPTION or t["start"] > K.EXTRACT:
            continue
        for m in t["mtas"]:
            if m["day"] > K.EXTRACT:
                continue
            prem = {"Change of address": rng.normal(18, 35), "Change of vehicle": rng.normal(45, 80),
                    "Change of cover": (rng.uniform(60, 160) if m["cover"] == "COMP" else -rng.uniform(50, 140))}[
                m["kind"]]
            frac = max(0.0, (t["end"] - m["day"]).days / 365.0)
            mtas.append(dict(i=i, ref=term_ref(i), seq=term_seq[i], start=t["start"], day=m["day"], kind=m["kind"],
                             district=m["district"], inward=inward[(t["pid"], m["district"])], cover=m["cover"],
                             reg=m.get("reg", ""), veh_group=m.get("veh_group"), prem=round(float(prem) * frac, 2),
                             system="L" if t["start"] < K.MIGRATION else "P"))
    # ---------------------------------------------------------------- claims (numbered at the end, in notification order)
    claims = []

    def notify(day, mean=3.0, cap=60, r=None):
        r = r or rng
        d = day + dt.timedelta(days=int(min(cap, r.exponential(mean))))
        return dt.datetime.combine(d, dt.time(int(r.integers(8, 20)), int(r.integers(0, 60)), int(r.integers(0, 60))))

    def system_of(when):
        return "L" if when.date() < K.MIGRATION else "P"

    def develop(c, cost, recovery=0.0, r=None, reopen=True):
        """Paid and outstanding at the extract: closed once settled, larger and recent claims still open."""
        r = r or rng
        age = (K.EXTRACT - c["notified"].date()).days
        settle = r.gamma(2.0, 30.0 + 0.010 * cost)
        if c.get("section") == "TPI":
            settle += r.gamma(3.0, 120.0)
        if age > settle:
            c["status"] = "Closed"
            c["paid"], c["outstanding"] = round(cost, 2), 0.0
            if reopen and r.random() < 0.02:
                c["status"] = "Reopened"
                c["outstanding"] = round(float(cost * r.uniform(0.05, 0.25)), 2)
        else:
            c["status"] = "Open"
            est = cost * float(np.exp(r.normal(0.0, 0.12)))
            frac = min(0.9, age / max(settle, 1.0))
            c["paid"] = round(cost * frac * r.uniform(0.3, 0.9), 2)
            c["outstanding"] = round(max(est - c["paid"], 25.0), 2)
        c["recovered"] = round(min(recovery, c["paid"]), 2) if c["status"] != "Open" else 0.0
        return c

    def claim(kind, ev, i, loss, notified, **kw):
        c = dict(kind=kind, ev=ev, term=i, loss=loss, notified=notified, system=system_of(notified),
                 ref=quoted_ref(i, notified.date()), liab="", section="", police=None, supplier="", supplier_ref="",
                 status="Closed", paid=0.0, outstanding=0.0, recovered=0.0, cost=0.0)
        c.update(kw)
        claims.append(c)
        return c

    events = w["events"]
    for k, e in enumerate(events):
        if e["kind"] not in ("AF", "NAF"):
            continue
        if e["kind"] == "NAF" and e["cover"] == "TPFT":
            # the other driver's insurer pays the policyholder direct; the mutual records the notification at nil
            nd = notify(e["day"], 2.0, 30)
            if nd.date() <= K.EXTRACT:
                claim("ACC", k, e["term"], e["day"], nd, liab="N", section="NTF", region=e["region"])
            continue
        if not e["claimed"]:
            continue
        nd = notify(e["day"])
        if nd.date() > K.EXTRACT:
            continue
        if e["kind"] == "NAF":
            liab, section = "N", "OD"
        else:
            liab = "S" if e["split"] else "F"
            if (K.EXTRACT - e["day"]).days < 120 and rng.random() < 0.35:
                liab = "P"
            elif rng.random() < 0.015:
                liab = "P"
            if e["cover"] == "COMP":
                section = str(rng.choice(["OD", "TPP", "TPI"], p=[0.55, 0.33, 0.12]))
            else:
                section = str(rng.choice(["TPP", "TPI"], p=[0.75, 0.25]))
        c = claim("ACC", k, e["term"], e["day"], nd, liab=liab, section=section, region=e["region"])
        rec = 0.0
        if e["kind"] == "NAF":
            rec = e["cost"] if rng.random() < 0.45 else e["cost"] * rng.uniform(0.85, 0.99)
        develop(c, round(e["cost"], 2), rec)
        c["cost"] = round(e["cost"], 2)
    # third-party claims rejected outright (liability denied): nil claims
    for i, t in enumerate(terms):
        if t["start"] < K.FIRST_INCEPTION or t["start"] > K.EXTRACT or rng.random() >= 0.012:
            continue
        span = ((t["cancelled"] or t["end"]) - t["start"]).days
        if span <= 0:
            continue
        day = t["start"] + dt.timedelta(days=int(rng.integers(0, span)))
        nd = notify(day, 10.0, 90)
        if nd.date() <= K.EXTRACT:
            claim("ACC", None, i, day, nd, liab="F", section=str(rng.choice(["TPP", "TPI"], p=[0.7, 0.3])),
                  region=W.district_region(term_on(t, day)[0], day))
    # ---------------------------------------------------------------- fires
    for k, e in enumerate(events):
        if e["kind"] != "FIRE":
            continue
        nd = notify(e["day"], 1.5, 20)
        if nd.date() > K.EXTRACT:
            continue
        c = claim("FIR", k, e["term"], e["day"], nd, region=e["region"], section="FIRE")
        cost = round(float(np.exp(np.log(5200.0) + 0.7 * rng.standard_normal())), 2)
        develop(c, cost)
        c["cost"] = cost
    # ---------------------------------------------------------------- thefts
    crime_seen = {}

    def crime_no(force, year):
        used = crime_seen.setdefault((force, year), set())
        while True:
            n = int(trng.integers(1000, 999999))
            if n not in used:
                used.add(n)
                return (force, year % 100, n)

    thefts = []
    for k, e in enumerate(events):
        if e["kind"] != "THEFT":
            continue
        t = terms[e["term"]]
        force = FORCE[e["region"]][int(trng.integers(len(FORCE[e["region"]])))]
        crime = crime_no(force, e["day"].year)
        age = max(0, e["day"].year - t["veh_year"])
        value = max(1500.0, (6000.0 + 520.0 * t["veh_group"]) * (0.86 ** age) * trng.lognormal(0.0, 0.18))
        u = trng.random()
        outcome = "from" if u < 0.10 else "total" if u < 0.66 else "damaged" if u < 0.92 else "undamaged"
        th = dict(ev=k, term=e["term"], day=e["day"], region=e["region"], outcome=outcome, crime=crime,
                  value=round(value, 2), claims=[], salvage=None)
        thefts.append(th)
        nd = notify(e["day"], 1.0, 10, trng)
        if nd.date() > K.EXTRACT:
            continue
        cost = {"from": round(float(trng.uniform(280, 1800)), 2), "total": round(value, 2),
                "damaged": round(float(trng.uniform(120, 650)), 2), "undamaged": 0.0}[outcome]
        c1 = claim("THF", k, e["term"], e["day"], nd, police=crime, region=e["region"], section="THEFT")
        if cost > 0:
            develop(c1, cost, r=trng)
        c1["cost"] = cost
        th["claims"].append(c1)
        if outcome == "damaged":
            # the car is found damaged: the repair is opened as its own claim, dated the day the car was found
            found = e["day"] + dt.timedelta(days=int(trng.integers(4, 46)))
            nd2 = notify(found, 1.0, 3, trng)
            if nd2.date() <= K.EXTRACT:
                c2 = claim("THF", k, e["term"], found, nd2, police=crime, region=e["region"], section="THEFT")
                cost2 = round(float(trng.uniform(900, 7000)), 2)
                develop(c2, cost2, r=trng)
                c2["cost"] = cost2
                th["claims"].append(c2)
        if outcome == "total" and trng.random() < 0.17:
            sold = e["day"] + dt.timedelta(days=int(trng.integers(45, 200)))
            if sold <= K.EXTRACT:
                th["salvage"] = (sold, round(value * float(trng.uniform(0.10, 0.32)), 2))
    # ---------------------------------------------------------------- glass
    glass = []
    jobs = []
    own_last = {}
    for k, e in enumerate(events):
        if e["kind"] not in ("GLASS", "GLASS_TPFT"):
            continue
        t = terms[e["term"]]
        last = min(t["cancelled"] or t["end"], t["end"])
        booked = dt.datetime.combine(min(e["day"] + dt.timedelta(days=int(grng.integers(0, 2))), last),
                                     dt.time(int(grng.integers(7, 21)), int(grng.integers(0, 60))))
        if booked.date() > K.EXTRACT:
            continue
        dist, cover, reg = term_on(t, booked.date())
        greg = W.district_region(dist, booked.date())
        customer = cover == "TPFT"
        network = customer or grng.random() < 0.85
        repl = grng.random() < GLASS_REPL[greg]
        if not network:
            # a second chip within three weeks of the last on the same car is the same damage, already claimed
            prev = own_last.get(t["pid"])
            if prev is not None and booked - prev < dt.timedelta(days=21):
                continue
            own_last[t["pid"]] = booked
        jobs.append(dict(ev=k, term=e["term"], day=e["day"], booked=booked, network=network, customer=customer,
                         repl=repl, camera=bool(e["camera"]), veh_group=e["veh_group"], follow=False))
        if not customer and not repl and grng.random() < 0.09:
            # the chip is repaired, then the crack spreads and the screen is replaced, by the same kind of repairer
            b2 = booked + dt.timedelta(days=int(grng.integers(6, 41)), hours=int(grng.integers(-4, 5)))
            if b2.date() <= K.EXTRACT and b2.date() <= (t["cancelled"] or t["end"]):
                jobs.append(dict(ev=k, term=e["term"], day=b2.date(), booked=b2, network=network, customer=False,
                                 repl=True, camera=bool(e["camera"]), veh_group=e["veh_group"], follow=True))
                if not network:
                    own_last[t["pid"]] = b2
    jobs.sort(key=lambda j: (j["booked"], j["ev"], j["follow"]))
    own_claimed = {}
    for j in jobs:
        t = terms[j["term"]]
        dist, cover, reg = term_on(t, j["booked"].date())
        price = GLASS_PRICE[W.district_region(dist, j["booked"].date())]
        if j["repl"]:
            net = round(float((240.0 + 6.0 * j["veh_group"] + grng.normal(0, 30)) * price), 2)
        else:
            net = round(float(grng.uniform(62, 88) * price), 2)
        calib = round(float(grng.uniform(135, 185) * price), 2) if (j["camera"] and j["repl"]) else 0.0
        fitted = j["booked"].date() + dt.timedelta(days=int(grng.integers(0, 6)))
        if grng.random() < 0.18:
            pool = K.REGIONS[int(grng.integers(8))][2]
            fit_district = pool[int(grng.integers(len(pool)))]
        else:
            fit_district = dist
        g = dict(j, region=W.district_region(dist, j["booked"].date()), district=dist, reg=reg, net=net, calib=calib,
                 fitted=fitted, fit_district=fit_district, ref=quoted_ref(j["term"], j["booked"].date()), claim=None,
                 calib_claim=None)
        glass.append(g)
        if g["customer"]:
            continue
        if g["network"]:
            prev = own_claimed.get(t["pid"])
            if g["booked"].year > 2025 and prev is not None and g["booked"] - prev < dt.timedelta(days=21):
                # the policyholder's own glazier is still on the job: the partner's booking is cancelled
                continue
            if g["booked"].date() >= K.MIGRATION:
                c = claim("WSC", g["ev"], g["term"], g["day"], g["booked"], region=g["region"], section="GLASS")
                cost = round(net + calib, 2)
                if (K.EXTRACT - fitted).days > 21:
                    c["status"], c["paid"] = "Closed", cost
                else:
                    c["status"], c["outstanding"] = "Open", cost
                c["cost"] = cost
                g["claim"] = c
        else:
            nd = notify(g["booked"].date(), 1.0, 7, grng)
            last = min(t["cancelled"] or t["end"], t["end"])
            if nd.date() > last:
                nd = dt.datetime.combine(last, nd.time())
            own_claimed[t["pid"]] = nd
            if nd.date() <= K.EXTRACT:
                gross = round(net * 1.2 * float(grng.uniform(1.00, 1.18)), 2)
                c = claim("WSC", g["ev"], g["term"], g["day"], nd, region=g["region"], section="GLASS")
                develop(c, gross, r=grng, reopen=False)
                c["cost"] = gross
                g["claim"] = c
                if calib:
                    # the policyholder's own glazier fits the screen but cannot set up the camera: the Society's
                    # partner recalibrates it a few days later, in a job of its own billed to the Society
                    cal = fitted + dt.timedelta(days=int(grng.integers(0, 4)))
                    when = dt.time(int(grng.integers(8, 18)), int(grng.integers(0, 60)))
                    d_cal = term_on(t, cal)[0]
                    away = grng.random() < 0.18
                    pool = K.REGIONS[int(grng.integers(8))][2]
                    fit_cal = pool[int(grng.integers(len(pool)))] if away else d_cal
                    if (cal.year == nd.year and cal <= K.EXTRACT and W.district_region(d_cal, cal)
                            == W.district_region(term_on(t, nd.date())[0], nd.date())):
                        gc = dict(ev=g["ev"], term=g["term"], day=g["day"], booked=dt.datetime.combine(cal, when),
                                  network=True, customer=False, repl=False, camera=True, veh_group=g["veh_group"],
                                  follow=g["follow"], calib_only=True, region=W.district_region(d_cal, cal),
                                  district=d_cal, reg=reg, net=0.0, calib=calib,
                                  fitted=cal + dt.timedelta(days=int(grng.integers(0, 3))), fit_district=fit_cal,
                                  ref=quoted_ref(g["term"], cal), claim=None, calib_claim=None, for_claim=c)
                        glass.append(gc)
                        g["cal_job"] = gc
                        if cal >= K.MIGRATION:
                            cf = claim("WSC", g["ev"], g["term"], g["day"], gc["booked"], region=gc["region"],
                                       section="GLASS")
                            if (K.EXTRACT - gc["fitted"]).days > 21:
                                cf["status"], cf["paid"] = "Closed", calib
                            else:
                                cf["status"], cf["outstanding"] = "Open", calib
                            cf["cost"] = calib
                            gc["claim"] = cf
    # ---------------------------------------------------------------- salvage: write-offs from accidents and fires,
    # and stolen cars recovered after the total loss was paid
    salvage = []
    for c in claims:
        if c["kind"] in ("ACC", "FIR") and c["section"] in ("OD", "FIRE") and c["cost"] > 6000 and srng.random() < 0.55:
            sold = c["notified"].date() + dt.timedelta(days=int(srng.integers(20, 120)))
            if sold <= K.EXTRACT:
                salvage.append(dict(claim=c, sold=sold, proceeds=round(c["cost"] * float(srng.uniform(0.08, 0.25)), 2)))
    for th in thefts:
        if th["salvage"] and th["claims"]:
            salvage.append(dict(claim=th["claims"][0], sold=th["salvage"][0], proceeds=th["salvage"][1]))
    # ---------------------------------------------------------------- claim numbers in notification order
    claims.sort(key=lambda c: (c["notified"], c["ev"] if c["ev"] is not None else -1, c["kind"], c["loss"]))
    nL, nP = 418230, 2500000
    for c in claims:
        if c["system"] == "L":
            nL += 1 + (1 if srng.random() < 0.03 else 0)
            c["no"] = "C%07d" % nL
        else:
            nP += 1 + (1 if srng.random() < 0.03 else 0)
            c["no"] = "FCL%07d" % nP
    salvage.sort(key=lambda s: (s["sold"], s["claim"]["no"]))
    lot = 7710400
    for s in salvage:
        lot += int(srng.integers(3, 40))
        s["lot"] = lot
        s["claim"]["supplier"] = K.SALVAGE
        s["claim"]["supplier_ref"] = "TVR%d" % lot
    return dict(leg_terms=leg_terms, plat_terms=plat_terms, crosswalk=crosswalk, mtas=mtas, claims=claims,
                thefts=thefts, glass=glass, salvage=salvage, legacy_no=legacy_no, platform_no=platform_no,
                first_plat=first_plat, inward=inward, term_ref=term_ref, quoted_ref=quoted_ref)
