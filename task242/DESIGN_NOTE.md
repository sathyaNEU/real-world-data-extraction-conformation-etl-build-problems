# task242 design note

Architecture 1, wave 3, seed DQ15 (whether an item's published prevalence carries a misclassification flag): the
seed's decision (which published prevalences carry the flag) and quantity (a prevalence corrected for the test's
sensitivity and specificity) only. The seed's survey world is the third survey pairing this wave would draw and its
pitfall (false positives ignored) is a formula executed, so the world moves to a city's dengue surveillance: a
municipal corporation in a southern Indian state ran a post-season household serosurvey in its 12 zones from mid
October to early December 2027 and published each zone's IgM-positive share as the share of residents infected with
dengue in 2027. Before the council's public health standing committee settles the 2028-29 vector-control allocation by
zone, the city epidemiology cell sets the quality flags on the indicators it publishes; a value that misstates the
quantity it stands for beyond the tolerance carries the misclassification flag.

## Draw

Card `cards/task242.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, each answered here:
repeat.gate_g and overuse.gate_g (method_or_model_selection against task469, a record-linkage dial, and in 8 of the
last 12: the key is the generic mechanism, the honest one for a choice between the panel's single sensitivity and the
sensitivity each zone's timing gives; no quantity or file is shared with any of them). test.same_puzzle_older and
test.same_driver_older (task229 v2, task461, task501 v4) and the nearest driver (task230 v2, 0.11) are differentiated
on the card.

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, serving Data Quality
  Monitoring & Alerting. Not banned against the last three builds (task241, task469, task194). The object is the
  health of the surveillance programme's own published serosurvey indicator (whether each zone's value stands for
  what the indicator register says it measures), the call a monitoring decision: which values carry the flag.
- **Niche.** IgM serosurveys read recent infection: IgM to dengue appears around the fifth day of illness and fades
  over the following two to three months, so a post-season IgM survey sees a season's infections only through that
  window, and how much of a zone's season it sees depends on where the zone's epidemic sat against its fieldwork.
- **The call.** Which of the 12 zones' published 2027 dengue infection shares carry the misclassification flag (the
  share of residents infected since 1 January to their specimen's collection, estimated with the assay's measured
  accuracy, more than 1.5 times or less than two-thirds of the published value).
- **Shape.** 07, a grid of cells: one row per zone with its published share, the share infected since 1 January and
  the flag, beside the zone's columns for the asks (12 rows, the call picked per row), the flagged set, the chart
  (each zone's published and estimated share against the tolerance band, flagged zones marked) and the two files:
  well over 25 criteria before the rubric folds them. Decision designation_set, answer set_of_items, question form
  which.
- **Strategy.** composition_mix (the panel's sensitivity is the assay's curve averaged over the panel's own mix of
  days since onset; each zone's is the same curve averaged over its own mix, which its epidemic timing sets), G13
  decisive (the marker's window of detection against the indicator's window since 1 January), G6 (the mix of days
  since onset shifts from the panel to each zone), G14 (the sensitivity conditioned on days since onset); gap time
  first (when the infections happened against when they were read) then population (the panel's specimens are not
  the zones' infections); Gate G method_or_model_selection (a single sensitivity against the zone-specific one the
  data forces); calibration gold_standard_subsample (the laboratory's verification panel: sera from confirmed cases
  at known days since onset, and controls); context artifact published_series (the zone values the corporation
  published); layer 2 family field_method, pattern own:igm-serosurvey-attack-rate-through-the-detection-window.
- **Forum, event, organisation.** council_or_assembly (the corporation council's public health standing committee),
  budget_or_appropriation (the 2028-29 vector-control allocation by zone), local_government (a municipal
  corporation's public health department). All clear the last three.
- **People** (`guard.py names --geo India --seed 242`, locale en_IN): Vedika Varghese, the city epidemiologist who sets
  the quality flags; Shaurya Issac, the medical college microbiologist whose laboratory tests the survey's specimens
  and ran the kit's verification panel; Gauri Kant, the serosurvey's field coordinator.
- **Deliverables.** `dengue_igm_flag_review_2027.xlsx` (each zone's row: published share, estimated share since 1
  January, flag, and the asks' columns) and `dengue_igm_flags_health_committee.pptx` (the slide for the standing
  committee: each zone's published and estimated share against the band, flagged zones marked). Names provisional
  until stage 3.
- **As-of.** Monday 10 January 2028: fieldwork closed on 6 December, the laboratory released the last results on 17
  December, the zone values were published in the December bulletin, and the standing committee meets on 24 January.
  The call is retrospective by nature (a quality flag says whether a published value stands for its quantity, and the
  quantity is the season's infection share); what it settles is which values reach the committee with the flag.
- **Data-native sentence.** The zones were surveyed one after another from mid October to early December while their
  epidemics peaked anywhere from August to November (some zones carried both the south-west and the north-east monsoon
  waves), and the assay finds IgM in nearly every infection in the first six weeks after onset and in few after three
  months; so the share of a zone's 2027 infections still detectable at collection is set by where its own epidemic
  curve sat against its fieldwork, which the laboratory's panel, built from cases at follow-up visits, cannot carry.

Sources, one line each (what it teaches; how this build differs):
- Rogan and Gladen (1978): an apparent prevalence corrected for the test's sensitivity and specificity; here the
  sensitivity that enters is not the assay's alone but the assay's curve over the population's own days since onset.
- Recent-infection incidence assays (the mean duration of recent infection, Kassanjee and colleagues, 2012):
  incidence read from a marker whose detection fades with time since infection; their steady-state shortcut fails in
  an epidemic season, so here the curve is carried through each zone's epidemic, never named in the pack.
- Dengue IgM kinetics (WHO dengue guidelines, 2009: IgM from about day five, detectable for two to three months): the
  world's structure, generated, never a real dataset.
- Post-outbreak IgM serosurveys estimating attack rates: the field's practice; the timing correction is the analyst's
  to find from the panel and the case line list.

## Default path

1. Read the indicator register and the quality standard: the zone value is the share of tested residents with a
   reactive IgM; it stands for the share of the zone's residents infected with dengue between 1 January 2027 and
   their specimen's collection; the flag goes on when that share, estimated with the assay's measured accuracy, is
   more than 1.5 times or less than two-thirds of the published value.
2. From the laboratory's verification panel: sensitivity is the reactive share of the confirmed-case specimens
   collected from the fifth day of illness on, specificity the non-reactive share of the control specimens.
3. Each zone's published value from the participants' results (reactive over tested), matching the bulletin.
4. The Rogan-Gladen estimate (p + Sp - 1) / (Se + Sp - 1) for each zone, and its ratio to the published value.

Ends on: no zone flagged (every ratio between about 0.8 and 1.35; prototype figures, to be replaced by the tuned
simulator's).

Golden: six zones flagged (four surveyed long after their epidemic, two whose early wave sat outside the window while
a late wave sat inside it), from each zone's effective sensitivity: the panel's sensitivity by days since onset
averaged over the zone's cases by onset date from 1 January up to each specimen's collection.

## Stump sentence

A competent analyst corrects each zone's published IgM share by the Rogan-Gladen estimator with the laboratory
panel's sensitivity from the fifth day of illness on and its specificity, finds every corrected share within 1.5 times
the published value and flags no zone; the step that lands it there is taking the panel's sensitivity as the assay's
sensitivity in every zone, when the zones surveyed months after their epidemic had most of their 2027 infections past
the weeks in which IgM is found, so only the panel's curve averaged over each zone's own onset dates up to collection
gives the six.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting (the surveillance programme's own published indicators are the monitored data, the
  misclassification flag the monitoring decision).
- **Domain test:** the quantity that decides is each zone's dengue attack rate since 1 January, estimated from IgM
  serology the way serosurvey epidemiology estimates incidence from a recent-infection marker: the assay's detection
  curve by days since onset (the laboratory's panel) averaged over the zone's own epidemic curve (cases by onset date)
  up to each specimen's collection, then the Rogan-Gladen correction with that effective sensitivity and the panel's
  specificity.
- **Swap:** "which zones' published dengue infection shares carry the misclassification flag" rewritten as "which
  wards' published bed-occupancy shares carry the flag" with admissions for infections: there is no antibody whose
  detection fades after the event and no epidemic curve to carry it through, so the effective sensitivity has nowhere
  to come from and the task stops making sense; with megawatt-hours the same.
- **Layer 1:** the case line list (the city's dengue surveillance, fed by hospitals and laboratories) carries
  day-month-year dates, onset and notification dates days apart, the 2026 season's tail and patients resident outside
  the city, and zone names spelt as each reporting unit writes them; the laboratory's panel export gives onset and
  collection dates rather than days since onset, with equivocal results retested; the survey's specimens were
  collected across each zone's ten-day fieldwork. Each is produced by the system that records it; none is placed to be
  caught, and the call is the same under every handling of each (asserted).
- **Layer 2:** field_method: the effective sensitivity of a fading recent-infection marker for a cumulative attack
  rate, the assay's curve carried through each zone's own epidemic timing, against the panel's single sensitivity.
- **Decisive step:** taking each zone's sensitivity as the panel's sensitivity by days since onset weighted by the
  zone's distribution of days since onset at collection, which the zone's epidemic curve gives, rather than one
  sensitivity for every zone (pooled over the panel, over a fixed window, or at the zone's peak).
- **Not semantics:** reading every field right (onset and collection dates, results, zones, the window since 1
  January) still leaves the single-sensitivity correction on no zone flagged: the panel's days since onset are plain
  dates, and reading them right does not say how the zones' timing enters.
- **Not rule application:** the indicator register files what the value stands for and the quality standard files the
  tolerance; no filed rule or procedure says how the infection share is estimated from IgM results, so executing every
  stated rule with the panel's sensitivity files no flag.
- **Analyst test:** a strong analyst who reads every file right and applies the flag rule as filed corrects each
  zone's IgM share by Rogan-Gladen with the panel's sensitivity from the fifth day on and its specificity, puts every
  zone between about 0.8 and 1.35 times its published value and flags none (Ends on: no zone flagged), where the golden
  flags six; one who uses the city's whole epidemic curve flags eight, and one who takes the sensitivity at the zone's
  peak or a fixed window of 60 or 90 days misses the zones with two waves or a short outbreak.
- **Estimand:** the indicator register (`zone indicator register`, in the pack) defines the zone value's quantity (the
  share of the zone's residents aged one year and over infected with dengue virus between 1 January 2027 and the
  collection of their survey specimen) and the published value (reactive over tested); the quality standard files the
  comparison and the tolerance (estimated share more than 1.5 times or less than two-thirds of the published value).
- **No decoy:** nothing is planted: no memo, draft or stakeholder figure argues a sensitivity or a flag; the panel is
  the laboratory's own verification export with no headline sensitivity; the bulletin's values are the figures under
  review, and no file ranks the zones on the flag.
- **No certified replay:** no certified or published 2027 attack rate exists for a method to reproduce; the method is
  found from the panel's structure and the zones' timing.
- **Lesson:** an IgM serosurvey measures a season's infections only through the marker's window, so its sensitivity
  for a cumulative attack rate depends on each population's epidemic timing against its fieldwork; no build on file
  reads a share through a detector whose sensitivity fades with the time since the event (task233 carries a gold
  standard's departure across base rates; task241 reads a sensor against a moving reference).

## Tried and rejected

- The seed's pitfall (false positives ignored in a rare trait's prevalence): executing the Rogan-Gladen formula is
  rule application; it stays as a lower rung every route shares; dropped as the stump at the draw.
- The seed's survey world: a third survey pairing in this wave (task238, task240); dropped at the draw.
- Two-phase validation of a register flag (a validation subsample weighted back to the register): its honest label is
  population_selection, banned against the last three builds; dropped at the draw.
- Transporting a test's sensitivity and specificity from the validation population to another prevalence: too close
  to task233 (a departure carried across base rates) and task230; dropped at the draw.
- Brazil as the world: the surveillance system's records and documents would be in Portuguese; the district and city
  framings of an English-language surveillance system in India kept the field, and the city corporation clears the
  organisation-family ban (a state government agency repeats task159); dropped at the draw.
