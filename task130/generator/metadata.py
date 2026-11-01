"""metadata.json: what the task decides, the deliverables, the distractors and each file's provenance. It names the
decision and never the method."""
import os

import pack as P

DISTRACTORS = ("nearmiss", "subs")
SOURCES = {
    "legacy": "Redbud EHS case log (legacy system), January 2021 to 31 May 2024, one row per case revision",
    "cases": "Redbud case management export, 1 June 2024 to 9 October 2026, with the cases migrated open",
    "assign": "HR crew and team assignment history, September 2020 to September 2026",
    "register": "Crew and technician team register as of 29 September 2026, with the March 2025 recodes",
    "hours": "Payroll timesheet hours by unit and biweekly pay period, 11 January 2021 to 27 September 2026",
    "payouts": "Payroll earnings lines under code CREW90 (HR-14 awards), pay dates January 2021 to 2 October 2026",
    "calendar": "Payroll calendar of biweekly pay periods, 2021 to 2027",
    "plan": "2027 work plan hours by district, unit type and quarter, from Pinewater's 2027 work release",
    "standard": "Pinewater EMC Contractor Safety Performance Standard CS-4, Revision 3 (effective 1 January 2026)",
    "programme": "Redbud HR-14 Crew Safety Recognition Programme, Revision 2 (effective 1 March 2021)",
    "notice": "Redbud notice of 2 October 2026 ending HR-14 on 31 December 2026",
    "nearmiss": "Field good-catch (near-miss) reports, January 2025 to September 2026",
    "subs": "Subcontractors' monthly safety returns, January to September 2026",
}
DATES = {"standard": "2025-12-08", "programme": "2021-02-24", "notice": "2026-10-02", "plan": "2026-10-15",
         "register": "2026-09-29", "cases": "2026-10-12"}


def metadata(target, counts):
    def rows_of(p):
        return (sum(1 for _ in open(p, encoding="utf-8")) - 1) if p.endswith(".csv") else None
    files = []
    for k, f in sorted(P.FILES.items(), key=lambda x: x[1]):
        pth = os.path.join(target, f)
        rows = rows_of(pth)
        if rows is None and k in ("cases", "register"):
            rows = counts.get(k)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(pth), "rows": rows,
                      "source": "Constructed: " + SOURCES[k], "date": DATES.get(k, "2026-10-16"),
                      "license": "CC BY 4.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task130",
        "title": "Redbud Line Services: 2027 recordable injuries on Pinewater work",
        "domain": "Economics & Econometrics",
        "task_type": "discrete choice and limited dependent variable modeling",
        "objective": "Forecasting & Predictive Modeling",
        "decision": "how many recordable injuries Redbud's field employees will record on Pinewater work in 2027, "
                    "and whether the rate they make on the 2027 work plan stays within CS-4's limit of 3.0",
        "as_of": "2026-10-16",
        "deliverables": ["safety_plan_recordables_2027.docx", "recordables_forecast_2027.xlsx",
                         "recordables_by_quarter_2027.png"],
        "distractor_files": [P.FILES[k] for k in DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task130/generator/make.py (seeded, deterministic) around a "
                               "fictional Georgia power line contractor, a fictional electric membership corporation "
                               "and fictional people; every record and figure is invented. Rate definitions follow "
                               "29 CFR 1904.",
                     "date": "2026-10-16", "license": "CC BY 4.0 (original work)"}],
        "files": files,
    }
