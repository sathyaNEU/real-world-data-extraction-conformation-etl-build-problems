"""Build task202: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks, the independent verifier, a second full build compared byte for byte,
and target.zip cut from the final build.

    python3 task202/generator/build.py              everything
    python3 task202/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import hashlib
import os
import shutil
import sys
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)


def state():
    lk = W.lake()
    rv = W.river(lk)
    wk = W.works(lk)
    ph = W.river_phosphorus(rv, wk)
    sm = W.sampler(rv, ph)
    of = W.outfall(lk)
    sd = W.sondes(lk, rv)
    S = dict(lake=lk, river=rv, works=wk, phos=ph, sampler=sm, outfall=of, sondes=sd)
    S["monthly"] = P.works_monthly(wk)
    S["survey"] = W.survey()
    S["lab"] = W.lab(lk, sd)
    S["bathing"] = W.bathing()
    S["farmyards"] = W.farmyards()
    return S


def cut(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    S = state()
    P.cut(out, S)
    return S


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def zip_target(target, dest):
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=(2026, 11, 9, 16, 42, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.out:
        cut(a.out)
        return
    target = os.path.join(TASK, "target")
    S = cut(target)
    import golden as G
    import writeup as WR
    F, seas, ins = G.all_figures(target)
    WR.write_all(TASK, target, S, F)
    import checks as C
    ok = C.run(TASK, target, S, F)
    import verify as V
    vok = V.run(target)
    scratch = os.path.join(TASK, ".rebuild_check")
    cut(scratch)
    same = digest(scratch) == digest(target)
    shutil.rmtree(scratch)
    print("byte-identical rebuild:", "PASS" if same else "FAIL")
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("target.zip", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:8])
    if not (ok and vok and same):
        sys.exit(1)


if __name__ == "__main__":
    main()
