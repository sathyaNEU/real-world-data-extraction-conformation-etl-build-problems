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
ZIP_STAMP = (2027, 1, 8, 16, 40, 0)
MTIME = calendar.timegm((2027, 1, 8, 22, 40, 0, 0, 0, 0))
PARAMS = {}


def write_pack(out):
    from world import World
    from events import Events
    import pack as P
    import docs as D
    os.makedirs(out, exist_ok=True)
    w = World(PARAMS)
    ev = Events(w)
    pk = P.Pack(w, ev)
    n = {}
    n[C.F_EPIS] = pk.write_episodes(out)
    n[C.F_XWALK] = pk.write_crosswalk(out)
    n[C.F_ASSESS] = pk.write_assessments(out)
    n[C.F_DARROW] = pk.write_darrow(out)
    n[C.F_KESWICK] = pk.write_keswick(out)
    n[C.F_HPD] = pk.write_hpd(out)
    n[C.F_GPS] = pk.write_gps(out)
    n[C.F_PROG] = pk.write_programs(out)
    D.write_directive(os.path.join(out, C.F_DIRECTIVE))
    D.write_codes(os.path.join(out, C.F_CODE))
    D.write_schedule(os.path.join(out, C.F_SCHED))
    D.write_brief(os.path.join(out, C.F_BRIEF))
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return n, w, ev, pk


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
    n, w, ev, pk = write_pack(target)
    if not quiet:
        for f in sorted(os.listdir(target)):
            print("  %-52s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), ("%d rows" % n[f]) if f in n else ""))
    gen = os.path.join(root, "generator") if root != TASK else HERE
    os.makedirs(gen, exist_ok=True)
    import deliver
    if os.path.isdir(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    deliver.main(target, os.path.join(root, "golden"), os.path.join(gen, "figures.json"),
                 os.path.join(root, "submission.md"), os.path.join(root, "metadata.json"), n)
    return w, ev, pk


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
        tmp = tempfile.mkdtemp(prefix="t179_rebuild_")
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
