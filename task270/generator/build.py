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
PDF_DATES = {"brief": ("D:20261028114500+00'00'", "D:20261028121000+00'00'"),
             "method": ("D:20260209093000+00'00'", "D:20260212160500+00'00'"),
             "rates": ("D:20261015101500+01'00'", "D:20261016090000+01'00'"),
             "report2025": ("D:20250530143000+01'00'", "D:20250530151500+01'00'")}
OOXML = {"schedules": ("Helena Gaspar", "Helena Gaspar", "2026-11-10T09:20:00Z", "2026-11-17T17:42:00Z",
                       "Esquemas de campanha 2027", True)}


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    w, rc, n = PK.build_pack(out, seed)
    return dict(world=w if keep else None, records=rc if keep else None, counts=n)


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.AGENCY
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def fix_embedded(path, stamp):
    """the chart's data workbook inside the deck as PowerPoint keeps it: no writer name, the deck's own stamp"""
    import io
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name.startswith("ppt/embeddings/") and name.endswith(".xlsx"):
            with zipfile.ZipFile(io.BytesIO(data)) as e:
                inner = [(i.filename, e.read(i.filename)) for i in e.infolist()]
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as e:
                for n, d in inner:
                    if n == "docProps/core.xml":
                        d = re.sub(rb"<dcterms:(created|modified)([^>]*)>[^<]*</dcterms:", lambda m: b"<dcterms:" +
                                   m.group(1) + m.group(2) + b">" + stamp.encode() + b"</dcterms:", d)
                        d = re.sub(rb"<dc:creator>[^<]*</dc:creator>", b"<dc:creator>" + K.PLANNER.encode() +
                                   b"</dc:creator>", d)
                    if n == "docProps/app.xml":
                        d = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>",
                                   d)
                    zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
                    zi.compress_type = zipfile.ZIP_DEFLATED
                    e.writestr(zi, d)
            data = buf.getvalue()
        out.append((name, data))
    with zipfile.ZipFile(path, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def finish_golden(golden):
    import postprocess as PP
    fix_embedded(os.path.join(golden, K.DECK), "2026-12-01T11:48:00Z")
    PP.COMPANY = K.AGENCY
    PP.normalize_ooxml(os.path.join(golden, K.BOOK), K.PLANNER, K.PLANNER, "2026-11-25T10:05:00Z",
                       "2026-11-30T18:12:00Z", title="Plano de televisão para jovens dadores 2027", excel=True)
    PP.normalize_ooxml(os.path.join(golden, K.DECK), K.PLANNER, K.PLANNER, "2026-11-26T15:30:00Z",
                       "2026-12-01T11:48:00Z", title="Esquema de televisão para jovens dadores, abril de 2027")
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, %s, %s, the %s, the channels, their sales houses, "
           "programmes, advertisers, panel members and people are fictional; the records follow the forms of a "
           "Portuguese television audience panel's client files, the channels' commercial as-run logs and booking "
           "extracts, a media agency's schedules and price compilation, and a blood donor association's booking "
           "portal" % (K.ORG, K.AGENCY, K.PANEL_CO, K.JIC))
    return {
        "task": "task270",
        "title": "%s: the television schedule for the April 2027 young donor campaign" % K.ORG,
        "domain": "Marketing & Consumer Research (media reach, frequency and audience measurement)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": [K.BOOK, K.DECK],
        "provenance": {name: {"source": src, "date": "2026-10-26", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "Schedule %s (three-plus reach %.1f%% of adults 18 to 34, %.1f points ahead of schedule %s)" % (
            fig["call"]["schedule"], fig["call"]["reach3_pct"][fig["call"]["schedule"]], fig["call"]["lead_points"],
            fig["call"]["runner_up"]),
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
