"""task482 architecture 16: build the pack, the goldens, figures.json, submission.md and metadata.json; rebuild into a
scratch folder and require byte-identical output; cut target.zip; then run the checks and the independent verifier.

    python3 task482/generator/make.py
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B     # noqa: E402
import deliver as DL  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMPS = {"brackwell_site_gas_meter_2026.csv": (2027, 1, 12, 9, 4, 18),
          "brackwell_gas_invoices_2026.pdf": (2027, 1, 12, 10, 40, 2),
          "brackwell_melting_furnace_logs_2026.xlsx": (2027, 1, 19, 15, 22, 40),
          "brackwell_homogenizing_furnace_h1_2026.csv": (2027, 1, 18, 11, 7, 34),
          "brackwell_heat_treatment_oven_t1_2026.csv": (2027, 1, 18, 11, 9, 6),
          "brackwell_production_lots_2026.csv": (2027, 1, 15, 8, 51, 12),
          "velden_scr2_supplier_carbon_requirement.pdf": (2025, 12, 8, 14, 3, 0),
          "velden_2027_calloff_schedule.xlsx": (2026, 12, 14, 8, 47, 30),
          "brackwell_scr2_data_package.eml": (2027, 1, 21, 16, 12, 0),
          "brackwell_works_weather_2026.csv": (2027, 1, 5, 7, 30, 54),
          "brackwell_weighbridge_2026.csv": (2027, 1, 8, 13, 16, 26),
          "brackwell_scrap_goods_in_2026.csv": (2027, 1, 8, 13, 40, 8),
          "brackwell_electricity_hh_2026.csv": (2027, 1, 11, 9, 58, 44),
          "brackwell_plant_asset_register.xlsx": (2026, 9, 22, 14, 36, 10),
          "brackwell_shift_roster_2026.csv": (2025, 12, 15, 10, 21, 52)}


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def one(target, golden, extra, here):
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    B.build(target)
    fig, res = DL.write_all(target, golden, here)
    WU.submission(fig, res, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"))
    return digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read(), \
        open(os.path.join(here, "figures.json"), "rb").read()


def main():
    t1 = one(TARGET, GOLDEN, TASK, HERE)
    with tempfile.TemporaryDirectory() as tmp:
        t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp, tmp)
    same = t1 == t2
    print("byte-identical rebuild: target %s, golden %s, submission %s, figures %s" % tuple(
        a == b for a, b in zip(t1, t2)))
    if not same:
        sys.exit(1)
    assert sorted(STAMPS) == sorted(os.listdir(TARGET)), sorted(set(STAMPS) ^ set(os.listdir(TARGET)))
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMPS[f])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    sys.exit(rc)


if __name__ == "__main__":
    main()
