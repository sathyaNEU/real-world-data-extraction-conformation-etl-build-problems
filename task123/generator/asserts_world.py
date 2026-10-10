"""Assertions on the built world (before any file is written): the September call, the ladder, the
corpus and its rivals, convergence, and the clean-data and lens-swap tests (A1 to A38, A41 to A43)."""
import datetime as dt
import random
from collections import Counter

from common import (MARCH_CENSUSES, SEPT_CENSUS, EXTRACT_DATE, POTS, SEPT_POT, FLOOR, CAP, LINE_PCT,
                    natural_end, prev_census, fyq, qend, pct1, offer_for, strike_rate, fend, is_final)
from roster import Q
from screen import Book, screen, replay, filed_year_screen, published_row, eod
from world import CENSUS_DATES

T_SET = {"A5", "A6", "F1", "F2", "F3", "F4", "F5", "F6", "F7"}
MOVERS = {"BC1", "BC2", "BC3"}                 # 30 June to 31 March balance date during 2025-26
GAP = "GT"                                     # between operating-grant terms at the census (loop 3)
R6_SET = T_SET | {GAP}                         # the stop: scope read off the register's start and end dates
R5_OWN = {"BC1", "BC2"}                        # offered on one balance date, unscored on each return's year
R5_SET = R6_SET | R5_OWN
R4_OWN = {"M", "A2", "A3", "A4", "C1"}          # offered without rule 4.1, unscored under it
R4R_SET = T_SET | R4_OWN                       # the step-back on each return's own year, without rule 4.1
R4_SET = R5_SET | R4_OWN                       # the step-back on one balance date, without rule 4.1
JUNE30 = {"A5", "A6"}                          # offered by the answer and the stop, not by R3
ANSWER = {"M", "A2", "A3", "A4", "A5", "A6"}   # the movers the step-back turns (R4's edge over R3)
DECOYS = {"Y1", "Y2", "Y3", "Y4"}
RESIDUE = {("D1", y) for y in range(2021, 2027)} | {("D2", 2022), ("D2", 2024), ("J1", 2023),
                                                   ("J2", 2024)}
CDAY = {("J3", 2023), ("D2", 2025), ("J4", 2026)}

RUNGS = {   # every rung below the answer takes scope from the grants register's dates (hardening loop 3)
    "R1": dict(unit="ref", basis="latest", q4src="portal", stepback="none", scope="dates"),
    "R2": dict(basis="latest", q4src="portal", stepback="none", scope="dates"),
    "R3": dict(q4src="portal", stepback="none", scope="dates"),
    "R4": dict(recency="off", labels="app", scope="dates"),
    "R5": dict(labels="app", scope="dates"),
    "R6": dict(scope="dates"),
}
RUNG_KEYS = ("R0", "R1", "R2", "R3", "R4", "R5", "R6")
R4RET = dict(recency="off")      # the loop 1 stop: the step-back on each return's own year, no rule 4.1
RIVALS = {
    "R1": RUNGS["R1"], "R2": RUNGS["R2"], "R3": RUNGS["R3"],
    "cutoff a week after the census": dict(cutoff_days=7),
    "V1 overdue only": dict(stepback="overdue"),
    "V2 December balance dates": dict(stepback="dec"),
    "V3 Q4 amended after census": dict(stepback="amended"),
    "V4 current window only": dict(prior="natural"),
    "V5 unfiled left unscored": dict(drop_unfiled=True),
    "T-strict census day exclusive": dict(inclusive=False),
    "T-extract register at 7 Oct": dict(reg_at="extract"),
    "fallback register Q4 else management": dict(stepback="none"),
}


class Checks:
    def __init__(self):
        self.n = 0
        self.ids = Counter()
        self.lines = []

    def ok(self, aid, cond, msg):
        self.n += 1
        self.ids[aid] += 1
        if not cond:
            raise AssertionError(f"{aid} FAILED: {msg}")
        self.lines.append(f"{aid}: {msg}")


def offered_names(s):
    return {r["org"] for r in s["rows"] if r["offer"]}


def alloc_map(s):
    a = {}
    for r in s["rows"]:
        if r["offer"]:
            a[r["org"]] = a.get(r["org"], 0) + r["offer"]
    return a


def replaced(s, t, pot):
    a, b = alloc_map(s), alloc_map(t)
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b)) / 2 / pot


def rank_by_fall(s, org):
    rows = sorted(s["rows"], key=lambda r: (-r["fall"], r["unit"]))
    for i, r in enumerate(rows, 1):
        if r["org"] == org:
            return i
    return None


def edge_gap(pct):
    x = round(pct * 10.0, 9)
    frac = x - int(x) if x >= 0 else x - int(x) + 1
    return abs(frac - 0.5) / 10.0


def sept_screens(W):
    book, c = W["book"], SEPT_CENSUS
    S = {"T": W["sept"]}
    for k, opt in RUNGS.items():
        S[k] = screen(book, c, SEPT_POT, **opt)
    S["R0"] = filed_year_screen(book, c, SEPT_POT)
    cells = {
        "per return, as held, no step-back": dict(unit="ref", q4src="portal", stepback="none"),
        "per return, latest, step-back": dict(unit="ref", basis="latest"),
        "per return, as held, step-back": dict(unit="ref"),
        "per organisation, latest, step-back": dict(basis="latest"),
        "30-June grantees not stepped back": dict(step_bal={3, 12}),
        "only 30-June grantees stepped back": dict(step_bal={6}),
        "current window stepped back, prior not": dict(prior="natural"),
        "register read as at the extract": dict(reg_at="extract"),
        "overdue only": dict(stepback="overdue"),
        "register fallback, no step-back": dict(stepback="none"),
        "census day exclusive": dict(inclusive=False),
        "4.1 read strictly (after, not on)": dict(recency="strict"),
        "4.1 against the census a year before": dict(recency="year"),
        "step-back on each return's own year, without rule 4.1": dict(recency="off"),
        "R4, per return, as held": dict(unit="ref", recency="off"),
        "R4, latest versions": dict(basis="latest", recency="off"),
        "one balance date, per return": dict(labels="app", unit="ref"),
        "one balance date, latest versions": dict(labels="app", basis="latest"),
        "one balance date, census day exclusive": dict(labels="app", inclusive=False),
        "one balance date, register at the extract": dict(labels="app", reg_at="extract"),
        # hardening loop 3: scope read off the register's start and end dates, alone and composed
        "scope from the register's dates, census day exclusive": dict(scope="dates", inclusive=False),
        "scope from the register's dates, register at the extract": dict(scope="dates", reg_at="extract"),
        "scope from the register's dates, per return": dict(scope="dates", unit="ref"),
        "scope from the register's dates, latest versions": dict(scope="dates", basis="latest"),
        "scope from the register's dates, without rule 4.1": dict(scope="dates", recency="off"),
        "data a week after the census": dict(cutoff_days=7),
    }
    for k, opt in cells.items():
        S[k] = screen(book, c, SEPT_POT, **opt)
    return S


def first_outside(s):
    under = sorted([r for r in s["rows"] if r["pct"] < LINE_PCT], key=lambda r: -r["pct"])
    return under[0], under[1]


def check_world(W, C):
    by, book = W["by"], W["book"]
    S = sept_screens(W)
    W["S"] = S
    T = S["T"]
    rows = {r["org"]: r for r in T["rows"]}
    elig = [r for r in T["rows"] if r["pct"] >= LINE_PCT]
    rate = T["rate"]
    tot_r = sum(offer_for(rate, r["fall"]) for r in elig)
    tot_n = sum(offer_for(rate + 1, r["fall"]) for r in elig)

    # A1-A4: the call
    C.ok("A1", 3600 <= rate <= 4800, f"answer rate {rate/100:.2f} cents in [36.00, 48.00]")
    C.ok("A1", tot_r <= SEPT_POT < tot_n, f"highest hundredth within the pot: {tot_r} <= {SEPT_POT} < {tot_n}")
    C.ok("A2", SEPT_POT - tot_r >= 25 and tot_n - SEPT_POT >= 25,
         f"remainder {SEPT_POT - tot_r} and next-step overshoot {tot_n - SEPT_POT} both >= 25")
    C.ok("A3", offered_names(T) == T_SET, f"the answer offers the 9 designed grantees: {sorted(offered_names(T))}")
    C.ok("A3", all((r["offer"] > 0) == (r["pct"] >= 10.0) for r in T["rows"]),
         "offered set equals the round rules applied to the answer's falls")
    C.ok("A3", offered_names(S["R6"]) == R6_SET, f"the stop (R6) offers its 10: {sorted(offered_names(S['R6']))}")
    C.ok("A3", offered_names(S["R5"]) == R5_SET, f"R5 offers its 12: {sorted(offered_names(S['R5']))}")
    C.ok("A3", offered_names(S["R4"]) == R4_SET, f"R4 offers its 17: {sorted(offered_names(S['R4']))}")
    r4r = S["step-back on each return's own year, without rule 4.1"]
    C.ok("A3", offered_names(r4r) == R4R_SET, f"the step-back without rule 4.1 on each return's own year offers its 14")
    C.ok("A4", len(T["rows"]) == 132 and len(S["R6"]["rows"]) == 133 and len(S["R5"]["rows"]) == 136
         and len(S["R4"]["rows"]) == 150 and len(r4r["rows"]) == 149 and len(S["R2"]["rows"]) == 148
         and len(S["R3"]["rows"]) == 148 and len(S["R1"]["rows"]) == 155,
         f"scored: answer {len(T['rows'])}, R6 {len(S['R6']['rows'])}, R5 {len(S['R5']['rows'])}, "
         f"R4 {len(S['R4']['rows'])}, R2 {len(S['R2']['rows'])}, R3 {len(S['R3']['rows'])}, R1 rows {len(S['R1']['rows'])}")
    # A5-A7: the ladder (the answer is the highest rate on the grid)
    for k, lo in (("R0", 1.15), ("R1", 1.40), ("R2", 1.40), ("R3", 1.40), ("R4", 2.00), ("R5", 1.40),
                  ("R6", 1.20)):
        C.ok("A5", rate >= lo * S[k]["rate"], f"answer at {rate/S[k]['rate']:.3f}x {k} ({S[k]['rate']/100:.2f}; floor {lo})")
    names = {k: offered_names(S[k]) for k in ("T",) + RUNG_KEYS}
    ks = list(names)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            C.ok("A6", names[ks[i]] != names[ks[j]], f"{ks[i]} and {ks[j]} offer different names")
    for k, lo_n, lo_p in (("R0", 4, 0.25), ("R1", 3, 0.25), ("R2", 3, 0.25), ("R3", 6, 0.35), ("R4", 7, 0.45),
                          ("R5", 3, 0.25), ("R6", 1, 0.15)):
        dn = len(names[k] ^ names["T"])
        rp = replaced(S[k], T, SEPT_POT)
        C.ok("A7", dn >= lo_n and rp >= lo_p, f"{k}: {dn} names differ from the answer, {rp:.1%} of the pot re-placed")
    C.ok("A7", not (names["T"] - names["R6"]) and names["R6"] - names["T"] == {GAP},
         "the answer's offers are the stop's less the grantee between terms at the census")
    C.ok("A7", names["R5"] - names["R6"] == R5_OWN,
         "on one balance date the stop also offers the two balance-date movers")
    C.ok("A7", names["R4"] - names["R5"] == R4_OWN and offered_names(r4r) - names["T"] == R4_OWN,
         "rule 4.1 takes the same five offers out on either calendar")
    # A8-A11: the grid
    for k in ("30-June grantees not stepped back", "current window stepped back, prior not",
              "4.1 read strictly (after, not on)"):
        C.ok("A8", S[k]["rate"] >= 1.10 * rate, f"partial cell '{k}' at {S[k]['rate']/rate:.3f}x the answer")
    C.ok("A8", S["only 30-June grantees stepped back"]["rate"] <= 0.80 * rate,
         f"partial cell 'only 30-June grantees stepped back' (the June window for the fourteen) at "
         f"{S['only 30-June grantees stepped back']['rate']/rate:.3f}x")
    for k in ("per return, as held, step-back", "per organisation, latest, step-back",
              "per return, latest, step-back", "R4, per return, as held", "R4, latest versions",
              "step-back on each return's own year, without rule 4.1", "one balance date, per return",
              "one balance date, latest versions", "one balance date, census day exclusive",
              "one balance date, register at the extract", "scope from the register's dates, census day exclusive",
              "scope from the register's dates, register at the extract", "scope from the register's dates, per return",
              "scope from the register's dates, latest versions",
              "scope from the register's dates, without rule 4.1", "data a week after the census"):
        C.ok("A9", S[k]["rate"] <= 0.92 * rate, f"cell '{k}' {100*(S[k]['rate']/rate-1):+.1f}%")
    ce = S["census day exclusive"]
    C.ok("A10", ce["rate"] == rate and alloc_map(ce) == alloc_map(T) and len(ce["rows"]) == len(T["rows"]) - 14,
         f"census day exclusive: same rate and offers, {len(ce['rows'])} scored against {len(T['rows'])}")
    rx = S["register read as at the extract"]
    C.ok("A10", rx["rate"] == rate and alloc_map(rx) == alloc_map(T) and len(rx["rows"]) == len(T["rows"]) + 6,
         f"register read as at the extract: same rate and offers, {len(rx['rows'])} scored against {len(T['rows'])}")
    # R3 on the answer's scope (the grid cells below change one convention from the answer, scope included)
    r3rows = {r["org"]: published_row(r) for r in screen(book, SEPT_CENSUS, SEPT_POT, q4src="portal",
                                                          stepback="none")["rows"]}
    fb = {r["org"]: published_row(r) for r in S["register fallback, no step-back"]["rows"]}
    ov = {r["org"]: published_row(r) for r in S["overdue only"]["rows"]}
    yr = S["4.1 against the census a year before"]
    C.ok("A11", fb == r3rows, "register fallback equals R3 on every row (on the answer's scope)")
    C.ok("A11", ov == r3rows, "overdue-only equals R3 at September (on the answer's scope)")
    C.ok("A11", published_rows(yr) == published_rows(r4r),
         "4.1 read against the census a year before equals the step-back without the clause")
    # A12-A16: the line and the bins
    band = [r["org"] for r in T["rows"] if 8.5 < r["pct"] < 11.5]
    C.ok("A12", not band, f"no answer fall within 1.5 points of the line ({band})")
    first, second = first_outside(T)
    f4, _ = first_outside(S["R4"])
    C.ok("A13", first["org"] == "L_dual" and 6.0 <= first["pct"] <= 8.5 and first["pct"] - second["pct"] >= 0.3
         and f4["org"] != first["org"],
         f"first outside the line {first['org']} at {first['pct']:.2f} (next {second['pct']:.2f}); R4's is {f4['org']} at {f4['pct']:.2f}")
    # hardening loop 2: "first outside the line" converges. In screen order (largest dollar fall first)
    # the first grantee not offered is the same grantee as the largest fall per cent under the line.
    unoff = sorted([r for r in T["rows"] if not r["offer"]], key=lambda r: (-r["fall"], r["unit"]))
    C.ok("A13", unoff[0]["org"] == first["org"] and unoff[0]["fall"] >= 1.10 * unoff[1]["fall"],
         f"first outside in screen order is also {unoff[0]['org']} (fall {unoff[0]['fall']:,}; next {unoff[1]['org']} "
         f"{unoff[1]['fall']:,})")
    capped = [r["org"] for r in T["rows"] if r["offer"] == CAP]
    floored = [r["org"] for r in T["rows"] if r["offer"] == FLOOR]
    C.ok("A14", capped == ["F1"] and not floored, f"cap binds for {capped} only; no offer at the floor ({floored})")
    C.ok("A14", not any(r["offer"] == CAP for k in ("R6", "R5", "R4", "R3") for r in S[k]["rows"]),
         "the cap binds under the answer only: neither the stop (R6), R5, R4 nor R3 caps an offer")
    falls = [r["fall"] for r in T["rows"]]
    C.ok("A15", len(set(falls)) == len(falls), "no two scored grantees share a dollar fall")
    gaps = [(edge_gap(r["pct"]), r["org"]) for r in T["rows"]]
    C.ok("A16", min(gaps)[0] >= 0.02, f"every answer fall per cent at least 0.02 from an x.x5 edge (min {min(gaps)[0]:.4f}, {min(gaps)[1]})")
    # A17: filing counts at the census
    in_scope = {r["org"] for r in S["R3"]["rows"]} | {r["org"] for r in r4r["rows"]}
    unf31 = sorted(k for k in in_scope if by[k].bal == 3 and not book.received(k, Q(2026, 3), SEPT_CENSUS))
    unf30 = sorted(k for k in in_scope if by[k].bal == 6 and not book.received(k, Q(2026, 6), SEPT_CENSUS))
    dday = sorted(k for k in in_scope if by[k].bal == 3 and W["annual"][(k, Q(2026, 3))].received == SEPT_CENSUS)
    octs = sorted(k for k in in_scope if by[k].bal == 3 and W["annual"][(k, Q(2026, 3))].received is not None
                  and SEPT_CENSUS < W["annual"][(k, Q(2026, 3))].received <= EXTRACT_DATE)
    C.ok("A17", len(unf31) == 17 and len(unf30) == 18 and MOVERS <= set(unf31),
         f"unfiled at the census: {len(unf31)} (31 March, the three movers among them) + {len(unf30)} (30 June)")
    C.ok("A17", len(dday) == 14 and len(octs) == 6, f"deadline-day receipts {len(dday)}; 1 to 7 October receipts {len(octs)}")
    # A55: the seventeen the answer does not score are exactly the 31 March grantees unfiled at the census,
    # each scored by the step-back without rule 4.1 on the twelve months to December 2025 the March 2026 round scored
    gone = sorted({r["org"] for r in r4r["rows"]} - set(rows))
    c26 = dt.date(2026, 3, 31)
    m26 = {r["org"]: r for r in W["corpus"][c26]["rows"]}
    r4rm = {r["org"]: r for r in r4r["rows"]}
    C.ok("A55", gone == unf31 and all(r4rm[k]["end"] == Q(2025, 12) == m26[k]["end"] and
                                       published_row(r4rm[k])[:4] == published_row(m26[k])[:4] for k in gone),
         f"the answer leaves out exactly the {len(gone)} unfiled 31 March grantees, each on the March 2026 round's own twelve months")
    # A56: the decisive rung. The three movers' returns for the quarters to September 2025, December 2025
    # and March 2026 run within a year ending 31 March 2026; their latest annual return as held is for the
    # year to 30 June 2025 and none filed a June 2026 return. One balance date per organisation reads them
    # as 30 June grantees on twelve months to March 2026 (rule 4.1 keeps them); their own year makes March
    # 2026 a final quarter with no annual return, the twelve months end at December 2025 and rule 4.1
    # leaves them out.
    r5 = {r["org"]: r for r in S["R5"]["rows"]}
    mv_ok = all(by[k].cal_change and fend(by[k], Q(2026, 3)) == Q(2026, 3) and fend(by[k], Q(2025, 9)) == Q(2026, 3)
                and fend(by[k], Q(2025, 6)) == Q(2025, 6) and not book.received(k, Q(2026, 3), EXTRACT_DATE)
                and not book.by_org.get((k, Q(2026, 6))) and k in r5 and r5[k]["end"] == Q(2026, 3)
                and r4rm[k]["end"] == Q(2025, 12) and k not in rows for k in MOVERS)
    C.ok("A56", mv_ok, "the three movers: a nine-month year to 31 March 2026, no annual return for it and no June 2026 "
                       "return by the extract; R5 scores them on twelve months to March 2026, the answer not at all")
    falls5 = ", ".join(f"{k} {r5[k]['pct']:.2f}" for k in sorted(MOVERS))
    C.ok("A56", all(r5[k]["pct"] >= 11.5 for k in R5_OWN) and abs(r5["BC3"]["pct"]) <= 8.5,
         f"under R5 the movers fall {falls5} per cent")
    C.ok("A56", all(published_row(r5[k])[:4] == published_row(rows[k])[:4] for k in rows),
         "R5 and the answer agree on all 132 rows the answer scores")
    # A58 (hardening loop 3): the decisive rung. GT's operating-grant term ended on 31 July 2026 and the grant
    # was renewed from 1 November 2026 (approved 16 September 2026), so no term was in force at the census:
    # the register's start of the grant and end of its current term span the census, rule 3.1 leaves GT
    # out of the answer, and the stop scores and offers it on the window the answer would have used.
    g = by[GAP]
    g_end, g_restart, g_appr = g.gaps[0]
    r6 = {r["org"]: r for r in S["R6"]["rows"]}
    C.ok("A58", g.og_start <= SEPT_CENSUS <= g.og_end and g_end < SEPT_CENSUS < g_restart and g_appr < SEPT_CENSUS,
         f"{GAP}: grant {g.og_start} to {g.og_end}, term ended {g_end}, renewed from {g_restart} (approved {g_appr})")
    C.ok("A58", GAP not in rows and GAP in r6 and r6[GAP]["end"] == Q(2026, 6) and r6[GAP]["pct"] >= 11.5
         and book.received(GAP, Q(2026, 3), SEPT_CENSUS),
         f"the stop scores {GAP} on twelve months to June 2026 (NZ${r6[GAP]['cur']:,} against NZ${r6[GAP]['prior']:,}, "
         f"a fall of NZ${r6[GAP]['fall']:,}, {r6[GAP]['pct']:.2f} per cent) and offers it NZ${r6[GAP]['offer']:,}; "
         f"the answer does not")
    C.ok("A58", all(published_row(r6[k])[:4] == published_row(rows[k])[:4] for k in rows) and set(r6) - set(rows) == {GAP},
         "the stop and the answer agree on all 132 rows the answer scores and differ by the one grantee only")
    gpays = [p["inst_for"] for p in W["payments"] if p["org"] == GAP and p["prog"] == "OG"]
    C.ok("A58", not any(m in gpays for m in ((2026, 8), (2026, 9), (2026, 10))) and (2026, 7) in gpays,
         f"no operating instalment for August to October 2026 for {GAP}; the last paid was for July 2026")
    twins = [o for o in W["orgs"] if o.gaps and o.key != GAP]
    C.ok("A58", len(twins) == 3 and all(not any(e - dt.timedelta(days=20) <= c <= r_ + dt.timedelta(days=20)
                                                   for c in CENSUS_DATES) for o in twins for e, r_, _ in o.gaps),
         f"three earlier lapses ({', '.join(o.key for o in twins)}), none spanning a census or within 20 days of one")
    C.ok("A55", all(qend(r["end"]) >= prev_census(SEPT_CENSUS) for r in T["rows"]) and
         sum(1 for r in T["rows"] if qend(r["end"]) == prev_census(SEPT_CENSUS)) == 17,
         "every scored window ends on or after 31 March 2026; the 17 scored 30 June grantees end on it")
    # A18-A19: dominance and the movers
    r3 = {r["org"]: r for r in S["R3"]["rows"]}
    r3_elig = sum(r["fall"] for r in S["R3"]["rows"] if r["offer"])
    t_elig = sum(r["fall"] for r in T["rows"] if r["offer"])
    r4 = {r["org"]: r for r in r4r["rows"]}
    r4_elig = sum(r["fall"] for r in r4r["rows"] if r["offer"])
    own4 = sum(r4[k]["fall"] for k in R4_OWN) / r4_elig
    r5_elig = sum(r["fall"] for r in S["R5"]["rows"] if r["offer"])
    own5s = sum(r5[k]["fall"] for k in R5_OWN) / r5_elig
    C.ok("A18", own5s >= 0.12, f"R5's two balance-date movers hold {own5s:.1%} of its eligible falls")
    r6 = {r["org"]: r for r in S["R6"]["rows"]}
    r6_elig = sum(r["fall"] for r in S["R6"]["rows"] if r["offer"])
    own6 = r6[GAP]["fall"] / r6_elig
    C.ok("A18", own6 >= 0.15, f"the stop's own offer (the grantee between terms) holds {own6:.1%} of its eligible falls")
    own3 = sum(r3[k]["fall"] for k in DECOYS | {"C1"}) / r3_elig
    own5 = sum(rows[k]["fall"] for k in JUNE30) / t_elig
    C.ok("A18", own4 >= 0.45, f"rule 4.1's five removed offers hold {own4:.1%} of the step-back's eligible falls")
    C.ok("A18", own3 >= 0.20 and own5 >= 0.20,
         f"R3's own names hold {own3:.1%} of its eligible falls; the answer's (the two 30 June) {own5:.1%} of its")
    for k in sorted(DECOYS):
        C.ok("A19", k not in rows and r4[k]["pct"] <= 8.0 and r3[k]["pct"] >= 15.0,
             f"decoy {k}: unscored by the answer, R4 {r4[k]['pct']:.2f}, R3 {r3[k]['pct']:.2f}")
    for k in sorted(ANSWER):
        src = rows if k in rows else r4
        C.ok("A19", src[k]["pct"] >= 11.5 and r3[k]["pct"] <= 8.5,
             f"step-back mover {k}: {'answer' if k in rows else 'R4'} {src[k]['pct']:.2f}, R3 {r3[k]['pct']:.2f}")
    return S


def corpus_checks(W, C):
    book = W["book"]
    stats = {}
    tot_rows = sum(len(W["corpus"][c]["rows"]) for c in MARCH_CENSUSES)
    tot_off = sum(W["corpus"][c]["n_offers"] for c in MARCH_CENSUSES)
    C.ok("A20", [len(W["corpus"][c]["rows"]) for c in MARCH_CENSUSES] == [122, 128, 135, 141, 146, 149]
         and [W["corpus"][c]["n_offers"] for c in MARCH_CENSUSES] == [9, 10, 11, 12, 13, 16],
         f"corpus: {tot_rows} rows, {tot_off} offers, six rates")
    misses = {}
    for name, opt in RIVALS.items():
        m_rows, m_names, off_fail, rate_fail, cnt_fail = 0, [], 0, 0, 0
        for c in MARCH_CENSUSES:
            pub = W["corpus"][c]
            rv = screen(book, c, POTS[c.year], **opt)
            rp = replay(pub, rv)
            m_rows += rp["n_pub"] - rp["rows_back"]
            m_names += [(k, c.year) for k in rp["missed"]]
            off_fail += 0 if rp["offers_all"] else 1
            rate_fail += 0 if rp["rate_ok"] else 1
            cnt_fail += 0 if rp["count_ok"] else 1
        misses[name] = dict(rows=m_rows, names=m_names, off=off_fail, rate=rate_fail, cnt=cnt_fail)
    r0 = 0
    r0_back = 0
    for c in MARCH_CENSUSES:
        rp = replay(W["corpus"][c], filed_year_screen(book, c, POTS[c.year]))
        r0 += rp["n_pub"] - rp["rows_back"]
        r0_back += rp["rows_back"]
    misses["R0"] = dict(rows=r0, names=[], off=None, rate=None, cnt=None)
    W["rival_misses"] = misses
    m3 = misses["R3"]
    C.ok("A21", m3["rows"] == 10 and set(m3["names"]) == RESIDUE and m3["off"] == 0 and m3["rate"] == 0,
         f"R3 gives back {tot_rows - m3['rows']} of {tot_rows} rows, every offer and rate; misses {sorted(m3['names'])}")
    # A22: residue miss sizes
    for c in MARCH_CENSUSES:
        pub = {r["org"]: r for r in W["corpus"][c]["rows"]}
        r3 = {r["org"]: r for r in screen(book, c, POTS[c.year], **RUNGS["R3"])["rows"]}
        for k, y in sorted(RESIDUE):
            if y != c.year:
                continue
            a, b = pub[k], r3[k]
            di = abs(a["cur"] - b["cur"]) / a["cur"]
            dp = abs(a["pct"] - b["pct"])
            C.ok("A22", di <= 0.012 and dp <= 1.0 and not a["offer"] and not b["offer"]
                 and abs(a["pct"] - 10) >= 5 and abs(b["pct"] - 10) >= 5,
                 f"residue {k} {y}: income gap {di:.2%}, fall gap {dp:.2f} points, falls {a['pct']:.2f}/{b['pct']:.2f}")
    m2 = misses["R2"]
    C.ok("A23", m2["rows"] >= 40 and m2["off"] >= 4 and m2["rate"] >= 4,
         f"R2 misses {m2['rows']} rows, offers in {m2['off']} rounds, rates in {m2['rate']}")
    C.ok("A24", misses["R1"]["cnt"] == 6, f"R1 row count fails all six rounds")
    C.ok("A24", r0_back < 0.05 * tot_rows, f"R0 gives back {r0_back} of {tot_rows} rows")
    # A25: the twin pair
    ta, tb = W["by"]["TA"], W["by"]["TB"]
    cols = ("sector", "district", "bal", "og_start", "og_end")
    C.ok("A25", all(getattr(ta, a) == getattr(tb, a) for a in cols) and
         W["terms"]["TA"] == W["terms"]["TB"], "twins identical on every grants-register column")
    c25 = dt.date(2025, 3, 31)
    lat = {r["org"]: r for r in screen(book, c25, POTS[2025], basis="latest")["rows"]}
    pub = {r["org"]: r for r in W["corpus"][c25]["rows"]}
    C.ok("A25", (lat["TA"]["cur"], lat["TA"]["prior"], lat["TA"]["fall"]) ==
         (lat["TB"]["cur"], lat["TB"]["prior"], lat["TB"]["fall"]),
         f"twins identical on today's versions: fall {lat['TA']['pct']:.2f} per cent each")
    ratio = pub["TB"]["pct"] / pub["TA"]["pct"]
    C.ok("A25", 1.8 <= ratio <= 2.2 and pct1(pub["TA"]["pct"]) == 5.9 and pct1(pub["TB"]["pct"]) == 11.6,
         f"published falls {pct1(pub['TA']['pct'])} and {pct1(pub['TB']['pct'])} ({ratio:.2f}x)")
    r2_25 = screen(book, c25, POTS[2025], **RUNGS["R2"])
    r2o = {r["org"]: r for r in r2_25["rows"]}
    C.ok("A25", pub["TB"]["offer"] and not pub["TA"]["offer"] and r2o["TA"]["offer"] and r2o["TB"]["offer"]
         and r2_25["rate"] != W["corpus"][c25]["rate"],
         "on today's versions both twins are offered and the March 2025 rate fails; only the versions held at the census reproduce both")
    # A26: the rival family
    expect = {"V1 overdue only": 8, "V2 December balance dates": 12, "V4 current window only": 10,
              "V5 unfiled left unscored": 10, "T-strict census day exclusive": 3,
              "T-extract register at 7 Oct": 10, "fallback register Q4 else management": 10}
    for name, m in misses.items():
        C.ok("A26", m["rows"] >= 3, f"rival {name} misses {m['rows']} rows")
        if name in expect:
            C.ok("A26", m["rows"] == expect[name], f"rival {name} misses exactly {expect[name]}")
    C.ok("A26", misses["V3 Q4 amended after census"]["rows"] >= 10, "V3 misses at least 10")
    C.ok("A26", misses["R0"]["rows"] >= 760, f"R0 misses {misses['R0']['rows']} rows")
    C.ok("A26", len(misses) == 13, "thirteen rival rules scored")
    # A59 (hardening loop 3, determinism): the replay pins the data cutoff to the census day. One correction
    # was accepted four days after the March 2023 census; a cutoff a week after the census (where the
    # extract sits after the September census) gives that row back wrong.
    cases = W["params"]["_cutoff_cases"]
    wk = misses["cutoff a week after the census"]
    C.ok("A59", all(cs_ in wk["names"] for cs_ in cases) and wk["rows"] == 3,
         f"a cutoff a week after the census misses {wk['rows']} published rows, the three corrections accepted four "
         f"days after a census ({cases})")
    # A58 (corpus side): no grantee was between terms at any March census, so the scope read off the
    # register's dates gives back every pack; the grantee between terms at September is scored in all six
    gaps_at = [(o.key, c.year) for o in W["orgs"] for c in MARCH_CENSUSES for e, r_, _ in o.gaps if e < c < r_]
    C.ok("A58", not gaps_at, "no grantee was between terms at any March census")
    for c in MARCH_CENSUSES:
        d_ = screen(book, c, POTS[c.year], scope="dates")
        C.ok("A58", published_rows(d_) == published_rows(W["corpus"][c]),
             f"March {c.year}: scope read off the register's dates gives back the same pack")
    gt_rows = [r for c in MARCH_CENSUSES for r in W["corpus"][c]["rows"] if r["org"] == GAP]
    C.ok("A58", len(gt_rows) == 6 and all(abs(r["pct"] - 10) >= 4 and not r["offer"] for r in gt_rows),
         f"{GAP} is scored in all six March rounds, never offered, never within 4 points of the line")
    # A27-A29: blindness and the census-day receipts
    unf = []
    for c in MARCH_CENSUSES:
        for r in W["corpus"][c]["rows"]:
            o = W["by"][r["org"]]
            n = natural_end(c)
            for q in range(n - 3, n + 1):
                if is_final(o, q) and not book.received(o.key, q, c):
                    unf.append((o.key, c.year))
    C.ok("A27", set(unf) == RESIDUE and len(unf) == 10,
         "every year-end quarter inside a March window was on the register except the ten residue rows")
    t_eq = 0
    for c in MARCH_CENSUSES:
        r3 = {r["org"]: published_row(r) for r in screen(book, c, POTS[c.year], **RUNGS["R3"])["rows"]}
        for r in W["corpus"][c]["rows"]:
            if (r["org"], c.year) not in RESIDUE and r3[r["org"]] == published_row(r):
                t_eq += 1
    C.ok("A28", t_eq == tot_rows - 10, f"T and R3 identical on the other {t_eq} rows")
    cday = set()
    for (k, q4), ar in W["annual"].items():
        if ar.received in MARCH_CENSUSES:
            cday.add((k, ar.received.year))
    C.ok("A29", cday == CDAY and not any(d == dt.date(2024, 3, 31) for _, d in cday),
         f"census-day receipts {sorted(cday)}")
    ts = misses["T-strict census day exclusive"]
    C.ok("A29", set(ts["names"]) == CDAY, "each census-day receipt reproduces only with the census day inclusive")
    # A54: rule 4.1's census-before sentence is silent on the corpus. Every published window ends on or
    # after the census before it (J1 in 2023 and J2 in 2024 exactly on it), so the screen with the
    # sentence ignored gives back the same rows, offers and rates in all six rounds.
    on, before = [], []
    for c in MARCH_CENSUSES:
        pc = prev_census(c)
        for r in W["corpus"][c]["rows"]:
            e = qend(r["end"])
            if e < pc:
                before.append((r["org"], c.year))
            elif e == pc:
                on.append((r["org"], c.year))
    C.ok("A54", not before and sorted(on) == [("J1", 2023), ("J2", 2024)],
         f"no published window ends before the census before it; exactly on it: {sorted(on)}")
    for c in MARCH_CENSUSES:
        off = screen(book, c, POTS[c.year], recency="off")
        C.ok("A54", published_rows(off) == published_rows(W["corpus"][c]),
             f"March {c.year}: the screen without rule 4.1's sentence gives back the same pack")
    # A57: one balance date per organisation is as blind on the corpus as rule 4.1. Structurally: no
    # financial year of other than four quarters ends inside any March window (the movers' nine-month
    # year ends 31 March 2026, after the March 2026 window closes, and its first two quarters sit inside
    # that window as quarters one and two on either calendar). Case by case: the screen keyed to one
    # balance date gives back every pack.
    odd = []
    for c in MARCH_CENSUSES:
        n = natural_end(c)
        for r in W["corpus"][c]["rows"]:
            o = W["by"][r["org"]]
            for q in range(r["pend"] - 7, r["end"] + 1):
                if q >= 0 and (fend(o, q) != fend(o, q, "app") or is_final(o, q) != is_final(o, q, "app")):
                    if is_final(o, q) or is_final(o, q, "app"):
                        odd.append((r["org"], c.year, q))
    C.ok("A57", not odd, f"no year-end quarter inside a March window differs between the two calendars ({odd[:3]})")
    for c in MARCH_CENSUSES:
        one = screen(book, c, POTS[c.year], labels="app")
        C.ok("A57", published_rows(one) == published_rows(W["corpus"][c]),
             f"March {c.year}: the screen on one balance date per organisation gives back the same pack")
    mv_rows = sum(1 for c in MARCH_CENSUSES for r in W["corpus"][c]["rows"] if r["org"] in ("BC1", "BC2", "BC3"))
    C.ok("A57", mv_rows == 18, f"the three movers are scored in all six March rounds ({mv_rows} rows), never near the line")
    return misses


def flips_check(W, C):
    """A30: every rule the answer composes breaks at least one corpus case when flipped."""
    book = W["book"]
    flips = {
        "trailing four quarters (filed year instead)": None,
        "one row per organisation": dict(unit="ref"),
        "as held at the census": dict(basis="latest"),
        "latest version across the organisation's grants": dict(unit="op"),
        "fourth quarter only from a received annual return": dict(q4src="portal", stepback="none"),
        "not yet due still steps back": dict(stepback="overdue"),
        "prior window steps back with the current": dict(prior="natural"),
        "census day inclusive": dict(inclusive=False),
        "eight quarters required": dict(require8=False),
        "the latest accepted version, not the first filed": dict(basis="first"),
        "rule 4.1 on or after the census before, not strictly after": dict(recency="strict"),
        "data as at the census, not a week after it": dict(cutoff_days=7),
    }
    for name, opt in flips.items():
        broken = 0
        for c in MARCH_CENSUSES:
            pub = W["corpus"][c]
            rv = filed_year_screen(book, c, POTS[c.year]) if opt is None else screen(book, c, POTS[c.year], **opt)
            rp = replay(pub, rv)
            broken += (rp["n_pub"] - rp["rows_back"]) + (0 if rp["count_ok"] else 1)
        C.ok("A30", broken >= 1, f"flip '{name}' breaks {broken} corpus cases")
    # offer arithmetic flips, checked on the published rounds
    for name, fn in (("floor and cap", lambda r, f: (2 * r * f + 10000) // 20000),
                     ("whole-dollar half-up rounding", lambda r, f: min(max((r * f) // 10000, FLOOR), CAP))):
        broken = 0
        for c in MARCH_CENSUSES:
            pub = W["corpus"][c]
            el = [r for r in pub["rows"] if r["offer"]]
            rr, offs, _ = strike_rate([r["fall"] for r in el], POTS[c.year], offer_fn=fn)
            broken += sum(1 for r, o in zip(el, offs) if o != r["offer"])
        C.ok("A30", broken >= 1, f"flip '{name}' breaks {broken} published offers")
    broken = 0
    for c in MARCH_CENSUSES:
        pub = W["corpus"][c]
        el = [r for r in pub["rows"] if r["offer"]]
        rr, offs, _ = strike_rate([r["fall"] for r in el], POTS[c.year], step=10)
        broken += 0 if rr == pub["rate"] else 1
    C.ok("A30", broken >= 1, f"flip 'rate to the hundredth of a cent' (tenth instead) breaks {broken} rates")
    broken = 0
    for c in MARCH_CENSUSES:
        for r in W["corpus"][c]["rows"]:
            if pct1(100.0 * r["fall"] / r["cur"]) != pct1(r["pct"]):
                broken += 1
    C.ok("A30", broken >= 1, f"flip 'fall per cent on the prior twelve months' breaks {broken} rows")


def convergence_checks(W, C):
    book, annual = W["book"], W["annual"]
    # A31: a return on the register by a census has its true-up accepted by then, or exact management
    bad = []
    for (k, q4), ar in annual.items():
        if ar.received is None:
            continue
        lst = book.by_org.get((k, q4), [])
        if not lst:
            continue
        for c in CENSUS_DATES:
            if ar.received <= c:
                held = [v for v in lst if v.accepted <= eod(c)]
                if held and held[-1].ytd != ar.total:
                    bad.append((k, q4, c))
    C.ok("A31", not bad, f"every return on the register by a census has a trued-up or exact fourth quarter held ({len(bad)} exceptions)")
    order = [v for v in W["versions"] if v.accepted is not None and v.accepted <= v.submitted]
    C.ok("A32", not order, f"every accepted version was accepted after it was submitted ({len(order)} exceptions)")
    seq = {}
    bad_seq = 0
    for v in sorted(W["versions"], key=lambda v: (v.ref, v.q, v.no)):
        prev = seq.get((v.ref, v.q))
        if prev is not None and v.submitted < prev:
            bad_seq += 1
        seq[(v.ref, v.q)] = v.submitted
    C.ok("A32", bad_seq == 0, "version numbers follow submission order")
    near = [v for v in W["versions"] if v.accepted is not None and
            any(abs((v.accepted.date() - c).days) <= 1 for c in CENSUS_DATES)]
    C.ok("A32", not near, "no portal version accepted within a day of any census")
    gr = []
    for o in W["orgs"]:
        for d in (o.og_start, o.og_end):
            if any(abs((d - c).days) <= 20 for c in CENSUS_DATES):
                gr.append(o.key)
    for o in W["orgs"]:
        for e, r_, a_ in o.gaps:
            if any(abs((d - c).days) <= 20 for d in (e, r_) for c in CENSUS_DATES):
                gr.append(o.key)
    C.ok("A33", not gr, "no operating grant or term starts or ends within 20 days of a census")
    # A34: comparatives on total-income rows equal the prior year's own total as held at every census
    bad = 0
    checked = 0
    for v in W["versions"]:
        if v.accepted is None or v.q - 4 < 5:
            continue
        for c in CENSUS_DATES:
            if v.accepted > eod(c):
                continue
            held = book.ytd(v.org, v.q - 4, eod(c))
            if held is None:
                continue
            checked += 1
            if held != v.py_total:
                bad += 1
    C.ok("A34", bad == 0, f"comparative total equals the prior year's own total as held ({checked} checks)")
    # A35: rejected and withdrawn versions carry the accepted total
    bad = 0
    for (k, q), lst in book.all_by_org.items():
        for v in lst:
            if v.status != "accepted":
                prev = [a for a in lst if a.status == "accepted" and a.accepted <= v.submitted]
                if not prev or prev[-1].ytd != v.ytd:
                    bad += 1
    C.ok("A35", bad == 0, "rejected and withdrawn versions carry the accepted version's total income")
    # A36: row order does not matter
    rnd = random.Random(5)
    base = (W["sept"]["rate"], tuple(published_row(r) for r in W["sept"]["rows"]))
    for k in range(6):
        vs = list(W["versions"])
        rnd.shuffle(vs)
        b2 = Book(W["orgs"][::-1] if k % 2 else W["orgs"], vs, dict(reversed(list(annual.items()))))
        s2 = screen(b2, SEPT_CENSUS, SEPT_POT)
        C.ok("A36", (s2["rate"], tuple(published_row(r) for r in s2["rows"])) == base, f"row order {k+1} gives the same screen")
    C.ok("A37", max(v.q for v in W["versions"]) == Q(2026, 6) and
         all(qend(q4) <= dt.date(2026, 6, 30) for (_, q4) in annual if annual[(_, q4)].received),
         "no July to September 2026 return in the extract")
    octs = [o.key for o in W["orgs"] if o.bal == 3 and o.sept_status == "oct"]
    ok = all(book.by_org[(k, Q(2026, 3))][0].ytd == annual[(k, Q(2026, 3))].total for k in octs)
    C.ok("A38", ok and len(octs) == 6, "the six 1 to 7 October filers carry exact management fourth quarters")


def clean_data_checks(W, C):
    """A41-A43, and the lens-swap test, run on the answer, R3, R4, R5 and the stop (R6)."""
    import copy
    book, c = W["book"], SEPT_CENSUS
    T0 = published_rows(W["sept"])
    R30 = published_rows(screen(book, c, SEPT_POT, **RUNGS["R3"]))
    R40 = published_rows(screen(book, c, SEPT_POT, **RUNGS["R4"]))
    R50 = published_rows(screen(book, c, SEPT_POT, **RUNGS["R5"]))
    R60 = published_rows(screen(book, c, SEPT_POT, **RUNGS["R6"]))

    def four(b):
        """The answer, R3, R4, R5 and the stop (R6) on a repaired book."""
        return (published_rows(screen(b, c, SEPT_POT)), published_rows(screen(b, c, SEPT_POT, **RUNGS["R3"])),
                published_rows(screen(b, c, SEPT_POT, **RUNGS["R4"])),
                published_rows(screen(b, c, SEPT_POT, **RUNGS["R5"])),
                published_rows(screen(b, c, SEPT_POT, **RUNGS["R6"])))
    base = (T0, R30, R40, R50, R60)
    distinct = len(set(base)) == 5
    # portal as held at the census
    vs = [v for v in W["versions"] if v.accepted is None or v.accepted <= eod(c)]
    C.ok("A41", four(Book(W["orgs"], vs, W["annual"])) == base and distinct,
         "portal cut to the census: the answer, R3, R4, R5 and the stop unchanged and all five different")
    # register completed with the eventual returns (the movers' nine-month years among them)
    ann = copy.copy(W["annual"])
    for key, ar in W["annual"].items():
        if ar.received is None and ar.eventual is not None:
            a2 = copy.copy(ar)
            a2.received = ar.eventual
            ann[key] = a2
    C.ok("A42", four(Book(W["orgs"], W["versions"], ann)) == base,
         "register completed with every outstanding 2025-26 return: the answer, R3, R4, R5 and the stop unchanged")
    # management fourth quarters replaced by the audited figure where the extract holds the return
    vs3 = []
    for v in W["versions"]:
        o = W["by"][v.org]
        ar = W["annual"].get((v.org, v.q))
        if is_final(o, v.q) and v.kind == "mgmt" and ar is not None and ar.received is not None:
            v = copy.copy(v)
            v.ytd = ar.total
        vs3.append(v)
    C.ok("A43", four(Book(W["orgs"], vs3, W["annual"])) == base,
         "management fourth quarters replaced by audited ones: the answer, R3, R4, R5 and the stop unchanged")
    # the instrument: every return carries the year its figures run within (the portal's year_end), so the
    # calendar the answer uses is observed directly; the movers' June 2026 returns, filed after the extract
    # and supplied at their true figures, change neither the answer nor the stop (both step past June)
    vs4 = list(W["versions"])
    from world import Version
    for k in ("BC1", "BC2", "BC3"):
        o = W["by"][k]
        tq = Q(2026, 6)
        true = int(W["tot"][k][tq])
        d = dt.datetime(2026, 10, 20, 11, 0)
        vs4.append(Version(o.og_ref, k, tq, 1, "accepted", d, d, true, "original"))
    with_june = four(Book(W["orgs"], vs4, W["annual"]))
    C.ok("A43", with_june[0] == T0 and with_june[3] == R50 and with_june[4] == R60,
         "the movers' June 2026 returns supplied: the answer, R5 and the stop unchanged")
    # hardening loop 3, the grants register (a current-state snapshot as at the extract): every lapse's renewal
    # was approved before the census and nothing in the register changed between the census and the
    # extract, so the register as held at the census carries the same start and end dates and the same
    # Variations rows; repaired to the census, the answer and the stop are unchanged and still differ
    late = [(o.key, a_) for o in W["orgs"] for e, r_, a_ in o.gaps if not a_ < c]
    C.ok("A43", not late and T0 != R60,
         "the grants register as held at the census equals the shipped one (every renewal approved before the "
         "census): the answer and the stop unchanged, and different")
    # lens swap: not one population read two ways
    T = {r["org"]: r for r in W["sept"]["rows"]}
    R3 = {r["org"]: r for r in screen(book, c, SEPT_POT, **RUNGS["R3"])["rows"]}
    R4r = {r["org"]: r for r in screen(book, c, SEPT_POT, **R4RET)["rows"]}
    R5 = {r["org"]: r for r in screen(book, c, SEPT_POT, **RUNGS["R5"])["rows"]}
    same3 = [k for k in T if T[k]["end"] == R3[k]["end"]]
    diff3 = [k for k in T if T[k]["end"] != R3[k]["end"]]
    C.ok("A42", len(same3) == 115 and all(published_row(T[k])[:4] == published_row(R3[k])[:4] for k in same3),
         "lens-swap: the 115 filed grantees are identical under the answer and R3")
    C.ok("A42", len(diff3) == 17 and all(T[k]["end"] < R3[k]["end"] for k in diff3),
         "lens-swap: the 17 scored 30 June grantees are different periods, not one figure read twice")
    C.ok("A42", all(published_row(T[k])[:4] == published_row(R4r[k])[:4] for k in T) and len(R4r) - len(T) == 17,
         "the answer and the step-back without rule 4.1 agree on all 132 rows; the step-back adds 17 rows on "
         "twelve months the March 2026 round already scored")
    C.ok("A42", all(published_row(T[k])[:4] == published_row(R5[k])[:4] for k in T) and set(R5) - set(T) == MOVERS | {GAP}
         and all(R5[k]["end"] != R4r[k]["end"] for k in MOVERS),
         "lens-swap: R5 adds the three movers on twelve months to March 2026, a different period from the "
         "December 2025 their own year leaves, not one figure read twice")
    R6 = {r["org"]: r for r in screen(book, c, SEPT_POT, **RUNGS["R6"])["rows"]}
    C.ok("A42", all(published_row(T[k])[:4] == published_row(R6[k])[:4] for k in T) and set(R6) - set(T) == {GAP},
         "lens-swap: the stop and the answer score the same figures for the same 132 grantees and differ by one "
         "organisation's membership of the round, decided by dated grant records, not one figure read two ways")


def published_rows(s):
    return (s["rate"], tuple(sorted((r["org"],) + published_row(r) for r in s["rows"])))
