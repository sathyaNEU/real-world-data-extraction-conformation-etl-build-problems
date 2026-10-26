"""Build task271: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task271/generator/build.py              everything
    python3 task271/generator/build.py --out DIR    the pack only, into DIR
    python3 task271/generator/build.py --golden     the pack and the goldens, no checks"""
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
import pack as PK          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())
GOLDEN_MTIME = calendar.timegm((2026, 11, 10, 17, 25, 0))
PDF_DATES = {"standard": ("D:20240312101500-05'00'", "D:20240314154000-04'00'"),
             "guide": ("D:20250203091000-05'00'", "D:20250205162500-05'00'"),
             "brief": ("D:20261005101200-04'00'", "D:20261005102000-04'00'"),
             "plan": ("D:20190620140000-04'00'", "D:20190624110500-04'00'")}
OOXML = {"bordereau": ("Corrigan Adjusting Services", "Corrigan Adjusting Services", "2023-04-03T14:10:00Z",
                       "2026-09-04T15:32:00Z", "Claims bordereau, Halverstead Mutual", True)}


def build(out, seed=K.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    w, ex, n = PK.build_pack(out, seed)
    return dict(counts=n)


def finish(out):
    """the containers as their writers save them, then every file's modified time set to the pack's assembly"""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = "Corrigan Adjusting Services LLC"
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.ORG
    PP.normalize_ooxml(os.path.join(golden, K.BOOK), K.REQUESTER, K.REQUESTER, "2026-10-27T13:40:00Z",
                       "2026-11-10T17:25:00Z", title="2027 agency: the township", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (GOLDEN_MTIME, GOLDEN_MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, %s, its townships, %s, Corrigan Adjusting Services and "
           "every home, policy, claim, hydrant and person are fictional; the records follow the forms of a "
           "Pennsylvania county mutual's policy and claim extracts, a county assessment roll, the State Tax "
           "Equalization Board's common level ratio table, a water authority's open GIS layers and an adjusting "
           "firm's bordereau" % (K.ORG, K.COUNTY, K.AUTHORITY))
    c = fig["call"]
    f = fig["components"]["frequency_per_1000"]
    return {
        "task": "task271",
        "title": "%s: the township for the 2027 agency" % K.ORG,
        "domain": "Actuarial Science & Insurance (claims frequency and severity)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": [K.BOOK, K.CHART],
        "provenance": {name: {"source": src, "date": "2026-10-21", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "%s %s (%d non-weather water claims per 1,000 house-years, against %s %d)" % (
            c["name"], dict((a, k) for a, n, k in K.TOWNS)[c["township"]], f[c["township"]], c["runner_up_name"],
            f[c["runner_up"]]),
    }


def main_build(target, golden, seed=K.SEED):
    import deliver as DV
    b = build(target, seed)
    finish(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    fig, res = DV.write(target, golden)
    finish_golden(golden)
    DV.write_figures(os.path.join(HERE, "figures.json"), fig)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True, ensure_ascii=False)
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
