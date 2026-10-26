"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "paye_returns_m12_2021-22.csv": ("Revenue Office, PAYE employer extract, tax month 12 of 2021-22, layout version 3", "2022-05-16"),
    "paye_returns_m12_2025-26.csv": ("Revenue Office, PAYE employer extract, tax month 12 of 2025-26, layout version 4", "2026-05-18"),
    "paye_extract_specification_v4.pdf": ("Revenue Office, Statistics and Data Sharing, PAYE employer extract specification, version 4", "2026-05-11"),
    "rating_list_2017_extract_20220404.csv": ("Torvasay Valuation Office, 2017 rating list extract", "2022-04-04"),
    "rating_list_2023_extract_20260413.csv": ("Torvasay Valuation Office, 2023 rating list extract", "2026-04-13"),
    "valuation_description_codes.json": ("Torvasay Valuation Office, primary description codes", "2023-02-14"),
    "rating_list_extract_guide.pdf": ("Torvasay Valuation Office, rating list extracts field guide", "2026-04-13"),
    "business_rates_accounts_2017-2026.xlsx": ("The six district councils' business rates accounts with a liability, April 2017 to April 2026, as supplied to Torvasay Statistics", "2026-05-12"),
    "companies_register_extract_20260501.csv": ("Torvasay Companies Registry, register extract", "2026-05-01"),
    "town_centre_schedule_2026.csv": ("Department for the Economy, Town Centres Unit, postcode schedule of the designated town centres", "2026-08-20"),
    "town_centre_renewal_fund_2027_prospectus.pdf": ("Department for the Economy, Town Centre Renewal Fund 2027 prospectus", "2026-09-07"),
    "sic2007_subclasses.csv": ("Torvasay Statistics, SIC 2007 subclasses in use in the extracts", "2026-05-20"),
    "town_centre_footfall_daily_2021-2026.csv": ("Department for the Economy, Town Centres Unit, footfall counters, daily counts", "2026-04-06"),
    "labour_force_survey_employment_by_industry_2022_2026.xlsx": ("Torvasay Statistics, Labour Force Survey, residents in employment by industry and district", "2026-06-11"),
}
DISTRACTORS = ["target/town_centre_footfall_daily_2021-2026.csv",
               "target/labour_force_survey_employment_by_industry_2022_2026.xlsx"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task486", title="The 2027 Town Centre Renewal Fund: which designated town centres qualify",
                setting="A fictional self-governing island nation, Torvasay, whose statistics office compiles each designated "
                        "town centre's workplace retail employment from the tax authority's PAYE returns, the valuation "
                        "office's rating lists and the district councils' business rates accounts: the island, its bodies, "
                        "the firms and the people are fictional, and every record is synthetic.",
                as_of="2026-10-29",
                deliverables=["town_centre_fund_2027_eligibility.xlsx", "town_centre_retail_employment_2022_2026.png"],
                distractor_files=DISTRACTORS, stated_inputs=["8 per cent", "March 2022 and March 2026"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
