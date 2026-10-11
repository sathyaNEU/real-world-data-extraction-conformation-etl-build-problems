"""Build task229's evidence pack into <out>/ (default: task229/target)."""
import argparse
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim as S
import records as R
import pack as P
import docs as D
import postprocess as PP

TASK = os.path.dirname(HERE)


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    insts = S.simulate()
    ev = R.fix_rollback_images(R.history(insts))
    ev = R.week_events(insts, ev)
    bench = R.bench_meters()
    rows = R.deliveries(insts)
    sched = R.wave8(insts)
    p = lambda k: os.path.join(out, P.FILES[k])
    counts = {}
    counts["mdm"] = P.write_mdm(p("mdm"), insts, rows)
    n_m, n_e, n_rep = P.write_hes(p("hes"), insts, {k: list(v) for k, v in ev.items()}, bench)
    counts["hes_meters"] = n_m
    P.write_register(p("register"), insts)
    counts["register"] = len(insts)
    P.write_catalogue(p("catalogue"))
    counts["catalogue"] = 12
    P.write_wave8(p("wave8"), sched)
    counts["wave8"] = len(sched)
    P.write_census(p("census"), insts, ev, bench)
    counts["census"] = sum(1 for _ in open(p("census"))) - 1
    P.write_telco(p("telco"))
    D.standard_pdf(p("standard"))
    D.field_reference_md(p("fieldref"))
    P.write_log(p("log"), counts)
    for k in ("register", "wave8", "telco"):
        PP.normalize_zip(p(k))
    PP.normalize_pdf(p("standard"), stamp=b"D:20260624101500Z'")
    ts = dt.datetime(2026, 10, 12, 15, 40).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (ts, ts))
    if not quiet:
        print("built", out, len(os.listdir(out)), "files;", counts["mdm"], "MDM rows;", n_e, "HES events;", n_rep, "replayed")
    return dict(insts=insts, ev=ev, bench=bench, rows=rows, sched=sched, counts=counts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    a = ap.parse_args()
    build(a.out)
