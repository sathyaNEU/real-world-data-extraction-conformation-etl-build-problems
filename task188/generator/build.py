"""Build task188: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task188/generator/build.py              everything
    python3 task188/generator/build.py --out DIR    the pack only, into DIR
    python3 task188/generator/build.py --no-checks  the pack, goldens and figures only"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cases as C          # noqa: E402
import docs as D           # noqa: E402
import pack as P           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "db": R.DB, "county": D.COUNTY, "protocol": D.PROTOCOL, "contract": D.CONTRACT, "dictionary": D.DICTIONARY,
    "register": P.REGISTER, "zonemap": P.ZONEMAP, "cases": C.LOG, "weather": P.WEATHER, "birds": P.BIRDS,
    "flights": P.FLIGHTS, "manifest": P.MANIFEST,
}
DISTRACTORS = ("weather", "birds", "flights")
CDT = dt.timezone(dt.timedelta(hours=-5))


def world():
    sim = R.simulate()
    flat = R.number_pools(sim)
    return dict(sim=sim, flat=flat, cases=C.build())


def county_week32(flat):
    return sorted((q for q in flat if q["lab"] == "county" and q["year"] == 2026 and q["week"] == 32),
                  key=lambda q: q["sample_no"])


def build(out, quiet=False, w=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = w or world()
    sim, flat, rows = w["sim"], w["flat"], w["cases"]
    R.write_db(p("db"), sim, flat)
    c32 = county_week32(flat)
    D.write_county_report(p("county"), c32, None)
    D.write_protocol(p("protocol"))
    D.write_contract(p("contract"))
    D.write_dictionary(p("dictionary"))
    P.write_register(p("register"), sim["sites"])
    P.write_zonemap(p("zonemap"))
    C.write(p("cases"), rows)
    P.write_weather(p("weather"))
    P.write_birds(p("birds"))
    P.write_flights(p("flights"))
    n_tn = len(sim["tn"])
    entries = [
        (FILES["db"], "Field database: sites, trap-nights, catches, pools and test results, 2024 season to the "
                      "trap-nights of 11 August 2026 (%d trap-night records)" % n_tn, "RCVCD field database",
         "2026-08-17 08:20", n_tn),
        (FILES["county"], "County laboratory RT-PCR results for the pools collected 11 and 12 August 2026",
         "Rindal County Public Health Laboratory", "2026-08-14", len(c32)),
        (FILES["protocol"], "Surveillance and adult control protocol, 2026 season, revision 1", "RCVCD",
         "2026-06-26", ""),
        (FILES["contract"], "Aerial ULV adulticide agreement, 2026 season", "RCVCD and %s" % W.APPLICATOR,
         "2026-03-09", ""),
        (FILES["dictionary"], "Field database data dictionary", "RCVCD", "2026-08-17", ""),
        (FILES["register"], "Site register 2026: trap sites, legacy code crosswalk, zone sections",
         "RCVCD", "2026-06-15", len(sim["sites"])),
        (FILES["zonemap"], "Treatment zones from 1 May 2026", "RCVCD", "2026-05-01", len(W.ZONES)),
        (FILES["cases"], "West Nile virus human case log, 2026", W.HEALTH, "2026-08-14", len(rows)),
        (FILES["weather"], "Daily weather, Fjelstad Regional Airport", "airport weather station daily summary",
         "2026-08-16", len(P.weather_rows())),
        (FILES["birds"], "Dead bird reports to the district's hotline, with test results", "RCVCD", "2026-08-16",
         len(P.bird_rows())),
        (FILES["flights"], "Aerial blocks designated and flown, 2024 to 2026", "RCVCD and %s" % W.APPLICATOR,
         "2026-08-14", len(P.FLIGHT_ROWS)),
    ]
    P.write_manifest(p("manifest"), entries)
    surv = W.PEOPLE["surv"][0]
    PP.normalize_ooxml(p("register"), surv, surv, "2026-04-09T15:12:40Z", "2026-06-15T19:47:05Z", excel=True)
    PP.normalize_ooxml(p("cases"), W.PEOPLE["epi"][0], W.PEOPLE["epi"][0], "2026-06-04T14:31:09Z",
                       "2026-08-14T21:06:52Z", excel=True)
    PP.normalize_pdf(p("protocol"), b"D:20260427101522-05'00'", b"D:20260626154809-05'00'")
    PP.normalize_pdf(p("contract"), b"D:20260309141007-05'00'", b"D:20260309141007-05'00'")
    PP.normalize_pdf(p("county"), b"D:20260814153344-05'00'", b"D:20260814153344-05'00'")
    stamp = dt.datetime(2026, 8, 17, 8, 34, tzinfo=CDT).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files" % (out, len(os.listdir(out))))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 8, 17, 8, 41, 12)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    w = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    fig = DL.figures(os.path.join(root, "target"))
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    DL.write_chart(os.path.join(gold, DL.CHART), fig)
    DL.write_memo(os.path.join(gold, DL.MEMO), fig)
    DL.write_workbook(os.path.join(gold, DL.WORKBOOK), fig)
    surv = W.PEOPLE["surv"][0]
    PP.normalize_pdf(os.path.join(gold, DL.MEMO), b"D:20260817113415-05'00'", b"D:20260817115902-05'00'")
    PP.normalize_ooxml(os.path.join(gold, DL.WORKBOOK), surv, surv, "2026-08-17T15:02:44Z", "2026-08-17T16:51:30Z",
                       excel=True)
    stamp = dt.datetime(2026, 8, 17, 12, 4, tzinfo=CDT).timestamp()
    for f in os.listdir(gold):
        os.utime(os.path.join(gold, f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    w["fig"] = fig
    return w


def main():
    import checks as CK
    import verify as V
    w = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), w, os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))), allh[:16]))
    import zipfile
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--no-checks", action="store_true", help="build the pack, goldens and figures only")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    elif a.no_checks:
        everything(TASK)
    else:
        main()
