"""task171 constants and helpers shared by every generator module.

Corvane Therapeutics (fictional, Cambridge, Massachusetts) develops dovikizumab (CVN-2184), a humanised IgG1 antibody
against the p19 subunit of interleukin-23, for moderately to severely active ulcerative colitis. Study CVN2184-UC-201
randomised 720 patients 2 to 1 to dovikizumab 600 mg or placebo, IV at weeks 0, 4 and 8, stratified by prior biologic or
JAK inhibitor failure, at 71 sites in the United States, Canada, Poland and Hungary. The database locked on 14 July 2026;
the phase 3 dose goes into the end-of-phase-2 briefing package due on 4 December 2026, chosen under the dose-selection
charter: the lowest of 300, 600 and 900 mg whose forecast week-12 clinical remission rate is no more than 5 points below
the highest of the three forecasts."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

SEED = 1710527
WORLD_SEED = 2                  # the paper world sim_er4.py seed the margins were measured on
NA, NP = 480, 240
DOSES = (300, 600, 900)
THR = 5.0                       # charter: within 5 percentage points of the highest forecast
DIARY_WEEKS = ((6, 42), (8, 56), (10, 70))     # the e-diary timepoints: week, study day of the reference
STUDY = "CVN2184-UC-201"
LOCK = dt.date(2026, 7, 14)
TOPLINE = dt.date(2026, 6, 2)
DAY0 = dt.date(2024, 11, 4)     # first screening visit

# file names (the pack)
CONC = "cvn2184_201_serum_concentrations.csv"
RAND = "cvn2184_201_randomisation_log.csv"
BASE = "cvn2184_201_baseline_characteristics.csv"
DOSE = "cvn2184_201_infusion_records.csv"
EFF_LOCK = "cvn2184_201_efficacy_database_lock.csv"
EFF_TOP = "cvn2184_201_efficacy_topline_extract.csv"
DIARY = "cvn2184_201_ediary_entries.csv"
LAB = "cvn2184_201_central_laboratory.csv"
AE = "cvn2184_201_adverse_events.csv"
ADA = "cvn2184_201_ada_results.csv"
ADA_RUNS = "brightwater_ada_run_log.csv"
ENDO = "cvn2184_201_endoscopy_reads.csv"
CHARTER = "cvn2184_phase3_dose_selection_charter.pdf"
SAP = "cvn2184_201_statistical_analysis_plan_v2_section6.pdf"
IB = "dovikizumab_investigators_brochure_section5.pdf"
SITES = "cvn2184_201_site_list.csv"
VISITS = "cvn2184_201_visit_dates.csv"
DEVICES = "cvn2184_201_ediary_handset_log.csv"
CONMED = "cvn2184_201_concomitant_medications.csv"
PHASE1 = "cvn2184_hv101_pk_summary.xlsx"

# goldens
MEMO = "induction_dose_memo.docx"
TABLES = "phase2b_induction_tables.xlsx"
CHART = "exposure_response_chart.png"

COUNTRIES = (("US", 30), ("CA", 8), ("PL", 18), ("HU", 15))


def rng(*keys):
    h = hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def day_date(n):
    return DAY0 + dt.timedelta(days=int(n))


ZONE = {"Boston": "America/New_York", "Cleveland": "America/New_York", "Atlanta": "America/New_York",
        "Tampa": "America/New_York", "Houston": "America/Chicago", "Chicago": "America/Chicago",
        "Omaha": "America/Chicago", "Denver": "America/Denver", "Phoenix": "America/Phoenix",
        "Seattle": "America/Los_Angeles", "Toronto": "America/Toronto", "Montreal": "America/Toronto",
        "Hamilton": "America/Toronto", "Calgary": "America/Edmonton", "Warszawa": "Europe/Warsaw", "Krakow": "Europe/Warsaw",
        "Lodz": "Europe/Warsaw", "Wroclaw": "Europe/Warsaw", "Poznan": "Europe/Warsaw", "Gdansk": "Europe/Warsaw",
        "Budapest": "Europe/Budapest", "Debrecen": "Europe/Budapest", "Szeged": "Europe/Budapest", "Pecs": "Europe/Budapest",
        "Gyor": "Europe/Budapest"}


def local_to_utc(zone, local):
    """a naive local datetime at a site in time zone `zone` to naive UTC"""
    from zoneinfo import ZoneInfo
    return local.replace(tzinfo=ZoneInfo(zone)).astimezone(dt.timezone.utc).replace(tzinfo=None)


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    for r in rows:
        w.writerow([("" if r.get(c) is None else r.get(c)) for c in cols])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def call(fc, thr=THR):
    top = max(fc.values())
    return next(d for d in DOSES if fc[d] >= top - thr)


def r1(x):
    return float("%.1f" % (x + 0.0))
