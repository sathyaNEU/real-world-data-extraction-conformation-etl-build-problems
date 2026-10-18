"""task197 verifier. Reads only the shipped bundle under target/ (plus the goldens it checks) and
rebuilds the call and every graded figure from it, with no access to the generator's arrays.

Usage: python3 task197/generator/verify.py [task_dir]
"""
import os, sys, csv, json, sqlite3, datetime as dt, statistics, zipfile, re
from collections import defaultdict

TASK = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                       os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TGT = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
DEADBAND, SPAN = 0.010, 0.190
QUAL_UNDER, QUAL_OVER, QUAL_SECS = 49.920, 50.080, 15
TOL = 90.0
OFFSET = dt.timedelta(hours=2)
FAILS, CHECKS = [], []

def ck(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        FAILS.append("%s: %s" % (name, detail))

def rd(path):
    with open(os.path.join(TGT, path), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

def tl(s):
    return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")

def episodes_from(seq, threshold, over=False):
    """Qualifying episodes inside one published extract: the extract is split into contiguous runs of
    seconds first, so a gap in the published series never joins two deviations."""
    out = []
    runs, cur = [], []
    for i, (t, f) in enumerate(seq):
        if cur and (t - cur[-1][0]).total_seconds() != 1.0:
            runs.append(cur); cur = []
        cur.append((t, f))
    if cur:
        runs.append(cur)
    for run in runs:
        hit = [(f >= threshold) if over else (f <= threshold) for (_, f) in run]
        i, n = 0, len(run)
        while i < n:
            if not hit[i]:
                i += 1
                continue
            j = i
            while j < n and hit[j]:
                j += 1
            if j - i >= QUAL_SECS:
                seg = run[i:j]
                k = max(range(len(seg)), key=lambda x: seg[x][1]) if over else \
                    min(range(len(seg)), key=lambda x: seg[x][1])
                out.append((seg[0][0], seg[-1][0], seg[k][0], seg[k][1]))
            i = j
    return out


def main():
    # ---- frequency -------------------------------------------------------------------------
    rows = rd("operator/system_frequency_1s_extracts.csv")
    byext = defaultdict(list)
    for r in rows:
        byext[r["extract_id"]].append((ts(r["ts_utc"]), float(r["frequency_hz"])))
    freq = {}
    under, over = [], []
    for eid, seq in byext.items():
        seq.sort()
        for t, f in seq:
            freq[t] = f
        under += episodes_from(seq, QUAL_UNDER)
        over += episodes_from(seq, QUAL_OVER, over=True)
    ck("frequency extracts read", len(rows) > 25000, "%d one-second rows" % len(rows))
    ck("qualifying episodes found", len(under) > 50 and len(over) > 20,
       "%d under-frequency, %d over-frequency" % (len(under), len(over)))

    # minute summary: the only frequency series covering the whole window
    minutes = {}
    for r in rd("operator/system_frequency_minute_summary.csv"):
        minutes[ts(r["minute_utc"])] = (float(r["frequency_min_hz"]), float(r["frequency_max_hz"]))

    # ---- commitments, programme, events ----------------------------------------------------
    com = defaultdict(set)
    cap = {}
    for r in rd("platform/fcr_block_commitments.csv"):
        com[(r["delivery_date"], int(r["block"]))].add(r["site_id"])
        cap[r["site_id"]] = float(r["committed_mw"])
    prog = {}
    for r in rd("platform/site_programme_15min.csv"):
        prog[(r["site_id"], tl(r["period_start_local"]))] = float(r["programme_mw"])
    ev = rd("platform/control_platform_event_log.csv")
    cancelled = {e["supersedes_event_id"] for e in ev if e["event_type"] == "correction"}
    unavail = defaultdict(list)
    for e in ev:
        if e["event_type"] != "reserve_unavailable" or e["event_id"] in cancelled:
            continue
        a = tl(e["start_local"]) - OFFSET
        unavail[e["site_id"]].append((a, a + dt.timedelta(minutes=int(e["duration_min"]))))

    def contracted(site, t_utc):
        loc = t_utc + OFFSET
        block = loc.hour // 4 + 1
        if site not in com.get((loc.date().isoformat(), block), ()):
            return False
        return not any(a <= t_utc < b for (a, b) in unavail.get(site, []))

    def setpoints(site, t_utc):
        loc = t_utc + OFFSET
        p0 = loc.replace(minute=(loc.minute // 15) * 15, second=0, microsecond=0)
        cur = prog.get((site, p0))
        prev = prog.get((site, p0 - dt.timedelta(minutes=15)), cur)
        return prev, cur, p0

    # ---- the archive -----------------------------------------------------------------------
    con = sqlite3.connect(os.path.join(TGT, "platform", "vkf_highres_archive.sqlite"))
    nrec = con.execute("SELECT count(*) FROM recording").fetchone()[0]
    nrow = con.execute("SELECT count(*) FROM power_1s").fetchone()[0]
    ck("archive rows", nrow > 25000, "%d one-second power rows in %d recordings" % (nrow, nrec))
    power = defaultdict(dict)
    for sid, t, p in con.execute("""SELECT r.site_id, w.ts_utc, w.p_mw FROM power_1s w
                                    JOIN recording r ON r.recording_id = w.recording_id"""):
        power[sid][ts(t)] = p
    con.close()

    # ---- each site's traverse span, from boundaries with no qualifying episode --------------
    marked = set()
    for (a, b, x, f) in under + over:
        t = a - dt.timedelta(seconds=120)
        while t <= b + dt.timedelta(seconds=120):
            marked.add(t); t += dt.timedelta(seconds=1)
    spans = {}
    for sid, series in power.items():
        secs = sorted(series)
        seglist = []
        for t in secs:
            loc = t + OFFSET
            if not (loc.second == 0 and loc.minute % 15 == 0):
                continue
            prev, cur, p0 = setpoints(sid, t)
            if prev is None or cur is None or abs(cur - prev) < 1.0:
                continue
            back = prog.get((sid, p0 - dt.timedelta(minutes=30)))
            if back is None or abs(prev - back) > 0.35:
                continue
            if any((t + dt.timedelta(seconds=k)) in marked for k in range(-30, 215)):
                continue
            # the frequency has to sit inside the dead band across the whole traverse, or the site's
            # own response is moving its output alongside its programme
            m0 = t.replace(second=0)
            quiet = True
            for mk in range(0, 5):
                mm = minutes.get(m0 + dt.timedelta(minutes=mk))
                if mm is None or mm[0] < 50.0 - DEADBAND or mm[1] > 50.0 + DEADBAND:
                    quiet = False; break
            if not quiet:
                continue
            if any((t + dt.timedelta(seconds=k)) not in series for k in range(0, 205)):
                continue
            ys = [series[t + dt.timedelta(seconds=k)] for k in range(0, 205)]
            seglist.append((prev, cur - prev, ys))
        best, bestres = None, None
        for S in range(40, 361):
            res = 0.0
            for (prev, step, ys) in seglist:
                for k, y in enumerate(ys):
                    frac = k / float(S)
                    if frac > 1.0:
                        frac = 1.0
                    e = y - (prev + step * frac)
                    res += e * e
            if bestres is None or res < bestres:
                best, bestres = S, res
        if seglist and best:
            spans[sid] = float(best)
    ck("traverse spans recovered", len(spans) >= 9 and all(
           abs(spans[s] - 900.0) > 1 for s in spans),
       ", ".join("%s=%.0fs" % (k, v) for k, v in sorted(spans.items())))

    # ---- the four baselines ----------------------------------------------------------------
    def score(eps, over_side=False):
        agg = defaultdict(lambda: defaultdict(list))
        for (a, b, x, f) in eps:
            dev = abs(50.0 - f) - DEADBAND
            sgn = -1.0 if over_side else 1.0
            # the last undisturbed second at or before the episode start
            pre = None
            t = a
            while t >= a - dt.timedelta(seconds=900):
                if t in freq and abs(freq[t] - 50.0) <= DEADBAND:
                    pre = t; break
                t -= dt.timedelta(seconds=1)
            for sid in power:
                if not contracted(sid, x) or x not in power[sid]:
                    continue
                prev, cur, p0 = setpoints(sid, x)
                if prev is None or cur is None:
                    continue
                cg = cap[sid] / SPAN
                v = power[sid][x]
                el = (x - (p0 - OFFSET)).total_seconds()
                frac = min(1.0, el / spans.get(sid, 900.0))
                base = prev + (cur - prev) * frac
                agg[sid]["traj"].append(sgn * (v - base) / dev / cg)
                agg[sid]["sp"].append(sgn * (v - cur) / dev / cg)
                agg[sid]["lin"].append(sgn * (v - (prev + (cur - prev) * el / 900.0)) / dev / cg)
                if pre is not None and pre in power[sid]:
                    agg[sid]["pre"].append(sgn * (v - power[sid][pre]) / dev / cg)
        return {sid: {k: 100 * statistics.fmean(vs) for k, vs in d.items() if vs} |
                     {"n": len(d["traj"])} for sid, d in agg.items()}

    su, so = score(under), score(over, True)
    print("spans: " + ", ".join("%s=%.0fs" % (k, spans[k]) for k in sorted(spans)))
    print("under n: " + ", ".join("%s=%d" % (k, su[k]["n"]) for k in sorted(su)))
    print("over  n: " + ", ".join("%s=%d" % (k, so[k]["n"]) for k in sorted(so)))
    F = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    order = sorted(su, key=lambda s: (round(su[s]["traj"]), s))
    ck("call reproduces", order[0] == F["call_site"],
       "verifier %s %.1f, figures.json %s %.0f" % (order[0], su[order[0]]["traj"], F["call_site"], F["call_gain"]))
    ck("runner-up reproduces", order[1] == F["runner_site"],
       "verifier %s %.1f" % (order[1], su[order[1]]["traj"]))
    for r in F["scorecard"]:
        got = round(su[r["site"]]["traj"])
        ck("gain %s" % r["site"], abs(got - r["gain_pct"]) < 1e-9,
           "verifier %.2f, golden %.0f" % (su[r["site"]]["traj"], r["gain_pct"]))
        ck("episodes %s" % r["site"], su[r["site"]]["n"] == r["episodes"],
           "verifier %d, golden %d" % (su[r["site"]]["n"], r["episodes"]))
    for d in F["down"]:
        if d["gain_pct"] is None:
            ck("down none %s" % d["site"], d["site"] not in so or so[d["site"]]["n"] == 0, "no episode")
            continue
        got = round(so[d["site"]]["traj"])
        ck("down gain %s" % d["site"], abs(got - d["gain_pct"]) < 1e-9,
           "verifier %.2f, golden %.0f" % (so[d["site"]]["traj"], d["gain_pct"]))
    # the naive baselines each land on a site that is not the call
    for key, who in (("pre", F["ladder_names"]["pre"]), ("sp", F["ladder_names"]["sp"]),
                     ("lin", F["ladder_names"]["lin"])):
        o = sorted([s for s in su if key in su[s]], key=lambda s: round(su[s][key], 1))
        ck("rung %s names %s" % (key, who), o[0] == who and o[0] != F["call_site"],
           "verifier %s %.1f" % (o[0], su[o[0]][key]))

    # ---- documents read back from the shipped bytes -----------------------------------------
    try:
        from pypdf import PdfReader
        std = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in
                     PdfReader(os.path.join(TGT, "standards", "reserve_performance_standard_v4.pdf")).pages))
        tc = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in
                    PdfReader(os.path.join(TGT, "operator", "fcr_technical_conditions_2026.pdf")).pages))
    except Exception as exc:
        std = tc = ""
        ck("pdf text read", False, str(exc))
    for name, text, must, mustnot in (
            ("standard", std, ["49.920", "50.080", "15 consecutive seconds", "190",
                               "nearest whole per cent", "90 per cent", "equal weight",
                               "extreme second"], ["ramp", "linear ramp", "traverse"]),
            ("conditions", tc, ["10 millihertz", "200 millihertz", "30 seconds", "90 per cent",
                                "additional to the active power"], ["ramp rate", "ramps linearly"])):
        for m in must:
            ck("%s states %r" % (name, m), m in text, "not found in the shipped pdf")
        for m in mustnot:
            ck("%s silent on %r" % (name, m), m not in text.lower(), "the pdf states it")
    ck("positive control on the pdf sweep", "Veerkracht" in std and "zzqq" not in std,
       "the assertion can find and fail to find text")

    # ---- input gates -------------------------------------------------------------------------
    files, fmts = [], set()
    for root, _, names in os.walk(TGT):
        for n in names:
            files.append(os.path.join(root, n)); fmts.add(os.path.splitext(n)[1].lower())
    ck("10 or more files", len(files) >= 10, "%d files" % len(files))
    ck("3 or more formats", len({f for f in fmts if f}) >= 3, ", ".join(sorted(fmts)))
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    ck("2 or more distractors named", len(md.get("distractors", [])) >= 2,
       ", ".join(d["path"] for d in md.get("distractors", [])))
    for d in md.get("distractors", []):
        ck("distractor not named in a file name", "distract" not in d["path"].lower(), d["path"])
    ck("provenance recorded", all(k in md for k in ("source", "licence", "generated")), sorted(md))

    # ---- the goldens --------------------------------------------------------------------------
    memo = open(os.path.join(GOLD, "response_determination.md"), encoding="utf-8").read()
    ck("memo names the call", F["call_name"] in memo and ("%.0f" % F["call_gain"]) in memo, "")
    ck("memo names the runner-up and the gap",
       F["runner_name"] in memo and ("%.0f" % F["gap_pp"]) in memo, "")
    with zipfile.ZipFile(os.path.join(GOLD, "site_response_scorecard.xlsx")) as z:
        names = z.namelist()
        blob = "".join(z.read(n).decode("utf-8", "replace") for n in names
                       if n.startswith(("xl/worksheets/", "xl/sharedStrings")))
    ck("workbook carries the chart", any(n.startswith("xl/charts/") for n in names),
       ", ".join(n for n in names if "chart" in n) or "no chart part")
    ck("workbook names the call", F["call_name"] in blob, "")
    ck("workbook carries every scorecard gain",
       all(("%g" % r["gain_pct"]) in blob for r in F["scorecard"]),
       ", ".join("%g" % r["gain_pct"] for r in F["scorecard"] if ("%g" % r["gain_pct"]) not in blob))

    print("%d checks, %d failed" % (len(CHECKS), len(FAILS)))
    for name, ok, detail in CHECKS:
        if not ok:
            print("  FAIL %s: %s" % (name, detail))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
