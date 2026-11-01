"""Independent verifier for task133 architecture 4: reads every shipped format with its own code (pandas, python-docx,
openpyxl, pdftotext), takes the limits and grade lengths from the shipped documents, recomputes the call and both asks
and compares them with generator/figures.json and the goldens.

    python3 task133/generator/verify.py          # exit 1 on any mismatch
"""
import json
import os
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd
from docx import Document
from openpyxl import load_workbook

GEN = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(GEN)
T = os.path.join(TASK, "target")
FAILS = []


def ok(label, cond, detail=""):
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    if not cond:
        FAILS.append(label)


def near(x, step):
    return float(Decimal(repr(float(x) / step)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) * step


def pdftext(name):
    return subprocess.run(["pdftotext", "-layout", os.path.join(T, name), "-"], capture_output=True, text=True).stdout


def main():
    figs = json.load(open(os.path.join(GEN, "figures.json")))
    basis = "\n".join(p.text for p in Document(os.path.join(T, "cartage_planning_basis_FY2028.docx")).paragraphs)
    for phrase in ("weighed on the port weighbridge", "1 July 2027 to 30 June 2028", "fleet register at 30 June 2026",
                   "would carry on the same units in FY2028", "run at 50 tonnes gross", "whose unit hauled the load",
                   "by delivery date"):
        ok("positive control: the planning basis files %r" % phrase, phrase in basis)
    appr = pdftext("50MAX_route_approval_RDC-2026-114.pdf")
    new_gross = float(re.search(r"up\s+to\s+(\d+)\s+tonnes gross", appr.replace("\n", " ")).group(1))
    old_gross = float(re.search(r"limit of (\d+) tonnes gross", appr.replace("\n", " ")).group(1))
    ok("limits read from the approval PDF", (new_gross, old_gross) == (50.0, 44.0), (new_gross, old_gross))
    spec = pdftext("export_log_grade_specifications_2025.pdf")
    length = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s*(A|P|K|KI|KIS)\s+\S.*?\s(\d+\.\d)\s", spec, re.M)}
    ok("grade lengths read from the specification PDF", len(length) == 5, length)
    wb = pd.read_csv(os.path.join(T, "weighbridge_tickets_port_kowhai_FY2026.csv"), dtype={"ticket_no": str})
    wb["t"] = pd.to_datetime(wb["weighed_at"], format="%d/%m/%Y %H:%M")
    sc = pd.read_csv(os.path.join(T, "log_scaling_port_kowhai_FY2026.csv"))
    sc["t"] = pd.to_datetime(sc["scaled_at"])
    m = pd.merge_asof(wb.sort_values("t"), sc.sort_values("t")[["t", "truck_rego", "jas_m3"]], on="t",
                      left_by="vehicle_rego", right_by="truck_rego", direction="forward", tolerance=pd.Timedelta("60min"))
    ok("every port ticket links to a scaling record", m["jas_m3"].notna().all())
    fl = pd.read_excel(os.path.join(T, "fleet_register_2026-06-30.xlsx"), header=2)
    reg = {}
    for _, u in fl.iterrows():
        reg[u["Registration"]] = u
        if isinstance(u["Previous registration"], str):
            reg[u["Previous registration"]] = u
    cls = {12.1: "Full bunks 12.1 m logs (JAS m3)", 5.9: "Full bunks 5.9 m logs (JAS m3)", 3.9: "Full bunks 3.9 m logs (JAS m3)"}
    pay = []
    for _, r in m.iterrows():
        u = reg[r["vehicle_rego"]]
        g = (new_gross if u["50MAX permit"] == "Y" else old_gross) - u["Tare (t)"]
        pay.append(min(g, u[cls[length[r["product_code"]]]] * r["net_tonnes"] / r["jas_m3"]))
    m["pay"] = pay
    plan = pd.read_excel(os.path.join(T, "harvest_plan_FY2028.xlsx"), sheet_name="Export", header=3)
    names = {"A grade": "A", "Pruned": "P", "K grade": "K", "KI grade": "KI", "KIS grade": "KIS"}
    plan_t = {names[c]: plan[c].sum() for c in names}
    loads = {g: plan_t[g] / m.loc[m["product_code"] == g, "pay"].mean() for g in plan_t}
    tot = sum(loads.values())
    ok("the call: FY2028 loads, nearest 100", near(tot, 100) == figs["call"]["fy2028_loads_nearest_100"], round(tot, 1))
    inv_names = {v: k for k, v in names.items()}
    for g, v in loads.items():
        ok("grade %s loads, nearest 50" % g, near(v, 50) == figs["loads_by_grade_nearest_50"][inv_names[g]], round(v, 1))
    ok("FY2026 loads and tonnes", len(wb) == figs["components"]["fy2026_loads"] and
       round(wb["net_tonnes"].sum()) == figs["components"]["fy2026_tonnes"])
    inv = pd.read_csv(os.path.join(T, "cartage_invoices_FY2026.csv"), dtype={"ticket_ref": str})
    rego = dict(zip(wb["ticket_no"], wb["vehicle_rego"]))
    inv["carrier"] = [reg[rego[t]]["Carrier"] for t in inv["ticket_ref"]]
    cart = inv.groupby("carrier")["amount_nzd"].sum()
    for c, v in figs["ask_a_cartage_nzd_k"].items():
        ok("cartage %s" % c, near(cart[c] / 1e3, 1) == v, round(cart[c] / 1e3, 3))
    mw = pd.read_csv(os.path.join(T, "mill_weighbridge_logs_FY2026.csv"))
    mw = mw[mw["supplier_docket"].str.startswith("MFP")].copy()
    mw["t"] = pd.to_datetime(mw["weigh_in"])
    mw["q"] = "Q" + (((mw["t"].dt.month - 7) % 12) // 3 + 1).astype(str)
    mw["net"] = mw["gross_t"] - mw["tare_t"]
    mills = {"MSM": "Mohaka Sawmills", "AHT": "Ahuriri Timber Processors", "HBL": "Heretaunga Box and Lumber"}
    agg = mw.groupby(["mill_code", "q"])["net"].sum()
    for k, v in figs["ask_b_mill_tonnes"].items():
        mill, q = k.rsplit(" ", 1)
        code = {n: c for c, n in mills.items()}[mill]
        ok("mill %s" % k, near(agg[(code, q)], 10) == v, round(agg[(code, q)], 2))
    g = load_workbook(os.path.join(TASK, "golden", "matiri_fy2028_log_cartage_loads.xlsx"), data_only=True)
    ok("golden workbook headline", g["FY2028 loads"]["F4"].value == figs["call"]["fy2028_loads_nearest_100"])
    ok("golden chart exists", os.path.getsize(os.path.join(TASK, "golden", "fy2028_loads_by_grade.svg")) > 10000)
    ok("no em or en dash in the write-up", not re.search("[–—]", open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()))
    print("\n%d checks failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
