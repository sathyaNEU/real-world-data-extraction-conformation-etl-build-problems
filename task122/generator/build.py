#!/usr/bin/env python3
"""task122 generator: build the slot review folder (target/) and metadata.json under an output root,
deterministically, then assert the ladder, the archive, the fork grid, the ask layer and the input
gates on the files as written.

    python3 task122/generator/build.py --out <root>          (root defaults to the task folder)
    python3 task122/generator/build.py --out <root> --record <path.json>

Seeded throughout (params.SEED); two builds into different roots are byte-identical.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import archive as Ar  # noqa: E402
import docs as D  # noqa: E402
import params as P  # noqa: E402
import place as PL  # noqa: E402
import records as R  # noqa: E402
import traffic as Tr  # noqa: E402
import world as Wm  # noqa: E402
import writers as Wr  # noqa: E402
import asks as K  # noqa: E402

REPO = HERE.parents[1]
TASK = HERE.parent
SCRUB = REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
EPOCH = datetime(2025, 1, 1)
FLOOR, CEILING = "2023-01-01", P.PACK_DATE.isoformat()

DISTRACTORS = [D.F_SEARCH, D.F_SURVEY]


def archive_frames(tests, meta, A):
    """The tests sheet and the logged-sessions sheet, as the archive workbook carries them."""
    rng = P.stream("archive-sheet")
    band = ["0-29", "30-179", "180-729", "730+"]
    rows = []
    sess = []
    for m in meta:
        df = A[A.test_id == m["test_id"]].reset_index(drop=True)
        s, rw, rp, rs = Ar.arch_estimates(df)
        published = round(rp + 1e-9, 1)
        rows.append(dict(test_id=m["test_id"], policy_family=m["family"], inputs=m["inputs"],
                         logger_version=m["logger"], logging_from=m["log_from"].isoformat(),
                         logging_to=m["log_to"].isoformat(), test_from=m["test_from"].isoformat(),
                         test_to=m["test_to"].isoformat(), traffic_share_pct=m["traffic"], duration_days=m["days"],
                         cells_in_scope="all eight cells" if m["cells"] == "all" else "app cells only",
                         offline_estimate_published=published, realised_lift=m["realised"],
                         realised_lift_low90=round(m["realised"] - m["half"], 1),
                         realised_lift_high90=round(m["realised"] + m["half"], 1)))
        ndays = (m["log_to"] - m["log_from"]).days + 1
        order = rng.permutation(len(df))
        days = rng.integers(0, ndays, size=len(df))
        for i, j in enumerate(order):
            r = df.iloc[j]
            c = int(r.cell)
            sess.append((m["test_id"], f"{m['test_id']}-{i + 1:06d}",
                         (m["log_from"] + timedelta(days=int(days[i]))).isoformat(),
                         P.PLATFORMS[c // 4], band[c % 4], r.arm, float(r.p), int(r.n), int(r.y)))
    T = pd.DataFrame(rows)
    Sx = pd.DataFrame(sess, columns=["test_id", "session_ref", "logged_on", "platform", "tenure_band", "arm",
                                     "propensity", "renders", "in_session_orders"])
    Sx = Sx.sort_values(["test_id", "logged_on", "session_ref"], kind="stable").reset_index(drop=True)
    return T, Sx


def write_all(W, tests_df, arch_sessions, adj, tgt):
    tgt.mkdir(parents=True, exist_ok=True)
    out = {}
    out[Wr.F_RENDER] = Wr.render_log(W, str(tgt / Wr.F_RENDER))
    out[Wr.F_RANKINGS] = Wr.served_rankings(W, str(tgt / Wr.F_RANKINGS))
    out[Wr.F_ORDERS] = Wr.orders(W, str(tgt / Wr.F_ORDERS))
    out[Wr.F_PAYMENTS] = Wr.payments(W, str(tgt / Wr.F_PAYMENTS))
    name, n = Wr.offers(W, str(tgt))
    out[name] = n
    tt = Tr.true_table(adj)
    r1 = Tr.first_release(tt)
    r2 = Tr.r2_table(tt)
    Wr.write_csv(Tr.weekly_frame(r1), str(tgt / K.F_WEEKLY))
    Wr.write_csv(Tr.weekly_frame(r2), str(tgt / K.F_R2))
    with open(tgt / D.F_ICS, "w", encoding="utf-8", newline="") as f:
        f.write(Tr.ics_text())
    D.archive_workbook(str(tgt / D.F_ARCHIVE), tests_df, arch_sessions)
    D.charter(str(tgt / D.F_CHARTER))
    D.terms(str(tgt / D.F_TERMS))
    D.commitment(str(tgt / D.F_COMMIT))
    D.minutes(str(tgt / D.F_MINUTES))
    D.register(str(tgt / D.F_REGISTER))
    D.field_reference(str(tgt / D.F_FIELDS))
    D.release_log(str(tgt / D.F_RELEASES))
    D.capacity_note(str(tgt / D.F_CAPACITY))
    D.tariff_register(str(tgt / D.F_TARIFF))
    D.thread(str(tgt / D.F_THREAD))
    PM = W.PM.copy()
    PM["captured_iso"] = [str(np.datetime64("2025-01-01T00:00:00") + np.timedelta64(int(x), "s")) for x in PM.captured]
    plat = W.O.set_index("order_id").platform
    D.finance_statement(str(tgt / D.F_FINANCE), PM, PM.order_id.map(plat).to_numpy())
    D.search_tests(str(tgt / D.F_SEARCH))
    D.seller_survey(str(tgt / D.F_SURVEY))
    D.folder_index(str(tgt / D.F_INDEX), index_rows(name))
    return out


def index_rows(offers_name):
    pulled = "2026-10-12"
    return [
        (Wr.F_RENDER, "Home carousel render log", "logged sessions 22 Jun to 20 Sep 2026", "carousel logger 4.3", pulled),
        (Wr.F_RANKINGS, "Ranking served in each logged session, with the session's ranker inputs",
         "logged sessions 22 Jun to 20 Sep 2026", "carousel logger 4.3", pulled),
        (Wr.F_ORDERS, "Orders by the logger slice's buyers, every channel", "1 Jun to 11 Oct 2026", "orders warehouse",
         pulled),
        (Wr.F_PAYMENTS, "Checkout payments for those orders", "1 Jun to 11 Oct 2026", "payments ledger", pulled),
        (offers_name, "Accepted offers by those buyers", "offers accepted up to 11 Oct 2026", "offers service", pulled),
        (D.F_ARCHIVE, "Archive of completed home carousel tests", "nine tests, March 2023 to May 2026",
         "Marketplace Science", "2026-06-02"),
        (K.F_WEEKLY, "Weekly logged-in home carousel sessions, first release", "2025-W01 to 2026-W39",
         "analytics warehouse", pulled),
        (K.F_R2, "Restatement R2 of the weekly sessions table", "2026-W01 to 2026-W26", "analytics warehouse", pulled),
        (D.F_RELEASES, "Analytics release log, home tables", "to 14 Aug 2026", "Analytics Engineering", pulled),
        (D.F_CHARTER, "Experimentation charter, home surfaces, v4", "in force from 1 Jun 2026", "Marketplace Science",
         "2026-06-01"),
        (D.F_COMMIT, "Fresh-listing commitment to private sellers", "2026", "Seller Experience", "2026-02-10"),
        (D.F_REGISTER, "Ranking policy register, home carousel", "as of 5 Oct 2026", "Ranking Engineering",
         "2026-10-05"),
        (D.F_FIELDS, "Field reference for the logger and the extracts", "logger 4.3", "Ranking Engineering",
         "2026-10-05"),
        (D.F_TERMS, "Buyer Protection terms for buyers", "in force from 1 Sep 2026", "Legal", "2026-09-01"),
        (D.F_TARIFF, "Buyer-protection tariff register (kopersbescherming)", "rows entered to 22 Sep 2026", "Finance",
         pulled),
        (D.F_MINUTES, "Pricing committee minutes", "meeting of 6 Oct 2026", "Finance", "2026-10-07"),
        (D.F_FINANCE, "Buyer-protection fee income, Q3 2026, logger slice", "Jul to Sep 2026", "Finance",
         "2026-10-09"),
        (D.F_CAPACITY, "Home carousel test capacity and release gating", "as of 22 Sep 2026",
         "Experimentation Programme", "2026-09-22"),
        (D.F_ICS, "App release calendar", "2026 to mid 2027", "Mobile Platform", "2026-09-30"),
        (D.F_THREAD, "Slot thread", "5 to 7 Oct 2026", "#carousel-slot-q1", "2026-10-14"),
        (D.F_SEARCH, "Search ranking tests, first half of 2026", "five tests", "Search Relevance", "2026-07-03"),
        (D.F_SURVEY, "Seller survey on new-listing exposure, Q2 2026", "1,612 responses", "Seller Experience",
         "2026-06-05"),
    ]


def normalise_containers(tgt):
    for f in sorted(os.listdir(tgt)):
        if f.endswith((".docx", ".xlsx")):
            Wr.normalise_zip(str(tgt / f))


def scrub(tgt, producer="Vouwlijn", stamp=None):
    stamp = stamp or P.PACK_DATE.isoformat()
    r = subprocess.run([sys.executable, str(SCRUB), str(tgt), "--apply", "--producer", producer, "--stamp", stamp,
                        "--floor", FLOOR, "--ceiling", CEILING], capture_output=True, text=True)
    a = subprocess.run([sys.executable, str(SCRUB), str(tgt), "--floor", FLOOR, "--ceiling", CEILING],
                       capture_output=True, text=True)
    return r.returncode, a.returncode, (r.stdout + r.stderr + a.stdout + a.stderr)


def normalise_mtimes(tgt, root):
    ts = datetime(P.PACK_DATE.year, P.PACK_DATE.month, P.PACK_DATE.day, 17, 30).timestamp()
    for f in sorted(os.listdir(tgt)):
        os.utime(tgt / f, (ts, ts))
    os.utime(tgt, (ts, ts))
    if (root / "metadata.json").exists():
        os.utime(root / "metadata.json", (ts, ts))


def file_rows(tgt):
    out = []
    for f in sorted(os.listdir(tgt)):
        p = tgt / f
        ext = p.suffix.lstrip(".")
        rows = None
        if ext == "csv":
            rows = sum(1 for _ in open(p, encoding="utf-8")) - 1
        elif ext == "parquet":
            import pyarrow.parquet as pq
            rows = pq.ParquetFile(p).metadata.num_rows
        elif ext == "xlsx" and f == D.F_ARCHIVE:
            rows = int(pd.read_excel(p, sheet_name="logged_sessions", usecols=[0]).shape[0])
        out.append(dict(path=f, format=ext, bytes=p.stat().st_size, rows=rows,
                        source="Constructed for this task: fictional platform Vouwlijn; no third-party data",
                        date=P.PACK_DATE.isoformat(), license="CC0-1.0 (original work)"))
    return out


def metadata(tgt, record):
    files = file_rows(tgt)
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task122",
        "title": "Q1 2027 home carousel test slot: which registered ranking policy",
        "domain": "Product Analytics",
        "subdomain": "experimentation-measurement",
        "objective": "Experiment & Causal Analysis",
        "prompt_shape": "07 (grid of cells)",
        "as_of": P.AS_OF.isoformat(),
        "deliverables": ["carousel_slot_q1_2027.ipynb", "carousel_slot_q1_2027_cells.png"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK))
    ap.add_argument("--record", help="write the build record (JSON) here, outside the task folder")
    ap.add_argument("--skip-checks", action="store_true")
    a = ap.parse_args()
    root = Path(a.out).resolve()
    tgt = root / "target"
    if tgt.exists():
        shutil.rmtree(tgt)
    t0 = time.time()
    W = Wm.build_world()
    R.build_records(W)
    og, fg = PL.orders_grid_now(W), PL.fee_grid_now(W)
    adj, margin = PL.choose_traffic_adjust(W, og, fg)
    W.traffic_adjust, W.traffic_margin = adj, margin
    tests, meta, A = Ar.build_archive()
    A_hidden = Ar.hidden_layers(A)
    tests_df, arch_sessions = archive_frames(tests, meta, A)
    print(f"world, archive {time.time() - t0:.0f}s", flush=True)
    write_all(W, tests_df, arch_sessions, adj, tgt)
    normalise_containers(tgt)
    scrub_rc = scrub(tgt)
    print(f"written {time.time() - t0:.0f}s", flush=True)
    record = {"scrub": scrub_rc}
    if not a.skip_checks:
        import checks
        record.update(checks.run_all(W, meta, A_hidden, tgt, root, DISTRACTORS, scrub_rc))
    meta_doc = metadata(tgt, record)
    with open(root / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta_doc, f, indent=1)
        f.write("\n")
    normalise_mtimes(tgt, root)
    if a.record:
        Path(a.record).write_text(json.dumps(record, indent=1, default=str))
    print(f"total {time.time() - t0:.0f}s")
    if "assertions" in record:
        print(f"ASSERTIONS {record['assertions']} passed")


if __name__ == "__main__":
    main()
