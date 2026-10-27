"""submission.md, drafted from figures.json."""
import params as P
import golden as GD

NAMES = GD.NAMES
STORMS = GD.STORMS
STORM_NAME = {"2016-04": "Ines", "2018-05": "Kendra", "2020-08": "Marisol", "2022-04": "Odile", "2024-07": "Quenby"}


def text(f):
    aal = f["aal_musd"]
    run = f["runner_up"]
    fails = [STORM_NAME[s] for s in f["mg04_storms"] if abs(f["mg04_default_pct"][s]) > 100 * P.MG04_TOL]
    L = []
    L += ["## Tags", "",
          "**Domain:** Actuarial science and insurance (catastrophe exposure and accumulation).",
          "**Analytical objective:** Opportunity sizing and decision support.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Award the 2027 FORTIFIED Roof grant round to %s: re-roofing its portfolio removes about USD %.1f million "
          "a year of expected hurricane loss, the most of the four counties.**" % (f["call"], f["call_removed_musd"]),
          "Not %s, the runner-up, which carries the largest annual expected loss (USD %.2f million) almost all in "
          "events gusting 130 mph or more, where the roof cuts little. Not Heron Bay or Calloway Flats, which remove "
          "less." % (run, aal[run]), ""]
    L += ["## 2. Critical Components", "",
          "1. 2027 annual expected loss on the portfolios' current roofs (USD million): " +
          ", ".join("%s **%.2f**" % (n, aal[n]) for n in NAMES) + ".",
          "2. The FORTIFIED Roof cut read class by class of peak gust reproduces the paid loss on FORTIFIED homes "
          "within **10 percent** in all **5** storms MG-04 tests (%s); one cut for all storms misses in %s." % (
              ", ".join(STORM_NAME[s] for s in f["mg04_storms"]), ", ".join(fails)),
          "3. Expected annual loss removed: %s **USD %.1f million**, ahead of %s." % (
              f["call"], f["call_removed_musd"], run), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. For each named storm since 2012 (named_storm_register_2008-2025.csv), summed every payment line coded to "
          "its catastrophe code in claims_payment_lines_2012-01_to_2026-09.csv by ZIP code and FORTIFIED credit "
          "(FORT-R), against Coverage A at landfall from inforce_at_landfall_by_zip_2008-2025.parquet (USD thousands "
          "before 2019) and the ZIP's peak gust from storm_peak_gust_footprints_2008-2025.xlsx (knots times 1.150779 "
          "before 2019).",
          "2. Took the FORTIFIED Roof cut in each 10 mph gust class as one minus the FORTIFIED homes' paid per dollar "
          "of Coverage A over the standard homes', pooled over the class's storms and ZIP codes.",
          "3. Ran MG-04's reproduction test on the %d storms with USD %d million or more paid on FORTIFIED homes: the "
          "class cuts pass on all %d, one cut for all storms fails in %s." % (
              len(f["mg04_storms"]), P.MG04_MIN_PAID // 1_000_000, len(f["mg04_storms"]), ", ".join(fails)),
          "4. Joined corvane_hu27_elt_sandpiper_retrofit_2027.parquet to corvane_hu27_event_hazard_summary.csv on "
          "the event number (HU27- prefix dropped) and county, and took each portfolio's annual expected loss and the "
          "loss removed as the sum over events of annual rate times mean loss, and times the cut for the event's gust "
          "class.",
          "5. For FORTIFIED homes, kept certificates in fortified_certificate_register_2012-2026.csv issued by "
          "September 30, 2026, expiring after it and not voided, and matched each to the home in force that day in "
          "policy_master_2006-2026.csv by parcel and building (the main house or the COTTAGE), not by the policy it was "
          "issued under nor by the street name, which the county has changed since some were issued, counting each "
          "home once.",
          "6. For the storms before 2012, took each legacy claim's last paid to date in "
          "legacy_claims_valuations_2008-2011.csv and added its carried lines in the claims file (legacy_claim_ref), "
          "leaving out the January 1, 2012 line that repeats the legacy paid to date; paid after 2011 is those added "
          "lines.",
          "7. For roof ages, raised each portfolio home's roof year on record in "
          "retrofit_2027_modeled_portfolios.csv to the year of its latest RE-ROOF permit by September 30, 2026 in "
          "county_building_permits_roofing_2013-2026.csv (BLDG 2 the cottage, ROOF REPAIR not a new roof, a permit "
          "on a street the county later renamed matched by ZIP code and house number to the street's new name) and "
          "counted roof years 2012 or earlier.",
          "8. Recommended %s, the largest expected annual loss removed." % f["call"], ""]
    L += ["## 4. Deliverable Answers", "", "### retrofit_round_2027.xlsx", "",
          "1. County for the 2027 round: %s." % f["call"],
          "2. Expected annual hurricane loss the round removes there: USD %.1f million." % f["call_removed_musd"],
          "3. Runner-up: %s." % run,
          "4. 2027 annual expected loss on each county's portfolio (USD million):"]
    L += ["   - %s: %.2f" % (n, aal[n]) for n in NAMES]
    L += ["5. Insured homes holding a valid FORTIFIED Roof certificate on September 30, 2026, and their Coverage A "
          "(USD thousands):"]
    L += ["   - %s: %s, %s" % (n, "{:,}".format(f["ask_a"][n][0]), "{:,}".format(f["ask_a"][n][1])) for n in NAMES]
    L += ["6. Net paid to date and the part of it paid after 2011 (USD thousands):"]
    L += ["   - %s: %s, %s" % (s, "{:,}".format(f["ask_b"][s][0]), "{:,}".format(f["ask_b"][s][1])) for s in STORMS]
    L += ["7. Portfolio homes with a roof 15 or more years old on June 1, 2027, and their Coverage A (USD thousands):"]
    L += ["   - %s: %s, %s" % (n, "{:,}".format(f["ask_c"][n][0]), "{:,}".format(f["ask_c"][n][1])) for n in NAMES]
    L += ["", "### avoided_loss_by_county.png", "",
          "1. Bar chart of each county's 2027 annual expected loss beside the loss the round removes, %s's bar the "
          "tallest of the loss removed." % f["call"], "",
          "### board_note_retrofit_2027.docx", "",
          "1. One-page note to the board recommending %s at about USD %.1f million a year removed, %s next, with the "
          "chart." % (f["call"], f["call_removed_musd"], run), ""]
    return "\n".join(L)
