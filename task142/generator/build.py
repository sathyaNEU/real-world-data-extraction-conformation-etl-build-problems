"""Builds task142 (architecture 3) twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
generator/figures.json, metadata.json, target.zip and submission.md.

    python3 task142/generator/build.py
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
import deliver as GD  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402

SOURCES = {
    "brp": "Gemeente Veenhaven, extract of the municipal population register for Veenhaven-Noord (residents since 1 October 2020)",
    "roll": "Basisschool De Kwikstaart pupil administration, the roll at each 1 October count 2020 to 2026",
    "procedure": "Stichting Primair Onderwijs Veenhaven, procedure PV-2 v2 for pupil forecasts",
    "accommodation": "Stichting Primair Onderwijs Veenhaven, accommodation plan De Kwikstaart 2026",
    "district": "Gemeente Veenhaven, district profile Veenhaven-Noord 2026",
    "schools": "Gemeente Veenhaven, overview of the primary schools in Veenhaven-Noord, 12 October 2026",
    "gasreads": "Gasnet Veenstreek, monthly telemetry reads of the school's gas meters, August 2023 to August 2026",
    "gasmaster": "Gasnet Veenstreek, connection and meter master data for the school's gas connections, 1 October 2026",
    "bso_att": "Kinderopvang Het Klavertje, after-school care attendance export, October 2026",
    "bso_loc": "Kinderopvang Het Klavertje, locations and contracts, October 2026",
    "request": "Stichting Primair Onderwijs Veenhaven, draft accommodation request 2028",
    "calendar": "Basisschool De Kwikstaart, school calendar 2026-2027",
}


def metadata(n, w):
    return {
        "task": "task142", "architecture": 3, "as_of": P.ASOF.isoformat(),
        "decision": "whether Basisschool De Kwikstaart exceeds its buildings' capacity at the 1 October counts of 2027, "
                    "2028 or 2029, and from which count",
        "deliverables": [GD.BOOK],
        "files": {P.FILES[k]: {"source": SOURCES[k] + "; synthetic, built for this task", "date": P.ASOF.isoformat(),
                               "license": "synthetic, CC0",
                               "role": "distractor" if k in P.DISTRACTORS else "evidence"} for k in P.FILES},
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "stated_inputs": [str(w["capacity"]), "3841", "3842"],
        "distractor_notes": {
            P.FILES["district"]: "the municipality's population by age per neighbourhood; relevant to the catchment, "
                                 "unused by the solution",
            P.FILES["calendar"]: "the school's holidays and study days; relevant to the school year, unused by the solution",
        },
        "largest_file": {"name": P.FILES["brp"], "rows": n["brp"]},
        "row_counts": {P.FILES[k]: v for k, v in sorted(n.items()) if k in P.FILES},
    }


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = (os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen"))
    w, n = PK.build(target)
    GD.write_all(target, golden, gen)
    with open(os.path.join(base, "metadata.json"), "w") as fh:
        json.dump(metadata(n, w), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=GD.STAMP)
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
    import writeup
    writeup.main()
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
