"""Independent verifier: reads only target/ and golden/, plain csv (no pandas, no generator state),
recomputes every graded figure and compares it with the golden deliverables."""
import csv
import datetime as dt
import os
import sys
from collections import defaultdict

import openpyxl

P3, P4 = dt.date(2022, 9, 30), dt.date(2022, 12, 31)
EXTRACT, SWITCH = dt.date(2023, 2, 3), dt.date(2023, 1, 3)
DROPS = ["form13f_2022q3", "form13f_2022q4", "edgar13f_daily_20230103_20230203"]


def d(s):
    return dt.datetime.strptime(s, "%d-%b-%Y").date()


def chk(base):
    t = 0
    for i, ch in enumerate(base):
        v = int(ch) if ch.isdigit() else ord(ch) - 55
        v = v * 2 if i % 2 else v
        t += v // 10 + v % 10
    return str((10 - t % 10) % 10)


def tsv(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def run(target, golden):
    wb = openpyxl.load_workbook(os.path.join(target, "client_watchlist_crowding_2022Q4.xlsx"), read_only=True)
    rows = list(wb["Watchlist"].iter_rows(values_only=True))
    hdr = rows[4]
    wl = [dict(zip(hdr, r)) for r in rows[5:] if r[0] is not None]
    cus = [w["CUSIP"] for w in wl]
    byname = {w["Issuer"].upper().replace(".", ""): w["CUSIP"] for w in wl}
    fil, lines = {}, defaultdict(list)
    for dr in DROPS:
        cov = {r["ACCESSION_NUMBER"]: r for r in tsv(os.path.join(target, dr, "COVERPAGE.tsv"))}
        for r in tsv(os.path.join(target, dr, "SUBMISSION.tsv")):
            c = cov[r["ACCESSION_NUMBER"]]
            fil[r["ACCESSION_NUMBER"]] = dict(cik=int(r["CIK"]), date=d(r["FILING_DATE"]), per=d(c["REPORTCALENDARORQUARTER"]),
                                              amend=c["ISAMENDMENT"], atype=c["AMENDMENTTYPE"], rtype=c["REPORTTYPE"],
                                              name=c["FILINGMANAGER_NAME"])
        for r in tsv(os.path.join(target, dr, "INFOTABLE.tsv")):
            lines[r["ACCESSION_NUMBER"]].append(r)

    def norm(r):
        c = r["CUSIP"].strip().upper().zfill(9)
        if len(c) == 9 and chk(c[:8]) == c[8]:
            return c
        n = r["NAMEOFISSUER"].upper().replace(".", "")
        return byname.get(n) if r["TITLEOFCLASS"] == "COM" else None

    def report(per, cut=None):
        by = defaultdict(list)
        for a, f in fil.items():
            if f["per"] == per and f["rtype"] != "13F NOTICE" and (cut is None or f["date"] <= cut):
                by[f["cik"]].append((f["date"], a, f))
        out = {}
        for cik, xs in by.items():
            cur = []
            for _, a, f in sorted(xs, key=lambda x: (x[0], x[1])):
                cur = cur + [a] if (f["amend"] == "Y" and f["atype"] == "NEW HOLDINGS") else [a]
            out[cik] = cur
        return out

    def shares(rep):
        s = defaultdict(int)
        for cik, accs in rep.items():
            for a in accs:
                for r in lines[a]:
                    if r["SSHPRNAMTTYPE"] == "SH" and not r["PUTCALL"]:
                        c = norm(r)
                        if c in cus:
                            s[(cik, c)] += int(r["SSHPRNAMT"])
        return s

    # share counts
    sub = {r["adsh"]: r for r in tsv(os.path.join(target, "fsds_cover_extract", "sub.txt"))}
    cnt = defaultdict(list)
    for r in tsv(os.path.join(target, "fsds_cover_extract", "num.txt")):
        if r["tag"] == "EntityCommonStockSharesOutstanding":
            cnt[int(sub[r["adsh"]]["cik"])].append((dt.datetime.strptime(r["ddate"], "%Y%m%d").date(), int(float(r["value"]))))

    def so(icik, per):
        return max(x for x in cnt[icik] if x[0] <= per)[1]

    rep3, rep4 = report(P3), report(P4, EXTRACT)
    s3, s4 = shares(rep3), shares(rep4)
    pend = set(rep3) - {f["cik"] for f in fil.values() if f["per"] == P4 and f["date"] <= EXTRACT}
    out = {}
    for w in wl:
        c = w["CUSIP"]
        S3, S4 = so(w["Issuer CIK"], P3), so(w["Issuer CIK"], P4)
        sep = sum(v for (k, cc), v in s3.items() if cc == c)
        dec = sum(v for (k, cc), v in s4.items() if cc == c) + sum(v for (k, cc), v in s3.items() if cc == c and k in pend)
        # dollar values, December
        val = defaultdict(int)
        pxs = defaultdict(list)
        for cik, accs in rep4.items():
            for a in accs:
                for r in lines[a]:
                    if r["SSHPRNAMTTYPE"] == "SH" and not r["PUTCALL"] and norm(r) == c and int(r["SSHPRNAMT"]) > 0:
                        pxs[a].append(int(r["VALUE"]) / int(r["SSHPRNAMT"]))
        allp = sorted(p for v in pxs.values() for p in v)
        med = allp[len(allp) // 2]
        for cik, accs in rep4.items():
            for a in accs:
                mult = 1000 if fil[a]["date"] < SWITCH else 1
                if pxs.get(a) and max(pxs[a]) < med / 300:
                    mult = 1000
                for r in lines[a]:
                    if r["SSHPRNAMTTYPE"] == "SH" and not r["PUTCALL"] and norm(r) == c:
                        val[cik] += int(r["VALUE"]) * mult
        top = max(val.items(), key=lambda kv: (kv[1], -kv[0]))
        out[c] = dict(S3=S3, S4=S4, sep=100 * sep / S3, dec=100 * dec / S4, flag=100 * dec / S4 > 80.0,
                      top_cik=top[0], top_usd=top[1])
    # bridge
    q3acc = {a for a, f in fil.items() if f["per"] == P3}
    eff = {a for accs in rep3.values() for a in accs}
    raw = opt = sup = rep_ = 0
    for a in q3acc:
        for r in lines[a]:
            n = int(r["SSHPRNAMT"])
            if r["CUSIP"] in cus:
                raw += n
                if r["PUTCALL"]:
                    opt += n
                elif a not in eff:
                    sup += n
            elif not r["PUTCALL"] and a in eff and norm(r) in cus:
                rep_ += n
    br = dict(raw=raw, options=opt, superseded=sup, cusip_repaired=rep_, conformed=raw - opt - sup + rep_)

    # compare with golden
    with open(os.path.join(golden, "crowded_flags_2022q4.csv"), encoding="utf-8") as fh:
        gold = {r["cusip"]: r for r in csv.DictReader(fh)}
    bad = []
    from decimal import Decimal, ROUND_HALF_UP

    def r1(x):
        return str(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    for c, o in out.items():
        g = gold[c]
        pairs = [("shares_outstanding", str(o["S4"])), ("inst_own_pct", r1(o["dec"])), ("crowded", "Y" if o["flag"] else "N"),
                 ("prior_shares_outstanding", str(o["S3"])), ("prior_inst_own_pct", r1(o["sep"])),
                 ("top_holder_cik", str(o["top_cik"])), ("top_holder_value_usd", str(o["top_usd"]))]
        for k, v in pairs:
            if g[k] != v:
                bad.append((c, k, g[k], v))
    assert sum(o["sep"] * o["S3"] / 100 for o in out.values()) - br["conformed"] < 1, "bridge does not tie to September"
    if bad:
        raise AssertionError(f"verifier disagrees with golden: {bad[:6]}")
    return out, br


if __name__ == "__main__":
    t = sys.argv[1]
    o, br = run(os.path.join(t, "target"), os.path.join(t, "golden"))
    print("verifier ok", len(o), br)
