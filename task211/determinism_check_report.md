# determinism-check report, task211, 2026-11-04

Architecture 2 (Larkhaven Health's levetiracetam 500 mg products and the contract lab's Q3 2026 re-test).

## Pass 1 (target.zip f7e348d0, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE, no fix, no rerun. Order kept: derivation.md was written from
prompt.txt and target/ alone before graded_blocks.md and graded/ were opened. Every golden figure reproduced: the
patient-months and qualifying visits for every product, the spend by quarter received, the backorder days by quarter,
and Tessard's excess of 4 per 1,000 patient-months (4.07 to 4.25 on every adjusted estimator it ran). Gate F good: a
strong analyst who cleans the data and reads MS-12 correctly still files Halvorne (15.5) by the crude or case-mix
adjusted excess. Gate G decomposition_attribution, analytical_non_defect, no surface-read dependency, no sole data
defect. Gate H domain pass, layers pass, decisive step analytical.

The coordinator's note on Gate F: the thread's own blind derivation found the appearance-change transient and filed
Tessard before it opened the graded blocks, by an adjustment beyond the natural route (the crude excess and the
case-mix adjusted rate both file Halvorne). Recorded as the build's known stump-power risk in the pre-ship check; the
bar needs one of the top two responses stumped, and the portal is the only stump oracle.

### The thread's verdict, verbatim

# Determinism verdict, task211 (levetiracetam 500 mg, MS-12 re-test referral)

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG: every golden figure reproduced).
- **Disposition:** APPROVE. Two residual forks are listed under Evidence for the author's awareness; neither changes a golden value on the most defensible reading, and no repair is required.
- **Why:** The call is Tessard, 4 excess visits per 1,000 patient-months. Crude excess over Levaril (observed minus Levaril's rate) names Halvorne (15.5 vs Pellbrook 10.8, Corwen 7.3, Tessard 5.7). The shipped data show visits run about 2.3x in the first supply after a change in how a patient's tablet looks (product_register.xlsx descriptions plus the Halvorne and Corwen notices), whatever the maker, while Fort Wayne tablets at steady state equal the reference. MS-12 2.6's counterfactual (same patients, same days, tablets releasing like the reference) keeps that spike, so Halvorne's excess nets to about 0 to 2 and only Tessard clears the 2.0 bar of 3.1. The answer is forced by the filed estimand and the data, not by a reading of a word.

## Evidence (recomputed from target/ only)
| Item | Mine | Golden | Reproduced |
|---|---|---|---|
| Patient-months (nearest 10): Halvorne / Pellbrook / Corwen / Tessard / Wynfield | 104,190 / 33,310 / 19,260 / 53,040 / 54,140 | same | yes |
| Qualifying visits, same order | 4,882 / 1,402 / 744 / 1,960 / 1,743 | same | yes |
| Spend Q1, Q2 (nearest 10), received-quarter, adjustments pushed back to receipt quarter | Halv 307,200/251,490; Pell 70,640/114,700; Corw 105,850/106,590; Tess 77,180/168,640; Wynf 164,840/133,850 | same | yes (adjustment lines total 10,305.50, fully allocated) |
| Backorder days Q1/Q2 | Halv 14/14; Pell 59/33; Corw 11/11; Tess 44/9; Wynf 12/17 | same | yes, under the elimination mapping below |
| Tessard excess per 1,000 pm | Poisson (DRE, age 3 or 4 bands, time-since-change bands or first-fill marker): 4.07 to 4.25; with DC 4.10; pooled Levaril+Corwen reference 4.20; cell standardisation with marker 3.99; marker also on first-ever fills 4.45 | 4 | yes |
| Other generics' excess | Halvorne 0.1 to 0.4 (1.7 if first-ever fills are marked), Pellbrook 0.5 to 2.2, Corwen about 0, Wynfield about -1 | "every other under 2.0" | yes |

Competing answers tried and rejected:
- **Halvorne (crude, 15.5).** Fails MS-12 2.6: the spike belongs to the patients' tablet-appearance change, not to release; the same spike appears in Levaril to Corwen changes and Pellbrook moves onto the pink tablets.
- **Pellbrook or Corwen.** Same cause, smaller; vanish under the same adjustment.
- **No product sent.** Tessard's log-rate term (+0.12, z about 3.6, with Tessard vs Wynfield, same maker, also separated within family) clears 2.0 on every adjusted estimator.

Residual forks (flagged, not failing):
1. **Backorder item numbers (asks 3 only; no effect on the call).** Item numbers 447120 (notice 12 Jan) and 448193 (notice 2 Feb) fall before the list's own effective date of 2 Mar, when Corwen was 446507 and Wynfield 447650 per former_item_no. A direct current-number lookup (the naive reading) gives Corwen 12/11, Halvorne 0/14, Pellbrook 0/0, Wynfield 16/17. The golden treats them as the old numbers of the two products with no listed former number (Halvorne, Pellbrook), assigned to the one whose ASN shipments stop when the notice opens (Halvorne gap 5 Jan to 26 Jan; Pellbrook gap 28 Jan to 4 May). That is the only reading consistent with the list's dates, the elimination, and the ASN feed, but no sentence states it; it is a reconstruction across two systems. The naive reading contradicts the list's own effective-date and former-number columns, so I do not count it as a surviving alternative. Also needed: case barcodes (10 + base GTIN, uom CS) read as the product, and ASN/notice UTC times dated in Pacific; both are derivable and not planted.
2. **Whole-visit rounding of the excess.** The point estimate sits at 4.0 to 4.45 on every sensible Poisson or standardised estimator (sampling error of the Tessard term is about 1 visit per 1,000 pm). A steady-state-days-only additive standardisation gives 4.9, which would round to 5. The method is unfiled by design (the standard's general method is open), and the data separate the candidates on the identity of the product, but the integer is only as robust as 4.45 vs 4.5; flagging, since the golden is itself a model output.
Minor: the Larkhaven hospital CSV carries no time zone label (treated as Pacific; the partner JSON is labeled UTC and is converted), and the golden is unaffected.

## Files/Hygiene: PASS
21 files: csv (10), parquet (1, 551,845 claim rows), json (2), pdf (5), xlsx (2); more than 3 formats; one file over 25,000 rows plus several large csv/json. Distractors present and unused: levetiracetam_supply_monitor.xlsx (aggregate, all products), formulary_list_prices_2026.csv, contract_lab_quotation_2026q3.pdf, expected_release in the backorder notices. Operational-looking exports (receiving log with split receipts, invoice price-adjustment lines, two code schemes, merged MRNs, reversals/resubmissions, UTC feeds) read as system output; no authoring or benchmark language found; dates are coherent with a July 2026 setting (latest file 14 Jul 2026, memo 20 Jul). No answer-contamination or provenance issue; nothing exclusion-level.

## Stump power (Gate F)
Good. A strong analyst who cleans the data and reads MS-12 correctly still computes the crude excess against Levaril and files Halvorne (15.5), the natural wrong answer; getting Tessard needs the appearance-change confounder identified and the product term separated from it. The asks add independent hard layers (split receipts and price adjustments pushed back to receipt quarters, the item-number reconstruction, case GTINs, transfer and merged-MRN handling, supply overlap). Not too easy: nothing in the pack names the spike or its fix.

## Stumping type (Gate G)
`mechanism: decomposition_attribution` (confounder-adjusted attribution), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is wrong: the crude rates are correct and the difficulty is separating the release effect from the tablet-change effect; on clean data the same decomposition still decides the call.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- H1: post-market surveillance of generic interchangeability (an excess-event rate against a reference, per patient-month, with case-mix adjustment) is the field's own work; swapping nouns does not preserve the task.
- H2: Layer 1 is the mess (two claim code schemes, reversals, merged MRNs, UTC vs local, transfers, split receipts, item-number cut-over); Layer 2 is estimating the release-attributable excess net of a tablet-change effect.
- H3: the easy route (crude excess vs the reference, or even a case-mix-adjusted rate without the change marker) files Halvorne at 15.5; the correct analysis files Tessard at 4. It is not data semantics or rule application: the effect is established from the data's structure, and the Halvorne spike is a real-world mechanism, not a planted decoy.

## Fix: none
Optional (not required): one neutral line in the purchasing manual extract or item list stating that item numbers were reissued at the 2 March cut-over would harden the backorder ask's determinism, at the cost of making the reconstruction easier.
