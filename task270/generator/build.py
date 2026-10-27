"""Build task270: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks, the independent verifier and the cracker, then a second
full build into a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task270/generator/build.py              everything
    python3 task270/generator/build.py --scratch    the pack and goldens only, into the folders the environment names"""
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
import common as K          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = time.mktime((2027, 1, 27, 9, 20, 0, 0, 0, -1))   # the morning the paper's figures were drawn
PDF_STAMPS = {"statin_adherence_support_service_specification_2027-28.pdf": (b"D:20261116143000+00'00'",
                                                                            b"D:20261116151200+00'00'"),
              "compliance_aids_prescribing_and_supply_guidance_2025.pdf": (b"D:20250602101500+01'00'",
                                                                           b"D:20250602104000+01'00'"),
              "community_pharmacy_contractual_framework_summary_2024-26.pdf": (b"D:20240930160500+01'00'",
                                                                               b"D:20240930160500+01'00'")}


def build_pack(out, golden, figs, sub):
    import deliver
    import docs
    import pilot
    import postprocess as PP
    import records
    import world
    os.makedirs(out, exist_ok=True)
    pracs, pharms, pts = world.build()
    n = records.write_all(pracs, pharms, pts)
    pilots, moved, ev = pilot.build(pharms, pts)
    n.update(pilot.write_all(pilots, moved, ev, pharms))
    docs.write_all()
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(records.F_SYNARIS), "IVHDS Extracts", "IVHDS Extracts", "2027-01-11T06:40:00Z",
                       "2027-01-11T06:40:00Z", excel=True, company=K.DATA_SERVICE)
    PP.normalize_ooxml(p(pilot.F_STATEMENTS), "Primary Care Payments", "Primary Care Payments", "2025-12-04T09:30:00Z",
                       "2027-01-08T16:05:00Z", excel=True, company=K.FEDERATION)
    for f, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(p(f), c, m)
    for f in os.listdir(out):
        os.utime(p(f), (MTIME, MTIME))
    deliver.main(out, golden, figs, sub)
    return n


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip():
    target = os.path.join(TASK, "target")
    zpath = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 1, 27, 9, 20, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", action="store_true")
    a = ap.parse_args()
    if a.scratch:
        root = os.path.dirname(K.TARGET)
        build_pack(K.TARGET, K.GOLDEN, os.path.join(root, "figures.json"), os.path.join(root, "submission.md"))
        return 0
    for d in (K.TARGET, K.GOLDEN):
        if os.path.isdir(d):
            shutil.rmtree(d)
    n = build_pack(K.TARGET, K.GOLDEN, os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    for f in sorted(os.listdir(K.TARGET)):
        print("  %-66s %10d bytes %s" % (f, os.path.getsize(os.path.join(K.TARGET, f)),
                                         ("%d rows" % n[f]) if f in n else ""))
    import metadata
    metadata.write(TASK)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")], capture_output=True, text=True)
    print("\n".join(l for l in r1.stdout.splitlines() if not l.startswith("PASS")))
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")])
    r3 = subprocess.run([sys.executable, os.path.join(HERE, "cracker.py")], capture_output=True, text=True)
    print(r3.stdout.splitlines()[-1])
    tmp = tempfile.mkdtemp(prefix="b270_", dir=TASK)
    try:
        env = dict(os.environ, TASK270_TARGET=os.path.join(tmp, "target"), TASK270_GOLDEN=os.path.join(tmp, "golden"))
        subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "--scratch"], env=env, check=True)
        same = digest(K.TARGET) == digest(os.path.join(tmp, "target"))
        same_g = digest(K.GOLDEN) == digest(os.path.join(tmp, "golden"))
        same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
        same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"), "rb").read()
        print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
    finally:
        shutil.rmtree(tmp)
    z = cut_zip()
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    return 1 if (r1.returncode or r2.returncode or r3.returncode or not (same and same_g and same_f and same_s)) else 0


if __name__ == "__main__":
    sys.exit(main())
