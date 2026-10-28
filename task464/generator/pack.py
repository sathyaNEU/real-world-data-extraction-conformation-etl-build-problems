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
    """
    rng = np.random.default_rng(W.SEED + 13)
    rows = sim["rows"]

    # --- the course catalogue -------------------------------------------------------------
    courses = []
    cid = 0
    for area in W.CURRICULUM:
        for _ in range(42):
            cid += 1
            span = 2 if rng.random() < W.TWO_TERM_SHARE else 1
            ti = int(rng.integers(0, len(W.TERMS) - 1)) if span == 2 else int(rng.integers(0, len(W.TERMS)))
            site = W.SITES[int(rng.integers(0, len(W.SITES)))]
            courses.append({"course_ref": "C-%04d" % cid, "curriculum_area": area,
                            "site_code": site["code"], "planned_guided_hours": int(rng.choice([30, 45, 60, 90, 120])),
                            "start_term": W.TERMS[ti]["code"],
                            "terms_spanned": span})
    by_area = {}
    for c in courses:
        by_area.setdefault(c["curriculum_area"], []).append(c)

    def term_codes(c):
        i = [t["code"] for t in W.TERMS].index(c["start_term"])
        return [W.TERMS[i]["code"]] + ([W.TERMS[i + 1]["code"]] if c["terms_spanned"] == 2 else [])

    uln = 1500000000
    enrolments, wmeta = [], {}

    # --- the withdrawals: one learner-course each, the call's own population ---------------
    for r in rows:
        uln += 1
        t = W.term(r["term"])
        site = W.SITES[int(rng.integers(0, len(W.SITES)))]
        cur = W.CURRICULUM[int(rng.integers(0, len(W.CURRICULUM)))]
        start = _d(t["start"]) + dt.timedelta(days=int(rng.integers(0, 10)))
        wdate = start + dt.timedelta(days=int(rng.integers(14, 70)))
        if wdate > _d(t["end"]):
            wdate = _d(t["end"])
        wmeta[r["wid"]] = {"uln": str(uln), "site": site, "curriculum": cur,
                           "start": start.isoformat(), "wdate": wdate.isoformat(),
                           "local_ref": "%s/%06d" % (site["code"], (r["wid"] % 900000) + 1)}
        c = by_area[cur][int(rng.integers(0, len(by_area[cur])))]
        enrolments.append({"uln": str(uln), "term_code": r["term"], "site_code": site["code"],
                           "curriculum_area": cur, "course_ref": c["course_ref"],
                           "start_date": start.isoformat(), "status": "withdrawn",
                           "guided_hours_planned": c["planned_guided_hours"]})

    # --- the learners who did not withdraw -------------------------------------------------
    target = W.ENROLMENTS - len(enrolments)
    made = 0
    while made < target:
        uln += 1
        c = courses[int(rng.integers(0, len(courses)))]
        tcs = term_codes(c)
        done = rng.random() < 0.86
        site = c["site_code"]
        moved = rng.random() < W.TRANSFER_SHARE
        other = None
        if moved:
            cand = [x["code"] for x in W.SITES if x["code"] != site]
            other = cand[int(rng.integers(0, len(cand)))]
        for k, tc in enumerate(tcs):
            t = W.term(tc)
            start = _d(t["start"]) + dt.timedelta(days=int(rng.integers(0, 10)))
            # a mid-course move leaves the sending centre's row open and closes the receiving centre's
            if moved and len(tcs) == 2:
                here = site if k == 0 else other
                stat = "continuing" if k == 0 else ("completed" if done else "continuing")
            else:
                here = site
                stat = ("completed" if done else "continuing") if k == len(tcs) - 1 else "continuing"
            enrolments.append({"uln": str(uln), "term_code": tc, "site_code": here,
                               "curriculum_area": c["curriculum_area"], "course_ref": c["course_ref"],
                               "start_date": start.isoformat(), "status": stat,
                               "guided_hours_planned": c["planned_guided_hours"]})
            made += 1
            if made >= target:
                break

    # --- subcontracted delivery, outside the review's five centres -------------------------
    shares = np.array([t["share"] for t in W.TERMS]); shares = shares / shares.sum()
    for _ in range(W.SUBCONTRACT_ENROLMENTS):
        uln += 1
        t = W.TERMS[int(rng.choice(len(W.TERMS), p=shares))]
        c = courses[int(rng.integers(0, len(courses)))]
        start = _d(t["start"]) + dt.timedelta(days=int(rng.integers(0, 10)))
        enrolments.append({"uln": str(uln), "term_code": t["code"],
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

    def csvw(name, data, fields, sortkeys):
        data = sorted(data, key=lambda r: tuple(str(r[f]) for f in sortkeys))
        with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            for r in data:
                w.writerow({k: r[k] for k in fields})
        written.append((name, len(data)))

    # --- the withdrawal records, in two exports across the system change -----------------
    a, b = [], []
    for r in rows:
        m = wmeta[r["wid"]]
        site = m["site"]
        if W.term(r["term"])["export"] == "A":
            a.append({"withdrawal_ref": "WD%06d" % r["wid"], "learner_ref": m["local_ref"],
                      "uln": m["uln"],
                      "centre": site["former"] or site["name"], "curriculum_area": m["curriculum"],
                      "term": W.term(r["term"])["label"], "withdrawal_date": m["wdate"],
                      "exit_comment": r["comment"], "reason_code": r["coded"]})
        else:
            b.append({"withdrawalRef": "WD%06d" % r["wid"], "localRef": m["local_ref"],
                      "learnerUln": m["uln"], "siteCode": site["code"],
                      "curriculumArea": m["curriculum"], "termCode": r["term"],
                      "withdrawalDate": m["wdate"], "exitComment": r["comment"],
                      "exitReasonCode": r["coded"]})
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
        mod.append({"withdrawal_ref": "WD%06d" % r["wid"], "term_code": r["term"],
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
