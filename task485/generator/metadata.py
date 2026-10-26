"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
PO = "Population Office, Cabinet Office, Esklett"
ESU = "Esklett Statistics Unit"
SOURCES = {
    "population_register_extract_20260930.csv": (PO + ", Population Register current system, extract of 30 September "
                                                 "2026 for the Statistics Unit", "2026-09-30"),
    "population_register_legacy_archive_2014_2023.csv": (PO + ", legacy register archive, records from 1 January 2014 "
                                                         "to 12 March 2023", "2026-09-30"),
    "registration_number_crosswalk_2023.csv": (PO + ", registration numbers issued at the move to the current system",
                                               "2023-03-13"),
    "sector_classification_2026.json": (ESU + ", employment sector classification, 2026 edition", "2025-11-14"),
    "parish_codes.csv": (PO + ", parish codes", "2025-04-01"),
    "population_policy_2024_2028_sector_allowances.pdf": ("Cabinet Office, Population Policy Unit, Population Policy "
                                                          "2024 to 2028: sector allowances and work permit quotas",
                                                          "2024-04-09"),
    "long_term_migration_methods_2026.pdf": (ESU + ", methods note for long-term migration statistics, 2026 edition",
                                             "2026-09-01"),
    "population_register_extract_specification.pdf": (PO + ", extract specification for the Statistics Unit, version 3",
                                                      "2026-09-01"),
    "long_term_immigration_by_sector_2023_24.xlsx": (ESU + ", Population and Migration Statistics, Table 1, published "
                                                     "16 October 2025", "2025-10-16"),
    "port_passenger_movements_2024_2026.xlsx": ("Esklett Ports Authority, monthly passenger movements by port",
                                                "2026-09-09"),
    "census_2021_population_by_parish.xlsx": (ESU + ", Census 2021 table CT03, usual residents by parish and country "
                                              "of birth", "2022-06-29"),
}
DISTRACTORS = ["target/port_passenger_movements_2024_2026.xlsx", "target/census_2021_population_by_parish.xlsx"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task485", title="Esklett's provisional long-term immigration by employment sector, 2025-26, "
                                      "against the Population Policy's allowances",
                setting="A fictional self-governing island in the Irish Sea, Esklett, with a Population Register kept "
                        "in two systems either side of a 2023 move and a Population Policy that sets each employment "
                        "sector an allowance of long-term immigration: the island, its parishes, its bodies and its "
                        "people are fictional, and every record is synthetic.",
                as_of="2026-10-07",
                deliverables=["provisional_long_term_immigration_2025_26.xlsx",
                              "long_term_immigration_by_sector_2025_26.png"],
                distractor_files=DISTRACTORS, stated_inputs=["31 August 2026 cut", "year to 30 June 2026",
                                                             "nearest 50"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
