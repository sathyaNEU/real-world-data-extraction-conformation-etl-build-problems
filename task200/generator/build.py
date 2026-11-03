"""Cut target/ from the clean truth: python3 task200/generator/build.py [folder]"""
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack  # noqa: E402
import params as P  # noqa: E402


def walk(folder):
    out = []
    for root, _, files in os.walk(folder):
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), folder))
    return sorted(out)


def stamp(folder, when=P.EXPORT_STAMP):
    t = time.mktime((*when, 0, 0, -1))
    for rel in walk(folder):
        os.utime(os.path.join(folder, rel), (t, t))


def run(target):
    shutil.rmtree(target, ignore_errors=True)
    os.makedirs(target, exist_ok=True)
    W = pack.run(target)
    stamp(target)
    return W


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    t0 = time.time()
    run(t)
    print("built", t, "%.1fs" % (time.time() - t0))
    for rel in walk(t):
        print("  %-60s %10d" % (rel, os.path.getsize(os.path.join(t, rel))))
