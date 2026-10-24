"""Independent verifier for task482: reads only the shipped files under target/ and recomputes the call and ask A's
figures with its own code, then compares them with generator/figures.json.

    python3 task482/generator/verify.py     # exit 1 on any mismatch
"""
import collections
import csv
import datetime as dt
import json
import os
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
DAY0 = dt.date(2016, 10, 1)
FY0, FY1 = (dt.date(2025, 10, 1) - DAY0).days, (dt.date(2026, 10, 1) - DAY0).days
CLOSE = (dt.date(2027, 1, 1) - DAY0).days
CAP = 35361.44
H = 6000


def d(s):
    return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8])) if s.strip() else None


def n(x):
    return (x - DAY0).days


def load():
    reg = json.load(open(os.path.join(TARGET, "provider_numbers.json")))
    ours = [p["provider_number"] for p in reg["provider_numbers"]]
    names = {p["provider_number"]: p["program"] for p in reg["provider_numbers"]}
    ext = []
    with open(os.path.join(TARGET, "medicare_hospice_benefit_periods_20270105.txt")) as f:
        for line in f:
            if line[0] != "D":
                continue
            ext.append(dict(mbi=line[1:12], bp=int(line[12:15]), elect=d(line[15:23]), ccn=line[23:29], start=d(line[29:37]),
                            end=d(line[37:45]), days=int(line[45:49]), dod=d(line[49:57])))
    cw = {r["hicn"]: r["mbi"] for r in csv.DictReader(open(os.path.join(TARGET, "hicn_mbi_crosswalk.csv")))}
    grp = {r["icd10_code"]: r["census_group"] for r in csv.DictReader(open(os.path.join(TARGET, "diagnosis_groups.csv")))}
    group, when = {}, {}
    for r in csv.DictReader(open(os.path.join(TARGET, "wendleglen_emr_admissions.csv"))):
        if r["payer"] != "Medicare":
            continue
        m = cw.get(r["medicare_id"], r["medicare_id"])
        if m not in when or r["admit_date"] >= when[m]:
            when[m], group[m] = r["admit_date"], grp[r["primary_dx"]]
    wb = openpyxl.load_workbook(os.path.join(TARGET, "fallowmere_census_register_20250228.xlsx"), read_only=True)
    ws = wb["Census Export"]
    for row in ws.iter_rows(min_row=5, values_only=True):
        if not row or not row[0]:
            continue
        acct, mno, dob, sex, admit, disch, status, dx, payer = row[:9]
        m = cw.get(mno, mno)
        dx = dx if "." in dx or len(dx) <= 3 else dx[:3] + "." + dx[3:]
        a = admit.date().isoformat() if hasattr(admit, "date") else str(admit)
        if m not in when or a > when[m]:
            when[m], group[m] = a, grp[dx]
    return ours, names, ext, group


def km_s(t, o):
    t = np.clip(np.asarray(t, int), 0, H)
    o = np.asarray(o, bool)
    ev = np.bincount(t[o], minlength=H + 1)
    ce = np.bincount(t[~o], minlength=H + 1)
    risk = len(t) - np.concatenate([[0], np.cumsum(ev + ce)[:-1]])
    return np.cumprod(1 - np.where(risk > 0, ev / np.maximum(risk, 1), 0.0))


def resid(S, e):
    e = int(min(max(e, 0), H))
    base = S[e - 1] if e > 0 else 1.0
    return float(S[e:].sum() / base) if base > 0 else 0.0


def cif(rows, kind):
    t = np.array([min(max(int(x), 0), H) for x, _ in rows])
    k = np.array([y for _, y in rows])
    a = np.bincount(t[k == kind], minlength=H + 1)
    b = np.bincount(t[(k != kind) & (k != "cen")], minlength=H + 1)
    c = np.bincount(t[k == "cen"], minlength=H + 1)
    risk = len(t) - np.concatenate([[0], np.cumsum(a + b + c)[:-1]])
    s, f = 1.0, 0.0
    S, F = np.ones(H + 1), np.zeros(H + 1)
    for i in range(H + 1):
        if risk[i] > 0:
            f += s * a[i] / risk[i]
            s *= 1 - (a[i] + b[i]) / risk[i]
        S[i], F[i] = s, f
    return S, F


def rate_sheet():
    """The FY2026 rates and labor shares, each checked against the rate sheet's printed table."""
    from pdfminer.high_level import extract_text
    text = " ".join(extract_text(os.path.join(TARGET, "fy2026_hospice_payment_rates.pdf")).split())
    printed = ["230.83", "181.94", "69.76", "532.48", "1,199.86", "66.0%", "75.2%", "61.0%", "63.5%"]
    missing = [v for v in printed if v not in text]
    assert not missing, "rate sheet lacks %s" % missing
    return ({"R_HI": 230.83, "R_LO": 181.94, "C": 69.76, "I": 532.48, "G": 1199.86},
            {"R": 0.660, "C": 0.752, "I": 0.610, "G": 0.635})


def routine_count(ext):
    """Each beneficiary's day -> position in the routine home care count: every day of hospice care at any hospice,
    the count running on across a gap of 60 days or fewer between stays (the rate sheet)."""
    by = collections.defaultdict(list)
    for r in ext:
        by[r["mbi"]].append((n(r["start"]), r["days"]))
    out = {}
    for m, periods in by.items():
        idx, cnt, prev = {}, 0, None
        for s0, k in sorted(periods):
            if prev is not None and s0 - prev > 60:
                cnt = 0
            for day in range(s0, s0 + k):
                cnt += 1
                idx[day] = cnt
            prev = s0 + k
        out[m] = idx
    return out


def price(days, rates, labor, wi, idx):
    fixed = lab = 0.0
    for day, lv, q in days:
        if lv == "C":
            pay = rates["C"] * q / 4.0
        elif lv == "R":
            pay = rates["R_HI"] if idx.get(day, 1) <= 60 else rates["R_LO"]
        else:
            pay = rates[lv]
        fixed += pay * (1 - labor[lv])
        lab += pay * labor[lv]
    return round(fixed + lab * wi, 2)


def main():
    ours, names, ext, group = load()
    own = set(ours)
    stays = collections.defaultdict(list)
    tmp = collections.defaultdict(list)
    for r in ext:
        tmp[(r["mbi"], r["elect"])].append(r)
    dod = {}
    for (m, e), rows in tmp.items():
        rows.sort(key=lambda r: r["start"])
        days = sum(r["days"] for r in rows)
        s = n(e)
        dd = rows[0]["dod"]
        dod[m] = n(dd) if dd else None
        is_open = rows[-1]["end"] is None
        died = (not is_open) and dd is not None and n(dd) == s + days - 1
        stays[m].append(dict(s=s, n=days, e=s + days, open=is_open, died=died, first=rows[0]["ccn"], last=rows[-1]["ccn"],
                             segs=[(r["ccn"], n(r["start"]), r["days"]) for r in rows]))
    for m in stays:
        stays[m].sort(key=lambda x: x["s"])
    # experience by (provider number, group)
    st_rows, lv_rows, rt_rows = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    for m, lst in stays.items():
        g = group.get(m)
        if g is None:
            continue
        for k, x in enumerate(lst):
            if x["s"] >= CLOSE:
                continue
            if x["first"] in own and x["s"] >= 0:
                st_rows[(x["first"], g)].append((x["n"], "cen" if x["open"] else ("death" if x["died"] else "live")))
            if x["open"] or x["died"] or x["last"] not in own or x["e"] < 0 or x["e"] > CLOSE:
                continue
            nx = lst[k + 1] if k + 1 < len(lst) and lst[k + 1]["s"] < CLOSE else None
            if nx:
                lv_rows[(x["last"], g)].append((nx["s"] - x["e"], "ret"))
                rt_rows[(x["last"], g)].append((nx["n"], not nx["open"]))
            elif dod[m] is not None and dod[m] <= CLOSE:
                lv_rows[(x["last"], g)].append((dod[m] - x["e"], "death"))
            else:
                lv_rows[(x["last"], g)].append((CLOSE - x["e"], "cen"))
    cache = {}

    def model(key):
        if key in cache:
            return cache[key]
        sr = st_rows.get(key, [])
        S = km_s([a for a, _ in sr], [b != "cen" for _, b in sr])
        Ss, Fl = cif([(a, "ret" if b == "live" else b) for a, b in sr], "ret")
        Sr, Fr = cif(lv_rows.get(key, []), "ret")
        rr = rt_rows.get(key, [])
        A = float(km_s([a for a, _ in rr], [b for _, b in rr]).sum()) if rr else 0.0
        Sret = km_s([a for a, _ in rr], [b for _, b in rr]) if rr else np.zeros(H + 1)
        cache[key] = (S, Ss, Fl, Sr, Fr, A, Sret)
        return cache[key]

    counts = collections.defaultdict(float)
    for m, lst in stays.items():
        fy, kn, home = {}, 0, None
        for x in lst:
            if x["s"] >= CLOSE:
                continue
            kn += min(x["n"], CLOSE - x["s"])
            for ccn, s, k in x["segs"]:
                if ccn in own:
                    a, z = max(s, FY0), min(s + k, FY1)
                    if z > a:
                        fy[ccn] = fy.get(ccn, 0) + z - a
                    if s < CLOSE:
                        home = ccn
        if not fy:
            continue
        S, Ss, Fl, Sr, Fr, A, Sret = model((home, group[m]))
        last = [x for x in lst if x["s"] < CLOSE][-1]
        if last["open"]:
            e = CLOSE - last["s"]
            if last["first"] not in own:
                fut = resid(Sret, e)
            else:
                ei = min(e, H)
                pl = (Fl[-1] - Fl[ei]) / Ss[ei] if Ss[ei] > 1e-12 else 0.0
                fut = resid(S, e) + pl * Fr[-1] * A
        elif last["died"] or (dod[m] is not None and dod[m] <= CLOSE - 1):
            fut = 0.0
        else:
            s_out = min(CLOSE - last["e"], H)
            p = (Fr[-1] - Fr[s_out]) / Sr[s_out] if Sr[s_out] > 1e-12 else 0.0
            fut = p * A
        for ccn, dd in fy.items():
            counts[ccn] += dd / (kn + fut)
    # payments and the repayment
    pay = collections.defaultdict(float)
    paid_keys = collections.defaultdict(int)
    for r in csv.DictReader(open(os.path.join(TARGET, "remittance_register_fy2026.csv"))):
        if r["record_type"] != "CLP":
            continue
        pay[r["provider_number"]] += float(r["paid_amount"]) + float(r["adj_carc_253"])
        paid_keys[r["patient_control_no"]] += 1 if r["claim_status"] == "1" else -1
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    inv = {v: k for k, v in figs["provider_numbers"].items()}
    fal = figs["provider_numbers"]["FAL"]
    total = 0.0
    for ccn in ours:
        rep = max(0.0, 0.98 * (pay[ccn] - counts[ccn] * CAP))
        total += rep
        want = figs["repayment_usd"][inv[ccn]]
        if abs(rep - want) > 1.0:
            bad.append("%s repayment %.2f against %.2f" % (inv[ccn], rep, want))
        if abs(pay[ccn] - figs["payments_usd"][inv[ccn]]) > 0.05:
            bad.append("%s payments %.2f against %.2f" % (inv[ccn], pay[ccn], figs["payments_usd"][inv[ccn]]))
    if round(total / 1e6 + 1e-12, 1) != figs["call"]["total_musd"]:
        bad.append("total %.1f" % (total / 1e6))
    # ask A: the inpatient days Medicare paid for on the versions the register shows paid and not reversed, each
    # version repriced at its billed levels from the rate sheet and its provider number's wage index; where the payment
    # falls short, the count of its last general inpatient and respite days paid at the routine rate that closes the gap
    rates, labor = rate_sheet()
    wi = {p["provider_number"]: p["fy2026_wage_index_applied"]
          for p in json.load(open(os.path.join(TARGET, "provider_numbers.json")))["provider_numbers"]}
    tier = routine_count(ext)
    remitted, net = {}, collections.defaultdict(float)
    for r in csv.DictReader(open(os.path.join(TARGET, "remittance_register_fy2026.csv"))):
        if r["record_type"] != "CLP":
            continue
        amt = float(r["paid_amount"]) + float(r["adj_carc_253"])
        net[r["patient_control_no"]] += amt
        if r["claim_status"] == "1":
            remitted[r["patient_control_no"]] = amt
    lines = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(TARGET, "wendleglen_claim_lines_fy2026.csv"))):
        lines[r["claim_key"]].append(r)
    gip, irc = collections.Counter(), collections.Counter()
    unexplained = 0
    for key, rows in lines.items():
        if net.get(key, 0.0) <= 0.005:
            continue
        ccn, mbi = rows[0]["provider_number"], rows[0]["mbi"]
        days = []
        for r in rows:
            first = n(dt.date.fromisoformat(r["line_date"]))
            lv = {"0651": "R", "0652": "C", "0655": "I", "0656": "G"}[r["revenue_code"]]
            if lv == "C":
                days.append((first, "C", int(r["units"])))
            else:
                days += [(first + k, lv, 0) for k in range(int(r["units"]))]
        days.sort()
        want = remitted[key]
        g_n = sum(1 for d in days if d[1] == "G")
        i_n = sum(1 for d in days if d[1] == "I")
        found = None
        for kg in range(g_n + 1):
            for ki in range(i_n + 1):
                adj = list(days)
                for lv, k in (("G", kg), ("I", ki)):
                    for j in ([j for j, d in enumerate(adj) if d[1] == lv][-k:] if k else []):
                        adj[j] = (adj[j][0], "R", 0)
                if abs(price(adj, rates, labor, wi[ccn], tier.get(mbi, {})) - want) < 0.02:
                    found = (kg, ki)
                    break
            if found:
                break
        if found is None:
            unexplained += 1
            found = (0, 0)
        gip[ccn] += g_n - found[0]
        irc[ccn] += i_n - found[1]
    if unexplained:
        bad.append("%d paid claims whose payment no count of routine-paid days explains" % unexplained)
    print("verify: Fallowmere USD %.2f (%.1f), total %.1f, ask A %d provider numbers checked" % (
        max(0.0, 0.98 * (pay[fal] - counts[fal] * CAP)), max(0.0, 0.98 * (pay[fal] - counts[fal] * CAP)) / 1e6,
        total / 1e6, len(ours)))
    for b in bad:
        print("MISMATCH", b)
    print("verify: %s" % ("PASS" if not bad else "FAIL"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
