#!/usr/bin/env python3
"""task128 generator. Builds the evidence pack into <out>/target, the golden deliverables into
<out>/golden, and <out>/metadata.json, then scrubs container metadata and normalises mtimes.

    python3 build.py --out /path/to/task128 [--record /path/to/record.json]
"""
import argparse
import datetime as dt
import importlib.util
import json
import os
import shutil
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRUB = os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")

import world as WORLD
import writers_data as WD
import docs as DOC
import deliver as DEL
from params import SEED, ESTATES, COLO, CLOUD, AS_OF, EXPORT_TIME, ORG
import checks as CHECKS


def load_scrub():
    spec = importlib.util.spec_from_file_location("scrub_producer_metadata", SCRUB)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def write_all(W, out):
    target = os.path.join(out, "target")
    golden = os.path.join(out, "golden")
    for d in (target, golden):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    p = lambda f: os.path.join(target, f)
    g = lambda f: os.path.join(golden, f)
    info = {}
    info["spine"] = WD.write_spine(p(WD.SPINE), W)
    info["history"] = WD.write_history(p(WD.HISTORY), W)
    info["feed"] = WD.write_feed(p(WD.FEED), W)
    info["inv"] = WD.write_inventory(p(WD.INVENTORY), W)
    WD.write_capreg(p(WD.CAPREG), W)
    info["fc"] = WD.write_forecast(p(WD.FORECAST), W, SEED)
    info["acks"] = WD.write_acks(p(WD.ACKS), W)
    WD.write_ticketlog(p(WD.TICKETLOG), W)
    WD.write_fixed(p(WD.FIXEDF), W)
    info["dep"] = WD.write_deploylog(p(WD.DEPLOYLOG), W["deployments"])
    info["asset"] = WD.write_assetreg(p(WD.ASSETREG), W["assets"])
    info["cov"] = WD.write_coverage(p(WD.COVERAGE), W["coverage"])
    WD.write_advisory(p(WD.ADVISORY), W["deployments"])
    WD.write_novcal(p(WD.NOVCAL))
    WD.write_draintool(p(WD.DRAINTOOL))
    DOC.write_standard(p(DOC.STANDARD))
    DOC.write_sre(p(DOC.SRE))
    DOC.write_schedule(p(DOC.SCHEDULE), W)
    DOC.write_closeout(p(DOC.CLOSEOUT), W)
    DOC.write_memo(p(DOC.MEMO))
    DOC.write_thread(p(DOC.THREAD))
    DOC.write_dict(p(DOC.DICT))
    DOC.write_provenance(p(DOC.PROVENANCE), info)
    # golden deliverables
    rows = DEL.write_cut(g(DEL.CUT), W)
    DEL.write_deck(g(DEL.DECK), W, rows)
    return target, golden, info


def scrub_and_stamp(target, golden):
    scrub = load_scrub()
    floor, ceiling = "2026-10-20", "2026-10-25"
    for d in (target, golden):
        for f in sorted(os.listdir(d)):
            path = os.path.join(d, f)
            ext = os.path.splitext(f)[1].lower()
            if ext in (".pdf",):
                scrub.scrub_pdf(path, ORG, "2026-10-23", floor, ceiling)
            elif ext in (".docx", ".xlsx", ".pptx"):
                scrub.scrub_ooxml(path, ORG, "2026-10-23", floor, ceiling)
    for d in (target, golden):
        for f in sorted(os.listdir(d)):
            if os.path.splitext(f)[1].lower() in (".xlsx", ".docx", ".pptx"):
                _fix_zip_times(os.path.join(d, f))
    stamp = EXPORT_TIME.timestamp()
    for d in (target, golden):
        for f in os.listdir(d):
            os.utime(os.path.join(d, f), (stamp, stamp))


import re as _re
_ISO = _re.compile(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ")
_FIXED = (2026, 10, 23, 6, 0, 0)
_FIXED_ISO = b"2026-10-23T06:00:00Z"


def _norm_ooxml_bytes(raw):
    """Return OOXML bytes with fixed member order/timestamps and every ISO datetime pinned, so a
    nested embedded workbook (a chart's data) is byte-stable across builds."""
    import io, zipfile
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
        for i, b in items:
            if i.filename.startswith("docProps/") or i.filename.endswith(".xml"):
                b = _ISO.sub(_FIXED_ISO, b)
            zi = zipfile.ZipInfo(i.filename, date_time=_FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = i.external_attr
            zi.create_system = 0
            zo.writestr(zi, b)
    return buf.getvalue()


def _fix_zip_times(path):
    """Rewrite an OOXML archive byte-stable, normalising any nested embedded OOXML too."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = [(i, z.read(i.filename)) for i in infos]
    tmp = path + ".zt"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for i, b in data:
            if i.filename.endswith((".xlsx", ".docx", ".pptx")):
                b = _norm_ooxml_bytes(b)
            zi = zipfile.ZipInfo(i.filename, date_time=_FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = i.external_attr
            zi.internal_attr = i.internal_attr
            zi.create_system = 0
            zo.writestr(zi, b)
    os.replace(tmp, path)


def write_metadata(out, W, info):
    tickets = DEL.G.answer_tickets(W)
    split = W["answer_split"]
    meta = {
        "task": "task128",
        "title": "Sendalia Viajes, November 2026 patch ticket split across six estates",
        "domain": "Business & Operations Analytics",
        "subdomain": "field-service-maintenance",
        "objective": "Opportunity Sizing & Decision Support",
        "as_of": AS_OF.isoformat(),
        "deliverables": [DEL.CUT, DEL.DECK],
        "answer": {
            "split": {e: split[e] for e in ESTATES},
            "exposures_taken_out": {e: W["figs"][e] for e in ESTATES},
            "total_exposures": W["figs"]["_total"],
        },
        "input_files": sorted(os.listdir(os.path.join(out, "target"))),
        "large_file": {"path": WD.SPINE, "rows": info["spine"]},
        "distractor_files": [WD.DRAINTOOL, DOC.MEMO],
    }
    with open(os.path.join(out, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--record")
    a = ap.parse_args()
    W = WORLD.build_world()
    target, golden, info = write_all(W, a.out)
    scrub_and_stamp(target, golden)
    meta = write_metadata(a.out, W, info)
    n = CHECKS.run(W, a.out, info, meta)
    print(f"task128 built: {len(meta['input_files'])} input files, spine {info['spine']:,} rows, "
          f"{n} assertions passed")
    if a.record:
        rec = {"figs": W["figs"], "split": {e: W["answer_split"][e] for e in ESTATES},
               "rungs": {k: (v[0], v[1]) for k, v in W["rungs"].items() if k.startswith("R")},
               "assertions": n}
        with open(a.record, "w") as f:
            json.dump(rec, f, indent=2, default=str)


if __name__ == "__main__":
    main()
