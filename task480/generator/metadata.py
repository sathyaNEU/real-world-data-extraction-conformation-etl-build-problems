"""metadata.json: every shipped file with its source, date and licence, the distractors and why the solution leaves
them unused, and the deliverables."""
import json

import world as W

DATES = {"registrations": "2026-07-06", "inspections": "2026-01-12", "stations": "2026-06-30", "rates": "2026-04-15",
         "guidelines": "2026-09-08", "counties": "2026-07-06", "body": "2026-07-06", "vouchers": "2026-01-20",
         "invoices": "2026-01-16", "closeout": "2026-02-10", "annual": "2025-03-20", "dictionary": "2026-09-14",
         "hpms": "2026-06-12", "fuel": "2026-04-03", "population": "2025-12-18"}
SOURCE = {"registrations": W.DMV, "inspections": W.EIP, "stations": W.EIP, "rates": W.SECTION,
          "guidelines": W.SECTION, "counties": W.DMV, "body": W.DMV, "vouchers": "%s program office" % W.PROGRAM,
          "invoices": "the 2025 pilot's three licensed dismantlers", "closeout": W.SECTION, "annual": W.SECTION,
          "dictionary": W.SECTION, "hpms": "State %s" % W.DOT, "fuel": "State Department of Revenue",
          "population": "State Demographer"}


def write(path, n):
    files = [dict(file=fn, source="%s (fictional), synthetic records" % SOURCE[k], date=DATES[k],
                  license="CC0-1.0 (synthetic, generated for this task)", rows=n.get(k))
             for k, fn in sorted(W.FILES.items(), key=lambda t: t[1])]
    why = {
        "dot_county_vmt_2025.csv": "road miles counted on each county's roads by every vehicle including through "
                                   "traffic; guidelines 3.3 judges each vehicle's 2027 miles on its own odometer reading",
        "gasoline_sales_by_county_2025.csv": "gallons sold by county of sale, every vehicle that fuels there; not a "
                                             "vehicle's miles, which 3.3 takes from its own reading",
        "county_population_estimates_2025.csv": "residents and households; the eligible fleet is the registration "
                                                "snapshot's ACTIVE records (2.1)",
        "eip_station_register_2026-06-30.xlsx": "where intake desks could sit (guidelines 5); a county's NOx rests on its "
                                                "vehicles' own readings wherever they were tested (3.3)"}
    meta = dict(task="task480", title="%s: the 2027 %s intake counties" % (W.AREA, W.PROGRAM),
                setting="A fictional state environmental quality department's mobile sources section, a fictional "
                        "twelve-county ozone nonattainment area and its first biennial inspection cycle; every "
                        "record is synthetic.",
                as_of="2026-10-26", files=files,
                distractors=[dict(file=f, why=why[f]) for f in W.DISTRACTORS],
                deliverables=[W.GOLDEN["workbook"], W.GOLDEN["memo"]])
    json.dump(meta, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
