"""Build task489: the pack into <task>/target, the goldens into <task>/golden, metadata.json, generator/figures.json
and submission.md; then the checks, the independent verifier, a second full build in a scratch folder compared byte
for byte, and target.zip cut last.

    python3 task489/generator/build.py              everything
    python3 task489/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import hashlib
import os
import shutil
import sys
import time
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P     # noqa: E402
import sim as S      # noqa: E402
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)


def build(out, wd=None):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    wd = wd or S.simulate()
    n = {}
    n["cycles"] = P.write_csv(f("cycles"), ["received_local", "controller_sn", "well", "cycle_count", "arrival_count", "valve_open_local",
                                            "travel_s", "result", "afterflow_min", "casing_kpa", "tubing_kpa"],
                              P.cycle_rows(wd))
    n["prod"] = P.write_csv(f("prod"), ["production_date", "uwi", "reporting_facility", "hours_on", "gas_e3m3",
                                        "condensate_m3", "water_m3", "allocation_run"], P.prod_rows(wd))
    n["ppa"] = P.write_csv(f("ppa"), ["journal_no", "posted_date", "allocation_run", "uwi", "product", "volume_e3m3",
                                      "comment"], P.ppa_rows(wd))
    n["runs"] = P.write_csv(f("runs"), ["allocation_run", "production_month", "run_date", "run_type", "run_by"],
                            P.run_rows(wd))
    n["analyses"] = P.write_csv(f("analyses"), ["sample_no", "surface_location", "sample_date", "sample_point", "lab",
                                                "methane_mol_pct", "ethane_mol_pct", "propane_mol_pct", "i_butane_mol_pct",
                                                "n_butane_mol_pct", "pentanes_plus_mol_pct", "nitrogen_mol_pct",
                                                "co2_mol_pct"], P.analysis_rows(wd))
    n["counters"] = P.write_csv(f("counters"), ["timestamp_utc", "tag", "value"], P.counter_rows(wd))
    n["orders"] = P.write_csv(f("orders"), ["work_order", "created_local", "pad", "equipment_tag", "work_type",
                                            "description", "assigned_to", "status"], P.order_rows(wd))
    n["ogi"] = P.write_csv(f("ogi"), ["survey_date", "pad", "component", "component_id", "finding", "est_rate_kg_h",
                                      "repair_date", "camera_operator"], P.ogi_rows(wd))
    P.write_register(f("register"), wd)
    P.write_template(f("template"))
    P.write_tanks(f("tanks"), wd)
    DC.write_standard(f("standard"))
    DC.write_survey(f("survey"), wd)
    DC.write_sheet(f("sheet_corrigan"), "Corrigan")
    DC.write_sheet(f("sheet_aldous"), "Aldous")
    DC.write_sheet(f("sheet_brannick"), "Brannick")
    DC.write_controller_sheet(f("sheet_trellick"))
    DC.write_plan(f("plan"))
    for k, who, last, c, m, co in (
            ("register", "Brittany Welch", "Brittany Welch", "2019-04-02T16:20:00Z", "2027-01-18T22:41:00Z", W.ORG),
            ("template", W.PEOPLE["lead"], W.PEOPLE["lead"], "2025-11-21T18:05:00Z", "2025-12-04T20:12:00Z", W.ORG),
            ("tanks", "Anthony Keller", "Anthony Keller", "2026-05-11T15:30:00Z", "2026-10-02T21:48:00Z", W.ORG),
            ("plan", W.PEOPLE["lead"], W.PEOPLE["lead"], "2026-11-30T17:10:00Z", "2027-01-12T16:55:00Z", W.ORG)):
        PP.normalize_ooxml(f(k), who, last, c, m, excel=f(k).endswith(".xlsx"), company=co,
                           revision=9 if k == "plan" else None, total_time=212 if k == "plan" else None)
    for k, c in (("standard", b"D:20251204142917-07'00'"), ("survey", b"D:20260708101342-06'00'"),
                 ("sheet_corrigan", b"D:20230314091158-06'00'"), ("sheet_aldous", b"D:20220930153321-06'00'"),
                 ("sheet_brannick", b"D:20210602112644-06'00'"), ("sheet_trellick", b"D:20240219083507-07'00'")):
        PP.normalize_pdf(f(k), c, c)
    ts = time.mktime(W.STAMP + (0, 0, -1))
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, wd


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=W.STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    import writeup as WU
    n, wd = build(os.path.join(root, "target"))
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    g, figd = DL.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return wd, n, g


def main():
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    wd, n, g = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), wd=wd, n=n, g=g,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {f: open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
                for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, submission.md, figures.json" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()))
    if not good:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main()
