"""Independent verifier for task239: reads only the shipped bundle, the goldens, figures.json and submission.md, and
recomputes every owed figure on its own code path (no import of the generator's estimators)."""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

ITEMS = ["TC%02d" % k for k in range(1, 13)]
NEG = {"TC04", "TC07"}
ON = dict(zip(["tc%02d" % k for k in range(1, 13)], ITEMS))
PA = ON
SCORE = {"Strongly disagree": 1, "Disagree": 2, "Neither agree nor disagree": 3, "Agree": 4, "Strongly agree": 5}


def _f(target, pat):
    return [os.path.join(target, f) for f in os.listdir(target) if re.search(pat, f)][0]


def returns(target):
    S = pd.read_csv(_f(target, r"platform_sessions"), dtype=str, keep_default_na=False)
    A = pd.read_csv(_f(target, r"platform_responses"), dtype=str, keep_default_na=False)
    Pp = pd.read_csv(_f(target, r"paper_scans"), dtype=str, keep_default_na=False)
    K = pd.read_csv(_f(target, r"paper_packs"), dtype=str, keep_default_na=False)
    S = S[S["status"] == "submitted"]
    A = A[A["question"].isin(ON)]
    wide = A.assign(item=A["question"].map(ON)).pivot(index="session_id", columns="item", values="response")
    on = S.set_index("session_id").join(wide)
    on["chan"] = on["link_type"]
    on["t"] = pd.to_datetime(on["submitted_utc"].str.rstrip("Z"))
    on["st"] = pd.to_datetime(on["started_utc"].str.rstrip("Z"))
    # a tablet session sent twice: one copy
    site = on[on["chan"] == "site"].sort_values("t")
    site = site[~site["tablet_ref"].duplicated()]
    on = pd.concat([on[on["chan"] != "site"], site])
    pk = K.set_index("form_serial")
    pa = Pp.copy()
    pa = pa[pd.to_datetime(pa["scanned_at_local"]).dt.date <= pd.Timestamp("2027-10-08").date()]
    qcols = [c for c in pa.columns if c not in ("batch", "form_serial", "scanned_at_local")]
    pa = pa[(pa[qcols] != "No mark").any(axis=1)]
    pa = pa.rename(columns=PA)
    pa["chan"] = "paper"
    pa["t"] = pd.to_datetime(pa["scanned_at_local"]) - pd.Timedelta(hours=1)
    pa["st"] = pd.NaT
    pa["team_code"] = pa["form_serial"].map(pk["team_code"])
    pa["member"] = pa["form_serial"].map(pk["inv_code"])
    known = set(S["inv_code"]) | set(K["inv_code"])
    typed = on["entered_code"].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True)
    on["member"] = np.where(on["chan"] == "personal", on["inv_code"], np.where(typed.isin(known), typed, ""))
    on = on.reset_index().rename(columns={"session_id": "rid"})
    pa["rid"] = "F" + pa["form_serial"]
    cols = ["rid", "chan", "t", "st", "team_code", "member"] + ITEMS
    R = pd.concat([on[cols], pa[cols]], ignore_index=True)
    for it in ITEMS:
        v = R[it].map(SCORE).astype(float)
        R[it] = 6 - v if it in NEG else v
    R = R.sort_values(["t", "rid"])
    keyed = R[R["member"] != ""]
    keyed = keyed[~keyed["member"].duplicated(keep="last")]
    return pd.concat([R[R["member"] == ""], keyed]).sort_values(["t", "rid"]).reset_index(drop=True)


def teams(target, R):
    reg = pd.read_csv(_f(target, r"team_register"), dtype=str, keep_default_na=False)
    mp = pd.read_csv(_f(target, r"reorganisation_map"), dtype=str, keep_default_na=False)
    tl = pd.read_csv(_f(target, r"site_tablet_log"), dtype=str, keep_default_na=False)
    codes = set(reg["team_code"])
    succ = mp[mp["old_code"] != ""].groupby("old_code")["new_code"].apply(lambda s: sorted(set(s)))
    switch = pd.to_datetime(tl.loc[tl["event"] == "team list loaded", "at_local"]).max() - pd.Timedelta(hours=1)

    def july(c):
        if c in succ.index:
            return succ[c][0] if len(succ[c]) == 1 else None
        return c if c in codes else None

    out = []
    for ch, c, st in zip(R["chan"], R["team_code"], R["st"]):
        if ch == "personal":
            out.append(c if c in codes else None)
        elif ch == "site" and st < switch:
            out.append(july(c))
        elif ch == "site":
            out.append(c if c in codes else None)
        else:
            out.append(july(c))
    R = R.copy()
    R["team"] = out
    n = R.dropna(subset=["team"]).groupby("team").size()
    rep = set(n[n >= 5].index)
    R["reported"] = R["team"].isin(rep)
    R["complete"] = R[ITEMS].notna().all(axis=1)
    R["used"] = R["reported"] & R["complete"]
    return R, rep, reg


def between_loadings(U):
    """the scaled between-team matrix less the pooled within-team matrix, then principal axis factoring"""
    X = U[ITEMS].astype(float)
    grp = X.groupby(U["team"].values)
    n = grp.size().values.astype(float)
    M = grp.mean().values
    N, G = len(X), len(n)
    Dw = X.values - grp.transform("mean").values
    Spw = Dw.T @ Dw / (N - G)
    Dm = M - X.values.mean(0)
    Sb = (Dm * n[:, None]).T @ Dm / (G - 1)
    c = (N * N - (n * n).sum()) / (N * (G - 1))
    Sig = (Sb - Spw) / c
    d = np.sqrt(np.diag(Sig))
    Rm = Sig / np.outer(d, d)
    h = 1 - 1 / np.diag(np.linalg.inv(Rm))
    for _ in range(20000):
        Rr = Rm.copy()
        np.fill_diagonal(Rr, h)
        w, v = np.linalg.eigh(Rr)
        lam = v[:, -1] * np.sqrt(w[-1])
        if np.max(np.abs(lam ** 2 - h)) < 1e-13:
            break
        h = lam ** 2
    return lam if lam.sum() > 0 else -lam


def main(target, golden, figures, submission):
    F = json.load(open(figures))
    sub = open(submission).read()
    R = returns(target)
    R, rep, reg = teams(target, R)
    U = R[R["used"]]
    lam = between_loadings(U)
    stay = [it for it, l in zip(ITEMS, lam) if l >= 0.75]
    assert stay == F["call"]["stay"], (stay, F["call"]["stay"])
    assert all(lam[i] >= F["components"]["kept_band"] for i, it in enumerate(ITEMS) if it in stay)
    assert all(abs(lam[i]) < F["components"]["withdrawn_band"] for i, it in enumerate(ITEMS) if it not in stay)
    band = F["deliverables"]["withdrawn_loading_one_decimal"]
    for i, it in enumerate(ITEMS):
        one = round(float(lam[i]), 1) + 0.0
        if it in stay:
            assert one == F["deliverables"]["loadings"][it] == 0.9, (it, lam[i])
        else:
            assert F["deliverables"]["loadings"][it] == 0.0 and band["low"] <= one <= band["high"], (it, lam[i])
    assert len(R) == F["steps"]["returns_that_count"] and len(rep) == F["steps"]["teams_reported"]
    assert len(U) == F["steps"]["returns_used"]
    # development plans: each plan's latest version; a number is a row of the team's page as the dashboard note lists it
    from openpyxl import load_workbook as _lw
    ws = _lw(_f(target, r"dashboard_plans"), data_only=True)["Plans"]
    head = [c.value for c in ws[1]]
    plans = [dict(zip(head, [c.value for c in row])) for row in ws.iter_rows(min_row=2)]
    latest = {}
    for p in plans:
        if p["plan_ref"] not in latest or p["version"] > latest[p["plan_ref"]]["version"]:
            latest[p["plan_ref"]] = p
    inteam = R[R["team"].isin(rep)]
    pages = {}
    for t, grp in inteam.groupby("team"):
        vals = []
        for k, it in enumerate(ITEMS):
            s = grp[it].dropna()
            pct = int((s >= 4).sum()) * 1000 // len(s)          # tenths of a per cent, then half up on the next digit
            rem = (int((s >= 4).sum()) * 10000 // len(s)) % 10
            vals.append((pct + (1 if rem >= 5 else 0), k))
        pages[t] = [ITEMS[k] for v, k in sorted(vals)]
    got = {it: {"targets": 0, "agreed": 0} for it in ITEMS}
    for p in latest.values():
        for col in ("target_1", "target_2", "target_3"):
            v = p[col]
            if v is None:
                continue
            it = v if isinstance(v, str) else pages[p["team_code"]][int(v) - 1]
            got[it]["targets"] += 1
            got[it]["agreed"] += int(p["status"] == "Agreed")
    assert got == F["deliverables"]["plans"], got
    # the documents the call and the asks lean on, read back through this verifier's own extractors
    import zipfile
    from pypdf import PdfReader
    note = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>",
                               zipfile.ZipFile(_f(target, r"dashboard_methodology")).read("word/document.xml").decode()))
    assert "went live for team leaders on 1 November 2027" in note, "positive control: the note's own publication line"
    assert "from the team's lowest figure to its highest" in note and "in the order of Table 1" in note
    assert "the new version replaces the earlier one" in note and "every return that counts" in note
    assert "holds a plan from the leader's first save" in note and "a draft until the leader sends it" in note
    std = " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(_f(target, r"measurement_standard")).pages)
    assert "WI-SV-03" in std, "positive control: the standard's own reference"
    assert "0.75 or more stays in the index" in std and "five or more returns that count" in std
    assert "the return received last counts" in std and "a member of the team is expected to give" in std
    # the goldens carry the same figures
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(golden, "lfp_tci_structure_check_2027.xlsx"), data_only=True)
    ws = wb["Check"]
    rows = {ws.cell(row=r, column=1).value: (ws.cell(row=r, column=3).value, ws.cell(row=r, column=4).value)
            for r in range(5, 17)}
    for i, it in enumerate(ITEMS):
        assert rows[it][0] == F["deliverables"]["loadings"][it] and rows[it][1] == ("Stays" if it in stay else "Withdrawn")
    ws = wb["Check"]
    for r in range(5, 17):
        it = ws.cell(row=r, column=1).value
        assert [ws.cell(row=r, column=5).value, ws.cell(row=r, column=6).value] == [
            F["deliverables"]["plans"][it]["targets"], F["deliverables"]["plans"][it]["agreed"]], it
    from pptx import Presentation
    prs = Presentation(os.path.join(golden, "lfp_tci_items_2028.pptx"))
    ch = [s for s in prs.slides[0].shapes if s.has_chart][0].chart
    vals = dict(zip(ch.plots[0].categories, ch.plots[0].series[0].values))
    for i, it in enumerate(ITEMS):
        assert vals[it] == F["deliverables"]["loadings"][it], it
    # every number in the submission's answer blocks recomputes
    for it in stay:
        assert "%s (" % it in sub and "): 0.9, stays" in sub, it
    for it, x in F["deliverables"]["plans"].items():
        assert "%s: %s plans, %s agreed" % (it, "{:,}".format(x["targets"]), "{:,}".format(x["agreed"])) in sub, it
    print("verify: every figure recomputes from the bundle (%d returns, %d teams, %d used; %s stay)"
          % (len(R), len(rep), len(U), len(stay)))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(os.path.join(task, "target"), os.path.join(task, "golden"), os.path.join(here, "figures.json"),
         os.path.join(task, "submission.md"))
