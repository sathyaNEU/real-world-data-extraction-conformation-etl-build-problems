"""task211 pair ceiling, measured on the cut pack (target/) with code that shares nothing with the generator.

The cracker lands the call and then works every ask the careful way: it runs the hygiene battery (exact and near
duplicates, a repeated total on every line, key normalisation, a per-chain latest-version rule, the current code list,
gaps checked against every control it can match). The mirror misses the call and stops at the natural read of each
ask. Each ask figure is scored a hit when it falls in the golden's bin at the stated rounding. Prints every figure,
the keeps and the pair arithmetic (C = 38 + 7 + 55 Lc on the call, S = 5 + 7 + 55 Ls off it).
Run: python3 task211/generator/ceiling.py"""
import csv, json, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = json.load(open(os.path.join(HERE, "figures.json")))


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def season(datestr, first_month=10):
    y, m = int(datestr[:4]), int(datestr[5:7])
    s = y if m >= first_month else y - 1
    return "%d/%02d" % (s, (s + 1) % 100)


def hit(v, g, unit):
    return round(v / unit) == round(g / unit)


# ---------------------------------------------------------------- ask 1: developer statements
st = rows("developer_standby_statements.csv")


def a1(latest_chain, redate):
    revised = {r["their_ref"][5:] for r in st if r["their_ref"].startswith("Rev. ")}
    out = defaultdict(float)
    for r in st:
        if latest_chain and r["statement_no"] in revised:
            continue
        out["%s|%s" % (r["developer"], season(r["period"] + "-01", 11))] += float(r["days"])
    return out


# ---------------------------------------------------------------- ask 2: the jack-up's shift reports
js = json.load(open(os.path.join(T, "atlas_shift_reports.json")))["shifts"]
codes = {r["code"]: r for r in rows("atlas_activity_codes.csv")}
hire_txt = open(os.path.join(T, "atlas_final_hire_statement.pdf"), "rb").read()


def a2(fill_gap):
    out = defaultdict(float)
    for x in js:
        k = season(x["date"], 11)
        for c, h in x["hours"].items():
            # the current list's weather code, and the retired WW read as waiting on weather
            if c == "WX" or (c == "WW" and c not in codes):
                out[k] += h
    if fill_gap:
        # the control it can match: the owner's reduced-rate hours for 15 Jan to 15 Feb 2026 against the reports
        hrs = 286.0   # read off the statement by eye; recomputed below when the text layer is readable
        m = re.findall(rb"weather standby\)?\s*Tj.*?\((\d+)\)", hire_txt, re.S)
        reported = sum(x["hours"].get("WX", 0) for x in js if "2026-01-15" <= x["date"] <= "2026-02-15")
        stated = HIRE_HOURS
        out["2025/26"] += max(0.0, stated - reported)
    return out


HIRE_HOURS = None
try:
    from pypdf import PdfReader
    txt = "".join(p.extract_text() for p in PdfReader(os.path.join(T, "atlas_final_hire_statement.pdf")).pages)
    m = re.search(r"reduced rate, weather standby\s+(\d+)", txt)
    HIRE_HOURS = float(m.group(1)) if m else None
except Exception:
    HIRE_HOURS = None

# ---------------------------------------------------------------- ask 3: port charges
ap = rows("ap_port_charges_2023_2026.csv")


def portkey(r):
    return "%s|%s" % ("Tranevig" if r["vendor"].startswith("Tranevig") else "Hjortby Havn", season(r["invoice_date"], 10))


def a3(careful):
    out = defaultdict(float)
    if not careful:
        for r in ap:
            out[portkey(r)] += float(r["amount_eur"])
        return out
    # Tranevig: a repeated total on every weekly line, counted once per run of consecutive weeks
    trv = sorted([r for r in ap if r["vendor"].startswith("Tranevig")], key=lambda r: (r["vessel"], r["invoice_date"]))
    last = {}
    for r in trv:
        prev = last.get(r["vessel"])
        week = int(r["invoice_date"].replace("-", ""))
        if prev and prev[1] == r["amount_eur"] and 0 < _days(prev[0], r["invoice_date"]) <= 7:
            last[r["vessel"]] = (r["invoice_date"], r["amount_eur"])
            continue
        last[r["vessel"]] = (r["invoice_date"], r["amount_eur"])
        out[portkey(r)] += float(r["amount_eur"])
    # Hjortby: invoice numbers normalised, one invoice per number and date
    seen = set()
    for r in ap:
        if r["vendor"].startswith("Hjortby"):
            k = (r["invoice_no"].lstrip("0"), r["invoice_date"])
            if k in seen:
                continue
            seen.add(k)
            out[portkey(r)] += float(r["amount_eur"])
    return out


def _days(a, b):
    import datetime as dt
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


# ---------------------------------------------------------------- scoring
asks = [("ask 1 statements", GOLD["ask_statements_days"], 0.01, a1(True, False), a1(False, False)),
        ("ask 2 jack-up standby", GOLD["ask_atlas_weather_standby_hours"], 1, a2(True), a2(False)),
        ("ask 3 port dues", GOLD["ask_port_dues_eur"], 10, a3(True), a3(False))]
tot = kc = km = 0
print("%-34s %-14s %-14s %-14s %s" % ("figure", "golden", "cracker", "mirror", "hits"))
per = []
for name, g, unit, cr, mi in asks:
    hc = hm = 0
    for k, v in g.items():
        c = cr.get(k, 0.0); m = mi.get(k, 0.0)
        h1, h2 = hit(c, v, unit), hit(m, v, unit)
        hc += h1; hm += h2
        print("%-34s %-14.2f %-14.2f %-14.2f %s%s" % (k[:34], v, c, m, "C" if h1 else "-", "M" if h2 else "-"))
    per.append((name, len(g), hc, hm))
    tot += len(g); kc += hc; km += hm
Lc, Lm = kc / tot, km / tot
C = 38 + 7 + 55 * Lc
Sx = 5 + 7 + 55 * Lm
print()
for name, n, hc, hm in per:
    print("%-24s figures %2d  cracker keeps %2d  mirror keeps %2d  cracker %s" % (name, n, hc, hm, "miss" if hc < n / 2 else "KEEPS"))
print("full includer (cracker) keeps %d of %d ask figures (%.1f%%); mirror keeps %d (%.1f%%)" % (kc, tot, 100 * Lc, km, 100 * Lm))
print("pair ceiling, one on the call and one off: (%.1f + %.1f) / 2 = %.1f" % (C, Sx, (C + Sx) / 2))
print("pair with both on the call: %.1f" % C)
sys.exit(0)
