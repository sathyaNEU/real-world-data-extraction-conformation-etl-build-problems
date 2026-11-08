"""Independent verifier: reads only target.zip and submission.md, recomputes every graded figure on its own code
path (no generator module is imported), and exits 1 on any disagreement."""
import csv
import datetime as dt
import io
import os
import re
import sys
import zipfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def hm(s):
    """'hh:mm', 'hh:mmH' or 'hh:mm:ss' to minutes after midnight."""
    if s is None or s == "":
        return None
    if isinstance(s, dt.time):
        return s.hour * 60 + s.minute + s.second / 60.0
    if s.endswith("H"):
        h, m = s[:-1].split(":")
        return int(h) * 60 + int(m) + 0.5
    p = s.split(":")
    return int(p[0]) * 60 + int(p[1]) + (int(p[2]) / 60.0 if len(p) > 2 else 0.0)


def load(zp):
    z = zipfile.ZipFile(zp)
    names = z.namelist()

    def rd(name):
        return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8"))))
    pack = {"names": names}
    pack["running"] = rd("train_running_autumn_2026.csv")
    pack["census"] = rd("passenger_census_2026-10-13.csv")
    pack["stations"] = rd("station_register.csv")
    pack["gates"] = rd("gateline_readings_2026-10-12_to_16.csv")
    pack["repay"] = rd("delay_repay_claims_extract_2027-01-15.csv")
    wb = openpyxl.load_workbook(io.BytesIO(z.read("working_timetable_autumn_2026.xlsx")), read_only=True)
    wtt = {}
    rules = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if ws.title == "Planning rules":
            for r in rows:
                if r[0] and isinstance(r[1], str):
                    rules[r[0]] = r[1]
            continue
        for r in rows[1:]:
            hc, o, d, loc, tip, a, dp, al = r
            wtt.setdefault(hc, {"line": ws.title, "calls": []})["calls"].append((tip, hm(a), hm(dp), loc))
    pack["wtt"] = wtt
    pack["rules"] = rules
    pack["brief"] = z.read("dispatch_team_brief_2027.docx")
    return pack


def brief_text(raw):
    z = zipfile.ZipFile(io.BytesIO(raw))
    x = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"<[^>]+>", " ", x)


def network(pack):
    """Per weekday, every train's booked and recorded calls, its unit; the census alighters by headcode and TIPLOC."""
    tip_of = {s["station"]: s["tiploc"] for s in pack["stations"]}
    alight = {}
    for r in pack["census"]:
        alight[(r["headcode"], tip_of[r["station"]])] = int(r["alighters"])
    days = {}
    for r in pack["running"]:
        days.setdefault(r["date"], {}).setdefault(r["headcode"], {"unit": r["unit"], "rec": {}})["rec"][r["tiploc"]] = \
            (hm(r["arr"]), hm(r["dep"]))
    return days, alight, tip_of


def replay_day(pack, trains, alight, team_tip, share, t_from, t_to, min_turn, follow_units=True):
    wtt = pack["wtt"]
    order = sorted(trains, key=lambda hc: trains[hc]["rec"][wtt[hc]["calls"][0][0]][1])
    by_unit = {}
    for hc in order:
        by_unit.setdefault(trains[hc]["unit"], []).append(hc)
    total = 0.0
    for unit, seq in by_unit.items():
        prev_arr = prev_cf = None
        for hc in seq:
            calls = wtt[hc]["calls"]
            rec = trains[hc]["rec"]
            b0 = calls[0][2]
            d0 = rec[calls[0][0]][1]
            dep = d0
            if follow_units and prev_arr is not None and d0 > b0 + 1e-9 and abs(d0 - (prev_arr + min_turn)) < 1e-9:
                dep = max(b0, prev_cf + min_turn)
            last_arr = None
            for i in range(1, len(calls)):
                tip, barr, bdep, loc = calls[i]
                ra, rd_ = rec[tip]
                run = ra - rec[calls[i - 1][0]][1]
                a = dep + run
                last_arr = a
                if a > barr:
                    total += alight.get((hc, tip), 0) * (a - barr)
                if bdep is not None:
                    if rd_ > bdep + 1e-9:
                        over = rd_ - ra - (bdep - barr)
                        if team_tip == tip and t_from <= bdep < t_to and over > 0:
                            over *= (1 - share)
                        dep = max(bdep, a + (bdep - barr) + over)
                    else:
                        dep = bdep
            prev_arr = rec[calls[-1][0]][0]
            prev_cf = last_arr
    return total


def turnround_floor(pack, days):
    """The least time any working that left its origin late left after its unit's previous arrival, from the record."""
    wtt = pack["wtt"]
    gaps = []
    for d, trains in days.items():
        by_unit = {}
        for hc in sorted(trains, key=lambda h: trains[h]["rec"][wtt[h]["calls"][0][0]][1]):
            by_unit.setdefault(trains[hc]["unit"], []).append(hc)
        for seq in by_unit.values():
            for a, b in zip(seq, seq[1:]):
                d0 = trains[b]["rec"][wtt[b]["calls"][0][0]][1]
                if d0 > wtt[b]["calls"][0][2] + 1e-9:
                    gaps.append(round(d0 - trains[a]["rec"][wtt[a]["calls"][-1][0]][0], 4))
    floor = min(gaps)
    assert sum(1 for g in gaps if g == floor) > 100, "no common turnround floor in the record"
    return floor


def savings(pack, follow_units=True):
    txt = brief_text(pack["brief"])
    assert "three fifths" in txt and "06:30 to 19:30" in txt, "brief: valuation sentence not found"
    short = re.search(r"November 2026: (.+?)\.", txt).group(1)
    names = [s.strip() for s in re.split(r",| and ", short) if s.strip()]
    days, alight, tip_of = network(pack)
    min_turn = turnround_floor(pack, days)
    out = {}
    for nm in names:
        tip = tip_of[nm]
        s = 0.0
        for d, trains in days.items():
            base = replay_day(pack, trains, alight, None, 0.6, 390, 1170, min_turn, follow_units)
            team = replay_day(pack, trains, alight, tip, 0.6, 390, 1170, min_turn, follow_units)
            s += base - team
        out[nm] = s / len(days)
    return out, len(days)


def gates(pack):
    by = {}
    for r in pack["gates"]:
        by.setdefault(r["array"], []).append((dt.datetime.strptime(r["reading_utc"], "%Y-%m-%d %H:%M:%S"), r["crs"],
                                              int(r["entries"]), int(r["exits"])))
    crs_name = {s["crs"]: s["station"] for s in pack["stations"]}
    day = dt.date(2026, 10, 13)
    res = {}
    for arr, rows in by.items():
        rows.sort()
        backup = {}
        for t, c, en, ex in rows:
            if t.time() == dt.time(1, 0):
                backup[t.date()] = (en, ex)
        incs = []
        for k in range(1, len(rows)):
            t0, _, e0, x0 = rows[k - 1]
            t1, c, e1, x1 = rows[k]
            if t0.second or t0.minute % 15:      # the reading after a restart's closing reading
                be, bx = backup[t1.date()]
                de, dx = (e1 - be) % 65536, (x1 - bx) % 65536
            else:
                de, dx = (e1 - e0) % 65536, (x1 - x0) % 65536
            incs.append((t1, c, de, dx))
        # tidal hours: runs of four or more daytime quarters with entries moving and exits still
        local = [(t + dt.timedelta(hours=1), c, de, dx) for t, c, de, dx in incs]
        flags = [(6 <= lt.hour < 21) and dx == 0 and de > 0 for lt, c, de, dx in local]
        tidal = [False] * len(local)
        k = 0
        while k < len(local):
            if flags[k]:
                j = k
                while j < len(local) and flags[j]:
                    j += 1
                if j - k >= 4:
                    for q in range(k, j):
                        tidal[q] = True
                k = j
            else:
                k += 1
        for (lt, c, de, dx), td in zip(local, tidal):
            start = lt - dt.timedelta(minutes=15) if lt.second == 0 and lt.minute % 15 == 0 else lt
            if (lt - dt.timedelta(seconds=1)).date() != day:
                continue
            nm = crs_name[c]
            r = res.setdefault(nm, {"entered": 0, "left": 0})
            if td:
                r["left"] += de + dx
            else:
                r["entered"] += de
                r["left"] += dx
    return res


def repay(pack, reverse=True, redate=True, every_row=True):
    """Approved Delay Repay payments for weekday journeys to or from RVC in the window, by line and by the band of
    the train's lateness at the passenger's destination in the running record. Each claim is matched to the train
    leaving its stated origin at the stated time and calling at its stated destination, or, failing that, the other
    way round (a return ticket's claim names the ticket's stations). A claim dated the day it was first submitted
    whose train did not reach the destination 15 minutes late that day is dated by the last earlier weekday its train
    did; its appeal rows follow it."""
    wtt = pack["wtt"]
    crs_tip = {s["crs"]: s["tiploc"] for s in pack["stations"]}
    crs_line = {s["crs"]: s["lines"] for s in pack["stations"]}
    days, alight, tip_of = network(pack)
    dep_index = {}
    for hc, t in wtt.items():
        for k, (tip, a, d, loc) in enumerate(t["calls"]):
            if d is not None:
                dep_index.setdefault((tip, "%02d:%02d" % (int(d) // 60, int(d) % 60)), []).append((hc, k))
    out = {}
    lo, hi = dt.date(2026, 9, 7), dt.date(2026, 11, 27)
    rows = [r for r in pack["repay"] if r["decision"] == "APPROVED" and "RVC" in (r["origin_crs"], r["destination_crs"])]
    first_sub = {}
    for r in rows:
        first_sub[r["claim_ref"]] = min(first_sub.get(r["claim_ref"], r["submitted"]), r["submitted"])
    if not every_row:
        last = {}
        for r in rows:
            last[r["claim_ref"]] = r
        rows = list(last.values())
    for r in rows:
        jd = dt.date.fromisoformat(r["journey_date"])
        o, d = crs_tip[r["origin_crs"]], crs_tip[r["destination_crs"]]
        hit = None
        for frm, to in ((o, d), (d, o)) if reverse else ((o, d),):
            for hc, k in dep_index.get((frm, r["booked_departure"]), []):
                tips = [c[0] for c in wtt[hc]["calls"]]
                if to in tips[k + 1:]:
                    hit = (hc, to, wtt[hc]["calls"][tips.index(to)][1])
                    break
            if hit is not None:
                break
        if hit is None:
            continue
        hc, to, barr = hit

        def late_on(day):
            rec = days.get(day.isoformat())
            return None if rec is None else rec[hc]["rec"][to][0] - barr
        lt = late_on(jd)
        if redate and first_sub[r["claim_ref"]][:10] == r["journey_date"] and (lt is None or lt < 15):
            earlier = [dt.date.fromisoformat(x) for x in days if dt.date.fromisoformat(x) < jd
                       and late_on(dt.date.fromisoformat(x)) >= 15]
            if earlier:
                jd = max(earlier)
                lt = late_on(jd)
        if not (lo <= jd <= hi) or jd.weekday() > 4 or lt is None or lt < 15:
            continue
        band = "15 to 29" if lt < 30 else ("30 to 59" if lt < 60 else "60 or more")
        other = r["destination_crs"] if r["origin_crs"] == "RVC" else r["origin_crs"]
        line = crs_line[other]
        out[(line, band)] = out.get((line, band), 0.0) + float(r["amount_gbp"])
    return out


def block4(path):
    txt = open(path).read()
    b4 = txt.split("## 4. Deliverable Answers", 1)[1]
    return b4


def main(zp=None):
    zp = zp or os.path.join(TASK, "target.zip")
    pack = load(zp)
    bad = 0
    sv, ndays = savings(pack)
    b4 = block4(os.path.join(TASK, "submission.md"))
    for nm, v in sv.items():
        want = int(round(v / 100.0) * 100)
        m = re.search(r"- %s: ([\d,]+)" % re.escape(nm), b4)
        ok = m and int(m.group(1).replace(",", "")) == want
        print("%s  saving %-15s %8.1f -> %d" % ("PASS" if ok else "FAIL", nm, v, want))
        bad += not ok
    order = sorted(sv, key=lambda c: -sv[c])
    gap = int(round((sv[order[0]] - sv[order[1]]) / 100.0) * 100)
    m = re.search(r"Pick (.+?) \(([\d,]+)\); runner-up (.+?) \(([\d,]+)\); gap ([\d,]+)", b4)
    ok = m and m.group(1) == order[0] and m.group(3) == order[1] and int(m.group(5).replace(",", "")) == gap
    print("%s  pick %s, runner-up %s, gap %d" % ("PASS" if ok else "FAIL", order[0], order[1], gap))
    bad += not ok
    same, _ = savings(pack, follow_units=False)
    so = sorted(same, key=lambda c: -same[c])
    ok = so[0] != order[0]
    print("%s  the same-train route files %s, not the pick" % ("PASS" if ok else "FAIL", so[0]))
    bad += not ok
    g = gates(pack)
    for nm, v in g.items():
        m = re.search(r"- %s: entered ([\d,]+); left ([\d,]+)" % re.escape(nm), b4)
        ok = m and int(m.group(1).replace(",", "")) == v["entered"] and int(m.group(2).replace(",", "")) == v["left"]
        print("%s  gates %-15s entered %d left %d" % ("PASS" if ok else "FAIL", nm, v["entered"], v["left"]))
        bad += not ok
    rp = repay(pack)
    names = {"Crossmoor": "Crossmoor line", "Ambrey": "Ambrey line", "Holm Ferry": "Holm Ferry line"}
    for (ln, band), v in sorted(rp.items()):
        lname = names[ln]
        m = re.search(r"- %s: 15 to 29 minutes £([\d,]+); 30 to 59 minutes £([\d,]+); 60 minutes or more £([\d,]+)"
                      % re.escape(lname), b4)
        idx = {"15 to 29": 1, "30 to 59": 2, "60 or more": 3}[band]
        ok = m and int(m.group(idx).replace(",", "")) == int(round(v))
        print("%s  repay %-16s %-10s %.2f" % ("PASS" if ok else "FAIL", lname, band, v))
        bad += not ok
    print("verify:", "PASS" if not bad else "FAIL %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
