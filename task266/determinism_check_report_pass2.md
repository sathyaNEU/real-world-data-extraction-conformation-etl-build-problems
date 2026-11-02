# determinism-check report (pass 2), task266, 2026-11-02

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (statistical_rigor), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Single re-judge after pass 1's FIX_NOW (ask 2 year length). Terms 3.2 now files "at 365.25 days to a year", which closes the fork; the member counts reproduce at 355 / 1,457 / 3,272 / 5,286 / 6,685 / 7,340. The main call is forced: terms 4.2, 4.4, the annual report's window (1 Jul 2004 to 30 Jun 2026) and the histories give one doubly truncated curve, 85.1% at 55 and 93.3% at 60, so the horizon is 60. Ask 3 (1,923 reviews, 14 towns) and 7,570 distinct members reproduce. Verdict thread: /tmp/determinism-check-task266-1793613603/verdict.md (one pass, no retry).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Stacked cases | 6,387 | 4,052 + 2,335 = 6,387, no duplicate refs | yes |
| Occupational, first exposed before 1986 | 5,271 | 5,271 | yes |
| Shares 40..70 | 32.1/53.9/72.4/85.1/93.3/97.4/99.1 | identical (EP NPMLE, 365.25) | yes |
| Ask 2 members 45..70 | 355/1,457/3,272/5,286/6,685/7,340 | identical | yes |
| Reviews per town / total | 14 towns, 1,923 | identical | yes |
| Distinct members reviewed | 7,570 | 7,570 | yes |

## Competing answers that survived
None that the shipped files leave open. Second readings and their figures:
- Estimator: naive 92.7% at 55 (files 55); left-truncation only 95.9% at 55; right-truncation only files 70. These are wrong methods, not readings of the estimand.
- Window end 30 Sep 2026: shares 32.8/54.9/73.4/85.9/93.7/97.6/99.2, call still 60. The annual report's sentence (diagnoses held to 30 June 2026) closes it. Judge flags it as the one place a careful solver can split on a printed figure.
- Year length 365 days: shares move at most 0.1; ask 2 365 days gives 348/1,443/3,253/5,276/6,679/7,334 (design note SF23); closed by terms 3.2.
- Town: published schedule gives Brinalong 215, Quillerton 291, Tarramore 191; contradicted on 24 days by card purchases and attendee homes.
- Review held: Attended only 1,724; Attended plus every MRU blank 2,173; QA images/2 on all days 1,948. The QA log fits only the golden rule (16 outage days vs 62 others).
- Members: fixed-site blanks counted 7,805 (362/1,501/3,378/5,452/6,899/7,566); Attended only 7,371 (345/1,420/3,181/5,144/6,511/7,146); all blanks 8,055 (370/1,556/3,496/5,631/7,126/7,810).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 13 / pdf, csv, xlsx | yes |
| Large file | 25,000+ rows | 48,839 (histories), 27,450 (appointments) | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | state cancer registry, workplace register 2024; names do not label them | yes |
| Distractors weigh but do not answer | yes | judge: carry no latency, rank no setting | yes |
| Deliverables | 1 to 3 | 2 (docx, xlsx), all in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes | yes |
| Prompt | one paragraph, under 1,000 chars | 772 chars | yes |
| Rubric 25+ criteria | 25+ | not checkable here (generated downstream); shape of 7 shares, 6 counts, 14 towns plus call supports it | not verified |
| Reads as real work product / not LLM | yes | judge found no provenance disclosure; golden-realism not re-run here | yes (judge) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata: declared distractors are the two named files; the note's No decoy line names them as carrying no latency. The thread names the naive and one-sided latency curves as the surface read, not a distractor. No mismatch, no too-load-bearing distractor.

## Gate H / stump power (Gate F)
Thread: domain pass, layers pass, decisive_step analytical (doubly truncated latency estimation, the field's own method; easy routes file 55 or 70). This agrees with the note's Three rules (No decoy, Not semantics, Not rule application) and its ladder (as it stands 55, delayed entry 55, reverse time 70, both edges 60). The note says no filed sentence names the window, truncation or estimator. Caveat for the main thread: the doubly truncated NPMLE is a textbook route, and the judge reached it by applying the method with the window read from the annual report, so a strong solver can land the call (stumping 1.3). Weigh this against the note's ladder; the judge rates stump power good.

## Findings, ranked
1. None blocking.
2. Optional: shares move 0.4 to 1.0 points if a solver takes 30 Sep 2026 as the window end; ask 1 could name the window in the workbook note.
3. Optional: Sites sheet label "circuit as scheduled" is mildly contrary to the card evidence; the data overrides it by a wide margin, left as realistic mess.

## Next action for the author
Proceed to ship; no rerun of the judge is needed.
