"""Build task449: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task449/generator/build.py              everything
    python3 task449/generator/build.py --out DIR    the pack only, into DIR
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

import numpy as np          # noqa: E402

import docs as DC           # noqa: E402
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import sim as S             # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-4))
STAMP = dt.datetime(2026, 10, 9, 11, 42, tzinfo=EASTERN)       # the folder as workforce planning shared it


def simulate():
    w = S.simulate()
    P.source_refs(np.random.default_rng(W.SEED + 1), w["rows"])
    return w


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or simulate()
    rng = np.random.default_rng(W.SEED + 2)
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["register"] = P.write_register(w["rows"], f("register"))
    n["history"] = P.write_history(w["rows"], f("history"))
    n["social"] = P.write_social(w["social"], f("social"))
    n["meridel"] = P.write_meridel(w["payments"], f("meridel"))
    n["portfolio"] = P.write_portfolio(rng, f("portfolio"))
    n["codes"] = P.write_codes(f("codes"))
    n["time"] = P.write_time(w["time"], f("time"))
    n["marlowby"] = P.write_marlowby(w["marlowby"], f("marlowby"))
    n["treadwell"] = P.write_treadwell(w["treadwell"], f("treadwell"))
    DC.write_opslog(f("opslog"))
    n["ivr"] = P.write_ivr(rng, f("ivr"))
    n["cfpb"] = P.write_cfpb(rng, w["rows"], f("cfpb"))
    DC.write_wps(os.path.join(out, DC.WPS))
    DC.write_schedule(os.path.join(out, DC.SCHEDULE))
    DC.write_sow(os.path.join(out, DC.SOW))
    DC.write_dictionary(os.path.join(out, DC.DICTIONARY))
    n["manifest"] = P.write_manifest(f("manifest"), n)
    PP.normalize_ooxml(f("treadwell"), "Treadwell & Oake", "Treadwell & Oake", "2026-01-05T15:02:00Z",
                       "2026-10-02T21:17:44Z", excel=True, company="Treadwell & Oake")
    PP.normalize_ooxml(f("opslog"), W.PEOPLE["social"], W.PEOPLE["planning"], "2026-01-05T13:40:00Z",
                       "2026-10-09T14:51:09Z", excel=True, company=W.BPO)
    PP.normalize_ooxml(os.path.join(out, DC.DICTIONARY), W.PEOPLE["planning"], W.PEOPLE["planning"],
                       "2025-10-14T18:22:00Z", "2026-10-09T15:31:26Z", excel=True, company=W.BPO)
    PP.normalize_pdf(os.path.join(out, DC.WPS), b"D:20250226140511-05'00'", b"D:20250226140511-05'00'")
    PP.normalize_pdf(os.path.join(out, DC.SCHEDULE), b"D:20260619163304-04'00'", b"D:20260619163304-04'00'")
    PP.normalize_pdf(os.path.join(out, DC.SOW), b"D:20251208101716-05'00'", b"D:20251211092244-05'00'")
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
    stamp = (2026, 10, 9, 11, 42, 0)
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
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()).hexdigest()
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
