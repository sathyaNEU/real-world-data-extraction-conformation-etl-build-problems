# solver round: round 1, skeptic

**Proxy score 37.6 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 28.1 of 58). Main call missed. 1 of 6 ask items cracked (80 per cent of tokens).

## Main call

golden: Book a collective expected credit loss allowance of AUD 13,773,000 on the PL36 and PL60 personal loans at 30 September 2026.

solver: The collective ECL allowance on PL36 and PL60 personal loans (stages 1 and 2) at 30 September 2026 is A$13,318 thousand, coverage 2.62% on a gross carrying amount of A$509,248 thousand across 40,554 loans, Q1 FY27 scenarios (multiplier 1.06); 343 stage 3 loans left out.

tokens matched 2 of 4 (13,773,000, 30, Book, September)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| ecl_allowance_2026Q3.xlsx | 1 | 2 | 4 | 50% |
| ecl_allowance_2026Q3.xlsx | 2 | 5 | 17 | 29% |
| ecl_allowance_2026Q3.xlsx | 3 | 1 | 9 | 11% |
| ecl_allowance_2026Q3.xlsx | 4 | 3 | 3 | 100% |
| arc_ecl_q3_2026.pptx | 1 | 1 | 2 | 50% |
| arc_ecl_q3_2026.pptx | 2 | 1 | 2 | 50% |

## Solver's path

1. Stage 3: 343 loans 90+ days past due excluded.
2. Hardship in force 612; v3 conversion; score falls 2,635; stage 2 3,265 loans.
3. m = repayments fallen due; remaining term = term - m; past-maturity loans one month.
4. PD(k) = C(m+k) - C(m+k-1), unconditional, times 2.4 for stage 2; LGD 70/76; EAD re-amortised; discounted at contract rate.
5. Scenarios: multiplier 1.06; allowance A$13,318 thousand.

confidence: Medium-high; risk: the PD(k) convention; conditioning on survival gives A$13,773k.

notes: Plain curve increment at month on book (literal reading); conditioning on survival would give A$13,773k.

### ecl_allowance_2026Q3.xlsx (solver's answers)
- Collective ECL allowance at 30 Sep 2026: A$13,318 thousand
- By stage and product: Stage 1 PL36: 17,109 loans; A$138,349 thousand; allowance A$3,129 thousand; coverage 2.26%. Stage 1 PL60: 20,180 loans; A$330,436 thousand; allowance A$7,466 thousand; coverage 2.26%. Stage 2 PL36: 1,421 loans; A$11,728 thousand; allowance A$660 thousand; coverage 5.63%. Stage 2 PL60: 1,844 loans; A$28,735 thousand; allowance A$2,063 thousand; coverage 7.18%
- Allowance by drawdown year and product: 2023 and earlier: PL36 A$5 thousand; PL60 A$573 thousand. 2024: PL36 A$146 thousand; PL60 A$981 thousand. 2025: PL36 A$886 thousand; PL60 A$2,269 thousand. 2026: PL36 A$2,753 thousand; PL60 A$5,706 thousand
- Stage 3 loans left out: 343

### arc_ecl_q3_2026.pptx (solver's answers)
- Slide 1: Allowance A$13,318 thousand; stage and product table as above
- Slide 2: Column chart by drawdown year: largest bar 2026 PL60 A$5,706 thousand
