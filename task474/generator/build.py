"""Build task474: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task474/generator/build.py            everything
    python3 task474/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task474/generator/build.py --pack-only
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
    n["dahs"] = P.write_csv(f("dahs"), P.DAHS_COLS, P.dahs_rows(x))
    n["tickets"] = P.write_csv(f("tickets"), P.TICKET_COLS, P.ticket_rows(x), crlf=True)
    n["invoices"] = P.write_csv(f("invoices"), P.INV_COLS, P.invoice_rows(x))
    n["events"] = P.write_csv(f("events"), P.EVENT_COLS, P.event_rows(x))
    n["ozone"] = P.write_csv(f("ozone"), P.OZONE_COLS, P.ozone_rows(x))
    DC.write_guidelines(f("guidelines"))
    DC.write_terms(f("terms"))
    DC.write_notes(f("notes"), n["dahs"])
    DC.write_units(f("units"))
    DC.write_allowances(f("allowances"), x)
    PP.normalize_pdf(f("guidelines"), b"D:20260112101533-06'00'", b"D:20260112101533-06'00'")
    PP.normalize_pdf(f("terms"), b"D:20241028143011-05'00'", b"D:20241028143011-05'00'")
    PP.normalize_ooxml(f("units"), "Generation Engineering", "Generation Engineering", "2026-06-30T15:02:00Z",
                       "2026-06-30T15:44:31Z", excel=True, company=W.COOP)
    PP.normalize_ooxml(f("allowances"), "Environmental Services", "Environmental Services", "2026-10-01T13:20:00Z",
                       "2026-10-01T13:52:10Z", excel=True, company=W.COOP)
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
    WU.write(os.path.join(TASK, "generator", "figures.json"), os.path.join(TASK, "submission.md"))
    MD.write(os.path.join(TASK, "metadata.json"), x, n)
    import checks as C
    ok = C.main(os.path.join(TASK, "target"), gdir, x)
    import verify as V
    ok = V.main(os.path.join(TASK, "target"), gdir) and ok
    if a.fast:
        return 0 if ok else 1
    scratch = os.path.join(TASK, ".rebuild")
    x2 = P.everything.__wrapped__()
    build_pack(os.path.join(scratch, "target"), x2)
    GD.build(os.path.join(scratch, "golden"), x2, target=os.path.join(scratch, "target"), figs=os.path.join(scratch, "figures.json"))
    WU.write(os.path.join(scratch, "figures.json"), os.path.join(scratch, "submission.md"))
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
            zi = zipfile.ZipInfo(fn, date_time=(2026, 11, 9, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(tgt)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
