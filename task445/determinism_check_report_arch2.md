# determinism-check report, task445 (architecture 2), 2026-11-01

Target.zip sha256 b103f21fb2366d0eb3a4b1dfb1a89bfacc834456706c6c0f1c4b30352b3c18b2. Judge thread verdict: /tmp/determinism-check-task445-1793491098/verdict.md. Architecture 1 reports are not read or overwritten. prompt.txt (not the legacy prompt.md).

## Verdict
NOT_DETERMINISTIC (supplementary answer 5 only; the main recommendation, the CSV and supplementary 2 to 4 are forced), plus SOLUTION_WRONG (Final Recommendation prose on Ashwold).
**Disposition:** SEND_BACK
**Stumping type:** mechanism: other (cross-source reconciliation of unregistered deaths), stumping_family: surface_read_rejection (borderline), surface_read_dependency: yes (borderline), sole_data_defect: yes
**Gate H:** domain: pass, layers: pass for Layer 1 and Layer 2 missing, decisive_step: rule_application. H3 fails.

## Why
1. Supplementary 5 rests on an unfiled convention: the golden takes the latest version's fields with version 1's registration date. Nothing shipped defines "version", and "the entry as it now stands" read literally gives a different answer (underspecified_objective).
2. The Final Recommendation prose contradicts itself: it designates Ashwold, then says that completed with the earlier summers' share Ashwold "reads 6.3 per cent and is left out". The scorecard, the critical components and the terms (section 4, "whether or not it has been registered") all qualify Ashwold at 13.1 (SOLUTION_WRONG as written).
3. The main call is forced and reproduced. The decisive step is executing the filed counting rule through a match and dedup across three sources, which is rule application (Gate H3).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Register rows, versions (key district + entry number) | 81,590; v1 79,507; v2 2,083 | same | yes |
| Summer 2026 register v1 residents' deaths | not claimed | 3,068 | n/a |
| Deaths / expected / excess, six places | 891/828/7.6; 666/589/13.1; 345/304/13.5; 409/383/6.8; 595/528/12.7; 364/345/5.5 | same | yes |
| Unregistered, found only in logs | 60, 72, 15, 21, 20, 14 = 202 | same | yes |
| Ellesmoor | 3,270, 9.8 per cent over Table 1 (2,977) | 9.84 | yes |
| Monthly CSV (Jun/Jul/Aug) | per submission | same, all six places | yes |
| Scrutiny by quarter 2025-26 | North 1,924/1,812/2,170/2,183; South 1,454/1,349/1,713/1,633 | same | yes (first vs last completion identical; UTC shifts no case) |
| Supplementary 5 shares | golden convention | reproduces only under latest fields + v1 registration date | conditional, see fork |

## Competing answers that survived
- **Supplementary 5, version convention.** Moorbridge Q1 to Q4: golden (latest fields, v1 registration date) 61.7/60.9/59.9/65.5; all version 1 58.8/58.9/56.8/63.4; latest version wholesale 53.1/55.5/51.4/58.2. Thornley Vale Q1: 63.9 / 61.1 / 55.8. No shipped rule closes it. Fix: file the registration date convention (date of first registration, other fields as the entry now stands), a WHAT pin that moves no main figure.
- Scrutiny merge by shared coroner reference is a cleaning inference not filed (person-only merge gives North Q1 1,940), but the pairs are plain duplicates; noted, not a fork the thread counted against the verdict.
- Gross-up by earlier summers' share (Ashwold 6.3) and register-only (594 vs 589) contradict the filed "whether or not registered" rule, so they are wrong routes, not forks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or large DB | 81,590-row register | yes |
| Distractors | 2 or more in metadata.json, none labelled in file name | 4 named (population estimates, temperature, heat alerts, care homes); no file name labels one | yes |
| Distractors unused but weighable | yes | unused by solution; none answers a graded quantity (judge saw none as surface read); not separately stress-tested by me | yes (thread-based) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | place x quarter/month grids; prompt states per cent to one decimal, whole counts | yes |
| Prompt shape, 25 or more criteria | identifiable, 25+ | shape 10; criteria count is generated at rubric time, grids supply well over 25 cells | yes (not counted) |
| Not LLM-generated; goldens read as work products | yes | judge saw no disclosure; realism not re-judged by me. The self-contradicting Ashwold sentence reads as drafted, not as a work product | no, fix the sentence |

## Gate G reconciliation
Thread: mechanism other (cross-source reconciliation), stumping_family surface_read_rejection (borderline), surface_read_dependency yes (borderline), sole_data_defect yes. Design note and card: strategy maturity_censoring, Gate G etl_conformance, the stump is the completion-by-earlier-share route (Ashwold 6.3) overturned by the log match (Ashwold 13.1). The thread's surface read (register incomplete, find the missing deaths in the logs) matches the design note's decisive step. No declared distractor is named as the surface read, so the distractors are not too load-bearing. Mismatch is on strength, not identity: the note calls the completion the "field's own step" that fails; the thread finds that route contradicts the filed rule, so it is not a landable wrong route for a strong reader.

## Gate H reconciliation
Design note claims Layer 2 (completion vs data's real structure), Not semantics and Not rule application. Thread: Layer 2 missing, decisive_step rule_application, since the terms state "whether or not it has been registered" and executing that through the match and dedup lands the golden. This is the mismatch that reliably predicts a send-back, and it is the CLAUDE.md rule 3 ban. The note's own "Not rule application" line leans on the terms never saying how to find the deaths, but finding them by joining logs to the register is execution of a filed rule once the join is read.

## Stump power (Gate F)
Moderate to low per the thread. A strong model that reads the terms looks beyond the register. Routes that fail: register-only count, gross-up. Name-variant duplicates, versions, UTC, terminated postcodes are Layer 1. Thread lever: make the deciding quantity a modelled one (for example a registration-delay completion validated out of sample that the terms do not make literal) while keeping the filed WHAT. The completion route is the textbook method (stumping 1.3), and here the filed text dismisses it, so the main thread must weigh whether any step is left that a capable analyst gets wrong while reading every rule correctly.

## Findings, ranked
1. Gate H3 fails: decisive step is rule application; Layer 2 absent (rebuild around an analytical step).
2. Supplementary 5 version convention unfiled (underspecified_objective).
3. Final Recommendation prose on Ashwold contradicts the golden (SOLUTION_WRONG).
4. Scrutiny merge rule unfiled (minor, plain duplicates).
5. Cross-batch reference check could not run inside the allow-list.

## Next action for the author
Re-root the decisive step so the filed WHAT leaves an analytical choice the data must settle (Gate H3), and in the same pass pin the registration-date convention for supplementary 5 and rewrite the last sentence of the Final Recommendation, then rebuild byte-identically and re-judge once.
