"""Independent verifier: recomputes every graded figure from target/ with its own code (csv and openpyxl, no generator
module) and compares with figures.json at the stated rounding. Exit 1 on any mismatch."""
import csv, json, math, os, sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import openpyxl
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
CT = ZoneInfo("America/Chicago")
D0 = datetime(2020, 10, 1)
FY0, FY1, REV = datetime(2025, 10, 1), datetime(2026, 10, 1), datetime(2025, 12, 1)


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sheet(name, sh):
    ws = openpyxl.load_workbook(os.path.join(T, name), read_only=True)[sh]
    it = ws.iter_rows(values_only=True)
    h = next(it)
    return [dict(zip(h, r)) for r in it]


def local_from_utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(CT).replace(tzinfo=None)


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    # ---- major event days: 2.5 beta on fiscal 2021 to 2025 daily SAIDI (minutes)
    daily = {}
    for r in sheet("daily_reliability_fy2021-fy2026.xlsx", "Legacy OMS to Feb 2023"):
        daily[datetime.strptime(r["Date"], "%m/%d/%Y").date()] = r["SAIDI Hrs"] * 60
    for r in sheet("daily_reliability_fy2021-fy2026.xlsx", "OMS daily"):
        d = r["date"].date() if hasattr(r["date"], "date") else r["date"]
        daily[d] = r["saidi_min"]
    hist = [math.log(v) for d, v in daily.items() if d < FY0.date() and v > 0]
    mu = sum(hist) / len(hist); sd = math.sqrt(sum((x - mu) ** 2 for x in hist) / (len(hist) - 1))
    tmed = math.exp(mu + 2.5 * sd)
    med = {d for d, v in daily.items() if v > tmed}
    # ---- the outage records
    cw = {r["old_section_id"]: r["section_id"] for r in sheet("system_register_2026-09-30.xlsx", "gis_crosswalk")}
    ev = []
    for r in rows("outage_events_fy2022-fy2026.csv"):
        s, e = datetime.fromisoformat(r["start_local"]), datetime.fromisoformat(r["end_local"])
        ev.append(dict(sec=cw.get(r["section_id"], r["section_id"]), s=s, e=e, ci=int(r["customers_interrupted"]),
                       cause=r["cause_code"], planned=r["planned"] == "Y", xf=r["transformer_id"], st=r["structure_id"],
                       sect=r["device_type"] != "XFMR", feeder=r["feeder"], dev=r["device_id"], wo=r["work_order"]))
    un = [x for x in ev if not x["planned"]]
    inyr = lambda x, frm=FY0: frm <= x["s"] < FY1 and x["s"].date() not in med
    # ---- the switching revision: each overload record of a section device against the end of the same section's
    # previous record, where that record lasted an hour or more
    bysec = {}
    for x in un:
        if x["sect"]:
            bysec.setdefault(x["sec"], []).append(x)
    G = 0; staged_pairs = 0
    for s, L in bysec.items():
        L.sort(key=lambda x: x["s"])
        for a, b in zip(L, L[1:]):
            gap = (b["s"] - a["e"]).total_seconds() / 60
            if 0 <= gap <= 10 and (a["e"] - a["s"]).total_seconds() >= 3600:
                if REV <= b["s"] < FY1 and b["s"].date() not in med and b["cause"] == "OVLD":
                    G += b["ci"]
                if datetime(2024, 10, 1) <= b["s"] < REV:
                    staged_pairs += 1
    # ---- the rivals' replays
    reb = sheet("heat_pump_rebates_fy2024-fy2026.xlsx", "rebates")
    conn = {}
    for r in reb:
        if r["load_study"] == "waived":
            x = "T" + r["service_transformer"][2:]
            d = r["connected"] if isinstance(r["connected"], datetime) else datetime.fromisoformat(str(r["connected"]))
            conn[x] = min(conn.get(x, d), d)
    Rv = sum(x["ci"] for x in un if inyr(x) and not x["sect"] and x["cause"] == "OVLD" and x["xf"] in conn and x["s"] >= conn[x["xf"]])
    al = openpyxl.load_workbook(os.path.join(T, "asset_programme_lists_2022-2026.xlsx"), read_only=True)
    g26 = {r[1] for r in al["animal_guards"].iter_rows(min_row=2, values_only=True) if r[0] == 2026}
    r25 = {r[1] for r in al["riser_replacements"].iter_rows(min_row=2, values_only=True) if r[0] == 2025}
    E = sum(x["ci"] for x in un if inyr(x, datetime(2026, 1, 1)) and x["cause"] == "ANML" and x["st"] in g26)
    D = sum(x["ci"] for x in un if inyr(x) and x["cause"] == "UGTERM" and x["st"] in r25)
    units = pq.read_table(os.path.join(T, "transformer_units.parquet")).to_pylist()
    fit = {}
    for u in units:
        f = datetime.combine(u["fitted"], datetime.min.time())
        if u["supplier"] == "Brekke Power Products" and f >= datetime(2026, 2, 1):
            fit[u["transformer_id"]] = min(fit.get(u["transformer_id"], f), f)
    Fv = sum(x["ci"] for x in un if inyr(x, datetime(2026, 2, 1)) and not x["sect"] and x["cause"] == "XFMR" and x["xf"] in fit and x["s"] >= fit[x["xf"]])
    mine = {"Restoration switching template SO-7 revision": G, "Heat pump connections without a load study": Rv,
            "Animal guard programme ended": E, "Riser termination replacements suspended": D, "Transformer supplier change": Fv}
    for k, v in mine.items():
        if round(v / 100) * 100 != figs["costs"][k]:
            bad.append("cost %s %s against %s" % (k, v, figs["costs"][k]))
    srt = sorted(mine.items(), key=lambda kv: -kv[1])
    if srt[0][0] != figs["call"] or srt[1][0] != figs["runner_up"] or round((srt[0][1] - srt[1][1]) / 100) * 100 != figs["gap"]:
        bad.append("call, runner-up or gap")
    # ---- Ask A: one event per member per five minutes across every device upstream at the time
    reg = sheet("system_register_2026-09-30.xlsx", "sections")
    mem = {r["section_id"]: r["members"] for r in reg}; dist = {r["section_id"]: r["district"] for r in reg}
    cur = {r["section_id"]: r["feeder"] for r in reg}
    moved = {x["sec"]: [x["feeder"], x["e"]] for x in ev if x["cause"] == "XFER"}
    rec = {r["device_id"]: r["section_id"] for r in sheet("system_register_2026-09-30.xlsx", "reclosing_devices") if r["type"] == "LINE RECLOSER"}
    ops = {}
    for r in rows("scada_reclosing_operations_fy2026.csv"):
        ops.setdefault(r["device_id"], []).append((local_from_utc(r["time_utc"]), r["operation"]))
    seqs = []
    for dv, L in ops.items():
        L.sort()
        cur_seq = []
        for t, o in L:
            if cur_seq and (t - cur_seq[0][0]).total_seconds() > 300:
                seqs.append((dv, cur_seq)); cur_seq = []
            cur_seq.append((t, o))
        if cur_seq:
            seqs.append((dv, cur_seq))
    hits = {}
    feeders = {}
    for s, f in cur.items():
        feeders.setdefault(f, []).append(s)
    for dv, sq in seqs:
        if not any(o == "TRIP" for _, o in sq) or sq[-1][1] == "TRIP":
            continue          # a lone close, or a sequence that ended in lockout
        t0 = sq[0][0]
        if dv.startswith("CB-"):
            f = dv[3:]
            secs = [s for s in cur if (moved[s][0] if (s in moved and t0 < moved[s][1]) else cur[s]) == f]
        else:
            secs = [rec[dv]]
        for s in secs:
            hits.setdefault(s, []).append(t0)
    tot = {}
    for s, ts in hits.items():
        st = None
        for t in sorted(ts):
            if st is None or (t - st).total_seconds() > 300:
                st = t
                q = {10: 1, 11: 1, 12: 1, 1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3}.get(t.month, 4)
                tot[(dist[s], q)] = tot.get((dist[s], q), 0) + mem[s]
    dm = {}
    for s in mem:
        dm[dist[s]] = dm.get(dist[s], 0) + mem[s]
    for (d, q), v in tot.items():
        if round(v / dm[d], 2) != figs["maifi"]["%s|Q%d" % (d, q)]:
            bad.append("MAIFIe %s Q%d %.4f against %s" % (d, q, v / dm[d], figs["maifi"]["%s|Q%d" % (d, q)]))
    # ---- Ask B: chained restoration callouts, latest correction, rejected entries out
    rate = {"Line Foreman": 61.42, "Journeyman Lineworker": 55.87, "Apprentice Lineworker (6th step)": 50.28,
            "Apprentice Lineworker (4th step)": 44.69, "Equipment Operator": 46.15}
    hol = {datetime(2025, 11, 27).date(), datetime(2025, 11, 28).date(), datetime(2025, 12, 24).date(), datetime(2025, 12, 25).date(),
           datetime(2026, 1, 1).date(), datetime(2026, 2, 16).date(), datetime(2026, 5, 25).date(), datetime(2026, 7, 3).date(),
           datetime(2026, 9, 7).date()}
    latest = {}
    for r in rows("crew_time_overtime_fy2026.csv"):
        if r["status"] != "APPROVED" or r["pay_code"] != "CALLOUT":
            continue
        k = (r["employee_id"], r["work_order"], r["start_time"])
        if k not in latest or r["entered_at"] > latest[k]["entered_at"]:
            latest[k] = r
    ostart = {x["wo"]: x["s"] for x in ev}
    byemp = {}
    for r in latest.values():
        if r["order_type"] == "OUTAGE":
            o = ostart[r["work_order"]]
            hh, mm = int(r["start_time"][:2]), int(r["start_time"][3:])
            s = datetime.combine(o.date(), datetime.min.time()) + timedelta(hours=hh, minutes=mm)
            if s < o:
                s += timedelta(days=1)
            h2, m2 = int(r["end_time"][:2]), int(r["end_time"][3:])
            dur = ((h2 * 60 + m2) - (hh * 60 + mm)) % 1440
            byemp.setdefault(r["employee_id"], []).append((s, s + timedelta(minutes=dur), r["order_type"], rate[r["job_class"]]))
    H, Pp = {}, {}
    for emp, L in byemp.items():
        L.sort()
        chains, c = [], []
        for x in L:
            if c and (x[0] - max(y[1] for y in c)).total_seconds() / 60 >= 15:
                chains.append(c); c = []
            c.append(x)
        chains.append(c)
        for c in chains:
            if not any(y[2] == "OUTAGE" for y in c):
                continue
            s, e, rt = c[0][0], max(y[1] for y in c), c[0][3]
            mkey = s.strftime("%b %Y")
            hrs = (e - s).total_seconds() / 3600
            H[mkey] = H.get(mkey, 0) + hrs
            if hrs < 2:
                Pp[mkey] = Pp.get(mkey, 0) + 2 * rt * 1.5
            else:
                t = s
                while t < e:
                    nxt = min(e, datetime.combine(t.date() + timedelta(days=1), datetime.min.time()))
                    Pp[mkey] = Pp.get(mkey, 0) + (nxt - t).total_seconds() / 3600 * rt * (2.0 if t.date() in hol else 1.5)
                    t = nxt
    for k, v in figs["callout_hours"].items():
        if round(H.get(k, 0)) != v:
            bad.append("hours %s %.2f against %d" % (k, H.get(k, 0), v))
    for k, v in figs["callout_pay"].items():
        if round(Pp.get(k, 0)) != v:
            bad.append("pay %s %.2f against %d" % (k, Pp.get(k, 0), v))
    n = 5 + 3 + 16 + 24
    print("verify: %d graded figures recomputed independently, %d mismatches; staged-era re-trips %d; T_MED %.2f" % (n, len(bad), staged_pairs, tmed))
    for b in bad:
        print("  MISMATCH", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
