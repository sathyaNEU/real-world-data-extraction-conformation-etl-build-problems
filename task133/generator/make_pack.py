"""Writes the whole of target/ for task133 architecture 3 into a directory."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import docs  # noqa: E402
import pack  # noqa: E402
import pack_asks  # noqa: E402
import world  # noqa: E402
from io_util import set_mtime  # noqa: E402

FILES = [
    docs.STANDARD, docs.SCENARIO,
    "business_lending_book_2026-09-30.csv",
    "operating_account_credits_2025-10_to_2026-09.csv",
    "nzbn_extract_canterbury_otago_southland_2026-10-12.csv",
    "industry_sales_quarterly_south_island_2021Q4-2026Q3.csv",
    "write_offs_2023-10_to_2026-09.csv", "collections_cases_open_2026-09-30.csv", "collections_receipts_FY2026.xlsx",
    "guarantees_register_2026-09-30.csv", "security_realisations_settled_FY2026.csv",
    "customer_master_extract_2026-10-09.csv", "risk_grade_snapshot_2025-09-30.csv", "grade_overrides_2024-2026.xlsx",
    "default_register_business_FY2026.csv", "default_register_rural_FY2026.csv", "connected_groups_2026-09-30.csv",
    "customer_merge_log_2026-03-14.csv",
    docs.RURAL_PDF, docs.DEPOSITS,
]
DISTRACTORS = ["industry_sales_quarterly_south_island_2021Q4-2026Q3.csv", docs.RURAL_PDF, docs.DEPOSITS]


def make(out):
    os.makedirs(out, exist_ok=True)
    W = world.make()
    pack.write_register(W, out)
    pack.write_lending_book(W, out)
    pack.write_credits(W, out)
    pack.write_industry_series(W, out)
    pack_asks.write_loss_files(W, out)
    pack_asks.write_customer_master(W, out)
    pack_asks.write_backtest_files(W, out)
    docs.write_standard(out)
    docs.write_scenario(out)
    docs.write_rural_pdf(out)
    docs.write_deposits(W, out)
    present = sorted(os.listdir(out))
    assert sorted(FILES) == present, (sorted(set(FILES) ^ set(present)))
    for f in present:
        set_mtime(os.path.join(out, f))
    return W


if __name__ == "__main__":
    make(sys.argv[1])
