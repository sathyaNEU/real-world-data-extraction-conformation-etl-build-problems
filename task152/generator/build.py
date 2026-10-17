"""Build task152: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task152/generator/build.py              everything
    python3 task152/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)


class Built:
    pass


def world():
    W = WD.simulate()
    R.sensors(W)
    R.district(W)
    R.hedges(W)
    return W


def write_lines(path, lines, crlf=False):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(("\r\n" if crlf else "\n").join(lines) + ("\r\n" if crlf else "\n"))
    return len(lines)


def build_data(out, W):
    p = lambda f: os.path.join(out, f)
    counts = {}
    counts[R.F_OLD] = K.write_csv(p(R.F_OLD), R.OLD_COLS, R.old_rows(W), crlf=True)
    counts[R.F_NEW] = K.write_csv(p(R.F_NEW), R.NEW_COLS, R.new_rows(W))
    counts[R.F_TAGS] = K.write_csv(p(R.F_TAGS), R.TAG_COLS, R.tag_rows())
    counts[R.F_HOURLY] = K.write_csv(p(R.F_HOURLY), R.HOURLY_COLS, R.hourly_rows(W))
    counts[R.F_MET] = K.write_csv(p(R.F_MET), R.MET_COLS, R.met_rows(W))
    counts[R.F_EVENTS] = K.write_csv(p(R.F_EVENTS), R.EVENT_COLS, R.event_rows(W))
    wo = R.wo_rows(W)
    counts[R.F_WO] = R.write_xlsx(p(R.F_WO), "WorkOrders", R.WO_COLS, wo, [13, 6, 10, 92, 17, 17, 9, 10],
                                  date_cols=(5, 6), num_cols=((7, "0.0"),))
    counts[R.F_LEGACY] = write_lines(p(R.F_LEGACY), R.legacy_lines(W), crlf=True)
    counts[R.F_MDM] = K.write_csv(p(R.F_MDM), R.MDM_COLS, R.mdm_rows(W))
    counts[R.F_SP] = K.write_csv(p(R.F_SP), R.SP_COLS, R.sp_rows())
    bl = R.blotter_rows(W)
    counts[R.F_BLOTTER] = R.write_xlsx(p(R.F_BLOTTER), "Blotter", R.BLOTTER_COLS, bl, [16, 12, 28, 40, 9, 5, 14, 13, 11, 8],
                                       datefmt="mm/dd/yyyy", date_cols=(2,), num_cols=((7, "#,##0"), (8, "0.00")))
    lt = list(R.lt_rows(W))
    with open(p(R.F_LT), "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(R.lt_header()) + "\n")
        fh.write(",".join(R.LT_COLS) + "\n")
        fh.write("\n".join(",".join(r) for r in lt) + "\n")
    counts[R.F_LT] = len(lt)
    counts[R.F_CURVE] = K.write_csv(p(R.F_CURVE), R.CURVE_COLS, R.curve_rows())
    return counts


def build(out, quiet=False, W=None, docs=True):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    W = W or world()
    counts = build_data(out, W)
    if docs:
        import docs as DOC
        DOC.write_all(out, W)
        for f in DOC.OFFICE:
            pass
    stamp = K.EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    B = Built()
    B.W, B.counts = W, counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return B


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = K.EXPORT_STAMP.timetuple()[:6]
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
    B = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    G = DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                os.path.join(root, "generator", "figures.json"), os.path.join(root, "submission.md"), B=B)
    stamp = K.EXPORT_STAMP.timestamp() + 2 * 86400
    for f in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), B)
    return B, G


def main():
    import checks as CK
    import verify as V
    B, G = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), B=B, G=G,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json")):
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
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, figures.json, submission.md and "
          "target.zip (sha256 %s; target.zip sha256 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--nodocs", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out, docs=not a.nodocs)
    else:
        main()
