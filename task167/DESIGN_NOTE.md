# task167 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task167.json`, registered 2026-10-18T06:59:01Z, guard WARN (no BLOCK).
  WARNs answered: driver.near 0.12 against task501 v3 (its catch-up is driven by a deadline, what a fund must still
  place before its investment period ends; here it is a class of schedule shape that each fund's own first-year
  notices reveal, and no deadline enters); overuse.objective and overuse.gate_g (Forecasting is the lane's most
  wanted objective, and two schedules pinned by the funds that have passed the forward ages is the honest Gate G);
  repeat.decision against task168 (the call is an amount, the reserve). The older same-puzzle and same-driver
  matches (population, E) carry one differentiation line each on the card.
- **Pairing:** Nonprofit & Grant-making (house domain `nonprofit-grant-making`, task type endowment management, card
  subdomain `other`), client domain General Statistics & Data Science. Objective Forecasting & Predictive Modeling:
  the reserve is next year's expected capital calls on commitments already made, a value the supplied fund history
  pins and a window (calendar 2027) not yet open.
- **Seed:** FC38, re-rooted by the coordinator on 2026-10-18 after the measurement in `## Tried and rejected` (v1).
  Kept from the re-root: the world (a grant-making foundation's private-markets programme), the decision (the call
  reserve the liquidity policy requires for the coming year) and the quantity (next year's capital calls on existing
  unfunded commitments).
- **Strategy:** `forecast_method_backtest`, pattern E (G14's form) with G16 as the frame. The natural fit, a call
  schedule by fund age pooled over every fund (Takahashi-Alexander rates on the undrawn balance, or shares of
  commitment by age), is wrong out of sample for the funds that bridge their first deals on a subscription line:
  they call almost nothing but fees in their first year and most of their capital in their second and third. No
  field names the class; each fund's first-year notices show it. The 2025 re-entry programme spends 2027 in its
  second year, and its funds' fee-only 2026 puts them in that class.
- **Furniture (honest alternatives where the first choice was banned at the draw):** forum `board_of_directors` (the
  foundation is a Minnesota nonprofit corporation; its board confirms the call reserve at its January meeting);
  forcing event `vote_or_meeting` (that meeting); organisation `foundation_or_funder`; role `compliance_or_audit`
  (the investment office's director of investment risk, who certifies the reserve; the treasurer,
  `finance_controller`, was banned against task198); context artifact `close_out_summary` (the administrator's
  year-end capital account summary the certification works from; `filed_standard` banned against task168);
  calibration `none` (the back-test runs on the spine's own record, no separate organ ships).
- **Personas** (`guard.py names --geo 'United States' --seed 167`): Troy Stein, Kristin Brown, Brian Erickson. Lisa
  Stone and Sara Salazar were passed over (first names on task118 and task265); none appears in the prompt.

## Tried and rejected

- v1, the tail test on appraisal-smoothed marks (2026-10-18, on paper, never registered): the largest one-off
  outflow the endowment could take while the tenth percentile of its value ten years on stayed above a share of
  today's, with the private sleeve's marks de-smoothed before the tail is read. Died on resampling noise: on a
  148-quarter record (37 years) the ten-year tenth percentile moves by a standard deviation of about $281 million
  between independent and block-of-eight bootstrap draws on the same record (24 replicate worlds, 8,000 paths each),
  the de-smoothing variants (Geltner first-order, Getmansky-Lo-Makarov with two and three lags) move it by more, and
  back-filling the shorter private history against the longer public one scatters it by about $160 million. No
  realistic draw step is deterministic, and filing the resampling scheme to close it turns the de-smoothing step into
  a literal fork the judge executes.
- v2 draft, a call schedule broken by vintage date (2026-10-18, on paper, never registered): every fund from the
  2018 vintage on called little in year one and most in years two and three. Died at the reflex sweep on paper: any
  recent calendar window holds only post-break funds at young ages, so a plain recency choice reaches the golden,
  while a softer break leaves the cut year a knob; and abstractly it repeats task501 v4's pooled regimes (the
  forward window's regime selected from a pool of two). Replaced by the class read from each fund's own first-year
  notices, spread across vintages and strategies so no date cut, window or visible attribute isolates it.
