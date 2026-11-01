"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker is drawn from the careful solver's route, never from the ask list (supplemental-stumping 1.1): it lands
the call, runs the hygiene battery (1.1c) and executes every filed rule it points at. It is written here from the
files alone and shares no code with the generator's estimator:

  3.1   online sessions with status submitted, by 23:59 UK time on 4 October;
  3.2   paper forms scanned by 8 October that carry an answer;
  3.3   each return once (a tablet's re-sent copy, the same tablet reference with the same answers, kept once: the
        battery's re-sent batch), and each member once at the return received last, the member found through the
        battery's cross-system match of the invitation code (the personal link's code, the code typed on a tablet
        once its case, spaces and hyphens are normalised, and the pack each form was posted in);
  3.4   a return's team from the code on it, a code of the July structure read through HR's reorganisation map
        (paper packs printed in July; tablet sessions started before each tablet's second team list load, the
        battery's walk of a state back through a change log);
  5.1   the teams with five or more returns that count; 4.4 the returns answering all twelve items on the scale;
  note  each item's company-wide answers on the scale and the favourable ones over every return that counts; each
        team under its division on the census date (the register's previous division for a move dated after it,
        the battery's walk back through the register's own change fields).

The mirror stops at the default path on the call (one factor on the team means) and takes the same ask paths. A
figure is kept when it equals the golden's. Weights 38 / 7 / 55 over the ask criteria: the item lines (12, keyed to
the call's construction: the cracker keeps every one, the mirror the five whose team-mean loading clears 0.80 on the
side of the golden's verdict), the slide (3, keyed to the call) and every device figure.

    python3 task239/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ITEMS = ["TC%02d" % k for k in range(1, 13)]
REVERSED = {"TC04", "TC07"}
SLIDE = 3
CLOSE_UTC = "2027-10-04T22:59:59Z"          # 23:59:59 BST
PAPER_LAST = "2027-10-08"
CENSUS = "2027-09-01"


def _find(target, stem):
    hit = [f for f in os.listdir(target) if f.startswith(stem)]
    assert len(hit) == 1, (stem, hit)
    return os.path.join(target, hit[0])


def read(target):
    rd = lambda stem: pd.read_csv(_find(target, stem), dtype=str, keep_default_na=False)
    return dict(S=rd("lfp_sv27_platform_sessions"), A=rd("lfp_sv27_platform_responses"),
                P=rd("lfp_sv27_paper_scans"), K=rd("lfp_sv27_paper_packs"),
                G=rd("lfp_hr_team_register"), M=rd("lfp_hr_reorganisation_map"), T=rd("lfp_sv27_site_tablet_log"))


def norm(code):
    return "".join(ch for ch in str(code).upper() if ch.isalnum())


def returns(D, link_members=True, dedupe_resent=True, typed_link=True):
    """every return that counts under 3.1 to 3.3, one row each, with its scored answers"""
    S, A, P, K = D["S"], D["A"], D["P"], D["K"]
    sub = S[(S["status"] == "submitted") & (S["submitted_utc"] <= CLOSE_UTC)].copy()
    online_q = sorted(q for q in A["question"].unique() if q.startswith("Q3"))
    assert len(online_q) == 12
    wide = A[A["question"].isin(online_q)].pivot(index="session_id", columns="question", values="response")
    wide = wide.reindex(sub["session_id"])
    on = pd.DataFrame({"rid": sub["session_id"].values, "channel": sub["link_type"].values,
                       "received": sub["submitted_utc"].str.replace("Z", "").values,
                       "started": sub["started_utc"].str.replace("Z", "").values,
                       "code": sub["team_code"].values, "inv": sub["inv_code"].values,
                       "typed": sub["entered_code"].map(norm).values, "ref": sub["tablet_ref"].values})
    for it, q in zip(ITEMS, online_q):
        on[it] = pd.to_numeric(wide[q].values, errors="coerce")
    paper_q = [c for c in P.columns if c.startswith("Q3_")]
    assert len(paper_q) == 12
    scanned = pd.to_datetime(P["scanned_at"])
    keep = (scanned.dt.strftime("%Y-%m-%d") <= PAPER_LAST) & (P[[c for c in P.columns if c.startswith("Q")]]
                                                              .ne("9").any(axis=1))
    Pk = P[keep]
    pack_inv = K.set_index("form_serial")["inv_code"]
    pack_code = K.set_index("form_serial")["team_code"]
    pa = pd.DataFrame({"rid": "F" + Pk["form_serial"].values, "channel": "paper",
                       "received": (scanned[keep] - pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%dT%H:%M:%S").values,
                       "started": "", "code": Pk["form_serial"].map(pack_code).fillna("").values,
                       "inv": Pk["form_serial"].map(pack_inv).fillna("").values, "typed": "", "ref": ""})
    for it, q in zip(ITEMS, paper_q):
        pa[it] = pd.to_numeric(Pk[q].values, errors="coerce")
    R = pd.concat([on, pa], ignore_index=True)
    for it in ITEMS:
        v = R[it].where((R[it] >= 1) & (R[it] <= 5))
        R[it] = 6 - v if it in REVERSED else v
    if dedupe_resent:
        site = (R["channel"] == "site") & (R["ref"] != "")
        dup = R[site].sort_values(["received", "rid"]).duplicated(["ref"] + ITEMS, keep="first")
        R = R.drop(index=dup[dup].index)
    if link_members:
        known = (set(S["inv_code"]) | set(K["inv_code"])) - {""}
        mem = R["inv"].where(R["channel"] != "site", "")
        if typed_link:
            mem = mem.where(~((R["channel"] == "site") & R["typed"].isin(known)), R["typed"])
        R["member"] = mem
        has = R["member"] != ""
        last = R[has].sort_values(["received", "rid"]).drop_duplicates("member", keep="last")
        R = pd.concat([R[~has], last])
    else:
        pers = R["channel"] == "personal"
        last = R[pers].sort_values(["received", "rid"]).drop_duplicates("inv", keep="last")
        R = pd.concat([R[~pers], last])
    return R.sort_values(["received", "rid"]).reset_index(drop=True)


def teams(D, R, tablets="log", paper="map"):
    """3.4: each return's September team"""
    reg = set(D["G"]["team_code"])
    M = D["M"]
    succ = M[M["old_code"] != ""].groupby("old_code")["new_code"].agg(lambda s: sorted(set(s))).to_dict()

    def via_map(c):
        if c in succ:
            return succ[c][0] if len(succ[c]) == 1 else None
        return c if c in reg else None

    def as_is(c):
        return c if c in reg else via_map(c)

    T = D["T"]
    loads = T[T["event"] == "team list loaded"].copy()
    loads["utc"] = (pd.to_datetime(loads["at_local"]) - pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%dT%H:%M:%S")
    second = loads.sort_values("utc").groupby("tablet")["utc"].agg(lambda s: s.iloc[-1]).to_dict()
    out = []
    for ch, c, st, ref in zip(R["channel"], R["code"], R["started"], R["ref"]):
        if ch == "personal":
            out.append(c if c in reg else None)
        elif ch == "site":
            tab = ref.rsplit("-", 1)[0]
            if tablets == "log":
                out.append(via_map(c) if st < second[tab] else (c if c in reg else None))
            elif tablets == "as_is":
                out.append(as_is(c))
            else:
                out.append(via_map(c))
        else:
            out.append(via_map(c) if paper == "map" else as_is(c))
    R = R.copy()
    R["team"] = out
    n = R[R["team"].notna()].groupby("team").size()
    rep = set(n[n >= 5].index)
    R["reported"] = R["team"].isin(rep)
    R["complete"] = R[ITEMS].notna().all(axis=1)
    R["used"] = R["reported"] & R["complete"]
    return R, rep


def figures(D, R, rep, division="census"):
    out = {}
    for ch in ("personal", "site", "paper"):
        x = R[R["channel"] == ch]
        out["ledger.%s.count" % ch] = int(len(x))
        out["ledger.%s.outside" % ch] = int((~x["reported"]).sum())
        out["ledger.%s.incomplete" % ch] = int((x["reported"] & ~x["complete"]).sum())
        out["ledger.%s.used" % ch] = int(x["used"].sum())
    for it in ITEMS:
        v = R[it].dropna()
        out["favourable.%s.base" % it] = int(len(v))
        out["favourable.%s.fav" % it] = int((v >= 4).sum())
    G = D["G"].set_index("team_code")

    def div(t):
        r = G.loc[t]
        if division == "census":
            return r["previous_division"] if r["division_since"] and r["division_since"] > CENSUS else r["division"]
        return r["division"]

    for d in sorted(set(G["division"]) | set(G["previous_division"]) - {""}):
        out["divisions.%s.teams" % d] = 0
        out["divisions.%s.used" % d] = 0
    for t in rep:
        out["divisions.%s.teams" % div(t)] += 1
    for t, k in R[R["used"]].groupby("team").size().items():
        out["divisions.%s.used" % div(t)] += int(k)
    return out


def golden_figures():
    f = json.load(open(os.path.join(HERE, "figures.json")))["deliverables"]
    out = {}
    for ch, v in f["ledger"].items():
        for k, x in v.items():
            out["ledger.%s.%s" % (ch, k)] = x
    for it, v in f["favourable"].items():
        for k, x in v.items():
            out["favourable.%s.%s" % (it, k)] = x
    for d, v in f["divisions"].items():
        for k, x in v.items():
            out["divisions.%s.%s" % (d, k)] = x
    return out


def kept(c, g):
    return sum(int(c.get(k) == g[k]) for k in g)


def run(target):
    D = read(target)
    g = golden_figures()
    R, rep = teams(D, returns(D))
    crack = figures(D, R, rep)
    k_dev = kept(crack, g)
    n_dev = len(g)
    lines_c, lines_m = 12, 5
    n = n_dev + 12 + SLIDE
    lc = (k_dev + lines_c + SLIDE) / float(n)
    lm = (k_dev + lines_m) / float(n)
    cracker, mirror = 38 + 7 + 55 * lc, 5 + 7 + 55 * lm
    stress = {}
    for name, kw_r, kw_t, dv in [
            ("natural read (no member link, copies kept, codes as they stand, current division)",
             dict(link_members=False, dedupe_resent=False), dict(tablets="as_is", paper="as_is"), "current"),
            ("members linked by the personal link only", dict(typed_link=False), {}, "census"),
            ("re-sent tablet copies kept", dict(dedupe_resent=False), {}, "census"),
            ("July codes joined as they stand", {}, dict(tablets="as_is", paper="as_is"), "census"),
            ("every tablet code read through the map", {}, dict(tablets="map"), "census"),
            ("current division", {}, {}, "current")]:
        Rv, repv = teams(D, returns(D, **kw_r), **kw_t)
        stress[name] = kept(figures(D, Rv, repv, dv), g)
    miss = sorted(k for k in g if crack.get(k) != g[k])
    return dict(ask_criteria=n, device_figures=n_dev, cracker_kept_device=k_dev, cracker_missed=miss,
                cracker=round(cracker, 1), mirror=round(mirror, 1), pair_ceiling=round((cracker + mirror) / 2, 1),
                cracker_keep_pct=round(100 * lc, 1), mirror_leakage_pct=round(100 * lm, 1),
                stress_kept_of_device_figures=stress)


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
