"""The golden, computed from target/ alone with the csv module: the split of the 1,200 packages and the bed-days
they free, the ladder's rungs, Ask A (each hospital's nights after the discharge ready date by month) and Ask B
(each district's referrals with care started within seven days, by month), with every stop the ask sheet names."""
import csv
import datetime as dt
import os
from fractions import Fraction

import core

FUND = 1200
W0, W1 = dt.date(2025, 12, 1), dt.date(2026, 2, 28)
SITES = list(core.HOSPITALS)
NAMES = {s: h["name"] for s, h in core.HOSPITALS.items()}


def _rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def d(s):
    return dt.date.fromisoformat(s[:10])


def t(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def files():
    import pack
    return pack.FILES


def spells(target, dedup=True):
    F = files()
    rows = _rows(target, F["spells"])
    if not dedup:
        return rows
    last = {}
    for r in rows:
        k = (r["provider_code"], r["spell_number"])
        if k not in last or int(r["submission_id"]) > int(last[k]["submission_id"]):
            last[k] = r
    return list(last.values())


def marchshire_practices(target):
    return {r["practice_code"] for r in _rows(target, files()["practices"]) if "Marchshire" in r["icb"]}


def discharge_orders(target):
    """Delivered hospital-discharge orders: NHS number and required-by date to the delivery date."""
    out = {}
    for r in _rows(target, files()["ices"]):
        if r["route"] != "Hospital discharge" or not r["delivered_date"]:
            continue
        k = (r["nhs_number"].replace(" ", ""), d(r["required_by"]))
        out.setdefault(k, set()).add(d(r["delivered_date"]))
    return out


def covered(target):
    mp = marchshire_practices(target)
    out = []
    for r in spells(target):
        if (r["discharge_pathway"] == "1" and r["p1_care_package"] == "New package" and r["gp_practice_code"] in mp
                and W0 <= d(r["discharge_ready_date"]) <= W1 and r["site_code"] in SITES):
            out.append(r)
    return out


def allocate(values, caps, fund=FUND):
    order = sorted(SITES, key=lambda s: -values[s])
    left, out = fund, {}
    for s in order:
        out[s] = min(left, caps[s])
        left -= out[s]
    return order, out


def main_call(target):
    cov = covered(target)
    eq = discharge_orders(target)
    caps = {s: 0 for s in SITES}
    save, delay, oc, ne_sum, ne_n = ({s: 0 for s in SITES} for _ in range(5))
    p1all = {s: [0, 0] for s in SITES}
    for r in spells(target):
        if r["discharge_pathway"] == "1" and W0 <= d(r["discharge_ready_date"]) <= W1:
            p1all[r["site_code"]][0] += 1
            p1all[r["site_code"]][1] += (d(r["discharge_datetime"]) - d(r["discharge_ready_date"])).days
    for r in cov:
        s, R, D = r["site_code"], d(r["discharge_ready_date"]), d(r["discharge_datetime"])
        E = eq.get((r["nhs_number"], R))
        assert E is None or len(E) == 1, r["spell_number"]
        E = min(E) if E else None
        caps[s] += 1
        save[s] += max(0, (D - max(R, E or R)).days)
        delay[s] += (D - R).days
        oc[s] += 0 if E else (D - R).days
        if not E:
            ne_sum[s] += (D - R).days
            ne_n[s] += 1
    val = {s: Fraction(save[s], caps[s]) for s in SITES}
    order, packages = allocate(val, caps)
    bed = {s: packages[s] * val[s] for s in SITES}
    rungs = {
        "R0": {s: Fraction(p1all[s][1], p1all[s][0]) for s in SITES},
        "R1": {s: Fraction(delay[s], caps[s]) for s in SITES},
        "OC": {s: Fraction(oc[s], caps[s]) for s in SITES},
        "NE": {s: Fraction(ne_sum[s], ne_n[s]) for s in SITES},
        "G": val,
    }
    alloc = {k: allocate(v, caps)[1] for k, v in rungs.items()}
    rung_bed = {k: {s: alloc[k][s] * rungs[k][s] for s in SITES} for k in rungs}
    return dict(caps=caps, save=save, val=val, order=order, packages=packages, bed=bed,
                total=sum(bed.values()), none=[s for s in SITES if packages[s] == 0], rungs=rungs, alloc=alloc,
                rung_bed=rung_bed, n_covered=len(cov))


# ---------------------------------------------------------------------------------------------- Ask A

def ward_sites(target):
    return {r["ward_code"]: r["site_code"] for r in _rows(target, files()["wardref"])}


def tw(s):
    """Ward stay times: ISO from one trust's system, day/month/year from the other's."""
    return dt.datetime.strptime(s, "%d/%m/%Y %H:%M") if "/" in s else t(s)


def ward_stays(target, parse=tw):
    out = {}
    for r in _rows(target, files()["wards"]):
        out.setdefault((r["provider_code"], r["spell_number"]), []).append((parse(r["ward_start"]),
                                                                            parse(r["ward_end"]), r["ward_code"]))
    for v in out.values():
        v.sort()
    return out


def month_key(n):
    return (n.year, n.month)


def monthfirst(s):
    """A parser that reads an ambiguous day/month/year as month first."""
    if "/" not in s:
        return t(s)
    first, second, rest = s.split("/", 2)
    y, hm = rest.split(" ")
    mo, dy = (int(first), int(second)) if int(first) <= 12 else (int(second), int(first))
    h, mi = (int(x) for x in hm.split(":"))
    return dt.datetime(int(y), mo, dy, h, mi)


def ask_a(target, site_from="wards", month_by="night", window="nights", dedup=True, keep="last", parse=tw,
          patients=False):
    """Nights after the discharge ready date, by the site the patient was on at the night's midnight and the month
    of the evening the night begins; with patients=True, the patients with at least one such night."""
    ws = ward_stays(target, parse=parse) if site_from == "wards" else {}
    site_of = ward_sites(target)
    out = {(s, m): 0 for s in SITES for m in core.ASK_MONTHS}
    who = {k: set() for k in out}
    rows = spells(target, dedup=False)
    if dedup:
        best = {}
        for r in rows:
            k = (r["provider_code"], r["spell_number"])
            if (k not in best or (int(r["submission_id"]) > int(best[k]["submission_id"])) == (keep == "last")):
                best[k] = r
        rows = list(best.values())
    for r in rows:
        R, D = d(r["discharge_ready_date"]), d(r["discharge_datetime"])
        if window == "ready" and not (W0 <= R <= W1):
            continue
        stays = ws.get((r["provider_code"], r["spell_number"]), [])
        n = R
        while n < D:
            mid = dt.datetime(n.year, n.month, n.day) + dt.timedelta(1)
            if site_from == "wards":
                before = [w for a, b, w in stays if a < mid]
                site = site_of[before[-1]] if before else r["site_code"]
            else:
                site = r["site_code"]
            m = month_key(n) if month_by == "night" else (month_key(D) if month_by == "discharge" else month_key(R))
            if (site, m) in out:
                out[(site, m)] += 1
                who[(site, m)].add(r["nhs_number"])
            n += dt.timedelta(1)
    if patients:
        return {k: len(v) for k, v in who.items()}
    return out


# ---------------------------------------------------------------------------------------------- Ask B

def norm_pc(pc):
    p = pc.strip().upper().replace(" ", "")
    return p[:-3] + " " + p[-3:]


def ask_b(target, spot=True, parse="dayfirst", prefix_map=False, normalise=True, first=True):
    """Referrals the brokerage received in each month of last winter, by the district of the care address, whose
    care started no more than seven days after the day of referral."""
    F = files()
    lookup = {r["postcode"]: r["district"] for r in _rows(target, F["postcodes"])}
    starts = {}
    if spot:
        for r in _rows(target, F["spot"]):
            dd, mm, yy = (int(x) for x in r["service_start"].split("/"))
            if parse == "dayfirst":
                sd = dt.date(yy, mm, dd)
            else:                      # a parser that reads ambiguous dates month first
                sd = dt.date(yy, dd, mm) if dd <= 12 else dt.date(yy, mm, dd)
            k = "BR%06d" % int(r["brokerage_ref"][3:])
            starts[k] = (min if first else max)(starts.get(k, sd), sd)
    out = {(dist, m): 0 for dist in core.DISTRICTS for m in core.ASK_MONTHS}
    received = {(dist, m): 0 for dist in core.DISTRICTS for m in core.ASK_MONTHS}
    for r in _rows(target, F["brokerage"]):
        rd = d(r["received_at"])
        m = month_key(rd)
        if m not in core.MONTH_LABEL:
            continue
        pc = norm_pc(r["care_postcode"]) if normalise else r["care_postcode"]
        if prefix_map:
            dist = "Severnside" if pc.startswith("SV") else lookup.get(pc)
        else:
            dist = lookup.get(pc)
        if dist not in core.DISTRICTS:
            continue
        received[(dist, m)] += 1
        sd = d(r["start_date"]) if r["start_date"] else starts.get(r["referral_no"])
        if sd is not None and (sd - rd).days <= 7:
            out[(dist, m)] += 1
    return out, received


def extras(target):
    """Counts the write-up's steps cite: covered patients with equipment delivered for their discharge, those who
    left on the delivery day at each hospital, and last winter's closed referrals whose care was bought by spot
    purchase."""
    eq = discharge_orders(target)
    with_eq, on_day = 0, {s: 0 for s in SITES}
    for r in covered(target):
        E = eq.get((r["nhs_number"], d(r["discharge_ready_date"])))
        if E:
            with_eq += 1
            on_day[r["site_code"]] += min(E) == d(r["discharge_datetime"])
    refs = {"BR%06d" % int(r["brokerage_ref"][3:]) for r in _rows(target, files()["spot"])}
    spot = sum(1 for r in _rows(target, files()["brokerage"])
               if r["referral_no"] in refs and month_key(d(r["received_at"])) in core.MONTH_LABEL)
    return dict(with_equipment=with_eq, left_on_delivery=on_day, spot_winter=spot)


def main(target):
    M = main_call(target)
    A = ask_a(target)
    AP = ask_a(target, patients=True)
    B, Brec = ask_b(target)
    return dict(M=M, A=A, AP=AP, A_total=sum(A.values()), B=B, B_received=Brec, X=extras(target))
