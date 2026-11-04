"""submission.md from generator/figures.json: tags, the call, the critical components, the steps and the deliverable
answers, every figure taken from the file the generator wrote."""
import json

MONTH = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]


def n(v):
    return "{:,}".format(v)


def day(iso):
    y, m, d = iso.split("-")
    return "%d %s" % (int(d), MONTH[int(m) - 1])


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    c, r = f["call"], f["rungs"]
    piles = f["piles"]
    bases = ", ".join("%s %s" % (p["area"], day(p["base_survey"])) for p in piles)
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** General statistics and data science (data integration, record linkage and entity resolution), "
      "for a utility's fuel stock (house domain: business and operations analytics).")
    w("**Analytical objective:** Data extraction and conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Do not nominate Silesia's winter option cargo: the coal yard held %s t at the 16 December survey, %d days of "
      "the first-quarter burn plan against the %d-day floor.** The reserve clears the floor by %s t. Not the base "
      "through each pile's toe, which files %s t (%d days) because the pad has settled into bowls under the five "
      "long-standing pile areas and a toe base leaves the coal in them out; not the lowest point around each pile, "
      "%s t (%d days), short for the same reason."
      % (n(c["reserve"]), c["cover_days"], c["floor_days"], n(c["margin_t"]), n(r["toe_plane"]["reserve"]),
         r["toe_plane"]["cover"], n(r["toe_low"]["reserve"]), r["toe_low"]["cover"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Each pile area's pad is the surface the 2026 surveys recorded with the area bare, not a plane through the "
      "toe: %s." % bases)
    w("2. The reserve is **%s t**." % n(c["reserve"]))
    w("3. The planned burn is **%s t a day** (%s t over %d days)." % (n(c["planned_burn"]), n(c["plan_total"]),
                                                                       c["plan_days"]))
    w("4. Days of cover: **%d**, %s t above the floor of %s t." % (c["cover_days"], n(c["margin_t"]),
                                                                    n(c["floor_t"])))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took every survey onto the 16 December 2026 survey's points with survey_control_report_2026-07.pdf (the "
      "plant grid's rotation and offset, N2000 = N60 + %s m) and gave each point to its pile area in "
      "coalyard_pile_areas.csv, each area to half the gap to the next." % f["cited"]["datum_m"])
    w("2. For each area took as its pad the latest survey before December in which the area was bare (%s), up to "
      "about two metres below the pile's toe under the long-standing areas." % bases)
    w("3. Multiplied each area's volume above that pad by the latest fuel_lab_density_tests.csv density before the "
      "survey (PR-07 3.2) and summed: %s t." % n(c["reserve"]))
    w("4. Divided by the plan's %s t over %d days in coal_burn_plan_2027Q1.xlsx (PR-07 3.3): %d days, %s t above the "
      "%d-day floor, so no nomination (PR-07 5)." % (n(c["plan_total"]), c["plan_days"], c["cover_days"],
                                                     n(c["margin_t"]), c["floor_days"]))
    w("5. Receipts (OH-12 1.1): each call's CV-01 intervals while gu1_unloader_events.csv shows GU-1 running, between "
      "the two December flights, plus each historian catch-up whose link fell while that call discharged, by "
      "coal_contracts.csv: %s." % "; ".join("%s %s t" % (k, n(v)) for k, v in f["ask_a"].items()))
    w("6. Deliveries (OH-12 1.2, 2.1): CV-21 between the shift log's readings at 00:00 on each quarter's first day "
      "(the June integrator restart bridged), less the CV-21 blocks run while CV-01 carried coal with GU-1 stopped "
      "(the crossover): %s." % "; ".join("%s %s t" % (k, n(v)) for k, v in f["ask_b"].items()))
    w("7. Let the winter option lapse: %s t and %d days against the %d-day floor." % (n(c["reserve"]),
                                                                                     c["cover_days"], c["floor_days"]))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### coal_reserve_2026.xlsx")
    w("")
    w("1. Each pile area at the 16 December 2026 survey, volume to the nearest 1,000 m3 and tonnes to the nearest "
      "1,000:")
    for p in piles:
        w("   - %s (%s): %s m3, %s t" % (p["area"], p["coal"], n(p["volume_m3"]), n(p["tonnes"])))
    w("2. Reserve: %s t" % n(c["reserve"]))
    w("3. Days of cover: %d" % c["cover_days"])
    w("4. Call: do not nominate the winter option cargo; it lapses on 8 January 2027")
    w("5. Coal received into the yard between the December 2025 and December 2026 surveys:")
    for k, v in f["ask_a"].items():
        w("   - %s: %s t" % (k, n(v)))
    w("6. Coal sent to the boiler house in 2026:")
    for k, v in f["ask_b"].items():
        w("   - %s: %s t" % (k, n(v)))
    w("")
    w("### coalyard_stock_2026.svg")
    w("")
    w("1. Line chart of the coal in the yard at every survey from 17 December 2025 to 16 December 2026, with the "
      "%d-day floor (%s t) drawn across it and the December 2026 point at %s t, %d days." % (
          c["floor_days"], n(c["floor_t"]), n(c["reserve"]), c["cover_days"]))
    with open(out_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
