# Determinism verdict, N25-014 (Ledgestone Health / Brightwater Medical Group)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Two optional one-line pins are listed under Fix; neither moves a golden figure, so no rerun is forced.

**Why:** Every committed answer reproduces from the shipped files. Literal execution gives professional repricing of $609,633 and a referred-service increase of $1,599,572, for a total of $2,209,205, which is $2.2 million against the $2.0 million threshold in OHCCR 4.06, so the call is "proceed". The expected-share step is pinned by the data. After the 2021 to 2023 acquisitions, the rise in the share at the acquiring system is 86% where the product places the acquirer first or has no tiers, and 0% (-0.1%) where it places the acquirer second. That holds in every leave-one-practice-out run. Rule 4.04 projects "the same member under the same product ... in the projection year", and the tier file supplies the 2026 placements. Every coarser alternative I built (pooled, by carrier, by product, by code) gives $1.47M to $1.64M and closes the review. None of those leaves the strata homogeneous, so none is a licensed reading.

## Literal reading first (what the shipped text gives, word for word)
- Baseline year is 2024 (rule 4.03; the notice is complete 8 Oct 2025, so 2024 is the latest year paid six months after year end).
- Professional services are the lines billed under TIN 39-9943822, repriced at the Exhibit C Ledgestone Medical Group schedule by carrier, with modifier 26 on 93306. No code lacks a rate. There are no versions, voids or dual-plan lines in the professional file. Nothing in the file is paid after 30 June 2025.
- Referred services are the 2024 commercial facility lines, latest version net of voids, whose referring NPI is one of the 18 Brightwater physicians. They must be on a code Ledgestone sites bill (the same 21 codes as Exhibit C) and not already at a Ledgestone site. The moved part is priced at Exhibit C. Bayfield is priced at its multiple of the CY2025 Medicare amount; the cells are formatted 0%, so 4.05 displays as 405%.
- The moving share comes from the 27 physicians of practices acquired 2021 to 2023 under appendix A5. This set is exactly the set of referring NPIs in the 2021-23 extract.
  - Oak Hollow, Northpoint (one at a time, all four inside 42 days), Harborview and Lakeside are TIN mergers.
  - Baird Creek, Cedar Ridge and Fond du Lac Digestive Health are controlled-affiliate registrations.
  - Excluded: Mishicot (2019, no before data), Fox River and Bayside (2018 to 2020), the Harbor Lakes CIN participant, and individual hires.
- Each referral gets the tier of its product for the acquirer from the member's benefit period (plan year, with 1 July renewals) and the tier filings.
- Shares are rounded to whole per cent and used as stated (rule 4.05).

## Recomputation ledger

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| CC1 Brightwater professional repricing | $610,000 | $609,632.63 (baseline $3,302,047.26, repriced $3,911,679.89) | yes (rounds to $610k) |
| CC2 share moved, first-tier or untiered | 86% | 86.09% (tier 1) and 86.08% (no tiers) | yes |
| CC2 share moved, second-tier | none | -0.11%, stated as 0% | yes |
| CC3 Bayfield VTP3 places Ledgestone first from PY2025 | first tier | tier 1 in the PY2025 and PY2026 filings; tier 2 through 2024 | yes |
| CC4 referred services add | $1,600,000 | $1,599,572 (8,972 referred lines, 8,029 candidate lines; Bayfield tier-1 delta $669,926) | yes |
| CC5 projected increase | $2.2M | $2,209,205 | yes |
| Threshold comparison | 2.2 vs 2.0 | 2.209 vs 2.000, proceed | yes |
| Ask 3 Manitowoc imaging | 3,269 / 40.6% | 3,269 / 40.6% | yes |
| Ask 3 Manitowoc endoscopy | 1,574 / 52.9% | 1,574 / 52.9% | yes |
| Ask 3 Manitowoc arthroscopy | 328 / 42.7% | 328 / 42.7% | yes |
| Ask 3 Kewaunee imaging | 1,008 / 45.4% | 1,008 / 45.4% | yes |
| Ask 3 Kewaunee endoscopy | 444 / 64.0% | 444 / 64.0% | yes |
| Ask 3 Kewaunee arthroscopy | 97 / 41.2% | 97 / 41.2% | yes |
| Ask 4 primary care, Brightwater / Ledgestone | 35.0 / 7.6 | 35.0 / 7.6 | yes |
| Ask 4 gastroenterology | 41.8 / 4.0 | 41.8 / 4.0 | yes |
| Ask 4 orthopaedics | 35.7 / 3.7 | 35.7 / 3.7 | yes |
| Ask 4 cardiology | 71.9 / 7.6 | 71.9 / 7.6 | yes |

Ask 3 works as follows.
- It uses the latest version net of voids: 171 replacements and 65 voids resolve to 67,675 lines.
- The county is the ZIP of the eligibility span covering the date (unique for every line).
- 659 cross-carrier duplicates (same member, date, code, modifier and facility) are counted once, leaving 67,016 lines. The 17 same-carrier repeats stay separate.
- Without the cross-carrier dedup the figures are off, for example Manitowoc imaging is 3,336 / 39.8%.

Ask 4 works as follows.
- It keeps codes 99202 to 99215 at place of service 11 and drops modifier 95 and place of service 10 (telehealth).
- It uses the provider-file taxonomy and MD/DO credentials. The 594 NP visits carry taxonomy 363L and fall outside every specialty.
- It counts 2,420 cross-carrier pairs once.
- Without that dedup, primary care is 34.1 / 7.4.

## Forks tested
| Fork | Option A (golden) | Option B | Outcome |
|---|---|---|---|
| Expected share granularity (rule 4.05 does not name tiers) | tier or untiered, 86 / 0: total $2.209M | pooled 44%: $1.47M. By carrier: $1.51M. By product: $1.64M. By code: $1.52M. Ledgestone-only pooled (39%) is lower still. | Call flips to "close". Option A is the only stratification whose strata are homogeneous. The 2026 placement table and "same member under the same product ... in the projection year" point to it. Residual risk: a literal reader could pool. |
| Plan year versus calendar year for the tier lookup | plan year (tier file note and benefit_period_begin) | calendar year gives tier 1 = 83% | Total about $2.19M, still $2.2M and "proceed". Not decisive. |
| Dual-plan dedup in the main figure | no dual lines among Brightwater referrals or professional lines | n/a | No effect. |
| Clayton Brown's 149 lines billed under Kinnickinnic Physician Network (concurrent TIN from 2023-02) | excluded under 4.03 (Brightwater TIN only) | included | A few thousand dollars at most. No effect on the call. |
| Medicare Advantage file | excluded (rule 4.02(b), commercial only) | included | Not a Brightwater-baseline input. |
| Ask 4 specialty source | provider file (carrier primary taxonomy per NPI) | claim-submitted taxonomy, where Kinnickinnic Physician Network reports family medicine for all 21 physicians | Option B gives cardiology 90.4 / 9.6, gastroenterology 49.3 / 4.7, orthopaedics 40.4 / 4.2. No shipped sentence names the provider file as the specialty source. A physician's real specialty is the only defensible one, and the other eight billing groups agree between the two sources, so I treat B as a semantics error. It is the one residual determinism risk (see Fix). |

## Files and hygiene: PASS
- 18 files: csv (11), pdf (4), xlsx (1), json (1). The manifest row counts match the files.
- The pack reads like system output: mixed layouts 2.4 and 3.1, hyphenless TINs, void and replacement versions, credential and practice-name casing noise, and duplicate carrier provider rows.
- No authoring or benchmark language. File metadata names fictional authors. Temporal order is coherent (extract 15 Sept 2025, notice 6 to 8 Oct 2025, no data after the snapshot).
- The distractors present are the Medicare Advantage file, nuclear cardiology 78452 and sleep studies 95810 (no Ledgestone rate), the Harbor Lakes CIN, Mishicot's 2019 affiliation, and individual hires.
- Minor: the manifest description of the MA file says "lakeshore physicians", a stray fiction phrase. Not exclusion-level.

## Stump power (Gate F)
Strong. The decisive trap is the pooled or carrier-level share (35% to 55% against 86% and 0%), which closes the review at $1.5M to $1.6M. Getting there also needs these steps:
1. Find the 27 acquired physicians, including the controlled-affiliate practices.
2. Conform layout 2.4.
3. Tier every referral by benefit-period plan year.
4. Project with 2026 placements, where Bayfield's 2025 move to first tier carries about $0.76M of delta.

Most capable runs that pool or reuse the product-level share will land on "close".

## Stumping type (Gate G)
`mechanism: method_or_model_selection` / `forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported numbers are fine. The difficulty is choosing the exposure-conditioned (tier) estimator over a pooled one. On clean data it still stumps.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: the expected referral shift on acquisition under tiered networks is what health-policy cost reviewers estimate.
- Layer 1: layout 2.4 versus 3.1, voids and replacements, dual coverage, July plan years, TIN mergers and retired TINs.
- Layer 2: estimating the share that moves conditional on network tier and projecting with 2026 placements.
- Easy route: a pooled (44%) or carrier-level rise gives about $1.5M and "close the review", which is wrong.

## Fix
None required (location: none). Optional, solver-visible, no figure moves:
1. Add to appendix A3 that a physician's specialty is the primary taxonomy in the carriers' provider files. This closes the ask-4 claim-taxonomy fork.
2. Add to rule 4.05 or the appendix that the expected share is estimated within the network tier the member's product gives the acquirer. This would turn the pooled-versus-stratified choice into a stated convention, but it removes the stump, so it is not advised.
