"""Write task166/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence. Every file is constructed; none is labelled as a real organisation's release."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_LEGACY: "Carrick Valley Bank legacy mortgage servicing platform, monthly loan extract of the 2023 and 2024 "
                "originations, cycles January 2023 to August 2024",
    R.F_SERV: "Carrick Valley Bank mortgage servicing platform, monthly loan extract of the 2023 and 2024 originations, "
              "September 2024 to November 2026",
    R.F_XREF: "Carrick Valley Bank servicing conversion, legacy loan numbers to loan ids (August 2024)",
    R.F_RATES: "Carrick Valley Bank pricing desk, posted rate sheet archive, 2015 to November 2026",
    R.F_CRE: "Carrick Valley Bank commercial loan system, commercial real estate term loans at 30 November 2026",
    R.F_STMT: "Carrick Valley Bank credit administration, borrowers' annual operating statements as reviewed, from 2013",
    R.F_CUSTODY: "Carrick Valley Bank custodian statement of the available-for-sale account, 30 November 2026 "
                 "(constructed holdings and identifiers)",
    R.F_FACTORS: "Carrick Valley Bank investment accounting, monthly factors of the agency pools held (constructed "
                 "pools; not an agency release)",
    R.F_AUTO: "Carrick Valley Bank consumer loan system, indirect auto loans at 30 November 2026",
    R.F_ROLL: "Carrick Valley Bank consumer finance, indirect auto portfolio roll by month from January 2023",
    R.F_SCHED: "Carrick Valley Bank treasury system, notional schedules of the amortizing swaps",
    R.F_CLEAR: "Carrick Valley Bank clearing broker statement of cleared swaps, 30 November 2026 (constructed)",
    R.F_LOCKS: "Carrick Valley Bank mortgage pipeline, rate locks outstanding at 30 November 2026",
    DOC.F_LOG: "Carrick Valley Bank credit administration, commercial real estate maturity log, 2015 to 2026",
    DOC.F_PLAN: "Carrick Valley Bank ALCO planning cycle, 2027 plan, base case (21 September 2026)",
    DOC.F_REGISTER: "Carrick Valley Bank treasury system, register of interest-rate swaps at 30 November 2026",
    DOC.F_NMD: "Carrick Valley Bank ALM, non-maturity deposit study 2026",
    DOC.F_POLICY: "Carrick Valley Bancorp treasury, balance sheet hedging policy version 1.0 (24 March 2026)",
    DOC.F_ALM: "Carrick Valley Bank ALM, report for the third quarter of 2026 (14 October 2026)",
    DOC.F_NOTES: "Carrick Valley Bank ALM, notes on the files pulled for the overlay designation memo (3 December 2026)",
}
DISTRACTORS = [DOC.F_NMD, R.F_LOCKS]
TITLE = ("Which fixed-rate pool a Pittsburgh regional bank's one $1.2 billion four-year pay-fixed swap overlay is "
         "designated against, ranked on the +200 basis point loss in economic value averaged over the swap's first "
         "year, when the 2023-24 mortgages lose most on last year's speed and most of the commercial real estate "
         "balloons due in 2027 cannot be refinanced at the planning cycle's rate")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
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
                    "source": "Constructed: " + SOURCES[f], "date": "2026-12-03",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task166",
        "title": TITLE,
        "domain": "Banking, Credit & Financial Risk",
        "client_domain": "Banking, Credit & Financial Risk",
        "house_domain": "banking-credit-financial-risk",
        "subdomain": "stress-testing-capital (interest-rate risk in the banking book: each fixed-rate pool's +200 bp "
                     "loss in economic value through the swap's first year, on base-case cash flows that need each "
                     "pool's behaviour forecast: mortgage prepayment at the planning rate, commercial real estate "
                     "balloons extended by their refinance cover)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed designation (one of five pools) with its averaged +200 bp loss to the nearest $25 "
                        "million, a table of the hedge programme's notional in effect at each 2027 quarter-end for its "
                        "overlays, funding hedges and loan hedges, and a two-slide ALCO deck charting it",
        "as_of": "2026-12-03",
        "deliverables": ["overlay_designation_2027.xlsx", "overlay_designation_alco.pptx"],
        "distractor_files": DISTRACTORS,
        "field_terms": ["ladder"],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task166/generator/build.py (seeded, deterministic) around a "
                               "fictional Pittsburgh bank holding company, in the layouts of a mortgage servicing "
                               "platform's monthly loan extract before and after a conversion, a commercial loan "
                               "system, a credit administration log and review file, a custodian's holdings statement, "
                               "an agency pool factor history, a consumer loan tape and roll, a treasury system's swap "
                               "register and a clearing broker's statement, office workbooks and PDF documents; the "
                               "securities, pools and identifiers are constructed and are not an agency's or a "
                               "custodian's release, and no real organisation's records or person is depicted.",
                     "date": "2026-12-03", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task166/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
