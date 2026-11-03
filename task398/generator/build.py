"""Build task398: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks, the independent verifier, a second full build compared byte for byte, and
target.zip cut from the final build.

    python3 task398/generator/build.py              everything
    python3 task398/generator/build.py --out DIR    the pack only, into DIR
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

import fund as F      # noqa: E402
import pack as P      # noqa: E402
import records as R   # noqa: E402

TASK = os.path.dirname(HERE)


def state():
    world = F.build_world()
    P.dress(world)
    act = F.simulate(world)
    S = dict(world=world, act=act)
    S["inp"] = F.recorded_inputs(world, act)
    S["settled"] = R.settled_positions(act)
    S["ent"] = R.entitlements(act)
    S["scrip_offer"] = R.scrip_offer(world, act)
    return S


def cut(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    S = state()
    S["counts"] = P.cut(out, S)
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
            zi = zipfile.ZipInfo(fn, date_time=(2026, 11, 3, 17, 26, 0))
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
    Fg = G.all_figures(S, target)
    WR.write_all(TASK, target, S, Fg)
    import checks as C
    ok = C.run(TASK, target, S, Fg)
    import verify as V
    vok = V.run(target, Fg)
    scratch = os.path.join(TASK, ".rebuild_check")
    cut(scratch)
    same = digest(scratch) == digest(target)
    shutil.rmtree(scratch)
    print("byte-identical rebuild:", "PASS" if same else "FAIL")
    # the goldens rebuild to the byte as well: nothing in them carries the build clock
    gold_tmp = os.path.join(TASK, ".golden_check")
    os.makedirs(gold_tmp, exist_ok=True)
    G.workbook(os.path.join(gold_tmp, "change_pricing_2025-26.xlsx"), S, Fg)
    G.deck(os.path.join(gold_tmp, "board_review_2025-26.pptx"), S, Fg)
    gsame = all(open(os.path.join(gold_tmp, f), "rb").read() == open(os.path.join(TASK, "golden", f), "rb").read()
                for f in sorted(os.listdir(gold_tmp)))
    shutil.rmtree(gold_tmp)
    print("byte-identical goldens:", "PASS" if gsame else "FAIL")
    same = same and gsame
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("target.zip", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:8])
    if not (ok and vok and same):
        sys.exit(1)


if __name__ == "__main__":
    main()
