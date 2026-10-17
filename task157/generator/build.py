"""Build task157: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte, then target.zip cut from the pack.

    python3 task157/generator/build.py              everything
    python3 task157/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import ops as OP            # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2027, 1, 3, 21, 46, 0)                       # the pull's end, Central time
MTIME = calendar.timegm((2027, 1, 4, 3, 46, 0, 0, 0, 0))  # the same moment, UTC


class Built:
    pass


def world():
    B = Built()
    B.W = WD.simulate()
    B.O = OP.build(B.W)
    B.S = R.shape(B.W, B.O)
    return B


def build_data(out, B):
    p = lambda f: os.path.join(out, f)
    W, O, S = B.W, B.O, B.S
    n = {}
    n[R.F_LEGACY] = K.write_csv(p(R.F_LEGACY), R.LEGACY_COLS, R.legacy_rows(W, O, S), crlf=True)
    n[R.F_ACTIVITY] = K.write_csv(p(R.F_ACTIVITY), R.ACTIVITY_COLS, R.activity_rows(W, O, S))
    n[R.F_CROSSWALK] = K.write_csv(p(R.F_CROSSWALK), R.CROSSWALK_COLS, R.crosswalk_rows(W, O, S))
    n[R.F_ACCOUNTS] = K.write_csv(p(R.F_ACCOUNTS), R.ACCOUNT_COLS, R.account_rows(W, O, S))
    R.write_run25(p(R.F_RUN25), W, O)
    n[R.F_RUN25] = len(O.pay[2025].main_ids)
    n[R.F_RUN26] = K.write_csv(p(R.F_RUN26), R.RUN26_COLS, R.run26_rows(W, O))
    n[R.F_ADJ] = K.write_csv(p(R.F_ADJ), R.ADJ_COLS, R.adj_rows(W, O))
    n[R.F_RETURNS] = K.write_csv(p(R.F_RETURNS), R.RETURN_COLS, R.return_rows(W, O))
    n[R.F_EVENTS] = K.write_csv(p(R.F_EVENTS), R.EVENT_COLS, R.event_rows(W, O))
    n[R.F_APPS] = K.write_csv(p(R.F_APPS), R.APP_COLS, R.app_rows(S))
    n[R.F_ORDERS] = K.write_csv(p(R.F_ORDERS), R.ORDER_COLS, R.order_rows(S))
    n[R.F_REFERRAL] = K.write_csv(p(R.F_REFERRAL), R.REFERRAL_COLS, R.referral_rows(W, O))
    R.write_demand(p(R.F_DEMAND), W)
    return n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(R.F_RUN25), "Payout Reports", "Payout Reports", "2025-02-14T14:02:00Z",
                       "2025-02-14T14:02:00Z", excel=True, company=K.OPERATOR)
    PP.normalize_ooxml(p(R.F_DEMAND), "Marketplace Planning", "Marketplace Planning", "2026-11-23T16:20:00Z",
                       "2026-12-04T17:05:00Z", excel=True, company=K.OPERATOR)


def build(out, quiet=False, B=None):
    os.makedirs(out, exist_ok=True)
    B = B or world()
    n = build_data(out, B)
    normalize(out)
    DOC.write_all(out, n)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-56s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
                                              ("%d rows" % n[f]) if f in n else ""))
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
            zi = zipfile.ZipInfo(f, date_time=PULL_DONE)
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
                 os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    tmp = tempfile.mkdtemp(prefix="b157_", dir=TASK)
    try:
        build(os.path.join(tmp, "target"), quiet=True)
        deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"),
                     os.path.join(tmp, "submission.md"))
        same = digest(target) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"),
                                                                               "rb").read()
        same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"),
                                                                                "rb").read()
        print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
    finally:
        shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    if r1.returncode or r2.returncode or not (same and same_g and same_f and same_s):
        sys.exit(1)


if __name__ == "__main__":
    main()
