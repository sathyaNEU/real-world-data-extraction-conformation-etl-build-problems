# leak check, task311

**Verdict: REVIEW.** 11 files read, 17 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: design, effect, report, central, valley, lakeshore, weighting, weights, correlation, section, published, variance, sentence, projection, decisive, weight, sample, family, concordance, weighted, centre, prompt, nothing, target, objective

## 1 file names (REVIEW 2)
- **REVIEW** `northmark_disposition_codes.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `ostrander_code_frame.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `phms_2025_technical_report.pdf`: 16 of 25 stump-paragraph terms appear (design, effect, report, central, valley, lakeshore); read whether the document names the move
- **REVIEW** `wexcombe_boost_terms_2027.pdf`: 7 of 25 stump-paragraph terms appear (design, report, section, weight, sample, weighted); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `phms_2025_technical_report.pdf`: names 8 column(s) of the data files verbatim (Health region, North, Northmark Field Research, Ostrander Data Collection, interviewer, region): confirm it is the organisation's own record and not a note written for the analyst

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader run 2026-11-01 on target.zip 2ec516f2 (isolated copy of prompt.txt and target/ only; round 3, after the prompt's rounding sentence filed the unrounded comparison).

1. None quoted. No sentence states the decisive step. The nearest is in phms_2025_technical_report.pdf section 4, "For planning, Table 2 also gives each region's intraclass correlation ... estimated from the wave's interviews; an estimate below zero is shown as zero." This names a planning input without saying how to use it.

2. None. Table 2 of the technical report ranks no candidate on the boost question. It gives 2025 estimates, SEs, design effects and ICCs on the pre-reorganisation regions, as published. Table 1 gives areas and interviews. The grant terms define the share removed but give no value.

3. Nothing is a pure analyst helper. health_regions.csv is a 5-row lookup. moh_survey_area_concordance_2024.xlsx is the Ministry's own crosswalk, which is Layer-1 work material. The two code-frame txt files are vendor records (see 8). No readme, manifest or how-to is shipped.

4. No figure reads as the answer. The Table 2 ICCs and design effects are context. Table 2 (SE and estimate) and Table 1 (areas, interviews) are 2025 figures on the pre-reorganisation regions. The fieldwork quotes xlsx carries per-interview prices, which are context or distractor material.

5. Filed sentences:
- Grant terms s.2: "1,200 completed interviews in addition to the 2027 wave's regular sample, all in one health region ... in that region's 2025 sampled areas, the same number of additional completed interviews in each of those areas, and are weighted with the region's other 2027 interviews in the Centre's usual way. Apart from the boost, the 2027 wave repeats the design of the 2025 wave." This fixes the population (the region's 2025 areas), an equal split per area, and the design.
- Terms s.3: "one minus the ratio of the standard error that estimate would have with the boost to the standard error it would have without it ... the standard error being the one the Centre publishes for a regional estimate (2025 Technical Report, section 4). Health regions are the regions as constituted ... from 1 April 2024." This fixes the share formula, the SE type and the region basis.
- Report s.3 and s.4: equal final weight within an area; Taylor linearisation with areas as PSUs, with replacement within strata; the Central Valley supplement is its own stratum.
- Report s.5 and s.6: complete means reaching the end of section D; another adult counts as complete; DK and refused are left out; no-prescription households count as not going without.
Read literally, the main figures (shares, the region that gets the boost, the runner-up) are determinate. Possible open points: (a) the runner-up boost is a per-area integer, "smallest boost, in whole interviews per area", and the boost the foundation pays for is 1,200 split over areas, which may not divide evenly. (b) The 2024 estimates are asked on the post-reorganisation regions, so the weighting and the area mapping for 2024 must be reconstructed from the concordance. I find no wording that leaves a figure open to two values, but I did not compute any.

6. An analytical choice. The decision rests on how a cluster design's SE responds to extra interviews per fixed area (between-area against within-area variance, per region, with the supplement stratum), not on a stated rule or a field. The sentence closest to it is the terms s.3 "share ... removed ... on the evidence of the 2025 wave". The case files themselves do need code reading (disposition codes, reissues, area renumbering). That is Layer 1 and not the decider. Classification: analytical, with data cleaning as supporting mess. One caution: the report's published design effects and ICCs, if used directly, give a shortcut that may not match the unclipped, stratified computation. That is analysis, not a leak.

7. Realism:
- phms_2025_technical_report.pdf: Table 1 totals reconcile (700+2504+1210+1162+2516=8092; 20+80+100+40+60=300). The rounded design-effect and SE values look plausible. No narrating tell found.
- Table 2 pairs Households answering with Table 1 interviews (695 against 700, etc.), which is natural.
- northmark export: sequential case numbers, listing lines and ISO dates. Fine.
- Ostrander JSON: day/month/year dates, a different code set and area labels (CVL-034). A believable second vendor.
- The concordance maps Northern areas into new Lakeshore numbers 3098 to 3100 in sequence, which is regular but consistent with "renumbered in one sequence".
- Pharmacy register: brand names with numbers such as "Remedy'sRx #5832" and a uniform small set of fee values. Mildly synthetic but a distractor.
- Quotes xlsx: tidy; the North note "boost interviews at the same rate" reads slightly written for the task but is harmless.
- Terms letter: the dates fit the timeline (9 October 2026, due 6 November 2026).
Nothing serious.

8.
- northmark_disposition_codes.txt: harmless. It is a vendor code list (disposition codes and the Q_RX_COST value labels) in the vendor's own style, release 7.4. It describes codes, not the data's content or the method.
- ostrander_code_frame.txt: harmless. Same reasoning; it is a vendor code frame (v2.1, dated 27 January 2025) with a different code set. The reader must map both to one scheme, which is Layer 1.
- phms_2025_technical_report.pdf: harmless with one note. Column values it names (the three completion-status rules, the 'no prescription' answer) are the organisation's own definitions and make the file the governing document. It publishes 2025 SEs, design effects and ICCs. I did not compute whether any equals a graded figure, so I cannot confirm the overlap the sweep flagged. As the pre-reorganisation 2025 table it cannot be copied as an answer to a 2027 post-reorganisation question. Section 7's remark that the 2024 estimates are on the old regions is a statement of fact the task needs.
- wexcombe_boost_terms_2027.pdf: harmless. It is the funder's grant letter. The overlap with the author's notes comes from the letter being the governing definition of the estimand (share removed, regions from 1 April 2024). It states what is asked, not how to compute it.

9. Forks:
- "the region that gets the boost, the runner-up": the runner-up is the second-ranked region on share removed. This is clear and ties are unlikely.
- "smallest boost, in whole interviews per area, that would remove a larger share of the runner-up's error than the 1,200 remove in the region that gets them": this compares the runner-up's share at a per-area boost against the winner's share at 1,200 total. Both are unrounded, per the prompt's "compared unrounded". The reading "larger than" (strict) against "at least" is stated. A solver might ask whether the boost is split over the runner-up's areas as the winner's is, which the terms fix.
- "2024 completed interviews": the prompt says on the regions as they have stood since the reorganisation. The report says the 2024 estimates were published on the old regions, which is a Layer-1 conversion and not a fork.
- "completed interviews" for 2024: the report s.5 defines complete (CI, CP count; partial interviews not used). Closed.
- "standard error ... percentage points to two decimals": the SE is the Centre's published type (Taylor, areas as PSUs, with replacement within strata), filed in s.4.
No reading I can find gives two answers.
