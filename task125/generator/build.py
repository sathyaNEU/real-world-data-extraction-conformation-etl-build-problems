"""Build task125: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task125/generator/build.py              everything
    python3 task125/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import datetime as dt      # noqa: E402

import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import sim as S            # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "person": R.PERSON, "calls": R.CALLS, "register": R.REGISTER, "controls": R.CONTROLS, "release": R.RELEASE,
    "claimants": R.CLAIMANTS, "staffing": R.STAFFING, "methods": D.METHODS, "fi_2026": D.FI_2026, "fi_2024": D.FI_2024,
    "dictionary": D.DICTIONARY, "notes": D.NOTES,
}
DISTRACTORS = ("claimants", "staffing")


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = world or S.simulate_all()
    I = w["intakes"]
    counts = {}
    w["person_rows"] = R.person_file(I)
    counts["person"] = R.write_person(p("person"), w["person_rows"])
    w["call_rows"] = R.calls(I)
    counts["calls"] = R.write_calls(p("calls"), w["call_rows"])
    counts["register"] = R.write_register(p("register"), I)
    R.write_controls(p("controls"))
    R.write_release(p("release"), I)
    counts["claimants"] = R.write_claimants(p("claimants"))
    R.write_staffing(p("staffing"))
    D.write_methods(p("methods"))
    D.write_fi_2026(p("fi_2026"))
    D.write_fi_2024(p("fi_2024"))
    D.write_dictionary(p("dictionary"))
    D.write_notes(p("notes"))
    PP.normalize_ooxml(p("controls"), "Population Estimates", "Dylan Fletcher", "2026-02-11T03:12:40Z",
                       "2026-10-20T02:31:05Z", excel=True)
    PP.normalize_ooxml(p("release"), "Labour Market Statistics", "Raewyn Bailey", "2026-08-06T21:40:12Z",
                       "2026-08-12T22:02:51Z", excel=True)
    PP.normalize_pdf(p("methods"), b"D:20250311104455+13'00'", b"D:20250314081530+13'00'")
    PP.normalize_pdf(p("fi_2026"), b"D:20260617091207+12'00'", b"D:20260617093342+12'00'")
    PP.normalize_pdf(p("fi_2024"), b"D:20240304140318+13'00'", b"D:20240304141102+13'00'")
    stamp = dt.datetime(2026, 10, 20, 16, 20, tzinfo=dt.timezone(dt.timedelta(hours=13))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 20, 16, 22, 4)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    world["deliver"] = DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
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
