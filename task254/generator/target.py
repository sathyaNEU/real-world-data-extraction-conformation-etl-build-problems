"""Write task254/target/: every file of the evidence pack, containers normalised, writer names scrubbed."""
import datetime as dt
import os
import shutil
import subprocess
import sys

import build as B
import distractors as DI
import docs as D
import pack as P
import postprocess as PP
import supply as SU

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
SCRUB = os.path.join(os.path.dirname(TASK), ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
PDF_STAMP = {"annex": b"D:20260824101200+02'00'", "guide": b"D:20260226143500+01'00'"}


def write(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, P.FILES[k])
    allc, dups = B.make_world()
    T = B.tables(allc, dups)
    sellin, calloff, fin = SU.build()
    counts = {}
    P.write_csv(p("listing"), T["listing"])
    counts["listing"] = len(T["listing"])
    P.write_csv(p("dosage"), T["dosage"])
    counts["dosage"] = len(T["dosage"])
    P.write_csv(p("feed"), T["feed"])
    counts["feed"] = len(T["feed"])
    P.write_labreg(p("labreg"), T["labreg"])
    counts["labreg"] = len(T["labreg"])
    P.write_dupreg(p("dupreg"), T["dupreg"])
    counts["dupreg"] = len(T["dupreg"])
    P.write_terms(p("terms"), T["terms"], T["changes"])
    D.annex_pdf(p("annex"))
    D.field_guide_pdf(p("guide"))
    D.section5_docx(p("section5"))
    counts["sellin"] = len(P.write_sellin(p("sellin"), sellin))
    counts["calloff"] = len(P.write_calloffs(p("calloff"), calloff))
    counts["master"] = len(P.write_master(p("master")))
    P.write_xevmpd(p("xevmpd"))
    P.write_channels(p("channels"))
    counts["finance"] = len(P.write_finance(p("finance"), fin))
    counts["medinfo"] = DI.medinfo(p("medinfo"))
    li = [(c["case_no"], c["versions"][0]) for c in allc if c["report_type"] == "LI" and c["kind"] != "dup"]
    dli = [(c["case_no"], c["versions"][0]) for c in allc if c["report_type"] == "LI" and c["kind"] == "dup"]
    counts["litscreen"] = DI.literature(p("litscreen"), li, dli)
    counts["signals"] = DI.signals(p("signals"))
    P.write_log(p("log"), counts)
    for k in P.WB:
        PP.normalize_zip(p(k), modified=P.saved_stamp(k))
    PP.normalize_zip(p("section5"), modified="2026-10-05T15:02:00Z")
    for k, stamp in PDF_STAMP.items():
        b = open(p(k), "rb").read().replace(b"D:20000101000000+00'00'", stamp)
        open(p(k), "wb").write(b)
    subprocess.run([sys.executable, SCRUB, out, "--apply", "--producer", "Ravnsborg Pharma Document Control",
                    "--stamp", "2026-10-06", "--floor", "2023-01-01", "--ceiling", "2026-10-06"],
                   check=True, stdout=subprocess.DEVNULL)
    ts = dt.datetime(2026, 10, 6, 16, 5).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (ts, ts))
    if not quiet:
        print("target:", len(os.listdir(out)), "files;", counts)
    return dict(allc=allc, dups=dups, tables=T, sellin=sellin, calloff=calloff, fin=fin, counts=counts)


if __name__ == "__main__":
    write(os.path.join(TASK, "target"))
