"""task483 metadata.json: provenance and the input gates, outside target/."""
import csv
import json
import os

import pack as P

SOURCES = [
    {"files": [P.FILES["cultures"], P.FILES["organisms"], P.FILES["antimicrobials"]],
     "origin": "constructed: the pathology network laboratory's urine culture export across its two laboratory "
               "systems (go-live 7 September 2026) and its current code tables, generated from a simulated process "
               "of consultations, cultures and susceptibilities (task483/generator/world.py, records.py, pack.py)",
     "date": "2027-01-06", "license": "CC0-1.0 (synthetic, no real patient data)"},
    {"files": [P.FILES["issues"]],
     "origin": "constructed: the federation's EMIS and SystmOne issue extract for urinary problems, generated from "
               "the same simulated consultations", "date": "2027-01-07", "license": "CC0-1.0 (synthetic)"},
    {"files": [P.FILES["register"], P.FILES["codelists"], P.FILES["spec"]],
     "origin": "constructed: the federation's register, pathway code lists and pathway specification, written for "
               "this task; drug choices follow NICE NG109 (lower UTI, antimicrobial prescribing, 2018)",
     "date": "2026-12-03", "license": "CC0-1.0 (synthetic); NICE NG109 cited, not reproduced"},
    {"files": [P.FILES["icb"], P.FILES["cdiff"], P.FILES["lists"]],
     "origin": "constructed: ICB prescribing indicators, community C. difficile cases and an NHS Digital style "
               "registered-list file for the invented practices (layout after NHS Digital's Patients Registered at "
               "a GP Practice, Open Government Licence v3.0)", "date": "2026-11-13",
     "license": "CC0-1.0 (synthetic); layout reference OGL-3.0"},
]


def _rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return sum(1 for _ in csv.reader(fh)) - 1


def write(target, path):
    files = sorted(os.listdir(target))
    sizes = {f: _rows(os.path.join(target, f)) for f in files if f.endswith(".csv")}
    big = max(sizes, key=sizes.get)
    meta = {
        "task": "task483", "architecture": 2,
        "title": "Placing the 2027-28 UTI pathway pharmacists",
        "domain": "pharmacology-pharmacoepidemiology-safety", "subdomain": "benefit-risk-assessment",
        "objective": "Opportunity Sizing & Decision Support", "prompt_shape": "01", "as_of": "2027-01-11",
        "deliverables": ["uti_pathway_placement_2027-28.xlsx", "uti_pathway_placement_note_2027-28.docx"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
                        "largest_file": big, "largest_file_rows": sizes[big]},
        "sources": SOURCES,
    }
    with open(path, "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
