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
import records as R      # noqa: E402
import tune as TU        # noqa: E402

TASK = os.path.dirname(HERE)


def build_pack(out, e):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["detections"] = P.write_csv(f("detections"), P.DET_COLS, P.detection_rows(e))
    n["traversals"] = P.write_csv(f("traversals"), P.TRAV_COLS, P.traversal_rows(e))
    n["inventory"] = P.write_csv(f("inventory"), P.INV_COLS, P.inventory_rows(e))
    n["crosswalk"] = P.write_csv(f("crosswalk"), P.XW_COLS, P.crosswalk_rows(e))
    n["orders"] = P.write_csv(f("orders"), P.WO_COLS, P.order_rows(e), crlf=True)
    n["pci"] = P.write_csv(f("pci"), P.PCI_COLS, P.pci_rows(e))
    n["winter"] = P.write_csv(f("winter"), P.WINTER_COLS, P.winter_rows(e), crlf=True)
    n["sections"] = P.write_csv(f("sections"), ["section", "section_name", "yard", "district"], P.section_rows(e))
    open(f("sessions"), "w", encoding="utf-8", newline="\n").write(P.sessions_json(e))
    n["sessions"] = sum(1 for s in e["sessions"] if not s.get("unclosed"))
    n["covers"] = P.write_csv(f("covers"), P.COVER_COLS, P.cover_rows(e))
    n["register"] = DC.write_register(f("register"), e)
    n["manifest"] = P.write_csv(f("manifest"), ["file", "source_system", "extracted", "covers", "rows", "notes"],
                                P.manifest_rows(n))
    DC.write_program(f("program"))
    DC.write_sow(f("sow"))
    DC.write_turnback(f("turnback"), e["segs"])
    DC.write_dictionary(f("dictionary"), n)
    PP.normalize_pdf(f("program"), b"D:20270406091512-04'00'", b"D:20270406091512-04'00'")
    PP.normalize_pdf(f("sow"), b"D:20270119141033-05'00'", b"D:20270119141033-05'00'")
    PP.normalize_pdf(f("turnback"), b"D:20270301103207-05'00'", b"D:20270301103207-05'00'")
    PP.normalize_pdf(f("dictionary"), b"D:20270403113845-04'00'", b"D:20270403113845-04'00'")
    PP.normalize_ooxml(f("register"), "Kerbline Vision", "Kerbline Vision", "2027-02-19T16:40:00Z", "2027-04-01T14:12:09Z",
                       excel=True, company="Kerbline Vision, Inc.")
    return n


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def stamp(folder, when=(2027, 4, 9, 10, 15, 0)):
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
    e = R.everything()
    n = build_pack(os.path.join(TASK, "target"), e)
    stamp(os.path.join(TASK, "target"))
    big = max(n.items(), key=lambda t: t[1])
    print("pack: %d files, largest %s (%d rows)" % (len(os.listdir(os.path.join(TASK, "target"))), P.FILES[big[0]], big[1]))
    if a.pack_only:
        return 0
    import csv
    import golden as G
    import metadata as MD
    import writeup as WU
    G.main(os.path.join(TASK, "target"))
    WU.main()
    MD.write(os.path.join(TASK, "metadata.json"), n)
    stamp(os.path.join(TASK, "golden"), (2027, 4, 12, 16, 40, 0))
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
    e2 = R.everything()
    build_pack(os.path.join(TASK, "target"), e2)
    stamp(os.path.join(TASK, "target"))
    G.main(os.path.join(TASK, "target"))
    stamp(os.path.join(TASK, "golden"), (2027, 4, 12, 16, 40, 0))
    same = first == digest(os.path.join(TASK, "target")) and gfirst == digest(os.path.join(TASK, "golden"))
    print("%s  two consecutive builds byte-identical (target and golden)" % ("PASS" if same else "FAIL"))
    if not same:
        return 1
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(os.path.join(TASK, "target"))):
            zi = zipfile.ZipInfo(fn, date_time=(2027, 4, 9, 10, 15, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(TASK, "target", fn), "rb").read())
    print("zip: %s (%s)" % (zp, hashlib.md5(open(zp, "rb").read()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
