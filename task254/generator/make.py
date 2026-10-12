"""Build the pack, the goldens and metadata.json, run every check and the independent verifier, build a second
time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task254/generator/make.py            (full checks)
    python3 task254/generator/make.py --quick    (two quantile readings on the mature-cohort sweeps)
"""
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks as CK
import deliver as DL
import pack as P
import target as TG
import verify as V

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SOURCES = {
    "listing": "Safety database (Argus Safety) line listing of every version of every Lyrevo case received up to the extraction run of 6 October 2026",
    "dosage": "Safety database dosage lines of Lyrevo for every case, as held at the extraction run",
    "feed": "Patient support programme vendor's laboratory transfer for programme patients with a safety case",
    "labreg": "PSP partner laboratory register: units and reference limits by laboratory and analyte",
    "dupreg": "Case Processing duplicate management register for Lyrevo",
    "terms": "RMP term list version 4 (MedDRA preferred term to safety concern) with the changes from version 3",
    "annex": "RMP annex 7, methods for characterising the important identified risks, version 3.0",
    "guide": "Field guide for the safety database export (line listing, dosage lines, PSP laboratory feed)",
    "sellin": "SAP sell-in to wholesalers by month, customer and national article code, including credit notes and free goods",
    "calloff": "Third-party logistics provider's hospital call-off report for France, Italy and Spain",
    "master": "Regulatory mapping of national article codes and GTINs to EU presentations",
    "xevmpd": "xEVMPD (Article 57) export of the four authorised presentations",
    "channels": "Supply Chain Planning overview of the supply channel of each market",
    "section5": "PSUR 6 section 5 exposure method note",
    "finance": "Net sales by market and quarter from the management accounts",
    "medinfo": "Medical Information enquiry log",
    "litscreen": "Weekly literature screening log for the PSUR period",
    "signals": "Signal tracker",
    "log": "PSUR 6 data package log (extraction runs, documents, notes)",
}


def rows_of(path):
    if path.endswith(".csv"):
        return sum(1 for _ in open(path, encoding="utf-8")) - 1
    return None


def metadata():
    files = []
    for k, f in P.FILES.items():
        p = os.path.join(TARGET, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-06",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task254",
        "title": "Monitoring windows for the identified risks of an oral immunomodulator, set from a post-marketing case series at the PSUR data lock",
        "domain": "Pharmacology, Pharmacoepidemiology & Safety",
        "subdomain": "other: time-to-onset characterisation of identified risks for routine risk minimisation",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "14 (cuts of a distribution): the 80 and 95 per cent months of six identified risks, the ILD 95 per cent month as the call, with reporting rates and the exposure under them",
        "as_of": "2026-10-06",
        "deliverables": ["rmp_monitoring_windows_2027.xlsx", "onset_windows_by_risk.svg"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "referee_file": P.FILES[P.REFEREE],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task254/generator/make.py (seeded, deterministic) around a fictional "
                               "marketing authorisation holder (Ravnsborg Pharma A/S) and product (Lyrevo, RVB-417); MedDRA preferred "
                               "terms, ISO country codes and national article code formats are used as published; no real patient, "
                               "case, laboratory, wholesaler or hospital is depicted.",
                     "date": "2026-10-06", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task254/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 6, 16, 5, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    with zipfile.ZipFile(zp) as z:
        names = z.namelist()
        assert names == sorted(os.listdir(TARGET)), names
        for n in names:
            assert z.read(n) == open(os.path.join(TARGET, n), "rb").read(), n
    return zp


def main(quick=False):
    world = TG.write(TARGET)
    g = DL.main(TARGET, GOLDEN)
    # H1: no writer's name and no stamp outside the setting, in the pack and in the deliverables
    import subprocess
    for folder, ceiling in ((TARGET, "2026-10-06"), (GOLDEN, "2026-10-07")):
        rc = subprocess.run([sys.executable, TG.SCRUB, folder, "--floor", "2023-01-01", "--ceiling", ceiling],
                            capture_output=True, text=True)
        assert rc.returncode == 0, rc.stdout + rc.stderr
    meta = metadata()
    assert meta["input_gates"]["files"] >= 10 and len(meta["input_gates"]["formats"]) >= 3
    assert meta["input_gates"]["largest_file_rows"] >= 25000 and len(meta["distractor_files"]) >= 2
    ck, g2 = CK.run(TARGET, world, quick=quick)
    print("checks: %d assertions passed" % ck.n)
    v = V.main(TARGET, GOLDEN)
    assert v["windows"] == g2["windows"], (v["windows"], g2["windows"])
    assert v["golden_workbook_rows_checked"] == 12
    for r in v["rates"]:
        for w in ("launch", "interval"):
            assert v["rates"][r][w] == round(g2["rates"][r][w] + 1e-9, 1), (r, w)
    assert v["py"]["launch"] == int(round(g2["py"]["launch"] / 10.0)) * 10
    assert v["py"]["interval"] == int(round(g2["py"]["interval"] / 10.0)) * 10
    assert v["ild_rungs"] == {"drop2026": [8, 18], "year": [8, 19]}, v["ild_rungs"]
    print("independent verifier: windows, rates, patient-years, ILD rungs and the golden workbook agree")
    tmp = tempfile.mkdtemp()
    try:
        t2, g2d = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        TG.write(t2, quiet=True)
        DL.main(t2, g2d)
        d1, d2 = digest(TARGET), digest(t2)
        bad = [f for f in d1 if d1[f] != d2.get(f)]
        gd1, gd2 = digest(GOLDEN), digest(g2d)
        badg = [f for f in gd1 if gd1[f] != gd2.get(f)]
    finally:
        shutil.rmtree(tmp)
    if bad or badg:
        raise SystemExit("second build differs: %s %s" % (bad, badg))
    print("two builds byte-identical (%d target files, %d golden files)" % (len(d1), len(gd1)))
    zp = cut_zip()
    print("zip:", zp)
    with zipfile.ZipFile(zp) as z:
        members = z.namelist()
    sub_path = os.path.join(TASK, "submission.md")
    if os.path.exists(sub_path):
        # H19: every file the write-up names is in the archive or among the deliverables
        sub = open(sub_path, encoding="utf-8").read()
        named = set(re.findall(r"`([^`]+\.(?:csv|xlsx|pdf|docx|xml|txt|svg))`", sub))
        named |= set(re.findall(r"^### (\S+\.(?:xlsx|svg))$", sub, re.M))
        for f in named:
            assert f in members or f in meta["deliverables"], f
        print("write-up names %d files, every one shipped" % len(named))
    assert sorted(os.listdir(GOLDEN)) == sorted(meta["deliverables"]), os.listdir(GOLDEN)
    # H11: one live write-up and one prompt anywhere in the task tree
    for name in ("submission.md", "prompt.md"):
        hits = [os.path.join(dp, f) for dp, _, fs in os.walk(TASK) for f in fs if f == name]
        assert len(hits) <= 1, hits
    print("receipt: target.zip %d bytes, %d members, sha256 %s" % (
        os.path.getsize(zp), len(members), hashlib.sha256(open(zp, "rb").read()).hexdigest()))
    for k, v in ck.rec.items():
        print("record:", k, v)
    return ck, g2


if __name__ == "__main__":
    main(quick="--quick" in sys.argv)
