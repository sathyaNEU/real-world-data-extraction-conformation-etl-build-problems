# task501 design note

## DRAW (v3, re-rooted 2026-10-11 after the v2 portal result; v1 and v2 retired, see Tried and rejected and the card's lineage)

| Axis | Draw |
|---|---|
| Domain / subdomain | Quantitative Finance (author-declared, 2026-10-10) / Liquidity, funding & balance-sheet risk |
| Objective | Forecasting & Predictive Modeling |
| Niche | a Swiss occupational pension fund's private-markets programme sizing a standby capital-call facility for 2027, where the directive selects the pacing basis by a walk-forward test and sizes the buffer from how far realised calls ran ahead of the forecast at any point in a test horizon; managers close most deals in the first half of each year, so the end-of-horizon miss understates the exposure the facility faces |
| Shape | 02 forecast across many periods (twelve 2027 months of net outflow and a twelve-origin test table, one committed facility tranche) |
| Gate G mechanism | forecasting (the deciding quantity is the within-horizon path error of a forecast, the facility's actual exposure), carrying method_or_model_selection (the basis selected by validation on data it was not built on) |
| Gap / pattern | time first (the exposure is a path through the year, not a year-end total), population, rule / none: G13 horizon (the month-end path against the twelve-month total), G16 method selection, G2 the per-fund grain of the richest basis |
| Decision / unit | dial_setting, the facility tranche in CHF from the lender's menu (CHF 25 million steps to 300) |
| Calibration | the twelve-origin walk-forward record: realised monthly calls of the funds on the register at each quarter-end from December 2022 to September 2025 |
| Context artifact | register (static terms, including the recycling clause) |
| Role / forum / event / org | head of treasury and liquidity (finance_controller) / the foundation board (trustees_or_governors) / the September 2026 liquidity squeeze (incident_or_complaint) / financial_institution |
| As-of | plan extract 30 September 2026; the golden is prepared in October 2026 for the board's November sitting; forward window calendar 2027 |
| World | Switzerland, Zurich, CHF (fund currencies USD and EUR); people drawn with `guard.py names --geo Switzerland --seed 118`: Serena Sidler, Luciano Hotz, Othmar Suter, Enrique Hofer, Noelia Amrein, Marino Imhof |

**The client's three rules, answered.** (1) The deciding quantity is a forecast's path error over a horizon, the liquidity exposure a desk sizes a line against; swap the nouns to grants and the walk-forward and the path buffer still have to be built. (2) Layer 1: withdrawn notices, absent statements, a booked-rate column, value-date currency, in-specie lines, a recycling clause to apply, strong first-half seasonality in calls; layer 2: the easy analysis reads the shortfall at the end of each horizon and lands a tranche short, and the easy validation (fit once, score the past) lands there too by another route. (3) No planted defect, definition or hidden rule decides the call: every term is filed in the register or the directive, and a solver who reads every rule correctly still lands short by measuring the buffer the way the error table invites.

**Stump sentence.** A competent solver runs the walk-forward as filed, selects the age-band basis, and sizes the buffer from the end-of-horizon shortfalls it already has in its error table (largest 61,852 thousand), electing CHF 200 million; the step that lands them there is never tracing realised against forecast cumulative calls month by month inside each horizon, where the first-half run of calls puts realised 96,560 thousand ahead of the forecast at a month-end, the exposure the facility is drawn against under s.4 and the amount s.5.6 asks for "at any point in a horizon", which elects CHF 225 million. A solver who also fits the candidates once on the whole record crowns the manager's-own basis and lands on 200 by that route too; with no test at all, the CIO's reading, 175.

**Why v2 cracked and v3 is drawn differently.** v2's decisive step was the walk-forward's mechanics, filed in full in s.5.3; both portal responses executed it and landed CHF 250 million. v3 keeps that machinery as a filed execution layer and moves the deciding quantity to one the filing leaves to the analysis: the error table is naturally built on twelve-month totals, and the facility's exposure is the cumulative path inside the year. The seasonality that makes the two differ is ordinary first-half deal closing, visible in the ledger.

**Nearest exemplars read.** Treasury Cash Flow Forecasting (client mean 0.41: a loss method pinned on a cumulative within-period position against independent-date scoring, the same shape as this build's path against end-of-horizon) and Capital Grant Drawdown Forecasting (0.34).

**Realism debts.** The recycling term is uniform across the 47 funds (filed per fund in the register). First-half seasonality runs at about seventy per cent of a year's calls in January to June; strong, and stated nowhere because the ledger shows it. The fund-year pacing noise is ordinary lumpiness that makes the manager's-own basis memorise the past.

## GATE G

- **Litmus.** No reported number is wrong and no conclusion is overturned; the CIO's belief in each manager's own record is true of the past (the best in-sample fit) and false forward. The difficulty is measuring the buffer on the exposure the facility faces rather than on the total the error table shows.
- **Primary mechanism:** `forecasting`, supported by `method_or_model_selection`.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Clean-data and lens tests.** Nothing is repaired on the way to the answer; the recycling clause is filed and applied. The wrong and right buffers are two measurements of the same forecast errors (end of horizon against path), an estimand choice, not two readings of one figure.
- **Delete every wrong number:** there are none; still hard because the leak is in the solver's own procedure and the estimand is the analyst's to get right.

## LADDER (facility required = peak cumulative net outflow + buffer less the CHF 75m reserve, CHF million)

Answer: **elect CHF 225 million** (required 212.2: peak 190.6 in December plus the path buffer 96.6 less 75; 12.2 and 12.8 from the bin edges).

| Cell | Basis and buffer | Required | Tranche | Violates |
|---|---|---|---|---|
| R0 | manager's own, no test, no buffer (the CIO's belief) | 163.5 | 175 | s.5.3, s.5.6 |
| R1 | every candidate fitted once on the whole record: manager's own wins (5.6 per cent against 9.9), buffer at the end of the horizons | 183.4 | 200 | s.5.3, s.5.6 |
| R1p | fitted once, buffer on the path | 241.4 | 250 | s.5.3 |
| R2 | **the test as filed, age band wins (11.6 against 14.4 and 29.9), buffer read at the end of each horizon: 61,852** | 177.5 | 200 | s.5.6 (at any point in a horizon) |
| R3 | **the test as filed, buffer on the month-end path: 96,560** | **212.2** | **225** | |
| band, no buffer | s.5.6 ignored | 115.6 | 125 | s.5.6 |
| strategy and band, path buffer | the runner-up basis (24 per cent behind) with the right estimand | 224.9 | 225 | s.5.3 selection; lands on the answer at its edge |
| strategy and band, end-of-horizon buffer | two errors of opposite sign | 202.0 | 225 | s.5.3, s.5.6; lands on the answer 2.0 from the edge |
| band, leaky end-of-horizon buffer | right basis, buffer from a full-window fit | 156.5 | 175 | s.5.3, s.5.6 |

Every single-error path lands below the answer (200 or 175) or above it (250). The two cells that reach the answer tranche need the runner-up basis, which the test refuses by 24 per cent, and one of them a second error on top; they are the known Gate F exposure. Discriminator: the path buffer exceeds the end-of-horizon buffer by 34.7 million on the same basis, one tranche; the leaky winner's end-of-horizon buffer is 19,907 thousand.

## ORGANS

- **Validation record** (the calibration organ): the notice ledger and the register give, at each of the twelve origins, the funds on the register, their unfunded commitments and their realised monthly calls over the next twelve months; s.5.3 files origins, horizon, estimation window, population, error measure and tie rule once each, and s.5.6 files the buffer as the furthest realised calls ran ahead of the forecast at any point in a horizon.
- **Filed pins (RL-PM-04):** fund age from the first call; the bands; the three candidate bases (s.5.2); the walk-forward protocol (s.5.3); distributions (s.5.4); the plan buffer (s.5.6); the cap at unfunded commitment; the CHF 75 million reserve (s.3); the tranche rule (s.4); the ledger basis of unfunded commitment with the register's recycling clause (s.6.1) and its agreement to the audited cells (s.6.2); reporting conventions (s.7).
- **Licensed wrong basis:** the CIO (Hotz) argues in the minutes and the thread for each manager's own record estimated on everything on file (R0 and R1); the portfolio manager (Suter) expects little from the credit funds. Nobody argues for the age-band basis, the walk-forward or the path buffer.
- **Context artifact:** the register (static terms). The H1 2025 semi-annual report carries a correct NAV bridge for a closed period in the s.7 format and shares no figure with any ask.

## DETERMINISM CLOSURE (22 axes)

| # | Axis | Reading | Closed by |
|---|---|---|---|
| 1 | Population | at each origin and at the plan date, every fund admitted by that date; a fund without a call aged from the month after; no fund has a first call before its admission (asserted) | s.2, s.5.3 filed |
| 2 | Unit of account | unfunded commitment per fund in fund currency under s.6.1 with the register's recycling clause | filed; agrees 180 of 180 (asserted) |
| 3 | Attribution window | calls by notice month; cash views by value date | s.5.2, s.7.2 filed |
| 4 | As-of | 30 September 2026; origins at twelve quarter ends | s.2, s.5.3 filed |
| 5 | Version basis | ISSUED lines only | field notes |
| 6 | Denominator | commitments (pooled bases), the fund's own commitment (manager basis), realised calls (error) | s.5.2, s.5.3 filed |
| 7 | Weighting | ratio of sums at the window's last-day rate; manager basis as the fund's own mean | s.5.2 filed |
| 8 | Window length | January 2019 to the origin or plan date; twelve-month horizon | s.2, s.5.3 filed |
| 9 | Boundary inclusivity | estimation window includes the origin month; the reading that stops the month before selects the same basis and the same tranche (asserted) | s.5.3 filed, C1 |
| 10 | Rounding path | rates unrounded; CHF thousand after translation; errors as percentages to one decimal | s.5.1, s.5.5 filed; every graded figure at least 10 francs from a thousand boundary and every error at least 0.008 points from a one-decimal boundary (asserted) |
| 11 | Tie-break | lowest error, then fewest parameters; honest margins 24 and 158 per cent | s.5.3 filed |
| 12 | Maturity | no realisation straddles a year-end or an investment-period end | C1 asserted |
| 13 | Order of operations | schedule Q4 2026 first; cumulate from 1 January 2027; buffer as an amount added to the peak | s.4, s.5.1, s.5.6 filed |
| 14 | Buffer estimand | the furthest realised cumulative calls ran ahead of forecast cumulative calls at any month-end of a horizon, at the origin's rate | s.5.6 "at any point in a horizon"; the end-of-horizon reading is the designed wrong cell, one tranche below, and a share-of-forecast reading has no sentence to rest on |
| 15 | Duplicate resolution | reissued notices under their own number | field notes |
| 16 | Identity normalisation | currency case folded | field notes |
| 17 | Netting | in-specie lines in the distribution rates, out of the cash views | s.5.4, s.7.2 filed |
| 18 | Dimensional units | the origin's rate inside the test, the plan-date rate for the plan, value-date rates for cash | s.4, s.5.3, s.5.6, s.7.2 filed |
| 19 | Code semantics | line types per field notes | filed |
| 20 | Integerisation | none | n/a |
| 21 | Scope of a clause | s.5.3 governs any basis the plan runs on; s.5.6 the buffer | filed |
| 22 | Forward window | January to December 2027 | term sheet filed |

Fork cells computed and off the answer: reserve ignored 287.2 (300), one-half credit 100.2 (125), strategy basis without buffer 114.9 (125), in-sample manager basis with its end-of-horizon buffer 190.5 (200).

## ASK SHEET (device ledger)

Main-call row population: ISSUED notice lines (notice month, type, line type, investment_ref, amount), the register, the investment register, the FX rates of the twelve origin dates and the plan date, the audited NAVs, the directive. It never reads the NAV register, the value_date column, the FX history on other dates, in-specie lines as cash, or the H1 2025 report.

| Ask | Figures | Layer | Device | Enters the call as |
|---|---|---|---|---|
| A (coupled) | the twelve-origin test table (48 figures), three errors, three furthest-ahead amounts, the basis, the buffer, 12 months x 5, the tranche below, uncovered, fees, first month past | the construction's own outputs | none | the components of the call |
| B | NAV bridge, 5 x 5 | value-date flows, period-end FX | D3/D8: the register's ready `nav_chf_booked` at the booking-date rate against s.7.2's period-end rate; D4: three Q2 2026 statements absent, s.7.3 adjusts the Q1 value; D8: flows by value date | audit trail of the NAV the distribution forecast is struck on |
| C | 2026 cash, 9 x 3 | value-date cash at value-date FX | D8: notice-month and notice-date FX land every month elsewhere; in-specie line of 24 August and three withdrawn notices excluded | the realised baseline the plan is read against |

Pair arithmetic (planning weights 38/7/55): A carries about 75 of 125 criteria; one cracker missing the silent devices on B and C: about 45 + 55 x 0.60 = 78; the best non-cracker, on the end-of-horizon buffer, keeps the whole test table and the plan months and loses the buffer, the tranche and the appendices' devices: about 5 + 7 + 55 x 0.45 = 37; pair about 57. The build measures above the bar on paper because the client's rule 2 makes the test table and the plan the construction's own outputs, which a solver on the wrong buffer still gets; only the main ladder holding every response but one off the path buffer brings the pair down, and the portal is the measurement.

## PACK (13 files, 7 formats; spine 13083 lines)

kapitalabrufe_ausschuettungen_2015-2026.csv (spine) · fondsregister_2026-09-30.xlsx (register with the recycling clause) · beteiligungsverzeichnis_2026-09-30.csv · kapitalkonten_revidiert_2021-2025.xlsx · nav_register_quartal.csv · fx_referenzkurse_tagesende.csv · richtlinie_liquiditaet_privatmarkt_RL-PM-04.docx (governing) · term_sheet_lindenhof_standby_2027.pdf · stiftungsrat_protokoll_auszug_2026-09-24.pdf · halbjahresbericht_privatmarkt_2025-H1.pdf (context) · mail_standby_line_2027.txt (social) · feldbeschrieb_privatmarkt_extrakt.md (field notes) · export_manifest_2026-09-30.json.

## LEAK REVIEW (leak.py --asof 2026-09-30)

- The tranche figures in the term sheet: the lender's menu, which the prompt names as the candidate set.
- "180 rows" in the field notes and the thread: the row count of the audited workbook.
- Stump vocabulary (commitment, unfunded, notice, origin, basis, test, horizon) in the directive, the field notes, the minutes and the thread: the directive files the protocol, which is required; no sentence says that the end-of-horizon reading understates the exposure, and no document mentions the seasonality.
- Sweep 4 on the prompt: the ask names the directive's test, the bases, the errors and the buffer, the graded outputs in the client's own good-example form; no sentence says how the buffer is measured.
- Dates after 30 September 2026 in the register (investment-period and term ends, Halvorsen III's final close), the spine (October value dates of September notices) and the investment register (closing dates of September calls due in October): forward by nature.
- "ladder" in the minutes: the bond ladder the treasury sold.
- Container metadata scrubbed in both generators, producer "Pensionskasse Werdinsel" stamped 2026-10-01 on the pack and 2026-11-06 on the deliverables. The chart PNG keeps its Matplotlib text chunk: honest script output, H1 leaves outputs alone; its body states no date.

**Prompt form (author's instruction 2026-10-11).** One continuous paragraph with no backstory and nothing the pack states; the CIO's belief is carried by the minutes and the thread only; the crossing asks are worded conditionally so they presuppose nothing.

**Thinnest margin.** The runner-up basis with the path buffer lands on the answer tranche 0.1 million from its edge, and with the end-of-horizon buffer 2.0 million inside it; both need a basis the test refuses by 24 per cent. The answer itself sits 12.2 and 12.8 million from its edges.

## STOPPING RULE

Two consecutive plain-solver landings on CHF 225 million by the path-buffer route file the device as at ceiling and retire the slot. A landing by the intended route with the B and C devices missed licenses one device-layer repair. A miss licenses the next round.

## PORTAL LOG

- P1 (v2, 2026-10-11): two of two responses landed CHF 250 million by the filed walk-forward; the mechanics were in s.5.3 and were executed. Re-rooted to v3 (the buffer estimand).

## Tried and rejected

- v2 architecture (2026-10-11): the walk-forward selection with its mechanics filed in s.5.3 and the buffer as the largest end-of-horizon shortfall; both portal responses executed the filed test and landed CHF 250 million. Retired the same day: a validation whose mechanics are filed is a computation to a strong solver. v3 keeps the test and moves the deciding quantity to the buffer's estimand.
- Candidate set including a trailing twelve-month basis at v3: persistence won the honest test whenever recent vintages paced faster than history; left out.
- Seasonality at 1.35 to 0.65 (first half to second half): the path and end-of-horizon buffers sat 5 to 20 million apart, inside one tranche; set at about 70:30, which puts them 35 million apart.
- Seed sweep 118 to 149 under the sharper seasonality: nine seeds meet the honest margin, the leaky margin and the path separation; 118 kept (the persona draw's seed).
- Reserve at 50, 60 and 70 million with the 25-million menu: the fit-once path-buffer cell or the end-of-horizon cell sat within three million of the answer bin's edges; 75 million puts the answer 12 from both edges and every single-error cell at least 4 from them.
- v1 architecture (2026-10-10): the unfunded commitment restored by recallable proceeds under a term no document stated, pinned by reproducing 180 audited cells; retired 2026-10-11 under the client's 10/10 rules as data semantics and a hidden rule deciding the call (rule 3), and as a backdrop domain under the noun-swap (rule 1). The world, the pack and asks B and C were kept; the recycling term is now filed in the register and the stump moved into the validation.
- Candidate set with a trailing twelve-month basis: persistence won the honest test whenever the recent vintages paced faster than history and landed on the answer tranche; dropped, the three bases are band, strategy and band, manager's own.
- Strategy-coherent pacing shifts in the recent vintages: the strategy-and-band basis then won honestly by 11 per cent and the full-window fit tied the pooled bases, so the leak crowned nothing; replaced by manager-level and fund-year noise, under which the manager's-own basis memorises the past (full window 2.9 per cent against 6.0) and loses forward (17.2 against 9.1).
- Buffer as the second-largest shortfall: the truth and the leaky cell sat within three million of tranche edges at every reserve from 55 to 80; the largest shortfall with a CHF 60 million reserve puts the truth 10.8 and 39 from its edges and every wrong cell at least 4 from its own.
- Pooled rates as the mean of per-fund-month ratios: a fund in run-off with a small audited NAV and one large exit produced ratios above one and dominated the band; replaced by the ratio of sums at the plan-date rate (RL-PM-04 s.5.2, 5.3), which is also what a treasury would write.
- Estimator as rate on unfunded commitment (the Takahashi-Alexander form): the naive and true rates partly cancel because the naive denominator is smaller by the same recallables, and the Gate G label would have moved off binding_constraint; kept the cap form, where the construction is inert unless the cap bites, and built heterogeneous pacing so the recycling funds are the fast deployers whose cap bites.
- Uniform fast pacing: every fund fully drawn by month 24, the later age bands carried no history and the cap never bit under any construction (all constructions on one tranche); replaced by per-manager pacing (fast credit deployers, slower buyout and infrastructure).
- Distributions credited at one half: the programme's run-off distributions swamped the calls and the required facility sat at one tranche for every construction; the directive credits one quarter.
- Age bands 37 to 48 and 49 to 72: the recycling funds straddled the thin fourth band in 2027 and the band rate was too small for the restored commitment to matter; bands set to 37 to 54 and 55 to 78.
- The 2026 prepayment wave drawn from loans funded from January 2024: a third of the wave exited in 2025 and sat inside the audited cells, so the audited roll-forward reproduced most of the answer; the wave is drawn from loans funded in 2025 and exits in 2026 only.
- Short holds from the ordinary hold distribution: the normal draws put exits under eighteen months in half the funds, so commitment less calls missed 96 of 178 audited cells and was not the empirically excellent basis L7 requires; ordinary holds now start above the convergence gap and only the designed quick exits, the two historical flippers and the 2026 wave are short.
- Recallable proceeds attributed to the audited year by realisation date: an exit on 28 December with a January notice put the proceeds in different years under the two readings (one cell unreproduced); attributed by notice date, and no realisation now falls after the 15th of December.
- Reserve at CHF 30, 45 and 55 million: the truth or a wrong construction sat within five million of a tranche edge; CHF 65 million puts the truth 11.1 and 13.9 from its edges and the three wrong bases 8 to 15 from theirs.
- Producer string "Treasury & Liquidity" on the board paper's container: the raw ampersand broke the core-properties XML and the file no longer opened; the deliverables are stamped with the organisation's name.
- Context artifact as the H2 2025 semi-annual report (30 June to 31 December 2025): its closing NAV column is the opening column of ask B, five golden figures in a shipped document (leak.py LEAK); replaced by the H1 2025 report, which shares no figure with any ask.

- Signature rule / B / method_or_model_selection (any decision type): guard BLOCK, spent in 12 earlier builds (test.same_driver_older) and task71 (test.same_puzzle_older). Relabelled honestly: the forward regime is the decisive gap (time first) and the cap at remaining commitment is the Gate G mechanism (binding_constraint).
- Driver variant "late-close equalisation" (a midway entrant's first draw equals the process's draw-to-date on its own size): nearest driver task107 at 0.09, kept out because the catch-up is stated on every real notice and the rule reduces to a readable term.
- Driver variant "notices netted by some counterparties": kept out because the gross lines exist on the notice file and the move collapses to a file choice.
