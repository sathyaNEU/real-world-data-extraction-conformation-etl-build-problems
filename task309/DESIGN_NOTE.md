# task309: which county gets the 2027 roof-retrofit grant round, and the hurricane loss it removes there

Wave 7, Opportunity Sizing & Decision Support. Architecture 1, drawn 2026-10-27. Seed OS11 (an express-lane conversion
under a toll cap) is spent: task308 tried its corridor world and task307 holds road networks, so the build keeps only
the seed's decision form (which of N gets one scarce programme, sized as an annual sum) and moves to a pairing and a task
type never drawn, actuarial-science-insurance / catastrophe-exposure-accumulation. No probe, reader or solver was run
(the STOP rule); the stump is argued on paper below.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | actuarial-science-insurance / catastrophe-exposure-accumulation (serves Opportunity Sizing) |
| Objective | Opportunity Sizing & Decision Support: the headline is the 2027 expected hurricane loss the round removes, sized from the pool (each county's modelled annual loss on its eligible homes) to the realisable (the part a FORTIFIED re-roof takes off it, event by event), and the largest figure picks the county |
| Decision / answer unit / question form | pick_one_of_n / named_option with a USD figure / which |
| Shape | 01, a ranked list of the four counties (each county's annual loss and loss removed, the call, the runner-up and the gap) |
| Gap / pattern / generators | rule, population / none / G6 (composition), G14 (conditioned yield) |
| Gate G / strategy | method_or_model_selection / composition_mix: the cut the retrofit gives depends on the event's local gust, and the record's exposure and each county's annual loss sit in different parts of the gust range |
| Layer 2 | estimation_fit, own:a-mitigations-loss-reduction-falls-with-local-gust |
| Forum / forcing event / org family | board_of_directors (Sandpiper's board, January 2027 meeting) / season_or_peak (re-roofs finished before the 1 June 2027 start of the hurricane season) / financial_institution |
| Stakeholder | Sherry Lang, Catastrophe Risk Manager (portfolio_manager) |
| People (guard.py names --geo "United States" --seed 309) | Sherry Lang; Andrew Mack, Claims Director (the storm close-out summaries); Eric Brown, Chief Risk Officer (the model-governance standard) |
| World | Sandpiper Mutual Insurance Company, a mutual homeowners insurer on a fictional US Gulf Coast; USD; records to 30 September 2026, board paper November 2026 |
| Deliverables | retrofit_round_2027.xlsx (the county workbook), avoided_loss_by_county.png (the chart for the board pack), board_note_retrofit_2027.docx (the one-page note) |
| Guard | WARN only: repeat.gate_g against task270, repeat.question_form against task139 and task270, people.first |

The WARNs, answered: the decisive move is a choice between a one-ratio model and an intensity-conditioned one that a
filed criterion and the claims settle, so method_or_model_selection is the honest Gate G; the board picks one county,
so the question is which. The axes redrawn at the check: the decisive generator from G14 to G6 (G14 is task308's
pattern, inside the ban window), the decisive gap from population to rule after (population, G6, pick_one_of_n) repeated
task144's lineage inside the batch (the company's model-governance standard is a filed criterion the claims settle,
C2), and the context artifact from filed_model (task307) to close_out_summary, the claims department's per-storm
close-out summaries, which are the catastrophe risk manager's own file; the vendor's event set is an input.

### Candidates written before the choice (each with its default path)

1. **Survey boost inside existing clusters** (survey-research-official-statistics / sample-design-allocation-weighting x
   OS: which region gets a labour force survey boost, sized as local-area estimates made publishable). Default: scale
   each published CV by the root of the sample ratio, the region with most near-threshold areas. Dropped: the design
   effect under a larger take per cluster is Kish's textbook formula, small-area shrinkage is on file as a reflex the
   opponent applies unprompted (task253), and the boost specification that the estimand needs names the clusters.
2. **Deprescribing review where risk concentrates after initiation** (pharmacology / benefit-risk-assessment x OS: which
   drug class gets a falls-prevention medication review). Default: pooled excess fall rate over all exposed time times
   current users. Dropped: the natural prevalent-user cohort from a snapshot date lands the golden without any insight,
   and confounding by indication forks the estimand.
3. **Currency hedge on a fund's foreign sleeves** (quantitative-finance / portfolio-construction-risk x OS). Default:
   hedge the most volatile currency exposure. Dropped: the value turns on the currency's co-movement with the fund's bad
   states, task308's driver.
4. **Volume-weighted conjoint launch** (marketing-consumer-research / conjoint-choice-willingness-to-pay-analysis x OS).
   Default: share of preference times category units. Dropped: weighting a simulator by volume or distribution is
   practice (task174's screen), and task301's conjoint probe fitted latent classes unprompted.
5. **Retention of retrofitted homes** (this world, the round valued on homes still on Sandpiper's book in the season).
   Default: loss removed on every retrofitted home. Dropped: whether the round's value counts homes that leave the book is
   a reading of the estimand, a semantic fork, never a stump.
6. **The retrofit's cut read class by class of local gust (chosen).** Default: one cut ratio over the record's storms
   times each county's modelled annual loss names Marlin Shoals; golden Cypress Ridge.

The data-native sentence: the company's storm record holds its FORTIFIED homes mostly in gusts under 130 mph, where a
sealed roof deck keeps the cover on and the paid loss per insured dollar falls by about three fifths, and only a few
majors put them above 130 mph, where the structure fails with or without the roof and the fall is about a seventh; one
ratio over the record therefore averages a large cut over most of the exposure with a small cut over most of the loss,
and the vendor's 2027 event set puts Marlin Shoals' annual loss almost wholly above 130 mph and Cypress Ridge's almost
wholly below.

## Tried and rejected

- Candidates 1 to 5 above, at the draw (2026-10-27), each for the reason given on its line.
- The composition card as first drafted (gap population, G14 then G6 decisive): blocked by ban.pattern (G14, task308)
  and by test.same_puzzle against task144's lineage; redrawn with the company's model-governance standard as the filed
  criterion (gap rule) rather than relabelled.
- The vendor's own FORTIFIED loss column in the event table: dropped, it hands each event's cut over and leaves no
  analysis; the cut is read from the company's claims.
