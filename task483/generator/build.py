"""Build task483: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task483/generator/build.py            everything
    python3 task483/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task483/generator/build.py --pack-only
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

import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2026, 10, 16, 10, 20, 0)
GSTAMP = (2026, 11, 6, 16, 5, 0)


def build_pack(out):
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    n = P.build_pack(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    PP.normalize_pdf(f("standard"), b"D:20260618143012-06'00'", b"D:20260622091544-06'00'")
    PP.normalize_pdf(f("notes"), b"D:20260409101225-06'00'", b"D:20260414080510-06'00'")
    PP.normalize_pdf(f("coa"), b"D:20240611133047-06'00'", b"D:20240701090212-06'00'")
    PP.normalize_pdf(f("demand"), b"D:20260210154401-07'00'", b"D:20260212110936-07'00'")
    PP.normalize_ooxml(f("release24"), W.CENTER, W.CENTER, "2025-03-28T15:10:00Z", "2025-04-15T13:02:44Z", excel=True,
                       company=W.CENTER)
    PP.normalize_ooxml(f("inventory"), "Office of Academic Affairs", "Office of Academic Affairs",
                       "2025-05-12T16:40:00Z", "2025-08-19T20:11:32Z", excel=True)
    PP.normalize_ooxml(f("older"), "Institutional Research", "Institutional Research", "2025-07-21T14:05:00Z",
                       "2025-07-21T14:05:00Z", excel=True)
    PP.normalize_ooxml(f("register"), "Business Office", "Business Office", "2023-06-05T15:30:00Z",
                       "2026-07-09T17:48:20Z", excel=True)
    PP.normalize_ooxml(f("oews"), "Labor Market Information", "Labor Market Information", "2026-03-30T14:00:00Z",
                       "2026-04-02T15:26:51Z", excel=True, company="State Department of Workforce Services")
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
