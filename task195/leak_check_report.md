# leak check, task195

**Verdict: REVIEW.** 19 files read, 32 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: paired, specimen, asserted, difference, estimate, verdict, nothing, decisive, comparison, sentence, estimator, uncertainty, window, laboratory, accepted, cutoffs, method, intervals, population, golden, corpus, parallel, closed, protocol, two-sample

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `method_validation_protocol_kval07.pdf`: carries 8 of 10 distinctive words of the committed call: 'Replace the contamination screen in service with the re-run mixture-fraction screen at the 0.030 cutoff for the quarter '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `extraction_platform_validation_2025.pdf`: 3 of 25 stump-paragraph terms appear (specimen, laboratory, method); read whether the document names the move
- **REVIEW** `method_validation_protocol_kval07.pdf`: 12 of 25 stump-paragraph terms appear (specimen, verdict, comparison, estimator, window, laboratory); read whether the document names the move
- **REVIEW** `mixture_estimator_model_card_v34.pdf`: 6 of 25 stump-paragraph terms appear (specimen, estimate, estimator, laboratory, accepted, cutoffs); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


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
