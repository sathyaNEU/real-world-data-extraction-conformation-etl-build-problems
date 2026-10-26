"""Build task184: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build compared
byte for byte, then target.zip cut from the final build.

    python3 task184/generator/build.py              everything
    python3 task184/generator/build.py --out DIR    the pack only, into DIR
    python3 task184/generator/build.py --no-checks  the pack, goldens and figures only
"""
import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import asks as A        # noqa: E402
import deliver as DV    # noqa: E402
import docs as D        # noqa: E402
import ledger as L      # noqa: E402
import metadata as MD   # noqa: E402
import postprocess as PP  # noqa: E402
import records as R     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
DISTRACTORS = (R.FUEL, R.STOCK)


def world():
    """Everything the pack and the goldens are written from, built once."""
    sim = L.materialise()
    t26 = L.entry_table(sim, "FY26")
    for r in t26:
        r["source_interface"] = r["interface"]
    t25 = L.entry_table(sim, "FY25")
    reg = L.register_rows(t26, "FY26")
    accr = A.accruals(sim)
    control = A.ap_control(accr)
    till = A.tills(sim)
    sales = A.sales_control(till)
    log = A.run_log(t25)
    return dict(sim=sim, t26=t26, t25=t25, reg=reg, accr=accr, control=control, till=till,
                sales=sales, log=log)


def build_pack(out, sim, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    c = {}
    ne, nl = R.write_gl(p(R.GL_DB), sim["t26"])
    c["journal_entries (sqlite)"] = ne
    c["journal_lines (sqlite)"] = nl
    c[R.EXCEPTIONS] = R.write_exceptions(p(R.EXCEPTIONS), sim["reg"])
    c[R.FY25_SUMMARY] = R.write_fy25_summary(p(R.FY25_SUMMARY), sim["t25"])
    c[R.UNIT_REGISTER] = R.write_unit_register(p(R.UNIT_REGISTER))
    c[R.CALENDAR] = R.write_calendar(p(R.CALENDAR))
    c[R.ACCOUNTS] = R.write_accounts(p(R.ACCOUNTS))
    c[A.ACCRUALS] = A.write_accruals(p(A.ACCRUALS), sim["accr"])
    c[A.AP_CONTROL] = A.write_ap_control(p(A.AP_CONTROL), sim["control"])
    c[A.SUPPLIERS] = A.write_suppliers(p(A.SUPPLIERS))
    c[A.TILLS] = A.write_tills(p(A.TILLS), sim["till"])
    c[A.SALES_CONTROL] = A.write_sales_control(p(A.SALES_CONTROL), sim["sales"])
    c[A.RUN_LOG] = A.write_run_log(p(A.RUN_LOG), sim["log"])
    c[R.FUEL] = R.write_fuel(p(R.FUEL))
    c[R.STOCK] = R.write_stock(p(R.STOCK))
    monthly = {}
    for r in sim["reg"]:
        key = (W.resolve_unit(r["unit_code"]), r["period"])
        monthly[key] = monthly.get(key, 0) + 1
    D.write_catalogue(p(D.CATALOGUE))
    D.write_platform(p(D.PLATFORM), monthly)
    D.write_dictionary(p(D.DICTIONARY))
    D.write_epos_notes(p(D.EPOS_NOTES))
    for f in (D.CATALOGUE, D.PLATFORM, D.DICTIONARY, D.EPOS_NOTES):
        # the fiction's issue stamps, and no writing-library banner (reduce-house-fixes H1)
        PP.normalize_pdf(p(f), b"D:20260629090000+01'00'", b"D:20260629090000+01'00'")
        c[f] = "document"
    R.write_manifest(p(R.MANIFEST), {k: v for k, v in c.items() if isinstance(v, int)})
    # The platform's own reported exception counts are inputs the organisation publishes, not answers:
    # the exception summary in the operating guide and the manifest's row counts both state them, and
    # Gate B requires them in the pack. Declared here so the leak sweep reads them as stated inputs.
    stated = ["the twelve trading units", "FY26 P1 to P9", "the rounding of each graded figure",
              "journal entries raised as exceptions, by trading unit and fiscal period, as the "
              "monitoring platform reports them"]
    # the sweep matches the figure as it is written, so these carry their thousands separators
    fmt = lambda v: "{:,}".format(int(v))
    stated += [fmt(v) for v in sorted({v for v in monthly.values()})]
    stated += [fmt(sum(monthly.values()))]
    stated += [fmt(v) for v in
               sorted({sum(x for (u, _p), x in monthly.items() if u == code[0]) for code in W.UNITS})]
    MD.write(p(MD.NAME), {k: v for k, v in c.items()}, list(DISTRACTORS), stated)
    if not quiet:
        for k, v in c.items():
            print("  %-46s %s" % (k, "{:,}".format(v) if isinstance(v, int) else v))
    return c


def figures(sim):
    g = AN.group_figure(sim["sim"])
    a1 = AN.ask1(sim["accr"], sim["control"])
    a2 = AN.ask2(sim["till"], sim["sales"])
    rows = [tuple(x) for x in csv.reader(open(os.path.join(TARGET, R.FY25_SUMMARY),
                                              encoding="utf-8"))][1:]
    logr = [tuple(x) for x in csv.reader(open(os.path.join(TARGET, A.RUN_LOG),
                                              encoding="utf-8"))][1:]
    a3 = AN.ask3(rows, logr)
    return dict(
        call=dict(
            group_postings_tripped=g["graded"],
            group_postings_tripped_unrounded=round(g["raw"], 1),
            entries_raised_as_exceptions=g["flagged"],
            postings_in_window=g["postings"],
            entries_in_window=g["entries"],
            unit_postings_tripped={k: v["graded"] for k, v in g["units"].items()},
            unit_entries_raised={k: v["flagged"] for k, v in g["units"].items()},
            unit_postings={k: v["postings"] for k, v in g["units"].items()},
            unit_bridge={k: v["graded"] - v["flagged"] for k, v in g["units"].items()},
            group_bridge=g["graded"] - g["flagged"],
            max_postings_on_an_entry=g["max_items"],
            licensed_mom=int(round(sum(v["licensed"]["mom"] for v in g["units"].values()))),
            licensed_cloglog=int(round(sum(v["licensed"]["cloglog"] for v in g["units"].values()))),
        ),
        # the rungs are counts of postings, so they are stated as whole numbers
        rungs={k: int(round(v)) for k, v in AN.rungs(sim["sim"]).items()},
        asks=dict(ask1={"%s|%s" % (u, f): a1[u][f] for u in a1 for f in a1[u]},
                  ask2={"%s|%s" % (k, f): a2[k][f] for k in a2 for f in a2[k]},
                  ask3=dict(a3)),
    ), g, a1, a2, a3


def build_goldens(out, sim, g, a1, a2, a3, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    DV.write_bridge(os.path.join(out, DV.BRIDGE), g, a1, a2, a3)
    DV.write_chart(os.path.join(out, DV.CHART), g)
    DV.write_paper(os.path.join(out, DV.PAPER), g, a1)
    name, _role = W.PEOPLE["audit"]
    PP.normalize_ooxml(os.path.join(out, DV.BRIDGE), name, name,
                       "2026-07-03T09:00:00Z", "2026-07-03T09:00:00Z",
                       title="Exception population bridge", excel=True)
    PP.normalize_pdf(os.path.join(out, DV.PAPER), b"D:20260703090000+01'00'",
                     b"D:20260703090000+01'00'")
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-46s %8.1f KB" % (f, os.path.getsize(os.path.join(out, f)) / 1024))


def digest(folder):
    h = hashlib.sha256()
    for root, dirs, files in os.walk(folder):
        dirs.sort()
        for f in sorted(files):
            full = os.path.join(root, f)
            h.update(os.path.relpath(full, folder).encode())
            with open(full, "rb") as fh:
                while True:
                    b = fh.read(1 << 20)
                    if not b:
                        break
                    h.update(b)
    return h.hexdigest()[:16]


def cut_zip(path, folder):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, dirs, files in os.walk(folder):
            dirs.sort()
            for f in sorted(files):
                full = os.path.join(root, f)
                zi = zipfile.ZipInfo(os.path.relpath(full, folder), date_time=(2026, 7, 3, 9, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                with open(full, "rb") as fh:
                    z.writestr(zi, fh.read())
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-checks", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    sim = world()
    if a.out:
        build_pack(a.out, sim, quiet=a.quiet)
        return 0
    print("pack")
    build_pack(TARGET, sim, quiet=a.quiet)
    fig, g, a1, a2, a3 = figures(sim)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("goldens")
    build_goldens(GOLDEN, sim, g, a1, a2, a3, quiet=a.quiet)
    print("\nthe call: %s postings tripped the ruleset in FY26 P1 to P9 (unrounded %.1f), against %s "
          "entries raised" % ("{:,}".format(g["graded"]), g["raw"], "{:,}".format(g["flagged"])))
    if a.no_checks:
        return 0
    for script in ("checks.py", "verify.py"):
        print("\n%s" % script)
        r = subprocess.run([sys.executable, os.path.join(HERE, script)], cwd=HERE)
        if r.returncode:
            print("FAIL %s exited %d" % (script, r.returncode))
            return r.returncode
    print("\nrebuild")
    d1 = digest(TARGET)
    tmp = tempfile.mkdtemp(dir=TASK)
    try:
        build_pack(os.path.join(tmp, "target"), world(), quiet=True)
        d2 = digest(os.path.join(tmp, "target"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("  %s and %s" % (d1, d2), "identical" if d1 == d2 else "DIFFER")
    if d1 != d2:
        return 1
    cut_zip(os.path.join(TASK, "target.zip"), TARGET)
    print("  target.zip %.1f MB" % (os.path.getsize(os.path.join(TASK, "target.zip")) / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(main())
