"""Build task273: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task273/generator/build.py              everything
    python3 task273/generator/build.py --out DIR    the pack only, into DIR
    python3 task273/generator/build.py --golden     the pack and the goldens, no checks"""
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

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A           # noqa: E402
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("standard", "Platform Engineering: Public API Year-End Readiness Standard, 2026 edition (approved 8 September "
                 "2026)."),
    ("plan", "Performance Engineering: Year-End Peak Load Test Plan, November 2026, with the campaign log."),
    ("register", "Platform Engineering: the public API's endpoint register, the services that run the endpoints, and "
                 "the plans."),
    ("jmeter", "Load test results, JMeter runs of 10 to 12 November 2026 (JTL)."),
    ("k6", "Load test results, k6 runs of 16 to 19 November 2026 (http_req_duration)."),
    ("gc", "Log platform export: the performance cluster's garbage-collection logs, each run and five minutes either "
           "side, 10 to 19 November 2026."),
    ("events", "Performance cluster: pod events and service start-up lines, namespace perf, November 2026."),
    ("edge", "API edge: requests by route and clock hour (UTC), January 2026, production."),
    ("synthetic", "Site Reliability: the uptime monitors run against the production edge's public API."),
    ("changelog", "Developer portal: the public API's 2026 changelog."),
    ("employers", "CRM: employer accounts with an active subscription on 1 November 2026."),
    ("subs", "Billing: subscription events from 1 January to 31 October 2026."),
    ("legacy", "Legacy billing: service credits issued from 1 January to 30 April 2026."),
    ("credits", "Billing: credit notes created from 1 May to 19 November 2026."),
    ("incidents", "Status page: incidents from December 2025 to November 2026."),
    ("apm", "APM: trace sample from the performance cluster, 18 November 2026."),
    ("slowq", "Performance database: slow query log (statements over 200 ms), 10 to 19 November 2026."),
]


def achieved(w):
    """Each endpoint's throughput in its run of record's measurement (requests a second)."""
    out = {}
    for c in K.CODES:
        rows = w["runs"][c]["rows"]
        out[c] = sum(1 for x in rows if K.WARMUP_S <= x[2] < K.RUN_S) / K.MEASURE_S
    return out


def worlds(seed=K.SEED):
    w = W.world(seed)
    emp = A.employer_world(seed)
    growth = A.growth_truth(emp)
    cust, redir = A.edge_hourly(seed, achieved(w), growth)
    inc, cr = A.incident_world(seed, emp)
    legacy, new = A.billing(seed, cr)
    return dict(w=w, emp=emp, growth=growth, cust=cust, redir=redir, inc=inc, credits=cr, legacy=legacy, new=new)


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    X = worlds(seed)
    w = X["w"]
    n = {}
    head, rows = R.jmeter_rows(w)
    R.write_csv(p("jmeter"), head, rows)
    n["jmeter"] = len(rows)
    head, rows = R.k6_rows(w)
    R.write_csv(p("k6"), head, rows)
    n["k6"] = len(rows)
    lines, starts = R.gc_lines(w)
    with open(p("gc"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    n["gc"] = len(lines)
    ev = R.pod_events(w, starts)
    R.write_csv(p("events"), ev[0], ev[1:])
    n["events"] = len(ev) - 1
    n["edge"] = R.write_edge(p("edge"), A.edge_rows(seed, X["cust"], X["redir"]))
    n["employers"] = R.write_employers(p("employers"), X["emp"])
    n["subs"] = R.write_subscription_events(p("subs"), X["emp"])
    n["legacy"] = R.write_legacy_credits(p("legacy"), X["legacy"])
    n["credits"] = R.write_new_credits(p("credits"), X["new"])
    n["incidents"] = len(X["inc"])
    n["apm"] = R.write_apm(p("apm"), w)
    n["slowq"] = R.write_slow_queries(p("slowq"), w)
    DC.write_standard(p("standard"))
    DC.write_plan(p("plan"), w)
    DC.write_register(p("register"), seed)
    n["register"] = len(K.CODES)
    DC.write_incidents(p("incidents"), X["inc"])
    DC.write_changelog(p("changelog"))
    DC.write_synthetic(p("synthetic"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(X=X if keep else None, counts=n)


PDF_DATES = {"standard": ("D:20260904110200-04'00'", "D:20260908163000-04'00'")}
OOXML = {
    "plan": ("Performance Engineering", "Performance Engineering", "2026-10-14T13:20:00Z", "2026-11-19T21:45:00Z",
             "Year-End Peak Load Test Plan, November 2026", False),
    "register": ("Platform Engineering", "Platform Engineering", "2024-03-11T14:02:00Z", "2026-11-09T18:40:00Z",
                 "Public API endpoint register", True),
    "incidents": ("Site Reliability", "Site Reliability", "2026-11-20T15:12:00Z", "2026-11-20T15:12:00Z",
                  "Status page incidents", True),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.COMPANY
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.COMPANY
    PP.normalize_ooxml(os.path.join(golden, K.DELIVERABLES[0]), K.REQUESTER, K.REQUESTER, "2026-11-23T14:06:00Z",
                       "2026-11-25T20:31:00Z", title="Year-end readiness 2027", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, its services, pods, customers, incidents, credits and "
           "people are fictional; JMeter, k6, JVM unified logging and Kubernetes event formats follow public "
           "documentation" % K.COMPANY)
    return {
        "task": "task273",
        "title": "%s: the public API endpoints to fix before the 2026 code freeze" % K.COMPANY,
        "domain": "General Statistics & Data Science (missing data, censoring and measurement error)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES[k] for k in K.DISTRACTORS],
        "provenance": {name: {"source": src, "date": "2026-10-22", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": "%d endpoints to fix: %s" % (len(fig["call"]["fix"]), ", ".join(fig["call"]["fix"])),
    }


def main_build(target, golden, seed=K.SEED):
    import deliver as DV
    b = build(target, seed, keep=True)
    finish(target)
    fig, res = DV.write(target, golden)
    finish_golden(golden)
    DV.write_figures(os.path.join(HERE, "figures.json"), fig)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, res


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(target, path):
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=K.SEED)
    a = ap.parse_args()
    if a.out:
        b = build(a.out, a.seed)
        finish(a.out)
        print(b["counts"])
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden, a.seed)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"), a.seed)
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    finish_golden(os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    g1, g2 = digest(golden), digest(os.path.join(scratch, "golden"))
    same = d1 == d2 and g1 == g2
    for f in sorted(set(d1) | set(g1)):
        if d1.get(f, g1.get(f)) != d2.get(f, g2.get(f)):
            print("  differs on rebuild:", f)
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
