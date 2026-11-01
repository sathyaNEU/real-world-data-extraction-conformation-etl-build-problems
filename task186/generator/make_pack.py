"""Builds the world and writes target/ (the pack) into a folder. Used by build.py and by the checks."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

STAMP = P.STAMP


def build(target):
    w = W.World()
    ids, n = PK.build(w, target)
    import time
    ts = time.mktime((2026, 12, 2, 9, 10, 0, 0, 0, -1))
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (ts, ts))
    return w, ids, n


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    w, ids, n = build(out)
    for k, v in sorted(n.items()):
        print(k, PK.FILES[k], v)
