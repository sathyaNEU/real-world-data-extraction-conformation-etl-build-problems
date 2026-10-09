#!/usr/bin/env python3
"""Independent verifier for task123. Reads only the shipped files in <task>/target (and the task's
metadata.json for the declared distractors). Shares no code with the generator: it parses the bytes,
rebuilds the screen under the standing method and under every rival, replays Ledgerwood's six packs,
and recomputes every graded September figure, every rival-killer and every ask stop.

    python3 verify.py <task folder> [--json out.json]
"""
import argparse
import csv
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from itertools import combinations

N_CHECKS = [0]
LOG = []


def check(cond, msg):
    N_CHECKS[0] += 1
    if not cond:
        raise SystemExit(f"VERIFY FAILED: {msg}")
    LOG.append(msg)


# ----------------------------------------------------------------------------- quarters

def q_add(q, k):
    y, m = q
    t = y * 12 + (m - 1) + 3 * k
    return (t // 12, t % 12 + 1)


def q_of(d):
    return (d.year, ((d.month - 1) // 3 + 1) * 3)


def q_last_day(q):
    y, m = q
    nxt = date(y + (m == 12), m % 12 + 1, 1)
    return nxt - timedelta(days=1)


def fy_pos(q, bal):
    return ((q[1] - bal - 1) % 12) // 3 + 1


def iso(s):
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def census_before(c):
    """Rule 2: census dates are 31 March each year and, from 2026, 30 September."""
    days = [date(y, 3, 31) for y in range(2015, c.year + 1)] + [date(y, 9, 30) for y in range(2026, c.year + 1)]
    return max(d for d in days if d < c)


def rule7_pay_day(y, m):
    """Rule 7: an instalment is paid on the 20th of the month before the month it is for, or on the
    Friday before when the 20th falls at a weekend."""
    py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
    d = date(py, pm, 20)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


# ----------------------------------------------------------------------------- reading the pack

def xlsx_sheets(path):
    """Minimal xlsx reader on the zip bytes: sheet name -> rows of cell values."""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        x = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            ss.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    wbx = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    rid2t = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    rid2t.update({a: b for b, a in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)})
    out = {}
    for name, rid in re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wbx):
        t = rid2t[rid].lstrip("/")
        t = t if t.startswith("xl/") else "xl/" + t
        x = z.read(t).decode("utf-8")
        rows = []
        for rx in re.findall(r"<row [^>]*>(.*?)</row>", x, re.S):
            cells = {}
            for attrs, body in re.findall(r"<c ([^>]*?)(?:/>|>(.*?)</c>)", rx, re.S):
                ref = re.search(r'r="([A-Z]+)\d+"', attrs).group(1)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                typ = re.search(r't="(\w+)"', attrs)
                typ = typ.group(1) if typ else "n"
                v = re.search(r"<v>(.*?)</v>", body or "")
                if typ == "s" and v:
                    val = ss[int(v.group(1))]
                elif typ == "inlineStr":
                    val = "".join(re.findall(r"<t[^>]*>(.*?)</t>", body, re.S))
                elif v:
                    val = float(v.group(1))
                    if val == int(val) and "." not in v.group(1):
                        val = int(val)
                else:
                    val = None
                cells[col] = val
            if cells:
                rows.append([cells.get(i) for i in range(1, max(cells) + 1)])
        out[name] = rows
    return out


def excel_date(v):
    return date(1899, 12, 30) + timedelta(days=int(v))


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


class Pack:
    def __init__(self, target):
        self.t = target
        f = lambda n: os.path.join(target, n)
        self.files = sorted(os.listdir(target))
        # grants register
        sh = xlsx_sheets(f("grants_register_20261007.xlsx"))
        g = sh["Grants"]
        hdr = g[0]
        self.grant = {}
        self.org_refs = defaultdict(list)
        self.name = {}
        self.bal = {}
        for r in g[1:]:
            d = dict(zip(hdr, r))
            bal = {"31 March": 3, "30 June": 6, "31 December": 12}[d["balance_date"]]
            rec = dict(prog=d["programme"], cc=d["charity_no"], start=excel_date(d["start_date"]),
                       end=excel_date(d["end_date"]), bal=bal, sector=d["sector"], district=d["district"],
                       amount=d["annual_amount"])
            self.grant[d["grant_ref"]] = rec
            self.org_refs[d["charity_no"]].append(d["grant_ref"])
            self.name[d["charity_no"]] = d["organisation"]
            self.bal[d["charity_no"]] = bal
        self.variations = [dict(zip(sh["Variations"][0], r)) for r in sh["Variations"][1:]]
        so = sh["Steady Ground offers"]
        self.sgf_offers = [dict(zip(so[0], r)) for r in so[1:]]
        self.op_ref = {cc: next(r for r in refs if self.grant[r]["prog"] == "Operating grant")
                       for cc, refs in self.org_refs.items()}
        self.pg_ref = {cc: next((r for r in refs if self.grant[r]["prog"] == "Project grant"), None)
                       for cc, refs in self.org_refs.items()}
        # portal
        self.versions = defaultdict(dict)   # (ref, q) -> no -> version
        with open(f("portal_return_lines_2018q3_2026q2.csv"), newline="") as fh:
            rd = csv.DictReader(fh)
            self.spine_cols = rd.fieldnames
            n = 0
            for row in rd:
                n += 1
                pe = iso(row["period_end"])
                key = (row["grant_ref"], (pe.year, pe.month))
                vno = int(row["version_no"])
                v = self.versions[key].get(vno)
                if v is None:
                    v = dict(no=vno, status=row["version_status"], sub=row["submitted_at"],
                             acc=row["accepted_at"], form=row["form"], ytd={}, py={},
                             year_end=row["year_end"], rid=row["return_id"])
                    self.versions[key][vno] = v
                (v["ytd"] if row["column"] == "YTD" else v["py"])[row["line_code"]] = int(row["amount"])
            self.spine_rows = n
        # register match
        self.reg = {}
        with open(f("charities_register_returns_extract_20261007.csv"), newline="") as fh:
            for row in csv.DictReader(fh):
                cc = row["charity_no"].strip().upper()
                ye = iso(row["year_end"])
                self.reg[(cc, (ye.year, ye.month))] = dict(
                    rec=row["date_received"], total=int(row["total_gross_income"]),
                    gov=int(row["govt_grants_contracts"]))
        # packs
        self.packs = {}
        for fn in self.files:
            m = re.match(r"SGF_screen_run_(\d{4})-03\.xlsx$", fn)
            if not m:
                continue
            y = int(m.group(1))
            sh = xlsx_sheets(f(fn))
            rows = {}
            scr = sh["Screen"]
            h = next(i for i, r in enumerate(scr) if r and r[0] == "Charity no.")
            for r in scr[h + 1:]:
                if not r or not r[0]:
                    continue
                rows[r[0]] = (int(r[2]), int(r[3]), int(r[4]), float(r[5]), int(r[6]) if len(r) > 6 and r[6] else 0)
            rd = {r[0]: r[1] for r in sh["Round"]}
            self.packs[y] = dict(rows=rows, pot=int(rd["Pot ($)"]),
                                 rate=int(round(float(rd["Rate (cents per dollar of fall)"]) * 100)),
                                 order=[r[0] for r in scr[h + 1:] if r and r[0]])
        # payment run
        self.pay = []
        with open(f("trust_payment_run_2018-07_to_2026-09.csv"), newline="") as fh:
            for row in csv.DictReader(fh):
                self.pay.append(dict(cc=row["charity_no"], ref=row["grant_ref"], value=iso(row["value_date"]),
                                     inst=row["instalment_for"], amount=int(row["amount"]),
                                     status=row["payment_status"], prog=row["programme"]))
        # documents: the rules' line, floor and cap; the budget minute's September pot
        rules = pdf_text(f("SGF_round_rules_rev2026-06.pdf"))
        self.rules = rules
        self.line = float(re.search(r"fall is (\d+) per cent or more", rules).group(1))
        self.floor = int(re.search(r"raised to \$([\d,]+)", rules).group(1).replace(",", ""))
        self.cap = int(re.search(r"held to \$([\d,]+)", rules).group(1).replace(",", ""))
        minute = pdf_text(f("trustees_budget_minute_2026-27_extract.pdf"))
        self.sept_pot = int(re.search(r"September 2026 round\s*\$([\d,]+)", minute).group(1).replace(",", ""))


# ----------------------------------------------------------------------------- the screen

def cutoff_str(c):
    return c.isoformat() + " 23:59"


EXTRACT = date(2026, 10, 7)


class Screen:
    def __init__(self, P):
        self.P = P
        self.by_org = defaultdict(list)   # (cc, q) -> accepted versions across refs
        self.by_ref = defaultdict(list)
        self.all_org = defaultdict(list)
        for (ref, q), vs in P.versions.items():
            cc = P.grant[ref]["cc"]
            for v in vs.values():
                v2 = dict(v, ref=ref)
                self.all_org[(cc, q)].append(v2)
                if v["status"] == "accepted":
                    self.by_org[(cc, q)].append(v2)
                    self.by_ref[(ref, q)].append(v2)
        for d in (self.by_org, self.by_ref):
            for lst in d.values():
                lst.sort(key=lambda v: v["acc"])

    def version(self, cc, q, cut, unit="org", ref=None, how="held"):
        if how == "delivered":
            c = [v for v in self.all_org.get((cc, q), []) if v["sub"] <= cut]
            return max(c, key=lambda v: (v["sub"], v["no"])) if c else None
        lst = self.by_org.get((cc, q), []) if unit == "org" else self.by_ref.get((ref, q), [])
        held = [v for v in lst if v["acc"] <= cut]
        return held[-1] if held else None

    @staticmethod
    def total(v):
        return v["ytd"].get("TOT_INC", v["ytd"].get("TOT_REV"))

    def received(self, cc, q4, by, strict=False):
        r = self.P.reg.get((cc, q4))
        if r is None:
            return False
        return r["rec"] < by.isoformat() if strict else r["rec"] <= by.isoformat()

    def row(self, cc, ref, c, o):
        P = self.P
        bal = P.bal[cc]
        cut = cutoff_str(EXTRACT if o.get("latest") else c)
        reg_by = EXTRACT if o.get("reg_extract") else c
        strict = o.get("strict", False)
        nat = q_add(q_of(c), -1)
        sb = o.get("stepback", "T")
        bals = o.get("bals")

        def admissible(q):
            if fy_pos(q, bal) != 4 or sb == "none" or (bals is not None and bal not in bals):
                return True
            got = self.received(cc, q, reg_by, strict)
            if sb == "T":
                return got
            if sb == "overdue":
                due = date(q[0], 9, 30) if bal == 3 else (date(q[0], 12, 31) if bal == 6 else date(q[0] + 1, 6, 30))
                return got or c <= due
            if sb == "dec":
                return not (bal == 12 and c.month == 3 and q == nat)
            if sb == "amended":
                vs = self.by_org.get((cc, q), [])
                return not any(v["acc"] > cutoff_str(c) and v["no"] > 1 for v in vs)
            raise ValueError(sb)

        e = nat
        steps = 0
        while not all(admissible(q_add(e, -k)) for k in range(4)):
            e = q_add(e, -1)
            steps += 1
            if steps > 8:
                return None
        rc = o.get("recency", "on")
        if rc != "off":
            before = date(c.year - 1, c.month, c.day) if rc == "year" else census_before(c)
            if q_last_day(e) < before or (rc == "strict" and q_last_day(e) == before):
                return None
        pe = nat if o.get("prior_natural") else e
        cur = [q_add(e, -k) for k in range(4)]
        pri = [q_add(pe, -k) for k in range(4, 8)]
        unit = o.get("unit", "org")

        def ytd(q):
            v = self.version(cc, q, cut, unit="org" if unit == "org" else "ref", ref=ref)
            return None if v is None else self.total(v)

        def disc(q):
            k = fy_pos(q, bal)
            y = ytd(q)
            if y is None:
                return None
            b = 0 if k == 1 else ytd(q_add(q, -1))
            if b is None:
                return None
            if k == 4 and o.get("q4", "register") == "register" and self.received(cc, q, reg_by, strict):
                return P.reg[(cc, q)]["total"] - b
            return y - b

        vals = [disc(q) for q in cur + pri]
        if any(v is None for v in vals):
            return None
        cs, ps = sum(vals[:4]), sum(vals[4:])
        return dict(cc=cc, ref=ref, cur=cs, prior=ps, fall=ps - cs, pct=100.0 * (ps - cs) / ps,
                    end=e, pend=pe)

    def run(self, c, pot, **o):
        P = self.P
        rows = []
        for cc, refs in P.org_refs.items():
            op = P.op_ref[cc]
            g = P.grant[op]
            if not (g["start"] <= c <= g["end"]):
                continue
            units = [op] if o.get("unit", "org") != "ref" else [r for r in refs if
                                                               P.grant[r]["start"] <= c <= P.grant[r]["end"]]
            for ref in units:
                r = self.row(cc, ref, c, o)
                if r is not None:
                    rows.append(r)
        elig = [r for r in rows if r["pct"] >= P.line]
        rate, offs = strike(P, [r["fall"] for r in elig], pot)
        for r in rows:
            r["offer"] = 0
        for r, x in zip(elig, offs):
            r["offer"] = x
        return dict(rows=rows, rate=rate, total=sum(offs), pot=pot)


def offer(P, rate_hc, fall):
    raw = (2 * rate_hc * fall + 10000) // 20000
    return min(max(raw, P.floor), P.cap)


def strike(P, falls, pot):
    lo, hi = 0, 10000
    tot = lambda r: sum(offer(P, r, f) for f in falls)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if tot(mid) <= pot:
            lo = mid
        else:
            hi = mid
    return lo, [offer(P, lo, f) for f in falls]


def pct1(x):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def pubrow(r):
    return (r["cur"], r["prior"], r["fall"], pct1(r["pct"]), r["offer"])


def replay(P, y, s):
    pk = P.packs[y]["rows"]
    mine = defaultdict(list)
    for r in s["rows"]:
        mine[r["cc"]].append(pubrow(r))
    back = sum(1 for cc, v in pk.items() if v in mine.get(cc, []))
    offers_ok = all(mine.get(cc) and any(x[4] == v[4] for x in mine[cc]) for cc, v in pk.items()) and \
        sum(1 for r in s["rows"] if r["offer"]) == sum(1 for v in pk.values() if v[4])
    return back, offers_ok, s["rate"] == P.packs[y]["rate"], len(s["rows"]) == len(pk)


# ----------------------------------------------------------------------------- the asks

class Asks:
    def __init__(self, S):
        self.S, self.P = S, S.P
        self.cache = {}

    def gov(self, cc, q, cut, mapping="correct", how="held", comps=False):
        if comps and q < (2024, 12) and q_add(q, 4) >= (2024, 12):
            nv = self.pick(cc, q_add(q, 4), cut, how)
            if nv is not None and "GOV_GRT" in nv["py"]:
                return nv["py"]["GOV_GRT"]
        v = self.pick(cc, q, cut, how)
        if v is None or "GOV_GRT" not in v["ytd"]:
            return None
        y = v["ytd"]
        if v["form"] == "QFR-24":
            return y["GOV_GRT"]
        if mapping == "correct":
            return y["GOV_GRT"] + y["FEE_SVC_GOV"]
        if mapping == "label":
            return y["GOV_GRT"]
        return y["GOV_GRT"] + y["FEE_SVC"]

    def pick(self, cc, q, cut, how):
        S, P = self.S, self.P
        if how == "pg" and P.pg_ref.get(cc):
            v = S.version(cc, q, cut, unit="ref", ref=P.pg_ref[cc])
            if v is not None:
                return v
        if how == "delivered":
            return S.version(cc, q, cut, how="delivered")
        return S.version(cc, q, cut)

    def k1(self, r, c, q4="register", **kw):
        P = self.P
        cc, bal = r["cc"], P.bal[r["cc"]]
        cut = cutoff_str(c)
        cur = [q_add(r["end"], -k) for k in range(4)]
        pri = [q_add(r["pend"], -k) for k in range(4, 8)]
        tot = {}
        for q in cur + pri:
            k = fy_pos(q, bal)
            g = self.gov(cc, q, cut, **kw)
            if k == 1:
                tot[q] = g
                continue
            b = self.gov(cc, q_add(q, -1), cut, **kw)
            if b is None:
                return None
            if k == 4 and q4 == "register":
                tot[q] = P.reg[(cc, q)]["gov"] - b
            else:
                tot[q] = None if g is None else g - b
        if any(v is None for v in tot.values()):
            return None
        return sum(tot[q] for q in pri) - sum(tot[q] for q in cur)

    def instalments(self):
        """Steady Ground instalments, rebuilt from the offers sheet and rule 7 (they are in no run)."""
        out = []
        for x in self.P.sgf_offers:
            y0, m0 = int(x["first_instalment_for"][:4]), int(x["first_instalment_for"][5:7])
            n, each, amt = int(x["instalments"]), int(x["instalment"]), int(x["offer_amount"])
            for k in range(n):
                t = y0 * 12 + m0 - 1 + k
                y, m = t // 12, t % 12 + 1
                out.append(dict(cc=x["charity_no"], ref=x["offer_ref"], value=rule7_pay_day(y, m),
                                inst=f"{y}-{m:02d}", amount=each if k < n - 1 else amt - (n - 1) * each,
                                status="paid", prog="Steady Ground Fund"))
        return out

    def run_series(self, how="value", statuses=("paid",), drop_pg=False, sgf=True):
        key = (how, statuses, drop_pg, sgf)
        if key in self.cache:
            return self.cache[key]
        out = defaultdict(int)
        P = self.P
        for p in self.P.pay + (self.instalments() if sgf else []):
            if p["status"] not in statuses:
                continue
            if drop_pg and p["ref"] == P.pg_ref.get(p["cc"]):
                continue
            if how == "value":
                q = q_of(p["value"])
            elif how == "for":
                y, m = int(p["inst"][:4]), int(p["inst"][5:7])
                q = q_of(date(y, m, 1))
            else:
                q = q_of(p["value"])
                if (q_last_day(q) - p["value"]).days <= 10:
                    continue
            out[(p["cc"], q)] += p["amount"]
        self.cache[key] = out
        return out

    def k2(self, r, c, **kw):
        cc = r["cc"]
        run = self.run_series(**kw)
        cur = [q_add(r["end"], -k) for k in range(4)]
        pri = [q_add(r["pend"], -k) for k in range(4, 8)]
        v = {q: run[(cc, q)] for q in cur + pri}
        return sum(v[q] for q in pri) - sum(v[q] for q in cur)


# ----------------------------------------------------------------------------- checks

def edge_gap(p):
    x = round(p * 10, 9)
    f = x - int(x) if x >= 0 else x - int(x) + 1
    return abs(f - 0.5) / 10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("--json")
    a = ap.parse_args()
    target = os.path.join(a.task, "target")
    meta = json.load(open(os.path.join(a.task, "metadata.json")))
    P = Pack(target)
    S = Screen(P)
    A = Asks(S)
    out = {}
    MARCH = [date(y, 3, 31) for y in range(2021, 2027)]
    SEPT = date(2026, 9, 30)

    # --- input gates
    files = P.files
    fmts = {os.path.splitext(f)[1] for f in files}
    check(len(files) >= 10 and len(fmts) >= 3, f"gates: {len(files)} files, {len(fmts)} formats")
    check(P.spine_rows >= 25000, f"gates: the portal export has {P.spine_rows} rows")
    dis = meta["distractor_files"]
    check(len(dis) >= 2 and all(d in files for d in dis), f"gates: distractors {dis} shipped and declared")
    for fn in files:
        check("distractor" not in fn.lower(), f"no file name says distractor ({fn})")
    for fn in files:
        if fn.endswith((".md", ".txt", ".csv")):
            check("distractor" not in open(os.path.join(target, fn), encoding="utf-8").read().lower(),
                  f"{fn} never says distractor")

    # --- the corpus under the standing method
    T = {}
    for c in MARCH:
        T[c.year] = S.run(c, P.packs[c.year]["pot"])
        back, offers_ok, rate_ok, count_ok = replay(P, c.year, T[c.year])
        check(back == len(P.packs[c.year]["rows"]) and offers_ok and rate_ok and count_ok,
              f"T gives back {back} of {len(P.packs[c.year]['rows'])} rows, every offer and the rate in {c.year}")
    total_rows = sum(len(P.packs[y]["rows"]) for y in P.packs)
    out["corpus"] = {y: dict(rows=len(P.packs[y]["rows"]), rate=P.packs[y]["rate"],
                             offers=sum(1 for v in P.packs[y]["rows"].values() if v[4])) for y in P.packs}

    # --- every rival on the corpus
    rivals = {
        "R1": dict(unit="ref", latest=True, q4="portal", stepback="none"),
        "R2": dict(latest=True, q4="portal", stepback="none"),
        "R3": dict(q4="portal", stepback="none"),
        "V1": dict(stepback="overdue"), "V2": dict(stepback="dec"), "V3": dict(stepback="amended"),
        "V4": dict(prior_natural=True), "V5": "drop", "T-strict": dict(strict=True),
        "T-extract": dict(reg_extract=True), "fallback": dict(stepback="none"),
    }
    misses = {}
    for name, o in rivals.items():
        m = dict(rows=0, offers=0, rates=0, counts=0, who=[])
        for c in MARCH:
            if o == "drop":
                s = S.run(c, P.packs[c.year]["pot"])
                s["rows"] = [r for r in s["rows"] if r["end"] == q_add(q_of(c), -1)]
                el = [r for r in s["rows"] if r["pct"] >= P.line]
                rate, offs = strike(P, [r["fall"] for r in el], P.packs[c.year]["pot"])
                for r in s["rows"]:
                    r["offer"] = 0
                for r, x in zip(el, offs):
                    r["offer"] = x
                s["rate"] = rate
            else:
                s = S.run(c, P.packs[c.year]["pot"], **o)
            back, ok_o, ok_r, ok_c = replay(P, c.year, s)
            mine = defaultdict(list)
            for r in s["rows"]:
                mine[r["cc"]].append(pubrow(r))
            m["who"] += [(cc, c.year) for cc, v in P.packs[c.year]["rows"].items() if v not in mine.get(cc, [])]
            m["rows"] += len(P.packs[c.year]["rows"]) - back
            m["offers"] += 0 if ok_o else 1
            m["rates"] += 0 if ok_r else 1
            m["counts"] += 0 if ok_c else 1
        misses[name] = m
    r0 = 0
    for c in MARCH:
        for cc, v in P.packs[c.year]["rows"].items():
            recs = sorted(q for (k, q), x in P.reg.items() if k == cc and x["rec"] <= c.isoformat())
            if len(recs) >= 2:
                cur, pri = P.reg[(cc, recs[-1])]["total"], P.reg[(cc, recs[-2])]["total"]
                if (cur, pri, pri - cur) == v[:3]:
                    continue
            r0 += 1
    residue = set(misses["R3"]["who"])
    check(misses["R3"]["rows"] == 10 and misses["R3"]["offers"] == 0 and misses["R3"]["rates"] == 0,
          f"R3 gives back {total_rows - 10} of {total_rows} rows, every offer and every rate")
    check(misses["R2"]["rows"] >= 40 and misses["R2"]["offers"] >= 4, f"R2 misses {misses['R2']['rows']} rows and {misses['R2']['offers']} rounds' offers")
    check(misses["R1"]["counts"] == 6, "R1's row count fails all six rounds")
    check(r0 >= 0.95 * total_rows, f"R0 misses {r0} of {total_rows} rows")
    exp = {"V1": 8, "V2": 12, "V4": 10, "V5": 10, "T-strict": 3, "T-extract": 10, "fallback": 10}
    for k, n in exp.items():
        check(misses[k]["rows"] == n, f"rival {k} misses {misses[k]['rows']} rows (expected {n})")
    check(misses["V3"]["rows"] >= 10, f"rival V3 misses {misses['V3']['rows']}")
    check(min(m["rows"] for m in misses.values()) >= 3, "no rival misses fewer than 3 rows")
    for k in ("fallback", "T-extract", "V4", "V5"):
        check(set(misses[k]["who"]) == residue, f"{k} misses exactly the R3 residue rows")
    check(set(misses["V1"]["who"]) < residue and set(misses["T-strict"]["who"]).isdisjoint(residue),
          "V1 misses a subset of the residue; T-strict misses the census-day receipts only")
    out["rivals"] = {k: dict(rows=v["rows"], offers=v["offers"], rates=v["rates"]) for k, v in misses.items()}
    out["rivals"]["R0"] = dict(rows=r0)
    # residue rows: small, not offered, far from the line
    for cc, y in sorted(residue):
        a_ = next(r for r in T[y]["rows"] if r["cc"] == cc)
        b_ = next(r for r in S.run(date(y, 3, 31), P.packs[y]["pot"], **rivals["R3"])["rows"] if r["cc"] == cc)
        check(abs(a_["cur"] - b_["cur"]) / a_["cur"] <= 0.012 and abs(a_["pct"] - b_["pct"]) <= 1.0
              and not a_["offer"] and abs(a_["pct"] - 10) >= 5 and abs(b_["pct"] - 10) >= 5,
              f"residue {P.name[cc]} {y} is small and far from the line")
    # the twin pair: identical register columns and today's figures, published falls about 2x apart
    c25 = date(2025, 3, 31)
    lat = {r["cc"]: r for r in S.run(c25, P.packs[2025]["pot"], latest=True)["rows"]}
    twins = []
    for x, y in combinations(sorted(lat), 2):
        gx, gy = P.grant[P.op_ref[x]], P.grant[P.op_ref[y]]
        if all(gx[k] == gy[k] for k in ("sector", "district", "start", "bal", "amount")) and \
                (lat[x]["cur"], lat[x]["prior"]) == (lat[y]["cur"], lat[y]["prior"]):
            twins.append((x, y))
    check(len(twins) == 1, f"one twin pair found: {[(P.name[a_], P.name[b_]) for a_, b_ in twins]}")
    tx, ty = twins[0]
    px, py = P.packs[2025]["rows"][tx][3], P.packs[2025]["rows"][ty][3]
    lo, hi = sorted([px, py])
    check(1.8 <= hi / lo <= 2.2, f"twins published at {lo} and {hi} per cent ({hi/lo:.2f}x), {lat[tx]['pct']:.2f} each today")

    # rule 4.1's recency clause is blind on the corpus: switched off, or read against the census a
    # year before, every March round gives back the same rows, offers and rate
    check(re.search(r"ending\s+on\s+or\s+after\s+the\s+census\s+before\s+it", P.rules) is not None and
          re.search(r"31 March each year and, from 2026, 30\s+September", P.rules) is not None,
          "rule 4.1 ties twelve-month income to the census before; rule 2 adds 30 September from 2026")
    for c in MARCH:
        for rc in ("off", "year"):
            s_ = S.run(c, P.packs[c.year]["pot"], recency=rc)
            back, ok_o, ok_r, ok_c = replay(P, c.year, s_)
            check(back == len(P.packs[c.year]["rows"]) and ok_o and ok_r and ok_c,
                  f"recency {rc}: {c.year} given back in full (the corpus cannot see rule 4.1's clause)")
    for c in MARCH:
        ends = [r["end"] for r in T[c.year]["rows"]]
        before = census_before(c)
        check(all(q_last_day(e) >= before for e in ends), f"{c.year}: no scored window ends before {before}")
    on_it = sorted((P.name[r["cc"]], c.year) for c in MARCH for r in T[c.year]["rows"]
                   if q_last_day(r["end"]) == census_before(c))
    check(len(on_it) == 2, f"windows ending on the census before: {on_it} (the inclusive reading is pinned)")

    # --- September: the call
    pot = P.sept_pot
    check(pot == 560000, f"the September pot from the budget minute: {pot}")
    TS = S.run(SEPT, pot)
    el = [r for r in TS["rows"] if r["pct"] >= P.line]
    nxt = sum(offer(P, TS["rate"] + 1, r["fall"]) for r in el)
    check(TS["total"] <= pot < nxt and pot - TS["total"] >= 25 and nxt - pot >= 25,
          f"rate {TS['rate']/100:.2f} cents: offers {TS['total']}, remainder {pot - TS['total']}, next step {nxt - pot} over")
    check(3600 <= TS["rate"] <= 4800, "rate inside 36.00 to 48.00 cents")
    check(len(TS["rows"]) == 132 and len(el) == 9, f"{len(TS['rows'])} scored, {len(el)} offered")
    check(all(q_last_day(r["end"]) >= date(2026, 3, 31) for r in TS["rows"]) and
          sum(1 for r in TS["rows"] if r["end"] == (2026, 3)) == 17,
          "every scored window ends on or after 31 March 2026; 17 end on it")
    check(not any(8.5 < r["pct"] < 11.5 for r in TS["rows"]), "no September fall within 1.5 points of the line")
    check(min(edge_gap(r["pct"]) for r in TS["rows"]) >= 0.02, "every September fall per cent mid-bin")
    check(len({r["fall"] for r in TS["rows"]}) == len(TS["rows"]), "no two dollar falls equal")
    under = sorted([r for r in TS["rows"] if r["pct"] < P.line], key=lambda r: -r["pct"])
    check(under[0]["pct"] - under[1]["pct"] >= 0.3 and 6.0 <= under[0]["pct"] <= 8.5,
          f"first outside the line {P.name[under[0]['cc']]} at {pct1(under[0]['pct'])} per cent")
    check(sum(1 for r in TS["rows"] if r["offer"] == P.cap) == 1 and
          not any(r["offer"] == P.floor for r in TS["rows"]), "one capped offer, none at the floor")
    # the rungs and the cells
    rungs = {"R1": rivals["R1"], "R2": rivals["R2"], "R3": rivals["R3"], "R4": dict(recency="off")}
    RS = {k: S.run(SEPT, pot, **o) for k, o in rungs.items()}
    names = {k: {r["cc"] for r in s["rows"] if r["offer"]} for k, s in RS.items()}
    names["T"] = {r["cc"] for r in el}
    # R0 at September
    r0rows = []
    for cc, refs in P.org_refs.items():
        g = P.grant[P.op_ref[cc]]
        if not g["start"] <= SEPT <= g["end"]:
            continue
        recs = sorted(q for (k, q), x in P.reg.items() if k == cc and x["rec"] <= SEPT.isoformat())
        if len(recs) >= 2 and q_add(recs[-2], 4) == recs[-1]:
            cu, pr = P.reg[(cc, recs[-1])]["total"], P.reg[(cc, recs[-2])]["total"]
            r0rows.append(dict(cc=cc, fall=pr - cu, pct=100.0 * (pr - cu) / pr))
    r0el = [r for r in r0rows if r["pct"] >= P.line]
    r0rate, _ = strike(P, [r["fall"] for r in r0el], pot)
    RS["R0"] = dict(rate=r0rate)
    names["R0"] = {r["cc"] for r in r0el}
    for k, lo_ in (("R0", 1.15), ("R1", 1.40), ("R2", 1.40), ("R3", 1.30), ("R4", 2.00)):
        check(TS["rate"] >= lo_ * RS[k]["rate"], f"the answer at {TS['rate']/RS[k]['rate']:.3f}x {k}'s rate")
    ks = sorted(names)
    for x, y in combinations(ks, 2):
        check(names[x] != names[y], f"{x} and {y} name different offer sets")
    check(len(names["R3"] ^ names["T"]) >= 6, f"R3 and T differ by {len(names['R3'] ^ names['T'])} names")
    check(names["T"] < names["R4"] and len(names["R4"] - names["T"]) == 5,
          "the answer's offers are R4's less five it does not score")
    check(len(RS["R4"]["rows"]) == 146 and len(RS["R3"]["rows"]) == 147 and len(RS["R2"]["rows"]) == 147 and
          len(RS["R1"]["rows"]) == 154, "R4 scores 146, R3 and R2 147, R1 154 rows")
    gone = {r["cc"] for r in RS["R4"]["rows"]} - {r["cc"] for r in TS["rows"]}
    m26 = P.packs[2026]["rows"]
    r4map = {r["cc"]: r for r in RS["R4"]["rows"]}
    check(len(gone) == 14 and all(r4map[cc]["end"] == (2025, 12) and P.bal[cc] == 3 and
                                  (r4map[cc]["cur"], r4map[cc]["prior"]) == m26[cc][:2] for cc in gone),
          "the fourteen R4 scores and the answer does not: 31 March grantees on the March 2026 round's own twelve months")
    cells = {"dual twice": dict(unit="ref"), "latest": dict(latest=True), "dual twice, latest": dict(unit="ref", latest=True),
             "30 June unstepped": dict(bals={3, 12}), "only 30 June stepped": dict(bals={6}),
             "prior natural": dict(prior_natural=True), "register at extract": dict(reg_extract=True),
             "census exclusive": dict(strict=True), "4.1 strict": dict(recency="strict"),
             "4.1 a year before": dict(recency="year"), "R4 dual twice": dict(unit="ref", recency="off"),
             "R4 latest": dict(latest=True, recency="off"), "fallback": dict(stepback="none"),
             "overdue": dict(stepback="overdue")}
    CS = {k: S.run(SEPT, pot, **o) for k, o in cells.items()}
    for k in ("30 June unstepped", "prior natural", "4.1 strict"):
        check(CS[k]["rate"] >= 1.10 * TS["rate"], f"cell {k} at {CS[k]['rate']/TS['rate']:.3f}x")
    check(CS["only 30 June stepped"]["rate"] <= 0.80 * TS["rate"],
          f"cell only 30 June stepped at {CS['only 30 June stepped']['rate']/TS['rate']:.3f}x")
    for k in ("dual twice", "latest", "dual twice, latest", "R4 dual twice", "R4 latest"):
        check(CS[k]["rate"] <= 0.92 * TS["rate"], f"cell {k} {100*(CS[k]['rate']/TS['rate']-1):+.1f}%")
    toffers = {r["cc"]: r["offer"] for r in TS["rows"] if r["offer"]}
    for k, dn in (("census exclusive", -14), ("register at extract", 6)):
        x = CS[k]
        check(x["rate"] == TS["rate"] and {r["cc"]: r["offer"] for r in x["rows"] if r["offer"]} == toffers and
              len(x["rows"]) - len(TS["rows"]) == dn, f"{k}: the same rate and offers, {len(x['rows'])} scored")
    sig = lambda s_: sorted((r["cc"], r["cur"], r["prior"], r["offer"]) for r in s_["rows"])
    check(sig(CS["fallback"]) == sig(RS["R3"]) and sig(CS["overdue"]) == sig(RS["R3"]),
          "the register fallback and the overdue-only step-back both equal R3 at September")
    check(sig(CS["4.1 a year before"]) == sig(RS["R4"]), "rule 4.1 read against the census a year before equals R4")
    out["september"] = dict(rate=TS["rate"], total=TS["total"], scored=len(TS["rows"]),
                            first_outside=[P.name[under[0]["cc"]], pct1(under[0]["pct"])],
                            rungs={k: RS[k]["rate"] for k in RS}, cells={k: v["rate"] for k, v in CS.items()})
    # --- the asks
    G = {}
    for r in TS["rows"]:
        G[r["cc"]] = dict(K1=A.k1(r, SEPT), K2=A.k2(r, SEPT))
    off = [r for r in TS["rows"] if r["offer"]]
    n = len(off)
    r3map = {r["cc"]: r for r in RS["R3"]["rows"]}
    stops = {"K1 GOV_GRT on both forms": lambda r: A.k1(r, SEPT, mapping="label"),
             "K1 comparatives": lambda r: A.k1(r, SEPT, comps=True),
             "K1 whole fees": lambda r: A.k1(r, SEPT, mapping="over"),
             "K1 project copy": lambda r: A.k1(r, SEPT, how="pg"),
             "K1 delivered": lambda r: A.k1(r, SEPT, how="delivered"),
             "K2 payment run alone": lambda r: A.k2(r, SEPT, sgf=False),
             "K2 instalment month": lambda r: A.k2(r, SEPT, how="for"),
             "K2 returned": lambda r: A.k2(r, SEPT, statuses=("paid", "returned")),
             "K2 ten-day transit": lambda r: A.k2(r, SEPT, how="transit"),
             "K2 one reference": lambda r: A.k2(r, SEPT, drop_pg=True)}
    moved = {}
    for name, fn in stops.items():
        ask = name[:2]
        d = [(r["cc"], fn(r) - G[r["cc"]][ask]) for r in off]
        check(all(x == 0 or abs(x) >= 500 for _, x in d), f"stop {name}: no offered figure within NZ$500 of the answer")
        moved[name] = sum(1 for _, x in d if x)
    for name, lo_ in (("K1 GOV_GRT on both forms", n - 1), ("K1 comparatives", n - 3), ("K1 whole fees", n),
                      ("K2 payment run alone", n), ("K2 instalment month", n - 2), ("K2 ten-day transit", n)):
        check(moved[name] >= lo_, f"stop {name} moves {moved[name]} of {n} offered figures")
    for name, want in (("K2 returned", 1), ("K2 one reference", 1), ("K1 project copy", 1), ("K1 delivered", 2)):
        check(moved[name] == want, f"stop {name} moves {moved[name]} offered figure(s)")
    same = [r["cc"] for r in off if (r4map[r["cc"]]["end"], r4map[r["cc"]]["pend"]) == (r["end"], r["pend"])]
    check(len(same) == n, "R4 holds every offered grantee on the answer's windows (only the devices separate it)")
    mir = [(r["cc"], A.k1(r3map[r["cc"]], SEPT, q4="portal") - G[r["cc"]]["K1"],
            A.k2(r3map[r["cc"]], SEPT) - G[r["cc"]]["K2"]) for r in off if r3map[r["cc"]]["end"] != r["end"]]
    check(len(mir) == 2 and all(abs(x) >= 500 and abs(y) >= 500 for _, x, y in mir),
          "R3's windows miss both 30 June offerees on K1 and K2")
    # the new-form Trust memo equals the payment run by value date; Steady Ground money is in neither
    run = A.run_series(sgf=False)
    full = A.run_series()
    bad = nchk = outside = 0
    for (cc, q), lst in S.by_org.items():
        if q < (2024, 12):
            continue
        v = lst[-1]
        if "GRT_NGO_APT" not in v["ytd"]:
            continue
        k = fy_pos(q, P.bal[cc])
        nchk += 1
        want = sum(run[(cc, q_add(q, -j))] for j in range(k))
        if v["ytd"]["GRT_NGO_APT"] != want:
            bad += 1
        if sum(full[(cc, q_add(q, -j))] for j in range(k)) != want:
            outside += 1
    check(bad == 0 and nchk > 800, f"Trust memo equals the payment run on {nchk} returns")
    check(outside >= 100, f"Steady Ground instalments sit outside the memo and the run on {outside} returns")
    # distractors: delete them and the answer does not move
    tmp = tempfile.mkdtemp()
    try:
        t2 = os.path.join(tmp, "target")
        shutil.copytree(target, t2)
        for d in dis:
            os.remove(os.path.join(t2, d))
        S2 = Screen(Pack(t2))
        T2 = S2.run(SEPT, pot)
        check((T2["rate"], sorted((r["cc"], r["offer"]) for r in T2["rows"])) ==
              (TS["rate"], sorted((r["cc"], r["offer"]) for r in TS["rows"])),
              "with both distractors deleted the call is unchanged")
    finally:
        shutil.rmtree(tmp)
    # the extract record: every row count it states is the file's own, and none equals a screen figure
    rec = open(os.path.join(target, "warehouse_extract_record_2026-10-07.md"), encoding="utf-8").read()
    stated = {m.group(1): int(m.group(2).replace(",", "")) for m in
              re.finditer(r"^\| (\S+\.csv) \|[^|\n]*\(([\d,]+) rows\)", rec, re.M)}
    check(len(stated) == 4, f"the extract record states row counts for {sorted(stated)}")
    for fn, n in sorted(stated.items()):
        with open(os.path.join(target, fn), newline="", encoding="utf-8") as fh:
            have = sum(1 for _ in csv.DictReader(fh))
        check(have == n, f"the extract record's {n:,} rows for {fn} match the file ({have:,})")
    figs = {abs(v) for r in TS["rows"] for v in (r["cur"], r["prior"], r["fall"], r["offer"],
                                                 G[r["cc"]]["K1"], G[r["cc"]]["K2"]) if v is not None}
    figs |= {TS["rate"], sum(r["offer"] for r in TS["rows"]), len(TS["rows"]), len(off)}
    check(not (set(stated.values()) & figs), "no row count in the extract record equals a figure of the screen")
    out["golden"] = {"rate_cents": TS["rate"] / 100, "offers": [
        dict(name=P.name[r["cc"]], cc=r["cc"], offer=r["offer"], fall=r["fall"], pct=pct1(r["pct"]),
             K1=G[r["cc"]]["K1"], K2=G[r["cc"]]["K2"]) for r in sorted(off, key=lambda r: -r["fall"])],
        "screen": [dict(name=P.name[r["cc"]], cc=r["cc"], cur=r["cur"], prior=r["prior"], fall=r["fall"],
                        pct=pct1(r["pct"]), offer=r["offer"], K1=G[r["cc"]]["K1"], K2=G[r["cc"]]["K2"])
                   for r in sorted(TS["rows"], key=lambda r: -r["fall"])],
        "replay_rows_given_back": {y: len(P.packs[y]["rows"]) for y in sorted(P.packs)}}
    out["checks"] = N_CHECKS[0]
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(out, fh, indent=1, default=str)
    print(f"task123 verifier: {N_CHECKS[0]} checks green from the shipped bytes")
    print(f"September rate {TS['rate']/100:.2f} cents; {len(off)} offers; {len(TS['rows'])} scored; "
          f"first outside {P.name[under[0]['cc']]} {pct1(under[0]['pct'])}%")


if __name__ == "__main__":
    main()
