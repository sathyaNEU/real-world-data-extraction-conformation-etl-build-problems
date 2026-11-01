# task311: which health region the foundation's 2027 boost of 1,200 interviews goes to

Wave 7, Opportunity Sizing & Decision Support. Architecture 1, drawn 2026-10-27, redesigned at stage 2 on 2026-11-01.
Seed OS13 (a public charging coverage figure) was read for its world only: its mechanism is a site-unit reading (data
semantics) and its state energy office repeats task310's organisation family, so the number moved to Survey Research &
Official Statistics. No probe, reader or solver is run (the STOP rule); the stump is argued on paper here and measured
on the generator's clean truth.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | survey-research-official-statistics / sample-design-allocation-weighting (serves Opportunity Sizing) |
| Objective | Opportunity Sizing & Decision Support: the headline is the precision the boost buys in each region, sized from the pool (1,200 completed interviews) to the realisable (the share of the region's 2027 standard error they remove), and the sizes decide the region |
| Decision / answer unit / question form | pick_one_of_n / named_option (one of five health regions) / where |
| Shape | 13: five placement scenarios (the boost in each region) each with the share of the 2027 error it removes, the call, the runner-up, the flip point (the smallest boost in whole interviews per area at which the runner-up removes a larger share than the call's), plus the 2024 ask |
| Gap / pattern / generators | objective (the 2025 error and its design effect are correct and are not what the boost is scored on), time / none / G2 (interviews against areas), G17 |
| Gate G / strategy | binding_constraint (the between-area variance the fixed areas carry is a floor no added interview moves) / uncertainty_hold (the decisive quantity is the precision a sample change buys) |
| Layer 2 | estimation_fit, own:boost-precision-through-area-weights-not-held-design-effect |
| Forum / forcing event / org family | funder_or_donor (the foundation releases the boost on the centre's placement) / purchase_order_or_contract (the 2027 fieldwork contract is let on the placement) / research_or_statistics_office |
| Stakeholder | the director of a university survey research centre (statistical_office_head); the prompt carries no persona |
| People (guard.py names --geo CA --seed 311) | Heidi Roberts, director of the Survey Research Centre; Jeremy Morris, the foundation's programme director; Jason Clarke, the centre's sampling statistician (redrawn at stage 2: the faker pool behind the seed moved and Schmidt carried a people.last WARN) |
| World | the Provincial Household Medicines Survey, run by Halvorsen University's Survey Research Centre for the province's Ministry of Health since 2019: an area panel of 300 survey areas in five health regions (a Central Valley supplement of 20 new-subdivision areas since 2023), each area worked to a fixed take of completed interviews, waves 2023, 2024 and 2025 fielded by Northmark Field Research and, from 2025 in two regions, Ostrander Data Collection; the ministry reorganised the regions and renumbered the areas on 1 April 2024; the Wexcombe Foundation funds 1,200 extra interviews in one region in 2027 |
| Deliverables | boost_region_2027.xlsx (the placement workbook), boost_memo_2027.pdf (the memo to the foundation with its chart) |
| Guard | WARN only, rerun 2026-11-01 on the registered card: overuse.objective (the lane's), repeat.gate_g (binding_constraint after task310: here the binding quantity is a variance component, not an export limit), repeat.decision (pick_one_of_n after task305 v3), repeat.deliverables (answered: the memo moved from docx to pdf), people.last (answered by the redraw) |

**The data-native sentence:** the centre works every area to a fixed take of completed interviews, and in the Central
Valley the 2023 supplement of new-subdivision areas carries a third of the region's households on a take of five
interviews an area, so each supplement interview carries about twelve times the weight of a core interview; an equal
boost in every area multiplies the supplement's take by four and the core's by a third more, which narrows the spread of
the weights as well as adding sample, while in the North, where whole communities share one pharmacy, most of the error
sits between areas the boost cannot add.

**The abstraction sentence:** the precision an equal addition to every group buys is set by how the present error divides
among the groups and how the addition reshapes the weight each record carries, so summarising the present error by its
average group size and one weighting factor misprices the groups whose share of the error comes from their small size.
Against the nearest drivers on file (task486, published small-area counts with added noise; task269, a test's
reliability projected from examiner variance; task190, a ratio with a complete numerator) the sentence does not hold: none
projects a sampling error under a changed take, and none turns on an addition reshaping the weights.

**Sources:** every file is constructed (synthetic, CC0, recorded in metadata.json): the two contractors' case exports, the
weighting system's area table, the ministry's concordance, the region list, two code lists, the technical report, the
grant terms and two distractors (a pharmacy register, the 2027 fieldwork quotes).

## Survivor anatomy

- **Actor:** the deciding property (how much of a region's error sits in areas whose small takes an equal boost multiplies, and how far the boost narrows the weights) has no column: each area's weight sits in the weighting system's table on the pre-2024 numbering, its take is a count of case rows in two contractors' exports, and the share is a relation between the two at the area grain that no file stores.
- **Link:** the weights reach the 2025 interviews only through the ministry's concordance (new numbers to old), and the comparison that decides, each area's weight share against its take before and after the boost, is one the field's design-effect projection never asks for: Kish's factorisation summarises the weights into one weighting effect and the takes into one average.
- **Reflex:** Kish's design-effect projection, the field's named method for an error under a changed take, sits at rung 1 and files Lakeshore; count scaling, rung 0, files the North.
- **Back-test:** the textbook route validates: Kish's factorisation, the weighting effect times one plus the average take less one times the report's correlation, comes within half a point of every published 2025 design effect (the North 7.23 against 7.69, the Southern Uplands 1.90 against 1.94, Metro 2.10 against 2.25, Lakeshore 1.00 against 0.88), and puts the Central Valley's weighting effect (3.38) above its design effect (3.11), which the Kish analyst reads as no clustering at all (its correlation shown as zero); the route checks out region by region, and nothing in the check moves the weighting effect it holds.
- **Second use:** every file the decisive step reads is in the pack for the 2025 estimates and the 2024 ask anyway (the exports, the weights table and the concordance for every estimate, the technical report for the published table and the method, the terms for the objective); deleting the decisive step drops no file.
- **Shock:** the Central Valley is extreme on no shipped statistic a reader sorts: its 2025 estimate, standard error and design effect sit inside the range (its estimate 9.0 per cent between the Southern Uplands' 13.5 and Metro's 7.2, its error 1.01 points between the Southern Uplands' 1.40 and Metro's 0.78, its design effect 3.11 second to the North's 7.69, its 2,476 households answering second to Metro's 2,501), its correlation of 0.000 is shared with Lakeshore, so a sort on it does not separate the two (and with no clustering in either, the Kish route funds Lakeshore), it holds neither the most nor the fewest interviews, and the North carries the widest error and the largest design effect.
- **Pins:** the terms file the WHAT in a grant-terms genre (the objective, the boost inside the 2025 areas with an equal number per area, the usual weighting, the 2025 design, the 2025 wave as the evidence, the regions from 1 April 2024); no filed sentence names the weighting effect, the takes, the components or how the 2027 error is projected.

## Default path

1. Read the terms (sections 2 and 3): the boost of 1,200 completed interviews goes equally into a region's 2025 sampled areas, and the region is the one whose 2027 standard error (the kind the centre publishes) loses the largest share, both errors reckoned the same way for the 2027 design on the evidence of the 2025 wave.
2. Assemble the 2025 complete and proxy interviews with a usable answer from both contractors' exports, attach each area's final weight from the weights table through the concordance, and reproduce Table 2 of the technical report (each region's estimate, standard error by Taylor linearisation with areas as primary sampling units within strata, design effect and intraclass correlation).
3. Take each region's intraclass correlation from Table 2 into Kish's factorisation, deff = deff_w x (1 + (m - 1) rho) with the weighting effect deff_w = 1 + cv squared of the weights (the Central Valley's design effect is all weighting effect, its correlation nil), project the 2027 design effect at the boosted average take m + 1,200/k with the weighting effect held at its 2025 value, and scale: SE 2027 = SE 2025 x root(n / (n + 1,200) x deff 2027 / deff 2025).
4. Fund the region with the largest share removed.

**Ends on:** Lakeshore, 29 per cent of its 2027 standard error removed (the Central Valley 18 per cent).

**Golden:** Central Valley (44 per cent removed, Lakeshore second at 29 per cent), projected area by area from the report's
intraclass correlation through each area's own weight share with every area's take raised by the boost.

Below rung 1 sits count scaling (rung 0): the 2025 error scaled by the root of the interviews before over after, the
design effect held, which funds the North (39 per cent, the region with the fewest interviews).

## Stump sentence

A competent analyst reproduces each region's published 2025 design effect, puts the report's intraclass correlation into
Kish's factorisation of it, projects the design effect at the boosted average take with the weighting effect held at its
2025 value and funds Lakeshore; but a third of the Central Valley's households sit in its
supplement areas on five interviews an area, an equal boost quadruples their take and narrows the weights, so projected
area by area through the design's own weights the boost removes 44 per cent of the Central Valley's error against 29 per cent of
Lakeshore's.

## Three rules

- **Task type:** survey-research-official-statistics / sample-design-allocation-weighting, which serves Opportunity Sizing: the boost is sample allocated to one region and sized by the precision it buys, from the pool of 1,200 completed interviews to the realisable share of the region's 2027 standard error they remove.
- **Domain test:** the deciding quantity is the standard error a two-stage weighted cluster sample will give a regional estimate once every area's take is raised, which survey sampling projects from the design itself, each area's weight share and take, and from the between-area and within-area variance the outcome carries.
- **Swap:** "put the 1,200 extra interviews in the Central Valley" becomes "put 1,200 extra hospital beds in the Central Valley": beds carry no sampling error, no areas they are drawn within, no selection weights and no take to raise, so nothing in the projection survives.
- **Layer 1:** two contractors' case exports with their own code frames, date formats and layouts (each contractor's case system); the 2024 reorganisation (the ministry's concordance, the 2025 exports on the new numbering and the weighting system's table on the old); partial and proxy interviews under disposition codes; refusals reissued under new case numbers; addresses withdrawn once an area's take is reached; don't-know and refused answers; the no-prescription answer. Nothing is placed to be caught, and each mishandling is asserted to leave the call.
- **Layer 2:** estimation_fit: the projection of a weighted two-stage design's error under a changed take; the choice that flips the call is carrying the boosted takes into each area's weight and variance instead of holding the design effect's weighting part at its 2025 value.
- **Decisive step:** recognising that an equal boost in every area lifts small takes proportionally most, so in the Central Valley it narrows the weights the supplement's small takes spread as well as adding interviews, and projecting each region's 2027 variance area by area as the sum of each area's squared weight share times the between-area part plus the within-area part over the boosted take (the parts from the report's intraclass correlation).
- **Not semantics:** every field read correctly (both contractors' codes, the concordance, the disposition codes, the completeness rule, the no-prescription answer) and the report's correlation read as published leave the analyst with the correct 2025 estimates, errors, design effects and correlations, and Kish's projection with the weighting effect held is the field's own; no field, code or definition says how an equal boost changes the weights.
- **Not rule application:** no filed rule projects an error under a changed take: the terms file the objective, the boost and the evidence, the report files the weighting, the variance method and each region's intraclass correlation, and executing them with Kish's projection files Lakeshore. Spread: the enumerated family (fifteen constructions: count scaling; Kish from the total design effect, with the weighting effect divided out, with the published correlation, with an ANOVA or a REML correlation; the projection through the area weights with the published correlation, ANOVA, REML or Kish's weighting effect recomputed at the boosted takes; and the readings a filed sentence rules out, the published 2025 error as the error without, the unfloored design-based remainder, weighted ANOVA, design-based and by-stratum components) files the North (one), Lakeshore (five) or the Central Valley (nine), the Central Valley's share running 5 to 48 per cent; the standing family (the four through the area weights) files the Central Valley at 44 per cent with Lakeshore second at 29 per cent, a spread of zero whole points on every share; what rules the Kish routes out is quiet: the report's weighting rule (an area's weighted dwellings over its completed interviews) applied at the 2027 takes, which no sentence connects to the boost.
- **Analyst test:** a strong analyst who joins both contractors' exports, attaches the weights through the concordance and reproduces the published 2025 design effects puts each region's published intraclass correlation into Kish's factorisation, projects the design effect at the boosted average take with the weighting effect held, and funds Lakeshore at 29 per cent removed.
- **Estimand:** the terms, section 3: the region in which the boost removes the largest share of the standard error of its 2027 estimate of households in which someone did not fill a prescription in the past 12 months because of its cost, the share one minus the ratio of the error that estimate would have with the boost to the error it would have without it, both reckoned in the same way for the 2027 design on the evidence of the 2025 wave, the error the kind the centre publishes for a regional estimate (report section 4), the regions those from 1 April 2024; section 2 files the boost (1,200 completed interviews, the same number in each 2025 area, weighted the centre's usual way) and the 2027 design (the 2025 design repeated).
- **No decoy:** nothing is planted: the published design effects and intraclass correlations are the report's ordinary table and reproduce exactly from the files; no memo, draft, briefing or stakeholder figure names a region, a share or a projection.
- **No certified replay:** no file states a 2027 error or a share removed; the published 2025 table certifies the 2025 errors, which every route reproduces and none recovers a method from.
- **Lesson:** the precision an addition buys depends on where the existing error sits and how the addition changes the design's weights, not on the size of the present error or on its design effect; no build on file teaches projecting a weighted cluster design's error under an equal boost per area.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 count scaling, the North | none | none | yes, the scaled error | none | none | yes, one ratio of counts | none | readable |
| R1 Kish from the total design effect, Lakeshore | the report publishes the design effect | none | yes, Kish's roh | none | none | no | none | readable |
| R2 Kish with the published correlation, the weighting effect held, Lakeshore | the report publishes the correlation for planning | none | yes, Kish's factorisation | none | none | no | none | readable |
| R3 (decisive) components through the area weights at the boosted takes, the Central Valley | no: the terms file the equal boost and the report the weight rule, and no sentence connects them | no: no column holds a take, a weight share or a weighting effect | no: the field's reflex is the summary design effect | none | no | no: a sum over areas of weight shares and takes | no: the weights, exports, concordance and report serve every estimate | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | health region | the regions from 1 April 2024 | the pre-2024 regions the weights table carries | same call (asserted) | terms section 3, "the regions as constituted by the Ministry of Health from 1 April 2024" |
| SF2 | the 2027 estimate | households in which someone went without, all households answering, no-prescription households counted as not going without | the share among households with a prescription | same call (asserted) | report section 6, "Households with no prescription to fill in the period count among the households that did not go without" |
| SF3 | the boost | 1,200 completed interviews | 1,200 usable answers, or 1,200 issued addresses | same call and shares (asserted); addresses ruled out | terms section 2, "1,200 completed interviews" |
| SF4 | the same number in each area | 1,200 over the region's 2025 sampled areas, a whole number in every region | areas counted on the pre-2024 regions | same call (asserted) | terms section 2, "that region's 2025 sampled areas" with section 3's regions |
| SF5 | the standard error with and without | both projected for the 2027 design on one basis | the realised 2025 error as the error without, a model error with | same call (asserted); other shares | terms section 3, "both reckoned in the same way for the 2027 design on the evidence of the 2025 wave" |
| SF6 | the share removed | one minus the ratio of the standard errors | the share of the variance removed | same call (asserted) | terms section 3, "one minus the ratio of that standard error with the boost to the same standard error without it" |
| SF7 | the 2025 sampled areas | every area of the region, the Central Valley supplement included | the core areas only | a different call; ruled out by text | report section 2 (the supplement areas are sampled areas, visited every wave) and terms section 2, "each of those areas" |
| SF8 | weighted the usual way | the boost's interviews share their area's weight, recomputed at the boosted take | a separate weight for the boost's interviews | same call | terms section 2, "weighted with the region's other 2027 interviews in the Centre's usual way" with report section 3 |
| SF9 | the evidence | the 2025 wave | components pooled over 2023 to 2025 | same call (asserted) | terms section 3, "on the evidence of the 2025 wave" |
| SF10 | the 2027 design | the 2025 areas, takes and listings repeated | the 2025 realised takes where an area fell short | same call (asserted) | terms section 2, "the 2027 wave repeats the design of the 2025 wave" |
| SF11 | rounding | each share computed unrounded, rounded once to a whole per cent | shares rounded before ranking | same call | the prompt's last sentence |
| SF12 | an area's take in the projection | its usable answers | its completed interviews | same call and whole-per-cent shares (asserted) | convergence (C1), asserted |
| SF13 | strata | the five regions with the Central Valley supplement a stratum of its own | the Central Valley one stratum | same call (asserted) | report section 4, "the Central Valley supplement being a stratum of its own" |
| SF14 | the runner-up's boost | the smallest whole boost per area whose share removed, unrounded, is strictly larger than the call's | an equal share, or the shares compared as whole per cents (28 per area once the takes are counted as completed interviews) | same boost at the golden's takes (asserted); the whole-per-cent comparison ruled out by text | the prompt, "that would remove a larger share of the runner-up's error than the 1,200 remove in the region that gets them" and "Shares are whole per cents, compared unrounded" |
| SF15 | the between-area part | the report's intraclass correlation as published (three decimals) | the correlation re-estimated unrounded, by analysis of variance or REML, from the 2025 interviews | same call, whole-per-cent shares and runner-up boost (asserted) | report section 4 and Table 2; C1 |
| SF16 | the within-area part | one minus the published correlation (a share removed is scale-free) | a binomial p(1 - p) as the within part beside an analysis-of-variance between part | same call and whole-per-cent shares (asserted, weighted or unweighted p) | report section 4 and Table 2; C1 |
| SF17 | a between-area estimate below zero | zero, as the report shows it | the design variance less the within part kept negative (the Central Valley 48.0, Lakeshore 34.4) | same call (asserted); other shares | report section 4, "an estimate below zero is shown as zero", and Table 2 |
| SF18 | the 2027 takes | each 2025 area's own count, repeated | each stratum's nominal take (35, 40 and 5, 12, 29, 42) | same call, whole-per-cent shares and runner-up boost (asserted) | terms section 2, "the 2027 wave repeats the design of the 2025 wave"; C1 |
| SF19 | strata for the 2024 errors (ask side) | the five health regions as reorganised, the Central Valley supplement a stratum of its own | the pre-2024 regions as strata | same call (the call reads no 2024 row); the North's 2024 error moves | report section 4, "The strata are the five health regions, the Central Valley supplement being a stratum of its own", and Table 2's 2025 errors reproduce only on those strata (asserted) |

## Ladder

Measured on the shipped sample (generator seed 312377; checks.py asserts every row):

| Rung | Route | Pick | Shares removed, best first | Margin |
|---|---|---|---|---|
| R0 | count scaling | North | North 39.4, Southern Uplands 30.0, Lakeshore 29.2, Central Valley 17.9, Metro 17.8 | 1.31x |
| R1 | Kish, rho from the total design effect | Lakeshore | Lakeshore 34.8, Southern Uplands 13.6, Metro 7.3, Central Valley 5.0, North 3.4 | 2.56x |
| R2 | Kish with the published correlation, the weighting effect held (the default path) | Lakeshore | Lakeshore 29.2, Central Valley 17.9, Southern Uplands 14.0, Metro 7.8, North 3.7 | 1.63x |
| R2b | Kish with rho from the design effect over the weighting effect, or an ANOVA or REML rho, the weighting effect held | Lakeshore | Lakeshore 29.2, Central Valley 17.9, Southern Uplands 13.6 to 14.2, Metro 7.3 to 7.8, North 3.4 to 3.7 | 1.63x |
| R3 | through the area weights at the boosted takes, the report's correlation (golden; ANOVA, REML and Kish recomputed agree) | Central Valley | Central Valley 43.9, Lakeshore 29.3, Southern Uplands 14.1, Metro 7.8, North 3.6 (the family: the Central Valley 43.9 to 44.1, Lakeshore 29.3, the Southern Uplands 14.1 to 14.2, Metro 7.8, the North 3.6 to 3.7) | 1.50x |

- **Readings a filed sentence rules out, each keeping the call (checks.py):** the published 2025 error as the error without (the Central Valley 42.1, Lakeshore 24.5); the unfloored design-based remainder (48.0, 34.4); weighted ANOVA, design-based and by-stratum components (43.9 to 44.1, 29.3).
- **Position:** the Central Valley is fourth on rung 0 (17.9 against Metro's 17.8), fourth on R1, second on the Kish rungs only (each names Lakeshore, which leads it 1.63x there), never first before the decisive rung.
- **Dominance:** the decisive edge (the Central Valley over Lakeshore on R3, 14.6 points) against the Kish route's carried advantage (Lakeshore over the Central Valley on R2, 11.3 points): 1.29 times.
- **The pricing sequence.** 1, the residue the filed WHAT leaves is the projection (a method, not a knob). 2, the move needs the Central Valley's share to rise past Lakeshore's: from 18 per cent to above 29 per cent, and the boost's reshaping of the weights carries it to 44 per cent. 3, the one-group-by route (count scaling) files the North; its algebra is a function of n alone. 4, the step estimates nothing it can lose to noise: on this sample the Central Valley's and Lakeshore's between-area variance is nil under every estimator (the report shows both correlations as 0.000), so their shares and the runner-up's boost are pure design quantities; the clustered regions' shares agree to a whole point across the family and are pinned by the published correlation. 5, the lever (the boosted takes in the weights) is not the ranked quantity's noise: the Central Valley's share does not depend on an estimated component here. 6, no change call. 7, no subset prints the hidden quantity. 8, the reflex sweep: every Kish variant and count scaling run as code (checks.py), none files the Central Valley.
- **Flip point:** Lakeshore removes a larger share than the Central Valley's 43.9 per cent only at 27 more interviews per area, 2,700 interviews (44.5 per cent); 26 per area leaves it at 43.8 per cent; compared unrounded or as whole per cents, and at the strata's nominal takes, the same 27 (SF14, SF18).
- **Truth:** the world's own components (no estimation) put the Central Valley first as well (checks.py).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the region's 2025 sampled areas and their complete and proxy interviews with a usable answer | report sections 2, 5 and 6; C1 |
| 2 Unit of account | the household (one interview a household) | report section 1; the terms' estimate |
| 3 Attribution window | the 2025 wave | terms section 3, "on the evidence of the 2025 wave" |
| 4 As-of dating | the 2025 listing for the weights; the 2027 design repeats 2025 | terms section 2; report section 3 |
| 5 Version basis | the regions from 1 April 2024 | terms section 3; the concordance |
| 6 Denominator | all households answering, no-prescription households counted as not going without | report section 6 |
| 7 Weighting | the report's area weight; the boost weighted the usual way | report section 3; terms section 2 |
| 8 Window length | one wave | terms section 3 |
| 9 Boundary inclusivity | a closed wave worked to fixed takes; no boundary | C1 |
| 10 Rounding path | shares unrounded, rounded once to whole per cents | the prompt |
| 11 Tie-break | none needed (margin 1.50x) | C4 |
| 12 Maturity and censoring | none (a closed wave) | C1 |
| 13 Order of operations | weights per area before the estimate; the ratio is basis-free | C1 |
| 14 Row order | no effect | C1 |
| 15 Duplicate resolution | a reissue is its own case; no complete appears twice | asserted |
| 16 Identity normalisation | the concordance maps new numbers to the weights table's old; Ostrander's area labels to the numbers | the concordance (C4: the raw join mismatches) |
| 17 Netting against gross | none | n/a, recorded |
| 18 Dimensional units | shares in per cent, errors in points | the prompt |
| 19 Code and status semantics | each contractor's code list | the code lists; never the stump |
| 20 Integerisation | 1,200 over every region's areas is whole | C1 |
| 21 Clause scope | terms section 3 applies to every region alike | the terms |
| 22 Forward window contents | the 2027 wave repeats 2025, the boost the only change | terms section 2 |

## Literal reader

Executing the terms word for word: the boost of 1,200 completed interviews is spread equally over each region's 2025 areas
and weighted the centre's way (report section 3), and each region's 2027 standard error with and without it, both reckoned
the same way for the 2027 design on the evidence of the 2025 wave, the error the kind the centre publishes (report section
4, whose Table 2 gives each region's intraclass correlation for planning), is the error the 2027 design will carry; the
terms leave the projection to the analyst, every term reads one way (SF1 to SF19, each closed by a quoted sentence or an
asserted same call), and the easy answers (the North, Lakeshore) come from easy projections of the same literal estimand,
never from another reading.

## Oracles

- Table 2 of the technical report (the 2025 estimates, errors, design effects and intraclass correlations) is reproduced exactly by every route; it confirms every route's 2025 baseline and ranks no placement.
- Kish's factorisation with the published correlations comes close to Table 2's design effects (the Central Valley's 3.11 against a weighting effect of 3.38, Lakeshore's 0.88 against 1.00, both correlations nil), so the textbook route checks out against the report: a second source agreeing on the wrong route too, never an arbiter.
- Nothing ties only under the golden.

## Ask sheet

- **The 2024 ask: each region's 2024 completed interviews, estimate (per cent to one decimal) and standard error (percentage points to two decimals) on the regions as they have stood since the reorganisation (15 figures).** H18 home: the precision history the memo sets beside the boost (each region's 2024 error on today's regions, never published, since the 2024 report used the old regions), a measure every region carries that the call does not turn on. Use: the foundation reads each region's error before the boost beside the 2027 projection. Path: Northmark's export (its 2024 rows), the weights table (its 2024 rows), the ministry's concordance and the report's sections 3, 4 and 7 (four files; wave, case_no, area_at_assignment, assigned, disposition, q_rx_cost, area_pre2024, stratum, design_weight, occupied_dwellings and the concordance's four columns).
- **Primary device: D2 with D7, a label at the wrong vintage on a key whose meaning changed.** The ministry's reorganisation took effect on 1 April 2024 and renumbered each region's areas in one sequence, so most new numbers name a different area than the same number named before, and seventeen new numbers name an area in another region than the same old number. Northmark's case system took the new numbers up on 22 April 2024 and each case carries the number in force on the day it was assigned (its column is area_at_assignment): cases assigned before 22 April carry pre-2024 numbers, later cases the new ones. The battery's repair (a number the pre-2024 series holds read as pre-2024, any other as new) misplaces every case assigned from 22 April; the filed date (the concordance's and the report's 1 April) misplaces every case assigned from 1 to 19 April; nothing dates Northmark's switch. The data pin it: the first number the pre-2024 series never had (5059) is assigned on 22 April, and reissues assigned on Friday 19 April carry their originals' pre-2024 numbers.
- **Forcing (asserted on the shipped rows, ceiling.py):** read with the switch between the last pre-2024-only number (an area's batch on Friday 19 April) and the first new-only number (Monday 22 April), with no assignment on 20 or 21 April, every case falls in a numbering that holds it and every cut between those two batch days gives the same figures; the three careful-path readings each miss all fifteen figures at their stated rounding: the battery's repair moves the counts by 12 to 78, the estimates by 0.36 to 2.70 points and the errors by 0.005 to 0.537; the 1 April split by assignment date moves the counts by 4 to 125, the estimates by 0.08 to 0.88 and the errors by 0.085 to 1.208; the same split by disposition date the counts by 4 to 125, the estimates by 0.10 to 0.95 and the errors by 0.043 to 1.207.
- **Hazards:** H1 the weights table on the pre-2024 numbering (the concordance join, which the battery makes); H2 refusals reissued under new case numbers (only completes count); H3 the no-prescription code counted among households that did not go without (report section 6).
- **Stops (asserted):** the battery's repair, the 1 April split by assignment and by disposition date, every number read as pre-2024 and every number read as new each keep none of the fifteen figures; the golden handling keeps all fifteen.
- **Pin test:** the asking sentence pins the year (2024), the regions (as they have stood since the reorganisation) and the figures (completed interviews, the estimate and its standard error, the report fixing the method); the device sits in which numbering each 2024 case carries, which no pin names; the export's column name says what the number is, nothing dates the switch.
- **Realism:** a contractor's case system takes up a reorganised code frame some weeks after a ministry's effective date and stamps each case with the number in force when it was assigned; the centre's weighting system still keys areas on the old numbers.
- **Main population zero-counts (asserted):** the main call reads no 2024 row and every 2025 case carries its new number; the ask reads no 2025 row.
- **Hazard table:** H1 moves every 2024 figure when the join is skipped (the weights then miss); H2 and H3 move nothing on the golden handling (asserted through the shared readers).
- **Referee:** none: no file holds a 2024 total by region on either set of regions.
- **Residual risk, recorded:** the layer stands on one primary; the full includer, who reads the switch from the numbers the old series never had, keeps all fifteen, and with the call landed the pair with a mirror-includer would be 83.5.

| Ask row | The cracker (lands the call, runs the hygiene battery, executes every filed rule) | Verdict |
|---|---|---|
| 2024, North (completed interviews, estimate, error) | the numbers the pre-2024 series holds read as pre-2024: cases assigned from 22 April land in the wrong areas, three North areas' cases in Lakeshore | miss |
| 2024, Central Valley | the same reading puts the supplement's late cases in core areas at core weights and two Central Valley areas' cases in the North | miss |
| 2024, Lakeshore | the same reading adds the North's misread cases and loses three areas' cases to Metro | miss |
| 2024, Southern Uplands | the same reading adds Metro's and the Central Valley's misread cases | miss |
| 2024, Metro | the same reading adds Lakeshore's misread cases and loses three areas' cases to the Southern Uplands | miss |

- **Measured by:** generator/ceiling.py on the cut pack (target.zip 2ec516f2): the cracker keeps 0 of 15 under the battery's repair and under both 1 April splits; the mirror, on the same ask paths, the same.
- **Pair ceiling:** 28.5 (the cracker 38 + 7 + 55 x 0/15 = 45.0; the mirror at the Kish rung, 5 + 7 + 55 x 0/15 = 12.0).
- **Mirror leakage:** 0.0 per cent of ask weight.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| Two code frames, date formats and layouts | each contractor's case system | both exports | a contractor's proxy code dropped | call unchanged |
| The 2024 renumbering | the ministry; the weighting system still on the old numbers | concordance, weights table | weights joined on the raw number | call unchanged |
| Partial interviews | both case systems | both exports | partials with an answer kept | call unchanged |
| Proxy interviews | both case systems | both exports | dropped | call unchanged |
| Reissued refusals under new numbers | both case systems | both exports | none on completes | call unchanged |
| Withdrawn addresses | the fixed-take fieldwork | both exports | counted as non-response | none on the call |
| Don't know and refused | the item | both exports | read as no | call unchanged |
| No prescription to fill | the item | both exports | dropped from the denominator | call unchanged |
| The old regions in the weights table | the weighting system | weights table | used as regions | call unchanged |

## Leak check

- leak.py (2026-11-01, target.zip 2ec516f2, --asof 2026-11-02): REVIEW, no LEAK. Rulings: the two code lists
  (northmark_disposition_codes.txt, ostrander_code_frame.txt) are each contractor's own code list, the producing system's
  form, carrying item labels and codes and nothing about how the files fit together, harmless; the technical report's
  and the terms' stump-paragraph words (16 and 8 of 25: design, effect, weighting, variance, the region names, section,
  weight) are the field's ordinary vocabulary in the genre's own sections, and checks.py asserts that neither document
  carries the decisive vocabulary (weighting effect, variance component, take of five, between-area, weight share,
  projected, the switch date), harmless; sweep 12's eight names in the report are region and contractor names and the
  word interviewer, not a gloss on any column, harmless; the answer-figure sweep is clean on this cut.
- The single-use test on the sentences the judge repair added. The report's intraclass correlation column is the planning
  figure survey reports publish (it serves any sample-size calculation for any region and feeds Kish's route exactly as
  well as the golden's). The deletion test: on this sample the Central Valley's and Lakeshore's between-area variance is
  nil under every estimator, so deleting the column moves no call, no top-two share and not the runner-up's boost; it
  pins only the clustered regions' shares, which is the fork it closes. The terms' "both reckoned in the same way for the
  2027 design" files the comparison (WHAT) and names no method.
- The reader, round 2 (target.zip 2ec516f2, an isolated copy of prompt.txt and target/): question 1 none; 2 none; 3 none;
  4 none (Table 2's North row read as context); 5 every quoted sentence executes to the golden's estimand, and its 2024
  note (no 2024 source seen) is answered by the Northmark export, which carries the 2024 wave; 6 an analytical choice; 7 no
  tell beyond the fixed takes' regular counts, which the report's design states; 8 every flagged file harmless; 9 the
  whole-per-cent reading of the runner-up's boost is closed by convergence (SF14: unrounded and whole-per-cent comparisons
  both give 27 per area).
- The reader, round 3 (target.zip 2ec516f2, after the prompt's rounding sentence filed the unrounded comparison): question 1 none (the nearest, the report's planning sentence, names an input without saying how to use it); 2, 3 and 4 none; 5 the main figures determinate on a literal reading; 6 an analytical choice; 7 nothing serious: the fieldwork quotes' North note (boost interviews priced at the same rate) is the contractor's commercial term in a distractor the criterion never reads, harmless; its reading of Table 2 as on the pre-reorganisation regions is answered by report section 7 ("The 2025 estimates in this report are on the regions as reorganised"); 8 every flagged file harmless; 9 no reading with two answers, the runner-up's comparison unrounded per the prompt.
- The reader, round 1 (target.zip 08eedf9f): its question 6, "an analytical choice with a rule-application element", is
  ruled by measurement (R3a: executing every filed sentence with Kish's projection files Lakeshore, so the filed rules do
  not reach the call); its realism tell (1,205 completed interviews in two regions) was fixed by the Southern Uplands'
  take of 29; its "match" fork by the strictly larger share the prompt now asks for.

## Pre-ship check

- **The 10/10 rules against the built pack.** The domain test holds: the call turns on the expected design-based error
  of a weighted two-stage sample under a changed take, worked from the pack's microdata, weights and design; the swap
  leaves nothing. Layer 1 stays Layer 1: every mess item mishandled leaves the call (checks.py R2, six variants). The
  decisive step stays analytical: the Kish route executes every filed sentence correctly and files Lakeshore (R3a), the
  decisive step alone moves it to the Central Valley (R3b), no field, code or definition settles it, and nothing is
  planted (the supplement has been in the design since 2023 for coverage, the report's own section 2 says why).
- **Gates on this cut (target.zip 2ec516f2, seed 312377):** generator checks 134 of 134; verify OK from the bundle alone;
  two builds byte-identical; figures_check 48 of 48; ceiling.py pair 28.5, mirror 0.0, every careful-path cracker 0 of 15;
  precut 61 checks, 0 FAIL; voice-check PASS; leak.py REVIEW (ruled above); guard.py surface 0 promoted pairs, personas
  the card's; guard.py heart WARN only (nearest drivers 0.07); guard.py check WARN only; container audit clean (target
  and golden); the realism sweep adds no region's completed interviews repeating between any two waves or between two
  regions in a wave, and no round all-region total.
- **Determinism judge:** round 1 (08eedf9f) NOT_DETERMINISTIC on the supplementary cells, repaired in one generator pass (Tried and rejected); round 2 (2ec516f2) DETERMINISTIC, FIX_NOW, fixed in the solution and the prompt's rounding sentence; round 3, the one FIX_NOW re-judge (2ec516f2), DETERMINISTIC, APPROVE: every committed figure reproduced blind, Gate G method_or_model_selection (analytical_non_defect, no surface read), Gate H domain pass, layers pass, decisive step analytical. Its one residual, the North's 2024 error with the pre-2024 regions as strata (3.94 against 3.98), is closed by report section 4 (the strata are the five health regions; only that convention reproduces Table 2's 4.56), asserted in checks.py (SF19, ask side).
- **House fixes:** H1 containers scrubbed, every document's created and modified stamps distinct and in order; H9 no
  describing file; H13 no constant-step identifier (Northmark case numbers step 1 or 2, Ostrander's 1 to 3, licences 3
  to 28); H16 every document dated after what it reports (the report 18 November 2025 on a wave closed 13 June; the
  concordance 14 March 2024 for 1 April); H21 the university renamed from a name two letters off a real college, the
  pharmacy register stripped of place names; H24 provenance in metadata.json only; H23 the flip ask reads with any
  answer (the runner-up can always remove a larger share with enough interviews, its between-area variance being nil).

## Tried and rejected

- Seed OS13's co-located charging sites as one site: the call turns on reading the federal site definition (data semantics); its state energy office repeats task310's organisation family; set aside.
- The objective as drafted, the largest fall in the region's 2027 standard error (prototype of 2026-10-31, scratchpad proto.py, clean truth, 400 replicate draws a region): the absolute fall rewards the region whose present error is largest, so the North still tops the truth at 0.0023 against 0.0020 to 0.0021 for the low-clustering regions even with an intraclass correlation of 0.14, and the margins between the other regions are a few ten-thousandths, too thin for an estimator family; the Kish projection with the weighting effect divided out can turn a fall negative. Redrawn at the same time: stump_strategy uncertainty_hold (the decisive quantity is the precision a sample change buys) and shape 13 for 01 and grain_or_unit, both banned once task309 and task139 v3 entered the window. Next: an objective whose truth separates cleanly (a relative fall, or the ministry's publication standard as the line), measured before any data is cut.
- The prototype ladder of 2026-10-31 (a weight spread from a dual-frame top-up with the boost's effect on the weights not modelled, Kish rungs falling on Lakeshore only through the noise of the realised design effect: R2 picked the Central Valley in 9 to 19 of 30 realised samples at every setting tried): a rung that holds by the luck of one sample is seed-hostage and its Kish member sits inside the licensed family (Gate C against Gate F). Replaced on 2026-11-01 by a structural rung: the supplement's small fixed take, which an equal boost multiplies, so the Kish projection that holds the weighting effect is wrong by construction in every realised sample (40 of 40) and the components projection right in every one.
- Free takes driven by response (2026-11-01, seed search on 600 worlds): the estimator family (ANOVA, REML, weighted ANOVA, design-based, by stratum, Kish recomputed) spread the Central Valley's share over 38 to 42 per cent and the clustered regions' over a point or more, a fork on every whole-per-cent figure; replaced by the centre's fixed take of completed interviews per area, which collapses the family for the clustered regions and leaves the Central Valley's and Lakeshore's shares pure design quantities wherever their between-area variance estimates are nil.
- Shipping the first built sample (seed 91771): two shares sat 0.03 to 0.07 points from a whole-per-cent edge and the decisive edge only matched the Kish route's carried advantage (1.0x against 1.2x); Lakeshore's take raised to 12 and the seed redrawn on the full assertion set (100816).
- The 2024 ask's device on the first reorganisation draft (nine areas moved region): the misread numbers moved every completed-interview count but left the Metro, Lakeshore and Central Valley estimates within a tenth of a point in a third of worlds (30 worlds measured); redrawn with seventeen areas moving between every pair of neighbouring regions.
- Judge round 1 (2026-11-01, target.zip 08eedf9f): NOT_DETERMINISTIC on the supplementary cells, the call and the stump standing (Gate G and Gate H pass): the published 2025 error as the error without the boost (the terms' "both as the Centre would publish them" read literally), a binomial within-area variance, the between part left unfloored and "match" read on whole per cents each moved a share or the runner-up's boost, and the 2024 numbering cut was bracketed only between 8 and 22 April. Kept the call, the stump and the ask device; repaired in one generator pass: the report's Table 2 publishes each region's intraclass correlation for planning (a negative estimate shown as zero), the terms file both errors reckoned the same way for the 2027 design, the prompt asks for a strictly larger share, an old-only area's 2024 batch goes out on Friday 19 April so the cut sits between two batch days, and the sample was reseeded.
- A seed search requiring all five projections (published correlation, analysis of variance, Kish recomputed, the published-error baseline and the unfloored design-based remainder) to agree to the whole per cent in every region: no hit in about 2,000 worlds, the published baseline matching the model error only by coincidence; the two readings a filed sentence now rules out need only keep the call.
- Seed 100816 after the repair: fails the published-baseline criterion. Seed 302004: passes every gate, but the North's 2024 completed interviews (701) repeat its 2025 count in Table 1, a realism tell beside the 2024 ask. Seed 312292: the North's intraclass correlation 0.454 and design effect 16.6, extreme for the indicator. Seed 310387: the 2025 Table 1 total a round 8,100 with the North at exactly 700.
- Judge round 2 (2026-11-01, target.zip 2ec516f2): DETERMINISTIC, FIX_NOW, Gate H analytical; two supplementary cells soft on the golden's own wording: the runner-up's boost compared as whole per cents gives 28 per area once the takes are counted as completed interviews (Lakeshore 44.39 at 27 against the Central Valley's 43.91, both 44), and the Central Valley's weighting effect sits on its second decimal's edge (3.375 over usable answers, 3.366 over completed interviews). Kept the call, the shares, the runner-up's boost and the 2024 figures; filed the rounding path in the prompt's rounding sentence (shares compared unrounded, the runner-up's boost per area), led the golden's answer with 27 per area, and stated the weighting effect to one decimal (3.4 to 1.6, the same under both counts).
