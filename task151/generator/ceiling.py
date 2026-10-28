"""task151 ceiling: the cracker, the mirror and every includer run on the cut pack, scored against the golden ask figures
in generator/figures.json, with the pair arithmetic on supplemental-stumping Part 0's weights (38 recommendation and
critical components, 7 instruction-following, 55 asks, 5 kept by a wrong call) and on the portal's own calibration (a
response off the call kept about 20 of the 38 at the 10-27 return) printed beside it.

The ask: the playing-time bonuses other than plate-appearance bonuses the club paid for each of the 2023, 2024 and 2025
seasons, player by player and in total (18 player rows and 3 totals, whole dollars).

The cracker is the careful solver of Part 1.1. It reads every value for what it says and executes the files' own
mappings: the earning-code table names the playing-time code (BPA, and E40 PERF BONUS migrated as BPA) and the
catch-all (E45 OTHER BONUS migrated as BOT, Other bonus); the register's "Other playing-time bonuses" column names the
players; it runs the battery (the legacy number that carries two names is split by the name on each line, the void and
its reversal net out) and puts each payment in the season it was earned (an October payment in that season, a January
payment in the season before). The mirror stops at the most attractive wrong rung: the same lines by the year paid.

The includers have found the first device (the legacy season-end payments to the pitchers on the catch-all):
  whole   the October and January lines, any of the three codes, taken whole;
  every   every line on the three codes to those players, any month, taken whole;
  full    the full handling of the first device and every one of its hazards: the October and January lines whatever
          the code, an All-Star bonus taken out where the October line exceeds its January twin by one of his award
          terms, each legacy line by its name, the void netted, each payment to its season. This is the gated case;
  double  the other full handling: twice the January half, each to the season before;
  cap     'full' with each row cut to the largest amount the player's terms allow at or below it (the terms check
          applied as a repair);
  round   'full' with each line his terms cannot hold split into a bonus his terms allow and the roundest remainder (a
          guess at a round non-bonus payment, no reconciliation);
  full2   'full' with the second device handled too: the salary each contract deferred to its end (the register's
          salary for each of its seasons less the salary lines paid in it) taken out of the season-end line after the
          contract's last season. The fair handling: it reproduces every figure.
Nothing here reads the generator or the world: the pack and figures.json only.

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
W_REC, W_IF, W_ASK, W_WRONG, W_WRONG_PORTAL = 38.0, 7.0, 55.0, 5.0, 20.0
SEASONS = (2023, 2024, 2025)
PATHS = ("cracker", "mirror", "whole", "every", "full", "double", "cap", "round", "full2")
INCLUDERS = ("whole", "every", "full", "double", "cap", "round", "full2")
ROUND_UNITS = (1000000, 500000, 250000, 100000, 50000, 25000, 10000, 5000, 1000)


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def span(text):
    a, b = (str(text).split("-") + [str(text)])[:2]
    return set(range(int(a), int(b) + 1))


class Pack:
    def __init__(self, folder):
        f = lambda n: os.path.join(folder, n)
        self.pay = rows(f("ral_payroll_player_earnings_2023_2026.csv"))
        self.codes = {r["earning_code"]: r for r in rows(f("ral_payroll_earning_codes.csv"))}
        wb = openpyxl.load_workbook(f("ral_player_contract_register_2023_2026.xlsx"), read_only=True)
        hdr, self.reg = None, []
        for r in wb["Register"].iter_rows(values_only=True):
            if r and r[0] == "Player":
                hdr = list(r)
                continue
            if hdr and r and r[0]:
                self.reg.append(dict(zip(hdr, r)))
        self.by_id = {str(r["Employee ID"]): r["Player"] for r in self.reg}
        self.by_name = {}
        for r in self.reg:
            last, first = r["Player"].split(", ")
            self.by_name["%s %s" % (fold(last).upper(), fold(first).upper())] = r["Player"]
        self.seasons = defaultdict(set)
        self.awards = defaultdict(set)
        self.terms = {}
        self.contracts = []
        for r in self.reg:
            text = r["Other playing-time bonuses (each season)"]
            if text:
                ss = span(r["Seasons"])
                self.seasons[r["Player"]] |= ss
                tt = [(int(a.replace(",", "")), len(re.findall(r"\d+", lines))) for a, lines in
                      re.findall(r"\$([\d,]+) (?:each )?for ([\d, and]+)", text)]
                for y in ss:
                    self.terms[(r["Player"], y)] = tt
                self.contracts.append((r["Player"], ss, {y: r.get("Salary %d" % y) for y in range(2023, 2027)}))
            for x in re.findall(r"\$([\d,]+) for", r["Award bonuses"] or ""):
                self.awards[r["Player"]].add(float(x.replace(",", "")))
        # the playing-time codes as the earning-code table gives them
        self.pt_codes = {c for c, r in self.codes.items() if r["description"] == "Playing-time bonus" or
                         r["migrated_as"] == "BPA"}
        self.catch_all = {c for c, r in self.codes.items() if r["migrated_as"] == "BOT"}
        self.salary_codes = {c for c, r in self.codes.items() if r["migrated_as"] == "SAL" or
                             r["description"] == "Player salary"}

    def who(self, r):
        e = r["employee_id"]
        if not e.isdigit():
            return self.by_id.get(e)
        return self.by_name.get(r["employee_name"])            # the battery: a number with two names, split by name

    def largest(self, name, y, v):
        sums = {0}
        for a, n in self.terms[(name, y)]:
            sums = {x + a * j for x in sums for j in range(n + 1)}
        return max(x for x in sums if x <= v + 0.5)

    def roundest(self, name, y, v):
        """The bonus his terms allow that leaves the roundest remainder of v (largest round unit dividing it, then the
        larger bonus)."""
        sums = {0}
        for a, n in self.terms[(name, y)]:
            sums = {x + a * j for x in sums for j in range(n + 1)}
        cands = []
        for b in sums:
            if b <= v + 0.5:
                r = round(v - b)
                u = next((u for u in ROUND_UNITS if r % u == 0), 1)
                cands.append((u, b))
        return max(cands)[1]

    def deferral(self):
        """The salary each contract deferred to its end, keyed by its last season: the register's salary for each of
        its seasons less the salary lines paid in it."""
        paid = defaultdict(float)
        for r in self.pay:
            if r["earning_code"] in self.salary_codes:
                paid[(self.who(r), int(r["pay_date"][:4]))] += float(r["amount"])
        out = {}
        for name, ss, sal in self.contracts:
            gap = sum(sal[y] - paid[(name, y)] for y in ss if sal.get(y))
            if gap > 0.5:
                out[(max(ss), name)] = gap
        return out


def paths(P, path):
    parts = defaultdict(lambda: defaultdict(float))
    for r in P.pay:
        name = P.who(r)
        if name not in P.seasons:
            continue
        d = dt.date.fromisoformat(r["pay_date"])
        code, amt = r["earning_code"], float(r["amount"])
        if path in ("cracker", "mirror", "double"):
            if code not in P.pt_codes:
                continue
            if path == "double":
                if d.month == 1:
                    parts[(d.year - 1, name)]["all"] += 2 * amt
                continue
            y = d.year if path == "mirror" else (d.year if d.month >= 7 else d.year - 1)
            parts[(y, name)]["all"] += amt
            continue
        if code not in P.pt_codes | P.catch_all:
            continue
        if path == "every":
            parts[(d.year if d.month >= 7 else d.year - 1, name)]["all"] += amt
        elif d.month == 10:
            parts[(d.year, name)]["oct"] += amt
        elif d.month == 1:
            parts[(d.year - 1, name)]["jan"] += amt
    held = P.deferral() if path == "full2" else {}
    out = {}
    for (y, name), p in parts.items():
        if y not in SEASONS or y not in P.seasons[name]:
            continue
        if "all" in p:
            v = p["all"]
        else:
            o = p["oct"] - held.get((y, name), 0.0)
            v = o + p["jan"]
            diff = round(o - p["jan"], 2)
            if path in ("full", "cap", "full2") and p["jan"] > 0.5 and diff > 0.5 and diff in P.awards[name]:
                v -= diff
            if path == "cap":
                v = P.largest(name, y, v)
            if path == "round" and v > P.largest(name, y, v) + 0.5:
                v = P.roundest(name, y, v)
        if abs(v) > 0.5:
            last, first = name.split(", ")
            out[(y, "%s %s" % (first, last))] = v
    return out


def golden():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))["deliverables"]
    g = {}
    for blk in fig["paid"]:
        y = int(blk["season"])
        for n, v in blk["rows"]:
            g[(y, n)] = float(v.replace("$", "").replace(",", ""))
        g[(y, "total")] = float(blk["total"].replace("$", "").replace(",", ""))
    return g


def score(got, g):
    tot = defaultdict(float)
    for (y, n), v in got.items():
        tot[y] += v
    out = []
    for (y, n), v in sorted(g.items()):
        mine = tot.get(y) if n == "total" else got.get((y, n))
        out.append(("%d %s" % (y, n), mine is not None and abs(mine - v) < 0.5, mine))
    return out


def pair(c, m, n, wrong=W_WRONG):
    """(one response on the call keeping c of n ask figures with the other off it keeping m, both off the call keeping
    c each)."""
    kc, km = W_ASK * c / n, W_ASK * m / n
    one = ((W_REC + W_IF + kc) + (wrong + W_IF + km)) / 2
    none_ = ((wrong + W_IF + kc) + (wrong + W_IF + kc)) / 2
    return one, none_


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
        g = golden()
        res = {p: score(paths(P, p), g) for p in PATHS}
    finally:
        if tmp:
            shutil.rmtree(tmp)
    n = len(g)
    if not n:
        raise SystemExit("ceiling.py: no golden ask figure in figures.json; nothing to measure")
    keep = {p: sum(1 for _, h, _ in r if h) for p, r in res.items()}
    print("pack: %s" % (src or "task151 target"))
    print("playing-time codes per the earning-code table: %s; catch-all: %s; salary: %s" % (
        sorted(P.pt_codes), sorted(P.catch_all), sorted(P.salary_codes)))
    print("%-30s" % "ask figure" + "".join("%-8s" % p for p in PATHS))
    for i, (lab, _, _) in enumerate(res["cracker"]):
        print("%-30s" % lab[:30] + "".join("%-8s" % ("hit" if res[p][i][1] else "miss") for p in PATHS))
    c, m = keep["cracker"], keep["mirror"]
    one, none_ = pair(c, m, n)
    one_p, none_p = pair(c, m, n, W_WRONG_PORTAL)
    print("cracker keeps %d of %d ask figures (%.1f of %.0f ask points); mirror keeps %d of %d (%.1f per cent of the ask "
          "weight)" % (c, n, W_ASK * c / n, W_ASK, m, n, 100.0 * m / n))
    print("the asks consume nothing the call's construction produces, so the cracker's and the mirror's ask rows do not "
          "depend on the call (checks.py SEP1, SEP2, SEP4, SEP5)")
    print("pair, one response on the call (the cracker) and one off it (the mirror): %.1f (portal calibration %.1f)" % (
        one, one_p))
    print("pair, neither on the call, both on the cracker's ask path (the portal's case): %.1f (portal calibration %.1f)"
          % (none_, none_p))
    for p in INCLUDERS:
        k = keep[p]
        o, nn = pair(k, k, n)
        op, nnp = pair(k, k, n, W_WRONG_PORTAL)
        print("includer '%s' keeps %d of %d: pair both off the call %.1f (portal calibration %.1f); one on the call and "
              "both includers %.1f (%.1f)" % (p, k, n, nn, nnp, o, op))
    return dict(cracker=c, mirror=m, n=n, pair_one=one, pair_none=none_, pair_one_portal=one_p,
                pair_none_portal=none_p, includers={p: keep[p] for p in INCLUDERS})


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
