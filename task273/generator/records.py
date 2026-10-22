"""The load-test evidence as the platform's own systems wrote it: JMeter's JTL results (until 12 November), k6's CSV
output (from 16 November), the log platform's export of every pod's garbage-collection log, the cluster's pod events,
and the platform register."""
import csv
import datetime as dt
import zlib

import numpy as np

import common as K
import world as W

UTC = dt.timezone.utc
EST = dt.timezone(dt.timedelta(hours=-5))
HOST = "https://perf-api.mirrendale.internal"
EPOCH = dt.datetime(1970, 1, 1)
MARGIN = 300.0                       # seconds of each pod's GC log kept either side of a run


def wall(start, t):
    return start + dt.timedelta(seconds=float(t))


def ms_epoch(x):
    return int(round((x - EPOCH).total_seconds() * 1000.0))


def url_for(code, r):
    path = K.PATH[code].split(" ", 1)[1]
    if "{id}" in path:
        pref = {"payroll-core": "PR", "filings": "FL", "employees": "E", "companies": "CO"}.get(K.SERVICE[code], "ID")
        path = path.replace("{id}", "%s-%06d" % (pref, int(r.integers(100000, 999999))))
    q = {"EP03": "?year=2026&employee=E-%06d", "EP04": "?year=2026&payee=V-%06d", "EP13": "?employee=E-%06d",
         "EP19": "?q=W2+correction+%06d", "EP24": "?zip=%05d", "EP07": "?company=CO-%06d", "EP08": "?company=CO-%06d"}
    if code in q:
        path += q[code] % int(r.integers(10000, 99999))
    return HOST + path


def errors(seed, code, n):
    """The rare server errors the platform returned during a run (a few hundredths of a per cent)."""
    r = np.random.default_rng([seed, int(code[2:]), 21])
    return r.random(n) < 0.0004


def jmeter_rows(w):
    """JMeter's JTL CSV, written as each sample completes, timeStamp at the sample's start (the plan's
    sampleresult.timestamp.start=true), elapsed and Latency in whole milliseconds."""
    head = ["timeStamp", "elapsed", "label", "responseCode", "responseMessage", "threadName", "dataType", "success",
            "failureMessage", "bytes", "sentBytes", "grpThreads", "allThreads", "URL", "Latency", "IdleTime", "Connect",
            "servedBy"]
    out = []
    for code in K.CODES:
        s = w["sched"][code]
        if s["tool"] != "jmeter":
            continue
        pods = w["pods"][K.SERVICE[code]]
        th_n = w["eps"][code]["threads"]
        for kind in ("aborted", "record"):
            run = w["runs"][code] if kind == "record" else w["runs"][code].get("aborted")
            if run is None:
                continue
            start = s["start"] if kind == "record" else s["aborted_start"]
            r = np.random.default_rng([w["seed"], int(code[2:]), 31 if kind == "record" else 32])
            err = errors(w["seed"] + (0 if kind == "record" else 1), code, len(run["rows"]))
            group = "%s %s" % (code, K.SERVICE[code])
            first = set()
            for i, (th, pod, t, f, sv) in enumerate(run["rows"]):
                el = int(round((f - t) * 1000.0))
                bad = bool(err[i])
                conn = 0
                if th not in first:
                    first.add(th)
                    conn = int(r.integers(4, 16))
                lat = max(1, el - int(r.integers(0, 4)))
                nbytes = int(r.integers(900, 4200)) if not bad else 312
                out.append((f, [ms_epoch(wall(start, t)), el, "%s %s" % (code, K.PATH[code]),
                                "500" if bad else "200", "Internal Server Error" if bad else "OK",
                                "%s 1-%d" % (group, th + 1), "text", "false" if bad else "true",
                                "500 Internal Server Error" if bad else "", nbytes, int(r.integers(180, 900)),
                                th_n, th_n, url_for(code, r), lat, 0, conn, pods[pod]], start))
    out.sort(key=lambda x: wall(x[2], x[0]))
    return head, [x[1] for x in out]


def k6_rows(w):
    """k6's CSV output with the plan's rfc3339_nano time format: one http_req_duration sample per request, stamped
    when the response completed; the script tags each request with its virtual user and the X-Served-By pod."""
    head = ["metric_name", "timestamp", "metric_value", "check", "error", "error_code", "expected_response", "group",
            "method", "name", "proto", "scenario", "service", "status", "subproto", "tls_version", "url", "extra_tags",
            "metadata"]
    out = []
    for code in K.CODES:
        s = w["sched"][code]
        if s["tool"] != "k6":
            continue
        pods = w["pods"][K.SERVICE[code]]
        method = K.PATH[code].split(" ")[0]
        for kind in ("aborted", "record"):
            run = w["runs"][code] if kind == "record" else w["runs"][code].get("aborted")
            if run is None:
                continue
            start = s["start"] if kind == "record" else s["aborted_start"]
            r = np.random.default_rng([w["seed"], int(code[2:]), 41 if kind == "record" else 42])
            err = errors(w["seed"] + (0 if kind == "record" else 1), code, len(run["rows"]))
            scen = "peak_%s" % code.lower()
            for i, (th, pod, t, f, sv) in enumerate(run["rows"]):
                end = wall(start, f)
                stamp = end.strftime("%Y-%m-%dT%H:%M:%S.") + "%06d%03dZ" % (end.microsecond, int(f * 1e9) % 1000)
                val = "%.6f" % ((f - t) * 1000.0)
                u = url_for(code, r)
                bad = bool(err[i])
                out.append((end, ["http_req_duration", stamp, val, "", "request failed" if bad else "",
                                  "1500" if bad else "", "false" if bad else "true", "", method, u, "HTTP/1.1", scen,
                                  "", "500" if bad else "200", "", "tls1.3", u,
                                  "vu=%d&served_by=%s&endpoint=%s" % (th + 1, pods[pod], code), ""]))
    out.sort(key=lambda x: x[0])
    return head, [x[1] for x in out]


def heap_mb(seed, svc):
    """Each service's heap (-Xmx, megabytes): the same on every pod of the service."""
    r = np.random.default_rng([seed, zlib.crc32(svc.encode()), 63])
    gc = K.SERVICES[svc][0]
    if gc == "parallel":
        return int(r.choice([2048, 3072, 4096]))
    if gc == "g1":
        return int(r.choice([1024, 1536, 2048]))
    return int(r.choice([4096, 6144]))


def jvm_starts(w):
    """When each pod's JVM started (UTC): every pod deployed on Monday 9 November, two restarted during the campaign."""
    r = np.random.default_rng([w["seed"], 0, 51])
    out = {}
    base = dt.datetime(2026, 11, 9, 19, 12, 0)
    restarts = {("tax-forms", 1): dt.datetime(2026, 11, 13, 3, 41, 7), ("banking", 0): dt.datetime(2026, 11, 14, 22, 5, 52)}
    for svc, pods in w["pods"].items():
        for i, pod in enumerate(pods):
            t = base + dt.timedelta(seconds=float(r.uniform(0, 1800)))
            run_for = float(r.uniform(6.5, 12.0))
            out[pod] = [(t, run_for)]
            if (svc, i) in restarts:
                out[pod].append((restarts[(svc, i)], float(r.uniform(6.5, 12.0))))
    return out


def jvm_start_at(starts, pod, when):
    """The JVM start in force at a moment: the latest start before it."""
    best = None
    for t, run_for in starts[pod]:
        if t <= when:
            best = t
    return best


def gc_lines(w):
    """The log platform's export: '<ingested at> <pod> <the JVM's own log line>' for every GC event of every pod
    during each run and five minutes either side. The JVM writes a pause's line when the pause ends."""
    starts = jvm_starts(w)
    events = []
    for code in K.CODES:
        svc = K.SERVICE[code]
        gc = w["gcs"][svc]["gc"]
        s = w["sched"][code]
        for kind in ("aborted", "record"):
            run = w["runs"][code] if kind == "record" else w["runs"][code].get("aborted")
            if run is None:
                continue
            start = s["start"] if kind == "record" else s["aborted_start"]
            run_s = K.RUN_S if kind == "record" else W.ABORTED[code]
            r = np.random.default_rng([w["seed"], int(code[2:]), 61 if kind == "record" else 62])
            P = [list(p) for p in run["pauses"]]
            # the quieter minutes either side of the run: young collections only, at a third of the rate
            for pi in range(len(P)):
                for lo, hi in ((-MARGIN, -30.0), (run_s + 30.0, run_s + MARGIN)):
                    for f in w["gcs"][svc]["fams"][:1]:
                        t = lo + r.exponential(180.0 / f["rate"])
                        while t < hi:
                            d = float(np.exp(np.log(f["med"]) + f["sd"] * r.standard_normal())) / 1000.0
                            P[pi].append((t, t + d, f["name"]))
                            t += r.exponential(180.0 / f["rate"])
                P[pi].sort()
            cap = heap_mb(w["seed"], svc)
            for pi, plist in enumerate(P):
                pod = w["pods"][svc][pi]
                for a, b, fam in plist:
                    events.append((wall(start, b), pod, gc, fam, (b - a) * 1000.0, cap, svc))
            for pi, t, conc, end in run.get("cycles", []):
                pod = w["pods"][svc][pi]
                # the cycle's closing line, written once Cleanup has finished, with the whole cycle's length
                events.append((wall(start, end + 0.0004), pod, gc, "concurrent", (end - t) * 1000.0, 0, svc))
    events.sort(key=lambda e: (e[1], e[0]))
    out = []
    gcn = {}
    zseq = {}
    rr = np.random.default_rng([w["seed"], 0, 64])
    for end, pod, gc, fam, dur, cap, svc in events:
        js = jvm_start_at(starts, pod, end)
        n = gcn.get((pod, js), int(rr.integers(40, 400)))
        if fam == "concurrent":
            body = "GC(%d) Concurrent Mark Cycle %.3fms" % (n, dur)
        elif gc == "parallel":
            before = int(cap * rr.uniform(0.70, 0.95))
            after = int(before * (rr.uniform(0.15, 0.35) if fam == "young" else rr.uniform(0.45, 0.65)))
            label = "Pause Young (Allocation Failure)" if fam == "young" else "Pause Full (Ergonomics)"
            body = "GC(%d) %s %dM->%dM(%dM) %.3fms" % (n, label, before, after, cap, dur)
            gcn[(pod, js)] = n + 1
        elif gc == "g1":
            before = int(cap * rr.uniform(0.55, 0.92))
            if fam == "remark":
                body = "GC(%d) Pause Remark %dM->%dM(%dM) %.3fms" % (n, before, int(before * 0.98), cap, dur)
            elif fam == "cleanup":
                body = "GC(%d) Pause Cleanup %dM->%dM(%dM) %.3fms" % (n, before, before, cap, dur)
                gcn[(pod, js)] = n + 1
            else:
                after = int(before * rr.uniform(0.12, 0.40))
                label = "Pause Young (Normal) (G1 Evacuation Pause)" if fam == "young" else \
                    "Pause Young (Mixed) (G1 Evacuation Pause)"
                body = "GC(%d) %s %dM->%dM(%dM) %.3fms" % (n, label, before, after, cap, dur)
                gcn[(pod, js)] = n + 1
        else:
            k = zseq.get(pod, 0)
            zseq[pod] = (k + 1) % 3
            body = "GC(%d) %s %.3fms" % (n, ("Pause Mark Start", "Pause Mark End", "Pause Relocate Start")[k], dur)
            if k == 2:
                used = int(cap * rr.uniform(0.2, 0.5))
                out.append((end + dt.timedelta(milliseconds=float(rr.uniform(40, 160))), pod,
                            "GC(%d) Garbage Collection (Allocation Rate) %dM(%d%%)->%dM(%d%%)" % (
                                n, used, round(100 * used / cap), int(used * 0.45), round(45 * used / cap)), js, svc))
                gcn[(pod, js)] = n + 1
        out.append((end, pod, body, js, svc))
    lines = []
    for end, pod, body, js, svc in out:
        if svc in W.UPTIME_SERVICES:
            deco = "[%.3fs][info][gc]" % (end - js).total_seconds()
        else:
            loc = end.replace(tzinfo=UTC).astimezone(EST)
            deco = "[%s.%03d-0500][info][gc]" % (loc.strftime("%Y-%m-%dT%H:%M:%S"), loc.microsecond // 1000)
        if " Pause Mark " in body or " Pause Relocate " in body:
            deco = deco.replace("[gc]", "[gc,phases]")
        ing = end + dt.timedelta(seconds=float(rr.uniform(0.15, 2.5)))
        lines.append((ing, "%sZ %s %s %s" % (ing.strftime("%Y-%m-%dT%H:%M:%S.") + "%03d" % (ing.microsecond // 1000),
                                             pod, deco, body)))
    lines.sort(key=lambda x: x[0])
    return [x[1] for x in lines], starts


def pod_events(w, starts):
    """The cluster's pod events and each service's start-up line, which says how long its process had been running."""
    r = np.random.default_rng([w["seed"], 0, 71])
    app = {s: "".join(p.capitalize() for p in s.split("-")) + "Application" for s in K.SERVICES}
    rows = []
    for svc, pods in w["pods"].items():
        for pod in pods:
            for t, run_for in starts[pod]:
                sched = t - dt.timedelta(seconds=float(r.uniform(8, 25)))
                rows.append((sched, pod, "kubelet", "Scheduled", "Successfully assigned perf/%s to perf-node-%02d" % (
                    pod, int(r.integers(1, 13)))))
                rows.append((sched + dt.timedelta(seconds=float(r.uniform(1, 4))), pod, "kubelet", "Pulled",
                             "Container image \"registry.mirrendale.internal/%s:2026.11.2\" already present on machine" % svc))
                rows.append((t - dt.timedelta(seconds=float(r.uniform(0.2, 0.6))), pod, "kubelet", "Started",
                             "Started container %s" % svc))
                rows.append((t + dt.timedelta(seconds=run_for), pod, "app", "Log",
                             "Started %s in %.3f seconds (process running for %.2f)" % (
                                 app[svc], run_for - float(r.uniform(0.4, 1.1)), run_for)))
            if len(starts[pod]) > 1:
                t2 = starts[pod][1][0]
                rows.append((t2 - dt.timedelta(seconds=float(r.uniform(20, 40))), pod, "kubelet", "Killing",
                             "Stopping container %s" % svc))
    rows.sort()
    return [["time", "namespace", "pod", "source", "reason", "message"]] + [
        [x[0].strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (x[0].microsecond // 1000), "perf", x[1], x[2], x[3], x[4]]
        for x in rows]


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(head)
        wr.writerows(rows)


# ------------------------------------------------------------------------------------- the ask records' exports
def write_edge(path, rows):
    write_csv(path, ["hour_start_utc", "route", "requests", "status_5xx", "bytes_out"], rows)
    return len(rows)


def write_employers(path, emp):
    rows = []
    for eid in sorted(emp["snapshot"]):
        s = emp["snapshot"][eid]
        rows.append([eid, s["state"], s["hc"], s["freq"], s["plan"], s["since"].isoformat()])
    write_csv(path, ["employer_id", "state", "headcount", "payroll_frequency", "plan", "subscription_start"], rows)
    return len(rows)


def write_subscription_events(path, emp):
    rows = []
    order = sorted(range(len(emp["events"])), key=lambda i: (emp["events"][i]["date"], i))
    for n, i in enumerate(order):
        e = emp["events"][i]
        rows.append(["SE-26-%06d" % (n + 1), e["employer"], e["date"].isoformat(), e["kind"], e["plan_before"],
                     e["plan_after"], e["hc_before"], e["hc_after"], e["reason"]])
    write_csv(path, ["event_id", "employer_id", "effective_date", "event", "plan_before", "plan_after",
                     "headcount_before", "headcount_after", "reason"], rows)
    return len(rows)


def write_legacy_credits(path, legacy):
    rows = [[x["credit_no"], x["issued"].isoformat(), x["account"], x["incident"], x["cents"], x["status"]]
            for x in sorted(legacy, key=lambda y: y["credit_no"]) if x["issued"] >= dt.date(2026, 1, 1)]
    write_csv(path, ["credit_no", "issued_on", "account", "incident", "amount", "status"], rows)
    return len(rows)


def write_new_credits(path, new):
    import json
    items = []
    for x in new:
        items.append({"id": x["id"], "created_at": x["created"].strftime("%Y-%m-%dT%H:%M:%SZ"), "account": x["account"],
                      "incident": x["incident"], "type": x["kind"], "amount": "%.2f" % x["amount"], "currency": "USD",
                      "memo": x["memo"], "reverses": x["reverses"]})
    doc = {"export": {"system": "Billing", "object": "credit_notes", "exported_at": "2026-11-20T06:00:14Z",
                      "created_from": "2026-05-01", "created_to": K.CREDITS_TO.isoformat(), "count": len(items)},
           "credits": items}
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    return len(items)


# ------------------------------------------------------------------------------------- the two distractors
def write_apm(path, w):
    """The APM tool's trace sample for 18 November (one request in a hundred, server-side span durations)."""
    import json
    r = np.random.default_rng([w["seed"], 0, 91])
    spans = []
    for code in K.CODES:
        s = w["sched"][code]
        if s["start"].date() != dt.date(2026, 11, 18):
            continue
        pods = w["pods"][K.SERVICE[code]]
        for kind in ("aborted", "record"):
            run = w["runs"][code] if kind == "record" else w["runs"][code].get("aborted")
            if run is None:
                continue
            start = s["start"] if kind == "record" else s["aborted_start"]
            for th, pod, t, f, sv in run["rows"]:
                if r.random() >= 0.01:
                    continue
                srv = max(0.4, (f - t) * 1000.0 - float(r.uniform(0.3, 0.9)))
                st = wall(start, t + 0.0002)
                spans.append({"trace_id": "%032x" % int(r.integers(0, 2 ** 62)) ,
                              "span_id": "%016x" % int(r.integers(0, 2 ** 62)),
                              "service": K.SERVICE[code], "pod": pods[pod], "name": K.PATH[code],
                              "start": st.strftime("%Y-%m-%dT%H:%M:%S.") + "%06dZ" % st.microsecond,
                              "duration_ms": round(srv, 3), "http.status_code": 200})
    spans.sort(key=lambda x: (x["start"], x["span_id"]))
    doc = {"source": "apm", "environment": "perf", "date": "2026-11-18", "sampling": "head-based, 1 in 100 traces",
           "spans": spans}
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    return len(spans)


FINGERPRINTS = [
    ("svc_payroll_core", "SELECT * FROM payroll_run_lines WHERE run_id = ? AND employee_id IN (?)"),
    ("svc_payroll_core", "UPDATE payroll_runs SET status = ?, updated_at = ? WHERE id = ?"),
    ("svc_tax_forms", "SELECT f.* FROM w2_forms f JOIN employees e ON e.id = f.employee_id WHERE f.tax_year = ? AND "
                      "e.company_id = ?"),
    ("svc_filings", "INSERT INTO filing_batches (company_id, form, tax_year, payload) VALUES (?, ?, ?, ?)"),
    ("svc_reports", "SELECT company_id, SUM(gross), SUM(net) FROM payroll_run_lines WHERE pay_date BETWEEN ? AND ? "
                    "GROUP BY company_id"),
    ("svc_employees", "SELECT * FROM employees WHERE company_id = ? ORDER BY last_name LIMIT ? OFFSET ?"),
    ("svc_deductions", "SELECT * FROM deductions WHERE employee_id = ? AND effective_to >= ?"),
    ("svc_banking", "SELECT * FROM bank_accounts WHERE employee_id = ? FOR UPDATE"),
    ("svc_search", "SELECT id, ts_rank(doc, q) FROM search_index, plainto_tsquery(?) q WHERE doc @@ q ORDER BY 2 DESC "
                   "LIMIT ?"),
    ("svc_accounting_sync", "SELECT * FROM journal_exports WHERE company_id = ? AND period = ?"),
    ("svc_state_local", "SELECT rate FROM local_tax_rates WHERE zip = ? AND effective_from <= ? ORDER BY "
                        "effective_from DESC LIMIT ?"),
]


def write_slow_queries(path, w):
    """The perf database's slow query log (statements over 200 ms) for the campaign's days."""
    r = np.random.default_rng([w["seed"], 0, 92])
    rows = []
    for day in W.JMETER_DAYS + W.K6_DAYS:
        for _ in range(int(r.integers(60, 130))):
            t = dt.datetime.combine(day, dt.time(14, 0)) + dt.timedelta(seconds=float(r.uniform(0, 4 * 3600)))
            user, fp = FINGERPRINTS[int(r.integers(len(FINGERPRINTS)))]
            dur = float(np.exp(r.normal(np.log(420), 0.55)))
            dur = max(201.0, dur)
            ex = int(np.exp(r.normal(9.5, 1.4)))
            rows.append([t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000), "payroll_perf", user,
                         "%.3f" % dur, ex, int(ex * r.uniform(0.0005, 0.05)), fp])
    rows.sort()
    write_csv(path, ["logged_at", "database", "db_user", "duration_ms", "rows_examined", "rows_sent",
                     "query_fingerprint"], rows)
    return len(rows)
