"""The pack's data files from the simulated world: the census tables, the post-enumeration survey's person files, the
roll on census day and its electorates, the vital and border series by year of birth, the roll's transaction log, and
the 2018-base estimates the Office published for June 2024."""
import csv
import io

import numpy as np

import sim as S
from methods import LOG_COLS  # noqa: F401
import world as W

FILES = {
    "census": "census_2025_usual_residents_by_region.xlsx",
    "pes_people": "pes_2025_people.csv",
    "pes_records": "pes_2025_census_records.csv",
    "pes_meshblocks": "pes_2025_sampled_meshblocks.csv",
    "pes_report": "pes_2025_methods_report.pdf",
    "roll": "roll_at_close_of_census_day_2025.csv",
    "electorates": "electorates_and_regions.csv",
    "births": "live_births_by_sex_1925_2025.csv",
    "deaths_hist": "deaths_by_year_of_birth_1925_1990.xlsx",
    "deaths": "deaths_by_year_of_birth_1991_2025.csv",
    "movements": "long_term_movements_by_year_of_birth_1950_2025.csv",
    "series_notes": "vital_and_border_series_notes.pdf",
    "plan": "enrolment_campaign_plan_2027.docx",
    "spec": "enrolment_gap_file_specification.xlsx",
    "log": "roll_transactions_2025_2026.csv",
    "dictionary": "roll_extract_data_dictionary.xlsx",
    "migration": "roll_platform_migration_notes.pdf",
    "estimates_2024": "subnational_population_estimates_jun2024.csv",
    "field_ops": "census_2025_field_operations_summary.pdf",
}
DISTRACTORS = ["estimates_2024", "field_ops"]
PERIOD_2025 = "2025-01-01/2025-03-03"


def rng(seed, k):
    return np.random.default_rng(seed * 1000 + k)


def everything(seed=W.SEED):
    nat = S.national(seed)
    reg = S.regional(nat, seed)
    cov = S.coverage(seed)
    cnt = S.counts(reg, cov, seed)
    roll_counts = S.roll(reg, cov, seed)
    log, electors = S.roll_log(reg, roll_counts, seed)
    x = {"nat": nat, "reg": reg, "cov": cov, "cnt": cnt, "roll_counts": roll_counts, "log": log,
         "electors": electors, "seed": seed}
    x["ids"] = survey_ids(x)
    x["snapshot"] = snapshot_rows(x)
    return x


def write_csv(path, cols, rows, lineterminator="\r\n"):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator=lineterminator)
        w.writerow(cols)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


# ------------------------------------------------------------------ the post-enumeration survey

def meshblock_code(c, m):
    return "%02d%05d" % (int(c), m)


def survey_ids(x):
    """record numbers for the survey's people and the census records in its meshblocks; a matched person carries the
    number of the census record that counted them"""
    r = rng(x["seed"], 11)
    people, records = [], []
    used = set()

    def rec_no():
        while True:
            k = "C%09d" % int(r.integers(100000000, 999999999))
            if k not in used:
                used.add(k)
                return k
    pes_no = 100000
    for (c, mb, s, a, cls, inc, inp, pid) in x["cnt"]["p_sample"]:
        cr = rec_no() if inc else ""
        if inc:
            records.append((cr, meshblock_code(c, mb), c, s, a, "C"))
        if inp:
            pes_no += int(r.integers(1, 4))
            people.append(("P%07d" % pes_no, meshblock_code(c, mb), c, s, a, "M" if inc else "N", cr))
    for (c, mb, s, a, pid) in x["cnt"]["e_sample"]:
        status = r.choice(["D", "V", "O", "W"], p=[0.52, 0.17, 0.09, 0.22])
        if status == "O" and a > 1 and r.random() < 0.6:
            status = "D"
        records.append((rec_no(), meshblock_code(c, mb), c, s, a, str(status)))
    people.sort(key=lambda p: (p[1], p[0]))
    records.sort(key=lambda p: (p[1], p[0]))
    return {"people": people, "records": records}


PEOPLE_COLS = ["PES_PERSON", "MESHBLOCK", "REGION", "SEX", "AGE", "MATCH", "CENSUS_RECORD"]
RECORD_COLS = ["CENSUS_RECORD", "MESHBLOCK", "REGION", "SEX", "AGE", "STATUS"]
MB_COLS = ["MESHBLOCK", "REGION", "DWELLINGS_LISTED", "PEOPLE_LISTED", "VISITS_TO_COMPLETE"]


def meshblock_rows(x):
    r = rng(x["seed"], 12)
    listed = {}
    for p in x["ids"]["people"]:
        listed[p[1]] = listed.get(p[1], 0) + 1
    rows = []
    for c in W.CODES:
        for m in x["cnt"]["sampled_mb"][c]:
            code = meshblock_code(c, m)
            n = listed.get(code, 0)
            rows.append((code, c, max(1, int(round(n / r.uniform(2.3, 2.9)))), n, int(r.integers(1, 5))))
    return rows


# ------------------------------------------------------------------ the census tables

def census_table(x):
    """(region, sex, age) -> (counted including imputed, imputed)"""
    out = {}
    for (c, s, a), v in x["cnt"]["census"].items():
        out[(c, s, a)] = (v["correct"] + v["erroneous"] + v["imputed"], v["imputed"])
    return out


# ------------------------------------------------------------------ the roll on census day

AGE_BANDS = [(18, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69),
             (70, 74), (75, 120)]


def band_label(b):
    return "%d-%d" % b if b[1] < 120 else "%d+" % b[0]


def snapshot_rows(x):
    """electors at the close of census day by electorate, address type, sex and age band; overseas electors kept under
    the electorate of their last residential address"""
    r = rng(x["seed"], 13)
    rows = []
    by_region = {c: [e for e in W.ELECTORATES if e[2] == c] for c in W.CODES}
    for c in W.CODES:
        es = by_region[c]
        w = np.array([x["electors"][e[0]] for e in es], float)
        w = w / w.sum()
        for s in ("M", "F"):
            for b in AGE_BANDS:
                n = sum(x["roll_counts"][(c, s, a)] for a in range(b[0], min(b[1], 100) + 1))
                draw = r.multinomial(n, w)
                for e, k in zip(es, draw):
                    rows.append([e[0], e[1], "R", s, band_label(b), int(k)])
        for e in es:
            for s in ("M", "F"):
                for b in AGE_BANDS:
                    share = 0.0045 if b[0] < 30 else 0.0035 if b[0] < 50 else 0.0015
                    k = int(r.poisson(x["electors"][e[0]] * share / len(AGE_BANDS) * 6))
                    if k:
                        rows.append([e[0], e[1], "O", s, band_label(b), k])
    rows.sort(key=lambda q: (int(q[0]), q[2], q[3], AGE_BANDS.index(next(b for b in AGE_BANDS if band_label(b) == q[4]))))
    return rows


ROLL_COLS = ["ELECTORATE", "ELECTORATE_NAME", "ADDRESS_TYPE", "SEX", "AGE_GROUP", "ELECTORS"]
ELECTORATE_COLS = ["ELECTORATE", "ELECTORATE_NAME", "NAME_BEFORE_2024_REVIEW", "REGION", "REGION_NAME"]


def electorate_rows():
    return [(e[0], e[1], W.RENAMED.get(e[0], ""), e[2], W.NAME[e[2]]) for e in W.ELECTORATES]


# ------------------------------------------------------------------ vital and border series

BIRTH_COLS = ["PERIOD", "SEX", "LIVE_BIRTHS"]
DEATH_COLS = ["PERIOD", "SEX", "YEAR_OF_BIRTH", "DEATHS"]
MOVE_COLS = ["PERIOD", "SEX", "YEAR_OF_BIRTH", "ARRIVALS", "DEPARTURES"]


def period(y):
    return PERIOD_2025 if y == "2025Q" else str(y)


def birth_rows(x):
    rows = []
    for (y, s), n in sorted(x["nat"]["births"].items(), key=lambda kv: (kv[0][0] if kv[0][0] != "2025Q" else 2025.5, kv[0][1])):
        rows.append((period(y), s, int(n)))
    return rows


def _yk(y):
    return 2025.5 if y == "2025Q" else y


def death_rows(x, lo=1991):
    rows = []
    for (y, s, c), n in sorted(x["nat"]["deaths"].items(), key=lambda kv: (_yk(kv[0][0]), kv[0][1], kv[0][2])):
        if _yk(y) >= lo:
            rows.append((period(y), s, c, int(n)))
    return rows


def death_wide(x, hi=1990):
    """1925 to 1990: one row a year of death and sex, one column a year of birth"""
    cells = {}
    for (y, s, c), n in x["nat"]["deaths"].items():
        if y != "2025Q" and y <= hi:
            cells[(y, s, c)] = n
    return cells


def movement_rows(x, lo=1950):
    keys = set(k for k in x["nat"]["arrivals"]) | set(k for k in x["nat"]["departures"])
    rows = []
    for (y, s, c) in sorted(keys, key=lambda k: (_yk(k[0]), k[1], k[2])):
        if _yk(y) < lo:
            continue
        rows.append((period(y), s, c, int(x["nat"]["arrivals"].get((y, s, c), 0)),
                     int(x["nat"]["departures"].get((y, s, c), 0))))
    return rows


# ------------------------------------------------------------------ the roll's transaction log

def log_rows(x):
    return [r[:13] for r in x["log"]]


# ------------------------------------------------------------------ the 2018-base estimates at June 2024 (distractor)

EST_COLS = ["REGION", "REGION_NAME", "SEX", "AGE_GROUP", "ESTIMATED_RESIDENT_POPULATION"]
EST_GROUPS = [(0, 14), (15, 24), (25, 44), (45, 64), (65, 120)]


def estimate_rows(x):
    """the Office's 2018-base estimates for 30 June 2024: the census-day people rolled back eight months, the 2018
    census's coverage adjustment carried forward without any measure of the men both counts missed"""
    r = rng(x["seed"], 14)
    rows = []
    for c in W.CODES:
        for s in ("M", "F"):
            for g in EST_GROUPS:
                n = sum(int(x["reg"]["pop"][c][s][a]) for a in range(g[0], min(g[1], 100) + 1))
                if s == "M" and g[0] in (15, 25):
                    n -= int(sum(x["reg"]["unsettled"][c][a] for a in range(max(g[0], 18), min(g[1], 49) + 1)) * 0.27)
                n = int(round(n * r.uniform(0.982, 0.996) / 10.0)) * 10
                rows.append((c, W.NAME[c], s, "%d-%d" % g if g[1] < 120 else "%d+" % g[0], n))
    return rows
