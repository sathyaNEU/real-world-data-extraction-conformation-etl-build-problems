"""Build task501: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, submission.md, then the checks and the independent verifier, then a second full build into a
scratch folder inside the task (removed after) compared byte for byte. target.zip is cut from the final build with --zip.

    python3 task501/generator/build.py              everything
    python3 task501/generator/build.py --zip        everything, then target.zip
    python3 task501/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import hashlib
import os
import shutil
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK          # noqa: E402
import records as RC       # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2026, 11, 16, 9, 30, 0)


def set_mtimes(folder):
    t = time.mktime(STAMP + (0, 0, -1))
    for root, _, files in os.walk(folder):
        for f in files:
            os.utime(os.path.join(root, f), (t, t))


def write_pack(out, tr=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    n, info = PK.write_pack(out, tr)
    set_mtimes(out)
    return n, info


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip(target, zpath):
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    if a.out:
        write_pack(a.out)
        return
    import checks as K
    import golden as G
    import writeup as WU
    target = os.path.join(TASK, "target")
    gold = os.path.join(TASK, "golden")
    tr = RC.truth()
    counts, info = write_pack(target, tr)
    res, figs = G.build(target, gold, os.path.join(HERE, "figures.json"))
    G.metadata(os.path.join(TASK, "metadata.json"), target, counts)
    WU.main()
    set_mtimes(gold)
    K.run(target, gold, tr, info, res, figs)
    import verify as V
    V.main([target, os.path.join(HERE, "figures.json")])
    if not a.no_rebuild:
        scratch = os.path.join(TASK, ".rebuild")
        write_pack(scratch)
        G.build(scratch, os.path.join(scratch, "_golden"), os.path.join(scratch, "_figures.json"))
        set_mtimes(scratch)
        d1 = digest(target)
        d2 = {k: v for k, v in digest(scratch).items() if not k.startswith("_")}
        g1 = digest(gold)
        g2 = digest(os.path.join(scratch, "_golden"))
        f1 = hashlib.sha256(open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
        f2 = hashlib.sha256(open(os.path.join(scratch, "_figures.json"), "rb").read()).hexdigest()
        shutil.rmtree(scratch)
        assert d1 == d2, sorted(k for k in set(d1) | set(d2) if d1.get(k) != d2.get(k))
        assert g1 == g2, sorted(k for k in set(g1) | set(g2) if g1.get(k) != g2.get(k))
        assert f1 == f2, "figures.json differs between builds"
        print("REBUILD  byte-identical: %d pack files, %d goldens, figures.json" % (len(d1), len(g1)))
    if a.zip:
        cut_zip(target, os.path.join(TASK, "target.zip"))
        print("ZIP      %s" % os.path.join(TASK, "target.zip"))


if __name__ == "__main__":
    main()
