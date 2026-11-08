"""Build task184: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks, the independent verifier and the ceiling; then a second full build into a
scratch folder compared byte for byte; then target.zip from the final build.

    python3 task184/generator/build.py              everything
    python3 task184/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
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
sys.path.insert(0, HERE)
import docs as DOCS          # noqa: E402
import pack as P             # noqa: E402
import postprocess as PP     # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = dt.datetime(2027, 2, 15, 6, 41, 0).timestamp()


def build_pack(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    app, paper = P.returns_rows()
    n["app"] = P._csv(p("app"), P.APP_HEADER, app)
    n["paper"] = P._csv(p("paper"), P.PAPER_HEADER, paper, crlf=True)
    n["flocks"] = P._csv(p("flocks"), P.FLOCK_HEADER, P.flock_rows())
    kh, lw = P.hatchery_rows()
    n["kh"] = P._csv(p("kh"), P.KH_HEADER, kh, crlf=True)
    n["lw"] = P._csv(p("lw"), P.LW_HEADER, lw)
    n["catch"] = P._csv(p("catch"), P.CATCH_HEADER, P.catch_rows(), crlf=True)
    lds = P.loads()
    n["intake"] = P._csv(p("intake"), P.INTAKE_HEADER, P.intake_rows(lds))
    l2 = P.line2_rows(lds)
    with open(p("line2"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"system": "Riverside line control", "line": 2, "export": "loads",
                   "from": "2027-01-04", "to": "2027-01-31", "loads": [{k: v for k, v in r.items() if k != "line"}
                                                                       for r in l2]}, fh, indent=1)
        fh.write("\n")
    n["line2"] = len(l2)
    n["wild"] = P._csv(p("wild"), P.WILD_HEADER, P.wild_rows())
    n["weather"] = P._csv(p("weather"), P.WEATHER_HEADER, P.weather_rows())
    reg = P.farm_register_rows()
    DOCS.write_farm_register(p("farms"), P.FARM_HEADER, reg)
    n["farms"] = len(reg)
    DOCS.write_protocol(p("protocol"))
    DOCS.write_aipz(p("aipz"))
    PP.normalize_ooxml(p("farms"), "Grower Services", "Eileen Porter", "2023-03-06T09:12:00Z", "2027-01-11T14:27:40Z",
                       excel=True)
    PP.normalize_pdf(p("protocol"), b"D:20261030154211+00'00'", b"D:20261102081902+00'00'")
    PP.normalize_pdf(p("aipz"), b"D:20261126101507+00'00'", b"D:20261126101507+00'00'")
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (STAMP, STAMP))
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.out:
        print(build_pack(a.out))
        sys.exit(0)
    import deliver as DL     # noqa: E402
    import metadata as MD    # noqa: E402
    target = os.path.join(TASK, "target")
    counts = build_pack(target)
    figs = DL.build_goldens(target, os.path.join(TASK, "golden"))
    MD.write(os.path.join(TASK, "metadata.json"), counts)
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(figs, fh, indent=1, sort_keys=True)
        fh.write("\n")
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "ceiling.py")])
    # a second full pack build, compared byte for byte
    tmp = tempfile.mkdtemp(prefix="t184b_", dir=TASK)
    try:
        build_pack(tmp)
        same = True
        for name in sorted(os.listdir(target)):
            a1 = open(os.path.join(target, name), "rb").read()
            a2 = open(os.path.join(tmp, name), "rb").read()
            if a1 != a2:
                print("REBUILD DIFFERS", name)
                same = False
        print("rebuild byte-identical" if same else "REBUILD NOT IDENTICAL")
        rc |= 0 if same else 1
    finally:
        shutil.rmtree(tmp)
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + name, date_time=(2027, 2, 15, 6, 41, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, name), "rb").read())
    print("target.zip md5", hashlib.md5(open(zp, "rb").read()).hexdigest())
    sys.exit(rc)
