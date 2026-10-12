"""task501 submission.md, rendered from generator/figures.json so that no figure is typed. Run after checks.py;
then .claude/skills/determinism-check/figures_check.py task501."""
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, "figures.json")))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
NAMES = {"LOS-III": "Loschwitz Equity III", "JUN-II": "Juneau Infrastructure Partners II", "ROS-II": "Rosenthal Buyout Partners II",
         "TES-I": "Tessin Private Credit I", "COR-VI": "Corvisart Equity VI", "BRW-II": "Brantwood Partners II",
         "ULM-II": "Ulmenhof Capital II", "QUE-III": "Quendel Partners III", "ISE-II": "Isenring Private Capital II"}
STRATS = [("BO", "Buyout"), ("GR", "Growth"), ("PC", "Private credit"), ("IN", "Infrastructure")]


def k(x):
    return f"{x:,.0f}"


def m1(x):
    return f"{x:,.1f}"


def dm(s):
    d = date.fromisoformat(s)
    return f"{d.day} {MONTHS[d.month - 1]}"


def main():
    fu = F["four_funds"]
    four = sorted(fu, key=lambda c: fu[c]["ip_end"])
    slow = sorted(F["slow_starters"], key=lambda c: F["slow_starters"][c]["ip_end"])
    amt, down = F["call_amount_chf_m"], F["next_amount_down_chf_m"]
    D = F["distributions_2026_chf_k"]
    lo4, hi4 = F["four_drawn_range_pct"]
    lo6, hi6 = F["six_drawn_range_pct"]
    slo, shi = F["slow_year_before_range_pct"]
    names4 = ", ".join(NAMES[c] for c in four[:-1]) + " and " + NAMES[four[-1]]
    shares4 = ", ".join(f"{fu[c]['drawn_share']:.1f}" for c in four[:-1]) + " and " + f"{fu[four[-1]]['drawn_share']:.1f}"
    dates4 = ", ".join(dm(fu[c]["ip_end"]) for c in four[:-1]) + " and " + dm(fu[four[-1]]["ip_end"]) + " 2027"
    slow_names = ", ".join(NAMES[c] for c in slow[:-1]) + " and " + NAMES[slow[-1]]
    top = F["top_strategy"]
    tcode = next(c for c, n in STRATS if n == top)
    out = f"""## Tags

**Domain:** Quantitative Finance (liquidity, funding and balance-sheet risk: a pension foundation's standby facility for the capital calls of its private-markets programme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Elect a standby facility of CHF {amt} million for 2027.**
Expected capital calls of CHF {m1(F['expected_calls_chf_m'])} million in 2027, plus one tenth and less the CHF {F['reserve_chf_m']} million reserve, leave CHF {m1(F['requirement_chf_m'])} million for the facility to cover, CHF {m1(F['shortfall_next_down_chf_m'])} million more than CHF {down} million. Not CHF {F['default_amount_chf_m']} million, where the programme's age-band call rates on unfunded commitment land (CHF {m1(F['default_expected_calls_chf_m'])} million of calls): they give {names4} the pace of funds their age, CHF {m1(F['four_default_chf_m'])} million, when those four must draw to {F['closed_share_mean_pct']:.1f} per cent of commitment before their investment periods close between September and December 2027 and call CHF {m1(F['four_2027_chf_m'])} million. Not CHF {down} million, which the programme's 2026 calls of CHF {m1(F['programme_calls_2026_chf_m'])} million carried forward would give: it leaves CHF {m1(F['shortfall_next_down_chf_m'])} million of the requirement uncovered.

## 2. Critical Components

1. {names4} end their investment periods on {dates4} with **{shares4} per cent** of commitment drawn at 31 December 2026 and **CHF {m1(F['four_undrawn_chf_m'])} million** undrawn at the plan-date rates
2. The **{F['closed_funds']}** funds whose investment periods ended by 31 December 2026 had drawn **{F['closed_share_min_pct']:.1f} to {F['closed_share_max_pct']:.1f} per cent** of commitment by the end of them, **{F['closed_share_mean_pct']:.1f} per cent** on average
3. Expected 2027 calls are **CHF {m1(F['expected_calls_chf_m'])} million**, **CHF {m1(F['four_2027_chf_m'])} million** of them from the four funds, and the requirement is **CHF {m1(F['requirement_chf_m'])} million**, above CHF {down} million and within CHF {amt} million

## 3. Step-by-Step Solution

1. Took the issued capital-call lines of kapitalabrufe_ausschuettungen_2015-2026.csv (investments, management fees and partnership expenses; cancelled notices out) by value date for the {F['funds_in_register']} commitments in fondsregister_2026-12-31.xlsx, in francs at the 31 December 2026 reference rates of fx_referenzkurse_tagesende.csv (USD {F['plan_date_rates']['USD']:.4f}, EUR {F['plan_date_rates']['EUR']:.4f}), per RL-PM-05 sections 2 and 4.
2. For the {F['closed_funds']} funds whose investment_period_end is on or before 31 December 2026, divided the calls value-dated by that day by commitment: {F['closed_share_min_pct']:.1f} to {F['closed_share_max_pct']:.1f} per cent, {F['closed_share_mean_pct']:.1f} on average, including {slow_names}, which were {slo:.1f} to {shi:.1f} per cent drawn a year before.
3. Estimated the programme's monthly call rate on unfunded commitment in 12-month bands of age from each fund's first call, summed calls over summed unfunded commitment across the record; run from the ends of 2024 and 2025 it forecasts the next year's calls within {F['backtests_pct']['2025']:.1f} and {F['backtests_pct']['2026']:.1f} per cent.
4. Found the ten funds whose investment periods end in 2027: the four are {lo4:.1f} to {hi4:.1f} per cent drawn with CHF {m1(F['four_undrawn_chf_m'])} million undrawn, the other six {lo6:.1f} to {hi6:.1f} per cent.
5. Forecast 2027 month by month: each of the ten calls the balance to {F['closed_share_mean_pct']:.1f} per cent of commitment by its period end and the band rate on what remains after it, every other fund its band rate on its unfunded commitment, capped at what is undrawn: CHF {m1(F['expected_calls_chf_m'])} million, CHF {m1(F['four_2027_chf_m'])} million from the four (the band rates alone give them CHF {m1(F['four_default_chf_m'])} million and the year CHF {m1(F['default_expected_calls_chf_m'])} million).
6. Applied RL-PM-05 section 4: CHF {m1(F['expected_calls_chf_m'])} million plus one tenth, CHF {m1(F['expected_calls_plus_tenth_chf_m'])} million, less the CHF {F['reserve_chf_m']} million reserve is CHF {m1(F['requirement_chf_m'])} million, and the smallest amount on the term sheet's menu that covers it is CHF {amt} million.
7. Took the term sheet's {F['commitment_fee_pct']:.2f} per cent commitment fee and {F['arrangement_fee_pct']:.2f} per cent arrangement fee on the amount: CHF {F['fees_at_amount_chf']:,} at CHF {amt} million and CHF {F['fees_at_next_down_chf']:,} at CHF {down} million.
8. Matched each 2026 credit "Gutschrift Ausschuettung" on programmkonto_lindenhof_2025-2026.csv to its notice in the ledger (Transaktionsreferenz for the custodian's advice, the notice number in Referenz for a keyed notice), counted each credit once and valued the notice's cash amount at the reference rate of the credit's value date, by the fund's strategy and the quarter of the credit: {top} returned the most, CHF {k(D[f'{tcode}_year'])} thousand.

## 4. Deliverable Answers

### facility_election_2027.docx

1. Facility amount for 2027: CHF {amt} million
2. Fees for 2027 at CHF {amt} million: CHF {F['fees_at_amount_chf']:,} (commitment fee CHF {F['commitment_fee_at_amount']:,}, arrangement fee CHF {F['arrangement_fee_at_amount']:,})
3. Fees for 2027 at CHF {down} million: CHF {F['fees_at_next_down_chf']:,} (commitment fee CHF {F['commitment_fee_next_down']:,}, arrangement fee CHF {F['arrangement_fee_next_down']:,})
4. Chart of the cash received from distributions in 2026: one stacked bar per quarter with a segment per strategy, the bars labelled CHF {k(D['total_Q1'])}, {k(D['total_Q2'])}, {k(D['total_Q3'])} and {k(D['total_Q4'])} thousand, the title naming {top} as the strategy that returned the most

### distributions_received_2026.xlsx

1. Distributions received in 2026 by strategy, CHF thousand (Q1, Q2, Q3, Q4, year):
"""
    for c, n in STRATS:
        out += f"   - {n}: {k(D[c + '_Q1'])}, {k(D[c + '_Q2'])}, {k(D[c + '_Q3'])}, {k(D[c + '_Q4'])}, {k(D[c + '_year'])}\n"
    with open(os.path.join(os.path.dirname(HERE), "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("submission.md written")


if __name__ == "__main__":
    main()
