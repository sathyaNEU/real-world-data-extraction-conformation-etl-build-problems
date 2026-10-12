"""Build task184: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task184/generator/build.py              everything
    python3 task184/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import profiles as PR      # noqa: E402
import records as R        # noqa: E402
import sim as S            # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "lanes": R.LANE_COUNTS, "queue": R.QUEUE_TIME, "roster26": R.ROSTER_26, "roster27": R.ROSTER_27,
    "planning": R.PLANNING, "postings": R.POSTINGS, "register": R.REGISTER, "returns": R.RETURNS,
    "hotels": R.HOTELS, "claims": R.CLAIMS, "faults": R.FAULTS, "feedback": R.FEEDBACK,
    "standard26": D.STANDARD_26, "standard23": D.STANDARD_23, "policy": D.POLICY, "notes": D.NOTES,
    "flags": D.FLAGS,
}
DISTRACTORS = ("faults", "feedback")


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = world or S.simulate_all()
    counts = {}
    counts["lanes"] = R.write_lane_counts(p("lanes"), w)
    counts["queue"] = R.write_queue_time(p("queue"), w)
    R.write_roster(p("roster26"), "S26", "2026-05-24", "2026-09-12")
    R.write_roster_27(p("roster27"))
    design, plans, phase = PR.design27()
    R.write_planning(p("planning"), design)
    posts = R.postings()
    R.write_postings(p("postings"), posts)
    R.write_register(p("register"))
    R.write_returns(p("returns"), w)
    lines, stays = R.invoices(posts)
    R.write_hotels(p("hotels"), lines)
    counts["claims"] = R.write_claims(p("claims"), R.export_claims(R.claims(posts)))
    counts["faults"] = R.write_faults(p("faults"), w)
    counts["feedback"] = R.write_feedback(p("feedback"), w)
    D.write_standard_2026(p("standard26"))
    D.write_standard_2023(p("standard23"))
    D.write_policy(p("policy"))
    D.write_notes(p("notes"))
    D.write_flags(p("flags"))
    PP.normalize_ooxml(p("planning"), "Alana Marnan", "Alana Marnan", "2027-03-29T10:14:22Z",
                       "2027-04-23T07:48:05Z", excel=True)
    PP.normalize_ooxml(p("hotels"), "AP Reporting", "AP Reporting", "2027-04-22T16:31:50Z",
                       "2027-04-22T16:31:50Z", excel=True)
    PP.normalize_ooxml(p("roster27"), "KAS Rostering", "KAS Rostering", "2027-04-21T05:02:37Z",
                       "2027-04-21T05:02:37Z", excel=True)
    PP.normalize_pdf(p("standard26"), b"D:20260216113005+00'00'", b"D:20260216114412+00'00'")
    PP.normalize_pdf(p("standard23"), b"D:20230109093310+00'00'", b"D:20230109093847+00'00'")
    PP.normalize_pdf(p("policy"), b"D:20270302150218+00'00'", b"D:20270302152940+00'00'")
    stamp = dt.datetime(2027, 4, 23, 17, 5, tzinfo=dt.timezone(dt.timedelta(hours=1))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    w["phase"] = phase
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 4, 23, 17, 6, 12)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    import analysis as AN
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    F = AN.compute(world)
    DL.main(os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"), F)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    world["F"] = F
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
