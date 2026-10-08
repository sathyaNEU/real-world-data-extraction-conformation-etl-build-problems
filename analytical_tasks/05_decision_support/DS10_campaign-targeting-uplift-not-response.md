# DS10 — Who should get the email? The likeliest buyers would buy anyway

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Targeting of promotions, notifications and retention offers at e-commerce, ride-hail and subscription companies, where the goal is incremental behaviour |
| Domain | Retail marketing |
| Task shape | 01 · Ranked list under a cap (the customer segments receiving the next campaign, ranked by incremental spend per email, until the 30% contact budget) |
| Core method | Use the randomised campaign to estimate uplift (treatment − control) in conversion and spend by segment (recency × history × channel × newbie); rank segments by incremental spend per contact; Qini/uplift curve for the targeting policy; compare with targeting by highest response rate in the treated group |
| Analytical stump | Ranking customers by predicted purchase probability targets loyal recent buyers who purchase regardless of email; some segments respond negatively. With a randomised control group available, the decision must use the treatment effect, not the treated group's response |
| Primary sources | Kevin Hillstrom's MineThatData E-Mail Analytics and Data Mining Challenge dataset (64,000 customers, randomised men's/women's/no email) |

## 1. The real-world situation

A retailer will email **30%** of its customer file next season. The CRM team proposes targeting the segments with the highest conversion rates
among customers who received last season's email. The analytics lead noted that last season's test randomised a control group.

## 2. The decision (one deterministic recommendation)

**The segments targeted (by incremental spend per email, cumulative contacts ≤ 30% of the file) with the men's email creative, the expected
incremental spend per 1,000 customers, and the segments the CRM proposal would have included that show no uplift.**

Rules (marketing memo):

* Data: Hillstrom dataset; treatment = "Mens E-Mail"; control = "No E-Mail" (women's arm excluded for this decision).
* Segments: recency band (1–3, 4–6, 7–9, 10–12 months) × history segment (provided bands) × channel (Phone/Web/Multichannel); segments with
  ≥ 200 customers in each arm.
* Uplift in spend per customer = mean spend (treatment) − mean spend (control); SE by Welch.
* Rank by uplift; include segments in order until cumulative share of the file reaches 30% (segment sizes from the full file); exclude segments
  whose uplift lower 80% bound < 0.
* Report the CRM proposal (rank by treated conversion rate) and its expected incremental spend.

## 3. Why capable analysts get it wrong

* Response models are standard in CRM.
* Incrementality requires a counterfactual; the control group provides it.
* Some segments have negative uplift (annoyance or cannibalisation of organic purchases).
* Small segments have noisy uplift; the bound rule guards against noise.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv` | CSV | 64,000 | MineThatData (Kevin Hillstrom) | Released publicly for the challenge (verify terms; cite) | Customers, treatment, visits, conversions, spend |
| 2 | `hillstrom_challenge_description.html` | HTML | — | MineThatData blog | Cite | Field definitions |
| 3 | `segment_definitions.json` | JSON | — | Task author | — | Segments |
| 4 | `marketing_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `crm_response_ranking.xlsx` | XLSX | ~36 | Task author | — | CRM proposal |
| 6 | `uplift_modelling_reference.pdf` | PDF | — | Cite (Radcliffe & Surry) | Cite | Qini curves |

## 5. Deterministic solution path

1. Filter arms; build segments; check sizes.
2. Uplift and SE per segment; bounds; ranking; 30% cut.
3. Expected incremental spend per 1,000; Qini curve; CRM contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — rank by treated conversion.** Targets sure things.

**B — conversion uplift instead of spend uplift.** Not the memo's objective.

**C — including the women's arm in treatment.** Mixes creatives.

**D — ignoring noise.** Small segments with spurious uplift chosen.

## 7. Why the stump is analytical, not semantic

The arms, segments and rules are specified. The trap is optimising response rather than incremental effect.

## 8. Draft task prompt (prose)

> Which customer segments should receive next season's men's email? Use last season's randomised test to rank segments by incremental spend as the
> marketing memo specifies, within a 30% contact budget. Provide `segment_uplift.csv` (segment: n, conversion and spend by arm, uplift, bound, target),
> `qini_curve.png`, and a one-page `targeting_plan.pdf`.

## 9. Deliverables

* `segment_uplift.csv`, `qini_curve.png`, `targeting_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* Targeted segments; uplift for 12 segments; expected incremental spend; CRM contrast; negative-uplift segments.

## 11. Golden-output checklist

* Arm filter; segment sizes; uplift and SE; bound; budget cut; contrast.

## 12. Build notes (scope tuning)

* Confirm at least three CRM-proposed segments have non-positive uplift.
