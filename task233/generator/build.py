"""Write the task233 pack into a target folder and return the clean truth for the checks."""
import os

import numpy as np

import docs
import params as P
import records as RC
import sim

FILES = {
    "frame26": "leaver_destinations_frame_2026.csv",
    "final25": "leaver_destinations_final_2025.csv",
    "fu": "nonresponse_followup_2025_outcomes.csv",
    "xw": "followup_case_crosswalk_2025.csv",
    "reg": "school_register.xlsx",
    "codes": "activity_codes.csv",
    "points": "state_exam_points_2026.csv",
    "qs4": "QS-4_quality_flags_standard.pdf",
    "meth": "leaver_destinations_methodology_2026.pdf",
    "furep": "nonresponse_followup_2025_report.pdf",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
    "lfs": "lfs_youth_neet_by_region_2025.csv",
    "rel25": "destinations_release_2025_tables.xlsx",
    "careers": "careers_service_contacts_2026.csv",
}
DISTRACTORS = ["lfs", "rel25", "careers"]

DICTIONARY = """# Data dictionary

Social Survey Unit, Leaver Destinations Survey. Files supplied for the Department of Education's 2026 release.
Times are UTC. Allocation shares are fractions of one leaver; rates are percentages.

## leaver_destinations_frame_2026.csv
One row per leaver on the 2026 frame, extracted on 10 November 2026 after the allocation run of 9 November.

| Column | Meaning |
|---|---|
| leaver_ref | leaver reference on the 2026 frame |
| school_code | school the leaver left (school_register.xlsx) |
| sex | F or M, from the school's leaver return |
| attainment_band | AB1 to AB4, as supplied with the school's September leaver return |
| return_form | LDS-1 (paper) or LDS-2 (online) for a returned form; blank when no form was returned by the close |
| form_build | build of the online form the return was made on (online returns only) |
| returned_at | time the return was written to the frame |
| activity_code | activity recorded on the form, as captured (activity_codes.csv) |
| alloc_he, alloc_fe, alloc_app, alloc_emp, alloc_neet | the leaver's allocation to each destination (nonrespondents only; methodology section 4) |

## leaver_destinations_final_2025.csv
One row per leaver on the 2025 frame, final file of 31 March 2026. Columns as the 2026 frame, plus:

| Column | Meaning |
|---|---|
| destination | destination of a returned form after processing (HE, FE, APP, EMP, NEET) |
| alloc_* | the 2025 allocation of a leaver who never returned a form |

## nonresponse_followup_2025_outcomes.csv
One row per route by which a follow-up case was resolved (field report section 3); unresolved cases have one row
with outcome F99.

| Column | Meaning |
|---|---|
| case_no | field system case number |
| route | adviser visit, telephone, benefits record, college enrolment record or employer record |
| resolved_on | date the route resolved the case |
| outcome_code | F01 to F07, F99 (field report section 5) |

## followup_case_crosswalk_2025.csv

| Column | Meaning |
|---|---|
| case_no | field system case number |
| leaver_ref | the leaver's 2025 frame reference as the field system holds it |
| district_code | district the case was drawn in |
| drawn_on | date of the sample draw |

## activity_codes.csv
The processing reference list for the current editions of the forms (LDS-1 paper; LDS-2 online, 2026 edition): each
activity code and the destination it maps to.

## school_register.xlsx
Sheet Schools: each school's code, name and district on the 2025 and the 2026 map. Sheet Districts: district codes
and names.

## state_exam_points_2026.csv
One row per 2026 leaver: state examination points and the date the results were last issued (initial results
25 August 2026, revised results after appeals 20 October 2026).

## lfs_youth_neet_by_region_2025.csv
Labour Force Survey: NEET rate of people aged 16 to 24 by region and quarter of 2025, with the sample size.

## destinations_release_2025_tables.xlsx
The 2025 release's district table as published on 11 December 2025, on the 2025 district map.

## careers_service_contacts_2026.csv
The careers service's weekly contacts with school leavers by district, autumn 2026.
"""

README = """# Leaver Destinations Survey: files for the 2026 release

| File | What it is |
|---|---|
| leaver_destinations_frame_2026.csv | the 2026 frame after the allocation run: forms returned, activity codes, allocations |
| leaver_destinations_final_2025.csv | the 2025 final file: processed destinations and 2025 allocations |
| nonresponse_followup_2025_outcomes.csv | the 2025 follow-up's outcomes by case and route |
| followup_case_crosswalk_2025.csv | follow-up case numbers to 2025 leaver references |
| nonresponse_followup_2025_report.pdf | the follow-up's field report: design, completion, outcome codes |
| QS-4_quality_flags_standard.pdf | the quality standard for the district flags |
| leaver_destinations_methodology_2026.pdf | the survey methodology for 2026 |
| activity_codes.csv | activity code list for the current form editions |
| school_register.xlsx | schools and their districts on the 2025 and 2026 maps |
| state_exam_points_2026.csv | state examination points of the 2026 leavers |
| destinations_release_2025_tables.xlsx | the 2025 release's district table |
| lfs_youth_neet_by_region_2025.csv | Labour Force Survey youth NEET rates by region, 2025 |
| careers_service_contacts_2026.csv | careers service contacts with leavers, autumn 2026 |
| DATA_DICTIONARY.md | column definitions |
"""


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.World(); W.build()
    R = RC.Records(W)
    f26, t26 = R.frame(26)
    f25, t25 = R.frame(25)
    fo, xw, cases = R.followup(t25)
    reg = R.register()
    pts = R.points(t26)
    p = lambda k: os.path.join(target, FILES[k])
    f26.to_csv(p("frame26"), index=False, lineterminator="\n")
    f25.to_csv(p("final25"), index=False, lineterminator="\n")
    fo.to_csv(p("fu"), index=False, lineterminator="\n")
    xw.to_csv(p("xw"), index=False, lineterminator="\n")
    RC.code_list().to_csv(p("codes"), index=False, lineterminator="\n")
    pts.to_csv(p("points"), index=False, lineterminator="\n")
    R.lfs().to_csv(p("lfs"), index=False, lineterminator="\n")
    R.careers_contacts().to_csv(p("careers"), index=False, lineterminator="\n")
    docs.register(p("reg"), reg)
    docs.release_tables(p("rel25"), R.release_2025_tables(t25))
    docs.standard(p("qs4"))
    docs.methodology(p("meth"), dict(frame26=len(f26), schools=len(reg)))
    comp = []
    for d in P.TRACED:
        c = cases[cases["d25"] == d]
        comp.append(dict(name=P.NAME[d], code=P.CODE[d], drawn=len(c), resolved=int((c["kind"] != "unresolved").sum()),
                         unresolved=int((c["kind"] == "unresolved").sum())))
    comp.sort(key=lambda r: r["code"])
    docs.followup_report(p("furep"), comp)
    with open(p("dict"), "w") as fh:
        fh.write(DICTIONARY)
    with open(p("readme"), "w") as fh:
        fh.write(README)
    return dict(W=W, t26=t26, t25=t25, cases=cases, reg=reg, comp=comp)
