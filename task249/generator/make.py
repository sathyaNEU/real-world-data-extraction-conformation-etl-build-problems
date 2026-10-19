"""Build the task249 target, the goldens, the write-up, metadata and target.zip."""
import json
import os
import shutil
import sys
import zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build as B
import golden
import writeup


def zipdir(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(src)):
            info = zipfile.ZipInfo("target/" + f, date_time=(2029, 5, 14, 9, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(src, f), "rb") as fh:
                z.writestr(info, fh.read())


def main(target=os.path.join(TASK, "target")):
    if os.path.isdir(target):
        shutil.rmtree(target)
    B.run(target)
    L, G = writeup.figures(target, B.FILES)
    gd = os.path.join(TASK, "golden")
    if os.path.isdir(gd):
        shutil.rmtree(gd)
    os.makedirs(gd)
    golden.workbook(os.path.join(gd, B.FILES["deliv_xlsx"]), G)
    golden.note(os.path.join(gd, B.FILES["deliv_pdf"]), G)
    writeup.write_figures(os.path.join(HERE, "figures.json"), G)
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(writeup.submission(G))
    metadata(target)
    zipdir(target, os.path.join(TASK, "target.zip"))
    return L, G


def metadata(target):
    import pandas as pd
    files = sorted(os.listdir(target))
    rows = len(pd.read_parquet(os.path.join(target, B.FILES["exposure"]), columns=["item_id"]))
    m = {
        "task": "task249",
        "title": "Which client accounts sit the extended verification test in the 2029 campus season because their "
                 "check would refer more than 15 per cent of the genuine candidates they shortlist, beside the 2028 "
                 "season's item exposure, impersonations and interrupted bookings",
        "domain": "Psychology & Behavioral Science",
        "subdomain": "psychometric-measurement-scale-validation (an unproctored adaptive aptitude test verified by a "
                     "proctored adaptive test: measurement error, the test's conditional standard error, the retest gain "
                     "and the referral rule's false referrals among shortlisted candidates)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10: a scorecard of the 28 client accounts against the 15 per cent referral cap, beside three "
                        "2028 integrity tables",
        "deliverables": [B.FILES["deliv_xlsx"], B.FILES["deliv_pdf"]],
        "input_files": files,
        "file_count": len(files),
        "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
        "largest_file": {"name": B.FILES["exposure"], "rows": rows},
        "distractors": [
            {"file": "selection_venues_2029.csv", "why_relevant": "the assessment-centre venues and seats for 2029 "
             "selection days, where MAT-V would be sat", "why_unused": "seat counts bear on logistics, not on how often "
             "the check refers a genuine candidate"},
            {"file": "candidate_feedback_2028.csv", "why_relevant": "candidates' own reports of technical problems in "
             "their 2028 sittings", "why_unused": "a sample survey of experience; interruptions are counted from the "
             "platform's attempts and nothing in the call reads it"},
        ],
        "sources": "Constructed: the firm, its client employers, the colleges, the candidates and the people are fictional. "
                   "The psychometric model (an adaptive test's conditional standard error, true-score regression among "
                   "candidates chosen on a score, the retest gain fading with the interval) and the practice of verifying "
                   "unproctored internet tests under proctoring are real. License: CC BY 4.0 (the task author's own work).",
        "as_of": "2029-05-14",
    }
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1)


if __name__ == "__main__":
    main()
