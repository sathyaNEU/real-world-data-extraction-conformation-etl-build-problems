"""Generator checks for task204 v2: the three-rules block (R1 to R3c), every SF row, the C1 families, mess
neutrality per Layer 1 item, the ladder, the input gates and the realism sweep. Exit 1 on any failure."""
import collections
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import pack             # noqa: E402
import params as P      # noqa: E402
import world_net as N   # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def grounds(series, polys):
    return sorted(tuple(t["districts"]) + (t["n"],) for t in A.team_table(series, polys))


def main():
    res = A.run_all(TARGET)
    offs, gt, cache, polys = res["_offs"], res["_gtfs"], res["_cache"], res["_polys26"]
    rms, tpo, codes, stref, fare = res["_rms"], res["_tpo"], res["_codes"], res["_stref"], res["_fare_codes"]
    gold_series, gold_runs = A.golden_series(offs, gt, cache=cache)
    G = grounds(gold_series, polys)
    gold_tab = res["golden"]

    # ---- world truth -------------------------------------------------------------------------------
    w = pack.make_world()
    tmp = tempfile.mkdtemp(prefix="t204chk_")
    pack.write_pack(w, os.path.join(tmp, "target"))
    idx = w.rms_index
    truth = collections.defaultdict(set)
    for e in w.ev.events:
        if e["group"] and id(e) in idx and P.W26[0] <= e["t_occ"].date() <= P.W26[1]:
            truth[e["group"]].add(idx[id(e)])
    gold_sets = sorted(sorted(t["ids"]) for t in gold_tab)
    truth_sets = sorted(sorted(v) for v in truth.values())
    check("L-golden-truth: the golden series are exactly the four offender groups the world built", gold_sets == truth_sets,
          "%s" % [len(s) for s in gold_sets])

    # ---- ladder ---------------------------------------------------------------------------------------
    check("L-rung0: the field's linkage files seven series teams", len(res["rung0"]) == 7, str(len(res["rung0"])))
    check("L-rung1: one team per district carrying a series files six teams", len(res["rung1"]) == 6, str(len(res["rung1"])))
    check("L-rung2: the corridor merge files three teams", len(res["rung2"]) == 3, str(len(res["rung2"])))
    merged = max(res["rung2"], key=lambda t: t["n"])
    check("L-rung2-merge: the merged corridor team holds Cobb Street and the four Eastline group stations",
          set(merged["stations"]) == {"Cobb Street", "Ridgeview", "Ashford Road", "Millbrook", "Union Yards"}, str(merged["stations"]))
    check("L-golden: four teams on grounds 4/6/7/9, 5, 8 and 6", sorted(tuple(t["districts"]) for t in gold_tab)
          == sorted([("D4", "D6", "D7", "D9"), ("D5",), ("D8",), ("D6",)]), str([t["districts"] for t in gold_tab]))
    check("L-separation: no rung files the golden's team set",
          all(sorted(tuple(t["districts"]) for t in res[k]) != sorted(tuple(t["districts"]) for t in gold_tab)
              for k in ("rung0", "rung1", "rung2")))
    check("L-reversal: the corrections walk 7, 6, 3 and only the decisive move turns back to 4",
          [len(res["rung0"]), len(res["rung1"]), len(res["rung2"]), len(gold_tab)] == [7, 6, 3, 4])
    check("L-runs: eighteen trips carry two or three offences each", len(gold_runs) == 18, str(len(gold_runs)))

    # ---- three rules ------------------------------------------------------------------------------------
    clean = []
    for e in w.ev.events:
        if P.W26[0] <= e["t_occ"].date() <= P.W26[1]:
            clean.append({"src": "W", "id": str(id(e)), "t": e["t_occ"], "station": N.STN[e["station"]]["name"] if e["station"] else None,
                          "x": e["x"], "y": e["y"], "mo": {"SNATCH": "SNATCH", "STREET": "STREET-CONFRONT", "STREET-WEAPON": "STREET-WEAPON", "PICKPOCKET": "STEALTH"}[e["mo"]],
                          "sus": e["suspects"], "alo": e["age_low"], "ahi": e["age_high"], "loc": e["loc"], "offence": e["offence"]})
    r0_clean = A.local_series(clean)
    check("R3a: on the clean truth the default path (the field's linkage) files seven teams, not the golden's four",
          len(r0_clean) == 7, str(len(r0_clean)))
    g_clean, _ = A.golden_series(clean, gt, cache=cache)
    check("R3b: the default path with only the trip step added files the golden's four teams", len(g_clean) == 4, str(len(g_clean)))
    r2_clean = A.corridor_series(clean)
    check("R3b-lower: the corridor correction alone stays wrong (three teams)", len(r2_clean) == 3, str(len(r2_clean)))
    names = set()
    for root, _, files in os.walk(TARGET):
        for f in files:
            if f.endswith((".csv", ".txt")):
                with open(os.path.join(root, f), encoding="utf-8") as fh:
                    names.update(c.lower() for c in next(csv.reader(fh)))
    check("R1: offence-level records ship and no column holds a series, group or trip of an offence",
          not any(re.search(r"series|group|crew|run_id", c) for c in names) and "occurred_from_local" in names)
    check("R1-raw: the decisive step reads the timetable's stop times", len(gt.st) > 500)
    directive = A_pdf_text(os.path.join(TARGET, "ops41_series_crime_response_directive.pdf"))
    check("R3c-control: the directive's text is readable (positive control)", "three or more offences committed by the same offender group" in directive)
    check("R3c: no filed sentence names a train, trip, timetable or link between offences",
          not re.search(r"\b(train|trip|timetable|schedule|ride|link)", directive.lower()))
    note = A_docx_text(os.path.join(TARGET, "summer_deployment_planning_note.docx"))
    check("R3c-note: the planning note carries no team count, ground or group (no voice, no decoy)",
          not re.search(r"\b(teams? (?:for|on)|four|seven|three|Eastline group|crew)\b", note) and "OPS-41" in note)

    # ---- semantic forks ----------------------------------------------------------------------------------
    lone = [dict(o, sus=max(o["sus"], 2)) for o in offs]
    alt_lone = A.local_series(lone)
    check("SF1: counting lone offenders as groups changes the series (ruled out by OPS-41 section 3)",
          grounds(alt_lone, polys) != grounds(A.local_series(offs), polys), "%d vs %d" % (len(alt_lone), len(res["rung0"])))
    two = [c for c in A.golden_series(offs, gt, cache=cache)[0]]
    check("SF2: no two-offence cluster exists, so the three-offence series threshold files the same teams",
          all(len(c) >= 3 for c in two) and len(_pairs_only(offs)) == 0)
    rep = []
    for o in offs:
        rep.append(o)
    check("SF3: placing offences by reported date instead of occurred date files the same teams",
          grounds(A.golden_series(_by_reported(offs, rms), gt, cache=cache)[0], polys) == G)
    rec = all(_recorded_district(rms, o) == A.district_at(polys, o["x"], o["y"]) for c in gold_series for o in c)
    check("SF4: the recorded 2026 district, the boundaries and the station reference agree for every series offence",
          rec and all(stref[o["station"]] == A.district_at(polys, o["x"], o["y"]) for c in gold_series for o in c if o["station"]))
    only_phone = [o for o in offs if _prop(rms, o) in (None, "CELL PHONE")]
    check("SF5: reading 'a phone was taken' as phone-only property drops series offences (ruled out by OPS-41 section 2)",
          sum(len(c) for c in A.golden_series(only_phone, gt, cache=cache)[0]) < sum(len(c) for c in gold_series))
    nodup = A.phone_offences(rms, tpo, codes, A.W26, dedupe=False, fare_codes=fare)
    check("SF6: counting a report made to both systems twice leaves every series and count unchanged",
          grounds(A.golden_series(nodup, gt, cache=cache)[0], polys) == G)
    modal = all(len(t["districts"]) == 1 for t in A.team_table(gold_series, polys) if t["n"] < 40)
    check("SF7: the Eastline team's ground is every district of its series, four districts, not its busiest one",
          any(len(t["districts"]) == 4 for t in gold_tab) and modal)
    to_t = [dict(o) for o in offs]
    check("SF8: occurred_to equals occurred_from for every series offence, so either time files the same trips",
          all(_occ_to(rms, o) == o["t"] for c in gold_series for o in c if o["src"] == "RMS"))
    tolset = [grounds(A.golden_series(offs, gt, tol_min=t, cache=cache)[0], polys) for t in (2.0, 3.0, 4.0, 5.0)]
    check("SF9: trip windows of two to five minutes file the same teams", all(x == G for x in tolset))
    linkset = set()
    for dm in (500.0, 750.0, 1000.0, 1250.0, 1500.0):
        for dd in (21, 28, 42, 60):
            linkset.add(tuple(grounds(A.golden_series(offs, gt, dmax=dm, days=dd, cache=cache)[0], polys)))
    check("SF10: linkage radii of 500 m to 1.5 km and windows of 21 to 60 days file the same teams", linkset == {tuple(G)}, str(len(linkset)))
    inb = _one_direction(offs, gt, cache)
    check("SF11: matching on westbound trips only finds the same eighteen runs", inb == 18, str(inb))

    # ---- mess neutrality (R2), one per Layer 1 item ----------------------------------------------------------
    utc_as_local = _tpo_shift(rms, tpo, codes, fare)
    check("R2-utc: the transit log's UTC stamps read as local leave the teams unchanged",
          grounds(A.golden_series(utc_as_local, gt, cache=cache)[0], polys) == G)
    cur = A.phone_offences(rms, tpo, codes, A.W26, date_aware_codes=False, fare_codes=fare)
    check("R2-codes: transit station codes read on the current code list leave the teams unchanged",
          grounds(A.golden_series(cur, gt, cache=cache)[0], polys) == G)
    check("R2-dedupe: skipping the cross-system match leaves the teams unchanged (SF6)",
          grounds(A.golden_series(nodup, gt, cache=cache)[0], polys) == G)
    flat = A.GTFS(TARGET)
    flat.expand = False
    check("R2-frequencies: the feed read without expanding frequencies.txt leaves the teams unchanged",
          grounds(A.golden_series(offs, flat, cache={})[0], polys) == G)
    check("R2-layout: every 2026 series offence's recorded district matches the 2026 boundaries (SF4)", rec)
    check("R2-names: every RMS station location text resolves to a GTFS stop name",
          {A.rms_station(r["location_text"]) for r in rms if "LRT STN" in r["location_text"]} <= set(gt.station_of_stop.values()))
    check("R2-service-change: winter and spring timetables place the Eastline group's stops within 60 s of each other",
          _period_shift(w) <= 60, "%d s" % _period_shift(w))
    check("R2-crs: GeoJSON in EPSG:26912 and stops in WGS84 place every station in the same 2026 district",
          all(A.district_at(polys, N.STN[c]["x"], N.STN[c]["y"]) == stref[N.STN[c]["name"]] for c in N.STN))

    # ---- simultaneity and geometry -----------------------------------------------------------------------------
    sim = max((len(v) for v in res["simultaneous"].values()), default=0)
    check("P-simultaneous: Cobb Street offences fell within three minutes of Eastline group offences at Union Yards on three evenings",
          sim == 3, str(sim))
    check("P-train-time: no train joins Cobb Street and Union Yards in under eight minutes", _min_ride(w, "CB", "UY") >= 480)
    gs = [N.STN[c] for c in ("RV", "AR", "MB", "UY", "CB")]
    check("P-spacing: the five platform stations sit at least 1.5 km apart, so straight-line linkage cannot chain them",
          min(N.dist((a["x"], a["y"]), (b["x"], b["y"])) for i, a in enumerate(gs) for b in gs[i + 1:]) >= 1500)

    # ---- asks --------------------------------------------------------------------------------------------------
    crackA = A.ask_a(rms, tpo, codes, polys, stref, fare, date_aware=False)
    check("A1: ask 2 read on the current code list misses cells (the renumbering)", crackA != res["ask_a"])
    diffB = sum(1 for s in res["ask_b"] if A.ask_b(TARGET, codes, date_aware=False)[s] != res["ask_b"][s])
    check("A2: entries joined on gate codes alone miss at least six stations", diffB >= 6, str(diffB))
    flatC = A.ask_c(flat, cache={})
    check("A3: departures without the frequency templates miss every station", all(flatC[s] != res["ask_c"][s] for s in flatC))
    svc = A.ask_c(gt, by_service_date=True, cache=cache)
    check("A4: departures counted by service date instead of clock time differ (after-midnight trips)", svc != res["ask_c"])
    utcB = A.ask_b(TARGET, codes, local_window=False)
    check("A5: entries windowed on UTC dates differ from Mountain-time dates", utcB != res["ask_b"])
    for win in (12, 15, 30):
        check("A6-%d: matching referred reports within %d minutes files the same 2025 grid" % (win, win),
              _ask_a_window(rms, tpo, codes, polys, stref, fare, win) == res["ask_a"])
    check("A7: every station's entries and departures are distinct (no repeated block)",
          len(set(res["ask_b"].values())) == 9 and len(set(res["ask_c"].values())) == 9)

    # ---- input gates and realism -------------------------------------------------------------------------------
    files = [os.path.join(r, f) for r, _, fs in os.walk(TARGET) for f in fs]
    check("G-files: ten or more files", len(files) >= 10, str(len(files)))
    exts = {os.path.splitext(f)[1] for f in files}
    check("G-formats: three or more formats", len(exts) >= 3, str(sorted(exts)))
    check("G-rows: one file of 25,000 rows or more", len(rms) >= 25000, str(len(rms)))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("G-distractors: two or more distractors declared, none named as one",
          len(meta["distractor_files"]) >= 2 and not any("distract" in f.lower() for f in files))
    check("G-no-describing-file: no readme, dictionary, notes or manifest under target",
          not any(re.search(r"readme|dictionar|field_notes|manifest|notes\.", os.path.basename(f).lower()) for f in files))
    check("G-distractor-deletion: the analysis never opens the distractors",
          "secondhand" not in open(os.path.join(HERE, "analysis.py")).read() and "cpsd" not in open(os.path.join(HERE, "analysis.py")).read())
    occ = [int(r["occurrence_no"].split("-")[1]) for r in rms if r["occurrence_no"].startswith("CP26")]
    steps = {b - a for a, b in zip(occ, occ[1:])}
    check("Z-ids: occurrence numbers are not an arithmetic sequence", len(steps) > 2, str(sorted(steps)[:6]))
    tid = sorted(int(t) for t in gt.trips)
    check("Z-trip-ids: trip ids are not an arithmetic sequence", len({b - a for a, b in zip(tid, tid[1:])}) > 10)
    mx = max(A.parse_local(r["reported_local"]) for r in rms)
    check("Z-dates: no RMS record is reported after the 11 May 2026 pull", mx <= dt.datetime(2026, 5, 11, 6, 15), str(mx))
    tmax = max(A.utc_to_local(r["Logged (UTC)"]) for r in tpo)
    check("Z-dates-tpo: no transit log entry after its 11 May 2026 export", tmax <= dt.datetime(2026, 5, 11, 9, 40), str(tmax))
    people = set(P.PEOPLE.values())
    text_all = directive + note + A_pdf_text(os.path.join(TARGET, "cau_lrt_station_reference_2026.pdf"))
    check("Z-people: every named person in the documents is a drawn persona",
          all(n in people or n.split()[0] in ("E.",) for n in re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b(?= (?:at|,))", note)))
    gx = os.path.join(TASK, "golden", "series_assessment_2026.xlsx")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    check("Z-golden-xlsx: the golden workbook carries the figures.json team counts and grounds", _golden_matches(gx, figs))
    memo = A_docx_text(os.path.join(TASK, "golden", "summer_series_deployment_memo.docx"))
    check("Z-golden-memo: the memo states four teams and every ground",
          "four series teams" in memo and all(("District%s %s" % ("s" if len(t["districts"]) > 1 else "", t["districts"][0])) in memo for t in figs["teams"]))
    check("Z-mtimes: every target file carries the 15 May 2026 export time",
          all(abs(os.path.getmtime(f) - pack.FILE_TIME) < 1 for f in files))
    shutil.rmtree(tmp)

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail and not ok else ""))
    print("checks: %d, failed: %d" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


# ---- helpers ------------------------------------------------------------------------------------------------
def A_pdf_text(path):
    import zlib
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        raw = m.group(1)
        for dec in (_a85_flate, lambda b: zlib.decompress(b)):
            try:
                out.append(dec(raw).decode("latin-1"))
                break
            except Exception:
                continue
    txt = " ".join(re.findall(r"\((.*?)\)\s*Tj", " ".join(out)))
    return txt.replace("\\(", "(").replace("\\)", ")").replace("\\222", "'")


def _a85_flate(b):
    import base64
    import zlib
    s = b.strip()
    if s.startswith(b"<~"):
        s = s[2:]
    return zlib.decompress(base64.a85decode(s, adobe=False) if not s.endswith(b"~>") else base64.a85decode(s[:-2]))


def A_docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"<[^>]+>", " ", x.replace("</w:p>", "\n")).replace("  ", " ")


def _pairs_only(offs):
    pairs = []
    loc = A.local_series(offs)
    inside = {id(o) for c in loc for o in c}
    grp = [o for o in offs if o["sus"] >= 2 and o["x"] is not None and id(o) not in inside]
    for i, a in enumerate(grp):
        for b in grp[i + 1:]:
            if A.behaviour_match(a, b) and abs((a["t"] - b["t"]).days) <= 28 and ((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2) ** 0.5 <= 1000:
                pairs.append((a["id"], b["id"]))
    return pairs


def _by_reported(offs, rms):
    rep = {r["occurrence_no"]: A.parse_local(r["reported_local"]) for r in rms}
    out = []
    for o in offs:
        if o["src"] == "RMS" and not (A.W26[0] <= rep[o["id"]].date() <= A.W26[1]):
            continue
        out.append(o)
    return out


def _recorded_district(rms, o):
    for r in rms:
        if r["occurrence_no"] == o["id"]:
            return r["patrol_district"]
    return None


def _prop(rms, o):
    if o["src"] != "RMS":
        return None
    for r in rms:
        if r["occurrence_no"] == o["id"]:
            return r["property_taken"]
    return None


def _occ_to(rms, o):
    for r in rms:
        if r["occurrence_no"] == o["id"]:
            return A.parse_local(r["occurred_to_local"])
    return None


def _one_direction(offs, gt, cache):
    local = A.local_series(offs)
    plat = [o for c in local for o in c if o["loc"] == "LRT PLATFORM" and o["station"]]
    westbound = {tid for tid, tr in gt.trips.items() if tr["direction_id"] == "1"}
    cands = A.trip_candidates(gt, plat, 3.0, cache)
    cands = [{(d, t) for d, t in c if t.split("@")[0] in westbound} for c in cands]
    runs = set()
    for i in range(len(plat)):
        for j in range(i + 1, len(plat)):
            if plat[i]["station"] != plat[j]["station"] and cands[i] & cands[j]:
                runs.add(sorted(cands[i] & cands[j])[0])
    return len(runs)


def _tpo_shift(rms, tpo, codes, fare):
    shifted = []
    for r in tpo:
        r2 = dict(r)
        t = dt.datetime.strptime(r["Logged (UTC)"], "%Y-%m-%dT%H:%MZ")
        local_as_utc = A.utc_to_local(r["Logged (UTC)"])
        r2["Logged (UTC)"] = (t + (t - local_as_utc)).strftime("%Y-%m-%dT%H:%MZ")
        shifted.append(r2)
    return A.phone_offences(rms, shifted, codes, A.W26, fare_codes=fare)


def _period_shift(w):
    worst = 0
    for run in w.ev.g1_runs:
        tr = next(t for t in w.trips if t["trip_id"] == run["trip_id"])
        if tr["period"] != "S26":
            continue
        pg = dict((s, d) for s, a, d in tr["stops"])["PG"]
        alt = [t for t in w.trips if t["period"] == "W26" and t["daytype"] == tr["daytype"] and t["line"] == "EL"
               and t["direction"] == 1 and dict((s, d) for s, a, d in t["stops"]).get("PG") == pg]
        if not alt:
            return 10 ** 6
        a = dict((s, d) for s, aa, d in alt[0]["stops"])
        b = dict((s, d) for s, aa, d in tr["stops"])
        worst = max(worst, max(abs(a[c] - b[c]) for c in ("RV", "AR", "MB", "UY")))
    return worst


def _min_ride(w, a, b):
    best = 10 ** 6
    for t in w.trips:
        d = dict((s, dep) for s, arr, dep in t["stops"])
        ar = dict((s, arr) for s, arr, dep in t["stops"])
        if a in d and b in d:
            if d[a] < ar[b]:
                best = min(best, ar[b] - d[a])
            if d[b] < ar[a]:
                best = min(best, ar[a] - d[b])
    return best


def _ask_a_window(rms, tpo, codes, polys, stref, fare, win):
    old = A.phone_offences.__defaults__
    src = A.phone_offences
    import types
    code = src.__code__
    # re-run the match with a different window by patching the constant through a wrapper
    def patched(rms_, tpo_, codes_, window, dedupe=True, date_aware_codes=True, fare_codes=None):
        out = src(rms_, tpo_, codes_, window, dedupe=False, date_aware_codes=date_aware_codes, fare_codes=fare_codes)
        files = {o["id"] for o in out if o["src"] == "RMS"}
        keep = []
        rmsst = collections.defaultdict(list)
        for o in out:
            if o["src"] == "RMS" and o["station"]:
                rmsst[o["station"]].append(o)
        tpo_by_id = {r["TPO Log #"]: r for r in tpo_}
        for o in out:
            if o["src"] == "TPO":
                r = tpo_by_id[o["id"]]
                if r["CPS File #"] and r["CPS File #"] in files:
                    continue
                if r["Referred To Police"] == "Y" and not r["CPS File #"]:
                    if any(0 <= (o["t"] - x["t"]).total_seconds() <= win * 60 for x in rmsst.get(o["station"], [])):
                        continue
            keep.append(o)
        return keep
    A.phone_offences = patched
    try:
        return A.ask_a(rms, tpo, codes, polys, stref, fare)
    finally:
        A.phone_offences = src


def _golden_matches(path, figs):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    rows = list(wb["Series teams"].iter_rows(values_only=True))
    teams = [r for r in rows if r and isinstance(r[0], str) and r[0].startswith("Team ")]
    got = sorted((str(r[2]), int(r[3])) for r in teams)
    want = sorted((", ".join(t["districts"]), t["n"]) for t in figs["teams"])
    return got == want


if __name__ == "__main__":
    main()
