# Determinism check, task447, the repair after the house review

Three isolated passes, each one thread at medium effort reading only a fresh unzip of `target.zip`, the prompt,
the submission's graded blocks and the judge's system prompt. Pass 1 (2026-10-13, `determinism_check_report.md`)
returned DETERMINISTIC and APPROVE on the build as first shipped, and recorded two pins it declined: the provider
file as the specialty source, and the tier stratification filed, "not taken: it removes the stump".

**The house review of 2026-10-16 was right on the determinism axis, and the fault was ours, not the review's.**
Rule 4.05 shipped as a complete recipe, "the rise, after the acquisition, in the share of those services at the
acquiring system, as a share of the services that were elsewhere before it", whose literal execution over the
estimation set 4.05 itself defines gives $1.516M and close against the golden's $2.209M and proceed.
`determinism-check` section 1 bans exactly that: "Never file a procedure, basis or formula whose literal
application gives another answer." Section 2's pass test needs every literal reading to give the golden, or each
differing reading to violate a quotable shipped sentence, or the readings to converge, and none of the three held:
the design note's own fork table closed the pooled reading with "the records", which is an inference. Both in-task
determinism judges had passed every gate with F strong, and the measured response was a valid stump at an 11 per
cent rubric, so the difficulty was never in question; the record was.

**What was filed, and what was deliberately not.** The repair files the estimand's unit of analysis, which section 1
requires filed literally, and not the method, which rule 3 of the client's standard bans as a decisive step:

- 4.04(b): the service moves "in the share expected for that service under the member's product as the product
  stands in the projection year".
- 4.05: "A share is estimated for a service and a product, and is the share expected under that product as it
  stands in the projection year; the office does not estimate one share across products."
- A2: a unit billed to two carriers is one service, and two units of a code provided on one date, which the claims
  show by their quantities or their referring providers, are two services.
- A3: a visit reported to more than one carrier is one visit, and a physician's specialty is the classification of
  the physician's own NUCC taxonomy as the carriers' provider files record it rather than as a claim reports it.
- A5: a physician joins on the date he or she first bills under the system's numbers, and that date, not the first
  day of its calendar year, is the date a service falls before or after.
- The tier filings' purpose line no longer says it is kept for another report. It was not rewritten to read as an
  input to the 4.05 estimate: a file that announces its own part in the deciding step is a leak under sweep 5.

The review's own wording for 4.05 ("estimated separately by the acquiring system's network tier placement") was not
taken, because it files the method. Its third suggestion, a filed back-test with a stated tolerance, was not taken
either: task457 in the same lane already ships one, and a recognisable organ may not appear in consecutive builds.

**Scope, proved.** `freeze.py check task447 --mode determinism` passes, and the main-call reference's `figures`
block is byte-identical across the whole repair: the call (proceed), the increase ($2.2M), the professional part
($610,000), the referred part ($1,600,000) and all ten exhibit figures are the figures that shipped. Only three
documents changed, plus the two generator assertions that read them.

**The isolated reader of the repaired pack** (medium, pack and prompt only) answered that nothing tells it the
decisive step ("No sentence names a method"), that no file ranks the candidates, that the main answer is decided by
"(a), an analytical choice", and that "No sentence anywhere in the pack says tier placement matters to the share".
It reached proceed at $2.21M by finding the gate in the data, which is the task working as designed.

**Pass 2 (this repair, first thread): DETERMINISTIC, FIX_NOW** on three input wordings, all three applied above (A2's
two-unit case, A3's dual-carrier visit, A5's join date; the last closed a reading that landed at $1.98M, just under
the threshold).

**Pass 3, after those fixes, follows verbatim.**

# Determinism verdict, task447 (re-judge after FIX_NOW repair)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; every graded figure reproduced from the bundle, no model rerun required.

- **Why:** Read literally, the filed text fixes the estimand: OHCCR 4.05 defines the share that moves as the rise in the acquiring-system share, as a share of the services that were elsewhere before, estimated for a service and product as the product stands in the projection year. Appendix A5 now pins the join date to the physician's own first billing date, and A2, A3 and A4 pin the unit, visit, specialty and system definitions. On that reading the main call (proceed, $2.2 million against the $2.0 million threshold in 4.06) and all four asks recompute exactly. Gates A to E pass.

## Evidence (recomputed from the shipped files)

| Item | Recomputed | Source |
|---|---|---|
| Brightwater professional lines, TIN 39-9943822, 2024, paid by 30 Jun 2025 | 23,970 lines, allowed $3,302,047 | apcd_professional_claims_2024.csv |
| Same lines repriced at Exhibit C Professional by carrier | $3,911,680, so +$609,633 (golden $610,000) | N25-014_exhibit_C xlsx |
| Brightwater referred lines (18 NPIs billing under the TIN), net of voids and replacements | 8,972 lines; 8,029 offered by Ledgestone and not at a Ledgestone site | apcd_op_facility_claims_2024.csv |
| Joiners | 27 physicians: Oak Hollow, Northpoint (4 orthopedists, join dates 2022-10-03 to 2022-11-14, all within 90 days), Baird Creek, Harborview, Cedar Ridge for Ledgestone; Lakeside and Fond du Lac Digestive for Wolf River. Matches the 27 referring NPIs in the 2021-2023 extract | register, NPI history |
| Share that moves, by the member's benefit-period plan year and the tier filing | untiered 86.1%, acquirer first tier 86.1%, acquirer second tier -0.1% (0%). Every physician shows about 8% at the acquirer before and 87% after. Norbridge Tiered EPO at Wolf River: second tier 2022-2023 about 8%, first tier from 2024 87% | claims 2021-2024, eligibility, tier JSON |
| Referred increase at 86% / 86% / 0% | $1,599,573 (golden $1,600,000) | Exhibit C; Bayfield at 1.15/1.55/1.6/2.3/4.05 times CY2025 Medicare (baseline Bayfield claims at hospitals pay 1.3 to 3.3 times Medicare, so the multiplier reading is data-supported) |
| Projected increase | $2,209,205, so $2.2M, at or above $2.0M, so proceed | |
| Ask 3 (Manitowoc / Kewaunee: imaging, endoscopy, arthroscopy) | 3,269 / 40.6; 1,574 / 52.9; 328 / 42.7; 1,008 / 45.4; 444 / 64.0; 97 / 41.2 | exact match |
| Ask 4 (Brightwater / Ledgestone) | PC 35.0 / 7.6; GI 41.8 / 4.0 (4.02); Ortho 35.7 / 3.7; Cardiology 71.9 / 7.6 | exact match |

### The four points the previous pass raised

1. **OHCCR 4.04/4.05 and the share.** The filed text now says what the share is a share of (services of the joined physicians that the acquirer offers, rise after as a share of those elsewhere before) and the placement it is conditioned on (the product as it stands in the projection year). Variants tested:
   - Share by service code and tier state: $2.216M.
   - Share by code, product and tier state: $2.210M.
   - Share as a plain rise in share points (79% instead of 86%): $2.079M. Still proceed.
   - Dropping the join year: 86% / 86% / 0%. Unchanged.
   - Only Ledgestone-acquired joiners: unchanged.
   - Dual-billed duplicates collapsed in the referred set: unchanged.

   No estimate that respects "as it stands in the projection year" lands below $2.0M. The only estimates that do ignore that clause and carry history forward:
   - Bayfield's own tier-2 history (share 0): $1.633M.
   - Per-product share pooled over years: $1.643M.
   - Per-carrier share pooled over years: $1.512M.
   - One share across products and tiers (44%): $1.473M.

   Rule 4.05 already says the office does not estimate one share across products. **Residual note, not a fail:** Bayfield's first-tier state has no observation under Bayfield. It must take its share from the same placement state under the other products (Wolf River first tier at Cedarbrook, Lakefront and Norbridge). A reader who treats "estimated for a product" as "from that product's own history" gets 0 for Bayfield and a "close". That reading contradicts "as it stands in the projection year", so I do not treat it as defensible. Bayfield's first-tier part is $576k of the $1.6M, so this is the load-bearing step.
2. **A2 counting.**
   - Same member, date, code, modifier and facility from two carriers with the same referrer: 657 pairs, counted once.
   - Two carriers each with quantity 2: 2 pairs, counted as 2 units.
   - Same carrier, two referrers: 16 pairs, counted as two services.
   - The only same-carrier, same-referrer pair (CPT 85025) is laboratory, outside the ask lines.
   - No residual fork. Naive counts differ: Manitowoc imaging 3,336 against 3,269.
3. **A3 counting and specialty.**
   - 1,210 two-carrier pairs for the same rendering physician are counted once; 5 same-carrier repeats give identical one-decimal shares either way.
   - Specialty comes from carrier_provider_file.csv: 216 NPIs, one taxonomy each across carriers, and every rendering NPI is present.
   - The claim taxonomy would misstate shares: Cardiology Brightwater 90.4 against 71.9, because Kinnickinnic reports 207Q for everyone.
   - Telehealth (POS 10 or modifier 95, 701 lines on POS 11) is excluded explicitly. No residual fork.
4. **A5 join date.** The rule now says the physician's own first billing date, not the first day of the calendar year. The literal reader is closed. For completeness, a January-1 date gives shares of 73% / 80% / 0%, a total of $2.014M. The call would still be proceed, but the figure would show 2.0, not 2.2. The control-case join date is read from the register (Baird 2022-04-01, Cedar Ridge 2023-08-01, Fond du Lac Digestive 2023-02-01); because every physician moves about 8 to 87% regardless of date, this reading does not change the result.

### Other forks examined

- **Clayton Brown** (GI, NPI 1451989697) bills under both Brightwater and Kinnickinnic through 2024. Rule 4.02(e) makes him a physician of Brightwater, and A2 and the 18-physician notice agree. Excluding him gives $1.851M (flip), but that reading contradicts the text.
- **Harbor Lakes** (clinically integrated network, not control) and the single LMG to Harbor Lakes to LMG physician are not joiners under A4 and A5.
- **Bayfield "Percent of Medicare" values** (1.15 to 4.05) are multipliers. A literal percent reading is absurd (a $10 MRI) and is contradicted by Bayfield's baseline allowed amounts. This is a labelling wart. I rate it low risk.
- **Bayfield uses CY2025 Medicare amounts** for 2026 services because no 2026 file exists and 4.04 forbids trending.
- **No paid-date effect:** all Brightwater lines were paid by 13 Mar 2025 (professional) or by 30 Jun 2025 (referred).
- **Nuclear cardiology (78452)** is not offered by Ledgestone and is excluded. Wolf River offers it, but joiners of Wolf River barely refer it.

## Files/Hygiene

PASS. 19 files in four formats (csv, pdf, xlsx, json). The 2024 facility file has 67,976 rows and the professional file 69,086. There are two layouts (2.4 and 3.1), replacements and voids, dual-carrier duplicates, mixed-case provider names, nine-digit TINs without hyphens, and an unrelated Medicare Advantage extract and a HCRIS extract as distractors (unused). Provenance is recorded in export_manifest.csv. Nothing reads as authored for a benchmark. Temporal coherence is fine: the extract of 15 Sep 2025 predates the 8 Oct 2025 notice; the baseline year 2024 qualifies under 4.03. Minor: the manifest dates Exhibit C 7 Oct, a day after the 6 Oct signature, which is harmless. No exclusion-level finding. metadata.json was not read, per isolation.

## Stump power

Moderate. The main call is carried by the tier-conditioned share. A strong model that reads the tier file will stratify. One that pools by product, carrier or physician reaches $1.47M to $1.64M and files "close here". That is a genuine analytical error, not a semantic one. The asks (dual-carrier unit counting, ZIP by span date, specialty from the provider file instead of the claim, Ledgestone share through the register) add many gradable cells where a careful solver's easy path goes wrong.

## Stumping type

mechanism: method_or_model_selection (share estimated conditional on network placement, validated by the data's own before/after structure); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.
No reported number is misleading; the difficulty survives clean data, since the share genuinely depends on tier. Gate G passes.

## Three rules (Gate H)

domain: pass, layers: pass, decisive_step: analytical.
Swap test: the deciding quantity is an expected referral diversion share estimated from past acquisitions and priced at the acquirer's rates, which is the core of a merger cost review. Layer 1 is layouts 2.4 and 3.1, replacements and voids, dual-carrier duplicates, NPI reassignments, July-renewal plan years and name variants. Layer 2 is stratifying the diversion share by the acquirer's tier placement and carrying it to the 2026 placement. A strong analyst who cleaned the data and read every rule would still take the easy route of a per-product or pooled share, which gives $1.47M to $1.64M and a wrong "close".

## Fix

none.
