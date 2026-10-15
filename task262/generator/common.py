"""Constants for task262: the Wrenmore Foundation's 2027 Opportunity Pathways region, the Provincial Research Data
Centre's census-linked intergenerational extract, and the foundation's 2019 to 2023 Bridges program records."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2620415


def rng(*keys):
    """One independent stream per named purpose, so a change in one part of the world moves no other part."""
    h = hashlib.sha256(("%d/" % SEED + "/".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# ---------------------------------------------------------------------------------------------- the world
FOUNDATION = "Wrenmore Foundation"
PROGRAM = "Opportunity Pathways"
OLD_PROGRAM = "Bridges"
CENTRE = "Provincial Research Data Centre"
PEOPLE = dict(director="Monique Webb", chair="Carl Mcclain", analyst="Lawrence Ferguson")

# region: 2001 census region code, the foundation's name for it, children in the extract (approximate), and the
# generating design (mean and spread of families' long-run log income in 2005 dollars, the slope of children's
# log earnings on it above and below a knee, the knee, and continuous filing as a logistic in the family's level)
REGIONS = [
    # code   name               n      mu     sd     bt     bb     knee    fa      fb     su
    ("4710", "Torvale Metro",   15400, 11.121, 0.834, 0.292, 0.665, -0.691, -0.224,  5.277, 0.383),
    ("4720", "Halverston",       6900, 11.117, 0.565, 0.352, 0.250, -0.679,  1.859,  1.661, 0.331),
    ("4730", "Kestry North",     4300, 10.747, 0.437, 0.336, 0.408, -0.871, -1.591, 12.000, 0.467),
    ("4740", "Selvane Valley",   6100, 10.450, 0.345, 0.258, 1.000, -0.200,  2.897, 10.000, 0.368),
    ("4750", "Danholt Lakes",    7800, 11.134, 0.446, 0.314, 0.534, -0.385,  0.168,  1.500, 0.346),
    ("4760", "Caskell Coast",    5600, 11.149, 0.422, 0.272, 0.259, -0.642, -0.425,  5.338, 0.393),
    ("4770", "Ostler Plains",    7200, 10.839, 0.571, 0.306, 0.250, -0.368,  2.644,  1.653, 0.428),
    ("4780", "Wendmoor",         5300, 11.128, 0.370, 0.306, 0.511, -0.844, -2.500,  9.574, 0.469),
]
# the stream each region's five tax years are drawn from
TAX_DRAW = {"4710": 2, "4730": 1060, "4740": 1, "4780": 6}
NAMES = [r[1] for r in REGIONS]
CODES = [r[0] for r in REGIONS]
SIGMA_E = 0.55          # children's long-run earnings around their parents' level
SIGMA_W = 0.28          # children's year-to-year earnings swing
COHORTS = (1984, 1985, 1986, 1987, 1988)
CENSUS_YEAR = 2000      # the 2001 census asked about income in 2000
TAX_YEARS = (2001, 2002, 2003, 2004, 2005)
EARN_YEARS = tuple(range(2014, 2023))
AGES = (30, 31, 32, 33, 34)

# consumer price index, 2005 = 100 (the data centre's table)
CPI = {2000: 89.7, 2001: 91.8, 2002: 93.8, 2003: 96.4, 2004: 98.2, 2005: 100.0, 2006: 102.0, 2007: 104.2, 2008: 106.6,
       2009: 106.9, 2010: 108.9, 2011: 112.0, 2012: 113.7, 2013: 114.7, 2014: 116.9, 2015: 118.2, 2016: 120.0,
       2017: 121.9, 2018: 124.7, 2019: 127.1, 2020: 128.0, 2021: 132.3, 2022: 141.6}

# ---------------------------------------------------------------------------------------------- dates
RELEASE = dt.date(2026, 6, 22)        # the data centre's release of the linked extract
BRIEF_DATE = dt.date(2026, 11, 6)     # the director's brief to the trustees
BOARD = dt.date(2026, 11, 26)         # the board meets
MIGRATION = dt.date(2021, 4, 6)       # Bridges moved case management systems
BRIDGES_START = dt.date(2019, 1, 7)
BRIDGES_END = dt.date(2023, 12, 31)

# ---------------------------------------------------------------------------------------------- files
COHORT = "linked_cohort_extract_2026.csv"
EARN = "child_earnings_2014_2022.csv"
HIST = "parent_income_history_2001_2005.csv"
RECODE = "region_recode_2001_2021.csv"
CPI_FILE = "consumer_price_index_2000_2022.csv"
GUIDE = "linked_extract_user_guide_2026.pdf"
DICT = "linked_extract_dictionary_2026.xlsx"
BRIEF = "opportunity_pathways_brief_2027.docx"
PART = "bridges_participants_2019_2023.csv"
LEDGER = "bridges_program_ledger_2019_2024.csv"
OFFICES = "bridges_offices.csv"
GUIDELINES = "bridges_program_guidelines_2019.pdf"
CLOSEOUT = "bridges_close_out_summary_2024.pdf"
INDICATORS = "regional_economic_indicators_2021.xlsx"
SURVEY = "youth_aspirations_survey_2023.pdf"
DELIVERABLES = ("opportunity_pathways_2027.pdf", "opportunity_pathways_2027.xlsx", "region_elasticities_2027.png")
