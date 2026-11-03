# determinism-check report, task200, pass 2, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pass 2 judged the rebuilt bundle (fresh unzip at /tmp/determinism-check-task200-r2/target/, 17 files) against the updated submission blocks. The one value that moved since pass 1 is Dene screen time, now 4,593.8 (unrounded 4,593.785). Pass 1 had 4,593.7 (4,593.74). The rebuild also moved the rounding margin from 0.011 h to 0.035 h.

## Why
The judge derived every value independently from the bundle before comparing, and everything reproduced. The order Fell, Brook, Dene, Esk, Arden, Cleve is the first-meeting hit share, which is the reading SPS-04 4.2's "least likely to find" calls for. It holds under cancelled-as-met, team at time of projection, team-level exposure and class-mix standardisation. The gaps are 6.4 points at the top and at least 3.4 elsewhere. The exposure gradient is visible in the data: Fell's hit share by prior meetings (0 to 5) is 62.8, 76.9, 86.3, 88.1, 90.1 and 90.5.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fell first-meeting rate | 63% (707/1,125) | 62.84% | yes |
| Brook / Dene / Esk / Arden / Cleve first-meeting | 69 / 74 / 77 / 81 / 85 | 69.24 / 73.73 / 77.15 / 80.85 / 84.93 | yes |
| Fell repeats | 4,104 of 5,229, 84% | same, 84.3% | yes |
| Overall rate Brook / Fell | 71 / 80 | 71.3 / 79.7 | yes |
| Screen time h (Arden, Brook, Cleve, Dene, Esk, Fell) | 5,168.8; 4,750.9; 5,545.6; 4,593.8; 5,297.1; 4,603.7 | 5,168.815; 4,750.902; 5,545.590; 4,593.785; 5,297.090; 4,603.704 | yes (nearest edge 0.035 h: Arden .815, Dene .785) |
| Clear searches | 6,608; 4,399; 6,737; 6,429; 11,915; 5,683 | identical | yes |
| Expiring certificates | 4; 2; 3; 2; 5; 3 | identical (nearest expiries 22 Jun and 9 Jul 2027, no boundary case) | yes |
| Order | Fell, Brook, Dene, Esk, Arden, Cleve | same | yes |

## Competing answers that survived
1. First-meeting restriction (main call). The literal reading of 4.2 plus the section 3 hit/miss definition gives the overall hit share: Brook, Dene, Esk, Fell, Arden, Cleve. The judge ruled the first-meeting reading licensed, not open: it is the field's estimand for detecting a threat not yet seen, and the exposure gradient is in the data. A literal reader who ignores exposure files Brook first, and the judge calls that residual real.
2. History truncation. If "already met" is built from the 2026 file only, Fell's first-meeting share is 77.2% and Brook (70.8%) goes first. Using all shipped history is the data-forced reading but is not stated.
3. Pier B screen-time close (Fell only). No shipped document says how a log-on without a log-off ends. The golden uses next log-on or shutdown (4,603.7). Capping at 20 minutes (SPS-04 5.1) gives 4,522.7. Explicit log-offs only gives 2,476.2. The judge ranks the cap weak because it needs an invented 20-minute close, but it is the one supplementary figure with a live alternative.
4. Closed by a filed rule or by the data: the union of overlapping CT rows (raw sum double counts), the NF to CLEAR vocabulary (inferable), two-tray records as two searches (SPS-04 section 3), the 31 December roster team (SPS-04 section 3), and the certificates (EXT-IIC keyed date gives 3/0/1/1/3/2; omitting the 2 unkeyed centre certificates gives Dene 3; the centre list is shipped and joins cleanly).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, xlsx, docx, pdf, eml) | yes |
| Large file | 25,000 rows or more | 121,884 (CT sessions); 50,436 (search log, pass 1) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 (lane throughput, queue time, compliance PDF), unlabelled in names; judge: unused, the PDF scopes out image interpretation | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-team across six teams; hours to one decimal; counts | yes |
| Prompt shape and 25 criteria | identifiable shape, 25 or more | shape 06; the criteria count is not verifiable by me | unverified |
| Realism | not LLM generated | judge found nothing exclusion-level; the Pier B banner dated 15/01/2027 is after the 12 Jan email, which is trivial | yes |

## Gate G reconciliation
The thread's Gate G line is statistical_rigor / analytical_non_defect / surface_read_dependency no / sole_data_defect no, as in pass 1. It matches the design note's `## Three rules` (read after the thread returned): the pooled projection score and d-prime are the easy routes, with no decoy and no ranking artifact. No declared distractor carries the surface read, and the naive overall rate is built by the solver, not reported. The judge notes a borderline lens-swap flavour, but the repeat gradient is structural and survives clean data. No mismatch.
**Gate G class:** clean.
**Gate H:** domain: pass, layers: pass, decisive_step: analytical. Layer 1 is UTC and local time, overlapping sessions, the tray split, badge replacement, LMS against centre certificate dates, and the vocabulary change. Layer 2 is the exposure-aware estimand. A strong analyst who read every rule would still file Brook first by the overall share. The first-meeting restriction is an estimand choice, not a data-semantics reading or rule application.

## Stump power (Gate F)
Moderate to good. The solver has to think of image memory and rebuild per-operator history across three CT years and the Pier B log. A strong solver who tests for exposure effects lands the call by the standard method. This is a landable call (library `stumping` 1.3), and the main thread should weigh it against the design note's ladder. The asks add heavy reconstruction (session union, UTC conversion, two-tray split, badge history, unkeyed certificates), so a solver off the call still loses a lot there.

## Findings, ranked
1. The first-meeting restriction is not stated anywhere; the literal overall-score reading gives Brook first. The judge ruled it licensed. This is a residual, not a fail.
2. History truncation (2026-only "already met") flips the call to Brook, because the 2024 and 2025 exports are not named as required.
3. The Pier B open-session close is the one ask with a live alternative (4,522.7 with the 20-minute cap). Fell only. The judge's optional fix is one line in SPS-04 section 3.
4. Rounding: the nearest edge is 0.035 h (Arden .815, Dene .785), so Dene is safer than in pass 1. First-meeting percents are at least 0.34 point from a .5 edge.
5. Not assessed: the cross-batch fingerprint and the 25-criteria count.

## Next action for the author
Nothing is required to ship on the determinism gate. If you want the ask pinned, add one line to SPS-04 section 3 giving how an unclosed Pier B session ends. Do not file the first-meeting method itself, since that would turn the decisive step into rule application.
