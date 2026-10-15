"""Build task145: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task145/generator/build.py              everything
    python3 task145/generator/build.py --out DIR    the pack only, into DIR"""
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
import field as FD          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 10, 9, 19, 42, tzinfo=dt.timezone.utc)   # 15:42 in Mississauga, the pack assembled


class Field:
    pass


def world():
    W = WD.simulate()
    F = Field()
    F.staff = FD.build_staff()
    F.lines = FD.apply_new_system(FD.simulate_time(F.staff, WD.FED_HOLIDAYS))
    F.entries, F.stmts, F.flagged = FD.simulate_brandmoor(WD.FED_HOLIDAYS)
    return W, F


def build(out, quiet=False, WF=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W, F = WF or world()
    counts = {}
    hv = R.hv_rows(W)
    for q, f in R.F_HV.items():
        cols = R.HV_OLD if q in R.OLD_LAYOUT else R.HV_NEW
        counts[f] = K.write_csv(p(f), cols, hv[q])
    DOC.write_gw_legacy(p(R.F_GW_LEGACY), R.gw_legacy_rows(W))
    counts[R.F_GW_NEW] = K.write_csv(p(R.F_GW_NEW), R.GW_NEW, R.gw_new_rows(W))
    DOC.write_plan(p(R.F_PLAN27), W, 2027)
    DOC.write_plan(p(R.F_PLAN26), W, 2026)
    DOC.write_standard(p(R.F_STD))
    DOC.write_routing(p(R.F_CLR))
    DOC.write_clearance_note(p(R.F_NOTE_CLR))
    old, new = R.ta_rows(F.staff, F.lines)
    counts[R.F_TA_OLD] = K.write_csv(p(R.F_TA_OLD), R.TA_OLD, old, crlf=True)
    counts[R.F_TA_NEW] = K.write_csv(p(R.F_TA_NEW), R.TA_NEW, new)
    DOC.write_hr_staff(p(R.F_HR_STAFF), F.staff)
    counts[R.F_HR_CHG] = K.write_csv(p(R.F_HR_CHG), R.HR_CHG, R.hr_change_rows(F.staff))
    counts[R.F_CC] = K.write_csv(p(R.F_CC), R.CC_COLS, R.cc_rows())
    DOC.write_payroll_note(p(R.F_NOTE_PAY))
    DOC.write_statements(p(R.F_BCS_PDF), F.stmts)
    counts[R.F_BCS_PORTAL] = R.write_portal(p(R.F_BCS_PORTAL), F.stmts)
    DOC.write_ap(p(R.F_AP), R.ap_rows(F.stmts, WD.FED_HOLIDAYS))
    DOC.write_rate_schedule(p(R.F_BCS_RATES))
    counts[R.F_EXPORTS] = K.write_csv(p(R.F_EXPORTS), R.EXPORTS, R.export_rows(W))
    P = K.PEOPLE
    PP.normalize_ooxml(p(R.F_GW_LEGACY), "BX4 Reports", "BX4 Reports", "2024-10-03T13:05:12Z", "2024-10-03T13:05:12Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(R.F_PLAN27), P["network"], P["network"], "2026-08-24T14:31:07Z", "2026-09-18T16:02:44Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(R.F_PLAN26), P["network"], P["network"], "2025-08-26T13:12:50Z", "2025-09-19T15:47:21Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(R.F_HR_STAFF), "HR Reporting", P["hrsys"], "2026-10-06T12:55:03Z", "2026-10-06T13:08:41Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(R.F_AP), "AP Reporting", "AP Reporting", "2026-10-06T14:20:16Z", "2026-10-06T14:20:16Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_pdf(p(R.F_STD), b"D:20250317101422-04'00'", b"D:20260918094117-04'00'")
    PP.normalize_docx(p(R.F_CLR), P["clearance"], P["clearance"], "2024-10-08T12:41:00Z", "2024-10-15T13:12:00Z",
                      revision=5, total_time=74, seed="task145/clr-ops-11",
                      title="CLR-OPS-11 Valuation, routing and the high-value check", company=K.COMPANY)
    PP.normalize_pdf(p(R.F_BCS_RATES), b"D:20260112140533-05'00'", b"D:20260112140533-05'00'")
    PP.normalize_pdf(p(R.F_BCS_PDF), b"D:20260406111904-04'00'", b"D:20260406111904-04'00'")
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    W.counts = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return W, F


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
    W, F = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    G = DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                os.path.join(root, "generator", "figures.json"), W=W, staff=F.staff, lines=F.lines, stmts=F.stmts)
    P = K.PEOPLE
    PP.normalize_ooxml(os.path.join(root, "golden", DL.GOLD_BOOK), P["planner"], P["planner"], "2026-10-13T13:40:22Z",
                       "2026-10-15T18:12:05Z", excel=True, company=K.COMPANY)
    PP.normalize_ooxml(os.path.join(root, "golden", DL.GOLD_DECK), P["planner"], P["planner"], "2026-10-14T15:02:48Z",
                       "2026-10-15T18:20:31Z", company=K.COMPANY)
    stamp = dt.datetime(2026, 10, 15, 18, 25, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return W, F, G


def main():
    import checks as CK
    import verify as V
    W, F, G = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), W=W, F=F, G=G,
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
            dt_ = digest(os.path.join(TASK, "target")); d2 = digest(os.path.join(tmp, "target"))
            dg = digest(os.path.join(TASK, "golden")); dg2 = digest(os.path.join(tmp, "golden"))
            raise SystemExit("second build differs: target %s, golden %s, %s; %s" % (
                same_t, same_g, same, [f for f in dt_ if dt_[f] != d2.get(f)] + [f for f in dg if dg[f] != dg2.get(f)]))
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
