"""task464 architecture 8: every graded figure, computed from the SHIPPED pack only.

This module reads target/ the way a solver does. golden.py, checks.py and verify.py all go through it, so a
figure can never be right in one place and wrong in another.
"""
import csv, json, os
import world as W

TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")


def _p(n):
    return os.path.join(TARGET, n)


def load():
    coded = []
    for r in csv.DictReader(open(_p("withdrawals_autumn_winter_2025.csv"), encoding="utf-8")):
        coded.append({"ref": r["withdrawal_ref"], "code": r["reason_code"], "term": r["term"],
                      "area": r["curriculum_area"]})
    for r in json.load(open(_p("withdrawals_spring_summer_2026.json"), encoding="utf-8"))["records"]:
        coded.append({"ref": r["withdrawalRef"], "code": r["exitReasonCode"], "term": r["termCode"],
                      "area": r["curriculumArea"]})
    mod = list(csv.DictReader(open(_p("coding_moderation_2025_26.csv"), encoding="utf-8")))
    enr = list(csv.DictReader(open(_p("enrolments_2025_26.csv"), encoding="utf-8")))
    sites = list(csv.DictReader(open(_p("site_directory.csv"), encoding="utf-8")))
    return coded, mod, enr, sites


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

    # a learner-course is the unit: one learner on one course, however many terms it spans
    lc = {}
    for e in rows:
        k = (e["uln"], e["course_ref"])
        d = lc.setdefault(k, {"terms": set(), "sites": [], "status": set(), "area": e["curriculum_area"]})
        d["terms"].add(e["term_code"])
        d["sites"].append((e["term_code"], e["site_code"]))
        d["status"].add(e["status"])

    a1 = {}
    for area in W.CURRICULUM:
        ks = [k for k, d in lc.items() if d["area"] == area]
        hours = sum(int(cat[k[1]]["planned_guided_hours"]) for k in ks)
        a1[area] = {"learner_courses": len(ks), "planned_hours": hours}

    a2 = {}
    for x in sites:
        started = [k for k, d in lc.items()
                   if min(d["sites"], key=lambda p: tcodes.index(p[0]))[1] == x["site_code"]]
        done = [k for k in started if "completed" in lc[k]["status"]]
        a2[x["site_name"]] = round(100.0 * len(done) / len(started), 1) if started else 0.0

    a3 = {}
    for i, t in enumerate(W.TERMS[:-1]):
        nxt = tcodes[i + 1]
        a3[t["code"]] = sum(1 for d in lc.values() if t["code"] in d["terms"] and nxt in d["terms"])

    a4 = {}
    for i in codes:
        sub = [m for m in mod if m["coded_reason"] == i]
        a4[i] = sum(1 for m in sub if m["moderated_reason"] != i)

    return {
        "call": call, "call_label": W.LABEL[call],
        "call_share_pct": round(100 * p[call], 1),
        "runner_up": runner, "runner_up_label": W.LABEL[runner],
        "runner_up_share_pct": round(100 * p[runner], 1),
        "gap_points": round(100 * (p[call] - p[runner]), 1),
        "corrected_share_pct": {c: round(100 * p[c], 1) for c in codes},
        "coded_share_pct": {c: round(100 * q[c], 1) for c in codes},
        "withdrawals_total": n,
        "moderated_total": len(mod),
        "ask1_curriculum": a1,
        "ask2_started_and_completed_pct": a2,
        "ask3_carried_over": a3,
        "ask4_changed_on_moderation": a4,
        "ask4_changed_total": sum(a4.values()),
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
    print("ask1 hours:", {k: v["planned_hours"] for k, v in f["ask1_curriculum"].items()})
    print("ask1 learner-courses:", {k: v["learner_courses"] for k, v in f["ask1_curriculum"].items()})
    print("ask2 started-and-completed:", f["ask2_started_and_completed_pct"])
    print("ask3 carried over:", f["ask3_carried_over"])
    print("ask4 changed on moderation:", f["ask4_changed_on_moderation"], "total", f["ask4_changed_total"])
    print("learner-courses in scope %d from %d rows (%d in the extract)" % (
        f["learner_courses_in_scope"], f["enrolment_rows_in_scope"], f["enrolment_rows_in_extract"]))
    print("figures.json written")


if __name__ == "__main__":
    main()
