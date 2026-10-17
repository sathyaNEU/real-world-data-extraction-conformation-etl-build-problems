"""Write task158/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_ROLLUP: "Slenk fleet capacity rollup, GPU busy time and gateway counters by pool and UTC hour, 1 January to 6 "
                "December 2026",
    R.F_BILLING: "Slenk billing, Docs usage by organisation, channel and Amsterdam business day, 1 September to 6 "
                 "December 2026",
    R.F_INTAKE: "Slenk fleet capacity, Q1 2027 capacity intake from the six product teams (filed by 27 November 2026)",
    R.F_PLAN: "Slenk fleet capacity, Q1 2027 fleet plan, issue v3 (1 December 2026)",
    R.F_LEDGER: "Slenk report service, commitments ledger export (4 December 2026)",
    R.F_NODES: "Slenk fleet inventory, nodes with hall, rack and pool memberships (6 December 2026)",
    R.F_JOBS: "Slenk fleetctl, job step log, 26 October to 6 December 2026",
    R.F_CONSOLE: "Slenk ops console, audit export, 26 October to 6 December 2026",
    R.F_BURN: "Noordermeer Compute, NX7 stopgap cluster burn-in results as sent for the 4 December 2026 review",
    R.F_FABRIC: "Noordermeer Compute, NX7 stopgap cluster all-reduce results as sent for the 4 December 2026 review",
    R.F_HANDOVER: "Noordermeer Compute, NX7 stopgap cluster handover inventory (4 December 2026)",
    R.F_INCIDENTS: "Slenk serving incident log, July to December 2026",
    R.F_SPEC: "Slenk GPU spec register, serving deployments and the leased cluster (7 December 2026)",
    DOC.F_POLICY: "Slenk fleet capacity, stopgap capacity policy for Q1 2027 (16 November 2026)",
    DOC.F_CLOSEOUT: "Slenk fleet capacity, Q3 2026 capacity close-out (16 October 2026)",
    DOC.F_SCHEDULE: "Lease of GPU capacity, Noordermeer Compute and Slenk, Schedule 3: Acceptance (13 November 2026)",
    DOC.F_LEASE: "Lease of GPU capacity, Noordermeer Compute and Slenk, principal terms (13 November 2026)",
    DOC.F_NOTES: "Slenk capacity desk, notes on the 7 December 2026 pull",
    DOC.F_LOG: "Slenk capacity desk, log of the 7 December 2026 pull",
}
DISTRACTORS = [R.F_INCIDENTS, R.F_SPEC, DOC.F_LEASE]
TITLE = ("Which of an Amsterdam model provider's six serving pools gets a leased 240-GPU stopgap for Q1 2027, and "
         "that pool's Q1 peak-week GPU shortfall, when the document Q&A pool takes on eleven report-service "
         "contracts whose every call opens its own session")


def rows_of(path):
    if path.endswith(".csv") or path.endswith(".jsonl"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - (1 if path.endswith(".csv") else 0)
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-12-07",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task158",
        "title": TITLE,
        "domain": "General Statistics & Data Science",
        "client_domain": "General Statistics & Data Science",
        "house_domain": "general-statistics-data-science",
        "subdomain": "regression-classification-model-diagnostics (GPU busy time regressed on the prompt tokens a model "
                     "computes and the tokens it generates, the specification chosen on its out-of-sample fit to an "
                     "early-access tenant's report calls)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed pick (one of six serving pools for a leased cluster) with the pool's Q1 peak-week "
                        "GPU shortfall to the nearest 10, a table of each pool's November out-of-service GPU-hours "
                        "and longest stay out, a table of the leased cluster's accepted GPUs by rack with the nodes "
                        "held back, and a bar chart of the November out-of-service GPU-hours",
        "as_of": "2026-12-07",
        "deliverables": ["stopgap_q1_2027.xlsx", "pool_out_of_service_nov2026.png"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": ["240"],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task158/generator/build.py (seeded, deterministic) around "
                               "a fictional Amsterdam model provider, in the layouts of a fleet capacity rollup, a "
                               "billing usage export, maintenance automation and ops console logs, a provider's "
                               "acceptance exports and the provider's own planning workbooks and documents; no real "
                               "organisation's records or person is depicted.",
                     "date": "2026-12-07", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task158/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
