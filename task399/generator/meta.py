"""metadata.json: what the task is about, the deliverables, the distractors and every file's provenance. It names
the decision and never the method."""
import pack as PK

LICENCE = "CC0 1.0 (synthetic, generated for this task)"


def metadata():
    files = {
        PK.PATHS["log"]: "Route-setting action log of both servers, 1 October 2025 to 30 September 2026.",
        PK.PATHS["reg25"]: "Incident register, 2025-26 financial year.",
        PK.PATHS["reg26"]: "Incident register, 2026-27 financial year to date, from the new incident tool.",
        PK.PATHS["delay"]: "Delay records attributed to the operating centre, April 2025 to September 2026.",
        PK.PATHS["reviews"]: "Delay attribution review decisions moving minutes between incidents.",
        PK.PATHS["layout"]: "Workstation display configuration export, release 8.2.1.",
        PK.PATHS["ros25"]: "Published signalling rosters, periods 7 to 13 of 2025-26.",
        PK.PATHS["ros26"]: "Published signalling rosters, periods 1 to 7 of 2026-27, new rostering tool.",
        PK.PATHS["changes"]: "Roster changes agreed on the day (swaps, sickness cover, rest day working).",
        PK.PATHS["comp"]: "Competence records of the signalling staff.",
        PK.PATHS["ars"]: "ARS sub-area status log export, both control servers.",
        PK.PATHS["adhesion"]: "Railhead adhesion reports, autumn 2025.",
        PK.PATHS["tor"]: "Safety Review Panel terms of reference for the 2027 operating improvement plan.",
        PK.PATHS["catalogue"]: "Operating centre improvement catalogue 2027.",
        PK.PATHS["workload"]: "Consultant's signaller workload assessment, March 2025.",
    }
    dated = {PK.PATHS["log"]: "2026-10-02", PK.PATHS["reg25"]: "2026-04-08", PK.PATHS["reg26"]: "2026-10-07",
             PK.PATHS["delay"]: "2026-10-06", PK.PATHS["reviews"]: "2026-10-06", PK.PATHS["layout"]: "2026-10-02",
             PK.PATHS["ros25"]: "2026-02-27", PK.PATHS["ros26"]: "2026-09-09", PK.PATHS["changes"]: "2026-10-05",
             PK.PATHS["comp"]: "2026-08-28", PK.PATHS["ars"]: "2026-10-02", PK.PATHS["adhesion"]: "2025-12-22",
             PK.PATHS["tor"]: "2026-09-03", PK.PATHS["catalogue"]: "2026-07-30", PK.PATHS["workload"]: "2025-03-28"}
    return {
        "task": "task399",
        "decision": "Which programme in the Fenmoor Rail Operating Centre improvement catalogue the route's 2027 "
                    "operating improvement plan funds, and the operating centre's delay minutes its cause produced "
                    "in the twelve months to 30 September 2026.",
        "deliverables": ["improvement_plan_case_2027.pptx", "staffing_and_ars_2025-26.xlsx"],
        "objective": "Root-Cause Analysis",
        "domain": "Human Factors & Ergonomics",
        "as_of": "2026-10-09",
        "distractor_files": [PK.PATHS["workload"], PK.PATHS["adhesion"]],
        "files": [dict(path=p, source="Synthetic, Wyvern Route operating records as exported", dated=dated[p],
                       licence=LICENCE, covers=desc) for p, desc in files.items()],
    }
