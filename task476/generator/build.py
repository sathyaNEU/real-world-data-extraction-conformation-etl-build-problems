"""Build task476 (architecture 2): the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task476/generator/build.py            everything
    python3 task476/generator/build.py --fast     one build with the checks, no second build or zip
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


def build_pack(out, x):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    n["mains"] = P.write_csv(f("mains"), P.SEG_COLS, P.seg_rows(x))
    n["schedule"] = P.write_csv(f("schedule"), P.SCHED_COLS, P.sched_rows(x))
    n["finds"] = P.write_csv(f("finds"), P.FIND_COLS, P.find_rows(x))
    n["odor"] = P.write_csv(f("odor"), P.ODOR_COLS, P.odor_rows(x), crlf=True)
    n["repairs"] = P.write_csv(f("repairs"), P.REP_COLS, P.repair_rows(x))
    n["costs"] = P.write_csv(f("costs"), P.COST_COLS, P.cost_rows(x), crlf=True)
    n["closeouts"] = P.write_csv(f("closeouts"), P.CLOSE_COLS, P.close_rows(x), crlf=True)
    n["tickets"] = P.write_csv(f("tickets"), P.TIX_COLS, P.ticket_rows(x))
    n["meters"] = P.write_csv(f("meters"), P.PREM_COLS, P.prem_rows(x))
    DC.write_guidelines(f("guidelines"))
    DC.write_lauf(f("lauf"))
    DC.write_customers(f("customers"), x)
    DC.write_notes(f("notes"), n)
    PP.normalize_pdf(f("guidelines"), b"D:20270111101533-06'00'", b"D:20270111101533-06'00'")
    PP.normalize_pdf(f("lauf"), b"D:20270216142208-06'00'", b"D:20270216142208-06'00'")
    PP.normalize_ooxml(f("customers"), "Customer Accounting", "Customer Accounting", "2027-01-08T15:02:00Z",
                       "2027-01-12T19:44:31Z", excel=True, company=W.UTILITY)
    return n


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args()
    x = P.everything()
    n = build_pack(os.path.join(TASK, "target"), x)
    big = max(n.items(), key=lambda t: t[1])
    print("pack: %d files, largest %s (%d rows)" % (len(os.listdir(os.path.join(TASK, "target"))), W.FILES[big[0]],
                                                     big[1]))
    if a.pack_only:
        return 0
    import golden as GD
    import writeup as WU
    import metadata as MD
    gdir = os.path.join(TASK, "golden")
    GD.build(gdir, x)
    WU.write(os.path.join(TASK, "submission.md"), x)
    MD.write(os.path.join(TASK, "metadata.json"), x, n)
    import checks as C
    ok = C.main(os.path.join(TASK, "target"), gdir, x)
    import verify as V
    ok = V.main(os.path.join(TASK, "target"), gdir) and ok
    if a.fast:
        return 0 if ok else 1
    scratch = os.path.join(TASK, ".rebuild")
    x2 = P.everything()
    build_pack(os.path.join(scratch, "target"), x2)
    GD.build(os.path.join(scratch, "golden"), x2)
    WU.write(os.path.join(scratch, "submission.md"), x2)
    MD.write(os.path.join(scratch, "metadata.json"), x2, n)
    same = digest(os.path.join(TASK, "target")) == digest(os.path.join(scratch, "target")) and \
        digest(gdir) == digest(os.path.join(scratch, "golden")) and \
        open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(scratch, "submission.md"), "rb").read() and \
        open(os.path.join(TASK, "metadata.json"), "rb").read() == open(os.path.join(scratch, "metadata.json"), "rb").read()
    shutil.rmtree(scratch)
    print("two builds byte-identical: %s" % same)
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    tgt = os.path.join(TASK, "target")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(tgt)):
            zi = zipfile.ZipInfo(fn, date_time=(2027, 3, 16, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(tgt)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
