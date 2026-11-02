"""Independent re-computation of every graded figure from target/, on its own readers and its own fits.
Run: python3 verify.py <target_dir> <figures.json>"""
import base64
import csv
import json
import math
import os
import re
import sys
import zipfile
import zlib
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

import numpy as np
from scipy import optimize, stats

BRU = ZoneInfo("Europe/Brussels")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


# ------------------------------------------------------------------ readers
def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find("m:sheets", NS):
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rmap[rid].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(z.read(target))
        rows = []
        for row in root.iter("{%s}row" % NS["m"]):
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
                else:
                    val = v.text if v is not None else None
                vals[col - 1] = val
            n = max(vals) + 1 if vals else 0
            rows.append([vals.get(i) for i in range(n)])
        out[sh.get("name")] = rows
    return out


def pdf_strings(path):
    data = open(path, "rb").read()
    txt = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1)
        hdr = data[max(0, m.start() - 300):m.start()]
        try:
            if b"ASCII85Decode" in hdr:
                body = raw.strip()
                if body.endswith(b"~>"):
                    body = body[:-2]
                if body.startswith(b"<~"):
                    body = body[2:]
                raw = base64.a85decode(body)
            if b"FlateDecode" in hdr:
                raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", raw):
            s = s.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
            txt.append(s.decode("latin-1"))
    return " ".join(txt)


def rows(path, delim=","):
    with open(path, encoding="utf-8", newline="") as f:
        body = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(body, delimiter=delim))


# ------------------------------------------------------------------ fits
def within_hour_slope(lrr, lqt, hour):
    levels = sorted(set(hour.tolist()))
    X = np.column_stack([lrr] + [(hour == h).astype(float) for h in levels])
    return float(np.linalg.lstsq(X, lqt, rcond=None)[0][0])


def reml(y, X, Z, g):
    groups = sorted(set(g.tolist()))
    idx = [np.where(g == k)[0] for k in groups]
    n, p = X.shape

    def nll(th):
        s0, s1, rho, ls = math.exp(th[0]), math.exp(th[1]), math.tanh(th[2]), th[3]
        G = np.array([[s0 * s0, rho * s0 * s1], [rho * s0 * s1, s1 * s1]])
        se2 = math.exp(ls)
        A = np.zeros((p, p))
        bvec = np.zeros(p)
        ld = 0.0
        Vi = []
        for ii in idx:
            V = Z[ii] @ G @ Z[ii].T + se2 * np.eye(len(ii))
            Vinv = np.linalg.inv(V)
            Vi.append(Vinv)
            ld += np.linalg.slogdet(V)[1]
            A += X[ii].T @ Vinv @ X[ii]
            bvec += X[ii].T @ Vinv @ y[ii]
        beta = np.linalg.solve(A, bvec)
        q = sum(float((y[ii] - X[ii] @ beta) @ Vinv @ (y[ii] - X[ii] @ beta)) for ii, Vinv in zip(idx, Vi))
        return 0.5 * (ld + np.linalg.slogdet(A)[1] + q), beta, np.linalg.inv(A)
    best = None
    for start in ([1.0, 1.0, 0.0, 3.0], [0.0, 0.0, 0.0, 3.5], [1.5, 2.0, 0.3, 2.5]):
        r = optimize.minimize(lambda th: nll(th)[0], start, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    _, beta, cov = nll(best.x)
    return beta, cov


def nca_auc(pts):
    pts = sorted(pts)
    t = [p[0] for p in pts]
    c = [p[1] for p in pts]
    fq = next(i for i, v in enumerate(c) if v > 0)
    keep = [i for i in range(len(c)) if i <= fq or c[i] > 0]
    t = [t[i] for i in keep]
    c = [c[i] for i in keep]
    last = max(i for i, v in enumerate(c) if v > 0)
    auc = 0.0
    for i in range(last):
        dt = t[i + 1] - t[i]
        if 0 < c[i + 1] < c[i]:
            auc += dt * (c[i] - c[i + 1]) / math.log(c[i] / c[i + 1])
        else:
            auc += dt * (c[i] + c[i + 1]) / 2
    imax = c.index(max(c))
    cand = [i for i in range(imax + 1, last + 1) if c[i] > 0]
    best = None
    for k in range(3, len(cand) + 1):
        sel = cand[-k:]
        x = np.array([t[i] for i in sel])
        yv = np.log([c[i] for i in sel])
        slope, icpt, r, _, _ = stats.linregress(x, yv)
        adj = 1 - (1 - r * r) * (k - 1) / (k - 2)
        if best is None or adj > best[0] - 1e-4:
            best = (adj, -slope)
    return auc + c[last] / best[1]


def sig(x, n):
    e = math.floor(math.log10(abs(x))) - (n - 1)
    return int(round(x / 10 ** e) * 10 ** e) if e >= 0 else round(round(x / 10 ** e) * 10 ** e, -e)


# ------------------------------------------------------------------ main
def main(target, figs_path):
    figs = json.load(open(figs_path))
    fails = []
    f = {k: os.path.join(target, v) for k, v in {
        "holter": "holter_5min_segments_VLT317-101-102.txt", "e1": "corelab_ecg_VLT317-101_transfer3.xlsx",
        "e2": "corelab_ecg_VLT317-102_transfer2.csv", "pk": "bioanalysis_plasma_VLT317-101-102.csv",
        "amb": "ambulatory_lab_results_2026.csv", "dose": "dosing_log_VLT317-101-102.csv",
        "rand": "randomisation_unblinded_VLT317-101-102.xlsx", "scr": "screening_log_2026.csv",
        "ddi": "VLT-317-103_CSR_synopsis.pdf", "plan": "VLT-317_CQTc_analysis_plan_v2.0.pdf"}.items()}
    ddi = pdf_strings(f["ddi"])
    m = re.search(r"Cmax \(ng/mL\), geometric mean\s+[\d.]+\s+[\d.]+\s+([\d.]+) \(", ddi)
    gmr = float(m.group(1)) if m else float("nan")
    plan = pdf_strings(f["plan"])
    if "below 10 ms" not in plan:
        fails.append("plan PDF unreadable")
    subj = {}
    for name, rws in xlsx_sheets(f["rand"]).items():
        for r in rws[1:]:
            subj[int(float(r[1]))] = dict(study=name[-3:], scr=r[2], dose=int(float(r[4])), act=r[5] == "VLT-317")
    scr = {v["scr"]: k for k, v in subj.items()}
    dose = {}
    for r in rows(f["dose"]):
        dose[(int(r["SUBJECT"]), int(r["STUDY_DAY"]))] = datetime.strptime(
            r["DOSE_DATE"] + r["DOSE_TIME"], "%Y-%m-%d%H:%M:%S").replace(tzinfo=BRU)
    conc = {}
    for r in rows(f["pk"]):
        if r["RESULT_NG_ML"] == ">ULOQ":
            continue
        v = 0.0 if r["RESULT_NG_ML"].startswith("BLQ") else float(r["RESULT_NG_ML"])
        conc[(int(r["SUBJECT"]), int(r["STUDY_DAY"]), float(r["NOMINAL_H"]))] = (
            v, datetime.strptime(r["COLLECTED"], "%d/%m/%Y %H:%M").replace(tzinfo=BRU))
    ecg = {}
    sh = xlsx_sheets(f["e1"])["Intervals"]
    H = sh[0]
    for r in sh[1:]:
        d = dict(zip(H, r))
        key = (scr[d["SCREENING_NO"]], int(d["VISIT"].split()[1]), float(d["NOMINAL_H"]))
        ecg[key] = [(float(d["RR_%d" % i]), float(d["QT_%d" % i])) for i in (1, 2, 3)
                    if d["QT_%d" % i] not in (None, "") and (d["READ_%d" % i] or "") != "U"]
    for r in rows(f["e2"]):
        key = (scr[r["SCRNO"]], int(r["VISIT"].split()[1]), float(r["TPT"][:-1].replace("P", ".")))
        ecg.setdefault(key, [])
        if r["QT"] and not r["EGSTAT"]:
            ecg[key].append((60000.0 / float(r["HR"]), float(r["QT"])))
    # Holter
    seg = {}
    for r in rows(f["holter"], "\t"):
        seg.setdefault(r["RecordingID"], []).append(r)
    own = {}
    for rid, L in seg.items():
        digits = re.findall(r"\d{4}", L[0]["PatientID"])
        if digits:
            own[rid] = int(digits[-1])

    def ts(r):
        return datetime.strptime(r["SegmentStart_UTC"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    expo = {}
    for rid, sid in own.items():
        t1 = dose[(sid, 1)]
        x, y, hh = [], [], []
        for r in seg[rid]:
            if not r["RR_ms"]:
                continue
            t = ts(r)
            if t + timedelta(seconds=int(r["Dur_s"])) > t1:
                continue
            x.append(math.log(float(r["RR_ms"])))
            y.append(math.log(float(r["QT_ms"])))
            hh.append(t.astimezone(BRU).hour)
        expo[sid] = within_hour_slope(np.array(x), np.array(y), np.array(hh))
    # model
    times = [0.5, 1, 2, 3, 4, 6, 8, 12, 24]
    qc = {k: np.mean([qt / (rr / 1000.0) ** expo[k[0]] for rr, qt in v]) for k, v in ecg.items() if v}
    base = {s: np.mean([qc[(s, -1, t)] for t in times if (s, -1, t) in qc]) for s in subj}
    mb = np.mean(list(base.values()))
    Y, X, Z, Gs = [], [], [], []
    for (s, d, t), v in sorted(qc.items()):
        if d == -1 or (s, -1, t) not in qc:
            continue
        c = conc[(s, d, t)][0]
        Y.append(v - qc[(s, -1, t)])
        X.append([1, int(subj[s]["act"]), c] + [float(t == tt) for tt in times[1:]] + [base[s] - mb])
        Z.append([1, c / 1000.0])
        Gs.append(s)
    Y, X, Z, Gs = map(np.array, (Y, X, Z, Gs))
    beta, cov = reml(Y, X, Z, Gs)
    ch = {}
    for dd in (25, 50, 100):
        cm = [max(v[0] for k, v in conc.items() if k[0] == s and k[1] == 10) for s, x in subj.items()
              if x["study"] == "102" and x["act"] and x["dose"] == dd]
        ch[dd] = gmr * math.exp(np.mean(np.log(cm)))
    q = stats.t.ppf(0.95, len(Y) - X.shape[1])
    ub = {}
    for dd in (25, 50, 100):
        x0 = np.zeros(X.shape[1])
        x0[1], x0[2] = 1, ch[dd]
        ub[dd] = float(x0 @ beta + q * math.sqrt(x0 @ cov @ x0))
    call = max([d for d in ub if ub[d] < 10], default=0)
    if call != figs["call_mg"]:
        fails.append("call %s vs %s" % (call, figs["call_mg"]))
    for dd in (25, 50, 100):
        if sig(ch[dd], 3) != figs["c_high_%d" % dd]:
            fails.append("C_high %d: %s vs %s" % (dd, sig(ch[dd], 3), figs["c_high_%d" % dd]))
        if ("yes" if ub[dd] < 10 else "no") != figs["below10_%d" % dd]:
            fails.append("below10 %d" % dd)
    # ask A
    xw = {}
    for r in rows(f["scr"]):
        if r["SCREENING_NO"] in scr:
            xw[(r["VOLUNTEER_NO"], r["PROTOCOL"])] = scr[r["SCREENING_NO"]]
    late = {}
    for r in rows(f["amb"]):
        if r["TEST"].startswith("VLT-317"):
            s = xw[(r["VOLUNTEER_NO"], r["PROTOCOL"])]
            t = datetime.strptime(r["VISIT_DATE"] + " " + r["DRAW_TIME"], "%Y-%m-%d %H:%M").replace(tzinfo=BRU)
            late.setdefault(s, []).append((t, 0.0 if r["RESULT"].startswith("BLQ") else float(r["RESULT"])))
    for dd in (25, 50, 100, 200, 400):
        vals = []
        for s, x in subj.items():
            if x["study"] != "101" or not x["act"] or x["dose"] != dd:
                continue
            t0 = dose[(s, 1)]
            pts = [(0.0 if k[2] == 0 else (v[1] - t0).total_seconds() / 3600, v[0]) for k, v in conc.items()
                   if k[0] == s and k[1] == 1]
            pts += [((t - t0).total_seconds() / 3600, c) for t, c in late[s]]
            vals.append(nca_auc(pts))
        g = math.exp(np.mean(np.log(vals)))
        if sig(g, 2) != figs["auc_sad_%d" % dd]:
            fails.append("AUC %d: %s vs %s" % (dd, sig(g, 2), figs["auc_sad_%d" % dd]))
    # ask B
    stop = {rid: max(ts(r) + timedelta(seconds=int(r["Dur_s"])) for r in seg[rid]) for rid in own}
    who = dict(own)
    for rid, L in seg.items():
        if rid in own:
            continue
        on = min(ts(r) for r in L if int(r["Beats"]) > 0)
        who[rid] = own[min(stop, key=lambda k: abs((stop[k] - on).total_seconds()))]
    night = {}
    for rid, L in seg.items():
        s = who[rid]
        d1 = dose[(s, 1)].date()
        for r in L:
            if not r["HR_bpm"]:
                continue
            tl = ts(r).astimezone(BRU)
            if tl.hour < 6:
                k = (tl.date() - d1).days
                if k in (0, 1):
                    night.setdefault((s, k), []).append(float(r["HR_bpm"]))
    chg = {s: np.mean(night[(s, 1)]) - np.mean(night[(s, 0)]) for s in subj}
    for study, doses in (("101", (25, 50, 100, 200, 400)), ("102", (25, 50, 100))):
        pl = np.mean([chg[s] for s, x in subj.items() if x["study"] == study and not x["act"]])
        for dd in doses:
            v = np.mean([chg[s] for s, x in subj.items() if x["study"] == study and x["act"] and x["dose"] == dd]) - pl
            if round(v + 0.0, 1) != figs["night_hr_%s_%d" % (study, dd)]:
                fails.append("night HR %s %d: %.3f vs %s" % (study, dd, v, figs["night_hr_%s_%d" % (study, dd)]))
    print("verify: call %d, UB %s, C_high %s, GMR %.2f" % (call, {k: round(v, 2) for k, v in ub.items()},
                                                          {k: round(v, 1) for k, v in ch.items()}, gmr))
    for x in fails:
        print("MISMATCH", x)
    print("VERIFY %s" % ("PASS" if not fails else "FAIL"))
    return len(fails)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2]) else 0)
