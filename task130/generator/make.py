"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task130/generator/make.py [--once] [--pack-only] [--target DIR]
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
import distract as DX   # noqa: E402
import docs             # noqa: E402
import pack as P        # noqa: E402
import sim              # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = 1792204800      # 16 October 2026, 13:20 UTC, when the EHS team pulled the extracts


def build_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    S = sim.simulate()
    D = P.derive(S)
    c = {}
    c["legacy"], c["cases"] = P.write_cases(S, D, target)
    c["assign"] = P.write_assignments(S, target)
    c["register"] = P.write_register(S, target)
    c["hours"] = P.write_hours(S, target)
    c["calendar"] = P.write_calendar(target)
    c["plan"] = P.write_plan(S, target)
    docs.standard_pdf(os.path.join(target, P.FILES["standard"]))
    docs.programme_pdf(os.path.join(target, P.FILES["programme"]))
    docs.notice_docx(os.path.join(target, P.FILES["notice"]))
    c["nearmiss"] = DX.write_good_catch(S, target)
    c["subs"] = DX.write_subs(target)
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (STAMP, STAMP))
    return S, D, c


def zip_target(target, path):
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 16, 13, 20, 0))
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
    S, D, c = build_target(target)
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
    n = C.run(S, D, c, target, F, golden_dir)
    print("checks: %d assertions pass" % n)
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
    build_target(t2)
    F2 = AN.main(t2)
    GD.write(os.path.join(tmp, "golden"), F2)
    assert same_tree(target, t2), "the second build differs under target/"
    assert same_tree(golden_dir, os.path.join(tmp, "golden")), "the second build differs under golden/"
    shutil.rmtree(tmp)
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("rebuild byte-identical; target.zip written")


if __name__ == "__main__":
    main()
