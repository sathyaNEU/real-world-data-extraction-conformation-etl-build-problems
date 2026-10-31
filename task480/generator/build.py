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


def clear():
    import methods
    import pack
    import sim
    for f in (sim.world, sim.households, sim.vital, pack.parcels, pack.facility_building, methods.load, methods.stock,
              methods.rungs):
        f.cache_clear()


def build_pack(out):
    import books as BK
    import docs as DC
    import pack as P
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    n["roll"] = P.write_csv(f("roll"), P.ROLL_COLS, P.roll_rows())
    n["cos"] = P.write_csv(f("cos"), P.CO_COLS, P.co_rows())
    n["demo"] = P.write_csv(f("demo"), P.DEMO_COLS, P.demo_rows())
    rows = P.bg2020_rows()
    with open(f("bg2020"), "w", newline="", encoding="utf-8") as fh:
        import csv
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(P.BG_COLS)
        w.writerow(P.BG_LABELS)
        w.writerows(rows)
    n["bg2020"] = len(rows)
    n["boundary"] = P.write_csv(f("boundary"), P.BOUNDARY_COLS, P.boundary_rows())
    n["points"] = P.write_csv(f("points"), P.POINT_COLS, P.points_rows(), crlf=False)
    n["births"] = P.write_csv(f("births"), P.BIRTH_COLS, P.births_rows())
    n["deaths"] = P.write_csv(f("deaths"), P.DEATH_COLS, P.deaths_rows())
    n["vintage"] = P.write_csv(f("vintage"), P.VINTAGE_COLS, P.vintage_rows(), crlf=False)
    BK.write_history(f("history"))
    BK.write_gq(f("gq"))
    BK.write_roads(f("roads"))
    DC.write_act(f("act"))
    DC.write_statement(f("method"))
    for k, stamp in (("act", b"D:20251118102200-06'00'"), ("method", b"D:20260803091500-05'00'")):
        PP.normalize_pdf(f(k), stamp, stamp)
    for k, who, created, modified in (("history", W.OFFICE, "2021-09-14T15:02:00Z", "2021-09-30T19:41:12Z"),
                                      ("gq", W.PEOPLE["estimates"][0], "2026-03-02T14:10:00Z", "2026-06-11T20:05:44Z"),
                                      ("roads", "Local Roads Aid Section", "2026-03-27T13:40:00Z", "2026-03-31T18:22:09Z")):
        PP.normalize_ooxml(f(k), who, who, created, modified, excel=True,
                           company=("State " + W.DOT) if k == "roads" else ("State " + W.DEPT))
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
    GD.build(gdir, a.out, figs=os.path.join(HERE, "figures.json"))
    WU.write(os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    MD.write(os.path.join(TASK, "metadata.json"), n, a.out)
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
    MD.write(os.path.join(scratch, "metadata.json"), n, os.path.join(scratch, "target"))
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
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 30, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(a.out, fn), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (len(os.listdir(a.out)),
                                                                    hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
