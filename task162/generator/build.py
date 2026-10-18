"""Build task162: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte (and deleted), then target.zip cut from the pack.

    python3 task162/generator/build.py              everything
    python3 task162/generator/build.py --out DIR    the pack only, into DIR"""
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
import parallel as PR       # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
SCRATCH = os.environ.get("TASK162_SCRATCH", "/tmp")
PULL_DONE = (2026, 12, 18, 6, 58, 0)                       # the pull's end, Helsinki
MTIME = calendar.timegm((2026, 12, 18, 4, 58, 0, 0, 0, 0))  # the same moment, UTC


class Built:
    pass


def world():
    B = Built()
    B.T = WD.simulate()
    B.reps = WD.realize(B.T)
    B.states = R.old_states(B.T, B.reps)
    B.issues = PR.build(B.T, B.reps)
    R.task_history(B.issues)
    for it in B.issues:
        it["hist"].sort(key=lambda h: h["at"])
    return B


def build_data(out, B):
    p = lambda f: os.path.join(out, f)
    n = {}
    n[R.F_EXPORT] = K.write_csv(p(R.F_EXPORT), R.EXPORT_COLS, R.export_rows(B.states), crlf=True)
    n[R.F_SHARES] = K.write_csv(p(R.F_SHARES), R.SHARE_COLS, R.share_rows(B.T))
    n[R.F_INSTALLS] = K.write_csv(p(R.F_INSTALLS), R.INSTALL_COLS, R.install_rows(B.T))
    n[R.F_PUBLIC] = K.write_csv(p(R.F_PUBLIC), R.PUBLIC_COLS, R.public_rows(B.states, B.T))
    n[R.F_STABILITY] = K.write_csv(p(R.F_STABILITY), R.STABILITY_COLS, R.stability_rows(B.T))
    n[R.F_DASH] = len(R.write_dashboard(p(R.F_DASH), B.states))
    n[R.F_GROUPS] = len(R.write_groups(p(R.F_GROUPS)))
    R.write_rota(p(R.F_ROTA))
    n[R.F_ROTA] = len(R.rota_rows())
    J = R.newtracker(B.issues)
    K.write_json(p(R.F_NEWEXPORT), J, indent=1)
    n[R.F_NEWEXPORT] = len(J["issues"])
    return n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    lead = K.PEOPLE["lead"]
    PP.normalize_ooxml(p(R.F_DASH), "Triage dashboard", "Triage dashboard", "2025-10-06T05:02:00Z",
                       "2026-12-18T04:40:00Z", excel=True, company=K.VENDOR)
    PP.normalize_ooxml(p(R.F_GROUPS), lead, lead, "2026-10-21T09:12:00Z", "2026-10-26T13:48:00Z", excel=True,
                       company=K.VENDOR)
    PP.normalize_ooxml(p(R.F_ROTA), lead, lead, "2026-10-29T12:30:00Z", "2026-11-27T14:06:00Z", excel=True,
                       company=K.VENDOR)


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
            print("  %-46s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
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
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    B, n = build(target)
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = same_g = same_f = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="b162_", dir=SCRATCH)
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
    if r1.returncode or r2.returncode or not (same and same_g and same_f):
        sys.exit(1)


if __name__ == "__main__":
    main()
