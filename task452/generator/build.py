"""Builds task452 twice, asserts the two builds byte-identical, and installs target/, golden/, figures.json,
metadata.json, submission.md and target.zip.

    python3 task452/generator/build.py
"""
import datetime as dt
import filecmp
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as C          # noqa: E402
import golden               # noqa: E402
import pack                 # noqa: E402
import truth                # noqa: E402
import writeup              # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_TIME = dt.datetime(2027, 1, 11, 9, 0, tzinfo=dt.timezone.utc).timestamp()
ZIP_TIME = (2027, 1, 11, 9, 0, 0)


PRODUCERS = {  # each document's issuing body and its own date (H1, H13)
    "IEL-1186-03_conditions_consolidated_2026.pdf": ("Licensing Unit", "2026-06-30"),
    "stack_tests_Hg_2024-2026.pdf": ("Ardcarn Emissions Monitoring Ltd", "2026-10-20"),
    "production_ledger_2026.xlsx": ("Production Accounting", "2027-01-07"),
    "QC_lab_composites_2026.xlsx": ("QC Laboratory", "2027-01-08"),
    "site_register_2026.xlsx": ("Environment and Quality", "2026-03-02"),
    "kiln_mercury_memo_2026.pdf": ("Environment and Quality", "2027-01-11"),
    "kiln_emissions_2026.xlsx": ("Environment and Quality", "2027-01-11"),
}


def scrub(d):
    sys.path.insert(0, os.path.join(TASK, "..", ".claude", "skills", "reduce-house-fixes", "scripts"))
    import scrub_producer_metadata as S
    for fn in sorted(os.listdir(d)):
        if fn in PRODUCERS:
            prod, stamp = PRODUCERS[fn]
            f = S.scrub_pdf if fn.endswith(".pdf") else S.scrub_ooxml
            f(os.path.join(d, fn), prod, stamp, floor="2024-01-01", ceiling="2027-01-11")


def one_build(root):
    t = truth.build_truth()
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    pack.write_pack(t, tgt)
    res = golden.write_golden(tgt, gld)
    scrub(tgt)
    scrub(gld)
    for d in (tgt, gld):
        for fn in os.listdir(d):
            os.utime(os.path.join(d, fn), (EXPORT_TIME, EXPORT_TIME))
    return t, res


def same_tree(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    assert fa == fb, (fa, fb)
    for fn in fa:
        assert filecmp.cmp(os.path.join(a, fn), os.path.join(b, fn), shallow=False), "differs: %s" % fn
    return len(fa)


def metadata(files):
    prov = {
        "IEL-1186-03_conditions_consolidated_2026.pdf": "the installation's consolidated licence conditions after the 2026 review (extract)",
        "PI_historian_K1K2_2026_30min.csv": "the plant historian's half-hour export for both kiln lines, calendar 2026",
        "CEMS_logger_A1-1_A1-2_May2026.csv": "the stack analysers' own data logger export for May 2026",
        "DCS_event_journal_2026.txt": "the control system's alarm and event journal for 2026",
        "production_ledger_2026.xlsx": "the works' monthly production and materials ledger, 2026",
        "QC_lab_composites_2026.xlsx": "the quality laboratory's composite analyses, 2026",
        "weighbridge_byproducts_2026.csv": "the weighbridge's by-product dispatch tickets, 2026",
        "stack_tests_Hg_2024-2026.pdf": "the accredited contractor's annual mercury test reports, 2024 to 2026",
        "site_register_2026.xlsx": "the site's register of emission points and plant",
        "fuel_receipts_2026.csv": "fuel receipts with the suppliers' certificate values, 2026",
        "quarry_extraction_2026.csv": "the quarry's daily haulage to the crusher, 2026",
    }
    out = {
        "task": "task452",
        "title": "Kilcarrow Works: mercury to air in 2026 against the annual load from 2028",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "Physical & Environmental Sciences",
        "decision": "whether the works keeps under the annual mercury load from 2028 at its 2026 release, and the 2026 figures for its annual report",
        "deliverables": ["kiln_mercury_memo_2026.pdf", "kiln_emissions_2026.xlsx"],
        "distractor_files": ["target/fuel_receipts_2026.csv", "target/quarry_extraction_2026.csv",
                             "target/weighbridge_byproducts_2026.csv"],
        "distractor_reasons": {
            "target/quarry_extraction_2026.csv": "haulage from the quarry faces to the crusher: 1.69 Mt of limestone hauled in 2026 against 2.15 Mt of limestone in the production records, and not split by kiln line, so it gives neither kiln's raw material intake",
            "target/fuel_receipts_2026.csv": "fuel purchases with the suppliers' certificates, by consignment received rather than by fuel fired, and not split by kiln line",
            "target/weighbridge_byproducts_2026.csv": "by-product dispatches off site (filter dust, refractory waste, scrap), by ticket and truck rather than by kiln line or month of production",
        },
        "as_of": "2027-01-11",
        "files": [],
    }
    for fn in sorted(files):
        out["files"].append({"path": "target/" + fn, "content": prov[fn],
                             "source": "synthetic: constructed by the task generator (fixed seed) in the layout of the named system's export",
                             "date": "2027-01-11", "licence": "CC0 1.0 (constructed for this task)"})
    return out


def make_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, fn), "rb") as f:
                z.writestr(zi, f.read())


def main():
    tmp = tempfile.mkdtemp(prefix="t452_")
    try:
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        os.makedirs(a)
        os.makedirs(b)
        t, res = one_build(a)
        one_build(b)
        n1 = same_tree(os.path.join(a, "target"), os.path.join(b, "target"))
        n2 = same_tree(os.path.join(a, "golden"), os.path.join(b, "golden"))
        print("two builds byte-identical: %d target files, %d golden files" % (n1, n2))
        for d in ("target", "golden"):
            dst = os.path.join(TASK, d)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(os.path.join(a, d), dst)
            for fn in os.listdir(dst):
                os.utime(os.path.join(dst, fn), (EXPORT_TIME, EXPORT_TIME))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tgt = os.path.join(TASK, "target")
    res = golden.compute(tgt)
    figs = golden.figures(res)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(os.listdir(tgt)), f, indent=1)
    writeup.write(figs, os.path.join(TASK, "submission.md"))
    make_zip(tgt, os.path.join(TASK, "target.zip"))
    import hashlib
    print("target.zip md5", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    print(json.dumps(figs, sort_keys=True))


if __name__ == "__main__":
    main()
