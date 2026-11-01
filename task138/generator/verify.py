"""Independent verifier for task138: reads only target/, on its own code path (csv, zipfile and xml for the
workbook, its own PDF stream decoder, its own log-Pearson III through the gamma distribution), recomputes every
graded figure and compares it with generator/figures.json.

    python3 task138/generator/verify.py      # exit 1 on any mismatch
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

from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
OUT = []


def check(name, cond, detail=""):
    OUT.append((name, bool(cond), detail))


def path(pat):
    for f in sorted(os.listdir(TARGET)):
        if re.search(pat, f):
            return os.path.join(TARGET, f)
    raise SystemExit("missing " + pat)


# ------------------------------------------------------------------ readers
def read_csv(p, skip_hash=True, skip_lines=0):
    with open(p, encoding="utf-8", newline="") as fh:
        lines = fh.read().splitlines()
    lines = lines[skip_lines:]
    if skip_hash:
        lines = [x for x in lines if not x.startswith("#")]
    rows = list(csv.reader(lines))
    return rows[0], rows[1:]


def pdf_strings(p):
    raw = open(p, "rb").read()
    out = []
    for m in re.finditer(rb"(?<!end)stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        head = raw[raw.rfind(b"<<", 0, m.start()):m.start()]
        body = raw[start:end].strip()
        if b"ASCII85Decode" in head:
            if body.endswith(b"~>"):
                body = body[:-2]
            body = base64.a85decode(body)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        for s in re.findall(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", body):
            out.append(re.sub(rb"\\(.)", rb"\1", s).decode("latin-1"))
    return " ".join(out)


def xlsx_sheets(p):
    z = zipfile.ZipFile(p)
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find("m:sheets", ns):
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        tgt = rmap[rid]
        tgt = tgt.lstrip("/")
        tgt = tgt if tgt.startswith("xl/") else "xl/" + tgt
        rows = []
        for row in ET.fromstring(z.read(tgt)).iter("{%s}row" % ns["m"]):
            vals = {}
            for c in row.findall("m:c", ns):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                col = sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(ref))) - 1
                v = c.find("m:v", ns)
                t = c.get("t")
                if t == "s":
                    vals[col] = shared[int(v.text)]
                elif t == "inlineStr":
                    vals[col] = "".join(x.text or "" for x in c.iter("{%s}t" % ns["m"]))
                elif v is not None:
                    vals[col] = float(v.text)
            if vals:
                rows.append([vals.get(i) for i in range(max(vals) + 1)])
        out[sh.get("name")] = rows
    return out


def sta(s):
    a, b = s.strip().split("+")
    return int(a) * 100 + int(b)


# ------------------------------------------------------------------ frequency method
def lp3(x, gr, mser):
    y = [math.log10(v) for v in x]
    n = len(y)
    mu = sum(y) / n
    s = math.sqrt(sum((v - mu) ** 2 for v in y) / (n - 1))
    g = n * sum((v - mu) ** 3 for v in y) / ((n - 1) * (n - 2) * s ** 3)
    ag = abs(g)
    a = -0.33 + 0.08 * ag if ag <= 0.9 else -0.52 + 0.30 * ag
    b = 0.94 - 0.26 * ag if ag <= 1.5 else 0.55
    mg = 10 ** (a - b * math.log10(n / 10.0))
    gw = (mser * g + mg * gr) / (mser + mg)
    return mu, s, gw


def k_factor(p_non_exceed, g):
    if abs(g) < 1e-6:
        return stats.norm.ppf(p_non_exceed)
    alpha = 4.0 / g ** 2
    if g > 0:
        return (stats.gamma.ppf(p_non_exceed, alpha) - alpha) / math.sqrt(alpha)
    return -(stats.gamma.ppf(1 - p_non_exceed, alpha) - alpha) / math.sqrt(alpha)


def exceed(mu, s, gw, q):
    z = (math.log10(q) - mu) / s
    if abs(gw) < 1e-6:
        return 1 - stats.norm.cdf(z)
    alpha = 4.0 / gw ** 2
    if gw > 0:
        return 1 - stats.gamma.cdf(alpha + z * math.sqrt(alpha), alpha)
    return stats.gamma.cdf(alpha - z * math.sqrt(alpha), alpha)


def wy_of(d):
    return d.year + 1 if d.month >= 10 else d.year


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    # ---- peaks
    h, rows = read_csv(path(r"annual_peaks.*\.csv$"))
    ix = {k: i for i, k in enumerate(h)}
    hal, coy = {}, {}
    for r in rows:
        d = dt.date.fromisoformat(r[ix["peak_dt"]])
        if r[ix["site_no"]] == "05433000":
            hal[wy_of(d)] = float(r[ix["peak_va"]])
        elif r[ix["site_no"]] == "05432100":
            coy[wy_of(d)] = float(r[ix["peak_va"]])
    check("peaks: 65 water years at both gauges", sorted(hal) == sorted(coy) == list(range(1962, 2027)))
    # ---- documents
    std = pdf_strings(path(r"LS-02"))
    check("LS-02 read back (positive control)", "1 per cent chance of being exceeded" in std)
    fb_gen = float(re.search(r"Levee generally (\d\.\d) ft", std).group(1))
    fb_br = float(re.search(r"closure structure (\d\.\d) ft", std).group(1))
    fb_up = float(re.search(r"(\d\.\d) ft at station 0\+00", std).group(1))
    sk = pdf_strings(path(r"regional_skew"))
    check("SW-16-03 read back (positive control)", "Central Lowlands" in sk and "Marrow" in sk)
    gm = re.search(r"2 Central Lowlands (-?\d\.\d\d) (\d\.\d\d)", sk)
    gr, mser = float(gm.group(1)), float(gm.group(2))
    t4txt = pdf_strings(path(r"Table4"))
    check("Table 4 read back (positive control)", "Computed water surface elevations" in t4txt)
    qs = sorted({int(x.replace(",", "")) for x in re.findall(r"\b(\d{2,3},000)\b", t4txt)})
    table = {}
    for m in re.finditer(r"(\d+\+\d\d)\s*\*?\s+((?:\d{3}\.\d\d\s*){10})", t4txt):
        table[sta(m.group(1))] = [float(v) for v in m.group(2).split()]
    check("Table 4: 21 cross-sections by 10 discharges", len(table) == 21 and len(qs) == 10)
    sheets = xlsx_sheets(path(r"levee_inventory.*\.xlsx$"))
    check("inventory read back: four sheets", set(sheets) == {"Segments", "Orrinsford crown", "Gauges", "Structures"})
    seg = sheets["Segments"]
    gauges = {r[0]: r for r in sheets["Gauges"][1:]}
    rm_c, rm_h = float(gauges["05432100"][2]), float(gauges["05433000"][2])
    inforce = []
    for r in seg[1:]:
        a, b = float(r[3]), float(r[4])
        txt = "" if r[6] is None else str(r[6])
        if rm_h < min(a, b) and max(a, b) < rm_c and txt.strip():
            inforce.append(int(re.search(r"(\d{4})", txt).group(1)) + 1)
    cut = max(inforce)
    check("raises between the gauges: six, the last in force from water year 2009", len(inforce) == 6 and cut == 2009)
    crown = {sta(r[0]): float(r[2]) for r in sheets["Orrinsford crown"][1:]}
    bridges = [sta(r[1]) for r in sheets["Structures"][1:] if "bridge" in r[2].lower()]

    # ---- the present river's record and the design flood
    yrs = sorted(hal)
    post = [y for y in yrs if y >= cut]
    r = sum(hal[y] * coy[y] for y in post) / sum(coy[y] ** 2 for y in post)
    ser = [hal[y] if y >= cut else r * coy[y] for y in yrs]
    mu, s, gw = lp3(ser, gr, mser)
    q1 = 10 ** (mu + k_factor(0.99, gw) * s)
    std_window = int(re.search(r"opened in water year (\d{4})", std).group(1))
    check("LS-02 window: one peak for every water year since %d (65 years)" % std_window,
          std_window == 1962 and len(ser) == 2026 - std_window + 1)
    check("design discharge %.0f cfs reported %d" % (q1, fig["call"]["design_discharge_cfs"]),
          int(round(q1 / 5000) * 5000) == fig["call"]["design_discharge_cfs"])

    def fb(x):
        near = any(abs(x - b) <= 100 for b in bridges)
        return (fb_br if near else fb_gen) + fb_up * (1 - x / 18000.0)

    def wse(q, x):
        row = table[x]
        if q <= qs[0]:
            return row[0]
        for i in range(len(qs) - 1):
            if q <= qs[i + 1]:
                return row[i] + (row[i + 1] - row[i]) * (q - qs[i]) / (qs[i + 1] - qs[i])
        return row[-1]

    def q_of(z, x):
        row = table[x]
        for i in range(len(qs) - 1):
            if row[i] <= z <= row[i + 1]:
                return qs[i] + (z - row[i]) * (qs[i + 1] - qs[i]) / (row[i + 1] - row[i])
        if z < row[0]:
            return qs[0] + (z - row[0]) * (qs[1] - qs[0]) / (row[1] - row[0])
        return qs[-1] + (z - row[-1]) * (qs[-1] - qs[-2]) / (row[-1] - row[-2])

    short = max(wse(q1, x) + fb(x) - crown[x] for x in table)
    rz = 0 if short <= 0 else math.ceil(short)
    check("raise %d ft (shortfall %.2f ft)" % (rz, short), rz == fig["call"]["raise_ft"])
    for k in range(5):
        cap = min(q_of(crown[x] + k - fb(x), x) for x in table)
        a = 100 * exceed(mu, s, gw, cap)
        check("annual chance with a %d ft raise %.3f%% reported %.1f" % (k, a, fig["aep_pct_by_raise"]["%d ft" % k]),
              round(a, 1) == fig["aep_pct_by_raise"]["%d ft" % k])
    q0 = lp3([hal[y] for y in yrs], gr, mser)
    q_easy = 10 ** (q0[0] + k_factor(0.99, q0[2]) * q0[1])
    s0 = max(wse(q_easy, x) + fb(x) - crown[x] for x in table)
    check("the published-record fit files no raise (%.0f cfs)" % q_easy, s0 <= 0)

    # ---- ask A: settlement
    h24, r24 = read_csv(path(r"certification_survey_2024"))
    h16, r16 = read_csv(path(r"crown_survey_2016"))
    hb_, rb = read_csv(path(r"benchmark_list"))
    shift = sum(float(x[3]) - float(x[2]) for x in rb) / len(rb)
    f24 = {x[2]: sta(x[0]) for x in r24 if x[2] != "CL"}
    f16 = {x[2]: sta(x[0]) for x in r16 if x[2] != "CL" and not x[2].startswith("BM")}
    offs = {f16[k] - f24[k] for k in f24 if k in f16}
    check("stationing offset from the shared structures: one value", len(offs) == 1)
    off = offs.pop()
    cl24 = {sta(x[0]): (float(x[1]), x[3]) for x in r24 if x[2] == "CL"}
    acc = {}
    for x in r16:
        if x[2] != "CL":
            continue
        p = sta(x[0]) - off
        if p in cl24:
            z, reach = cl24[p]
            acc.setdefault(reach, []).append(float(x[1]) + shift - z)
    for k, v in sorted(acc.items()):
        mval = sum(v) / len(v)
        check("settlement %s %.4f reported %.2f" % (k, mval, fig["settlement_ft"][k]),
              round(mval, 2) == fig["settlement_ft"][k])

    # ---- ask B: lead times
    proc = pdf_strings(path(r"OP-04"))
    check("OP-04 read back (positive control)", "flood warning" in proc)
    wm = re.search(r"warning level, elevation (\d+\.\d\d) ft NGVD 29 \((\d+\.\d) ft on the gauge\)", proc)
    wel, wst = float(wm.group(1)), float(wm.group(2))
    sill = float(re.search(r"closure sill, (\d+\.\d\d) ft NAVD 88", proc).group(1))
    with open(path(r"05432100_hourly"), encoding="utf-8") as fh:
        top = fh.read(600)
    cdat = float(re.search(r"Gauge datum (\d+\.\d\d) ft above NGVD 29", top).group(1))
    hc, rc = read_csv(path(r"05432100_hourly"))
    ct = [dt.datetime.strptime(x[0], "%Y-%m-%d %H:%M") for x in rc]
    cs = [float(x[1]) for x in rc]
    cq = [float(x[2]) for x in rc]
    # datum change: the first hour after which low-flow stage sits 1.5 ft or more above the first year's relation
    import numpy as np
    lq = np.log(np.array(cq))
    hs_ = np.array(cs)
    band = (np.array(cq) >= 1500) & (np.array(cq) <= 15000)
    first = band & (np.array([t < dt.datetime(2018, 10, 1) for t in ct]))
    cf = np.polyfit(lq[first], hs_[first], 2)
    res = hs_ - np.polyval(cf, lq)
    idx = [i for i in range(len(ct)) if band[i]]
    change = None
    for j in range(len(idx) - 48):
        win = res[idx[j:j + 48]]
        if np.all(win > 1.0):
            change = ct[idx[j]]
            break
    check("Coyle Bridge datum change found from the data", change is not None)
    with open(path(r"ORF2_logger"), encoding="utf-8") as fh:
        head = [next(fh) for _ in range(4)]
    hdat = float(re.search(r"(\d+\.\d\d) ft NGVD 29", head[2]).group(1))
    hh, rh = read_csv(path(r"ORF2_logger"), skip_hash=False, skip_lines=4)
    ht = [dt.datetime.strptime(x[0], "%m/%d/%Y %H:%M") for x in rh]
    hv = [float(x[1]) for x in rh]
    gi = next(i for i in range(1, len(ht)) if ht[i] < ht[i - 1])        # the new logger's records start here
    old = dict(zip(ht[:gi], hv[:gi]))
    new = dict(zip(ht[gi:], hv[gi:]))
    best = None
    for s in range(-12, 13):
        pairs = [(old[t], new[t + dt.timedelta(hours=s)]) for t in old if t + dt.timedelta(hours=s) in new]
        if len(pairs) >= 24:
            d = sum(abs(a - b) for a, b in pairs) / len(pairs)
            best = (d, s) if best is None or d < best[0] else best
    dh = best[1]
    check("ORF2 clock: the two loggers' overlap lines up at %d h" % dh, dh == 6)
    pub = []
    for r in rows:
        if r[ix["site_no"]] == "05433000" and r[ix["peak_tm"]]:
            pub.append(dt.datetime.strptime(r[ix["peak_dt"]] + " " + r[ix["peak_tm"]], "%Y-%m-%d %H:%M"))
    offs = set()
    for blk in ((ht[:gi], hv[:gi]), (ht[gi:], hv[gi:])):
        for p in pub:
            win = [i for i in range(len(blk[0])) if p - dt.timedelta(days=3) < blk[0][i] < p + dt.timedelta(days=3)]
            if win:
                top = max(win, key=lambda i: blk[1][i])
                offs.add(round((blk[0][top] - p).total_seconds() / 3600))
    check("ORF2 clock: yearly highest readings sit 0 h (old logger) and 6 h (new logger) from the published times",
          offs == {0, 6})
    ht2 = [t + dt.timedelta(hours=dh) for t in ht[:gi] if t + dt.timedelta(hours=dh) < ht[gi]] + ht[gi:]
    hv = [v for t, v in zip(ht[:gi], hv[:gi]) if t + dt.timedelta(hours=dh) < ht[gi]] + hv[gi:]
    ht = ht2
    sill_stage = sill - (hdat + shift)
    leads = []
    for j in range(1, len(hv)):
        if hv[j - 1] < sill_stage <= hv[j] and ht[j] - ht[j - 1] == dt.timedelta(hours=1):
            tj = ht[j - 1] + (ht[j] - ht[j - 1]) * ((sill_stage - hv[j - 1]) / (hv[j] - hv[j - 1]))
            k = max(i for i in range(len(ct)) if ct[i] <= ht[j])
            while k > 1:
                thr = wst if ct[k] < change else wel - cdat
                if cs[k - 1] < thr <= cs[k]:
                    tk = ct[k - 1] + (ct[k] - ct[k - 1]) * ((thr - cs[k - 1]) / (cs[k] - cs[k - 1]))
                    leads.append((tj, (tj - tk).total_seconds() / 3600))
                    break
                k -= 1
    got = [int(round(h_)) for _, h_ in leads]
    want = list(fig["lead_time_h"].values())
    check("lead times %s reported %s" % (got, want), got == want)

    bad = [o for o in OUT if not o[1]]
    for n, okk, d in OUT:
        print("%s  %s" % ("OK  " if okk else "FAIL", n))
    print("verify: %d checks, %d failed" % (len(OUT), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
