"""Build task148: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task148/generator/build.py              everything
    python3 task148/generator/build.py --out DIR    the pack only, into DIR"""
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
import asks as AS           # noqa: E402
import cast as CA           # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 10, 5, 20, 41, tzinfo=dt.timezone.utc)     # 4.41 pm on 5 October 2026, Eastern
F_README = DOC.F_README


class World:
    pass


def world():
    Wd = World()
    Wd.W = WD.simulate()
    Wd.I = R.ids(Wd.W)
    Wd.C = CA.build(Wd.W)
    Wd.S = R.sold(Wd.W)
    Wd.A = AS.build_1112(Wd.W, Wd.I, Wd.C)
    Wd.B = AS.build_workout(Wd.W, Wd.I, Wd.C, Wd.S)
    return Wd


FILES = [
    (R.F_CURRENT, "Current servicing system, month-end loan history, October 2017 to September 2026."),
    (R.F_LEGACY, "Legacy core, month-end loan history, October 2009 to October 2017."),
    (R.F_CODES, "Servicing status codes, both systems."),
    (R.F_MASTER, "SBA Lending portfolio register: every 7(a) loan approved from October 2009 and disbursed by 30 September 2026."),
    (R.F_REGISTER, "Loan documentation system, guarantee register, as at 30 September 2026."),
    (DOC.F_POLICY, "Credit policy CP-SBA-07, allowance for credit losses on SBA 7(a) unguaranteed portions (version 4)."),
    (DOC.F_TERMS, "SBA loan authorization, Part B standard terms (form SBL-AUTH-B, March 2018)."),
    (AS.F_CARES, "SBA fiscal transfer agent, Section 1112 remittance detail, CARES Act payments."),
    (AS.F_EAA, "SBA fiscal transfer agent, Section 1112 remittance detail, Economic Aid Act payments."),
    (AS.F_CREDITS, "Treasury management, credits to the SBA settlement account, October 2019 to September 2026."),
    (AS.F_LEDGER, "Special Assets, charge-off and recovery entries, fiscal 2020 to fiscal 2026."),
    (AS.F_PAYSBA, "Accounts payable and treasury management, payments to SBA, October 2019 to September 2026."),
    (R.F_1502, "Form 1502 report to SBA's fiscal transfer agent for September 2026."),
    (R.F_SECMKT, "Secondary market settlements of guaranteed portions sold."),
    (R.F_MANIFEST, "Export manifest."),
    (F_README, "This file."),
]


def build(out, quiet=False, Wd=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    Wd = Wd or world()
    W, I, C, S, A, B = Wd.W, Wd.I, Wd.C, Wd.S, Wd.A, Wd.B
    counts = {}
    counts[R.F_CURRENT] = R.write_current(p(R.F_CURRENT), W, I)
    counts[R.F_LEGACY] = R.write_legacy(p(R.F_LEGACY), W, I)
    counts[R.F_CODES] = K.write_csv(p(R.F_CODES), ["system", "code", "description"], R.code_rows())
    counts[R.F_MASTER] = K.write_csv(p(R.F_MASTER), R.MASTER_COLS, R.master_rows(W, I, C))
    reg = R.register_rows(W, I, C)
    DOC.write_register(p(R.F_REGISTER), R.REGISTER_COLS, reg)
    counts[R.F_REGISTER] = len(reg)
    DOC.write_policy(p(DOC.F_POLICY))
    DOC.write_terms(p(DOC.F_TERMS))
    counts[AS.F_CARES] = K.write_csv(p(AS.F_CARES), AS.CARES_COLS, AS.cares_rows(W, I, C, A), crlf=True)
    eaa = AS.eaa_rows(W, I, C, A)
    DOC.write_eaa(p(AS.F_EAA), AS.EAA_COLS, eaa)
    counts[AS.F_EAA] = len(eaa)
    counts[AS.F_CREDITS] = K.write_csv(p(AS.F_CREDITS), AS.CREDIT_COLS, AS.credit_rows(W, I, A, B, S))
    counts[AS.F_LEDGER] = K.write_csv(p(AS.F_LEDGER), AS.LEDGER_COLS, AS.ledger_rows(W, I, C, B))
    counts[AS.F_PAYSBA] = K.write_csv(p(AS.F_PAYSBA), AS.PAYSBA_COLS, AS.paysba_rows(W, I, B))
    counts[R.F_1502] = K.write_csv(p(R.F_1502), R.F1502_COLS, R.form1502_rows(W, I, C))
    counts[R.F_SECMKT] = K.write_csv(p(R.F_SECMKT), R.SECMKT_COLS, R.secmkt_rows(W, I, S))
    man = []
    for f, d in FILES:
        if f in (R.F_MANIFEST, F_README):
            continue
        man.append({"file": f, "description": d, "rows": counts.get(f, ""), "extracted": "2026-10-05"})
    counts[R.F_MANIFEST] = K.write_csv(p(R.F_MANIFEST), ["file", "description", "rows", "extracted"], man)
    with open(p(F_README), "w", encoding="utf-8", newline="") as fh:
        fh.write(DOC.readme_text(FILES))
    P = K.PEOPLE
    PP.normalize_pdf(p(DOC.F_POLICY), b"D:20240723101544-04'00'", b"D:20240726142210-04'00'")
    PP.normalize_pdf(p(DOC.F_TERMS), b"D:20180305091102-05'00'", b"D:20180312163327-04'00'")
    PP.normalize_ooxml(p(R.F_REGISTER), "Loan Documentation", "Loan Documentation", "2019-02-11T15:20:44Z",
                       "2026-10-05T19:58:12Z", excel=True, company=K.BANK)
    PP.normalize_ooxml(p(AS.F_EAA), "Colson Services Corp.", P["loanops"], "2021-03-09T13:04:51Z",
                       "2022-06-14T18:37:05Z", excel=True, company=K.BANK)
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
    stamp = dt.datetime(2026, 10, 7, 14, 12, tzinfo=dt.timezone.utc).timestamp()
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
