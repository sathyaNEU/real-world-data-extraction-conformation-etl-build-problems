"""Builds task160 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
figures.json, metadata.json and target.zip.

    python3 task160/generator/build.py"""
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
import golden as GD  # noqa: E402
import io_util as IO  # noqa: E402
import pack as PK  # noqa: E402

SOURCES = {
    "history": ("Quillfield Regional Medical Center, Clarity medication alert history extract, pulled by quarter",
                "evidence"),
    "background": ("Quillfield Pharmacy Informatics, MSP26 background (silent) mode log", "evidence"),
    "census": ("Quillfield patient flow, unit census by day", "evidence"),
    "plan": ("Quillfield Finance, Decision Support, FY2027 inpatient volume plan", "evidence"),
    "register": ("Quillfield Pharmacy Informatics, medication alert rule register", "evidence"),
    "release": ("Halverson Clinical Content, MSP26 content release 2026.2 client bulletin", "evidence"),
    "schedule": ("Corvane Remote Pharmacy and Quillfield, Schedule B override review service, revision 3",
                 "evidence"),
    "cr": ("Quillfield change request CR-2291", "evidence"),
    "queue": ("Corvane Remote Pharmacy, review queue export for client QRMC", "evidence"),
    "pocmap": ("Corvane Remote Pharmacy, client point-of-care location map", "evidence"),
    "pump": ("Quillfield biomedical engineering, smart pump guardrail event export, Q3 2026", "distractor"),
    "interventions": ("Quillfield Pharmacy Clinical Services, pharmacist intervention log, Q3 2026", "distractor"),
}


def metadata(n):
    return {
        "task": "task160", "architecture": 2, "as_of": "2026-10-28",
        "decision": "the net change in override reviews Corvane's desk should plan for from Quillfield's adult wards "
                    "in the thirteen weeks from 4 January 2027, when the MSP26 alert package goes live on every adult "
                    "ward, against the same weeks without the go-live",
        "deliverables": [GD.BOOK, GD.MEMO],
        "files": {PK.FILES[k]: {"source": SOURCES[k][0] + "; synthetic, built for this task", "date": "2026-10-28",
                                "license": "synthetic, CC0", "role": SOURCES[k][1]} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "distractors": {PK.FILES["pump"]: "infusion pump guardrail events: medication safety alerts of another kind, "
                                          "never sent to the review desk",
                        PK.FILES["interventions"]: "Quillfield's own pharmacists' interventions: pharmacist workload "
                                                   "that is not override review"},
        "largest_file": {"name": PK.FILES["history"], "rows": n["history"]},
        "row_counts": {PK.FILES[k]: v for k, v in sorted(n.items()) if v},
    }


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen")
    os.makedirs(gen, exist_ok=True)
    _w, _R, n = PK.build(target)
    GD.write_all(target, golden, gen)
    json.dump(metadata(n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=IO.ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    da, db = one_build(a), one_build(b)
    if da != db:
        bad = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        print("NOT byte-identical:", bad)
        sys.exit(1)
    print("two builds byte-identical over %d files" % len(da))
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "gen", "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
