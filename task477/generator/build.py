"""Build task477: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task477/generator/build.py            everything
    python3 task477/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task477/generator/build.py --pack-only
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
    n["qcew_a"] = P.write_csv(f("qcew_a"), P.OLD, P.qcew_rows(x, "a"))
    n["qcew_b"] = P.write_csv(f("qcew_b"), P.NEW, P.qcew_rows(x, "b"))
    n["qcew_c"] = P.write_csv(f("qcew_c"), P.NEW, P.qcew_rows(x, "c"))
    ar = DC.area_rows()
    n["areas"] = P.write_csv(f("areas"), ar[0], ar[1:])
    ir = DC.industry_rows(x)
    n["industries"] = P.write_csv(f("industries"), ir[0], ir[1:])
    n["exits"] = P.write_csv(f("exits"), P.EXIT_COLS, P.exit_rows(x), crlf=True)
    n["wages"] = P.write_csv(f("wages"), P.WAGE_COLS, P.wage_rows(x))
    n["employers"] = P.write_csv(f("employers"), P.EMP_COLS, P.employer_rows(x))
    n["peo"] = P.write_csv(f("peo"), P.PEO_COLS, P.peo_rows(x))
    n["ita"] = P.write_csv(f("ita"), P.LEDGER_COLS, P.ledger_rows(x), crlf=True)
    n["register"] = P.write_csv(f("register"), P.REG_COLS, P.register_rows(x), crlf=True)
    DC.write_guidelines(f("guidelines"))
    DC.write_layout(f("layout"), n)
    DC.write_manual(f("manual"))
    DC.write_etpl(f("etpl"), x)
    DC.write_projections(f("projections"), x)
    DC.write_oews(f("oews"), x)
    PP.normalize_pdf(f("guidelines"), b"D:20260803091214-05'00'", b"D:20260803091214-05'00'")
    PP.normalize_pdf(f("layout"), b"D:20260611140342-05'00'", b"D:20260611140342-05'00'")
    PP.normalize_pdf(f("manual"), b"D:20250219103055-05'00'", b"D:20250219103055-05'00'")
    PP.normalize_ooxml(f("etpl"), "ETPL Administrator", "ETPL Administrator", "2026-06-30T13:20:00Z",
                       "2026-06-30T13:41:12Z", excel=True, company="State Department of Labor")
    PP.normalize_ooxml(f("projections"), "LMI Projections Unit", "LMI Projections Unit", "2026-05-12T15:02:00Z",
                       "2026-05-19T19:44:31Z", excel=True, company="State Department of Labor")
    PP.normalize_ooxml(f("oews"), "LMI OEWS Unit", "LMI OEWS Unit", "2026-04-02T12:10:00Z",
                       "2026-04-02T12:31:09Z", excel=True, company="State Department of Labor")
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
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 14, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(tgt)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
