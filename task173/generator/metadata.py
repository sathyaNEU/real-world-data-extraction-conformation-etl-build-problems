"""Write task173/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import acd as A
import docs as DOC
import records as RC

ORG = "Ashdale Software Inc."
HCS = "Hillsborough Contact Services Ltd."
SOURCES = {
    RC.F_CRM: ORG + " Ashdale Tax Live CRM, expert interaction export for the 2026 filing season, both queues (UTC)",
    RC.F_ROSTER: ORG + " Workforce Planning, seasonal expert roster with the 2027 recall answers, and the outsourcer's "
                       "2026 agents",
    RC.F_HISTORY: ORG + " Human Resources, seasonal expert history 2021 to 2026 with the old ticketing agent codes",
    RC.F_OLD_A: ORG + " old ticketing system, weekly agent report, 2021 and 2022 seasons",
    RC.F_OLD_B: ORG + " old ticketing system, weekly agent report, 2023 to 2025 seasons (new layout)",
    RC.F_DEMAND: ORG + " Demand Planning, 2027 daily forecast of new expert cases for the English queue, with its basis",
    A.F_USERS: ORG + " contact centre systems, ACD user list exported 29 October 2026",
    A.F_STATES: ORG + " contact centre systems, ACD agent state detail for the HCS team, 13 April to 3 May 2026 (UTC)",
    A.F_CONTACTS: ORG + " contact centre systems, ACD contact detail for the English expert queue, 20 April to 3 May "
                        "2026 (UTC)",
    A.F_ONBOARD: HCS + " agent onboarding list for the Ashdale Tax Live program, 8 April 2026",
    "csat_survey_responses_2026.csv": ORG + " customer experience, post-contact survey responses, 2026 season",
    "finance_live_returns_weekly.csv": ORG + " Finance, weekly returns filed by Ashdale Tax Live customers, 2021 to "
                                             "2026 seasons",
    DOC.F_STANDARD: ORG + " Workforce Planning, expert capacity planning standard version 3.2 (14 September 2026)",
    DOC.F_SCHEDULE_B: HCS + " and " + ORG + ", master services agreement Schedule B as amended 2 March 2026",
    DOC.F_CALENDAR: ORG + " Ashdale Tax Live training centre, 2027 expert training calendar (26 October 2026)",
    DOC.F_INVOICES: HCS + ", invoices for the 2026 deadline period, 20 April to 19 May 2026",
    DOC.F_GUIDE: ORG + " contact centre systems, ACD reports field guide version 2.0 (9 March 2026)",
    DOC.F_CRM_NOTES: ORG + " CRM administrator's notes on the 29 October 2026 interaction export",
    DOC.F_THREAD: ORG + " email thread on the 2027 deadline booking, 26 to 29 October 2026",
    DOC.F_MANIFEST: ORG + " Workforce Planning, manifest of the files pulled for the 2027 deadline booking",
}
DISTRACTORS = ["csat_survey_responses_2026.csv", "finance_live_returns_weekly.csv"]
TITLE = ("How many agent hours a tax-software company's live expert service books with its outsourcer for the 2027 "
         "deadline fortnight, when only half of last season's experienced bench returns and four new classes fill the "
         "rest, and whether a customer's case comes back depends on who took its first contact")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-30",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task173",
        "title": TITLE,
        "domain": "Business & Operations Analytics",
        "client_domain": "General Statistics & Data Science",
        "house_domain": "business-operations-analytics",
        "subdomain": "workforce and labour planning (a contact centre's deadline-period outsourcing booking, sized by "
                     "a classification model of each case's follow-up on who took its first contact, diagnosed against "
                     "the contact-level alternative and back-tested on earlier seasons)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed booking in whole blocks of 1,000 agent hours, the outsourcer's billable hours by "
                        "day and its unsupported invoiced hours by invoice week for the 2026 deadline fortnight, and "
                        "the English queue's average wait by day and share answered within three minutes by week",
        "as_of": "2026-10-30",
        "deliverables": ["deadline_fortnight_plan_2027.xlsx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {
            "files": len(out),
            "formats": sorted({x["format"] for x in out}),
            "largest_file": big["path"],
            "largest_file_rows": big["rows"],
        },
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task173/generator/build.py (seeded, deterministic) around a "
                      "fictional Canadian tax-software company's live expert service and a fictional Moncton contact "
                      "centre outsourcer, in the layouts of a CRM interaction export, an ACD's user list, agent state "
                      "and contact detail reports, an old ticketing system's weekly agent reports, an HR history, a "
                      "workforce roster, a demand plan, an outsourcer's onboarding list and invoices, a services "
                      "agreement schedule, a training calendar and a planning standard; no real organisation's records "
                      "or person is depicted.",
            "date": "2026-10-30",
            "license": "CC0-1.0 (original work)",
        }],
        "created": "2026-10-18",
        "generator": "task173/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta
