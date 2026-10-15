"""task143 constants and helpers shared by every generator module.

Kalvenhorst Systeme GmbH (Bielefeld) builds business and rugged notebooks and assembles their battery packs in its own
battery plant from pouch cells bought from Zelvora Cell s.r.o. (Ostrava). The battery reliability lab releases each
Zelvora lot on a 100-cycle release test of 20 formation trays; the release model of record (RL-3, memo QM-07) predicts
each test cell's cycles to 80 per cent of rated capacity; product finance books the lot's Model K warranty reserve on
release day under FIN-RS-04. Lot ZC2638 is released on Friday 16 October 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1430915

# ---------------------------------------------------------------------------------------------------- the product
RATED_MAH = 4820            # ZP-4820 cell and Model K pack rated capacity
EOL_FRACTION = 0.80
EOL_MAH = RATED_MAH * EOL_FRACTION   # 3,856 mAh
WARRANTY_CYCLES = 600
PACK_CELLS = 3              # Model K: 3S1P
TRAY_CELLS = 6              # a Zelvora formation tray
TEST_TRAYS = 20             # trays in a release test
MODEL_K_PACKS = 7200        # the lot under release

# ---------------------------------------------------------------------------------------------------- lots
def _monday(y, m, d):
    return dt.date(y, m, d)


# formation Mondays: one lot a month, coded by the ISO year and week of the formation week
LOT_STARTS = [
    _monday(2024, 9, 9), _monday(2024, 10, 7), _monday(2024, 11, 4), _monday(2024, 12, 2),
    _monday(2025, 1, 6), _monday(2025, 2, 3), _monday(2025, 3, 3), _monday(2025, 3, 31),
    _monday(2025, 5, 5), _monday(2025, 6, 2), _monday(2025, 7, 7), _monday(2025, 8, 4),
    _monday(2025, 9, 1), _monday(2025, 10, 6), _monday(2025, 11, 3), _monday(2025, 12, 1),
    _monday(2026, 1, 5), _monday(2026, 2, 2), _monday(2026, 3, 2), _monday(2026, 3, 30),
    _monday(2026, 5, 4), _monday(2026, 6, 1), _monday(2026, 7, 6), _monday(2026, 8, 3),
    _monday(2026, 9, 14),
]


def lot_code(d):
    iy, iw, _ = d.isocalendar()
    return "ZC%02d%02d" % (iy % 100, iw)


LOTS = [lot_code(d) for d in LOT_STARTS]
LOT_START = dict(zip(LOTS, LOT_STARTS))
NEW_LOT = LOTS[-1]                     # ZC2638, the lot under release
TRAIN_LOTS = LOTS[:20]                 # every qualification cell has finished its life test
OPEN_LOTS = LOTS[20:24]                # life tests still running at the pull
ASK_LOTS = LOTS[:12]                   # released October 2024 to September 2025
TRAY_KEY_CHANGE = "ZC2532"             # Zelvora's data package writes tray keys in the new form from this lot

# ---------------------------------------------------------------------------------------------------- calendar
RELEASE_DAY = dt.date(2026, 10, 16)    # the lot under release is released and the reserve booked (a Friday)
LAB_PULL = dt.date(2026, 10, 12)       # the lab, supplier and genealogy extracts
SERVICE_END = dt.date(2026, 9, 30)     # the service and invoice extracts run to the end of this day
SERVICE_PULL = dt.date(2026, 10, 5)
COST_FROM = dt.date(2025, 10, 1)       # Ask B: the twelve months to 30 September 2026
MIGRATION = dt.date(2026, 3, 2)        # the depot's service orders moved onto the service case system
MODEL_FIT = dt.date(2026, 9, 30)       # RL-3 refitted on the twenty finished lots


def lot_release(lot):
    """Release Friday of a lot: the fifth Friday after its formation Monday (the release test finishes in between)."""
    return LOT_START[lot] + dt.timedelta(days=32)


# ---------------------------------------------------------------------------------------------------- the pack
F_POLICY = "fin_rs04_battery_warranty_reserve_policy.pdf"
F_MEMO = "qm07_release_model_rl3_zp4820.pdf"
F_SPEC = "model_k_pack_specification_rev_d.pdf"
F_README = "extract_note_battery_lab_2026-10-12.txt"
F_README_SVC = "extract_note_service_operations_2026-10-09.txt"
F_CYC_A = "qp3_first100_cycles_fleet_a.csv"
F_CYC_B = "qp3_first100_cycles_fleet_b.csv"
F_LIFE = "qp3_life_monitoring_results.csv"
F_REG = "qp3_release_register.csv"
F_CELLS = "zelvora_cell_data_zc2638.csv"
F_GEN = "model_k_genealogy_zc2638.csv"
F_CASES = "service_cases_2024-09_2026-09.csv"
F_SAP = "depot_service_orders_2024-09_2026-03.xlsx"
F_RETURNS = "depot_returns_log_2024-09_2026-09.xlsx"
F_FX = "treasury_month_end_rates_2025-2026.csv"
F_CARRIER = "carrier_statement_inbound_returns_2025-09_2026-10.csv"
F_COST = "service_cost_sheet_fy2026.xlsx"
F_INV = {"FRB": "invoices_dauvergne_frb_2025-09_2026-09.xlsx",
         "UKI": "invoices_tolley_marsh_uki_2025-09_2026-09.xlsx",
         "NOR": "invoices_ljungqvist_nor_2025-09_2026-09.xlsx",
         "SOU": "invoices_ferrucci_sou_2025-09_2026-09.xlsx"}
F_MODEL_J = "model_j_genealogy_zc2638.csv"
F_COA = "zelvora_certificate_of_analysis_zc2638.pdf"
DISTRACTORS = [F_MODEL_J, F_COA]

GOLD_BOOK = "z2638_warranty_reserve.xlsx"
GOLD_NOTE = "z2638_reserve_note.docx"

COMPANY = "Kalvenhorst Systeme GmbH"
SUPPLIER = "Zelvora Cell s.r.o."
PEOPLE = {
    "controller": "Christiana Harloff",   # product finance controller, notebook division (requester; not in the prompt)
    "lab": "Frieder Henschel",            # head of the battery reliability lab, author of QM-07
    "mfg": "Dietmar Schaaf",              # manufacturing engineering, battery plant (genealogy)
    "service": "Annelie Geisel",          # service operations analyst (service case system)
}

REGIONS = ["DACH", "FRB", "UKI", "NOR", "SOU"]
REGION_NAME = {"DACH": "Germany, Austria and Switzerland", "FRB": "France and Benelux", "UKI": "UK and Ireland",
               "NOR": "Nordics", "SOU": "Southern Europe"}


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def write_csv(path, cols, rows, crlf=False, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delimiter)
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round_dp(x, dp):
    f = 10 ** dp
    return math.floor(x * f + 0.5) / f if x >= 0 else -math.floor(-x * f + 0.5) / f


# ---------------------------------------------------------------------------------------------------- central European time
def _last_sunday(y, month):
    d = dt.date(y, month, 31 if month in (3, 10) else 30)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def cet_offset(t_utc):
    """Hours to add to UTC for Bielefeld wall time: CEST (+2) from the last Sunday of March 01:00 UTC to the last Sunday
    of October 01:00 UTC, CET (+1) otherwise."""
    y = t_utc.year
    a = dt.datetime.combine(_last_sunday(y, 3), dt.time(1))
    b = dt.datetime.combine(_last_sunday(y, 10), dt.time(1))
    return 2 if a <= t_utc < b else 1


def utc_to_local(t_utc):
    return t_utc + dt.timedelta(hours=cet_offset(t_utc))
