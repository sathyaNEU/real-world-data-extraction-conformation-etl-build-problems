"""task163 golden: every figure computed from the shipped files in target/ alone (never from the world's truth), so
the figures a reader can reproduce are the figures the write-up states."""
from __future__ import annotations

import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np

import common as K
import pack as PK

BASE_WEEKS = None


# ------------------------------------------------------------------------------------------------- readers
def items(t):
    out = {}
    for r in K.read_csv(os.path.join(t, PK.F_ITEM)):
        w = float(r["unit_weight"]) * (1000.0 if r["weight_uom"] == "kg" else 1.0)
        out[int(r["item_code"])] = dict(aub=r["aubrine_code"], family=r["family"], w=round(w, 1),
                                        size=r["size_class"], cost=float(r["std_cost_gbp"]), desc=r["description"])
    return out


def faces_current(t):
    pos = {}
    for r in K.read_csv(os.path.join(t, PK.F_LOC)):
        if r["status"] != "Active":
            continue
        run = (r["zone"], r["aisle"], int(r["level"]))
        pos[int(r["item_code"])] = (run, (int(r["bay"]) - 1) * 3 + int(r["position"]) - 1)
    return pos


def plan(t):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(t, PK.F_PLAN), read_only=True, data_only=True)
    ws = wb["Faces 2027"]
    rows = list(ws.iter_rows(values_only=True))[1:]
    out = []
    for loc, aub, desc, fam, fc in rows:
        z, a, b, lev, p = loc.split(".")
        out.append(dict(run=(z, z + a, int(lev)), idx=(int(b) - 1) * 3 + int(p) - 1, aub=aub, fc=int(fc)))
    return out


def neighbours(pos):
    at = {(run, i): it for it, (run, i) in pos.items()}
    return {it: [at[(run, j)] for j in (i - 1, i + 1) if (run, j) in at] for it, (run, i) in pos.items()}


def alike_share(nb, it, wt):
    ns = nb[it]
    return sum(abs(wt[j] - wt[it]) <= K.TOL_G for j in ns) / len(ns)


def velocity(t, d0=K.BASE_FROM, d1=K.BASE_TO):
    lines = defaultdict(int)
    for r in K.read_csv(os.path.join(t, PK.F_VEL)):
        wc = dt.date.fromisoformat(r["week_commencing"])
        if d0 <= wc and wc + dt.timedelta(6) <= d1:
            lines[int(r["item_code"])] += int(r["lines_picked"])
    return lines


def claims(t):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(t, PK.F_CLAIMS), read_only=True, data_only=True)
    ws = wb["Claims"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


def baseline_claims(t, it_by_aub, d0=K.BASE_FROM, d1=K.BASE_TO):
    out = []
    for r in claims(t):
        desp = r["Despatched"].date() if isinstance(r["Despatched"], dt.datetime) else r["Despatched"]
        if r["Reason"] == "Wrong item received" and r["Status"] == "Validated" and d0 <= desp <= d1:
            out.append((it_by_aub[r["Product ordered"]], it_by_aub[r["Product received"]], desp))
    return out


# ------------------------------------------------------------------------------------------------- the call
def main_call(t):
    it = items(t)
    wt = {k: v["w"] for k, v in it.items()}
    by_aub = {v["aub"]: k for k, v in it.items()}
    cur = faces_current(t)
    nb_cur = neighbours(cur)
    pl = plan(t)
    pos_plan = {by_aub[r["aub"]]: (r["run"], r["idx"]) for r in pl}
    fc = {by_aub[r["aub"]]: r["fc"] for r in pl}
    nb_plan = neighbours(pos_plan)
    L = velocity(t)
    cl = baseline_claims(t, by_aub)
    lines_base = sum(L.values())
    lines_2027 = sum(fc.values())
    U_base = sum(L.get(i, 0) * alike_share(nb_cur, i, wt) for i in cur)
    U_plan = sum(fc[i] * alike_share(nb_plan, i, wt) for i in pos_plan)
    U_cur27 = sum(fc[i] * alike_share(nb_cur, i, wt) for i in cur)
    rate = len(cl) / U_base
    plan_claims = rate * U_plan
    cur_claims = rate * U_cur27
    f = dict(
        base_claims=len(cl), base_lines=lines_base, lines_2027=lines_2027,
        base_per_10k=len(cl) / lines_base * 1e4,
        alike_share_base=U_base / lines_base, alike_share_plan=U_plan / lines_2027,
        alike_share_cur27=U_cur27 / lines_2027,
        claims_per_10k_alike=rate * 1e4,
        plan_claims=plan_claims, plan_per_10k=plan_claims / lines_2027 * 1e4,
        cur_claims=cur_claims, cur_per_10k=cur_claims / lines_2027 * 1e4,
        default_claims=len(cl) / lines_base * lines_2027,
    )
    f["breach"] = f["plan_per_10k"] > K.KPI_PER_10K
    return f, dict(items=it, wt=wt, by_aub=by_aub, cur=cur, nb_cur=nb_cur, pos_plan=pos_plan, nb_plan=nb_plan, fc=fc,
                   L=L, claims=cl)


# ------------------------------------------------------------------------------------------------- Ask A
def agency(t):
    hours, prem = [], []
    for r in K.read_csv(os.path.join(t, PK.F_AGENCY)):
        if r["line_type"] == "Hours":
            d = dt.date.fromisoformat(r["shift_start_date"])
            hours.append(dict(d=d, shift=r["shift"], h=float(r["hours"]), nh=float(r["night_hours"]),
                              sun=float(r["hours"]) if d.weekday() == 6 else 0.0, amt=float(r["amount_gbp"])))
        else:
            prem.append((dt.date.fromisoformat(r["invoice_date"]), float(r["amount_gbp"])))
    return hours, prem


def window_fit(hours, prem, window):
    """Least-squares night and Sunday uplifts for the premium lines read as covering window(invoice date); the worst
    residual says whether the lines are an identity over those hours."""
    nh = defaultdict(float)
    sh = defaultdict(float)
    for r in hours:
        nh[r["d"]] += r["nh"]
        sh[r["d"]] += r["sun"]
    A, y = [], []
    for inv, amt in prem:
        a, b = window(inv)
        n = s = 0.0
        d = a
        while d <= b:
            n += nh.get(d, 0.0)
            s += sh.get(d, 0.0)
            d += dt.timedelta(1)
        A.append((n, s))
        y.append(amt)
    A, y = np.array(A), np.array(y)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = float(np.max(np.abs(A @ coef - y)))
    return float(coef[0]), float(coef[1]), res


def pay_period_window(inv):
    """The four weeks ending the Sunday nine days before the invoice."""
    b = inv - dt.timedelta(9)
    return b - dt.timedelta(27), b


def ask_a(t):
    hours, prem = agency(t)
    un, us, res = window_fit(hours, prem, pay_period_window)
    un, us = round(un, 2), round(us, 2)
    m = defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in hours:
        k = (r["d"].year, r["d"].month)
        m[k][0] += r["amt"]
        m[k][1] += r["nh"] * un + r["sun"] * us
        m[k][2] += r["h"]
    out, detail = {}, {}
    for k in K.ASK_A_MONTHS:
        b, p, h = m[k]
        out["%d-%02d" % k] = (b + p) / h
        detail["%d-%02d" % k] = dict(hours=round(h, 2), base=round(b, 2), premium=round(p, 2))
    return out, dict(u_night=un, u_sunday=us, residual=res, detail=detail)


# ------------------------------------------------------------------------------------------------- Ask B
def bills(t):
    from pypdf import PdfReader
    out = {}
    for page in PdfReader(os.path.join(t, PK.F_RAV)).pages:
        txt = page.extract_text()
        m = re.search(r"Re-work of returned stock for Aubrine, (\w+) (\d{4})\s+([\d,]+\.\d{2})", txt)
        out[(int(m.group(2)), K.MONTH_NAMES.index(m.group(1)))] = float(m.group(3).replace(",", ""))
    return out


def graded(t):
    last = {}
    for r in K.read_csv(os.path.join(t, PK.F_RET)):
        key = r["return_ref"]
        ts = r["graded_at"]
        if key not in last or ts >= last[key]["ts"]:
            last[key] = dict(ts=ts, day=dt.date.fromisoformat(ts[:10]), item=int(r["item_code"]), grade=int(r["grade"]),
                             cap=r["captured_by"])
    return list(last.values())


OLD = {1: "resell", 2: "repack", 3: "scrap"}
APP = {1: "resell", 2: "scrap", 3: "repack"}


def reading_counts(units, it, legend_of):
    c = defaultdict(lambda: [0, 0])
    for u in units:
        if legend_of(u)[u["grade"]] == "repack":
            c[(u["day"].year, u["day"].month)][0 if it[u["item"]]["size"] == "S" else 1] += 1
    return c


def bill_fit(counts, bl, months=None):
    ms = sorted(bl) if months is None else months
    A = np.array([counts.get(m, [0, 0]) for m in ms], dtype=float)
    y = np.array([bl[m] for m in ms])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef, float(np.max(np.abs(A @ coef - y)))


def ask_b(t):
    it = items(t)
    units = graded(t)
    bl = bills(t)
    go = min(u["day"] for u in units if u["cap"] == "Handheld")
    legend = lambda u: OLD if u["day"] < go else APP
    coef, res = bill_fit(reading_counts(units, it, legend), bl)
    fam = defaultdict(lambda: [0, 0, 0, 0.0])
    for u in units:
        if not (K.ASK_B_FROM <= u["day"] <= K.ASK_B_TO):
            continue
        f = fam[it[u["item"]]["family"]]
        fate = legend(u)[u["grade"]]
        f[0] += 1
        f[1] += fate == "repack"
        f[2] += fate == "scrap"
        f[3] += it[u["item"]]["cost"] if fate == "scrap" else 0.0
    out = {}
    for name, (n, rp, sc, val) in fam.items():
        out[name] = dict(units=n, repack_pct=100.0 * rp / n, scrap_pct=100.0 * sc / n, scrap_value=val)
    return out, dict(go_live=go, prices=[round(float(c), 4) for c in coef], residual=res)


# ------------------------------------------------------------------------------------------------- figures
def figures(t):
    f, _ = main_call(t)
    a, ainfo = ask_a(t)
    b, binfo = ask_b(t)
    fig = {
        "call_plan_claims": K.round_to(f["plan_claims"], 100),
        "call_plan_per_10k": K.round_half_up(f["plan_per_10k"], 1),
        "call_cur_claims": K.round_to(f["cur_claims"], 100),
        "call_cur_per_10k": K.round_half_up(f["cur_per_10k"], 1),
        "call_breach": "over" if f["breach"] else "within",
        "kpi_per_10k": K.KPI_PER_10K,
        "base_claims": f["base_claims"],
        "base_lines": f["base_lines"],
        "lines_2027": f["lines_2027"],
        "base_per_10k": K.round_half_up(f["base_per_10k"], 2),
        "alike_share_base_pct": K.round_half_up(100 * f["alike_share_base"], 1),
        "alike_share_plan_pct": K.round_half_up(100 * f["alike_share_plan"], 1),
        "claims_per_10k_alike": K.round_half_up(f["claims_per_10k_alike"], 2),
        "default_claims": K.round_to(f["default_claims"], 100),
        "raw": {k: (float(v) if not isinstance(v, (bool, str)) else v) for k, v in f.items()},
        "ask_a": {k: K.round_half_up(v, 2) for k, v in a.items()},
        "ask_a_raw": a,
        "ask_a_uplifts": dict(u_night=ainfo["u_night"], u_sunday=ainfo["u_sunday"], residual=ainfo["residual"]),
        "ask_a_detail": ainfo["detail"],
        "base_weeks": 52,
        "per_lines": 10000,
        "tol_g": K.TOL_G,
        "alike_share_cur27_pct": K.round_half_up(100 * f["alike_share_cur27"], 1),
        "base_per_10k_1dp": K.round_half_up(f["base_per_10k"], 1),
        "ask_b": {k: dict(repack_pct=K.round_half_up(v["repack_pct"], 1), scrap_pct=K.round_half_up(v["scrap_pct"], 1),
                          scrap_value=int(K.round_half_up(v["scrap_value"], 0)), units=v["units"])
                  for k, v in sorted(b.items())},
        "ask_b_raw": b,
        "ask_b_fit": dict(go_live=binfo["go_live"].isoformat(), prices=binfo["prices"], residual=binfo["residual"]),
    }
    return fig
