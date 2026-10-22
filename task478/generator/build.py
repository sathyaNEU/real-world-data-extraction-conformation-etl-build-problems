"""Build task478: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task478/generator/build.py            everything
    python3 task478/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task478/generator/build.py --pack-only
"""
import argparse
import hashlib
import os
import shutil
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)


def build_pack(out, e=None):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    e, n = P.build_pack(out, e)
    f = lambda k: os.path.join(out, P.FILES[k])
    n["stations"] = len(W.CODES)
    n["plazas"] = sum(1 for p in W.PLAZAS if p[6] is None)
    n["pavement"] = 2 * len(W.CODES)
    n["bridges"] = sum(1 for _ in open(f("bridges"), encoding="utf-8")) - 1
    DC.write_program(f("program"))
    DC.write_dictionary(f("dictionary"), n)
    DC.write_schedule(f("schedule"))
    PP.normalize_pdf(f("program"), b"D:20270212091512-05'00'", b"D:20270212091512-05'00'")
    PP.normalize_pdf(f("dictionary"), b"D:20270209163205-05'00'", b"D:20270209163205-05'00'")
    PP.normalize_pdf(f("schedule"), b"D:20241118110430-05'00'", b"D:20241118110430-05'00'")
    PP.normalize_ooxml(f("tickets"), "CTPA Enforcement", "CTPA Enforcement", "2027-01-04T14:20:00Z",
                       "2027-02-06T16:05:44Z", excel=True, company=PP.COMPANY)
    PP.normalize_ooxml(f("pavement"), "CTPA Pavement Management", "CTPA Pavement Management", "2026-07-20T13:11:00Z",
                       "2026-07-22T20:42:19Z", excel=True, company=PP.COMPANY)
    return e, n


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def stamp(folder, when=(2027, 2, 12, 10, 15, 0)):
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
    e, n = build_pack(os.path.join(TASK, "target"))
    stamp(os.path.join(TASK, "target"))
    big = max(((k, v) for k, v in n.items() if isinstance(v, int)), key=lambda t: t[1])
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
    stamp(os.path.join(TASK, "golden"), (2027, 2, 12, 14, 47, 0))
    import subprocess
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
    stamp(os.path.join(TASK, "golden"), (2027, 2, 12, 14, 47, 0))
    same = first == digest(os.path.join(TASK, "target")) and gfirst == digest(os.path.join(TASK, "golden"))
    print("%s  two consecutive builds byte-identical (target and golden)" % ("PASS" if same else "FAIL"))
    if not same:
        return 1
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(os.path.join(TASK, "target"))):
            zi = zipfile.ZipInfo(fn, date_time=(2027, 2, 12, 10, 15, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(TASK, "target", fn), "rb").read())
    print("zip: %s (%s)" % (zp, hashlib.md5(open(zp, "rb").read()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
