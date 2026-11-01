"""Builds task255 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
figures.json, metadata.json and target.zip.

    python3 task255/generator/build.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import asks_world as AW  # noqa: E402
import golden as GD  # noqa: E402
import io_util as IO  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

SOURCES = {
    "journeys": ("Ravelmondse Vervoerbedrijf data warehouse, OV-chipkaart metro journeys 1 October to 4 November "
                 "2026 as re-exported on 5 November 2026; synthetic, constructed for this task"),
    "network": "Ravelmondse Vervoerbedrijf metro network planning model 2026; synthetic",
    "products": "Ravelmondse Vervoerbedrijf product code list; synthetic",
    "rate_card": "Spoorbeeld Media rate card 2027 for the Ravelmond metro, version 1.0 of 10 November 2026; synthetic",
    "terms": "Spoorbeeld Media general terms 2026 for metro screen advertising; synthetic",
    "register": "Spoorbeeld Media screen register as kept by screen operations, state of 12 November 2026; synthetic",
    "cms": "Spoorbeeld Media content management system, player event log 1 October to 4 November 2026; synthetic",
    "bookings": "Spoorbeeld Media autumn 2026 bookings workbook kept by sales; synthetic",
    "legacy": "Spoorbeeld Media legacy invoicing system, 2026 invoices to its close on 14 October 2026; synthetic",
    "billing": "Spoorbeeld Media billing system export, documents 15 October to 12 November 2026; synthetic",
    "statements": "Agency commission statements of 31 October 2026, as received and scanned; synthetic",
    "ridership": "Ravelmondse Vervoerbedrijf published monthly boardings by stop, January to September 2026; synthetic",
    "survey": "Passenger survey of the Ravelmond metro, third quarter 2026, by an outside agency; synthetic",
    "benchmark": "Industry benchmark of digital transit screens in Dutch city networks, September 2026; synthetic",
}


def metadata(n):
    return {
        "task": P.TASK, "architecture": 2, "as_of": P.AS_OF.isoformat(),
        "decision": "which of the concessionaire's metro screen packages are sold in the guaranteed-reach tier "
                    "(Tier G) of its 2027 rate card",
        "deliverables": [GD.BOOK, GD.PAGE],
        "files": {PK.FILES[k]: {"source": SOURCES[k], "date": P.AS_OF.isoformat(), "license": "synthetic, CC0",
                                "role": "distractor" if k in PK.DISTRACTORS else "evidence"} for k in PK.FILES},
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "stated_inputs": [b[0].split("-")[-1] for b in AW.BOOKINGS],
        "largest_file": {"name": PK.FILES["journeys"], "rows": n["journeys"]},
        "row_counts": {PK.FILES[k]: v for k, v in sorted(n.items())},
    }


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen")
    os.makedirs(target, exist_ok=True)
    w = W.build(P.SEED)
    n = PK.build_all(w, target)
    GD.write_all(target, golden, gen)
    json.dump(metadata(n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=IO.ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    da, db = one_build(a), one_build(b)
    if da != db:
        bad = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        print("NOT byte-identical:", bad)
        sys.exit(1)
    print("two builds byte-identical over %d files" % len(da))
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "gen", "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    import writeup
    writeup.main()
    print("submission.md written")
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
