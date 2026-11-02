"""The golden analysis, the ladder and the asks, computed from target/ alone."""
import csv
import math
import os
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl

import cqtc
from pack import FILES

BRU = ZoneInfo("Europe/Brussels")
UTC = timezone.utc
ECG_TIMES = [0.5, 1, 2, 3, 4, 6, 8, 12, 24]
PH2B = [25, 50, 100]
GMR = 2.61                       # read from the synopsis PDF below and asserted equal


def _csv(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines, delimiter=delimiter))


def _local(s, fmt):
    return datetime.strptime(s, fmt).replace(tzinfo=BRU)


def conc_value(txt):
    if txt in ("BLQ", "") or txt.startswith("BLQ"):
        return 0.0
    return float(txt)


def load(target):
    D = {}
    # randomisation
    wb = openpyxl.load_workbook(os.path.join(target, FILES["rand"]), read_only=True)
    subj = {}
    for ws in wb.worksheets:
        study = ws.title.split("-")[-1]
        rows = list(ws.iter_rows(values_only=True))
        for r in rows[1:]:
            subj[int(r[1])] = dict(subject=int(r[1]), study=study, cohort=int(r[0]), screening=r[2],
                                   dose=int(r[4]), active=(r[5] == "VLT-317"))
    D["subj"] = subj
    scr2sub = {v["screening"]: k for k, v in subj.items()}
    # dosing
    doses = {}
    for r in _csv(os.path.join(target, FILES["dosing"])):
        t = _local(r["DOSE_DATE"] + " " + r["DOSE_TIME"], "%Y-%m-%d %H:%M:%S")
        doses.setdefault(int(r["SUBJECT"]), {})[int(r["STUDY_DAY"])] = t
    D["doses"] = doses
    # plasma (re-assay replaces an above-range original)
    pk = {}
    for r in _csv(os.path.join(target, FILES["plasma"])):
        key = (int(r["SUBJECT"]), int(r["STUDY_DAY"]), float(r["NOMINAL_H"]))
        if r["RESULT_NG_ML"] == ">ULOQ":
            continue
        pk[key] = dict(c=conc_value(r["RESULT_NG_ML"]), t=_local(r["COLLECTED"], "%d/%m/%Y %H:%M"))
    D["pk"] = pk
    # ECG study 101 (wide)
    ecg = {}
    wb = openpyxl.load_workbook(os.path.join(target, FILES["ecg101"]), read_only=True)
    ws = wb["Intervals"]
    rows = list(ws.iter_rows(values_only=True))
    h = rows[0]
    ix = {k: i for i, k in enumerate(h)}
    for r in rows[1:]:
        sid = scr2sub[r[ix["SCREENING_NO"]]]
        day = int(str(r[ix["VISIT"]]).split()[-1])
        reps = []
        for i in (1, 2, 3):
            qt = r[ix["QT_%d" % i]]
            if r[ix["READ_%d" % i]] == "U" or qt in (None, ""):
                continue
            reps.append((float(r[ix["RR_%d" % i]]), float(qt)))
        ecg[(sid, day, float(r[ix["NOMINAL_H"]]))] = reps
    # ECG study 102 (long, heart rate)
    for r in _csv(os.path.join(target, FILES["ecg102"])):
        sid = scr2sub[r["SCRNO"]]
        day = int(r["VISIT"].split()[-1])
        nt = float(r["TPT"].rstrip("H").replace("P", "."))
        ecg.setdefault((sid, day, nt), [])
        if r["QT"] == "" or r["EGSTAT"]:
            continue
        ecg[(sid, day, nt)].append((60000.0 / float(r["HR"]), float(r["QT"])))
    D["ecg"] = ecg
    # Holter segments
    seg = []
    for r in _csv(os.path.join(target, FILES["holter"]), delimiter="\t"):
        t = datetime.strptime(r["SegmentStart_UTC"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        seg.append(dict(rec=r["RecordingID"], pid=r["PatientID"].strip(), start=t, dur=int(r["Dur_s"]),
                        beats=int(r["Beats"]), hr=float(r["HR_bpm"]) if r["HR_bpm"] else None,
                        rr=float(r["RR_ms"]) if r["RR_ms"] else None, qt=float(r["QT_ms"]) if r["QT_ms"] else None,
                        noise=int(r["Noise_pct"])))
    D["seg"] = seg
    # screening log and ambulatory visits
    D["screen"] = _csv(os.path.join(target, FILES["screen"]))
    D["amb"] = _csv(os.path.join(target, FILES["amb"]))
    return D


# ------------------------------------------------------------------ recordings to subjects
def recordings(D):
    recs = {}
    for g in D["seg"]:
        recs.setdefault(g["rec"], []).append(g)
    owner = {}
    labelled = {}
    for rid, L in recs.items():
        p = L[0]["pid"]
        if p:
            m = re.findall(r"\d{4}", p)
            owner[rid] = int(m[-1])
            labelled[rid] = L
    stops = {rid: max(g["start"] + timedelta(seconds=g["dur"]) for g in L) for rid, L in labelled.items()}
    pairing = {}
    margin = []
    for rid, L in recs.items():
        if rid in owner:
            continue
        first = min(g["start"] for g in L if g["beats"] > 0)       # the segment it was put on in
        d = sorted((abs((first - st).total_seconds()), r1) for r1, st in stops.items()
                   if abs((first - st).total_seconds()) < 6 * 3600)
        pairing[rid] = owner[d[0][1]]
        margin.append(d[1][0] / max(d[0][0], 1.0))
    return recs, owner, pairing, min(margin)


def drug_free(D, recs, owner, cut="actual"):
    out = {}
    for rid, L in recs.items():
        if rid not in owner:
            continue
        sid = owner[rid]
        if cut == "actual":
            tdose = D["doses"][sid][1]
        else:                                  # nominal 08:00 on the dosing day
            d1 = D["doses"][sid][1].astimezone(BRU)
            tdose = datetime(d1.year, d1.month, d1.day, 8, 0, tzinfo=BRU)
        rows = []
        for g in L:
            if g["rr"] is None:
                continue
            if g["start"] + timedelta(seconds=g["dur"]) > tdose:
                continue
            tl = g["start"].astimezone(BRU)
            rows.append((tl.hour + tl.minute / 60 + tl.second / 3600, g["rr"], g["qt"],
                         g["start"].hour + g["start"].minute / 60))
        out[sid] = np.array(rows)
    return out


def exponents(df, method, clock="local"):
    res = {}
    for sid, a in df.items():
        ck = a[:, 0] if clock == "local" else a[:, 3]
        res[sid] = cqtc.exponent(np.log(a[:, 1]), np.log(a[:, 2]), ck, method)
    return res


# ------------------------------------------------------------------ the concentration-QTc model
def c_high(D, gmr=GMR):
    out = {}
    for dose in PH2B:
        v = []
        for sid, s in D["subj"].items():
            if s["study"] == "102" and s["active"] and s["dose"] == dose:
                v.append(max(x["c"] for k, x in D["pk"].items() if k[0] == sid and k[1] == 10))
        out[dose] = gmr * float(np.exp(np.mean(np.log(v))))
    return out


def qtc_table(D, scheme, b=None):
    val = {}
    for key, reps in D["ecg"].items():
        if not reps:
            continue
        bb = b[key[0]] if isinstance(b, dict) else b
        val[key] = float(np.mean([cqtc.corrected(qt, rr, scheme, bb) for rr, qt in reps]))
    return val


def model_rows(D, val):
    base = {}
    for sid in D["subj"]:
        v = [val[(sid, -1, t)] for t in ECG_TIMES if (sid, -1, t) in val]
        base[sid] = float(np.mean(v))
    rows = []
    for (sid, day, nt), v in sorted(val.items()):
        if day == -1 or (sid, -1, nt) not in val:
            continue
        rows.append(dict(subject=sid, trt=int(D["subj"][sid]["active"]), conc=D["pk"][(sid, day, nt)]["c"],
                         nominal=nt, dq=v - val[(sid, -1, nt)]))
    return rows, base


def run_cqtc(D, scheme, b=None, slope=True, basecov=True, df="residual", ch=None):
    val = qtc_table(D, scheme, b)
    rows, base = model_rows(D, val)
    m = cqtc.fit(rows, base, slope=slope, baseline_cov=basecov)
    ch = ch or c_high(D)
    pred = {d: cqtc.predict(m, ch[d], df) for d in PH2B}
    ubs = {d: pred[d][1] for d in PH2B}
    return dict(model=m, pred=pred, ubs=ubs, call=cqtc.highest_passing(ubs), n=len(rows))


# ------------------------------------------------------------------ ask A: SAD AUC0-inf
def crosswalk(D):
    """volunteer number + protocol -> subject, through the screening log and the randomisation list."""
    scr2sub = {v["screening"]: k for k, v in D["subj"].items()}
    out = {}
    for r in D["screen"]:
        if r["SCREENING_NO"] in scr2sub:
            out[(r["VOLUNTEER_NO"], r["PROTOCOL"])] = scr2sub[r["SCREENING_NO"]]
    return out


def nca(pts, trap="linlog", lz="adjr2"):
    pts = sorted(pts)
    t = np.array([p[0] for p in pts])
    c = np.array([p[1] for p in pts])
    first_q = np.where(c > 0)[0][0]
    keep = [i for i in range(len(c)) if i <= first_q or c[i] > 0]
    t, c = t[keep], c[keep]
    last = np.where(c > 0)[0][-1]
    auc = 0.0
    for i in range(last):
        dt = t[i + 1] - t[i]
        if trap == "linlog" and c[i + 1] < c[i] and c[i + 1] > 0:
            auc += dt * (c[i] - c[i + 1]) / math.log(c[i] / c[i + 1])
        else:
            auc += dt * (c[i] + c[i + 1]) / 2
    imax = int(np.argmax(c))
    cand = [i for i in range(imax + 1, last + 1) if c[i] > 0]

    def fitk(idx):
        tt = t[idx]
        cc = np.log(c[idx])
        bb, aa = np.polyfit(tt, cc, 1)
        pred = aa + bb * tt
        ss = ((cc - pred) ** 2).sum()
        st = ((cc - cc.mean()) ** 2).sum()
        r2 = 1 - ss / st
        n = len(idx)
        return -bb, 1 - (1 - r2) * (n - 1) / (n - 2)
    if lz == "adjr2":
        best = None
        for k in range(3, len(cand) + 1):
            lam, adj = fitk(cand[-k:])
            if best is None or adj > best[1] - 1e-4:
                best = (lam, adj)
        lam = best[0]
    elif lz == "last3":
        lam = fitk(cand[-3:])[0]
    else:
        lam = fitk([i for i in cand if t[i] >= 47])[0]
    return auc + c[last] / lam, lam


def ask_a(D, use_late=True, times="actual", trap="linlog", lz="adjr2", xw=None):
    xw = crosswalk(D) if xw is None else xw
    late = {}
    if use_late:
        for r in D["amb"]:
            if r["TEST"] != "VLT-317 (plasma)":
                continue
            sid = xw.get((r["VOLUNTEER_NO"], r["PROTOCOL"]))
            if sid is None:
                continue
            t = _local(r["VISIT_DATE"] + " " + r["DRAW_TIME"], "%Y-%m-%d %H:%M")
            late.setdefault(sid, []).append((t, conc_value(r["RESULT"]), int(r["VISIT"].split()[-1])))
    per = {}
    for sid, s in D["subj"].items():
        if s["study"] != "101" or not s["active"]:
            continue
        t0 = D["doses"][sid][1]
        pts = []
        for (k, day, nt), x in D["pk"].items():
            if k != sid or day != 1:
                continue
            tt = 0.0 if nt == 0 else ((x["t"] - t0).total_seconds() / 3600 if times == "actual" else nt)
            pts.append((tt, x["c"]))
        for t, c, vday in late.get(sid, []):
            nominal = {3: 48, 4: 72, 5: 96, 7: 144}.get(vday, (vday - 1) * 24)
            tt = (t - t0).total_seconds() / 3600 if times == "actual" else nominal
            pts.append((tt, c))
        per[sid] = nca(pts, trap, lz)[0]
    gm = {}
    for dose in (25, 50, 100, 200, 400):
        v = [per[k] for k in per if D["subj"][k]["dose"] == dose]
        gm[dose] = float(np.exp(np.mean(np.log(v))))
    return gm, per


def sig2(x):
    e = math.floor(math.log10(abs(x))) - 1
    return int(round(x / 10 ** e) * 10 ** e), 10 ** e


# ------------------------------------------------------------------ ask B: night heart rate
def ask_b(D, recs, owner, pairing, rule="start"):
    who = dict(owner)
    who.update(pairing)
    first_dose = {sid: D["doses"][sid][1] for sid in D["subj"]}
    vals = {}
    for rid, L in recs.items():
        sid = who.get(rid)
        if sid is None:
            continue
        d1 = first_dose[sid].astimezone(BRU).date()
        for g in L:
            if g["hr"] is None:
                continue
            if rule == "start":
                t = g["start"]
            elif rule == "mid":
                t = g["start"] + timedelta(seconds=g["dur"] / 2)
            else:
                t = g["start"] + timedelta(seconds=g["dur"] - 1)
            tl = t.astimezone(BRU)
            if tl.hour >= 6:
                continue
            night = (tl.date() - d1).days        # 0: the night before dosing ends on Day 1; 1: the night after
            if night not in (0, 1):
                continue
            vals.setdefault((sid, night), []).append(g["hr"])
    change = {sid: float(np.mean(vals[(sid, 1)]) - np.mean(vals[(sid, 0)])) for sid in D["subj"]
              if (sid, 0) in vals and (sid, 1) in vals}
    out = {}
    for study, doses in (("101", (25, 50, 100, 200, 400)), ("102", (25, 50, 100))):
        pl = [change[k] for k in change if D["subj"][k]["study"] == study and not D["subj"][k]["active"]]
        for dose in doses:
            act = [change[k] for k in change if D["subj"][k]["study"] == study and D["subj"][k]["active"]
                   and D["subj"][k]["dose"] == dose]
            out[(study, dose)] = float(np.mean(act) - np.mean(pl))
    return out, change


def naive_pairing(recs, owner):
    """The cracker's pairing: unlabelled recordings in recording-ID order against labelled ones in stop order,
    within each night's batch."""
    lab = {rid: max(g["start"] + timedelta(seconds=g["dur"]) for g in L) for rid, L in recs.items() if rid in owner}
    unl = {rid: min(g["start"] for g in L) for rid, L in recs.items() if rid not in owner}
    out = {}
    nights = sorted({v.astimezone(BRU).date() for v in unl.values()})
    for d in nights:
        u = sorted([r for r, t in unl.items() if t.astimezone(BRU).date() == d])
        l = sorted([r for r, t in lab.items() if t.astimezone(BRU).date() == d], key=lambda r: lab[r])
        for a, b in zip(u, l):
            out[a] = owner[b]
    return out


# ------------------------------------------------------------------ everything
def golden(target):
    D = load(target)
    recs, owner, pairing, pair_margin = recordings(D)
    df = drug_free(D, recs, owner)
    ex = {m: exponents(df, m) for m in ("hour", "half_hour", "two_hour", "three_hour", "harmonic1", "harmonic2",
                                        "pooled", "day_only", "day_night", "stable", "six_hour")}
    ch = c_high(D)
    G = run_cqtc(D, "own", ex["hour"], ch=ch)
    F = dict(D=D, recs=recs, owner=owner, pairing=pairing, pair_margin=pair_margin, df=df, ex=ex, ch=ch, G=G)
    F["rungs"] = {
        "QTcF": run_cqtc(D, "F", ch=ch),
        "pooled_own": run_cqtc(D, "own", ex["pooled"], ch=ch),
        "Bazett": run_cqtc(D, "B", ch=ch),
        "Framingham": run_cqtc(D, "Fram", ch=ch),
    }
    F["ask_a"] = ask_a(D)[0]
    F["ask_b"] = ask_b(D, recs, owner, pairing)[0]
    return F


if __name__ == "__main__":
    import sys
    F = golden(sys.argv[1])
    print("C_high", {d: round(v, 1) for d, v in F["ch"].items()})
    print("golden", F["G"]["call"], {d: round(v, 2) for d, v in F["G"]["ubs"].items()})
    for k, r in F["rungs"].items():
        print(k, r["call"], {d: round(v, 2) for d, v in r["ubs"].items()})
    print("mean exponent hour %.4f pooled %.4f" % (np.mean(list(F["ex"]["hour"].values())),
                                                    np.mean(list(F["ex"]["pooled"].values()))))
    print("ask A", {d: (round(v), sig2(v)[0]) for d, v in F["ask_a"].items()})
    print("ask B", {k: round(v, 2) for k, v in F["ask_b"].items()}, "pair margin %.2f" % F["pair_margin"])
