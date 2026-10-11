"""Independent verifier: reads only target/ and golden/, shares no code with golden.py, and recomputes
every graded figure with the standard library (csv, json, datetime) and openpyxl."""
import csv
import datetime as dt
import json
import math
import os
import sys

import openpyxl

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTC = dt.timezone.utc


def t_utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def local(s):
    t = dt.datetime.strptime(s, "%d/%m/%Y %H:%M")
    y = t.year
    fs = lambda m: dt.date(y, m, 1) + dt.timedelta(days=(6 - dt.date(y, m, 1).weekday()) % 7)
    off = 11 if (t.date() >= fs(10) or t.date() < fs(4)) else 10
    return t.replace(tzinfo=dt.timezone(dt.timedelta(hours=off)))


def main(target, golden):
    ws_ = dt.datetime(2026, 10, 4, 14, 0, tzinfo=UTC)          # Monday 5 October 00:00 AEST
    we_ = ws_ + dt.timedelta(days=7)
    # images to releases
    img = {}
    with open(os.path.join(target, "fw_release_catalogue.csv")) as fh:
        for r in csv.DictReader(fh):
            img[r["hes_image"]] = r["release"]
    # head-end: build spells per meter, first copy of each event id only
    hes = json.load(open(os.path.join(target, "hes_meter_firmware_history.json")))
    spells, w7 = {}, {}
    for m in hes["meters"]:
        s = m["meter_id"][4:]
        seen, sp = set(), []
        for e in sorted(m["events"], key=lambda e: (e["ts_utc"], e["seq"])):
            if e["event_id"] in seen:
                continue
            seen.add(e["event_id"])
            if e["type"] in ("COMMISSIONED", "FW_ACTIVATED"):
                sp.append((t_utc(e["ts_utc"]), img[e["image"]]))
            if e["type"] == "FW_ACTIVATED" and (e["job"] or "").startswith("WAVE7"):
                w7[s] = (img[e["image"]], (t_utc(e["ts_utc"]) + dt.timedelta(hours=10)).strftime("%Y%m%d"))
        spells[s] = sp

    def at(s, t):
        b = None
        for (u, rel) in spells.get(s, []):
            if u <= t:
                b = rel
        return b
    # register: meter assignments
    wb = openpyxl.load_workbook(os.path.join(target, "mp_installation_register_20261012.xlsx"), read_only=True)
    assign = {}
    for row in list(wb["Meters"].iter_rows(values_only=True))[3:]:
        nmi = str(row[0])[:10]
        assign.setdefault(nmi, []).append((str(row[1]).zfill(8), local(row[4]), local(row[5]) if row[5] else None))
    pop = {}
    for nmi, ms in assign.items():
        live = [m for m in ms if m[1] < we_ and (m[2] is None or m[2] > ws_)]
        if len(live) != 1:
            continue
        s, a, b = live[0]
        if a > ws_ or (b is not None and b < we_):
            continue
        if any(ws_ < u < we_ for u, _ in spells.get(s, [])):
            continue
        pop[nmi] = at(s, ws_)
    # MDM: per data stream and day, the latest delivery received before 20:00 UTC on the read date
    best = {}
    with open(os.path.join(target, "mdm_interval_receipts_20261005_20261011.csv")) as fh:
        for r in csv.DictReader(fh):
            rd = r["READ_DATE"]
            cut = dt.datetime(int(rd[:4]), int(rd[4:6]), int(rd[6:]), 20, 0, tzinfo=UTC)
            t = t_utc(r["RECEIVED_UTC"])
            if t >= cut:
                continue
            k = (r["NMI"], r["NMI_SUFFIX"], rd)
            if k not in best or t > best[k][0]:
                exp = int(r["QTY_A"]) + int(r["QTY_S"]) + int(r["QTY_F"])
                best[k] = (t, int(r["QTY_A"]), exp)
    held, expd, day_miss = {}, {}, {}
    for (nmi, sx, rd), (_, a, e) in best.items():
        held[nmi] = held.get(nmi, 0) + a
        expd[nmi] = expd.get(nmi, 0) + e
        day_miss[(nmi, rd)] = day_miss.get((nmi, rd), 0) + (e - a)
    shares = {}
    for nmi, rel in pop.items():
        shares.setdefault(rel, []).append(100.0 * held[nmi] / expd[nmi])
    score = {}
    for rel, xs in shares.items():
        n = len(xs)
        mu = sum(xs) / n
        sd = math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1))
        lcl = 99.50 - 3 * sd / math.sqrt(n)
        score[rel] = (n, mu, lcl, mu < lcl)
    # wave 8
    wb8 = openpyxl.load_workbook(os.path.join(target, "wave8_schedule.xlsx"), read_only=True)
    in_service = {}
    for nmi, ms in assign.items():
        for s, a, b in ms:
            if b is None:
                in_service[s] = nmi
    end = dt.datetime(2026, 10, 12, 4, 0, tzinfo=UTC)
    w8 = {}
    for sh in ("Batch A 13-10", "Batch B 14-10"):
        for row in list(wb8[sh].iter_rows(values_only=True))[2:]:
            if row[1] is None:
                continue
            s = str(row[1]).zfill(8)
            if s in in_service and at(s, end) != row[5]:
                w8.setdefault(row[5], set()).add(in_service[s])
    # wave 7
    serial2nmi = {s: nmi for nmi, ms in assign.items() for s, _, _ in ms}
    w7c = {}
    for s, (rel, day) in w7.items():
        c = w7c.setdefault(rel, [set(), 0])
        c[0].add(serial2nmi[s])
        c[1] += day_miss.get((serial2nmi[s], day), 0)
    # compare with the golden payload
    gj = json.load(open(os.path.join(golden, "wave8_read_health_alerts.json")))
    bad = []
    fire = sorted(r for r, v in score.items() if v[3])
    if sorted(gj["fire"]) != fire:
        bad.append(("fire", gj["fire"], fire))
    order = sorted(score, key=lambda r: score[r][1] - score[r][2])
    if [b["release"] for b in gj["builds"]] != order:
        bad.append(("order", order))
    for b in gj["builds"]:
        n, mu, lcl, f = score[b["release"]]
        if (b["assessed_installations"], b["read_health_pct"], b["lower_limit_pct"], b["alert"]) != (n, round(mu, 2), round(lcl, 2), "FIRE" if f else "HOLD"):
            bad.append((b, (n, mu, lcl, f)))
    if gj["wave8_schedule_moves_if_it_goes_ahead"] != {k: len(v) for k, v in w8.items()}:
        bad.append(("wave8", {k: len(v) for k, v in w8.items()}))
    for x in gj["wave7_moves_this_week"]:
        c = w7c[x["onto"]]
        if (x["installations_moved"], x["interval_reads_missing_at_cutoff_on_move_day"]) != (len(c[0]), c[1]):
            bad.append(("wave7", x, c[1]))
    if bad:
        print("VERIFY FAILED", bad)
        sys.exit(1)
    print("verify: every graded figure recomputes from target/ (%d builds, wave 8, wave 7)" % len(score))


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
