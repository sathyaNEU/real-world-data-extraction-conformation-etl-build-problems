"""Independent verifier: reads only target/ and golden/, plain csv (no pandas, no generator state),
executes OM-4 as written, recomputes every graded figure and the back-test that selects the estimation
basis, and compares with the golden deliverables."""
import csv
import datetime as dt
import os
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

import openpyxl

P2, P3, P4 = dt.date(2022, 6, 30), dt.date(2022, 9, 30), dt.date(2022, 12, 31)
EXTRACT, SWITCH = dt.date(2023, 2, 3), dt.date(2023, 1, 3)
DAY = (EXTRACT - P4).days
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


def r1(x):
    return str(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def run(target, golden):
    wb = openpyxl.load_workbook(os.path.join(target, "client_watchlist_crowding_2022Q4.xlsx"), read_only=True)
    rows = list(wb["Watchlist"].iter_rows(values_only=True))
    hdr = rows[4]
    wl = [dict(zip(hdr, r)) for r in rows[5:] if r[0] is not None]
    cus = [w["CUSIP"] for w in wl]
    stems = defaultdict(list)
    for w in wl:
        stems[w["Issuer"].upper().replace(".", "").split()[0]].append(w["CUSIP"])
    with open(os.path.join(target, "manager_register.csv"), encoding="utf-8") as fh:
        mtype = {int(r["cik"]): r["manager_type"] for r in csv.DictReader(fh)}
    fil, lines = {}, defaultdict(list)
    for dr in DROPS:
        cov = {r["ACCESSION_NUMBER"]: r for r in tsv(os.path.join(target, dr, "COVERPAGE.tsv"))}
        for r in tsv(os.path.join(target, dr, "SUBMISSION.tsv")):
            c = cov[r["ACCESSION_NUMBER"]]
            fil[r["ACCESSION_NUMBER"]] = dict(cik=int(r["CIK"]), date=d(r["FILING_DATE"]), per=d(c["REPORTCALENDARORQUARTER"]),
                                              hper=d(r["PERIODOFREPORT"]), drop=dr,
                                              amend=c["ISAMENDMENT"], atype=c["AMENDMENTTYPE"], rtype=c["REPORTTYPE"],
                                              no=int(c["AMENDMENTNO"] or 0),
                                              name=c["FILINGMANAGER_NAME"], note=c["ADDITIONALINFORMATION"])
        for r in tsv(os.path.join(target, dr, "INFOTABLE.tsv")):
            lines[r["ACCESSION_NUMBER"]].append(r)

    def norm(r):
        c = r["CUSIP"].strip().upper().zfill(9)
        if len(c) == 9 and chk(c[:8]) == c[8]:
            return c
        h = stems.get(r["NAMEOFISSUER"].upper().replace(".", "").split()[0], [])
        return h[0] if (len(h) == 1 and r["TITLEOFCLASS"] == "COM") else None

    def option(r):
        return bool(r["PUTCALL"]) or r["TITLEOFCLASS"] in ("CALL", "PUT")

    def report(per, cut=None, key="per", order="number", drops=None):
        """each manager's report as amended: by filing date, amendments filed on one day by amendment number
        (order 'file': by accession, the data set's order); a new holdings amendment adds, anything else replaces"""
        by = defaultdict(list)
        for a, f in fil.items():
            if f[key] == per and f["rtype"] != "13F NOTICE" and (cut is None or f["date"] <= cut) \
                    and (drops is None or f["drop"] in drops):
                by[f["cik"]].append((f["date"], f["no"] if order == "number" else 0, a, f))
        out = {}
        for cik, xs in by.items():
            cur = []
            if order == "latest":
                out[cik] = [max(xs, key=lambda x: (x[0], x[2]))[2]]
                continue
            for _, _, a, f in sorted(xs, key=lambda x: (x[0], x[1], x[2])):
                cur = cur + [a] if (f["amend"] == "Y" and f["atype"] == "NEW HOLDINGS") else [a]
            out[cik] = cur
        return out

    def shares(rep):
        s = defaultdict(int)
        for cik, accs in rep.items():
            for a in accs:
                for r in lines[a]:
                    if r["SSHPRNAMTTYPE"] == "SH" and not option(r):
                        c = norm(r)
                        if c in cus:
                            s[(cik, c)] += int(r["SSHPRNAMT"])
        return s

    sub = {r["adsh"]: r for r in tsv(os.path.join(target, "fsds_cover_extract", "sub.txt"))}
    cnt = defaultdict(list)
    for r in tsv(os.path.join(target, "fsds_cover_extract", "num.txt")):
        if r["tag"] == "EntityCommonStockSharesOutstanding":
            cnt[int(sub[r["adsh"]]["cik"])].append((dt.datetime.strptime(r["ddate"], "%Y%m%d").date(), int(float(r["value"]))))

    def so(icik, per):
        return max(x for x in cnt[icik] if x[0] <= per)[1]

    ic = {w["CUSIP"]: w["Issuer CIK"] for w in wl}
    SP = "Index and ETF sponsor"

    def estimate(qn_per, qp_per, cut):
        """every manager still due completed four ways: the golden (each index or ETF sponsor by the change the
        filed sponsors show in that name, every other type by its own change pooled over the twelve), its stake
        formulation (the sponsor's stake at the last period end grown by the filed sponsors' stake change over
        the twelve and read against this period's count, every other type flat), each type's change pooled over
        the twelve (the type-pooled rival) and flat carry"""
        rep_n, rep_p = report(qn_per, cut), report(qp_per)
        filed_any = {f["cik"] for f in fil.values() if f["per"] == qn_per and f["date"] <= cut}
        due = set(rep_p) - filed_any
        both = set(rep_n) & set(rep_p)
        sn, sp = shares(rep_n), shares(rep_p)
        Sn = {c: so(ic[c], qn_per) for c in cus}
        Sp = {c: so(ic[c], qp_per) for c in cus}
        num, den = defaultdict(int), defaultdict(int)
        numc, denc = defaultdict(int), defaultdict(int)
        for (k, c), v in sn.items():
            if k in both:
                num[mtype[k]] += v
                numc[(mtype[k], c)] += v
        for (k, c), v in sp.items():
            if k in both:
                den[mtype[k]] += v
                denc[(mtype[k], c)] += v
        rate = {t: num[t] / den[t] for t in den}
        stake = sum(numc[(SP, c)] / Sn[c] for c in cus) / sum(denc[(SP, c)] / Sp[c] for c in cus)
        est, stk, typ, flat = (defaultdict(float) for _ in range(4))
        for (k, c), v in sn.items():
            for x in (est, stk, typ, flat):
                x[c] += v
        for (k, c), v in sp.items():
            if k in due:
                t = mtype[k]
                est[c] += v * (numc[(SP, c)] / denc[(SP, c)] if t == SP else rate.get(t, 1.0))
                stk[c] += v / Sp[c] * stake * Sn[c] if t == SP else v
                typ[c] += v * rate.get(t, 1.0)
                flat[c] += v
        return dict(golden=est, stake=stk, type_pooled=typ, flat=flat), due, rate

    rep3 = report(P3)
    s3 = shares(rep3)
    sep = defaultdict(int)
    for (k, c), v in s3.items():
        sep[c] += v
    # the criterion: the September window at the same day, completing from June
    cut3 = P3 + dt.timedelta(days=DAY)
    E3, _, _ = estimate(P3, P2, cut3)
    miss = {k: max(abs(100 * (x[c] - sep[c]) / so(ic[c], P3)) for c in cus) for k, x in E3.items()}
    assert min(miss, key=miss.get) in ("golden", "stake") and miss["golden"] < 0.15, miss
    assert min(miss["type_pooled"], miss["flat"]) - max(miss["golden"], miss["stake"]) >= 0.4, miss
    E4, due, rate = estimate(P4, P3, EXTRACT)
    est = E4["golden"]
    out = {}
    for w in wl:
        c = w["CUSIP"]
        S3, S4 = so(ic[c], P3), so(ic[c], P4)
        out[c] = dict(S3=S3, S4=S4, sep=100 * sep[c] / S3, dec=100 * est[c] / S4, flag=100 * est[c] / S4 > 80.0,
                      dec_stake=100 * E4["stake"][c] / S4, dec_type=100 * E4["type_pooled"][c] / S4)
        assert abs(out[c]["dec_stake"] - out[c]["dec"]) < 0.01 and r1(out[c]["dec_stake"]) == r1(out[c]["dec"]), (c, out[c])
    assert sorted(w["Ticker"] for w in wl if out[w["CUSIP"]]["dec_type"] > 80) != sorted(w["Ticker"] for w in wl if out[w["CUSIP"]]["flag"])

    def bridge(key="per", order="number", drops=None):
        rep = report(P3, key=key, order=order, drops=drops)
        q3acc = {a for a, f in fil.items() if f[key] == P3 and (drops is None or f["drop"] in drops)}
        eff = {a for accs in rep.values() for a in accs}
        raw = opt = sup = rep_ = 0
        for a in q3acc:
            for r in lines[a]:
                n = int(r["SSHPRNAMT"])
                if r["CUSIP"] in cus:
                    raw += n
                    if option(r):
                        opt += n
                    elif a not in eff:
                        sup += n
                elif not option(r) and a in eff and norm(r) in cus:
                    rep_ += n
        return dict(raw=raw, options=opt, superseded=sup, cusip_repaired=rep_, conformed=raw - opt - sup + rep_)

    br = bridge()
    assert abs(sum(sep.values()) - br["conformed"]) == 0, "bridge does not tie to September"
    stops_a, stops_b = {}, {}
    for k, (key, order) in {"S1": ("hper", "file"), "S2": ("per", "file"), "S3": ("hper", "number"),
                            "S4": ("per", "latest"), "S5": ("per", "number")}.items():
        sh = defaultdict(int)
        for (cik, c), v in shares(report(P3, key=key, order=order)).items():
            sh[c] += v
        stops_a[k] = {c: 100 * sh[c] / so(ic[c], P3) for c in cus}
    for k, args in {"S1": ("hper", "file", None), "S2": ("per", "file", None), "S3": ("hper", "number", None),
                    "S4": ("per", "number", ["form13f_2022q4"]), "S5": ("per", "number", None)}.items():
        stops_b[k] = bridge(*args)

    with open(os.path.join(golden, "crowded_flags_2022q4.csv"), encoding="utf-8") as fh:
        gold = {r["cusip"]: r for r in csv.DictReader(fh)}
    bad = []
    for c, o in out.items():
        g = gold[c]
        pairs = [("inst_own_pct", r1(o["dec"])), ("crowded", "Y" if o["flag"] else "N"), ("prior_inst_own_pct", r1(o["sep"]))]
        for k, v in pairs:
            if g[k] != v:
                bad.append((c, k, g[k], v))
    if bad:
        raise AssertionError(f"verifier disagrees with golden: {bad[:6]}")
    return out, br, dict(due=len(due), miss=miss, stops_a=stops_a, stops_b=stops_b)


if __name__ == "__main__":
    t = sys.argv[1]
    o, br, x = run(os.path.join(t, "target"), os.path.join(t, "golden"))
    print("verifier ok", len(o), br, x)
