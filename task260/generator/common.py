"""task260 constants shared by every generator module.

Merrowdale Breast Screening Service (fictional), England: four static screening sites and three mobile units, 26 film
readers, about 45,000 screening studies a year. In 2026 it ran one reader study per AI reading-support tool on
ReadPoint (a fictional reader-study platform) and now chooses one tool for a two-year licence from 1 April 2027."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2600417

ORG = "Merrowdale Breast Screening Service"
PLATFORM = "ReadPoint"
PEOPLE = {"director": "Hayley Kelly", "lead": "Darren Jenkins", "research": "Eileen Walton",
          "procurement": "Gary Pritchard", "ondrix": "Leonard Hilton", "halvic": "Jemma Barnes",
          "lumidra": "Kim Summers"}


def rng(label):
    """One random stream per label, fixed by the build seed."""
    h = hashlib.sha256(("%d/%s" % (SEED, label)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# ------------------------------------------------------------------ the three reader studies, in the order they ran
# kind: 'readers' (the gain swings from reader to reader), 'steady', 'cases' (readers defer to the tool's own case
# score, so the gain sits in the examinations it moves). params: see world.study().
STUDIES = [
    dict(sid="S1", code="MBS-AI-01", tool="Lumidra Detect", vendor="Lumidra AI Ltd", short="Lumidra", kind="cases",
         platform="4.1", first_session=dt.date(2026, 2, 9), export=dt.date(2026, 4, 24), case_prefix="C",
         params=dict(alpha=1.40, lam=2.60, lam_sd=0.30)),
    dict(sid="S2", code="MBS-AI-02", tool="Ondrix Mammo", vendor="Ondrix Imaging Ltd", short="Ondrix",
         kind="readers", platform="4.1", first_session=dt.date(2026, 4, 27), export=dt.date(2026, 7, 8),
         case_prefix="C", params=dict(gain=0.55, reader_sd=0.55, case_sd=0.85)),
    dict(sid="S3", code="MBS-AI-03", tool="Halvic Breast", vendor="Halvic Medical Ltd", short="Halvic",
         kind="steady", platform="4.2", first_session=dt.date(2026, 7, 13), export=dt.date(2026, 9, 25),
         case_prefix="03-", params=dict(alpha=1.90, lam=0.105, lam_sd=0.03)),
]
STUDY_SEEDS = {"S1": 146, "S2": 195, "S3": 32}     # chosen by a seed search against the design note's margins
N_READERS, N_CANCER, N_NORMAL = 10, 75, 225
SESSIONS, PRACTICE = 4, 5                       # four sessions per condition, five practice cases opening each
WASHOUT_DAYS = 28

# Latent reading model (world.study): every reading = reader threshold + case difficulty + reader skill on cancers
# + reader-by-case + reading noise; the probability of malignancy is a logistic of it.
MODEL = dict(mu=1.55, skill_sd=0.25, bias_sd=0.35, vis_sd=0.85, norm_sd=0.55, rc_sd=0.5, e_sd=0.5, theta=1.6,
             slope=1.6)

# ------------------------------------------------------------------ the service
SITES = [  # code, name, town, RIS screening location, assessment clinic, symptomatic clinic
    dict(code="CRB", name="Corrowby Road Breast Unit", town="Merrowdale", ris="CRBBS", assess="CRBAS", sympt="CRBSY"),
    dict(code="WDL", name="Wendlow Breast Screening Centre", town="Wendlow", ris="WDLBS", assess=None, sympt=None),
    dict(code="CPL", name="Copse Lane Breast Screening Centre", town="Kelsford", ris="CPLBS", assess=None,
         sympt="CPLSY"),
    dict(code="TLW", name="Tallowmere Park Breast Unit", town="Lindhallow", ris="TLWBS", assess="TLWAS", sympt=None),
]
SITE_ORDER = [s["code"] for s in SITES]
MOBILE = {"MBSU1": "CPL", "MBSU2": "WDL", "MBSU3": "TLW"}       # current hosts (the location directory)
MU2_OLD_HOST, MU2_OLD_LAST, MU2_NEW_FIRST = "CRB", dt.date(2026, 5, 29), dt.date(2026, 6, 8)
VEHICLES = {"MBSU1": ["MV-0582"], "MBSU2": ["MV-0614", "MV-1127"], "MBSU3": ["MV-0739"]}

# The new imaging system (RIS) went live site by site; for each site's first fortnight studies were registered in
# both systems, and the legacy system's records up to its switch-off were loaded into the new one afterwards.
GO_LIVE = {"CRB": (dt.date(2026, 3, 24), dt.date(2026, 4, 3)), "WDL": (dt.date(2026, 4, 7), dt.date(2026, 4, 17)),
           "CPL": (dt.date(2026, 4, 20), dt.date(2026, 5, 1)), "TLW": (dt.date(2026, 5, 5), dt.date(2026, 5, 15))}
HISTORY_LOAD = dt.date(2026, 6, 12)
WINDOW = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
BANK_HOLIDAYS = {dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 4, 3),
                 dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31)}
BST = [(dt.datetime(2025, 3, 30, 1), dt.datetime(2025, 10, 26, 1)),
       (dt.datetime(2026, 3, 29, 1), dt.datetime(2026, 10, 25, 1))]   # UTC instants daylight time runs between

EXAM_CODES = [  # code, description, programme, sent for AI analysis
    ("MAMS", "Mammography, screening (bilateral, standard views)", "Screening", "yes"),
    ("MAMT", "Mammography, screening technical repeat", "Screening", "yes"),
    ("MAMA", "Mammography, assessment clinic (further views)", "Assessment", "no"),
    ("MAMD", "Mammography, symptomatic diagnostic", "Symptomatic", "no"),
]

# ------------------------------------------------------------------ the vendors' quotes (pounds, excluding VAT)
PRICES = {
    "Ondrix": dict(per_study=1.62, minimum=60000, one_off=14800),
    "Lumidra": dict(per_episode=2.08, per_reader=340, one_off=9500),
    "Halvic": dict(per_seat=2450, per_site=5900, one_off=12000),
}
CONTRACT_START = dt.date(2027, 4, 1)

# ------------------------------------------------------------------ calendar
PROTOCOL_DATE = dt.date(2026, 1, 12)
RIS_PULL = dt.datetime(2026, 10, 5, 8, 47, 12)
WORKFORCE_DATE = dt.date(2026, 10, 9)
QUOTE_DATES = {"Ondrix": dt.date(2026, 9, 24), "Halvic": dt.date(2026, 9, 28), "Lumidra": dt.date(2026, 9, 22)}
PACK_DATE = dt.datetime(2026, 10, 12, 16, 20)
DELIVERY_DATE = dt.date(2026, 11, 10)
PANEL_DATE = dt.date(2026, 11, 18)

# ------------------------------------------------------------------ file names
EXPORTS = {"S1": "readpoint_MBS-AI-01_export_2026-04-24.csv", "S2": "readpoint_MBS-AI-02_export_2026-07-08.csv",
           "S3": "readpoint_MBS-AI-03_export_2026-09-25.csv"}
EXPORT_GUIDE = "readpoint_export_fields_v4.pdf"
CASES = "reader_study_case_sets_2026.xlsx"
PANELS = "reader_study_panels_2026.xlsx"
PROTOCOL = "ai_evaluation_protocol_v2.pdf"
RIS = "ris_mammography_studies_2025-10_2026-09.csv"
CODES = "ris_examination_codes.csv"
LOCATIONS = "screening_locations.json"
VISITS = "mobile_unit_visits_2025-26.xlsx"
WORKFORCE = "film_reader_workforce_2026-10.xlsx"
QUOTES = {"Ondrix": "quote_ondrix_mammo_2027.pdf", "Halvic": "quote_halvic_breast_2027.pdf",
          "Lumidra": "quote_lumidra_detect_2027.pdf"}
PRODUCT_SUMMARIES = "vendor_product_summaries_2026.pdf"
KPIS = "screening_kpis_2023-24_to_2025-26.xlsx"
QA_SCORES = "reader_self_assessment_2025.csv"

DELIVERABLES = ("ai_reading_support_decision_2027.pdf", "ai_tool_evaluation_2027.xlsx", "reader_study_gains.png")


def is_bst(utc):
    return any(a <= utc < b for a, b in BST)


def to_utc(local):
    """A naive local (UK) datetime to naive UTC."""
    guess = local - dt.timedelta(hours=1)
    return guess if is_bst(guess) else local


def to_local(utc):
    return utc + dt.timedelta(hours=1) if is_bst(utc) else utc


def screening_days(first, last):
    d, out = first, []
    while d <= last:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out
