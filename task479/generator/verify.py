"""The independent verifier: every graded figure recomputed from the cut pack alone (target/), without the generator's
world, and compared with generator/figures.json. It also carries the loaders ceiling.py and checks.py use on the cut
pack.

    python3 task479/generator/verify.py [target]
"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
YEAR = 365 * 1440
BASE = dt.datetime(2026, 1, 1)
SCF_PER_NM3_68F = 35.3146667 * 293.15 / 273.15


def name(target, prefix):
    hits = [f for f in os.listdir(target) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(target, hits[0])


def est_minute_from_local(s, fmt):
    d = dt.datetime.strptime(s, fmt)
    m = int((d - BASE).total_seconds() // 60)
    if dt.datetime(2026, 3, 8, 3) <= d < dt.datetime(2026, 11, 1, 1):
        m -= 60
    return m


def est_minute_from_utc(s):
    d = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    return int((d - dt.timedelta(hours=5) - BASE).total_seconds() // 60)


def local_boundary(y, mo):
    d = dt.datetime(y, mo, 1)
    m = int((d - BASE).total_seconds() // 60)
    return m - 60 if dt.datetime(2026, 3, 8, 3) <= d < dt.datetime(2026, 11, 1, 1) else m


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(p.extract_text() for p in PdfReader(path).pages)


def load_basis(target):
    import openpyxl
    wb = openpyxl.load_workbook(name(target, "vent_calculation_basis"), data_only=True)
    reactor, dryer, other = {}, {}, {}
    for r in wb["Reactor steps"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            reactor[(r[0], int(r[1]))] = (float(r[4]), float(r[5]))
    for r in wb["PX line (licensor)"].iter_rows(min_row=3, values_only=True):
        if r[0]:
            reactor[(r[0], int(r[1]))] = (float(r[4]) * SCF_PER_NM3_68F / 60.0, float(r[5]) * 2.20462262)
    for r in wb["Dryer steps"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            dryer[(r[0], int(r[1]))] = (float(r[4]), float(r[5]))
    for r in wb["Other vents"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            other[(r[0], r[1] if r[1] not in (None, "") else None)] = (float(r[4]), float(r[5]))
    return reactor, dryer, other


def fan_max(target):
    import openpyxl
    wb = openpyxl.load_workbook(name(target, "cvs1_closed_vent_system_register"), data_only=True)
    for r in wb.active.iter_rows(min_row=5, values_only=True):
        if r[0] == "RTO-1":
            return float(re.search(r"([\d,]+) scfm", r[4]).group(1).replace(",", ""))
    raise AssertionError("no RTO-1 row")


def rate(unit, product, stepno, step, basis):
    reactor, dryer, other = basis
    if unit.startswith("SR"):
        return other[("SR-301", 1 if step in ("FEED/REFLUX", "OP-310") else 2)]
    if unit.startswith("D"):
        return dryer[(product, stepno)]
    if step in ("HOLD", "OP-099"):
        return other[("Reactor, any product", None)]
    if product in ("CIP", "CLEAN-SOLV"):
        return other[("Reactor, campaign change", 1)]
    return reactor[(product, stepno)]


def load_steps(target, basis):
    """Every executed step once: Orbitas whole (its migrated history included), Batchwise for the steps Orbitas does
    not hold. (unit, start, end, flow scfm, VOC lb/hr) on EST minutes."""
    import pyarrow.parquet as pq
    t = pq.read_table(name(target, "orbitas_process_operations")).to_pydict()
    steps, seen = [], set()
    for i in range(len(t["process_order"])):
        unit = t["equipment_id"][i].replace("PFC-", "")
        op = int(t["operation"][i])
        stepno = op // 10 if op >= 10 else None
        a, b = est_minute_from_utc(t["start_utc"][i]), est_minute_from_utc(t["end_utc"][i])
        f, v = rate(unit, t["material"][i], stepno, t["op_code"][i], basis)
        steps.append((unit, a, b, f, v, "orb"))
        seen.add((unit, a))
    with open(name(target, "batchwise4_batch_steps"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            unit = re.sub(r"^([A-Z]+)(\d+)$", r"\1-\2", r["Unit"])
            a = est_minute_from_local(r["Start"], "%m/%d/%Y %H:%M")
            if (unit, a) in seen:
                continue
            assert r["End"], ("open step not in Orbitas", r)
            b = est_minute_from_local(r["End"], "%m/%d/%Y %H:%M")
            stepno = int(r["Step No"]) if r["Step No"] else None
            prod = {"SOLV RECOVERY": "SR"}.get(r["Product"], r["Product"])
            f, v = rate(unit, prod, stepno, r["Step"], basis)
            steps.append((unit, a, b, f, v, "bw"))
    return steps


def arrays(steps):
    flow, voc = np.zeros(YEAR), np.zeros(YEAR)
    for unit, a, b, f, v, src in steps:
        a, b = max(0, a), min(YEAR, b)
        if a < b:
            flow[a:b] += f
            voc[a:b] += v / 60.0
    return flow, voc


def load_mode(target):
    run = np.zeros(YEAR, bool)
    with open(name(target, "rto1_dahs_1min"), encoding="utf-8") as fh:
        for _ in range(5):
            fh.readline()
        rd = csv.reader(fh)
        next(rd)
        for i, r in enumerate(rd):
            assert r[0] == (BASE + dt.timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            run[i] = r[3] == "RUN"
    return run


def quarters_lb(e):
    edges = [local_boundary(2026, 1), local_boundary(2026, 4), local_boundary(2026, 7), local_boundary(2026, 10), YEAR]
    return [float(e[edges[q]:edges[q + 1]].sum()) for q in range(4)]


def emitted(flow, voc, run, fan, dre, capacity=True, bin_min=1):
    f = flow
    if bin_min > 1:
        m = len(flow) // bin_min
        f = np.concatenate([np.repeat(flow[:m * bin_min].reshape(m, bin_min).mean(1), bin_min), flow[m * bin_min:]])
    cap = np.where(f > fan, fan / np.maximum(f, 1e-9), 1.0) if capacity else np.ones(len(flow))
    return np.where(run, voc * ((1 - cap) + cap * (1 - dre)), voc)


SOLVENT_TEXT = [("METHANOL", "Methanol"), ("TOLUENE", "Toluene"), ("ISOPROPYL", "Isopropanol"),
                ("ETHYL ACETATE", "Ethyl acetate"), ("HEPTANE", "n-Heptane"), ("ISOHEXANE", "Isohexane"),
                ("TETRAHYDROFURAN", "Tetrahydrofuran")]


def load_purchasing(target):
    import openpyxl
    with open(name(target, "wms_receipts"), newline="", encoding="utf-8") as fh:
        wms = list(csv.DictReader(fh))
    with open(name(target, "erp_material_master"), newline="", encoding="utf-8") as fh:
        mm = {r["Material"]: r for r in csv.DictReader(fh)}
    wb = openpyxl.load_workbook(name(target, "ap_invoice_lines"), data_only=True)
    ws = wb.active
    hdr = [c.value for c in ws[1]]
    ap = [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=2, values_only=True)]
    return wms, mm, ap


def solvent_of(text):
    for key, nm in SOLVENT_TEXT:
        if key in text.upper():
            return nm
    return None


DENSITY = {"Methanol": "SOL-01", "Toluene": "SOL-03", "n-Heptane": "SOL-12"}


def deliveries(target):
    """Each delivery once (its bill of lading), its solvent from the supplier's invoice line, its date the
    supplier's delivery date, its quantity from the warehouse receipts (all receipt lines of the BOL)."""
    wms, mm, ap = load_purchasing(target)
    inv = {}
    for r in ap:
        if r["Doc Type"] == "INV" and solvent_of(r["Item Text"] or ""):
            assert r["Delivery Ticket"] not in inv, r["Delivery Ticket"]
            inv[r["Delivery Ticket"]] = r
    qty = {}
    for r in wms:
        q, u = qty.get(r["BOL No"], (0.0, r["UoM"]))
        assert u == r["UoM"]
        qty[r["BOL No"]] = (q + float(r["Qty"]), u)
    out = []
    for bol, r in inv.items():
        s = solvent_of(r["Item Text"])
        day = dt.date.fromisoformat(r["Delivery Date"])
        if bol in qty:
            q, u = qty[bol]
            assert abs(q - float(r["Qty"])) < 0.05 and u == r["UoM"], (bol, q, r["Qty"])
        else:
            q, u = float(r["Qty"]), r["UoM"]
        lb = q * float(mm[DENSITY[s]]["Density (lb/gal @60F)"]) if u == "GAL" else q * 2.20462262
        out.append((day, s, lb, bol))
    return out


def golden_figures(target):
    basis = load_basis(target)
    fan = fan_max(target)
    permit = pdf_text(name(target, "PTO-2219-0447"))
    limit = float(re.search(r"shall not exceed ([\d.]+) tons in any calendar year", permit).group(1))
    test = pdf_text(name(target, "BST-25-0418"))
    dre = float(re.search(r"demonstrated is\s+([\d.]+) per cent", test).group(1)) / 100.0
    steps = load_steps(target, basis)
    flow, voc = arrays(steps)
    run = load_mode(target)
    e = emitted(flow, voc, run, fan, dre)
    q = [x / 2000 for x in quarters_lb(e)]
    d = deliveries(target)
    d26 = [x for x in d if x[0].year == 2026]
    by_s = {}
    for day, s, lb, bol in d26:
        by_s[s] = by_s.get(s, 0.0) + lb
    by_q = [sum(lb for day, s, lb, bol in d26 if (day.month - 1) // 3 == k) for k in range(4)]
    return dict(limit=limit, dre=dre, fan=fan, quarters=q, total=sum(q), flow=flow, voc=voc, run=run,
                ask_a=by_q, ask_b=by_s, steps=steps)


def main(target=None, fig_path=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(fig_path or os.path.join(HERE, "figures.json")))
    g = golden_figures(target)
    rows = []

    def row(label, got, want):
        rows.append((label, got == want, got, want))

    r1 = lambda x: "%.1f" % round(x + 1e-12, 1)
    r100 = lambda x: "{:,}".format(int(round(x / 100.0)) * 100)
    row("limit", r1(g["limit"]), fig["call"]["limit_tons"])
    row("destruction", "%.1f" % (100 * g["dre"]), fig["call"]["dre_pct"])
    row("fan", "{:,}".format(int(g["fan"])), fig["call"]["fan_scfm"])
    row("total tons", r1(g["total"]), fig["call"]["total_tons"])
    row("verdict", "over" if g["total"] > g["limit"] else "within", fig["call"]["verdict"])
    row("margin tons", r1(g["total"] - g["limit"]), fig["call"]["margin_tons"])
    ytd = np.cumsum(g["quarters"])
    for k in range(4):
        row("Q%d tons" % (k + 1), r1(g["quarters"][k]), fig["quarters"]["Q%d" % (k + 1)]["tons"])
        row("Q%d year to date" % (k + 1), r1(ytd[k]), fig["quarters"]["Q%d" % (k + 1)]["ytd_tons"])
    run, flow, voc = g["run"], g["flow"], g["voc"]
    cap = np.where(flow > g["fan"], g["fan"] / np.maximum(flow, 1e-9), 1.0)
    row("PSV-31 lb", "{:,}".format(int(round(float(np.where(run, voc * (1 - cap), 0).sum()) / 100.0)) * 100),
        fig["capture"]["psv31_lb"])
    row("default path tons", r1(float(emitted(flow, voc, run, g["fan"], g["dre"], capacity=False).sum()) / 2000),
        fig["default_path"]["tons"])
    row("hourly check tons", r1(float(emitted(flow, voc, run, g["fan"], g["dre"], bin_min=60).sum()) / 2000),
        fig["hourly_check"]["tons"])
    for k in range(4):
        row("ask A Q%d lb" % (k + 1), r100(g["ask_a"][k]), fig["ask_a"]["Q%d" % (k + 1)])
    for s, v in fig["ask_b"].items():
        row("ask B %s lb" % s, r100(g["ask_b"].get(s, 0.0)), v)
    bad = [r for r in rows if not r[1]]
    for label, ok, got, want in rows:
        if not ok:
            print("VERIFY FAIL %-22s got %s want %s" % (label, got, want))
    print("verify: %d of %d figures recomputed from target/ alone" % (len(rows) - len(bad), len(rows)))
    return not bad


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
