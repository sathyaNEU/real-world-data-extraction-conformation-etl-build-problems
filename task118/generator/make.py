"""Builds target/, the goldens, figures.json, submission.md and metadata.json; checks; a second build to
prove byte-identical rebuilds; target.zip; the verifier."""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)
import params as P
import pack as K
import golden as GD
import figs as F

STAMP = (2027, 1, 18, 9, 0, 0)


def stamp(folder):
    t = dt.datetime(*STAMP, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def fresh(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp


def build_once(target, golden):
    fresh(target)
    W, gt, rt = K.build(target)
    stamp(target)
    fig = F.compute(W, gt, rt)
    fresh(golden)
    GD.write(golden, fig)
    stamp(golden)
    return W, fig


def main(second=True, checks=True):
    W, fig = build_once(TARGET, GOLDEN)
    F.write(fig, os.path.join(HERE, "figures.json"))
    import writeup as WU
    WU.write(os.path.join(TASK, "submission.md"), fig)
    import meta as M
    M.write(TARGET, fig)
    if checks:
        import checks as C
        assert C.main(W, fig, TARGET) == 0
    if second:
        tmp = tempfile.mkdtemp()
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        build_once(t2, g2)
        d1, d2 = digest(TARGET), digest(t2)
        assert d1 == d2, [f for f in d1 if d1[f] != d2.get(f)]
        e1, e2 = digest(GOLDEN), digest(g2)
        assert e1 == e2, [f for f in e1 if e1[f] != e2.get(f)]
        shutil.rmtree(tmp)
        zp = cut_zip()
        print("byte-identical; target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
        import verify as V
        assert V.main(zp) == 0
        import ceiling as CE
        assert CE.main(zp) == 0
    return fig


if __name__ == "__main__":
    main(second="--once" not in sys.argv, checks="--nochecks" not in sys.argv)
