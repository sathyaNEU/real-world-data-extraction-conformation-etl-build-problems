# task133 determinism check, architecture 3 (spent)

One isolated judge pass on the ICAAP business-book architecture (target.zip d613bac0). It returned NOT_DETERMINISTIC with SOLUTION_WRONG on one figure and failed Gate H (the filed standard licensed the own-division route); the leak reader's question 6 read the call as a stated procedure plus field reading. Architecture 3 was spent and the slot re-rooted.

# Determinism check, round 1 (2026-11-01): NOT_DETERMINISTIC with SOLUTION_WRONG on one figure, SEND_BACK; order kept; Gate G PASS; Gate H 'decisive_step analytical only if the method is filed'

Read against the gate table this is a Gate H failure: the filed standard licenses the own-division route (NZD 10.0m), so a strong analyst who reads every rule correctly is not wrong the easy way, and filing the payer route would make the decisive step rule application. The leak reader's question 6 read the call the same way (a stated procedure plus field reading). Architecture 3 is spent and task133 re-roots as architecture 4 in another world. Isolated thread, Sonnet at medium effort, on target.zip d613bac0.

# Verdict, task133 round 1

ORDER: kept. derivation.md was written to disk (own figures for every asked quantity) before graded_blocks.md was opened. The cross-batch reference check could not be run (no prior packages are readable in this sandbox); no near-duplicate claim is made.

- **Verdict:** NOT_DETERMINISTIC (also SOLUTION_WRONG on a sub-point: Trade and logistics 2.4 does not reproduce).
- **Disposition:** SEND_BACK. The decisive step (how a borrower's own sales fall is derived from the scenario) and three asks' conventions are unfiled; fixing means filing them in CR-ST-02 and/or the prompt, which changes what solvers see, so a rerun is required.
- **Governing taxonomy label:** underspecified_objective (Gates B, C and E fail; Gate A fails on one figure).

## Why
CR-ST-02 2.1 gives only "the change in the division's sales" per ANZSIC division, 3.2 asks for "the fall in the borrower's own sales", and no filed sentence says the borrower's fall is anything other than its division's fall (4.1 files the division from the NZBN register). Read word for word, every borrower takes its NZBN division's scenario change and the book loses NZD 10.0 million (10.03). The golden's 11.5 comes only from an unfiled method (classify the 74,492 operating-account credits, match payers to the NZBN extract by an upper-cased, LIMITED-to-LTD, first-20-characters name, credit-weight the payers' division changes), and the golden itself names three rival answers (10.0, 10.5, 12.0) for that step. Nothing in the package pins payer-weighted over own-division, nor how to treat individuals, unmatched firm names, card settlements or government payers.

## Evidence (my own recomputation vs the golden)
| Item | Literal reading of the filed text | Golden | Reproduced? |
|---|---|---|---|
| Book stressed loss, NZD m | 10.03 -> 10.0 | 11.5 | No under filed text. Payer method gives 11.72 (rounds to 11.5), 11.75 or 11.91 (rounds to 12.0) depending on how unmatched payers are weighted; 11.5 sits 0.03 from the 11.75 edge |
| Segments (own division) | Con 2.9, Mfg 0.7, Trade 1.8, Hosp 3.4, BPS 0.8, Health 0.4 | Con 2.5, Mfg 1.3, Trade 2.4, Hosp 3.4, BPS 1.5, Health 0.4 | Payer method: Con 2.54, Mfg 1.33, Trade 2.56 to 2.61, Hosp 3.38, BPS 1.51, Health 0.41. Trade 2.4 does NOT reproduce (SOLUTION_WRONG sub-point) |
| 632 borrowers, EAD 496.7m | 634 borrowers, 497.5m (two book-D customers 7357449 and 7109135 carry an in-force override to 6, so by 3.2 their risk grade is 6, not D) | 632, 496.7 | Yes, if D is read off the book column ignoring the override. Immaterial to rounded figures (0.012m) but a second unfiled convention |
| 56 per cent of credits from other divisions | n/a | 56 | Yes (56.5 per cent with my matching) |
| NCL by segment and half, NZD thousand | Business write-offs less Agency remittance, Liquidator dividend and Instalments dated on or after the customer's first write-off: Con 251/957, Mfg 156/409, Trade 218/212, Hosp 366/733, BPS 296/324, Health 283/288 | Con 187/858, Mfg 115/380, Trade 200/148, Hosp 331/699, BPS 289/292, Health 270/280 | Golden reproduces exactly only by also crediting the 69 Instalment receipts on 34 Personal/Retail cases to the company each guarantor guaranteed (guarantees_register), a link no filed text states |
| Default back-test | 1-3: 2/187 = 1.1; 4: 6/142 = 4.2; 5: 8/152 = 5.3; 6: 10/128 = 7.8; 7-9: 8/73 = 11.0 (register customer_no, merge map applied, rural-book customers out) | 4 (2.1), 9 (6.2), 10 (6.5), 13 (9.9), 9 (12.3) | Golden reproduces only with three unfiled choices together: rural register defaults included, 11 Rural-book customers kept in the bands, and each register facility moved to the customer holding it in the lending book (cross-default rows under a group lead credited to members) |

Forks that survive (each shown with the answers it produces):
1. Sales transmission: own division 10.0 vs payer-weighted 11.5/12.0 vs division-average mix 10.5 (golden's own list). Decides the main call and segment figures. Fails C, E (and B: the rule is nowhere in the files).
2. NCL recovery definition: Agency remittance vs Agency collection (double count, commission); Instalments on or after first write-off in or out; guarantor personal-case receipts in or out; for 15 multi-facility customers, 9 receipts fall between first and last write-off with no facility key (first-date vs last-date moves Con H1 251 vs 254, Health H1 283 vs 290, Hosp H1 366 vs 369). CR-ST-02 4.2 says only "recoveries the bank received in the half on loans already written off". At the thousand-dollar rounding asked, every variant gives different graded figures. Fails C, E.
3. Default back-test population and unit: rural-book customers in/out (grade 4 8 vs 9 defaulters, grade 6 11 vs 13) and register customer vs facility holder (grade 1-3 2 vs 4). 4.3 says "business borrowers" and 1.2 puts the rural book outside the standard. Fails C, E.
Things that are forced and reproduced: NZBN division over the bank's old ANZSIC codes, override-in-force logic, Table 1 to 3, 50 per cent undrawn on revolvers, no Table 2 band edge touched, merge-log mapping (without it grade 4 and 6 lose one defaulter each), grade D snapshot rows (31) outside the bands.

## Files/Hygiene
PASS, with notes. 20 files, 4 formats (csv, xlsx, docx, pdf); rows: operating credits 74,492, NZBN 26,300, lending book 1,346. Read like system extracts (mixed date formats, old-code industry fields, blank codes, merge log, truncated 20-character payer names). Distractors present: rural_book_stress_summary_ICAAP_2026.pdf (20.4m rural total), deposit balances, connected_groups, industry_sales_quarterly. No README or authoring language seen. Temporal: NZBN and master extracts post-date the book date, acceptable. No exclusion-level finding. Note: the operating-account file is not a distractor; it carries the golden's decisive step, yet no filed document mentions using it.

## Stump power (Gate F)
A strong model will most likely stress each borrower at its division path (the filed text), land 10.0, and score off the main call; that is a valid-looking miss but for an unfiled reason, so it is not creditable as a stump. The payer-mix build is long and name-matching sensitive, so even a solver who chooses it can land 11.5 or 12.0 by chance of classification. Lever: file the sales-path convention (population, which credits are sales, payer-weighted) so the literal reading is the golden, keeping the decision on the analysis of the payer base, not on guessing it.

## Stumping type (Gate G)
`mechanism: other (sales-path transmission through the payer base, with ETL conformance)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Not a surface-read-rejection (no reported figure is wrong), but the transmission rule is an invention the files do not contain, so it cannot be credited as a valid analytical stump until filed.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical` (conditional on being filed).
H1: ICAAP stress of PD x LGD x EAD by sales shock passes the swap test. H2: Layer 1 = old ANZSIC codes, blank industry fields, merge log, truncated payer names, gross vs net agency receipts; Layer 2 = deriving the borrower's own sales exposure from where its credits come from. H3: the easy route (borrower inherits its division's fall) gives 10.0 where the golden says 11.5, which would be analytical, but the shipped standard licenses the easy route, so the golden's decisive step is not forced; it is also close to a hidden rule until 3.2 is amended.

## Fix
- prompt / input_files: amend CR-ST-02 3.2 (file the WHAT: the borrower's sales change is the credit-weighted change of the divisions its trading credits come from; which credit types are sales; how individuals, card settlements, government payers and unmatched payers count; how payers are matched), so the literal execution is 11.5 or whatever the generator asserts, and re-verify Trade and logistics (2.4 does not reproduce).
- 4.2: file whether receipts on a guarantor's personal case are recoveries of the guaranteed company's write-off, whether post-write-off Instalments count, and the date test for multi-facility customers.
- 4.3: file the unit of "defaulted" (facility holder vs register customer) and whether rural-book customers scored in the 30 Sep 2025 snapshot belong to the bands; file that a book-D customer with an in-force override is in or out.
- Rerun required after the fix.

