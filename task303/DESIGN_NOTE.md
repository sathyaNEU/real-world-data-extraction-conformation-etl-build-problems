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
- Golden (built pack): Essentials at CAD 0.5 million (0.463 to 0.509 across the 144 constructions that split the
  lifetime products' response by a continuing condition); the one-response routes file Lifetime Dog at CAD 0.5 to 1.9
  million.
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
- Shape `other`: the call, its figure, a chart of what each product's increase adds, and three asks by product and
  quarter of 2026 (the renewals-line calls, the renewal-premium complaints, the monthly instalments never collected),
  48 cells: about 30 criteria with the call, the figure, the chart and the two files.
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
Layer 1: the policy administration system that went live on 15 April 2024 renumbered every policy, so terms before it
sit in a legacy archive with its own layout, codes and day-first dates, the term in force at the go-live sits in both
systems, and a crosswalk joins a pet's two numbers; invitations and claims carry the reference in use when they were
issued or lodged; clinics' free-text diagnoses carry abbreviations and variants under the claims team's condition
references; claims are paid net of a deductible and co-insurance, a reopened claim adds a second payment row, and a
claim still being assessed at the extract has no payment; about one invitation in thirty went out with a wrong premium
and was issued again; policies end mid-term when a pet dies or the owner cancels; part of the book carries a multi-pet
discount. Each comes from the insurer's own systems and none is placed to be caught.
Layer 2: estimand identification (the policies an increase drives away are not the product's average policies): the
renewal response differs by whether the owner can replace the cover, and the margin differs the same way, so the
increase's yield is the rise on those who stay less the margin of those who leave, each counted at its own.
Decisive step: splitting each lifetime product's renewal response by whether the pet carries a continuing condition the
product keeps paying (rebuilt from the claims history: the condition references and what the clinics diagnosed), so that
the extra lapses an increase brings are counted as the healthy pets they are and valued at their margin.
Not semantics: every field, code, condition reference and the note's valuation can be read correctly and the easy route
still fits one response per product (with age and claim history) and lets the extra lapses fall across the book's
policies in proportion, because no file names the barrier; it lives only in the joint of the renewal history and the
condition references.
Not rule application: no filed rule says who lapses; the note files the population (the policies in force at 31 December
2026), the outcome (premiums of the renewing policies less their claims), the window (their 2027 policy year), the cost
basis (what the 2025 policy years that ran to their renewal date had paid by 31 December 2026) and the comparison (1.12
times the scheduled premium against it), never how the renewal response or the claims are estimated. Enumerated family on
the built pack, 149 constructions (five one-response routes and 144 that split the lifetime response): two products
named, the named figure from CAD 0.46 to 1.89 million. Standing family, the 144 that split the response (four ways of
marking the condition, nine response models, four claims models): all name Essentials, all print CAD 0.5 million (0.463
to 0.509), at least CAD 37 thousand above the next product. Ruling-out loudness: no clause rules the one-response routes
out; the renewal history does, the owners of lifetime pets with a continuing condition lapsing 3 to 7 per cent in every
offer band against 13 to 40 per cent for the rest, a split nothing in the files names.
Analyst test: a strong analyst who fits the owners' renewal response to past offers by product, with age and claim
history, and values every renewing policy at its expected claims puts the increase on Lifetime Dog at about CAD 0.5 to
1.4 million, where the golden is Essentials at CAD 0.5 million.
Estimand: the pricing note (pricing_note_2027.docx) files the population, outcome, window, cost basis and comparison
above, and policy_terms_2024-2026.csv carries each in-force policy's scheduled 2027 renewal premium before any change.
No decoy: nothing is planted; no memo, briefing, dashboard or broker figure prices the products, the claims system
publishes no retention or margin figure, and the distractors rank nothing on the question.
No certified replay: no certified or published figure is reproduced to recover a method; the increase and the cost
level are inputs the note files.
Lesson: a model learns that a price rise's yield on a book depends on who it drives away, that the response and the
margin covary when the members who cost most are the ones who cannot leave, and that the barrier is read from each
member's own history rather than a column; no build on file prices a renewal increase through who can replace the cover.

## Default path

1. Read the pricing note: one product's 2027 renewals take 12 per cent on the scheduled renewal premium; the addition is
   the premium of the policies that renew less their 2027 claims at what the 2025 policy years paid, with against
   without.
2. Join the legacy and new terms through the 2024 crosswalk, take each renewal's offer from the invitations and total each
   term's paid claims.
3. Fit the owners' renewal response to the offered change from the past renewals, by product, with age and claim history
   (a logistic regression or grouped rates).
4. Value each in-force policy at its expected 2027 claims (by product, age and claim history) and sum the change in
   (renewal probability times margin) at 1.12 times the scheduled premium against 1.00, by product.
- Ends on: Lifetime Dog at about CAD 0.5 to 1.4 million (the largest book, its response read as the product's and its
  extra lapses spread across costly and healthy dogs alike).
- Golden: Essentials at CAD 0.5 million.

## Stump sentence

A competent solver fits the renewal response to past offers by product with age and claim history, values each renewal
at its expected claims and puts the increase on Lifetime Dog at about CAD 0.5 to 1.4 million, where the golden is
Essentials at CAD 0.5 million; the step that lands it there is reading the renewal response as the product's, when the
owners of pets with a continuing condition covered for life renew whatever the price and the increase drives away only
the healthy pets, whose margin is the book's highest.

Data-native sentence: on the lifetime products the owners of pets with a continuing condition lapse 3 to 7 per cent in
every offer band while the rest lapse 13 per cent at offers of 6 to 10 per cent and 40 per cent above 18, and a Lifetime
Dog policy renewing in 2027 carries a margin of about CAD 360 without a continuing condition against minus 1,280 with
one, so the extra lapses an increase brings are almost all margin; an Essentials renewal's margin is about nil.

## Ladder

| Rung | What the solver does | Files |
|---|---|---|
| R0 | prices the increase on the scheduled premiums with no lapse response | Lifetime Dog, CAD 1.9 million |
| R1 | one renewal response a product (logistic on the offered change), each renewing policy at its product's average 2025 claims | Lifetime Dog, CAD 1.1 million |
| R2 | adds age to the response and costs claims by age band | Lifetime Dog, CAD 1.4 million |
| R3 | adds claim history to the response and costs claims by age and claim history | Lifetime Dog, CAD 0.8 million |
| R4 | adds the claims paid in the term to the response and costs claims by age and paid band | Lifetime Dog, CAD 0.5 million (Essentials 0.4) |
| R5 (decisive) | splits the lifetime products' renewal response by a continuing condition rebuilt from the condition references, and costs 2027 claims by condition status | Essentials, CAD 0.5 million |

## Readability screen

| Rung | Where a file shows it | Verdict |
|---|---|---|
| R1 the offered change | the invitations against the terms' premiums | readable |
| R2 age | the tariff's age loading and the pets' dates of birth | readable |
| R3 and R4 claim history | the claims file | readable |
| R5 (decisive) the continuing condition's hold on the lifetime renewal response | no file names it: it lives in the joint of the renewal history and the condition references; the dictionary states the products' cover as product facts and no file says who renews | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the population | each product's policies in force at 31 December 2026 (term_status In force), each renewing once in 2027 | the 2027 renewals plus 2027 new business | not a reading: new business has no 2027 renewal | the note: "the population is the product's policies in force at 31 December 2026" and "leaves out ... new business" |
| SF2 | the cost base | the policy years that started in 2025 and ran to their renewal date | every policy year that started in 2025, those cut short included | same call, CAD 0.5 million (asserted) | the note: "the policy years that started in 2025 and ran to their renewal date" |
| SF3 | the offer a past renewal answered | the last invitation issued for that renewal date | the first invitation | same call (asserted on the revised invitations) | the dictionary: a Revised renewal invitation is "issued again with a corrected premium" |
| SF4 | a claim's cost | every payment row, a reopened claim's second payment included | the first payment only | same call (asserted on the second payments) | the dictionary: payment_no 2 is "a further payment" |
| SF5 | the age a 2027 claim is costed at | the pet's age at its 2027 renewal | its age at the start of the 2026 term | same call (asserted) | the note: the claims "over the policy year that starts at that renewal" |
| SF6 | claims still being assessed | nothing paid by 31 December 2026 | valued at their invoice less the deductible and co-insurance | same call, CAD 0.5 million (asserted) | the note: "what the policy years ... had paid by 31 December 2026" |
| SF7 | the premium the increase applies to | 1.12 times renewal_premium_2027 | 1.12 times the 2026 term's premium | Lifetime Dog | the note: the increase "is applied to the scheduled renewal premium" and the policies renew "at 1.12 times it" |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | each product's policies in force at 31 December 2026, each renewing once in 2027 | filed in the note (SF1) |
| 2 Unit of account | CAD of the product's 2027 underwriting result | the question and the note |
| 3 Attribution window | each policy's 2027 policy year, from its 2027 renewal date | the note |
| 4 As-of dating | the systems' extract on 31 December 2026; claims paid by then | the note (SF6) |
| 5 Version basis | the last invitation issued for each renewal date | the dictionary (SF3) |
| 6 Denominator | none: an amount | no rate in the estimand |
| 7 Weighting | each policy at its own scheduled premium and expected claims | the note |
| 8 Window length | the renewal history from 2020; renewals from 2022 only give the same call and figure | C1 (family) |
| 9 Boundary inclusivity | in force at 31 December 2026 inclusive; 2025 policy years starting 1 January to 31 December 2025 | the note |
| 10 Rounding path | the product's addition rounded once to CAD 0.1 million | the prompt; every construction prints 0.5 |
| 11 Tie-break | none needed | the call leads the next product by CAD 37 thousand or more in every construction |
| 12 Maturity and censoring | 2025 policy years cut short left out; claims paid by 31 December 2026 | the note (SF2, SF6) |
| 13 Order of operations | the response and claims models, then each policy with and without, then the sum | one path |
| 14 Row order | none | grouped computations only |
| 15 Duplicate resolution | the archive's MIGR rows are the new system's terms; a revised invitation replaces the first | the dictionary (SF3) |
| 16 Identity normalisation | legacy references to policy numbers through the crosswalk | the crosswalk |
| 17 Netting against gross | claims as paid, after the deductible and co-insurance, every payment row | the dictionary (SF4) |
| 18 Dimensional units | CAD throughout | the dictionary |
| 19 Code and status semantics | the archive's product and status codes | the dictionary |
| 20 Integerisation | none before the final rounding | one rounding |
| 21 Clause scope | the increase on every renewing policy of the chosen product, on its scheduled premium | the note (SF7) |
| 22 Forward window contents | the 2027 renewals priced on the 2020 to 2026 renewal history and the 2025 claims | the note |

## Literal reader

Executed word for word, the pricing note fixes the population (each product's policies in force at 31 December 2026,
each reaching its 2027 renewal date once), the outcome (the premiums of the policies that renew less the claims those
policies cost over the policy year that starts at that renewal), the comparison (1.12 times the scheduled premium
against the scheduled premium) and the cost basis (what the 2025 policy years that ran to their renewal date had paid by
31 December 2026). It leaves open how the owners' renewal response and the 2027 claims are estimated, and no sentence
read literally names a product, a response model or a cell. Every construction that splits the lifetime products'
response by a continuing condition names Essentials at CAD 0.5 million (144 of 144: four ways of marking the condition,
nine response models, four claims models), and the renewal history prefers marking a condition from its first treatment
to marking it only once it recurs (log-likelihood 753 better) or once it spans 90 days (357 better).

## Oracles

None. No file carries a product's retention, lapse response, margin or addition; the tariff workbook carries rates and
factors only. The vet fee benchmark and the clinic network are reference files the call does not need (named in
metadata.json as distractors) and rank nothing.

## Ask sheet

Ask A, the calls in which each product's policyholders chose renewals and premiums at the customer line's menu, by
quarter of 2026 (16 cells). Use: the contact load each product's renewal season already brings, a measure every
candidate carries that the call does not turn on. The call handling system records the option number; on 5 October 2026
the menu was reordered (claim status up to option 2, renewals and premiums to option 3), each option passing its calls
to the queue of its own number, and the dictionary gives the menu and the queues as they stand at the extract. Device D2
(a label stored before a silent switch), silent: nothing marks the change, and the menu and queue descriptions agree
with each other; the evidence is a cross-file cut, the agents' wrap codes on the queued calls (renewal codes on option 2
until 4 October and on option 3 after) and the calls' timing after each policy's invitation. Read with the dictionary's
menu all year, Q1 to Q3 count the claim-status calls and Q4 four days of them; every cell moves. Hazard (shared with the
call): about one caller in eleven with a pre-2024 policy keys the legacy reference, joined through the crosswalk.

Ask B, the complaints about the renewal premium received for each product, by quarter of 2026 (16 cells). Use: the
conduct exposure each product's renewal pricing already carries. Customer Relations' case export lists the cases it
owns; a complaint that disputes how a premium was rated passes to the Pricing team and its case leaves the export.
Device D5 (a silently partial extract), silent: the dictionary calls the file Customer Relations' complaint cases,
which is true, and every complaint is acknowledged by Customer Relations' letter, so the correspondence log holds
acknowledgements for cases the export does not. Read from the case export alone, every cell is about a third short.

Ask C, the monthly instalments falling due in each quarter of 2026 that the bank returned and that were never
collected, by product (16 cells). Use: the affordability stress on each product's book before any increase. Billing
presents a returned debit again ten days later as a new item for the same policy and amount, and the bank's returns
list each returned item. Device D1 (a resubmission that opens no second case) with its over-cleaning half: counting
each returned item as an uncollected instalment counts the re-presented ones that were paid and both returns of one
that was not; taking one debit a policy a month, the reflex for a monthly debit, separates a re-presentation that
crosses a month end from its instalment and pairs it with the next month's. Only the chain of a returned item and the
same policy's debit for the same amount ten days later recovers the instalment.

| Ask | Cracker's handling | Cracker |
|---|---|---|
| A | the dictionary's menu read all year | miss |
| B | the case export as the complaints | miss |
| C | each returned item an uncollected instalment | miss |

Pair ceiling: 28.5 (cracker 45.0 on the call with no ask cell, mirror 12.0 off it with none); a cracker that also finds
one ask's device reaches 37.7
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/pair.py on the cut pack.

Separation: none of the ask files is read by the main call (the golden opens the two policy term files, the crosswalk,
the invitations and the claims), and the asks' devices sit in the call handling and queue exports, the case export
with the correspondence log, and the debits with the bank's returns; the crosswalk is the one file both read, and it
carries no device.

## Tried and rejected

- Permit centre standard plans (the seed's world, municipal permitting x Opportunity Sizing: ten funded positions across
  intake, plan review, corrections and issuance, plan review's 2027 load driven by the builders entering the city with
  their plan libraries): both call-only probes landed the allocation (intake 3, plan review 3, corrections 1, issuance
  3) from the builders' outlook; and staffing a stage pipeline reads the same in any office, so the swap test fails.
- A world with the Lifetime Dog tariff at its first level and narrow claim costs: marking a continuing condition only
  once it recurs in a second policy year put Lifetime Dog above Essentials in 21 of 144 constructions, and raising the
  tariff 10 per cent instead let the claims-paid route land Essentials; claim costs were given a wider spread and the
  tariff 5 per cent, with a larger Essentials book, so every split names Essentials and every route Lifetime Dog.
- A policy history from 2014 instead of 2019: the lifetime books' held owners piled up, and the recurrence and span
  markings named Lifetime Dog.
- Architecture 1, the lifetime owners held by a continuing condition (Essentials at CAD 0.5 million, every one-response route on Lifetime Dog), spent at stage 4: reader A named Essentials with a retention logit carrying claims in the expiring and prior terms by product (lifetime claimants almost never leave), a covariate reflex that reaches the split without marking a condition; the judge returned SEND_BACK because the printed addition ran from CAD 0.32 to 0.51 million across condition markings, flag timings and response fits; both readers took all 48 ask cells (the wrap codes against the menu option, the case-number gaps against the letters, a same-amount debit 10 to 14 days after each return).
