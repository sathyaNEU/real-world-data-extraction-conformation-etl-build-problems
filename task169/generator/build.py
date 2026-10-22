"""Build task169: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build into
a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task169/generator/build.py              everything
    python3 task169/generator/build.py --pack-only  the pack, goldens and write-up, no checks"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import pickle
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C      # noqa: E402

TASK = os.path.dirname(HERE)
ZIP_STAMP = (2026, 10, 14, 16, 40, 0)
MTIME = calendar.timegm((2026, 10, 14, 20, 40, 0, 0, 0, 0))


def world():
    import records as R
    ppl, book = R.history()
    cohort = R.cohort(ppl, book)
    return ppl, book, cohort


def write_pack(out, ppl, book, cohort):
    import docs as D
    import pack as P
    import postprocess as PP
    import tables as T
    os.makedirs(out, exist_ok=True)
    ident = P.Identity(ppl, cohort)
    grades = P.arrest_grades(book)
    n = {}
    n[C.F_REL] = P.write_releases(os.path.join(out, C.F_REL), book, ident, ppl)
    n[C.F_ADM], lags = P.write_admissions(os.path.join(out, C.F_ADM), book, ident)
    n[C.F_ARR] = P.write_arrests(os.path.join(out, C.F_ARR), book, ident, grades)
    n[C.F_XW] = P.write_crosswalk(os.path.join(out, C.F_XW), ident)
    n[C.F_AOC] = P.write_cases(os.path.join(out, C.F_AOC), book, ident, grades)
    n[C.F_DEATH] = P.write_deaths(os.path.join(out, C.F_DEATH), book, ident)
    legacy, new = P.board_frames(book, ident)
    n[C.F_BLEG] = P.write_board_legacy(os.path.join(out, C.F_BLEG), legacy, None)
    n[C.F_BNEW] = P.write_board_new(os.path.join(out, C.F_BNEW), new)
    n[C.F_PROJ] = P.write_projection(os.path.join(out, C.F_PROJ), cohort, ident, book)
    n[C.F_CAP] = T.write_capacity(os.path.join(out, C.F_CAP), T.capacity_rows(book, lags))
    n[C.F_CASE] = T.write_caseload(os.path.join(out, C.F_CASE), T.caseload_rows(book, ident))
    T.write_dictionary(os.path.join(out, C.F_DICT))
    import calc
    D.write_prat(os.path.join(out, C.F_PRAT), calc.prat_study(out))
    D.write_act(os.path.join(out, C.F_ACT))
    D.write_methodology(os.path.join(out, C.F_METH))
    T.write_manifest(os.path.join(out, C.F_MAN), n)
    for f, who, when in ((C.F_BLEG, "Board of Parole", "2026-10-05T13:02:00Z"),
                         (C.F_CAP, "Bureau of Planning, Research and Statistics", "2026-10-06T14:20:00Z"),
                         (C.F_DICT, "Research and Projections Unit", "2026-10-14T19:55:00Z")):
        PP.stamp_ooxml(os.path.join(out, f), who, who, when, when)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return n


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip(root):
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def full(root, quiet=False):
    ppl, book, cohort = world()
    target = os.path.join(root, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n = write_pack(target, ppl, book, cohort)
    if not quiet:
        for f in sorted(os.listdir(target)):
            print("  %-56s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), ("%d rows" % n[f]) if f in n else ""))
    gen = os.path.join(root, "generator") if root != TASK else HERE
    os.makedirs(gen, exist_ok=True)
    if os.path.exists(os.path.join(HERE, "deliver.py")):
        import deliver
        import metadata
        if os.path.isdir(os.path.join(root, "golden")):
            shutil.rmtree(os.path.join(root, "golden"))
        deliver.main(target, os.path.join(root, "golden"), os.path.join(gen, "figures.json"),
                     os.path.join(root, "submission.md"))
        metadata.write(root)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-only", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    full(TASK)
    if a.pack_only:
        return
    target = os.path.join(TASK, "target")
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    if r1.returncode or r2.returncode:
        sys.exit("checks %d verify %d" % (r1.returncode, r2.returncode))
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="t169_rebuild_")
        try:
            full(tmp, quiet=True)
            mine = {k: v for k, v in digest(TASK).items() if k.split(os.sep)[0] in ("target", "golden")
                    or k in ("submission.md", "metadata.json", os.path.join("generator", "figures.json"))}
            theirs = digest(tmp)
            diff = [k for k in mine if mine[k] != theirs.get(k)]
            print("rebuild: %d files compared, %d differ%s" % (len(mine), len(diff), (": " + ", ".join(diff)) if diff else ""))
            if diff:
                sys.exit(1)
        finally:
            shutil.rmtree(tmp)
    print("zip:", cut_zip(TASK))


if __name__ == "__main__":
    main()
