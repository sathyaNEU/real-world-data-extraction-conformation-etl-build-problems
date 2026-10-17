# Determinism verdict, task190 architecture 3

Judged cold on the shipped bundle, 2026-10-17. This file replaces architecture 2's verdict, whose
substance is in the design note's post-mortem; it was judging a different world (Arahura Bank, cash
deposits below a reporting threshold) and would have read as current evidence if it shipped beside
this pack.

**Verdict: NOT_DETERMINISTIC. Disposition: SEND_BACK, overridden by the author to FIX_NOW.** The
override, its test and the condition attached to it are in the design note. In short: every fix this
verdict asks for files the WHAT, none files the estimator, and this verdict's own Gate F, G and H
findings say the decisive step is alive. If the re-judge after the fix pass is not APPROVE, the number
retires.

The judge's own text follows, unedited.

---

# verdict.md (working draft, part 1: BLIND CANDIDATE ENUMERATION, written before opening submission_graded_blocks.md)

Population: capital_payment_lines_2026.csv, delivery_sequence=1 only (26,652 lines; 222 bank-feed redeliveries dropped), 2 reversed + 2 credit_note
lines (net nil, untested). Tested set: testing_schedule_extract 2026 rows (272 rows, 271 distinct lines; CPL-26-095171 listed twice), all of
which match the ledger on amount and none missing from it. PDF schedule lists the same 271 refs. 10 lines show exceptions, all non-certain
(smallest amount 1.4k..5.4k each; found misstatement total 15,445.38; none in CP-11, CP-14, CP-31).
Structure of the tested set: every line >= 180,726 (31 lines, whole-euro amounts) is tested; below that the testing probability rises with
value (0.26% below 1k, 1.3% 1-5k, 3.1% 5-10k, ~35% 50-100k), i.e. selection probability ~ value / ~182k (monetary-unit style selection).
Largest untested line 85,087.70; 108,945.95 tested. Nothing in the shipped text states an interval, count or probability.

Candidates (authority total, programme figures to 50k):
C1  Known (found) only: 15,445 -> every programme rounds to 0 (authority 0). Not an estimate of the population.
C2  Value-weighted ratio: sum(err)/sum(value) over tested non-certain lines x non-certain population value, + certain-stratum errors (0):
    pooled 129,202; programme-by-programme sum 152,457 (CP-21 7,650; CP-23 52,905; CP-34 10,618; CP-41 47,252; CP-44 25,563; CP-47 8,470)
    -> rounds 0/0/0/0/0/50k/0/50k/0 style; authority ~100k-150k. (Biased: sample is size-biased, so value-weighting double counts big lines.)
C3  Inclusion-probability weighting (I x sum of taints, taint = error/recorded), I = interval, pi = value/I, certain stratum at full value:
    I=180,000: CP-21 46,548; CP-23 264,312; CP-34 53,298; CP-41 214,056; CP-44 141,876; CP-47 91,080; others 0 -> sum 811,170
    rounded 50k/250k/50k/200k/150k/100k = 800,000.
    I=170,000: 43,962; 249,628; 50,337; 202,164; 133,994; 86,020 (766,105) -> 50/250/50/200/150/100 = 800,000.
    I=183,200 (my MLE of the inclusion rate from the data): 47,375; 269,011; 54,246; 217,861; 144,398; 92,699 (825,591) -> 50/250/50/200/150/100 = 800,000.
    I=190,000: 49,134; 278,996; 56,259; 225,948; 149,757; 96,140 (856,235) -> 50/300/50 or 250(CP-41 225,948 -> 250)/150/100 = 900,000.
C4  Per-programme mean taint x non-certain population value (Hansen-Hurwitz by programme): CP-21 38,430; CP-23 428,005; CP-34 43,797;
    CP-41 223,689; CP-44 146,731; CP-47 86,793 -> sum 967,446; rounds 50(CP-21 38k->50k)/450/50/200 (223.7k->200k)/150/100 -> 1,000,000.
C5  Pooled mean taint x total non-certain value: 819,492 (-> not programme-resolved).
Rounding-edge spread across plausible I (153k..187k): authority figure holds at 800,000 under C3; CP-23 flips to 300k at I>187.5k; CP-41 to 250k at I>189.2k;
lower edges: CP-23 -> 200k below I=152.7k, CP-41 -> 150k below 147k, CP-44 -> 100k below 139k, CP-47 -> 50k below 148k.
Certain-selection share (certain value / programme recorded value, certain = amount >= 150k, same set for any threshold in (108,945.95,180,726]):
CP-11 .3524 CP-14 .3419 CP-21 .1849 CP-23 .1688 CP-31 .4263 CP-34 .1841 CP-41 .1383 CP-44 .1559 CP-47 .1404
(if 108,945.95 were also certain, CP-21 becomes .1979).
Easy way: value-weighted error rate x population (C2, ~150k) gives an authority figure ~1/5 the inclusion-weighted one and accepts the population
(below 1,160,000) where C3 plus basic precision (3.0 x 180,000 = 540,000 -> ~1.35m) refers it.
Recovery of I alternatives: (a) certain boundary from record: I in (108,945.95 or 85,087.70, 180,726]; (b) non-certain value / tested count = 181,847;
(c) MLE from inclusion pattern 183,200 (+-6% sampling noise); (d) per-programme (non-certain value / count) ranges 148k..321k, so no per-programme interval;
(e) systematic sampling in ledger order from a start: best fit I=180,000 leaves 199 mismatches, so not systematic in ledger order; (f) no I at all (C2).

---------------------------------------------------------------------------------------------------
# PART 2: VERDICT (written after reading submission_graded_blocks.md)

## Verdict
**NOT_DETERMINISTIC. Disposition: SEND_BACK.** Solution is not wrong on the headline call (800,000 / refer / Rail siding and yard 250,000 reproduce under
the pooled-interval reading), but the golden holds only under an unfiled method and an unfiled interval; a defensible, equally natural reading gives
1,000,000 and CP-23 450,000, and two graded critical components cannot be reproduced to the cent from anything shipped.

## Probe 1: estimand filed, method open?
- Population: 9.1 "every payment line in the population ... the year in which the line was paid"; 9.4 programmes from the register; ledger
  paid_date all in 2026 (2025 file is wholly 2025). Fixed. Redeliveries (delivery_sequence 2, 222 rows) closed by field_dictionary. Reversed/credit pairs closed by dictionary.
- Outcome: 9.1 euro by which recorded exceeds properly payable. Fixed. Window: year of payment. Fixed. Unit: euro, nearest 50k, authority = sum of stated. Fixed.
  Comparison: recorded vs amount properly payable; population vs 4.2 tolerable (1,160,000) at 95% in 4.3. Fixed in words.
- Literal execution of 9.1: the quantity is the population's total misstatement over every line. No column holds it (9.2 says so). The testing covers 271 of 26,652 lines.
  Literally the only quantity the record gives is the found 15,445.38 (C1), which is the misstatement of the tested lines, not the population.
- Method sentences shipped: none. No interval, selection count, inclusion probability, projection, weighting, stratum, reliability factor or ordering is stated anywhere
  (audit_manual 9.1/9.2/9.4/9.7, audit_plan 4.1-4.6, provenance, dictionary). "Certain of selection" (asked in the prompt) and "taintings", "basic precision", "incremental
  allowance", "upper limit" (recommendation) are defined nowhere in the bundle. Method is wholly open, and the design that forces it is only inferable from the tested-line pattern.

## Probe 2: candidates (see part 1). Which I would file: C3 at I = 180,000, programme figures 0/0/0/50k/50k/100k/150k/200k/250k, authority 800,000, because the
certain stratum (lines >= 180,726, 31 lines, all whole-euro) and the pooled inclusion rate (MLE I = 183,200; non-certain value / non-certain tested = 181,847) agree. The competing C4 (below) I
cannot exclude.

## Probe 3: recovery of the population scale
Recovered I from: (a) certainty boundary: I in (85,087.70, 180,726] (108,945.95 tested, non-whole-euro, so sampled if I > 108,945.95); (b) non-certain value / tested count 181,847;
(c) MLE of pi = v/I over all non-certain lines 183,200 (95% band about 172k-196k); (d) per-programme non-certain value / tested count (each programme its own interval; equals
mean taint x non-certain value); (e) systematic from a start in ledger order: best fit 199 line mismatches, refused; (f) no interval, value-weighted ratio.
Figures: (a)/(b)/(c) -> 800,000 (CP-23 250k, CP-41 200k, CP-44 150k, CP-47 100k, CP-21 50k, CP-34 50k). (d) -> CP-21 38,430 (50k), CP-23 428,005 (**450k**), CP-34 43,797 (50k), CP-41 223,689 (200k),
CP-44 146,731 (150k), CP-47 86,793 (100k): authority **1,000,000**. (f) -> 129,202 pooled / 152,457 by programme (authority ~100k-150k, CP-23 50k).
Using the all-line population as the base for I (59.47M/271 = 219,445) -> 900k-ish (CP-23 300k, CP-41 250k).
What the record admits: pooled common interval (admitted: expected tested per programme at I=180k is 49.9/38.8/38.0/29.1/17.8/21.4/16.7/15.5/15.2 against actual 51/42/46/18/10/26/16/15/16,
chi-square 10.8 on 8 df, p about 0.2, so a common Poisson-type interval is not refused) and the per-programme interval (not refused either: nothing in the record shows the sample was
drawn with a common interval rather than a programme-by-programme count). Neither is refused by anything shipped. I cannot tell which; the answer to CP-23 and the authority figure moves
between 250k/800k and 450k/1,000,000. Across I from 153k to 187k the pooled-interval figures hold; outside it CP-23 -> 200k (below 152.7k) or 300k (above 187.5k) and CP-41 -> 250k (above 189.2k).

## Probe 4: rounding edges (pooled I = 180,000; unrounded -> nearest 50k line, distance, flip condition)
- CP-21 46,548 -> lines 25k/75k, 21.5k; flips only I < 96.7k. Stated 50,000.
- CP-23 264,312 -> line 275,000, 10,688; flips at I > 187,400 (+4.1%). Stated 250,000. Closest to an edge.
- CP-34 53,298 -> 25k/75k, 21.7k. Stated 50,000.
- CP-41 214,056 -> line 225,000, 10,944; flips at I > 189,200 (+5.1%). Stated 200,000.
- CP-44 141,876 -> line 125,000, 16,876; flips at I < 158,400 (-12%). Stated 150,000.
- CP-47 91,080 -> line 75,000, 16,080; flips at I < 148,200 (-18%). Stated 100,000.
- CP-11, CP-14, CP-31: exactly 0 (no tainted line among 51, 42, 10 non-certain tested lines; no found error in the certain stratum). Genuinely nil on arithmetic, not an edge wearing a zero;
  but a nil that depends on the sample having drawn no error (sampling luck), which a different recovery cannot change.
- Authority: sum of stated figures = 800,000 (unrounded sum 811,170.09, 13.8k below the 825k line only if figures were not stated first; by 9.1 the stated sum governs).
- Grain: the write-up's 50,000 grain is the filed one (9.1). Rounding is not chosen to make the figures agree.
- Informativeness: nine figures carry six distinct values (0,0,0,50,50,100,150,200,250). A single rate times one column does not reproduce them (it would put a nonzero value on the three nil
  programmes); the nil/non-nil split and the order need the taint pattern. Adequately informative.
- Certain shares: CP-11 35.2, CP-14 34.2, CP-21 18.5, CP-23 16.9, CP-31 42.6, CP-34 18.4, CP-41 13.8, CP-44 15.6, CP-47 14.0, authority 26.6 all reproduce at certainty cut anywhere in
  (108,945.95, 180,726]. If the cut were <= 108,945.95, CP-21 -> 19.8 (and authority 26.8). The data refutes such a cut (pooled inclusion fit), but no sentence does.

## Recomputation ledger (claimed / recomputed)
- Lines in population 26,648, recorded 59,469,739.92 -> 26,652 deduped rows less 4 reversal/credit rows = 26,648; total 59,469,739.92 (same either way, pair nets nil). Reproduced.
- Lines tested 271 recorded 21,043,847.13 -> 271 distinct; 21,043,847.13 (272 rows is 21,224,573.13). Reproduced. 31 certain holding 15,826,525.00 -> reproduced.
- Found 15,445.38 -> reproduced (10 exceptions). 43,648.52 -> 15,445.38 x 59,469,739.92 / 21,043,847.13 = 43,648.52 reproduced. 129,201.54 -> reproduced (pooled value-weighted).
- Projection 811,170.09 = 180,000 x sum of taints -> reproduced only if I = 180,000, which is not shipped (my recoveries give 181,847/183,200).
- Basic precision 540,000 = 3.0 x 180,000 -> reproduced only with the factor 3.0 (exact Poisson 95% factor 2.996 gives 539,280) and I = 180,000. Not shipped.
- **Incremental allowance 347,797.48 over 10 taintings: did NOT reproduce.** My value 347,603.78 (exact chi-square Poisson factors) or 347,332.00 (two-decimal published table). Neither matches to the cent; table not in bundle.
- **Upper limit 1,698,967.57: did NOT reproduce** (mine 1,698,773.9 with exact factors; 1,698,502 with table). The refer call is robust (projection + basic precision alone is 1,351,170 > 1,160,000).
- Tolerable 1,160,000 "2.0 per cent of budgeted capital expenditure": register budgets sum to 59,481 thousand, 2.0% = 1,189,620. **Did not reproduce** (58,000 thousand needed). Call is unaffected.
- Programme figures: reproduced under C3 (I 153k-187k); did NOT reproduce under C4 (CP-23 450,000; authority 1,000,000).
- Runs by quarter (released quarter, PR-26-017 once): 25/26/27/26 reproduced; past cut-off 9/8/5/6 and values 5,303,327.24 / 5,217,457.85 / 3,433,308.73 / 3,470,389.62 reproduced (gross run_value_eur; net of
  reversed_value would be 5,215,326.86 for Q2). Forks: quarter by run_date gives runs 26/26/26/26; a release after midnight judged against the run day's cut-off gives past 13/9/7/7 (7,692,261.69 / 5,621,180.86 /
  4,286,745.00 / 3,885,419.38).
- Risk categories: raised 0/29/42/31/39 reproduced (accepted events only, labels mapped; superseded would add 2,5 to categories 2,3). "Removed into it" 25/24/36/26/0 reproduced as moved DOWN into the category;
  "raised then removed" 0/16/11/16/0 reproduced only as raised into the category then later moved OUT of it. The prompt says "those removed", which read literally is removed from the category (31/69/49/76/27 move out
  of cat 1..5; 0/24/23/37/27 moved down out). The dictionary claims categories move one way and never return, contradicted by the data (both directions occur). Open fork on the ask.
- Lines covered per month: 34/19/26/17/25/23/28/14/27/24/12/23 reproduced as ROW counts (272). Distinct lines are 33 in January (the 1 duplicate row CPL-26-095171, 2026-01-30). The submission elsewhere says 271 lines
  tested, so January 34 counts the duplicated line twice. Fork: 33 vs 34. Missing from ledger: none (reproduced). Duplicated: 1 (reproduced).

## Gates
- A (computation/determinism): FAIL. Programme figures depend on an unfiled interval and an unfiled choice between a common interval and a programme-by-programme count (CP-23 250k vs 450k; authority 800k vs 1,000k); the
  incremental allowance and upper limit do not reproduce to the cent; asks carry forks (removed, quarter basis/cut-off day, January 33 vs 34).
- B (inputs in bundle): FAIL. Needed from the field and not shipped: Poisson reliability factors / incremental-allowance method, basic precision factor 3.0, the meaning of "certain of selection", "taintings", the selection interval.
  Tolerable 2.0% does not match the register.
- C-E: no further issue found (units, 2025 vs 2026, redeliveries, reversals, superseded events closed by the dictionary).
- F (stump power): high. The easy routes (15,445 found; 43,648 on recorded value; 129,202-152,457 value-weighted/stratified ratio) all accept the population and put every programme at 0 to 50k; only the
  inclusion-weighted projection refers it. A strong analyst who guesses a ratio estimator fails.
- G (**Gate G line**): PASS. No shipped artifact ranks programmes on the misstatement question and gets it wrong. grant_claim (claim year to 31 March), revenue_expenditure_summary and the 2025 ledger/testing rows are
  wrong-population or wrong-basis files that do not rank programmes on misstatement; the 2025 extract (15,878.96 over 9 exceptions) is a different year.
- H (**Gate H line**): domain = internal audit substantive testing / audit sampling (real: projecting tested lines to the population); layers = Layer 1 redelivered rows, reversed pairs, 2025 vs 2026, supplier-number
  crosswalk, superseded events, relabelled categories; Layer 2 = recognising the tested set is selected with probability proportional to value above a certain stratum and weighting the taints accordingly;
  decisive_step = project taints through the inclusion probabilities (recovered interval), certain stratum at its own error. Classification: analytical (data's real structure/estimand), not a planted decoy and not
  data semantics; but not pure rule application only if the method is recoverable, which it is not exactly because the method and interval are unfiled (so the step also leans on field knowledge, Gate B).
- Three rules: No decoy: pass (the 43,648 ratio route is an easy wrong route, not a certified decoy). Not semantics: pass for the main call. Not rule application: pass (no shipped rule produces the figure).

## Stumping type
mechanism: inclusion-probability (monetary-unit style) projection of tested-line taints with a certain stratum; stumping_family: wrong estimator on a size-biased sample (value-weighted ratio / found-only);
surface_read_dependency: none for the declared distractors (grant claim, revenue summary, 2025 rows are not on the path); sole_data_defect: none (no planted defect).

## Fix
File the WHAT of the selection (that selection was with probability proportional to recorded value from the lines not certain of selection, the interval or sample size in force and whether it was common to
the programmes, and what certain of selection means) in a shipped sentence, and file the reliability factor table or drop the incremental allowance and upper limit from the graded critical components; correct the
2.0 per cent tolerable to the register; file "removed" and the January line count (lines versus rows) and the quarter/cut-off day basis for the asks.
