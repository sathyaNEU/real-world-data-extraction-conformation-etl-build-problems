# determinism-check report, task180, 2026-10-11

Pass 1. Invoked by the `determinism-check` skill's rehearsal rule at `/build` stage 7, after the solver round passed. Judge standard: `guidelines/determinism_judge_system_prompt.md` as it stands today (v3 plus the 2026-10-10 Gate H block), applied verbatim.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

FIX_NOW comes from one hygiene finding: templated non-decisional rows in `maintenance_log_2019-2026.xlsx`. There are also two optional solution-block rewordings. No figure, trap or decisional record changes, and no model rerun is needed.

## Why
ES-DGA-02 5.2 gives the three windows only to code 3 transformers with a fault in the main tank, in descending severity, and the shipped data force which of the seven code 3 units qualify. At Dunsandel T1 and Leeston T2, main-tank acetylene rises in lockstep with their in-oil arcing tap changers' operations (r 0.998 and 0.995 on per-interval increments, with an elapsed-time term near zero) while hydrogen stays flat (twelve-month C2H2/H2 9.8 and 8.2). That is diverter-compartment oil, not a main-tank fault. Rolleston T2's acetylene also tracks operations (r 0.999), but it arrives with hydrogen: H2 rose from a pre-onset baseline of about 33 ppm to 54 ppm after the March 2025 onset in a sealed unit (ratio 0.64), so the arc gas is made in the main tank. Southbridge T2 (vacuum) gasses with hydrogen and independently of operations (r -0.07). The slate is Southbridge T2 8.07, Rolleston T2 4.98 and Coalgate T1 4.73, with Springston T2 (4.43) the first left out, 6.3 per cent below.

## Recomputation ledger
Every value below was recomputed from the fresh bundle copy, not read from the submission. Scripts and outputs are in `/tmp/determinism-check-task180-20261011T071748Z-2f319fab/` (`judge_coding.csv`, `judge_tapops.csv`, `judge_rs.csv`, `verdict.md`).

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Main recommendation | SBG-T2, RLS-T2, CGT-T1, in that order | same (5.2 order by severity among code 3 with a main-tank fault) | yes |
| Code 3 set (CC1, CC4, step 1) | DSL-T1 9.64, LST-T2 8.07, SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45 | identical; SBG-T2 and LST-T2 tie exactly (8.067385) | yes |
| Fleet coding (step 1) | 44 coded on the September 2026 round, 7 code 3 | 33 code 1, 4 code 2, 7 code 3; every latest sample is Sept 2026 | yes |
| Acetylene increments vs tap operations, r (CC2, step 2) | DSL-T1 0.998, LST-T2 0.995, RLS-T2 0.999, SBG-T2 -0.07 | 0.998, 0.995, 0.999, -0.073 (each from its acetylene onset; R² at least 0.99 with a time term near 0 for the first three) | yes |
| Twelve-month C2H2/H2 (CC2, step 2) | 9.8, 8.2, 0.64, 0.51 | 9.800, 8.200, 0.6375, 0.5125 | yes |
| DSL-T1, LST-T2 stay code 3 with no main-tank fault (CC3) | code 3, no fault | code 3 confirmed; H2 flat (5 to 10 ppm) through acetylene rises of about 22 and 13 ppm | yes |
| Code 3 with a main-tank fault, by severity (CC4, step 4) | 8.07, 4.98, 4.73, 4.43, 3.45 | identical | yes |
| Tap changers past interval (step 5) | 7 of 27 | 7 of 27 (5 on operations above 60,000; GLT-T2 and SHF-T1 on more than 7 years) | yes |
| Above 30 per cent RS (step 6) | 6 | 6 | yes |
| Slate (docx ask 1): SBG-T2 code / severity / gas | 3 / 8.07 / acetylene | 3 / 8.0674 / C2H2 | yes |
| Slate (docx ask 1): RLS-T2 code / severity / gas | 3 / 4.98 / acetylene | 3 / 4.9773 / C2H2 | yes |
| Slate (docx ask 1): CGT-T1 code / severity / gas | 3 / 4.73 / ethylene | 3 / 4.7276 / C2H4 | yes |
| Tap ops (docx ask 2): DSL-T1 | 87,322, past yes | 87,322, past yes (ops); last service 2021-05-18 | yes |
| Tap ops (docx ask 2): DYL-T2 | 87,029, past yes | 87,029, past yes (ops); last service 2021-03-16 | yes |
| Tap ops (docx ask 2): GLT-T1 | 75,013, past yes | 75,013, past yes (ops); last service 2021-11-30 | yes |
| Tap ops (docx ask 2): TPR-T2 | 64,224, past yes | 64,224, past yes (ops); last service 2022-05-10 | yes |
| Tap ops (docx ask 2): LST-T1 | 61,972, past yes | 61,972, past yes (ops); last service 2022-08-16 | yes |
| Tap ops (docx ask 2): GLT-T2 | 29,695, past yes | 29,695, past yes (time); last service 2019-04-09 | yes |
| Tap ops (docx ask 2): SHF-T1 | 23,553, past yes | 23,553, past yes (time); last service 2019-08-20 | yes |
| Tap ops (docx ask 2): CGT-T2 | 57,551, past no | 57,551, past no; last service 2023-03-28 | yes |
| Tap ops (docx ask 2): LST-T2 | 54,294, past no | 54,294, past no; last service 2023-05-16 | yes |
| Tap ops (docx ask 2): RLS-T2 | 49,897, past no | 49,897, past no; last service 2023-05-23 | yes |
| Tap ops (docx ask 2): WDN-T1 | 38,209, past no | 38,209, past no; last service 2021-10-19 | yes |
| Tap ops (docx ask 2): DYL-T1 | 32,511, past no | 32,511, past no; last service 2021-11-09 | yes |
| Tap ops (docx ask 2): SBG-T1 | 32,019, past no | 32,019, past no; last service 2022-10-11 | yes |
| Tap ops (docx ask 2): WML-T1 | 31,680, past no | 31,680, past no; last service 2023-02-21 | yes |
| Tap ops (docx ask 2): CGT-T1 | 27,923, past no | 27,923, past no; last service 2022-10-04 | yes |
| Tap ops (docx ask 2): DFD-T1 | 21,895, past no | 21,895, past no; last service 2024-02-20 | yes |
| Tap ops (docx ask 2): WDS-T1 | 21,319, past no | 21,319, past no; last service 2025-06-24 | yes |
| Tap ops (docx ask 2): DSL-T2 | 20,955, past no | 20,955, past no; last service 2025-04-08 | yes |
| Tap ops (docx ask 2): GDL-T1 | 20,915, past no | 20,915, past no; last service 2023-11-21 | yes |
| Tap ops (docx ask 2): LDB-T1 | 20,592, past no | 20,592, past no; last service 2023-04-18 | yes |
| Tap ops (docx ask 2): LDB-T2 | 16,890, past no | 16,890, past no; last service 2025-09-02 | yes |
| Tap ops (docx ask 2): LIN-T1 | 16,064, past no | 16,064, past no; last service 2025-11-04 | yes |
| Tap ops (docx ask 2): SPF-T1 | 14,842, past no | 14,842, past no; last service 2024-05-14 | yes |
| Tap ops (docx ask 2): SPF-T2 | 11,034, past no | 11,034, past no; last service 2026-02-17 | yes |
| Tap ops (docx ask 2): LIN-T2 | 10,079, past no | 10,079, past no; last service 2026-03-03 | yes |
| Tap ops (docx ask 2): KRW-T1 | 6,837, past no | 6,837, past no; last service 2026-05-19 | yes |
| Tap ops (docx ask 2): HOR-T1 | 3,909, past no | 3,909, past no; last service 2026-07-14 | yes |
| RS > 30 % (docx ask 3): SHF-T1 | 36.1 | 36.116 (T 28.1 SCADA UTC hour) | yes |
| RS > 30 % (docx ask 3): GDL-T1 | 34.9 | 34.919 (T 30.6 SCADA UTC hour) | yes |
| RS > 30 % (docx ask 3): WDN-T1 | 34.1 | 34.078 (T 22.5 label) | yes |
| RS > 30 % (docx ask 3): DYL-T1 | 33.1 | 33.071 (T 24.3 SCADA UTC hour) | yes |
| RS > 30 % (docx ask 3): TPR-T2 | 31.7 | 31.721 (T 19.1 SCADA UTC hour) | yes |
| RS > 30 % (docx ask 3): SPF-T1 | 31.5 | 31.505 (T 26.5 label) | yes |
| CSV row BNM-T1 (code, sev, slate, ops, RS) | 1, 0.38, no, none, 8.8 | 1, 0.38, no, none, 8.8 | yes |
| CSV row BNM-T2 (code, sev, slate, ops, RS) | 1, 0.21, no, none, 7.0 | 1, 0.21, no, none, 7.0 | yes |
| CSV row CGT-T1 (code, sev, slate, ops, RS) | 3, 4.73, yes, 27,923, 22.8 | 3, 4.73, yes, 27,923, 22.8 | yes |
| CSV row CGT-T2 (code, sev, slate, ops, RS) | 1, 0.28, no, 57,551, 28.2 | 1, 0.28, no, 57,551, 28.2 | yes |
| CSV row DFD-T1 (code, sev, slate, ops, RS) | 3, 3.45, no, 21,895, 19.6 | 3, 3.45, no, 21,895, 19.6 | yes |
| CSV row DFD-T2 (code, sev, slate, ops, RS) | 1, 0.16, no, none, 11.7 | 1, 0.16, no, none, 11.7 | yes |
| CSV row DSL-T1 (code, sev, slate, ops, RS) | 3, 9.64, no, 87,322, 21.5 | 3, 9.64, no, 87,322, 21.5 | yes |
| CSV row DSL-T2 (code, sev, slate, ops, RS) | 1, 0.33, no, 20,955, 17.0 | 1, 0.33, no, 20,955, 17.0 | yes |
| CSV row DYL-T1 (code, sev, slate, ops, RS) | 1, 0.29, no, 32,511, 33.1 | 1, 0.29, no, 32,511, 33.1 | yes |
| CSV row DYL-T2 (code, sev, slate, ops, RS) | 1, 0.46, no, 87,029, 23.9 | 1, 0.46, no, 87,029, 23.9 | yes |
| CSV row GDL-T1 (code, sev, slate, ops, RS) | 1, 0.34, no, 20,915, 34.9 | 1, 0.34, no, 20,915, 34.9 | yes |
| CSV row GDL-T2 (code, sev, slate, ops, RS) | 1, 0.21, no, none, 20.9 | 1, 0.21, no, none, 20.9 | yes |
| CSV row GLT-T1 (code, sev, slate, ops, RS) | 1, 0.19, no, 75,013, 19.7 | 1, 0.19, no, 75,013, 19.7 | yes |
| CSV row GLT-T2 (code, sev, slate, ops, RS) | 2, 0.30, no, 29,695, 18.2 | 2, 0.30, no, 29,695, 18.2 | yes |
| CSV row HOR-T1 (code, sev, slate, ops, RS) | 1, 0.49, no, 3,909, 27.0 | 1, 0.49, no, 3,909, 27.0 | yes |
| CSV row HOR-T2 (code, sev, slate, ops, RS) | 1, 0.25, no, none, 15.6 | 1, 0.25, no, none, 15.6 | yes |
| CSV row KRW-T1 (code, sev, slate, ops, RS) | 1, 0.49, no, 6,837, 28.5 | 1, 0.49, no, 6,837, 28.5 | yes |
| CSV row KRW-T2 (code, sev, slate, ops, RS) | 1, 0.27, no, none, 11.0 | 1, 0.27, no, none, 11.0 | yes |
| CSV row LDB-T1 (code, sev, slate, ops, RS) | 2, 0.33, no, 20,592, 24.4 | 2, 0.33, no, 20,592, 24.4 | yes |
| CSV row LDB-T2 (code, sev, slate, ops, RS) | 1, 0.49, no, 16,890, 21.1 | 1, 0.49, no, 16,890, 21.1 | yes |
| CSV row LIN-T1 (code, sev, slate, ops, RS) | 1, 0.14, no, 16,064, 19.0 | 1, 0.14, no, 16,064, 19.0 | yes |
| CSV row LIN-T2 (code, sev, slate, ops, RS) | 1, 0.22, no, 10,079, 27.3 | 1, 0.22, no, 10,079, 27.3 | yes |
| CSV row LST-T1 (code, sev, slate, ops, RS) | 1, 0.31, no, 61,972, 22.2 | 1, 0.31, no, 61,972, 22.2 | yes |
| CSV row LST-T2 (code, sev, slate, ops, RS) | 3, 8.07, no, 54,294, 18.2 | 3, 8.07, no, 54,294, 18.2 | yes |
| CSV row PRB-T1 (code, sev, slate, ops, RS) | 1, 0.42, no, none, 8.9 | 1, 0.42, no, none, 8.9 | yes |
| CSV row PRB-T2 (code, sev, slate, ops, RS) | 1, 0.49, no, none, 10.0 | 1, 0.49, no, none, 10.0 | yes |
| CSV row RLS-T1 (code, sev, slate, ops, RS) | 1, 0.45, no, none, 8.0 | 1, 0.45, no, none, 8.0 | yes |
| CSV row RLS-T2 (code, sev, slate, ops, RS) | 3, 4.98, yes, 49,897, 12.5 | 3, 4.98, yes, 49,897, 12.5 | yes |
| CSV row SBG-T1 (code, sev, slate, ops, RS) | 1, 0.15, no, 32,019, 26.7 | 1, 0.15, no, 32,019, 26.7 | yes |
| CSV row SBG-T2 (code, sev, slate, ops, RS) | 3, 8.07, yes, none, 13.9 | 3, 8.07, yes, none, 13.9 | yes |
| CSV row SHF-T1 (code, sev, slate, ops, RS) | 1, 0.21, no, 23,553, 36.1 | 1, 0.21, no, 23,553, 36.1 | yes |
| CSV row SHF-T2 (code, sev, slate, ops, RS) | 1, 0.39, no, none, 16.9 | 1, 0.39, no, none, 16.9 | yes |
| CSV row SPF-T1 (code, sev, slate, ops, RS) | 2, 0.24, no, 14,842, 31.5 | 2, 0.24, no, 14,842, 31.5 | yes |
| CSV row SPF-T2 (code, sev, slate, ops, RS) | 1, 0.30, no, 11,034, 22.4 | 1, 0.30, no, 11,034, 22.4 | yes |
| CSV row SPN-T1 (code, sev, slate, ops, RS) | 1, 0.11, no, none, 12.1 | 1, 0.11, no, none, 12.1 | yes |
| CSV row SPN-T2 (code, sev, slate, ops, RS) | 3, 4.43, no, none, 11.0 | 3, 4.43, no, none, 11.0 | yes |
| CSV row TPR-T1 (code, sev, slate, ops, RS) | 1, 0.49, no, none, 17.9 | 1, 0.49, no, none, 17.9 | yes |
| CSV row TPR-T2 (code, sev, slate, ops, RS) | 1, 0.26, no, 64,224, 31.7 | 1, 0.26, no, 64,224, 31.7 | yes |
| CSV row WDN-T1 (code, sev, slate, ops, RS) | 1, 0.28, no, 38,209, 34.1 | 1, 0.28, no, 38,209, 34.1 | yes |
| CSV row WDN-T2 (code, sev, slate, ops, RS) | 1, 0.32, no, none, 14.5 | 1, 0.32, no, none, 14.5 | yes |
| CSV row WDS-T1 (code, sev, slate, ops, RS) | 1, 0.23, no, 21,319, 14.7 | 1, 0.23, no, 21,319, 14.7 | yes |
| CSV row WDS-T2 (code, sev, slate, ops, RS) | 1, 0.27, no, none, 10.7 | 1, 0.27, no, none, 10.7 | yes |
| CSV row WML-T1 (code, sev, slate, ops, RS) | 2, 1.39, no, 31,680, 16.1 | 2, 1.39, no, 31,680, 16.1 | yes |
| CSV row WML-T2 (code, sev, slate, ops, RS) | 1, 0.39, no, none, 19.0 | 1, 0.39, no, none, 19.0 | yes |

All 80 supplementary rows above reproduce: 3 slate rows, 27 tap-changer rows, 6 wet-transformer rows, and 44 CSV rows covering 220 values. The golden `dga_fleet_review.csv` also matches the recomputation on all 44 rows.

## Competing answers that survived
None. The judge tested these rivals and each one failed:

- **Rank every code 3 by severity:** DSL-T1, then LST-T2 and SBG-T2 tied at 8.07. Closed by std 5.1 and 5.2 (a fault in the main tank) and by the tap-linked, hydrogen-free acetylene at DSL-T1 and LST-T2.
- **Drop every unit whose acetylene tracks operations:** SBG-T2, CGT-T1, SPN-T2. Closed by RLS-T2's hydrogen rising with its acetylene from the same onset. SBG-T2 is the in-pack control: a free-breathing unit with a main-tank arc that kept its hydrogen. This closure rests on DGA domain knowledge (see Findings 1).
- **Screen C2H2/H2 on latest levels** (DSL-T1 2.5, LST-T2 1.6, RLS-T2 0.17), which could keep LST-T2. Closed because LST-T2's hydrogen never moved (5 to 8 ppm since 2021) while its acetylene went from below detection to 12.9; the level ratio only reflects the hydrogen background.
- **Exclude CGT-T1 as tap-linked** (raw ethylene-vs-operations r 0.66). Closed because the correlation is an interval-length artifact. On rates, CGT-T1 gives -0.11 and DFD-T1 -0.44.

Supplementary forks that move graded values, each closed:

| Fork | Values moved | What closes it |
|---|---|---|
| Register `oltc_last_service` instead of the maintenance log | 8 rows of ask 2 | std 6.1 and annex B |
| First issue instead of latest issue | KRW-T1 enters ask 3 at 43.0; SPF-T1 leaves at 28.6 | std 3.4 |
| Parquet read as NZ local time | 15 RS values; DYL-T1 and TPR-T2 leave ask 3 | Data structure only (see below) |
| Rollover vs replacement | ops counts | the notes' "five digits" plus the log's replacement records |
| Pre-2021 services | GLT-T2, SHF-T1 counts | the log's counter readings |

The UTC reading of the parquet is not stated in any file. It is closed by the data's structure: the series starts at 2020-12-31 11:00 (00:00 NZDT) and ends at the hour before the run date, both DST-change days have 24 rows, and the stamped evening peak falls at 06:00 in winter and 05:00 in summer.

These forks have no effect: LOD at 0, half or full; rewind vs manufacture year; fractional vs calendar days; a 365-day base; mid-year age; and the service-day counter baseline (every service-day increment is 0).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in pack | 10 or more | 11 | yes |
| Distinct formats | 3 or more | 6 (csv x3, xlsx x3, pdf x2, parquet, md, txt) | yes |
| Large file | 25,000+ rows or a large database | `scada_top_oil_hourly_2021-2026.parquet` 2,232,384 rows; `scada_tap_counters_daily_2021-2026.csv` 93,060 | yes |
| Distractors declared | 2 or more in `metadata.json`; none labelled in `target/` | `protection_relay_events_2025-2026.csv`, `thermal_imaging_survey_2026.pdf`; no file name or content labels either | yes |
| Distractors unused but relevant | same world, something to weigh | Relay events: through-fault history at the same substations, unused (no T2 incomer event near either SBG-T2 gas step; fault-current ceilings uniform near 2,390 A). Thermal survey: the same 22 substations, switchgear only, transformers stated out of scope, unused | yes |
| Distractor that answers a graded quantity | reproduces, ruled out by a shipped fact | neither answers the decision or any graded quantity | n/a |
| Deliverable count | 1 to 3 | 2 (`inspection_slate_2027-28.docx`, `dga_fleet_review.csv`) | yes |
| Format family | none required | not assessed | n/a |
| Multi-dimensional asks | not stacked lookups | slate (3 rows x order, code, severity, gas), tap table (27 x count, flag), wet table (6), CSV (44 x 5) | yes |
| Goldens present | each named deliverable | both present; golden CSV matches on all 44 rows; the docx carries all three asks | yes |
| Units and rounding stated | every ask | severity to 2 dp (prompt, std 4.4), RS to 1 dp in docx ask 3, integer counts; the CSV ask gives no precision for RS | partial |
| Prompt shape and 25-criteria floor | identifiable; 25 or more | ranked list under a cap (metadata shape 01) plus two tables and a 44-row CSV; well over 25 criteria reachable | yes |
| Realism | nothing reads as generated; goldens read as real | Goldens read as a real board paper and register. `maintenance_log_2019-2026.xlsx` annual-inspection text is templated (see Findings 2) | partial (FIX_NOW) |

## Gate G and Gate H reconciliation
**Gate G.** The judge classified the task as `decomposition_attribution`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The pack ships no scorecard, code list or stakeholder conclusion to reject, and every code and severity stands. The stump is attributing a correctly measured acetylene rise to its source, and it survives the clean-data test.

The design note was not read, because this invocation forbids it. The judge's line is therefore compared with the card only.

- The `stump` field in `pipeline.json` puts the trap at "reading main-tank acetylene as a main-tank fault, when its increments track each unit's tap-change counts and its ratio to hydrogen is the tap changer's".
- `metadata.json` and the Tags give the objective as "Anomaly Detection & Diagnostics ... each anomalous gas attributed to its source before ranking".

Both describe the same decisive step on fine numbers, so there is no shape mismatch on the evidence available. The card carries no mechanism label or flags. Before the real review, the author should confirm that the design note's mechanism line and its three flags agree with the judge's line. A label other than `decomposition_attribution` would be a naming difference rather than a shape difference, because both sides name the same step. The judge did not name either declared distractor as the read that carries the task.

**Gate H.** The judge returned domain pass, layers pass, decisive_step analytical. The card's `three_rules` gives domain "pass (DGA fault-gas source diagnosis; the swap breaks it)", layers "pass", decisive_step "analytical", and analyst_test "tracking-only attribution drops RLS-T2 and files SBG-T2, CGT-T1, SPN-T2". All three fields match. The judge named the card's analyst route as one of its two easy routes; the other is the plain severity ranking, which files DSL-T1, LST-T2 and SBG-T2.

## Stump power (Gate F)
Good. The easy route is to code the fleet correctly (already substantial Layer 1 work) and rank code 3 by severity, which files DSL-T1, LST-T2 and SBG-T2. A strong model that treats code 3 as a main-tank fault lands there. A model that does spot tap-changer contamination meets a second trap: dropping every tap-linked unit loses RLS-T2.

The judge named one mild too-easy signal: the board's tap-operations table makes the tap-changer join salient. No lever is needed.

## Findings, ranked
1. **Watch item: the most likely point of challenge in the real review. No file change.** The RLS-T2 against DSL-T1/LST-T2 split rests on DGA domain knowledge that no shipped file states: arc gas in oil carries hydrogen, and diverter-compartment oil reaching the main tank is acetylene-rich and hydrogen-poor.
   - ES-DGA-02 s.2 cites IEC 60599 without its operative terms.
   - No input uses "selector", "leak" or "C2H2/H2".
   - RLS-T2's hydrogen increments do not track operations interval by interval (rate r 0.07; the expected per-interval rise is below the 1 ppm reporting step), so the inference rides on the co-onset level trend (about 33 ppm before onset to 54 ppm latest).

   The judge credited this as the field's own method, given the stark in-pack contrasts. A strict reviewer could press it as Gate B external_dependency. Do not add the rule to the pack, because that would pre-disarm the stump. Have the contrasts ready instead: hydrogen flat at DSL-T1 and LST-T2 through acetylene rises of about 22 and 13 ppm; RLS-T2 hydrogen up from about 33 ppm to 54 ppm after its March 2025 onset; SBG-T2 as the free-breathing control.
2. **FIX_NOW, hygiene, in-house: `maintenance_log_2019-2026.xlsx`.**
   - The 176 annual inspections share one sentence plus five recurring remarks. "T2 fan 3 noisy bearing, raised WO." appears 25 times at 16 sites and is never followed up. "T1 oil level gauge glass cracked, replace at next outage." appears 28 times at 16 sites and is never replaced.
   - Burnham's battery bank is "replaced (110 V, 8 years old)" in both WO41615 (Nov 2019) and WO42969 (May 2022).
   - Change, in the generator: vary or drop the recurring remarks, add the follow-up orders or drop "raised WO", and correct WO42969. Keep every OLTC SERVICE, OLTC INSPECTION, BREATHER and OIL PROCESSING row byte-identical.
3. **FIX_NOW, solution wording, optional: `submission.md`.**
   - In the Final Recommendation, change "both are code 3 as reported" to "as coded". Nothing in the pack reports a code, and the phrase reads as a surface-read rejection to a Gate G reviewer.
   - In step 2, restate "(the tap selector works in the main tank)" as "arc gas made in the main-tank oil at each tap change", since no shipped file uses "selector".
   - The golden docx carries both phrasings ("as reported"; "most likely at the tap selector"); the same optional rewording applies there.
4. **Rubric guidance, no file change.**
   - Grade the CSV's relative saturation at one decimal. Ask 3 states that precision; the CSV ask does not.
   - For CGT-T1's "gas behind it", accept ethylene, which sets the severity, and do not penalise also naming methane, which also meets the code 3 test.
5. **Metadata, optional.**
   - The PDF Producer fields name the companies rather than authoring software.
   - `mobile_substation_bookings_2027-28.xlsx` carries the extract's 2026-10-16 06:40 creation stamp, although it is a copied document "as booked at 9 October 2026".
6. **Not run in this pass:** the judge's cross-batch fingerprint. The isolation allow-list excludes other task folders; the clone audit covers this.

## Next action for the author
Make the Findings 2 change in the generator: vary or drop the five recurring annual-inspection remarks and correct WO42969's battery age. Then rebuild twice and confirm that the build is byte-identical and that every OLTC, breather and oil-processing row and every graded figure is unchanged.

## Process notes
- **No `Agent` tool in this runtime.** A tool search for `Agent` and `Task` found neither, so the one judge pass ran in the orchestrator's own context, under the same allow-list and with no retries.
- **What the judge had read before the verdict:** the agent definition, the `determinism-check` SKILL.md, the judge system prompt (verbatim), `prompt.md`, and `submission.md` lines 9 to 123 (the four graded blocks). The Tags block was read only after `verdict.md` was written.
- **What the judging read:** only the fresh copy at `/tmp/determinism-check-task180-20261011T071748Z-2f319fab/target/`, which is byte-identical to `task180/target/` (there is no `target.zip`). No web or server tools were used and no subagent was spawned.
- **Post-verdict reads:** for the spec gates and the reconciliation only, `metadata.json`, the Tags block, the `stump`, `three_rules` and stage fields of `pipeline.json` (no other fields), and `golden/`.
- **Not read:** the design note, the generator, the solver rounds, any verifier, the clone and leak reports, and `START_HERE.md`.
- **Writes:** this pass wrote nothing in the task folder. The harness refused the subagent's report write, so this content was handed back for the caller to save. No commit or push.
