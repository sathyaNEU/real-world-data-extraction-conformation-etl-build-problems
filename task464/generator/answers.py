"""task464 architecture 8: every graded figure, computed from the SHIPPED pack only.

This module reads target/ the way a solver does. golden.py, checks.py and verify.py all go through it, so a
figure can never be right in one place and wrong in another.
"""
import csv, json, os
import world as W

TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")


def _p(n):
    return os.path.join(TARGET, n)


def load(raw=False):
    coded, seen = [], set()
    labels = {t["label"]: t["code"] for t in W.TERMS}
    stack = [({"ref": r["withdrawal_ref"], "code": r["reason_code"], "term": labels[r["term"]],
               "area": r["curriculum_area"]})
             for r in csv.DictReader(open(_p("withdrawals_autumn_winter_2025.csv"), encoding="utf-8"))]
    stack += [({"ref": r["withdrawalRef"], "code": r["exitReasonCode"], "term": r["termCode"],
                "area": r["curriculumArea"]})
              for r in json.load(open(_p("withdrawals_spring_summer_2026.json"), encoding="utf-8"))["records"]]
    for r in stack:
        if raw:                           # as stacked, for the mess-neutrality checks
            coded.append(dict(r))
            continue
        if r["ref"] in seen:              # a late-keyed winter withdrawal, in both exports
            continue
        seen.add(r["ref"])
        r["code"] = r["code"].strip().upper()
        coded.append(r)
    mod = list(csv.DictReader(open(_p("coding_moderation_2025_26.csv"), encoding="utf-8")))
    enr = list(csv.DictReader(open(_p("enrolments_2025_26.csv"), encoding="utf-8")))
    sites = list(csv.DictReader(open(_p("site_directory.csv"), encoding="utf-8")))
    return coded, mod, enr, sites


def cutover_links(rows, cat):
    """New reference -> old reference for each course created again across the system change.

    Read off the shipped rows alone. A course the catalogue plans over two terms that has no row in its second
    term was closed after its first; the course that carries it on is the one-term course starting in that
    second term at the same centre, in the same curriculum area, with the same planned hours, every one of
    whose learners is one of the first course's continuing learners. Exactly one candidate must qualify.
    """
    tcodes = [t["code"] for t in W.TERMS]
    learners = {}
    for e in rows:
        learners.setdefault((e["course_ref"], e["term_code"]), {}).setdefault(e["uln"], set()).add(e["status"])
    link = {}
    for ref, c in cat.items():
        if int(c["terms_spanned"]) != 2:
            continue
        i = tcodes.index(c["start_term"])
        second = tcodes[i + 1]
        if (ref, second) in learners:
            continue
        first = learners.get((ref, c["start_term"]), {})
        carry = {u for u, st in first.items() if "continuing" in st}
        cands = []
        for ref2, c2 in cat.items():
            if (c2["start_term"] != second or int(c2["terms_spanned"]) != 1
                    or c2["site_code"] != c["site_code"] or c2["curriculum_area"] != c["curriculum_area"]
                    or c2["planned_guided_hours"] != c["planned_guided_hours"]):
                continue
            on = set(learners.get((ref2, second), {}))
            if on and on <= carry:
                cands.append(ref2)
        assert len(cands) == 1, (ref, cands)
        link[cands[0]] = ref
    return link


def figures():
    coded, mod, enr, sites = load()
    codes = W.CODES
    n = len(coded)

    # --- the main call ----------------------------------------------------------------
    q = {c: sum(1 for r in coded if r["code"] == c) / n for c in codes}
    R = {j: {} for j in codes}
    for i in codes:
        sub = [m for m in mod if m["coded_reason"] == i]
        for j in codes:
            R[j][i] = sum(1 for m in sub if m["moderated_reason"] == j) / len(sub)
    p = {j: sum(q[i] * R[j][i] for i in codes) for j in codes}
    order = sorted(codes, key=lambda c: -p[c])
    call, runner = order[0], order[1]

    # --- the asks -------------------------------------------------------------------
    # The review's scope is the service's five centres, the only list of which is site_directory.csv.
    in_scope = {x["site_code"] for x in sites}
    rows = [e for e in enr if e["site_code"] in in_scope]
    cat = {c["course_ref"]: c for c in csv.DictReader(open(_p("course_catalogue_2025_26.csv"), encoding="utf-8"))}
    tcodes = [t["code"] for t in W.TERMS]
    link = cutover_links(rows, cat)
    canon = lambda ref: link.get(ref, ref)

    # a learner-course is the unit: one learner on one course, however many terms it spans
    lc = {}
    for e in rows:
        k = (e["uln"], canon(e["course_ref"]))
        d = lc.setdefault(k, {"terms": set(), "sites": [], "status": set()})
        d["terms"].add(e["term_code"])
        d["sites"].append((e["term_code"], e["site_code"]))
        d["status"].add(e["status"])

    a1 = {}
    for area in W.CURRICULUM:
        ks = [k for k in lc if cat[k[1]]["curriculum_area"] == area]
        a1[area] = {"planned_hours": sum(int(cat[k[1]]["planned_guided_hours"]) for k in ks),
                    "learner_courses": len(ks)}

    a2 = {}
    for x in sites:
        started = [k for k, d in lc.items()
                   if min(d["sites"], key=lambda p: tcodes.index(p[0]))[1] == x["site_code"]]
        done = [k for k in started if "completed" in lc[k]["status"]]
        a2[x["site_name"]] = {"started": len(started),
                              "completed_pct": round(100.0 * len(done) / len(started), 1) if started else 0.0,
                              "completed_raw": (100.0 * len(done) / len(started)) if started else 0.0}

    return {
        "call": call, "call_label": W.LABEL[call],
        "call_share_pct": round(100 * p[call], 1),
        "runner_up": runner, "runner_up_label": W.LABEL[runner],
        "runner_up_share_pct": round(100 * p[runner], 1),
        "gap_points": round(100 * (p[call] - p[runner]), 1),
        "corrected_share_pct": {c: round(100 * p[c], 1) for c in codes},
        "coded_share_pct": {c: round(100 * q[c], 1) for c in codes},
        "withdrawals_total": n,
        "coded_counts": {c: sum(1 for r in coded if r["code"] == c) for c in codes},
        "wh_coded_belonging_cr_pct": round(100 * R["CR"]["WH"], 1),
        "cr_coded_confirmed_pct": round(100 * R["CR"]["CR"], 1),
        "moderated_total": len(mod),
        "ask1_planned_hours": {k: v["planned_hours"] for k, v in a1.items()},
        "ask2_started": {k: v["started"] for k, v in a2.items()},
        "ask2_completed_pct": {k: v["completed_pct"] for k, v in a2.items()},
        "ask2_completed_raw": {k: v["completed_raw"] for k, v in a2.items()},
        "cutover_links": len(link),
        "learner_courses_in_scope": len(lc),
        "enrolment_rows_in_scope": len(rows),
        "enrolment_rows_in_extract": len(enr),
    }


def main():
    f = figures()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    json.dump(f, open(out, "w"), indent=1)
    print("call           : %s at %.1f per cent" % (f["call_label"], f["call_share_pct"]))
    print("runner-up      : %s at %.1f, gap %.1f points" % (f["runner_up_label"], f["runner_up_share_pct"],
                                                            f["gap_points"]))
    print("corrected      :", {W.LABEL[c]: f["corrected_share_pct"][c] for c in W.CODES})
    print("coded          :", {W.LABEL[c]: f["coded_share_pct"][c] for c in W.CODES})
    print("withdrawals %d, moderated %d" % (f["withdrawals_total"], f["moderated_total"]))
    print("ask1 planned hours:", f["ask1_planned_hours"])
    print("ask2 started:", f["ask2_started"])
    print("ask2 completed share:", f["ask2_completed_pct"])
    print("cutover links found:", f["cutover_links"])
    print("learner-courses in scope %d from %d rows (%d in the extract)" % (
        f["learner_courses_in_scope"], f["enrolment_rows_in_scope"], f["enrolment_rows_in_extract"]))
    print("figures.json written")


if __name__ == "__main__":
    main()
