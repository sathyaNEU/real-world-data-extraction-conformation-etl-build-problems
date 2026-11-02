"""Build task266: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task266/generator/build.py              everything
    python3 task266/generator/build.py --out DIR    the pack only, into DIR
    python3 task266/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2027, 2, 11, 15, 26)     # the pack as put together for the board paper, AEDT
MTIME = calendar.timegm((EXPORT - dt.timedelta(hours=11)).timetuple())


def report_figures(T):
    import numpy as np
    rng = np.random.default_rng([K.SEED, 7])
    m = sum(1 for x in T["members"] if x["status"] == "Active")
    return dict(lodged=(int(rng.integers(780, 840)), int(rng.integers(800, 870))),
                accepted=(int(rng.integers(560, 610)), int(rng.integers(575, 630))),
                lump=("%.1f" % rng.uniform(88, 94), "%.1f" % rng.uniform(92, 99)),
                care=("%.1f" % rng.uniform(41, 46), "%.1f" % rng.uniform(44, 50)),
                recov=("%.1f" % rng.uniform(52, 57), "%.1f" % rng.uniform(54, 61)),
                members="{:,}".format(m), visits=len(T["unit"]),
                levy="%.1f" % rng.uniform(212, 228), invest="%.1f" % rng.uniform(61, 74),
                liab="{:,}".format(int(rng.integers(2140, 2390))))


def world(seed=K.SEED):
    return W.build(seed)


def build(out, seed=K.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = world(seed)
    n = {}
    n["register"] = R.write_register(p("register"), T)
    n["legacy"] = R.write_legacy(p("legacy"), T)
    n["histories"] = R.write_histories(p("histories"), T)
    n["members"] = R.write_members(p("members"), T)
    n["appointments"] = R.write_appointments(p("appointments"), T)
    n["card"] = R.write_card(p("card"), T)
    n["qa"] = R.write_qa(p("qa"), T)
    n["roads"] = R.write_roads(p("roads"))
    n["registry"] = R.write_registry(p("registry"))
    n["workplaces"] = R.write_workplaces(p("workplaces"), T)
    D.write_terms(p("terms"))
    D.write_report(p("report"), report_figures(T))
    D.write_schedule(p("schedule"), T["unit"])
    PP.COMPANY = K.FUND
    PP.normalize_ooxml(p("legacy"), "Case system 1", "Case system 1", "2013-02-15T04:12:40Z", "2013-02-15T04:12:40Z",
                       excel=True)
    PP.normalize_ooxml(p("card"), "Fleet Services", "Fleet Services", "2026-07-06T00:41:19Z", "2026-07-06T00:41:19Z",
                       excel=True)
    PP.normalize_ooxml(p("qa"), "J Marchetti", "T Szabo", "2025-07-10T22:15:03Z", "2026-06-30T06:48:51Z", excel=True)
    PP.normalize_ooxml(p("roads"), "Finance", "Finance", "2024-03-18T03:22:10Z", "2025-05-26T01:05:44Z", excel=True)
    PP.normalize_ooxml(p("registry"), K.REGISTRY, K.REGISTRY, "2025-11-03T23:40:02Z", "2025-11-04T02:11:37Z", excel=True)
    PP.normalize_pdf(p("terms"), b"D:20261127153014+11'00'", b"D:20261128090212+11'00'")
    PP.normalize_pdf(p("report"), b"D:20261014101551+11'00'", b"D:20261021164433+11'00'")
    PP.normalize_pdf(p("schedule"), b"D:20250612141022+10'00'", b"D:20250616093045+10'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["n"] = n
    return T


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=K.SEED)
    a = ap.parse_args()
    if a.out:
        build(a.out, a.seed)
        return
    target = os.path.join(TASK, "target")
    T = build(target)
    print("pack:", T["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
