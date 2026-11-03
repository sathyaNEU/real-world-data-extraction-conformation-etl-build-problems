"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker is drawn from the careful solver's route, never from the ask list (supplemental-stumping 1.1): it lands
the call, runs the hygiene battery (1.1c) and executes every filed rule it points at. It is written here from the
files alone and shares no code with the generator's estimator:

  3.1   online sessions with status submitted, by 23:59 UK time on 4 October;
  3.2   paper forms scanned by 8 October that carry an answer;
  3.3   each return once (a tablet's re-sent copy, the same tablet reference with the same answers, kept once: the
        battery's re-sent batch), and each member once at the return received last, the member found through the
        battery's cross-system match of the invitation code;
  3.4   a return's team from the code on it, a code of the July structure read through HR's reorganisation map
        (paper packs printed in July; tablet sessions started before each tablet's second team list load);
  5.1   the teams with five or more returns that count; 4.4 the returns answering all twelve items on the scale;
  note  each team's development plan at its latest version (the dashboard note: a new version replaces the earlier
        one; the battery's latest-version rule), a plan's targets counted for each item, agreed when the plan's status
        is Agreed. The plans export holds a target as a number up to 5 November and as an item code from 8 November:
        the battery's key-format repair reads a number as the item it numbers (3 is TC03).

The mirror stops at the default path on the call (one factor on the team means) and takes the same ask path. A figure
is kept when it equals the golden's. Weights 38 / 7 / 55 over the ask criteria: the item lines scored as each loading
at one decimal and each verdict apart (24, keyed to the call's construction: the cracker keeps every one, the mirror the
verdicts its eight items get right and any loading its team means reach), the slide (3, keyed to the call) and every
plan figure (24).

    python3 task239/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ITEMS = ["TC%02d" % k for k in range(1, 13)]
REVERSED = {"TC04", "TC07"}
SCALE = {"Strongly disagree": 1, "Disagree": 2, "Neither agree nor disagree": 3, "Agree": 4, "Strongly agree": 5}
SLIDE = 3
CLOSE_UTC = "2027-10-04T22:59:59Z"          # 23:59:59 BST
PAPER_LAST = "2027-10-08"


def _find(target, stem):
    hit = [f for f in os.listdir(target) if f.startswith(stem)]
    assert len(hit) == 1, (stem, hit)
    return os.path.join(target, hit[0])


def read(target):
    rd = lambda stem: pd.read_csv(_find(target, stem), dtype=str, keep_default_na=False)
    ws = load_workbook(_find(target, "lfp_sv27_dashboard_plans"), data_only=True)["Plans"]
    head = [c.value for c in ws[1]]
    plans = pd.DataFrame([[c.value for c in row] for row in ws.iter_rows(min_row=2)], columns=head)
    return dict(S=rd("lfp_sv27_platform_sessions"), A=rd("lfp_sv27_platform_responses"),
                P=rd("lfp_sv27_paper_scans"), K=rd("lfp_sv27_paper_packs"),
                G=rd("lfp_hr_team_register"), M=rd("lfp_hr_reorganisation_map"), T=rd("lfp_sv27_site_tablet_log"),
                PL=plans)


def norm(code):
    return "".join(ch for ch in str(code).upper() if ch.isalnum())


def returns(D):
    """every return that counts under 3.1 to 3.3, one row each, with its scored answers"""
    S, A, P, K = D["S"], D["A"], D["P"], D["K"]
    sub = S[(S["status"] == "submitted") & (S["submitted_utc"] <= CLOSE_UTC)].copy()
    tags = ["tc%02d" % k for k in range(1, 13)]
    wide = A[A["question"].isin(tags)].pivot(index="session_id", columns="question", values="response")
    wide = wide.reindex(sub["session_id"])
    on = pd.DataFrame({"rid": sub["session_id"].values, "channel": sub["link_type"].values,
                       "received": sub["submitted_utc"].str.replace("Z", "").values,
                       "started": sub["started_utc"].str.replace("Z", "").values,
                       "code": sub["team_code"].values, "inv": sub["inv_code"].values,
                       "typed": sub["entered_code"].map(norm).values, "ref": sub["tablet_ref"].values})
    for it, q in zip(ITEMS, tags):
        on[it] = wide[q].map(SCALE).values
    scanned = pd.to_datetime(P["scanned_at_local"])
    marks = [c for c in P.columns if c not in ("batch", "form_serial", "scanned_at_local")]
    keep = (scanned.dt.strftime("%Y-%m-%d") <= PAPER_LAST) & (P[marks].ne("No mark").any(axis=1))
    Pk = P[keep]
    pack_inv = K.set_index("form_serial")["inv_code"]
    pack_code = K.set_index("form_serial")["team_code"]
    pa = pd.DataFrame({"rid": "F" + Pk["form_serial"].values, "channel": "paper",
                       "received": (scanned[keep] - pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%dT%H:%M:%S").values,
                       "started": "", "code": Pk["form_serial"].map(pack_code).fillna("").values,
                       "inv": Pk["form_serial"].map(pack_inv).fillna("").values, "typed": "", "ref": ""})
    for it, q in zip(ITEMS, tags):
        pa[it] = Pk[q].map(SCALE).values
    R = pd.concat([on, pa], ignore_index=True)
    for it in ITEMS:
        v = R[it].astype(float)
        R[it] = 6 - v if it in REVERSED else v
    site = (R["channel"] == "site") & (R["ref"] != "")
    dup = R[site].sort_values(["received", "rid"]).duplicated(["ref"] + ITEMS, keep="first")
    R = R.drop(index=dup[dup].index)
    known = (set(S["inv_code"]) | set(K["inv_code"])) - {""}
    mem = R["inv"].where(R["channel"] != "site", "")
    mem = mem.where(~((R["channel"] == "site") & R["typed"].isin(known)), R["typed"])
    R["member"] = mem
    has = R["member"] != ""
    last = R[has].sort_values(["received", "rid"]).drop_duplicates("member", keep="last")
    R = pd.concat([R[~has], last])
    return R.sort_values(["received", "rid"]).reset_index(drop=True)


def teams(D, R):
    """3.4: each return's September team"""
    reg = set(D["G"]["team_code"])
    M = D["M"]
    succ = M[M["old_code"] != ""].groupby("old_code")["new_code"].agg(lambda s: sorted(set(s))).to_dict()

    def via_map(c):
        if c in succ:
            return succ[c][0] if len(succ[c]) == 1 else None
        return c if c in reg else None

    T = D["T"]
    loads = T[T["event"] == "team list loaded"].copy()
    loads["utc"] = (pd.to_datetime(loads["at_local"]) - pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%dT%H:%M:%S")
    second = loads.sort_values("utc").groupby("tablet")["utc"].agg(lambda s: s.iloc[-1]).to_dict()
    out = []
    for ch, c, st, ref in zip(R["channel"], R["code"], R["started"], R["ref"]):
        if ch == "personal":
            out.append(c if c in reg else None)
        elif ch == "site":
            out.append(via_map(c) if st < second[ref.rsplit("-", 1)[0]] else (c if c in reg else None))
        else:
            out.append(via_map(c))
    R = R.copy()
    R["team"] = out
    n = R[R["team"].notna()].groupby("team").size()
    rep = set(n[n >= 5].index)
    return R, rep


def _tenths(fav, base):
    """a percentage to one decimal, half up, in tenths"""
    q, r = divmod(10000 * fav // base, 10)
    return q + (r >= 5)


def pages(R, rep):
    """each reported team's page: its items from the lowest percent favourable to the highest, ties in Table 1 order"""
    out = {}
    for t, grp in R[R["team"].isin(rep)].groupby("team"):
        vals = [(_tenths(int((grp[it] >= 4).sum()), int(grp[it].notna().sum())), k) for k, it in enumerate(ITEMS)]
        out[t] = [ITEMS[k] for v, k in sorted(vals)]
    return out


def company_page(R):
    vals = [(_tenths(int((R[it] >= 4).sum()), int(R[it].notna().sum())), k) for k, it in enumerate(ITEMS)]
    return [ITEMS[k] for v, k in sorted(vals)]


def plan_figures(D, read="number", every=False, team_pages=None, company=None):
    pl = D["PL"]
    use = pl if every else pl.sort_values(["plan_ref", "version"]).drop_duplicates("plan_ref", keep="last")
    out = {}
    for it in ITEMS:
        out["plans.%s.targets" % it] = 0
        out["plans.%s.agreed" % it] = 0
    for _, r in use.iterrows():
        for col in ("target_1", "target_2", "target_3"):
            v = r[col]
            if v is None or v != v:
                continue
            if isinstance(v, str):
                it = norm(v)
            elif read == "number":
                it = "TC%02d" % int(v)
            elif read == "page":
                it = team_pages[r["team_code"]][int(v) - 1]
            elif read == "company":
                it = company[int(v) - 1]
            else:
                continue
            out["plans.%s.targets" % it] += 1
            out["plans.%s.agreed" % it] += int(r["status"] == "Agreed")
    return out


def golden_figures():
    f = json.load(open(os.path.join(HERE, "figures.json")))["deliverables"]
    out = {}
    for it, v in f["plans"].items():
        for k, x in v.items():
            out["plans.%s.%s" % (it, k)] = x
    return out


def kept(c, g):
    return sum(int(c.get(k) == g[k]) for k in g)


def item_lines():
    """the item criteria scored separately, the worst honest count: each loading at one decimal and each verdict (24);
    the cracker has every one, the mirror (one factor on the team means) the ones its own figures reach"""
    f = json.load(open(os.path.join(HERE, "figures.json")))
    gold = f["deliverables"]["loadings"]
    band = f["deliverables"]["withdrawn_loading_one_decimal"]
    stay = set(f["call"]["stay"])
    means = f["rungs"]["team_means"]
    m_stay = {it for it, v in means.items() if v >= 0.75}
    kept_m = 0
    for it in ITEMS:
        one = round(means[it], 1)
        kept_m += (one == gold[it]) if it in stay else (band["low"] <= one <= band["high"])
        kept_m += (it in m_stay) == (it in stay)
    return 24, kept_m


def run(target):
    D = read(target)
    g = golden_figures()
    crack = plan_figures(D, read="number")
    k_dev = kept(crack, g)
    n_dev = len(g)
    n_lines, lines_m = item_lines()
    lines_c = n_lines
    n = n_dev + n_lines + SLIDE
    lc = (k_dev + lines_c + SLIDE) / float(n)
    mirror_dev = kept(plan_figures(D, read="number"), g)
    lm = (mirror_dev + lines_m) / float(n)
    cracker, mirror = 38 + 7 + 55 * lc, 5 + 7 + 55 * lm
    R, rep = teams(D, returns(D))
    tp, cp = pages(R, rep), company_page(R)
    stress = {
        "the full includer (each number read as that row of the team's page)":
            kept(plan_figures(D, read="page", team_pages=tp), g),
        "numbers dropped": kept(plan_figures(D, read="drop"), g),
        "every version counted, numbers read as item numbers": kept(plan_figures(D, read="number", every=True), g),
        "every version counted, numbers dropped": kept(plan_figures(D, read="drop", every=True), g),
        "numbers read as rows of the company page": kept(plan_figures(D, read="company", company=cp), g),
    }
    full = (38 + 7 + 55 * (stress["the full includer (each number read as that row of the team's page)"] + lines_c
                           + SLIDE) / n)
    miss = sorted(k for k in g if crack.get(k) != g[k])
    return dict(ask_criteria=n, device_figures=n_dev, cracker_kept_device=k_dev, cracker_missed=len(miss),
                mirror_kept_device=mirror_dev, cracker=round(cracker, 1), mirror=round(mirror, 1),
                pair_ceiling=round((cracker + mirror) / 2, 1), cracker_keep_pct=round(100 * lc, 1),
                mirror_leakage_pct=round(100 * lm, 1), stress_kept_of_device_figures=stress,
                full_includer_pair_with_mirror=round((full + mirror) / 2, 1))


def main():
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=1, default=str))
        return
    zp = os.path.join(TASK, "target.zip")
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(zp) as z:
            z.extractall(tmp)
        out = run(tmp)
        out["pack"] = "target.zip " + hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8]
        print(json.dumps(out, indent=1, default=str))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
