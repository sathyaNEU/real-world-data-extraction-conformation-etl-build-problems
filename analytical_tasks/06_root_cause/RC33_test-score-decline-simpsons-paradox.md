# RC33 — State maths scores fell 2 points while every student group held steady or improved: what failed?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Aggregate KPIs down while every segment is up (conversion rate falling as traffic shifts to lower-converting channels; average rating falling as new markets join) |
| Domain | Education policy / assessment |
| Task shape | 12 · Drill-down to one leaf (state average change → cross-classified student groups → within-group changes vs composition; the leaf that carries any real decline) |
| Core method | Decompose the change in the state mean into within-group and composition effects using cross-classified groups (race/ethnicity × eligibility for free or reduced-price lunch), base-period shares; drill to the group with the most negative within contribution; judge each within-group change against its NAEP standard error |
| Analytical stump | The aggregate fell because the student population shifted toward groups with lower average scores, while within-group performance was flat or rising (Simpson's paradox). Decomposing by one dimension at a time can leave the paradox hidden inside a dimension; cross-classification is needed. And small within-group changes must be judged against NAEP's sampling and measurement error, not read as real gains or losses |
| Primary sources | NAEP (National Assessment of Educational Progress) Data Explorer — state results by student group, with standard errors |

## 1. The real-world situation

A state's average NAEP grade 8 mathematics score fell 2 points between two assessments. A legislative committee blamed the state's new curriculum
framework and proposed repealing it. The education department's analysts noticed that most student groups' scores were stable or up, while the
state's enrolment had shifted. The committee wants to know whether the decline reflects within-group learning losses.

## 2. The decision (one deterministic recommendation)

**Whether the decline is attributed to within-group performance (attributed if the within effect accounts for ≥ 50% of the decline and at least one
group's within change is statistically significant at p < 0.05), with the decomposition and the leaf group.**

Rules (department memo):

* Data: NAEP Data Explorer exports for the state, grade 8 mathematics, the two assessment years: mean scale scores, standard errors and percentage of
  students for each cell of race/ethnicity (memo's 6 categories) × NSLP eligibility (eligible, not eligible; "information not available" kept as a
  third category).
* Cells with reporting standards not met (‡) are merged with the memo's designated neighbouring cell within the same race/ethnicity.
* Shares: NAEP-reported percentages renormalised to 100 over reported cells.
* State mean change Δ = within + composition + interaction: within = Σ s0 × Δμ; composition = Σ Δs × μ0; interaction = Σ Δs × Δμ.
* Report the reconstructed state means against published state means (differences from rounding and suppression).
* Significance of a within-group change: z = Δμ ÷ √(SE0² + SE1²), two-sided p < 0.05.
* Leaf: the cell with the most negative s0 × Δμ.

## 3. Why capable analysts get it wrong

* The aggregate is the headline and the policy changed at the same time.
* One-dimension breakdowns can still hide composition within groups.
* Subgroup changes are small and noisy.
* Suppressed cells and "not available" categories must be handled consistently.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `naep_mathematics_grade8_state_groups_<years>.xlsx` | XLSX | ~12k (state × year × group cells) | NAEP Data Explorer | U.S. Government work (public domain) | Means, SEs, percentages |
| 2 | `naep_state_overall_<years>.csv` | CSV | ~500 | NAEP Data Explorer | Public domain | Published state means |
| 3 | `naep_reporting_standards.html` | HTML | — | NCES | Public domain | Suppression rules |
| 4 | `department_memo.pdf` | PDF | — | Task author | — | Rules in §2, merge rules |
| 5 | `committee_repeal_brief.pdf` | PDF | — | Task author | — | The curriculum claim |
| 6 | `simpsons_paradox_reference.pdf` | PDF | — | Cite | Cite | Background |

## 5. Deterministic solution path

1. Extract cross-classified cells for the state and years; merge suppressed cells; renormalise shares.
2. Reconstruct state means; compare with published means.
3. Within, composition and interaction effects; z-tests per cell.
4. Leaf; decision; contrast with the committee's reading and with one-dimension decompositions.

## 6. Wrong paths (method errors, not misreadings)

**A — aggregate change only.** Curriculum blamed for a composition effect.

**B — one dimension at a time.** Race-only or NSLP-only breakdowns leave composition inside groups.

**C — ignoring standard errors.** Small within-group changes are treated as real.

**D — dropping suppressed cells.** Shares no longer reflect the population.

## 7. Why the stump is analytical, not semantic

The cells, merge rules and formulas are specified. The trap is a weighted mean whose weights moved, hidden by partial breakdowns.

## 8. Draft task prompt (prose)

> The committee wants to repeal the curriculum because maths scores fell. Use the department memo's cross-classified decomposition to tell me whether
> students in comparable groups actually did worse. Provide `score_decomposition.csv` (cell: shares, means, SEs, contributions), `simpson_chart.png`,
> and a one-page `curriculum_rca.pdf`.

## 9. Deliverables

* `score_decomposition.csv` — all cells with inputs, contributions and z-tests; summary lines.
* `simpson_chart.png` — within-group changes alongside composition shifts, aggregate change overlaid.
* `curriculum_rca.pdf` — decision, leaf, and why the aggregate misleads.

## 10. Where 25+ rubric criteria come from

* Cell extraction and merges: 3.
* Shares and means for the 6 largest cells × 2 years: 12 (grouped).
* Reconstruction check: 1.
* Within, composition, interaction: 3.
* Significance tests and the leaf: 4.
* Decision and contrasts (committee, one-dimension): 4.

## 11. Golden-output checklist

* Cross-classified cells with the "not available" category.
* Renormalised shares; suppression merges.
* Decomposition with base shares; SE-based tests.

## 12. Build notes (scope tuning)

* Choose a state and assessment pair where the state mean fell by ≥ 2 points while race-only and NSLP-only groups were mostly flat or up; confirm the
  composition effect exceeds 50% of the decline.
