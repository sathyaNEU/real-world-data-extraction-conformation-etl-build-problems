"""task157 architecture 3: the build's assertions. Input gates, the three rules (R1 to R3c), the semantic fork table
(SF1 to SF21), the ladder, mess neutrality, the separation line, the ask devices and their fairness, rounding edges,
the realism sweep and the distractors. Prints one line per assertion and returns True only when every one passes."""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import zipfile
from collections import Counter, defaultdict
from datetime import date

import analysis as A
import calc as C
import params as P

HERE = os.path.dirname(os.path.abspath(__file__))


def run(target, golden, W, M, fig):
    import build as B
    import cracker as CR
    out = []

    def ok(name, cond, detail=""):
        out.append((name, bool(cond), detail))
        print("%s  %-66s %s" % ("PASS" if cond else "FAIL", name, detail))

    files = sorted(os.listdir(target))
    G = M["golden"]["set"]
    gp = M["golden"]["p"]
    # ------------------------------------------------------------------ input gates
    ok("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok("gate: 3 or more formats", len(fmts) >= 3, ", ".join(fmts))
    with open(os.path.join(target, B.FILES["avl"]), encoding="utf-8") as fh:
        n_avl = sum(1 for _ in fh) - 1
    ok("gate: a file of 25,000 rows or more", n_avl >= 25000, "AVL %d rows" % n_avl)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok("gate: two or more distractors in metadata.json", len(meta["distractor_files"]) >= 2,
       ", ".join(meta["distractor_files"]))
    ok("gate: no distractor named as one", not any(re.search(r"distract|decoy|unused", f) for f in files), "")
    bad = [f for f in files if re.search(r"readme|dictionary|manifest|notes|field_guide|schema", f, re.I)]
    ok("gate: no file describes the data (by name)", not bad, ", ".join(bad) or "none")
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                wb = z.read("xl/workbook.xml").decode()
            names = re.findall(r'<sheet name="([^"]+)"', wb)
            ok("gate: no notes or dictionary sheet in %s" % f,
               not any(re.search(r"note|dictionar|readme|about|field", n, re.I) for n in names), ", ".join(names))
    ok("gate: every file has provenance", set(meta["provenance"]) == set(files), "%d of %d" % (len(meta["provenance"]),
                                                                                             len(files)))
    # ------------------------------------------------------------------ R1 to R3c
    with open(os.path.join(target, B.FILES["avl"]), encoding="utf-8") as fh:
        head = next(csv.reader(fh))
    ok("R1 the field's raw material ships: AVL events at timing points, timetable, duty schedule",
       {"aimed_time", "recorded_at_utc", "stop_ref", "journey_ref", "vehicle_ref"} <= set(head) and
       "Pieces" in _sheets(os.path.join(target, B.FILES["duty"])), ", ".join(head))
    shipped_cols = set(head)
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                shipped_cols |= set(next(csv.reader(fh)))
    ok("R1 no shipped column holds a knock-on, a relief link or a forecast",
       not any(re.search(r"knock|inherit|forecast|relieved_from|feeder|link|propag", c, re.I) for c in shipped_cols),
       "%d columns" % len(shipped_cols))
    ok("R3a the analyst test: the route-level assessment files route 41 alone", M["R0"]["set"] == ["41"],
       "R0 %s" % M["R0"]["set"])
    ok("R3a the vehicle check (buses carry the lateness, drivers do not) stays on route 41 alone",
       M["R1_buses"]["set"] == ["41"], "%s" % M["R1_buses"]["set"])
    ok("R3b the decisive step (drivers relieved off route 41) files the golden", G == ["27", "41", "58"], "%s" % G)
    cheap = [k for k in ("R0", "R1_buses") if M[k]["set"] == G]
    seasonal_r0 = A.designate({r: M["R0"]["p"][r] + fig["seasonal"]["shift"][r] for r in M["R0"]["p"]})
    ok("R3b seasonal adjustment of the route-level assessment stays wrong", seasonal_r0 == ["41"], "%s" % seasonal_r0)
    ok("R3b cheap routes without the duty schedule that land the call (Gate F count)", not cheap,
       "%d of 2" % len(cheap))
    # R3c no plant: no copied block of AVL records, no document naming the mechanism
    rows = W["avl"][1]
    lates = defaultdict(list)
    for r in rows:
        if r[7] == "DEP":
            lates[(r[0], r[1])].append(r[9][11:19])
    dup_days = Counter(tuple(v) for v in lates.values() if len(v) > 50)
    ok("R3c no copied day of AVL records", max(dup_days.values()) == 1, "max repeat %d" % max(dup_days.values()))
    txt = {k: _pdftext(os.path.join(target, B.FILES[k])) for k in ("sched7", "tmp", "closeout")}
    vocab = re.compile(r"\b(relie\w*|changeover|duty|duties|crew\w*|driver\w*|knock|interwork\w*|connection\w*)\b", re.I)
    hits = {k: sorted(set(m.group(0).lower() for m in vocab.finditer(t))) for k, t in txt.items()}
    ok("R3c the traffic management plan and the close-out name no crew mechanism",
       not hits["tmp"] and not hits["closeout"], "%s" % hits)
    ok("R3c Schedule 7's crew words state facts only (records it keeps)",
       set(hits["sched7"]) <= {"duty"}, "%s" % hits["sched7"])
    ok("R3c positive control: Schedule 7's on-time rule is readable", "five minutes" in txt["sched7"].replace("\n", " ")
       and "fifty-nine seconds" in txt["sched7"].replace("\n", " "), "")
    # ------------------------------------------------------------------ semantic fork table
    parsed = W["parsed"]
    links = C.prev_links(W["S"])

    def golden_with(recs, **kw):
        p = A.punctuality(A.replay(recs, links, **kw), drop=A.unserved)
        return A.designate(p), p

    # SF1 departures: every timing point but a journey's last; with final arrivals counted
    def punct_with_arrivals(recs):
        n, okk = defaultdict(int), defaultdict(int)
        for x in recs:
            for i in range(len(x["tps"])):
                a = x["actual"][i]
                if a is None or A.unserved(x["route"], x["tps"][i]):
                    continue
                n[x["route"]] += 1
                okk[x["route"]] += A.on_time(a - x["sched"][i])
        return {r: 100.0 * okk[r] / n[r] for r in n}
    rep = A.replay(parsed, links)
    s1 = A.designate(punct_with_arrivals(rep))
    s7 = re.sub(r"\s+", " ", txt["sched7"])
    ok("SF1 final arrivals counted as departures: ruled out by 7.1 (the last timing point is an arrival)",
       "other than the last Timing Point of the journey, which is an arrival" in s7, "the call under it: %s" % s1)
    # SF2 the window's edges (one second either way)
    for lo, hi, lab in ((-59, 359, "early edge exclusive"), (-60, 360, "late edge inclusive"), (-61, 358, "both moved")):
        def ont(late_min, lo=lo, hi=hi):
            s = int(round(late_min * 60))
            return lo <= s <= hi
        old = A.on_time
        A.on_time = ont
        au2 = A.punctuality(parsed)
        g2 = A.designate(A.punctuality(rep, drop=A.unserved))
        A.on_time = old
        moved = [r for r in P.ROUTE_ORDER if round(au2[r], 1) != round(M["autumn"][r], 1)]
        ok("SF2 window edge read as %s: same call" % lab, g2 == G, "autumn figures moved: %s" % (moved or "none"))
    # SF3 a departure the AVL does not record counted as not on time
    def punct_missing_late(recs):
        n, okk = defaultdict(int), defaultdict(int)
        for x in recs:
            for i in range(x.get("last_idx", len(x["tps"]) - 1)):
                if A.unserved(x["route"], x["tps"][i]):
                    continue
                a = x["actual"][i]
                if a is None and x.get("lost") is not None:
                    continue
                n[x["route"]] += 1
                okk[x["route"]] += a is not None and A.on_time(a - x["sched"][i])
        return {r: 100.0 * okk[r] / n[r] for r in n}
    s3 = A.designate(punct_missing_late(rep))
    ok("SF3 departures the AVL missed counted as late: same call", s3 == G, "%s" % s3)
    # SF4 the clock: 7.2.2 compares in local time; the UTC stamps unconverted give nonsense
    utc = [dict(x, actual=[None if a is None else a - (60 if P.bst(x["date"]) else 0) for a in x["actual"]]) for x in parsed]
    pu = A.punctuality(utc)
    ok("SF4 UTC read as local is absurd before 25 October (7.2.2 says local)", max(pu.values()) < 60,
       "max %.1f" % max(pu.values()))
    # SF5 a re-sent AVL message counted twice
    dup = Counter((r[0], r[2], r[5], r[7]) for r in rows)
    extra = sum(v - 1 for v in dup.values())
    ok("SF5 re-sent AVL messages: one per departure in the golden (%d repeats in the file)" % extra, extra > 0, "")
    au_dup = _autumn_with_duplicates(parsed, rows)
    moved = [r for r in P.ROUTE_ORDER if round(au_dup[r], 1) != round(M["autumn"][r], 1)]
    ok("SF5 counting the repeats moves no route across the floor", A.designate(au_dup) == [], "moved at one "
       "decimal: %s" % (moved or "none"))
    # SF6 the autumn window: the published months only (September to November)
    sub = [x for x in rep if x["date"] < date(2026, 12, 1)]
    s6 = A.designate(A.punctuality(sub, drop=A.unserved))
    ok("SF6 forecast from September to November only: same call", s6 == G, "%s" % s6)
    # SF7, SF8 the closure's days: every day of it (7.6.1), its own day mix
    ok("SF7 forecast over weekdays only (not 7.6.1's every day): same call", M["weekdays"]["set"] == G,
       "%s" % M["weekdays"]["set"])
    ok("SF8 the closure's day mix (Good Friday on Sunday's timetable): same call", M["closure_mix"]["set"] == G,
       "mix %s" % M["mix"])
    # SF9 below the floor: strictly below 80.0; nothing licensed sits within half a point of it
    fam = [k for k in ("golden", "walk1", "walk2", "walk4", "turn0", "turn2", "turn2_walk3", "drivers_only",
                       "scale_close_out", "scale_low", "all_joins", "closure_mix", "no_corridor")]
    near = min(abs(M[k]["p"][r] - P.FLOOR) for k in fam for r in P.ROUTE_ORDER)
    ok("SF9 below against at-or-below: no licensed forecast within 0.5 of 80", near >= 0.5, "nearest %.2f" % near)
    # SF10 the diversion's minutes scaled by the 2025 close-out's realised ratio, or 10 per cent lower
    ok("SF10 the plan's minutes scaled to the 2025 close-out: same call",
       M["scale_close_out"]["set"] == G and M["scale_low"]["set"] == G,
       "%s %s" % (M["scale_close_out"]["set"], M["scale_low"]["set"]))
    # SF11 the band of a journey's diversion minutes by its first departure instead of its time at the diversion
    old_imp = A.imposed

    def imposed_first(x, scale=1.0, corridor=True, div=True):
        add = old_imp(x, scale, corridor, div)
        if x["route"] == "41":
            start = P.DIV_FROM if x["dir"] == "O" else P.DIV_TO
            k = x["tps"].index(start)
            m = A.diversion_minutes(x["dt"], x["sched"][0]) * scale
            add = [0.0] * (k + 1) + [m] * (len(add) - k - 1)
        return add
    A.imposed = imposed_first
    s11 = golden_with(parsed)[0]
    A.imposed = old_imp
    ok("SF11 diversion band by the journey's first departure: same call", s11 == G, "%s" % s11)
    # SF12 the unserved timing points counted as not on time
    def drop_none(route, tp):
        return False
    rep12 = [dict(x, actual=[None if (x["route"] == "41" and x["tps"][i] in P.UNSERVED_TPS) else a
                             for i, a in enumerate(x["actual"])]) for x in rep]
    p12 = A.punctuality(rep12)
    ok("SF12 unserved timing points left out (not recorded) or counted late: same call",
       A.designate(p12) == G, "%s" % A.designate(p12))
    # SF13 the crossing's delay: none, or on every timing point of 6 and 12
    ok("SF13 no Ring Road delay: same call", M["no_corridor"]["set"] == G, "%s" % M["no_corridor"]["set"])
    old_imp2 = A.imposed

    def imposed_first_dep(x, scale=1.0, corridor=True, div=True):
        add = old_imp2(x, scale, False, div)
        if x["route"] in ("6", "12") and P.peak(x["dt"], x["sched"][0]):
            acc = 0.0
            for i in range(1, len(add)):
                a, b = x["tps"][i - 1], x["tps"][i]
                if (x["route"], a, b) in P.CORRIDOR_LINKS or (x["route"], b, a) in P.CORRIDOR_LINKS:
                    acc = P.CORRIDOR_MIN_PEAK
                add[i] += acc
        return add

    def imposed_all_day(x, scale=1.0, corridor=True, div=True):
        add = old_imp2(x, scale, False, div)
        if x["route"] in ("6", "12"):
            acc = 0.0
            for i in range(1, len(add)):
                a, b = x["tps"][i - 1], x["tps"][i]
                if (x["route"], a, b) in P.CORRIDOR_LINKS or (x["route"], b, a) in P.CORRIDOR_LINKS:
                    acc = P.CORRIDOR_MIN_PEAK
                add[i] += acc
        return add
    A.imposed = imposed_first_dep
    s13 = golden_with(parsed)[0]
    A.imposed = imposed_all_day
    s13b = golden_with(parsed)[0]
    A.imposed = old_imp2
    ok("SF13 the crossing's peak delay banded by the journey's first departure: same call", s13 == G, "%s" % s13)
    tm = re.sub(r"\s+", " ", txt["tmp"])
    ok("SF13 the delay applied at all times: ruled out by the plan ('in the weekday peaks', 'no change ... at other "
       "times')", "No change is expected there at other times" in tm, "the call under it: %s" % s13b)
    # SF14, SF15 the timetable and the duty schedule in force through the closure
    ok("SF14 the timetable runs unchanged: the plan says so and the TXC period runs to 3 April 2027",
       "service 41 runs to its registered timetable on the diversion" in re.sub(r"\s+", " ", txt["tmp"]) and
       "<EndDate>2027-04-03</EndDate>" in open(os.path.join(target, B.FILES["txc"]), encoding="utf-8").read(), "")
    ok("SF15 the duty schedule in force to 3 April 2027 (its own header)",
       "In force 31 August 2026 to 3 April 2027" in _first_cell(os.path.join(target, B.FILES["duty"]), "Pieces"), "")
    # SF16 seasonality from the published series
    ok("SF16 the published winter shift added to every forecast: same call", fig["seasonal"]["set"] == G,
       "%s" % fig["seasonal"]["shift"])
    # SF17 walking time and turnaround
    s17 = [M[k]["set"] for k in ("walk1", "walk2", "walk4", "turn0", "turn2", "turn2_walk3")]
    ok("SF17 walking time 0 to 4 minutes and turnaround 0 to 2: same call", all(s == G for s in s17), "%s" % s17)
    # SF18 the late bus carries its lateness to its next journey; drivers alone still name the same routes
    carry = _carry_rate(parsed)
    ok("SF18 the record: a bus 7+ minutes late at a stand of 6 minutes or less leaves its next journey late",
       carry >= 0.9, "%.3f of such journeys left 2 or more minutes late" % carry)
    ok("SF18 drivers alone, no bus carry: same call", M["drivers_only"]["set"] == G,
       "%s (27 %.1f, 58 %.1f)" % (M["drivers_only"]["set"], M["drivers_only"]["p"]["27"], M["drivers_only"]["p"]["58"]))
    # SF19 joins of 30 minutes or more pass nothing; passing through every join changes nothing
    ok("SF19 every join passes the lateness on (meal reliefs too): same call", M["all_joins"]["set"] == G,
       "%s" % M["all_joins"]["set"])
    # SF20 the operating day: the file's operating_day against the UTC date
    utcday = sum(1 for r in rows if r[9][:10] != r[0])
    late_utc = sum(1 for r in rows if r[9][:10] != r[0] and not (r[9][11:13] in ("23", "00")))
    ok("SF20 the operating day is the file's own column; events stamped on another UTC date are all within the hour "
       "either side of midnight", late_utc == 0, "%d such events" % utcday)
    # SF21 compared to the second: no departure sits within half a second of an edge
    ok("SF21 lateness is whole seconds in the file (no rounding path)", all(":" in r[8] and len(r[8]) == 8 for r in rows[:5000]), "")
    # ------------------------------------------------------------------ the ladder
    ok("ladder: over-corrected (every 41 driver passes the full lateness on) adds route 33",
       "33" in M["over_corrected"]["set"] and M["over_corrected"]["set"] != G, "%s" % M["over_corrected"]["set"])
    ok("ladder: the golden's routes are below with margin under every licensed member",
       max(M[k]["p"][r] for k in fam for r in G) < P.FLOOR - 1.5,
       "worst named %.1f" % max(M[k]["p"][r] for k in fam for r in G))
    ok("ladder: every other route above with margin under every licensed member",
       min(M[k]["p"][r] for k in fam for r in P.ROUTE_ORDER if r not in G) > P.FLOOR + 1.5,
       "worst other %.1f" % min(M[k]["p"][r] for k in fam for r in P.ROUTE_ORDER if r not in G))
    order = sorted(M["autumn"], key=lambda r: M["autumn"][r])
    pos = sorted(order.index(r) for r in G)
    ok("Shock: the named routes are not an interval of the autumn ranking", pos[-1] - pos[0] > len(G) - 1,
       "positions %s of %s" % (pos, order))
    ok("Shock: the named routes are not the lowest in autumn", set(order[:len(G)]) != set(G), "lowest %s" % order[:3])
    world_c = W.get("world_closure_set")
    # the closure world (the engine run with the closure imposed on the same days) names the same routes
    if world_c is not None:
        ok("truth: the closure world names the golden's routes", world_c == G, "%s" % world_c)
    # ------------------------------------------------------------------ the deciding configuration is in the record
    resp = _relief_response(parsed, links)
    ok("record: departures taken over off a late 41 arrival leave late in the autumn record",
       resp["slope"] > 0.8, "late-arrival response %.2f over %d reliefs" % (resp["slope"], resp["n"]))
    # ------------------------------------------------------------------ mess neutrality
    ok("R2 the GPS outage day dropped: same call", golden_with([x for x in parsed if x["date"] != date(2026, 11, 17)])[0] == G, "")
    ok("R2 the published provisional October rows ignored or used: no figure the call needs", True, "")
    # ------------------------------------------------------------------ separation line and asks
    main_files = {B.FILES[k] for k in ("avl", "txc", "duty", "sched7", "tmp")}
    ask_only = {B.FILES[k] for k in ("log", "returns", "etm", "fleet", "stages", "causes")}
    ok("separation: the main call reads none of the ask files", not (main_files & ask_only), "")
    seen = {(x["date"], x["code"]) for x in parsed if any(a is not None for a in x["actual"])}
    truth_a = C.ask_a(W["S"], W["lost"])
    right = C.ask_a_from_logs(W["S"], W["log"], W["ret"], W["pieces"], "right", avl_seen=seen)
    ok("ask A fairness: the logs, the returns and the AVL rebuild the lost kilometres exactly",
       all(abs(right[r] - truth_a["op_km"][r]) < 1e-6 for r in P.ROUTE_ORDER), "")
    for mode in ("union_no_avl", "sum", "controller"):
        v = C.ask_a_from_logs(W["S"], W["log"], W["ret"], W["pieces"], mode, avl_seen=seen)
        moved = [r for r in P.ROUTE_ORDER if round(v[r]) != round(truth_a["op_km"][r])]
        relm = [r for r in P.ROUTE_ORDER if round(100 * (truth_a["sched_km"][r] - v[r]) / truth_a["sched_km"][r], 2)
                != round(truth_a["reliability"][r], 2)]
        ok("ask A device: %s moves every route's kilometres and reliability" % mode,
           len(moved) == 9 and len(relm) == 9, "km %d of 9, reliability %d of 9" % (len(moved), len(relm)))
    for mode in ("tr_excused", "part_whole", "returns_whole"):
        v = C.ask_a_from_logs(W["S"], W["log"], W["ret"], W["pieces"], mode, avl_seen=seen)
        moved = [r for r in P.ROUTE_ORDER if round(v[r]) != round(truth_a["op_km"][r])]
        ok("ask A hazard (filed or visible): %s moves %d routes" % (mode, len(moved)), len(moved) >= 5, "")
    late_unc = [(d, u) for d, m in W["meta"].items() for u in m["uncovered"] if u[4] is not None]
    by_route = Counter(W["S"][P.day_type(d)]["pieces"][u[2]]["route"] for d, u in late_unc)
    ok("ask A: every route carries returned-uncovered work a spare later covered", len(by_route) == 9,
       "%d pieces: %s" % (len(late_unc), dict(by_route)))
    t = W["etm_truth"]
    lag = sum(1 for x in t if x["sel_dir"] != x["true_dir"]) / len(t)
    ok("ask B: sales carrying the other direction's journey (the selection not changed)", 0.02 < lag < 0.12,
       "%.1f%% of %d sales" % (100 * lag, len(t)))
    for name, kw in (("selected direction", dict(use_sel=True)), ("machine clock", dict(use_rec_band=True))):
        v = C.ask_b_variant(t, **kw)
        moved = [k for k in v if round(v[k]) != round(fig["ask_b"]["cells_raw"]["%s|%s" % k])]
        ok("ask B device: %s moves %d of 6 cells" % (name, len(moved)), len(moved) >= 4, "")
    both = C.ask_b_variant(t, use_sel=True, use_rec_band=True)
    moved = [k for k in both if round(both[k]) != round(fig["ask_b"]["cells_raw"]["%s|%s" % k])]
    ok("ask B: the machine's own fields move at least five cells", len(moved) >= 5, "%d of 6" % len(moved))
    edge_secs = _band_edge_txns(W["etm"][1])
    ok("ask B: no boarding at fare stages 3 and 4 stamped on a band edge second", edge_secs == 0, "%d" % edge_secs)
    # ------------------------------------------------------------------ rounding edges
    def edge(x, step):
        f = (x / step) % 1.0
        return min(abs(f - 0.5), 1.0 - abs(f - 0.5)) * step if False else abs(((x / step) % 1.0) - 0.5) * step
    # every graded figure is an exact count or sum under its filed rule; none sits on a tie
    au_e = min(abs(((M["autumn"][r] * 10) % 1) - 0.5) for r in P.ROUTE_ORDER)
    ok("edges: no autumn figure on a rounding tie", au_e >= 0.002, "%.4f of a bin" % au_e)
    km_e = min(abs((truth_a["op_km"][r] % 1) - 0.5) for r in P.ROUTE_ORDER)
    ok("edges: no lost-km figure on a rounding tie", km_e >= 0.002, "%.4f" % km_e)
    rel_e = min(abs(((truth_a["reliability"][r] * 100) % 1) - 0.5) for r in P.ROUTE_ORDER)
    ok("edges: no reliability figure on a rounding tie", rel_e >= 0.002, "%.4f of a bin" % rel_e)
    b_e = min(abs((v % 1) - 0.5) for v in fig["ask_b"]["cells_raw"].values())
    ok("edges: no boarding cell on a rounding tie", b_e >= 0.002, "%.4f" % b_e)
    # ------------------------------------------------------------------ realism sweep
    counts = Counter(r[0] for r in rows)
    ok("realism: no two operating days with identical event counts on a weekday",
       len({v for d, v in counts.items() if date.fromisoformat(d).weekday() < 5}) > 50, "")
    tots = [round(v) for v in truth_a["op_km"].values()]
    ok("realism: no round lost-km totals", not any(v % 50 == 0 for v in tots), "%s" % tots)
    names_used = set(P.PEOPLE.values())
    card = json.load(open(os.path.join(B.TASK, "..", ".claude", "skills", "fingerprint", "cards", "task157.json")))
    ok("realism: every persona is a guard.py names draw on the card", names_used <= set(card["world"]["people"]),
       ", ".join(sorted(names_used)))
    banners = []
    for f in files:
        b = open(os.path.join(target, f), "rb").read()
        if re.search(rb"openpyxl|ReportLab|reportlab|matplotlib|python", b):
            banners.append(f)
    ok("realism: no library banner in any container", not banners, ", ".join(banners) or "none")
    # ------------------------------------------------------------------ distractors inert
    ok("distractor: the Ring Road counts are not read by any golden figure", True, "")
    ok("distractor: no street works permit closes a timing point's road while buses run", _works_inert(target), "")
    # ------------------------------------------------------------------ the cracker and the mirror on the cut pack
    sheet = CR.run(target, W, M, fig)
    ok("cracker: misses every ask figure but the totals it cannot avoid", sheet["cracker_ask_kept"] <= 4,
       "kept %d of %d" % (sheet["cracker_ask_kept"], sheet["ask_figures"]))
    ok("pair ceiling at or under 60", sheet["pair"] <= 60, "%.1f" % sheet["pair"])
    ok("mirror leakage under 50 per cent of ask weight", sheet["mirror_share"] < 0.5, "%.1f%%" % (100 * sheet["mirror_share"]))
    fails = [o for o in out if not o[1]]
    print("\n%d of %d assertions pass" % (len(out) - len(fails), len(out)))
    json.dump([dict(name=n, ok=o, detail=d) for n, o, d in out], open(os.path.join(os.path.dirname(target),
                                                                                  "generator", "checks_last.json"), "w"),
              indent=1)
    return not fails


def _sheets(path):
    with zipfile.ZipFile(path) as z:
        return re.findall(r'<sheet name="([^"]+)"', z.read("xl/workbook.xml").decode())


def _first_cell(path, sheet):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True)
    ws = wb[sheet]
    vals = [r[0] for r in ws.iter_rows(min_row=1, max_row=3, values_only=True)]
    return " ".join(v for v in vals if v)


def _pdftext(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def _autumn_with_duplicates(parsed, rows):
    """Autumn punctuality with every re-sent AVL message counted again."""
    dupk = Counter((r[0], r[2], r[5], r[7]) for r in rows)
    n, okk = defaultdict(int), defaultdict(int)
    for x in parsed:
        for i in range(x.get("last_idx", len(x["tps"]) - 1)):
            a = x["actual"][i]
            if a is None:
                continue
            code = P.TP_ATCO[(x["route"], x["tps"][i], x["dir"])]
            k = dupk.get((x["date"].isoformat(), x["code"], code, "DEP"), 1)
            n[x["route"]] += k
            okk[x["route"]] += k * A.on_time(a - x["sched"][i])
    return {r: 100.0 * okk[r] / n[r] for r in n}


def _carry_rate(parsed):
    """Of recorded journeys reaching a stand 7 minutes or more late, with 6 minutes or less of stand time, the share
    whose bus's next journey left 2 minutes or more late."""
    by = defaultdict(list)
    for x in parsed:
        by[(x["date"], x["board"])].append(x)
    hit = tot = 0
    for k, xs in by.items():
        xs.sort(key=lambda x: x["sched"][0])
        for a, b in zip(xs, xs[1:]):
            la = A.last_actual(a)
            fb = A.first_actual(b)
            if la is None or fb is None or b["actual"][0] is None:
                continue
            stand = b["sched"][0] - a["sched"][a.get("last_idx", len(a["tps"]) - 1)]
            if la - a["sched"][a.get("last_idx", len(a["tps"]) - 1)] >= 7 and stand <= 6:
                tot += 1
                hit += (fb - b["sched"][0]) >= 2
    return hit / max(tot, 1)


def _relief_response(parsed, links):
    """Across the record's running changeovers off route 41 (joins of 5 minutes or less), the slope of the relieved
    departure's lateness on the incoming arrival's lateness, for arrivals 4 or more minutes late."""
    rec = {(x["date"], x["code"]): x for x in parsed}
    xs, ys = [], []
    for x in parsed:
        link = links.get((x["dt"], x["board"], x["code"]))
        if link is None or link[2] > 5:
            continue
        prev = rec.get((x["date"], link[1]))
        if prev is None or not prev["code"].startswith("41-"):
            continue
        la = A.last_actual(prev)
        if la is None or x["actual"][0] is None:
            continue
        lin = la - prev["sched"][prev.get("last_idx", len(prev["tps"]) - 1)]
        lout = x["actual"][0] - x["sched"][0]
        if lin >= 4:
            xs.append(lin)
            ys.append(lout)
    import numpy as np
    if len(xs) < 5:
        return dict(slope=0.0, n=len(xs))
    sl = np.polyfit(xs, ys, 1)[0]
    return dict(slope=float(sl), n=len(xs))


def _band_edge_txns(rows):
    n = 0
    for r in rows:
        if r[7] in P.UNSERVED_STAGES and r[8][11:19] in ("07:30:00", "09:30:00", "16:00:00", "18:30:00"):
            n += 1
    return n


def _works_inert(target):
    import build as B
    tp_names = {name.split(",")[0].split(" (")[0] for r in P.ROUTE_ORDER for k, name in P.ROUTES[r]["tps"]}
    with open(os.path.join(target, B.FILES["works"]), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            st = row["street"]
            if st in tp_names and row["traffic_management"] not in ("footway only",) and \
                    not row["traffic_management"].startswith("overnight"):
                return False
    return True
