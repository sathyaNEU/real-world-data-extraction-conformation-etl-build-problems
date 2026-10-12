"""Build task128: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task128/generator/build.py              everything
    python3 task128/generator/build.py --out DIR    the pack only, into DIR
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
import numpy as np         # noqa: E402

import docs as DC          # noqa: E402
import extras as X         # noqa: E402
import pack as P           # noqa: E402
import postprocess as PP   # noqa: E402
import sim as S            # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-4))
STAMP = dt.datetime(2026, 10, 9, 16, 42, tzinfo=EASTERN)       # the folder as Collections MI shared it


def simulate():
    A, E, caps = S.simulate()
    rng = np.random.default_rng(W.SEED + 1)
    E = X.results(E, rng)
    R, agents = X.attempts(E, None, rng)
    rates = X.booking_rates(rng)
    E = X.balances(A, E, rng, rates)
    arr = X.arrangements(E, rng, agents)
    H = X.history(E, rng)
    C = X.capacity_log(E, rng)
    T = X.test_calls(rng, agents)
    G60 = X.ls60_summary(H, A.centre.values, rng)
    HC = X.headcount(rng)
    acctno, opened = X.account_numbers(A, rng)
    return dict(A=A, E=E, caps=caps, R=R, agents=agents, rates=rates, arr=arr, H=H, C=C, T=T, G60=G60, HC=HC,
                acctno=acctno, opened=opened, rng_tail=rng)


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or simulate()
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["lists"] = P.lists(w["E"], w["acctno"], f("lists"))
    n["calls"] = P.calls(w["R"], w["T"], w["acctno"], np.random.default_rng(W.SEED + 2), f("calls"))
    n["history"] = P.history(w["H"], w["A"], w["acctno"], f("history"))
    n["worklog"] = P.worklog(w["C"], f("worklog"))
    n["arrangements"] = P.arrangements(w["arr"], w["acctno"], f("arrangements"))
    n["rates"] = P.rates(w["rates"], f("rates"))
    n["ls60"] = P.ls60(w["G60"], f("ls60"))
    n["headcount"] = P.headcount(w["HC"], f("headcount"))
    DC.write_protocol(os.path.join(out, DC.PROTOCOL))
    DC.write_policy(os.path.join(out, DC.POLICY))
    DC.write_budget(os.path.join(out, DC.BUDGET))
    DC.write_fields(os.path.join(out, DC.FIELDS))
    DC.write_manifest(os.path.join(out, DC.MANIFEST), n)
    PP.normalize_ooxml(os.path.join(out, DC.POLICY), "Gabriel Ross", "Kathryn Gray", "2024-03-11T14:05:00Z",
                       "2026-10-06T15:47:00Z", title="CP-14 Collections Resourcing")
    PP.normalize_ooxml(os.path.join(out, DC.BUDGET), "Elizabeth Marquez", "Elizabeth Marquez", "2026-08-19T13:40:11Z",
                       "2026-09-30T21:08:52Z", excel=True)
    PP.normalize_ooxml(os.path.join(out, DC.FIELDS), "Collections MI", "Collections MI", "2025-02-03T15:00:00Z",
                       "2026-10-09T18:31:00Z", title="Collections data extracts: field reference")
    PP.normalize_ooxml(f("headcount"), "HR Reporting", "HR Reporting", "2026-10-06T12:15:40Z", "2026-10-06T12:16:02Z",
                       excel=True)
    PP.normalize_pdf(os.path.join(out, DC.PROTOCOL), b"D:20241219153310-05'00'", b"D:20241219153544-05'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    w["counts"] = n
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 9, 16, 42, 0)
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
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
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
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()).hexdigest()
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
