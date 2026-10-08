# RC49 — E-scooter injuries tripled: are shared scooters getting more dangerous, or are there just far more rides — and whose rides?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Product-safety incident rates (battery fires per device in use, crash reports per mile driven, app-related harms per active user), where exposure and the user mix grow faster than the incident count |
| Domain | Product safety / urban mobility policy |
| Task shape | 18 · Hypotheses versus evidence (exposure growth, rising per-trip risk on shared scooters, shift to privately owned scooters, coding or sampling artefact → evidence lines from weighted national estimates and exposure; the hypothesis a city's ban decision rests on) |
| Core method | National injury estimates from the probability sample of emergency departments using the case weights and design (strata, PSUs) with 95% intervals; injuries per million shared trips by year; the 2020 natural experiment (shared trips fell while injuries continued); share of injured under 18 (who cannot rent shared scooters) as a marker for private scooters; checks for coding changes and unstable estimates |
| Analytical stump | Counting sample cases instead of weighted estimates, or comparing injuries without exposure, makes the trend look like rising danger. The shared-trip denominator covers only part of the exposure: when injuries keep rising in a year shared trips collapse, and the under-18 share climbs, private scooters are driving growth. A ban on shared scooters would then miss most of the risk |
| Primary sources | U.S. CPSC National Electronic Injury Surveillance System (NEISS) annual data; NACTO shared micromobility reports (annual shared e-scooter trips) |

## 1. The real-world situation

A city council proposed banning shared e-scooters after national news reported that e-scooter injuries had tripled in five years. The city's
transport department argued that ridership had grown even faster and that many injuries involved privately owned scooters, including by
teenagers. The council asked for the evidence on each explanation before voting.

## 2. The decision (one deterministic recommendation)

**The hypothesis the council's decision should rest on (exposure growth, rising shared per-trip risk, private-scooter shift, or artefact) from the
evidence grid, with weighted national estimates and rates.**

Rules (policy memo):

* Data: NEISS annual files for the memo's years; cases with the memo's powered-scooter product codes (either product field); national estimate =
  Σ case weights; 95% intervals by Taylor linearisation using the stratum and PSU fields; estimates flagged unstable if based on < 20 cases or
  coefficient of variation > 33%.
* Exposure: annual U.S. shared e-scooter trips from NACTO reports (memo table with page references).
* Evidence lines:
  * E1 exposure: injuries per million shared trips change by < 20% between the first and last pre-2020 years → supports exposure growth.
  * E2 shared risk: the same rate rises by ≥ 20% → supports rising shared per-trip risk.
  * E3 decoupling: in 2020 shared trips fell ≥ 50% while the injury estimate fell < 10% → supports the private shift.
  * E4 age marker: share of injured aged < 18 rises by ≥ 5 points over the period (shared services require riders 18+) → supports the private shift.
  * E5 artefact: a step change ≥ 50% in a single year coinciding with a product-code revision or sample redesign noted in NEISS documentation →
    supports artefact.
* Hypothesis adopted: the one with the most supporting lines (E3 and E4 both support the private shift); ties resolved in the order artefact,
  private shift, shared risk, exposure.

## 3. Why capable analysts get it wrong

* Headlines report sample cases or national estimates without exposure.
* Shared-trip data cover only rented scooters.
* NEISS estimates need weights and design-based intervals; small cells are unstable.
* Coding changes can create artificial jumps.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `neiss_<year>.tsv` (6 years) | TSV | ~350k per year | CPSC NEISS | U.S. Government work (public domain) | Injury cases with weights |
| 2 | `neiss_fmt.xlsx` | XLSX | ~2k | CPSC NEISS coding manual tables | Public domain | Product and field codes |
| 3 | `neiss_coding_manual_<years>.pdf` | PDF | — | CPSC | Public domain | Code revisions, sample notes |
| 4 | `nacto_shared_micromobility_trips.csv` | CSV | ~8 | Task author (from NACTO annual reports; cite pages) | Cite | Shared trips by year |
| 5 | `policy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `council_ban_motion.pdf` | PDF | — | Task author | — | The motion and its evidence |

## 5. Deterministic solution path

1. Stack years; filter product codes; compute weighted estimates and design-based intervals; flag unstable cells.
2. Rates per million shared trips; 2020 comparison; age-share trend; code-revision check.
3. Evidence grid; adopted hypothesis; contrast with the council motion.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted case counts.** Sample cases are not national estimates; trends depend on hospital mix.

**B — injuries without exposure.** Ridership growth read as rising danger.

**C — shared trips as all exposure.** Private scooter injuries attributed to shared services.

**D — intervals ignored.** Small year-to-year changes treated as real.

## 7. Why the stump is analytical, not semantic

Cases are selected by product codes, not narratives; every line is a numeric threshold. The trap is a numerator without the right denominator and
the wrong exposure population.

## 8. Draft task prompt (prose)

> The council wants to ban shared e-scooters because injuries tripled. Evaluate the policy memo's evidence lines with properly weighted NEISS estimates
> and tell me which explanation the vote should rest on. Provide `injury_evidence_grid.csv` (line: statistic, interval, holds?), `injury_vs_trips.png`, and a
> one-page `scooter_policy_note.pdf`.

## 9. Deliverables

* `injury_evidence_grid.csv` — weighted estimates, intervals, rates and evidence outcomes.
* `injury_vs_trips.png` — injuries (with intervals) against shared trips, with the under-18 share.
* `scooter_policy_note.pdf` — adopted hypothesis and implications for the ban.

## 10. Where 25+ rubric criteria come from

* Weighted estimates and intervals for 6 years: 12 (grouped).
* Unstable flags: 2.
* Rates per million trips: 3.
* E1–E5 outcomes: 5.
* Adopted hypothesis: 1.
* Contrast with the motion: 2+.

## 11. Golden-output checklist

* Product codes in either product field; weights; Taylor-linearised intervals with strata and PSUs.
* NACTO trip figures with citations.
* Decision rule and tie order.

## 12. Build notes (scope tuning)

* Use a year range spanning 2018–2022; confirm E3 and E4 hold, so the private-shift hypothesis is adopted.
