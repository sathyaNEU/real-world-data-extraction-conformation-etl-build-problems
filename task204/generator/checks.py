"""Generator checks for task204 v2: the three-rules block (R1 to R3c), the cheap-route count (F), every SF row of the
design note, mess neutrality per Layer 1 item (R2), the ladder (L), the asks (A), each graded figure's distance to its
bin edge (B), the input gates (G) and the realism sweep (Z). Exit 1 on any failure."""
import base64
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
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ROOT = os.path.dirname(TASK)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import pack             # noqa: E402
import params as P      # noqa: E402
import world_net as N   # noqa: E402

RESULTS = []
MO = {"SNATCH": "SNATCH", "STREET": "STREET-CONFRONT", "STREET-WEAPON": "STREET-WEAPON", "PICKPOCKET": "STEALTH"}


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), str(detail)))


def grounds(series, polys):
    return sorted((tuple(t["districts"]), t["n"]) for t in A.team_table(series, polys))


def teams_only(series, polys):
    return sorted(tuple(t["districts"]) for t in A.team_table(series, polys))


class GTFSVariant(A.GTFS):
    """The feed read with one calendar convention changed."""

    def __init__(self, target, mode):
        super().__init__(target)
        self.mode = mode

    def runs_on(self, service_id, d):
        c = self.cal[service_id]
        wd = c[["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][d.weekday()]] == "1"
        ds = d.strftime("%Y%m%d")
        if self.mode == "no_ranges":          # both timetables on every date
            ex = self.cdates.get(service_id, {}).get(ds)
            return {"1": True, "2": False}.get(ex, wd)
        if self.mode == "no_exceptions":      # holiday swaps ignored
            return wd and c["start_date"] <= ds <= c["end_date"]
        if self.mode == "spring_only":        # the feed's current timetable for every date
            return wd and service_id.startswith("26SPR")
        return super().runs_on(service_id, d)


def main():
    res = A.run_all(TARGET)
    offs, gt, cache, polys = res["_offs"], res["_gtfs"], res["_cache"], res["_polys26"]
    rms, tpo, codes, stref, fare = res["_rms"], res["_tpo"], res["_codes"], res["_stref"], res["_fare_codes"]
    R = {r["occurrence_no"]: r for r in rms}
    gold_series, gold_runs = A.golden_series(offs, gt, cache=cache)
    G = grounds(gold_series, polys)
    gold_tab = res["golden"]
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ---- world truth -----------------------------------------------------------------------------------------
    w = pack.make_world()
    tmp = tempfile.mkdtemp(prefix="t204chk_")
    pack.write_pack(w, os.path.join(tmp, "target"))
    idx = w.rms_index
    truth = collections.defaultdict(set)
    for e in w.ev.events:
        if e["group"] and id(e) in idx and P.W26[0] <= e["t_occ"].date() <= P.W26[1]:
            truth[e["group"]].add(idx[id(e)])
    check("L-golden-truth: the golden series are exactly the four offender groups the world built",
          sorted(sorted(t["ids"]) for t in gold_tab) == sorted(sorted(v) for v in truth.values()),
          [len(t["ids"]) for t in gold_tab])
    clean = []
    for e in w.ev.events:
        if P.W26[0] <= e["t_event"].date() <= P.W26[1]:
            clean.append({"src": "W", "id": str(id(e)), "t": e["t_event"],
                          "station": N.STN[e["station"]]["name"] if e["station"] else None, "x": e["x"], "y": e["y"],
                          "mo": MO[e["mo"]], "sus": e["suspects"], "alo": e["age_low"], "ahi": e["age_high"],
                          "loc": e["loc"], "offence": e["offence"]})

    # ---- ladder ------------------------------------------------------------------------------------------------
    nr = [len(res["rung0"]), len(res["rung1"]), len(res["rung2"]), len(gold_tab)]
    check("L-rung0: the field's linkage (method, description, 1 km, 28 days) files seven series teams", nr[0] == 7, nr[0])
    check("L-rung1: one team per patrol district holding a series files six teams", nr[1] == 6, nr[1])
    check("L-rung2: linking every same-line platform series files three teams", nr[2] == 3, nr[2])
    merged = max(res["rung2"], key=lambda t: t["n"])
    check("L-rung2-merge: the corridor merge folds Cobb Street into the four Eastline group stations",
          set(merged["stations"]) == {"Cobb Street", "Ridgeview", "Ashford Road", "Millbrook", "Union Yards"}, merged["stations"])
    check("L-golden: four teams on districts 4/6/7/9, 5, 8 and 6",
          sorted(tuple(t["districts"]) for t in gold_tab) == sorted([("D4", "D6", "D7", "D9"), ("D5",), ("D8",), ("D6",)]),
          [t["districts"] for t in gold_tab])
    check("L-separation: no rung files the golden's team set",
          all(sorted(tuple(t["districts"]) for t in res[k]) != sorted(tuple(t["districts"]) for t in gold_tab)
              for k in ("rung0", "rung1", "rung2")))
    check("L-walk: the corrections walk 7, 6, 3 and only the decisive step turns back to 4", nr == [7, 6, 3, 4], nr)
    check("L-runs: eighteen train trips each carry two or three Eastline group offences", len(gold_runs) == 18, len(gold_runs))
    check("L-counts: the four series hold 42, 18, 16 and 14 offences",
          sorted(t["n"] for t in gold_tab) == [14, 16, 18, 42], sorted(t["n"] for t in gold_tab))
    r0f = {len(A.local_series(offs, dm, dd)) for dm in (400.0, 1000.0, 2000.0) for dd in (14, 28, 90)}
    r2f = {len(A.corridor_series(offs, dd, dm)) for dm in (400.0, 1000.0, 2000.0) for dd in (14, 28, 90)}
    check("L-rung-family: rung 0 files seven and rung 2 three across radii of 400 m to 2 km and windows of 14 to 90 days",
          r0f == {7} and r2f == {3}, (r0f, r2f))

    # ---- the three rules ------------------------------------------------------------------------------------------
    r0c = A.local_series(clean)
    check("R3a: on the clean truth the default path (the field's linkage) files seven teams, not four", len(r0c) == 7, len(r0c))
    gc, _ = A.golden_series(clean, gt, cache=cache)
    check("R3b: on the clean truth the default path plus the trip step alone files the golden's four teams",
          teams_only(gc, polys) == teams_only(gold_series, polys), teams_only(gc, polys))
    r2c = A.corridor_series(clean)
    check("R3b-lower: on the clean truth the corridor correction alone stays wrong (three teams)", len(r2c) == 3, len(r2c))
    cols = set()
    for root, _, files in os.walk(TARGET):
        for f in files:
            if f.endswith((".csv", ".txt")):
                with open(os.path.join(root, f), encoding="utf-8") as fh:
                    cols.update(c.lower() for c in next(csv.reader(fh)))
    check("R1: offence-level records ship with time, place, method and description; no column holds a series, group or trip of an offence",
          not any(re.search(r"series|group|crew|gang|run_id|linked", c) for c in cols)
          and {"occurred_from_local", "x_utm12n", "mo_code", "num_suspects"} <= cols)
    check("R1-raw: the trip step reads the published timetable's stop times (raw material, nothing precomputed)",
          sum(len(v) for v in gt.st.values()) > 4000 and "trip_id" not in R[next(iter(R))])
    directive = pdf_text(os.path.join(TARGET, "ops41_series_crime_response_directive.pdf"))
    check("R3c-control: the directive's text decodes (positive control)",
          "three or more offences committed by the same offender group" in directive)
    check("R3c: no filed sentence names a train, trip, timetable, travel or link between offences",
          not re.search(r"\b(trains?|trips?|timetables?|schedul\w*|rid(e|es|ing)|link\w*|travel\w*|journey)\b", directive.lower()))
    note = docx_text(os.path.join(TARGET, "summer_deployment_planning_note.docx"))
    check("R3c-note: the planning note carries no team count, ground or group (no voice ranking the candidates)",
          not re.search(r"\b(teams? (?:for|on|in)|four|seven|three|six|Eastline group|crew|gang)\b", note) and "OPS-41" in note)
    check("R3c-no-plant: every series offence is an ordinary RMS record (open, single occurrence, coordinates on file)",
          all(R[i]["clearance_status"] == "OPEN" and R[i]["x_utm12n"] for t in gold_tab for i in t["ids"]))

    # ---- Gate F: cheap routes on the clean truth -------------------------------------------------------------------
    cheap, landed = 0, 0
    for dm in (250.0, 500.0, 1000.0, 1500.0, 2000.0, 3000.0, 5000.0, 10 ** 6):
        for dd in (14, 28, 60, 90):
            cheap += 1
            landed += int(teams_only(A.local_series(clean, dmax=dm, days=dd), polys) == teams_only(gold_series, polys))
    for dd in (14, 28, 60):
        cheap += 1
        landed += int(teams_only(A.corridor_series(clean, days=dd), polys) == teams_only(gold_series, polys))
    check("F-cheap: none of %d distance, time and corridor linkages on the clean truth files the golden's teams" % cheap,
          landed == 0, landed)

    # ---- semantic forks (design note SF rows) -----------------------------------------------------------------------
    alt = A.local_series([dict(o, sus=max(o["sus"], 2)) for o in offs])
    check("SF1: reading lone offenders into offender groups changes the series (OPS-41 section 3 rules it out)",
          grounds(alt, polys) != grounds(A.local_series(offs), polys), len(alt))
    po = pairs_outside(offs)
    in_east = {i for t in gold_tab if len(t["districts"]) > 1 for i in t["ids"]}
    check("SF2: reading a series as two or more offences files the same teams (the one locally linked pair is inside the Eastline group)",
          grounds(A.golden_series(offs, gt, cache=cache, min_n=2)[0], polys) == G and all(o in in_east for p_ in po for o in p_), po)
    rep = by_reported(rms, tpo, codes, fare)
    check("SF3: windowing by reported date instead of occurred date files the same teams and counts",
          grounds(A.golden_series(rep, gt, cache=cache)[0], polys) == G)
    rec_ok = all(R[o["id"]]["patrol_district"] == A.district_at(polys, o["x"], o["y"]) for c in gold_series for o in c)
    st_ok = all(stref[o["station"]] == A.district_at(polys, o["x"], o["y"]) for c in gold_series for o in c if o["station"])
    check("SF4: recorded district, 2026 boundaries and station reference agree for every series offence", rec_ok and st_ok)
    only = [o for o in offs if o["src"] != "RMS" or R[o["id"]]["property_taken"] == "CELL PHONE"]
    check("SF5: reading 'a phone was taken' as phone-only property loses series offences (OPS-41 section 2 rules it out)",
          grounds(A.golden_series(only, gt, cache=cache)[0], polys) != G)
    nodup = A.phone_offences(rms, tpo, codes, A.W26, dedupe=False, fare_codes=fare)
    check("SF6: counting a report made to both systems twice leaves every team and count unchanged",
          grounds(A.golden_series(nodup, gt, cache=cache)[0], polys) == G)
    east = [t for t in gold_tab if len(t["districts"]) > 1]
    per = collections.Counter(A.district_at(polys, o["x"], o["y"]) for c in gold_series for o in c if len(c) == max(map(len, gold_series)))
    check("SF7: the Eastline team's ground is all four districts of its series (section 4), each holding six or more offences",
          len(east) == 1 and len(east[0]["districts"]) == 4 and min(per.values()) >= 6, dict(per))
    check("SF8: occurred_to equals occurred_from on every series offence, so either time files the same trips",
          all(R[i]["occurred_to_local"] == R[i]["occurred_from_local"] for t in gold_tab for i in t["ids"]))
    tolset = [grounds(A.golden_series(offs, gt, tol_min=t, cache=cache)[0], polys) for t in (1.5, 2.0, 3.0, 4.0, 5.0)]
    check("SF9: trip windows of 1.5 to 5 minutes file the same teams and counts", all(x == G for x in tolset))
    linkset = set()
    mo_only = lambda a, b: a["mo"] == b["mo"] and bool(a["mo"])
    for dm in (400.0, 500.0, 750.0, 1000.0, 1250.0, 1500.0, 2000.0):
        for dd in (14, 21, 28, 42, 60, 90):
            for m in (None, mo_only):
                linkset.add(tuple(grounds(A.golden_series(offs, gt, dmax=dm, days=dd, cache=cache, match=m)[0], polys)))
    check("SF10: linkage radii of 400 m to 2 km, windows of 14 to 90 days, with or without the description, plus the trip step, file the same teams",
          linkset == {tuple(G)}, len(linkset))
    od = one_direction(offs, gt, cache)
    check("SF11: matching westbound trips only finds the same eighteen trips", od == 18, od)
    c26 = collections.Counter(A.district_at(polys, o["x"], o["y"]) if o["src"] == "RMS" else stref.get(o["station"]) for o in offs)
    rose = all(c26[d] > sum(res["ask_a"][d]) for t in gold_tab for d in t["districts"])
    check("SF12: every district on a team's ground rose against the same weeks of 2025, so 'behind the spring rise' files the same teams", rose)
    check("SF13: no series offence is cleared, so the section 6 stand-down never applies", all(
        R[i]["clearance_status"] == "OPEN" for t in gold_tab for i in t["ids"]))
    check("SF14: the review period from the directive (twelve completed weeks before 4 May) is the prompt's 9 Feb to 3 May",
          (dt.date(2026, 5, 4) - dt.timedelta(days=84), dt.date(2026, 5, 3)) == A.W26)
    tpo_only = [o for o in offs if o["src"] == "TPO"]
    check("SF15: every transit-only report has one suspect, so placing it by station or leaving it out files the same teams",
          all(o["sus"] <= 1 for o in tpo_only) and grounds(A.golden_series([o for o in offs if o["src"] == "RMS"], gt, cache=cache)[0], polys) == G)
    others = [r for r in rms if r["offence_code"] not in ("ROB-PERS", "THFT-PERS") and "CELL PHONE" in r["property_taken"]]
    check("SF16: no other offence code carries a phone in a described group record (scope by code is inert)",
          all(not (r["num_suspects"] and int(r["num_suspects"]) >= 2 and r["mo_code"]) for r in others), len(others))
    check("SF17: every offender group holds exactly one series, so a team per group equals a team per series",
          len(gold_tab) == len(truth))

    # ---- mess neutrality (R2), one per Layer 1 item ----------------------------------------------------------------
    shifted = utc_as_local(rms, tpo, codes, fare)
    check("R2-utc: the transit log's UTC stamps read as local time leave the teams unchanged",
          grounds(A.golden_series(shifted, gt, cache=cache)[0], polys) == G)
    cur = A.phone_offences(rms, tpo, codes, A.W26, date_aware_codes=False, fare_codes=fare)
    check("R2-codes: transit station codes read on the current code list leave the teams unchanged",
          grounds(A.golden_series(cur, gt, cache=cache)[0], polys) == G)
    check("R2-dedupe: skipping the cross-system match leaves the teams unchanged (SF6)",
          grounds(A.golden_series(nodup, gt, cache=cache)[0], polys) == G)
    flat = A.GTFS(TARGET)
    flat.expand = False
    check("R2-frequencies: the feed read without expanding frequencies.txt leaves the teams unchanged",
          grounds(A.golden_series(offs, flat, cache={})[0], polys) == G)
    for mode in ("no_ranges", "no_exceptions", "spring_only"):
        gv = GTFSVariant(TARGET, mode)
        check("R2-calendar-%s: the feed read with that calendar convention leaves the teams unchanged" % mode,
              grounds(A.golden_series(offs, gv, cache={})[0], polys) == G)
    check("R2-layout: every 2026 series offence's recorded district matches the 2026 boundaries (SF4)", rec_ok)
    names_rms = {A.rms_station(r["location_text"]) for r in rms if "LRT STN" in r["location_text"]}
    check("R2-names: every RMS station location text resolves to a GTFS stop name",
          None not in names_rms and names_rms <= set(gt.station_of_stop.values()), sorted(n for n in names_rms if n))
    check("R2-crs: stops in WGS84 and districts in EPSG:26912 put every station in its reference district",
          all(A.district_at(polys, *latlon_to_utm(float(s["stop_lat"]), float(s["stop_lon"]))) == stref[gt.station_of_stop[sid]]
              for sid, s in gt.stops.items()))
    edge = min(edge_distance(polys, o["x"], o["y"]) for c in gold_series for o in c)
    check("R2-edges: every series offence sits 60 m or more inside its 2026 district", edge >= 60, round(edge))

    # ---- simultaneity and geometry ----------------------------------------------------------------------------------
    sim = max((len(v) for v in res["simultaneous"].values()), default=0)
    check("P-simultaneous: on four evenings a Cobb Street offence fell within three minutes of an Eastline group offence at Union Yards",
          sim == 4, sim)
    mr = min_ride(w, "CB", "UY")
    check("P-train-time: no scheduled train joins Cobb Street and Union Yards in under six minutes", mr >= 360, mr)
    gs = [N.STN[c] for c in ("RV", "AR", "MB", "UY", "CB")]
    sp = min(N.dist((a["x"], a["y"]), (b["x"], b["y"])) for i, a in enumerate(gs) for b in gs[i + 1:])
    check("P-spacing: the five platform stations sit 1.5 km or more apart, so 1 km linkage cannot chain them", sp >= 1500, round(sp))

    # ---- asks ---------------------------------------------------------------------------------------------------------
    crackA = A.ask_a(rms, tpo, codes, polys, stref, fare, date_aware=False)
    dA = sum(1 for d in A.DISTRICTS for k in range(3) if crackA[d][k] != res["ask_a"][d][k])
    check("A1: 2025 transit codes read on the current code list miss eight or more of the thirty cells", dA >= 8, dA)
    rep_win = reported_grid(rms, tpo, codes, polys, stref, fare)
    dW = sum(1 for d in A.DISTRICTS for k in range(3) if rep_win[d][k] != res["ask_a"][d][k])
    check("A1b: windowing 2025 by reported date moves %d cells; the note's 'took place in the same weeks' files the occurrence date" % dW,
          "took place in the same weeks of last year, 10 February to 4 May 2025" in " ".join(note.split()) and dW <= 4, dW)
    recA = A.ask_a(rms, tpo, codes, polys, stref, fare, redistrict=False)
    dR = sum(1 for d in A.DISTRICTS for k in range(3) if recA[d][k] != res["ask_a"][d][k])
    check("A2: 2025 offences left in their recorded (2025 layout) districts miss six or more cells", dR >= 6, dR)
    bB = A.ask_b(TARGET, codes, date_aware=False)
    dB = sum(1 for s in res["ask_b"] if bB[s] != res["ask_b"][s])
    check("A3: entries joined on gate codes alone miss six or more stations", dB >= 6, dB)
    uB = A.ask_b(TARGET, codes, local_window=False)
    check("A4: entries windowed on UTC dates miss every station", all(uB[s] != res["ask_b"][s] for s in uB))
    fC = A.ask_c(flat, cache={})
    check("A5: calls without the frequency templates miss every station", all(fC[s] != res["ask_c"][s] for s in fC))
    nC = A.ask_c(GTFSVariant(TARGET, "no_exceptions"), cache={})
    check("A6: calls with the holiday service swaps ignored miss every station", all(nC[s] != res["ask_c"][s] for s in nC))
    sC = A.ask_c(gt, by_service_date=True, cache=cache)
    check("A7: calls counted by service date or by clock time agree (no service runs past midnight into a window edge)",
          sC == res["ask_c"])
    for win in (15, 20, 30, 45, 60):
        check("A8-%d: matching referred reports without a file number within %d minutes files the same 2025 grid" % (win, win),
              A.ask_a(rms, tpo, codes, polys, stref, fare, ref_window_min=win) == res["ask_a"])
    same = lambda a, b: res["ask_c"][a] == res["ask_c"][b]
    check("A9: entries differ at every station; calls differ except between stations every one of whose trains serves the other",
          len(set(res["ask_b"].values())) == 9 and len(set(res["ask_c"].values())) == 6
          and same("Westgate", "Centre Square") and same("Millbrook", "Cobb Street") and same("Ridgeview", "Prairie Gate"))
    check("A10: no 2025 cell is zero and no district repeats another's row (no constant block)",
          min(min(v) for v in res["ask_a"].values()) > 0 and len({tuple(v) for v in res["ask_a"].values()}) == 10)

    # ---- distance to bin edge for every graded figure ------------------------------------------------------------
    variants = [grounds(A.golden_series(offs, gt, tol_min=t, dmax=dm, days=dd, cache=cache)[0], polys)
                for t in (1.5, 3.0, 5.0) for dm in (400.0, 1000.0, 2000.0) for dd in (14, 28, 90)]
    variants += [grounds(A.golden_series(nodup, gt, cache=cache)[0], polys), grounds(A.golden_series(rep, gt, cache=cache)[0], polys),
                 grounds(A.golden_series(offs, flat, cache={})[0], polys)]
    check("B-main: the team count, every ground and every series count are exact under all %d licensed variants "
          "(margin 0.5 of a whole-number bin)" % len(variants), all(v == G for v in variants))
    gridset = {json.dumps(A.ask_a(rms, tpo, codes, polys, stref, fare, ref_window_min=wn), sort_keys=True) for wn in (15, 20, 30, 45, 60)}
    check("B-ask2: all thirty 2025 cells are exact under every licensed matching window (margin 0.5)", len(gridset) == 1)
    check("B-ask3: entries and calls are exact under every licensed clock reading (margin 0.5)",
          sC == res["ask_c"] and A.ask_b(TARGET, codes) == res["ask_b"])

    # ---- input gates ------------------------------------------------------------------------------------------------
    files = [os.path.join(r, f) for r, _, fs in os.walk(TARGET) for f in fs]
    check("G-files: ten or more files", len(files) >= 10, len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    check("G-formats: three or more formats", len(exts) >= 3, sorted(exts))
    check("G-rows: one file of 25,000 rows or more", len(rms) >= 25000, len(rms))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("G-distractors: two or more distractors declared, none named as one",
          len(meta["distractor_files"]) >= 2 and not any("distract" in f.lower() for f in files))
    check("G-provenance: every shipped file has source, date and licence in metadata.json",
          {os.path.relpath(f, TARGET) for f in files} == set(meta["files"]) and all(
              v["source"] and v["date"] and v["license"] for v in meta["files"].values()))
    check("G-no-describing-file: no readme, dictionary, notes or manifest under target",
          not any(re.search(r"readme|dictionar|field_notes|manifest|schema|codebook", os.path.basename(f).lower()) for f in files))
    asrc = open(os.path.join(HERE, "analysis.py")).read()
    check("G-distractor-deletion: the analysis never opens a distractor", all(
        os.path.basename(d).split(".")[0] not in asrc for d in meta["distractor_files"]))

    # ---- realism sweep ------------------------------------------------------------------------------------------------
    occ = [int(r["occurrence_no"].split("-")[1]) for r in rms if r["occurrence_no"].startswith("CP26")]
    steps = {b - a for a, b in zip(occ, occ[1:])}
    check("Z-ids: occurrence numbers are not an arithmetic sequence", len(steps) > 2, sorted(steps)[:6])
    tid = sorted(int(t) for t in gt.trips)
    check("Z-trip-ids: trip ids are not an arithmetic sequence", len({b - a for a, b in zip(tid, tid[1:])}) > 10)
    mx = max(A.parse_local(r["reported_local"]) for r in rms)
    check("Z-dates-rms: no RMS record reported after the 11 May 2026 pull", mx <= dt.datetime(2026, 5, 11, 6, 15), mx)
    tmax = max(A.utc_to_local(r["Logged (UTC)"]) for r in tpo)
    check("Z-dates-tpo: no transit log entry after its 11 May 2026 export", tmax <= dt.datetime(2026, 5, 11, 23, 59), tmax)
    fg_early = [r for r in rms if r["location_text"].startswith("FAIRGROUNDS") and A.parse_local(r["occurred_from_local"]).date() < P.SPRING_CHANGE]
    fg_codes = {g[2] for g in P.GATES["FG"]}
    tpo_early = [r for r in tpo if A.utc_to_local(r["Logged (UTC)"]).date() < P.SPRING_CHANGE and not r["Station Code"]]
    check("Z-opening: nothing is recorded at Fairgrounds before it opened on 29 March 2026, and every transit report carries a station code",
          not fg_early and not tpo_early and all(r["Station Code"] for r in tpo), (len(fg_early), len(tpo_early)))
    check("Z-note-dates: the planning note (4 May) names the extract pull as still to come",
          "11 May" in note and "pulled this morning" not in note)
    card = json.load(open(os.path.join(ROOT, ".claude", "skills", "fingerprint", "cards", "task204.json")))
    people = set(P.PEOPLE.values())
    card_people = set(card.get("world", {}).get("people", []))
    check("Z-people: the personas in the documents are exactly the card's drawn names",
          people == card_people, sorted(people ^ card_people))
    docs_text = directive + " " + note + " " + pdf_text(os.path.join(TARGET, "cau_lrt_station_reference_2026.pdf"))
    named = set(re.findall(r"\b(?:Superintendent|Deputy Chief \(Operations\)|Sergeant|Inspector) ([A-Z][a-z]+ [A-Z][a-z]+)", docs_text))
    check("Z-named: every titled person in the documents is a persona", named <= people, sorted(named - people))
    blk = collections.Counter(r["location_text"] for r in rms if "BLK" in r["location_text"])
    check("Z-free-text: no street block address recurs beyond a real rate (top block under 0.5 per cent of rows)",
          blk.most_common(1)[0][1] < 0.005 * len(rms), blk.most_common(1)[0])
    daily = collections.Counter(A.parse_local(r["occurred_from_local"]).date() for r in rms)
    check("Z-volume: daily occurrence counts vary (no constant stream)", len(set(daily.values())) > 20)
    gx = os.path.join(TASK, "golden", "series_assessment_2026.xlsx")
    check("Z-golden-xlsx: the golden workbook carries the figures.json teams, grounds and counts", golden_matches(gx, figs))
    memo = docx_text(os.path.join(TASK, "golden", "summer_series_deployment_memo.docx"))
    dtext = lambda ds: ("District %s" % ds[0]) if len(ds) == 1 else ("Districts %s and %s" % (", ".join(ds[:-1]), ds[-1]))
    check("Z-golden-memo: the memo states four teams, every ground and the evenings Cobb Street and Union Yards coincided",
          "four series teams" in memo and all(dtext(t["districts"]) in memo for t in figs["teams"])
          and ("on %s evenings" % {3: "three", 4: "four", 5: "five"}[figs["simultaneous_evenings"]]) in memo)
    check("Z-mtimes: every target file carries the 15 May 2026 export time",
          all(abs(os.path.getmtime(f) - pack.FILE_TIME) < 1 for f in files))
    gfiles = [os.path.join(TASK, "golden", g) for g in sorted(os.listdir(os.path.join(TASK, "golden")))]
    for f in files + gfiles:
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(f) as z:
                bad = [n for n in z.namelist() if re.search(r"comments|people\.xml|vbaProject|revisions", n)]
                core = z.read("docProps/core.xml").decode("utf-8") if "docProps/core.xml" in z.namelist() else ""
                core += z.read("docProps/app.xml").decode("utf-8") if "docProps/app.xml" in z.namelist() else ""
            check("Z-container-%s: no comments, tracked people or macros; no tool signature in core properties" % os.path.basename(f),
                  not bad and not re.search(r"openpyxl|python-docx|python", core.lower()), bad)
    # H25 and H13: every PDF opens alike in a strict reader, a lenient one and pdftotext; dates distinct and in order
    import logging
    import subprocess
    import warnings
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    import pypdf
    stamps = []
    for f in sorted(x for x in files if x.endswith(".pdf")):
        with warnings.catch_warnings(record=True) as wr:
            warnings.simplefilter("always")
            ts = " ".join(pg.extract_text() for pg in pypdf.PdfReader(f, strict=True).pages)
            tl = " ".join(pg.extract_text() for pg in pypdf.PdfReader(f, strict=False).pages)
            meta_ = pypdf.PdfReader(f).metadata
        pt = subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True) if shutil.which("pdftotext") else None
        ok_pt = pt is None or (pt.returncode == 0 and "Error" not in pt.stderr and len(pt.stdout.split()) > 40)
        stamps.append(meta_.get("/CreationDate"))
        check("Z-readers-%s: strict and lenient readers agree, no parser warning, pdftotext reads it" % os.path.basename(f),
              ts == tl and not wr and ok_pt and meta_.get("/CreationDate") == meta_.get("/ModDate"), (len(wr), ok_pt))
    check("Z-pdf-dates: every PDF carries its own creation date", len(set(stamps)) == len(stamps), stamps)
    for f in files + gfiles:
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(f) as z:
                core = z.read("docProps/core.xml").decode("utf-8")
            c_ = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
            m_ = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
            check("Z-office-dates-%s: created on or before modified, inside 2025-06 to 2026-05-15" % os.path.basename(f),
                  c_ <= m_ and "2025-06-01" <= c_[:10] <= "2026-05-15", (c_, m_))
    shutil.rmtree(tmp)

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail and not ok else ""))
    print("checks: %d, failed: %d" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


# ---- helpers ----------------------------------------------------------------------------------------------------
def pdf_text(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        txt = None
        if raw.endswith(b"~>"):
            body = raw[2:] if raw.startswith(b"<~") else raw
            try:
                txt = zlib.decompress(base64.a85decode(body[:-2])).decode("latin-1")
            except Exception:
                txt = None
        if txt is None:
            try:
                txt = zlib.decompress(raw).decode("latin-1")
            except Exception:
                continue
        out.append(txt)
    body = " ".join(out)
    parts = re.findall(r"\((.*?)(?<!\\)\)\s*Tj", body)
    s = " ".join(parts)
    return re.sub(r"\\([()\\])", r"\1", s).replace("\\222", "'")


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    x = x.replace("</w:p>", "\n").replace("<w:br/>", "\n")
    return re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", "", x))


def pairs_outside(offs):
    loc = A.local_series(offs)
    inside = {id(o) for c in loc for o in c}
    grp = [o for o in offs if o["sus"] >= 2 and o["x"] is not None and id(o) not in inside]
    pairs = []
    for i, a in enumerate(grp):
        for b in grp[i + 1:]:
            if A.behaviour_match(a, b) and abs((a["t"] - b["t"]).total_seconds()) <= 28 * 86400 \
                    and ((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2) ** 0.5 <= 1000:
                pairs.append((a["id"], b["id"]))
    return pairs


def by_reported(rms, tpo, codes, fare):
    wide = (A.W26[0] - dt.timedelta(days=14), A.W26[1] + dt.timedelta(days=14))
    offs = A.phone_offences(rms, tpo, codes, wide, fare_codes=fare)
    rep = {r["occurrence_no"]: A.parse_local(r["reported_local"]).date() for r in rms}
    return [o for o in offs if A.W26[0] <= (rep[o["id"]] if o["src"] == "RMS" else o["t"].date()) <= A.W26[1]]


def reported_grid(rms, tpo, codes, polys, stref, fare):
    """The 2025 grid with RMS offences placed by reported date (occurrence times kept for the cross-system match)."""
    wide = (A.W25[0] - dt.timedelta(days=3), A.W25[1] + dt.timedelta(days=3))
    offs = A.phone_offences(rms, tpo, codes, wide, fare_codes=fare)
    rep = {r["occurrence_no"]: A.parse_local(r["reported_local"]).date() for r in rms}
    grid = {d: [0, 0, 0] for d in A.DISTRICTS}
    for o in offs:
        day = rep[o["id"]] if o["src"] == "RMS" else o["t"].date()
        dist = A.district_at(polys, o["x"], o["y"]) if o["src"] == "RMS" else stref.get(o["station"])
        for k, (a, b) in enumerate(A.PERIODS25):
            if a <= day <= b and dist in grid:
                grid[dist][k] += 1
    return grid


def one_direction(offs, gt, cache):
    plat = [o for o in offs if o["sus"] >= 2 and o["x"] is not None and o["loc"] == "LRT PLATFORM" and o["station"]]
    west = {tid for tid, tr in gt.trips.items() if tr["direction_id"] == "1" and tr["route_id"] == "201"}
    cands = [{(d, t) for d, t in c if t.split("@")[0] in west} for c in A.trip_candidates(gt, plat, 3.0, cache)]
    runs = set()
    for i in range(len(plat)):
        for j in range(i + 1, len(plat)):
            if plat[i]["station"] != plat[j]["station"] and A.behaviour_match(plat[i], plat[j]) and cands[i] & cands[j]:
                runs.add(sorted(cands[i] & cands[j])[0])
    return len(runs)


def utc_as_local(rms, tpo, codes, fare):
    out = []
    for r in tpo:
        r2 = dict(r)
        t = dt.datetime.strptime(r["Logged (UTC)"], "%Y-%m-%dT%H:%MZ")
        loc = A.utc_to_local(r["Logged (UTC)"])
        r2["Logged (UTC)"] = (t + (t - loc)).strftime("%Y-%m-%dT%H:%MZ")
        out.append(r2)
    return A.phone_offences(rms, out, codes, A.W26, fare_codes=fare)


def latlon_to_utm(lat, lon):
    """Forward transverse Mercator for UTM zone 12N (GRS80), written out for the check."""
    import math
    a, f = 6378137.0, 1 / 298.257222101
    e2 = f * (2 - f)
    k0, lon0 = 0.9996, math.radians(-111.0)
    ph, la = math.radians(lat), math.radians(lon)
    n_ = a / math.sqrt(1 - e2 * math.sin(ph) ** 2)
    t_ = math.tan(ph) ** 2
    ep2 = e2 / (1 - e2)
    c_ = ep2 * math.cos(ph) ** 2
    a_ = math.cos(ph) * (la - lon0)
    m_ = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * ph - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * math.sin(2 * ph)
              + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * ph) - (35 * e2 ** 3 / 3072) * math.sin(6 * ph))
    x = k0 * n_ * (a_ + (1 - t_ + c_) * a_ ** 3 / 6 + (5 - 18 * t_ + t_ ** 2 + 72 * c_ - 58 * ep2) * a_ ** 5 / 120) + 500000.0
    y = k0 * (m_ + n_ * math.tan(ph) * (a_ ** 2 / 2 + (5 - t_ + 9 * c_ + 4 * c_ ** 2) * a_ ** 4 / 24
                                       + (61 - 58 * t_ + t_ ** 2 + 600 * c_ - 330 * ep2) * a_ ** 6 / 720))
    return x, y


def edge_distance(polys, x, y):
    best = 10 ** 9
    for _, ring in polys:
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            dx, dy = x2 - x1, y2 - y1
            L = dx * dx + dy * dy
            u = 0 if L == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L))
            best = min(best, ((x - x1 - u * dx) ** 2 + (y - y1 - u * dy) ** 2) ** 0.5)
    return best


def min_ride(w, a, b):
    best = 10 ** 6
    for t in w.trips:
        dep = {s: d for s, arr, d in t["stops"]}
        arr = {s: ar for s, ar, d in t["stops"]}
        if a in dep and b in dep:
            if dep[a] < arr[b]:
                best = min(best, arr[b] - dep[a])
            if dep[b] < arr[a]:
                best = min(best, arr[a] - dep[b])
    return best


def golden_matches(path, figs):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    rows = list(wb["Series teams"].iter_rows(values_only=True))
    teams = [r for r in rows if r and isinstance(r[0], str) and r[0].startswith("Team ")]
    got = sorted((str(r[2]), int(r[3])) for r in teams)
    want = sorted((", ".join(t["districts"]), t["n"]) for t in figs["teams"])
    n = [r for r in rows if r and r[0] == "Series teams required"]
    return got == want and bool(n) and n[0][1] == figs["n_teams"]


if __name__ == "__main__":
    main()
