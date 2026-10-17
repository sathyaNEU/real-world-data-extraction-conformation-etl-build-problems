"""An independent reader of the shipped bundle: it knows figures.json and target/ and nothing else."""
import collections
import csv
import datetime as dt
import json
import os

K = [0]
D = dt.date.fromisoformat
Q_FROM, Q_TO = D("2026-07-01"), D("2026-09-30")
PRR_MIN, CHI_MIN, N_MIN, CAPACITY = 2.0, 4.0, 15, 16
CHANNELS = ["clinician", "licence holder", "patient", "pharmacy"]
MONTHS = ["2026-07", "2026-08", "2026-09"]


def ok(cond, msg):
    K[0] += 1
    if not cond:
        raise AssertionError("verify: " + msg)


def rd(tgt, name):
    with open(os.path.join(tgt, name), newline="") as f:
        return list(csv.DictReader(f))


def run(tgt, figures_path):
    fig = json.load(open(figures_path))

    master = {r["submission_id"]: r for r in rd(tgt, "report_master.csv")}
    code_of, former = {}, None
    for r in rd(tgt, "product_register.csv"):
        code_of[r["product_name"]] = r["product_code"]
        if r["former_name"]:
            code_of[r["former_name"]] = r["product_code"]
            former = r["product_code"]
    dic = rd(tgt, "reaction_dictionary.csv")
    pref = {(r["reaction_verbatim"], r["dictionary_version"]): r["preferred_term"] for r in dic}
    ser = {(r["reaction_verbatim"], r["dictionary_version"]): r["serious"] == "yes" for r in dic}
    listed = collections.defaultdict(set)
    for r in rd(tgt, "product_information_listed.csv"):
        listed[r["product_code"]].add(r["preferred_term"])

    cases = {}
    for row in rd(tgt, "spontaneous_reports_extract.csv"):
        m = master[row["submission_id"]]
        d = D(m["receipt_date"])
        if not (Q_FROM <= d <= Q_TO):
            continue
        c = cases.setdefault(row["case_id"], {"code": code_of[row["product_reported"]],
                                              "reactions": set(), "serious": set(),
                                              "region": m["region"], "age": m["age_band"]})
        k = (row["reaction_verbatim"], row["dictionary_version"])
        c["reactions"].add(pref[k])
        if ser[k]:
            c["serious"].add(pref[k])
    cases = list(cases.values())
    npr, a = collections.Counter(), collections.Counter()
    for c in cases:
        npr[c["code"]] += 1
        for r in c["reactions"]:
            a[(c["code"], r)] += 1

    def table(code, reaction, drop=()):
        aa = a.get((code, reaction), 0)
        np_ = npr[code]
        bb = np_ - aa
        cc = dd = 0
        for q, n in npr.items():
            if q == code or q in drop:
                continue
            x = a.get((q, reaction), 0)
            cc += x
            dd += n - x
        return aa, bb, cc, dd

    def prr_chi(code, reaction, drop=()):
        aa, bb, cc, dd = table(code, reaction, drop)
        if aa == 0 or cc == 0:
            return None, None
        prr = (aa / (aa + bb)) / (cc / (cc + dd))
        t = aa + bb + cc + dd
        e = [(aa + bb) * (aa + cc) / t, (aa + bb) * (bb + dd) / t,
             (cc + dd) * (aa + cc) / t, (cc + dd) * (bb + dd) / t]
        return prr, sum((o - x) ** 2 / x for o, x in zip((aa, bb, cc, dd), e))

    def take(drop=()):
        out = []
        for (code, reaction), aa in sorted(a.items()):
            if aa < N_MIN or reaction in listed.get(code, ()):
                continue
            prr, chi = prr_chi(code, reaction, tuple(q for q in drop if q != code))
            if prr and prr >= PRR_MIN and chi >= CHI_MIN:
                out.append((code, reaction, prr, chi, aa))
        return out

    dom = max(npr, key=lambda c: npr[c])
    crude = take()
    corr = take((dom,))
    ok(len(corr) == fig["taken_forward"], "the pairs taken forward")
    ok(len(crude) == fig["crude_count"], "the pairs the whole-database comparison takes")
    ok(CAPACITY - len(corr) == fig["slots_left"], "the assessment slots left")
    ok(abs(100.0 * npr[dom] / len(cases) - fig["dominant_share"]) < 5e-2, "the dominant share")
    sc = set(x[:2] for x in crude)
    su = set(x[:2] for x in corr)
    ok(set(tuple(x) for x in fig["masked_pairs"]) == su - sc, "the pairs the booster held down")
    ok(sc <= su, "the crude list is a subset of the answer")
    byk = {(x["code"], x["reaction"]): x for x in fig["signals"]}
    ok(len(byk) == len(corr), "figures.json lists every pair taken forward")
    for code, reaction, prr, chi, aa in corr:
        f = byk[(code, reaction)]
        ok(f["reports"] == aa, "reports for %s %s" % (code, reaction))
        ok(abs(round(f["prr"], 2) - round(prr, 2)) < 5e-3, "ratio for %s %s" % (code, reaction))
        ok(abs(round(f["chi"], 1) - round(chi, 1)) < 5e-2, "chi-square for %s %s" % (code, reaction))
        if (code, reaction) in su - sc:
            p0, _ = prr_chi(code, reaction)
            ok(abs(round(f["prr_crude"], 2) - round(p0, 2)) < 5e-3,
               "the whole-database ratio for %s %s" % (code, reaction))
            ok(p0 < PRR_MIN, "a masked pair is short of the threshold against the whole database")
    for r, sh in fig["campaign_share"].items():
        nam = sum(v for (c, rr), v in a.items() if rr == r)
        ok(abs(100.0 * a[(dom, r)] / nam - sh) < 5e-2, "the booster's share of %s" % r)

    # the asks
    tot = collections.Counter()
    for r in rd(tgt, "channel_totals.csv"):
        d = D(r["received_on"])
        if Q_FROM <= d <= Q_TO:
            tot[(r["channel"], d.strftime("%Y-%m"))] += int(r["submissions_received"])
    nc = collections.Counter()
    for r in rd(tgt, "coding_exceptions.csv"):
        d = D(r["received_on"])
        if Q_FROM <= d <= Q_TO:
            nc[(r["channel"], d.strftime("%Y-%m"))] += 1
    days = collections.defaultdict(list)
    for r in rd(tgt, "report_master.csv"):
        d = D(r["receipt_date"])
        if Q_FROM <= d <= Q_TO:
            days[(r["channel"], d.strftime("%Y-%m"))].append((D(r["coded_date"]) - d).days)
    for ch in CHANNELS:
        for mo in MONTHS:
            want = fig["a1_channels"]["%s|%s" % (ch, mo)]
            k = (ch, mo)
            ok(want["received"] == tot[k], "A1 received, %s %s" % (ch, mo))
            ok(want["not_coded"] == nc[k], "A1 not coded, %s %s" % (ch, mo))
            ok(abs(want["mean_days"] - round(sum(days[k]) / len(days[k]) + 1e-9, 1)) < 5e-2,
               "A1 mean days, %s %s" % (ch, mo))

    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(tgt, "data_agreement_schedule.xlsx"))
    base, amend = {}, {}
    for row in wb["Schedule"].iter_rows(min_row=5, values_only=True):
        if row and row[0]:
            base[row[1]] = int(row[2])
    for row in wb["Amendments"].iter_rows(min_row=4, values_only=True):
        if row and row[0]:
            amend[row[1]] = (int(row[3]), D(row[4]))
    got = {}
    for r in rd(tgt, "holder_submissions.csv"):
        h = r["licence_holder"]
        d = D(r["received_on"])
        e = got.setdefault(h, [0, 0, 0])
        e[0] += 1
        if d > Q_TO:
            e[1] += 1
        rate = base[h]
        if h in amend and d >= amend[h][1]:
            rate = amend[h][0]
        e[2] += rate
    for h, v in fig["a2_holders"].items():
        ok(got[h][0] == v["filed"], "A2 filed, %s" % h)
        ok(got[h][1] == v["after_close"], "A2 after the close, %s" % h)
        ok(got[h][2] == v["fee"], "A2 fee, %s" % h)

    for key, v in fig["a3_cells"].items():
        reg, band = key.split("|")
        sel = [c for c in cases if c["region"] == reg and (c["age"] or "not stated") == band]
        ok(len(sel) == v["cases"], "A3 cases, %s" % key)
        s = sum(1 for c in sel if c["serious"])
        ok(abs(round(100.0 * s / len(sel), 1) - v["serious_share"]) < 5e-2, "A3 share, %s" % key)
    return K[0]
