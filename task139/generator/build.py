"""Build task139: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task139/generator/build.py              everything
    python3 task139/generator/build.py --out DIR    the pack only, into DIR"""
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
EXPORT_STAMP = dt.datetime(2026, 11, 9, 14, 20, tzinfo=dt.timezone.utc)   # 8:20 am in St. Louis, the request


def pick_total(W):
    """The AY2027 indemnity pick before the credit for the eight segments (context in the memo; nothing reads it)."""
    tot = 0.0
    # usual handling's pure premium per intake from the model's design economics, trended two years at 4 per cent
    pp = {"HC-SS": 2850, "HC-OT": 6330, "RW-SS": 2300, "RW-OT": 6720, "MF-SS": 3470, "MF-OT": 8080, "CN-SS": 4840,
          "CN-OT": 12910}
    for s in K.PROG:
        n = WD.intakes_window(W.claims, s, dt.date(2025, 10, 1), K.EXTRACT_END) * 1.025
        tot += n * pp[s] * 1.04 ** 2
    return tot


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or WD.simulate()
    counts = {}
    counts[K.EXTRACT] = K.write_csv(p(K.EXTRACT), R.EXTRACT_COLS, R.extract_rows(W))
    counts[K.NURSE_LOG] = K.write_csv(p(K.NURSE_LOG), R.NURSE_COLS, R.nurse_rows(W), crlf=True)
    counts[K.CROSSWALK] = K.write_csv(p(K.CROSSWALK), R.CROSS_COLS, R.crosswalk_rows())
    counts[K.PAYMENTS] = K.write_csv(p(K.PAYMENTS), R.PAY_COLS, R.payment_rows(W))
    counts[K.ACH_RETURNS] = K.write_csv(p(K.ACH_RETURNS), R.ACH_COLS, R.ach_rows(W), crlf=True)
    counts[K.MERGES] = K.write_csv(p(K.MERGES), R.MERGE_COLS, R.merge_rows(W))
    counts[K.SURVEY] = K.write_csv(p(K.SURVEY), R.SURVEY_COLS, R.survey_rows(W), crlf=True)
    counts[K.REGISTER] = len(DOC.write_register(p(K.REGISTER), W))
    sheets = DOC.write_review_book(p(K.REVIEW_BOOK), W)
    counts[K.REVIEW_BOOK] = sum(len(v) for v in sheets.values())
    frame_n = sum(1 for i in W.pilot_ids if W.claims[i].ind)
    sample_n = sum(len(v) for v in sheets.values())
    open_n = sum(1 for v in sheets.values() for r in v if r[2] == "Open")
    total = sum(r[3] + r[4] + r[5] for v in sheets.values() for r in v)
    DOC.write_review(p(K.REVIEW_PDF), frame_n, sample_n, open_n, total)
    DOC.write_charter(p(K.CHARTER))
    DOC.write_charter_draft(p(K.CHARTER_DRAFT_DOC))
    DOC.write_pick_memo(p(K.PICK_MEMO), pick_total(W))
    DOC.write_dictionary(p(K.DICTIONARY))
    DOC.write_staffing(p(K.STAFFING))
    files = [
        (K.EXTRACT, "Claims listing: claims reported January 2021 to September 2026 with time lost at first report or "
                    "indemnity paid or reserved", "Claims system", "2026-09-30", K.PEOPLE["data"]),
        (K.MERGES, "Claims merged on the claims system in 2025", "Claims system", "2026-09-30", K.PEOPLE["data"]),
        (K.REGISTER, "ERN pilot assignment register", "Triage screen", "2025-03-07", K.PEOPLE["claimsops"]),
        (K.NURSE_LOG, "ERN pilot case log", "ERN case system", "2025-08-04", K.PEOPLE["clinical"]),
        (K.REVIEW_BOOK, "Kellerman Pryce verification workbook", K.KPA, "2026-06-30", K.PEOPLE["kpa"]),
        (K.REVIEW_PDF, "Kellerman Pryce report on the pilot verification", K.KPA, "2026-08-14", K.PEOPLE["kpa"]),
        (K.CHARTER, "ERN programme charter 2027, signed", "Medical Case Management", "2026-10-19", K.PEOPLE["director"]),
        (K.CHARTER_DRAFT_DOC, "ERN programme charter 2027, draft v3", "Medical Case Management", "2026-09-18",
         K.PEOPLE["director"]),
        (K.PICK_MEMO, "AY2027 indemnity pick: the ERN credit", "Pricing and Reserving", "2026-10-28", K.PEOPLE["pricing"]),
        (K.CROSSWALK, "Segment code crosswalk at the 2025 upgrade", "Data Engineering", "2025-06-02", K.PEOPLE["data"]),
        (K.PAYMENTS, "Indemnity payments issued January to September 2026", "Payment register", "2026-09-30",
         K.PEOPLE["data"]),
        (K.ACH_RETURNS, "ACH returns on workers' compensation EFT payments", "Bank return file", "2026-09-30",
         "Treasury"),
        (K.DICTIONARY, "Field definitions", "Data Engineering", "2026-10-02", K.PEOPLE["data"]),
        (K.SURVEY, "ERN pilot worker survey", "ERN case system", "2025-08-04", K.PEOPLE["clinical"]),
        (K.STAFFING, "2027 ERN staffing plan", "Medical Case Management", "2026-10-30", K.PEOPLE["director"]),
    ]
    DOC.write_manifest(p(K.MANIFEST), files)
    PP.normalize_ooxml(p(K.REGISTER), K.PEOPLE["claimsops"], K.PEOPLE["claimsops"], "2023-02-21T15:12:40Z",
                       "2025-03-07T21:44:18Z", excel=True)
    PP.normalize_ooxml(p(K.REVIEW_BOOK), K.PEOPLE["kpa"], K.PEOPLE["kpa"], "2026-05-11T13:20:02Z",
                       "2026-08-13T22:05:37Z", excel=True, company=K.KPA)
    PP.normalize_ooxml(p(K.DICTIONARY), K.PEOPLE["data"], K.PEOPLE["data"], "2025-05-19T14:02:11Z",
                       "2026-10-02T16:31:50Z", excel=True)
    PP.normalize_ooxml(p(K.STAFFING), K.PEOPLE["director"], K.PEOPLE["director"], "2026-08-24T17:40:05Z",
                       "2026-10-30T19:12:44Z", excel=True)
    PP.normalize_docx(p(K.CHARTER_DRAFT_DOC), K.PEOPLE["director"], K.PEOPLE["director"], "2026-09-02T15:10:00Z",
                      "2026-09-18T20:41:00Z", revision=9, total_time=143, pages=1, seed="charter-draft-v3",
                      title="ERN charter 2027 draft v3")
    PP.normalize_pdf(p(K.CHARTER), b"D:20261019160512-05'00'", b"D:20261019161144-05'00'")
    PP.normalize_pdf(p(K.PICK_MEMO), b"D:20261028093015-05'00'", b"D:20261028094207-05'00'")
    PP.normalize_pdf(p(K.REVIEW_PDF), b"D:20260814101530-05'00'", b"D:20260814102422-05'00'")
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
    print("byte-identical rebuild: target, golden, metadata.json, figures.json, target.zip (%s)" % allh.hexdigest()[:16])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
