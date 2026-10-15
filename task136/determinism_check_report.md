# Judge verdict, task136 (fresh pass after redesign)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is required and no rerun is implied. One optional hardening is listed under Fix.

**Why:** The call is forced by NPP-114 rev 3 and the shipped data. Every committed figure reproduced from the files: the base forecasts, the bulk-buy increments, the 2029 excesses and all 32 per-feeder DER cells. The decisive quantity is the incremental uptake of a bulk-buy, and the prompt asks how much each bulk-buy "will raise its feeder's PV". That wording asks for the increment over what the suburb would have lodged anyway, not the installer's gross count. Every controlled estimator I tried puts the incremental rate inside the band that yields YRB27. Only a biased flat baseline or a letterbox denominator leaves the band.

**Evidence (recomputed from the bundle):**

| Item | Golden | My recompute | Source |
|---|---|---|---|
| Connected capacity 31 Aug 2026, YRB27 / YRB24 | 11,645 / 17,845 kW | 11,645.0 / 17,844.8 | applications csv + legacy equipment, feeder from network model, last connected, removed excluded |
| Trend kW/yr, YRB27 / YRB24 | 1,245 / 1,935 | 1,245 / 1,935 | FY23-24 to FY25-26 increases less program systems first connected |
| Base forecast | 15,380 / 23,648 | 15,380 / 23,648 | |
| FY25-26 average new inverter | 9.35 / 9.15 kW | 9.348 / 9.149 | |
| Owner-occupied houses without PV, 1 Sep 2026 (land use 02, R1, via xref) | 4,537 Bindarra Waters / 1,857 Wattleview | 4,537 / 1,857 | |
| Net systems from 7 campaigns | 627.8 on 15,349 houses = 4.09 per 100 | 627.8 on 15,349 = 4.09 | year-before ratio against later-campaign suburbs |
| Bulk-buy increments | 1.7 MW / 0.7 MW | 1.70 / 0.71 | |
| 2029 excess (hosting capacity 23.65 / 14.19 / 21.79 MW, 2029 spring case) | YRB27 1.9, YRB24 1.7, gap 0.2, YRB22 1.39 | 1.90 / 1.70 / 0.20 / 1.39 | hosting capacity PDF table, 2029 column |
| DER sites, first lodged FY25-26, kW, kWh, all 8 feeders | block 4 | all match, e.g. YRB21 3,443 / 98 / 19,280 / 3,260 | der_register csv, reallocations, network model |

Competing answers and the forks they open. Define x as the net systems per 100 owner-occupied houses without PV. YRB27 wins for 1.2 < x < 4.94, YRB22 below 1.2 and YRB24 above 4.94.

- **Gross uptake (the easy route):** 9.32 per 100 houses without PV (installed over the same base), or 4.35 per 100 letterboxed homes. YRB24 wins at 3.9 MW (2.8 MW for YRB27) or 4.2 MW (2.5 MW for YRB27). This is the intended trap. The "raise" and "impact" wording and NPP 3.2, which strips program systems from the trend, argue against adding gross installs, because that double-counts the organic adopters.
- **Ignoring the bulk-buys:** YRB22 at 1.39 MW. This is rejected by the prompt's "counting".
- **Controlled net estimators:** all land inside the YRB27 band.
  - Control set: later campaigns only 4.09, never-campaigned suburbs only 4.07, both 4.09.
  - Additive per-house rate version: 3.66.
  - Per-campaign rates are tight, 3.8 to 4.3 per 100.
- **Residual forks:**
  - A flat own-baseline ("year before times three", no control) gives about 5.3 to 5.7, which makes YRB24 win by roughly 0.1 MW. It is biased: control suburbs grow 3.3 to 3.8 times over the window, not 3.0.
  - Net systems per letterboxed home (2.10) gives YRB24 2.0 against YRB27 1.8. It is contradicted by the data. Per eligible house the rate is stable (CV about 4 percent), per letterboxed home it is not (1.3 to 2.3), and the program terms restrict the offer to owner-occupiers of houses.
  - Neither fork is ruled out by a sentence in the files. The data and the wording separate them, so I judge the call forced. The margin to the flip is 0.85 per 100 (about 20 percent).
- **Feeder attribution:** NPP 3.1 and 2.2 pin the network model at the base date. Using feeder_at_application for the trend gives 15,426 / 23,583 kW. The call holds but the runner-up would read 1.6 MW. The literal NPP reading is the golden.
- **DER asks:** the following variants change the answer, and the golden reading is the literal one in each case.
  - Using the register's own feeder column changes the counts by up to 200 sites.
  - Counting "first lodged" on active connections only adds 12 to 53 sites per feeder.
  - Not collapsing the pre-July-2024 two-inverter rows or the SBR stacks inflates kW by 460 to 770 and kWh by 880 to 1,780.
  - Each device rule is derivable from the files (model nameplate against rated kW, and 3.2 kWh times the row count against the stack total).
  - The reallocation reasons other than the builder's temporary supply change nothing.

Other gates:
- Gate B: every decisive fact is in a shipped file. The 6-month rule and the written confirmation (clause 4.2) are met by the 14 Aug 2026 letter and the 27 Nov 2026 close. Hosting capacity is the 2029 column. The peak-demand workbook and the rebate file are unused distractors.
- Gate E: the call, runner-up, gap, increments and per-feeder asks are each single-valued with units and rounding stated.

**Files/Hygiene:** PASS. 15 files: 9 csv, 3 xlsx, 3 pdf (three formats). Two files exceed 25,000 rows (applications 27,854, rates roll 64,795). There are at least two distractors (feeder_peak_demand_forecast, home_battery_rebate_approvals). The manifest and dictionary carry source, date and owner. Authoring-flavoured phrasing is limited to the council letter's "treat this letter as Council's written confirmation" and the NPP revision note. I judge both non-exclusionary. Feeder transfers, 11-character NMIs, legacy-migrated inverters and reallocated NMIs are realistic mess. Dates are coherent (extract 1 Sep 2026, base 31 Aug 2026). No public-data contamination is evident. Nothing is exclusion-level.

**Stump power:** Good. The strong-model failure route is the gross uptake from the program summary ("systems installed" over letterboxed homes or houses), which yields YRB24 and a wrong 1.7 MW bulk-buy figure. The second route ignores the bulk-buys and yields YRB22. The DiD-style estimate on a staggered rollout must be built from house-level first applications, so the trap does not disappear after the data is cleaned. The ask layer (duplicate device rows, NMI mapping, feeder source) adds independent stumping surface.

**Stumping type:** `mechanism: statistical_rigor` (incremental program impact against a counterfactual), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The program summary's counts are honest. The difficulty is estimating the incremental effect on clean data (a causal comparison group with pull-forward), which is a FINE-numbers shape. On clean data the task still stumps. Borderline note: a reader could call gross-versus-net a lens swap. I judge it a causal-estimand question, not a defect catch.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: hosting capacity, feeder connected-capacity trend and program free-rider/pull-forward impact are distribution-planning work. They do not survive swapping in another field's nouns.
- Layer 1: NMI keys (11-character, reallocations), legacy-migrated inverter equipment, feeder transfers, duplicated device rows. Layer 2: net-of-baseline program impact via a staggered control comparison, then scaled to the eligible pool.
- Easy route: take the campaigns' installed count per home, which gives YRB24 at 1.7 MW for Bindarra Waters becoming 3.9 MW and the wrong feeder. A strong analyst who read every field correctly still gets this wrong.

**Fix:** none required (fix location: none). Optional hardening, with no rerun needed because the answer would not move: have the prompt's "raise" be explicit that the increment is over what the suburb would have lodged anyway (the WHAT, not the HOW), which closes the flat-baseline and letterbox-denominator forks on the literal reading. Do not name the estimator.
