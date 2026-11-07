# leak check, task272

**Verdict: REVIEW.** 12 files read, 75 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: weighed, register, tolerance, golden, family, weights, litres, reader, architecture, spread, hospital, calendar, pumped, capability, reflex, pooled, volume, percent, points, outside, checks, application, readers, determinations, distribution

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `PH-QP-07_batch_compounded_products_policy.pdf`: golden figure 100 appears: ...its out-of-tolerance doses made in that year per 100,000 of its doses made in that year. The year is...
- **REVIEW** `PH-QP-07_batch_compounded_products_policy.pdf`: golden figure 3.1 appears: ...l time. 3. Gravimetric verification of every dose 3.1 At each configuration of the pharmacy's IV workfl...
- **REVIEW** `SC-SOP-12_batch_compounding_procedure.pdf`: golden figure 3.1 appears: ...s are in the compounded product master. 3. Set-up 3.1 Install the set, prime it with the product's sour...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `PH-QP-07_batch_compounded_products_policy.pdf`: 7 of 25 stump-paragraph terms appear (weighed, register, tolerance, calendar, volume, outside); read whether the document names the move
- **REVIEW** `SC-SOP-12_batch_compounding_procedure.pdf`: 7 of 25 stump-paragraph terms appear (weighed, register, tolerance, hospital, volume, outside); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 37% of 196 prompts (cap 30%); reword at the role level, not the verb

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 3, read 1 on target.zip 81176264 (isolated Sonnet reader, a fresh copy of prompt.txt and target/ only).

1. Decisive step: none stated; the nearest is PH-QP-07 sections 2 and 3.1 (a product filled on PC-1 to PC-4 is
   configured where its out-of-tolerance rate in the last full calendar year exceeded 10 per 100,000 doses made),
   which name the estimand, not the step; nothing says doses must be placed on their sets' pumped litres or that the
   unweighed doses need estimating.
2. Ranking file: none; the master's weighed-every-dose column restates policy 3.2, and per-dose verdicts exist only
   for the gravimetric compounder's doses and the sampled checks.
3. Helping file: none; the product master and the equipment register are reference tables, the two PDFs governing
   documents, the email the request.
4. Answer figure or name: none; the master's tolerances, specific gravities and tares are inputs.
5. Population sentences: PH-QP-07 sections 2 and 3.1 (each product's completed doses made in Ontario's calendar 2026,
   out of tolerance whether or not weighed or quarantined, per 100,000 doses made, over 10 configured) and SC-SOP-12
   section 4.2 (delivered volume as net weight over specific gravity); their literal result is the golden's
   population.
6. What decides: an analytical choice, estimating out-of-tolerance across every dose made, the unweighed majority
   included, rather than reading the sampled check results; not field semantics, a stated procedure or a planted
   defect (the registers' gross and net weight columns are layout mess).

Sweep lines: PH-QP-07's and SC-SOP-12's words (weighed, register, tolerance, volume, outside) name no way to estimate
the unweighed doses and no set-wear effect, harmless; the 24-hour set reuse and the bag products' fresh set-up say
what a set is, not what to configure, harmless; the gravimetric dose weights hold only the two GC-1 products, all
in tolerance, harmless.

Realism: the PDFs carry a named author and plausible dates, the workbooks different authors, the quarantine register
recount rows, the check register varying initials, the equipment register a PC-3 serial swap on 14 July; the sorts'
100 quarantined and 100 weighed match the SOP's sampling interval.
