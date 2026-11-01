"""Builds task138 (architecture 3) twice from nothing, checks the two builds are byte-identical, installs target/, golden/,
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

DISTRACTORS = ("outages", "ties")
SOURCES = {
    "scada_old": ("Breckwater Electric Cooperative SCADA historian (retired system), Dunraith feeder hourly kW, "
                  "summers 2022 and 2023, exported 2024-03-18", "2024-03-18"),
    "scada_new": ("Breckwater Electric Cooperative SCADA historian, Dunraith feeder hourly MW, summers 2024 to 2026",
                  "2026-10-06"),
    "wx": ("Mossford Municipal Airport ASOS routine and special observations, summers 2022 to 2026, climate data "
           "service export (local standard time)",
           "2026-10-06"),
    "criteria": ("Breckwater Electric Cooperative Distribution Planning Criteria, revision 4", "2024-02-27"),
    "opplan": ("Breckwater Electric Cooperative 2027 Operating Plan, Board approved", "2026-09-22"),
    "testplan": ("Breckwater Electric Cooperative CVR pilot test plan, Dunraith 2025", "2025-05-16"),
    "reglog": ("Dunraith feeder regulator controller event log, May to October 2025", "2025-10-14"),
    "forecast": ("Hollis & Brandt Utility Consulting, BEC load forecast 2025", "2025-06-24"),
    "mdms": ("Breckwater Electric Cooperative meter data management system, transformer daily kWh, Dunraith, "
             "June to September 2026", "2026-10-12"),
    "so": ("Breckwater Electric Cooperative switching order SO-2026-114", "2026-07-01"),
    "register": ("Breckwater Electric Cooperative GIS export, Dunraith transformers and protective devices",
                 "2026-10-09"),
    "mv90": ("Westmarch G&T MV-90 interval export, delivery point DP-0417, June to September 2026", "2026-10-14"),
    "dpsched": ("Wholesale Power Contract Exhibit A, delivery points and metering, revision 2024-1", "2023-12-05"),
    "outages": ("Breckwater Electric Cooperative OMS outage events, Dunraith feeders, 2026", "2026-10-21"),
    "ties": ("Breckwater Electric Cooperative Dunraith feeder ties to neighbouring substations", "2026-08-03"),
}


def metadata(n):
    return {
        "task": "task138", "architecture": 3, "as_of": PR.AS_OF,
        "decision": "how much load Breckwater Electric Cooperative must transfer off the Dunraith substation in "
                    "each summer from 2027 to 2031 to keep its planning peak within the firm rating, with "
                    "conservation voltage reduction on every feeder from June 2027",
        "deliverables": [GD.BOOK],
        "files": {PK.FILES[k]: {"source": SOURCES[k][0], "date": SOURCES[k][1],
                                "license": "synthetic, constructed for this task, CC0",
                                "role": "distractor" if k in DISTRACTORS else "evidence"} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in DISTRACTORS],
        "largest_file": {"name": PK.FILES["scada_new"], "rows": n["scada_new"]},
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
