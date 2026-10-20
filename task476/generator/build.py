"""Build task476: the pack into <task>/target, the golden into <task>/golden, metadata.json, submission.md and
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
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    for key, per in (("tract18", 1), ("tract23", 2)):
        cols, lab, rows = P.acs_tract(x, per)
        n[key] = P.write_csv(f(key), cols, rows, crlf=True, extra_header=lab)
    for key, per in (("bg18", 1), ("bg23", 2)):
        cols, lab, rows = P.acs_bg(x, per)
        n[key] = P.write_csv(f(key), cols, rows, crlf=True, extra_header=lab)
    cols, lab, rows = P.pl2010_rows(x)
    n["pl2010"] = P.write_csv(f("pl2010"), cols, rows, crlf=True, extra_header=lab)
    n["tractrel"] = P.write_csv(f("tractrel"), P.TRACTREL_COLS, P.tractrel_rows(x), delim="|", crlf=True)
    n["blockrel"] = P.write_csv(f("blockrel"), P.BLOCKREL_COLS, P.blockrel_rows(x), delim="|", crlf=True)
    n["parcels"] = P.write_csv(f("parcels"), P.PARCEL_COLS, P.parcel_rows(x))
    crows, erows = P.case_rows(x)
    n["cases"] = P.write_csv(f("cases"), P.CASE_COLS, crows)
    n["events"] = P.write_csv(f("events"), P.EVENT_COLS, erows)
    DC.write_guidelines(f("guidelines"))
    DC.write_candidates(f("neighbourhoods"), x)
    DC.write_journal(f("payments"), x)
    DC.write_notes(f("notes"), x, n["parcels"], n["cases"], n["events"])
    import postprocess as PP
    PP.normalize_pdf(f("guidelines"), b"D:20270104093312-06'00'", b"D:20270104093312-06'00'")
    PP.normalize_ooxml(f("neighbourhoods"), W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][0], "2027-02-22T15:04:00Z",
                       "2027-03-15T16:41:09Z", excel=True, company="City of Carrow")
    PP.normalize_ooxml(f("payments"), "NSF Finance", W.PEOPLE["manager"][0], "2022-07-05T14:20:00Z",
                       "2027-03-15T13:12:37Z", excel=True, company="City of Carrow")
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
            zi = zipfile.ZipInfo(fn, date_time=(2027, 3, 15, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(tgt)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
