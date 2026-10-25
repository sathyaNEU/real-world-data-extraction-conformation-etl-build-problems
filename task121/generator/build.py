"""Build task121: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task121/generator/build.py              everything
    python3 task121/generator/build.py --out DIR    the pack only, into DIR
    python3 task121/generator/build.py --golden     the pack and the goldens, no checks"""
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
import context as CX       # noqa: E402
import docs as DC          # noqa: E402
import pack as PK          # noqa: E402
import survey as SV        # noqa: E402
import world as Wd         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())


def survey_stats(sv):
    st = {"batches": {}, "issued": {}, "returned": {}, "overall": {}, "items": {}}
    for wave in (2025, 2026):
        bs = [b for b in sv.batches if b["wave"] == wave]
        st["batches"][wave] = len(bs)
        st["issued"][wave] = sum(b["issued"] for b in bs)
        st["returned"][wave] = sum(b["post"] + b["online"] for b in bs)
        rs = [x for x in sv.resp if x["wave"] == wave]
        w = sum(x["weight"] for x in rs)
        st["overall"][wave] = 100.0 * sum(x["weight"] for x in rs if x["overall"] >= 4) / w
        for q, _ in K.ITEMS + [K.ITEM_2026]:
            if q == "q5k" and wave == 2025:
                continue
            ans = [x for x in rs if x["R"].get(q) not in (None, 9)]
            st["items"].setdefault(q, {})[wave] = 100.0 * sum(x["weight"] for x in ans if x["R"][q] >= 4) / \
                sum(x["weight"] for x in ans)
    return st


def build(out, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = Wd.World()
    sv = SV.Survey(w)
    n = {}
    for key, fn in (("responses", lambda: PK.responses(sv)), ("fieldwork", lambda: PK.fieldwork(sv)),
                    ("timetable", lambda: PK.timetable(w)), ("movements", lambda: PK.movements(w)),
                    ("loadweigh", lambda: PK.loadweigh(w, sv)), ("formations", lambda: PK.formations(w)),
                    ("crew_worked", lambda: PK.crew_as_worked(w)), ("fares", lambda: PK.fares(w)),
                    ("stations", PK.stations), ("contacts", CX.contacts), ("delays", lambda: CX.delays(w))):
        head, rows = fn()
        PK.write_csv(p(key), head, rows)
        n[key] = len(rows)
    (h1, r1), (h2, r2) = PK.crew_live(w)
    PK.write_csv(p("crew_roster"), h1, r1)
    PK.write_csv(p("crew_amend"), h2, r2)
    n["crew_roster"], n["crew_amend"] = len(r1), len(r2)
    st = survey_stats(sv)
    DC.write_technote(p("technote"), st)
    DC.write_topline(p("topline"), st)
    DC.write_requirement(p("requirement"), st)
    DC.write_schedule(p("standards"))
    DC.write_fleet(p("fleet"), w)
    DC.write_dictionary(p("dictionary"))
    return dict(w=w if keep else None, sv=sv if keep else None, counts=n, stats=st)


PDF_DATES = {"technote": ("D:20260511101500+01'00'", "D:20260511101500+01'00'"),
             "topline": ("D:20260511102000+01'00'", "D:20260511102000+01'00'"),
             "requirement": ("D:20261002143000+01'00'", "D:20261002143000+01'00'"),
             "standards": ("D:20260401090000+01'00'", "D:20260401090000+01'00'")}
OOXML = {"fleet": (K.PEOPLE["fleet"], K.PEOPLE["fleet"], "2019-12-02T09:12:00Z", "2026-09-22T15:48:00Z",
                   "Fleet register", True)}


def finish(out):
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.OPERATOR_LTD
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.OPERATOR_LTD
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), K.PEOPLE["contract"], K.PEOPLE["contract"],
                       "2026-10-26T09:05:00Z", "2026-11-06T16:40:00Z", title="Satisfaction fall, spring 2026",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, the %s, %s, their network, people and records are "
           "fictional; the records follow the forms of a train operator's working timetable, train movement, "
           "load-weigh, formation and crew exports and of a customer satisfaction tracker's data file"
           % (K.OPERATOR, K.AUTHORITY, K.AGENCY))
    return {
        "task": "task121",
        "title": "%s: which service driver accounts for most of the fall in passengers satisfied, spring 2025 to "
                 "spring 2026" % K.OPERATOR,
        "domain": "Marketing & Consumer Research (customer satisfaction driver analysis)",
        "objective": "Root-Cause Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-23", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": fig["call"]["sentence"],
    }


def main_build(target, golden):
    import deliver as DV
    b = build(target, keep=True)
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
    a = ap.parse_args()
    if a.out:
        b = build(a.out)
        finish(a.out)
        print(b["counts"])
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"))
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
