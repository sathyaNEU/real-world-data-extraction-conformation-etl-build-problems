"""Build task143: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task143/generator/build.py              everything
    python3 task143/generator/build.py --out DIR    the pack only, into DIR"""
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
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import field as FD          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 10, 12, 14, 25, tzinfo=dt.timezone.utc)   # 16:25 in Bielefeld, the pack assembled

FILES = [
    (K.F_POLICY, "FIN-RS-04 Battery warranty reserve at lot release, revision 3", "Product Finance, Notebook Division"),
    (K.F_MEMO, "QM-07 Release model RL-3 for Zelvora ZP-4820 cells, revision 4 of 30 September 2026",
     "Battery Reliability Lab"),
    (K.F_SPEC, "Model K battery pack specification, revision D", "Product Engineering, Battery Plant"),
    (K.F_CYC_A, "First 100 QP-3 cycles of every release-test cell run on cycler fleet A, lots ZC2437 to ZC2638",
     "Battery Reliability Lab, fleet A cycler software export"),
    (K.F_CYC_B, "First 100 QP-3 cycles of every release-test cell run on cycler fleet B, lots ZC2506 to ZC2638",
     "Battery Reliability Lab, fleet B cycler software export"),
    (K.F_REG, "Release test register: every release-test cell, its lot, formation tray, fleet, channel and start",
     "Battery Reliability Lab"),
    (K.F_LIFE, "Life test results of the release-test cells of the lots whose life tests have finished (ZC2437 to "
     "ZC2614)", "Battery Reliability Lab, life monitoring"),
    (K.F_CELLS, "Zelvora cell data package for lot ZC2638: every cell formed, its formation tray and formation "
     "measurements", "Zelvora Cell s.r.o."),
    (K.F_GEN, "Genealogy of the Model K packs built from lot ZC2638, one row per cell", "Battery Plant, line MES"),
    (K.F_MODEL_J, "Genealogy of the Model J packs built from lot ZC2638, one row per cell", "Battery Plant, line MES"),
    (K.F_COA, "Zelvora certificate of analysis for lot ZC2638", "Zelvora Cell s.r.o., Quality"),
    (K.F_CASES, "Service cases on K14 and K15 batteries, September 2024 to September 2026", "Service case system"),
    (K.F_SAP, "DACH depot service orders on K14 and K15 batteries, September 2024 to 1 March 2026",
     "DACH service depot, SAP"),
    (K.F_RETURNS, "Batteries received at the Bielefeld returns depot, September 2024 to October 2026",
     "Returns depot, Bielefeld"),
    (K.F_CARRIER, "Carrier statement: inbound consignments of returned batteries, September 2025 to October 2026",
     "Carrier statement to Service Operations"),
    (K.F_INV["FRB"], "Dauvergne Réparation invoices, September 2025 to September 2026", "Dauvergne Réparation SAS"),
    (K.F_INV["UKI"], "Tolley Marsh Repair invoices, September 2025 to September 2026", "Tolley Marsh Repair Ltd"),
    (K.F_INV["NOR"], "Ljungqvist Service invoices, September 2025 to September 2026", "Ljungqvist Service AB"),
    (K.F_INV["SOU"], "Ferrucci Assistenza invoices, September 2025 to September 2026", "Ferrucci Assistenza S.r.l."),
    (K.F_FX, "Treasury month-end exchange rates, January 2025 to September 2026", "Treasury"),
    (K.F_COST, "Service cost sheet FY2026", "Service Operations controlling"),
]


LAB_FILES = {K.F_POLICY, K.F_MEMO, K.F_SPEC, K.F_CYC_A, K.F_CYC_B, K.F_REG, K.F_LIFE, K.F_CELLS, K.F_GEN, K.F_MODEL_J,
             K.F_COA}


def world():
    W = WD.simulate()
    FD.simulate_field(W)
    FD.simulate_money(W)
    return W


def fit_memo(out):
    """RL-3 fitted on the shipped records, as the lab fitted it, and its leave-one-lot-out validation."""
    import math
    import numpy as np
    cyc = C.cycles(out)
    feat = C.features(cyc)
    lifes = C.life(out)
    beta, X, y, keys = C.fit_ols(feat, lifes)
    beta = [round(float(b), 4) for b in beta]
    rmse = C.lolo_rmse(feat, lifes)
    lots = sorted({L["lot"] for L in lifes.values()}, key=K.LOTS.index)
    table, means = [], []
    for lot in lots:
        others = [l for l in lots if l != lot]
        b, *_ = C.fit_ols(feat, lifes, others)
        errs = []
        for cell, L in lifes.items():
            if L["lot"] == lot and L["status"] == "EOL":
                f1, f2 = feat[cell]
                errs.append(math.log(float(L["cycles"])) - (b[0] + b[1] * f1 + b[2] * f2))
        errs = np.array(errs)
        means.append(errs.mean())
        table.append([lot, K.lot_release(lot).strftime("%d.%m.%Y"), str(len(errs)), "%+.3f" % errs.mean(),
                      "%.3f" % math.sqrt((errs ** 2).mean())])
    n_cells = len(y)
    n_stop = sum(1 for L in lifes.values() if L["status"] == "STOPPED")
    lo, hi = min(means), max(means)
    rng_err = ("%+.2f" % (math.floor(lo * 100) / 100), "%+.2f" % (math.ceil(hi * 100) / 100))
    model = {"b0": beta[0], "b1": beta[1], "b2": beta[2], "rmse": round(rmse, 3)}
    return model, table, n_cells, n_stop, rng_err


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or world()
    counts = {}
    a_rows, b_rows = R.cycle_rows(W)
    counts[K.F_CYC_A] = K.write_csv(p(K.F_CYC_A), R.CYC_A_COLS, a_rows, crlf=True, delimiter=";")
    counts[K.F_CYC_B] = K.write_csv(p(K.F_CYC_B), R.CYC_B_COLS, b_rows)
    counts[K.F_REG] = K.write_csv(p(K.F_REG), R.REG_COLS, R.register_rows(W))
    counts[K.F_LIFE] = K.write_csv(p(K.F_LIFE), R.LIFE_COLS, R.life_rows(W))
    counts[K.F_CELLS] = K.write_csv(p(K.F_CELLS), R.CELL_COLS, R.cell_package_rows(W))
    counts[K.F_GEN] = K.write_csv(p(K.F_GEN), R.GEN_COLS, R.genealogy_rows(W))
    counts[K.F_MODEL_J] = K.write_csv(p(K.F_MODEL_J), R.GEN_COLS, R.model_j_rows(W))
    counts[K.F_CASES] = K.write_csv(p(K.F_CASES), R.CASE_COLS, R.case_rows(W))
    R.write_sap(p(K.F_SAP), R.sap_rows(W))
    R.write_returns(p(K.F_RETURNS), W)
    counts[K.F_CARRIER] = K.write_csv(p(K.F_CARRIER), R.CARRIER_COLS, R.carrier_rows(W))
    counts[K.F_FX] = K.write_csv(p(K.F_FX), R.FX_COLS, R.fx_rows(W))
    R.write_cost_sheet(p(K.F_COST))
    for reg, f in K.F_INV.items():
        R.write_invoice_book(p(f), FD.PARTNER[reg], W)
    DOC.write_policy(p(K.F_POLICY))
    DOC.write_spec(p(K.F_SPEC))
    DOC.write_coa(p(K.F_COA), W)
    model, table, n_cells, n_stop, rng_err = fit_memo(out)
    W.memo = (model, table, n_cells, n_stop, rng_err)
    DOC.write_memo(p(K.F_MEMO), model, table, n_cells, n_stop, rng_err)
    DOC.write_readme(p(K.F_README), [f for f in FILES if f[0] in LAB_FILES and f[0] != K.F_POLICY])
    DOC.write_service_readme(p(K.F_README_SVC), [f for f in FILES if f[0] not in LAB_FILES])
    P = K.PEOPLE
    PP.normalize_ooxml(p(K.F_SAP), "SAP Export", P["service"], "2026-10-05T07:12:41Z", "2026-10-05T07:12:41Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(K.F_RETURNS), "Returns Depot", P["service"], "2024-09-30T06:48:02Z", "2026-10-09T13:20:17Z",
                       excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(K.F_COST), P["service"], P["service"], "2025-09-24T10:03:55Z", "2026-01-08T15:41:30Z",
                       excel=True, company=K.COMPANY)
    stamps = {"FRB": ("Comptabilité Dauvergne", "2026-10-06T08:51:12Z", "Dauvergne Réparation SAS"),
              "UKI": ("Tolley Marsh Accounts", "2026-10-07T09:02:44Z", "Tolley Marsh Repair Ltd"),
              "NOR": ("Ekonomi Ljungqvist", "2026-10-06T12:30:05Z", "Ljungqvist Service AB"),
              "SOU": ("Amministrazione", "2026-10-08T07:40:29Z", "Ferrucci Assistenza S.r.l.")}
    for reg, f in K.F_INV.items():
        who, when, comp = stamps[reg]
        PP.normalize_ooxml(p(f), who, who, "2025-11-03T09:00:00Z", when, excel=True, company=comp)
    PP.normalize_pdf(p(K.F_POLICY), b"D:20250318094412+01'00'", b"D:20250318095030+01'00'")
    PP.normalize_pdf(p(K.F_MEMO), b"D:20260930161205+02'00'", b"D:20260930163348+02'00'")
    PP.normalize_pdf(p(K.F_SPEC), b"D:20250314111827+01'00'", b"D:20250314112601+01'00'")
    PP.normalize_pdf(p(K.F_COA), b"D:20260922084015+02'00'", b"D:20260922084122+02'00'")
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
