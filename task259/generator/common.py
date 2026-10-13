"""task259 constants and helpers shared by every generator module.

Tarnwick Systems (fictional), a US software company: its Data Engineer pay bands for 1 April 2027 from Tallyband
(a fictional salary-sharing platform) as in effect on the 1 October 2026 benchmark date, and the two ask paths (the
HRIS job history, the ATS requisitions)."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2590929

COMPANY = "Tarnwick Systems"
PLATFORM = "Tallyband"
PEOPLE = {"head": "Patty Carroll", "comp": "Cole Gillespie", "data": "Wanda Kane"}

BENCHMARK = dt.date(2026, 10, 1)
EFFECTIVE = dt.date(2027, 4, 1)
EXTRACT_FROM = dt.date(2023, 10, 2)          # Tallyband keeps reports filed in the 36 months to the extract
HR_EXPORT = dt.date(2026, 10, 14)            # the HRIS and ATS exports the people data team pulled

# The market for every Data Engineer level (the world's own, never shipped as figures): the median base pay at the
# benchmark date, the market's movement at a fixed level, each person's merit inside the level, the promotion step
LEVELS = ["I", "II", "III", "IV"]
MARKET_MEDIAN = {"I": 116922.7, "II": 142895.5, "III": 168071.8, "IV": 201031.0}
MOVEMENT = 0.017            # a year, continuous
MERIT = 0.030               # a year inside the level, continuous
PROMOTION_STEP = 0.165      # log step between adjacent levels at promotion
SPREAD = {"I": 0.1050, "II": 0.1100, "III": 0.1188, "IV": 0.1200}   # log sd of base pay at a level and date

# Tallyband's families and the shares of respondents in each (the extract holds every family)
FAMILIES = [("Software Engineering", 0.40), ("Data Engineering", 0.16), ("Machine Learning Engineering", 0.08),
            ("Data Science", 0.10), ("Product Management", 0.08), ("Design", 0.06), ("Site Reliability", 0.06),
            ("Security Engineering", 0.06)]
N_RESPONDENTS = 36_000
# Within Tallyband's data engineering family: primary focus and its pay step against data pipelines
DE_FOCUS = [("data pipelines and platforms", 0.75, 0.0), ("machine learning infrastructure", 0.17, 0.12),
            ("analytics engineering", 0.08, -0.07)]

# The pack's files, in Tarnwick's and Tallyband's own naming
POLICY = "tarnwick_compensation_policy_2026.pdf"
EXTRACT = "tallyband_extract_2026-10-01.csv"
PROFILES = "tallyband_profiles_2026-10-01.csv"
METHODOLOGY = "tallyband_methodology.md"
ARCHITECTURE = "tarnwick_engineering_job_architecture.xlsx"
CROSSWALK = "level_crosswalk_2026.csv"
OFFERS = "tallyband_offers_extract_2026-10-01.csv"
OEWS = "oews_database_architects_2025.csv"
HRIS = "hris_job_history_2026-10-14.csv"
ZONES = "pay_zones_2026.csv"
ATS = "ats_requisitions_2026-10-14.csv"
PEOPLE_NOTES = "people_data_exports_readme.md"
DISTRACTORS = (OFFERS, OEWS)
DELIVERABLES = ("data_engineer_bands_2027.xlsx", "data_engineer_bands_2027.svg")


def stream(*keys) -> np.random.Generator:
    """One RNG stream per named component, seeded by blake2b so no process salt reaches it."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8)
    return np.random.default_rng(int.from_bytes(h.digest(), "big"))


def hexid(*keys, n=12) -> str:
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).hexdigest()[:n]


def years_to_benchmark(d: dt.date) -> float:
    return (BENCHMARK - d).days / 365.25

ARCH_HEADER_ROW = 3                           # the Jobs sheet's header row (0-based), under its title block
