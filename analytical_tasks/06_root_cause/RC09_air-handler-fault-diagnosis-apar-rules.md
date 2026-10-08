# RC09 — An air-handling unit using 30% more energy: stuck damper, biased sensor or leaking valve?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Facilities and data-centre HVAC fault diagnosis; any control system where faults masquerade as one another in aggregate energy |
| Domain | Building systems / facilities engineering |
| Task shape | 18 · Hypotheses versus evidence (candidate faults × rule-based evidence by operating mode; the fault the technician is sent to fix) |
| Core method | Mode-specific air-handler performance assessment rules (APAR): classify each interval into operating modes (heating, economiser cooling, mechanical cooling with economiser, mechanical cooling); evaluate rules (e.g., mixed-air temperature between return and outdoor air; supply air temperature tracking setpoint; valve command at 0% with coil ΔT; outdoor-air fraction versus damper command); count rule violations per mode; map rule patterns to faults |
| Analytical stump | Energy or comfort complaints in aggregate cannot distinguish faults. A leaking heating valve and a biased mixed-air sensor both raise energy, but they violate different rules in different modes. Evaluating rules without mode classification, or across all hours, misattributes the fault |
| Primary sources | LBNL "Fault detection and diagnostics datasets" for air-handling units (experimental and field data with labelled fault periods) |

## 1. The real-world situation

A facilities team noticed that an air-handling unit's energy use rose about 30% after a maintenance visit. The contractor suspected a failing economiser
damper. The controls engineer wants an evidence-based diagnosis before ordering parts.

## 2. The decision (one deterministic recommendation)

**The fault diagnosed (from stuck outdoor-air damper, mixed-air temperature sensor bias, leaking heating valve, cooling valve stuck) by the rule-pattern
match in the post-maintenance period, with the violation rates that support it.**

Rules (controls memo):

* Data: the LBNL AHU dataset in memo (1-minute data with temperatures, valve and damper commands, fan status); the evaluation window is the period
  labelled as fault-free baseline plus the unlabelled "post-maintenance" window per memo (labels used for validation only).
* Modes from heating valve, cooling valve and damper commands (APAR mode definitions).
* Rules (APAR subset in `apar_rules.json`) evaluated with the memo's tolerances in steady-state intervals (exclude 30 minutes after mode changes).
* Rule violation rate per mode; fault signatures (which rules violated in which modes) in `fault_signature_table.json`.
* Diagnosis: the fault whose signature has the highest match score (share of signature rules violated above 20% minus share of non-signature rules
  violated above 20%).
* Validate against the dataset's fault label for the period.

## 3. Why capable analysts get it wrong

* Energy totals are the visible symptom.
* Faults are distinguished by mode-conditional behaviour.
* Transients after mode changes create spurious violations.
* Multiple rules must be combined into signatures.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ahu_<case>_fault_free.csv` | CSV | ~500k minutes | LBNL FDD datasets (Granderson et al.) | CC BY 4.0 (dataset terms; verify) | Baseline data |
| 2 | `ahu_<case>_post_maintenance.csv` | CSV | ~200k | Same | Same | Evaluation window |
| 3 | `ahu_point_list.csv` | CSV | ~40 | Same | Same | Sensor/command definitions |
| 4 | `apar_rules.json` | JSON | ~25 rules | Task author (from House et al. APAR) | Cite | Rules |
| 5 | `fault_signature_table.json` | JSON | 4 | Task author (from APAR literature) | Cite | Signatures |
| 6 | `controls_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `contractor_hypothesis.xlsx` | XLSX | — | Task author | — | Damper hypothesis |
| 8 | `fault_labels.json` | JSON | — | LBNL dataset labels | Same | Validation only |

## 5. Deterministic solution path

1. Load data; classify modes; remove transients.
2. Evaluate rules; violation rates per mode.
3. Signature matching; diagnosis; validation.

## 6. Wrong paths (method errors, not misreadings)

**A — energy comparison only.** No diagnosis.

**B — rules evaluated across all modes.** Spurious violations.

**C — including transients.** Noise.

**D — single-rule diagnosis.** Ambiguous between faults.

## 7. Why the stump is analytical, not semantic

The rules, modes and matching are specified. The trap is diagnosing from aggregate symptoms instead of conditional rule patterns.

## 8. Draft task prompt (prose)

> What fault is behind the AHU's energy increase? Apply the mode-based rules and signature matching in the controls memo. Provide `rule_violations.csv`
> (mode × rule: violation rate), `fault_signature_match.png`, and a one-page `ahu_diagnosis.pdf`.

## 9. Deliverables

* `rule_violations.csv`, `fault_signature_match.png`, `ahu_diagnosis.pdf`.

## 10. Where 25+ rubric criteria come from

* Violation rates for ~20 rule × mode cells; match scores for 4 faults; diagnosis; validation; contractor contrast.

## 11. Golden-output checklist

* Mode classification; transient filter; tolerances; signatures; scoring.

## 12. Build notes (scope tuning)

* Use a labelled case whose true fault is not the damper; confirm the matching identifies it.
