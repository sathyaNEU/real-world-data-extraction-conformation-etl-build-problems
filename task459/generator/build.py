"""Build task459: the pack into <task>/target, the goldens into <task>/golden, metadata.json and generator/figures.json;
then the checks and the independent verifier, a second full build into a scratch folder inside the task compared byte
for byte, and target.zip cut from the final build.

    python3 task459/generator/build.py              everything
    python3 task459/generator/build.py --out DIR    the pack only, into DIR
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
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import sim as S             # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
PACIFIC = dt.timezone(dt.timedelta(hours=-8))
STAMP = dt.datetime(2026, 11, 4, 16, 40, tzinfo=PACIFIC)       # the evaluation folder as the district shared it


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or S.simulate()
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["camd"] = P.write_camd(w, f("camd"))
    n["plans"] = P.write_plans(w, f("plans"))
    n["xwalk"] = P.write_xwalk(f("xwalk"))
    n["eia860"] = P.write_eia860(f("eia860"))
    n["eia923"] = P.write_eia923(w, f("eia923"))
    n["offers"] = P.write_offers(w, f("offers"))
    n["meter"] = P.write_meter(w, f("meter"))
    n["gads"] = P.write_gads(w, f("gads"))
    n["outages27"] = P.write_outages27(w, f("outages27"))
    DC.write_procedure(f("procedure"))
    DC.write_terms(f("terms"))
    n["dictionary"] = DC.write_dictionary(f("dictionary"))
    pl = W.PEOPLE["planning"][0]
    cj = W.PEOPLE["compliance"][0]
    PP.normalize_ooxml(f("offers"), pl, cj, "2026-06-01T16:05:00Z", "2026-10-01T15:42:37Z", excel=True,
                       company=W.DISTRICT)
    # the public extracts carry the department that filtered them, not a person
    PP.normalize_ooxml(f("eia860"), "Resource Planning", "Resource Planning", "2026-10-06T17:20:00Z",
                       "2026-10-06T17:31:54Z", excel=True, company=W.DISTRICT)
    PP.normalize_ooxml(f("eia923"), "Resource Planning", "Resource Planning", "2026-10-06T17:22:00Z",
                       "2026-10-06T17:40:09Z", excel=True, company=W.DISTRICT)
    PP.normalize_pdf(f("procedure"), b"D:20260609141500-07'00'", b"D:20260609142710-07'00'")
    PP.normalize_pdf(f("terms"), b"D:20260601083000-07'00'", b"D:20260601084512-07'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    w["counts"] = n
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 11, 4, 16, 40, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False, world=None):
    import golden as G
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet, world=world)
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
