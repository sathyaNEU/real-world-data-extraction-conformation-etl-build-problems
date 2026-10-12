"""Write task185/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "daily": "National Climate Service data portal, Merrin Flat automatic station 041391, daily elements from 1 November 1995",
    "register": "National Climate Service climatological register for Merrin Flat 041207, maximum temperature, 1964 to 1995 (digitised)",
    "parallel": "National Climate Service parallel observations archive, daily maxima on both instruments at seven sites",
    "district": "National Climate Service monthly mean maximum temperature, the district's other stations",
    "stations": "National Climate Service station list, Merrin and Murrow valleys",
    "history": "National Climate Service station history, Merrin Flat",
    "manual": "Southward Mutual weather index pricing manual, revision 3",
    "terms27": "Southward Mutual heat-day cover term sheet, 2027/28 quotation",
    "terms26": "Southward Mutual heat-day cover term sheet, 2026/27 (bound)",
    "notes": "Southward Mutual weather desk extract notes, 27 August 2027",
    "schedule": "Southward Mutual policy system extract, policy schedule for the co-operative's heat-day cover",
    "blocks": "Merrin Valley Winegrowers Co-operative block register at 1 August 2027",
    "claims": "Southward Mutual claims register report, heat-day cover, 2019/20 to 2026/27",
    "ledger": "Southward Mutual general ledger 6120, weather claims payments, FY2020 to FY2028",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2027-08-27",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task185",
        "title": "The premium per hectare to quote Merrin Valley Winegrowers for its 2027/28 heat-day cover at Merrin "
                 "Flat after the station's 1995 change of instrument, the heat days and severe heat days it assumes, "
                 "the 2027/28 schedule by sub-district, and what the cover has paid each season since 2019/20",
        "domain": "General Statistics & Data Science (secondary Physical & Environmental Sciences)",
        "subdomain": "exploratory data analysis and distribution assessment (a paired-instrument difference assessed "
                     "across the range of the reading, for a threshold count read off a weather station with an "
                     "instrument change)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "14 (cuts by segment): the call and its two expected counts, the 2027/28 schedule by the four "
                        "sub-districts, the cover's paid claims by season, the chart",
        "as_of": "2027-08-27",
        "deliverables": ["heat_cover_quote_2027_28.pdf", "heat_cover_payouts.csv"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task185/generator/build.py (seeded, deterministic) around a "
                               "fictional insurer, grower co-operative and national climate service; no real "
                               "organisation, station, person or record is depicted.",
                     "date": "2027-08-27", "license": "CC0-1.0 (original work)"}],
        "created": "2027-08-27",
        "generator": "task185/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
