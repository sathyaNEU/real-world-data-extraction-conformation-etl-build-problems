# determinism-check report, task184, 2026-10-12

## Verdict
NOT_DETERMINISTIC (one answer only: the break-even shortfall). The call, all eight passenger figures and the workbook measures reproduce.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition (counterfactual capacity baseline), stumping_family: analytical, surface_read_dependency: no, sole_data_defect: no

## Why
The prompt asks how far Halloran Bay's forecast passengers "could fall short before another posting would move more", in whole per cent, and never says which whole number. The judge cut the design-day arrivals in steps: at 12 per cent Halloran Bay still leads (258,447 vs 236,860), at 13 it trails (226,769), and the true break-even lies between 12.4 per cent (242,011, ahead) and 12.5 per cent (231,698, behind). "How far it could fall before" reads as 12 (largest whole per cent still ahead, and nearest whole per cent to about 12.4). The golden's 13 is the first whole per cent at which it loses. The design note's fork row SF8 claims 13 under floor, round and ceiling alike, and that claim does not hold: floor and nearest both give 12. Labels: competing_defensible_answer / underspecified_objective. Everything else is forced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Stand-down per interval (lane counts vs roster 2026) | 2 lanes 05:00-21:00 at 7 hosts, 0 through HAL banks | same, constant on every posted day | yes |
| HAL / CUL / ARD / ESK passengers moved | 390,700 / 236,900 / 229,300 / 216,600 | same | yes |
| FAR / DRM / BRN / GLK | 210,100 / 183,100 / 173,700 / 162,500 | same | yes |
| 2026 passengers screened (HAL..GLK) | 622,000 / 1,310,900 / 1,136,600 / 899,100 / 1,068,900 / 874,900 / 765,300 / 647,400 | same | yes |
| Hotel cost per officer-night | 112.98 / 116.72 / 110.01 / 98.50 / 90.30 / 95.40 / 84.70 / 93.73 | same | yes |
| Expense claims per posting week | 8,091.04 / 7,135.92 / 7,339.69 / 8,163.34 / 7,991.56 / 8,824.96 / 8,247.46 / 8,724.60 | same | yes |
| Shortfall at which another posting moves more | 13 per cent | break-even about 12.4 to 12.5; 12 still ahead, 13 behind | no (convention open: 12 or 13) |

## Competing answers that survived
- Shortfall: 12 (largest whole per cent still ahead; nearest whole per cent of the break-even) vs 13 (first whole per cent at which Halloran Bay loses). No shipped sentence closes it.
- Posting call: closed. Roster plus 3 lanes gives Cullinvale 705,300 (the declared default). A flat 2-lane HAL stand-down puts Cullinvale ahead; the feed rules it out (0 through HAL banks on every posted day). The filed text never states that hosts repeat the stand-down in 2027; the call rests on the 8-of-8, every-posted-day regularity.
- Minor, not a fork: claims EC26-61697 (11 Jun) and EC26-61698 (31 Aug), EUR 197.85 in total, fall outside every posting week and are assigned to no airport.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 5 (csv, pdf, xlsx, json, md) | yes |
| Large file | 25,000+ rows | 279,417 rows | yes |
| Distractors named in metadata.json | 2+, none labelled by file name | lane_fault_log_2026.csv, passenger_feedback_summer2026.csv; no file name labels one | yes |
| Distractor weighs, unused, ruled out by a shipped fact | each | judge named neither as the surface read; I did not separately re-derive an arithmetic answer from each | partial, not verified |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | per-airport x per-period passengers, 3 measures x 8 airports; nearest hundred, whole per cent, euros to the cent stated. The shortfall convention (floor, nearest or first-losing) is not stated | no (shortfall) |
| Prompt shape, 25+ criteria | identifiable, 25+ | shape 13, about 40 per design note | yes |
| Prompt form | one paragraph, question first, under 1,000 characters | 882 characters, question first | yes |
| Reads as real work product, not LLM generated | | the judge found no hygiene problem; I did not review the golden PDF and workbook | not checked |

## Gate G reconciliation
Thread: mechanism decomposition (counterfactual capacity baseline), stumping_family analytical, surface_read_dependency no, sole_data_defect no. Design note: gate G `decomposition_attribution` (the team's added capacity net of the host's release), stump the stand-down by interval, stump_class analytical. They match. The declared distractors (fault log, passenger feedback) were not named as the surface read, so neither is too load-bearing. The thread's caution: the stand-down is never filed as a rule and is only visible by comparing the feed, the 2026 roster and the postings. It is derived rather than read off, so it is not a planted rule, but a reviewer applying Gate H may probe it. SF2's closure also leans on the 2027 roster planning the same lanes as 2026.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical (counterfactual lanes with and without the unit under KAS-STD-07 section 6, with the net capacity taken from observed host behaviour).

## Stump power (Gate F)
Strong. The natural route (roster plus the unit's 3 lanes) gives Cullinvale 705,300 against Halloran Bay 390,700, the wrong call. Only reconciling the 2026 feed with the roster exposes the stand-down.

## Findings, ranked
1. Shortfall convention open (12 vs 13). Fork row SF8 is wrong: its claim of 13 under floor, round and ceiling alike does not hold.
2. The stand-down persisting into 2027 is an empirical inference with no filed sentence. Watch it under Gate H; the judge accepted it as forced.
3. Two claims (EUR 197.85) fall outside every posting week. Harmless, but note them in the design note.
4. The postings table ends 30 Aug while the prompt window runs to 31 Aug. Harmless.

## Next action for the author
Fix the prompt's shortfall wording, for example "the smallest whole per cent shortfall at which another posting would move more" (answer 13, golden unchanged). Correct fork row SF8 and re-assert it in `checks.py`, then re-judge once.
