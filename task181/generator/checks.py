"""Assertions on the cut pack: the call, every route the ladder prices, the fork rows, the asks' devices, the
separation of the asks from the call, and the input gates.

    python3 task181/generator/checks.py
"""
import datetime as dt
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import solve as S    # noqa: E402

GOLD = ["GS-16", "GS-21"]
DEFAULT = ["GS-05", "GS-12", "GS-16", "GS-21"]
FAILS = []
N = [0]


def check(label, ok, detail=""):
    N[0] += 1
    print(("PASS  " if ok else "FAIL  ") + label + ("" if ok else "   " + str(detail)))
    if not ok:
        FAILS.append(label)


def margins(table, gold):
    m_in = min(table[c]["observed"] - table[c]["limit"] for c in gold)
    m_out = min(table[c]["limit"] - table[c]["observed"] for c in table if c not in gold)
    return m_in, m_out


def period_adjusted(P, inf, repair):
    """Rung 1: the expectation scaled for the department's own rise after the repair date (the period effect)."""
    win = P[(P["day"] >= C.WIN0) & (P["day"] <= C.WIN1)]
    post = win["knife"] >= repair
    f = (sum(i in inf for i in win.index[post]) / win["expected"][post].sum()) / \
        (sum(i in inf for i in win.index[~post]) / win["expected"][~post].sum())
    out = {}
    for c in C.CONSULTANTS:
        w = win[win["consultant"] == c]
        pp = w["knife"] >= repair
        e = float(w["expected"][~pp].sum() + w["expected"][pp].sum() * f)
        o = int(sum(i in inf for i in w.index))
        out[c] = dict(expected=e, observed=o, limit=C.poisson_upper(e))
    return out, f


def session_adjusted(P, inf, D):
    """Rung 2: afternoon-list procedures carry their own department rate (a visible attribute of the operation)."""
    ops = D["ops"].set_index("booking_no")
    win = P[(P["day"] >= C.WIN0) & (P["day"] <= C.WIN1)]
    pm = win["session"] == "PM"
    f = (sum(i in inf for i in win.index[pm]) / win["expected"][pm].sum()) / \
        (sum(i in inf for i in win.index[~pm]) / win["expected"][~pm].sum())
    out = {}
    for c in C.CONSULTANTS:
        w = win[win["consultant"] == c]
        p = w["session"] == "PM"
        e = float(w["expected"][~p].sum() + w["expected"][p].sum() * f)
        out[c] = dict(expected=e, observed=int(sum(i in inf for i in w.index)), limit=C.poisson_upper(e))
    return out, f


def own_history(P, inf):
    """A consultant judged against their own 2022 to 2026 ratio of observed to expected."""
    out = {}
    for c in C.CONSULTANTS:
        h = P[(P["consultant"] == c) & (P["knife"].dt.year <= 2026)]
        ratio = sum(i in inf for i in h.index) / h["expected"].sum()
        w = P[(P["consultant"] == c) & (P["day"] >= C.WIN0) & (P["day"] <= C.WIN1)]
        e = float(w["expected"].sum() * ratio)
        out[c] = dict(expected=e, observed=int(sum(i in inf for i in w.index)), limit=C.poisson_upper(e))
    return out


def main():
    R = S.solve()
    D, P, inf, exposed, rep = R["D"], R["P"], R["inf"], R["exposed"], R["repair"]
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    # ---------------- the call
    check("call: the golden refers %s" % ", ".join(GOLD), S.referred(R["gold"]) == GOLD, S.referred(R["gold"]))
    check("call: figures.json carries the same set", fig["call"]["referred"] == GOLD, fig["call"])
    mi, mo = margins(R["gold"], GOLD)
    check("call: the golden's margins (inside %d, outside %d) are at least 4 counts" % (mi, mo), mi >= 4 and mo >= 4)
    check("default path (R0, the raw ratio against the limit) refers %s" % ", ".join(DEFAULT),
          S.referred(R["naive"]) == DEFAULT, S.referred(R["naive"]))
    mi0, mo0 = margins(R["naive"], DEFAULT)
    check("default path's margins (inside %d, outside %d) are at least 4" % (mi0, mo0), mi0 >= 4 and mo0 >= 4)
    check("SF3 stratified by exposure (expected times the exposed ratio %.2f): same call" % R["rr"][0],
          S.referred(R["strat"]) == GOLD, S.referred(R["strat"]))
    ms = margins(R["strat"], GOLD)
    check("SF3 the stratified route's margins (%d, %d) are at least 4" % ms, min(ms) >= 4)
    check("the exposure carries several times the risk (ratio %.2f on %d operations)" % (R["rr"][0], R["rr"][1]),
          R["rr"][0] > 2.5 and R["rr"][1] > 150)
    check("every window procedure is traced to its theatre scans", len(R["linked"]) ==
          int(((P["day"] >= C.WIN0) & (P["day"] <= C.WIN1)).sum()), len(R["linked"]))
    # ---------------- the ladder's other rungs
    pa, f = period_adjusted(P, inf, rep)
    check("R1 the department's own rise after the repair taken out (factor %.2f) files another set (%s)" %
          (f, ", ".join(S.referred(pa)) or "none"), S.referred(pa) != GOLD, S.referred(pa))
    sa, g = session_adjusted(P, inf, D)
    check("R2 afternoon lists given their own rate (factor %.2f) files another set" % g, S.referred(sa) != GOLD,
          S.referred(sa))
    oh = own_history(P, inf)
    check("R2b each consultant against their own 2022 to 2026 ratio files another set", S.referred(oh) != GOLD,
          S.referred(oh))
    pre = P[(P["day"] >= C.WIN0) & (P["knife"] < rep)]
    pre_tab = {}
    for c in C.CONSULTANTS:
        w = pre[pre["consultant"] == c]
        e = float(w["expected"].sum())
        pre_tab[c] = dict(expected=e, observed=int(sum(i in inf for i in w.index)), limit=C.poisson_upper(e))
    check("the window before the repair alone (six weeks) does not file the golden", S.referred(pre_tab) != GOLD,
          S.referred(pre_tab))
    # ---------------- fork rows
    ex_tray, _ = S.trace(D, P, rep, rule="tray")
    t2 = S.consultant_table(P, inf, ex_tray, "exclude")
    check("SF2 exposure read on rigid containers only: same call", S.referred(t2) == GOLD, S.referred(t2))
    ex_all, _ = S.trace(D, P, rep, rule="s3_all")
    t3 = S.consultant_table(P, inf, ex_all, "exclude")
    check("SF2 exposure read on every steriliser 3 load of the year: same call", S.referred(t3) == GOLD, S.referred(t3))
    rep_day = dt.datetime.combine(rep.date(), dt.time(0, 0))
    ex_d, _ = S.trace(D, P, rep_day)
    check("SF11 the repair taken from the start of 12 May: same call",
          S.referred(S.consultant_table(P, inf, ex_d, "exclude")) == GOLD)
    q95 = lambda tab: sorted(c for c, v in tab.items() if v["observed"] > C.poisson_upper(v["expected"], 0.95))
    check("SF4 the limit read as the 95th centile: same call and default", q95(R["gold"]) == GOLD and
          q95(R["naive"]) == DEFAULT, (q95(R["gold"]), q95(R["naive"])))
    # duration from anaesthetic start to leaving theatre
    P2 = P.copy()
    P2["minutes"] = (pd_to(P2["out_of_theatre"]) - P2["anaes"]).dt.total_seconds() / 60
    P2["idx"] = [C.risk_index(int(a), {"Clean": 1, "Clean-contaminated": 2, "Contaminated": 3, "Dirty": 4}[w], m, k)
                 for a, w, m, k in zip(P2["asa_class"], P2["wound_class"], P2["minutes"], P2["surveillance_category"])]
    P2["expected"] = [C.expected_rate(k, i) for k, i in zip(P2["surveillance_category"], P2["idx"])]
    t5 = S.consultant_table(P2, inf, exposed, "exclude")
    check("SF5 duration read from anaesthetic start to leaving theatre: same call", S.referred(t5) == GOLD,
          S.referred(t5))
    inf30 = S.infections(D, P, window=False)
    check("SF8 every infection kept whatever its day: same call",
          S.referred(S.consultant_table(P, inf30, exposed, "exclude")) == GOLD)
    Pr = S.procedures(D, drop_returns=False)
    infr = S.infections(D, Pr)
    exr, _ = S.trace(D, Pr, rep)
    check("SF9 returns to theatre kept as procedures: same call",
          S.referred(S.consultant_table(Pr, infr, exr, "exclude")) == GOLD)
    Ps = S.procedures(D, seq1=False)
    infs = S.infections(D, Ps)
    exs, _ = S.trace(D, Ps, rep)
    check("SF10 an add-on's second line kept as a procedure: same call",
          S.referred(S.consultant_table(Ps, infs, exs, "exclude")) == GOLD)
    Pb = P.copy()
    ops = D["ops"].drop_duplicates("booking_no").set_index("booking_no")
    Pb["consultant"] = [S.CODE_MAP.get(ops.loc[b, "booked_consultant"], ops.loc[b, "booked_consultant"])
                        for b in Pb["booking_no"]]
    check("SF14 the booked consultant in place of the responsible one: same call",
          S.referred(S.consultant_table(Pb, inf, exposed, "exclude")) == GOLD,
          S.referred(S.consultant_table(Pb, inf, exposed, "exclude")))
    check("SF1 the raw ratio read as each consultant's own practice files the default path's four",
          S.referred(R["naive"]) == DEFAULT and S.referred(R["naive"]) != GOLD)
    P6 = P.copy()
    P6["idx"] = [int(int(a) >= 3) + int({"Clean": 1, "Clean-contaminated": 2, "Contaminated": 3, "Dirty": 4}[w] >= 3)
                 + int(m >= C.CUT_MIN[k]) for a, w, m, k in zip(P6["asa_class"], P6["wound_class"], P6["minutes"],
                                                                P6["surveillance_category"])]
    P6["expected"] = [C.expected_rate(k, i) for k, i in zip(P6["surveillance_category"], P6["idx"])]
    check("SF6 a duration at the cut-point taking a point: same call",
          S.referred(S.consultant_table(P6, inf, exposed, "exclude")) == GOLD)
    P7 = P.copy()
    P7["day"] = [dt.date.fromisoformat(x) for x in P7["list_date"]]
    check("SF7 the window read on the list date: same call",
          S.referred(S.consultant_table(P7, inf, exposed, "exclude")) == GOLD)
    ex12, _ = S.trace(D, P, rep, aborted=True)
    check("SF12 an item's last load read with aborted cycles included: same call",
          S.referred(S.consultant_table(P, inf, ex12, "exclude")) == GOLD)
    w27 = D["ops"][(D["ops"]["list_date"] >= "2027-01-01")]
    check("SF13 no 2027 procedure carries the retired code GS-41",
          not ((w27["responsible_consultant"] == "GS-41") | (w27["booked_consultant"] == "GS-41")).any())
    # ---------------- shock: the golden is no interval of any one-number sort
    win = P[(P["day"] >= C.WIN0) & (P["day"] <= C.WIN1)]
    sorts = {"raw ratio": {c: R["naive"][c]["observed"] / R["naive"][c]["expected"] for c in C.CONSULTANTS},
             "infections": {c: R["naive"][c]["observed"] for c in C.CONSULTANTS},
             "afternoon share": {c: float((win[win["consultant"] == c]["session"] == "PM").mean()) for c in C.CONSULTANTS},
             "procedures": {c: int((win["consultant"] == c).sum()) for c in C.CONSULTANTS}}
    for k, v in sorts.items():
        order = sorted(v, key=lambda c: -v[c])
        pos = sorted(order.index(c) for c in GOLD)
        check("shock: the golden is not an interval of the %s sort" % k, pos[1] - pos[0] != 1 or pos[0] not in (0, 8))
    # ---------------- the asks: devices and separation
    a, b = R["ask_a"], R["ask_b"]
    check("ask A figures match figures.json", {k: v for k, v in a.items()} == fig["ask_a"])
    check("ask B figures match figures.json", {k: v for k, v in b.items()} == fig["ask_b"])
    pa_raw = S.ask_procedures(S.procedures(D, merge_addons=False))
    check("ask A device: counting bookings moves at least 20 of 30 cells",
          sum(pa_raw[k] != a[k] for k in a) >= 20, sum(pa_raw[k] != a[k] for k in a))
    pa_codes = S.ask_procedures(S.procedures(D, map_codes=False))
    check("ask A hazard: the 2025 code change unmerged moves GS-14's cells", all(pa_codes["GS-14 %d" % y] != a["GS-14 %d" % y]
                                                                               for y in (2022, 2023, 2024)))
    raw_b = cracker_infections(D)
    check("ask B device: counting the export by its own consultant and date moves at least 20 of 30 cells",
          sum(raw_b.get(k, 0) != b[k] for k in b) >= 20, sum(raw_b.get(k, 0) != b[k] for k in b))
    ex_link = S.infections(D, P, link="exact")
    b_exact = S.ask_infections(P, ex_link)
    check("ask B device: joining on the recorded date exactly moves cells", sum(b_exact[k] != b[k] for k in b) >= 8,
          sum(b_exact[k] != b[k] for k in b))
    # separation: the window's rows carry neither ask device
    o = D["ops"]
    w27 = o[o["list_date"] >= "2027-01-01"]
    dup = w27[w27["status"] == "Completed"].groupby(["ur_number", "theatre", "knife_to_skin"])["booking_no"].nunique()
    check("separation: no 2027 operation is split across two bookings", int((dup > 1).sum()) == 0, int((dup > 1).sum()))
    s27 = D["ssi"][D["ssi"]["operation_date"] >= "2025-01-01"]
    check("separation: every surveillance record from 2025 carries its booking", s27["booking_no"].notna().all())
    # ---------------- input gates
    files = sorted(os.listdir(C.TARGET))
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("input: 10 or more files (%d)" % len(files), len(files) >= 10)
    check("input: 3 or more formats (%s)" % ", ".join(sorted(exts)), len(exts) >= 3)
    big = max(sum(1 for _ in open(os.path.join(C.TARGET, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    check("input: a file of 25,000 or more rows (%d)" % big, big >= 25000)
    meta = json.load(open(os.path.join(C.TASK, "metadata.json"), encoding="utf-8"))
    check("input: two or more distractors named in metadata.json", len(meta.get("distractors", [])) >= 2)
    names = " ".join(files).lower()
    check("input: no file name labels a distractor or the step", not re.search(r"distract|decoy|fault|exposure|trace",
                                                                             names))
    zp = os.path.join(C.TASK, "target.zip")
    if os.path.exists(zp):
        check("target.zip holds exactly target/", sorted(zipfile.ZipFile(zp).namelist()) == files)
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


def pd_to(series):
    import pandas as pd
    return pd.to_datetime(series)


def cracker_infections(D):
    """The careful solver's reading of the export: latest record, confirmed, its own consultant code and date."""
    s = D["ssi"].copy()
    s["record_version"] = s["record_version"].astype(int)
    s = s.sort_values(["infection_id", "record_version"]).drop_duplicates("infection_id", keep="last")
    s = s[s["status"] == "Confirmed"]
    s = s.drop_duplicates(["ur_number", "operation_date", "surveillance_category"])
    out = {}
    for c, d in zip(s["consultant_code"], s["operation_date"]):
        c = S.CODE_MAP.get(c, c)
        y = int(d[:4])
        if 2022 <= y <= 2024:
            out["%s %d" % (c, y)] = out.get("%s %d" % (c, y), 0) + 1
    return out


if __name__ == "__main__":
    sys.exit(main())
