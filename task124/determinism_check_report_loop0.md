# Determinism check, task124

Stage 4 judge run, 2026-10-12: one isolated thread at medium effort on a fresh unzip of the stage 3 cut, the prompt,
the submission's graded blocks and the judge's system prompt. Its verdict follows verbatim, between the rules; the
disposition after it records the repair. The re-judge on the repaired cut is the main session's.

---

# Verdict, task124

**Verdict:** NOT_DETERMINISTIC (main recommendation; supplementary asks 1 to 3 reproduce).

**Disposition:** SEND_BACK. The deciding estimator (which verifications estimate the lead share of Lead Status Unknown lines) is not forced by any shipped text, so the filed record needs a closing fact or the prompt/plan needs a pin, which changes what solvers see and needs a rerun.

**Why:** Plan rev 2 s4.3 says only "the share of lead or GRR expected among Lead Status Unknown lines of its construction era". No shipped file says how verification digs were chosen, that 78 segments were swept whole, or that the other digs were evidence-prompted. Read literally, the plain estimator is the lead share among field-verified, no-tap-card, pre-1989 lines of each era (0.763 / 0.585 / 0.217). That gives 12.82 programme years, RZ-06 in 2039, $347.5M, i.e. NOT finished before the deadline. The golden's 0.556 / 0.316 / 0.083 (78 whole segments) gives 2037, the opposite yes/no. Gate C / E fork, label underspecified_objective (the sampling frame is an unfiled method choice that flips the main call).

Why the data only partly rescue it: segment coverage is bimodal (78 segments at 100%, max 0.42 for all others), and partial-segment shares are far higher in every era (0.842/0.668/0.254 vs 0.556/0.316/0.083, same zones and eras). A careful analyst can see the two frames disagree. But nothing in the files says which frame is unselected. Segment-level tap-card covariates do NOT expose the selection: a stratified model (era x segment tap-card share) gives 12.86 years, 2039. Only recognising the complete-segment structure leads to 2037. That is an insight, not a filed or forced method, and the 2039 reading is equally "literal".

## Evidence (recomputed)
| Item | Result | Source |
|---|---|---|
| Latest verification per line, joined (CIS premise zero-padded to 8 digits via crosswalk, codes via result_codes) | 6,446 lines; all joined; 4,911 no tap card, built 1930-1988 or earlier (yb>0, <1989) | verifications, crosswalk, codes, inventory |
| Whole-segment shares (78 segments, no-tap-card lines) | 0.5556 (440/792), 0.3158 (96/304), 0.0833 (14/168) reproduce | same |
| Same using first verification or all rows | identical (whole-segment lines verified once) | same |
| Shares over all verifications | 0.7625, 0.5847, 0.2168 reproduce | same |
| Plan cost, whole shares | $284.67M, 10.504 years; zone costs, lines (rounded) and finish years all match golden table (cum. years 0.851, 2.136, 3.235, 4.136, 5.174, 6.231, 7.22, 7.781, 8.529, 9.346, 9.824, 10.504) | inventory, unit_cost_schedule, plan 4.2-5.4, CIP 27.1 |
| Alternatives | all-verified shares: 12.82 yrs, 2039; pooled whole-seg share 0.435: 12.09 yrs; whole segments incl. tap-card lines: 11.38 yrs (2038); stratified model: 12.86 yrs | recomputed |
| Ask 2 payments | latest closing by closed_on, ET quarter, COs added once, per contract: reproduces golden exactly (LSL-01 13890/13494/13416/13673; LSL-02 14509/13937/13903/13568; LSL-03 14488/14459/15008/14784). Quarter counts 135/195/315/127 match the progress report | completions, CO log, contracts |
| Ask 3 agreements | distinct lines with SIGNED form, premise via crosswalk, inventory zone: reproduces all 12 counts (857, 1217, 626, 954, 889, 539, 975, 663, 1017, 368, 1118, 518); zone_on_form differs on 171 forms | agreements, crosswalk, inventory |

Secondary forks (ask 2, smaller): (a) first closing instead of the RECLOSED row changes 5 sites and moves 6 of 12 cells by $2 to $37 (e.g. LSL-02 Q1 14,485, LSL-03 Q1 14,451); the export note says the reclose is a correction, so latest is the better reading but "latest" is not stated as the payment rule. (b) Whether "paid" includes change-order amounts is not stated in the prompt; co_amount sits in the completions export and the CO log is "approved", so inclusion is likely but not pinned. (c) Ask 3 relies on inventory zone, not the form's zone; the plan text shipped does not mention the boundary redraw, but the inventory is the current record. None of these flips a qualitative call.

## Files/Hygiene
PASS. 16 files; formats csv, pdf, docx, xlsx, md (5). Large file 87,410 rows (inventory). Two distractors present and unused: lcr_tap_samples_2025_2026.csv, ami_meter_exchanges_2023_2025.csv. Dates coherent (plan 20 Oct 2026, unit costs 2 Nov 2026, CIP draft 14 Dec 2026, progress report 6 Jan 2027, extract 8 Jan 2027, last verification 18 Dec 2026). The field-notes .md reads like a data-dictionary and states file grains; plausible as a GIS hand-off. No authoring or synthetic disclosures found. No exclusion-level finding.

## Stump power
If the fork were closed, the all-verifications share (2039) is the natural wrong answer for a strong model that cleans the data and reads the plan; most will take the plain estimator, so stump is likely high, but the divergence is currently an estimator-choice fork, not a provable error, so it cannot be credited as a valid stump.

## Stumping type
mechanism: statistical_rigor (selection in the verification sample, estimand/frame choice); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. No reported figure is wrong; the difficulty is choosing the unbiased sampling frame, which passes Gate G once it is a filed, forced choice.

## Three rules
domain: pass, layers: pass, decisive_step: analytical. Field analysis: estimating the lead share of unknown lines (inventory validation) and the schedule it drives; Layer 1 is the CIS to WMS migration (padded premise numbers, code tables per recording route, UTC vs Eastern, reclosings, change orders repeated per site); Layer 2 is the unbiased estimate of the unknown-line share. Easy route: pool every verification by era, giving 2039 (not finished by 1 Nov 2037); golden gives 2037.

## Fix
Where: input_files / prompt (plus solution blocks after). Close the fork with a filed, non-leaking fact that makes the frame forced, for example a QA or verification-programme record stating how digs were scheduled (complete-segment validation sweeps vs customer/complaint-prompted digs) or a plan 4.3 sentence naming the estimation sample (lines verified in segments where every service line was verified). Alternatively pin the estimator in the plan's own words. Also state in the plan/notes that a reclosed work order's payment replaces the first and that change orders are part of what a contractor is paid. Then rerun; golden figures stay unchanged if the pin selects the whole-segment frame.

---

## Disposition

FIX_NOW in substance (the fork is closed in the record, the call and every graded figure frozen), committed PAUSED
for the main session's re-judge. The fork was closed by filing a fact the record lacked, never the estimator: which
verifications estimate the share stays the solver's step.

1. **Main call (Gate C/E, `underspecified_objective`).** The field notes for `sl_field_verifications_2021_2026.csv`
   now carry the extract's own account of how lines come to be verified: "Lines come to be verified in one of two
   ways. When a water main is replaced under the distribution system renewal programme (from 2023), every service on
   the replaced main is exposed and its material recorded before it is reconnected. Every other row is a visit to a
   single line, raised by a customer reporting lead or galvanized pipe or asking for a check, a leak on the service, a
   lead and copper sampling site (2021 and 2022) or the 2024 consultant ranking of services likely to be lead (2024
   and 2025)." It names no share, sample, segment, coverage or method (asserted, S1 and S6), and every clause is true
   of every row (W3). With it, pooling every verification (0.763, 0.585, 0.217, last zone 2039) keeps the visits'
   selection and the 78 whole segments (the replaced mains, known by complete coverage) give 0.556, 0.316, 0.083 and
   2037 (SF15, asserted).
2. **A rival the filing would have exposed.** Under plan 4.3's earlier wording ("expected among Lead Status Unknown
   lines") the share among the lines the single-line visits left unverified (0.497, 0.279, 0.075) is a coherent
   estimate once the selection is filed: last zone 2037, but five zones a year earlier and $10.4 million less. Plan
   4.3 now reads "at the share of lead or GRR expected among the district's lines of its construction era that have
   no usable tap card", a class the whole segments estimate exactly: known results plus the left-unverified share for
   the rest return 0.556, 0.316 and 0.083 (SF16, asserted in `checks.py` and `verify.py`); known results with the
   whole-segment share for the rest (0.601, 0.348, 0.091) counts the selection back in (SF17).
3. **Ask 2 secondary forks.** (a) The field notes' `row_status` now ends "and the reclosing's paid amounts replace the
   first closing's" (paying on the first closing moves 5 of 12 figures, A10). (b) The change order log's header now
   reads "Approved change orders, paid to the contractor on its pay applications. Each change order is entered once,
   with the sites it covers." (leaving change orders out moves all 12 figures by $25 or more, A11); no filed sentence
   says how a change order counts against its sites, so ask A's device is untouched (A11).
4. **Ask 3 secondary fork.** The field notes define the inventory's `zone` as "the line's replacement zone under plan
   revision 2"; no rule counts agreements by either zone, since a filed rule would adjudicate ask B's device (B7).
5. **Realism tells (the reader's list).** Change order approvals are backed off weekends and district holidays (the
   25 December approval is now 23 December, R8); each change order entry is worded on its own (45 of 45 distinct,
   R3); the unit cost schedule states its system rates ($12,400 and $2,390) and each zone's rate basis (R9). The
   unit costs themselves, the ids and the 87,410-row inventory are unchanged, since moving them moves graded figures.
   The prompt is unchanged: voice-check passes it, and every reading of "the November 2037 deadline" gives the same
   call because the plan files 1 November 2037 and the 31 October season close (SF6).

**Scope.** Four pack files changed (the plan, the field notes, the change order log, the unit cost schedule); every
data file is byte-identical to the stage 3 cut. No graded figure moved: `figures.json` is byte-identical,
`freeze.py check --mode determinism` passes, and the goldens changed in prose only (plan 4.3's wording and the visit
reasons). Submission: Critical Component 1's label follows plan 4.3, and step 2 cites the field notes.

**Gates on the repaired cut.** `checks.py` 108 assertions, 0 failed (SF1 to SF17, S1 to S6, W1 to W3, A1 to A11,
B1 to B7, R1 to R9); `verify.py` green on its own parser, the SF16 and SF17 rivals included; two builds
byte-identical; `figures_check.py` exit 0 (76 figures); `precut.py` exit 0 (38 checks, 17 fork rows); voice-check
PASS; `leak.py` REVIEW, no LEAK; `guard.py surface` 0 promoted, `heart` WARN (`repeat.gate_g`, answered in the draw).

**Next.** Re-judge on a fresh cut (the main session), and the leak reader again, since four documents changed. If the
re-judge finds a fork convergence cannot close, the design note's stopping rule applies: re-root, never pin the
estimator.
