"""Build task153: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task153/generator/build.py              everything
    python3 task153/generator/build.py --out DIR    the pack only, into DIR"""
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
    R.devices(W)
    return W


def write_lines(path, lines, crlf=False):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(("\r\n" if crlf else "\n").join(lines) + ("\r\n" if crlf else "\n"))
    return len(lines)


def build_data(out, W):
    p = lambda f: os.path.join(out, f)
    n = {}
    n[R.F_DAYS] = K.write_csv(p(R.F_DAYS), R.DAY_COLS, R.day_rows(W))
    n[R.F_GEO] = K.write_csv(p(R.F_GEO), R.GEO_COLS, R.geo_rows(W))
    n[R.F_DEV] = K.write_csv(p(R.F_DEV), R.DEV_COLS, R.dev_rows(W))
    n[R.F_UNITS] = R.write_units(p(R.F_UNITS), W)
    n[R.F_FMS] = K.write_csv(p(R.F_FMS), R.FMS_COLS, R.fms_rows(W), crlf=True)
    n[R.F_WEST] = K.write_csv(p(R.F_WEST), R.WEST_COLS, R.west_rows(W), crlf=True)
    n[R.F_CENTRAL] = R.write_central(p(R.F_CENTRAL), W)
    n[R.F_EAST] = write_lines(p(R.F_EAST), R.east_lines(W), crlf=True)
    n[R.F_DELIV] = K.write_csv(p(R.F_DELIV), R.DELIV_COLS, R.deliv_rows(W))
    inv, cred = R.invoices(W)
    n[R.F_INV] = K.write_csv(p(R.F_INV), R.INV_COLS, R.fmt_lines(inv, 7, 8, 9))
    n[R.F_CRED] = K.write_csv(p(R.F_CRED), R.CRED_COLS, R.fmt_lines(cred, 8, 9, 10))
    n[R.F_RACK] = K.write_csv(p(R.F_RACK), R.RACK_COLS, R.rack_rows(W))
    n[R.F_TANKS] = R.write_tanks(p(R.F_TANKS), W)
    n[R.F_IFTA] = R.write_ifta(p(R.F_IFTA), W)
    return n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(R.F_UNITS), K.PEOPLE["fleet"], K.PEOPLE["fleet"], "2026-08-28T13:21:00Z",
                       "2026-08-28T13:21:00Z", excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(R.F_CENTRAL), "Crossroads Fleet Card", "Crossroads Fleet Card", "2026-08-28T13:30:00Z",
                       "2026-08-28T13:30:00Z", excel=True, company="Crossroads Fleet Card")
    PP.normalize_ooxml(p(R.F_TANKS), K.PEOPLE["fleet"], K.PEOPLE["fleet"], "2023-04-03T15:12:00Z",
                       "2026-08-24T14:47:00Z", excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(R.F_IFTA), K.PEOPLE["controller"], K.PEOPLE["controller"], "2025-10-21T19:04:00Z",
                       "2026-07-27T16:38:00Z", excel=True, company=K.COMPANY)


def build(out, quiet=False, W=None, docs=True):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    W = W or world()
    counts = build_data(out, W)
    normalize(out)
    if docs:
        import docs as DOC
        DOC.write_all(out, W)
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
    stamp = K.EXPORT_STAMP.timestamp() + 5 * 86400
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
