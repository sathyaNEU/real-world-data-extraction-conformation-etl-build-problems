"""task151 ceiling: the cracker and the mirror run on the cut pack, scored against the golden ask figures in
generator/figures.json, and the pair arithmetic on supplemental-stumping Part 0's weights (38 recommendation and
critical components, 7 instruction-following, 55 asks, 5 kept by a wrong call).

The cracker is the careful solver of Part 1.1: it reads every governing sentence on the ask paths and executes it
(League Rules 22.1, 22.2, 22.3 to 22.7 and 22.9 on the transaction wire, the weekly report and the calendar; the
contract register's Notes on the payroll, with the plate appearances and starts each player made for the Club in the
batting lines), and runs the hygiene battery (ID joins, void netting, the pitchers' lines set apart by the register).
The mirror stops at the most attractive wrong rung: the move's own date as the date a stint took effect, and the
payroll's playing-time lines at face value as the plate-appearance bonuses. Neither reads generator code or the world;
both read only the pack.

    python3 task151/generator/ceiling.py                 the pack at <task>/target, or target.zip when absent
    python3 task151/generator/ceiling.py PATH            a pack folder or a zip"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
W_REC, W_IF, W_ASK, W_WRONG = 38.0, 7.0, 55.0, 5.0
MIN_DAYS = {"7-day": 7, "10-day": 10, "15-day": 15, "60-day": 60}


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def ymd(s):
    return dt.date.fromisoformat(s)


def mdy(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date()


def rows(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


class Pack:
    def __init__(self, folder):
        f = lambda n: os.path.join(folder, n)
        self.f = f
        # identities: the five by name from the term sheets' order, League IDs from the vendor's winter depth charts
        self.lg, self.name_lg = {}, {}
        for ws in openpyxl.load_workbook(f("hvbd_winter_depth_charts_2021_2026.xlsx"), read_only=True).worksheets:
            hdr = None
            for r in ws.iter_rows(values_only=True):
                if r and r[0] == "Tm":
                    hdr = list(r)
                    continue
                if hdr and r and r[0]:
                    self.lg.setdefault(r[4], int(r[6]))
                    first, last = r[4].split(" ", 1)
                    self.name_lg["%s, %s" % (last, first)] = int(r[6])
        self.cal = {int(r["season"]): (ymd(r["opening_day"]), ymd(r["last_scheduled_day"]))
                    for r in rows(f("league_calendar_2021_2027.csv"))}
        self.tx = json.load(open(f("lsf_transactions_2024_2026.json"), encoding="utf-8"))["transactions"]
        self.rep = rows(f("league_office_il_report_2024_2026.csv"))
        self.pay = rows(f("ral_payroll_player_earnings_2023_2026.csv"))
        self.hmap = {r["legacy_employee_no"]: r["employee_id"] for r in rows(f("ral_hris_legacy_employee_map.csv"))}
        wb = openpyxl.load_workbook(f("ral_player_contract_register_2024_2026.xlsx"), read_only=True)
        self.reg, hdr = [], None
        for r in wb["Register"].iter_rows(values_only=True):
            if r and r[0] == "Player":
                hdr = list(r)
                continue
            if hdr and r and r[0]:
                self.reg.append(dict(zip(hdr, r)))
        # plate appearances by player, season and club, in game order (both layouts, the crosswalk, the directory)
        xw = {r["legacy_id"]: int(r["player_id"]) for r in rows(f("lsf_player_id_crosswalk.csv"))}
        clubs = rows(f("league_club_directory.csv"))
        lc = {r["legacy_code"]: r["abbrev"] for r in clubs}
        tm = {int(r["team_id"]): r["abbrev"] for r in clubs}
        self.games = defaultdict(list)
        for r in rows(f("lsf_batting_2021_2024.txt"), "|"):
            d = mdy(r["GAME_DT"])
            if d.year >= 2024:
                pa = sum(int(r[c]) for c in ("AB", "BB", "HBP", "SH", "SF", "CI"))
                self.games[(d.year, xw[r["PLAYER_CD"]])].append((d, int(r["GAME_CT"]), lc[r["TEAM_CD"]], pa))
        for r in rows(f("lsf_batting_2025_2026.csv")):
            d = ymd(r["official_date"])
            self.games[(d.year, int(r["player_id"]))].append((d, int(r["game_number"]), tm[int(r["team_id"])],
                                                             int(r["pa"])))


def five(P):
    """The five signings, as the club's 2027 depth chart marks them (free agents signed this winter)."""
    names = []
    wb = openpyxl.load_workbook(P.f("ral_depth_chart_2027.xlsx"), read_only=True)
    for r in wb.worksheets[0].iter_rows(values_only=True):
        if r and isinstance(r[0], int) and r[4] and str(r[4]).startswith("Free agent"):
            names.append(r[2])
    return names


# ------------------------------------------------------------------------------------------------- Ask A (stints)
def stints(P, n):
    mv = sorted((t for t in P.tx if t["player_id"] == P.lg[n] and t["type"] in (
        "IL_PLACEMENT", "IL_ACTIVATION", "IL_REINSTATEMENT")), key=lambda t: (t["date"], t["transaction_id"]))
    out, cur = [], None
    for t in mv:
        d = ymd(t["date"])
        if t["type"] == "IL_PLACEMENT":
            if cur is None:                    # 22.3: a transfer does not end the placement
                cur = dict(placed=d)
        else:
            cur["end"] = d
            out.append(cur)
            cur = None
    if cur:
        out.append(dict(cur, end=None))
    return out


def ask_a(P, path):
    out = []
    for n in five(P):
        last, first = fold(n).split(" ", 1)[1].upper(), fold(n).split(" ", 1)[0].upper()
        for s in stints(P, n):
            if path == "cracker":              # 22.2 inverted on 22.9's report: the first date of reinstatement less
                rr = sorted((r for r in P.rep if r["player"] == "%s, %s" % (last, first) and
                             mdy(r["placed"]) == s["placed"]), key=lambda r: r["report_date"])
                eff = mdy(rr[0]["eligible"]) - dt.timedelta(days=MIN_DAYS[rr[0]["injured_list"]])
            else:                              # the mirror: the move's own date
                eff = s["placed"]
            od, last_day = P.cal[s["placed"].year]
            end = (s["end"] - dt.timedelta(days=1)) if s["end"] else last_day      # 22.7, 22.6
            out.append((fold(n), eff, (min(end, last_day) - max(eff, od)).days + 1))
    return out


# ------------------------------------------------------------------------------------------- Ask B (bonuses paid)
def ask_b(P, path):
    terms = {}
    for r in P.reg:
        t = r["Plate-appearance bonuses (each season)"]
        if t:
            m = re.match(r"\$([\d,]+) each for ([\d, and]+) plate appearances", t)
            a, b = (str(r["Seasons"]).split("-") + [str(r["Seasons"])])[:2]
            terms[r["Employee ID"]] = dict(name=r["Player"], amt=int(m.group(1).replace(",", "")),
                                           lines=[int(x) for x in re.findall(r"\d+", m.group(2))],
                                           seasons=range(int(a), int(b) + 1))
    out = defaultdict(float)
    for r in P.pay:
        e = P.hmap.get(r["employee_id"], r["employee_id"])
        d = ymd(r["pay_date"])
        pt = r["earning_code"] == "BPA" or (r["earning_code"] == "E40" and d.month in (10, 1))
        if e not in terms or not pt:
            continue
        y = d.year if d.month >= 7 else d.year - 1                     # the Notes: both halves are the season's
        if y not in (2024, 2025, 2026):
            continue
        if path == "mirror":                                          # the line at face value, voids netted
            out[(y, terms[e]["name"])] += float(r["amount"])
            continue
        if r["status"] in ("VOIDED", "VOID REVERSAL") or y not in terms[e]["seasons"]:
            continue
        t, n, c = terms[e], 0, 0
        for d2, g, club, pa in sorted(P.games[(y, P.name_lg[t["name"]])]):
            before, c = c, c + pa
            n += sum(1 for T in t["lines"] if before < T <= c and club == "RAL")   # lines reached for the Club
        out[(y, t["name"])] += t["amt"] * n / 2                         # the plate-appearance half of the season
    return {k: v for k, v in out.items() if abs(v) > 0.5}


# ------------------------------------------------------------------------------------------------------- scoring
def golden():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))["deliverables"]
    a = [(fold(s["player"]), dt.datetime.strptime(s["took_effect"], "%B %d, %Y").date(), int(s["days"]))
         for s in fig["stints"]]
    b = {}
    for blk in fig["paid"]:
        y = int(blk["season"])
        for n, v in blk["rows"]:
            b[(y, fold(n))] = float(v.replace("$", "").replace(",", ""))
        b[(y, "total")] = float(blk["total"].replace("$", "").replace(",", ""))
    return a, b


def score(P, path, ga, gb):
    A = ask_a(P, path)
    hits_a = []
    for n, eff, days in ga:
        mine = [x for x in A if x[0] == n and x[1] == eff]
        hits_a.append(("A date %s %s" % (n, eff), bool(mine)))
        hits_a.append(("A days %s %s" % (n, eff), bool(mine) and mine[0][2] == days))
    B = ask_b(P, path)
    tot = defaultdict(float)
    for (y, n), v in B.items():
        tot[y] += v
    hits_b = []
    for (y, n), v in gb.items():
        if n == "total":
            got = tot.get(y)
        else:
            got = next((B[k] for k in B if k[0] == y and fold(k[1]).split(", ")[::-1] == n.split(" ", 1)), None)
        hits_b.append(("B %d %s" % (y, n), got is not None and abs(got - v) < 0.5))
    return hits_a + hits_b


def pair(c, m, n):
    kc, km = W_ASK * c / n, W_ASK * m / n
    one = ((W_REC + W_IF + kc) + (W_WRONG + W_IF + km)) / 2
    none_ = ((W_WRONG + W_IF + kc) + (W_WRONG + W_IF + kc)) / 2
    mixed = ((W_WRONG + W_IF + kc) + (W_WRONG + W_IF + km)) / 2
    return one, none_, mixed, kc, km


def main(src=None):
    tmp = None
    folder = src or os.path.join(TASK, "target")
    if not os.path.isdir(folder):
        z = src if src and src.endswith(".zip") else os.path.join(TASK, "target.zip")
        tmp = tempfile.mkdtemp(prefix="t151ceil")
        zipfile.ZipFile(z).extractall(tmp)
        folder = tmp
    try:
        P = Pack(folder)
        ga, gb = golden()
        cr = score(P, "cracker", ga, gb)
        mi = score(P, "mirror", ga, gb)
    finally:
        if tmp:
            shutil.rmtree(tmp)
    n = len(cr)
    c, m = sum(1 for _, h in cr if h), sum(1 for _, h in mi if h)
    print("pack: %s" % (src or "task151 target"))
    print("%-34s %-8s %-8s" % ("ask figure", "cracker", "mirror"))
    for (lab, hc), (_, hm) in zip(cr, mi):
        print("%-34s %-8s %-8s" % (lab[:34], "hit" if hc else "miss", "hit" if hm else "miss"))
    one, none_, mixed, kc, km = pair(c, m, n)
    print("cracker keeps %d of %d ask figures (%.1f of %.0f ask points); mirror keeps %d of %d (%.1f per cent of the "
          "ask weight)" % (c, n, kc, W_ASK, m, n, 100.0 * m / n))
    print("pair, one response on the call (the cracker) and one off it (the mirror): %.1f" % one)
    print("pair, neither on the call, both on the cracker's ask path (the portal's case): %.1f" % none_)
    print("pair, neither on the call, one cracker and one mirror: %.1f" % mixed)
    return dict(cracker=c, mirror=m, n=n, pair_one=one, pair_none=none_, pair_mixed=mixed)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
