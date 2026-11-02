"""Independent verifier: reads only the shipped bundle (every format: CSV, JSONL, XLSX, PDF) on its own code path
and recomputes the call and every ask figure, then compares with generator/figures.json."""
import sys, os, re, csv, json, zlib, base64, datetime as dt, zipfile
from xml.etree import ElementTree as ET
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------- format readers (own code: no openpyxl, no pandas) ----------
def pdf_text(path):
    """text of every content stream: objects parsed one by one, ASCII85 then Flate decoded as each filter says"""
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"\d+\s+0\s+obj(.*?)endobj", data, re.S):
        obj = m.group(1)
        k = obj.find(b"stream")
        if k < 0:
            continue
        head = obj[:k]
        body = obj[k + 6:]
        body = body[2:] if body.startswith(b"\r\n") else body[1:]
        e = body.rfind(b"endstream")
        body = body[:e].rstrip(b"\r\n")
        filters = re.findall(rb"/(ASCII85Decode|FlateDecode)", head)
        try:
            for f in filters:
                if f == b"ASCII85Decode":
                    b = body.strip()
                    if b.startswith(b"<~"):
                        b = b[2:]
                    if b.endswith(b"~>"):
                        b = b[:-2]
                    body = base64.a85decode(b)
                else:
                    body = zlib.decompress(body)
        except Exception:
            continue
        for t in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", body, re.S):
            out.append(t.decode("latin-1"))
        for arr in re.findall(rb"\[(.*?)\]\s*TJ", body, re.S):
            out.append("".join(x.decode("latin-1") for x in re.findall(rb"\((.*?)(?<!\\)\)", arr, re.S)))
    txt = " ".join(out)
    txt = txt.replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\")
    return re.sub(r"\s+", " ", txt)


def xlsx_rows(path, sheet_index=0):
    with zipfile.ZipFile(path) as z:
        ss = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            ns = {"m": root.tag.split("}")[0].strip("{")}
            for si in root.findall("m:si", ns):
                ss.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        sheets = sorted([n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n)], key=lambda n: int(re.findall(r"\d+", n)[0]))
        root = ET.fromstring(z.read(sheets[sheet_index]))
        ns = root.tag.split("}")[0].strip("{")
        rows = []
        for r in root.iter("{%s}row" % ns):
            vals = {}
            for c in r.findall("{%s}c" % ns):
                ref = c.get("r"); col = re.match(r"[A-Z]+", ref).group(0)
                v = c.find("{%s}v" % ns); is_ = c.find("{%s}is" % ns)
                if c.get("t") == "s" and v is not None:
                    val = ss[int(v.text)]
                elif c.get("t") == "inlineStr" and is_ is not None:
                    val = "".join(t.text or "" for t in is_.iter("{%s}t" % ns))
                elif v is not None:
                    val = v.text
                else:
                    val = None
                vals[col] = val
            if vals:
                width = max(len(k) for k in vals)
                cols = sorted(vals, key=lambda k: (len(k), k))
                rows.append([vals.get(k) for k in cols])
        return rows


def csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------- recomputation ----------
def compute(target):
    reg_rows = xlsx_rows(os.path.join(target, "tank_register.xlsx"))
    hi = [i for i, r in enumerate(reg_rows) if r and r[0] == "Tank"][0]
    hdr = reg_rows[hi]
    reg = {}
    for r in reg_rows[hi + 1:]:
        if r and r[0]:
            d = dict(zip(hdr, r))
            reg[d["Tank"]] = {"marina": d["Marina"], "product": d["Product"], "re": float(d["Reorder height (in)"]),
                              "half": float(d["Half-full height (in)"]), "fill": float(d["Normal fill height (in)"]), "chart": d["Chart no."]}
    pip = xlsx_rows(os.path.join(target, "dock_piping.xlsx"))
    hi = [i for i, r in enumerate(pip) if r and r[0] == "Marina"][0]
    piping = {(r[0], r[2]): r[4] for r in pip[hi + 1:] if r and r[0]}
    setup = csv_rows(os.path.join(target, "atg_tank_setup.csv"))
    def tid_of(cs, tn, when):
        for s in setup:
            if s["console_sn"] == cs and s["tank"] == str(tn):
                a = s["in_service_from"]; b = s["in_service_to"] or "2100-01-01"
                if a <= when.strftime("%Y-%m-%d") <= b:
                    return s["marina_tank_ref"]
    kk = {"REC-90 ethanol-free": 0.00068, "E10 unleaded": 0.00069, "Diesel": 0.00046}
    fs3 = pdf_text(os.path.join(target, "FS-3_fuel_systems_standard.pdf"))
    for prod, k in (("REC-90 ethanol-free", "0.00068"), ("E10 unleaded", "0.00069"), ("Diesel", "0.00046")):
        assert k in fs3, "FS-3 Table 1 not read back"
    limit = float(re.search(r"by more than (\d+) gallons", fs3).group(1))
    # gauge readings, re-dated on the sequence chain
    inv = csv_rows(os.path.join(target, "atg_inventory_2026.csv"))
    groups = {}
    for r in inv:
        groups.setdefault((r["console_sn"], r["tank"]), []).append(r)
    readings = {}
    for (cs, tn), rows in groups.items():
        rows.sort(key=lambda r: int(r["record_seq"]))
        ts = [dt.datetime.fromisoformat(r["reading_time"]) for r in rows]
        bad = [i for i, t in enumerate(ts) if t.year != 2026]
        if bad:
            j = bad[-1]
            shift = ts[j + 1] - dt.timedelta(hours=2) - ts[j]
            for i in bad:
                ts[i] += shift
        for r, t in zip(rows, ts):
            if t.year == 2026:
                readings.setdefault(tid_of(cs, tn, t), []).append((t, float(r["height_in"]), float(r["temp_f"]), float(r["tc_gal_60f"])))
    for k in readings:
        readings[k].sort()
    # A1
    year = {dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)}
    A1 = {t: len(year - {x[0].date() for x in readings.get(t, [])}) for t in reg}
    # sales (legacy) per tank
    sales = {}
    leg = csv_rows(os.path.join(target, "dock_sales_legacy_2026.csv"))
    for r in leg:
        sales.setdefault(piping[(r["store_name"], r["disp_hose"])], []).append((dt.datetime.strptime(r["sale_time"], "%m/%d/%Y %H:%M:%S"), float(r["gallons"])))
    # deliveries and bills of lading
    dlv = {}
    for r in csv_rows(os.path.join(target, "atg_deliveries_2026.csv")):
        s = dt.datetime.fromisoformat(r["start_time"]); e = dt.datetime.fromisoformat(r["end_time"])
        dlv.setdefault(tid_of(r["console_sn"], r["tank"], s), []).append((s, e, float(r["start_height_in"]), float(r["end_height_in"]),
                                                                         float(r["start_tc_gal_60f"]), float(r["end_tc_gal_60f"]), float(r["start_temp_f"]), float(r["end_temp_f"])))
    up = {g["marina"].upper(): g["marina"] for g in reg.values()}
    bols = {}
    for r in csv_rows(os.path.join(target, "bols_2026.csv")):
        m = up[r["ship_to"]]
        tid = [t for t in reg if reg[t]["marina"] == m and t.endswith("-" + r["tank_ref"][2:])][0]
        bols.setdefault(tid, []).append((dt.datetime.strptime(r["drop_time"], "%m/%d/%Y %H:%M"), float(r["net_gal_60f"])))
    s0, s1 = dt.datetime(2026, 4, 1), dt.datetime(2026, 11, 1)
    call = {}
    for tid, g in reg.items():
        k = kk[g["product"]]
        R = [x for x in readings.get(tid, []) if s0 <= x[0] < s1]
        D = [x for x in dlv.get(tid, []) if s0 <= x[0] < s1]
        S = sorted(sales.get(tid, []))
        st = np.array([x[0].timestamp() for x in S]); sg = np.array([x[1] for x in S])
        def sold(a, b, ta, tb):
            msk = (st > a.timestamp()) & (st <= b.timestamp())
            return float(sg[msk].sum()) * (1 - k * ((ta + tb) / 2 - 60))
        # observations of the chart error between heights: intervals carry a meter term, deliveries do not
        knots = sorted(set([float(x) for x in np.arange(6, 116, 3)] + [g["re"], g["half"], g["fill"]]))
        def basis(h):
            v = np.interp(h, knots, np.eye(len(knots)).T.tolist()[0]) if False else None
            out = np.zeros(len(knots))
            if h <= knots[0]:
                out[0] = 1; return out
            if h >= knots[-1]:
                out[-1] = 1; return out
            j = int(np.searchsorted(knots, h)) - 1
            f = (h - knots[j]) / (knots[j + 1] - knots[j]); out[j] = 1 - f; out[j + 1] = f
            return out
        rows, ys = [], []
        spans = [(x[0], x[1]) for x in D]
        for a, b in zip(R[:-1], R[1:]):
            if (b[0] - a[0]).total_seconds() > 2.1 * 3600 or any(x < b[0] and y > a[0] for x, y in spans):
                continue
            sn = sold(a[0], b[0], a[2], b[2])
            rows.append(np.concatenate([basis(b[1]) - basis(a[1]), [sn]])); ys.append(b[3] - a[3] + sn)
        for x in D:
            bl = [b for b in bols.get(tid, []) if x[0] - dt.timedelta(hours=3) <= b[0] <= x[0] + dt.timedelta(minutes=30)]
            if not bl:
                continue
            sn = sold(x[0], x[1], x[6], x[7])
            rows.append(np.concatenate([basis(x[3]) - basis(x[2]), [0.0]])); ys.append(x[5] - x[4] + sn - bl[0][1])
        X = np.array(rows); y = np.array(ys)
        used = np.where(np.abs(X[:, :-1]).sum(0) > 0)[0]
        keep = list(used[1:]) + [X.shape[1] - 1]
        Xr = X[:, keep]
        coef = np.linalg.lstsq(Xr, y, rcond=None)[0]
        full = np.zeros(X.shape[1]); full[keep] = coef
        c = lambda h: float(basis(h)[:-1 if False else len(knots)] @ full[:len(knots)])
        parts = (c(g["half"]) - c(g["re"]), c(g["fill"]) - c(g["half"]), c(g["fill"]) - c(g["re"]))
        labels = ["reorder and half-full", "half-full and normal fill", "reorder and normal fill"]
        i = int(np.argmax(np.abs(parts)))
        call[tid] = (abs(parts[i]), labels[i])
    listed = sorted(t for t, v in call.items() if v[0] > limit)
    # A2: tests collapsed on the console's test number, dated by its own Sunday print or the weekly chain
    tests = {}
    for r in csv_rows(os.path.join(target, "atg_leak_tests_2026.csv")):
        tests.setdefault((r["console_sn"], r["tank"], int(r["test_no"])), []).append(r)
    chi = __import__("zoneinfo").ZoneInfo("America/Chicago")
    def L(s):
        return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(chi).replace(tzinfo=None)
    bycon = {}
    for key, rs in tests.items():
        rs.sort(key=lambda r: int(r["rec_id"]))
        bycon.setdefault(key[:2], []).append((key[2], rs[0]))
    passed = set()
    for (cs, tn), lst in bycon.items():
        anc = {}
        for no, r in lst:
            t = L(r["logged_utc"])
            if t.year == 2026 and t.weekday() == 6 and t.hour >= 21:
                anc[no] = t
        for no, r in lst:
            if no in anc:
                d = anc[no]
            else:
                prev = [a for a in anc if a < no]; nxt = [a for a in anc if a > no]
                d = (anc[max(prev)] + dt.timedelta(days=7 * (no - max(prev)))) if prev else (anc[min(nxt)] - dt.timedelta(days=7 * (min(nxt) - no)) if nxt else L(r["logged_utc"]))
            if d.year == 2026 and r["result"] == "PASS":
                passed.add((tid_of(cs, tn, d), d.month))
    A2 = {}
    for t, g in reg.items():
        A2[g["marina"]] = A2.get(g["marina"], 0) + sum(1 for mo in range(1, 13) if (t, mo) not in passed)
    # A3
    price = {}
    for r in leg:
        price[r["price"]] = {"REC-90 NE": "REC-90 ethanol-free", "E10 87": "E10 unleaded", "MARINE DSL": "Diesel"}[r["product"]]
    A3 = {}
    last_leg = max(dt.datetime.strptime(r["sale_time"], "%m/%d/%Y %H:%M:%S") for r in leg)
    for r in leg:
        key = "%s|%s" % (r["store_name"], price[r["price"]])
        A3[key] = A3.get(key, 0.0) + float(r["gallons"])
    grades = {(r["site"], r["grade"]): r["site_name"] for r in csv_rows(os.path.join(target, "pos_grades.csv"))}
    for line in open(os.path.join(target, "dock_sales_2026-11-09_2026-12-31.jsonl"), encoding="utf-8"):
        j = json.loads(line)
        t = L(j["ts"])
        sale_day = (t - dt.timedelta(days=1)).date() if j["tender"] == "CARD" else t.date()
        when = dt.datetime.combine(sale_day, dt.time(12)) if j["tender"] == "CARD" else t
        if when <= last_leg or sale_day.year != 2026:
            continue
        key = "%s|%s" % (grades[(j["site"], str(j["grade"]))], price["%.2f" % j["ppg"]])
        A3[key] = A3.get(key, 0.0) + float(j["gal"])
    return {"listed": listed, "pairs": {t: call[t][1] for t in listed}, "A1": A1, "A2": A2,
            "A3": {k: int(round(v)) for k, v in A3.items()}, "fs3_text": fs3}


def main(target, figures):
    v = compute(target)
    f = json.load(open(figures))
    fails = []
    def chk(label, cond):
        print(("PASS " if cond else "FAIL ") + label)
        if not cond:
            fails.append(label)
    chk("listed tanks recompute", v["listed"] == f["call"]["listed"])
    chk("count recomputes", len(v["listed"]) == f["call"]["count"])
    chk("each listed tank's heights recompute", v["pairs"] == f["call"]["pairs"])
    chk("A1 recomputes (20 tanks)", v["A1"] == f["A1"])
    chk("A2 recomputes (8 marinas)", v["A2"] == f["A2"])
    chk("A3 recomputes (marina x product)", v["A3"] == f["A3"])
    chk("PDF read back: FS-3 3.4 sentence", "must not misstate the change in stock between any two of its reorder, half-full and normal fill heights" in v["fs3_text"])
    lt = pdf_text(os.path.join(target, "wetstock_onboarding_2027.pdf"))
    chk("PDF read back: onboarding letter readiness sentence", "at least 355 of the days of 2026" in lt)
    gp = os.path.join(os.path.dirname(target), "golden", "cutover_readiness_2027.pdf")
    if os.path.exists(gp):
        gt = pdf_text(gp)
        chk("golden PDF read back: states the list", all(t in gt for t in f["call"]["listed"]))
    xr = xlsx_rows(os.path.join(target, "monthly_closeouts_2026.xlsx"))
    chk("XLSX read back: close-out sheet", any(r and r[0] == "Tank" for r in xr))
    chk("JSONL read back", sum(1 for _ in open(os.path.join(target, "dock_sales_2026-11-09_2026-12-31.jsonl"))) > 100)
    print("verify: %d failures" % len(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    figs = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "figures.json")
    sys.exit(main(tgt, figs))
