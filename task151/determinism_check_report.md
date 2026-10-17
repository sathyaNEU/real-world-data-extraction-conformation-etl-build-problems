# Verdict (task151, re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun needed. One optional solution-block wording fix (Step 4 parenthetical and the 0.2182 / 0.2254 / 0.2698 rival scores, see Evidence); it moves no graded figure.

**Why:** The policy (FIN-14 4.2 to 4.4) and the working paper (CF-14.4) fix the estimand (bonus x probability of reaching each threshold in 2027, contract as signed, role as planned, health risk inside the probability) and the selection rule (lowest look-back score on the 748 hitter-seasons of 2023 to 2026). Executed literally, the basis that scores lowest is the non-catcher regulars' starts x the PA-per-start of the player's 2027 lineup slot. About 40 alternative constructions (pool windows, rate definitions, conditioning on own history, age, hand, slot band, vendor projection, kernel smoothing) either tie it to within 0.0003 (same accrual, $4.25M) or lose by 0.0005 or more. The rounded outputs sit 97k to 150k inside their rounding boundaries. The IL table and the paid-bonus table are forced by the files plus Rules 22.1 to 22.8. No committed answer has a surviving competitor.

## Evidence (recomputed from the shipped files)

Literal reading and the places the text is silent:
- The candidate bases are not enumerated (silent). The rule "the basis the look-back scores best" is clear, so the answer is the best basis the solver can build.
- Which seasons form the pool (silent). 2021-26, 2023-26, 2024-26 and 2025-26 all give $4.25M. A single-season pool (2026 only) gives $4.0M, but it scores worse in the look-back (0.1742 vs 0.1730), so the rule rejects it.
- How PA per start is measured (silent). Starters' lines gives 0.17301. Slot PA including substitutes per start gives 0.17359 and a $4.50M total, so the look-back rejects it, by a thin 0.0006. This is the only near-tie that moves the answer.

| Item | Result | Source / status |
|---|---|---|
| Batting lines | 276,378 (184,271 legacy + 92,107 platform), 0 unmapped IDs, 0 duplicate game-player rows | lsf_batting files, crosswalk. Reproduced. |
| PA per start by slot | 4.716, 4.596, 4.481, 4.366, 4.247, 4.139, 4.038, 3.936, 3.828 | Matches 4.72 to 3.83 and 4.25 / 4.14 / 4.04 / 3.94 / 3.83. Reproduced. |
| Non-catcher regular seasons | 1,440; 391 with 155+ starts; 178 with under 100 | hvbd depth charts + batting. Reproduced exactly. |
| Look-back sample | 748 hitter-seasons | Reproduced exactly. |
| Regulars x slot score | 0.17301 (rate from prior seasons), 0.17320 (rate from all years) | Reproduced as 0.1730. |
| Accrual per player (unrounded) | Lusk 513,778; Rivas 1,010,937; Brock 587,583; Medina 1,198,417; Meeks 911,000; total 4,221,715 | Rounds to 500k / 1.0M / 600k / 1.2M / 900k and $4,250,000. Reproduced. |
| Rival bases (my constructions) | Vendor point 0.353; vendor + band 0.224 to 0.283; own last three 0.225 (smoothed) to 0.265; nines whole 0.2182 (all positions) / 0.1845 (grouped by catcher); regulars all positions 0.194 | Every one is worse than 0.1730. |
| Accrual under rival bases | Own seasons $7.79M; vendor point $7.90M; vendor + band $5.27M; nines non-C $5.15M; nines all $4.62M | The easy routes miss by $0.4M to $3.6M. |
| IL stints (9) | Lusk 5/4/24 68d; Medina 5/19/24 10d; Medina 6/2/24 14d; Meeks 8/9/24 8d; Brock 8/14/24 13d; Meeks 3/25/25 13d; Brock 6/13/26 76d; Rivas 7/8/26 14d; Lusk 9/11/26 17d | Effective date = report "eligible" minus minimum period (22.2); end = transaction activation (22.7); days clipped to Opening Day / last scheduled day. Reproduced. |
| IL traps | RHP Andres Rivas (657232) and Dilson Rivas / Ulises Medina excluded by ID and birth date; paternity list excluded (22.8); rehab and 60-day transfer do not end a stint (22.3, 22.4); Brock's trade does not end a stint (22.5) | Consistent with the weekly report. |
| Paid PA bonuses | 2024: Cedeno 200k, Vasquez 125k (325k). 2025: Vasquez 375k, Candelario 300k, Nunez 225k (900k). 2026: Briggs 262.5k, Candelario 150k (412.5k). | Reproduced; see below. |

How the paid-bonus split reproduces:
- Each payment is split into its PA part by pairing the contract terms with actual PA and starts: Cedeno 524 PA gives 200k, and his E40 150k = 100k PA half + 50k All-Star. Vasquez 513 PA gives 125k, and 85k x 2 = 125k + 45k games started.
- Herron's 2024 PA is 461, so no PA bonus; his 75k is an award. His 235k x 2 belongs to the 2023 season (the 1/15/24 payment is the 2023 second half).
- Candelario's voided, reversed and reissued 165k is one payment. Pitchers' bonuses (Livingston, Lara) are excluded by the register note.
- 2026 is the first half only; the second half falls due 1/15/2027, after the close date. "Paid to date" in the prompt pins this reading.

Defects found in the solution blocks (immaterial to every committed answer):
- Step 4 says every basis was priced "from the seasons of his own group", but the nines-whole score of 0.2182 reproduces only when catchers are pooled in. The grouped version is 0.1845, which still loses to 0.1730.
- The rival scores 0.2254 (vendor + band) and 0.2698 (own last three) depend on constructions the files do not fix. My closest reproductions are 0.2245 / 0.2249 and 0.2649 (own history, unsmoothed). Every one loses by at least 0.03.

Competing answers tested and killed:
- Vendor 2027 projections, with or without a band.
- Players' own seasons.
- Nines whole.
- Single-season pool.
- Slot PA including substitutes: $4.50M, the only live near-tie. It loses on the look-back by 0.0006 and counts bench PA against a starter's start.

Cross-batch check: not performed. The isolation rules forbid reading other task folders. No near-duplicate was visible from inside the bundle.

## Files/Hygiene: PASS
- 21 files in 5 formats: pdf (5), csv (9), xlsx (3), txt (2), json (1). The largest file has 184,271 rows. Real distractors are present: the vendor projections, the RHP Andres Rivas and other name collisions, the league schedule, the club directory, the HRIS map and the earning codes.
- The close-file index reads as a system artifact. Dates are coherent: vendor 2027 projections are dated 12/1/26 and show the five as RAL or FA consistent with their signing dates; the depth chart is dated 12/10/26; the pulls are dated 12/11/26.
- No benchmark or authoring language and no toolchain banners seen. Legacy CRLF, MM/DD/YYYY dates and no PA field give genuine Layer 1 mess. No public-data contamination concern (fictional league). Nothing exclusion-level.

## Stump power
Moderate to good. The easy routes are the natural ones (the vendor's 2027 projections, the players' own recent seasons, the starting nines' PA taken whole), and they file $4.6M to $7.9M against $4.25M. The look-back is filed, so a solver who runs it honestly and builds a slot-conditioned basis lands on the golden. A solver who tests only the obvious bases picks a wrong one. The asks add many separately gradable traps: a name collision, a 7-day concussion list, a transfer that does not end a stint, an effective date that is not the transaction date, a preseason clip, a legacy E40 code that bundles bonuses, a voided and reissued payment, and a payment that falls in a different calendar year than its season.

## Stumping type
`mechanism: method_or_model_selection` (with forecasting), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported inputs (vendor projections, batting lines, depth charts) are correct. The difficulty is choosing the basis by out-of-sample scoring, and it would persist on perfectly clean data. Gate G passes.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- Domain: the deciding quantity is a probability of a contingent playing-time bonus (starts x lineup-slot PA rate), scored by squared error against actual outcomes. A club's finance staff and actuaries do exactly this. The swap test fails to transplant it: lineup slots, starts, IL days and PA thresholds do not survive a change of field.
- Layer 1: the legacy-to-platform layout change, the legacy-to-League ID crosswalk, the HRIS legacy employee map, E40 bundling, the voided payment, the name collisions.
- Layer 2: choosing among bases by look-back score.
- Easy route and its wrong answer: a strong analyst who cleaned everything and read every rule can still file the vendor projection with a band ($5.27M) or his own seasons ($7.79M).

## Fix
none (optional, solution only): reword Step 4's "own group" parenthetical, and either restate the nines-whole score as 0.1845 or say it was priced with catchers pooled. No file or prompt change.
