"""task249 independent verifier: recomputes every graded figure from the shipped bundle alone and checks figures.json,
submission.md and the two goldens against it. No generator module is imported. Table 4.3, the cap, the band and the
exposure ceiling are read from the shipped PDFs; the retest gain is refitted per pair by non-linear least squares;
each account's share is computed by a different construction from the solver's simulation: the exact posterior of
each pool member's ability on a grid (Table 4.3's error at each ability), the account's top share of its own pool by
MAT-R, and the referral probability in closed form over the interval distribution.

    python3 task249/generator/verify.py [target.zip or target dir]
"""
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader
from scipy.optimize import curve_fit
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
F = {"attempts": "mat_r_attempts_2028.parquet", "exposure": "mat_r_exposure_2028.parquet",
     "register": "candidate_register_2028.csv", "shares": "results_shared_2028.csv", "shortlists": "shortlists_2028.csv",
     "cases": "integrity_cases_2028.xlsx", "study": "mat_v_equivalence_study_2028.csv",
     "standard": "MAL-IS-04_integrity_standard.pdf", "manual": "mat_technical_manual_ch4.pdf",
     "plans": "client_plans_2029.xlsx", "accounts": "client_accounts.csv", "colleges": "colleges.csv"}
FAILS = []


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def pdf_text(path):
    return " ".join(" ".join(p.extract_text() for p in PdfReader(path).pages).split())


def unpack(src):
    if os.path.isdir(src):
        return src
    d = tempfile.mkdtemp(prefix="t249v_")
    with zipfile.ZipFile(src) as z:
        z.extractall(d)
    return os.path.join(d, "target")


# ------------------------------------------------------------------ the filed numbers, read from the documents
def filed(tgt):
    std = pdf_text(os.path.join(tgt, F["standard"]))
    cap = float(re.search(r"no more than (\d+) per cent of the genuine candidates", std).group(1)) / 100
    z = float(re.search(r"plus (\d\.\d+) times the MAT-V standard error", std).group(1))
    ceiling = float(re.search(r"exposure exceeds (\d+) per cent", std).group(1)) / 100
    man = pdf_text(os.path.join(tgt, F["manual"]))
    rows = re.findall(r"([+-]\d\.\d\d) (\d\.\d{3}) (\d\.\d{3}) (\d\.\d{3})", man)
    tab = np.array([[float(x) for x in r] for r in rows])
    check(len(tab) == 25 and tab[0, 0] == -3.0 and tab[-1, 0] == 3.0, "Table 4.3 read: 25 rows from -3 to +3")
    return cap, z, ceiling, tab


def se_at(t, tab, col):
    return np.interp(np.clip(t, tab[0, 0], tab[-1, 0]), tab[:, 0], tab[:, col])


# ------------------------------------------------------------------ the call
def retest(study):
    d = study.dropna(subset=["mat_v_logit"]).copy()
    d["days"] = (pd.to_datetime(d["mat_v_started_ist"]).dt.normalize() - pd.to_datetime(d["mat_r_started_ist"]).dt.normalize()).dt.days
    d["gain"] = d["mat_v_logit"] - d["mat_r_logit"]
    f = lambda x, c, a, tau: c + a * np.exp(-x / tau)
    (c, a, tau), _ = curve_fit(f, d["days"].values.astype(float), d["gain"].values, p0=(0.05, 0.3, 15.0))
    return d, (lambda g: c + a * np.exp(-np.asarray(g, float) / tau)), (c, a, tau)


def plans_sheet(path):
    ws = load_workbook(path, data_only=True)["2029 plans"]
    rows = list(ws.iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == "Code")
    df = pd.DataFrame(rows[h + 1:], columns=rows[h]).dropna(subset=["Code"])
    return df.set_index("Code")


def gaps_of(row):
    """days from the 2029 MAT-R sitting to the selection day, every arrangement equally likely"""
    fmt = row["Selection format"]
    if fmt in ("Day-one campus drive", "First-company campus drive"):
        return np.array([2])                       # lab sitting on day 1, selection day on day 3
    m = re.search(r"(\d{1,2} \w+ 2029) to (\d{1,2} \w+ 2029)", str(row["Selection days"]))
    d0, d1 = (dt.datetime.strptime(m.group(k), "%d %B %Y").date() for k in (1, 2))
    sel = [d0 + dt.timedelta(days=k) for k in range((d1 - d0).days + 1)]
    sit = [dt.date(2029, 7, d) + dt.timedelta(days=k) for d in (2, 9, 16, 23) for k in (0, 1)]
    return np.array([(a - b).days for a in sel for b in sit])


def pools(tgt):
    reg = set(pd.read_csv(os.path.join(tgt, F["register"]))["candidate_id"])
    att = pd.read_parquet(os.path.join(tgt, F["attempts"]))
    comp = att[(att["attempt_status"] == "completed") & att["candidate_id"].isin(reg)].set_index("candidate_id")
    acc = pd.read_csv(os.path.join(tgt, F["accounts"]))
    merged = {r.account_code: re.search(r"into ([A-Z]{3})", r.note).group(1) for r in acc.itertuples() if r.status == "merged"}
    sh = pd.read_csv(os.path.join(tgt, F["shares"]))
    sh["account_code"] = sh["account_code"].replace(merged)
    out = {}
    for code, g in sh.groupby("account_code"):
        ids = pd.Index(g["candidate_id"].unique())
        out[code] = comp.loc[ids.intersection(comp.index), ["theta_logit", "se_logit"]]
    return out


def share(pool, q, gaps, gain, tab, z):
    e, s = pool["theta_logit"].values, pool["se_logit"].values
    mu, tau2 = e.mean(), e.var(ddof=1) - np.mean(s ** 2)
    k = max(1, int(round(q * len(e))))
    top = np.sort(e)[::-1][:k]
    th = np.linspace(-4, 5, 451)
    su = se_at(th, tab, 1)
    v = np.linspace(-5, 7, 4801)
    h = v + z * se_at(v, tab, 2)                      # referred when MAT-R exceeds h(MAT-V)
    vstar = np.interp(top, h, v)                      # h is increasing
    # the referral probability on a grid of thresholds, averaged over the interval distribution, then read off
    vg = np.linspace(vstar.min() - 0.01, vstar.max() + 0.01, 801)
    sv = se_at(th, tab, 2)
    gu, gw = np.unique(gaps, return_counts=True)
    tabp = np.zeros((len(vg), len(th)))
    for g, w in zip(gu, gw):
        tabp += w * norm.cdf((vg[:, None] - th[None, :] - gain(g)) / sv[None, :])
    tabp /= gw.sum()
    total = 0.0
    for lo in range(0, k, 4000):
        blk, vs = top[lo:lo + 4000], vstar[lo:lo + 4000]
        ll = -(th - mu) ** 2 / (2 * tau2) - (blk[:, None] - th[None, :]) ** 2 / (2 * su[None, :] ** 2) - np.log(su)[None, :]
        post = np.exp(ll - ll.max(1, keepdims=True))
        post /= post.sum(1, keepdims=True)
        pos = np.interp(vs, vg, np.arange(len(vg)))
        i0 = np.clip(np.floor(pos).astype(int), 0, len(vg) - 2)
        f = (pos - i0)[:, None]
        p = (1 - f) * tabp[i0] + f * tabp[i0 + 1]
        total += float((post * p).sum())
    return total / k


def the_call(tgt, cap, z, tab):
    study = pd.read_csv(os.path.join(tgt, F["study"]))
    pairs, gain, coef = retest(study)
    pl = plans_sheet(os.path.join(tgt, F["plans"]))
    po = pools(tgt)
    res = {}
    for code, row in pl.iterrows():
        q = float(row["Shortlist"]) / float(row["Expected applicants"])
        res[code] = share(po[code], q, gaps_of(row), gain, tab, z)
    pairs["ref"] = pairs["mat_r_logit"] > pairs["mat_v_logit"] + z * pairs["mat_v_se"]
    study_rates = (float(pairs.loc[pairs["days"] <= 3, "ref"].mean()), float(pairs.loc[pairs["days"] >= 42, "ref"].mean()))
    return res, study_rates, coef, pairs


# ------------------------------------------------------------------ the asks
def asks(tgt, ceiling):
    reg = pd.read_csv(os.path.join(tgt, F["register"]))
    regset = set(reg["candidate_id"])
    att = pd.read_parquet(os.path.join(tgt, F["attempts"]))
    att = att[att["candidate_id"].isin(regset)]
    # A: weekly exposure, distinct candidates, IST weeks from Monday 3 July 2028
    ist = pd.to_datetime(att["started_utc"]) + pd.Timedelta(minutes=330)
    att = att.assign(week=(ist.dt.normalize() - pd.Timestamp("2028-07-03")).dt.days // 7)
    ex = pd.read_parquet(os.path.join(tgt, F["exposure"]))
    lab = ex.merge(att[["booking_ref", "attempt_no", "candidate_id", "week"]], on=["booking_ref", "attempt_no"], how="inner")
    over, rested = [], set()
    for k in range(4):
        den = att.loc[att["week"] == k, "candidate_id"].nunique()
        x = lab[lab["week"] == k].drop_duplicates(["candidate_id", "item_id"]).groupby("item_id").size() / den
        over.append(int((x > ceiling).sum()))
        rested |= set(x.index[x > ceiling])
    # B: each sitting's latest decision across the candidate's cases
    cases = pd.read_excel(os.path.join(tgt, F["cases"]), sheet_name="Case log")
    last = cases.sort_values(["decided", "case_ref"]).drop_duplicates("candidate_id", keep="last")
    stood = set(last.loc[last["finding"].isin(["confirmed impersonation", "confirmed on appeal"]), "candidate_id"])
    col = pd.read_csv(os.path.join(tgt, F["colleges"])).set_index("college_code")["tier"]
    tier = reg.set_index("candidate_id")["college_code"].map(col)
    sl = pd.read_csv(os.path.join(tgt, F["shortlists"]))
    shortlisted = pd.Series(sl["candidate_id"].unique())
    imp = {}
    for t in ("T1", "T2", "T3", "T4"):
        n = sum(1 for c in stood if tier.get(c) == t)
        d = int((shortlisted.map(tier) == t).sum())
        imp[t] = (n, 1000.0 * n / d)
    # C: a candidate's attempts in time order are the booking; device of the first; interrupted if any was
    a = att.sort_values(["candidate_id", "started_utc"])
    first = a.groupby("candidate_id")["device"].first()
    lastd = a.groupby("candidate_id")["device"].last()
    hit = a.groupby("candidate_id")["attempt_status"].apply(lambda s: (s == "interrupted").any())
    intr = {}
    for dvc in ("desktop", "laptop", "tablet"):
        b = first.index[first == dvc]
        h = b[hit.reindex(b).values]
        intr[dvc] = (100.0 * len(h) / len(b), int((lastd.reindex(h) != dvc).sum()))
    return over, len(rested), imp, intr


# ------------------------------------------------------------------ the deliverables against the recomputation
def main(src):
    tgt = unpack(src)
    cap, z, ceiling, tab = filed(tgt)
    check((cap, z, ceiling) == (0.15, 1.96, 0.12), "the cap, the band and the ceiling read from MAL-IS-04")
    res, study_rates, coef, pairs = the_call(tgt, cap, z, tab)
    flagged = sorted(c for c, v in res.items() if v > cap)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    check(sorted(fig["call"]["flagged"]) == flagged, "the 15 accounts recompute (exact posterior): %s" % ", ".join(flagged))
    lo = min(v for v in res.values() if v > cap)
    hi = max(v for v in res.values() if v <= cap)
    check(lo >= 0.20 and hi < cap - 0.04, "flagged shares at least 20 per cent (%.3f), kept at least 4 points under the cap (%.3f)" % (lo, hi))
    c = fig["components"]
    check(round(100 * study_rates[0], 1) == c["study_rate_within_3_days_pct"] and round(100 * study_rates[1], 1) == c["study_rate_6_weeks_or_more_pct"],
          "the study's rates by interval: %.1f and %.1f per cent" % (100 * study_rates[0], 100 * study_rates[1]))
    check(abs(coef[0] - c["retest_gain_c"]) < 0.01 and abs(coef[1] - c["retest_gain_a"]) < 0.02 and abs(coef[0] + coef[1] * np.exp(-2 / coef[2]) - c["retest_gain_at_2_days"]) < 0.01,
          "the retest gain refitted per pair: %.3f + %.3f exp(-days/%.1f)" % coef)
    # the study's top tenth: shrinkage at the ability against the reported error
    e, s = pairs["mat_r_logit"].values, pairs["mat_r_se"].values
    mu, tau2 = e.mean(), e.var(ddof=1) - np.mean(s ** 2)
    k = int(round(0.1 * len(e)))
    idx = np.argsort(-e, kind="stable")[:k]
    gain = lambda g: coef[0] + coef[1] * np.exp(-np.asarray(g, float) / coef[2])
    m = e[idx].copy()
    for _ in range(60):
        m = mu + tau2 / (tau2 + se_at(m, tab, 1) ** 2) * (e[idx] - mu)
    mk = mu + tau2 / (tau2 + s[idx] ** 2) * (e[idx] - mu)
    scored = pairs["mat_v_logit"].values[idx].mean()
    g = gain(pairs["days"].values[idx])
    check(k == c["study_top_tenth_n"] and abs((m + g).mean() - scored) <= 0.02 and scored - (mk + g).mean() >= 0.08,
          "study's top tenth (%d): scored %.3f, at the ability %.3f, at the reported error %.3f" % (k, scored, (m + g).mean(), (mk + g).mean()))
    over, rested, imp, intr = asks(tgt, ceiling)
    a = fig["asks"]
    weeks = ["week_of_3_july", "week_of_10_july", "week_of_17_july", "week_of_24_july"]
    check([a["items_over_ceiling"][w] for w in weeks] == over and a["items_rested_for_2029"] == rested,
          "exposure: %s over, %d rested" % (over, rested))
    check(all(a["impersonations_confirmed"][t] == imp[t][0] and a["impersonations_per_thousand_shortlisted"][t] == round(imp[t][1], 1) for t in imp),
          "impersonations: " + "; ".join("%s %d %.1f" % (t, *imp[t]) for t in imp))
    check(all(a["interrupted_share_pct"][d] == round(intr[d][0], 2) and a["interrupted_finished_on_another_device"][d] == intr[d][1] for d in intr),
          "interruptions: " + "; ".join("%s %.2f %d" % (d, *intr[d]) for d in intr))
    # submission.md and the goldens
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check(all(code in sub.split("## 3.")[0] for code in flagged), "submission block 1 names every flagged account")
    for w, label in zip(weeks, ["3 July", "10 July", "17 July", "24 July"]):
        check("| %s | %d |" % (label, a["items_over_ceiling"][w]) in sub, "submission exposure row %s" % label)
    check("rested before the 2029 season (over 12 per cent in any test week): %d." % rested in sub, "submission rested count")
    for t in ("T1", "T2", "T3", "T4"):
        check("| %s | %d | %.1f |" % (t, imp[t][0], imp[t][1]) in sub, "submission impersonation row %s" % t)
    for dvc in ("desktop", "laptop", "tablet"):
        check("| %s | %.2f per cent | %d |" % (dvc, intr[dvc][0], intr[dvc][1]) in sub, "submission interruption row %s" % dvc)
    wb = load_workbook(os.path.join(TASK, "golden", "verification_bands_2029.xlsx"), data_only=True)
    ws = wb["2029 bands"]
    ext = sorted(r[0] for r in ws.iter_rows(min_row=5, values_only=True) if r[0] and r[10] and str(r[10]).startswith("Extended"))
    check(ext == flagged, "golden workbook: MAT-V Extended rows are the 15")
    note = pdf_text(os.path.join(TASK, "golden", "account_referral_note_2029.pdf"))
    check(all(code in note for code in flagged) and "15 client accounts move to MAT-V Extended" in note, "golden note names the 15")
    print("\n%d failure(s)" % len(FAILS))
    return len(FAILS)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target.zip")) else 0)
