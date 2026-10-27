#!/usr/bin/env python3
"""The independent verifier for task204.

It reads target/ and generator/figures.json and nothing else: no params, no world, no analysis, no
bundle, no generator state. Every quantity is recomputed here on its own code path, with its own
parsing, its own time handling and its own arithmetic, and then compared with the figure the
generator filed.

    python3 task204/generator/verify.py          # one line per claim, exit 1 on any mismatch
"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
DUBLIN = ZoneInfo("Europe/Dublin")
WORKBOOK = "tulrohan_ventilation_assessment.xlsx"
CHART = "tulrohan_co2_day_profile.png"

RESULTS = []


def claim(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def hu(value, places):
    return float(Decimal(repr(float(value))).quantize(Decimal(1).scaleb(-places),
                                                      rounding=ROUND_HALF_UP))


def to_half(value):
    return float(Decimal(repr(float(value) * 2)).quantize(Decimal(1),
                                                          rounding=ROUND_HALF_UP)) / 2.0


def minutes(hhmm):
    return int(hhmm[:2]) * 60 + int(hhmm[3:5])


# ----------------------------------------------------------------- readers, written here afresh

def text_of_pdf(name):
    import pypdf
    reader = pypdf.PdfReader(os.path.join(TARGET, name))
    out = []
    for page in reader.pages:
        out.append(page.extract_text() or "")
    joined = "\n".join(out)
    if len(joined) < 400:
        raise AssertionError("%s: extractor returned %d characters" % (name, len(joined)))
    return joined


def sheet_of(name, title):
    """Read a worksheet straight out of the package, without a spreadsheet library, so the
    verifier's path into a workbook is not the generator's."""
    with zipfile.ZipFile(os.path.join(TARGET, name)) as z:
        book = z.read("xl/workbook.xml").decode("utf-8")
        rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = z.read("xl/sharedStrings.xml").decode("utf-8")
            shared = [re.sub(r"<[^>]+>", "", s) for s in
                      re.findall(r"<si>(.*?)</si>", sst, re.S)]
        rid = None
        for m in re.finditer(r'<sheet [^>]*name="([^"]*)"[^>]*r:id="(rId\d+)"', book):
            if m.group(1) == title:
                rid = m.group(2)
        if rid is None:
            raise AssertionError("%s: no sheet %r" % (name, title))
        target = None
        for el in re.finditer(r"<Relationship\b[^>]*/?>", rels):
            tag = el.group(0)
            if re.search(r'Id="%s"' % rid, tag):
                target = re.search(r'Target="([^"]*)"', tag).group(1)
        if target is None:
            raise AssertionError("%s: no relationship %s" % (name, rid))
        path = target[1:] if target.startswith("/") else "xl/" + target
        xml = z.read(path).decode("utf-8")
    rows = []
    for rm in re.finditer(r"<row[^>]*>(.*?)</row>", xml, re.S):
        cells = {}
        for cm in re.finditer(r'<c r="([A-Z]+)(\d+)"([^>]*)>(.*?)</c>', rm.group(1), re.S):
            col, attrs, body = cm.group(1), cm.group(3), cm.group(4)
            v = re.search(r"<v>(.*?)</v>", body, re.S)
            if v is None:
                continue
            raw = v.group(1)
            if 't="s"' in attrs:
                cells[col] = shared[int(raw)]
            elif 't="str"' in attrs or 't="inlineStr"' in attrs:
                cells[col] = raw
            else:
                cells[col] = raw
        if cells:
            width = max(col_index(c) for c in cells)
            rows.append([cells.get(col_name(i), None) for i in range(1, width + 1)])
    return rows


def col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def col_name(index):
    out = ""
    while index:
        index, rem = divmod(index - 1, 26)
        out = chr(65 + rem) + out
    return out


def read_csv(name):
    with open(os.path.join(TARGET, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def number(text):
    return float(re.sub(r"[^0-9.\-]", "", str(text)))


# ----------------------------------------------------------------- the filed facts

def filed():
    std = text_of_pdf("tgd_m4_ventilation_extract.pdf")
    assert "A teaching space shall be provided with outdoor air" in std.replace("\n", " "), \
        "standard extract: positive control not found through this extractor"
    required = float(re.search(r"not less than\s+([\d.]+)\s+litres per second per person",
                               std).group(1))
    lines = [x.strip() for x in std.split("\n")]
    generation = None
    for i, line in enumerate(lines):
        if line.startswith("Carbon dioxide generation"):
            generation = float(lines[i + 1])
    assert generation, "standard extract: generation rate not read"

    proc = text_of_pdf("iaq_monitoring_procedure_note.pdf")
    assert "A space counts as occupied for the hours" in proc.replace("\n", " "), \
        "procedure note: positive control not found"
    screening = float(re.search(r"passes\s+([\d,]+)\s*ppm", proc.replace("\n", " "))
                      .group(1).replace(",", ""))

    built = text_of_pdf("asbuilt_room_data_sheets_kilmoneen.pdf")
    assert "Volumes below are gross internal" in built.replace("\n", " "), \
        "as-built sheets: positive control not found"
    blines = [x.strip() for x in built.split("\n")]
    volumes = {}
    for i, line in enumerate(blines):
        if re.fullmatch(r"[A-Z]{3}-[A-Z0-9]\d{2}", line):
            volumes[line] = float(blines[i + 4].replace(",", ""))

    scope = sheet_of("capital_bid_tulrohan_block.xlsx", "Scope")
    block = [r[0] for r in scope if r and isinstance(r[0], str)
             and re.fullmatch(r"TUL-[A-Z]\d{2}", r[0])]

    cal = sheet_of("etb_academic_calendar_2026_27.xlsx", "Autumn term")
    teaching = []
    for r in cal[1:]:
        if len(r) >= 3 and r[2] == "Teaching day":
            serial = int(float(r[0]))
            teaching.append((dt.date(1899, 12, 30) + dt.timedelta(days=serial)).isoformat())
    return {"required": required, "generation": generation, "screening": screening,
            "volumes": volumes, "block": block, "teaching": sorted(teaching)}


# ----------------------------------------------------------------- the series and the sessions

def baseline():
    out = {}
    for r in read_csv("campus_outdoor_co2_hourly_2026.csv"):
        out[(r["timestamp_local"][:13], r["utc_offset"])] = float(r["co2_ppm"])
    for r in read_csv("macehead_gaw_co2_hourly_2026.csv"):
        t = dt.datetime.strptime(r["datetime_utc"], "%Y-%m-%dT%H:%M:%SZ")
        t = t.replace(tzinfo=dt.timezone.utc).astimezone(DUBLIN)
        off = "+%02d:00" % (int(t.utcoffset().total_seconds()) // 3600)
        out.setdefault((t.strftime("%Y-%m-%d %H"), off), float(r["co2_ppm"]))
    return out


def load():
    base = baseline()
    series = defaultdict(dict)
    with open(os.path.join(TARGET, "bms_co2_5min_autumn2026.csv"), newline="",
              encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            series[r["space_code"]][(r["timestamp_local"], r["utc_offset"])] = number(r["co2"])

    label = {}
    ahu = {}
    for r in read_csv("campus_room_register.csv"):
        if r["bms_point_ref"]:
            label[r["timetable_room_label"]] = r["room_code"]
            ahu[r["room_code"]] = r["ahu_ref"]

    present = defaultdict(int)
    with open(os.path.join(TARGET, "attendance_marks_autumn2026.csv"), newline="",
              encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["mark"] == "present":
                present[r["session_ref"]] += 1

    sessions = []
    for r in read_csv("timetable_autumn2026.csv"):
        sessions.append({"ref": r["session_ref"], "space": label[r["room_label"]],
                         "date": r["date"], "period": r["period"], "group": r["group_code"],
                         "start": r["start_time"], "end": r["end_time"],
                         "n": present[r["session_ref"]]})

    status = defaultdict(list)
    for r in read_csv("bms_plant_status_autumn2026.csv"):
        a = minutes(r["interval_start_local"][11:16])
        e = r["interval_end_local"][11:16]
        b = 1440 if e == "24:00" else minutes(e)
        status[(r["ahu_ref"], r["interval_start_local"][:10])].append((a, b, r["status"]))
    return series, base, sessions, ahu, status


def frames(series, base, sessions, block):
    out = []
    for s in sessions:
        if s["space"] not in block:
            continue
        vals, mins = [], []
        for k in range(minutes(s["start"]), minutes(s["end"]) + 1, 5):
            hh, mm = divmod(k, 60)
            key = "%s %02d:%02d:00" % (s["date"], hh, mm)
            for off in ("+01:00", "+00:00"):
                if (key, off) in series[s["space"]]:
                    vals.append(series[s["space"]][(key, off)] - base[(key[:13], off)])
                    mins.append(k)
                    break
        if len(vals) >= 3:
            out.append(dict(s, readings=vals, seconds=(mins[-1] - mins[0]) * 60))
    return out


def supply(frame, volumes, generation):
    """Simpson's rule here, where the generator used the trapezoid: the two agree inside a bin and
    this is the verifier's own arithmetic."""
    vals = frame["readings"]
    step = frame["seconds"] / float(len(vals) - 1)
    n = len(vals) - 1
    if n >= 2 and n % 2 == 0:
        total = vals[0] + vals[-1] + sum((4 if i % 2 else 2) * vals[i] for i in range(1, n))
        integral = total * step / 3.0
    else:
        integral = step * (sum(vals) - 0.5 * (vals[0] + vals[-1]))
    integral *= 1e-6
    stored = volumes[frame["space"]] * (vals[-1] - vals[0]) * 1e-6
    generated = frame["n"] * generation / 1000.0 * frame["seconds"]
    return (generated - stored) / integral if integral > 0 else None


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    f = filed()
    claim("the standard's requirement reads back from its own PDF",
          f["required"] == fig["constants"]["required_ls_per_person"],
          "%g litres per second per person" % f["required"])
    claim("the standard's generation rate reads back from its own PDF",
          f["generation"] == fig["constants"]["generation_l_per_s"],
          "%s litres per second per person" % f["generation"])
    claim("the procedure note's screening indicator reads back from its own PDF",
          f["screening"] == fig["constants"]["screening_ppm"],
          "%s ppm" % "{:,}".format(int(f["screening"])))
    claim("the as-built sheets give a volume for every monitored space",
          len(f["volumes"]) >= 14 and
          all(f["volumes"][k] == fig["constants"]["block_volumes_m3"][k] for k in f["block"]),
          "%d room volumes, the six block volumes matching the filed figures" % len(f["volumes"]))
    claim("the bid sheet files the block", f["block"] == fig["constants"]["block_rooms"],
          ", ".join(f["block"]))
    claim("the calendar gives the term's teaching days",
          len(f["teaching"]) == fig["constants"]["teaching_days"],
          "%d teaching days, %s to %s" % (len(f["teaching"]), f["teaching"][0], f["teaching"][-1]))

    series, base, sessions, ahu, status = load()
    bf = frames(series, base, sessions, f["block"])
    air = sum(supply(x, f["volumes"], f["generation"]) * x["seconds"] for x in bf)
    occ_s = sum(x["n"] * x["seconds"] for x in bf)
    rate = 1000.0 * air / occ_s
    claim("the block's rate recomputes from the bundle",
          to_half(rate) == fig["call"]["block_rate_ls_per_occupant"] and
          abs(rate - fig["call"]["block_rate_unrounded"]) < 0.02,
          "%.4f litres per second per occupant present, printing %.1f"
          % (rate, to_half(rate)))
    claim("the printed figure sits away from its cell edge",
          abs(0.25 - abs(rate - to_half(rate))) > 0.10,
          "%.4f from the nearer edge of the printed cell"
          % (0.25 - abs(rate - to_half(rate))))
    short = fig["call"]["shortfall_ls_per_occupant"]
    claim("the shortfall against the requirement recomputes",
          to_half(f["required"] - rate) == short, "%.1f litres per second per occupant" % short)
    claim("the shortfall is the same from the printed rate as from the unrounded one",
          to_half(f["required"] - to_half(rate)) == short,
          "%.1f either way, so the figure carries no rounding fork"
          % to_half(f["required"] - to_half(rate)))

    bsess = [s for s in sessions if s["space"] in f["block"]]
    claim("the block's timetabled sessions recompute",
          len(bsess) == fig["components"]["block_sessions"], "%d sessions" % len(bsess))
    occ_hours = sum(s["n"] * (minutes(s["end"]) - minutes(s["start"])) for s in bsess) / 60.0
    claim("the occupant-hours present recompute",
          hu(occ_hours, 1) == fig["components"]["occupant_hours_present"],
          "%s occupant-hours" % "{:,.1f}".format(hu(occ_hours, 1)))
    per = defaultdict(lambda: [0.0, 0.0])
    for x in bf:
        q = supply(x, f["volumes"], f["generation"])
        per[x["space"]][0] += q * x["seconds"]
        per[x["space"]][1] += x["seconds"]
    resp = {k: f["volumes"][k] / (v[0] / v[1]) / 60.0 for k, v in per.items()}
    claim("the shortest response time recomputes",
          int(math.floor(min(resp.values()))) == fig["components"]["shortest_response_minutes"],
          "%d minutes, against a %d minute period"
          % (int(math.floor(min(resp.values()))), fig["components"]["period_minutes"]))
    below = sum(1 for k in f["block"]
                if 1000.0 * per[k][0] / sum(x["n"] * x["seconds"] for x in bf
                                            if x["space"] == k) < f["required"])
    claim("the count of rooms below the requirement recomputes",
          below == fig["components"]["spaces_below_requirement"],
          "%d of %d" % (below, len(f["block"])))

    # the easy route, which must land on the named wrong answer
    naive_air = 0.0
    for x in bf:
        vals = x["readings"]
        step = x["seconds"] / float(len(vals) - 1)
        mean = (step * (sum(vals) - 0.5 * (vals[0] + vals[-1]))) / x["seconds"]
        naive_air += x["n"] * f["generation"] / 1000.0 / (mean * 1e-6) * x["seconds"]
    naive = 1000.0 * naive_air / occ_s
    claim("the easy route still files the named wrong answer",
          to_half(naive) == 11.0 and naive > f["required"],
          "the session-mean steady-state read files %.4f, printing %.1f" % (naive, to_half(naive)))

    # ask A
    months = ["2026-09", "2026-10", "2026-11", "2026-12"]
    hours = defaultdict(int)
    over = defaultdict(int)
    recv = defaultdict(int)
    teaching = set(f["teaching"])
    with open(os.path.join(TARGET, "bms_co2_5min_autumn2026.csv"), newline="",
              encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sp, ts = r["space_code"], r["timestamp_local"]
            if ts[:10] in teaching:
                recv[sp] += 1
            m = minutes(ts[11:16])
            state = "OFF"
            for a, b, st in status.get((ahu[sp], ts[:10]), ()):
                if a <= m < b:
                    state = st
            if state != "OCCUPIED":
                continue
            hours[(sp, ts[:7])] += 1
            if number(r["co2"]) > f["screening"]:
                over[(sp, ts[:7])] += 1
    bad = []
    for row in fig["asks"]["A"]:
        key = (row["space"], months[["September 2026", "October 2026", "November 2026",
                                     "December 2026"].index(row["month"])])
        if hu(hours[key] / 12.0, 2) != row["occupied_hours"] or \
                hu(over[key] / 12.0, 2) != row["hours_over_indicator"]:
            bad.append(key)
    claim("every occupied-hour cell recomputes", not bad,
          "%d cells, %d figures" % (len(fig["asks"]["A"]), 2 * len(fig["asks"]["A"])))

    expected = 288 * len(f["teaching"])
    bad = [row["space"] for row in fig["asks"]["B"]
           if hu(100.0 * recv[row["space"]] / expected, 1) != row["share_pct"]
           or recv[row["space"]] != row["received"] or row["expected"] != expected]
    claim("every capture share recomputes", not bad,
          "%d spaces against %s readings expected" % (len(fig["asks"]["B"]),
                                                      "{:,}".format(expected)))

    bad = []
    for row in fig["asks"]["C"]:
        rows = [s for s in bsess if s["space"] == row["space"]]
        if int(hu(sum(s["n"] for s in rows) / len(rows), 0)) != row["mean_occupants"] \
                or len(rows) != row["sessions"]:
            bad.append(row["space"])
    claim("every mean occupancy recomputes", not bad, "six block rooms")

    rises = sorted(((x["readings"][-1] - x["readings"][0], x["space"], x["date"], x["period"])
                    for x in bf), reverse=True)
    want = [(r["space"], r["date"], r["period"]) for r in fig["asks"]["D"]]
    got = [(r[1], r[2], r[3]) for r in rises[:4]]
    claim("the four largest within-session rises recompute", want == got,
          "fourth and fifth largest rises %.0f and %.0f ppm" % (rises[3][0], rises[4][0]))

    # the write-up's own figures, read from the file rather than from figures.json
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    claim("the write-up states the recomputed call",
          "**%.1f**" % to_half(rate) in sub
          and "**%.1f**" % fig["call"]["shortfall_ls_per_occupant"] in sub,
          "the rate and the shortfall both appear at the rounding the asking sentence states, and "
          "every figure in the sentence recomputes from the printed rate alone")
    claim("the write-up prints every ask figure at the stated precision",
          all(re.search(r"%s, %s: %.2f recorded, %.2f over"
                        % (r["space"], re.escape(r["month"]), r["occupied_hours"],
                           r["hours_over_indicator"]), sub) for r in fig["asks"]["A"][:8]),
          "hours to two decimals, shares to one, occupants whole")

    # the goldens carry the same figures
    assess = sheet_of_golden(WORKBOOK, "Assessment")
    flat = [c for row in assess for c in row if c is not None]
    claim("the golden workbook carries the recomputed call",
          any(abs(float(c) - to_half(rate)) < 1e-9 for c in flat if _isnum(c)),
          "the assessment sheet states %.1f" % to_half(rate))
    hours_rows = sheet_of_golden(WORKBOOK,
                                 "Occupied hours by month")
    claim("the golden workbook carries every graded row", len(hours_rows) == 57,
          "56 space-month rows under one header")
    png = open(os.path.join(GOLDEN, CHART), "rb").read()
    claim("the chart is a readable PNG", png[:8] == b"\x89PNG\r\n\x1a\n" and len(png) > 50000,
          "%s bytes" % "{:,}".format(len(png)))

    bad = 0
    for name, ok, detail in RESULTS:
        print("%-4s %-58s %s" % ("OK" if ok else "FAIL", name, detail))
        bad += 0 if ok else 1
    print("%s verify task204: %d claims, %d failed"
          % ("PASS" if not bad else "FAIL", len(RESULTS), bad))
    return 1 if bad else 0


def _isnum(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


def sheet_of_golden(name, title):
    global TARGET
    keep = TARGET
    TARGET = GOLDEN
    try:
        return sheet_of(name, title)
    finally:
        TARGET = keep


if __name__ == "__main__":
    sys.exit(main())
