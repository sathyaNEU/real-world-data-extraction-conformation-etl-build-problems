# task160 determinism check (architecture 2)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 2fd81ca5 | NOT_DETERMINISTIC on supplementary 3 only (order kept; main call forced; F good; G PASS; H PASS) | FIX_NOW | Schedule B 2.3 files that a queue task carries every high-severity alert overridden on its order at that signing and signing it off signs off each review; the prompt pins the shift table to all of Quillfield's adult wards; CR-2291's date agrees with the register; a new ask device (the queue platform's clock change on 3 August) carries the shift ask |
| 2 | 5586cd17 | DETERMINISTIC (order kept; F strong; G PASS; H PASS) | APPROVE | none |

---

# Determinism check, round 1 (2026-11-01): NOT_DETERMINISTIC on supplementary 3 only, FIX_NOW; order kept; main call forced; Gate F good; Gate G PASS; Gate H PASS

Isolated thread, Sonnet at medium effort, on target.zip 2fd81ca5.

# Verdict, task160 (r1)

Order kept: yes. derivation.md was written to disk from the prompt and the 12 bundle files before graded_blocks.md was opened. Cross-batch fingerprint against delivered tasks: not performed (no access outside this folder).

- **Verdict:** NOT_DETERMINISTIC (supplementary answer 3 only; the main call and supplementary answer 2 are forced and reproduce).
- **Disposition:** FIX_NOW. Pin in the bundle what one signed-off review is (a queue-export note, or one export row per overridden alert) and say in the prompt whether the shift-by-month table covers all adult wards or only the going-live wards. The main call, ladder, background log and every other graded figure stay byte-identical, so no rerun of the stump is needed. Escalate to SEND_BACK if the author will not touch the export.
- **Why:** Supplementary 3 (562/417/143, 504/415/130, 532/417/124) holds only under a convention no file states: that one queue task covers every overridden alert on its order. The queue lists 3,006 tasks, one per order, and carries none of the 250 second or third alerts (all 248 two-alert orders have only the first alert as a task). A literal count of signed-off tasks by Eastern month and shift gives 519/377/129, 463/391/117, 494/380/120 (2,990). Schedule B 2.1 ("one overridden alert is one review") supports the golden only if the absent alerts are assumed signed off inside the same task. Taxonomy: competing_defensible_answer (Gates C and E). A second, smaller fork sits in the same ask: the sentence does not say whether "the reviews they signed off" covers all 18 wards (golden) or the 15 going-live wards (Jul 439/327/113, Aug 392/331/98, Sep 428/330/94).
- **Evidence (recomputed from the bundle):**

| Item | Golden | My value | Reproduced |
|---|---|---|---|
| Net change, alert basis | +296, about +300 | +292 per patient-day, +296 to +297 per admission, so +300 | yes |
| Gross QT added / DUP-driven loss | 491 / 195 | 484 / 192 (patient-day), 491 / 195 (admissions) | yes |
| Pilot response rates (7W, 5E, 8N, deduplicated) | QT 58 per cent overridden, DUP 49 per cent removed | 57.6 per cent, 49.0 per cent | yes |
| Desk hours, 15 wards | 28, 21, 25, 14, 24, 16, 17, 18, 15, 11, 41, 36, 36, 22, 26 | identical; total 349.97 hours | yes |
| Shift by month (supp. 3) | 562/417/143 etc. | 519/377/129 etc. on literal task count; the golden figures reproduce only by weighting each task by its order's overridden alerts | no, convention only |

  - **Main call is forced.** Schedule B 4.3 fixes the estimand: the 15 units not yet live, with the change live and prescribers answering "as they have on any unit where it already runs", against the same units without it.
    - The pilot-unit history shows that when the MSP26 alert is answered "Order removed", every other alert on that order is also removed. No history alert has a removed order as its interacting order.
    - So go-live adds QT overrides and deletes same-order reviews. It also deletes later DDI_SEVERE overrides whose interacting order is a would-be-removed duplicate-opioid order.
    - The join from the background log's order_id to the history's order_id and interacting_order_id is available in the files: 108 own-order and 363 cascade overridden alerts.
  - **Margin is clean.** The result is about 292 to 297; the 250 boundary is about 3 sigma away on removal-rate sampling noise, and 2026Q3-only rates give 270 to 305.
  - **Residual fork F1 on the main call, mild.** If "review" is read as the desk's queue task (one per order) rather than Schedule B 2.1's overridden alert, the net becomes about +390, which rounds to +400. 2.1 is explicit, so 300 is the literal answer, but the queue granularity contradicts 2.1 and the golden's own step 7 treats a task as several reviews. The same pin closes this.
  - **Wrong routes:** QT only gives +480, so 500. Own-order loss without the cascade gives +430, so 400. Extrapolating the live-unit alert rates (QT 31.9 per 1,000 patient-days against 25.8 in the background log, DUP 44.9 against 58.9) misstates the gross because the case mix differs.
  - **Layer 1 mess handled by the golden:**
    - 507 duplicate history rows removed; unit names remapped across the 9 Nov 2025 rename.
    - Alert_dttm is Eastern and the queue and background log are UTC (offset 4 hours on all 146 joined and all 3,006 queue rows).
    - Poc_location disagrees with the alert department on 30 per cent of rows, so ward hours must key on the alert history (Schedule B 3.2). Grouping by poc_location moves 4N, 4S, 6E, 6W, 9E, 9W, 10N and 10S.
    - handle_min on the 137 second-session rows is elapsed time since first claim. A handle_min sum gives 391 hours; the contract's claim-to-close definition gives 350.
- **Files/Hygiene:** PASS with one minor flag. 12 files; formats csv (6), xlsx (3), pdf (2), docx (1); largest file 48,434 rows. Distractors: PumpGuardrail events and the RPh interventions workbook (relevant, unused). Minor temporal incoherence: the change request is dated 21 Oct 2026 but attaches a rule register "as of 26 Oct" and data to 25 Oct. Fix by redating, which does not touch the stump. No authoring or provenance disclosure and no public-data contamination found. Nothing exclusion-level.
- **Stump power:** Good. The easy routes are QT-only (+500) and own-order loss without the cascade (+400); the correct +300 needs the prescriber-response counterfactual and the join through interacting_order_id. A strong model that reads Schedule B 4.3 and the pilot-unit data may find the DUP removal but plausibly misses the downstream DDI_SEVERE cascade or double-counts it. Risk: a model that gets 300 yet counts queue tasks in the asks is penalized on a convention (see Why).
- **Stumping type:** `mechanism: forecasting` (counterfactual workload forecast with pilot-unit response rates), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The background log and the history are correct as reported; the difficulty is modelling what prescribers do with the new alerts. On clean data it would still stump. Passes Gate G.
- **Three rules:** `domain: pass`, `layers: pass` (Layer 1: quarter-pull duplicates, unit rename, UTC against Eastern, poc against alert department, cumulative handle_min; Layer 2: net counterfactual workload change), `decisive_step: analytical`. The field's own analysis is a pharmacy-informatics alert-burden forecast using pilot-unit override and removal rates and the effect of removed orders on downstream alerts. The easy route is adding the QT alerts from the background log to get +500 (or +400 with only same-order losses). The swap test fails for a generic substitution, because the removal-and-cascade mechanism is specific to clinical decision support. Not planted, not data semantics, not rule application.
- **Fix:**
  - **input_files:** add the missing definition to the queue export. Either add a column or header note that one task covers all overridden alerts on its order, or emit one row per overridden alert. Redate the change request or the attachments.
  - **prompt:** state whether the shift-by-month table covers all adult wards or the going-live wards only.
  - The golden for supplementary 3 then stays valid under the all-wards, alert-weighted reading. Do not alter the background log, history or census.


---

# Determinism check, round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate F strong; Gate G PASS; Gate H PASS

The re-judge after round 1's shift-ask repair, on target.zip 5586cd17. Isolated thread, Sonnet at medium effort.

# Verdict (task160, r2)

- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.
- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no repair needed; no solution-block defect found, no rerun).
- **Why:** The net figure is forced by Schedule B 2.1-2.3/4.3 and the shipped data: the 15 non-live wards' background-log events, answered at the live wards' rates (QT removed 517/1218 = 42.4 pct, DUP_OPIOID removed 837/1708 = 49.0 pct), with removal also deleting the same order's reviews and the later DDI_SEVERE overrides that name the removed order as interacting order (0 of 34,067 interacting links ever point at a removed order). Every scaling basis I tried (patient days, admissions, per ward, aggregate, plan-to-plan, time only) lands +285 to +297, so the nearest 100 is +300 with about 35 reviews of margin to the 250 line. The per-ward desk hours and the nine shift-by-month counts all reproduce once the queue clock and the department source are read as the data forces.

## Evidence (recomputed from target/)
| Item | My value | Golden | Source |
|---|---|---|---|
| Added QT reviews, 16-week base | 1008 x 0.5755 = 580 (golden drops 3 baseline-removed orders: 578) | 578 | BackgroundLog, MedAlertHistory (live-ward rates) |
| Lost reviews, base | X 52.4 + cascade 177.9 = 230.3 | 230 | History High/Overridden by order_id and by interacting_order_id |
| Net, base | +350.2 | | |
| Net, 13 plan weeks | +291.7 (patient days), +296.7 (admissions, 8,287 over 9,765), +284.5 (time only) | 296 / +300 | Volume_Plan weeks 2027-01-04 to 03-29, UnitCensus |
| Desk hours, 15 wards | 10N 36, 10S 22, 11N 17, 11S 18, 12N 16, 2N 24, 3E 15, 3W 11, 4N 28, 4S 21, 5W 26, 6E 41, 6W 36, 9E 25, 9W 14 (sum 349.965 = 350) | identical | sum of closed-claimed over every session, alert-fired department |
| Signed-off reviews (alerts) Jul/Aug/Sep | Day 562/504/532, Evening 417/415/417, Night 143/130/124 (total 3244) | identical | queue task x alert count on order, Eastern sign-off |

Two things must be read correctly, both forced by the data: (a) the queue's "Z" stamps are true UTC only through 3 Aug about 07:00; afterward they equal the history's Eastern clock (join offset of queue received time minus alert_dttm is exactly 4.0 h before, 0.0 h after, no task straddles; the history's diurnal profile is unchanged across the switch, so the history is Eastern throughout). Treating all stamps as UTC gives Aug 512/245/294 and Sep 503/244/324, wrong. (b) poc_location swaps within five twin-ward pairs from 20 Jul; Schedule B 3.2 files "department in which the alert fired", the history department is csn-consistent, so per-ward rows follow history (poc-based gives 10N 29, 4N 22, etc.; totals unchanged at 350).

Competing answers tried and eliminated: +500 (QT only, no response), about +400 to +450 (own-order losses but no cascade), pooled removal rate +265 (still rounds to +300), tasks instead of alerts (closed by 2.1 "one overridden alert is one review"). Desk time by handle_min gives 381, wrong (session 2 handle_min is cumulative from first claim); closed-claimed is filed by 3.2.

## Findings (each in one line, none changes the verdict)
1. Gate C/B, low: "a removed order is never active, so later alerts naming it do not fire" is not stated in a document; it is forced by Bulletin 3 / register note ("orders active at that moment") plus 0 of 34,067 history links to a removed order. Route without it gives +400 to +500; this is the analytic step, not an ambiguity.
2. Gate B/C, low-moderate: the 3 Aug queue clock change is documented in no shipped file; recoverable only by joining alert_ref to the history and checking the hour profile. Unique and reproducible, but the prompt's asks (not the main call) ride on it; acceptable as Layer 1 mess.
3. Gate C/E, low: per-ward desk-hour rows depend on choosing history department over queue poc_location for ten twin wards; closed by Schedule B 3.2 literally, totals unaffected.
4. Gate A, none: no solution block is wrong. Minor wording: step 4's "3410" alert base and 42 pct own-order QT removal are consistent with the 230 loss I reproduce.

## Files/Hygiene: PASS
12 files, formats csv (6), pdf (2), xlsx (3), docx (1); one file of 48,434 rows (9.99 MB). Distractors present: PumpGuardrail_Events (pump overrides, different system) and RPh_Interventions (pharmacist time not on override queue). Documents carry plausible creators/dates, no authoring or benchmark language, timeline coherent (extracts to 25 Oct, CR 26 Oct, Schedule B signed 18 Jun effective 1 Jul). 507 exact duplicate history rows at quarter-pull boundaries and renamed departments are realistic mess. Nothing exclusion-level. No public-data contamination identified.

## Stump power (Gate F)
Strong. A capable analyst who cleans the data and reads Schedule B takes background QT events x override rate (about +500) or nets only same-order losses (about +400); only modelling the response of removal on later alerts via interacting_order_id gives +300. Asks add an independent layer: the Z-label clock switch and the department swap each move 9 of 9 shift cells or 10 of 15 ward rows if missed.

## Stumping type (Gate G)
`mechanism: forecasting` (counterfactual from background-mode evaluation plus observed pilot-unit response), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Numbers shipped are fine; the difficulty is projecting the response (removal and its downstream suppression) the background log does not show, and it survives on clean data.

## Three rules (Gate H)
`domain: pass`, `layers: pass` (Layer 1: duplicate quarterly pulls, renamed departments, mixed clock, swapped point-of-care codes, session-cumulative handle_min; Layer 2: counterfactual review volume under observed prescriber response including downstream alert suppression), `decisive_step: analytical`. Swap test: replacing "override reviews" with another field's count breaks the pharmacy-alert-response model, which is the field's own forecasting work; the easy route (background log count x override rate, +500, or no cascade, +400) is wrong for an analyst who read every rule correctly.

## Fix
none (prompt, input_files and solution stand). Optional: none required.

