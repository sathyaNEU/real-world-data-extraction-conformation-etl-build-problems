"""Write task270/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import common as K

SOURCES = {
    K.F_V3: "Brindholm and Wendholt NHS Foundation Trust digital services, mood app export (app version 3), "
            "prompts sent 5 January to 14 June 2026, pulled 6 January 2027",
    K.F_V4: "Brindholm and Wendholt NHS Foundation Trust digital services, mood app export (app version 4), "
            "prompts sent 15 June to 27 December 2026, pulled 6 January 2027",
    K.F_ENROL: "Brindholm and Wendholt NHS Foundation Trust digital services, mood app enrolment log, 2025 to 2026",
    K.F_REGISTER: "Brindholm and Wendholt NHS Foundation Trust psychological therapies team, assessment fortnights "
                  "register 2026",
    K.F_EPISODES: "Brindholm and Wendholt NHS Foundation Trust electronic patient record, community mental health team "
                  "care episodes, 2025 to 2026 (pulled 6 January 2027)",
    K.F_STANDARD: "Sallowdene Provider Collaborative, mood monitoring standard: emotional instability, version 1.1 "
                  "(12 October 2026)",
    K.F_PAPER: "Brindholm and Wendholt NHS Foundation Trust, Finance and Performance Committee paper, DBT skills groups "
               "in community mental health teams 2027-28 (21 January 2027)",
    K.F_ESR: "Brindholm and Wendholt NHS Foundation Trust workforce team, staff record extract of clinical assignments "
             "(4 January 2027)",
    K.F_LEARN: "Brindholm and Wendholt NHS Foundation Trust learning and development, learning records April 2022 to "
               "December 2026",
    K.F_CATALOGUE: "Brindholm and Wendholt NHS Foundation Trust learning and development, learning catalogue 2026",
    K.F_LDREPORT: "Brindholm and Wendholt NHS Foundation Trust learning and development, annual report 2024-25 "
                  "(27 June 2025)",
    K.F_DBTSTD: "Brindholm and Wendholt NHS Foundation Trust Complex Emotional Needs Service, DBT programme operating "
                "standard, version 3.1 (6 July 2026)",
    K.F_MODULE: "Brindholm and Wendholt NHS Foundation Trust electronic patient record, referral module export for the "
                "Complex Emotional Needs Service (8 January 2027)",
    K.F_LETTERS: "Brindholm and Wendholt NHS Foundation Trust electronic patient record, correspondence log for the "
                 "Complex Emotional Needs Service, April 2023 to January 2027 (8 January 2027)",
    K.F_INDEX: "Brindholm and Wendholt NHS Foundation Trust electronic patient record, patient index extract "
               "(6 January 2027)",
    K.F_PHQ: "Brindholm and Wendholt NHS Foundation Trust psychological therapies team, PHQ-9 and GAD-7 scores taken "
             "at assessment, 2026",
    K.F_PILOT: "Sallowdene Provider Collaborative digital mental health programme, mood app pilot evaluation "
               "(3 December 2025)",
}
DISTRACTORS = [K.F_PHQ, K.F_PILOT]
TITLE = ("Which of an English mental health trust's eleven community mental health teams get a 2027-28 DBT skills "
         "group, on each team's share of its 2026 assessed patients whose emotional instability reaches the "
         "collaborative's standard as the collaborative's three-hourly app will measure it")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(sum(1 for _ in ws.iter_rows(values_only=True)) - 1, 0) for ws in wb.worksheets)
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "role": "distractor" if f in DISTRACTORS else "input",
                    "source": "Constructed: " + SOURCES[f], "date": "2027-01-21",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task270",
        "title": TITLE,
        "domain": "Psychology & Behavioral Science",
        "client_domain": "Psychology & Behavioral Science",
        "subdomain": "experience-sampling-intensive-longitudinal-analysis (an English mental health trust's 2027-28 "
                     "DBT skills groups, each community team's share of its 2026 assessed patients with high "
                     "emotional instability as a provider collaborative's three-hourly mood app will measure it, read "
                     "from the trust's own mood app ratings)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "cuts of a distribution per segment: eleven teams, each with whether it gets a group, its "
                        "clinicians able to co-facilitate on 1 April 2027 and the mean weeks its patients on the DBT "
                        "waiting list had waited at the year end, and a chart of each team's share against the 30 per "
                        "cent line",
        "as_of": "2027-01-21",
        "deliverables": [K.X_GOLD, K.P_GOLD],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task270/generator/build.py (seeded, deterministic) around "
                               "a fictional English mental health trust, its eleven community mental health teams and "
                               "its Complex Emotional Needs Service, and a fictional provider collaborative, in the "
                               "layouts of a mood app's exports, a patient record's episodes, referral module and "
                               "index, a staff record extract, a learning system and the documents such an "
                               "organisation files; no real organisation's records or person is depicted.",
                     "date": "2027-01-21", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-27",
        "generator": "task270/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
