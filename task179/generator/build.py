"""Build task179: the pack into <task>/target, the goldens into <task>/golden, metadata.json, generator/figures.json
and submission.md; then checks and the independent verifier; then a second full build into a scratch folder compared
byte for byte; then target.zip.

    python3 task179/generator/build.py              everything
    python3 task179/generator/build.py --pack-only  pack, goldens and write-up only"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C      # noqa: E402

TASK = os.path.dirname(HERE)
ZIP_STAMP = (2026, 10, 16, 15, 40, 0)
MTIME = calendar.timegm((2026, 10, 16, 2, 40, 0, 0, 0, 0))


def write_pack(out):
    from world import World
    from pack import Pack
    import docs as D
    import xlsx_writer as XW
    os.makedirs(out, exist_ok=True)
    XW.STAMPS.update({C.F_ADM: ("Admissions Office", "2026-10-06T21:14:00Z"),
                      C.F_TT: ("Timetabling", "2026-10-02T01:52:00Z")})
    w = World()
    pk = Pack(w)
    P = lambda f: os.path.join(out, f)
    n = {}
    n[C.F_SCLS] = pk.write_sirius_classes(P(C.F_SCLS))
    n[C.F_ACLS] = pk.write_arc_classes(P(C.F_ACLS))
    n[C.F_CENSUS] = pk.write_census(P(C.F_CENSUS))
    n[C.F_XWALK] = pk.write_crosswalk(P(C.F_XWALK))
    n[C.F_PROG] = pk.write_progress(P(C.F_PROG))
    n[C.F_CAT] = pk.write_catalogue(P(C.F_CAT))
    n[C.F_TRF] = pk.write_transfers(P(C.F_TRF))
    n[C.F_HALL] = pk.write_halls(P(C.F_HALL))
    n[C.F_NSL] = pk.write_school_leavers(P(C.F_NSL))
    n[C.F_TT] = pk.write_timetable(P(C.F_TT))
    n[C.F_CLE] = pk.write_class_enrolments(P(C.F_CLE))
    n[C.F_ADM] = pk.write_admissions(P(C.F_ADM))
    D.write_cutover(P(C.F_CUT))
    D.write_conventions(P(C.F_CONV))
    D.write_dict(P(C.F_DICT))
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return n, w, pk


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
    target = os.path.join(root, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n, w, pk = write_pack(target)
    if not quiet:
        for f in sorted(os.listdir(target)):
            print("  %-56s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), ("%d rows" % n[f]) if f in n else ""))
    gen = os.path.join(root, "generator") if root != TASK else HERE
    os.makedirs(gen, exist_ok=True)
    import deliver
    if os.path.isdir(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    deliver.main(target, os.path.join(root, "golden"), os.path.join(gen, "figures.json"),
                 os.path.join(root, "submission.md"), os.path.join(root, "metadata.json"), quiet=quiet)


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
        tmp = tempfile.mkdtemp(prefix="t179_rebuild_", dir=os.environ.get("T179_TMP"))
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
