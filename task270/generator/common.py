"""Constants shared by the task270 generator: the city, its police division and civil service commission, the four
2024 and 2025 entry examinations, the five components, the appointment rule, the academy classes, the costs' cost
centres and the shipped file names."""
import datetime as dt

CITY = "Kessling"
STATE = "Ohio"
DIVISION = "Kessling Division of Police"
COMMISSION = "Kessling Civil Service Commission"
ACADEMY = "Kessling Police Training Academy"
HR = "Department of Human Resources"
PEOPLE = {"analyst": "Melanie Howard", "secretary": "Julia Larson"}

# the five components every 2024 and 2025 candidate sat
COMPONENTS = ["written", "oral", "pat", "sjt", "inventory"]
LABEL = {"written": "Written test", "oral": "Oral board", "pat": "Physical ability test",
         "sjt": "Situational judgement test", "inventory": "Work style inventory"}
# minutes of testing per candidate (the cost rule shares cost centre 4410 by these)
MINUTES = {"written": 150, "oral": 30, "pat": 20, "sjt": 60, "inventory": 40}

# the appointment rule of the 2024 and 2025 examinations (the Commission's rules, 2023 edition)
WEIGHT = {"written": 0.60, "oral": 0.40}
VETERAN_POINTS = 5.0
PAT_LIMIT = 240          # seconds: the obstacle course, best of two attempts

# the four administrations: code, written test date, list certified, the academy classes the list fed
ADMIN = [
    dict(code="2024-1", name="Spring 2024", open=dt.date(2024, 1, 16), close=dt.date(2024, 2, 16),
         written=dt.date(2024, 3, 16), boards=(dt.date(2024, 4, 8), dt.date(2024, 4, 19)),
         pat=(dt.date(2024, 4, 27), dt.date(2024, 4, 28)), online=(dt.date(2024, 3, 18), dt.date(2024, 3, 29)),
         certified=dt.date(2024, 5, 14), classes=("24-2", "24-3"), fy=2024, posting="PO-24-0116"),
    dict(code="2024-2", name="Autumn 2024", open=dt.date(2024, 7, 15), close=dt.date(2024, 8, 16),
         written=dt.date(2024, 9, 21), boards=(dt.date(2024, 10, 7), dt.date(2024, 10, 18)),
         pat=(dt.date(2024, 10, 26), dt.date(2024, 10, 27)), online=(dt.date(2024, 9, 23), dt.date(2024, 10, 4)),
         certified=dt.date(2024, 11, 19), classes=("25-1", "25-2"), fy=2025, posting="PO-24-0715"),
    dict(code="2025-1", name="Spring 2025", open=dt.date(2025, 1, 21), close=dt.date(2025, 2, 21),
         written=dt.date(2025, 3, 15), boards=(dt.date(2025, 4, 7), dt.date(2025, 4, 18)),
         pat=(dt.date(2025, 4, 26), dt.date(2025, 4, 27)), online=(dt.date(2025, 3, 17), dt.date(2025, 3, 28)),
         certified=dt.date(2025, 5, 13), classes=("25-3", "25-4"), fy=2025, posting="PO-25-0121"),
    dict(code="2025-2", name="Autumn 2025", open=dt.date(2025, 7, 14), close=dt.date(2025, 8, 15),
         written=dt.date(2025, 9, 20), boards=(dt.date(2025, 10, 6), dt.date(2025, 10, 17)),
         pat=(dt.date(2025, 10, 25), dt.date(2025, 10, 26)), online=(dt.date(2025, 9, 22), dt.date(2025, 10, 3)),
         certified=dt.date(2025, 11, 18), classes=("26-1", "26-2"), fy=2026, posting="REQ-2025-0714"),
]
CLASS_START = {"24-2": dt.date(2024, 7, 8), "24-3": dt.date(2024, 9, 9), "25-1": dt.date(2025, 1, 6),
               "25-2": dt.date(2025, 3, 3), "25-3": dt.date(2025, 7, 7), "25-4": dt.date(2025, 9, 8),
               "26-1": dt.date(2026, 1, 5), "26-2": dt.date(2026, 3, 2)}
ACADEMY_WEEKS = 26

# the applicant tracking system moved from the old system to the new on this day (the spring 2025 window was open)
ATS_CUTOVER = dt.date(2025, 2, 3)

# cost centres on the extract
CC = {"4410": "Examinations - administration", "4411": "Examinations - written test",
      "4412": "Examinations - oral board", "4413": "Examinations - physical ability test",
      "4414": "Examinations - situational judgement trial", "4415": "Examinations - work style inventory trial"}
CC_OF = {"written": "4411", "oral": "4412", "pat": "4413", "sjt": "4414", "inventory": "4415"}

ASSEMBLED = dt.datetime(2026, 10, 6, 15, 12)       # the working pack, assembled for the Commission's November meeting
MEETING = dt.date(2026, 11, 12)

FILES = {
    "rules": "civil_service_rules_police_officer_exam_2023.pdf",
    "plan": "entry_exam_validation_trial_plan_2023.pdf",
    "roster": "eligibility_lists_police_officer_2024_2025.csv",
    "crosswalk": "candidate_numbers_crosswalk_2024_2025.csv",
    "written": "hss_written_examination_scores_2024_2025.csv",
    "oral": "oral_board_ratings_2024_2025.csv",
    "pat": "physical_ability_course_timing_2024_2025.csv",
    "sjt": "pellwyn_sjt_trial_scores_2024_2025.xlsx",
    "inventory": "hss_work_style_inventory_2024_2025.csv",
    "academy": "academy_gradebook_classes_24-2_to_26-2.xlsx",
    "handbook": "academy_recruit_handbook_2024.pdf",
    "ats_old": "applicant_tracking_export_legacy_2024-01_to_2025-02.csv",
    "ats_new": "applicant_tracking_export_2025-02_to_2025-09.csv",
    "ledger": "general_ledger_examinations_fy2024_fy2026.csv",
    "jobs": "police_officer_job_analysis_2022.pdf",
    "campaign": "recruitment_campaign_summary_2025.xlsx",
    "calendar": "police_officer_exam_calendar_2023_2026.csv",
    "contents": "entry_exam_working_pack_contents.txt",
}
