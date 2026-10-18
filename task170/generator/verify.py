"""Independent verifier: reads only the shipped bundle (no generator module, no generator state) and recomputes the
call, its components and every ask answer on its own code path, then compares them with figures.json.

    python3 verify.py <target>        exit 0 when every figure reproduces"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import sys
import zipfile
import re

D = dt.date
DPM = 30.4375
COUNT = D(2026, 8, 31)
PALLET = 84 * 96
FAILS = []


def ok(cond, label):
    print(("PASS  " if cond else "FAIL  ") + label)
    if not cond:
        FAILS.append(label)


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def xlsx_sheet(path, sheet):
    """Read a worksheet's cell values with the standard library (shared strings resolved)."""
    z = zipfile.ZipFile(path)
    wb = z.read("xl/workbook.xml").decode()
    names = re.findall(r'<sheet name="([^"]+)" sheetId="\d+" r:id="rId(\d+)"', wb)
    rid = [r for n, r in names if n == sheet][0]
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    target = re.search(r'<Relationship Id="rId%s"[^>]*Target="([^"]+)"' % rid, rels).group(1)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S):
            ss.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    data = z.read("xl/" + target.lstrip("/").replace("xl/", "")).decode()
    out = {}
    for m in re.finditer(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', data, re.S):
        col, row, attrs, inner = m.group(1), int(m.group(2)), m.group(3), m.group(4) or ""
        v = re.search(r"<v>(.*?)</v>", inner)
        if v is None:
            continue
        val = v.group(1)
        if 't="s"' in attrs:
            val = ss[int(val)]
        else:
            try:
                val = float(val)
            except ValueError:
                pass
        out.setdefault(row, {})[col] = val
    return out


def add_m(d, k):
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return D(y, m, min(d.day, 28))


def month_ends():
    out = []
    for k in range(1, 11):
        y, m = 2026 + (8 + k - 1) // 12, (8 + k - 1) % 12 + 1
        nxt = D(y + (m == 12), m % 12 + 1, 1)
        out.append(nxt - dt.timedelta(days=1))
    return out


def sf(z):
    """Upper tail of the standard normal."""
    return 0.5 * math.erfc(z / math.sqrt(2.0))


# ---------------------------------------------------------------------------------------------------- the call
def children_need(t):
    codes = {r["legacy_register_text"]: r["regimen_code"] for r in rows(os.path.join(t, "national_regimen_codes_2026.csv"))}
    cw = {r["art_no"]: r["upid"] for r in rows(os.path.join(t, "art_number_crosswalk_2024-06.csv"))}
    visits = {}
    seen = set()
    for r in sorted(rows(os.path.join(t, "paed_register_visits_epr_2024-06_2026-08.csv")), key=lambda r: r["synced_at"]):
        key = (r["upid"], r["facility_code"], r["visit_date"], r["encounter_type"], r["weight_kg"], r["regimen_code"],
               r["months_dispensed"], r["next_appointment"])
        if key in seen:
            continue
        seen.add(key)
        d = D.fromisoformat(r["visit_date"])
        visits[(r["upid"], d)] = (float(r["weight_kg"]) if r["weight_kg"] else None, r["regimen_code"],
                                  int(r["months_dispensed"]), D.fromisoformat(r["next_appointment"]))
    for r in rows(os.path.join(t, "paed_register_visits_legacy_2023-01_2024-06.csv")):
        u = cw[r["art_no"]]
        dd, mm, yy = r["visit_date"].split("/")
        d = D(int(yy), int(mm), int(dd))
        if (u, d) in visits:
            continue
        nd, nm, ny = r["next_visit"].split("/")
        visits[(u, d)] = (float(r["weight_kg"]) if r["weight_kg"] else None, codes[r["regimen"]],
                          int(r["months_dispensed"]), D(int(ny), int(nm), int(nd)))
    by = {}
    for (u, d), v in visits.items():
        by.setdefault(u, []).append((d,) + v)
    pts = {r["upid"]: r for r in rows(os.path.join(t, "paed_register_patients_2026-09-02.csv"))}
    ends = month_ends()
    # exit hazards by age group, September 2025 to August 2026
    num, den = [0, 0], [0, 0]
    for k in range(12):
        m0 = add_m(D(2025, 9, 1), k)
        m1 = add_m(m0, 1) - dt.timedelta(days=1)
        for p in pts.values():
            st = D.fromisoformat(p["art_start_date"])
            od = D.fromisoformat(p["outcome_date"]) if p["outcome_date"] else None
            if st > m1 or (od is not None and od < m0):
                continue
            age = (m0 - D.fromisoformat(p["date_of_birth"])).days / 365.25
            if age >= 20:
                continue
            g = 1 if age >= 12 else 0
            den[g] += 1
            if od is not None and m0 <= od <= m1 and p["outcome"] in ("Lost to follow-up", "Transferred out", "Died"):
                num[g] += 1
    h = [num[0] / den[0], num[1] / den[1]]

    def surv(dob):
        s, out = 1.0, []
        for e in ends:
            s *= 1 - (h[1] if (e - dob).days / 365.25 >= 12 else h[0])
            out.append(s)
        return out
    on, cand = [], []
    for u, p in pts.items():
        dob = D.fromisoformat(p["date_of_birth"])
        if dob <= D(2011, 8, 31) or D.fromisoformat(p["art_start_date"]) > COUNT:
            continue
        if p["outcome_date"] and D.fromisoformat(p["outcome_date"]) <= COUNT:
            continue
        vs = sorted(v for v in by.get(u, []) if v[0] <= COUNT)
        if not vs:
            continue
        reg = vs[-1][2]
        if reg == "A1-TLD":
            on.append(u)
        elif reg in ("P1-AB3D10", "P1-AB3D50"):
            cand.append(u)
    # fits and scatter
    fit = {}
    ss, dof = 0.0, 0.0
    for u in cand:
        pts_ = [((v[0] - COUNT).days / DPM, v[1]) for v in by[u] if v[0] <= COUNT and v[1] is not None]
        n = len(pts_)
        if n < 3:
            continue
        sx = sum(x for x, _ in pts_)
        sy = sum(y for _, y in pts_)
        sxx = sum(x * x for x, _ in pts_)
        sxy = sum(x * y for x, y in pts_)
        dn = n * sxx - sx * sx
        if dn <= 1e-9:
            continue
        b = (n * sxy - sx * sy) / dn
        a = (sy - b * sx) / n
        fit[u] = (a, b)
        ss += sum((y - a - b * x) ** 2 for x, y in pts_)
        dof += n - 2
    sig = math.sqrt(ss / dof)
    # the share of first readings of 30 kg or more since the 2026 guidelines, on a paediatric first line at the
    # weighing before, that did not move the child onto TLD at that visit
    held = moved = 0
    for u, vs in by.items():
        ws_ = sorted(v for v in vs if v[0] <= COUNT and v[1] is not None)
        for j, v in enumerate(ws_):
            if v[0] >= D(2026, 3, 1) and v[1] >= 30.0:
                if j > 0 and ws_[j - 1][2] in ("P1-AB3D10", "P1-AB3D50"):
                    if v[2] == "A1-TLD":
                        moved += 1
                    else:
                        held += 1
                break
    lag = held / (held + moved)
    lastyr = [v for u in cand for v in by[u] if add_m(COUNT, -12) < v[0] <= COUNT]
    q = 1 - sum(1 for v in lastyr if v[1] is None) / len(lastyr)
    Cm = [0.0] * 10
    for u in on:
        for k, s in enumerate(surv(D.fromisoformat(pts[u]["date_of_birth"]))):
            Cm[k] += s
    for u in cand:
        vs = sorted(v for v in by[u] if v[0] <= COUNT)
        last = vs[-1]
        step, d = last[3], last[4]
        while d <= COUNT:
            d = add_m(d, step)
        sch = []
        while d <= ends[-1]:
            sch.append(d)
            d = add_m(d, step)
        if u in fit:
            a, b = fit[u]
            mus = [a + b * (x - COUNT).days / DPM for x in sch]
        else:
            lw = [v[1] for v in vs if v[1] is not None][-1]
            mus = [lw] * len(sch)
        free, hold, done = 1.0, 0.0, 0.0
        cum = [0.0] * len(sch)
        for j, mu in enumerate(mus):
            pj = sf((30.0 - mu) / sig) * q
            mh = hold * q
            trig = free * pj
            done += mh + trig * (1 - lag)
            hold += trig * lag - mh
            free -= trig
            cum[j] = done
        S = surv(D.fromisoformat(pts[u]["date_of_birth"]))
        for k, e in enumerate(ends):
            done = [cum[j] for j, x in enumerate(sch) if x <= e]
            Cm[k] += (done[-1] if done else 0.0) * S[k]
    need = sum(round(x) for x in Cm) + 6 * round(Cm[-1])
    return need, len(on), len(cand), sig, lag


def call(t):
    proj = xlsx_sheet(os.path.join(t, "art_patient_projection_2026-09_2027-06.xlsx"), "Projection")
    nat = [r for r in proj.values() if r.get("A") == "National"][0]
    months = [nat[c] for c in "BCDEFGHIJK"]
    adults = sum(months) + 6 * months[-1]
    cons, mx = sum(months), 6 * months[-1]
    st = xlsx_sheet(os.path.join(t, "cms_stock_status_2026-08-31.xlsx"), "Stock on hand")
    soh = sum(r["F"] for k, r in st.items() if k > 1 and r.get("E") == "Usable")
    oo = xlsx_sheet(os.path.join(t, "cms_stock_status_2026-08-31.xlsx"), "On order")
    shipped = sum(r["D"] for k, r in oo.items() if k > 1 and r.get("F") == "Confirmed")
    need, n_on, n_c, sig, lag = children_need(t)
    line1 = adults - soh - shipped
    return dict(adults=int(adults), cons=int(cons), mx=int(mx), soh=int(soh), shipped=int(shipped), children=need,
                on=n_on, cand=n_c, sig=sig, lag=lag, line1_unrounded=line1, line1=int(round(line1 / PALLET)),
                line2_unrounded=need, line2=int(round(need / PALLET)))


# ---------------------------------------------------------------------------------------------------- the asks
def asks(t):
    reg = rows(os.path.join(t, "facility_registry_extract_2026-09-01.csv"))
    byc = {}
    for r in reg:
        byc.setdefault(r["mfl_code"], []).append(r)

    def region(code, d):
        found = [r["region"] for r in byc.get(code, [])
                 if r["opened_on"][:7] <= d.isoformat()[:7] <= (r["closed_on"][:7] if r["closed_on"] else "9999-12")]
        return found[0] if len(found) == 1 else None
    acc = {r["account"]: r["mfl_code"] for r in rows(os.path.join(t, "cms_customer_accounts_2026-09-02.csv"))}
    pod = {r["delivery_no"]: r for r in rows(os.path.join(t, "cms_pod_2025-07_2026-08.csv"))}
    cyc = {"C4": (D(2025, 7, 1), D(2025, 12, 31)), "C5": (D(2026, 1, 1), D(2026, 6, 30))}
    A, B = {}, {}
    for ln in rows(os.path.join(t, "cms_deliveries_tld_2025-07_2026-08.csv")):
        if ln["delivery_type"] != "LF":
            continue
        p = pod.get(ln["delivery_no"])
        if p is None or p["signed_by"].startswith("Refused"):
            continue
        d = D.fromisoformat(p["signed_on"])
        for c, (lo, hi) in cyc.items():
            if lo <= d <= hi:
                r = region(acc[ln["customer"]], d)
                A[(r, c)] = A.get((r, c), 0) + int(ln["qty"])
    lm = json.load(open(os.path.join(t, "lmis_monthly_reports_2025-07_2026-08.json"), encoding="utf-8"))
    for q in lm["requisitions"]:
        if q["status"] != "Approved":
            continue
        y, m = int(q["period"][:4]), int(q["period"][5:])
        d = D(y, m, 15)
        v = sum(li["quantityDispensed"] for li in q["lineItems"] if li["product"].startswith("TDF/3TC/DTG 300/300/50 mg tablets, 30"))
        for c, (lo, hi) in cyc.items():
            if lo <= d <= hi:
                r = region(q["facilityCode"], d)
                B[(r, c)] = B.get((r, c), 0) + v
    return A, B


def main(t):
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    c = call(t)
    ok(c["adults"] == fig["adults"], "V1 adults' need %d recomputes from the projection" % c["adults"])
    ok(c["cons"] == fig["adult_consumption"] and c["mx"] == fig["adult_max_stock"], "V1 their consumption %d and "
       "maximum stock %d recompute" % (c["cons"], c["mx"]))
    ok(c["soh"] == fig["soh"], "V2 usable stock %d recomputes from the stock status report" % c["soh"])
    ok(c["shipped"] == fig["shipped"], "V3 confirmed shipments %d recompute" % c["shipped"])
    ok(c["on"] == fig["on_tld"], "V4 children on TLD at the count %d" % c["on"])
    ok(c["cand"] == fig["candidates"], "V5 children on a paediatric first line %d" % c["cand"])
    ok(abs(c["sig"] - fig["sigma"]) < 0.005, "V6 residual scatter %.3f kg" % c["sig"])
    ok(abs(100 * c["lag"] - fig["held_back_pct"]) < 0.05, "V6 readings of 30 kg or more held back since March 2026: "
       "%.1f%%" % (100 * c["lag"]))
    ok(c["line1"] == fig["line1"], "V7 line 1 recomputes: %d pallets (unrounded %.0f bottles)" % (c["line1"], c["line1_unrounded"]))
    ok(c["line2"] == fig["call"] and c["line2_unrounded"] == fig["call_unrounded"], "V7 line 2 recomputes: %d "
       "pallets (unrounded %d bottles)" % (c["line2"], c["line2_unrounded"]))
    edge = PALLET / 2 - abs(c["line2_unrounded"] - c["line2"] * PALLET)
    ok(edge >= PALLET / 8, "V8 line 2 sits %.0f bottles inside its pallet" % edge)
    A, B = asks(t)
    for k, v in fig["asks"].items():
        kind, r, cy = k.split()
        got = (A if kind == "delivered" else B).get((r, cy), 0)
        ok(got == v, "V9 %s recomputes: %d" % (k, got))
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sub = open(os.path.join(task, "submission.md")).read()
    ok("%d pallets of TLD 30s (%s bottles)" % (c["line2"], "{:,}".format(c["line2"] * PALLET)) in sub,
       "V10 the write-up states line 2, %d pallets" % c["line2"])
    gx = os.path.join(task, "golden", "c7_tld_order.xlsx")
    sh = xlsx_sheet(gx, "C7 order")
    vals = [v.get("B") for k, v in sorted(sh.items())]
    want = [fig["line1_bottles"], fig["call_bottles"], fig["call_unrounded"], fig["adult_consumption"],
            fig["adult_max_stock"], -fig["soh"], -fig["shipped"], fig["on_tld"], fig["candidates"]]
    ok(all(w in vals for w in want), "V11 the order workbook carries both lines and their components as the write-up "
       "states them")
    rg = xlsx_sheet(gx, "Regions C4 C5")
    got = {}
    for k, v in rg.items():
        if k > 1 and v.get("A") in ("Capital", "Central", "Northern", "Eastern", "Southern", "Western"):
            for col, kind, cy in (("B", "delivered", "C4"), ("C", "delivered", "C5"), ("D", "dispensed", "C4"),
                                  ("E", "dispensed", "C5")):
                got["%s %s %s" % (kind, v["A"], cy)] = int(v[col])
    ok(got == fig["asks"], "V12 the workbook's region table carries the 24 figures of the write-up")
    print("%d checks, %d failed" % (len([1 for _ in fig["asks"]]) + 13, len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
