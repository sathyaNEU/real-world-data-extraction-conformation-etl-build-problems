# determinism-check report, task188, 2026-11-03 (pass 6, r3 FIX_NOW re-judge)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (expected-cash benchmark estimation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle: target.zip sha256 prefix eaf930e6, current prompt.txt. One thread (r3), no retry. Thread verdict: /tmp/determinism-check-task188-r3/verdict.md.

## Why
Section 7.3 files the test, the business-date convention, and sections 6.2 the 24-hour window and 15-day due rule. The shipped postings separate the candidate measures of "cash the trade produced": only the peer cash-to-card-settlement ratio by business type keeps Seaview Specialty Foods (2.91x) and Pacifica Donair & Pizza (3.17x), and the next member, Sunrise Fresh Market, sits at 0.75x. Mean, pooled, leave-one-out, trimmed and p75 ratios return the same pair and the same 25k-rounded figures. Every graded and ask figure recomputes.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cash paid in, Seaview / Pacifica | 477,000 / 299,000 | 476,947 / 299,345 | yes |
| Card settlements | 321,676 / 183,043 | same | yes |
| Type median cash per card dollar | 0.379 grocery, 0.392 quick service | same | yes |
| Produced / excess, Seaview | 125,000 / 350,000 | 121,924 / 355,023 | yes (rounded) |
| Produced / excess, Pacifica | 75,000 / 225,000 | 71,762 / 227,583 | yes (rounded) |
| Largest non-qualifier | Sunrise Fresh Market | Sunrise, excess 471,806, 0.75x | yes |
| LCTR required Q1-Q4 | 25/40/44/38 | same (inclusive or exclusive boundary) | yes |
| LCTR filed Q1-Q4 | 19/44/44/37 | same | yes |
| LCTR late Q1-Q4 | 2/6/11/9 | same (144 of 144 reports match account cash on transaction_date) | yes |
| Branch ATM cash, 9 branches | as filed | same | yes |
| Branch night depository cash, 9 branches | as filed | same (bag + pickup_date joins every transit-19004 deposit once) | yes |

## Competing answers that survived
- Langley City ATM total (low risk): the terminal was removed on 2026-06-26, the branch's closing date, with 18 deposits that day. Counting the removal day gives 1,278,000 (golden); excluding it or using the UTC day gives 1,259,000. Only Langley's ATM figure moves. Design note SF18 closes "its deposit ATMs" as the terminal at its site on the day of the deposit, listed once per installation, but does not name the removal day as inclusive. Judge reads "in force" as including it. Residual, not a call fork.
- All other alternatives tested were closed by a shipped fact: CDD expectation x12 (refers Kingsway and Bright Spark, rejected by their card-trade match), turnover or card+EFT peers (refers nobody), card+platform denominator (clears Pacifica; dash users' cash/card ratio equals non-users'), posted-date year (Pacifica 300,000; 7.3 pins business date), member_number key for LCTR (17/38/38/33; account is the stronger key), late from transaction_date (1/1/2/6; contradicts the programme), bag-register issuing_transit (not a deposit site; manifest is the physical record).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows or more | hrcu_business_postings_2026.csv, 321,918 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | 3 (str_submissions, fiu_case_register, international_wires); all weighed and unused | yes |
| Distractor soundness | does not answer a graded quantity | none reproduces a graded figure | yes |
| Deliverables | 1 to 3, all in golden | 3 (docx, xlsx, png), all in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | quarterly LCTR counts and 9-branch ATM/night cash; rounding in the asking sentence | yes |
| Prompt | one paragraph, under 1,000 characters | 973 characters | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | card shape `other`; design note states 47 criteria (not re-derived here) | yes (per note) |
| Not LLM-generated; goldens real | clean | judge found clean document metadata; ToR docx creation date 2025-10-02 against approval 2025-11-14 is trivial; golden realism not re-read here | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical. Design note stump sentence: the solver judges cash against the declared expected activity (refers Kingsway and Bright Spark) or against peers/turnover (refers nobody), while only the acquirer-settled walk-in trade shows the two fronts. This matches the thread's easy routes exactly. The declared distractors (STR submissions, FIU case register, international wires) are not named by the thread as the surface read carrying the task, so they are not too load-bearing. No mismatch.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Card analyst_test and domain_test agree: peer-calibrated produced cash from acquirer settlements is cash-intensive-business AML monitoring; Layer 1 is the Pacific/UTC business date, relocated ATMs, bag manifests, key errors, corrections and duplicate Originals; Layer 2 is the produced-cash estimate. The swap (hospitals, megawatt-hours) breaks the call.

## Stump power (Gate F)
Good. Each easy route files a specific wrong slate (declaration refers Kingsway and Bright Spark and misses both fronts; turnover refers nobody; card+platform clears Pacifica). Caveat for the main thread to weigh against the design note's ladder: a cash-to-card-ratio benchmark is a recognised AML technique, and the data converge every reasonable peer statistic on the golden pair, so a solver who builds expected cash from the acquirer settlements lands the call. The thread reached the golden by choosing the estimand from the data, not by a rule filed in the text. The asks (windows, late counts, installation and manifest joins) are hard and separately gradable.

## Findings, ranked
1. Residual fork: Langley City ATM total, 1,278,000 (removal day counted) against 1,259,000; affects one ask cell only. Low risk.
2. Stump power note: the peer-ratio method is a textbook route; stump relies on solvers using declared or turnover benchmarks. Main thread to weigh against the ladder.
3. Trivial hygiene: terms-of-reference docx creation date precedes its approval date.

## Next action for the author
Optionally close the Langley removal day in the design note's SF18 row (inclusive of the removal day, asserted in `checks.py`); no repair to the call or any graded figure is needed, and the build may proceed to ship.
