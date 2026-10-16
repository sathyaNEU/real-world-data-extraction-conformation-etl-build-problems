"""Build task146: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task146/generator/build.py              everything
    python3 task146/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import industry as I        # noqa: E402
import notices as N         # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 10, 8, 2, 47, tzinfo=dt.timezone.utc)   # 15:47 on 8 October at the desk (UTC+13)


class World:
    pass


def world():
    Wd = World()
    Wd.T = WD.simulate()
    Wd.ind = I.simulate(Wd.T)
    Wd.notices = N.simulate()
    Wd.program = R.program(Wd.T, Wd.ind)
    return Wd


def build(out, quiet=False, Wd=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    Wd = Wd or world()
    T = Wd.T
    counts = {}
    counts[R.F_LEGACY] = K.write_csv(p(R.F_LEGACY), R.LEGACY_COLS, R.legacy_rows(T), crlf=True)
    counts[R.F_CURRENT] = K.write_csv(p(R.F_CURRENT), R.CURRENT_COLS, R.current_rows(T))
    DOC.write_release(p(R.F_RELEASE), R.release(T))
    DOC.write_program(p(R.F_PROGRAM), T, Wd.program)
    DOC.write_notes(p(R.F_NOTES))
    counts[R.F_REGIONS] = K.write_csv(p(R.F_REGIONS), R.REGION_COLS, R.region_rows())
    counts[R.F_HOLIDAYS] = K.write_csv(p(R.F_HOLIDAYS), ["date", "day", "holiday"], R.holiday_rows())
    counts[R.F_PORTAL] = K.write_csv(p(R.F_PORTAL), N.PORTAL_COLS, N.portal_rows(Wd.notices))
    DOC.write_register(p(R.F_REGISTER), N.register_rows(Wd.notices))
    counts[R.F_CASES] = K.write_csv(p(R.F_CASES), N.CASE_COLS, N.case_note_rows(Wd.notices))
    counts[R.F_CUBE] = K.write_csv(p(R.F_CUBE), R.CUBE_COLS, I.cube_rows(Wd.ind))
    counts[R.F_CODES] = K.write_csv(p(R.F_CODES), ["division", "title", "group_no", "group"], R.code_list_rows())
    DOC.write_concordance(p(R.F_CONCORD), R.concordance_rows())
    counts[R.F_LFS] = K.write_csv(p(R.F_LFS), ["quarter", "region", "labour_force_000", "unemployed_000",
                                                "unemployment_rate", "unemployment_rate_sa"], R.lfs_rows(T))
    DOC.write_ads(p(R.F_ADS), R.ads_series(T))
    counts[R.F_LOG] = K.write_csv(p(R.F_LOG), R.LOG_COLS, R.log_rows(), crlf=True)
    P = K.PEOPLE
    PP.normalize_pdf(p(R.F_NOTES), b"D:20260714101522+12'00'", b"D:20260721143906+12'00'")
    PP.normalize_pdf(p(R.F_RELEASE), b"D:20261008082114+13'00'", b"D:20261008082114+13'00'")
    PP.normalize_ooxml(p(R.F_PROGRAM), "Labour Market Statistics", P["statsmgr"], "2021-08-04T22:10:31Z",
                       "2026-10-07T19:02:56Z", excel=True, company=K.BOARD)
    PP.normalize_ooxml(p(R.F_REGISTER), "Employer Services", P["employer"], "2025-07-01T20:33:12Z",
                       "2026-06-30T04:41:27Z", excel=True, company=K.BOARD)
    PP.normalize_ooxml(p(R.F_CONCORD), "Classifications and Standards", "Classifications and Standards",
                       "2025-06-18T23:05:40Z", "2025-11-11T01:27:18Z", excel=True, company=K.STATS_OFFICE)
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    Wd.counts = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return Wd


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = EXPORT_STAMP.timetuple()[:6]
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(folder, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    Wd = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    G = DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                os.path.join(root, "generator", "figures.json"), Wd=Wd)
    stamp = dt.datetime(2026, 10, 8, 3, 58, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return Wd, G


def main():
    import checks as CK
    import verify as V
    Wd, G = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), Wd=Wd, G=G,
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
        same["target.zip"] = open(cut_zip(TASK), "rb").read() == open(cut_zip(tmp), "rb").read()
        if not (same_t and same_g and all(same.values())):
            d1, d2 = digest(os.path.join(TASK, "target")), digest(os.path.join(tmp, "target"))
            g1, g2 = digest(os.path.join(TASK, "golden")), digest(os.path.join(tmp, "golden"))
            raise SystemExit("second build differs: target %s, golden %s, %s; %s" % (
                same_t, same_g, same, [f for f in d1 if d1[f] != d2.get(f)] + [f for f in g1 if g1[f] != g2.get(f)]))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, figures.json and target.zip "
          "(sha256 %s; target.zip sha256 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
