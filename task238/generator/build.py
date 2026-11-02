"""Builds task238 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
generator/figures.json, metadata.json, target.zip and submission.md.

    python3 task238/generator/build.py
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
import golden as GD  # noqa: E402
import pack as M  # noqa: E402
import params as P  # noqa: E402

ZIPTIME = (2027, 1, 15, 16, 30, 0)
SOURCES = {
    "standard": "Saltmarsh Market Store Operations, Price Integrity Standard PI-2 revision 3 (approved 18 September "
                "2026); synthetic",
    "hourly": "Saltmarsh Market POS host, item scans by store, business date and hour, Q4 2026; synthetic",
    "movement": "Saltmarsh Market Pricing analytics, price-changed item movement on each changeover Thursday and "
                "the Thursday before, Q4 2026; synthetic",
    "printer": "Saltmarsh Market printer fleet console, shelf-edge label printer jobs, 1 October to 31 December "
               "2026; synthetic",
    "checks": "Saltmarsh Market Price Integrity, Thursday changeover check handheld export, Q4 2026; synthetic",
    "audits": "Saltmarsh Market Price Integrity, weekly random price audit results, Q4 2026; synthetic",
    "stores": "Saltmarsh Market Store Operations, store directory, January 2027; synthetic",
    "desk": "Saltmarsh Market Customer Service, service desk adjustments, Q4 2026; synthetic",
    "overrides": "Saltmarsh Market POS host, register price overrides, 2026-10-01T00:00Z to 2027-01-01T00:00Z; "
                 "synthetic",
    "adplan": "Saltmarsh Market Merchandising, weekly flyer ad plan, flyer weeks starting 1 October to 31 December "
              "2026; synthetic",
    "pricefile": "Saltmarsh Market Pricing, weekly price change releases (preliminary and revised), Q4 2026; "
                 "synthetic",
    "adsales": "Saltmarsh Market Merchandising, flyer item units by price zone and day, flyer weeks starting 1 "
               "October to 31 December 2026; synthetic",
    "corrections": "Saltmarsh Market Pricing, mid-week price corrections, Q4 2026; synthetic",
    "contacts": "Saltmarsh Market Customer Care, contacts mentioning a store, Q4 2026; synthetic",
    "markdowns": "Saltmarsh Market store systems, clearance markdown tags printed, Q4 2026; synthetic",
}


def metadata(n):
    return {
        "task": "task238", "architecture": 2, "as_of": P.ASOF.isoformat(),
        "decision": "which Saltmarsh Market stores go on Price Watch for the first quarter of 2027 under the price "
                    "integrity standard, from their fourth-quarter 2026 price accuracy",
        "deliverables": [GD.BOOK, GD.CHART],
        "files": {P.FILES[k]: {"source": SOURCES[k], "date": P.PULL.isoformat(), "license": "synthetic, CC0",
                               "role": "distractor" if k in P.DISTRACTORS else "evidence"} for k in P.FILES},
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "distractor_notes": {
            P.FILES["contacts"]: "customer care contacts by store and category over the quarter; relevant to price "
                                 "integrity, unused by the solution",
            P.FILES["markdowns"]: "clearance markdown tags printed at each store; relevant to shelf labels, unused "
                                  "by the solution",
        },
        "stated_inputs": ["99.0"],
        "largest_file": {"name": P.FILES["movement"], "rows": n["movement"]},
        "row_counts": {P.FILES[k]: v for k, v in sorted(n.items()) if k in P.FILES},
    }


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = (os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen"))
    w, n = M.build(target)
    GD.write_all(target, golden, gen)
    with open(os.path.join(base, "metadata.json"), "w") as fh:
        json.dump(metadata(n), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIPTIME)
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
    import writeup
    writeup.main()
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
