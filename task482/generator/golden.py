"""task482 architecture 16: the golden solution, read from the pack alone.

SCR-2 on Brackwell's 2026: the site meter's 15-minute volumes at each invoice period's calorific value give the gas
burned; a regression of each local day's gas on what each process did that day (tonnes melted in the casthouse,
tonnes charged to the tower melter, hours the homogenizing furnace and the solution oven fired, heating degree days)
reads the gas each process burns; each family carries its processes' gas (melting by its tonnes melted, the
homogenizing furnace by the hours its loads fired), the rest is shared by tonnes produced, and the premium is paid on
the 2027 call-offs of the families at or under the limit. The asks read the weighbridge and the goods-in register.

    python3 task482/generator/golden.py [target folder]
"""
import csv
import datetime as dt
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
LON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
YEAR = 2026
DAYS = [dt.date(YEAR, 1, 1) + dt.timedelta(days=i) for i in range(365)]
DAY_INDEX = {d: i for i, d in enumerate(DAYS)}
FAMILIES = ["BIL6063", "BIL6082", "INGLM25", "CSTLM25"]
PRODUCT = {"6063 extrusion billet": "BIL6063", "6082 extrusion billet": "BIL6082", "LM25 foundry ingot": "INGLM25",
           "LM25-TF sand castings": "CSTLM25"}
ALLOY = {"6063": "BIL6063", "6082": "BIL6082", "LM25": "INGLM25"}
GRADES = ["CST", "EXT", "TRN", "UBC"]
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
CO2 = 0.18296          # SCR-2 section 4, kg per kWh
LIMIT = 0.235          # SCR-2 section 7
PREMIUM = 38           # SCR-2 section 7, EUR a tonne
F = dict(meter="brackwell_site_gas_meter_2026.csv", invoices="brackwell_gas_invoices_2026.pdf",
         furnaces="brackwell_melting_furnace_logs_2026.xlsx", h1="brackwell_homogenizing_furnace_h1_2026.csv",
         t1="brackwell_heat_treatment_oven_t1_2026.csv", lots="brackwell_production_lots_2026.csv",
         calloff="velden_2027_calloff_schedule.xlsx", weather="brackwell_works_weather_2026.csv",
         weighbridge="brackwell_weighbridge_2026.csv", goodsin="brackwell_scrap_goods_in_2026.csv")


def to_utc(naive):
    return naive.replace(tzinfo=LON).astimezone(UTC)


def local_date(t_utc):
    return t_utc.astimezone(LON).date()


def day_bounds():
    """Each local day of 2026 as a UTC window."""
    return [(to_utc(dt.datetime.combine(d, dt.time())), to_utc(dt.datetime.combine(d + dt.timedelta(days=1),
                                                                                   dt.time()))) for d in DAYS]


BOUNDS = day_bounds()


def split_days(a, b):
    """[(day index, hours)] of the UTC span [a, b) over the local days."""
    out = []
    if b <= a:
        return out
    i = DAY_INDEX.get(local_date(a))
    while i is not None and i < len(DAYS):
        lo, hi = BOUNDS[i]
        if lo >= b:
            break
        h = (min(b, hi) - max(a, lo)).total_seconds() / 3600.0
        if h > 0:
            out.append((i, h))
        i += 1
    return out


def quarter(d):
    return "Q%d" % ((d.month - 1) // 3 + 1)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------ reading the pack
def read_invoices(path):
    pdf = pdfplumber.open(path)
    out = []
    for page in pdf.pages:
        text = page.extract_text() or ""
        stamps = re.findall(r"(\d\d/\d\d/\d{4}) (\d\d:\d\d)", text)
        cv = float(re.search(r"Calorific value \(MJ/m3\)\s+([\d.]+)", text).group(1))
        vcf = float(re.search(r"Volume correction factor\s+([\d.]+)", text).group(1))
        a = dt.datetime.strptime(" ".join(stamps[0]), "%d/%m/%Y %H:%M")
        b = dt.datetime.strptime(" ".join(stamps[-1]), "%d/%m/%Y %H:%M")
        out.append(dict(a=to_utc(a), b=to_utc(b), cv=cv, vcf=vcf))
        conv = re.search(r"converted at ([\d.]+) cubic metres", text)
        if conv:
            out[-1]["hcf"] = float(conv.group(1))
    out.sort(key=lambda p: p["a"])
    return out


def read_meter(path, per):
    hcf = [p["hcf"] for p in per if "hcf" in p][0]
    starts, kwh = [], []
    k = 0
    for r in rows(path):
        t = dt.datetime.strptime(r["Interval start (UTC)"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
        v = float(r["Consumption"])
        m3 = v * hcf if r["Unit"] == "hcf" else v
        while not (per[k]["a"] <= t < per[k]["b"]):
            k += 1
        starts.append(t)
        kwh.append(m3 * per[k]["vcf"] * per[k]["cv"] / 3.6)
    return starts, np.array(kwh)


def read_furnaces(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    heats, seen = [], set()
    for sheet in ("M1 casthouse", "M2 casthouse"):
        for r in list(wb[sheet].iter_rows(values_only=True))[1:]:
            if r[0] is None or (sheet, r[0]) in seen:
                continue
            seen.add((sheet, r[0]))
            heats.append(dict(furnace=sheet[:2], heat=r[0], family=ALLOY[str(r[1])], a=to_utc(r[2]), b=to_utc(r[3]),
                              t=float(r[4]), lot=r[5]))
    m3, seen = [], set()
    for r in list(wb["M3 tower melter"].iter_rows(values_only=True))[1:]:
        if r[0] is None or r[0] in seen:
            continue
        seen.add(r[0])
        m3.append(dict(charge=r[0], a=to_utc(r[1]), t=r[2] / 1000.0))
    return heats, m3


def read_h1(path):
    out = []
    for r in rows(path):
        out.append(dict(load=int(r["Load"]), family=ALLOY[r["Alloy"]],
                        a=to_utc(dt.datetime.strptime(r["Door closed"], "%d/%m/%Y %H:%M")),
                        b=to_utc(dt.datetime.strptime(r["Door opened"], "%d/%m/%Y %H:%M")), t=float(r["Billet t"])))
    return out


def read_t1(path):
    out = []
    for r in rows(path):
        out.append(dict(batch=int(r["Batch"]), a=to_utc(dt.datetime.strptime(r["Start"], "%Y-%m-%dT%H:%M")),
                        b=to_utc(dt.datetime.strptime(r["End"], "%Y-%m-%dT%H:%M")), t=int(r["Net kg"]) / 1000.0))
    return out


def read_lots(path):
    """SCR-2 section 5: a lot counts at its last result, and a family's production is what passed."""
    last = {}
    for r in rows(path):
        when = dt.datetime.strptime(r["Inspected"], "%d/%m/%Y %H:%M")
        if r["Lot"] not in last or when >= last[r["Lot"]][0]:
            last[r["Lot"]] = (when, r)
    prod = {f: 0.0 for f in FAMILIES}
    for when, r in last.values():
        if r["Result"] == "PASS" and when.year == YEAR:
            prod[PRODUCT[r["Product"]]] += int(r["Net kg"]) / 1000.0
    return prod


def read_weather(path):
    return {dt.date.fromisoformat(r["Date"]): float(r["Mean C"]) for r in rows(path)}


def read_calloffs(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = {f: 0 for f in FAMILIES}
    for r in list(wb["Call-offs 2027"].iter_rows(values_only=True))[1:]:
        if not r[0]:
            continue
        desc = r[1]
        fam = ("BIL6063" if "6063" in desc else "BIL6082" if "6082" in desc else
               "CSTLM25" if "casting" in desc.lower() else "INGLM25")
        months = sum(int(x) for x in r[3:15])
        assert months == int(r[15]), r
        out[fam] += months
    return out


def load(T=TARGET):
    p = lambda k: os.path.join(T, F[k])  # noqa: E731
    per = read_invoices(p("invoices"))
    starts, kwh = read_meter(p("meter"), per)
    heats, m3 = read_furnaces(p("furnaces"))
    return dict(per=per, starts=starts, kwh=kwh, heats=heats, m3=m3, h1=read_h1(p("h1")), t1=read_t1(p("t1")),
                prod=read_lots(p("lots")), weather=read_weather(p("weather")), calloff=read_calloffs(p("calloff")),
                T=T)


# ------------------------------------------------------------------------------------------------ the decomposition
def daily(d, hdd_base=15.5):
    y = np.zeros(365)
    for t, k in zip(d["starts"], d["kwh"]):
        y[DAY_INDEX[local_date(t)]] += k
    x = {k: np.zeros(365) for k in ("melt", "m3", "h1", "t1", "h1_t", "t1_t", "hdd")}
    for h in d["heats"]:
        span = (h["b"] - h["a"]).total_seconds() / 3600.0
        for i, hrs in split_days(h["a"], h["b"]):
            x["melt"][i] += h["t"] * hrs / span
    for c in d["m3"]:
        x["m3"][DAY_INDEX[local_date(c["a"])]] += c["t"]
    for ld in d["h1"]:
        span = (ld["b"] - ld["a"]).total_seconds() / 3600.0
        for i, hrs in split_days(ld["a"], ld["b"]):
            x["h1"][i] += hrs
            x["h1_t"][i] += ld["t"] * hrs / span
    for b in d["t1"]:
        span = (b["b"] - b["a"]).total_seconds() / 3600.0
        for i, hrs in split_days(b["a"], b["b"]):
            x["t1"][i] += hrs
            x["t1_t"][i] += b["t"] * hrs / span
    for day, m in d["weather"].items():
        x["hdd"][DAY_INDEX[day]] = max(0.0, hdd_base - m)
    return y, x


def fit(y, x, drivers=("melt", "m3", "h1", "t1"), hdd=True):
    cols = list(drivers) + (["hdd"] if hdd else [])
    A = np.column_stack([x[c] for c in cols] + [np.ones(len(y))])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    r2 = 1 - (resid ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return dict(zip(cols + ["const"], beta)), r2


def attribute(d, beta, h1="hours", melt="melted", h1_driver="h1", t1_driver="t1"):
    """Each family's process gas (kWh) from the fitted rates, the rest shared by tonnes produced."""
    gas = {f: 0.0 for f in FAMILIES}
    melted = {f: 0.0 for f in FAMILIES}
    for h in d["heats"]:
        melted[h["family"]] += h["t"]
    m3_t = sum(c["t"] for c in d["m3"])
    melted["CSTLM25"] = m3_t
    if melt == "melted":
        for f in ("BIL6063", "BIL6082", "INGLM25"):
            gas[f] += beta["melt"] * melted[f]
    else:      # the casthouse's melting gas spread by the tonnes each family produced
        tot = beta["melt"] * sum(melted[f] for f in ("BIL6063", "BIL6082", "INGLM25"))
        p = sum(d["prod"][f] for f in ("BIL6063", "BIL6082", "INGLM25"))
        for f in ("BIL6063", "BIL6082", "INGLM25"):
            gas[f] += tot * d["prod"][f] / p
    gas["CSTLM25"] += beta["m3"] * m3_t
    hours = {f: 0.0 for f in FAMILIES}
    tonnes = {f: 0.0 for f in FAMILIES}
    for ld in d["h1"]:
        hours[ld["family"]] += (ld["b"] - ld["a"]).total_seconds() / 3600.0
        tonnes[ld["family"]] += ld["t"]
    if h1_driver == "h1":
        h1_total = beta["h1"] * sum(hours.values())
    else:
        h1_total = beta["h1_t"] * sum(tonnes.values())
    basis = hours if h1 == "hours" else tonnes
    for f in ("BIL6063", "BIL6082"):
        gas[f] += h1_total * basis[f] / sum(basis.values())
    t1_hours = sum((b["b"] - b["a"]).total_seconds() / 3600.0 for b in d["t1"])
    t1_tonnes = sum(b["t"] for b in d["t1"])
    gas["CSTLM25"] += beta["t1"] * t1_hours if t1_driver == "t1" else beta["t1_t"] * t1_tonnes
    total = float(d["kwh"].sum())
    process = sum(gas.values())
    allp = sum(d["prod"].values())
    out = {}
    for f in FAMILIES:
        kwh = gas[f] + (total - process) * d["prod"][f] / allp
        out[f] = dict(kwh=kwh, co2=kwh * CO2 / 1000.0, intensity=kwh * CO2 / 1000.0 / d["prod"][f])
    return out, dict(total=total, process=process, base=total - process, gas=gas, hours=hours, tonnes=tonnes,
                     melted=melted)


def premium(fam, calloff):
    earning = [f for f in FAMILIES if fam[f]["intensity"] <= LIMIT]
    return PREMIUM * sum(calloff[f] for f in earning), earning


def mass_allocation(d):
    """The works' gas over the families by the tonnes each produced: every family at the works' average."""
    total = float(d["kwh"].sum())
    allp = sum(d["prod"].values())
    return {f: dict(kwh=total * d["prod"][f] / allp, co2=total * d["prod"][f] / allp * CO2 / 1000.0,
                    intensity=total * CO2 / 1000.0 / allp) for f in FAMILIES}


# ------------------------------------------------------------------------------------------------ the asks
def weighings(T):
    visits = {}
    for r in rows(os.path.join(T, F["weighbridge"])):
        t = dt.datetime.strptime(r["Weighed (UTC)"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        key = (int(r["Ticket"]), local_date(t))
        v = visits.setdefault(key, dict(w=[], movement=r["Movement"], haulier=r["Haulier"], last=t))
        v["w"].append((int(r["Weighing"]), int(r["Weight kg"])))
        v["last"] = max(v["last"], t)
    for v in visits.values():
        v["w"] = [kg for _, kg in sorted(v["w"])]
    return visits


def scrap(T, split="weighings", key="ticket_date"):
    """Ask A: tonnes of each grade bought in each quarter, as weighed at the works' weighbridge. A two-grade load is
    weighed in, between its tips and out; each grade's weight is the drop across its own tip, the tips matched to the
    goods-in lines by the weights declared on them."""
    visits = weighings(T)
    by_ticket = {}
    for (tk, day), v in visits.items():
        by_ticket.setdefault(tk, []).append((day, v))
    lines = {}
    for r in rows(os.path.join(T, F["goodsin"])):
        day = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        lines.setdefault((int(r["WB ticket"]), day), []).append(r)
    out = {g: {q: 0.0 for q in QUARTERS} for g in GRADES}
    for (tk, day), ls in lines.items():
        if key == "ticket_date":
            v = visits[(tk, day)]
        else:          # the ticket number alone: the first visit that carried it
            v = sorted(by_ticket[tk], key=lambda x: x[0])[0][1]
        w = v["w"]
        ok = [r for r in ls if r["Status"] == "Accepted" and r["Grade"] in GRADES]
        if not ok:
            continue
        if len(ls) == 1:
            nets = [w[0] - w[-1]]
        elif len(w) < 3:          # only on the wrong join: a two-line delivery matched to another visit
            dec = [int(r["Declared kg"]) for r in ls]
            nets = [(w[0] - w[-1]) * x / sum(dec) for x in dec]
        elif split == "weighings":
            drops = [w[0] - w[1], w[1] - w[2]]
            dec = [int(r["Declared kg"]) for r in ls]
            straight = abs(drops[0] - dec[0]) + abs(drops[1] - dec[1])
            crossed = abs(drops[1] - dec[0]) + abs(drops[0] - dec[1])
            nets = drops if straight <= crossed else [drops[1], drops[0]]
        elif split == "line_order":
            nets = [w[0] - w[1], w[1] - w[2]]
        else:          # the load's net shared by the declared weights
            dec = [int(r["Declared kg"]) for r in ls]
            nets = [(w[0] - w[-1]) * x / sum(dec) for x in dec]
        for r, net in zip(ls, nets):
            if r["Status"] == "Accepted" and r["Grade"] in GRADES:
                out[r["Grade"]][quarter(day)] += net / 1000.0
    return out


def declared(T):
    out = {g: {q: 0.0 for q in QUARTERS} for g in GRADES}
    for r in rows(os.path.join(T, F["goodsin"])):
        if r["Grade"] in GRADES:
            day = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
            out[r["Grade"]][quarter(day)] += int(r["Declared kg"]) / 1000.0
    return out


def dross(T, combined="weighings"):
    """Ask B: tonnes of dross sent off for recovery each quarter, as weighed: the skip's rise in weight, which on a
    visit that first unloads returned metal is measured from the weighing after the unloading."""
    out = {q: 0.0 for q in QUARTERS}
    for (tk, day), v in weighings(T).items():
        if v["movement"] != "Waste out":
            continue
        w = v["w"]
        net = (w[-1] - w[-2]) if combined == "weighings" else (w[-1] - w[0])
        out[quarter(local_date(v["last"]))] += net / 1000.0
    return out


# ------------------------------------------------------------------------------------------------ the golden
def solve(T=TARGET):
    d = load(T)
    y, x = daily(d)
    beta, r2 = fit(y, x)
    fam, parts = attribute(d, beta)
    prem, earning = premium(fam, d["calloff"])
    a = scrap(T)
    b = dross(T)
    return dict(d=d, y=y, x=x, beta=beta, r2=r2, fam=fam, parts=parts, premium=prem, earning=earning, ask_a=a,
                ask_b=b)


def figures(res):
    d, fam = res["d"], res["fam"]
    hours, tonnes = res["parts"]["hours"], res["parts"]["tonnes"]
    loads = {f: sum(1 for ld in d["h1"] if ld["family"] == f) for f in ("BIL6063", "BIL6082")}
    return {
        "constants": {"alloys": [6063, 6082], "co2_kg_per_kwh": CO2, "volume_correction": 1.02264,
                      "mj_per_kwh": 3.6, "hdd_base_c": 15.5, "hcf_to_m3": 2.83, "meter_exchange": "14 April 10:30",
                      "co2_rounding_t": 10, "ticket_restart": "29 June"},
        "h1": {"mean_cycle_h": {f: round(hours[f] / loads[f], 1) for f in loads},
               "hours_share_6082_pct": int(round(100 * hours["BIL6082"] / sum(hours.values()))),
               "tonnes_share_6082_pct": int(round(100 * tonnes["BIL6082"] / sum(tonnes.values())))},
        "earning_calloff_t": int(sum(d["calloff"][f] for f in res["earning"])),
        "call": {"premium_eur": int(res["premium"]), "earning": res["earning"],
                 "not_earning": [f for f in FAMILIES if f not in res["earning"]]},
        "intensity_2dp": {f: "%.2f" % fam[f]["intensity"] for f in FAMILIES},
        "intensity_3dp": {f: "%.3f" % fam[f]["intensity"] for f in FAMILIES},
        "produced_t": {f: int(round(d["prod"][f])) for f in FAMILIES},
        "calloff_t": {f: int(d["calloff"][f]) for f in FAMILIES},
        "co2_t": {f: int(round(fam[f]["co2"], -2)) for f in FAMILIES},
        "gas_mwh": int(round(res["parts"]["total"] / 1000.0, -2)),
        "rates": {k: round(v, 1) for k, v in res["beta"].items()},
        "ask_a": {g: {q: int(round(res["ask_a"][g][q])) for q in QUARTERS} for g in GRADES},
        "ask_b": {q: int(round(res["ask_b"][q])) for q in QUARTERS},
        "limit": LIMIT, "premium_eur_per_t": PREMIUM,
    }


if __name__ == "__main__":
    res = solve(sys.argv[1] if len(sys.argv) > 1 else TARGET)
    print("r2 %.4f" % res["r2"], {k: round(v, 1) for k, v in res["beta"].items()})
    for f in FAMILIES:
        print(f, "%.4f" % res["fam"][f]["intensity"], "produced %.0f" % res["d"]["prod"][f])
    print("premium", res["premium"], res["earning"])
    print("ask A", {g: {q: round(v, 2) for q, v in res["ask_a"][g].items()} for g in GRADES})
    print("ask B", {q: round(v, 2) for q, v in res["ask_b"].items()})
