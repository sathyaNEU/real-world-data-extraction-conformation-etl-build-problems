# Verdict, task136 (re-judge b)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is required and no rerun. One optional watch item is the battery-row semantics (see Evidence).

**Why:** The shipped text forces YRB24 on a literal execution of NPP-114. Connected capacity is taken from the network model at 31 Aug 2026. The trend is the three-FY average net of program systems. The bulk-buy yield comes from "the distributor's records of past programs" (cl. 4.1). The seven past campaigns, recomputed from the connection records, rates roll and xref, put systems on a near-constant 4.55 to 4.63 percent of owner-occupied houses still without PV at sign-up (CV 0.6 percent). Every other base is far from constant: per letterbox CV 25 percent, per owner-occupied house 30 percent, per address without PV 28 percent. So the data separates the candidate calibrations. Gates A to E pass for the main call and for every supplementary figure.

## Evidence (all recomputed from target/; "ok" = reproduced)

| Item | Source | Recomputed | Golden | Result |
|---|---|---|---|---|
| YRB24 connected capacity at 31 Aug 2026 | eg_connection_applications, legacy_inverter_equipment, nmi_network_model | 3,063.8 kW | 3,064 | ok |
| YRB24 and YRB22 trend per year | same, with program systems netted out | 432.2 and 826.1 kW | 432 and 826 | ok |
| Past campaign rates | applications (program_ref), xref, rates roll (land use 02, R1) | 4.55 to 4.63 percent each, 4.58 percent pooled (358 / 7,817) | same | ok |
| Systems per past campaign | program_ref counts (34, 48, 104, 78, 55, 39) | equal the "Systems installed" figures in solar_streets_program_summary.xlsx | | ok |
| Owner-occupied houses without PV, less FY2025-26 first applications | | Bindarra Waters 5,275, Wattleview 668 | 5,275 and 668 | ok |
| Bulk-buy systems | | 241.6 and 30.6, which round to **240 and 30** | 240 and 30 | ok |
| Average inverter, FY2025-26 New connections | | YRB24 7.252 kW, YRB27 6.671 kW | 7.25 and 6.67 | ok |
| Bulk-buy kW | | 1,752 kW on YRB24, 204 kW on YRB27 | | ok |
| Hosting capacity, 2029 spring minimum-demand case | yarrabin_hosting_capacity_assessment_2026.pdf | YRB24 4.22 MW, YRB22 14.66 MW | | ok |
| Excess over hosting capacity | | YRB24 6.112 less 4.22 = **1.89 MW**; YRB22 16.168 less 14.66 = **1.51 MW**; YRB25 1.24; YRB21 1.11 | 1.9 and 1.5, gap 0.4 | ok |

The unrounded gap is 0.384 MW and the gap of the rounded figures is 0.4 MW, so both agree.

Bindarra Waters sits wholly on YRB24 (6,264 NMIs) and Wattleview wholly on YRB27 (3,329 NMIs). Both campaigns pass cl. 4.1 (sign-ups close 26 Nov 2027, more than six months before 31 Aug 2029) and cl. 4.3 (the council letter SS/2027/01 confirms them in writing).

**Competing answers tested.**
- Letterbox-rate method: about 90 systems in Bindarra Waters, YRB24 at 1.35 MW, so YRB22 wins.
- Mean campaign, owner-occupied-house base, address base and no bulk-buys: YRB22 wins in each case.
- YRB24 holds the lead down to a rate of about 3.6 percent (break-even about 189 systems at 7.25 kW). It holds at 7.16 kW (all FY2025-26 connections), 241.6 and 240 systems alike, feeder_at_application in place of the model, ignoring historic removals, and not netting program systems. The nearest-ten bulk-buy results (240 and 30) are stable under every roll-forward, withdrawn-handling and connection-date variant I ran.
- The data therefore pins the calibration. The 4.58 percent base is also one the program terms sheet makes natural (owner-occupiers of houses only; tenants and units are excluded).

**Supplementary figures.** Not shown / sites with no connected system:

| Feeder | Not shown | No connected system |
|---|---|---|
| YRB21 | 12 | 11 |
| YRB22 | 8 | 12 |
| YRB23 | 11 | 10 |
| YRB24 | 2 | 8 |
| YRB25 | 6 | 5 |
| YRB26 | 14 | 4 |
| YRB27 | 14 | 9 |
| YRB28 | 12 | 4 |

All reproduced exactly (first ten characters of 11-character NMIs, plus the reallocations mapping).
- The counts are identical whether the Register match uses active connections only or any status. They are identical counting NMIs or AC connections.
- Skipping the truncation or the reallocation gives counts of 123 to 367 on the wrong side, so the cleaning matters.

Battery storage per active AC connection, counted once: 2,439.7 / 1,767.9 / 1,800.8 / 392.5 / 900.5 / 1,588.4 / 1,738.1 / 1,311.2 kWh. These round to 2,440 / 1,770 / 1,800 / 390 / 900 / 1,590 / 1,740 / 1,310, matching the golden. No site carries two active battery connections.

**Residual fork (watch item, not a gate failure).**
- The dictionary does not say that the identical `storage_capacity_kwh` repeated on each of the 1 to 5 battery rows of an AC connection is the system total.
- Literal row-summing gives 6,125 kWh for YRB21, 4,114 for YRB22 and 915 for YRB24, about 2.3 to 3.1 times the golden.
- The files point to the once-per-connection reading. The value is independent of the row count (k = 1 to 5). It is a whole-battery size (9.6 to 16.2 kWh), the same range as `battery_kwh` in the applications (maximum 15.4) and `nominal_kwh` in the rebate file (maximum 16). Row-summing would imply 48 to 81 kWh home batteries.
- Resolvable by inference from the shipped files, so I treat it as a low-to-moderate risk on one supplementary ask. A single dictionary line would close it, but that is an input change, so it is optional.

## Files/Hygiene

**PASS.**
- 15 files in three formats: 9 csv (including export_manifest), 3 xlsx, 3 pdf.
- Largest file: the network model with 47,515 rows. Eight data extracts are at or above 17,000 rows.
- Distractors: feeder_peak_demand_forecast (summer-peak MVA), home_battery_rebate_approvals, and the summary sheet's letterbox and installer columns, which tempt the letterbox method.
- No visible authoring or benchmark language, no hidden sheets or comments, and clean PDF and xlsx metadata (named creators).
- Nothing exclusion-level.
- Minor temporal note: data_dictionary.xlsx was modified 2 Sep 2026 but describes the 5 Sep 2026 DER Register extract. It is harmless and in-house fixable.
- Cross-batch: I did not search other packages, as instructed. The shipped files show no self-evident duplicate.

## Stump power

Good.
- The summary workbook invites "systems per homes letterboxed", a defensible-looking method that gives about 90 systems in Bindarra Waters and puts YRB22 first. A strong solver who also built the connected-capacity and trend ladder correctly would fail the call that way.
- Choosing the right unit of analysis needs a join chain: rates roll land use and rating, then xref, then applications received before each sign-up date, then the withdrawn exclusion. It is validated by the near-zero CV across seven campaigns.
- The supplementary asks add independent data work: NMI truncation, reallocations, Register status, and the battery-row repeat.
- The margin is 0.38 MW, thin but clean and not contested (see Evidence).

## Stumping type

mechanism: method_or_model_selection (with etl_conformance); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

No reported number is wrong. The summary sheet's systems and letterbox figures are correct, and the difficulty is picking, from seven campaigns, the base on which the yield is stable. On clean data it would still stump.

## Three rules

domain: pass, layers: pass, decisive_step: analytical

- **Domain:** distribution-network planning. The deciding quantity is forecast micro-EG connected capacity against hosting capacity, plus a program-yield estimate, which is work the field itself does. A swap to another field's nouns breaks the task.
- **Layer 1 (messy data):** legacy inverter migration, reallocated NMIs, 11-character NMIs, superseded feeder-at-application, alterations replacing systems, and the repeated battery rows.
- **Layer 2 (rigour):** calibrating program yield on the stable base and applying NPP-114's trend and assignment.
- **Easy route:** a capable analyst who cleans everything correctly and scales by letterbox or by all owner-occupied houses gets about 90 systems, 1.35 MW over, and so names YRB22 (1.5 MW) as the winner.

## Fix

none. Optional only: one line in data_dictionary.xlsx on module-row repetition for the battery capacity (input_files), and align its modified date with the 5 Sep extract.

## Disposition

Approved as judged (judge-task136b, the re-judge after the pass-1 FIX_NOW in determinism_check_report_round1.md). No graded
figure, document text, golden, write-up or prompt changed.

1. **Watch item (Ask B's repeated battery capacity).** Left unwritten in the pack: a dictionary line saying the value
   repeats on each module row would announce the ask's device. The data admits only the once-per-connection reading,
   now asserted in `checks.py` and recorded in the design note's Ask B. The value is identical on every battery row of
   a connection and does not rise with the module rows (mean 11.8 kWh on one row, 10.8 to 13.1 on two to five;
   Spearman 0.05). It runs 9.6 to 16.2 kWh per connection, against the register's `battery_kwh` (9.6 to 15.4) and the
   rebate file's `nominal_kwh` (9.6 to 16.0). By module count, its median ratio to the site's own connected
   `battery_kwh` is 0.84 to 1.00, where the row sums' is 1.7 to 4.7.
2. **Hygiene note (the dictionary dated 2 September for the 5 September extract).** Fixed as a date only:
   `data_dictionary.xlsx` is dated 7 September 2026 in its `docProps/core.xml` modified stamp and in
   `export_manifest.csv`, and `checks.py` asserts the dictionary on or after every extract it lists. The optional
   dictionary line is declined (item 1).
3. **The shipped bundle against the judged one.** The final rebuild differs from the pack the re-judge read in that
   date alone: 13 of 15 files byte-identical, the dictionary differing only in its modified stamp and the manifest only
   in the dictionary's date cell; both goldens, `figures.json`, `metadata.json` and `submission.md` byte-identical.
   Free gates on it: `checks.py` 293 PASS; `verify.py` 123 PASS; two builds byte-identical; `figures_check.py` exit 0
   (50 figures); `precut.py` exit 0; `voice-check.py` PASS; `leak.py` REVIEW (no LEAK, sweep 11 clean, the same seven
   lines, each answered in the design note); container audit clean; `guard.py surface` 0 promoted; `guard.py heart`
   WARN (`overuse.gate_g`, `repeat.question_form`, answered at the draw); `freeze.py check task136 --mode determinism`
   PASS. `target.zip` is cut from that rebuild by the generator's `cut_zip` (15 members, equal to `target/`; sha256
   c80a36f8a7c914bd492d0fe3635e3ef6ced9141b517a6d9810360eed354395d9).
