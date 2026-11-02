"""Builds task149 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
figures.json, metadata.json and target.zip.

    python3 task149/generator/build.py"""
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
import params as P  # noqa: E402

SOURCES = {
    "stays": ("Vantra Insights, Resident Mobility Panel extract RMP-2027-114, stays", "evidence"),
    "devices": ("Vantra Insights, Resident Mobility Panel extract RMP-2027-114, devices", "evidence"),
    "cells": ("Vantra Insights, cell to census zone lookup v3", "evidence"),
    "census": ("Census 2022 place of work tables, Rathgarvan catchment small areas, KMTA GIS extract", "evidence"),
    "case": ("KMTA Rail Planning, Rathgarvan Station Final Business Case demand refresh, draft v0.4", "evidence"),
    "review": ("KMTA Rail Planning, Lisnagry Station post-opening review, April 2020", "evidence"),
    "gates": ("Ardnagree line operator, daily gate entries by location code, 1 January 2018 to 30 November 2027",
              "evidence"),
    "register": ("Ardnagree line operator, station register", "evidence"),
    "assets": ("Ardnagree line operator, gate asset register, location history", "evidence"),
    "calendar": ("KMTA, public holiday and school break calendar 2018 to 2027", "evidence"),
    "panel_note": ("Vantra Mobile Ireland and KMTA, data licence 2027-114, Schedule 2 service description", "evidence"),
    "housing": ("Kilcarrow City and County Council Planning Department, Rathgarvan residential pipeline, October 2027",
                "distractor"),
    "jobs": ("Kilcarrow City and County Council Economic Development Unit, employment outlook to 2030", "distractor"),
    "timetable": ("Ardnagree line operator, draft 2028 timetable, departures from Rathgarvan", "distractor"),
}


def metadata(n, R):
    return {
        "task": "task149", "architecture": 2, "as_of": P.AS_OF,
        "decision": "the commuter boardings the new Rathgarvan station will carry on an average ordinary weekday in "
                    "2029, and on that figure whether the full or the reduced scheme is built",
        "deliverables": [GD.BOOK, GD.MEMO],
        "files": {PK.FILES[k]: {"source": SOURCES[k][0] + "; synthetic, built for this task", "date": P.AS_OF,
                                "license": "synthetic, CC0", "role": SOURCES[k][1]} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "distractors": {
            PK.FILES["housing"]: "new homes in the catchment: every expected completion falls in 2030 or later, and "
                                 "the refresh holds the census base at 2022",
            PK.FILES["jobs"]: "jobs growth by employment area to 2030: the refresh holds the catchment's commuters at "
                              "the 2022 census base",
            PK.FILES["timetable"]: "the draft 2028 departures from Rathgarvan: service frequency and train length do "
                                   "not enter the commuter count",
        },
        "largest_file": {"name": PK.FILES["stays"], "rows": n["stays"]},
        "stated_inputs": ["1,400", "1400"],
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
    _w, n, _mean = PK.build(target)
    R, _F = GD.write_all(target, golden, gen)
    json.dump(metadata(n, R), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
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
    for fn in ("figures.json", "results.json", "variants.json"):
        shutil.copy(os.path.join(a, "gen", fn), os.path.join(HERE, fn))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
