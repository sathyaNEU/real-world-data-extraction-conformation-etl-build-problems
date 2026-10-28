"""Build task268: the evidence pack into <task>/target, the goldens into <task>/golden, submission.md, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task268/generator/build.py              everything
    python3 task268/generator/build.py --out DIR    the pack only, into DIR"""
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
import zipfile       # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import pack as PK          # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())
PDF_DATES = {"terms": ("D:20261006151204+01'00'", "D:20261006151204+01'00'"),
             "standard": ("D:20251124102733+00'00'", "D:20251124102733+00'00'"),
             "quote": ("D:20260922093018+01'00'", "D:20260922093018+01'00'")}


def build_pack(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w, pk, n = PK.write_pack(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(p("exposure"), "Pricing MI", "Pricing MI", "2023-02-06T09:14:52Z", "2026-10-02T07:41:09Z", excel=True)
    PP.normalize_ooxml(p("aggregator"), "Distribution MI", "Distribution MI", "2025-11-03T08:20:41Z",
                       "2026-10-05T08:02:17Z", excel=True)
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(p(k), c.encode(), m.encode())
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return w, pk, n


def build_golden(target, golden, gen_dir):
    import analysis as A
    import deliver as D
    import writeup as WU
    G = A.Golden(target)
    R = G.run()
    R["_G"] = G
    F = D.figures(R)
    text, extras = WU.write(R, F)
    F["writeup"] = extras
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    D.write_workbook(os.path.join(golden, K.GOLDEN), R, F)
    D.write_deck(os.path.join(golden, K.DECK), R, F)
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), K.PEOPLE["actuary"], K.PEOPLE["actuary"], "2026-10-12T13:05:44Z",
                       "2026-10-14T15:52:10Z", excel=True)
    PP.normalize_ooxml(os.path.join(golden, K.DECK), K.PEOPLE["actuary"], K.PEOPLE["actuary"], "2026-10-13T09:31:02Z",
                       "2026-10-14T16:02:37Z", title="Telematics pilot 2027")
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return R, F


def write_metadata(n, R):
    prov = {}
    synth = ("constructed by the task generator (seeded); Corriven Insurance, its sales regions, policies, claims, "
             "representatives, staff and suppliers are fictional; postcode districts are real UK districts, used only "
             "to place the fictional book")
    about = {
        "claims": ("Corriven's claims system extract of every motor claim notified to the end of 30 September 2026 on "
                   "accidents from 1 January 2019, one row a claim", "2026-10-01"),
        "reps": ("the claims system's table of claimant representatives", "2026-10-01"),
        "districts": ("the 2025 drawing of the sales regions by postcode district", "2025-01-06"),
        "exposure": ("the pricing mart's earned exposure by month, region, product and cover, 2019 to 2025", "2026-10-02"),
        "terms": ("the chief underwriting officer's terms for the 2027 telematics pilot", "2026-10-06"),
        "standard": ("the Motor Claims Reserving Standard, version 4", "2025-11-24"),
        "thread": ("the planning thread for the pilot paper", "2026-10-09"),
        "inforce": ("policy admin's file of the vehicles on terms in force at 30 September 2026", "2026-10-01"),
        "changes": ("policy admin's log of mid-term changes processed to 30 September 2026", "2026-10-01"),
        "quote": ("the telematics supplier's quotation", "2026-09-22"),
        "aggregator": ("the distribution team's aggregator quote and sales report", "2026-10-05"),
    }
    for k, fn in K.FILES.items():
        prov[fn] = {"source": synth, "covers": about[k][0], "date": about[k][1],
                    "licence": "CC0 1.0 (constructed for this task)",
                    "made": "generated by task268/generator (pack.py, docs.py) from world.py's seeded records"}
    m = {"task": "task268",
         "title": "Corriven Insurance: the sales regions for the 2027 private-car telematics pilot",
         "domain": "Actuarial Science & Insurance (claims frequency and severity)",
         "objective": "Descriptive & Distribution Analysis",
         "answer": "%s and %s host the pilot" % tuple(R["call"]),
         "deliverables": list(K.DELIVERABLES),
         "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
         "rows": sorted((K.FILES[k], v) for k, v in n.items() if k in ("claims", "inforce", "changes")),
         "provenance": prov}
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(m, f, indent=1)
        f.write("\n")


def digest(d):
    out = {}
    for root, _, files in os.walk(d):
        for f in sorted(files):
            p = os.path.join(root, f)
            out[os.path.relpath(p, d)] = hashlib.md5(open(p, "rb").read()).hexdigest()
    return out


def cut_zip(target, path):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.out:
        build_pack(a.out)
        return
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    w, pk, n = build_pack(target)
    R, F = build_golden(target, golden, HERE)
    write_metadata(n, R)
    import checks
    rows = checks.run(TASK)
    bad = [r for r in rows if not r[1]]
    for r in rows:
        print("%s  %-28s %s" % ("PASS" if r[1] else "FAIL", r[0], r[2]))
    print("checks: %d assertions, %d failed" % (len(rows), len(bad)))
    import verify
    vbad = verify.run(target, os.path.join(HERE, "figures.json"))
    print("verify: %s" % ("PASS" if not vbad else "FAIL " + "; ".join(vbad)))
    scratch = os.path.join(TASK, ".rebuild")
    build_pack(os.path.join(scratch, "target"))
    a1, a2 = digest(target), digest(os.path.join(scratch, "target"))
    shutil.rmtree(scratch)
    same = a1 == a2
    print("rebuild: %s" % ("byte-identical" if same else "DIFFERS " + ", ".join(k for k in a1 if a1[k] != a2.get(k))))
    cut_zip(target, os.path.join(TASK, "target.zip"))
    for k, v in sorted(a1.items()):
        print("  %s  %s" % (v, k))
    sys.exit(1 if (bad or vbad or not same) else 0)


if __name__ == "__main__":
    main()
