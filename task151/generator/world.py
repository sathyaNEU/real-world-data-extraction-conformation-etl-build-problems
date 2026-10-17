"""The league as it happened, 2021 to 2026, and the club's December 2026 plan: players and their careers, each club's
winter depth chart, the schedules, every player's availability (injured-list stints before and during the season,
day-to-day absences, rest, a lost job, a deadline trade), the lineups each game, every batting line, and the moves the
injured lists generate. This is the clean truth: nothing here is messed; `records.py` writes the shipped layouts."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

import numpy as np

import common as K
import names as NM

D = dt.timedelta

CLUBS = [   # code, city, nickname, home time zone
    ("RAL", "Raleigh", "Oaks", "America/New_York"),
    ("NSH", "Nashville", "Fiddlers", "America/Chicago"),
    ("CHA", "Charlotte", "Rails", "America/New_York"),
    ("POR", "Portland", "Ospreys", "America/Los_Angeles"),
    ("MTL", "Montreal", "Mariniers", "America/Toronto"),
    ("IND", "Indianapolis", "Stokers", "America/Indiana/Indianapolis"),
    ("CLB", "Columbus", "Ironmen", "America/New_York"),
    ("LOU", "Louisville", "Thoroughbreds", "America/Kentucky/Louisville"),
    ("MEM", "Memphis", "Riverboats", "America/Chicago"),
    ("SLC", "Salt Lake", "Pioneers", "America/Denver"),
    ("SAC", "Sacramento", "Prospectors", "America/Los_Angeles"),
    ("SAT", "San Antonio", "Lancers", "America/Chicago"),
    ("AUS", "Austin", "Grackles", "America/Chicago"),
    ("OKC", "Oklahoma City", "Drovers", "America/Chicago"),
    ("OMA", "Omaha", "Cattlemen", "America/Chicago"),
    ("ABQ", "Albuquerque", "Sandias", "America/Denver"),
    ("LVS", "Las Vegas", "Silverados", "America/Los_Angeles"),
    ("ORL", "Orlando", "Herons", "America/New_York"),
    ("JAX", "Jacksonville", "Navigators", "America/New_York"),
    ("BUF", "Buffalo", "Millers", "America/New_York"),
    ("HFD", "Hartford", "Charters", "America/New_York"),
    ("PVD", "Providence", "Quahogs", "America/New_York"),
    ("RIC", "Richmond", "Canalers", "America/New_York"),
    ("HRD", "Hampton Roads", "Shipwrights", "America/New_York"),
    ("BHM", "Birmingham", "Forge", "America/Chicago"),
    ("NOL", "New Orleans", "Levees", "America/Chicago"),
    ("TUL", "Tulsa", "Pipeliners", "America/Chicago"),
    ("VAN", "Vancouver", "Harbourmen", "America/Vancouver"),
    ("CGY", "Calgary", "Ranchers", "America/Edmonton"),
    ("OTT", "Ottawa", "Lumberjacks", "America/Toronto"),
]
CODES = [c[0] for c in CLUBS]
AFFILIATE = {c[0]: "%s Triple-A" % c[1] for c in CLUBS}

# The five signings' old clubs (2024 to 2026); P2 was traded to OKC at the 2026 deadline while on the injured list.
OLD_CLUB = {"P4": "OMA", "P1": "SAC", "P2": "BUF", "P3": "MEM", "P5": "LVS"}
P2_TRADED_TO = "OKC"
INF = {"1B", "2B", "3B", "SS"}
OF = {"LF", "CF", "RF"}


class Player:
    __slots__ = ("key", "pid", "name", "code", "origin", "born", "bats", "pos", "talent", "rates", "is_c")

    def __init__(self, key, pid, name, code, origin, born, bats, pos, talent, rates):
        self.key, self.pid, self.name, self.code, self.origin = key, pid, name, code, origin
        self.born, self.bats, self.pos, self.talent, self.rates = born, bats, pos, talent, rates
        self.is_c = pos == "C"

    def age(self, y):
        """Age on July 1 of the season (the convention the vendor uses)."""
        b = self.born
        return y - b.year - (1 if (b.month, b.day) > (7, 1) else 0)


class League:
    def __init__(self):
        self.players = {}           # key -> Player
        self.by_pid = {}
        self.used_names = set()
        self.codes = set()
        self.next_pid = 0
        self.rosters = {}           # (season, club) -> dict(starters={pos: key}, slots={pos: slot}, bench=[keys])
        self.games = {}             # season -> list of game dicts
        self.lines = {}             # season -> list of batting-line dicts
        self.stints = []            # injured-list stints (dicts)
        self.lists = []             # paternity and bereavement list spells
        self.trades = []            # deadline trades
        self.callups = []           # (season, club, key, first date, last date)
        self.club_of = {}           # (season, key) -> club at season start
        self.rosters_end = {}       # (season, club) -> the roster as the season ended (trades, lost jobs)
        self.design = {}            # the five signings' keys etc.


_PIDS = []


def player_id_pool():
    """League player IDs: six digits, issued in no order a reader could follow."""
    if not _PIDS:
        _PIDS.extend(int(x) for x in K.rng("player_ids").permutation(np.arange(600100, 699900)))
    return _PIDS


def new_player(L, r, pos, born_year, talent=None, name=None, origin=None, key=None):
    if name is None:
        name, origin = NM.draw_name(r, L.used_names)
    else:
        L.used_names.add(name)
        L.used_names.add(NM.ascii_fold(name))
    code = NM.legacy_code(name, L.codes)
    L.next_pid += 1
    r.integers(0, 13)                       # a draw the season streams have always made here
    pid = int(player_id_pool()[L.next_pid])
    born = dt.date(born_year, int(r.integers(1, 13)), int(r.integers(1, 29)))
    bats = ["R", "L", "S"][int(r.choice(3, p=[0.58, 0.34, 0.08]))]
    t = float(r.normal(0, 1)) if talent is None else talent
    avg = float(np.clip(0.255 + 0.016 * t + r.normal(0, 0.012), 0.205, 0.315))
    rates = dict(avg=avg, bb=float(np.clip(0.083 + 0.012 * t + r.normal(0, 0.015), 0.04, 0.15)),
                 hbp=float(np.clip(r.normal(0.011, 0.004), 0.003, 0.025)),
                 hr=float(np.clip(0.12 + 0.025 * t + r.normal(0, 0.03), 0.03, 0.24)),
                 k=float(np.clip(r.normal(0.30, 0.05), 0.15, 0.42)))
    key = key or "p%05d" % L.next_pid
    p = Player(key, pid, name, code, origin, born, bats, pos, t, rates)
    L.players[key] = p
    L.by_pid[pid] = p
    return p


# ------------------------------------------------------------------------------------------------------------ rosters
def lineup_order(L, starters, r):
    """Batting order: the best hitters first and fourth, the catcher low, by a lineup score with noise."""
    keys = list(starters.items())
    score = {}
    for pos, k in keys:
        p = L.players[k]
        s = p.talent + r.normal(0, 0.6)
        if pos == "C":
            s -= 1.6
        score[pos] = s
    ranked = sorted(score, key=lambda q: -score[q])
    # slots by rank: 2, 3, 1, 4, 5, 6, 7, 8, 9 (the top two hitters bat second and third, the next leads off)
    order = [2, 3, 1, 4, 5, 6, 7, 8, 9]
    return {pos: order[i] for i, pos in enumerate(ranked)}


def fresh_roster(L, r, club, y):
    starters, bench = {}, []
    for pos in K.POSITIONS:
        age = int(np.clip(round(r.normal(29.0, 3.2)), 23, 37))
        p = new_player(L, r, "C" if pos == "C" else ("1B" if pos == "DH" and r.random() < 0.5 else pos),
                       y - age, talent=float(r.normal(0.5, 0.8)))
        starters[pos] = p.key
    for bpos in ["C", "INF", "INF", "OF", "UT"]:
        age = int(np.clip(round(r.normal(28.5, 3.5)), 22, 37))
        pos = {"C": "C", "INF": ["2B", "SS", "3B", "1B"][int(r.integers(4))], "OF": ["LF", "CF", "RF"][int(r.integers(3))],
               "UT": ["2B", "3B", "LF", "RF"][int(r.integers(4))]}[bpos]
        p = new_player(L, r, pos, y - age, talent=float(r.normal(-0.6, 0.7)))
        bench.append(p.key)
    return dict(starters=starters, bench=bench)


def offseason(L, y):
    """Carry each club's roster from season y-1 into y: retirements, free agency, demotions, promotions, rookies."""
    r = K.rng("offseason", y)
    prev = {c: L.rosters_end[(y - 1, c)] for c in CODES}
    fa_pool = []
    nxt = {}
    retire_p = lambda a: 0.02 if a <= 33 else {34: 0.08, 35: 0.16, 36: 0.28}.get(a, 0.45)
    for c in CODES:
        st, bench = dict(prev[c]["starters"]), list(prev[c]["bench"])
        keep, open_pos = {}, []
        for pos, k in st.items():
            p = L.players[k]
            if k in L.design.get("locked", {}).get(y, {}):
                continue
            u = r.random()
            if u < retire_p(p.age(y)):
                open_pos.append(pos)
            elif u < retire_p(p.age(y)) + 0.16:
                fa_pool.append(k)
                open_pos.append(pos)
            elif u < retire_p(p.age(y)) + 0.21:
                bench.append(k)
                open_pos.append(pos)
            else:
                keep[pos] = k
        nb = []
        for k in bench:
            p = L.players[k]
            u = r.random()
            if u < retire_p(p.age(y)) + 0.05:
                continue
            if u < retire_p(p.age(y)) + 0.20:
                fa_pool.append(k)
                continue
            nb.append(k)
        nxt[c] = dict(starters=keep, open=open_pos, bench=nb)
    # fill open starting positions: promote a bench player sometimes, else sign a free agent or a rookie
    r.shuffle(fa_pool)
    for c in CODES:
        R = nxt[c]
        for pos in R["open"]:
            choice = None
            if R["bench"] and r.random() < 0.25:
                cands = [k for k in R["bench"] if (L.players[k].is_c == (pos == "C"))]
                if cands:
                    choice = cands[int(r.integers(len(cands)))]
                    R["bench"].remove(choice)
            if choice is None and fa_pool and r.random() < 0.55:
                cands = [k for k in fa_pool if (L.players[k].is_c == (pos == "C")) and L.players[k].age(y) <= 36]
                if cands:
                    choice = cands[0]
                    fa_pool.remove(choice)
            if choice is None:
                age = int(np.clip(round(r.normal(25.5, 2.2)), 22, 31))
                ppos = "C" if pos == "C" else ("1B" if pos == "DH" else pos)
                choice = new_player(L, r, ppos, y - age, talent=float(r.normal(0.2, 0.8))).key
            R["starters"][pos] = choice
        # bench back to five: free agents or call-ups from the system
        need = {"C": 1, "X": 4}
        have_c = sum(1 for k in R["bench"] if L.players[k].is_c)
        while have_c < 1:
            age = int(np.clip(round(r.normal(28, 3)), 23, 36))
            R["bench"].append(new_player(L, r, "C", y - age, talent=float(r.normal(-0.7, 0.6))).key)
            have_c += 1
        while len(R["bench"]) < 5:
            cands = [k for k in fa_pool if not L.players[k].is_c]
            if cands and r.random() < 0.5:
                k = cands[0]
                fa_pool.remove(k)
                R["bench"].append(k)
            else:
                age = int(np.clip(round(r.normal(26.5, 3)), 22, 35))
                pos = ["2B", "SS", "3B", "1B", "LF", "CF", "RF"][int(r.integers(7))]
                R["bench"].append(new_player(L, r, pos, y - age, talent=float(r.normal(-0.6, 0.7))).key)
        while len(R["bench"]) > 6:
            R["bench"].pop()
    for c in CODES:
        L.rosters[(y, c)] = dict(starters=nxt[c]["starters"], bench=nxt[c]["bench"])
    apply_locks(L, y)


def apply_locks(L, y):
    """The designed players' clubs and positions (the five signings' old clubs, the club's own veterans)."""
    for key, (club, pos) in L.design.get("locked", {}).get(y, {}).items():
        # remove the player from wherever the carry-over put him
        for c in CODES:
            R = L.rosters[(y, c)]
            for q, k in list(R["starters"].items()):
                if k == key:
                    del R["starters"][q]
            if key in R["bench"]:
                R["bench"].remove(key)
        R = L.rosters[(y, club)]
        if pos == "BENCH":
            R["bench"].append(key)
            continue
        disp = R["starters"].get(pos)
        R["starters"][pos] = key
        if disp and disp != key:
            R["bench"].append(disp)
    # every club still fields nine; any position left empty is filled from the bench or a rookie
    r = K.rng("locks", y)
    for c in CODES:
        R = L.rosters[(y, c)]
        for pos in K.POSITIONS:
            if pos not in R["starters"]:
                cands = [k for k in R["bench"] if L.players[k].is_c == (pos == "C")]
                if cands:
                    R["starters"][pos] = cands[0]
                    R["bench"].remove(cands[0])
                else:
                    age = int(np.clip(round(r.normal(26, 2.5)), 22, 31))
                    R["starters"][pos] = new_player(L, r, "C" if pos == "C" else pos, y - age).key
        while len(R["bench"]) > 6:
            R["bench"].pop(0)


# ------------------------------------------------------------------------------------------------------------ schedule
def make_schedule(L, y):
    """54 three-game series a club (162 games), a league-wide off day after 20 of them, the All-Star break; rainouts made
    up as doubleheaders and a few games suspended and completed the next day."""
    r = K.rng("schedule", y)
    od, last, asb = K.SEASON[y]
    asb_days = {asb + D(days=k) for k in range(4)}
    days = [d for d in K.daterange(od, last) if d not in asb_days]
    assert len(days) == 182
    gaps = set(int(x) for x in r.choice(np.arange(1, 54), 20, replace=False))
    slots, i = [], 0
    for s in range(54):
        slots.append(days[i:i + 3])
        i += 3
        if s + 1 in gaps:
            i += 1
    assert i == 182
    off_days = [d for d in days if not any(d in sl for sl in slots)]
    home_ct = defaultdict(int)
    games = []
    pk = {2021: 633001, 2022: 661001, 2023: 717001, 2024: 744001, 2025: 776001, 2026: 822001}[y]
    for s, sl in enumerate(slots):
        order = list(CODES)
        r.shuffle(order)
        for j in range(0, 30, 2):
            a, b = order[j], order[j + 1]
            if home_ct[a] < home_ct[b] or (home_ct[a] == home_ct[b] and r.random() < 0.5):
                h, v = a, b
            else:
                h, v = b, a
            home_ct[h] += 1
            for g, d in enumerate(sl):
                games.append(dict(season=y, date=d, home=h, away=v, series=s, gnum=0, completed=None, pk=None))
    # rainouts: the game is made up as the first game of a doubleheader on the series' next day, or on the next
    # league-wide off day when it was the series' last game
    games.sort(key=lambda g: (g["date"], g["home"]))
    by_series = defaultdict(list)
    for g in games:
        by_series[(g["series"], g["home"])].append(g)
    made_up = set()          # (club, off day) already taken by a game made up there
    for key, gs in by_series.items():
        for idx, g in enumerate(gs):
            if r.random() < 0.005:
                if idx < len(gs) - 1:
                    nxt = gs[idx + 1]
                    if nxt["gnum"] == 0:
                        g["date"] = nxt["date"]
                        g["gnum"], nxt["gnum"] = 1, 2
                else:
                    later = [d for d in off_days if d > g["date"] and (g["home"], d) not in made_up and
                             (g["away"], d) not in made_up]
                    if later:
                        g["date"] = later[0]
                        made_up |= {(g["home"], later[0]), (g["away"], later[0])}
            elif r.random() < 0.002 and idx < len(gs) - 1 and g["gnum"] == 0:
                g["completed"] = gs[idx + 1]["date"]
    games.sort(key=lambda g: (g["date"], g["gnum"], g["home"]))
    for g in games:
        g["pk"] = pk
        pk += int(r.integers(1, 3))
        for side, other, team_off in (("home", "away", K.PAR["home_adj"]), ("away", "home", -K.PAR["home_adj"])):
            t = r.normal(K.PAR["team_pa_mean"] + team_off, K.PAR["team_pa_sd"])
            if r.random() < 0.085:
                t += r.choice([4, 5, 6, 8, 10])
            g["pa_" + side] = int(np.clip(round(t), 27, 62))
    L.games[y] = games
    return games


# -------------------------------------------------------------------------------------------------------- availability
def il_from_games(cg, s, e, n):
    """An injured-list interval in dates from missed club games [s, e): it takes effect the day after the last game
    before it (the day before opening day's game for a spring stint) and ends on the day of the first game back."""
    eff = cg[s - 1]["date"] + D(days=1) if s >= 1 else None
    reinst = cg[e]["date"] if e < n else None
    return eff, reinst


def gen_availability(L, y, key, cg, role, r):
    """Random availability for one player on one club's schedule: injured-list stints (spring and in-season),
    day-to-day absences, rest, a lost job."""
    p = L.players[key]
    n = len(cg)
    P = K.PAR
    av = dict(stints=[], dtd=set(), rest=set(), jobloss=None, lists=[])
    missed = np.zeros(n, bool)
    spells = []
    sp = P["spring_p"] if role == "starter" else 0.08
    if r.random() < sp:
        Lg = int(round(np.exp(r.normal(P["spring_mu"], P["spring_sig"]))))
        Lg = max(Lg, 3)
        spells.append([0, min(Lg, n), "spring", "10-day"])
    lam = P["stint_rate"] if role == "starter" else 0.5
    for _ in range(int(r.poisson(lam))):
        s = int(r.integers(1, n))
        if r.random() < P["concussion_share"]:
            Lg, lst = int(r.integers(6, 13)), "7-day"
        else:
            Lg, lst = 9 + int(round(np.exp(r.normal(P["stint_mu"], P["stint_sig"])))), "10-day"
        spells.append([s, min(s + Lg, n), "season", lst])
    spells.sort()
    od = K.SEASON[y][0]
    spring_eff = od - D(days=int(r.integers(3, 11)))
    merged = []
    for s, e, kind, lst in spells:
        if merged and s <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e, kind, lst])
        # the stint lasts at least the list's minimum period from the date it takes effect
        m = merged[-1]
        eff = spring_eff if m[0] == 0 else cg[m[0] - 1]["date"] + D(days=1)
        while m[1] < n and cg[m[1]]["date"] < eff + D(days=MIN_DAYS[m[3]]):
            m[1] += 1
    for s, e, kind, lst in merged:
        missed[s:e] = True
        eff = spring_eff if s == 0 else cg[s - 1]["date"] + D(days=1)
        av["stints"].append(dict(s=s, e=e, kind=kind, list=lst, eff=eff, reinst=cg[e]["date"] if e < n else None))
    # day-to-day absences, never the game before a stint
    for _ in range(int(r.poisson(P["dtd_rate"]))):
        s = int(r.integers(0, n))
        ln = int(r.integers(1, 3))
        for g in range(s, min(s + ln, n)):
            if not missed[g] and not any(st["s"] == g + 1 for st in av["stints"]):
                av["dtd"].add(g)
                missed[g] = True
    if role == "starter":
        mu = P["catcher_rest"] if p.is_c else P["rest_rate"]
        cand = [g for g in range(3, n) if not missed[g] and not any(st["s"] == g + 1 for st in av["stints"])]
        k = min(len(cand), int(r.poisson(mu)))
        if k:
            for g in r.choice(cand, k, replace=False):
                av["rest"].add(int(g))
        if r.random() < P["job_loss_p"]:
            av["jobloss"] = int(r.integers(25, 140))
    # paternity and bereavement lists (not injured lists)
    u = r.random()
    if u < 0.03 or u > 0.99:
        kind = "paternity" if u < 0.03 else "bereavement"
        s = int(r.integers(5, n - 5))
        ln = int(r.integers(1, 3)) if kind == "paternity" else int(r.integers(3, 6))
        if not missed[s:s + ln].any() and not any(st["s"] <= s + ln and s <= st["e"] for st in av["stints"]):
            av["lists"].append(dict(kind=kind, s=s, e=s + ln))
            for g in range(s, s + ln):
                av["dtd"].add(g)
    return av


MIN_DAYS = {"7-day": 7, "10-day": 10, "15-day": 15, "60-day": 60}


def designed_availability(L, y, key, cg, spec, r):
    """The five signings' seasons as designed: stints at fixed games, rest drawn, no day-to-day, no lost job."""
    n = len(cg)
    av = dict(stints=[], dtd=set(), rest=set(), jobloss=None, lists=[])
    missed = np.zeros(n, bool)
    for st in spec.get("stints", []):
        s = nearest_game(cg, st["from"]) if st["from"] is not None else 0
        e = min(s + st["games"], n) if st.get("games") is not None else n
        eff0, _ = il_from_games(cg, s, e, n)
        eff = st.get("eff") or eff0
        lst = st.get("list", "10-day")
        while st.get("reinst") is None and e < n and cg[e]["date"] < eff + D(days=MIN_DAYS[lst]):
            e += 1
        rein = st.get("reinst") or (cg[e]["date"] if e < n else None)
        av["stints"].append(dict(s=s, e=e, kind=st.get("kind", "season"), list=st.get("list", "10-day"), d=st,
                                 eff=eff, reinst=rein))
        missed[s:e] = True
    for ls in spec.get("lists", []):
        s = nearest_game(cg, ls["from"])
        av["lists"].append(dict(kind=ls["kind"], s=s, e=s + ls["games"]))
        for g in range(s, s + ls["games"]):
            av["dtd"].add(g)
            missed[g] = True
    cand = [g for g in range(3, n) if not missed[g] and not any(st["s"] == g + 1 for st in av["stints"])]
    k = spec.get("rest", 3)
    if k:
        for g in r.choice(cand, k, replace=False):
            av["rest"].add(int(g))
    return av


def nearest_game(cg, d):
    """Index of the club's first game on or after date d."""
    for i, g in enumerate(cg):
        if g["date"] >= d:
            return i
    return len(cg) - 1


INJURIES = ["right hamstring strain", "left hamstring strain", "right oblique strain", "left oblique strain",
            "lower back strain", "right wrist sprain", "left wrist sprain", "right shoulder inflammation",
            "left knee sprain", "right ankle sprain", "left calf strain", "right groin strain", "left thumb sprain",
            "fractured left hand", "fractured right foot", "right elbow inflammation", "neck spasms",
            "left quadriceps strain", "right hip flexor strain", "plantar fasciitis, left foot"]
GROUP = {"C": "C", "1B": "INF", "2B": "INF", "3B": "INF", "SS": "INF", "LF": "OF", "CF": "OF", "RF": "OF", "DH": "ANY"}


def bat_line(p, pa, r):
    """Counting stats for one batting line with a given number of plate appearances."""
    q = p.rates
    bb = int(r.binomial(pa, q["bb"])) if pa else 0
    hbp = int(r.binomial(pa - bb, q["hbp"])) if pa - bb > 0 else 0
    rest = pa - bb - hbp
    sf = int(r.binomial(rest, 0.007)) if rest > 0 else 0
    sh = int(r.binomial(rest - sf, 0.003)) if rest - sf > 0 else 0
    ci = int(r.binomial(rest - sf - sh, 0.0006)) if rest - sf - sh > 0 else 0
    ab = rest - sf - sh - ci
    h = int(r.binomial(ab, q["avg"])) if ab else 0
    hr = int(r.binomial(h, q["hr"])) if h else 0
    t3 = int(r.binomial(h - hr, 0.025)) if h - hr > 0 else 0
    d2 = int(r.binomial(h - hr - t3, 0.24)) if h - hr - t3 > 0 else 0
    so = int(r.binomial(ab - h, q["k"])) if ab - h > 0 else 0
    runs = int(r.binomial(pa, 0.118)) if pa else 0
    rbi = int(r.binomial(pa, 0.112)) if pa else 0
    rbi = max(rbi, hr)
    runs = max(runs, hr)
    return dict(pa=pa, ab=ab, r=runs, h=h, d2=d2, t3=t3, hr=hr, rbi=rbi, bb=bb, so=so, hbp=hbp, sh=sh, sf=sf, ci=ci)


def simulate_season(L, y):
    games = make_schedule(L, y)
    cg = {c: [] for c in CODES}
    for g in games:
        cg[g["home"]].append(g)
        cg[g["away"]].append(g)
    gidx = {c: {id(g): i for i, g in enumerate(cg[c])} for c in CODES}
    locked = L.design.get("locked", {}).get(y, {})
    dslot = L.design.get("slot", {}).get(y, {})
    # planned batting orders (the winter depth charts), designed players at their designed slots
    for c in CODES:
        R = L.rosters[(y, c)]
        sl = lineup_order(L, R["starters"], K.rng("order", y, c))
        for key, want in dslot.items():
            if locked.get(key, (None,))[0] != c:
                continue
            pos = locked[key][1]
            have = sl[pos]
            other = [q for q, s in sl.items() if s == want][0]
            sl[pos], sl[other] = want, have
        R["slots"] = sl
        for pos, k in R["starters"].items():
            L.club_of[(y, k)] = c
        for k in R["bench"]:
            L.club_of[(y, k)] = c
    # deadline trades: designed one-way trades and a few swaps of starters at one position between two clubs
    trades = [dict(t) for t in L.design.get("trades", {}).get(y, [])]
    r = K.rng("trades", y)
    pool = [(c, pos) for c in CODES for pos in K.POSITIONS if pos != "C"
            and L.rosters[(y, c)]["starters"][pos] not in locked and c != K.CLUB]
    r.shuffle(pool)
    used_c = set(t["frm"] for t in trades) | set(t["to"] for t in trades)
    nswap = int(r.binomial(len(pool) // 2, K.PAR["trade_p"]))
    i = 0
    while nswap > 0 and i + 1 < len(pool):
        (c1, p1), (c2, p2) = pool[i], pool[i + 1]
        i += 2
        if p1 != p2:
            match = [j for j in range(i, len(pool)) if pool[j][1] == p1 and pool[j][0] not in {c1} | used_c]
            if not match:
                continue
            c2, p2 = pool[match[0]]
            pool.pop(match[0])
        if c1 in used_c or c2 in used_c or c1 == c2:
            continue
        d = dt.date(y, 7, int(r.integers(24, 32)))
        k1, k2 = L.rosters[(y, c1)]["starters"][p1], L.rosters[(y, c2)]["starters"][p1]
        trades.append(dict(key=k1, frm=c1, to=c2, date=d, pos=p1, swap=k2))
        trades.append(dict(key=k2, frm=c2, to=c1, date=d, pos=p1, swap=k1))
        used_c |= {c1, c2}
        nswap -= 1
    for t in trades:
        L.trades.append(dict(t, season=y))
    # availability on each player's season-start club schedule
    AV = {}
    dspec = L.design.get("avail", {}).get(y, {})
    for c in CODES:
        R = L.rosters[(y, c)]
        for pos, k in R["starters"].items():
            rr = K.rng("avail", y, k)
            AV[k] = designed_availability(L, y, k, cg[c], dspec[k], rr) if k in dspec else \
                gen_availability(L, y, k, cg[c], "starter", rr)
        for k in R["bench"]:
            AV[k] = gen_availability(L, y, k, cg[c], "bench", K.rng("avail", y, k))
    # date views for players who change clubs
    dated = {}
    for k, av in AV.items():
        c = L.club_of[(y, k)]
        ivs = []
        for st in av["stints"]:
            if "eff" in st:
                eff, rein = st["eff"], st["reinst"]
            else:
                eff, rein = il_from_games(cg[c], st["s"], st["e"], len(cg[c]))
            ivs.append((eff or dt.date(y, 3, 1), rein))
        dated[k] = dict(il=ivs, off={cg[c][g]["date"] for g in av["dtd"] | av["rest"]})
    # who owns each lineup slot, game by game (trades and lost jobs change it)
    owner = {}
    for c in CODES:
        R = L.rosters[(y, c)]
        for pos, k in R["starters"].items():
            owner[(c, R["slots"][pos])] = [(dt.date(y, 1, 1), k, pos)]
    benches = {c: list(L.rosters[(y, c)]["bench"]) for c in CODES}
    for t in sorted(trades, key=lambda t: (t["date"], t["key"])):
        R = L.rosters[(y, t["to"])]
        slot = t.get("slot") or R["slots"][t["pos"]]
        prev = owner[(t["to"], slot)][-1]
        owner[(t["to"], slot)].append((t["date"], t["key"], prev[2]))
        if not t.get("swap"):
            benches[t["to"]].append(prev[1])
            fr = L.rosters[(y, t["frm"])]
            fslot = [s for (cc, s), v in owner.items() if cc == t["frm"] and v[-1][1] == t["key"]]
            for s in fslot:
                cands = [b for b in benches[t["frm"]] if GROUP.get(L.players[b].pos, "INF") ==
                         GROUP[owner[(t["frm"], s)][-1][2]] or GROUP[owner[(t["frm"], s)][-1][2]] == "ANY"]
                rep = cands[0] if cands else benches[t["frm"]][0]
                t["rep"] = rep
                owner[(t["frm"], s)].append((t["date"], rep, owner[(t["frm"], s)][-1][2]))
                benches[t["frm"]].remove(rep)
    lines = []
    callups = defaultdict(list)
    stint_rep, rep_busy = {}, {}
    lost_jobs = []
    L.design.setdefault("callup_pool", {})
    rr = K.rng("games", y)
    jobloss_done = set()
    for c in CODES:
        R = L.rosters[(y, c)]
        for gi, g in enumerate(cg[c]):
            side = "home" if g["home"] == c else "away"
            opp = g["away"] if side == "home" else g["home"]
            T = g["pa_" + side]
            used = set()
            lineup = {}
            for slot in K.LINEUP_SLOTS:
                hist = owner[(c, slot)]
                cur = [h for h in hist if h[0] <= g["date"]][-1]
                k, pos = cur[1], cur[2]
                # a lost job: the slot passes to a bench player for the rest of the season
                av = AV.get(k)
                if av and av["jobloss"] is not None and L.club_of[(y, k)] == c and gi >= av["jobloss"] \
                        and (c, slot, k) not in jobloss_done:
                    cands = [b for b in benches[c] if b not in used and L.players[b].is_c == (pos == "C") and
                             (GROUP[pos] == "ANY" or GROUP.get(L.players[b].pos, "INF") == GROUP[pos] or pos == "1B")]
                    if cands:
                        rep = cands[0]
                        owner[(c, slot)].append((g["date"], rep, pos))
                        owner[(c, slot)].sort(key=lambda h: h[0])
                        benches[c].remove(rep)
                        benches[c].append(k)
                        jobloss_done.add((c, slot, k))
                        lost_jobs.append((c, pos, k, rep))
                        k = rep
                starter = k if available(L, y, k, c, gi, g, AV, dated, cg) else None
                if starter is None:
                    # an injured-list stint: the club's replacement for it (a bench player or a call-up) starts
                    si = on_il(L, y, k, c, gi, g, AV, dated)
                    if si is not None:
                        rk = (c, slot, k, si)
                        if rk not in stint_rep:
                            stint_rep[rk] = pick_stint_rep(L, y, c, pos, gi, g, k, si, benches, used, AV, dated,
                                                           cg, rep_busy, rr)
                        cand = stint_rep[rk]
                        if cand not in used and available(L, y, cand, c, gi, g, AV, dated, cg):
                            starter = cand
                            if cand in L.design["callup_pool"].get((y, c), []):
                                callups[(c, cand)].append(g["date"])
                if starter is None or starter in used:
                    starter = pick_fill(L, y, c, pos, gi, g, benches, used, AV, dated, cg, callups, rr)
                lineup[slot] = (starter, pos)
                used.add(starter)
            for slot in K.LINEUP_SLOTS:
                k, pos = lineup[slot]
                pa = (T - slot) // 9 + 1
                sub = None
                u = rr.random()
                if u < K.PAR["late_sub_p"] and pa >= 3:
                    sub = pick_sub(L, y, c, gi, g, benches, used, AV, dated, cg, callups, rr)
                    if sub:
                        pa -= 1
                        used.add(sub)
                elif u > 0.996:
                    sub = pick_sub(L, y, c, gi, g, benches, used, AV, dated, cg, callups, rr)
                    if sub:
                        used.add(sub)
                        lines.append(row(y, g, c, opp, side, slot, 1, pos, sub, bat_line(L.players[sub], 0, rr)))
                        sub = None
                lines.append(row(y, g, c, opp, side, slot, 0, pos, k, bat_line(L.players[k], pa, rr)))
                if sub:
                    lines.append(row(y, g, c, opp, side, slot, 1, "PH", sub, bat_line(L.players[sub], 1, rr)))
    for (c, k), ds in callups.items():
        L.callups.append((y, c, k, min(ds), max(ds)))
    L.lines[y] = lines
    record_stints(L, y, AV, cg)
    end_rosters(L, y, trades, lost_jobs)
    return lines


def end_rosters(L, y, trades, lost_jobs):
    """Each club's roster as the season ended: traded players with their new clubs, a lost job's replacement as the
    starter and the player who lost it on the bench."""
    end = {c: dict(starters=dict(L.rosters[(y, c)]["starters"]), bench=list(L.rosters[(y, c)]["bench"])) for c in CODES}
    for c, pos, k, rep in lost_jobs:
        E = end[c]
        if E["starters"].get(pos) == k:
            E["starters"][pos] = rep
            if rep in E["bench"]:
                E["bench"].remove(rep)
            E["bench"].append(k)
    for t in sorted(trades, key=lambda t: (t["date"], t["key"])):
        k, frm, to, pos = t["key"], t["frm"], t["to"], t["pos"]
        E1, E2 = end[frm], end[to]
        for q, kk in list(E1["starters"].items()):
            if kk == k:
                del E1["starters"][q]
                if t.get("rep") and t["rep"] in E1["bench"]:
                    E1["starters"][q] = t["rep"]
                    E1["bench"].remove(t["rep"])
        if k in E1["bench"]:
            E1["bench"].remove(k)
        disp = E2["starters"].get(pos)
        E2["starters"][pos] = k
        if disp and disp != k and not t.get("swap") and disp not in E2["bench"]:
            E2["bench"].append(disp)
    for c in CODES:
        L.rosters_end[(y, c)] = end[c]


def row(y, g, c, opp, side, slot, seq, pos, k, stat):
    d = dict(season=y, pk=g["pk"], date=g["date"], gnum=g["gnum"], completed=g["completed"], home=g["home"], club=c,
             opp=opp, ha="H" if side == "home" else "A", slot=slot, seq=seq, pos=pos, key=k)
    d.update(stat)
    return d


def available(L, y, k, c, gi, g, AV, dated, cg):
    av = AV.get(k)
    if av is None:
        return True
    if L.club_of.get((y, k)) == c:
        if any(st["s"] <= gi < st["e"] for st in av["stints"]):
            return False
        if gi in av["dtd"] or gi in av["rest"]:
            return False
        return True
    dv = dated[k]
    for eff, rein in dv["il"]:
        if eff <= g["date"] and (rein is None or g["date"] < rein):
            return False
    return g["date"] not in dv["off"]


def on_il(L, y, k, c, gi, g, AV, dated):
    """The injured-list stint (its index) keeping player k out of club c's game, or None."""
    av = AV.get(k)
    if av is None:
        return None
    if L.club_of.get((y, k)) == c:
        for i, st in enumerate(av["stints"]):
            if st["s"] <= gi < st["e"]:
                return i
        return None
    for i, (eff, rein) in enumerate(dated[k]["il"]):
        if eff <= g["date"] and (rein is None or g["date"] < rein):
            return i
    return None


def stint_end(L, y, k, c, gi, si, AV, dated, cg):
    """Index of club c's first game after the stint (the schedule's length when it runs to the end)."""
    if L.club_of.get((y, k)) == c:
        return AV[k]["stints"][si]["e"]
    rein = dated[k]["il"][si][1]
    if rein is None:
        return len(cg[c])
    for j in range(gi, len(cg[c])):
        if cg[c][j]["date"] >= rein:
            return j
    return len(cg[c])


def pick_stint_rep(L, y, c, pos, gi, g, k, si, benches, used, AV, dated, cg, rep_busy, rr):
    """The club's answer to a regular's injured-list stint: about half the time the bench player at his position
    takes the job, otherwise a player recalled from Triple-A."""
    grp = GROUP[pos]
    end = stint_end(L, y, k, c, gi, si, AV, dated, cg)
    free = lambda b: rep_busy.get((c, b), -1) <= gi
    same = [b for b in benches[c] if b not in used and free(b) and available(L, y, b, c, gi, g, AV, dated, cg) and
            ((grp == "C" and L.players[b].is_c) or (grp == "ANY" and not L.players[b].is_c) or
             (grp not in ("C", "ANY") and GROUP.get(L.players[b].pos, "INF") == grp))]
    if same and rr.random() < K.PAR["bench_rep_p"]:
        same.sort(key=lambda b: -L.players[b].talent)
        rep = same[0]
    else:
        pool = L.design["callup_pool"].setdefault((y, c), [])
        cands = [q for q in pool if q not in used and free(q) and (L.players[q].is_c == (grp == "C"))]
        if cands and rr.random() < K.PAR["recall_again_p"]:
            rep = cands[0]
        else:
            r = K.rng("callup", y, c, len(pool))
            age = int(np.clip(round(r.normal(25.5, 2.5)), 21, 33))
            ppos = "C" if grp == "C" else (pos if pos not in ("DH",) else "1B")
            rep = new_player(L, r, ppos, y - age, talent=float(r.normal(-1.0, 0.6))).key
            pool.append(rep)
            L.club_of.setdefault((y, rep), c)
    rep_busy[(c, rep)] = end
    return rep


def pick_fill(L, y, c, pos, gi, g, benches, used, AV, dated, cg, callups, rr):
    grp = GROUP[pos]
    cands = [b for b in benches[c] if b not in used and available(L, y, b, c, gi, g, AV, dated, cg)]
    same = [b for b in cands if (grp == "ANY" and not L.players[b].is_c) or
            (grp != "ANY" and (GROUP.get(L.players[b].pos, "INF") == grp))]
    if grp == "C":
        same = [b for b in cands if L.players[b].is_c]
    pick = same or ([b for b in cands if not L.players[b].is_c] if grp != "C" else [])
    if pick:
        w = np.array([np.exp(1.2 * L.players[b].talent) for b in pick])
        return pick[int(rr.choice(len(pick), p=w / w.sum()))]
    # a call-up from the club's Triple-A affiliate
    pool = [k for k in L.design.setdefault("callup_pool", {}).setdefault((y, c), [])
            if k not in used and (L.players[k].is_c == (grp == "C"))]
    if pool:
        k = pool[0]
    else:
        r = K.rng("callup", y, c, len(L.design["callup_pool"][(y, c)]))
        age = int(np.clip(round(r.normal(25.5, 2.5)), 21, 33))
        ppos = "C" if grp == "C" else ("SS" if grp == "INF" else ("CF" if grp == "OF" else "1B"))
        k = new_player(L, r, ppos, y - age, talent=float(r.normal(-1.0, 0.6))).key
        L.design["callup_pool"][(y, c)].append(k)
        L.club_of.setdefault((y, k), c)
    callups[(c, k)].append(g["date"])
    return k


def pick_sub(L, y, c, gi, g, benches, used, AV, dated, cg, callups, rr):
    cands = [b for b in benches[c] if b not in used and not L.players[b].is_c and
             available(L, y, b, c, gi, g, AV, dated, cg)]
    if not cands:
        return None
    return cands[int(rr.integers(len(cands)))]


def club_on(L, y, k, d):
    c = L.club_of.get((y, k))
    for t in L.trades:
        if t["season"] == y and t["key"] == k and t["date"] <= d:
            c = t["to"]
    return c


def record_stints(L, y, AV, cg):
    od, last, _ = K.SEASON[y]
    for k, av in AV.items():
        c0 = L.club_of[(y, k)]
        r = K.rng("moves", y, k)
        for st in av["stints"]:
            d = st.get("d", {})
            if "eff" in st:
                eff, rein = st["eff"], st["reinst"]
            else:
                eff, rein = il_from_games(cg[c0], st["s"], st["e"], len(cg[c0]))
            if eff is None:
                eff = od - D(days=int(r.integers(3, 11)))
            lst = st["list"]
            injury = d.get("injury") or INJURIES[int(r.integers(len(INJURIES)))]
            if lst == "7-day":
                injury = "concussion"
            lag = d.get("lag")
            if lag is None:
                lag = int(r.choice(4, p=[0.10, 0.30, 0.35, 0.25]))
            mv = [(eff + D(days=lag), club_on(L, y, k, eff + D(days=lag)), "PLACED", lst + " IL", injury)]
            end = rein or dt.date(y, 10, 1)
            cur = lst
            if lst != "7-day" and (end - eff).days >= 60:
                if d.get("to60_date"):
                    d60 = d["to60_date"]
                elif d.get("to60") is not None:
                    d60 = eff + D(days=d["to60"])
                else:
                    d60 = eff + D(days=int(r.integers(14, 25)))
                if d60 < end:
                    mv.append((d60, club_on(L, y, k, d60), "PLACED", "60-day IL", injury))
                    cur = "60-day"
            if rein is not None and (rein - eff).days >= 25:
                if d.get("rehab_date"):
                    dr = d["rehab_date"]
                elif d.get("rehab") is not None:
                    dr = rein - D(days=d["rehab"])
                else:
                    dr = rein - D(days=int(r.integers(4, 10)))
                mv.append((dr, club_on(L, y, k, dr), "REHAB ASSIGNMENT", cur + " IL",
                           "rehabilitation assignment with %s" % AFFILIATE[club_on(L, y, k, dr)]))
            if rein is not None:
                mv.append((rein, club_on(L, y, k, rein), "ACTIVATED", cur + " IL", ""))
            else:
                dz = dt.date(y, 11, int(r.integers(3, 7)))
                mv.append((dz, club_on(L, y, k, last), "REINSTATED", cur + " IL", ""))
            L.stints.append(dict(season=y, key=k, eff=eff, reinst=rein, list=lst, injury=injury, moves=mv,
                                 to60=[m[0] for m in mv if m[3] == "60-day IL" and m[2] == "PLACED"]))
        for ls in av["lists"]:
            s, e = ls["s"], ls["e"]
            dd = cg[c0][s]["date"]
            back = cg[c0][min(e, len(cg[c0]) - 1)]["date"]
            nm = "paternity list" if ls["kind"] == "paternity" else "bereavement list"
            L.lists.append(dict(season=y, key=k, club=club_on(L, y, k, dd), start=dd, back=back, list=nm))


# ---------------------------------------------------------------------------------------------------------- the design
# the club's designed players and the signing's namesake pitcher: their names are the build's, never redrawn
DESIGNED = ("P4", "P1", "P2", "P3", "P5", "RC", "RSS", "RCF", "RRF", "INC", "V1", "V2", "V3", "V4", "V5", "qTWIN")
FIVE_BORN = {"P4": (1992, 9, 14), "P1": (1995, 10, 2), "P2": (1993, 11, 21), "P3": (1996, 8, 6), "P5": (1994, 12, 9)}
FIVE_POS = {"P4": "3B", "P1": "1B", "P2": "1B", "P3": "LF", "P5": "2B"}
FIVE_TALENT = {"P4": 1.1, "P1": 1.3, "P2": 1.2, "P3": 1.0, "P5": 0.8}


def designed_name(L, k):
    """A name for one of the club's designed players: no origin outside the United States twice among them, and no
    first name or surname shared with another of them."""
    taken = L.design.setdefault("names", [])
    for attempt in range(60):
        r = K.rng("name", k, attempt)
        trial = set(L.used_names)
        nm, org = NM.draw_name(r, trial)
        first, last = nm.replace(" Jr.", "").split(" ", 1)
        if any(first == f or last == s for f, s, _ in taken):
            continue
        if org != "US" and any(o == org for _, _, o in taken):
            continue
        taken.append((first, last, org))
        return nm, org
    raise RuntimeError("no designed name")


def setup_design(L):
    r = K.rng("design")
    locked = defaultdict(dict)
    slot = defaultdict(dict)
    avail = defaultdict(dict)
    trades = defaultdict(list)
    # the five signings, at their old clubs from 2021 to 2026
    for k in K.SIGN_ORDER:
        by, bm, bd = FIVE_BORN[k]
        nm, org = designed_name(L, k)
        p = new_player(L, K.rng("make", k), FIVE_POS[k], by, talent=FIVE_TALENT[k], name=nm, origin=org, key=k)
        p.born = dt.date(by, bm, bd)
        for y in K.HIST:
            locked[y][k] = (OLD_CLUB[k], FIVE_POS[k])
            slot[y][k] = K.SIGNINGS[k]["old_slot"]
    # the club's own: four core regulars kept into 2027, the incumbent first baseman (2025-2027) and the veterans whose
    # plate-appearance bonuses the payments ask covers
    core = {"RC": ("C", 1995, 1.4), "RSS": ("SS", 1997, 1.4), "RCF": ("CF", 1998, 1.5), "RRF": ("RF", 1996, 1.6)}
    for k, (pos, by, t) in core.items():
        nm, org = designed_name(L, k)
        new_player(L, K.rng("make", k), pos, by, talent=t, key=k, name=nm, origin=org)
        for y in (2023, 2024, 2025, 2026):
            locked[y][k] = (K.CLUB, pos)
    vets = {   # key: position, born, talent, seasons as the club's starter
        "INC": ("1B", 1994, 0.9, (2025, 2026)),
        "V1": ("1B", 1989, 0.9, (2023, 2024)),
        "V3": ("1B", 1991, 0.7, (2023, 2024)),
        "V2": ("LF", 1992, 1.0, (2024, 2025, 2026)),
        "V4": ("3B", 1993, 0.8, (2025,)),
        "V5": ("2B", 1991, 0.6, (2026,)),
    }
    vpos = {"INC": "1B", "V1": "DH", "V3": "1B", "V2": "LF", "V4": "3B", "V5": "2B"}
    for k, (pos, by, t, seasons) in vets.items():
        nm, org = designed_name(L, k)
        new_player(L, K.rng("make", k), pos, by, talent=t, key=k, name=nm, origin=org)
        for y in seasons:
            locked[y][k] = (K.CLUB, vpos[k])
    locked[2027]["INC"] = (K.CLUB, "BENCH")
    # deadline trades: the club's third baseman to New Orleans (2025), P2 to Oklahoma City while on the injured list
    trades[2025].append(dict(key="V4", frm=K.CLUB, to="NOL", date=dt.date(2025, 7, 28), pos="3B"))
    trades[2026].append(dict(key="P2", frm=OLD_CLUB["P2"], to=P2_TRADED_TO, date=dt.date(2026, 7, 30), pos="DH"))
    # the five's seasons since 2024, as designed (stints: first missed game on or after `from`, games missed, the
    # days between the day the stint took effect and the move, the 60-day placement and the rehabilitation assignment)
    avail[2024]["P4"] = dict(rest=3, stints=[dict(**{"from": dt.date(2024, 5, 4)}, games=58, lag=2, to60=18, rehab=7,
                                                   injury="left hamstring strain")])
    avail[2025]["P4"] = dict(rest=3)
    avail[2026]["P4"] = dict(rest=4, stints=[dict(**{"from": dt.date(2026, 9, 11)}, games=None, lag=2,
                                                   injury="right oblique strain")])
    avail[2024]["P1"] = dict(rest=2)
    avail[2025]["P1"] = dict(rest=3, lists=[dict(kind="paternity", games=2, **{"from": dt.date(2025, 6, 10)})])
    avail[2026]["P1"] = dict(rest=3, stints=[dict(**{"from": dt.date(2026, 7, 8)}, games=9, lag=2,
                                                   injury="right wrist sprain")])
    avail[2024]["P2"] = dict(rest=3, stints=[dict(**{"from": dt.date(2024, 8, 15)}, games=11, lag=2,
                                                   injury="lower back strain")])
    avail[2025]["P2"] = dict(rest=2)
    avail[2026]["P2"] = dict(rest=2, stints=[dict(**{"from": dt.date(2026, 6, 13)}, games=None, lag=2,
                                                   reinst=dt.date(2026, 8, 28), to60_date=dt.date(2026, 8, 1),
                                                   rehab_date=dt.date(2026, 8, 20), injury="right calf strain")])
    avail[2024]["P3"] = dict(rest=2, stints=[
        dict(**{"from": dt.date(2024, 5, 19)}, games=8, lag=1, injury="left hamstring strain"),
        dict(**{"from": dt.date(2024, 6, 2)}, games=11, lag=1, injury="left hamstring strain")])
    avail[2025]["P3"] = dict(rest=3)
    avail[2026]["P3"] = dict(rest=2)
    avail[2024]["P5"] = dict(rest=3, stints=[dict(**{"from": dt.date(2024, 8, 9)}, games=7, lag=1, list="7-day",
                                                   injury="concussion")])
    avail[2025]["P5"] = dict(rest=3, stints=[dict(**{"from": None}, games=12, lag=3, kind="spring",
                                                   eff=dt.date(2025, 3, 25), injury="right oblique strain")])
    avail[2026]["P5"] = dict(rest=3)
    L.design.update(locked=locked, slot=slot, avail=avail, trades=trades)


def run():
    L = League()
    setup_design(L)
    for y in K.HIST:
        if y == K.HIST[0]:
            r = K.rng("rosters", y)
            for c in CODES:
                L.rosters[(y, c)] = fresh_roster(L, r, c, y)
            apply_locks(L, y)
        else:
            offseason(L, y)
        simulate_season(L, y)
    plan_2027(L)
    pitchers(L)
    return L


def plan_2027(L):
    """The club's December 2026 depth chart: the four core regulars, the five signings, the incumbent to the bench."""
    R26 = L.rosters[(2026, K.CLUB)]
    bench = [k for k in R26["bench"] if L.players[k].age(2027) <= 35][:3] + ["INC"]
    lineup = [("CF", "RCF"), ("SS", "RSS"), ("RF", "RRF"), ("C", "RC"), ("3B", "P4"), ("1B", "P1"), ("DH", "P2"),
              ("LF", "P3"), ("2B", "P5")]
    L.plan = dict(lineup=[(i + 1, pos, k) for i, (pos, k) in enumerate(lineup)], bench=bench)
    for k in K.SIGN_ORDER:
        assert dict((kk, s) for s, _, kk in L.plan["lineup"])[k] == K.SIGNINGS[k]["slot"]


def pitchers(L):
    """Pitchers' injured-list stints (the moves and the weekly report carry them; pitchers do not bat). One of them
    shares his name with one of the five signings, as two players in a league of this size sometimes do."""
    r0 = K.rng("namesake")
    twin = new_player(L, r0, "P", 1997, key="qTWIN", name=L.players["P1"].name, origin="US")
    for y, club, eff, span, inj in ((2024, "CHA", dt.date(2024, 6, 21), 34, "right elbow inflammation"),
                                    (2026, "CHA", dt.date(2026, 4, 30), 19, "right lat strain")):
        L.club_of[(y, "qTWIN")] = club
        rein = eff + D(days=span)
        lag = int(r0.integers(1, 3))
        mv = [(eff + D(days=lag), club, "PLACED", "15-day IL", inj)]
        if span >= 25:
            mv.append((rein - D(days=6), club, "REHAB ASSIGNMENT", "15-day IL",
                       "rehabilitation assignment with %s" % AFFILIATE[club]))
        mv.append((rein, club, "ACTIVATED", "15-day IL", ""))
        L.stints.append(dict(season=y, key="qTWIN", eff=eff, reinst=rein, list="15-day", injury=inj, moves=mv, to60=[]))
    for y in (2024, 2025, 2026):
        od, last, _ = K.SEASON[y]
        r = K.rng("pitchers", y)
        for c in CODES:
            for _ in range(int(r.poisson(7.5))):
                k = "q%s%d%04d" % (c, y, int(r.integers(10000)))
                if k in L.players:
                    continue
                age = int(np.clip(round(r.normal(29, 3.5)), 22, 39))
                p = new_player(L, r, "P", y - age, key=k)
                L.club_of[(y, k)] = c
                if r.random() < 0.12:
                    eff = od - D(days=int(r.integers(3, 15)))
                    span = int(r.integers(15, 200))
                else:
                    eff = od + D(days=int(r.integers(5, 175)))
                    span = int(9 + np.exp(r.normal(2.7, 1.0)))
                span = max(span, 15)
                rein = eff + D(days=span)
                if rein > last:
                    rein = None
                lst = "15-day" if (r.random() < 0.9 or span < 60) else "60-day"
                inj = ["right elbow inflammation", "right shoulder strain", "left forearm tightness", "right lat strain",
                       "Tommy John surgery", "right elbow sprain", "blister, right middle finger", "left oblique strain",
                       "right rotator cuff strain", "lower back tightness"][int(r.integers(10))]
                lag = int(r.choice(4, p=[0.1, 0.3, 0.35, 0.25]))
                mv = [(eff + D(days=lag), c, "PLACED", lst + " IL", inj)]
                end = rein or dt.date(y, 10, 1)
                cur = lst
                if lst == "15-day" and (end - eff).days >= 60:
                    d60 = eff + D(days=int(r.integers(14, 30)))
                    mv.append((d60, c, "PLACED", "60-day IL", inj))
                    cur = "60-day"
                if rein is not None and (rein - eff).days >= 25:
                    dr = rein - D(days=int(r.integers(5, 15)))
                    mv.append((dr, c, "REHAB ASSIGNMENT", cur + " IL", "rehabilitation assignment with %s" % AFFILIATE[c]))
                if rein is not None:
                    mv.append((rein, c, "ACTIVATED", cur + " IL", ""))
                else:
                    mv.append((dt.date(y, 11, int(r.integers(3, 7))), c, "REINSTATED", cur + " IL", ""))
                L.stints.append(dict(season=y, key=k, eff=eff, reinst=rein, list=lst, injury=inj, moves=mv, to60=[]))
