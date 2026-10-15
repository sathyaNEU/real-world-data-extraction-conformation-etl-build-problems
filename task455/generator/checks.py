"""task455's assertions, run on every build: the input gates; the golden from the bundle against the generator's truth;
the three-rules block on the clean truth (the default path files Caldmere, Eskwell and Tolbeck, the decisive step alone
files Dunrath, Eskwell and Quarrin); every rung and reflex by name; the fork rows SF1 to SF16; the variants'
convergence and the margins; mess neutrality; the asks' goldens and stops and their separation from the call; the
realism sweep; the deliverables against figures.json."""
import json
import os
import re
from collections import Counter

import numpy as np

import golden as G
import methods as M
import world as W

RESULTS = []
GOLD = {"Dunrath", "Eskwell", "Quarrin"}
DEFAULT = {"Caldmere", "Eskwell", "Tolbeck"}
ADDRESS = {"Dunrath", "Eskwell", "Tolbeck"}
N = W.NAME


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def names(cs):
    return {N[c] for c in cs}


def top3(rates):
    return {N[c] for c in sorted(rates, key=lambda c: -rates[c])[:3]}


def edge(v, unit=0.1):
    """Distance of v from the nearest rounding edge at `unit` (absolute)."""
    x = v / unit
    return abs((x - np.floor(x)) - 0.5) * unit


def openpyxl_load(path):
    import openpyxl
    return openpyxl.load_workbook(path, data_only=True)


def truth(world):
    """The clean truth, read from the generator's accounts: who is a new business and who continues one."""
    A = world["world"].accts
    emp = world["d"]["emp"]
    t = {"births26": Counter(), "cont26": Counter(), "filed26": Counter(), "births25": Counter(), "base25": Counter(),
         "base24": Counter(), "deaths25": Counter()}
    for a in A:
        e = emp[a.idx]
        if e[12:15].max() > 0:
            t["base25"][a.county] += 1
        if e[0:3].max() > 0:
            t["base24"][a.county] += 1
        if a.kind == "birth" and a.year == 2026:
            t["births26"][a.county] += 1
        if a.kind == "succ" and a.year == 2026:
            t["cont26"][a.county] += 1
            if a.succ_type == "filed":
                t["filed26"][a.county] += 1
        if a.kind == "birth" and a.year == 2025:
            t["births25"][a.county] += 1
        nz = np.nonzero(e)[0]
        if len(nz) and 3 <= nz[-1] <= 14 and e[15:].max() == 0 and a.successor is None:
            t["deaths25"][a.county] += 1
    return t


def run(target, golden_dir, world=None, meta_path=None):
    del RESULTS[:]
    B = M.Bundle(target)
    g = B.golden()
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    meta = json.load(open(meta_path)) if meta_path else {}

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    ok("gate: a file of 25,000 rows or more", len(B.w) >= 25000 and len(B.q) >= 25000,
       "wage records %d, quarterly reports %d" % (len(B.w), len(B.q)))
    ok("gate: two or more distractors declared", len(meta.get("distractor_files", [])) >= 2,
       ", ".join(meta.get("distractor_files", [])))
    ok("gate: no file named after a distractor or the stump", not any(re.search(r"distract|decoy|continu|successor|birth",
                                                                                f, re.I) for f in files), "")
    ok("gate: every distractor ships", all(f in files for f in meta.get("distractor_files", [])), "")

    # ---------------------------------------------------------------- golden against the truth
    T = truth(world) if world else None
    if T:
        ok("golden: births by county equal the generator's new businesses",
           {N[c]: v for c, v in g["births"].items()} == dict(T["births26"]), str(dict(T["births26"])))
        ok("golden: set-aside accounts equal the generator's continuations",
           {N[c]: v for c, v in g["setaside"].items() if v} == dict(T["cont26"]), str(dict(T["cont26"])))
        ok("golden: the 2025Q4 base is the planned count", {N[c]: v for c, v in g["base"].items()} ==
           {k: v["B"] for k, v in W.Y26.items()}, "")
        a, b = B.ask_a(), B.ask_b()
        ok("golden: Ask A births equal the generator's 2025 new businesses",
           {N[c]: v for c, v in a["births"].items()} == dict(T["births25"]), str(dict(T["births25"])))
        ok("golden: Ask B deaths equal the generator's 2025 closures not continued",
           {N[c]: v for c, v in b["deaths"].items()} == dict(T["deaths25"]), str(dict(T["deaths25"])))
        ok("golden: the 2024Q4 base by the worksite's county equals the truth",
           {N[c]: v for c, v in a["base"].items()} == dict(T["base24"]), "")
    ok("golden: designation", names(g["top3"]) == GOLD, ", ".join(sorted(names(g["top3"]))))
    ok("golden: runner-up Caldmere", N[g["runner_up"]] == "Caldmere", N[g["runner_up"]])
    r = g["rates"]
    o = g["order"]
    ok("golden: third over fourth 1.2x or more", r[o[2]] / r[o[3]] >= 1.2, "%.3f" % (r[o[2]] / r[o[3]]))
    ok("golden: runner-up clear of the fifth by 0.5 or more", r[o[3]] - r[o[4]] >= 0.5, "%.3f" % (r[o[3]] - r[o[4]]))
    ok("golden: every 2026 rate and the gap 0.01 or more from a rounding edge",
       min(edge(v) for v in r.values()) >= 0.01 and edge(g["gap"]) >= 0.01,
       "least %.4f, gap %.4f" % (min(edge(v) for v in r.values()), edge(g["gap"])))
    ok("golden: rounded rates keep the order of the three and the runner-up",
       len({round(r[c], 1) for c in o[:4]}) == 4 and round(r[o[2]], 1) > round(r[o[3]], 1), "")

    # ---------------------------------------------------------------- the three rules, executed
    if world:
        A = world["world"].accts
        base = {k: v["B"] for k, v in W.Y26.items()}
        new26 = Counter(a.county for a in A if a.kind in ("birth", "succ") and a.year == 2026)
        filed = Counter(a.county for a in A if a.kind == "succ" and a.year == 2026 and a.succ_type == "filed")
        same = Counter(a.county for a in A if a.kind == "succ" and a.year == 2026
                       and a.succ_type in ("same", "chain", "resold"))
        relet = Counter(a.county for a in A if a.kind == "birth" and a.year == 2026 and a.relet_of is not None)
        easy = {c: 100.0 * (new26[c] - filed[c]) / base[c] for c in base}
        ok("R3a: the easy route on the clean truth (new accounts net of the filed transfers) files Caldmere, Eskwell "
           "and Tolbeck", set(sorted(easy, key=lambda c: -easy[c])[:3]) == DEFAULT,
           ", ".join("%s %.2f" % (c, easy[c]) for c in sorted(easy, key=lambda c: -easy[c])))
        dec = {c: 100.0 * (new26[c] - (new26[c] - T["births26"][c])) / base[c] for c in base}
        ok("R3b: the easy route with only the decisive step (workforce continuity) files the golden",
           set(sorted(dec, key=lambda c: -dec[c])[:3]) == GOLD, "")
        one = {c: 100.0 * (new26[c] - filed[c] - same[c] - relet[c]) / base[c] for c in base}
        ok("R3b: the easy route with the address correction alone files a wrong set (Dunrath, Eskwell, Tolbeck)",
           set(sorted(one, key=lambda c: -one[c])[:3]) == ADDRESS, "")
        ok("R3c: no plant: one quarterly report per account and quarter, one wage row per worker, account and quarter",
           not B.q.duplicated(["account_no", "year", "qtr"]).any()
           and not B.w.duplicated(["worker_key", "account_no", "year", "qtr"]).any(), "")
    cols = set(B.reg.columns) | set(B.q.columns) | set(B.w.columns)
    ok("R1: no shipped column holds continuity, a birth flag or a source account",
       not any(re.search(r"birth|continu|success|source|flow|new_bus", c, re.I) for c in cols), ", ".join(sorted(cols)))
    wf = sum(1 for k in g["cls"].values() if k == "workforce")
    ok("R1: the golden's decisive computation reads the wage records (continuations found only there)", wf >= 40,
       "%d continuations by workforce, %d filed" % (wf, sum(1 for k in g["cls"].values() if k == "filed")))

    # ---------------------------------------------------------------- the ladder by name
    lad = B.ladder()
    def names_of(key):
        rr, oo = lad[key]
        return {N[c] for c in oo[:3]}, rr, oo
    for key, want in (("R0 default (net of filed)", DEFAULT), ("R0 every new account", DEFAULT),
                      ("R1 address match", ADDRESS), ("R3 workforce (golden)", GOLD)):
        got, rr, oo = names_of(key)
        ok("rung: %s files %s" % (key, ", ".join(sorted(want))), got == want, ", ".join(sorted(got)))
    for key in ("R1 address, same industry, adjacent", "R1 address without suites", "name match", "address or name",
                "R2 attributes, same county", "R2 attributes, any county", "R2 attributes or address",
                "address and workforce", "any worker from a closed account"):
        got, rr, oo = names_of(key)
        ok("reflex: %s misses the golden" % key, got != GOLD, ", ".join(sorted(got)))
        ok("reflex: %s keeps Caldmere or Tolbeck in, or Quarrin out" % key,
           ("Caldmere" in got or "Tolbeck" in got or "Quarrin" not in got), "")
    rr, oo = lad["R1 address match"]
    ok("margin: rung 1 third over fourth 1.15x or more", rr[oo[2]] / rr[oo[3]] >= 1.15, "%.3f" % (rr[oo[2]] / rr[oo[3]]))
    rr, oo = lad["R0 default (net of filed)"]
    q, cald, tolb = W.CODE["Quarrin"], W.CODE["Caldmere"], W.CODE["Tolbeck"]
    ok("margin: rung 0 Caldmere over Quarrin 1.1x or more", rr[cald] / rr[q] >= 1.1, "%.3f" % (rr[cald] / rr[q]))
    for key in ("R1 address match", "R1 address, same industry, adjacent", "R2 attributes, same county",
                "R2 attributes, any county", "name match"):
        rr, oo = lad[key]
        ok("dominance: Tolbeck under %s above Quarrin's golden rate" % key, rr[tolb] > g["rates"][q] or
           {N[c] for c in oo[:3]} != GOLD, "%.2f against %.2f" % (rr[tolb], g["rates"][q]))

    # ---------------------------------------------------------------- the semantic fork table
    new26 = B.new_accounts(2026)
    wages_first = {a for a in B.ai if (B.wag[B.ai[a]] > 0).any() and int(np.argmax(B.wag[B.ai[a]] > 0)) >= 5}
    emp_first = set(new26)
    ok("SF1: first quarter with wages and first month with employment select the same 2026 new accounts",
       {a for a in wages_first if B.emp[B.ai[a], :15].max() == 0} == emp_first, "%d accounts" % len(emp_first))
    liab = {a for a, r0 in B.reg_by.iterrows() if r0["liability_date"][:4] == "2026"}
    ok("SF2: liability dates in 2026 select the same new accounts", liab == emp_first, "%d" % len(liab))
    regd = {a for a, r0 in B.reg_by.iterrows() if r0["registration_date"][:4] == "2026"}
    ok("SF3: every 2026 new account was opened in 2026", emp_first <= regd, "")
    rates_reg, _ = B.rung_rates(set(B.pred) | {a for a, k in g["cls"].items() if k == "workforce"})
    ok("SF3: the registration reading (adds accounts opened in 2026 that never employed) keeps the call",
       top3({c: 100.0 * (sum(1 for a in regd if B.county[a] == c and g["cls"].get(a, "birth") == "birth")) /
             g["base"][c] for c in g["base"]}) == GOLD, "")
    q2026 = B.q[B.q["year"] == 2026]
    ok("SF4: no 2026 new account filed a report before 2026",
       not B.q[(B.q["year"] < 2026) & B.q["account_no"].isin(emp_first)].shape[0], "")
    dec = Counter(B.county[a] for a, i in B.ai.items() if B.emp[i, 14] > 0)
    ok("SF5: December 2025 employment alone as the base keeps the call",
       top3({c: 100.0 * g["births"][c] / dec[c] for c in dec}) == GOLD, "")
    qi4 = W.QUARTERS.index((2025, 4))
    wb = Counter(B.county[a] for a, i in B.ai.items() if B.wag[i, qi4] > 0)
    ok("SF6: wages in 2025Q4 as the base keeps the call", top3({c: 100.0 * g["births"][c] / wb[c] for c in wb}) == GOLD,
       "")
    rows_read = B.q[(B.q["qi"] >= qi4)]
    ok("SF7: every quarterly row from 2025Q4 on carries the register's county",
       (rows_read["county_code"].to_numpy() == rows_read["account_no"].map(B.county).to_numpy()).all(), "")
    ok("SF8: private accounts only", set(B.reg["ownership_code"]) == {"5"} and set(B.q["own_code"]) == {"5"}, "")
    fl = [B.flow(a) for a in new26 if a in B.pred]
    ok("SF9: every filed successor's first workforce came mostly from its predecessor",
       all(f[0] == B.pred[a] and f[3] > 0.5 for a, f in zip([a for a in new26 if a in B.pred], fl)), "")
    base_cls = g["cls"]
    for thr in (0.6, 0.7, 0.8):
        ok("SF10: a threshold of %.0f per cent selects the same accounts" % (100 * thr),
           B.classify(2026, threshold=thr) == base_cls, "")
    shares = [B.flow(a) for a in new26]
    births_share = max(f[3] for a, f in zip(new26, shares) if base_cls[a] == "birth")
    cont_share = min(f[3] for a, f in zip(new26, shares) if base_cls[a] != "birth")
    ok("SF10: births draw 40 per cent or less from any one account, continuations 80 per cent or more",
       births_share <= 0.40 and cont_share >= 0.80, "births at most %.2f, continuations at least %.2f" %
       (births_share, cont_share))
    ok("SF11: dropping the stopped-reporting condition selects the same accounts",
       B.classify(2026, need_stop=False) == base_cls, "")
    wq = {a: int(np.argmax(B.wag[B.ai[a]] > 0)) for a in new26}
    ok("SF12: every 2026 new account's first quarter with wages is its first quarter with employment",
       all(wq[a] == B.first_quarter(a) for a in new26), "")
    alt = {}
    for a in new26:
        if a in B.pred:
            alt[a] = "filed"
            continue
        qi = B.first_quarter(a)
        c = Counter()
        ws = B.paid.get((a, qi), set())
        for wk in ws:
            for k in range(qi - 1, -1, -1):
                ps = [p for p in B.payers.get((wk, k), ()) if p != a]
                if ps:
                    for p in ps:
                        c[p] += 1
                    break
        top = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0] if c else (None, 0)
        alt[a] = "workforce" if top[0] and top[1] / len(ws) > 0.5 and B.stopped_by(top[0], qi) else "birth"
    ok("SF13: the worker's last account in any earlier quarter selects the same accounts", alt == base_cls, "")
    ok("SF14: the two-sided reading selects the same accounts", B.classify(2026, two_sided=True) == base_cls, "")
    src_share = min(f[5] for a, f in zip(new26, shares) if base_cls[a] == "workforce")
    ok("SF14: every continuation carries 70 per cent or more of its old account's workers", src_share >= 0.7,
       "%.2f" % src_share)
    rr = {c: round(v, 1) for c, v in g["rates"].items()}
    ok("SF15: rounded and unrounded rates designate the same three",
       {N[c] for c in sorted(rr, key=lambda c: (-rr[c], c))[:3]} == GOLD, "")
    if world:
        A = world["world"].accts
        nums = world["nums"]
        resold = [nums[a.idx] for a in A if a.role == "resold"]
        succ = [nums[a.idx] for a in A if a.kind == "succ" and a.succ_type == "resold"]
        ok("SF16: births that changed hands within 2026 stay births and their successors are set aside",
           all(base_cls.get(x) == "birth" for x in resold) and all(base_cls.get(x) == "workforce" for x in succ),
           "%d and %d" % (len(resold), len(succ)))

    # ---------------------------------------------------------------- mess neutrality (R2)
    ok("R2: address formats: the golden reads no address", True, "classification uses accounts, reports, wages")
    ok("R2: ZIP-based county codes: the rows the call reads carry the worksite's county (SF7)", True, "")
    payers_keep = B.payers
    one = {}
    wtab = B.w.sort_values(["worker_key", "qi", "wages"])
    last = wtab.drop_duplicates(["worker_key", "qi"], keep="last")
    B.payers = {(wk, qi): {ac} for wk, qi, ac in zip(last["worker_key"], last["qi"], last["account_no"])}
    one = B.classify(2026)
    B.payers = payers_keep
    ok("R2: a worker on two accounts in a quarter counted at the higher-paying one only: same accounts", one == base_cls,
       "")
    ok("R2: monthly employment against quarterly wages (SF1, SF6) and registration against liability (SF2, SF3): "
       "same call", True, "")
    zero_base = Counter(B.county[a] for a in set(B.q[B.q["qi"] == qi4]["account_no"]))
    ok("R2: zero reports from open accounts read as operating: same call (counts ruled out by guideline 3.4)",
       top3({c: 100.0 * g["births"][c] / zero_base[c] for c in zero_base}) == GOLD, "")

    # ---------------------------------------------------------------- separation of the asks
    if world:
        A = world["world"].accts
        nums = world["nums"]
        summer = {nums[a.idx] for a in A if a.kind == "seasonal"}
        dormant = {nums[a.idx] for a in A if a.kind == "dormant"}
        base_rows = {a for a, i in B.ai.items() if B.emp[i, 12:15].max() > 0}
        ok("separation: no summer employer among the 2026 new accounts or the 2025Q4 base, no dormant account among "
           "the 2026 new accounts", not (summer & (set(emp_first) | base_rows)) and not (dormant & set(emp_first)),
           "%d summer, %d dormant accounts" % (len(summer), len(dormant)))
        ok("separation: the dormant accounts employ in 2025Q4 under every reading (the base is the same however they "
           "are read)", dormant <= base_rows, "")
        minority = {nums[a.idx] for a in A if a.minority}
        ok("separation: the border worksites' ZIP-based rows are all before 2025Q3",
           (B.q[B.q["account_no"].isin(minority) & (B.q["qi"] >= 3)]["county_code"].to_numpy() ==
            B.q[B.q["account_no"].isin(minority) & (B.q["qi"] >= 3)]["account_no"].map(B.county).to_numpy()).all(), "")

    # ---------------------------------------------------------------- the asks: goldens and stops
    a, b = B.ask_a(), B.ask_b()
    ok("Ask A: every 2025 birth rate 0.01 or more from a rounding edge", min(edge(v) for v in a["rates"].values()) >= 0.01,
       "%.4f" % min(edge(v) for v in a["rates"].values()))
    ok("Ask B: every 2025 death rate 0.01 or more from a rounding edge", min(edge(v) for v in b["rates"].values()) >= 0.01,
       "%.4f" % min(edge(v) for v in b["rates"].values()))
    def misses(x, ref, key, every=True):
        if key in ("births", "deaths"):
            hit = [c for c in ref[key] if x[key].get(c, 0) == ref[key][c]]
        else:
            hit = [c for c in ref[key] if round(x[key][c], 1) == round(ref[key][c], 1)]
        return (not hit) if every else len(hit), hit
    stops = [
        ("Ask A cracker: the extract's window and the quarterly row's county", B.ask_a(liability=False, county_from="qcew"), a, ("births", "rates")),
        ("Ask A: the extract's window alone", B.ask_a(liability=False), a, ("births", "rates")),
        ("Ask A: the quarterly row's county alone", B.ask_a(county_from="qcew"), a, ("births", "rates")),
        ("Ask B cracker: the quarterly row's county", B.ask_b(county_from="qcew"), b, ("deaths", "rates")),
        ("Ask B mirror: filed transfers only", B.ask_b(continuation=False), b, ("deaths", "rates")),
        ("Ask B: wages for employment", B.ask_b(by="wages"), b, ("deaths", "rates")),
    ]
    for label, x, ref, keys in stops:
        for k in keys:
            allmiss, hit = misses(x, ref, k)
            ok("%s misses every %s figure" % (label, "count" if k != "rates" else "rate"), allmiss,
               "hits: %s" % ", ".join(N[c] for c in hit))
    mirror = B.classify(2025)
    mirror_births = Counter(B.county[x] for x, k in mirror.items() if k in ("birth", "workforce"))
    ok("Ask A mirror (no workforce test) misses every count",
       all(mirror_births[c] != a["births"][c] for c in a["births"]), "")

    rr0, oo0 = lad["R0 every new account"]
    ok("write-up: Caldmere and Tolbeck are second and third on new employer accounts per 100 establishments",
       [N[c] for c in oo0[1:3]] == ["Caldmere", "Tolbeck"], ", ".join(N[c] for c in oo0[:3]))

    # ---------------------------------------------------------------- registers (H9) and the fiction (H24)
    import csv as _csv
    man = [r["file_name"] for r in _csv.DictReader(open(os.path.join(target, W.FILES["manifest"]), encoding="utf-8"))]
    ok("H9: the manifest names exactly the shipped files", sorted(man) == files, "%d named" % len(man))
    dwb = openpyxl_load(os.path.join(target, W.FILES["dict"]))
    dfiles = [r[0] for r in dwb["Files"].iter_rows(min_row=5, values_only=True) if r[0]]
    ok("H9: the dictionary's Files sheet names exactly the shipped files", sorted(dfiles) == files, "%d named" % len(dfiles))
    tell = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith((".csv", ".txt")):
            txt = open(p, encoding="utf-8").read(3_000_000)
        elif f.endswith(".pdf"):
            from pypdf import PdfReader as _R
            txt = "\n".join(pg.extract_text() or "" for pg in _R(p).pages)
        else:
            w_ = openpyxl_load(p)
            txt = " ".join(str(c) for ws_ in w_.worksheets for row in ws_.iter_rows(values_only=True) for c in row if c)
        if re.search(r"fictional|fictitious|constructed for|invented|this exercise|synthetic", txt, re.I):
            tell.append(f)
    ok("H24: no shipped file says the pack was built", not tell, ", ".join(tell))

    # ---------------------------------------------------------------- realism sweep
    for label, vals in (("2026 births", g["births"]), ("2025 births", a["births"]), ("2025 deaths", b["deaths"]),
                        ("2025Q4 base", g["base"]), ("2024Q4 base", a["base"])):
        v = [vals[c] for c in sorted(vals)]
        ok("realism: %s differ across counties" % label, len(set(v)) == len(v), str(v))
    ok("realism: no county's 2024Q4 and 2025Q4 bases are equal", all(a["base"][c] != g["base"][c] for c in g["base"]), "")
    ok("realism: no county's 2025 births equal its 2025 deaths", all(a["births"][c] != b["deaths"][c] for c in g["base"]),
       "")
    tot = [sum(g["births"].values()), sum(a["births"].values()), sum(b["deaths"].values()), sum(g["base"].values())]
    ok("realism: no round regional totals", all(t % 10 for t in tot), str(tot))
    per = B.q.groupby("account_no")["total_qtrly_wages"].apply(lambda s: s[s > 0].round(0).value_counts().max()
                                                              if (s > 0).any() else 0)
    ok("realism: no account reports the same wages in three quarters", (per >= 3).sum() == 0, "%d" % (per >= 3).sum())
    tn = B.reg["trade_name"].value_counts()
    ok("realism: trade names repeat only for take-overs that kept the name", (tn > 3).sum() == 0, str(tn.head(3).to_dict()))
    for f in ("register", "qcew", "wages"):
        p = os.path.join(target, W.FILES[f])
        txt = open(p, encoding="utf-8").read(400000)
        ok("realism: no em or en dash in %s" % W.FILES[f], "—" not in txt and "–" not in txt, "")
    regd_ok = (B.reg["registration_date"] <= W.EXTRACT.isoformat()).all() and \
        (B.reg["inactivation_date"].replace("", "0000") <= W.EXTRACT.isoformat()).all()
    ok("realism: every register date on or before the extract", regd_ok, "")
    persons = set(W.PEOPLE.values())
    gtxt = ""
    from pypdf import PdfReader
    gtxt = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(target, W.FILES["guideline"])).pages)
    ok("realism: the guideline names only the drawn persona", re.findall(r"Brandon Compton", gtxt) != [] and
       not any(p in gtxt for p in persons - {W.PEOPLE["director"]}), "")
    ok("realism: the guideline names no evidence or method (worker, wage, flow, address, ZIP, staff, workforce)",
       not re.search(r"worker|wage|flow|address|ZIP|staff|workforce(?! Services)", gtxt, re.I), "")

    # ---------------------------------------------------------------- deliverables against figures.json
    import openpyxl
    wbk = openpyxl.load_workbook(os.path.join(golden_dir, G.BOOK), data_only=True)
    ws = wbk["Designation 2026"]
    rows = {r[0]: r for r in ws.iter_rows(min_row=5, values_only=True) if r[0] in fig["counties"]}
    ok("deliverable: workbook county rows equal figures.json",
       all(rows[n][6] == fig["counties"][n]["births"] and rows[n][5] == fig["counties"][n]["set_aside"] and
           rows[n][8] == fig["counties"][n]["rate"] for n in fig["counties"]), "")
    ys = wbk["2025 births and deaths"]
    yr = {r[0]: r for r in ys.iter_rows(min_row=5, values_only=True) if r[0] in fig["y2025"]}
    ok("deliverable: workbook 2025 rows equal figures.json",
       all(yr[n][2] == fig["y2025"][n]["births"] and yr[n][3] == fig["y2025"][n]["birth_rate"] and
           yr[n][4] == fig["y2025"][n]["deaths"] and yr[n][5] == fig["y2025"][n]["death_rate"] for n in fig["y2025"]), "")
    na = wbk["New accounts 2026"]
    ok("deliverable: the workbook lists every 2026 new account once", na.max_row - 1 == len(new26) ==
       fig["new_accounts"], "%d" % (na.max_row - 1))
    mtxt = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(golden_dir, G.MEMO)).pages)
    ok("deliverable: the memo names the three and the runner-up", all(n in mtxt for n in fig["designated"]) and
       fig["runner_up"] in mtxt and ("%.1f" % fig["gap"]) in mtxt, "")
    ok("deliverable: no em dash in the goldens", "—" not in mtxt, "")

    bad = [r0 for r0 in RESULTS if not r0[1]]
    for label, good, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("checks: %d of %d passed" % (len(RESULTS) - len(bad), len(RESULTS)))
    return not bad
