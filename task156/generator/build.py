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
import askdata as AD        # noqa: E402
import docs as DC           # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
SCRATCH = os.environ.get("TASK156_SCRATCH", "/tmp")
MTIME = time.mktime((2026, 11, 3, 10, 15, 0, 0, 0, -1))
ZIP_TIME = (2026, 11, 3, 10, 15, 0)


def build_data(out):
    p = lambda f: os.path.join(out, f)
    n = {}
    n[R.F_REG] = R.write_csv(p(R.F_REG), R.REG_COLS, R.register_rows())
    n[R.F_INV] = R.write_csv(p(R.F_INV), R.INV_COLS, R.invitation_rows())
    n[R.F_VOTES] = R.write_csv(p(R.F_VOTES), R.VOTE_COLS, R.vote_rows())
    n[R.F_SITES] = R.write_csv(p(R.F_SITES), R.SITE_COLS, R.site_rows())
    n[R.F_DELEG] = R.write_delegates(p(R.F_DELEG))
    n[R.F_RETURN] = R.write_return(p(R.F_RETURN))
    n[R.F_ROUND] = R.write_round(p(R.F_ROUND))
    n[R.F_REMIT] = R.write_csv(p(R.F_REMIT), AD.REMIT_COLS, AD.remit_rows(), crlf=True)
    n[R.F_DIARY] = R.write_csv(p(R.F_DIARY), AD.DIARY_COLS, AD.diary_rows())
    n[R.F_SIGNIN] = R.write_csv(p(R.F_SIGNIN), AD.SIGNIN_COLS, AD.signin_rows())
    n[R.F_WORKFORCE] = R.write_csv(p(R.F_WORKFORCE), AD.WORKFORCE_COLS, AD.workforce_rows(), crlf=True)
    n[R.F_SURVEY] = R.write_survey(p(R.F_SURVEY))
    org = "Local Services Union, Victoria Branch"
    PP.normalize_ooxml(p(R.F_DELEG), org, org, "2018-06-29T03:40:00Z", "2026-06-30T05:21:00Z",
                       excel=True, title="Delegate register")
    PP.normalize_ooxml(p(R.F_RETURN), org, org, "2026-07-14T23:05:00Z", "2026-10-28T05:21:00Z",
                       excel=True, title="Delegate elections July 2026: return")
    PP.normalize_ooxml(p(R.F_ROUND), org, org, "2026-08-11T00:52:00Z",
                       "2026-10-31T04:07:00Z", excel=True, title="2027 bargaining round")
    PP.normalize_ooxml(p(R.F_SURVEY), org, org, "2024-10-03T02:15:00Z",
                       "2024-10-09T06:48:00Z", excel=True, title="Member survey 2024")
    return n


def build(out, quiet=False):
    os.makedirs(out, exist_ok=True)
    n = build_data(out)
    DC.write_all(out)
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
        build(a.out, quiet=True)
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
        tmp = tempfile.mkdtemp(prefix="b156_", dir=SCRATCH)
        try:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "--out", os.path.join(tmp, "target")],
                           check=True, capture_output=True)
            subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, %r); import deliver; deliver.main("
                            "%r, %r, %r, %r)" % (HERE, os.path.join(tmp, "target"), os.path.join(tmp, "golden"),
                                                 os.path.join(tmp, "figures.json"), os.path.join(tmp, "submission.md"))],
                           check=True, capture_output=True)
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"),
                                                                                    "rb").read()
            same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"),
                                                                                     "rb").read()
            print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f,
                                                                                               same_s))
        finally:
            shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    if r1.returncode or r2.returncode or not (same and same_g and same_f and same_s):
        sys.exit(1)


if __name__ == "__main__":
    main()
