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
PDF_DATES = {"agreement": ("D:20260512094118+01'00'", "D:20260512094118+01'00'"),
             "terms": ("D:20251218112730+00'00'", "D:20251218112730+00'00'"),
             "board": ("D:20260630171544+01'00'", "D:20260630171544+01'00'")}


def build_pack(out, w=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w, n = PK.write_pack(out, w)
    p = lambda k: os.path.join(out, K.FILES[k])
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(p("master"), "Range Data", "Katy Kinnegan", "2023-01-16T10:02:11Z", "2026-12-02T15:47:30Z",
                       excel=True)
    PP.normalize_ooxml(p("deals"), K.PEOPLE["buyer"], K.PEOPLE["buyer"], "2025-12-08T09:15:40Z", "2026-12-21T16:33:05Z",
                       excel=True)
    PP.COMPANY = "Lisnagree Research"
    PP.normalize_ooxml(p("tracker"), "Lisnagree Research", "Lisnagree Research", "2026-05-25T13:20:00Z",
                       "2026-12-04T11:06:52Z", excel=True)
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(p("brief"), K.PEOPLE["brand"], K.PEOPLE["brand"], "2027-01-08T14:40:00Z", "2027-01-11T10:12:00Z",
                       title="Roastery sampling 2027: brief")
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(p(k), c.encode(), m.encode())
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return w, n


def build_golden(target, golden, gen_dir):
    import analysis as A
    import deliver as D
    import writeup as WU
    G = A.Golden(target)
    R = G.run()
    F = D.figures(R)
    text, _ = WU.write(R, F)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    D.write_deck(os.path.join(golden, K.DECK), R, F)
    D.write_csv(os.path.join(golden, K.CSV_OUT), R)
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(os.path.join(golden, K.DECK), K.PEOPLE["insight"], K.PEOPLE["insight"], "2027-01-18T09:41:00Z",
                       "2027-01-21T16:28:00Z", title="Roastery sampling 2027")
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
    synth = ("constructed by the task generator (seeded); Corcally's, its stores, members, suppliers, brands, Faircourt "
             "Merchant Services, the guest roasters and every record are fictional")
    about = {
        "till": ("the data warehouse's coffee category till lines for 2026, one row a line", "2027-01-08"),
        "online": ("the online shop's order history export with its coffee lines, orders placed from 1 December 2025",
                   "2027-01-08"),
        "register": ("the Corcally's Rewards card register extract", "2027-01-08"),
        "settle": ("Faircourt Merchant Services' settlement detail for Corcally & Sons Limited, 2026", "2027-01-07"),
        "agreement": ("Faircourt's merchant service agreement, Schedules 2 to 4", "2026-05-12"),
        "master": ("the buying team's product master for the coffee range", "2026-12-02"),
        "terms": ("the Corcally's Rewards terms and conditions, January 2026 edition", "2025-12-18"),
        "brief": ("the Roastery team's brief for the 2027 sampling", "2027-01-11"),
        "labels": ("the Drumsallagh coffee counter's scale label log for 2026", "2027-01-05"),
        "board": ("the coffee counter's price board as displayed in 2026", "2026-06-30"),
        "deals": ("the coffee buyer's multibuy deal log for 2026", "2026-12-21"),
        "census": ("2022 census households by size for the small areas in the stores' catchment", "2023-05-30"),
        "tracker": ("a research agency's coffee brand tracker for Corcally's, May and November 2026 waves",
                    "2026-12-04"),
    }
    for k, fn in K.FILES.items():
        prov[fn] = {"source": synth, "covers": about[k][0], "date": about[k][1],
                    "licence": "CC0 1.0 (constructed for this task)",
                    "made": "generated by task268/generator (pack.py, docs.py) from world.py's seeded records"}
    m = {"task": "task268",
         "title": "Corcally's: the rival coffee brand whose homes get the 2027 Roastery sampling",
         "domain": "Marketing & Consumer Research",
         "objective": "Descriptive & Distribution Analysis",
         "decision": "the rival coffee brand whose 2026 buying homes least often also bought Corcally's Roastery",
         "answer": "%s's homes get the 2027 Roastery sampling" % K.BRAND_NAME[R["call"]],
         "deliverables": list(K.DELIVERABLES),
         "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
         "rows": sorted([(K.FILES["till"], n["till"]), (K.FILES["settle"], n["settle"]), (K.FILES["labels"], n["labels"]),
                         (K.FILES["register"], n["register"])]),
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
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    if a.out:
        build_pack(a.out)
        return
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    w, n = build_pack(target)
    R, F = build_golden(target, golden, HERE)
    write_metadata(n, R)
    import checks
    rows = checks.run(TASK, world=w)
    bad = [r for r in rows if not r[1]]
    for r in rows:
        print("%s  %-74s %s" % ("PASS" if r[1] else "FAIL", r[0], r[2]))
    print("checks: %d assertions, %d failed" % (len(rows), len(bad)))
    import verify
    vbad = verify.run(target, os.path.join(HERE, "figures.json"))
    print("verify: %s" % ("PASS" if not vbad else "FAIL " + "; ".join(vbad)))
    same = True
    if not a.no_rebuild:
        scratch = os.path.join(TASK, ".rebuild")
        build_pack(os.path.join(scratch, "target"))
        a1, a2 = digest(target), digest(os.path.join(scratch, "target"))
        shutil.rmtree(scratch)
        same = a1 == a2
        print("rebuild: %s" % ("byte-identical" if same else "DIFFERS " + ", ".join(k for k in a1 if a1[k] != a2.get(k))))
    cut_zip(target, os.path.join(TASK, "target.zip"))
    for k, v in sorted(digest(target).items()):
        print("  %s  %s" % (v, k))
    sys.exit(1 if (bad or vbad or not same) else 0)


if __name__ == "__main__":
    main()
