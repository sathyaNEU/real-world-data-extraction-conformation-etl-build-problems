# AD21 — Drug-safety signals from spontaneous reports: small counts shout, duplicates echo, big signals mask

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Pharmacovigilance at drug makers and regulators (and any "disproportionate reporting" monitor, e.g. crash or complaint reports by device model) |
| Domain | Drug safety / regulatory science |
| Task shape | 01 · Ranked list under a cap (20 drug–event pairs to signal review) |
| Core method | Case-level de-duplication; disproportionality with Bayesian shrinkage (information component IC with lower credibility bound IC025); background computed excluding a masking drug; minimum counts |
| Analytical stump | Proportional reporting ratios on pairs with 1–3 reports are huge by chance; duplicate case versions inflate counts; one heavily reported drug–event pair inflates the background rate and hides others (masking). Shrinkage, de-duplication and unmasking change the review list |
| Primary sources | FDA Adverse Event Reporting System (FAERS) quarterly data files |

## 1. The real-world situation

A drug maker's safety team reviews **20 drug–event combinations** per quarter flagged by a disproportionality screen over its therapeutic
area. The analyst computed PRRs on the raw quarterly files; the list was dominated by pairs with one or two reports, several pairs appeared
because the same case was submitted in multiple versions, and a well-known signal for one product made similar events for other products
look unremarkable.

## 2. The decision (one deterministic recommendation)

**The 20 drug–event pairs sent to signal review this quarter, and the 21st.**

Rules (pharmacovigilance memo):

* Data: FAERS quarterly files for the last 8 quarters. De-duplicate by `caseid`, keeping the highest `caseversion`.
* Drugs: active-ingredient level (normalized names per the mapping file) with role code PS or SS only; events: MedDRA preferred terms as
  reported.
* Scope: the 30 ingredients in the therapeutic-area list; background = all de-duplicated reports.
* Masking: the drug–event pair listed in `masking_pair.json` (a widely publicized association) is removed from the background counts.
* IC = log₂((n + 0.5) ÷ (E + 0.5)), E = (n_drug × n_event) ÷ N; IC025 by the approximation in the memo. Flag pairs with n ≥ 3 and IC025 > 0;
  rank by IC025 (ties by n).
* Review list = top 20; report #21.

## 3. Why capable analysts get it wrong

* PRR and ROR are simple and widely taught; with tiny n they are dominated by noise.
* FAERS stores follow-up versions of the same case; without de-duplication, counts and backgrounds are inflated unevenly.
* A notorious association inflates E for related events across all drugs, hiding signals for others.
* Concomitant drugs (role C) are not suspected; including them dilutes signals.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–8 | `faers_ascii_YYYYQq/DEMOyyQq.txt` (8 quarters) | $-delimited text | ~400k each | FDA FAERS | U.S. Gov public domain | Case demographics, versions |
| 9–16 | `DRUGyyQq.txt` (8 quarters) | Text | ~1.5–2M each | FDA FAERS | Public domain | Drugs and roles |
| 17–24 | `REACyyQq.txt` (8 quarters) | Text | ~1.2–1.5M each | FDA FAERS | Public domain | Reactions (MedDRA PTs) |
| 25 | `faers_readme.pdf` | PDF | — | FDA | Public domain | Table definitions, de-duplication guidance |
| 26 | `ingredient_mapping.csv` | CSV | ~5k | Task author (from public drug name references) | — | Name normalization |
| 27 | `therapeutic_area_ingredients.json` | JSON | 30 | Task author | — | Scope |
| 28 | `masking_pair.json` | JSON | 1 | Task author | — | Pair excluded from background |
| 29 | `noren_ic_shrinkage_citation.pdf` | PDF | — | Cite | Cite | IC and IC025 |
| 30 | `pharmacovigilance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 31 | `analyst_prr_list.xlsx` | XLSX | 20 | Task author | — | Raw PRR list |

## 5. Deterministic solution path

1. Load and de-duplicate cases; filter suspect roles; normalize ingredients.
2. Count n, n_drug, n_event, N excluding the masking pair from background counts.
3. IC and IC025; filters; rank; top 20 + 21st.
4. Contrast with the PRR list (overlap, pairs with n < 3).

## 6. Wrong paths (method errors, not misreadings)

**A — raw PRR.** Small-count pairs dominate.

**B — no de-duplication.** Inflated counts.

**C — no unmasking.** Signals hidden behind the notorious pair.

**D — concomitant drugs included.** Diluted signals.

## 7. Why the stump is analytical, not semantic

Every rule is specified. The traps are small-sample noise, duplicate inflation and masking — statistical properties of disproportionality.

## 8. Draft task prompt (prose)

> Give me this quarter's 20 drug–event pairs for signal review following the pharmacovigilance memo: de-duplicate FAERS cases, use suspect
> drugs only, remove the masking pair from the background and rank by the shrunken IC lower bound. Provide `signal_list.csv` (pair: n, E, IC,
> IC025, rank), `ic_vs_count.png` (IC025 against n with the review cut), and a one-page `signal_review_memo.pdf` with the list, #21, and the
> pairs the PRR list would have sent instead.

## 9. Deliverables

* `signal_list.csv`, `ic_vs_count.png`, `signal_review_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 pairs + #21; n, E, IC025 for 10 pairs; de-duplication count; masking effect on 3 pairs; PRR overlap.

## 11. Golden-output checklist

* Case de-dup by version; suspect roles; normalization; background without masking pair; IC025; thresholds; ranking.

## 12. Build notes (scope tuning)

* Pick a therapeutic area with a publicized association to use as the masking pair; confirm unmasking adds ≥ 2 pairs to the list.
* Record the quarters used; FAERS files are revised.
