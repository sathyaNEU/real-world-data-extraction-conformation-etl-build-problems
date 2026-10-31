"""metadata.json: what the task decides, the deliverables, the distractors and each file's provenance. It names the
decision and never the method."""
import os

import pack as P

SOURCES = {
    "legacy": "Inspection system export, January 2019 to 1 March 2024 (the system replaced on 4 March 2024)",
    "current": "Inspection system export, 4 March 2024 to 31 December 2026",
    "permits": "Food establishment permit register, as of 31 December 2026",
    "roster": "Human Resources staff roster for the food safety program, December 2026, with separations since 2019",
    "plan": "Food Safety Program Plan 2027, issued 11 January 2027",
    "schedule": "Routine inspection schedule for 2027, issued with the plan",
    "fees": "Environmental health fee schedule 2026, as amended 1 July 2026",
    "capacity": "Return team capacity report for calendar 2026 with the officers' day sheet log",
    "complaints": "Complaint intake records, 4 March 2024 to 31 December 2026",
    "letters": "Outgoing correspondence log, 2026",
    "holidays": "Observed county holidays, 2025 to 2027",
    "illness": "Communicable disease team's foodborne illness investigations, 2019 to 2026",
    "invoices": "Annual permit fee invoices for 2026",
}


def metadata(target, counts):
    def rows_of(p):
        return (sum(1 for _ in open(p, encoding="utf-8")) - 1) if p.endswith(".csv") else None
    files = []
    for k, f in sorted(P.FILES.items(), key=lambda x: x[1]):
        pth = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(pth), "rows": rows_of(pth),
                      "source": "Constructed: " + SOURCES[k], "date": "2027-01-08" if k not in ("plan", "schedule")
                      else "2027-01-11", "license": "CC BY 4.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task130",
        "title": "Elkhorn County food safety program: a third return-inspection officer for 2027",
        "domain": "Psychology & Behavioral Science",
        "task_type": "decision-making and computational behavioral modeling",
        "objective": "Forecasting & Predictive Modeling",
        "decision": "whether the county adds a third return-inspection officer for 2027 under its program plan's "
                    "staffing rule, with the forecast the rule compares",
        "as_of": "2027-01-11",
        "deliverables": ["return_officer_memo_2027.pdf", "return_inspections_2027.xlsx"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task130/generator/make.py (seeded, deterministic) around a "
                               "fictional Washington county, its public health department, food establishments and "
                               "people; every record and figure is invented.",
                     "date": "2027-01-11", "license": "CC BY 4.0 (original work)"}],
        "files": files,
    }
