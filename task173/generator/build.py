"""Build task173: the pack into <task>/target, the goldens into <task>/golden, metadata.json, generator/figures.json
and submission.md; then checks and the independent verifier; then a second full build into a scratch folder compared
byte for byte; then target.zip.

    python3 task173/generator/build.py              everything
    python3 task173/generator/build.py --pack-only  pack, goldens and write-up only"""
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
ZIP_STAMP = (2026, 10, 21, 16, 40, 0)
MTIME = calendar.timegm((2026, 10, 21, 21, 40, 0, 0, 0, 0))


def write_pack(out):
    from world import World
    import pack as P
    import docs as D
    import xlsx_writer as XW
    os.makedirs(out, exist_ok=True)
    XW.STAMPS.update({C.F_EAM: ("EAM Reporting", "2026-10-05T13:22:00Z"),
                      C.F_PAYEST: ("Contract Administration", "2026-10-20T15:05:00Z")})
    w = World()
    pk = P.Pack(w)
    n = {}
    n[C.F_GIS_SVC] = pk.write_gis_services(out)
    n[C.F_GIS_MAIN] = pk.write_gis_mains(out)
    n[C.F_PREM] = pk.write_premises(out)
    n[C.F_METER] = pk.write_meter_events(out)
    n[C.F_LEGACY], n[C.F_EAM] = pk.write_workorders(out)
    n[C.F_AMI] = pk.write_ami(out)
    n[C.F_PAYEST] = pk.write_payest(out)
    n[C.F_AP] = pk.write_ap(out)
    n[C.F_VALVE] = pk.write_valves(out)
    n[C.F_WX] = pk.write_weather(out)
    D.write_bid(os.path.join(out, C.F_BID))
    D.write_cip(os.path.join(out, C.F_CAP), w, pk)
    D.write_flush(os.path.join(out, C.F_FLUSH))
    D.write_dict(os.path.join(out, C.F_DICT))
    D.write_manifest(os.path.join(out, C.F_MAN), n)
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
    if os.path.exists(target):
        shutil.rmtree(target)
    n, w, pk = write_pack(target)
    import deliver
    import writeup
    figs = deliver.build(root, target)
    writeup.write(root, figs)
    return n


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-only", action="store_true")
    ap.add_argument("--target-only", action="store_true")
    a = ap.parse_args(argv)
    if a.target_only:
        n, w, pk = write_pack(os.path.join(TASK, "target"))
        print(n)
        return 0
    full(TASK)
    if a.pack_only:
        return 0
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py"), os.path.join(TASK, "target")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "verify.py"), os.path.join(TASK, "target")])
    tmp = tempfile.mkdtemp(prefix="t173_")
    try:
        for sub in ("generator",):
            shutil.copytree(os.path.join(TASK, sub), os.path.join(tmp, sub), ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(os.path.join(TASK, "metadata.json"), tmp)
        sys.path.insert(0, os.path.join(tmp, "generator"))
        full(tmp, quiet=True)
        a1, a2 = digest(os.path.join(TASK, "target")), digest(os.path.join(tmp, "target"))
        g1, g2 = digest(os.path.join(TASK, "golden")), digest(os.path.join(tmp, "golden"))
        same = a1 == a2 and g1 == g2 and open(os.path.join(TASK, "submission.md")).read() == open(os.path.join(tmp, "submission.md")).read()
        print("rebuild byte-identical: %s (%d target files, %d golden files)" % (same, len(a1), len(g1)))
        if not same:
            rc |= 1
            for k in sorted(set(a1) | set(a2)):
                if a1.get(k) != a2.get(k):
                    print("  differs:", k)
    finally:
        shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.md5(open(z, "rb").read()).hexdigest())
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
