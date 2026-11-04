"""task489 independent verifier. Reads only the shipped bundle (target/) and the goldens (golden/), on its own code
path: no generator module is imported. Recomputes every level controller's 2026 dump cycles and methane, each pad's
intermittent-vent methane and the conversion set, each plunger well's cycles without an arrival, the continuous-bleed
methane by maker and area, and the ladder's wrong routes, then checks them against the goldens.

    python3 task489/generator/verify.py
"""
import csv
import datetime as dt
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

import openpyxl
import pdfplumber

TZ = ZoneInfo("America/Edmonton")
UTC = dt.timezone.utc
F = {"cycles": "plunger_cycles_2026.csv", "vol": "daily_well_volumes_2026.csv", "reg": "deep_basin_equipment_register.xlsx",
     "gas": "gas_analyses_2025_2026.csv", "ctr": "scada_dump_counters_2026.csv", "wo": "deep_basin_work_orders_2026.csv",
     "std": "MRS-03_methane_measurement_and_reporting_standard_rev4.pdf", "plan": "methane_reduction_plan_2027.docx",
     "survey": "sheldrake_pneumatic_survey_2026.pdf"}
SHEETS = ["corrigan_CL-200_CP-10_data_sheet.pdf", "aldous_SV-40_PC-60_data_sheet.pdf", "brannick_DLC-3_TC-5_data_sheet.pdf"]
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def pdf_text(path):
    with pdfplumber.open(path) as p:
        t = "\n".join(pg.extract_text() or "" for pg in p.pages)
    assert len(t) > 500, path
    return t


def local(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


WIN0 = dt.datetime(2026, 1, 1, 8, 0, 0)          # MRS-03 3.2: production days 1 January to 31 December, from 08:00
WIN1 = dt.datetime(2027, 1, 1, 8, 0, 0)


def prod_day(t):
    return (t - dt.timedelta(hours=8)).date()


def load(target):
    p = lambda k: os.path.join(target, F[k])
    std = re.sub(r"\s+", " ", pdf_text(p("std")))
    assert "Production days" in std or "production day" in std, "positive control: the standard's production day clause"
    scf = float(re.search(r"converted at ([0-9.]+) m3 per scf", std).group(1))
    rho = float(re.search(r"times ([0-9.]+) kg per m3", std).group(1))
    import docx
    plan = " ".join(x.text for x in docx.Document(p("plan")).paragraphs)
    line = float(re.search(r"vented more than ([0-9.]+) tonnes of methane in 2026", plan).group(1))
    per_cycle, bleed_rate = {}, {}
    for sh in SHEETS:
        t = re.sub(r"\s+", " ", pdf_text(os.path.join(target, sh)))
        lc = re.search(r"\b([A-Z]{2,3}-\d+) [^.]*?(?:level controller|dump valve package|level controller)\b", t)
        m_lc = re.findall(r"(CL-200|SV-40|DLC-3)", t)[0]
        m_bl = re.findall(r"(CP-10|PC-60|TC-5)", t)[0]
        per_cycle[m_lc] = float(re.search(r"(?:per dump cycle|per valve trip) ([0-9.]+) scf\b", t).group(1))
        bleed_rate[m_bl] = float(re.search(r"(?:steady state|relay bleed|Steady bleed nil at rest) ([0-9.]+) scf/h", t).group(1))
        assert lc is not None or m_lc
    wb = openpyxl.load_workbook(p("reg"), read_only=True)
    pads = {r[0]: {"lsd": r[1], "area": r[2]} for r in list(wb["Pads"].iter_rows(values_only=True))[1:]}
    wells = {r[1]: {"uwi": r[0], "pad": r[2], "lift": r[3]} for r in list(wb["Wells"].iter_rows(values_only=True))[1:]}
    vessels = []
    for r in list(wb["Vessels"].iter_rows(values_only=True))[1:]:
        vessels.append({"vessel": r[0], "pad": r[1], "bore": float(r[4]), "lc": r[6], "model": r[7].split()[-1],
                        "span": float(r[8]), "well": r[10], "scada": r[11] == "Yes"})
    devices = [{"tag": r[0], "pad": r[1], "cls": r[2], "model": r[5], "serial": r[6],
                "in_service": r[7] if isinstance(r[7], dt.datetime) else dt.datetime.combine(r[7], dt.time())}
               for r in list(wb["Pneumatic devices"].iter_rows(values_only=True))[1:]]
    gas = {}
    for r in rows(p("gas")):
        if r["sample_date"].startswith("2026"):
            gas[r["surface_location"]] = float(r["methane_mol_pct"]) / 100.0
    vol = {}
    for r in rows(p("vol")):
        vol.setdefault(r["uwi"], {})[dt.date.fromisoformat(r["production_date"])] = float(r["condensate_m3"]) + float(r["water_m3"])
    ctr = {}
    for r in rows(p("ctr")):
        ctr.setdefault(r["tag"], []).append((dt.datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC),
                                             int(r["value"])))
    cyc = rows(p("cycles"))
    wo = rows(p("wo"))
    sv = pdf_text(p("survey"))
    return {"scf": scf, "rho": rho, "line": line, "per_cycle": per_cycle, "bleed_rate": bleed_rate, "pads": pads,
            "wells": wells, "vessels": vessels, "devices": devices, "gas": gas, "vol": vol, "ctr": ctr, "cyc": cyc, "wo": wo,
            "survey": sv}


# ------------------------------------------------------------------------------------------------ plunger cycles
def moves(B):
    """Controller units moved between wells, from the work orders: serial, receiving well, local time it ran there."""
    out = []
    for w in B["wo"]:
        t = w["description"]
        donor = re.search(r"(?:off|from) (LRL [A-Z]+ [\d-]+ #\d)", t)
        sn = re.search(r"s/n (PCX-\d+)", t)
        hm = re.search(r"\b(\d\d):(\d\d)\b", t)
        names = re.findall(r"LRL [A-Z]+ [\d-]+ #\d", t)
        if donor and sn and hm and len(set(names)) == 2 and re.search(r"dead|blank|failed|No display", t):
            day = local(w["created_local"]).date()
            out.append({"serial": sn.group(1), "to": next(n for n in names if n != donor.group(1)), "from": donor.group(1),
                        "at": dt.datetime(day.year, day.month, day.day, int(hm.group(1)), int(hm.group(2)))})
    return out


def true_cycles(B):
    """Each controller cycle once (by unit and its own cycle count), on the well the unit was on."""
    mv = moves(B)
    seen, out = set(), []
    for r in B["cyc"]:
        k = (r["controller_sn"], int(r["cycle_count"]))
        if k in seen:
            continue
        seen.add(k)
        t = local(r["valve_open_local"])
        well = r["well"]
        for m in mv:
            if r["controller_sn"] == m["serial"] and t >= m["at"]:
                well = m["to"]
        out.append({"serial": r["controller_sn"], "well": well, "label": r["well"], "cc": int(r["cycle_count"]),
                    "ac": int(r["arrival_count"]), "t": t, "arrived": r["result"] == "ARRIVE"})
    return out


def nonarrivals(B, cyc=None):
    cyc = cyc if cyc is not None else true_cycles(B)
    groups = {}
    for c in cyc:
        if WIN0 <= c["t"] < WIN1:
            groups.setdefault((c["well"], c["serial"]), []).append(c)
    out = {}
    for (well, serial), g in groups.items():
        g.sort(key=lambda c: c["cc"])
        n_cyc = g[-1]["cc"] - g[0]["cc"] + 1
        n_arr = g[-1]["ac"] - g[0]["ac"] + (1 if g[0]["arrived"] else 0)
        out[well] = out.get(well, 0) + n_cyc - n_arr
    return out


# ------------------------------------------------------------------------------------------------ level controllers
def band(v):
    r = v["bore"] * 0.0254 / 2.0
    return math.pi * r * r * v["span"] * 0.0254


def counter_cycles(series):
    s = sorted(series)
    w0 = dt.datetime(2026, 1, 1, 8, tzinfo=TZ).astimezone(UTC)
    w1 = dt.datetime(2027, 1, 1, 8, tzinfo=TZ).astimezone(UTC)
    inside = [(t, v) for t, v in s if w0 <= t <= w1]
    assert inside[0][0] == w0 and inside[-1][0] == w1, "counter samples at both window ends"
    tot = 0
    for (t0, a), (t1, b) in zip(inside, inside[1:]):
        tot += (b - a) % 65536
    return tot


def lc_cycles(B, route="golden", cyc=None):
    """Dump cycles per level controller under a route: golden (each arrival's slug against the band), volume
    (liquid over band everywhere, counted cycles where SCADA counts), arrivals (one dump per arrival on plunger wells)."""
    cyc = cyc if cyc is not None else true_cycles(B)
    arrivals = {}
    for c in cyc:
        if c["arrived"] and WIN0 <= c["t"] < WIN1:
            arrivals.setdefault(c["well"], {}).setdefault(prod_day(c["t"]), 0)
            arrivals[c["well"]][prod_day(c["t"])] += 1
    out = {}
    for v in B["vessels"]:
        w = B["wells"][v["well"]]
        liq = B["vol"][w["uwi"]]
        bnd = band(v)
        if v["scada"]:
            tag = "%s_%s_LC%s.DMPCNT" % ({"Kakwa": "KAK", "Elmworth": "ELM"}[B["pads"][v["pad"]]["area"]], v["lc"][3:7],
                                         v["lc"][-2:])
            out[v["lc"]] = counter_cycles(B["ctr"][tag])
            continue
        if w["lift"] == "Flowing" or route == "volume":
            out[v["lc"]] = sum(liq.values()) / bnd
            continue
        days = arrivals.get(v["well"], {})
        if route == "arrivals":
            out[v["lc"]] = sum(days.values())
            continue
        lvl, n = 0.0, 0
        for day in sorted(liq):
            a = days.get(day, 0)
            if a == 0:
                continue
            s = liq[day] / a
            for _ in range(a):
                lvl += s
                if lvl >= bnd - 1e-12:
                    n += 1
                    lvl = 0.0
        out[v["lc"]] = n
    return out


def lc_kg(B, cycles):
    kg = {}
    for v in B["vessels"]:
        x = B["gas"][B["pads"][v["pad"]]["lsd"]]
        kg[v["lc"]] = cycles[v["lc"]] * B["per_cycle"][v["model"]] * B["scf"] * x * B["rho"]
    return kg


def pad_tonnes(B, kg):
    t = {}
    for v in B["vessels"]:
        t[v["pad"]] = t.get(v["pad"], 0.0) + kg[v["lc"]] / 1000.0
    return t


def campaign_tonnes(B):
    """Rung 0: the survey's mean vent rate per level controller over its test hours, for every hour of the year."""
    lines = re.findall(r"(\d{4}-\d\d-\d\d) (LRL \w+ \d+-\d+ #\d) (CL-200|SV-40|DLC-3) (\d+) (\d+) ([0-9.]+)", B["survey"])
    rate = sum(float(x[5]) for x in lines) / sum(int(x[3]) for x in lines) * 60.0
    t = {}
    for v in B["vessels"]:
        x = B["gas"][B["pads"][v["pad"]]["lsd"]]
        t[v["pad"]] = t.get(v["pad"], 0.0) + rate * 8760 * B["scf"] * x * B["rho"] / 1000.0
    return t, rate, len(lines)


# ------------------------------------------------------------------------------------------------ continuous bleed
def bleed(B, join="model"):
    """Each continuous-bleed device's 2026 stints and methane. join='model' finds the surveyed device by the pad,
    the model and the survey date; join='tag' takes the survey's tag at face value against the register."""
    y0, y1 = dt.datetime(2026, 1, 1, 8), dt.datetime(2027, 1, 1, 8)
    stints = []
    for d in B["devices"]:
        if d["cls"] != "Continuous bleed":
            continue
        start = max(y0, d["in_service"]) if d["in_service"] > y0 else y0
        stints.append({"serial": d["serial"], "model": d["model"], "pad": d["pad"], "tag": d["tag"], "start": start, "end": y1})
    depres = []
    for w in B["wo"]:
        t = w["description"]
        m = re.search(r"Replaced controller (\w{3}) (\d+) at (\d\d):(\d\d) with .*? s/n (\S+), old unit s/n (\S+) ", t)
        if m:
            when = dt.datetime(2026, MONTHS[m.group(1)], int(m.group(2)), int(m.group(3)), int(m.group(4)))
            for s in stints:
                if s["serial"] == m.group(5):
                    s["start"] = when
            old = m.group(6)
            model = {"CP": "CP-10", "PC": "PC-60", "TC": "TC-5"}[old.split("-")[0]]
            stints.append({"serial": old, "model": model, "pad": w["pad"], "tag": w["equipment_tag"], "start": y0, "end": when})
        m = re.search(r"Isolated fuel and instrument supply (\w{3}) (\d+) at (\d\d):(\d\d), heater package incl\. bath TC s/n (\S+) "
                      r"pulled", t)
        if m:
            when = dt.datetime(2026, MONTHS[m.group(1)], int(m.group(2)), int(m.group(3)), int(m.group(4)))
            stints.append({"serial": m.group(5), "model": "TC-5", "pad": w["pad"], "tag": w["equipment_tag"], "start": y0,
                           "end": when})
        m = re.search(r"bath TC s/n (\S+), fuel and instrument supply tied in and on (\w{3}) (\d+) at (\d\d):(\d\d)", t)
        if m:
            when = dt.datetime(2026, MONTHS[m.group(2)], int(m.group(3)), int(m.group(4)), int(m.group(5)))
            for s in stints:
                if s["serial"] == m.group(1) and s["pad"] == w["pad"]:
                    s["start"] = when
        m = re.search(r"instrument supply isolated (\w{3}) (\d+) (\d\d):(\d\d) to (\w{3}) (\d+) (\d\d):(\d\d)", t)
        if m:
            a = dt.datetime(2026, MONTHS[m.group(1)], int(m.group(2)), int(m.group(3)), int(m.group(4)))
            b = dt.datetime(2026, MONTHS[m.group(5)], int(m.group(6)), int(m.group(7)), int(m.group(8)))
            depres.append((w["pad"], a, b))
    surveyed = re.findall(r"(\d{4}-\d\d-\d\d) (\w+ \d+-\d+) ((?:PC|TC)-\d) (CP-10|PC-60|TC-5) ([0-9.]+) ([0-9.]+)", B["survey"])
    rate = {}
    for date, pad, tag, model, meas, rated in surveyed:
        day = dt.datetime.fromisoformat(date) + dt.timedelta(hours=11)
        here = [s for s in stints if s["pad"] == pad and s["start"] <= day < s["end"]]
        if join == "model":
            cand = [s for s in here if s["model"] == model]
            if len(cand) > 1:
                cand = [s for s in cand if s["tag"] == tag] or cand
        else:
            cand = [s for s in here if s["tag"] == tag]
        if cand:
            rate[cand[0]["serial"]] = float(meas)
    out = []
    for s in stints:
        hours = (s["end"] - s["start"]).total_seconds() / 3600.0
        for pad, a, b in depres:
            if pad == s["pad"]:
                lo, hi = max(a, s["start"]), min(b, s["end"])
                if hi > lo:
                    hours -= (hi - lo).total_seconds() / 3600.0
        r = rate.get(s["serial"], B["bleed_rate"][s["model"]])
        x = B["gas"][B["pads"][s["pad"]]["lsd"]]
        out.append(dict(s, hours=hours, rate=r, kg=r * hours * B["scf"] * x * B["rho"]))
    return out


def bleed_by_maker_area(B, stints):
    maker = {"CP-10": "Corrigan Controls", "PC-60": "Aldous Valve and Instrument"}
    out = {}
    for s in stints:
        if s["model"] not in maker:
            continue
        k = (maker[s["model"]], B["pads"][s["pad"]]["area"])
        out[k] = out.get(k, 0.0) + s["kg"]
    return out


def rnd(x, n=0):
    q = 10 ** n
    return int(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)


# ------------------------------------------------------------------------------------------------ the check
def main(target, golden):
    B = load(target)
    cyc = true_cycles(B)
    cy = lc_cycles(B, "golden", cyc)
    kg = lc_kg(B, cy)
    pt = pad_tonnes(B, kg)
    call = sorted(p for p, v in pt.items() if v > B["line"])
    na = nonarrivals(B, cyc)
    bma = bleed_by_maker_area(B, bleed(B, "model"))
    g = openpyxl.load_workbook(os.path.join(golden, "larchmere_source_inventory_2026.xlsx"), read_only=True)
    bad = []
    src = list(g["Annex B sources"].iter_rows(values_only=True))
    lc_rows = {r[2]: r for r in src[6:] if r and r[3] == "Intermittent vent"}
    assert len(lc_rows) == len(B["vessels"]), "one Annex B row per level controller"
    for v in B["vessels"]:
        if lc_rows[v["lc"]][10] != int(rnd(kg[v["lc"]])):
            bad.append("kg %s golden %s verifier %.2f" % (v["lc"], lc_rows[v["lc"]][10], kg[v["lc"]]))
    pads_g = {r[0]: r for r in list(g["Annex B pads"].iter_rows(values_only=True))[1:]}
    for p, v in pt.items():
        if abs(pads_g[p][2] - rnd(v, 2)) > 1e-9:
            bad.append("pad %s golden %s verifier %.4f" % (p, pads_g[p][2], v))
        if (pads_g[p][4] == "Yes") != (v > B["line"]):
            bad.append("pad %s conversion flag" % p)
    pl = {r[1]: r[3] for r in list(g["Plunger lift wells"].iter_rows(values_only=True))[1:]}
    for w, n in na.items():
        if pl.get(w) != n:
            bad.append("non-arrivals %s golden %s verifier %s" % (w, pl.get(w), n))
    assert len(pl) == len(na), "every plunger well in the golden"
    bm = {(r[0], r[1]): r[2] for r in list(g["Sales PCs by maker"].iter_rows(values_only=True))[1:]}
    for k, v in bma.items():
        if bm.get(k) != int(rnd(v)):
            bad.append("bleed %s golden %s verifier %.2f" % (k, bm.get(k), v))
    from pptx import Presentation
    prs = Presentation(os.path.join(golden, "controller_conversion_2027.pptx"))
    tbl = next(sh for sh in prs.slides[0].shapes if sh.has_table).table
    deck = sorted(tbl.cell(i, 0).text for i in range(1, len(tbl.rows)))
    if deck != call:
        bad.append("deck list %s against %s" % (deck, call))
    for i in range(1, len(tbl.rows)):
        if tbl.cell(i, 2).text != "%.2f" % rnd(pt[tbl.cell(i, 0).text], 2):
            bad.append("deck tonnes %s" % tbl.cell(i, 0).text)
    vol = pad_tonnes(B, lc_kg(B, lc_cycles(B, "volume", cyc)))
    arr = pad_tonnes(B, lc_kg(B, lc_cycles(B, "arrivals", cyc)))
    camp, rate, ntests = campaign_tonnes(B)
    m = re.search(r"We tested\s+(\d+)\s+separator\s+level\s+controllers", B["survey"])
    assert m and int(m.group(1)) == ntests, "every survey level controller row parsed (%s of %s)" % (ntests, m and m.group(1))
    sets = {"volume": sorted(p for p, v in vol.items() if v > B["line"]),
            "arrivals": sorted(p for p, v in arr.items() if v > B["line"]),
            "campaign": sorted(p for p, v in camp.items() if v > B["line"])}
    for k, s in sets.items():
        if s == call:
            bad.append("route %s files the golden set" % k)
    print("verify: %d level controllers, %d pads, %d in the conversion; %d plunger wells; %d maker-area totals; "
          "routes volume %d, arrivals %d, campaign %d pads" % (len(kg), len(pt), len(call), len(na), len(bma),
                                                            len(sets["volume"]), len(sets["arrivals"]), len(sets["campaign"])))
    if bad:
        print("VERIFY FAILED:\n  " + "\n  ".join(bad[:40]))
        raise SystemExit(1)
    print("verify: every graded figure recomputes from the bundle")
    return {"B": B, "call": call, "kg": kg, "pt": pt, "na": na, "bma": bma, "sets": sets, "cyc": cyc}


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(here, "target"), os.path.join(here, "golden"))
