"""task129 ask ceiling, measured on the cut pack.

Shares no code with the generator: it imports nothing from task129/generator and reads only the pack (a target
folder or target.zip) and figures.json for the golden values. The cracker is the careful solver's route drawn from
the prompt, the two policies and the files, never from the ask list: it lands the call, executes every filed rule it
points at (ENG-REL-02 2.1 to 3.3, OPS-ROW-01 4.3), and runs the hygiene battery (exact duplicates, one outage per
device opening as 2.1 folds it, a reversed row removed by its reversal, a credit memo netted against the invoice it
names, units per source converted, unmatched joins). The mirror stops on the district rise against the contract
register (a re-bid) and walks the same ask paths, the asks being decoupled from the call. Stress rows print the
routes a response might take beyond the battery; they are not the gate.

    python3 ceiling.py <target folder or target.zip> <figures.json>
"""
import hashlib
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

DIST = ["North", "East", "South"]
VENDORS = ["Hollenbeck Line Clearance, Inc.", "Garrity Vegetation Services, LLC"]


def opener(pack):
    if pack.endswith(".zip"):
        z = zipfile.ZipFile(pack)
        return lambda n: io.BytesIO(z.read(n)), z.namelist()
    return lambda n: open(os.path.join(pack, n), "rb"), os.listdir(pack)


def table(op, names, stem):
    name = [n for n in names if n.startswith(stem)][0]
    return pd.read_csv(op(name), dtype=str, keep_default_na=False)


# ---------------------------------------------------------------- the main call's construction (the cracker has it)
def tickets(X):
    X = X.drop_duplicates()
    X = X.assign(t0=pd.to_datetime(X.start_local), t1=pd.to_datetime(X.step_restored_local))
    X["cmi"] = X.members_restored.astype(int) * (X.t1 - X.t0).dt.total_seconds() / 60.0
    T = X.groupby("ticket_no").agg(t0=("t0", "min"), t1=("t1", "max"), lvl=("level", "first"),
                                   d=("service_area", "first"), dev=("device_id", "first"),
                                   cause=("cause_code", "first"), mem=("members_out", "first"),
                                   cmi=("cmi", "sum")).reset_index()
    T["mem"] = T.mem.astype(int)
    return T


def one_outage_a_device(T, start="t0", end="t1"):
    """ENG-REL-02 2.1: a device is in one outage at a time, so a record opening while its device is out is that
    outage"""
    T = T.sort_values(["dev", start]).reset_index(drop=True)
    prev = T.groupby("dev")[end].transform(lambda s: s.cummax().shift())
    return T[~(T[start] <= prev)].copy()


def major_event_days(T, M):
    served = M.assign(n=M.members_at_year_end.astype(int)).groupby(M.year.astype(int)).n.sum()
    T = T.assign(sus=(T.t1 - T.t0).dt.total_seconds() > 300, day=T.t0.dt.normalize())
    s = T[(T.cause != "PLANNED") & T.sus].groupby("day").cmi.sum()
    s = s / np.array([served[d.year] for d in s.index])
    out = {}
    for y in range(2021, 2026):
        h = s[(s.index.year >= y - 5) & (s.index.year < y) & (s > 0)]
        th = np.exp(np.log(h).mean() + 2.5 * np.log(h).std(ddof=1))
        out[y] = sorted(s[(s.index.year == y) & (s > th)].index)
    return out


def call_rates(T, R, md):
    allmed = {d for y in md for d in md[y]}
    T = T.assign(sus=(T.t1 - T.t0).dt.total_seconds() > 300, day=T.t0.dt.normalize(), yr=T.t0.dt.year)
    t = T[(T.cause == "TREE") & (T.lvl == "PRIMARY") & T.sus & ~T.day.isin(allmed)]
    a = pd.to_datetime(R.in_service_date)
    b = pd.to_datetime(R.retired_date.replace("", "2999-12-31"))
    mi = R.miles.astype(float)
    out = {}
    for y in range(2021, 2026):
        lo, hi = pd.Timestamp(y, 1, 1), pd.Timestamp(y + 1, 1, 1)
        m = (mi * (np.minimum(b, hi) - np.maximum(a, lo)).dt.days.clip(lower=0) / (hi - lo).days).sum()
        out[y] = 100.0 * (t.yr == y).sum() / m
    return round(out[2025], 1), round(np.mean([out[y] for y in (2021, 2022, 2023)]), 1)


# ---------------------------------------------------------------- ask B: 2025's major event days
def med_openings(X, days, reading):
    """the openings on the major event days under a reading of a negative restored step: net (the battery: a reversal
    removed with the restoration it reverses), literal (one opening a ticket, the steps as they stand), drop (negative
    rows dropped as impossible), split (a new device opening at the negative step, ENG-REL-02 2.1)"""
    X = X.drop_duplicates()
    X = X[pd.to_datetime(X.start_local).dt.normalize().isin(days)].copy()
    X["t0"] = pd.to_datetime(X.start_local)
    X["t"] = pd.to_datetime(X.step_restored_local)
    X["n"] = X.members_restored.astype(int)
    X["k"] = X.step.astype(int)
    rows = []
    for tk, g in X.sort_values(["ticket_no", "k"]).groupby("ticket_no", sort=False):
        top = g.iloc[0]
        steps = list(zip(g.t, g.n))
        if reading == "drop":
            steps = [(t, n) for t, n in steps if n >= 0]
        if reading == "net":
            kept = []
            for t, n in steps:
                if n < 0:
                    hit = [j for j, (_, m) in enumerate(kept) if m == -n]
                    if hit:
                        kept.pop(hit[-1])
                        continue
                kept.append((t, n))
            steps = kept
        segs = [[top.t0, int(top.members_out), []]]
        for t, n in steps:
            if reading == "split" and n < 0:
                segs.append([t, -n, []])
            else:
                segs[-1][2].append((t, n))
        for s0, mem, st in segs:
            e = max([t for t, _ in st] or [s0])
            rows.append(dict(dev=top.device_id, d=top.service_area, cause=top.cause_code, lvl=top.level, t0=s0, t1=e,
                             mem=mem, cmi=sum(n * (t - s0).total_seconds() / 60.0 for t, n in st)))
    O = one_outage_a_device(pd.DataFrame(rows))
    return O[(O.cause != "PLANNED") & ((O.t1 - O.t0).dt.total_seconds() > 300) & O.t0.dt.normalize().isin(days)]


def ask_b(X, days, reading):
    O = med_openings(X, days, reading)
    return {d: (len(O[O.d == d]), int(O[O.d == d].mem.sum()), int(round(O[O.d == d].cmi.sum()))) for d in DIST}


# ---------------------------------------------------------------- asks A and C: the trimming invoices
MON = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def stated(text):
    a = re.search(r"(\d\d)/\d\d/(\d{4})-\d\d/\d\d/\d{4}", text)
    if a:
        return "%s-%s" % (a.group(2), a.group(1))
    b = re.search(r"\b([A-Z]{3}) (20\d\d)\b", text)
    return "%s-%02d" % (b.group(2), MON[b.group(1)]) if b and b.group(1) in MON else ""


def trimming(I, reading):
    """trimming lines in miles with the month each reading files them under: service (the cracker: credit memos
    netted against the invoices they name, the rest at their service month), lag (credits netted, the invoice month
    less one), own (every signed line at its own service month, a blank credit at its invoice's), stated (the period
    a line states, else its service month, a blank credit at its invoice's)"""
    I = I.drop_duplicates()
    tr = I[I.item_code.str.startswith("TRIM")].copy()
    tr["mi"] = tr.quantity.astype(float) / np.where(tr.uom == "LF", 5280.0, 1.0)
    named = set(tr.applies_to_invoice[tr.doc_type == "CREDIT MEMO"])
    if reading in ("service", "lag"):
        tr = tr[(tr.doc_type != "CREDIT MEMO") & ~tr.invoice_no.isin(named)].copy()
        tr["m"] = tr.service_month if reading == "service" else \
            (pd.to_datetime(tr.invoice_date).dt.to_period("M") - 1).astype(str)
    else:
        own = tr.service_month if reading == "own" else \
            pd.Series([stated(t) or s for t, s in zip(tr.description, tr.service_month)], index=tr.index)
        first = own[tr.doc_type == "INVOICE"].groupby(tr.invoice_no[tr.doc_type == "INVOICE"]).first()
        tr["m"] = [o if o else first.get(a, "") for o, a in zip(own, tr.applies_to_invoice)]
    return tr[tr.m.str.startswith("2025")]


def ask_a(I, reading):
    tr = trimming(I, reading)
    q = "Q" + ((tr.m.str[5:7].astype(int) + 2) // 3).astype(str)
    g = tr.mi.groupby([tr.vendor, q]).sum()
    return {"%s %s" % (v, k): float(g.get((v, k), 0.0)) for v in VENDORS for k in ("Q1", "Q2", "Q3", "Q4")}


def ask_c(I, C, R, reading):
    tr = trimming(I, reading)
    unit_d = dict(zip(R.unit_id, R.district))
    wo = C.assign(d=C.unit_id.map(unit_d)).groupby("work_order").d.agg(lambda s: s.iloc[0] if s.nunique() == 1 else "")
    g = tr.mi.groupby(tr.work_order.map(wo)).sum()
    return {d: float(g.get(d, 0.0)) for d in DIST}


# ---------------------------------------------------------------- scoring
def hit(golden, got, step):
    return abs(got - float(str(golden).replace(",", ""))) < step / 2.0 + 1e-9


def score(fig, a, b, c):
    rows = []
    for k, v in fig["billing"].items():
        rows.append(("A " + k, a[k], v, 0.1))
    for d in DIST:
        for i, key in enumerate(("outages", "members", "customer_minutes")):
            rows.append(("B %s %s" % (d, key), b[d][i], fig["med"][d][key], 1.0))
    for d in DIST:
        rows.append(("C %s" % d, c[d], fig["district_billing"][d], 0.1))
    return rows, [hit(g, x, s) for _, x, g, s in rows]


def pair(kept_c, kept_s, r=5.0):
    cc = 38 + 7 + 55 * kept_c
    ss = r + 7 + 55 * kept_s
    return cc, ss, (cc + ss) / 2.0


def main(pack, figpath):
    fig = json.load(open(figpath))
    op, names = opener(pack)
    X = table(op, names, "oms_outage_export")
    M = table(op, names, "member_counts")
    R = table(op, names, "trim_unit_register")
    C = table(op, names, "row_trim_completions")
    I = table(op, names, "ap_trimming_invoice_lines")
    T = tickets(X)
    Tu = one_outage_a_device(T)
    md = major_event_days(Tu, M)
    days = set(md[2025])
    lands = call_rates(Tu, R, md)
    digest = hashlib.sha256(open(pack, "rb").read()).hexdigest()[:16] if pack.endswith(".zip") else "folder"
    print("pack: %s (%s)" % (pack, digest))
    print("the cracker lands the call: rates %.1f in 2025 and %.1f over 2021 to 2023 (golden %s, %s); 2025's major "
          "event days %s" % (lands[0], lands[1], fig["rate_2025"], fig["rate_base"],
                             ", ".join(d.strftime("%d %b") for d in md[2025])))
    routes = {
        "cracker": (ask_a(I, "service"), ask_b(X, days, "net"), ask_c(I, C, R, "service")),
        "stress, fold and literal steps (B), service month (A, C)": (ask_a(I, "service"), ask_b(X, days, "literal"),
                                                                    ask_c(I, C, R, "service")),
        "stress, invoice month less one (A, C), literal steps (B)": (ask_a(I, "lag"), ask_b(X, days, "literal"),
                                                                    ask_c(I, C, R, "lag")),
        "stress, every signed line at its own month (A, C), negatives dropped (B)": (ask_a(I, "own"),
                                                                                    ask_b(X, days, "drop"),
                                                                                    ask_c(I, C, R, "own")),
        "full includer (stated periods, a new opening at each negative step)": (ask_a(I, "stated"),
                                                                               ask_b(X, days, "split"),
                                                                               ask_c(I, C, R, "stated")),
    }
    rows, hits = score(fig, *routes["cracker"])
    if not rows or not fig.get("rate_2025"):
        sys.exit("ceiling.py refuses: %s" % ("no ask figure in figures.json to score" if not rows else
                                             "no call figure in figures.json to land"))
    print("\n%-56s %14s %14s  %s" % ("ask figure", "cracker", "golden", "verdict"))
    for (lab, x, g, s), h in zip(rows, hits):
        print("%-56s %14s %14s  %s" % (lab, ("{:,.1f}".format(x) if s < 1 else "{:,}".format(int(x))), g,
                                         "HIT" if h else "miss"))
    n = len(hits)
    kept = sum(hits) / n
    cc, ss, pr = pair(kept, kept)
    print("\ncracker keeps %d of %d ask figures; the mirror (R0, a re-bid) walks the same ask paths and keeps the same"
          % (sum(hits), n))
    print("landed 38 + 7 + 55 x %.3f = %.1f; mirror 5 + 7 + 55 x %.3f = %.1f; pair %.1f; mirror leakage %.1f per cent"
          % (kept, cc, kept, ss, pr, 100 * kept))
    print("\nstress rows (not the gate):")
    for name, (a, b, c) in routes.items():
        if name == "cracker":
            continue
        _, h = score(fig, a, b, c)
        k = sum(h) / n
        print("  %-76s keeps %2d of %d, pair %.1f if both top responses take it" % (name, sum(h), n, pair(k, k)[2]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
