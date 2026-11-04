"""Build task210 end to end from the seed: the clean truth, the records, target/, metadata.json, the golden
deliverables, figures.json and target.zip. A rerun is byte-identical (verify with the printed digests).

    python3 task210/generator/build.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import world as W  # noqa: E402
import simulate as S  # noqa: E402
import records as RC  # noqa: E402
import pack  # noqa: E402
import golden as GD  # noqa: E402

SOURCES = {
    "edr": ("Ashcombe Regional Transit, event data recorder export", "streetcar fleet recorders, 1 April to 31 October 2026"),
    "avl": ("Ashcombe Regional Transit, AVL section-pass log", "streetcar revenue trips, 2026"),
    "survey": ("Ashcombe Regional Transit GIS, streetcar track survey", "2025 survey"),
    "metar": ("Ashcombe Municipal Airport AWOS", "hourly observations, 2026"),
    "yard": ("Ashcombe Regional Transit, rail yard block sheets", "daily, 2026"),
    "releases": ("Ashcombe Regional Transit, Foundry depot maintenance releases", "2026"),
    "runs": ("Ashcombe Regional Transit, dispatch run sheets", "daily, 2026"),
    "roster": ("Ashcombe Regional Transit, operator roster", "as of 31 October 2026"),
    "cards": ("Ashcombe Regional Transit, badge card register", "as of 31 October 2026"),
    "mms": ("Ashcombe Regional Transit, maintenance management system", "defect reports created 1 April to 2 November 2026"),
    "srm": ("Ashcombe Regional Transit, Safety Risk Management Procedure SRM-07", "revision 4, effective 1 October 2026"),
    "pick": ("Ashcombe Regional Transit, Scheduling Department", "January 2027 pick, issued 2 November 2026"),
    "normals": ("Ashcombe Municipal Airport climate normals", "1991 to 2020"),
    "dash": ("Ashcombe Regional Transit, Rail Operations dashboard", "monthly downloads, 2026"),
    "peds": ("Ashcombe Downtown Partnership, pedestrian counters", "hourly, 2026"),
    "arena": ("Ashcombe Arena, event calendar with scans", "2026"),
    "track": ("Ashcombe Regional Transit, track maintenance log", "2026"),
    "school": ("Ashcombe School District, 2026-27 calendar", "August 2026 to June 2027"),
}


def metadata():
    files = []
    for k, name in pack.FILES.items():
        src, cover = SOURCES[k]
        files.append({"file": name, "source": src, "coverage": cover, "date": "2026-11-02",
                      "license": "CC BY 4.0 (synthetic records generated for this task; no real agency's data)"})
    meta = {"task": "task210", "objective": "Anomaly Detection & Diagnostics", "domain": "Human Factors & Ergonomics",
            "task_type": "safety-incident-error-analysis", "files": files,
            "distractors": [pack.FILES[k] for k in pack.DISTRACTORS],
            "distractor_note": "relevant enough to weigh (pedestrian volumes, arena crowds, track work, the school "
                               "calendar), unused by the golden solution",
            "generated": "2026-11-02", "seed": W.SEED}
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")


def digest(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def main():
    T = S.simulate(seed=W.SEED)
    Rr = RC.records(T, W.SEED)
    pack.build(W.SEED, T, Rr)
    fig, r, obs, G = GD.compute()
    GD.write_golden(r, obs, G, fig["ask_a"], fig["ask_b"])
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    metadata()
    z = pack.cut_zip()
    for p in (z, os.path.join(TASK, "golden", "slot_plan_jan_feb_2027.csv"), os.path.join(TASK, "golden", "braking_shift.png"),
              os.path.join(HERE, "figures.json")):
        print(digest(p), os.path.relpath(p, TASK))


if __name__ == "__main__":
    main()
