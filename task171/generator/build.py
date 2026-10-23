"""Build task171: target/ (the evidence pack), golden/ (the deliverable), metadata.json, generator/figures.json, then
the checks and the independent verifier, then a second build compared byte for byte, then target.zip.

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

MTIME = 1795_000_000  # placeholder, replaced below
ZIP_STAMP = (2026, 11, 20, 7, 42, 0)


def write_pack(out):
    import numpy as np
    import pandas as pd
    import world, pack, docs
    W = world.build()
    P = pack.build_pack(W, out)
    rng = np.random.default_rng(C.SEED + 2)
    crm = docs.crm_requests(P, rng)
    docs.write_xlsx(os.path.join(out, C.F_CRM), [("requests", crm)])
    docs.write_pdf(os.path.join(out, C.F_SCHED), docs.sched_text())
    docs.write_docx(os.path.join(out, C.F_PLAN), docs.PLAN)
    docs.billing_summary(W, P).to_csv(os.path.join(out, C.F_BILL), index=False, lineterminator="\n")
    docs.ev_rebates(W, P, rng).to_csv(os.path.join(out, C.F_EV), index=False, lineterminator="\n")
    docs.degree_days(rng).to_csv(os.path.join(out, C.F_HDD), index=False, lineterminator="\n")
    dict_rows = [(f, c, d) for f, cols in docs.DICT.items() for c, d in cols]
    docs.write_xlsx(os.path.join(out, C.F_DICT), [("fields", pd.DataFrame(dict_rows, columns=["file", "field", "definition"]))],
                    author="Sablewood IT data services")
    man = [
        (C.F_AMI, "Meter data management system", "2026-11-19", "Billing months March 2023 to October 2026, every residential meter read", "Load-research extract, one row per meter, service account and read period"),
        (C.F_SVC, "Customer information system", "2026-11-19", "Every residential service open at any time since March 2023", "Service accounts as at October 31, 2026"),
        (C.F_RATE, "Customer information system", "2026-11-19", "Rate assignments of the same services", "R-TOU rows are written by the TOU enrolment module"),
        (C.F_EXCH, "Work management system", "2026-11-18", "Meter exchanges at residential locations, 2023 to 2026", ""),
        (C.F_CRM, "Member services CRM", "2026-11-18", "Residential rate-change cases from March 1, 2024", "Times in UTC"),
        (C.F_BILL, "Billing system MIS", "2026-11-12", "Billing months November 2025 to October 2026", "Residential class, base schedules"),
        (C.F_EV, "Energy services rebate register", "2026-11-10", "EV charger rebates paid 2021 to 2026", ""),
        (C.F_HDD, "SCADA weather feed", "2026-11-01", "Daily, January 2023 to October 2026", ""),
        (C.F_SCHED, "Tariff book", "2026-11-06", "Residential schedules, revision 14", ""),
        (C.F_PLAN, "Rates Committee papers", "2026-11-13", "Paper RC-26-19", "Draft"),
        (C.F_DICT, "IT data services", "2026-11-19", "Field definitions for the extracts", ""),
    ]
    pd.DataFrame(man, columns=["file", "source_system", "extracted", "covers", "notes"]).to_csv(os.path.join(out, C.F_MAN), index=False, lineterminator="\n")
    return W, P


def solve_all(tdir):
    import solve
    F = solve.frames(tdir)
    g, P12 = solve.golden(F)
    A = solve.ask_A(F)
    B = solve.ask_B(tdir, F)
    return F, g, A, B


def figures(g, A, B):
    fig = {"call_members_2027": int(round(g["members"] / 250) * 250),
           "call_shortfall_2027_usd": int(round(g["shortfall"] / 25000) * 25000),
           "members_unrounded": round(g["members"], 1), "shortfall_unrounded": round(g["shortfall"], 0),
           "cohort_2024": g["cohort"], "takers_first_year_2024": g["takers12"], "population_2026": g["pop"]}
    for d in C.DISTRICTS:
        k = C.DCODE[d]
        fig["a_%s_twelve_months" % k] = A[d]["twelve"]
        fig["a_%s_kwh_4to9pm" % k] = A[d]["kwh"]
        fig["a_%s_kwh_11pmto6am" % k] = A[d]["night"]
        fig["b_%s_requests" % k] = B[d]["requests"]
        fig["b_%s_web" % k] = B[d]["web"]
    return fig


def write_golden(fig, gdir):
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    import docs
    os.makedirs(gdir, exist_ok=True)
    bold = Font(bold=True); head = PatternFill("solid", fgColor="DCE6F0"); thin = Border(bottom=Side(style="thin", color="7F7F7F"))
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "R-ON 2027"
    ws["A1"] = "R-ON in its first year: %s services moved by December 31, 2027, $%s a year given up" % ("{:,}".format(fig["call_members_2027"]), "{:,}".format(fig["call_shortfall_2027_usd"]))
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Rates Committee, December 3, 2026. Forecast for the 2027 budget, basis as in paper RC-26-19."
    ws["A2"].font = Font(italic=True, color="595959")
    ws.append([])
    ws.append(["Measure", "Forecast", "Rounded to"])
    for c in ws[4]:
        c.font = bold; c.fill = head; c.border = thin
    ws.append(["R-1 services with R-ON in effect on December 31, 2027", fig["call_members_2027"], "nearest 250 services"])
    ws.append(["Revenue given up a year: R-1 bill less R-ON bill, 2027 schedules, test-year use", fig["call_shortfall_2027_usd"], "nearest $25,000"])
    ws["B5"].number_format = "#,##0"; ws["B6"].number_format = "$#,##0"
    ws.append([])
    ws.append(["Take-up is each service's chance of moving in 2027, from the R-TOU launch year (March 2024 to February 2025) read on each service's saving over its twelve billing months before the March 2024 offer."])
    ws.column_dimensions["A"].width = 78; ws.column_dimensions["B"].width = 14; ws.column_dimensions["C"].width = 22
    ws2 = wb.create_sheet("R-TOU book Oct 2026")
    ws2.append(["District", "On R-TOU without a break since Nov 1, 2025 or earlier", "kWh 4 p.m. to 9 p.m.", "kWh 11 p.m. to 6 a.m."])
    for c in ws2[1]:
        c.font = bold; c.fill = head; c.border = thin; c.alignment = Alignment(wrap_text=True, vertical="top")
    for d in C.DISTRICTS:
        k = C.DCODE[d]
        ws2.append([d, fig["a_%s_twelve_months" % k], fig["a_%s_kwh_4to9pm" % k], fig["a_%s_kwh_11pmto6am" % k]])
    n = len(C.DISTRICTS)
    ws2.append(["All districts", "=SUM(B2:B%d)" % (n + 1), "=SUM(C2:C%d)" % (n + 1), "=SUM(D2:D%d)" % (n + 1)])
    for c in ws2[n + 2]:
        c.font = bold
    for row in ws2.iter_rows(min_row=2, min_col=2, max_col=4):
        for c in row:
            c.number_format = "#,##0"
    ws2.append([])
    ws2.append(["kWh: every service on R-TOU at October 31, 2026, billing months November 2025 to October 2026, the re-collected read where the MDM holds an estimate and a re-collection."])
    ws2.column_dimensions["A"].width = 16
    for col in "BCD":
        ws2.column_dimensions[col].width = 22
    ws2.row_dimensions[1].height = 45; ws2.freeze_panes = "B2"
    ws3 = wb.create_sheet("R-TOU requests 2024")
    ws3.append(["District", "Enrolment requests received Mar 1 to May 31, 2024", "Of which by the web form"])
    for c in ws3[1]:
        c.font = bold; c.fill = head; c.border = thin; c.alignment = Alignment(wrap_text=True, vertical="top")
    for d in C.DISTRICTS:
        k = C.DCODE[d]
        ws3.append([d, fig["b_%s_requests" % k], fig["b_%s_web" % k]])
    ws3.append(["All districts", "=SUM(B2:B%d)" % (n + 1), "=SUM(C2:C%d)" % (n + 1)])
    for c in ws3[n + 2]:
        c.font = bold
    ws3.append([])
    ws3.append(["Central time; a duplicate web submission counted once; a request counted where the service it put on R-TOU is."])
    ws3.column_dimensions["A"].width = 16; ws3.column_dimensions["B"].width = 26; ws3.column_dimensions["C"].width = 18
    ws3.row_dimensions[1].height = 45; ws3.freeze_panes = "B2"
    ws4 = wb.create_sheet("Notes")
    for line in ["Population: R-1 services on the books at October 31, 2026 billed in all twelve billing months November 2025 to October 2026, none closing or opening in 2027.",
                 "Moved: R-ON in effect for the service on the date (tariff general terms 1 and 2).",
                 "Revenue: full twelve test-year months whatever month of 2027 a service moves; riders PCA-1 and TX-2 apply alike on every schedule and are left out.",
                 "Sources: MDM load-research extract to billing month October 2026; CIS service accounts and rate assignments at October 31, 2026; member services CRM; tariff book section 3, revision 14."]:
        ws4.append([line])
    ws4.column_dimensions["A"].width = 120
    wb.properties.creator = "Rate Products"; wb.properties.lastModifiedBy = "Rate Products"
    wb.properties.created = docs.FIXED; wb.properties.modified = docs.FIXED
    p = os.path.join(gdir, "r-on_2027_forecast.xlsx")
    wb.save(p); docs._normalise_zip(p)


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
        print(json.dumps({k: fig[k] for k in list(fig)[:7]})); return
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
