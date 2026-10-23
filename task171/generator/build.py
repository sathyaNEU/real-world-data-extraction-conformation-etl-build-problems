"""Build task171: target/ (the evidence pack), golden/ (the deliverable), metadata.json, generator/figures.json,
submission.md, then the checks and the independent verifier, then a second build compared byte for byte, then
target.zip.

    python3 task171/generator/build.py             everything
    python3 task171/generator/build.py --pack-only the pack, the golden and figures.json, no checks"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402

ZIP_STAMP = (2026, 11, 12, 9, 14, 0)
MONTHS_A = list(range(1, 10))


def write_pack(out):
    import numpy as np
    import pandas as pd
    import world, pack, docs
    W = world.build()
    P = pack.build_pack(W, out)
    rng = np.random.default_rng(C.SEED + 2)
    pack.lanes().to_csv(os.path.join(out, C.F_LANES), index=False, lineterminator="\n")
    pack.traffic(W, rng).to_csv(os.path.join(out, C.F_TRAFFIC), index=False, lineterminator="\n")
    pack.image_review(W, rng).to_csv(os.path.join(out, C.F_IMG), index=False, lineterminator="\n")
    docs.write_pdf(os.path.join(out, C.F_POLICY), docs.policy_text())
    docs.write_docx(os.path.join(out, C.F_PLAN), docs.plan_items())
    rows = [(f, c, d) for f, cols in docs.DICT.items() for c, d in cols]
    docs.write_xlsx(os.path.join(out, C.F_DICT), [("fields", pd.DataFrame(rows, columns=["file", "field", "definition"]))])
    man = [
        (C.F_LINES, "Toll-by-mail back office", "2026-11-09", "Crossings billed by mail, 3 March 2025 to 30 September 2026", "One row per billed crossing"),
        (C.F_INV, "Toll-by-mail back office", "2026-11-09", "Invoices issued April 2025 to October 2026", "Status at 31 October 2026"),
        (C.F_PAY, "Toll-by-mail back office", "2026-11-09", "Payments posted from April 2025", "Includes postings to the export run"),
        (C.F_MVD, "Division of Motor Vehicles hold returns", "2026-11-02", "Hold requests from June 2025 to 31 October 2026", ""),
        (C.F_AGY, "Collection agency placement file", "2026-11-04", "Placements from July 2025 to 31 October 2026", ""),
        (C.F_TAG, "MarrowPass account system", "2026-11-06", "Commercial account postings in the express lanes, January to September 2026", ""),
        (C.F_LANES, "Toll systems", "2026-11-06", "Plaza lane table", ""),
        (C.F_TRAFFIC, "Traffic and revenue", "2026-10-20", "Plaza transactions by month and hour, January 2025 to September 2026", ""),
        (C.F_IMG, "Image review", "2026-11-05", "Captures by month of crossing, March 2025 to September 2026", ""),
        (C.F_POLICY, "Office of Toll Revenue", "2026-02-02", "Resolution 2025-31 as amended", ""),
        (C.F_PLAN, "AET programme", "2026-11-10", "Programme note PN-14", ""),
        (C.F_DICT, "Toll systems", "2026-11-12", "Field definitions for the extracts", ""),
    ]
    pd.DataFrame(man, columns=["file", "source_system", "extracted", "covers", "notes"]).to_csv(os.path.join(out, C.F_MAN), index=False, lineterminator="\n")
    return W, P


def solve_all(tdir):
    import solve
    F = solve.frames(tdir)
    g = solve.golden(F)
    V = solve.straddle_and_phantom(F)
    A = solve.ask_A(F, V)
    B = solve.ask_B(F, V)
    return F, g, A, B


def figures(g, A, B):
    fig = {"call_collected_toll_2027_usd": int(round(g["collected"] / 250_000) * 250_000),
           "call_share_in_state_pct": int(round(g["IS"] * 100)),
           "call_share_out_of_state_pct": int(round(g["OS"] * 100)),
           "collected_unrounded": round(g["collected"], 0), "share_in_state_unrounded": round(g["IS"] * 100, 2),
           "share_out_of_state_unrounded": round(g["OS"] * 100, 2),
           "plan_toll_in_state_usd": C.PLAN_TOLL["IS"], "plan_toll_out_of_state_usd": C.PLAN_TOLL["OS"],
           "early_share_in_state_pct": round(g["parts"]["early"] * 100, 1), "renewal_share_in_state_pct": round(g["parts"]["renew"] * 100, 1),
           "collected_toll_2027_million": round(round(g["collected"] / 250_000) * 0.25, 2), "rounding_unit_million": 0.25,
           "split_window_seconds": 0.4, "straddle_window_seconds": 1}
    for mo in MONTHS_A:
        n, t = A[mo]
        fig["a_2026_%02d_crossings" % mo] = n
        fig["a_2026_%02d_toll_owed_usd" % mo] = round(t, 2)
    for q, v in B.items():
        fig["b_%s_collected_pct" % q.lower()] = int(round(v * 100))
    return fig


def write_golden(fig, gdir):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    import docs
    os.makedirs(gdir, exist_ok=True)
    bold = Font(bold=True); head = PatternFill("solid", fgColor="DDE7EE"); thin = Border(bottom=Side(style="thin", color="7F7F7F"))
    n = lambda x: "{:,}".format(x)
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Certificate 2027"
    ws["A1"] = "Toll-by-mail, cash lanes' users, 2027: $%.2f million of the $%.1f million billed will be collected" % (
        fig["call_collected_toll_2027_usd"] / 1e6, (C.PLAN_TOLL["IS"] + C.PLAN_TOLL["OS"]) / 1e6)
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "For the 2027 revenue certificate, toll-by-mail line. Basis as in programme note PN-14; records as at 31 October 2026."
    ws["A2"].font = Font(italic=True, color="595959")
    ws.append([])
    ws.append(["", "Toll billed by mail in 2027 (Traffic, PN-14)", "Share eventually collected", "Toll collected"])
    for c in ws[4]:
        c.font = bold; c.fill = head; c.border = thin; c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.append(["Plates registered in this state", C.PLAN_TOLL["IS"], fig["share_in_state_unrounded"] / 100, "=B5*C5"])
    ws.append(["Plates registered elsewhere", C.PLAN_TOLL["OS"], fig["share_out_of_state_unrounded"] / 100, "=B6*C6"])
    ws.append(["Total", "=B5+B6", "", "=D5+D6"])
    for c in ws[7]:
        c.font = bold
    for r in (5, 6, 7):
        ws.cell(r, 2).number_format = "$#,##0"; ws.cell(r, 4).number_format = "$#,##0"
        ws.cell(r, 3).number_format = "0%"
    ws.append([])
    ws.append(["Total toll collected for the certificate, rounded to the nearest $0.25 million: $%s." % n(fig["call_collected_toll_2027_usd"])])
    ws.append(["In-state shares come from the overnight toll-by-mail invoices: the share paid within 60 days, and for invoices put on a registration hold, the share paid once the plate's registration on file had expired, so every renewal it could be collected at has passed."])
    ws.append(["Out-of-state shares come from the overnight invoices issued a year or more before 31 October 2026, by when the agency had collected or returned them."])
    for r in (9, 10, 11):
        ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 46; ws.column_dimensions["B"].width = 22; ws.column_dimensions["C"].width = 16; ws.column_dimensions["D"].width = 16
    ws.row_dimensions[4].height = 32
    ws2 = wb.create_sheet("Violations 2026")
    ws2.append(["Month of crossing", "Violation crossings", "Toll owed"])
    for c in ws2[1]:
        c.font = bold; c.fill = head; c.border = thin
    import calendar
    for mo in MONTHS_A:
        ws2.append(["%s 2026" % calendar.month_name[mo], fig["a_2026_%02d_crossings" % mo], fig["a_2026_%02d_toll_owed_usd" % mo]])
    k = len(MONTHS_A) + 1
    ws2.append(["January to September", "=SUM(B2:B%d)" % k, "=SUM(C2:C%d)" % k])
    for c in ws2[k + 1]:
        c.font = bold
    for row in ws2.iter_rows(min_row=2, min_col=2, max_col=3):
        row[0].number_format = "#,##0"; row[1].number_format = "$#,##0.00"
    ws2.append([])
    ws2.append(["A vehicle read in both express lanes is one crossing; a trailer or towed car the classifier counted separately behind a MarrowPass truck owes nothing."])
    ws2.column_dimensions["A"].width = 22; ws2.column_dimensions["B"].width = 20; ws2.column_dimensions["C"].width = 14
    ws2.freeze_panes = "A2"
    ws3 = wb.create_sheet("Violation collections")
    ws3.append(["Out-of-state violation invoices issued", "Share of toll owed collected by 31 Oct 2026"])
    for c in ws3[1]:
        c.font = bold; c.fill = head; c.border = thin; c.alignment = Alignment(wrap_text=True, vertical="top")
    labels = {"2025q2": "April to June 2025", "2025q3": "July to September 2025", "2025q4": "October to December 2025", "2026q1": "January to March 2026"}
    for q, lab in labels.items():
        ws3.append([lab, fig["b_%s_collected_pct" % q] / 100])
        ws3.cell(ws3.max_row, 2).number_format = "0%"
    ws3.append([])
    ws3.append(["Agency settlements applied oldest invoice first, toll before fees (policy 3.3 and 4.4)."])
    ws3.column_dimensions["A"].width = 36; ws3.column_dimensions["B"].width = 24; ws3.row_dimensions[1].height = 32
    ws4 = wb.create_sheet("Notes")
    for line in ["Toll only: invoice, violation, late and collection fees are budgeted separately (PN-14).",
                 "Toll billed by mail in 2027: Traffic's figures in PN-14, 2026 traffic at the 2027 rates, after image review.",
                 "Records: toll-by-mail back office export of 9 November 2026, payments posted to 31 October 2026; Division of Motor Vehicles hold returns; agency placements; MarrowPass commercial postings January to September 2026.",
                 "Policy: toll schedule and toll-by-mail policy, resolution 2025-31 as amended, sections 3 and 4."]:
        ws4.append([line])
    ws4.column_dimensions["A"].width = 120
    wb.properties.creator = "AET programme"; wb.properties.lastModifiedBy = "AET programme"
    wb.properties.created = docs.FIXED; wb.properties.modified = docs.FIXED
    p = os.path.join(gdir, "aet_2027_toll_by_mail_forecast.xlsx")
    wb.save(p); docs.normalise_zip(p, docs.FIXED)


def stamp(tdir):
    import calendar
    t = calendar.timegm(ZIP_STAMP + (0, 0, 0))
    for f in os.listdir(tdir):
        os.utime(os.path.join(tdir, f), (t, t))


def digest(tdir):
    h = hashlib.sha256()
    for f in sorted(os.listdir(tdir)):
        h.update(f.encode()); h.update(open(os.path.join(tdir, f), "rb").read())
    return h.hexdigest()


def make_zip(tdir, zpath):
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(tdir)):
            zi = zipfile.ZipInfo(f, date_time=ZIP_STAMP); zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(tdir, f), "rb").read())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--pack-only", action="store_true"); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    tdir = a.out or os.path.join(C.TASK, "target")
    if os.path.exists(tdir):
        shutil.rmtree(tdir)
    write_pack(tdir)
    stamp(tdir)
    if a.out:
        print(digest(tdir)); return
    F, g, A, B = solve_all(tdir)
    fig = figures(g, A, B)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1)
    write_golden(fig, os.path.join(C.TASK, "golden"))
    import writeup
    writeup.write(fig)
    import metadata
    metadata.write()
    if a.pack_only:
        print(json.dumps({k: fig[k] for k in list(fig)[:10]})); return
    r = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")]); assert r.returncode == 0, "checks failed"
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")]); assert r.returncode == 0, "verify failed"
    d1 = digest(tdir)
    tmp = os.path.join(os.path.dirname(C.TASK), ".rebuild_task171")
    out = subprocess.run([sys.executable, __file__, "--out", tmp], capture_output=True, text=True).stdout.strip().splitlines()[-1]
    shutil.rmtree(tmp, ignore_errors=True)
    assert out == d1, "rebuild not byte-identical"
    print("byte-identical rebuild", d1[:16])
    make_zip(tdir, os.path.join(C.TASK, "target.zip"))
    print("target.zip", hashlib.md5(open(os.path.join(C.TASK, "target.zip"), "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
