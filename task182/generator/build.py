"""Build task182: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json, then the
checks and the independent verifier, then a second full build into a scratch folder inside the task (removed
after) compared byte for byte.

    python3 task182/generator/build.py              everything
    python3 task182/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D          # noqa: E402
import postprocess as PP  # noqa: E402
import readings as RD     # noqa: E402
import records as R       # noqa: E402
import sim as S           # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "register": R.REGISTER, "mg02": D.MG02, "notes": D.NOTES, "dips": R.DIPS, "loggers": R.LOGGERS,
    "installs": R.INSTALLS, "baro": R.BARO, "climate": R.CLIMATE, "take": R.TAKE, "contacts": R.CONTACTS,
    "quality": R.QUALITY,
}
DISTRACTORS = ("contacts", "quality")


def simulate():
    clim = S.climate()
    q = S.take()
    hd = S.heads(clim, q)
    rows, truth = RD.dips(hd, clim)
    bt, bp, btemp, bmap = RD.baro()
    logs, installs = RD.loggers(hd, bmap)
    baseline = {t["label"]: (t["day"], round(t["depth_m"], 2)) for t in truth if t["purpose"] == "baseline"}
    return dict(clim=clim, q=q, hd=hd, dips=rows, truth=truth, baro=(bt, bp, btemp), logs=logs, installs=installs,
                baseline=baseline)


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = world or simulate()
    counts = {}
    counts["dips"] = R.write_dips(p("dips"), w["dips"])
    counts["loggers"] = R.write_loggers(p("loggers"), w["logs"])
    counts["installs"] = R.write_installs(p("installs"), w["installs"])
    counts["baro"] = R.write_baro(p("baro"), *w["baro"])
    counts["climate"] = R.write_climate(p("climate"), w["clim"])
    counts["take"] = R.write_take(p("take"), w["q"])
    counts["quality"] = R.write_quality(p("quality"), w["hd"])
    R.write_register(p("register"), w["baseline"])
    counts["contacts"] = R.write_contacts(p("contacts"))
    D.write_mg02(p("mg02"))
    D.write_notes(p("notes"))
    PP.normalize_ooxml(p("register"), W.PEOPLE["env"], W.PEOPLE["env"], "2014-08-19T01:42:10Z", "2026-10-09T03:18:44Z",
                       excel=True)
    PP.normalize_ooxml(p("contacts"), W.PEOPLE["env"], W.PEOPLE["env"], "2026-01-05T23:20:31Z", "2026-10-09T01:05:12Z",
                       excel=True)
    stamp = dt.datetime(2026, 10, 9, 14, 20, tzinfo=W.AEST).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as C
    import verify as V
    world = everything(TASK)
    C.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
          meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        m1 = hashlib.sha256(open(os.path.join(TASK, "metadata.json"), "rb").read()).hexdigest()
        m2 = hashlib.sha256(open(os.path.join(tmp, "metadata.json"), "rb").read()).hexdigest()
        if not (same_t and same_g and m1 == m2):
            raise SystemExit("second build differs: target %s, golden %s, metadata %s" % (same_t, same_g, m1 == m2))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode()
                          + "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()
                          + m1.encode()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files and metadata.json (combined sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))), allh[:16]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
