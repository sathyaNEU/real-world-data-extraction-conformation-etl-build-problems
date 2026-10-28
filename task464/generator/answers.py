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

    # --- the asks ---------------------------------------------------------------------
    # The review's scope is the service's five centres, which site_directory.csv is the only list of.
    in_scope = {s["site_code"] for s in sites}
    enr_scope = [e for e in enr if e["site_code"] in in_scope]
    a1 = {}
    for a in W.CURRICULUM:
        rows = [e for e in enr_scope if e["curriculum_area"] == a]
        hours = sum(int(e["guided_hours_planned"]) for e in rows)
        a1[a] = {"enrolments": len(rows), "planned_hours_nearest_10": int(round(hours / 10.0) * 10)}
    a2 = {}
    for s in sites:
        rows = [e for e in enr_scope if e["site_code"] == s["site_code"]]
        comp = sum(1 for e in rows if e["status"] == "completed")
        a2[s["site_name"]] = round(100.0 * comp / len(rows), 1)
    a3 = {}
    for i in codes:
        sub = [m for m in mod if m["coded_reason"] == i]
        a3[i] = sum(1 for m in sub if m["moderated_reason"] != i)
    a3_total = sum(a3.values())

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
        "ask2_completion_pct": a2,
        "ask3_changed_on_moderation": a3,
        "ask3_changed_total": a3_total,
        "enrolments_in_scope": len(enr_scope),
        "enrolments_in_extract": len(enr),
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
    print("ask3 changed on moderation:", f["ask3_changed_on_moderation"], "total", f["ask3_changed_total"])
    print("figures.json written")


if __name__ == "__main__":
    main()
