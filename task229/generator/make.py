"""Build task229 into its task folder: the pack under target/, every check, the goldens under golden/,
generator/figures.json and metadata.json, the independent verifier, a second build into a scratch folder compared
byte for byte, then target.zip cut from the final build.

    python3 task229/generator/make.py
"""
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
import build as B      # noqa: E402
import checks as C     # noqa: E402
import deliver as DV   # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2026, 11, 6, 7, 45, 0)


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    tgt = os.path.join(TASK, "target")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(tgt)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, f), "rb").read())
    return zp


def main():
    tgt, R = B.write_pack(TASK)
    meta = B.metadata(TASK, tgt)
    rec = C.run(TASK, tgt, R, meta)
    B.set_mtimes(tgt)
    _, fig = DV.write(rec, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"))
    tmp = tempfile.mkdtemp(prefix="t229rec")
    recp = os.path.join(tmp, "record.json")
    with open(recp, "w") as fh:
        json.dump(rec, fh, default=str)
    v = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), tgt, "--record", recp], capture_output=True, text=True)
    print(v.stdout.strip().splitlines()[-2] if v.stdout.strip() else v.stderr[-2000:])
    if v.returncode != 0:
        print(v.stdout[-4000:])
        raise SystemExit("verify failed")
    t2 = tempfile.mkdtemp(prefix="t229b2")
    tgt2, _ = B.write_pack(t2)
    B.set_mtimes(tgt2)
    g2 = os.path.join(t2, "golden")
    DV.write(rec, g2, os.path.join(t2, "figures.json"))
    same_t = digest(tgt) == digest(tgt2)
    same_g = digest(os.path.join(TASK, "golden")) == digest(g2)
    same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(t2, "figures.json"), "rb").read()
    shutil.rmtree(t2)
    shutil.rmtree(tmp)
    if not (same_t and same_g and same_f):
        raise SystemExit("second build differs: target %s, golden %s, figures %s" % (same_t, same_g, same_f))
    zp = cut_zip()
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(tgt):
        raise SystemExit("target.zip differs from target/")
    print("checks %d; two builds byte-identical (%d target files, %d golden files, figures.json); target.zip sha256 %s" % (
        rec["checks"], len(inside), len(os.listdir(os.path.join(TASK, "golden"))), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    print(json.dumps({"call": fig["call_first"], "bias": fig["bias_range_pct"], "least": fig["bias_least"]}))


if __name__ == "__main__":
    main()
