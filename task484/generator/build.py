"""Build task484: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task484/generator/build.py            everything
    python3 task484/generator/build.py --fast     one build with the checks, no second build or zip
    python3 task484/generator/build.py --pack-only
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


def acs_rates(e):
    import numpy as np
    rng = np.random.default_rng(W.SEED + 30)
    return {c: float(v["stock_occ"] + rng.normal(0, .0025)) for c, v in sorted(e["x"].items())}


def build_pack(out, e):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    n["metro"] = P.write_csv(f("metro"), P.METRO_COLS, P.metro_rows(e), crlf=True)
    n["civic"] = P.write_csv(f("civic"), P.CIVIC_COLS, P.civic_rows(e))
    n["utility"] = P.write_csv(f("utility"), P.UTIL_COLS, P.util_rows(e))
    n["demo"] = P.write_csv(f("demo"), P.DEMO_COLS, P.demo_rows(e))
    n["gq"] = P.write_csv(f("gq"), P.GQ_COLS, P.gq_rows(e))
    n["schools"] = P.write_csv(f("schools"), P.SCHOOL_COLS, P.school_rows(e))
    n["voters"] = P.write_csv(f("voters"), P.VOTER_COLS, P.voter_rows(e))
    DC.write_rules(f("rules"))
    DC.write_notes(f("notes"), n)
    DC.write_census(f("census"), e["x"])
    DC.write_acs(f("acs"), e["x"], acs_rates(e))
    DC.write_county(f("county"), P.county_rows(e))
    DC.write_codes(f("codes"))
    PP.normalize_pdf(f("rules"), b"D:20260217101533-05'00'", b"D:20260217101533-05'00'")
    for k, who, a, b in (("census", "Population and Demographics Unit", "2023-05-25T14:02:00Z", "2023-05-25T14:31:12Z"),
                         ("acs", "Population and Demographics Unit", "2025-12-15T15:20:00Z", "2025-12-15T15:41:50Z"),
                         ("county", "County Building Department", "2026-10-02T13:05:00Z", "2026-10-02T13:48:27Z"),
                         ("codes", "Housing Data Program", "2025-01-08T16:10:00Z", "2025-01-08T16:22:41Z")):
        PP.normalize_ooxml(f(k), who, who, a, b, excel=True, company=W.OFFICE)
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
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 14, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(tgt)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
