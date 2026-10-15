"""Write task142/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.EPISODES: "Hospital in the Home episodes admitted 1 April 2024 to 30 September 2026 from the Alliance warehouse "
                "(Members' admitted episode returns)",
    K.CENSUS: "Hospital in the Home daily census, 1 July 2025 to 30 September 2026, with each day's nurse visits",
    K.CROSSWALK: "Program codes used to 30 June 2025 mapped to the July 2025 streams",
    K.CAMPUSES: "Members' campus codes with validity dates (Altona Park merger, March 2025)",
    K.STREAMDOC: "Hospital in the Home program streams and visit schedule, July 2025 (clinical governance)",
    K.PATHWAY: "Bone and joint infection at home pathway for Northgate and Westmere, August 2026",
    K.PLANS: "Members' Hospital in the Home operating plans 2026-27, revision 1 of October 2026",
    K.CAPACITY: "In-house visit capacity return for January to March 2027",
    K.SCHED2: "Bellbird agreement, Schedule 2 (Variation 9): the January to March 2027 overflow block",
    K.SCHED34: "Bellbird agreement, Schedules 3 and 4 (Variation 8): fees, referrals and service levels",
    K.BB_VISITS: "Bellbird visit records for the Alliance's patients, July to September 2026 (UTC)",
    K.PORTAL: "Referrals sent to Bellbird through the Alliance referral portal, July to September 2026",
    K.REGISTER: "Bellbird intake line log, 2026",
    K.ACCOUNTS: "Bellbird client accounts for the Alliance and its Members",
    K.CALENDAR: "Alliance finance calendar 2026-27 with pay weeks and Victorian public holidays",
    K.DICTIONARY: "Field definitions for the overflow files",
    K.MANIFEST: "Files in the set, with source, period and preparation",
    K.SURVEY: "Hospital in the Home patient experience survey 2025-26",
    K.BB_REPORT: "Bellbird service report to the Alliance, 2025-26",
    K.DECLINED: "Referrals Bellbird declined in 2025-26, with reasons",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".jsonl"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for line in fh if line.strip())
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-11-03",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task142",
        "title": "How many visits of Bellbird Home Nursing's 850-visit January to March 2027 Hospital in the Home "
                 "overflow block each of Ironbark Health Alliance's five members books",
        "domain": "Healthcare Delivery & Health Economics",
        "client_domain": "Healthcare Delivery & Health Economics",
        "subdomain": "utilization-access-demand-forecasting (Hospital in the Home capacity: each member's "
                     "90th-percentile visit requirement for a quarter not yet open, built from planned admissions and "
                     "the stays on file, against a capped block of contract visits booked in a filed order)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "05: allocation of a fixed block (850 visits in lots of 25) across five members in a filed "
                        "order, with each member's requirement, two July to September 2026 tables (what the Alliance "
                        "owes Bellbird by member and month; each member's referrals and Bellbird's two response "
                        "shares) and one chart (payable visits by week and member)",
        "as_of": "2026-11-03",
        "deliverables": [K.GOLD_BOOK, K.GOLD_CHART],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task142/generator/build.py (seeded, deterministic) around "
                               "a fictional purchasing alliance of five Victorian public health services (Ironbark "
                               "Health Alliance), its members, a fictional private home nursing provider (Bellbird "
                               "Home Nursing) and their people; no real organisation, person or system is depicted. "
                               "Diagnosis codes follow ICD-10-AM categories in form only.",
                     "date": "2026-11-03", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-15",
        "generator": "task142/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
