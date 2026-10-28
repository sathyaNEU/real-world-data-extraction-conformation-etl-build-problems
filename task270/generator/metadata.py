"""Write task270/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import common as K

SOURCES = {
    K.F_DEATHS: "NSW Registry of Births, Deaths and Marriages layout: registrations 1 January 2016 to 30 June 2027 of the "
                "deaths of the region's usual residents, released to the network under a data release agreement",
    K.F_INTERSTATE: "Australian Bureau of Statistics layout: deaths of the region's usual residents registered in other "
                    "states and territories, registrations 1 January 2016 to 30 June 2027",
    K.F_CENSUS: "ABS TableBuilder export layout ('CSV string value'): 2021 Census counts by SA2 of usual residence, sex "
                "and single year of age, cells randomly adjusted",
    K.F_ERP: "ABS Regional population by age and sex layout: estimated resident population by local government area "
             "(2023 boundaries), sex and five-year age group to 85 and over, 30 June 2016 to 2026 (2026 preliminary)",
    K.F_NSW: "ABS layout: New South Wales estimated resident population by single year of age (to 100 and over) and "
             "sex, 30 June 2016 to 2026",
    K.F_CORR: "ABS correspondence layout: ASGS 2021 SA2 to 2023 local government area",
    K.F_GUIDE: "Tidewell Coast and Ranges Primary Health Network, late-life frailty program 2028 to 2030, program "
               "guidelines version 1.0 (2 September 2027)",
    K.F_AH: "Tidewell After Hours Medical Service attendance export for 2026 (January to June from the old clinical "
            "system, July to December from the new), one row per clinician attending",
    K.F_RACF: "Residential aged care services in the region at 30 June 2026 (service list filtered to the network's SA2s)",
    K.F_FALLS: "Falls-related injury hospitalisations of people aged 65 and over by local government area, 2024-25 "
               "(published table)",
}
TITLE = ("Which of a primary health network's twelve local government areas qualify for its 2028 to 2030 late-life "
         "frailty program, the areas whose residents reaching 85 could expect fewer than seven more years under the "
         "area's 2024 to 2026 death rates, each age's population inside the published 85-and-over estimate rebuilt from "
         "the 2021 census followed forward with each birth window's deaths; with the after-hours service's 2026 visits "
         "to residents aged 85 and over and the residents they reached")


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


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": K.AS_OF.isoformat(),
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task270",
        "title": TITLE,
        "domain": "Sociology & Demography",
        "client_domain": "Sociology & Demography",
        "subdomain": "fertility-mortality-life-table-estimation (period life expectancy at 85 by local government area "
                     "on a single-year life table to 95 and over, each age's population inside the published "
                     "85-and-over estimate rebuilt from the census and the deaths since)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "scorecard against a threshold: each of twelve areas' life expectancy at 85 against the "
                        "seven-year line and whether it qualifies, beside each area's after-hours visits to residents "
                        "aged 85 and over in 2026 and the residents they reached, and a chart",
        "as_of": K.AS_OF.isoformat(),
        "deliverables": [K.G_BOOK, K.G_CHART],
        "distractor_files": K.DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task270/generator/build.py (seeded, deterministic) around a "
                               "fictional New South Wales primary health network and its twelve local government areas, "
                               "in the layouts of a registry death registration extract, an ABS file of deaths "
                               "registered interstate, an ABS TableBuilder census export, ABS estimated resident "
                               "population tables and an ASGS correspondence, a commissioned after-hours service's "
                               "attendance export, a residential aged care service list, a published hospitalisation "
                               "table and the network's PDF program guidelines; the NSW Registry of Births, Deaths and "
                               "Marriages and the Australian Bureau of Statistics are named descriptively as the "
                               "publishers whose layouts are followed, and no real organisation's records or person is "
                               "depicted.",
                     "date": K.AS_OF.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-28",
        "generator": "task270/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
