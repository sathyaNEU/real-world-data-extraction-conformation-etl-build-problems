# task202 design note

**Status: architecture v1 built, stage 3 complete on the free gates, one gate red (the ask layer's
pair ceiling, measured at 65.5 against the bar of 40).** Four grounds were screened to
death before it (human-factors thinned-count and time-on-task, multiple-testing selective inference, the
designation-set device on task181's safety-incident ground, and environmental-monitoring exceedance on four
mechanisms and five candidates); all of those kills, with their measurements, are in `## Tried and
rejected`, and none of them binds this architecture. Architecture v1 is the first live one in this slot,
so the card's `lineage` is empty. The card draft is
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/wave5/task202b/task202_card.json`
and `guard.py check` returns WARN with no BLOCK.

## Draw

1. **Cell.** `nonprofit-grant-making` (card `domain`) inside `general-statistics-data-science` (card
   `client_domain`), subdomain `grant-award-portfolios`, objective `anomaly-detection`, prompt shape 14
   (cuts of a distribution). The domain's only other anomaly-detection build is task103 of 2026-10-03, on a
   fan-out driver; this architecture adds no units and re-partitions nothing (card `differentiation`).
2. **Niche.** A corporate-endowed relief foundation reimburses accredited community partners for one-off
   household relief awards. Partners have always claimed in aggregate: the monthly claim return states, per
   partner per household-size band, a total amount and an award count, and nothing else. Since January 2025
   the partners in two pilot provinces have claimed award by award on the foundation's partner claim portal.
3. **Call and shape.** One figure: the 2027/28 referral ceiling at the reference household size (four
   persons), in pesos to the nearest PHP 100 (`dial_setting`, answer unit currency). Shape 14 supplies the
   criteria: two committed shares across six household-size bands, each band's ceiling, each band's referred
   share and referred value share, the equivalence-scale factor at each band, and the exhibit.
4. **Why anomaly detection and not descriptive distribution.** The object is a detector: an award above its
   band's ceiling is referred to the relief desk before payment, so the ceiling schedule is the scheme's
   anomaly trigger and its setting is a monitoring decision. The committed share is a staffing constraint on
   that desk, which is why the boundary is solved backwards from it rather than read off the distribution.
5. **Mechanism.** Strategy `grain_or_unit`, gap `population` (Gap 2, the file is not the thing: the claim
   return's rows are partner-band-months and the decision's population is awards), generators G17 then G2,
   Gate G `method_or_model_selection`, calibration `pilot_log` (the portal), context artifact
   `filed_standard` (the scheme's operating policy), `layer2_family` `estimation_fit`, `layer2_pattern`
   `own:award-distribution-rebuilt-from-partner-averages-and-a-measured-within-partner-shape`.
6. **The data-native sentence.** This pack produces the pitfall because two files hold two different halves
   of one distribution and neither holds both: the claim returns are the only record of **where each
   partner's awards sit** (every partner's own average), and the portal is the only record of **how a
   partner's awards spread about that average**, so a cut of the award distribution exists in neither file
   and has to be built from both.
7. **The client's two rigor patterns for the task type were screened and both are dead as stated.**
   `general-statistics-data-science/exploratory-data-analysis-distribution-assessment/1` ("judge outliers on
   the symmetric scale") pins the anomaly rule or the distributional assumption, and a stated anomaly rule
   is rule application under the estimand pincer; `/2` ("stratify before reading a correlation") pins the
   within-group comparison or the unit-defining grouping, which is the estimand's unit. `layer2_pattern` is
   therefore `own:`, and the swap test is answered on the domain's nouns in `## Three rules`.
8. **The `guard.py check` WARNs, answered.** `three_rules.strategy_risk` on `grain_or_unit`: the grain
   mismatch is the **gap** this build exploits, not its decisive step, and the `Analyst test` line shows the
   easy route failing after every field is read and every filed rule applied. `repeat.gate_g` against
   task172: `method_or_model_selection` is the honest label, because seven routes to the same filed
   quantity stand and the portal's own goodness of fit is what closes the family; no other Gate G key
   describes a method closed by the data. **Registering this card moved the window and added two more
   WARNs, which is the behaviour `fingerprint` Part 2b predicts:** `repeat.gate_g` now also cites
   task190 (6) and `overuse.gate_g` fires at five of the last twelve. Both are answered the same way, and
   neither is clearable by redrawing honestly: the remaining Gate G keys describe a forecast, a stated
   limit, an attribution, a hold, or a correct number resisted, and this call is none of those. The
   mechanism inside the key is not the recycled part, which is what the heart check measures.
9. **`guard.py heart task202`, run after registration: `HEART VERDICT: WARN`, exit 0, not BLOCK.** On
   driver and stump text against every card, every lineage driver, every stump and every shipped-ledger
   row, the nearest is **0.09** (task255's truncated-and-censored size distribution, differentiated in the
   card) and the nearest stump text is **0.04** (task103 v3, this domain's incumbent), so the heart of
   this stump sits far from the build that shares its domain and objective.

## Default path

What a competent analyst builds without thinking, with every field read correctly and every filed rule
applied. Figures are the locked model's ten-seed means (`final_check.py`, `lock.py`); the shipped numbers
are fixed by the generator at the cut.

1. Parse the monthly claim returns for the twelve months to 31 March 2027, including the two months whose
   revised return supersedes a preliminary one, and fix the partner crosswalk between the claims ledger and
   the portal.
2. Read the operating policy's equivalence scale (six factors, three decimals) and its rounding rule
   (each band's ceiling rounded up to the nearest PHP 100).
3. Build each partner-band's own average award from the return's total and award count. This is the only
   award-level figure the claim returns state, and it is correct.
4. Cut the distribution of those partner-band averages, weighted by award count, at the committed share.
5. Solve the reference-size ceiling backwards through the equivalence scale and the rounding rule.
6. File the schedule and report each band's referred share.

**Ends on:** PHP 5,800 at the reference band, a schedule that would refer 9.82 per cent of the window's
awards against the 6.0 per cent the board committed to.

**Golden:** PHP 7,800 at the reference band, 20.0 printed units above the default path, referring 5.94 per
cent of the window's awards. The design read PHP 7,830 before the pack was cut, which was the mean of ten
draws of the world rather than a ceiling any world prints: clause 9 makes every ceiling a multiple of
PHP 100, so 7,830 is unattainable and the cut pack prints the attainable figure nearest it. Clause 9's own
margin at that figure is measured, not assumed: the schedule refers 5.9429 per cent against the 6.0000 per
cent cap, which is 0.57 of the step the last PHP 100 of ceiling buys, and PHP 7,700 refers 6.0432 per cent,
0.43 of the step above it.

## Stump sentence

A competent solver parses every claim return, supersedes the revised months, fixes the partner crosswalk,
reads the equivalence scale and the rounding rule, builds each partner-band's own correct average award
from the stated total and count, cuts that distribution at the committed share and files PHP 5,800, because
the distribution of partner averages carries the spread **between** partners and none of the spread
**within** them; the portal is the only record of that within-partner spread, and no route that pools it,
rescales it by one ratio or reweights it to the portfolio's band mix reproduces the averages the claim
returns state for the other sixty-six partners.

## Three rules

**Task type:** `general-statistics-data-science/exploratory-data-analysis-distribution-assessment`, which
the taxonomy gives as serving DD and AD; the build sits on its distribution-assessment side, cutting one
award-amount distribution at committed shares.

**Domain test:** the deciding quantity is the shape of the scheme's award-amount distribution, which is the
task type's own statistical object and which a relief funder genuinely estimates and acts on, because a
referral ceiling is a desk it has to staff; the field's own analysis is to rebuild the award-level
distribution from each partner's own stated average and a scale-free within-partner award shape measured on
the partners that claim award by award.

**Swap:** the General Statistics swap is of the method, and it breaks: replace the distribution's shape with
a generic summary, the partner average, and the reference ceiling moves from PHP 7,800 to PHP 5,800, 20.0
printed units, and the referral rate from 5.94 per cent to 9.82; on the domain's own nouns the swap fails too,
because the award shape is bimodal for a reason only a relief scheme produces, a standard living-cost award
with a one-off capital item on about nine awards in a hundred at about four times the standard, and because
the ceiling is nested across household sizes by the scheme's own equivalence scale.

**Layer 1:** the claim workbooks' band columns were renamed and a header block added from July 2026 (a
system change the foundation made); the equivalence scale is filed as a rule and the rounding as a separate
clause of the policy PDF, with no factor tabulated anywhere (how the policy was drafted); partner identifiers differ between the claims ledger and the portal
and join on an imperfect crosswalk (two systems procured years apart); the scheme's fiscal year runs July to
June while the policy names the twelve months to 31 March (the policy was drafted to the claim cycle);
amounts are in pesos in the returns and thousands of pesos in the published summary; a preliminary and a
revised return overlap for two months; small cells are suppressed in the published summary; one partner was
accredited mid-window and one exited. Nothing is placed to be caught and none of it carries the call.

**Layer 2:** family `estimation_fit`. The methodological choice that flips the call is which distribution
the committed share is cut on: the distribution of partner averages, or the award-level distribution those
averages and a measured within-partner shape imply.

**Decisive step:** rebuild the award-amount distribution as each partner-band's own stated average times the
scale-free within-partner award shape the portal measures, and cut that; in the field's words, the ceiling
has to be struck on awards, not on partner averages.

**Not semantics:** every field is read correctly on the default path. The claim return's total and award
count mean exactly what they say, their quotient is the partner-band's true average award, the equivalence
scale and the rounding rule are read off the policy correctly, and the crosswalk and the superseding
revision are resolved correctly. The easy route is still wrong by 20.3 printed units, because what is
missing is not a reading but a distribution the record never states.

**Not rule application:** the operating policy files the estimand (population, outcome, window, unit,
comparison, the scale and the rounding) and no shipped sentence says how to recover the award-level
distribution from aggregate returns; executing every filed rule correctly produces the default path's PHP
5,800. The seven routes measured all execute the same filed rules and print seven different ceilings.

**Analyst test:** a strong analyst who has read the operating policy, applied the equivalence scale and the
rounding rule, superseded the revised returns and fixed the partner crosswalk still cuts the distribution of
partner average awards, because that is the only award figure the claim returns state, and files PHP 5,800.

**Estimand:** filed in the scheme's operating policy, clause 9: the referral ceiling at the reference
household size is the lowest amount, a multiple of PHP 100, such that when each band's ceiling is generated
from it by the scale in schedule B and rounded up to the nearest PHP 100, the share of the scheme's awards
that would be referred is at or below 6.0 per cent, where the scheme's awards are those of all accredited
partners at the award volumes and award levels of the twelve months to 31 March 2027, an award is one
household's relief application resolved with a payment, and the award shape is measured on portal claims
over those same twelve months.

**No decoy:** nothing is planted to be caught. There is no copied block, no hidden rule, no memo, draft or
briefing arguing a figure, and no stakeholder number the task overturns. The pilot's two provinces sit low
on award level and carry the pilot's own household-size mix because a pilot in two provinces does, and that
fact kills only the pooling rungs, never the golden.

**No certified replay:** the method is not hidden and is not recovered by reproducing any certified or
published figure. The published partner summary reconciles to the claim returns under every route measured,
so it separates none of them; what closes the family is the portal's own goodness of fit and the
requirement that a route reproduce the average each claim return states.

**Lesson:** a committed share has to be cut on the distribution of the things being counted, and an
aggregate's average carries only the spread between reporting units; where two files hold the two halves of
one distribution, a model that uses either alone files a confidently wrong boundary. No build on file
teaches it: task187 corrects a curved response at a unit's own level, task246 separates variance components
from replicates, and task103 re-partitions contacts across units.

## Readability screen

Six tests per rung: T1 published at a glance (a shipped figure states it), T2 one group-by (a single
aggregation reaches it), T3 a sorted column (ordering one column reveals it), T4 a stakeholder sentence
(someone in the pack says it), T5 a file or field name (naming gives it away), T6 a round-number tell (the
construction leaves a suspiciously round artefact).

| Rung | T1 | T2 | T3 | T4 | T5 | T6 | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 1, cut the partner-average distribution (the default path) | no | yes | yes | no | no | no | readable |
| Rung 2, pool the portal's awards as they stand | no | yes | no | no | yes | no | readable |
| Rung 3, rescale the pooled portal by one portfolio ratio | no | no | no | no | no | no | readable |
| Rung 4, rescale per band and reweight to the portfolio's band counts | no | no | no | no | no | no | readable |
| Rung 5, rebuild per partner-band but smooth the shape into one fitted family | no | no | no | no | no | no | readable |
| Rung 6 (decisive), rebuild per partner-band with the shape as the portal measures it | no | no | no | no | no | no | silent |

The decisive rung is silent on all six: no shipped sentence states that the award shape must be used as
measured rather than smoothed, no single group-by produces it, the portal's bimodality shows only once the
awards are expressed as multiples of their own partner-band average, and no file or field name points at it.

## Ladder

Seven routes to the one filed quantity, each executing every filed rule, measured on the locked model over
ten seeds (`lock.py`). Printed unit PHP 100. "Ties" counts seeds on which the route prints the golden's
value.

Measured on the shipped pack (`generator/checks.py`, asserted rung by rung), with the same route measured
over the 84 draws of this world the scan covered beside it, each rescaled so clause 9's ceiling lands on
PHP 7,800, so the separation can be read as the mechanism's and not the draw's.

| Rung | Route | Ceiling | Against golden | Over 84 draws (mean, median) |
|---|---|---|---|---|
| 1 | partner-band averages, award-count weighted (default path) | PHP 5,800 | -20.0 pu | -18.9, -20 pu |
| 2 | the portal's awards pooled as they stand | PHP 6,600 | -12.0 pu | -14.2, -12 pu |
| 3 | the pooled portal rescaled by one portfolio-to-portal ratio | PHP 9,600 | +18.0 pu | +13.6, +14 pu |
| 4 | the portal rescaled per band and reweighted to the portfolio's band counts | PHP 8,800 | +10.0 pu | +5.2, +6 pu |
| 5a | rebuilt per partner-band, one lognormal at the portal's CV | PHP 8,400 | +6.0 pu | +5.0, +5 pu |
| 5b | rebuilt per partner-band, one gamma at the portal's CV | PHP 8,700 | +9.0 pu | +8.1, +8 pu |
| 6 | **rebuilt per partner-band with the measured shape (golden)** | **PHP 7,800** | 0 | 0 |
| - | rebuilt per partner-band, a correctly specified two-component mixture fitted by EM | PHP 7,800 | 0 | +0 pu on 80 of 84 |

**How much of the shipped separation is the mechanism and how much is the draw, stated as a number.** The
three large rungs are the mechanism and hold on essentially every draw: dropping the within-partner spread
costs about 19 printed units, pooling the portal as it stands about 14, and rescaling that pool by one
ratio about 14 the other way. The *thinnest* rung is the draw's: across the 84 draws the smallest
separation in a draw has a median of 2.0 printed units and sits under 3 in 47 of them, and the routes that
come closest are the two nearest neighbours of the decisive step (rung 4 and rung 5a, which both rebuild
something per cell). The shipped draw was selected where that thinnest rung is widest, at 6.0 printed
units, PHP 600, which is what `checks.py` asserts on the pack the judge will see; the selection is recorded
here rather than presented as the mechanism's typical behaviour.

The last row is not a rung and is the strongest determinism evidence in the build: the award shape is a
two-component lognormal mixture, so a correctly specified fit recovers it (fitted weight 0.9102 against a
true 0.9100) and prints the same ceiling. How the shape is represented is therefore a C3 corridor rather
than a fork, while every route that substitutes a single smooth family (5a, 5b) or that skips the rebuild
altogether (1 to 4) is 6 to 20 printed units away. The minimum separation across the six wrong routes on
the shipped pack is 6.0 printed units, PHP 600.

The arithmetic. The measured shape's coefficient of variation is 0.72. Rung 1 drops it entirely, which is
why it is the largest error and why its schedule refers 9.82 per cent of awards instead of 6.0. Rungs 2 to 4
use the portal's awards, which carry the shape but also the pilot's own level range and household-size mix:
the pilot is two provinces of eight, so its partners are alike in level (within-province level spread 0.12
against 0.42 between provinces) and its mix is 27/24/19/14/9/7 per cent against the portfolio's
16/17/18/19/16/14. Rungs 5a to 5c keep each partner's own average and replace the measured shape with a
fitted one, which is what the portal refuses.

**Two independent dials, which is why this is not the single-dial death that killed S1.** Rung 1's
separation is set by the within-award spread; rungs 2 to 4 by the gap between the portfolio's and the
pilot's between-partner level spread; rungs 5a to 5c by the capital-item mode. The first two trade against
each other on one parameter, and the third moves independently, so the sweep found a setting where all
three hold (`tune.py`, `tune2.py`, `lock.py`): minimum separation across the seven wrong routes 1.8
printed units.

## Semantic fork table

| ID | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | "the scheme's awards" | all accredited partners' awards, or only the portal partners' | clause 9 names all accredited partners; `same call` is false, so the sentence closes it (C1 by filing) |
| SF2 | the window | the fiscal year July to June, or the twelve months to 31 March 2027 | clause 9 files the twelve months to 31 March 2027; the generator keeps every award clear of both boundaries (C1) |
| SF3 | which awards measure the award shape | the portal's 27 months, or the portal's awards inside the window | the records decide it, not a clause: the two capital-item components became eligible only on 1 July 2025 (schedule D and the policy's amendment history), so the portal's earlier claims are a different award mix and the component codes show it. Measured: the 27-month reading prints PHP 7,200, 6.0 printed units low (C4, the alternative violates a shipped fact) |
| SF4 | the shape pooled or per band | one shape across bands, or each band's own | `same call`, measured on the cut pack: the per-band reading and the per-partner-level-tercile reading both print PHP 7,800, asserted in `checks.py`. The 7.0 printed units the design reported was the spread of nine separate subset ceilings, which is not the alternative reading; the per-band reading uses all 11,788 claims partitioned, so its errors cancel. Each band's own 94th percentile of the shape sits within 12 per cent of the pooled one, asserted band by band |
| SF5 | "rounded to the nearest PHP 100" | up, down or nearest | schedule B files "rounded up"; asserted in `checks.py` |
| SF6 | "at or below 6.0 per cent" | the lowest qualifying ceiling, or the closest to 6.0 | clause 9 files the lowest; the share falls monotonically in the ceiling, so the lowest is unique (C1) |
| SF7 | share of awards or of value | the count share, or the value share | clause 9 files "the share of the scheme's awards"; the value share is a separate graded ask |
| SF8 | band 6 | exactly six, or six or more | schedule B files "six or more"; no award sits at a seven-person band boundary |
| SF9 | the normalisation of the measured shape | each award over its own partner-band average, normalised or not | identical by construction: each cell's ratios average exactly one, so the pooled mean is exactly one and the normalisation is a no-op; asserted |
| SF10 | the superseded months | preliminary, revised, or both | the return's own status field and the policy's filing rule; both-counted is refused by the award-count reconciliation |
| SF11 | the partner accredited mid-window and the one that exited | in or out of the window's volumes | clause 9's "at the award volumes of the twelve months" counts each partner's own awards in the window; neither partner's awards straddle the boundary |
| SF12 | amounts in the published summary | pesos or thousands of pesos | the summary's own column header and a reconciliation to the returns, which only one reading satisfies |

## Closure table

| # | Axis | Reading and closure move |
|---|---|---|
| 1 | Population | all accredited partners' awards in the window, filed in clause 9; partners not yet accredited stated as out. C1 |
| 2 | Unit of account | one award, filed as one household's application resolved with a payment, not one household and not one claim line. C4 at a factor |
| 3 | Attribution window | the award's payment month; every award clear of both window edges by construction. C1 |
| 4 | As-of dating | the claim returns as they stood at the 30 April 2027 extract, filed; the revised return supersedes. C1 |
| 5 | Version basis | the revised return where one exists, the preliminary otherwise, by the return's status field. C1 |
| 6 | Denominator | the window's award count, in clause 9's own words. C1 |
| 7 | Weighting | each partner-band cell weighted by its own award count, which clause 9's "share of the scheme's awards" fixes. C1 |
| 8 | Window length | twelve months, filed; the shape is measured over the same twelve. C1 |
| 9 | Boundary inclusivity | "exceed" the ceiling is strict; the generator puts no award within PHP 20 of any band ceiling. C1 |
| 10 | Rounding path | each band's ceiling rounded up to PHP 100 once, after the scale is applied, filed in schedule B. Asserted |
| 11 | Tie-break | the lowest qualifying multiple of PHP 100; the share is strictly monotone in the ceiling over the solve range. C1 |
| 12 | Maturity and censoring | no censoring anywhere: every award in the window is resolved and paid, and nothing is truncated or capped. Stated |
| 13 | Order of operations | scale then round then compare, filed; comparing before rounding is refused by schedule B's wording. Filed order |
| 14 | Row order | the solve is a sum of per-cell tail shares, invariant to row order; asserted over six permutations |
| 15 | Duplicate resolution | the two overlapping months resolved by status; the award-count reconciliation refuses both-counted. C1 |
| 16 | Identity normalisation | partner identity across the claims ledger and the portal, by the shipped crosswalk; every portal partner resolves to exactly one ledger partner. C4 |
| 17 | Netting against gross | awards are gross; one partner's recovered award is shown as a separate negative claim line and is out of scope by clause 9. Filed scope |
| 18 | Dimensional units | pesos throughout the returns, thousands in the published summary only; the summary is not in the solve path. C4 |
| 19 | Code and status semantics | the return's status codes and the award's component codes; dictionary semantics, never the stump |
| 20 | Integerisation | ceilings are whole multiples of PHP 100 by construction; award counts are whole. C1 |
| 21 | Clause scope | clause 9 governs the scheme, schedule B the scale and rounding; the scope of each is filed in its own heading. Filed scope |
| 22 | Forward window contents | the 2027/28 window is not observed; clause 9 fixes its contents as the window's own volumes and levels, which the returns state. Filed |

## Literal reader

A judge executing the shipped text word for word reads clause 9, takes the claim returns for the twelve
months to 31 March 2027 with the revised months superseding, computes each partner-band's average award as
total over count, expresses each portal award in the same window as a multiple of its own partner-band
average to get the award shape, then for each candidate multiple of PHP 100 generates the six band ceilings
by schedule B's scale rounded up, computes for each partner-band cell the share of the shape above that
cell's ceiling over its average, weights by the cell's award count, and takes the lowest candidate whose
total is at or below 6.0 per cent. That execution is the golden. Nothing in clause 9 names a method, and
the sentence it files is a quantity, not a procedure: the population, outcome, window, unit and comparison
are fixed and how the award distribution is recovered is left to the analysis.

## Oracles

- `generator/checks.py`: the analyst test executed on the clean truth (rung 1 files PHP 5,800), then the
  decisive step alone changed and the golden asserted (PHP 7,800); every SF row asserted;
  the edge distance of every graded figure from its printed cell boundary; row-order invariance over six
  permutations; the award-count and value reconciliation between the returns, the portal and the summary.
- `verify.py`: reads only the shipped bundle and recomputes the ceiling schedule, each band's referred
  share and referred value share, and the referred award count.
- `generator/figures.json` plus `figures_check.py`: every graded figure with its printed unit and its
  mid-bin clearance.
- **Implementation invariance of the solve itself**, measured rather than argued: the committed share falls
  monotonically in the ceiling, and two independent implementations of the backward solve (an exhaustive
  grid over every multiple of PHP 100, and a binary search) return the **same ceiling on all ten seeds at
  each of three committed shares, 6, 10 and 15 per cent**, on the second model cut. The solve is therefore
  not itself a fork, and the ladder's spread is the shape's, not the search's.
- The portal's goodness of fit, which is the pack's own closure evidence: KS against a single lognormal
  16.1 times the five per cent critical value, against a gamma 19.1 times, against an EM two-component fit
  0.33 times, which accepts it and is why the correctly specified fit is a corridor and not a rung; and the
  within-partner spread scaling with the partner's level at a correlation of 0.969 over the 22 portal
  partners, which refuses an additive shape.

## Ask sheet

The prompt asks for four families of six figures and two deliverables: twenty-four graded figures, every
one separately gradable and determinate, each with its unit and rounding inside the asking sentence. Band
4's ceiling is the main call.

| Ask | Figures | Device against the careful solver's path |
|---|---|---|
| A1 each band's 2027/28 referral ceiling, pesos to the nearest PHP 100 | 6 | the scale is filed as a rule inside the policy PDF and the rounding rule is a separate clause of it, applied once and after the factor |
| A2 each band's referred share of its own window awards, one decimal | 6 | the band mix differs between the pilot and the portfolio, so a portal-only read misses every band; counting a superseded return as well as its revision moves band 4 from 6.1 to 6.0, measured |
| A3 each band's referred share of its own window award value, one decimal | 6 | value share against count share: the capital-item components carry 22 per cent of value against 6 per cent of count |
| A4 the equivalence-scale factor applied at each band, three decimals | 6 | schedule B tabulates no factor at all: every band's factor has to be computed from B.2's rule, and the band's size is its lower bound, which is what fixes the open band |
| D1, D2 the two deliverables | 2 content criteria | the schedule workbook and the board paper, which must carry the distribution against the ceilings |

**Dropped, and why each is out.** The designating ask (which partners' own referred share would exceed 12
per cent) was dropped at the design stage because the golden's own estimator family returned 2 distinct
designated sets over 12 bootstrap redraws. Two further asks were dropped at the build: the number of
window awards referred, and the award shape's coefficient of variation. The prompt asks for neither, and a
graded figure the prompt never asked for is an open fork by construction, since nothing fixes its basis,
population or rounding (`determinism-check` section 5). Both are still computed and asserted; they sit in
the goldens' basis sheet as working, not as answers the rubric owes.

**Pair ceiling:** 65.5 (measured on the cut pack, over the bar of 40, and the one red gate in this build).

**Mirror leakage:** 34.6 per cent of ask weight (measured, under the 35 bar).

**Measured by:** `generator/cracker.py`, run on the cut pack. It scores both responses from different
readings on Part 0's weights (38 recommendation and components, 7 instruction-following, 55 asks, r = 5),
prints one row per response and sweeps the pair against the cracker's keep count.

**What the measurement says, and it is a finding about the ask layer rather than about any device.** Every
graded figure in the prompt is the call's own construction over the call's own population: the six ceilings
are generated from the call by schedule B, the six factors are read off schedule B, and the twelve shares
are that construction cut per band over exactly the rows clause 9's own comparison runs over. A response
that lands the call therefore keeps all twenty-four, so the cracker keeps 26 of 26 ask criteria and scores
100 against the mirror's 31.0. `supplemental-stumping` Part 1.2 ban 4 forbids an ask keyed to the call's
construction and Part 2.1's corollary gives the reason no device can repair it: an ask computed over the
call's own population can carry no primary, because the separation line puts zero device rows inside the
main call's declared population. The sweep in `cracker.py` prices it exactly: the pair reaches 40 only when
the cracker keeps 2 of 26 or fewer.

The ask layer therefore needs re-siting rather than hardening, onto quantities the call never reads (the
claims pipeline's own records, the accreditation and enrolment history, the reconciliation between the
returns and the Treasury's payment runs), and that changes `prompt.txt`, which is outside this pass. The
repair route is `/fix-rubric` with the main recommendation side frozen, and `freeze.py check --mode rubric`
proves the scope.

**The premise the number rests on, stated so it is not read as more than it is.** The pair ceiling assumes
one of the top two responses lands the call, which is the conservative premise and the one the gate reads.
Measured the other way, with both top responses stopping at a wrong rung, the pair is 31.0: every mirror
measured keeps only the six scale factors and the two content criteria. Which premise holds is a question
about the ladder, and the ladder's own evidence is the six wrong routes at 6 to 20 printed units and the
silent decisive rung; the stage 4 cold reader settles it, and until it does the gated field carries the
worse of the two numbers.

| Ask | The cracker's route | Cracker |
|---|---|---|
| A1 | lands the call and generates the band ceilings by schedule B | keeps 6 of 6 |
| A2 | lands the call and cuts the rebuilt distribution per band | keeps 6 of 6 |
| A3 | lands the call and takes the value above each band ceiling | keeps 6 of 6 |
| A4 | reads schedule B.2 and computes all six factors from the rule | keeps 6 of 6 |
| D1, D2 | produces both named files with the schedule and the chart | keeps 2 of 2 |

## Tried and rejected

### The designation-set device on task181's ground: six candidate drivers, all six already on file (2026-10-18)

The device carried over intact from task194's architecture 6, where it passed the sixth screen twice,
uniqueness on five estimator variants (one set, printed rates 28.4 / 28.6 / 28.7) and all three Gate B
tests. The assignment was to put it on human-factors-ergonomics / safety-incident-error-analysis, screening
against task181 first because task181 holds that domain, that subdomain, that objective and that decision
type. The screen was run as code (`guard.py nearest` on each candidate driver) and then as the abstraction
test on latent structure, default path and correction.

| Candidate driver for the designation set | guard nearest | Killed by |
|---|---|---|
| C1 the rate's real exposure is an opportunity count the pack never publishes, and a forward change multiplies it | **0.11** vs task181 v4 | abstraction: it IS task181 v4, in other nouns |
| C2 the tolerance is crossed by the busiest short window, set by within-period clustering | 0.06 | the dichotomy: a peak is a records-fixed statistic, so computing it is rule application and projecting it returns to C1; and clustered arrivals on an event log is task181 v3's data structure |
| C3 the chance two checks on one item both miss is not the product of their own miss rates | 0.07 | readability test 6: the joint rate is escaped over committed, one group-by; the unobserved version is the banned dark figure |
| C4 a unit's forward count follows its people's experience along a practice curve, not its own history | 0.08 | abstraction: task183 (the unit's events arise in its parts and the parts' own histories beat the unit's rate); and tenure is a visible attribute, which is this number's own earlier death |
| C5 the count is short by a classification lag the record measures about itself | **0.36** vs task181 v2 | a `driver.text` BLOCK, and task181 v2's recorded fate is that no filed criterion choosing the delay history leaves the step silent |
| C6 each candidate's marginal contribution to a set functional, overlapping in the same windows | 0.06 | abstraction: task106 (a set drawing on a shared finite pool, so summing individual sizings overstates the set and admits the wrong members) |

**The guard passes two of the six clones.** C1 scores 0.11 against task181 and C6 scores 0.06 against
task106, both under the 0.12 WARN line, and both are the same driver under the abstraction test on all
three elements. This is the blind spot the skill names (two task500 re-roots passed at 0.05 and 0.08 and
still repeated earlier drivers), measured twice in one pass on this ground. The lexical score cannot see a
mechanism told in other nouns, and on this ground the nouns are very far apart (aircraft levels, hospital
handovers, alarm floods, check failures).

**What the device does and does not supply.** The designation set discretises a free weighting away, which
is real and still holds. It does not supply a driver. The driver still has to come from the data's own
structure, and on this cell every driver a tolerance-exceedance call can carry is on file: three of them
inside task181's own slot (v2 the classification lag, v3 the self-exciting burst, v4 the unpublished
exposure) and the rest in the wider anomaly-detection corpus (task183's parts with their own histories,
task106's overlap under a shared pool, task195's paired screens on shared units).

**I nearly filed a third over-general law tonight and the corpus refused it before I reported it.** The
claim forming was that a designation set against a filed tolerance must decide a forward rate, so the
ground's furniture of counts and hours closes it. Counted on both sides: there are 32 `designation_set`
builds on file, and only 4 are on anomaly-detection (task48, task180, task181, task193). **13 are
data-quality-monitoring and 8 are ETL**, and what they designate is mostly a property rather than a
forward rate: which estimates carry a reliability warning (task230, task240), which series carry a
misclassification flag (task236, task242), which rates get suppressed (task233), which items stay in an
index (task237, task239, task463), which units qualify (task451, task462, task470), which campaigns repeat
another (task84). So the device does not force a rate, and the wall is not the device.

**The structural fact about the cell itself, which is worth more than the six kills.** The assigned cell is
the one spent pairing in this domain. `human-factors-ergonomics` has two builds on file in total
(task181 on anomaly-detection, task256 on descriptive-distribution) and **six never-built pairings**:
forecasting, root-cause, experiment-causal, ETL, opportunity-sizing-decision and data-quality-monitoring.
It also has **four never-drawn subdomains**: usability-task-performance-studies,
workload-fatigue-shift-analysis, human-reliability-assessment and alarm-interface-evaluation. The
compatibility proof that recommended this cell (task181 ships a designation set here) and the clone risk
that killed all six candidates are therefore the same fact: the incumbent is a designation set on this
ground, and it took the natural driver.

**Not run, and why.** The published-adjustment sweep, the sixth screen and the four unspent screens all
take a candidate, and no candidate survived the first one. Screening a driver already on file would spend
the pass on a build that cannot be registered.

### The serial-dependence ground: both channels dead on sign and on a single dial (2026-10-18)

Moved off the human-factors ground entirely (none of the six designation-set kills binds this pass).
New ground: `physical-environmental-sciences` / `environmental-monitoring-exceedance`, the cell task189
holds with censoring at instrument-specific limits. The direction screened was the one an exceedance
call actually turns on in the field: how often a compliant site looks like this by chance, when the
monitored readings are not independent, so the effective number of observations behind a mean, a run or
a control limit is a fraction of the row count. Near neighbours, one line each: task189 spends what each
observation's VALUE is when it is known only as a bound; task186 spends WHICH VARIANCE COMPONENT a test's
reference distribution comes from when units swing in shared local cycles; task191 spends the fact that
SELECTION for being extreme changes the reference distribution, so the family's maximum is the bar.
Mine would have spent how many independent observations one series contains. It does not survive.

**Channel 1, variance inflation (the brief's candidate 1). Dead three ways, measured in
`screen_A_ess.py`.** (a) The pricing test `stumping` Part 3 names fires: of the 36 (rho, m) settings
where the row-count standard error is at least 1.5x too tight, the unit's own level spread is within a
factor of two of the correct standard error in 23, share 0.64, and at every setting that could carry a
ladder (rho 0.8 to 0.95, m 6 to 24, naive 2.0x to 4.1x too tight) the ratio runs 1.05 to 1.81, so the
decisive rung is readable off the series. The escape condition solves exactly: R in [0.5, 2] means
VIF >= m/4, so a naive factor f escapes only beyond m = 4f^2 periods, which is 36 assessment periods at
f = 3. The dial fails at both ends: at rho 0.3 the naive route is only 1.5x wrong, at rho 0.9 the level
spread is right. (b) The run-length form is published at a glance: a compliant pre-change record of 16
periods at rho 0.8 already contains a run of 4 above its own baseline with probability 0.68 (0.79 for a
run of 3), and shape 17's own deliverable prints that table. (c) The sign is wrong and structurally so.
A dependence correction leaves the point estimate identical (+0.006 against +0.006 compliant, +0.977
against +0.977 shifted) and only widens, so it moves a call one way, exceedance to clear: at m 12,
rho 0.8 the naive route calls exceedance in 0.32 of compliant series against the ESS route's 0.14. The
golden is therefore always the hold, and every conservative reflex lands it without the analysis.

**Channel 2, variance bias (the one variant whose sign is right). Dead on the single dial, measured in
`screen_B_percentile_bias.py`.** Under positive autocorrelation the sample spread understates the
process spread, so an upper percentile computed on the record's own spread understates the site's true
percentile and the site looks compliant when it is not: at quarterly sampling and a correlation time of
2.5 years (rho 0.905), E[s]/sigma is 0.574 at n 12 and the percentile lands at 0.704 of the truth. But
the lever (the bias in s) and the noise the same graded percentile carries through the mean of the logs
are both functions of VIF/n alone, and the ratio never reaches 1 anywhere on the range: 0.19 at
VIF/n 0.05, 0.59 at 0.40, 0.89 at 0.70. Over 40 seeds at the most favourable setting the intended
separation (naive below the limit, honest above it) holds in 11/40 at n 12, 10/40 at n 20 and 7/40 at
n 32, and the golden itself runs 0.64 to 2.75 times the limit while the design's truth never moves.
That is task200's death on a different ground.

### Candidate 2, a long-term average over an averaging period the monitors do not produce (2026-10-18)

Dead on the WHAT screen, measured in `screen_CDE.py` section C. On one cut of 30 samples whose spacing
follows a wet-season programme, "the average over the period" reads 45.88 as the mean of samples, 38.61
as the mean of monthly means and 38.64 day-weighted, a spread of 7.27. Those three numbers are three
readings of the estimand's UNIT, which is one of the five parts a decisive step may not settle: name the
unit and the computation follows from the clause (rule application), leave it unnamed and it is a
semantic fork on the main recommendation. task200 measured the same three readings at 12.22, 12.22 and
9.20 and found no third position. It is also task189's shape on task189's own cell, a per-unit average
over measurements against a limit where naive averaging is wrong.

### Candidate 3, a forward exceedance probability from a declustered tail (2026-10-18)

Dead on the estimator family and on sign, measured in `screen_CDE.py` section D. On three years of
hourly readings at a 12-hour correlation time, 789 readings sit above the 97th percentile. The
declustered event rate runs 78.0, 58.7, 48.0, 42.3, 38.7, 34.3 and 29.7 a year across runs declustering
at 1, 3, 6, 12, 24, 48 and 72 hours, a factor of 2.6, and no filed criterion and nothing in the data
separates the run lengths: that is task194's chain-ladder death, several standard variants fitting the
record equally. The graded figure collapses besides, 0.000 expected exceedances of the limit under every
declustering choice against 2.636 undeclustered, so declustering only ever lowers the rate and the golden
is again the clear that every conservative reflex lands.

### Candidate 5, a consented load carried by the complete record (2026-10-18)

The three kills above all pointed the same way, so the fourth mechanism was drawn from what they leave:
a quantity whose estimator is forced by the data rather than by a variance. A works' consented monthly
load, concentration on a routine grab programme, flow and turbidity logged every 15 minutes, the mass
carried in wet-weather events the schedule never sees. The sign is right and the lever is large: across
40 simulated years the grab mean times the volume files 0.510 of the true load (sd 0.240) and on the cut
year 0.376, with 32 to 63 per cent of the load in the wettest 1 to 5 per cent of the record. It dies on
the same dial at both ends, measured in `screen_E2_ladder.py`, `screen_E3_ladder.py` and
`screen_E4_ladder.py`.

- With the calibration window narrow (campaign turbidity 3.8 to 30.2 NTU against a record reaching 272),
  the honest variants are extrapolating by a factor of nine and spread 910.5 kg in the decisive month,
  cross the consent in 2 of 18 months, and name the qualifying run's start month as 13 under one variant
  and None under three. Fitted on daily composites and applied to 15-minute values the "honest" route
  lands at 0.567 of the truth, BELOW the rung above it (turbidity calibration on the grabs, 0.748).
- With the campaign placed in the record's wettest six weeks so the calibration interpolates, the fork
  closes and the decisive rung becomes worthless: the turbidity calibration fitted on the ordinary grabs
  lands at 0.961, 0.968, 0.995 and 0.935 of the truth against the campaign-fitted route's 0.964, 0.944,
  0.988 and 0.917 over four seeds. A surrogate calibration does not care which subset of the record it is
  fitted on, because it is a physical relationship and not a schedule artefact. 0/5 seeds satisfied all
  four pass conditions (honest variants within 8 per cent, no month straddling the consent, one run-start
  month across variants, every other route naming something else).
- The corpus had it already, and `driver.near` could not see it: **task452 architecture v1** is this
  driver verbatim in other nouns ("a period total of the product of two series, one recorded at every
  interval and one sampled on a few intervals that mostly catch the quiet state"), in this same domain,
  shipped 2026-10-13 and re-rooted at the author's request with the recorded reason that "the decisive
  step (a concentration-discharge rating curve applied to every day of the gage record) is the field's
  standard load method, which careful solvers reach for", its two rejected hardening prototypes being "a
  dense automated sampler, a kinked relation", which is the campaign device above. It scores **0.07**,
  under the 0.12 WARN line, and fires no rule: `guard.py check` BLOCKed the card on `ban.artifact`,
  `ban.org_family` and `test.same_driver_older` and never mentioned the clone. That is the third measured
  instance of this blind spot inside this slot.

### The ground-level finding, which is worth more than a sixth candidate (2026-10-18)

Four structurally distinct Layer 2 mechanisms, five candidates, every one killed with a number, and they
fail in one pattern. On an exceedance call the decisive step is either records-fixed (it decides a
selection, a threshold crossing or which recorded quantity the comparison runs on) or it is an
estimator's output. The records-fixed branch on this cell is held: task189 took censoring at
instrument-specific limits and task245 took non-random gaps in a monitoring record ("a count of periods
above a level over a whole cycle, read from records whose gaps are not random: a recorder fails"), which
was the fifth idea in reserve and is spent by the incumbent. Every estimator-output branch fails on one
of three measured grounds: a dependence correction only widens, so the golden is a hold and conservative
reflexes land it; a correction that moves a point estimate is financed by the same VIF/n that randomises
the graded figure; and a correction forced by a fitted transfer is either extrapolating (the variants
fork) or interpolating (the rung below it lands the golden). The axis reservations do not survive the
window either: `org_family government_agency` and the cell's natural `monitoring_export` artifact both
BLOCK against task170, `gate_g signal_vs_noise_or_hold` is honest only for a hold, and the honest
`method_or_model_selection` on gap `rule` with pattern `none` fires `test.same_driver_older` against
task240. The live question for the next pass is the cell, not the device: this cell needs a records-fixed
decisive step and its two incumbents hold the two that the data supply.

### The pincer test written out, on the coordinator's instruction of 2026-10-18

The instruction arrived addressed to a `grid-reliability-outage-analysis` draw (a restoration-time
distribution, a major-event-day threshold, an index with a definable population, window and unit), which
is `energy-systems-utilities`, not this cell; task202's ground is
`physical-environmental-sciences` / `environmental-monitoring-exceedance` and no restoration time or
major-event rule appears anywhere in its brief or its screens. The pincer test itself is general, so it
is run here on all five candidates. It changes one verdict and hardens four.

| Candidate | The decisive quantity | Estimated, or one of the five parts | Pincer |
|---|---|---|---|
| C1a variance inflation | the number of independent observations behind a mean or a run | **estimated** (a standard error) | passes |
| C1b variance bias | the process spread behind a short record | **estimated** | passes |
| C2 long-term average | whether the average runs over time or over samples | the **unit** | **fails** |
| C3 declustered tail | the rate of independent exceedance events | the **unit**: the run length defines what counts as one event | **fails** |
| C5 load by fitted transfer | the mass discharged past the point in the month | **estimated**; the estimand files to the letter (determinand, point, month, kg) while the transfer stays open | passes |

**The one verdict that changes is C3's, and it hardens the kill.** I had filed C3 as dead on the
estimator family (the declustered rate running 78.0 to 29.7 events a year across runs declustering at
1 to 72 hours, a factor of 2.6) and on sign. The pincer says that fork is a *symptom*, not the disease:
the declustering run length is what fixes the unit of the count, no parameter-free reading fixes it, and
task192 architecture v1 is the recorded death on exactly that shape ("count the processes behind the
bursts, not the bursts", the unit of the count). So C3 is not revivable by filing a selection criterion
for the run length: filing it makes the step the execution of a filed clause, and leaving it unfiled
forks the main call, which is the pincer's own both-ends.

**The other direction is just as useful.** C1a, C1b and C5 all pass the pincer, so none of them died on
estimand filing and none is revivable by filing the estimand better. They died on arithmetic the pincer
does not reach: C1a on sign (a dependence correction only widens, so the golden is a hold that
conservative reflexes land) and on the level-spread reflex at 0.64 of live settings; C1b on the single
dial, lever/noise never reaching 1 anywhere on the VIF/n range and the intended separation holding in
11/40 seeds at best; C5 on the same dial at both ends plus task452 architecture v1, which is its driver
in other nouns in this same domain, re-rooted for the reason the screen independently measured.

**No client rigor pattern block on this ground either.** `layer2-rigor-patterns.md` carries 14 domain
sections and `physical-environmental-sciences` is not among them (nor are `energy-systems-utilities` or
`human-factors-ergonomics`), and `environmental-monitoring-exceedance` appears in no block, so
`layer2_pattern` here takes `own:<name>` as task189's card does
(`own:left-censored-results-with-several-reporting-limits`). The warning that travels with that freedom
is the swap test, and the swap was never this cell's problem: every candidate's deciding quantity broke
cleanly on a noun swap. What broke was the decisive step's arithmetic.

**The stop rule stands.** The correction revives nothing. The screen's conclusion is unchanged: this cell
needs a records-fixed decisive step and its two incumbents, task189 and task245, hold the two the data
supply.

### The nonprofit-grant-making ground: three mechanisms screened, one survives (2026-10-18)

New ground on the coordinator's assignment: `nonprofit-grant-making` as the card's domain inside
`general-statistics-data-science`, task type `exploratory-data-analysis-distribution-assessment`, objective
`anomaly-detection`, shape 14. Near neighbours, one line each on the insight each spends: task103 spends a
fan-out, one recorded contact serving several units through an effective-dated authorisation with a
one-allowance rule; task187 spends a record that is the average of a capped, curved response over a spread
of inputs; task246 spends a variance decomposition into measurer offset and field error from replicates;
task255 (the nearest driver at 0.11) spends a size distribution truncated below and censored above.

**Both of the client's rigor patterns for the task type are dead as stated, on the pincer.** Pattern 1
("judge outliers on the symmetric scale, robust or log-scale rules on skewed data") carries the pin "the
anomaly rule or distributional assumption is stated", and a stated anomaly rule is rule application;
leaving it unstated forks the call on the choice of scale, which is the pincer's both-ends. Pattern 2
("stratify before reading a correlation") carries the pin "the within-group comparison or unit-defining
grouping is named", and a named grouping is the estimand's unit. Neither is revivable by filing better, so
`layer2_pattern` takes `own:`.

**S1, band boundaries cut on a latent distribution reached by a noise correction. Dead on the single dial
and on the open family, measured in `screen_S1_latent_cuts.py`.** The mechanism: the committed coverage
share is cut on the distribution of each unit's true level, where the record gives each unit a noisy
estimate whose precision varies with a recorded item count. Three defensible deconvolution estimators
(method of moments on the logs, precision-weighted moments, and a Kiefer-Wolfowitz nonparametric MLE by EM)
spread **10.8 to 21.5 times the printed unit** across the whole noise range, against the 0.4 bar, so every
graded boundary forks. The lever over that noise never reaches 2.5 anywhere: 0.30 at a noise ratio of 0.3,
0.65 at 0.6, 1.29 at 0.9, 1.78 at 1.2, 2.11 at 1.5, and it rises with the same single parameter that opens
the family, which is task182's recorded death. The common-exposure subset screen fires besides: cutting the
distribution of the well-measured units alone beats the designed route at every setting from 0.6 up (7.65
against 9.83 printed units of error, 9.48 against 19.79, 11.58 against 32.50). And the coherence objection
is fatal on its own: a coverage commitment is operationally struck on the quantity the decision can see, so
the boundary covering a committed share of units by the recorded figure is the recorded distribution's own
percentile, which the records fix.

**S2, the aggregation mechanism, first parameter setting. The pool-and-rescale reflex landed the golden,
measured in `measure_all.py`.** With the portal partners drawn by a probability falling in their level, the
portal was a miniature of the portfolio: it carried both variance components, so pooling its awards and
rescaling by one portfolio-to-portal mean ratio reached the golden exactly (+0.0 printed units, the same
printed value on 3 of 12 seeds). Pool, stratify and reweight are all listed reflexes, so that setting spent
the stump. Re-rooted inside the mechanism rather than abandoned: the pilot is two provinces of eight, which
makes its partners alike in level (within-province level spread 0.12 against 0.42 between provinces) and
gives it its own household-size mix, and at the locked setting the same route lands +3.4 printed units away.

**S2, second failure: a correctly specified two-component fit forked the graded figure by 8.2 printed
units** on 5,368 portal awards (`measure_all.py`), because the cut is a tail functional of a shape and
shape estimators differ in the tail. Fixed by making the portal the 25,000-row spine, which puts about
11,900 of its awards inside the estimand's window, and by filing the window the shape is measured over
(SF3). At the locked setting every fitted family is refused by the portal's own goodness of fit (KS 12.5,
18.8 and 23.0 times the five per cent critical value) and each prints a different ceiling.

**S2, third failure: the capital-item mode and the province spread first looked like one dial.** At
p_cap 0.22 and 2.35x, the smooth-fit rungs collapsed onto the golden (a gamma at the portal's CV tied the
golden's printed value, -1.3 and +0.0 printed units); at p_cap 0.09 and 3.90x they separated to +7.2 and
+10.7 but the pooling rungs tightened. The sweep (`tune.py`, `tune2.py`) found the two are in fact
independent: the pooling rungs are set by the portfolio-to-pilot gap in between-partner level spread and
the smooth-fit rungs by the capital-item mode, so a setting exists where all three hold. Locked at p_cap
0.09, 3.90x, upper-mode log-sd 0.28, province spread 0.42 against 0.12 within, committed share 6.0 per
cent: minimum separation across the seven wrong routes 1.8 printed units, the golden stable on 10 of 10
seeds, the default path 20.3 printed units low and referring 9.6 per cent of awards against the committed
6.0.

**S3, a designating ask, dropped on the sixth screen's family count.** An ask naming the partners whose own
referred share would exceed 12 per cent was designed and measured before it was written into the sheet: the
golden's own estimator family returns **2 distinct designated sets over 12 bootstrap redraws of the portal,
with set sizes 11 and 12** (`final_check.py`), so the set is not determinate and neither is its count. The
ask sheet carries only cuts, shares and counts that follow from the forced construction.

**One measurement that is reported as a limit rather than a pass.** Measuring the award shape on a subset of
the portal (one household-size band, or one tercile of portal partner level) moves the ceiling by up to 7.0
printed units, which is larger than three of the seven rung separations. The design closes it at SF4 by the
pack's own band-homogeneity test, which does not reject, so pooling is the forced reading and subsetting is
rung 4's error; but the closure rests on a test rather than on the records, and it is the row the
determinism judge should be pointed at first.

### The build pass: six design figures falsified by measuring them on the pack (2026-10-18)

Every line here is a number computed on the generator's own truth or on the cut pack, and each replaced a
figure the design had argued. The scripts are `generator/tune.py` (the draw and award-level scan),
`generator/checks.py` (188 assertions), `generator/mess_check.py`, `generator/cracker.py` and
`generator/verify.py`.

**Rung 5c, the EM two-component mixture, is not a rung: it converges on the golden.** The design recorded
it at PHP 6,820, 10.1 printed units below the golden, and recorded the portal as refusing it at 23.0 times
the five per cent Kolmogorov-Smirnov critical value. Both figures were artefacts. Fitted on the pack the
mixture recovers the truth almost exactly (weight 0.9102 against a true 0.9100, log means -0.2564 and
+1.0765 against -0.2607 and +1.0899) and fits the portal at **0.33 times the critical value**, better than
the true parameters do at 1.98, because the award shape *is* a two-component lognormal mixture by
construction. The 10.1 printed units came from drawing only 150,000 values from the fitted mixture and
reading a 94th-percentile tail functional off that sample: the same fitted parameters give -1.0, -12.0 and
-10.0 printed units on three seeds with a 150,000 draw and **+0.0 on all three** with analytic quantiles.
The build is better for it. How the shape is represented is now a C3 corridor, not a fork, and the ladder
keeps the two misspecified families (a single lognormal at +6.0, a gamma at +9.0) which the portal really
does refuse at 16.1 and 19.1 times critical.

**"The golden stable over ten seeds" was a tie count against itself.** `lock.py` compared each route with
the golden and reported ties, so the golden's own row read 10 of 10 by construction. Measured per seed at
the locked parameters the golden runs **PHP 5,300 to PHP 10,400**, because it is a tail functional of a
realised portfolio of eight province levels and 88 partner levels, and more volume does not shrink it
(102,000 window awards gives the same spread as 51,000). Nothing in the build rested on that stability and
nothing needs it: the pack is one realised portfolio, and what has to hold across draws is the
*separation*, which does (the mean separations over eight draws sit beside the shipped pack's in the ladder
table). The claim is withdrawn rather than repaired.

**PHP 7,830 was not an attainable ceiling.** It is the mean of ten draws; clause 9 makes every ceiling a
multiple of PHP 100. The shipped pack prints PHP 7,800, and the award level was chosen inside the plateau
that prints it (the plateau runs from about PHP 3,300 to PHP 3,333 of standard award; the shipped 3,311.5
sits in it with the graded figures centred, below).

**Rung 2 at +1.8 and rung 4 at +3.4 printed units were implementation artefacts, and both widened to -12.0
and +10.0 without touching a mechanism parameter.** Two causes. The design's rung 2 and rung 3 were
measured with the *portfolio's* band weights, so the pilot's own household-size mix never cost them
anything, although the rung's own words are "pooled as they stand"; implemented literally, with the
portal's own mix, rung 2 moves to -18.0 per cent of the golden on the mean of eight draws. And which two of
the eight provinces ran the portal pilot is a free world fact: ranks 2 and 5 by award level leave the
pilot's level range wide enough that the pooling routes partly cancel, while two provinces adjacent in
level (ranks 2 and 4) make the portal's between-partner spread clearly narrower than the portfolio's, which
is the mechanism the design note already describes. Swept over nine rank pairs on eight draws each: the
worst per-seed separation across all six wrong routes runs 0.0 printed units at ranks 2 and 5 and 7.4 at
ranks 2 and 4. The pilot provinces are still two ordinary ones rather than the extremes.

**SF4's 7.0 printed units was a measurement of something that is not a reading of the clause.** It was the
spread of nine ceilings, each computed by applying one subset's shape to every cell. The alternative
reading SF4 names is one ceiling computed with each band's own shape applied to that band's cells, which
uses all 11,788 window claims partitioned rather than a sixth of them, so the subset errors cancel.
Measured on the cut pack both that reading and the per-partner-level-tercile reading print **PHP 7,800**,
and `checks.py` asserts it. SF4 is now `same call` and is no longer the row to point the judge at.

**Volume is a weak lever and was rejected.** Tripling every partner's award volume (161,000 awards to
484,000, and the portal spine from 26,000 rows to 79,000) moves the subset spread only from 5.6 to 4.25
printed units, because the dominant term is the realised portfolio and not the portal's sample size. The
pack keeps the 26,195-row portal spine.

**The policy ships as a text PDF, not as a scan.** The design's Layer 1 inventory called for the
equivalence scale in a table inside a scanned policy PDF. A scan has no text layer, so no verifier can read
the clause back, and `dataset-generation` requires every format read back through the verifier's own
extractor with a positive control on the same code path. The policy ships as the document system's own PDF
with schedule B as a table in it, which is the canonical Layer 1 item (a table inside a PDF) and which
`verify.py` reads back: it pulls the four tabulated factors out of the text layer, derives the two
untabulated ones from B.2's rule and recomputes all six band ceilings from them.

**The scheme change that closes SF3 is a world fact, not a clause.** Filing the shape's measurement window
in clause 9 was drafted and rejected: any wording that names the within-partner variation tells the solver
the thing the default path misses, and the readability screen's test 4 would fail the decisive rung. The
two capital-item components instead became eligible on 1 July 2025 by board resolution, recorded in
schedule D and the amendment history, so the portal's earlier claims carry a visibly different award mix
and the 27-month reading is refused by a shipped fact rather than by a clause. Measured: it prints
PHP 7,200, 6.0 printed units low.

**Where the draw was chosen from, and on what.** 84 draws of the world were scanned (`tune.py`), each
rescaled so clause 9's ceiling lands on PHP 7,800, and scored on four things measured rather than argued:
the worst separation across the six wrong routes, clause 9's own clearance below the cap and excess above
it one step down, and the tightest graded figure's distance from its printed cell edge. The shipped draw
holds 6.0 printed units of worst separation, 0.57 and 0.43 of the step, and 0.22 of a half-cell on the
tightest of the twelve share figures (band 4's referred share at 6.0612, which flips at a change of about
one referred award in that band). The award level was then centred inside the PHP 7,800 plateau on the same
criterion, which moved the tightest figure from 0.03 to 0.22 of its half-cell.

**Every Layer 1 item is neutral on the call, measured item by item on the cut pack**
(`generator/mess_check.py`): taking the preliminary returns only, counting a superseded return as well as
its revision, netting the recovery line, resolving the band labels through the reference table and
bypassing the identifier crosswalk by normalising the portal's own reference all print PHP 7,800 and leave
the overall referred share at 5.94 per cent. Counting a superseded return as well as its revision does move
band 4's referred share from 6.1 to 6.0, which is a breach of the policy's own superseding rule rather than
a mishandling of mess, and it is one of the ask layer's devices.

**The ask layer cannot hold the pair ceiling, and no device can repair it.** Measured at 65.5 against the
bar of 40. The reason is in the ask sheet above: the prompt's twenty-four graded figures are the call's own
construction over the call's own population, which `supplemental-stumping` Part 1.2 ban 4 forbids and Part
2.1's corollary proves undeviceable. Two asks were dropped on the way (the referred award count and the
shape's coefficient of variation) because the prompt asks for neither and a graded figure with no asking
sentence has no fixed basis. The repair is to re-site the ask layer onto quantities the call never reads,
which changes `prompt.txt` and belongs to `/fix-rubric`.
