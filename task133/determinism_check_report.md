# task133 determinism check (architecture 4)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | e53d1a72 | DETERMINISTIC (order kept; F good; G PASS; H PASS) | FIX_NOW | the cartage clause names FY2026's loads (prompt and planning note); the total graded to the nearest 500 and each grade to the nearest 100, the harvest plan's export tonnes by grade tuned at their planning step so every licensed payload and density convention sits mid-bin, asserted; the fleet register's tares and volumes given their configuration spread; the planning note rewritten in a logistics planner's voice, still listing each unit's tare, permit and full-bunk volume and naming no rule that combines them |
| 2 | 4a9ed312 | DETERMINISTIC (order kept; F good; G PASS; H PASS) | APPROVE | none |

---

# Determinism check, architecture 4 round 1 (2026-11-01): DETERMINISTIC, FIX_NOW; order kept; Gate G PASS (binding_constraint); Gate H PASS

Isolated thread, Sonnet at medium effort, on target.zip e53d1a72. FIX_NOW findings: the cartage window (load date against invoice date) unfiled; the total's rounding margin (two licensed payload variants round to 29,200); grade A under the per-load 1/payload variant.

# Verdict, task133 round 1

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every golden figure reproduced).
- **Disposition:** FIX_NOW. Close two filing gaps with no change to the evidence: (1) pin the cartage window, and (2) pin the treatment of 44 t units and the averaging convention so the total cannot land on 29,200. Prompt/planning-basis wording only; no model rerun on the analytic surface.
- **Order:** kept. derivation.md was written to disk before graded_blocks.md was opened.

## Why
The main call (29,100) follows from planning basis 3.1 and 3.2, RDC-2026-114 and the register's full-bunk volumes: payload = min(gross limit less tare, full-bunk JAS m3 for the grade length x t/JAS m3), averaged by grade, divided into the plan tonnes. My own derivation gave A 4,900.6, P 2,497.3, K 7,555.8, KI 8,047.2, KIS 6,098.8 loads (29,099.7), matching the golden to the rounding. Cartage by hauling unit, mill tonnes by weigh-in date and the load counts all reproduce. Residual risk is concentrated in Gate C/E on the total and on the cartage window (below), not in correctness.

## Evidence (recomputed, all reproduced)
- 29,981 tickets joined 1:1 to scaling (rego plus k-th trip, 4 to 26 min lag), 764,046.34 t, 71 pct on 50MAX units (21,270 of 29,981). Previous registrations (VLX649, JHD554) resolved through the register.
- FY2026 gross never exceeds 44.0 t; for Y units only A is mass-bound at 50 t (50 less tare is below the 12.1 m bunk); K, P, KI, KIS are volume-bound, so the 50MAX uplift is nil beyond bunk fill.
- Grades (nearest 50): A 4,900, P 2,500, K 7,550, KI 8,050, KIS 6,100, sum 29,100. Forest x grade payloads give 29,099.7; load-level or simple-mean density gives 29,100/29,088; mass-only gives 26,907 (golden's "not 26,900").
- Cartage by hauling unit, net of the 7 credit notes (each cancels a double-billed ticket), NZD thousand: Ruahine 2,073; Kereru 1,811; Tutaekuri 1,632; Wilson & Heke 1,158; Kinross 1,008; Patoka 1,012. Billing-code basis (KRH/RLC/TTT only) is the wrong route and differs.
- Mill tonnes by weigh-in quarter, MFP-docket loads only: AHT 10,870/8,680/8,700/9,780; HBL 5,340/4,610/5,610/5,440; MSM 14,090/12,000/12,600/13,130. All match.

## Open forks (named, with answers)
1. **Total rounding (Gate C, margin_or_boundary_fragility, minor).** Base 29,099.7 is 50 loads from the 29,150 line, fine; but two licensed variants cross it: (a) 8-axle units keep their actual FY2026 net rather than being re-modelled to min(44 less tare, bunk) gives 29,153 -> 29,200; (b) averaging 1/payload per load (harmonic) gives 29,161 -> 29,200 and A 4,950. Load-density plus keep-actual-net gives 29,144.8 -> 29,100. The planning basis ("average payload ... would carry on the same units") favours the golden (a unit that stays at 44 t is modelled the same way) and (b) contradicts the stated "divided by the average payload", so the golden is the better literal reading, but it is not closed by a sentence. Per-grade figures are unaffected (all variants round to the same nearest 50). Gate C/E on the total only.
2. **Cartage window (Gate E, underspecified_objective, the larger risk).** "FY2026 cartage paid against each carrier" is not tied to ticket date or invoice date in the prompt or planning basis. Loads of FY2026 (golden, invoices to 8 Jul 2026): Kereru 1,811; Kinross 1,008; Patoka 1,012; Ruahine 2,073; Tutaekuri 1,632; W&H 1,158. Invoice date <= 30 Jun 2026: 1,652; 912; 928; 1,887; 1,487; 1,060. The file name (cartage_invoices_FY2026) and doc 4.1 ("reported against the carrier whose unit hauled the load") support the golden, but the word "paid" invites the second. Fails Gate E for supplementary answer 4 unless pinned (for example "for the loads weighed in FY2026").
3. **Density not filed (Gate B, minor).** t per JAS m3 is not stated anywhere; it is derived from tickets x scaling. It is in the files (derivable), and grade-mean vs load-level vs volume-weighted all round the same per grade, so not decisive.
4. **Quarter and delivery date (Gate E, minor).** "Quarter of FY2026" is read as Jul-Sep etc.; "delivery date" is weigh-in at the mill (docket date is posted 1 to 11 days later; the 73 docket-dated 1 Jul 2025 lines belong to FY2025 and the 50 weigh-ins of 23 to 30 Jun 2026 are undocketed). Closed by evidence and doc 4.2, and the alternative (docket date) is distinguishable as wrong, so low risk.

## Files / Hygiene
PASS on count (13 files) and formats (csv, xlsx, docx, pdf; csv-heavy but 4 formats). Distractors present and unused: export_log_prices_FY2026.csv, port_kowhai_vessel_calls_FY2026.csv, forest_road_closures_FY2026.csv. Layout mess is realistic (dd/mm/yyyy against ISO timestamps, two ticket and scaling systems, previous registrations, multi-supplier mill logs, double-billed tickets with credit notes, docket lag). No authoring leakage seen; provenance and licence records are not in the judge's universe. Temporal: planning basis v2 (6 Oct 2026) follows RDC approval (29 Sep) and Board plan (18 Sep). No exclusion-level finding.

## Stump power (Gate F)
Good. A strong analyst takes the easy route of 50 t less tare for every permit unit (26,900) or adds 6 t to the average payload (about 25,700), or counts only the 44 t-bound loads (27,300); the data's bunk volumes (K, P, KI, KIS full a few tonnes above today's payload) are what cap the uplift. No document narrates this: the register carries the bunk volumes and the grade spec PDF the lengths, but the connection is the analyst's to make. Not too easy.

## Stumping type (Gate G)
`mechanism: binding_constraint`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The numbers are honest; the binding volume constraint on a modelled counterfactual payload carries the difficulty, and on clean data it would still stump. (Also etl_conformance for the asks.)

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: payload and truck-load capacity planning from weighbridge and scaling data is what forest logistics estimates (swap "megawatt-hours" in and it no longer reads). Layer 1: two weighbridge systems with different key formats, previous registrations, subcontract billing codes, double-billed tickets with credit notes, docket lag at the mill. Layer 2: a counterfactual payload under a mass and a volume constraint, per unit and grade. Easy route a strong analyst who read everything would take: apply 50 t less tare to every permit unit, giving 26,900 (or 6 t uplift, 25,700), instead of testing the bunk-volume cap.

## Fix (FIX_NOW, prompt or planning basis only)
- prompt: state the cartage window ("for the loads weighed in FY2026", or the invoice-date alternative) so supplementary answer 4 is single-valued.
- planning basis 3.1: add a sentence that every unit's FY2028 payload is the lesser of its gross limit less tare and its full-bunk volume times the grade's density, including units that stay at 44 t, and that the average is the arithmetic mean of load payloads; this closes the 29,100 versus 29,200 total fork. Adding that sentence files the HOW; if the project rule is WHAT only, instead keep as is and accept the narrow total risk (per-grade answers are safe).


---

# Determinism check, architecture 4 round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate F good; Gate G PASS (binding_constraint); Gate H PASS

The re-judge after round 1's FIX_NOW, on target.zip 4a9ed312. Isolated thread, Sonnet at medium effort.

# Verdict, task133 r2

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; no rerun.
- **Order:** kept. derivation.md was written to disk before graded_blocks.md was opened.

**Why:** The docx fixes the estimand (export tonnes per grade divided by the average FY2028 payload the grade's FY2026 port loads would carry on the same units, 50 t gross for permit units and 44 t otherwise, register fleet only). The only open input is t per JAS m3, and every reasonable estimate gives the same rounded figures. Every committed answer (total, five grades, six carriers, twelve mill-quarters) reproduced exactly from the files.

**Evidence (all reproduced)**
| Item | My value | Golden | Source |
|---|---|---|---|
| Loads / tonnes | 30,036 / 764,072 t | same | tickets, scaling |
| Permit share | 76.8% | 77% | tickets joined to fleet register |
| Plan export tonnes | 813,000 (A 148,100, P 69,700, K 218,400, KI 210,100, KIS 166,700) | same | harvest_plan Export |
| FY2028 loads | A 4,889, P 2,499, K 7,486, KI 7,983, KIS 6,088, total 28,945 | 4,900 / 2,500 / 7,500 / 8,000 / 6,100 / 29,000 | min(limit minus tare, bunk volume x density) |
| Cartage, NZD thousand | Ruahine 2,113.0; Kereru 1,834.9; Tutaekuri 1,678.2; Wilson & Heke 1,175.0; Kinross 1,010.7; Patoka 1,013.3 | 2,113 / 1,835 / 1,678 / 1,175 / 1,011 / 1,013 | invoices, net of 7 credit notes, carrier by unit |
| Mill tonnes | AHT 10,308 / 9,139 / 9,497 / 8,821; HBL 5,511 / 5,010 / 5,462 / 5,360; MSM 14,811 / 11,827 / 12,509 / 12,449 | matches after rounding to 10 t | MFP rows of the mill weighbridge log by weigh-in date |

Forks I tested; every one closes to the same rounded answer or is closed by filed text.
- **Density** (per load, grade mean, pooled, per unit and grade, per forest): total 28,923 to 28,945. Grades round identically. Nearest rounding boundary: K sits 25 loads above 7,450, and the total sits 170 above 28,750.
- **Unit-weighted against load-weighted average:** the same rounded figures.
- **Sum of rounded grades against rounded total:** both 29,000.
- **Mass-only scaling with no bunk-volume ceiling:** 26,787, about 27,000. This is the intended wrong route. Raising only loads at the 44 t limit gives about 27,100 to 27,200, and adding 6 t to the average payload gives about 25,900. These match the recommendation's "27,000" and "26,000" remarks.
- **Carrier:** the docx files "the carrier whose unit hauled the load". The invoice carrier_code is a billing group (KRH = Kereru + Kinross, RLC = Ruahine + Wilson & Heke, TTT = Tutaekuri + Patoka). Old registrations WYL161 and WHV180 resolve through the "Previous registration" column.
- **Invoice dates:** invoices run to 17 Aug 2026. "Paid for FY2026's loads" ties them to the load, not the invoice date.
- **Credits:** dropping credit notes changes Kereru, Patoka and Ruahine. "Net of any credit note" closes this.
- **Mill dates:** docket_date lags the weigh-in by 1 to 11 days. It carries 2 duplicated lines, 55 early-July dockets for FY2025 deliveries, and no dockets for 68 late-June deliveries. The docx says "by delivery date", and the weigh-in is the delivery event. Using docket_date moves AHT Q1 from 10,310 to about 10,090. The docket_date column is a document date, so I read it as not the delivery date. This is the one reading a hurried solver could take the other way, and it sits in an ask, not the main call.
- **Matiri filter:** the weighbridge log has 4 other supplier prefixes (TWN, PAN, HFL, OTH). Only MFP numbers match mill_dockets, so Matiri's own deliveries are identifiable from the files.

**Files/Hygiene:** PASS.
- 13 files in 5 formats: csv (8), xlsx (2), docx, pdf (2), plus the svg deliverable named in the prompt but not shipped.
- Rows: 30k tickets, 30k scaling lines, 30k invoice lines.
- Distractors: export prices, vessel calls, road closures, and the grade-spec PDF (lengths are needed to map grades to bunk volume, so it is not a distractor).
- Real-looking artifacts: mixed date formats, duplicate dockets, credit notes, personalised plates, and docx authors named.
- No provenance, authoring or benchmark language found. Dates are coherent, with docx v2 of 6 Oct 2026 after the 29 Sep 2026 approval. No public-data contamination.
- Minor: mill_code to mill name (AHT, MSM, HBL) is by initials only, which is fine. The council letter says the 50MAX route covers "nine-axle combinations holding a current permit", and the register agrees (all 9-axle Y, all 8-axle N).

**Stump power (Gate F):** Good. The trap is the bunk-volume ceiling on the short grades. A strong solver who scales payload by the gross-limit ratio gets 26,800 to 27,200 (27,000), and one who leaves FY2026 payloads unchanged gets 32,000. The doc never says that volume caps payload and never says what density to use. The solver must derive density from the ticket/scaling pairing, notice that KI, KIS, K and P loads on 9-axle units sit well below full bunks at 44 t, and apply min(weight room, volume x density). Strong models plausibly file 27,000. The ticket-scaling pairing by registration and sequence, old registrations and billing-code carriers add real Layer 1 work. The asks carry independent traps in invoice code against hauling carrier, credit netting, docket date against weigh-in, and the MFP filter.

**Stumping type (Gate G):** mechanism: binding_constraint (physical payload capacity); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. No reported figure is wrong, and on perfectly clean data the volume ceiling still defeats the mass-only route. Passes.

**Three rules (Gate H):** domain: pass; layers: pass; decisive_step: analytical.
- Domain: payload and capacity modelling for a log cartage tender is what forest logistics estimates. The swap test fails when other nouns are put in, because bunk volume, log density and gross vehicle limits are specific to the domain.
- Layer 1: change of registration, billing codes that are not carriers, a dockets file that lags and truncates, credit notes, and a ticket file that has to be paired to a scaling file.
- Layer 2: payload is the lesser of weight room and volume capacity, estimated per grade on the same units.
- Easy route: raise every permit unit to 50 t gross less tare, which gives about 27,000. The correct figure is 29,000.
- Weakness on H3: the formula min(weight, volume x density) is not stated in any file. It is a physical inference from the register's full-bunk columns, not a hidden rule or semantics, so I class it as analytical. The doc does name "full-bunk volume" as a unit attribute, so it is discoverable.

**Findings (gate failed)**
1. None fail Gates A to E.
2. Minor, optional, not a failure (Gate C/E, ask 5): "delivery date" for mill tonnes could be misread as docket_date. The docx's "by delivery date" closes it, so no change is needed.
3. Minor (hygiene, none): the SVG is a deliverable only and is not shipped. This is correct.

**Fix:** none. Fix location: none.

