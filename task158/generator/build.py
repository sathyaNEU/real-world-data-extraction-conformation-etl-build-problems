"""Build task158: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte, then target.zip cut from the pack.

    python3 task158/generator/build.py              everything
    python3 task158/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2026, 12, 7, 7, 47, 0)                        # just after the pull log's last line, Amsterdam time
MTIME = calendar.timegm((2026, 12, 7, 6, 47, 0, 0, 0, 0))  # the same moment, UTC


class Built:
    pass


def world():
    B = Built()
    B.W = WD.simulate()
    B.NODES = WD.nodes(np.random.default_rng(K.SEED + 29))
    B.M = WD.center_ask_a(WD.maintenance(B.NODES), B.NODES)
    B.A = WD.acceptance()
    B.S = R.shape(B.W, B.NODES, B.M)
    B.INC = WD.incidents()
    return B


def build_data(out, B):
    p = lambda f: os.path.join(out, f)
    W, S, M, A = B.W, B.S, B.M, B.A
    n = {}
    n[R.F_ROLLUP] = K.write_csv(p(R.F_ROLLUP), R.ROLLUP_COLS, R.rollup_rows(W, S))
    n[R.F_BILLING] = K.write_csv(p(R.F_BILLING), R.BILLING_COLS, R.billing_rows(W))
    n[R.F_NODES] = K.write_csv(p(R.F_NODES), R.NODE_COLS, R.node_rows(B.NODES))
    n[R.F_JOBS] = K.write_jsonl(p(R.F_JOBS), R.job_objs(M))
    n[R.F_CONSOLE] = K.write_csv(p(R.F_CONSOLE), R.CONSOLE_COLS, R.console_rows(M))
    n[R.F_BURN] = K.write_csv(p(R.F_BURN), R.BURN_COLS, R.burn_rows(A))
    n[R.F_FABRIC] = K.write_csv(p(R.F_FABRIC), R.FABRIC_COLS, R.fabric_rows(A))
    n[R.F_HANDOVER] = K.write_csv(p(R.F_HANDOVER), R.HANDOVER_COLS, R.handover_rows(A))
    n[R.F_INCIDENTS] = K.write_csv(p(R.F_INCIDENTS), R.INCIDENT_COLS, R.incident_rows(B.INC))
    n[R.F_SPEC] = K.write_csv(p(R.F_SPEC), R.SPEC_COLS, R.spec_rows())
    R.write_intake(p(R.F_INTAKE), W)
    R.write_plan(p(R.F_PLAN))
    R.write_ledger(p(R.F_LEDGER), W)
    return n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(R.F_INTAKE), K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-11-02T09:15:00Z",
                       "2026-11-30T16:48:00Z", excel=True, company=K.ORG_LEGAL)
    PP.normalize_ooxml(p(R.F_PLAN), K.PEOPLE["capacity_lead"], K.PEOPLE["capacity_lead"], "2026-10-05T08:30:00Z",
                       "2026-12-01T10:05:00Z", excel=True, company=K.ORG_LEGAL)
    PP.normalize_ooxml(p(R.F_LEDGER), K.PEOPLE["reports_pm"], K.PEOPLE["reports_pm"], "2026-09-09T13:20:00Z",
                       "2026-12-04T15:31:00Z", excel=True, company=K.ORG_LEGAL)


def build(out, quiet=False, B=None):
    os.makedirs(out, exist_ok=True)
    B = B or world()
    n = build_data(out, B)
    normalize(out)
    CL = C.closeout(out)
    DOC.write_closeout(out, CL)
    DOC.write_policy(out)
    DOC.write_schedule(out)
    DOC.write_lease(out)
    DOC.write_notes(out)
    log_rows = [(R.F_ROLLUP, n[R.F_ROLLUP], "2026-01-01T00:00Z..2026-12-06T23:00Z"),
                (R.F_BILLING, n[R.F_BILLING], "2026-09-01..2026-12-06 (Europe/Amsterdam)"),
                (R.F_JOBS, n[R.F_JOBS], "2026-10-26T00:00Z..2026-12-07T00:00Z"),
                (R.F_CONSOLE, n[R.F_CONSOLE], "2026-10-26..2026-12-06 (Europe/Amsterdam)"),
                (R.F_NODES, n[R.F_NODES], "as of 2026-12-06"),
                (R.F_INCIDENTS, n[R.F_INCIDENTS], "2026-07-01..2026-12-06"),
                (R.F_SPEC, n[R.F_SPEC], "as of 2026-12-07"),
                (R.F_BURN, n[R.F_BURN], "provider export, received 2026-12-04"),
                (R.F_FABRIC, n[R.F_FABRIC], "provider export, received 2026-12-04"),
                (R.F_HANDOVER, n[R.F_HANDOVER], "provider export, received 2026-12-04"),
                (R.F_INTAKE, None, "SharePoint capacity/intake"), (R.F_PLAN, None, "SharePoint capacity/plans"),
                (R.F_LEDGER, None, "report service export 2026-12-04"), (DOC.F_CLOSEOUT, None, "SharePoint capacity/close-outs"),
                (DOC.F_POLICY, None, "SharePoint capacity/policy"), (DOC.F_SCHEDULE, None, "contracts/noordermeer"),
                (DOC.F_LEASE, None, "contracts/noordermeer"), (DOC.F_NOTES, None, "")]
    DOC.write_log(out, log_rows)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-58s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
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
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    import subprocess
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    B, n = build(target)
    if a.pack_only:
        return
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    tmp = tempfile.mkdtemp(prefix="b158_", dir=TASK)
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
    print("zip", z, os.path.getsize(z), "bytes")
    sys.exit(0 if (r1.returncode == 0 and r2.returncode == 0 and same and same_g and same_f and same_s) else 1)


if __name__ == "__main__":
    main()
