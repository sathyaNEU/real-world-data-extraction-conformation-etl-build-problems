"""Independent verifier for task146. Reads only the shipped bundle (target/) and the goldens, on its own code path
(the csv module, openpyxl and numpy least squares; nothing from the generator's modules), and recomputes the call
(each region's step on its closing quarter's determinations month by month), its components, the default path (the
same regions on the quarter taken whole), the national-rate rival, the seasonal route, every Ask A cell and every
Ask B change, then checks the goldens carry them.

    python3 task146/generator/verify.py [target] [golden]"""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MON = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def find(target, prefix):
    hits = [f for f in os.listdir(target) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(target, hits[0])


def half_up(x, step):
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def dp1(x):
    return math.floor(x * 10 + 0.5) / 10 if x >= 0 else -math.floor(-x * 10 + 0.5) / 10


def quarter(d):
    return d.year, (d.month - 1) // 3 + 1


# ---------------------------------------------------------------------------------------------------- the call
def series(target):
    reg = rows(find(target, "regions_"))
    code = {r["region_code"]: r["region"] for r in reg}
    regions = list(dict.fromkeys(r["region"] for r in reg))
    s = {r: {} for r in regions}
    for r in rows(find(target, "brs_weekly")):
        d = dt.date(int(r["WEEK_COMMENCING"][6:]), int(r["WEEK_COMMENCING"][3:5]), int(r["WEEK_COMMENCING"][:2]))
        s[code[r["REGION_CD"]]][d] = int(r["INITIAL_CLAIMS"])
    for r in rows(find(target, "uics_weekly")):
        s[r["region"]][dt.date.fromisoformat(r["claims_week_start"])] = int(r["initial_claims"])
    return regions, code, s


def pools(target, regions, code):
    wb = openpyxl.load_workbook(find(target, "ui_program_statistics"), data_only=True)
    m = {}
    for ws in wb.worksheets:
        if not ws.title.startswith("FY"):
            continue
        vals = list(ws.iter_rows(values_only=True))
        if vals[0][0] == "UNEMPLOYMENT INSURANCE BOARD":
            for i, r in enumerate(vals):
                if r[0] == "INSUFFICIENT":
                    months = [(2000 + int(h[-2:]), MON[h[:3]]) for h in vals[i + 1][1:13]]
                    for rr in vals[i + 2:i + 10]:
                        for ym, v in zip(months, rr[1:13]):
                            if v is not None:
                                m[(ym, code[rr[0]])] = int(v)
        else:
            h = list(vals[2])
            c = h.index("Monetarily ineligible")
            for r in vals[3:]:
                if isinstance(r[0], dt.datetime) and r[1] in regions:
                    m[((r[0].year, r[0].month), r[1])] = int(r[c])
    out, nm = {}, {}
    for ((y, mo), r), v in m.items():
        q = (y, (mo - 1) // 3 + 1)
        out[(r, q)] = out.get((r, q), 0) + v
        if r == regions[0]:
            nm[q] = nm.get(q, 0) + 1
    return out, nm, m


def lsq(X, y):
    X, y = np.asarray(X, float), np.asarray(y, float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = float(e @ e) / (len(y) - X.shape[1])
    return b, s2 * np.linalg.inv(X.T @ X)


def the_call(target):
    regions, code, s = series(target)
    pool, nm, monthly = pools(target, regions, code)
    weeks = sorted(s[regions[0]])
    nat = {d: sum(s[r][d] for r in regions) for d in weeks}
    last = weeks[-1]
    target_q = quarter(last + dt.timedelta(days=7))
    closing = quarter(last)

    def months(q, r):
        return [monthly[((q[0], 3 * (q[1] - 1) + j), r)] for j in (1, 2, 3)]
    turns = [k for k in range(1, len(weeks)) if quarter(weeks[k]) != quarter(weeks[k - 1])
             and nm.get(quarter(weeks[k - 1])) == 3]
    tot, var, refile, without, slopes, tb, tb_refile = 0.0, 0.0, 0.0, 0.0, {}, 0.0, 0.0
    for r in regions:
        X, Xq, y = [], [], []
        for k in turns:
            q = quarter(weeks[k])
            d4 = [1.0 if q[1] == j else 0.0 for j in (1, 2, 3, 4)]
            X.append(d4 + months(quarter(weeks[k - 1]), r))
            Xq.append(d4 + [pool[(r, quarter(weeks[k - 1]))]])
            y.append(s[r][weeks[k]] - s[r][weeks[k - 1]])
        b, V = lsq(X, y)
        x = np.array([0, 0, 0, 1.0] + months(closing, r))
        tot += s[r][last] + float(x @ b)
        var += float(x @ V @ x)
        refile += float(np.array(months(closing, r)) @ b[4:])
        without += s[r][last] + b[3]
        slopes[r] = list(b[4:])
        bq, _ = lsq(Xq, y)
        tb += s[r][last] + bq[3] + bq[4] * pool[(r, closing)]
        tb_refile += bq[4] * pool[(r, closing)]
    # the national rival: the national step on the national pool, one intercept per quarter of the year
    X, y = [], []
    for k in turns:
        q = quarter(weeks[k])
        X.append([1.0 if q[1] == j else 0.0 for j in (1, 2, 3, 4)] + [sum(pool[(r, quarter(weeks[k - 1]))]
                                                                         for r in regions)])
        y.append(nat[weeks[k]] - nat[weeks[k - 1]])
    b, _ = lsq(X, y)
    nat_rival = nat[last] + b[3] + b[4] * sum(pool[(r, closing)] for r in regions)
    # the default path: each week over its centred 52-week mean, averaged by week of the quarter and quarter over
    # 2022 to 2025; the last four weeks deseasonalised and averaged; times the factor of the quarter's first week
    kq, prev = [], None
    for d in weeks:
        kq.append(0 if prev is None or quarter(d) != quarter(prev) else kq[-1] + 1)
        prev = d
    vals = [nat[d] for d in weeks]
    fac = {}
    for i, d in enumerate(weeks):
        if dt.date(2022, 1, 2) <= d <= dt.date(2025, 12, 28) and i - 26 >= 0 and i + 25 < len(weeks):
            ma = sum(vals[i - 26:i + 26]) / 52.0
            fac.setdefault((kq[i], quarter(d)[1]), []).append(vals[i] / ma)
    fac = {k: sum(v) / len(v) for k, v in fac.items()}
    lvl = sum(vals[i] / fac[(kq[i], quarter(weeks[i])[1])] for i in range(len(weeks) - 4, len(weeks))) / 4.0
    default = lvl * fac[(0, target_q[1])]
    wci = sum(pool[(r, closing)] for r in ("Western", "Coastal", "Island"))
    sep = sum(months(closing, r)[2] for r in ("Western", "Coastal", "Island"))
    return dict(call=tot, se=math.sqrt(var), refile=refile, without=without, slopes=slopes, base=nat[last],
                pool=sum(pool[(r, closing)] for r in regions), wci_share=wci / sum(pool[(r, closing)] for r in regions),
                sep_share=sep / wci, national=nat_rival, default=default, turns=len(turns), last=last, tb=tb,
                tb_refile=tb_refile)


# ---------------------------------------------------------------------------------------------------- Ask A
LN = re.compile(r"ln[\s-]*2026[\s-]*0*(\d+)", re.I)
ES = re.compile(r"es\s*/?\s*(\d{2})\s*/\s*0*(\d+)", re.I)


def ref_of(text):
    m = LN.search(text)
    if m:
        return "LN-2026-%05d" % int(m.group(1))
    m = ES.search(text)
    if m:
        return "ES/%s/%04d" % (m.group(1), int(m.group(2)))
    return None


def withdrawn_refs(notes):
    out = set()
    for r in notes:
        t = r["note"].lower()
        if any(w in t for w in ("considering", "may withdraw", "thinks they may")):
            continue
        if "withdr" in t or "w/drawn" in t:
            ref = ref_of(r["reference"])
            if ref:
                out.add(ref)
    return out


def day(v):
    if isinstance(v, dt.datetime):
        return v.date()
    t = str(v).strip()
    m = re.fullmatch(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", t)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return dt.date.fromisoformat(t[:10])


def ask_a(target):
    reg = rows(find(target, "regions_"))
    town = {r["locality"]: r["region"] for r in reg}
    code = {r["region_code"]: r["region"] for r in reg}
    regions = list(dict.fromkeys(r["region"] for r in reg))
    notes = rows(find(target, "es_case_notes"))
    gone = withdrawn_refs(notes)
    portal = {}
    for r in rows(find(target, "employer_portal_notices")):
        portal.setdefault(r["notice_no"], []).append(r)
    wb = openpyxl.load_workbook(find(target, "es_layoff_notice_register"), data_only=True)
    vals = list(wb["Notices"].iter_rows(values_only=True))
    h = [i for i, r in enumerate(vals) if r and r[0] == "ES ref"][0]
    hdr = vals[h]
    register = {}
    for r in vals[h + 1:]:
        if r and r[0]:
            d = dict(zip(hdr, r))
            register.setdefault(d["ES ref"], []).append(d)
    items = []
    keys = {}
    for no, ls in portal.items():
        if ls[0]["status"] == "Superseded" or ls[0]["notice_type"] != "Layoff":
            continue
        it = dict(refs={no}, first=day(ls[0]["first_layoff"]),
                  sites=[(town[x["site_town"]], int(x["workers"])) for x in ls])
        key = (ls[0]["business_no"], it["first"], tuple(sorted((x["site_town"], int(x["workers"])) for x in ls)))
        keys.setdefault(key, []).append(it)
        items.append(it)
    for ref, ls in register.items():
        if ls[0]["Status"] != "Open" or ls[0]["Type"] != "Layoff":
            continue
        first = day(ls[0]["First layoff"])
        key = (str(ls[0]["Business no."]), first, tuple(sorted((x["Town"], int(x["Workers"])) for x in ls)))
        if key in keys:
            keys[key][0]["refs"].add(ref)       # re-keyed onto the portal: one notice under two numbers
            continue
        items.append(dict(refs={ref}, first=first, sites=[(code[x["Region"]], int(x["Workers"])) for x in ls]))
    periods = [("11-31 Oct", dt.date(2026, 10, 11), dt.date(2026, 10, 31)),
               ("Nov", dt.date(2026, 11, 1), dt.date(2026, 11, 30)), ("Dec", dt.date(2026, 12, 1), dt.date(2026, 12, 31))]
    out = {(r, p): 0 for r in regions for p, _, _ in periods}
    for it in items:
        if it["refs"] & gone:
            continue
        for p, a, b in periods:
            if a <= it["first"] <= b:
                for r, w in it["sites"]:
                    out[(r, p)] += w
    return out, regions, periods


# ---------------------------------------------------------------------------------------------------- Ask B
def ask_b(target):
    group_of = {r["division"]: r["group"] for r in rows(find(target, "uib_industry_divisions"))}
    wb = openpyxl.load_workbook(find(target, "sic_2006_sic_2023"), data_only=True)
    vals = list(wb.active.iter_rows(values_only=True))
    h = [i for i, r in enumerate(vals) if r and r[0] == "SIC 2006 division"][0]
    old = {}
    for r in vals[h + 1:]:
        if r and r[0]:
            old.setdefault(str(r[0]), set()).add(group_of[str(r[2])])
    assert all(len(v) == 1 for v in old.values())
    old = {k: next(iter(v)) for k, v in old.items()}
    tot = {}
    for r in rows(find(target, "ic_open_data_by_industry")):
        if r["claim_type"] not in ("N", "A"):
            continue
        d = dt.date.fromisoformat(r["week"])
        sat = d.weekday() == 5
        sun = d - dt.timedelta(days=6) if sat else d
        if not 7 <= sun.month <= 9 or sun.year not in (2025, 2026):
            continue
        g = old[r["division"]] if sat else group_of[r["division"]]
        tot[(sun.year, g)] = tot.get((sun.year, g), 0) + int(r["claims"])
    groups = list(dict.fromkeys(group_of[k] for k in sorted(group_of, key=lambda c: int(c))))
    return {g: (tot[(2026, g)] / tot[(2025, g)] - 1) * 100 for g in set(group_of.values())}, tot


# ---------------------------------------------------------------------------------------------------- the goldens
def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", " ", x)))


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    bad = []

    def ok(label, cond, detail=""):
        if not cond:
            bad.append("%s %s" % (label, detail))
    c = the_call(target)
    call = half_up(c["call"], 1000)
    ok("V call 17,000 from the shipped files", call == 17000, c["call"])
    ok("V the call is two bins clear of the seasonal default path", half_up(c["default"], 1000) <= call - 2000,
       c["default"])
    ok("V the regions on the quarter taken whole file two bins low", half_up(c["tb"], 1000) == call - 2000, c["tb"])
    ok("V the national rate files four bins low", half_up(c["national"], 1000) == call - 4000, c["national"])
    ok("V one standard error leaves the call's thousand", half_up(c["call"] - c["se"], 1000) == call ==
       half_up(c["call"] + c["se"], 1000), c["se"])
    ok("V 50 quarter turns", c["turns"] == 50, c["turns"])
    ok("V refiled claims between 5,000 and 6,000", 5000 <= c["refile"] <= 6000, c["refile"])
    ok("V the rest of the week between 11,000 and 12,000", 11000 <= c["without"] <= 12000, c["without"])
    ok("V the timing-blind refiling between 3,000 and 4,000", 3000 <= c["tb_refile"] <= 4000, c["tb_refile"])
    ok("V in Western, Coastal and Island two thirds to nine tenths of a quarter's last-month refusals file again, "
       "under one in five of its earlier months'", all(2 / 3 <= c["slopes"][r][2] <= 0.9 and c["slopes"][r][1] < 0.2 and
                                                      c["slopes"][r][0] < 0.2 for r in ("Western", "Coastal", "Island")),
       c["slopes"])
    a, regions, periods = ask_a(target)
    b, _ = ask_b(target)
    wb = openpyxl.load_workbook(os.path.join(golden, "ic_preview_2026-10-10.xlsx"), data_only=True)
    ok("V golden workbook carries the call", wb["Call"]["B4"].value == call, wb["Call"]["B4"].value)
    work = {r[0]: r[1] for r in wb["Call"].iter_rows(min_row=4, max_row=20, values_only=True) if r[0]}
    ok("V golden workbook carries the third quarter's determinations, their three-region part and its September part",
       work.get("Monetarily ineligible determinations, claims weeks of July to September 2026") == c["pool"] and
       work.get("  of which Western, Coastal and Island (%)") == dp1(100 * c["wci_share"]) and
       work.get("  of which Western, Coastal and Island, made in September (%)") == dp1(100 * c["sep_share"]), work)
    ws = wb["Layoff notices"]
    got = {}
    for r in ws.iter_rows(min_row=5, max_row=4 + len(regions), values_only=True):
        for (p, _, _), v in zip(periods, r[1:4]):
            got[(r[0], p)] = v
    ok("V golden workbook carries every Ask A cell", got == a, [k for k in a if got.get(k) != a[k]])
    ws = wb["Claims by industry"]
    gb = {r[0]: r[3] for r in ws.iter_rows(min_row=5, max_row=18, values_only=True)}
    ok("V golden workbook carries every Ask B change", all(abs(gb[g] - dp1(b[g])) < 1e-9 for g in b),
       [g for g in b if abs(gb.get(g, 1e9) - dp1(b[g])) > 1e-9])
    txt = docx_text(os.path.join(golden, "ic_preview_2026-10-10.docx"))
    ok("V the preview opens with the call", "about 17,000" in txt[:400], txt[:200])
    ok("V the preview names the week", "10 October 2026" in txt[:600])
    if bad:
        for x in bad:
            print("VERIFY FAIL", x)
        raise SystemExit(1)
    print("verify.py: the call %.0f (%d), se %.0f, refiled %.0f, without %.0f, timing-blind %.0f, default %.0f, "
          "national %.0f; Ask A %d cells, Ask B %d groups; goldens agree" % (
              c["call"], call, c["se"], c["refile"], c["without"], c["tb"], c["default"], c["national"], len(a), len(b)))
    return c, a, b


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
