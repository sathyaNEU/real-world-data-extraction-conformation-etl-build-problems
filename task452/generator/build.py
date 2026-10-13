"""Build task452: the pack into <task>/target (data first, the asks' figures centred, then the agreement with each
tributary's allocation placed from the loads the shipped data give), the goldens into <task>/golden, metadata.json
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task452/generator/build.py              everything
    python3 task452/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import calc as C            # noqa: E402
import docs as DC           # noqa: E402
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import sim as S             # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2027, 1, 12, 9, 40, tzinfo=EASTERN)       # the folder as the program shared it

GOLDEN_SLATE = ("Kestle River", "Hessick River", "Varrow Brook")
DEFAULT_SLATE = ("Varrow Brook", "Orrinwood Brook", "Ambrey River")


def place_allocations(target):
    """each tributary's Schedule 1 allocation from the shipped data. The golden slate's three stand above their
    allocations on every rating-curve route (seasonal or not, either retransformation, quadratic, any calibration
    window, even uncorrected) by clear margins over the fourth; Varrow Brook also stands just above its allocation on
    the interpolated loads; Orrinwood Brook and Ambrey River sit about at their allocations on the rating curves and
    clearly above on the interpolated loads; the rest sit under"""
    L = C.load(target)
    R, info = C.route_loads(L)
    G = R[C.GOLD]
    r0 = R[C.DEFAULT]
    fam = [R[k] for k in C.GOLDEN]
    A = {}
    for code in W.CODES:
        n = W.NAME[code]
        role = W.ROLE[code]
        lo, hi = min(v[n] for v in fam), max(v[n] for v in fam)
        if role == "gold_top":
            A[n] = lo / 1.12
        elif role == "both_top":
            A[n] = min(r0[n] - 0.06 * G[n], lo / 1.12)
        elif role == "interp_top":
            A[n] = min(lo, r0[n]) / 1.05
        elif role == "clear":
            A[n] = max(hi, r0[n]) / 0.92
    out = {n: float(round(v / 10.0) * 10) for n, v in A.items()}
    return {code: out[W.NAME[code]] for code in W.CODES}, None


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or S.simulate()
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["wq"] = P.write_wq(w, f("wq"))
    n["uv"] = P.write_uv(w, f("uv"))
    n["dv"] = P.write_dv(w, f("dv"))
    n["prov"] = P.write_prov(w, f("prov"))
    n["register"] = P.write_register(w, f("register"))
    n["dmr"] = P.write_dmr(w, f("dmr"))
    n["contracts"] = P.write_contracts(w, f("contracts"))
    n["fields"] = P.write_fields(w, f("fields"))
    n["precip"] = P.write_precip(w, f("precip"))
    n["lake"] = P.write_lake(w, f("lake"))
    import polish as PO
    PO.straddle(out)
    w["polish"] = dict(wastewater=PO.wastewater(out), cover=PO.cover(out))
    alloc, band = place_allocations(out)
    DC.write_agreement(f("agreement"), alloc)
    DC.write_program(f("program"))
    DC.write_transmittal(f("transmittal"), n)
    mgr, dr = W.PEOPLE["manager"][0], W.PEOPLE["director"][0]
    PP.normalize_ooxml(f("program"), mgr, mgr, "2024-02-20T14:10:00Z", "2026-11-17T16:22:41Z",
                       title="Tributary monitoring program", company=W.COMMISSION)
    PP.normalize_ooxml(f("register"), mgr, mgr, "2023-09-12T13:45:00Z", "2026-12-18T20:04:13Z", excel=True, company=W.COMMISSION)
    PP.normalize_ooxml(f("lake"), mgr, mgr, "2024-05-02T12:30:00Z", "2026-11-03T15:51:09Z", excel=True, company=W.COMMISSION)
    PP.normalize_pdf(f("agreement"), b"D:20251210101530-05'00'", b"D:20251210103347-05'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    w["counts"] = n
    w["alloc"] = alloc
    w["band"] = band
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 1, 12, 9, 40, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False, world=None):
    import golden as G
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet, world=world)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    world["golden"] = G.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                             os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
                meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode() +
                          open(os.path.join(TASK, "metadata.json"), "rb").read() +
                          open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))), allh[:16]))
    import zipfile
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not ok:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
