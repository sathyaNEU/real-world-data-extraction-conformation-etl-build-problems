"""metadata.json: the decision, the deliverables, the distractors and each file's provenance, never the method."""
import pack as P


def metadata(counts):
    files = {
        P.FILES["northmark"]: dict(source="Northmark Field Research case system export, PHMS 2023 to 2025 waves",
                                   date="2025-06-20", licence="synthetic, CC0", rows=counts["northmark"],
                                   made="constructed by the task author's generator from a simulated survey"),
        P.FILES["ostrander"]: dict(source="Ostrander Data Collection case export, PHMS 2025", date="2025-06-17",
                                   licence="synthetic, CC0", rows=counts["ostrander"],
                                   made="constructed by the task author's generator"),
        P.FILES["weights"]: dict(source="Survey Research Centre weighting system, area table", date="2025-07-08",
                                 licence="synthetic, CC0", rows=counts["weights"],
                                 made="constructed by the task author's generator"),
        P.FILES["crosswalk"]: dict(source="Ministry of Health concordance of survey areas", date="2024-03-14",
                                   licence="synthetic, CC0", rows=counts["crosswalk"],
                                   made="constructed by the task author's generator"),
        P.FILES["regions"]: dict(source="Survey Research Centre region list", date="2024-04-01", licence="synthetic, CC0",
                                 made="constructed by the task author's generator"),
        P.FILES["nm_codes"]: dict(source="Northmark Field Research code list", date="2023-01-16", licence="synthetic, CC0",
                                  made="written by the task author"),
        P.FILES["os_codes"]: dict(source="Ostrander Data Collection code frame", date="2025-01-27", licence="synthetic, CC0",
                                  made="written by the task author"),
        P.FILES["report"]: dict(source="Survey Research Centre, PHMS 2025 technical report", date="2025-11-18",
                                licence="synthetic, CC0", made="written by the task author, tables computed by the generator"),
        P.FILES["terms"]: dict(source="Wexcombe Foundation grant terms WF-2026-117", date="2026-10-09",
                               licence="synthetic, CC0", made="written by the task author"),
        P.FILES["pharmacy"]: dict(source="College of Pharmacists community pharmacy register extract", date="2025-09-30",
                                  licence="synthetic, CC0", rows=counts["pharmacy"],
                                  made="constructed by the task author's generator"),
        P.FILES["quotes"]: dict(source="PHMS 2027 fieldwork quotes from the two contractors", date="2026-10-03",
                                licence="synthetic, CC0", made="written by the task author"),
    }
    return {
        "task": "task311",
        "title": "Placing a foundation's 2027 boost of 1,200 survey interviews among five health regions",
        "domain": "survey-research-official-statistics",
        "objective": "Opportunity Sizing & Decision Support",
        "decision": "the health region that receives the 1,200 extra interviews in the 2027 wave",
        "deliverables": ["boost_region_2027.xlsx", "boost_memo_2027.pdf"],
        "distractor_files": ["target/" + f for f in P.DISTRACTORS],
        "files": {"target/" + k: v for k, v in files.items()},
        "as_of": "2026-11-02",
    }
