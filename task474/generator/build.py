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
RATE_COLS = ["class_group", "fhwa_classes", "description", "calendar_year", "nox_g_per_mile", "basis"]


def build_pack(out, e):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    n["stations"] = P.write_csv(f("stations"), P.STATION_COLS, P.station_rows(e))
    n["dot"] = P.write_csv(f("dot"), P.DOT_COLS, P.dot_rows(e), crlf=True)
    n["consultant"] = P.write_csv(f("consultant"), P.CONS_COLS, P.consultant_rows(e))
    n["gates"] = P.write_csv(f("gates"), P.GATE_COLS, P.gate_rows(e))
    n["fleet"] = P.write_csv(f("fleet"), P.FLEET_COLS, P.fleet_rows(e))
    n["no2"] = P.write_csv(f("no2"), P.NO2_COLS, P.no2_rows(e))
    n["complaints"] = P.write_csv(f("complaints"), P.COMPLAINT_COLS, P.complaint_rows(e), crlf=True)
    desc = {"P": ("1-3", "Passenger vehicles"), "SU": ("4-7", "Single-unit trucks"), "CU": ("8-13", "Combination trucks")}
    n["rates"] = P.write_csv(f("rates"), RATE_COLS, [[c, desc[c][0], desc[c][1], 2026, "%.3f" % W.EF[c],
                                                       "MOVES county-scale run, Harbor County, annual average"]
                                                      for c in W.CLASSES])
    DC.write_rules(f("rules"))
    DC.write_notes(f("notes"), n)
    DC.write_register(f("register"))
    DC.write_links(f("links"))
    DC.write_county(f("county"), P.county_tables(e))
    PP.normalize_pdf(f("rules"), b"D:20260114101533-05'00'", b"D:20260114101533-05'00'")
    for k, who, a, b in (("register", "Traffic Monitoring Section", "2026-07-01T14:02:00Z", "2026-07-01T14:31:12Z"),
                         ("links", "Environmental Planning", "2026-10-22T15:20:00Z", "2026-10-22T15:41:50Z"),
                         ("county", "Traffic Engineering", "2026-09-29T13:05:00Z", "2026-09-29T13:48:27Z")):
        PP.normalize_ooxml(f(k), who, who, a, b, excel=True, company=W.PORT)
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
    e = P.everything()
    n = build_pack(os.path.join(TASK, "target"), e)
    big = max(n.items(), key=lambda t: t[1])
    print("pack: %d files, largest %s (%d rows)" % (len(os.listdir(os.path.join(TASK, "target"))), W.FILES[big[0]],
                                                     big[1]))
    if a.pack_only:
        return 0
    import golden as GD
    import writeup as WU
    import metadata as MD
    gdir = os.path.join(TASK, "golden")
    GD.build(gdir, e)
    WU.write(os.path.join(TASK, "generator", "figures.json"), os.path.join(TASK, "submission.md"))
    MD.write(os.path.join(TASK, "metadata.json"), e, n)
    import checks as C
    ok = C.main(os.path.join(TASK, "target"), gdir, e)
    import verify as V
    ok = V.main(os.path.join(TASK, "target"), gdir) and ok
    if a.fast:
        return 0 if ok else 1
    scratch = os.path.join(TASK, ".rebuild")
    e2 = P.everything.__wrapped__()
    build_pack(os.path.join(scratch, "target"), e2)
    GD.build(os.path.join(scratch, "golden"), e2, target=os.path.join(scratch, "target"),
             figs=os.path.join(scratch, "figures.json"))
    WU.write(os.path.join(scratch, "figures.json"), os.path.join(scratch, "submission.md"))
    MD.write(os.path.join(scratch, "metadata.json"), e2, n)
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
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 26, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(tgt)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
