"""Build task450: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task450/generator/build.py              everything
    python3 task450/generator/build.py --out DIR    the pack only, into DIR
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
CENTRAL = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2026, 10, 9, 16, 42, tzinfo=CENTRAL)       # the folder as the office shared it


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or S.simulate()
    rng = np.random.default_rng(W.SEED + 17)
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["resp26"] = P.write_resp26(w, f("resp26"), np.random.default_rng(W.SEED + 26))
    n["resp25"] = P.write_resp25(w, f("resp25"), np.random.default_rng(W.SEED + 25))
    n["bank"] = P.write_bank(w["F"], f("bank"), np.random.default_rng(W.SEED + 3))
    n["enroll"] = P.write_enroll(w, f("enroll"))
    n["xwalk"] = P.write_xwalk(w, f("xwalk"), rng)
    n["merges"] = P.write_merges(w, f("merges"))
    n["directory"] = P.write_directory(w, f("directory"), rng)
    n["projection"] = P.write_projection(w, f("projection"), np.random.default_rng(W.SEED + 41))
    n["learning"] = P.write_learning(w, f("learning"), np.random.default_rng(W.SEED + 43))
    strands = {}
    for r in P.items(w["F"], np.random.default_rng(W.SEED + 3)):
        if r["pos25"]:
            strands[r["strand"]] = strands.get(r["strand"], 0) + 1
    DC.write_report(os.path.join(out, DC.REPORT), [(s, strands.get(s, 0)) for s, _ in P.STRANDS])
    DC.write_rules(os.path.join(out, DC.RULES))
    bk = P.bank_key(w["F"])
    DC.write_notice(os.path.join(out, DC.NOTICE), w["F"]["ids26"][P.FIX_POS - 1], bk[P.FIX_POS - 1],
                    w["F"]["key26"][P.FIX_POS - 1])
    by = W.PEOPLE["director"][0]
    PP.normalize_ooxml(f("bank"), "Jacqueline Sanchez", by, "2024-11-04T15:10:00Z", "2026-04-06T13:22:41Z", excel=True)
    PP.normalize_ooxml(f("directory"), by, by, "2026-01-12T16:05:00Z", "2026-07-08T19:41:09Z", excel=True)
    PP.normalize_pdf(os.path.join(out, DC.REPORT), b"D:20250915101204-05'00'", b"D:20250916083518-05'00'")
    PP.normalize_pdf(os.path.join(out, DC.RULES), b"D:20260818163002-05'00'", b"D:20260819090144-05'00'")
    PP.normalize_pdf(os.path.join(out, DC.NOTICE), b"D:20260519112715-05'00'", b"D:20260519112715-05'00'")
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
    stamp = (2026, 10, 9, 16, 42, 0)
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
