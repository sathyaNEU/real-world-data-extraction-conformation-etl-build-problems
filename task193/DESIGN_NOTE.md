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
  pharmacy chain's October batch was re-sent, so 1,477 lines appear twice under fresh record identifiers
  while the register's own note says a re-sent line is one dispensing; 420
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
| 2 patients whose first product receipt falls within 60 days of either window edge dropped, half of the pair expected | no | the window's two dates are in the standard, so the guard is a row predicate once the solver has asked the question | yes, the edge-guard reflex for a window-bounded comparison | nothing scores a method; every pair the tracker holds open fails 3.2(b) on every basis, so it ties under every rung | no | one filter on the product date | readable |
| 3 the expected number taken from the window's own first-receipt dates (decisive) | no sentence names symmetry, equal likelihood, a null ratio, an incidence distribution or a sequence ratio, asserted by a word sweep over every shipped file for nineteen phrasings | no column holds an expected number, and the first-receipt dates are a construction across two layouts, a crosswalk and a dated code register rather than a field | no reflex computes it: the 60-day edge guard refers eleven pairs and the extract as it comes refers nine, both measured on the shipped bundle | nothing scores a method; the tracker's pairs fail 3.2(b) on every basis | the battery repairs the extract and leaves the expectation at half | no: it is a double count over the pair's two date sets, or either drug's window incidence distribution | silent |

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
| SF8 | a patient who died or left the country | the register records the dates and the standard says nothing of them, because no dispensing falls after any such date | excluded from the pair | `same call`, asserted on the set and on every pair's two counts: both readings select the same patients |
| SF9 | at least 25 patients | 25 or more of the pair's patients, after the same-day exclusion | 25 or more dispensings, or 25 or more in each order | the candidate set changes | section 3.2(a), quoted; asserted |
| SF10 | at least 1.25 times | at or above 1.25 times the expected number | strictly above | `same call`, asserted: no pair's ratio is 1.250 on any of the five arithmetics |
| SF11 | the expected number | the number expected if receiving the product had no bearing on when the marker treatment is first received, taken from the window's own first-receipt dates | half of the pair | the referral set changes, 7 against 10 | nothing: this is the method, not a term. `## Literal reader` gives the forcing, and all four window-aware arithmetics give the same seven pairs, asserted |
| SF12 | a pair already under assessment | a pair the tracker records as opened before the extract date | any pair the tracker names, including closed ones | `same call`, asserted: no pair the tracker names passes 3.2(b) on either basis |
| SF13 | rounding | counts whole, shares and days to one decimal, fees to the nearest krone | shares to two decimals | `same call`, asserted: no pair's share sits within 0.004 of a referral boundary on any basis, and every graded figure sits mid bin (see `## Mid-bin figures`) |
| SF14 | the re-sent batch | one dispensing, as `register_release_notes.json` states: a line re-sent after a transmission failure counts once in any count of lines and once in any count of doses | every transmission counted | `same call` on the referral set, asserted; the ask figures are fixed by that quoted note and asserted both ways |
| SF15 | the two layouts' dates | ISO in the clearance extract, day-month-year in the window extract, both read as calendar dates | the window extract read as month-day-year | the pair counts change | `register_release_notes.json` states each layout's date format; asserted that the misread produces impossible dates in 61 per cent of rows |
| SF16 | the order of the output rows | the share receiving the marker after, longest first, as the asking sentence says | by product code | `same call`; the chart's ordering is graded and the asking sentence fixes it |
| SF17 | the referral quarter | the quarter beginning 1 January 2027, as section 4.1 states | the quarter the extract was pulled in | `same call`: the referral test reads the tracker at the extract date, asserted |
| SF18 | the fee's unit of account | the holder that pays the fee for a dispensing, which the asking sentence names as the unit | the marketing authorisation holder of record at the extract date, so the transfer and the merger are not followed | the ask's figures change, 7 payers against 6, and two payers' doses swap | the asking sentence names the payer as the unit; the workbook's Notes sheet states who pays before and after a merger and the product register carries the transfer date. The figures are graded and asserted |
| SF19 | how many bars the chart carries | one for each of the 23 screened pairs, as the asking sentence says | the 20 candidates only | the chart's row set changes | the asking sentence states all 23, and every pair including the three below the patient minimum carries a share; asserted |
| SF20 | the chart's referral line | not drawn: its position is 1.25 times a pair's expected share, which depends on the construction the standard leaves open | drawn at each pair's expected share times 1.25 | no graded element moves, because the marker is not a graded element | the asking sentence asks only for the referred pairs in the darker fill; asserted that no threshold is drawn |

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
(Ternivast with gout treatment, Oxelumab with antidepressant). Rung 2's eleven differ from the answer in
six members. The five pairs the easy route adds sit at 1.51 to 1.63 times half the pair, clearly past
1.25, and at 0.98 to 1.02 times the expected number once that is taken from the dates, clearly short of
it; the two it misses sit at 0.98 and 1.10 against half the pair and at 1.37 and 1.36 against the expected
number. The lowest of the five shared referrals is 1.40 against the dates and 1.44 against half the pair,
so no shared pair is lost on either basis. The highest multiple among the thirteen pairs this run refuses
is 1.03, Dalvextin with acid-suppressant, the nearest pair on the wrong side of the line. The nearest
figure to the 1.25 multiple on any of the five arithmetics, over all 20 candidates, is 8.5 per cent away.

**The grid.** Two axes, the hygiene battery and the expected number:

| | half of the pair | from the window's own dates |
|---|---|---|
| the extract as it comes | 9 referred | 7 referred |
| hygiene battery done | 10 referred | **7 referred** |

Every cell is a named count. The decisive axis moves the same seven memberships in both rows, taking out
the five pairs on the two products leaving the market and adding the two on the products entering it, so a
solver who finds the window's arithmetic but not the reissued package codes still names the seven: the
hygiene battery is Layer 1 and never carries the call. What it does carry is every pair's two counts and
its share, each of them graded, and one membership in the crude column, Sovraxil with topical
corticosteroid, which is why the crude row reads 9 and then 10.

**Dominance.** The pair the ladder turns on hardest is Varenadol with antiemetic, whose share receiving the
marker after is 81.4 per cent, the highest on the screen, and whose multiple is 1.63 against half the pair
and 0.99 against the expected number: the loudest pair on the crude basis is the one the arithmetic
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
| 15 | Duplicate resolution | the re-sent batch's lines | C1 on the call: both copies carry the same person key, package code, dispensing date and pharmacy, so any resolution leaves the first receipts alone and the referral set is identical with the resend kept, asserted. `register_release_notes.json` states that a re-sent line counts once in any count of lines and once in any count of doses, which fixes both ask layers |
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
- `pharmacy_submission_log.csv` gives each chain's submitted, accepted, turned-back and withdrawn line
  counts by month of submission. It is the chains' own count, not the register's, so it does not
  reconcile to the extract line for line, and it ties under every rung of the main call.
- `spontaneous_reports_summary.csv` and `literature_screening_log.csv` are the declared distractors: the
  agency's other two signal sources for the same quarter. Neither holds a marker treatment, a patient
  pseudonym or a pair, so neither ranks the candidates on the decision question, asserted by column name.
- **The reports file is held to a tie, not merely to silence.** A distractor whose counts happen to agree
  with the right answer and not with the easy one is an oracle even with no marker column, because the
  two constructions disagree about exactly four products: Ternivast and Oxelumab entering the market, and
  Varenadol and Admirabin leaving it. On a first cut this file failed that test badly, because the
  realistic pattern it carried, a newly marketed product under additional monitoring being reported on
  far more, put Ternivast and Oxelumab at the top of every reading by a factor of two to five, which is
  the whole difference between the seven and the ten. It now carries a reporting rate driven by how
  visible the reaction is rather than by how new the product is, and the generator asserts, on each of
  the reports received, the serious reports, the reports from patients and the reports per thousand
  window dispensings, that all four of those products sit strictly inside the range the other five span
  and that no cut of the ordering isolates the two entering, the two leaving, or the four together.
  Eight assertions, one per reading per claim.
- No shipped file states a referral list, an expected number, a sequence ratio or a count of referrals for
  any window. There is no calibration organ.

## Mid-bin figures

Every graded figure sits away from the boundary that would make its rounding a convention, and the
distance is a number the generator asserts rather than a hope.

| Figure | Rounding | Construction | Measured distance | What would flip it |
|---|---|---|---|---|
| a payer's defined daily doses | one decimal | every screened product's strengths are whole or half doses per unit, so a package holds a whole number of tenths of a dose and a payer's window total is exact at one decimal | 0.05 of a tenth, the maximum: the figure needs no rounding at all | nothing: there is no fractional part to round |
| a payer's data fee | nearest krone | the rates in the executive order were chosen against the realised dose totals, measured as the distance to the half krone that decides the rounding | 0.432 krone at the tightest of the seven, so the exact figure is within a tenth of a whole krone, and half-up and half-even agree for all seven | one more half-dose package on that payer, worth 0.56 krone |
| a region and age cell's share | one decimal | the reporting bands were chosen on two criteria at once, every cell mid bin and the cracker's natural reading missing every cell | 0.0127 of a point at the tightest of the 24, against 0.00011 in the judged pass | one patient either way in that cell, which no filed reading of the population produces |
| a chain-quarter's median days | one decimal | every even cell's two middle values are equal | exact: every median convention gives the same figure | nothing |
| a pair's referral multiple | two decimals against 1.25 | the effects and the product lifecycles | 8.5 per cent of the multiple over 20 candidates by 5 arithmetics | a sixth arithmetic 8.5 per cent away from all four window-aware ones |
| the chart's bar order | one decimal on the share | all 23 pairs carry a share | 0.1 of a point between the closest two bars | a share tie, which the generator refuses |

The arithmetic runs in integers where it can: the doses accumulate in tenths as whole numbers and the
fee is struck with exact decimals and an explicit half-up, in the golden and in the independent
verifier alike, so no figure carries a floating-point residue. The verifier reads the rates out of the
shipped workbook rather than holding its own copy.

**What is deliberately not a graded element.** The chart carries no referral-line marker. Its position
is 1.25 times a pair's expected share, and the expected share is the one thing the standard leaves to
the division's own epidemiology, so the marker's position is the stump wearing a ruler. Dropping it
costs nothing the ask was buying: the referred pairs are still read off the chart, in the darker fill,
and the bar order is graded bar by bar.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per pharmacy chain and quarter of the window, the dispensing lines the register accepted, the lines it rejected and the median days from dispensing to submission | 3 per chain-quarter, 4 chains by 4 quarters | the audit trail from an input the call consumes, through lines it never reads, to the chain's own control total | the register's own quarterly ingest review | D4 absence as the signal: the rejected lines sit in `submission_exceptions.csv`, which no habitual join reaches, and never enter either extract | D6 the chains' log counts by month of submission while the register reports a line in the quarter of its dispensing, which the release notes state; D1 the re-sent lines, one dispensing by that same note | both extracts, the exceptions file, the submission log, the pharmacy register, the manifest, the release notes, the standard; 12 columns | 4 stops, lazy delta 12 of 16 chain-quarters | an ingest pipeline's own quarterly review |
| A2 per holder that pays the fee for a dispensing, the defined daily doses of its Annex A products dispensed inside the window and the statutory data fee due | 2 per payer, 7 payers | an input reconciled to another system's total, the gap made of devices | the finance office settles the holders' statutory fees | D2 version: the fee schedule was amended with effect from 1 April 2026 and the amended rate applies to the window's later half, which the superseded sheet does not carry | D3 the schedule's bands are in thousands of defined daily doses while the extract gives doses; D7 one product's authorisation transfers to another holder inside the window and one holder merges into another, so a payer is read at the dispensing's own date; D1 the re-sent lines, which the register's note says are one dispensing | the fee workbook's three sheets, the holder register, the product register's holder columns, the package index, both extracts, the release notes, the manifest; 15 columns | 5 stops, lazy delta 6 of 7 payers | the finance office's quarterly settlement |
| A3 per region and age band at the window's start, the patients with a first receipt of an Annex A product inside the window and the share of them who also had a first receipt of an Annex B marker treatment inside it | 2 per cell, 6 regions including not stated by 4 bands | the decisive construction's output on the segment the agency publishes anyway | the agency's standing quarterly utilisation table | the construction layer: a wrong patient unit, an unmapped reissued package code or a clearance period read at 12 months fails every cell | D4 region blank for patients registered outside Denmark, whose meaning the person register's own notes state; D5 patients who died or emigrated inside the window | the person register, both extracts, the crosswalk, the product register, the ATC index, the standard, the manifest; 11 columns | 4 stops, lazy delta 14 of 20 cells | the agency's own quarterly table |

**The main population's zero counts.** Zero device rows and zero hazard rows in the patients and pairs the
call rests on: A1's device sits in the exceptions file, which carries no accepted dispensing; A2's sit in
the fee workbook, its amendment sheet and the holder register, none of which carries a patient; A3 reads
the person register's demographic columns, which the main call never reads. Deleting every device leaves
the seven and the ten exactly as they are, asserted.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D6 grain | A1, A2 | A1 every chain-quarter when the chains' log is used instead of the extracts, which is also the file that does not reconcile to the extract line for line, A2 the band of every payer when thousands are read as doses |
| D1 duplication | A1, A2 | A1 the accepted count for the two chains that re-sent a transmission, A2 the doses of every payer whose products those chains dispensed |
| D4 absence | A1, A3 | A1 the rejected count in all 16 chain-quarters, A3 the four "not stated" cells |
| D7 keys | A2 | A2 one payer's whole dose total when the authorisation transfer or the merger is read at the wrong date |
| D5 scope | A3 | A3 the patient counts in the cells holding the patients who changed region inside the window |

**The referee.** `extract_manifest.csv` states each file's rows, date range and layout version and settles
the one designed disagreement, the exceptions file's scope, without naming a level.

**The cracker sheet, measured.** `generator/cracker.py` writes the cracker's path as code and the
build runs it on the cut pack, so the figures below are output and not prose. It reads `target/`
only, down to taking the reporting bands out of the shipped PDF. It stacks both layouts on the
release notes' column map, counts a re-sent line once, folds the retired pseudonyms, joins the
package index at the date of the dispensing, and then executes every filed sentence the asking
sentences point at, taking the natural reading only where nothing in the pack adjudicates one.
Every figure is scored against the golden within half a unit of the stated rounding.

| Ask | Figures | Cracker keeps | What it misses on | Result |
|---|---|---|---|---|
| A1 chain and quarter: accepted, rejected, median days | 48 | 3 | the chain that owned the pharmacy on the day of the dispensing | miss |
| A2 payer: doses and fee | 14 | 8 | the dose the edition in force assigns, against the figure the package row was written with | miss |
| A3 region and age band: patients and share | 48 | 0 | the region the October 2025 delivery holds, which the current extract's history columns cannot reconstruct | miss |

**Pair ceiling:** 34.0
**Mirror leakage:** 10.0
**Measured by:** `generator/cracker.py`, run on the cut pack by `checks.py` at every build

The asks are decoupled from the call, so the mirror walks the cracker's ask path: Ls equals Lc at
0.100. C is 38 + 7 + 55 x 0.100 = 50.5 and S is 5 + 7 + 55 x 0.100 = 17.5, so the pair ceiling is
34.0 against a ceiling of 40 and the leakage is 10.0 against 35. A2 is the weakest ask at 8 of its
14 figures kept.

**The three silent primaries, and what each is worth.** Each sits under a pin that stays, and none
of them is adjudicated by any filed sentence. Running the cracker again with one of them found
measures what it carries:

| Primary | Family | The pin it sits under | What finds it | Ask weight then kept | Ceiling |
|---|---|---|---|---|---|
| the chain that owned the pharmacy on the day | D7 keys, an as-of join | the asking sentence's quarter of dispensing, standard 2.1 and the dictionary | the chains' own monthly log of what the register accepted: it ties to the extract in all 148 chain-months when a line is read against the chain that owned its pharmacy that day, and fails in 144 of them, by 56,626 lines, when it is read against the chain the register gives now | 50.9 per cent | 56.5 |
| the dose the edition in force assigns | D2 version | the fee workbook's bands, its amendment and its payer rule | the stored figure contradicts the formula its own column description gives, on nine package rows across three codes and nowhere else, beyond the rounding it is stated at; one edition of the index is in force across the whole fee period, so no vintage explains it | 15.5 per cent | 37.0 |
| the region the October 2025 delivery holds | D2 version | standard 4.2's region vintage | the current extract has kept a previous region only since 1 April 2026, which its documentation states and no row contradicts, so a blank is not evidence of no change; the two deliveries then disagree for patients the current extract records nothing against, and it cannot reconstruct the earlier state | 53.6 per cent | 58.0 |
| all three found | - | - | 100 per cent | 83.5 |

The last row is the fairness proof: one handling reproduces the golden exactly, and it is the only
one that does.

**Why each is silent.** None is found by the hygiene battery. Every line joins the pharmacy register
and every key joins both person extracts, so there is no unmatched join; the package index's keys
are unique and its rows are not duplicates; the counts tie wherever the register publishes a
control. The chain transaction shows up only when the chains' own monthly totals are set against
the extract, which the dictionary warns does not reconcile line for line anyway. The stale dose
shows up only when a derived column is recomputed from its own inputs across two files. The silent
region correction shows up only when two deliveries of the same extract are set side by side.

**Why none of them is marked.** `previous_chain_code` and `in_chain_from` are populated for every
pharmacy that ever changed hands, and most of those transfers are years older than the extract, so
the column does not isolate the four transactions that matter. `atc_text.csv` carries a dose for
every code, not only the revised ones. The two person deliveries disagree for the recorded movers
as well as the silent ones, and for the recorded movers the current extract explains itself.

**Separation.** The three primaries live in `pharmacy_register.csv`, `atc_text.csv` and
`person_register_2025Q4.csv`, none of which the main call opens. The call reads the two dispensing
extracts, the package index, the annexes, the crosswalk, the tracker and the standard. No device
adds, removes or alters a row of the call's own columns, and a line the register turns back is
never a patient's earliest observed receipt of a treatment, asserted over every line rather than
over the generator's own flag.

## Tried and rejected
- Two of the three silent primaries adjudicated by the register's own documentation, and pointing
  the wrong way. The variable dictionary said the defined daily dose is `n_packages` times
  `ddd_per_pack`, while the golden strikes it on the dose the edition in force assigns; and it
  defined the register's chain as the owner at the extract date, while the golden uses the owner on
  the day of the dispensing. A filed rule may not adjudicate a device, and these adjudicated against
  the golden, which is `answer_contradicts_files` rather than a hard ask. Both sentences are gone.
  The dictionary now says what `n_packages` holds and nothing about the basis for a quantity an ask
  grades, and names the pharmacy's chain without dating it; the standard's own definition of
  `ddd_per_pack`, pack size times strength over the dose the index assigns, stands and is what makes
  the three stale rows an internal inconsistency. Neither reading is pinned in the prompt, because
  pinning the source is what kills a device.
- The third primary was a bare contradiction between two shipped files with nothing adjudicating
  either way, which is a competing defensible answer and not a device. The data forces it now: the
  current extract claims no region change for the patients whose region differs between the two
  deliveries, and the register's own documentation of `previous_region` and `region_recorded_from`
  states that it began keeping a previous region on 1 April 2026 and holds none for a change
  recorded earlier. That is a fact about the column, not a handling rule, and it turns the
  disagreement from a contradiction into evidence that the current extract cannot reconstruct the
  earlier state.
- Grading the nearest unreferred pair, which the prompt never asks for. A graded figure with no
  asking sentence has nothing to fix its basis or its population, so a judge reads it as Gate E and
  Gate C at once. It is out of the graded blocks, and the prompt is at 997 characters so adding an
  ask was not available.
- 6,590 accepted lines dispensed at six pharmacies after their own recorded closing date, which the
  register's own rejection rule would have turned back. That is a defect, not mess. A closed
  pharmacy now dispenses nothing after its closing date: its customers' prescriptions are filled at
  the next branch of the same chain, and the handful still transmitted under its identifier are
  turned back with the reason the register holds for it. No accepted line survives its pharmacy's
  closing date, and the exceptions file carries 89 rows that now have a record behind them.
- A register whose dates were clipped rather than recorded: seven deaths and nine emigrations
  landing exactly on the window's last day. The civil registration system now records the event on
  the day it happened, and a patient whose last dispensing is too close to the pull simply has no
  recorded exit, because the register had none to give. The seven referred pairs were re-measured
  after this and are unchanged at 1.365 to 1.499 with the nearest unreferred at 1.033.
- The rest of the reader's realism list: the screening log ran to exactly 96 rows with references
  stepping by one and its last eight rows screened on a single day, so it now runs in numbered
  weekly batches and stops where the desk had got to when the extract was drawn, at 74 rows over 58
  days; the crosswalk's three reasons were exactly 140 each and are now drawn unevenly; the chains'
  log was a complete four-by-thirty-seven grid and now omits a chain-month it filed nothing in;
  packs were only ever 1, 2 or 3 and now reach 4 and 6 for a repeat filled a quarter at a time; the
  four authorisation transfers arrived on four identical dates and now take effect per pharmacy
  within a few days of each transaction, as the authorisations are reissued one at a time; exception
  references carried a 2026 prefix on 2023 dispensings and are now numbered in the year the register
  wrote them; and the spontaneous-report series were six monotone ladders out of nine, which is the
  market story told too neatly, and are now four, with the quarter-to-quarter swing widened.
- Removing the sentence that adjudicated the dose against the golden, without putting anything in
  its place. The second judge then read it as a competing defensible answer: no shipped file said
  which source governed, and it named a third reading, the index column for the 2025 quarter and
  the 2026 edition from 1 January. Removing a pointer to the wrong answer is not the same as
  forcing the right one. Two things force it now. `ddd_per_pack`'s own column description gives its
  formula, the pack size times the strength over the dose the index assigns, and names
  `atc_text.csv` as the index, so every input to the check is shipped; nine package rows across
  three codes then contradict that formula by a factor, beyond the rounding they are stated at,
  while the other 49 satisfy it. And `atc_text.csv` now carries the date the register's statistics
  took up the edition it ships, 1 July 2025, which is before the fee period opens, so no day of
  that period sits under two editions and the vintage reading has nothing to stand on. Both are
  facts about a column and a document, not handling rules, and finding the three codes is still the
  work.
- Leaving ask 3's basis to be implied rather than forced. "Per pharmacy chain" does not say at the
  dispensing date, and the current reading moves a chain-quarter from 5,265 to 3,546. The data
  settles it: the chains' own monthly log of what the register accepted ties to the extract in all
  148 chain-months under the at-date reading and fails in 144 of them, by 56,626 lines, under the
  current-chain reading. That required the log's accepted count to be what the register accepted,
  one line per dispensing however many times a chain transmitted it, so the retransmissions now sit
  in its submitted count where they belong; before that change the at-date reading left a residue
  of 1,922 lines and neither reading tied. Both directions are asserted, in the generator and
  independently in the verifier, so the reconciliation and the rollup the device rides on are the
  same fact measured from both sides and cannot be confused.
- Three impossible register rows and a staged transfer history: APK-110, DSA-116 and VST-126 each
  changed chain after their own closing date, and 32 of 43 transfers fell in one quarter against
  eleven spread over four years. A pharmacy whose authorisation has ended no longer changes hands,
  the four transactions are spread across January, March, August and September 2026, and the
  register's own history is 25 transfers back to 2017, so the inside-window ones are a minority of
  the column rather than three quarters of it.
- The Final Recommendation named Ternivast and Oxelumab as pairs dropped from the equal-chance ten
  when they are the two it hides. Reworded, and reworded a second time so the figure set in that
  block is unchanged: the first rewrite dropped a repeated 10 and `freeze.py` caught it.
- The reader's remaining realism list, carried forward rather than fixed, because the pack ships
  as measured and no graded figure may move: the screening log's last two rows are the same title
  screened on two databases; pharmacy identifiers run 101 upward with no gaps within a chain and
  the names come from one stock list; `in_chain_from` still clusters on four dates, one per
  transaction, which is what a transaction is but reads as a block; the Sovraxil package swap and
  its holder transfer fall on 2026-02-26 and 2026-02-27, which is correct for a transfer but makes
  two devices share a date; and the tracker's two under-assessment rows are exactly the pairs its
  rule could matter for. None of them moves a figure and none is a defect; they are the next
  realism pass on this pack if it is ever reopened.
- **Forced and findable are different properties, and section 3.2(b) carries both.** The judge
  measured the call forced: all 23 pair rows, all 48 chain-by-quarter values, all seven holder dose
  and fee rows, all 24 region and age cells and the chart's two end points reproduce; the seven
  referred pairs come out at 1.365 to 1.499 with the nearest unreferred at 1.033; equal chance
  refers 10 while three date-based constructions all refer the same 7; and dropping the re-sent
  dedup, the retired-key crosswalk or the clearance rule one at a time still gives the same seven,
  so no Layer 1 step decides the call. Gate G and Gate H pass with the decisive step analytical.
  The same sentence that forces it also makes it findable: "the number that would be expected if
  receiving the product had no bearing on when the marker treatment is first received" names the
  timing the null has to be adjusted for. I first read that as a leak, was told it was not, and
  both readings were half right. The phrase is why three independence constructions converge, which
  is what determinism rests on, and it is why a strong reader can see what to adjust, which is what
  Gate F costs. The judge rates the stump power moderate and puts it plainly: it expects a
  substantial share of strong runs to file the crude 50 per cent.
- Rewording 3.2(b) to state the threshold, the comparison and the population without naming the
  timing, so the record would force the adjustment instead of the sentence. Not tried, and
  deliberately so: the launch and lapse dates in `product_register.csv` can carry that work, but
  the same clause is what makes three constructions converge, so removing the words that make the
  answer findable risks the words that make it forced. A forced call a strong reader sometimes
  finds is worth shipping and an unforced one is not, and that trade is not worth taking against a
  judge that has already approved the call. **For the next build in this family: those two
  properties trade against each other in exactly that clause, and the place to buy difficulty is
  the spacing of the multiples rather than the wording of the null.**
- **The multiples are spaced so widely that almost any trend-adjusted null lands the same seven**,
  which is the other half of why the call is findable, and it is the lever a future build should
  pull. Measured across the four window-aware constructions: the null pairs sit at 0.91 to 1.12 and
  the referred pairs at 1.35 to 2.16, with nothing at all between 1.12 and 1.35. The cross-
  construction spread is small for most pairs, 0.014 to 0.15, and only the two the window decides,
  Ternivast with gout treatment at 0.79 and Oxelumab with antidepressant at 0.34, spread widely.
  So two or three pairs placed to sit between 1.20 and 1.35 on all four constructions at once,
  tightly clustered, would make the null construction decide them without breaking the convergence
  the call rests on. That is a data change, not a wording change, and it is the one I would make
  first on a re-root of this slot.
- The reader found one of the three silent primaries, the chain that owned the pharmacy on the day of
  the dispensing, and reported that reading the chain at the extract date instead changes every cell.
  It missed the prior person extract, saying in terms that using `person_register_2025Q4.csv` changes
  all 24 cells, and it did not reach the edition's own dose. One of three found is the ask layer
  working as designed; the primary it found is the one whose own monthly log is a rollup above its
  parts, which is the most visible of the three.
- Its realism list is held rather than worked, because the judge is reading the same pack and a verdict
  on a pack whose data moved underneath it is worth nothing. Held, and all of them real: 96 screening
  titles from about ten stock templates with references stepping by exactly one and the last eight rows
  all screened on one day; exactly 140 crosswalk rows for each of three reasons, a perfectly even
  split; seven deaths and nine emigrations landing exactly on 2026-09-30, the window end, which reads
  as clipped rather than recorded; a complete four chains by thirty-seven months submission grid; pack
  counts only ever 1, 2 or 3; pharmacy names on a "<Town> <Area> Apotek" pattern with chain changes
  arriving in blocks on identical dates; small round spontaneous-report counts that track each
  product's market story; and exception references stepping one to five with 2026 references sitting on
  2023 dispensings. The clipped register is the one that matters, because the person register is an
  input the call reads.
- One reader finding is the reader's own error and is recorded so nobody acts on it: it reported that
  the prompt names two files absent from the bundle. Those two are the deliverables the solver
  produces, not inputs.
- The cracker script printed the mirror's ask score as a second measurement when it was the cracker's
  own score computed twice. For asks that consume nothing the call produces the two agree by
  construction, so this was evidence that was not evidence rather than a wrong number: the skill's
  coupling test cannot be run by comparing a list with itself. The output now says so and points at
  the separation assertions, and it names the weakest ask, A2, which keeps 8 of its 14 figures to a
  response that landed the call. A2 is accepted on the pair arithmetic at 36.5 against a bar of 40 and
  recorded as the layer's thin point.

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
  margin, so the join error costs one membership in the crude column of the grid, none in the window
  column, and the decisive axis still moves the same seven in both rows.
- A flat 3.1 per cent rejection rate drawn over the whole extract, pharmacies open every day of the week
  including Sunday, and each chain's lag a clean rung of the ladder: the cold reader named all three as
  synthetic. Replaced by a per-chain validation rate lifted by quarter with one chain's month of missing
  price records, a pharmacy week drawn from its own open-day shape, and a submission lag that reaches zero
  days. The rejected lines still fall only on repeat dispensings, so no patient's first receipt moves.
- Pinning the four handling conventions in a `known_handling` block of the register's release notes: the
  cold reader read the block as a solver's checklist and named the file under question 3. Each convention
  now stands where the organisation would state it and in its own voice, the re-sent line and the package
  validity in the register's data dictionary, the quarter of dispensing beside the window definition in
  the standard, the extract's adult scope in the manifest's scope statement, and the dictionary covers
  every variable of the files it documents rather than only the four a solver needs.
- Pairs under assessment chosen among the two late-launching products, so the tracker's two open entries
  opened months before their products were marketed: three further dated rows contradicted the same
  lifecycle. Every dated row in the pack now falls inside its product's marketing dates and no date passes
  the extract's pull, both asserted; the tracker's entries still fail 3.2(b) on every arithmetic, which is
  what closes SF12.
- An ask layer with no device mass under its pins. The measured ceiling was 83.5 with the cracker
  keeping all 110 figures, and restoring every pinned reading still left it at 49.5, so the layer
  was rebuilt rather than the pins thinned. Three silent primaries went in, one under each ask, each
  in a file the call never opens: the chain that owned a pharmacy on the day of a dispensing, the
  defined daily dose the edition in force assigns against the figure the package row was written
  with, and the region the October 2025 delivery holds where the current extract's history columns
  are silent. Measured after each one rather than at the end: 83.5, then 50.0, then 41.5, then 40.0,
  then 36.5, with every ask row missing and the leakage at 14.5. The five pins all stayed and
  `freeze.py check --mode rubric` is at exit 0.
- Measuring a graded figure's distance from the wrong edge. `fee_distance` was computed as the gap
  to the nearest whole krone rather than to the half krone that decides the rounding, so the metric
  was inverted: the 0.38 reported last pass was 0.12 from the boundary, and the rates chosen to
  maximise it put four of the seven fees exactly on it. The metric now measures the distance from
  the half krone, the rates were struck against it, and the tightest of the seven is 0.425 with the
  exact figure within a tenth of a whole krone. The verifier recomputes the distance itself rather
  than trusting the figure.
- A turned-back line that was a patient's earliest observed receipt. The rejection device read the
  generator's own `is_first` flag, which no prevalent user's first line in the extract carries, so a
  rejection could move a first receipt the screen reads. The protection is now computed over every
  line, earliest day per patient and medicine, and asserted on the shipped pack rather than on a
  flag.
- Grading 23 chart bar positions when the workbook already grades their inputs: see the entry below.
- A pair ceiling and a mirror leakage declared on paper and never measured. `generator/cracker.py`
  now writes the cracker's path as code and runs it on the cut pack: the measured ceiling is 83.5
  against the declared 39.4, and the leakage 100 per cent against 18.5, because the cracker keeps all
  110 ask figures. The declared sheet had described, row by row, a solver that reads none of the pack's
  filed sentences, which is each ask's mirror and not its cracker. The determinism pins of the previous
  pass then closed the readings the devices rode on, and restoring all five at once still leaves the
  cracker 38.2 per cent and the ceiling 49.5, so the layer's device mass was always short. The pins stay,
  because the judge's verdict rests on them; the ask paths need silent primaries under them, which is
  `/fix-rubric` and the author's call. The number is in the sheet in place of the claim.
- Grading the chart as 23 bar positions: every one of the 23 shares is the workbook's own after-count
  over its patient count, both already graded, so the 23 positions were a second grading of the same
  figures, which is the stacked-ask shape `guide-to-prompt` bans. The chart is back to its named parts,
  the 23 bars, the 7 and 16 of the two fills, the order with its two end anchors and the title's claim:
  10 figures where there were 31, and 200 graded figures in the submission where there were 221. The
  determinism the 23 positions bought is kept in the generator instead, which refuses a share tie, holds
  the order strictly descending and asserts that the two named anchors are its true ends.
- Carrying a payer's doses and fee as floating-point sums: one holder's total was exactly 159766.95
  defined daily doses and the shipped figure was 159766.9, which no rounding convention reaches, and
  three of the seven totals landed on an exact half. Pinning a tie convention was offered and refused: it
  would add a shipped sentence the pack needs only because our own arithmetic lands on halves, and whole
  doses would not help, since whole numbers tie at a half just as readily. Instead every screened
  product's strengths are now whole or half defined daily doses per unit, so a package holds a whole
  number of tenths and a payer's window total is exact at one decimal with no fractional part to round;
  the doses accumulate in tenths as integers and the fee is struck with exact decimals and an explicit
  half-up in the golden and in the verifier alike. The marker treatments keep the index's own two-decimal
  values, because no graded figure sums them.
- Leaving the statutory rates where they were: two payers' fees then sat 0.06 and 0.11 krone from the
  half krone, which one fewer half-dose package flips. The rates were re-struck against the realised
  dose totals, and the tightest of the seven is now 0.38 krone from the boundary with half-up and
  half-even agreeing for all seven, asserted with the distance.
- Reporting the utilisation table on 18 to 39, 40 to 59, 60 to 74 and 75 and over: four of the 24 cells
  then sat within 0.07 of a point of a tenth, the tightest 0.00011 from 79.65. The reporting bands are a
  filed convention and re-partition the same patients without touching the draw, so they were searched
  instead: 18 to 24, 25 to 44, 45 to 54 and 55 and over puts the tightest cell 0.0127 of a point from a
  boundary, asserted, with no cell on an exact half, and the cracker's natural reading misses all
  24 cells.
- Marking each pair's referral threshold on the chart: the marker's position is 1.25 times the pair's
  expected share, and the expected share is the one quantity the standard leaves to the division's own
  epidemiology, so two constructions put the Ternivast gout marker at 0.451, 0.291 or 0.404. A graded
  element cannot depend on the stump. The marker is gone and the chart's graded elements are the 23 bars,
  their order and the darker fill on the referred seven.
- Letting the chart's bar count follow from the data: the deliverable showed the 20 candidates while the
  workbook showed all 23, and nothing said which. The asking sentence now says all 23 and every pair,
  including the three below the patient minimum, carries a share, with the closest two bars 0.1 of a
  point apart.
- Leaving the fee ask on "per authorisation holder" while the golden was struck per fee payer: the holder
  reading gives one payer 224,794.5 doses against the golden's 113,515.5, which is a semantic fork on a
  graded figure. The merger and the transfer are the ask's own device, so nothing was pinned in a
  document; the asking sentence names the payer as the unit, the way it names any other population, and
  the work of noticing the transfer stays where it was.
- A `person_register.csv` whose dictionary entry said a replaced pseudonym appears under both while the
  360 retired keys were absent: a flat self-contradiction in a file a solver reads closely, with no
  arithmetic consequence. The entry and the manifest note now say what the file is, one row per current
  pseudonym, and the crosswalk carries the retired one.
- A submission side that was too clean: the chains' log reconciled to the extract line for line in all
  148 cells, every retransmission belonged to one chain in one month, submissions fell on Sundays as
  often as on Tuesdays, the lag stopped at 20 days and the chain means were a clean ladder. The log now
  counts what the chains transmitted, including lines they withdrew and a cut-off difference, so it does
  not reconcile; the retransmissions are two batches on two chains; the chains transmit on working days
  with weekend batches swept either side; the lag reaches 48 days; and a per-chain, per-quarter transfer
  offset breaks the ordering. All of it is drawn on its own random stream, so the first receipts and the
  whole screen are bit-identical to the judged pass.
- Rejection reasons drawn without regard to the registers: 547 of 568 package-code rejections named codes
  with no validity period and the pharmacy-closed reason had no closing date behind it. A reason is now
  only available to a line the registers can support, and `pharmacy_register.csv` carries `closed_on`.
- Reading the third ask's share as the earliest marker receipt across all eight marker groups: measured at
  the build, and the earliest is in the clearance period for almost every patient, so nineteen of the
  twenty-four cells sat between 2 and 7 per cent and three were zero. The standard's section 4.2 now states
  the table as at least one Annex B marker treatment first received inside the window, which is the reading
  the asking sentence carries, and the cells run from 68.6 to 87.3 per cent.
- A submission lag that let the slowest chain's September lines arrive after the extract was pulled: three
  days of lines sat outside the extract's own as-of date. The pull moved to 20 October 2026, which is after
  every line in the pack, asserted over all 120,388 rows.
- Architecture 2, first judge pass: NOT_DETERMINISTIC, SEND_BACK, with the main call, the pair data and the
  region table all forced and every finding in the other two asks. Four of them: `product_register.csv`
  named the authorisation transfer but not the holder it went to, and about 221 thousand doses turn on it;
  the fee golden counted the re-sent lines twice; it left out the pre-merger payer, which the ask's own
  wording licenses; and the schedule did not say whether a band's rate is charged flat or in tiers, which
  split one payer by 63 thousand kroner. Fixed by filing each of the four in a shipped file (the register's
  `holder_code`, `previous_holder_code` and `holder_code_from`; a release note saying a re-sent line is one
  dispensing in any count of lines or doses; the notes sheet on the payer before and after a merger; and the
  schedule's own sentence that the bands are not applied in tiers), and the fee golden now carries seven
  payers.
- The chain-and-quarter ask took its quarter from nothing in particular: dispensing or submission, the
  window's quarters or all thirteen, and a re-sent line once or twice. The release notes now state that the
  register reports a line in the quarter of its date of dispensing and that the chains' own log counts by
  month of submission instead, the asking sentence says quarter of dispensing in the window, and the re-sent
  rule covers the third.
- The chart ask said the referral line was labelled at its value, which reads as one number, while the
  threshold is 1.25 times each pair's own expected share. Reworded as each pair's referral threshold marked.
- Section 2.5 carried a sentence on patients who died or left the country that could never apply, because
  no dispensing falls after any such date. The sentence is gone and the convergence is asserted instead: a
  clause that never binds reads as scaffolding.
- Eight realism tells the cold reader found, all fixed in the generator without moving the call: the dose
  per pack was a function of pack size rather than a constant per medicine, packages came in an exact
  one-third split across one, two and three, the submission lag's median never moved inside a chain, the
  five rejection reasons came in near-equal counts, the same 22 municipalities repeated across all four
  chains, the literature log stepped exactly three days and cycled its titles, the spontaneous-report
  summary's serious share was 43 per cent every quarter, and the register held no patient under 18, which is
  now the extract's own stated scope.

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

- **Free gates.** 115 generator assertions, 251 independent checks in `verify.py` (it reads only `target/`
  and `figures.json`), `precut.py` 49 checks 0 FAIL 0 WARN, `figures_check.py` 206 of 206,
  `voice-check.py` exit 0 at 988 characters, `leak.py` REVIEW with three answered lines and no LEAK,
  `guard.py heart` WARN with every line answered in `## Draw`, `guard.py surface` promoting no file name
  and no persona. Two rebuilds byte-identical, `target.zip` cut from the final rebuild, 19 entries.
- **Input gates.** 19 files, 4 formats (csv, pdf, xlsx, json), two files above 25,000 rows
  (`dispensings_2023_2025.csv` at 73,879 and `dispensings_2025_2026.csv` at 47,012), three distractors
  named in `metadata.json` and in no file name.
- **The three rules against the built pack.** R1: the pack ships patient-level dispensing lines with their
  dates and no shipped column holds an expected number, a multiple or a referral, asserted over every csv
  header. R2: the referral set is identical with the retired person keys unfolded, with the package index
  joined without its date condition and with the re-sent batch left in, each asserted. R3a: the easy route
  on the clean truth, every filed rule applied, refers 10 pairs. R3b: changing only the expected number
  refers 7, and all four window-aware arithmetics give that same 7. R3c: nothing is planted, and a word
  sweep over all nineteen files finds none of nineteen phrasings of the decisive move.
- **The judge's first pass.** NOT_DETERMINISTIC with disposition SEND_BACK, and every reason in the ask
  layer: Gate G passed (`statistical_rigor`, `analytical_non_defect`, no surface-read dependency, no sole
  data defect), Gate H passed with the decisive step analytical, all 23 pair rows reproduced, and the judge
  built the no-bearing expectation six ways (pair marginals, the same with ties excluded, permutation with
  and without ties, all-window marginals, a marker spread evenly) and every one referred the same seven
  pairs, with referred multiples 1.36 to 2.16 and the nearest miss at 1.03 to 1.12. It ruled the
  equal-chance reading not a licensed second reading, because it assumes identical date distributions and
  the launches inside the window contradict that. The cold reader reached the same seven at about 90 per
  cent confidence, quoted nothing for the decisive step, found no ranking file and answered question 6 an
  analytical choice. Every ask-layer finding is closed in `## Tried and rejected` and asserted in
  `checks.py`.
- **Gate G.** No shipped artifact ranks the pairs on the decision question and `metadata.json` declares no
  wrong-basis distractor. The tracker names two pairs as under assessment and neither passes 3.2(b) on any
  of the five arithmetics; the two distractors carry no marker treatment, no patient key and no pair.
  Delete every wrong number in the pack and the call still turns on how the expected number is obtained.
