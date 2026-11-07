"""task156: the main call recomputed from the shipped pack (target/). The golden: a member-level turnout model fitted
on the branch's online votes with the delegate active at each member's worksite on each vote's close, set on the
protected action ballots' level by the ballot agent's declared turnouts, and run on the 2 November 2026 roll with the
delegates of the 2026-28 term. The rungs below it (the vote-history routes) are computed here too, for the checks."""
import csv
import datetime as dt
import functools
import math
import os
import re
import subprocess

import numpy as np
import statsmodels.api as sm
from openpyxl import load_workbook

BALLOT_CLOSE = dt.date(2027, 3, 15)
EXTRACT = dt.date(2026, 11, 2)
END24 = dt.date(2026, 6, 30)
F_REG = "membership_register_extract_2026-11-02.csv"
F_INV = "online_vote_invitations_2022-2025.csv"
F_VOTES = "online_votes_2022-2025.csv"
F_SITES = "worksites_2026-11.csv"
F_DELEG = "delegate_register_2018-2028.xlsx"
F_ROUND = "bargaining_round_2027.xlsx"
PAB_PDFS = ["tallyhouse_pab_declarations_2021.pdf", "tallyhouse_pab_declarations_2023-24.pdf"]


def pdate(s):
    return dt.date.fromisoformat(s) if s else None


def years(a, b):
    return (b - a).days / 365.25


def age_band(age):
    return 0 if age < 30 else (1 if age < 45 else (2 if age < 60 else 3))


class Pack:
    pass


@functools.lru_cache(maxsize=None)
def load(target):
    K = Pack()
    sites = list(csv.DictReader(open(os.path.join(target, F_SITES), encoding="utf-8")))
    K.old2new = {r["code_before_2024_07"]: r["worksite_code"] for r in sites}
    K.site_council = {r["worksite_code"]: r["council"] for r in sites}
    names = sorted(set(K.site_council.values()))
    K.councils = names
    K.members = {}
    for r in csv.DictReader(open(os.path.join(target, F_REG), encoding="utf-8")):
        site = r["worksite"] if r["worksite"] in K.site_council else K.old2new[r["worksite"]]
        K.members[int(r["member_no"])] = {"site": site, "council": K.site_council[site], "dob": pdate(r["date_of_birth"]),
                                          "join": pdate(r["joined"]), "cease": pdate(r["ceased"]),
                                          "emp": r["employment"]}
    K.votes = {}
    for r in csv.DictReader(open(os.path.join(target, F_VOTES), encoding="utf-8")):
        K.votes[r["vote_id"]] = dt.datetime.strptime(r["closes_local"], "%Y-%m-%d %H:%M").date()
    K.inv = [(r["vote_id"], int(r["member_no"]), r["voted_utc"] != "")
             for r in csv.DictReader(open(os.path.join(target, F_INV), encoding="utf-8"))]
    # delegates: (term start year, site) -> member numbers
    wb = load_workbook(os.path.join(target, F_DELEG), read_only=True)
    K.deleg = {}
    for ws in wb.worksheets:
        term = int(ws.title[:4])
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0 or row[0] is None:
                continue
            code = str(row[1])
            site = code if code in K.site_council else K.old2new[code]
            K.deleg.setdefault((term, site), []).append(int(row[3]))
    wb = load_workbook(os.path.join(target, F_ROUND), read_only=True)
    ws = wb["2027 round"]
    K.candidates = [r[0] for i, r in enumerate(ws.iter_rows(values_only=True)) if i > 0 and r[0]]
    K.pab = pab_declarations(target)
    return K


def pab_declarations(target):
    """Every final declaration in the agent's two reports: council, roll date, close date, roll, ballots returned."""
    out = []
    for f in PAB_PDFS:
        txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, f), "-"], capture_output=True,
                             text=True, check=True).stdout
        for block in re.split(r"\n(?=\s*DECLARATION\b)", txt):
            m = re.search(r"Employer:\s+(.+?Council)", block)
            if not m or "DECLARATION" not in block:
                continue
            council = m.group(1).strip()

            def grab(*pats):
                for p in pats:
                    g = re.search(p, block, re.I)
                    if g:
                        return g.group(1)
                raise ValueError("no %s in a declaration for %s" % (pats[0], council))
            roll = int(grab(r"Persons on the roll\s+([\d,]+)", r"persons on roll\s+([\d,]+)").replace(",", ""))
            ret = int(grab(r"Ballot papers returned\s+([\d,]+)", r"Total votes received[^\d\n]*([\d,]+)").replace(",", ""))
            rd = grab(r"Roll date\s+(\d{1,2} \w+ \d{4})", r"Roll closed\s+(\d{1,2} \w+ \d{4})")
            cd = grab(r"Ballot closed\s+(\d{1,2} \w+ \d{4})", r"ballot closed\s+(\d{1,2} \w+ \d{4})")
            out.append({"council": council, "roll": roll, "returned": ret,
                        "roll_date": dt.datetime.strptime(rd, "%d %B %Y").date(),
                        "close": dt.datetime.strptime(cd, "%d %B %Y").date()})
    return out


def term_of(d):
    y = d.year if d.month >= 7 else d.year - 1
    return y - (y % 2)


def active(m, d):
    return m["join"] <= d and (m["cease"] is None or m["cease"] > d)


def D(K, site, d, term=None):
    t = term_of(d) if term is None else term
    return 1.0 if any(active(K.members[n], d) for n in K.deleg.get((t, site), []) if n in K.members) else 0.0


def features(K, m, d):
    age = years(m["dob"], d)
    b = age_band(age)
    return [1.0 if b == 0 else 0.0, 1.0 if b == 1 else 0.0, 1.0 if b == 3 else 0.0,
            math.log(1 + max(0.0, years(m["join"], d))),
            1.0 if m["emp"] == "Part time" else 0.0, 1.0 if m["emp"] == "Casual" else 0.0]


@functools.lru_cache(maxsize=None)
def fit(target, with_d=True):
    """Pooled logit on the online votes: vote and council effects, age band, membership years, employment, and the
    delegate active at the member's worksite on the vote's close."""
    K = load(target)
    vids = sorted(K.votes)
    cidx = {c: i for i, c in enumerate(K.councils)}
    X, y = [], []
    for vid, no, voted in K.inv:
        m = K.members[no]
        d = K.votes[vid]
        row = [1.0 if vid == v else 0.0 for v in vids]
        row += [1.0 if cidx[m["council"]] == j else 0.0 for j in range(1, len(K.councils))]
        row += features(K, m, d)
        if with_d:
            row.append(D(K, m["site"], d))
        X.append(row)
        y.append(1.0 if voted else 0.0)
    X, y = np.array(X), np.array(y)
    res = sm.Logit(y, X).fit(disp=0, maxiter=200)
    b = res.params
    nv, nc = len(vids), len(K.councils) - 1
    out = {"vote": dict(zip(vids, b[:nv])), "council": {K.councils[0]: 0.0}, "beta": b[nv + nc:nv + nc + 6],
           "gamma": float(b[-1]) if with_d else 0.0, "se_gamma": float(res.bse[-1]) if with_d else 0.0}
    for j in range(1, len(K.councils)):
        out["council"][K.councils[j]] = float(b[nv + j - 1])
    return out


def eta(K, f, m, d, dval):
    return float(np.dot(f["beta"], features(K, m, d)) + f["council"][m["council"]] + f["gamma"] * dval)


@functools.lru_cache(maxsize=None)
def pab_level(target, with_d=True):
    """The protected action ballots' level: one shift on the online-vote scale that returns, over every declared
    ballot, the ballots the agent declared (each member on the roll at the ballot's close)."""
    K = load(target)
    f = fit(target, with_d)
    etas, obs, rolls = [], [], []
    for r in K.pab:
        roll = [m for m in K.members.values() if m["council"] == r["council"] and active(m, r["roll_date"])]
        e = np.array([eta(K, f, m, r["close"], D(K, m["site"], r["close"]) if with_d else 0.0) for m in roll])
        etas.append(e)
        obs.append(r["returned"])
        rolls.append(r["roll"])
    lo, hi = -5.0, 5.0
    tot = sum(obs)
    for _ in range(80):
        mid = (lo + hi) / 2
        pred = sum(float((1 / (1 + np.exp(-(e + mid)))).sum() * (rl / max(1, len(e)))) for e, rl in zip(etas, rolls))
        if pred < tot:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def forecast(target, with_d=True, term=2026, when=BALLOT_CLOSE):
    """Each candidate council's expected 2027 turnout: the mean over the 2 November 2026 roll."""
    K = load(target)
    f = fit(target, with_d)
    a = pab_level(target, with_d)
    out = {}
    for c in K.candidates:
        roll = [m for m in K.members.values() if m["council"] == c and active(m, EXTRACT)]
        if with_d:
            dd = [D(K, m["site"], EXTRACT if term == 2026 else END24, term) for m in roll]
        else:
            dd = [0.0] * len(roll)
        e = np.array([eta(K, f, m, when, dv) for m, dv in zip(roll, dd)]) + a
        out[c] = float((1 / (1 + np.exp(-e))).mean())
    return out


def golden(target):
    return forecast(target, True, 2026)


def naive_history(target):
    """Rung 1: the same model with no delegate term in it (the members' own voting record carries the history)."""
    return forecast(target, False)


def naive_carried(target):
    """Rung 1': the delegate term fitted, but each worksite carried at the delegates it had when members last voted."""
    return forecast(target, True, 2024)


def naive_last_pab(target):
    """Rung 0: each council's last declared turnout carried forward; the model without delegates where none."""
    K = load(target)
    hist = naive_history(target)
    last = {}
    for r in sorted(K.pab, key=lambda r: r["close"]):
        last[r["council"]] = r["returned"] / r["roll"]
    return {c: last.get(c, hist[c]) for c in K.candidates}


def member_share(target):
    """Rung 1'': each member's own share of the online votes they were invited to, put on the ballots' scale by the
    ratio of declared turnout to the roll's mean share at the councils balloted in 2023-24."""
    K = load(target)
    seen, cast = {}, {}
    for vid, no, voted in K.inv:
        seen[no] = seen.get(no, 0) + 1
        cast[no] = cast.get(no, 0) + (1 if voted else 0)
    mean_all = sum(cast.values()) / max(1, sum(seen.values()))

    def share(no):
        return cast[no] / seen[no] if no in seen else mean_all
    ratios = []
    for r in K.pab:
        if r["close"].year < 2023:
            continue
        roll = [no for no, m in K.members.items() if m["council"] == r["council"] and active(m, r["roll_date"])]
        s = np.mean([share(no) for no in roll])
        ratios.append((r["returned"] / r["roll"]) / s)
    k = float(np.mean(ratios))
    out = {}
    for c in K.candidates:
        roll = [no for no, m in K.members.items() if m["council"] == c and active(m, EXTRACT)]
        out[c] = float(min(0.99, k * np.mean([share(no) for no in roll])))
    return out


def backtest(target, with_d=False):
    """The 2023-24 round recomputed from the online votes before it, against the declared turnouts."""
    K = load(target)
    f = fit(target, with_d)
    a = pab_level(target, with_d)
    out = {}
    for r in K.pab:
        if r["close"].year < 2023:
            continue
        roll = [m for m in K.members.values() if m["council"] == r["council"] and active(m, r["roll_date"])]
        e = np.array([eta(K, f, m, r["close"], D(K, m["site"], r["close"]) if with_d else 0.0) for m in roll]) + a
        out[r["council"]] = (float((1 / (1 + np.exp(-e))).mean()), r["returned"] / r["roll"])
    return out
