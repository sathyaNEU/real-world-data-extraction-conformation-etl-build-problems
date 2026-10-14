"""Build task452 (architecture 2): the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task452/generator/build.py              everything
    python3 task452/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import docs as DC           # noqa: E402
import interp as I          # noqa: E402
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2026, 5, 22, 17, 25, tzinfo=LOCAL)        # the folder as the laboratory assembled it


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    pts = I.points()
    qc, adj = I.qc_campaign(pts)
    n = {}
    n["main"] = P.write_main(pts, f("main"))
    n["qc"] = P.write_qc(qc, f("qc"))
    n["adj"] = P.write_adjudication(adj, f("adj"))
    n["intersect"] = P.write_intersect(pts, f("intersect"))
    n["stats"] = P.write_stats(f("stats"))
    n["poly"] = P.write_polygons(f("poly"))
    n["conc"] = P.write_concordance(f("conc"))
    n["nfi"] = P.write_nfi(f("nfi"))
    n["fire"] = P.write_fire(f("fire"))
    n["dict"] = P.write_dictionary(f("dict"))
    n["manifest"] = P.write_manifest(f("manifest"), n)
    DC.write_design(f("design"))
    DC.write_erpa(f("erpa"))
    DC.write_plan(f("plan"))
    DC.write_frel(f("frel"))
    DC.write_release(f("release"))
    PP.normalize_ooxml(f("adj"), W.PEOPLE["reference"], W.PEOPLE["reference"], "2026-04-13T13:02:00Z",
                       "2026-04-17T22:41:09Z", excel=True, company=W.LAB)
    PP.normalize_ooxml(f("stats"), W.PEOPLE["maps"], W.PEOPLE["maps"], "2026-04-20T15:10:00Z",
                       "2026-04-22T18:05:44Z", excel=True, company=W.LAB)
    PP.normalize_pdf(f("design"), b"D:20260126091503-05'00'", b"D:20260126093140-05'00'")
    PP.normalize_pdf(f("erpa"), b"D:20240315140000-05'00'", b"D:20240315141255-05'00'")
    PP.normalize_pdf(f("plan"), b"D:20230320100000-05'00'", b"D:20230320101722-05'00'")
    PP.normalize_pdf(f("frel"), b"D:20231121110000-05'00'", b"D:20231121112033-05'00'")
    PP.normalize_pdf(f("release"), b"D:20260422162210-05'00'", b"D:20260422163905-05'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return {"counts": n, "pts": pts, "qc": qc, "adj": adj}


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 5, 22, 17, 25, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import golden as G
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    world["golden"] = G.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                             os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
                meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode() +
                          open(os.path.join(TASK, "metadata.json"), "rb").read() +
                          open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))), allh[:16]))
    import zipfile
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not ok:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
