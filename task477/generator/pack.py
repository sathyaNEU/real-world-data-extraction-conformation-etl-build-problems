"""The state's quarterly county file, cut from the clean truth: three releases (2013 to 2019, 2020 to the third
quarter of 2025 as first published, and the 2025 annual release that revises 2025's first three quarters), two
layouts, county totals, ownerships, sectors and three-digit industries, suppressed cells, the 2022 NAICS recode of
retail."""
import csv
import hashlib
import datetime as dt
import functools
import io

import numpy as np

import records as R
import sources as S
import world as W

OLD = ["area_fips", "own_code", "industry_code", "agglvl_code", "size_code", "year", "qtr", "disclosure_code",
       "qtrly_estabs_count", "month1_emplvl", "month2_emplvl", "month3_emplvl", "total_qtrly_wages",
       "taxable_qtrly_wages", "qtrly_contributions", "avg_wkly_wage"]
NEW = ["area_fips", "own_code", "industry_code", "agglvl_code", "size_code", "year", "qtr", "disclosure_code",
       "qtrly_estabs", "month1_emplvl", "month2_emplvl", "month3_emplvl", "total_qtrly_wages", "taxable_qtrly_wages",
       "qtrly_contributions", "avg_wkly_wage", "oty_month1_emplvl_chg", "oty_total_qtrly_wages_chg"]
TAXBASE = 15000            # taxable wage base per worker a year
RATE = {"23": .041, "56": .033, "72": .027, "71": .029, "44-45": .024}


@functools.lru_cache(None)
def everything():
    rng = np.random.default_rng(W.SEED)
    counties = {W.COUNTY_FIPS: S.tallis(rng)}
    for name, fips, scale in W.COUNTIES:
        counties[fips] = S.series(rng, fips, scale, S.other_profile(rng))
    gov = {}
    for fips in counties:
        sc = 1.0 if fips == W.COUNTY_FIPS else dict((f, s) for _, f, s in W.COUNTIES)[fips]
        gov[fips] = S.series(rng, fips, sc, {
            "1": ("Federal", 820, 1490, .16, .002, [("1", 1.0, 1.0, {"FA": .5, "FB": .5})]),
            "2": ("State", 2900, 1180, .15, .004, [("2", 1.0, 1.0, {"FB": 1.0})]),
            "3": ("Local", 9400, 1050, .155, .006, [("3", 1.0, 1.0, {"SM": .55, "FA": .45})])})
    prelim = {}
    for fips, inds in counties.items():
        for code in list(inds) + sorted({v["sector"] for v in inds.values()}) + ["10"]:
            for q in (1, 2, 3):
                prelim[(fips, code, q)] = (float(np.exp(rng.normal(0, .004))), int(rng.integers(-3, 4)))
    asks = R.build(np.random.default_rng(W.SEED + 1000))
    return dict(counties=counties, gov=gov, prelim=prelim, asks=asks)


def suppressed(code, v, k):
    """The program's disclosure screen: fewer than three establishments, or one dominating the cell."""
    if v["estabs"][k] < 3:
        return True
    return code in ("622", "212", "221", "551", "336") and v["estabs"][k] < 6


def _vintage(code, y):
    if y >= 2022 and code in W.NAICS2022:
        return W.NAICS2022[code]
    return [(code, 1.0)]


def cells(x):
    """Every published cell: (fips, own, industry, agglvl, y, q) -> dict(estabs, m1, m2, m3, wages, taxable, contrib,
    disclosed). Sector and total cells are sums of the three-digit cells, so they are published whether or not a child
    is suppressed."""
    out = {}
    for fips, inds in x["counties"].items():
        for (y, q) in S.QUARTERS:
            k = (y, q)
            tot = None
            secs = {}
            for code, v in inds.items():
                jm = [v["jobs"][(y, m)] for m in range(3 * q - 2, 3 * q + 1)]
                w = int(round(v["paid"][k]))
                per = w / max(1, sum(jm) / 3)
                cum = per * (q - .5)
                tax = int(round(min(w, max(0.0, TAXBASE - (cum - per / 2)) * sum(jm) / 3))) if cum - per < TAXBASE else 0
                tax = max(0, min(w, tax))
                con = int(round(tax * RATE.get(v["sector"], .021)))
                c = dict(estabs=v["estabs"][k], m=jm, wages=w, taxable=tax, contrib=con)
                for vcode, sh in _vintage(code, y):
                    cc = dict(estabs=max(1, int(round(c["estabs"] * sh))) if sh < 1 else c["estabs"],
                              m=[int(round(a * sh)) for a in jm], wages=int(round(w * sh)),
                              taxable=int(round(tax * sh)), contrib=int(round(con * sh)))
                    if sh < 1:
                        cc["wages"] = int(round(w * sh))
                    out[(fips, "5", vcode, "75", y, q)] = dict(cc, disclosed=not suppressed(code, v, k))
                s = secs.setdefault(v["sector"], dict(estabs=0, m=[0, 0, 0], wages=0, taxable=0, contrib=0))
                for f in ("estabs", "wages", "taxable", "contrib"):
                    s[f] += c[f]
                s["m"] = [a + b for a, b in zip(s["m"], jm)]
            priv = dict(estabs=0, m=[0, 0, 0], wages=0, taxable=0, contrib=0)
            for sec, s in secs.items():
                small = s["estabs"] < 3 or (sec in ("21", "22", "99") and s["estabs"] < 5)
                out[(fips, "5", sec, "74", y, q)] = dict(s, disclosed=not small)
                for f in ("estabs", "wages", "taxable", "contrib"):
                    priv[f] += s[f]
                priv["m"] = [a + b for a, b in zip(priv["m"], s["m"])]
            out[(fips, "5", "10", "71", y, q)] = dict(priv, disclosed=True)
            tot = dict(priv, m=list(priv["m"]))
            for own, v in sorted(x["gov"][fips].items()):
                jm = [v["jobs"][(y, m)] for m in range(3 * q - 2, 3 * q + 1)]
                w = int(round(v["paid"][k]))
                c = dict(estabs=v["estabs"][k], m=jm, wages=w, taxable=0, contrib=0, disclosed=True)
                out[(fips, own, "10", "71", y, q)] = c
                tot["estabs"] += c["estabs"]
                tot["wages"] += w
                tot["m"] = [a + b for a, b in zip(tot["m"], jm)]
            out[(fips, "0", "10", "70", y, q)] = dict(tot, disclosed=True)
    return out


def _row(key, c, layout, prev=None, scale=(1.0, 0)):
    fips, own, ind, agg, y, q = key
    f, dj = scale
    if not c["disclosed"]:
        vals = [0, 0, 0, 0, 0, 0, 0, 0]
        disc = "N"
    else:
        m = [max(0, a + (dj if a > 50 else 0)) for a in c["m"]]
        w = int(round(c["wages"] * f))
        avg = sum(m) / 3
        vals = [c["estabs"], m[0], m[1], m[2], w, int(round(c["taxable"] * f)), int(round(c["contrib"] * f)),
                int(round(w / avg / 13)) if avg else 0]
        disc = ""
    r = [fips, own, ind, agg, "0", y, q, disc] + vals
    if layout == "new":
        if prev is not None and c["disclosed"] and prev["disclosed"]:
            r += [vals[1] - prev["m"][0], vals[4] - prev["wages"]]
        else:
            r += [0, 0]
    return r


def qcew_rows(x, which):
    cl = cells(x)
    keys = sorted(cl, key=lambda k: (k[4], k[5], k[0], k[1], k[3], k[2]))
    out = []
    for key in keys:
        fips, own, ind, agg, y, q = key
        if which == "a" and not (W.Y0 <= y <= 2019):
            continue
        if which == "b" and not (2020 <= y <= 2025 and (y, q) != (2025, 4)):
            continue
        if which == "c" and y != 2025:
            continue
        c = cl[key]
        scale = (1.0, 0)
        if which == "b" and y == 2025:
            scale = x["prelim"].get((fips, ind, q))
            if scale is None:
                h = int(hashlib.sha256(("%s%s%s%d" % (fips, own, ind, q)).encode()).hexdigest()[:8], 16)
                scale = (1 + ((h % 1000) - 500) / 1.0e5, (h // 1000) % 7 - 3)
        prev = cl.get((fips, own, ind, agg, y - 1, q))
        out.append(_row(key, c, "old" if which == "a" else "new", prev, scale))
    return out


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)


# the board's and the state's records behind the asks
EXIT_COLS = ["enrollment_id", "participant_id", "program", "exit_date", "exit_reason", "birth_date", "home_zip"]
WAGE_COLS = ["participant_id", "ui_acct", "rptg_unit", "wage_yr", "wage_qtr", "wages"]
EMP_COLS = ["ui_acct", "legal_name", "naics", "county_fips", "status", "liability_date"]
PEO_COLS = ["peo_acct", "peo_name", "client_seq", "client_legal_name", "client_fein", "client_ui_acct",
            "agreement_start", "agreement_end"]
LEDGER_COLS = ["voucher_no", "participant_id", "program_id", "description", "installment", "of_installments",
               "voucher_amount", "due_date", "check_no"]
REG_COLS = ["check_no", "payee", "issue_date", "amount", "status", "void_date"]


def _d(d, fmt="%Y-%m-%d"):
    return d.strftime(fmt) if d else ""


def exit_rows(x):
    a = x["asks"]
    out = []
    for i, e in enumerate(sorted(a["exits"], key=lambda e: (e["exit_date"], e["enroll"]))):
        reason = "" if i % 23 else "Entered employment"
        out.append([e["enroll"], e["pid"], e["program"], _d(e["exit_date"], "%m/%d/%Y"), reason,
                    _d(e["dob"], "%m/%d/%Y"), e["zip"]])
    return out


def wage_rows(x):
    a = x["asks"]
    rows = sorted(a["wage_rows"], key=lambda r: (r["y"], r["q"], r["pid"], r["acct"]))
    return [[r["pid"], r["acct"], r["unit"], r["y"], r["q"], "%.2f" % r["wages"]] for r in rows]


def employer_rows(x):
    a = x["asks"]
    out = []
    for e in sorted(a["emps"], key=lambda e: e["acct"]):
        liab = "%d-%02d-01" % (2004 + int(e["acct"]) % 20, 1 + int(e["acct"]) % 12)
        out.append([e["acct"], e["name"].upper(), e["naics"], e["county"], "ACTIVE", liab])
    return out


def peo_rows(x):
    out = []
    regs = sorted(x["asks"]["peo_regs"], key=lambda r: (r["peo_account"], r["rpt_unit"], r["effective"]))
    for r in regs:
        out.append([r["peo_account"], r["peo_name"], r["rpt_unit"], r["client_name"], r["client_fein"],
                    r["client_account"], _d(r["effective"]), _d(r["ended"])])
    return out


def ledger_rows(x):
    a = x["asks"]
    return [[l["vid"], l["pid"], l["prog"], l["desc"], l["inst"], l["n"], "%.2f" % l["amount"], _d(l["due"]),
             l["check"] or ""]
            for l in sorted(a["ledger"], key=lambda l: (l["vid"], l["inst"]))]


def register_rows(x):
    a = x["asks"]
    return [[r["check"], r["payee"], _d(r["issue"]), "%.2f" % r["amount"], r["status"], _d(r["void"])]
            for r in sorted(a["register"], key=lambda r: int(r["check"])) if r["issue"] >= dt.date(2025, 1, 1)]
