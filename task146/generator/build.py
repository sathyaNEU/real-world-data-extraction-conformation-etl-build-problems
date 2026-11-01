"""Build task146's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip, then run the checks and the verifier.

    python3 task146/generator/build.py            # the full build
    python3 task146/generator/build.py --pack DIR # the data and documents alone, into DIR
"""
import datetime as dt
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pack as PK    # noqa: E402
import world as W    # noqa: E402

ZIP_STAMP = (2026, 12, 3, 9, 20, 0)
XLSX_STAMPS = {"products": (dt.datetime(2019, 2, 11, 10, 4), dt.datetime(2025, 7, 1, 8, 31)),
               "swaps": (dt.datetime(2024, 1, 29, 15, 12), dt.datetime(2026, 12, 2, 16, 47))}


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    f = lambda k: os.path.join(out, PK.FILES[k])
    w = W.World()
    n = {}
    n["balances"] = PK.balances(w, f("balances"))
    n["events"] = PK.events(w, f("events"))
    PK.products(f("products"), XLSX_STAMPS["products"])
    PK.swaps(f("swaps"), XLSX_STAMPS["swaps"])
    n["bonds"] = PK.bonds(w, f("bonds"))
    PK.rates(f("rates"))
    PK.isa_in(f("isa_in"))
    try:
        import docs as DO
        DO.policy(f("policy"))
        DO.minutes(f("minutes"))
        DO.email(f("email"))
    except ImportError:
        pass
    return w, n


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for name in sorted(files):
            p = os.path.join(root, name)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def full(out_task):
    target = os.path.join(out_task, "target")
    golden = os.path.join(out_task, "golden")
    for d in (target, golden):
        if os.path.isdir(d):
            shutil.rmtree(d)
    build_pack(target)
    import deliver as DL
    import writeup as WU
    res = DL.goldens(target, golden)
    WU.write(target, res, out_task)
    return digest(target), digest(golden), open(os.path.join(out_task, "submission.md"), "rb").read()


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(name, ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, name), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--pack":
        build_pack(sys.argv[2])
        sys.exit(0)
    a = full(TASK)
    with tempfile.TemporaryDirectory() as tmp:
        b = full(tmp)
    same = a == b
    print("two builds byte-identical:", same)
    if not same:
        sys.exit(1)
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    print("target.zip", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rc2 = subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    sys.exit(rc or rc2)
