"""Build task269: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task269/generator/build.py              everything
    python3 task269/generator/build.py --out DIR    the pack only, into DIR
    python3 task269/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

import numpy as np   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A       # noqa: E402
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2026, 12, 2, 15, 18)            # the working pack, assembled by the examinations office
MTIME = calendar.timegm(EXPORT.timetuple())


def feedback(w, seed):
    r = np.random.default_rng([seed, 51])
    out = []
    for st in K.STATIONS26:
        out.append((st[0], st[2], int(r.integers(52, 71)), float(np.round(r.uniform(3.4, 4.6), 1)),
                    float(np.round(r.uniform(3.2, 4.5), 1)), int(r.integers(64, 97))))
    return out


def write_sp_invoices(path, seed, b):
    """The simulated patient agency's invoices for the 2026 sittings: one invoice a sitting day, a line a station
    a session for every station whose case needs a simulated patient."""
    import openpyxl
    r = np.random.default_rng([seed, 52])
    rows = []
    inv = iter(range(4417, 9999))
    res = {c["code"]: c["resources"] for c in b["cases"]}
    may = [(st[0], st[5]) for st in K.STATIONS26]
    aug = [(u["station"], res[u["code"]]) for u in b["usage"] if u["date"] == b["sit_dates"][("Aug", 2026)]]
    for dd, sessions, stations in ((K.SIT26[0], ("AM", "PM"), may), (K.SIT26[1], ("AM", "PM"), may),
                                   (b["sit_dates"][("Aug", 2026)], ("AM",), aug)):
        no = "CSA-%d" % next(inv)
        when = dd + dt.timedelta(days=int(r.integers(9, 20)))
        for sno, need in stations:
            if need not in W.SP_NEED:
                continue
            for s in sessions:
                rate = 168.0 if s == "AM" else 152.0
                rows.append([no, when, dd, sno, s, 1, rate, rate])
        rows.append([no, when, dd, None, "Travel", 1, 0.0, float(np.round(r.uniform(180, 420), 2))])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Invoice lines"
    R._sheet(ws, ["Invoice", "Invoice date", "Exam date", "Station", "Session", "Simulated patients", "Rate (EUR)",
                  "Amount (EUR)"], rows, [12, 12, 12, 9, 9, 18, 11, 13], date_cols=(1, 2))
    wb.save(path)
    return len(rows)


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.marks(seed)
    w["seed"] = seed
    b = W.bank(seed)
    e = W.examiners(seed)
    alloc = R.allocation(e, seed)
    n = {}
    n["marks"] = R.write_marks(p("marks"), w, alloc)
    n["global"] = R.write_global(p("global"), w, alloc)
    n["stations"] = R.write_station_sheet(p("stations"))
    n["examiners26"] = R.write_allocation(p("examiners26"), alloc)
    n["bank"] = R.write_bank(p("bank"), b)
    n["usage"] = R.write_usage(p("usage"), b)
    n["register"] = R.write_register(p("register"), e)
    n["availability"] = R.write_availability(p("availability"), e)
    n["training"] = R.write_training(p("training"), e)
    n["sp_invoices"] = write_sp_invoices(p("sp_invoices"), seed, b)
    y = W.station_marks(w)
    n_pass, n_fail, _ = A.pass_fail(w, y)
    DC.write_policy(p("policy"))
    DC.write_minutes(p("minutes"), n_pass, n_fail)
    DC.write_migration(p("migration"), b)
    DC.write_feedback(p("feedback"), feedback(w, seed))
    DC.write_plan(p("plan"))
    import docx as _docx
    n["plan_words"] = sum(len(par.text.split()) for par in _docx.Document(p("plan")).paragraphs)
    from pypdf import PdfReader
    for k in ("policy", "minutes", "migration", "feedback"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    DC.write_contents(p("contents"), contents(n))
    PP.COMPANY = K.UNIVERSITY
    PP.normalize_ooxml(p("stations"), "Examinations Office", "Examinations Office", "2026-04-27T10:12:44Z",
                       "2026-05-08T15:40:19Z", excel=True)
    PP.normalize_ooxml(p("examiners26"), "Examinations Office", "Examinations Office", "2026-04-30T09:05:31Z",
                       "2026-05-11T16:22:07Z", excel=True)
    PP.normalize_ooxml(p("bank"), "Assessment Item Bank", "Assessment Item Bank", "2026-11-30T08:14:02Z",
                       "2026-11-30T08:14:02Z", excel=True)
    PP.normalize_ooxml(p("register"), "Examinations Office", "Examinations Office", "2019-02-11T11:20:16Z",
                       "2026-11-30T12:41:55Z", excel=True)
    PP.normalize_ooxml(p("sp_invoices"), "Finance", "Finance", "2026-09-15T14:02:10Z", "2026-09-15T14:09:48Z",
                       excel=True)
    PP.normalize_ooxml(p("plan"), K.PEOPLE["skills"], K.PEOPLE["skills"], "2026-11-05T09:41:00Z",
                       "2026-11-12T16:03:00Z")
    PP.normalize_pdf(p("policy"), b"D:20260923112041+01'00'", b"D:20260924094417+01'00'")
    PP.normalize_pdf(p("minutes"), b"D:20260514170212+01'00'", b"D:20260515103355+01'00'")
    PP.normalize_pdf(p("migration"), b"D:20251202142608+00'00'", b"D:20251202150131+00'00'")
    PP.normalize_pdf(p("feedback"), b"D:20260618093122+01'00'", b"D:20260618101507+01'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return {"marks": w, "bank": b, "examiners": e, "alloc": alloc, "n": n, "seed": seed, "pass": (n_pass, n_fail)}


def contents(n):
    F = K.FILES
    pg = lambda k: "%d pages" % n[k + "_pages"] if n[k + "_pages"] != 1 else "1 page"
    rw = lambda k: "{:,} rows".format(n[k])
    return [
        ["File", "What it holds", "Kept by", "As at", "Size"],
        [F["policy"], "Assessment policy, version 7", "Head of Assessment", "2026-09-23", pg("policy")],
        [F["plan"], "Final OSCE 2027: delivery plan (draft)", "Director of Clinical Skills", "2026-11-12",
         "%d words" % n["plan_words"]],
        [F["marks"], "Final OSCE May 2026: every examiner's marks, both days", "OSCE system", "2026-05-14",
         rw("marks")],
        [F["global"], "Final OSCE May 2026: every examiner's global grades", "OSCE system", "2026-05-14",
         rw("global")],
        [F["stations"], "Final OSCE May 2026: station sheet", "Examinations Office", "2026-05-08",
         "%d stations" % n["stations"]],
        [F["examiners26"], "Final OSCE May 2026: examiners by station", "Examinations Office", "2026-05-11",
         rw("examiners26")],
        [F["minutes"], "Board of examiners, final OSCE: minutes", "Examinations Office", "2026-05-14", pg("minutes")],
        [F["bank"], "OSCE case bank", "Assessment Item Bank", "2026-11-30", "{:,} cases".format(n["bank"])],
        [F["usage"], "Cases set at each final OSCE sitting since 2021", "Examinations Office", "2026-09-01",
         rw("usage")],
        [F["migration"], "Case bank migration: cut-over report", "Assessment Technology", "2025-12-02",
         pg("migration")],
        [F["register"], "Examiner register", "Examinations Office", "2026-11-30", "{:,} examiners".format(n["register"])],
        [F["training"], "Examiner training and refresher sessions since 2021", "Training team", "2026-11-30",
         rw("training")],
        [F["availability"], "Final OSCE 2027 examiner availability form: responses", "Examinations Office",
         "2026-11-27", rw("availability")],
        [F["sp_invoices"], "Simulated patient agency invoices, 2026 sittings", "Finance", "2026-09-15",
         rw("sp_invoices")],
        [F["feedback"], "Final OSCE 2026: candidate feedback", "Student Experience Office", "2026-06-18",
         pg("feedback")],
    ]


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=W.SEED)
    a = ap.parse_args()
    if a.out:
        w = build(a.out, a.seed)
        print("pack:", w["n"])
        return
    target = os.path.join(TASK, "target")
    w = build(target)
    print("pack:", w["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), w)
    if a.golden:
        return
    import checks
    checks.run(target, w)
    r = os.system("python3 %s %s %s" % (os.path.join(HERE, "verify.py"), target, os.path.join(TASK, "golden")))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
