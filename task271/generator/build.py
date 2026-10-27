"""Build task271: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte, then target.zip cut from the pack.

    python3 task271/generator/build.py              everything
    python3 task271/generator/build.py --out DIR    the pack only, into DIR"""
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
import common as K          # noqa: E402
import docs as D            # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import wealth as WL         # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = time.mktime((2026, 11, 4, 9, 20, 0, 0, 0, -1))   # the file list's morning, London


def world():
    X = W.simulate()
    X["orders"] = WL.simulate(X["stocks"], X["closes"])
    X["notes"] = WL.deal(X["orders"], X["stocks"], X["closes"])
    R.prepare(X)
    return X


def build_data(out, X):
    p = lambda f: os.path.join(out, f)
    n = {}
    n[R.F_HESS] = K.write_csv(p(R.F_HESS), R.HESS_COLS, R.hess_rows(X))
    n[R.F_ASHL] = K.write_csv(p(R.F_ASHL), R.ASHL_COLS, R.ashl_rows(X))
    R.write_pemb(p(R.F_PEMB), X)
    n[R.F_OMS] = K.write_csv(p(R.F_OMS), R.OMS_COLS, R.oms_rows(X))
    R.write_venues(p(R.F_VENUES))
    n[R.F_MASTER] = K.write_csv(p(R.F_MASTER), R.MASTER_COLS, R.master_rows(X))
    R.write_ca(p(R.F_CA), X)
    n[R.F_CAL] = K.write_csv(p(R.F_CAL), R.CAL_COLS, R.cal_rows())
    n[R.F_ORDERS] = K.write_csv(p(R.F_ORDERS), R.ORDER_COLS, R.order_rows(X))
    n[R.F_NOTES] = K.write_csv(p(R.F_NOTES), R.NOTE_COLS, R.note_rows(X), crlf=True)
    n[R.F_AUCT] = K.write_csv(p(R.F_AUCT), R.AUCT_COLS, R.auction_rows(X))
    return n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(R.F_PEMB), "Pemberwick Client Reporting", "Pemberwick Client Reporting",
                       "2026-11-02T07:41:00Z", "2026-11-02T07:44:00Z", excel=True, company="Pemberwick & Co")
    PP.normalize_ooxml(p(R.F_VENUES), "Owen Porter", "Declan Davies", "2023-02-20T10:12:00Z",
                       "2026-06-02T08:05:00Z", excel=True, company="Fenmarsh Investment Management")


def build(out, quiet=False, X=None, docs=True):
    os.makedirs(out, exist_ok=True)
    X = X or world()
    n = build_data(out, X)
    normalize(out)
    if docs:
        D.write_all(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-62s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if f in n else ""))
    return X, n


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
            zi = zipfile.ZipInfo(f, date_time=(2026, 11, 4, 9, 20, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    import subprocess
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    X, n = build(target)
    if a.pack_only:
        return
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    tmp = tempfile.mkdtemp(prefix="b271_", dir=TASK)
    try:
        build(os.path.join(tmp, "target"), quiet=True)
        deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"),
                     os.path.join(tmp, "submission.md"))
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
