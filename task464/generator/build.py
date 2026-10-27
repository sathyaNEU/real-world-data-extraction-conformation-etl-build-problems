#!/usr/bin/env python3
"""task464: the one entry point. Builds the clean truth, the record, the bundle, the goldens, the
write-up and target.zip, and runs every assertion.

    python3 generator/build.py [--skip-zip]

It writes generator/figures.json itself, so a rebuild from this script alone leaves the task folder clean
(reduce-house-fixes H33).
"""
import datetime as dt
import os
import random
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import answers          # noqa: E402
import checks           # noqa: E402
import docs             # noqa: E402
import golden           # noqa: E402
import metadata         # noqa: E402
import pack             # noqa: E402
import sim              # noqa: E402
import world            # noqa: E402
import writeup          # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
EXPORT_STAMP = dt.datetime(2027, 2, 16, 10, 30, 0)


def normalise_mtimes(root, stamp=EXPORT_STAMP):
    t = stamp.timestamp()
    for base, dirs, files in os.walk(root):
        for n in sorted(files):
            os.utime(os.path.join(base, n), (t, t))
        for n in sorted(dirs):
            os.utime(os.path.join(base, n), (t, t))


def make_zip(path, root, stamp=EXPORT_STAMP):
    names = []
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for n in sorted(files):
            full = os.path.join(base, n)
            names.append((os.path.relpath(full, root).replace(os.sep, "/"), full))
    names.sort()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, full in names:
            zi = zipfile.ZipInfo(arc, date_time=(stamp.year, stamp.month, stamp.day,
                                                 stamp.hour, stamp.minute, stamp.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(full, "rb") as f:
                z.writestr(zi, f.read())
    return names


def run(skip_zip=False):
    rnd = random.Random(world.SEED + 17)
    sites, by_area = world.build()
    extra, moved = world.extras(sites)
    rows, panels = sim.build(sites)
    cancels = sim.noshows(rows, sites)

    for d in (TARGET, GOLDEN):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)

    dir_rows, taxes = pack.directory(TARGET, sites, extra, rnd)
    lic_rows, reissues, amendments = pack.licence_register(TARGET, sites, extra, rnd)
    roster_rows = pack.roster(TARGET, sites)
    na, nb = pack.encounters_db(TARGET, sites, rows, cancels)
    proj_rows = pack.projection(TARGET, by_area)
    filing_rows = pack.filing(TARGET, sites, extra, rnd)
    oon_main, oon_runout = pack.out_of_network(TARGET, sites, extra, rows, rnd)
    trans = pack.transmittal(TARGET, na, nb, rows, cancels)
    nemt_rows = pack.nemt(TARGET, by_area, rnd)
    docs.write(TARGET)

    truth = golden.write(GOLDEN, sites, by_area, extra, rows, lic_rows, filing_rows, dir_rows,
                         oon_main, oon_runout)
    state = dict(sites=sites, by_area=by_area, extra=extra, rows=rows, cancels=cancels, panels=panels,
                 dir_rows=dir_rows, lic_rows=lic_rows, roster_rows=roster_rows, proj_rows=proj_rows,
                 filing_rows=filing_rows, oon_main=oon_main, oon_runout=oon_runout, trans=trans,
                 nemt_rows=nemt_rows, truth=truth, target=TARGET, golden=GOLDEN, task=TASK,
                 reissues=reissues, amendments=amendments, moved=moved, na=na, nb=nb, taxes=taxes)
    metadata.write(TASK, truth)
    writeup.write(TASK, state)
    normalise_mtimes(TARGET)
    normalise_mtimes(GOLDEN)
    n = checks.run(state)
    if not skip_zip:
        names = make_zip(os.path.join(TASK, "target.zip"), TARGET)
        print("target.zip: %d members" % len(names))
    print("checks: %d assertions passed" % n)
    return state


if __name__ == "__main__":
    run(skip_zip="--skip-zip" in sys.argv)
