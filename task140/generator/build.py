"""Build task140: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task140/generator/build.py              everything
    python3 task140/generator/build.py --out DIR    the pack only, into DIR"""
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
EXPORT_STAMP = dt.datetime(2026, 12, 14, 7, 55, tzinfo=dt.timezone.utc)   # 08:55 in Alcobendas, the papers compiled

FILES = [
    (K.STANDARD_PDF, "Cell Capacity Standard CS-3, revision of June 2026", "Infrastructure, approved 22 June 2026"),
    (K.MEMO, "Capacity memo for the C-22 review of 2027 Q1", "Head of Infrastructure, 9 December 2026"),
    (K.HWPLAN, "C-22 hardware plan for 2027 Q1, racks and machines in service by date", "Fleet & Hardware, revision of "
     "11 December 2026"),
    (K.REQUESTS, "Firm tenants' reservation requests for 2027 Q1", "Quota tool, request window 16 November to "
     "4 December 2026"),
    (K.BUDGETS, "Technology compute budgets by cost centre, 2026 and January to March 2027, with the freeze note",
     "Technology Controlling, 27 November 2026"),
    (K.RATECARD, "Compute rate card for MAD1 reserved cores, every rate by effective date", "Technology Controlling"),
    (K.LEDGER, "C-22 reservation ledger, 2025 Q1 to 2026 Q4, as approved at each review", "Compute Operations"),
    (K.USAGE, "C-22 monitoring export, each tenant's average cores in use by hour, 1 January 2025 to 13 December 2026",
     "Cell monitoring, pulled 14 December 2026 06:10 UTC"),
    (K.CELLHOURLY, "C-22 machines installed and in service by hour, same period", "Cell monitoring, pulled 14 December "
     "2026 06:10 UTC"),
    (K.DIRECTORY, "C-22 tenant directory", "Compute Operations, 1 December 2026"),
    (K.CAPREPORT, "C-22 capacity report for 2026 Q3", "Compute Operations, 6 October 2026"),
    (K.OPSLOG, "MAD1 operations log, July to December 2026", "Data-centre operations"),
    (K.RUNS, "Batch training runs that held cores in 2026 Q3", "Batch scheduler, quarter snapshot of 1 October 2026"),
    (K.CHECKPOINTS, "Checkpoints written by those runs, and the checkpoints their resumptions restored", "Batch "
     "scheduler, quarter snapshot of 1 October 2026"),
    (K.RESIZES, "Resizes of elastic batch runs in 2026 Q3", "Batch scheduler, quarter snapshot of 1 October 2026"),
    (K.MEVENTS, "C-22 machine events, 1 July to 30 September 2026", "MAD1 cluster manager event log"),
    (K.INVENTORY, "MAD1 hardware inventory for C-22, assets and their cluster ids", "Fleet & Hardware, extract of "
     "14 December 2026"),
    (K.QCHANGES, "Changes to firm reservations in 2026 Q3", "Quota tool"),
    (K.QRUNS, "Quota service reconciliation runs in 2026 Q3", "Quota service log"),
    (K.CHARGEBACK, "Technology chargeback policy 2026", "Technology Controlling"),
    (K.DICTIONARY, "Field definitions for these files", "Compute Operations"),
    (K.SISTERS, "MAD1 compute cells' quarterly summary, 2025 and 2026", "Compute Operations, 2 October 2026"),
    (K.BATCH_DEMAND, "ML Platform's note on batch training demand for January to June 2027", "ML Platform, "
     "2 December 2026"),
]


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or WD.simulate()
    counts = {}
    counts[K.USAGE] = K.write_csv(p(K.USAGE), R.USAGE_COLS, R.usage_rows(W))
    counts[K.CELLHOURLY] = K.write_csv(p(K.CELLHOURLY), R.CELL_COLS, R.cell_rows(W))
    counts[K.LEDGER] = K.write_csv(p(K.LEDGER), R.LEDGER_COLS, R.ledger_rows(W))
    counts[K.REQUESTS] = K.write_csv(p(K.REQUESTS), R.REQ_COLS, R.request_rows(W))
    counts[K.RATECARD] = K.write_csv(p(K.RATECARD), R.RATE_COLS, R.rate_rows(W), crlf=True)
    counts[K.RUNS] = K.write_csv(p(K.RUNS), R.RUNS_COLS, R.runs_rows(W))
    counts[K.CHECKPOINTS] = K.write_csv(p(K.CHECKPOINTS), R.CKPT_COLS, R.ckpt_rows(W))
    counts[K.RESIZES] = K.write_csv(p(K.RESIZES), R.RESIZE_COLS, R.resize_rows(W))
    counts[K.MEVENTS] = K.write_csv(p(K.MEVENTS), R.MEV_COLS, R.machine_events(W))
    counts[K.QCHANGES] = K.write_csv(p(K.QCHANGES), R.QCH_COLS, R.quota_change_rows(W))
    counts[K.QRUNS] = K.write_csv(p(K.QRUNS), R.QRUN_COLS, R.quota_run_rows(W))
    R.write_directory(p(K.DIRECTORY), W)
    DOC.write_standard(p(K.STANDARD_PDF))
    DOC.write_memo(p(K.MEMO), W)
    DOC.write_hwplan(p(K.HWPLAN), W)
    DOC.write_budgets(p(K.BUDGETS), W)
    DOC.write_capreport(p(K.CAPREPORT), W)
    DOC.write_opslog(p(K.OPSLOG), W)
    DOC.write_inventory(p(K.INVENTORY), W)
    DOC.write_chargeback(p(K.CHARGEBACK))
    DOC.write_dictionary(p(K.DICTIONARY))
    DOC.write_sisters(p(K.SISTERS), W)
    DOC.write_batch_demand(p(K.BATCH_DEMAND), W)
    DOC.write_readme(p(K.README), FILES)
    P = K.PEOPLE
    PP.normalize_ooxml(p(K.MEMO), P["head"], P["head"], "2026-12-09T08:41:12Z", "2026-12-09T10:02:47Z",
                       title="C-22 capacity review 2027 Q1", company=K.COMPANY)
    PP.normalize_ooxml(p(K.OPSLOG), P["dcops"], P["sre"], "2026-07-01T05:58:31Z", "2026-12-14T06:22:05Z",
                       title="MAD1 operations log 2026 H2", company=K.COMPANY)
    PP.normalize_ooxml(p(K.HWPLAN), P["fleet"], P["fleet"], "2024-02-12T09:14:52Z", "2026-12-11T11:58:20Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(K.BUDGETS), P["finance"], P["finance"], "2025-12-18T15:31:09Z", "2026-11-27T16:20:44Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(K.INVENTORY), P["fleet"], P["fleet"], "2026-12-14T06:47:30Z", "2026-12-14T06:47:30Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(K.DICTIONARY), P["requester"], P["requester"], "2025-03-10T10:22:41Z", "2026-12-14T07:31:18Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(K.SISTERS), P["requester"], P["requester"], "2025-04-03T08:05:57Z", "2026-10-02T14:40:26Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_pdf(p(K.STANDARD_PDF), b"D:20260622101544+02'00'", b"D:20260622103012+02'00'")
    PP.normalize_pdf(p(K.CAPREPORT), b"D:20261006092611+02'00'", b"D:20261006092611+02'00'")
    PP.normalize_pdf(p(K.CHARGEBACK), b"D:20251215163002+01'00'", b"D:20251215164418+01'00'")
    PP.normalize_pdf(p(K.BATCH_DEMAND), b"D:20261202171953+01'00'", b"D:20261202172240+01'00'")
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
