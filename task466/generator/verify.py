"""Independent verifier for task466: reads every shipped format back on its own code path (CSV with the csv module,
XLSX by unzipping the sheet XML, the event log as text, and the PDFs by decoding their ASCII85 and Flate streams) and
recomputes every graded figure, then compares with generator/figures.json. It imports nothing from the generator.

    python3 task466/generator/verify.py
"""
import base64
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
UTC = dt.timezone.utc
TZ = ZoneInfo("America/Chicago")
OK = []
BAD = []


def ok(label, cond, detail=""):
    (OK if cond else BAD).append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, (": " + detail) if detail else ""))


# ------------------------------------------------------------------------------------------------ PDF, by hand
def pdf_text(path):
    raw = open(path, "rb").read()
    out = []
    for mm in re.finditer(rb"\d+ 0 obj\s*<<(.*?)>>\s*stream\r?\n(.*?)endstream", raw, re.S):
        head, data = mm.group(1), mm.group(2).strip()
        if b"ASCII85Decode" in head:
            data = data.strip()
            if data.endswith(b"~>"):
                data = data[:-2]
            data = base64.a85decode(data)
        if b"FlateDecode" in head:
            try:
                data = zlib.decompress(data)
            except zlib.error:
                continue
        if b"Tj" not in data and b"TJ" not in data:
            continue
        for s in re.finditer(rb"\((.*?)(?<!\\)\)\s*Tj", data, re.S):
            t = s.group(1).replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\")
            out.append(t.decode("latin-1"))
    return out


# ------------------------------------------------------------------------------------------------ XLSX, by hand
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(tn.text or "" for tn in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find("m:sheets", NS):
        rid = sh.get("{%s}id" % NS["r"])
        p = target[rid].lstrip("/")
        p = p if p.startswith("xl/") else "xl/" + p
        rows = []
        for row in ET.fromstring(z.read(p)).iter("{%s}row" % NS["m"]):
            vals = {}
            for c in row.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                t = c.get("t")
                v = c.find("m:v", NS)
                if t == "s":
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif v is None:
                    val = None
                else:
                    val = float(v.text) if re.fullmatch(r"-?[\d.]+(E-?\d+)?", v.text) else v.text
                vals[col] = val
            rows.append([vals.get(i) for i in range(1, max(vals) + 1)] if vals else [])
        out[sh.get("name")] = rows
    return out


# ------------------------------------------------------------------------------------------------ the rule, read back
rule = " ".join(pdf_text(os.path.join(T, "DEQ_closed_landfill_methane_rule_extract.pdf")))
ok("positive control: the rule PDF decodes through ASCII85 and Flate to its own text",
   "Collection efficiency" in rule and "Schedule 2" in rule, "%d characters" % len(rule))
RHO = float(re.search(r"normal cubic metre of methane weighs ([\d.]+) kg", rule).group(1))
CE = float(re.search(r"Final cover with geomembrane\s+([\d.]+)", rule).group(1))
OX = float(re.search(r"oxidised in the cap:\s+([\d.]+)", rule).group(1))
DE_FLARE = float(re.search(r"enclosed flare ([\d.]+)", rule).group(1))
DE_ENG = float(re.search(r"engine ([\d.]+);", rule).group(1))
T2 = float(re.search(r"Tier 2\s+(\d+) tonnes or more", rule).group(1))
T3 = float(re.search(r"Tier 3\s+(\d+) tonnes or more", rule).group(1))
C2 = int(re.search(r"under %d tonnes\s+\$([\d,]+)" % T3, rule).group(1).replace(",", ""))
C3 = int(re.search(r"Tier 3.*?\$([\d,]+)", rule).group(1).replace(",", ""))
ok("rule factors read from the PDF", (RHO, CE, OX, DE_ENG, DE_FLARE, T2, T3, C2, C3) ==
   (0.7168, 0.90, 0.10, 0.99, 0.99, 375.0, 450.0, 118000, 312000), "")
plan = " ".join(pdf_text(os.path.join(T, "BH_gas_management_plan_2025.pdf")))
EXC = float(re.search(r"more than (\d+) ppm methane above background", plan).group(1))
ok("plan read from the PDF: the exceedance level and the void rule", EXC == 500 and "readings taken since the last passing check are void" in plan, "")

# ------------------------------------------------------------------------------------------------ historian
rows = []
with open(os.path.join(T, "BH_gas_plant_hourly_2024-2026.csv"), newline="", encoding="utf-8") as f:
    lines = [ln for ln in f if not ln.startswith("#")]
rd = csv.DictReader(lines)
for r in rd:
    t = dt.datetime.strptime(r["Timestamp (UTC)"], "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
    fl = float(r["FT-101 LFG flow (Nm3/h)"])
    c = float(r["AT-101 CH4 (%)"]) if r["AT-101 CH4 (%)"] else 0.0
    rows.append(dict(t=t, run=float(r["BLWA run (h)"]) + float(r["BLWB run (h)"]), flow=fl, ch4=c,
                     kg=fl * c / 100.0 * RHO, g1=float(r["FT-201 GEN1 fuel (Nm3/h)"]),
                     g2=float(r["FT-202 GEN2 fuel (Nm3/h)"]), fm=float(r["FT-301 flare gas (m3/h)"])))
Y0 = dt.datetime(2026, 1, 1, tzinfo=TZ).astimezone(UTC)
Y1 = dt.datetime(2027, 1, 1, tzinfo=TZ).astimezone(UTC)
idx = {r["t"]: i for i, r in enumerate(rows)}
yr = [r for r in rows if Y0 <= r["t"] < Y1]
captured = sum(r["kg"] for r in yr) / 1000.0
HOURS = (Y1 - Y0).total_seconds() / 3600.0

# ------------------------------------------------------------------------------------------------ outage log
ol = xlsx_sheets(os.path.join(T, "BH_gas_plant_outage_log_2024-2026.xlsx"))["Outages"]
outs = []
for r in ol:
    if r and isinstance(r[0], float) and r[1]:
        a = dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M").replace(tzinfo=TZ).astimezone(UTC)
        b = dt.datetime.strptime(r[2], "%Y-%m-%d %H:%M").replace(tzinfo=TZ).astimezone(UTC)
        outs.append(dict(a=a, b=b, cause=r[4]))
down = sum((o["b"] - o["a"]).total_seconds() / 3600.0 for o in outs if Y0 <= o["a"] < Y1)
frec = 1 - down / HOURS


def released(gen, cap):
    return (gen - cap) * (1 - OX) + cap * (1 - DE_ENG)


# steady hours: full running, not in an outage hour, and outside a fixed 36 h after each restart (an independent rule
# from the generator's return-to-baseline windows)
bad = set()
for o in outs:
    h = o["a"].replace(minute=0)
    while h <= o["b"] + dt.timedelta(hours=36):
        bad.add(h)
        h += dt.timedelta(hours=1)
gen = 0.0
for mo in range(1, 13):
    a = dt.datetime(2026, mo, 1, tzinfo=TZ).astimezone(UTC)
    b = (dt.datetime(2026, mo + 1, 1, tzinfo=TZ) if mo < 12 else dt.datetime(2027, 1, 1, tzinfo=TZ)).astimezone(UTC)
    st = [r["kg"] for r in yr if a <= r["t"] < b and r["run"] >= 0.999 and r["t"] not in bad]
    gen += (sum(st) / len(st)) / CE * (b - a).total_seconds() / 3600.0 / 1000.0
rel = released(gen, captured)
hh8 = released(captured / (CE * frec), captured)
naive = released(captured / CE, captured)
tier = "Tier 1" if rel < T2 else ("Tier 2" if rel < T3 else "Tier 3")
charge = 0 if tier == "Tier 1" else (C2 if tier == "Tier 2" else C3)

F = json.load(open(os.path.join(HERE, "figures.json")))
ok("captured methane, whole tonnes", int(round(captured)) == F["captured_t"], "%.2f" % captured)
ok("methane generated, nearest 100 t", int(100 * round(gen / 100)) == F["generated_t_nearest_100"], "%.1f" % gen)
ok("methane released, nearest 10 t", int(10 * round(rel / 10)) == F["released_t_nearest_10"], "%.2f" % rel)
ok("tier and charge", tier == F["tier"] and charge == F["charge_usd"], "%s %d" % (tier, charge))
ok("the running-share route files another tier, as figures.json says", int(round(hh8)) == F["default_hh8_released_t"]
   and hh8 >= T3, "%.2f" % hh8)
ok("capture over 0.90 files Tier 1, as figures.json says", int(round(naive)) == F["naive_released_t"] and naive < T2, "%.2f" % naive)

# ------------------------------------------------------------------------------------------------ event log
ev = []
last = None
with open(os.path.join(T, "BH_engine_plant_events_2026.txt"), encoding="utf-8") as f:
    for ln in f:
        mm = re.match(r"^(\d{4}-\d\d-\d\d)\s+(\d\d:\d\d:\d\d)\s+(GEN1|GEN2|FLR)\s+(.+?)\s{2,}(.*)$", ln.rstrip())
        if not mm:
            continue
        naive_t = dt.datetime.strptime(mm.group(1) + " " + mm.group(2), "%Y-%m-%d %H:%M:%S")
        t = naive_t.replace(tzinfo=TZ, fold=0).astimezone(UTC)
        if last is not None and t < last:
            t = naive_t.replace(tzinfo=TZ, fold=1).astimezone(UTC)
        last = t
        ev.append((t, mm.group(3), mm.group(4).strip(), mm.group(5)))


def qb(q):
    m0 = (1, 4, 7, 10)[q - 1]
    a = dt.datetime(2026, m0, 1, tzinfo=TZ).astimezone(UTC)
    b = (dt.datetime(2026, m0 + 3, 1, tzinfo=TZ) if q < 4 else dt.datetime(2027, 1, 1, tzinfo=TZ)).astimezone(UTC)
    return a, b


def overlap(ivs, a, b):
    return sum(max(0.0, (min(y, b) - max(x, a)).total_seconds()) for x, y in ivs) / 3600.0


pfail = [o for o in outs if o["cause"] == "Utility power failure"]
for unit, e in (("GEN1", 1), ("GEN2", 2)):
    on, since, ivs, starts, req = True, Y0, [], [], None
    for t, u, code, text in ev:
        if u != unit:
            continue
        if code == "START REQUEST":
            req = t if on is False else None
            continue
        if code == "START FAIL":
            req = None
            continue
        if code == "STOP" and on is False and req is not None:
            starts.append(req)          # fired from standstill, stopped before synchronising
            req = None
            continue
        if code in ("STOP", "TRIP", "BREAKER OPEN") and on:
            ivs.append((since, t))
            on = code if code == "BREAKER OPEN" else False
        elif code == "CONTROLLER POWER UP":
            if on:
                src = [o for o in pfail if o["a"] <= t <= o["b"]]
                ivs.append((since, src[0]["a"] if src else t))
            on = False
        elif code == "RUNNING":
            if on is False:
                starts.append(t)
            if on is not True:
                since = t
            on = True
    if on is True:
        ivs.append((since, Y1))
    for q in (1, 2, 3, 4):
        a, b = qb(q)
        h = overlap(ivs, a, b)
        n = sum(1 for s in starts if a <= s < b)
        ok("engine %d Q%d hours and starts" % (e, q),
           int(round(h)) == F["engine%d_hours_q%d" % (e, q)] and n == F["engine%d_starts_q%d" % (e, q)], "%.2f h, %d" % (h, n))

flr = [x for x in ev if x[1] == "FLR"]
perm = flr[0][2] in ("LOW TEMP", "FLARE STOP")
since = Y0 if perm else None
ivs = []
for t, u, code, text in flr:
    if code in ("TEMP PERMISSIVE", "TEMP NORMAL") and not perm:
        perm, since = True, t
    elif code in ("LOW TEMP", "FLARE STOP") and perm:
        ivs.append((since, t))
        perm = False
for q in (1, 2, 3, 4):
    a, b = qb(q)
    h = overlap(ivs, a, b)
    dest = sum(max(0.0, r["flow"] - r["g1"] - r["g2"]) * r["ch4"] / 100.0 * RHO for r in rows if a <= r["t"] < b) * DE_FLARE / 1000.0
    ok("flare Q%d hours and methane destroyed" % q,
       int(round(h)) == F["flare_hours_q%d" % q] and int(round(dest)) == F["flare_destroyed_t_q%d" % q], "%.2f h, %.2f t" % (h, dest))

# ------------------------------------------------------------------------------------------------ surface monitoring
sem = xlsx_sheets(os.path.join(T, "BH_surface_emissions_monitoring_2026.xlsx"))
site = xlsx_sheets(os.path.join(T, "BH_site_register_2025.xlsx"))["Site"]
tie = [r[1] for r in site if r and r[0] == "Site grid"][0]
E0, N0, LA0, LO0 = re.search(r"E(\d+) N(\d+) = ([\d.]+) N, ([\d.]+) W", tie).groups()
E0, N0, LA0, LO0 = float(E0), float(N0), float(LA0), -float(LO0)
# WGS84 ellipsoid radii of curvature at the tie latitude, metres to US survey feet
a_e, f_e = 6378137.0, 1 / 298.257223563
e2 = f_e * (2 - f_e)
phi = math.radians(LA0)
Mr = a_e * (1 - e2) / (1 - e2 * math.sin(phi) ** 2) ** 1.5
Nr = a_e / math.sqrt(1 - e2 * math.sin(phi) ** 2)
FT = 3937.0 / 1200.0


def to_site(lat, lon):
    return (E0 + math.radians(lon - LO0) * Nr * math.cos(phi) * FT, N0 + math.radians(lat - LA0) * Mr * FT)


checks = []
with open(os.path.join(T, "SEM_analyser_checks_2026.csv"), newline="") as f:
    for r in csv.DictReader(f):
        checks.append((dt.datetime.strptime(r["date"] + " " + r["time"], "%Y-%m-%d %H:%M"), r["result"]))
void = []
for t, res in checks:
    if res == "FAIL":
        prior = [u for u, rr in checks if rr == "PASS" and u < t and u.date() == t.date()]
        void.append((max(prior), t))
rm = []
for r in sem["Re-monitoring"][2:]:
    if r and r[0]:
        x, y = to_site(r[3], r[4])
        rm.append((dt.datetime.strptime(r[0] + " " + r[1], "%Y-%m-%d %H:%M"), x, y, r[5]))
for q in (1, 2, 3, 4):
    pts = {}
    lastday = None
    for r in sem["Q%d walkover" % q][2:]:
        if not r or not r[0]:
            continue
        t = dt.datetime.strptime(r[0] + " " + r[1], "%Y-%m-%d %H:%M:%S")
        lastday = max(lastday, t) if lastday else t
        if any(lo <= t < hi for lo, hi in void):
            continue
        if r[5] - r[6] > EXC:
            pts.setdefault(r[2], (r[3], r[4]))
    still = 0
    for lab, (x, y) in pts.items():
        later = sorted(v for v in rm if v[0] > lastday and math.hypot(v[1] - x, v[2] - y) <= 50)
        if later and later[0][3] - 3 > EXC:
            still += 1
    ok("walkover Q%d exceedance locations and still over at first re-monitoring" % q,
       len(pts) == F["sem_exceed_q%d" % q] and still == F["sem_still_q%d" % q], "%d, %d" % (len(pts), still))

# ------------------------------------------------------------------------------------------------ golden files agree
gold = xlsx_sheets(os.path.join(TASK, "golden", "breck_hollow_methane_return_2026.xlsx"))
ret = {r[0]: (r[1] if len(r) > 1 else None) for r in gold["Return 2026"] if r and r[0]}
ok("golden workbook carries the verified return figures",
   ret.get("Methane generated (t, nearest 100)") == F["generated_t_nearest_100"]
   and ret.get("Methane captured (t)") == F["captured_t"] and ret.get("Methane released (t, nearest 10)") == F["released_t_nearest_10"], "")
brief = " ".join(pdf_text(os.path.join(TASK, "golden", "breck_hollow_charge_brief_2026.pdf")))
ok("golden brief states the tier and the charge", "Tier 2" in brief and "$118,000" in brief, "")

print("%s  task466 verify: %d checks, %d failed" % ("PASS" if not BAD else "FAIL", len(OK) + len(BAD), len(BAD)))
sys.exit(1 if BAD else 0)
