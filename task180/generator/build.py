"""Build task180's evidence pack into <out>/ (default task180/target), then the goldens, metadata.json, the
checks, the independent verifier, and a second full build into a scratch folder compared byte for byte."""
import argparse
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D          # noqa: E402
import hospital as H      # noqa: E402
import records as R       # noqa: E402
import sim as S           # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "screen": D.SCREEN, "sop": D.SOP, "notes": D.NOTES, "rx": R.PRESCRIPTIONS, "contacts": R.CONTACTS,
    "dx": R.DIAGNOSES, "civil": R.CIVIL, "matched": R.MATCHED, "atc": R.ATC, "population": R.POPULATION,
    "psur": D.PSUR, "minutes": D.MINUTES,
}
DISTRACTORS = ("psur", "minutes")


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    world = S.simulate()
    C, Dx, hosp = H.build(world)
    pnr = R.pnrs(world["P"])
    counts = {"rx": R.write_prescriptions(p("rx"), world, pnr)}
    counts["contacts"], counts["dx"] = R.write_contacts(p("contacts"), p("dx"), C, Dx, hosp, pnr)
    counts["civil"] = R.write_civil(p("civil"), world["P"], pnr)
    counts["matched"] = R.write_matched(p("matched"), world["P"], pnr)
    counts["atc"] = R.write_atc(p("atc"))
    counts["pop"] = R.write_population(p("population"))
    world["screen_q3"], world["screen_rows"] = D.write_screen(p("screen"))
    D.write_sop(p("sop"))
    D.write_notes(p("notes"), counts)
    D.write_psur(p("psur"), D.psur_exposure(world))
    D.write_minutes(p("minutes"))
    stamp = W.dt.datetime(2026, 10, 7, 9, 30, tzinfo=W.dt.timezone.utc).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    world["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %s" % kv for kv in counts.items())))
    return world


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


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
    import checks as C
    import verify as V
    world = everything(TASK)
    C.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
