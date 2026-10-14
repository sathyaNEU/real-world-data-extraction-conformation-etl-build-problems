"""Build task456: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task456/generator/build.py              everything
    python3 task456/generator/build.py --out DIR    the pack only, into DIR
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
import feeds as FD          # noqa: E402
import latent as LT         # noqa: E402
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import roster as RO         # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = dt.timezone(dt.timedelta(hours=-6))
STAMP = dt.datetime(2026, 1, 20, 6, 47, tzinfo=LOCAL)        # the extract as the data team assembled it


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    H = RO.hospitals()
    Z = LT.states(H)
    F = LT.flags(H, Z)
    S = FD.survey(H, F)
    B = FD.board(H, F)
    R = FD.transfers(H, F)
    n = {}
    n["regions"] = P.write_regions(f("regions"))
    n["crosswalk"] = P.write_crosswalk(H, f("crosswalk"))
    n["aliases"] = P.write_aliases(H, f("aliases"))
    n["codes"] = P.write_codes(f("codes"))
    n["survey_old"], n["survey_new"] = P.write_survey(H, S, f("survey_old"), f("survey_new"))
    n["board"] = P.write_board(B, f("board"))
    n["tc_old"], n["tc_new"], typed, ids = P.write_transfers(H, R, f("tc_old"), f("tc_new"))
    n["federal"] = P.write_federal(H, S, f("federal"))
    n["history"] = P.write_history(f("history"))
    n["dict"] = P.write_dictionary(f("dict"))
    n["manifest"] = P.write_manifest(f("manifest"), n)
    DC.write_compact(f("compact"))
    DC.write_annex(f("annex"))
    PP.normalize_ooxml(f("tc_old"), "Transfer Center", "Transfer Center", "2026-01-05T06:02:00Z",
                       "2026-01-20T12:31:07Z", excel=True, company=W.CENTER)
    PP.normalize_ooxml(f("dict"), W.PEOPLE["data"], W.PEOPLE["data"], "2025-11-03T15:20:00Z",
                       "2026-01-20T12:40:51Z", excel=True, company=W.ALLIANCE)
    PP.normalize_pdf(f("compact"), b"D:20250916143005-05'00'", b"D:20250916150212-05'00'")
    PP.normalize_pdf(f("annex"), b"D:20251103091544-06'00'", b"D:20251103094810-06'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return {"counts": n, "H": H, "Z": Z, "F": F, "S": S, "B": B, "R": R, "typed": typed, "ids": ids}


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 1, 20, 6, 47, 0)
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
    stamp = dt.datetime(2026, 1, 21, 9, 34, tzinfo=LOCAL).timestamp()
    for name in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", name), (stamp, stamp))
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
