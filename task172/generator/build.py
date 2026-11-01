"""Build task172's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip, then run the checks and the verifier.

    python3 task172/generator/build.py            # the full build
    python3 task172/generator/build.py --pack DIR # the pack alone, into DIR (for development)
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import docs as D     # noqa: E402
import pack as PK    # noqa: E402
import records as RC  # noqa: E402
import world as W    # noqa: E402

ZIP_STAMP = (2026, 12, 2, 8, 40, 0)
SOURCES = {
    "charter": "the trials unit's data monitoring committee charter",
    "sap": "the trials unit's statistical analysis plan",
    "schedule": "the funder's research funding agreement, Schedule 2",
    "irt_rand": "the interactive response technology's randomisation export",
    "bicr": "the blinded independent central review vendor's timepoint transfer",
    "inv": "the electronic data capture system's investigator tumour assessment pages",
    "status": "the electronic data capture system's baseline, disposition and death pages",
    "screening": "the trials unit's central screening log",
    "pv": "the pharmacovigilance safety database's line listing",
    "ae": "the electronic data capture system's adverse event pages",
    "central": "the central laboratory's cumulative data transfer",
    "local": "the electronic data capture system's local laboratory pages",
    "samples": "the electronic data capture system's central laboratory sample tracking page",
    "exposure": "the electronic data capture system's study drug administration pages",
    "irt_admin": "the interactive response technology's drug administration log",
    "sites": "the trials unit's site register",
}
STAMPS = {"status": ("2026-12-01T17:42:10Z", "2026-12-01T17:58:31Z"),
          "pv": ("2026-12-01T09:05:44Z", "2026-12-01T09:21:02Z")}
FILE_TIMES = {"charter": (2026, 3, 3, 16, 40), "sap": (2026, 2, 11, 14, 19), "schedule": (2025, 10, 14, 10, 33),
              "sites": (2026, 9, 30, 11, 2)}


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    f = lambda k: os.path.join(out, PK.FILES[k])
    w = W.World()
    R = RC.Records(w)
    n = {}
    n["irt_rand"] = PK.irt_rand(R, f("irt_rand"))
    n["bicr"] = PK.bicr(R, f("bicr"))
    n["inv"] = PK.inv(R, f("inv"))
    PK.status(R, f("status"), STAMPS["status"])
    n["screening"] = PK.screening(R, f("screening"))
    n["pv"] = PK.pv(R, f("pv"), STAMPS["pv"])
    n["ae"] = PK.ae(R, f("ae"))
    n["central"] = PK.central(R, f("central"))
    n["local"] = PK.local(R, f("local"))
    n["samples"] = PK.samples(R, f("samples"))
    n["exposure"] = PK.exposure(R, f("exposure"))
    n["irt_admin"] = PK.irt_admin(R, f("irt_admin"))
    PK.sites(R, f("sites"))
    D.charter(f("charter"))
    D.sap(f("sap"))
    D.schedule(f("schedule"))
    for k in PK.FILES:
        t = dt.datetime(*(FILE_TIMES.get(k) or (2026, 12, 1, 18, 5))).timestamp()
        os.utime(f(k), (t, t))
    return w, R, n


def metadata(w, n):
    return {"task": "task172", "architecture": 2, "as_of": w.cut.isoformat(), "snapshot": w.snapshot.isoformat(),
            "files": {PK.FILES[k]: {"source": SOURCES[k], "date": w.snapshot.isoformat() if k not in FILE_TIMES else
                                    dt.date(*FILE_TIMES[k][:3]).isoformat(), "license": "synthetic, CC0",
                                    "role": "distractor" if k in PK.DISTRACTORS else "evidence"} for k in PK.FILES},
            "distractors": {PK.FILES["inv"]: "the investigators' own tumour reads: progression-free survival is assessed "
                                              "by the blinded independent central review, so these reads decide nothing",
                            PK.FILES["ae"]: "the EDC adverse event pages: serious adverse events are counted from the "
                                             "pharmacovigilance database, so this listing decides nothing"},
            "largest_file": {"name": PK.FILES["central"], "rows": n["central"]},
            "deliverables": ["talon2_interim_recommendation.pdf", "talon2_interim_tables.csv"]}


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    import golden as GD  # noqa: E402
    target, golden = os.path.join(base, "target"), os.path.join(base, "golden")
    w, R, n = build_pack(target)
    fig = GD.write_all(target, golden, base)
    json.dump(fig, open(os.path.join(base, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(w, n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base), fig


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--pack":
        w, R, n = build_pack(sys.argv[2])
        print("pack written:", sys.argv[2], n, "cut", w.cut)
        return
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    ha, fig = one_build(a)
    hb, _ = one_build(b)
    same = ha == hb
    print("two builds byte-identical:", same, "(%d files)" % len(ha))
    if not same:
        for k in sorted(set(ha) | set(hb)):
            if ha.get(k) != hb.get(k):
                print("  differs:", k)
        sys.exit(1)
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.rmtree(a)
    shutil.rmtree(b)
    zp = os.path.join(TASK, "target.zip")
    cut_zip(os.path.join(TASK, "target"), zp)
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    print("call", fig["call"], "conditional power", fig["cp_golden"])
    for script in ("checks.py", "verify.py"):
        p = os.path.join(HERE, script)
        if os.path.exists(p):
            rc = subprocess.call([sys.executable, p])
            print(script, "exit", rc)
            if rc:
                sys.exit(rc)


if __name__ == "__main__":
    main()
