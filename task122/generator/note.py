"""Fill the design note's measured sections from figures.json and the cut pack's routes, so no figure in the note is
typed: the sections between `## Draw`'s close and `## Tried and rejected` are rewritten each run.

    python3 task122/generator/note.py
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NOTE = os.path.join(TASK, "DESIGN_NOTE.md")


def ceiling():
    out = subprocess.run([sys.executable, os.path.join(HERE, "ceiling.py")], capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if l.startswith("pair ceiling")][0]
    pc = float(line.split()[2].rstrip(";"))
    ml = float(line.split()[5])
    keep = [l for l in out.splitlines() if l.startswith("cracker")][0]
    return pc, ml, keep, out


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    L = f["ladder"]
    pct = f["share_prevented_pct_nearest5"]
    sp = 100 * f["share_prevented"]
    zp = os.path.join(TASK, "target.zip")
    zsha = hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8] if os.path.exists(zp) else "(not cut)"
    pc, ml, keep, cout = ceiling()
    fam = {k: v for k, v in L.items() if k.startswith("R3")}
    wrong = {k: v for k, v in L.items() if not k.startswith("R3")}
    S = []
    S.append("""## Default path

1. Read SRB 2026/04 section 3.1: the probe becomes mandatory if its use prevented at least one in five of the STCA
   activations the six sectors would have raised in the time it was running, counted as the Safety Performance
   Report counts them.
2. Clean the records the report's way: each flight's latest plan revision from the FDPS crossing list, live
   activations once per event in the sector where they began, the planner workstation log's New Zealand time taken to
   UTC, a combined position's display covering both sectors.
3. Take the report's own measure, activations per 1,000 flight hours, with the probe running against without: %.1f
   against %.1f, the probe's minutes higher.
4. Recognise that the planners run the probe in busy traffic and hold the traffic: compare each sector's minutes with
   the probe running against its minutes without at the same number of aircraft in the sector (the field's
   traffic-adjusted comparison, conflicts growing with the aircraft present): the probe prevented %.1f per cent.
5. File: short of the one in five, keep the probe discretionary.

Ends on: %.1f per cent prevented, keep PROBE-M discretionary
Golden: %d per cent prevented (%.1f), mandatory from 1 April 2027
""" % (f["rate_on_per_1000fh"], f["rate_off_per_1000fh"], L["R2 like occupancy"], L["R2 like occupancy"], pct, sp))
    S.append("""## Stump sentence

The default path holds the number of aircraft in the sector, minute by minute, finds the probe's minutes raising
activations at %.1f per cent below the rate without it, short of the one in five, and keeps PROBE-M discretionary;
the step that lands it there is holding only the count, when the planners switch the probe on as climbing and
descending traffic gathers and almost every activation involves an aircraft climbing or descending, so at the same
count and the same number climbing or descending the probe prevented about %d per cent of the activations its running
time would have raised, and becomes mandatory.
""" % (L["R2 like occupancy"], pct))
    S.append("""## Three rules

Task type: usability-task-performance-studies (Human Factors & Ergonomics), which serves Experiment & Causal Analysis: the effect of a controller's decision aid on how often the conflict alert fires, read from an operational trial with the aid at the planner's discretion.
Domain test: the quantity that decides is the share of STCA activations the conflict probe prevented, a task-performance effect the field estimates by comparing the alert rate with and without the aid at matched traffic load (activations per flight hour, then at like occupancy, since conflicts grow with the aircraft present); with a hospital's or a retailer's nouns there is no sector, no vertical mix and no conflict alert, and the task stops reading the same.
Swap: "should the ward's early-warning tool be mandatory, on the share of rapid-response calls it prevented" has no aircraft pairs, no climbing or descending traffic and no planner switching the aid on into a traffic mix, so the comparison that decides it does not exist there.
Layer 1: the FDPS crossing list's plan revisions (a revision re-issues the flight's whole list, so a superseded route's crossings drop out), the STCA log's continuation records when an alert carries into the next sector, inhibited and test activations beside live ones, combined sectors overnight on operational names against the crossings' elementary sectors, the planner workstation log in New Zealand time across both daylight-time changes against UTC everywhere else, re-entries into a sector; each is what the systems produce and none is placed to be caught.
Layer 2: estimand_identification, confounding by the conditions of use: the probe is switched on when the climbing and descending traffic that produces the alerts gathers, so its minutes and its idle minutes differ in that mix at any count of aircraft, and the counterfactual for its minutes has to be read at like count and like mix.
Decisive step: setting the probe's running minutes against minutes without it in the same sector at the same number of aircraft and the same number of them climbing or descending, both rebuilt minute by minute from the crossings' entry and exit levels, and reading the activations prevented from the difference.
Not semantics: reading every field, code and definition correctly (the revisions, the continuation records, the combined sectors, the local time) still leaves the report's rate at %.1f per cent and the like-occupancy comparison at %.1f per cent; no column marks a climbing aircraft or holds a minute's traffic mix.
Not rule application: SRB 2026/04 files the estimand (the share of the activations the sectors would have raised in the probe's running time) and the report the counting; no clause says which minutes stand for the probe's minutes without it, and executing every filed rule files whatever comparison the analyst picks; the enumerated family spreads from %.1f to %.1f per cent, the standing family (the strata, observed against expected, the Poisson forms with the count of aircraft as factors or pairs and the climbing count) from %.1f to %.1f, every member printing %d, ruled by the data's own structure (probe use and activations both rising with the climbing and descending count at every occupancy).
Analyst test: a strong analyst cleans the records the report's way, takes the report's rate per 1,000 flight hours (%.1f per cent prevented), holds the number of aircraft minute by minute (%.1f per cent prevented) and keeps the probe discretionary; every field is read and every filed rule applied, and the call is wrong because the probe's minutes carry more climbing and descending traffic at any count of aircraft.
Estimand: probe_m_trial_acceptance_criteria.pdf section 3.1: the share of the STCA activations the trial sectors would have raised in the time PROBE-M was running that its use prevented; population, the six sectors' minutes with the probe running (section 3.3); window, 1 April to 30 September 2026, New Zealand time; unit, activations counted as the Safety Performance Report counts them (section 3.2); comparison, the same time without the probe.
No decoy: nothing is planted to be caught: no memo, draft, briefing or stakeholder figure argues a share or a call, the report's rates are its own published series for 2024/25, and the request asks for the paper and the tables without a view.
No certified replay: no certified or published figure reproduces any route; no file carries a share prevented, a rate with and without the probe, or a recommendation.
Lesson: an aid used at the operator's discretion is switched on when the conditions that produce the outcome gather, so its effect has to be read at like conditions measured at the grain the aid is switched at, the traffic's mix as well as its count; no build on file teaches confounding by the conditions of use.
""" % (L["R0 per flight hour"], L["R2 like occupancy"], min(L.values()), max(L.values()), min(fam.values()),
       max(fam.values()), pct, L["R0 per flight hour"], L["R2 like occupancy"]))
    S.append("""## Survivor anatomy

Actor: the deciding property, how many of the aircraft in a sector are climbing or descending at a given minute, has no column; it is a relation between the crossing rows present in the same minute whose entry and exit levels differ, and the probe's minutes hold more of it at every count of aircraft.
Link: the probe's running time comes from the planner workstation log in New Zealand time on operational, sometimes combined, sectors, the traffic from the FDPS crossings in UTC on elementary sectors, the activations from the STCA log; no key joins them, only time intervals on the configuration in force, and the report's measure never compares a minute's traffic mix across the three.
Reflex: the field's measure, activations per 1,000 flight hours with the probe running against without (%.1f per cent prevented), and its traffic-adjusted form at like occupancy (%.1f), sit at rungs 0 and 2 and file a wrong call.
Back-test: the textbook route validates: the trial's minutes without the probe run at the report's 2024/25 rates for each sector, and the like-occupancy comparison is steady when the hour of day is added (%.1f per cent), so nothing in the record flags the comparison it rests on.
Second use: every file the decisive step reads is in the pack for a reason it independently has: the crossings for the flight hours and flights handled the tables owe, the STCA log for the activation rates, the planner log for the probe's running time the criterion names; the entry and exit levels are the crossing list's own fields.
Shock: the climbing and descending mix swings with the hub's departure and arrival banks every day, ordinary movement; no sector, month or day stands out, and the probe's share prevented holds in every sector.
Pins: the WHAT sits in SRB 2026/04 (the share of the activations the sectors would have raised in the probe's running time, the counting by the report, the window, the combined positions) and no filed sentence names the traffic, the count or the mix of aircraft, or a comparison; deleting section 3.1 unforces the call and the section names no step.
""" % (L["R0 per flight hour"], L["R2 like occupancy"], L["R2 like occupancy and hour of day"]))
    S.append("""## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 the report's rate per 1,000 flight hours, probe running against not | the report defines the rate | flight hours from the crossings | the field's measure | none refutes it | the battery runs it | one ratio | none | readable |
| 1 the hour's traffic held | none | hourly counts from the crossings | a careful variant | none | yes | one stratification | none | readable |
| 2 like occupancy, minute by minute | none | the crossings give the count | the traffic-adjusted reflex | none | yes | one stratification | none | readable |
| 2b per aircraft pair | none | pairs from the count | the conflict-geometry reflex | none | no | one ratio | none | readable |
| 3 (decisive) like count and like climbing and descending mix | none names the mix, the levels or a comparison | no column holds a minute's climbing count | not the reflex: the field adjusts for load | none | no battery item | not affine in a shipped column | the levels are the crossing list's own fields | silent |
""")
    S.append("""## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the activations the sectors would have raised in the time it was running | the counterfactual for the probe's minutes | the rate of the minutes without it | the off-time rate files discretionary | SRB 2026/04 3.1 ("would have raised"); asserted |
| SF2 | the time it was running | the planner log's New Zealand time taken to UTC | the log read as UTC | moves the call (asserted) | the planner guide section 4 ("in New Zealand time") |
| SF3 | activations counted as the report counts them | live, once per event where it began | every live record, or every status | same call; same printed share for the continuation reading (asserted) | the report section 2; SRB 3.2 |
| SF4 | a combined-sector activation | the elementary sector of the first-named aircraft | the first sector of the combined name | same printed share (asserted) | the report section 2 |
| SF5 | the trial window | 1 April to 30 September 2026, New Zealand time | UTC dates | same call (the export is the window; asserted) | SRB 2026/04 section 2 |
| SF6 | the share prevented | over the probe's running minutes | a pooled rate ratio | same printed share (asserted) | none needed |
| SF7 | an aircraft or a probe display in a minute | the minute's midpoint inside the interval | the minute's start, or any overlap | same printed share (asserted) | none needed |
| SF8 | a flight's crossings | its latest plan revision's list | the latest revision of each flight and sector | same printed share; moves the asks (asserted) | the crossing list (a superseded crossing overlaps the flown one in time) |
| SF9 | climbing or descending | entry and exit levels differ | a threshold on the change | same call (levels equal or 40 or more apart; asserted) | the crossing list |
| SF10 | the share's rounding | the nearest five per cent | other units | the prompt files it; mid-bin asserted | the prompt |
| SF11 | the asks' months | New Zealand calendar months | UTC months | moves 30 or more of 36 cells (asserted) | the prompt; the report section 2 |
| SF12 | flights handled | each flight once in each sector it entered | crossings | moves every sector (asserted) | the report section 2 |
| SF13 | an activation's month and sector | its start in New Zealand time, where it began | its end, or the receiving sector | the report's counting (asserted in figs) | the report section 2 |
| SF14 | further strata (hour of day, configuration, weekday) | not needed | added | same printed share (asserted) | none needed |
""")
    S.append("""## Ladder

| Rung | Construction | Share prevented (per cent) | Dies to |
|---|---|---|---|
""" + "\n".join("| %s | %s | %.1f | %s |" % (k.split(" ")[0], " ".join(k.split(" ")[1:]), v,
                                              "the golden" if k.startswith("R3 observed") else
                                              ("a standing member; prints %d" % pct if k.startswith("R3") else
                                               "the probe's minutes carry more climbing and descending traffic at any count"))
                for k, v in L.items()) + """

- **Margins on the cut pack** (asserted in checks.py): every route without the climbing count sits %.1f points or
  more under the bar (highest %.1f); every standing member prints %d, from %.1f to %.1f, clear of the bin's edges;
  the golden %.1f sits mid-bin.
- **Separation.** The default path is wrong on the clean truth (T2) and the like-count-and-mix route on the world's
  own records is the golden (T2); the pack's handling recovers the truth minute by minute (T1).
- **Gate F.** No route that skips the climbing count reaches the bar (asserted).
""" % (20 - max(wrong.values()), max(wrong.values()), pct, min(fam.values()), max(fam.values()), sp))
    S.append("""## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the six sectors' minutes with the probe running | filed (SRB 2026/04 3.1, 3.3) |
| 2 Unit of account | an STCA activation, once per event | filed (the report section 2) |
| 3 Attribution window | 1 April to 30 September 2026, New Zealand time | filed (SRB 2026/04 section 2) |
| 4 As-of dating | the extracts of 5 October 2026 | the files' own period |
| 5 Version basis | each flight's latest plan revision | C1 (SF8) |
| 6 Denominator | the probe's running minutes' expected activations | filed (SRB 3.1) |
| 7 Weighting | the probe's own minutes (observed against expected) | C1 (SF6) |
| 8 Window length | the trial | filed |
| 9 Boundary inclusivity | at least one in five | filed (SRB 3.1) |
| 10 Rounding path | the share unrounded, printed to the nearest five | the prompt; C1 |
| 11 Tie-break | none | C1 |
| 12 Maturity and censoring | the trial closed on 30 September; the log is complete | filed |
| 13 Order of operations | clean, rebuild the minutes, stratify, compare | C1 |
| 14 Row order | none: set operations by sector and minute | C1 |
| 15 Duplicate resolution | a continuation record is the same event | filed (the report section 2; SF3) |
| 16 Identity normalisation | callsign and time to the flight's crossing | SF4 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | minutes, flight hours, activations per 1,000 flight hours | the files' own fields |
| 19 Code and status semantics | LIVE, INHIBITED, TEST | filed (the report section 2) |
| 20 Integerisation | whole activations and aircraft | C1 by construction |
| 21 Clause scope | SRB section 4's survey and training plan inform the rollout, not the decision | filed scope |
| 22 Forward window contents | the mandate from 1 April 2027 | filed (SRB 2026/04 section 1) |
""")
    S.append("""## Literal reader

Executed word for word, SRB 2026/04 section 3.1 asks for the share of the STCA activations the six sectors would have
raised in the time PROBE-M was running that its use prevented. Read literally, the minutes without the probe stand for
the probe's minutes only where they carry the same traffic: the same sector, the same aircraft present and the same of
them climbing or descending, since the planners switched the probe on as that traffic gathered and the activations
come from it; set against those minutes, the probe's running time raised %s activations against %s, about %d per cent
prevented. The asks' months, counts and flights read literally on the report's definitions give the figures in
figures.json.
""" % ("{:,}".format(f["observed"]), "{:,}".format(int(round(f["expected"]))), pct))
    S.append("""## Oracles

None on the main call: no file carries a share prevented, an activation rate with and without the probe, or a
recommendation; the report's rates are for July 2024 to June 2025, before the probe. The asks have no oracle either:
the report's tables cover a year with no overlap with the trial.
""")
    S.append("""## Ask sheet

Three asks on the trial's records, each read through a reconstruction across two systems or grains no sentence
states.

**Ask A, flight hours by sector and New Zealand month (36 figures).**
- Files: the FDPS crossing list.
- Primary (D9, a superseded plan): a revision re-issues the flight's whole crossing list, so a rerouted flight's
  first-plan crossing through a sector it never flew stays in under the natural de-duplication (the latest revision
  of each flight and sector); only each flight's latest revision is flown.
- Hazards: month ends in New Zealand time against UTC timestamps, across both daylight-time changes.

**Ask B, STCA activations per 1,000 flight hours by sector and month (36 figures).**
- Files: the STCA log, the crossing list.
- Primary: the continuation record an alert opens as it carries into the next sector is the same event, found only
  by its pair and its start at the hand-over second; a combined-sector activation goes to the first-named aircraft's
  sector, read from the crossings.
- Hazards: inhibited and test activations; Ask A's hours as the denominator.

**Ask C, flights handled by sector over the trial (6 figures).**
- Files: the crossing list.
- Primary: Ask A's superseded crossings put flights in sectors they never entered.
- Hazard: re-entries counted once (the report).

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at like occupancy) | Verdict |
|---|---|---|---|
| A, 36 monthly figures | takes the latest revision of each flight and sector | the same | miss |
| B, 36 monthly figures | the same hours under the rates | the same | miss |
| C, 6 figures | counts the superseded crossings' flights | the same | miss |

Pair ceiling: %.1f (%s).
Mirror leakage: %.1f per cent of the ask weight.
Measured by: generator/ceiling.py (run on the cut pack, target.zip %s)
""" % (pc, keep.split(": ", 1)[1] if ": " in keep else keep, ml, zsha))
    body = "\n".join(S)
    note = open(NOTE, encoding="utf-8").read()
    i = note.index("## Default path") if "## Default path" in note else note.index("## Tried and rejected")
    j = note.index("## Tried and rejected")
    note = note[:i] + body + "\n" + note[j:]
    open(NOTE, "w", encoding="utf-8").write(note)
    print(cout)
    print("note filled")


if __name__ == "__main__":
    main()
