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
