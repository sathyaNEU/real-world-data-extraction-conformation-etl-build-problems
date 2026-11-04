"""task401 metadata.json: every input file with its description, date, source and licence, and the distractors."""
import json
import os

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'Synthetic records generated for this task by its generator (no real council\'s, school\'s or pupil\'s data); CC0 1.0.'
D = {
    'pupil_roll_extract_2026-06-12.csv': ('SEEMiS extract: S1 to S3 pupils on the roll in session 2025-26', '2026-06-12'),
    'pupil_roll_2024-25.csv': ('SEEMiS extract: S1 to S3 pupils on the roll in session 2024-25 (older report layout)', '2025-06-20'),
    'june_common_paper_marks_2025.csv': ('June 2025 common paper item marks, one row per pupil', '2025-06-27'),
    'june_common_paper_marks_2026.csv': ('June 2026 common paper item marks, one row per pupil and question', '2026-06-12'),
    'common_paper_and_unit_map.xlsx': ('Common paper questions to topics and units under both course plans; Corvella skill codes', '2025-08-11'),
    'corvella_homework_export_2024-25.csv': ('Corvella homework platform export for session 2024-25', '2025-07-31'),
    'mathsbridge_homework_export_2025-26.parquet': ('Mathsbridge homework platform export for session 2025-26', '2026-06-12'),
    's1-s3_maths_change_register_2025-26.docx': ('Education Service change register for S1 to S3 mathematics, with the review remit', '2026-06-15'),
    'support_base_signins_2025-11-03_to_2026-05-29.csv': ('Support base kiosk sign-in export, all bases', '2026-06-01'),
    'support_base_guidance_2025-10.pdf': ('Support bases: guidance for school staff', '2025-10-20'),
    'bell_times_2025-26.xlsx': ('Bell times for the asymmetric week, by school', '2025-06-12'),
    'maths_timetable_2025-26.csv': ('Mathematics timetable export, S1 to S3 classes, autumn and spring', '2026-01-08'),
    'timetable_staff_codes_2025-26.xlsx': ('Timetable staff codes, autumn 2025 and spring 2026', '2026-01-08'),
    'maths_staffing_establishment_2025-26.xlsx': ('HR establishment: mathematics posts and their holders', '2026-01-12'),
    'attendance_by_month_2024-25_2025-26.csv': ('Monthly attendance by school and stage, both sessions', '2026-06-12'),
    'pupil_homework_survey_2025_2026.xlsx': ('Pupil homework survey results, 2025 and 2026', '2026-04-20'),
}
DISTRACTORS = [
    {'file': 'attendance_by_month_2024-25_2025-26.csv',
     'why': 'attendance reads as a cause of a fall in marks; it is level across the two sessions, belongs to no change in the '
            'register, and the review books the fall to the changes the register lists'},
    {'file': 'pupil_homework_survey_2025_2026.xlsx',
     'why': 'pupils rate Mathsbridge easier and say they complete more homework, which reads as the platform switch helping; '
            'the review counts June marks, and the survey measures neither marks nor what the homework revisited'},
]


def run():
    files = sorted(os.listdir(os.path.join(TASK, 'target')))
    assert set(files) == set(D), set(files) ^ set(D)
    out = dict(task='task401', organisation='Strathcorrie Council Education Service (invented)',
               files=[dict(file=f, description=D[f][0], date=D[f][1], source=SRC, license='CC0-1.0') for f in files],
               distractors=DISTRACTORS, wrong_basis_distractors=[],
               deliverables=['maths_change_review.docx', 'support_and_staffing_by_school.csv'])
    json.dump(out, open(os.path.join(TASK, 'metadata.json'), 'w'), indent=1)


if __name__ == '__main__':
    run()
