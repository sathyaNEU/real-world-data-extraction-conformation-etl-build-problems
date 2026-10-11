# Layer 1 library: data messiness by domain

The client's messiness library. Layer 1 makes the inputs hard to use the way real data is hard to use; it costs the solver time and care and never decides the answer (that is Layer 2, `../../stumping/references/client/layer2-rigor-patterns.md`). How it is built into a pack: `../SKILL.md` §7. The card's `layer1` field lists the techniques a pack carries.

## The test

Would a real analyst meet this in the real source? If it exists only so that catching it flips the answer, it is a planted defect, not Layer 1: copied or backfilled blocks, swapped or reversed series, a hidden year-to-date column, deliberately wrong totals, fields mislabelled to mislead, decoy memos or drafts written to carry the wrong answer. **Keep it honest**: ship what a careful analyst needs to resolve each mess (the codebook, the crosswalk, the release note), so care is rewarded and the cleaned data supports exactly one recommendation once Layer 2 is done right. Each line below reads: the mess and the work it forces; *honest:* what ships so it resolves one way.

## Techniques that work in every field

1. **Native release formats.** Multi-sheet workbooks with title blocks, merged headers and footnote markers; PDFs with tables; fixed-width or layout files that change across years.
2. **Several sources for one picture.** A registry, a periodic release, a filing and a log, each with its own keys, grain and timing, never designed to join.
3. **Imperfect keys.** Codes in one file and names in another, identifiers that change between systems or years, several spellings of one entity, many-to-many links needing a stated rule.
4. **Vintages and revisions.** Overlapping preliminary and revised releases, classification or boundary changes between years, crosswalks that split or merge units.
5. **Units, time and scale.** Fiscal against calendar years, local time against UTC, nominal against real, counts and rates on different bases, thousands in one file and units in another.
6. **Genuine overlap.** Overlapping extracts, records resubmitted after correction, one event reported by two parties; deduplication needs a rule a careful analyst would apply.
7. **Real coverage and missingness.** Suppressed small cells, skip and reserve codes, partial years, entities entering or exiting, reporting thresholds: documented features of the source, not inserted holes.
8. **Documentation that has to be read.** Codebooks, dictionaries, release notes and methodology statements the solver must apply to interpret fields.

## Product Analytics  (`product-analytics`)

1. **Event names drift across releases.** Renamed events and retyped properties mapped onto one taxonomy; *honest:* a tracking-plan changelog, old and new names overlapping in time.
2. **Anonymous devices stitched to users.** Device ids before login, user ids after, merged through an alias table; *honest:* ship the identity map, state per user or per device.
3. **Client clocks, server clocks, offline batches.** Pick the clock, convert zones, sessionize; *honest:* both timestamp columns named, the window states clock and zone.
4. **Retried and double-fired events.** Dedupe on the insert id, not on content; *honest:* every event carries an id, duplicate share low and realistic.
5. **Assignment, exposure and outcome in separate tables.** Assigned-not-exposed users, rare cross-arm users; *honest:* the exposure rule in the experiment spec, cross-arm users identifiable.
6. **Nested JSON properties.** Flatten, explode arrays, cast types that shift by version; *honest:* valid JSON, keys in the tracking plan, type changes tied to versions.
7. **Internal, test and bot traffic.** Filtered by account list, test flags and user agents; *honest:* the list or flag ships, the exclusion rule in the metric definitions.
8. **Billing events against product accounts.** Trials, prorations and refunds under billing ids and currencies; *honest:* the account crosswalk and a short billing glossary.

## Quantitative Finance  (`quantitative-finance`)

1. **Unadjusted prices around splits and dividends.** Adjustment factors built from a corporate-actions file; *honest:* real ex-dates, never an unrecorded split.
2. **Ticker reuse and identifier changes.** Histories linked through a dated identifier map, not the ticker string; *honest:* real effective dates, ticker-only joins visibly mismatch.
3. **Delistings outside the price file.** Delisting returns and reason codes merged from an events table; *honest:* natural frequency, the table documented.
4. **Trade and quote clocks in mixed zones.** Normalise clocks and DST, match trades to prevailing quotes; *honest:* each source's documented precision and zone.
5. **Trading calendars differ across markets.** Align panels without inventing returns on closed days; *honest:* real holiday calendars, the alignment method stated.
6. **Futures contracts needing a continuous series.** Stitch under a roll rule, treat the roll gap; *honest:* the roll rule in a spec, every contract file shipped.
7. **Mixed quoting conventions.** Clean prices in fractions, rates in percent or bp, direct or indirect FX, vol or premium; *honest:* each convention labelled.
8. **Holdings filings with lags and amendments.** Use what was known on each date, keep the latest valid version; *honest:* real filing dates, the as-of rule defined.

## Banking, Credit & Financial Risk  (`banking-credit-financial-risk`)

1. **Monthly loan tapes with status transitions.** Snapshots reshaped into histories under the status codebook; *honest:* the real codebook, payoffs and transfers at natural rates.
2. **Regulatory line items renumbered across form revisions.** A crosswalk across vintages before ratios; *honest:* the revision notes, so the crosswalk is derivable.
3. **Mergers and charter changes.** Aggregate through a structure history without double counting; *honest:* real effective dates, mergers as texture, not a switch.
4. **Bureau sentinel values.** No-trade and not-applicable codes in numeric columns decoded before averaging; *honest:* every sentinel documented as a bureau would.
5. **Ratings on several agency scales.** Mapped to one ordinal scale, the rating in force on each date; *honest:* a real mapping convention named.
6. **Charge-offs and recoveries in different periods.** Recoveries matched back to loans or vintages for net loss; *honest:* realistic lags, the basis (vintage or period) stated.
7. **Reversals and chargebacks as separate rows.** Event types linked into one transaction; *honest:* real processor codes and keys, no phantom duplicates.
8. **Rates on different bases and day counts.** Harmonised before comparing yields; *honest:* each basis labelled, never an unstated convention that decides.

## Actuarial Science & Insurance  (`actuarial-science-insurance`)

1. **Claim transactions needing a triangle.** Payments and reserve changes aggregated by accident period and age, reopenings handled; *honest:* transaction data, a clear date dictionary.
2. **Endorsements and cancellations.** In-force periods rebuilt for earned premium and exposure; *honest:* real transaction types and effective dates.
3. **Accident, policy and calendar year bases mixed.** Each basis identified and aligned; *honest:* the basis labelled per report, the question names its basis.
4. **Published table grids.** Select-and-ultimate grids reshaped long and keyed by issue age and duration; *honest:* native layout and notes, no altered cell.
5. **Bordereaux in differing layouts.** Mapped to one schema, genuine resubmissions deduped; *honest:* dated corrected sends, latest kept by a documented rule.
6. **Peril codes revised.** Counted consistently through a code crosswalk; *honest:* the crosswalk or manual notes, few documented unmapped codes.
7. **Catastrophe claims assigned to events by window.** By loss date and location under the event definition; *honest:* the definition stated, boundary claims natural, not placed.
8. **Member census across valuation dates.** Members matched across dates, exits inferred, reconciled to payments; *honest:* realistic id changes, matching keys documented.

## General Statistics & Data Science  (`general-statistics-data-science`)

1. **Results under inconsistent conventions.** Percent against fraction, best seed against mean, different splits harmonised; *honest:* seed count, aggregation and split labelled.
2. **Resumed and crashed runs.** Each run's history stitched, the right final metric picked; *honest:* run and resume ids with timestamps.
3. **Dataset versions and split manifests.** Examples joined to the right version and split; *honest:* the changelog ships, the question names the version.
4. **Multi-rater annotations with adjudication.** One label per item by the stated rule; *honest:* guideline version per round and the aggregation rule documented.
5. **Nested configs with implicit defaults.** Effective hyperparameters resolved before grouping; *honest:* base and default configs shipped.
6. **Large prediction dumps.** Class indices aligned to the label map and ground truth; *honest:* the index map ships, ordering consistent.
7. **Compute in mixed units and hardware.** GPU hours, accelerator days and wall clock normalised; *honest:* hardware and device count per job, conversion factors.
8. **Near duplicates across splits.** Flagged by provided content hashes under the stated protocol; *honest:* realistic low overlap, handling stated.

## Biomedical & Clinical Research  (`biomedical-clinical-research`)

1. **Trial data split across domain tables.** Demographics, exposure, visits, labs and AEs joined to one row per subject; *honest:* key structure and dictionary, every subject traceable.
2. **Labs in mixed units and ranges.** Units harmonised, flags mapped, the primary lab chosen; *honest:* unit labels and range table, the protocol names the primary lab.
3. **Unscheduled and out-of-window visits.** Study day computed, records mapped to analysis windows; *honest:* the windowing rule in the plan, realistic drift.
4. **Partial dates.** The stated imputation applied before durations; *honest:* the convention in the plan, realistic frequency.
5. **Verbatim terms coded to a dictionary.** Grouped at the right level across dictionary versions; *honest:* the hierarchy file, real version drift and synonyms.
6. **Free-text concomitant medications.** Dose parsed, names standardised, class assigned; *honest:* a drug lookup, real entry habits that careful parsing resolves.
7. **Assays beyond quantification limits.** Censored values handled, repeats chosen; *honest:* limits and repeat rule in the lab manual, native codes kept.
8. **Questionnaires needing a scoring manual.** Reverse items, allowed missing items, form versions scored per manual; *honest:* the manual ships and settles every case.

## Epidemiology & Public Health  (`epidemiology-public-health`)

1. **Small-cell suppression.** Suppressed cells carried honestly through margins, never zero; *honest:* the rule in footnotes, the decision rests on unsuppressed cells.
2. **Provisional counts revised later.** The right vintage per week, reporting lag near the end; *honest:* release dates labelled, the vintage stated, real backfill.
3. **Denominators from mismatched population vintages.** Age bands aligned, the stated series used; *honest:* the series named in a methods note, one correct mapping.
4. **Geographic codes changing over time.** Crosswalks with allocation factors; *honest:* the official crosswalk, the allocation rule stated.
5. **Case definitions and coding revisions.** Confirmed against probable, comparability across the break; *honest:* definition history or ratios, the counting definition named.
6. **Survey microdata with design and skip codes.** Missing codes recoded, design variables used; *honest:* codebook and design notes, a unique stated estimator.
7. **Overlapping reports across jurisdictions.** Deduplicated under matching and episode rules; *honest:* the rules stated, natural overlap only.
8. **Rates on different bases and standards.** Converted and re-standardised to one standard; *honest:* standard weights ship, the base labelled.

## Pharmacology, Pharmacoepidemiology & Safety  (`pharmacology-pharmacoepidemiology-safety`)

1. **Package codes to active ingredients.** 10 and 11 digit formats normalised, mapped through a product crosswalk; *honest:* the real directory, the counting level stated.
2. **Overlapping fills, early refills, reversals.** Reversals netted, fills stitched into exposure; *honest:* realistic rates, stockpiling and grace rules stated.
3. **Spontaneous reports with versions and duplicates.** Latest version per case, genuine duplicates merged; *honest:* real case and version ids.
4. **Verbatim reactions across dictionary versions.** Mapped to the current hierarchy and rolled up; *honest:* the hierarchy file, the counting level named.
5. **Strength strings and dose units.** Parsed into numeric ingredient amounts for daily or cumulative dose; *honest:* genuine string formats, the dose metric stated.
6. **Labs with per-lab limits.** Expressed as multiples of each lab's ULN; *honest:* each lab's range on the row, the threshold defined.
7. **Enrolment months into spans.** Continuous spans for baseline and follow-up; *honest:* genuine gaps and switches, the allowable gap stated.
8. **Partial dates in case records.** Events ordered, time to onset under a stated imputation; *honest:* realistic frequency, the rule in a conventions document.

## Healthcare Delivery & Health Economics  (`healthcare-delivery-health-economics`)

1. **Provider identifiers that do not line up.** CCN, NPI, licence ids and names crosswalked, many-to-many rolled up; *honest:* the crosswalk or the fields to build it, the reporting unit stated.
2. **Cost reports by worksheet, line and column.** Pivoted, codes mapped, fiscal periods aligned; *honest:* the code map, real short periods, the alignment rule.
3. **Claim headers, lines and replacement bills.** Collapsed to the final action claim; *honest:* real frequency or adjustment codes mark replacements.
4. **Negotiated rates in mixed formats.** Dollars, per diems, case rates and percent of charges normalised; *honest:* native nesting, the comparison basis stated.
5. **Coding revisions across years.** Crosswalked so volumes and case mix compare; *honest:* the official crosswalk, the target version named.
6. **Suppression in public files.** Bounded unknowns, never zeros; *honest:* the source's threshold and flag, the handling stated.
7. **Reserved negative codes in expenditure surveys.** Recoded, levels joined, weights applied; *honest:* the codebook, real skip logic, the weight named.
8. **Geographies that do not nest.** Allocation crosswalks onto one geography; *honest:* ratios ship, the target geography and weight stated.

## Economics & Econometrics  (`economics-econometrics`)

1. **Several vintages of one series.** One consistent vintage per calculation, no splicing; *honest:* the vintage named, revisions at ordinary size.
2. **Chained real components that do not add.** Nominal shares or contribution tables, never summed reals; *honest:* the residual line as published, chaining documented.
3. **SA and NSA mixed, annual rates.** Basis aligned before growth; *honest:* adjustment status labelled as the release does.
4. **Indexes on different base periods.** Rebased and spliced at an overlap; *honest:* a genuine overlap and base notes.
5. **Classification codes revised.** A concordance with weighted many-to-many links; *honest:* the real concordance and weights, the answer's classification named.
6. **Mixed currencies, scales and fiscal years.** Units and periods harmonised first; *honest:* notes where the source puts them, the target stated.
7. **Wide panels with flag letters.** Flags split from values, reshaped long, breaks handled; *honest:* the real legend, realistic flag frequency.
8. **Top codes and imputation flags.** Top codes and allocated cases handled per rule; *honest:* top-code values and flags in the codebook.

## Political Science & Public Policy  (`political-science-public-policy`)

1. **Precincts redrawn between elections.** Crosswalked or aggregated to stable units; *honest:* a real crosswalk or the stable unit named.
2. **Canvass reports in printed layout.** Reshaped long, subtotals dropped, ballots cast separated from votes; *honest:* subtotal and over/under rows labelled as published.
3. **Legislator identities inconsistent.** A stable person key across roll calls, rosters and finance; *honest:* real variation only, enough fields to link.
4. **Amended finance reports beside originals.** Latest per period, no double count, memo entries handled; *honest:* real amendment indicators and report ids.
5. **Budget lines across reorganisations.** Codes mapped over time, the stated budget column used; *honest:* the reorganisation note or code map.
6. **Opinion survey codes, waves and leaners.** Codebook and stated weight applied; *honest:* the full codebook, the weight and nonsubstantive treatment named.
7. **Several policy date concepts.** Treatment coded to the date the design requires; *honest:* the defining date stated.
8. **Turnout denominators.** Registered, voting-age or eligible assembled as stated; *honest:* the measure defined, each piece with its coverage notes.

## Sociology & Demography  (`sociology-demography`)

1. **Census geographies changing between decades.** Apportioned by relationship-file weights; *honest:* the real file and weights, the target geography named.
2. **Age bands differ across tables.** Harmonised to common bands, the open top handled; *honest:* bands the inputs support, the open interval rule stated.
3. **Race and ethnicity categories revised.** Consistent categories under a stated scheme; *honest:* definitions per year, no invented recodes.
4. **Suppressed cells and reliability flags.** Handled per rule or aggregated up; *honest:* the real threshold and symbols, no decision on a guessed cell.
5. **Linked household and person files.** Joined by serial, household measures built; *honest:* keys and relationship codebook as documented.
6. **Panels with attrition and refresher samples.** Persons tracked, the stated weight chosen; *honest:* wave naming and weight purposes in the codebook.
7. **Vital events by occurrence or registration.** Counts aligned to the stated basis; *honest:* the basis labelled as the tables do.
8. **Attitude scales changed across waves.** Items harmonised before trends; *honest:* changes in the codebook, the harmonisation rule stated.

## Psychology & Behavioral Science  (`psychology-behavioral-science`)

1. **Reverse-keyed items.** Recoded, subscales scored, item counts checked; *honest:* keying and scoring rules, the version named.
2. **Trial logs from experiment software.** Files stacked, practice dropped by block field, aggregated by condition; *honest:* native practice and timeout codes, the exclusion rule.
3. **Skip logic and several missing codes.** Legitimate skips separated from nonresponse; *honest:* every code listed, a stated denominator rule.
4. **Wide panel waves with attrition.** Reshaped long, presence tracked per wave; *honest:* stable ids, complete-case or all-waves stated.
5. **Online panel screening and repeats.** Screening applied, one record per participant; *honest:* realistic failure rates, the rule in a protocol.
6. **Scale forms and anchors change.** Common items or documented linking; *honest:* the item mapping and anchor change shipped.
7. **Double-coded observations.** Aligned by session and segment, adjudicated, agreement computed; *honest:* realistic disagreement, the rule stated.
8. **Device streams on separate clocks.** Aligned to events, resampled, dropout handled; *honest:* real signal loss, the offset in headers.

## Criminology & Justice  (`criminology-justice`)

1. **Incidents in linked segments.** Segments joined under the counting rule; *honest:* the layout and rule, the unit of analysis stated.
2. **Agencies reporting partial years.** Months-reported read, non-reporting never zero; *honest:* the field as published, the coverage or imputation rule.
3. **Agency codes against jurisdictions.** Crosswalked, overlapping populations allocated; *honest:* the crosswalk and the allocation rule.
4. **Charge-level court records.** Statutes mapped, collapsed by a most-serious-charge rule; *honest:* the map and ranking, the case rule stated.
5. **Repeat custody spells.** Linked on the person id, stays computed, open spells handled; *honest:* the system's own id, open-spell treatment stated.
6. **Dispatch logs with many call codes.** Codes mapped, response intervals computed; *honest:* the code table, the defining timestamps stated.
7. **Masked locations and redrawn beats.** Assigned with the boundary vintage of each period; *honest:* boundary files per vintage, real geocode failure rates.
8. **Victimization files and series incidents.** Files linked, weights and the series rule applied; *honest:* codebook and weight documentation.

## Physical & Environmental Sciences  (`physical-environmental-sciences`)

1. **Station moves and instrument swaps.** Segments split or aligned from station metadata; *honest:* changes documented as networks do, no hidden step.
2. **Censored lab results and qualifiers.** Less-than values and qualifier letters parsed consistently; *honest:* the qualifier codebook, the censoring rule stated.
3. **Mixed units and bases.** mg/L against ppb, wet against dry, CO2e sets harmonised; *honest:* a units column, the conversion basis stated.
4. **Logger clocks in local, DST and UTC.** Time normalised, period-start against period-end labels aligned; *honest:* the basis in headers, genuine transition hours.
5. **Wide sheets with multi-row headers.** Reshaped long, header metadata carried to rows; *honest:* the agency's own layout, every field present.
6. **Provisional and approved records overlap.** Deduped, the approved value kept; *honest:* the source's approval flag, the governing status stated.
7. **Site ids differ across systems.** Crosswalked from ids, names and spatial matching; *honest:* enough fields to match, ambiguous sites outside the decisive set.
8. **QC samples among field results.** Blanks, duplicates and spikes separated, replicates handled; *honest:* real sample-type codes, the replicate rule stated.

## Energy Systems & Utilities  (`energy-systems-utilities`)

1. **Interval reads with estimates and gaps.** Quality codes applied, resolutions aligned, reconciled to billing; *honest:* real codes, totals reconcile within documented estimation.
2. **Hour-ending labels and DST days.** Interval labels normalised before joins; *honest:* each file's convention stated as the operator does.
3. **Fuel units and heating-value bases.** Converted with stated heat contents on one basis; *honest:* heat-content tables, the HHV or LHV basis named.
4. **Plant, unit and generator ids across registries.** Crosswalked and aggregated at the needed level; *honest:* real crosswalk fields, the level set.
5. **Preliminary, final and amended filings.** Deduped to the governing vintage; *honest:* the source's revision flag or filing date, the vintage named.
6. **Tariffs with tiers, riders and effective dates.** Parsed and prorated across rate changes; *honest:* the full tariff, proration per its text.
7. **Outage logs with staged restorations.** Events collapsed, exclusions applied before indices; *honest:* the cause codes and exclusion standard.
8. **Competing capacity ratings.** Nameplate, net summer or winter, AC or DC chosen per metric; *honest:* each rating labelled, the metric's rating stated.

## Human Factors & Ergonomics  (`human-factors-ergonomics`)

1. **Sensor streams at different rates and clocks.** Resampled and synchronised on event markers; *honest:* sync markers and device documentation.
2. **Interaction logs needing sessionisation.** Attempts rebuilt, completion times derived; *honest:* event codes and task start and end definitions.
3. **Item-level questionnaires.** Reverse items and version anchors scored by the key; *honest:* the key ships, version changes documented.
4. **Anthropometric definitions differ.** Units, measured against self-report and landmarks harmonised, weights applied; *honest:* definitions and the percentile method stated.
5. **Safety reports mixing codes and narratives.** Narratives coded, taxonomies mapped, duplicates merged; *honest:* matchable multiple reporters, a taxonomy crosswalk.
6. **Condition orders kept apart from trial data.** Assignments joined, exclusions applied; *honest:* the lab's own logs and a stated rule.
7. **Exposure instruments with different settings.** Normalised to shift exposure, aligned with task logs; *honest:* the standard and exchange rate, settings in headers.
8. **Trial files with practice, timeouts and lapses.** Filtered under the protocol, aggregated per participant; *honest:* the software's flags, the trimming rule stated.

## Survey Research & Official Statistics  (`survey-research-official-statistics`)

1. **Skip patterns and reserve codes.** Who was asked, from codebook and routing; *honest:* the real reserve scheme, the universe stated per estimate.
2. **Replicate weights and design variables.** The right weight set and variance method; *honest:* the full replicate set and variance documentation.
3. **Preliminary, revised and benchmarked vintages.** Releases stacked, the stated vintage selected; *honest:* overlapping vintages with release dates.
4. **SA and NSA side by side.** The series fit for the comparison type; *honest:* both labelled, the comparison implies which.
5. **Footnote symbols in numeric cells.** Symbols parsed into values and flags; *honest:* the agency's legend in the file, no decision on an imputed cell.
6. **Industry and occupation codes revised.** Official concordances with allocation shares; *honest:* the concordance and the target vintage named.
7. **Disposition and paradata files.** Linked to compute response rates under a standard definition; *honest:* the real code list, the formula named.
8. **Wording and mode changes.** The break accounted for before trends; *honest:* the change and any bridge sample documented.

## Urban & Regional Science  (`urban-regional-science`)

1. **Small areas redrawn between vintages.** Relationship-file weights put all years on one geography; *honest:* the real file, target geography and weight named.
2. **Address strings needing geocoding.** Standardised and assigned to areas; *honest:* a parcel or address reference, few genuinely unmatched.
3. **Parcels split and merged.** Lineage traced, condo units not double counted; *honest:* the lineage table, the unit of analysis stated.
4. **Origin-destination matrices.** Reshaped, aggregated, reconciled to totals; *honest:* real suppression and coding, aggregates that survive it.
5. **Overlapping jurisdictions.** Places allocated to the stated area definition; *honest:* the definition and vintage, the delineation file.
6. **Schedules against recorded operations.** Stop and trip keys joined, calendars expanded; *honest:* consistent ids, unmatched trips genuine.
7. **House prices in mixed index forms.** Rebased, frequency aligned, measures kept distinct; *honest:* bases labelled, the measure named.
8. **Local land-use schemes.** Mapped to a common classification; *honest:* every local code list and a stated target.

## Education & Learning Sciences  (`education-learning-sciences`)

1. **School identifiers changing.** Crosswalked across files and years; *honest:* directory files with open, close and id history.
2. **Suppressed subgroup counts.** Masks parsed into flags or bounds; *honest:* real masking rules, comparisons that need no unmasking.
3. **Assessment scales changed.** Comparisons restricted or linked; *honest:* technical notes on the break, comparable years stated.
4. **Student, course and enrolment linkage.** Student-year measures across transfers; *honest:* realistic spells, the attribution rule stated.
5. **Platform event logs.** Sessionised across midnight and zones, retries deduped; *honest:* genuine retries, the schema and session timeout documented.
6. **Year and term conventions.** Periods aligned, labels read correctly; *honest:* each file's convention, the reference period stated.
7. **Programme and course codes revised.** Crosswalked across editions; *honest:* the official crosswalk, the target edition named.
8. **Rubric scores across raters.** Rater rows reshaped, the reconciliation rule applied; *honest:* rubric versions and the rule documented.
