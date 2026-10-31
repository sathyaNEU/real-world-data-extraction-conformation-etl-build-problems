"""The ask files and their truths: the two hospitals' dengue admissions, the September larval survey round,
and the city laboratory's dengue tests with its run log. None of these is read by the main call."""
import datetime as dt
import json

import numpy as np

from common import rng, mw_of, mw_start
from world import NAMES, IDX, DRUS

ASK_WEEKS_HOSP = list(range(33, 41))
ASK_WEEKS_LAB = list(range(35, 41))
EXTRACT_DT = dt.datetime(2027, 10, 11, 8, 0)
HOSP_FROM = dt.date(2027, 7, 25)          # the extracts start with week 30 (25 July 2027)


class UniqueIds:
    """Random identifiers drawn without replacement, so no two patients ever share one."""

    def __init__(self, r, lo, hi):
        self.r, self.lo, self.hi, self.used = r, lo, hi, set()

    def take(self):
        while True:
            v = int(self.r.integers(self.lo, self.hi))
            if v not in self.used:
                self.used.add(v)
                return v


def _admit_time(r, d):
    h = int(r.choice(range(24), p=_hour_weights()))
    return dt.datetime.combine(d, dt.time(h, int(r.integers(0, 60))))


_HW = None


def _hour_weights():
    global _HW
    if _HW is None:
        w = np.array([2, 1.5, 1.2, 1, 1, 1.2, 2, 3, 5, 6, 6.5, 6, 5.5, 5.5, 6, 6.5, 7, 7.5, 7, 6, 5, 4, 3, 2.5])
        _HW = w / w.sum()
    return _HW


# ---------------------------------------------------------------- hospital admissions
WARDS_CHILD = ["PEDIA WARD A", "PEDIA WARD B"]
WARDS_ADULT = {"F": "MEDICINE (FEMALE)", "M": "MEDICINE (MALE)"}


def hospital_stays(persons):
    """Every dengue stay at DMC and DDH from week 30 to the extract, residents and non-residents alike."""
    r = rng("hospital")
    stays = []
    for p in persons:
        if not p.get("dengue", True) or p["dru"] not in (0, 1) or not p["admitted"]:
            continue
        adm_day = p["consult"]
        if adm_day < HOSP_FROM:
            continue
        adm = _admit_time(r, adm_day)
        if adm >= EXTRACT_DT:
            continue
        los = int(r.integers(2, 7)) + (2 if r.random() < 0.15 else 0)
        stays.append({"hosp": p["dru"], "pid": p.get("pid_key", id(p)), "age": p["age"], "sex": p["sex"],
                      "admit": adm, "los": los, "home": p.get("home"), "resident": p.get("resident", True),
                      "town": p.get("town", "Dalisay City"), "brgy": p.get("town_brgy")})
    stays.sort(key=lambda s: (s["admit"], s["hosp"], s["age"]))
    # readmissions: a patient discharged and admitted again within days, a new stay of its own
    extra = []
    for s in stays:
        if r.random() < 0.045:
            d_out = s["admit"] + dt.timedelta(days=s["los"])
            re_adm = d_out + dt.timedelta(days=int(r.integers(2, 9)), hours=int(r.integers(0, 12)))
            if re_adm < EXTRACT_DT:
                t = dict(s, admit=re_adm, los=int(r.integers(2, 5)), readmission=True)
                extra.append(t)
    stays += extra
    stays.sort(key=lambda s: (s["admit"], s["hosp"], s["age"]))
    # patients moved from DMC to DDH when DMC's dengue beds run short: a new admission at DDH, no shared key
    moved = []
    for s in stays:
        if s["hosp"] != 0:
            continue
        y, w = mw_of(s["admit"])
        p_move = 0.12 if (y == 2027 and 34 <= w <= 40) else 0.05
        if r.random() < p_move:
            t_tr = s["admit"] + dt.timedelta(hours=int(r.integers(10, 44)))
            if t_tr < EXTRACT_DT - dt.timedelta(hours=6):
                s["transferred_out"] = t_tr
                t_in = t_tr + dt.timedelta(minutes=int(r.integers(70, 330)))
                moved.append(dict(s, hosp=1, admit=t_in, los=int(r.integers(2, 6)), transfer_in=True,
                                  transferred_out=None))
    stays += moved
    stays.sort(key=lambda s: (s["admit"], s["hosp"], s["age"]))
    return stays


def dmc_census(stays):
    """DMC's inpatient census extract: one row per ward-stay segment."""
    r = rng("dmc")
    rows = []
    numbers = {}
    ids = UniqueIds(r, 1100000, 1999999)
    truth = {w: 0 for w in ASK_WEEKS_HOSP}
    for s in stays:
        if s["hosp"] != 0:
            continue
        key = s["pid"]
        if key not in numbers:
            numbers[key] = "%07d" % ids.take()
        hn = numbers[key]
        y, w = mw_of(s["admit"])
        if y == 2027 and w in truth:
            truth[w] += 1
        ward0 = WARDS_CHILD[int(r.integers(0, 2))] if s["age"] < 15 else WARDS_ADULT[s["sex"]]
        t0 = s["admit"]
        end = s["admit"] + dt.timedelta(days=s["los"], hours=int(r.integers(-6, 7)))
        last_disp = "Discharged" if r.random() > 0.02 else "Discharged against advice"
        if s.get("transferred_out"):
            end = s["transferred_out"]
            last_disp = "Transferred to other hospital"
        cuts = [t0]
        wards = [ward0]
        if r.random() < 0.27:
            t1 = t0 + dt.timedelta(days=int(r.integers(1, 3)), hours=int(r.integers(0, 20)))
            if t1 < end:
                unit = "DENGUE UNIT" if r.random() < 0.75 else "ICU"
                cuts.append(t1)
                wards.append(unit)
                if unit == "ICU" and r.random() < 0.6:
                    t2 = t1 + dt.timedelta(days=int(r.integers(1, 3)), hours=int(r.integers(0, 12)))
                    if t2 < end:
                        cuts.append(t2)
                        wards.append(ward0)
        cuts.append(end)
        brgy = (NAMES[s["home"]] if s["resident"] else s["brgy"]).upper()
        town = "DALISAY CITY" if s["resident"] else s["town"].upper()
        for k, ward in enumerate(wards):
            a, b = cuts[k], cuts[k + 1]
            if a >= EXTRACT_DT:
                continue
            still = b >= EXTRACT_DT
            disp = last_disp if (k == len(wards) - 1 and not still) else ""
            rows.append([hn, s["age"], s["sex"], brgy, town, ward, a.strftime("%d/%m/%Y %H:%M"),
                         "" if still else b.strftime("%d/%m/%Y %H:%M"), disp,
                         "A97.%d" % (2 if ward == "ICU" else (1 if ward == "DENGUE UNIT" else int(r.random() < 0.35)))])
    rows.sort(key=lambda x: (dt.datetime.strptime(x[6], "%d/%m/%Y %H:%M"), x[0]))
    header = ["hospital_no", "age", "sex", "barangay", "city_municipality", "ward", "ward_in", "ward_out",
              "disposition", "dx_icd10"]
    return header, rows, truth


def ddh_sheets(stays):
    """DDH's dengue admissions log: one sheet per morbidity week of entry, the clerk closing each week's
    sheet at 17:00 on Saturday."""
    r = rng("olp")
    sheets = {}
    truth = {w: 0 for w in ASK_WEEKS_HOSP}
    pno = {}
    ids = UniqueIds(r, 10000, 99999)
    for s in stays:
        if s["hosp"] != 1:
            continue
        lag = dt.timedelta(minutes=int(r.integers(20, 240)))
        if r.random() < 0.08:
            lag = dt.timedelta(days=int(r.integers(1, 4)), hours=int(r.integers(0, 8)))
        entered = s["admit"] + lag
        # the sheet for the week the entry was made in; entries after Saturday 17:00 open next week's
        ey, ew = mw_of(entered)
        week_end = dt.datetime.combine(mw_start(ey, ew) + dt.timedelta(days=6), dt.time(17, 0))
        if entered >= week_end:
            ey, ew = mw_of(entered + dt.timedelta(days=1))
        if entered >= EXTRACT_DT:
            continue
        y, w = mw_of(s["admit"])
        if y == 2027 and w in truth and not s.get("transfer_in"):
            truth[w] += 1
        key = s["pid"]
        if key not in pno:
            pno[key] = "%d-%05d" % (27, ids.take())
        addr = ("%s, Dalisay City" % NAMES[s["home"]]) if s["resident"] else ("%s, %s" % (s["brgy"], s["town"]))
        dx = r.choice(["Dengue fever", "Dengue without warning signs", "Dengue with warning signs",
                       "Dengue with warning signs", "Severe dengue"], p=[0.25, 0.25, 0.22, 0.22, 0.06])
        a = s["admit"]
        hour12 = a.strftime("%I:%M %p").lstrip("0")
        sheets.setdefault((ey, ew), []).append([pno[key], s["age"], s["sex"], addr, a.strftime("%m/%d/%Y"),
                                                hour12, "%s-%d" % (r.choice(["2F", "3F", "4F"]), r.integers(1, 30)),
                                                dx])
    header = ["Patient No.", "Age", "Sex", "Address", "Date Admitted", "Time Admitted", "Room", "Diagnosis"]
    return header, sheets, truth


# ---------------------------------------------------------------- larval survey, September 2027 round
TEAM_A = ["San Isidro", "Santa Cruz", "Rizal", "Mabini", "Lumbia", "Tagumpay"]
TEAM_B = ["Dila", "Parian", "Liwayway", "Bayanihan", "Mangga", "Talon"]
CONTAINERS = ["Drum", "Pail", "Plastic container", "Tire", "Flower vase", "Plant pot saucer", "Roof gutter",
              "Coconut shell", "Dish rack", "Water jar", "Discarded can", "Refrigerator tray"]


def larval_survey():
    r = rng("larval")
    rows = []
    truth = {}
    for name in TEAM_A + TEAM_B:
        team = "VCU" if name in TEAM_A else "BHW"
        n_house = int(r.integers(170, 330))
        hi = r.uniform(0.07, 0.24)
        pos_houses = 0
        days = sorted(r.integers(1, 31, size=n_house))
        per_purok = {}
        for h in range(n_house):
            pk = int(r.integers(1, 9))
            purok = "Purok %d" % pk
            if team == "VCU":
                code = "%s-%05d" % ("".join(w[0] for w in name.replace("-", " ").split()).upper()[:3],
                                    10000 + h * 13 + int(r.integers(0, 13)))
            else:
                # the barangay health workers number the houses of each purok from 1
                per_purok[pk] = per_purok.get(pk, 0) + 1 + (1 if r.random() < 0.15 else 0)
                code = "%03d" % per_purok[pk]
            d = dt.date(2027, 9, int(days[h]))
            positive = r.random() < hi
            pos_houses += positive
            if team == "VCU":
                k = int(r.integers(0, 9))
                if k == 0:
                    rows.append([d.strftime("%d/%m/%Y"), team, name, purok, code, "No container", "", "", "", "", ""])
                    if positive:
                        pos_houses -= 1
                    continue
                npos = 0 if not positive else int(r.integers(1, min(3, k) + 1))
                flags = [1] * npos + [0] * (k - npos)
                r.shuffle(flags)
                for f in flags:
                    ctype = CONTAINERS[int(r.integers(0, len(CONTAINERS)))]
                    loc = "Outdoor" if r.random() < 0.6 else "Indoor"
                    pupae = "Y" if (f and r.random() < 0.35) else "N"
                    rows.append([d.strftime("%d/%m/%Y"), team, name, purok, code, ctype, loc, "Y" if f else "N",
                                 pupae, "", ""])
            else:
                k = int(r.integers(1, 10))
                npos = 0 if not positive else int(r.integers(1, min(3, k) + 1))
                rows.append([d.strftime("%d/%m/%Y"), team, name, purok, code, "", "", "", "", k, npos])
                if positive:
                    d2 = d + dt.timedelta(days=int(r.integers(5, 10)))
                    if d2.month == 9:
                        still = int(r.random() < 0.05)
                        rows.append([d2.strftime("%d/%m/%Y"), team, name, purok, code, "", "", "", "",
                                     max(1, k - npos + still), still])
        truth[name] = round(100.0 * pos_houses / n_house, 1)
    rows.sort(key=lambda x: (dt.datetime.strptime(x[0], "%d/%m/%Y"), x[2], x[4]))
    header = ["survey_date", "team", "barangay", "purok", "household_code", "container_type", "location",
              "larvae", "pupae", "containers_inspected", "containers_positive"]
    return header, rows, truth


# ---------------------------------------------------------------- the city laboratory
def laboratory(persons):
    """Specimens from the city health centres and clinics, tested at the City Health Office laboratory:
    NS1 antigen ELISA within five days of onset, IgM ELISA after that."""
    r = rng("lab")
    pts = []
    for p in persons:
        if p["dru"] < 2 or p["consult"] < dt.date(2027, 7, 18):
            continue
        if r.random() < 0.58:
            pts.append(p)
    # febrile patients tested and found negative, not dengue
    neg = []
    for p in pts:
        if r.random() < 0.42:
            q = dict(p)
            q["dengue"] = False
            q["consult"] = p["consult"] + dt.timedelta(days=int(r.integers(-3, 4)))
            neg.append(q)
    pts = pts + neg
    specs = []
    sid = 0
    refs = {}
    ids = UniqueIds(r, 10000, 99999)
    FIRST = "ABCDEFGJKLMNPRSTV"
    LAST = "ABCDEFGHIJLMNOPRSTV"
    for p in pts:
        who = {"initials": "%s.%s.%s." % (r.choice(list(FIRST)), r.choice(list(LAST)), r.choice(list(LAST))),
               "dob": p["onset"] - dt.timedelta(days=int(p["age"] * 365.25 + r.integers(0, 365))),
               "sex": p["sex"], "key": len(refs)}
        day = (p["consult"] - p["onset"]).days
        fac0 = DRUS[p["dru"]][0]
        dengue = p.get("dengue", True)

        def ref_for(fac):
            k = (who["key"], fac)
            if k not in refs:
                refs[k] = "L27-%05d" % ids.take()
            return refs[k]

        def add(coll_date, test, prob_pos, fac):
            nonlocal sid
            sid += 1
            res = "Positive" if (dengue and r.random() < prob_pos) else "Negative"
            if not dengue and r.random() < 0.015:
                res = "Positive"
            if test == "IgM" and res == "Negative" and r.random() < 0.05:
                res = "Equivocal"
            specs.append({"sid": sid, "pref": ref_for(fac), "fac": fac, "coll": coll_date, "test": test,
                          "true": res, "pdeng": dengue, "who": who})
            return res

        def follow_fac():
            if r.random() < 0.30:
                others = [d[0] for d in DRUS[2:] if d[0] != fac0]
                return others[int(r.integers(0, len(others)))]
            return fac0
        if day <= 5:
            res1 = add(p["consult"], "NS1", 0.86 if day <= 3 else 0.70, fac0)
            second = (res1 != "Positive" and r.random() < 0.55) or (res1 == "Positive" and r.random() < 0.30)
            if second:
                add(p["consult"] + dt.timedelta(days=int(r.integers(7, 13))), "IgM", 0.88, follow_fac())
        else:
            res1 = add(p["consult"], "IgM", 0.76, fac0)
            if res1 != "Positive" and r.random() < 0.6:
                add(p["consult"] + dt.timedelta(days=int(r.integers(7, 13))), "IgM", 0.90, follow_fac())
    specs = [s for s in specs if s["coll"] <= dt.date(2027, 10, 9)]
    LAST_RUN = dt.date(2027, 10, 8)        # the export left at 07:55 on Monday 11 October, before that day's plates
    specs.sort(key=lambda s: (s["coll"], s["sid"]))
    # runs: NS1 plates each working day, IgM plates on Tuesdays and Fridays
    runs = {}
    for s in specs:
        d = s["coll"] + dt.timedelta(days=1)
        while d.weekday() >= 5 or (s["test"] == "IgM" and d.weekday() not in (1, 4)):
            d += dt.timedelta(days=1)
        s["run_date"] = d
        if d > LAST_RUN:
            continue
        runs.setdefault((s["test"], d), []).append(s)
    specs = [s for s in specs if s["run_date"] <= LAST_RUN]
    rejected = set()
    rr = rng("labqc")
    ns1_days = sorted(d for (t, d) in runs if t == "NS1" and dt.date(2027, 8, 30) <= d <= dt.date(2027, 10, 8))
    # a kit lot with a high negative control, in use from week 35 to week 40
    lot = [d for d in ns1_days if dt.date(2027, 8, 30) <= d <= dt.date(2027, 10, 7)]
    for d in [lot[i] for i in sorted(rr.choice(len(lot), size=4, replace=False))]:
        rejected.add(("NS1", d))
    log = []
    rows = []
    for (test, d) in sorted(runs, key=lambda x: (x[1], x[0])):
        group = runs[(test, d)]
        rid = "%s-%s" % ("N" if test == "NS1" else "M", d.strftime("%y%m%d"))
        ok = (test, d) not in rejected
        entry = {"run_id": rid, "assay": "Dengue NS1 Ag ELISA" if test == "NS1" else "Dengue IgM capture ELISA",
                 "run_date": d.isoformat(), "specimens": len(group), "qc": "Accepted" if ok else "Rejected"}
        if not ok:
            entry["qc_note"] = rr.choice(["Negative control above cut-off", "Calibrator out of range"])
            d2 = d + dt.timedelta(days=1)
            while d2.weekday() >= 5:
                d2 += dt.timedelta(days=1)
            entry["repeated_in"] = "N-%s-R" % d2.strftime("%y%m%d")
            log.append(entry)
            rep = {"run_id": entry["repeated_in"], "assay": entry["assay"], "run_date": d2.isoformat(),
                   "specimens": len(group), "qc": "Accepted", "repeat_of": rid}
            log.append(rep)
            for s in group:
                shown = s["true"]
                if shown == "Negative" and rr.random() < 0.36:
                    shown = "Positive"
                rows.append(_lab_row(s, rid, shown, d))
                rows.append(_lab_row(s, rep["run_id"], s["true"], d2))
        else:
            log.append(entry)
            for s in group:
                rows.append(_lab_row(s, rid, s["true"], d))
    # specimen numbers as the reception desk issues them, in collection order with skipped numbers
    rs = rng("specimen_ids")
    order = sorted(specs, key=lambda s: (s["coll"], s["sid"]))
    nxt = 2704310
    sp_no = {}
    for s in order:
        nxt += 1 + (int(rs.integers(1, 6)) if rs.random() < 0.3 else 0)
        sp_no[s["sid"]] = "SP%07d" % nxt
    for row in rows:
        row[0] = sp_no[row[0]]
    rows.sort(key=lambda x: (x[8], x[0], x[7]))
    # truth: each patient's first positive on an accepted run, by test and collection week
    truth = {("NS1", w): 0 for w in ASK_WEEKS_LAB}
    truth.update({("IgM", w): 0 for w in ASK_WEEKS_LAB})
    first = {}
    for s in sorted(specs, key=lambda s: (s["coll"], s["sid"])):
        if s["true"] == "Positive" and s["who"]["key"] not in first:
            first[s["who"]["key"]] = s
    for s in first.values():
        y, w = mw_of(s["coll"])
        if y == 2027 and w in ASK_WEEKS_LAB:
            truth[(s["test"], w)] += 1
    header = ["specimen_id", "patient_ref", "patient_initials", "date_of_birth", "sex", "requesting_facility",
              "collected_on", "test", "result", "resulted_on", "run_id"]
    rows = [[x[0], x[1], x[9], x[10], x[11], x[2], x[3], x[4], x[5], x[6], x[7]] for x in rows]
    return header, rows, log, truth


def _lab_row(s, rid, shown, d):
    resulted = d + dt.timedelta(days=0 if rid.startswith("N") else 1)
    w = s["who"]
    return [s["sid"], s["pref"], s["fac"], s["coll"].strftime("%d/%m/%Y"),
            "NS1 Ag" if s["test"] == "NS1" else "IgM", shown, resulted.strftime("%d/%m/%Y"), rid, d.isoformat(),
            w["initials"], w["dob"].strftime("%d/%m/%Y"), w["sex"]]
