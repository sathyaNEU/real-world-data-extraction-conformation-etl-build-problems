# determinism-check report, task229, 2026-10-11

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Pass 1 was one isolated judge thread on the loop-2 cut. It had only the prompt, the ten shipped files and the four graded blocks.

Every committed answer reproduces to the decimal from the shipped files. MDS-STD-114 r3 pins every operational choice but one:
- the 06:00 AEST cut-off (3.4, 3.5);
- read health as the mean over installations (4.2);
- the running-build and assessed-installation rules (3.6, 3.7);
- the 99.50 reference and the three-error limit (5.1 to 5.3);
- sample standard deviations (7).

The open choice is how to estimate the standard error, and the data settle it. Four collector-nights each cost the day to 77 to 100 per cent of the installations behind the collector:
- EMC-8306 on 5 October;
- EMC-8631 on 8 October;
- EMC-2773 and EMC-7873 on 11 October.

No other node-day loses more than 3 installations. Treating installations as independent is therefore a pseudo-replication error, not an equally licensed reading. Every collector-aware estimator fires on EM3.12.1, EM3.10.9 and PX5.2.7 and holds the other five.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fire list | EM3.12.1, EM3.10.9, PX5.2.7 | EM3.12.1, EM3.10.9, PX5.2.7 | yes |
| Hold list | PX5.3.0, EM3.12.0, EM3.11.4, PX5.3.1, EM3.12.2 | same | yes |
| EM3.12.1 read health, SE, limit, distance | 98.92, 0.07, 99.30, -0.38 | 98.92, 0.07, 99.30, -0.38 (695 installations, 11 nodes) | yes |
| EM3.10.9 read health, SE, limit, distance | 98.06, 0.37, 98.40, -0.34 | 98.06, 0.37, 98.40, -0.34 (423, 53) | yes |
| PX5.2.7 read health, SE, limit, distance | 98.73, 0.18, 98.96, -0.23 | 98.73, 0.18, 98.96, -0.23 (728, 14) | yes |
| PX5.3.0 read health, SE, limit, distance | 99.49, 0.05, 99.36, +0.13 | 99.49, 0.05, 99.36, +0.13 (789, 14) | yes |
| EM3.12.0 read health, SE, limit, distance | 98.21, 0.57, 97.80, +0.41 | 98.21, 0.57, 97.80, +0.41 (2,242, 44) | yes |
| EM3.11.4 read health, SE, limit, distance | 99.57, 0.15, 99.05, +0.52 | 99.57, 0.15, 99.05, +0.52 (1,662, 44) | yes |
| PX5.3.1 read health, SE, limit, distance | 98.98, 1.05, 96.35, +2.63 | 98.98, 1.05, 96.35, +2.63 (37, 3) | yes |
| EM3.12.2 read health, SE, limit, distance | 97.87, 1.83, 94.01, +3.86 | 97.87, 1.83, 94.01, +3.86 (153, 7) | yes |
| Wave 8 onto EM3.12.2 | 1,274 | 1,274 (1,472 rows, 1,451 meters, less 22 removed and those already on the target) | yes |
| Wave 8 onto PX5.3.1 | 109 | 109 | yes |
| Substitution load | 1,846 | 423 + 695 + 728 = 1,846 | yes |
| Critical components 1 to 5 | as block 2 | all five, consistent across blocks | yes |

The judge rebuilt the chain itself:
- reads held at the cut-off: 518 keys have more than one delivery before it, and 589 stream-days have none and count zero;
- expected intervals from the register, with all 12,366 streams matched;
- meters joined on serials padded to eight digits;
- running builds from the head-end history, with 275 re-ingested events dropped;
- 6,729 assessed installations;
- CR1 over `comms_parent`, which reproduces to four decimals.

## Competing answers that survived
None counted as equally valid.

- **The designed trap.** The independent-installation error (sample SD over root n) fires EM3.12.0 and EM3.12.2. That gives 0 Wave 8 moves onto EM3.12.2 and a substitution load of 5,379. The judge adjudicated it a valid analytical stump, not a semantic fork. Nine collector-aware estimators all give the golden list:
  - design-based: CR1, CR0, the cluster jackknife, the cluster bootstrap, node-by-day and day clusters, and the average-size design effect;
  - model-based: random-intercept GLS and node means.

  EM3.12.0's lowest collector-aware SE is 0.47, above the 0.43 below which it would fire. EM3.12.2's is 1.69, above its 0.54.
- **Residual, not licensed.** A hybrid (the simple mean with an exchangeable random-intercept variance) gives EM3.10.9 an SE of 0.65 against the 0.48 it needs, so it holds EM3.10.9. The full random-intercept fit (97.44, SE 0.46) and every design-based estimator fire it.

  The main thread reproduced both figures with a moment estimator, and `generator/checks.py` now asserts them. The design note (`## Stump or fork`) records why the hybrid is not a licensed reading: the model charges the small nodes' spread to the large nodes by size squared, though the large nodes' means sit near the build's.
- **Rules the standard pins.** Ignoring any of these flips the call, and each is filed:
  - counting late deliveries (3.5);
  - pooling reads (4.2);
  - skipping the in-week exclusion (3.7).
- **Inert choices.** None of these change the call:
  - AEDT for the cut-off or week;
  - how failed activations and duplicate events are handled;
  - first rather than latest delivery;
  - planned interruptions;
  - dropping Q1 or keeping only E1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in the pack | 10 or more | 10 | yes |
| Distinct formats | 3 or more | 5 (pdf, xlsx, csv, json, md) | yes |
| Largest file | 25,000 rows or a database | `mdm_interval_receipts_20261005_20261011.csv`, 95,140 rows | yes |
| Declared distractors | 2 or more, unlabelled, unused, relevant | `extract_log_20261012.csv`, `dnsp_planned_interruptions_oct2026.xlsx`; asserted unused by the golden; no file named for its role | yes |
| Distractor answering a graded quantity | ruled out by a shipped fact | neither answers one (the census, which sums to the load once the call is known, is declared a cross-check) | yes |
| Deliverables requested | 1 to 3 | 2 (`wave8_read_health_alerts.json`, `read_health_by_build_wk41.png`) | yes |
| Asks multi-dimensional | not stacked lookups | lists, eight four-figure records in order, Wave 8 moves under the call, the load, the chart | yes |
| Golden deliverables present | every one named | both in `golden/` | yes |
| Units and rounding stated | every ask | per cent to two decimals; counts whole | yes |
| Prompt shape and rubric floor | identifiable; 25 or more criteria | shape 10 (scorecard against thresholds); about 51 criteria | yes |
| Realism | no LLM tells; goldens read as work product | judge hygiene PASS; its three container nits fixed (below) | yes |

## Gate G reconciliation
The judge's flags are `analytical_non_defect`, `surface_read_dependency: no` and `sole_data_defect: no`. They match the design note's `## Gate G` exactly.

The judge's mechanism label, `method_or_model_selection`, is its vocabulary for the move the note files as signal_vs_noise_or_hold with statistical_rigor support: choosing the unit of the error on honest data. The judge's stump-power paragraph calls it a signal-versus-noise call. No mismatch.

The judge names no declared distractor as the surface read. `metadata.json` declares the extract log and the planned-interruption notifications.

## Stump power (Gate F)
One trap does the work: the collector-clustered standard error. The standard's section 7 wording and the textbook reflex both point to s over root n, and the prompt never mentions collectors.

A model that applies every written rule but treats installations as independent fires five builds. It then reports 0 Wave 8 moves onto EM3.12.2 and a 5,379 substitution load, so it gets the main answer and asks 1 to 3 wrong.

The other traps are written into MDS-STD-114 or the schedule's notes, so they add execution load but not stump power. No contrasting model responses were supplied, so the empirical bar is unchecked and goes to live testing.

The judge named one lever in case live runs cluster routinely: hide the topology behind a join the prompt does not mention. It is not applied, because it changes the data and needs a rerun.

## Findings, ranked
1. **Grading tolerance (optional, no rerun).** A limit or distance worked from the two-decimal SE moves by 0.01 for EM3.12.1, EM3.10.9, PX5.3.0 and EM3.12.0.
   - Applied: `submission.md` step 6 now says the limits and distances come from the unrounded error and names those four as moving by 0.01 with no call changing.
2. **Recommendation wording (optional, no rerun).** The recommendation called EM3.12.0 a deciding margin, but the thinnest hold is PX5.3.0 at +0.13.
   - Applied: the recommendation now names PX5.2.7 (0.23 below) and PX5.3.0 (0.13 above).
3. **Container metadata (optional, in-house).** The PDF named Microsoft Word as creator over a ReportLab structure. The workbooks carried openpyxl's layout and one shared modified stamp.
   - Applied in the generator: the records system is named as creator, and the workbooks are laid out the way Excel saves them, each with its own UTC stamps.
   - The rebuilt pack was compared with the judged cut:
     - text files byte-identical;
     - PDF text identical and parsing clean;
     - every workbook cell value, type, number format, header style and pane identical (empty-string cells unstored, still empty);
     - LibreOffice opens all three workbooks;
     - 120 assertions, the verifier and two byte-identical builds green.
   - No graded figure, rung or document text moved, so no fresh round and no second pass.
4. **Cross-batch duplicate check not run by the judge**, because its allow-list barred the batch folders. This is covered by:
   - stage 5: the heart check (WARN answered) and the adjudicated pre-flight (CLEAN);
   - the stage 8 surface screen against task228's pack: 0 promoted, pair surface 0.08.

## Next action for the author
Ship: cut `target.zip` from the final rebuild and set task229 to `shipped` in the root `START_HERE.md`.
