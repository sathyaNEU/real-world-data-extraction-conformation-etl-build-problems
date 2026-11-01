"""Builds task273 twice from nothing, checks the two builds are byte-identical, writes target/, golden/,
figures.json, metadata.json and target.zip.

    python3 task273/generator/build.py            # build, compare, install, zip
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
    "daily": "Kaitanga site SCADA historian, monthly export of each production bore's daily take, mean pumping "
             "water level and pump run hours; synthetic, built for this task",
    "mb1": "Matarae Regional Council environmental data portal, MB1 daily mean groundwater level; synthetic",
    "register": "Kaitanga bore register maintained by the site utilities team; synthetic",
    "test": "Waipa Drilling Ltd logger record of the PB9 step and constant-rate test, October 2026; synthetic",
    "plan": "Kaitanga summer bore plan 2026-27 prepared for the site drought committee; synthetic",
    "standard": "SWS-03 site water supply security standard, revision 4; synthetic",
    "permit": "Matarae Regional Council water permit AUTH-117204 as varied 19 October 2026; synthetic",
    "telemetry": "Matarae Regional Council water use telemetry for AUTH-117204, 2025-26; synthetic",
    "icp": "Metering equipment provider half-hourly interval data for the pump ICPs, 2025-26; synthetic",
    "icp_reg": "Site register of pump ICPs and meters; synthetic",
    "nitrate": "Quarterly nitrate-nitrogen results for the production bores; synthetic",
    "rain": "Kaitanga site weather station daily rainfall (9 am to 9 am); synthetic",
}


def metadata(n):
    return {
        "task": "task273", "architecture": 6, "as_of": "2026-11-02",
        "decision": "whether the Kaitanga bore field's 2026-27 summer plan passes the site's drought test, and the "
                    "bores and months that fail it",
        "deliverables": [GD.BOOK, GD.DECK],
        "files": {PK.FILES[k]: {"source": SOURCES[k], "date": "2026-11-02", "license": "synthetic, CC0",
                                "role": "distractor" if k in PK.DISTRACTORS else "evidence"} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "largest_file": {"name": PK.FILES["telemetry"], "rows": n["telemetry"]},
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
    w, plan, n, truth = M.build(target)
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
