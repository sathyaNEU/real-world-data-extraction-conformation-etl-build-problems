# Determinism check, task270 (architecture 8)

Run 2026-10-27, stage 4 of /build: the determinism-judge agent prepared the brief (/tmp/determinism-check-task270-133558/judge_brief.md, the system prompt inlined verbatim, KEY_ASSUMPTIONS empty) and the main session spawned the one isolated thread (general-purpose, sonnet, medium) on a fresh unzip of target.zip dc5e15f6ea0ab486. The thread's verdict.md follows verbatim. Outcome: NOT_DETERMINISTIC, SEND_BACK; Gate G planted_defect_flip (surface_read_rejection), Gate H decisive_step data_semantics. Architecture 8 is spent; the build re-roots at the draw (architecture 9).

---

# Determinism verdict: task270 (Statin Adherence Support Service tiers)

**Verdict:** NOT_DETERMINISTIC. The main call and the tier table are forced and reproduce. Supplementary asks 5 and 6 (the pilot workbook) are not forced, so Gate C/E fails. Failure type: competing_defensible_answer (underspecified duplicate-record rule).

**Disposition:** SEND_BACK. The fork needs a prompt pin (which of two first-consultation records for one patient is the patient's first consultation). Gate H3 and Gate G also fail, and the fix for those rebuilds the decisive step. Prior runs are invalidated, so a rerun is required.

## Why
- Asks 5 and 6: 17 patients have two first-consultation records straddling a quarter boundary, one of them carrying a Recovery line in pilot_payment_statements_2025-11_to_2027-01.xlsx. The golden keeps the record the federation did not recover and calls the other a "hand-keyed second record". No shipped file says that. The prompt says "each patient once" and "counting every consultation held whether or not the federation paid for it". Read literally, both records are held consultations and the patient's first consultation is the earlier one.
- That literal reading moves 7 of the 16 pilot cells by 1 (list below).
- Main call: decisive step is excluding patients whose statins a pharmacy packs into a compliance aid when the lists record only part of them. That is data semantics / a partially recorded flag, not analysis (Gate H3, Gate G).

## Evidence (recomputed from target/)
| Item | Result |
|---|---|
| Step 1 population (born 1961 or earlier, 2 or more 2026 items, crosswalk-merged, network at 31 Dec 2026) | 24,893. Reproduced. |
| Care home removed (quarvis care_home_since plus synaris Residence Care home) | 697. Reproduced. |
| Compliance-aid exclusion | 2,136 reproduced: 682 coded (all quarvis mds_since) plus 1,454 uncoded. Uncoded ones have every 2026 item on one weekday (with only bank-holiday next-day shifts) at gaps of 7 or 28 days, 13 or more items. Synaris has no compliance-aid field at all. |
| Remaining population | 22,060. Reproduced. |
| Shares (to one decimal) | Corvendale 2,500 / 35.1; Feldcote 1,686 / 33.6; Nevgarth 2,086 / 33.4; Krathwold 1,978 / 32.9; Grevmoor 2,094 / 32.2; Briskdale 1,905 / 32.1; Iversford 1,555 / 27.0; Marlwold 26.3; Pellholt 26.0; Lathcombe 24.9; Tarvdale 24.1; Ellinholt 23.9. All match the golden exactly. |
| Gap | Iversford 27.01, so 3.0 points under the line. Reproduced. |
| Codes-only answer | Corvendale 34.2, Nevgarth 32.4, Feldcote 31.5, Krathwold 30.9; Grevmoor 28.1 and Briskdale 27.2 fall under the line. The four-network claim in the recommendation reproduces. |

**Main call forks.**
- PDC variants:
  - A union-of-days PDC with no carry-forward gives the same six networks (Briskdale 32.2, Iversford 27.2).
  - A capped total-days/period PDC gives the same six (Grevmoor 30.3).
  - The tier set is therefore robust; the 2.2 definition governs the figures.
- Compliance-aid detection rule:
  - A looser "single weekday, multiples of 7" rule (no 7-or-28 step, no minimum items) catches 60 more ordinary low-item patients. The shares move: Briskdale 31.9, Corvendale 35.0, Ellinholt 23.7. The tier set holds.
  - The natural "weekday plus gaps of 6 to 8 or 27 to 29" rule gives 2,138, not 2,136, so Tarvdale reads 1,638 against the golden 1,640.
  - The graded patient counts therefore rest on an unfiled cut: 13 or more items, or full-year coverage, to exclude two or three coincidental two-item patients. Minor, but exact-figure.
- Bank holidays: no holiday list is shipped. The shifts must be inferred from the data. It is derivable, so not a Gate B failure.

**Pilot workbook (asks 5 and 6).**
- The golden reproduces exactly under its rule. Krathwold counts are 124 / 88 / 97 / 72, followed up 57 / 49 / 50 / 33. Lathcombe counts are 78 / 76 / 83 / 74, followed up 46 / 34 / 46 / 34.
- Of the 45 duplicate pairs, the recovered record is the earlier of the two in 23 and the later in 22, so no consistent "keep earliest" or "keep latest" rule gives the golden.
- Alternative: each patient counted once at their earliest first-consultation record, recovery ignored.

| Cell | Golden | Alternative |
|---|---|---|
| Krathwold Q4 / follow-up | 124 / 57 | 125 / 58 |
| Krathwold Q1 / follow-up | 88 / 49 | 89 / 50 |
| Krathwold Q3 / follow-up | 72 / 33 | 71 / 32 |
| Lathcombe Q4 / follow-up | 78 / 46 | 79 / 47 |
| Lathcombe Q1 / follow-up | 76 / 34 | 77 / 35 |
| Lathcombe Q2 / follow-up | 83 / 46 | 82 / 45 |
| Lathcombe Q3 / follow-up | 74 / 34 | 73 / 33 |

  Only Krathwold Q2 is unchanged.
- Dropping every recovered record gives yet another grid, but the prompt's "whether or not the federation paid" excludes that reading.
- Follow-up window of 41 versus 42 days makes no difference. The relocation of FY975 (Krathwold to Marlwold on 1 June 2026) is handled by community_pharmacies_2026-12.csv. The export's `network` column is stale for it, which is fair Layer 1.

## Files/Hygiene
PASS. 12 files in 3 formats (csv, xlsx, pdf), including one file of 368,662 rows. Distractors: community_pharmacy_contractual_framework_summary_2024-26.pdf and statin_products_dmd_2026-12.csv (unused; every item is in tablets). Mixed date formats and old/new pseudonyms are realistic mess. Names come from a visibly generated pool (Sorrfield, Sorrwick, Ellinwold and so on), a mild tell only. No authoring or benchmark disclosure found. Temporal note: the specification is issued 16 Nov 2026 yet defines the population as of 31 Dec 2026; acceptable as a forward definition. Nothing exclusion-level.

## Stump power (Gate F)
The trap is the uncoded compliance-aid population. A solver using only the recorded flags and the care-home codes will file the four-network answer. The guidance PDF describes same-weekday weekly packs, so a careful reader can connect it. Plausible stump on the main call; the asks are very hard on exact cells. The reasons it works are invalid under Gates G and H (below).

## Stumping type (Gate G)
mechanism: planted_defect_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes.

Banned scaffold: the decisive step is catching that the recorded compliance-aid flag (682 patients) is incomplete (2,136 actual) and flipping away from the lists' codes. Clean-data test: with every flag coded, six networks come out by simply applying the spec, so there is no stump left. Rebuild around a FINE-numbers shape. The surface read being wrong is not, by itself, a sufficient trap, and adding more corrections does not fix it; rebuild the difficulty where the reported numbers are FINE.

## Three rules (Gate H)
domain: pass (PDC adherence is the field's own estimand), layers: pass (Layer 1: pseudonym rotation, two list systems, a PCN membership change, a relocated pharmacy, preliminary and later statements. Layer 2: none that decides the call), decisive_step: data_semantics.

The easy route is the recorded flags plus care-home codes, which gives four networks. A strong analyst who read the spec and found the weekday pattern then simply executes spec 2.2 and 3.1: rule application after identification, with nothing a careful analyst could still get wrong the easy way. H3 fails. Rebuild so the deciding quantity needs an estimand or method choice (for example, an adherence estimate for patients whose supply is censored or imputed, validated out of sample) rather than recovering a hidden population.

## Fix
- prompt (asks 5 and 6): file the WHAT. For example, "a patient who has two first-consultation records within a week counts once, for the record the federation did not recover", or an equivalent that fixes which record is the patient's first consultation and its quarter.
- Task design: replace the decisive step (Gate G and H3) with an analytical, FINE-numbers one.
- If the main call is kept: file the compliance-aid identification criterion explicitly, such as the weekday and 7-or-28 step rule with a minimum item count, so the graded counts reproduce exactly.
