"""The independent verifier: reads only target.zip, on its own code path (nothing imported from the generator), and
recomputes every graded figure: the five networks' net fare revenue and the pick, the people by home area, the pilot's
charging energy by month and the workshop jobs per 10,000 rides; it reads back every format the pack ships (CSV, XLSX,
JSON, PDF) with a positive control on each document that carries a filed sentence the call leans on."""
import io
import json
import math
import os
import re
import sys
import zipfile
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

TZ = ZoneInfo("America/Chicago")
HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def check(label, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + label + (("  " + detail) if detail else ""))
    if not cond:
        FAIL.append(label)


def secs_utc(series):
    t = pd.to_datetime(series, utc=True)
    return ((t - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds()).round().astype("int64")


def secs_local(series):
    t = pd.to_datetime(series).dt.tz_localize(TZ, ambiguous="NaT", nonexistent="shift_forward")
    # the repeated November hour: take the first pass, as the trip system does
    bad = t.isna()
    if bad.any():
        t2 = pd.to_datetime(series[bad]).dt.tz_localize(TZ, ambiguous=np.ones(int(bad.sum()), bool))
        t[bad] = t2
    return ((t - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds()).round().astype("int64")


def pdf_text(raw):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(io.BytesIO(raw)).pages))


def main(zp):
    del FAIL[:]
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    rd = lambda n, **k: pd.read_csv(io.BytesIO(z.read(n)), **k)
    # ---------------------------------------------------------------- every format back
    stations = json.loads(z.read("station_information.json"))["data"]["stations"]
    regions = {r["region_id"]: r["name"] for r in json.loads(z.read("system_regions.json"))["data"]["regions"]}
    check("json: station feed and regions", len(stations) == 115 and len(regions) == 6)
    board = pdf_text(z.read("board_paper_2026-12_item7_extract.pdf"))
    pilot_txt = pdf_text(z.read("ebike_pilot_harbour_2025.pdf"))
    fares = pdf_text(z.read("fare_schedule_2025.pdf"))
    quote = pdf_text(z.read("vendor_quote_ebikes_2026.pdf"))
    check("pdf: positive control (the vendor's quotation number reads back)", "HVS-Q-26-0418" in quote)
    check("pdf: the board paper files the measure", "the fares riders would pay in that network in a year with the "
          "e-bikes, less the fares they paid in that network in 2025, at 2025 demand" in board)
    check("pdf: the board paper files the deployment", "so that every station holds e-bikes through the day" in board)
    check("pdf: the fare schedule files the fares", "USD 0.12" in fares and "USD 0.17" in fares and "within 60 seconds is not charged" in fares)
    audit = pd.read_excel(io.BytesIO(z.read("audit_0300_2025.xlsx")), dtype={"station_id": str})
    dic = pd.read_excel(io.BytesIO(z.read("data_dictionary.xlsx")), sheet_name=None)
    check("xlsx: the audit and the dictionary", len(audit) == 115 * 365 and "Read me" in dic)
    readme = " ".join(str(v) for v in dic["Read me"].fillna("").values.ravel())
    check("xlsx: the dictionary files the reporting calendar and the false start",
          "quarters run on Central Time" in readme and "is not a ride" in readme)
    # ---------------------------------------------------------------- trips on one footing
    st = pd.DataFrame(stations)
    st["network"] = st.region_id.map(regions)
    name2id = dict(zip(st.name, st.station_id)); code2id = dict(zip(st.short_name, st.station_id))
    rows = []
    for n in ("tripsys_export_2025Q1.csv", "tripsys_export_2025Q2.csv"):
        d = rd(n, dtype={"account_no": str})
        rows.append(pd.DataFrame({"start": secs_local(d.start_time), "dur": d.duration_sec, "a": d.start_station.map(name2id),
                                  "b": d.end_station.map(name2id), "e": d.bike_type == "electric", "fare": d.fare_usd,
                                  "acct": "L" + d.account_no, "bike": d.bike_no.str.replace(r"\D", "", regex=True).astype(int)
                                  + np.where(d.bike_type == "electric", 500000, 100000)}))
    for n in ("rides_2025Q3.csv", "rides_2025Q4.csv"):
        d = rd(n, dtype={"account_id": str})
        rows.append(pd.DataFrame({"start": secs_local(d.started_at), "dur": d.duration_s, "a": d.start_station_code.map(code2id),
                                  "b": d.end_station_code.map(code2id), "e": d.vehicle_type == "EBIKE",
                                  "fare": d.fare_cents / 100.0, "acct": d.account_id, "bike": d.vehicle_id}))
    T = pd.concat(rows, ignore_index=True)
    T["end"] = T.start + T.dur
    T["fs"] = (T.dur < 60) & (T.a == T.b)
    check("trips: every station resolves", T.a.notna().all() and T.b.notna().all())
    mv = rd("dispatch_moves_2025.csv", dtype={"from_station": str, "to_station": str})
    mv = mv[mv.bike_class == "classic"].copy()
    mv["t"] = secs_utc(mv.completed_utc)
    audit["t"] = secs_local(pd.Series([str(pd.Timestamp(d).date()) + " 03:00:00" for d in audit.audit_date]))
    # ---------------------------------------------------------------- each station's classic stock, event by event
    T0 = int(secs_local(pd.Series(["2025-01-01 00:00:00"]))[0]); T1 = int(secs_local(pd.Series(["2026-01-01 00:00:00"]))[0])
    nh = (T1 - T0) // 3600
    hrs = pd.to_datetime(np.arange(T0, T1, 3600), unit="s", utc=True).tz_convert(TZ)
    cell = (hrs.month.values - 1) * 48 + (hrs.weekday.values >= 5) * 24 + hrs.hour.values
    cls = T[~T.e]
    turned = {}
    for sid in st.station_id:
        ev = []
        for t in cls.start[cls.a == sid].values:
            ev.append((t, 0, -1))
        for t in cls.end[cls.b == sid].values:
            ev.append((t, 1, 1))
        for t, q in mv.loc[mv.from_station == sid, ["t", "qty"]].values:
            ev.append((t, 1, -q))
        for t, q in mv.loc[mv.to_station == sid, ["t", "qty"]].values:
            ev.append((t, 1, q))
        ev.sort()
        anchors = audit[audit.station_id == sid].sort_values("t")[["t", "classic_docked"]].values
        stocked = np.zeros(nh); empty = np.zeros(nh)
        j = 0
        for k, (a0, c0) in enumerate(anchors):
            a1 = anchors[k + 1][0] if k + 1 < len(anchors) else T1
            while j < len(ev) and ev[j][0] <= a0:
                j += 1
            cur, tprev = c0, a0
            while True:
                tn = ev[j][0] if j < len(ev) and ev[j][0] <= a1 else a1
                # split [tprev, tn) at hour boundaries
                x = tprev
                while x < tn:
                    h = (x - T0) // 3600
                    y = min(tn, T0 + (h + 1) * 3600)
                    if cur > 0:
                        stocked[h] += y - x
                    else:
                        empty[h] += y - x
                    x = y
                if tn >= a1 and not (j < len(ev) and ev[j][0] <= a1):
                    break
                cur += ev[j][2]; tprev = tn; j += 1
                assert cur >= 0, (sid, tn)
        reqs = cls[(cls.a == sid) & (~cls.fs) & (cls.start >= anchors[0][0])]
        dep = np.bincount(((reqs.start.values - T0) // 3600).astype(int), minlength=nh)[:nh]
        s_c = np.bincount(cell, weights=stocked, minlength=576); d_c = np.bincount(cell, weights=dep, minlength=576)
        rate = np.where(s_c > 0, d_c / np.maximum(s_c, 1e-9), 0.0)
        turned[sid] = float((rate[cell] * empty).sum())
    # ---------------------------------------------------------------- the pilot and the networks
    lines = [l for l in re.split(r"(?=HBR-\d\d )", pilot_txt)]
    pil = re.findall(r"(HBR-\d\d) [^|]*?(?= pilot station)", pilot_txt)
    grp = dict(re.findall(r"(HBR-\d\d) .*? (pilot station|comparison station)", pilot_txt))
    pil = [code2id[c] for c, g in grp.items() if g == "pilot station"]
    cmpn = [code2id[c] for c, g in grp.items() if g == "comparison station"]
    check("pdf: 24 pilot and 12 comparison stations read from the pilot note", len(pil) == 24 and len(cmpn) == 12)
    real = T[~T.fs]
    p_r = real[real.a.isin(pil)]; c_r = real[real.a.isin(cmpn)]
    share = p_r.e.mean(); upl = (len(p_r) / 24) / (len(c_r) / 12) - 1
    prem = p_r[p_r.e].fare.mean() - p_r[~p_r.e].fare.mean()
    netrev = {}
    for n in ["Central", "University", "Riverside", "Old Town", "Hillcrest"]:
        ids = set(st.station_id[st.network == n])
        rides = real[(~real.e) & real.a.isin(ids)]
        U = sum(turned[s] for s in ids); D = len(rides) + U
        netrev[n] = (U + upl * D) * rides.fare.mean() + share * D * (1 + upl) * prem
        r25 = int(25000 * math.floor(netrev[n] / 25000 + 0.5))
        check("call: %s net fare revenue %s" % (n, "{:,}".format(r25)), r25 == fig["net_revenue"][n], "%.0f" % netrev[n])
    check("call: the pick", max(netrev, key=netrev.get) == fig["recommended_network"])
    # ---------------------------------------------------------------- people by home area
    acc = rd("account_register_2025-12-31.csv", dtype=str)
    acc["home"] = acc.home_area.str.strip().str.title()
    m = dict(zip("L" + acc.legacy_account_no.fillna("-"), acc.account_id))
    real_acct = real.acct.map(lambda x: m.get(x, x))
    last = real.assign(aid=real_acct).groupby("aid").end.max()
    a = acc[acc.account_id.isin(last.index)].copy()
    a["opened"] = secs_local(a.created_at); a["last"] = a.account_id.map(last)
    people = {}
    for card, g in a.sort_values("opened").groupby("card_fingerprint"):
        chains = []
        for r in g.itertuples():
            for ch in chains:
                if ch[0] < r.opened:
                    ch[0] = max(ch[0], r.last); ch[1] = r.home
                    break
            else:
                chains.append([r.last, r.home])
        for ch in chains:
            people[ch[1]] = people.get(ch[1], 0) + 1
    for n in fig["people"]:
        check("people: %s %d" % (n, fig["people"][n]), people.get(n.title() if n != "Old Town" else "Old Town") == fig["people"][n])
    # ---------------------------------------------------------------- charging energy by month
    ch = rd("charging_sessions_harbour_2025.csv").sort_values("session_id")
    first = ~ch.duplicated(["station_code", "point", "meter_start_wh", "meter_stop_wh"])
    ch = ch[first | (ch.meter_start_wh == ch.meter_stop_wh)]
    mon = pd.to_datetime(ch.plug_out_utc, utc=True).dt.tz_convert(TZ).dt.month
    for i, mname in enumerate(fig["energy_kwh"], 1):
        pass
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    for i, mname in enumerate(months, 1):
        v = int(round(ch.energy_kwh[mon == i].sum()))
        check("energy: %s %d kWh" % (mname, v), v == fig["energy_kwh"][mname])
    # ---------------------------------------------------------------- workshop jobs per 10,000 rides
    jb = rd("workshop_jobs_2025.csv")
    jb["o"] = secs_utc(jb.opened_utc); jb["c"] = secs_utc(jb.closed_utc)
    jb["q"] = (pd.to_datetime(jb.opened_utc, utc=True).dt.tz_convert(TZ).dt.month - 1) // 3 + 1
    jb["tag"] = jb.asset_tag.str[2:].astype(int) + np.where(jb.asset_class == "E-bike", 500000, 100000)
    times = {b: np.sort(g.start.values) for b, g in real.groupby("bike")}
    keep, prev = [], {}
    for r in jb.sort_values(["o", "job_no"]).itertuples():
        p = prev.get(r.tag)
        if p is not None:
            ts = times.get(r.tag, np.array([]))
            if ((ts > p) & (ts < r.o)).sum() == 0:
                prev[r.tag] = r.c
                continue
        keep.append(r.Index); prev[r.tag] = r.c
    jk = jb.loc[keep]
    rq = (pd.to_datetime(real.start, unit="s", utc=True).dt.tz_convert(TZ).dt.month - 1) // 3 + 1
    for cls_name, is_e in (("E-bike", True), ("Classic", False)):
        for q in range(1, 5):
            v = round(1e4 * ((jk.asset_class == cls_name) & (jk.q == q)).sum() / ((real.e == is_e) & (rq == q)).sum(), 1)
            check("workshop: %s Q%d %.1f" % (cls_name, q, v), v == fig["workshop_per_10000"]["%s Q%d" % (cls_name, q)])
    print("%d failure(s)" % len(FAIL))
    return len(FAIL)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target.zip")) else 0)
