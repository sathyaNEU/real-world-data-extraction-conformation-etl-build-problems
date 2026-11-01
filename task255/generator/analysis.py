"""Every rung and every graded figure, computed from the shipped files under target/ alone."""
import collections
import datetime as dt
import os
import re
import statistics

import io_util as IO

FILES = {
    "dispensings": "statin_dispensings_202407_202612.csv",
    "products": "statin_products.csv",
    "ddd": "atc_ddd_2026.xlsx",
    "practices": "practice_register_2026.xlsx",
    "pharmacies": "pharmacies.csv",
    "programme": "statin_followup_programme_2027.pdf",
    "agreement": "pharmacy_pilot_agreement_2026.pdf",
    "conversations": "pilot_conversations_2026.xlsx",
    "statements": "pilot_statements_2026.pdf",
}
WINDOW = (dt.date(2025, 7, 1), dt.date(2025, 12, 31))
LOOKBACK, HORIZON, GRACE, LINE = 365, 365, 30, 60.0
_CACHE = {}


def p(target, key):
    return os.path.join(target, FILES[key])


def parse_date(s):
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", s):
        return dt.datetime.strptime(s, "%d-%m-%Y").date()
    return dt.date.fromisoformat(s)


def load(target):
    if target in _CACHE:
        return _CACHE[target]
    h, rows = IO.read_csv(p(target, "products"))
    prods = {r[0]: {"name": r[1], "atc": r[2], "mg": float(r[3].split()[0]), "pack": int(r[4])} for r in rows}
    h, rows = IO.read_xlsx(p(target, "ddd"), "DDD")
    ddd = {r[0]: float(r[2]) for r in rows if r[0]}
    h, rows = IO.read_xlsx(p(target, "practices"), "Practices")
    practices = {str(r[0]): r[1] for r in rows if r[0]}
    h, rows = IO.read_csv(p(target, "dispensings"))
    idx = {k: i for i, k in enumerate(h)}
    disp = collections.defaultdict(list)
    meta = {}
    for r in rows:
        pid = r[idx["pseudonym"]]
        pr = prods[r[idx["product_number"]]]
        disp[pid].append({"date": parse_date(r[idx["dispensing_date"]]), "tablets": int(r[idx["packs"]]) * pr["pack"],
                          "atc": pr["atc"], "mg": pr["mg"], "prescriber": r[idx["prescriber_id"]],
                          "pharmacy": r[idx["pharmacy_id"]], "product": r[idx["product_number"]]})
        meta[pid] = (r[idx["sex"]], r[idx["birth_date"]])
    for v in disp.values():
        v.sort(key=lambda x: (x["date"], x["product"]))
    _CACHE[target] = {"prods": prods, "ddd": ddd, "practices": practices, "disp": disp, "meta": meta}
    return _CACHE[target]


def cohort(target):
    """New statin users of the second half of 2025 by the practice that prescribed their first dispensing."""
    D = load(target)
    out = []
    for pid, ds in D["disp"].items():
        firsts = [d for d in ds if WINDOW[0] <= d["date"] <= WINDOW[1]]
        if not firsts:
            continue
        f = firsts[0]
        if any(0 < (f["date"] - d["date"]).days <= LOOKBACK for d in ds if d["date"] < f["date"]):
            continue
        if not re.fullmatch(r"\d{6}", f["prescriber"]) or f["prescriber"] not in D["practices"]:
            continue
        out.append((pid, f["prescriber"], f["date"]))
    return out


# ---------------------------------------------------------------- the patient's own daily dose
def rate_overall(ds, start=None):
    """Tablets dispensed before the last dispensing over the days from the first to the last."""
    if start is not None:
        ds = [d for d in ds if (d["date"] - start).days < HORIZON]
    if len(ds) < 2:
        return None
    days = (ds[-1]["date"] - ds[0]["date"]).days
    return sum(d["tablets"] for d in ds[:-1]) / days if days > 0 else None


def rate_median(ds):
    rs = [a["tablets"] / (b["date"] - a["date"]).days for a, b in zip(ds, ds[1:]) if (b["date"] - a["date"]).days > 0]
    return statistics.median(rs) if rs else None


def rate_recent(ds):
    rs = [a["tablets"] / (b["date"] - a["date"]).days for a, b in zip(ds, ds[1:]) if (b["date"] - a["date"]).days > 0]
    return sum(rs[-3:]) / len(rs[-3:]) if rs else None


def rate_snapped(ds):
    r = rate_median(ds)
    if r is None:
        return None
    return min((0.5, 1.0, 2.0, 4.0), key=lambda s: abs(s - r) / s)


def persistent(ds, start, rate):
    """No more than 30 days in a row without tablets in the 365 days from start: each dispensing's tablets last
    tablets / rate days, taken after the tablets still in hand."""
    stock_end = 0.0
    for d in ds:
        x = (d["date"] - start).days
        if x < 0:
            continue
        if x >= HORIZON:
            break
        if x - stock_end > GRACE:
            return False
        stock_end = max(stock_end, x) + d["tablets"] / rate
    return HORIZON - stock_end <= GRACE


class Call:
    pass


def main_call(target, rule="own"):
    """rule: 'own' (each patient's own daily dose from their dispensings, the golden), 'own_median', 'own_recent',
    'own_horizon', 'own_snapped' (the same dose read other ways), 'one_a_day' (one tablet a day), 'ddd' (the WHO
    defined daily dose), 'product_rate' (the usual rate of the patient's product among all patients)."""
    D = load(target)
    C = Call()
    C.cohort = cohort(target)
    prod_rates = None
    if rule == "product_rate":
        acc = collections.defaultdict(list)
        for pid, ds in D["disp"].items():
            r = rate_overall(ds)
            if r:
                acc[(ds[0]["atc"], ds[0]["mg"])].append(r)
        prod_rates = {k: statistics.median(v) for k, v in acc.items()}
    n = collections.Counter()
    k = collections.Counter()
    C.status = {}
    for pid, practice, start in C.cohort:
        ds = [d for d in D["disp"][pid] if d["date"] >= start]
        first = ds[0]
        ddd_rate = D["ddd"][first["atc"]] / first["mg"]
        if rule == "one_a_day":
            rate = 1.0
        elif rule == "ddd":
            rate = ddd_rate
        elif rule == "product_rate":
            rate = prod_rates.get((first["atc"], first["mg"]), 1.0)
        else:
            est = {"own": rate_overall(ds), "own_median": rate_median(ds), "own_recent": rate_recent(ds),
                   "own_horizon": rate_overall(ds, start), "own_snapped": rate_snapped(ds)}[rule]
            # one dispensing shows no rhythm: at any dose from half a tablet a day it runs out long before the year
            rate = est if est else 1.0
        ok = persistent(ds, start, rate)
        C.status[pid] = ok
        n[practice] += 1
        k[practice] += ok
    C.n, C.k = n, k
    C.share = {pr: 100.0 * k[pr] / n[pr] for pr in n}
    C.names = D["practices"]
    C.joins = sorted(pr for pr, v in C.share.items() if v < LINE)
    return C


# ---------------------------------------------------------------- ask: the pilot payment due to each pharmacy
def load_conversations(target):
    h, rows = IO.read_xlsx(p(target, "conversations"), "Conversations")
    out = []
    for r in rows:
        if r[0]:
            out.append({"no": r[0], "pharmacy": r[1], "date": dt.date.fromisoformat(str(r[2])[:10]), "status": r[3],
                        "cancelled": dt.date.fromisoformat(str(r[4])[:10]) if r[4] else None})
    return out


def load_statements(target):
    txt = IO.pdf_text(p(target, "statements"))
    out = []
    for m in re.finditer(r"\((A\d{3})\)\s+(\d{2})\.(\d{2})\.(\d{4})\s+([\d.]+,\d{2})", txt):
        amount = float(m.group(5).replace(".", "").replace(",", "."))
        out.append({"pharmacy": m.group(1), "date": dt.date(int(m.group(4)), int(m.group(3)), int(m.group(2))),
                     "amount": amount})
    return out


def quarter_start(d):
    return dt.date(d.year, 3 * ((d.month - 1) // 3) + 1, 1)


def pilot_payments(target, mode="rate"):
    """mode: 'rate' (each pharmacy's rate, recovered from its statements over the conversations they covered, times the
    conversations held and never cancelled; the golden), 'statements' (the four statements added up)."""
    convs = load_conversations(target)
    stm = load_statements(target)
    out = {}
    for ph in sorted({s["pharmacy"] for s in stm}):
        ss = [s for s in stm if s["pharmacy"] == ph]
        if mode == "statements":
            out[ph] = sum(s["amount"] for s in ss)
            continue
        rates = set()
        for s in ss:
            q0 = quarter_start(s["date"])
            cnt = sum(1 for c in convs if c["pharmacy"] == ph and q0 <= c["date"] <= s["date"] and
                      (c["cancelled"] is None or c["cancelled"] > s["date"]))
            if cnt:
                rates.add(round(s["amount"] / cnt, 6))
        rate = sorted(rates)[0]
        out[ph] = rate * sum(1 for c in convs if c["pharmacy"] == ph and c["cancelled"] is None)
        out[ph + ":rates"] = sorted(rates)
    return out


# ---------------------------------------------------------------- ask: continuing statin users of 2026, each person once
def continuing_users(target, mode="persons"):
    """mode: 'persons' (a pseudonym that stops and one that starts the same person: same birth date and sex, same
    practice and product line, the second beginning after the first ends; the golden), 'pseudonyms'."""
    D = load(target)
    groups = {pid: pid for pid in D["disp"]}
    if mode == "persons":
        by_key = collections.defaultdict(list)
        for pid, ds in D["disp"].items():
            by_key[D["meta"][pid]].append(pid)
        for key, pids in by_key.items():
            if len(pids) != 2:
                continue
            a, b = sorted(pids, key=lambda x: D["disp"][x][0]["date"])
            da, db = D["disp"][a], D["disp"][b]
            if da[-1]["date"] < db[0]["date"] and (da[-1]["atc"], da[-1]["mg"]) == (db[0]["atc"], db[0]["mg"]) and \
                    da[-1]["prescriber"] == db[0]["prescriber"]:
                groups[b] = a
    persons = collections.defaultdict(list)
    for pid, ds in D["disp"].items():
        persons[groups[pid]] += ds
    out = collections.Counter()
    for person, ds in persons.items():
        d26 = sorted((d for d in ds if d["date"].year == 2026), key=lambda d: d["date"])
        if {(d["date"].month - 1) // 3 for d in d26} != {0, 1, 2, 3}:
            continue
        practice = d26[-1]["prescriber"]
        if practice in D["practices"]:
            out[practice] += 1
    return {pr: out.get(pr, 0) for pr in D["practices"]}
