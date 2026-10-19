"""Build task269: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder
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
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

import numpy as np   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A       # noqa: E402
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import pack as PK          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
ASSEMBLED = dt.datetime(2026, 10, 2, 14, 41)          # the working pack, assembled by Network Performance
MTIME = calendar.timegm(ASSEMBLED.timetuple())


def report_figures(net, S, first_rows, J):
    """The August report's figures for the frequent routes: on-time running under section 4 on the first release
    (the census fortnight standing in for the month), average weekday boardings all day and trips delivered."""
    rng = np.random.default_rng([W.SEED, 81])
    otp, n = {}, {}
    for r in first_rows:
        if r[10]:
            continue
        rt = r[1]
        sh, sm, ss = (int(x) for x in r[8].split(":"))
        dev = (r[9] - (sh * 60 + sm + ss / 60)) * 60
        n[rt] = n.get(rt, 0) + 1
        if -59 <= dev <= 359:
            otp[rt] = otp.get(rt, 0) + 1
    days = len(K.CENSUS)
    pat = {rt: int(round(sum(1 for j in J if j["route"] == rt) / days * float(rng.uniform(1.48, 1.62)), -1))
           for rt in K.ROUTES}
    return ({rt: 100.0 * otp[rt] / n[rt] for rt in K.ROUTES}, pat,
            {rt: float(np.round(rng.uniform(98.6, 99.8), 1)) for rt in K.ROUTES})


CONTENTS = [
    ("avl_timingpoint_departures_census_revised.csv", "Location vendor, revised release of 2 September 2026: buses' departures from timing points on the frequent routes, 10 to 21 August 2026, 6 to 10 am and 2:30 to 7 pm."),
    ("avl_timingpoint_departures_census_first_release.csv", "Location vendor, first release of 24 August 2026, same fortnight and hours."),
    ("ticketing_journeys_census_2026-08.csv", "Ticketing system: journeys tapped on the frequent routes, 10 to 21 August 2026, 6 to 10 am and 2:30 to 7 pm; one row a tag-on, card numbers hashed."),
    ("gtfs_pellbrook_2026-07-20.zip", "Timetable feed in force 20 July to 16 August 2026, frequent routes, weekdays."),
    ("gtfs_pellbrook_2026-08-17.zip", "Timetable feed in force from 17 August 2026, frequent routes, weekdays."),
    ("frequent_corridors_2026.xlsx", "Network Planning: the frequent corridors' stops by route and direction, July 2026."),
    ("stop_changes_log_2026.csv", "Network Planning: stop changes, 2026."),
    ("bus_service_reliability_standard_v4.pdf", "The Bus Service Reliability Standard, version 4."),
    ("headway_programme_guidelines_2027.pdf", "The headway management programme's guidelines for 2027."),
    ("headway_supervision_pilot_plan_2026.pdf", "The 2026 headway supervision pilot plan agreed with the operator."),
    ("pbc_supervision_timesheets_feb-jun_2026.csv", "Pellbrook Bus Company: supervisor shifts, February to June 2026, as exported from its systems."),
    ("pbc_staff_list_2026-10-01.csv", "Pellbrook Bus Company: supervisors on its staff list, 1 October 2026."),
    ("ledger_network_performance_fy2026_fy2027.csv", "General ledger: lines on the Network Performance cost centres, July 2025 to September 2026."),
    ("service_performance_report_august_2026.pdf", "The monthly service performance report for August 2026."),
    ("customer_feedback_term3_2026.xlsx", "Customer contact centre: feedback cases on the frequent routes, Term 3 2026."),
]


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    net = W.network()
    R.relocation(net)
    S = W.simulate(net, seed)
    J = W.journeys(net, S, seed)
    P = W.pilot(seed)
    T = W.pilot_truth(P)
    rev, first = R.departures(net, S, seed)
    counts = {}
    counts["avl_rev"] = R.write_departures(p("avl_rev"), rev, "R2")
    counts["avl_first"] = R.write_departures(p("avl_first"), first, "R1")
    counts["journeys"] = R.write_journeys(p("journeys"), J)
    counts["gtfs1"] = R.write_gtfs(p("gtfs1"), net, S["timetable"][1], 1)
    counts["gtfs2"] = R.write_gtfs(p("gtfs2"), net, S["timetable"][2], 2)
    counts["corridors"] = R.write_corridors(p("corridors"), net)
    counts["stops_log"] = R.write_stop_changes(p("stops_log"), net)
    DC.write_standard(p("standard"))
    DC.write_guidelines(p("guidelines"))
    DC.write_pilot_plan(p("pilot_plan"))
    ts = R.timesheet_rows(P, seed)
    counts["timesheets"] = R.write_timesheets(p("timesheets"), ts)
    counts["staff"] = R.write_staff(p("staff"), P)
    counts["ledger"] = R.write_ledger(p("ledger"), R.ledger_rows(P, T, seed))
    otp, pat, dlv = report_figures(net, S, first, J)
    DC.write_report(p("report"), otp, pat, dlv)
    counts["feedback"] = R.write_feedback(p("feedback"), seed)
    DC.write_contents(p("contents"), CONTENTS)
    return dict(net=net, S=S, J=J, P=P, T=T, rev=rev, first=first, ts=ts, counts=counts)


DOC_DATES = {
    "standard": ("D:20250303101500+10'00'", "D:20250303101500+10'00'"),
    "guidelines": ("D:20260907161200+10'00'", "D:20260907161200+10'00'"),
    "pilot_plan": ("D:20260122140500+10'00'", "D:20260122140500+10'00'"),
    "report": ("D:20260911093000+10'00'", "D:20260911093000+10'00'"),
}
OOXML = {
    "corridors": ("Network Planning", "Network Planning", "2026-07-03T02:10:00Z", "2026-07-06T00:48:00Z",
                  "Frequent corridors, July 2026"),
    "feedback": ("Customer Contact Centre", "Customer Contact Centre", "2026-09-30T05:22:00Z", "2026-09-30T05:31:00Z",
                 None),
}


def finish(out):
    """The containers as the agency's systems save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in DOC_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    for k, (cr, lb, c, m, title) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=True)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def metadata(fig, counts):
    meta = {
        "task": "task269",
        "title": "Pellbrook Metro: the four frequent routes for the 2027 headway supervisor teams",
        "domain": "Urban & Regional Science (network analysis)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["report"], K.FILES["feedback"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); Pellbrook, Pellbrook Metro, "
                                        "Pellbrook Bus Company and every person are fictional",
                              "date": "2026-10-02", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Routes %s" % ", ".join(str(r) for r in fig["call"]["routes"]),
    }
    return meta


def main_build(target, golden):
    import deliver as DV
    b = build(target)
    finish(target)
    fig, exact = DV.write(target, golden)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(golden, DV.WB), "Network Performance", "Network Performance",
                       "2026-10-05T03:12:00Z", "2026-10-05T04:40:00Z", title="2027 headway programme routes",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, exact


def digest(folder):
    h = {}
    for f in sorted(os.listdir(folder)):
        h[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return h


def cut_zip(target, path):
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        finish(a.out)
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, exact = main_build(target, golden)
    print("pack:", b["counts"])
    print("call:", fig["call"], "first below:", fig["first_below"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, exact)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    b2 = build(os.path.join(scratch, "target"))
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    same = d1 == d2
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
