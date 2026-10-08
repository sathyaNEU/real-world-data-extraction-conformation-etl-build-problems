# AD25 — Single-bidder red flags: specialised buyers are not corrupt buyers

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Procurement-integrity analytics (EU Arachne, opentender.eu, World Bank integrity units); any marketplace flagging sellers or buyers by a rate that depends heavily on category mix |
| Domain | Public procurement / integrity |
| Task shape | 01 · Ranked list under a cap (20 contracting authorities for integrity review) |
| Core method | Lot-level single-bid indicator; indirect standardisation: expected single-bid lots from national rates by CPV division × procedure type × value band; observed/expected ratio with a Poisson lower confidence bound; minimum lot count |
| Analytical stump | Single-bid rates vary several-fold by what is bought and how (negotiated procedures, niche medical devices, framework call-offs). Ranking authorities by raw single-bid share selects hospitals and defence buyers, not anomalous behaviour. Award notices also bundle lots; the notice is the wrong unit |
| Primary sources | EU Tenders Electronic Daily (TED) contract award notices — CSV bulk exports |

## 1. The real-world situation

A national audit office will review **20** contracting authorities whose tenders attract only one bid unusually often. The pilot list,
based on raw single-bid share of award notices, was dominated by university hospitals and the defence agency; reviewers found nothing
irregular. They asked for a list that compares each authority with what its purchase mix would predict.

## 2. The decision (one deterministic recommendation)

**The 20 contracting authorities sent for integrity review, and the 21st.**

Rules (integrity memo):

* Data: TED contract award notices for the country in scope, 2018–2022; unit = awarded lot (one row per award per lot); keep lots with a
  numeric number of offers received.
* Single-bid lot: offers received = 1.
* Strata: CPV division (first two digits) × procedure type (open, restricted, negotiated with/without publication, competitive dialogue,
  other) × value band (< €100k, €100k–1M, €1M–10M, ≥ €10M; values converted at the notice's currency rate table).
* Expected single-bid lots per authority = Σ over its lots of the national stratum single-bid rate (computed excluding that authority).
* O/E ratio; lower 95% bound from the exact Poisson interval on O divided by E.
* Eligible: ≥ 50 lots. Rank by the lower bound; top 20; report #21.

## 3. Why capable analysts get it wrong

* Raw rates are intuitive and quick.
* Category and procedure mix explain most variation; this is a case-mix problem, as in hospital mortality comparisons.
* Including the authority in its own expected rate dampens outliers in strata it dominates.
* Ranking by the point ratio favours small authorities with a handful of lots.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–5 | `TED_CAN_2018.csv` … `TED_CAN_2022.csv` | CSV | ~700k–900k each (EU-wide) | TED bulk CSV (Publications Office of the EU) | EU reuse policy (Decision 2011/833/EU) | Award notices, lots |
| 6 | `TED_csv_data_dictionary.pdf` | PDF | — | Publications Office | Same | Field definitions |
| 7 | `cpv_2008_codes.xlsx` | XLSX | ~9.5k | EU CPV regulation | EU reuse | CPV hierarchy |
| 8 | `procedure_type_map.json` | JSON | ~15 | Task author | — | Procedure groupings |
| 9 | `ecb_reference_rates.csv` | CSV | ~6k days | ECB | ECB reuse terms | Currency conversion |
| 10 | `integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `pilot_raw_share_list.xlsx` | XLSX | 20 | Task author | — | Pilot list |
| 12 | `authority_name_clusters.csv` | CSV | ~5k | Task author (name/ID harmonisation) | — | Authority identity |

## 5. Deterministic solution path

1. Filter country and years; explode to lot level; keep valid offer counts.
2. Assign strata; convert values; compute national stratum rates with leave-one-authority-out.
3. Sum expected per authority; O/E; exact Poisson lower bound.
4. Eligibility; rank; top 20 + #21.
5. Overlap with the pilot list.

## 6. Wrong paths (method errors, not misreadings)

**A — raw single-bid share.** Specialised buyers dominate.

**B — notice-level unit.** Multi-lot notices miscounted.

**C — expected rates including the authority itself.** Outliers dampened.

**D — ranking by point O/E.** Small-sample extremes.

## 7. Why the stump is analytical, not semantic

The indicator, strata and test are specified. The trap is comparing units with different case mix and unit-of-analysis errors.

## 8. Draft task prompt (prose)

> Give me the 20 contracting authorities for integrity review, ranked the way the memo specifies: single-bid lots against what each
> authority's purchase mix would predict. Provide `authority_oe.csv` (authority: lots, observed, expected, O/E, lower bound, rank),
> `oe_funnel.png` (O/E against expected with the cut), and a one-page `review_selection.pdf` including how many pilot-list authorities
> survive.

## 9. Deliverables

* `authority_oe.csv`, `oe_funnel.png`, `review_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 authorities + #21; O, E, bound for 8; stratum rates for 4 strata; pilot overlap; exclusions.

## 11. Golden-output checklist

* Lot-level unit; offer-count filter; strata; leave-one-out rates; exact bound; eligibility; ranking.

## 12. Build notes (scope tuning)

* Pick a country with enough lots and diverse procedure use; verify the offers-received field coverage by year.
* Confirm that at most half the pilot list survives.
