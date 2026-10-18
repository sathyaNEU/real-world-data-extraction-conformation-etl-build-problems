# task197 determinism review (re-judge after repair)

**Order kept:** yes. The derivation was written to disk (`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task197_derivation.md`) before the graded blocks were opened. Nothing else outside the brief and the pack was read.

**Verdict:** DETERMINISTIC
**Disposition:** APPROVE. All 39 committed figures reproduce (nothing left to repair), and the four repair items check out as stated. No model rerun.

## Gates

| Gate | Result | Line |
|---|---|---|
| A | PASS | Every graded figure reproduced independently: 17 gains and 17 counts (nine under, eight over, MPD none), 12 capacity figures, 20 energy figures; Kampvliet 72 per cent (137), Reiderland 83, gap 11 (unrounded 11.03); 3 sites below 90; 935 under-frequency site-episode pairs. |
| B | PASS | Every decisive fact is in a shipped file. Three items are recovered from data, not from text: the per-site ramp span (DPDT recordings in the sqlite), the meter stamp being interval END (lag +15 min correlation 0.9995 against 0.970 at lag 0), and nine event-log start_local clocks that are really UTC (logged_utc minus clock = 90 s, against 7,290 s on the label). Each has a data check that closes it. |
| C | PASS | Two surviving alternatives were stress-tested and neither is defensible: setpoint baseline (RDL 57.6 lowest) and last-in-band baseline (ZWT 76.8 lowest). Both are named and ruled out in the write-up, and the literal "output it would have produced at that second" plus the shipped DPDT recordings contradict them. Within the ramp-aware route the call is stable (tie-break, ratio of means, fitted against round spans, UTC against label reading of events: same whole-per-cent values; margin 11 points). |
| D | PASS | Difficulty is the counterfactual baseline, not a word. |
| E | PASS | One site, its gain, runner-up and gap are pinned; rounding stated once. |
| F | STRONG | The easy route (period setpoint) files RDL, the undisturbed-level route files ZWT; the right answer needs the ramp-aware counterfactual from the DPDT recordings. |
| G | PASS | See line below. |
| H | PASS | See line below. |

**Gate G:** `mechanism: method_or_model_selection` (choice of counterfactual baseline on honest data), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is overturned; the setpoint and last-in-band readings are both arithmetically correct on their own basis and wrong as the counterfactual; the ramp physics is present on clean data, so the task still stumps with the Layer 1 mess (UTC clocks, kWh file, end stamps, EAN change) removed.

**Gate H:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to preserve the task (a response gain against a linear droop characteristic at the extreme second, a ramp-aware counterfactual output and a re-prequalification slot are reserve-provider work). Layer 1: UTC clocks labelled +02:00, interval-end stamps, kWh against MWh, replaced metering point, preliminary and amended statements; Layer 2: estimating what the unit would have produced mid-programme-ramp. A strong analyst who cleaned everything and read every rule can still file RDL (57.6 per cent, setpoint basis) or ZWT (76.8 per cent, last-in-band basis) by taking the easy baseline.

## The four repair items, literal results

1. **Rejected bases (blocks 1 and 3): true.** Recomputed over 935 under-frequency pairs. Period setpoint basis: lowest is Reiderland at 57.6 per cent (next Kampvliet 68.4, Terborgh 76.7, Hoogezand 74.8, Meppelerdiep 78.3). Undisturbed level (recorded power at the last second inside the 10 mHz dead band before the episode): lowest is Zwartewater at 76.8 per cent (next Oosterhout 83.4). The lowest site is unchanged under the withdrawal reading (UTC clocks, label clocks, no exclusion) and under inclusive and strict dead-band tests. Kampvliet is not lowest on either basis (second lowest on setpoint at 68.4; 93.5 per cent on last-in-band, well above the lowest), so "neither basis names Kampvliet" is correct. Narrative checks: Reiderland's traverse is 190 s and the extreme second falls on average 42 per cent through it; Zwartewater's block 3 programme falls from about 12.8 MW (06 to 08) to about -9.4 MW (12) and 83 per cent of its episode periods have a falling setpoint, so "unwinding a morning discharge" holds. No percentage for either basis is printed anywhere in the blocks, nothing is said about Kampvliet's own figure on them.
2. **Traverse spans: unique.** Criterion "boundary at which the site held no reserve commitment" read as the period beginning at the boundary uncommitted: 40 to 156 boundaries per site, spans 99.97 (DLK), 185.04 (HGZ), 89.99 (KPV), 200.04 (MPD), 95.04 (NWV), 84.99 (OOS), 189.97 (RDL), 299.97 (TRB), 80.04 (ZWT) seconds, spread under 2.5 s. KPV 90 and TRB 300 reproduce. Competing readings: previous period uncommitted gives the same medians but admits one disturbed DLK recording (43.3 s); all boundaries at once gives medians within 0.3 s of these (NWV 94.79, OOS 84.85) but individual disturbed values (NWV 3.6 s, KPV 40.4 s); none changes a rounded span or any whole-per-cent gain. Only the wording "boundaries at which the site held no reserve commitment" is slightly loose about which of the two periods at the boundary is meant.
3. **One-second sentence: literally true, one soft spot.** Minute summary covers all 30,240 minutes (every day). Of 1,217 minutes beyond 75 mHz, 896 have full one-second cover, 167 partial, 154 none; of 926 beyond 80 mHz, 30 have none. All 515 qualifying episodes sit in extracts and none touches an extract edge. The 154 uncovered minutes are not covered by "sustained" (only 1 has a minute mean beyond 75 mHz; 14 sit next to another uncovered beyond-75 minute), so the sentence is conditional and not false. The summary alone cannot exclude a 15 s run inside any of those 30 minutes (all 30 are arithmetically feasible), but no site FREQ-DEV recording lies outside an extract (1,756 of 1,756 overlap one) and only 1 of the 30 minutes has any site recording at all (a DPDT), so nothing in the files points at a missing episode. No change needed. Also noted: 6 full-cover minutes where the summary min or max disagrees with the extract (over-frequency side, up to 0.04 Hz), not used by any figure.
4. **Rounding edges (distance of the unrounded value to the nearest tie, in units of the stated rounding; 0 is on a tie, 0.5 is centred):** gains 0.34 to 0.49 (tightest: TRB over 97.84 at 0.34, MPD under 96.86 at 0.36, OOS over 95.87 at 0.37); energies 0.30 to 0.49 (tightest: RDL above 11.6197 at 0.30, KPV above 10.9189 at 0.31, KPV below 21.9164 at 0.34); capacity figures are exact multiples of 0.1. No figure sits on a tie; none prints as a rounded whole number except the capacity values that are exact (542.0, 18.0, 17.0, 1151.0). The only non-obvious convention is the portfolio energy row: unrounded sums 114.388 and 242.593, the column of rounded rows sums to 114.3 and 242.6, which the write-up already says.

## Figures that did not reproduce

None. (A discrepancy in my own notes, 925 against 935 under-frequency pairs, was my arithmetic slip; 145+157+137+33+113+40+156+77+77 = 935.)

## Other

- Tolerance flags: Nieuwveen 90.94 per cent is above 90 by 0.94 points and holds under every variant tried (ratio of means 90.85).
- Hygiene not assessed beyond what the checks above touched (18 members, csv, pdf, xlsx, sqlite).
- Fix location: none.
