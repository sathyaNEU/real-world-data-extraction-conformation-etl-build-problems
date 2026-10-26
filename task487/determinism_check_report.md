# Verdict: task487 (Vennholt Energy, Directive 17 levy), round 4

**Order kept:** yes. work/derivation.md was written, with all figures computed from target/, before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG). Residual fragility is noted under Why and Evidence.
- **Disposition:** APPROVE. No rerun is needed. Optional FIX_NOW, only if the author wants a thinner fork on Schedule B: pin in the notes what counts as a "survey" of a battery. Do this without handing over the re-check rule, because it changes what solvers see.
- **Why:**
  - The levy is forced to CAD 171,000 (band C, CAD 950 x 180 batteries). The shipped records show hatch finds are strongly sub-linear in the length of the window since the previous visit. Fitting a "left open by the departing visit" share plus a per-hour rate gives 53.7 to 54.3 t across four fit forms, all in band C. The golden's 54.5 t is in the same place.
  - The tempting reading starts every undated event at the midpoint of its window. That gives 44.6 to 45.3 t, band B, CAD 115,200, and it ignores what the full set of windows says about where starts sit. Directive s3.2 says "expected value given those records".
  - Every Schedule B figure (24 of 24 at 0.1 t) reproduced independently.
  - Not NOT_DETERMINISTIC, but Gate C is thinner on Schedule B than on the levy (see Evidence).
- **Evidence:**
  - **Counts:** 180 batteries (register, BT-0907 renamed BT-0907A and counted once). 1,660 events: 1,425 hatch, 58 pilot, 177 relief valve. 54 relief valves are timed by a collapse alarm: ALARM followed by a NORMAL near 0 kPa; routine lifts return to about 14 kPa. SCADA time is UTC and converted to local with UTC-7 until 8 Mar 2026 and UTC-6 after, with no fall-back. All reproduced.
  - **Real visits:** the 1,022 check-in geofence records with tanks_gauged = 0 are drive-bys, not visits. This changes the total by only 0.3 t.
  - **Window-length evidence:** hatch finds per window run 0.0107 (5 h), 0.0238 (24 h), 0.049 (67 h) and 0.062 (118 h). There is no day-of-week or hauler effect. The mixture fit gives share q = 0.0086 and rate 0.0006 per hour. Pilot and relief-valve finds have q about 0, so their starts are midpoints.
  - **Release-event methane (t):**

    | Reading | Total | Band, levy (CAD) |
    |---|---|---|
    | Mixture, per kind, linear | 54.27 | C, 171,000 |
    | Mixture, per kind, exponential | 54.05 | C |
    | Mixture, pooled, linear | 54.05 | C |
    | Mixture, pooled, exponential | 53.75 | C |
    | Mixture, hatch only, linear | 53.93 | C |
    | Mixture, hatch only, exponential | 53.71 | C |
    | Midpoint, all variants | 44.6 to 45.3 | B, 115,200 |
    | Start = Found | 0.64 | A, 59,400 |
    | Start = previous departure | about 89 | E, 360,000 |

  - **Margins:** the mixture readings sit 5.7 t under 60 and 5.7 t over 48. The golden's 54.5 t is not pinned to one decimal by the method (53.7 to 54.3 here), but band and levy are. The prompt asks one-decimal tonnes only for Schedule B.
  - **Genuine competing answer:** the midpoint reading, band B, CAD 115,200. The files separate it by likelihood, not by a stated rule, and no shipped sentence prescribes the mixture. This is the one real Gate C exposure on the main call. I judge it forced because "given those records" cannot be met by ignoring the other 52,000 windows, and because the golden's reading is the better-supported one.
  - **Schedule B, 24 of 24 matched at 0.1 t.** Method: full surveys only, dedup by component, final repair date (field-ticket date for FT orders, Completed for EHS orders, honouring the 36 "did not hold" re-repairs), route by half, BT-0907/0907A conformed. R10 July to December is 7.8497, 0.0003 t under the rounding edge to 7.9, so it is fragile to any 1-hour or 300 g convention difference. All other figures are at least 0.01 t from an edge.
  - **Competing Schedule B readings** (each changes many of the 24 figures; total in t, best-supported 165.8):

    | Reading | Total | Example |
    |---|---|---|
    | Every session counts as a survey | 137.5 | R04 10.4/9.5 |
    | Tracker Closed as repair day | 175.4 | R04 11.7/12.2 |
    | Ignore "did not hold" | 163.7 | R07 H2 3.7 vs 4.3 |
    | Register (2027) route for both halves | not totalled | R07 7.8/2.8 vs 12.7/4.3 |
    | No dedup | not totalled | R01 10.7/10.7 |

  - **Why the best-supported reading is the forced one:**
    - 318 of 858 sessions screen 2 to 20 points and never tag a leak, against 100 to 410 points for full surveys. A 3-point re-check is not an "OGI survey of the battery".
    - The tracker note says Closed is the day closed against the work order, not the repair day.
    - The work-order text says "did not hold".
    - Routes differ by half for 26 batteries (route app to 30 Jun, check-in app from 1 Jul). The register carries the post-4-Jan-2027 route, so it is the wrong source.
    - The cut-offs are inferred from data patterns, not stated in Directive 17. A strict reader could call "survey" and "repaired" under-specified. I weigh these as data-supported and not reasonably contested.
- **Files/Hygiene:** PASS.
  - **Inventory:** 15 files, 6 formats (csv x8, xlsx x3, jsonl, txt, pdf). Largest is 68,760 rows (battery_daily_production). Hauler tickets (26,495), sales gas statements, the hauler/sales/meter material and the work orders other than leak repairs are relevant distractors; none decides the call.
  - **Provenance:** no authoring or benchmark language. The in-fiction data-notes file is plausible. No temporal break: exports are 8 to 13 Jan 2027, the pack is as-of Jan 2027, and the Directive is dated 2025.
  - **Layer 1 mess:** UTC vs local, two app time formats, a renamed battery, drive-by records, a 2027 route reshuffle, buffered alarms with RTU time.
  - **Not done:** the cross-batch fingerprint check (other task folders are off-limits to me); no exclusion-level finding.
- **Stump power:** HIGH.
  - The natural route is the midpoint start, which files band B and CAD 115,200 (wrong). A start at Found files band A. Both are plausible for a strong model; only the window-length structure (an interval-censored start with a left-open share) separates the right band.
  - The Schedule B asks stack independent traps. Each is cleanly separable: survey definition, repair date, re-repairs, route by half, battery rename.
- **Stumping type:** `mechanism: method_or_model_selection` (a mixture start model validated against all of the year's windows; Schedule B adds statistical and rule layers), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
  - On clean data the call still turns on the expected-start model. The data is honest and no reported number is overturned.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`
  - The field's own analysis is estimating the start of an interval-censored release event from visit windows and a telemetered alarm, then converting it to methane volumes and a band.
  - The easy route is a midpoint start (band B, CAD 115,200) or a start at Found (band A, CAD 59,400); a strong analyst who cleaned and read everything correctly still files one of them.
  - Swap test: replacing "tank hatch" with another field's noun breaks the flash GOR/C1 methane chain, so the domain is not a backdrop.
- **Fix:** none required (fix location: none).
  - Optional (solution/notes only): note in submission that the main call rests on the sub-linear window evidence, and consider stating explicitly in the data notes what a "survey" session is, to thin the Schedule B fork. Avoid wording that hands over the 100-point cut.
