"""Computes every rung, the golden and every ask figure from the shipped files under target/ alone."""
import csv
import datetime as dt
import os
import re
import zlib
import base64
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Dublin")
UTC = dt.timezone.utc
MONTHS = list(range(1, 13))
MON_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# the analyst's crosswalk from each record's own names to one material list
LEDGER_NAMES = {"Limestone (quarry)": "limestone", "Limestone": "limestone", "Rathmore shale": "shale", "Shale": "shale",
                "Sand": "sand", "Iron ore": "iron_ore", "Steel slag (BOF)": "steel_slag", "Slag": "steel_slag",
                "Fly ash (PFA)": "fly_ash", "PFA": "fly_ash", "Coal as fired": "coal", "Coal (fired)": "coal",
                "SRF as fired": "srf", "SRF (fired)": "srf", "Clinker produced": "clinker", "Clinker made": "clinker",
                "Raw meal silo stock, month end": "silo", "Meal silo closing stock": "silo",
                "Filter dust to silo S7": "dust", "CKD bled (S7)": "dust",
                "Clinker to cement mills": "clinker_out"}
LAB_PREFIX = {"LS": "limestone", "SH": "shale", "SA": "sand", "FE": "iron_ore", "SL": "steel_slag", "FA": "fly_ash",
              "CO": "coal", "RF": "srf", "CK1": "clinker_K1", "CK2": "clinker_K2", "FD1": "dust_K1"}
NONCARB = {"K1": ["steel_slag"], "K2": ["fly_ash"]}


# ------------------------------------------------------------------------------------------------- readers
def read_ledger(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "production_ledger_2026.xlsx"), data_only=True)
    out = {}
    ws = wb["H1 2026"]
    for row in ws.iter_rows(min_row=5, values_only=True):
        if not row or not row[0] or not str(row[0]).startswith("Kiln"):
            continue
        k = "K" + str(row[0]).split()[-1]
        item = LEDGER_NAMES[row[1]]
        for i, m in enumerate(range(1, 7)):
            out[(k, item, m)] = float(row[2 + i])
    ws = wb["H2 2026"]
    for row in ws.iter_rows(min_row=5, values_only=True):
        if not row or not row[0] or row[0] not in LEDGER_NAMES:
            continue
        k = "K" + str(row[1])[-1]
        item = LEDGER_NAMES[row[0]]
        for i, m in enumerate(range(7, 13)):
            out[(k, item, m)] = float(row[3 + i])
    return out


def read_lab(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "QC_lab_composites_2026.xlsx"), data_only=True)
    ws = wb["Results"]
    hdr = [c.value for c in ws[1]]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        rec = dict(zip(hdr, row))
        code = rec["Sample"]
        pre = code.split("-")[0]
        mat = LAB_PREFIX[pre]
        per = code.split("-")[1][2:]
        if per.startswith("Q"):
            q = int(per[1])
            months = [3 * (q - 1) + 1, 3 * (q - 1) + 2, 3 * (q - 1) + 3]
        else:
            months = [int(per)]
        for m in months:
            out[(mat, m)] = rec
    return out


def read_weighbridge(target):
    rows = []
    with open(os.path.join(target, "weighbridge_byproducts_2026.csv"), encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for r in rd:
            rows.append(r)
    seen = set()
    out = []
    for r in rows:
        if not r["Product"].startswith("FILTER DUST") or r["Status"] != "OK":
            continue
        key = tuple(r.values())
        if key in seen:          # a reprinted ticket
            continue
        seen.add(key)
        d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        out.append((d, float(r["Net kg"]) / 1000.0))
    return out


def read_certificates(target):
    """The suppliers' certificate mercury (mg/kg as received) for each fuel and month, three ways: each month's own
    consignments (coal: the cargo in use that month), the tonnage-weighted mean of the year, the plain mean."""
    rows = []
    with open(os.path.join(target, "fuel_receipts_2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((dt.date.fromisoformat(r["Received"]), "coal" if r["Fuel"] == "Coal" else "srf",
                         float(r["Tonnes received"]), float(r["Supplier cert. Hg ug/kg (as received)"]) / 1000.0))
    out = {}
    for fuel in ("coal", "srf"):
        rs = sorted(x for x in rows if x[1] == fuel)
        y26 = [x for x in rs if x[0].year == 2026] if fuel == "srf" else [x for x in rs if x[0] < dt.date(2026, 12, 1)]
        wmean = sum(x[2] * x[3] for x in y26) / sum(x[2] for x in y26)
        pmean = sum(x[3] for x in y26) / len(y26)
        for m in MONTHS:
            if fuel == "srf":
                mm = [x for x in rs if x[0].year == 2026 and x[0].month == m]
                monthly = sum(x[2] * x[3] for x in mm) / sum(x[2] for x in mm)
            else:
                first = dt.date(2026, m, 1)
                monthly = [x for x in rs if x[0] <= first][-1][3]
            out[("certificates_monthly", fuel, m)] = monthly
            out[("certificates_annual", fuel, m)] = wmean
            out[("certificates_plain", fuel, m)] = pmean
    return out


def read_journal(target):
    ev = []
    with open(os.path.join(target, "DCS_event_journal_2026.txt"), encoding="utf-8") as f:
        lines = f.read().splitlines()
    prev_utc = None
    for ln in lines:
        m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s{2}(.{12})\s{2}(.{10})\s{2}(.{32})\s{2}(\S+)", ln)
        if not m:
            continue
        naive = dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
        # local wall time to UTC; in the repeated hour the file's own order decides which occurrence it is
        cands = sorted({naive.replace(tzinfo=TZ, fold=0).astimezone(UTC), naive.replace(tzinfo=TZ, fold=1).astimezone(UTC)})
        t = cands[0]
        if prev_utc is not None and len(cands) > 1 and cands[0] < prev_utc:
            t = cands[1]
        prev_utc = t
        ev.append((t, m.group(4).strip(), m.group(5).strip(), "state at start" in ln))
    return ev


def read_csv(path, sep=","):
    with open(path, encoding="utf-8") as f:
        rd = csv.reader(f, delimiter=sep)
        hdr = next(rd)
        return hdr, [r for r in rd]


def pdf_text(path):
    """Text of a reportlab PDF: every content stream decoded (ASCII85 and Flate) and its strings read."""
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<([^<>]*?)>>\s*stream\r?\n(.*?)endstream", raw, re.S):
        dic, data = m.group(1), m.group(2).strip()
        if b"ASCII85Decode" in dic:
            if data.endswith(b"~>"):
                data = data[:-2]
            data = base64.a85decode(data, adobe=False)
        if b"FlateDecode" in dic:
            try:
                data = zlib.decompress(data)
            except zlib.error:
                continue
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", data, re.S):
            out.append(s.decode("latin-1").replace("\\(", "(").replace("\\)", ")"))
    return out


def read_tests(target):
    """The mean Hg mass emission (g/h), mean clinker t/h and test year per kiln from the test reports."""
    words = pdf_text(os.path.join(target, "stack_tests_Hg_2024-2026.pdf"))
    tests = []
    cur = None
    i = 0
    while i < len(words):
        w = words[i]
        m = re.search(r"AEM-(\d{4})-(A1-\d)-Hg", w)
        if m:
            cur = dict(year=int(m.group(1)), stack=m.group(2), clk=[], gph=[])
            tests.append(cur)
        i += 1
    # second pass: the run rows of each report, read positionally
    k = -1
    mode = None
    for j, w in enumerate(words):
        if "AEM-" in w and "-Hg" in w:
            k += 1
            mode = None
            continue
        if w == "H2O %":
            mode = "proc"
            continue
        if w == "Result":
            mode = "res"
            continue
        if mode == "proc" and w in ("1", "2", "3") and j + 4 < len(words):
            tests[k]["clk"].append(float(words[j + 3]))
        if mode == "res" and w in ("1", "2", "3") and j + 3 < len(words):
            tests[k]["gph"].append(float(words[j + 3]))
        if mode == "res" and w == "Mean":
            tests[k]["mean_gph"] = float(words[j + 3])
            mode = None
    return tests


# ------------------------------------------------------------------------------------------------- the call
def mercury(target, variant="golden"):
    led = read_ledger(target)
    lab = read_lab(target)
    wb = read_weighbridge(target) if variant == "dust_shipped" else []
    res = {}
    for k in ("K1", "K2"):
        hg_in = hg_clk = hg_dust = 0.0
        mats = sorted({it for (kk, it, m) in led if kk == k and it not in ("clinker", "clinker_out", "silo", "dust")})
        per_mat = {}
        for mat in mats:
            tot = 0.0
            if variant == "annual_mean":
                q = [led[(k, mat, m)] for m in MONTHS]
                hg = sum(float(lab[(mat, m)]["Hg mg/kg"]) for m in MONTHS) / 12.0
                tot = sum(q) * hg / 1000.0
            elif variant.startswith("certificates") and mat in ("coal", "srf"):
                cert = read_certificates(target)
                for m in MONTHS:
                    tot += led[(k, mat, m)] * cert[(variant, mat, m)] / 1000.0
            else:
                for m in MONTHS:
                    rec = lab[(mat, m)]
                    q = led[(k, mat, m)]          # raw materials dry, fuels as fired: each on its composite's own basis
                    if variant == "moisture_again":
                        q = q * (1 - float(rec["Moisture % (as received)"]) / 100.0)
                    tot += q * float(rec["Hg mg/kg"]) / 1000.0
            per_mat[mat] = tot
            hg_in += tot
        for m in MONTHS:
            hg_clk += led[(k, "clinker", m)] * float(lab[("clinker_" + k, m)]["Hg mg/kg"]) / 1000.0
        if k == "K1" and variant != "no_dust":
            if variant == "dust_shipped":
                for d, t in wb:
                    hg_dust += t * float(lab[("dust_K1", d.month)]["Hg mg/kg"]) / 1000.0
            else:
                for m in MONTHS:
                    hg_dust += led[(k, "dust", m)] * float(lab[("dust_K1", m)]["Hg mg/kg"]) / 1000.0
        rel = hg_in - hg_clk - hg_dust
        if variant == "silo":
            meal_hg = sum(per_mat[mm] for mm in per_mat if mm not in ("coal", "srf")) * 1000.0 / \
                sum(led[(k, mm, m)] for mm in per_mat if mm not in ("coal", "srf") for m in MONTHS)
            # the meal silo's stock fell over the year: the kiln drew meal ground the year before
            dstock = led[(k, "silo", 12)] - SILO_OPENING[k]
            rel += -dstock * meal_hg / 1000.0
        res[k] = dict(inputs=hg_in, clinker=hg_clk, dust=hg_dust, release=rel, per_mat=per_mat)
    return res


SILO_OPENING = {"K1": 6100.0, "K2": 4300.0}   # opening stock in the 2025 ledger close (not shipped: used only to price the term)


def feed_hours_from_journal(target):
    q = ask_feed(target)
    return {k: sum(v) for k, v in q.items()}


def default_route(target):
    tests = read_tests(target)
    hours = feed_hours_from_journal(target)
    led = read_ledger(target)
    out = {}
    for k, stack in (("K1", "A1-1"), ("K2", "A1-2")):
        t26 = [t for t in tests if t["stack"] == stack and t["year"] == 2026][0]
        three = [t for t in tests if t["stack"] == stack]
        clk_year = sum(led[(k, "clinker", m)] for m in MONTHS)
        out[k] = dict(
            hours=hours[k],
            gph=t26["mean_gph"],
            r0=t26["mean_gph"] * hours[k] / 1000.0,
            r0_three_year=sum(t["mean_gph"] for t in three) / 3 * hours[k] / 1000.0,
            r1_per_clinker=t26["mean_gph"] / (sum(t26["clk"]) / 3) * clk_year / 1000.0,
        )
    return out


# ------------------------------------------------------------------------------------------------- ask 1
def quarter_bounds():
    out = []
    for q in range(4):
        a = dt.datetime(2026, 3 * q + 1, 1, tzinfo=TZ).astimezone(UTC)
        b = (dt.datetime(2026, 3 * q + 4, 1, tzinfo=TZ) if q < 3 else dt.datetime(2027, 1, 1, tzinfo=TZ)).astimezone(UTC)
        out.append((a, b))
    return out


def month_bounds():
    out = []
    for m in MONTHS:
        a = dt.datetime(2026, m, 1, tzinfo=TZ).astimezone(UTC)
        b = (dt.datetime(2026, m + 1, 1, tzinfo=TZ) if m < 12 else dt.datetime(2027, 1, 1, tzinfo=TZ)).astimezone(UTC)
        out.append((a, b))
    return out


def direct_intervals(target, journal=None, burner_trip_stops_feed=True, want="direct"):
    """Intervals in which each kiln was on feed while its raw mill was stopped, from the DCS journal."""
    ev = journal if journal is not None else read_journal(target)
    out = {}
    for n in ("1", "2"):
        feed_on = mill_on = None
        cur = None
        iv = []
        for t, desc, state, start in ev:
            if desc == "KILN %s FEED" % n:
                feed_on = state == "ON"
            elif desc == "KILN %s MAIN BURNER" % n and state == "TRIP" and burner_trip_stops_feed:
                feed_on = False
            elif desc == "RAW MILL %s" % n:
                mill_on = state in ("START", "RUNNING")
            else:
                continue
            direct = bool(feed_on) and (mill_on is False) if want == "direct" else bool(feed_on)
            if direct and cur is None:
                cur = t
            elif not direct and cur is not None:
                iv.append((cur, t))
                cur = None
        if cur is not None:
            iv.append((cur, dt.datetime(2027, 1, 1, tzinfo=UTC)))
        out["K" + n] = iv
    return out


def overlap_hours(iv, a, b):
    tot = 0.0
    for x, y in iv:
        lo, hi = max(x, a), min(y, b)
        if hi > lo:
            tot += (hi - lo).total_seconds() / 3600.0
    return tot


def ask1(target, burner_trip_stops_feed=True):
    iv = direct_intervals(target, burner_trip_stops_feed=burner_trip_stops_feed)
    qb, mb = quarter_bounds(), month_bounds()
    return {k: dict(quarters=[overlap_hours(iv[k], a, b) for a, b in qb],
                    months=[overlap_hours(iv[k], a, b) for a, b in mb]) for k in iv}


def ask_feed(target, burner_trip_stops_feed=True):
    """Hours each kiln was producing clinker (on feed), by local quarter, from the journal."""
    iv = direct_intervals(target, burner_trip_stops_feed=burner_trip_stops_feed, want="feed")
    return {k: [overlap_hours(iv[k], a, b) for a, b in quarter_bounds()] for k in iv}


def ask_feed_historian(target, prorate_gap=True):
    hdr, rows = read_historian(target)
    data = {"K1": {}, "K2": {}}
    for r in rows:
        t = dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
        data[r[1]][t] = float(r[2])
    out = {}
    for k, d in data.items():
        qs = []
        for a, b in quarter_bounds():
            n_all = int((b - a).total_seconds() // 1800)
            got = [f for t, f in d.items() if a <= t < b]
            h = 0.5 * sum(1 for f in got if f > 0)
            if prorate_gap and len(got) < n_all:
                h = h * n_all / len(got)
            qs.append(h)
        out[k] = qs
    return out


def ask1_naive_dst(target):
    """The same journal read with every local time taken as its first occurrence (the repeated hour misplaced)."""
    ev = []
    with open(os.path.join(target, "DCS_event_journal_2026.txt"), encoding="utf-8") as f:
        for ln in f.read().splitlines():
            m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s{2}(.{12})\s{2}(.{10})\s{2}(.{32})\s{2}(\S+)", ln)
            if not m:
                continue
            naive = dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
            ev.append((naive.replace(tzinfo=TZ, fold=0).astimezone(UTC), m.group(4).strip(), m.group(5).strip(),
                       "state at start" in ln))
    iv = direct_intervals(target, journal=ev)
    qb = quarter_bounds()
    return {k: [overlap_hours(iv[k], a, b) for a, b in qb] for k in iv}


def read_historian(target):
    hdr, rows = read_csv(os.path.join(target, "PI_historian_K1K2_2026_30min.csv"))
    return hdr, rows


def ask1_historian(target, prorate_gap=True):
    """The careful route on the historian: run fraction per half-hour, UTC to local quarters, the May hole pro-rated."""
    hdr, rows = read_historian(target)
    seen = set()
    data = {"K1": {}, "K2": {}}
    for r in rows:
        key = tuple(r)
        if key in seen:
            continue
        seen.add(key)
        t = dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
        data[r[1]][t] = (float(r[2]), float(r[3]))     # feed t/h, raw mill run status at the timestamp
    qb = quarter_bounds()
    out = {}
    for k, d in data.items():
        qs = []
        for a, b in qb:
            n_all = int((b - a).total_seconds() // 1800)
            got = [(f, fr) for t, (f, fr) in d.items() if a <= t < b]
            h = sum(0.5 * (1 - fr) for f, fr in got if f > 0)
            if prorate_gap and len(got) < n_all:
                h = h * n_all / len(got)
            qs.append(h)
        out[k] = qs
    return out


# ------------------------------------------------------------------------------------------------- ask 2
def ask2(target, convert=True, use_logger=True, prorate=False, logger_converted_again=False):
    hdr, rows = read_historian(target)
    seen = set()
    hist = {"K1": {}, "K2": {}}
    for r in rows:
        key = tuple(r)
        if key in seen:
            continue
        seen.add(key)
        t = dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
        flow, o2, nox = float(r[4]), float(r[5]), float(r[6])
        if flow <= 0:
            m = 0.0
        else:
            c = nox * (21.0 - o2) / 11.0 if convert else nox
            m = c * flow * 0.5 / 1e9           # tonnes in the half-hour
        hist[r[1]][t] = m
    out = {}
    lhdr, lrows = read_csv(os.path.join(target, "CEMS_logger_A1-1_A1-2_May2026.csv"), sep=";")
    stack = {"A1-1": "K1", "A1-2": "K2"}
    logger = {"K1": {}, "K2": {}}
    for r in lrows:
        end_local = dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M").replace(tzinfo=TZ)
        start = end_local.astimezone(UTC) - dt.timedelta(minutes=30)
        c = float(r[2])
        if logger_converted_again:
            c = c * (21.0 - float(r[3])) / 11.0
        logger[stack[r[1]]][start] = c * float(r[4]) * 0.5 / 1e9
    year0 = dt.datetime(2026, 1, 1, tzinfo=UTC)
    allslots = [year0 + dt.timedelta(minutes=30 * i) for i in range(365 * 48)]
    for k in ("K1", "K2"):
        tot = sum(hist[k].values())
        missing = [t for t in allslots if t not in hist[k]]
        if use_logger:
            tot += sum(logger[k][t] for t in missing)
        elif prorate:
            tot = tot * len(allslots) / (len(allslots) - len(missing))
        out[k] = dict(total=tot, missing=len(missing), logger_cover=sum(1 for t in missing if t in logger[k]))
    return out


def ask2_append(target):
    """The logger appended whole, without removing the hours the historian already holds."""
    base = ask2(target)
    lhdr, lrows = read_csv(os.path.join(target, "CEMS_logger_A1-1_A1-2_May2026.csv"), sep=";")
    stack = {"A1-1": "K1", "A1-2": "K2"}
    extra = {"K1": 0.0, "K2": 0.0}
    hdr, rows = read_historian(target)
    have = {(r[1], r[0]) for r in rows}
    for r in lrows:
        end_local = dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M").replace(tzinfo=TZ)
        start = end_local.astimezone(UTC) - dt.timedelta(minutes=30)
        if (stack[r[1]], start.strftime("%Y-%m-%d %H:%M")) in have:
            extra[stack[r[1]]] += float(r[2]) * float(r[4]) * 0.5 / 1e9
    return {k: base[k]["total"] + extra[k] for k in base}


# ------------------------------------------------------------------------------------------------- ask 3
def ask3(target, correct=True):
    led = read_ledger(target)
    lab = read_lab(target)
    out = {}
    for k in ("K1", "K2"):
        co2 = 0.0
        clk = 0.0
        for m in MONTHS:
            c = led[(k, "clinker", m)]
            rec = lab[("clinker_" + k, m)]
            co2 += c * (0.785 * float(rec["CaO %"]) + 1.092 * float(rec["MgO %"])) / 100.0
            clk += c
            if correct:
                for mat in NONCARB[k]:
                    r2 = lab[(mat, m)]
                    dry = led[(k, mat, m)]
                    co2 -= dry * (0.785 * float(r2["CaO %"]) + 1.092 * float(r2["MgO %"])) / 100.0
        out[k] = dict(co2=co2, clinker=clk, factor=co2 / clk)
    return out


def all_figures(target, limit_kg):
    hg = mercury(target)
    k1, k2 = round(hg["K1"]["release"]), round(hg["K2"]["release"])
    works = k1 + k2
    a1 = ask1(target)
    a2 = ask2(target)
    a3 = ask3(target)
    figs = {
        "hg_K1_kg": k1, "hg_K2_kg": k2, "hg_works_kg": works, "limit_kg": limit_kg,
        "over_by_kg": works - limit_kg,
        "verdict": "over" if works > limit_kg else "under",
    }
    for k in ("K1", "K2"):
        for q in range(4):
            figs["direct_h_%s_Q%d" % (k, q + 1)] = round(a1[k]["quarters"][q])
        figs["direct_h_%s_year" % k] = round(sum(a1[k]["quarters"]))
        figs["nox_t_%s" % k] = round(a2[k]["total"])
        figs["co2_t_%s" % k] = round(a3[k]["co2"])
        figs["co2_factor_%s" % k] = round(a3[k]["factor"], 3)
    return figs
