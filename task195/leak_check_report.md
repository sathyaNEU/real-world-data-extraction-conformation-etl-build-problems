# leak check, task195

**Verdict: REVIEW.** 17 files read, 32 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: paired, specimen, asserted, difference, estimate, verdict, nothing, decisive, comparison, sentence, estimator, uncertainty, window, laboratory, accepted, cutoffs, method, intervals, population, golden, corpus, parallel, closed, protocol, two-sample

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `method_validation_protocol_kval07.pdf`: carries 8 of 10 distinctive words of the committed call: 'Replace the contamination screen in service with the re-run mixture-fraction screen at the 0.030 cutoff for the quarter '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `extraction_platform_validation_2025.pdf`: 3 of 25 stump-paragraph terms appear (specimen, laboratory, method); read whether the document names the move
- **REVIEW** `method_validation_protocol_kval07.pdf`: 12 of 25 stump-paragraph terms appear (specimen, verdict, comparison, estimator, window, laboratory); read whether the document names the move
- **REVIEW** `mixture_estimator_model_card_v34.pdf`: 6 of 25 stump-paragraph terms appear (specimen, estimate, estimator, laboratory, accepted, cutoffs); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 30% of 196 prompts (cap 30%); reword at the role level, not the verb

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read, wave 6 audit (the shipped pack, target.zip 4dc5342a)

Run as part of an audit of every shipped build, because `leak.py` overwrote this build's original
reader section before that bug was fixed, so no reader evidence survived. The reader held only a
fresh unzip of the pack and `prompt.txt`, and was scored key by key against `generator/figures.json`
by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | figures answered | hit | share |
|---|---|---|---|
| main call | 1 | **1** | the reader landed it |
| ask figures | 30 | **26** | 86.7 per cent |

It committed to the 0.030 cutoff, which is the shipped call, at about 70 per cent confidence, and it
named the decisive step in its own words: the interval on a paired design, because the two screens
score the same specimens.

### How it got there, which is the part to fix

It read the route off a filed sentence. Clause 3.4 of the validation protocol says **"Detection is
counted per specimen"**, and the reader quoted that as what told it the design is paired. It then
computed both branches and reported them: paired methods give 0.030 and unpaired methods give 0.015,
with all paired variants agreeing and all unpaired variants agreeing. So the decisive choice is a
clean two-way fork that one shipped sentence resolves, which is readability screen test 1, a filed
sentence naming the decisive quantity.

The author's earlier paper argument for this build was that the variance structure is forced by the
data and nowhere filed. That argument was wrong twice over: the reader found the sentence that
points at it, and reached the golden in one pass.

### Realism findings it volunteered

The weekly-reports PDF footer states the double-count mechanism outright ("where a report is
re-sent, the week's count includes the results sent again"). The model card's "where a share falls
relative to any screening cutoff is KVAL-07's matter" reads as a pointed handoff. The extract
dictionary defines each troublesome field one by one, more helpfully than a real LIMS dictionary.
The dilution panel's mixed-case level labels and its "Replicates reported: 28" against 27 rows read
as tidy planted mess.

## Solver's-eye read, reship cut (no describing file), 2026-10-31

Reader: one isolated general-purpose agent (sonnet, medium) on fresh copies of `prompt.txt` and `target/` after the
reship dropped the extract dictionary and the export manifest. It read all 17 files and solved nothing.

1. Decisive step: KVAL-07 4.1 is quoted as the decision rule; the reader notes that "the interval method is not named,
   and the 95 per cent test could be done several ways". No sentence names the estimator.
2. Ranking or scoring file: none (Table 2 lists the cutoffs only).
3. Helper-only file: none; the Panel notes sheet and the re-run config's notes read as the laboratory's own record.
4. Answer-like figure or name: none.
5. Literal sentence: KVAL-07 3.1 to 3.5, 4.1 and 5.2 give the population and the rule; the interval's construction
   is left open, which is the design.
6. What decides: the reader calls it "rule application, with a possible analytical element in the interval". Settled
   against the judge (pass 2, Gate H analytical): the easy routes recomputed on the clean truth (`checks.py` R3a) hold
   the change on overlapping per-screen intervals and file 0.015 on an unpaired two-sample interval; only the paired
   difference on the same specimens files 0.030, so the step that decides is the estimator the design forces, not
   the execution of 4.1.

Realism notes: the run log's control threshold reads near-constant; the PDFs share one producer, empty authors and
round creation times, and the model card's and weekly reports' creation dates precede their own last entries. Open
for the ask-layer pass.
