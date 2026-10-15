# Verdict, task136

**Verdict:** DETERMINISTIC (one intermediate figure, YRB22 connected capacity 13,683 kW, does not reproduce to the kW; immaterial, see Evidence).

**Disposition:** FIX_NOW (optional). Restate the YRB22 intermediate in the solution text (13,690 kW, or note the unkeyed legacy-number collision). Every graded figure and every file stay as they are, no model rerun.

**Why:** The shipped text, read word for word, forces YRB24 (1.9 MW above its 4.22 MW 2029 spring minimum-demand hosting capacity) over YRB22 (1.5 MW), gap 0.4 MW. NPP-114 2.2, 3.1-3.2, 4.1-4.3, 5.1, 6.1 and 7.1 file the connected-capacity definition, the trend, the 4.3 written-confirmation test (met by the council letter), the average-inverter rule, the hosting-capacity source and the rounding. The one step the procedure leaves open is the base a past campaign's yield is scaled by, and the data separates the candidates sharply (CV 0.6% against 25-30%). All eight supplementary pairs and the storage figures reproduce.

**Evidence** (all recomputed from target/):

| Item | Recomputed | Source | Reproduced |
|---|---|---|---|
| YRB24 connected capacity at 31 Aug 2026 | 3,063.8 kW | eg_connection_applications (latest connected per NMI, alteration replaces, removal excluded), feeder from nmi_network_model | yes (3,064) |
| YRB22 connected capacity | 13,689.8 kW (file-order or panel_kwp pairing of colliding legacy numbers); 13,766.5 naive; 13,672 to 13,697 across pairings | same, plus legacy_inverter_equipment | NO to the kW (golden 13,683); effect on YRB22 excess under 0.01 MW |
| Trend, FY23-24 to FY25-26, less program systems first connected | YRB24 432.2, YRB22 826.1 kW/yr (YRB26 FY24 -357.6 and YRB21 FY25 -259.8 program deductions) | applications, program_ref | yes (432, 826) |
| Past campaign yield on owner-occupied houses (02/R1) with no non-withdrawn application received before sign-ups | 34/740, 48/1054, 104/2270, 37/810, 41/885, 55/1207, 39/851 = 4.55% to 4.63%, pooled 358/7817 = 4.58% | rates roll, xref, applications, program summary | yes |
| Alternative bases, CV across 7 campaigns | per letterbox 25.5%, per owner-occupied house 30.1%, per residential (02/08/09) untapped 27.5%, systems per campaign (mean 51) | summary xlsx, rates roll | confirms the invariant exists only on untapped owner-occupied houses |
| Pool (no PV at 31 Aug 2026 less FY25-26 first applications) | Bindarra Waters 5,299 - 24 = 5,275; Wattleview 720 - 52 = 668 | same | yes |
| Bulk-buy systems | 241.6 and 30.6, so 240 and 30 (without the FY deduction 242.7 and 33.0, same tens) | | yes |
| Average new inverter, FY25-26 New applications | YRB24 7.252, YRB27 6.671 kW | applications | yes |
| Forecast PV 2029 | YRB24 6.112 MW (excess 1.89), YRB22 16.168 (1.508), YRB27 15.007 (1.017), YRB21 18.92 (1.11), YRB25 1.24, others lower | | yes: 1.9, 1.5, gap 0.38 reported 0.4, consistent with 1.9 minus 1.5 |
| Bindarra Waters / Wattleview feeders | wholly YRB24 / wholly YRB27 in the network model | | yes |
| Connected, not shown in DER Register (active, NMI first ten characters, builders' temporary NMIs mapped through reallocations) YRB21 to YRB28 | 12, 8, 11, 2, 6, 14, 14, 12 | der_register, reallocations | yes (same under any-status match) |
| Active register sites with no connected system (distinct NMIs, register feeder column) | 11, 12, 10, 8, 5, 4, 9, 4 | der_register, reallocations | yes (20 active sites sit on NMIs absent from the network model; the register feeder column places them) |
| Storage at active sites, each AC connection counted once | 2,439.7 / 1,767.9 / 1,800.8 / 392.5 / 900.5 / 1,588.4 / 1,738.1 / 1,311.2 kWh, so 2,440 / 1,770 / 1,800 / 390 / 900 / 1,590 / 1,740 / 1,310 | der_register | yes; "once per connection" is supported in the files: for connections with 3 to 5 rows the application battery_kwh matches the repeated value (ratio about 1.0), not the row sum |
| Hosting capacity 2029 case | 17.81, 14.66, 12.03, 4.22, 6.75, 14.71, 13.99, 11.54 | assessment PDF table | yes (customers per feeder equal network-model NMI counts) |

Forks tested:
- Yield base (the only real open choice). Per letterbox (about 1.45% of 6,240 gives about 90 systems), per owner-occupied house, per untapped residential address, per average campaign (about 51 each) all put YRB22 first. Only the untapped owner-occupied base gives YRB24. NPP-114 4.1 ("records of past programs ... indicate") does not name the base. It is closed only by the data, through the stable rate, and the program terms (offer to owner-occupiers of houses only) support it. This is the residual determinism risk. I accept it as a data-separated method selection, not a semantic fork.
- Definition of "no PV" (withdrawn counted or not, received or connected before opening). The pooled rate stays 4.53% to 4.66%. Bindarra Waters stays at 239 to 246, which is 240 except one over-inclusive variant (withdrawn counted as PV, no FY deduction: 245.8, rounding to 250). Neither version moves the call or the 1.9 MW.
- Colliding legacy application numbers. 40 numbers are shared by two applications and two rows in legacy_inverter_equipment, with no key beyond file order and panel_kwp. Summing both rows overstates capacity (YRB22 +77 kW). Pairing variants move feeders by at most about 40 kW and YRB22 excess by under 0.02 MW.
- Feeder basis (feeder_at_application versus network-model feeder). NPP-114 3.1 and 2.2 specify the model, so this is closed.

**Files/Hygiene:** PASS. 15 files, 3 formats (9 csv, 3 xlsx, 3 pdf), one 47,515-row table and several others over 17,000. Distractors: the battery rebate approvals, the summer-peak demand forecast, and the program summary's letterbox and contract columns. No README, authoring or "synthetic" text. PDF and xlsx metadata name in-fiction authors. Minor: hosting-assessment PDF created 22 Jul against 24 Jul issue date; the DER extract is dated 5 Sep but carries no event after 31 Aug. No exclusion-level finding. No public data.

**Stump power:** High-moderate. A strong solver reading the council letter and program summary will most naturally scale by letterboxed homes (6,240), by owner-occupied houses or by an average campaign, and then rank YRB22 first (about 1.5 against YRB24 at or under 1.2 MW). Reaching YRB24 needs testing which base the seven past campaigns hold steady on, applying the unit, the untapped pool at sign-up and the feeder's new-system average. Gate F too-easy signals: none; no shipped document names the base.

**Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Every reported number is correct (letterbox counts, systems installed); the difficulty is choosing the yield base and carrying it to the new suburbs. On perfectly clean data the task still stumps.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is distribution-network micro-EG hosting-capacity forecasting per a planning procedure, with a bulk-buy program yield estimated from past campaigns. Layer 1 is the mess: 11-character and builder's-temporary NMIs, migrated legacy inverters with recycled numbers, alterations and removals, a feeder transfer, repeated battery rows. Layer 2 is the estimand of campaign yield. The easy route (per letterboxed home or per owner-occupied house, about 90 to 140 systems at Bindarra Waters) gives YRB22 at 1.5 MW; the right answer is YRB24 at 1.9 MW.

**Fix:** solution only. Restate the YRB22 base capacity (13,690 kW, or the pairing note) in the solution steps; no change to the prompt or the input files. Optional: if the author wants the yield base closed more firmly, name no base but keep the data signal as is, since filing it would remove the stump.

## Disposition

Applied in one generator pass by the build session and committed PAUSED for the main session's re-judge. The main call
(YRB24), the stump, the ladder, the default path and every graded figure are unchanged: `freeze.py check task136 --mode
determinism` PASS, with the twelve non-graded step keys named in item 1 allowed (their reason is in the design note's
`## Tried and rejected` and fork row SF23).

1. **The FIX_NOW (YRB22's connected capacity).** Closed in the data, not only restated. The 40 shared legacy application
   numbers were a generator artifact (numbers drawn with replacement), and they reached further than the intermediate: a
   summed join (13,766 kW) files YRB22 at 1.6 MW and the gap at 0.3, both graded. A legacy system never reissues an
   application number, so each is now issued once: the later application of each pair carries a new number in both
   `eg_connection_applications_20260901.csv` and `legacy_inverter_equipment.csv` (that column only; every inverter
   count and every other row unchanged). A lookup, a merge, a first-match join, file order and panel size now select the
   same inverter for every migrated row: YRB22 13,689.8 kW, the judge's figure. Asserted in `checks.py` (SF23: both
   columns unique, the join one to one, the three joins equal row by row) and in `verify.py` on its own code path.
   - The write-up's step 1 drops YRB22's figure, which no ask or component owes. It keeps YRB24's 3,064 kW, which
     reproduced.
   - Non-graded step intermediates that moved to the true pairing, in `figures.json` and the golden's forecast sheet:
     - connected capacity: YRB21 16,126 to 16,136 kW, YRB22 13,683 to 13,690, YRB23 10,752 to 10,742, YRB26 12,018 to
       11,984, YRB27 12,534 to 12,540;
     - YRB23's trend: 575 to 576 kW a year;
     - the same five feeders' 2029 forecasts;
     - YRB26's excess: -0.6 to -0.7 MW (-0.657 unrounded).
   - The assessment's eight 2029 hosting capacities stand, held by resetting the generator's targets and asserted equal
     to the published figures.
   - Graded figures:
     - YRB24 1.892 MW (1.9), YRB22 1.508 (1.5, as the judge computed) and the gap 0.384 (0.4);
     - 240 and 30 systems, 6.1 MW, 4.22 MW, 4.55 to 4.63 and 4.58 per cent;
     - both asks, all unchanged.
2. **The yield-base reading (the reader's per-letterbox 90 and 50).** Recorded in the design note's fork table as ruled
   out by the data (SF16). By sample coefficient of variation, the seven campaigns vary 0.6 per cent per untapped
   owner-occupied house against 25.5 per letterbox, 30.1 per owner-occupied house and 27.5 per address without PV. The
   pooled per-letterbox reading (1.45 per cent) files YRB22 at 1.5 MW with 90 and 50 systems and YRB24 fifth. Asserted in
   `checks.py`. No prompt or NPP-114 change, and no base filed: as the judge's optional note says, filing it would remove
   the stump.
3. **The over-inclusive variant (a withdrawn application counted as PV: 245.8, rounding to 250).** It was not filed
   before. The dictionary listed the register's statuses without defining them, and the seven campaigns fit the variant
   about as well (4.66 per cent pooled), so the records alone cannot separate it. With the first-year deduction it gives
   244.6, 0.4 systems from the edge.
   - NPP-114 has no first-year rule to cite. The deduction on its own converges (241.6 with it, 242.7 without, both 240;
     SF11, asserted), so the withdrawn reading is the half that has to be closed.
   - The data dictionary now defines each status value, among them "Withdrawn: withdrawn by the applicant or lapsed
     before connection; nothing was connected under the application." A house whose only application was withdrawn is
     therefore without PV. The definition names no device.
   - Asserted in `checks.py` (SF24): the definition ships, no withdrawn row carries a connection, an inverter or a legacy
     number, and the variant's figures are as stated. Document changed: `data_dictionary.xlsx`.
4. **Realism (the reader).** The assessment's 2026 case now follows each feeder's change in spring minimum demand, at a
   sensitivity inside the report's own stated 0.6 to 1.2 (asserted in `checks.py` and `verify.py`).
   - From 2026 to 2029, hosting capacity falls on six feeders by 0.04 to 0.70 MW and rises on YRB23 (0.02) and on YRB24
     (0.29, its minimum demand growing with the estate).
   - The 2029 columns, the route lengths and the customer counts are unchanged, so no call or MW figure moved.
   - The 2026 case still files YRB24 (SF21). Document changed: `yarrabin_hosting_capacity_assessment_2026.pdf` (the
     2026 columns only).
5. **Fingerprint gate (not a judge finding).** `guard.py heart` had moved to BLOCK on `ban.forum`. task128's
   architecture 3 was drawn the same day, so it comes before this build by draw key, and it carries `executive_team`. No
   shipped file or prompt sentence names a forum, so the card now carries `line_manager_or_team`. Heart is WARN
   (`overuse.gate_g`, `repeat.question_form`).
6. **Rebuild and free gates.**
   - Generator and figures: `checks.py` 284 PASS; `verify.py` 123 PASS; two builds byte-identical; `figures_check.py`
     exit 0 (50 figures); `precut.py` exit 0 (38 checks, `voice-check.py` included).
   - Leak: `leak.py --asof 2026-10-12` REVIEW, the same seven lines (no LEAK, sweep 11 clean).
   - Fingerprint: `guard.py surface` 0 promoted (nearest 0.094); `guard.py heart` WARN; `guard.py validate` clean.
   - Container audit clean, and `target.zip` equal to `target/` by content.
   - Changed under `target/`: the connection register and the legacy equipment table (40 legacy numbers each), the
     data dictionary and the hosting capacity assessment. The other eleven pack files are byte-identical.
   - Two documents changed, so the leak reader re-reads them before the re-judge.
