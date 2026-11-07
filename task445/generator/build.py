"""task445 architecture 3: build the pack, the goldens, figures.json, submission.md and metadata.json twice, require
byte-identical output, cut target.zip, then run the checks and the independent verifier.

    python3 task445/generator/build.py
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
import deliver as DL  # noqa: E402
import docs           # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMPS = {"p2_essay_marks_2026.csv": (2026, 11, 28, 5, 12, 44),
          "p2_section_a_scan_2026.csv": (2026, 11, 27, 23, 48, 10),
          "asc_history_entries_2026.xlsx": (2026, 11, 28, 5, 41, 2),
          "aeb_centres_register.csv": (2026, 10, 14, 1, 7, 36),
          "aeb_code_of_practice_2026.pdf": (2026, 3, 19, 14, 0, 0),
          "history_awarding_minute_2026.pdf": (2026, 11, 25, 15, 35, 0),
          "results_certification_2026-12-01.eml": (2026, 11, 30, 23, 48, 40),
          "post_results_reviews_2025.csv": (2026, 3, 2, 3, 22, 18),
          "teacher_predicted_grades_2026.csv": (2026, 9, 30, 6, 2, 50),
          "p2_question_statistics_2025.xlsx": (2025, 12, 3, 2, 5, 0),
          "aeb_markers_2026.csv": (2026, 10, 30, 0, 44, 12)}


def build_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    world = W.build()
    PK.write(target, world)
    docs.code_of_practice(os.path.join(target, PK.FILES["code"]))
    docs.awarding_minute(os.path.join(target, PK.FILES["minute"]))
    docs.request(os.path.join(target, PK.FILES["email"]))
    return world


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def one(target, golden, extra, here):
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    build_target(target)
    S, fig = DL.write_all(target, golden, here)
    WU.submission(fig, S, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"))
    return digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read(), \
        open(os.path.join(here, "figures.json"), "rb").read()


def main():
    t1 = one(TARGET, GOLDEN, TASK, HERE)
    with tempfile.TemporaryDirectory() as tmp:
        t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp, tmp)
    print("two builds byte-identical: target %s, golden %s, submission %s, figures %s" % tuple(
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
    if len(sys.argv) > 1 and sys.argv[1] == "--target-only":
        build_target(TARGET)
    else:
        main()
