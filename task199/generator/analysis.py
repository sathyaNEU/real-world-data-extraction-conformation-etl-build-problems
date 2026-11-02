"""The golden's code path for task199 (architecture 2): reads only the shipped files under target/.

Every rung of the ladder, the call and every ask figure is computed here from the exports; nothing is imported
from world.py or params.py except the review-year dates, which the procedure itself files.
"""
import csv
import datetime as dt
import os
import re
from collections import defaultdict

YEAR_START = dt.date(2025, 10, 1)
YEAR_END = dt.date(2026, 9, 30)


# ---------------------------------------------------------------- readers
def _num(s):
    s = (s or "").strip().replace(",", "")
    return float(s) if s else 0.0


def read_rates(target):
    rates = defaultdict(dict)
    name = {"US DOLLAR": "USD", "EURO": "EUR", "STG POUND": "GBP"}
    with open(os.path.join(target, "cbk_indicative_rates_2025-09_2026-10.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
            rates[name[r["Currency"]]][d] = {"mean": float(r["Mean"]), "buy": float(r["Buy"]), "sell": float(r["Sell"])}
    return rates


def rate(rates, cur, d, basis="mean"):
    if cur == "KES":
        return 1.0
    s = rates[cur]
    k = d
    while k not in s:
        k -= dt.timedelta(days=1)
    return s[k][basis]


def read_statements(target):
    out = []
    with open(os.path.join(target, "tawi_core_legacy_stmt_2025-10_2026-03.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            amt = _num(r["CREDIT"]) - _num(r["DEBIT"])
            out.append(dict(cif=r["CIF"], acct=r["ACCOUNT_NO"], cur=r["CCY"],
                            booking=dt.datetime.strptime(r["TXN_DATE"], "%d/%m/%Y").date(),
                            value=dt.datetime.strptime(r["VALUE_DATE"], "%d/%m/%Y").date(), code=r["TRAN_CODE"],
                            ref=r["TXN_REF"], narr=r["NARRATION"], amount=amt, lcy=None, src="legacy"))
    with open(os.path.join(target, "tawi_t24_stmt_2026-04_2026-09.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cur = r["CURRENCY"]
            amt = float(r["AMOUNT.FCY"]) if cur != "KES" else float(r["AMOUNT.LCY"])
            out.append(dict(cif=r["CUSTOMER"], acct=r["ACCOUNT.NUMBER"], cur=cur,
                            booking=dt.datetime.strptime(r["BOOKING.DATE"], "%Y%m%d").date(),
                            value=dt.datetime.strptime(r["VALUE.DATE"], "%Y%m%d").date(), code=r["TRANSACTION.CODE"],
                            ref=r["OUR.REFERENCE"], their=r["THEIR.REFERENCE"], narr=r["NARRATIVE"], amount=amt,
                            lcy=float(r["AMOUNT.LCY"]), src="t24"))
    return out


def read_conversion(target):
    m = {}
    with open(os.path.join(target, "t24_account_conversion_20260401.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m[r["LEGACY.ACCOUNT"]] = (r["T24.ACCOUNT"], r["CUSTOMER"], r["CURRENCY"])
    return m


def parse_mt103(path):
    msgs = []
    text = open(path, encoding="ascii").read()
    for blk in [b for b in text.split("\n\n") if b.strip()]:
        lines = blk.splitlines()
        fields, cur = {}, None
        for ln in lines[1:]:
            mt = re.match(r"^:(\w+):(.*)$", ln)
            if mt:
                cur = mt.group(1)
                fields[cur] = [mt.group(2)]
            elif ln.startswith("-}"):
                cur = None
            elif cur:
                fields[cur].append(ln)
        v = fields["32A"][0]
        d = dt.datetime.strptime(v[:6], "%y%m%d").date()
        ccy = v[6:9]
        amt = float(v[9:].replace(",", "."))
        ins = fields.get("33B", [v[6:]])[0]
        msg = dict(ref=fields["20"][0], value=d, cur=ccy, amount=amt, instructed=float(ins[3:].replace(",", ".")),
                   ordering=fields["50K"], beneficiary=fields["59"], remit=" ".join(fields.get("70", [""])),
                   charges=float(fields["71F"][0][3:].replace(",", ".")) if "71F" in fields else 0.0)
        msg["ordering_acct"] = msg["ordering"][0].lstrip("/")
        msg["ordering_name"] = msg["ordering"][1] if len(msg["ordering"]) > 1 else ""
        msg["bene_acct"] = msg["beneficiary"][0].lstrip("/")
        msg["bene_name"] = msg["beneficiary"][1] if len(msg["beneficiary"]) > 1 else ""
        msgs.append(msg)
    return msgs


def read_register(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "edd_register_profiles_2026.xlsx"), read_only=True, data_only=True)
    reg = {}
    for row in wb["Register"].iter_rows(min_row=5, values_only=True):
        if row and row[0]:
            reg[str(row[0])] = dict(name=row[1], sector=row[2])
    for row in wb["Profiles"].iter_rows(min_row=4, values_only=True):
        if row and row[0]:
            cif = str(row[0])
            reg[cif]["expected"] = float(row[1])
            other = str(row[4] or "")
            reg[cif]["elsewhere"] = re.findall(r"\b\d{9,14}\b", other)
    return reg


# ---------------------------------------------------------------- the call
def credits_kes(stmts, rates, basis="mean", use_lcy=False, by="value"):
    """Credits within the review year with their shilling value (procedure 3.1 and 3.2)."""
    out = []
    for p in stmts:
        d = p[by]
        if p["amount"] <= 0 or not (YEAR_START <= d <= YEAR_END):
            continue
        if use_lcy and p["lcy"] is not None:
            kes = p["lcy"]
        else:
            kes = p["amount"] * rate(rates, p["cur"], p["value"] if by == "value" else d, basis)
        q = dict(p)
        q["kes"] = kes
        out.append(q)
    return out


def own_transfer_refs(stmts):
    """Refs that appear as a debit on one account and a credit on another account of the same customer."""
    legs = defaultdict(list)
    for p in stmts:
        if p["ref"]:
            legs[(p["cif"], p["ref"])].append(p)
    own = set()
    for (cif, ref), ps in legs.items():
        if any(x["amount"] < 0 for x in ps) and any(x["amount"] > 0 for x in ps) and \
                len({x["acct"] for x in ps}) > 1:
            own.add((cif, ref))
    return own


def declared_elsewhere(credit, reg):
    accs = reg.get(credit["cif"], {}).get("elsewhere", [])
    return any(a in credit["narr"] for a in accs)


def visible_return(credit, in_by_ref):
    n = credit["narr"].upper()
    if "RETURN" in n or "REFUND" in n:
        return True
    ref = credit.get("their") or credit["ref"]
    m = in_by_ref.get(ref)
    return bool(m and "/RETN/" in m["remit"])


def business_days_between(a, b, holidays):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in holidays:
            n += 1
    return n


def acct_owner(stmts, conv):
    owner = {}
    for p in stmts:
        owner[p["acct"]] = p["cif"]
    for leg, (new, cif, cur) in conv.items():
        owner[leg] = cif
        owner[new] = cif
    return owner


def pair_returns(swift_out, swift_in, owner, max_bd=10, tol=200.0, holidays=frozenset(), min_lag=1):
    """An inward credit that returns an outward payment of the same customer: same currency, credited within
    max_bd business days after it, short of the outward amount by no more than tol (charges taken on the way)."""
    lo = min([m["value"] for m in swift_out + swift_in]) - dt.timedelta(days=10)
    hi = max([m["value"] for m in swift_out + swift_in]) + dt.timedelta(days=10)
    idx, k, d = {}, 0, lo
    while d <= hi:
        if d.weekday() < 5 and d not in holidays:
            k += 1
        idx[d] = k
        d += dt.timedelta(days=1)
    by_key = defaultdict(list)
    for o in swift_out:
        by_key[(owner.get(o["ordering_acct"]), o["cur"])].append(o)
    pairs, used = {}, set()
    for m in sorted(swift_in, key=lambda x: (x["value"], x["ref"])):
        key = (owner.get(m["bene_acct"]), m["cur"])
        best = None
        for o in by_key.get(key, []):
            if o["ref"] in used or o["value"] > m["value"]:
                continue
            lag = idx[m["value"]] - idx[o["value"]]
            gap = o["amount"] - m["amount"]
            if min_lag <= lag <= max_bd and 0 <= gap <= tol:
                if best is None or gap < best[0]:
                    best = (gap, o)
        if best:
            pairs[m["ref"]] = best[1]["ref"]
            used.add(best[1]["ref"])
    return pairs


_CACHE = {}


def load(target):
    key = os.path.abspath(target)
    if key not in _CACHE:
        _CACHE[key] = dict(stmts=read_statements(target), rates=read_rates(target), reg=read_register(target),
                           conv=read_conversion(target),
                           out=parse_mt103(os.path.join(target, "swift_mt103_outward_fy2026.txt")),
                           inn=parse_mt103(os.path.join(target, "swift_mt103_inward_fy2026.txt")))
    return _CACHE[key]


def third_party(target, basis="mean", use_lcy=False, by="value", max_bd=10, tol=200.0, rung=3, holidays=None):
    L = load(target)
    stmts, rates, reg, conv, out_msgs, in_msgs = L["stmts"], L["rates"], L["reg"], L["conv"], L["out"], L["inn"]
    in_by_ref = {m["ref"]: m for m in in_msgs}
    owner = acct_owner(stmts, conv)
    hol = holidays if holidays is not None else kenya_holidays(rates)
    own = own_transfer_refs(stmts)
    pairs = pair_returns(out_msgs, in_msgs, owner, max_bd, tol, hol) if rung >= 3 else {}
    cr = credits_kes(stmts, rates, basis, use_lcy, by)
    tot = defaultdict(lambda: defaultdict(float))
    for p in cr:
        cif = p["cif"]
        ref_in = p.get("their") or p["ref"]
        cls = "tp"
        if rung >= 1 and (cif, p["ref"]) in own:
            cls = "own_internal"
        elif rung >= 1 and p["code"] in ("RVC", "109"):
            cls = "reversal"
        elif rung >= 2 and declared_elsewhere(p, reg):
            cls = "own_external"
        elif rung >= 2 and visible_return(p, in_by_ref):
            cls = "return"
        elif rung >= 3 and ref_in in pairs:
            cls = "uturn"
        tot[cif][cls] += p["kes"]
        tot[cif]["gross"] += p["kes"]
    res = {}
    for cif, info in reg.items():
        t = tot[cif]
        tp = t["tp"]
        e = info["expected"]
        res[cif] = dict(name=info["name"], expected=e, tp=tp, ratio=tp / e, dev=max(tp / e, e / tp), parts=dict(t))
    return res, dict(pairs=pairs, own=own)


def kenya_holidays(rates):
    """Weekdays on which the CBK published no rate are the bank holidays of the span."""
    days = set(rates["USD"].keys())
    lo, hi = min(days), max(days)
    hol, d = set(), lo
    while d <= hi:
        if d.weekday() < 5 and d not in days:
            hol.add(d)
        d += dt.timedelta(days=1)
    return frozenset(hol)


def call(res):
    order = sorted(res.items(), key=lambda kv: -kv[1]["dev"])
    return order


# ---------------------------------------------------------------- ask A: large cash withdrawals
def ask_cash(target, basis="mean", aggregate=True, net_reversals=True, by_customer=True):
    stmts = read_statements(target)
    conv = read_conversion(target)
    owner = acct_owner(stmts, conv)
    rates = read_rates(target)
    rows = []
    with open(os.path.join(target, "teller_cash_txn_2025-10_2026-09.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    reversed_refs = {r["ORIG_REF"] for r in rows if r["TXN_TYPE"] == "REVERSAL" and r["ORIG_REF"]}
    day = defaultdict(float)
    for r in rows:
        if r["TXN_TYPE"] not in ("CWDL", "CHQ_ENCASH"):
            continue
        if net_reversals and r["TXN_REF"] in reversed_refs:
            continue
        d = dt.datetime.strptime(r["TXN_TIMESTAMP"], "%Y-%m-%d %H:%M:%S").date()
        if not (YEAR_START <= d <= YEAR_END):
            continue
        key = owner.get(r["ACCOUNT"], "?") if by_customer else r["ACCOUNT"]
        if aggregate:
            day[(key, d)] += float(r["AMOUNT_KES"])
        else:
            day[(key, d, r["TXN_REF"])] += float(r["AMOUNT_KES"])
    out = defaultdict(lambda: [0, 0.0])
    for k, amt in day.items():
        cif_or_acct, d = k[0], k[1]
        thr = 10_000 * rate(rates, "USD", d, basis)
        if amt >= thr:
            cif = cif_or_acct if by_customer else owner.get(cif_or_acct, "?")
            out[cif][0] += 1
            out[cif][1] += amt
    return {k: (v[0], v[1]) for k, v in out.items()}


# ---------------------------------------------------------------- ask B: September 2026 salaries
def ask_salary(target, by_period=True, distinct=True, include_casual=False):
    """Salaries for the September 2026 payroll period: the period sits in the batch reference (SAL-cccc-YYMM-nnn)."""
    stmts = read_statements(target)
    conv = read_conversion(target)
    owner = acct_owner(stmts, conv)
    people = defaultdict(set)
    total = defaultdict(float)
    with open(os.path.join(target, "bulk_salary_uploads_2026-07_2026-10.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ref = r["BATCH_REF"]
            vd = dt.date.fromisoformat(r["VALUE_DATE"])
            casual = ref.startswith("CAS-")
            if casual and not include_casual:
                continue
            if by_period:
                mt = re.match(r"^SAL-\d{4}-(\d{2})(\d{2})-", ref)
                if not casual and not (mt and (mt.group(1), mt.group(2)) == ("26", "09")):
                    continue
                if casual and not (dt.date(2026, 9, 1) <= vd <= dt.date(2026, 9, 30)):
                    continue
            else:
                if not (dt.date(2026, 9, 1) <= vd <= dt.date(2026, 9, 30)):
                    continue
            cif = owner.get(r["DEBIT_ACCOUNT"], "?")
            key = r["PAYEE_ID_NO"] if distinct else (r["PAYEE_ID_NO"], r["BATCH_REF"], r["PAYEE_NAME"])
            people[cif].add(key)
            total[cif] += float(r["AMOUNT_KES"])
    return {cif: (len(people[cif]), total[cif]) for cif in people}


# ---------------------------------------------------------------- ask C: VAT paid by tax period
def ask_vat(target, by_period=True, first=(2025, 10), last=(2026, 8)):
    pin2cif = {}
    with open(os.path.join(target, "customer_master_extract_20261016.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pin2cif[r["KRA_PIN"].replace(" ", "").upper()] = r["CIF"]
    out = defaultdict(float)
    with open(os.path.join(target, "kra_gateway_payments_2025-09_2026-10.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["TAX_HEAD"] != "VAT":
                continue
            cif = pin2cif.get(r["TAXPAYER_PIN"].replace(" ", "").upper(), "?")
            if by_period:
                p = dt.date.fromisoformat(r["TAX_PERIOD_FROM"])
                if not ((first[0], first[1]) <= (p.year, p.month) <= (last[0], last[1])):
                    continue
            else:
                pd_ = dt.date.fromisoformat(r["PAYMENT_DATE"])
                if not (YEAR_START <= pd_ <= YEAR_END):
                    continue
            out[cif] += float(r["AMOUNT_PAID"])
    return dict(out)


def figures(target):
    res, aux = third_party(target)
    order = call(res)
    first, second = order[0], order[1]
    cash = ask_cash(target)
    sal = ask_salary(target)
    vat = ask_vat(target)
    return dict(res=res, order=order, first=first, second=second, cash=cash, sal=sal, vat=vat, aux=aux)
