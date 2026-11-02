"""Everything the golden needs, computed from the files under target/ alone: the survey households with their
equivalised 2027 incomes, each measure's eligibility and payments, the children each measure brings above the line
under every construction on the ladder, the claiming pace of newly entitled families and the decision lag read from
the Complemento register, and the three asks."""
import collections
import datetime as dt
import os
import re

import io_util as IO

FILES = {
    "households": "ecvv2026_households.csv",
    "persons": "ecvv2026_persons.csv",
    "fieldwork": "ecvv2026_fieldwork_cases.csv",
    "register": "cfv_register_extract_20261102.csv",
    "incidents": "cfv_incidents_2025.xlsx",
    "codes": "territorial_codes.csv",
    "guidance": "appraisal_guidance_child_poverty_2027.docx",
    "proposals": "child_poverty_proposals_2027.pdf",
    "rules": "complemento_familiar_rules_2026.pdf",
    "coverage": "complemento_familiar_coverage_2025.pdf",
    "results": "ecvv2026_main_results.pdf",
}
PROV_NAMES = {"81": "Valmesura", "82": "Las Cuencas", "83": "Sierra del Alba"}
_CACHE = {}


def p(target, key):
    return os.path.join(target, FILES[key])


# ---------------------------------------------------------------- the filed definitions, read from the documents
def filed(target):
    g = IO.docx_text(p(target, "guidance"))
    line = int(re.search(r"poverty line for 2027 is €([\d,]+) a year", g).group(1).replace(",", ""))
    uprate = 1 + float(re.search(r"increased by ([\d.]+) per cent", g).group(1)) / 100.0
    born_from = int(re.search(r"born in (\d{4}) or later", g).group(1))
    age_base = int(re.search(r"taken as (\d{4}) less the year of birth", g).group(1))
    pr = IO.pdf_text(p(target, "proposals"))
    table = pr[pr.index("A. Prestación Infancia Directa"):pr.index("Notes on the measures")]
    labels = ["A. Prestación Infancia Directa", "B. Ayuda a la Crianza", "C. Complemento Familiar: higher limit",
              "D. Suplemento de Alquiler con Hijos", "E. Complemento Familiar: higher amount"]
    seg = {}
    for i, lab in enumerate(labels):
        a = table.index(lab)
        b = table.index(labels[i + 1]) if i + 1 < len(labels) else len(table)
        seg[lab[0]] = table[a:b]
    a_rate = float(re.search(r"€(\d+) a month per child", seg["A"]).group(1))
    a_lim = float(re.search(r"returns was below €([\d,]+)", seg["A"]).group(1).replace(",", ""))
    b_rate = float(re.search(r"€(\d+) a month per child", seg["B"]).group(1))
    c_old, c_new = [float(x.replace(",", "")) for x in
                    re.search(r"from €([\d,]+) to €([\d,]+) of computable income", seg["C"]).groups()]
    d_rate = float(re.search(r"€(\d+) a month per child", seg["D"]).group(1))
    e_rate = float(re.search(r"€(\d+) a month more per child", seg["E"]).group(1))
    cv = IO.pdf_text(p(target, "coverage"))
    take_up = float(re.search(r"reached ([\d.]+) per cent of entitled families", cv).group(1)) / 100.0
    ru = IO.pdf_text(p(target, "rules"))
    cfv_rate = float(re.search(r"€(\d+) a month for each child under 18", ru).group(1))
    rise = re.search(r"raised the limit to €([\d,]+) from (\d+) (\w+) (\d{4})", ru)
    old_limit = float(re.search(r"with a limit of €([\d,]+) of computable income", ru).group(1).replace(",", ""))
    return {"line": line, "uprate": uprate, "born_from": born_from, "age_base": age_base, "A_rate": a_rate,
            "A_limit": a_lim, "B_rate": b_rate, "C_old": c_old, "C_new": c_new, "D_rate": d_rate, "E_rate": e_rate,
            "take_up": take_up, "cfv_rate": cfv_rate, "cfv_limit": float(rise.group(1).replace(",", "")),
            "cfv_old_limit": old_limit, "rise_date": dt.date(int(rise.group(4)), 4, int(rise.group(2)))}


# ---------------------------------------------------------------- the survey
def survey(target, F):
    hh_h, hh_r = IO.read_csv(p(target, "households"), delimiter=";")
    pe_h, pe_r = IO.read_csv(p(target, "persons"), delimiter=";")
    hi = {k: i for i, k in enumerate(hh_h)}
    pi = {k: i for i, k in enumerate(pe_h)}
    members = collections.defaultdict(list)
    for r in pe_r:
        members[r[pi["household_id"]]].append(int(r[pi["birth_year"]]))
    H = []
    for r in hh_r:
        hid = r[hi["household_id"]]
        births = members[hid]
        ages = [F["age_base"] - b for b in births]
        big = sorted([a for a in ages if a >= 14], reverse=True)
        small = [a for a in ages if a < 14]
        eq = (1.0 + 0.5 * (len(big) - 1) + 0.3 * len(small)) if big else (1.0 + 0.3 * (len(small) - 1))
        kids = sum(1 for b in births if b >= F["born_from"])
        disp = IO.uncomma(r[hi["disposable_income_2025"]])
        cfv = IO.uncomma(r[hi["complemento_familiar_2025"]]) or 0.0
        gross = IO.uncomma(r[hi["irpf_gross_income_2025"]])
        H.append({"hid": hid, "prov": r[hi["province"]], "w": IO.uncomma(r[hi["household_weight"]]), "eq": eq,
                  "kids": kids, "disp": disp, "cfv": cfv, "now": r[hi["complemento_familiar_now"]] == "1",
                  "filed": r[hi["irpf_return_2025"]] == "1", "gross": gross,
                  "renting": r[hi["tenure"]].startswith("rented"), "base27": disp * F["uprate"],
                  "comp_eq": (disp - cfv) / eq})
    return H


def pays(F):
    line = F["line"]
    return {
        "A": lambda h: 12 * F["A_rate"] * h["kids"] if (h["kids"] and h["filed"] and h["gross"] is not None
                                                        and h["gross"] < F["A_limit"]) else 0.0,
        "B": lambda h: 12 * F["B_rate"] * h["kids"] if (h["kids"] and h["comp_eq"] < line) else 0.0,
        "C": lambda h: 12 * F["cfv_rate"] * h["kids"] if (h["kids"] and F["C_old"] <= h["comp_eq"] < F["C_new"]
                                                          and not h["now"]) else 0.0,
        "D": lambda h: 12 * F["D_rate"] * h["kids"] if (h["kids"] and h["renting"] and h["comp_eq"] < line) else 0.0,
        "E": lambda h: 12 * F["E_rate"] * h["kids"] if (h["kids"] and h["now"]) else 0.0,
    }


CLAIMED = ("B", "C", "D")
AUTOMATIC = ("A", "E")


def lifted(h, line, pay):
    return h["base27"] / h["eq"] < line <= (h["base27"] + pay) / h["eq"]


def static(H, F, m, by_prov=False):
    f = pays(F)[m]
    out = collections.Counter()
    for h in H:
        x = f(h)
        if x and lifted(h, F["line"], x):
            out[h["prov"]] += h["w"] * h["kids"]
    return dict(out) if by_prov else sum(out.values())


# ---------------------------------------------------------------- the register
def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    y, m, d = s.split("-")
    return dt.date(int(y), int(m), int(d))


def parse_month(s):
    s = (s or "").strip()
    if not s:
        return None
    if "/" in s:
        m, y = s.split("/")
        return (int(y), int(m))
    y, m = s.split("-")
    return (int(y), int(m))


def mi(ym):
    return ym[0] * 12 + ym[1] - 1


def register(target):
    if ("reg", target) in _CACHE:
        return _CACHE[("reg", target)]
    h, rows = IO.read_csv(p(target, "register"), delimiter="|")
    ix = {k: i for i, k in enumerate(h)}
    out = []
    for r in rows:
        out.append({"case": r[ix["case_number"]], "fam": r[ix["family_number"]], "type": r[ix["claim_type"]],
                    "claim": parse_date(r[ix["claim_date"]]), "dec": parse_date(r[ix["decision_date"]]),
                    "res": r[ix["decision"]], "inc": IO.uncomma(r[ix["computable_income_per_eq_adult"]]),
                    "kids": int(r[ix["children"]]), "muni": r[ix["municipality"]], "prov": r[ix["province"]],
                    "first": parse_month(r[ix["first_month_paid"]]), "last": parse_month(r[ix["last_month_paid"]])})
    _CACHE[("reg", target)] = out
    return out


def final_decisions(reg):
    """Each case number's resolution with the latest decision date (an appeal replaces the decision it reviews)."""
    best = {}
    for r in reg:
        if r["dec"] is None:
            continue
        cur = best.get(r["case"])
        if cur is None or r["dec"] > cur["dec"]:
            best[r["case"]] = r
    return best


def granted_initial(reg):
    fin = final_decisions(reg)
    return [r for r in fin.values() if r["type"] == "INITIAL" and r["res"] == "GRANTED"]


def pace(claims, open_month, n_months):
    """Cumulative share of the claims made in the first n months after the window opened, by month."""
    cnt = collections.Counter(mi((c.year, c.month)) - mi(open_month) + 1 for c in claims)
    tot = sum(v for k, v in cnt.items() if 1 <= k <= n_months)
    out, acc = [], 0
    for k in range(1, n_months + 1):
        acc += cnt.get(k, 0)
        out.append(acc / tot)
    return out, tot


def paces(target, F):
    reg = register(target)
    gi = granted_initial(reg)
    single = collections.Counter(r["case"] for r in reg)
    rise = F["rise_date"]
    r0 = (rise.year, rise.month)
    widen_rows = [r for r in gi if F["cfv_old_limit"] <= r["inc"] < F["cfv_limit"] and r["claim"] >= rise]
    widen = [r["claim"] for r in widen_rows]
    last_month = (2026, 10)
    n24 = mi(last_month) - mi(r0) + 1
    c24, n_w = pace(widen, r0, n24)
    c24_30, _ = pace(widen, r0, n24 - 1)
    launch = [r["claim"] for r in gi if r["claim"] < rise and r["inc"] < F["cfv_old_limit"]]
    c22, n_l = pace(launch, (2022, 10), mi(r0) - mi((2022, 10)))
    c22_12, _ = pace(launch, (2022, 10), 12)
    c22all, _ = pace([r["claim"] for r in gi], (2022, 10), mi(last_month) - mi((2022, 10)) + 1)
    lag = collections.Counter(mi(r["first"]) - mi((r["claim"].year, r["claim"].month)) for r in gi
                              if single[r["case"]] == 1 and r["first"] is not None)
    nl = sum(lag.values())
    lagd = [(k, v / nl) for k, v in sorted(lag.items())]
    # the same widening cohort dated by its first month paid (the decision lag folded into the curve)
    fp = [dt.date(r["first"][0], r["first"][1], 1) for r in widen_rows if r["first"] is not None]
    c24_paid, _ = pace(fp, (r0[0], r0[1] + 1), n24 - 1)
    return {"widening": c24, "n_widening": n_w, "widening_30": c24_30, "widening_paid": c24_paid,
            "launch": c22, "n_launch": n_l, "launch_12": c22_12, "launch_all": c22all, "lag": lagd}


def months_received(curve, lag, mode="pace"):
    """Distribution of the months a measure pays in 2027 to its eventual claimants: claims made month by month
    along curve (mode 'pace'), all in January ('once'), evenly through the year ('even'), or with the curve
    already dated by first month paid ('paid'); each claim paid from the month after its decision."""
    d = collections.Counter()
    prev = 0.0
    for month in range(1, 13):
        if mode == "once":
            share = 1.0 if month == 1 else 0.0
        elif mode == "even":
            share = 1.0 / 12.0
        else:
            share = curve[month - 1] - prev
            prev = curve[month - 1]
        if share <= 0:
            continue
        if mode == "paid":
            d[13 - month] += share
            continue
        for k, pk in lag:
            d[max(0, 13 - month - k)] += share * pk
    d[0] += max(0.0, 1.0 - sum(d.values()))
    return d


def first_year(H, F, m, curve, lag, T, mode="pace", how="expect"):
    """Children a claimed measure brings above the line in 2027 when its eventual claimants (share T of the families
    it covers) claim along curve. how: 'expect' takes each household's chance of being lifted over its claim month
    and decision lag; 'avg' gives every claimant the average months paid; 'exppay' gives every covered household
    its expected payment; 'linear' scales the full-year count by the expected share of the year paid; 'fullyear'
    counts every claimant paid in 2027 as receiving the whole year (not the payments received)."""
    f = pays(F)[m]
    d = months_received(curve, lag, mode)
    paid = 1.0 - d.get(0, 0.0)
    em = sum(n * q for n, q in d.items())
    mbar = em / paid if paid else 0.0
    line = F["line"]
    tot = 0.0
    for h in H:
        x = f(h)
        if not x:
            continue
        wk = h["w"] * h["kids"]
        if how == "expect":
            tot += wk * T * sum(q for n, q in d.items() if n and lifted(h, line, x / 12.0 * n))
        elif how == "avg":
            tot += wk * T * paid if lifted(h, line, x / 12.0 * mbar) else 0.0
        elif how == "exppay":
            tot += wk if lifted(h, line, x * T * em / 12.0) else 0.0
        elif how == "linear":
            tot += wk * T * em / 12.0 if lifted(h, line, x) else 0.0
        elif how == "fullyear":
            tot += wk * T * paid if lifted(h, line, x) else 0.0
    return tot


def ladder(target):
    if ("lad", target) in _CACHE:
        return _CACHE[("lad", target)]
    F = filed(target)
    H = survey(target, F)
    PC = paces(target, F)
    T = F["take_up"]
    LAG = PC["lag"]
    S = {m: static(H, F, m) for m in ("A", "B", "C", "D", "E")}

    def run(curves, Tm=T, mode="pace", how="expect", modes=None):
        out = {}
        for m in S:
            if m in AUTOMATIC:
                out[m] = S[m]
            else:
                mm = (modes or {}).get(m, mode)
                out[m] = first_year(H, F, m, curves.get(m) if curves else None, LAG,
                                    Tm[m] if isinstance(Tm, dict) else Tm, mm, how)
        return out

    gold = {"B": PC["launch"], "C": PC["widening"], "D": PC["launch"]}
    R0 = S
    R1 = {m: (T * S[m] if m in CLAIMED else S[m]) for m in S}
    R1b = run(None, mode="once")
    R2 = run({m: PC["launch"] for m in CLAIMED})
    R2e = run(None, mode="even")
    R3 = run(gold)
    band = sum(h["w"] for h in H if h["kids"] and F["cfv_old_limit"] <= h["comp_eq"] < F["cfv_limit"])
    t_w = min(0.95, PC["n_widening"] / band)
    licensed = {
        "golden: each household's chance over claim month and lag": R3,
        "every claimant given the average months paid": run(gold, how="avg"),
        "every covered household given its expected payment": run(gold, how="exppay"),
        "full-year count scaled by the expected share of the year paid": run(gold, how="linear"),
        "widening pace for every claimed measure": run({m: PC["widening"] for m in CLAIMED}),
        "launch pace normalised to its first twelve months for B and D": run(dict(gold, B=PC["launch_12"],
                                                                                  D=PC["launch_12"])),
        "widening pace through September 2026 only": run(dict(gold, C=PC["widening_30"])),
        "widening cohort dated by first month paid": run(dict(gold, C=PC["widening_paid"]),
                                                         modes={"C": "paid"}),
        "every entitled family claims eventually": run(gold, Tm=1.0),
        "eventual share from the widening cohort itself": run(gold, Tm=t_w),
    }
    wrong = {
        "R0 every covered family paid all year": R0,
        "R1 all-year payments at the coverage rate": R1,
        "R1b every claim in January, paid after its decision": R1b,
        "R2 claims at the launch's pace": R2,
        "R2 claims spread evenly through 2027": R2e,
        "launch pace, average months paid": run({m: PC["launch"] for m in CLAIMED}, how="avg"),
        "launch pace, expected payment": run({m: PC["launch"] for m in CLAIMED}, how="exppay"),
        "launch pace, linear share of the year": run({m: PC["launch"] for m in CLAIMED}, how="linear"),
        "even spread, expected payment": run(None, mode="even", how="exppay"),
        "golden paces, claimants counted as paid all year": run(gold, how="fullyear"),
        "full-year count at the coverage rate times 0.50": {m: (R1[m] * 0.5 if m in CLAIMED else S[m]) for m in S},
        "full-year count at the coverage rate times 0.75": {m: (R1[m] * 0.75 if m in CLAIMED else S[m]) for m in S},
    }
    misspecified = {
        "all initial claims since launch, normalised to every claim to date": run({m: PC["launch_all"]
                                                                                  for m in CLAIMED}),
    }
    out = {"F": F, "H": H, "paces": PC, "T": T, "R0": R0, "R1": R1, "R1b": R1b, "R2": R2, "R2e": R2e, "R3": R3,
           "licensed": licensed, "wrong": wrong, "misspecified": misspecified,
           "A_by_prov": static(H, F, "A", by_prov=True)}
    _CACHE[("lad", target)] = out
    return out


# ---------------------------------------------------------------- the asks
QUARTER_ENDS = [(2025, 3), (2025, 6), (2025, 9), (2025, 12)]
CUTOFF = dt.date(2025, 12, 31)


def incidents(target):
    out = []
    for sh in IO.sheet_names(p(target, "incidents")):
        hdr, rows = IO.read_xlsx(p(target, "incidents"), sh)
        ix = {k: i for i, k in enumerate(hdr)}
        for r in rows:
            d = r[ix["Date"]]
            if isinstance(d, dt.datetime):
                d = d.date()
            out.append({"date": d, "fam": r[ix["Family"]], "case": r[ix["Case"]], "type": r[ix["Incident"]],
                        "detail": "" if r[ix["Detail"]] is None else str(r[ix["Detail"]])})
    return out


def ask_families(target):
    """Families the Complemento was paying for each quarter's last month of 2025, as its decisions stood at 31
    December 2025, by the province the family lived in that month. An award whose status now reads REVOKED stood
    granted at the cut-off when its revocation was decided later."""
    reg = register(target)
    codes = territorial(target)
    revoked_on = {}
    for r in reg:
        if r["type"] == "REVOCATION" and r["dec"] is not None:
            revoked_on[r["case"]] = min(r["dec"], revoked_on.get(r["case"], r["dec"]))
    moves = collections.defaultdict(list)
    for r in incidents(target):
        if r["type"] == "Change of address":
            moves[r["fam"]].append((r["date"], r["detail"]))
    out = {}
    for ym in QUARTER_ENDS:
        m = mi(ym)
        fams = {}
        for r in reg:
            if r["type"] == "REVOCATION" or r["first"] is None or r["dec"] is None or r["dec"] > CUTOFF:
                continue
            if r["res"] == "GRANTED":
                last = r["last"]
            elif r["res"] == "REVOKED" and r["case"] in revoked_on:
                if revoked_on[r["case"]] <= CUTOFF:
                    v = revoked_on[r["case"]]
                    last = (v.year, v.month)
                else:
                    last = r["last"]
            else:
                continue
            if mi(r["first"]) <= m and (last is None or mi(last) >= m):
                prev = fams.get(r["fam"])
                if prev is None or r["dec"] > prev["dec"]:
                    fams[r["fam"]] = r
        cnt = collections.Counter()
        for fam, r in fams.items():
            muni = r["muni"]
            for d, new in sorted(moves.get(fam, [])):
                if mi((d.year, d.month)) + 1 <= m:
                    muni = new
            cnt[codes[muni]] += 1
        out[ym] = dict(cnt)
    return out


def territorial(target):
    h, rows = IO.read_csv(p(target, "codes"))
    ix = {k: i for i, k in enumerate(h)}
    return {r[ix["municipality_code"]]: r[ix["province_code"]] for r in rows}


NOT_ELIGIBLE = ("empty dwelling", "not a dwelling", "address not found")


def ask_fieldwork(target):
    """Eligible sample dwellings, complete interviews and the response rate by the province the dwelling is in. A
    dwelling is its municipality and serial in the dwelling register (its census section was renumbered for cases
    issued from April 2026); a dwelling issued twice counts once, with the result of its last issue."""
    h, rows = IO.read_csv(p(target, "fieldwork"))
    ix = {k: i for i, k in enumerate(h)}
    codes = territorial(target)
    last = {}
    for r in rows:
        ref = r[ix["dwelling"]]
        key = (ref.split("-")[0], ref.split("-")[2])
        iss = int(r[ix["issue"]])
        if key not in last or iss > last[key][0]:
            last[key] = (iss, r[ix["result"]])
    out = {}
    for (muni, _), (iss, res) in last.items():
        e = out.setdefault(codes[muni], [0, 0])
        if res not in NOT_ELIGIBLE:
            e[0] += 1
            if res == "complete interview":
                e[1] += 1
    return {pc: (v[0], v[1], round(100.0 * v[1] / v[0], 1), 100.0 * v[1] / v[0]) for pc, v in out.items()}


# ---------------------------------------------------------------- the golden
def round_to(x, unit):
    return int(unit * round(x / unit))


def golden(target):
    L = ladder(target)
    R3 = L["R3"]
    call = max(R3, key=lambda m: R3[m])
    A_tot = L["R0"]["A"]
    G = {"call": call, "A_total": A_tot, "A_total_r": round_to(A_tot, 100),
         "A_by_prov": {pc: L["A_by_prov"].get(pc, 0.0) for pc in PROV_NAMES},
         "A_by_prov_r": {pc: round_to(L["A_by_prov"].get(pc, 0.0), 100) for pc in PROV_NAMES},
         "families": ask_families(target), "fieldwork": ask_fieldwork(target),
         "ladder": L}
    return G
