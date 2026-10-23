"""task483's independent verifier: reads only the shipped bundle (target/), the golden deliverables and
generator/figures.json, recomputes every graded figure with its own code (pandas, no generator module), and compares.

    python3 task483/generator/verify.py
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
FAILS = []
SYS = "Larkspur Basin Community College"


def say(name, ok):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def half_up(x):
    return int(np.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def qkey(ts):
    """a timestamp's quarter as an integer"""
    return ts.year * 4 + (ts.month - 1) // 3


def qbounds(k):
    y, q = divmod(k, 4)
    a = pd.Timestamp(year=y, month=3 * q + 1, day=1)
    return a, (a + pd.offsets.QuarterEnd(0))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    inv = pd.read_excel(os.path.join(T, "larkspur_program_inventory_2025-26.xlsx"), sheet_name="Programs")
    inv["short"] = inv["Length"].astype(str).str.contains("clock hours")
    cip = {}
    for _, r in inv[~inv["short"]].iterrows():
        cip[str(r["CIP 2020"])] = r["Program"]
        if pd.notna(r["CIP before fall 2022"]):
            cip[str(r["CIP before fall 2022"])] = r["Program"]

    # credit programs: the release's three-years-after cells
    r24 = pd.read_excel(os.path.join(T, "postsecondary_earnings_outcomes_2024_edition.xlsx"), header=3)
    r24 = r24[(r24["Institution"] == SYS) & (r24["Years after award"] == 3) & (r24["Award year"] == "2020-21")]
    cells = []
    for _, r in r24.iterrows():
        if r["Completers with earnings"] == "S":
            continue
        q = [float(r[c]) * 1.0294 for c in ("10th percentile", "25th percentile", "Median", "75th percentile",
                                            "90th percentile")]
        cells.append((cip[str(r["CIP code"])], int(r["Completers with earnings"]), q))
    r25 = pd.read_csv(os.path.join(T, "postsecondary_earnings_outcomes_2025_edition.csv"), dtype=str)
    r25 = r25[(r25["institution"] == SYS) & (r25["years_after_award"] == "3") & (r25["award_year"] == "2021-22")]
    for (camp, c), g in r25.groupby(["campus", "cip_2020"]):
        m = dict(zip(g["measure"], g["value"]))
        if g["suppression"].eq("S").any():
            continue
        cells.append((cip[c], int(m["completers_with_earnings"]), [float(m[k]) for k in ("p10", "p25", "p50", "p75",
                                                                                         "p90")]))
    med = {}
    for prog in inv.loc[~inv["short"], "Program"]:
        cs = [(n, q) for p, n, q in cells if p == prog]
        if sum(n for n, _ in cs) < 30:
            med[prog] = None
            continue
        grid = np.linspace(5000, 150000, 290001)
        F = sum(n * np.interp(grid, [0.45 * q[0]] + q + [1.7 * q[-1]], [0, .1, .25, .5, .75, .9, 1]) for n, q in cs)
        F = F / sum(n for n, _ in cs)
        med[prog] = float(np.interp(0.5, F, grid))

    # short-term programs: the roster, the wage records, each job dated
    ros = pd.read_csv(os.path.join(T, "ctg_participant_roster_2023-2026.csv"), dtype=str)
    etp = dict(zip(inv["Career Training Grant program ID"], inv["Program"]))
    ros["prog"] = ros["etp_program_id"].map(etp)
    ros["end"] = pd.to_datetime(ros["section_end"])
    comp = ros[(ros["exit_reason"] == "Completed") & (ros["end"] >= "2024-07-01") & (ros["end"] <= "2025-06-30")]
    wg = pd.read_csv(os.path.join(T, "ctg_participant_wage_records_2022q3-2026q2.csv"), dtype={"participant_id": str,
                                                                                               "ui_account": str})
    wg = wg[wg["participant_id"].isin(set(comp["participant_id"]))]
    wg["amended"] = (wg["report_type"] == "Amended").astype(int)
    wg = wg.sort_values(["participant_id", "ui_account", "year", "quarter", "received_date", "amended"])
    wg = wg.groupby(["participant_id", "ui_account", "year", "quarter"], as_index=False).last()
    wg["k"] = wg["year"] * 4 + wg["quarter"] - 1
    pay = {pid: {(a, k): w for a, k, w in zip(g["ui_account"], g["k"], g["wages"])}
           for pid, g in wg.groupby("participant_id")}

    def working(pid, end):
        d = end + pd.Timedelta(days=180)
        k = qkey(d)
        a0, a1 = qbounds(k)
        days = (a1 - a0).days + 1
        rec = pay.get(pid, {})
        for acct in sorted({a for a, kk in rec if kk == k}):
            before, after = (acct, k - 1) in rec, (acct, k + 1) in rec
            if before and after:
                return True
            if after and (acct, k + 2) in rec:
                if a1 - pd.Timedelta(days=min(rec[(acct, k)] / rec[(acct, k + 1)], 1) * days) <= d:
                    return True
            elif before and (acct, k - 2) in rec:
                if a0 + pd.Timedelta(days=min(rec[(acct, k)] / rec[(acct, k - 1)], 1) * days) >= d:
                    return True
        return False
    place = {}
    for prog, g in comp.groupby("prog"):
        n = len(g)
        place[prog] = None if n < 20 else 100.0 * sum(working(p, e) for p, e in zip(g["participant_id"], g["end"])) / n
    for prog in inv.loc[inv["short"], "Program"]:
        place.setdefault(prog, None)

    # the 2024-25 completers
    old = pd.read_excel(os.path.join(T, "fennimore_ridgefield_completions_2024-25.xlsx"), dtype={"SSID": str})
    new = pd.read_csv(os.path.join(T, "copper_flats_antelope_springs_completions_2024-25.csv"), dtype=str)
    by_old = dict(zip(inv["Fennimore and Ridgefield code"], inv["Program"]))
    by_new = dict(zip(inv["Copper Flats and Antelope Springs ID"].astype(str), inv["Program"]))
    comps = pd.concat([pd.DataFrame({"prog": old["Program Code"].map(by_old), "ssid": old["SSID"].astype(str)}),
                       pd.DataFrame({"prog": new["program_id"].map(by_new),
                                     "ssid": new["state_student_id"].str.replace("-", "")})])
    n2425 = comps.groupby("prog").size().to_dict()
    tested = {p: v for p, v in list(med.items()) + list(place.items()) if v is not None}
    passes = {p: (v >= 34200 if p in med else v >= 70) for p, v in tested.items()}
    den = sum(n2425[p] for p in tested)
    num = sum(n2425[p] for p in tested if passes[p])
    share = 100.0 * num / den
    say("the call: %d of %d, %.2f per cent, %s" % (num, den, share, "renews" if share >= 75 else "lapses"),
        fig["call"]["renews"] == (share >= 75) and fig["call"]["in_passing"] == num and fig["call"]["tested"] == den
        and fig["call"]["share_pct"] == half_up(share))
    fail = sorted(p for p in tested if not passes[p])
    say("the failing programs %s" % fail, fail == fig["call"]["failing"])
    ok = all(fig["programs"][p]["figure_thousands"] == (None if med[p] is None else half_up(med[p] / 1000.0))
             for p in med)
    say("every credit program's median, whole thousands", ok)
    ok = all(fig["programs"][p]["figure_pct"] == (None if place[p] is None else half_up(place[p])) for p in place)
    say("every short-term program's day-180 share, whole per cent", ok)

    # ask A: every attended session dated in the year once, its time as hours and minutes after the point
    att = pd.read_csv(os.path.join(T, "larkspur_ctg_attendance_2023-2026.csv"), dtype=str).drop_duplicates()
    att = att[(att["session_date"] >= "2024-07-01") & (att["session_date"] <= "2025-06-30")].copy()
    hm = att["hours"].str.split(".", expand=True).astype(int)
    att["h"] = hm[0] + hm[1] / 60.0
    att["prog"] = att["crn"].map(dict(zip(ros["section_id"], ros["prog"])))
    tot = att.groupby("prog")["h"].sum()
    ok = all(fig["programs"][p]["clock_hours_fy2025"] == half_up(tot.get(p, 0.0)) for p in place)
    say("every short-term program's fiscal 2025 clock hours attended, whole hours", ok)

    # ask B: before July 2024 every disbursement (returns netted); from July 2024 each loan once
    ln = pd.read_csv(os.path.join(T, "larkspur_direct_loan_disbursements_2019-2026.csv"), dtype={"SSID": str})
    ln = ln[~ln["LOAN_TYPE"].str.contains("PLUS")].copy()
    newsys = pd.to_datetime(ln["DISB_DATE"]) >= "2024-07-01"
    per = pd.concat([ln[~newsys], ln[newsys].drop_duplicates("LOAN_ID")]).groupby("SSID")["GROSS_AMT"].sum()
    ok = True
    for prog in med:
        s = comps.loc[comps["prog"] == prog, "ssid"]
        v = per.reindex(s).dropna()
        v = v[v > 0.005]
        m = float(np.median(v)) if len(v) else 0.0
        ok &= fig["programs"][prog]["loan_median_usd"] == half_up(m / 10.0) * 10
        ok &= fig["programs"][prog]["loan_total_usd"] == half_up(float(v.sum()) / 10.0) * 10
    say("every credit program's median and total loan principal, nearest 10 dollars", ok)

    # the golden workbook carries the same figures
    wb = pd.read_excel(os.path.join(GOLD, "larkspur_workforce_value_2027-28.xlsx"), sheet_name=None, header=None)
    des = wb["Designation 2027-28"]
    rows = {str(r[0]): list(r[1:]) for r in des.itertuples(index=False) if pd.notna(r[0])}
    ok = "lapses" in str(des.iloc[0, 0]) and rows["Share in passing programs, per cent"][5] == fig["call"]["share_pct"]
    for p, x in fig["programs"].items():
        r = rows[p]
        if x["test"] == "earnings" and x["tested"]:
            ok &= r[1] == x["figure_thousands"] and r[3] == ("Passes" if x["passes"] else "Fails")
        if x["test"] == "placement" and x["tested"]:
            ok &= r[2] == x["figure_pct"] and r[4] == ("Passes" if x["passes"] else "Fails")
    tu = {str(r[0]): r[1] for r in wb["Clock hours FY2025"].itertuples(index=False)}
    lo = {str(r[0]): r[1] for r in wb["Loan principal"].itertuples(index=False)}
    ok &= all(tu[p] == x["clock_hours_fy2025"] for p, x in fig["programs"].items() if x["test"] == "placement")
    lt = {str(r[0]): r[2] for r in wb["Loan principal"].itertuples(index=False)}
    ok &= all(lo[p] == x["loan_median_usd"] and lt[p] == x["loan_total_usd"] for p, x in fig["programs"].items()
              if x["test"] == "earnings")
    say("the golden workbook states the call, the share and every figure", ok)
    svg = open(os.path.join(GOLD, "larkspur_program_tests_2027-28.svg"), encoding="utf-8").read()
    say("the golden chart states the call and the share", ("lapses" in svg) and ("%d per cent" % fig["call"]["share_pct"])
        in svg)
    print("%s  verify: %d failed" % ("PASS" if not FAILS else "FAIL", len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
