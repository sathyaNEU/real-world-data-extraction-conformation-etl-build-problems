"""Build the pack, the goldens and metadata.json, run every check and the verifier, build a second time
into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task229/generator/make.py
"""
import filecmp
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import checks as C
import deliver as DL
import pack as P
import verify as V

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SOURCES = {
    "mdm": "MDM interval receipt extract: one row per data stream, read date and delivery, read dates 5 to 11 October 2026",
    "hes": "Head-end (HES) firmware service export: every meter and its firmware events since commissioning",
    "register": "MP installation register extract: installations, meters with install and removal times, data streams",
    "catalogue": "Firmware engineering release catalogue: release names and HES image ids",
    "wave8": "Rollout desk Wave 8 schedule workbook, both batches",
    "standard": "Controlled document MDS-STD-114 revision 3, firmware read health",
    "fieldref": "MDS analytics field reference for the read-health extracts",
    "log": "Extract log for the pull of 12 October 2026",
    "census": "HES nightly firmware census by image and status, 00:00 on 12 October 2026",
    "dnsp": "Planned supply interruption notifications received from the distributors in October 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        return sum(1 for _ in open(path)) - 1
    if path.endswith(".json"):
        d = json.load(open(path))
        return sum(len(m["events"]) for m in d["meters"])
    return None


def metadata():
    files = []
    for k, f in P.FILES.items():
        p = os.path.join(TARGET, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task229",
        "title": "Which comms firmware builds the read-health alert fires on before a smart-meter rollout wave",
        "domain": "Energy Systems & Utilities",
        "subdomain": "other: smart-meter interval data delivery quality (metering data provider read performance)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10 (scorecard against thresholds): eight builds, each with read health, its standard error, lower limit, distance from the limit and fire or hold, plus the Wave 8 moves under the call and the substitution load",
        "as_of": "2026-10-12",
        "deliverables": ["wave8_read_health_alerts.json", "read_health_by_build_wk41.png"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task229/generator/make.py (seeded, deterministic) around a fictional "
                               "metering data provider (Halvane Metering) with real New South Wales distributor names and the "
                               "AEMO NMI checksum; no real installation, meter, customer or firmware product is depicted.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task229/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def digest(folder):
    out = {}
    for f in sorted(os.listdir(folder)):
        out[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return out


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 12, 15, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp


def main():
    world = B.build(TARGET)
    DL.main(TARGET, GOLDEN)
    metadata()
    n, log = C.run(TARGET, world)
    V.main(TARGET, GOLDEN)
    tmp = tempfile.mkdtemp()
    t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    B.build(t2, quiet=True)
    DL.main(t2, g2)
    d1, d2 = digest(TARGET), digest(t2)
    bad = [f for f in d1 if d1[f] != d2.get(f)]
    gd = [f for f in os.listdir(GOLDEN) if not filecmp.cmp(os.path.join(GOLDEN, f), os.path.join(g2, f), shallow=False)]
    shutil.rmtree(tmp)
    if bad or gd:
        raise SystemExit("second build differs: %s %s" % (bad, gd))
    print("two builds byte-identical (%d target files, %d golden files)" % (len(d1), len(os.listdir(GOLDEN))))
    print("zip:", cut_zip())


if __name__ == "__main__":
    main()
