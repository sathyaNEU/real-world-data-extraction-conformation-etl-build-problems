"""Build task181's evidence pack into <out>/ (default task181/target)."""
import argparse
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D          # noqa: E402
import postprocess as PP  # noqa: E402
import records as R       # noqa: E402
import sim as S           # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
URGENT_SEED = 3
FILES = {
    "line_list": R.LINE_LIST, "notes": D.NOTES, "run_report": D.RUN_REPORT, "protocol": D.PROTOCOL,
    "concordance": R.CONCORDANCE, "admissions": R.ADMISSIONS, "births": R.BIRTHS, "register": R.REGISTER,
    "rosters": R.ROSTERS, "influenza": R.INFLUENZA, "bulletin": D.BULLETIN,
}
DISTRACTORS = ("influenza", "bulletin")


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    world = S.simulate(URGENT_SEED)
    pert = R.line_list_rows(world)
    flu = R.influenza_rows(world)
    R.assign_ids(pert, flu)
    counts = {"line_list": R.write_line_list(p("line_list"), pert)}
    counts["influenza"] = R.write_csv(p("influenza"), flu, R.FLU_COLUMNS)
    R.write_concordance(p("concordance"))
    R.plan_merged_mrns(world)                  # the quarterly table's records draw from the "ask" streams only
    counts["admissions"] = R.write_admissions(p("admissions"), world)
    pregnancies, rb = R.build_mothers_and_births(world)
    counts["births"] = R.write_births(p("births"), pregnancies, world, rb)
    counts["register"] = R.write_register(p("register"), pregnancies, rb)
    world["roster_students"] = R.write_rosters(p("rosters"), world)
    D.write_protocol(p("protocol"))
    D.write_notes(p("notes"))
    D.write_run_report(p("run_report"), p("line_list"), counts["line_list"], len(R.LL_COLUMNS))
    world["bulletin"] = D.write_bulletin(p("bulletin"), p("line_list"), p("influenza"))
    PP.normalize_ooxml(p("concordance"), W.PEOPLE["data_officer"], W.PEOPLE["data_officer"],
                       "2023-02-06T23:12:40Z", "2026-07-14T05:31:09Z")
    PP.normalize_ooxml(p("rosters"), W.PEOPLE["nurse"], W.PEOPLE["nurse"], "2026-09-08T03:02:51Z", "2026-10-01T06:48:13Z")
    ts = W.EXTRACT_LOCAL.timestamp() + 600
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (ts, ts))
    world["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return world


def digest(folder):
    import hashlib
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    """target.zip from root/target: the pack's files at the archive's root, in name order, each stamped with the
    pack's own local time, so the archive is cut from the tree it ships beside and two cuts are byte-identical."""
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (W.EXTRACT_LOCAL + dt.timedelta(minutes=10)).timetuple()[:6]
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    """Pack, goldens and metadata into root/target, root/golden and root/metadata.json."""
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import hashlib
    import tempfile
    import checks as C
    import verify as V
    world = everything(TASK)
    n, log, g = C.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
                      meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        everything(tmp, quiet=True)
        same = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target")) \
            and digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        m1 = hashlib.sha256(open(os.path.join(TASK, "metadata.json"), "rb").read()).hexdigest()
        m2 = hashlib.sha256(open(os.path.join(tmp, "metadata.json"), "rb").read()).hexdigest()
        if not (same and m1 == m2):
            raise SystemExit("second build differs")
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode()
                          + "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()
                          + m1.encode()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files and metadata.json (combined sha256 %s)" % (
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
