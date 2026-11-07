"""task156: the independent verifier. Recomputes the call and every ask figure from target/ alone with its own code
(pandas, a binomial GLM through formulas, pdfplumber for the PDFs) and compares with figures.json. Imports nothing
from the generator.

    python3 task156/generator/verify.py [target]"""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import pdfplumber
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
bad = []


def check(cond, msg):
    print(("ok   " if cond else "BAD  ") + msg)
    if not cond:
        bad.append(msg)


def term(d):
    y = d.year if d.month >= 7 else d.year - 1
    return y - y % 2


sites = pd.read_csv(os.path.join(T, "worksites_2026-11.csv"), dtype=str)
code_map = dict(zip(sites.code_before_2024_07, sites.worksite_code))
code_map.update(dict(zip(sites.worksite_code, sites.worksite_code)))
site_council = dict(zip(sites.worksite_code, sites.council))
reg = pd.read_csv(os.path.join(T, "membership_register_extract_2026-11-02.csv"), dtype={"worksite": str})
reg["site"] = reg.worksite.map(code_map)
reg["council"] = reg.site.map(site_council)
for c in ("date_of_birth", "joined", "ceased"):
    reg[c] = pd.to_datetime(reg[c])
reg = reg.set_index("member_no")

xl = pd.ExcelFile(os.path.join(T, "delegate_register_2018-2028.xlsx"))
dl = []
for sh in xl.sheet_names:
    df = xl.parse(sh, dtype={"Worksite code": str})
    df["term"] = int(sh[:4])
    dl.append(df)
dl = pd.concat(dl)
dl["site"] = dl["Worksite code"].map(code_map)
dl = dl.join(reg[["joined", "ceased"]], on="Member no")


def covered(day):
    """worksites with a delegate of the term in force still a member on day"""
    ts = pd.Timestamp(day)
    x = dl[(dl.term == term(day)) & (dl.joined <= ts) & (dl.ceased.isna() | (dl.ceased > ts))]
    return set(x.site)


def covered_term(day, t):
    ts = pd.Timestamp(day)
    x = dl[(dl.term == t) & (dl.joined <= ts) & (dl.ceased.isna() | (dl.ceased > ts))]
    return set(x.site)


votes = pd.read_csv(os.path.join(T, "online_votes_2022-2025.csv"))
close = {r.vote_id: dt.datetime.strptime(r.closes_local, "%Y-%m-%d %H:%M").date() for r in votes.itertuples()}
inv = pd.read_csv(os.path.join(T, "online_vote_invitations_2022-2025.csv"))
inv = inv.join(reg[["site", "council", "date_of_birth", "joined", "employment"]], on="member_no")
inv["close"] = inv.vote_id.map(close)


def design(df, day_col):
    d = pd.to_datetime(df[day_col])
    age = (d - df.date_of_birth).dt.days / 365.25
    out = pd.DataFrame(index=df.index)
    out["band"] = pd.cut(age, [0, 30, 45, 60, 200], right=False, labels=["u30", "30_44", "45_59", "60p"]).astype(str)
    out["lten"] = np.log1p(((d - df.joined).dt.days / 365.25).clip(lower=0))
    out["emp"] = df.employment.values
    out["council"] = df.council.values
    return out


X = design(inv, "close")
X["vote"] = inv.vote_id.values
cov_by_vote = {v: covered(c) for v, c in close.items()}
X["deleg"] = [1.0 if s in cov_by_vote[v] else 0.0 for s, v in zip(inv.site, inv.vote_id)]
X["y"] = inv.voted_utc.notna().astype(float).values
model = smf.glm("y ~ C(vote) + C(council) + C(band, Treatment('45_59')) + lten + C(emp, Treatment('Full time')) + deleg",
                data=X, family=sm.families.Binomial()).fit()
gamma = model.params["deleg"]
print("delegate lift (log odds) %.3f" % gamma)
check(abs(gamma - FIG["gamma"]) < 0.01, "the delegate lift agrees with figures.json (%.3f)" % FIG["gamma"])


def lin(df, vote_ref):
    df = df.copy()
    df["vote"] = vote_ref
    return model.predict(df, which="linear") if "which" in model.predict.__code__.co_varnames else \
        np.log(model.predict(df) / (1 - model.predict(df)))


# the agent's declarations, read with pdfplumber
decl = []
for f in ("tallyhouse_pab_declarations_2021.pdf", "tallyhouse_pab_declarations_2023-24.pdf"):
    with pdfplumber.open(os.path.join(T, f)) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            m = re.search(r"Employer: (.+?Council)", t)
            if not m:
                continue
            roll = re.search(r"(?:Persons on the roll|Number of persons on roll) ([\d,]+)", t)
            ret = re.search(r"(?:Ballot papers returned|Total votes received \(post and online\)) ([\d,]+)", t)
            rd = re.search(r"(?:Roll date|Roll closed) (\d{1,2} \w+ \d{4})", t)
            cd = re.search(r"(?:Ballot closed|ballot closed) (\d{1,2} \w+ \d{4})", t)
            decl.append(dict(council=m.group(1), roll=int(roll.group(1).replace(",", "")),
                             ret=int(ret.group(1).replace(",", "")),
                             rd=dt.datetime.strptime(rd.group(1), "%d %B %Y").date(),
                             cd=dt.datetime.strptime(cd.group(1), "%d %B %Y").date()))
check(len(decl) == 32, "%d declarations read" % len(decl))


def roll_frame(council, day):
    ts = pd.Timestamp(day)
    r = reg[(reg.council == council) & (reg.joined <= ts) & (reg.ceased.isna() | (reg.ceased > ts))].copy()
    return r


def eta_for(r, day, cov):
    df = r.copy()
    df["close"] = day
    Z = design(df.reset_index(), "close")
    Z["deleg"] = [1.0 if s in cov else 0.0 for s in r.site]
    Z["vote"] = "V2510"
    lp = model.predict(Z, linear=True) if False else np.log(model.predict(Z) / (1 - model.predict(Z)))
    return lp.values - model.params["C(vote)[T.V2510]"]


etas = []
for d_ in decl:
    r = roll_frame(d_["council"], d_["rd"])
    etas.append((eta_for(r, d_["cd"], covered(d_["cd"])), d_["roll"], d_["ret"]))


def gap(s):
    return sum((1 / (1 + np.exp(-(e + s)))).sum() * rl / len(e) for e, rl, _ in etas) - sum(x[2] for x in etas)


shift = brentq(gap, -6, 6)
rnd = pd.read_excel(os.path.join(T, "bargaining_round_2027.xlsx"), sheet_name="2027 round")
cands = list(rnd.Council)
cov27 = covered_term(dt.date(2026, 11, 2), 2026)
fc = {}
for c in cands:
    r = roll_frame(c, dt.date(2026, 11, 2))
    e = eta_for(r, dt.date(2027, 3, 15), cov27) + shift
    fc[c] = float((1 / (1 + np.exp(-e))).mean())
call = sorted(c for c, v in fc.items() if v >= 0.5)
check(call == FIG["call"], "the call: %d councils, as figures.json" % len(call))
for c in cands:
    check((fc[c] >= 0.5) == (FIG["turnout"][c] >= 0.5) and abs(fc[c] - FIG["turnout"][c]) < 0.01,
          "%s: %.3f against %.3f" % (c, fc[c], FIG["turnout"][c]))

# ---- Ask A ----
ra = pd.read_csv(os.path.join(T, "payroll_remittance_advices_2025-26.csv")).drop_duplicates("advice_no")
ra["pe"] = pd.to_datetime(ra.period_end)
ra.loc[ra.pe.dt.weekday == 3, "pe"] -= pd.Timedelta(days=4)
fy = (ra.pe >= "2025-07-01") & (ra.pe <= "2026-06-30") & (ra.employer != "Western Shires Payroll Services")
dues = ra[fy].groupby("employer").amount.sum().to_dict()
with pdfplumber.open(os.path.join(T, "western_shires_payroll_statements_2025-26.pdf")) as pdf:
    txt = "\n".join(p.extract_text() or "" for p in pdf.pages)
for m in re.finditer(r"(\d{2})/(\d{2})/(\d{4}) (.+?Council) (\d+) ([\d,]+\.\d{2})", txt):
    d_ = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    if dt.date(2025, 7, 1) <= d_ <= dt.date(2026, 6, 30):
        dues[m.group(4)] = dues.get(m.group(4), 0.0) + float(m.group(6).replace(",", ""))
for c, v in FIG["dues"].items():
    check(int(dues.get(c, 0.0) + 0.5) == v, "Ask A %s: %d against %d" % (c, int(dues.get(c, 0.0) + 0.5), v))

# ---- Ask B ----
di = pd.read_csv(os.path.join(T, "organiser_diary_export_2025-26.csv"))
di = di[~di.activity.isin(["Travel", "Administration"]) & (di.date >= "2025-07-01") & (di.date <= "2026-06-30")]
di = di.sort_values("last_updated_utc").drop_duplicates(["invitation_uid", "organiser", "date"], keep="last")
di["h"] = (pd.to_datetime(di.ends, format="%H:%M") - pd.to_datetime(di.starts, format="%H:%M")).dt.total_seconds() / 3600
hours = di[di.activity != "Regional delegates forum"].groupby("council").h.sum().to_dict()
fh = di[di.activity == "Regional delegates forum"].groupby("date").h.sum()
si = pd.read_csv(os.path.join(T, "regional_forum_signin_2025-26.csv"))
si["council"] = si.member_no.map(reg.council)
share = si.groupby(["forum_date", "council"]).size()
for (d_, c), k in share.items():
    hours[c] = hours.get(c, 0.0) + fh[d_] * k / share[d_].sum()
for c, v in FIG["hours"].items():
    check(int(hours.get(c, 0.0) + 0.5) == v, "Ask B %s: %d against %d" % (c, int(hours.get(c, 0.0) + 0.5), v))

print("%d disagreements" % len(bad))
sys.exit(1 if bad else 0)
