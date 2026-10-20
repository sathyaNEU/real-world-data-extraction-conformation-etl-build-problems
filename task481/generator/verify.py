"""Independent verification of task481 from the shipped bundle and the golden workbook only: the restated 2024 total,
the 2025 count and the change, with the walk from the published total; the shootings by quarter, 2023 to 2025. Written
apart from methods.py."""
import csv
import datetime as dt
import os
import sys
import zoneinfo

import openpyxl

CENTRAL = zoneinfo.ZoneInfo("America/Chicago")
DV = {"SE", "CS", "PA", "SB", "CH", "GP", "GC", "IL", "SP", "SC", "SS", "OF", "BG", "XS", "XR", "CF"}


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        r = csv.DictReader(fh)
        return list(r)


def local_ym(s):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(CENTRAL)
    return t.year, t.month


def return_a(target):
    out = {}
    order = ["1A", "1B", "2", "3", "3A", "3B", "3C", "3D", "4", "4A", "4B", "4C", "4D", "4E", "5", "5A", "5B", "5C",
             "6", "7", "7A", "7B", "7C"]
    mon = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
                                           "Nov", "Dec"])}
    for y in (2023, 2024):
        wb = openpyxl.load_workbook(os.path.join(target, "return_a_%d.xlsx" % y), read_only=True, data_only=True)
        for ws in wb.worksheets:
            m = mon[ws.title[:3]]
            vals = list(ws.iter_rows(values_only=True))
            i0 = [i for i, r in enumerate(vals) if r[0] == "Line"][0]
            for code, r in zip(order, vals[i0 + 1:]):
                assert r[0] == code, (ws.title, code, r[0])
                out[(y, m, code)] = r[4]          # column 4: actual offenses
    return out


def main(target, gdir):
    ext = rows(os.path.join(target, "epd_nibrs_offense_extract_2024-10_to_2026-09.csv"))
    ra = return_a(target)
    dvu = rows(os.path.join(target, "dvu_case_log_2021_2026.csv"))
    q4 = [(2024, 10), (2024, 11), (2024, 12)]
    agg = ("4A", "4B", "4C", "4D")
    n, k, incs = {}, {}, {}
    month13a = {}
    for r in ext:
        ym = local_ym(r["report_datetime_utc"])
        if r["offense_code"] == "13A":
            month13a[ym] = month13a.get(ym, 0) + 1
        if ym not in q4:
            continue
        incs.setdefault(r["incident_number"], set()).add(r["offense_code"])
    rob_inc, hom = set(), 0
    for r in ext:
        ym = local_ym(r["report_datetime_utc"])
        if ym not in q4:
            continue
        c, o = r["ucr_summary_class"], r["offense_code"]
        if c in agg or c == "4E":
            key = c if c != "4E" else ("dv" if r["relationship_1"] in DV else "non")
            n[key] = n.get(key, 0) + 1
            k[key] = k.get(key, 0) + (o == "13A")
        elif c == "NS" and o == "13A":
            key = "hhom" if "09A" in incs[r["incident_number"]] else "hrob"
            k[key] = k.get(key, 0) + 1
        if o == "120" and c in ("3A", "3B", "3C", "3D"):
            rob_inc.add(r["incident_number"])
        if o == "09A" and c == "1A":
            hom += 1
    n["hrob"], n["hhom"] = len(rob_inc), hom
    rate = {key: k.get(key, 0) / n[key] for key in n}
    dv = {}
    for d in dvu:
        y, m = int(d["report_date"][:4]), int(d["report_date"][5:7])
        if y == 2024 and m <= 9 and d["ucr_line"] == "4E" and d["case_status"] != "UNFOUNDED":
            dv[m] = dv.get(m, 0) + 1
    restated, hidden, gained, lost = 0.0, 0.0, 0.0, 0.0
    for m in range(1, 10):
        a = {l: ra[(2024, m, l)] for l in agg}
        restated += sum(rate[l] * a[l] for l in agg)
        lost += sum((1 - rate[l]) * a[l] for l in agg)
        g = rate["dv"] * dv[m] + rate["non"] * (ra[(2024, m, "4E")] - dv[m])
        h = rate["hrob"] * sum(ra[(2024, m, l)] for l in ("3A", "3B", "3C", "3D")) + rate["hhom"] * ra[(2024, m, "1A")]
        restated += g + h
        gained += g
        hidden += h
    restated += sum(month13a.get(ym, 0) for ym in q4)
    gained += k["dv"] + k["non"]
    hidden += k["hrob"] + k["hhom"]
    lost += sum(n[l] - k[l] for l in agg)
    published = sum(ra[(2024, m, l)] for m in range(1, 13) for l in agg)
    y25 = sum(month13a.get((2025, m), 0) for m in range(1, 13))
    change = int(round(100 * (y25 / restated - 1)))
    wb = openpyxl.load_workbook(os.path.join(gdir, "ellsmere_aggravated_assault.xlsx"), data_only=True)
    ws = wb["Aggravated assault"]
    top = [c for c in next(ws.iter_rows(min_row=5, max_row=5, values_only=True))]
    got = [top[1], top[2], int(round(100 * top[3]))]
    got += [r[1] for r in ws.iter_rows(min_row=9, max_row=13, values_only=True)]
    want = [int(round(restated, -2)), y25, change, published, round(hidden), round(gained), -round(lost), round(restated)]
    good = got == want and ws["D5"].number_format.startswith("+0%")
    print("verify: call %s (restated %d, 2025 %d, change %+d%%, lines %d %d %d)" % (
        "PASS" if good else "FAIL %s %s" % (got, want), round(restated), y25, change, round(hidden), round(gained),
        round(lost)))
    # shootings
    gvr = rows(os.path.join(target, "gvr_shooting_log_2023_2026.csv"))
    me = rows(os.path.join(target, "medical_examiner_homicide_list_2023_2026.csv"))
    died = {(d["date_of_injury"], d["injury_location"].rsplit(", ", 1)[0], d["age"], d["sex"]) for d in me
            if d["injury_location"].endswith(", ELLSMERE")}
    # a block the log puts outside the city in any row is outside it in every row
    out_blocks = {g["block"].split(" (")[0] for g in gvr if g["inside_city"] == "N"}
    seen, vic, sho = set(), {}, {}
    for g in gvr:
        if g["circumstance"] != "ASSAULT" or g["inside_city"] != "Y" or g["outcome"] != "WOUNDED":
            continue
        if g["block"] in out_blocks:
            continue
        if (g["shot_datetime"][:10], g["block"], g["victim_age"], g["victim_sex"]) in died:
            continue
        person = (g["rms_number"], g["shot_datetime"], g["victim_age"], g["victim_sex"])
        if person in seen:
            continue
        seen.add(person)
        q = "%s Q%d" % (g["shot_datetime"][:4], (int(g["shot_datetime"][5:7]) - 1) // 3 + 1)
        vic[q] = vic.get(q, 0) + 1
        sho.setdefault(q, set()).add((g["shot_datetime"], g["block"]))
    ws3 = wb["Shootings"]
    good_s = True
    quarters = ["%d Q%d" % (y, q) for y in (2023, 2024, 2025) for q in (1, 2, 3, 4)]
    if [r[0] for r in ws3.iter_rows(min_row=2, max_row=13, values_only=True)] != quarters:
        good_s = False
    for r in ws3.iter_rows(min_row=2, max_row=13, values_only=True):
        if (vic.get(r[0]), len(sho.get(r[0], ()))) != (r[1], r[2]):
            good_s = False
            print("  shootings %s: %s %s against %s %s" % (r[0], vic.get(r[0]), len(sho.get(r[0], ())), r[1], r[2]))
    print("verify: shootings %s" % ("PASS" if good_s else "FAIL"))
    return good and good_s


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
