"""task464 architecture 8: the input pack.

The service's own records. No file states a hit rate, a corrected share or a ranking. The coding manual says
what each category means and never how often it is recognised; the quality procedure says how the moderation
sample is drawn and never what to do with it.

Layer 1, all of it from the service's own systems and none of it carrying the stump: the student record system
changed between the winter and spring terms, so T1 and T2 come out as a flat CSV and T3 and T4 as JSON with its
own field names; a merger renamed two sites, so the earlier export carries the former names; the enrolment
extract is keyed on the unique learner number while the sites use their own learner references.
"""
import csv, json, os, datetime as dt
import numpy as np
import world as W
import sim as S

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
STATUS = ["completed", "continuing", "withdrawn"]


def _d(s):
    return dt.date.fromisoformat(s)


def build(sim):
    """The withdrawal records (the call's path) and the enrolment extract with its course catalogue.

    The catalogue is the only place a course's planned hours appear once. The enrolment extract opens a row per
    term a course spans and repeats the course's whole hours on each, because the hours belong to the course.
    A course running across the system change is closed under its old reference after its winter term and
    created again under a new reference for its spring term, so its learners' two rows sit on two references.
    """
    rng = np.random.default_rng(W.PACK_SEED)
    rows = sim["rows"]
    tcodes = [t["code"] for t in W.TERMS]
    cut = tcodes.index(W.CUTOVER_AFTER)

    # --- the course catalogue -------------------------------------------------------------
    planned = []
    for area in W.CURRICULUM:
        for _ in range(42):
            span = 2 if rng.random() < W.TWO_TERM_SHARE else 1
            ti = int(rng.integers(0, len(W.TERMS) - 1)) if span == 2 else int(rng.integers(0, len(W.TERMS)))
            site = W.SITES[int(rng.integers(0, len(W.SITES)))]
            planned.append({"curriculum_area": area, "site_code": site["code"],
                            "planned_guided_hours": int(rng.choice(W.GUIDED_HOURS)),
                            "start_term": tcodes[ti], "terms_spanned": span, "ord": float(rng.random())})
    # a course across the cutover gets a second occurrence for its spring term
    for c in list(planned):
        if c["terms_spanned"] == 2 and tcodes.index(c["start_term"]) == cut:
            y = dict(c, start_term=tcodes[cut + 1], terms_spanned=1, ord=float(rng.random()))
            c["recreated_as"] = y
            planned.append(y)
    # references are issued in the order courses were set up, term by term, with the gaps a live system leaves
    planned.sort(key=lambda c: (tcodes.index(c["start_term"]), c["ord"]))
    idr = np.random.default_rng(W.PACK_SEED + 5)
    k = 1000 + int(idr.integers(0, 400))
    for c in planned:
        k += 1 + int(idr.integers(0, 4))
        c["course_ref"] = "C-%05d" % k
    courses = [{key: c[key] for key in ("course_ref", "curriculum_area", "site_code", "planned_guided_hours",
                                        "start_term", "terms_spanned")} for c in planned]
    recreated = {id(c["recreated_as"]) for c in planned if "recreated_as" in c}
    originals = [c for c in planned if id(c) not in recreated]

    def legs(c):
        """(term, reference) for each term the learner attends, following a cutover course to its new ref."""
        i = tcodes.index(c["start_term"])
        out = [(tcodes[i], c["course_ref"])]
        if c["terms_spanned"] == 2:
            out.append((tcodes[i + 1], c["recreated_as"]["course_ref"] if "recreated_as" in c
                        else c["course_ref"]))
        return out

    ulr = np.random.default_rng(W.PACK_SEED + 7)
    issued = set()

    def new_uln():
        while True:
            u = str(int(ulr.integers(1000000000, 9999999999)))
            if u not in issued:
                issued.add(u)
                return u

    enrolments, wmeta = [], {}

    # --- the withdrawals: one learner-course each, withdrawn in its first term ---------------
    starting = {t: [c for c in originals if c["start_term"] == t] for t in tcodes}
    for r in rows:
        uln = new_uln()
        t = W.term(r["term"])
        pool = starting[r["term"]]
        c = pool[int(rng.integers(0, len(pool)))]
        site = [x for x in W.SITES if x["code"] == c["site_code"]][0]
        start = _d(t["start"]) + dt.timedelta(days=int(rng.integers(0, 10)))
        wdate = start + dt.timedelta(days=int(rng.integers(14, 70)))
        if wdate > _d(t["end"]):
            wdate = _d(t["end"])
        wmeta[r["wid"]] = {"uln": uln, "site": site, "curriculum": c["curriculum_area"],
                           "start": start.isoformat(), "wdate": wdate.isoformat(),
                           "local_ref": "%s/%06d" % (site["code"], int(ulr.integers(10000, 999999)))}
        enrolments.append({"uln": uln, "term_code": r["term"], "site_code": site["code"],
                           "curriculum_area": c["curriculum_area"], "course_ref": c["course_ref"],
                           "start_date": start.isoformat(), "status": "withdrawn",
                           "guided_hours_planned": c["planned_guided_hours"]})

    # --- the learners who did not withdraw -------------------------------------------------
    target = W.ENROLMENTS - len(enrolments)
    made = 0
    while made < target:
        uln = new_uln()
        c = originals[int(rng.integers(0, len(originals)))]
        lg = legs(c)
        done = rng.random() < 0.86
        site = c["site_code"]
        moved = rng.random() < W.TRANSFER_SHARE
        other = None
        if moved:
            cand = [x["code"] for x in W.SITES if x["code"] != site]
            other = cand[int(rng.integers(0, len(cand)))]
        for k, (tc, ref) in enumerate(lg):
            t = W.term(tc)
            start = _d(t["start"]) + dt.timedelta(days=int(rng.integers(0, 10)))
            # a mid-course move leaves the sending centre's row open and closes the receiving centre's
            if moved and len(lg) == 2:
                here = site if k == 0 else other
                stat = "continuing" if k == 0 else ("completed" if done else "continuing")
            else:
                here = site
                stat = ("completed" if done else "continuing") if k == len(lg) - 1 else "continuing"
            enrolments.append({"uln": uln, "term_code": tc, "site_code": here,
                               "curriculum_area": c["curriculum_area"], "course_ref": ref,
                               "start_date": start.isoformat(), "status": stat,
                               "guided_hours_planned": c["planned_guided_hours"]})
            made += 1
            if made >= target:
                break

    # --- subcontracted delivery, outside the review's five centres -------------------------
    shares = np.array([t["share"] for t in W.TERMS]); shares = shares / shares.sum()
    for _ in range(W.SUBCONTRACT_ENROLMENTS):
        uln = new_uln()
        t = W.TERMS[int(rng.choice(len(W.TERMS), p=shares))]
        pool = starting[t["code"]]
        c = pool[int(rng.integers(0, len(pool)))]
        start = _d(t["start"]) + dt.timedelta(days=int(rng.integers(0, 10)))
        enrolments.append({"uln": uln, "term_code": t["code"],
                           "site_code": W.SUBCONTRACT_SITE["code"],
                           "curriculum_area": c["curriculum_area"], "course_ref": c["course_ref"],
                           "start_date": start.isoformat(),
                           "status": "completed" if rng.random() < 0.79 else "continuing",
                           "guided_hours_planned": c["planned_guided_hours"]})
    return enrolments, wmeta, courses


def write(sim, enrolments, wmeta, courses):
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(W.SEED + 29)
    rows = sim["rows"]
    written = []
    # withdrawal references come off the student record's own counter, which other record types share
    wrng = np.random.default_rng(W.SEED + 43)
    wref, k = {}, 204000 + int(wrng.integers(0, 900))
    for r in rows:
        k += 1 + int(wrng.integers(0, 3))
        wref[r["wid"]] = "WD%07d" % k

    def csvw(name, data, fields, sortkeys):
        data = sorted(data, key=lambda r: tuple(str(r[f]) for f in sortkeys))
        with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            for r in data:
                w.writerow({k: r[k] for k in fields})
        written.append((name, len(data)))

    # --- the withdrawal records, in two exports across the system change -----------------
    # The old system took the reason code as typed, so a few carry a stray case or space. Winter withdrawals
    # keyed late, after the old system had closed, were entered in the new one as well, so they come out in
    # both exports under the same reference.
    nrng = np.random.default_rng(W.SEED + 37)
    a, b = [], []
    for r in rows:
        m = wmeta[r["wid"]]
        site = m["site"]
        rec_b = {"withdrawalRef": wref[r["wid"]], "localRef": m["local_ref"],
                 "learnerUln": m["uln"], "siteCode": site["code"],
                 "curriculumArea": m["curriculum"], "termCode": r["term"],
                 "withdrawalDate": m["wdate"], "exitComment": r["comment"],
                 "exitReasonCode": r["coded"]}
        if W.term(r["term"])["export"] == "A":
            code = r["coded"]
            u = nrng.random()
            if u < 0.018:
                code = code.lower()
            elif u < 0.030:
                code = code + " "
            elif u < 0.036:
                code = code[0] + code[1].lower()
            a.append({"withdrawal_ref": wref[r["wid"]], "learner_ref": m["local_ref"],
                      "uln": m["uln"],
                      "centre": site["former"] or site["name"], "curriculum_area": m["curriculum"],
                      "term": W.term(r["term"])["label"], "withdrawal_date": m["wdate"],
                      "exit_comment": r["comment"], "reason_code": code})
            if r["term"] == W.CUTOVER_AFTER and m["wdate"] >= "2025-12-08" and nrng.random() < W.LATE_KEYED_SHARE:
                b.append(rec_b)
        else:
            b.append(rec_b)
    csvw("withdrawals_autumn_winter_2025.csv", a,
         ["withdrawal_ref", "learner_ref", "uln", "centre", "curriculum_area", "term",
          "withdrawal_date", "exit_comment", "reason_code"], ["withdrawal_ref"])
    b = sorted(b, key=lambda r: r["withdrawalRef"])
    with open(os.path.join(OUT, "withdrawals_spring_summer_2026.json"), "w", encoding="utf-8") as fh:
        json.dump({"extract": "Learner Withdrawal Extract", "system": "Horizon SR v4",
                   "service": W.SERVICE, "terms": ["T3", "T4"], "records": b}, fh, indent=1)
        fh.write("\n")
    written.append(("withdrawals_spring_summer_2026.json", len(b)))

    # --- the moderation sample ------------------------------------------------------------
    mod = []
    for r in rows:
        if not r["moderated"]:
            continue
        m = wmeta[r["wid"]]
        d = _d(W.term(r["term"])["end"]) + dt.timedelta(days=int(rng.integers(6, 26)))
        mod.append({"withdrawal_ref": wref[r["wid"]], "term_code": r["term"],
                    "coded_reason": r["coded"], "moderated_reason": r["true"],
                    "moderator": W.PEOPLE["moderator"], "moderation_date": d.isoformat()})
    csvw("coding_moderation_2025_26.csv", mod,
         ["withdrawal_ref", "term_code", "coded_reason", "moderated_reason", "moderator",
          "moderation_date"], ["withdrawal_ref"])

    # --- the enrolment extract, the pack's large file -------------------------------------
    csvw("enrolments_2025_26.csv", enrolments,
         ["uln", "term_code", "site_code", "curriculum_area", "course_ref", "start_date",
          "status", "guided_hours_planned"], ["uln"])

    # --- reference -------------------------------------------------------------------------
    csvw("site_directory.csv",
         [{"site_code": s["code"], "site_name": s["name"],
           "former_name": s["former"] or "", "renamed_on": "2026-01-05" if s["former"] else ""}
          for s in W.SITES],
         ["site_code", "site_name", "former_name", "renamed_on"], ["site_code"])
    csvw("course_catalogue_2025_26.csv", courses,
         ["course_ref", "curriculum_area", "site_code", "planned_guided_hours", "start_term",
          "terms_spanned"], ["course_ref"])
    csvw("reason_code_list.csv",
         [{"reason_code": c, "reason_label": W.LABEL[c], "manual_order": i + 1}
          for i, c in enumerate(W.CODES)],
         ["reason_code", "reason_label", "manual_order"], ["manual_order"])
    return written


def main():
    sim = S.simulate()
    enr, wmeta, courses = build(sim)
    for name, n in write(sim, enr, wmeta, courses):
        print("  %-44s %7d rows" % (name, n))


if __name__ == "__main__":
    main()
