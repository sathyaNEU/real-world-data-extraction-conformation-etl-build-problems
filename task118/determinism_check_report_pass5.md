# determinism-check report (re-judge after /fix-determinism), task118, 2026-10-27

Numbering note: determinism_check_report_pass2.md, _pass3.md and _pass4.md already exist and were not touched; this file is the next free pass (pass5).

## Status
PREPARED, JUDGE NOT YET RUN. The runtime has no Agent tool. The brief is at /tmp/determinism-check-task118-r5/judge_brief.md (fresh unzip in /tmp/determinism-check-task118-r5/target/, 19 files). Verdict, Disposition, ledger and Gate G/H reconciliation below are to be completed from /tmp/determinism-check-task118-r5/verdict.md after the thread returns. Sections here are what I could settle without the thread.

## Verdict
PENDING (thread not run).

## Competing answers that survived
Pending thread. Author-side read of the two portal forks against shipped text:
- Under-test hours: headline_squad_2027_placement_brief.pdf now says "Clicks in those hours count at the winning headline's lift." A mixture-rate reading (750,000 / 800,000) contradicts that sentence directly; it is quotable and closes the fork.
- "Going live": cms_revisions_export_fields.txt status field now says "A save recorded live publishes the document, and a scheduled revision publishes it at its publish_at; the document first went live when it was first published either way." That closes "first live save" for scheduled articles.
- publish_at clock: field note says "On a scheduled revision, the time the editor set ... Brisbane time", while saved_at is "UTC". Closes the clock. Residual risk: the +10 hour offset is not stated as a number in the pack (AEST is named for published_date and the scope, Brisbane has no DST); the judge may call this world knowledge. Flag to see whether the thread treats it as an open fork.

## Spec gates (own check, partial)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 19 | yes |
| Formats | 3+ | csv, xlsx, pdf, parquet, md, txt, eml, docx | yes |
| Large file | 25,000+ rows | parquet 2,324,291 rows; CMS csv 266,633 | yes |
| Distractors, deliverables, rubric count, LLM-read | see metadata.json / thread | not completed before the thread | pending |

## Counter-pin sweep (own read of all prose files: brief, CMS field notes, field reference, standards s7, bulletin, syndication agreement, eml, dashboard export, export log, desk register)
No shipped sentence found that reads against the committed answer. Checked specifically: the dashboard's avg_winning_lift_pct is a different, labelled quantity (reported winning lift, not the shrunk lift) and the field reference defines winning lift consistently with it; standards 7.4 ("logged on the revision that publishes the corrected headline") agrees with the same-save/ten-minute rule; 7.5 agrees with live-blog entries counting; the brief's "counted at the owning desk from each article's publication" agrees with the owning-desk basis. Thread to confirm independently.

## Stump power (Gate F), author-side, plainly
The committed desk is reachable by a fairly ordinary route. I computed from the pack: own-surface clicks on articles with no test, times each desk's raw mean lift (controls counted as zero) gives Sport·metro 2.76M, Culture·national 1.56M, Local·metro 1.08M, Business 0.82M, Sport·national 0.76M, Politics 0.62M. So an analyst who (a) restricts to own surfaces, (b) removes already-tested articles, and (c) simply distrusts Sport·metro's 10.8% raw mean from 150 small tests lands on Culture·national without any shrinkage machinery. What stops them: only the Sport·metro raw-lift lure, which is easy to distrust, and the two layers (own-surface, untested) which are domain-standard. Readers-led (Politics) and dashboard-lift-times-plan (Sport·metro 11.3M, Business 7.2M) routes fail. Consistent with both portal judges' own responses reaching Culture. The exact committed figures (1.25M, 450k gap) need the shrunk lift, but the desk does not. Reported, not blocking; the stump is frozen.

## Next action for the author
Spawn the thread with the prompt returned to the main session, then re-invoke determinism-judge with /tmp/determinism-check-task118-r5/verdict.md to finish this report (ledger, Gate G/H reconciliation after reading the design note).
