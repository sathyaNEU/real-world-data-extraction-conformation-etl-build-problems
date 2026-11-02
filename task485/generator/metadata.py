"""metadata.json, outside target/: the decision, the deliverables, each file's provenance and the distractors."""
import json

import analysis as A

DESC = {
    "claims": ("Halcroft Pharmacy Solutions, paid claims extract for the Employees' Group Health Plan, brand drugs, "
               "dates of service 1 July 2025 to 30 June 2026, paid through 30 September 2026, pulled 9 October 2026",
               "csv"),
    "drug": ("Halcroft Pharmacy Solutions client portal, drug file for the NDCs on the plan's claims, October 2026", "xlsx"),
    "network": ("Halcroft Pharmacy Solutions, pharmacy network file, 1 October 2026", "txt"),
    "roster": ("Office of Employee Benefits eligibility system, member roster at 9 October 2026", "csv"),
    "policy": ("Office of Employee Benefits, Preferred Drug List Policy EB-RX-04, revised 14 March 2024", "pdf"),
    "review": ("Pharmacy and Therapeutics Committee, clinical review for the 2027 preferred drug list, 12 October 2026",
               "pdf"),
    "exhibit": ("Pharmacy Benefit Services Agreement, Exhibit C, effective 1 July 2024", "pdf"),
    "emails": ("Office of Employee Benefits, messages on the 2027 preferred drug list load, September and October 2026",
               "pdf"),
    "rec25": ("Halcroft Pharmacy Solutions, rebate guarantee reconciliation for plan fiscal year 2025, 30 September 2025",
              "pdf"),
}
for q, d in (("2025Q2", "19 September 2025"), ("2025Q3", "19 December 2025"), ("2025Q4", "20 March 2026"),
             ("2026Q1", "19 June 2026"), ("2026Q2", "18 September 2026")):
    DESC["stmt_" + q] = ("Halcroft Pharmacy Solutions, manufacturer rebate remittance statement for calendar quarter "
                         "%s, remitted %s" % (q.replace("Q", " Q"), d), "xlsx")


def write(path, counts):
    files = []
    for k, (src, fmt) in DESC.items():
        rec = {"path": "target/" + A.FILES[k], "format": fmt, "source": src, "date": src.split(", ")[-1],
               "licence": "Office of Employee Benefits operational record; internal use, released for this analysis"}
        if k in counts:
            rec["rows"] = counts[k]
        files.append(rec)
    meta = {
        "task": "task485",
        "decision": "the preferred product in each brand drug class the Pharmacy and Therapeutics Committee reviews, "
                    "for the Employees' Group Health Plan's 2027 preferred drug list",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "Healthcare Delivery & Health Economics: payment, claims and health plan analytics",
        "deliverables": ["pdl_2027_net_cost.xlsx", "pdl_2027_trustees.pptx"],
        "as_of": "2026-10-19",
        "files": files,
        "distractor_files": ["target/" + A.FILES["stmt_2025Q2"], "target/" + A.FILES["rec25"]],
    }
    json.dump(meta, open(path, "w"), indent=1)
