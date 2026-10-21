"""Build task480: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task480/generator/build.py            everything
    python3 task480/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task480/generator/build.py --pack-only
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

import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
OWNER = "%s %s" % (W.STATE_AGENCY, W.DIVISION)


def clear():
    import fleet
    import methods
    import pilot
    import stations
    for f in (fleet.build, fleet.county, fleet._models, stations.register, pilot.vouchers, pilot.invoices, methods.load, methods.readings,
              methods.eligible, methods.golden, methods.routes):
        f.cache_clear()


def build_pack(out):
    import books as BK
    import docs as DC
    import pack as P
    import pilot as PL
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    n["registrations"] = P.write_csv(f("registrations"), P.REG_COLS, P.registration_rows())
    n["inspections"] = P.write_csv(f("inspections"), P.TEST_COLS, P.test_rows())
    n["counties"] = P.write_csv(f("counties"), P.COUNTY_COLS, P.county_rows())
    n["body"] = P.write_csv(f("body"), P.BODY_COLS, P.body_rows())
    n["invoices"] = P.write_csv(f("invoices"), PL.INVOICE_COLS, PL.invoices())
    n["hpms"] = P.write_csv(f("hpms"), P.VMT_COLS, P.vmt_rows())
    n["fuel"] = P.write_csv(f("fuel"), P.FUEL_COLS, P.fuel_rows())
    n["population"] = P.write_csv(f("population"), P.POP_COLS, P.pop_rows())
    n["stations"] = BK.write_stations(f("stations"))
    BK.write_rates(f("rates"))
    n["vouchers"] = BK.write_vouchers(f("vouchers"))
    DC.write_guidelines(f("guidelines"))
    DC.write_closeout(f("closeout"), dict(letters="11,206", apps="963", approved="771", dec_title="94", dec_my="57",
                                          dec_two="11"))
    DC.write_annual(f("annual"))
    DC.write_dictionary(f("dictionary"))
    for k, stamp in (("guidelines", b"D:20260908093000-05'00'"), ("closeout", b"D:20260210141500-06'00'"),
                     ("annual", b"D:20250320101000-05'00'"), ("dictionary", b"D:20260914160500-05'00'")):
        PP.normalize_pdf(f(k), stamp, stamp)
    for k, who, created, modified in (("stations", "EIP Station Licensing", "2026-06-30T14:02:00Z", "2026-06-30T14:19:37Z"),
                                      ("rates", W.SECTION, "2026-04-14T19:40:00Z", "2026-04-15T13:05:12Z"),
                                      ("vouchers", "VRP Program Office", "2026-01-20T15:11:00Z", "2026-01-20T15:26:44Z")):
        PP.normalize_ooxml(f(k), who, who, created, modified, excel=True, company="State " + OWNER)
    clear()
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
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    a = ap.parse_args()
    n = build_pack(a.out)
    big = max(n.items(), key=lambda t: t[1])
    print("pack: %d files, largest %s (%d rows)" % (len(os.listdir(a.out)), W.FILES[big[0]], big[1]))
    if a.pack_only:
        return 0
    import golden as GD
    import metadata as MD
    import writeup as WU
    gdir = os.path.join(TASK, "golden")
    GD.build(gdir, a.out)
    WU.write(os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    MD.write(os.path.join(TASK, "metadata.json"), n)
    import checks as C
    ok = C.main(a.out, gdir)
    import verify as V
    ok = V.main(a.out, gdir) and ok
    if a.fast:
        return 0 if ok else 1
    scratch = os.path.join(TASK, ".rebuild")
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    clear()
    build_pack(os.path.join(scratch, "target"))
    GD.build(os.path.join(scratch, "golden"), os.path.join(scratch, "target"), figs=os.path.join(scratch, "figures.json"))
    WU.write(os.path.join(scratch, "figures.json"), os.path.join(scratch, "submission.md"))
    MD.write(os.path.join(scratch, "metadata.json"), n)
    same = digest(a.out) == digest(os.path.join(scratch, "target")) and \
        digest(gdir) == digest(os.path.join(scratch, "golden")) and \
        open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(scratch, "submission.md"), "rb").read() and \
        open(os.path.join(TASK, "metadata.json"), "rb").read() == open(os.path.join(scratch, "metadata.json"), "rb").read()
    shutil.rmtree(scratch)
    print("two builds byte-identical: %s" % same)
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(a.out)):
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 26, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(a.out, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(a.out)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
