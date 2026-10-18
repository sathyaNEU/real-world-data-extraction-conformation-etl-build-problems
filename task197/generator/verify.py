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
    # where the published deviation opens, relative to a settlement period start, read off the
    # shipped extract file alone
    starts = {}
    for r in rows:
        starts.setdefault(r["extract_id"], []).append(ts(r["ts_utc"]))
    opens = [min(v) + OFFSET for v in starts.values()]
    away = [t for t in opens if 2 <= ((t.minute % 15) * 60 + t.second) // 60 <= 13]
    ck("the shipped record's deviation opens away from a period boundary as well as on one",
       len(away) >= 40, "%d of %d published extracts open 2 to 13 minutes into a period, %.1f per "
       "cent" % (len(away), len(opens), 100.0 * len(away) / len(opens)))
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
    # The window a logged withdrawal actually covers. The platform writes its log row 90 seconds
    # after the window opens, on every row; the start_local field agrees with that on most rows and
    # sits 7,290 seconds from it on the rest, which cannot be a local offset of a 90 second lag. The
    # log timestamp is the clock that holds across the whole file, so it is the one the hours are
    # taken from. The verifier records both gaps and asserts the set below.
    unavail = defaultdict(list)
    for e in ev:
        if e["event_type"] != "reserve_unavailable" or e["event_id"] in cancelled:
            continue
        a = ts(e["logged_utc"]) - dt.timedelta(seconds=90)
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
    # the archive's own spread, read back from the shipped database: an organ identical on every
    # dimension but its timestamps announces the step it was built for
    meta = con.execute("""SELECT trigger, site_id, start_utc,
                          (julianday(end_utc) - julianday(start_utc)) * 86400 + 1 AS secs
                          FROM recording""").fetchall()
    trig = {}
    for (tg, sid, st, secs) in meta:
        trig.setdefault(tg, []).append((sid, st, int(round(secs))))
    ck("the shipped archive holds captures of four or more kinds", len(trig) >= 4,
       ", ".join("%s %d" % (k, len(v)) for k, v in sorted(trig.items(), key=lambda x: -len(x[1]))))
    alen = {x[2] for v in trig.values() for x in v}
    aoff = set()
    for v in trig.values():
        for (sid, st, secs) in v:
            t = ts(st) + OFFSET
            aoff.add((t.minute % 15) * 60 + t.second)
    ck("the shipped archive's lengths and offsets vary",
       len(alen) >= 100 and len(aoff) >= 30,
       "%d distinct lengths %d..%d, %d distinct quarter-hour offsets"
       % (len(alen), min(alen), max(alen), len(aoff)))
    big = max(trig, key=lambda k: len(trig[k]))
    ck("positive control, the archive reader can tell the capture kinds apart",
       big == "FREQ-DEV" and len(trig[big]) > 1000 and "zzqq" not in trig,
       "largest kind %s with %d recordings" % (big, len(trig[big])))
    for k, v in trig.items():
        if k == "FREQ-DEV":
            continue
        ck("capture kind %s is a minority of the archive" % k, len(v) < nrec * 0.5,
           "%d of %d" % (len(v), nrec))
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
    ck("the rung 0 figure the write-up prints reproduces from the bundle",
       abs(su[F["rung0_site"]]["pre"] - F["rung0_pre"]) < 0.05,
       "verifier %.2f, write-up %.1f" % (su[F["rung0_site"]]["pre"], F["rung0_pre"]))
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
    # Positive controls on the same code path as the absence checks: a sentence the writer put in
    # each pdf, searched the way the absence checks search, and a sentence that is not there.
    for name, text, control in (("standard", std, "reserve performance standard"),
                                ("conditions", tc, "frequency containment reserve")):
        ck("positive control, %s pdf extraction is non-empty" % name, len(text) > 500,
           "%d characters extracted" % len(text))
        ck("positive control, %s absence check can find what is there" % name,
           control in text.lower(), "control sentence %r not found" % control)
        ck("positive control, %s absence check can fail" % name,
           "zzqq-not-in-this-document" not in text.lower(), "")
    # clause 4 and clause 5 carry the ask quantities; the call leans on clause 2 and clause 3
    for m in ["in fact not holding reserve", "one decimal place",
              "no delivery-block commitment", "above programme", "below programme",
              "rounded once at the end", "grid loss adjustment"]:
        ck("standard states %r" % m, m in std, "not found in the shipped pdf")
    for m in ["correction", "two hours", "settlement_period", "interval it closes",
              "period ending", "utc clock", "block average", "block averages"]:
        ck("standard silent on %r" % m, m not in std.lower(), "the pdf states it")

    # ---- the shipped register, read back through the verifier's own reader -------------------
    import openpyxl
    rwb = openpyxl.load_workbook(os.path.join(TGT, "register", "asset_register.xlsx"))
    ck("register sheets read", "Sites" in rwb.sheetnames and "Notes" in rwb.sheetnames,
       ", ".join(rwb.sheetnames))
    rws = rwb["Sites"]
    rhdr = [c.value for c in rws[1]]
    reg = {}
    for row in rws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(rhdr, row))
        reg[d["Site id"]] = d
    ck("positive control, the register reader sees nine rows and the capacity column",
       len(reg) == 9 and "Contracted FCR (MW)" in rhdr, "%d rows, %d columns" % (len(reg), len(rhdr)))
    ck("register capacities match the contracted gains the call uses",
       all(abs(float(reg[r["site"]]["Contracted FCR (MW)"]) / 0.190 - r["contract_gain"]) < 0.01
           for r in F["scorecard"]), "")
    nblob = " ".join(str(c.value) for c in rwb["Notes"]["A"] if c.value)
    ck("positive control, the register notes reader finds text", "asset master" in nblob.lower(),
       nblob[:60])
    ck("register notes silent on the interval index and the logged clock",
       "interval" not in nblob.lower() and "utc" not in nblob.lower(), nblob[:80])

    # ---- ask B recomputed from the bundle ----------------------------------------------------
    cap = {k: float(v["Contracted FCR (MW)"]) for k, v in reg.items()}
    com = {}
    for r in rd("platform/fcr_block_commitments.csv"):
        com.setdefault((r["site_id"], r["delivery_date"]), set()).add(int(r["block"]))
    committed = dict.fromkeys(range(1, 7), 0.0)
    for (sid, _d), blocks in com.items():
        for b in blocks:
            committed[b] += cap[sid] * 4.0
    ev = rd("platform/control_platform_event_log.csv")
    cancelled = {e["supersedes_event_id"] for e in ev if e["event_type"] == "correction"}
    lag = {}
    lost = dict.fromkeys(range(1, 7), 0.0)
    for e in ev:
        if e["event_type"] != "reserve_unavailable":
            continue
        start = ts(e["logged_utc"]) - dt.timedelta(seconds=90) + dt.timedelta(hours=2)
        gap = (ts(e["logged_utc"]) + dt.timedelta(hours=2) - tl(e["start_local"])).total_seconds()
        lag[gap] = lag.get(gap, 0) + 1
        if e["event_id"] in cancelled:
            continue
        lost[start.hour // 4 + 1] += cap[e["site_id"]] * int(e["duration_min"]) / 60.0
    ck("the event log's two clocks disagree on a known set of rows",
       set(lag) == {90.0, 7290.0}, ", ".join("%.0fs x%d" % (k, v) for k, v in sorted(lag.items())))
    for b in F["availability"]:
        ck("held available block %d" % b["block"],
           abs(committed[b["block"]] - lost[b["block"]] - b["available"]) < 0.05,
           "verifier %.1f, golden %.1f" % (committed[b["block"]] - lost[b["block"]], b["available"]))
        ck("shortfall block %d" % b["block"], abs(lost[b["block"]] - b["shortfall"]) < 0.05,
           "verifier %.1f, golden %.1f" % (lost[b["block"]], b["shortfall"]))

    # ---- ask C recomputed from the bundle ----------------------------------------------------
    met = rd("settlement/metered_volumes_15min.csv")
    ck("the meter file is indexed by the interval it closes, not the one it opens",
       "interval_ts_local" in met[0] and "period_start_local" not in met[0],
       ", ".join(sorted(met[0])))
    ean = {str(v["Metering point (EAN)"]): k for k, v in reg.items()}
    for e in ev:
        if e["event_type"] == "metering":
            for c in {r["metering_point"] for r in met} - set(ean):
                ean[c] = e["site_id"]
    prog = {}
    for r in rd("platform/site_programme_15min.csv"):
        prog[(r["site_id"], tl(r["period_start_local"]))] = float(r["programme_mw"])
    above = dict.fromkeys(reg, 0.0)
    below = dict.fromkeys(reg, 0.0)
    for r in met:
        sid = ean.get(r["metering_point"])
        key = tl(r["interval_ts_local"]) - dt.timedelta(minutes=15)
        if sid is None or (sid, key) not in prog:
            continue
        if key.hour // 4 + 1 in com.get((sid, key.date().isoformat()), ()):
            continue
        v = float(r["net_volume"]) / (1000.0 if r["unit"] == "kWh" else 1.0)
        dv = v - prog[(sid, key)] * 0.25
        if dv >= 0:
            above[sid] += dv
        else:
            below[sid] += -dv
    for r in F["exposure"]:
        ck("above programme %s" % r["site"], abs(above[r["site"]] - r["above"]) < 0.05,
           "verifier %.1f, golden %.1f" % (above[r["site"]], r["above"]))
        ck("below programme %s" % r["site"], abs(below[r["site"]] - r["below"]) < 0.05,
           "verifier %.1f, golden %.1f" % (below[r["site"]], r["below"]))
    ck("exposure portfolio totals", abs(sum(above.values()) - F["exposure_above_total"]) < 0.05
       and abs(sum(below.values()) - F["exposure_below_total"]) < 0.05,
       "verifier %.1f / %.1f" % (sum(above.values()), sum(below.values())))
    ck("the meter file covers the window's intervals once per metering point",
       len(met) == 9 * 21 * 96, "%d rows" % len(met))

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
