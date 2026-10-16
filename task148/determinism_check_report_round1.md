Judged pack: commit 027f6ff (architecture 2 as first built, before the stage 4 hardening of the late shift's patience and the ask pins); the hardened pack has not been re-judged.

# Verdict, task148 (fresh judge pass)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Every committed figure reproduced from the shipped files, so no repair is required and no rerun. Two small optional pins are listed under Fix.

**Why:** The main call (July 2027, August 2027, June 2028 short of the 90 per cent standard with four call-takers) reproduces exactly from the shipped files. It uses SOP 2.10 sections 3.3, 4.2, 5 and 6, the FY2028 board forecast and the 417,086 calls from the legacy ACD plus the i3 log. Within the abandonment-aware queue family the month set does not move over the reasonable range of busy time (225 to 231 s) and patience (150 to 184 s). The only readings that change the set are ones the data rejects as methods: Erlang C (May to September short) and patience read off the hang-ups' own waits (no month short). No taxonomy failure applies (none).

## Evidence (recomputed from target/)
| Item | Golden | Mine | Source |
|---|---|---|---|
| Non-test 911 calls (acd 77,385 ANS + 1,007 ABN; i3 332,050 + 6,644) | 417,086 | 417,086 | acd csv + i3 jsonl, test dropped, i3 UTC to Central |
| Abandoned calls | 7,651 | 7,651 | same |
| Busy time, answered to Ready | 227.0 s | 227.0 s | same |
| Patience, total wait of all calls / abandons | 161.4 s | 161.35 s | same. This is the exponential-patience MLE with answered waits as censored. The abandoned calls' own mean wait is 45.6 s. |
| Erlang A (M/M/4+M), SOP 3.3 compliance, nights weighted by Fri/Sat count, forecast row of the starting month | 88, 89, 91, 93, 94, 93, 94, 95, 94, 93, 91, 89 | 88.07, 88.91, 91.11, 92.96, 94.05, 92.88, 94.02, 94.94, 94.09, 92.90, 91.04, 88.97 | FY2028 sheet, Tavish rows, Fri 22/23, Sat 00/01, Sat 22/23, Sun 00/01 |
| Same without night weights | | 88.07, 88.91, 91.11, 92.96, 94.05, 92.82, 94.06, 94.94, 94.05, 92.95, 91.04, 88.89 | rounds to the same whole per cents |
| Erlang C | May to Sep short | 83.6, 85.0, 88.3, 91.0, ..., 88.2, 85.0 (May, Sep and Jun-Aug short) | consistent with the golden's note |
| Own-wait patience (45.6 s) | no month short | 90.8 to 95.9, none short | consistent |
| Sensitivity: busy 231 s with patience 183.5 s | | May 90.41, Sep 90.48, Jun 88.21, Aug 88.15, Jul 87.24 | set unchanged. Whole-per-cent values would shift by at most 1 at the extreme corner. |
| Observed FY2026 whole-floor compliance (SOP 3.3) | 95.2 | 95.24 | back-test target reproduces |
| Back-test with H1-2025 busy and patience and the roster, per hour | A 95.3, C 93.7, own-wait 96.4 | A 94.7, C 92.7, own-wait 96.0 against 95.2 observed | direction and ordering reproduce. My simplified replication separates A from own-wait only weakly (0.5 against 0.7 away), so the golden's sharper separation depends on its implementation. |
| Halvorsen reached, by fiscal 2026 quarter | 1,473 / 1,249 / 1,104 / 1,265 | same | che records located at the last (equal to smallest-radius) fix, point-in-polygon on the MultiPolygon with its hole, joined to i3 by callId, Central quarters |
| Halvorsen transferred to Wexley | 1,304 / 1,126 / 1,001 / 1,154 | same | transferTo is the Wexley primary URI plus alt07@bkp.state911 (Wexley's alternate per the PSAP directory). The primary URI alone gives 1,153 / 994 / 881 / 1,015. |
| Callback within 2 min, Jan to Jun 2026 | 54.9, 55.3, 51.4, 53.6, 48.3, 51.6 | same | Denominator is all abandoned 911 calls, misdials included (SOP 7.1). Numerator is the first dial after the hang-up to that number (callback_desk number to i3 callbackRef). 71 repeat abandons have no task of their own and are covered by the open task. A task-keyed-only read gives 49.8, 52.5, 48.2, 50.9, 46.4, 48.0. |

Other checks:
- The cutover split is clean: no wireline ACD rows after 16 May and no wireless/VoIP ACD rows after 13 May.
- Busy time is homogeneous across transferred-out, transferred-in and Halvorsen calls (about 226 to 237 s), so the pooled 227 s does not misstate the new Halvorsen load.
- The task rests on SOP 5.1 (the forecast as planning basis), so the forecast's Halvorsen column is taken as filed.

## Competing answers stress-tested
- Erlang C (the textbook model): May to Sep short. It overstates shortfall because callers hang up; rejected by the back-test (2.5 points under observed) and by the filed definition of the data.
- Erlang A with patience = mean abandoned wait: no month short. It is biased because it ignores the answered calls' waits as censored holds. The golden's estimator is the standard exponential MLE.
- FY2026 observed late-shift compliance (about 99 per cent): it ran with five call-takers and no Halvorsen load. Not applicable.
- Night weighting, month-start attribution (SOP 6.1), 4 call-takers (budget PDF): no effect on the set or the rounded values.

## Files/Hygiene: PASS
- 14 files (more than 10).
- Formats: csv (8), jsonl, xlsx, pdf (2), geojson, md.
- Row gates: i3 has 340k rows and the legacy ACD 78k.
- Distractors: admin_line_acd, cad_incidents, esinet directory. qa_extract_log and the README read as an export manifest. Counts in qa_extract_log match (78,758 / 340,059 / 3,829 / 39,486 / 4,565 / 6,241 / 35,036).
- No authoring or benchmark disclosure found. The `.example` domains are placeholder-style.
- Dates are coherent: pulled 6 October 2026, budget draft 2 October 2026, forecast published 15 September 2026.
- Not exclusion-level.

## Stump power
The trap that does the work is the abandonment-aware queue with patience estimated under censoring: the unit of analysis is the call, not the hang-up. A strong model plausibly reaches for Erlang C (May to September short, wrong) or estimates patience from the abandoned callers' own waits (no month short, wrong). Both are specific, data-refuted wrong answers. The back-test in the files lets a careful analyst separate them, though only moderately in my replication. Likely strong-model failure rate is high but not 100 per cent. The supplementary asks add independent, hard ETL layers: refined-location selection, MultiPolygon with hole, alternate-URI mapping, repeat-abandon callback linkage.

## Stumping type
`mechanism: method_or_model_selection` (with statistical_rigor on censored patience), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Reported numbers are fine and clean data would still stump. The difficulty is choosing and calibrating the queue model, not rejecting a misleading figure. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- Layer 1: UTC against Central, legacy ACD against i3 layouts, cutover overlap, test calls, transfers in and out, pseudonymised keys.
- Layer 2: abandonment-aware Erlang A with patience from a censoring-aware estimate, validated out of sample, applied to a forecast of a changed demand.
- Domain: staffing a PSAP floor to an answer-time standard is workforce-queueing work the field does. Swap test: "visits" or "hospital" nouns would not preserve the Erlang A with call-abandonment framing.
- Easy route: a strong analyst who read everything correctly applies Erlang C, or reads patience from the hang-ups' own waits. Erlang C gives May, June, July, August and September short (five months). The own-wait read gives no month short. The filed answer is three months.

## Fix: none required (optional, solution or prompt, no rerun)
1. If the author wants the asks tighter: the located Halvorsen calls rely on taking the last/most precise location record. The README gives the radius field but no stated rule. A first (cell) reading gives 1,568 / 1,329 / 1,188 / 1,445 reached. State in the prompt that a call's location is its most precise fix, or accept the risk. This is a pin on the asks, which are free of the main call.
2. The callback ask depends on joining desk numbers to i3 `callbackRef` (`cb-` + lower-case pseudonym) to cover repeat abandons. The README says the pseudonym is consistent across files, so it is reachable, but an optional README sentence would reduce risk.
