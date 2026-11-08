"""Generator assertions on the clean truth: the three rules (R1, R2, R3), every semantic fork (SF), the ladder,
the bins, the record's identities, the asks' devices, the input gates, the distractors and the realism sweep."""
import datetime as dt
import itertools
import os
import re
import statistics
import zipfile
from collections import defaultdict

import params as P
import world as Wd
import asks as A
import pack as K

HM = P.HM
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def edge(v, u=100):
    return u / 2 - abs(v - round(v / u) * u)


def r100(v):
    return int(round(v / 100.0) * 100)


# ---------------------------------------------------------------------------------------------------------
# An independent replay with every licensed reading as a switch
# ---------------------------------------------------------------------------------------------------------

def replay_v(trains, rec, census, team, follow="full", hours="booked", overrun="late_only", net=False,
             booked=None, seqs=None, keep=None, share=P.TEAM_SHARE, ident="exact"):
    seqs = seqs if seqs is not None else Wd.unit_days(trains, rec)
    total = 0.0
    for seq in seqs:
        prev_arr = prev_cf = None
        prev_direct = False
        for idx in seq:
            tr = trains[idx]
            r = rec[idx]
            barr, bdep = booked[idx] if booked else (tr["barr"], tr["bdep"])
            dep = r["dep"][0]
            bound = prev_arr is not None and r["dep"][0] > bdep[0] and (
                r["dep"][0] == prev_arr + P.MIN_TURN if ident == "exact" else
                r["dep"][0] <= prev_arr + P.MIN_TURN + 1 if ident == "near" else
                True if ident == "gap" else
                prev_arr + P.MIN_TURN > bdep[0])
            if bound and (follow == "full" or (follow == "hop1" and prev_direct)):
                held = (r["dep"][0] - prev_arr) if ident == "gap" else P.MIN_TURN
                dep = max(bdep[0], prev_cf + held)
            direct = False
            a = None
            n = len(tr["stops"])
            for i in range(1, n):
                a = dep + (r["arr"][i] - r["dep"][i - 1])
                late = a - barr[i]
                if (keep is None or keep(tr)) and (late > 0 or net):
                    total += census[idx][1][i] * late
                if i < n - 1:
                    if overrun == "always" or r["dep"][i] > bdep[i]:
                        bd = bdep[i] - barr[i]
                        o = r["dep"][i] - r["arr"][i] - bd
                        t_h = r["dep"][i] if hours == "actual" else bdep[i]
                        in_h = (P.TEAM_FROM <= t_h <= P.TEAM_TO) if hours == "inclusive" else Wd.in_team_hours(t_h)
                        if team is not None and tr["line"] == team[0] and tr["stops"][i] == team[1] \
                                and in_h and o > 0:
                            o *= (1.0 - share)
                            direct = True
                        dep = max(bdep[i], a + bd + o)
                    else:
                        dep = bdep[i]
            prev_arr = r["arr"][-1]
            prev_cf = a
            prev_direct = direct
    return total / HM


def savings_v(W, days=None, per_day=False, **kw):
    trains, census, records = W["trains"], W["census"], W["records"]
    days = days if days is not None else W["days"]
    out = {c: [] for c in P.SHORTLIST}
    for d in days:
        rec = records[d]
        b = replay_v(trains, rec, census, None, **kw)
        for c, team in P.SHORTLIST.items():
            out[c].append(b - replay_v(trains, rec, census, team, **kw))
    if per_day:
        return out
    return {c: sum(v) / len(v) for c, v in out.items()}


def call_of(s):
    o = sorted(s, key=lambda c: -s[c])
    return o[0], o[1], s[o[0]] / s[o[1]]


# ---------------------------------------------------------------------------------------------------------

def main(W, fig, target):
    RESULTS.clear()
    trains, census, days, records = W["trains"], W["census"], W["days"], W["records"]
    R = fig["rungs"]
    C = list(P.SHORTLIST)
    win = lambda r: max(C, key=lambda c: R[c][r])
    order = lambda r: sorted(C, key=lambda c: -R[c][r])
    marg = lambda r: R[order(r)[0]][r] / R[order(r)[1]][r]
    gold = {c: R[c]["R2"] for c in C}
    pick, ru = fig["pick"], fig["runner_up"]
    brief = _docx_text(os.path.join(target, K.FILES["brief"]))
    brief_flat = re.sub(r"\s+", " ", brief)

    # ---------------- R1: the field's raw material ships, the deciding quantity does not --------------
    hdr = open(os.path.join(target, K.FILES["running"])).readline().strip()
    check("R1 the running record ships every call with its unit, at the call grain",
          hdr == "date,headcode,unit,tiploc,arr,dep", hdr)
    n_run = sum(1 for _ in open(os.path.join(target, K.FILES["running"]))) - 1
    check("R1 the record holds every call of every train on every weekday",
          n_run == len(days) * sum(len(t["stops"]) for t in trains), str(n_run))
    heads = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads.append(open(os.path.join(target, f)).readline())
    check("R1 no shipped column holds a saving, knock-on, reactionary or turnround figure",
          not any(re.search(r"saving|knock|reaction|propagat|turnround|lateness", h, re.I) for h in heads))
    perf = _xlsx_cells(os.path.join(target, K.FILES["perf"]))
    check("R1 the performance summary is by line and month, never by station",
          not any(s in perf for s in C))
    check("R1 no shipped document states a figure in passenger-minutes for a station",
          not re.search(r"\d[\d,]*\s*passenger-minutes", brief_flat))

    # ---------------- R2: every Layer 1 mess item is real and neutral ------------------------------------
    hc = [t["headcode"] for t in trains]
    check("R2 the census keys a train by headcode and origin time, the record by headcode and unit: the headcode "
          "alone joins them, unique on every weekday", len(set(hc)) == len(hc))
    check("R2 the record's unit swaps (a spare unit on a failure day) give the planned diagrams' figure",
          all(abs(R[c]["R2plan"] - R[c]["R2"]) < 1e-6 for c in C))
    dis = {x[0] for x in P.DISRUPTIONS} | {x[0] for x in P.UNIT_FAILURES}
    s = savings_v(W, days=[d for d in days if d not in dis])
    check("R2 the disrupted and unit-failure weekdays dropped leaves the call",
          call_of(s)[0] == pick and call_of(s)[1] == ru, "%s %.1f over %s %.1f" % (call_of(s)[0], s[pick], ru, s[ru]))
    clocks = {r["arr"][k] % 1 for d in days[:3] for r in records[d].values() for k in range(1, len(r["arr"]))}
    check("R2 the record's clock strings sit on the half-minute the train describer logs", clocks == {0})
    check("R2 the spare units appear only on the failure days",
          {d for d in days for r in records[d].values() if r["unit"] in P.SPARES} == {x[0] for x in P.UNIT_FAILURES})

    # ---------------- R3: the analyst test, the decisive step alone, no plant ---------------------------
    check("R3a the same-train route (every filed rule applied) files Saltgate, not the pick",
          win("R1") == "Saltgate" and pick == "Pellingham", "%s / %s" % (win("R1"), pick))
    check("R3a train-minutes and on-board passenger-minutes file Saltgate",
          win("R0b") == "Saltgate" and win("R0") == "Saltgate")
    check("R3a every reactionary scaling of the same-train figure files Saltgate",
          all(win(r) == "Saltgate" for r in ["RNF", "RLF", "RPF"]))
    check("R3b the same-train route with only the unit-following step added files Pellingham",
          win("R2") == "Pellingham" and win("R2a") == "Pellingham")
    check("R3c no repeated block of running rows across days",
          len({tuple(tuple(records[d][i]["arr"][1:]) for i in sorted(records[d])) for d in days}) == len(days))
    check("R3c no two trains carry identical census rows",
          len({(tuple(census[t["id"]][0]), tuple(census[t["id"]][1])) for t in trains}) == len(trains))
    check("R3c no memo, draft or stakeholder figure ships: the brief states no figure for a station",
          not re.search(r"(Ostley|Brathwick|Ambrey|Pellingham|Holcroft|Saltgate)[^.]{0,60}\d{3,}", brief_flat))

    # ---------------- ladder ----------------------------------------------------------------------------
    for r in ["R0b", "R0", "R1", "RNF", "RLF", "RPF"]:
        check("ladder %s margin at least 1.15, winner Saltgate" % r, marg(r) >= 1.15 and win(r) == "Saltgate",
              "%.3f" % marg(r))
        check("ladder %s the winner clears Pellingham by 1.20" % r, R[win(r)][r] / R["Pellingham"][r] >= 1.20,
              "%.3f" % (R[win(r)][r] / R["Pellingham"][r]))
    check("ladder Pellingham third or lower on train-minutes and on-board passenger-minutes",
          order("R0b").index("Pellingham") >= 2 and order("R0").index("Pellingham") >= 2)
    check("ladder golden margin at least 1.25", marg("R2") >= 1.25, "%.3f" % marg("R2"))
    check("ladder runner-up Saltgate on the golden", ru == "Saltgate")
    check("ladder dominance: Pellingham's knock-on exceeds Saltgate's same-train lead over it by 1.2",
          (R["Pellingham"]["R2"] - R["Pellingham"]["R1"]) >= 1.2 * (R["Saltgate"]["R1"] - R["Pellingham"]["R1"]),
          "%.0f vs %.0f" % (R["Pellingham"]["R2"] - R["Pellingham"]["R1"], R["Saltgate"]["R1"] - R["Pellingham"]["R1"]))

    # ---------------- semantic forks ------------------------------------------------------------------
    check("SF1 passenger lateness at each passenger's alighting station is filed; the train-minutes reading files "
          "another station", "each passenger's minutes after the booked arrival at the station where they leave the "
          "train" in brief_flat and win("R0b") != pick)
    s_net = savings_v(W, net=True)
    check("SF2 early arrivals count none: the brief files it, so the netted reading (which files %s) is ruled out"
          % call_of(s_net)[0], "with none for an early or on-time arrival" in brief_flat,
          "%s over %s %.3f" % call_of(s_net))
    run_dates = sorted({ln.split(",", 1)[0] for ln in open(os.path.join(target, K.FILES["running"])).readlines()[1:]})
    check("SF3 the record's weekdays are the filed window: 60, Monday 7 September to Friday 27 November 2026",
          len(run_dates) == 60 and run_dates[0] == "2026-09-07" and run_dates[-1] == "2026-11-27"
          and all(dt.date.fromisoformat(x).weekday() < 5 for x in run_dates)
          and "Monday 7 September to Friday 27 November 2026" in brief_flat)
    t_bounds = [(c, tr["headcode"]) for c, (ln, st) in P.SHORTLIST.items() for tr in trains
                if tr["line"] == ln and st in tr["stops"][1:-1]
                and tr["bdep"][tr["stops"].index(st)] in (P.TEAM_FROM, P.TEAM_TO)]
    s_act = savings_v(W, hours="actual")
    s_inc = savings_v(W, hours="inclusive")
    check("SF4 the team's hours read by actual departure, or with 19:30 included, give the same call and the same bin "
          "at every station", call_of(s_act)[0] == pick and call_of(s_inc)[0] == pick
          and all(r100(s_act[c]) == r100(gold[c]) and r100(s_inc[c]) == r100(gold[c]) for c in C),
          "calls booked on an end: %s; %s %.1f; %s %.1f" % (t_bounds[:3], call_of(s_act)[0], s_act[pick],
                                                             call_of(s_inc)[0], s_inc[pick]))
    s_def = savings_v(W)
    s_alw = savings_v(W, overrun="always")
    check("SF5 the overrun read on every call (an early arrival's wait included) gives the same replay",
          all(abs(s_alw[c] - s_def[c]) < 1e-9 for c in C) and all(abs(s_def[c] - gold[c]) < 0.051 for c in C))
    check("SF6 the planned diagrams and the record's units give the same figure at every station",
          all(abs(R[c]["R2plan"] - R[c]["R2"]) < 1e-6 for c in C))
    check("SF7 one hop and every hop give the same bin at every station",
          all(r100(R[c]["R2a"]) == r100(R[c]["R2"]) for c in C))
    n_census = sum(1 for _ in open(os.path.join(target, K.FILES["census"]))) - 1
    check("SF8 one census day's counts serve every weekday: one row per call, no per-day counts ship",
          n_census == sum(len(t["stops"]) for t in trains) and "passenger census on Tuesday 13 October 2026" in brief_flat)
    check("SF9 the gap from unrounded figures and from rounded figures is one bin",
          r100(fig["gap_raw"]) == fig["pick_saving"] - fig["runner_up_saving"])
    rules = _xlsx_cells(os.path.join(target, K.FILES["wtt"]))
    check("SF10 the four-minute turnround floor is the record's own: every late start at a terminus sits exactly "
          "four minutes after its unit's arrival or follows a turnround with slack, and no filed rule states it",
          _turnround_identity(W) and not re.search(r"turnround|turnaround|turn-round", rules + brief_flat, re.I))
    gaps = _late_start_gaps(W)
    check("SF10 every late start of a unit's later working sits exactly four minutes after the unit's arrival (at least "
          "100 of them); the only other late starts are units' first workings, late off the depot",
          len(gaps) >= 100 and all(g == P.MIN_TURN for g in gaps), "%d late later workings, gaps %s" %
          (len(gaps), sorted(set(gaps))[:5]))
    s_gap = savings_v(W, ident="gap")
    check("SF17 how a unit passes its lateness on: pulling every late later working forward by its own recorded gap "
          "after the unit's arrival gives the identical replay to holding it four minutes after the replayed arrival",
          all(abs(s_gap[c] - gold[c]) < 0.051 for c in C), str({c: round(s_gap[c], 1) for c in C}))
    s_x = savings_v(W, keep=lambda tr: tr["kind"] == "all")
    check("SF11 the park-and-ride extras are weekday passenger trains; leaving them out gives the same call",
          call_of(s_x)[0] == pick and any(t["kind"] == "extra" and census[t["id"]][0].sum() > 0 for t in trains),
          "%s over %s %.3f" % call_of(s_x))
    check("SF12 the 2027 timetable keeps the autumn 2026 train plan, filed in the brief",
          "keeps the autumn 2026 train plan on all three lines" in brief_flat)
    pdays = savings_v(W, per_day=True)
    med = {c: statistics.median(v) for c, v in pdays.items()}
    check("SF13 averaged per weekday (filed); the median weekday gives the same call",
          "averaged per weekday" in brief_flat and call_of(med)[0] == pick, "%s over %s %.3f" % call_of(med))
    short = re.search(r"November 2026: (.+?)\.", brief_flat).group(1)
    names = [x.strip() for x in re.split(r",| and ", short) if x.strip()]
    check("SF14 the shortlist is the brief's six stations", names == C, str(names))
    # the cross product of every same-call reading
    bad = []
    for fol, hrs, ovr, ext, idn in itertools.product(["full", "hop1"], ["booked", "actual"], ["late_only", "always"],
                                                     [None, lambda tr: tr["kind"] == "all"],
                                                     ["exact", "near", "capacity", "gap"]):
        s = savings_v(W, follow=fol, hours=hrs, overrun=ovr, keep=ext, ident=idn)
        if call_of(s)[0] != pick or call_of(s)[1] != ru or (ext is None and r100(s[pick]) != r100(gold[pick])):
            bad.append((fol, hrs, ovr, ext is not None, idn, call_of(s)[:2], round(s[pick], 1)))
    check("SF15 the cross product of SF4, SF5, SF7, SF11 and four ways to pick out a turnround-bound start (64 "
          "cells) files one pick and one runner-up, and the pick's bin wherever the extras are in",
          not bad, str(bad[:3]))

    perf_tab = _perf_rows(os.path.join(target, K.FILES["perf"]))
    mine = _line_month_punctuality(W)
    check("back-test: the performance summary's punctuality by line and month ties to the running record every route "
          "reads, and carries no passenger figure", all(perf_tab[k] == mine[k] for k in mine) and len(perf_tab) == 9
          and "passenger" not in _xlsx_cells(os.path.join(target, K.FILES["perf"])).lower(),
          str([(k, perf_tab.get(k), v) for k, v in mine.items() if perf_tab.get(k) != v][:3]))

    # ---------------- bins -------------------------------------------------------------------------------
    for c in C:
        check("bin %s mid-bin (at least 15 from a rounding line)" % c, edge(gold[c]) >= 15, "%.1f" % edge(gold[c]))
    check("bin gap mid-bin", edge(fig["gap_raw"]) >= 15, "%.1f" % edge(fig["gap_raw"]))

    # ---------------- asks: gatelines --------------------------------------------------------------------
    rows, truth = A.gate_readings(W)
    naive = _gate_naive(rows)
    for st in P.GATED:
        for f in ("entered", "left"):
            check("gates %s %s: the battery route (UTC to BST, wraps added, a restart's jump dropped, each counter "
                  "read as named) misses" % (st, f), naive[st][f] != truth[st][f],
                  "%d vs %d" % (naive[st][f], truth[st][f]))
    check("gates census alighters as gate exits miss every station",
          all(_census_offs(W, st) != truth[st]["left"] for st in P.GATED))
    check("gates the census day sits before the clock change (readings are UTC, the day is BST)",
          P.CENSUS_DAY < P.CLOCK_CHANGE)
    # ---------------- asks: Delay Repay ------------------------------------------------------------------
    claims, rtruth = A.delay_repay(W)
    inscope = [c for c in claims if c["decision"] == "APPROVED" and not c.get("outside") and c["central"]]
    paid_band = defaultdict(float)
    for c in inscope:
        pb = "60 or more" if c["band_paid"] in ("60 to 119", "120 or more") else c["band_paid"]
        paid_band[(c["line"], pb)] += c["amount"]
    moved = sum(1 for k in rtruth if round(paid_band[k]) != round(rtruth[k]))
    check("repay banding by band_paid misses at least six of nine cells", moved >= 6, "%d of 9" % moved)
    nodup = defaultdict(float)
    seen = set()
    for c in inscope:
        if c["claim_ref"] not in seen:
            seen.add(c["claim_ref"])
            nodup[(c["line"], A.ask_band(c["true_late"]))] += c["amount"]
    moved2 = sum(1 for k in rtruth if round(nodup[k]) != round(rtruth[k]))
    check("repay keeping one row per claim reference (dropping the appeal top-ups) misses cells", moved2 >= 3,
          "%d of 9" % moved2)
    direct_only = _repay_direct_only(W, claims)
    moved3 = sum(1 for k in rtruth if round(direct_only[k]) != round(rtruth[k]))
    check("repay matching the claimed direction only (return legs unmatched) misses cells", moved3 >= 3,
          "%d of 9" % moved3)
    careful = defaultdict(float)
    for c in inscope:
        if c["journey_date"] == c["true_date"]:
            careful[(c["line"], A.ask_band(c["true_late"]))] += c["amount"]
    moved4 = sum(1 for k in rtruth if round(careful[k]) != round(rtruth[k]))
    check("repay the careful route (every paid row, return legs reversed, each claim on its stated date) misses at "
          "least six cells", moved4 >= 6, "%d of 9" % moved4)
    dflt = [c for c in inscope if c["journey_date"] != c["true_date"]]
    late_days = defaultdict(list)
    for d in days:
        for t in trains:
            r = records[d][t["id"]]
            for k in range(1, len(t["stops"])):
                if r["arr"][k] - t["barr"][k] >= 15 * HM:
                    late_days[(t["id"], k)].append(d)
    idx = _dep_index(W)
    crs = {v: k for k, v in P.CRS.items()}
    uniq = True
    for c in dflt:
        o, d_ = crs[c["origin"]], crs[c["destination"]]
        m = int(c["booked_dep"] // HM)
        tk = [(t, k) for t, k in idx[(o, m)] if d_ in [Wd.station_name(t, q) for q in range(k + 1, len(t["stops"]))]]
        t, k = tk[0]
        kd = [Wd.station_name(t, q) for q in range(len(t["stops"]))].index(d_)
        ld = late_days[(t["id"], kd)]
        first = min(x["submitted"] for x in inscope if x["claim_ref"] == c["claim_ref"])
        uniq &= (first.date() == c["journey_date"] and ld == [c["true_date"]] and c["true_date"] < c["journey_date"])
    check("repay every app-default journey date is the claim's first submission date, and its train reached the "
          "destination 15 or more minutes late on one record weekday, before it", uniq and len(dflt) >= 30,
          "%d defaulted" % len(dflt))
    check("repay genuine same-day app claims exist beside the defaulted ones",
          sum(1 for c in inscope if c["submitted"].date() == c["journey_date"] == c["true_date"]) >= 3)
    check("repay no in-scope claim on a band edge (29.5 or 59.5 minutes late)",
          not any(c["true_late"] in (29.5, 59.5) for c in inscope))
    check("repay out-of-window claims are submitted at least a day after the journey",
          all(c["submitted"].date() > c["journey_date"] for c in claims if c.get("outside")))
    latest = {}
    for c in inscope:
        latest[c["claim_ref"]] = c
    lat_agg = defaultdict(float)
    for c in latest.values():
        lat_agg[(c["line"], A.ask_band(c["true_late"]))] += c["amount"]
    moved5 = sum(1 for k in rtruth if round(lat_agg[k]) != round(rtruth[k]))
    check("SF16 compensation paid: every payment row (each with its own paid_on and amount) against the latest row per "
          "claim read as a re-assessment; the asking sentence's 'paid' closes it, and the readings differ in at least "
          "six cells", moved5 >= 6, "%d of 9" % moved5)
    check("repay appeal top-ups present", sum(1 for c in claims if c.get("appeal")) >= 10)
    check("repay out-of-window and within-line claims present",
          sum(1 for c in claims if c.get("outside")) > 50 and sum(1 for c in claims if not c["central"]) > 50)
    check("repay every in-scope claim matches one train", _repay_unique(W, claims))
    check("repay no payment dated after the extract", all(c["paid_on"] is None or c["paid_on"] <= P.DR_EXTRACT
                                                         for c in claims),
          str(max(c["paid_on"] for c in claims if c["paid_on"])))
    check("repay no truth cell empty", all(v > 0 for v in rtruth.values()))
    check("repay every row submitted on or after its journey and paid on or after its submission",
          all(c["submitted"].date() >= c["journey_date"] or c["journey_date"] != c["true_date"] for c in claims
              if "true_date" in c) and all(c["paid_on"] is None or c["paid_on"] >= c["submitted"].date() for c in claims))

    # ---------------- input gates and distractors ---------------------------------------------------------
    files = sorted(os.listdir(target))
    check("gate 10 or more files", len(files) >= 10, str(len(files)))
    check("gate 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    check("gate a file of 25,000 rows or more", n_run >= 25000, str(n_run))
    check("gate two distractors shipped", all(K.FILES[k] in files for k in K.DISTRACTORS) and len(K.DISTRACTORS) >= 2)
    check("no file or sheet describes the data",
          not any(re.search(r"readme|dictionary|field.?notes|manifest|notes|schema", f, re.I) for f in files)
          and not any(re.search(r"readme|dictionary|notes|about", sh, re.I)
                      for f in files if f.endswith(".xlsx") for sh in _xlsx_sheets(os.path.join(target, f))))

    # ---------------- realism -----------------------------------------------------------------------------
    refs = [int(c["claim_ref"][2:]) for c in sorted(claims, key=lambda c: c["claim_ref"])]
    check("realism claim references not an arithmetic sequence", len({b - a for a, b in zip(refs, refs[1:])}) > 5)
    inc = sorted(int(ln.split(",", 1)[0][2:]) for ln in open(os.path.join(target, K.FILES["incidents"])).readlines()[1:])
    check("realism incident references not an arithmetic sequence", len({b - a for a, b in zip(inc, inc[1:])}) > 5)
    check("realism station daily gate flows balance within 2.2 to 1",
          all(max(v["entered"], v["left"]) / min(v["entered"], v["left"]) < 2.2 for v in truth.values()))
    loads = [int((census[t["id"]][0].cumsum() - census[t["id"]][1].cumsum()).max()) for t in trains]
    check("realism peak loads below 600 on every train, and varied", max(loads) < 600 and len(set(loads)) > len(loads) // 4,
          "max %d" % max(loads))
    check("realism personas drawn: Julia Clayton issues the brief, Leon Ross saves Cardale's workbooks",
          "Julia Clayton" in brief and "Leon Ross" in _core(os.path.join(target, K.FILES["wtt"])))
    check("realism no library signature in any OOXML container", _no_signature(target))
    check("realism the brief's dates sit after the record and before the export",
          K.BRIEF_DATES[0].date() > P.RECORD_END and K.BRIEF_DATES[1].date() < P.EXPORT_DATE)
    fails = [r for r in RESULTS if not r[1]]
    for lab, ok, det in RESULTS:
        print("%s  %s %s" % ("PASS" if ok else "FAIL", lab, ("(" + det + ")") if det else ""))
    print("checks: %d, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def _docx_text(path):
    z = zipfile.ZipFile(path)
    return re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", z.read("word/document.xml").decode("utf-8")))


def _xlsx_cells(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    return " ".join(str(v) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for v in r if v is not None)


def _xlsx_sheets(path):
    import openpyxl
    return openpyxl.load_workbook(path, read_only=True).sheetnames


def _core(path):
    return zipfile.ZipFile(path).read("docProps/core.xml").decode("utf-8")


def _turnround_identity(W):
    trains = W["trains"]
    for d in W["days"]:
        rec = W["records"][d]
        for seq in Wd.unit_days(trains, rec):
            prev = None
            for i in seq:
                r, tr = rec[i], trains[i]
                if prev is not None and r["dep"][0] > tr["bdep"][0]:
                    bound = r["dep"][0] == rec[prev]["arr"][-1] + P.MIN_TURN
                    slack = rec[prev]["arr"][-1] + P.MIN_TURN <= tr["bdep"][0]
                    if not (bound or slack):
                        return False
                prev = i
    return True


def _late_start_gaps(W):
    out = []
    for d in W["days"]:
        rec = W["records"][d]
        for seq in Wd.unit_days(W["trains"], rec):
            for a, b in zip(seq, seq[1:]):
                if rec[b]["dep"][0] > W["trains"][b]["bdep"][0]:
                    out.append(rec[b]["dep"][0] - rec[a]["arr"][-1])
    return out


def _perf_rows(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True).worksheets[0]
    out = {}
    for r in list(ws.iter_rows(values_only=True))[3:]:
        if r[0]:
            out[(r[0], r[1])] = (r[4], r[5])
    return out


def _line_month_punctuality(W):
    run = defaultdict(int)
    w5 = defaultdict(int)
    stops = defaultdict(int)
    ot = defaultdict(int)
    for d in W["days"]:
        key_m = d.strftime("%B %Y")
        for t in W["trains"]:
            k = (key_m, P.LINE_NAME[t["line"]])
            r = W["records"][d][t["id"]]
            run[k] += 1
            w5[k] += r["arr"][-1] - t["barr"][-1] < 5 * HM
            for i in range(1, len(t["stops"])):
                stops[k] += 1
                ot[k] += r["arr"][i] - t["barr"][i] < 1 * HM
    return {k: (round(100.0 * ot[k] / stops[k], 1), round(100.0 * w5[k] / run[k], 1)) for k in run}


def _gate_naive(rows):
    """UTC read as BST, consecutive differences, a negative difference read as a wrap, a jump over 2,000 dropped,
    the exits counter read as exits and the entries counter as entries."""
    by = defaultdict(list)
    for st, a, t, en, ex in rows:
        by[a].append((t, st, en, ex))
    out = {s: {"entered": 0, "left": 0} for s in P.GATED}
    for a, rr in by.items():
        rr.sort()
        for (t0, s0, e0, x0), (t1, s1, e1, x1) in zip(rr, rr[1:]):
            lt = t1 + dt.timedelta(hours=1)
            if (lt - dt.timedelta(seconds=1)).date() != P.CENSUS_DAY:
                continue
            de, dx = (e1 - e0) % 65536, (x1 - x0) % 65536
            out[s1]["entered"] += de if de <= 2000 else 0
            out[s1]["left"] += dx if dx <= 2000 else 0
    return out


def _census_offs(W, s):
    line, idx = A._station_index(s)
    return int(sum(W["census"][t["id"]][1][t["stops"].index(idx)] for t in W["trains"]
                   if t["line"] == line and idx in t["stops"]))


def _dep_index(W):
    idx = defaultdict(list)
    for t in W["trains"]:
        for k in range(len(t["stops"])):
            if t["bdep"][k] is not None:
                idx[(Wd.station_name(t, k), int(t["bdep"][k] // HM))].append((t, k))
    return idx


def _repay_unique(W, claims):
    idx = _dep_index(W)
    crs = {v: k for k, v in P.CRS.items()}
    for c in claims:
        if c["decision"] != "APPROVED" or c.get("outside") or not c["central"]:
            continue
        o, d = crs[c["origin"]], crs[c["destination"]]
        m = int(c["booked_dep"] // HM)
        direct = [t for t, k in idx[(o, m)] if d in [Wd.station_name(t, q) for q in range(k + 1, len(t["stops"]))]]
        rev = [t for t, k in idx[(d, m)] if o in [Wd.station_name(t, q) for q in range(k + 1, len(t["stops"]))]]
        if len(direct) > 1 or (not direct and len(rev) != 1):
            return False
    return True


def _repay_direct_only(W, claims):
    """The careful route that matches each claim to the train leaving its stated origin at the stated time and
    drops the claims it cannot match."""
    idx = _dep_index(W)
    crs = {v: k for k, v in P.CRS.items()}
    out = defaultdict(float)
    for c in claims:
        if c["decision"] != "APPROVED" or c.get("outside") or not c["central"]:
            continue
        o, d = crs[c["origin"]], crs[c["destination"]]
        m = int(c["booked_dep"] // HM)
        direct = [(t, k) for t, k in idx[(o, m)] if d in [Wd.station_name(t, q) for q in range(k + 1, len(t["stops"]))]]
        if direct:
            out[(c["line"], A.ask_band(c["true_late"]))] += c["amount"]
    return out


def _no_signature(target):
    for f in os.listdir(target):
        if f.endswith((".docx", ".xlsx")):
            z = zipfile.ZipFile(os.path.join(target, f))
            meta = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
            if re.search(rb"python-docx|openpyxl", meta, re.I):
                return False
    return True
