"""Build task156: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte, then target.zip cut from the pack.

    python3 task156/generator/build.py              everything
    python3 task156/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK           # noqa: E402
import common as K          # noqa: E402
import docs as D            # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = time.mktime((2026, 10, 9, 9, 40, 0, 0, 0, -1))   # the file list's morning, Toronto


class Built:
    pass


def world():
    B = Built()
    B.W = WD.simulate()
    B.mods = AK.paid_team()
    B.flags = AK.flags_q3(B.W, B.mods)
    B.moves = AK.question_moves(B.W)
    B.cells = R.inbox_cells(B.W)
    B.old = R.old_workbook_cells(B.W, B.moves)
    B.plan = {s: dict(B.W.sites[s].plan) for s in K.SITES}
    return B


def build_data(out, B):
    p = lambda f: os.path.join(out, f)
    n = {}
    W = B.W
    n[R.F_INBOX] = K.write_csv(p(R.F_INBOX), R.INBOX_COLS, R.inbox_rows(W, B.cells))
    n[R.F_INBOX_PRE] = K.write_csv(p(R.F_INBOX_PRE), R.INBOX_COLS, R.inbox_prelim_rows(W, B.cells))
    R.write_old_workbook(p(R.F_OLD), B.old)
    n[R.F_ROSTER] = K.write_csv(p(R.F_ROSTER), R.ROSTER_COLS, R.roster_rows(W))
    n[R.F_FLAGSUM] = K.write_csv(p(R.F_FLAGSUM), R.FLAGSUM_COLS, R.flagsum_rows(W))
    n[R.F_POSTS] = K.write_csv(p(R.F_POSTS), R.POSTS_COLS, R.posts_rows(W))
    R.write_plan(p(R.F_PLAN), W, B.plan)
    n[R.F_REGISTER] = K.write_csv(p(R.F_REGISTER), R.REGISTER_COLS, R.register_rows())
    p1, p2 = R.flag_export_rows(B.flags)
    n[R.F_FLAGS1] = K.write_csv(p(R.F_FLAGS1), R.FLAG_COLS, p1, crlf=True)
    n[R.F_FLAGS2] = K.write_csv(p(R.F_FLAGS2), R.FLAG_COLS, p2, crlf=True)
    n[R.F_REVIEWS] = K.write_csv(p(R.F_REVIEWS), R.REVIEW_COLS, R.review_rows(B.flags), crlf=True)
    n[R.F_WFM] = K.write_csv(p(R.F_WFM), R.WFM_COLS, R.wfm_rows(B.mods))
    n[R.F_ASSIGN] = K.write_csv(p(R.F_ASSIGN), R.ASSIGN_COLS, R.assign_rows(B.mods))
    n[R.F_MOVES] = K.write_csv(p(R.F_MOVES), R.MOVE_COLS, R.move_rows(B.moves))
    n[R.F_PAGEVIEWS] = K.write_csv(p(R.F_PAGEVIEWS), R.PV_COLS, R.pageview_rows(W))
    return n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(R.F_OLD), "Community Operations", "Community Operations", "2022-01-11T15:02:00Z",
                       "2024-01-09T16:48:00Z", excel=True)
    PP.normalize_ooxml(p(R.F_PLAN), "Planning & Analytics", "Planning & Analytics", "2026-09-14T13:20:00Z",
                       "2026-09-18T19:05:00Z", excel=True)


def build(out, quiet=False, B=None, docs=True):
    os.makedirs(out, exist_ok=True)
    B = B or world()
    n = build_data(out, B)
    normalize(out)
    if docs:
        D.write_all(out, n)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-58s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if f in n else ""))
    return B, n


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
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 9, 9, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    import subprocess
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    B, n = build(target)
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"), B)
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    tmp = tempfile.mkdtemp(prefix="b156_", dir=TASK)
    try:
        build(os.path.join(tmp, "target"), quiet=True)
        deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"),
                     os.path.join(tmp, "submission.md"), None)
        same = digest(target) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
        same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"), "rb").read()
        print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
    finally:
        shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    if r1.returncode or r2.returncode or not (same and same_g and same_f and same_s):
        sys.exit(1)


if __name__ == "__main__":
    main()
