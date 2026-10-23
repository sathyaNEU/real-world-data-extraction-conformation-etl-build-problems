"""Build task275: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task275/generator/build.py              everything
    python3 task275/generator/build.py --out DIR    the pack only, into DIR
    python3 task275/generator/build.py --golden     the pack and the goldens, no checks"""
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
    ("terms", "The board's terms for the 2027 Selectivity Programme (adopted 14 October 2026)."),
    ("register", "The PO's vessel register: one row a member vessel in 2025, with its fleet segment."),
    ("trips", "Electronic logbooks: one row a fishing trip begun in 2025 (extract of 3 February 2026)."),
    ("landings", "Electronic logbooks: the landing declarations of those trips, by species, presentation and "
                 "size status."),
    ("deploy", "At-sea observer scheme: the deployment log, one row a trip drawn for observation in 2025."),
    ("hauls", "At-sea observer scheme: the observers' haul records, by species and fraction."),
    ("manual", "At-sea observer scheme: the 2025 scheme manual."),
    ("sales", "Sales notes of the registered buyers for members' landings, sale dates 1 January 2025 to 31 January "
              "2026 (extract of 6 February 2026)."),
    ("vms", "VMS position reports from members' vessels in 2025, from the PO's VMS service provider."),
    ("transponders", "The PO's record of the VMS terminal fitted to each member vessel."),
    ("ports", "Port limits of the ports the members land at."),
    ("grounds", "The PO's fishing grounds."),
    ("species", "The PO's species list, with minimum sizes and conversion factors."),
    ("quota", "The PO's quota uptake report for 2025."),
    ("gear", "Members' gear declarations for 2025."),
    ("dictionary", "The PO's data dictionary for these files."),
]


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    rc = R.Records(seed)
    n = {}
    for key, fn in (("register", rc.register_rows), ("trips", rc.trip_rows), ("landings", rc.landing_rows),
                    ("deploy", rc.deployment_rows), ("hauls", rc.haul_rows), ("grounds", rc.ground_rows),
                    ("species", rc.species_rows), ("sales", rc.sales_rows), ("vms", rc.vms_rows),
                    ("transponders", rc.transponder_rows), ("ports", rc.port_rows), ("gear", rc.gear_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    DC.write_quota(p("quota"), rc.quota_rows())
    DC.write_terms(p("terms"))
    DC.write_manual(p("manual"))
    DC.write_dictionary(p("dictionary"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(rc=rc if keep else None, counts=n)


PDF_DATES = {"terms": ("D:20261014111500+01'00'", "D:20261014111500+01'00'"),
             "manual": ("D:20250113094000+00'00'", "D:20250120162200+00'00'"),
             "dictionary": ("D:20250210142000+00'00'", "D:20261102101500+00'00'")}
OOXML = {"quota": ("Ellie Arnold", "Ellie Arnold", "2025-01-08T09:12:00Z", "2026-01-30T15:41:00Z",
                   "Quota uptake 2025", True)}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
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
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), K.REQUESTER, K.REQUESTER, "2026-11-12T10:05:00Z",
                       "2026-11-20T16:48:00Z", title="Segment discard shares 2025", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); the %s, its vessels, ports, grounds, buyers, observers and "
           "people are fictional; the records follow the forms of UK electronic logbooks, landing declarations, "
           "sales notes, VMS reports and at-sea observer programmes" % K.PO)
    return {
        "task": "task275",
        "title": "%s: the fleet segments designated for the 2027 Selectivity Programme" % K.PO,
        "domain": "Survey Research & Official Statistics (nonresponse, calibration and measurement error)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-23", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "%d segments designated: %s" % (len(fig["call"]["designated"]),
                                                  ", ".join(fig["call"]["designated"])),
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
