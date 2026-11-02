"""metadata.json for the pack (provenance, licence, input gates, distractors)."""
import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LIC = "CC0 public domain dedication (original work, constructed for this task)"
DESC = {
    "pas_inpatient_episodes_2021_2026.csv": ("Constructed: finished consultant episodes of every provider spell with an episode in general surgery or gastroenterology at Marlstead General Hospital and Fennick Hospital, April 2021 to October 2026 (PAS and EPR extract)", "2026-11-01"),
    "fennick_pas_to_epr_number_map.csv": ("Constructed: Fennick Hospital PAS numbers and the Trust EPR hospital numbers given at the April 2023 migration", "2023-04-17"),
    "admitted_ptl_snapshots_2021_2026.parquet": ("Constructed: month-end snapshots of the general surgery admitted patient tracking list, both hospitals, April 2021 to October 2026", "2026-11-01"),
    "ers_referrals_general_surgery_2019_2026.csv": ("Constructed: e-Referral Service referrals received by the Trust's general surgery services", "2026-11-01"),
    "population_mid_year_estimates_2018_2025.xlsx": ("Constructed: mid-year population estimates, Marlstead and Coldvale districts, by sex and five-year age band", "2026-06-25"),
    "population_projections_2022_based.xlsx": ("Constructed: 2022-based subnational population projections, Marlstead and Coldvale districts, by sex and five-year age band", "2025-06-24"),
    "operational_plan_2027_28_activity_lines.pdf": ("Constructed: the Trust's 2027/28 operational plan activity line definitions, version 1.2", "2026-10-07"),
    "elective_capacity_plan_2027_28_general_surgery.pdf": ("Constructed: the Trust's 2027/28 elective capacity plan for general surgery, approved 22 October 2026", "2026-10-22"),
    "elective_access_policy_v6.pdf": ("Constructed: the Trust's elective access policy, version 6.0", "2025-06-26"),
    "ecds_abdominal_pain_attendances_2023_2026.csv": ("Constructed: emergency department attendances with abdominal pain, both hospitals, April 2023 to October 2026 (ECDS extract)", "2026-11-01"),
    "theatre_case_log_2024_2026.csv": ("Constructed: general surgery theatre case log, both hospitals, April 2024 to October 2026", "2026-11-01"),
}


def rows(path):
    if path.endswith(".csv"):
        return int(sum(1 for _ in open(path)) - 1)
    if path.endswith(".parquet"):
        return int(len(pd.read_parquet(path)))
    if path.endswith(".xlsx"):
        return int(sum(len(v) for v in pd.read_excel(path, sheet_name=None).values()))
    return None


def write():
    t = os.path.join(TASK, "target")
    files = []
    for f in sorted(os.listdir(t)):
        p = os.path.join(t, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows(p),
                      "source": DESC[f][0], "date": DESC[f][1], "license": LIC})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    m = {"task": "task173",
         "title": "The 2027/28 operational plan figure for emergency admissions with gallstone disease at a two-hospital NHS trust, with its general surgery waiting list baseline",
         "domain": "Healthcare Delivery & Health Economics", "client_domain": "Healthcare Delivery & Health Economics",
         "subdomain": "utilization-access-demand-forecasting", "objective": "Forecasting & Predictive Modeling",
         "prompt_shape": "the 2027/28 plan figure to the nearest 50 with its build, and the general surgery waiting list baseline at each 2025/26 quarter end by hospital (waits of 52 weeks or more from referral, hernia repairs waited for)",
         "as_of": "2026-10-31", "deliverables": ["gallstone_nel_plan_2027_28.xlsx", "rtt_baseline_general_surgery_2025_26.csv"],
         "distractor_files": ["ecds_abdominal_pain_attendances_2023_2026.csv", "theatre_case_log_2024_2026.csv"],
         "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}), "largest_file": big["path"], "largest_file_rows": big["rows"]},
         "sources": [{"files": "all files under target/", "origin": "constructed for this task by task173/generator/build.py (seeded, deterministic) around a fictional English acute trust, in the layouts of a PAS episode extract, a patient tracking list, an e-Referral Service extract, an ECDS extract, a theatre case log, population tables and the Trust's own PDF documents; the trust, hospitals, districts, people and numbers are constructed, and no real organisation's records or person is depicted.",
                      "date": "2026-11-01", "license": LIC}],
         "created": "2026-11-02", "generator": "task173/generator/build.py", "files": files}
    json.dump(m, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    return m


if __name__ == "__main__":
    m = write()
    print(m["input_gates"])
