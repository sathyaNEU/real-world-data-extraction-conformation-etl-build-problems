#!/usr/bin/env python3
"""Build task128 twice into scratch, assert byte-identical, build into the task folder, run the
independent verifier there.

    python3 ship.py --task /path/to/task128 --scratch /path/to/scratch
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def digest(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit("failed: " + " ".join(cmd))
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    gen = os.path.join(HERE, "build.py")
    ver = os.path.join(HERE, "verify.py")
    dirs = []
    for k in ("build_a", "build_b"):
        d = os.path.join(a.scratch, k)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        print(run([sys.executable, gen, "--out", d]))
        dirs.append(d)
    da = digest(os.path.join(dirs[0], "target"))
    db = digest(os.path.join(dirs[1], "target"))
    assert da == db, "two builds differ in target/: " + str(set(da) ^ set(db) or
                     [k for k in da if da[k] != db.get(k)])
    ga = digest(os.path.join(dirs[0], "golden"))
    gb = digest(os.path.join(dirs[1], "golden"))
    assert ga == gb, "two builds differ in golden/"
    ma = hashlib.sha256(open(os.path.join(dirs[0], "metadata.json"), "rb").read()).hexdigest()
    mb = hashlib.sha256(open(os.path.join(dirs[1], "metadata.json"), "rb").read()).hexdigest()
    assert ma == mb, "metadata differs between builds"
    print(f"byte-identical: {len(da)} target files, {len(ga)} golden files, metadata")
    print(run([sys.executable, gen, "--out", a.task]))
    dt_ = digest(os.path.join(a.task, "target"))
    assert dt_ == da, "shipped target differs from scratch builds"
    print("shipped pack byte-identical to the scratch builds")
    print(run([sys.executable, "-I", ver, a.task]))


if __name__ == "__main__":
    main()
