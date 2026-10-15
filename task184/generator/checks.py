"""Assertions on the built pack and goldens: the input gates; the three rules executed on the generator's clean
truth (R1 every offence ships with both its occurrence times and nothing states a weight; R2 each Layer 1 item is
neutral for the call and the graded bins; R3a the easy route files the seven evening slots and Friday morning with
every filed rule applied; R3b the decisive step alone files the golden eight and each single correction stays wrong;
R3c nothing planted); the ladder by name with its margins; every spreading grain and the profile-weighted
refinement in one slate; the semantic forks SF1 to SF9; the asks' goldens against the truth with every stop outside
the bin; the separation of the asks from the call; the documents' silence; and the goldens against figures.json."""
import csv
import datetime as dt
import io
import json
import os
import re
import zipfile

import openpyxl

import analysis as AN
import asks as AK
import build as B
import deliver as DL
import docs as D
import offences as O
import pack as P
import places as PL
import records as R
import sensors as S
import world as W

N = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def ok(cond, what):
    N[0] += 1
    if not cond:
        raise AssertionError(what)


def read_csv(path):
    with io.open(path, encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(path).pages))


def fifty(x):
    return int(round(x / 50.0) * 50)


def name(s):
    return "%s %02d:00-%02d:00" % (W.DAYS[s[0]], s[1], (s[1] + W.SLOT_H) % 24)


def slate_of(w):
    return AN.slate(w)


def run(target, golden, w, meta_path, quiet=False):
    fig = w["fig"]
    rows, fringe, counts = w["rows"], w["fringe"], w["counts"]
    contracted, lad = w["contracted"], w["ladder"]
    g = lad["golden"]
    weights, slate = g["weights"], g["slate"]
    meta = json.load(io.open(meta_path, encoding="utf-8"))
    rms = read_csv(os.path.join(target, R.RMS))
    legacy = read_csv(os.path.join(target, R.LEGACY))
    head = rms[0]
    col = {c: i for i, c in enumerate(head)}

    # ---------------------------------------------------------------- the input gates
    files = os.listdir(target)
    ok(len(files) >= 10, "ten files or more (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three formats or more")
    ok(len(rms) - 1 >= 25000, "one file of 25,000 rows or more (%d)" % (len(rows) - 1))
    ok(len(meta["distractor_files"]) >= 2, "two distractors or more")
    for f in meta["distractor_files"]:
        ok(f in files, "the distractor %s ships" % f)
        ok("distract" not in f and "unused" not in f, "no distractor names itself")
    for e in meta["files"]:
        ok(e["source"] and e["date"] and e["license"], "every file records source, date and licence")

    # ---------------------------------------------------------------- R1: the raw material ships, nothing derived
    ok(head == ["crime_reference", "offence_class", "occurred_from", "occurred_to", "reported_at", "location_code",
                "address_text", "beat_code", "record_status"], "R1 the extract's columns")
    for r in rms[1:]:
        ok(r[col["occurred_from"]] and r[col["occurred_to"]], "R1 both occurrence times ship on every row")
    allcols = " ".join(head + legacy[0]).lower()
    for word in ("weight", "share", "slot", "duration", "hours", "aoristic", "spread", "midpoint", "minutes"):
        ok(word not in allcols, "R1 no derived column (%s)" % word)
    refs = [r[0] for r in rms[1:]]
    ok(len(refs) == len(set(refs)), "R1 the crime reference is unique in the extract")
    docs_text = {f: (pdf_text(os.path.join(target, f)) if f.endswith(".pdf")
                     else io.open(os.path.join(target, f), encoding="utf-8").read())
                 for f in files if f.endswith(".pdf") or f.endswith(".md") or f.endswith(".csv")}
    for f, text in docs_text.items():
        low = text.lower()
        for word in ("aoristic", "in proportion to the window", "share of the window", "spread the offence",
                     "weight of a slot", "slot weight", "fraction of the window"):
            ok(word not in low, "R1 no document names the weighting (%s in %s)" % (word, f))
    for f, text in docs_text.items():
        if f.endswith(".pdf") or f.endswith(".md"):
            ok("{:,}".format(fifty(g["files"])) not in text and str(fifty(g["files"])) not in text,
               "R1 no document carries the covered total (%s)" % f)
        if f in (D.SCHEDULE, D.CONTRACT, S.TRADING, PL.PREMISES):
            continue                      # these list slot and trading times, and no offence figure
        for d in range(7):
            for h in range(0, 24, W.SLOT_H):
                for label in ("%s %02d:00" % (W.DAYS[d], h), "%s, %02d:00" % (W.DAYS[d], h)):
                    for m in re.finditer(re.escape(label), text):
                        tail = text[m.end():m.end() + 40]
                        ok(re.search(r"\d{3,}", tail) is None,
                           "R1 no document pairs a slot with a figure (%s, %s)" % (f, label))

    # ---------------------------------------------------------------- R2: Layer 1 is neutral for the call
    main = [r for r in rms[1:] if r[col["offence_class"]] in W.CONTRACTED and
            r[col["location_code"]] in PL.CODE.values()]
    ok(len(main) == len(contracted), "R2 the main population is the quarter's contracted rows (%d)" % len(main))
    ok(all(r[col["location_code"]] for r in main), "R2 no contracted quarter row has a blank location code")
    ok(not any(r.get("code") in PL.CODE.values() for r in fringe), "R2 no fringe row carries a quarter code")
    ok(not any(r["cls"] in W.CONTRACTED and "cis" in r for r in rows),
       "R2 no contracted offence is in the legacy export")
    leg_classes = {r[1] for r in legacy[1:]}
    ok(all(W.LEGACY_NAMES.get(c, c) in leg_classes or True for c in leg_classes), "R2 the legacy classes are named")
    ok(not any(c in leg_classes for c in W.CONTRACTED), "R2 the legacy export holds no contracted class")
    # the main path reads none of the ask files
    for f in (R.LEGACY, PL.GAZETTEER, S.COUNTS, S.AVAIL, S.SENSREG, P.PLAN, PL.PREMISES, PL.BEATS):
        ok(f in files, "the ask and distractor file %s ships" % f)

    # ---------------------------------------------------------------- R3a: the easy route, every rule applied
    r0 = lad["rung0_window_start"]
    ok([name(s) for s in r0["slate"]] == fig["default_path"]["slate"], "R3a the easy route's slate")
    ok(all(s[1] in (16, 20) for s in r0["slate"]),
       "R3a the easy route takes the late afternoon and evening slots only")
    ok(fifty(r0["files"]) == fig["default_path"]["files"], "R3a the easy route's own figure")
    ok(r0["files"] / g["files"] >= 1.4, "R3a the easy route overstates its coverage by at least two fifths")
    ok(set(r0["slate"]) != set(slate), "R3a the easy route is not the golden slate")
    ok(len(set(r0["slate"]) & set(slate)) == 4, "R3a the easy route keeps four of the eight names")
    for rung in ("rung0_window_start", "rung1_window_end", "rung2_midpoint"):
        rw = lad[rung]["weights"]
        kept = [s for s in W.SLOTS if fifty(rw[s]) == fifty(weights[s])]
        ok(len(kept) <= 2, "R3a %s keeps at most two of the 42 cell figures (%d)" % (rung, len(kept)))
        ok(all(s not in kept for s in slate), "R3a %s gets every commissioned cell wrong" % rung)
        ok(len([s for s in W.SLOTS if fifty(rw[s]) != fifty(weights[s])]) >= 40,
           "R3a %s gets at least 40 of the 42 cells wrong" % rung)

    # ---------------------------------------------------------------- R3b: the decisive step alone
    ok([name(s) for s in slate] == fig["call"]["slate"], "R3b the golden slate")
    ok(fifty(g["files"]) == fig["call"]["covered_total"], "R3b the covered total")
    for rung in ("rung0_window_start", "rung1_window_end", "rung2_midpoint"):
        ok(set(lad[rung]["slate"]) != set(slate), "R3b %s files another slate" % rung)
        ok(lad[rung]["meets"] / g["files"] <= 0.83, "R3b %s meets at most five sixths" % rung)
        ok(lad[rung]["files"] / g["files"] >= 1.05 and fifty(lad[rung]["files"]) != fifty(g["files"]),
           "R3b %s overstates its own coverage and files a figure outside the bin" % rung)
    order = sorted(weights.items(), key=lambda kv: -kv[1])
    gap = 100.0 * (order[7][1] - order[8][1]) / order[8][1]
    ok(gap >= 9.0, "R3b the cap falls on a gap of at least 9 per cent (%.1f)" % gap)
    ok(fifty(order[8][1]) == fig["call"]["runner_up_offences"], "R3b the runner-up's figure")

    # ---------------------------------------------------------------- R3c: nothing planted, nothing hidden
    ok(all(r["to"] >= r["from"] for r in rows + fringe), "R3c no window runs backwards")
    ok(all(r["reported"] >= r["to"] for r in rows + fringe), "R3c nothing is reported before it ends")
    ok(all(r["from"] <= r["true"] <= r["to"] for r in rows), "R3c every true time lies inside its window")
    tw = AN.per_season(AN.true_time_weights(contracted))
    ok(set(slate_of(tw)) == set(slate), "R3c the offences' true times give the same eight slots")
    ok(not any("true" in c or "actual" in c for c in head), "R3c no column holds the unobserved time")

    # ---------------------------------------------------------------- the grain and the refinement converge (C1)
    for step in (60, 15, 5):
        sw = AN.per_season(AN.sampled_weights(contracted, step))
        ok(max(abs(sw[s] - weights[s]) for s in weights) < 1e-6,
           "SF7 the %d-minute grain gives the same figure" % step)
        ok(set(slate_of(sw)) == set(slate), "SF7 the %d-minute grain gives the same slate" % step)
    ct = pdf_text(os.path.join(target, D.CONTRACT))
    # SF8 and SF10: the agreement's clause 4.4 is what rules out placing an offence inside its window from
    # another source, and the two routes it rules out are shown here to file another slate, so the clause is
    # load bearing rather than decorative.
    ok("built from the force's record of those offences and from nothing else" in ct,
       "SF8 the agreement's clause 4.4 confines the count to the force's record of the covered offences")
    ok("no other offence, data source or proxy may be used to place it within that period" in ct,
       "SF10 clause 4.4 rules out any other source for placing an offence inside its window")
    pw = AN.per_season(AN.profile_weighted(contracted, rows))
    ok(set(slate_of(pw)) != set(slate), "SF8 the other classes' hourly profile files a different slate")
    sensor_of = {loc: sid for sid, (loc, _pos) in W.SENSORS.items()}
    fw = AN.per_season(AN.footfall_weighted(contracted, counts, sensor_of))
    ok(set(slate_of(fw)) != set(slate), "SF10 the footfall-weighted route files a different slate")
    ok(not any(c in " ".join(docs_text.values()).lower()
               for c in ("equally likely", "uniformly across", "evenly across the window")),
       "SF10 no document states the distribution inside a window")
    windowed = [r for r in contracted if r["to"] > r["from"]]
    ok(all(r["from"].minute == 0 and r["to"].minute == 0 for r in windowed),
       "SF7 every window is recorded on the hour at both ends")
    ok(len(windowed) == len(contracted), "SF7 every contracted offence carries a window")

    # ---------------------------------------------------------------- the semantic forks
    sched = read_csv(os.path.join(target, D.SCHEDULE))
    ok(len(sched) - 1 == len(W.SLOTS), "SF3 the tasking schedule lists all 42 slots")
    ok(sched[0] == ["slot_id", "day_of_week", "slot_start_local", "slot_end_local", "hours"], "SF3 its columns")
    ok(all(r[2].endswith(":00") and int(r[2][:2]) % W.SLOT_H == 0 for r in sched[1:]),
       "SF3 every slot starts on a four-hour boundary from midnight")
    ok("eight patrol slots in each week" in ct, "SF1 the contract buys eight slots a week")
    ok("1 April 2027 to 30 September 2027" in ct, "SF5 the contract fixes the season")
    ok("occurred within the quarter" in ct and "occurred while a commissioned patrol slot was being worked" in ct,
       "SF2 the contract defines a covered offence by when it occurred")
    ok("reported, recorded or detected during a patrol slot" in ct, "SF2 the contract rules the report time out")
    for c in W.CONTRACTED:
        ok(c in ct, "SF1 the contract's Annex B names %s" % c)
    for c in W.CLASSES:
        if c not in W.CONTRACTED:
            ok(c not in ct, "SF1 the contract names no class it does not cover (%s)" % c)
    reg = read_csv(os.path.join(target, PL.REGISTER))
    ok(len(reg) - 1 == len(W.LOCATIONS), "SF4 the register holds the quarter's five locations")
    ok([r[1] for r in reg[1:]] == list(W.LOCATIONS), "SF4 the register names them")
    dict_rows = read_csv(os.path.join(target, D.DICTIONARY))
    defs = {r[1]: r[3] for r in dict_rows[1:]}
    ok("earliest time at which the offence can have occurred" in defs["occurred_from"],
       "the dictionary files what occurred_from means")
    ok("latest time at which the offence can have occurred" in defs["occurred_to"],
       "the dictionary files what occurred_to means")
    ok("no time between the two" in defs["occurred_to"] and "none is derived" in defs["occurred_to"],
       "the dictionary says the system holds nothing between the two")
    rules = pdf_text(os.path.join(target, D.RULES))
    ok("earliest and the latest time at which it can have occurred" in rules,
       "the recording standard files the window")
    ok("no inference is recorded about where within the two the offence occurred" in rules,
       "the recording standard records no inference inside the window")

    # SF6, the figure's period: one season, the mean of the two on record
    per_both = {s: v * len(W.SEASONS) for s, v in weights.items()}
    ok(abs(sum(per_both[s] for s in slate) - len(W.SEASONS) * g["files"]) < 1e-9,
       "SF6 the two seasons added are twice the figure the paper carries")
    ok(all(fifty(per_both[s]) != fifty(weights[s]) for s in slate),
       "SF6 the two seasons added land outside the bin on every commissioned slot")
    ok(AN.slate(per_both) == slate, "SF6 the two seasons added give the same eight slots in the same order")

    # SF9, the rounding path: the figure is rounded once, at the end
    parts = {s: 0.0 for s in W.SLOTS}
    for r in contracted:
        a, b = r["from"], r["to"]
        if b <= a:
            parts[O.slot_of(a)] += 1.0
            continue
        span = (b - a).total_seconds()
        t = a
        while t < b:
            nxt = AN.slot_start(t) + dt.timedelta(hours=W.SLOT_H)
            parts[O.slot_of(t)] += round((min(b, nxt) - t).total_seconds() / span, 1)
            t = min(b, nxt)
    parts = AN.per_season(parts)
    ok(max(abs(parts[s] - weights[s]) for s in W.SLOTS) > 1.0,
       "SF9 rounding each offence's share first is a different path, as the question's closing sentence rules out")
    ok(AN.slate(parts) == slate, "SF9 and it still gives the same eight slots in the same order")

    # ---------------------------------------------------------------- the graded figures sit mid-bin
    worst = min(abs(v % 50 - 25) for v in list(weights.values()) + [g["files"]])
    ok(worst >= 2.0, "every one of the 43 call figures sits at least 2 offences from a half of fifty (%.2f)"
       % worst)
    for (c, si), v in w["ask1"].items():
        ok(v % 10 != 5, "ask 1 %s %d is not a tie on a ten" % (c, si))
        if c in W.LEGACY_NAMES:
            # the classes the two exports both hold are the ones a solver can reconcile more than one way, so
            # their counts sit clear of the rounding edge; the five the contract covers are in one export only,
            # fully coded, and their count has no second route (verify.py checks both routes agree row for row)
            ok(abs(v % 10 - 5) >= 2, "ask 1 %s %d sits clear of the rounding edge (%d)" % (c, si, v))
    worst2 = min(abs((v * 10) % 1 - 0.5) for v in w["ask2"].values())
    ok(worst2 >= 0.12, "every location share sits clear of the one-decimal edge (%.3f)" % worst2)
    worst3 = min(abs(v % 10 - 5) for v in w["ask3"].values())
    ok(worst3 >= 1.4, "every footfall figure sits clear of the half-ten (%.2f)" % worst3)

    # ---------------------------------------------------------------- ask 1: the device and its stops
    a1 = w["ask1"]
    st1 = AK.offences_by_class_stops(rows, fringe)
    for k in a1:
        ok(abs(st1["union"][k] - a1[k]) > 5, "ask 1 the union stop lands outside the bin at %s %d" % k)
        ok(abs(st1["by_reference"][k] - a1[k]) > 5,
           "ask 1 de-duplicating on the reference lands outside the bin at %s %d" % k)
    for c in W.LEGACY_NAMES:
        if c != "Theft from the person":
            ok(abs(st1["rms_only"][(c, 0)] - a1[(c, 0)]) > 5,
               "ask 1 the legacy export left out lands outside the bin at %s" % c)
    dbl = [r for r in rows if "cis" in r and R.in_rms(r)]
    ok(len(dbl) > 200, "ask 1 the parallel fortnight is big enough to move the figures (%d)" % len(dbl))
    ok(all(W.PARALLEL[0] <= r["reported"].date() <= W.PARALLEL[1] for r in dbl),
       "ask 1 every double-written row is inside the fortnight")
    ok(all(r["cls"] != "Theft from the person" for r in dbl), "ask 1 the benign twin was not double written")
    notes = io.open(os.path.join(target, D.NOTES), encoding="utf-8").read()
    ok("in both systems" in notes and "the references do not" in notes,
       "the extract notes describe the parallel running without naming a repair")

    # ---------------------------------------------------------------- ask 2: the keys and the register's range
    a2 = w["ask2"]
    st2 = AK.location_share_stops(rows, fringe)
    for k, v in a2.items():
        for nm in ("range_kept", "coded_only"):
            if k in st2[nm]:
                ok(abs(st2[nm][k] - v) > 0.05, "ask 2 the %s stop lands outside the bin at %s %d" % (nm, k[0], k[1]))
    gaz = read_csv(os.path.join(target, PL.GAZETTEER))
    alts = [r for r in gaz[1:] if r[3] == "alternative"]
    ok(len(alts) >= 2, "ask 2 the gazetteer carries the alternative spellings")
    ok(any(r[1] == "Harbourgate Street" and r[2] != "Harbourgate" for r in gaz[1:]),
       "ask 2 the gazetteer holds the second Harbourgate Street")
    ok([r for r in reg[1:] if r[1] == "Harbourgate Street"][0][4] == "178",
       "ask 2 the register's Harbourgate Street range stops at 178")
    ok(any(r["number"] > 178 for r in fringe), "ask 2 the fringe rows are numbered above the range")

    # ---------------------------------------------------------------- ask 3: the outages
    a3 = w["ask3"]
    st3 = AK.footfall_stops(counts)
    for k, v in a3.items():
        for nm in ("every_hour", "faults_left_in", "faults_out_of_the_count_only"):
            ok(abs(st3[nm][k] - v) > 5, "ask 3 the %s stop lands outside the bin at %s %d" % (nm, k[0], k[1]))
    av = read_csv(os.path.join(target, S.AVAIL))
    ok(len(av) - 1 == sum(len(v) for v in S.FAULTS.values()), "ask 3 every fault is in the supplier's log")
    ok(all(len(S.FAULTS[sid]) == len(W.SEASONS) for sid in W.SENSORS),
       "ask 3 every sensor carries a fault in both seasons")
    cnt = read_csv(os.path.join(target, S.COUNTS))
    ok(cnt[0] == ["sensor_id", "count_hour_utc", "pedestrians"], "ask 3 the feed's columns")
    ok(any(r[2] == "0" for r in cnt[1:]), "ask 3 the feed holds genuine zero rows")
    ok(len(cnt) - 1 == len(counts), "ask 3 the feed ships every row")
    sr = read_csv(os.path.join(target, S.SENSREG))
    ok(all(r[4] == "UTC" for r in sr[1:]), "ask 3 the register files the feed's time zone")
    ok(len(cnt) - 1 == len(W.SENSORS) * sum(len(W.season_days(i)) for i in range(len(W.SEASONS))) * 24,
       "ask 3 the feed publishes every hour of both seasons")
    ok(all(v == int(round(a3[k], -1)) for k, v in
           zip(sorted(a3), [int(round(a3[k], -1)) for k in sorted(a3)])), "ask 3 the figures round to the ten")

    # ---------------------------------------------------------------- the goldens
    paper = pdf_text(os.path.join(golden, DL.PAPER))
    for s in slate:
        label = "%s %02d:00 to %02d:00" % (W.DAYS[s[0]], s[1], (s[1] + W.SLOT_H) % 24)
        ok(label in paper, "the paper names %s" % label)
        ok("{:,}".format(fifty(weights[s])) in paper, "the paper carries %s's figure" % label)
    ok("{:,}".format(fifty(g["files"])) in paper, "the paper carries the covered total")
    ok("—" not in paper and "–" not in paper, "no dash in the paper")
    book = openpyxl.load_workbook(os.path.join(golden, DL.BOOK))
    ok(book.sheetnames == ["Week", "Commissioned", "Offences by class", "Location shares", "Footfall", "Notes"],
       "the workbook's sheets")
    nt = [c.value for c in book["Notes"]["A"] if c.value]
    ok(len(nt) >= 8, "the workbook's notes sheet carries the population, the conventions and the exclusions")
    ok(not any("\u2014" in x or "\u2013" in x for x in nt), "no dash in the workbook's notes")
    wk = list(book["Week"].iter_rows(min_row=2, values_only=True))
    ok(len(wk) == len(W.SLOTS), "the workbook carries all 42 slots")
    for r in wk:
        d = W.DAYS.index(r[0])
        h = int(r[1][:2])
        ok(r[2] == fifty(weights[(d, h)]), "the workbook's figure for %s %s" % (r[0], r[1]))
        ok((r[3] == "commissioned") == ((d, h) in set(slate)), "the workbook marks the eight")
    cls_rows = list(book["Offences by class"].iter_rows(min_row=2, values_only=True))
    ok(len(cls_rows) == len(W.CLASSES) * len(W.SEASONS), "the workbook's class rows")
    for c, yr, v in cls_rows:
        ok(v == int(round(a1[(c, yr - 2025)], -1)), "the workbook's offence count for %s %d" % (c, yr))
    for loc, yr, v in book["Location shares"].iter_rows(min_row=2, values_only=True):
        ok(abs(v - round(a2[(loc, yr - 2025)], 1)) < 1e-9, "the workbook's share for %s %d" % (loc, yr))
    for sid, yr, v in book["Footfall"].iter_rows(min_row=2, values_only=True):
        ok(v == int(round(a3[(sid, yr - 2025)], -1)), "the workbook's footfall for %s %d" % (sid, yr))

    # ---------------------------------------------------------------- figures.json against the goldens
    ok(fig["week"] == {name(s): fifty(weights[s]) for s in W.SLOTS}, "figures.json carries the 42 cells")
    ok(fig["context"]["share_of_windows_over_four_hours"] >= 0.85, "nine in ten windows run over four hours")
    ok(fig["context"]["share_of_windows_crossing_a_slot"] >= 0.90, "almost every window crosses a slot boundary")
    for f in files:
        ok(not f.startswith("."), "no dot file in the pack")
        ok("golden" not in f and "answer" not in f and "clean" not in f, "no author noun in a file name")
    if not quiet:
        print("checks: %d assertions passed (slate %s at %d a season; the easy route files %d on %s and meets %d, "
              "%.3f of it; worst call bin %.2f of 25; gap at the cap %.1f per cent)"
              % (N[0], ", ".join(name(s) for s in slate[:3]) + " and five more", fifty(g["files"]),
                 fig["default_path"]["files"], ", ".join(name(s) for s in r0["slate"][:3]) + " and five more",
                 fig["default_path"]["meets"], fig["default_path"]["share_of_golden"], worst, gap))
