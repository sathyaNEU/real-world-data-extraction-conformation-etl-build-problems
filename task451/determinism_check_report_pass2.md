# determinism-check report, task451, 2026-10-31 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (incurred-but-unpaid completion across a payment-speed regime change), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (sonnet, medium, scratch prefix /tmp/determinism-check-task451-r/ only, target.zip sha256 prefix 0d912557b442d3cb) recomputed the main call from the bundle. Stonecrest, Bellmont, Kettle Run and Harrow Point owe; the other eight do not. Schedule B (B.1.3 to B.1.6, B.2.1, B.3.1) and the Keswold notice CN-2026-14 (5 October 2026 Tallis change) force it. The owing four sit 1.0 to 7.2 points over the 102 line under every received-date variant; the best non-owing partner (Ashby Lane) sits at 96.1 to 96.3. Asks 1 to 3 all recompute, pharmacy to the thousand and out-of-group shares to one decimal.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Members over 200,000 in 2026 | 7 | 7 | yes |
| Received-date ladder, all history (Stonecrest/Bellmont/Kettle Run/Harrow Point) | 108.9-109.4 / 107.1-107.5 / 103.7-104.1 / 103.2-103.7 | 109.2 / 107.1 / 103.9 / 103.6 | yes |
| Same, latest 12 receipt months | in range | 109.4 / 107.3 / 104.1 / 103.7 | yes |
| Same, by claim type | in range | 108.6 / 107.2 / 103.5 / 103.0 | call yes; edges 0.2 to 0.3 below the stated range for Stonecrest and Harrow Point |
| Paid-date ladder, all history | nine owe | nine (Bellmont 120.2 ... Calder 102.8) | yes |
| Paid-date links Nov 2026 to Jan 2027 | same four | 112.1 / 110.5 / 107.3 / 106.3 | yes |
| Median receipt-to-payment lag | 23 days / 1 day | 23 / 1 | yes |
| Median last service to receipt | 13 / 14 days | 13 / 14 | yes |
| Pharmacy, 12 partners (thousands) | 550, 581, 403, 553, 525, 577, 533, 505, 524, 660, 579, 543 | identical (tightest margin about 170 dollars) | yes |
| Out-of-group share, 12 partners | 35.9, 42.1, 31.6, 40.7, 32.1, 44.5, 31.4, 38.4, 30.3, 41.6, 26.2, 39.9 | identical | yes |

## Competing answers that survived
- Paid-date ladder with links from October 2026 on: five owe (Ashby Lane 103.0). October mixes pre-break and catch-up payments, so the cut changes the fifth partner. No shipped rule fixes the cut. This lands off the call only for a solver who adopts a break-aware paid ladder and cuts it at October; it is a method path, not a reading fork.
- Eligibility cut at 29 Jan 2027 (19 span rows posted 30 Jan to 1 Feb): moves Brookhollow's pharmacy from 581 to 583 thousand, nothing else. Schedule B puts the date cut on claims only, so the literal reading is the golden. Residual fork on one ask figure.
- Ask 3 on the clinician roster alone: differs by 0.5 to 2.3 points. The billing NPI against the Exhibit 1 group NPI, with B.4.1(b) and "when the service was given", is the closing evidence; the prompt does not name the billing NPI.
- Chart metric not pinned in the prompt; the ratio reads the same under each basis.
- No completion gives two owing; B.3.1 requires estimating unpaid claims, which excludes it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / rows | 10+ / 3+ / 25,000+ | 10 / 3 (csv, pdf, xlsx) / 174,248 | yes |
| Distractors | 2+, in metadata.json, none named in a file name | stop_loss_policy_2026.pdf, partner_quality_scorecard_2026.xlsx; unused, relevant, ruled out by shipped facts (175,000 deductible vs 200,000 B.1.5 cap; scorecard feeds only B.2.2 savings, no partner reaches it) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12-row asks with nearest thousand and one-decimal percent in the prompt | yes |
| Prompt shape / 25 criteria | identifiable, 25+ | register shape; 12 partners x 3 columns plus call, chart and components give well over 25 (rubric not shipped, counted from graded cells) | yes |
| Reads as real | no LLM tells | thread found system-extract artifacts, no authoring or benchmark disclosure | yes |
| Licence/provenance | source, date, licence recorded | metadata.json: CC0-1.0, constructed, dated 2027-02-03 | yes |

## Gate G reconciliation
Thread: `analytical_non_defect`, surface read no, sole data defect no. Card: `stump_class: analytical` with analyst_test and domain_test present; the design note's stump sentence is the all-history paid-date ladder (nine partners) against the received-date completion (four). These match. The declared distractors are not the surface read; the surface read that carries the trap is the standard paid-date chain ladder, and no shipped artifact ranks the partners. Gate G: clean. The difficulty survives deleting every wrong number, since nothing shipped holds one.
Gate H: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Matches the card.

## Stump power (Gate F)
Strong on paper. The easy route (paid-date ladder over all history) names nine; skipping completion names two; the received-date ladder or a break-aware paid ladder using links from November lands on four. The decisive step is analytical, not semantics or rule application. For the main thread to weigh against the design note's ladder: the break-aware route is a landable path for a strong solver who reads the notice and the lag medians, so both top responses can reach the call; the asks must carry the ceiling (see the 51 and 60 targets in CLAUDE.md).

## Findings, ranked
1. Stale gates line in DESIGN_NOTE.md (around line 287) says "11 files in 5 formats"; the shipped bundle and metadata.json show 10 files in 3 formats. Correct the note; no bundle change.
2. Step 5 of submission.md gives claim-type ranges whose edges the thread did not reproduce (Stonecrest 108.6 vs 108.9 lower bound; Harrow Point 103.0 vs 103.2). The call is unaffected, but the stated range is the golden's critical component, so recheck the stated edges against figures_check.py.
3. Brookhollow pharmacy 581 vs 583 thousand turns on whether the 19 late-posted eligibility rows count. Optional one-line pin: eligibility is taken as posted in the supplied file.
4. October cut of a break-aware paid ladder yields five owing. Optional: say in the golden why October is excluded.
5. Ask 3 does not name the billing NPI; closed by B.4.1(b) and Exhibit 1, optional pin.

## Next action for the author
Fix findings 1 and 2 in the generator and design note, rebuild byte-identically and reship; findings 3 to 5 are optional pins. No re-judge is required.
