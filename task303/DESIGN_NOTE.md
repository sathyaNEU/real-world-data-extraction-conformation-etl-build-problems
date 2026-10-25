# task303: design note

## Draw

- Number task303, wave 6, Opportunity Sizing (seed OS05, a permit centre placing ten funded positions across four
  stages). The seed's world was drawn first and died at the probes (Tried and rejected); staffing a stage pipeline reads
  the same in any office, so the swap test leaves municipal permitting a backdrop, and the world is re-drawn where the
  field's own analysis decides, keeping the seed's decision form: one commitment among four, sized by what it adds.
- Pairing: Actuarial Science & Insurance (client domain `actuarial-science-insurance`), task type
  `pricing-ratemaking-credibility` (renewal rate changes priced on each policy's response and expected claims),
  objective Opportunity Sizing & Decision Support. Never built before on this objective.
- World: Kestrel Pet Insurance, a specialist Canadian insurer of dogs and cats (head office in Ontario, policies in
  eight provinces). Four products: Lifetime Dog and Lifetime Cat cover each condition for the pet's life while the
  policy renews; Condition Year and Essentials cover each condition for twelve months from its first treatment. The
  board has approved a corrective 12 per cent increase on one product's 2027 renewals.
- Call: which product takes the increase, and what it adds to the 2027 underwriting result on the renewals due that
  year (every policy in force at 31 December 2026), valued as the pricing note does: the premiums of the policies that
  renew less the claims those policies cost over their 2027 policy year, at the claims cost of the policy years that
  started in 2025, with the increase against without it.
- Golden (prototype, seed 303 retuned): Essentials at about CAD 500,000 (512,000 to 536,000 across five licensed
  constructions); the easy routes file Lifetime Dog at 866,000 to 1,865,000.
- Candidates weighed, default path first:
  1. Road-safety programme sites read through regression to the mean: the default ranks sites by recent crashes;
     shrinkage is one of the opponent's reflexes (stumping Part 0). Dropped.
  2. Capacity credit of four resources for a 2027 obligation: the estimand names the loss-of-load computation, so a
     reader who files it computes it. Dropped.
  3. A battery at a curtailed node, its recovered energy capped by multi-day spells: an hourly state-of-charge
     simulation is the first thing a reader writes for a battery. Dropped.
  4. An ambulance post read through busy units: trace replay and the busy-fraction model are both licensed and part
     at the design's scale. Dropped.
  5. A storable line's list price read through purchase acceleration: demand moved in time is task302's heart. Dropped.
  6. A pet insurer's renewal increase on one of four products: the default prices the extra lapses at the product's
     response and the policies' own claims without asking who leaves; the owners who leave are those whose pets carry no
     continuing condition, because a continuing condition covered for life cannot be taken to a new insurer. Chosen.
- Shape `other`: the call, its figure, a chart of what each product's increase adds, and the asks (designed at stage 2).
- Furniture: role portfolio_manager (the head of pricing recommends to the board, forum board_of_directors), forcing
  event launch_or_rollout (the 2027 renewal price list), organisation financial_institution, calibration
  existing_book_actuals (the book's own renewal history), context artifact other (the pricing team's note).

## Three rules

Task type: pricing-ratemaking-credibility, the renewal-pricing part of it (a rate change's effect on a product's result
read from each policy's renewal response and expected claims), which the taxonomy lets serve Opportunity Sizing &
Decision Support.
Domain test: the deciding quantity is the change in a product's underwriting result from a renewal rate increase, net of
the margin on the policies the increase drives away, which pricing actuaries estimate from each policy's renewal response
and expected claims; the response is set by whether the owner can replace the cover, and any new insurer excludes a
continuing condition as pre-existing, so lifetime cover keeps exactly the owners whose pets cost most.
Swap: put schools or hospitals in for pet insurance products and the call loses its terms: no pre-existing-condition
exclusion stops a family moving a child, and no lapse at an annual renewal ends a hospital's book; the task reads only as
an insurer's.
Layer 1: a policy administration migration in April 2024 renumbered every policy (a crosswalk joins a pet's two
numbers); veterinarians' free-text diagnoses carry abbreviations and variants the claims team codes to condition ids;
claims are paid net of a deductible and co-insurance, and a reopened claim adds a second payment row; renewal
invitations sit in a separate system with the premium offered, re-issued after a mid-term change; policies end mid-term
when a pet is rehomed or dies; part of the book carries a multi-pet discount. Each comes from the insurer's own systems
and none is placed to be caught.
Layer 2: estimand identification (the policies an increase drives away are not the product's average policies): the
renewal response differs by whether the owner can replace the cover, and the margin differs the same way, so the
increase's yield is the rise on those who stay less the margin of those who leave, each counted at its own.
Decisive step: splitting each lifetime product's renewal response by whether the pet carries a continuing condition the
product keeps paying (rebuilt from the claims history's condition ids), so that the extra lapses an increase brings are
counted as the healthy pets they are and valued at their margin.
Not semantics: every field, code, condition id and the note's valuation can be read correctly and the easy route still
fits one response per product (with age, tenure and claim history) and lets the extra lapses fall across the book's
policies in proportion, because no file names the barrier; it lives only in the joint of the renewal history and the
condition ids.
Not rule application: no filed rule says who lapses; the note files the population (the policies in force at 31 December
2026), the outcome (premium of the renewing policies less their claims), the window (their 2027 policy year), the cost
level (the 2025 policy years) and the comparison (with the increase against without it), never how the renewal response
is read. Enumerated family on the retuned prototype, 8 constructions (one response per product with average or own
claims, with age, with claim history, and five that split the lifetime products' response by a continuing condition):
two products named, the named figure from CAD 512,000 to 1,865,000. Standing family, the five that split the response
(logistic with and without age and claim history, grouped rates by product and condition with a linear response): all
five name Essentials at 512,000 to 536,000 (within one printed unit of CAD 50,000), at least 300,000 above the next
product. Ruling-out loudness: no clause rules the one-response routes out; the renewal history does, the owners of pets
with a continuing condition on a lifetime product renewing at about 97 per cent across every offer against 63 to 87 per
cent for the rest, a split nothing in the files names.
Analyst test: a strong analyst who fits the owners' renewal response to past offers by product, with age, tenure and
claim history, and values every renewing policy at its own expected claims puts the increase on Lifetime Dog at about
CAD 0.9 to 1.9 million, where the golden is Essentials at about CAD 500,000.
Estimand: the pricing note (pricing_note_2027.docx) files the population, outcome, window, cost level and comparison
above, and the policy file carries each in-force policy's scheduled 2027 renewal premium before any rate change.
No decoy: nothing is planted; no memo, briefing, dashboard or broker figure prices the products, the claims system
publishes no retention or margin figure, and the distractors rank nothing on the question.
No certified replay: no certified or published figure is reproduced to recover a method; the increase and the cost
level are inputs the note files.
Lesson: a model learns that a price rise's yield on a book depends on who it drives away, that the response and the
margin covary when the members who cost most are the ones who cannot leave, and that the barrier is read from each
member's own history rather than a column; no build on file prices a renewal increase through who can replace the cover.

## Default path

1. Read the pricing note: one product's 2027 renewals take 12 per cent on the scheduled renewal premium; the addition is
   the premium of the policies that renew less their 2027 claims at the 2025 policy years' cost, with against without.
2. Join the policy periods to the claims through the 2024 crosswalk and total each period's paid claims.
3. Fit the owners' renewal response to the offered change from the past renewals, by product, with age, tenure and claim
   history (a logistic regression or grouped rates).
4. Value each in-force policy at its own expected 2027 claims (by product, age and claim history) and sum the change in
   (renewal probability times margin) at 1.12 times the scheduled premium against 1.00, by product.
- Ends on: Lifetime Dog at about CAD 0.9 to 1.9 million (the largest premium, its claim-history response still
  spreading the extra lapses across costly and healthy dogs alike).
- Golden: Essentials at about CAD 500,000 (Lifetime Dog near nil, Lifetime Cat about 150,000 to 210,000).

## Stump sentence

A competent solver fits the renewal response to past offers by product with claim history, values each renewal at its
own expected claims and puts the increase on Lifetime Dog at about CAD 0.9 million or more, where the golden is
Essentials at about CAD 500,000; the step that lands it there is reading the renewal response as the product's, when the
owners of pets with a continuing condition covered for life renew whatever the price and the increase drives away only
the healthy pets, whose margin is the book's highest.

Data-native sentence: on the lifetime products the owners of pets with a continuing condition renew at about 97 per cent
whatever the offer, while the rest lapse at 18 to 37 per cent as the offer rises, and a healthy lifetime dog's margin is
about CAD 340 against minus 1,080 for one with a continuing condition, so the extra lapses an increase brings are
almost all margin.

## Tried and rejected

- Permit centre standard plans (the seed's world, municipal permitting x Opportunity Sizing: ten funded positions across
  intake, plan review, corrections and issuance, plan review's 2027 load driven by the builders entering the city with
  their plan libraries): both call-only probes landed the allocation (intake 3, plan review 3, corrections 1, issuance
  3) from the builders' outlook; and staffing a stage pipeline reads the same in any office, so the swap test fails.
