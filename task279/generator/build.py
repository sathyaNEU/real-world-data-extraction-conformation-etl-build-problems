"""Build task279: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task279/generator/build.py              everything
    python3 task279/generator/build.py --out DIR    the pack only, into DIR
    python3 task279/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("protocol", "The peat monitoring network's protocol, edition 2024 (English edition)."),
    ("points", "The network's point register: one row a monitoring point, with its 1997 and current codes."),
    ("core97", "Bodemlab Wageveld's report 97-0412 on the 1997 baseline cores, as printed."),
    ("core24", "Gouwlanden Laboratoria's LIMS export of the 2024 cores."),
    ("qc24", "Gouwlanden Laboratoria's quality control results for the 2024 cores."),
    ("grid", "The levelling grids: the 1997 levelling and the 2024 survey, one row a grid point and survey."),
    ("survey", "Landmeetbureau Hoekstra-Venema's report on the 2024 survey of surface levels."),
    ("dw_series", "The dipwell network's readings, April 2014 to March 2026."),
    ("dw_meta", "The dipwell network's register."),
    ("dw_maint", "The dipwell maintenance log."),
    ("register", "The board's register of peat units and of changes to their target levels."),
    ("parcels", "Crop parcels declared for 2025 within the units."),
    ("soils", "The board's soil classes by unit."),
    ("weather", "Daily weather at the board's station at the main pumping station."),
    ("dictionary", "The department's data dictionary for these files."),
]


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    rc = R.Records(seed)
    n = {}
    for key, fn, delim in (("points", rc.point_rows, ","), ("core24", rc.core24_rows, ";"), ("qc24", rc.qc24_rows, ";"),
                           ("grid", rc.grid_rows, ","), ("dw_series", rc.dipwell_series_rows, ","),
                           ("dw_meta", rc.dipwell_meta_rows, ","), ("dw_maint", rc.dipwell_maintenance_rows, ","),
                           ("parcels", rc.parcel_rows, ","), ("soils", rc.soil_rows, ","),
                           ("weather", rc.weather_rows, ",")):
        head, rows = fn()
        R.write_csv(p(key), head, rows, delimiter=delim)
        n[key] = len(rows)
    lines = rc.core97_lines()
    DC.write_lines(p("core97"), lines, encoding="latin-1")
    n["core97"] = sum(1 for ln in lines if ln.startswith("97-0412-"))
    DC.write_register(p("register"), rc.register())
    DC.write_protocol(p("protocol"))
    g = rc.grid()
    DC.write_survey(p("survey"), len(g), sum(1 for x in g if x["lost"]), len(K.UNIT_CODES))
    DC.write_lines(p("dictionary"), DC.DICTIONARY.strip("\n").split("\n"))
    DC.write_lines(p("contents"), ["Contents of this folder (assembled 2 November 2026)", ""] +
                   ["%-44s %s" % (K.FILES[k], d) for k, d in CONTENTS])
    return dict(rc=rc if keep else None, counts=n)


PDF_DATES = {"protocol": ("D:20240115103000+01'00'", "D:20240117091500+01'00'"),
             "survey": ("D:20240612141000+02'00'", "D:20240612141000+02'00'")}
OOXML = {"register": ("Yfke Gemen", "Yfke Gemen", "2019-03-11T08:20:00Z", "2026-10-28T15:02:00Z",
                      "Register peilvakken", True)}


def finish(out):
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.COMPANY
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.COMPANY
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), "Vera Kosten", "Vera Kosten",
                       "2026-11-03T08:55:00Z", "2026-11-09T16:20:00Z", title="Peat carbon loss 1997-2024",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); the %s, its units, monitoring points, laboratories, survey "
           "contractor, dipwells and people are fictional; the records follow the forms of Dutch peat monitoring, "
           "laboratory, levelling and dipwell files" % K.BOARD)
    return {
        "task": "task279",
        "title": "%s: the first raise of the 2027 water-level order" % K.BOARD,
        "domain": "Physical & Environmental Sciences (emissions inventory)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-24", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "first raise: %s" % ", ".join(fig["call"]["first_raise"]),
    }


def main_build(target, golden, seed=K.SEED):
    import deliver as DV
    b = build(target, seed, keep=True)
    finish(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    fig, res = DV.write(target, golden)
    finish_golden(golden)
    DV.write_figures(os.path.join(HERE, "figures.json"), fig)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, res


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(target, path):
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=K.SEED)
    a = ap.parse_args()
    if a.out:
        b = build(a.out, a.seed)
        finish(a.out)
        print(b["counts"])
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden, a.seed)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"), a.seed)
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    finish_golden(os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    g1, g2 = digest(golden), digest(os.path.join(scratch, "golden"))
    same = d1 == d2 and g1 == g2
    for f in sorted(set(d1) | set(g1)):
        if d1.get(f, g1.get(f)) != d2.get(f, g2.get(f)):
            print("  differs on rebuild:", f)
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
