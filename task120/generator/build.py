#!/usr/bin/env python3
"""task120 generator: builds target/ and metadata.json under an output root, deterministically,
and asserts the ladder, the corpus, the fork grid, the ask layer and the input gates.

    python3 task120/generator/build.py --out <root>        (root defaults to the task folder)

Everything the build asserts runs on the files as written, read back from disk, except the
world-level facts (the trust group, the conveyor, the twin) that only the generator can see.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import asks  # noqa: E402
import calib  # noqa: E402
import constructions as C  # noqa: E402
import docs  # noqa: E402
import shipped  # noqa: E402
import world as Wm  # noqa: E402
from common import Checks, EXPORT_DATE, YEARS, floor_conventions, round_thousand, stream, PCTS, k_top  # noqa: E402

REPO = HERE.parents[1]
TASK = HERE.parent
SCRUB = REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"

FILES = {
    "returns": "returns_processed_ty{y}.parquet",
    "sched": "dependents_schedule_ty{y}.parquet",
    "tables": "household_income_tables_ty{y}.xlsx",
    "method": "income_tax_tier_methodology.pdf",
    "layouts": "research_extract_record_layouts.txt",
    "intake": "intake_log.csv",
    "thread": "re_ty2025_tier_rebase.txt",
    "dept": "returns_processed_by_agi_class_ty2025.xlsx",
    "ledger": "estimated_payments_ledger_2025.parquet",
    "returned": "returned_items_2025.csv",
    "register": "tin_match_cases.csv",
    "schd": "schedule_d_extract_ty2025.csv",
    "amended": "amended_returns_log_ty2025.csv",
    "efile": "wage_statements_efile_ty2025.parquet",
    "paper": "w2_paper_keyed_ty2025.txt",
    "recon": "employer_reconciliations_ty2025.xlsx",
    "deposits": "withholding_deposits_2025.csv",
}
DISTRACTORS = [FILES["dept"], FILES["deposits"]]


def frames(W, years):
    R, S = {}, {}
    for y in years:
        R[y] = Wm.returns_frame(W, y)
        S[y] = Wm.schedule_frame(W, y, R[y])
    return R, S


def robust_2025(W):
    """Clear every unpinned construction's TY2025 floor off a half-thousand rounding edge."""
    y = 2025
    for _ in range(6):
        R, S = frames(W, (y,))
        bad = []
        for c in C.ALL_CONSTRUCTIONS:
            u = C.units(R[y], S[y], *c)
            for p in PCTS:
                fc = floor_conventions(u.agi.to_numpy(), p)
                vals = list(fc.values())
                if len({round_thousand(v) for v in vals}) > 1 or min(abs((v % 1000) - 500) for v in vals) < 70:
                    bad.append(int(round(np.median(vals) / 500.0)) * 500)
        if not bad:
            return R[y], S[y]
        for B in sorted(set(bad)):
            Wm.clear_rounding_edge(W, y, B)
    raise AssertionError("rounding edges did not clear")


def random_elections(r, y):
    """Credit elections on returns whose transfers fall outside the ledger's window: a share of
    higher-income resident returns, processed after the window closes."""
    rng = stream(f"elect{y}")
    r = r.copy()
    agi = r.federal_agi.to_numpy()
    p = np.interp(np.maximum(agi, 0), [0, 100_000, 300_000, 1_000_000], [0.004, 0.012, 0.05, 0.08])
    if y == 2025:
        p = np.where(r.processed_date.to_numpy() > np.datetime64("2026-01-31"), p, 0)
    pick = (rng.random(len(r)) < p) & (r.residency_code.to_numpy() == 1)
    amt = np.round(np.maximum(agi, 0) * rng.uniform(0.002, 0.012, len(r)) / 10) * 10
    r["overpayment_credit_elect"] = np.where(pick, np.maximum(amt, 50), 0).astype(np.int64)
    return r


# ------------------------------------------------------------------ writers

RET_SCHEMA = pa.schema([("return_id", pa.int64()), ("tax_year", pa.int16()), ("filer_tin", pa.int32()),
                        ("spouse_tin", pa.int32()), ("federal_primary_tin", pa.int32()), ("filing_status", pa.int8()),
                        ("residency_code", pa.int8()), ("county_code", pa.string()), ("federal_agi", pa.int32()),
                        ("state_taxable_income", pa.int32()), ("overpayment_credit_elect", pa.int32()),
                        ("processed_date", pa.date32())])
SCHED_SCHEMA = pa.schema([("claimant_return_id", pa.int64()), ("dependent_tin", pa.int32()),
                          ("relationship_code", pa.string()), ("dependent_birth_year", pa.int16())])
LOW_CARD = {"tax_year", "filing_status", "residency_code", "county_code", "processed_date", "relationship_code",
            "dependent_birth_year", "txn_type", "channel", "received_date", "overpayment_credit_elect"}


def pq_write(t, path):
    """Deterministic parquet that every common reader opens (pyarrow, pandas, DuckDB, Spark):
    plain encoding, dictionary pages only for low-cardinality columns, zstd."""
    names = t.schema.names
    pq.write_table(t, path, compression="zstd", compression_level=19, row_group_size=1_048_576,
                   use_dictionary=[n for n in names if n in LOW_CARD], data_page_version="1.0")


def write_parquet(df, schema, path):
    cols = {}
    for f in schema:
        s = df[f.name]
        if f.name == "spouse_tin":
            v = s.to_numpy()
            cols[f.name] = pa.array(v, type=f.type, mask=(v == 0))
        elif pa.types.is_date32(f.type):
            cols[f.name] = pa.array(pd.to_datetime(s).dt.date.to_numpy(), type=pa.date32())
        else:
            cols[f.name] = pa.array(s.to_numpy(), type=f.type)
    t = pa.table(cols, schema=schema)
    pq_write(t, path)


def write_csv(df, path):
    df.to_csv(path, index=False, lineterminator="\n", na_rep="")


def write_all(root, R, S, A, app_named, pub, intake_extra):
    tgt = root / "target"
    tgt.mkdir(parents=True, exist_ok=True)
    for y in YEARS:
        write_parquet(R[y], RET_SCHEMA, tgt / FILES["returns"].format(y=y))
        write_parquet(S[y], SCHED_SCHEMA, tgt / FILES["sched"].format(y=y))
    for y in (2022, 2023, 2024):
        docs.household_table(str(tgt / FILES["tables"].format(y=y)), y, pub[y], app_named)
    docs.methodology_pdf(str(tgt / FILES["method"]))
    (tgt / FILES["layouts"]).write_text(docs.record_layouts(), encoding="utf-8")
    (tgt / FILES["thread"]).write_text(docs.THREAD, encoding="utf-8")
    docs.dept_table(str(tgt / FILES["dept"]), docs.dept_table_rows(R[2025]))
    led, pay_txn = shipped.ledger(A)
    lt = pa.table({"txn_id": pa.array(led.txn_id, pa.int64()), "account_tin": pa.array(led.account_tin, pa.int32()),
                   "tax_year": pa.array(led.tax_year, pa.int16()), "txn_type": pa.array(led.txn_type, pa.string()),
                   "amount": pa.array(led.amount, pa.int32()), "txn_utc": pa.array(led.txn_utc, pa.string()),
                   "source_ref": pa.array(led.source_ref, pa.string()), "channel": pa.array(led.channel, pa.string())})
    pq_write(lt, tgt / FILES["ledger"])
    write_csv(shipped.returned_items(A, pay_txn), tgt / FILES["returned"])
    reg = shipped.register(A)
    reg["resolved_tin"] = reg.resolved_tin.astype("Int64").where(reg.resolved_tin > 0)
    write_csv(reg, tgt / FILES["register"])
    write_csv(shipped.schd_extract(A), tgt / FILES["schd"])
    write_csv(shipped.amended_log(A), tgt / FILES["amended"])
    ef = shipped.w2_efile(A)
    et = pa.table({"statement_id": pa.array(ef.statement_id, pa.int64()), "submission_id": pa.array(ef.submission_id, pa.int64()),
                   "employer_ein": pa.array(ef.employer_ein, pa.int32()), "employee_tin": pa.array(ef.employee_tin, pa.int32()),
                   "tax_year": pa.array(ef.tax_year, pa.int16()), "state_wages": pa.array(ef.state_wages, pa.int32()),
                   "state_tax_withheld": pa.array(ef.state_tax_withheld, pa.int32()),
                   "received_date": pa.array(ef.received_date.to_numpy(), pa.date32())})
    pq_write(et, tgt / FILES["efile"])
    (tgt / FILES["paper"]).write_text("\n".join(shipped.w2_paper_lines(A)) + "\n", encoding="ascii")
    docs.recon_table(str(tgt / FILES["recon"]), shipped.recon_summary(A))
    write_csv(A["deposits"], tgt / FILES["deposits"])
    # the office's intake log: what arrived on the share and from whom
    rows = intake_extra(tgt)
    write_csv(pd.DataFrame(rows, columns=["file", "received", "from", "holds", "records"]), tgt / FILES["intake"])
    return tgt


def intake_rows_fn(R, S):
    def f(tgt):
        dor = "Department of Revenue, Research and Statistics Section"
        rows = []
        for y in YEARS:
            rec = "2026-10-23" if y == 2025 else "2026-10-23"
            rows.append((FILES["returns"].format(y=y), rec, dor, f"Processed individual income tax returns, tax year {y}, as of record", len(R[y])))
            rows.append((FILES["sched"].format(y=y), rec, dor, f"Dependents claimed on processed returns, tax year {y}", len(S[y])))
        for y, d in ((2022, "2023-11-14"), (2023, "2024-11-13"), (2024, "2025-11-12")):
            rows.append((FILES["tables"].format(y=y), d, "Revenue Estimating Conference (published)", f"Household Income Tables, tax year {y}", ""))
        rows.append((FILES["method"], "2026-09-18", "Office of Revenue Research", "Income tax tier methodology, revised September 2026", ""))
        rows.append((FILES["layouts"], "2026-10-23", dor, "Record layouts for the research extracts, revision 2026-10", ""))
        rows.append((FILES["thread"], "2026-10-29", "Office of Revenue Research", "Correspondence on the TY2025 delivery and certification", ""))
        rows.append((FILES["dept"], "2026-10-23", dor, "Returns Processed by AGI Class, tax year 2025 (Department publication)", ""))
        for key, holds in (("ledger", "Estimated-tax account activity, tax years 2024 and 2025, posted January 2025 to January 2026"),
                           ("returned", "Payments returned unpaid, 2025 and January 2026"),
                           ("register", "TIN match cases for payments and wage statements"),
                           ("schd", "Schedule D, tax year 2025, latest version received"),
                           ("amended", "Amended returns, tax year 2025, every version"),
                           ("efile", "Wage statements filed electronically, tax year 2025"),
                           ("paper", "Wage statements filed on paper, keyed by the capture vendor, tax year 2025"),
                           ("recon", "Employer annual withholding reconciliations, tax year 2025, by channel"),
                           ("deposits", "Employer withholding deposits received in 2025")):
            p = tgt / FILES[key]
            n = ""
            if p.suffix == ".parquet":
                n = pq.ParquetFile(p).metadata.num_rows
            elif p.suffix in (".csv",):
                n = sum(1 for _ in open(p)) - 1
            elif p.suffix == ".txt":
                n = sum(1 for _ in open(p))
            rows.append((FILES[key], "2026-10-23", dor, holds, n))
        return rows
    return f


# ------------------------------------------------------------------ main

def generate(t0):
    W = Wm.build_world()
    R, S, app, pub, cells, hits, misses, rounds = calib.settle_ties(W, frames)
    R[2025], S[2025] = robust_2025(W)
    print(f"world and frames {time.time() - t0:.0f}s; tie rounds {rounds}", flush=True)
    A = asks.build(W, R[2025], R[2024])
    R[2024] = shipped.apply_credit_elections(R[2024], A)
    for y in (2022, 2023, 2025):
        R[y] = random_elections(R[y], y)
    return W, R, S, A, app, pub


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK))
    ap.add_argument("--skip-slow", action="store_true")
    ap.add_argument("--cache", help="development only: pickle of the generated state, reused if present")
    ap.add_argument("--record", help="write the build record (JSON) to this path, outside the task folder")
    a = ap.parse_args()
    root = Path(a.out).resolve()
    t0 = time.time()
    if a.cache and Path(a.cache).exists():
        import pickle
        W, R, S, A, app, pub = pickle.load(open(a.cache, "rb"))
    else:
        W, R, S, A, app, pub = generate(t0)
        if a.cache:
            import pickle
            pickle.dump((W, R, S, A, app, pub), open(a.cache, "wb"), protocol=4)
    names = {b[1]: b[0] for b in Wm.BIG12}
    app_named = [(names[c], c) for c in app]
    tgt = write_all(root, R, S, A, app_named, pub, intake_rows_fn(R, S))
    print(f"written {time.time() - t0:.0f}s", flush=True)
    import checks
    K = Checks()
    record = checks.run_all(K, W, R, S, A, app, pub, tgt, root, FILES, DISTRACTORS, skip_slow=a.skip_slow)
    meta = metadata(record)
    (root / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    checks.check_metadata(K, root, tgt, DISTRACTORS)
    scrub(tgt)
    checks.check_containers(K, tgt, SCRUB)
    normalise_mtimes(tgt, root)
    if a.record:
        Path(a.record).write_text(json.dumps(record, indent=1, default=str))
    else:
        print(json.dumps(record, indent=1, default=str))
    print(f"ASSERTIONS {K.count()} passed; groups {K.groups()}")
    print(f"total {time.time() - t0:.0f}s")


def metadata(record):
    return {
        "task": "task120",
        "title": "TY2025 household-income tier floors for the Revenue Estimating Conference",
        "domain": "Economics",
        "subdomain": "public-finance",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "14 (cuts of a distribution)",
        "deliverables": ["tier_schedule.xlsx", "tier_floors.png"],
        "as_of": "2026-11-09",
        "distractor_files": DISTRACTORS,
        "sources": [{"files": "all files under target/",
                     "origin": "synthetic: constructed by task120/generator/build.py (seed 120) for a fictional US state; return "
                               "microdata is confidential, so the shape is calibrated to public IRS Statistics of Income state "
                               "AGI-class aggregates and no real record is used",
                     "date": "2026-10-09", "license": "CC0-1.0 (author-generated)"}],
        "files": record["files"],
    }


def scrub(tgt):
    for f in sorted(os.listdir(tgt)):
        p = tgt / f
        if p.suffix.lower() in (".pdf",):
            r = subprocess.run([sys.executable, str(SCRUB), str(tgt), "--apply", "--producer", "Office of Revenue Research",
                                "--stamp", "2026-09-18", "--floor", "2023-01-01", "--ceiling", "2026-11-06"],
                               capture_output=True, text=True)
            if r.returncode not in (0, 1):
                raise RuntimeError(r.stdout + r.stderr)
            break


def normalise_mtimes(tgt, root):
    ts = pd.Timestamp(EXPORT_DATE + " 08:30:00").timestamp()
    for f in sorted(os.listdir(tgt)):
        os.utime(tgt / f, (ts, ts))
    os.utime(tgt, (ts, ts))
    os.utime(root / "metadata.json", (ts, ts))


if __name__ == "__main__":
    main()
