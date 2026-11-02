# determinism-check report, task266, 2026-11-02

## Verdict
NOT_DETERMINISTIC (workbook ask 2 only; main call, ask 1 and ask 3 forced and reproduced)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Ask 2 counts members with "fewer years than [the setting] since first exposure on 1 July 2027". The year length is not filed for this use: terms 4.3 files 365.25 days for a mesothelioma's latency only, and terms 3.2 gives no convention. The golden (355 / 1,457 / 3,272 / 5,286 / 6,685 / 7,340) holds only under 365.25 days. Label: underspecified_objective on supplementary 2. The design note's fork SF6 closes year length for the latency, and SF20 closes "fewer than" but not the year length of the member count, so the fork table has a gap here. Everything else is forced. The main call at 60 follows from terms 4.2 ("whenever it is diagnosed"), 4.4 and the annual report's coverage sentences. Mid-run provenance: judge thread verdict at /tmp/determinism-check-task266-1793612332/verdict.md (single pass, no retry).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Register cases stacked | 6,387 | 4,052 csv + 2,335 xlsx = 6,387, no duplicate refs | yes |
| Occupational, first exposed before 1 Jan 1986 | 5,271 | 5,271 (any-job first exposure would give 5,516, closed by terms 2.2) | yes |
| Shares 40/45/50/55/60/65/70 | 32.1/53.9/72.4/85.1/93.3/97.4/99.1 | same, doubly truncated NPMLE, window 1 Jul 2004 to 30 Jun 2026 | yes |
| Horizon | 60 | 60 | yes |
| Reviews across circuit towns | 1,923 | 1,923; per-town table equals golden | yes |
| Distinct members reviewed | 7,570 | 7,570 | yes |
| Members under 45/50/55/60/65/70 | 355/1,457/3,272/5,286/6,685/7,340 | same at 365.25 days only | yes, under one year length |

## Competing answers that survived
- **Ask 2, year length (the open fork).** Members with fewer years than 45/50/55/60/65/70:
  - 365.25 days (golden): 355 / 1,457 / 3,272 / 5,286 / 6,685 / 7,340
  - 365.2425 days: 354 / 1,457 / 3,272 / 5,286 / 6,685 / 7,340
  - completed calendar years: 354 / 1,455 / 3,271 / 5,286 / 6,685 / 7,340
  - 365 days: 348 / 1,443 / 3,253 / 5,276 / 6,679 / 7,334
  No shipped sentence closes it for the member count.
- **Ask 3 and ask 2, what a review held is (closed by data, not by text).** Text is silent. The QA log counter and the fixed-site DNA-versus-blank convention force the golden for an expert who reads the log. Second readings: attended-only gives 1,724 reviews (Fenalong 66, Haskesford 44, Ostlebury 51, Pellandra 70, Strathowie 67, Wennobank 36) and 7,371 members (345 / 1,420 / 3,181 / 5,144 / 6,511 / 7,146). Attended plus all blanks gives 2,173 reviews and 7,805 members (362 / 1,501 / 3,378 / 5,452 / 6,899 / 7,566), contradicted by the blank/DNA convention.
- **Ask 3, town.** Published-schedule towns differ for eight towns (Brinalong 215, Corrinbar 301, Quillerton 291, Tarramore 191, Garrock 100, Kellowie 100, Dorrabee 112, Lathardine 80). Closed by the card statement's midday purchases (11:30 to 14:00); any purchase of the day gives the same towns.
- **Main call, closed.** Year of 365 days moves the first three shares by 0.1 (32.0 / 53.8 / 72.3), call unchanged. Window end at the 30 Sep 2026 register close gives 32.8 / 54.9 / 73.5 / 85.9 / 93.7, call still 60, and the annual report ("holds every mesothelioma diagnosed to 30 June 2026") closes it. Window start 30 Jun 2004 or end 1 Jul 2026 changes nothing at one decimal.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, rows | 10+ files, 3+ formats, 25,000+ rows in a file | 13 files, csv/xlsx/pdf, histories 48,839 rows, bookings 27,450 | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | 2 named (state cancer registry xlsx, workplace register csv), neither labelled in a file name; the judge also noted the road-distances workbook as unused | yes |
| Distractors unused, relevant, ruled out by a shipped fact | yes | judge found no latency in either; deletion-tested per design note | yes |
| 1 to 3 deliverables, all in the golden | yes | 2 (docx, xlsx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | share to one decimal, whole-number counts stated in the prompt | yes |
| Prompt shape, rubric 25+ criteria | yes | prompt 772 chars, one paragraph; the rubric is generated and not shipped, so 25+ is not checked here (7 shares, 6 settings, 14 towns plus the call give ample cells) | not checkable, likely |
| Nothing reads as LLM generated, goldens business-realistic | yes | judge found no authoring leakage, layer-1 mess authentic; golden realism not reviewed by this pass | judge: yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; analyst_test names the delayed-entry curve (95.9% at 55, files 55) against the doubly truncated estimate (85.1% / 93.3%); design note names the same. Match. The declared distractors are not named as the surface read carrying the task, so they are not too load-bearing. Gate G passes.
**Gate H:** domain pass, layers pass, decisive_step analytical. Matches the card's domain_test (latency distribution under a register's two-sided truncation) and the note's `## Three rules`. Note that the doubly truncated NPMLE is the field's standard method for this data, and the golden is reached only by applying it, with the empirical share (92.7% at 55) and left-truncation alone (55) and right-truncation alone (70) all landing elsewhere, so it is a real analytical stump rather than a landable textbook route.

## Stump power (Gate F)
Good. The route a strong solver takes from the terms (empirical share or delayed entry) files 55; only the two-sided estimator files 60. The asks add card-statement town reconstruction and QA-counter blank-row recovery with no stated rule, hard for a legitimate reason. Residual risk: the prompt never says "truncation", supplied by terms 4.2 and the annual report coverage.

## Findings, ranked
1. Ask 2 year length unfiled for the member count (three cells move under completed years: 45, 50, 55; four under 365 days, all six cells). FIX_NOW.
2. Fork table gap: SF6 and SF20 do not cover the member count's year length. Add the row once pinned and assert it in checks.py.
3. "Review held" is closed only by reading the QA log, not by a sentence. The judge counts this as acceptable; optional pin.

## Next action for the author
Pin ask 2's year length with one sentence in terms 3.2 (preferred, same 365.25-day convention as terms 4.3, golden stays frozen) or restate ask 2 as completed years and re-key 45/50/55 to 354 / 1,455 / 3,271. Add the SF row, rebuild twice byte-identical, and re-judge once. Main call, ask 1, ask 3 and the stump stay frozen.
