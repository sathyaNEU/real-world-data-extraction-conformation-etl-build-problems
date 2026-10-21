"""The system's own records about the people on the register, drawn from their own stream so the asks' records never
move the world: identifiers (enterprise IDs, hospital record numbers, duplicate registrations and their merges),
breast surgery (first course in the tumor registry, procedures in the current EHR), breast MRI, and deaths."""
import datetime as dt

import numpy as np

import common as K
import core as C
import world as W

CUTOVER_Y = W.yfrac(K.EHR_CUTOVER)
WIN0, WIN1 = W.yfrac(K.MRI_WINDOW[0]), W.yfrac(K.MRI_WINDOW[1]) + 1 / 365
EXPORT_Y = W.EXPORT_Y
HOSP_W = np.array([14, 9, 7, 9, 6, 4, 3, 10, 5, 5, 8, 3, 3, 2, 6, 3], float)
HOSP_W /= HOSP_W.sum()

# first-course surgery in the tumor registry (the registry's codes for the most definitive breast surgery)
SURG = {
    22: "Lumpectomy or excisional biopsy",
    41: "Total (simple) mastectomy, without removal of uninvolved contralateral breast",
    42: "Total (simple) mastectomy, with removal of uninvolved contralateral breast",
    51: "Modified radical mastectomy, without removal of uninvolved contralateral breast",
    56: "Modified radical mastectomy, with removal of uninvolved contralateral breast",
}
BOTH = {42, 56}


def ids(rng, n, prefix, width, taken):
    out = []
    while len(out) < n:
        x = "%s%0*d" % (prefix, width, int(rng.integers(10 ** (width - 1), 10 ** width)))
        if x not in taken:
            taken.add(x)
            out.append(x)
    return out


def build(w, seed=C.CLINICAL_SEED):
    rng = np.random.default_rng(seed)
    fams = w["families"]
    taken = set()
    # family and person keys: families numbered in an order unrelated to their group
    order = rng.permutation(len(fams))
    fid = {}
    for k, i in enumerate(order):
        fid[int(i)] = "ICRS-F%05d" % (10017 + 3 * k + int(rng.integers(0, 3)))
    people = []   # (family index, lid)
    for i, f in enumerate(fams):
        for p in f["persons"]:
            people.append((i, p["lid"]))
    perm = rng.permutation(len(people))
    pid = {}
    for k, j in enumerate(perm):
        pid[people[int(j)]] = "ICRS-P%06d" % (100003 + 2 * k + int(rng.integers(0, 2)))
    # patients: enterprise ID, hospital, record number, exact birth date
    pat = {}
    for i, f in enumerate(fams):
        home = int(rng.choice(len(K.HOSP_CODES), p=HOSP_W))
        for p in f["persons"]:
            if not p["patient"]:
                continue
            h = home if (p["role"] == "PROBAND" or rng.random() < 0.55) else int(rng.choice(len(K.HOSP_CODES), p=HOSP_W))
            pat[(i, p["lid"])] = dict(hosp=K.HOSP_CODES[h], dob=W.ydate(p["birth"]))
    eids = ids(rng, len(pat), "E", 9, taken)
    for (key, e) in zip(sorted(pat), eids):
        pat[key]["eid"] = e
    mrn_taken = set()
    for key in sorted(pat):
        rec = pat[key]
        rec["mrns"] = [(rec["hosp"], ids(rng, 1, "", 8, mrn_taken)[0])]
        if rng.random() < 0.14:
            other = K.HOSP_CODES[int(rng.choice(len(K.HOSP_CODES), p=HOSP_W))]
            if other != rec["hosp"]:
                rec["mrns"].append((other, ids(rng, 1, "", 8, mrn_taken)[0]))
    out = dict(fid=fid, pid=pid, pat=pat, abstracts=[], procedures=[], exams=[], deaths=[], merges=[],
               duplicates={})

    # deaths of patients up to the export (the linkage reaches state vital records)
    for i, f in enumerate(fams):
        for p in f["persons"]:
            key = (i, p["lid"])
            yd = p["birth"] + p["death"]
            if key in pat and 2016.0 <= yd <= EXPORT_Y:
                out["deaths"].append(dict(key=key, date=W.ydate(yd),
                                          source="State vital records" if rng.random() < 0.7 else "EHR"))
    dead = {d["key"]: d["date"] for d in out["deaths"]}

    # breast cancers diagnosed at the system from 2016: probands, and patient relatives diagnosed after intake
    for i, f in enumerate(fams):
        for p in f["persons"]:
            key = (i, p["lid"])
            if key not in pat or p["sex"] != "F" or not np.isfinite(p["breast"]):
                continue
            yo = p["birth"] + p["breast"]
            is_pb = p["role"] == "PROBAND"
            if not (is_pb or (f["intake"] < yo <= EXPORT_Y - 0.25)) or yo < 2016.0:
                continue
            ys = yo + rng.uniform(0.04, 0.2)
            u = rng.random()
            # relatives' first course before the cutover is kept to one breast (no device on the estimate's women)
            both_ok = is_pb or ys >= CUTOVER_Y
            if u < 0.50:
                code = 22
            elif u < 0.74 or not both_ok:
                code = 41 if rng.random() < 0.8 else 51
            else:
                code = 42 if rng.random() < 0.8 else 56
            lat = "Left" if rng.random() < 0.5 else "Right"
            out["abstracts"].append(dict(key=key, dx=W.ydate(yo), surg=code, surg_date=W.workday(W.ydate(ys)), lat=lat,
                                         hosp=pat[key]["hosp"], age=int(np.floor(p["breast"])),
                                         behavior="In situ" if rng.random() < 0.16 else "Invasive"))
            p_side = {"Left": "LT", "Right": "RT"}[lat]
            o_side = {"LT": "RT", "RT": "LT"}[p_side]
            if ys >= CUTOVER_Y:
                cpt = {22: "19301", 41: "19303", 42: "19303", 51: "19307", 56: "19307"}[code]
                if code in BOTH:
                    if rng.random() < 0.6:
                        out["procedures"].append(dict(key=key, date=W.workday(W.ydate(ys)), cpt=cpt, mod="50"))
                    else:
                        out["procedures"].append(dict(key=key, date=W.workday(W.ydate(ys)), cpt=cpt, mod=p_side))
                        out["procedures"].append(dict(key=key, date=W.workday(W.ydate(ys)), cpt="19303", mod=o_side))
                else:
                    out["procedures"].append(dict(key=key, date=W.workday(W.ydate(ys)), cpt=cpt, mod=p_side))
            # a later contralateral mastectomy (probands only)
            if is_pb and code not in BOTH and rng.random() < 0.16:
                yc = ys + rng.uniform(0.8, 6.0)
                if CUTOVER_Y <= yc <= EXPORT_Y and (key not in dead or W.yfrac(dead[key]) > yc):
                    out["procedures"].append(dict(key=key, date=W.workday(W.ydate(yc)), cpt="19303", mod=o_side))
            elif is_pb and code == 22 and rng.random() < 0.05:
                yc = ys + rng.uniform(0.5, 4.0)
                if CUTOVER_Y <= yc <= EXPORT_Y:
                    out["procedures"].append(dict(key=key, date=W.workday(W.ydate(yc)), cpt="19301", mod=p_side))
    # risk-reducing mastectomy of unaffected relatives who tested positive, after the family's history date
    for i, f in enumerate(fams):
        for p in f["persons"]:
            key = (i, p["lid"])
            if key not in pat or p["sex"] != "F" or p["role"] == "PROBAND" or not p["car"]:
                continue
            if not np.isfinite(p["test"]) or (np.isfinite(p["breast"]) and p["birth"] + p["breast"] <= EXPORT_Y):
                continue
            if rng.random() < 0.10:
                yr = max(p["test"] + rng.uniform(0.5, 4.0), f["history"] + 0.1, CUTOVER_Y + 0.1)
                if yr <= EXPORT_Y and (key not in dead or W.yfrac(dead[key]) > yr):
                    out["procedures"].append(dict(key=key, date=W.workday(W.ydate(yr)), cpt="19303", mod="50"))
    # unrelated breast procedures (excisional biopsies, reductions) for texture
    keys = sorted(pat)
    for _ in range(int(len(keys) * 0.03)):
        key = keys[int(rng.integers(0, len(keys)))]
        y = rng.uniform(CUTOVER_Y, EXPORT_Y)
        cpt = "19120" if rng.random() < 0.7 else "19318"
        out["procedures"].append(dict(key=key, date=W.workday(W.ydate(y)), cpt=cpt, mod="RT" if rng.random() < 0.5 else "LT"))
    return out


def ensure_contralateral(w, rec, positives, seed=C.CLINICAL_SEED):
    """Every group holds at least one known-carrier proband, alive, of clinic age and a patient, whose first course
    before the cutover took one breast (registry only) and whose other breast was removed later (surgical record
    only)."""
    rng = np.random.default_rng([seed, 5])
    dead = {d["key"] for d in rec["deaths"]}
    for code in K.CODES:
        cands, have = [], False
        for i, f in enumerate(w["families"]):
            if f["code"] != code:
                continue
            p = f["persons"][0] if f["persons"][0]["role"] == "PROBAND" else None
            key = (i, f["proband"])
            if p is None or key in dead or key not in positives or not p["alive_at_hist"]:
                continue
            if not 30 <= age_on(rec["pat"][key]["dob"], K.PROGRAM_START) <= 74:
                continue
            ab = [a for a in rec["abstracts"] if a["key"] == key]
            if not ab or ab[0]["surg"] not in (41, 51) or W.yfrac(ab[0]["surg_date"]) >= CUTOVER_Y:
                continue
            later = [q for q in rec["procedures"] if q["key"] == key and q["cpt"] == "19303"]
            if later:
                have = True
                break
            cands.append((key, ab[0]))
        if not have and cands:
            key, a = cands[int(rng.integers(0, len(cands)))]
            side = {"Left": "RT", "Right": "LT"}[a["lat"]]
            y = rng.uniform(max(CUTOVER_Y + 0.2, W.yfrac(a["surg_date"]) + 1.0), EXPORT_Y - 0.3)
            rec["procedures"].append(dict(key=key, date=W.workday(W.ydate(y)), cpt="19303", mod=side))
    return rec


def removed_both(rec, key):
    """Both breasts removed by the export, on all the system's records (first course and procedures)."""
    sides = set()
    for a in rec["abstracts"]:
        if a["key"] == key and a["surg"] in (41, 42, 51, 56):
            sides.add({"Left": "LT", "Right": "RT"}[a["lat"]])
            if a["surg"] in BOTH:
                sides |= {"LT", "RT"}
    for q in rec["procedures"]:
        if q["key"] == key and q["cpt"] in ("19303", "19305", "19306", "19307"):
            sides |= {"LT", "RT"} if q["mod"] == "50" else {q["mod"]}
    return sides >= {"LT", "RT"}


def age_on(dob, day):
    return day.year - dob.year - ((day.month, day.day) < (dob.month, dob.day))


def eligible(w, rec, labs_positive):
    """Ask A's women: a laboratory result showing the family's variant, an enterprise ID, no recorded death by the
    export, aged 30 to 74 on the program's first day, not both breasts removed. labs_positive: set of keys."""
    dead = {d["key"] for d in rec["deaths"]}
    out = {}
    for i, f in enumerate(w["families"]):
        for p in f["persons"]:
            key = (i, p["lid"])
            if key not in labs_positive or p["sex"] != "F" or key not in rec["pat"] or key in dead:
                continue
            if not p["alive_at_hist"]:
                continue
            a = age_on(rec["pat"][key]["dob"], K.PROGRAM_START)
            if not 30 <= a <= 74 or removed_both(rec, key):
                continue
            out[key] = f["code"]
    return out


def imaging(w, rec, elig, seed=C.CLINICAL_SEED):
    """Breast MRI at the system's hospitals, 2024 to the export: the women under the clinic's surveillance have an
    annual screening study, a few have a diagnostic one, and some orders are cancelled. Duplicate registrations: a
    probands' second record at another hospital carries a second enterprise ID until the two are merged; studies
    done there before the merge carry the retired ID."""
    rng = np.random.default_rng([seed, 7])
    fams = w["families"]
    pat = rec["pat"]
    surveil = {"PALB2": 0.62, "ATM": 0.40, "CHEK2": 0.40, "BARD1": 0.30, "RAD51C": 0.30, "RAD51D": 0.30, "BRIP1": 0.2}
    exams = []
    taken = {pat[k]["eid"] for k in pat}
    merges = []
    dup_of = {}
    for key in sorted(pat):
        i, lid = key
        f = fams[i]
        p = next(q for q in f["persons"] if q["lid"] == lid)
        if p["sex"] != "F":
            continue
        start = max(2024.0, p["birth"] + 25)
        end = min(EXPORT_Y, p["birth"] + p["death"])
        if end <= start:
            continue
        known = key in elig or (p["car"] and np.isfinite(p["test"]))
        pr = surveil[K.GENE[f["code"]]] if known else (0.06 if p["degree"] in ("first", "proband") else 0.02)
        if p["role"] == "PROBAND" and known:
            pr = min(0.85, pr + 0.2)
        if rng.random() >= pr:
            continue
        # a proband registered twice: her studies at the second hospital before the merge carry the second ID
        dup = None
        if p["role"] == "PROBAND" and key in elig and rng.random() < 0.08:
            other = [h for h in K.HOSP_CODES if h != pat[key]["hosp"]]
            h2 = other[int(rng.integers(0, len(other)))]
            e2 = ids(rng, 1, "E", 9, taken)[0]
            m2 = ids(rng, 1, "", 8, set())[0]
            mdate = rng.uniform(EXPORT_Y - 0.2, EXPORT_Y - 0.02)
            dup = dict(hosp=h2, mrn=m2, eid=e2, merged=mdate)
            pat[key]["mrns"].append((h2, m2))
            merges.append(dict(retired=e2, surviving=pat[key]["eid"], date=W.workday(W.ydate(mdate)), key=key))
            dup_of[key] = dup
        y = start + rng.uniform(0, 1.0)
        while y < end:
            r = rng.random()
            status = "Completed" if r < 0.9 else ("Cancelled" if r < 0.96 else "No show")
            reason = "Screening" if rng.random() < 0.92 else "Diagnostic"
            hosp, mrn = pat[key]["mrns"][0]
            eid = pat[key]["eid"]
            if dup and y < dup["merged"] and (y >= WIN0 or rng.random() < 0.5):
                hosp, mrn, eid = dup["hosp"], dup["mrn"], dup["eid"]
            exams.append(dict(key=key, date=W.workday(W.ydate(y)), hosp=hosp, mrn=mrn, eid=eid, status=status, reason=reason))
            if status != "Completed":
                y += rng.uniform(0.05, 0.3)
            else:
                y += rng.uniform(0.85, 1.25) if rng.random() < 0.85 else rng.uniform(1.4, 2.2)
    # every group holds at least one such woman whose window studies carry the retired ID
    for code in K.CODES:
        def stale_only(k, d):
            win = [e for e in exams if e["key"] == k and e["status"] == "Completed" and e["reason"] == "Screening"
                   and K.MRI_WINDOW[0] <= e["date"] <= K.MRI_WINDOW[1]]
            return bool(win) and all(e["eid"] == d["eid"] for e in win)
        hit = any(fams[k[0]]["code"] == code and k in elig and stale_only(k, d) for k, d in dup_of.items())
        if hit:
            continue
        cands = sorted({e["key"] for e in exams if fams[e["key"][0]]["code"] == code and e["key"] in elig and
                        e["key"][1] == fams[e["key"][0]]["proband"] and e["key"] not in dup_of and
                        e["status"] == "Completed" and e["reason"] == "Screening" and
                        K.MRI_WINDOW[0] <= e["date"] <= K.MRI_WINDOW[1]})
        if not cands:
            continue
        key = cands[int(rng.integers(0, len(cands)))]
        other = [h for h in K.HOSP_CODES if h != pat[key]["hosp"]]
        h2 = other[int(rng.integers(0, len(other)))]
        e2 = ids(rng, 1, "E", 9, taken)[0]
        m2 = ids(rng, 1, "", 8, set())[0]
        last = max(W.yfrac(e["date"]) for e in exams if e["key"] == key and e["date"] <= K.MRI_WINDOW[1])
        mdate = min(EXPORT_Y - 0.01, last + rng.uniform(0.05, 0.3))
        dup_of[key] = dict(hosp=h2, mrn=m2, eid=e2, merged=mdate)
        pat[key]["mrns"].append((h2, m2))
        merges.append(dict(retired=e2, surviving=pat[key]["eid"], date=W.workday(W.ydate(mdate)), key=key))
        for e in exams:
            if e["key"] == key and K.MRI_WINDOW[0] <= e["date"] <= K.MRI_WINDOW[1]:
                e["hosp"], e["mrn"], e["eid"] = h2, m2, e2
    # merges of other duplicate registrations on the register (most of them unrelated to any study)
    keys = sorted(pat)
    for _ in range(int(len(keys) * 0.012)):
        key = keys[int(rng.integers(0, len(keys)))]
        if key in dup_of:
            continue
        e2 = ids(rng, 1, "E", 9, taken)[0]
        merges.append(dict(retired=e2, surviving=pat[key]["eid"], date=W.workday(W.ydate(rng.uniform(2016.5, EXPORT_Y - 0.02))),
                           key=key))
    merges.sort(key=lambda m: (m["date"], m["retired"]))
    rec["exams"], rec["merges"], rec["duplicates"] = exams, merges, dup_of
    return rec


def screened(rec, key, current_only=False):
    """A completed screening MRI in the twelve months to the export, keyed on the woman's current enterprise ID and,
    unless current_only, on every ID merged into it."""
    eid = rec["pat"][key]["eid"]
    ok = {eid}
    if not current_only:
        ok |= {m["retired"] for m in rec["merges"] if m["surviving"] == eid}
    for e in rec["exams"]:
        if e["eid"] in ok and e["status"] == "Completed" and e["reason"] == "Screening" \
                and K.MRI_WINDOW[0] <= e["date"] <= K.MRI_WINDOW[1]:
            return True
    return False
