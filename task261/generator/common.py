"""task261 constants shared by every generator module.

Kelvane Life, a fictional Australian life insurer, sets its 2027 retirement range: one product per segment, each
segment a run of neighbouring age groups of the household's older partner, two neighbouring groups kept in separate
segments when their difference in median household net worth is more than 1.96 times its standard error. The evidence
is the 2025 wave of the fictional National Household Wealth Survey (stratified, two areas in each of 60 strata, five
implicates, 200 bootstrap replicate weights), released as a public-use file by the fictional Household Finance
Research Centre. The asks size Kelvane's own retirement income book by the same age groups."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2610523


def rng(label):
    """One random stream per label, fixed by the build seed."""
    h = hashlib.sha256(("%d/%s" % (SEED, label)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# ------------------------------------------------------------------ the age groups (the brief's six)
BANDS = [(0, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 120)]
BAND_NAMES = ["Under 35", "35 to 44", "45 to 54", "55 to 64", "65 to 74", "75 and over"]
BAND_SHORT = ["<35", "35-44", "45-54", "55-64", "65-74", "75+"]
OLDER = [3, 4, 5]                 # the asks' three groups from 55


def band_of(age):
    a = np.asarray(age)
    out = np.zeros(a.shape, int)
    for i, (lo, hi) in enumerate(BANDS):
        out[(a >= lo) & (a <= hi)] = i
    return out


# ------------------------------------------------------------------ the survey design
STRATA = 60
PSU_PER_STRATUM = 2
HH_PER_PSU = 50                 # about; each area's achieved interviews vary
REPLICATES = 200
IMPLICATES = 5
POPULATION_HOUSEHOLDS = 10_452_300    # the survey's benchmark: households in private dwellings, mid-2025
SCALE = 2.30                    # net worth level (Australian dollars) relative to the design study's units
DESIGN = dict(common_sd=0.95, specific_sd=(0.50, 0.50, 0.50, 0.31, 0.31, 0.50), idio_sd=1.20,
              share_area=(0.45, 0.75, 0.90, 1.00, 1.00, 0.95),
              couple_premium=(0.20, 0.24, 0.24, 0.26, 0.34, 0.48),
              log_median=(40, 132, 245, 345, 395, 350),       # thousands, before tuning and SCALE
              ref_younger_p=0.70, gap_mean=3.36, gap_sd=3.4, imputed_share=0.24, imputation_sd=0.45)
DESIGN_SEED = 312               # chosen by the design search (search2.py, refine.py): every rival route off the golden
# net worth factor per older-partner age group (the design's tuning, set against the ladder's margins)
TUNE = (0.9999, 0.9995, 1.0001, 1.078704, 1.140228, 1.17941)
IMPUTED_SHARE = (0.15, 0.55)    # the imputed items' share of an imputed household's net worth
OLDER_AREA = (0.0, 0.54)        # sd of the 65-74 and 75-and-over groups' own area effect on log net worth

# ------------------------------------------------------------------ dates
SURVEY_FIELD = (dt.date(2025, 3, 3), dt.date(2025, 10, 31))
RELEASE_DATE = dt.date(2026, 9, 14)            # the public-use release and the bulletin
AS_AT = dt.date(2026, 12, 31)                  # the asks' date
PULL = dt.date(2027, 1, 12)                    # the client register and the annuity listing
BRIEF_DATE = dt.date(2027, 1, 13)
COMMITTEE = dt.date(2027, 1, 27)

# ------------------------------------------------------------------ the organisations and people
INSURER = "Kelvane Life"
INSURER_LEGAL = "Kelvane Life Limited"
TRUSTEE = "Kelvane Super Pty Ltd"
SURVEY = "National Household Wealth Survey"
CENTRE = "Household Finance Research Centre"
PEOPLE = dict(head="Tracey Zimmerman",      # head of retirement products
              chair="Ryan Ferrell",         # chair, retirement product committee
              actuary="Wendy Koch")         # senior actuary, valuations

# ------------------------------------------------------------------ files
SUMMARY = "nhws2025_household_summary.csv"
PERSONS = "nhws2025_persons.csv"
REPW = "nhws2025_replicate_weights.csv"
GUIDE = "nhws2025_user_guide.pdf"
BULLETIN = "nhws2025_results_bulletin.xlsx"
BRIEF = "retirement_range_2027_brief.docx"
CRM = "crm_clients_20270112.csv"
RIA = "ria_pension_accounts_20261231.csv"
NOMS = "ria_nominations_20261231.csv"
ANN = "lifetime_annuity_lives_20270112.csv"
DICT = "retirement_book_data_dictionary.xlsx"
PDS = "retirement_income_account_pds_2026.pdf"
FACTS = "lifetime_annuity_key_facts_2026.pdf"
RESEARCH = "retirement_customer_research_2026.pdf"
DELIVERABLES = ("retirement_segments_2027.docx", "retirement_segments_2027.xlsx", "adjacent_differences_2027.svg")
