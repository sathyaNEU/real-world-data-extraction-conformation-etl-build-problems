"""The pack's data files, in the exporting systems' own layouts: Tallyband's extract and profile table, Tarnwick's
level crosswalk, Tallyband's offers extract and the OEWS wage table beside them, and the people data team's HRIS,
pay zone and ATS exports."""
from __future__ import annotations

import csv
import datetime as dt

import numpy as np
import pandas as pd

import common as K

FOCI = {"Software Engineering": ("backend", "frontend", "full stack", "mobile", "embedded"),
        "Machine Learning Engineering": ("model training", "machine learning platform", "applied machine learning"),
        "Data Science": ("product analytics", "experimentation", "statistical modelling"),
        "Product Management": ("core product", "platform", "growth"),
        "Design": ("product design", "design systems", "user research"),
        "Site Reliability": ("infrastructure", "observability", "incident response"),
        "Security Engineering": ("application security", "cloud security", "detection and response")}
DEGREES = ("bachelor's", "master's", "none", "doctorate", "associate")


def _write(path, df):
    df.to_csv(path, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    return len(df)


def _heap(values, r):
    """What respondents type: a quarter round their salary to the thousand, the rest give it to the dollar."""
    u = r.random(len(values))
    step = np.where(u < 0.25, 1000.0, 1.0)
    return (np.floor(values / step + 0.5) * step).astype(int)


def extract_frame(tb):
    r = K.stream("heap")
    df = tb.copy()
    us = (df.country == "US").to_numpy()
    base = np.where(us, _heap(df.base.to_numpy(), r), np.round(df.base.to_numpy()).astype(int))
    prev = np.where(us, _heap(df.prev_base.to_numpy(), r), np.round(df.prev_base.to_numpy()).astype(int))
    out = pd.DataFrame({
        "respondent_id": df.respondent_id,
        "filed_on": [d.isoformat() for d in df.filed_on],
        "employer": df.employer,
        "employer_level": df.level_code,
        "tallyband_level": df.tallyband_level,
        "job_family": df.family,
        "title": df.title,
        "years_experience": df.years_experience,
        "country": df.country,
        "state": df.state,
        "employment_type": df.employment_type,
        "base_salary_usd": base,
        "previous_filed_on": [d.isoformat() if d is not None else "" for d in df.previous_filed_on],
        "previous_employer_level": df.previous_level_code,
        "previous_base_salary_usd": np.where(df.updated, prev.astype(object), ""),
    })
    out = out.sort_values(["filed_on", "respondent_id"], kind="mergesort").reset_index(drop=True)
    return out


def write_extract(path, tb):
    return _write(path, extract_frame(tb))


def write_profiles(path, tb):
    r = K.stream("profiles")
    focus = []
    for fam, f in zip(tb.family, tb.focus):
        if fam == "Data Engineering":
            focus.append(f)
        else:
            opts = FOCI[fam]
            focus.append(opts[int(r.integers(0, len(opts)))])
    df = pd.DataFrame({"respondent_id": tb.respondent_id, "primary_focus": focus,
                       "works_remotely": np.where(r.random(len(tb)) < 0.31, "yes", "no"),
                       "highest_degree": [DEGREES[int(k)] for k in r.choice(5, len(tb), p=(0.55, 0.31, 0.07, 0.04,
                                                                                           0.03))]})
    return _write(path, df.sort_values("respondent_id", kind="mergesort"))


def write_crosswalk(path, cw):
    return _write(path, cw)


def write_offers(path, of):
    return _write(path, of.sort_values(["offered_on", "offer_id"], kind="mergesort"))


def write_oews(path, oe):
    df = oe.rename(columns={"area": "AREA_TITLE", "occ_code": "OCC_CODE", "occ_title": "OCC_TITLE",
                            "tot_emp": "TOT_EMP", "a_mean": "A_MEAN", "a_pct10": "A_PCT10", "a_pct25": "A_PCT25",
                            "a_median": "A_MEDIAN", "a_pct75": "A_PCT75", "a_pct90": "A_PCT90"})
    return _write(path, df)


def _iso(v):
    return v.isoformat() if isinstance(v, dt.date) else ""


def write_hris(path, hr):
    df = hr.copy()
    df["effective_date"] = [_iso(d) for d in df.effective_date]
    return _write(path, df)


def write_zones(path, zn):
    return _write(path, zn)


def write_ats(path, req):
    df = req.copy()
    for c in ("opened_on", "closed_on", "status_date"):
        df[c] = [_iso(d) for d in df[c]]
    return _write(path, df)
