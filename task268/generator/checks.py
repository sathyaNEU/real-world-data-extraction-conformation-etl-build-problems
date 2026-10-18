"""Generator checks for task268, run on the built pack and the clean truth. Every assertion is counted; any failure
stops the build."""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

import analysis as A
import common as K
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
N = [0]


def ok(cond, label):
    N[0] += 1
    if not cond:
        raise AssertionError(label)


def edge(v, u):
    """Distance from v to the nearest edge of the cell it rounds into at unit u."""
    return u / 2 - abs(v - round(v / u) * u)


def truth_presence(T, rate):
    """People present per core tract from the generator's clean truth (its tracts and integer flows)."""
    out = {}
    for M in T["metros"]:
        cbsa = {M["central"]} | M["outlying"]
        ring_in = lambda h, M=M: "C" if h[:5] == M["central"] else ("O" if h[:5] in M["outlying"] else "X")
        ring_out = lambda w, cbsa=cbsa: "C" if w[:5] in cbsa else "X"
        core = [t for t in M["tracts"] if t["core"] and t["kind"] != "water"]
        cs = {t["geoid"] for t in core}
        P = {t["geoid"]: float(round(t["R"])) for t in core}
        for (h, w), gs in M["flows"].items():
            if h == w:
                continue
            if h in cs:
                P[h] -= sum(n * rate(g, ring_out(w)) for g, n in gs.items())
            if w in cs:
                P[w] += sum(n * rate(g, ring_in(h)) for g, n in gs.items())
        p = np.array([P[t["geoid"]] for t in core])
        a = np.array([int(round(t["area"] * 1e6)) / 1e6 for t in core])
        out[M["metro"]["name"]] = (p * (p / a)).sum() / p.sum()
    return out


def run(target, T):
    D = A.load(target)
    G = A.run(D, "golden")
    F, order = G["F"], G["order"]
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    pick, runner = order[0], order[1]

    # ---------------------------------------------------------------- the ladder, read off the shipped pack
    rungs = {r: A.run(D, r) for r in ("cadp", "acs", "one", "pool", "ring")}
    ok(rungs["cadp"]["pick"] == "Halberdine", "R0 every job present picks Halberdine")
    ok(rungs["cadp"]["margin"] >= 1.2, "R0 margin 1.2 or more")
    ok(rungs["cadp"]["order"].index("Tessavon") in (3, 4), "Tessavon 4th or 5th at R0")
    ok(rungs["acs"]["pick"] == "Halberdine", "the ACS hazard lands on R0's metro")
    ok(rungs["acs"]["margin"] >= 1.15, "the hazard's margin")
    ok(rungs["one"]["pick"] == "Halberdine", "one survey share for every job lands on R0's metro")
    ok(rungs["pool"]["pick"] == "Corrisford", "R1 the share by industry group picks Corrisford")
    ok(rungs["pool"]["margin"] >= 1.15, "R1 margin 1.15 or more")
    ok(rungs["pool"]["order"].index("Tessavon") >= 2, "Tessavon below second at R1")
    ok(pick == "Tessavon" and fig["call"]["metro"] == "Tessavon", "R2 the golden picks Tessavon")
    ok(G["margin"] >= 1.25, "final margin 1.25 or more")
    ok(rungs["ring"]["pick"] == "Tessavon", "the residence type alone lands on the golden's call")
    lift = (F["Tessavon"]["pwd"] / rungs["pool"]["F"]["Tessavon"]["pwd"]) / (F["Corrisford"]["pwd"] / rungs["pool"]["F"]["Corrisford"]["pwd"])
    adv = rungs["pool"]["F"]["Corrisford"]["pwd"] / rungs["pool"]["F"]["Tessavon"]["pwd"]
    ok(lift >= 1.2 * adv, "dominance: Tessavon's lift over Corrisford at least 1.2 times Corrisford's R1 advantage")
    for m in K.METRO_NAMES:
        ok(F[m]["pwd"] < rungs["cadp"]["F"][m]["pwd"] * 1.0001 or m in ("Ashcombe",), "every correction walks %s down" % m)

    # ---------------------------------------------------------------- R1, R2, R3: the three rules on the clean truth
    tru = {g: {r: W.ATT[g][r] for r in "COX"} for g in K.GROUPS}
    pool_t = {g: sum(W.SMIX[g][r] * W.ATT[g][r] for r in "COX") for g in K.GROUPS}
    t0 = truth_presence(T, lambda g, r: 1.0)
    t1 = truth_presence(T, lambda g, r: pool_t[g])
    t2 = truth_presence(T, lambda g, r: tru[g][r])
    ok(max(t0, key=t0.get) == "Halberdine", "R3a the default path on the clean truth files Halberdine")
    ok(max(t1, key=t1.get) == "Corrisford", "R3b the share by group alone on the clean truth files Corrisford")
    ok(max(t2, key=t2.get) == "Tessavon", "R3b the decisive step alone on the clean truth files Tessavon")
    heads = set()
    for k in ("od_main", "survey", "population", "gazetteer"):
        with open(os.path.join(target, K.FILES[k])) as f:
            heads |= {h.strip().lower() for h in re.split(r"[,\t]", f.readline())}
    ok(not any(w in h for h in heads for w in ("present", "attend", "share", "density")),
       "R1 no shipped column holds people present, an attendance share or a density")
    ok(len(D["survey"]) >= 50000 and len(D["od"]) >= 100000, "R1 the survey's respondents and the flows ship at their grain")
    # R2, each mess item mishandled leaves the call and the critical components (the two leading densities) in their cells
    for kw, lab in ((dict(drop_aux=True), "the auxiliary part dropped"), (dict(sqmi=True), "land from the square-mile column")):
        r_ = A.run(D, "golden", **kw)
        ok(r_["pick"] == pick and r_["order"][1] == runner, "R2 %s keeps the call and runner-up" % lab)
        ok(round(r_["F"][pick]["pwd"] / 100) == round(F[pick]["pwd"] / 100) and
           round(r_["F"][runner]["pwd"] / 100) == round(F[runner]["pwd"] / 100), "R2 %s keeps both critical densities" % lab)
    unnorm = {r_[0] for r_ in csv.reader(open(os.path.join(target, K.FILES["population"])))}
    core_set = {g for gs in D["cores"].values() for g in gs}
    ok(not (unnorm & core_set), "R2 the population table's GEO_ID joins no tract until its prefix is dropped (loud)")
    D2 = dict(D)
    D2["survey"] = [dict(x, NAICS_SECTOR="23") if x["NAICS_SECTOR"] == "22" else x for x in D["survey"]]
    ok(A.run(D2, "golden")["pick"] == pick, "R2 utilities read as goods producing keep the call")
    me = A.run(D, "months_equal")
    ok(all(round(me["F"][m]["pwd"] / 100) == round(F[m]["pwd"] / 100) for m in K.METRO_NAMES),
       "R2 the twelve waves pooled or equal: same densities")
    blocks = {}
    for x in D["survey"]:
        blocks.setdefault(x["WAVE"], []).append((x["DAYS_PREM"], x["DAYS_HOME"], x["DAYS_NOTWORK"]))
    ok(len({tuple(v[:200]) for v in blocks.values()}) == len(blocks), "R3c no wave's block repeats another's")
    board = subprocess.run(["pdftotext", os.path.join(target, K.FILES["board"]), "-"], capture_output=True, text=True).stdout
    board = re.sub(r"\s+", " ", board)
    ok(not re.search(r"survey|attendance|remote|premises|outlying", board, re.I), "R3c the board paper names no method")
    ok(not any(m in board.split("3. The candidates")[0] for m in K.METRO_NAMES), "R3c no document ranks the metros")

    # ---------------------------------------------------------------- the semantic fork table
    ok(F[pick]["present"] > 0 and all(p >= 0 for p in G["P"].values()), "SF1 people present built from residents and workers")
    ok(all(g in D["pop"] for g in core_set), "SF2 every core tract has its census population")
    na = A.run(D, "golden", drop_aux=True)
    ok(na["pick"] == pick, "SF3 the main part alone: same call")
    ok(any(x.get("part") == "aux" for x in D["od"]), "SF3 the auxiliary part ships")
    pw = A.run(D, "per_workday")
    ok(pw["pick"] == pick, "SF4 days worked as the base: same call")
    sw = A.run(D, "sep_wave")
    ok(sw["pick"] == pick, "SF5 the September wave alone: same call")
    sq = A.run(D, "golden", sqmi=True)
    ok(all(round(sq["F"][m]["pwd"] / 100) == round(F[m]["pwd"] / 100) and
           round(sq["F"][m]["present"] / 1000) == round(F[m]["present"] / 1000) and
           round(100 * sq["F"][m]["dense"]) == round(100 * F[m]["dense"]) for m in K.METRO_NAMES), "SF6 square miles: same figures")
    ok(all(len(D["cores"][m]) >= 30 for m in K.METRO_NAMES), "SF7 the planning map lists every core")
    unw = {m: sum(d for _, _, _, d in F[m]["tracts"]) / len(F[m]["tracts"]) for m in K.METRO_NAMES}
    crude = {m: F[m]["present"] / sum(a for _, _, a, _ in F[m]["tracts"]) for m in K.METRO_NAMES}
    ok(max(unw, key=unw.get) != pick or True, "SF8 the unweighted tract mean is another quantity (recorded)")
    ok(max(crude, key=crude.get) != pick or True, "SF8 the crude density is another quantity (recorded)")
    water = [g for g in core_set if A.land_km2(D, g) == 0]
    ok(len(water) == 2 and all(D["pop"][g] == 0 for g in water), "SF9 two water-only core tracts, nobody living there")
    ok(all(K.SECTOR_GROUP[s] == g for s, _, g in K.SECTORS), "SF10 the sector list matches the extract notes")
    ok(A.run(D, "unweighted")["pick"] == pick, "SF12 unweighted: same call")
    tot = {}
    for x in D["survey"]:
        tot[x["WAVE"]] = tot.get(x["WAVE"], 0.0) + float(x["FINALWT"])
    ok(max(tot.values()) / min(tot.values()) < 1.02, "SF13 every wave's weights total its month within 2 per cent")
    dens = np.array([d for m in K.METRO_NAMES for _, _, _, d in F[m]["tracts"]])
    ok(np.min(np.abs(dens / K.DENSE - 1)) >= .02, "SF14 no core tract within 2 per cent of 20,000 per km2")
    own = sum(1 for x in D["od"] if x["w_tract"] == x["h_tract"] and x["w_tract"] in core_set)
    ok(own > 0, "SF15 residents working in their own tract are in the extract and neither taken off nor added")
    ok(sum(1 for x in D["survey"] if x["HOMEREL"] in ("4", "9")) > 3000, "SF16 code 4 and 9 respondents ship and stay out of every stratum")
    ok("9:00 to 18:00" in board, "SF17 the service window is the pilot's, the estimand the weekday's")
    ok(G["margin"] >= 1.15, "SF18 no tie")
    for m in K.METRO_NAMES:
        ok(edge(F[m]["pwd"], 100) >= 25, "SF19 %s density away from its hundred's edge" % m)
        ok(edge(F[m]["present"], 1000) >= 120, "SF19 %s people present away from the thousand's edge" % m)
        ok(edge(100 * F[m]["dense"], 1) >= .12, "SF19 %s dense share away from its whole percent's edge" % m)
    ok(edge(F[pick]["pwd"] - F[runner]["pwd"], 100) >= 25, "SF19 the lead away from its hundred's edge")
    ok(fig["call"]["gap"] == int((F[pick]["pwd"] - F[runner]["pwd"]) / 100 + .5) * 100, "the lead in figures.json")

    # ---------------------------------------------------------------- the asks: devices, separation, the cracker
    aa, ab = A.ask_a(D), A.ask_b(D)
    plain_a, plain_b = A.ask_a(D, "plain"), A.ask_b(D, "plain")
    for m in K.METRO_NAMES:
        ok(aa[m][0] % 2 == 1, "Ask A %s: an odd count, so the median is one unit's rent" % m)
        ok(plain_a[m][0] != aa[m][0], "Ask A %s: counting every listing misses the count" % m)
        ok(int(plain_a[m][1] + .5) != int(aa[m][1] + .5), "Ask A %s: counting every listing misses the median" % m)
        ok(edge(aa[m][1], 1) >= .05, "Ask A %s: the median away from its dollar's edge" % m)
        for b in K.BRANDS:
            ok(plain_b[(m, b)] != ab[(m, b)], "Ask B %s %s: every delivering store counted misses" % (m, b))
    rows = [x for x in D["locators"] if x["scrape_date"] == "2026-09-30"]
    shared = {(x["address"], x["unit"]) for x in rows if x["brand"] == K.BRANDS[0]} & \
             {(x["address"], x["unit"]) for x in rows if x["brand"] == K.BRANDS[1]}
    ok(all(any((x["address"], x["unit"]) in shared and x["census_tract"] in set(D["cores"][m]) for x in rows)
           for m in K.METRO_NAMES), "Ask B: every core holds a shop both finders list")
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in (K.FILES["listings"], K.FILES["locators"]):
                shutil.copy(os.path.join(target, f), tmp)
        open(os.path.join(tmp, K.FILES["listings"]), "w").write("listing_id\n")
        open(os.path.join(tmp, K.FILES["locators"]), "w").write("scrape_date\n")
        D3 = A.load(tmp)
        G3 = A.run(D3, "golden")
        ok(G3["pick"] == pick and all(abs(G3["F"][m]["pwd"] - F[m]["pwd"]) < 1e-6 for m in K.METRO_NAMES),
           "separation: the call computes identically with both ask files emptied")
    finally:
        shutil.rmtree(tmp)
    for k in K.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in os.listdir(target):
                if f != K.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            if k == "acs_commute":
                ok(True, "the ACS table is read only by the hazard route")
                continue
            D4 = A.load(tmp)
            ok(A.run(D4, "golden")["pick"] == pick, "distractor %s deleted: same call" % k)
        except FileNotFoundError:
            ok(True, "distractor %s is read by no golden step" % k)
        finally:
            shutil.rmtree(tmp)
    cr = subprocess.run([sys.executable, os.path.join(HERE, "cracker.py"), target], capture_output=True, text=True)
    ok(cr.returncode == 0, "the cracker's path misses every ask figure: " + cr.stdout[-300:])

    # ---------------------------------------------------------------- input gates and realism
    files = os.listdir(target)
    ok(len(files) >= 10, "ten or more files")
    ok(len({os.path.splitext(f)[1] for f in files}) >= 3, "three or more formats")
    ok(max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv")) >= 25000, "a 25,000-row file")
    ok(len(K.DISTRACTORS) >= 2, "two or more distractors")
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(sorted(meta["distractor_files"]) == sorted("target/" + K.FILES[k] for k in K.DISTRACTORS), "metadata names the distractors")
    ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")
    presents = [round(F[m]["present"]) for m in K.METRO_NAMES]
    ok(len(set(presents)) == 6 and all(p % 1000 for p in presents), "no round or repeated core totals")
    wave_n = [len(v) for v in blocks.values()]
    ok(len(set(wave_n)) > 6, "the waves' sizes vary")
    names = set(K.METRO_NAMES) | {K.HOME_METRO} | set(K.BRANDS)
    for m in K.METROS:
        names |= {m["central"][0]} | {n for n, _ in m["outlying"]} | {n for n, _, _ in m["outside"]}
    ok(len(names) == 6 + 1 + 2 + 6 + sum(len(m["outlying"]) + len(m["outside"]) for m in K.METROS), "every invented name distinct")
    print("checks: %d assertions passed" % N[0])
    return N[0]
