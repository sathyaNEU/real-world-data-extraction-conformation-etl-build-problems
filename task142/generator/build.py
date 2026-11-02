"""Builds task142 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
generator/figures.json, metadata.json, target.zip and submission.md.

    python3 task142/generator/build.py
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
import deliver as GD  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402

SOURCES = {
    "amr": "Stadswarmte Lekstede AMR head-end, daily heat meter export for Warmtenet West, meter year 2025-26 (UTC days)",
    "register": "Stadswarmte Lekstede Netbeheer, connection register with meter history, 1 October 2026",
    "weather": "Stadswarmte Lekstede weather station LKS, daily mean, minimum and maximum temperature, 2025-26",
    "scada": "OS West station SCADA, hourly flow, temperatures, heat and pump power (UTC), 2025-26",
    "schedule": "Woonstichting Weidehaven, phasing schedule of the aardgasvrij programme, 30 September 2026",
    "revised": "Hoogland & Brak bouwfysica, design heat loss under NEN-EN 12831, revision 2, 18 September 2026",
    "prelim": "Hoogland & Brak bouwfysica, design heat loss, concept of 27 March 2026",
    "hydraulic": "Stadswarmte Lekstede Network Planning, hydraulic test OS West 2026-27, 9 October 2026",
    "procedure": "Stadswarmte Lekstede Network Planning, capacity test for new connections CT-03 v3",
    "scope": "Woonstichting Weidehaven and Stadswarmte Lekstede, scope of works aardgasvrij 2027-2028, v1.2",
    "gasreads": "Gasnet Lekstede, monthly telemetry reads of the Weidehaven boiler-room gas meters, 2025-26",
    "gasmaster": "Gasnet Lekstede, connection and meter master data for the Weidehaven boiler rooms, 1 October 2026",
    "tariff": "Stadswarmte Lekstede, heat tariff sheet 2026",
    "legacy": "Stadswarmte Lekstede drive-by reading system, monthly heat meter reads, October 2024 to September 2025",
}


def metadata(n):
    return {
        "task": "task142", "architecture": 2, "as_of": P.ASOF.isoformat(),
        "decision": "the first heating season (2027-28, 2028-29 or neither) in which OS West runs short of design-day "
                    "flow as the Weidehaven blocks connect to Warmtenet West",
        "deliverables": [GD.BOOK],
        "files": {P.FILES[k]: {"source": SOURCES[k] + "; synthetic, built for this task", "date": P.ASOF.isoformat(),
                               "license": "synthetic, CC0",
                               "role": "distractor" if k in P.DISTRACTORS else "evidence"} for k in P.FILES},
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "stated_inputs": ["167", "1,120", "953", "1.163", "90/50", "90", "0"],
        "distractor_notes": {
            P.FILES["prelim"]: "the consultant's concept design heat losses, superseded by revision 2 under CT-03 3.4; "
                               "relevant to the loads, unused by the solution",
            P.FILES["tariff"]: "the 2026 heat tariffs; relevant to the programme's economics, unused by the solution",
            P.FILES["scada"]: "the station's hourly operating record; relevant to the station's load, unused by the "
                              "solution",
        },
        "largest_file": {"name": P.FILES["amr"], "rows": n["amr"]},
        "row_counts": {P.FILES[k]: (v if isinstance(v, int) else list(v)) for k, v in sorted(n.items()) if k in P.FILES},
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
    w, n = PK.build(target)
    GD.write_all(target, golden, gen)
    with open(os.path.join(base, "metadata.json"), "w") as fh:
        json.dump(metadata(n), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=GD.STAMP)
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
