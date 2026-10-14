"""Build task138: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task138/generator/build.py              everything
    python3 task138/generator/build.py --out DIR    the pack only, into DIR"""
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
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2027, 2, 1, 15, 40, tzinfo=dt.timezone.utc)   # 7:40 am in Kestrel Bend, the hand-off


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or WD.simulate()
    counts = {}
    counts[K.ST39] = K.write_csv(p(K.ST39), R.ST39_COLS, R.st39_rows(W), crlf=True)
    counts[K.YARD] = K.write_csv(p(K.YARD), R.YARD_COLS, R.yard_rows(W))
    counts[K.REGISTER] = K.write_csv(p(K.REGISTER), R.REGISTER_COLS, R.register_rows(W))
    counts[K.ORDERS] = K.write_csv(p(K.ORDERS), R.ORDERS_COLS, R.orders_rows(W))
    counts[K.METER_BOOK] = K.write_csv(p(K.METER_BOOK), R.BOOK_COLS, R.book_rows(W), crlf=True)
    counts[K.HEADINGS] = K.write_csv(p(K.HEADINGS), R.HEAD_COLS, R.heading_rows(W))
    counts[K.WEIRS] = K.write_csv(p(K.WEIRS), R.WEIR_COLS, R.weir_rows(W), crlf=True)
    counts[K.GROUNDWATER] = K.write_csv(p(K.GROUNDWATER), R.GW_COLS, R.groundwater_rows(W))
    counts[K.CROP_REPORT] = K.write_csv(p(K.CROP_REPORT), R.CROP_REPORT_COLS, R.crop_report_rows(W))
    DOC.write_wop(p(K.WOP_PDF))
    DOC.write_wop_tables(p(K.WOP_TABLES))
    DOC.write_requests(p(K.REQUESTS), W)
    DOC.write_shop_log(p(K.SHOP_LOG), W)
    DOC.write_structures(p(K.STRUCTURES))
    DOC.write_ops_log(p(K.OPS_LOG), W)
    DOC.write_dictionary(p(K.DICTIONARY))
    DOC.write_notice(p(K.NOTICE))
    files = [
        (K.WOP_PDF, "The Water Order Procedure (Resolution 2019-07, revised December 2025)", "Board records"),
        (K.WOP_TABLES, "The procedure's Tables 1 to 5 for the 2027 order", "Board records, adopted 9 December 2025"),
        (K.REQUESTS, "Growers' 2027 water requests, every version", "Request log, exported 1 February 2027"),
        (K.REGISTER, "Field register: fields, turnouts, laterals, soil units", "GIS, exported 1 February 2027"),
        (K.ST39, "Daily weather, station 39 (Kestrel Bend South), October 1995 to January 2027",
         "State agricultural weather network download, 1 February 2027"),
        (K.YARD, "Daily weather, Kestrel Bend yard station, April 2014 to January 2027",
         "Yard logger export, 1 February 2027"),
        (K.ORDERS, "Irrigation orders, 2023 to 2026 seasons", "Ordering system, exported 1 February 2027"),
        (K.METER_BOOK, "Riders' turnout meter reads, 2026", "Meter book, closed 30 November 2026"),
        (K.SHOP_LOG, "Meter shop work orders, 2026 season, and the meter inventory", "Meter shop"),
        (K.HEADINGS, "Daily volume at each lateral heading, 2026 season", "SCADA daily report"),
        (K.WEIRS, "Riders' tail weir sheets, 2026 season", "Water Master's office"),
        (K.STRUCTURES, "Tail weirs, lateral headings and main canal structures", "District Engineer's inventory"),
        (K.OPS_LOG, "Canal operations log, 2026 season", "Water Master's office"),
        (K.GROUNDWATER, "Spring and fall depth to groundwater at the District's monitoring wells, 2016 to 2026",
         "Groundwater monitoring program"),
        (K.CROP_REPORT, "2026 crop survey by field", "Water Conservation, June and July 2026"),
        (K.NOTICE, "The Authority's 2027 initial allocation notice", "Tolan Valley Water Authority, 15 December 2026"),
        (K.DICTIONARY, "Field definitions for these files", "Water Resources"),
    ]
    DOC.write_readme(p(K.README), files)
    PP.normalize_ooxml(p(K.WOP_TABLES), K.PEOPLE["requester"], K.PEOPLE["gm"], "2019-03-28T17:12:40Z",
                       "2025-12-10T00:31:17Z", excel=True)
    PP.normalize_ooxml(p(K.REQUESTS), K.PEOPLE["conservation"], K.PEOPLE["conservation"], "2026-11-12T18:02:11Z",
                       "2027-02-01T15:21:08Z", excel=True)
    PP.normalize_ooxml(p(K.SHOP_LOG), K.PEOPLE["watermaster"], K.PEOPLE["watermaster"], "2021-02-03T16:44:02Z",
                       "2026-11-30T23:05:51Z", excel=True)
    PP.normalize_ooxml(p(K.STRUCTURES), K.PEOPLE["engineer"], K.PEOPLE["engineer"], "2012-06-19T20:10:33Z",
                       "2025-03-21T17:48:20Z", excel=True)
    PP.normalize_ooxml(p(K.DICTIONARY), K.PEOPLE["requester"], K.PEOPLE["requester"], "2023-01-24T19:33:51Z",
                       "2027-02-01T15:30:12Z", excel=True)
    PP.normalize_ooxml(p(K.OPS_LOG), K.PEOPLE["watermaster"], K.PEOPLE["watermaster"], "2026-01-26T15:02:00Z",
                       "2027-01-25T22:14:36Z", title="Canal operations log 2026")
    PP.normalize_pdf(p(K.WOP_PDF), b"D:20251210083122-08'00'", b"D:20251210091405-08'00'")
    PP.normalize_pdf(p(K.NOTICE), b"D:20261215101530-08'00'", b"D:20261215102207-08'00'")
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    W.counts = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return W


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
    W = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return W


def main():
    import checks as CK
    import verify as V
    W = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), W=W, meta_path=os.path.join(TASK, "metadata.json"))
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
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
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
