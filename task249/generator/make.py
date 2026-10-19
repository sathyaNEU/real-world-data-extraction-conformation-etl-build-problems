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
            info = zipfile.ZipInfo("target/" + f, date_time=(2029, 1, 15, 9, 0, 0))
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
    rows = pd.read_parquet(os.path.join(target, B.FILES["sessions"]), columns=["client_id"]).shape[0]
    m = {
        "task": "task249",
        "title": "Which of a regional newspaper group's twelve local editions carry the measurement note in the 2029 media "
                 "kit because their reported monthly unique browsers for October to December 2028 overstate the browsers "
                 "that read them by more than 25 per cent, beside each edition's sold copies and newsletter subscribers",
        "domain": "Product Analytics",
        "subdomain": "metric-definition-measurement-science (a published audience metric counted by an analytics identifier "
                     "that WebKit deletes after seven days without a visit; the unique browsers it represents estimated by "
                     "replaying the identifier rule on browsers that keep it, matched on what the limit cannot change)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10: a scorecard of the twelve editions against the 25 per cent tolerance, beside two per-edition "
                        "figures of the kit",
        "deliverables": [B.FILES["deliv_xlsx"], B.FILES["deliv_pdf"]],
        "input_files": files,
        "file_count": len(files),
        "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
        "largest_file": {"name": B.FILES["sessions"], "rows": int(rows)},
        "distractors": [
            {"file": B.FILES["ads"], "why_relevant": "the ad server's delivered and viewable impressions by edition and device, "
             "the kit's inventory figures", "why_unused": "impressions are counted by the ad server per ad shown and say "
             "nothing about how many browsers an identifier stands for"},
            {"file": B.FILES["reach"], "why_relevant": "the Media-Analyse survey's readers per issue by edition, quoted in the "
             "kit beside print", "why_unused": "a survey of print readership; neither the note nor sold copies nor the "
             "newsletter count reads it"},
        ],
        "sources": "Constructed: the group, its editions, readers, accounts, subscriptions, retail points, newsletter contacts "
                   "and the people are fictional. The measurement facts are real: WebKit's tracking prevention limits "
                   "script-written cookies and storage to seven days from the last write (Safari on macOS and every iOS and "
                   "iPadOS browser); German dailies' sold copies follow the IVW's per-publication-day averages; newsletter "
                   "platforms export current status and keep activity logs. License: CC BY 4.0 (the task author's own work).",
        "as_of": "2029-01-15",
    }
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    main(t)
