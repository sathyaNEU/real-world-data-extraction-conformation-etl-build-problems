"""Build task183: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task183/generator/build.py              everything
    python3 task183/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A           # noqa: E402
import docs as DOCS        # noqa: E402
import pack as P           # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = dt.datetime(2026, 10, 14, 16, 22, 5).timestamp()


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["acct"] = P._csv(p("acct"), P.ACCT_HEADER, P.acct_rows(), crlf=True)
    n["ms"] = P._csv(p("ms"), P.MS_HEADER, P.ms_rows())
    n["till"] = P._csv(p("till"), P.TILL_HEADER, P.till_rows())
    n["ap"] = P._csv(p("ap"), A.AP_HEADER, A.ap_rows(), crlf=True)
    n["tlog"] = P._csv(p("tlog"), A.TILL_LOG_HEADER, A.till_log_rows())
    n["rsi"] = P._csv(p("rsi"), P.RSI_HEADER, P.rsi_rows())
    mreg = P.mreg_rows()
    P.write_xlsx(p("mreg"), [("Merchants", [], P.MREG_HEADER, mreg, [13, 11, 34, 6, 13, 19, 11, 8])])
    n["mreg"] = len(mreg)
    seg = P.seg_rows()
    P.write_xlsx(p("seg"), [("Review list", [["Cash-intensive segment: review list for the review year 2025-26"],
                                             ["Drawn by Financial Crime Operations, 1 October 2025"]],
                             P.SEG_HEADER, seg, [11, 40, 15, 28, 18, 18, 18, 11, 14, 10])])
    n["seg"] = len(seg)
    orders = P.orders_rows()
    P.write_xlsx(p("orders"), [("Orders", [], P.ORDERS_HEADER, orders, [16, 18, 12, 12, 12, 11, 10, 16])])
    n["orders"] = len(orders)
    offices = P.offices_rows()
    P.write_xlsx(p("offices"), [("Offices", [], P.OFFICES_HEADER, offices, [11, 20, 12, 15, 15, 15])])
    n["offices"] = len(offices)
    DOCS.write_bcr3(p("bcr"))
    DOCS.write_apfee(p("apfee"))
    PP.normalize_ooxml(p("mreg"), "Merchant Services", "Dearbhail Cashman", "2021-02-08T10:14:00Z",
                       "2026-10-14T11:02:37Z", excel=True)
    PP.normalize_ooxml(p("seg"), "Conall Mulgrew", "Malachy Crohan", "2025-10-01T08:47:00Z", "2025-10-01T15:31:12Z",
                       excel=True)
    PP.normalize_ooxml(p("orders"), "Cash Centre", "Conall Mulgrew", "2025-09-26T07:55:00Z", "2026-10-02T09:18:44Z",
                       excel=True)
    PP.normalize_ooxml(p("offices"), "An Post Agency Services", "An Post Agency Services", "2024-03-04T09:00:00Z",
                       "2026-10-05T12:40:09Z", excel=True)
    PP.normalize_pdf(p("bcr"), b"D:20250618101544+01'00'", b"D:20250618101544+01'00'")
    PP.normalize_pdf(p("apfee"), b"D:20250624143010+01'00'", b"D:20250624143010+01'00'")
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (STAMP, STAMP))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return dict(counts=n)


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 11, 6, 9, 12, 40)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    sim = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), sim["counts"])
    return sim


def main():
    import checks as CK
    import verify as V
    sim = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"))
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
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s, md5 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16],
        hashlib.md5(open(zp, "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
