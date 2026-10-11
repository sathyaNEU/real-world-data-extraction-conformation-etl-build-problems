

## Solver's-eye read

Pass 1: one isolated reader on Sonnet, 2026-10-11, relaunched after a session restart.

1. **none.** The nearest is MG-02 4.1, "A decline with another cause is not the mine's." It restates the prompt's
   "decline the mine's take has caused". No file says how to separate the mine's share from the rainfall response,
   or that the coal measures lag rainfall by years.
2. **none.** The register "holds no current water levels and no assessment results", and no file ranks the bores or
   states a level, change, decline or yes/no.
   - The coordinates allow only a proximity guess.
   - The five bores nearest the mine-bore ring (LB12, LB04, LB05, LB07, LB10) are the five its rough model finds
     impaired.
3. **`monitoring_network_notes.md`**, "the only file that exists to brief the analyst". It carries the field
   dictionary, the ft/m rule, the pump-off rule, the pressure-to-level recipe and the two measuring-point changes.
4. **none.** The nearest is "pump lowered by the landholder's contractor in July" (contact log, Saltbush Flat,
   6 Aug), the kind of line a real log carries.

**Plan (summarised).**
- Clean the site spellings and the feet rounds, and drop pumped dips.
- Take levels from the measuring point in force on the day, and compensate the loggers hour by hour in Queensland
  days.
- Fit each bore's record before dewatering (to June 2022) to a lagged, smoothed rainfall departure, and take
  modelled minus observed as the mine's decline. Check it on the reference bores and LB16.
- Its rough run:
  - 6.5 to 7.9 m at LB04, LB05, LB07 and LB10;
  - 3.6 to 4.0 m at LB12;
  - 0 to 1.6 m elsewhere.
- The raw change since baseline flags a different eight.

**REVIEW lines: all six harmless.**
- 2.4 and 1.1 in MG-02 are clause numbers.
- The kPa readings coincide with levels by chance, among about 1M rows.
- MG-02 and the notes use their own procedure and network vocabulary and never name the counterfactual.
- The register and the contact log hold inputs and complaints, and rank nothing.

**Realism notes (deferred to stage 6b or the hardening brief).**
- **Loggers:**
  - the MB03 logger is typed 0-300 kPa but reads up to 589.7;
  - logger temperatures are constant (25.40 and 25.70 C) and logger levels show no drift;
  - there is one outage only;
  - an LB05 battery comment is contradicted by the data.
- **Dips:**
  - feet rounds in 2012;
  - remarks drawn from a short fixed list ("windmill turning" on bores without a windmill).
- **Water quality:** sample_ids climb in steps of 7, there are no non-detects, and nothing moves at the pit bores.
- **Dewatering:** the meters have no outages, and AD03 and AD04 start later than the notes say.
- **Contact log:**
  - entries on weekends;
  - lines repeated verbatim;
  - a count of complainants that runs ahead of the log;
  - a dip the dips file does not hold.
- **MG-02:** effective on a Sunday, with a 08:30:00 creation stamp and no Water Act references.
- **Workbooks:** openpyxl signatures under an app.xml that says Excel, and a line in the register saying what it
  lacks.
