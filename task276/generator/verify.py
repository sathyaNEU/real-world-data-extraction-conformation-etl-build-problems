"""Independent verifier: reads only the shipped bundle (target/, golden/, figures.json, submission.md) on its own code
path, takes every constant from the documents' own text, and recomputes the call, every graded figure and the
deliverables' content. Imports nothing from the generator."""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import pandas as pd
from pypdf import PdfReader


def pdf_text(p):
    t = "\n".join(pg.extract_text() or "" for pg in PdfReader(p).pages)
    assert len(t) > 200, p
    return t


def docx_text(p):
    x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
    assert len(t) > 200, p
    return t


def num(s):
    return float(s.replace(",", "").replace("+", ""))


def day(s):
    if s is None or (not isinstance(s, str) and pd.isna(s)) or s == "":
        return None
    if isinstance(s, (pd.Timestamp, dt.datetime)):
        return s.date()
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y) + (2000 if len(y) == 2 else 0), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def find(T, name):
    for root, _, files in os.walk(T):
        if name in files:
            return os.path.join(root, name)
    raise FileNotFoundError(name)


def documents(T):
    std = docx_text(find(T, "cab_fit_standard_issue2.docx"))
    assert "latest measurement stands" in std
    up = int(re.search(r"rises at least (\d+) degrees", std).group(1))
    dn = int(re.search(r"falls at least (\d+) degrees", std).group(1))
    pm = pdf_text(find(T, "driver_posture_model_ellisand_2025.pdf"))
    m = re.search(r"([\d.]+) \+ ([\d.]+) x \(stature - (\d+)\) \+ ([\d.]+) x \(BMI - (\d+)\) - ([\d.]+) x \(H30 - (\d+)\)", pm)
    t = re.search(r"([\d.]+) \+ ([\d.]+) x \(stature - (\d+)\) \+ ([\d.]+) x \(BMI - (\d+)\)\n", pm)
    ex = int(re.search(r"(\d+) mm forward of the hip point", pm).group(1))
    ez = float(re.search(r"H30 \+ ([\d.]+) x sitting eye height", pm).group(1))
    model = {"hx": [float(x) for x in m.groups()], "th": [float(x) for x in t.groups()], "ex": ex, "ez": ez}
    seat = pdf_text(find(T, "seat_dimension_sheet_brevin_as7.pdf"))
    along = float(re.search(r"top rear corner\n([\d.]+)", seat).group(1))
    behind = float(re.search(r"behind the torso line at the top rear corner\n([\d.]+)", seat).group(1))
    rec = re.search(r"Recline range, torso line from vertical \(degrees\)\n(\d+) to (\d+)", seat)
    cabs = {}
    rows = re.findall(r"<w:tr>(.*?)</w:tr>", zipfile.ZipFile(find(T, "cab_fit_standard_issue2.docx")).read(
        "word/document.xml").decode("utf-8"))
    short = []
    for r in rows:
        cells = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<w:tc>(.*?)</w:tc>", r)]
        if len(cells) == 3 and cells[2].startswith("Tender"):
            short.append((cells[0], cells[1]))
    for fname, conv in (("package_drawing_data_pennick.pdf", "Pennick Coachbuild"),
                        ("package_drawing_data_wrenfold.pdf", "Wrenfold Bodies"),
                        ("package_drawing_data_ostrel.pdf", "Ostrel Vehicle Conversions")):
        txt = pdf_text(find(T, fname))
        for sec in re.split(r"\n(?=\w+ conversion on the )", txt)[1:]:
            ch = re.match(r"\w+ conversion on the (\w+) chassis-cab", sec).group(1)
            sg = re.search(r"SgRP located (\d+) mm aft of and (\d+) mm above", sec)
            ox, oz = (int(sg.group(1)), int(sg.group(2))) if sg else (0, 0)

            def val(label, pair=False, z_default=None):
                v = re.search(re.escape(label) + r"[^\n]*\n([+\-\d, ]+)\n", sec).group(1)
                if pair:
                    parts = [num(x) for x in v.split(", ")] if re.search(r"\d, [+\-\d]", v) else [num(v), z_default]
                    return parts[0] + ox, parts[1] + oz
                return num(v)
            h30 = val("Seat height H30")
            cabs[(conv, ch)] = {"h30": h30, "t0": val("H-point travel, front limit") + ox,
                                "t1": val("H-point travel, rear limit") + ox,
                                "b0": val("Bulkhead trim face at floor", True, 0.0),
                                "b1": val("Bulkhead trim face 1,700 above floor", True, 1700.0),
                                "hdr": val("Windscreen header, lower edge of clear area", True),
                                "bon": val("Lowest road sight point over bonnet", True)}
    kpi = pdf_text(find(T, "fleet_performance_reporting_standard_issue4.pdf"))
    assert "first raised" in kpi and "that date not counted" in kpi and "365 days" in kpi
    return {"up": up, "dn": dn, "model": model, "along": along * 25.4, "behind": behind * 25.4,
            "recline": (int(rec.group(1)), int(rec.group(2))), "cabs": cabs, "shortlist": short}


def drivers(T):
    with open(find(T, "front_line_driving_roster_2026-10-01.csv"), encoding="utf-8-sig") as fh:
        roster = list(csv.DictReader(fh))
    cw = pd.read_excel(find(T, "vennerley_staff_number_crosswalk.xlsx"), dtype=str)
    new = dict(zip(cw.iloc[:, 0], cw.iloc[:, 1]))
    ms = pd.read_excel(find(T, "cab_fit_measurements_2025_26.xlsx"))
    latest = {}
    for _, r in ms.iterrows():
        k = str(r["Staff number"])
        k = new.get(k, k)
        if r["Form"] == "Vennerley paper form":
            s = (r["Stature (ft)"] * 12 + r["Stature (in)"]) * 25.4
            e = r["Sitting eye height (in)"] * 25.4
            w = (r["Weight (st)"] * 14 + r["Weight (lb)"]) * 0.45359237
        else:
            s, e, w = r["Stature (mm)"], r["Sitting eye height (mm)"], r["Weight (kg)"]
        key = (r["Date measured"], r["Ref"])
        if k not in latest or key > latest[k][0]:
            latest[k] = (key, float(s), float(w), float(e))
    out = []
    for r in roster:
        _, s, w, e = latest[r["Staff number"]]
        out.append((r["Sex"], s, w, e))
    return out


def fails(D, cab, sex_s_w_e):
    sex, s, w, e = sex_s_w_e
    m = D["model"]
    bmi = w / (s / 1000.0) ** 2
    a, b, c0, d, e0, f, g0 = m["hx"]
    xh = a + b * (s - c0) + d * (bmi - e0) - f * (cab["h30"] - g0)
    t0, t1, t2, t3, t4 = m["th"]
    th = t0 + t1 * (s - t2) + t3 * (bmi - t4)
    xe, ze = xh - m["ex"], cab["h30"] + m["ez"] * e
    up = math.degrees(math.atan2(cab["hdr"][1] - ze, xe - cab["hdr"][0]))
    dn = math.degrees(math.atan2(ze - cab["bon"][1], xe - cab["bon"][0]))
    r = math.radians(th)
    cx = xh + D["along"] * math.sin(r) + D["behind"] * math.cos(r)
    cz = cab["h30"] + D["along"] * math.cos(r) - D["behind"] * math.sin(r)
    (x0, z0), (x1, z1) = cab["b0"], cab["b1"]
    bulk = x0 + (x1 - x0) * (cz - z0) / (z1 - z0)
    seated = cab["t0"] <= xh <= cab["t1"] and D["recline"][0] <= th <= D["recline"][1] and cx <= bulk
    return not (seated and up >= D["up"] and dn >= D["dn"])


def fleet(T):
    reg = pd.read_excel(find(T, "front_line_fleet_register_2026-10-01.xlsx"), dtype={"Former fleet number": str})
    dis = pd.read_excel(find(T, "vehicle_disposals_2025_26.xlsx"), dtype={"Former fleet number": str})
    al = pd.read_excel(find(T, "vennerley_asset_list_2025-06-27.xlsx"))
    orig = {r["Vehicle"]: r["In service"].date() for _, r in al.iterrows()}
    V = []
    for _, r in reg.iterrows():
        f = r["Former fleet number"] if isinstance(r["Former fleet number"], str) else ""
        V.append({"no": r["Fleet number"], "former": f, "conv": r["Converter"], "ch": r["Chassis-cab"],
                  "start": orig.get(f, r["In service"].date()), "end": None})
    for _, r in dis.iterrows():
        f = r["Former fleet number"] if isinstance(r["Former fleet number"], str) else ""
        V.append({"no": r["Fleet number"], "former": f, "conv": r["Converter"], "ch": r["Chassis-cab"],
                  "start": orig.get(f, r["In service"].date()), "end": r["Disposed"].date()})

    def owner(label, d):
        c = [v for v in V if label in (v["no"], v["former"])]
        held = [v for v in c if v["end"] is None or d < v["end"]]
        held.sort(key=lambda v: v["end"] is None)
        return (held or c)[0]
    cmap = pd.read_excel(find(T, "workshop_code_map.xlsx"))
    to_code = dict(zip(cmap.iloc[:, 0], cmap.iloc[:, 2]))
    with open(find(T, "workshop_jobs_2025_26.csv"), encoding="utf-8") as fh:
        merged = list(csv.DictReader(fh))
    with open(find(T, "vennerley_workshop_jobs_apr_jun_2025.csv"), encoding="utf-8") as fh:
        legacy = list(csv.DictReader(fh))
    cut = dt.date(2025, 7, 1)
    jobs, spells = [], []
    carried = {}
    for r in legacy:
        v = owner(r["Vehicle"], day(r["Date in"]))
        code = to_code[r["Defect code"]]
        if r["Status"] == "TRANSFERRED":
            carried[(id(v), code)] = carried.get((id(v), code), 0) + 1
        jobs.append((v, day(r["Date in"]), code))
        if r["Off road"] == "Y":
            spells.append((v, day(r["Date in"]), day(r["Date out"]) or cut))
    for r in merged:
        v = owner(r["fleet_no"], day(r["raised"]))
        if day(r["raised"]) == cut and carried.get((id(v), r["job_code"]), 0) > 0:
            carried[(id(v), r["job_code"])] -= 1
        else:
            jobs.append((v, day(r["raised"]), r["job_code"]))
        if r["off_road"] == "Y":
            spells.append((v, day(r["off_road_from"]), day(r["back_on_road"])))
    assert all(x == 0 for x in carried.values()), "every carried Vennerley job has its fleet system twin"
    fy0, fy1 = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
    q = lambda d: (d.month - 4) // 3 if d.month >= 4 else 3
    out = {"jobs": {}, "miles": {}, "days": {}, "vy": {}}
    for v, d, code in jobs:
        if code in ("B12", "B30") and fy0 <= d <= fy1:
            out["jobs"].setdefault(v["conv"], [0, 0, 0, 0])[q(d)] += 1
    seen = {}
    for v, a, b in spells:
        d = a
        while d < b:
            if fy0 <= d <= fy1:
                seen.setdefault(id(v), (v, set()))[1].add(d)
            d += dt.timedelta(days=1)
    for v, ds in seen.values():
        for d in ds:
            out["days"].setdefault(v["ch"], [0, 0, 0, 0])[q(d)] += 1
    for v in V:
        a = max(v["start"], fy0)
        b = min(v["end"] or fy1 + dt.timedelta(days=1), fy1 + dt.timedelta(days=1))
        out["vy"][v["ch"]] = out["vy"].get(v["ch"], 0) + max(0, (b - a).days)
    units = pd.read_excel(find(T, "telematics_unit_changes.xlsx"))
    rd = {}
    with open(find(T, "telematics_daily_odometer_2025_26.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rd.setdefault(r["unit_id"], []).append((day(r["reading_date"]), float(r["odometer_miles"])))
    for _, u in units.iterrows():
        fitted = u["Fitted"].date()
        removed = u["Removed"].date() if not pd.isna(u["Removed"]) else None
        v = owner(u["Fleet number"], max(fitted, fy0))
        xs = sorted(rd.get(u["Unit ID"], []))
        lo, hi = max(fitted, fy0), min(removed or fy1 + dt.timedelta(days=1), fy1 + dt.timedelta(days=1))
        inside = [x for x in xs if lo <= x[0] < hi]
        if not inside:
            continue
        base = u["Odometer entered at fitting (miles)"] if fitted >= fy0 else [x for x in xs if x[0] < lo][-1][1]
        out["miles"][v["conv"]] = out["miles"].get(v["conv"], 0.0) + inside[-1][1] - float(base)
    return out


def main(T, Gd, fig_path, sub_path):
    fig = json.load(open(fig_path))
    sub = open(sub_path).read()
    D = documents(T)
    assert len(D["shortlist"]) == 5 and D["up"] == fig["vision_up_deg"] and D["dn"] == fig["vision_down_deg"]
    dr = drivers(T)
    assert len(dr) == fig["drivers"], (len(dr), fig["drivers"])
    counts = {}
    for conv, ch in D["shortlist"]:
        cab = D["cabs"][(conv, ch)]
        f = [x for x in dr if fails(D, cab, x)]
        counts[(conv, ch)] = (len(f), sum(1 for x in f if x[0] == "F"))
    ids = {("Pennick Coachbuild", "FD35"): "PEN-FD35", ("Pennick Coachbuild", "RD43"): "PEN-RD43",
           ("Wrenfold Bodies", "FD35"): "WRE-FD35", ("Wrenfold Bodies", "RD43"): "WRE-RD43",
           ("Ostrel Vehicle Conversions", "FD35"): "OST-FD35"}
    for k, (n, w) in counts.items():
        assert fig["fail_" + ids[k]] == n and fig["women_" + ids[k]] == w, (k, n, w)
    order = sorted(counts, key=lambda k: counts[k][0])
    assert "%s on %s" % order[0] == fig["call"] and "%s on %s" % order[1] == fig["runner_up"]
    assert counts[order[1]][0] - counts[order[0]][0] == fig["gap"]
    F = fleet(T)
    for conv in ("Pennick Coachbuild", "Ostrel Vehicle Conversions"):
        k = conv.split()[0].lower()
        assert F["jobs"][conv] == [fig["jobs_%s_q%d" % (k, i)] for i in range(1, 5)], (conv, F["jobs"][conv])
        assert int(round(F["miles"][conv] / 100.0)) * 100 == fig["miles_%s" % k], (conv, F["miles"][conv])
        assert round(sum(F["jobs"][conv]) / F["miles"][conv] * 1e5, 2) == fig["jobs_rate_%s" % k]
    for ch in ("FD35", "RD43"):
        k = ch.lower()
        assert F["days"][ch] == [fig["vor_%s_q%d" % (k, i)] for i in range(1, 5)], (ch, F["days"][ch])
        vy = F["vy"][ch] / 365.0
        assert round(vy, 1) == fig["vy_%s" % k] and round(sum(F["days"][ch]) / vy, 1) == fig["vor_rate_%s" % k]
    # the deliverables carry the same figures
    wb = pd.read_excel(os.path.join(Gd, "cab_fit_2027.xlsx"), sheet_name=None, header=None)
    flat = " ".join(str(x) for df in wb.values() for x in df.values.ravel())
    for key in ("call_fail", "runner_up_fail", "gap", "jobs_pennick_q1", "vor_rd43_q4", "miles_ostrel"):
        assert str(fig[key]) in flat, key
    chart = pdf_text(os.path.join(Gd, "cab_fit_2027.pdf"))
    assert "Recommended" in chart and str(fig["call_fail"]) in chart
    for k, v in fig.items():
        if isinstance(v, int) and k.startswith(("fail_", "women_", "jobs_", "vor_")):
            assert format(v, ",") in sub, k
    print("verify: call %s (%d), runner-up %s (%d), %d drivers, every fleet figure and deliverable recomputed from the "
          "bundle" % (fig["call"], fig["call_fail"], fig["runner_up"], fig["runner_up_fail"], len(dr)))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(os.path.join(task, "target"), os.path.join(task, "golden"), os.path.join(here, "figures.json"),
         os.path.join(task, "submission.md"))
