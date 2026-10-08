# OS23 — Water loss recovery: not all non-revenue water is leakage, and not all leakage is worth chasing

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Loss-reduction programmes that must separate measurement losses from physical losses and recognise an unavoidable floor (retail shrink, cloud waste, scrap) |
| Domain | Water utilities |
| Task shape | 03 · Bridge between two totals (non-revenue water volume → recoverable real losses, via apparent losses, unbilled authorised use and unavoidable annual real losses; the utilities funded for leak detection) |
| Core method | AWWA M36 water balance: NRW = unbilled authorised + apparent losses + real losses; UARL from mains length, service connections and pressure (Lambert formula); recoverable = max(0, real losses − UARL) valued at variable production cost; ILI = real ÷ UARL |
| Analytical stump | Treating the whole non-revenue water volume as recoverable leakage overstates the opportunity: apparent losses (meter under-registration, theft, billing errors) are fixed differently and valued at retail price; a technical minimum of leakage is unavoidable. Ranking utilities by NRW percentage favours small systems with few customers per mile |
| Primary sources | Texas Water Development Board (TWDB) water loss audit data |

## 1. The real-world situation

A state revolving fund will support leak-detection programmes at utilities with the largest recoverable real-loss value. The draft ranked
utilities by non-revenue water as a percentage of production and valued the whole volume at retail rates.

## 2. The decision (one deterministic recommendation)

**The 10 utilities funded, ranked by annual value of recoverable real losses, and the bridge from NRW to recoverable volume for the top
utility.**

Rules (fund memo):

* Data: TWDB water loss audits for the audit year in memo; utilities with ≥ 3,000 connections and data validity score ≥ 50 (as reported).
* Components from the audit: billed/unbilled authorised, apparent losses, real losses, mains miles, connections, average pressure, variable
  production cost.
* UARL (gallons/day) = (5.4 × mains miles + 0.15 × connections + 7.5 × total service-line length per memo approximation) × pressure (Lambert);
  annualised.
* Recoverable real losses = max(0, real losses − UARL); value = recoverable × variable production cost.
* Rank by value; top 10; bridge for the top utility (NRW → unbilled authorised → apparent → UARL → recoverable).

## 3. Why capable analysts get it wrong

* NRW percentage is the most quoted KPI.
* Percentages penalise low-consumption, long-network systems and ignore volume.
* Apparent losses are revenue, not production, problems.
* Real losses below the UARL are not economically recoverable.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `twdb_water_loss_audits_<year>.xlsx` | XLSX | ~2.5k utilities | Texas Water Development Board | Texas public information (public) | Audit components |
| 2 | `twdb_water_loss_audit_manual.pdf` | PDF | — | TWDB | Public | Definitions, validity |
| 3 | `awwa_m36_formulas_citation.pdf` | PDF | — | AWWA M36 (cite) | Cite | UARL, ILI |
| 4 | `fund_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `draft_nrw_ranking.xlsx` | XLSX | ~200 | Task author | — | Naive ranking |
| 6 | `uarl_check.json` | JSON | — | Task author | — | Worked example |
| 7 | `utility_scope.csv` | CSV | ~250 | Derived | Public | Eligible utilities |

## 5. Deterministic solution path

1. Filter utilities by connections and validity.
2. UARL; recoverable real losses; value.
3. Rank; top 10; bridge.
4. Contrast with the NRW% ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — NRW percentage ranking.** Small systems dominate.

**B — valuing all NRW at retail.** Overstated.

**C — no UARL floor.** Unrecoverable volume counted.

**D — apparent losses treated as leakage.** Wrong intervention.

## 7. Why the stump is analytical, not semantic

The water balance and formulas are specified. The trap is gross loss versus economically recoverable loss.

## 8. Draft task prompt (prose)

> Which ten utilities should get leak-detection funding? Separate the water balance and compute recoverable real losses above the unavoidable
> floor as the fund memo specifies. Provide `recoverable_losses.csv` (utility: NRW, apparent, real, UARL, ILI, recoverable value, rank),
> `nrw_bridge.png`, and a one-page `funding_list.pdf`.

## 9. Deliverables

* `recoverable_losses.csv`, `nrw_bridge.png`, `funding_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 utilities + #11; values for 12 utilities; bridge items; UARL check; contrast.

## 11. Golden-output checklist

* Filters; UARL formula; recoverable; valuation; ranking; bridge.

## 12. Build notes (scope tuning)

* Confirm fewer than half of the NRW% top 10 are funded.
