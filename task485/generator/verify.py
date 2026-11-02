"""task485's independent verifier: every graded figure recomputed from target/ on a code path of its own (its own
XLSX reader on the zip's XML, its own PDF decoder for ASCII85 and Flate streams, the csv and text files read raw, the
account codes mapped through the statements' own account names, the manufacturers matched by their first word, each
manufacturer's rebates solved by the normal equations), then compared with generator/figures.json, the golden
workbook and the golden slides read back the same way.

    python3 task485/generator/verify.py
"""
import base64
import collections
import csv
import datetime as dt
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


# ------------------------------------------------------------------ readers
def xlsx(path):
    """{sheet name: [row values]} from the package XML, shared and inline strings resolved."""
    z = zipfile.ZipFile(path)
    names = z.namelist()
    shared = []
    if "xl/sharedStrings.xml" in names:
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wbx = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wbx.find("m:sheets", NS):
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        t = target[rid].lstrip("/")
        t = t if t.startswith("xl/") else "xl/" + t
        rows = []
        for row in ET.fromstring(z.read(t)).iter("{%s}row" % NS["m"]):
            vals = {}
            for c in row.findall("m:c", NS):
                ref = c.get("r")
                col = 0
                for ch in re.match(r"[A-Z]+", ref).group(0):
                    col = col * 26 + ord(ch) - 64
                typ, v = c.get("t"), c.find("m:v", NS)
                if typ == "s":
                    val = shared[int(v.text)]
                elif typ == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif typ == "str":
                    val = v.text if v is not None else ""
                elif v is not None:
                    f = float(v.text)
                    val = int(f) if f == int(f) and "." not in v.text and "E" not in v.text else f
                else:
                    val = None
                vals[col] = val
            k = int(row.get("r")) - 1
            while len(rows) < k:
                rows.append([])
            rows.append([vals.get(i) for i in range(1, max(vals) + 1)] if vals else [])
        out[sh.get("name")] = rows
    return out


def pdf_text(path):
    data = open(path, "rb").read()
    parts = []
    for m in re.finditer(rb"/Filter\s*\[?([^\]>]*)\]?[^>]*>>\s*stream\r?\n", data):
        start = m.end()
        end = data.index(b"endstream", start)
        body, filt = data[start:end], m.group(1)
        if b"ASCII85Decode" in filt:
            body = body.strip()
            if body.endswith(b"~>"):
                body = body[:-2]
            body = base64.a85decode(body)
        if b"FlateDecode" in filt:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        parts.append(body)
    words = []
    for body in parts:
        for s in re.findall(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", body):
            s = re.sub(rb"\\([()\\])", rb"\1", s)
            s = re.sub(rb"\\(\d{3})", lambda mm: bytes([int(mm.group(1), 8)]), s)
            words.append(s.decode("latin-1"))
    return re.sub(r"\s+", " ", " ".join(words))


def day(s):
    s = s.strip()
    if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", s):
        mo, d, y = map(int, s.split("/"))
        return dt.date(y, mo, d)
    y, mo, d = map(int, s.split("-"))
    return dt.date(y, mo, d)


def quarter(d):
    if not (dt.date(2025, 7, 1) <= d <= dt.date(2026, 6, 30)):
        return None
    return "Q%d" % (((d.month - 7) % 12) // 3 + 1)


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(TARGET))

    # drug file
    dsheet = xlsx(os.path.join(TARGET, "pbm_drug_file_202610.xlsx"))["Drug File"]
    h = dsheet[0]
    drug = {}
    for r in dsheet[1:]:
        rec = dict(zip(h, r))
        drug[str(rec["NDC"]).zfill(11)] = rec
    ok("drug file read: %d NDCs" % len(drug), len(drug) > 20)

    # clinical review: classes, products and 30-day quantities
    rv = pdf_text(os.path.join(TARGET, "clinical_review_2027_pdl.pdf"))
    brands = sorted({v["Proprietary Name"] for v in drug.values()}, key=len, reverse=True)
    t1 = rv[rv.index("Products compared"):rv.index("The 30-day supply")]
    class_names = re.findall(r"(GLP-1 receptor agonists|SGLT2 inhibitors|Long-acting insulins|Direct oral anticoagulants|"
                             r"Inhaled corticosteroid and LABA combinations|Adalimumab products)", t1)
    cls = {}
    for i, c in enumerate(class_names):
        seg = t1[t1.index(c): t1.index(class_names[i + 1]) if i + 1 < len(class_names) else len(t1)]
        for b in brands:
            if re.search(r"(?<![\w-])%s \(" % re.escape(b), seg) and b not in cls:
                cls[b] = c
    t2 = rv[rv.index("30-day supply (quantity)"):]
    q30 = {}
    for b in cls:
        m = re.search(r"(?<![\w-])%s .+? (\d+(?:\.\d+)?) (?:each|mL|g)\b" % re.escape(b), t2)
        q30[b] = float(m.group(1))
    ok("clinical review read: %d products in %d classes, each with its 30-day quantity" % (len(cls), len(set(cls.values()))),
       len(cls) == 17 and len(set(cls.values())) == 6 and len(q30) == 17)

    # statements: account codes mapped by the account name on each line, manufacturers by first word
    lines = []
    code_name = {}
    for f in files:
        if not f.startswith("rebate_remittance_"):
            continue
        rows = xlsx(os.path.join(TARGET, f))["Remittance"]
        hi = [i for i, r in enumerate(rows) if r and r[0] == "Manufacturer"][0]
        for r in rows[hi + 1:]:
            if not r or not r[0] or str(r[0]).startswith("Total"):
                continue
            code_name[str(r[1])] = r[2]
            lines.append(dict(mfr=r[0].split()[0].upper(), acct=r[2], svc=r[4], kind=r[3], amt=float(r[5])))
    svcq = {"Jul-Sep 2025": "Q1", "Oct-Dec 2025": "Q2", "Jan-Mar 2026": "Q3", "Apr-Jun 2026": "Q4"}
    ok("statements read: %d lines, %d account codes named" % (len(lines), len(code_name)), len(code_name) == 8)

    # claims
    paid, revd = {}, set()
    with open(os.path.join(TARGET, "pbm_paid_claims_fy2026.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["claim_status"] == "R":
                revd.add(r["reversal_of"])
                continue
            nd = r["ndc"].replace("-", "")
            paid[r["claim_number"]] = dict(
                dos=day(r["date_of_service"]), acct=code_name[r["group_id"]], brand=drug[nd]["Proprietary Name"],
                mfr=drug[nd]["Labeler Name"].split()[0].upper(), pkg=float(drug[nd]["Package Quantity"]),
                qty=float(r["quantity_dispensed"]), ds=int(r["days_supply"]), ingr=float(r["ingredient_cost_paid"]),
                fee=float(r["dispensing_fee_paid"]), comp=r["compound_code"] == "2", npi=r["pharmacy_npi"],
                card=r["cardholder_id"], pc=r["person_code"], dob=day(r["patient_dob"]), sex=r["patient_gender"])
    live = [c for n, c in paid.items() if n not in revd]
    ok("claims read: %d paid rows, %d reversed, %d counted" % (len(paid), len(revd), len(live)), len(live) > 40000)

    # the fit: per manufacturer, normal equations on 30-day supplies per account and quarter of service
    accts = sorted(set(code_name.values()))
    qs = ["Q1", "Q2", "Q3", "Q4"]
    units = collections.defaultdict(float)
    cost = collections.defaultdict(float)
    cell = collections.defaultdict(float)
    for c in live:
        u = c["qty"] / q30.get(c["brand"], c["pkg"])
        units[c["brand"]] += u
        cost[c["brand"]] += c["ingr"]
        if not c["comp"]:
            cell[(c["brand"], c["acct"], quarter(c["dos"]))] += u
    remit = collections.defaultdict(float)
    for l in lines:
        if l["svc"] in svcq:
            remit[(l["mfr"], l["acct"], svcq[l["svc"]])] += l["amt"]
    mfr_brands = collections.defaultdict(set)
    for c in live:
        mfr_brands[c["mfr"]].add(c["brand"])
    rate = {}
    worst = 0.0
    for m, bs in mfr_brands.items():
        bs = sorted(bs)
        X = np.array([[cell[(b, a, q)] for b in bs] for a in accts for q in qs])
        y = np.array([remit[(m, a, q)] for a in accts for q in qs])
        beta = np.linalg.solve(X.T @ X, X.T @ y)
        worst = max(worst, float(np.max(np.abs(X @ beta - y))))
        rate.update(zip(bs, beta))
    ok("every manufacturer's remittances solved exactly (largest cell residual under a cent)", worst < 0.01,
       "%.5f" % worst)
    net = {b: (cost[b] - rate[b] * units[b]) / units[b] for b in cls}
    for b in cls:
        ok("net cost %s %d" % (b, figs["net." + b]), int(round(net[b] / 10.0)) * 10 == figs["net." + b],
           "%.2f" % net[b])
    picks = {}
    for b, c in cls.items():
        if c not in picks or net[b] < net[picks[c]]:
            picks[c] = b
    for c, b in picks.items():
        ok("preferred %s: %s" % (c, b), figs["call." + c] == b)
    # the default split, for the record
    split = {}
    for m, bs in mfr_brands.items():
        total = sum(remit[(m, a, q)] for a in accts for q in qs)
        s = sum(cost[b] for b in bs)
        for b in bs:
            split[b] = (cost[b] - total * cost[b] / s) / units[b]
    dpk = {}
    for b, c in cls.items():
        if c not in dpk or split[b] < split[dpk[c]]:
            dpk[c] = b
    ok("the split by ingredient cost files a different set (Liraquent, insulin glargine-qmrt, Saltiva)",
       {dpk[c] for c in dpk} - {picks[c] for c in picks} == {"Liraquent", "insulin glargine-qmrt", "Saltiva"})

    # Exhibit C: rates, channels on the date of service, remittances by service period
    ex = pdf_text(os.path.join(TARGET, "pbm_agreement_exhibit_c.pdf"))
    rates = {}
    for key, lab in (("RETAIL30", "Retail, days supply under 84"), ("RETAIL90", "Retail, days supply 84 or more"),
                     ("MAIL", "Mail order"), ("SPECIALTY", "Specialty")):
        rates[key] = float(re.search(re.escape(lab) + r" ([\d,]+\.\d\d)", ex).group(1).replace(",", ""))
    network = {}
    for ln in open(os.path.join(TARGET, "pharmacy_network_202610.txt"), encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("|")
        network[f[0]] = f[4]
    for i, q in enumerate(qs, 1):
        n = collections.Counter()
        for c in live:
            if quarter(c["dos"]) != q or c["comp"]:
                continue
            netw = "RETAIL" if c["fee"] > 0 else network[c["npi"]]
            n[("RETAIL90" if c["ds"] >= 84 else "RETAIL30") if netw == "RETAIL" else netw] += 1
        g = sum(n[k] * rates[k] for k in rates)
        rem = sum(l["amt"] for l in lines if svcq.get(l["svc"]) == q)
        sf = max(0.0, g - rem)
        fk = "FQ%d" % i
        ok("guarantee %s: claims by channel, guarantee, remitted, shortfall" % fk,
           all(n[k] == figs["guar.%s.%s" % (fk, k)] for k in rates) and int(round(g)) == figs["guar.%s.guarantee" % fk]
           and int(round(rem)) == figs["guar.%s.remitted" % fk] and int(round(sf)) == figs["guar.%s.shortfall" % fk],
           "%s %d %d %d" % (dict(n), g, rem, sf))

    # members: old identities joined to the roster on legacy cardholder number, birth date and gender
    roster = list(csv.DictReader(open(os.path.join(TARGET, "member_roster_20261009.csv"), encoding="utf-8")))
    fam = {r["legacy_cardholder_id"]: r["cardholder_id"] for r in roster if r["legacy_cardholder_id"]}
    who = {(r["cardholder_id"], day(r["birth_date"]), r["gender"]): r["member_id"] for r in roster}
    by_new = {(r["cardholder_id"], r["person_code"]): r["member_id"] for r in roster}

    def person(c):
        if c["dos"] >= dt.date(2026, 1, 1):
            return by_new.get((c["card"], c["pc"]), "new:%s%s" % (c["card"], c["pc"]))
        nc = fam.get(c["card"])
        hit = who.get((nc, c["dob"], c["sex"])) if nc else None
        return hit or "old:%s%s" % (c["card"], c["pc"])
    mem = collections.defaultdict(set)
    for c in live:
        if c["brand"] in cls:
            mem[(cls[c["brand"]], c["acct"])].add(person(c))
    good = all(len(mem[(c, a)]) == figs["members.%s.%s" % (c, a)] for c in set(cls.values()) for a in accts)
    ok("members by class and account (24 cells)", good)

    # the golden deliverables read back
    gw = xlsx(os.path.join(GOLDEN, "pdl_2027_net_cost.xlsx"))
    t = gw["Net cost FY2026"]
    hdr = t[2]
    body = [dict(zip(hdr, r)) for r in t[3:] if r and r[0] in set(cls.values())]
    ok("golden workbook: every compared product's net cost and status", len(body) == 17 and all(
        r["Net cost per 30-day supply (USD)"] == figs["net." + r["Product"]] and
        (r["2027 status"] == "Preferred") == (picks[cls[r["Product"]]] == r["Product"]) for r in body))
    gsh = [r for r in gw["Rebate guarantee"][3:7]]
    ok("golden workbook: the guarantee table", all(
        r[5] == figs["guar.FQ%d.guarantee" % i] and r[6] == figs["guar.FQ%d.remitted" % i] and
        r[7] == figs["guar.FQ%d.shortfall" % i]
        for i, r in enumerate(gsh, 1)))
    msh = gw["Members"]
    ok("golden workbook: the members table", all(
        msh[i][j + 1] == figs["members.%s.%s" % (msh[i][0], a)] for i in range(3, 9) for j, a in enumerate(msh[2][1:])))
    z = zipfile.ZipFile(os.path.join(GOLDEN, "pdl_2027_trustees.pptx"))
    s1 = re.sub(r"<[^>]+>", " ", z.read("ppt/slides/slide1.xml").decode("utf-8"))
    ok("golden slides: slide 1 names every preferred product with its net cost",
       all(b in s1 and "${:,}".format(figs["net." + b]) in s1 for b in picks.values()))
    charts = [n for n in z.namelist() if n.startswith("ppt/charts/chart")]
    ok("golden slides: slide 2 carries native charts of every product's net cost", len(charts) == 2 and all(
        str(figs["net." + b]) in "".join(z.read(n).decode("utf-8") for n in charts) for b in cls))

    # every shipped format read back
    fmts = collections.Counter(f.rsplit(".", 1)[1] for f in files)
    ok("every shipped format read by this verifier (csv, xlsx, txt, pdf)", set(fmts) == {"csv", "xlsx", "txt", "pdf"},
       str(dict(fmts)))
    for f in files:
        if f.endswith(".pdf"):
            ok("pdf read back: %s" % f, len(pdf_text(os.path.join(TARGET, f))) > 500)

    bad = [r for r in RESULTS if not r[1]]
    for lab, good_, det in RESULTS:
        print("%s  %s%s" % ("PASS" if good_ else "FAIL", lab, ("  [%s]" % det) if det and not good_ else ""))
    print("verify: %d of %d" % (len(RESULTS) - len(bad), len(RESULTS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
