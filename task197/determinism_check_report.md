# Determinism review, task197 (isolated judge)

Universe: fresh unzip at `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task197_judge_pack`
(18 members). No design note, generator, pipeline file, earlier report, skill or guideline folder was opened; no
git command was run and no agent was spawned. Every figure below was recomputed from the shipped files with
pandas / sqlite3 / pdftotext / openpyxl, not checked against arithmetic shown to me. The committed blocks were
read only after the derivation below was written.

---

## Part 1: the answer the prompt and the bundle lead to (derived before reading the blocks)

**Governing text.** `standards/reserve_performance_standard_v4.pdf` clause 2 defines realised response gain as
"the active power the site delivered **in excess of the output it would have produced at that second had the
system frequency stayed inside the dead band**", divided by the deviation beyond the dead band, at the extreme
second of each qualifying episode in a settlement period the site was contracted for, averaged with equal weight,
as a percentage of contracted FCR capacity / 190 mHz. Clause 2 also fixes the qualifying tests (<= 49.920 Hz or
>= 50.080 Hz for >= 15 consecutive seconds, extreme second = lowest/highest published second, earliest on a tie)
and the two scope exclusions (periods not contracted; parts of a block withdrawn from reserve). Clause 3 fixes the
window (2026-09-21 to 2026-10-11 inclusive for the 13 Oct 2026 determination), the 90 per cent tolerance, and the
rule that the single monthly slot goes to the site furthest below contract. `operator/fcr_technical_conditions_2026.pdf`
clause 2 gives the 10 mHz dead band and the 190 mHz slope; clause 5 states the response is **additional to the
programme** and that nothing in a programme reduces it.

**Derived episode set.** `operator/system_frequency_1s_extracts.csv` (111,454 rows, 666 extracts, 2026-09-21
05:15:06Z to 2026-10-11 19:32:32Z) yields **274** qualifying under-frequency and **241** qualifying over-frequency
episodes. No episode crosses a settlement-period boundary or a four-hour block boundary (checked: 0 of 274 and
0 of 241), so episode-to-period assignment is not a live fork. Extreme seconds sit 67 to 549 s (median 80 s) after
the period boundary.

**The decisive construction.** Because the extreme second falls ~80 s after a settlement-period boundary, the
site's programme is still mid-traverse at that second. The traverse is a linear ramp from the previous period's
setpoint to the new one over a span fixed per controller, recoverable from `platform/vkf_highres_archive.sqlite`
at boundaries where the site held no reserve commitment (so no FCR response contaminates the trace). Fitting every
such boundary with |delta| > 2 MW gives a **unanimous** span per site:

| site | span (s) | unanimity |
|---|---|---|
| VKF-ZWT | 80 | 85/85 |
| VKF-OOS | 85 | 47/47 |
| VKF-KPV | 90 | 24/24 |
| VKF-NWV | 95 | 48/48 |
| VKF-DLK | 100 | 132/132 |
| VKF-HGZ | 185 | 13/13 |
| VKF-RDL | 190 | 20/20 |
| VKF-MPD | 200 | 15/15 |
| VKF-TRB | 300 | 36/38 (2 at 299) |

**Scope.** 256 block commitments in `platform/fcr_block_commitments.csv`; committed_mw equals contracted FCR
capacity in `register/asset_register.xlsx` for all 256 rows. Withdrawals: `platform/control_platform_event_log.csv`
holds 30 `reserve_unavailable` rows, 3 of which (4147, 4148, 4149) are cancelled by `COR-CANC` corrections,
leaving **27**. Every `reserve_unavailable` row is logged exactly 1.5 min after its start; on **9** rows
(4130, 4131, 4132, 4133, 4134, 4135, 4136, 4137, 4138) the `+02:00` offset on `start_local` is wrong and the stamp
is really UTC (the lag is 121.5 min if the offset is honoured, 1.5 min if it is not). Resolving by `logged_utc`
drops **5** over-frequency site-episode pairs in which the site delivered ~0 response while nominally obliged
(HGZ 2026-09-26 18:16:15Z, KPV 2026-10-03 17:31:20Z, OOS 2026-10-02 10:01:23Z, TRB 2026-10-09 07:31:21Z,
ZWT 2026-10-08 07:46:18Z); the data corroborates the correction. No under-frequency pair is withdrawn either way.
Obliged pairs: **935** under, **443** over.

**My derived answer, before reading the blocks.**

Realised gain on the programme-traverse baseline, under-frequency (raw, then to the nearest whole per cent):

| site | n | raw % | reported | below 90 |
|---|---|---|---|---|
| VKF-KPV Kampvliet | 137 | 71.961 | 72 | yes |
| VKF-RDL Reiderland | 156 | 82.986 | 83 | yes |
| VKF-HGZ Hoogezand | 157 | 87.918 | 88 | yes |
| VKF-NWV Nieuwveen | 113 | 90.940 | 91 | no |
| VKF-DLK Dollardkust | 145 | 92.967 | 93 | no |
| VKF-OOS Oosterhout | 40 | 94.939 | 95 | no |
| VKF-MPD Meppelerdiep | 33 | 96.862 | 97 | no |
| VKF-ZWT Zwartewater | 77 | 98.958 | 99 | no |
| VKF-TRB Terborgh | 77 | 100.950 | 101 | no |

**Withdraw Kampvliet (VKF-KPV) for the November 2026 delivery month at 72 per cent of contracted gain; runner-up
Reiderland (VKF-RDL) at 83 per cent; gap 11 percentage points; 3 sites outside the 90 per cent tolerance.**

Over-frequency: KPV 73.026/20, RDL 80.934/22, HGZ 86.993/152, NWV 88.918/72, DLK 91.957/20, ZWT 93.934/71,
OOS 95.869/15, TRB 97.840/71, MPD none/0.

Capacity hours (clause 4), raw: block 1 held 542.000 / short 18.000; block 2 1151.000 / 17.000; block 3
1407.100 / 20.900; block 4 352.900 / 7.100; block 5 1615.500 / 26.500; block 6 244.200 / 7.800. Every withdrawal
falls wholly inside a committed block (no unallocated withdrawal hours).

Imbalance energies (clause 5), raw MWh: OOS 9.3071 / 22.1866; ZWT 16.3023 / 49.4891; HGZ 8.2121 / 18.6087;
KPV 10.9189 / 21.9163; MPD 9.8023 / 16.0957; NWV 10.9074 / 27.9912; TRB 15.3073 / 22.1026; DLK 22.0112 / 46.7990;
RDL 11.6197 / 17.4036. Portfolio raw 114.3883 / 242.5927 -> **114.4 / 242.6** rounded once.

## Part 2: every option I had to enumerate where the shipped text is silent, and what each computes to

| # | silence | options enumerated | what each gives | closed by |
|---|---|---|---|---|
| 1 | clause 2's counterfactual "output it would have produced had the frequency stayed inside the dead band" | (a) programme traverse trajectory; (b) undisturbed level (power at the last pre-episode second inside the dead band); (c) period setpoint; (d) previous period's setpoint held flat; (e) ramp spread over the whole 900 s period | (a) KPV 71.96 lowest; (b) ZWT 76.84 lowest, KPV 93.45; (c) RDL 57.63 lowest, KPV 68.37; (d) ZWT 71.08 lowest; (e) ZWT 73.79 lowest | clause 2 ("at that second") plus technical conditions clause 5 ("additional to the programme ... nothing in a unit's programme reduces the response owed"): only (a) removes the site's own programme movement. (b)-(e) each credit or debit a site with its own traverse. **This is the decisive step and it changes the answer: Zwartewater or Reiderland instead of Kampvliet.** |
| 2 | how the traverse span is recovered | boundaries with no *qualifying* episode (the submission's own wording) vs boundaries where the site held **no reserve commitment** | the looser rule is contaminated by sub-threshold droop response and returns ~70-72 s for NWV (NWV under 91.52 -> 92, over 81.0); the commitment-free rule returns 95 s unanimously (NWV 90.94 -> 91, over 88.9 -> 89) | the contaminated fits are self-rejecting (modelled ramp fraction exceeds 1.000, which a linear traverse cannot), and the commitment-free boundaries are unanimous for all nine sites. Forced, but the submission's step 3 wording understates it. |
| 3 | `start_local` offsets in the event log | honour `+02:00` on all rows vs resolve by the uniform 1.5-min `logged_utc` lag | honouring the offset keeps 5 extra over pairs: HGZ 153 @ 86.43, KPV 21 @ 69.51, OOS 16 @ 89.92, TRB 72 @ 96.47, ZWT 72 @ 92.63 (under-frequency unchanged) | `logged_utc` partitions cleanly (21 rows at 1.5 min, 9 at 121.5 min) and the five disputed seconds show ~0 delivered response, which only the withdrawal explains. Forced. |
| 4 | which interval a `metered_volumes_15min` stamp belongs to | interval-**end** stamping vs interval-**start** stamping (the file's own `settlement_period` column says start: 00:15 is labelled period 2) | end-stamp: 114.4 / 242.6 portfolio, residual rms vs programme 0.021-0.067 MWh, coverage exactly 2016 periods = 09-21 P1 .. 10-11 P96; start-stamp: 944.5 / 1054.1 portfolio, rms 0.154-0.514, coverage shifted by one period | the data: end-stamping cuts the residual ~10x for all nine sites (corr 0.9957-0.9996 vs 0.874-0.970) and aligns the file exactly to the clause 3 window. The `settlement_period` column is off by one, which is Layer-1 mess, not a fork the answer can rest on. `market/imbalance_prices_15min.csv` is start-stamped, which is what makes the trap live. |
| 5 | the kWh row block (DLK, 2016 of 18,144 rows) | convert per interval; convert the metered sum only; convert the above/below totals; no conversion | per interval: DLK 22.0 / 46.8; totals-converted: 638.0 / 1984.9; unconverted: 638,011 / 1,984,850 | only the per-interval conversion is dimensionally coherent against a programme in MW, and it is the only one that matches the site's 10 MW contract / 25 MW connection. Forced. |
| 6 | the grid-loss factor (settled volumes are 1.0042x own meters at the two 150 kV sites) | not applied; applied to the metered series; applied to the totals | not applied: ZWT 16.3 / 49.5, DLK 22.0 / 46.8, portfolio 114.4 / 242.6; applied: ZWT 17.9 / 47.8, DLK 20.4 / 50.8, portfolio 114.4 / 245.0 | clause 5 names "the net volume its own settlement meters register ... **before any adjustment the system operator applies at settlement**". Forced; the three settlement statements are a distractor. |
| 7 | the rounding path on clause 4 and clause 5 quantities | round each interval/segment to 1 dp then sum, vs sum unrounded and round once | per-interval rounding: portfolio 56.2 / 129.3 (vs 114.4 / 242.6); capacity hours unaffected (every block total is an exact tenth) | clause 5 says "summed over those periods and **rounded once at the end**"; clause 4 says "summed over the window's delivery dates and reported ... to one decimal place". Forced. |
| 8 | which frequency file defines episodes | 1 s extracts vs `system_frequency_minute_summary.csv` | the minute summary carries only a per-minute minimum and cannot establish 15 consecutive seconds; it also shows 17 minutes at or below 49.920 Hz with no 1 s extract and disagrees with the 1 s data by up to 0.0355 Hz on the overlapping minutes | clause 2 needs second resolution, so the 1 s file is the only admissible source. The 17 uncovered minutes are a coherence wrinkle (technical conditions say 1 s is published for every deviation beyond 75 mHz) but no episode can be built from them, so nothing is actionable. |
| 9 | the metering-point switch at Oosterhout | register EAN only (…398201, data from 2026-10-01 02:15 local) vs stitching the retired EAN (…312447, to 2026-10-01 02:00 local) | register-only: OOS covers 1,048 of 2,016 periods and its energies are understated; stitched: 9.3 / 22.2 | the register's own Notes sheet ("shows the code in force at the pull date; replaced codes are kept in the metering history") plus event 4112 `MET-CHG`. Forced. |
| 10 | the duplicated high-resolution recording after the HGZ archive restore (event 4114) | dedupe vs count rows | recording 2820 duplicates 1611 byte-for-byte (156 duplicate (site, second) rows, 0 with a differing value); naive row counting gives HGZ 153 over pairs instead of 152 | values identical, so no figure forks; only the count does, and `recording` shows one duplicated `start_utc`. |

## Part 3: gate table

| gate | call | one line |
|---|---|---|
| A, solution correct | **PASS**, with one SOLUTION_WRONG figure | 38 of 39 committed figures reproduced exactly; step 6's "Kampvliet at 94" on the undisturbed-level basis reproduces as 93.454 under every construction of that basis I could build (4 dead-band variants plus an any-recording variant: all 93.454). |
| B, decisive facts present | **PASS** | Measure, thresholds, dead band, slope, window, tolerance, decision rule, capacity-hours formula and imbalance-energy formula all in the two PDFs; contracted capacities in the xlsx `Sites` sheet; the action vocabulary ("withdraw", "re-prequalification", "tolerance", "realised response gain") is in the shipped standard and technical conditions; "Kampvliet" is in the register. "Traverse" and "undisturbed" appear in no shipped file, but they label derived quantities, not the committed action. |
| C, uniquely forced | **PASS** | Ten silences enumerated above; each closed by shipped text or decisively by the data. Main margin is 11.03 pp (71.96 vs 82.99) and survives a +/-10 per cent error in every traverse span (KPV 69.30 to 74.40, RDL 80.95 to 84.66, order and "3 below tolerance" unchanged). |
| D, difficulty analytical not semantic | **PASS** | The split among good answers is the counterfactual baseline, i.e. the estimand, not the reading of a prompt word; the standard states the counterfactual in substantive terms and the easy route is a recognised industry proxy, not a misreading. |
| E, prompt unambiguous on the decision | **PASS** | 991 characters, one paragraph, one site demanded, every graded figure carries unit and rounding in the asking sentence, no hedge available, no method prescribed, no leak of the baseline question. |
| F, stump power | **STRONG** | Nothing in the prompt mentions programme, ramp or baseline. The natural route (pre-episode power as the undisturbed level) is a real FCR prequalification convention and files **Zwartewater at 77**; the period-setpoint route files **Reiderland at 58**. Both are specific wrong answers, not coin flips. Secondary devices (event-log offset, interval-end stamping, the kWh block, the retired EAN) bite the asks. |
| G, stumping type | **PASS** | `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Every reported number in the pack is correct: the frequency, the power, the programme and the step-test records are all fine. Nothing has to be caught as wrong; the difficulty is selecting the baseline the standard's counterfactual actually names and reconstructing it. On perfectly clean data the task still stumps, so the clean-data test passes. |
| H, three rules | **PASS** | `domain: pass`, `layers: pass`, `decisive_step: analytical`. |

### Gate G line, in full

`mechanism: method_or_model_selection` | `stumping_family: analytical_non_defect` |
`surface_read_dependency: no` | `sole_data_defect: no`. The FINE-numbers method carrying the difficulty is
baseline/estimand selection on honest data: the realised gain must be measured against the programme traverse the
controller was executing at the extreme second, and the two plausible-but-wrong baselines (the undisturbed level,
the period setpoint) are each internally consistent, each computable from correct reported inputs, and each names a
different site. No reported figure in the pack is misleading and no planted defect decides anything.

### Gate H line, in full

`domain: pass`, `layers: pass`, `decisive_step: analytical`. H1: the deciding quantity is a droop gain against a
contracted frequency-response characteristic, measured on 1 s telemetry with the market programme removed, which
is the reserve desk's own core calculation; the swap test fails immediately (substitute "hospital" or "visits" and
the 190 mHz slope, the 10 mHz dead band and the 15-consecutive-second episode test have nothing to attach to).
H2, layer 1: interval-end stamping against a `settlement_period` column that is off by one, one meter reporting
kWh among eight in MWh, a metering point replaced mid-window with only the new EAN in the register, nine event-log
start stamps carrying a wrong `+02:00` offset, a cancelled-withdrawal correction chain, a duplicated recording
after an archive restore, preliminary and amended October settlement issues carrying a 0.42 per cent grid-loss
adjustment, and a minute summary that disagrees with the 1 s extracts. H2, layer 2: which counterfactual the
realised gain is measured against. H3, the easy route: a strong analyst who cleaned all of that and read every
clause correctly takes each site's recorded power at the last pre-episode second inside the dead band as "the
output it would have produced", averages the ratios, and files **Zwartewater at 77 per cent** (Kampvliet reads 93
and sits inside tolerance on that basis); taking the period setpoint instead files **Reiderland at 58 per cent**.
Both are wrong answers reached without misreading a field or a rule, so H3 is analytical.

## Part 4: figures I could not reproduce

| block | figure as submitted | what I got | load-bearing? |
|---|---|---|---|
| Step 6 | "the undisturbed level ... puts Zwartewater at 77 per cent and **Kampvliet at 94**" | Zwartewater 76.840 -> 77 (agrees); Kampvliet **93.454 -> 93** under all five constructions of the undisturbed level I built | No. It is narrative support for a rejected route, appears in no graded deliverable, and the rejection holds under every construction (Kampvliet stays above tolerance and Zwartewater remains the furthest below on that basis). |

Everything else reproduced: all 9 under-frequency gains and counts, all 9 over-frequency gains and counts
(including Meppelerdiep "none"), the 935 obliged pairs, the 90 s and 300 s traverse spans, the "3 sites below
tolerance" count, all 12 capacity-hour figures, all 18 site energies and both portfolio totals.

## Part 5: bin-edge distances for every graded figure

Distances are expressed in units of the rounding unit its asking sentence states (1 per cent for gains,
0.1 MWh for energies); 0.500 means the raw value sits dead centre in its bin. **Nothing is within 0.3.**

Under-frequency gains: KPV 0.461, RDL 0.486, HGZ 0.418, NWV 0.440, DLK 0.467, OOS 0.439, MPD 0.362, ZWT 0.458,
TRB 0.450. Over-frequency gains: KPV 0.474, RDL 0.434, HGZ 0.493, NWV 0.418, DLK 0.457, ZWT 0.434, OOS 0.369,
TRB 0.340. Gap: 11.025 pp, and 83 - 72 = 11, so the gap is 11 whether taken as the rounded difference or the
rounded raw difference. Tolerance line: the nearest site to 90.0 is Nieuwveen at 90.940, clear by 0.94 pp.
Capacity hours: all twelve figures are exact tenths (0.500). Energies, tightest first: RDL above 11.6197 (0.303),
KPV above 10.9189 (0.311), KPV below 21.9163 (0.337), OOS below 22.1866 (0.366), HGZ above 8.2121 (0.379),
portfolio above 114.3883 (0.383), DLK above 22.0112 (0.388), ZWT below 49.4891 (0.391), NWV below 27.9912 (0.412),
HGZ below 18.6087 (0.413), NWV above 10.9074 (0.426), portfolio below 242.5927 (0.427), TRB above 15.3073 (0.427),
OOS above 9.3071 (0.429), MPD below 16.0957 (0.457), RDL below 17.4036 (0.464), TRB below 22.1026 (0.474),
ZWT above 16.3023 (0.477), MPD above 9.8023 (0.477), DLK below 46.7990 (0.490). The two tightest, Reiderland's and
Kampvliet's above-programme energies, clear the 0.3 trip wire by 0.003 and 0.011 of a rounding unit respectively:
worth noting, not a finding.

## Part 6: the reported total that is not the sum of its printed rows

Portfolio above programme is **114.4** MWh while the nine printed rows sum to **114.3**. The shipped text forces
this: clause 5 requires the portfolio quantity to be "summed over those periods and rounded once at the end", so
it is 114.3883 rounded once, not a sum of nine already-rounded rows. The below-programme column is 242.6 either
way (raw 242.5927; rounded rows sum to 242.6). The submission states the reason in the deliverable, correctly.

## Part 7: files and hygiene

**PASS.** 18 files, 4 formats (13 csv, 3 pdf, 1 xlsx, 1 sqlite), csv-leaning but not a monoculture; the 24 MB
sqlite (2,820 recordings, 563,213 one-second rows) and the 111,454-row frequency extract clear the volume bar.
Every file reads as a system export or a signed governing document: a daily commitment file, a platform event log
with corrections and a superseded-event pointer, an asset-register extract with a Notes sheet about retired
metering codes, two overlapping October settlement issues, a group availability statement that explicitly declines
to attribute performance to units. No README, no "synthetic"/"generated"/"benchmark" disclosure, no tool banner, no
solver-facing language (checked by grep across all plain files and by `pdftotext` on all three PDFs). Temporal
coherence holds: register pulled 2026-10-12, last event 2026-10-11, meters end at period 96 of 2026-10-11, the
standard names the 13 Oct 2026 determination, nothing postdates the snapshot. Distractors present and relevant but
unused: imbalance prices, the capacity auction results, the three settlement statements (grid-loss adjusted and
daily, both disqualifying under clause 5), the minute summary, the group availability PDF, and
`prequalification_records.csv`. No finding is exclusion-level.

Two notes, neither exclusion-level, neither a send-back:
1. `prequalification_records.csv` is a wrong-basis route that ranks the sites and gets the decision wrong
   (measured/contracted step-test gain puts Reiderland lowest at 98.5 per cent and nobody outside tolerance). It is
   ruled out by shipped fact (the tests are witnessed step tests from 2017-2025; technical conditions clause 4 and
   standard clause 1 put the review on delivered response over the window, and four sites carry post-test
   controller-change declarations with no measured gain). No `metadata.json` is in the pack, so I could not confirm
   the distractor is declared there; if it is not, declare it.
2. The minute summary shows 17 minutes at or below 49.920 Hz and 13 at or above 50.080 Hz with no corresponding
   1 s extract, and disagrees with the 1 s data by up to 0.0355 Hz where they overlap, while the technical
   conditions promise 1 s publication for every deviation beyond 75 mHz. Nothing is computable from those minutes,
   so no figure moves; it is a coherence wrinkle in a distractor file.

## Part 8: verdict

- **Verdict: DETERMINISTIC (SOLUTION_WRONG)**
- **Disposition: FIX_NOW.** Regenerate step 6's Kampvliet figure on the undisturbed-level basis from 94 to 93, and
  restate step 3's recovery criterion as "at the settlement-period boundaries where the site held no reserve
  commitment" rather than "holding no qualifying episode", because the looser wording selects boundaries
  contaminated by sub-threshold droop response and returns ~72 s for Nieuwveen instead of 95 s. Both edits are
  solution-block text; the analytic surface solvers work against stays byte-identical, so **no model rerun is
  required**.
- **Fix location: solution.**
- **Why:** the decision is forced. Clause 2's counterfactual plus technical conditions clause 5 admit only the
  programme-traverse baseline; the traverse span is recovered unanimously per site from commitment-free boundaries;
  on that baseline Kampvliet is 71.96 per cent against Reiderland's 82.99, a lead of 11.03 pp that survives a
  +/-10 per cent span error, and clause 3 sends the single slot to the site furthest below contract. The only
  defect is one narrative figure attached to a route the solution rejects, which the Gate A carve-out keeps inside
  a DETERMINISTIC verdict.
