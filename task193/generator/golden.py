"""Everything the write-up states, computed from the files the pack ships and nothing else."""
import collections
import csv
import datetime as dt
import os
import statistics

import world as W

D = dt.date.fromisoformat


def rd(tgt, name):
    with open(os.path.join(tgt, name), newline="") as f:
        return list(csv.DictReader(f))


def load(tgt):
    """the quarter as the standard's paragraphs 2.1 to 2.4 define it"""
    master = {r["submission_id"]: r for r in rd(tgt, "report_master.csv")}
    extract = rd(tgt, "spontaneous_reports_extract.csv")
    reg = rd(tgt, "product_register.csv")
    dic = rd(tgt, "reaction_dictionary.csv")
    listed = collections.defaultdict(set)
    for r in rd(tgt, "product_information_listed.csv"):
        listed[r["product_code"]].add(r["preferred_term"])

    # a product name, as reported, resolves to one code whichever name was in force
    code_of = {}
    for r in reg:
        code_of[r["product_name"]] = r["product_code"]
        if r["former_name"]:
            code_of[r["former_name"]] = r["product_code"]
    # the dictionary at the version the case was coded at
    pref = {(r["reaction_verbatim"], r["dictionary_version"]): r["preferred_term"] for r in dic}
    serious = {(r["reaction_verbatim"], r["dictionary_version"]): r["serious"] == "yes" for r in dic}

    cases = {}
    for row in extract:
        m = master[row["submission_id"]]
        if not (W.Q_FROM <= D(m["receipt_date"]) <= W.Q_TO):
            continue
        key = row["case_id"]
        c = cases.get(key)
        if c is None:
            c = cases[key] = {"code": code_of[row["product_reported"]], "reactions": set(),
                              "serious": set(), "receipt": D(m["receipt_date"]),
                              "channel": m["channel"], "reporter": m["reporter_type"],
                              "region": m["region"], "age": m["age_band"], "sex": m["sex"]}
        elif D(m["receipt_date"]) < c["receipt"]:
            c["receipt"] = D(m["receipt_date"])
            c["channel"] = m["channel"]
        t = pref[(row["reaction_verbatim"], row["dictionary_version"])]
        c["reactions"].add(t)
        if serious[(row["reaction_verbatim"], row["dictionary_version"])]:
            c["serious"].add(t)
    return list(cases.values()), listed


def tally(cases):
    npr, a = collections.Counter(), collections.Counter()
    for c in cases:
        npr[c["code"]] += 1
        for r in c["reactions"]:
            a[(c["code"], r)] += 1
    return npr, a


def measure(npr, a, code, reaction, drop=()):
    aa = a.get((code, reaction), 0)
    np_ = npr.get(code, 0)
    if aa == 0 or np_ == 0:
        return None, None
    bb = np_ - aa
    cc = dd = 0
    for q, n in npr.items():
        if q == code or q in drop:
            continue
        x = a.get((q, reaction), 0)
        cc += x
        dd += n - x
    if cc == 0:
        return None, None
    prr = (aa / np_) / (cc / (cc + dd))
    tot = aa + bb + cc + dd
    e = [(aa + bb) * (aa + cc) / tot, (aa + bb) * (bb + dd) / tot,
         (cc + dd) * (aa + cc) / tot, (cc + dd) * (bb + dd) / tot]
    chi = sum((o - x) ** 2 / x for o, x in zip((aa, bb, cc, dd), e))
    return prr, chi


def odds(npr, a, code, reaction, drop=()):
    aa = a.get((code, reaction), 0)
    np_ = npr.get(code, 0)
    bb = np_ - aa
    cc = dd = 0
    for q, n in npr.items():
        if q == code or q in drop:
            continue
        x = a.get((q, reaction), 0)
        cc += x
        dd += n - x
    if 0 in (aa, bb, cc, dd):
        return None
    return (aa / bb) / (cc / dd)


def run(npr, a, listed, drop=(), stat="prr"):
    out = []
    for (code, reaction), aa in sorted(a.items()):
        if aa < W.N_MIN or reaction in listed.get(code, ()):
            continue
        dr = tuple(q for q in drop if q != code)
        prr, chi = measure(npr, a, code, reaction, dr)
        if prr is None:
            continue
        v = prr if stat == "prr" else odds(npr, a, code, reaction, dr)
        if v is None:
            continue
        if v >= W.PRR_MIN and chi >= W.CHI_MIN:
            out.append({"code": code, "reaction": reaction, "reports": aa,
                        "prr": prr, "chi": chi, "ror": odds(npr, a, code, reaction, dr)})
    out.sort(key=lambda x: (-x["reports"], x["code"], x["reaction"]))
    return out


def stratified(npr, a, cases, listed, strat):
    """the ratio the standard names, pooled over a report attribute, weighted by the product's reports"""
    keys = sorted(set(c[strat] for c in cases))
    lay = {k: {"n": collections.Counter(), "a": collections.Counter()} for k in keys}
    for c in cases:
        L = lay[c[strat]]
        L["n"][c["code"]] += 1
        for r in c["reactions"]:
            L["a"][(c["code"], r)] += 1
    out = set()
    for (code, reaction), aa in a.items():
        if aa < W.N_MIN or reaction in listed.get(code, ()):
            continue
        num = den = 0.0
        for k in keys:
            L = lay[k]
            A = L["a"][(code, reaction)]
            NP = L["n"][code]
            C = sum(v for (q, rr), v in L["a"].items() if rr == reaction and q != code)
            ND = sum(v for q, v in L["n"].items() if q != code)
            if NP == 0 or ND == 0 or C == 0:
                continue
            num += NP * (A / NP) / (C / ND)
            den += NP
        if den == 0:
            continue
        _, chi = measure(npr, a, code, reaction)
        if num / den >= W.PRR_MIN and chi and chi >= W.CHI_MIN:
            out.add((code, reaction))
    return out


def raw_run(tgt, listed):
    """the run on the extract as it stands: a submission taken for a report, the verbatim term taken
    for the reaction, the product taken at the name reported, the window read on the report date"""
    master = {r["submission_id"]: r for r in rd(tgt, "report_master.csv")}
    npr, a = collections.Counter(), collections.Counter()
    seen = collections.defaultdict(set)
    for row in rd(tgt, "spontaneous_reports_extract.csv"):
        m = master[row["submission_id"]]
        if not (W.Q_FROM <= D(m["report_date"]) <= W.Q_TO):
            continue
        key = row["submission_id"]
        if key not in seen:
            npr[row["product_reported"]] += 1
        seen[key].add(row["reaction_verbatim"])
        a[(row["product_reported"], row["reaction_verbatim"])] += 1
    out = []
    for (name, term), aa in sorted(a.items()):
        if aa < W.N_MIN:
            continue
        np_ = npr[name]
        bb = np_ - aa
        cc = dd = 0
        for q, n in npr.items():
            if q == name:
                continue
            x = a.get((q, term), 0)
            cc += x
            dd += n - x
        if cc == 0 or aa == 0:
            continue
        prr = (aa / np_) / (cc / (cc + dd))
        tot = aa + bb + cc + dd
        e = [(aa + bb) * (aa + cc) / tot, (aa + bb) * (bb + dd) / tot,
             (cc + dd) * (aa + cc) / tot, (cc + dd) * (bb + dd) / tot]
        chi = sum((o - x) ** 2 / x for o, x in zip((aa, bb, cc, dd), e))
        if prr >= W.PRR_MIN and chi >= W.CHI_MIN:
            out.append((name, term))
    return out


def rung0(tgt, listed):
    """the run on the extract with the reporter's own words taken for the reaction, everything else
    done right: the cases collapsed, the product resolved, the window on receipt date"""
    master = {r["submission_id"]: r for r in rd(tgt, "report_master.csv")}
    code_of = {}
    for r in rd(tgt, "product_register.csv"):
        code_of[r["product_name"]] = r["product_code"]
        if r["former_name"]:
            code_of[r["former_name"]] = r["product_code"]
    units = {}
    for row in rd(tgt, "spontaneous_reports_extract.csv"):
        m = master[row["submission_id"]]
        if not (W.Q_FROM <= D(m["receipt_date"]) <= W.Q_TO):
            continue
        u = units.setdefault(row["case_id"], {"code": code_of[row["product_reported"]],
                                              "reactions": set()})
        u["reactions"].add(row["reaction_verbatim"])
    npr, a = collections.Counter(), collections.Counter()
    for u in units.values():
        npr[u["code"]] += 1
        for r in u["reactions"]:
            a[(u["code"], r)] += 1
    return run(npr, a, listed)


MONTHS = [(2026, 7, "2026-07"), (2026, 8, "2026-08"), (2026, 9, "2026-09")]


def ask_channels(tgt):
    """per channel and month of the quarter: submissions received, those not coded, median days
    from receipt to coding"""
    tot = collections.Counter()
    for r in rd(tgt, "channel_totals.csv"):
        d = D(r["received_on"])
        if W.Q_FROM <= d <= W.Q_TO:
            tot[(r["channel"], d.strftime("%Y-%m"))] += int(r["submissions_received"])
    nc = collections.Counter()
    for r in rd(tgt, "coding_exceptions.csv"):
        d = D(r["received_on"])
        if W.Q_FROM <= d <= W.Q_TO:
            nc[(r["channel"], d.strftime("%Y-%m"))] += 1
    days = collections.defaultdict(list)
    for r in rd(tgt, "report_master.csv"):
        d = D(r["receipt_date"])
        if W.Q_FROM <= d <= W.Q_TO:
            days[(r["channel"], d.strftime("%Y-%m"))].append((D(r["coded_date"]) - d).days)
    out = {}
    for ch in W.CHANNELS:
        for _y, _m, key in MONTHS:
            k = (ch, key)
            out["%s|%s" % (ch, key)] = {
                "received": tot[k], "not_coded": nc[k],
                "mean_days": round(sum(days[k]) / len(days[k]) + 1e-9, 1) if days[k] else None}
    return out


def ask_holders(tgt):
    """per licence holder: submissions filed, those filed after the quarter closed, the fee due"""
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(tgt, "data_agreement_schedule.xlsx"))
    base, amend = {}, {}
    ws = wb["Schedule"]
    for row in ws.iter_rows(min_row=5, values_only=True):
        if not row or not row[0]:
            continue
        base[row[1]] = {"rate": int(row[2]), "to": D(row[4]) if row[4] else None}
    for row in wb["Amendments"].iter_rows(min_row=4, values_only=True):
        if not row or not row[0]:
            continue
        amend[row[1]] = {"rate": int(row[3]), "from": D(row[4])}
    subs = rd(tgt, "holder_submissions.csv")
    out = {}
    for r in subs:
        h = r["licence_holder"]
        d = D(r["received_on"])
        e = out.setdefault(h, {"filed": 0, "after_close": 0, "fee": 0.0})
        e["filed"] += 1
        if d > W.Q_TO:
            e["after_close"] += 1
        rate = base[h]["rate"]
        if h in amend and d >= amend[h]["from"]:
            rate = amend[h]["rate"]
        e["fee"] += rate
    for h in out:
        out[h]["fee"] = int(round(out[h]["fee"]))
    return dict(sorted(out.items()))


def ask_cells(tgt, cases):
    """per region and age group: the cases, and the share of them naming a serious reaction"""
    out = {}
    bands = W.AGE_BANDS + ["not stated"]
    for reg in W.REGIONS:
        for band in bands:
            sel = [c for c in cases if c["region"] == reg
                   and (c["age"] or "not stated") == band]
            n = len(sel)
            s = sum(1 for c in sel if c["serious"])
            out["%s|%s" % (reg, band)] = {
                "cases": n, "serious_share": round(100.0 * s / n, 1) if n else None}
    return out
