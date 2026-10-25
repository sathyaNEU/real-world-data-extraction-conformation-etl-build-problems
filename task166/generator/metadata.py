"""Write task166/metadata.json from the built pack: the distractors, the input gates and every shipped file's source, date
and licence. Every file is constructed; none is labelled as a real organisation's release."""
import json
import os

import asks as A
import docs as DOC
import records as R

SOURCES = {
    R.F_LEGACY: "Hollowell Community Credit Union legacy core, home equity loan master archived at the 1 September 2024 "
                "conversion (loans on the books at any month-end from December 2018 to August 2024)",
    R.F_CORE: "Hollowell Community Credit Union core system, monthly trial balance of fixed-rate home equity loans, "
              "September 2024 to November 2026",
    R.F_XREF: "Hollowell Community Credit Union core conversion, legacy loan and member numbers to new (September 2024)",
    R.F_LOS: "Hollowell Community Credit Union lending system, funded fixed-rate home equity loans since 2009 with the "
             "senior lien as underwritten",
    R.F_SERV: "Hollowell Community Credit Union mortgage servicing system, first mortgages active at 30 November 2026 or "
              "paid in full since January 2025",
    R.F_MAP: "Hollowell Community Credit Union lending administration, counties of the regional lending centers",
    R.F_RATES: "Hollowell Community Credit Union pricing desk, posted rate sheet archive, December 2018 to November 2026",
    R.F_HELOC: "Hollowell Community Credit Union core system, home equity lines of credit at 30 November 2026",
    R.F_HPI: "Hollowell Community Credit Union ALM market data, county house price index (constructed, not an agency "
             "release)",
    A.F_LOG: "Hollowell Community Credit Union payoff statement system, requests October 2025 to November 2026",
    A.F_MANUAL: "Hollowell Community Credit Union payoff desk, statements prepared by hand during the March 2026 upgrade",
    DOC.F_PLAN: "Hollowell Community Credit Union ALM, 2027 planning cycle rates (22 September 2026)",
    DOC.F_POLICY: "Hollowell Community Credit Union Lending Policy section 7.4, version 1.0 (21 October 2026)",
    DOC.F_ALM: "Hollowell Community Credit Union ALM report for the third quarter of 2026 (16 October 2026)",
    DOC.F_DICT: "Hollowell Community Credit Union lending analytics, data dictionary of the files pulled 3 December 2026",
    DOC.F_MANIFEST: "Hollowell Community Credit Union lending analytics, list of the files pulled 3 December 2026",
}
DISTRACTORS = [R.F_HELOC, R.F_HPI]
TITLE = ("Which of a West Michigan credit union's four regional lending centers opens its 2027 payoff-retention pilot, by "
         "the fixed-rate home equity principal each region's members will pay off in 2027, when the largest new home "
         "equity loans sit behind small seasoned first mortgages")


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
        "subdomain": "deposit-liquidity-behaviour (home equity prepayment: each region's 2027 payoffs of fixed-rate "
                     "closed-end seconds under the planning cycle's base case)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed pick of one of four regional lending centers with its 2027 principal paid ahead of "
                        "schedule to the nearest $10 million and the center second, a table of loans quoted a payoff and "
                        "of those paid in full by center and quarter (32 counts), and a stacked bar chart of the quotes",
        "as_of": "2026-12-03",
        "deliverables": ["he_payoff_pilot_2027.xlsx", "payoff_quotes_by_center.png"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task166/generator/build.py (seeded, deterministic) around a "
                               "fictional West Michigan credit union, in the layouts of a credit union's legacy and new "
                               "core systems, a lending system, a mortgage servicing system, a payoff statement system, a "
                               "pricing desk's rate sheets, office workbooks and PDF documents; the members, loans, "
                               "addresses and creditors are constructed, and no real organisation's records or person is "
                               "depicted.",
                     "date": "2026-12-03", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-25",
        "generator": "task166/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
