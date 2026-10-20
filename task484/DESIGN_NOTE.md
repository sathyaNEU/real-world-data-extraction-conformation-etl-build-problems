# task484 design note: a state population unit's 2027 revenue-sharing tiers (architecture 1)

Drawn 2026-10-20 from seed ET41's number, re-worlded at the draw (see Tried and rejected).

## Draw

- **Pairing.** Client domain survey-research-official-statistics (house domain demographic-social-science, housing),
  task type census-register-administrative-data-quality, objective Data Extraction & Conformation (ETL): the 2020
  census base, the cities' certificate-of-occupancy exports from their own permit systems, demolition records, the
  ACS occupancy rates, the group quarters survey and an electric utility's residential account history are conformed
  into one housing-unit-method population estimate per city.
- **Decision.** How many, and which, of the state's cities near the line stand at 50,000 residents or more on
  1 April 2026, and so move into the upper tier of the 2027 municipal revenue-sharing formula. Forward facing: the
  tiers fund 2027.
- **The quantity.** Each city's household population (occupied housing units times persons per household) plus
  its group quarters residents on 1 April 2026.
- **Data-native sentence.** Apartment buildings completed in the last two years fill over a year or more after they
  open, so the city's stock occupancy rate, applied to every housing unit, counts as households the units still
  standing empty, most in the cities that built most; the utility's account history, which covers only the cities in
  its territory, records month by month how earlier buildings filled after opening.
- **Default path.** The housing unit method with each city's ACS occupancy on every unit.
- **Golden.** The same for the stock; the units completed since the start of 2024 at the occupancy the lease-up
  record gives for their months since completion.
- **Guard.** WARN (objective and Gate G overuse); nearest task43 at 0.06; personas Kimberly Rogers and Martin Booth
  from guard.py names; off the seasonal-adjustment subdomain and composition_mix (lane reservations).

## Tried and rejected

- 2026-10-20, at the draw: ET41's own world, broadband grant allocation from the FCC map: served, underserved,
  reliable technology, enforceable commitments and the location fabric are filed BEAD definitions and the base is a
  recorded count, so every lever was a filed definition, a fabric clean-up (Layer 1) or maturity of pending
  challenges; re-worlded.
