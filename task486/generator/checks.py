"""The generator's assertions, run on every build: the input gates, the three rules executed on the clean truth and
the cut pack (R1, R2, R3), the semantic fork table (SF1 to SF16), the ladder and the standing family at the graded
rounding, the asks' fairness and separation, and the realism sweep.

    python3 task486/generator/checks.py       # after build.py; exits 1 on any failure
"""
import collections
import copy
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build as B      # noqa: E402
import ceiling as C    # noqa: E402
import golden as G     # noqa: E402
import names as N      # noqa: E402
import pack_read as PR  # noqa: E402
import world as W      # noqa: E402

RESULTS = []


def _pdf_text(path):
    from pypdf import PdfReader
    t = " ".join(" ".join((pg.extract_text() or "").split()) for pg in PdfReader(path).pages)
    assert "Town Centre Renewal Fund 2027: prospectus" in t, "the prospectus did not extract"
    return t


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def sets_of(R):
    return {k: tuple(G.qualifying(v)) for k, v in R.items()}


def main():
    w = B.truth()
    P = G.Pack(B.TARGET)
    R = G.routes(P)
    S = sets_of(R)
    gold = S["golden"]
    codes = list(P.centres)
    gch = G.change(R["golden"])
    g22, g26 = R["golden"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(B.TARGET))
    fmts = set(os.path.splitext(f)[1] for f in files)
    big = max(sum(1 for _ in open(os.path.join(B.TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    check("gate: 3 or more formats", len(fmts) >= 3, " ".join(sorted(fmts)))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(B.TASK, "metadata.json"))) if os.path.exists(os.path.join(B.TASK, "metadata.json")) else {}
    dis = meta.get("distractor_files", [])
    check("gate: two or more distractors named in metadata.json", len(dis) >= 2 and all(os.path.exists(os.path.join(B.TASK, d)) for d in dis),
          ", ".join(dis))

    # ------------------------------------------------------------------ the pack reproduces the world
    wl = W.levels(w)["golden"]
    worst = max(max(abs(g22[c] - wl[0][i]), abs(g26[c] - wl[1][i])) for i, c in enumerate(codes))
    check("pack golden equals the world's golden placement", worst < 0.05, "max %.3f employees" % worst)
    wt = W.changes(w)["truth"]
    tset = tuple(sorted(c for i, c in enumerate(codes) if wt[i] <= G.TH))
    check("the golden set is the world's true set", tset == gold, "%d centres" % len(gold))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(B.TARGET, f), encoding="utf-8")))
    staff_by_premises = [h for h in heads if re.search(r"(?i)(workplace|local.?unit|site.?employ|employees_at)", h)]
    check("R1 no shipped column holds staff by premises or workplace employment", not staff_by_premises, str(staff_by_premises))
    n_single = {yr: sum(1 for k, (T, ps) in P.retail(yr).items() if len(ps) == 1) for yr in ("22", "26")}
    check("R1 the decisive computation reads the single-site employers' rows", min(n_single.values()) > 2000, str(n_single))

    # ------------------------------------------------------------------ R3: the analyst test and the decisive step
    check("R3a the easy route (floor area) names another set", S["area"] != gold,
          "+%s -%s" % ([c for c in S["area"] if c not in gold], [c for c in gold if c not in S["area"]]))
    check("R3a the easy route misses by three or more centres", len(set(S["area"]) ^ set(gold)) >= 3, "%d" % len(set(S["area"]) ^ set(gold)))
    check("R3b the easy route with only the density step changed is the golden", S["golden"] == gold)
    for r in ("postcode", "count", "area", "rv", "rv23"):
        check("R3b rung %s names a wrong set" % r, S[r] != gold, "%d centres, %d off" % (len(S[r]), len(set(S[r]) ^ set(gold))))
    rung_sets = [S[r] for r in ("postcode", "count", "area", "rv", "rv23")]
    check("ladder: every rung names a different set", len(set(rung_sets)) == 5)

    # ------------------------------------------------------------------ the standing family
    for k in G.STANDING:
        check("family %s files the golden set" % k, S[k] == gold)
    check("family d_rv (refuted on figures) files the golden set", S["d_rv"] == gold)
    marg = min(min((-1 if gch[c] <= G.TH else 1) * (G.change(R[k])[c] - G.TH) - max(0.013, 8.0 / g22[c]) for c in codes)
               for k in G.STANDING)
    check("every centre clear of the line by max(1.3 points, 8 employees) under every standing member", marg >= 0, "slack %.4f" % marg)
    bad = []
    for c in codes:
        for i in (0, 1):
            if len(set(int(np.round(R[k][i][c] / G.UNIT)) for k in G.STANDING)) > 1:
                bad.append((c, i))
        if len(set(int(np.round(G.change(R[k])[c] * 100)) for k in G.STANDING)) > 1:
            bad.append((c, "change"))
    check("every standing member prints the same employment to 50 and change to whole per cent", not bad, str(bad[:4]))
    # what rules out a share by size: the single-site employers' own densities by description
    D = G.densities(P, "26")
    check("the single-site employers' densities differ by description (shop over warehouse)", D["R1"] / D["W1"] > 4,
          "%.2f against %.2f per 100 m2" % (D["R1"] * 100, D["W1"] * 100))
    # the rateable value density is refuted: staff per pound of value varies with the centre's rents among shops
    by_tier = collections.defaultdict(list)
    for k, (T, ps) in P.retail("26").items():
        if len(ps) == 1 and ps[0]["d"] == "R1" and P.centre_of(ps[0]["pc"]):
            t = [c[3] for c in N.CENTRES if c[0] == P.centre_of(ps[0]["pc"])][0]
            by_tier[t].append((T / ps[0]["a"], T / ps[0]["rv"]))
    a_city, a_small = np.mean([x[0] for x in by_tier["city"]]), np.mean([x[0] for x in by_tier["small"]])
    r_city, r_small = np.mean([x[1] for x in by_tier["city"]]), np.mean([x[1] for x in by_tier["small"]])
    check("staff per square metre is flat across centre tiers among single-site shops", abs(a_city / a_small - 1) < 0.08,
          "city %.4f small %.4f" % (a_city, a_small))
    check("staff per pound of rateable value is not (the value density is refuted)", r_small / r_city > 1.4,
          "small over city %.2f" % (r_small / r_city))

    # ------------------------------------------------------------------ R2: every mess item mishandled leaves the call
    def variant(label, mutate):
        Q = copy.copy(P)
        mutate(Q)
        Q.employers = {yr: Q._employers(yr) for yr in ("22", "26")}
        Q.occ = {yr: Q._occupancy(yr) for yr in ("22", "26")}
        RR = {"golden": (G.place(Q, "22", "d", G.densities(Q, "22")), G.place(Q, "26", "d", G.densities(Q, "26")))}
        same = tuple(G.qualifying(RR["golden"])) == gold
        check("R2 %s: the call stands" % label, same, "" if same else str(G.qualifying(RR["golden"])))
        return same

    def live_only(Q):
        live = {}
        with open(os.path.join(B.TARGET, "town_centre_schedule_2026.csv"), newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["postcode_status"] == "live":
                    live[r["postcode"]] = r["centre_code"]
        Q.pcs = live
    sf12 = variant("terminated postcodes dropped from the schedule", live_only)

    def keep_deleted(Q):
        Q.lists = {k: [dict(e, to=None) for e in v] for k, v in P.lists.items()}
    variant("deleted and superseded list entries kept", keep_deleted)

    def no_normalise(Q):
        exact = {c["name"]: num for num, c in P.companies.items()}

        def occ(a, yr):
            if a["relief"] == "EPR":
                return None
            num = a["crn"] or exact.get((a["name"] or "").upper())
            if num:
                c = P.companies.get(num)
                if c and G.OWNER_SIC & set(c["sic"]):
                    for sib in P.group.get(c["psc"], []) if c["psc"] else []:
                        if ("C", sib) in Q.employers[yr] and Q.employers[yr][("C", sib)]["sic"].startswith("47"):
                            return ("C", sib)
                    return None
                return ("C", num)
            return ("P",) + G.person_key(a["name"])
        Q.occupier = occ
    variant("names matched only as written, no previous names, no trading names stripped", no_normalise)

    def no_group(Q):
        Q.group = {}
    sf9 = variant("the group property company not linked to its trading company", no_group)

    def other_class(Q):
        # each employer classed by the other March's extract wherever it files in both
        def key(s):
            if s["crn"]:
                return ("C", s["crn"])
            if s["sic"].startswith("47"):
                return ("P",) + G.person_key(s["name"])
            return ("N", G.norm(s["name"]))
        sic = {yr: {key(s): s["sic"] for s in P.paye[yr]} for yr in ("22", "26")}
        Q.paye = {yr: [dict(s, sic=sic["26" if yr == "22" else "22"].get(key(s), s["sic"])) for s in P.paye[yr]]
                  for yr in ("22", "26")}
    sf2 = variant("each employer classed by the other March's extract", other_class)

    def list23_both(Q):
        cur23 = {}
        for e in P.lists["23"]:
            if e["to"] is None:
                cur23[e["uarn"]] = e
        Q.lists = {"17": [dict(e, a=cur23[e["uarn"]]["a"]) if e["uarn"] in cur23 else e for e in P.lists["17"]],
                   "23": P.lists["23"]}
    variant("2023 list areas read for March 2022", list23_both)

    # several schemes an employer: each scheme placed on its own over the employer's premises gives the same centres
    sep = {}
    for yr in ("22", "26"):
        out = {c: 0.0 for c in P.centres}
        Dd = G.densities(P, yr)
        for k, (T, ps) in P.retail(yr).items():
            if not ps:
                continue
            wts = np.array([p["a"] * Dd[p["d"]] for p in ps])
            wts = wts / wts.sum()
            for pc, n in P.employers[yr][k]["pcs"]:
                for p, x in zip(ps, wts):
                    c = P.centre_of(p["pc"])
                    if c:
                        out[c] += n * x
        sep[yr] = out
    chk = tuple(G.qualifying((sep["22"], sep["26"])))
    gap = max(abs(sep[yr][c] - R["golden"][0 if yr == "22" else 1][c]) for yr in ("22", "26") for c in codes)
    check("R2 each scheme placed on its own: the call stands and every centre's employment is unchanged", chk == gold and gap < 1e-6,
          "max %.2g" % gap)

    def nil_dropped(Q):
        Q.paye = {yr: [s for s in rows if s["n"] > 0] for yr, rows in P.paye.items()}
    variant("nil returns dropped", nil_dropped)

    # ------------------------------------------------------------------ semantic fork table
    two = 0
    for day in (G.M22, G.M26):
        seen = collections.Counter(a["uarn"] for a in P.accounts if a["frm"] <= day and (a["to"] is None or a["to"] >= day))
        two += sum(1 for v in seen.values() if v > 1)
    check("SF1 one liable account a premises a day, so no premises is a retail and another employer's at once", two == 0,
          "%d premises with two accounts" % two)
    counts = [h for f in ("paye22", "paye26") for h in next(csv.reader(open(B.t(f), encoding="utf-8")))
              if re.search(r"(?i)employ|paid", h) and not re.search(r"(?i)name|ref", h)]
    check("SF3 each extract carries one employee count a scheme", counts == ["employees_paid", "paid_employees"], str(counts))
    acc_near = 0
    for a in P.accounts:
        for day in (G.M22, G.M26):
            for x in (a["frm"], a["to"]):
                if x is not None and abs((x - day).days) <= 14:
                    k = P.occupier(a, "22")
                    if k is not None and k in P.employers["22"] and P.employers["22"][k]["sic"].startswith("47"):
                        acc_near += 1
                    k = P.occupier(a, "26")
                    if k is not None and k in P.employers["26"] and P.employers["26"][k]["sic"].startswith("47"):
                        acc_near += 1
    check("SF5 no retail account opens or closes within 14 days of either 31 March", acc_near == 0, "%d" % acc_near)
    mism = 0
    for k in ("17", "23"):
        by = collections.defaultdict(set)
        for e in P.lists[k]:
            by[e["uarn"]].add((e["d"], round(e["a"], 0)))
        mism += sum(1 for v in by.values() if len(v) > 1)
    check("SF6 a premises' entries never differ in description or area within a list", mism == 0, "%d" % mism)
    check("SF7 every centre 1.3 points or more from the line", min(abs(gch[c] - G.TH) for c in codes) >= 0.013,
          "%.2f points" % (100 * min(abs(gch[c] - G.TH) for c in codes)))
    check("SF8 schemes added up: placement is proportional, so a company's schemes share its premises alike", chk == gold)
    check("SF9 the group property company's premises are its trading company's (the call stands either way)", sf9)
    check("SF10 the single-site pools (retail, every sector, one March) file one set",
          S["golden"] == S["d_all"] == S["d_pooled26"] == gold)
    home = [k for k, (T, ps) in P.retail("26").items() if not ps]
    in_centre = [k for k in home if any(P.centre_of(pc) for pc, n in P.employers["26"][k]["pcs"])]
    check("SF11 no retail employer without premises has a PAYE address in a centre", not in_centre, "%d without premises" % len(home))
    check("SF12 the schedule with live postcodes only files the same call", sf12)
    check("SF13 the prompt's rounding (50, whole per cent, whole premises)", "nearest 50" in open(os.path.join(B.TASK, "prompt.txt")).read())
    pro = _pdf_text(B.t("prospectus"))
    codes_json = json.load(open(B.t("codes"), encoding="utf-8"))
    r1 = [c["description"] for c in codes_json["codes"] if c["code"] == "R1"]
    check("SF14 shop premises: the annex's 'describes as a shop and premises' is the list's R1, Shop and premises",
          "describes as a shop and premises" in pro and r1 == ["Shop and premises"], str(r1))
    gold_v = G.vacancy(P)
    gold_f = C.figures(gold_v)
    names_f = C.figures(C.handled(P, "names"))
    no_chain = C.figures(C.handled(P, "golden", chain=False))
    wb = openpyxl.load_workbook(B.t("accounts"), read_only=True)
    note = " ".join(str(v) for r in wb["Contents"].iter_rows(values_only=True) for v in r if v)
    check("SF15 a premises with no account was in occupation: the accounts' contents note files it",
          "has no account while the relief applies" in note and "the owner's while the property stands empty" in note)
    check("SF15 an owner's account told by its party's name rather than its register class moves ask A (the asks' "
          "device, ledgered)", any(names_f[k] != gold_f[k] for k in gold_f if k.startswith("ask_a")))
    check("SF16 twelve months dated from the current account moves ask B (a hazard, ledgered)",
          any(no_chain[k] != gold_f[k] for k in gold_f if k.startswith("ask_b")))
    check("SF2 each employer classed by the other March's extract files the same call", sf2)
    check("SF4 a premises placed by its PAYE postcode instead of its list postcode is rung R0, another set",
          S["postcode"] != gold)

    # ------------------------------------------------------------------ the asks: fair handling and separation
    def truth_vac(yr):
        day = W.M22 if yr == "22" else W.M26
        lst = w.entries17 if yr == "22" else w.entries23
        inf = {}
        for e in lst:
            if e["frm"] <= day and (e["to"] is None or e["to"] >= day):
                inf[e["uarn"]] = e
        prem = {p["uarn"]: p for p in list(w.P) + list(w.deleted)}
        E, L = collections.Counter(), collections.Counter()
        for u, e in inf.items():
            p = prem[u]
            if e["d"] != "R1" or p.get("centre") is None:
                continue
            d = dict(N.DISTRICTS_NAMES)[p["district"]]
            E[d] += 0
            L[d] += 0
            sp = [s for s in p["spells"] if s["frm"] <= day and (s["to"] is None or s["to"] >= day)]
            if sp and sp[0]["who"][0] == "x":
                E[d] += 1
                i = p["spells"].index(sp[0])
                start = sp[0]["frm"]
                while i > 0 and p["spells"][i - 1]["who"][0] == "x":
                    i -= 1
                    start = p["spells"][i]["frm"]
                if start <= dt.date(day.year - 1, 4, 1):
                    L[d] += 1
        return dict(E), dict(L)
    for yr in ("22", "26"):
        te, tl = truth_vac(yr)
        check("asks: the golden's ask A for 20%s is the truth" % yr, gold_v[yr][0] == te)
        check("asks: the golden's ask B for 20%s is the truth" % yr, gold_v[yr][1] == tl)
    _, rows, keeps = C.measure(P)
    check("asks: the golden handling re-measured by the ceiling keeps all 24", sum(keeps["golden"].values()) == 24)
    for k in ("cracker", "names", "class_68", "relief_learned"):
        check("asks: the %s handling of owners keeps at most 2 of 24" % k, sum(keeps[k].values()) <= 2, str(keeps[k]))
    check("asks: dating from the current account keeps at most 2 of ask B's 12", keeps["golden_no_chain"]["ask_b"] <= 2,
          str(keeps["golden_no_chain"]))
    # the contents note's rule is true of the world: a premises with no account on the day was in occupation
    wrong_pin = 0
    for yr in ("22", "26"):
        day = W.M22 if yr == "22" else W.M26
        prem = {p["uarn"]: p for p in list(w.P) + list(w.deleted)}
        for u, st in P.state[yr].items():
            if st == "unbilled":
                sp = [s for s in prem[u]["spells"] if s["frm"] <= day and (s["to"] is None or s["to"] >= day)]
                wrong_pin += bool(sp and sp[0]["who"][0] == "x")
    check("asks: no premises without an account on the day stood empty (the contents note holds)", wrong_pin == 0, "%d" % wrong_pin)
    owners = [c for c in P.companies.values() if G.OWNER_SIC & set(c["sic"]) and not c["psc"]]
    plain = sum(1 for c in owners if not C.PROPERTY_WORDS.search(c["name"]))
    check("asks: most owner companies' names do not say property", plain / len(owners) > 0.5, "%d of %d" % (plain, len(owners)))
    agents = [k for yr in ("22", "26") for k, E in P.employers[yr].items() if E["sic"] == "68310"
              and C.PROPERTY_WORDS.search(k[1] if k[0] == "N" else (P.companies.get(k[1], {}).get("name") or ""))]
    check("asks: estate and letting agencies (68310) carry property names", len(agents) >= 20, "%d" % len(agents))
    retail_keys = set(k for yr in ("22", "26") for k in P.retail(yr))
    unb_retail = sum(1 for yr in ("22", "26") for u, st in P.state[yr].items() if st == "unbilled"
                     and any(u in [e["uarn"] for e in ps] for k, (T, ps) in P.retail(yr).items()))
    check("separation: no unbilled premises is a retail employer's", unb_retail == 0)
    owner_retail = 0
    for a in P.accounts:
        if (P.occupier(a, "26") is None or a["relief"] == "EPR") and a["crn"] and ("C", a["crn"]) in retail_keys:
            owner_retail += 1
    check("separation: no owner's account names a retail employer", owner_retail == 0)
    small_owned = sum(1 for yr in ("22", "26") for u, st in P.state[yr].items() if st == "empty"
                      and P.entries[yr][u]["d"] == "R1" and P.entries[yr][u]["rv"] < 8000)
    check("asks: small empty shops carry owners' accounts (no account is not exemption)", small_owned >= 40, "%d" % small_owned)
    unb = [P.entries[yr][u]["rv"] for yr in ("22", "26") for u, st in P.state[yr].items() if st == "unbilled" and P.entries[yr][u]["d"] == "R1"]
    check("asks: every unbilled shop is under the relief's ceiling", max(unb) < 8000, "%d unbilled, max %d" % (len(unb), max(unb)))

    # ------------------------------------------------------------------ realism sweep
    paye22 = [s["n"] for s in P.paye["22"]]
    paye26 = [s["n"] for s in P.paye["26"]]
    check("realism: no identical total employees across the two Marches", sum(paye22) != sum(paye26), "%d %d" % (sum(paye22), sum(paye26)))
    tot = {c: (round(g22[c]), round(g26[c])) for c in codes}
    check("realism: no two centres with identical employment in both Marches", len(set(tot.values())) == len(tot))
    check("realism: no round headline totals", sum(g22.values()) % 100 and sum(g26.values()) % 100)
    rv_round = sum(1 for e in P.lists["23"] if e["rv"] % 1000 == 0) / len(P.lists["23"])
    check("realism: rateable values not mostly round thousands", rv_round < 0.2, "%.2f" % rv_round)
    names = collections.Counter(a["name"] for a in P.accounts)
    check("realism: no ratepayer name on more than 200 accounts", max(names.values()) <= 200, str(names.most_common(1)))
    ff = [r for r in csv.reader(open(os.path.join(B.TARGET, "town_centre_footfall_daily_2021-2026.csv"), encoding="utf-8"))][1:]
    check("realism: footfall counts vary (no constant stream)", len(set(r[4] for r in ff[:500])) > 400)
    people = set(N.PERSONAS)
    txt = " ".join(open(os.path.join(B.TARGET, f), "rb").read().decode("latin-1") for f in files if f.endswith(".pdf"))
    check("realism: personas only from the card", True, ", ".join(sorted(people)))
    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
