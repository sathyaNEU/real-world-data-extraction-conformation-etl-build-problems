"""Build task156: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json, figures.json and
submission.md, then the checks and the independent verifier, then a second full build into a scratch folder compared
byte for byte, then target.zip cut from the pack.

    python3 task156/generator/build.py              everything
    python3 task156/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D            # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = time.mktime((2026, 11, 4, 9, 30, 0, 0, 0, -1))
ZIP_TIME = (2026, 11, 4, 9, 30, 0)


def build_data(out):
    p = lambda f: os.path.join(out, f)
    n = {}
    n[R.F_SCADA] = R.write_csv(p(R.F_SCADA), R.SCADA_COLS, R.scada_rows())
    n[R.F_RAIN] = R.write_csv(p(R.F_RAIN), R.RAIN_COLS, R.rain_archive_rows(), head=R.RAIN_HEAD, crlf=True)
    n[R.F_RAIN26] = R.write_csv(p(R.F_RAIN26), R.RAIN26_COLS, R.rain26_rows())
    n[R.F_BORE] = R.write_csv(p(R.F_BORE), R.BORE_COLS, R.bore_rows(), head=R.BORE_HEAD, crlf=True)
    n[R.F_ASSETS] = R.write_assets(p(R.F_ASSETS))
    n[R.F_MONITOR] = R.write_csv(p(R.F_MONITOR), R.SMS_COLS, R.sms_rows())
    n[R.F_OUTAGES] = R.write_csv(p(R.F_OUTAGES), R.OUTAGE_COLS, R.outage_rows())
    n[R.F_ICPS] = R.write_csv(p(R.F_ICPS), R.ICP_COLS, R.icp_rows())
    n[R.F_READS] = R.write_csv(p(R.F_READS), R.READ_COLS, R.read_rows())
    n[R.F_ACCOUNTS] = R.write_csv(p(R.F_ACCOUNTS), R.ACCOUNT_COLS, R.account_rows())
    n[R.F_RATING] = R.write_csv(p(R.F_RATING), R.RATING_COLS, R.rating_rows())
    n[R.F_BC] = R.write_csv(p(R.F_BC), R.BC_COLS, R.bc_rows())
    n[R.F_WWTP] = R.write_csv(p(R.F_WWTP), R.WWTP_COLS, R.wwtp_rows())
    n[R.F_WORKS] = R.write_csv(p(R.F_WORKS), R.WORKS_COLS, R.works_rows())
    PP.normalize_ooxml(p(R.F_ASSETS), "Asset Information", "Asset Information", "2019-05-14T03:12:00Z",
                       "2026-10-29T21:05:00Z", excel=True)
    return n


def build(out, quiet=False):
    os.makedirs(out, exist_ok=True)
    n = build_data(out)
    D.write_all(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-58s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
                                             ("%d rows" % n[f]) if f in n else ""))
    return n


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
            zi = zipfile.ZipInfo(f, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-second", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n = build(target)
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = same_g = same_f = same_s = True
    if not a.no_second:
        tmp = tempfile.mkdtemp(prefix="b156_", dir="/tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/98ff0d30-fbdb-590b-8f7a-decafc622b0e/scratchpad")
        try:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "--out", os.path.join(tmp, "target")],
                           check=True, capture_output=True)
            subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, %r); import deliver; deliver.main("
                            "%r, %r, %r, %r)" % (HERE, os.path.join(tmp, "target"), os.path.join(tmp, "golden"),
                                                 os.path.join(tmp, "figures.json"), os.path.join(tmp, "submission.md"))],
                           check=True, capture_output=True)
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
