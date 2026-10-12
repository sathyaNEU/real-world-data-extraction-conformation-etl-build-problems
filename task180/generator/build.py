"""Build task180: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task180/generator/build.py              everything
    python3 task180/generator/build.py --out DIR    the pack only, into DIR"""
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
import models as M         # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import sim as S            # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "cat": R.CAT, "auto": R.AUTO, "hourly": R.HOURLY, "reports": R.REPORTS, "inventory": R.INVENTORY, "gaps": R.GAPS,
    "visits": R.VISITS, "plant_reg": R.PLANT_REG, "well_reg": R.WELL_REG, "federal": R.FEDERAL, "gw": R.GW,
    "scheme": D.SCHEME, "ordinance": D.ORDINANCE, "bulletin": D.BULLETIN, "plans": D.PLANS, "notes": D.NOTES,
}
DISTRACTORS = ("federal", "gw")


def bulletin_figures(out):
    """The bulletin's counts, made the way the scheme counts, from the catalogue as the pack carries it."""
    d = M.load(out)
    c = M.counted(d)
    t = M.table(c)
    qs = [(2025, 4), (2026, 1), (2026, 2), (2026, 3)]
    counts = {p: {k: t[p][k] for k in qs} for p in W.PLANTS}
    q3 = c[(c["y"] == 2026) & (c["q"] == 3)]
    largest = {p: float(q3[q3["plant"] == p]["ml"].max()) for p in W.PLANTS}
    return counts, largest


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = world or S.simulate_all()
    counts = {}
    counts["cat"] = R.write_catalogue(p("cat"), w["cat"])
    counts["auto"] = R.write_automatic(p("auto"), w["auto"])
    counts["hourly"] = R.write_hourly(p("hourly"), w["hourly"])
    w["report_rows"] = R.report_rows(w["inj"])
    counts["reports"] = R.write_reports(p("reports"), w["report_rows"])
    R.write_plant_register(p("plant_reg"), w["stations"])
    counts["well_reg"] = R.write_well_register(p("well_reg"))
    R.write_inventory(p("inventory"), w["stations"])
    counts["gaps"] = R.write_gaps(p("gaps"), w["gaps"])
    counts["visits"] = R.write_visits(p("visits"), w["field"])
    counts["federal"] = R.write_federal(p("federal"), w["federal"])
    counts["gw"] = R.write_groundwater(p("gw"), w["gw"])
    D.write_scheme(p("scheme"))
    D.write_ordinance(p("ordinance"))
    D.write_plans(p("plans"))
    D.write_notes(p("notes"))
    w["bulletin"] = bulletin_figures(out)
    D.write_bulletin(p("bulletin"), *w["bulletin"])
    PP.normalize_ooxml(p("reports"), "Amalie Mende", "Amalie Mende", "2023-02-14T08:12:40Z", "2026-10-12T07:31:05Z",
                       excel=True)
    PP.normalize_ooxml(p("visits"), "Eugen Scheel", "Eugen Scheel", "2026-01-08T06:55:12Z", "2026-10-09T14:22:51Z",
                       excel=True)
    PP.normalize_pdf(p("scheme"), b"D:20240209104455+01'00'", b"D:20240212081530+01'00'")
    PP.normalize_pdf(p("ordinance"), b"D:20260330091207+02'00'", b"D:20260330091207+02'00'")
    PP.normalize_pdf(p("plans"), b"D:20260924140318+02'00'", b"D:20260924141102+02'00'")
    PP.normalize_pdf(p("bulletin"), b"D:20261008170544+02'00'", b"D:20261009083012+02'00'")
    stamp = dt.datetime(2026, 10, 12, 16, 20, tzinfo=W.LOCAL).timestamp()
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
    stamp = (2026, 10, 12, 16, 22, 4)
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
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
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
