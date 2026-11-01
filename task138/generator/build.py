"""Builds task138 twice from nothing, checks the two builds are byte-identical, installs target/, golden/,
figures.json and metadata.json, and cuts target.zip.

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
import golden as GD  # noqa: E402
import io_util as IO  # noqa: E402
import pack as PK  # noqa: E402
import params as PR  # noqa: E402
import world as W  # noqa: E402

DISTRACTORS = ("precip", "inspection")
SOURCES = {
    "peaks": ("State Water Survey annual peak streamflow export for the five Tamsen basin streamgauges, retrieved "
              "28 October 2026", "2026-10-28"),
    "standard": ("Orrinsford Levee and Drainage District levee design and review standard LS-02, revision 3",
                 "2018-04-09"),
    "skew": ("State Water Survey technical release SW-16-03, regional skew coefficients", "2016-09-26"),
    "table4": ("Orrinsford Levee Hydraulic Update (2019), Table 4, water surface elevations at levee cross-sections",
               "2019-12-16"),
    "inventory": ("State Department of Natural Resources Tamsen River levee inventory extract", "2025-03-14"),
    "crown24": ("Orrinsford levee crown certification survey, May 2024", "2024-05-31"),
    "crown16": ("Orrinsford levee crown profile survey, October 2016", "2016-10-14"),
    "bench": ("Orrinsford Levee and Drainage District vertical control list", "2019-08-20"),
    "coyle": ("State Water Survey hourly gauge height and discharge, Tamsen River at Coyle Bridge, water years "
              "2017 to 2026", "2026-10-28"),
    "halbrook": ("Orrinsford streamgauge logger export (ORF2), all records", "2026-10-05"),
    "procedure": ("Orrinsford Levee and Drainage District operating procedure OP-04, flood warning and closures",
                  "2014-03-03"),
    "precip": ("Cooperative observer daily precipitation, Orrinsford 2 NE and Coyle 1 W", "2026-10-02"),
    "inspection": ("Orrinsford Levee and Drainage District 2025 annual levee inspection, summary of findings",
                   "2025-08-29"),
}


def metadata(n):
    return {
        "task": "task138", "architecture": 2, "as_of": PR.AS_OF,
        "decision": "whether the Orrinsford levee crown needs raising before the 2027 flood season, and by how many "
                    "whole feet",
        "deliverables": [GD.BOOK, GD.MEMO],
        "files": {PK.FILES[k]: {"source": SOURCES[k][0], "date": SOURCES[k][1],
                                "license": "synthetic, constructed for this task, CC0",
                                "role": "distractor" if k in DISTRACTORS else "evidence"} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in DISTRACTORS],
        "largest_file": {"name": PK.FILES["coyle"], "rows": n["coyle"]},
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
    S = W.simulate()
    n = PK.write_pack(S, target)
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
