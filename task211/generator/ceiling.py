"""The cracker and mirror sheets, run on the cut pack. Every graded ask figure of the workbook is scored for each
response, each computed here from target/ by its own route:

  cracker  lands the call (the decay-bound falls), runs the hygiene battery (exact duplicate rows once, the LoRa
           gateway's UK clock converted, the earliest receipt of a re-sent hour, the latest version of a re-issued
           result, the outstation codes mapped, microsieverts converted, a negative totaliser difference read as the
           rollover or the controller replacement it is) and executes every filed rule (the repeat is the check, a
           certificate applies from its date of issue, the jig used, the quarter's intervals, the measured flow the
           controller export names); it takes each kit's source from the kit register, each filter's volume from the
           measured flow as logged and each interval from the ingest log's batches;
  mirror   misses the call (it clears the increases the procedure's rain screen clears) and takes the asks by the
           same careful route;
  naive    the asks with the battery half run (LoRa read as UTC, the first certificate a source has, the field
           sheets' totaliser readings differenced as they stand and AS2's volume at its set flow);
  full     the golden.

A hit is a figure within half a unit of its stated rounding (a source check's percentage with its result). Scores on
38, 7 and 55 so builds compare; the pack's digest is printed so a figure is tied to the pack it was measured on."""
import csv
import datetime as dt
import hashlib
import os

import numpy as np
from openpyxl import load_workbook

import golden as G
import pack
import world as W


def checks_by_register(tgt, latest_cert=False):
    """Source checks with each kit's source taken from the kit register."""
    real = G.source_checks(tgt)
    kit_src = {}
    with open(os.path.join(tgt, pack.FILES["kits"]), newline="") as f:
        for r in list(csv.reader(f))[1:]:
            kit_src[r[0]] = r[2]
    out = {}
    for code, c in real.items():
        src = kit_src[c["kit"]]
        certs = G.certs()[src]
        ok = certs[:1] if latest_cert else [x for x in certs if x[2] <= c["date"]]
        no, ref, issued, vals = ok[-1]
        y = (c["date"] - ref).days / 365.25
        exp = vals[c["jig"]] * 2 ** (-y / G.HALF)
        pct = c["net"] / exp * 100.0
        out[code] = (round(pct, 1), abs(pct - 100.0) <= 10.0)
    return out


def air_by_logged_flow(tgt, g):
    """Each filter's volume from the measured flow as the controller logged it, summed over its rows: a dropout's
    blank rows add nothing."""
    sums = {}
    with open(os.path.join(tgt, pack.FILES["pump"]), newline="") as f:
        rows = list(csv.reader(f))[1:]
    q15 = dt.timedelta(minutes=15)
    out = {}
    by = {}
    for s, ts, st, fl, tot in rows:
        by.setdefault(s, []).append((dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"), float(fl) if fl else 0.0))
    for fid, a in g["air"].items():
        vol = sum(fl * 0.25 for t, fl in by[a["sampler"]] if a["on"] - q15 < t < a["off"])
        out[fid] = round(a["activity"] / vol * 1000.0, 2)
    return out


def air_by_totaliser(tgt, g, replacement=True):
    """Each filter's volume from its totaliser readings (AS2's from its hour-meter volume at the set flow)."""
    wb = load_workbook(os.path.join(tgt, pack.FILES["field"]), read_only=True)
    log = {}
    with open(os.path.join(tgt, pack.FILES["pump"]), newline="") as f:
        rd = csv.reader(f); next(rd)
        for s, ts, st, fl, tot in rd:
            log.setdefault(s, []).append((dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"), st, tot))
    out = {}
    for sampler, code, flow, style in W.AIR:
        rows = list(wb[sampler].iter_rows(values_only=True))[1:]
        for r in rows:
            fid = r[0]
            if style == "hourmeter":
                vol = float(r[5])
            else:
                a, b = float(r[3]), float(r[4])
                vol = b - a
                if vol < 0 and replacement:
                    if a > 90000:
                        vol += 100000.0
                    else:
                        on = dt.datetime.strptime(r[1], "%d/%m/%Y %H:%M") - W.BST
                        off = dt.datetime.strptime(r[2], "%d/%m/%Y %H:%M") - W.BST
                        seq = [float(t) for ts, st, t in log[sampler] if on <= ts <= off and t]
                        drop = [k for k in range(1, len(seq)) if seq[k] < seq[k - 1]][0]
                        vol = (seq[drop - 1] - a) + b
            act = g["air"][fid]["activity"]
            out[fid] = round(act / vol * 1000.0, 2) if vol > 0 else None
    return out


def timely_by_ingest(tgt, lora_local=True):
    first = {}
    with open(os.path.join(tgt, pack.FILES["ingest"]), newline="") as f:
        rd = csv.reader(f); next(rd)
        for bid, code, ch, a, b, n, rec in rd:
            if rec.endswith("Z"):
                when = dt.datetime.strptime(rec, "%Y-%m-%dT%H:%M:%SZ")
            else:
                when = dt.datetime.strptime(rec, "%d/%m/%Y %H:%M:%S") - (W.BST if lora_local else dt.timedelta(0))
            m = (when - W.Q_START).total_seconds() / 60.0
            arr = first.setdefault(code, np.full(W.N10, np.inf))
            seg = arr[G.t_of(a):G.t_of(b) + 1]
            np.minimum(seg, m, out=seg)
    end = np.arange(W.N10) * 10.0 + 10.0
    return {c: round(float((v - end <= 60.0).sum()) / W.N10 * 100.0, 1) for c, v in first.items()}


def measure(tgt, g):
    gold_A = {c: (round(v["pct"], 1), v["passed"]) for c, v in g["checks"].items()}
    gold_B = {k: round(v["conc"], 2) for k, v in g["air"].items()}
    gold_C = {c: round(v["pct"], 1) for c, v in g["timely"].items()}
    routes = {
        "cracker": (checks_by_register(tgt), air_by_logged_flow(tgt, g), timely_by_ingest(tgt)),
        "naive": (checks_by_register(tgt, latest_cert=True), air_by_totaliser(tgt, g, replacement=False),
                  timely_by_ingest(tgt, lora_local=False)),
        "full": (gold_A, gold_B, gold_C),
    }
    gold = (gold_A, gold_B, gold_C)
    rows = {}
    for name, (A, B, C) in routes.items():
        hits = []
        for got, ref in zip((A, B, C), gold):
            hits.append(sum(1 for k in ref if got.get(k) is not None and got.get(k) == ref[k]))
        rows[name] = dict(A=hits[0], B=hits[1], C=hits[2])
    rows["mirror"] = dict(rows["cracker"])
    n = dict(A=len(gold_A), B=len(gold_B), C=len(gold_C))
    total = sum(n.values())
    Lc = sum(rows["cracker"].values()) / total
    Lm = sum(rows["mirror"].values()) / total
    Ln = sum(rows["naive"].values()) / total
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    digest = hashlib.sha256()
    for root, _, files in sorted(os.walk(tgt)):
        for fn in sorted(files):
            digest.update(open(os.path.join(root, fn), "rb").read())
    return dict(rows=rows, figures=n, cracker_score=round(C, 1), mirror_score=round(S, 1), pair=round((C + S) / 2, 1),
                cracker_keep=round(100 * Lc, 1), mirror_leakage=round(100 * Lm, 1), naive_keep=round(100 * Ln, 1),
                full_keep=round(100 * sum(rows["full"].values()) / total, 1), pack_digest=digest.hexdigest()[:16])
