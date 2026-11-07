"""task145 architecture 2: build the pack, the goldens, figures.json, submission.md and metadata.json; rebuild into a
scratch folder and require byte-identical output; cut target.zip; then run the checks and the independent verifier.

    python3 task145/generator/build.py
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as DC        # noqa: E402
import golden as GD      # noqa: E402
import pack as PK        # noqa: E402
import postprocess as PP  # noqa: E402
import writeup as WU     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMPS = {"enrollment_records_2023-24_to_2026-27.csv": (2026, 12, 21, 6, 12, 40),
          "attendance_absences_2023-24.csv": (2024, 7, 2, 10, 41, 8),
          "attendance_absences_2024-25_to_2026-27.csv": (2026, 12, 21, 6, 14, 2),
          "course_grades_2023-24_to_2026-27.csv": (2026, 12, 21, 6, 18, 55),
          "behavior_incidents_2023-24_to_2026-27.csv": (2026, 12, 21, 6, 16, 31),
          "registrar_records_requests_2023-2026.csv": (2026, 12, 18, 15, 2, 44),
          "instructional_calendars_2023-24_to_2026-27.xlsx": (2026, 8, 3, 9, 27, 10),
          "sis_code_reference.csv": (2026, 12, 21, 6, 20, 15),
          "board_policy_JF-7_bridge_program.pdf": (2025, 6, 12, 8, 30, 0),
          "attendance_regulation_JH-R_2026-27.pdf": (2026, 7, 28, 14, 5, 36),
          "bell_schedules_2026-27.pdf": (2026, 7, 21, 11, 40, 2),
          "pathwise_schedule_B_spring_2027.pdf": (2026, 12, 2, 16, 22, 48),
          "bridge_seats_for_spring.eml": (2026, 12, 21, 8, 42, 17),
          "family_texts_fall_2026.csv": (2026, 12, 19, 3, 0, 12),
          "transportation_routes_2026-27.csv": (2026, 8, 7, 13, 55, 30),
          "school_climate_survey_spring_2026.xlsx": (2026, 6, 15, 10, 8, 20)}


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def pack(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = PK.build(target)
    DC.write_all(W, target)
    p = lambda f: os.path.join(target, f)
    PP.normalize_ooxml(p("instructional_calendars_2023-24_to_2026-27.xlsx"), "Patricia Villarreal", "Patricia Villarreal",
                       "2023-06-19T15:02:11Z", "2026-08-03T15:27:10Z", excel=True, company=PP.COMPANY)
    PP.normalize_ooxml(p("school_climate_survey_spring_2026.xlsx"), "Panorama Export", "Angel Flores",
                       "2026-06-12T18:44:03Z", "2026-06-15T16:08:20Z", excel=True, company=PP.COMPANY)
    PP.normalize_pdf(p("board_policy_JF-7_bridge_program.pdf"), b"D:20240314190211-06'00'", b"D:20250612083000-06'00'")
    PP.normalize_pdf(p("attendance_regulation_JH-R_2026-27.pdf"), b"D:20260728140536-06'00'",
                     b"D:20260728140536-06'00'")
    PP.normalize_pdf(p("bell_schedules_2026-27.pdf"), b"D:20260721114002-06'00'", b"D:20260721114002-06'00'")
    PP.normalize_pdf(p("pathwise_schedule_B_spring_2027.pdf"), b"D:20261202162248-07'00'",
                     b"D:20261202162248-07'00'")
    return W


def one(target, golden, extra, figpath):
    pack(target)
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    fig, S = GD.write_all(target, golden, figpath)
    PP.normalize_ooxml(os.path.join(golden, "attendance_figures_2026.xlsx"), "Patricia Villarreal",
                       "Patricia Villarreal", "2026-12-21T17:05:40Z", "2026-12-22T00:18:09Z", excel=True,
                       company=PP.COMPANY)
    PP.normalize_pdf(os.path.join(golden, "bridge_2027_board_paper.pdf"), b"D:20261222101906-07'00'",
                     b"D:20261222154311-07'00'")
    WU.submission(fig, S, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"))
    return digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read(), \
        open(figpath, "rb").read()


def main():
    t1 = one(TARGET, GOLDEN, TASK, os.path.join(HERE, "figures.json"))
    with tempfile.TemporaryDirectory() as tmp:
        t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp, os.path.join(tmp, "figures.json"))
    print("byte-identical rebuild: target %s, golden %s, submission %s, figures %s" % tuple(
        a == b for a, b in zip(t1, t2)))
    if t1 != t2:
        sys.exit(1)
    assert sorted(STAMPS) == sorted(os.listdir(TARGET)), sorted(set(STAMPS) ^ set(os.listdir(TARGET)))
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMPS[f])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    sys.exit(rc)


if __name__ == "__main__":
    main()
