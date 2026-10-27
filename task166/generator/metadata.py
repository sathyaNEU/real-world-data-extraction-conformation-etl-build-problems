"""Write task166/metadata.json from the built pack: the distractors, the input gates and every shipped file's source, date
and licence. Every file is constructed; none is labelled as a real organisation's release."""
import json
import os

import docs as DOC
import onboarding as OB
import records as R

SOURCES = {
    R.F_LEGACY: "Plinthwise legacy billing system, every subscription with a first invoice from January 2015 to February 2023",
    R.F_REG: "Plinthwise subscription register, subscriptions with a service period from 1 December 2022 and the amendments "
             "recorded from that date",
    R.F_CRM: "Plinthwise CRM, customer, former customer and partner accounts at 1 October 2026",
    R.F_DIR: "Plinthwise product user directory, every user account on every workspace to 30 September 2026",
    R.F_TERR: "Plinthwise Sales Operations, the sales territory map from 1 March 2024 and the map before it",
    R.F_SPEND: "Plinthwise Marketing Operations, programme spend actuals February 2019 to September 2026 and the plan "
               "October 2026 to January 2028",
    OB.F_CASES: "Plinthwise onboarding tool, onboarding cases opened January 2024 to September 2026",
    OB.F_SESSIONS: "Plinthwise scheduling tool, onboarding session bookings January 2024 to September 2026",
    OB.F_CSAT: "Plinthwise survey tool, post-onboarding survey responses 2024 to 2026",
    OB.F_ROSTER: "Plinthwise People Operations, the onboarding team roster at 1 October 2026: each specialist's pod assignments with their first and last days, and the specialists who left it since 2024",
    R.F_CATALOG: "Plinthwise billing platform, the product catalog in force from 1 July 2026",
    DOC.F_MEMO: "Plinthwise Customer Onboarding, the VP's request of 20 October 2026",
    DOC.F_BASIS: "Plinthwise FP&A, FY2028 planning basis v1.0 (2 October 2026)",
    DOC.F_DECK: "Plinthwise board materials, FY2023 board deck customer growth pages (14 March 2023)",
    DOC.F_DICT: "Plinthwise Revenue Analytics, field definitions of the files pulled 1 October 2026",
    DOC.F_MANIFEST: "Plinthwise Revenue Analytics, list of the files pulled 1 October 2026",
}
DISTRACTORS = [DOC.F_DECK, OB.F_CSAT]
TITLE = ("Which of a construction software company's six regional sales teams adds the most new paying customers in 2027, "
         "when two in five new customers are founded by project staff who left existing customers and one region's "
         "customers released a surge of them in 2026")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 2, 0) for ws in wb.worksheets if ws.title != "Notes")
        wb.close()
        return n
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-01" if f not in (DOC.F_MEMO, DOC.F_DECK, DOC.F_BASIS) else
                    {DOC.F_MEMO: "2026-10-20", DOC.F_DECK: "2023-03-14", DOC.F_BASIS: "2026-10-02"}[f],
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task166",
        "title": TITLE,
        "domain": "Product Analytics",
        "client_domain": "Product Analytics",
        "house_domain": "product-analytics",
        "subdomain": "feature-adoption-diffusion-modeling (each region's 2027 new paying customers: organic acquisition plus "
                     "the customers founded by users who left paying customers)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed pick of one of six regional sales teams with its 2027 new paying customers to the nearest "
                        "200 and the region second, specialist hours by onboarding pod, quarter of 2025 and session kind "
                        "(24), the 2025 new customers by region and starting plan (18) and the annual contract value they "
                        "signed on each plan on the terms in force on the first paid invoice date (18)",
        "as_of": "2026-10-01",
        "deliverables": ["onboarding_pod_2027.docx", "onboarding_staffing_2025.xlsx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task166/generator/build.py (seeded, deterministic) around a "
                               "fictional construction project-management software company, in the layouts of a legacy "
                               "billing system, a subscription register, a CRM, a product user directory, an onboarding "
                               "tool, a scheduling tool, a survey tool, office workbooks and PDF documents; the companies, "
                               "people, phone numbers and partners are constructed, and no real organisation's records or "
                               "person is depicted.",
                     "date": "2026-10-01", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-26",
        "generator": "task166/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
