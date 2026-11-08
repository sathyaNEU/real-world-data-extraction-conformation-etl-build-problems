"""task482 architecture 17: builds the pack, the goldens, submission.md, metadata.json and figures.json twice (the
second time in a scratch folder), requires the two builds byte-identical, cuts target.zip deterministically and runs
checks.py, verify.py and ceiling.py."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B     # noqa: E402
import deliver as DL  # noqa: E402
import golden as G    # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMPS = {"y10sci_aug2026_responses.csv": (2026, 8, 24, 9, 12, 40),
          "y10sci_aug2026_sessions.csv": (2026, 8, 24, 9, 13, 2),
          "corlinn_item_bank_2026.xlsx": (2026, 9, 9, 10, 15, 22),
          "bank_calibration_runs.csv": (2026, 9, 7, 15, 48, 10),
          "item_renumbering_2025.csv": (2025, 2, 3, 11, 2, 44),
          "y10sci_2027_drafts.xlsx": (2026, 11, 3, 9, 5, 18),
          "y10sci_paper_specification_2027.pdf": (2026, 11, 4, 16, 40, 30),
          "standard_setting_record_y10sci.pdf": (2026, 3, 4, 9, 22, 6),
          "council_minute_2026_10_14.pdf": (2026, 10, 16, 11, 48, 50),
          "y10sci_course_review_2026.pdf": (2026, 9, 9, 8, 15, 12),
          "member_schools.csv": (2026, 8, 31, 14, 30, 0),
          "paper_choice_request.eml": (2026, 11, 6, 16, 42, 0),
          "entries_register_aug2026.xlsx": (2026, 8, 31, 11, 52, 36),
          "makeup_roster_aug2026.pdf": (2026, 8, 31, 9, 5, 40),
          "makeup_scripts_keyed.csv": (2026, 9, 10, 16, 20, 14),
          "candidate_survey_2026.csv": (2026, 8, 24, 10, 1, 8),
          "member_bell_times_2026.json": (2026, 8, 31, 14, 10, 2)}


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def one(target, golden, extra, figs):
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    res = B.build(target)
    G.write_figures(res, figs)
    DL.write_all(res, golden)
    WU.submission(res, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"))
    return (digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read(),
            open(figs, "rb").read())


def main():
    t1 = one(TARGET, GOLDEN, TASK, os.path.join(HERE, "figures.json"))
    with tempfile.TemporaryDirectory() as tmp:
        t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp, os.path.join(tmp, "figures.json"))
    same = [a == b for a, b in zip(t1, t2)]
    print("byte-identical rebuild: target %s, golden %s, submission %s, figures %s" % tuple(same))
    if not all(same):
        return 1
    assert sorted(STAMPS) == sorted(os.listdir(TARGET)), sorted(set(STAMPS) ^ set(os.listdir(TARGET)))
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMPS[f])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    rc = 0
    for s in ("checks.py", "verify.py", "ceiling.py"):
        rc |= subprocess.call([sys.executable, os.path.join(HERE, s)])
    return rc


if __name__ == "__main__":
    sys.exit(main())
