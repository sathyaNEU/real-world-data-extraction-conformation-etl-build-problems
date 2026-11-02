"""Write task161/metadata.json from the built pack."""
import json
import os

import pack as P

SOURCES = {
    P.F_LEGACY: ("Pellerin Distribution Services, legacy WMS1 daily inventory by client (pipe-delimited export)",
                 "business days 2019-04-01 to 2022-09-30"),
    P.F_NIGHTLY: ("Pellerin Distribution Services, WMS nightly inventory run by site and client",
                  "runs of 2022-09-13 to 2026-12-07"),
    P.F_OUTBOUND: ("Pellerin Distribution Services, WMS outbound loads and pallets by client and day",
                   "ship dates 2022-09-12 to 2026-12-06"),
    P.F_RECEIPTS: ("Pellerin Distribution Services, WMS inbound receipts with equipment",
                   "receipts of 2022-09-12 to 2026-12-06"),
    P.F_LPN: ("Pellerin Distribution Services, WMS pallet-level inventory by warehouse location",
              "the run of 2026-12-07T08:00Z"),
    P.F_CLIENTS: ("Pellerin Distribution Services, WMS client master", "as of 2026-12-07"),
    P.F_SITES: ("Pellerin Distribution Services facilities, site list", "as of 2026-12-07"),
    P.F_TRACKER: ("Pellerin Distribution Services customer service, December 2026 inbound booking tracker",
                  "arrivals due 2026-12-07 to 2026-12-31"),
    P.F_AVILA: ("Avila Transload Services, record of the trailers it delivered to Pellerin and the ocean containers "
                "each carried", "deliveries of 2024-03-04 to 2026-12-06"),
    P.F_POLA: ("monthly container statistics in the layout of the Port of Los Angeles's public release",
               "January to October 2026"),
    P.F_POLB: ("monthly TEU statistics in the layout of the Port of Long Beach's public release",
               "January to October 2026"),
    P.F_POLICY: ("Pellerin Distribution Services operations, space planning policy OPS-07, revision 4",
                 "effective 2026-03-02"),
    P.F_OFFER: ("Ridley-Ames Industrial Properties, block offer for Tamarind Avenue Logistics Park Building B",
                "letter of 2026-11-19"),
    P.F_ADVISORIES: ("Yamamoto & Vance Customs Brokers, client advisories on additional duties",
                     "advisories of 2019 to 2026, printed 2026-12-03"),
    P.F_CAPACITY: ("Pellerin Distribution Services capacity planning, capacity report, fiscal 2026 periods 1 to 12",
                   "2025-12-01 to 2026-11-30"),
    P.F_LABOR: ("Pellerin Distribution Services operations, dock labor plan, January to June 2027 (draft)",
                "2027-01 to 2027-06"),
}
AS_OF = "2026-12-07"


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh) - 1
    if path.endswith(".txt"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if ln.strip()) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
    return None


def write(target, out_path):
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        src, covers = SOURCES[f]
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + src, "covers": covers,
                    "date": P.FILE_STAMPS[f].date().isoformat(),
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task161",
        "title": "How many overflow blocks an import 3PL beside the San Pedro Bay ports should take for January to "
                 "June 2027 after customers front-loaded ahead of a duty increase",
        "domain": "Supply Chain & Logistics",
        "client_domain": "Urban & Regional Science",
        "subdomain": "fulfillment-warehousing (an import 3PL's commitment to overflow storage blocks for January to "
                     "June 2027 after its customers front-loaded imports ahead of a duty increase)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a count of overflow blocks to take for a half-year term, with the import TEU and port share "
                        "of January to October 2026 (twenty figures, charted)",
        "as_of": AS_OF,
        "deliverables": ["overflow_blocks_h1_2027.xlsx", "port_share_2026.pdf"],
        "distractor_files": list(P.DISTRACTORS),
        "field_terms": [],
        "stated_inputs": ["40,000", "40000", "4,000", "4000", "1,100,000", "1100000"],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task161/generator/build.py (seeded, deterministic) around "
                               "a fictional import 3PL (Pellerin Distribution Services) with four buildings in Carson, "
                               "Rancho Dominguez, Wilmington and Compton, its clients, people and systems, a fictional "
                               "industrial landlord (Ridley-Ames Industrial Properties) and park (Tamarind Avenue "
                               "Logistics Park), a fictional customs broker (Yamamoto & Vance Customs Brokers) and "
                               "transload partner (Avila Transload Services); no real company, person or system is "
                               "depicted. The two ports' monthly statistics for 2026 are constructed in the layout of "
                               "each port's public release and are not the ports' published figures. The broker's "
                               "advisories describe the 2019 and 2025 United States duty changes in general terms; the "
                               "duty increase of 1 January 2027 is fictional. Container owner prefixes, carriers, "
                               "vessels and terminal names are used descriptively.",
                     "date": AS_OF, "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task161/generator/build.py",
        "files": out,
    }
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
