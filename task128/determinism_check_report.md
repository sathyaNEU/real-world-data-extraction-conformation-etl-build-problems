# determinism-check report, task128, 2026-10-10

## Verdict
NOT_DETERMINISTIC, plus SOLUTION_WRONG
**Disposition:** FIX_NOW
**Stumping type:** mechanism: binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

How this pass ran: this harness had no Agent tool, so the judge pass could not run in a spawned thread. It ran in the orchestrator's own context, with the isolation enforced by procedure instead.
- The bundle was copied fresh to `/tmp/determinism-check-task128-20261010T042304Z-16735/target/` (sha256-identical to `target/`; the folder has no `target.zip`).
- The judge standard was `guidelines/determinism_judge_system_prompt.md` v3, applied verbatim.
- Before the verdict was written to `verdict.md` in that scratch path, nothing in the task folder was opened except `prompt.md` and `submission.md`. The design note, `metadata.json` and `golden/` were opened afterwards, and only for the reconciliation and spec gates below.
- `generator/`, `solver_rounds/`, `pipeline.json` and the leak report were never opened. No server-side tool was used.
- One hygiene count in `verdict.md` was corrected on recount (pre-release runs that succeeded: 20, not 13). The verdict did not change.
- If you want a process-isolated confirmation, re-invoke from a session that has the Agent tool.

## Why
The main recommendation is forced and every main figure reproduces from the bundle:
- Payments 4, checkout 5, search 72, media 75, internal tools 77, data pipeline 67, taking out 13,300.
- The SRE s.2 headroom rule gives 24 drains per November window, and the same rule reproduces all 412 provider acknowledgements.
- All 48 historical colocated tickets ride exactly one change request and one window.
- Drained hosts come back clean.
- The cloud cut falls cleanly between data pipeline libjpeg-turbo8 (10) and search libunistring2 (9).

The task fails Gate C on a supplementary answer (competing_defensible_answer). Two search tickets, DEP-SEA-0051 and DEP-SEA-0079, carry a `vendor_first_release` equal to their package advisory's `latest_revision` in `vendor_advisory_feed.json`. The dictionary defines `latest_revision` as the republish date and `first_published` as "the vendor's first release of the fix", which is the prompt's own phrase. Measured from `first_published`, the estate card's search row reads 27.0 days with 8 over target, against the golden's 26.0 and 7.

A lighter Gate E fork sits on the cut list's cloud "hosts it reaches" (10 against 112 for rank 300).

Separately, SOLUTION_STEPS step 1 says the cut-day rule reproduces all 12 cells of the Q3 close-out. It does not (SOLUTION_WRONG).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Tickets per estate (main) | 4 / 5 / 72 / 75 / 77 / 67 | 4 / 5 / 72 / 75 / 77 / 67 | yes |
| Payments taken out | 1,410 | 1,412 (top 96 hosts by open exploitable findings; window sums 432 / 372 / 327 / 281) | yes |
| Checkout taken out | 1,740 | 1,742 (top 120; 434 / 372 / 338 / 310 / 288) | yes |
| Search taken out | 2,580 | 2,582 | yes |
| Media taken out | 2,650 | 2,652 | yes |
| Internal tools taken out | 2,430 | 2,432 | yes |
| Data pipeline taken out | 2,480 | 2,482 | yes |
| Total taken out | 13,300 | 13,302 (the rounded estates sum to 13,290) | yes |
| Drains per November window | 24 | 24 in all 9 windows. Payments: 460 - 417 - 40 = 3, x 8 cycles; checkout: 582 - 539 - 40 = 3, x 8. Peaks are 21,684 = 417 x 52 and 18,326 = 539 x 34, so ceil, floor and round agree | yes |
| Drain rule back-test | all 412 acknowledgements | 412 of 412 rows and 82 of 82 windows, in submission order. Whole-day-peak reading fails 13 windows. max_parallel_drains 7 never bound (72 windows ran 11) | yes |
| Hosts drained, payments / checkout | 96 / 120 | 96 / 120 | yes |
| One ticket per window | stated | 48 of 48 colocated tickets have one change_request, run only in its window, and log rows equal to hosts_accepted (8 part-accepted) | yes |
| Drain clears every finding | stated | 632 of 632 drained hosts have in_service_since equal to their last accepted window. 0 of 7,648 feed findings were first seen on or before it | yes |
| glibc as the colocated package | glibc | CVE-2026-24054 at 0.9712 is on all 216 drained hosts and is the top score in every window | yes |
| Exploitable rule, November | latest score of 0.10 or more | every CVE's last score is dated 2026-10-22; no live score sits between 0.099 and 0.101; all 7,648 feed findings score 0.161 or more | yes |
| Cloud cut | rank 291 is 10, rank 292 is 9 | 290 pairs at 11 or more, then pipeline libjpeg-turbo8 at 10 and search libunistring2 at 9, both unique | yes |
| Q3 close-out back-test (step 1) | all 12 cells reproduce | exact cut-day score gives 801 against 891 (126 rows have no score until after their cut date). Best reading found (cut day, else first score) gives 893, 7 of 12 cells. No as-of date, offset or threshold matches more than 7 | NO |
| november_ticket_cut.csv: ask 1 | 300 rows; ranks 1 to 9 the colocated glibc tickets at 24 hosts each (1,412 / 1,742); rank 300 pipeline libjpeg-turbo8, 10 hosts, 10 | same on the aggregates; the hosts column is contested (see below) | yes, hosts column contested |
| november_ticket_cut.csv: ask 2 | 4 / 5 / 72 / 75 / 77 / 67 | same | yes |
| ticket_split_review.pptx: ask 1 | split and exposures to the nearest ten, total 13,300 | same | yes |
| ticket_split_review.pptx: ask 2 | last in: data pipeline libjpeg-turbo8, 10 | same | yes |
| ticket_split_review.pptx: ask 3 | first out: search libunistring2, 9 | same | yes |
| ticket_split_review.pptx: ask 4 | open 2,462 / 2,682 / 2,627 / 2,539 / 4,688 / 2,960; annotated 120 and 96 hosts; 13,300 in the title | tools 2,462, media 2,682, search 2,627, pipeline 2,539, checkout 4,688, payments 2,960; 120 / 96; 13,300 | yes |
| ticket_split_review.pptx: ask 5 | 22.0/4, 24.0/3, 26.0/7, 24.0/1, 24.0/3, 23.0/0 | same on crew-log `vendor_first_release`, last succeeded run 1 May to 23 Oct, over target above 35 days | yes on the golden's reading; search row contested (27.0/8) |
| ticket_split_review.pptx: ask 6 | 610/99, 870/149, 361/49, 696/92 | same: running only, joined on instance_id, scan on or after 9 Oct. No scans fall on 8, 9 or 23 Oct; the findings file's scan dates agree on all 2,537 running hosts | yes |

## Competing answers that survived
1. **Estate card, search row: median days and tickets over target.**
   - The golden reads the crew log's `vendor_first_release` as given: 26.0 days, 7 over target.
   - The rival re-dates the two tickets whose recorded date equals the matching advisory's `latest_revision` to that advisory's `first_published`. For DEP-SEA-0079 (openssl) that is 2026-06-21, the date the checkout and tools openssl tickets recorded. For DEP-SEA-0051 (containerd) it is 2026-04-22. The tickets move from 16 to 37 days and from 36 to 57 days, giving 27.0 days and 8 over target.
   - The shipped rule meant to close the fork is the dictionary's definition of the two feed fields, plus the prompt's "a vendor's first release of a fix". Nothing says which source governs a ticket. The blanket package-level feed join is not a rival, because it produces 28 negative durations. The targeted correction stays defensible.
2. **Cut list, "the hosts it reaches" on cloud rows.**
   - The golden counts the hosts carrying the exploitable finding. Every cloud row has hosts equal to exposures, and rank 300 reaches 10 hosts.
   - Standard s.3 says a ticket "names the hosts that carry that package below its fixed version". On that reading every host with an open finding on the package is reached: 112 for data pipeline libjpeg-turbo8, and 33,985 across the 291 cloud rows. The exposures column is the same under both readings.

Rivals on the main call that did not survive, each defeated by a shipped fact:
- **Bulk on payments.** Payments has 4 windows, so any further payments ticket drains nothing.
- **One ticket per colocated estate spanning its windows** (1 / 1 / 74 / 77 / 79 / 68, 13,360). Defeated by one change request per ticket (crew log, 48 of 48) and one window per request (schedule s.3).
- **Each drain credited with its ticket's package only** (39 / 48 / 55 / 56 / 53 / 49). Defeated by the rebuild and the 24 host-slots per window.
- **No drain limit** (27 / 27 / 62 / 67 / 61 / 56). Defeated by SRE s.2 and the schedule.
- **Standby hosts left out of the cloud pool.** Not credited, because "in service" is defined only for scan coverage. It would leave the counts alone but tie ranks 291 and 292 at 9.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 23 | PASS |
| Distinct formats | 3 or more | 10 (csv, parquet, jsonl, xlsx, pdf, docx, json, yaml, md, eml) | PASS |
| Largest row count | 25,000+ rows or a large database file | `vuln_findings_2026-10-23.csv` 215,867; parquet 482,855 | PASS |
| Distractors declared | 2 or more in metadata.json, none labelled as such in target/ | 2: `drain_orchestrator_config.yaml` and `superseded_cvss_band_allocation_memo.pdf`. Nothing says "distractor". The memo's own file name and heading say "superseded" (its in-fiction status) | PASS, with a caution |
| Distractors unused yet relevant | unused by the solution, same world | Memo: PASS. Yaml: its max_parallel_drains value is unused and ruled out, but its `rebuild_from: current_platform_image` is the only explicit statement of the decisive rebuild in the bundle, and golden slide 1 repeats it ("comes back on the current platform image") | FAIL (yaml) |
| Distractor answers reproduce and are ruled out | arithmetic, plus a shipped fact against it | Memo shares give 54 / 51 / 48 / 60 / 36 / 51 = 300, ruled out by "superseded" and standard v3 "in force from the November 2026 round". Yaml 7 x 8 = 56 per window, ruled out by its own note and the 412-row back-test | PASS |
| Deliverable count | 1 to 3 | 2 | PASS |
| Format family | none required | csv and pptx | n/a |
| Asks multi-dimensional | not stacked lookups | The split, cut list, chart and card each span six estates or 300 rows. The card asks are lookups the dictionary pre-disarms | PASS (weak ask layer) |
| Golden deliverables present | every file the prompt names | `golden/november_ticket_cut.csv` (300 rows, counts match) and `golden/ticket_split_review.pptx` (3 slides, opens on the split, chart with the total in its title and the 120 / 96 annotations) | PASS |
| Units and rounding stated | every figure | The split says nearest ten; the card says one decimal place and whole numbers. The cut list's per-ticket hosts and exposures, and the last-in and first-out figures, carry no stated rounding. Read with the split's "nearest ten", 9 becomes 10 | FAIL (minor) |
| Prompt shape and the 25-criteria floor | identifiable shape, 25+ criteria | Shape 01, ranked list under a cap. About 48 separately gradable figures (split 13, line 4, chart 6, cut list 5, pace 12, coverage 8) | PASS |
| Realism | nothing reads as LLM generated; goldens are real work products | Pack tells (finding 8). The goldens read as edited work products | FAIL (pack), PASS (goldens) |

## Gate G reconciliation
**The four fields match.**
- Judge pass: binding_constraint / analytical_non_defect / no / no.
- Design note's Gate G line: binding_constraint over correct data / analytical_non_defect / no / no.

So the build reads as the same shape from outside as from inside, and Gate G carries little send-back risk. The judge pass did not name a declared distractor as the surface read carrying the task.

**Three places where the inside story does not hold from outside:**
1. **The method-selection support layer is missing.** The note claims "method_or_model_selection support (two rules recovered by back-test)" and has rung 1 recover the cut-day EPSS rule from the close-out. From outside, only the drain rule back-tests (412 of 412). The EPSS rule is stated outright in standard s.2 and the dictionary, and its back-test fails (801 against 891). Rung 1 is therefore a stated rule with a broken check, not a recovered method.
2. **The decisive fact is stated in a file.** The note's litmus calls the drain's full removal something "no file states". The declared distractor yaml states it (`rebuild_from: current_platform_image`), and the judge pass leaned on that line as corroboration. A distractor that carries the decisive rung is too load-bearing, and it pre-disarms measured trap #25 for any solver that reads the config.
3. **The ask-layer devices did not survive into the shipped pack.** The ask ledger's devices for ask A (republished advisories, UTC completion reports, superseded tickets) are mostly absent. The note's residual-risk line says the feed's revision dates "never enter the answer". The one remnant, two crew-log dates equal to an advisory's latest_revision, enters as a fork rather than a forced device.

The note also calls the decisive move a "G1 unit-of-value swap". A reviewer could read that wording as a lens swap (single_conceptual_flip). The judge pass did not, because no shipped artifact reports a per-package colocated value for the solver to reject, and the window capacity is what binds. It is still the phrase to keep out of anything a reviewer sees.

## Stump power (Gate F)
The main call holds. The decisive trap is the window-bound ticket together with the rebuild valuation. A strong model that finds the drain limit can still file one colocated ticket per estate (1 / 1 / 74 / 77 / 79 / 68) or credit each drain with one package, because the one-request-one-window rule is reachable only through the crew log's `change_request` column and schedule s.3.

Too-easy signals named:
- The planning thread names the drain limit and the rack hold.
- The yaml note says concurrency is set by headroom.
- The yaml states the rebuild outright.
- The dictionary hands out every supplementary correction: join on instance_id "stable across a rename", rolled_back "did not land", the exploit flag "not the office measure", the latest-score rule. The card and coverage asks therefore reduce to lookups that strong models will clear.

Optional lever, which needs a solver rerun: drop `rebuild_from` from the yaml, so the rebuild is only measurable from the in_service_since identity.

## Findings, ranked
1. **Gate C, estate card search row (blocks DETERMINISTIC).**
   - The problem: in `crew_deployment_log_2026.csv`, DEP-SEA-0051 and DEP-SEA-0079 carry `vendor_first_release` dates of 2026-05-13 and 2026-07-12. Those equal the containerd and openssl `latest_revision` in `vendor_advisory_feed.json`.
   - The fix: add a pin to `warehouse_data_dictionary.md` saying whether the crew log's date governs per ticket (the feed lists only each package's current advisory), or regenerate the two dates. If you rule the other way, restate the search row in `submission.md` and the deck as 27.0 days and 8 over target.
2. **Declared distractor carries the decisive rung.**
   - The problem: `drain_orchestrator_config.yaml` line `rebuild_from: current_platform_image` is the only explicit statement that a drain rebuilds the host, and golden slide 1 cites it.
   - The fix, either way round: strip the key (needs a solver rerun) and have slide 1 cite the in_service_since identity; or stop declaring the yaml a distractor and declare another file.
3. **SOLUTION_WRONG and integrity: the Q3 close-out does not recompute.**
   - The problem: `q3_2026_remediation_closeout.pdf` gives 891 and its 12 cells. `cloud_q3_closed_findings.csv` against the parquet gives 801 on the cut-day score, and no reading found matches more than 7 of 12 cells. Yet the dictionary says the figures "recompute ... against the score on each ticket's cut date", and step 1 claims all 12 reproduce.
   - The likely cause: the parquet's late-starting histories for 126 closed-finding CVEs.
   - The fix: find that cause in the generator and regenerate until 12 of 12 hold; or drop the claim from step 1 and the dictionary.
4. **Gate E, cloud hosts reached.**
   - The problem: standard s.3's "below its fixed version" also licenses every host with an open finding on the package (112, not 10, for rank 300).
   - The fix: pin the meaning in the dictionary or the prompt (the hosts carrying the finding the ticket is raised against), or grade only the exposures column on cloud rows.
5. **Integrity, crew log timing.** 24 runs on 7 tickets (20 of them succeeded) are dated before the ticket's `vendor_first_release`. For example, DEP-SEA-0069 ran on 2 and 3 May against a 4 May release. Dropping the 6 in-scope tickets moves four card medians. Fix the generator so no run precedes its release date.
6. **Units.** Add "as whole numbers" to the cut list's hosts and exposures and to the last-in and first-out figures in `prompt.md`. As written, the split's "nearest ten" can be read onto them, which turns 9 into 10.
7. **Distractor bookkeeping.** `vendor_advisory_feed.json` is used by no solution step and is not declared in `metadata.json`. It is the source of finding 1. Either declare it, with a shipped fact ruling it out per ticket, or make it the governing source.
8. **Hygiene (none stump-affecting).**
   - `extract_provenance_2026-10-23.md` says "This folder is a constructed case ... built for this case". Keep the source, date and licence, and drop the disclosure.
   - Every PDF and the docx carry an identical 2026-10-23 00:00 UTC creation stamp, including the close-out "prepared 7 October".
   - The docx `app.xml` records 0 words.
   - `cloud_q3_closed_findings.csv` gives every row its own CVE (1,240 CVEs for 1,240 rows), unlike the live export.
   - The acknowledgements accept the same host twice in one window (404 host-slots).
   - The planning email has a stray phrase: "I will bring one rate and the list".
9. **Rubric caution.** The colocated per-ticket values in the golden cut list depend on an unforced host-to-window split, and ranks 3 and 4 tie at 372. Grade only the estate sums and the 24-host reach on those rows.
10. **Not run here.** The cross-batch fingerprint, because other task folders are out of bounds for the judge.

## Next action for the author
Make the in-house edit pass that closes the verdict, then re-invoke the rehearsal (pass 2):
- In `warehouse_data_dictionary.md`, pin crew-log `vendor_first_release` as the per-ticket first release, noting that the feed carries only each package's current advisory.
- In the same file, define a cloud ticket's hosts as the hosts carrying the finding it is raised against.
- In `submission.md`, rewrite step 1 without the 12-cell close-out claim.
