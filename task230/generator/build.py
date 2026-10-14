"""Write the pack under target/ from the simulated census."""
import csv
import os
from datetime import date, datetime

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import isco08
import params as P
import records as R
import sim
import world as W

FILES = dict(
    extract="census2026_occupation_coding_extract.parquet",
    study="census2026_coding_quality_study.csv",
    register="census2026_receipt_register.csv",
    visits="field_visit_log_jun_oct_2026.csv",
    aoc="aoc2026_occupation_classification.csv",
    eds="enumeration_districts_2026.csv",
    staff="coding_staff_register.csv",
    moves="coding_staff_movements_2026.csv",
    timesheets="coding_timesheets_21sep_01nov2026.csv",
    lfs="lfs_2026q3_employment_by_occupation.csv",
    c2021="census2021_occupation_by_region.csv",
    standard="OQ-4_occupation_output_quality_standard.docx",
    procedures="census2026_coding_procedures.pdf",
    manual="census2026_followup_field_manual.pdf",
    plan="census2026_processing_plan_nov2026.xlsx",
    dictionary="census2026_data_dictionary.xlsx",
    manifest="export_manifest.csv",
)
DISTRACTORS = ["lfs", "c2021"]


def _v(x):
    if x is None:
        return ""
    if isinstance(x, datetime):
        return x.strftime("%Y-%m-%d %H:%M")
    if isinstance(x, date):
        return x.isoformat()
    if isinstance(x, (float, np.floating)):
        return repr(float(x))
    return str(x)


def write_csv(path, header, cols):
    n = len(cols[0])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for i in range(n):
            w.writerow([_v(c[i]) for c in cols])
    return n


def run(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    S = sim.structure(seed)
    U = sim.uniforms(S)
    Cd = sim.coding(S, U)
    T = R.build_tables(S, U, Cd)
    counts = {}
    # the coding extract
    e = T["ext"]
    tab = pa.Table.from_arrays([
        pa.array(list(e["doc_id"]), pa.string()), pa.array(e["person_no"].astype(np.int8), pa.int8()),
        pa.array(list(e["load_batch"]), pa.string()), pa.array(e["coding_week"].astype(np.int16), pa.int16()),
        pa.array(list(e["autocoder_code"]), pa.string()), pa.array(e["autocoder_score"].astype(float), pa.float64()),
        pa.array(list(e["coding_path"]), pa.string()), pa.array(list(e["production_code"]), pa.string()),
        pa.array([c if c else None for c in e["coder_id"]], pa.string()),
        pa.array(list(e["coded_at"]), pa.timestamp("s"))],
        names=["doc_id", "person_no", "load_batch", "coding_week", "autocoder_code", "autocoder_score", "coding_path",
               "production_code", "coder_id", "coded_at"]).replace_schema_metadata(None)
    pq.write_table(tab, os.path.join(target, FILES["extract"]), compression="snappy", row_group_size=131072,
                   use_dictionary=True, write_statistics=True, store_schema=False)
    counts["extract"] = len(e["doc_id"])
    s = T["stu"]
    hdr = ["study_ref", "doc_id", "person_no", "load_batch", "batch_type", "coding_path", "selection_interval",
           "occupation_writein", "autocoder_code", "autocoder_score", "production_code", "reference_code", "reference_basis"]
    counts["study"] = write_csv(os.path.join(target, FILES["study"]), hdr,
                                [s[h] if h != "autocoder_score" else ["%.3f" % x for x in s[h]] for h in hdr])
    g = T["reg"]
    hdr = ["doc_id", "questionnaire_id", "address_id", "ed_code", "capture_mode", "received_date", "load_batch",
           "usual_residents", "in_employment", "occupation_writeins"]
    counts["register"] = write_csv(os.path.join(target, FILES["register"]), hdr, [g[h] for h in hdr])
    v = T["vis"]
    hdr = ["visit_id", "address_id", "ed_code", "staff_id", "visit_no", "visit_time", "outcome_code", "proxy_respondent",
           "questionnaire_id", "tablet_id", "synced_at"]
    counts["visits"] = write_csv(os.path.join(target, FILES["visits"]), hdr,
                                [v["device_id" if h == "tablet_id" else h] for h in hdr])
    # the classification
    rows = []
    sm = dict(isco08.sub_major())
    for u, t in isco08.units():
        nat = W.NATIONAL.get(u)
        for d, nt in (nat or [("0", t)]):
            rows.append((u + d, nt, u, t, u[:2], sm[u[:2]]))
    counts["aoc"] = write_csv(os.path.join(target, FILES["aoc"]),
                              ["aoc_code", "aoc_title", "isco08_unit_group", "isco08_unit_title", "isco08_sub_major",
                               "isco08_sub_major_title"], list(zip(*rows)))
    # enumeration districts
    reg = {c: n for c, n, _ in W.REGIONS}
    n_addr = np.bincount(S["a_ed"], minlength=len(S["ed_code"]))
    counts["eds"] = write_csv(os.path.join(target, FILES["eds"]), ["ed_code", "region_code", "region_name", "addresses_listed"],
                              [S["ed_code"], S["ed_region"], [reg[x] for x in S["ed_region"]], n_addr])
    st = T["staff"]
    hdr = ["staff_no", "coder_id", "team", "role", "contract", "status", "started", "left"]
    counts["staff"] = write_csv(os.path.join(target, FILES["staff"]), hdr, [[r[h] for r in st] for h in hdr])
    mv = T["moves"]
    hdr = ["staff_no", "coder_id", "movement", "team_from", "team_to", "effective_date"]
    counts["moves"] = write_csv(os.path.join(target, FILES["moves"]), hdr, [[r[h] for r in mv] for h in hdr])
    ts = T["ts"]
    hdr = ["staff_no", "work_date", "activity", "hours", "entered_on", "note"]
    counts["timesheets"] = write_csv(os.path.join(target, FILES["timesheets"]), hdr,
                                     [[("%.2f" % r[h]) if h == "hours" else r[h] for r in ts] for h in hdr])
    counts["lfs"] = distractor_lfs(os.path.join(target, FILES["lfs"]), S)
    counts["c2021"] = distractor_2021(os.path.join(target, FILES["c2021"]), S)
    facts = docs.write_all(target, FILES, S, T, Cd)
    counts.update(facts.get("counts", {}))
    write_manifest(os.path.join(target, FILES["manifest"]), counts)
    return S, U, Cd, T, counts, facts


def distractor_lfs(path, S):
    """the Labour Force Survey's third-quarter estimates of employment by sub-major group (thousands, with the
    coefficient of variation): the survey's own sample and weighting, not the census"""
    rng = np.random.default_rng(P.SEED + 61)
    tot = len(S["owner"]) * 1.031 / 1000.0
    deff = np.random.default_rng(P.SEED + 62)
    rows = []
    for g in W.GROUPS:
        est = tot * W.SHARE[g] / sum(W.SHARE.values()) * float(np.exp(rng.normal(0, 0.05)))
        # the design effect varies by group (clustering of an occupation within households and areas)
        cv = min(45.0, 100 * 0.9 / np.sqrt(max(est, 0.2) * 9) * float(np.exp(deff.normal(0, 0.22))))
        rows.append(("2026Q3", g, W.SUB[g], "%.1f" % est, "%.1f" % cv))
    return write_csv(path, ["quarter", "isco08_sub_major", "sub_major_title", "employed_thousands", "cv_percent"],
                     list(zip(*rows)))


def distractor_2021(path, S):
    """the 2021 census's published persons in employment by region and sub-major group"""
    rng = np.random.default_rng(P.SEED + 67)
    rows = []
    tot = len(S["owner"]) * 0.957
    for code, name, sh in W.REGIONS:
        for g in W.GROUPS:
            n = tot * sh * W.SHARE[g] / sum(W.SHARE.values()) * float(np.exp(rng.normal(0, 0.08)))
            rows.append((code, name, g, W.SUB[g], int(round(n))))
    return write_csv(path, ["region_code", "region_name", "isco08_sub_major", "sub_major_title", "persons_in_employment"],
                     list(zip(*rows)))


def write_manifest(path, counts):
    desc = [
        ("extract", "Coding system extract: every occupation write-in coded by Friday 13 November 2026, one row per person "
                    "write-in, with its autocoder suggestion and score, coding path, production code and the coder on the "
                    "clerical path", "Coding system (CODA)", "Census Processing"),
        ("study", "Coding quality study: the write-ins selected from each load batch and recoded by the classification "
                  "specialists, with the adjudicated reference code", "CODA study module", "Methodology Division"),
        ("register", "Receipt register: every census form received by the close of field operations, with its coding "
                     "document number and load batch", "Receipt and registration system", "Census Processing"),
        ("visits", "Field operations system visit log: every follow-up call recorded on an enumerator tablet, 22 June to 31 "
                   "October 2026, and the administrative closures", "Field operations system (FOS)", "Field Operations"),
        ("aoc", "Aldmere Occupational Classification 2026 with the ISCO-08 structure", "Classification management",
                "Methodology Division"),
        ("eds", "Enumeration districts and regions as at census day", "Address register", "Field Operations"),
        ("staff", "Coding staff register at 13 November 2026: everyone who has worked in census coding, with their team",
                  "HR and rostering", "Census Processing"),
        ("moves", "Coding staff movements since coding began on 4 May 2026: starters, transfers between teams and leavers",
                  "HR and rostering", "Census Processing"),
        ("timesheets", "Timesheet export for the pay fortnights from 21 September to 1 November 2026", "Timesheet system",
                       "Census Processing"),
        ("lfs", "Labour Force Survey, third quarter 2026: employment by ISCO-08 sub-major group", "LFS estimation system",
                "Labour Market Statistics"),
        ("c2021", "2021 Census of Population: persons in employment by region and ISCO-08 sub-major group (published)",
                  "Census 2021 dissemination tables", "Census Outputs"),
        ("standard", "Output quality standard OQ-4: occupation", "Quality management", "Methodology Division"),
        ("procedures", "Census 2026 coding procedures, version 3", "Census Processing", "Census Processing"),
        ("manual", "Census 2026 follow-up field manual (enumerators and field supervisors)", "Field Operations",
                   "Field Operations"),
        ("plan", "Census 2026 processing plan: coding capacity to the coding close, November 2026 update",
                 "Census Processing", "Census Processing"),
        ("dictionary", "Data dictionary for the extracts in this pack", "Census Processing", "Census Processing"),
    ]
    rows = []
    for k, d, src, own in desc:
        rows.append((FILES[k], d, counts.get(k, ""), src, own, "2026-11-13"))
    write_csv(path, ["file", "description", "rows", "source_system", "owner", "extracted"], list(zip(*rows)))
