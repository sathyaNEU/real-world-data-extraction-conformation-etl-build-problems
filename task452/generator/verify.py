"""Independent verifier for task452: reads only target/ and figures.json, on its own code path (pandas readers,
its own journal clock logic, its own PDF stream decoder), and recomputes every graded figure.

    python3 task452/generator/verify.py      exit 1 on any mismatch
"""
import datetime as dt
import json
import math
import os
import re
import sys
import zlib
from zoneinfo import ZoneInfo

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
DUB = ZoneInfo("Europe/Dublin")
UTC = dt.timezone.utc
OUT = []


def ok(name, cond, detail=""):
    OUT.append((name, bool(cond), detail))


def half_up(x):
    return int(math.floor(x + 0.5))


# ------------------------------------------------------------------ PDF: own ASCII85 and Flate decoding
def a85(data):
    data = re.sub(rb"\s", b"", data)
    if data.endswith(b"~>"):
        data = data[:-2]
    out = bytearray()
    group = []
    for ch in data:
        if ch == ord("z") and not group:
            out += b"\0\0\0\0"
            continue
        group.append(ch - 33)
        if len(group) == 5:
            v = 0
            for g in group:
                v = v * 85 + g
            out += v.to_bytes(4, "big")
            group = []
    if group:
        n = len(group)
        group += [84] * (5 - n)
        v = 0
        for g in group:
            v = v * 85 + g
        out += v.to_bytes(4, "big")[:n - 1]
    return bytes(out)


def pdf_strings(path):
    raw = open(path, "rb").read()
    texts = []
    pos = 0
    while True:
        i = raw.find(b"stream", pos)
        if i < 0:
            break
        if raw[i - 3:i] == b"end":
            pos = i + 6
            continue
        j = raw.find(b"endstream", i)
        head = raw[raw.rfind(b"<<", 0, i):i]
        body = raw[i + 6:j].strip(b"\r\n")
        if b"ASCII85Decode" in head:
            body = a85(body)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                pos = j + 9
                continue
        for m in re.finditer(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", body):
            texts.append(m.group(1).decode("latin-1").replace("\\(", "(").replace("\\)", ")"))
        pos = j + 9
    return texts


# ------------------------------------------------------------------ readers
def ledger():
    out = {}
    h1 = pd.read_excel(os.path.join(TGT, "production_ledger_2026.xlsx"), sheet_name="H1 2026", header=3)
    names = {"Limestone (quarry)": "limestone", "Rathmore shale": "shale", "Sand": "sand", "Iron ore": "iron_ore",
             "Steel slag (BOF)": "steel_slag", "Fly ash (PFA)": "fly_ash", "Coal as fired": "coal", "SRF as fired": "srf",
             "Clinker produced": "clinker", "Filter dust to silo S7": "dust", "Raw meal silo stock, month end": "silo",
             "Limestone": "limestone", "Shale": "shale", "Slag": "steel_slag", "PFA": "fly_ash", "Coal (fired)": "coal",
             "SRF (fired)": "srf", "Clinker made": "clinker", "CKD bled (S7)": "dust", "Meal silo closing stock": "silo"}
    for _, r in h1.iterrows():
        if not isinstance(r["Line"], str):
            continue
        k = "K" + r["Line"].split()[-1]
        for i, mo in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun"]):
            out[(k, names[r["Item"]], i + 1)] = float(r[mo])
    h2 = pd.read_excel(os.path.join(TGT, "production_ledger_2026.xlsx"), sheet_name="H2 2026", header=3)
    for _, r in h2.iterrows():
        if r["Item"] not in names:
            continue
        k = "K" + str(r["Line"])[-1]
        for i, mo in enumerate(["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
            out[(k, names[r["Item"]], i + 7)] = float(r[mo])
    return out


def lab():
    df = pd.read_excel(os.path.join(TGT, "QC_lab_composites_2026.xlsx"), sheet_name="Results")
    pref = {"LS": "limestone", "SH": "shale", "SA": "sand", "FE": "iron_ore", "SL": "steel_slag", "FA": "fly_ash",
            "CO": "coal", "RF": "srf", "CK1": "clinker_K1", "CK2": "clinker_K2", "FD1": "dust_K1"}
    out = {}
    for _, r in df.iterrows():
        p, per = r["Sample"].split("-")
        per = per[2:]
        months = [3 * (int(per[1]) - 1) + j for j in (1, 2, 3)] if per.startswith("Q") else [int(per)]
        for m in months:
            out[(pref[p], m)] = (float(r["Hg mg/kg"]), r["Basis"])
    return out


def journal_events():
    """Local wall times to UTC: before the logged IST-to-GMT change on 25 October a repeated time is IST, after it GMT."""
    ev = []
    passed_fallback = False
    for ln in open(os.path.join(TGT, "DCS_event_journal_2026.txt"), encoding="utf-8").read().splitlines():
        if not re.match(r"^\d{4}-\d{2}-\d{2} ", ln):
            continue
        parts = re.split(r"\s{2,}", ln.strip())
        stamp, desc, state = parts[0], parts[3], parts[4].split()[0]
        naive = dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")
        if desc.startswith("CLOCK CHANGE IST TO GMT"):
            utc = naive.replace(tzinfo=DUB, fold=0).astimezone(UTC)
            passed_fallback = True
        else:
            fold = 1 if (passed_fallback and naive.date() == dt.date(2026, 10, 25) and naive.hour == 1) else 0
            utc = naive.replace(tzinfo=DUB, fold=fold).astimezone(UTC)
        ev.append((utc, desc, state))
    return ev


def quarters():
    b = [dt.datetime(2026, m, 1, tzinfo=DUB).astimezone(UTC) for m in (1, 4, 7, 10)] + [dt.datetime(2027, 1, 1, tzinfo=DUB).astimezone(UTC)]
    return list(zip(b[:-1], b[1:]))


def state_hours(ev, kiln, want):
    feed, mill = None, None
    spans, start = [], None
    for t, desc, state in ev:
        if desc == "KILN %s FEED" % kiln:
            feed = state == "ON"
        elif desc == "KILN %s MAIN BURNER" % kiln and state == "TRIP":
            feed = False
        elif desc == "RAW MILL %s" % kiln:
            mill = state in ("START", "RUNNING")
        else:
            continue
        on = bool(feed) and (want == "feed" or mill is False)
        if on and start is None:
            start = t
        elif not on and start is not None:
            spans.append((start, t))
            start = None
    if start is not None:
        spans.append((start, dt.datetime(2027, 1, 1, tzinfo=UTC)))
    res = []
    for a, b in quarters():
        res.append(sum(max(0.0, (min(y, b) - max(x, a)).total_seconds()) for x, y in spans) / 3600.0)
    return res


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    led, lb = ledger(), lab()
    rel = {}
    for k in ("K1", "K2"):
        tot = 0.0
        for (kk, it, m), q in led.items():
            if kk != k or it in ("clinker", "dust", "silo"):
                continue
            hgv, basis = lb[(it, m)]
            ok("basis %s %s %d" % (k, it, m), basis == ("as received" if it in ("coal", "srf") else "dry"))
            tot += q * hgv / 1000.0
        tot -= sum(led[(k, "clinker", m)] * lb[("clinker_" + k, m)][0] for m in range(1, 13)) / 1000.0
        if k == "K1":
            tot -= sum(led[(k, "dust", m)] * lb[("dust_K1", m)][0] for m in range(1, 13)) / 1000.0
        rel[k] = tot
    ok("V1 kiln 1 mercury", half_up(rel["K1"]) == figs["hg_K1_kg"], "%.3f" % rel["K1"])
    ok("V2 kiln 2 mercury", half_up(rel["K2"]) == figs["hg_K2_kg"], "%.3f" % rel["K2"])
    ok("V3 works and margin", half_up(rel["K1"] + rel["K2"]) == figs["hg_works_kg"] and
       half_up(rel["K1"] + rel["K2"]) - figs["limit_kg"] == figs["over_by_kg"])
    lic = " ".join(pdf_strings(os.path.join(TGT, "IEL-1186-03_conditions_consolidated_2026.pdf")))
    ok("V4 licence read back: the load and its hours", ("shall not exceed %d kg" % figs["limit_kg"]) in lic and
       "in compound operation and in direct operation" in lic)
    tests = pdf_strings(os.path.join(TGT, "stack_tests_Hg_2024-2026.pdf"))
    ok("V5 test reports read back", any("AEM-2026-A1-2-Hg" in s for s in tests) and sum(s == "in operation" for s in tests) == 18)
    ev = journal_events()
    for kiln in ("1", "2"):
        d = state_hours(ev, kiln, "direct")
        f = state_hours(ev, kiln, "feed")
        for q in range(4):
            ok("V6 kiln %s Q%d direct-operation hours" % (kiln, q + 1), half_up(d[q]) == figs["direct_h_K%s_Q%d" % (kiln, q + 1)], "%.2f" % d[q])
            ok("V7 kiln %s Q%d hours on feed" % (kiln, q + 1), "{:,}".format(half_up(f[q])) == figs["feed_h_K%s_Q%d" % (kiln, q + 1)], "%.2f" % f[q])
    hist = pd.read_csv(os.path.join(TGT, "PI_historian_K1K2_2026_30min.csv"))
    hist["t"] = pd.to_datetime(hist["Time (UTC)"], utc=True)
    hist["tonnes"] = hist["STK.NOX.REF10 mg/Nm3"] * (21 - hist["STK.O2.DRY %"]) / 11 * hist["STK.FLOW.DRY Nm3/h"] * 0.5 / 1e9
    hist.loc[hist["STK.FLOW.DRY Nm3/h"] <= 0, "tonnes"] = 0.0
    lg = pd.read_csv(os.path.join(TGT, "CEMS_logger_A1-1_A1-2_May2026.csv"), sep=";")
    lg["end"] = pd.to_datetime(lg["Interval end"], format="%d/%m/%Y %H:%M").dt.tz_localize(DUB).dt.tz_convert(UTC)
    lg["t"] = lg["end"] - pd.Timedelta(minutes=30)
    lg["tonnes"] = lg["NOx mg/Nm3 dry"] * lg["Flow Nm3/h dry"] * 0.5 / 1e9
    for kiln, stack in (("K1", "A1-1"), ("K2", "A1-2")):
        h = hist[hist["Line"] == kiln]
        l = lg[(lg["Stack"] == stack) & (~lg["t"].isin(set(h["t"])))]
        tot = h["tonnes"].sum() + l["tonnes"].sum()
        ok("V8 %s NOx" % kiln, half_up(tot) == figs["nox_t_%s" % kiln], "%.2f (%d logger half-hours)" % (tot, len(l)))
        ok("V9 %s historian plus logger cover every half-hour of the year" % kiln, len(h) + len(l) == 365 * 48)
    fails = [o for o in OUT if not o[1]]
    for n, c, d in OUT:
        if not n.startswith("basis") or not c:
            print("%s  %s  %s" % ("PASS" if c else "FAIL", n, d))
    print("verify: %d checks, %d failed" % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
