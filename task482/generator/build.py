"""Build task482: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task482/generator/build.py            everything
    python3 task482/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task482/generator/build.py --pack-only
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import asks as A         # noqa: E402
import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2027, 1, 12, 9, 40, 0)
GSTAMP = (2027, 1, 14, 15, 37, 0)
CITY = "Transportation Services"
VENDOR = "Corlund Kiosk Systems"


def build_pack(out):
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    E = A.everything()
    n = P.build_pack(out, E)
    f = lambda k: os.path.join(out, P.FILES[k])
    PP.normalize_pdf(f("notes"), b"D:20270112101507-05'00'", b"D:20270112144033-05'00'")
    PP.normalize_pdf(f("agreement"), b"D:20260504113012-04'00'", b"D:20260511090245-04'00'")
    PP.normalize_pdf(f("report"), b"D:20270113160405-05'00'", b"D:20270114083951-05'00'")
    PP.normalize_ooxml(f("stations"), CITY, "Bike Share Program", "2019-04-02T14:10:00Z", "2026-11-24T19:05:37Z",
                       excel=True, company="City of Wellhaven")
    PP.normalize_ooxml(f("workorders"), VENDOR, "Field Service", "2027-01-08T15:20:00Z", "2027-01-08T15:20:41Z",
                       excel=True, company="Corlund Kiosk Systems Inc.")
    PP.normalize_ooxml(f("register"), VENDOR, "Asset Management", "2023-03-14T13:30:00Z", "2027-01-08T16:12:09Z",
                       excel=True, company="Corlund Kiosk Systems Inc.")
    return n


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def stamp(folder, when=STAMP):
    import time
    t = time.mktime((*when, 0, 0, -1))
    for root, _, files in os.walk(folder):
        for fn in files:
            os.utime(os.path.join(root, fn), (t, t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args()
    n = build_pack(os.path.join(TASK, "target"))
    stamp(os.path.join(TASK, "target"))
    big = max(n.items(), key=lambda t: t[1])
    print("pack: %d files, largest %s (%d rows)" % (len(os.listdir(os.path.join(TASK, "target"))), P.FILES[big[0]],
                                                   big[1]))
    if a.pack_only:
        return 0
    import golden as G
    import metadata as MD
    import writeup as WU
    G.main(os.path.join(TASK, "target"))
    WU.main()
    MD.write(os.path.join(TASK, "metadata.json"), n)
    stamp(os.path.join(TASK, "golden"), GSTAMP)
    rc = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")]).returncode
    rv = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")]).returncode
    if rc or rv:
        print("checks %d, verify %d" % (rc, rv))
        return 1
    if a.fast:
        return 0
    first = digest(os.path.join(TASK, "target"))
    gfirst = digest(os.path.join(TASK, "golden"))
    build_pack(os.path.join(TASK, "target"))
    stamp(os.path.join(TASK, "target"))
    G.main(os.path.join(TASK, "target"))
    stamp(os.path.join(TASK, "golden"), GSTAMP)
    same = first == digest(os.path.join(TASK, "target")) and gfirst == digest(os.path.join(TASK, "golden"))
    print("%s  two consecutive builds byte-identical (target and golden)" % ("PASS" if same else "FAIL"))
    if not same:
        return 1
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(os.path.join(TASK, "target"))):
            zi = zipfile.ZipInfo(fn, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(TASK, "target", fn), "rb").read())
    print("zip: %s (%s)" % (zp, hashlib.md5(open(zp, "rb").read()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
