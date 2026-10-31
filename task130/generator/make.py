"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task130/generator/make.py [--once] [--target DIR]
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import distract as DX
import docs
import pack as P
import records as RC
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = 1799430000          # 8 January 2027, 09:40 PST, when the program assembled the extracts


def world():
    import clearance as CL
    R = RC.build()
    R = RC.simulate(R)
    R = RC.schedule_2027(R)
    R["clearance"] = CL.run(R)
    D = P.derive(R)
    return R, D


def build_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    R, D = world()
    c = {}
    c["legacy"], c["current"] = P.write_exports(R, D, target)
    c["permits"] = P.write_permits(R, target)
    c["complaints"] = P.write_complaints(D, target)
    c["letters"] = P.write_letters(D, target)
    P.write_holidays(target)
    c["roster"] = P.write_roster(target)
    c["schedule"] = P.write_schedule(R, target)
    c["daysheet"] = P.write_capacity(R, D, target)
    docs.plan_pdf(os.path.join(target, P.FILES["plan"]), R["insp27"])
    docs.fees_pdf(os.path.join(target, P.FILES["fees"]))
    c["illness"] = DX.write_illness(R, target)
    c["invoices"] = DX.write_invoices(R, target)
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (STAMP, STAMP))
    return R, D, c


def zip_target(target, path):
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 1, 8, 9, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def same_tree(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    if fa != fb:
        return False
    return all(filecmp.cmp(os.path.join(a, f), os.path.join(b, f), shallow=False) for f in fa)


def main():
    target = TARGET
    if "--target" in sys.argv:
        target = sys.argv[sys.argv.index("--target") + 1]
    R, D, c = build_target(target)
    print("built", target, c)
    if "--pack-only" in sys.argv:
        return
    import analysis as AN
    F = AN.main(target)
    golden_dir = GOLDEN if target == TARGET else os.path.join(os.path.dirname(target), "golden")
    import golden as GD
    GD.write(golden_dir, F)
    import metadata as MD
    meta = MD.metadata(target, c)
    if target == TARGET:
        json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    import checks as C
    n = C.run(R, D, c, target, F, golden_dir)
    print("checks: %d assertions pass" % n)
    if target == TARGET:
        r1 = lambda d: {k: round(v, 1) for k, v in d.items()}
        print("measured: family %s; crossed %.1f to %.1f over %d; rich %s; rungs %s; refuted %s; r2 %s; sf9 %.1f; "
              "second-visit z %.2f; first-visit share %s; truth %.1f"
              % (r1(F["family"]), F["crossed"][0], F["crossed"][1], F["crossed"][2], r1(F["rich"]), r1(F["rungs"]),
                 r1(F["refuted"]), r1(F["r2"]), F["sf9"], F["z_second"], {y: round(v, 3) for y, v in
                                                                            F["first_share"].items()}, R["truth27"]))
    import figures as FG
    figs = FG.figures(F, n)
    if target == TARGET:
        json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, ensure_ascii=False)
    import verify as VF
    VF.main(target, golden_dir)
    if "--once" in sys.argv or target != TARGET:
        return
    tmp = tempfile.mkdtemp(prefix="t130-rebuild-")
    t2 = os.path.join(tmp, "target")
    R2, D2, c2 = build_target(t2)
    F2 = AN.main(t2)
    GD.write(os.path.join(tmp, "golden"), F2)
    assert same_tree(target, t2), "the second build differs under target/"
    assert same_tree(golden_dir, os.path.join(tmp, "golden")), "the second build differs under golden/"
    shutil.rmtree(tmp)
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("rebuild byte-identical; target.zip written")


if __name__ == "__main__":
    main()
