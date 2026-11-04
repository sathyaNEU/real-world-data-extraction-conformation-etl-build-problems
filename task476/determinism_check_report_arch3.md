# determinism-check report, task476 (architecture 3), 2026-11-04

## Verdict
DETERMINISTIC on the main call. The thread's SOLUTION_WRONG on memo ask 3 (energy charges) is **not sustained**: I recomputed it independently and the golden reproduces (see the diagnosis below). Open pins remain on graded depths and one graded one-decimal figure.
**Disposition:** FIX_NOW, limited to filing pins (no golden figure moves, no model rerun). Not a SEND_BACK.
**Stumping type:** mechanism: ETL conformation with an estimation step (energy to volume at the interval's head), stumping_family: method_model_selection, surface_read_dependency: no, sole_data_defect: no

## Why
The thread executed the shipped text literally and reached the golden on the call. The metered wells give 3,270 AF. The eleven unmetered wells, converted interval by interval at 1.0241 x total head over efficiency with the logger's mean depth moving the head, give 12,313 AF. The ranch is 15,583 AF, 224 over the 15,358.9 available, and the notice's whole 50 AF blocks give 250. Every reading variant of the level pairing gives 15,583 to 15,590, so the purchase holds at 250. The test-rate route (15,021, 337 inside) and the other wrong routes all file no purchase. The thread's failure on ask 3 is its own recomputation error, not a defect of the pack.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Metered total (W-01..W-04) | 3,270 | 3,270 | yes |
| Unmetered total | 12,313 | 12,313.4 | yes |
| Ranch | 15,583 | 15,583 | yes |
| Available | 15,358.9 | 15,358.9 from the parcel rows; printed total row 14879.0 | yes by rows, fork by printed total (closed by the whole-number rule, below) |
| Purchase | 250 | 250 under every variant | yes |
| Static depths | 30 values | 10 of 15 wells exact; W-04, W-05, W-07, W-08, W-15 differ 0.1 to 0.3 ft under the thread's first-pass rule | partial, see residuals |
| Energy charges (15) | 62,185 etc. | thread: 61,350 etc. (1.2 to 1.4 per cent low). Me, independent pandas: W-01 62,185.32, W-02 59,204.59, W-05 65,315.58, W-10 175,837.00, W-15 172,136.78 | **yes (my recompute), thread's figure is wrong** |

## Competing answers that survived
- Allocation total: printed 14879.0 against rows summing to 14878.9. Taken as the printed total, available is 15,359.0 and "224 over" is unchanged. The prompt asks acre-feet as whole numbers, so both readings file 15,359, and the gap closes on graded whole-number figures. It remains only a one-decimal figure in the golden text, and SF6 does not record it.
- Levelogger 5 clock (W-01 to W-04): the files carry no time zone, while the TROLL files state PST with no daylight saving. SF11 says "each as its header states", which is false for these four files. Reading them as UTC moves W-01 spring to 138.7, W-02 spring to 119.9 and W-03 fall to 148.2. **Open on graded depths.**
- 24-hour pump-off rule: the note's fork table has no row. The golden's reading is the literal one (off since the end of the last interval that drew energy, at 15-minute resolution). The thread's 0.1 to 0.3 ft differences on five depths come from its own hour-boundary test. **Open until a row is filed and the five depths are asserted in checks.py.**
- SWL against PWL as the head reference: the thread gets 11,420 AF (no purchase) by using the standing level. The test reports' definition (TDH = pumping level + discharge head + column loss) closes it, but the fork table has no row for it (SF14 covers only the datum).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 45 | yes |
| Formats | 3 or more | pdf 21, csv 22, xlsx 2 | yes |
| Large file | 25,000 rows or more | levels CSVs 40,908 rows; interval export 308,220 rows | yes |
| Distractors | 2 or more named, none labelled by file name | district deliveries and weather named in `metadata.json`; file names do not label them | yes |
| Distractors unused and weighable | unused; a fact rules out | surface-water deliveries (the notice counts groundwater) and ET; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding stated | 15 wells x months, depths, charges; the prompt's last sentence gives units and rounding | yes |
| Prompt | one paragraph, under 1,000 characters, no count of data | 764 characters, no data count | yes |
| Rubric 25 or more | generated | 15 wells x (volume, monthly, spring, fall, charge) clears it by construction (not verified from the portal rubric) | yes |
| Reads as real | no LLM tells; goldens read as work products | no authoring language found by the thread; I did not re-sweep the goldens | yes with note |

## Gate G reconciliation
The thread's family is method_model_selection with no surface-read dependency and no sole data defect. The card says `stump_class: analytical`, strategy decomposition_attribution, and its analyst_test names the same default path (test kWh/AF, 15,020, 339 inside) against the interval-head conversion (15,583, 224 over). The thread's easy route, 15,021 with 337 inside, matches the card within 2 AF. The thread did not name either declared distractor as the surface read, so neither is too load-bearing. No mismatch. Gate G passes.

Gate H, thread's line: domain pass, layers pass, decisive_step analytical. This matches the note's `## Three rules` (Layer 1 mess of units, clocks and renumbering; Layer 2 the field's energy-based method done at the interval's head). It agrees with the design note.

## Stump power (Gate F)
Strong on paper, with one caution. The conversion relation (kWh/AF = 1.0241 x TDH / efficiency, TDH defined from the pumping level) is printed on every test report, and the loggers carry the pumping level hourly, so a strong solver who reads the report carefully can land the call. The thread reached it by applying that relation with no further judgment the data had to settle, and the design note itself says the calculation the records support is the golden's. That is a landable call (library methods are textbook routes, `stumping` 1.3). The back-test on the metered wells confirms the easy route within 1.5 per cent, which helps keep it from being discovered by validation. The main thread should weigh this against the ladder. The decision band of 15,559 to 15,609 AF is narrow, so the 0.5 per cent ranch band (about 78 AF) is wider than the margin; a response inside it can still file 200 or 300 AF. The band is a grading choice, not a shipped rule.

## Energy-charge diagnosis
The source of the thread's 1.2 to 1.4 per cent shortfall is **not the generator**. `golden.energy_charges` prices each 15-minute interval in the register's schedule, AG-2T before 1 June for the agreements the letter moves, with the bundle's period function and the PDF's rates. I re-implemented it from the shipped files only, in pandas, with local time, 3 July as the observed 4 July, Memorial and Labor Day, summer from 1 June and the letter's agreements: W-01 62,185.32, W-02 59,204.59, W-05 65,315.58, W-10 175,837.00 and W-15 172,136.78, each equal to the golden to the dollar. The generator's `world.tou_period` and `bundle.period` agree to the cent on W-01. The PDF text, rates and the letter match what the generator parses. The thread's flat ratio is a computing error on its side (cause not identified; a window or interval-count slip would be flat across schedules). No regeneration of the 15 charges is warranted.

## Findings, ranked
1. Levelogger 5 files (W-01 to W-04) carry no stated clock zone; SF11 claims they do. Four wells' depths depend on it. Open on graded figures.
2. 24-hour pump-off rule has no fork row; five depths unverified to 0.1 ft by the thread. Open until asserted.
3. Allocation total printed 14879.0 against rows 14878.9; closed on whole-number figures by the prompt, open only on "15,358.9".
4. SWL/PWL head reference has no fork row; closed by the reports' TDH definition but not text-pinned.
5. The note's ladder header reads "Against 15,519 available"; the correct figure is 15,358.9 (the inside and over amounts already use it). A stale label.
6. Ask 3 SOLUTION_WRONG from the thread: overturned by independent recompute.

## Next action for the author
Fix list, in one pass, no golden figure moves:
- State the Levelogger 5 clock in the download log or the file headers as PST with no daylight saving, to match the TROLL headers, then assert it in checks.py.
- Print the notice total as 14878.9 (or add SF6 as `same call` at whole acre-feet) and fix the ladder's 15,519 label.
- Add fork rows for the 24-hour pump-off boundary and the PWL reference, asserted in checks.py; confirm the five depths (W-04, W-05, W-07, W-08, W-15) at 0.1 ft.
- Leave the 15 energy charges as they are. Rebuild twice, rerun the free gates, and re-judge once, per the FIX_NOW rule.
