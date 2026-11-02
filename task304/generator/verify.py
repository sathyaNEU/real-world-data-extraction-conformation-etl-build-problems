"""task304 architecture 5: an independent verifier on its own code path. It reads every shipped format back with the
standard library (csv, zipfile and XML for the workbooks, zlib and ASCII85 for the PDFs, json), fits the negative
binomial performance function by a joint quasi-Newton maximisation (not the analysis's IRLS and profile search), and
recomputes every graded figure and the easy routes. It also reads the golden deck of files (docx XML, xlsx XML).
Exit 1 on a mismatch."""
import base64
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
import zlib
from collections import defaultdict
from xml.etree import ElementTree as ET

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FAILS = []
N_OK = [0]


def ok(label, cond, detail=""):
    if cond:
        N_OK[0] += 1
        print("PASS  " + label)
    else:
        FAILS.append(label)
        print("FAIL  " + label + ("  [" + detail + "]" if detail else ""))


def csv_rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    return r


def xlsx_sheet(path, sheet_name):
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == sheet_name:
            rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    target = [r.get("Target") for r in rels if r.get("Id") == rid][0]
    target = target.lstrip("/")
    target = target if target.startswith("xl/") else "xl/" + target
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    rows = []
    for row in ET.fromstring(z.read(target)).find("m:sheetData", NS):
        vals = {}
        for c in row:
            ref = c.get("r")
            col = re.match(r"[A-Z]+", ref).group(0)
            v = c.find("m:v", NS)
            if c.get("t") == "s":
                val = shared[int(v.text)]
            elif c.get("t") == "inlineStr":
                val = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
            else:
                val = v.text if v is not None else None
            vals[col] = val
        rows.append(vals)
    return rows


def col_index(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n - 1


def table(rows):
    head = rows[0]
    keys = sorted(head, key=col_index)
    names = [head[k] for k in keys]
    out = []
    for r in rows[1:]:
        out.append({names[i]: r.get(k) for i, k in enumerate(keys)})
    return out


def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[2:-2] if raw.startswith(b"<~") else raw[:-2])
            raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", raw, re.S):
            out.append(s.decode("latin-1").replace("\\(", "(").replace("\\)", ")"))
    return " ".join(out)


def nb_joint(X, y):
    p = X.shape[1]

    def nll(th):
        b, la = th[:p], th[p]
        a = np.exp(la)
        mu = np.exp(np.clip(X @ b, -30, 30))
        r = 1 / a
        return -(gammaln(y + r) - gammaln(r) - gammaln(y + 1) + r * np.log(r / (r + mu)) + y * np.log(mu / (r + mu))).sum()

    def grad(th):
        b, la = th[:p], th[p]
        a = np.exp(la)
        mu = np.exp(np.clip(X @ b, -30, 30))
        gb = X.T @ ((y - mu) / (1 + a * mu))
        r = 1 / a
        from scipy.special import digamma
        dl_dr = (digamma(y + r) - digamma(r) + np.log(r / (r + mu)) + 1 - (r + y) / (r + mu)).sum()
        ga = dl_dr * (-1 / a ** 2) * a
        return -np.r_[gb, ga]
    th0 = np.zeros(p + 1)
    th0[0] = np.log(y.mean())
    th0[p] = np.log(0.5)
    res = minimize(nll, th0, jac=grad, method="L-BFGS-B", options={"maxiter": 20000, "gtol": 1e-9, "ftol": 1e-15})
    return res.x[:p], float(np.exp(res.x[p]))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    inv = table(xlsx_sheet(os.path.join(T, "junction_inventory_2026.xlsx"), "Junctions"))
    nodes = {r["node"]: r for r in inv}
    former = {r["former_node"]: r["node"] for r in inv if r["former_node"]}
    rec = csv_rows("collision_records_2016_2025.csv")
    counts = defaultdict(int)
    for r in rec:
        nd = r["junction_node"].strip()
        if nd:
            counts[(former.get(nd, nd), int(r["collision_date"][-4:]))] += 1
    win = [2021, 2022, 2023, 2024, 2025]
    ref = [n for n, r in nodes.items() if r["layout"] in ("T", "ST", "X") and r["control"] in ("GW", "STOP")]
    txt_s = pdf_strings(os.path.join(T, "network_screening_2026.pdf"))
    listed = [n for n in re.findall(r"J\d{4}", txt_s) if n in nodes]
    rule = sorted(n for n in ref if sum(counts[(n, y)] for y in win) >= 12)
    ok("V1 the screening note's junctions are the record's junctions with 12 or more collisions in 2021 to 2025",
       sorted(listed) == rule and len(listed) == 6)
    txt_g = " ".join(pdf_strings(os.path.join(T, "junction_safety_fund_guidance_2027.pdf")).split())
    cx = float(re.search(r"Crossroads \(four arms\) (\d\.\d\d)", txt_g).group(1))
    ct = float(re.search(r"T junction or staggered junction (\d\.\d\d)", txt_g).group(1))
    cmf = {"X": cx, "T": ct, "ST": ct}
    ok("V2 the guidance files the window 2021 to 2025 and the 2026 traffic", "2021 to 2025" in txt_g and "2026 traffic" in txt_g)
    # design: intercept, X, ST, ln maj, ln min, year 2022..2025
    rows, y = [], []
    for n in ref:
        r = nodes[n]
        for yr in win:
            rows.append([1.0, r["layout"] == "X", r["layout"] == "ST", np.log(float(r["aadt_major_%d" % yr])),
                         np.log(float(r["aadt_minor_%d" % yr]))] + [1.0 if yr == k else 0.0 for k in win[1:]])
            y.append(counts[(n, yr)])
    X = np.array(rows, dtype=float)
    yv = np.array(y, dtype=float)
    b, a = nb_joint(X, yv)
    ok("V3 the overdispersion recomputes (%.3f)" % a, abs(round(a, 2) - F["overdispersion"]) <= 0.01)

    def mu(n, yr, level):
        r = nodes[n]
        x = [1.0, r["layout"] == "X", r["layout"] == "ST", np.log(float(r["aadt_major_%d" % yr])),
             np.log(float(r["aadt_minor_%d" % yr]))] + [1.0 if level == k else 0.0 for k in win[1:]]
        return float(np.exp(np.array(x, dtype=float) @ b))
    ben, exp_, obs_b, spf_b = {}, {}, {}, {}
    for n in listed:
        r = nodes[n]
        mus = [mu(n, yr, yr) for yr in win]
        m26 = np.mean([mu(n, 2026, lv) for lv in win])
        o = sum(counts[(n, yr)] for yr in win)
        w = 1 / (1 + a * sum(mus))
        e = (w * sum(mus) + (1 - w) * o) / sum(mus) * m26
        name = r["junction_name"]
        exp_[name] = e
        ben[name] = e * (1 - cmf[r["layout"]])
        obs_b[name] = o / 5 * (1 - cmf[r["layout"]])
        spf_b[name] = m26 * (1 - cmf[r["layout"]])
    r1 = lambda v: float("%.1f" % (v + 1e-9))  # noqa: E731
    ok("V4 every listed junction's benefit recomputes at one decimal", all(r1(ben[k]) == F["benefit"][k] for k in ben),
       str({k: round(v, 3) for k, v in ben.items()}))
    best = max(ben, key=ben.get)
    ok("V5 the call recomputes: %s" % best, best == F["call"])
    ok("V6 the call's expected annual collisions recompute (%.3f)" % exp_[best], r1(exp_[best]) == F["call_expected"])
    ok("V7 the cluster-site route files %s" % max(obs_b, key=obs_b.get), max(obs_b, key=obs_b.get) == F["observed_route"] != best)
    ok("V8 the model alone files %s" % max(spf_b, key=spf_b.get), max(spf_b, key=spf_b.get) == F["model_route"] != best)

    # ---------------- the annex, on its own code path
    east = {r["node"]: int(r["easting"]) for r in inv}
    reg = csv_rows("road_network_register_2026.csv")
    secs = defaultdict(list)
    for r in reg:
        e0, e1 = sorted((east[r["from_node"]], east[r["to_node"]]))
        secs[r["road_number"]].append((e0, e1, r["highway_authority"]))

    def county(road, e):
        s = sorted(secs.get(road, []))
        if not s:
            return True
        for i, (e0, e1, auth) in enumerate(s):
            lo = -1e18 if i == 0 else e0
            hi = 1e18 if i == len(s) - 1 else e1
            if lo <= e < hi:
                return auth == "Ardleshire County Council"
        return True
    old = {}
    for r in csv_rows("police_collisions_2026_jan_may.csv"):
        d = dt.datetime.strptime(r["collision_date"] + " " + r["collision_time"], "%d/%m/%Y %H:%M")
        old[r["accident_ref"]] = dict(t=d, e=int(r["easting"]), n=int(r["northing"]), road=r["first_road"], cas=[])
    groups = {"Pedestrian", "Pedal cyclist", "Motorcyclist", "Car occupant"}
    for r in csv_rows("police_casualties_2026_jan_may.csv"):
        old[r["accident_ref"]]["cas"].append([int(r["casualty_severity"]), "M" if r["sex"] == "1" else "F", int(r["age"]),
                                              r["casualty_type"] if r["casualty_type"] in groups else None])
    vg = {"Car": "Car occupant", "Taxi or private hire car": "Car occupant", "Pedal cycle": "Pedal cyclist",
          "Motorcycle 125cc and under": "Motorcyclist", "Motorcycle 125cc to 500cc": "Motorcyclist",
          "Motorcycle over 500cc": "Motorcyclist"}
    sev = {"Fatal": 1, "Serious": 2, "Slight": 3}
    new = []
    for c in json.load(open(os.path.join(T, "police_export_2026_jun_sep.json"), encoding="utf-8"))["collisions"]:
        t = dt.datetime.strptime(c["occurred"][:16], "%Y-%m-%dT%H:%M")
        vt = {v["vehicle"]: v["type"] for v in c["vehicles"]}
        new.append(dict(t=t, e=c["easting"], n=c["northing"], road=c["road"],
                        cas=[[sev[k["severity"]], k["sex"], k["age"],
                              "Pedestrian" if k["class"] == "Pedestrian" else vg.get(vt[k["vehicle"]])] for k in c["casualties"]]))
    drop = set()
    for c in new:
        if c["t"] >= dt.datetime(2026, 6, 1):
            continue
        hit = [k for k, o in old.items() if o["road"] == c["road"] and o["t"].date() == c["t"].date()
               and abs((o["t"] - c["t"]).total_seconds()) <= 1200 and ((o["e"] - c["e"]) ** 2 + (o["n"] - c["n"]) ** 2) <= 1600]
        if len(hit) == 1:
            drop.add(hit[0])
    allc = [o for k, o in old.items() if k not in drop] + new
    notes = table(xlsx_sheet(os.path.join(T, "fatal_casualty_notifications_2026.xlsx"), "Notifications 2026"))
    for r in notes:
        cd = dt.datetime.strptime(r["collision_date"], "%d/%m/%Y")
        dd = dt.datetime.strptime(r["date_of_death"], "%d/%m/%Y")
        if (dd - cd).days > 30:
            continue
        tt = dt.datetime.strptime(r["collision_date"] + " " + r["approx_time"], "%d/%m/%Y %H:%M")
        sx = "M" if r["casualty_sex"] == "Male" else "F"
        cands = [c for c in allc if c["road"] == r["road"] and c["t"].date() == cd.date() and abs((c["t"] - tt).total_seconds()) <= 1800
                 and any(k[1] == sx and k[2] == int(float(r["casualty_age"])) for k in c["cas"])]
        if len(cands) == 1:
            for k in cands[0]["cas"]:
                if k[1] == sx and k[2] == int(float(r["casualty_age"])):
                    k[0] = 1
                    break
    A = defaultdict(int)
    B = defaultdict(int)
    for c in allc:
        if not county(c["road"], c["e"]):
            continue
        q = (c["t"].month - 1) // 3 + 1
        A[(q, min(k[0] for k in c["cas"]))] += 1
        for k in c["cas"]:
            if k[3]:
                B[(q, k[3])] += 1
    sname = {1: "Fatal", 2: "Serious", 3: "Slight"}
    ok("V9 annex A1 recomputes in all nine cells", all(A[(q, s)] == F["ask_a"]["Q%d" % q][sname[s]] for q in (1, 2, 3) for s in (1, 2, 3)),
       str(dict(A)))
    ok("V10 annex A2 recomputes in all twelve cells", all(B[(q, g)] == F["ask_b"]["Q%d" % q][g] for q in (1, 2, 3) for g in groups),
       str(dict(B)))

    # ---------------- the goldens
    z = zipfile.ZipFile(os.path.join(G, "junction_bid_2027.docx"))
    doc = re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf-8"))
    doc = " ".join(doc.split())
    ok("V11 the bid document names the junction chosen in its title line", F["call"] in doc[:400])
    ok("V12 the bid document's table carries every listed junction's benefit",
       all(re.search(re.escape(k) + r" .{0,40}?%.1f" % v, doc) for k, v in F["benefit"].items()))
    ok("V13 the bid document embeds the chart", any(n.startswith("word/media/") for n in z.namelist()))
    a1 = xlsx_sheet(os.path.join(G, "bid_annex_2026.xlsx"), "A1 Collisions by severity")
    a2 = xlsx_sheet(os.path.join(G, "bid_annex_2026.xlsx"), "A2 Casualties by road user")
    def qrow(rows, q, cols):
        r = [x for x in rows if (x.get("A") or "").startswith("Q%d 2026" % q)][0]
        return [r[c] for c in cols]
    v1 = [qrow(a1, q, "BCD") for q in (1, 2, 3)]
    v2 = [qrow(a2, q, "BCDE") for q in (1, 2, 3)]
    ok("V14 the annex workbook's A1 and A2 tables carry the annex figures",
       all(int(v1[q - 1][j]) == F["ask_a"]["Q%d" % q][s] for q in (1, 2, 3) for j, s in enumerate(["Fatal", "Serious", "Slight"]))
       and all(int(v2[q - 1][j]) == F["ask_b"]["Q%d" % q][g] for q in (1, 2, 3)
               for j, g in enumerate(["Pedestrian", "Pedal cyclist", "Motorcyclist", "Car occupant"])))
    print("%d checks, %d FAIL" % (N_OK[0] + len(FAILS), len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
