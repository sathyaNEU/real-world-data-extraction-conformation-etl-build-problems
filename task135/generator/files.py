"""The pack's data frames, and the writing of every file under target/."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import world as W
import book as BK
import observe as O
import docs as D
import grants as GR
import asks as A

FILES = {
    "val": "brackenfold_valuation_lots_2024-11_2026-11.csv",
    "moves": "brackenfold_capital_movements_2024-12_2026-11.csv",
    "events": "brackenfold_corporate_events_2024-12_2026-11.csv",
    "ent": "brackenfold_income_entitlements_by_lot_2025-11_2026-11.csv",
    "static": "brackenfold_static_data_2026-12-02.csv",
    "notes": "brackenfold_export_notes_2026-12-02.txt",
    "kest": "kestwick_charity_funds_prices_2024-11_2026-11.xlsx",
    "keyfacts": "kestwick_charity_funds_key_facts_2026.pdf",
    "cal": "market_calendars_2024-2027.csv",
    "policy": "wrexford_investment_policy_2025-12.pdf",
    "proc": "wrexford_finance_procedure_07_budget_2026-10.docx",
    "budget": "wrexford_budget_2027_draft_2026-11-24.xlsx",
    "reg": "wrexford_grants_register_2026-11-30.csv",
    "inst": "wrexford_grant_instalments_2026-11-30.csv",
    "pays": "wrexford_grant_payments_2023-01_2026-11.csv",
    "index": "benchmark_index_levels_2024-11_2026-11.csv",
    "factsheets": "kestwick_factsheets_2026-10.pdf",
    "fernside": "fernside_quarterly_report_2026-q3.pdf",
}
DISTRACTORS = ["index", "factsheets", "fernside"]
UK = "%d/%m/%Y"


def grant_frames(grants, inst, pays, seed):
    rng = np.random.default_rng(seed + 9)
    reg = pd.DataFrame([(g["ref"], g["grantee"], g["programme"], g["type"], g["award"].strftime(UK), g["currency"],
                         g["amount"], g["status"], g["status_date"].strftime(UK)) for g in grants],
                       columns=["grant_ref", "grantee", "programme", "grant_type", "award_date", "currency",
                                "award_amount", "status", "status_date"])
    ins = pd.DataFrame([(i["ref"], i["no"], i["due"].strftime(UK), i["amount"], i["status"]) for i in inst],
                       columns=["grant_ref", "instalment_no", "due_date", "amount", "status"])
    cur = {g["ref"]: g["currency"] for g in grants}
    rows = []
    no = 600_000 + int(rng.integers(1000, 5000))
    for i in sorted(pays, key=lambda i: (i["paid"], i["ref"], i["no"])):
        if i["paid"] < dt.date(2023, 1, 1):
            continue
        no += int(rng.integers(1, 30))
        c = cur[i["ref"]]
        rate = float(rng.uniform(1.135, 1.195)) if c == "EUR" else 1.0
        rows.append(("FP%07d" % no, i["paid"].isoformat(), i["ref"], i["no"], c, "%.2f" % i["amount"],
                     "%.2f" % (i["amount"] / rate)))
    pay = pd.DataFrame(rows, columns=["payment_ref", "payment_date", "grant_ref", "instalment_no", "currency", "amount",
                                      "amount_gbp"])
    return reg, ins, pay


def frames(M, fp, B, grants, inst, pays, gseed):
    F = {}
    F["val"] = O.valuation(B)
    F["moves"] = O.movements(B)
    F["events"] = O.corporate_events(B)
    F["ent"] = O.entitlements(B, M)
    F["static"] = O.static(B)
    F["kest"] = O.kestwick_history(B, M)
    F["cal"] = O.calendars()
    F["index"] = O.index_levels(M)
    F["reg"], F["inst"], F["pays"] = grant_frames(grants, inst, pays, gseed)
    return F


def pack_for_asks(F, running, capital, kest_isins=None):
    v = F["val"]
    last = v[v["valuation_date"] == W.VAL_DATE.isoformat()]
    kest = {}
    for f, df in F["kest"].items():
        d = df.copy()
        d["Date"] = [x if isinstance(x, dt.date) and not isinstance(x, dt.datetime) else x.date() for x in d["Date"]]
        kest[f] = d
    return A.Pack(val=last, ent=F["ent"], static=F["static"], kest=kest,
                  kest_isins=kest_isins or {f: (W.FUNDS[f]["isin_inc"], W.FUNDS[f]["isin_acc"]) for f in W.FUNDS},
                  reg=F["reg"], inst=F["inst"], pays=F["pays"], running=running, capital=capital)


def write_csv(df, path, head=None):
    """a CSV as the system exports it; `head` is the header block a report writes above its column row"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        for line in head or []:
            f.write(line + "\n")
        df.to_csv(f, index=False, lineterminator="\n")
