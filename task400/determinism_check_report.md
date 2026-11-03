# determinism-check report, task400, 2026-11-03

## Pass 1 (target.zip 36837e7e, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** FIX_NOW. Gate G: method_or_model_selection, analytical_non_defect, no
surface-read dependency, no sole data defect. Gate H: domain pass, layers pass, decisive step analytical. Order kept
(derivation written before the graded blocks were opened).

### The thread's verdict, verbatim

# Verdict, task400

- **Verdict:** DETERMINISTIC (main call C reproduces; two ask families rest on unfiled counting rules, see Gate C/E notes).
- **Disposition:** FIX_NOW. Pin in prompt.txt, as WHAT not HOW, what one light-vehicle trip is and what one time over the limit is (a vehicle entering counts once however many gate readers it passes; one continuous stretch over the limit counts once). Figures and files unchanged, no rerun needed beyond a re-read of the asks.
- **Why:** The only behavioural change the files measure is the haul trucks' response to critical alerts: in cas/fms data the share of CAS_CRITICAL windows where speed at t+6 s is at least 6 km/h below speed at t0 is 0.86 on 4.3.14 units and 0.29 on 5.0.2 units over 2 to 23 June 2026 (633 and 639 usable windows), flat 0.85 to 0.88 for the 17 months before and 0.30 to 0.33 in Jul to Oct. Alert volume, range, duration, acknowledgement (96 pct, 2 s) are unchanged, so the CAS report's "all on current release" and ack rate hide it. Day and night are the same (0.84/0.88 on 4.3, 0.32/0.26 on 5.0.2), which rules out D; the CRU rise is +4, ruling out E; A's operators still slow on 4.3 units. Programme C is the only one with measured support. Weakness (not a gate fail): the incident link is temporal and mechanistic, not estimated. Incidents rose from 3 June on trucks still on 4.3.14 (7 incidents in 5.7k truck-hours during the rollout vs 11 in 6.2k on 5.0.2), so "5.0.2 accounts for most of the rise" is not shown by the register alone.
- **Evidence (recomputed):**
  - VI-COL+VI-SPI: Jul-Oct 2025 6,2,9,5 = 22; Jul-Oct 2026 18,27,22,19 = 86. Reproduced.
  - Firmware 5.0.2 on trucks 2 to 23 June 2026 (Firmware sheet, 2/day, 02:30 UTC). Reproduced. Response rates 85 pct and 30 pct to the nearest 5: reproduced (86.1 and 28.9). The fms trigger_time is WA local (checked: CAS onset_utc less 8 h matches 500 of 500 windows), so the UTC to local step in solution step 3 is right.
  - Trips: IN rows 9,620 / 11,229 / 11,162 / 11,307. Dropping every NG-2 read 2 to 13 s after an NG-1 read (13,088 reads; histogram has no reads 13 to 20 s) gives 7,517 / 7,601 / 7,492 / 7,620 with 192 / 189 / 296 / 171 blank cas_tag. Reproduced. Fork: no shipped file says a trip is deduplicated across NG-1 and NG-2 (NG-2 opens 14 July); a literal reader counting IN rows gets 9,620 etc. The data separate the two readings (the 3 to 13 s cluster against nothing until 20 s), so a careful analyst reaches the golden, but the text does not force it.
  - Ramp times over limit in force (haul_road_speed_limits.csv, by local date; fms limit_kmh is back-filled to the current limit and wrong for NRP before 9 June and SRP before 18 Aug): merging windows 8 to 12 s apart on the same truck and ramp (94 pairs, next gap above 60 s) gives NRP 44/44/48/49 with 17/16/23/19 over 5; SRP 31/29/38/32 with 13/11/13/15. Reproduced. Counting raw OVERSPEED windows gives NRP 44/64/66/66 and SRP 31/39/53/46, and using the stale fms limit gives SRP over-5 of 31/23/14/18. Same fork class as trips: the merge rule is unfiled.
  - Step 2 (per 1,000 shifts S-ORE 2.2 to 11.7, N-WST 8.4 to 15.8): consistent with my shift join (5 to 19 and 7 to 35 incidents); both routes rise, so it weakens B only moderately; B is also at 23 pct of the rise (NRJ +15 of 64).
  - Competing answers tried: B (NRJ largest single location, 23 pct, and the north waste route took 5.5k to 6.0k h/month from 2.2k in June, a real route reallocation no document mentions); D (night 9 to 43, 53 pct, but hour mix of incidents is unchanged and the alert response is the same by day and night); A (rise is site wide, but no attention measure falls except on 5.0.2 units); E (+4). None has measured support.
- **Files/Hygiene:** PASS. 14 files; formats parquet, xlsx, csv, pdf, docx (5). Distractors present (dust PM10, road maintenance log, CAS monthly report, light vehicle register). Temporal coherence holds. One observation: the cas_alert peer tags for the incident's other party are not the register's party (random peer tags), harmless as nothing relies on it. No provenance disclosures found. No exclusion-level finding.
- **Stump power:** Good. The easy route is the register cut by location (NRJ largest, B) or by night (D), or accepting the CAS report ("current release, acknowledgement 96 pct, alerts per 100 h up a little") and finding nothing; a strong model that cuts incidents by location and route files B or A. The 5.0.2 contrast needs the staggered 2 to 23 June window (both firmwares running) to separate the firmware from the calendar; a before and after comparison by month mixes the rollout with the June step. Expect GPT to stump on B or D unless it joins fms to the firmware table.
- **Stumping type:** `mechanism: method_or_model_selection` (staggered-rollout contrast, experiment and causal), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures (incident counts, alert volumes, ack rate) are all correct; the difficulty is choosing the within-rollout comparison. Not banned.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Field's own analysis: attributing an incident rise to a controls change through a staged-rollout natural experiment on the operators' behavioural response. Layer 1: UTC against WA local, device swaps by asset, back-filled limit column, OCR plates, duplicate gate reads. Easy route and wrong answer: cut the register by location or hour (B or D), or trust the CAS report. A strong analyst who cleaned everything correctly still files B.
- **Fix:** prompt. Add one clause to each of the two ask sentences defining the counted unit (one vehicle entering the pits is one trip however many readers read it; one continuous stretch over the limit is one time). Optional, solution: state in the golden's step 7 that the incident rise also appears on trucks still on 4.3 in early June, or drop the sentence claiming the firmware accounts for it, so the claim is not stronger than the data.
- **Order kept:** yes. derivation.md was written before graded_blocks.md was opened; the alert-response mechanism was not in it (found only after) and is recorded in the addendum.

### Answered in one generator pass (target.zip 954bd646)

- FIX_NOW: the two ask units filed in prompt.txt as WHAT ("A trip is one vehicle entering a pit, and a time over the
  limit is one continuous run above it."), without naming the readers or the windows.
- Weakness: the incident register re-drawn on its own stream to a representative draw (checks.py R3d), and the
  recommendation and step 7 cut to what the records show.
- Re-judge: round 2 brief at the scratch folder judge_r2/ (pipeline.json resume).

## Pass 2 (target.zip 954bd646, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** FIX_NOW on the solution side only (the chart line). Every round-1 finding
closed. Gate G: decomposition_attribution (a staggered-rollout contrast) with etl_conformance asks, analytical
non-defect. Gate H: domain pass, layers pass, decisive step analytical. Order kept.

### The thread's verdict, verbatim

# Verdict, task400, round 2

Order kept: yes. prompt.txt and all 14 files read and every figure recomputed, derivation.md written first, then graded_blocks.md, then round1_findings.md. Cross-batch reference check: not possible from this folder (no other task visible); nothing in the bundle looks like a clone, not asserted either way.

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW. Reword graded ask 3 so it does not demand a bar chart with labelled bars (the prompt only says "a chart of the monthly count"); no data change, no rerun. One optional data item below (33 same-vehicle re-reads) is accepted risk unless the author wants it removed.
- **Why:** Programme C is forced by the shipped files. The 30 haul-truck units went from firmware 4.3.14 to 5.0.2 on 2 to 23 June 2026 (cas_device_register Firmware sheet, UTC, +8 h), and in that window, with both versions running on the same days and the same operators (dispatch operator_id), critical alerts were followed by the truck slowing 86 per cent of the time on 4.3 units and 29 per cent on 5.0.2 units (CAS_CRITICAL windows joined to cas_alert_events). A (operator attention) fails because the same operators slow on 4.3 units; B fails because the rate rise is on every route including the one that never passes the junction; D and E fail on shift and location share. The margin is 86 against 29, not a near tie.
- **Evidence (reproduced):**

| Item | Golden | Mine |
|---|---|---|
| VI incidents Jul-Oct 2025 / 2026 | 24 / 89 | 24 / 89 (same under UTC or AWST, +-8 h) |
| Firmware 5.0.2 on DT units | 2 to 23 Jun 2026 | 2 to 23 Jun (10:30 AWST) |
| Alerts followed by slowing, 2-23 Jun, to nearest 5 | 85 / 30 | 85.9 / 29.4 (matched, valid); 83.5 / 28.7 (NaN as not acted); 85-86 / 29 for any drop threshold 4 to 10 km/h at 4, 6 or 8 s |
| Unacted critical alerts Jul-Oct 2026 vs 2025 | more than 5x | 4,897 vs 876 = 5.6x |
| Incidents per 1,000 shifts, S-ORE>ROM / N-WST>NWD, 2025 to 2026 | 2.2 to 9.2 / 8.4 to 21.3 | same |
| Incident rate per 1,000 truck hours | not claimed | 4.3.11 0.36, 4.3.14 0.37, 5.0.2 1.43; roll-out window 0.35 before, 0.88 after |
| Trips Jul / Aug / Sep / Oct | 7,517 / 7,601 / 7,492 / 7,620 | identical with the NG-2 shadow rule (NG-2 read 2-13 s after an NG-1 read dropped, 13,088 shadows, 499 NG-2-only reads kept) |
| No tag detected | 192 / 189 / 296 / 171 | identical (blank cas_tag; consistent inside shadow pairs; 96 tags, all in the register, none removed) |
| NRP times / over +5 Jul-Oct | 53/22, 72/29, 59/23, 43/20 | identical |
| SRP times / over +5 Jul-Oct | 26/9, 19/7, 34/13, 48/23 | identical (SRP limit 40 until 17 Aug, 35 from 18 Aug; NRP 32; run joined only where the next window opens 10 s later on a shared sample above the limit; 12 s and 14 s neighbours in window are never continuous) |

  Residual forks, each shown with the two answers:
  1. Trips: 33 same-vehicle entries 16 to 27 s after the vehicle's previous north-gate read (for example 1DNZ797, 27 Jul 05:29:45 and 05:30:04, each with its own NG-2 shadow). Golden counts two trips; a solver who collapses any same-vehicle reads within 15 s gets 7,512 / 7,588 / 7,483 / 7,614. A wider vehicle window (60 s) gives 30,070 against 30,197 for the four months. Undetected counts are unaffected. Nothing in the prompt files the shadow rule; the 3 to 12 s shadow gap versus a 16 s minimum between different passes is discoverable, so this is a low-severity Gate C/E residual, not a block.
  2. Ask 3 (chart): the graded line says "Bar chart ... each bar labelled with its count"; the prompt says only "a chart of the monthly count from January 2025". Instruction-following mismatch (Gate E for a supplementary answer).
  3. SRP on 18 Aug: one run (DT425, peak 38.4) is over 35 but not over 40; effective_from is a date, so the whole day takes 35. Defensible reading, no timestamp to split the day.
- **Files/Hygiene:** PASS. 14 files; docx, pdf (2), xlsx (2), parquet (2), csv (7); 72k-row gate reads, 141k-row alert parquet, 245k-row FMS parquet; no hidden sheets, tracked changes or comments; dates coherent (notice 2 Sep, ToR 22 Sep, snapshots 31 Oct, register built 1 Nov, paper due 19 Nov). Distractors: CAS monthly report (alerts per 100 h, 38 to 41), dust PM10, road maintenance log. Minor realism note: injury lines in the register repeat boilerplate ("Task risk assessment reviewed."). The docx carries a thumbnail jpeg; not a leak. No exclusion-level finding. No public-data contamination (site data are fictional).
- **Stump power:** Moderate on the call, high on the workings. A strong solver who reads the Firmware sheet and the CAS report can reach C by a shallow route (alerts per 100 h up in June, release changed in June), so the call may be solved without the within-roll-out contrast; the wrong easy routes are B (North ramp junction 6 to 24, the notice cites it) and A (site-wide slowing rate falls from 86 to about 32 per cent in June). The three workings (shadow reader, stale FMS limit stamp, runs split across 8-second windows) and the UTC/AWST and unit-replacement joins make exact figures hard. Optional lever: none needed.
- **Stumping type:** `mechanism: decomposition_attribution (staggered roll-out contrast, same crews on both versions) with etl_conformance asks`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers (incident counts, hotspot, alert rate) are fine; the work is attributing the rise to the right driver on exposure-adjusted, unit-level evidence. Not banned.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Field analysis: incident-rate attribution with exposure (truck hours, shifts) and a staggered-adoption comparison of proximity-alert response by firmware version. Layer 1: UTC against AWST, replacement unit serials, a second gate reader shadowing the first, OCR-garbled plates, a stale current limit stamped on history, runs split over event windows. Easy route: fleet-wide trend or hotspot, giving A (operator vigilance) from the fall in slowing, or B from the North ramp junction having the most incidents. Swap test (hospital nouns) fails to preserve the alert-response and ramp-limit work, so the domain is not a backdrop.
- **Fix:** solution (reword ask 3 to "a chart of monthly counts, January 2025 to October 2026, with the 22 values readable"); optionally input_files (remove or space out the 33 same-vehicle re-reads) or prompt (nothing, per the no-data-sentence rule), author's call.

## Round 1 findings
- Unfiled units (FIX_NOW): CLOSED for the prompt text: "A trip is one vehicle entering a pit, and a time over the limit is one continuous run above it." What stays unfiled is the shadow-reader dedupe (residual fork 1 above).
- Link between 5.0.2 and the rise overclaimed: CLOSED. The recommendation now rests on the alert-response contrast (reproduced, 86 to 29 per cent in the roll-out window); the regenerated register gives 2 incidents in 5,747 hours before and 6 in 6,812 hours after within 2 to 23 June, and 0.37 against 1.43 per 1,000 hours across versions.
- Time basis: CLOSED (columns labelled AWST or UTC; register month counts unchanged under +-8 h; onset moved to AWST in step 3). "No tag detected" against the device register: CLOSED (blank cas_tag is the only reading; all 96 tags present, none removed, tag serial and fuzzy plate agree on every tagged read). Windows or samples with no GPS fix: CLOSED for graded figures (ramp counts identical whether a missing boundary sample counts as continuing or not, no run within 0.15 km/h of the +5 line; the 85 and 30 round the same with missing samples excluded or counted as not slowed; counting alerts with no FMS window as not slowed would give 80 for 4.3 units, not a defensible reading).

### Answered without moving a figure (target.zip 63cfa0bc)

- The chart line now grades a chart of the monthly count from January 2025 to October 2026 with each month's count
  readable, as the prompt asks; the golden chart is unchanged.
- Residual fork 1: a vehicle's next gate entry is at least 20 minutes after its last (asserted, 0 closer).
- Residual fork 3: no ramp window falls on its limit-change day (asserted, 0).
- All 38 figures in figures.json equal the pass-2 pack's; only the gate reads and the event windows changed.

