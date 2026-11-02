"""Builds task449 twice from the fixed seed, asserts the two builds byte-identical, and installs target/, golden/,
generator/figures.json, metadata.json, submission.md and target.zip.

    python3 task449/generator/build.py
"""
import datetime as dt
import filecmp
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np          # noqa: E402

import asks_world           # noqa: E402
import distractors          # noqa: E402
import docs                 # noqa: E402
import golden               # noqa: E402
import pack                 # noqa: E402
import params as P          # noqa: E402
import world as W           # noqa: E402
import writeup              # noqa: E402

TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
EXPORT_TIME = dt.datetime(2026, 11, 16, 9, 0, tzinfo=dt.timezone.utc).timestamp()
ZIP_TIME = (2026, 11, 16, 9, 0, 0)
AS_OF = "2026-11-16"

PRODUCERS = {   # each container's issuing body and its own date
    "qevs_2026q3_release_tables.xlsx": ("Provincial Statistics Bureau", "2026-11-06"),
    "in_demand_occupations_order_2027_program_guide.pdf": ("Department of Labour, Skills and Immigration", "2026-10-20"),
    "workshore_job_board_terms_for_employers_2026.pdf": ("Workshore", "2026-01-26"),
    "employer_services_vacancy_cases.xlsx": ("Workshore Employer Services", "2026-11-14"),
    "workshore_referrals_2025-04-01_2026-02-01.xlsx": ("Workshore", "2026-02-01"),
    "roe_received_workshore_clients_2025-04-01_2026-11-14.xlsx": ("Service Canada", "2026-11-14"),
    "in_demand_2027_briefing.docx": ("Provincial Statistics Bureau", "2026-11-16"),
    "in_demand_2027_tables.xlsx": ("Provincial Statistics Bureau", "2026-11-16"),
}

CONTENT = {
    "employer_services_vacancy_cases.xlsx": "Workshore Employer Services' vacancy case workbook, cases open from 1 April 2025, run 14 November 2026",
    "in_demand_occupations_order_2027_program_guide.pdf": "the order's program guide with Schedule A (Department of Labour, Skills and Immigration, 20 October 2026)",
    "noc_2016_v1.3_to_noc_2021_v1.0.csv": "NOC 2016 version 1.3 to NOC 2021 version 1.0 concordance for the unit groups on the board",
    "qevs_2026q3_release_tables.xlsx": "the Quarterly Employer Vacancy Survey's third quarter 2026 release tables",
    "workshore_board_events_2025-10-01_2026-02-01.csv": "the old job board platform's posting activity log, 1 October 2025 to 1 February 2026",
    "workshore_board_events_2026-02-02_2026-11-14.jsonl": "the new job board platform's posting activity log, 2 February to 14 November 2026",
    "workshore_employer_accounts.csv": "Workshore employer accounts register",
    "workshore_job_board_terms_for_employers_2026.pdf": "the job board's terms for employers, effective 2 February 2026",
    "workshore_live_postings_2025-07_2026-01.csv": "month-end snapshots of postings live on the old platform, July 2025 to January 2026",
    "workshore_live_postings_2026-02_2026-09.csv": "month-end extracts of postings live on the new platform, February to September 2026",
    "workshore_registered_jobseekers_schedule_a.csv": "registered jobseekers by primary sought occupation, Schedule A, month ends July 2025 to September 2026",
    "workshore_referrals_2025-04-01_2026-02-01.xlsx": "the old platform's Employer Services referral log at its close",
    "workshore_referrals_2026-02-02_2026-11-14.csv": "the new platform's Employer Services referral log",
    "workshore_client_job_reports_2025-04_2026-11.jsonl": "Workshore clients' job start and end reports, consultant and portal",
    "roe_received_workshore_clients_2025-04-01_2026-11-14.xlsx": "Records of Employment received for Workshore clients under the provincial data share",
    "lfs_employment_by_occupation_laurentide_quarterly.csv": "Labour Force Survey employment by broad occupational category, Laurentide, quarterly",
    "online_job_postings_index_laurentide_2025-2026.csv": "an aggregator's index of online job postings by broad occupational category, monthly",
}

DISTRACTORS = {
    "target/lfs_employment_by_occupation_laurentide_quarterly.csv":
        "employment by broad occupational category (one digit of NOC 2021), not by unit group, and neither vacancies "
        "nor registered jobseekers: the order's test uses neither employment nor a vacancy rate",
    "target/online_job_postings_index_laurentide_2025-2026.csv":
        "an index of online postings across many job sites, seasonally adjusted and by broad category: postings "
        "advertised, not positions unfilled on the reference dates, and with no level to share the survey's totals by",
}


def scrub(d):
    sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts"))
    import scrub_producer_metadata as S
    for fn in sorted(os.listdir(d)):
        if fn in PRODUCERS:
            prod, stamp = PRODUCERS[fn]
            f = S.scrub_pdf if fn.endswith(".pdf") else S.scrub_ooxml
            f(os.path.join(d, fn), prod, stamp, floor="2023-01-01", ceiling=AS_OF)


def write_pack(tgt):
    os.makedirs(tgt, exist_ok=True)
    emps, vac = W.simulate(np.random.default_rng(P.SEED))
    posts, cases = pack.write_main(emps, vac, tgt, np.random.default_rng(P.SEED + 11))
    js = pack.jobseeker_counts(np.random.default_rng(P.SEED + 21))
    pack.write_jobseekers(js, np.random.default_rng(P.SEED + 22), tgt)
    docs.write_survey_release(vac, np.random.default_rng(P.SEED + 31), emps, tgt)
    docs.write_program_guide(tgt)
    docs.write_employer_terms(tgt)
    asks_world.write_asks(emps, posts, cases, tgt, P.SEED + 41)
    distractors.write_distractors(tgt, P.SEED + 51)


def one_build(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    write_pack(tgt)
    scrub(tgt)
    res = golden.write_golden(tgt, gld)
    scrub(gld)
    for d in (tgt, gld):
        for fn in os.listdir(d):
            os.utime(os.path.join(d, fn), (EXPORT_TIME, EXPORT_TIME))
    return res


def same_tree(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    assert fa == fb, (fa, fb)
    for fn in fa:
        assert filecmp.cmp(os.path.join(a, fn), os.path.join(b, fn), shallow=False), "differs: %s" % fn
    return len(fa)


def metadata(files):
    out = {
        "task": "task449",
        "title": "Laurentide's In-Demand Occupations Order, 2027: the Schedule A occupations that meet the test",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "Survey Research & Official Statistics",
        "decision": "which Schedule A occupations the Bureau certifies for the 2027 In-Demand Occupations Order, with "
                    "the Employer Services referral figures for the Minister's briefing",
        "deliverables": ["in_demand_2027_briefing.docx", "in_demand_2027_tables.xlsx"],
        "distractor_files": sorted(DISTRACTORS),
        "distractor_reasons": DISTRACTORS,
        "as_of": AS_OF,
        "files": [],
    }
    for fn in sorted(files):
        out["files"].append({"path": "target/" + fn, "content": CONTENT[fn],
                             "source": "synthetic: constructed by the task generator (fixed seed) in the layout of the "
                                       "named system's export; no real person, employer or agency is depicted",
                             "date": AS_OF, "licence": "CC0 1.0 (constructed for this task)"})
    return out


def make_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, fn), "rb") as f:
                z.writestr(zi, f.read())


def main():
    tmp = tempfile.mkdtemp(prefix="t449_")
    try:
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        os.makedirs(a)
        os.makedirs(b)
        one_build(a)
        one_build(b)
        n1 = same_tree(os.path.join(a, "target"), os.path.join(b, "target"))
        n2 = same_tree(os.path.join(a, "golden"), os.path.join(b, "golden"))
        print("two builds byte-identical: %d target files, %d golden files" % (n1, n2))
        for d in ("target", "golden"):
            dst = os.path.join(TASK, d)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(os.path.join(a, d), dst)
            for fn in os.listdir(dst):
                os.utime(os.path.join(dst, fn), (EXPORT_TIME, EXPORT_TIME))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tgt = os.path.join(TASK, "target")
    res = golden.compute(tgt)
    figs = golden.figures(res, tgt)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(os.listdir(tgt)), f, indent=1)
    writeup.write(figs, os.path.join(TASK, "submission.md"))
    make_zip(tgt, os.path.join(TASK, "target.zip"))
    print("target.zip md5", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    print(json.dumps(figs, sort_keys=True))


if __name__ == "__main__":
    main()
