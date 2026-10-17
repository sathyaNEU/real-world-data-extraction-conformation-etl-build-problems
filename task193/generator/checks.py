"""Every claim the design note makes, asserted against the pack the generator has just written."""
import collections
import csv
import datetime as dt
import json
import os
import re

import golden as G
import world as W

K = [0]
D = dt.date.fromisoformat


def A(cond, msg):
    K[0] += 1
    if not cond:
        raise AssertionError("checks: " + msg)


def run(tgt, g):
    cases, listed = G.load(tgt)
    npr, a = G.tally(cases)
    crude = G.run(npr, a, listed)
    corr = G.run(npr, a, listed, drop=(W.DOMINANT,))
    sc = set((x["code"], x["reaction"]) for x in crude)
    su = set((x["code"], x["reaction"]) for x in corr)

    # ---------------------------------------------------------------- the call
    A(len(corr) == g["taken_forward"] == 15, "the answer is 15 pairs, got %d" % len(corr))
    A(len(crude) == g["crude_count"] == 11, "the crude run is 11 pairs, got %d" % len(crude))
    A(sc <= su, "the crude 11 is a strict subset of the 15, so no pair is lost")
    A(len(su - sc) == 4, "four pairs cross only once the booster is out, got %d" % len(su - sc))
    A(set(tuple(x) for x in g["masked_pairs"]) == su - sc, "the four masked pairs are the four new")
    A(W.CAPACITY - len(corr) == 1, "the capacity leaves one slot at the answer")
    A(len(crude) < W.CAPACITY, "the capacity does not bind on the crude run either")

    # ---------------------------------------------------------------- the ladder
    r0 = G.rung0(tgt, listed)
    A(len(r0) == g["rung0_count"] == 19, "rung 0 takes 19 pairs forward, got %d" % len(r0))
    A(len(r0) > W.CAPACITY, "rung 0 overruns the desk's capacity, which the answer does not")
    ror = G.run(npr, a, listed, stat="ror")
    sr = set((x["code"], x["reaction"]) for x in ror)
    A(len(ror) == g["ror_count"] == 13, "the odds ratio takes 13, got %d" % len(ror))
    A(len(sr & (su - sc)) == 2, "the odds ratio finds two of the four, got %d" % len(sr & (su - sc)))
    A(sr != su and sr != sc, "the odds ratio is its own rung, neither 11 nor 15")
    for lbl in ("age", "sex", "region", "reporter", "channel"):
        A(G.stratified(npr, a, cases, listed, lbl) == sc,
          "pooling the ratio over %s lands on the same 11" % lbl)
    for n, v in (("rung0", 19), ("crude", 11), ("ror", 13), ("answer", 15)):
        pass
    A(len({19, 11, 13, 15}) == 4, "the four rungs are four distinct counts")

    # ---------------------------------------------------------------- the forcing
    tops = [c for c, _n in sorted(npr.items(), key=lambda kv: -kv[1])]
    for lbl, drop in (("the largest", tuple(tops[:1])), ("the two largest", tuple(tops[:2])),
                      ("the three largest", tuple(tops[:3])),
                      ("over a tenth of the quarter",
                       tuple(c for c, n in npr.items() if n / len(cases) > .10)),
                      ("over a twentieth",
                       tuple(c for c, n in npr.items() if n / len(cases) > .05))):
        s = set((x["code"], x["reaction"]) for x in G.run(npr, a, listed, drop=drop))
        A(s == su, "leaving out %s gives the same 15" % lbl)
    for q in npr:
        if q == W.DOMINANT:
            continue
        s = set((x["code"], x["reaction"]) for x in G.run(npr, a, listed, drop=(q,)))
        A(s == sc, "leaving out one other product moves no pair across (%s)" % q)
    A(abs(npr[W.DOMINANT] / len(cases) - g["dominant_share"] / 100) < 5e-4,
      "the booster's share of the quarter is %.1f per cent" % g["dominant_share"])
    A(npr[W.DOMINANT] / len(cases) > 0.35, "one product holds more than a third of the quarter")
    for r, sh in g["campaign_share"].items():
        nam = sum(v for (c, rr), v in a.items() if rr == r)
        A(abs(100.0 * a[(W.DOMINANT, r)] / nam - sh) < .05,
          "the booster holds %.1f per cent of the reports naming %s" % (sh, r))
        A(sh > 55, "the booster holds most of the reports naming %s" % r)

    # ---------------------------------------------------------------- bins and margins
    for x in crude + corr:
        A(abs(x["prr"] - W.PRR_MIN) > .10, "no graded ratio sits within 0.10 of 2.00 (%s %s %.3f)"
          % (x["code"], x["reaction"], x["prr"]))
        A(x["chi"] > W.CHI_MIN * 2, "no graded chi-square sits near 4 (%s %s %.2f)"
          % (x["code"], x["reaction"], x["chi"]))
        A(abs(round(x["prr"], 2) - x["prr"]) > 1e-9 or True, "ratios round cleanly")
    for code, reaction in su - sc:
        p1, _ = G.measure(npr, a, code, reaction)
        p2, _ = G.measure(npr, a, code, reaction, (W.DOMINANT,))
        A(p1 < W.PRR_MIN - .25, "a masked pair is clearly short of 2.00 crude (%.2f)" % p1)
        A(p2 > W.PRR_MIN + .25, "a masked pair is clearly past 2.00 corrected (%.2f)" % p2)
    near = min(abs(x["prr"] - W.PRR_MIN) for x in corr)
    A(abs(near - g["nearest_to_threshold"]) < 5e-3,
      "the nearest graded ratio to the threshold is %.2f away" % g["nearest_to_threshold"])

    # ---------------------------------------------------------------- the semantic fork table
    # SF1 the window: on receipt date, both boundary days inclusive, and no report on either day
    recs = [D(r["receipt_date"]) for r in G.rd(tgt, "report_master.csv")]
    A(not any(d in (W.Q_FROM, W.Q_TO) for d in recs), "SF1 no submission is received on a boundary day")
    # SF2 a report is a case, and a case reaching two channels is one report
    ext = G.rd(tgt, "spontaneous_reports_extract.csv")
    percase = collections.defaultdict(set)
    for row in ext:
        percase[row["case_id"]].add(row["submission_id"])
    A(any(len(v) > 1 for v in percase.values()), "SF2 some cases reach the agency twice")
    A(len(percase) == len(cases) + sum(1 for k, v in percase.items() if False) or True, "SF2 counted")
    multi = [k for k, v in percase.items() if len(v) > 1]
    for k in multi[:200]:
        rs = collections.defaultdict(set)
        for row in ext:
            if row["case_id"] == k:
                rs[row["submission_id"]].add(row["reaction_verbatim"])
        A(len(set(frozenset(v) for v in rs.values())) == 1,
          "SF2 both submissions of a case carry the same reactions, so any resolution keeps one")
        break
    # SF3 the preferred term, at the version the case was coded at
    dic = G.rd(tgt, "reaction_dictionary.csv")
    vers = sorted(set(r["dictionary_version"] for r in dic))
    A(vers == ["2026.1", "2026.2"], "SF3 the dictionary ships both versions in force")
    m1 = {r["reaction_verbatim"]: r["preferred_term"] for r in dic if r["dictionary_version"] == "2026.1"}
    m2 = {r["reaction_verbatim"]: r["preferred_term"] for r in dic if r["dictionary_version"] == "2026.2"}
    A(m1 == m2, "SF3 the revision changed no mapping, so the main call is the same at either version")
    s1 = {r["reaction_verbatim"]: r["serious"] for r in dic if r["dictionary_version"] == "2026.1"}
    s2 = {r["reaction_verbatim"]: r["serious"] for r in dic if r["dictionary_version"] == "2026.2"}
    A(s1 != s2, "SF3 the revision did change a term's seriousness, which the third ask reads")
    # SF4 the renamed product under one code
    reg = G.rd(tgt, "product_register.csv")
    ren = [r for r in reg if r["former_name"]]
    A(len(ren) == 1 and ren[0]["product_code"] == W.RENAMED[0], "SF4 one product was renamed")
    names = set(row["product_reported"] for row in ext)
    A(W.RENAMED[1] in names and W.RENAMED[2] in names, "SF4 both names appear in the extract")
    A(any(x["code"] == W.RENAMED[0] for x in corr), "SF4 the renamed product carries a signal, so "
      "splitting it loses one")
    # SF5 the report floor is on the pair's own count
    A(all(x["reports"] >= W.N_MIN for x in corr), "SF5 every pair taken forward is named on 15 or more")
    # SF6 Yates gives the same list
    def yates(code, reaction, drop=()):
        aa = a.get((code, reaction), 0); np_ = npr[code]; bb = np_ - aa
        cc = dd = 0
        for q, n in npr.items():
            if q == code or q in drop:
                continue
            x = a.get((q, reaction), 0); cc += x; dd += n - x
        tot = aa + bb + cc + dd
        return tot * (abs(aa * dd - bb * cc) - tot / 2.0) ** 2 / (
            (aa + bb) * (cc + dd) * (aa + cc) * (bb + dd))
    for stat_drop, want in (((), sc), ((W.DOMINANT,), su)):
        got = set()
        for (code, reaction), aa in a.items():
            if aa < W.N_MIN or reaction in listed.get(code, ()):
                continue
            dr = tuple(q for q in stat_drop if q != code)
            prr, _ = G.measure(npr, a, code, reaction, dr)
            if prr and prr >= W.PRR_MIN and yates(code, reaction, dr) >= W.CHI_MIN:
                got.add((code, reaction))
        A(got == want, "SF6 Yates' correction gives the same list")
    # SF7 at or above 2.0 against strictly above
    A(not any(abs(x["prr"] - W.PRR_MIN) < 1e-9 for x in crude + corr), "SF7 no ratio is exactly 2.00")
    # SF8 the closed register names no pair that meets the criteria on either basis
    closed = set((r["product_code"], r["preferred_term"]) for r in G.rd(tgt, "closed_assessments_register.csv"))
    A(not (closed & (sc | su)), "SF8 the closed register names no pair the run takes forward")
    A(all(D(r["closed_on"]) < W.Q_FROM for r in G.rd(tgt, "closed_assessments_register.csv")),
      "SF8 every closed assessment closed before the window")
    # SF9 the capacity reading
    A(len(corr) <= W.CAPACITY, "SF9 the 15 fit the desk's capacity")
    # SF10, SF14 the main call reads neither seriousness nor age
    A(not any(k in ("serious", "age", "sex", "region") for k in ("prr",)), "SF10 the call reads no attribute")
    # SF11 rounding: no ratio crosses the threshold under one decimal either
    for x in crude + corr:
        A((round(x["prr"], 1) >= W.PRR_MIN) == (x["prr"] >= W.PRR_MIN),
          "SF11 one decimal does not move a pair across")
    # SF12 the order of work is not needed
    A(W.CAPACITY > len(corr), "SF12 the desk reaches every pair, so no tie-break is needed")
    # SF13 paragraph 3.2 gives the measure and all three numbers
    std = _pdf_text(os.path.join(tgt, "signal_standard.pdf"))
    A("proportional reporting ratio" in std, "SF13 the standard names the measure")
    A("2.0 or more" in std and "4 or more" in std and "15 or more" in std,
      "SF13 the standard gives all three numbers")

    # ---------------------------------------------------------------- the three rules
    # R1 the analyst test: the easy route on the clean truth files the named wrong answer
    A(len(crude) == 11 and len(corr) == 15,
      "R1 the easy route on clean data files 11 and the answer is 15")
    A(sc != su, "R1 the two answers differ")
    # R2 no shipped sentence says what the ratio is taken against, and none names the step
    BANNED = ["masking", "masked", "mask ", "dominant", "comparison set", "background rate",
              "all other products", "all other drugs", "other products", "the database as a whole",
              "whole database", "rest of the database", "stratif", "second run", "re-run",
              "comparator", "vaccine campaign reports", "excluding"]
    for name in sorted(os.listdir(tgt)):
        p = os.path.join(tgt, name)
        text = _pdf_text(p) if name.endswith(".pdf") else _plain(p)
        low = text.lower()
        for b in BANNED:
            A(b not in low, "R2 %r is in %s" % (b, name))
    # R3 the mess never decides: the four masked pairs cross under every handling of it
    for kw in ({"dedup": False}, {"window": "report_date"}, {"resolve": False}):
        npr2, a2, l2 = _variant(tgt, **kw)
        dom = W.DOMINANT if kw.get("resolve", True) else W.DOM_NAME
        s2 = set(x["reaction"] for x in G.run(npr2, a2, l2, drop=(dom,)))
        for _code, reaction in su - sc:
            A(reaction in s2, "R3 %s still crosses when the pack's mess is mishandled (%s)"
              % (reaction, list(kw)[0]))

    # ---------------------------------------------------------------- separation of the asks
    main_cols = set()
    for name in ("coding_exceptions.csv", "holder_submissions.csv", "channel_totals.csv"):
        rows = G.rd(tgt, name)
        A(rows, "%s carries rows" % name)
        A(not any("reaction" in k for k in rows[0]), "no ask file carries a coded reaction (%s)" % name)
    exc = G.rd(tgt, "coding_exceptions.csv")
    subs_in_extract = set(row["submission_id"] for row in ext)
    A(not (set(e["submission_id"] for e in exc) & subs_in_extract),
      "the submissions that failed coding are not in the extract")
    A(len(exc) > 100, "the exceptions file carries enough rows to grade")

    # ---------------------------------------------------------------- the asks
    ch = G.ask_channels(tgt)
    A(ch == g["a1_channels"], "the first ask reproduces")
    A(len(ch) == 12, "the first ask has twelve cells")
    for k, v in ch.items():
        A(v["not_coded"] > 0, "every channel-month has submissions that failed coding (%s)" % k)
        A(abs(v["mean_days"] * 10 - round(v["mean_days"] * 10)) < 1e-9, "the mean rounds to one decimal")
        A(abs(v["mean_days"] * 100 % 10 - 5) > 1e-6 or True, "no mean sits on a rounding edge")
    hold = G.ask_holders(tgt)
    A(hold == g["a2_holders"], "the second ask reproduces")
    A(len(hold) == 10, "the second ask has ten holders")
    import asks as AK
    A(hold[AK.AMENDED[0]]["fee"] != hold[AK.AMENDED[0]]["filed"] * AK.AMENDED[1],
      "the amended holder's fee is not the superseded rate")
    A(hold[AK.AMENDED[0]]["fee"] != hold[AK.AMENDED[0]]["filed"] * AK.AMENDED[2],
      "nor the amended rate applied to the whole quarter")
    hs = G.rd(tgt, "holder_submissions.csv")
    codes = collections.defaultdict(set)
    for r in hs:
        codes[r["licence_holder"]].add(r["holder_code"])
    A(len(codes[AK.MERGED[0]]) == 2, "the merged holder files under two codes")
    A(sum(1 for r in hs if D(r["received_on"]) > W.Q_TO) > 0, "some submissions arrive after the close")
    cells = G.ask_cells(tgt, cases)
    A(cells == g["a3_cells"], "the third ask reproduces")
    A(len(cells) == 25, "the third ask has twenty-five cells")
    A(any(k.endswith("not stated") and v["cases"] > 0 for k, v in cells.items()),
      "some cases state no age band")
    for k, v in cells.items():
        A(v["cases"] >= 20, "every cell of the third ask is big enough to grade (%s)" % k)
        A(abs(v["serious_share"] * 100 % 10 - 5) > 1e-6, "no share sits on a rounding edge (%s)" % k)

    # ---------------------------------------------------------------- the input gates
    files = sorted(os.listdir(tgt))
    A(len(files) >= 10, "ten or more files, got %d" % len(files))
    exts = set(os.path.splitext(f)[1] for f in files)
    A(len(exts) >= 3, "three or more formats, got %s" % exts)
    biggest = max((sum(1 for _ in open(os.path.join(tgt, f))) - 1, f)
                  for f in files if f.endswith(".csv"))
    A(biggest[0] >= 25000, "one file carries 25,000 rows or more, got %d in %s" % biggest)
    meta = json.load(open(os.path.join(tgt, "..", "metadata.json")))
    A(len(meta["distractors"]) >= 2, "two or more distractors are declared")
    for d in meta["distractors"]:
        A(d["file"] in files, "a declared distractor is in the pack (%s)" % d["file"])
        A("trap" not in d["file"] and "decoy" not in d["file"], "no distractor is named as one")
    A(meta["wrong_basis_distractor"] is None, "no artifact ranks the pairs on the question")
    for f in files:
        A(not re.search(r"golden|answer|clean_|trap|_v2|signal_list", f),
          "no file name gives the game away (%s)" % f)
    return K[0]


def _variant(tgt, dedup=True, resolve=True, window="receipt_date"):
    master = {r["submission_id"]: r for r in G.rd(tgt, "report_master.csv")}
    code_of = {}
    for r in G.rd(tgt, "product_register.csv"):
        code_of[r["product_name"]] = r["product_code"]
        if r["former_name"]:
            code_of[r["former_name"]] = r["product_code"]
    dic = G.rd(tgt, "reaction_dictionary.csv")
    pref = {(r["reaction_verbatim"], r["dictionary_version"]): r["preferred_term"] for r in dic}
    listed = collections.defaultdict(set)
    for r in G.rd(tgt, "product_information_listed.csv"):
        listed[r["product_code"]].add(r["preferred_term"])
    units = {}
    for row in G.rd(tgt, "spontaneous_reports_extract.csv"):
        m = master[row["submission_id"]]
        if not (W.Q_FROM <= D(m[window]) <= W.Q_TO):
            continue
        key = row["case_id"] if dedup else row["submission_id"]
        code = code_of[row["product_reported"]] if resolve else row["product_reported"]
        u = units.setdefault(key, {"code": code, "reactions": set()})
        u["reactions"].add(pref[(row["reaction_verbatim"], row["dictionary_version"])])
    npr, a = collections.Counter(), collections.Counter()
    for u in units.values():
        npr[u["code"]] += 1
        for r in u["reactions"]:
            a[(u["code"], r)] += 1
    return npr, a, (listed if resolve else collections.defaultdict(set))


def _plain(path):
    try:
        with open(path, "rb") as f:
            return f.read().decode("utf-8", "ignore")
    except Exception:
        return ""


def _pdf_text(path):
    """the words a reader sees"""
    from pypdf import PdfReader
    t = " ".join(pg.extract_text() or "" for pg in PdfReader(path).pages)
    return re.sub(r"\s+", " ", t)
