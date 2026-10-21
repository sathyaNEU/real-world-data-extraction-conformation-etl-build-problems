"""Readers of the cut pack, shared by the analysis and the cracker: every figure the build reports is computed from the
files in target/, never from the world."""
import csv
import datetime as dt
import os

import numpy as np

import common as K

FDR_FEMALE = ("MOTHER", "SISTER", "DAUGHTER")


def rows(target, key):
    with open(os.path.join(target, K.FILES[key]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def day(s):
    return dt.date.fromisoformat(s) if s else None


def pedigree(target):
    return rows(target, "pedigree")


def first_breast(r):
    """Age at the first breast cancer on a pedigree row, or None."""
    ages = [int(r["cancer_%d_age" % k]) for k in (1, 2, 3) if r["cancer_%d" % k] == "Breast" and r["cancer_%d_age" % k]]
    return min(ages) if ages else None


def lab_final(target):
    """Each person's final reports (a report superseded by an amendment or a re-analysis is set aside): whether any
    shows a variant, whether any was a test, and the genes reported."""
    L = rows(target, "labs")
    superseded = {r["supersedes"] for r in L if r["supersedes"]}
    out = {}
    for r in L:
        if r["report_id"] in superseded:
            continue
        d = out.setdefault(r["person_id"], dict(tested=True, positive=False, classes=set()))
        if r["result"] in ("Variant identified", "Detected", "Positive"):
            d["positive"] = True
            d["classes"].add(r["classification"])
    return out


def histories(target, roles=FDR_FEMALE, ped=None, labs=None):
    """By group: (t, ev, carrier, tested, living) for the pedigree rows with the given relationships; t is the age at
    a first breast cancer before 70, else the age the row gives (at the history date or at death)."""
    ped = pedigree(target) if ped is None else ped
    labs = lab_final(target) if labs is None else labs
    out = {c: [] for c in K.CODES}
    for r in ped:
        if r["relationship"] not in roles:
            continue
        b = first_breast(r)
        age = int(r["age"])
        ev = b is not None
        t = b if ev else age
        lf = labs.get(r["person_id"])
        out[r["family_variant_group"]].append((t, int(ev), int(bool(lf and lf["positive"])), int(bool(lf)),
                                                int(r["vital_status"] == "Living")))
    return {c: np.array(v, float) for c, v in out.items()}


def probands(target, ped=None):
    ped = pedigree(target) if ped is None else ped
    out = {c: [] for c in K.CODES}
    for r in ped:
        if r["relationship"] == "PROBAND":
            out[r["family_variant_group"]].append((first_breast(r), 1))
    return {c: np.array(v, float) for c, v in out.items()}


def incidence(target):
    """The registry's rates per 100,000 by 5-year band from 00-04, recomputed from cases and person-years."""
    R = rows(target, "incidence")
    return np.array([int(r["first_primary_breast_cancers"]) / int(r["female_patient_years"]) * 1e5 for r in R])
