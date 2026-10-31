"""The city surveillance unit's dengue line list export, 2022 week 1 to the extract of 11 October 2027.

One row per notification or update, as the online notification system exports it: a case notified by a
second reporting unit arrives under a new case number, a classification or outcome change arrives as an
Update row under the same case number, a suspect later ruled out ends on 'Not a case', and residents of
other towns treated in the city's facilities stay on the list until the unit forwards them.
"""
import datetime as dt

import numpy as np

from common import rng, fmt_dmy, fmt_iso, EXPORT_DATE
from world import NAMES, N, IDX, DRUS, SPLIT_FROM, SPLIT_NEW, SPLIT_DATE, BARANGAYS, draw_age, mw_start

EXTRACT_DAY = (EXPORT_DATE - dt.timedelta(hours=8)).date() - dt.timedelta(days=1)   # 10 Oct 2027
CUTOVER = dt.date(2025, 1, 6)        # the online system replaced the encoded weekly sheets

OTHER_TOWNS = [("Pinagbuklod", ["Pulo", "Bagong Silang", "Banaba", "San Isidro"]),
               ("Kalinaw", ["Balibago", "Dita", "Ibaba", "Pooc"]),
               ("Sinagtala", ["Real", "Parian", "Halang", "Palingon"]),
               ("Masilaw", ["San Antonio", "Malaban", "Canlalay", "Santo Tomas"])]
TRAVEL_PLACES = ["Manila", "Quezon City", "Batangas City", "Lucena", "Tagaytay", "Cebu City", "Antipolo",
                 "San Pablo", "Iloilo City", "Bacolod"]
SURNAME_INITIALS = "ABCDEFGHIJLMNOPRSTV"
FIRST_INITIALS = "ABCDEFGJKLMNPRSTV"


def spelled(r, name, dru_kind, dru, on):
    """The barangay as each reporting unit writes it."""
    s = name
    if name.startswith("Santo "):
        s = r.choice([name, name.replace("Santo ", "Sto. "), name.replace("Santo ", "Sto ")])
    if name == "Santo Nino":
        s = r.choice(["Santo Nino", "Sto. Nino", "Sto. Niño", "Santo Niño"])
    if name == "Poblacion":
        s = r.choice(["Poblacion", "Pob.", "Poblacion (City Proper)"])
    if "-" in name and r.random() < 0.4:
        s = s.replace("-", " ")
    if name == "Pulong Bayabas" and r.random() < 0.15:
        s = "Pulong-Bayabas"
    if dru == 0:
        s = ("BRGY. " + s).upper() if r.random() < 0.7 else s.upper()
    elif dru_kind == "clinic" and r.random() < 0.5:
        s = "Brgy. " + s
    elif dru_kind == "rhu" and r.random() < 0.08:
        s = s.lower()
    if r.random() < 0.01:
        s = s + " "
    return s


def purok_for(r, home, on):
    if home == SPLIT_NEW:
        p = int(r.integers(5, 9))
    elif home == SPLIT_FROM:
        p = int(r.integers(1, 5))
    else:
        p = int(r.integers(1, 9))
    form = r.random()
    if form < 0.55:
        return "Purok %d" % p
    if form < 0.80:
        return "Purok %d, %s St." % (p, r.choice(["Mabini", "Rizal", "Luna", "Burgos", "Del Pilar", "Quezon",
                                                    "Sampaguita", "Ilang-Ilang", "Acacia", "Narra"]))
    if form < 0.95:
        return "Blk %d Lot %d, Phase %d" % (r.integers(1, 40), r.integers(1, 30), r.integers(1, 4))
    return "Sitio %s" % r.choice(["Ilaya", "Ibaba", "Centro", "Looban", "Bukid"])


def written_home(r, home, on, dru_kind, dru):
    name = NAMES[home]
    if home == SPLIT_NEW and (on < SPLIT_DATE or r.random() < 0.18):
        name = NAMES[SPLIT_FROM]            # the old barangay's name for the new barangay's puroks
    return spelled(r, name, dru_kind, dru, on)


def fmt_date(d, dru, on):
    if d is None:
        return ""
    if on >= CUTOVER and dru in (0, 1):
        return fmt_iso(d)
    return fmt_dmy(d)


def case_no(year, seq):
    return "DAL-%02d-%05d" % (year % 100, seq)


def dru_ref(r, dru, d):
    if dru == 0:
        return "DMC-%s-%04d" % (d.strftime("%y%m"), r.integers(1, 9999))
    if dru == 1:
        return "DDH%06d" % r.integers(100000, 999999)
    if DRUS[dru][1] == "rhu":
        roman = DRUS[dru][0].split()[-1]
        return "CHC%s-%s-%04d" % (roman, d.strftime("%y"), r.integers(1, 3999))
    return "%s-%05d" % (["DFC", "DEMC", "DDWC"][dru - 8], r.integers(1, 99999))


def initials(r):
    return "%s.%s.%s." % (r.choice(list(FIRST_INITIALS)), r.choice(list(SURNAME_INITIALS)),
                          r.choice(list(SURNAME_INITIALS)))


def build_rows(people):
    """Return (header, rows, truth) where truth maps each case's first case number to its person."""
    r = rng("linelist")
    events = []        # (report_date, order key, payload)
    persons = []
    # the city's cases
    for p in people:
        q = dict(p)
        q["resident"] = True
        q["dengue"] = True
        persons.append(q)
    # suspects later ruled out, residents and others
    ro = rng("suspects")
    for p in people:
        if ro.random() < 0.045:
            q = dict(p)
            q["resident"] = True
            q["dengue"] = False
            q["home"] = int(ro.integers(0, N))
            q["age"] = draw_age(ro, "child" if ro.random() < 0.4 else "other")
            persons.append(q)
    # residents of other towns treated in the city, kept until forwarded
    rn = rng("nonresidents")
    for p in people:
        if p["dru"] in (0, 1) and rn.random() < 0.22:
            q = dict(p)
            q["resident"] = False
            q["dengue"] = True
            town, brgys = OTHER_TOWNS[int(rn.integers(0, len(OTHER_TOWNS)))]
            q["town"] = town
            q["town_brgy"] = brgys[int(rn.integers(0, len(brgys)))]
            q["forwarded"] = q["reported"] + dt.timedelta(days=int(rn.integers(3, 15)))
            persons.append(q)

    for pid, q in enumerate(persons):
        dru = q["dru"]
        kind = DRUS[dru][1]
        on = q["onset"]
        if not q["resident"]:
            if q["forwarded"] <= EXTRACT_DAY:
                continue
        first = q["reported"]
        if first > EXTRACT_DAY:
            continue
        base = {
            "pid": pid, "dru": dru, "initials": initials(r), "sex": q["sex"], "age": q["age"],
            "dob": None if r.random() < (0.10 if on >= CUTOVER else 0.22) else
            on - dt.timedelta(days=int(q["age"] * 365.25 + r.integers(0, 365))),
            "onset": None if r.random() < 0.018 else on, "consult": q["consult"],
            "admitted": q["admitted"], "travel": q.get("travel", False),
        }
        if q["resident"]:
            base["brgy"] = written_home(r, q["home"], on, kind, dru)
            base["purok"] = purok_for(r, q["home"], on)
            base["town"] = "Dalisay City"
        else:
            base["brgy"] = q["town_brgy"] if r.random() < 0.6 else "Brgy. " + q["town_brgy"]
            base["purok"] = purok_for(r, 0, on)
            base["town"] = q["town"]
        base["date_adm"] = q["consult"] if (q["admitted"] and r.random() < 0.42) else None
        base["travel_place"] = TRAVEL_PLACES[int(r.integers(0, len(TRAVEL_PLACES)))] if base["travel"] else ""
        cls0 = "Suspect"
        events.append((first, pid, 0, dict(base, status="New", cls=cls0, lab="", labres="", outcome="",
                                           ref=dru_ref(r, dru, first), reported=first)))
        # an update after the laboratory result or the outcome
        if q["dengue"]:
            if r.random() < 0.45:
                ud = first + dt.timedelta(days=int(r.integers(2, 12)))
                if ud <= EXTRACT_DAY:
                    test = r.choice(["NS1", "NS1", "IgM", "PCR"])
                    pos = r.random() < 0.82
                    events.append((ud, pid, 1, dict(base, status="Update",
                                                    cls="Confirmed" if pos else "Probable",
                                                    lab=test, labres="Positive" if pos else "Negative",
                                                    outcome="Alive", reported=ud)))
            # a second unit's notification of the same patient (seen at a centre, then admitted)
            if kind != "hospital" and r.random() < 0.11:
                d2 = first + dt.timedelta(days=int(r.integers(1, 6)))
                if d2 <= EXTRACT_DAY:
                    dru2 = 0 if r.random() < 0.6 else 1
                    b2 = dict(base, dru=dru2, admitted=True,
                              brgy=written_home(r, q["home"], on, "hospital", dru2) if q["resident"] else base["brgy"],
                              consult=d2, date_adm=d2 if r.random() < 0.5 else None)
                    events.append((d2, pid, 2, dict(b2, status="New", cls="Suspect", lab="", labres="",
                                                    outcome="", ref=dru_ref(r, dru2, d2), reported=d2)))
        else:
            ud = first + dt.timedelta(days=int(r.integers(2, 9)))
            if ud <= EXTRACT_DAY:
                events.append((ud, pid, 1, dict(base, status="Update", cls="Not a case", lab="NS1",
                                                labres="Negative", outcome="", reported=ud)))

    events.sort(key=lambda e: (e[0], e[2], e[1]))
    # case numbers: one per New notification, in report order, a few numbers voided in the sequence
    seq = {}
    numbers = {}
    first_no = {}
    rows = []
    for (d, pid, kind_ev, e) in events:
        y = d.year
        if e["status"] == "New":
            s = seq.get(y, 0) + 1 + (int(r.integers(1, 4)) if r.random() < 0.03 else 0)
            seq[y] = s
            no = case_no(y, s)
            numbers[(pid, kind_ev)] = no
            first_no.setdefault(pid, no)
        else:
            no = numbers.get((pid, 0))
            if no is None:
                continue
        old = e["reported"] < CUTOVER
        cls = e["cls"]
        if old:
            cls = {"Suspect": "S", "Probable": "P", "Confirmed": "C", "Not a case": "X"}[cls]
        dru = e["dru"]
        rows.append([
            no, DRUS[dru][0], e.get("ref", ""), e["status"], fmt_date(e["reported"], dru, e["reported"]),
            e["initials"], e["sex"], fmt_date(e["dob"], dru, e["reported"]) if e["dob"] else "", e["age"],
            e["brgy"], e["purok"], e["town"], "Laguna",
            fmt_date(e["onset"], dru, e["reported"]) if e["onset"] else "",
            fmt_date(e["consult"], dru, e["reported"]),
            "Y" if e["admitted"] else "N",
            fmt_date(e["date_adm"], dru, e["reported"]) if e["date_adm"] else "",
            cls, e["lab"], e["labres"], e["outcome"],
            ("Y" if e["travel"] else ("N" if not old else "")), e["travel_place"] if not old else "",
        ])
    header = ["case_no", "reporting_unit", "unit_case_ref", "report_status", "date_reported",
              "patient_initials", "sex", "date_of_birth", "age_years", "barangay", "street_purok",
              "city_municipality", "province", "date_onset", "date_consult", "admitted", "date_admitted",
              "case_classification", "lab_test", "lab_result", "outcome", "travel_14d", "travel_place"]
    return header, rows, persons, first_no
