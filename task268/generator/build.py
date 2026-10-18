"""Build task268: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task268/generator/build.py              everything
    python3 task268/generator/build.py --out DIR    the pack only, into DIR
    python3 task268/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askworld as AW      # noqa: E402
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2026, 10, 6, 16, 42)               # Location Analytics' data pack, Eastern time
MTIME = calendar.timegm((EXPORT + dt.timedelta(hours=4)).timetuple())


def world(seed=W.SEED):
    T = W.build(seed)
    T["listings"] = AW.listings(T, seed)
    T["locators"], T["stores"] = AW.locators(T, seed)
    return T


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = world(seed)
    n = {}
    n["od_main"], n["od_aux"] = R.write_od(p("od_main"), p("od_aux"), T)
    n["survey"] = R.write_survey(p("survey"), T)
    n["population"] = R.write_population(p("population"), T)
    n["gazetteer"] = R.write_gazetteer(p("gazetteer"), T)
    n["delineation"] = R.write_delineation(p("delineation"), T)
    n["cores"] = R.write_cores(p("cores"), T)
    n["acs_commute"] = R.write_acs_commute(p("acs_commute"), T)
    n["cbp"] = R.write_cbp(p("cbp"), T)
    n["expansion"] = R.write_expansion(p("expansion"))
    n["listings"] = R.write_listings(p("listings"), T["listings"])
    n["locators"] = R.write_locators(p("locators"), T["locators"])
    D.write_board(p("board"))
    D.write_codebook(p("codebook"))
    D.write_od_notes(p("od_notes"), n["od_main"], n["od_aux"])
    from pypdf import PdfReader
    for k in ("board", "codebook", "od_notes"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    D.write_manifest(p("manifest"), manifest(n))
    PP.COMPANY = K.ORG + " Inc."
    PP.normalize_ooxml(p("delineation"), "Carolyn Cook", "Carolyn Cook", "2026-09-08T14:12:40Z", "2026-09-08T14:31:02Z",
                       excel=True)
    PP.normalize_ooxml(p("cores"), "Network Expansion", "Carolyn Cook", "2026-08-21T19:02:11Z", "2026-09-15T13:47:55Z",
                       excel=True)
    PP.normalize_ooxml(p("expansion"), "Network Expansion", "Network Expansion", "2023-02-14T15:20:07Z",
                       "2026-08-28T20:11:43Z", excel=True)
    PP.normalize_pdf(p("board"), b"D:20260917084512-04'00'", b"D:20260917091930-04'00'")
    PP.normalize_pdf(p("codebook"), b"D:20261002103108-04'00'", b"D:20261002103108-04'00'")
    PP.normalize_pdf(p("od_notes"), b"D:20261002152647-04'00'", b"D:20261002155211-04'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["n"] = n
    return T


def manifest(n):
    F = K.FILES
    pg = lambda k: "%d page%s" % (n[k + "_pages"], "" if n[k + "_pages"] == 1 else "s")
    LA = "Location Analytics"
    return [
        (F["board"], "Board paper BD-2026-41: how the 2027 weekday pilot metro is chosen", "Network Expansion", "2026-09-17",
         pg("board"), "internal"),
        (F["cores"], "Planning map: the six candidate cores' census tracts", "Network Expansion", "2026-09-15",
         "%d tracts" % n["cores"], "internal"),
        (F["od_main"], "Regional commuting extract, LODES 8 JT01 2022, tract pairs touching a core, main part", LA,
         "2026-10-02", "%d rows" % n["od_main"], "public domain (U.S. Census Bureau)"),
        (F["od_aux"], "Regional commuting extract, auxiliary part (workers living in another state)", LA, "2026-10-02",
         "%d rows" % n["od_aux"], "public domain (U.S. Census Bureau)"),
        (F["od_notes"], "Notes on the commuting extract", LA, "2026-10-02", pg("od_notes"), "internal"),
        (F["survey"], "Work Location Survey public-use file, waves October 2025 to September 2026", "WLS Consortium",
         "2026-10-02", "%d rows" % n["survey"], "public-use file licence (attribution)"),
        (F["codebook"], "Work Location Survey public-use file codebook, release 2026-2", "WLS Consortium", "2026-10-02",
         pg("codebook"), "public-use file licence (attribution)"),
        (F["population"], "ACS 2018-2022 five-year, B01003 total population, tracts of the six metropolitan areas",
         "U.S. Census Bureau", "2023-12-07", "%d tracts" % n["population"], "public domain"),
        (F["gazetteer"], "2022 census tract gazetteer, tracts of the six metropolitan areas", "U.S. Census Bureau",
         "2022-10-31", "%d tracts" % n["gazetteer"], "public domain"),
        (F["delineation"], "CBSA delineation list, July 2023, the candidate areas and their neighbours",
         "U.S. Census Bureau / OMB", "2023-07-21", "%d counties" % n["delineation"], "public domain"),
        (F["acs_commute"], "ACS 2018-2022 five-year, B08301 means of transportation to work, by county of residence",
         "U.S. Census Bureau", "2023-12-07", "%d counties" % n["acs_commute"], "public domain"),
        (F["cbp"], "County Business Patterns 2022, establishments and employment by sector", "U.S. Census Bureau",
         "2024-06-27", "%d rows" % n["cbp"], "public domain"),
        (F["expansion"], "%s launch log" % K.HOME_METRO, "Network Expansion", "2026-08-28", "%d stores" % n["expansion"],
         "internal"),
        (F["listings"], "Retail and flex space listings in the six central counties, export of 1 October 2026",
         "Commercial listing service (Real Estate team's subscription)", "2026-10-01", "%d rows" % n["listings"],
         "subscriber licence, internal use"),
        (F["locators"], "Competitors' store locators, weekly scrapes 7 January to 30 September 2026", "Market Intelligence",
         "2026-09-30", "%d rows" % n["locators"], "internal"),
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
        T = build(a.out, a.seed)
        print("pack:", T["n"])
        return
    target = os.path.join(TASK, "target")
    T = build(target)
    print("pack:", T["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
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
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
