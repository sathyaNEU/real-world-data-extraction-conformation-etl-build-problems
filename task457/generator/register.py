"""Open Payments general payments for the faculty, program years 2021 to 2025, as the January 2027 refresh
publishes them, plus what the June 2026 publication showed for 2025.

Each remuneration relationship-year becomes the payment records a manufacturer reports (speaker programs, consulting
installments, advisory meetings), each with its date, nature and amount, summing to the year's remuneration. Around
them sit the records the policy's remuneration does not cover (meals, travel, education, royalties). Faculty carry one
covered-recipient profile (a few two); manufacturers leave the NPI off some records. Physicians elsewhere who share a
faculty member's name have their own profiles; the office's matcher attaches their records that carry no NPI, as it
attaches the faculty's own. A few faculty direct speaker fees to the university."""
import datetime as dt

import numpy as np

import world as W

D = dt.date
REMUN_KIND = {"consulting": [(0, 0.92), (2, 0.08)], "speaking": [(1, 0.70), (3, 0.18), (4, 0.12)],
              "advisory": [(0, 0.70), (2, 0.30)], "honoraria": [(2, 0.85), (1, 0.15)], "other": [(1, 1.0)],
              "expert": [(1, 1.0)]}
PAY_SIZE = {"consulting": 2600.0, "speaking": 2300.0, "advisory": 3200.0, "honoraria": 1800.0, "other": 2500.0,
            "expert": 3000.0}
OTHER_CITIES = [("Columbus", "OH", "43215"), ("Cleveland", "OH", "44106"), ("Pittsburgh", "PA", "15213"),
                ("Ann Arbor", "MI", "48109"), ("Indianapolis", "IN", "46202"), ("Louisville", "KY", "40202"),
                ("Chicago", "IL", "60611"), ("Baltimore", "MD", "21287"), ("Nashville", "TN", "37232"),
                ("Charlotte", "NC", "28204"), ("Milwaukee", "WI", "53226"), ("St. Louis", "MO", "63110"),
                ("Lexington", "KY", "40536"), ("Rochester", "NY", "14642"), ("Richmond", "VA", "23298")]
STREETS = ["Medical Center Drive", "University Boulevard", "Health Sciences Way", "Clinic Road", "Hospital Avenue",
           "Research Parkway", "Commons Way", "College Street"]


class Rec(dict):
    pass


def _days(r, year, k):
    start = D(year, 1, 1).toordinal()
    end = D(year, 12, 31).toordinal()
    return sorted(D.fromordinal(int(x)) for x in r.integers(start, end + 1, size=k))


def _split(r, total, k):
    """k positive amounts in cents summing to total."""
    w = r.gamma(6.0, 1.0, size=k)
    cents = np.floor(w / w.sum() * round(total * 100)).astype(int)
    cents[-1] += int(round(total * 100)) - int(cents.sum())
    if cents.min() <= 0:
        cents = np.full(k, int(round(total * 100)) // k)
        cents[-1] += int(round(total * 100)) - int(cents.sum())
    return [c / 100.0 for c in cents]


def _nature(r, kind):
    opts = REMUN_KIND[kind]
    i = r.choice(len(opts), p=[p for _, p in opts])
    return W.NATURES_REMUN[opts[i][0]]


def profiles(fac, r):
    """Each faculty member's covered-recipient profile ids (a few carry two). Some manufacturers registered a faculty
    member under a profile of their own without the NPI (the duplicate profile carries the faculty member's name and
    practice address); that manufacturer's records sit on it."""
    pid = 410000
    for f in fac:
        pid += int(r.integers(3, 900))
        f.profiles = [str(pid)]
        if f.group == "bg" and r.random() < 0.02:
            pid += int(r.integers(3, 900))
            f.profiles.append(str(pid))
    rd = np.random.default_rng([W.SEED, 16])
    want = {"consulting": 7, "speaking": 9, "honoraria": 5, "advisory": 3}
    pool = [f for f in fac if f.group == "bg" and f.cred in ("MD", "DO") and f.holds(D(2025, 12, 31))]
    order = [pool[int(k)] for k in rd.permutation(len(pool))]
    for f in order:
        rels = [rel for rel in f.rels if rel["mfr"] and 2025 in rel["years"] and want.get(rel["kind"], 0) > 0
                and not rel.get("now_reporting") and not rel.get("typed_former")]
        if not rels:
            continue
        rel = rels[int(rd.integers(len(rels)))]
        want[rel["kind"]] -= 1
        pid += int(rd.integers(3, 900))
        f.dup_profile, f.dup_mfr = str(pid), rel["mfr"]
        if not any(want.values()):
            break
    return pid


def address(f, year, r):
    """The business address a manufacturer reports for the faculty member in a year: the department's practice address
    while they hold the appointment, with the suite the manufacturer has on file."""
    here = f.holds(D(year, 6, 30)) or f.holds(D(year, 12, 31)) or f.holds(D(year, 1, 1))
    if here:
        street, zp = W.CAMPUS[f.dept]
        suite = W.SUITES[(int(f.npi[-3:]) + (year if r.random() < 0.1 else 0)) % len(W.SUITES)]
        return (street + (" " + suite if suite else "")), W.CITY, W.STATE, zp
    c = OTHER_CITIES[(int(f.emp_id) + year) % len(OTHER_CITIES)]
    return "%d %s" % (100 + int(f.emp_id) % 3900, STREETS[int(f.emp_id) % len(STREETS)]), c[0], c[1], c[2]


def namesake_profiles(namesakes, start):
    r = np.random.default_rng([W.SEED, 14])
    pid = start
    for ns in namesakes:
        pid += int(r.integers(3, 900))
        ns.profile = str(pid)


def records(fac, mfrs, namesakes):
    """Every general payment record of the faculty (and of the namesakes the matcher attaches), 2021 to 2025, as
    the refresh publishes it: a list of Rec."""
    r = np.random.default_rng([W.SEED, 11])
    byid = {m["id"]: m for m in mfrs}
    last = profiles(fac, r)
    namesake_profiles(namesakes, last)
    out = []
    for f in fac:
        rr = np.random.default_rng([W.SEED, 12, W.SPLIT_SALT, int(f.emp_id) if f.group == "bg" else 9000000 + 1000 * hash_group(f)])
        third = f.group == "bg" and f.rels and rr.random() < 0.05
        blank_rate = 0.0 if f.group != "bg" else (0.035 if rr.random() < 0.6 else 0.0)
        for rel in f.rels:
            if rel["mfr"] is None:
                continue
            m = byid[rel["mfr"]]
            nat = _nature(rr, rel["kind"])           # a relationship's payments carry one nature, now and then another
            for y, a in sorted(rel["years"].items()):
                if y > 2025:
                    continue
                dup = getattr(f, "dup_mfr", None) == rel["mfr"]
                for day, amt in rel["pay"][y]:
                    rec = Rec(f=f, year=y, mfr=m, amount=amt, date=day,
                              nature=nat if rr.random() < 0.85 else _nature(rr, rel["kind"]),
                              personal=True, npi_blank=dup or rr.random() < blank_rate, kind=rel["kind"], remun=True,
                              dup=dup)
                    out.append(rec)
                if third and rel["kind"] == "speaking" and rr.random() < 0.6:
                    # a speaker fee the faculty member directed to the university
                    amt = round(float(rr.uniform(1500, 4500)), 2)
                    out.append(Rec(f=f, year=y, mfr=m, amount=amt, date=_days(rr, y, 1)[0], nature=W.NATURES_REMUN[1],
                                   personal=False, npi_blank=False, kind="speaking", remun=True))
                if rel["kind"] in ("speaking", "consulting", "advisory") and rr.random() < 0.55:
                    for _ in range(int(rr.integers(1, 4))):
                        out.append(Rec(f=f, year=y, mfr=m, amount=round(float(rr.uniform(180, 1450)), 2),
                                       date=_days(rr, y, 1)[0], nature="Travel and Lodging", personal=True,
                                       npi_blank=rr.random() < blank_rate, kind=None, remun=False))
        if f.contact:
            lam = float(np.exp(rr.normal(np.log(8.0), 0.75)))
            older = [m for m in mfrs if not m.get("now_reporting")]
            for y in W.REGISTER_YEARS:
                n = int(rr.poisson(lam))
                pool = [byid[rel["mfr"]] for rel in f.rels if rel["mfr"] is not None and y >= 2025 or
                        (rel["mfr"] is not None and not byid[rel["mfr"]].get("now_reporting"))] or []
                for _ in range(n):
                    m = (pool[int(rr.integers(len(pool)))] if pool and rr.random() < 0.5 else
                         (mfrs if y >= 2025 else older)[int(rr.integers(len(mfrs) if y >= 2025 else len(older)))])
                    out.append(Rec(f=f, year=y, mfr=m, amount=round(float(np.exp(rr.normal(np.log(26.0), 0.55))), 2),
                                   date=_days(rr, y, 1)[0], nature="Food and Beverage", personal=True,
                                   npi_blank=rr.random() < blank_rate, kind=None, remun=False))
                if rr.random() < 0.08:
                    m = older[int(rr.integers(len(older)))]
                    out.append(Rec(f=f, year=y, mfr=m, amount=round(float(rr.uniform(40, 650)), 2),
                                   date=_days(rr, y, 1)[0], nature="Education", personal=True,
                                   npi_blank=False, kind=None, remun=False))
        launch = [byid[rel["mfr"]] for rel in f.rels if rel.get("now_reporting")]
        for m in sorted({m["id"]: m for m in launch}.values(), key=lambda m: m["id"]):
            # the 2025 launch meetings of a company that began reporting that year: meals, travel, no fees
            for _ in range(int(rr.integers(1, 4))):
                out.append(Rec(f=f, year=2025, mfr=m, amount=round(float(np.exp(rr.normal(np.log(48.0), 0.5))), 2),
                               date=_days(rr, 2025, 1)[0], nature="Food and Beverage", personal=True,
                               npi_blank=False, kind=None, remun=False))
            if rr.random() < 0.6:
                out.append(Rec(f=f, year=2025, mfr=m, amount=round(float(rr.uniform(420, 1350)), 2),
                               date=_days(rr, 2025, 1)[0], nature="Travel and Lodging", personal=True,
                               npi_blank=False, kind=None, remun=False))
        if f.group == "bg" and f.rels and rr.random() < 0.02:
            m = byid[[rel for rel in f.rels if rel["mfr"]][0]["mfr"]] if any(rel["mfr"] for rel in f.rels) else mfrs[0]
            if m.get("now_reporting"):
                m = mfrs[0]
            for y in W.REGISTER_YEARS[2:]:
                out.append(Rec(f=f, year=y, mfr=m, amount=round(float(rr.uniform(800, 9000)), 2),
                               date=_days(rr, y, 1)[0], nature="Royalty or License", personal=True,
                               npi_blank=False, kind=None, remun=False))
    older = [m for m in mfrs if not m.get("now_reporting")]
    for ns in namesakes:
        rr = np.random.default_rng([W.SEED, 13, int(ns.npi)])
        for y in W.REGISTER_YEARS:
            for _ in range(int(rr.poisson(ns.lam))):
                m = older[int(rr.integers(len(older)))]
                if rr.random() < 0.32:
                    nat = W.NATURES_REMUN[int(rr.choice(5, p=[0.3, 0.3, 0.15, 0.15, 0.1]))]
                    amt = round(float(np.exp(rr.normal(np.log(1800.0), 0.6))), 2)
                    remun = True
                else:
                    nat, amt, remun = "Food and Beverage", round(float(np.exp(rr.normal(np.log(24.0), 0.5))), 2), False
                out.append(Rec(f=ns, year=y, mfr=m, amount=amt, date=_days(rr, y, 1)[0], nature=nat, personal=True,
                               npi_blank=True, kind=None, remun=remun, namesake=True))
    # every remuneration nature carries at least three attached namesake records in 2025
    rr = np.random.default_rng([W.SEED, 15])
    for k, nat in enumerate(W.NATURES_REMUN):
        have = sum(1 for x in out if x.get("namesake") and x["year"] == 2025 and x["nature"] == nat)
        for j in range(max(0, 3 - have)):
            ns = namesakes[(7 * k + 3 * j) % len(namesakes)]
            out.append(Rec(f=ns, year=2025, mfr=older[int(rr.integers(len(older)))],
                           amount=round(float(np.exp(rr.normal(np.log(2100.0), 0.5))), 2), date=_days(rr, 2025, 1)[0],
                           nature=nat, personal=True, npi_blank=True, kind=None, remun=True, namesake=True))
    return out


def hash_group(f):
    import people as PE
    return [k for k, _ in PE.GROUPS].index(f.group) * 100 + 100 + f.q
