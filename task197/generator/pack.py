"""Read the cut pack back as a solver would: the main population's monthly counts and each product's period sales."""
import csv, os, datetime as dt
from collections import defaultdict
import openpyxl
import analysis as an

CASES = "network/case_export_watched_products.csv"
POS_REV = "market/halcyon_pos_4wk_revised.csv"
POS_PRE = "market/halcyon_pos_4wk_preliminary.csv"
REGISTER = "register/watched_products_register.xlsx"


def read_register(tgt):
    wb = openpyxl.load_workbook(os.path.join(tgt, REGISTER), read_only=True)
    rows = list(wb["Watched products"].iter_rows(values_only=True))
    head = rows[0]
    prod = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        e = prod.setdefault(d["Product code"], dict(name=d["Product"], upcs=[], launch=d["First marketed"]))
        e["upcs"].append(d["UPC"])
    ch = list(wb["Packaging changes"].iter_rows(values_only=True))
    changes = {}
    for r in ch[1:]:
        d = dict(zip(ch[0], r))
        v = d["Changed pack first sold at retail"]
        changes[d["Product code"]] = v.date() if isinstance(v, dt.datetime) else v
    return prod, changes


def main_counts(tgt, codes):
    """Accidental under-six exposures per product code per calendar month of the recorded call (procedure 3)."""
    out = defaultdict(lambda: defaultdict(int))
    with open(os.path.join(tgt, CASES), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["reason"] != "Unintentional - general" or r["product_code"] not in codes:
                continue
            if int(r["patient_age_years"]) >= 6:
                continue
            d = r["call_received_local"][:10]
            k = int(d[:4]) * 12 + int(d[5:7]) - 1
            out[r["product_code"]][k] += 1
    return out


def period_sales(tgt, upcs_by_code):
    """Units per period per product: the revised history, the preliminary release for the periods it alone covers."""
    code_of = {}
    for code, upcs in upcs_by_code.items():
        for u in upcs:
            code_of[u] = code
    rev = defaultdict(lambda: defaultdict(int))
    pre = defaultdict(lambda: defaultdict(int))
    for path, store in ((POS_REV, rev), (POS_PRE, pre)):
        with open(os.path.join(tgt, path), newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                c = code_of.get(r["upc"])
                if c is None:
                    continue
                store[c][r["period_ending"]] += int(r["units"])
    out = {}
    for code in upcs_by_code:
        ends = dict(rev[code])
        for e, u in pre[code].items():
            ends.setdefault(e, u)
        lst = []
        for e in sorted(ends):
            b = dt.date.fromisoformat(e)
            a = b - dt.timedelta(days=27)
            lst.append((a, b, ends[e]))
        out[code] = lst
    return out


def series(tgt, day0):
    prod, changes = read_register(tgt)
    codes = set(prod)
    counts = main_counts(tgt, codes)
    sales = period_sales(tgt, {c: prod[c]["upcs"] for c in prod})
    res = {}
    last = max(b for c in sales for (_, b, _) in sales[c])
    nd = (last - day0).days + 1
    for c in prod:
        res[c] = an.Series(day0, nd, sales[c], counts[c])
    return prod, changes, res
