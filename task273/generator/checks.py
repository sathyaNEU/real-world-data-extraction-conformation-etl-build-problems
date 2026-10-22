"""The build's assertions: the world against the pack, the estimator family and its margin, the analyst test on the
generator's clean truth, the ladder, every semantic fork row, the separation of the call from the asks' files, both ask
devices with their evidence, the cracker and the mirror, and the realism sweeps."""
import copy
import datetime as dt
import os
import re
import shutil
import subprocess

import numpy as np

import analysis as AN
import asks as A
import common as K
import cracker as CR
import models as M
import pack as P
import world as W

FAILS = []
CALL_FILES = ("jmeter", "k6", "gc", "events", "register")


def check(label, ok, detail=""):
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


def edit(a, b):
    m, n = len(a), len(b)
    if abs(m - n) > 2:
        return 9
    d = list(range(n + 1))
    for i in range(1, m + 1):
        p, d[0] = d[0], i
        for j in range(1, n + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[n]


def verdicts_of(G):
    return [c for c in K.CODES if G[c]["p99"] > K.SLA_MS]


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    X = b["X"]
    w = X["w"]
    R = res["R"]
    gold = fig["call"]["fix"]

    # ------------------------------------------------------------------ the call and its family
    check("CALL five endpoints on the freeze list", gold == ["EP01", "EP02", "EP05", "EP16", "EP22"], gold)
    for f in AN.GOLDEN_FAMILY:
        check("FAMILY %s names the golden set" % f, AN.verdicts(R, f) == gold, AN.verdicts(R, f))
    check("FAMILY margin from 800 ms at least 80 ms on every member and endpoint", fig["margin_floor_ms"] >= 80,
          fig["margin_floor_ms"])
    inputs = AN.call_inputs(target)
    check("RUNS each endpoint's run of record spans the warm-up and the measurement",
          all(inputs[c]["run"]["span"] >= K.RUN_S - 5 for c in K.CODES))
    check("RUNS the three first runs stopped early are the only second runs", fig["runs"]["stopped_early"] ==
          sorted(W.ABORTED), fig["runs"]["stopped_early"])

    # ------------------------------------------------------------------ the world against the pack
    for c in K.CODES:
        rows = w["runs"][c]["rows"]
        n_world = sum(1 for x in rows if K.WARMUP_S <= x[2] < K.RUN_S)
        if abs(n_world - R[c]["n"]) > 3:
            check("WORLD %s measured requests in the pack match the world's" % c, False, (n_world, R[c]["n"]))
    check("WORLD every endpoint's measured requests in the pack match the world's within 3 (window from the first "
          "request)", True)
    Pk = P.gc_pauses(target)
    for c in ("EP01", "EP16", "EP22"):
        svc = K.SERVICE[c]
        start = w["sched"][c]["start"]
        base = P.secs(start)
        for i, pod in enumerate(w["pods"][svc]):
            wp = [(base + a, base + bb) for a, bb, _ in w["runs"][c]["pauses"][i] if 0 <= a < K.RUN_S]
            pp = [(a, bb) for a, bb in Pk[pod] if base <= a < base + K.RUN_S]
            ok = len(wp) == len(pp) and all(abs(x[0] - y[0]) < 0.01 and abs(x[1] - y[1]) < 0.01 for x, y in zip(wp, pp))
            check("WORLD %s pod %s: the GC export's pauses are the world's to 10 ms" % (c, pod[-5:]), ok,
                  (len(wp), len(pp)))

    # ------------------------------------------------------------------ the analyst test on the clean truth
    raw_set, gold_set = [], []
    for c in K.CODES:
        rows = w["runs"][c]["rows"]
        Pw = [[(a, bb) for a, bb, _ in x] for x in w["runs"][c]["pauses"]]
        meas = [x for x in rows if K.WARMUP_S <= x[2] < K.RUN_S]
        lat = np.array([x[3] - x[2] for x in meas])
        if np.percentile(lat, K.PCT) * 1000.0 > K.SLA_MS:
            raw_set.append(c)
        svc = np.array([x[4] * W.warm(x[2]) for x in meas])
        if M.golden_p99(svc, Pw, K.WARMUP_S, K.RUN_S, 11 + int(c[2:]), n=400_000) > K.SLA_MS:
            gold_set.append(c)
    check("ANALYST TEST the easy route on the clean rows (every field read, every rule applied) files EP02, EP16, EP22",
          raw_set == ["EP02", "EP16", "EP22"], raw_set)
    check("ANALYST TEST the decisive step alone on the clean rows (the true service times) files the golden five",
          gold_set == gold, gold_set)

    # ------------------------------------------------------------------ the ladder
    expect = {"raw": 3, "raw_warm": 4, "drop": 0, "hdr": 10, "hdr_gc": 7, "hdr_gc_pods": 4, "lw": 10,
              "golden_rawsvc": 6, "pooled": 7}
    for k, n in expect.items():
        s = AN.verdicts(R, k)
        check("LADDER %s names %d endpoints, not the golden set" % (k, n), len(s) == n and s != gold, s)
    check("LADDER the default path files EP02, EP16 and EP22", AN.verdicts(R, "raw") == ["EP02", "EP16", "EP22"])
    longest = sorted(c for c in K.CODES if R[c]["longest"] > K.SLA_MS)
    share = sorted(c for c in K.CODES if R[c]["share"] > 1.0)
    check("LADDER a pause over 800 ms names the eight ParallelGC endpoints", longest == sorted(
        c for c in K.CODES if K.SERVICES[K.SERVICE[c]][0] == "parallel"), longest)
    check("LADDER over 1 percent of time paused names 22", len(share) == 22, len(share))

    # ------------------------------------------------------------------ the semantic forks (main call)
    N = 400_000
    G0 = AN.golden_only(inputs, N)
    check("SF2 the share answered within 800 ms is under 0.99 for exactly the golden five",
          sorted(c for c in K.CODES if G0[c]["within"] < 0.99) == gold,
          {c: round(G0[c]["within"], 4) for c in gold})
    Y = copy.deepcopy(inputs)
    for c in K.CODES:
        Y[c]["run"]["end"] = Y[c]["run"]["end"] - 0.001
    check("SF1 the server-side span (a millisecond off every response) keeps the call",
          verdicts_of(AN.golden_only(Y, N)) == gold)
    rs = P.runs(P.requests(target))
    Y = copy.deepcopy(inputs)
    for c in K.CODES:
        if len(rs[c]) > 1:
            a = rs[c][0]
            r = Y[c]["run"]
            m = a["start"] >= a["t0"] + K.WARMUP_S
            for f in ("start", "end", "pod", "ok", "thread"):
                r[f] = np.concatenate([a[f][m], r[f]])
    check("SF3 the first runs' measured minutes pooled with the run of record keep the call",
          verdicts_of(AN.golden_only(Y, N)) == gold)
    Y = copy.deepcopy(inputs)
    for c in K.CODES:
        Y[c]["t0"] -= 0.25
        Y[c]["t1"] -= 0.25
    check("SF4 a start a quarter second earlier keeps the call", verdicts_of(AN.golden_only(Y, N)) == gold)
    conc = _pauses_with_concurrent(target)
    Y = copy.deepcopy(inputs)
    for c in K.CODES:
        t0, t1 = Y[c]["t0"], Y[c]["t1"]
        Y[c]["pauses"] = [[(a, bb) for a, bb in conc.get(p, []) if bb > t0 - 60 and a < t1 + 60] for p in Y[c]["pods"]]
    check("SF5 G1's concurrent cycles counted as pauses keep the call", verdicts_of(AN.golden_only(Y, N)) == gold)
    Y = copy.deepcopy(inputs)
    for c in K.CODES:
        r = Y[c]["run"]
        k = r["ok"]
        for f in ("start", "end", "pod", "ok", "thread"):
            r[f] = r[f][k]
    check("SF6 the 500s left out keep the call", verdicts_of(AN.golden_only(Y, N)) == gold)
    std = subprocess.run(["pdftotext", P.path(target, "standard"), "-"], capture_output=True, text=True).stdout
    std1 = re.sub(r"\s+", " ", std)
    check("SF7 standard 3.3 files the run of record for the forecast volume",
          "no allowance is made for the difference between the two" in std1)
    eq = True
    for c in K.CODES:
        m = (inputs[c]["run"]["start"] >= inputs[c]["t0"]) & (inputs[c]["run"]["start"] < inputs[c]["t1"])
        _, cnt = np.unique(inputs[c]["run"]["pod"][m], return_counts=True)
        eq = eq and cnt.max() - cnt.min() <= 1
    check("SF8 the edge gave every pod an equal share of each run's requests (round robin)", eq)
    check("SF9 no endpoint within 90 ms of 800 on any family member", fig["margin_floor_ms"] >= 90,
          fig["margin_floor_ms"])

    # ------------------------------------------------------------------ Layer 1 mishandled, on the call's path
    starts = P.jvm_starts(target)
    first_only = {p: v[:1] for p, v in starts.items()}
    restarted = sorted(p for p, v in starts.items() if len(v) > 1)
    check("LAYER1 two pods restarted during the campaign (tax-forms and banking)", len(restarted) == 2, restarted)
    Y = copy.deepcopy(inputs)
    late = _pauses_from(target, first_only, stamp_is_start=False)
    for c in K.CODES:
        t0, t1 = Y[c]["t0"], Y[c]["t1"]
        Y[c]["pauses"] = [[(a, bb) for a, bb in late.get(p, []) if bb > t0 - 60 and a < t1 + 60] for p in Y[c]["pods"]]
    check("LAYER1 the uptime lines placed from each pod's first JVM start (restarts missed) keep the call",
          verdicts_of(AN.golden_only(Y, N)) == gold)
    Y = copy.deepcopy(inputs)
    st_start = _pauses_from(target, starts, stamp_is_start=True)
    for c in K.CODES:
        t0, t1 = Y[c]["t0"], Y[c]["t1"]
        Y[c]["pauses"] = [[(a, bb) for a, bb in st_start.get(p, []) if bb > t0 - 60 and a < t1 + 60]
                          for p in Y[c]["pods"]]
    moved = verdicts_of(AN.golden_only(Y, N))
    check("SF15 each GC stamp read as the pause's start adds EP06 (a Layer 1 misreading on the rebuild's route)",
          moved == sorted(gold + ["EP06"]), moved)
    plan_text = re.sub(r"\s+", " ", _docx_text(P.path(target, "plan")))
    check("SF15 the test plan files that the JVM writes a pause's line when the pause ends",
          "The JVM writes a pause's line when the pause ends, with its duration." in plan_text)

    # ------------------------------------------------------------------ the asks
    a, bb = res["a"], res["b"]
    tru_a = A.ask_a_truth(X["cust"], X["growth"])
    check("ASK A every forecast from the pack equals the generator's", all(a[c]["forecast"] == tru_a[c][2]
                                                                           for c in K.CODES))
    tru_b = A.ask_b_truth(X["inc"], X["legacy"], X["new"])
    check("ASK B every credit total from the pack equals the generator's", all(bb[c]["dollars"] == tru_b[c]
                                                                               for c in K.CODES))
    edge_h = [a[c]["hour"] for c in K.CODES]
    jan0, feb0 = P.secs(dt.datetime(2026, 1, 1)), P.secs(dt.datetime(2026, 2, 1))
    check("SF10 no busiest hour within five hours of January's edges", min(h - jan0 for h in edge_h) > 5 * 3600 and
          min(feb0 - h for h in edge_h) > 6 * 3600)
    ep, _ = P.register(target)
    syn = AN.synthetic_per_hour(target)
    alt_syn = AN.busiest(AN.january_series(target, ep, "golden"))
    alt_red = AN.busiest(AN.january_series(target, ep, "merged"), syn)
    check("SF11 the synthetic checks left in move 23 endpoints' busiest hour count",
          sum(alt_syn[c][0] != a[c]["peak"] for c in K.CODES) == 23)
    check("SF11 the old paths' redirects counted move the three renamed endpoints",
          sorted(c for c in K.CODES if alt_red[c][0] != a[c]["peak"]) == ["EP09", "EP19", "EP24"])
    ev = P.subscription_events(target)
    check("SF12 no subscription event on 1 January or 1 November", not any(
        e["effective_date"] in ("2026-01-01", "2026-11-01") for e in ev))
    inc = P.incidents(target)
    near = [k for k, i in inc.items() if abs(((i["start"] + AN.EST).date() - K.WINDOW_FROM).days) < 2 or
            abs(((i["start"] + AN.EST).date() - K.WINDOW_TO).days) < 2]
    check("SF14 no incident within a day of the window's edges", not near, near)
    rsg = {k: (i["start"] + AN.EST).date() for k, i in inc.items()}
    check("SF14 the end or UTC date of every incident falls on the same side of each edge", all(
        (K.WINDOW_FROM <= (i["start"] + AN.EST).date() <= K.WINDOW_TO) ==
        (K.WINDOW_FROM <= i["start"].date() <= K.WINDOW_TO) == (K.WINDOW_FROM <= i["end"].date() <= K.WINDOW_TO)
        for i in inc.values()))
    leg = P.legacy_credits(target)
    new = P.new_credits(target)
    issued = {(x["account"], x["incident"]): x for x in leg if x["status"] == "issued"}
    carried = [x for x in new if x["type"] == "credit" and (x["account"], x["incident"]) in issued]
    check("SF13 every carried-forward balance carries the new system's memo and none exceeds its legacy credit",
          all(x["memo"] == "Balance carried forward from legacy billing" and
              int(round(float(x["amount"]) * 100)) <= int(issued[(x["account"], x["incident"])]["amount"])
              for x in carried), len(carried))
    check("SF13 no native credit shares an account and incident with a legacy credit",
          all(x["memo"] == "Balance carried forward from legacy billing" for x in new
              if (x["account"], x["incident"]) in issued))
    rc = AN.route_codes(target)
    part = {c: 0 for c in K.CODES}
    for x in carried:
        lx = issued[(x["account"], x["incident"])]
        i = inc[x["incident"]]
        c = rc.get(i["comp"])
        if c and K.WINDOW_FROM <= (i["start"] + AN.EST).date() <= K.WINDOW_TO and \
                int(round(float(x["amount"]) * 100)) < int(lx["amount"]):
            part[c] += 1
    check("DEVICE B every endpoint carries a partly applied credit for a breach in the window",
          all(v > 0 for v in part.values()), part)
    emp = P.employers(target)
    resigned = [eid for eid, r in emp.items() if r["subscription_start"] > "2026-01-01" and any(
        e["employer_id"] == eid and e["event"] == "cancellation" and e["effective_date"] < r["subscription_start"]
        for e in ev)]
    check("DEVICE A accounts cancelled during 2026 and signed again carry a 2026 subscription start", len(resigned) >= 80,
          len(resigned))
    pay = [e for e in ev if e["event"] == "cancellation" and e["reason"] == "payment_failed"]
    check("DEVICE A the payment failures all fall on 2 March", {e["effective_date"] for e in pay} == {"2026-03-02"},
          len(pay))
    jan = AN.january_states(target)
    for c in K.CODES:
        pl = set(ep[c]["plans"])
        if not any(jan.get(e, (False, None))[0] and jan[e][1] in pl for e in resigned):
            check("DEVICE A %s has a re-signed account on its plans on 1 January" % c, False)
    check("DEVICE A every endpoint's plans hold a re-signed account on 1 January", True)

    # ------------------------------------------------------------------ the cracker and the mirror
    s = CR.score(target)
    check("CRACKER misses every Ask A figure", not s["cracker"]["a_hits"], s["cracker"]["a_hits"])
    check("CRACKER misses every Ask B figure", not s["cracker"]["b_hits"], s["cracker"]["b_hits"])
    check("MIRROR misses every ask figure", not s["mirror"]["a_hits"] and not s["mirror"]["b_hits"])
    check("PAIR ceiling at or under 40", s["pair_ceiling"] <= 40.0, s["pair_ceiling"])

    # ------------------------------------------------------------------ the separation line
    sep = os.path.join(task, "_separation_check")
    if os.path.exists(sep):
        shutil.rmtree(sep)
    os.makedirs(sep)
    for k in CALL_FILES:
        shutil.copy(P.path(target, k), os.path.join(sep, K.FILES[k]))
    Ys = AN.call_inputs(sep)
    check("SEPARATION the call computes from the load-test results, the GC export, the pod events and the register "
          "alone", verdicts_of(AN.golden_only(Ys, N)) == gold)
    shutil.rmtree(sep)

    # ------------------------------------------------------------------ realism and house fixes
    files = sorted(os.listdir(target))
    check("H4 the pack holds exactly the declared files", files == sorted(K.FILES.values()), files)
    contents = open(P.path(target, "contents"), encoding="utf-8").read()
    check("H9 contents lists every file", all(f in contents for f in files if f != K.FILES["contents"]))
    places = [x.strip().lower() for x in open(os.path.join(os.path.dirname(__file__), "h21_reference_places.txt"))
              if x.strip()]
    for nm in ("Mirrendale",):
        n = nm.lower()
        hit = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not hit, hit[:3])
    for f in files:
        raw = open(os.path.join(target, f), "rb").read()
        check("H1 no writer's name in %s" % f, b"ReportLab" not in raw and b"openpyxl" not in raw.lower()
              and b"matplotlib" not in raw.lower() and b"python-docx" not in raw.lower())
        if f.endswith((".csv", ".txt", ".jtl", ".log", ".yaml", ".html", ".json")):
            check("REALISM no em dash in %s" % f, "—".encode() not in raw)
    import docx
    import openpyxl
    golden = os.path.join(task, "golden")
    for f in [os.path.join(target, x) for x in files if x.endswith(".xlsx")] + \
            [os.path.join(golden, x) for x in sorted(os.listdir(golden)) if x.endswith(".xlsx")]:
        try:
            openpyxl.load_workbook(f)
            ok = True
        except Exception as e:      # noqa: BLE001
            ok = False
        check("REALISM %s opens" % os.path.basename(f), ok)
    try:
        docx.Document(P.path(target, "plan"))
        ok = True
    except Exception:               # noqa: BLE001
        ok = False
    check("REALISM the test plan opens", ok)
    dates = []
    for line in open(P.path(target, "gc"), encoding="utf-8"):
        dates.append(line[:10])
    check("H16 the GC export ends by 19 November", max(dates) <= "2026-11-19", max(dates))
    check("H16 the new system's credits run to 19 November", max(x["created_at"][:10] for x in new) <= "2026-11-19")
    check("H16 no incident starts after the pack's assembly", max(i["start"] for i in inc.values()) < K.ASSEMBLED)
    plan_txt = _docx_text(P.path(target, "plan"))
    banned = ["coordinated", "omission", "open-loop", "open loop", "back-fill", "backfill", "hdrhistogram",
              "customers would", "missing", "thinned", "under-sample", "undersample"]
    for name, txt in (("standard", std.lower()), ("test plan", plan_txt.lower()),
                      ("changelog", open(P.path(target, "changelog"), encoding="utf-8").read().lower()),
                      ("synthetic checks", open(P.path(target, "synthetic"), encoding="utf-8").read().lower())):
        hit = [x for x in banned if x in txt]
        check("LEAK the %s names no device or method word" % name, not hit, hit)
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)


def _docx_text(path):
    import zipfile
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    return re.sub(r"<[^>]+>", " ", x)


def _pauses_with_concurrent(target):
    """The pod pauses with G1's concurrent cycles read as pauses too (SF5)."""
    starts = P.jvm_starts(target)
    out = {}
    for line in open(P.path(target, "gc"), encoding="utf-8"):
        m = P.LINE.match(line.rstrip("\n"))
        if not m:
            continue
        ingest, pod, deco, tags, n, body = m.groups()
        if not (body.startswith("Pause ") or body.startswith("Concurrent Mark Cycle")):
            continue
        dur = float(re.search(r"([\d.]+)ms$", body).group(1)) / 1000.0
        if deco.endswith("s") and "T" not in deco:
            js = [s for s in starts[pod] if s <= P.utc(ingest + "Z")]
            end = js[-1] + float(deco[:-1])
        else:
            local = dt.datetime.strptime(deco[:23], "%Y-%m-%dT%H:%M:%S.%f")
            end = P.secs(local) + 5 * 3600
        out.setdefault(pod, []).append((end - dur, end))
    res = {}
    for p, v in out.items():
        v.sort()
        mg = []
        for a, b in v:
            if mg and a <= mg[-1][1]:
                mg[-1] = (mg[-1][0], max(mg[-1][1], b))
            else:
                mg.append((a, b))
        res[p] = mg
    return res


def _pauses_from(target, starts, stamp_is_start=False):
    """The pod pauses with the given JVM starts for the uptime lines, the stamp read as the pause's end (the JVM's
    way) or as its start."""
    out = {}
    for line in open(P.path(target, "gc"), encoding="utf-8"):
        m = P.LINE.match(line.rstrip("\n"))
        if not m:
            continue
        ingest, pod, deco, tags, n, body = m.groups()
        if not body.startswith("Pause "):
            continue
        dur = float(re.search(r"([\d.]+)ms$", body).group(1)) / 1000.0
        if deco.endswith("s") and "T" not in deco:
            js = [s for s in starts[pod] if s <= P.utc(ingest + "Z")]
            stamp = js[-1] + float(deco[:-1])
        else:
            local = dt.datetime.strptime(deco[:23], "%Y-%m-%dT%H:%M:%S.%f")
            stamp = P.secs(local) + 5 * 3600
        out.setdefault(pod, []).append((stamp, stamp + dur) if stamp_is_start else (stamp - dur, stamp))
    res = {}
    for p, v in out.items():
        v.sort()
        mg = []
        for a, b in v:
            if mg and a <= mg[-1][1]:
                mg[-1] = (mg[-1][0], max(mg[-1][1], b))
            else:
                mg.append((a, b))
        res[p] = mg
    return res
