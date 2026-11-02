"""Builds task138 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
submission.md, figures.json, metadata.json and target.zip.

    python3 task138/generator/build.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis  # noqa: E402
import golden  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402
import writeup  # noqa: E402

SOURCES = {
    "holter": "Ekerstede CPU HS-2 Holter station, 5-minute segment export of the continuous recordings of studies "
              "VLT-317-101 and VLT-317-102; synthetic",
    "ecg101": "Core laboratory ECG transfer 3 for study VLT-317-101 (triplicate extractions); synthetic",
    "ecg102": "Core laboratory ECG transfer 2 for study VLT-317-102 (triplicate extractions); synthetic",
    "plasma": "Ekerstede CPU bioanalytical laboratory, VLT-317 plasma results for inpatient samples; synthetic",
    "amb": "Ekerstede CPU laboratory results for ambulatory visits, 2026; synthetic",
    "dosing": "Ekerstede CPU dosing log for studies VLT-317-101 and VLT-317-102; synthetic",
    "rand": "Unblinded randomisation list for studies VLT-317-101 and VLT-317-102; synthetic",
    "screen": "Ekerstede CPU volunteer screening log, 2026; synthetic",
    "vitals": "Scheduled supine vital signs, studies VLT-317-101 and VLT-317-102; synthetic",
    "safety": "Safety 12-lead ECG machine reads at screening, admission, discharge and follow-up; synthetic",
    "plan": "Valtenna Therapeutics VLT-317 concentration-QTc analysis plan, version 2.0; synthetic",
    "ddi": "Valtenna Therapeutics clinical study report synopsis, study VLT-317-103; synthetic",
}


def metadata(n_rows):
    return {
        "task": "task138", "architecture": 4, "as_of": P.AS_OF,
        "decision": "the highest of the 25, 50 and 100 mg once-daily phase 2b doses of VLT-317 whose predicted "
                    "placebo-corrected QTc change at its high clinical exposure keeps the upper 90% bound below 10 ms",
        "deliverables": [golden.XLSX, golden.PDF],
        "files": {pack.FILES[k]: {"source": SOURCES[k], "date": P.AS_OF, "license": "synthetic, CC0",
                                  "role": "distractor" if pack.FILES[k] in pack.DISTRACTORS else "evidence"}
                  for k in pack.FILES},
        "distractor_files": list(pack.DISTRACTORS),
        "largest_file": {"name": pack.FILES["holter"], "rows": n_rows},
        "generator": {"seed": P.SEED, "streams": P.STREAMS},
    }


def zip_dir(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=(2026, 10, 28, 9, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(src, fn), "rb").read())


def build_once(out):
    W = world.build()
    tgt = os.path.join(out, "target")
    pack.write(W, tgt)
    F = analysis.golden(tgt)
    fig = golden.write(F, os.path.join(out, "golden"))
    fam = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in F["fam"].items()}
    writeup.write(fig, F["fam"], os.path.join(out, "submission.md"))
    figs = dict(fig)
    figs["family"] = fam
    with open(os.path.join(out, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    with open(os.path.join(out, "metadata.json"), "w") as f:
        json.dump(metadata(len(F["D"]["seg"])), f, indent=1)
    zip_dir(tgt, os.path.join(out, "target.zip"))
    return out


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def main():
    base = tempfile.mkdtemp(prefix="t138_")
    a = build_once(os.path.join(base, "a"))
    b = build_once(os.path.join(base, "b"))
    da, db = digest(a), digest(b)
    diff = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
    if diff:
        print("NOT BYTE-IDENTICAL:", diff)
        sys.exit(1)
    print("two builds byte-identical over %d files" % len(da))
    for name in ("target", "golden"):
        dst = os.path.join(TASK, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, name), dst)
    for name in ("submission.md", "metadata.json", "target.zip"):
        shutil.copyfile(os.path.join(a, name), os.path.join(TASK, name))
    shutil.copyfile(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.rmtree(base)
    print("installed; target.zip sha256 %s" % hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
