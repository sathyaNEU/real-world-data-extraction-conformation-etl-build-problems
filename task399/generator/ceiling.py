"""The cracker and mirror sheets as code, on the cut pack: each response route's ask figures recomputed from
target/ and scored against the goldens in figures.json (a hit is within half a unit of the stated rounding, 0.05
hours), then the pair ceiling on 38, 7 and 55. Usage: python3 ceiling.py [target_dir]"""
import bisect
import collections
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

import openpyxl

from verify import as_date, rows_csv, sheet, ts, utc_of_local

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
UTC = dt.timezone.utc
QN = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
QB = [dt.datetime(2025, 10, 1), dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1),
      dt.datetime(2026, 10, 1)]
W0, W1 = dt.datetime(2025, 10, 1), dt.datetime(2026, 10, 1)


class Pack:
    def __init__(self, T):
        J = lambda *p: os.path.join(T, *p)
        lay = json.load(open(J("control_system", "workstation_layout_export_r8.2.1.json"), encoding="utf-8"))
        self.desk = {w["desk"]: w["number"] for w in lay["ws_list"]}
        self.sub_ws = {s["subarea_code"]: s["ws"] for s in lay["ars_subareas"]}
        self.old = {s["replaces"]: s["subarea_code"] for s in lay["ars_subareas"]}
        comp = sheet(J("staffing", "signaller_competence_register.xlsx"), "Competence")
        k = comp[0].index("Date qualified")
        self.qual = {str(r[0]): as_date(r[k]) for r in comp[1:] if r[0]}
        self.duty = {}
        wb = openpyxl.load_workbook(J("staffing", "signalling_roster_2025-26_P07-P13.xlsx"), read_only=True)
        for name in [s for s in wb.sheetnames if s.startswith("P")]:
            rr = [list(x) for x in wb[name].iter_rows(values_only=True)]
            d0 = dt.datetime.strptime(re.search(r"(\d\d/\d\d/\d{4}) to", rr[0][0]).group(1), "%d/%m/%Y").date()
            for row in rr[3:]:
                if row and row[1]:
                    for j, v in enumerate(row[2:]):
                        if v in ("D", "N", "RD", "RN"):
                            self.duty[(str(row[1]), d0 + dt.timedelta(days=j), v[-1])] = (
                                self.desk[str(row[0]).upper()] if v in ("D", "N") else None)
        wb.close()
        lr = sheet(J("staffing", "signalling_roster_2026-27_P01-P07.xlsx"), "Roster")
        h = lr[0]
        for row in lr[1:]:
            kind = row[h.index("Duty")]
            if kind in ("DAY", "NIGHT", "RELIEF DAY", "RELIEF NIGHT"):
                self.duty[(str(row[h.index("Staff no")]), as_date(row[h.index("Duty date")]),
                           "N" if "NIGHT" in kind else "D")] = None if kind.startswith("RELIEF") else row[h.index("Desk")]
        self.changes = rows_csv(J("staffing", "roster_changes_2025-26_2026-27.csv"))
        self.acts = collections.defaultdict(list)
        self.at_desk = collections.defaultdict(list)
        for r in rows_csv(J("control_system", "roc_signaller_actions_20251001_20260930.csv")):
            w = self.ws(r["wkstn"])
            t = ts(r["event_utc"])
            self.acts[r["user"]].append((t, w))
            self.at_desk[w].append((t, r["user"]))
        for v in list(self.acts.values()) + list(self.at_desk.values()):
            v.sort()
        self.ars = rows_csv(J("control_system", "ars_status_log_20251001_20260930.csv"))

    def ws(self, v):
        v = str(v).strip()
        return v[:3] if re.match(r"^W0\d", v) else self.desk[v.upper()]


def two_years(q):
    try:
        return q.replace(year=q.year + 2)
    except ValueError:
        return q.replace(year=q.year + 2, day=28)


def hours(P, identity_from_log, clock_aware):
    def bounds(day, sh):
        s = dt.datetime(day.year, day.month, day.day, 7 if sh == "D" else 19)
        return s, s + dt.timedelta(hours=12)
    cover = {}
    for (sn, day, sh), desk in P.duty.items():
        s0, s1 = bounds(day, sh)
        if s1 <= W0 or s0 >= W1:
            continue
        if desk is None:
            a, b = utc_of_local(s0), utc_of_local(s1)
            n = collections.Counter(w for t, w in P.acts.get(sn, []) if a <= t < b)
            desk = n.most_common(1)[0][0]
        cover[(desk, day, sh)] = [(sn, s0, s1)]
    for r in P.changes:
        day = dt.datetime.strptime(r["duty_date"], "%d/%m/%Y").date()
        s0, s1 = bounds(day, r["duty"])
        if s1 <= W0 or s0 >= W1:
            continue
        desk = P.ws(r["desk"])
        hh, mm = map(int, r["from"].split(":"))
        frm = dt.datetime(day.year, day.month, day.day, hh, mm)
        if frm < s0:
            frm += dt.timedelta(days=1)
        if r["change_type"] == "Sickness cover" and frm > s0:
            cover[(desk, day, r["duty"])] = [(cover[(desk, day, r["duty"])][0][0], s0, frm), (r["worked_by"], frm, s1)]
        else:
            cover[(desk, day, r["duty"])] = [(r["worked_by"], s0, s1)]
    out = collections.defaultdict(float)
    for (desk, day, sh), lst in cover.items():
        for sn, a, b in lst:
            if identity_from_log:
                L2 = P.at_desk[desk]
                x, y = utc_of_local(a), utc_of_local(b)
                n = collections.Counter(u for t, u in L2[bisect.bisect_left(L2, (x, "")):bisect.bisect_left(L2, (y, ""))])
                if n:
                    top = n.most_common()
                    sn = sorted(u for u, k in top if k == top[0][1])[0]
            a, b = max(a, W0), min(b, W1)
            q = P.qual[sn]
            edges = [a] + [t for t in (dt.datetime.combine(q, dt.time()), dt.datetime.combine(two_years(q), dt.time()))
                           if a < t < b] + [b]
            for x, y in zip(edges, edges[1:]):
                band = "first two years" if q <= x.date() < two_years(q) else "other"
                span = (utc_of_local(y) - utc_of_local(x)) if clock_aware else (y - x)
                out[(desk, band)] += span.total_seconds() / 3600
    return out


def ars(P, servers, b_clock, users_only=False, expand_ws=True):
    ev = []
    for r in P.ars:
        if r["server"] not in servers or (users_only and not r["user"]):
            continue
        code = r["subarea"]
        if code in P.sub_ws:
            tg = [code]
        elif code in P.old:
            tg = [P.old[code]]
        elif expand_ws:
            w = P.ws(code)
            tg = sorted(s for s, x in P.sub_ws.items() if x == w)
        else:
            continue
        t = ts(r["logged_utc"])
        if r["server"] == "ROC-B" and b_clock:
            t = t.replace(tzinfo=ZoneInfo("Europe/Berlin")).astimezone(UTC).replace(tzinfo=None)
        for sa in tg:
            ev.append((t, sa, r["state"]))
    ev.sort()
    state, since, last = {}, {}, {}
    lo, hi = utc_of_local(W0), utc_of_local(W1)
    spans = collections.defaultdict(list)
    for t, sa, st in ev:
        if (sa, st) in last and (t - last[(sa, st)]).total_seconds() <= 2:
            continue
        last[(sa, st)] = t
        if sa not in state:
            state[sa] = "ON"
            if st == "ON":
                spans[sa].append((lo, t))
        if st == "OFF" and state[sa] == "ON":
            since[sa] = t
        elif st == "ON" and state[sa] == "OFF":
            spans[sa].append((since[sa], t))
        state[sa] = st
    for sa, st in state.items():
        if st == "OFF":
            spans[sa].append((since[sa], hi))
    out = collections.defaultdict(float)
    for sa, lst in spans.items():
        for a, b in lst:
            for k in range(4):
                x, y = max(a, utc_of_local(QB[k])), min(b, utc_of_local(QB[k + 1]))
                if y > x:
                    out[(P.sub_ws[sa], QN[k])] += (y - x).total_seconds() / 3600
    return out


def score(F, H, A):
    rows = {}
    for band in ("first two years", "other"):
        rows["hours, %s" % band] = [(w, H[(w, band)], F["hours_raw"][w][band]) for w in F["hours"]]
    for q in QN:
        rows["ARS off, %s" % q] = [(w, A[(w, q)], F["ars_raw"][w][q]) for w in F["ars"]]
    return {k: [(w, x, g, abs(x - g) < 0.05) for w, x, g in v] for k, v in rows.items()}


def main(T):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    P = Pack(T)
    routes = {
        "golden": (hours(P, True, True), ars(P, ("ROC-A", "ROC-B"), True)),
        "cracker (on the call; battery, every filed rule, relief desks from the log, both servers merged and "
        "deduplicated, old codes mapped, workstation-wide rows expanded)": (
            hours(P, False, True), ars(P, ("ROC-A", "ROC-B"), False)),
        "mirror (off the call; the natural read: shifts of twelve hours, the master server only)": (
            hours(P, False, False), ars(P, ("ROC-A",), False)),
        "over-cleaner (rows carrying a user only; the log's signed-on signaller)": (
            hours(P, True, True), ars(P, ("ROC-A", "ROC-B"), False, users_only=True)),
        "includer of both servers' clocks, missing the changes made on the day": (
            hours(P, False, True), ars(P, ("ROC-A", "ROC-B"), True)),
        "includer of the day's changes, missing B's clock": (
            hours(P, True, True), ars(P, ("ROC-A", "ROC-B"), False)),
    }
    kept = {}
    for name, (H, A) in routes.items():
        S = score(F, H, A)
        n = sum(len(v) for v in S.values())
        hit = sum(1 for v in S.values() for r in v if r[3])
        kept[name] = hit / n
        print("%s\n   keeps %d of %d ask figures (%.1f per cent)" % (name, hit, n, 100.0 * hit / n))
        for k, v in S.items():
            miss = [abs(x - g) for w, x, g, ok in v if not ok]
            print("   %-28s %d of %d kept%s" % (k, sum(1 for r in v if r[3]), len(v),
                                              ", median miss %.1f h" % sorted(miss)[len(miss) // 2] if miss else ""))
    names = list(routes)
    assert kept[names[0]] == 1.0, "the golden route must reproduce every ask figure"
    lc, lm = kept[names[1]], kept[names[2]]
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * lm
    print("\ncracker on the call: %.1f; mirror off it: %.1f; pair %.1f" % (C, S, (C + S) / 2))
    print("both on the call (the second on the mirror's ask routes): %.1f" % ((C + 38 + 7 + 55 * lm) / 2))
    print("mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    best_inc = max(kept[n] for n in names[3:])
    print("best partial includer keeps %.1f per cent" % (100 * best_inc))
    return dict(cracker=lc, mirror=lm, pair=(C + S) / 2, both_on_call=(C + 38 + 7 + 55 * lm) / 2, kept=kept)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
