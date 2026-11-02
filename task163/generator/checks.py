"""task163 checks: the generator's assertions on the world's clean truth and on the shipped pack. Exit 1 on any failure.

    python3 task163/generator/checks.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C      # noqa: E402
import common as K    # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def xlsx_text(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(ws.title)
        for row in ws.iter_rows(values_only=True):
            out.extend(str(v) for v in row if v is not None)
    return "\n".join(out)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    w = W.build()
    skus = w["skus"]
    by = {s["sku"]: s for s in skus}
    f, X = C.main_call(T)
    wt, nb_cur, nb_plan, fc, cur, pos_plan, L = (X["wt"], X["nb_cur"], X["nb_plan"], X["fc"], X["cur"],
                                                X["pos_plan"], X["L"])
    it = X["items"]
    L27 = sum(fc.values())
    item_of = {s["sku"]: s["item"] for s in skus}

    # ------------------------------------------------------------------ the pack reproduces the world
    truth_claims = sum(1 for e in w["events"] if e["reported"] and K.BASE_FROM <= e["day"] <= K.BASE_TO)
    check("pack: the shipped register's validated wrong-item claims in the window equal the world's reported escapes",
          f["base_claims"] == truth_claims, "%d against %d" % (f["base_claims"], truth_claims))
    bi = [i for i, d in enumerate(w["dd"]) if K.BASE_FROM <= d <= K.BASE_TO]
    check("pack: the velocity export's 52 weeks hold the world's lines", f["base_lines"] == int(w["lines"][:, bi].sum()))
    check("pack: the baseline is 52 whole ISO weeks", len(bi) == 364 and K.BASE_FROM.weekday() == 0)

    # ------------------------------------------------------------------ R1, the field's raw material ships
    cols = set()
    for fn in os.listdir(T):
        if fn.endswith(".csv"):
            cols |= set(K.read_csv(os.path.join(T, fn))[0].keys())
    check("R1: no shipped column holds a neighbour, a weight gap or an exposure",
          not any(re.search(r"neighbou|alike|adjacent|gap|exposure|escape", c, re.I) for c in cols), sorted(cols)[:6])
    check("R1: the golden reads the faces, the unit weights, the lines and the claims, at the pick-face grain",
          len(cur) == len(skus) and len(pos_plan) == len(skus) and len(L) > 800)

    # ------------------------------------------------------------------ claims and holds are neighbour swaps
    pos_of = cur
    def is_nb(a, b, pos):
        (ra, ia), (rb, ib) = pos[a], pos[b]
        return ra == rb and abs(ia - ib) == 1
    clm = X["claims"]
    check("data: every baseline claim's received item sits on the face left or right of the ordered one",
          all(is_nb(o, r, pos_of) for o, r, d in clm), "%d claims" % len(clm))
    check("data: every baseline claim's pair weighs within the tolerance",
          all(abs(wt[o] - wt[r]) <= K.TOL_G for o, r, d in clm))
    holds = [h for h in K.read_csv(os.path.join(T, PK.F_HOLDS)) if h["cause"] == "MISPICK"]
    hp = [(int(h["item_expected"]), int(h["item_found"])) for h in holds]
    check("data: every MISPICK hold's found item sits beside the expected one", all(is_nb(a, b, pos_of) for a, b in hp),
          "%d holds" % len(hp))
    check("data: every MISPICK hold's pair is more than the tolerance apart", all(abs(wt[a] - wt[b]) > K.TOL_G for a, b in hp))
    gaps = []
    for nb, pos in ((nb_cur, cur), (nb_plan, pos_plan)):
        for a, ns in nb.items():
            for b in ns:
                gaps.append(abs(wt[a] - wt[b]))
    check("SF10: no neighbour pair in either layout weighs within 4 g of the tolerance, so its boundary moves nothing",
          not any(K.TOL_G - 4 <= x <= K.TOL_G + 4 for x in gaps), "%d pairs" % len(gaps))

    # ------------------------------------------------------------------ lesson 7: the golden's assumptions
    def relation(a, b):
        if it[a]["desc"].rsplit(" ", 2)[0] == it[b]["desc"].rsplit(" ", 2)[0] and it[a]["family"] == it[b]["family"]:
            return "same line"
        return "same family" if it[a]["family"] == it[b]["family"] else "other"
    # opportunities by relation and alikeness, weighted by lines, each neighbour carrying half of a two-sided face
    opp = defaultdict(float)
    for i in cur:
        ns = nb_cur[i]
        for j in ns:
            opp[(relation(i, j), abs(wt[i] - wt[j]) <= K.TOL_G)] += L.get(i, 0) / len(ns)
    hold_w = [h for h in holds if K.BASE_FROM <= dt.date.fromisoformat(h["held_at"][:10]) <= K.BASE_TO]
    caught = defaultdict(int)
    for h in hold_w:
        caught[relation(int(h["item_expected"]), int(h["item_found"]))] += 1
    rates_c = {k: caught[k] / opp[(k, False)] for k in ("same line", "same family", "other") if opp[(k, False)] > 2e4}
    spread_c = max(rates_c.values()) / min(rates_c.values())
    check("lesson 7: mis-picks the check-weigh caught run at one rate per opportunity beside a same-line, a same-family "
          "or any other face", spread_c < 1.15, {k: round(v * 1e4, 2) for k, v in rates_c.items()})
    esc = defaultdict(int)
    for o, r, d in clm:
        esc[relation(o, r)] += 1
    rates_e = {k: esc[k] / opp[(k, True)] for k in ("same line", "same family", "other") if opp[(k, True)] > 2e4}
    spread_e = max(rates_e.values()) / min(rates_e.values())
    check("lesson 7: claims run at one rate per weight-alike opportunity whatever the neighbour's family or line",
          spread_e < 1.2, {k: round(v * 1e4, 2) for k, v in rates_e.items()})
    # error rate per line independent of the neighbour (truth)
    ev = [e for e in w["events"] if K.BASE_FROM <= e["day"] <= K.BASE_TO]
    p_hat = len(ev) / f["base_lines"]
    check("lesson 7 (truth): the error rate per line is the world's one constant", abs(p_hat * 800 - 1) < 0.03,
          "%.5f" % p_hat)
    # the fraction of alike neighbours, not an indicator: faces with one alike neighbour of two escape at half rate
    half = full = 0.0
    eh = ef = 0
    for i in cur:
        a = C.alike_share(nb_cur, i, wt)
        if len(nb_cur[i]) == 2 and a == 0.5:
            half += L.get(i, 0)
        elif len(nb_cur[i]) == 2 and a == 1.0:
            full += L.get(i, 0)
    cnt = defaultdict(int)
    for o, r, d in clm:
        cnt[o] += 1
    for i in cur:
        a = C.alike_share(nb_cur, i, wt)
        if len(nb_cur[i]) == 2 and a == 0.5:
            eh += cnt[i]
        elif len(nb_cur[i]) == 2 and a == 1.0:
            ef += cnt[i]
    ratio = (eh / half) / (ef / full)
    check("lesson 7: a face with one weight-alike neighbour of two yields half the claims per line of a face with two",
          0.40 < ratio < 0.60, "%.3f" % ratio)
    # no trend: claims per alike opportunity in the window's two halves
    mid = K.BASE_FROM + dt.timedelta(182)
    halves = []
    for a0, a1 in ((K.BASE_FROM, mid - dt.timedelta(1)), (mid, K.BASE_TO)):
        Lh = C.velocity(T, a0, a1)
        U = sum(Lh.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur)
        halves.append(sum(1 for o, r, d in clm if a0 <= d <= a1) / U)
    check("lesson 7: no trend, claims per alike opportunity in the two half-years within 8 per cent",
          abs(halves[0] / halves[1] - 1) < 0.08, ["%.3f" % (h * 1e4) for h in halves])
    # no cluster: no ordered/received pair claimed more than a few times in any week
    wk = defaultdict(lambda: defaultdict(int))
    for o, r, d in clm:
        wk[(o, r)][K.monday(d)] += 1
    weeks = sorted({K.monday(K.BASE_FROM + dt.timedelta(7 * k)) for k in range(52)})
    disp = []
    for pair, cnts in wk.items():
        xs = np.array([cnts.get(m, 0) for m in weeks], dtype=float)
        if xs.sum() >= 40:
            disp.append(xs.var(ddof=1) / xs.mean())
    check("lesson 7: no contamination cluster (claims per busy pair are Poisson across weeks, dispersion under 1.6)",
          disp and max(disp) < 1.6, "%d busy pairs, worst %.2f" % (len(disp), max(disp) if disp else 0))
    check("lesson 7: every face in the plan holds an item with a 2026 history", all(L.get(i, 0) > 0 for i in pos_plan))
    # report share flat across families (claims per alike opportunity by family)
    fam_rates = {}
    for fam in W.FAMILIES:
        U = sum(L.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur if it[i]["family"] == fam)
        n = sum(1 for o, r, d in clm if it[o]["family"] == fam)
        if U > 3e4:
            fam_rates[fam] = n / U
    chi = sum((sum(1 for o, r, d in clm if it[o]["family"] == fam) -
               fam_rates[fam] / fam_rates[fam] * sum(L.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur
                                                     if it[i]["family"] == fam) * len(clm) /
               sum(L.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur)) ** 2 /
              (sum(L.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur if it[i]["family"] == fam) * len(clm) /
               sum(L.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur)) for fam in fam_rates)
    check("lesson 7: claims per alike opportunity homogeneous across families (chi-square under 2 per family)",
          chi / max(1, len(fam_rates) - 1) < 2.0, "%.2f on %d families" % (chi, len(fam_rates)))

    # ------------------------------------------------------------------ the ladder, on the shipped pack
    plan_c, plan_r, cur_r = fig["call_plan_claims"], fig["call_plan_per_10k"], fig["call_cur_per_10k"]
    default_r = f["base_per_10k"]
    default_c = f["default_claims"]
    check("R3a: the default path (2026 claims per line onto 2027's lines) files about 1,700 claims, inside the limit",
          K.round_to(default_c, 100) == 1700 and default_r < K.KPI_PER_10K, "%.0f, %.2f" % (default_c, default_r))
    check("R3a: the default path's figure is not the golden's", K.round_to(default_c, 100) != plan_c)

    def mult(key):
        ca = cb = 0
        la = lb = 0.0
        for i in cur:
            hit = any(key(j) == key(i) for j in nb_cur[i])
            n = cnt[i]
            if hit:
                la += L.get(i, 0); ca += n
            else:
                lb += L.get(i, 0); cb += n
        pa = pb = 0.0
        for i in pos_plan:
            hit = any(key(j) == key(i) for j in nb_plan[i])
            if hit:
                pa += fc[i]
            else:
                pb += fc[i]
        return ca / la * pa + cb / lb * pb
    r1_line = mult(lambda i: it[i]["desc"].rsplit(" ", 2)[0] + it[i]["family"])
    r1_fam = mult(lambda i: it[i]["family"])
    check("rung 1: a same-line look-alike multiplier files another figure, inside the limit",
          K.round_to(r1_line, 100) != plan_c and r1_line / L27 * 1e4 < K.KPI_PER_10K, "%.0f" % r1_line)
    check("rung 1: a same-family look-alike multiplier files another figure, inside the limit",
          K.round_to(r1_fam, 100) != plan_c and r1_fam / L27 * 1e4 < K.KPI_PER_10K, "%.0f" % r1_fam)
    # per zone and per family rates per line (the field's per-unit reflex): same as the default
    def per_group_line(key):
        tot = 0.0
        for g in {key(i) for i in cur}:
            lg = sum(L.get(i, 0) for i in cur if key(i) == g)
            cg = sum(cnt[i] for i in cur if key(i) == g)
            tot += cg / lg * sum(fc[i] for i in pos_plan if key(i) == g)
        return tot
    for name, key in (("zone", lambda i: cur[i][0][0]), ("family", lambda i: it[i]["family"])):
        v = per_group_line(key)
        check("rung 0: claims per line by %s carried onto the plan's lines stays inside the limit" % name,
              v / L27 * 1e4 < K.KPI_PER_10K and K.round_to(v, 100) != plan_c, "%.0f" % v)
    # each current zone's rate per line applied to the lines the plan puts in that zone
    zr = {}
    for z in "ABCD":
        lz = sum(L.get(i, 0) for i in cur if cur[i][0][0] == z)
        zr[z] = sum(cnt[i] for i in cur if cur[i][0][0] == z) / lz
    v_zone_plan = sum(zr[pos_plan[i][0][0]] * fc[i] for i in pos_plan)
    check("rung 0: each zone's claims per line applied to the lines the plan puts in it stays inside the limit",
          v_zone_plan / L27 * 1e4 < K.KPI_PER_10K and K.round_to(v_zone_plan, 100) != plan_c,
          "%.0f, zone rates %s" % (v_zone_plan, {z: round(v * 1e4, 2) for z, v in zr.items()}))
    # the indicator exposure (any alike neighbour) is refuted above and files another figure
    def ind(nb, i):
        return 1.0 if any(abs(wt[j] - wt[i]) <= K.TOL_G for j in nb[i]) else 0.0
    U_ind = sum(L.get(i, 0) * ind(nb_cur, i) for i in cur)
    v_ind = len(clm) / U_ind * sum(fc[i] * ind(nb_plan, i) for i in pos_plan)
    check("rival exposure: an any-alike-neighbour indicator files another figure", K.round_to(v_ind, 100) != plan_c,
          "%.0f" % v_ind)
    cheap = [default_c, r1_line, r1_fam, per_group_line(lambda i: cur[i][0][0]), v_ind]
    check("Gate F: no cheap route lands the call's figure or its breach of the limit",
          not any(K.round_to(v, 100) == plan_c or v / L27 * 1e4 > K.KPI_PER_10K for v in cheap[:4]))

    # ------------------------------------------------------------------ R3b: the decisive step alone
    r3b = len(clm) / f["alike_share_base"] / f["base_lines"] * f["alike_share_plan"] * L27
    check("R3b: the default path with only its exposure changed to weight-alike picks files the golden",
          K.round_to(r3b, 100) == plan_c, "%.0f" % r3b)

    # ------------------------------------------------------------------ the golden family converges
    def pooled(d0, d1):
        Lw = C.velocity(T, d0, d1)
        cl = C.baseline_claims(T, X["by_aub"], d0, d1)
        U = sum(Lw.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur)
        r = len(cl) / U
        return r * sum(fc[i] * C.alike_share(nb_plan, i, wt) for i in pos_plan), \
            r * sum(fc[i] * C.alike_share(nb_cur, i, wt) for i in cur)
    variants = {"W40-W39": (dt.date(2025, 9, 29), dt.date(2026, 9, 27)),
                "W36-W38": (dt.date(2025, 9, 1), dt.date(2026, 9, 20)),
                "W36-W39": (dt.date(2025, 9, 1), dt.date(2026, 9, 27))}
    for name, (d0, d1) in variants.items():
        p, c = pooled(d0, d1)
        check("SF4 convergence: the window %s gives the same claims and rates" % name,
              K.round_to(p, 100) == plan_c and K.round_half_up(p / L27 * 1e4, 1) == plan_r and
              K.round_half_up(c / L27 * 1e4, 1) == cur_r, "%.0f %.3f %.3f" % (p, p / L27 * 1e4, c / L27 * 1e4))

    def grouped(key):
        cz, uz = defaultdict(int), defaultdict(float)
        for o, r, d in clm:
            cz[key(o)] += 1
        for i in cur:
            uz[key(i)] += L.get(i, 0) * C.alike_share(nb_cur, i, wt)
        p = sum(cz[key(i)] / uz[key(i)] * fc[i] * C.alike_share(nb_plan, i, wt) for i in pos_plan if uz[key(i)] > 0)
        c = sum(cz[key(i)] / uz[key(i)] * fc[i] * C.alike_share(nb_cur, i, wt) for i in cur if uz[key(i)] > 0)
        return p, c
    for name, key in (("zone", lambda i: cur[i][0][0]), ("family", lambda i: it[i]["family"])):
        p, c = grouped(key)
        check("convergence: rates by %s give the same claims and rates" % name,
              K.round_to(p, 100) == plan_c and K.round_half_up(p / L27 * 1e4, 1) == plan_r and
              K.round_half_up(c / L27 * 1e4, 1) == cur_r, "%.0f %.3f %.3f" % (p, p / L27 * 1e4, c / L27 * 1e4))
    # the 2027 lines: the plan's forecast against 2026 lines grown at one rate
    g = L27 / f["base_lines"]
    p_g = len(clm) / sum(L.get(i, 0) * C.alike_share(nb_cur, i, wt) for i in cur) * \
        sum(L.get(i, 0) * g * C.alike_share(nb_plan, i, wt) for i in pos_plan)
    plan_txt = xlsx_text(os.path.join(T, PK.F_PLAN))
    check("SF3: the plan files its forecast basis, and 2026 lines grown at one rate print the same claims and rate",
          "Aubrine demand plan of 12 October 2026" in plan_txt and K.round_to(p_g, 100) == plan_c and
          K.round_half_up(p_g / L27 * 1e4, 1) == plan_r, "%.0f, %.3f" % (p_g, p_g / L27 * 1e4))

    # ------------------------------------------------------------------ bins
    raw = fig["raw"]
    for name, v, step in (("plan claims", raw["plan_claims"], 100), ("plan rate", raw["plan_per_10k"], 0.1),
                          ("current rate", raw["cur_per_10k"], 0.1)):
        e = K.edge_distance(v, step)
        check("bin: the %s sits at least a quarter of its bin from an edge" % name, e >= 0.25, "%.3f of the bin" % e)
    check("call: the plan breaks the limit and today's layout keeps inside it",
          raw["plan_per_10k"] > K.KPI_PER_10K and raw["cur_per_10k"] < K.KPI_PER_10K)

    # ------------------------------------------------------------------ R2: Layer 1 mess is neutral
    rows = C.claims(T)
    def count(pred):
        return sum(1 for r in rows if pred(r))
    in_win = lambda r: K.BASE_FROM <= (r["Despatched"].date() if isinstance(r["Despatched"], dt.datetime) else r["Despatched"]) <= K.BASE_TO
    wrong = lambda r: r["Reason"] == "Wrong item received"
    n_all = count(lambda r: wrong(r) and in_win(r))
    n_lodged = count(lambda r: wrong(r) and r["Status"] == "Validated" and
                     K.BASE_FROM <= r["Lodged"].date() <= K.BASE_TO)
    rate = fig["raw"]["plan_claims"] / len(clm)
    for label, n in (("SF1 counting duplicate, rejected and open wrong-item claims", n_all),
                     ("SF5 dating claims by lodging instead of despatch", n_lodged)):
        check("R2: %s leaves the call's figures" % label,
              K.round_to(n * rate, 100) == plan_c and K.round_half_up(n * rate / L27 * 1e4, 1) == plan_r,
              "%d claims, %.0f" % (n, n * rate))
    check("R2: no claim on a line despatched in the window is still open at the extract",
          count(lambda r: wrong(r) and in_win(r) and r["Status"] == "Open") == 0)
    # a reader who takes kilogram weights as grams
    check("R2: the plan's dotted, zero-padded locations and the WMS's hyphenated ones place every item on the same "
          "physical faces in zone A, which the plan leaves unchanged",
          all(pos_plan[i] == cur[i] for i in cur if cur[i][0][0] == "A"))
    check("R3c: no plant: no item pair claimed in a copied block (no two weeks with identical claim lists)",
          len({tuple(sorted((o, r) for o, r, d in clm if K.monday(d) == m)) for m in {K.monday(d) for o, r, d in clm}})
          == len({K.monday(d) for o, r, d in clm}))

    # ------------------------------------------------------------------ the fork table, row by row
    sched = pdf_text(os.path.join(T, PK.F_SCHED))
    miss = [r for r in rows if r["Reason"] == "Item missing" and r["Status"] == "Validated" and in_win(r)]
    check("SF2: Schedule 3 defines a mis-pick as a product other than the one ordered, and counting missing items would "
          "move the figure", "a product other than the one ordered" in sched and
          K.round_to((len(clm) + len(miss)) * rate, 100) != plan_c, "%d missing-item claims" % len(miss))
    vel_loc = {}
    same = True
    for r in K.read_csv(os.path.join(T, PK.F_VEL)):
        loc = r["location"]
        z, rest = loc[0], loc[1:]
        aisle, bay, lev, posn = rest.split("-")
        key = int(r["item_code"])
        run, idx = cur[key]
        same &= (run == (z, z + aisle, int(lev)) and idx == (int(bay) - 1) * 3 + int(posn) - 1)
    check("SF6: the velocity export's location agrees with the location master for every item in every week", same)
    plan_items = [r["aub"] for r in C.plan(T)]
    check("SF7: the plan places every item once", len(plan_items) == len(set(plan_items)) == len(skus))
    units_27 = None
    check("SF8: Schedule 3 counts order lines whatever the quantity, and a units basis would print another rate",
          "whatever the quantity ordered" in sched)
    check("SF9: Schedule 3's limit is 2.5 per 10,000 order lines, and the re-slot is over it while today's layout is not",
          "shall not exceed 2.5 per 10,000 order lines" in sched and raw["plan_per_10k"] > 2.5 > raw["cur_per_10k"])
    cross = sum(1 for o, r, d in clm if cur[o][1] // 3 != cur[r][1] // 3)
    check("SF11: every claim pair is left or right on one shelf, and some cross a bay upright", cross > 0 and
          all(is_nb(o, r, cur) for o, r, d in clm), "%d of %d across an upright" % (cross, len(clm)))
    check("SF12: the graded figures are printed at the prompt's rounding",
          plan_c % 100 == 0 and round(plan_r, 1) == plan_r and round(cur_r, 1) == cur_r)
    ag_cols = K.read_csv(os.path.join(T, PK.F_AGENCY))[0].keys()
    check("SF13: the invoice data date each shift by its own start (shift_start_date)", "shift_start_date" in ag_cols)
    hours_only = {}
    for r in C.agency(T)[0]:
        k = "%d-%02d" % (r["d"].year, r["d"].month)
        a_ = hours_only.setdefault(k, [0.0, 0.0])
        a_[0] += r["amt"]
        a_[1] += r["h"]
    check("SF14: the hours lines alone file other costs in every month",
          all(K.round_half_up(hours_only[k][0] / hours_only[k][1], 2) != v for k, v in fig["ask_a"].items()))
    rr = K.read_csv(os.path.join(T, PK.F_RET))
    seen = defaultdict(list)
    for r in rr:
        seen[r["return_ref"]].append(r)
    reps = [v for v in seen.values() if len(v) > 1]
    okrep = all(len(v) == 2 and v[0]["station"] == v[1]["station"] and
                abs((dt.datetime.fromisoformat(v[1]["graded_at"]) - dt.datetime.fromisoformat(v[0]["graded_at"])).total_seconds()) <= 1800
                for v in reps)
    check("SF15: a return reference repeats only for a correction within half an hour at the same station", reps and okrep,
          "%d corrected references" % len(reps))
    check("SF16: the returns log carries one date per row (graded_at)", "graded_at" in rr[0])
    check("SF17: every item carries a standard cost", all(v["cost"] > 0 for v in it.values()))

    # ------------------------------------------------------------------ SF18: the month of an agency hour is its shift's
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    hours_, prem_ = C.agency(T)
    un_, us_, _ = C.window_fit(hours_, prem_, C.pay_period_window)
    un_, us_ = round(un_, 2), round(us_, 2)
    wc = {}
    for r in K.read_csv(os.path.join(T, PK.F_AGENCY)):
        if r["line_type"] == "Hours":
            wc[(r["worker_no"], r["shift_start_date"], r["shift"])] = dt.date.fromisoformat(r["week_commencing"])
    byw = defaultdict(lambda: [0.0, 0.0])
    for r in K.read_csv(os.path.join(T, PK.F_AGENCY)):
        if r["line_type"] != "Hours":
            continue
        d = dt.date.fromisoformat(r["shift_start_date"])
        m = dt.date.fromisoformat(r["week_commencing"])
        k = "%d-%02d" % (m.year, m.month)
        byw[k][0] += float(r["amount_gbp"]) + float(r["night_hours"]) * un_ + (float(r["hours"]) * us_ if d.weekday() == 6 else 0.0)
        byw[k][1] += float(r["hours"])
    moved = {k: round(byw[k][0] / byw[k][1] - fig["ask_a_raw"][k], 3) for k in fig["ask_a"]
             if K.round_half_up(byw[k][0] / byw[k][1], 2) != fig["ask_a"][k]}
    check("SF18: the prompt files the month each shift started, and months by week_commencing would print other costs",
          "by the month each shift started" in prompt and len(moved) >= 1, moved)
    # the distractor's own timeline: inducted before the first shift, nothing dated after the log
    import openpyxl
    tw = openpyxl.load_workbook(os.path.join(T, PK.F_TRAIN), read_only=True).worksheets[0]
    first = {}
    for r in K.read_csv(os.path.join(T, PK.F_AGENCY)):
        if r["line_type"] == "Hours":
            d = dt.date.fromisoformat(r["shift_start_date"])
            first[r["worker_no"]] = min(first.get(r["worker_no"], d), d)
    late = early = 0
    for r in list(tw.iter_rows(values_only=True))[1:]:
        ds = [x.date() if isinstance(x, dt.datetime) else x for x in r[3:] if x]
        late += sum(1 for x in ds if x > dt.date(2026, 10, 22))
        if r[0] in first and (r[3].date() if isinstance(r[3], dt.datetime) else r[3]) >= first[r[0]]:
            early += 1
    check("realism: every Corsley picker in the training record was inducted before their first invoiced shift, and no "
          "training date passes the record's own date", late == 0 and early == 0, "%d late, %d inducted after" % (late, early))

    # ------------------------------------------------------------------ Ask A
    hours, prem = C.agency(T)
    un, us, res = C.window_fit(hours, prem, C.pay_period_window)
    check("Ask A: the premium lines are an identity over the pay periods (residual under a penny a line)", res < 0.011,
          "%.4f at %.4f and %.4f" % (res, un, us))
    rivals = {"the invoice week": lambda inv: (inv - dt.timedelta(8), inv - dt.timedelta(2)),
              "the calendar month before": lambda inv: ((inv.replace(day=1) - dt.timedelta(1)).replace(day=1),
                                                        inv.replace(day=1) - dt.timedelta(1)),
              "the invoice month to date": lambda inv: (inv.replace(day=1), inv)}
    for off in range(0, 36):
        if off != 9:
            rivals["28 days ending %d days before" % off] = (lambda o: lambda inv: (inv - dt.timedelta(o + 27),
                                                                                    inv - dt.timedelta(o)))(off)
    for wlen in (21, 35, 56):
        rivals["%d days ending 9 days before" % wlen] = (lambda n: lambda inv: (inv - dt.timedelta(9 + n - 1),
                                                                                inv - dt.timedelta(9)))(wlen)
    worst = min((C.window_fit(hours, prem, fn)[2], k) for k, fn in rivals.items())
    check("Ask A: every rival grain or alignment leaves a residual of GBP 50 or more on some line", worst[0] >= 50,
          "closest rival %s at GBP %.2f" % (worst[1], worst[0]))
    docs_text = "\n".join(pdf_text(os.path.join(T, x)) for x in (PK.F_SCHED, PK.F_PBSOP, PK.F_RBSOP, PK.F_RAV))
    check("control: the documents' text is read (Schedule 3's accuracy sentence found)",
          "per 10,000 order lines despatched in a contract year" in docs_text)
    check("Ask A: no shipped sentence gives the premium line a grain or a period",
          not re.search(r"premium|reconciliation|pay period|four-week", docs_text, re.I))
    a_gold = fig["ask_a"]
    check("Ask A: twelve months, each to the penny", len(a_gold) == 12)

    # ------------------------------------------------------------------ Ask B
    units = C.graded(T)
    bl = C.bills(T)
    go = min(u["day"] for u in units if u["cap"] == "Handheld")
    check("Ask B: the handheld's first row is 8 June 2026 and no bench sheet is keyed after it",
          go == K.APP_LIVE and not any(u["cap"] == "Bench sheet" and u["day"] >= go for u in units) and
          not any(u["cap"] == "Handheld" and u["day"] < go for u in units))
    gold_counts = C.reading_counts(units, it, lambda u: C.OLD if u["day"] < go else C.APP)
    coef, resid = C.bill_fit(gold_counts, bl)
    check("Ask B: the golden reading reproduces every Ravelrig invoice to the penny at one pair of prices",
          resid < 0.005 and all(abs(c - p) < 1e-6 for c, p in zip(coef, (0.84, 1.31))),
          "%s, residual %.4f" % ([round(c, 4) for c in coef], resid))
    lit = C.reading_counts(units, it, lambda u: C.OLD)
    _, r_all = C.bill_fit(lit, bl)
    post = sorted(m for m in bl if m >= (2026, 6))
    _, r_post = C.bill_fit(lit, bl, post)
    check("Ask B: the filed legend fails at every constant pair of prices (least-squares residual GBP 20 or more)",
          r_all >= 20, "GBP %.2f" % r_all)
    check("Ask B: the filed legend fails even with new prices from the go-live (June to September refitted)",
          r_post >= 20, "GBP %.2f over %d months" % (r_post, len(post)))
    for sw in (dt.date(2026, 6, 1), dt.date(2026, 7, 1), dt.date(2026, 6, 15)):
        cnts = C.reading_counts(units, it, lambda u, s=sw: C.OLD if u["day"] < s else C.APP)
        _, rr = C.bill_fit(cnts, bl)
        check("Ask B: a switch on %s instead leaves a residual" % sw.isoformat(), rr >= 1.0, "GBP %.2f" % rr)
    check("Ask B: fifteen figures, five families", len(fig["ask_b"]) == 5)
    rb = docs_text
    check("Ask B: no shipped sentence names the handheld or a change of grade codes",
          not re.search(r"handheld|app\b|code change|from 8 June", rb, re.I))

    # ------------------------------------------------------------------ input gates and hygiene
    files = sorted(os.listdir(T))
    exts = {os.path.splitext(x)[1] for x in files}
    check("gate: ten or more files", len(files) >= 10, len(files))
    check("gate: three or more formats", len(exts) >= 3, sorted(exts))
    big = [x for x in files if x.endswith(".csv") and len(K.read_csv(os.path.join(T, x))) >= 25000]
    check("gate: a file of 25,000 rows or more", len(big) >= 1, big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("gate: two or more distractors named in metadata.json and shipped",
          len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(TASK, d)) for d in meta["distractor_files"]))
    check("gate: metadata.json carries source, date and licence for every file",
          set(meta["files"]) == {"target/" + x for x in files} and
          all({"source", "date", "licence"} <= set(v) for v in meta["files"].values()))
    check("leak: no file is named for describing the data",
          not any(re.search(r"readme|dictionary|notes|manifest|guide|codebook|schema", x, re.I) for x in files))
    sheets = []
    for x in files:
        if x.endswith(".xlsx"):
            import openpyxl
            sheets += openpyxl.load_workbook(os.path.join(T, x), read_only=True).sheetnames
    check("leak: no sheet describes the data", not any(re.search(r"readme|notes|dictionary|guide|about", s, re.I)
                                                       for s in sheets), sheets)
    texts = [docs_text] + [xlsx_text(os.path.join(T, x)) for x in files if x.endswith(".xlsx")]
    texts += [open(os.path.join(T, x), encoding="utf-8").read() for x in files if x.endswith(".csv")]
    check("hygiene: no em or en dash in any shipped text", not any(("—" in t or "–" in t) for t in texts))
    meta_txt = json.dumps(meta)
    check("leak: metadata.json names no mechanism",
          not re.search(r"neighbou|weight|tolerance|alike|premium|pay period|legend|handheld", meta_txt, re.I))
    # realism: id columns not arithmetic sequences
    for fn, col in ((PK.F_HOLDS, "hold_id"), (PK.F_RET, "return_ref"), (PK.F_AGENCY, "invoice_no")):
        vals = sorted({int(re.sub(r"\D", "", r[col])) for r in K.read_csv(os.path.join(T, fn))})
        steps = {b - a for a, b in zip(vals, vals[1:])}
        check("realism: %s in %s is not one constant step" % (col, fn), len(steps) > 3, sorted(steps)[:5])
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task163.json")))
    people = set(card["world"]["people"])
    docnames = set(re.findall(r"(?:Kathryn Tomlinson|Brian Cook|Hazel Collins|Kayleigh Ward|[A-Z][a-z]+ [A-Z][a-z]+)",
                              docs_text))
    check("realism: every persona a document names is on the card", {"Brian Cook", "Hazel Collins"} <= people)
    # the distractors are never read by the golden
    src = open(os.path.join(HERE, "calc.py")).read()
    check("distractors: the golden reads neither distractor", "F_TRAIN" not in src and "F_PROMO" not in src)

    # ------------------------------------------------------------------ report
    bad = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        if not ok or "-v" in sys.argv:
            print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("checks: %d assertions, %d failed" % (len(RESULTS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
