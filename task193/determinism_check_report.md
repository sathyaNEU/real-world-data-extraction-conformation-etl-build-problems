# Determinism verdict, t193 re-judge (judged cold from target/ and prompt.txt only)

**Verdict:** DETERMINISTIC, SOLUTION_WRONG (main recommendation forced; supplementary 5 has one wrong golden figure and one exact-tie figure).
**Disposition:** FIX_NOW. Regenerate the DDD answers for H4 (159767.0, not 159766.9) and pin the tie rule (or ask doses whole). Pinning in the prompt changes one ask's text, so a rerun of that ask only. If the author will not pin the rounding, ask 5 H6 (316685.25) is an open fork and Gate C fails for that ask.
**Why:** The 7 referred pairs fall out of every data-based construction of the expected number I could build (six of them), with the nearest referred pair at 1.35 to 1.36 and the nearest non-referred pair at 1.03 (1.19 on the loosest construction) against a 1.25 line. The shipped text closes the equal-chance reading (Standard 1.1: "more often than the register's own dispensing pattern would give"). The real weak points are in the asks: two exact rounding ties in ask 5, thresholds in the PNG that move with the construction, and "per authorisation holder" against "fee payer".

## Reproduction table (from the shipped files, deduped, crosswalk-folded, first receipt in window, same-day excluded)
| Item | Golden | Mine | Status |
|---|---|---|---|
| Ask 1, 23 pairs, patients / after / before | listed | all 69 counts identical | reproduced |
| Candidate pairs (n>=25) | 20 | 20 | reproduced |
| Referred | 7 | 7 (same pairs) | reproduced |
| Lowest referred multiple | 1.36 | 1.359 (Ternivast/gout and Oxelumab/antidepressant) | reproduced |
| Nearest non-referred | Dalvextin/acid 1.03 | 1.030 | reproduced |
| Equal-chance set | 10 (adds Varenadol x3, Admirabin x2) | 10 | reproduced |
| Ask 4, 16 chain-quarters, accepted / rejected / median | listed | all 48 identical (medians all whole days) | reproduced |
| Ask 5 DDD and fee, 7 payers | listed | fees all identical to the krone; DDD identical except H4 and H6 (see below) | 2 DDD figures not reproduced under half-up |
| Ask 6, 24 cells, patients and share | listed | all 48 identical (region at window start via previous_region) | reproduced |
| Unzip hygiene: 2,103 re-sent B lines, 360 retired keys folded | 16991 keys | 16991 | reproduced |

## Probe results
- Raw dispensings 176,612; 2,103 exact re-sends (all in the 2025_2026 file, same submission date) leave 174,509. No unmatched package codes, no line outside its code's validity window (so the "package at date of dispensing" rule is vacuous here), no dispensing after death or emigration. Rejected lines in submission_exceptions.csv do not overlap dispensings. Max submission date 16 Oct 2026, before the 20 Oct pull.
- Tracker (3.2c) does not bite: the two pairs under assessment (Oxelumab/topical, Ternivast/antiemetic) sit at 1.01 and 0.96 anyway.
- Product register launch and lapse dates match the dispensings (Ternivast from 11 Feb 2026, Oxelumab from 16 Oct 2025, Varenadol to 18 Apr 2026, Admirabin to 7 Jul 2026).

## The four questions

### 1. What the comparison is taken against
The shipped text never states the construction. Standard 3.5 sends it to "the division's own epidemiological work ... recorded with each run", which is not shipped. What is shipped: 1.1 "more often than the register's own dispensing pattern would give" and 3.2(b) "expected if receiving the product had no bearing on when the marker treatment is first received". Comparators left standing, with the referred set under each (multiple = after / expected after, threshold 1.25, n>=25, tracker applied):

| Comparator | Set | Tern/gout | Oxel/antid | Admirabin/antid | Nearest below line |
|---|---|---|---|---|---|
| Equal chance (n/2) | **10**, adds Varenadol x3, Admirabin x2 | 0.98 (hidden) | 1.10 (hidden) | 1.60 | n/a |
| Pair patients' own first-receipt dates, product and marker (golden) | **7** | 1.359 | 1.359 | 1.015 | 1.030 |
| Same, ties not conditioned out | 7 | 1.366 | 1.365 | 1.018 | 1.033 |
| Same, month-binned | 7 | 1.438 | 1.394 | 0.993 | 1.064 |
| All window first receivers of product and marker | 7 | 2.10 | 1.70 | 1.06 | 1.119 |
| All window dispensing dates of product and marker | 7 | 2.22 | 1.81 | 1.11 | 1.187 |
| Pair patients' dispensing dates | 7 | 1.45 | 1.358 | 1.06 | 1.04 |
| Product dates from pair patients, marker uniform over window | 7 | 2.15 | 1.67 | 1.09 | 1.03 |
| Uniform over product's marketed-and-authorised interval, marker uniform | **8: drops Oxelumab/antid (1.148), adds Admirabin/antid (1.301)** | 1.52 | 1.148 | 1.301 | 1.228 |
| Product uniform over availability, marker dates from pair patients | **5**: drops Tern/gout (1.04), Oxel/antid (0.99) | 1.04 | 0.99 | 1.09 | n/a |
| Null-effect adjusted sequence ratio (crude SR / null SR) >= 1.25 | 7 | 1.71 | 1.80 | 1.08 | 1.06 (Dalvextin/acid; Sovraxil/antipsychotic 1.40 has under 25 patients) |

Ruling out: 1.1 ("the register's own dispensing pattern") rules out equal chance, and it also, by its wording, rules out the two availability-interval constructions, because those use the product register's dates and not dispensing. Both rule-outs are by that one sentence read as the test; neither is stated as "do not use 50 per cent" or "use the pair's own dates". The write-up's phrase "from the pair's own first-receipt dates" is narration, not a shipped sentence. I count the data-based family (rows 2 to 8, 11) as closed to one set by the data, and the availability family as closed only by 1.1.

**Residual open fork the set does not hide: the plotted thresholds.** The PNG marks "each pair's referral threshold ... 1.25 times its expected share". The expected share depends on the construction, even though the referred set does not. Ternivast/gout threshold share: 0.451 (pair patients), 0.291 (all first receivers), 0.404 (availability). Oxelumab/antidepressant: 0.508, 0.406, 0.601. The bundle does not settle which; the bar position of each threshold marker is indeterminate across defensible constructions.

### 2. Forced, or forced only by data that cannot separate the candidates
Data separate with margin. Under the golden construction (permutation null, pair-patient marginals), the seven referred pairs sit at permutation z of 10.9 to 22.8 (observed after-share minus null share over its permutation SD), and the thirteen n>=25 non-referred pairs at |z| <= 1.5. Observed multiples fall in two clusters, 0.93 to 1.03 and 1.36 to 1.49, with the 1.25 line in the empty gap. Lowest referred after-count 268 of 546 against 246.5 needed (21.5 patients, about 1.8 SD of the after count). The differences between the data-based candidates (1.36 vs 2.10 for Ternivast/gout) are far larger than sampling error and none crosses 1.25.
Noise plausibility: under the permutation null the 13 non-signal pairs give chi-square 6.83 on 13 df, 0.53 per df (lower-tail p = 0.09). Under a plain binomial null with the pair's expected share it is 2.53 on 13 df, 0.19 per df (p = 0.999), which is too tight, but that binomial variance overstates the variance once the marginals are conditioned on, so I take the permutation figure as the right test: mildly under-dispersed, plausible. Verdict: neither failure side. It is not "candidates agree only because there is no noise" (there is binomial-sized noise, slightly low) and not "differences smaller than sampling error" (separation is 7 to 15 SD for signals, 0 to 1.5 for nulls). The weak side is the availability-based pair of constructions, which differ from the data ones by modelling choice, not noise.

### 3. Does the hygiene battery move the answer
No, for the main call. Selected set of 7 is unchanged by: skipping de-duplication of re-sends (counts only: multiples 1.359 to 1.494), skipping the crosswalk (Oxelumab/antid 697 vs 694 patients, multiple 1.357), ignoring the clearance rule (multiples 1.353 to 1.431, still 7), ignoring the tracker (still 7), same-day exclusion (56 patients, shifts multiples under 0.03). Hygiene moves counts and shares only; the difficulty is in the analysis layer. In the asks, de-duplication moves the DDD of every payer (H4 159,767 vs 171,581) but no band; failing to merge H7 into H2 moves H2 from 231,566 to 120,287 DDD and H7 from 113,516 to 224,795, fees by roughly 177,000 kroner each, bands unchanged (all under 250,000).

### 4. Rounding edges (about 200 graded figures; counts are whole and medians are all whole days, so only DDD, fees and shares can sit on an edge)
| Figure | Unrounded | Distance to edge | Note |
|---|---|---|---|
| H4 DDD 159766.9 | exactly 159766.95 | 0.0 (exact tie) | half-up and half-even both give 159767.0; the golden's .9 is a float artefact. Golden wrong. |
| H6 DDD 316685.2 | exactly 316685.25 | 0.0 (exact tie) | half-up .3, half-even .2; open fork |
| H5 DDD 80973.6 | exactly 80973.55 | 0.0 (exact tie) | both conventions give .6 |
| H2 fee 361748 | 361747.5622 | 0.0622 kr (0.06 of the unit) | one fewer 0.5-DDD pack at the post-April rate (about 0.67 kr) flips it to 361747; one more does not |
| H3 fee 542791 | 542791.390 | 0.110 | within 0.11 of the edge |
| Share Midtjylland 60-74 79.6 | 79.64989 | 0.0011 of the 0.1pp unit | 364/457 vs 79.65%; one extra marker patient or one extra non-marker patient flips |
| Share Hovedstaden 75+ 79.5 | 79.54866 | 0.013 unit | 564/709; one extra row of either type flips |
| Share Hovedstaden 18-39 68.5 | 68.54839 | 0.016 unit | 595/868; one extra marker patient flips |
| Share Syddanmark 60-74 79.2 | 79.15633 | 0.063 unit | 319/403 |
| H4 fee 237117 | 237116.8754 | 0.375 | outside half unit |
Nothing else within 0.1 unit. The shares are exact counts so a solver with the right counts gets them; only the DDD ties depend on convention. For the tightest (Midtjylland 60-74) one further patient at either end of the ratio flips the printed share.

## Other findings
- Ask 5 wording: the prompt says "per authorisation holder" while the golden table is by fee payer (merger-folded). The xlsx Notes sheet and holder_register.csv close it by the fee payer rule, but the prompt's noun is "holder". Reading it as the product register's holder gives H7 224,794.5 DDD, 345,493 kr and H2 120,286.7 DDD, 184,258 kr instead of 113,515.5 / 168,003 and 231,565.7 / 361,748. Minor Gate E fork on 4 figures.
- PNG: "a bar per pair" against the golden's 20-candidate title with 23 screened pairs: 20 or 23 bars is not pinned by the prompt.
- Documentation: the dictionary says a replaced pseudonym "appears once under each" in person_register.csv; the 360 retired keys are absent from it. No arithmetic consequence (the crosswalk folds).
- Standard 3.3 asks for expected to one decimal and multiple to two decimals; none of the gaps is within that rounding.

## Gate G
`mechanism: method_or_model_selection` (null-effect-adjusted sequence symmetry versus equal chance), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No shipped artifact ranks the candidates; the naive equal-chance read is not reported anywhere. Passes.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: the deciding quantity is an expected after-count from the pair's own first-receipt dates and the launches and lapses inside the window, which is sequence symmetry analysis; it does not survive replacing the nouns. Layer 1: release rename and date-format change, re-sent lines, retired keys, package re-issue, holder merger, fee amendment. Layer 2: the temporal-trend null. Easy route a strong analyst who cleaned correctly would take: crude equal-chance (50 per cent), which files 10 pairs (adds Varenadol x3 and Admirabin x2, hides Ternivast/gout and Oxelumab/antidepressant). Caveat: the construction is unfiled and the closing sentence is 1.1; if an author reads that as a "hidden rule" this is borderline, but 1.1 and 3.2(b) both state the test in words.

## Gate F, hygiene
Stump power: moderate. Standard 1.1 and the launch/lapse dates in product_register.csv signpost the null; a strong model that builds any data-based null gets 7. Spontaneous-report counts (rising for Ternivast and Oxelumab, falling for Varenadol and Admirabin) corroborate the right 7 and soften the trap. The asks (ask 5 ties, merger, April amendment, ask 4's rejected-line basis against the chains' monthly log) carry more of the failure surface.
Hygiene: PASS. 20 files; formats csv, json, xlsx, pdf. Distractors: spontaneous_reports_summary.csv, literature_screening_log.csv, pharmacy_submission_log.csv (by submission month, wrong basis for ask 4). No authoring leakage found; no exclusion-level finding.

## Fix
- solution: H4 DDD to 159767.0; regenerate the rounding of H5 and H6 from exact decimals.
- prompt or dictionary: pin the DDD tie rule (half-up) or ask doses whole; say "fee payer" or state that holder means the fee payer; say how many bars (20 or 23); name the expected share the threshold marker uses (or ask only that the referred pairs be darker).
