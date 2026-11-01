"""Independent verifier for task257: reads only target/ and golden/, shares no code with the generator, and
recomputes the call (the number of dimensions on the items' latent correlations and each item's placement) and the
department ask (respondents, response rate and stores showing results for each store department) by its own route:
scipy's bivariate normal for the latent correlations, its own random data for the retention test, principal-axis
factoring with varimax for the placements, and the HR report's September codes read through its 1 October rows.

    python3 task257/generator/verify.py"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import sys

import numpy as np
from openpyxl import load_workbook
from scipy.optimize import minimize_scalar
from scipy.stats import multivariate_normal, norm

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OFFSET = {"America/Toronto": 4, "America/Winnipeg": 5, "America/Moncton": 3}


def find(target, start):
    return os.path.join(target, next(f for f in sorted(os.listdir(target)) if f.startswith(start)))


def read_csv(path):
    with open(path, encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def sheet_rows(path, sheet=None, header_row=1):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[header_row - 1]
    return [dict(zip(head, r)) for r in rows[header_row:] if any(v is not None for v in r)]


def tetra(table):
    """ML latent correlation of a two-way table (thresholds from its margins), on the Fisher z scale."""
    table = table[table.sum(1) > 0][:, table.sum(0) > 0]
    a = norm.ppf(np.cumsum(table.sum(1))[:-1] / table.sum())
    b = norm.ppf(np.cumsum(table.sum(0))[:-1] / table.sum())
    A = np.concatenate([[-12.0], a, [12.0]])
    B = np.concatenate([[-12.0], b, [12.0]])
    gx, gy = np.meshgrid(A, B, indexing="ij")
    pts = np.column_stack([gx.ravel(), gy.ravel()])

    def nll(z):
        r = np.tanh(z)
        C = multivariate_normal(mean=[0, 0], cov=[[1, r], [r, 1]]).cdf(pts).reshape(gx.shape)
        C[0, :] = 0
        C[:, 0] = 0
        p = C[1:, 1:] - C[:-1, 1:] - C[1:, :-1] + C[:-1, :-1]
        return -(table * np.log(np.maximum(p, 1e-300))).sum()
    z = minimize_scalar(nll, bounds=(-2.9, 2.9), method="bounded", options={"xatol": 1e-6}).x
    return float(np.tanh(z))


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    # the questionnaire's question rows: English number, French number, type
    import re
    from pypdf import PdfReader
    text = " ".join(p.extract_text() for p in PdfReader(find(target, "engagement_survey_2026_questionnaire")).pages)
    rows_q = re.findall(r"\b(Q\d\d)\s+(F\d\d)\s+KL-\d{4}\s+(Statement|Yes or no)\b", text)
    order = [q for q, _, _ in rows_q]
    code = {}
    for q, f, _ in rows_q:
        code[q] = q
        code[f] = q
    scale = {q: ("agree5" if t == "Statement" else "yesno") for q, _, t in rows_q}
    # submissions, tokens and people
    subs = read_csv(find(target, "kestrava_brackenmere_2026_submissions"))
    test = {s["token"] for s in subs if s["status"] == "test"}
    channel = {s["token"]: s["channel"] for s in subs}
    last = {}
    for s in subs:
        last[s["token"]] = max(last.get(s["token"], 0), int(s["submission"]))
    dist = read_csv(find(target, "kestrava_brackenmere_2026_distribution_list"))
    person = {d["token"]: d["employee_id"] for d in dist}
    list_site = {d["token"]: int(d["site_no"]) for d in dist}
    with open(find(target, "kiosk_sessions"), encoding="utf-8") as fh:
        for line in fh:
            k = json.loads(line)
            person[k["session"]] = str(k["employee"]).zfill(7)
    sites = read_csv(find(target, "site_directory"))
    tz = {int(s["site_no"]): s["time_zone"] for s in sites}
    district = {int(s["site_no"]): s["district_code"] for s in sites}
    open_day = "2026-09-14"
    hr = read_csv(find(target, "hris_assignment_history"))
    stores = {int(s["site_no"]) for s in sites if s["site_type"] == "store"}

    def assigned(day):
        rows_d, ended = {}, {}
        for h in hr:
            if h["action"] == "termination":
                ended[h["employee_id"]] = min(ended.get(h["employee_id"], "9999"), h["effective_from"])
                continue
            if h["effective_from"] <= day and (h["effective_to"] == "" or h["effective_to"] >= day):
                rows_d[h["employee_id"]] = h
        return {e: h for e, h in rows_d.items() if not (e in ended and ended[e] <= day)}
    open_rows = assigned(open_day)
    on_open = {e: int(h["site_no"]) for e, h in open_rows.items()}
    # September store codes read through the 1 October reorganisation rows
    sep30 = assigned("2026-09-30")
    votes = {}
    for h in hr:
        if h["effective_from"] == "2026-10-01" and h["action"] == "reorganisation":
            b = sep30.get(h["employee_id"])
            if b is not None and b["site_no"] == h["site_no"] and int(b["site_no"]) in stores:
                votes.setdefault(b["department_code"], {}).setdefault(h["department"], 0)
                votes[b["department_code"]][h["department"]] += 1
    september = {c: max(v, key=v.get) for c, v in votes.items()}
    env = sheet_rows(find(target, "paper_returns"), None, header_row=5)
    sealed = {(int(r["Site"]), r["Keyed"].date().isoformat()): r["Sealed"].date() for r in env}

    def close_of(site):
        c = dt.datetime(2026, 9, 27, 23, 59, 59) + dt.timedelta(hours=OFFSET[tz[site]])
        return c.strftime("%Y-%m-%dT%H:%M:%SZ")
    # answers given before the close, by employee
    given = {}
    for r in read_csv(find(target, "kestrava_brackenmere_2026_responses")):
        t = r["token"]
        if t in test or int(r["submission"]) != last[t] or r["item"] not in code:
            continue
        e = person[t]
        site = on_open.get(e)
        if channel[t] == "paper":
            sd = sealed.get((list_site[t], r["answered_at"][:10]))
            ok = sd is not None and sd <= dt.date(2026, 9, 27)
        else:
            ok = site is not None and r["answered_at"] <= close_of(site)
        if ok:
            given.setdefault(e, {})[code[r["item"]]] = int(r["answer"])
    # the department ask
    dep_resp, dep_head, team = {}, {}, {}
    for e, h in open_rows.items():
        if int(h["site_no"]) not in stores:
            continue
        d = september[h["department_code"]]
        dep_head[d] = dep_head.get(d, 0) + 1
        if e in given:
            dep_resp[d] = dep_resp.get(d, 0) + 1
            team[(h["site_no"], d)] = team.get((h["site_no"], d), 0) + 1
    shown = {}
    for (s, d), n in team.items():
        shown[d] = shown.get(d, 0) + (n >= 10)
    # negatively worded statements: a statement whose answers run against the sum of the other items
    emps = sorted(given)
    raw = np.full((len(emps), 30), np.nan)
    for i, e in enumerate(emps):
        for j, c in enumerate(order):
            a = given[e].get(c)
            if a is None or a == 6:
                continue
            raw[i, j] = (a - 1) if scale[c] == "agree5" else (1 if a == 1 else 0)
    zs = np.nan_to_num((raw - np.nanmean(raw, 0)) / np.nanstd(raw, 0))
    rev = {c: scale[c] == "agree5" and np.corrcoef(zs[:, j], zs.sum(1) - zs[:, j])[0, 1] < 0
           for j, c in enumerate(order)}
    # the call
    X = np.full((len(emps), 30), np.nan)
    for i, e in enumerate(emps):
        for j, c in enumerate(order):
            a = given[e].get(c)
            if a is None or a == 6:
                continue
            if scale[c] == "agree5":
                X[i, j] = (5 - a) if rev[c] else (a - 1)
            else:
                X[i, j] = 1 if a == 1 else 0
    kcat = [5 if scale[c] == "agree5" else 2 for c in order]
    R = np.eye(30)
    for i in range(30):
        for j in range(i + 1, 30):
            m = ~np.isnan(X[:, i]) & ~np.isnan(X[:, j])
            tab = np.zeros((kcat[i], kcat[j]))
            np.add.at(tab, (X[m, i].astype(int), X[m, j].astype(int)), 1)
            R[i, j] = R[j, i] = tetra(tab)
    ev = np.sort(np.linalg.eigvalsh(R))[::-1]
    rng = np.random.default_rng(99)
    ref = np.percentile([np.sort(np.linalg.eigvalsh(np.corrcoef(rng.standard_normal((len(emps), 30)),
                                                                rowvar=False)))[::-1] for _ in range(100)], 95, axis=0)
    k = int(np.argmin(ev > ref))
    Xp = np.where(np.isnan(X), np.nanmean(X, 0), X)
    evp = np.sort(np.linalg.eigvalsh(np.corrcoef(Xp, rowvar=False)))[::-1]
    kp = int(np.argmin(evp > ref))
    # placements: principal axis, varimax
    h = 1 - 1 / np.diag(np.linalg.inv(R))
    for _ in range(500):
        Rr = R.copy()
        np.fill_diagonal(Rr, h)
        w, v = np.linalg.eigh(Rr)
        top = np.argsort(w)[::-1][:k]
        Lm = v[:, top] * np.sqrt(np.maximum(w[top], 0))
        h = (Lm ** 2).sum(1)
    T = np.eye(k)
    for _ in range(500):
        Z = Lm @ T
        u, s, vt = np.linalg.svd(Lm.T @ (Z ** 3 - Z * (Z ** 2).mean(0)))
        T = u @ vt
    grp = np.abs(Lm @ T).argmax(1)
    part = sorted(tuple(order[j] for j in range(30) if grp[j] == g) for g in set(grp))
    # against the goldens
    gi = sheet_rows(os.path.join(golden, "engagement_subscales_2027.xlsx"), "Items")
    gpart = {}
    for r in gi:
        if r.get("Sub-scale"):
            gpart.setdefault(r["Sub-scale"], []).append(r["Item"])
    gpart = sorted(tuple(sorted(v)) for v in gpart.values())
    gd = {r["Store department"]: (r["Answered at least one item before the close"], r["Response rate (%)"],
                                  r["Stores where results can be shown"])
          for r in sheet_rows(os.path.join(golden, "engagement_subscales_2027.xlsx"), "Departments")
          if isinstance(r.get("Answered at least one item before the close"), int) and
          r["Store department"] != "All store departments"}
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    fails = []
    if k != 3 or fig["call_subscales"] != 3:
        fails.append("dimensions %d" % k)
    if kp != 5:
        fails.append("Pearson route keeps %d" % kp)
    if [tuple(sorted(p)) for p in part] != gpart:
        fails.append("placements differ: %s" % part)
    if max(abs(a - b) for a, b in zip(ev[:6], fig["latent_eigen"])) > 0.01:
        fails.append("eigenvalues %s against %s" % (np.round(ev[:6], 3), fig["latent_eigen"]))
    if len(gd) != 8:
        fails.append("golden departments: %d rows" % len(gd))
    for d, (a, rt, sh) in gd.items():
        mine = round(100.0 * dep_resp.get(d, 0) / dep_head[d], 1)
        if (dep_resp.get(d) != a or abs(mine - rt) > 1e-9 or shown.get(d, 0) != sh or
                fig["dept_respondents"][d] != a or fig["dept_stores_shown"][d] != sh):
            fails.append("department %s: %s %s %s against golden %s %s %s" % (d, dep_resp.get(d), mine, shown.get(d),
                                                                             a, rt, sh))
    if fails:
        raise SystemExit("verify FAILED: " + "; ".join(fails))
    print("verify: %d respondents; latent eigenvalues %s keep %d (random data 95th %.2f at the fourth); Pearson keeps "
          "%d; placements and the 24 department figures match the golden" % (len(emps), np.round(ev[:4], 2), k, ref[3],
                                                                            kp))


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
