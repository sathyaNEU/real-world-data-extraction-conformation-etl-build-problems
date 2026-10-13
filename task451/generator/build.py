"""Build task451: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task451/generator/build.py              everything
    python3 task451/generator/build.py --out DIR    the pack only, into DIR
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
LONDON = dt.timezone(dt.timedelta(hours=1))
STAMP = dt.datetime(2026, 10, 9, 15, 26, tzinfo=LONDON)       # the folder as the secretariat shared it


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or S.simulate()
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["datastore"] = P.write_datastore(w, f("datastore"))
    n["gxml"] = P.write_fund_xml(w, "G", f("gxml"))
    n["sxml"] = P.write_fund_xml(w, "S", f("sxml"))
    P.write_register(f("register"))
    n["registry"] = P.write_registry(w, f("registry"))
    n["fx"] = P.write_fx(w["fx"], f("fx"))
    P.write_codelists(f("codelists"))
    P.write_query_file(f("query"), n["datastore"])
    P.write_indicators(f("indicators"))
    P.write_offices(f("offices"))
    DC.write_method(os.path.join(out, DC.METHOD))
    DC.write_paper(os.path.join(out, DC.PAPER))
    data, fin = W.PEOPLE["data"][0], W.PEOPLE["finance"][0]
    PP.normalize_ooxml(f("register"), data, data, "2022-02-14T10:05:00Z", "2026-09-01T08:47:12Z", excel=True,
                       company=W.SECRETARIAT)
    PP.normalize_ooxml(f("codelists"), fin, fin, "2026-10-05T07:31:00Z", "2026-10-05T07:44:39Z", excel=True,
                       company=W.SECRETARIAT)
    PP.normalize_ooxml(f("offices"), fin, data, "2026-08-04T13:20:00Z", "2026-08-27T16:02:51Z", excel=True,
                       company=W.SECRETARIAT)
    PP.normalize_pdf(os.path.join(out, DC.METHOD), b"D:20260311104408+00'00'", b"D:20260312091537+00'00'")
    PP.normalize_pdf(os.path.join(out, DC.PAPER), b"D:20260924162210+01'00'", b"D:20260925095301+01'00'")
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
    stamp = (2026, 10, 9, 15, 26, 0)
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
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
