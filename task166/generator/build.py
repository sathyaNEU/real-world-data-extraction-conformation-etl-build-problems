"""Build task166: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte (and deleted), then target.zip cut from the pack.

    python3 task166/generator/build.py              everything
    python3 task166/generator/build.py --out DIR    the pack only, into DIR
    python3 task166/generator/build.py --pack       the pack into target/ only"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import onboarding as OB     # noqa: E402
import postprocess as PP    # noqa: E402
import records as RC        # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
SCRATCH = os.environ.get("TASK166_SCRATCH", os.path.join(TASK, ".scratch"))
PULL_DONE = (2026, 10, 20, 16, 30, 0)                       # the request's pack assembled, Denver (MDT)
MTIME = calendar.timegm((2026, 10, 20, 22, 30, 0, 0, 0, 0))  # the same moment, UTC


def normalize(out):
    PP.normalize_ooxml(os.path.join(out, RC.F_REG), "Revenue Operations", "Revenue Operations", "2026-10-01T13:15:00Z",
                       "2026-10-01T13:15:00Z", excel=True, company=K.COMPANY_LEGAL)
    PP.normalize_ooxml(os.path.join(out, RC.F_SPEND), K.PEOPLE["mops"], K.PEOPLE["mops"], "2019-03-04T16:20:00Z",
                       "2026-10-01T15:45:00Z", excel=True, company=K.COMPANY_LEGAL)
    PP.normalize_docx(os.path.join(out, DOC.F_MEMO), K.PEOPLE["vp"], K.PEOPLE["vp"], "2026-10-19T20:41:00Z",
                      "2026-10-20T22:05:00Z", 3, 38, seed=166, title="Where the 2027 onboarding pod goes", company=K.COMPANY_LEGAL)
    for f, c, m in ((DOC.F_BASIS, b"D:20261002110000-06'00'", b"D:20261002110000-06'00'"),
                    (DOC.F_DECK, b"D:20230313171500-06'00'", b"D:20230313171500-06'00'"),
                    (DOC.F_DICT, b"D:20261002142000-06'00'", b"D:20261002142000-06'00'")):
        PP.normalize_pdf(os.path.join(out, f), c, m)


def build(out, quiet=False):
    os.makedirs(out, exist_ok=True)
    W = WD.simulate()
    B = RC.build(W)
    O = OB.build(B)
    n = RC.write_all(out, B)
    n.update(OB.write_all(out, O))
    DOC.write_all(out, B, n)
    normalize(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-52s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if n.get(f) else ""))
    return W, B, O, n


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
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    W, B, O, n = build(target)
    if a.pack:
        return
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
        os.makedirs(SCRATCH, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix="b166_", dir=SCRATCH)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"))
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
            print("rebuild byte-identical: target %s, golden %s, figures %s" % (same, same_g, same_f))
        finally:
            shutil.rmtree(tmp)
            if os.path.isdir(SCRATCH) and not os.listdir(SCRATCH):
                os.rmdir(SCRATCH)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    bad = (r1 is not None and r1.returncode) or (r2 is not None and r2.returncode)
    if bad or not (same and same_g and same_f):
        sys.exit(1)


if __name__ == "__main__":
    main()
