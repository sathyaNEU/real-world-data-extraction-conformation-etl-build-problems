"""Build task274: the evidence pack into <task>/target, the golden into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task274/generator/build.py              everything
    python3 task274/generator/build.py --out DIR    the pack only, into DIR
    python3 task274/generator/build.py --golden     the pack and the golden, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
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
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("contents", "This list."),
    ("plan", "The 2025 wave's analysis plan (version 2.1, 14 March 2025)."),
    ("persons", "Examined sample persons: county, examination date and session, age, sex, race and ethnicity, "
                "examination weight."),
    ("results", "MRMC Laboratory Medicine: 25-hydroxyvitamin D results released for the primary serum vials, 2025."),
    ("bridge", "MRMC Laboratory Medicine: the bridging run of December 2025 on the stored duplicate vials."),
    ("tracking", "Specimen tracking export: every event on every vial of the 2025 wave."),
    ("events", "Immunoassay analyzers' middleware event log, 1 December 2024 to 31 December 2025 (UTC)."),
    ("instruments", "The laboratory's instrument register."),
    ("check", "Brennick Reference Measurement Program: participant report for event 2025-B."),
    ("closeout", "Fieldwork close-out of the 2025 wave (20 January 2026)."),
    ("counties", "County codes, MEC stands and adults aged 20 and over."),
    ("dictionary", "Data dictionary of the 2025 wave's files."),
    ("supplements", "Dietary supplement questionnaire: products reported, one row a product line."),
    ("labels", "Label database extract for the products reported."),
    ("rosters", "Screener rosters: every person listed at every screening."),
    ("status", "Sample persons: final interview and examination dispositions, interview weights."),
    ("notice", "Varnholt Diagnostics customer notification CN-25-014 (June 2025)."),
    ("tables2021", "The 2021 wave's county tables (data brief 2022-3)."),
]
DISTRACTORS = ("notice", "tables2021")
STAMPS = {
    "plan": ("2025-03-14T16:05:00Z", "2025-03-14T16:40:00Z"),
    "check": ("2025-11-14T13:00:00Z", "2025-11-14T13:00:00Z"),
    "closeout": ("2026-01-20T15:10:00Z", "2026-01-20T17:25:00Z"),
    "dictionary": ("2026-01-09T14:00:00Z", "2026-01-09T15:30:00Z"),
    "notice": ("2025-06-16T09:00:00Z", "2025-06-16T09:00:00Z"),
    "tables2021": ("2022-08-09T13:30:00Z", "2022-08-09T13:30:00Z"),
    "labels": ("2026-02-17T10:12:00Z", "2026-02-17T10:44:00Z"),
}
AUTHOR = {"labels": K.CENTER}


def pdf_date(iso):
    return ("D:%s%s%s%s%s%s+00'00'" % (iso[0:4], iso[5:7], iso[8:10], iso[11:13], iso[14:16], iso[17:19]))


def stands(w):
    out = []
    for c, (code, name) in enumerate(K.COUNTIES):
        ex = [p for p in w["P"] if p["county"] == c]
        days = len(W.exam_days(c))
        ships = len({p["shipped"] for p in ex if p.get("blood")})
        out.append(dict(name=name, a=K.STANDS[c][0], b=K.STANDS[c][1], days=days - (2 if c == 1 else (2 if c == 5 else 0)),
                        examined=len(ex), blood=sum(1 for p in ex if p.get("blood")), ships=ships,
                        lost=(2 if c in (1, 5) else 0)))
    return out


def build_pack(out, seed=K.SEED):
    os.makedirs(out, exist_ok=True)
    w = W.simulate(seed)
    P = R.Pack(w, seed)
    F = K.FILES
    j = lambda k: os.path.join(out, F[k])
    R.write_csv(j("results"), *P.results_rows())
    R.write_csv(j("bridge"), *P.bridge_rows())
    R.write_csv(j("tracking"), *P.tracking_rows())
    R.write_csv(j("persons"), *P.persons_rows())
    R.write_csv(j("events"), *P.event_rows())
    R.write_csv(j("instruments"), *P.instrument_rows())
    R.write_csv(j("counties"), *P.county_rows())
    R.write_csv(j("supplements"), *P.dsq_rows())
    R.write_csv(j("rosters"), *P.roster_rows())
    R.write_csv(j("status"), *P.status_rows())
    R.write_labels(j("labels"), P.cat)
    DC.write_plan(j("plan"))
    DC.write_check(j("check"), w["check"])
    DC.write_closeout(j("closeout"), stands(w))
    DC.write_dictionary(j("dictionary"))
    DC.write_notice(j("notice"))
    DC.write_tables2021(j("tables2021"))
    DC.write_contents(j("contents"), [(F[k], d) for k, d in CONTENTS])
    for k in ("plan", "check", "closeout", "dictionary", "notice", "tables2021"):
        c, m = STAMPS[k]
        PP.normalize_pdf(j(k), pdf_date(c).encode(), pdf_date(m).encode())
    c, m = STAMPS["labels"]
    PP.normalize_ooxml(j("labels"), AUTHOR["labels"], AUTHOR["labels"], c, m, excel=True)
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (MTIME, MTIME))
    return w, P


def write_metadata(fig):
    src = ("constructed by the task generator (seeded); the Merrivane Health District, its counties, survey, "
           "laboratory, staff, the Brennick Reference Measurement Program, Varnholt Diagnostics and every supplement "
           "brand are fictional; the survey follows the design of a health and nutrition examination survey (MEC "
           "stands, household interview, examination weights) and the laboratory files the shape of a hospital "
           "laboratory information system's and an immunoassay analyzer's exports")
    prov = {name: dict(source=src, date=K.ASSEMBLED.date().isoformat(), licence="CC0 1.0 (constructed for this task)")
            for name in sorted(K.FILES.values())}
    meta = dict(
        answer="Counties opening first: %s" % ", ".join(fig["call"]["counties"]),
        deliverables=[K.GOLDEN],
        distractors=["target/" + K.FILES[k] for k in DISTRACTORS],
        distractor_reasons={
            K.FILES["notice"]: "the manufacturer's statement of what its restandardised lots do on average; the "
                               "wave's results are carried to the reference scale by the laboratory's own check and "
                               "bridging run, not by the notice's average",
            K.FILES["tables2021"]: "the 2021 wave's county shares and response rates, measured by LC-MS/MS at "
                                   "another laboratory; nothing in the 2025 figures is computed from them"},
        domain="Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment)",
        objective="Descriptive & Distribution Analysis",
        provenance=prov)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
        f.write("\n")


def digest(folder):
    h = {}
    for name in sorted(os.listdir(folder)):
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            h[name] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build_pack(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    w, P = build_pack(target)
    import deliver as DL
    golden = os.path.join(TASK, "golden")
    fig = DL.write(target, golden)
    write_metadata(fig)
    if a.golden:
        return
    import checks
    import verify
    failed = checks.run(TASK, w, P)
    ok = verify.run(TASK)
    scratch = os.path.join(TASK, ".rebuild")
    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    build_pack(os.path.join(scratch, "target"))
    DL.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"), figures=False)
    same = digest(target) == digest(os.path.join(scratch, "target")) and \
        digest(golden) == digest(os.path.join(scratch, "golden"))
    shutil.rmtree(scratch)
    print("rebuild byte-identical: %s" % same)
    import zipfile
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(name, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, name), "rb").read())
    print("target.zip %s" % hashlib.md5(open(zp, "rb").read()).hexdigest())
    print("checks failed: %d; verify: %s" % (failed, "PASS" if ok else "FAIL"))
    sys.exit(0 if (failed == 0 and ok and same) else 1)


if __name__ == "__main__":
    main()
