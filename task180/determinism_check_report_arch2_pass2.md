# determinism-check report, task180, 2026-10-11

Pass 2, on the hardened (loop-2) pack. Invoked by the `determinism-check` skill's rehearsal rule at `/build` stage 7, after the solver round passed. The judge standard is `guidelines/determinism_judge_system_prompt.md` as it stands today (v3 plus the 2026-10-10 Gate H block), applied verbatim. The judging ran in-line because this runtime has no `Agent` tool; see Process notes.

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

SEND_BACK because the repair regenerates Leeston T2's main-tank hydrogen series and breaks its exact severity tie with Southbridge T2. Both change what solvers see, so a solver rerun is required.

## Why
Gate C fails on the main recommendation. The governing label is `competing_defensible_answer`. The two answers keyed to the slate inherit the failure: `inspection_slate_2027-28.docx` ask 1 (the three) and the "on the slate" column of `dga_fleet_review.csv`.

The slate depends on whether Leeston T2's (LST-T2) acetylene "comes with none of its own" hydrogen.
- The submission gets "none" by treating all of LST-T2's post-onset hydrogen as a straight-line continuation of its pre-acetylene radiator pace.
- The submission's own method, applied to hydrogen, gives the opposite. That method sets increments between samples against SCADA tap operations. In the 2026 monthly samples, LST-T2's hydrogen increments track its tap operations: r 0.81, permutation p 0.005. Rolleston T2's (RLS-T2) do not: r 0.14.

A competent analyst who keeps LST-T2 files Southbridge T2 (SBG-T2) and LST-T2, exactly tied at 8.0674, then RLS-T2, and drops Coalgate T1 (CGT-T1).

## Recomputation ledger
Every value was recomputed from the fresh copy of `target/`, not accepted from the blocks.

**Main recommendation, critical components and steps**

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Final recommendation | SBG-T2, RLS-T2, CGT-T1, in that order | Follows from the ranking below only if LST-T2 is excluded. That exclusion is contested (see the next section). | **not forced** |
| Seven code 3 units (step 1, CC1) | DSL-T1 9.64, LST-T2 8.07, SBG-T2 8.07, then RLS-T2, CGT-T1, SPN-T2, DFD-T1 | Identical values. LST-T2 and SBG-T2 are both exactly 8.06739. | yes |
| All 44 condition codes and severities (step 1) | as listed in the CSV block | 44 of 44 identical. Rules: latest issue (3.4), half LOD (3.5), base sample at least 330 days back (4.3), O2/N2 class, rewind-year age band (4.1). Invariant to day-count convention, half/full/zero LOD, first versus latest issue, any-gas code-3 reading, register preservation field and rewind year. Graded severities sit at least 0.0022 inside their 2-decimal bins. | yes |
| C2H2 increments against tap operations, r (CC2, step 2) | DSL-T1 0.998, LST-T2 0.995, RLS-T2 0.999, SBG-T2 -0.07 | 0.998, 0.995, 0.999, -0.073, from first detection (0.978, 0.989, 0.999, 0.056 with the onset interval). Against elapsed days: 0.88, 0.79, 0.88, 0.02. Tap operations clearly beat time. | yes |
| Twelve-month C2H2/H2 (CC2) | DSL-T1 9.8, LST-T2 0.91, RLS-T2 0.64, SBG-T2 0.51 | 9.8 (9.8/1), 0.91 (8.2/9), 0.64 (5.1/8), 0.51 (8.2/16) | yes |
| LST-T2 hydrogen "rising at 9.7 ppm a year in the year before its first acetylene" (CC2, step 2) | 9.7 | 9.63 by OLS or 9.36 by endpoints, over the year before 9 Jun 2025. 9.74 appears only over 11 Sep 2023 to 9 Jun 2025, a window that includes the first acetylene sample. | **no** |
| LST-T2's acetylene "comes with none of its own" hydrogen (CC2, CC3) | none | **Contested.** Supporting: the latest twelve-month H2 pace (8.85 ppm a year) is no faster than the pre-onset 9.63. Against: in the 2026 monthly intervals H2 increments track tap operations (r 0.81, p 0.005). Through the origin, tap operations explain H2 increments with RSS 32.4, against 60.9 for elapsed days, 61.7 for oil degree-days, 68.3 for load and 61.9 for load swing. Saturating radiator-term fits leave 0.8 to 1.0 ppm H2 per ppm C2H2. | **not forced** |
| DSL-T1's acetylene "with almost no hydrogen" (CC2) | H2 flat | H2 between 7 and 10 throughout. Level slope 0.11 ppm H2 per ppm C2H2. Monthly H2 increments against tap operations r -0.26. | yes |
| RLS-T2's acetylene "with hydrogen that started with it" (CC2) | yes | H2 about 33 ppm in 2021 to 2024, then 54 by Sep 2026. Level slope 1.9 ppm H2 per ppm C2H2 (t about 16). The increment test does not show it (monthly r 0.14). | yes, in levels |
| Code 3 with a main-tank fault, by severity (CC4, step 4) | SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45 | Same values. CGT-T1, SPN-T2 and DFD-T1 show time-driven ethylene and methane, a thermal signature. | yes, given LST-T2 excluded |
| Past the annex B interval (step 5) | 7 of 27 | 7 of 27: five by operations, GLT-T2 and SHF-T1 by seven years. The same as at 16 and 28 Oct 2026. | yes |
| Above 30 per cent relative saturation (step 6) | 6 | 6 | yes |
| Docx ask 1: the three | SBG-T2 Southbridge, code 3, 8.07, acetylene; RLS-T2 Rolleston, code 3, 4.98, acetylene; CGT-T1 Coalgate, code 3, 4.73, ethylene | identical values | values yes; selection contested |

**Docx ask 2: in-oil tap changers.** Last service is taken from the maintenance log (6.1, annex B). A drop in the counter is a rollover past 99,999 unless the log records a counter replacement that day. Each logged service reading equals the SCADA 00:00 reading, with 0 operations on the service day, so the counting conventions converge.

| Tap changer (docx ask 2) | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| DSL-T1 | 87,322, past yes | 87,322, past yes | yes |
| DYL-T2 | 87,029, past yes | 87,029, past yes (rollover 2025-07-29) | yes |
| GLT-T1 | 75,013, past yes | 75,013, past yes (rollover 2025-07-04) | yes |
| TPR-T2 | 64,224, past yes | 64,224, past yes (rollover 2025-11-24) | yes |
| LST-T1 | 61,972, past yes | 61,972, past yes (rollover 2025-07-27) | yes |
| GLT-T2 | 29,695, past yes | 29,695, past yes (log reading 3,642 at 2019-04-09 service, past by 7.5 years) | yes |
| SHF-T1 | 23,553, past yes | 23,553, past yes (log reading 17,728 at 2019-08-20 service, past by 7.2 years) | yes |
| CGT-T2 | 57,551, past no | 57,551, past no (rollover 2025-08-17) | yes |
| LST-T2 | 54,294, past no | 54,294, past no | yes |
| RLS-T2 | 49,897, past no | 49,897, past no | yes |
| WDN-T1 | 38,209, past no | 38,209, past no (counter replaced 2021-10-19) | yes |
| DYL-T1 | 32,511, past no | 32,511, past no | yes |
| SBG-T1 | 32,019, past no | 32,019, past no (counter replaced 2022-10-11) | yes |
| WML-T1 | 31,680, past no | 31,680, past no | yes |
| CGT-T1 | 27,923, past no | 27,923, past no | yes |
| DFD-T1 | 21,895, past no | 21,895, past no | yes |
| WDS-T1 | 21,319, past no | 21,319, past no (rollover 2026-03-22; log service 2025-06-24, register says 2021-05-25) | yes |
| DSL-T2 | 20,955, past no | 20,955, past no (log service 2025-04-08, register says 2021-07-20) | yes |
| GDL-T1 | 20,915, past no | 20,915, past no (counter replaced 2023-11-21) | yes |
| LDB-T1 | 20,592, past no | 20,592, past no | yes |
| LDB-T2 | 16,890, past no | 16,890, past no (counter replaced 2025-09-02, register says 2021-08-24) | yes |
| LIN-T1 | 16,064, past no | 16,064, past no (counter replaced 2025-11-04, register says 2021-10-12) | yes |
| SPF-T1 | 14,842, past no | 14,842, past no | yes |
| SPF-T2 | 11,034, past no | 11,034, past no (log service 2026-02-17, register says 2021-11-23) | yes |
| LIN-T2 | 10,079, past no | 10,079, past no (log service 2026-03-03, register says 2022-03-15) | yes |
| KRW-T1 | 6,837, past no | 6,837, past no (counter replaced 2026-05-19, register says 2022-01-25) | yes |
| HOR-T1 | 3,909, past no | 3,909, past no (counter replaced 2026-07-14, register says 2022-07-12) | yes |

**Docx ask 3: above 30 per cent relative saturation.** Uses annex C on the latest issue. Where the label is blank, T is the parquet top-oil read as UTC and converted DST-aware to the NZ sampling hour. A back-test over 952 labelled samples gives a mean absolute error of 0.305 C for that reading, against 3.709 C naive and 0.84 C for a fixed +12 h offset.

| Transformer | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| SHF-T1 | 36.1 | 36.12 (no label; SCADA 28.1 C, NZDT hour) | yes |
| GDL-T1 | 34.9 | 34.92 (no label; SCADA 30.6 C, NZDT hour) | yes |
| WDN-T1 | 34.1 | 34.08 (label 22.5 C) | yes |
| DYL-T1 | 33.1 | 33.07 (no label; SCADA 24.3 C) | yes |
| TPR-T2 | 31.7 | 31.72 (no label; SCADA 19.1 C) | yes |
| SPF-T1 | 31.5 | 31.51 (label 26.5 C; issue-2 water 22 mg/kg) | yes |

KRW-T1 at 28.5 is correctly left out. Its issue-2 label of 21.5 C applies; issue 1's 12.5 C would put it in at 43.0.

**CSV, all 44 rows.** The slate flag follows the golden's slate.

| Transformer | Claimed (code, severity, slate, ops since service, RS %) | Judge recomputed | Reproduced |
|---|---|---|---|
| BNM-T1 | 1, 0.38, not on, no in-oil tap changer, 8.8 | 1, 0.38, not on, no in-oil tap changer, 8.8 | yes |
| BNM-T2 | 1, 0.21, not on, no in-oil tap changer, 7.0 | 1, 0.21, not on, no in-oil tap changer, 7.0 | yes |
| CGT-T1 | 3, 4.73, on, 27,923, 22.8 | 3, 4.73, on, 27,923, 22.8 | yes (slate flag contested, see fork) |
| CGT-T2 | 1, 0.28, not on, 57,551, 28.2 | 1, 0.28, not on, 57,551, 28.2 | yes |
| DFD-T1 | 3, 3.45, not on, 21,895, 19.6 | 3, 3.45, not on, 21,895, 19.6 | yes |
| DFD-T2 | 1, 0.16, not on, no in-oil tap changer, 11.7 | 1, 0.16, not on, no in-oil tap changer, 11.7 | yes |
| DSL-T1 | 3, 9.64, not on, 87,322, 21.5 | 3, 9.64, not on, 87,322, 21.5 | yes |
| DSL-T2 | 1, 0.33, not on, 20,955, 17.0 | 1, 0.33, not on, 20,955, 17.0 | yes |
| DYL-T1 | 1, 0.29, not on, 32,511, 33.1 | 1, 0.29, not on, 32,511, 33.1 | yes |
| DYL-T2 | 1, 0.46, not on, 87,029, 23.9 | 1, 0.46, not on, 87,029, 23.9 | yes |
| GDL-T1 | 1, 0.34, not on, 20,915, 34.9 | 1, 0.34, not on, 20,915, 34.9 | yes |
| GDL-T2 | 1, 0.21, not on, no in-oil tap changer, 20.9 | 1, 0.21, not on, no in-oil tap changer, 20.9 | yes |
| GLT-T1 | 1, 0.19, not on, 75,013, 19.7 | 1, 0.19, not on, 75,013, 19.7 | yes |
| GLT-T2 | 2, 0.30, not on, 29,695, 18.2 | 2, 0.30, not on, 29,695, 18.2 | yes |
| HOR-T1 | 1, 0.49, not on, 3,909, 27.0 | 1, 0.49, not on, 3,909, 27.0 | yes |
| HOR-T2 | 1, 0.25, not on, no in-oil tap changer, 15.6 | 1, 0.25, not on, no in-oil tap changer, 15.6 | yes |
| KRW-T1 | 1, 0.49, not on, 6,837, 28.5 | 1, 0.49, not on, 6,837, 28.5 | yes |
| KRW-T2 | 1, 0.27, not on, no in-oil tap changer, 11.0 | 1, 0.27, not on, no in-oil tap changer, 11.0 | yes |
| LDB-T1 | 2, 0.33, not on, 20,592, 24.4 | 2, 0.33, not on, 20,592, 24.4 | yes |
| LDB-T2 | 1, 0.49, not on, 16,890, 21.1 | 1, 0.49, not on, 16,890, 21.1 | yes |
| LIN-T1 | 1, 0.14, not on, 16,064, 19.0 | 1, 0.14, not on, 16,064, 19.0 | yes |
| LIN-T2 | 1, 0.22, not on, 10,079, 27.3 | 1, 0.22, not on, 10,079, 27.3 | yes |
| LST-T1 | 1, 0.31, not on, 61,972, 22.2 | 1, 0.31, not on, 61,972, 22.2 | yes |
| LST-T2 | 3, 8.07, not on, 54,294, 18.2 | 3, 8.07, not on, 54,294, 18.2 | yes (slate flag contested, see fork) |
| PRB-T1 | 1, 0.42, not on, no in-oil tap changer, 8.9 | 1, 0.42, not on, no in-oil tap changer, 8.9 | yes |
| PRB-T2 | 1, 0.49, not on, no in-oil tap changer, 10.0 | 1, 0.49, not on, no in-oil tap changer, 10.0 | yes |
| RLS-T1 | 1, 0.45, not on, no in-oil tap changer, 8.0 | 1, 0.45, not on, no in-oil tap changer, 8.0 | yes |
| RLS-T2 | 3, 4.98, on, 49,897, 12.5 | 3, 4.98, on, 49,897, 12.5 | yes |
| SBG-T1 | 1, 0.15, not on, 32,019, 26.7 | 1, 0.15, not on, 32,019, 26.7 | yes |
| SBG-T2 | 3, 8.07, on, no in-oil tap changer, 13.9 | 3, 8.07, on, no in-oil tap changer, 13.9 | yes |
| SHF-T1 | 1, 0.21, not on, 23,553, 36.1 | 1, 0.21, not on, 23,553, 36.1 | yes |
| SHF-T2 | 1, 0.39, not on, no in-oil tap changer, 16.9 | 1, 0.39, not on, no in-oil tap changer, 16.9 | yes |
| SPF-T1 | 2, 0.24, not on, 14,842, 31.5 | 2, 0.24, not on, 14,842, 31.5 | yes |
| SPF-T2 | 1, 0.30, not on, 11,034, 22.4 | 1, 0.30, not on, 11,034, 22.4 | yes |
| SPN-T1 | 1, 0.11, not on, no in-oil tap changer, 12.1 | 1, 0.11, not on, no in-oil tap changer, 12.1 | yes |
| SPN-T2 | 3, 4.43, not on, no in-oil tap changer, 11.0 | 3, 4.43, not on, no in-oil tap changer, 11.0 | yes |
| TPR-T1 | 1, 0.49, not on, no in-oil tap changer, 17.9 | 1, 0.49, not on, no in-oil tap changer, 17.9 | yes |
| TPR-T2 | 1, 0.26, not on, 64,224, 31.7 | 1, 0.26, not on, 64,224, 31.7 | yes |
| WDN-T1 | 1, 0.28, not on, 38,209, 34.1 | 1, 0.28, not on, 38,209, 34.1 | yes |
| WDN-T2 | 1, 0.32, not on, no in-oil tap changer, 14.5 | 1, 0.32, not on, no in-oil tap changer, 14.5 | yes |
| WDS-T1 | 1, 0.23, not on, 21,319, 14.7 | 1, 0.23, not on, 21,319, 14.7 | yes |
| WDS-T2 | 1, 0.27, not on, no in-oil tap changer, 10.7 | 1, 0.27, not on, no in-oil tap changer, 10.7 | yes |
| WML-T1 | 2, 1.39, not on, 31,680, 16.1 | 2, 1.39, not on, 31,680, 16.1 | yes |
| WML-T2 | 1, 0.39, not on, no in-oil tap changer, 19.0 | 1, 0.39, not on, no in-oil tap changer, 19.0 | yes |

## Competing answers that survived
**1. LST-T2 kept as a main-tank fault.**
- **The two answers.** The golden slate is SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73. The rival slate is SBG-T2 and LST-T2 (exactly tied at 8.0674, with no shipped tie-break, so the order is undefined), then RLS-T2 4.98, and CGT-T1 drops out.
- **What it affects.** The main recommendation, docx ask 1, and the CSV slate flags for LST-T2 and CGT-T1.
- **What was supposed to close it.** CC2 and step 2: "Leeston T2's comes with none of its own [hydrogen] ... its twelve-month C2H2/H2 of 0.91 is that hydrogen". The submission's own text names this rival ("Not a slate that keeps Leeston T2 on its gas ratio"). The card's `analyst_test` calls it rung 3c.
- **Why the closure does not hold on these files:**
  - The decisive quantity is the hydrogen LST-T2's acetylene brings of its own. It has to be separated from the radiator hydrogen that follows work order CW24-0417: new hot-dip galvanised radiators, 12 Nov 2024, in `maintenance_log_2019-2026.xlsx`. No shipped file says how that background behaves. Valid estimates of it fall on both sides of the deciding line.
  - **Straight-line continuation of the pre-onset pace** (the submission's reading): the latest twelve months' 8.85 ppm a year against 9.63 leaves no excess, so the unit is a leak and is dropped.
  - **Increments against tap operations** (the submission's own acetylene method, applied to hydrogen):
    - LST-T2's 2026 monthly intervals run 27 to 36 days, so elapsed time cannot drive their variation. Its H2 increments track tap operations: r 0.81, Spearman 0.78, one-sided permutation p 0.005.
    - Over every interval since Dec 2024, through the origin, tap operations fit with RSS 32.4. Elapsed days give 60.9, oil degree-days 61.7, load 68.3 and load swing 61.9.
    - The onset quarter (Mar to Jun 2025, 5,039 operations) carries the largest H2 jump, +9 ppm, alongside the first +2.55 ppm of acetylene.
    - Result: the hydrogen arrives with the tap-change process at about 0.9 to 1.2 ppm H2 per 1,000 operations, against C2H2 at 0.60 per 1,000 operations. That is a C2H2/H2 of about 0.5 to 0.7, a main-tank arc, so LST-T2 is kept.
  - **Levels with a front-loaded (saturating) radiator term:**
    - The best fits (tau 0.3 to 0.4 years, RSS 23.6 to 24.5) leave k = 0.8 to 1.0 ppm H2 per ppm C2H2 (t 6.7 to 8.9).
    - Only slower radiator curves (tau 1 year or more) or a straight-line ramp drive k to zero or below, and those fit worse: RSS 34.1 to 97.8, against 23.6.
    - The golden board paper itself describes the radiator hydrogen as rising "at the same easing pace", which is the front-loaded shape. (This was read after the verdict.)
  - **IEC 60599**, which ES-DGA-02 section 2 cites by title only, treats C2H2/H2 above 2 to 3 as the tap-changer contamination signature. LST-T2's raw twelve-month 0.91, and about 1.0 to 1.2 after a saturating radiator correction, both sit in the main-tank range.
  - **The increment lens points the opposite way from the golden on both units.** It shows LST-T2's hydrogen linked to tap operations but does not show RLS-T2's (monthly r 0.14). The golden's in/out split between RLS-T2 and LST-T2 survives only under the straight-line attribution.

**Rivals tested and defeated:**
- **Rank all code 3 by severity** (DSL-T1 9.64, then LST-T2 and SBG-T2 tied at 8.07). Defeated by 5.1 and 5.2 plus DSL-T1's tap-linked, hydrogen-free acetylene (level slope 0.11). Valid as the easy route.
- **Drop every unit whose acetylene tracks operations** (SBG-T2, CGT-T1, SPN-T2). Defeated by RLS-T2's level rise in hydrogen with its acetylene, from about 33 to 54 ppm (k 1.9). See Finding 5 on its increment-lens weakness.
- **MSU-2 rating (10/15 MVA) binds at a 23 MVA site.** Defeated: Rolleston's 2025-26 peak station load is 22.06 MVA, and 23 MVA from the remaining unit plus 15 MVA from MSU-2 are available. Every slate unit peaks well under 15 MVA.
- **Asset-register `oltc_last_service` instead of the log.** Would move 8 rows of ask 2. Closed by 6.1 and annex B.
- **First issue instead of latest.** KRW-T1 would enter ask 3 at 43.0 and SPF-T1 would leave at 28.6. Closed by 3.4.
- **Parquet read as NZ local time.** Would change 15 RS values and drop DYL-T1 and TPR-T2 from ask 3. Closed by annex C's "New Zealand time" plus the data's structure: the series starts at 2020-12-31 11:00 (NZ midnight), has no DST gaps, the evening load peak falls at 05:00 to 07:00 raw, and the label back-test MAE is 0.305.
- **Fixed +12 h offset.** Would move SHF-T1 to 34.0, GDL-T1 to 32.8 and CGT-T2 to 27.6. Closed by the DST-aware back-test (0.305 against 0.84).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 11 | yes |
| Distinct formats | 3 or more | 6 (csv x3, xlsx x3, pdf x2, parquet, md, txt) | yes |
| Largest row count | a file of 25,000+ rows, or a large database | `scada_top_oil_hourly_2021-2026.parquet` 2,232,384 rows; `scada_tap_counters_daily_2021-2026.csv` 93,060 | yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled by file name | `protection_relay_events_2025-2026.csv`, `thermal_imaging_survey_2026.pdf`; neither name labels it | yes |
| Distractors unused yet relevant | same world, something to weigh | Relay events: yes. Through-fault pickups at the same substations, including an LST-T2 incomer pickup on 7 May 2025, a month before its first acetylene. Thermal survey: weak. It is same-world, but its scope line excludes transformers, so it is dismissed in one sentence. | partial |
| Distractor answers a graded quantity | must reproduce and be ruled out | neither answers the decision or a graded figure | n/a |
| Deliverable count | 1 to 3 | 2 (`inspection_slate_2027-28.docx`, `dga_fleet_review.csv`) | yes |
| Format family | none required | n/a | n/a |
| Multi-dimensional asks | not stacked lookups | slate with code, severity and gas; 27-row tap table; 6-row wetness table; 44 x 5 CSV, all analysis-dependent | yes |
| Golden deliverables present | every named golden | `golden/inspection_slate_2027-28.docx`, `golden/dga_fleet_review.csv` | yes |
| Units and rounding stated | every ask | Docx: severity to two decimals, RS to one decimal, stated. CSV ask: no rounding for severity or relative saturation (the golden uses 2 and 1 decimals). | **no (FIX_NOW)** |
| Prompt shape and 25-criterion floor | shape identifiable, 25+ criteria | "01 ranked list under a cap" (`metadata.json`). The asks support well over 25 criteria (rubric not inspected). | yes |
| Realism | nothing reads as generated; goldens read as real | Goldens read as a real board paper and register export. Nits: identical SBG-T2/LST-T2 acetylene at the three severity-setting rounds; templated annual-inspection remarks; XLSX docProps time zone (see Finding 6). | partial |

## Gate G reconciliation
The design note was not read, per this invocation's instruction. The reconciliation uses the card fields in `pipeline.json` (`stump`, `three_rules`), `metadata.json` and the submission's Tags block.

- **Shape: no mismatch.** The judge's line is `decomposition_attribution`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The Gate H line is domain pass, layers pass, decisive_step analytical. The card's `three_rules` says the same (domain "pass (DGA fault-gas source diagnosis; the swap breaks it)", layers "pass", decisive_step "analytical"). The Tags call the objective "each anomalous gas attributed to its source before ranking". Both sides describe the same decisive step on fine numbers.
- **Validity of the analyst test: mismatch.** The card's `analyst_test` reads: "the plain gas ratio keeps LST-T2 (rung 3c: LST-T2, SBG-T2, RLS-T2); only each gas's own source gives SBG-T2, RLS-T2, CGT-T1". On the hardened pack, attributing LST-T2's hydrogen to its own source by increments lands on rung 3c, not on the golden. Rung 3c is therefore a defensible answer, not a provable error. This mismatch predicts a send-back.
- **Distractors.** The judge did not name either declared distractor as the read carrying the task. Neither is too load-bearing.

## Stump power (Gate F)
The judge's assessment: the build pulls strong models in several directions.
- **Rank code 3 by severity** (files DSL-T1, LST-T2, SBG-T2). A valid trap, though DGA-literate models will likely spot DSL-T1's 9.8 ratio.
- **Drop RLS-T2 because its acetylene tracks its tap changer.** A valid trap, and the card's rung 3b.
- **Keep LST-T2 on its gas ratio.** The likeliest strong-model divergence, and the one rung 3c relies on. It is **not a valid stump on these files**, because the data support it.
- **Layer-1 traps** cost rows in the two tables: UTC with the NZ DST change, rollover against replacement, register against log, reissued reports.

As built, much of the expected failure would be credited for the wrong reason. The lever is in Finding 1: make LST-T2's hydrogen unmistakably time-driven background, so that keeping LST-T2 becomes a provable analytical error.

## Findings, ranked
1. **SEND_BACK, input_files: LST-T2's main-tank hydrogen** in `dga_main_tank_results_2021-2026.csv`, Dec 2024 to Sep 2026, against CW24-0417 in `maintenance_log_2019-2026.xlsx`. Regenerate it so the radiator hydrogen is visibly a function of time alone. Assert in the generator, and check in the independent verifier:
   - On LST-T2's post-onset intervals, |r(dH2, tap operations)| < 0.2, and a time-only model fits at least as well as an operations-only model.
   - No H2 jump in the onset quarter.
   - The level-fit acetylene coefficient k stays near 0 for every radiator time constant in a plausible range (for example 0.2 to 3 years), not only under a straight line.

   Alternatively, separate the radiator works from the acetylene onset in time so the backgrounds do not overlap. Do not repair this by stating the C2H2/H2 rule in a shipped file: that would turn the decisive step into rule application (H3).
2. **SEND_BACK companion, input_files: the SBG-T2 = LST-T2 exact tie at 8.06739.** Both units read 2.8 (9 Jun 2025), 4.7 (8 Sep 2025, the base) and 12.9 (14 Sep 2026, the latest), over identical 371-day spans. Under the surviving rival the first-window order is undefined, and the coincidence reads as constructed. Change one unit's series so the two severities differ clearly at two decimals.
3. **Gate B watch item, now load-bearing against the golden.** The gas-source rule is stated nowhere in the pack: no hit for leak, contamination, C2H2/H2, selector or zinc in any file. The rule is that arc gas in oil carries hydrogen, while diverter-compartment oil reaching the main tank is acetylene-rich and hydrogen-poor. ES-DGA-02 cites IEC 60599 by title only. In pass 1 this was credited as the field's own method. On this pack, the rule's standard form (C2H2/H2 above 2 to 3) keeps LST-T2 on its raw ratio, so a strict reviewer can press it as `external_dependency` as well as Gate C.
4. **FIX_NOW, solution: `submission.md`, CC2 and step 2.** "9.7 ppm a year in the year before its first acetylene" does not reproduce: the year before 9 Jun 2025 gives 9.63 by OLS and 9.36 by endpoints. State the window and method, or use 9.6, after the Finding 1 rebuild. Also align the golden board paper's "at the same easing pace since" with whatever the regenerated hydrogen shows. An easing radiator curve is the shape under which LST-T2's acetylene-linked hydrogen appears.
5. **Recommendation for the rebuild: RLS-T2's acetylene-linked hydrogen is visible in levels but not in increments.** Its monthly r(dH2, operations) is 0.14 and its interval models are flat. After the rebuild, assert that RLS-T2 passes the "hydrogen of its own" test under both lenses. Otherwise an increment-based solver can drop RLS-T2 too.
6. **FIX_NOW, prompt: the `dga_fleet_review.csv` sentence gives no rounding.** Add "severity to two decimals" and "relative saturation in per cent to one decimal" to match the docx ask and the golden.
7. **Hygiene, non-decisional, FIX_NOW:**
   - The XLSX `docProps/core.xml` created/modified stamps read 2026-10-16T06:40:00Z for a 06:40 NZDT run, which is 2026-10-15T17:40:00Z.
   - In `maintenance_log_2019-2026.xlsx`, the annual-inspection lead sentence now has three variants, but specific remarks still recur verbatim across sites and years. "T2 conservator gauge glass fogged inside, cleaned" and "Starling nest cleared from T2 cooler" each appear about six times.

## Next action for the author
In the generator, regenerate LST-T2's post-November-2024 main-tank hydrogen as a time-only radiator background, and change one of the SBG-T2/LST-T2 acetylene series to break the 8.0674 tie. Add the Finding 1 assertions to the generator and the independent verifier, rebuild twice to confirm byte-identity, rerun the solver round, then re-invoke the determinism check as pass 3.

## Process notes
- **Concordance with pass 1.** Pass 1 (pre-hardening pack) returned DETERMINISTIC / FIX_NOW with the same Gate G and Gate H lines. In that pack LST-T2's hydrogen was flat (5 to 8 ppm, twelve-month ratio 8.2), so the ratio rival closed cleanly. In this pack LST-T2's hydrogen rises from 6 to 33 ppm after the CW24-0417 radiator works. That added hydrogen co-moves with tap operations, which is where the new fork comes from. Pass 1's report was read only after this pass's `verdict.md` was fixed.
- **No `Agent` tool in this runtime.** ToolSearch for "agent spawn subagent task general-purpose" and for `select:Agent,Task` found neither. The one judge pass therefore ran in the orchestrator's own context, under the same allow-list (the scratch copy only), with no retries. The verdict was written to scratch `verdict.md` before any post-verdict read.
- **Read before the verdict:**
  - the agent definition, the `determinism-check` SKILL.md and the judge system prompt (in full)
  - `prompt.md`
  - `submission.md` lines 9 to 123, the four graded blocks; the heading list was grepped first, and the Tags block (lines 3 to 8) was not read until after the verdict
  - the task folder's file listing (names only)
- **Judging read only** `/tmp/determinism-check-task180-20261011T083204Z-13804/target/`, a fresh copy of `task180/target/` (there is no `target.zip`). No web or server tools were used and no subagent was spawned.
- **Read after the verdict, for the spec gates and the reconciliation only:** `metadata.json`, the Tags block, `golden/` (copied to scratch), the pass 1 report, and these `pipeline.json` fields only: `stump`, `stage`, `stage_name`, `architecture`, `three_rules` (key names listed first; no `solver_rounds`, `judge`, `leak` or `duplicate_check` content).
- **Not read:** `DESIGN_NOTE.md`, `generator/`, `solver_rounds/`, the leak and clone reports, any verifier, `START_HERE.md`.
- **Writes:** this report is the only file written in the task folder. Scratch is under `/tmp/determinism-check-task180-20261011T083204Z-13804/` (scripts, extracted text, ledgers, `verdict.md`). No commit or push.
