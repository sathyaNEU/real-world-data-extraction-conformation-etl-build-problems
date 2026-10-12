"""Renders submission.md from golden_figures.json so every figure in the write-up is emitted from the objects that produced it."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, "golden_figures.json")))
K = lambda x: f"{round(x / 1000):,}"
P = lambda x: f"{x * 100:.1f}"
M = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
L = {"BO": "Buyout", "GR": "Growth", "PC": "Private credit", "IN": "Infrastructure", "TOTAL": "Programme"}
V = G["validation"]; cb = V["candidates"]; fp = M[G["first_past_below"][1] - 1]
A = []; add = A.append
add("# task501 submission"); add("")
add("## Tags"); add("")
add("**Domain:** Quantitative Finance, liquidity, funding and balance-sheet risk (capital-call cash-flow forecasting and facility sizing for a pension fund's private-markets programme).")
add("**Analytical objective:** Forecasting & Predictive Modeling (candidate pacing bases selected by a walk-forward test, a twelve-month plan and a buffer from the test's within-horizon shortfalls).")
add("**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate."); add("")
add("## 1. Final Recommendation"); add("")
add(f"**Elect the CHF {G['tranche']} million standby tranche for 2027.**"); add("")
add(f"The plan on the age-band basis peaks at a cumulative net outflow of CHF {K(G['peak'])} thousand in December 2027; the test's buffer, the most realised calls ran ahead of that basis's forecast at any point in a horizon, is CHF {K(G['buffer'])} thousand, and with the CHF 75 million reserve netted the need is CHF {K(G['required'])} thousand, which CHF {G['tranche']} million is the smallest tranche to cover. Not CHF {G['below']} million: it leaves CHF {K(G['uncovered_below'])} thousand uncovered in December, and it is where the plan lands when the buffer is read only at the end of each horizon (CHF {K(G['buffer_total'])} thousand), which misses the first-half run of calls the facility would actually face, and also where the manager's-own basis lands when every candidate is fitted once on the whole record and scored on years inside that fit. Not CHF 175 million on the manager's-own basis with no test and no buffer, the CIO's reading.")
add("")
add("## 2. Critical Components"); add("")
add(f"1. Walk-forward test errors, each candidate estimated at each of the twelve quarter-end origins on the record to that origin only: age band **{P(cb['band']['mape'])} per cent**, strategy and band {P(cb['strategy_band']['mape'])} per cent, manager's own {P(cb['fund_own']['mape'])} per cent, so the age-band basis is selected")
add(f"2. The most realised cumulative calls ran ahead of the age-band forecast at any month-end of a test horizon is CHF **{K(G['buffer'])}** thousand, the plan buffer (read at the end of the horizons alone it would be {K(G['buffer_total'])})")
add(f"3. Peak cumulative net outflow of the 2027 plan is CHF **{K(G['peak'])}** thousand, in December")
add(f"4. Peak plus buffer less the CHF 75 million reserve is CHF **{K(G['required'])}** thousand, inside the CHF {G['below']} to {G['tranche']} million tranche")
add("")
add("## 3. Step-by-Step Solution"); add("")
add("1. Built the monthly call and distribution history per fund from the issued lines of the notice ledger by notice month, cancelled notices out (field notes), and each fund's unfunded commitment at any date as commitment less calls plus return-of-capital proceeds under the register's recycling clause (directive s.6.1), which agrees to all 180 audited capital accounts.")
add("2. Estimated the three candidate bases of directive s.5.2 at each of the twelve quarter-end origins from the record up to that origin only, and forecast month by month the next twelve months of calls of the funds then on the register from their unfunded commitments at the origin, all at the origin's rate (s.5.3).")
add(f"3. Scored each candidate against the realised calls of the same funds over the same twelve months: age band {P(cb['band']['mape'])} per cent mean error, strategy and band {P(cb['strategy_band']['mape'])} per cent, manager's own {P(cb['fund_own']['mape'])} per cent; the age-band basis is selected, and fitting the candidates once on the whole record instead reverses the order and crowns the manager's-own basis.")
add(f"4. Took the buffer as the largest amount by which realised cumulative calls exceeded the age-band forecast's cumulative calls at any month-end of any horizon, CHF {K(G['buffer'])} thousand (s.5.6); the first half of each year runs far ahead of an even spread, so the end-of-horizon gap of {K(G['buffer_total'])} understates it.")
add("5. Scheduled October 2026 to December 2027 fund by fund on the age-band rates estimated to the plan date, capped at unfunded commitment, with distributions at the pooled strategy-and-band rates on the audited 31 December 2025 values credited at one quarter, everything at the 30 September 2026 rate (s.5.1, s.5.4, s.4).")
add(f"6. Summed the facility year: cumulative net outflow CHF {K(G['peak'])} thousand by December 2027, plus the buffer, less the reserve, CHF {K(G['required'])} thousand; the buffered need passes CHF {G['below']} million plus reserve in {fp}.")
add(f"7. Recommendation: elect the CHF {G['tranche']} million tranche (commitment and arrangement fees CHF {G['fee_sel']:,.0f} for the year against CHF {G['fee_below']:,.0f} at CHF {G['below']} million).")
add("")
add("## 4. Deliverable Answers"); add("")
add("### standby_facility_2027_board_paper.docx")
add(f"1. CHF {G['tranche']} million")
add(f"2. Tranche below: CHF {G['below']} million; uncovered in the peak month (December 2027): CHF {K(G['uncovered_below'])} thousand; commitment and arrangement fees for the year CHF {G['fee_sel']:,.0f} at CHF {G['tranche']} million and CHF {G['fee_below']:,.0f} at CHF {G['below']} million")
add("3. Walk-forward test, CHF thousand, per origin: realised calls of the funds then on the register over the following twelve months, then the age-band, strategy-and-band and manager's-own forecasts:")
for (y, m), a, i in zip(V["origins"], V["actual"], range(12)):
    add(f"   - {M[m - 1]} {y}: {K(a)}, {K(cb['band']['forecasts'][i])}, {K(cb['strategy_band']['forecasts'][i])}, {K(cb['fund_own']['forecasts'][i])}")
add(f"4. Test errors: age band {P(cb['band']['mape'])}%, strategy and band {P(cb['strategy_band']['mape'])}%, manager's own {P(cb['fund_own']['mape'])}%; the plan runs on the age-band basis; its buffer CHF {K(G['buffer'])} thousand (the furthest realised calls ran ahead of each basis at any point in a horizon: age band {K(cb['band']['buffer'])}, strategy and band {K(cb['strategy_band']['buffer'])}, manager's own {K(cb['fund_own']['buffer'])})")
add("5. 2027 plan, CHF thousand, per month: expected calls, expected distributions, credited distributions, net outflow, cumulative outflow:")
for m in G["months"]:
    add(f"   - {M[m['month'] - 1]}: {K(m['calls'])}, {K(m['dists'])}, {K(m['credited'])}, {K(m['net'])}, {K(m['cum'])}")
add(f"6. The buffered plan runs past the lower tranche; first month: {fp} 2027")
add(f"7. Chart on page 1: cumulative net outflow of 2027 as a line, the same line plus the buffer, the CHF {G['tranche']} million tranche plus reserve drawn at {G['tranche'] + 75} and the CHF {G['below']} million tranche plus reserve at {G['below'] + 75} (CHF million), the {fp} crossing marked, title stating the CHF {G['tranche']} million call")
add("8. NAV bridge 31 December 2025 to 30 June 2026, CHF thousand, per strategy: opening, called, distributed, valuation and currency, closing:")
for s in ("BO", "GR", "PC", "IN", "TOTAL"):
    b = G["bridge"][s]; add(f"   - {L[s]}: {K(b['opening'])}, {K(b['calls'])}, {K(b['dists'])}, {K(b['valuation_fx'])}, {K(b['closing'])}")
add("9. Cash paid and received January to September 2026, CHF thousand, per month: calls, distributions, net:")
for m in range(1, 10):
    c = G["cash"][str(m)]; add(f"   - {M[m - 1]}: {K(c['calls'])}, {K(c['dists'])}, {K(c['net'])}")
add("")
add("### standby_facility_2027.py")
add("1. Runs from the extract folder, prints the tranche, the tranche below with its uncovered amount and the fees, the walk-forward table with the three test errors and each basis's furthest-ahead amount, the selected basis and buffer, the twelve-month plan, the NAV bridge and the 2026 cash table above, and writes the chart; its basis check prints 180 of 180 audited capital accounts agreed")
open(os.path.join(os.path.dirname(HERE), "submission.md"), "w").write("\n".join(A) + "\n")
print("submission rendered: tranche", G["tranche"], "required", K(G["required"]), "buffer", K(G["buffer"]))
