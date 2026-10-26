# determinism-check report, task271 architecture 4, 2026-10-26 (judge thread verdict, run a4r1)

# Judge verdict, task271, run a4r1

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The candidate model set and the 20 psi conversion each need a solver-visible pin (standard / guide text), so prior runs are invalidated and a rerun is required.

## Why
The main call turns on the pressure-zone term, and no shipped file names it as a candidate characteristic. Read literally, Frequency Model Standard s.3 lists the characteristics of a home as year built (four eras), construction, foundation, full bathrooms and stories, "each as recorded on the term", and s.4 says only "of the models considered". Searched over those five, the 2025 test picks foundation alone (3,252.4), which gives Brookmere 18, Dorrance Hill 26 and Sallowmead 22, so the call becomes Brookmere. The golden's Dorrance Hill 21 / Sallowmead 25 / Brookmere 28 appears only if a spatial join to tcwa_pressure_zones.geojson is added as a considered term. That is an expert-reasonable choice but one the text never licenses, so it is an unpinned model-set fork on the main call (Gates C/E, underspecified_objective). Two supplementary answers also stand on a fact absent from the package: asks 2 and 5 need the NFPA 291 residual-to-20-psi conversion with exponent 0.54, which no shipped file states (Gate B, external_dependency). Ask 3 has a "their" reading fork.

## Evidence (recomputed from target/)

| Item | Reproduced? | Source |
|---|---|---|
| House-years 54,233.4; non-weather water claims 1,258 (23.2 per 1,000) | Yes | policy_terms (std 2.4), claims_register (-R1 dropped, WTR-P/A, 3110/20/30) |
| Valley-zone homes 217 / 1,238 / 2,192 (DOR/SAL/BRK) of 2,769 / 3,096 / 2,584 | Yes, with my own point-in-polygon; every parcel falls in exactly one zone | parcels, pressure_zones |
| Deviance 2025, foundation+zone 3,169.4 vs foundation 3,252.4 | Yes, at home-year grain (parcel and year, terms merged). At term-row grain it is 3,555.1 vs 3,638.0, same winner | policy_terms, claims |
| Township frequencies 21.0 / 25.1 / 27.9; Valley factor 2.31 | Yes | dwellings card 1 mapped per guide, zone |
| Protected homes 2,182 / 2,686 / 1,994 | Yes, but only with exponent 0.54 | hydrants, flow_tests, parcels |
| Appeals-adjusted value over 0.451: 804.6 / 906.7 / 768.0 | Yes, but that is ALL R-SFD homestead homes, not the protected ones | parcels, appeals, steb ratios |
| Avg payments 10,769 / 11,056 / 11,670 | Yes (indemnity+void+recovery for register claims; CAS paid-to-date less recovered for the 283 water claims on the bordereau, which are disjoint from the payments file) | claim_payments, bordereau |
| Unprotected fire frequency 5.3 | Yes (29 claims over 5,465.7 house-years), but it depends on the 0.54 exponent | claims, hydrants |

Forks that survive:
1. **Model candidate set (main call).** Only the s.3 characteristics: foundation alone wins, Brookmere 18 (lowest), and the call is Brookmere. Adding zone: Dorrance Hill 21, the golden. Adding zone and stories: the same, 21.0 / 25.05 / 27.9. Zone alone: DOR 18.7, SAL 25.9, BRK 35.9, so the call is Dorrance Hill but the numbers differ. Roll attributes such as heating, grade, half baths and deductible never beat foundation+zone.
2. **NFPA exponent (asks 2 and 5).** The guide asks for 500 gpm "at a residual pressure of 20 psi", and the master plan says only "tests follow NFPA 291". The raw flow gives 2,121 / 2,580 / 1,842 protected. A linear scaling gives 2,222 / 2,723 / 2,031. An exponent of 0.5 gives 2,182 / 2,686 / 1,981 (Brookmere differs). 0.54 gives the golden. Ask 5 is 4.4 on raw flow and 5.3 on the golden. The exponent is outside the package.
3. **"their total market value" (ask 3).** The golden values all owner-occupied homes. The prompt reads "how many ... would class as protected and their total market value", so the protected-only value is licensed: DOR 638.2, SAL 785.1, BRK 595.8 (0.451). The brief's "those homes" supports the golden but the prompt does not close it.
4. **Deviance grain (minor).** Aggregated to rating cells, the deviance ranks the intercept-only model first. Home-year and term-row grain agree on foundation+zone. The text should say "per home per year".

Closed correctly: the common level ratio of 0.451 (in effect 2026-01-01; 0.428 is the trap), the hydrant renumbering cut at 2024-04-01 (FORMER_ID/HYDRANT_ID collisions mapped with zero unmapped tests), and the Upper zone's two polygons being one zone.

## Files/Hygiene: PASS (with minor notes)
20 files. Formats: csv, pdf, xlsx, geojson, txt. Largest file has 73k rows. Decoys NOAA weather and building permits are unused. Dates are coherent (extract 2026-08-31, brief 2026-10-05, pack 2026-10-21). No exclusion-level finding. pack_contents.txt ("Pack assembled ...") reads as an assembly inventory and is worth a glance. The cause-code, bordereau and hydrant-ID mess is plausible Layer 1.

## Stump power
If the model set is read as §3's five characteristics, the obvious route (foundation, or any all-roll model) files Brookmere. A solver who spots the Valley-zone pressure effect from the master plan and the zone layer gets Dorrance Hill. That should stump many strong models, but part of the failure is the unpinned candidate set (a Gate C fork) rather than pure analysis. The asks add independent stumps: the hydrant renumbering, the CAS bordereau merge, and the common level ratio date.

## Stumping type
mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. The model is chosen by out-of-sample deviance on honest data, which is eligible for Gate G.

## Three rules
domain: pass, layers: pass, decisive_step: analytical. Actuarial frequency modelling (choosing a Poisson rating model by holdout deviance and applying it to an unwritten territory) is the field's own work, and the swap test fails to relocate it. Layer 1 is the pack's own mess (hydrant renumbering, legacy vs 2024 cause codes, bordereau vs payments, preliminary/revised ratios). Layer 2 is the hidden location driver found by the holdout search. The easy route is the five listed characteristics, which files Brookmere at 18.

## Fix
Where: prompt and input_files (the standard's text), not the solution.
- Pin the candidate set in the Standard s.4 or the brief without naming the answer: "any categorical attribute of the home that can be determined for every home in the territory, including attributes from the county roll and the Authority's records". Then assert in checks that the rule excludes nothing the golden needs.
- State the residual-to-20-psi conversion in the guide or master plan section 6.3 (the formula and exponent), or restate protection as measured at the tested residual.
- Reword ask 3 to "the total market value of all of its owner-occupied single-family homes" or "of the protected homes", whichever is intended.
- Say "per home per year" for the deviance grain.
Rerun required, because the standard, the guide and the prompt change.
