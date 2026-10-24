"""Build task280: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task280/generator/build.py              everything
    python3 task280/generator/build.py --out DIR    the pack only, into DIR
    python3 task280/generator/build.py --golden     the pack and the goldens, no checks"""
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
import asks as AK          # noqa: E402
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("schedule", "Schedule 4 (Network Performance) of the cable franchise agreement with Tollard Cable, renewed 12 June "
                 "2024."),
    ("methods", "The broadband measurement panel's methods note for 2026."),
    ("dictionary", "The Commission's data dictionary for these files."),
    ("tests", "The panel's evening extract: every download test the panel units ran between 5 pm and midnight, 14 "
              "September to 13 November 2026."),
    ("units", "The panel's measurement units."),
    ("households", "The panel's households."),
    ("plans", "Tollard's plan catalogue."),
    ("subs", "Tollard's subscription history for the panel households' accounts."),
    ("nodes", "Tollard's node register (filing of 16 November 2026)."),
    ("addr", "Tollard's nodes for the panel households' service addresses."),
    ("util", "Tollard's node utilisation filings for the nodes serving panel households, 14 September to 13 November "
             "2026."),
    ("subcounts", "Tollard's month-end subscriber counts by node, July to October 2026."),
    ("outages", "Tollard's outage reports, August to November 2026."),
    ("closeout", "The Commission's close-out of the 2025 designations."),
    ("complaints", "Complaints about Tollard the Commission received, July to November 2026."),
    ("latency", "The panel units' daily latency summaries, 5 pm to midnight, 14 September to 13 November 2026."),
]


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    rc = R.Records(seed)
    pl = AK.Plant(rc)
    n = {}
    for key, fn in (("tests", rc.test_rows), ("units", rc.unit_table), ("households", rc.household_rows),
                    ("plans", rc.plan_rows), ("subs", rc.subscription_rows), ("nodes", pl.register_rows),
                    ("addr", rc.address_rows), ("util", rc.util_rows), ("outages", pl.outage_rows),
                    ("complaints", rc.complaint_rows), ("latency", rc.latency_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    head, rows = pl.subcount_table()
    DC.write_subcounts(p("subcounts"), head, rows)
    n["subcounts"] = len(rows)
    DC.write_schedule(p("schedule"))
    DC.write_methods(p("methods"), rc.w.NH)
    DC.write_dictionary(p("dictionary"))
    DC.write_closeout(p("closeout"), AK.DESIGNATED_2025, pl.remedy)
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(rc=rc if keep else None, plant=pl if keep else None, counts=n)


PDF_DATES = {"schedule": ("D:20240612150500-04'00'", "D:20240612150500-04'00'"),
             "methods": ("D:20260821091500-04'00'", "D:20260821111800-04'00'"),
             "dictionary": ("D:20250304100000-05'00'", "D:20261118143000-05'00'"),
             "closeout": ("D:20260911084500-04'00'", "D:20260911162000-04'00'")}
OOXML = {"subcounts": ("Donna Atkins", "Donna Atkins", "2026-08-03T13:20:00Z", "2026-11-09T19:41:00Z",
                       "Subscribers by node", True)}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.FRANCHISEE_LEGAL
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.COMMISSION
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), "Performance compliance", "Performance compliance",
                       "2026-11-25T14:05:00Z", "2026-12-02T21:48:00Z", title="Hub peak congestion 2026", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); the %s, %s, its hubs, nodes, plans, the panel and every "
           "person are fictional; the records follow the forms of whitebox broadband measurement panels, cable "
           "operators' node registers and utilisation filings, and franchise performance schedules" %
           (K.COMMISSION, K.FRANCHISEE))
    return {
        "task": "task280",
        "title": "%s: the Tollard Cable hubs designated for 2027 under Schedule 4" % K.COMMISSION,
        "domain": "General Statistics & Data Science (missing data, censoring and measurement error)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-24", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "%d hubs designated: %s" % (fig["call"]["count"], ", ".join(fig["call"]["designated"])),
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
