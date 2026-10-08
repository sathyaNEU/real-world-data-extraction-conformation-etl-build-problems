# AD47 — What the month's surge of impossible ship movements is, and which notice goes out, when no single cause holds a majority

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · maritime tracking data |
| Mirrors | Location-integrity teams deciding whether a spike of impossible movements is spoofing, shared device IDs or connectivity gaps (GPS spoofing on ride-hail and delivery platforms such as Uber and DoorDash, fleet telematics providers, location services at Apple and Google), where the honest characterisation is sometimes that no single cause dominates |
| Decision shape | Hold, forced by a blocking quantity, on a structure the body adopts: the bulletin's characterisation of the surge (interference, shared identities, reception gaps, or mixed), which sets the notice issued |
| Committed call | The characterisation adopted in the monthly integrity bulletin, with the share that decides it, and therefore which notice (if any) goes out |
| Gap · Pattern | Gap 2 (population: which alerts belong to which cause) over Gap 4 (rule recovered from settled records) · hold forced by the largest attributed share, with the population a flag suggests (validly formatted identities that are two vessels) below it |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #1 reports a failed back-test, ships anyway · #4 never tests its reading against the control |
| Calibration form | Settled-transaction ledger: the pilotage authority's settled invoices for the month, each job's vessel, boarding position and boarding time |
| Driving force | Three causes leave the same mark (a ship that seems to jump) and each attribution order hands the overlap to whichever test runs first: the common-mode cell test claims busy approaches full of shared identities, an identity-first order claims ships that were really jammed, a gap-first order claims jammed ships whose messages dropped. The pilotage ledger, where a pilot boarded a known ship at a known point and time, reproduces only one order, and on that order interference holds 46% of alerts, shared identities 35% and gaps 19%. No cause holds the majority the bulletin requires, so the honest characterisation is a mixed surge and no cause notice goes out. |

## 1. Situation

A maritime analytics provider saw "impossible movement" alerts in the southern Baltic rise to 40,000 in a month. Its monthly bulletin must
characterise the surge, and its policy names a cause, and issues that cause's notice (a navigational interference warning to authorities and
shipping, a data-quality notice on shared identities, or a coverage notice), only when the cause accounts for more than half of the month's
alerts on the provider's attribution; otherwise the bulletin reports a mixed surge and issues no cause notice. The provider holds the
month's position and static AIS messages, its alert replay, the pilotage authority's settled invoices and last spring's confirmed jamming
episode. Customer success wants a jamming warning out this week.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the messages, the alerts, the identity validity flags, the static messages and the pilotage invoices.
  Customers are right that jamming occurred, and the data engineers are right that shared identities are rife. Nothing is overturned; the
  difficulty is attributing overlapping evidence, and then accepting what the attribution shows.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and last spring's episode. Each natural attribution order still names a majority cause and a notice.
* **Instrument repair.** Make every AIS message perfect: a jammed receiver still reports a displaced position honestly, two ships sharing an
  identity still both transmit it, and the overlap between causes is in the world, not the file.
* **Lens swap.** The naive structure assigns contested alerts by test order; the answer assigns them by what the settled record shows
  happened to those ships, which moves 25 to 30 points of share between causes and turns a named cause into a mixed surge.

## 3. The driving force

A strong solver starts from the common-mode test (ten or more ships jumping in one half-degree cell in one hour) and finds interference at
71%. It then sees that a validly formatted identity can be two ships, finds them by joining position messages to static messages where the
ship's registry number alternates within a day, attributes their alerts first and finds shared identities at 56%. Or it applies the
kinematic gap test first (a long message gap with a plausible speed over it) and finds gaps at 58%. Each order is defensible, each commits,
and each assigns the overlap to whatever runs first: jammed ships lose messages, so they also fail the gap test, and shared identities crowd
busy approaches, so they also pass the common-mode test. The pilotage invoices settle the overlap: a pilot boarded a known ship at a known
point and minute, so an alert on that ship near that minute is a displacement, another ship's position, or a coverage gap. Only one order
reproduces all 412 ledger-checked alerts, and on it nothing reaches half.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Common-mode cell-hour test first, then concurrent kinematic tracks, then gaps: interference 71%, shared identities 18%, gaps 11% | Interference: issue the jamming warning | The industry's standard common-mode test | The static messages: 3% of validly formatted identities alternate between two registry numbers within a day and carry 35% of alerts |
| 1 | Identities first (shared identities found through the static-message join), then common-mode, then gaps: shared identities 56%, interference 33%, gaps 11% | Shared identities: issue the data-quality notice | The validity flag fails 3% of identities, and identity before kinematics is the textbook order | The ledger: 61 of the alerts this order calls shared identity are on piloted ships whose AIS position sat exactly on a displaced track at boarding |
| 2 | Kinematic gap test first, then identities, then common-mode: gaps 58%, shared identities 24%, interference 18% | Reception gaps: issue the coverage notice | Long gaps with plausible speeds are the cheapest explanation | The ledger: piloted ships whose alerts follow a dropout inside a jammed cell-hour were displaced, not merely unheard |
| 3 | **Decisive:** the order that reproduces all 412 ledger-checked alerts (common-mode on single-ship identities, then shared identities outside jammed cell-hours, then gaps outside them) | **Hold: a mixed surge, no cause notice; the largest share is interference at 46%** | — | — |

* **The blocking quantity.** On the only reproducing attribution, interference holds 46% of the 40,000 alerts, 4 points below the policy's
  majority line; shared identities hold 35% and gaps 19%. Every cause fails the same standard, each by a stated margin.
* **Partial correction priced (L3).** A solver who uses the ledger to choose among the textbook orders, instead of building the order it
  implies, takes the identity-first order (288 of 412, the best of the three) and issues the data-quality notice on shared identities at
  56%, 6 points over the line. A solver who builds the reproducing order but finds shared identities through the validity flag sees almost
  none of them, lets interference claim their approaches, and issues the jamming warning at 74%. Both name a cause, not the hold.
* **Grid.** Attribution order (the six simple orders and the ledger-reproducing one) × identity population (validity flag or static join) =
  14 partitions. Every simple order hands the overlap to its first test and names that cause at 56% to 75%; the reproducing order with the
  validity flag names interference at 74%; only the reproducing order with the static join leaves the largest share below half. The
  nearest wrong cell, identity-first with the static join, sits 10 points above the answer's 46%.
* **Falsifiable.** Interference would have been named, and the warning issued, with about 1,600 more interference alerts (4 points of share),
  or had the ledger shown the contested approach cell-hours as displaced rather than shared.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The bulletin policy states the majority rule; no document says the causes overlap, gives an attribution order, or
   connects the pilotage invoices to AIS.
2. **The corpus pins a construction, not a menu (Pattern B).** The reproducing order matches all 412 alerts on piloted ships within ten
   minutes of boarding; the identity-first order matches 288, gap-first 263, common-mode-first 241. Each rival errs toward its own first test,
   so each misses the ledger's category totals as well. The order is fixed only through a join from invoice registry number to static
   message to identity to alert, which no listed option offers.
3. **No arithmetic symptom.** Every alert gets exactly one cause under every order, so every partition sums to 40,000 and every reconciliation
   passes.
4. **Not a row predicate.** Shared identities need static messages grouped by identity and day; jammed cell-hours need distinct ships counted
   per cell and hour; the ledger check needs invoices joined to identities and to alerts in time.
5. **The enumeration is arithmetic.** Each alert's cause is computed; no column carries it.
6. **No cutover date.** Jamming, shared identities and coverage gaps run through the whole month; no series steps on a date.
7. **Survives deletion.** Remove both voices and the spring episode, and each natural order still commits to a notice.

## 6. The calibration corpus

* **Form.** The pilotage authority's settled invoices for the month: 1,150 jobs, each with the ship's registry number, the boarding position
  and the boarding time.
* **What it pins.** The attribution order (above), through the 412 alerts that fall on piloted ships within ten minutes of boarding.
* **Every rule exercised.** The ledger holds displaced ships inside jammed cell-hours, shared identities in busy approaches outside them, and
  coverage gaps in the outer approaches, so each step of the order is tested where it competes with another.
* **Twin pair.** Two approach cell-hours each held 14 alerting identities and 120 alerts at the same hour of day and traffic density. The
  ledger shows one jammed (pilots boarded ships whose AIS sat 6 miles off) and one crowded with shared identities (AIS showed other ships),
  so their interference alerts are 96 and 41, about 2.3× apart, separated only by the ledger-reproducing attribution.
* **Resemblance points at the decoy.** The month's cell-hour pattern resembles last spring's confirmed jamming episode, when interference
  held 78% of alerts.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The bulletin policy: a cause is named, and its notice issued, only when it accounts for more than half the month's alerts on
  the provider's attribution; otherwise the bulletin reports a mixed surge. The AIS field description (position and static messages). The
  pilotage ledger as the authority's settled record. One sentence each.
* **Empirical pins.** The attribution order, from the ledger.
* **Voices.** The customer success lead: "Customers are asking about jamming; they need a warning this week." The data engineering lead:
  "Half these identities are junk; it is an identity problem."
* **Licensed wrong basis.** The policy records that the national maritime authority's monitoring desk attributes alerts by the common-mode
  test alone and will publish its own reading.

## 8. Determinism by construction

* **Shared identities.** Every shared identity alternates between exactly two registry numbers on every day it is active, and no identity
  changes registry number for any other reason in the month.
* **Thresholds.** Alerting cell-hours hold either four or fewer ships or twelve or more, and message gaps run under ten minutes or over 45, so
  the common-mode count and the gap length are threshold-free.
* **Ledger matching.** Each invoice's registry number maps to one identity on the boarding day, and no alert on a piloted ship falls between
  ten and twenty minutes from boarding.
* **Shares.** Shares are of the month's 40,000 alerts and are reported to the whole percentage point; 46% sits clear of 50% under any rounding.

## 9. Prompt sketch and deliverables

> The integrity bulletin goes out on the 5th and customers want to know what is behind this month's surge of impossible movements. Customer
> success wants a jamming warning out now. Tell me what the surge is and which notice we issue, or that we issue none, in a line for the
> bulletin, with the share that decides it. Send `surge_attribution.xlsx`, a chart `cause_shares.png`, and a one-page `bulletin_note.pdf`.

* `surge_attribution.xlsx` — the cause shares under each attribution order with each order's ledger reproduction (ask C), the port-call sheet
  (ask A) and the bunker sheet (ask B).
* `cause_shares.png` — stacked bars of the three causes' shares under each of the four rung orders, the 50% line drawn and labelled, the
  ledger reproduction count above each bar, and the verdict in the title.
* `bulletin_note.pdf` — the committed characterisation, the blocking quantity and what would have named a cause.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six ports in the region, port calls in the month and median berth time. *Device:* a
  ship that shifts berth within a port gets a new call record under the same voyage number, and the register guide counts one call per voyage
  number; counting rows inflates calls and shortens berth times at four ports. The attribution never uses the port register.
* **Ask B (device-carried).** For each port, bunker fuel delivered in the month and the share of deliveries within the sulphur limit.
  *Device:* some suppliers' notes state sulphur in per cent by mass and others in parts per million, as the delivery-note specification says;
  comparing raw values fails every ppm-reported delivery.
* **Ask C (validity).** For each of the four rung orders: the three cause shares and the ledger alerts reproduced.
* **Decoupling.** Clearing the attribution order and the static-message join changes no figure in asks A or B.

## 11. Rubric arithmetic

6 ports × 2 (ask A) + 6 × 2 (ask B) + 4 orders × 4 (ask C) + the committed characterisation, the blocking share, the runner-up share and the
falsifiability margin + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* 40,000 alerts. Partitions: 71/18/11, 33/56/11, 18/24/58 and the reproducing 46/35/19 (interference/shared/gaps); the reproducing order
  with the validity flag gives interference 74%. No non-answer partition has a largest share under 56%.
* Shared identities: 3% of validly formatted identities, carrying 35% of alerts on the reproducing order.
* The ledger: 1,150 jobs, 412 alerts within ten minutes of boarding; reproduction 412 / 288 / 263 / 241.
* The twin approach cell-hours are identical on every alert and traffic column.
* Port calls and bunker notes never touch AIS messages, alerts or the pilotage ledger.
