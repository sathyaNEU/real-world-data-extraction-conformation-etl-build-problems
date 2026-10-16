"""Every figure from the shipped files alone: the accrual (the golden), the default path and every rival, the
constructions that must round alike, the bootstrap, and the two asks. Reads only <target>; never the world."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os
import re
from collections import defaultdict
from statistics import NormalDist

import numpy as np
import openpyxl

NORM = NormalDist()
SLOTS = range(1, 10)
MIN_DAYS = {"7-day": 7, "10-day": 10, "15-day": 15, "60-day": 60}


# ------------------------------------------------------------------------------------------------------------ loading
def pdf_text(path):
    from pdfminer.high_level import extract_text
    return extract_text(path)


def read_csv(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def mdy(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date() if s else None


def ymd(s):
    return dt.date.fromisoformat(s) if s else None


def fold(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


class Pack:
    pass


def load(target, mishandle=()):
    """The shipped files read into one shape. `mishandle` names Layer 1 items handled the wrong way (for the R2
    neutrality checks): 'no_ci' plate appearances without catcher's interference in the legacy layout; 'subs_as_starts'
    every platform line a start; 'dh_once' one start a date (doubleheaders merged)."""
    P = Pack()
    P.target = target
    f = lambda n: os.path.join(target, n)
    xw = read_csv(f("lsf_player_id_crosswalk.csv"))
    P.legacy_to_id = {r["legacy_id"]: int(r["player_id"]) for r in xw}
    P.xwalk_name = {int(r["player_id"]): "%s %s" % (r["first_name"], r["last_name"]) for r in xw}
    clubs = read_csv(f("league_club_directory.csv"))
    P.legacy_club = {r["legacy_code"]: r["abbrev"] for r in clubs}
    P.team_club = {int(r["team_id"]): r["abbrev"] for r in clubs}
    P.season = {}
    if os.path.exists(f("league_calendar_2021_2027.csv")):
        cal = read_csv(f("league_calendar_2021_2027.csv"))
        P.season = {int(r["season"]): (ymd(r["opening_day"]), ymd(r["last_scheduled_day"])) for r in cal}
    # batting lines in one shape: season, game key, date, club, player, slot, starter, plate appearances, position
    lines = []
    comps = ("AB", "BB", "HBP", "SH", "SF") if "no_ci" in mishandle else ("AB", "BB", "HBP", "SH", "SF", "CI")
    for r in read_csv(f("lsf_batting_2021_2024.txt"), delimiter="|"):
        d = mdy(r["GAME_DT"])
        pa = sum(int(r[c]) for c in comps)
        lines.append((d.year, r["GAME_ID"], d, P.legacy_club[r["TEAM_CD"]], P.legacy_to_id[r["PLAYER_CD"]],
                      int(r["LINEUP"]), r["SEQ"] == "1", pa, int(r["POS"])))
    posmap = {"C": 2, "1B": 3, "2B": 4, "3B": 5, "SS": 6, "LF": 7, "CF": 8, "RF": 9, "DH": 10, "PH": 11, "P": 1}
    for r in read_csv(f("lsf_batting_2025_2026.csv")):
        d = ymd(r["official_date"])
        bo = int(r["batting_order"])
        start = True if "subs_as_starts" in mishandle else bo % 100 == 0
        lines.append((d.year, r["game_pk"], d, P.team_club[int(r["team_id"])], int(r["player_id"]), bo // 100,
                      start, int(r["pa"]), posmap[r["position"]]))
    if "dh_once" in mishandle:
        seen, kept = set(), []
        for ln in lines:
            if ln[6]:
                key = (ln[2], ln[4])
                if key in seen:
                    continue
                seen.add(key)
            kept.append(ln)
        lines = kept
    P.lines = lines
    # the vendor's winter depth charts
    wb = openpyxl.load_workbook(f("hvbd_winter_depth_charts_2021_2026.xlsx"), read_only=True)
    P.plan = []
    for ws in wb.worksheets:
        y = int(ws.title.split()[-1])
        hdr = None
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Tm":
                hdr = list(row)
                continue
            if hdr and row and row[0]:
                d = dict(zip(hdr, row))
                P.plan.append(dict(season=y, team=d["Tm"], role=d["Role"], ord=d["Ord"], pos=d["Pos"], name=d["Player"],
                                   lg=int(d["LG_ID"]), age=int(d["Age"])))
    # the club's 2027 depth chart
    wb = openpyxl.load_workbook(f("ral_depth_chart_2027.xlsx"), read_only=True)
    ws = wb.worksheets[0]
    P.lineup27 = {}
    mode = None
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Lineup":
            mode = "lineup"
            continue
        if row and row[0] in ("Bench", "Rotation", "Bullpen"):
            mode = None
        if mode == "lineup" and row and isinstance(row[0], int):
            P.lineup27[row[2]] = (row[0], row[1])
    # the term sheets
    P.terms = term_sheets(f("term_sheets_2027_free_agent_hitters.pdf"))
    P.proj = read_csv(f("hvbd_hitter_projections_2022_2027.csv")) if os.path.exists(
        f("hvbd_hitter_projections_2022_2027.csv")) else []
    return P


def term_sheets(path):
    txt = " ".join(pdf_text(path).split())
    heads = list(re.finditer(r"([A-Z][^()]{2,40}?) \((\w+), bats (\w), born ([A-Za-z]+ \d+, \d{4})\)", txt))
    out = {}
    for i, m in enumerate(heads):
        seg = txt[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(txt)]
        name = m.group(1).split("Salary ")[-1].strip()
        signed = re.search(r"([A-Z][a-z]+ \d+, \d{4})", seg).group(1)
        b = re.search(r"2027 season: \$([\d,]+) each for ([\d, and]+?) plate appearances", seg)
        amt = int(b.group(1).replace(",", ""))
        ts = [int(x) for x in re.findall(r"\d+", b.group(2))]
        out[name] = dict(pos=m.group(2), signed=dt.datetime.strptime(signed, "%B %d, %Y").date(),
                         born=dt.datetime.strptime(m.group(4), "%B %d, %Y").date(), lines=[(amt, t) for t in ts])
    return out


# --------------------------------------------------------------------------------------------------- season tables
def seasons(P):
    """Starts and plate appearances by player and season (every club), slot rates, and the planned regulars."""
    T = Pack()
    T.starts = defaultdict(int)
    T.pa = defaultdict(int)
    T.start_pa = defaultdict(int)
    T.slot_pa = defaultdict(int)
    T.slot_n = defaultdict(int)
    T.first_game = {}
    T.pos_starts = defaultdict(lambda: defaultdict(int))
    T.club_starts = defaultdict(lambda: defaultdict(int))
    for (y, g, d, club, pid, slot, st, pa, pos) in P.lines:
        T.pa[(y, pid)] += pa
        if st:
            T.starts[(y, pid)] += 1
            T.start_pa[(y, pid)] += pa
            T.slot_pa[(y, slot)] += pa
            T.slot_n[(y, slot)] += 1
            key = (y, club)
            if key not in T.first_game or (d, g) < T.first_game[key][0]:
                T.first_game[key] = ((d, g), [])
            T.pos_starts[(y, club, pos)][pid] += 1
            T.club_starts[(y, club)][pid] += 1
    T.opening = set()
    for (y, g, d, club, pid, slot, st, pa, pos) in P.lines:
        if st and T.first_game[(y, club)][0] == (d, g) and pos != 2:
            T.opening.add((y, pid))
    T.years = sorted({k[0] for k in T.starts})
    T.planned = [r for r in P.plan if r["role"] == "Lineup"]
    return T


def rate(T, years=None):
    years = years or T.years
    return {s: sum(T.slot_pa[(y, s)] for y in years) / sum(T.slot_n[(y, s)] for y in years) for s in SLOTS}


def planned_starts(T, catchers=False, years=None, ages=None):
    rows = [r for r in T.planned if (catchers or r["pos"] != "C") and (years is None or r["season"] in years)
            and (ages is None or ages[0] <= r["age"] <= ages[1])]
    return np.array([T.starts[(r["season"], r["lg"])] for r in rows], float), rows


def five(P):
    """The five signings: name, terms, new slot (2027 depth chart), league ID and old slot (the vendor's last winter
    chart, 2026)."""
    out = []
    last = max(r["season"] for r in P.plan)
    for name, t in P.terms.items():
        slot, pos = P.lineup27[name]
        prior = [r for r in P.plan if r["name"] == name and r["season"] == last and r["role"] == "Lineup"]
        lg = prior[0]["lg"] if prior else [r for r in P.plan if r["name"] == name][-1]["lg"]
        old = prior[0]["ord"] if prior else None
        age27 = 2027 - t["born"].year - (1 if (t["born"].month, t["born"].day) > (7, 1) else 0)
        out.append(dict(name=name, lines=t["lines"], slot=slot, pos=pos, lg=lg, old=old, age=age27, signed=t["signed"]))
    out.sort(key=lambda x: x["signed"])
    return out


def ev(lines, sample):
    """Expected amount of a set of bonus lines over a sample of season plate-appearance totals."""
    sample = np.asarray(sample, float)
    return sum(a * float(np.mean(sample >= T)) for a, T in lines)


def ev_normal(lines, mu, sd):
    return sum(a * (1 - NORM.cdf((T - mu) / sd)) for a, T in lines)


def ev_point(lines, x):
    return sum(a * float(x >= T) for a, T in lines)


def r250(x):
    return int(round(x / 250000.0)) * 250000


def r100(x):
    return int(round(x / 100000.0)) * 100000


# -------------------------------------------------------------------------------------------------------- the call
def golden(P, T=None):
    T = T or seasons(P)
    F = five(P)
    rt = rate(T)
    st, _ = planned_starts(T)
    per = {f["name"]: ev(f["lines"], st * rt[f["slot"]]) for f in F}
    lines = {f["name"]: [(a, Tt, float(np.mean(st * rt[f["slot"]] >= Tt))) for a, Tt in f["lines"]] for f in F}
    tot = sum(per.values())
    return dict(per=per, total=tot, total_r=r250(tot), per_r={k: r100(v) for k, v in per.items()}, lines=lines,
                rate=rt, n=len(st), five=F, starts=st)


def vendor_errors(P, T):
    """The vendor's past misses: actual season plate appearances less the preseason projection, for the regulars in
    its winter depth charts (2022 to 2026)."""
    planned = {(r["season"], r["lg"]) for r in T.planned if r["pos"] != "C"}
    errs = []
    for r in P.proj:
        y = int(r["season"])
        if y > 2026:
            continue
        key = (y, int(r["lg_id"]))
        if key in planned:
            errs.append(T.pa[key] - int(r["pa"]))
    return np.array(errs, float)


def rivals(P, T=None):
    T = T or seasons(P)
    G = golden(P, T)
    F = G["five"]
    rt = G["rate"]
    st = G["starts"]
    m, s = st.mean(), st.std()
    out = {}
    own = {f["name"]: np.array([T.pa[(y, f["lg"])] for y in (2024, 2025, 2026)], float) for f in F}
    sdp = float(np.std(np.array([T.pa[(r["season"], r["lg"])] for r in T.planned if r["pos"] != "C"], float)))
    if P.proj:
        proj27 = {int(r["lg_id"]): int(r["pa"]) for r in P.proj if r["season"] == "2027"}
        errs = vendor_errors(P, T)
        sdp = errs.std()
        out["vendor point"] = sum(ev_point(f["lines"], proj27[f["lg"]]) for f in F)
        out["default: vendor projection with a normal band"] = sum(ev_normal(f["lines"], proj27[f["lg"]], sdp) for f in F)
        out["vendor projection with its past misses"] = sum(ev(f["lines"], proj27[f["lg"]] + errs) for f in F)
        out["vendor projection rescaled to the new slot, normal band"] = sum(
            ev_normal(f["lines"], proj27[f["lg"]] * rt[f["slot"]] / rt[f["old"]], sdp) for f in F)
    out["own three seasons as the draws"] = sum(ev(f["lines"], own[f["name"]]) for f in F)
    out["own three-season mean, normal band"] = sum(ev_normal(f["lines"], own[f["name"]].mean(), sdp) for f in F)
    out["own seasons' starts at the new slot"] = sum(
        ev(f["lines"], np.array([T.starts[(y, f["lg"])] for y in (2024, 2025, 2026)]) * rt[f["slot"]]) for f in F)
    out["regulars at the old slot's rate"] = sum(ev(f["lines"], st * rt[f["old"]]) for f in F)
    out["old slot, normal band"] = sum(ev_normal(f["lines"], rt[f["old"]] * m, rt[f["old"]] * s) for f in F)
    out["new slot, normal band"] = sum(ev_normal(f["lines"], rt[f["slot"]] * m, rt[f["slot"]] * s) for f in F)
    out["new slot at the mean starts"] = sum(ev_point(f["lines"], rt[f["slot"]] * m) for f in F)
    out["new slot at the median starts"] = sum(ev_point(f["lines"], rt[f["slot"]] * np.median(st)) for f in F)
    p = m / 162.0
    out["new slot, starts game by game"] = sum(
        sum(a * (1 - NORM.cdf((Tt / rt[f["slot"]] - 0.5 - 162 * p) / np.sqrt(162 * p * (1 - p)))) for a, Tt in f["lines"])
        for f in F)
    stc, _ = planned_starts(T, catchers=True)
    out["catchers kept in"] = sum(ev(f["lines"], stc * rt[f["slot"]]) for f in F)
    od = np.array([T.starts[k] for k in sorted(T.opening)], float)
    out["opening-day lineups"] = sum(ev(f["lines"], od * rt[f["slot"]]) for f in F)
    _, rows = planned_starts(T)
    opened = np.array([T.starts[(r["season"], r["lg"])] for r in rows if (r["season"], r["lg"]) in T.opening], float)
    out["planned regulars who opened the season"] = sum(ev(f["lines"], opened * rt[f["slot"]]) for f in F)
    nonc = hitters_nonc(P, T)
    for th in (100,):
        d = np.array([T.starts[k] for k in nonc if T.starts[k] >= th], float)
        out["hitters with %d or more starts" % th] = sum(ev(f["lines"], d * rt[f["slot"]]) for f in F)
    for th in (400, 502):
        d = np.array([T.starts[k] for k in nonc if T.pa[k] >= th], float)
        out["hitters with %d or more plate appearances" % th] = sum(ev(f["lines"], d * rt[f["slot"]]) for f in F)
    pas = np.array([T.pa[(r["season"], r["lg"])] for r in rows], float)
    out["planned regulars' own plate appearances"] = sum(ev(f["lines"], pas) for f in F)
    # every appearance taken as a start (plate appearances per appearance at the slot, appearances for starts)
    Ta = seasons(_every_line_a_start(P))
    rta = rate(Ta)
    sta, _ = planned_starts(Ta)
    out["plate appearances per appearance, appearances for starts"] = sum(ev(f["lines"], sta * rta[f["slot"]]) for f in F)
    return out, G


def _every_line_a_start(P):
    Q = Pack()
    Q.__dict__.update(P.__dict__)
    Q.lines = [ln[:6] + (True,) + ln[7:] for ln in P.lines]
    return Q


def hitters_nonc(P, T):
    """Every non-catcher hitter-season in the box scores (a player's most common position not catcher)."""
    posc = defaultdict(lambda: defaultdict(int))
    for (y, g, d, club, pid, slot, st, pa, pos) in P.lines:
        if st:
            posc[(y, pid)][pos] += 1
    return sorted(k for k, d in posc.items() if max(d, key=d.get) != 2)


def constructions(P, T=None):
    """Constructions of the golden method that must round alike (C1): windows, slot-rate windows, ages, plate
    appearances rescaled or kept at the slot, and the loose regular definitions that select almost the same seasons."""
    T = T or seasons(P)
    G = golden(P, T)
    F = G["five"]
    rt = G["rate"]
    out = {}
    for y0 in (2022, 2023, 2024, 2025):
        st, _ = planned_starts(T, years=set(range(y0, 2027)))
        out["seasons from %d" % y0] = {f["name"]: ev(f["lines"], st * rt[f["slot"]]) for f in F}
    st = G["starts"]
    for ys in ((2024, 2025, 2026), (2025, 2026)):
        r2 = rate(T, list(ys))
        out["slot rates %d-%d" % (ys[0], ys[-1])] = {f["name"]: ev(f["lines"], st * r2[f["slot"]]) for f in F}
    _, rows = planned_starts(T)
    ages = np.array([r["age"] for r in rows])
    for w in (2, 3):
        out["ages within %d" % w] = {f["name"]: ev(f["lines"], st[np.abs(ages - f["age"]) <= w] * rt[f["slot"]]) for f in F}
    out["ages 30 to 34"] = {f["name"]: ev(f["lines"], st[(ages >= 30) & (ages <= 34)] * rt[f["slot"]]) for f in F}
    slot_of = np.array([r["ord"] for r in rows])
    pas = np.array([T.pa[(r["season"], r["lg"])] for r in rows], float)
    spas = np.array([T.start_pa[(r["season"], r["lg"])] for r in rows], float)
    sr = np.array([rt[int(q)] for q in slot_of])
    out["own plate appearances rescaled to the new slot"] = {f["name"]: ev(f["lines"], pas * rt[f["slot"]] / sr) for f in F}
    out["starting plate appearances rescaled"] = {f["name"]: ev(f["lines"], spas * rt[f["slot"]] / sr) for f in F}
    out["regulars planned at the new slot"] = {f["name"]: ev(f["lines"], pas[slot_of == f["slot"]]) for f in F}
    own = rate_of_club(P, "RAL")
    out["the club's own plate appearances per start"] = {f["name"]: ev(f["lines"], st * own[f["slot"]]) for f in F}
    top = []
    for (y, club, pos), d in T.pos_starts.items():
        if pos in (2, 11):
            continue
        top.append(T.starts[(y, max(sorted(d), key=lambda q: d[q]))])
    out["most starts at each position"] = {f["name"]: ev(f["lines"], np.array(top) * rt[f["slot"]]) for f in F}
    top8 = []
    for (y, club), d in T.club_starts.items():
        ks = sorted(d, key=lambda q: (-d[q], q))
        ks = [q for q in ks if q not in catchers_of(P, T, y, club)][:8]
        top8 += [T.starts[(y, q)] for q in ks]
    out["eight non-catchers with most starts per club"] = {f["name"]: ev(f["lines"], np.array(top8) * rt[f["slot"]]) for f in F}
    nonc = hitters_nonc(P, T)
    d81 = np.array([T.starts[k] for k in nonc if T.starts[k] >= 81], float)
    out["hitters with 81 or more starts"] = {f["name"]: ev(f["lines"], d81 * rt[f["slot"]]) for f in F}
    d300 = np.array([T.starts[k] for k in nonc if T.pa[k] >= 300], float)
    out["hitters with 300 or more plate appearances"] = {f["name"]: ev(f["lines"], d300 * rt[f["slot"]]) for f in F}
    return out, G


def rate_of_club(P, club):
    sp, sn = defaultdict(int), defaultdict(int)
    for (y, g, d, c, pid, slot, st, pa, pos) in P.lines:
        if st and c == club:
            sp[slot] += pa
            sn[slot] += 1
    return {s: sp[s] / sn[s] for s in SLOTS}


_CATCHERS = {}


def catchers_of(P, T, y, club):
    if not _CATCHERS:
        posc = defaultdict(lambda: defaultdict(int))
        for (yy, g, d, c, pid, slot, st, pa, pos) in P.lines:
            if st:
                posc[(yy, pid)][pos] += 1
        for k, d in posc.items():
            if max(d, key=d.get) == 2:
                _CATCHERS.setdefault(k[0], set()).add(k[1])
    return _CATCHERS.get(y, set())


def bootstrap(P, T=None, n=300, seed=151):
    T = T or seasons(P)
    G = golden(P, T)
    st = G["starts"]
    F = G["five"]
    rng = np.random.default_rng(seed)
    tot, per = [], defaultdict(list)
    for _ in range(n):
        i = rng.integers(0, len(st), len(st))
        vals = {f["name"]: ev(f["lines"], st[i] * G["rate"][f["slot"]]) for f in F}
        tot.append(sum(vals.values()))
        for k, v in vals.items():
            per[k].append(v)
    return float(np.std(tot)), {k: float(np.std(v)) for k, v in per.items()}


# ---------------------------------------------------------------------------------------------------- Ask A (stints)
def ask_a(P, mode="golden"):
    """Every injured-list stint of the five since the start of 2024: the date each took effect and the regular-season
    days it covered. Modes give the stops: 'move' (the transaction date as the date it took effect), 'split' (every
    placement a stint), 'merge' (stints a week apart joined), 'by_name' (the moves found by name), 'golden'."""
    tx = json.load(open(os.path.join(P.target, "lsf_transactions_2024_2026.json"), encoding="utf-8"))["transactions"]
    rep = read_csv(os.path.join(P.target, "league_office_il_report_2024_2026.csv"))
    F = five(P)
    names = {f["name"] for f in F}
    out = []
    for f in F:
        mine = (lambda t: t["player"] == f["name"]) if mode == "by_name" else (lambda t: t["player_id"] == f["lg"])
        mv = sorted((t for t in tx if mine(t) and t["type"] in (
            "IL_PLACEMENT", "IL_ACTIVATION", "IL_REINSTATEMENT")), key=lambda t: (t["date"], t["transaction_id"]))
        stints, cur = [], None
        for t in mv:
            d = ymd(t["date"])
            lst = re.search(r"the (\d+-day) injured list", t["description"]).group(1)
            if t["type"] == "IL_PLACEMENT":
                if cur is None or mode == "split":
                    if cur is not None:
                        cur["end"] = d
                        stints.append(cur)
                    cur = dict(placed=d, list=lst, end=None)
                else:
                    cur["list"] = lst
            else:
                cur["end"] = d
                stints.append(cur)
                cur = None
        if mode == "merge":
            merged = []
            for s in stints:
                if merged and (s["placed"] - merged[-1]["end"]).days <= 7:
                    merged[-1]["end"] = s["end"]
                else:
                    merged.append(dict(s))
            stints = merged
        rname = report_name(f["name"])
        for s in stints:
            if mode in ("move", "split", "merge", "by_name"):
                eff = s["placed"]
            else:
                rows = [r for r in rep if r["player"] == rname and mdy(r["placed"]) == s["placed"]]
                r0 = rows[0]
                eff = mdy(r0["eligible"]) - dt.timedelta(days=MIN_DAYS[r0["injured_list"]])
            od, last = P.season[s["placed"].year]
            start = max(eff, od)
            stop = min(s["end"] - dt.timedelta(days=1), last)
            days = (stop - start).days + 1
            out.append(dict(player=f["name"], eff=eff, days=days, season=s["placed"].year))
    out.sort(key=lambda x: (x["eff"], x["player"]))
    return out


def report_name(name):
    nm = fold(name)
    first, last = nm.split(" ", 1)
    return "%s, %s" % (last.upper(), first.upper())


# --------------------------------------------------------------------------------------------- Ask B (bonuses paid)
def ask_b(P, mode="golden"):
    """The plate-appearance bonuses the club paid for each of the 2024, 2025 and 2026 seasons, player by player.
    The payroll pays each player's playing-time bonuses for a season (plate appearances and games started) together,
    half after the season and half on the following January 15; the plate-appearance part of each payment is half the
    plate-appearance lines the player reached while he was the club's. Modes give the stops: 'face' (the payroll's
    playing-time and legacy season-end lines at face value, each half to its season, voids netted, pitchers dropped),
    'code_payyear' (the playing-time code by pay year), 'code_season' (the playing-time code, each half to its season,
    pitchers in), 'register' (the register's plate-appearance terms against the season's plate appearances),
    'gross' (the face-value lines with the void reversal ignored), 'golden'."""
    pay = read_csv(os.path.join(P.target, "ral_payroll_player_earnings_2023_2026.csv"))
    hmap = {r["legacy_employee_no"]: r["employee_id"] for r in read_csv(os.path.join(P.target, "ral_hris_legacy_employee_map.csv"))}
    wb = openpyxl.load_workbook(os.path.join(P.target, "ral_player_contract_register_2024_2026.xlsx"), read_only=True)
    ws = wb["Register"]
    hdr, reg = None, []
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Player":
            hdr = list(row)
            continue
        if hdr and row and row[0]:
            reg.append(dict(zip(hdr, row)))
    terms = {}
    for r in reg:
        t = r["Plate-appearance bonuses (each season)"]
        if t:
            m = re.match(r"\$([\d,]+) each for ([\d, and]+) plate appearances", t)
            a, b = r["Seasons"].split("-") if "-" in r["Seasons"] else (r["Seasons"], r["Seasons"])
            terms[r["Employee ID"]] = dict(name=r["Player"], amount=int(m.group(1).replace(",", "")),
                                           lines=[int(x) for x in re.findall(r"\d+", m.group(2))],
                                           seasons=range(int(a), int(b) + 1), status=r["Status"])
    emp = lambda r: hmap.get(r["employee_id"], r["employee_id"])
    name_of = {r["Employee ID"]: r["Player"] for r in reg}
    T = seasons(P)
    pa_club = defaultdict(int)
    for (y, g, d, club, pid, slot, st, pa, pos) in P.lines:
        pa_club[(y, pid, club)] += pa
    lg_of = {}
    for r in P.plan:
        first, last = r["name"].split(" ", 1)
        lg_of["%s, %s" % (last, first)] = r["lg"]

    def season_of(d):
        return d.year if d.month >= 7 else d.year - 1

    def playing_time(r):
        d = ymd(r["pay_date"])
        return r["earning_code"] == "BPA" or (r["earning_code"] == "E40" and d.month in (10, 1))

    out = defaultdict(float)
    if mode == "register":
        for e, t in terms.items():
            for y in (2024, 2025, 2026):
                if y in t["seasons"]:
                    pa = T.pa[(y, lg_of[t["name"]])]
                    out[(y, t["name"])] += t["amount"] * sum(1 for x in t["lines"] if pa >= x)
        return dict(out)
    if mode in ("face", "code_payyear", "code_season", "gross"):
        for r in pay:
            d = ymd(r["pay_date"])
            e = emp(r)
            if mode == "gross" and float(r["amount"]) < 0:
                continue
            if mode == "code_payyear":
                if r["earning_code"] == "BPA":
                    out[(d.year, name_of.get(e, e))] += float(r["amount"])
                continue
            if mode == "code_season":
                if r["earning_code"] == "BPA":
                    out[(season_of(d), name_of.get(e, e))] += float(r["amount"])
                continue
            if playing_time(r) and e in terms:
                out[(season_of(d), terms[e]["name"])] += float(r["amount"])
        return {k: v for k, v in out.items() if k[0] in (2024, 2025, 2026)}
    # golden (and 'gross'): the halves each season's playing-time payments made, times half the plate-appearance
    # lines the player reached for the club
    halves = defaultdict(lambda: defaultdict(float))
    for r in pay:
        e = emp(r)
        if e not in terms or not playing_time(r):
            continue
        amt = float(r["amount"])
        d = ymd(r["pay_date"])
        y = season_of(d)
        halves[(y, e)]["first" if d.month >= 7 else "second"] += amt
    for (y, e), parts in halves.items():
        if y not in (2024, 2025, 2026):
            continue
        t = terms[e]
        lg = lg_of[t["name"]]
        pa = pa_club[(y, lg, "RAL")]
        earned = t["amount"] * sum(1 for x in t["lines"] if pa >= x)
        n = sum(1 for v in parts.values() if v > 0.5)
        out[(y, t["name"])] += earned / 2 * n
    return {k: v for k, v in out.items() if v}


def ask_b_totals(d):
    tot = defaultdict(float)
    for (y, n), v in d.items():
        tot[y] += v
    return dict(tot)
