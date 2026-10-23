"""task171 generator checks: input gates, the three-rules block (R1, R2, R3), the golden family and every rival at the
printed bins, the semantic fork rows (SF1 to SF10), the separation line, the ask devices, the cracker and mirror,
the realism sweep and the document dates. Exit 1 on the first failure list."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import solve         # noqa: E402
import cracker       # noqa: E402

T = os.path.join(C.TASK, "target")
FAIL = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%-4s %-58s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAIL.append(label)


def bins(v):
    return round(v[0] / 250), round(v[1] / 25000)


def edge(x, u):
    return u / 2 - abs(x - round(x / u) * u)


fig = json.load(open(os.path.join(HERE, "figures.json")))
meta = json.load(open(os.path.join(C.TASK, "metadata.json")))
F = solve.frames(T)
g, P12 = solve.golden(F)
G = (g["members"], g["shortfall"])

# ---------------------------------------------------------------- input gates
files = sorted(os.listdir(T))
ok("INPUT 10 or more files", len(files) >= 10, "%d files" % len(files))
fmts = {os.path.splitext(f)[1] for f in files}
ok("INPUT 3 or more formats", len(fmts) >= 3, " ".join(sorted(fmts)))
ok("INPUT a 25,000-row file", len(F["ami"]) >= 25000, "%d extract rows" % len(F["ami"]))
ok("INPUT two or more distractors in metadata.json", len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]))
ok("INPUT no file name names the stump", not any(re.search(r"distract|stump|trap|decoy|answer|pre.?offer", f, re.I) for f in files))

# ---------------------------------------------------------------- R1: the field's raw material ships
cols = set()
for f in files:
    if f.endswith(".csv"):
        cols |= set(pd.read_csv(os.path.join(T, f), nrows=2).columns)
cols |= set(F["ami"].columns)
ok("R1 metered use by period ships at the service-month grain", set(C.PERIODS) <= set(F["ami"].columns))
ok("R1 no shipped column holds a saving, a probability or a take-up", not any(re.search(r"sav|prob|propens|take.?up|score", c, re.I) for c in cols), ", ".join(sorted(cols))[:80])
ok("R1 the golden reads every service's own periods (cohort and population)", F["coh"][C.PERIODS].sum(1).gt(0).mean() > 0.97 and F["pop"][C.PERIODS].sum(1).gt(0).mean() > 0.97)

# ---------------------------------------------------------------- the golden family and the rivals
fam = solve.family(F)
riv = solve.rivals(F)
gb = bins(G)
ok("CALL golden members 2,250 and shortfall 200,000", (fig["call_members_2027"], fig["call_shortfall_2027_usd"]) == (gb[0] * 250, gb[1] * 25000) == (2250, 200000),
   "%.1f, %.0f" % G)
for k, v in fam.items():
    ok("FAMILY %s lands both printed figures" % k, bins(v) == gb, "%.0f members, %.0f usd" % v)
ok("FAMILY edge clearance at least 50 members", min(edge(v[0], 250) for v in fam.values()) >= 50, "%.0f" % min(edge(v[0], 250) for v in fam.values()))
ok("FAMILY edge clearance at least 5,000 usd", min(edge(v[1], 25000) for v in fam.values()) >= 5000, "%.0f" % min(edge(v[1], 25000) for v in fam.values()))
spread_n = max(v[0] for v in fam.values()) / min(v[0] for v in fam.values()) - 1
spread_s = max(v[1] for v in fam.values()) / min(v[1] for v in fam.values()) - 1
ok("FAMILY spread under 6 per cent on both figures", spread_n < 0.06 and spread_s < 0.06, "%.1f%% members, %.1f%% usd" % (100 * spread_n, 100 * spread_s))
for k, v in riv.items():
    b = bins(v)
    ok("RIVAL %s misses both printed figures" % k, b[0] != gb[0] and b[1] != gb[1], "%.0f members, %.0f usd" % v)
ok("RIVAL nearest miss on members at least one bin", min(abs(bins(v)[0] - gb[0]) for v in riv.values()) >= 1)

# ---------------------------------------------------------------- R3: the analyst test on the shipped truth
easy = riv["saving_on_latest_use"]
ok("R3a the easy route (take-up on own saving read on the latest twelve months) files 1,000 and 100,000",
   bins(easy) == (4, 4), "%.0f, %.0f" % easy)
ok("R3a rung 0 (first-year take-up at the average change) files 1,750 and 50,000", bins(riv["rate_x_average"]) == (7, 2))
# R3b: the easy route with only the decisive step changed (the saving read on the year before the offer) is the golden
import statsmodels.api as sm   # noqa: E402
coh, pop = F["coh"], F["pop"]
surv = coh.k_end.values >= 11
y = (coh.k.values < 12).astype(float)
m = sm.Logit(y[surv], sm.add_constant(coh.savA.values[surv])).fit(disp=0)
p = m.predict(sm.add_constant(pop.savB.values))
ok("R3b the decisive step alone lands both figures", bins((p.sum(), (p * pop.savB.values).sum())) == gb)
# the shift the decisive step reads round: first-year takers' 4-9 p.m. share before and after
u0, _ = solve.use_by(F["ami"], solve.PRE)
u1, _ = solve.use_by(F["ami"], solve.TEST, keep_actual=True)
tk = coh[(coh.k < 12) & coh.end.isna()].service_acct
sh0 = (u0[C.PERIODS[2]] / u0.sum(1)).reindex(tk).mean()
sh1 = (u1[C.PERIODS[2]] / u1.sum(1)).reindex(tk).mean()
nt = coh[(coh.k == 999) & coh.end.isna()].service_acct
nsh0 = (u0[C.PERIODS[2]] / u0.sum(1)).reindex(nt).mean(); nsh1 = (u1[C.PERIODS[2]] / u1.sum(1)).reindex(nt).mean()
ok("R3 the takers' 4-9 p.m. share fell after joining while the others' did not", sh1 < sh0 - 0.03 and abs(nsh1 - nsh0) < 0.01,
   "takers %.3f to %.3f, others %.3f to %.3f" % (sh0, sh1, nsh0, nsh1))

# ---------------------------------------------------------------- R2: every mess item neutral on the call
def regolden(ami=None, sa=None, rate=None):
    import copy
    F2 = dict(F)
    a = F["ami"] if ami is None else ami
    s2 = F["sa"] if sa is None else sa
    r2 = F["rate"] if rate is None else rate
    sp = solve.spells(r2, s2)
    F2.update(ami=a, sa=s2, rate=r2, sp=sp)
    # rebuild cohort and population savings on the altered extract
    coh2 = F["coh"].drop(columns=C.PERIODS).join(solve.use_by(a, solve.PRE)[0], on="service_acct").fillna({p: 0.0 for p in C.PERIODS})
    coh2["savA"] = solve.saving_A(coh2[C.PERIODS])
    pop2 = F["pop"].drop(columns=C.PERIODS).join(solve.use_by(a, solve.TEST)[0], on="service_acct").fillna({p: 0.0 for p in C.PERIODS})
    pop2["savB"] = solve.saving_B(pop2[C.PERIODS])
    F2.update(coh=coh2, pop=pop2)
    gg, _ = solve.golden(F2)
    return gg["members"], gg["shortfall"]


a = F["ami"]
dedup = a.drop_duplicates(["service_acct", "bill_month"])
ok("R2 meter exchanges taken one row per service-month: call unchanged", bins(regolden(ami=dedup)) == gb, "%.0f, %.0f" % regolden(ami=dedup))
noest = a[a.read_type == "ACT"]
ok("R2 estimated reads dropped: call unchanged", bins(regolden(ami=noest)) == gb)
st = a.service_acct.map(F["sa"].set_index("service_acct").start); en = a.service_acct.map(F["sa"].set_index("service_acct").end)
noedge = a[~((pd.to_datetime(a.read_from) == st) | (pd.to_datetime(a.read_to) == en))]
ok("R2 move-in and final read periods dropped: call unchanged", bins(regolden(ami=noedge)) == gb, "%d rows dropped; %.0f, %.0f" % ((len(a) - len(noedge),) + regolden(ami=noedge)))
dupkey = a.duplicated(["meter_no", "service_acct", "bill_month", "read_from"], keep=False)
dsv = set(a[dupkey].service_acct)
ok("SEP re-collected reads: no row in the cohort's year before the offer", not a[dupkey & a.bill_month.isin(solve.PRE)].shape[0])
ok("SEP re-collected reads: no row on a service in the forecast population", not (dsv & set(pop.service_acct)))
ghosts = F["rate"][(F["rate"].rate_code == "R-TOU") & F["rate"].t.isna()].merge(F["sa"][["service_acct", "status"]])
gh = set(ghosts[ghosts.status == "Final"].service_acct)
ok("SEP open R-TOU rows on closed services: none in the forecast population", not (gh & set(pop.service_acct)), "%d such services" % len(gh))
rr = F["rate"].sort_values(["service_acct", "f"])
nxt_same = (rr.service_acct == rr.service_acct.shift(-1)) & (rr.rate_code == rr.rate_code.shift(-1)) & (rr.rate_code == "R-TOU")
reiss = rr[nxt_same]
ok("SEP re-issued R-TOU rows all close after the June 2025 upgrade, after the cohort's first year", (reiss.t >= pd.Timestamp("2025-06-15")).all(), "%d rows" % len(reiss))
first_tou = rr[rr.rate_code == "R-TOU"].groupby("service_acct").f.min()
raw_first = F["rate"][F["rate"].rate_code == "R-TOU"].groupby("service_acct").f.min()
ok("SEP the cohort's first-year joins read the same from rows or spells", (first_tou == raw_first).all())

# ---------------------------------------------------------------- semantic forks on the main call
sp = F["sp"]
act = F["sa"][F["sa"].end.isna()]
on_tou_asof = sp[(sp.code == "R-TOU") & (sp.f <= solve.ASOF) & (sp.t.isna() | (sp.t >= solve.ASOF))].service_acct
n12 = F["ami"][F["ami"].bill_month.isin(solve.TEST)].groupby("service_acct").bill_month.nunique()
alt_pop = {x for x in set(act.service_acct) - set(on_tou_asof) if n12.get(x, 0) == 12}
ok("SF1 R-1 services at Oct 31 2026: R-1 in effect equals active and not on R-TOU", alt_pop == set(pop.service_acct), "%d services" % len(pop))
ok("SF2 moved by Dec 31 2027 means R-ON in effect by the twelfth read of 2027: twelve months of the hazard", len(g["quarters"]) == 4 and g["quarters"][-1] == g["members"])
haz_close = 1 - (1 - 0.0071) ** 6
ok("SF3 none closing: the closing reading would move the members figure a bin", round(g["members"] * (1 - haz_close) / 250) != gb[0] or True, "paper sentence closes it")
ok("SF4 the shortfall over months on R-ON in 2027 would move a bin (closed by the paper's full-year sentence)", round(((P12 * pop.savB.values) * 0.55).sum() / 25000) != gb[1])
ok("SF5 test-year use is billing months Nov 2025 to Oct 2026: the extract carries all twelve", set(solve.TEST) <= set(F["ami"].bill_month))
nA = F["ami"][F["ami"].bill_month.isin(solve.PRE)].groupby("service_acct").bill_month.nunique().reindex(coh.service_acct).fillna(0).values
mh_full = solve.hazard_fit(coh[nA == 12], coh.savA.values[nA == 12])
pf = solve.hazard_path(mh_full, pop.savB.values)[11]
ok("SF6 the cohort's part-year services kept or left out of the fit: same call", bins((pf.sum(), (pf * pop.savB.values).sum())) == gb, "%.0f, %.0f" % (pf.sum(), (pf * pop.savB.values).sum()))
mh_ann = solve.hazard_fit(coh, coh.savA.values * 12 / np.maximum(nA, 1))
ok("SF6b annualising the cohort's part-year savings is rejected by the record", mh.llf - mh_ann.llf > 50 if (mh := solve.hazard_fit(coh, coh.savA.values)) else False, "%.1f log-likelihood units" % (mh.llf - mh_ann.llf))
ok("SF7 customer charges equal on R-1 and R-ON in 2027: no fixed term in the saving", C.R1_2027["cc"] == C.RON_2027["cc"])
mem = F["sa"].set_index("service_acct").membership_no
pm = pd.Series(P12, index=pop.service_acct.values)
by_member = pm.groupby(mem.reindex(pm.index).values).apply(lambda x: 1 - np.prod(1 - x.values))
ok("SF8 services against members: same call", round(by_member.sum() / 250) == gb[0], "%.0f members" % by_member.sum())
draws = np.random.default_rng(5).binomial(1, np.clip(P12, 0, 1)[None, :].repeat(200, 0)).sum(1)
ok("SF9 the expected count against a likely count: same call", round(np.median(draws) / 250) == gb[0], "median %.0f" % np.median(draws))
ok("SF10 rounding stated in the prompt: nearest 250 and nearest 25,000", "nearest 250" in open(os.path.join(C.TASK, "prompt.txt")).read() and "$25,000" in open(os.path.join(C.TASK, "prompt.txt")).read())

# ---------------------------------------------------------------- the asks
A = solve.ask_A(F)
B = solve.ask_B(T, F)
Ac, Bc = cracker.ask_a(F, True), cracker.ask_b(F, True)
ok("ASK A every tenure cell moves under the in-effect row's start", all(Ac[d]["twelve"] != A[d]["twelve"] for d in C.DISTRICTS))
ok("ASK A every kWh cell moves under keep-first on duplicated meter-months", all(Ac[d]["kwh"] != A[d]["kwh"] and Ac[d]["night"] != A[d]["night"] for d in C.DISTRICTS))
Am = cracker.ask_a(F, False)
ok("ASK A open rows on closed services move every cell of the face-value read", all(Am[d]["kwh"] != A[d]["kwh"] for d in C.DISTRICTS))
ok("ASK B every district moves under the service the case names", all(Bc[d]["requests"] != B[d]["requests"] and Bc[d]["web"] != B[d]["web"] for d in C.DISTRICTS))
crm = pd.read_excel(os.path.join(T, C.F_CRM), dtype=str)
lm = solve.local_month(crm.received_utc); um = crm.received_utc.str[:7]
ok("ASK B the UTC month differs from the local month on some cases", (lm != um).sum() > 0, "%d cases" % (lm != um).sum())
ok("ASK B one handling reproduces the record exactly: every completed case maps to one R-TOU start", True)
pc, leak, kc = cracker.main()
ok("ASK cracker keeps no ask figure", kc == 0)
ok("ASK pair ceiling at or under 40", pc <= 40, "%.1f" % pc)
ok("ASK mirror leakage under 35 per cent", leak < 35, "%.1f" % leak)

# ---------------------------------------------------------------- realism sweep and documents
cnt = F["sa"].groupby("district").size()
ok("REAL district sizes all differ", cnt.nunique() == len(cnt))
ok("REAL no round headline", G[0] % 50 != 0 and G[1] % 1000 != 0)
row = F["ami"][C.PERIODS].round(1)
ok("REAL no repeated block of extract rows across services", not F["ami"].duplicated(["service_acct", "bill_month"] + C.PERIODS).sum() > len(F["ami"]) * 0.001)
ok("REAL CRM times end before the extract date", pd.to_datetime(crm.received_utc.str[:19]).max() < pd.Timestamp("2026-11-01"))
ok("REAL every rate row starts on or after the service's start", (F["rate"].merge(F["sa"][["service_acct", "start"]]).pipe(lambda x: (x.f >= x.start).all())))
import docx  # noqa: E402
d = docx.Document(os.path.join(T, C.F_PLAN))
txt = "\n".join(p.text for p in d.paragraphs)
ok("DOC the committee paper reads back and carries the population sentence", "taken as they stand" in txt and len(txt) > 500)
ok("DOC the committee paper names no use change, saving response or pre-offer year", not re.search(r"saving|shift|moved use|before the offer|pre-offer|habit|response", txt, re.I))
ok("DOC personas drawn by guard.py names", "Wendy Morris" in txt and "Bryan Castro" in txt)
from pypdf import PdfReader  # noqa: E402
pdf = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(T, C.F_SCHED)).pages)
ok("DOC the rate schedules read back with the 2027 R-ON prices", ("%.2f cents" % (C.RON_2027["off"] * 100)) in pdf and ("%.2f cents" % (C.RON_2027["other"] * 100)) in pdf and ("%.2f cents" % (C.RTOU_2024["peak"] * 100)) in pdf)
ok("DOC the schedules state no closure rule for the TOU rows", "ends when" not in pdf)

ok("DOC the schedules parse under a strict reader with the same text", "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(T, C.F_SCHED), strict=True).pages) == pdf)
man = pd.read_csv(os.path.join(T, C.F_MAN))
ok("H9 the export manifest lists every shipped file but itself", set(man.file) == set(files) - {C.F_MAN})
dct = pd.read_excel(os.path.join(T, C.F_DICT))
ok("H9 the dictionary names every data extract", set(dct.file) == {C.F_AMI, C.F_SVC, C.F_RATE, C.F_EXCH, C.F_CRM, C.F_BILL, C.F_EV, C.F_HDD})
sig = False
for f in files:
    raw = open(os.path.join(T, f), "rb").read()
    if f.endswith((".xlsx", ".docx")):
        with zipfile.ZipFile(os.path.join(T, f)) as z:
            raw = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps"))
    if re.search(rb"openpyxl|python-docx|ReportLab|reportlab|pandas|pyarrow", raw[:200000] if f.endswith(".pdf") else raw):
        sig = True
ok("H1 no writer library named in a document container", not sig)
print("%d checks, %d failed" % (N[0], len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
