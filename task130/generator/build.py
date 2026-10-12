"""Build task130: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte.

    python3 task130/generator/build.py              everything
    python3 task130/generator/build.py --out DIR    the pack only, into DIR"""
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
import carrier as CR       # noqa: E402
import claims as C         # noqa: E402
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as WD         # noqa: E402

TASK = os.path.dirname(HERE)
CLAIMS_SEED = 3671         # chosen by the seed search (the design note's build record)
EXPORT_STAMP = dt.datetime(2026, 10, 12, 16, 20, tzinfo=dt.timezone.utc)   # 9:20 am Pacific, the pack's hand-off
JUNE = dt.date(2026, 6, 30)


def simulate(seed=None):
    K.CLAIMS_SEED = CLAIMS_SEED if seed is None else seed
    W = WD.build()
    incidents, notice_only = C.simulate(W)
    C.valuation(incidents)
    C.valuation(incidents, JUNE, "jun")
    sep = CR.records(incidents, notice_only, K.VALUATION, "v")
    jun = CR.records(incidents, notice_only, JUNE, "jun")
    return dict(W=W, incidents=incidents, notice_only=notice_only, rows=C.register(incidents), plan=WD.plan_2027(W),
                sep=sep, jun=jun, nums=CR.number(sep))


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    w = world or simulate()
    W = w["W"]
    counts = {}
    counts[K.REGISTER] = R.write_csv(p(K.REGISTER), R.REGISTER_COLS, R.register_rows(w["rows"]))
    counts[K.PAYROLL] = R.write_csv(p(K.PAYROLL), R.PAYROLL_COLS, R.payroll_rows(W))
    counts[K.HCM] = R.write_csv(p(K.HCM), R.HCM_COLS, R.hcm_rows(W), crlf=True)
    counts[K.CROSSWALK] = R.write_csv(p(K.CROSSWALK), R.CROSSWALK_COLS, R.crosswalk_rows(), crlf=True)
    counts[K.DIRECTORY] = R.write_csv(p(K.DIRECTORY), R.DIRECTORY_COLS, R.directory_rows())
    counts[K.NOTICES] = R.write_csv(p(K.NOTICES), R.NOTICE_COLS, R.notice_rows(w["incidents"], w["notice_only"]))
    counts[K.SC_SEP] = R.write_csv(p(K.SC_SEP), R.SC_COLS, R.sc_rows(w["sep"], w["nums"], K.VALUATION), crlf=True)
    counts[K.SAFETY] = R.write_csv(p(K.SAFETY), R.SAFETY_COLS, R.safety_rows())
    D.write_plan(p(K.PLAN), w["plan"])
    counts[K.PLAN] = len(w["plan"])
    qm = lambda recs: [r for r in recs if K.ENTITIES[r["entity"]]["carrier"] == "QM"]
    D.write_qm_run(p(K.QM_SEP), qm(w["sep"]), w["nums"], K.VALUATION, dt.date(2026, 10, 6))
    D.write_qm_run(p(K.QM_JUN), qm(w["jun"]), w["nums"], JUNE, dt.date(2026, 10, 9),
                   revision="Revision 1 of the run valued 06/30/2026: replaces the run of 07/08/2026 (expense reserves restated)")
    counts[K.QM_SEP], counts[K.QM_JUN] = len(qm(w["sep"])), len(qm(w["jun"]))
    D.write_premiums(p(K.PREMIUMS))
    D.write_agreement(p(K.AGREEMENT))
    D.write_policy(p(K.POLICY))
    D.write_dictionary(p(K.DICTIONARY), counts)
    log = [
        (K.REGISTER, "Risk management claims system (claims register)", "2026-10-02", counts[K.REGISTER],
         "Claims and Litigation", "clinician defendants on every claim number, valued 30 September 2026"),
        (K.PAYROLL, "Legacy payroll (closed December 2025)", "2026-10-02", counts[K.PAYROLL], "HR Systems",
         "employed clinicians, residents, fellows and psychologists, January 2016 to December 2025"),
        (K.HCM, "HCM payroll", "2026-10-02", counts[K.HCM], "HR Systems",
         "clinician pay lines, work months January to September 2026"),
        (K.CROSSWALK, "HCM job architecture", "2026-10-02", counts[K.CROSSWALK], "HR Systems",
         "HCM job profiles to legacy job codes"),
        (K.DIRECTORY, "General ledger", "2026-10-02", counts[K.DIRECTORY], "Finance", "cost centres, all entities"),
        (K.PLAN, "Financial Planning and Analysis", "2026-09-29", counts[K.PLAN], "Finance",
         "covered clinician FTE plan for 2027"),
        (K.NOTICES, "Risk management claims system (notices)", "2026-10-02", counts[K.NOTICES],
         "Claims and Litigation", "precautionary notices to carriers, 2012 to September 2026"),
        (K.QM_SEP, K.CARRIERS["QM"], "2026-10-06", counts[K.QM_SEP], "received from carrier",
         "loss run valued 30 September 2026"),
        (K.QM_JUN, K.CARRIERS["QM"], "2026-10-09", counts[K.QM_JUN], "received from carrier",
         "loss run valued 30 June 2026, revision 1"),
        (K.SC_SEP, K.CARRIERS["SC"], "2026-10-05", counts[K.SC_SEP], "received from carrier",
         "loss run valued 30 September 2026"),
        (K.SAFETY, "Patient safety reporting system", "2026-10-02", counts[K.SAFETY], "Quality and Patient Safety",
         "safety event reports, January 2019 to September 2026"),
        (K.PREMIUMS, "Risk Management and Insurance", "2026-10-02", "", "Risk Management and Insurance",
         "clinician professional liability premiums 2017 to 2026"),
        (K.AGREEMENT, "Office of the General Counsel", "2026-08-14", "", "Office of the General Counsel",
         "trust agreement as executed, extract"),
        (K.POLICY, "Trust secretary", "2026-09-22", "", "Trust secretary", "funding policy as adopted"),
        (K.DICTIONARY, "Risk Management and Insurance", "2026-10-02", "", "Claims and Litigation",
         "field definitions for these extracts"),
    ]
    R.write_csv(p(K.EXTRACT_LOG), R.EXTRACT_LOG_COLS, log)
    PP.normalize_ooxml(p(K.PLAN), K.PEOPLE["cfo"], K.PEOPLE["cfo"], "2026-08-31T22:14:09Z", "2026-09-29T23:02:51Z",
                       excel=True)
    PP.normalize_ooxml(p(K.QM_SEP), "QMPL Claims Reporting", "QMPL Claims Reporting", "2026-10-06T14:31:12Z",
                       "2026-10-06T14:31:12Z", excel=True)
    PP.normalize_ooxml(p(K.QM_JUN), "QMPL Claims Reporting", "QMPL Claims Reporting", "2026-10-09T15:07:40Z",
                       "2026-10-09T15:07:40Z", excel=True)
    PP.normalize_ooxml(p(K.PREMIUMS), K.PEOPLE["requester"], K.PEOPLE["requester"], "2021-03-16T17:40:00Z",
                       "2026-10-01T21:18:33Z", excel=True)
    PP.normalize_pdf(p(K.AGREEMENT), b"D:20260812153012-07'00'", b"D:20260814101544-07'00'")
    PP.normalize_pdf(p(K.POLICY), b"D:20260918094502-07'00'", b"D:20260922161730-07'00'")
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)),
                                          ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(folder))}


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
            os.path.join(root, "generator", "figures.json"), world=world)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
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
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
        allh.hexdigest()[:16]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
