"""task274 ask ceiling, measured on the cut pack.

    python3 task274/generator/ceiling.py [--pack DIR]

Reads only the shipped files under target/ (or an unzipped copy) and the golden figures in
generator/figures.json, and shares no code with the generator. It runs the careful solver's routes through
every ask: the cracker (lands the call, runs the hygiene battery, executes what the files state), the mirror
(off the call at full scale, the same ask handling), and for each ask the full includer of each device (a
response that notices that device and handles it, and nothing else it was not shown). Each graded ask figure
is a hit only when it equals the golden figure at the asking sentence's rounding (whole cases, hours and
dollars). The pair is priced on the standard weights: call and critical components 38, instructions 7, asks 55.
"""
import csv
import datetime as dt
import glob
import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def pack_dir():
    if "--pack" in sys.argv:
        return sys.argv[sys.argv.index("--pack") + 1]
    return os.path.join(TASK, "target")


PACK = pack_dir()
FY0, FY1 = dt.date(2025, 7, 1), dt.date(2026, 6, 30)


def read_csv(name):
    with open(os.path.join(PACK, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def case_key(s):
    """A court case reference typed any of the ways the files type it, as (division, yy, type, number)."""
    s = s.strip().upper()
    m = re.fullmatch(r"(LC|BW|WM|SH)(\d{2})(CM|CR)(\d{5})", s)
    if m:
        return (m.group(1), m.group(2), m.group(3), int(m.group(4)))
    m = re.fullmatch(r"(\d{2})-(CM|CR)-(\d{5})-(LC|BW|WM|SH)", s)
    if m:
        return (m.group(4), m.group(1), m.group(2), int(m.group(3)))
    m = re.fullmatch(r"(LC|BW|WM|SH)-(\d{2})-(CM|CR)-(\d{5})", s)
    if m:
        return (m.group(1), m.group(2), m.group(3), int(m.group(4)))
    m = re.fullmatch(r"(\d{2})(CM|CR)(\d+) (LC|BW|WM|SH)", s)
    if m:
        return (m.group(4), m.group(1), m.group(2), int(m.group(3)))
    m = re.fullmatch(r"(LC|BW|WM|SH) (\d{2}) (CM|CR) (\d+)", s)
    if m:
        return (m.group(1), m.group(2), m.group(3), int(m.group(4)))
    m = re.fullmatch(r"20(\d{2})-(CM|CR)-(\d{5}) \((LC|BW|WM|SH)\)", s)
    if m:
        return (m.group(4), m.group(1), m.group(2), int(m.group(3)))
    raise ValueError("unparsed reference %r" % s)


DIV = {"LC": "Larkmoor City", "BW": "Bramwick", "WM": "Wendmoor", "SH": "Strandham"}


def policy_classes():
    """Eligible 2026 sections by class, read from the Unit's policy table."""
    with zipfile.ZipFile(os.path.join(PACK, "pretrial_diversion_policy_pdu_2026_01.docx")) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    cells = re.findall(r"<w:tc>.*?</w:tc>", xml, re.S)
    texts = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", c)) for c in cells]
    out = {}
    for i in range(3, len(texts) - 2, 3):
        cls, sec = texts[i], texts[i + 1]
        if re.fullmatch(r"\d{3}\.\d{2}", sec):
            out[sec] = cls
    return out


CLASS_LABEL = {"A, theft and fraud": "Theft and fraud", "B, criminal damage": "Criminal damage",
               "C, drug possession": "Drug possession", "D, public order": "Public order",
               "E, license and driving": "License and driving"}


def filings(rule):
    """FY2026 cases by eligible class and by division under one reading of the charge sections."""
    conv = {r["section_2025"]: r["section_2026"] for r in read_csv("penal_code_conversion_table_2026.csv")}
    cls = policy_classes()
    legacy = read_csv("legacy_case_charges.csv")
    cms = read_csv("cms_case_charges.csv")
    lead = {}
    seen = set()
    for r in legacy:
        t = tuple(r.values())
        if t in seen:
            continue                     # a clerk's re-entry
        seen.add(t)
        if r["charge_seq"] != "1":
            continue
        k = case_key(r["case_number"])
        lead[k] = dict(src="legacy", filed=dt.datetime.strptime(r["filed_date"], "%m/%d/%Y").date(),
                       off=dt.datetime.strptime(r["offense_date"], "%m/%d/%Y").date(), sec=r["statute_section"])
    for r in cms:
        if r["count_number"] != "1":
            continue
        k = case_key(r["case_number"])
        prior = lead.get(k)
        lead[k] = dict(src="cms", filed=dt.date.fromisoformat(r["filing_date"]),
                       off=dt.date.fromisoformat(r["offense_date"]), sec=r["statute_section"],
                       converted=prior is not None, legacy_sec=prior["sec"] if prior else None)
    by_cls, by_div = Counter(), Counter()
    recode = dt.date(2026, 1, 1)
    for k, r in lead.items():
        if not (FY0 <= r["filed"] <= FY1):
            continue
        sec = rule(r, conv, recode)
        c = cls.get(sec)
        if c:
            by_cls[CLASS_LABEL[c]] += 1
            by_div[DIV[k[0]]] += 1
    return by_cls, by_div


def rule_filing_date(r, conv, recode):        # the cracker: the dated mapping, mapping what maps
    return conv.get(r["sec"], r["sec"]) if r["filed"] < recode else r["sec"]


def rule_offence_date(r, conv, recode):       # full includer of the offense-date device only
    return conv.get(r["sec"], r["sec"]) if r["off"] < recode else r["sec"]


def rule_conversion_aware(r, conv, recode):   # full includer of the conversion device only
    if r["src"] == "cms" and r.get("converted"):
        return r["sec"]
    return conv.get(r["sec"], r["sec"]) if r["filed"] < recode else r["sec"]


def rule_golden(r, conv, recode):
    if r["src"] == "cms" and r.get("converted"):
        return r["sec"]
    return conv[r["sec"]] if r["off"] < recode else r["sec"]


# ---------------------------------------------------------------------------------------------------------
# the provider's monthly reports


def load_reports():
    from openpyxl import load_workbook
    out = []
    for p in sorted(glob.glob(os.path.join(PACK, "nethercote_reports", "*.xlsx"))):
        ws = load_workbook(p, read_only=True).active
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        hdr_i = next(i for i, r in enumerate(rows) if r and r[0] in ("Client No", "Participant ID"))
        meta = " ".join(str(r[0]) for r in rows[:hdr_i] if r and r[0])
        m = re.search(r"(?:Report month|Period): ([A-Za-z]+ \d{4})", meta)
        month = dt.datetime.strptime(m.group(1), "%B %Y").date()
        system = "old" if rows[hdr_i][0] == "Client No" else "new"
        hdr = rows[hdr_i]
        recs = []
        for r in rows[hdr_i + 1:]:
            if not r or r[0] is None or not str(r[0]).startswith(("C", "P")) or len(str(r[0])) < 5:
                continue
            d = dict(zip(hdr, r))
            if system == "old":
                hh, mm = str(d["CS Hrs"]).split(":")
                recs.append(dict(key=case_key(d["Court Ref"]), site=d["Site"], hours=int(hh) + int(mm) / 60.0,
                                 rest=float(d["Restitution Rcvd"] or 0), pid=d["Client No"]))
            else:
                recs.append(dict(key=case_key(d["Case Number"]), site=d["Location"],
                                 hours=float(d["Community Service Hours"] or 0), rest=float(d["Restitution"] or 0),
                                 pid=d["Participant ID"]))
        out.append(dict(path=os.path.basename(p), month=month, system=system, recs=recs))
    return out


def fy_month(m):
    return FY0 <= m <= FY1


def provider(handling):
    """Each site's FY2026 hours and restitution under one handling of the reports."""
    reps = [r for r in load_reports() if fy_month(r["month"])]
    jan = [r for r in reps if r["month"] == dt.date(2026, 1, 1)]
    new_jan_keys = {x["key"] for r in jan if r["system"] == "new" for x in r["recs"]}
    hours, rest = Counter(), Counter()
    last_cum = {}
    old_hours = defaultdict(float)
    prev_cum = {}
    for rep in sorted(reps, key=lambda r: (r["month"], r["system"] == "new")):
        for x in rep["recs"]:
            dup_jan = rep["system"] == "old" and rep["month"] == dt.date(2026, 1, 1) and x["key"] in new_jan_keys
            keep_both_halves = handling.get("sum_january")
            if dup_jan and not keep_both_halves:
                pass
            else:
                r_amt = x["rest"] / 0.95 if (rep["system"] == "new" and handling.get("gross_up")) else x["rest"]
                rest[x["site"]] += r_amt
            if rep["system"] == "old":
                old_hours[x["key"]] += x["hours"]
                if not (dup_jan and not keep_both_halves) and handling.get("hours") in ("as_given", "difference"):
                    hours[x["site"]] += x["hours"]
            else:
                if handling.get("hours") == "as_given":
                    hours[x["site"]] += x["hours"]
                elif handling.get("hours") == "difference":
                    hours[x["site"]] += x["hours"] - prev_cum.get(x["key"], 0.0)
                prev_cum[x["key"]] = x["hours"]
                last_cum[x["key"]] = (x["site"], x["hours"])
    if handling.get("hours") == "cumulative":
        site_of = {}
        for rep in reps:
            for x in rep["recs"]:
                site_of[x["key"]] = x["site"]
        for k, (s, cum) in last_cum.items():
            hours[s] += cum
        for k, h in old_hours.items():
            if k not in last_cum:
                hours[site_of[k]] += h
    return ({s: int(round(v)) for s, v in hours.items()}, {s: int(round(v)) for s, v in rest.items()})


# ---------------------------------------------------------------------------------------------------------


def score(got, gold):
    return sum(1 for k, v in gold.items() if got.get(k) == v), len(gold)


def pack_digest():
    h = hashlib.sha256()
    for p in sorted(glob.glob(os.path.join(PACK, "**", "*"), recursive=True)):
        if os.path.isfile(p):
            h.update(os.path.relpath(p, PACK).encode())
            with open(p, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:12]


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    g_cls, g_div = F["filings_by_class"], F["filings_by_division"]
    g_h, g_r = F["hours_by_site"], F["restitution_by_site"]
    rows = []

    def court(label, rule):
        c, d = filings(rule)
        a = score(c, g_cls)
        b = score(d, g_div)
        return label, a[0] + b[0], a[1] + b[1], dict(c), dict(d)

    def prov(label, handling, which):
        h, r = provider(handling)
        a = score(h, g_h)
        b = score(r, g_r)
        if which == "hours":
            return label, a[0], a[1], h
        if which == "rest":
            return label, b[0], b[1], r
        return label, a[0] + b[0], a[1] + b[1], (h, r)

    golden_court = court("golden reading", rule_golden)
    golden_prov = prov("golden handling", dict(hours="cumulative", sum_january=True, gross_up=True), "both")
    assert golden_court[1] == golden_court[2], golden_court
    assert golden_prov[1] == golden_prov[2], golden_prov

    cracker = [
        court("filings by class and division: the dated mapping of the kept row", rule_filing_date),
        prov("site hours and restitution: the January rows matched and the later kept, the columns summed",
             dict(hours="as_given"), "both"),
    ]
    differencer = prov("site hours: the new system's figures differenced month on month, the January rows "
                       "matched and the later kept", dict(hours="difference"), "hours")
    includers = [
        court("filings, full includer of the go-live conversion only", rule_conversion_aware),
        court("filings, full includer of the offense-date charging only", rule_offence_date),
        prov("site hours, full includer of the system's running totals (restitution as the cracker)",
             dict(hours="cumulative"), "both"),
        prov("site restitution, full includer of the January halves only", dict(hours="cumulative", sum_january=True), "rest"),
        prov("site restitution, full includer of the remitted net only", dict(hours="cumulative", gross_up=True), "rest"),
    ]
    n_ask = golden_court[2] + golden_prov[2]
    kept_cracker = sum(r[1] for r in cracker)
    Lc = kept_cracker / n_ask
    Ls = Lc                     # the mirror runs the same ask handling off the call
    r_mirror = 5.0              # the mirror's main-side keep: the not-offered arm's share, nearly complete at the cut
    C = 38 + 7 + 55 * Lc
    S = r_mirror + 7 + 55 * Ls
    pair = (C + S) / 2
    print("pack %s, %d ask figures" % (pack_digest(), n_ask))
    print("| Ask route | kept | of |")
    for r in cracker + [differencer] + includers:
        print("| %s | %d | %d |" % (r[0], r[1], r[2]))
    print("cracker keeps %d of %d ask figures (L = %.3f); mirror keeps %d (L = %.3f)" % (kept_cracker, n_ask, Lc, kept_cracker, Ls))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f" % (C, S, pair))
    print("mirror leakage %.1f per cent of ask weight" % (100 * Ls))
    if "--detail" in sys.argv:
        details = dict(cracker=[r[3:] for r in cracker], differencer=differencer[3:], includers=[r[3:] for r in includers])
        print(json.dumps(details, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
