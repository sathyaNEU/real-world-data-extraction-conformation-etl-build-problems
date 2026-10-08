# RC21 — Unemployment rose 0.8 points: a wave of layoffs, or a hiring freeze?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Subscriber-base changes driven by churn versus acquisition (a falling active-user count from rising churn vs falling sign-ups); funnel stocks driven by inflow and outflow hazards |
| Domain | Labour-market analytics |
| Task shape | 03 · Bridge between two totals (unemployment rate, reference → current, bridged by the six transition hazards between employment, unemployment and non-participation via the steady-state rate) |
| Core method | Convert CPS labour-force-status gross flows into monthly transition probabilities (flow ÷ origin stock); compute the three-state steady-state unemployment rate from the transition matrix; check it tracks the actual rate; decompose the change in steady-state unemployment into the contribution of each transition probability with a Shapley decomposition over the six off-diagonal probabilities |
| Analytical stump | The layoff narrative comes from counts of people moving from employment into unemployment, which rise mechanically when the employed stock is large. Hazards, not flow counts, determine the stock. A two-state view (E↔U) ignores the large flows to and from non-participation, which often account for a big part of unemployment changes. And because the steady-state rate is nonlinear in the hazards, one-at-a-time attribution does not add up |
| Primary sources | U.S. BLS Current Population Survey labour force status flows (margin-adjusted gross flows, seasonally adjusted) |

## 1. The real-world situation

The economic research team at a large professional network had to brief its sales leadership on why unemployment rose 0.8 points in a year. The
recruiting-products team argued that a layoff wave had begun and wanted to pivot marketing toward outplacement; the research lead suspected that
falling job-finding rates (a hiring freeze) explained more. The two stories imply different product bets.

## 2. The decision (one deterministic recommendation)

**The dominant margin of the unemployment rise — separations into unemployment (EU), job finding (UE), or participation flows (NU, UN, EN, NE) —
by Shapley contribution to the change in steady-state unemployment, with all six contributions.**

Rules (research memo):

* Data: BLS CPS labour force status flows, seasonally adjusted, margin-adjusted levels for the 9 flows among E, U and N, monthly.
* Periods: 12-month averages of monthly transition probabilities for the reference and current years.
* Transition probability p_XY(t) = flow X→Y in month t ÷ stock X in month t − 1 (stocks from the same flows table: Σ flows from X).
* Steady state: solve π = π P for the 3 × 3 transition matrix P built from the averaged probabilities; u* = π_U ÷ (π_E + π_U).
* Fit check: report u* and the actual average unemployment rate for both periods.
* Decomposition: Shapley values over the six off-diagonal probabilities for Δu* (64 subsets, each probability set to its reference or current
  value; diagonal terms = 1 − row sums).
* Dominant margin: group contributions as EU (separations), UE (job finding), participation (sum of NU, UN, EN, NE); report the largest group.

## 3. Why capable analysts get it wrong

* Flow counts are reported in the news and look like hazards.
* Non-participation is forgotten in E↔U thinking.
* Steady-state formulas are nonlinear; ordering matters without Shapley.
* Monthly probabilities are noisy; averaging must happen on probabilities, not counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ln.data.1.AllData` (flows subset) | TXT (tab) | ~300k | BLS LN flat files (labour force flows series) | U.S. Government work (public domain) | Gross flows by month |
| 2 | `ln.series` | TXT | ~40k | BLS | Public domain | Series metadata |
| 3 | `lns14000000.csv` | CSV | ~900 | BLS (unemployment rate, SA) | Public domain | Actual rate for fit check |
| 4 | `cps_flows_methodology.pdf` | PDF | — | BLS (Frazis et al.; margin adjustment) | Public domain | Flows construction |
| 5 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `recruiting_layoff_brief.xlsx` | XLSX | — | Task author | — | Counts-based layoff narrative |
| 7 | `shimer_2012_citation.pdf` | PDF | — | Cite | Cite | Steady-state decomposition background |

## 5. Deterministic solution path

1. Identify the 9 flow series; build monthly stocks and transition probabilities.
2. Average probabilities over each 12-month period; build P for each period.
3. Steady states and fit check.
4. Shapley decomposition over the six probabilities; group contributions.
5. Dominant margin; contrast with the counts-based brief.

## 6. Wrong paths (method errors, not misreadings)

**A — flow counts.** E→U counts rise with the employed stock and seasonal churn; the layoff story is overstated.

**B — two-state model.** Ignores participation flows; contributions are misallocated to EU and UE.

**C — one-at-a-time substitution.** Contributions do not sum to Δu* and depend on order.

**D — averaging counts, then dividing.** Different from averaging probabilities when stocks move; inconsistent with the memo.

## 7. Why the stump is analytical, not semantic

The series, formulas and decomposition are specified. The trap is confusing flow counts with hazards and treating a nonlinear stock-flow system
additively.

## 8. Draft task prompt (prose)

> Sales leadership wants to know if rising unemployment is a layoff wave or a hiring freeze. Use the research memo's flow-based steady-state method to
> attribute the rise to each transition, and tell me which margin dominates. Provide `flow_contributions.csv` (transition: reference and current
> probability, Shapley contribution), `unemployment_flow_bridge.png`, and a one-page `margin_brief.pdf`.

## 9. Deliverables

* `flow_contributions.csv` — six probabilities in both periods, contributions and groups.
* `unemployment_flow_bridge.png` — waterfall from u*_ref to u*_cur by transition.
* `margin_brief.pdf` — dominant margin, fit check, and why the counts-based brief misleads.

## 10. Where 25+ rubric criteria come from

* Probabilities for 6 transitions × 2 periods: 12.
* Steady states and fit check: 4.
* Shapley contributions (6) and closure: 7.
* Grouping and dominant margin: 2.
* Brief contrast: 2+.

## 11. Golden-output checklist

* Origin stocks from the flows table, lagged one month.
* Averaging of probabilities, not counts.
* Three-state steady state; Shapley over 6 inputs.
* Groups as defined.

## 12. Build notes (scope tuning)

* Choose a year in which E→U counts rose noticeably but the UE probability fell more in Shapley terms; confirm that the two-state calculation and
  the counts view both point to separations.
