"""Independent verifier for task151: reads only the shipped bundle (target/), the goldens and figures.json, on its own
code path (pandas frames, pdftotext, no generator module), and recomputes the accrual and each player's figure, the
default path's figure, the write-up's step figures, and both asks."""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np
import openpyxl
import pandas as pd

MIN = {"7-day": 7, "10-day": 10, "15-day": 15, "60-day": 60}


def txt(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                              check=True).stdout.decode("utf-8"))


def ascii_upper(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).upper()


def batting(target):
    leg = pd.read_csv(os.path.join(target, "lsf_batting_2021_2024.txt"), sep="|", dtype=str, keep_default_na=False)
    xw = pd.read_csv(os.path.join(target, "lsf_player_id_crosswalk.csv"), dtype=str)
    leg = leg.merge(xw[["legacy_id", "player_id"]], left_on="PLAYER_CD", right_on="legacy_id", how="left")
    assert leg.player_id.notna().all()
    for c in ("AB", "BB", "HBP", "SH", "SF", "CI", "LINEUP", "SEQ"):
        leg[c] = leg[c].astype(int)
    leg["pa"] = leg.AB + leg.BB + leg.HBP + leg.SH + leg.SF + leg.CI
    leg["season"] = pd.to_datetime(leg.GAME_DT, format="%m/%d/%Y").dt.year
    leg["slot"] = leg.LINEUP
    leg["starter"] = leg.SEQ == 1
    leg["pid"] = leg.player_id.astype(int)
    leg["game"] = leg.GAME_ID
    new = pd.read_csv(os.path.join(target, "lsf_batting_2025_2026.csv"))
    new["season"] = pd.to_datetime(new.official_date).dt.year
    new["slot"] = new.batting_order // 100
    new["starter"] = new.batting_order % 100 == 0
    new["pid"] = new.player_id
    new["game"] = new.game_pk.astype(str)
    cols = ["season", "game", "pid", "slot", "starter", "pa"]
    return pd.concat([leg[cols], new[cols]], ignore_index=True)


def plan(target):
    wb = openpyxl.load_workbook(os.path.join(target, "hvbd_winter_depth_charts_2021_2026.xlsx"), data_only=True)
    out = []
    for ws in wb.worksheets:
        season = int(re.search(r"(\d{4})", ws.title).group(1))
        rows = list(ws.iter_rows(values_only=True))
        h = next(i for i, r in enumerate(rows) if r and r[0] == "Tm")
        hdr = list(rows[h])
        for r in rows[h + 1:]:
            if r and r[0]:
                d = dict(zip(hdr, r))
                out.append(dict(season=season, role=d["Role"], pos=d["Pos"], name=d["Player"], pid=int(d["LG_ID"]),
                                ord=d["Ord"]))
    return pd.DataFrame(out)


def five(target):
    t = txt(os.path.join(target, "term_sheets_2027_free_agent_hitters.pdf"))
    wb = openpyxl.load_workbook(os.path.join(target, "ral_depth_chart_2027.xlsx"), data_only=True)
    slots = {}
    on = False
    for r in wb.active.iter_rows(values_only=True):
        if r and r[0] == "Lineup":
            on = True
            continue
        if r and r[0] in ("Bench", "Rotation", "Bullpen"):
            on = False
        if on and r and isinstance(r[0], int):
            slots[r[2]] = r[0]
    out = []
    for name, slot in slots.items():
        i = t.find(name + " (")
        if i < 0:
            continue
        seg = t[i:i + 2500]
        m = re.search(r"2027 season: \$([\d,]+) each for (\d+), (\d+) and (\d+) plate appearances", seg)
        sg = re.search(r"Signed\s+([A-Z][a-z]+ \d{1,2}, \d{4})", seg)
        out.append(dict(name=name, slot=slot, amount=int(m.group(1).replace(",", "")),
                        T=[int(m.group(2)), int(m.group(3)), int(m.group(4))],
                        signed=dt.datetime.strptime(sg.group(1), "%B %d, %Y").date()))
    return sorted(out, key=lambda x: x["signed"])


def accrual(target):
    bl = batting(target)
    st = bl[bl.starter]
    rate = (st.groupby("slot").pa.sum() / st.groupby("slot").size()).to_dict()
    starts = st.groupby(["season", "pid"]).size()
    pl = plan(target)
    reg = pl[(pl.role == "Lineup") & (pl.pos != "C")]
    s = np.array([starts.get((a, b), 0) for a, b in zip(reg.season, reg.pid)], float)
    F = five(target)
    per = {}
    for f in F:
        x = s * rate[f["slot"]]
        per[f["name"]] = sum(f["amount"] * float((x >= T).mean()) for T in f["T"])
    return per, sum(per.values()), dict(lines=len(bl), planned=len(reg), rate=rate, s=s, F=F, starts=starts, pl=pl)


def default(target, D):
    pr = pd.read_csv(os.path.join(target, "hvbd_hitter_projections_2022_2027.csv"))
    bl = batting(target)
    pa = bl.groupby(["season", "pid"]).pa.sum()
    reg = D["pl"][(D["pl"].role == "Lineup") & (D["pl"].pos != "C")]
    past = pr[pr.season <= 2026].merge(reg[["season", "pid"]], left_on=["season", "lg_id"], right_on=["season", "pid"])
    err = np.array([pa.get((a, b), 0) - p for a, b, p in zip(past.season, past.lg_id, past.pa)], float)
    sd = err.std()
    last = D["pl"][D["pl"].season == 2026]
    tot = 0.0
    for f in D["F"]:
        pid = int(last[last.name == f["name"]].pid.iloc[0])
        p = int(pr[(pr.season == 2027) & (pr.lg_id == pid)].pa.iloc[0])
        tot += sum(f["amount"] * (1 - 0.5 * (1 + math.erf((T - p) / (sd * math.sqrt(2))))) for T in f["T"])
    return tot


def stints(target, F, pl):
    tx = pd.DataFrame(json.load(open(os.path.join(target, "lsf_transactions_2024_2026.json"),
                                    encoding="utf-8"))["transactions"])
    rep = pd.read_csv(os.path.join(target, "league_office_il_report_2024_2026.csv"), dtype=str)
    cal = pd.read_csv(os.path.join(target, "league_calendar_2021_2027.csv"), dtype=str).set_index("season")
    out = []
    for f in F:
        pid = int(pl[(pl.season == 2026) & (pl.name == f["name"])].pid.iloc[0])
        mv = tx[(tx.player_id == pid) & tx.type.isin(["IL_PLACEMENT", "IL_ACTIVATION", "IL_REINSTATEMENT"])]
        mv = mv.sort_values(["date", "transaction_id"])
        open_ = None
        for _, t in mv.iterrows():
            if t.type == "IL_PLACEMENT":
                if open_ is None:
                    open_ = t.date
            else:
                y = open_[:4]
                r = rep[(rep.player.str.split(", ").str[1] + " " + rep.player.str.split(", ").str[0] ==
                         ascii_upper(f["name"])) & (pd.to_datetime(rep.placed, format="%m/%d/%Y") ==
                                                    pd.Timestamp(open_))].iloc[0]
                eff = (pd.to_datetime(r.eligible, format="%m/%d/%Y") - pd.Timedelta(days=MIN[r.injured_list])).date()
                od = dt.date.fromisoformat(cal.loc[y, "opening_day"])
                last = dt.date.fromisoformat(cal.loc[y, "last_scheduled_day"])
                a = max(eff, od)
                b = min(dt.date.fromisoformat(t.date) - dt.timedelta(days=1), last)
                out.append((f["name"], eff, (b - a).days + 1))
                open_ = None
    return sorted(out, key=lambda x: (x[1], x[0]))


def paid(target, D):
    """Plate-appearance bonuses paid by season: each playing-time payment (the HRIS playing-time code, or the legacy
    performance line of a season-end or January payroll) to a player with plate-appearance terms is one half; the
    plate-appearance part of a half is half the lines he reached with the Club."""
    pay = pd.read_csv(os.path.join(target, "ral_payroll_player_earnings_2023_2026.csv"), dtype={"employee_id": str})
    hm = pd.read_csv(os.path.join(target, "ral_hris_legacy_employee_map.csv"), dtype=str)
    pay["emp"] = pay.employee_id.map(dict(zip(hm.legacy_employee_no, hm.employee_id))).fillna(pay.employee_id)
    wb = openpyxl.load_workbook(os.path.join(target, "ral_player_contract_register_2024_2026.xlsx"), data_only=True)
    rows = list(wb["Register"].iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == "Player")
    hdr = list(rows[h])
    reg = pd.DataFrame([dict(zip(hdr, r)) for r in rows[h + 1:] if r and r[0]])
    reg = reg[reg["Plate-appearance bonuses (each season)"].notna()]
    terms = {}
    for _, r in reg.iterrows():
        m = re.match(r"\$([\d,]+) each for ([\d, and]+) plate", r["Plate-appearance bonuses (each season)"])
        terms[r["Employee ID"]] = (r["Player"], int(m.group(1).replace(",", "")), [int(x) for x in re.findall(r"\d+", m.group(2))])
    bl = batting(target)
    new = pd.read_csv(os.path.join(target, "lsf_batting_2025_2026.csv"))
    clubs = pd.read_csv(os.path.join(target, "league_club_directory.csv"))
    leg = pd.read_csv(os.path.join(target, "lsf_batting_2021_2024.txt"), sep="|", dtype=str, keep_default_na=False)
    xw = pd.read_csv(os.path.join(target, "lsf_player_id_crosswalk.csv"), dtype=str)
    leg = leg.merge(xw[["legacy_id", "player_id"]], left_on="PLAYER_CD", right_on="legacy_id")
    leg["club"] = leg.TEAM_CD.map(dict(zip(clubs.legacy_code, clubs.abbrev)))
    for c in ("AB", "BB", "HBP", "SH", "SF", "CI"):
        leg[c] = leg[c].astype(int)
    leg["pa"] = leg.AB + leg.BB + leg.HBP + leg.SH + leg.SF + leg.CI
    leg["season"] = pd.to_datetime(leg.GAME_DT, format="%m/%d/%Y").dt.year
    leg["pid"] = leg.player_id.astype(int)
    new["club"] = new.team_id.map(dict(zip(clubs.team_id, clubs.abbrev)))
    new["season"] = pd.to_datetime(new.official_date).dt.year
    new["pid"] = new.player_id
    byclub = pd.concat([leg[["season", "pid", "club", "pa"]], new[["season", "pid", "club", "pa"]]]).groupby(
        ["season", "pid", "club"]).pa.sum()
    lg = {}
    for _, r in D["pl"].iterrows():
        first, last = r["name"].split(" ", 1)
        lg["%s, %s" % (last, first)] = r["pid"]
    pay["date"] = pd.to_datetime(pay.pay_date)
    pay["season"] = np.where(pay.date.dt.month >= 7, pay.date.dt.year, pay.date.dt.year - 1)
    pt = pay[pay.emp.isin(terms) & ((pay.earning_code == "BPA") | ((pay.earning_code == "E40") &
                                                                    pay.date.dt.month.isin([10, 1])))].copy()
    pt["half"] = np.where(pt.date.dt.month >= 7, "first", "second")
    net = pt.groupby(["season", "emp", "half"]).amount.sum()
    out = {}
    for (season, e, half), v in net.items():
        if season not in (2024, 2025, 2026) or v <= 0.5:
            continue
        name, amt, lines = terms[e]
        pa = byclub.get((season, lg[name], "RAL"), 0)
        out[(int(season), name)] = out.get((int(season), name), 0) + amt * sum(1 for x in lines if pa >= x) / 2
    return {k: v for k, v in out.items() if v}


def r(x, unit):
    return int(math.floor(x / unit + 0.5)) * unit


def main(target, golden, fig_path):
    per, tot, D = accrual(target)
    fig = json.load(open(fig_path, encoding="utf-8"))
    bad = []
    if "$%s" % format(r(tot, 250000), ",") != fig["call"]["total"]:
        bad.append(("total", tot))
    for n, v in per.items():
        if "$%s" % format(r(v, 100000), ",") != fig["critical_components"]["per_player"][n]:
            bad.append((n, v))
    if "{:,}".format(D["lines"]) != fig["steps"]["batting_lines"] or "{:,}".format(D["planned"]) != fig["steps"]["planned_seasons"]:
        bad.append(("steps", D["lines"], D["planned"]))
    if "%.2f" % D["rate"][1] != fig["steps"]["rate_first"] or "%.2f" % D["rate"][9] != fig["steps"]["rate_ninth"]:
        bad.append(("rates", D["rate"][1], D["rate"][9]))
    if str(int((D["s"] < 100).sum())) != fig["steps"]["under_100"].replace(",", "") or \
            str(int((D["s"] >= 155).sum())) != fig["steps"]["full_155"].replace(",", ""):
        bad.append(("starts counts",))
    dft = default(target, D)
    if "$%s" % format(r(dft, 250000), ",") != fig["rivals"]["default"]:
        bad.append(("default", dft))
    S = stints(target, D["F"], D["pl"])
    want = [(s["player"], s["took_effect"], s["days"]) for s in fig["deliverables"]["stints"]]
    got = [(a, b.strftime("%B %-d, %Y"), str(c)) for a, b, c in S]
    if got != want:
        bad.append(("stints", got, want))
    B = paid(target, D)
    want_b = {}
    for blk in fig["deliverables"]["paid"]:
        for n, v in blk["rows"]:
            want_b[(int(blk["season"]), n)] = v
    got_b = {}
    for (y, n), v in B.items():
        last, first = n.split(", ")
        got_b[(y, "%s %s" % (first, last))] = "$%s" % format(int(round(v)), ",")
    if got_b != want_b:
        bad.append(("paid", got_b, want_b))
    for blk in fig["deliverables"]["paid"]:
        t = sum(v for (y, n), v in B.items() if y == int(blk["season"]))
        if "$%s" % format(int(round(t)), ",") != blk["total"]:
            bad.append(("paid total", blk["season"], t))
    wb = openpyxl.load_workbook(os.path.join(golden, "pa_bonus_accrual_2027.xlsx"), data_only=True)
    cells = [c for row in wb["Accrual"].iter_rows(values_only=True) for c in row if isinstance(c, (int, float))]
    if r(tot, 250000) not in cells:
        bad.append(("workbook total",))
    if bad:
        print("verify.py: FAIL", bad)
        raise SystemExit(1)
    print("verify.py: the accrual %s (unrounded %.0f), five player figures, the default path %s, the step figures, "
          "nine stints and the bonuses paid reproduce from the bundle on an independent path" % (
              fig["call"]["total"], tot, fig["rivals"]["default"]))


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(t), "golden")
    f = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    main(t, g, f)
