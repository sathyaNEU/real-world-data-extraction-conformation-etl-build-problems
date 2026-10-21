"""The golden, computed from the cut pack: each group's breast cancer risk by 70 for a woman who carries it, by the
kin-cohort on the probands' mothers, sisters and daughters (each a carrier with probability one half, the population's
risk from the tumor registry's rates for the half who are not), checked against the Mendelian likelihood family; the
program's verdicts; and the criteria's two planning figures for the High-Risk Breast Clinic."""
import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import models as M      # noqa: E402
import pack as PK       # noqa: E402

LINE = 0.30


def published_rates(target):
    return np.array([float(r["rate_per_100000"]) for r in PK.rows(target, "incidence")])


def call(target):
    ped = PK.pedigree(target)
    labs = PK.lab_final(target)
    H = PK.histories(target, ped=ped, labs=labs)
    PB = PK.probands(target, ped=ped)
    rates = published_rates(target)
    res = {}
    for c in K.CODES:
        t, ev, car, tested, alive = H[c].T
        res[c] = M.estimates(t, ev, car, tested, alive, rates, PB[c][:, 0], PB[c][:, 1])
        res[c]["retrospective"] = M.retrospective(t, ev, car, tested, rates)
        res[c]["n_relatives"] = int(len(t))
        res[c]["n_tested"] = int(tested.sum())
        res[c]["n_tested_carriers"] = int(((tested == 1) & (car == 1)).sum())
        res[c]["n_families"] = int(len(PB[c]))
    qualify = [c for c in K.CODES if res[c]["kin"] >= LINE]
    # the testing the decisive step answers: living relatives of the groups identified late, by diagnosis
    late = [c for c in K.CODES if K.LATE[c]]
    ra, ru = [], []
    for c in late:
        t, ev, car, tested, alive = H[c].T
        ra.append(tested[(alive == 1) & (ev == 1)].mean())
        ru.append(tested[(alive == 1) & (ev == 0)].mean())
    lt = {"affected_lo": int(round(100 * min(ra))), "affected_hi": int(round(100 * max(ra))),
          "unaffected_lo": int(round(100 * min(ru))), "unaffected_hi": int(round(100 * max(ru)))}
    return dict(res=res, qualify=qualify, f_n=float(M.pop_risk(rates)), late_testing=lt)


def sets(res, key):
    return [c for c in K.CODES if res[c][key] >= LINE]


# ------------------------------------------------------------------------------------------ planning figures
def age_on(dob, d):
    return d.year - dob.year - ((d.month, d.day) < (dob.month, dob.day))


def both_removed(eid, abstracts, procedures, use_registry=True):
    sides = set()
    if use_registry:
        for a in abstracts.get(eid, []):
            code = int(a["surgery_primary_site_code"])
            if code in (41, 42, 51, 56):
                sides.add({"Left": "LT", "Right": "RT"}[a["laterality"]])
            if code in (42, 56):
                sides |= {"LT", "RT"}
    for q in procedures.get(eid, []):
        if q["cpt_code"] in ("19303", "19305", "19306", "19307"):
            sides |= {"LT", "RT"} if q["modifier"] == "50" else {q["modifier"]}
    return sides >= {"LT", "RT"}


def by_eid(R):
    out = {}
    for r in R:
        out.setdefault(r["enterprise_id"], []).append(r)
    return out


def known_women(target):
    """Women with a final report showing the family's variant (pathogenic or likely pathogenic), by person."""
    ped = {r["person_id"]: r for r in PK.pedigree(target)}
    labs = PK.lab_final(target)
    out = {}
    for pid, d in labs.items():
        r = ped[pid]
        if d["positive"] and r["sex"] == "F" and d["classes"] & {"Pathogenic", "Likely pathogenic"}:
            out[pid] = r
    return out


def ask_a(target, use_registry=True, women=None):
    """Criteria 3.1: known carriers with an enterprise ID, no recorded death, aged 30 to 74 on 1 April 2027, not both
    breasts removed."""
    women = known_women(target) if women is None else women
    dead = {r["enterprise_id"] for r in PK.rows(target, "deaths")}
    ab = by_eid(PK.rows(target, "abstracts"))
    pr = by_eid(PK.rows(target, "surgery"))
    out = {}
    for pid, r in women.items():
        eid = r["enterprise_id"]
        if not eid or eid in dead or r["vital_status"] != "Living":
            continue
        if not 30 <= age_on(PK.day(r["birth_date"]), K.PROGRAM_START) <= 74:
            continue
        if both_removed(eid, ab, pr, use_registry):
            continue
        out[pid] = r
    return out


def ask_b(target, eligible, follow_merges=True):
    """Criteria 3.2: of those women, the ones with no completed high-risk screening MRI from 1 October 2025 to 30
    September 2026, each study keyed to its woman through the EMPI (a retired enterprise ID to the one it was merged
    into)."""
    merged = {}
    for m in PK.rows(target, "merges"):
        merged[m["retired_enterprise_id"]] = m["surviving_enterprise_id"]

    def current(e):
        seen = set()
        while follow_merges and e in merged and e not in seen:
            seen.add(e)
            e = merged[e]
        return e
    lo, hi = K.MRI_WINDOW
    had = set()
    for x in PK.rows(target, "imaging"):
        if x["status"] == "COMPLETED" and x["indication"] == "SCREENING - HIGH RISK" and lo <= PK.day(x["exam_date"]) <= hi:
            had.add(current(x["enterprise_id"]))
    return {pid: r for pid, r in eligible.items() if r["enterprise_id"] not in had}


def count(people):
    out = {c: 0 for c in K.CODES}
    for r in people.values():
        out[r["family_variant_group"]] += 1
    return out


def asks(target):
    A = ask_a(target)
    B = ask_b(target, A)
    return dict(A=A, B=B, a=count(A), b=count(B))
