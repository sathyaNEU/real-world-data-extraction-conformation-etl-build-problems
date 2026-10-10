"""Build the task125 evidence pack:  python3 build.py [--out DIR] [--no-checks]

Writes DIR/target/ and DIR/metadata.json (DIR defaults to the task folder) and then runs every assertion
in checks.py. Exit status 0 only when every assertion holds. Deterministic: two builds are byte-identical.
"""
import argparse
import datetime as dt
import json
import shutil
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import params as PR          # noqa: E402
import world as WM           # noqa: E402
import screen as S           # noqa: E402
import fernhollow as FHM     # noqa: E402
import docs_data as DD       # noqa: E402
import docs_text as DT       # noqa: E402
import writers as WR         # noqa: E402

TASK = HERE.parent
F = dict(
    spine="wealdmoor_spend_over_500_2023-04_to_2027-02.csv",
    tsp="tenancy_sustainment_payments_2021-07_to_2027-02.csv",
    statements="digit_conformity_statements_2023-24_to_2025-26.pdf",
    method="payment_digit_screen_methodology_2023.pdf",
    runlog="digit_filter_run_log_2025-26.xlsx",
    runbook="digit_filter_run_book_2024-06.docx",
    calendar="bacs_payment_calendar_2025-26_to_2027-28.xlsx",
    rates="shared_lives_carer_rates_2023-24_to_2027-28.pdf",
    closure="home_first_step-down_closure_notice.eml",
    scheme="tenancy_sustainment_scheme_note.docx",
    terms="pasf_lot2_calloff_terms_clauses_4-8.pdf",
    ratecards="fernhollow_rate_cards_2025-26_2026-27.xlsx",
    order="calloff_WCC-FA-2025-26_order_and_variation_1.pdf",
    invoices="fernhollow_invoice_lines_2025-26.csv",
    acks="fernhollow_batch_acknowledgements_2025-26.json",
    q2report="fernhollow_service_report_q2_2025-26.pdf",
    thread="RE_FW_wealdmoor_2027-28_call-off.eml",
    index="calloff_working_papers_index.txt",
    auditplan="internal_audit_plan_2026-27.docx",
    hsf="household_support_fund_2026-27_allocations.xlsx",
)
DISTRACTORS = ["auditplan", "hsf"]
T = dt.datetime
WHEN = dict(spine=T(2027, 3, 1, 8, 41), tsp=T(2027, 3, 2, 10, 5), statements=T(2026, 7, 10, 12, 2),
            method=T(2023, 3, 20, 15, 10), runlog=T(2026, 4, 7, 16, 21), runbook=T(2024, 6, 28, 11, 47),
            calendar=T(2027, 1, 15, 9, 30), rates=T(2023, 3, 31, 14, 12), closure=T(2027, 1, 14, 10, 15),
            scheme=T(2025, 9, 22, 13, 36), terms=T(2023, 4, 1, 9, 0), ratecards=T(2026, 2, 17, 10, 44),
            order=T(2025, 9, 22, 16, 3), invoices=T(2026, 6, 4, 11, 18), acks=T(2026, 6, 3, 15, 52),
            q2report=T(2025, 11, 6, 12, 30), thread=T(2027, 3, 1, 14, 22), index=T(2027, 3, 3, 11, 34),
            auditplan=T(2026, 3, 23, 9, 15), hsf=T(2026, 5, 12, 14, 8))


def derive(W):
    """Every derived quantity the pack's documents print and the checks assert."""
    D = {}
    pays = [(p[0], p[5], p[6], p[7]) for p in W.pay]
    D["pays"] = pays
    D["counts"] = {b: S.screen_counts(pays, b) for b in S.BASES}
    D["st"] = S.statements(D["counts"][S.CORRECT], WM.DEPT_ORDER)
    D["cells2526"] = S.flagged_cells(D["counts"][S.CORRECT], "2025/26", WM.DEPT_ORDER)
    D["cells2324"] = S.flagged_cells(D["counts"][S.CORRECT], "2023/24", WM.DEPT_ORDER)
    runs, rows, batches = FHM.build_runs(W, D["cells2324"])
    acks = FHM.examine(batches)
    D.update(runs=runs, runrows=rows, batches=batches, acks=acks, inv=FHM.invoices(acks))
    D["b1"] = FHM.b1_routed(rows)
    D["b2"] = FHM.b2_examined(acks)
    D["c"] = FHM.c_quarters(acks)
    q2 = [a for a in acks if a["_run_month"] in ("2025-07", "2025-08", "2025-09")]
    D["q2"] = dict(batches=len(q2), received=sum(a["payments_received"] for a in q2),
                   returned=sum(a["returned_unexamined"] for a in q2),
                   examined=sum(a["payments_examined"] for a in q2),
                   charged=sum(FHM.charged_qty(a) for a in q2),
                   median_days=int(statistics.median(
                       sum(1 for d in PR.days(dt.date.fromisoformat(a["acknowledged"]) + dt.timedelta(days=1),
                                              dt.date.fromisoformat(a["examination_completed"])) if PR.is_wd(d))
                       for a in q2)))
    return D


def write_pack(W, D, target):
    target.mkdir(parents=True, exist_ok=True)
    p = lambda k: target / F[k]
    n = {}
    n["spine"] = DD.spine(p("spine"), W)
    n["tsp"] = DD.tsp_ledger(p("tsp"), W)
    DT.statements(p("statements"), D["st"], WHEN["statements"])
    DT.methodology(p("method"), WHEN["method"])
    n["runlog"] = DD.run_log(p("runlog"), D["runrows"], WHEN["runlog"])
    DT.run_book(p("runbook"), WHEN["runbook"])
    n["calendar"] = DD.calendar(p("calendar"), WHEN["calendar"])
    DT.rate_schedule(p("rates"), WHEN["rates"])
    DT.closure_notice(p("closure"))
    DT.scheme_note(p("scheme"), WHEN["scheme"])
    DT.framework_terms(p("terms"), WHEN["terms"])
    n["ratecards"] = DD.rate_cards(p("ratecards"), WHEN["ratecards"])
    DT.order_and_variation(p("order"), WHEN["order"])
    n["invoices"] = DD.invoice_lines(p("invoices"), D["inv"])
    n["acks"] = DD.acknowledgements(p("acks"), D["acks"], WHEN["acks"])
    DT.service_report_q2(p("q2report"), D["q2"], WHEN["q2report"])
    DT.calloff_thread(p("thread"))
    DT.index(p("index"), F)
    DT.audit_plan(p("auditplan"), WHEN["auditplan"])
    n["hsf"] = DD.hsf_allocations(p("hsf"), WHEN["hsf"])
    for k in F:
        WR.set_mtime(p(k), WHEN[k])
    return n


def write_metadata(path, target, n):
    files = []
    for k, name in F.items():
        fp = target / name
        files.append({"path": name, "format": fp.suffix.lstrip(".").lower(), "bytes": fp.stat().st_size,
                      "rows": n.get(k), "source": "constructed for this task (see sources)",
                      "date": WHEN[k].date().isoformat(), "license": "CC0-1.0 (original work)"})
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    meta = {
        "task": "task125",
        "title": "Wealdmoor County Council: 2027/28 call-off for examination of digit-filter routed payments",
        "domain": "Accounting, Audit & Forensic Analytics",
        "subdomain": "audit-testing-sampling",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "02 forecast across many periods",
        "as_of": PR.AS_OF.isoformat(),
        "deliverables": ["examination_calloff_2027-28.docx", "examination_calloff_2027-28.xlsx"],
        "distractor_files": [F[k] for k in DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task125/generator/build.py (seeded, deterministic) "
                               "around a fictional English shire county (Wealdmoor) and a fictional assurance "
                               "provider (Fernhollow Assurance Ltd); no real council, payee or record is depicted. "
                               "The spending file follows the layout of English Local Government Transparency Code "
                               "spend-over-500 publications; bank holidays are the published England and Wales "
                               "dates.",
                     "date": "2026-10-10", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-10",
        "generator": "task125/generator/build.py",
        "files": files,
    }
    Path(path).write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK))
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    target = out / "target"
    if target.exists():
        shutil.rmtree(target)
    W = WM.World().build()
    D = derive(W)
    n = write_pack(W, D, target)
    meta = write_metadata(out / "metadata.json", target, n)
    print("files %d, formats %s, spine rows %d" % (len(meta["files"]), ", ".join(meta["input_gates"]["formats"]),
                                                    n["spine"]))
    if a.no_checks:
        return 0
    import checks
    ok = checks.run_all(W, D, target, out / "metadata.json", F, DISTRACTORS)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
