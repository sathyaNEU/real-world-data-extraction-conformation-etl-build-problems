# task485 determinism check (architecture 5)

One isolated judge pass, a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 28ce0e20 (MD5 8e364099) | DETERMINISTIC (order kept; Gate F strong; G PASS, decomposition_attribution / analytical_non_defect; H PASS) | APPROVE | none; F1 (the pharmacies' channel before 1 May read from the claims' dispensing fee against the October network snapshot) taken as derivable, the judge's optional pin in the network file not taken because it would hand over the ask's device |

The architecture 4 record is in determinism_check_report_arch4.md.

---

# Determinism check, round 1 (2026-11-02): DETERMINISTIC, APPROVE; order kept; Gate F strong; Gate G PASS; Gate H PASS

Isolated thread, Sonnet at medium effort, on target.zip 28ce0e20.

# Verdict, task 485

- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.
- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair is required and no rerun. F1 below is the one residual risk, and closing it would change what solvers see.

## Why
The main call is forced by the filed text and the data. Policy 3.2 nets "the rebates the product's manufacturer paid the Plan on those claims". Only a per-product rebate rate reproduces the statements. Regressing manufacturer x account x quarter rebate (current plus FY2026 prior-period lines) on product ingredient cost fits all 192 cells to the cent (max error 0.056). Spreading a manufacturer's rebate over its products by ingredient cost does not reproduce them and credits a product with rebates paid on other products' claims. Net-cost margins within each class are 70 dollars or more, and no value is within 4 dollars of a rounding boundary. All 17 net costs, the six preferred products, and the 24 member counts reproduce the golden exactly. The guarantee table reproduces exactly too, once the hospital-pharmacy channel history is applied (F1).

## Evidence (recomputed from the bundle)
- **Basis:**
  - Net cost uses claims by date of service in FY2026 (Jul 2025 to Jun 2026) with reversed pairs removed.
  - 30-day supplies are quantity over the clinical review's listed quantity, per policy 4.1.
  - Ingredient cost is before fees.
  - FY2025 prior-period lines are excluded.
- **Net cost reproduced:**

| Class | Net cost per 30-day supply |
|---|---|
| GLP-1 | Velantro 510.90 (preferred), Liraquent 599.18, Dulavio 619.24 |
| SGLT2 | Empriva 259.26 (preferred), Daplexa 349.78, Canivo 370.40 |
| Insulin | Glarvia 99.65 (preferred), Deglutra 170.55, glargine-qmrt 210.70 |
| DOAC | Apiqor 369.66 (preferred), Ravelta 450.63 |
| ICS/LABA | Bevoria 200.93 (preferred), Vilaro 250.42, Saltiva 259.59 |
| Adalimumab | kvrn 1189.05 (preferred), Advelis 3060.71, Adalvane 3690.81 |

- **Guarantee check:**
  - Remitted for the quarter is the current line plus that quarter's prior-period lines: 3,648,594.97 / 3,589,431.43 / 3,453,708.88 / 3,469,407.06.
  - With the three hospital pharmacies treated as retail before 1 May 2026, counts and guarantees match the golden:

| Quarter | Retail <84 | Retail 84+ | Mail | Specialty | Guarantee | Shortfall |
|---|---|---|---|---|---|---|
| Jul-Sep 2025 | 9,484 | 654 | 839 | 572 | 3,476,679 | none |
| Oct-Dec 2025 | 9,570 | 659 | 792 | 535 | 3,419,630 | none |
| Jan-Mar 2026 | 9,653 | 685 | 818 | 466 | 3,373,898 | none |
| Apr-Jun 2026 | 9,573 | 652 | 798 | 610 | 3,519,558 | 50,151 |

- **Members:**
  - Counts match all 24 cells.
  - They need the legacy-cardholder bridge plus DOB and gender matching, because person codes were renumbered.
  - They also need 274 departed old cardholders (792 claim rows) counted as their own members under the claim account.
- **Forks tested:**

| Fork | Result |
|---|---|
| Pro rata allocation | Changes the winner in 3 of 6 classes (Liraquent, glargine-qmrt, Saltiva). Refuted by the exact fit. |
| days_supply/30 instead of quantity | Contradicts policy 4.1. |
| Fiscal-year scope by date paid | Immaterial, because net cost per supply is price times (1 minus rate). |
| Counting FY2025 prior-period lines | Immaterial for net cost. In the guarantee check it removes the Q3 shortfall. |

## Findings
- **F1, Gate C/B (moderate), supplementary 3: the channel history is not filed.**
  - Exhibit C C.5 sets the channel by network "on the date of service". The only network list (pharmacy_network_202610.txt) is an October 2026 snapshot showing three hospital outpatient pharmacies as specialty.
  - No file states when they changed. The golden's "retail until 1 May 2026" is inferred from the claims file.
  - Those three pharmacies bill the 1.25 retail dispensing fee on every paid claim through 27 Apr 2026. They have none from 1 May, and no claims fall between 28 Apr and 30 Apr.
  - A purely literal run of the snapshot gives:

| Quarter | Specialty claims | Guarantee | Shortfall |
|---|---|---|---|
| Jul-Sep 2025 | 726 | 3,649,131 | 536 |
| Oct-Dec 2025 | 699 | 3,602,694 | 13,263 |
| Jan-Mar 2026 | 629 | 3,556,192 | 102,483 |
| Apr-Jun 2026 | 665 | 3,579,744 | 110,337 |

  - The golden gives no shortfall in the first three quarters and 50,151 in the last.
  - The data separate the two readings cleanly, so I treat the golden as derivable. It is not literal-proof. A pin would belong in the network file (an effective-date history column). That change alters what solvers see and is optional.
- **F2, Gate C (low): the rebate allocation convention is never named.** It is closed by the policy wording "on those claims" and by the exact fit, and recorded for the fork table.
- **F3, Gate C (low): the member population.** The golden counts members on claims, including those not on the roster. A roster-only reading gives lower counts (GLP-1: 515 / 194 / 195 / 145). The prompt says "members with a paid claim", so I read it as claims-based.
- **F4, Gate C (low): the Q2 2026 prior-period adjustment is not yet received.** The golden uses what is remitted, which is the literal reading.
- **Gate A:** no solution-block defect. All figures agree across the blocks.

## Files/Hygiene
- **Result:** PASS.
- **Files:** 14, in four formats (6 pdf, 6 xlsx, 2 csv, 1 txt). Claims have 49,787 rows and the roster 79,886.
- **Layer 1 mess:** two claim layouts (dates, NDC format, account and cardholder codes), a person-code renumbering, and prior-period lines mixed into statements.
- **Distractors:**
  - the drug file's Specialty Indicator
  - the FY2025 guarantee reconciliation
  - the 2025Q2 and 2025Q3 remittances
  - the implementation messages
- **Other checks:**
  - Dates are coherent with the fiction. The FY2025 reconciliation ties out (3,241,314).
  - No provenance, README or authoring language was found, and no public-data contamination.

## Stump power (Gate F)
Strong. The natural default is to give each product its manufacturer's average rebate, and it is wrong in 3 of 6 classes (GLP-1, Insulin, ICS/LABA). Doing the work correctly needs a per-product rate recovery that a diligent analyst can validate to the cent. Ignoring rebates, or using the wrong 30-day supply, fails further. The supplementary guarantee check adds a second trap (F1) that costs credit on the asks, not on the call.

## Stumping type (Gate G)
`mechanism: decomposition_attribution` (a pooled payment attributed to products, validated by exact fit); `stumping_family: analytical_non_defect`; `surface_read_dependency: no`; `sole_data_defect: no`.

The remittance statements and claims are correct. The difficulty is attributing pooled rebates correctly, not rejecting a wrong reported number. On clean data the attribution would still stump, so it passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **Domain:** net cost per 30-day supply under a formulary rebate contract is the core of pharmacy-benefit PDL work. It fails the swap test for a backdrop.
- **Layer 1:** two layouts, ID bridging, prior-period lines.
- **Layer 2:** product-level rebate attribution.
- **Easy route:** a strong analyst who cleaned everything and read every rule would spread each manufacturer's rebate by ingredient cost. That prefers Liraquent, glargine-qmrt and Saltiva, which is wrong.
- **Asks (F1):** the hospital-channel history is data semantics inside a supplementary ask. Asks are exempt from the ban, and the main call is not affected.

## Fix
none (optional hardening of F1 sits in input_files and would require a rerun).

