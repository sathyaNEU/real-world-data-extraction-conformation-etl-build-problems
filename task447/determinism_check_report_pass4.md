# determinism-check report, task447, pass 4 (2026-11-01, the isolated thread's verdict on 60f87154, kept as filed; not reconciled, because its FIX_NOW went straight to the ask rework that pass 5 judged)

- **Verdict:** NOT_DETERMINISTIC, but only on supplementary answers 3 and 4 (the two market exhibits). The main call and the 2.2 figure are forced and reproduce. The cause is an unfiled person-linkage rule that changes graded one-decimal figures.
- **Disposition:** FIX_NOW. Add one sentence to appendix A2/A3 that pins how a member held under a second key is the same person. Add one sentence on how a replacement that cites a Ledgestone account number finds its original. The main call, the stump, the ladder and every other file stay byte-identical. The goldens already match the pinned reading, so no main-call rerun is needed.
- **Why:** The call "proceed" ($2.2M against $2.0M) follows from the shipped files. Every route that skips tier conditioning lands at $1.45M to $1.65M and files "close". Supplementary 3 (county and line counts and shares) and 4 (office-visit shares) reproduce only under a person-linkage rule that no shipped sentence states. A2 and A3 say only that a service or visit "reported to more than one carrier is one". Nothing defines how a member held under a second key is the same person. The nearest reasonable alternative, matching on birth year, sex, ZIP and the service alone, moves five of six facility counts and the primary-care Brightwater share (35.0 to 35.1). Gate C/E on a committed answer, label underspecified_objective. The main-call fork (see Evidence) is closed by the data, not by a sentence.

## Evidence (everything recomputed from target/)

**Main call**

| Figure | Reproduced | Source |
|---|---|---|
| Brightwater professional baseline | USD 3,302,047 on 23,970 lines of TIN 39-9943822, none paid after 30 Jun 2025, no replacements or voids | apcd_professional_claims_2024.csv |
| Repriced at Exhibit C Ledgestone Medical Group schedules | USD 3,911,680 | Exhibit C, sheet Professional (all codes and the modifier-26 line found) |
| Professional part | **USD 609,633**, which is CC1 USD 610,000 | |
| Referral baseline | 8,972 lines referred by the 18 Brightwater NPIs; 700 already at Ledgestone sites; 8,029 lines offered by Ledgestone (Exhibit C codes) and elsewhere | apcd_op_facility_claims_2024.csv, facility_directory.csv |
| Referred part (86% where Ledgestone is first-tier or untiered in 2026, 0% where second-tier) | **USD 1,599,572**, which is CC4 USD 1.6M | CMS file for Bayfield at percent of CY2025 Medicare |
| Total | **USD 2,209,205**, which is 2.2 | |

- Tier mapping for 2026: BMH-VTP3 first tier; CBH-TPO2, LBA-TPO9 and NBH-TEP4 second tier; the other six products untiered (network_tier_placements_2020_2026.json).
- Bayfield's Value Tier PPO moved Ledgestone to tier 1 from plan year 2025 (CC3 reproduced).
- Join set under A5: Oak Hollow 2021-10-01; Baird Creek 2022-04-01 (control); Northpoint's four orthopedists individually, 2022-10-03 to 2022-11-14 (all within 90 days); Harborview 2023-03-01; Cedar Ridge 2023-08-01 (control); Wolf River's Lakeside 2022-06-01 and Fond du Lac Digestive 2023-02-01.
- Excluded correctly:
  - 2020 joiners, who have no 2021 or earlier "before" data (none of their NPIs appear in the 2021-2023 file);
  - Harbor Lakes (a network participant, not control) and NPI 1644067740's round trip;
  - Mishicot (joined in 2019).
- Rise as a share of services that were elsewhere before the join (tier by the member's benefit-period plan year; 2021-23 file alone or with 2024 gives the same):

| Group | Rise |
|---|---|
| Untiered | 0.859 to 0.861 |
| Tier 1 (Wolf River under Cedarbrook and Lakefront tiered products; Norbridge from plan year 2024) | 0.860 to 0.861 |
| Tier 2 | -0.001 to 0.000 |

  CC2 reproduced, and so was "none" for second-tier. Join-date variants (practice date versus individual dates, control date versus mid-month) all give 86 / 86 / 0.
- Alternative main-call routes (referred part plus USD 609,633):

| Route | Total | Call |
|---|---|---|
| One pooled share (43 to 44%) | $1.45M to $1.47M | close |
| By carrier | $1.49M to $1.51M | close |
| By product over its own history, BMH-VTP3 = 0 to 1% | $1.64M | close |
| Product by tier with BMH-VTP3 missing cells set to 0 | $1.63M | close |
| By code and tier, or code, product and tier, with the 86 / 0 fallback | $2.20M to $2.22M | proceed |
| Tier by calendar year of service instead of plan year (tier-1 share 83%) | about $2.19M | proceed |

  Everything that conditions on the member's 2026 tier placement gives proceed and 2.2. Everything that does not gives close. The margin to the threshold is USD 0.21M and is not noise-driven.
- Tension to record (not a fork the data leaves open): 4.05 says "a share is estimated for a service and a product ... the office does not estimate one share across products". BMH-VTP3 has no history with Ledgestone in tier 1, because the 2021-23 acquisitions all sit under tier 2. The golden's 86% for BMH-VTP3 is therefore borrowed from the tier-1 and untiered experience of other products. The data separate the candidates sharply (0% against 86%, pooled by tier). The phrase "as it stands in the projection year" points at this. An expert reaches 86%, but the filed words do not say to borrow across products.
- Clayton Brown (NPI 1451989697) also bills under Kinnickinnic from 2023-02-06, with no end date on his Brightwater row. Under 4.02(e) he is a Brightwater physician on every 2024 date. His referrals carry USD 358K of the referred increase. Without him the total is about $1.85M and the call flips. No shipped sentence excludes him, so this is not a fork, but it is a load-bearing inclusion.
- Rate and unit points:
  - 4.04(b) prices moved services at the facility rate "filed with the notice", times the unit count; the data hold no quantity above 1 on these referred lines.
  - Bayfield's contract says "the Medicare amount ... in the calendar year of service". Only CY2025 amounts ship, so the golden uses them. This yields a single figure, not a second one.
  - The MA file (1,550 lines referred by Brightwater NPIs) and the HCRIS extract are correctly out of scope under 4.02(b).

**Supplementary 3 (exhibit 1)**
- Method: 2024 facility lines net of voids and replacements (claim frequency 8 voids net to zero; 7 replaces the original), A1 code ranges, county from the ZIP on the eligibility span covering the date, services as the sum of quantity.
- With the golden dedupe (433 removed: 113 same member key, 320 second key, each time the second claim's allowed amount equals the first claim's member liability and birth year, sex and ZIP agree): all six rows match the golden exactly.

| County and line | Count | Brightwater share |
|---|---|---|
| Manitowoc imaging | 3,269 | 40.6 |
| Manitowoc endoscopy | 1,574 | 52.9 |
| Manitowoc arthroscopy | 328 | 42.7 |
| Kewaunee imaging | 1,008 | 45.4 |
| Kewaunee endoscopy | 444 | 64.0 |
| Kewaunee arthroscopy | 97 | 41.2 |

- Forks, both reasonable readings of "one service however many carriers were billed":

| Reading | Result |
|---|---|
| No dedupe | Manitowoc imaging 3,398 / 39.1; Manitowoc endoscopy 1,658 / 50.2; Kewaunee imaging 1,069 / 42.8 |
| Same member key only | Manitowoc imaging 3,362 / 39.5 |
| Demographics-only person match | 3,267; 1,571; 327; 1,007, and Manitowoc arthroscopy 42.8 against 42.7 |

**Supplementary 4 (exhibit 2)**
- Method: codes 99202 to 99215; place of service 10 and modifier 95 excluded; locations by service facility ZIP; specialty from the carrier provider file (one taxonomy per NPI, so the Kinnickinnic claim-level family-medicine coding is bypassed); replacements resolved; second-key duplicates removed.
- Result with the golden linkage: all eight shares reproduce.

| Specialty | Brightwater | Ledgestone |
|---|---|---|
| Primary care | 35.0 | 7.6 |
| Gastroenterology | 41.8 | 4.0 |
| Orthopaedics | 35.7 | 3.7 |
| Cardiology | 71.9 | 7.6 |

- Ledgestone's numbers: LMG 39-8461147 plus Mishicot 39-2492126 (Fox River and the other controlled TINs bill no 2024 professional lines).
- Forks:
  - Demographics-only second-key match: primary care Brightwater 35.1 (n 39,021 against 39,075).
  - Same-member-key dedupe only: 33.7 / 7.3, 40.4 / 3.9, 34.2 / 3.5 and 70.7 / 7.5.
  - Ledgestone replacement not linked (997 replacement lines cite a numeric Ledgestone account number that is not a claim id in the file; each matches exactly one original on carrier, member, date and TIN): Ledgestone shares become 8.8, 4.9, 4.4 and 9.5, against 7.6, 4.0, 3.7 and 7.6.

**Undefined codes, units and keys (the pack ships no extract dictionary or manifest)**

| Item | Opens a second figure? |
|---|---|
| Claim frequency 1 / 7 / 8, quantity -1 voids | No. This is standard X12 usage and is discoverable from the negative lines and the id links. |
| Layout 2.4 columns (CLM_STATUS 'O', DOS yyyymmdd, TIN without hyphen, TOB 131) | No. The mapping is plain from the column names. |
| `relationship_code` 18 / 19 / 01 | Not needed. |
| The second member key and the pricing relation between a primary and a secondary claim | Yes. Supplementary 3, all six counts and one share; supplementary 4, primary-care Brightwater 35.0 or 35.1. |
| A replacement citing a Ledgestone "account number" | Yes. Supplementary 4, all Ledgestone shares. |
| `benefit_period_begin` to plan year | Defined by the tier JSON note; the call-day variant stays on proceed. |

## Files/Hygiene
**PASS.**
- Count and formats: 17 files; pdf (3), xlsx (1), json (1), csv (12).
- Size: one file over 25,000 rows (professional claims, 72,514 rows; the 2024 and 2021-23 facility files also exceed it).
- Distractors present: the Medicare Advantage claims, the HCRIS extract, and the Harbor Lakes network participant. Nothing in a file name names a trap.
- Provenance: PDF and xlsx metadata read as ordinary office output (Word, Microsoft Print To PDF); no authoring or benchmark language found by grep.
- Temporal coherence: latest paid dates are in 2025 (professional 2025-08-30, facility 2025-08-26), the tier JSON is dated 2025-09-26, and the notice is dated 6 Oct 2025 (received 8 Oct), so nothing postdates the setting.
- Baseline year: 2024 meets 4.03's six-month rule on 8 Oct 2025.
- No exclusion-level finding.
- Cross-batch check: not performed. I may read only this folder, and no prior verdicts or other tasks are in it.

## Stump power
Good. The four easy routes (pooled share, by carrier, by product, tier ignored) all give a confident "close" at $1.45M to $1.65M, and 4.05's "do not pool across products" invites the product route. The tell that separates them is the filing sheet plus the benefit-period tier join, which only the tier-conditioned estimate uses. One softener: the phrase "as it stands in the projection year" in 4.05 points close to the answer, and a careful model that tests the tier dependence gets it right. The Brightwater-only shortcut (excluding Clayton Brown) is a second wrong route that flips the call.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported numbers are fine. The difficulty is projecting a share to a network placement (Ledgestone first tier in Bayfield's product) that no history of that system or product shows, using the tier-conditional response seen under other products. On perfectly clean data it still stumps: the clean-data test passes.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: the field's own work (state cost review of a provider acquisition, with a referral-steering share estimated from earlier acquisitions) is what decides the call. The swap test fails to transplant: hospital and school nouns do not fit.
- Layers: Layer 1 is the layout change from 2.4 to the 2024 file, the three claim-version codes, replacement links by account number, second member keys, and the preliminary and revised releases. Layer 2 is estimating the share conditional on tier placement and applying it to placements not yet observed.
- Do 4.04, 4.05 and A5 as written already perform the decisive step? **No, but they come close to naming it.** A5 performs the join mechanics (who joined, on which date, individually or by practice), 4.04 performs the pricing and 4.05 performs the rise arithmetic. A strong analyst who reads all of them correctly can still file the wrong answer by an easy route. "A share is estimated for a service and a product ... does not estimate one share across products" literally yields BMH-VTP3 about 0% and a total of $1.64M ("close"). An analyst who prefers a pooled or by-carrier estimate files $1.45M to $1.51M ("close"). Reaching the golden needs the step the sentences stop short of: recognising that the response depends on the tier placement, reading the plan-year placements from the JSON via each member's benefit period, and borrowing the tier-1 and untiered response for a product-year configuration with no own history. That is a choice of estimand, so it counts as analysis, not rule application. The caveat is the sentence "as the product stands in the projection year", which hints at it.

## Fix
- **Where:** input_files (appendix pin) and none for the main call.
- Add to A2/A3: "A member the database holds under a second key for the second plan is the same person when that key's claim reports the same service priced on the first claim's member liability and both keys give one birth year, sex and ZIP. The second claim is the duplicate." Pin the rule only for exhibits 1 and 2; the main call and 4.05 are untouched.
- Add one line: "A replacement claim that cites an account number in place of a claim number replaces the one original of the same carrier, member, date and billing number."
- Optional, outside the verdict: say why Clayton Brown counts, for example a note that a physician billing under several numbers counts once for each practice he bills under. A4 currently covers only the system level.
