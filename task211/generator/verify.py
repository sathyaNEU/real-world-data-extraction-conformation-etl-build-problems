"""task211 independent verifier: recomputes every graded figure from target/ alone (no generator import) and compares
it with generator/figures.json at the graded rounding. Exit 1 on any mismatch.
Run: python3 task211/generator/verify.py"""
import csv, json, os, re, sys, datetime as dt
from collections import defaultdict
import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
BAD = []


def rows(n):
    with open(os.path.join(T, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(label, got, want, unit):
    good = round(got / unit) == round(want / unit)
    print("%-4s %-46s %14.4f %14.4f" % ("OK" if good else "BAD", label[:46], got, want))
    if not good:
        BAD.append(label)


# ---------------------------------------------------------------- the record, in Danish time
st = {r["station"]: r for r in rows("buoy_stations.csv")}
byname = {r["former_export_name"]: r["station"] for r in st.values()}
site_of = {k: v["site"] for k, v in st.items()}
NH = 2976; H = 2880
rec = defaultdict(dict)   # (site, winter) -> {hour: hs}


def place(station, t_utc, hs):
    loc = t_utc + dt.timedelta(hours=1)
    y = loc.year if loc.month >= 10 else loc.year - 1
    h = int((loc - dt.datetime(y, 11, 1)).total_seconds() // 3600)
    if 0 <= h < NH:
        rec[(site_of[station], y)][h] = hs


for r in rows("buoy_hm0_2008_2017.csv"):
    place(byname[r["buoy_name"]], dt.datetime.strptime(r["date_hour_utc"], "%Y%m%d%H"), int(r["hm0_cm"]) / 100)
for r in rows("buoy_hs_2016_2026.csv"):
    place(r["station"], dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%MZ"), float(r["hs_m"]))
SITES = ["Skarvgrund", "Lillevig Banke", "Osterrev", "Molleflak", "Fjernhav"]
WINTERS = sorted({y for (_, y) in rec})
HS = {(s, y): np.array([rec[(s, y)][h] for h in range(NH)]) for s in SITES for y in WINTERS}
assert len(WINTERS) == 18

# ---------------------------------------------------------------- registers and procedure
fleet = list(openpyxl.load_workbook(os.path.join(T, "vessel_register_2026.xlsx"))["Fleet"].iter_rows(values_only=True))
fh = fleet[0]
FV = [dict(zip(fh, r)) for r in fleet[1:] if r[2].startswith("Floating")]
LW = FV[0]["hs_working_limit_m"]; LS = FV[0]["hs_station_keeping_limit_m"]
SHELTER = {v["campaign_2026_27_site"]: v["shelter_port"] for v in FV}
GT = {v["vessel"]: v["gross_tonnage"] for v in FV}
pw = openpyxl.load_workbook(os.path.join(T, "port_register_2026.xlsx"))
ports = [dict(zip(next(pw["Ports"].iter_rows(values_only=True)), r)) for r in list(pw["Ports"].iter_rows(values_only=True))[1:]]
BERTHS = {p["port"]: int(p["heavy_lift_berths"] or 0) for p in ports}
DUES = {p["port"]: p["dues_eur_per_gt_per_24h"] for p in ports}
PAS = {(r[0], r[1]): int(r[3]) for r in list(pw["Passage plan"].iter_rows(values_only=True))[1:]}
TC = 10
dpr = rows("daily_progress_reports_2023_2026.csv")
MOORINGS = sorted({r["location"] for r in dpr if r["activity"].startswith("On storm moorings")})
assert len(MOORINGS) == 1
KAL = MOORINGS[0]


def runlen(x):
    r = np.zeros(len(x) + 1, dtype=int)
    for i in range(len(x) - 1, -1, -1):
        r[i] = r[i + 1] + 1 if x[i] <= LW else 0
    return r


def replay(y, sites, windows=None, trace=False):
    hs = {s: HS[(s, y)] for s in sites}; rl = {s: runlen(hs[s]) for s in sites}
    state = {s: None for s in sites}; until = {s: 0 for s in sites}; at = {s: None for s in sites}
    held = defaultdict(list); down = {s: 0 for s in sites}
    tr = {s: [None] * H for s in sites}
    for h in range(H):
        for s in sites:
            a0, a1 = windows[s] if windows else (0, H)
            if a0 <= h < a1 and state[s] == "port":
                a = h + PAS[(s, at[s])]
                if a + TC <= NH and rl[s][a] >= TC and hs[s][h: a + 1].max() <= LS:
                    if s in held[at[s]]:
                        held[at[s]].remove(s)
                    state[s] = "back"; until[s] = a
        for s in sites:
            a0, a1 = windows[s] if windows else (0, H)
            if not a0 <= h < a1:
                if state[s] is not None and h >= a1:
                    for p in held:
                        if s in held[p]:
                            held[p].remove(s)
                    state[s] = None
                continue
            if state[s] is None:
                state[s] = "site"
            if state[s] == "back" and h >= until[s]:
                state[s] = "site"
            home = SHELTER[s]
            if state[s] == "site":
                if hs[s][h: h + PAS[(s, home)] + 1].max() > LS:
                    state[s] = "out"; until[s] = h + PAS[(s, home)]; at[s] = home; r_ = ("TRN", home)
                elif hs[s][h] > LW:
                    r_ = ("WOW", s)
                else:
                    r_ = ("INST", s)
            elif state[s] == "out":
                r_ = ("TRN", home)
                if h >= until[s]:
                    if len(held[home]) < BERTHS[home]:
                        held[home].append(s); state[s] = "port"; r_ = ("SHEL", home)
                    else:
                        state[s] = "cont"; until[s] = h + PAS[(home, KAL)]; at[s] = KAL; r_ = ("TRN", KAL)
            elif state[s] == "cont":
                r_ = ("TRN", KAL)
                if h >= until[s]:
                    state[s] = "port"; r_ = ("SHEL", KAL)
            elif state[s] == "port":
                r_ = ("SHEL", at[s])
            else:
                r_ = ("TRN", s)
            down[s] += r_[0] != "INST"
            tr[s][h] = r_
    return (down, tr) if trace else down


av = {s: [] for s in SITES}; own = {s: [] for s in SITES}
for y in WINTERS:
    d0 = replay(y, SITES); A = sum(d0.values())
    for s in SITES:
        av[s].append(A - sum(replay(y, [x for x in SITES if x != s]).values())); own[s].append(d0[s])
AV = {s: np.mean(v) / 24 for s, v in av.items()}; OWN = {s: np.mean(v) / 24 for s, v in own.items()}
for s in SITES:
    check("avoided " + s, AV[s], FIG["avoided_days"][s], 1)
    check("own downtime " + s, OWN[s], FIG["own_downtime_days_all_floating"][s], 1)
order = sorted(SITES, key=lambda s: -AV[s])
print("call", order[0], "runner-up", order[1])
if order[0] != FIG["call"] or order[1] != FIG["runner_up"]:
    BAD.append("call or runner-up")
check("gap", AV[order[0]] - AV[order[1]], FIG["gap_days"], 1)

# ---------------------------------------------------------------- ask 1: statements, revisions line by line, catch-ups re-dated
sta = rows("developer_standby_statements.csv")
where = defaultdict(set)   # (vessel, yyyy-mm) -> sites worked, from the progress reports
for r in dpr:
    where[(r["vessel"], r["report_date"][:7])].add(r["site"])
rev = {}
for r in sta:
    if r["their_ref"].startswith("Rev. "):
        rev[(r["their_ref"][5:], r["vessel"], r["category"])] = r
out = defaultdict(float)
for r in sta:
    if r["their_ref"].startswith("Rev. "):
        continue
    k = (r["statement_no"], r["vessel"], r["category"])
    days = float(rev[k]["days"]) if k in rev else float(r["days"])
    y, m = int(r["period"][:4]), int(r["period"][5:])
    wy = y if m >= 11 else y - 1
    if r["site"] not in where.get((r["vessel"], r["period"]), set()):
        # the vessel did not work at that site that month: the line settles its last month there
        last = max(p for (v, p), ss in where.items() if v == r["vessel"] and r["site"] in ss and p < r["period"])
        ly, lm = int(last[:4]), int(last[5:])
        wy = ly if lm >= 11 else ly - 1
    out["%s|%d/%02d" % (r["developer"], wy, (wy + 1) % 100)] += days
for k, v in FIG["ask_statements_days"].items():
    check("ask 1 " + k, out.get(k, 0), v, 0.01)

# ---------------------------------------------------------------- ask 2: the old codes, the go-live gap
js = json.load(open(os.path.join(T, "atlas_shift_reports.json")))["shifts"]
txt = "".join(p.extract_text() for p in PdfReader(os.path.join(T, "atlas_final_hire_statement.pdf")).pages)
stated = float(re.search(r"reduced rate, weather standby\s+(\d+)", txt).group(1))
w2 = defaultdict(float)
for x in js:
    old = not x["id"].isdigit()
    y, m = int(x["date"][:4]), int(x["date"][5:7]); wy = y if m >= 11 else y - 1
    k = "%d/%02d" % (wy, (wy + 1) % 100)
    w2[k] += sum(h for c, h in x["hours"].items() if (c in ("WW", "WS") if old else c == "WX"))
reported = sum(x["hours"].get("WX", 0) for x in js if x["id"].isdigit() and x["date"] <= "2026-02-15")
w2["2025/26"] += stated - reported
for k, v in FIG["ask_atlas_weather_standby_hours"].items():
    check("ask 2 " + k, w2.get(k, 0), v, 1)

# ---------------------------------------------------------------- ask 3: calls from berth times, re-keyed copies matched
ap = rows("ap_port_charges_2023_2026.csv")
w3 = defaultdict(float)


def pw_key(port, t):
    y = t.year if t.month >= 10 else t.year - 1
    return "%s|%d/%02d" % (port, y, (y + 1) % 100)


ends = {}
for x in sorted([x for x in ap if x["vendor"] == "Tranevig Havn"], key=lambda x: (x["vessel"], x["berth_from"])):
    t = dt.datetime.fromisoformat(x["berth_from"])
    if ends.get(x["vessel"]) != t:
        w3[pw_key("Tranevig", t)] += float(x["amount_eur"])
    ends[x["vessel"]] = t + dt.timedelta(hours=int(x["berth_hours"]))
seen = set()
for x in ap:
    if x["vendor"] == "Hjortby Havn":
        k = (x["invoice_no"].lstrip("0"), x["vessel"], x["berth_from"], x["berth_hours"])
        if k in seen:
            continue
        seen.add(k)
        t = dt.datetime.fromisoformat(x["berth_from"])
        fee = GT[x["vessel"]] * DUES["Hjortby Havn"] * -(-int(x["berth_hours"]) // 24)
        w3[pw_key("Hjortby Havn", t)] += round(fee, 2)
for k, v in FIG["ask_port_dues_eur"].items():
    check("ask 3 " + k, w3.get(k, 0), v, 10)

print("%s  %d mismatches" % ("PASS" if not BAD else "FAIL", len(BAD)))
sys.exit(1 if BAD else 0)
