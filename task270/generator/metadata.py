"""Write task270/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import docs as DOC
import pilot as PL
import records as R

SOURCES = {
    R.F_DISP: "Iversford Vale Health Data Service, community pharmacy statin dispensing for the patients registered "
              "with Iversford Vale GP Federation's member practices, 1 December 2025 to 31 December 2026 (pulled 11 January 2027), pseudonymised",
    R.F_QUARVIS: "Iversford Vale Health Data Service, lipid cohort list from the Quarvis practices at 31 December 2026",
    R.F_SYNARIS: "Iversford Vale Health Data Service, lipid cohort list from the Synaris practices at 31 December 2026",
    R.F_XWALK: "Iversford Vale Health Data Service, pseudonym crosswalk at the re-keying of 1 July 2026",
    R.F_PRACTICES: "NHS Iversford Vale Integrated Care Board primary care team, practice membership of the primary care "
                   "networks, 2026",
    R.F_PRODUCTS: "NHS Iversford Vale Integrated Care Board medicines optimisation team, statin products in use "
                  "(December 2026)",
    PL.F_PORTAL: "Iversford Vale GP Federation services portal, statin adherence pilot export (pulled 2 October 2026)",
    PL.F_STATEMENTS: "Iversford Vale GP Federation finance, pilot payment statements, November 2025 to "
                     "January 2027",
    PL.F_PHARMACIES: "NHS Iversford Vale Integrated Care Board primary care team, community pharmacy list "
                     "(December 2026)",
    DOC.F_SPEC: "Iversford Vale GP Federation, Statin Adherence Support Service specification 2027-28 "
                "(16 November 2026)",
    DOC.F_GUIDE: "NHS Iversford Vale Integrated Care Board, compliance aids prescribing and supply guidance "
                 "(2 June 2025)",
    DOC.F_CPCF: "NHS Iversford Vale Integrated Care Board primary care contracting, a summary of the community "
                "pharmacy contractual framework 2024-26 (30 September 2024)",
}
DISTRACTORS = [DOC.F_CPCF, R.F_PRODUCTS]
TITLE = ("Which primary care networks a GP federation puts in the enhanced tier of its 2027-28 statin "
         "adherence service, on each network's 2026 share of its older self-managing statin patients under 80 per "
         "cent of days covered")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(sum(1 for _ in ws.iter_rows(values_only=True)) - 1, 0) for ws in wb.worksheets)
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "role": "distractor" if f in DISTRACTORS else "input",
                    "source": "Constructed: " + SOURCES[f], "date": "2027-01-27",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task270",
        "title": TITLE,
        "domain": "Pharmacology, Pharmacoepidemiology & Safety",
        "client_domain": "Pharmacology, Pharmacoepidemiology & Safety",
        "subdomain": "medication-adherence-persistence (a GP federation's enhanced tier for its statin "
                     "adherence service, each primary care network's 2026 share of its older self-managing statin "
                     "patients under 80 per cent of days covered, read from community pharmacy dispensing)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "cuts of a distribution per segment: twelve networks with each network's population and share "
                        "fallen behind against the 30 per cent line, the closest network left out and its gap, a "
                        "chart; and a table of the pilot's first consultations (October 2025 to September 2026) and six-week follow-ups by "
                        "quarter in two networks",
        "as_of": "2027-01-27",
        "deliverables": ["statin_service_tiers_2027-28.docx", "statin_adherence_2026_by_network.xlsx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task270/generator/build.py (seeded, deterministic) around "
                               "a fictional English GP federation, its twelve primary care networks, their "
                               "practices on two clinical systems, the community pharmacies and the integrated care "
                               "board whose data service supplies the extracts, in the layouts of a "
                               "health data service's dispensing extract and practice lists, a services portal export "
                               "and a commissioner's payment statements; no real organisation's records or person is "
                               "depicted.",
                     "date": "2027-01-27", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-27",
        "generator": "task270/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
