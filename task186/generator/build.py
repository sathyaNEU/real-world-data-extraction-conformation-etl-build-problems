"""Builds task186 twice from nothing, checks the two builds are byte-identical, writes target/, golden/,
figures.json, metadata.json and target.zip.

    python3 task186/generator/build.py            # build, compare, install, zip
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
import golden as GD  # noqa: E402
import make_pack as M  # noqa: E402
import pack as PK  # noqa: E402

SOURCES = {
    "tip": "Kestrine TIP manager event export for the seven CT lanes, 1 July 2025 to 30 November 2026; synthetic",
    "library": "Kestrine 3D TIP library release 1.0, object catalogue and image list from the library manager; synthetic",
    "logins": "CT operator login register kept by the screening systems coordinator; synthetic",
    "register": "Screening officer register kept by the Head of Security Screening; synthetic",
    "standard": "SCS-04 screening officer competency standard, revision 6; synthetic",
    "roster": "Lane roster export from the screening rostering system, screening year 2025-26; synthetic",
    "leave": "Payroll system export of leave taken by screening officers, screening year 2025-26; synthetic",
    "throughput": "CT units' hourly image counts collected by the screening systems coordinator; synthetic",
    "units": "CT unit register (current location of each unit); synthetic",
    "queues": "Checkpoint daily queue time and passengers screened, calendar 2026; synthetic",
    "cbt": "Computer-based X-ray training sessions completed by screening officers, 2026; synthetic",
    "tipcfg": "TIP manager projection settings export; synthetic",
}


def metadata(n):
    return {
        "task": "task186", "architecture": 2, "as_of": "2026-12-02",
        "decision": "which X-ray screening officers come off X-ray duty at the January 2027 recertification under "
                    "the airport's screening officer competency standard",
        "deliverables": [GD.CSV, GD.PDF],
        "files": {PK.FILES[k]: {"source": SOURCES[k], "date": "2026-12-02", "license": "synthetic, CC0",
                                "role": "distractor" if k in PK.DISTRACTORS else "evidence"} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "largest_file": {"name": PK.FILES["tip"], "rows": n["tip"]},
        "row_counts": {PK.FILES[k]: v for k, v in sorted(n.items())},
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
    w, ids, n = M.build(target)
    GD.write_all(target, golden, gen)
    json.dump(metadata(n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=M.STAMP)
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
