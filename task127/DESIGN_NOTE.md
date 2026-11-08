# task127, architecture 4: Ruahine Bank's 2027 business support envelope

Re-root of task127 after the portal returned architecture 2 as FAILED_TO_STUMP on 2026-11-07 (both responses filed the
golden split; the overlapping equipment wait was found from the data). One architecture per world: the discharge world
is spent, so the slot moves to banking-credit-financial-risk / expected-credit-loss-provisioning, a new world, dataset,
generator and shell, under the objective Opportunity Sizing & Decision Support. The author's five conditions of
2026-11-07 bind the design and are argued in `## Author's conditions` before any data is cut.

## Draw

| Item | Draw |
|---|---|
| Pairing | banking-credit-financial-risk / expected-credit-loss-provisioning x Opportunity Sizing & Decision Support (never carded on this objective on main) |
| Niche | a New Zealand member-owned bank's business support unit choosing which watch-list borrowers its 2027 working-capital envelope supports, by the credit write-off each package keeps off the bank's book |
| World | Ruahine Bank, lower North Island; about 900 business borrowers whose loans and transaction accounts it carries; head of business support Stella Perano, credit risk analyst Lance Middlemiss (guard.py names, en_NZ, seed 127); drawn as Fernmark Bank and renamed at stage 3, FernMark being New Zealand's national brand mark (H21), with Harcourt Packhouse renamed Marlowe Packhouse beside Harcourts |
| Decision | which watch-list borrowers the unit takes on within its NZ$6.0 million 2027 envelope of new working-capital lines, each package keeping its borrower out of default in 2027 |
| Quantity | the 2027 write-off each package keeps off the book, at the IFRS 9 LGD and EAD carried at 31 December 2026 |
| Shape | 05 allocation to a fixed total (the envelope); every watch-list borrower graded |
| Deliverables | bsu_intake_2027.xlsx, bsu_intake_2027.docx |
| Default path answer | Kinloch Engineering and Ridgeway Precast, NZ$3.00 million kept off the book on its own basis |
| Golden | Kinloch Engineering and Matai Valley Foods, NZ$3.35 million kept off the book (NZ$3,343,287 unrounded, asserted) |
| Nearest driver | task132 and task173 at 0.09 (`guard.py check`); mechanisms on the objective read with `guard.py mechanisms` |
| Guard | WARN only, answered. repeat.gate_g and overuse.gate_g (method_or_model_selection, against task268 v6): the default path's error is the model of the package's counterfactual (obligors treated as independent), which no other mechanism describes, and task268's selection is a sampling weight on a trace store, another family. repeat.deliverables (docx+xlsx, against task156 v3): a credit committee takes its papers as Word documents; task156's shell is where / the / the and this one how-much / that / write. Axes corrected at stage 3 against task165 v2 and task268 v6, both registered before this card: forum committee_or_panel (the Credit Committee confirms the intake), forcing event vote_or_meeting (the Credit Committee's February meeting confirms the intake; redrawn at ship from budget_or_appropriation, which task456 v3 holds, registered 2026-11-01), calibration form realised_outcome_roster (the default register counted into conditional rates); the card's notes give each reason. people.first (Christopher, Tracey, Paul, Stephen against older builds): the relationship managers on the watch list print as initial and surname, so no first name ships |

Layer 2 family `estimand_identification` (contamination and spillover); pattern own: the credit write-off a support
package prevents across trade-dependent borrowers. Strategy `causal_design` (spillover); Gate G mechanism
`method_or_model_selection` (the independent-obligor expected loss is the wrong model of the package's counterfactual).

## Default path

1. Read the support unit's 2027 terms of reference (`bsu_terms_of_reference_2027.pdf`): a NZ$6.0 million envelope of
   new working-capital lines; a supported borrower is treated as not defaulting in 2027; packages go to the watch-list
   borrowers whose support keeps the most write-off off the bank's book, each default valued at the facility's IFRS 9
   LGD times EAD as carried at 31 December 2026.
2. Take the borrowers on the January credit committee watch list (`watch_list_2027-01.pdf`) and each one's
   proposed working-capital line.
3. For each borrower, sum twelve-month PD times LGD times EAD over its facilities in the year-end IFRS 9 run
   (`ifrs9_facility_run_2026-12-31.csv`), the bank's validated expected loss (`ifrs9_pd_model_validation_2025.pdf`):
   the write-off its package keeps off the book.
4. Choose the borrowers whose proposed lines fit the envelope with the largest total.

Ends on: Kinloch Engineering and Ridgeway Precast, NZ$3.00 million kept off the book.
Golden: Kinloch Engineering and Matai Valley Foods, NZ$3.35 million: Matai's own expected write-off plus, for each
Ruahine borrower that takes most of its receipts from Matai, Matai's PD times the rise in that borrower's chance of
default when its main payer defaults (the bank's own 2021 to 2026 record) times its LGD and EAD.

## Stump sentence

The default path ends on Kinloch Engineering and Ridgeway Precast, NZ$3.00 million kept off the book, where the
golden gives Kinloch Engineering and Matai Valley Foods, NZ$3.35 million; the step that lands it there is valuing
each package at the supported borrower's own expected write-off, when several Ruahine borrowers take most of their
receipts from Matai Valley Foods and, in the bank's own record, borrowers whose main payer defaulted went on to default
far more often than the rest, so a package at Matai also keeps their write-off off the book.

## Data-native sentence

Ruahine carries both the loans and the transaction accounts of its business borrowers, so the payments between them,
and what became of a borrower after the firm paying most of its receipts defaulted, sit in its own transaction and
default records, while its IFRS 9 model scores each borrower on that borrower's own accounts.

## Author's conditions

The five conditions of 2026-11-07, each answered here before any data is cut.

1. **The field's full method, done carefully, files the wrong call.** The field's method for the write-off a
   package keeps off the book is the bank's own expected credit loss: each facility's twelve-month PD times its LGD
   times its EAD, read from the year-end IFRS 9 run the model risk team validated, summed over the supported
   borrower and maximised over the sets that fit the envelope. Done with every refinement a credit analyst brings
   (twelve-month against lifetime PD read off the terms, stage, facility to borrower grain, the envelope as a
   knapsack), it names Kinloch Engineering and Ridgeway Precast. Only one step files the golden: a package that keeps
   Matai Valley Foods out of default also keeps out of default the Ruahine borrowers that take most of their
   receipts from Matai, whose default chance, in the bank's own record, rises from about 2 per cent (5 of 211
   payee-years) to about 42 per cent (13 of 31) within a year of their main payer's default. No column holds that dependence and no sentence states it; it
   is a relation between rows of the payments ledger (who pays whom, and what share of each borrower's receipts) and
   between dates in the default register (a payer's default and its payees' defaults months later).
2. **No fit picks the golden route.** The IFRS 9 PD model is validated and kept: its back-test on 2024 defaults is green
   in grades 1 to 4 and amber in 5 to 7, monitored without recalibration (`ifrs9_pd_model_validation_2025.pdf`), and the
   terms file the run's PD as the chance of default (3.4), so no recalibration is open to the analyst. The defaults that
   follow a payer's default sit inside every grade's count, and no back-test separates them from the rest. The textbook valuation and the golden agree on
   every historical figure the pack holds: they differ only on the counterfactual the package creates, a payer's
   default that does not happen, which no history can replay. No R-squared, back-test or reconciliation separates
   them; the step is reached by asking what else the averted default changes, and the payments ledger answers it.
3. **The asks are not executable from filed rules.** Each rides a reconstruction across two systems or grains that
   no sentence states (`## Ask sheet`): security values whose valuation dates the 2023 core migration overwrote,
   the true date surviving only in the valuer's reference text, and mortgages discharged at Land Information records
   while the security register still lists them; guarantees given under a company's former name, linked only
   through the companies register, and released in the deed log while the register still shows them active;
   defaults the register records at the grain of the loan account in arrears, a number no customer record lists,
   tied to their borrower only by the loan repayments in the transaction ledger. Each top response keeps under two
   fifths of the ask weight, measured on the cut pack (cracker sheet below).
4. **The ladder keeps at least one of the top two off the call.** The call flips only for a response that both
   thinks of the averted payer default's effect on its payees and measures that effect from the bank's own record:
   an assumed uplift under 0.268 keeps Ridgeway, the borrower's own expected loss keeps Ridgeway, adding the
   payees' own IFRS 9 expected loss keeps Ridgeway, and a pooled rate over every payee of a defaulting payer keeps
   Ridgeway (`## Ladder`). The cracker on the call and the mirror off it measure a pair ceiling of 28.5; with each of
   the pair keeping two fifths of the ask weight the pair sits near 50; built under 60.
5. **The three rules** are in `## Three rules`, one labelled line each; `precut.py` exit 0 is the gate.

## Three rules

Task type: expected-credit-loss-provisioning (Banking, Credit & Financial Risk), which serves Opportunity Sizing & Decision Support in the taxonomy.
Domain test: the deciding quantity is the credit write-off a support package keeps off the bank's book in 2027, the field's own expected credit loss (twelve-month PD times LGD times EAD) read with one obligor's 2027 default removed; with another field's nouns there is no probability of default, loss given default or exposure at default, and no trade dependence that carries one firm's default to the firms it pays, so the task stops reading the same.
Swap: "Which of our watch-list schools should the improvement fund take on to keep the most pupils off the exclusion list?" keeps a pick under an envelope but loses the obligor's PD, LGD and EAD, the payments a bank processes between its own customers, and the default that spreads from a payer to the suppliers it pays, so the call no longer reads the same.
Layer 1: the payments export from the core banking system, whose 2023 migration renumbered every account, so on-us counterparty numbers keyed before the cut-over (and by payers who kept old details for months after it) carry the old number, written with and without dashes and with two- or three-digit suffixes, beside free-text particulars and references; the customer master's several accounts per customer and trading names apart from legal names; the IFRS 9 run at facility grain against a watch list and terms that speak of borrowers; the watch list as a credit committee PDF table; the default register's one row per trigger, so one default can carry an unlikely-to-pay row and a 90-days-past-due row weeks apart; nothing placed to be caught.
Layer 2: estimand identification, contamination and spillover: the averted default of one obligor changes the default chance of the obligors whose receipts depend on it, so the package's counterfactual is the book's expected credit loss with that dependence carried, not the supported obligor's own.
Decisive step: adding to each watch-list borrower's own figure, for every Ruahine borrower that takes most of its receipts from it, the borrower's PD times the rise in that payee's chance of default when its main payer defaults, read from the bank's own 2021 to 2026 record, times the payee's LGD and EAD, with the dependence read from the on-us payments between them.
Not semantics: every field read correctly (the run's twelve-month PD, LGD and EAD, the stage, the envelope, the terms' 2027 window) leaves the easy route at the supported borrower's own expected loss; the dependence is no field, code or definition but a share of receipts computed across two customers' accounts, and the uplift a rate across dated defaults.
Not rule application: no filed rule or procedure carries a default from a payer to its payees; the terms file only the WHAT (the write-off kept off the book, a supported borrower not defaulting, the year-end LGD and EAD). Enumerated family: own expected loss (twelve-month or lifetime), own plus the payees' own IFRS 9 expected loss, own plus an assumed uplift, own plus a pooled uplift over every payee of a defaulting payer, own plus the uplift for payees that take most of their receipts from the payer; Matai's figure runs from NZ$817,175 (own) through NZ$956,944 (payees' own expected loss), NZ$1,248,511 (pooled), NZ$1,406,995 (an assumed 0.25) and NZ$1,471,808 (own lifetime PD) to NZ$1,750,644 (the golden). Standing family (the record separates the rest): the last member with the receipts threshold anywhere from 10 to 50 per cent (Basel's 50 per cent economic-interdependence test included), a 9- to 18-month follow-up, a 3- to 24-month lookback, dependence read over any window of 2025 and 2026, and the payee baseline read from payee-years whose payer survived, from payers that never defaulted or from the payees' own PDs: 48 members, Matai's figure and the total each spread NZ$21,161 inside one NZ$50,000 bin, and the set never moves (it holds to a 55 per cent threshold); all asserted. The rate's grain stays open too: a logistic fit on receipt share and three share bands give the same bins (asserted; the record shows no slope on share), no payer that defaulted shares Matai's division, and SF11 gives the two-band cuts. The ruling-out is loud: payees above the threshold of a payer that defaulted went on to default in 13 of 31 cases, against 6 of 61 below it and a book rate of 3.8 to 7.1 per cent a year.
Analyst test: an analyst who reads every field and rule correctly sums each watch-list borrower's twelve-month PD times LGD times EAD from the validated year-end run and fills the envelope with the largest total (Ends on: Kinloch Engineering and Ridgeway Precast, NZ$3.00 million kept off the book), missing the write-off a package at Matai Valley Foods also keeps off the borrowers that take most of their receipts from it.
Estimand: `bsu_terms_of_reference_2027.pdf` section 3 files the WHAT: the 2027 packages go to the watch-list borrowers whose support keeps the most write-off off Ruahine's book within the NZ$6.0 million envelope of new working-capital lines, a supported borrower treated as not defaulting in the twelve months of its package, each default on the book valued at its facilities' IFRS 9 LGD times EAD as carried at 31 December 2026; the population is every Ruahine business borrower on that run, members not yet in default included, and the comparison is the book with the package against the book without it.
No decoy: nothing is planted to be caught: no copied block, hidden rule, memo, draft, briefing or stakeholder figure carries the wrong answer; the IFRS 9 run and its validation are true records answering their own questions (each borrower's PD, the model's calibration).
No certified replay: no certified or published figure is reproduced to recover the method; the uplift is a rate counted from the bank's own default register, not a rule backed out of settled cases.
Lesson: a credit intervention's value includes the defaults it averts among borrowers whose receipts depend on the supported firm, and the bank that processes their payments can see that dependence and measure its consequence; no build on file teaches default contagion through trade dependence (task177's joint-liability groups and task446's ownership flags are group structures of another kind).

## Survivor anatomy

Actor: the deciding property, how much of a package's value sits in other borrowers' averted defaults, has no column in any file: it is the share of each Ruahine borrower's receipts that come from a watch-list borrower's accounts (two customers' rows in the payments ledger) and the rate at which such payees defaulted after their payer did (dates across two customers in the default register).
Link: the payer and payee are linked only through on-us counterparty account numbers, half of them in the pre-migration format resolved by the 2023 crosswalk, and the consequence only through default dates months apart on different customers; no key joins a borrower to its dependants and no sentence asks for the comparison.
Reflex: the field's named method for the deciding quantity, the twelve-month expected credit loss from the validated IFRS 9 run, sits at rung 1 and files Kinloch Engineering and Ridgeway Precast, NZ$3.00 million.
Back-test: the textbook route validates: the PD model's back-test on 2024 defaults is green in the lower grades and amber in the riskier ones, monitored without recalibration, and the terms file the run's PD (3.4); the own-expected-loss ranking is consistent with every figure the pack holds, and the defaults that follow a payer's default sit inside each grade's count, where no back-test separates them from the rest.
Second use: the payments ledger is the bank's record of its business borrowers' accounts, the source the watch list's commentary on turnover and account conduct is drawn from and the record any support case starts from; the 2023 crosswalk serves every pre-cut-over account reference in it; the default register carries the 2025 defaults the sector table needs; the year-end run carries the limits the commitment figure needs.
Shock: Matai Valley Foods is unremarkable on the statistics a credit analyst sorts by: second of eight by PD but fourth by exposure and fourth by its own expected write-off, its line inside the range of the others, its watch-list commentary ordinary; its eight dependants, in packaging, labels, pallets, haulage, cold storage, cleaning, labour hire and engineering, sit in three divisions and none is its own; no sort of the watch list on one column fills the envelope with Kinloch and Matai (by PD it takes Ridgeway and Matai, by exposure or own expected loss Kinloch and Ridgeway, by line or date added Marlowe and Ridgeway).
Pins: the WHAT is filed in the support unit's terms of reference (the envelope, a supported borrower not defaulting, write-off valued at the year-end LGD and EAD, the whole book as the population) and the default definition in the model validation report; no filed sentence names payers, payees, receipts, dependence, contagion, a follow-up window or a threshold.

## Readability screen

| Rung | 1 named in a file | 2 a column | 3 the field's reflex | 4 an anomaly | 5 a sentence invites | 6 a key joins | 7 a file only it reads | Verdict |
|---|---|---|---|---|---|---|---|---|
| R1 own twelve-month expected loss | yes | yes | yes | no | yes | yes | no | readable |
| R2 lifetime against twelve-month PD | yes | yes | yes | no | yes | yes | no | readable |
| R3 the payees' own expected loss added | no | yes | no | no | no | no | no | readable |
| R4 (decisive) payees' default uplift from the record | no | no | no | no | no | no | no | silent |

R4's tests, one line each: no file names a payee, dependant or contagion (1); the receipt share and the uplift are
computed across rows and customers (2); the field's reflex is R1 (3); Matai and its payees are ordinary on every
statistic (4); the terms name the book and nothing else (5); on-us counterparty numbers need the crosswalk and the
customer master's account list, and default dates join only through the payment relation (6); every file R4 reads
has its own use (7).

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | write-off kept off the book | every Ruahine borrower's expected write-off with and without the package | the supported borrower's own only | Kinloch and Ridgeway | the terms' section 3: "the most write-off off Ruahine's book", the book being every borrower on the run (a method error, not a reading: the population is filed) |
| SF2 | PD | the run's twelve-month PD | the run's lifetime PD | same call (asserted) | the terms' "in the twelve months of its package" |
| SF3 | LGD and EAD | the run's facility LGD and EAD at 31 December 2026 | current drawn balance; limit | same call (asserted) | the terms' valuation sentence |
| SF4 | envelope | NZ$6.0 million of new working-capital lines, each package its proposed line | lines scaled to fit; partial packages | same call (asserted) | the terms: a package is the proposed line or none |
| SF5 | watch-list borrower | the borrowers on the January 2027 committee list | any Stage 2 borrower | same call | the terms name the committee's watch list |
| SF6 | supported borrower not defaulting | its 2027 PD set to nil | its PD halved | same call (asserted at a half) | the terms' sentence |
| SF7 | payee dependence | share of a borrower's 2026 receipts from the payer's accounts, own-account transfers and Ruahine lending left out | any threshold from 10 to 55 per cent; receipts gross of transfers; dependence over 2026 H2, 2026 Q4 or 2025 to 2026 | same call (asserted); the total's bin holds from 10 to 50 per cent | the record: no 2026 payee between 20 and 40 per cent of its receipts from one payer, so every threshold selects the same payees |
| SF8 | follow-up window | default within twelve months of the payer's first trigger, dependence over the twelve months before it | 9, 15 or 18 months; a 3-, 6- or 24-month lookback | same call and the same rate (asserted) | the record: no payee default falls 9 to 18 months after its payer's |
| SF9 | payee baseline | payees' default rate in years their main payer survived | payers that never defaulted; the payees' own twelve-month PDs; nil | same call and the same bins (asserted); nil is outside the bin | the record and the run agree within half a point; a nil baseline is a method error |
| SF10 | rounding | write-offs to the nearest NZ$50,000, unrounded until the end | rounding per facility | same call; every graded write-off clears its bin edge by NZ$2,000 (asserted) | the prompt's last sentence |
| SF11 | the uplift's grain | one rate over every payee above the threshold of a payer that defaulted in 2022 to 2025 | a logistic fit on receipt share; three share bands; two bands cut anywhere from 0.55 to 0.75; a rate by payer division or by year | same call under every one; every bin holds under the logistic fit, three bands and cuts at 0.55, 0.60, 0.70 and 0.75 (asserted for the first two), while a cut at 0.65 puts Matai at NZ$1,700,000 and the total at NZ$3,300,000 | the record shows no slope on share (bands at 4 of 10, 6 of 13 and 3 of 8), no payer that defaulted shares Matai's division, a year holds 4 to 9 payees, and a two-band cut fits halves whose rates differ by less than their sampling error (`generator/ladder.py`) |

## Ladder

| Rung | Construction | Kinloch | Ridgeway | Matai | Set chosen | Rung's own total | The set on the book |
|---|---|---|---|---|---|---|---|
| R0 | largest exposure first (the columns are EAD) | 8,779,004 | 6,512,160 | 4,060,799 | Kinloch and Ridgeway | not a write-off | 3,058,005 |
| R1 (default path) | own twelve-month PD x LGD x EAD | 1,592,644 | 1,421,988 | 817,175 | Kinloch and Ridgeway | 3,014,631 | 3,058,005 |
| R2 | own lifetime PD x LGD x EAD | 2,979,879 | 2,517,942 | 1,471,808 | Kinloch and Ridgeway | 5,497,821 | 3,058,005 |
| R3 | own plus the payees' own IFRS 9 expected loss | 1,592,644 | 1,428,477 | 956,944 | Kinloch and Ridgeway | 3,021,121 | 3,058,005 |
| R4a | own plus an assumed uplift of 0.25 over the payees | 1,592,644 | 1,449,394 | 1,406,995 | Kinloch and Ridgeway | 3,042,037 | 3,058,005 |
| R4b | own plus a pooled uplift over every on-us payee of a defaulting payer (19 of 92, 0.207) | 1,592,644 | 1,442,030 | 1,248,511 | Kinloch and Ridgeway | 3,034,673 | 3,058,005 |
| Golden | own plus the record's uplift for payees above the receipts threshold (13 of 31 less 5 of 211, 0.396) | 1,592,644 | 1,465,362 | 1,750,644 | Kinloch and Matai | 3,343,287 | 3,343,287 |

Measured on the cut pack in NZ$ by `generator/ladder.py`; `generator/checks.py` asserts each rung's set (R3a, R3b). The decisive step is worth
NZ$285,282 on the book (the golden set at 3,343,287 against the default set's 3,058,005, 9.3 per cent); the runner-up,
Matai and Ridgeway, sits at 3,216,005, NZ$127,282 behind. An assumed uplift must exceed 0.268 to move the set, so
every rung that guesses the rate or pools it below the record's keeps Ridgeway. The standing family's 48 members
spread Matai's figure and the total by NZ$21,161 inside one NZ$50,000 bin. Grading: each watch-list borrower's
write-off and the total to the nearest NZ$50,000, each clearing its bin edge by NZ$2,000 or more (asserted).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every Ruahine business borrower on the 31 December 2026 run, members not yet in default included | filed in the terms; C1 for borrowers off the run (none pays a watch-list borrower's payee) |
| 2 | Unit of account | the borrower (customer number), facilities summed | the terms name borrowers; the run carries the customer number |
| 3 | Attribution window | the twelve months of each package (the run's twelve-month PD) | filed in the terms |
| 4 | As-of dating | the run as at 31 December 2026; dependence on 2026 receipts | filed; C1 (2025 receipts give the same payees) |
| 5 | Version basis | the year-end run as published 15 January 2027 | one run shipped |
| 6 | Denominator | a payee's receipts from every payer, own-account transfers excluded | C1 (no payee between 20 and 40 per cent under either basis) |
| 7 | Weighting | each payee by its own LGD x EAD | the terms value each default at its own LGD x EAD |
| 8 | Window length | twelve-month follow-up after the payer's first trigger | C1 across 9 to 18 months |
| 9 | Boundary inclusivity | receipt share at or above the threshold | C1: nothing between 20 and 40 per cent; thresholds 0.10 to 0.55 file the set (asserted) |
| 10 | Rounding path | unrounded until each graded figure | filed in the prompt's last sentence |
| 11 | Tie-break | not needed | the golden set leads the runner-up (Matai and Ridgeway) by NZ$127,282 (asserted over NZ$100,000) |
| 12 | Maturity and censoring | payer defaults to December 2025 only, so every follow-up is complete | C1 by construction |
| 13 | Order of operations | sum within borrower, then the knapsack | commutes: sums within a borrower, then a set choice |
| 14 | Row order | file order immaterial | every step is a sum, a share or a set; no step reads a row's position |
| 15 | Duplicate resolution | a default's two trigger rows count once for the payee rate | C1: binary per payee |
| 16 | Identity normalisation | on-us counterparties through the 2023 crosswalk and the customer master | the systems' own keys; C4 (raw numbers miss half of the history) |
| 17 | Netting against gross | receipts gross of the payee's own outgoings | C1 |
| 18 | Dimensional units | NZ$ throughout | units in the data |
| 19 | Code and status semantics | stage, trigger codes read from the run's and register's own legends | never the stump |
| 20 | Integerisation | whole packages | filed in the terms |
| 21 | Clause scope | the envelope covers new working-capital lines only | filed |
| 22 | Forward window contents | 2027: the run's twelve-month PDs carry the forward window | filed; no driver file needed |

## Literal reader

Executed word for word, the terms' section 3 asks for the set of watch-list borrowers whose proposed lines fit
NZ$6.0 million and whose support keeps the most write-off off the book, each supported borrower's 2027 default
removed and every default valued at the run's LGD times EAD. A literal reader who removes only the supported
borrower's own default from the book executes the estimand with the payees' default chances held fixed, which the
record refutes (payees of a defaulting payer defaulted at 13 of 31, about 42 per cent, against 5 of 211, about 2 per
cent, in years their payer survived); the golden is
the literal estimand computed with the payees' chances conditioned as the record shows. No term reads two ways: every
SF row is ruled out by a filed sentence or converges.

## Oracles

None ships. No file states a dependence, a payee list, an uplift, a book-wide figure or any package's value; the
model validation report reports calibration by grade only; the watch list reports PD, exposure and the proposed line,
and is ordered by date added; no total in the pack ties only under the golden.


## Ask sheet

Three asks, each a component of the committee's case for every watch-list borrower or an audit trail of an input the
call consumes (H18), none computed over the call's own rows, each riding a reconstruction across two systems that no
sentence states.

**Ask A. The value at 31 December 2026 of the property held as security for each watch-list borrower's lending,
each valuation carried forward from the date it was made by the regional property index (8 figures, NZ$ to the
nearest thousand).** H18: a measure every candidate carries that the call does not turn on (the call values defaults
at the run's LGD). Use: the committee's security position for each case. Files: `security_register_2026-12.xlsx`
(Properties: 14 columns), `title_instruments_2026-12.csv` (Land Information mortgage instruments: 8 columns),
`commercial_property_index_2015-2026.csv` (7 columns), the customer master. Primary A1 (D8, a recorded date for the
event date): the 2023 core migration loaded every legacy security with the migration date as its valuation date; the
date the valuation was made survives only in the valuer's reference text, written each valuer's own way. Primary A2
(D4, absence in a file no habitual join reaches): mortgages discharged at Land Information in 2026 on properties the
borrowers sold, still listed as held in the security register; only the title instruments show the discharge.
Hazards: the index's latest quarter published provisional beside revised earlier quarters (latest release per
quarter); title references written with and without the land district prefix. Stops: register date, everything
listed (lazy); true date, discharged kept; register date, discharged dropped; golden. Every figure moves by several
bins under each mishandling (asserted). Pin test: the sentence fixes the basis (each valuation from the date it was
made, the regional index, held at 31 December) and leaves open which record holds the made date and which properties
are still held. Realism: a core migration stamping its load date on carried records, and a register that learns of a
discharge only when someone updates it, are what such systems do.

**Ask B. The most each watch-list borrower could owe Ruahine at 31 December 2026: its facility limits plus what it
has guaranteed of other customers' facilities, an unlimited guarantee counting the guaranteed customer's limits (8
figures, NZ$ to the nearest thousand).** H18: a measure every candidate carries. Use: the committee's total
commitment for each case. Files: the year-end run (limits), `security_register_2026-12.xlsx` (Guarantees: 9
columns; Deed log: 6 columns), `companies_register_extract.csv` (NZBN, current and former names with dates: 7
columns), the customer master. Primary B1 (D7, the true key elsewhere): guarantees executed before a guarantor's
change of name record the former name and, before 2016, no NZBN; only the companies register's former names link
them to the borrower. Primary B2 (D2, a state rebuilt from an event log): guarantees released during 2026 are
recorded as released only in the deed log, while the Guarantees sheet still shows them active. Hazards: limited
amounts written in words or with "plus interest and costs"; guaranteed customers named by trading name. Stops:
NZBN and exact name only, every listed guarantee (lazy); former names linked, released kept; exact names, released
dropped; golden. Pin test: the sentence fixes the WHAT (limits plus guarantees given, unlimited at the guaranteed
limits) and leaves open which guarantees are the borrower's and which still stand.

**Ask C. For each sector, the share of business borrowers performing at the end of 2024 that defaulted during 2025
(per cent to one decimal, 7 figures).** H18: an audit trail of the PD input the call consumes, realised defaults by
sector beside a model the validation report tests by grade only. Use: the committee's view of which sectors default
most. Files: `ifrs9_facility_run_2024-12-31.csv` (12 columns), `default_register_2021-2026.csv` (7 columns),
`default_cures_2021-2026.csv` (5 columns), the customer master's Accounts sheet, the transaction ledger's loan
repayments, and the validation report's default definition (dated by the first trigger, in default until the cure).
Primary C1 (D6, a register at another grain than its name): the register writes an unlikely-to-pay default against
the customer number and a 90-days-past-due default against the account in arrears; where that account is a loan, its
number is in no customer record, and only the ledger's loan repayments (LN rows from the borrower's cheque account to
the loan account) tie it to a borrower. Eleven of the twenty-four defaults of 2025 open on such a row; left unkeyed,
every sector's share falls by 1.9 points or more. The register keys rows to loan accounts in every year (6, 7, 11, 7,
14 and 6 from 2021 to 2026), so the organ is the register's habit, never a 2025 plant. Hazards, executed by the filed
default definition and kept as texture: a default's two trigger rows count once at the first trigger; borrowers that
met unlikely-to-pay late in December 2024 are in default at the year end though the 2024 run, cut off for arrears on
20 December, still staged them performing; cures in 2024 return a borrower to the base and a 2025 re-default counts.
Stops: the run's stage with customer-keyed rows only (lazy); the definition executed with loan rows unkeyed (the
cracker); golden. Pin test: the sentence fixes the WHAT (performing at the end of 2024, defaulted during 2025, by
sector), the filed definition fixes how a default is dated, and which register rows belong to which borrower is left
to the records.

Main population's zero-counts (asserted from the shipped rows): no device or hazard row among the watch-list
borrowers' facilities in the 2026 run's PD, LGD and EAD; no anchor or payee default with triggers straddling a year
end or a cure; no payee whose receipt share sits between 20 and 40 per cent; every payer and payee default the call reads
opens on a customer-keyed row, and the call reads the same rates with the register's account rows dropped.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| 2023 migration (dates, numbers) | A, and the call's crosswalk (neutral, asserted) | A: every borrower |
| the index's provisional latest quarter beside revised earlier quarters | A | A: 7 of 8 figures; the terms file the latest published value, so the cracker executes it |
| title references with and without the land district prefix | A | normalised by the battery |
| a default's two trigger rows; December 2024 unlikely-to-pay; 2024 cures | C | executed by the filed default definition |
| guaranteed customers named by trading name | B | B: one guarantee |

Referee: none; every ask's golden handling is named in a block 3 step only the grader reads.

| Ask | Cracker (call landed, battery run, every filed rule executed) | Figures it keeps | Verdict |
|---|---|---|---|
| A security value | latest index release and title prefixes handled; the register's dates used; discharged properties kept | 0 of 8 | miss |
| B most it could owe | NZBN and exact names matched; former names unlinked; released guarantees kept | 0 of 8 | miss |
| C sector shares | the default definition executed (first trigger, cures, December 2024 unlikely-to-pay at the year end); rows keyed by a loan account no customer record lists left unkeyed | 0 of 7 | miss |

After the notice (one device found and handled in full): made dates found with discharges missed keeps 5 of 8 of
ask A, discharges found with the register's dates 0 of 8; former names linked with releases missed keeps 4 of 8 of
ask B, releases found with exact names the other 4 of 8 (disjoint blocks); loan accounts resolved through the ledger
keep ask C whole, 7 of 23 ask figures (30.4 per cent), the largest single keep and under two fifths alone.
Mirror leakage: 0.0 per cent of ask weight, measured (the mirror stops at R1 and at each ask's lazy stop, 0 of 23).
Pair ceiling: 28.5 measured on the cut pack (cracker 45.0 on the call keeping 0 of 23 ask figures, mirror 12.0 off
the call keeping 0 of 23); a response on the call that also resolves ask C's loan accounts scores 61.7 and the pair 36.9.
Measured by: generator/ceiling.py on the cut pack.

## Deliverables and prompt

Deliverables: `bsu_intake_2027.xlsx` (the choice and the total, then a line per watch-list borrower with the
write-off its package keeps off the book, the security value and the most it could owe; a sector sheet) and
`bsu_intake_2027.docx` (a one-page note for the credit committee). Criteria: the set (1), the total (1), eight
borrowers times three figures (24), seven sectors' shares (7), two files (2): 35.


## Pre-ship check

- The three rules, re-read against the built pack: the decisive step is still analytical (an uplift measured from the
  bank's own default record and priced over the borrowers whose receipts depend on the payer); the mess is still only
  Layer 1 (the 2023 renumbering, the register keyed three ways, valuer references, former names, the index's releases);
  nothing is planted. The leak reader's question 6 and the judge's Gate H both read it as analytical from outside.
- Leak: `leak.py` REVIEW with no LEAK. The reader, twice: no sentence names the decisive step, no file ranks the
  candidates or explains the data, nothing reads as the answer; its question 5 reads terms 3.5 literally as the change
  in expected write-off across the whole book, the golden's estimand. It took the knock-on to run through guarantees.
- Stump-vocabulary sweep lines, ruled here and never sent to the reader: the terms carry default, twelve-month,
  million and carried as the WHAT's own words; the validation report carries default, twelve-month and record as its
  subject. Harmless, neither names payees, receipts or dependence.
- Answer-figure sweep lines: the terms' NZ$6.0 million envelope and section number 4.2 and a validation band edge
  coincide with two sector shares; six guarantee limits coincide with rounded write-offs. Harmless coincidences of
  round amounts; no file ranks the candidates. The block 1 rival figure that matched Matai's proposed line was dropped.
- Judge: pass 1 DETERMINISTIC with FIX_NOW on the control count, fixed in the write-up (the control group stated at
  the 30 per cent cut, which any cut from 10 to 45 per cent matches, and the uplift's composition shown); the one
  re-judge returned DETERMINISTIC, APPROVE, Gate G statistical rigor and analytical non-defect with no surface-read
  dependency, Gate H domain, layers and decisive step analytical. Its residual, the knock-on implied by 3.5 rather than
  instructed, is the stump: filing it would name the step.
- Duplicate: `guard.py heart` WARN answered in `## Draw`; `surface` clean, no unplanned persona.
- House fixes run: H1 (both containers audited clean), H2 (every note figure from `generator/ladder.py`), H3 (the
  note's counts emitted), H4 (16 members at the archive root, equal to the tree and `metadata.json`), H7 (byte-identical
  rebuilds, zip cut last), H13 (no constant id step; long-tailed transaction ids), H14 (SF11), H16 (no date past the
  pull), H21 (renames), H29 (bounds stated exactly), H34 (`ceiling.py` refuses an empty denominator).

## Tried and rejected

- The note's decisive rung, per feeder the smaller of expected buyers and hosting slots: a stated connection standard, a per-feeder hosting map and a neighbourhood-to-feeder join whose keys line up hand it to any solver who reads them, its driver sits nearest task106's, and as labelled it BLOCKs on ban.pattern C (task119), ban.calibration pilot_log (task122) and test.same_driver_older (a signature spent in nine builds); kept as rung 2.
- Resistance-to-heat-pump netting (each resistance conversion frees feeder headroom for oil or propane conversions): the connection standard either states a per-heat-pump assessment, which contradicts the netting and is a counter-pin, or states a net-change rule, which hands it over; a corpus of past approvals would refute the stop rung, which L1 forbids.
- Heat pumps per home (large ducted homes taking two outdoor units, so two feeder draws per slot): visible at heat-pump grain in any connection or rebate record, and found by any solver who counts rebates per buyer; moves only the saturated feeders, too little to change a leader.
- Survey staleness (homes converted since fieldwork leave the pool): a dated register keyed on neighbourhood is a schema-visible pool deduction a careful solver makes unprompted.
- Competing claims on feeder headroom (the utility's deferred queue, committed loads, a state income-qualified programme): each needs a first-come-first-served clause the solver executes, and the effect sits only on saturated feeders.
- Seasonal against winter hosting capacity on summer-peaking feeders: needs a filed "winter" assessment that sends the solver straight to the feeder load history.
- A feeder map naming each neighbourhood's primary feeder while boundary streets sit on the next one: reads as a coarse instrument (sole_data_defect yes under the instrument repair), and a solver who reads "primary" looks for the street-level join.
- The expected minimum against the minimum of the expectation at feeders where buyers and slots balance: under 10 per cent on any feeder and inside the nearest ten on co-op totals.
- The year-end lapse on Year 1's lag alone (late autumn purchases missing 31 December): a stated deadline the solver replays at the finest grain on offer; kept as the check that passes at rung 2.
- A utility service-upgrade queue for old 100 A homes as the decisive rung: the upgrade requirement has to be stated for determinism, which sends the solver to upgrade lead times, and old homes sit mostly on saturated feeders, where the feeder cap already binds.
- Relabelling the note's pilot log as realised_outcome_roster to clear ban.calibration: a relabel that does not name the decisive move, so the organ itself was redrawn as Year 1's install book.
- A Nova Scotia setting with a fictional utility (oil and electric heat): the province's distribution is one large utility, so a co-op that sets its own heat-pump rate meters reads as invented; moved to Minnesota co-op territory.
- A field operations voice saying the 2025 meter-exchange backlog is behind us: true, but it names the backlog and sends a reader to the weeks the crews ran at their ceiling; dropped.
- A filed field-procedure line on the order of work (standing orders first, then orders in date order): read beside the programme's volume it gives a solver a reason to ask whether the crews keep up; the order is to be pinned by the 2025 record instead, and the line stays out unless the determinism check needs it.
- Keeping one co-op as the requester at registration, relabelled cooperative_or_member_body to clear ban.org_family: the key is honest for a member-owned co-op, but two United States power-company allocation builds would then sit side by side with task124, the calibration and artifact bans would still need redrawing, and the business-operations-analytics x opportunity-sizing-decision pairing would still block task128; the requester moved to the fund instead.
- The draw's per-co-op ask figures (meters still unset on 31 December, qualifying buyers the feeders turn away) and its chart parts (the stacked series, the year-end queue annotated): each names rung 3 or rung 4 in the prompt, which outranks every file, so a solver is told the queue and the feeder cap exist before opening anything; replaced by two device-carried pilot audits and a 2027-against-2026 chart.
- Spare capacity of about six sets a week at Lakes: the autumn queue bites harder, but each crew's annual spare (about 300) then falls below Lakes' 420 placeable meters, so a crude annual check hands Riverbend the lead without the queue; spare set back to about ten (annual about 500).
- Lakes and Uplands crews on a Monday-to-Friday week: the 2027 Friday holidays (Christmas observed 24 December, New Year observed 31 December) and Thanksgiving Friday open a holiday-handling fork worth up to a full ten on Lakes' slots; moved both crews to four ten-hour days, Monday to Thursday, with the 2026 record showing they worked the Thursdays before Friday holidays.
- Grading the year's rebated installs as the unrounded co-op sets rounded once to the nearest ten: the two binding co-ops' convention spreads (about 5 and 3.5 sets) add across a ten on the total; the graded total is the sum of the co-ops' slots, with the unallocated figure its complement.
- A spring queue left to run continuously into the autumn at the binding crews: year-end sets then depend on the spring start week and every holiday from Memorial Day on, a spread of more than ten; spring volumes sized so both crews clear by August.
- Pilot spring shares that differ by neighbourhood: per-co-op and pooled readings of the forward calendar then differ by 4.2 sets a point at Lakes; set to exactly 25 per cent in every pilot neighbourhood.
- A 2027 slot-release rule (a quarter of each co-op's slots in the spring window): it makes arrivals depend on the allocation itself and its fixed point (Lakes about 183) disagrees with the one-pass queue (about 240), a fork created by a filed sentence; no release rule, so both readings give 240.
- A per-co-op ask on the pilot's days from claim to payment: a staffing decision that the split never reads, so it fails H18; re-cut to the rebate dollars paid in 2026 and the installs they cover, the audit trail of the pilot the rates are built on.
- A pilot close-out stating the total rebates paid: an oracle that verifies ask B's handling for free; the pack states no paid, cost or cleared total.
- Field-order volumes at the draw's 70,000 rows: six crews' standing work over 104 weeks is about 31,000 orders at realistic crew sizes, and padding the file to 70,000 would need order types nothing reads; 31,000 clears the gate.
- Ask B's clock device on the 31 December 2026 evening payment run: the pack's as-of date is 11 December and the trustees meet on 17 December, so no December run exists to cross the year; the cutoff moved to the fund's November month end (the 30 November run clears on 1 December UTC) and the prompt asks for rebate dollars paid through the end of November.
- Anthony Bentley as the outreach director: the name is not in the seed-127 draw (`guard.py names --geo "United States, Minnesota" --seed 127 --n 200`); Anne Garcia from the draw then took BLOCK people.first against task125; Sara Duncan from the same draw is clear.
- The outreach director's belief that Uplands has more propane and electric homes than any other co-op: Table H1 puts Valley first on propane and electricity, so the belief would be a stakeholder read the pack refutes; reworded to more qualifying homes, which the survey's joint counts make true (rung 1's leader).
- The rung 3 twins with each neighbourhood's buyers split across two feeders: the map puts each neighbourhood on exactly one feeder, so Elm Park and Birch Hollow are identical on the survey and sit on a full and a roomy feeder respectively.
- A Lakes ceiling cycle averaging 10.45 a day over twenty days: the plateau's 50 days start mid-cycle and recover 10.57, which moves Lakes across a ten; the ceiling is a four-day 11, 10, 11, 10 pattern (42 a week) and standing work a twenty-day block averaging 8.05, so spare is 2.44 a day in any window.
- Pilot install rates with neighbourhood-level noise: rates by system and income band, or each co-op's own pilot rates, would each give a different forward figure (H14); every pilot neighbourhood is built from unit blocks (38 ducted-propane households to 3 installs, 32 electric to 1, 95 hydronic to 1), so every finer grain returns the system rates exactly.
- Pilot purchase dates spread evenly with a random installer lead time: autumn installs clustered to six orders a week at Uplands (0.86 of its spare); installs are spread evenly over each season's install span instead, peak four a week at Lakes and three at Uplands.
- The rebate amount as a pilot-log column: it would let a per-rebate reconciliation of the ledger find every returned payment for free; the amounts live in Schedule B of the participation terms instead (still a reconciliation route, recorded as HZ2's leakage).
- The rules file named `clean_heat_programme_rules_2027.pdf` after the fund: leak.py's file-name sweep reads `clean_` as the author's cleaned-data noun (LEAK); renamed `heat_pump_programme_rules_2027.pdf` in the generator.
- A "Decision sought" closing section and totals for expected installs, feeder room and meter sets in the note's line-by-line table: the section restated the split on an orphaned page, and a meter-set total of 1,174 beside 1,170 placed is a second statement of the year's installs by another rounding path (H3); both cut.
- 2026-10-10: the crew meter-set queue as decisive rung under a hosting-slot cap; the determinism judge returned SEND_BACK and the build was retired, not submitted.
- 2026-10-12, re-root (architecture 2): the author re-queued the number in wave 1 as "re-root, Opportunity Sizing". Candidates weighed at the draw and rejected: a charged-off card portfolio's sale against keeping it (the warehouse's payers are a visible attribute every solver conditions on, and the composition-mix strategy is banned against task501); a diabetic eye screening van placed by first-round against repeat-round yield (the prevalence-round effect is textbook to a strong solver); acoustic leak-detection crews placed by main material (material is a GIS column the reflex stratifies on, and a conditioned yield transferred across mixes is composition mix); a health plan's navigations split by procedure group where members follow their surgeon (the payment-claims task type serves ETL and Anomaly Detection, not Opportunity Sizing); an overdraft fee cap's revenue at risk sequenced after the banks' own changes (lending sits outside Economics in the client taxonomy, and no banking task type serving Opportunity Sizing fits a rule's revenue impact).
- 2026-10-12, architecture 2 at stage 2: a brokerage "package available from" date beside the start date (care ready before the patient left): it shows the care wait apart from the delay for every patient held by equipment, so a solver reconciling the two sees a third of Ashby Vale's patients leaving days after their care was ready and goes looking; the brokerage records care starting on the day the patient went home, and the restart patients carry the counterfactual instead.
- Restart patients needing discharge equipment at the same rate as new-package patients: subtracting their average nights (the control reflex) filed the golden split exactly; restart patients mostly have their equipment at home already (0.15 of the rate), and the control now files Ashby Vale first.
- Wendlebury's equipment need at 0.27 of covered patients: counting equipment patients at nought (R2) then filed the golden split; at 0.62, with the North depot's quick deliveries, R2 fills Cleeve Park and leaves Wendlebury short while the golden barely moves.
- The national weekly return by site: its nights per discharge rank the hospitals on the delay, an artifact on rung 0; it ships by trust, a distractor.
- A boundary change moving two wards from Ashby to Marchford district in April 2026 as an Ask B device: the ask's "district" would read two ways (as then or as now); the districts are stable and the county-line postcode district carries the district hazard.
- The winter's delayed bed-days total in the chart's title: within-trust moves leave the five-hospital total unchanged, so the cracker banks it; the title states what the chart shows, and the ask adds each hospital's delayed patients.
- Re-brokered and re-sent referrals as Ask B devices: whether a re-sent referral is a second referral the brokerage took reads two ways; cut.
- The part-filled hospital's bed-days at 967.45: rounding the value to two places first gives 968; the clearance brings one Cleeve Park delivery forward a day, so 968.23 rounds to 968 on every path.
- 2026-10-14, second-layer attempt after shipping (built to stage 4, not shipped): the patients the wait for home care itself sent to a rehabilitation bed or a care home (re-assessed while waiting, so the warehouse records them on pathway 2 or 3 and the default cohort conditions on the wait's own outcome), found from the brokerage's withdrawn hospital referrals, with the note's section 3 moved to "medically optimised for discharge home on pathway 1". Every free gate was green (27,838 checks, the verifier, a byte-identical rebuild, precut, leak.py), but the judge returned NOT_DETERMINISTIC and SEND_BACK on that pack (determinism_check_report_loop1.md, which covers the rejected prototype and not the shipped pack): no shipped sentence says a withdrawn hospital referral marks a patient optimised for home, and that reading alone moves Ashby Vale from 10 packages to none. Filing the population as "whatever pathway they left on" would hand over the post-treatment insight and leave only a record linkage a solver executes once told, so the call would turn on a filed rule; the leak reader also opened a fork on the package's "up to four weeks" (the re-assessed patients waited 23 to 26 nights on average). Reverted to the shipped pack, which the generator rebuilds byte-identical (27,095 checks); the shipped build's longest saving is 14 nights, so the four-week fork does not reach it.
- 2026-10-14, architecture 3 (a full refresh at the author's request, built to stage 4, not shipped): actuarial reserving for a motor bodily injury book (Ninebark Mutual, year end 2026, Forecasting), the paid history restated at the latest diagonal's closed shares of claimant features (Berquist-Sherman) after a claims platform slowed settlement, $400 million carried against the paid chain ladder's $325 million. Stage 3 green, the leak reader clean and the adjudicated clone check on Sonnet CLEAN, but the judge returned NOT_DETERMINISTIC, SEND_BACK: the reserving basis leaves the method to the actuary, and frequency-severity on paid per closed feature carries $350 million with nothing shipped selecting between them, while filing the method would make the decisive step rule application. The author restored this architecture; architecture 3's note, generator and judge report are in git at 6edd337.
- 2026-10-16, loop 1: filing the dependency as a discharge rule ("the ward discharges the patient once the delivery is made") in the equipment notes: it states the timing that a package's counterfactual turns on, so the decisive step would read as executing a filed rule; the route's definition files only what the equipment is for. The judge's optional pin (required_by is the discharge ready date) stays out for the same reason.
- 2026-10-16, loop 1: practices closed by merger on covered patients' spells (67, carried by the patient for every later admission): dropping the closed codes moved four hospitals' caps, a field reading that could decide figures on the main call; the registration is now taken at admission, so the closed codes sit only on spells admitted before each merger.
- 2026-10-16, loop 1: waits drawn flat between two bounds (home care 4 to 10 nights in Marchford, 6 to 14 in Ashby; South deliveries 5 to 13): the stage 4 reader read the covered patients' nights after the ready date, 3 to 14 with a hard floor, as too clean for delay data; every wait is now right-skewed by its quantile at the same uniform draw, so no other draw in the stream moved.
- 2026-10-16, loop 1: a weekend event moved to the Monday (and sometimes the Tuesday) by a fixed chance: every Saturday and Sunday the services turned down piled onto Monday, so Monday carried 1.8 times a midweek day's discharges and 2.3 times its deliveries, a new tell; a turned-down weekend day now redraws the wait from the service's own spread, which spreads the weekend's load across the working week.
- 2026-10-31, reship under the learning loop's rules: the acute, equipment and council extract notes and the data
  request log withdrawn (shipped files may not describe the data, and the log narrated a device); the two reporting
  conventions the notes carried that a figure turns on (delayed nights dated to their evening, a patient delayed in a
  month with one such night; the brokerage's wait in calendar days from receipt to start) moved into the fund note's
  monitoring section, and every other field reads from its own column. The prompt dropped its counts of hospitals,
  districts and months and opens on where the packages go.
- 2026-11-07, portal FAILED_TO_STUMP on architecture 2: both responses filed the golden split exactly (Royal Marchford 508, Wendlebury 350, Holmford 120, Cleeve Park 222, Ashby Vale none, 6,816 bed-days). The equipment wait running alongside the care wait is an overlap a careful response finds by joining the depot's deliveries to the covered patients, so the stump was a hidden overlap rather than a method the field's full practice gets wrong; the discharge world is spent and the slot re-roots in another domain.
- 2026-11-07, architecture 4 draw, candidates screened on paper before this card: the marginal travel a visit
  adds to a crew's day (a shared cost a removal does not save is architecture 2's logic, and routing reads the same
  for any field); a pooled fleet assessed by round rather than by vehicle (task153's fleet duty-cycle world, and the
  estimand has to name the rounds); arrivals seeing busier units than the time-average busy fraction (the optimization
  card's MEXCLP is the careful route and a replay of the calls lands the golden); failures per running hour or start
  (task170 and task176 screens); vacancy chains (task174, task137); turbine wakes (task187); demand-response snapback
  (task118); a lower screening threshold read from interval cancers in excess of the undetectable band (excess over a
  reference band is epidemiology's attributable-risk reflex, and the follow-up contradicts any extrapolation, so a
  back-test picks the golden); a written-off portfolio's hold value by payment arrangement (architecture 2's draw
  rejected the card portfolio sale, and a paying segment is a visible attribute); a setting active only above a
  threshold (task162), threshold counts from point predictions (task253, task151), staggered adoption (task136,
  task137), immortal time (task122), a post-treatment control (the careful textbook's own remedy). Chosen: the
  write-off a support package keeps off borrowers that depend on the supported firm's payments.
- Contagion defaults on the first payees of each payer (stage 3, 2026-11-08): the record's payee default rate then rose
  with receipt share (bands at 0.30, 0.43 and 0.57), so a logistic fit on share or three share bands moved Matai's
  figure and the total a NZ$50,000 bin. Reassigned within each payer so the rate is flat in share, every count and date
  kept; a two-band cut at 0.65 still moves a bin (SF11), as no assignment of 31 outcomes holds every cut.
- Matai Valley Foods in Manufacturing (stage 3, 2026-11-08): a rate by the defaulting payer's division (3 of 8 in
  Manufacturing) put Matai at NZ$1,650,000. Moved to Agriculture as a grower-packer supplying supermarkets, a division
  in which no payer defaulted.
- Fernmark Bank and Harcourt Packhouse (stage 3, 2026-11-08, H21): FernMark is New Zealand's national brand mark and
  Harcourts a national real-estate brand one letter away. Renamed Ruahine Bank and Marlowe Packhouse.
- The wholesale borrower's 2025 re-default (stage 3, 2026-11-08): put wholesale's share at exactly 6.25 per cent, a
  rounding tie. Dropping it changed the number of defaults and shifted every later draw (asks A and C moved); the third
  re-default moved to retail instead, same draws.
- Round watch-list PDs and balances, and a validation table marked Pass on every grade (stage 4 leak reader,
  2026-11-08): two-digit PDs, term loans drawn exactly to their limits and balances in whole thousands read as built,
  and an honest one-sided test fails grades 5 to 7. PDs now carry four decimals, balances cents, term loans amortise,
  and the table carries the bank's traffic light, amber in grades 5 to 7 and monitored.
