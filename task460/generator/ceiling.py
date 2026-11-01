"""The ask sheet's cracker and mirror, run on the cut pack. Shares no code with the generator: it reads target.zip
with the standard library only and scores against generator/figures.json at the prompt's rounding.

The cracker lands the call (it holds the eight stores' avoided carbon dioxide and the hourly file), executes every
filed rule (the charter's measure and 4.2's three figures; the prompt's each bill's days in 2025 pro rata) and runs the
hygiene battery (supplemental-stumping 1.1c): the kilowatt-hours repeated on a bill's distribution, transmission and
tax lines taken once, Tennaford's declining blocks summed; Halvane's gas lines left out; the two systems that bill one
meter's consumption (the delivery utility and the retail supplier) matched cycle by cycle and one kept, the utility's
meter reading where its invoice reached accounts payable, the supplier's energy quantity where it did not, reconciled
to the meter by the ratio the two bear in every cycle both bill (the control); a bill that reached accounts payable and
was paid by the payment service as well (the same bill number on both) counted once. Nothing in the battery reads the
supplier's change of term in July, when it began billing the meter's kilowatt-hours, or the credit the utility carried
for the bill paid twice.

The mirror stops at the most attractive wrong rung on the call (R1, the published non-baseload rate, a reflex for what
a project avoids) and takes the same ask paths: the asks consume nothing the call's construction produces.

Weights 38 / 7 / 55; the ask weight over 37 criteria (the eight construction rates, the eight uses, shares and prices,
four chart criteria of which one is the monthly use bars, and the hourly file); the mirror's main block 5. Stress rows
(not the gate) are printed beside it: the fill as billed, the full includer who reads the term change, and the one who
also keeps every payment.

    python3 task460/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
Y0, Y1 = dt.date(2025, 1, 1), dt.date(2025, 12, 31)
N_ASK = 37
LB_PER_T = 2204.62262


def half_up(x, nd=0):
    q = 10 ** nd
    return int(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)


def frac(a, b):
    lo, hi = max(a, Y0), min(b, Y1)
    return max((hi - lo).days + 1, 0) / ((b - a).days + 1)


def load(target):
    inv = list(csv.DictReader(open(os.path.join(target, "corvane_electricity_invoice_lines_fy2025.csv"), encoding="utf-8")))
    for r in inv:
        r["a"] = dt.date.fromisoformat(r["service_period_start"])
        r["b"] = dt.date.fromisoformat(r["service_period_end"])
        r["q"] = float(r["quantity"]) if r["quantity"] else None
        r["usd"] = float(r["line_amount_usd"])
        v = r["vendor_name"]
        r["who"] = "supplier" if "Retail Energy" in v else ("service" if "Payment Services" in v else "utility")
        d = r["line_description"]
        r["gas"] = d.startswith("Gas ") or d.endswith("gas service")
    arr = {}
    for r in csv.DictReader(open(os.path.join(target, "pilot_array_output_model_2025.csv"), encoding="utf-8")):
        if r["hour_beginning_lst"].startswith("2025"):
            arr[int(r["store_number"])] = arr.get(int(r["store_number"]), 0.0) + float(r["ac_output_kw"]) / 1000.0
    return inv, arr


def meter_kwh(inv):
    """Per meter and cycle: the utility's own reading (distribution energy, blocks summed) and the supplier's bill."""
    own, sup = {}, {}
    for r in inv:
        k = (r["meter_number"], r["a"], r["b"])
        d = r["line_description"].lower()
        if r["who"] == "utility" and r["unit_of_measure"] == "KWH" and not any(
                w in d for w in ("transmission", "tax", "assessment", "receipts", "excise")):
            own[k] = own.get(k, 0.0) + r["q"]
        if r["who"] == "supplier":
            s = sup.setdefault(k, dict(energy=None, rps=False, store=int(r["store_number"])))
            if r["line_description"].startswith("Energy"):
                s["energy"] = r["q"]
            if r["line_description"].startswith("Renewable"):
                s["rps"] = True
    return own, sup


def use_by_store(inv, mode):
    """mode: recon (the cracker: the supplier's quantity over the meter's ratio wherever the utility's is missing),
    raw (the supplier's quantity as billed), term (the full includer: first-term bills over the ratio, second-term
    bills as billed)."""
    own, sup = meter_kwh(inv)
    ratio = {}
    for (m, a, b), s in sup.items():
        if (m, a, b) in own:
            n, d = ratio.get(m, (0.0, 0.0))
            ratio[m] = (n + s["energy"], d + own[(m, a, b)]) if (mode != "term" or s["rps"]) else (n, d)
    out = {}
    for (m, a, b), s in sup.items():
        f = ratio[m][0] / ratio[m][1]
        if (m, a, b) in own:
            q = own[(m, a, b)]
        elif mode == "recon":
            q = s["energy"] / f
        elif mode == "raw":
            q = s["energy"]
        else:
            q = s["energy"] / f if s["rps"] else s["energy"]
        out[s["store"]] = out.get(s["store"], 0.0) + q * frac(a, b) / 1000.0
    return out


def paid_by_store(inv, dedupe):
    direct = {r["invoice_number"] for r in inv if r["who"] == "utility"}
    out = {}
    for r in inv:
        if r["gas"]:
            continue
        if dedupe and r["who"] == "service" and r["line_description"].split(" bill ")[1].split()[0] in direct:
            continue
        st = int(r["store_number"])
        out[st] = out.get(st, 0.0) + r["usd"] * frac(r["a"], r["b"])
    return out


def score(F, arr, use, paid):
    kept = dict(use=0, share=0, price=0)
    rows = []
    if len(F.get("stores", {})) != 8 or any(g["store"] not in use or g["store"] not in paid for g in F["stores"].values()):
        raise SystemExit("ceiling.py: nothing to score (figures.json names %d stores; the pack yields use for %d) - no "
                         "verdict printed" % (len(F.get("stores", {})), len(use)))
    for town, g in F["stores"].items():
        st = g["store"]
        u, s, p = half_up(use[st]), half_up(100.0 * arr[st] / use[st], 1), half_up(paid[st] / use[st])
        kept["use"] += u == g["use"]
        kept["share"] += abs(s - g["share"]) < 1e-9
        kept["price"] += p == g["price"]
        rows.append((town, int(u), g["use"], s, g["share"], int(p), g["price"]))
    return kept, rows


def mirror_rates(target, F):
    """The mirror's eight figures: each area's published 2025 non-baseload output emission rate in t/MWh."""
    from xml.etree import ElementTree as ET
    path = os.path.join(target, "edc_generation_emission_rates_2025.xlsx")
    with zipfile.ZipFile(path) as z:
        ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        table = []
        for row in sheet.iter("{%s}row" % ns["m"]):
            vals = []
            for c in row.findall("m:c", ns):
                v = c.find("m:v", ns)
                is_ = c.find("m:is", ns)
                if c.get("t") == "s" and v is not None:
                    vals.append(shared[int(v.text)])
                elif c.get("t") == "inlineStr" and is_ is not None:
                    vals.append("".join(t.text or "" for t in is_.iter("{%s}t" % ns["m"])))
                else:
                    vals.append(v.text if v is not None else None)
            table.append(vals)
    head = next(r for r in table if r and r[0] == "BA code")
    col = head.index("CO2 non-baseload output emission rate (lb/MWh)")
    nb = {r[0]: float(r[col]) / LB_PER_T for r in table if r and r[0] in {g["area"] for g in F["stores"].values()}}
    return sum(1 for g in F["stores"].values() if half_up(nb[g["area"]], 2) == g["rate"])


def run(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    inv, arr = load(target)
    rows_out = {}

    def ask_keep(mode, dedupe):
        kept, rows = score(F, arr, use_by_store(inv, mode), paid_by_store(inv, dedupe))
        return kept, rows
    c_kept, c_rows = ask_keep("recon", True)
    chart_use_bars = 1 if c_kept["use"] == 8 else 0
    cracker_keep = 8 + 1 + 3 + chart_use_bars + c_kept["use"] + c_kept["share"] + c_kept["price"]
    mirror_rate_keep = mirror_rates(target, F)
    mirror_keep = mirror_rate_keep + 3 + chart_use_bars + c_kept["use"] + c_kept["share"] + c_kept["price"]
    lc, lm = cracker_keep / N_ASK, mirror_keep / N_ASK
    cracker, mirror = 38 + 7 + 55 * lc, 5 + 7 + 55 * lm
    stress = {}
    for lab, mode, dedupe in (("the fill as billed, the bill paid twice counted once", "raw", True),
                              ("the fill as billed, every payment kept", "raw", False),
                              ("the reconciled fill, every payment kept", "recon", False),
                              ("the full includer: the term change read, the bill paid twice counted once", "term", True),
                              ("the full includer who also keeps every payment", "term", False)):
        k, _ = ask_keep(mode, dedupe)
        stress[lab] = k
    fi = stress["the full includer: the term change read, the bill paid twice counted once"]
    fi_keep = 8 + 1 + 4 + fi["use"] + fi["share"] + fi["price"]
    fi_on, fi_off = 38 + 7 + 55 * fi_keep / N_ASK, 5 + 7 + 55 * (fi_keep - 9 + mirror_rate_keep) / N_ASK
    return dict(pack_sha256=hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:8]
                if os.path.exists(os.path.join(TASK, "target.zip")) else None,
                ask_criteria=N_ASK, cracker_asks_kept=c_kept, cracker_keep=cracker_keep, mirror_keep=mirror_keep,
                mirror_rates_kept=mirror_rate_keep, cracker=round(cracker, 1), mirror=round(mirror, 1),
                pair_ceiling=round((cracker + mirror) / 2, 1), mirror_leakage_pct=round(100 * lm, 1),
                cracker_rows=c_rows, stress_rows_kept_of_8=stress,
                full_includer_pair=round((fi_on + fi_off) / 2, 1),
                full_full_includer_pair=round((38 + 7 + 55 + 5 + 7 + 55 * (N_ASK - 9 + mirror_rate_keep) / N_ASK) / 2, 1))


def main():
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=1, default=str))
        return
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
            z.extractall(tmp)
        print(json.dumps(run(tmp), indent=1, default=str))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
