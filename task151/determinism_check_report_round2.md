# Verdict, task151 (re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed and no model rerun. One optional wording edit, no data change: SOLUTION_STEPS step 4 should say that in the look-back catchers are scored against catcher regulars and non-catchers against non-catcher regulars. Without that, the 0.1730 score does not reproduce.

**Why:** Every committed answer reproduces from the shipped files. The main call ($4,250,000; Lusk 0.5M, Rivas 1.0M, Brock 0.6M, Medina 1.2M, Meeks 0.9M) is forced by FIN-14 4.2 to 4.4 and 6. The choice of basis is made by the look-back, and the data separates the candidates widely. The unrounded total is $4,221,715, which sits inside the 4.125M to 4.375M rounding cell. It also survives every reasonable variant of the winning basis. The one real residual risk is that 4.4 does not enumerate the candidate bases (see Fork 1).

## Evidence (recomputed from target/)
| Item | Result | Source |
|---|---|---|
| 276,378 batting lines 2021 to 2026 | reproduced (legacy PA = AB+BB+HBP+SH+SF+CI, crosswalk joined, 0 unmapped) | lsf_batting_*, crosswalk |
| 1,440 non-catcher lineup seasons; 391 with 155+ starts; 178 with fewer than 100 | reproduced | hvbd_winter_depth_charts sheets, starter lines |
| PA per start by slot: 4.716 (1st) to 3.828 (9th); 5th 4.247, 6th 4.139, 7th 4.038, 8th 3.936, 9th 3.828 | reproduced | starter lines |
| Accrual by player: Lusk 513,778; Rivas 1,010,937; Brock 587,583; Medina 1,198,417; Meeks 911,000 | reproduced; round to 0.5, 1.0, 0.6, 1.2, 0.9 million | term_sheets, ral_depth_chart_2027 slots |
| Total | 4,221,715, rounds to 4,250,000 (sum of rounded players is 4.2M, and 6 says round the unrounded sum) | |
| 748 look-back hitter-seasons (183, 182, 194, 189 for 2023 to 2026) | reproduced | FIN-14 4.4 filters |
| Look-back scores (Brier): non-catchers vs non-catcher regulars and catchers vs catcher regulars at slot 0.1730; nines whole 0.2182; own last 3 seasons 0.2698; vendor projection with band 0.2245 to 0.2268 (golden 0.2254) | all reproduced; ranking identical | |

**IL stints** (all nine reproduced). The effective date is not printed anywhere, but it is forced as the report's "eligible" date minus the Art. 22.2 minimum period, and it agrees with the transaction date minus 0 to 3 days.
- Lusk: 5/4/2024, 68 days (the 10-day to 60-day transfer does not end the placement); 9/11/2026, 17 days (capped at the last scheduled day 9/27).
- Medina: 5/19/2024, 10 days; 6/2/2024, 14 days.
- Meeks: 8/9/2024, 8 days (7-day list); 3/25/2025, 13 days (only from Opening Day 3/27).
- Brock: 8/14/2024, 13 days; 6/13/2026, 76 days (trade, 60-day transfer and rehab do not end it; the All-Star break is inside the season per feed notes section 4).
- Not stints: the paternity list for Rivas in 2025, and the RHP Andres Rivas (CHA) and other Medinas (homonyms in the league IL report).
- Rivas: 7/8/2026, 14 days.

**Bonuses paid** (all reproduced). Each half carries half of PA plus games-started, and the E40 lines carry extras. PA and starts in the batting data pin the split.
- 2024: Cedeno 200,000 (524 PA gives two thresholds; his 150k E40 line is 100k half plus 50k other, and the 1/15/2025 half is 100k). Vasquez 125,000 (513 PA; the 85k+85k halves are 125k PA plus 45k starts). Herron 0 (461 PA, the 75k line is Silver Slugger, and the 10/2023 and 1/2024 halves belong to 2023). Total 325,000.
- 2025: Vasquez 375,000. Candelario 300,000. Nunez 225,000 (RAL-only 449 PA after assignment to New Orleans, one threshold). Total 900,000.
- 2026: Briggs 262,500 (first half only, as of the 12/11/2026 pull). Candelario 150,000 (the voided, reversed and reissued 165k is one payment). Total 412,500.
- Excluded correctly: Lockett games finished, Polanco innings, Candelario All-Star.

## Competing answers stress-tested
| Alternative | Total | Outcome |
|---|---|---|
| Regulars at slot, pooled incl. catchers | 3.79M, rounds to 3.75M | Loses on the look-back (0.1972 vs 0.1730) |
| Vendor projection with past-miss band | about 7.08M | Loses (0.225) |
| Players' own last 3 seasons | about 7.29M | Loses (0.270) |
| Nines whole | 4.62M | Loses (0.218) |
| Slot-third, half, DH, exact-position, last-2-years or slot-specific variants of the winning basis | 4.14M to 4.25M | All round to 4.25M and the same per-player amounts |
| Mixtures with own history, age-matched and prior-PA nearest-neighbour variants | not better | None beat 0.1730 |

## Forks
1. **Candidate set (main call).** 4.4 says "the basis with the lowest average" but does not list the bases to consider. A solver who builds only a pooled regulars-at-slot basis, without the catcher split, would file $3.75M. 4.3's "role the Club plans for him" and the data (catchers start far fewer games) license the split, and the look-back separates it from the pooled basis (0.173 vs 0.197). This is analytical discovery rather than an unstated rule, and I do not fail it. It is the only residual determinism risk.
2. **Total rounding margin.** The exact-position variant gives 4.141M, 16k above the 4.125M boundary. It still rounds to 4.25M.
3. **2026 paid.** Literal "we paid" gives first halves only (262,500 and 150,000). A solver could gross up to the full earned figure, but the 12/11/2026 pull and the register note make the paid-to-date reading the literal one.
4. **Slot at signing.** The only 2027 depth chart is dated 12/10, after Lusk, Rivas, Brock and Medina signed. There is no other plan in the package. Ignorable.

## Files/Hygiene
PASS. 20 files in 5 formats (pdf, csv, xlsx, txt, json). The batting files have 184,271 and 92,107 rows, over the 25,000-row floor. File metadata is organisation-authored, with no tool banners and no authoring or benchmark language. Dates are coherent: pulls are 12/11/2026, FIN-14 was revised 11/12/2026, and the depth chart is dated 12/10/2026. Layer-1 mess is real: legacy vs platform layouts and ID crosswalk, legacy E40 vs HRIS codes and the employee map, a void and reissue, a rehab and a trade, IL effective dates implied by "eligible", homonyms, and the paternity list. Distractors in use: the vendor projections (a tempting 7.1M), the players' own seasons, and the pitcher and award bonuses. No exclusion-level finding. The data is fictional (the club names are invented), so there is no public-answer contamination.

## Stump power (Gate F)
Strong. The two natural routes the policy points at, vendor projections with a band ($7.1M) and the players' own history ($7.3M), miss by about $3M. The pooled regulars-at-slot basis misses by $0.5M. Success needs a starts-by-slot-rate model, a positional split, and a correct point-in-time look-back, so the stump is not one rule-discovery step. The risk is Fork 1, which makes live-run divergence on the catcher split possible. That is analytically valid.

## Stumping type (Gate G)
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Honest data and correct reported inputs, and the difficulty is picking the validated forecasting basis out of sample. It stays hard on clean data. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: starts times plate appearances per lineup slot, catcher rest, and an out-of-sample Brier look-back of playing-time probabilities are baseball-specific forecasting work.
- Layer 1: legacy and platform layouts and ID crosswalk, payroll code migration, and voids.
- Layer 2: a validated playing-time model chosen by look-back.
- Easy route a clean, rule-reading analyst would take: the vendor's projections with a band, or the player's own seasons, giving about $7M. A pooled-lineup model gives $3.75M.

## Fix
none (optional solution wording, step 4, as noted under Disposition).
