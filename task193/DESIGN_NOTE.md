# task193 design note

Which product and marker-treatment pairs the agency's prescription-sequence screen refers for formal
signal assessment in the quarter beginning 1 January 2027.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task193.json`, architecture v2, registered 2026-10-17 |
| Domain, task type | pharmacology-pharmacoepidemiology-safety, `safety-signal-detection` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 07, a grid of cells: every screened pair against its three figures |
| Decision | designation_set, the pairs referred |
| Gate G | `method_or_model_selection`; decisive generators G7 (operating window), G16 (method selection) |
| Strategy | `other`: the value of a counterfactual expectation for a within-person ordering, set by each patient's own position in the screen window |
| Layer 2 | `estimation_fit`, own pattern `own:null-expectation-of-a-within-person-ordering-set-by-the-windows-own-arithmetic` |
| World | Denmark, a national medicines agency, DKK |
| Screen window | 1 October 2025 to 30 September 2026, with the 24 months before it as the clearance period |
| As-of date | the register extract pulled 20 October 2026; the referrals are worked from 1 January 2027 |
| Guard | registered at WARN, five WARNs answered below, two differentiated NOTEs |

**Shape arithmetic to 25.** 23 screened pairs times three graded figures (the pair's patients, the
patients in whom the marker treatment came after the product, the patients in whom it came before) is 69,
with the referral on each of the 20 candidates a further 20; the call, the count referred and the pair
nearest the referral line on the wrong side are 3; the chart's named parts (one bar per screened pair, the
ordering, the referral line at its value, the two fills, the title stating the finding) are 5; the two
deliverables are 2. Ninety-nine from the shape before any ask.

**Guard WARNs answered.** `overuse.org_family`: only a national medicines agency holds a national
prescription register and runs a statutory signal screen on it, and the decision is its own; nothing else
in the pack is governmental. `overuse.objective`: the lane is Anomaly Detection and the whole wave is
drawn inside it. `repeat.gate_g` and `overuse.gate_g` against task194 and task195: the mechanism key is
shared but the two methods standing on this build's filed estimand are two arithmetics for one
counterfactual count, separated by the data itself, not a model chosen against a corpus (task194) or an
interval read two ways (task195). `repeat.question_form` against task194 and task182: the call is a set of
designations, which asks which. `repeat.deliverables` against task190: the workbook is the screen's own
output table, which the standard requires the division to publish for every screened pair, and the chart
is what makes a referral line read at a glance; the two builds share only the file extensions. The two
NOTEs (`test.same_driver_older` against task254, `driver.near` 0.12 against task50) carry their
differentiation lines in the card.

**Data-native sentence.** Two of the nine products on the screen's Annex A are being withdrawn inside the
screen window and two were first marketed inside it, so for those four the register's own first-receipt
dates are piled against one end of the window, and a patient who first receives a product in the window's
last weeks has almost no window left for the marker treatment to follow while having the whole window
behind them for it to precede.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD16: the decision shape only, which alarms a scarce
  reviewer is given. Its own architecture turns on a channel attribute that explains every alarm on it, a
  field read deciding the call, which the client's rules ban; the build is re-rooted on the field's own
  sequence screen.
- `guard.py mechanisms --objective anomaly-detection` (28 builds): the spent drivers are a detection
  threshold moving on a cycle (task180), a count read before its records arrive (task181 v2, task190,
  task457), a selected extreme against the record of extremes (task191), a shared driver with
  unit-specific lags (task182), composition against rate (task183, task125, task188), capture measured on
  the overlap of two lists (task448), left-censored measurements at instrument-specific limits (task189),
  a change of unit to the event-hour (task184), regression to the mean under selection (task194), and this
  slot's own dead comparison population (task193 v1). None of them is the value of a null expectation set
  by the window's own arithmetic.
- `guard.py nearest`: 0.12 against task50 v4 (how much of a candidate's exposure falls inside a funded
  window, projected forward from a corpus-validated issue order) and a structural triple shared with
  task254 v3 (reading each stage of a passage at the period the unit enters it). Both differentiated in the
  card: this build projects nothing, validates nothing against a corpus, and has nothing missing or
  mis-timed to recover.

## Estimand and the WHAT screen

**The decisive step, in one sentence.** Compute the number of a pair's patients expected to receive the
marker treatment after the product, if receiving the product had no bearing on when the marker treatment
is first received, from the two sets of first-receipt dates the window actually holds, rather than taking
it to be half of the pair.

**Which part of the estimand does it settle? None.** Population, outcome, window, unit and comparison are
each filed by one sentence of the standard, and the decisive step changes none of them: it changes only
the numeric value of a counterfactual the standard itself names.

| Estimand part | Filed as | The sentence that files it |
|---|---|---|
| Population | the patients whose first receipt of the product and whose first receipt of the marker treatment both fall inside the screen window, excluding any patient whose two first receipts fall on the same day | standard section 2.5, quoted in the pack |
| Outcome | for each of those patients, whether the first receipt of the marker treatment fell after the first receipt of the product, or before it | section 3.1 |
| Window | 1 October 2025 to 30 September 2026, both days included, with the 24 months before it the clearance period that establishes a first receipt | sections 2.1 to 2.3 |
| Unit | the patient; each patient counts once in each pair | section 2.5 |
| Comparison | the number that would be expected if receiving the product had no bearing on when the marker treatment is first received | section 3.2(b), with the multiple 1.25 and the 25-patient minimum in 3.2(a) and 3.2(b) |

Every one of those five is beyond argument and the same under every rung of the ladder: the pair's
patients, their two counts and the referral multiple do not move. What moves is the expected number, and
the records already fix it: two or more arithmetics stand on the same filed counterfactual, and the data's
own structure (products whose first-receipt dates are piled against one end of the window) rules out the
easy one. The step survives the screen.

**The routes that stand, and that they agree.** Four arithmetics compute the filed counterfactual from the
window's own dates: the exchangeability expectation within the pair (one over N times the number of
ordered patient pairs whose marker date exceeds the other's product date), the two drugs' window-wide
incident-use distributions taken as independent, the pair's own product dates against the marker's
window-wide incident-use distribution, and the pair's own product dates against a marker spread evenly
over the window. All four refer exactly the same seven pairs, measured on the shipped bundle and asserted
in `checks.py` and `verify.py`; the tightest margin against the 1.25 multiple across all five arithmetics
and all 20 candidates is 6.3 per cent (Oxelumab and topical corticosteroid, 1.171 on the incident-use
route). The fifth arithmetic, half of the pair, is the only one that ignores the dates, and it is the one
the data contradicts.

## Default path

1. Read `dispensings_2023_2025.csv` and `dispensings_2025_2026.csv`, reconcile the two register layouts
   (renamed columns, ISO against Danish dates) and stack them into one dispensing table.
2. Run the hygiene battery: drop the pharmacy batch re-sent under fresh line identifiers, carry the
   package codes reissued at the February 2026 authorisation transfer onto one product code through
   `product_register.csv` at each dispensing's own date, and fold the replaced patient pseudonyms together
   through `person_key_crosswalk.csv`.
3. Map every package code to its Annex A product or Annex B marker treatment group, and take each
   patient's earliest dispensing in each as that patient's first receipt.
4. Apply section 2.3: a patient whose first receipt of a treatment falls in the clearance period
   (1 October 2023 to 30 September 2025) has no first receipt of it in the screen window.
5. For each of the 23 screened pairs, take the patients whose two first receipts both fall inside the
   window and not on the same day, and count those in whom the marker treatment came after the product and
   those in whom it came before. Keep the 20 pairs with at least 25 patients.
6. Apply section 3.2(b) by comparing each pair's after-count with 1.25 times half of its patients, since
   with no bearing either order is equally likely; check section 3.2(c) against
   `signal_tracker_export.csv`, and file the pairs that pass.

**Ends on:** 10 pairs referred, five of them pairs on Varenadol and Admirabin.
**Golden:** 7 pairs referred.

## Stump sentence

A competent solver reconciles the two layouts, folds the replaced pseudonyms, carries the reissued package
codes onto one product, establishes every first receipt against the clearance period, counts each pair's
after and before patients exactly and refers **10 pairs**; the step that lands it there is reading
"expected if receiving the product had no bearing" as half of the pair, when two of the nine products are
being withdrawn inside the window and two were first marketed inside it, so for those four the window
leaves the two orders nothing like equal room.

## Three rules

- **Task type:** `safety-signal-detection`, the task type in Pharmacology, Pharmacoepidemiology & Safety
  that serves Anomaly Detection: separating a real prescribing-sequence signal from what the register's own
  dispensing pattern over the window produces.
- **Domain test:** the deciding quantity is the number of a pair's patients expected to receive the marker
  treatment after the product if the product had no bearing on when the marker is first received, which is
  what prescription sequence symmetry analysis estimates and what pharmacoepidemiology takes from each
  medicine's own incident-use distribution across the window.
- **Swap:** "which carrier and repair-order pairs the control desk refers" is a count of repairs following
  deliveries; what breaks is that there is no within-person ordering of two first-ever exposures, no
  clearance period establishing a first exposure, and no incident-use distribution to take the expectation
  from, so nothing is left to estimate and the sort of the two counts is the whole answer.
- **Layer 1:** the agency's own pipeline produces all of it. The register's 2025 release renamed columns
  and changed the date format, so the clearance extract and the window extract have different layouts; one
  pharmacy chain's October batch was re-sent and its lines appear twice under fresh line identifiers; 420
  patients had their pseudonym replaced after a civil-registration correction and a crosswalk ships; every
  package code of one product was reissued when its marketing authorisation transferred in February 2026,
  and the register carries both code sets with valid-from and valid-to dates; the fee workbook quotes
  defined daily doses in thousands on one sheet and uses Danish decimal commas; the standard and the fee
  schedule are tables inside a PDF and a workbook. None of it is placed to be caught, and the referral set
  is identical whether or not any of it is repaired, asserted.
- **Layer 2:** `estimation_fit`. The methodological choice is the arithmetic that gives the filed
  counterfactual its value.
- **Decisive step:** take the expected number from the two sets of first-receipt dates the window holds,
  because a patient who first receives a product in the window's last weeks has almost no window left for
  the marker to follow and the whole window behind them for it to precede.
- **Not semantics:** every column, code, date, layout, pseudonym and package mapping read correctly still
  leaves a correct patient set, correct first receipts, correct after and before counts and a correct
  reading of section 3.2. Reading all of it right is exactly what produces the 10, which is the wrong
  answer's input, and the 20 candidate pairs and their 40 counts are the same under every rung.
- **Not rule application:** the standard files the window, the clearance period, the first-receipt rule,
  the pair's patients, the same-day exclusion, the order, the 25-patient minimum, the 1.25 multiple, the
  tracker check, the rounding and the referral quarter. No shipped sentence says how the expected number is
  obtained, and no shipped file holds it; a word sweep over every shipped file asserts that none of
  nineteen phrasings of symmetry, equal likelihood, a null ratio, an incidence distribution or a sequence
  ratio appears. A solver who executes every filed sentence exactly still has to construct that number, and
  the construction the clause invites is half of the pair.
- **Analyst test:** a strong analyst who reconciles both layouts, drops the re-sent batch, folds the
  replaced pseudonyms, carries the reissued codes onto one product at each dispensing's own date,
  establishes every first receipt against the clearance period and applies all three referral criteria
  exactly compares each after-count with 1.25 times half the pair and refers 10 pairs, the default path's
  `Ends on:`, where 7 are referred once the expected number is taken from the window's own dates.
- **Estimand:** sections 2.1 to 2.5, 3.1 and 3.2 of `screen_standard_7_2024.pdf`, quoted in the pack and
  tabulated under `## Estimand and the WHAT screen`: population, outcome, window, unit, comparison,
  minimum, multiple and rounding are all there, and the comparison is filed as a counterfactual whose value
  the standard does not give.
- **No decoy:** nothing is planted to be caught. No dispensings are copied to be found, no memo argues a
  list, no stakeholder figure carries a count, and no shipped file states a referral list, a sequence ratio
  or an expected number for this window or any other. The re-sent batch is one chain's ordinary resend and
  changes no referral.
- **No certified replay:** no referral list, confirmed-signal outcome or published screen result ships, so
  no method can be recovered by reproducing one. `signal_tracker_export.csv` holds only pairs the desk
  opened before the window, and no pair it names passes section 3.2(b) on either basis, asserted.
- **Lesson:** a within-person ordering is evidence only against the opportunity each order had, so when a
  medicine's own first receipts are piled against one end of the observation window, equal likelihood is
  not the null and the pairs it wrongly flags are exactly those on medicines leaving the market while the
  pairs it hides are those on medicines entering it. No build on file teaches it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the extract as it comes, half of the pair expected | section 3.2 files the multiple and the minimum | the two layouts stack on renamed columns in one line | yes, the first run anyone writes | none | the battery finds the resend, the reissued codes and the replaced pseudonyms | one group-by and a comparison | readable |
| 1 the hygiene battery done, half of the pair expected | no | no | yes, the hygiene reflex | none | yes, that is the battery | one filter | readable |
| 2 patients whose first product receipt falls within 60 days of either window edge dropped, half of the pair expected | no | the window's two dates are in the standard, so the guard is a row predicate once the solver has asked the question | yes, the edge-guard reflex for a window-bounded comparison | nothing scores a method; the tracker predates the window and ties under every rung | no | one filter on the product date | readable |
| 3 the expected number taken from the window's own first-receipt dates (decisive) | no sentence names symmetry, equal likelihood, a null ratio, an incidence distribution or a sequence ratio, asserted by a word sweep over every shipped file for nineteen phrasings | no column holds an expected number, and the first-receipt dates are a construction across two layouts, a crosswalk and a dated code register rather than a field | no reflex computes it: the 60-day edge guard refers twelve pairs and the extract as it comes refers nine, both measured on the shipped bundle | nothing scores a method; the tracker's pairs fail 3.2(b) on every basis | the battery repairs the extract and leaves the expectation at half | no: it is a double count over the pair's two date sets, or either drug's window incidence distribution | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | the screen window | 1 October 2025 to 30 September 2026 inclusive, on dispensing date | on the register's submission date, or the acceptance date | the pair counts change | section 2.1, quoted; asserted both ways |
| SF2 | a first receipt | the earliest dispensing of any package in that treatment's group recorded for the patient in the extract | the earliest in the window only, ignoring the clearance period | the candidate set changes | sections 2.2 and 2.3, quoted; asserted |
| SF3 | the clearance period | 1 October 2023 to 30 September 2025, and a first receipt falling in it means no first receipt in the window | a 12-month clearance, or none | the pair counts change | section 2.2, which states the 24 months; asserted |
| SF4 | a patient | one person after the replaced pseudonyms are folded through the crosswalk | the pseudonym as recorded, so a replaced patient counts twice | the pair counts change | `person_key_crosswalk.csv` with its replacement date, and section 2.4; asserted |
| SF5 | a product | the product code, with the reissued package codes carried onto one code at each dispensing's own date | the package code as dispensed, so the February transfer splits one product | one product's patients split in two | `product_register.csv`'s valid-from and valid-to dates, and section 2.4; asserted |
| SF6 | a marker treatment | the ATC group named in Annex B, so any package in the group counts | the single package code, or the whole ATC class above the group | the pair counts change | Annex B, which lists the group codes; `atc_group_index.csv`; asserted |
| SF7 | the pair's patients | patients whose two first receipts both fall in the window, same-day patients excluded | same-day patients counted as after, or as before | the pair counts change | section 2.5, quoted; asserted both ways |
| SF8 | a patient who died or left the country | counted if both first receipts fall on or before the recorded date | excluded from the pair | `same call`, asserted on the set and on every pair's two counts |
| SF9 | at least 25 patients | 25 or more of the pair's patients, after the same-day exclusion | 25 or more dispensings, or 25 or more in each order | the candidate set changes | section 3.2(a), quoted; asserted |
| SF10 | at least 1.25 times | at or above 1.25 times the expected number | strictly above | `same call`, asserted: no pair's ratio is 1.250 on any of the five arithmetics |
| SF11 | the expected number | the number expected if receiving the product had no bearing on when the marker treatment is first received, taken from the window's own first-receipt dates | half of the pair | the referral set changes, 7 against 10 | nothing: this is the method, not a term. `## Literal reader` gives the forcing, and all four window-aware arithmetics give the same seven pairs, asserted |
| SF12 | a pair already under assessment | a pair the tracker records as opened before the extract date | any pair the tracker names, including closed ones | `same call`, asserted: no pair the tracker names passes 3.2(b) on either basis |
| SF13 | rounding | counts whole, shares and days to one decimal, fees to the nearest krone | shares to two decimals | `same call`, asserted: no pair's share sits within 0.004 of a referral boundary on any basis |
| SF14 | the re-sent batch | one dispensing per pharmacy reference, so the resend collapses | every line counted | `same call` on the referral set, asserted; the ask figures move and that is graded there |
| SF15 | the two layouts' dates | ISO in the clearance extract, day-month-year in the window extract, both read as calendar dates | the window extract read as month-day-year | the pair counts change | `register_release_notes.json` states each layout's date format; asserted that the misread produces impossible dates in 61 per cent of rows |
| SF16 | the order of the output rows | the share receiving the marker after, longest first, as the asking sentence says | by product code | `same call`; the chart's ordering is graded and the asking sentence fixes it |
| SF17 | the referral quarter | the quarter beginning 1 January 2027, as section 4.1 states | the quarter the extract was pulled in | `same call`: the referral test reads the tracker at the extract date, asserted |

## Ladder

| Rung | The analysis | The referrals |
|---|---|---|
| 0 | the two extracts stacked with the package index joined on its open rows, the retired person keys left unfolded and the re-sent batch left in, the expected number half of the pair | **9**: Sovraxil and topical corticosteroid drops out, because the product's package codes were reissued at the February authorisation transfer and the retired rows carry its whole clearance period |
| 1 | the hygiene battery done, the expected number half of the pair | **10**: five pairs on Varenadol and Admirabin referred, Ternivast with gout treatment and Oxelumab with antidepressant passed over |
| 2 | patients whose first product receipt falls within 60 days of either window edge dropped, the expected number still half of the pair | **12**: it recovers both pairs the crude run hides and still refers all five pairs on the two products leaving the market |
| 3 | **answer:** the expected number taken from the window's own first-receipt dates | **7** |

**Separation.** The sets differ in membership, which is how the shape grades. Rung 1's ten and the
answer's seven share only five members: the easy route refers five pairs on the two products whose use is
ending inside the window (Varenadol with antiemetic, acid-suppressant and hypnotic; Admirabin with loop
diuretic and antidepressant) and passes over two real signals on the two products first marketed inside it
(Ternivast with gout treatment, Oxelumab with antidepressant). Rung 2's twelve differ from the answer in
five members. The five pairs the easy route adds sit at 1.53 to 1.73 times half the pair, clearly past
1.25, and at 0.99 to 1.02 times the expected number once that is taken from the dates, clearly short of
it; the two it misses sit at 1.02 and 1.13 against half the pair and at 1.39 and 1.34 against the expected
number. The lowest of the five shared referrals is 1.37 against the dates and 1.40 against half the pair,
so no shared pair is lost on either basis. The highest multiple among the thirteen pairs this run refuses
is 1.12, Dalvextin with acid-suppressant, the nearest pair on the wrong side of the line. The nearest
figure to the 1.25 multiple on any of the five arithmetics, over all 20 candidates, is 6.3 per cent away.

**The grid.** Two axes, the hygiene battery and the expected number:

| | half of the pair | from the window's own dates |
|---|---|---|
| the extract as it comes | 9 referred | 6 referred |
| hygiene battery done | 10 referred | **7 referred** |

Every cell is a named count. The decisive axis moves the same seven memberships in both rows, taking out
the five pairs on the two products leaving the market and adding the two on the products entering it, so a
solver who finds the window's arithmetic but not the reissued package codes names six of the seven and
none of the five: that is the fairness the ladder needs. The hygiene axis moves one pair in either column,
Sovraxil with topical corticosteroid, and every pair's two counts.

**Dominance.** The pair the ladder turns on hardest is Varenadol with hypnotic, whose share receiving the
marker after is 86.4 per cent, the highest on the screen, and whose multiple is 1.73 against half the pair
and 1.02 against the expected number: the loudest pair on the crude basis is the one the arithmetic
refuses most firmly, and no partial correction reaches it. The seven memberships the decisive step moves
sit on four different products, so no rule of thumb about a product's lifecycle substitutes for the
arithmetic: Sovraxil's use is also falling across the window and its pair is referred on both bases, while
two of Oxelumab's three pairs and two of Ternivast's three are refused on both.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which patients are in a pair | section 2.5 files it; 12,993 person keys in the extract, 20 of 23 pairs at or above the minimum, asserted |
| 2 | Unit of account | the patient, the dispensing, the package | section 2.5 files the patient, once per pair; asserted |
| 3 | Attribution window | which window a receipt falls in | dispensing date, section 2.1, quoted; the register holds no other date a receipt could be placed on |
| 4 | As-of dating | the extract at 20 October 2026 | `extract_manifest.csv` files the pull; the window closed twelve days before, asserted |
| 5 | Version basis | the package code's product at the February transfer | `product_register.csv`'s valid-from and valid-to read at the dispensing's own date; C1, asserted both ways |
| 6 | Denominator | what the after-count is compared with | **the decisive step. The comparison is filed as a counterfactual in section 3.2(b); its value is nowhere stated, asserted by word sweep, and is forced by the data, with all four window-aware arithmetics asserted to refer the same seven pairs** |
| 7 | Weighting | none: patients are counted, not weighted | stated in section 2.5 |
| 8 | Window length | twelve months, with a 24-month clearance period | sections 2.1 and 2.2; asserted that every referred pair's minimum is reached inside it |
| 9 | Boundary inclusivity | 1 October 2025 and 30 September 2026 | section 2.1 states both days included, quoted; the shipped sentence is the closure and `checks.py` asserts the standard carries it |
| 10 | Rounding path | counts whole, shares and days to one decimal, fees to the nearest krone | the asking sentence; no pair's multiple within 0.01 of 1.25 on any basis and no share within 0.4 points of its own referral boundary, asserted |
| 11 | Tie-break | the order of the output rows | the asking sentence orders by the share receiving the marker after; all 20 candidate shares are distinct to one decimal, asserted |
| 12 | Maturity and censoring | dispensings still arriving for the window | the manifest's note and the submission log: every window line was submitted before the pull, asserted; a line's submission date is never before its dispensing date, asserted over all 120,388 rows |
| 13 | Order of operations | clean then count, or count then clean | sections 2.3 and 2.4 file the conformance (one patient across a replaced key, the package read at the dispensing date, the earliest dispensing the first receipt), so the order is filed rather than open; the grid names the figure for each cell |
| 14 | Row order | the extract's order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the re-sent batch's lines | C1 on the call: both copies carry the same person key, package code, dispensing date and pharmacy, so any resolution leaves the first receipts alone and the referral set is identical with the resend kept, asserted. The manifest states that the extract holds one row per accepted transmission, which fixes the chain counts in the first ask |
| 16 | Identity normalisation | replaced pseudonyms, reissued package codes, ATC groups | the crosswalk, the register's validity dates and `atc_group_index.csv`; asserted that every code resolves to one treatment |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | patients, dispensing lines, packages, defined daily doses | the data dictionary names each; the call reads patients, asserted |
| 19 | Code and status semantics | the pharmacy, prescriber and acceptance codes | `register_release_notes.json` and the manifest; never the decisive step |
| 20 | Integerisation | the count of referrals is an integer by construction | stated |
| 21 | Clause scope | section 3.2 applies per pair | the section states it; asserted |
| 22 | Forward window contents | the assessments the desk will run from 1 January 2027 | section 4.1: the referrals are designated now from a closed window and worked in the coming quarter, so the call is forward facing |

## Literal reader

Executing the prompt and sections 2.1 to 2.5, 3.1, 3.2 and 4.1 word for word selects, for each of the 23
pairs in Annexes A and B, the patients whose first receipt of the product and whose first receipt of the
marker treatment both fall between 1 October 2025 and 30 September 2026 and not on the same day, with a
first receipt in the 24 months before that window disqualifying the patient; it records for each of them
whether the marker treatment came after the product or before it; it keeps the 20 pairs with at least 25
patients; and it asks for the pairs whose after-count is at least 1.25 times the number that would be
expected if receiving the product had no bearing on when the marker treatment is first received, excluding
pairs the tracker already has open. Every term and convention in that sentence has an SF row ruled out by a
quoted sentence or asserted to give the same seven pairs. What the text does not fix, and nowhere mentions,
is how that expected number is obtained: that is the measure's own arithmetic. No shipped sentence says
"equally likely", "symmetry", "half", "sequence ratio", "null ratio" or "incidence distribution", asserted
by a word sweep over every shipped file for nineteen phrasings, so the easy answer is the arithmetic the
clause invites rather than a reading of a filed word.

The data forces it. Varenadol's authorisation lapses on 18 April 2026 and Admirabin's on 7 July 2026, and
99.3 and 89.1 per cent of their patients' first receipts of them fall in the window's first half;
Ternivast was first marketed on 7 February 2026 and Oxelumab on 15 October 2025, and 94.1 and 76.7 per
cent of their patients' first receipts fall in the window's second half. Taking either order as equally
likely asserts of Varenadol's patients that a marker treatment was as likely to follow a product they
started in October 2025 as to precede it, which the window's own arithmetic forbids. All four arithmetics
that read the dates refer the same seven pairs: the exchangeability expectation inside the pair, the two
drugs' window-wide incident-use distributions, the pair's product dates against the marker's window-wide
distribution, and the pair's product dates against a marker spread evenly across the window, each asserted
on the set and on every pair's referral in `checks.py` and again in `verify.py`. The crude ten is not a
subset of the seven and the seven is not a subset of the ten, so no licensed reading connects them: the
easy answer is an easy arithmetic on the same literal estimand.

## Oracles

- `signal_tracker_export.csv` records the pairs the signal desk opened and closed before the extract date,
  with dates and status. It names no pair that passes section 3.2(b) on any of the five arithmetics and
  states no result for this window, so it ties under every rung, asserted.
- `extract_manifest.csv` states each file's rows, date range and layout version, and settles the ask
  layer's one designed disagreement (the exceptions file's scope) without naming a level.
- `pharmacy_submission_log.csv` gives each chain's submitted and accepted line counts by month. It
  reconciles to the extract once the rejected lines are added and ties under every rung of the main call,
  asserted.
- `spontaneous_reports_summary.csv` and `literature_screening_log.csv` are the declared distractors: the
  agency's other two signal sources for the same quarter. Neither holds a marker treatment, a patient
  pseudonym or a pair, so neither ranks the candidates on the decision question, asserted by column name.
- No shipped file states a referral list, an expected number, a sequence ratio or a count of referrals for
  any window. There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per pharmacy chain and quarter of the window, the dispensing lines the register accepted, the lines it rejected and the median days from dispensing to submission | 3 per chain-quarter, 4 chains by 4 quarters | the audit trail from an input the call consumes, through lines it never reads, to the chain's own control total | the register's own quarterly ingest review | D4 absence as the signal: the rejected lines sit in `submission_exceptions.csv`, which no habitual join reaches, and never enter either extract | D6 the exceptions file is per line while the chain log is per chain-month; D8 the submission stamp is the chain's own clock and the acceptance date the register's business date | both extracts, the exceptions file, the submission log, the manifest, the release notes, the standard, the product register; 12 columns | 4 stops, lazy delta 11 of 16 chain-quarters | an ingest pipeline's own quarterly review |
| A2 per marketing authorisation holder, the defined daily doses of its Annex A products dispensed inside the window and the statutory data fee due | 2 per holder, 6 holders | an input reconciled to another system's total, the gap made of devices | the finance office settles the holders' statutory fees | D2 version: the fee schedule was amended with effect from 1 April 2026 and the amended rate applies to the window's later half, which the superseded sheet does not carry | D3 one sheet quotes defined daily doses in thousands and uses Danish decimal commas; D7 one holder files under two codes after a merger dated inside the window | the fee workbook and its amendment sheet, the holder register, the product register, both extracts, the manifest; 13 columns | 5 stops, lazy delta 4 of 6 holders | the finance office's quarterly settlement |
| A3 per region and age band at the window's start, the patients with a first receipt of an Annex A product inside the window and the share of them who also had a first receipt of an Annex B marker treatment inside it | 2 per cell, 5 regions by 4 bands | the decisive construction's output on the segment the agency publishes anyway | the agency's standing quarterly utilisation table | the construction layer: a wrong patient unit, an unmapped reissued package code or a clearance period read at 12 months fails every cell | D4 region blank for patients registered outside Denmark, whose meaning the person register's own notes state; D5 patients who died or emigrated inside the window | the person register, both extracts, the crosswalk, the product register, the ATC index, the standard, the manifest; 11 columns | 4 stops, lazy delta 14 of 20 cells | the agency's own quarterly table |

**The main population's zero counts.** Zero device rows and zero hazard rows in the patients and pairs the
call rests on: A1's device sits in the exceptions file, which carries no accepted dispensing; A2's sit in
the fee workbook, its amendment sheet and the holder register, none of which carries a patient; A3 reads
the person register's demographic columns, which the main call never reads. Deleting every device leaves
the seven and the ten exactly as they are, asserted.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D6 grain | A1, A2 | A1 three chain-quarters, A2 two holders |
| D8 clocks | A1 | A1 the accepted count in 14 of 16 chain-quarters, by 6 to 43 lines |
| D4 absence | A1, A3 | A1 the rejected count in all 16 chain-quarters, A3 the four "not stated" cells |
| D5 scope | A3 | A3 the patient counts in the cells holding the 266 patients who changed region |

**The referee.** `extract_manifest.csv` states each file's rows, date range and layout version and settles
the one designed disagreement, the exceptions file's scope, without naming a level.

**The cracker sheet.** The cracker referred the seven, ran the hygiene battery (key uniqueness, exact
duplicates, unmatched joins, fan-out, count ties), executed every filed rule it points at and matched every
control total.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 lines the register rejected, all 16 chain-quarters | both extracts, which hold only accepted lines | 0 | 42 to 162 | miss |
| A1 lines the register accepted, 14 of 16 chain-quarters | the chains' own monthly log, which counts by month of submission | 6 to 43 lines out per cell | 1,495 to 5,795 | miss |
| A2 data fee due, all six payers | the schedule sheet, whose rates the amendment of 1 April 2026 replaced for later doses | 2,182 to 18,719 kroner low | 155,320 to 441,906 | miss |
| A2 data fee due, every payer's band | the band thresholds read as doses rather than thousands of doses | the lowest rate, 860 against 1,480 | as above | miss |
| A3 patients and share, all four "not stated" cells | the region column as recorded, so the blanks leave the table | the four cells absent | 35 to 63 patients, 68.6 to 87.3 per cent | miss |
| A3 patients, the cells holding the 266 patients who changed region inside the window | the region recorded at the pull, not at the window's start | two to five patients out per cell | as published | miss |

**Pair ceiling:** 39.4
**Mirror leakage:** 18.5

The pair arithmetic: the cracker lands the call and keeps about a fifth of the ask weight (Lc 0.21), the
mirror stops at rung 2's twelve pairs and keeps 0.185 of it, and a wrong call keeps about 5 of the
recommendation weight, so C is 38 + 7 + 55 x 0.21 = 56.6 and S is 5 + 7 + 55 x 0.185 = 22.2.

## Tried and rejected

- The seed's own architecture, a channel attribute that explains every alarm on the channel: the answer
  flips on reading one field, which the client's rules ban as the decisive step. Re-rooted at the draw.
- Masking confined to one reaction, with one dominant product flooding a single preferred term: the
  decisive step would move one pair, which no ladder can carry, and a solver who missed it would be wrong
  by one. Replaced by a campaign quarter, where the dominant product's whole profile sets the background for
  four reactions at once.
- Forcing the comparison set with a filed criterion in general terms, that the measure must not move when
  reporting for unrelated products moves: it makes the solver ask the decisive question, which the
  readability screen fails on test 1. Replaced by forcing through the data, with every masking-aware
  comparison set asserted to give the same 15.
- A register of the previous quarters' confirmed signals, to force the comparison set by showing which run
  caught them: a corpus that refutes the naive read makes the decisive rung readable, and it is a
  calibration organ the card does not carry. Dropped; the closed register ships with pairs that predate the
  window and ties under every rung.
- Letting the desk's capacity bind, so the call is the top 15 of 16 qualifying pairs by report count: the
  cap adds a filed ordering rule on top of the decisive step and puts two pairs on a boundary the judge
  would have to adjudicate. The capacity is left at 16 against 15 taken, which is what makes the easy
  answer's five idle slots a visible consequence.
- Architecture 2, first draw: shrinking each pair's reporting ratio toward the database's own distribution,
  the empirical-Bayes answer to sparse cells. Dropped at the draw: selection on a noisy estimate is
  task191's extreme-value reach and task194's regression to the mean, both in the last twelve, and the
  shrunk estimator is not forced by the data against the raw one.
- Architecture 2, second draw: a self-controlled comparison against a cohort comparison, to beat
  channelling. Dropped at the draw: task180 v3 is that exact pharmacovigilance architecture, spent, and the
  choice is which rows the measure is taken against, the shape this slot already died on.
- Architecture 2, third draw: the time-to-onset distribution's Weibull shape with the reports
  right-truncated by their own receipt. Dropped at the draw: whether the unobserved long onsets are in the
  population is the population part of the estimand, the WHAT screen's first failure mode, and task184 and
  task189 already hold interval-censored event times and left-censored measurements in this lane.
- A 24-month screen window with the asymmetry carried by trends in the marker treatments' own incident use:
  measured, and a 180-day sequence-interval restriction with the crude expectation reached the golden set
  exactly, so the sophisticated reflex spent the stump. Replaced by a 12-month window, where every interval
  a solver would choose is at least half the window and symmetrises nothing: measured over interval
  restrictions at 60, 90, 120, 180, 270 and 365 days, edge guards at 30, 60 and 90 days, the per-product
  marketing window, two compounds of those and the window's first half, and none of the fourteen reaches
  the seven.
- Carrying the asymmetry with trends in the marker treatments rather than the products: measured, and the
  arithmetic that spreads the marker evenly over the window then disagreed with the other three on two
  pairs, which is a fork on the main call. Replaced by level marker groups and product lifecycles, where all
  four window-aware arithmetics refer the same seven pairs.
- Grading the expected number itself per pair: it is method-dependent at one decimal across the four
  arithmetics, so a judge recomputing it would find a figure that does not reproduce. The graded figures are
  the pair's patients, its after-count and its referral, each determinate under the filed population, and
  the expected number appears in no graded block.
- Carrying the package reissue on a product whose pairs sit near the referral line: measured at the build,
  and joining the package index on its open rows alone then moved the call, which makes the hygiene battery
  worth the call rather than the figures. Moved to Sovraxil, whose pair is referred on both bases by a wide
  margin, so the join error costs one membership in either column of the grid and the decisive axis still
  moves the same seven in both rows.
- Reading the third ask's share as the earliest marker receipt across all eight marker groups: measured at
  the build, and the earliest is in the clearance period for almost every patient, so nineteen of the
  twenty-four cells sat between 2 and 7 per cent and three were zero. The standard's section 4.2 now states
  the table as at least one Annex B marker treatment first received inside the window, which is the reading
  the asking sentence carries, and the cells run from 68.6 to 87.3 per cent.
- A submission lag that let the slowest chain's September lines arrive after the extract was pulled: three
  days of lines sat outside the extract's own as-of date. The pull moved to 20 October 2026, which is after
  every line in the pack, asserted over all 120,388 rows.

## Architecture 1, spent at stage 4 on the judge's SEND_BACK

**The verdict.** NOT_DETERMINISTIC, `underspecified_objective`, disposition SEND_BACK. Gate G passes
(`method_or_model_selection`, `analytical_non_defect`, no surface-read dependency, no sole data
defect) and Gate H passes on all three rules, with the decisive step read as analytical: the choice
of comparison group under masking. Every golden figure reproduced from the shipped files, the 15
pairs with their ratios and chi-squares among them. The call is what failed: paragraph 3.1 names the
measure and no shipped text says what it is taken against, so the proportional reporting ratio
against all other reports, which is the textbook default, gives 11 and the golden's 15 appears only
when the booster is out of the comparison. The leak reader, reading the same pack cold, landed the
same 11 at moderate to high confidence and named the comparator as the one choice the documents left
to it.

**Why this is structural and not a missing sentence.** The judge's own fix is to file the comparison
population in the standard, and that is right: `determinism-check` section 1 counts the comparison
inside the estimand, the WHAT, which must be filed so that its literal execution is the golden. This
build put the decisive step in the comparison population, so it put the stump in the WHAT. File it
either way and the computation follows from the clause, which is rule application; leave it unfiled
and the call is not determinate. There is no third position, and no hardening reaches one: a general
criterion on the measure ("the expectation must not turn on the volume of any one product") makes the
exclusion an executed rule, and a record of past runs that shows which comparator caught the
confirmed signals is a corpus that refutes the naive read, which the readability screen fails on
test 4.

**The lesson, which is wider than this build.** Three architectures in this wave have now died the
same death: task190's population had to say whether members not yet observed are in it, task192's
decisive count had no parameter-free definition, and this one's comparison population is part of the
estimand. In each the decisive step sat in the WHAT. The next draw puts the estimand wholly beyond
argument, every term and population filed, and leaves two or more methods standing on it, with the
data's own structure ruling out the easy one. `method_or_model_selection` on a filed estimand, not
`estimand_identification`.

**Worth keeping from the build.** The world and the ask layer are sound and the pack is realistic
enough to reuse under another decisive step. Three defects the judge and the reader found in it are
recorded so a re-root does not repeat them:
- `dictionary_version` in the extract was set from the receipt date while paragraph 2.3 reads the
  version in force when the case was coded, so 1,388 rows disagree and the serious share forks.
- 501 licence-holder submissions carry a coded date one to four days before the receipt date, so the
  mean days to coding forks three ways (raw, clipped at zero, negatives dropped).
- The agreement schedule does not say whether the quarter's fee covers submissions received after
  the quarter closed, so the holder fees fork by about 7,300 kroner.

**How architecture 2 designs the three out.** Every package code's product is read at the dispensing's own
date and `checks.py` asserts that each dispensing date falls inside exactly one validity interval for its
package code, so no attribute is stamped from the wrong date. Every date order is asserted monotone: a
line's submission date is on or after its dispensing date for all lines, a patient's death or emigration
date is on or after their last dispensing, and a package's first dispensing is on or after its own
valid-from date. The fee schedule states in its own text how lines submitted after the quarter closed are
treated, and the amendment sheet states its effective date and which lines it governs, so no ask figure
forks on a rule the pack does not state.

## Leak sweep answered

`leak.py --asof 2026-10-20` is REVIEW with three lines and no LEAK. Each one, and why it is harmless:

- **Sweep 3, the figure 1.25 in `screen_standard_7_2024.pdf`.** It is the referral multiple section 3.2(b)
  files, which the standard has to state for the run to exist, and it is not a figure the analysis derives:
  no pair's own multiple, patient count or referral appears anywhere in the pack.
- **Sweep 3, 25 of 27 distinctive words of the committed call in the standard.** The call is written in the
  standard's own vocabulary (refer, pair, formal signal assessment, the quarter beginning 1 January 2027)
  because the standard is the document that names those things. It states no pair, no count and no figure
  for this run or any other.
- **Sweep 4, eight of 25 stump-paragraph terms in the standard** (expected, standard, inside, package,
  patient, clearance). They are the words a prescription-screen standard is made of. The document never
  says how the expected number is obtained, and a word sweep over all nineteen shipped files asserts that
  none of nineteen phrasings of symmetry, equal likelihood, a null ratio, a sequence ratio or an
  incidence distribution appears.
- **Sweep 6, `holder_register.csv` naming six of six answer-set candidates.** The names the sweep matched
  are marketing authorisation holders, not pairs. The file carries no marker treatment, no patient and no
  figure about any pair's reporting, asserted by column name.

## Pre-ship check

The pack as built, read against the gates one last time.

- **Free gates.** 103 generator assertions, 248 independent checks in `verify.py` (it reads only `target/`
  and `figures.json`), `precut.py` 49 checks 0 FAIL 0 WARN, `figures_check.py` 204 of 204,
  `voice-check.py` exit 0 at 999 characters, `leak.py` REVIEW with three answered lines and no LEAK,
  `guard.py heart` WARN with every line answered in `## Draw`, `guard.py surface` promoting no file name
  and no persona. Two rebuilds byte-identical, `target.zip` cut from the final rebuild, 19 entries.
- **Input gates.** 19 files, 4 formats (csv, pdf, xlsx, json), two files above 25,000 rows
  (`dispensings_2023_2025.csv` at 73,639 and `dispensings_2025_2026.csv` at 46,749), two distractors named
  in `metadata.json` and in no file name.
- **The three rules against the built pack.** R1: the pack ships patient-level dispensing lines with their
  dates and no shipped column holds an expected number, a multiple or a referral, asserted over every csv
  header. R2: the referral set is identical with the retired person keys unfolded, with the package index
  joined without its date condition and with the re-sent batch left in, each asserted. R3a: the easy route
  on the clean truth, every filed rule applied, refers 10 pairs. R3b: changing only the expected number
  refers 7, and all four window-aware arithmetics give that same 7. R3c: nothing is planted, and a word
  sweep over all nineteen files finds none of nineteen phrasings of the decisive move.
- **Gate G.** No shipped artifact ranks the pairs on the decision question and `metadata.json` declares no
  wrong-basis distractor. The tracker names two pairs as under assessment and neither passes 3.2(b) on any
  of the five arithmetics; the two distractors carry no marker treatment, no patient key and no pair.
  Delete every wrong number in the pack and the call still turns on how the expected number is obtained.
