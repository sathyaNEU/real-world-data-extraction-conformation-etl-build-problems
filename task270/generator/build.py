"""Build task270: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task270/generator/build.py              everything
    python3 task270/generator/build.py --out DIR    the pack only, into DIR
    python3 task270/generator/build.py --golden     the pack and the goldens, no checks"""
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
GOLDEN_MTIME = calendar.timegm((2027, 1, 27, 16, 5, 0))
PDF_DATES = {"strategy": ("D:20260311102000+00'00'", "D:20260311104500+00'00'"),
             "spec": ("D:20240219091500+00'00'", "D:20240219093000+00'00'"),
             "bureau": ("D:20250602140500+01'00'", "D:20250602141000+01'00'"),
             "kpi": ("D:20270109113000+00'00'", "D:20270109114000+00'00'")}
OOXML = {"register": ("Hallowmere Property", "Hallowmere Property", "2019-05-13T10:12:00Z", "2026-11-24T15:48:00Z",
                      "F-gas register", True)}


def build(out, seed=K.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    w, n = PK.build_pack(out, seed)
    return dict(counts=n)


def finish(out):
    """the containers as their writers save them, then every file's modified time set to the pack's assembly"""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.ORG_LTD
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.ORG
    PP.normalize_ooxml(os.path.join(golden, K.BOOK), K.REQUESTER, K.REQUESTER, "2027-01-18T10:05:00Z",
                       "2027-01-27T16:05:00Z", title="2027 pack programme", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (GOLDEN_MTIME, GOLDEN_MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, %s, %s and every store, pack, job, cylinder and person "
           "are fictional; the records follow the forms of a UK retailer's F-gas register, a refrigeration "
           "contractor's job sheet export and cylinder log, and a remote monitoring bureau's daily export"
           % (K.ORG, K.CONTRACTOR, K.BUREAU))
    c = fig["call"]
    f = fig["components"]["loss_share_pct"]
    return {
        "task": "task270",
        "title": "%s: the first region of the 2027 pack programme" % K.ORG,
        "domain": "General Statistics & Data Science (missing data, censoring and measurement error)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": [K.BOOK, K.CHART],
        "provenance": {name: {"source": src, "date": "2027-01-12", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "%s (%d per cent of its HFC packs' full charge lost in 2026, against %s %d)" % (
            c["name"], f[c["region"]], c["runner_up_name"], f[c["runner_up"]]),
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
