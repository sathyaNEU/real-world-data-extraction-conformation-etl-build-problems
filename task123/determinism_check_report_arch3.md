# Determinism check, architecture 3 round 1 (2026-11-01): NOT_DETERMINISTIC on asks 4 to 6, SEND_BACK; order kept; main call forced; Gate G banned (planted_defect_flip, surface_read_rejection); Gate H decisive_step planted

The decisive step read as a built-in coverage gap: the August survey total omits 194 establishments and the task collapses to a sum with a complete survey. Gates G and H fail, so architecture 3 is spent and task123 re-roots as architecture 4 in another world. Isolated thread, Sonnet at medium effort, on target.zip 9bb485be.

# Verdict, task123 round 1

**Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened. Cross-batch check: no prior verdicts or other task folders were available to me, so not run (nothing read outside this folder).

- **Verdict:** NOT_DETERMINISTIC (the main call is forced; supplementary answers 4, 5 and 6 are not). SOLUTION_WRONG also applies to the wording of steps 3 and 8.
- **Disposition:** SEND_BACK. Reasons: the open forks in asks 4 to 6 (prompt and input_files), the Gate G banned scaffold, and Gate H3. Fixing them changes what solvers see, so a rerun is required.

## Why
The main recommendation reproduces and is forced: Sant'Elvira a Mare, Capo Ferrino and Marina di Cervessa qualify, and Marina di Cervessa is closest to the line (31.4). Art. 3 says the survey and the quarterly declarations "registrano gli stessi pernottamenti". Q3 declared minus the complete July and September survey therefore gives the real August (Gate A, B, C pass for the main call and ask 1 to 3).

Asks 4, 5 and 6 each rest on a convention that no shipped file states, and the literal alternative gives different published figures:
- **Ask 4 (Jan to Apr 2026).** The golden adds 34 CIR codes that are in neither the register nor the crosswalk, assigning each to a comune by the CIR prefix. Art. 3 counts only "esercizi iscritti al registro regionale". Register-only gives different values at the nearest 100 for 11 of 15 members.
- **Ask 5 (October 2025 occupancy).** "Net", "type" and membership are not defined. The golden also treats RETTIFICA POSTI LETTO as retroactive.
- **Ask 6 (2025 tax).** The golden's own steps 3 and 8 say "the last filing" for each comune, quarter and category, but its numbers add the small late supplements.

Taxonomy label: underspecified_objective (Gates C and E, asks 4 to 6). Secondary: solution_incorrect (step wording). Gate D is also touched, because the split would be on conventions, not analysis.

## Evidence (recomputed from the bundle)
| Item | My value | Golden | Reproduced |
|---|---|---|---|
| Aug 2026 nights, 18 comuni (Q3 declared, deduped, minus Jul and Sep survey, latest submission per structure-month, CIR to CIN, April re-sends deduped) | e.g. Sant'Elvira a Mare 210,798 (61.3), Capo Ferrino 83,958 (36.9), Marina di Cervessa 228,555 (31.4), Acquanera Marina 124,898 (28.0) | same, all 18 | yes |
| Pop 1 Jan 2026 (popolazione csv, Alvea Salvina 6,205) | per resident as above | same | yes |
| Survey-only reading (naive) | only Sant'Elvira qualifies (47.6); closest Calarossa 22.7 | | the stump |
| Jan to Apr, incl. 34 unregistered structures | Porto Levarna 197,400; Cervessa 81,800; Capo Ferrino 31,200; total 729,400 | same | yes |
| Jan to Apr, register only (literal Art. 3) | Porto Levarna 184,000; Cervessa 80,800; Capo Ferrino 28,600; Acquanera 39,700; Castelpieno 7,600; total 702,700 | | **fork** |
| Oct 2025 occupancy, TIPOLOGIA, 18 comuni, net of closed days, rettifica retroactive | Albergo 29.9, Campeggio 24.2, Casa vacanze 26.2, B&B 28.2, Agriturismo 27.7, Affittacamere 28.5 | same | yes, under that convention only |
| Occupancy, 15 tax-regime comuni | Agriturismo 27.2, Affittacamere 28.6, B&B 28.1 | | fork on membership |
| Occupancy, rettifica dated (pre-correction value in Oct 2025) | Affittacamere 29.0, Agriturismo 27.9, Campeggio 24.3, Casa 26.1, B&B 28.1 | | fork (data evidence favours the corrected value, but no file says so) |
| Occupancy, gross (all open or closed days) | Albergo 25.0 | | fork on the unfiled "net" |
| 2025 tax, supplements added where the exempt count differs, replaced where it is equal | 468,700 / 2,452,800 / 3,861,200 / 854,100 | same | yes, but only under this rule |
| 2025 tax, "latest filing only" (what steps 3 and 8 literally say) | 464,700 / 2,308,100 / 3,455,400 / 728,600 | | does not match golden |
| 2025 tax, all lines summed | 476,100 / 2,579,200 / 4,199,400 / 867,000 | | fork |

Main-call checks:
- All 784 register structures file July and September. The 194 without an August return are the same set in 2025 and 2026.
- Q4 2025 and Q1 2026 declared totals equal survey totals exactly once the 34 unregistered structures are added.
- The 2025 and 2026 August gaps match per comune (ratio about 1.0), so the declaration route is corroborated.
- Alternatives I tried and rejected: scaling Jul and Sep by the reporters' ratio (Cervessa about 26.7, which does not qualify) and the survey-only sum. Art. 3 selects the declaration route.
- Cervessa clears 30 by 10.1k nights (4.4%), and the margin is clean.
- Porto Levarna's later Q3 2026 filing must replace the earlier one, otherwise the gap goes negative.

Competing answers on the main call: none that survives. Residual open point: the member list is not filed. It does not move the three qualifiers (Collebruno, San Gaudenzio and Fontecupa are at 0.9 to 2.3). It does decide which rows the workbook has and the occupancy figures.

## Findings, each with the gate it fails
1. **Ask 4, 34 unregistered CIR codes counted for Jan to Apr (Gates C and E; underspecified_objective).** Art. 3 limits nights to register establishments. The golden's step 6 admits the 34 are "absent from the register" and counts them anyway, assigning comune from the CIR prefix.
2. **Ask 5, "net bed-place occupancy" (Gates B, C, E).** "Net" is not defined. "Type" could mean the 6 TIPOLOGIA values or the 3 tax categories. The register is a Nov 2026 snapshot, so October 2025 beds must be rebuilt from VARIAZIONI. RETTIFICA (retroactive) against POSTI LETTO (dated) is unfiled, and the golden's "in force in October" would literally give the dated reading. Mid-month 16 Oct changes, suspensions and seasonal closes need a bed-days convention. Membership (18 or 15 comuni) moves Agriturismo.
3. **Ask 6, tax per quarter (Gates A, C, E).** Duplicate declarations are either a replacement or a supplement, and no file or flag says which. The solution text says "last filing" and does not reproduce its own figures (solution_incorrect, FIX_NOW in itself). Whether the answer is all-member totals per quarter or a per-comune table is also not fixed by the sentence.
4. **Member list not filed (Gates B and E).** No file lists the union's members. The three comuni without tax filings are included on inference.
5. **Gate G banned scaffold.** See below.
6. **Gate H3 planted.** See below.

## Files/Hygiene
PASS, with notes. 14 files and four formats (csv, xlsx, pdf, txt). The survey has 83,242 rows. Distractors are the airport passengers xlsx and the parking csv. No authoring or provenance language was found. The fiction is coherent (Union regulation 29/09/2026, extract 17/11/2026, Art. 6 date 20/11/2026). The 34 CIR codes missing from register and crosswalk are not explained by any shipped file (the CIR and CIN codes differ across the two files, so there is no register trace). No exclusion-level finding.

## Stump power (Gate F)
The trap that does the work is that the monthly survey silently omits 194 structures in August, so the survey-only total puts only Sant'Elvira over the line. A strong model that sums August and divides misses Cervessa and Capo Ferrino. Art. 3's "same nights" sentence points straight at the reconciliation, and an analyst who counts reporting structures per month (590 against 784) will find it, so the stump is plausible but not very deep. The layered Layer 1 mess (April CIR and CIN double sends, PROGR 2 restatements, five declaration formats, restated and supplementary filings) adds real work.

## Stumping type (Gate G)
`mechanism: planted_defect_flip` (coverage gap); `stumping_family: surface_read_rejection`; `surface_read_dependency: yes`; `sole_data_defect: yes`.
Banned scaffold: the primary stumping strategy is catching that a misleading reported read is wrong and flipping away from it, retired for tasks on or after 8/16 no matter how many corrections it takes. The misleading read is the August survey total, which omits 194 reporting establishments. Clean-data test: with a complete survey the task is a sum divided by population and collapses. The surface read being wrong is not, by itself, a sufficient trap, and adding more corrections does not fix it. Rebuild the difficulty where the reported numbers are FINE. Natural shapes here are a forecast of the August 2026 load that history does not pin, a validated estimate of the unfiled quantity, or a binding constraint. The call must stay forced after the rebuild.

## Three rules (Gate H)
`domain: pass (borderline)`, `layers: pass`, `decisive_step: planted`.
- **H1:** nights per resident is a tourism-statistics quantity, and reconciling the survey against tax returns is tourism-statistics practice. But the call is an eligibility threshold (at least 30) from a regulation. That is a stated-rule check, so the domain is thin.
- **H2.** Layer 1 is the CIR to CIN code change, the April double sends, restatements, an administrative merger and several declaration layouts. Layer 2 is the survey and declaration reconciliation.
- **H3.** The decisive step is a coverage defect built in to flip the answer (the same 194 establishments absent each August). It is not a question of the right comparison, estimand or inference. The easy route (survey August over residents) gives one qualifier, and it is wrong only because of that defect. A strong analyst who cleaned the data and read Art. 3 could still file it, but the miss is a data-coverage catch, which fails the test.

## Fix
- **Prompt and input_files.**
  - Rebuild the decisive step on a FINE-numbers analytical shape (see Gate G).
  - File the member list and the definition of "net" occupancy, with the establishment type (6 TIPOLOGIA or 3 tax categories) and the correction (RETTIFICA) semantics.
  - State whether unregistered establishments count for the Jan to Apr ask, or ship them with their comune.
  - Mark late declarations as replacing or adding, or state the rule.
  - Say whether the tax answer is a per-comune table or a union total.
- **Solution.** Rewrite steps 3 and 8 so the filing rule matches the figures.
