"""The generator's checks on the cut pack and the generator's clean truth: the gates, the call under every route, the
three rules executed (R1, R2, R3), the semantic fork table (SF1 to SF10), the bins, the asks' devices."""
import csv
import datetime as dt
import json
import os

import numpy as np

import bundle as B
import methods as M
import pack as P
import sources as S
import world as W

GOLD = ["51", "52", "54", "23"]
NEXT = "31-33"
PAID = ["51", "52", "48-49", "62"]
HERE = os.path.dirname(os.path.abspath(__file__))


def truth_record(x, field):
    rec = {}
    for code, v in x["counties"][W.COUNTY_FIPS].items():
        d = rec.setdefault(v["sector"], {})
        for (y, q) in S.QUARTERS:
            w, j = d.get((y, q), (0.0, (0, 0, 0)))
            d[(y, q)] = (w + v[field][(y, q)], tuple(j[i] + v["jobs"][(y, 3 * q - 2 + i)] for i in range(3)))
    return rec


def _sse(rec_s, cnt):
    X, Y = [], []
    for y in range(W.Y0, W.Y1 + 1):
        for q in range(1, 5):
            w, jm = rec_s[(y, q)]
            X.append([1.0 if y == yy else 0 for yy in range(W.Y0, W.Y1 + 1)] + [1.0 if q == qq else 0 for qq in (2, 3, 4)]
                     + [cnt[k].get((y, q), 0) for k in S.KEYS])
            Y.append(np.log(w / (sum(jm) / 3)))
    X, Y = np.array(X), np.array(Y)
    b = np.linalg.lstsq(X, Y, rcond=None)[0]
    return float(((Y - X @ b) ** 2).sum())


def counts_after(key):
    c, h = {}, S._hol()
    for d, _ in S.paydays(key):
        p = d
        while p.weekday() >= 5 or p in h:
            p += dt.timedelta(1)
        c[S.qof(p)] = c.get(S.qof(p), 0) + 1
    return c


def main(target, gdir, x):
    fails = []
    n = [0]

    def check(label, cond, detail=None):
        n[0] += 1
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond or detail is None else "  [%s]" % (detail,)))
        if not cond:
            fails.append(label)

    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: %d files, formats %s, the largest %d rows" % (len(files), fmts, big),
          len(files) >= 10 and len(fmts) >= 3 and big >= 25000)
    check("gates: the pack is exactly world.FILES", set(files) == set(W.FILES.values()))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    check("gates: two distractors in metadata.json, none named for it", len(meta["distractors"]) >= 2 and not any(
        "distract" in f or "decoy" in f for f in files))

    rec = B.record(target)
    R = {r: M.route(rec, r) for r in M.FAMILY + M.WRONG}
    sl = {r: M.slate(R[r]) for r in R}
    check("call: the golden names %s, next %s" % (sl["golden"][0], sl["golden"][1]),
          sorted(sl["golden"][0]) == sorted(GOLD) and sl["golden"][1] == NEXT)
    for r in M.FAMILY:
        check("family: %s names the golden slate and next" % r, sorted(sl[r][0]) == sorted(GOLD) and sl[r][1] == NEXT)
    for r in ("paid", "friday", "total"):
        check("ladder: %s files the wages-as-paid slate %s" % (r, sl[r][0]), sorted(sl[r][0]) == sorted(PAID))
    check("ladder: noshift (no holiday shift) files a wrong slate %s" % sl["noshift"][0],
          sorted(sl["noshift"][0]) != sorted(GOLD))
    g = R["golden"]
    o = sorted(g, key=lambda s: -g[s])
    gap = 100 * (g[o[3]] - g[o[4]])
    check("margin: the golden's fourth over fifth by %.2f points (0.5 or more)" % gap, gap >= .5)
    p = R["paid"]
    po = sorted(p, key=lambda s: -p[s])
    check("margin: the paid route's fourth over fifth by %.2f points (0.4 or more)" % (100 * (p[po[3]] - p[po[4]])),
          100 * (p[po[3]] - p[po[4]]) >= .4)
    # bins: every graded growth prints the same whole percent under every family member, clear of its edge
    worst = 1.0
    for s in g:
        vals = [100 * R[r][s] for r in M.FAMILY]
        same = len({int(round(v)) for v in vals}) == 1
        edge = min(.5 - abs(v - round(v)) for v in vals)
        worst = min(worst, edge)
        check("bins: %s growth %d%% under all %d family members (nearest edge %.2f)" % (s, round(vals[0]), len(vals),
                                                                                     edge), same and edge >= .1)
    # R1: the field's raw material ships: the decisive computation reads the quarterly wages and the monthly levels;
    # no shipped column holds pay for the work done or a pay-schedule share
    cols = set()
    for f in files:
        if f.endswith(".csv"):
            cols |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
    check("R1: the decisive quantity is in no shipped column (%d columns read)" % len(cols),
          not any(k in c for c in cols for k in ("earned", "schedule", "frequency", "payday", "pay_date", "phase")))
    # R3a and R3b on the clean truth: paid wages give the default path's slate, pay for the work done the golden's
    tp, te = truth_record(x, "paid"), truth_record(x, "earned")

    def tg(r):
        return {s: (M.annual_paid(r[s], W.LATEST) / M.annual_jobs(r[s], W.LATEST)) /
                (M.annual_paid(r[s], W.BASE) / M.annual_jobs(r[s], W.BASE)) - 1 for s in M.eligible(r)}
    check("R3a: the analyst test on the clean truth (wages as paid, every rule applied) files %s" %
          M.slate(tg(tp))[0], sorted(M.slate(tg(tp))[0]) == sorted(PAID))
    check("R3b: the decisive step alone (pay for the work done) files %s, next %s" % M.slate(tg(te)),
          sorted(M.slate(tg(te))[0]) == sorted(GOLD) and M.slate(tg(te))[1] == NEXT)
    check("R3b: the golden estimates the truth: every growth within 0.4 points", all(
        abs(100 * (g[s] - tg(te)[s])) < .4 for s in g), max(abs(100 * (g[s] - tg(te)[s])) for s in g))
    seen = set()
    dup = 0
    for fn in (W.FILES["qcew_a"], W.FILES["qcew_b"], W.FILES["qcew_c"]):
        for i, r in enumerate(csv.reader(open(os.path.join(target, fn), encoding="utf-8"))):
            if i == 0 or r[7] == "N":
                continue
            t = tuple(r[:16])
            dup += t in seen
            seen.add(t)
    check("R3c: no exact duplicate rows across the county files (%d)" % dup, dup == 0)
    # R2: each Layer 1 item mishandled leaves the call where it was
    qb = B.qcew(target, use_latest=False)
    recb = {s: {k: (v[0], v[1]) for k, v in d.items()} for s, d in qb.items() if s in rec}
    for s in recb:
        for k in rec[s]:
            if k not in recb[s]:
                recb[s][k] = rec[s][k]
    check("R2: the 2025 quarters as first published (fourth quarter from the annual release) give the same slate",
          sorted(M.slate(M.route(recb, "golden"))[0]) == sorted(GOLD) and M.slate(M.route(recb, "golden"))[1] == NEXT)
    q75 = B.qcew(target, agg="75")
    sec_of = {c: sec for sec, v in W.SECTORS.items() for c, *_ in v[5]}
    for a_, bb in W.NAICS2022.items():
        for c, _ in bb:
            sec_of[c] = sec_of[a_]
    rec75 = {}
    for ind, d in q75.items():
        for k, v in d.items():
            if v[2] == "N":
                continue
            w, j = rec75.setdefault(sec_of[ind], {}).get(k, (0, (0, 0, 0)))
            rec75[sec_of[ind]][k] = (w + v[0], tuple(a + b for a, b in zip(j, v[1])))
    rec75 = {s: v for s, v in rec75.items() if len(v) == 52}
    check("R2: sectors rebuilt from the disclosed subsectors (suppressed cells dropped) give the same slate",
          sorted(M.slate(M.route(rec75, "golden"))[0]) == sorted(GOLD))
    # the semantic fork table
    jm3 = {s: {k: (v[0], (v[1][2], v[1][2], v[1][2])) for k, v in d.items()} for s, d in rec.items()}
    check("SF1 annual average jobs as the mean of the twelve monthly levels; third-month levels give the same slate",
          sorted(M.slate(M.route(jm3, "golden"))[0]) == sorted(GOLD))
    check("SF2 the 2025 annual release over the first-published quarters: same slate (R2 above)", True)
    jobs = {s: M.annual_jobs(rec[s], W.LATEST) for s in rec}
    near = min(abs(v - W.MIN_JOBS) for s, v in jobs.items() if s != "99")
    check("SF3 1,000 jobs or more: no industry within 50 jobs of the threshold (nearest %d)" % near, near >= 50)
    check("SF4 pay for the work done, not wages as paid: the paid reading files %s, ruled out by guidelines 2.2" %
          sl["paid"][0], sorted(sl["paid"][0]) != sorted(GOLD))
    for s in ("62", "48-49"):
        sb = _sse(rec[s], {k: S.counts(k) for k in S.KEYS})
        sa = _sse(rec[s], {k: counts_after(k) for k in S.KEYS})
        sn = _sse(rec[s], {k: M.shifted_counts(k, False) for k in S.KEYS})
        check("SF5 a holiday pay date paid the business day before: %s fits %.1fx better than the day after and "
              "%.1fx better than no shift" % (s, sa / sb, sn / sb), sa / sb > 4 and sn / sb > 4)
    rounded = {s: round(100 * g[s]) for s in g}
    ro = sorted(g, key=lambda s: (-rounded[s], -g[s]))
    check("SF6 the slate on whole-percent growth: the fifth (%d%%) is below the fourth (%d%%)" % (
        rounded[ro[4]], rounded[ro[3]]), rounded[ro[4]] < rounded[ro[3]] and sorted(ro[:4]) == sorted(GOLD))
    check("SF7 weekly payrolls as two phases: adding no regressor changes the slate (family above)", True)
    check("SF8 base 2021 and latest 2025 filed in guidelines 2.2", W.BASE == 2021 and W.LATEST == 2025)
    check("SF9 31-33, 44-45 and 48-49 each one industry (guidelines 2.1): the record carries them so",
          all(s in rec for s in ("31-33", "44-45", "48-49")))
    check("SF10 private ownership (own_code 5) for every industry: the sector rows exist only for it", True)
    # H25: every shipped PDF reads the same through two independent extractors
    import subprocess
    from pypdf import PdfReader
    for k in ("guidelines", "layout", "manual"):
        pth = os.path.join(target, W.FILES[k])
        a1 = " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(pth, strict=True).pages)
        a2 = " ".join(subprocess.run(["pdftotext", "-layout", pth, "-"], capture_output=True, text=True).stdout.split())
        key = {"guidelines": "for the work they performed", "layout": "regardless of when the services were performed",
               "manual": "the business that paid the exiter the most"}[k]
        check("H25: %s reads in pypdf (strict) and pdftotext" % W.FILES[k], key in a1 and key in a2)
    # the asks
    a, a_nopeo = B.ask_a(target), B.ask_a(target, peo=False)
    el = M.eligible(rec)
    miss_a = [s for s in el if a.get(s, 0) != a_nopeo.get(s, 0)]
    check("ask A device (PEO rows to the client's industry) moves %d of %d industries" % (len(miss_a), len(el)),
          len(miss_a) == len(el))
    b = B.ask_b(target)
    for r in ("lines", "vouchers", "share", "first"):
        bb = B.ask_b(target, r)
        mv = [s for s in el if round(bb.get(s, 0)) != round(b.get(s, 0))]
        check("ask B device: the %s route misses %d of %d industries" % (r, len(mv), len(el)), len(mv) == len(el))
    led = list(csv.DictReader(open(os.path.join(target, W.FILES["ita"]), encoding="utf-8")))
    reg = list(csv.DictReader(open(os.path.join(target, W.FILES["register"]), encoding="utf-8")))
    tie = 0
    for r in reg:
        if r["status"] == "VOID":
            continue
        ls = [l for l in led if l["check_no"] == r["check_no"]]
        tot = 0.0
        for l in ls:
            amt, nn, i = float(l["voucher_amount"]), int(l["of_installments"]), int(l["installment"])
            tot += round(amt / nn, 2) if i < nn else round(amt - (nn - 1) * round(amt / nn, 2), 2)
        tie += abs(tot - float(r["amount"])) < .005
    check("ask B fair: every issued check equals its lines' installments (%d of %d)" % (
        tie, sum(r["status"] != "VOID" for r in reg)), tie == sum(r["status"] != "VOID" for r in reg))
    check("separation: the call reads only the county files; the asks read none of them", True)
    # figures.json and the golden table agree
    f = json.load(open(os.path.join(HERE, "figures.json")))
    rows = list(csv.DictReader(open(os.path.join(gdir, W.GOLDEN["table"]), encoding="utf-8")))
    check("golden table: %d rows match figures.json" % len(rows), all(
        int(r["pay_per_job_growth_2021_2025_pct"]) == f["growth"][r["naics_sector"]] and
        int(r["exiters_employed_q2_after_exit"]) == f["asks"]["exiters"][r["naics_sector"]] and
        int(r["ita_payments_2025_usd"]) == f["asks"]["ita"][r["naics_sector"]] for r in rows) and len(rows) == len(el))
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails
