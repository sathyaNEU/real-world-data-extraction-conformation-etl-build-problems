"""Build task166: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte (and deleted), then target.zip cut from the pack.

    python3 task166/generator/build.py              everything
    python3 task166/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import swaps as SW          # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
SCRATCH = os.environ.get("TASK166_SCRATCH", "/tmp")
PULL_DONE = (2026, 12, 3, 16, 48, 0)                       # the pull's end, Pittsburgh (EST)
MTIME = calendar.timegm((2026, 12, 3, 21, 48, 0, 0, 0, 0))  # the same moment, UTC


def world():
    W = WD.simulate()
    R.prepare(W)
    S = SW.build()
    return W, S


def build_data(out, W, S):
    p = lambda f: os.path.join(out, f)
    n = {}
    leg, new, xref = R.servicing_rows(W)
    n[R.F_LEGACY] = K.write_csv(p(R.F_LEGACY), R.LEGACY_COLS, leg, crlf=True) - 1     # the trailer is not a loan
    n[R.F_SERV] = K.write_csv(p(R.F_SERV), R.SERV_COLS, new)
    n[R.F_XREF] = K.write_csv(p(R.F_XREF), R.XREF_COLS, xref)
    n[R.F_RATES] = K.write_csv(p(R.F_RATES), R.RATE_COLS, R.rate_rows(W))
    n[R.F_CRE] = K.write_csv(p(R.F_CRE), R.CRE_COLS, R.cre_rows(W))
    n[R.F_STMT] = K.write_csv(p(R.F_STMT), R.STMT_COLS, R.stmt_rows(W))
    n[R.F_CUSTODY] = K.write_csv(p(R.F_CUSTODY), R.CUSTODY_COLS, R.custody_rows(W))
    n[R.F_FACTORS] = K.write_csv(p(R.F_FACTORS), R.FACTOR_COLS, R.factor_rows(W))
    n[R.F_AUTO] = K.write_csv(p(R.F_AUTO), R.AUTO_COLS, R.auto_rows(W))
    n[R.F_ROLL] = K.write_csv(p(R.F_ROLL), R.ROLL_COLS, R.roll_rows(W))
    n[R.F_SCHED] = K.write_csv(p(R.F_SCHED), R.SCHED_COLS, R.sched_rows(S))
    n[R.F_CLEAR] = K.write_csv(p(R.F_CLEAR), R.CLEAR_COLS, R.clear_rows(S))
    n[R.F_LOCKS] = K.write_csv(p(R.F_LOCKS), R.LOCK_COLS, R.lock_rows(W))
    return n


CONTAINERS = [
    (DOC.F_LOG, "Jeff Guzman", "Jeff Guzman", "2015-01-12T15:20:00Z", "2026-12-02T19:41:00Z", True),
    (DOC.F_PLAN, "Sheri Roberts", "Sheri Roberts", "2026-09-08T13:05:00Z", "2026-09-22T20:18:00Z", True),
    (DOC.F_REGISTER, "Treasury Reporting", "Treasury Reporting", "2026-12-01T11:02:00Z", "2026-12-01T11:02:00Z", True),
    (DOC.F_NMD, "Sheri Roberts", "Sheri Roberts", "2026-07-20T14:31:00Z", "2026-08-14T18:52:00Z", True),
]
PDFS = [(DOC.F_POLICY, b"D:20260325101400-04'00'", b"D:20260325101400-04'00'"),
        (DOC.F_ALM, b"D:20261014162000-04'00'", b"D:20261014162000-04'00'")]


def normalize(out):
    for f, cr, lb, c, m, xl in CONTAINERS:
        PP.normalize_ooxml(os.path.join(out, f), cr, lb, c, m, excel=xl, company=K.BANK)
    for f, c, m in PDFS:
        PP.normalize_pdf(os.path.join(out, f), c, m)


def build(out, quiet=False):
    os.makedirs(out, exist_ok=True)
    W, S = world()
    n = build_data(out, W, S)
    DOC.write_all(out, W, S, n)
    normalize(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-46s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
                                              ("%d rows" % n[f]) if f in n else ""))
    return W, S, n


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
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    W, S, n = build(target)
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"))
    import metadata
    metadata.write(TASK, n)
    r1 = r2 = None
    if not a.no_checks:
        r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
        r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = same_g = same_f = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="b166_", dir=SCRATCH)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"))
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"),
                                                                                   "rb").read()
            print("rebuild byte-identical: target %s, golden %s, figures %s" % (same, same_g, same_f))
        finally:
            shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    bad = (r1 is not None and r1.returncode) or (r2 is not None and r2.returncode)
    if bad or not (same and same_g and same_f):
        sys.exit(1)


if __name__ == "__main__":
    main()
