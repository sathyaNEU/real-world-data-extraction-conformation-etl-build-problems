# DA05 — How long do patients wait? The waiting list over-represents the people who wait longest

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Backlog analytics anywhere a queue is snapshotted: support-ticket ages versus resolution times, hiring pipelines, claims backlogs, app-review queues |
| Domain | Healthcare operations |
| Task shape | 14 · Cuts of a distribution (median and 92nd percentile wait for 4 specialties on two bases; the communication standard adopted for patient letters) |
| Core method | Distinguish the waiting-time distribution of *completed* pathways (admitted and non-admitted clock stops in a month) from the *time-already-waited* distribution of the incomplete-pathway snapshot; percentiles from weekly bands by linear interpolation within the band; NHS RTT conventions |
| Analytical stump | A snapshot of people still waiting is length-biased: long waits stay on the list longer and are counted more, and the snapshot measures time waited *so far*, not total wait. Using the snapshot to tell new patients "how long you will wait" overstates or misstates waits depending on list dynamics; completed-pathway distributions answer the question |
| Primary sources | NHS England Referral to Treatment (RTT) waiting times — provider-level full CSV extracts (incomplete, admitted and non-admitted pathways by week bands) |

## 1. The real-world situation

A hospital trust sends referral letters stating the typical wait for treatment. The communications team quoted the median and 92nd
percentile from the incomplete-pathway list (the published headline measure for the 18-week standard). Clinicians objected that most
patients were treated much faster than the letter implied for some specialties and slower for others.

## 2. The decision (one deterministic recommendation)

**For each of four specialties, the median and 92nd-percentile wait (weeks, one decimal) quoted in patient letters, computed on the basis
the memo requires, and the change versus the current letter.**

Rules (communications memo):

* Provider: the trust named in the memo; month: the latest 12 months; specialties (treatment function codes) in scope: 4 listed.
* Quoting basis: completed pathways = admitted plus non-admitted clock stops in the 12 months, pooled; adjusted admitted counts per the RTT
  guidance.
* Percentiles: cumulative counts across weekly bands (0–1, 1–2, …, 104+); linear interpolation within the band containing the target rank;
  the open band 104+ uses the band's lower bound.
* Report alongside: the same percentiles of the incomplete-pathway snapshot at the last month end (time waited so far), labelled as such.
* Letter change = completed-basis value − current letter value.

## 3. Why capable analysts get it wrong

* The incomplete-pathway measure is the headline statistic and the operational standard; it is the natural number to quote.
* Length bias: in a snapshot, each patient's chance of being observed is proportional to their wait.
* Snapshot waits are censored (still waiting); they are not total waits.
* Interpolation within bands matters at the 92nd percentile, where bands are sparse.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `<Month>-<Year>-RTT-full-extract.csv` (12 months) | CSV | ~180k each | NHS England RTT statistics | Open Government Licence v3 | Pathways by provider, treatment function, week band |
| 13 | `rtt_guidance.pdf` | PDF | — | NHS England RTT recording guidance | OGL | Definitions, adjusted admitted |
| 14 | `treatment_function_codes.csv` | CSV | ~25 | NHS England | OGL | Specialty codes |
| 15 | `communications_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `current_letter_values.xlsx` | XLSX | 4 | Task author | — | Current letters |
| 17 | `week_band_bounds.json` | JSON | ~105 | Derived | — | Band boundaries |
| 18 | `trust_rtt_tidy.parquet` | Parquet | ~50k | Derived | OGL | Convenience |

## 5. Deterministic solution path

1. Filter provider and specialties; stack 12 months of admitted (adjusted) and non-admitted counts by band.
2. Cumulative counts; interpolate median and P92 per specialty.
3. Snapshot percentiles from the last month's incomplete pathways.
4. Compare with current letter values.

## 6. Wrong paths (method errors, not misreadings)

**A — snapshot percentiles for letters.** Length-biased, censored.

**B — unadjusted admitted counts.** Double-counted pathways.

**C — band midpoint instead of interpolation.** Biased percentiles.

**D — one month only.** Volatile small cells.

## 7. Why the stump is analytical, not semantic

All three distributions are defined. The trap is the sampling mechanism of a queue snapshot versus completed events.

## 8. Draft task prompt (prose)

> What waits should our referral letters quote for the four specialties? Follow the communications memo: completed pathways over 12 months,
> interpolated within week bands, with the snapshot figures shown for contrast. Provide `letter_waits.csv` (specialty: median and P92 on both
> bases, current letter, change), `wait_distributions.png` (completed vs snapshot cumulative curves per specialty), and a one-page
> `letter_update.pdf`.

## 9. Deliverables

* `letter_waits.csv`, `wait_distributions.png`, `letter_update.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 specialties × (median, P92 completed; median, P92 snapshot; change) = 20; volumes; interpolation details; recommendation wording.

## 11. Golden-output checklist

* Specialty filter; adjusted admitted; pooling; interpolation; open band; snapshot labelling.

## 12. Build notes (scope tuning)

* Choose specialties where snapshot and completed percentiles diverge in both directions (growing and shrinking lists).
