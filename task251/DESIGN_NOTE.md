# task251 design note

## Draw

Card `cards/task251.json` (architecture 1, drawn 2026-10-20). Guard verdict WARN, no BLOCK. The draft card's five
BLOCKs were redrawn rather than argued: the role (compliance, against task474 v2) is now the network's head, who owns
the round list, which is the honester label anyway; the strategy (decomposition_attribution, against task475) is
`other` with the reason in the card's notes, since none of the listed strategies names a reference that ages; the gap
and generator (population and G3, the same puzzle as task468 v4, task450 v1, task101 and task121) are now objective
(the span ratio is reported correctly and the decision is scored on the gain against true SO2) and G13 (the certified
concentration holds at its certification date, not on the night of use), which is what the mechanism is. The WARNs,
answered: overuse.domain (Physical & Environmental Sciences in 4 of the last 12; the seed's domain, and this slot's
neighbour task250 is a temperature network's quality control, a different instrument, reference and decision);
overuse.shape (10 in 3 of 12: the decision is a set of analyzers each read against one tolerance, a scorecard by
nature); repeat.deliverables (xlsx and png after task471 v3: the round list is a workbook and the gains read at a
glance in a chart); repeat.question_form (which, after task474 v2: the decision is a designation set). driver.near
0.14 against task249 v2, differentiated on the card (there the units stood apart from references that shared the truth
only in mixed hours; here the reference stands with the unit and loses strength with its own age). `guard.py slots`
for span, cylinder, reference gas and decay: no slot note holds the mechanism. task249 v1 spent this seed's own
pitfall (the errors-in-variables slope, landed by the reader).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring & Alerting; drawn for Data Quality Monitoring & Alerting. The object is the health of the network's SO2
  measurements, and the call is a monitoring decision: which analyzers go to the recalibration round.
- **The seed, re-found.** DQ24 gave the world (instruments read against references), the decision (which instruments'
  calibration factor breaches tolerance) and the quantity (each instrument's gain). Its pitfall, the attenuated slope
  between two noisy instruments, is spent (task249 v1); the decisive step is re-found in the data's own structure:
  the reference the routine checks read against loses strength as it ages.
- **Niche.** Fundición Caleta Lobos, a copper smelter on the Atacama coast, runs the SO2 network its decontamination
  plan requires (Red de Monitoreo Bahía Lobos): twelve stations with UV-fluorescence analyzers, duplicated at the three
  compliance stations. Every night each analyzer is spanned through its dilution calibrator against its own on-site
  span-gas cylinder (SO2 in nitrogen, from two suppliers, each certified at filling); at the monthly visit the
  technician adjusts it when the span reads more than 2 per cent off, and changes a cylinder that runs low or whose
  certificate lapses, reading the analyzer on the outgoing and the incoming cylinder minutes apart. In January 2028 an
  accredited laboratory recalibrates, against fresh certified gas, the analyzers outside the network's 5 per cent
  tolerance against true SO2.
- **The call.** Which analyzers go to the January 2028 round: those whose gain against true SO2 on 31 December 2027
  lies outside the 5 per cent tolerance.
- **Shape.** 10, a scorecard: each analyzer's gain against the tolerance and its flag, with the asks; designation set,
  question form which.
- **Strategy.** `other` (reference ageing): a span gas of reactive SO2 loses SO2 to its cylinder as it ages, so an
  analyzer adjusted to read an old cylinder's certified concentration reads high by the gas the cylinder has lost, and
  its nightly spans against that cylinder read in tolerance; the cylinder changes, read on both cylinders minutes
  apart, show each supplier's loss rate. Gate G decomposition_attribution (the analyzer's apparent agreement split into
  its own gain and its gas's loss); G13 decisive, G3; gap objective, then population; calibration
  parallel_run_overlap (two references read by one analyzer over the same minutes); context artifact
  monitoring_export; Layer 2 field_method, pattern own:span-gas-loss-written-into-the-analyzer-by-adjustment.
- **Forum, event, organisation.** operations_desk (the network desk books the round), purchase_order_or_contract (the
  laboratory's January round is ordered by purchase order), manufacturer (a smelter). Role field_unit_lead (the head
  of the SO2 monitoring network).
- **People** (`guard.py names --geo Chile --seed 251`, locale es_CL): Daniela Ferrada, head of the monitoring network,
  who asks; Vicente Toloza, the field technicians' lead; Néstor Fuentes, the accredited laboratory's account manager.
  None appears in the prompt.
- **Data-native sentence.** A low-concentration SO2 span gas loses SO2 to its cylinder as it ages, so every adjustment
  of an analyzer to an aged cylinder writes the gas's loss into the analyzer and the nightly spans against that same
  cylinder cannot see it; the cylinder changes, each read on both cylinders minutes apart, measure the loss by
  supplier, and an analyzer's gain against true SO2 is its span ratio over the fraction of SO2 its cylinder still
  holds.
- **As-of.** Monday 3 January 2028, before the laboratory's round on 17 January.
- **Sources.** The client's two-layer standard; the stability of low-concentration reactive gas standards and their
  certificates' validity (ISO 6142 and ISO 6143 practice, EPA Protocol gas certification); EN 14212 quality assurance
  for UV-fluorescence SO2 analyzers (span checks, as-found and as-left, adjustment criteria).

## Tried and rejected

- The seed's own pitfall (the errors-in-variables slope between two noisy instruments): spent by task249 v1, landed
  by its reader.
