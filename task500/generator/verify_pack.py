"""Independent verifier for task500 v3. Reads only the shipped files in target/, the two deliverables and the
write-up, re-implements the standing procedure on its own code path (csv module, openpyxl, plain Python; no numpy, no
pandas, nothing imported from the generator), recomputes every graded figure and exits 1 on any disagreement."""
import csv
import datetime as dt
import hashlib
import json
import math
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

from openpyxl import load_workbook

TASK = Path(__file__).resolve().parent.parent
T = TASK / "target"
G = TASK / "golden"
GOLD = json.loads((Path(__file__).resolve().parent / "golden_figures.json").read_text())
fails = []
n_checks = 0


def same(a, b, what):
    global n_checks
    n_checks += 1
    if a != b:
        fails.append("%s: verifier %r, expected %r" % (what, a, b))


def rows(name):
    with open(T / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


MONTHS = []
y, m = 2022, 7
for _ in range(48):
    MONTHS.append("%d-%02d" % (y, m))
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
MI = {p: i for i, p in enumerate(MONTHS)}

reg = {r["filer_id"]: r for r in rows("lodging_filer_register_2026-08.csv")}
R = defaultdict(lambda: [0.0] * 48)
TX = defaultdict(lambda: [0.0] * 48)
cut_lines = defaultdict(float)
for r in rows("lodging_tax_returns_fy2023-fy2026.csv"):
    i = MI[r["period"]]
    R[r["filer_id"]][i] += float(r["taxable_receipts"])
    TX[r["filer_id"]][i] += float(r["tax_due"])
    if r["county"] in ("Prairie", "Bluff") and i >= MI["2025-10"]:
        cut_lines[r["filer_id"]] += float(r["taxable_receipts"])
ids = sorted(reg)
IDX = {f: i for i, f in enumerate(ids)}
for fid in ids:
    R[fid], TX[fid]
wb = load_workbook(T / "variance_statements_appendix_b_fy2024_fy2025.xlsx", data_only=True)
cert = {}
for code, ws in zip(("HW", "SD"), wb.worksheets):
    cert[code] = {row[0]: row[5] for row in ws.iter_rows(min_row=5, values_only=True)
                  if row[0] and str(row[0]).startswith("LT")}
LODGING = {"FS", "LS", "ES", "MO", "BB", "CG"}


def touched(year):
    if year == 2024:
        return {"HW": set(cert["HW"])}
    if year == 2025:
        return {"SD": set(cert["SD"])}
    t = {"CC": {f for f in ids if reg[f]["region"] == "Capital City Downtown" and reg[f]["class"] in ("FS", "LS")},
         "LX": {f for f in ids if reg[f]["class"] == "ES"},
         "CO": {f for f in ids if reg[f]["county"] in ("Prairie", "Bluff")},
         "PC": {f for f in ids if reg[f]["class"] == "STR"},
         "AH": {f for f in ids if reg[f]["region"] == "Airport Corridor" and reg[f]["class"] in ("FS", "LS")}}
    return t


EFF = {"HW": "2024-03", "SD": "2024-09", "CC": "2025-09", "LX": "2026-01", "AH": "2025-11", "PC": "2025-08",
       "CO": "2025-10"}


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def procedure(year, code):
    tset = touched(year)
    anyt = set().union(*tset.values())
    end = MI["%d-06" % year]
    eff = MI[EFF[code]]
    pool = [f for f in ids if f not in anyt and reg[f]["class"] in LODGING
            and all(R[f][t] > 0 for t in range(end - 23, end + 1))]

    def z(f):
        v = R[f][eff - 12:eff]
        mu = sum(v) / 12
        sd = math.sqrt(sum((x - mu) ** 2 for x in v) / 12) or 1.0
        return [(x - mu) / sd for x in v]
    zp = {f: z(f) for f in pool}
    order = sorted(tset[code], key=lambda f: (-sum(R[f][eff - 12:eff]), IDX[f]))
    used = defaultdict(int)
    out = {}
    for f in order:
        zf = z(f)
        cand = [g for g in pool if reg[g]["region"] != reg[f]["region"] and used[g] < 2]
        cand.sort(key=lambda g: (math.sqrt(sum((a - b) ** 2 for a, b in zip(zp[g], zf))), IDX[g]))
        peers = cand[:5]
        for g in peers:
            used[g] += 1
        ref = act = tax = 0.0
        for t in range(eff, end + 1):
            g_t = median([R[g][t] / R[g][t - 12] for g in peers])
            cf = R[f][t - 12] * g_t
            rate = TX[f][t] / R[f][t] if R[f][t] > 0 else 0.08
            ref += cf
            act += R[f][t]
            tax += rate * (R[f][t] - cf)
        out[f] = (act, ref, tax, peers)
    return out


# --------------------------------------------------------------------------- the certified figures reproduce
hit = 0
for year, code in ((2024, "HW"), (2025, "SD")):
    det = procedure(year, code)
    hit += sum(1 for f, v in cert[code].items() if round(det[f][1]) == v)
same(hit, 78, "Appendix B figures reproduced")

# --------------------------------------------------------------------------- fiscal 2026 effects
eff = {}
dets = {}
for code in ("CC", "LX", "AH"):
    dets[code] = procedure(2026, code)
    eff[code] = sum(v[2] for v in dets[code].values())
eff["CO"] = -0.005 * sum(cut_lines.values())
anyt = set().union(*touched(2026).values())
uni = [f for f in ids if f not in anyt and reg[f]["class"] in LODGING and all(R[f][t] > 0 for t in range(24, 48))]
hosts = [f for f in ids if reg[f]["class"] == "STR"]
pfs = [f for f in ids if reg[f]["class"] == "PF"]
pc = 0.0
for t in range(MI["2025-08"], 48):
    g = median([R[f][t] / R[f][t - 12] for f in uni])
    pc += sum(TX[f][t] for f in hosts + pfs) - sum(TX[f][t - 12] for f in hosts) * g
eff["PC"] = pc
for code, v in eff.items():
    same(round(v / 1000), round(GOLD["effects"][code] / 1000), "effect %s (thousands)" % code)
named = min(eff, key=eff.get)
same(named, "LX", "the change the statement names")
actual = sum(TX[f][t] for f in ids for t in range(36, 48))
forecast = sum(int(r["adopted_forecast_tax"]) for r in rows("adopted_forecast_lodging_fy2026.csv"))
same(round((forecast - actual) / 1000), round(GOLD["shortfall"] / 1000), "shortfall (thousands)")
residual = (actual - forecast) - sum(eff.values())
same(round(residual / 1000), round(GOLD["residual"] / 1000), "line no change accounts for (thousands)")

# --------------------------------------------------------------------------- cash reconciliation
ledger = rows("treasury_lodging_deposits_fy2025-fy2026.csv")
a, b = "2025-07-01", "2026-06-30"
own = other = refunds = 0.0
latest = {}
for r in ledger:
    inyr = a <= r["deposit_date"] <= b
    if r["type"] == "TAX" and inyr:
        if "2025-07" <= r["period"] <= "2026-06":
            own += float(r["amount"])
        else:
            other += float(r["amount"])
    elif r["type"] == "REFUND" and inyr:
        refunds += float(r["amount"])
    elif r["type"] == "AMEND":
        k = (r["filer_id"], r["period"])
        if k not in latest or r["amendment_seq"] > latest[k][0]:
            latest[k] = (r["amendment_seq"], r["deposit_date"], float(r["amount"]))
amend = sum(v[2] for v in latest.values() if a <= v[1] <= b)
cash = own + other + amend + refunds
recon = dict(liability=actual, own_periods_not_deposited=actual - own, earlier_periods_deposited=other,
             amendments=amend, refunds=refunds, cash=cash)

# --------------------------------------------------------------------------- the CSV deliverable
with open(G / "fy2026_lodging_reference_matches.csv", newline="", encoding="utf-8") as fh:
    out_rows = list(csv.DictReader(fh))
same(sorted((r["change_code"], r["filer_id"]) for r in out_rows),
     sorted((c, f) for c in ("CC", "LX", "AH") for f in dets[c]), "CSV covers every touched filer of CC, LX, AH")
bad = [r["filer_id"] for r in out_rows if abs(float(r["reference_taxable_receipts"]) - dets[r["change_code"]][r["filer_id"]][1]) > 0.01
       or abs(float(r["tax_effect"]) - dets[r["change_code"]][r["filer_id"]][2]) > 0.01
       or r["reference_filers"].split(";") != dets[r["change_code"]][r["filer_id"]][3]]
same(bad, [], "CSV rows that disagree with the recomputation")

# --------------------------------------------------------------------------- the deck states the same figures
with zipfile.ZipFile(G / "fy2026_lodging_tax_variance.pptx") as z:
    deck = " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8")) for n in sorted(z.namelist())
                    if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
    meta = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
    same([n for n in z.namelist() if "thumbnail" in n], [], "deck carries no stored thumbnail")
deck = re.sub(r"\s+", " ", deck)
k = lambda x: "{:,}".format(abs(int(round(x / 1000))))
for phrase in ("reduced fiscal 2026 lodging tax by $%s thousand" % k(eff["LX"]),
               "came in $%s thousand under the adopted forecast" % k(forecast - actual),
               "the closure itself accounts for $%s thousand" % k(eff["CC"]),
               "reproduced all 78 reference figures"):
    same(phrase in deck, True, "deck states '%s'" % phrase)
for code, label in (("LX", "Long-stay exemption"), ("CC", "Convention center closure"), ("AH", "Airline hub reduction")):
    same(re.search(re.escape(label) + r"\s*[-+]" + re.escape(k(eff[code])), deck) is not None, True,
         "deck table row %s" % code)
for label, key in (("Treasury collections, fiscal 2026", "cash"), ("Less refunds booked in fiscal 2026", "refunds"),
                   ("Plus earlier periods deposited in fiscal 2026", "earlier_periods_deposited"),
                   ("Less fiscal 2026 periods not deposited by June 30", "own_periods_not_deposited")):
    same(re.search(re.escape(label) + r"\s*[-+]?" + re.escape(k(recon[key])), deck) is not None, True,
         "deck cash row %s" % key)
SIG = (b"python-pptx", b"python-docx", b"openpyxl", b"ReportLab", b"reportlab", b"pypdf", b"matplotlib")
same([s.decode() for s in SIG if s in meta], [], "writer signature in the deck's properties")

# --------------------------------------------------------------------------- the write-up, once written
sub_path = TASK / "submission.md"
if sub_path.exists():
    sub = sub_path.read_text(encoding="utf-8")
    same("\u2014" in sub, False, "em dash in submission.md")
    for phrase in ("%s thousand" % k(eff["LX"]), "%s thousand" % k(eff["CC"]), "78 of 78"):
        same(phrase in sub, True, "submission states '%s'" % phrase)
    owed = {k(v) for v in eff.values()} | {k(forecast - actual), k(residual), k(forecast), k(actual)}
    owed |= {k(v) for v in recon.values()} | {"78"}
    head, csv_block = sub.split("### fy2026_lodging_reference_matches.csv")
    want_lines = set()
    for code in ("LX", "CC", "AH"):
        for fid, (act, ref, tax, peers) in dets[code].items():
            want_lines.add("   - %s, %s %s, %s to 2026-06: actual %s, reference %s, tax effect %s, reference filers %s" % (
                fid, code, reg[fid]["class"], EFF[code], "{:,.2f}".format(act), "{:,.2f}".format(ref),
                "{:,.2f}".format(tax), ", ".join(peers)))
    got_lines = {ln for ln in csv_block.splitlines() if ln.startswith("   - LT")}
    same(sorted(got_lines ^ want_lines)[:3], [], "submission CSV rows against the recomputation")
    body = re.sub(r"(?m)^\s*(#+\s*)?\d+\.\s", "", head)
    body = re.sub(r"[\w-]+\.(?:csv|pdf|xlsx|md|txt|pptx)|task500|fy20\d\d|FY20\d\d|20\d\d|K-\d+", "", body)
    nums = set(re.findall(r"\d{1,3}(?:,\d{3})+|\d+", body))
    same(sorted(n for n in nums - owed if len(n.replace(",", "")) > 2), [], "numbers in submission.md nothing recomputes")

# --------------------------------------------------------------------------- containers, registers, dates, the tree
shipped = sorted(p.name for p in T.iterdir() if p.is_file())
notes = (T / "extract_notes.txt").read_text(encoding="utf-8")
same([n for n in shipped if n != "extract_notes.txt" and n not in notes], [], "files the extract notes never register")
guide = (T / "lodging_extract_field_guide.md").read_text(encoding="utf-8")
same([n for n in shipped if n.endswith((".csv", ".xlsx")) and n not in guide], [], "data files the guide never describes")
later = [p.name for p in T.iterdir() if p.suffix in (".csv", ".txt", ".md")
         and any(x > "2026-08-14" for x in re.findall(r"20\d\d-\d\d-\d\d", p.read_text(encoding="utf-8")))]
same(later, [], "files dated after the extract")
tree = [p for p in TASK.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
same([str(p.relative_to(TASK)) for p in tree if p.suffix in (".md", ".py", ".txt", ".csv", ".json") and
      "\u2014" in p.read_text(encoding="utf-8", errors="ignore")], [], "em dashes in the build")

# --------------------------------------------------------------------------- the prompt
prompt = (TASK / "prompt.md").read_text(encoding="utf-8")
for leak in (r"long-stay", r"exemption", r"pattern", r"profile", r"seasonal", r"business travel", r"Appendix B",
             r"standing procedure", r"matched", r"comparable", r"nearest"):
    same(re.search(leak, prompt, re.I) is None, True, "prompt does not say '%s'" % leak)
same([n for n in shipped if n in prompt], [], "prompt names no input file")
deliverables = sorted(re.findall(r"\b[\w-]+\.(?:pptx|csv)\b", prompt))
same(sorted(p.name for p in G.iterdir() if p.is_file()), deliverables, "golden/ holds the deliverables")
for zname, folder, want in (("target.zip", T, shipped), ("golden.zip", G, deliverables)):
    zp = TASK / zname
    if not zp.exists():
        print("  %s not cut yet" % zname)
        continue
    with zipfile.ZipFile(zp) as z:
        mem = z.namelist()
        same(sorted(mem), want, "%s members" % zname)
        same([n for n in mem if z.read(n) != (folder / n).read_bytes()], [], "%s members differing from the tree" % zname)
    print("  %s  %d bytes  %d members  sha256 %s" % (zname, zp.stat().st_size, len(mem),
                                                    hashlib.sha256(zp.read_bytes()).hexdigest()[:16]))

if fails:
    print("\n".join(fails))
    sys.exit(1)
print("verify_pack: every graded figure reproduces from target/ (%d checks), house checks clean" % n_checks)
