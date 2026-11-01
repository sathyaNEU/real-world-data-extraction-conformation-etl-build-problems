# determinism-check report, task146, 2026-10-16, round 1

The judge ran at stage 4, isolated, at medium effort, on a fresh unzip of the stage 3 cut (commit f71f5a0, target.zip
sha256 22f06ed9a9233bf7), before the rule 3 repair; the call then was 16,000. The repair and the strengthening since
changed the world and the call (17,000 on the shipped cut), so this verdict is history; the shipped cut's verdict is
`determinism_check_report.md`. Verbatim:

# Verdict, task146 (UI initial claims, week ended 10 Oct 2026)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun is needed. Optional wording fix in the solution blocks: state the SIC 2006 to SIC 2023 cutover (week of 4 Jan 2026) and the Saturday-end to Sunday-start label change explicitly.

**Why:** Every committed answer reproduced from the shipped files. The main call is a region-by-region forecast of the advance count, and it is separated from the easy routes by out-of-sample validation. The regression gives 15,993, and every region-specific variant rounds to 16,000. The easy routes give 13,000 to 14,700.

## Method and literal reading
- The prompt asks for the advance count "first reported" for the claims week 4 to 10 Oct 2026. Technical notes 3.1 define the advance count and say the revision comes a week later. The release PDF and the `uics` file carry the advance counts.
- That week is the first claims week of Q4, because notes 2.1 put a claims week in the month of its Sunday. 4 Oct is a Sunday and the previous Sunday, 27 Sep, falls in September.
- Notes 2.3 define the base period, the monetary determination and monetary ineligibility. They do not state that refused claimants file again at the quarter turn. That has to be found in the history.

## Evidence (recomputed from the bundle)

| Item | Golden | Recomputed | Source |
|---|---|---|---|
| Advance count, week ended 3 Oct | 11,687 | 11,687 (regions sum to it) | `uics` rows for 2026-09-27, release PDF |
| Monetarily ineligible, Jul to Sep 2026 | 40,524 | 40,524 | `ui_program_statistics_2026-09.xlsx`, FY2026-27, summed over the three months |
| Share in Western, Coastal, Island | 39.4% | 15,963 / 40,524 = 39.4% | same |
| Quarter turns in the regression | 50 | 50 (Apr 2014 to Jul 2026) | BRS file joined to `uics` at 27 Jun 2021 |
| Refile share, Western | about 1 in 5 | 0.213 | per-region regression with a Q1/Q2/Q3/Q4 intercept |
| Refile share, Coastal | about 1 in 4 | 0.242 | same |
| Refile share, Island | about 1 in 4 | 0.265 | same |
| Refile share, other five regions | under 1 in 10 | 0.021 to 0.086 | same |
| Q4 intercept per region | not stated | -18 to -53 | same |
| Claims filed again | 4,000 to 5,000 | 4,306 net of intercepts (4,609 slope part) | same |
| Share of that in Western, Coastal, Island | about four fifths | 80.4% | same |
| Rest of the week | 11,000 to 12,000 | 11,687 net, 11,384 gross | same |
| **National call** | **16,000** | **15,993** | same |

- **Data checks.** The monthly sums of new plus additional claims from the weekly files equal the program statistics exactly, in every region and month. New plus additional equals initial in both weekly files.
- **Trap in the parse.** The FY2013-14 sheet needed care: its Jul to Dec 2013 cells are blank, so a naive parser misses the Jan to Jun 2014 ineligible rows. Handled correctly it gives 50 turns.
- **Robustness of 16,000.**
  - Region-specific slope with a Q4 intercept: 15,993.
  - Q4-only intercept: 15,821.
  - Excluding the COVID turns: 16,075.
  - Post-2016 sample: 16,001.
  - Last five years: 15,942.
  - Last three years: 15,713.
  - Ratio (multiplicative) form: 15,753 to 16,105.
  - Re-basing from the advance count to the revised-equivalent level moves it by about 90 or less.
  - All of these fall in 15,500 to 16,500, so none straddles a rounding line. The thinnest case (last three years, 15,703, or about 15,610 after an advance-versus-revised discount) is still about 100 above the line.
- **Competing answers, and why they lose.**

  | Method | Result | Out-of-sample RMSE |
  |---|---|---|
  | Region-specific refile shares | 16,000 | 400 (254 excluding the COVID turns) |
  | One share for every region | 13,400 (13,000 to 13,400 without COVID), or 14,300 with region intercepts | 845 |
  | National-level regression | 14,700 | not computed |
  | Seasonal step only (average past Q4 first-week step, applied to the last week) | 13,100 to 13,400 | 927 |

  The rolling leave-one-turn-out test across the 50 turns separates the candidates clearly, so the data picks the method.
- **Extrapolation risk.** The 2026 Q3 ineligible counts (Western 7,677, Coastal 5,297, Island 2,989) sit above ordinary quarters. The 2020 turns in the history (Western 6,261, Coastal 5,202, Island 3,650) bracket them and are consistent with the same linear share. The extrapolation is therefore supported, not speculative.
- **Layoff table.** The golden is the only reading that fits the filed terms, and it reproduced exactly in all 24 cells.
  - Population: register layoff rows with status other than Withdrawn, plus portal rows with notice type Layoff and status Lodged. Portal rows marked Superseded drop out, and the amended notices stand in place of the notices they replace.
  - Case-note withdrawals: 34 notices, with ES and LN references normalised (`ES 26/253`, `LN2026-508`, `ln-2026-00489`). Notes saying "may withdraw" or "considering" are not withdrawals.
  - Register notices re-keyed onto the portal (77 business-number-and-first-layoff groups) match on business number, first layoff and sites. Each is counted once.
  - Regions are by site locality. The portal `region` column is the employer's head-office region and differs from the site region in 158 rows.
  - First-layoff dates parse day first.
- **Industry table.** All 14 changes reproduced to one decimal.
  - The open-data labels are Saturday week-ends up to 3 Jan 2026 and Sunday week-starts from 4 Jan 2026.
  - Division codes are SIC 2006 up to the week ended 3 Jan 2026 and SIC 2023 from the week of 4 Jan 2026. 2023-only codes 11, 16, 17, 33, 36 and others first appear in that week.
  - The 2006 codes map through the concordance. Every 1-to-n split stays inside one group, so each group is unique.
  - Claims weeks are those whose Sunday falls in Jul to Sep (13 weeks each year). Transitional claims (type T) are excluded under notes 2.2.
  - Misreads give different numbers. Mapping the 2025 codes as 2023 gives Education about 28% instead of 2.3% and Construction 76.1% instead of 55.0%.
  - Using the Saturday labels as calendar dates gives Education -10.6 and Construction 54.4.

## Forks listed (all closed by a shipped sentence, or immaterial)
1. Chart start. "From April 2026" read by week-end date would add the week ended 4 Apr. Notes 2.1 put that week in March, so the chart starts at the week ended 11 Apr. Low risk, graded item only.
2. Advance versus revised for the plotted history. Notes 3.1 say the revised count is final, so plotted history uses revised counts, with the advance count for the latest week. Immaterial to the call.
3. SIC version and label convention. No note states the cutover or the label convention. Both are inferable from the data and the shipped concordance. Moderate risk for supplementary ask 3 only. This is data semantics, which is permitted in the asks.
4. Voluntary leavers on notices ("notice stands") do not change the notice size. The notes say "unchanged", so the workers are not reduced.

## Files/Hygiene
**PASS.**
- 16 files in four formats: csv, xlsx, pdf, json.
- One file of 25,000 or more rows (`ic_open_data_by_industry`, 189,848 rows).
- Provenance and in-fiction dates are coherent. The desk log is in-fiction. Nothing postdates 8 Oct 2026. The export timestamps match the log.
- Realistic mess is present:
  - day-first dates in the BRS file;
  - mixed date formats in the register;
  - ES and LN reference variants in the case notes;
  - blank FY2013-14 cells;
  - sufficient/insufficient headings in the old sheets;
  - a one-week advance count.
- Minor LLM tell: the case notes repeat about 15 template phrases and the employer names are templated. This is cosmetic, not stump-affecting. No exclusion-level finding; the data is fictional, so contamination is not a concern.
- The cross-batch check could not be run under the isolation rules. Nothing in the allowed universe indicates a duplicate.

## Stump power (Gate F)
- The decisive structure (region-specific refile share, with the largest ineligible block in Western, Coastal and Island) is not narrated in any file. It has to be found in 50 turns of history.
- A strong model that stops at a seasonal step or a national pooled rate files 13,000 to 14,700 (13,000 to 13,400 for the seasonal step). One that finds the ineligible link but pools shares gets 13,400, or about 14,300 with region intercepts.
- The base-period sentence in the technical notes and the salient ineligible column raise the chance of discovery, so I estimate moderate to good stump power. Most of the difficulty comes from selecting the regional model and validating it out of sample. No decoy or planted memo is present.

## Stumping type (Gate G)
`mechanism: forecasting` (with method selection), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
All reported counts are correct, and the difficulty is a forward projection the trailing figure does not pin. Run on perfectly clean data it would still stump, so it passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **Domain.** The deciding quantity is what a UI statistics unit would model: how many refused claimants re-file when the base period rolls over. The swap test fails if you put in another field's nouns.
- **Layer 1.** BRS to UICS system change, advance versus revised counts, fiscal-year sheets in two layouts, SIC 2006 to SIC 2023 cutover, an email register against the portal with re-keyed notices, and mixed date formats.
- **Layer 2.** A region-by-region refile-share regression validated out of sample against pooled and seasonal rivals.
- **Easy route.** The seasonal step of past first-quarter weeks on the last four weeks (or a national pooled share) gives about 13,000 to 14,700, and a capable analyst who read everything correctly would still file it.
- **Not decisive.** The ask layer holds semantics and rule application (notice handling, the SIC mapping), which Gate H allows because they do not decide the main call.

## Fix
`none`. Optionally the solution blocks (no input change):
- Step 6 should state that the open-data codes are SIC 2023 from the week of 4 Jan 2026.
- Critical components 3 and 4 give ranges. Add the point values (4,306 net or 4,609 gross for claims filed again; 11,687 or 11,384 for the rest) so a grader can check them.
