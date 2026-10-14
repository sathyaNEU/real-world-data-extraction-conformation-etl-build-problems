# task184 design note (architecture 2)

Re-root in oviya13ya's Anomaly Detection lane, same number and objective. Architecture 1 (a mobile screening team
posted among eight flagged airports, decided by the lanes each checkpoint actually opens) was sent back at judge pass
3 on Gate C and Gate G and is spent; its two architectures of the stump, the stand-down and then the counterfactual
arm, are in `## Tried and rejected` and in the card's lineage. Nothing of the airport world carries over.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task184.json` (v2), registered 2026-10-14, verdict WARN.
- **Pairing:** Criminology & Justice, `crime-incidence-hotspot-analysis`, objective Anomaly Detection & Diagnostics.
  The domain has never been drawn (zero cards), and the task type is the one the client taxonomy lists against
  Anomaly Detection, so the structural WARN that dogged architecture 1 (a client domain with no task type serving the
  objective) is gone.
- **World:** Kelverstoke, a fictional city in a UK-like island state, and its community safety partnership. The
  Harbourgate quarter is the city's night-time economy: licensed premises, a taxi rank, two car parks and the streets
  between them. People (guard.py names, en_GB, seed 1842): Bethan Murray, Adrian Daniels, Rosie Kelly,
  Joshua Davies; roles fixed at design.
- **Stakeholder, forum, forcing event:** the partnership's community safety manager (role `programme_officer`) puts
  the 2027 patrol slate to the partnership board (forum `committee_or_panel`); the forcing event is the
  tasking contract for the 2027 season, which is let on a fixed number of four-hour patrol slots
  (`purchase_order_or_contract`).
- **Shape 01 (ranked list under a cap):** every one of the week's four-hour slots is a candidate, each graded on the
  offences the patrol would cover there; the cap is the slots the contract buys. The call is the slate, the figure is
  the offences it covers, and the asks add three measures for every slot or quarter. Well over 25 criteria.
- **Strategy and gate:** `grain_or_unit` (the unit of analysis is the offence-hour, not the offence), gate G
  `method_or_model_selection`, gap population then time, generators G1 (unit of value) then G7 (operating window),
  pattern none, layer 2 `estimand_identification` (own:aoristic-weight-against-a-point-in-time), calibration none.
- **Data-native sentence:** a recorded offence carries three timestamps, the earliest it can have happened, the
  latest, and when it was reported, and for the offences this patrol exists to catch the first two are hours or days
  apart, because the victim was asleep, away or had left the vehicle, so each such offence belongs partly to every
  four-hour slot its window touches and the slate is set on that weight.
- **WARNs answered:** `three_rules.strategy_risk` (grain_or_unit) is answered by the analyst test, which files a
  wrong slate with every column read correctly, both recording systems reconciled and every duplicate dropped: the
  decisive quantity is one the solver builds (the weight a window puts on a slot), not one it reads.
  `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, six of the last twelve): the mechanism here is the
  weight a windowed event puts on each candidate slot, not a model picked from a menu, and the batch's variation sits
  in the generators (G1 and G7, neither used on this objective since task85). `repeat.question_form` (which): the
  decision is a slate under a cap, so the leading question asks which slots.
- **Same-puzzle test:** no build on file shares gap population, pattern none and decision `ranked_slate_under_cap`;
  the nearest drivers are 0.08 (task121 v3, task180 v4) and the card carries a differentiation line against task180,
  whose hourly distortion is in which events reach the record at all, where this one's is in where recorded events
  are placed.
- **Sources (one line each):** strategies.md Part 4, G1 (the unit of value: the natural metric leads and the right
  unit flips it) and G7 (the operating window pinned in an operations file, never the prompt); the AD mechanism
  screen's 21 spent drivers, none of which turns on the precision of an event's recorded time.

## Default path

1. Read the extract notes and the counting rules: the offence classes, the two recording systems and the cut-over.
2. Load the legacy incident export and the new records management export, conform the columns, drop the offences that
   appear in both across the cut-over fortnight, and fix the gazetteer so every offence location maps to the
   Harbourgate quarter.
3. Keep the offence classes the tasking contract names and the Harbourgate locations.
4. Take each offence's occurrence time as `occurred_from`, the earliest time it can have happened, and bucket it into
   its day of week and four-hour slot.
5. Sum the offences per slot over the two seasons on record, divide by the seasons, and commission the six slots with
   the most offences.

Ends on: the seven 20:00 to 24:00 slots and Friday 16:00 to 20:00, covering 3,199.5 contracted offences a season, 0.758 of what the golden slate covers.
Golden: Saturday 20:00, Sunday 00:00, Friday 20:00, Saturday 00:00, Sunday 04:00, Saturday 04:00, Thursday 20:00 and Wednesday 20:00, covering 4,223.1 contracted offences a season.

## Stump sentence

A competent solver conforms the two recording systems, drops the cross-system duplicates, fixes the gazetteer, keeps
the contracted classes in the quarter, takes each offence's occurrence time as `occurred_from` and commissions the
seven 20:00 to 24:00 slots and Friday 16:00 to 20:00, covering 3,199.5 contracted offences a season; the step that
lands it there is treating a window as the point in time it starts, when nine in ten of these offences have a window
over four hours long and the weight those windows put on the quarter's after-midnight and early-morning slots is
what the patrol is bought for.

## Three rules

- **Task type:** `crime-incidence-hotspot-analysis`, the client taxonomy's own task type for Anomaly Detection in
  Criminology & Justice: where and when recorded offences concentrate, and which concentration is real.
- **Domain test:** the deciding analysis is aoristic crime analysis, the field's own method for offences whose
  occurrence time is known only as a window: each offence contributes a fraction of itself to every hour its window
  touches, and a slot's weight is the sum of those fractions over the offence classes the patrol covers.
- **Swap:** "which six four-hour slots should the depot's relief crew cover, and how many breakdowns would they
  reach" has no offence discovered on return, no last-seen and found pair and so no window to spread: a breakdown is
  reported when it happens, and the task stops making sense.
- **Layer 1:** two recording systems across a cut-over with different column names and time formats; the same offence
  in both exports under two reference numbers for one fortnight; a gazetteer with two spellings per street; four
  footfall sensors with outages; a tasking plan spreadsheet with hours as text; two clock changes inside the seasons;
  one offence class whose counts jump when a national counting rule changed, documented in the notes. Each is what
  these systems produce, none decides the call.
- **Layer 2:** the shortcut is to treat a recorded offence as an event at a point in time; the expert treats it as a
  distribution over the window it is known to lie in, and sums those distributions into the slot weights.
- **Decisive step:** spreading each offence's weight across the hours of its occurrence window instead of assigning
  it to one hour of it.
- **Not semantics:** `occurred_from` and `occurred_to` mean exactly what they say and the analyst test reads them
  correctly; what the easy route gets wrong is that the decision's quantity is defined over the window, not over
  either end of it.
- **Not rule application:** no filed sentence says how to treat an occurrence window. The counting rules say when an
  offence is recorded and under what class; the tasking contract says how many slots it buys; neither says what a
  slot's offence weight is.
- **Analyst test:** a strong analyst who reads every column correctly, conforms the legacy export to the new records
  management export, drops the cross-system duplicates, fixes the gazetteer and keeps the contracted classes takes
  each offence's occurrence time as `occurred_from` and commissions the seven 20:00 to 24:00 slots and Friday 16:00
  to 20:00, 3,199.5 covered offences a season; wrong, because for nine in ten of these offences the window runs over
  four hours and a point in it is not where the offence happened.
- **Estimand:** the offences of the contracted classes in the Harbourgate quarter whose occurrence window overlaps a
  slot, weighted by the share of the window that falls in it, summed over the seasons on record and divided by the
  seasons; filed in the tasking contract's definition of a covered offence and the quarter's boundary.
- **No decoy:** nothing is planted to be caught. No block is copied, no rule withheld, no memo argues a wrong slate,
  and no shipped artifact ranks the slots.
- **No certified replay:** no published slot ranking or covered-offence figure exists in the pack, so the method
  cannot be recovered by reproducing one.
- **Lesson:** an event recorded with a window is not an event at a time, and a decision scored over sub-daily
  windows has to be built on the weight each window puts on each one. No build on file teaches it: task180 turns on
  which events reach the record, task181 on the opportunities that generate them, task85 on each unit's own
  observation window, and none on the precision of a recorded time.

## Readability screen

Each rung is the move a solver makes to leave the rung below; the decisive rung has to be silent on all six tests.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 1, the window's other end, the discovery time | no | yes, `occurred_to` sits beside `occurred_from` | yes, "when was it found" is the first thing a reader asks of a window | no | no | yes, one column swapped | readable |
| 2, the window's midpoint | no | no, the midpoint is computed | yes, the statistically minded correction to a range | no | no | yes, one mean of two columns | readable |
| 3, the weight each window puts on each slot (decisive) | no: no shipped sentence says an offence contributes to more than one slot, names a weight, or says what to do with a window; the counting rules say when an offence is recorded and under which class, the tasking contract says how many slots it buys and that a covered offence is one that occurred in the quarter while the patrol was on duty, and neither says how to treat a window (asserted by word sweep over every document) | no: no column holds a weight, a duration or a slot, and the weight is built from two timestamps against a recurring grid the solver lays down itself | no: the window's start, its end, its midpoint and the precisely timed subset each name a different slate, and the first three are the three reflexes | no: no shipped figure ranks or scores a slot; the patrol's own tasking plan records the hours worked, not the offences they met | no: keys unique once the cut-over duplicates go, every join matched, no missing day | no: the weight is a sum over 42 recurring blocks of each window's overlap with them, and 92 per cent of the windows cross a block boundary | silent |

## Ladder

Built values from the prototype generator. Offence-equivalents a season, the mean of the two seasons on record.

| Rung | Construction | Slate | Covered a season |
|---|---|---|---|
| 0, default | each offence at `occurred_from` | Sat, Fri, Thu, Wed, Sun, Mon and Tue at 20:00, Fri at 16:00 | 3,199.5 (0.758 of the golden) |
| 1 | each offence at `occurred_to`, when it was found | Sun and Sat at 08:00, Sun and Sat at 04:00, Fri, Thu and Mon at 08:00, Fri at 16:00 | 2,628.2 (0.622) |
| 2 | each offence at its window's midpoint | Sun, Sat, Fri, Thu, Mon, Tue and Wed at 00:00, Fri at 12:00 | 2,880.3 (0.682) |
| 3, golden | each offence spread across the slots its window touches | Sat 20:00, Sun 00:00, Fri 20:00, Sat 00:00, Sun 04:00, Sat 04:00, Thu 20:00, Wed 20:00 | 4,223.1 |

- **The golden's eight, in order:** Saturday 20:00 630.8, Sunday 00:00 628.5, Friday 20:00 614.7, Saturday 00:00
  559.6, Sunday 04:00 539.0, Saturday 04:00 468.8, Thursday 20:00 395.1, Wednesday 20:00 386.5. Ninth is Monday
  20:00 at 347.4, so the cap falls on an 11.2 per cent gap.
- **Why only the spread finds it:** each wrong route concentrates the slate in one band, the evening starts, the
  morning discoveries or the after-midnight midpoints. The golden slate is the only one that spans all three, and
  the two 04:00 to 08:00 slots no reflex reaches are its fifth and sixth members.
- **Variants (asserted):** spreading in one-hour steps instead of 15-minute steps gives the same slate and the same
  covered figure; spreading in proportion to the quarter's own hourly profile of precisely timed offences, the
  refinement in the literature, gives the same slate and the same figure, because the quarter trades from 04:00 at
  the fish market and its taxi rank clears at 05:00, so that profile is not empty in the early morning; and the
  slate computed from the offences' true times, which the generator holds and the pack never ships, is the same
  eight slots. The hygiene reflex has nothing to keep: every contracted offence's window runs at least two hours
  and nine in ten run over four, so dropping the imprecise records empties the population rather than cleaning it.
- **Worth:** every one of the 42 slot figures is wrong on every wrong basis, and the covered figure is 24 to 38 per
  cent low; a rung-0 response keeps four of the eight slot names and not one figure.

## Tried and rejected

- The seed's idle lane positions as the decisive limit (2026-10-12, at the draw): a per-airport cap that removes the
  natural pick and re-places it, strategies.md F3's dead form (58 v3 and v4).
- Lane capacity observed only while a queue stands, so passengers per lane-hour measures demand at quiet airports
  (2026-10-12, at the draw): task127's driver (a team's capacity visible only as the ceiling it held through a surge).
- Transfer passengers who never reach the landside checkpoint, so departing seats overstate the hub's summer demand
  (2026-10-12, at the draw): the share of a flight's passengers who pass the checkpoint is one ratio per route, and a
  bottom-up build calibrated to last summer's checkpoint counts at airport level already lands close to the call, so
  the decisive step is one enumerable correction.
- The release at only Cullinvale, Ardcarrig and Faranloe, four hosts releasing nothing (2026-10-12, at build): the
  default path kept 15 of the 24 airport-period figures and the averaged path 21, so a response off the call banked
  most of the airport figures; every host but Halloran Bay now stands down two lanes all day.
- Dromkeel as last summer's realised-effect leader (2026-10-12, at build): on the simulated 2026 feed Cullinvale's
  deep queues give it the largest realised effect (1.48 times Eskerford) under every demand Dromkeel's checkpoint
  clears by close; the lateral rung lands on rung 0's answer and the ladder runs three rungs.
- Asking for each airport's figure by period (2026-10-12, at build): 24 construction figures the cracker holds put the
  pair near 44; the prompt asks each airport's summer figure.
- Sinusoidal design days with flat banks (2026-10-12, stage 4): the leak reader read them as synthetic-smooth and the
  same shape at every airport; the design days now carry a late-morning wave, an afternoon lull, a thinning last hour,
  cresting banks and rough 15-minute noise.
- "How far the chosen airport's forecast passengers could fall short before another posting would move more"
  (2026-10-12, judge pass 1): read as the last whole per cent still ahead or the first behind; the prompt asks the
  smallest whole per cent shortfall at which another posting would move more.
- Taking the stand-down as the whole decisive step (2026-10-14, the hardening): the first architecture's single layer,
  shipped 10-12. The portal left it off the approved list, so the posted-day gap against the roster pattern is now
  rung 2 and the decisive step is the counterfactual arm: both sides of the comparison read from the lanes each
  checkpoint actually opens. Every figure moved; the call moved from Halloran Bay to Eskerford.
- The host stand-down measured against matched non-posted weeks, with the crowd-out as the difference (2026-10-14, at
  the hardening): the quiet-hour closures a matched-week design nets out never breach the standard, so the correction
  was worth nothing on the graded quantity (stumping Part 3, a rung measured on the graded figure). The same
  comparison against the checkpoint's own days moves the baseline arm, where it is worth 23 to 40 per cent of every
  airport's figure.
- A chronic shortfall across the whole rostered peak window (2026-10-14, at the hardening): two lanes short through
  Eskerford's plateau put its 2027 design-day waits over 95 minutes and left 58 of 78 simulated 2026 days with a
  queue at close, which no national agency would run a summer on. The shortfall now sits on the pattern's shoulders,
  which keeps the 2026 sensor's 99th percentile at 50 minutes.
- A shallow-breach world (the banks just above the pattern's capacity) to make the shortfall cheap in queue time
  (2026-10-14, at the hardening): with the plan barely breaching, the unit's three lanes fully relieve every
  checkpoint, so the stand-down stops biting and rung 2 collapses onto rung 0's answer; the ladder needs the banks
  deep enough for a two-lane stand-down to leave a residual.
- The whole hardening: the counterfactual arm read from the checkpoint's own days against its filed roster pattern
  (2026-10-14, judge pass 3): built, green on every free gate and 1.26 times clear on the call, and sent back on the
  architecture. The forward lanes are not filed, so both arms rest on an inference from last summer, and the
  difficulty is the refusal of an official artifact, which Gate G bans at any depth. The repair that would close the
  fork (filing the persistence, or naming the lane sensor record as the basis) is the one `/fix-determinism` forbids,
  because it turns the decisive step into rule application. The number re-roots at stage 1: the next draw needs a
  Layer 2 family that does not turn on a plan the records contradict.
- Architecture 1 as a whole, the airport posting world (2026-10-14, re-root): spent at judge pass 3 (Gate C, the
  forward lanes are not filed; Gate G, surface_read_rejection). Architecture 2 draws Criminology & Justice, where the
  deciding quantity is the weight a recorded offence's occurrence window puts on a patrol slot, so no filed artifact
  is refused and no forward fact has to be inferred from a past regularity: every offence's window is in the record
  and the estimand is defined over it.

