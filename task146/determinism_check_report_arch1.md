# Verdict (task146, fresh judge pass)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. One minor hygiene fix is optional and in-house: es_case_notes CN051136 (dated 2026-07-10) says "busy again since the start of October", which is a future month. The withdrawal still reads as a withdrawal, so no rerun is needed.

**Why:** All three committed answers reproduce from the shipped files. The main call needs a forward model of re-filing after the quarter turn, and the data pin it. Fitted on the 50 quarter turns, the by-month refusal model gives about 16.9k (bootstrap 95% range 16.7k to 17.1k on a revised basis). Every variant that captures the timing mechanism rounds to 17,000. The only alternatives are the non-mechanism routes (13k, 14k, 15k), and those validate clearly worse out of sample. Both tables in the xlsx recompute to the golden cell for cell (24 of 24 layoff cells, 14 of 14 industry changes).

## Evidence (recomputed from the bundle)

| Item | Result | Source |
|---|---|---|
| Q3 2026 monetarily ineligible, all regions | 26,035 (6,419 + 8,796 + 10,820), reproduced | ui_program_statistics_2026-09.xlsx, FY2026-27 |
| Western, Coastal, Island share of that total | 10,430, 40.1%, reproduced | same |
| September share of those three regions' ineligible | 5,767 of 10,430 = 55.3%, reproduced | same |
| Usual last-month share | 32% to 35% in every region; 2026 Q3 is 0.565 Western, 0.55 Coastal, 0.53 Island | same |
| Base week ended 3 Oct 2026 | 11,814 advance, matches the PDF | uics csv, ui_weekly_claims_release_2026-10-08.pdf |

**Main-call forecast.** I rebuilt the weekly panel by joining the BRS csv (day-first dates, region codes via the regions file) to the UICS csv at 27 June 2021. I rebuilt monthly ineligible determinations across the headed-insufficient layout (to June 2021) and the later layout. For each region I regressed the change in claims at the 50 first claims weeks of a quarter on ineligible determinations in the three months of the closing quarter, with one intercept per quarter of the year.

- **Month slopes, Western / Coastal / Island:**

| Month of refusal | Western | Coastal | Island |
|---|---|---|---|
| September (last month of the quarter) | 0.70 | 0.85 | 0.82 |
| Earlier months | 0.155 or less | 0.147 or less | 0.085 or less |

- **Month slopes, other five regions:** 0.09 or less in every month.
- **Predicted week ended 10 Oct 2026:** about 16,895 national (revised basis). The first report is the advance count, which runs about 0.6% below revised (mean over the history), so about 16,800. Either rounds to 17,000.
- **Re-filed claims:** about 5,300 national, 4,860 of them (92%) in W/C/I. The rest of the week is about 11,590. This reproduces the "5,000 to 6,000", "11,000 to 12,000" and "about nine tenths" components.
- **Bootstrap over turns, 95% range:** 16,656 to 17,137 on a revised basis.
- **Variants that still round to 17,000:**

| Variant | Prediction |
|---|---|
| Last-month term only | 16,970 |
| Dropping the COVID turns | 16,925 |
| Only W/C/I carrying the refusal term | 16,975 |
| Last 30 turns | 16,975 |
| Last 20 turns | 17,051 |
| Common intercept | 17,047 |

- **Alternatives that do not reach 17,000:**

| Route | Prediction | Out-of-sample note |
|---|---|---|
| Quarter total at one share per region | 14,849 | Leave-one-out RMSE 155 per region, against 76 for the by-month model |
| Seasonal step only | about 13,080 | |
| Pooled across regions | about 14,200 | |
| National-level regression | about 14,500 | |
| Repeat the July 2026 turn step | about 14,860 | |

The prompt and files do not state that the timing model is the right one. The data separate the candidates by leave-one-out error.

**Layoff table (region by first layoff 11 to 31 Oct / Nov / Dec).** Matches the golden in all 24 cells.

- **Sources and filters:** register layoff rows (Open or Closed) plus portal layoff rows. Reduced-hours rows are dropped.
- **Dates and regions:** mixed d/m/Y and dd.mm.Y first-layoff strings are parsed. Each site is assigned to its region through the locality and postcode ranges in regions_territorial_authorities_localities.csv. The portal header region is the employer's, not the site's: 158 site rows differ, so this matters.
- **Duplicates, amendments and withdrawals:**
  - 12 register notices have an exact portal copy on business number, first layoff and site list. Each is counted once.
  - 9 superseded portal notices are dropped in favour of the notices that replace them.
  - 34 withdrawal notes are matched through messy references (LN-2026-545, "LN 2026 00461", "ES 26/140" and similar). A withdrawal by ES ref or LN ref also removes the other copy of the same notice.
  - "Considering withdrawing" and "may withdraw" notes are not counted as withdrawals.

**Industry change (July to September 2025 to July to September 2026).** All 14 groups reproduce.

- **Pre-2026 week labels:** these are Saturdays, so I shifted them back by 6 days to the claims-week Sunday.
- **Codes and measure:** SIC 2006 codes before the week of 4 Jan 2026 are mapped through the concordance, and every 1:n split stays inside one group. Measure is new plus additional claims, with transitional excluded.
- **Totals:** 155,527 and 173,544 claims. The 2026 total equals the program statistics' new plus additional claims for July to September.
- **Check against the naive route:** using the label dates unshifted gives different figures (for example Education -8.6, Public administration -1.7), so the Sunday rule from the technical notes decides these asks.

## Gate notes

- **Gate A:** passes. The main figures reproduce. The critical-component ranges and the 26,035 / 40.1 / 55.3 figures hold. Grain is a full weekly panel, with no change-log trap.
- **Gate B:** passes. Every decisive fact is in the files: the refile rule in technical notes 2.3, the Sunday-week rule in 2.1, the site-region rule and the withdrawal and amendment rules in 5, and the 8:30 Thursday advance and revised counts in 3.1. The mechanism itself (the by-month refile timing) is estimated from the files, not stated.
- **Gate C:** passes, with a caveat. The method is open and the data separate the candidates. A solver who stops at the quarter-total share lands on 15k, but that route validates visibly worse. The 17,000 rounding has about 400 of margin to 16,500 on the advance basis, and the bootstrap keeps it inside. Moderately comfortable, not razor-thin.
- **Gates D and E:** pass. The prompt pins the estimand (the first-reported national initial claims count for the week ended 10 Oct, the rounding, the table definitions and the 11 to 31 October window). Method vagueness here is legitimate.
- **Cross-batch check:** no reference corpus was available to me inside the allowed directory, so this check was not run. No near-duplicate was visible.

## Files/Hygiene

**PASS.** There are 16 files in four formats (csv, xlsx, pdf, json). Two files share the same notice data across csv and xlsx but are not copies of one table. The largest file, ic_open_data_by_industry_2023-2026.csv, has 189,904 rows.

- **Dates:** the snapshot is 8 Oct 2026 and nothing postdates the setting.
- **Layer-1 mess is authentic:** a layout change in July 2021, mixed date formats, SIC 2006 against SIC 2023, Saturday against Sunday week labels, UTC timestamps, re-keyed duplicates, free-text reference variants.
- **Distractors:** lfs_regional_unemployment, online_job_ads_index_weekly and public_holidays are unused and no holiday falls in the target week.
- **Provenance:** the desk_data_log reads like an operational log with no authoring leakage.
- **LLM-tell, minor and not stump-affecting:** several case notes reuse the same sentence templates ("Notice withdrawn. The X confirmed by phone (...), so none of the N layoffs will go ahead."). CN051136 is dated 2026-07-10 but refers to "since the start of October". Neither is exclusion-level.

## Stump power

Moderate. The easy routes give the wrong thousand: a seasonal step from the last week gives about 13,000, repeating the July step or a whole-quarter refusal share gives about 15,000, and a national-level regression gives about 14,500. Only a by-month, per-region view of the refusals gives 17,000. Two things lower the stump power. The July 2026 turn (a +3,042 step) is a recent, visible precedent, so a solver who notices the June refusal spike and applies the July re-filing ratio to September's 5,767 gets about 4.9k re-filed and roughly 16.8k to 17k. The September refusal spike in Western, Coastal and Island is also visible in the program statistics. Strong models that read the program workbook and quantify re-filing from the history will clear it, so expect partial failures rather than a wall.

## Stumping type

`mechanism: forecasting` (with a method-selection element validated out of sample), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

The reported counts and determinations are all fine. The difficulty is a forward projection the trailing counts do not pin, and the clean-data test still stumps (the by-month re-filing dynamic would remain on clean data). Gate G passes.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **Domain:** the field's own work is nowcasting initial claims from the monetary-determination pipeline, with base-period rules, advance and revised counts, and claims-week conventions. Swapping in another field's nouns breaks it.
- **Layer 1:** system change, mixed formats, SIC revision, UTC timestamps, duplicate and amended notices.
- **Layer 2:** estimating and validating the timing of re-filing at the quarter turn.
- **Decisive step:** the main call is analytical. A strong analyst who cleaned the data and read every field and rule correctly could still take the easy route and file about 13k (seasonal step), about 15k (quarter-total share) or about 14.9k (repeat the July step).
- **Supplementary asks:** these turn on rule application and data semantics, which the project rules allow for asks.

## Fix

none. Optionally reword CN051136 in es_case_notes_2026-07-01_2026-10-07.csv so its reason is not a future month; this is a note edit and needs no rerun.
