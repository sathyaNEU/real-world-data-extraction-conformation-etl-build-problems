"""The golden for task482 (architecture 14), read from the cut pack alone.

Conform the three payers' feeds (claims at their current version, eligibility spans, attribution runs) into the network
measure of the performance standard: each practice's total cost of care per attributed member month, pooled across the
payers. The benchmark is the 2025 figure on the final 2025 attribution times 1.052; a practice enters the two-sided track
when its 2026 figure on the final 2026 attribution comes in at least 2 per cent under. The year is open at the extract,
so the 2026 figure is the October interim run's figure carried to the year by the practice's own run-out (its 2025
attribution re-run at the same cut, the 2025 final figure over the figure of the members that cut attributes), except
for the members still in a hospital stay on 31 August: a stay is billed at discharge, so the October feeds hold only its
physicians' daily visits, and a member whose days in the unit to the cut, at the lowest per-day amount the closed long
stays of the same kind were allowed, already pass the member cap is carried at the cap. Every rung of the ladder is a
function here."""
import csv
import datetime as dt
import json
import os
import re

import numpy as np
import openpyxl
import pandas as pd

D = dt.date
TREND, MSR, CAP = 1.052, 0.02, 250000.0
PAYERS = ("MLH", "KBP", "PMH")
CUT = {2025: (D(2025, 8, 31), D(2025, 9, 30)), 2026: (D(2026, 8, 31), D(2026, 9, 30))}
FINAL_PAID = {2025: D(2026, 3, 31)}
EM = ("99211", "99212", "99213", "99214", "99215")


def _ts(x):
    return pd.Timestamp(x)


def load(target):
    f = lambda n: os.path.join(target, n)
    names = sorted(os.listdir(target))
    pick = lambda pat: f([n for n in names if re.search(pat, n)][0])
    p = {}
    # --- claims, one frame with payer, member, type, dates, codes and allowed at the current version ---
    m = pd.read_csv(pick(r"^mlh_tcoc_claims"), dtype=str, keep_default_na=False)
    m["allowed"] = m.ALLOWED_AMT.astype(float)
    m["grp"] = "M" + m.ORIG_CLM_ID.where(m.ORIG_CLM_ID != "", m.CLM_ID)
    m["first_paid"] = m.groupby("grp").PD_DT.transform("min")
    mlh = pd.DataFrame(dict(payer="MLH", member=m.MBR_ID, ctype=m.CLM_TYP.map({"PROF": "P", "OUTP": "O", "INPT": "I", "PHRM": "R"}),
                            svc=pd.to_datetime(m.SVC_FROM_DT), end=pd.to_datetime(m.SVC_THRU_DT), paid=pd.to_datetime(m.PD_DT),
                            first_paid=pd.to_datetime(m.first_paid),
                            code=m.PROC_CD, mod=m.PROC_MOD, pos=m.POS_CD, npi=m.REND_NPI, rev=m.REV_CD, allowed=m.allowed,
                            reversal=m.ADJ_TYP == "VOID", superseded=m.CLM_ID.isin(m.ORIG_CLM_ID[m.ADJ_TYP == "VOID"]),
                            grp=m.grp, ver=np.where(m.ADJ_TYP == "REPL", 2, 1), clm="M" + m.CLM_ID))
    k = pd.read_csv(pick(r"^KBP_CLAIMS"), sep="|", dtype=str, keep_default_na=False)
    k["base"] = "K" + k.CLAIM_NO.str.replace(r"-\d+$", "", regex=True)
    k["fp"] = pd.to_datetime(k.PAID_DATE, format="%m/%d/%Y")
    k["first_paid"] = k.groupby("base").fp.transform("min")
    kbp = pd.DataFrame(dict(payer="KBP", member=k.MEMBER_NO, ctype=k.CLAIM_FORM.map({"1500": "P", "UB04": "O", "NCPDP": "R"}),
                            svc=pd.to_datetime(k.FIRST_DOS, format="%m/%d/%Y"), end=pd.to_datetime(k.LAST_DOS, format="%m/%d/%Y"),
                            paid=k.fp, first_paid=k.first_paid,
                            code=k.PROCEDURE, mod=k.MODIFIER, pos=k.PLACE_OF_SVC, npi=k.RENDERING_PROV_NPI, rev=k.REVENUE,
                            allowed=k.ALLOWED_CENTS.astype(int) / 100.0, reversal=False, superseded=k.CLAIM_STATUS == "A",
                            grp=k.base, ver=np.where(k.CLAIM_NO.str.contains("-"), 2, 1), clm="K" + k.CLAIM_NO))
    kbp.loc[(k.CLAIM_FORM == "UB04") & k.BILL_TYPE.str.startswith("011"), "ctype"] = "I"
    j = json.load(open(pick(r"^pmh_partner_claims")))["records"]
    t = pd.DataFrame(j)
    t["first_paid"] = t.groupby("claimId").adjudicated.transform("min")
    t["latest"] = t.groupby("claimId").version.transform("max") == t.version
    pmh = pd.DataFrame(dict(payer="PMH", member=t.memberId, ctype=t.type.map({"professional": "P", "institutional_outpatient": "O",
                                                                             "institutional_inpatient": "I", "pharmacy": "R"}),
                            svc=pd.to_datetime(t.serviceStart), end=pd.to_datetime(t.serviceEnd), paid=pd.to_datetime(t.adjudicated),
                            first_paid=pd.to_datetime(t.first_paid), code=t.get("cpt", pd.Series([""] * len(t))).fillna(""),
                            mod=t.get("modifier", pd.Series([""] * len(t))).fillna(""),
                            pos=t.get("pos", pd.Series([""] * len(t))).fillna(""),
                            npi=t.get("renderingNpi", pd.Series([""] * len(t))).fillna(""),
                            rev=t.get("revenueCode", pd.Series([""] * len(t))).fillna(""), allowed=t.allowed.astype(float),
                            reversal=False, superseded=~t.latest, grp="P" + t.claimId, ver=t.version.astype(int),
                            clm="P" + t.claimId + ":" + t.version.astype(str)))
    c = pd.concat([mlh, kbp, pmh], ignore_index=True)
    c["current"] = ~c.reversal & ~c.superseded
    c["year"] = c.svc.dt.year
    p["claims"] = c
    # --- eligibility spans: member months by year (a month of coverage counts once) ---
    spans = []
    e = pd.read_csv(pick(r"^mlh_eligibility"), dtype=str, keep_default_na=False)
    spans += [("MLH", r.MBR_ID, r.COV_EFF_DT, r.COV_TERM_DT) for r in e.itertuples()]
    e = pd.read_csv(pick(r"^KBP_ELIG"), sep="|", dtype=str, keep_default_na=False)
    spans += [("KBP", r.MEMBER_NO, _mdy(r.EFF_DATE), _mdy(r.TERM_DATE) if r.TERM_DATE else "9999-12-31") for r in e.itertuples()]
    e = pd.read_csv(pick(r"^pmh_members"), dtype=str, keep_default_na=False)
    spans += [("PMH", r.memberId, r.coverageStart, r.coverageEnd or "9999-12-31") for r in e.itertuples()]
    p["spans"] = spans
    # --- attribution runs ---
    att, det = {}, {}
    a = pd.read_csv(pick(r"^mlh_attribution"), dtype=str)
    for r in a.itertuples():
        key = ("MLH", r.MBR_ID, "final2025" if r.RUN_ID == "PY2025-F" else "run2026")
        att[key] = r.PRACTICE_TIN
        det[key] = (int(r.QUAL_SVC_DAYS), r.LAST_QUAL_SVC_DT)
    wb = openpyxl.load_workbook(pick(r"^KBP_ATTRIBUTION"), read_only=True)
    for ws, tag in ((wb["PY2025 Final"], "final2025"), (wb["PY2026 Run 10"], "run2026")):
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i < 4 or row[0] is None:
                continue
            att[("KBP", str(row[0]), tag)] = str(row[1]).replace("-", "")
            det[("KBP", str(row[0]), tag)] = (int(row[3]), _d(row[4]).isoformat())
    a = pd.read_csv(pick(r"^pmh_attribution"), dtype=str)
    for r in a.itertuples():
        key = ("PMH", r.memberId, "final2025" if r.py == "2025" else "run2026")
        att[key] = r.tin.replace("-", "")
        det[key] = (int(r.qualDays), r.lastQualDate)
    p["att"], p["att_detail"] = att, det
    # --- the network's roster: NPI to practice by date, TIN to practice ---
    wb = openpyxl.load_workbook(pick(r"^lpn_primary_care_roster"), read_only=True)
    ros = []
    for i, row in enumerate(wb.active.iter_rows(values_only=True)):
        if i == 0:
            continue
        ros.append(dict(npi=str(row[0]), practice=row[3], tin=str(row[4]).replace("-", ""), start=_d(row[5]),
                        end=_d(row[6]) if row[6] else None))
    p["roster"] = ros
    p["tin2prac"] = {r["tin"]: r["practice"] for r in ros}
    p["practices"] = list(dict.fromkeys(r["practice"] for r in ros))     # the roster's own order of practices
    p["qualifying"] = set(pd.read_csv(pick(r"^qualifying_primary_care"), dtype=str).code)
    cf = pd.read_csv(pick(r"^payer_completion_factors"), dtype=str)
    p["cf"] = {(r.payer, int(r.incurred_month[5:7])): float(r.completion_factor) for r in cf.itertuples()}
    # --- fee schedules (ask A) ---
    wb = openpyxl.load_workbook(pick(r"^payer_em_fee_schedules"), read_only=True)
    fees = {}
    for ws, ab in zip(wb.worksheets, PAYERS):
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i >= 4 and row[0] and str(row[0]).isdigit():
                fees[(ab, str(row[0]))] = (row[2], row[3])
    p["fees"] = fees
    return p


def _mdy(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date().isoformat()


def _d(x):
    if isinstance(x, dt.datetime):
        return x.date()
    if isinstance(x, dt.date):
        return x
    return dt.date.fromisoformat(str(x)[:10])


def member_months(p, year, upto):
    """{(payer, member): months of coverage in year, January through month upto}."""
    memo = p.setdefault("_mm", {})
    key = (id(p["spans"]), year, upto)
    if key in memo:
        return memo[key]
    out = {}
    for payer, mid, s, e in p["spans"]:
        s, e = dt.date.fromisoformat(s), dt.date.fromisoformat(e)
        n = 0
        for mo in range(1, upto + 1):
            first = D(year, mo, 1)
            last = D(year + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1)
            if s <= last and e >= first:
                n += 1
        if n:
            out[(payer, mid)] = out.get((payer, mid), 0) + n
    memo[key] = out
    return out


def npi_practice(p, npi, day):
    for r in p["roster"]:
        if r["npi"] == npi and r["start"] <= day and (r["end"] is None or day <= r["end"]):
            return r["practice"]
    return None


def attribute(p, year, svc_to, paid_to, first_paid=True, tie="latest"):
    """Re-run the standard's attribution on the claims the pack holds: qualifying days by practice, plurality, ties to
    the latest day (tie 'earliest' for the other reading). A visit counts once a version of it was paid by paid_to
    (first_paid) or at its current version."""
    c = p["claims"]
    q = c[(c.ctype == "P") & (c.year == year) & c.code.isin(p["qualifying"]) & c.current & (c.svc <= _ts(svc_to))]
    q = q[(q.first_paid if first_paid else q.paid) <= _ts(paid_to)]
    cache = {}
    days = {}
    for r in q[["payer", "member", "npi", "svc"]].itertuples(index=False):
        key = (r.npi, r.svc)
        if key not in cache:
            cache[key] = npi_practice(p, r.npi, r.svc.date())
        pr = cache[key]
        if pr is None:
            continue
        days.setdefault((r.payer, r.member), {}).setdefault(pr, set()).add(r.svc.date())
    out = {}
    for mk, byp in days.items():
        if tie == "latest":
            best = sorted(byp.items(), key=lambda kv: (-len(kv[1]), -max(kv[1]).toordinal(), kv[0]))[0]
        else:
            best = sorted(byp.items(), key=lambda kv: (-len(kv[1]), min(kv[1]).toordinal(), kv[0]))[0]
        out[mk] = best[0]
    return out


def run_members(p, tag):
    return {(payer, mid): p["tin2prac"][tin] for (payer, mid, tg), tin in p["att"].items() if tg == tag}


def claims_at(p, year, svc_to, paid_to, version="current"):
    """The year's claims incurred through svc_to that a cut at paid_to counts. 'current': every claim first paid by the
    cut, at its current version (the standard's reading); 'asof': each claim at the version it stood at on the cut;
    'all': every row of the feeds summed as it stands."""
    c = p["claims"]
    c = c[(c.year == year) & (c.svc <= _ts(svc_to))]
    if version == "current":
        return c[c.current & (c.first_paid <= _ts(paid_to))]
    if version == "all":
        return c[c.paid <= _ts(paid_to)]
    c = c[~c.reversal & (c.paid <= _ts(paid_to))]
    return c[c.ver == c.groupby("grp").ver.transform("max")]


def figure(p, members, year, upto, svc_to, paid_to, complete=False, cap=CAP, version="current"):
    """Per practice: (capped allowed, member months) over the given {(payer, member): practice} set."""
    sub = claims_at(p, year, svc_to, paid_to, version)
    if complete:
        w = np.array([1.0 / p["cf"][(py, mo)] for py, mo in zip(sub.payer, sub.svc.dt.month)])
        sub = sub.assign(allowed=sub.allowed.values * w)
    tot = sub.groupby(["payer", "member"]).allowed.sum().to_dict()
    mm = member_months(p, year, upto)
    out = {}
    for mk, prac in members.items():
        a = min(cap, tot.get(mk, 0.0))
        o = out.setdefault(prac, [0.0, 0])
        o[0] += a
        o[1] += mm.get(mk, 0)
    return out


def pm(d, k):
    return d[k][0] / d[k][1]


STAY_CODES = {"99468": "NICU", "99469": "NICU", "99291": "ICU", "99239": "ICU", "99223": "MEDSURG", "99232": "MEDSURG",
              "99238": "MEDSURG"}
STAY_REV = {"0174": "NICU", "0200": "ICU"}


def stay_rates(p):
    """The lowest per-day facility allowed of the closed stays of 30 days or more in the feeds, by kind of unit."""
    c = p["claims"]
    f = c[(c.ctype == "I") & c.current].copy()
    f["los"] = (f.end - f.svc).dt.days
    f = f[f.los >= 30]
    out = {}
    for r in f.itertuples():
        kind = STAY_REV.get(r.rev)
        if kind:
            out[kind] = min(out.get(kind, 1e12), r.allowed / r.los)
    return out


def stay_day_amounts(p):
    """The median per-day facility allowed of the closed stays in the feeds, by kind of unit (revenue code)."""
    c = p["claims"]
    f = c[(c.ctype == "I") & c.current].copy()
    f["los"] = (f.end - f.svc).dt.days
    f = f[f.los >= 1]
    kind = f.rev.map({"0174": "NICU", "0200": "ICU", "0120": "MEDSURG"})
    return {k: float((f.allowed / f.los)[kind == k].median()) for k in ("NICU", "ICU", "MEDSURG") if (kind == k).any()}


def open_stays(p, year, rule="cap", rates=None):
    """The members in a stay still running at the year's cut: inpatient visits by the attending physicians day by day up to
    the cut, and no facility claim for the stay paid by it. rule 'cap': only the stays whose days to the cut, at the lowest
    per-day amount of the closed stays of the same kind of unit, already pass the member cap; 'all': every running stay.
    Returns {(payer, member): (kind, first day, days to the cut)}."""
    cut, paid = CUT[year]
    rates = rates or stay_rates(p)
    c = p["claims"]
    pr = c[(c.ctype == "P") & c.current & (c.pos == "21") & (c.year == year) & (c.svc <= _ts(cut)) & (c.first_paid <= _ts(paid)) &
           c.code.isin(list(STAY_CODES))]
    fac = c[(c.ctype == "I") & c.current & (c.year == year) & (c.first_paid <= _ts(paid))]
    fac = {k: g for k, g in fac.groupby(["payer", "member"])}
    out = {}
    for mk, g in pr.groupby(["payer", "member"]):
        days = sorted(set(g.svc.dt.date))
        if (cut - days[-1]).days > 10:
            continue
        run = [days[-1]]
        for d in reversed(days[:-1]):
            if (run[-1] - d).days > 2:
                break
            run.append(d)
        first = run[-1]
        f = fac.get(mk)
        if f is not None and ((f.svc.dt.date <= first + dt.timedelta(days=1)) & (f.end.dt.date >= days[-1])).any():
            continue
        kinds = g[g.svc.dt.date >= first].code.map(STAY_CODES)
        kind = "NICU" if (kinds == "NICU").any() else ("ICU" if (kinds == "ICU").any() else "MEDSURG")
        ndays = (cut - first).days + 1
        if rule == "cap" and not (kind in rates and ndays * rates[kind] >= CAP):
            continue
        out[mk] = (kind, first, ndays)
    return out


def golden(p, pooled=False, per_payer=False, first_paid=True, cut_paid=True, a_reported=False, f_paid=None, aug=None,
           season=False, complete=True, version="current", cap=CAP, stays=True, stays25=True, stay_months=True,
           stay_rule="cap"):
    """Every practice's figures on the golden handling: the October run's interim measure carried to the year by the
    practice's own 2025 run-out (the 2025 final figure over the figure of the members the 2025 attribution re-run at the
    same cut attributes, January to August). The options are the family's members and the ladder's rungs: pooled (one
    network run-out), per_payer (each payer's run-out on its own interim members), first_paid and cut_paid (which paid
    date counts a visit in the re-run, and by when), a_reported (the re-run's figure as the network would have reported
    it, paid by 30 September 2025 over the factors), f_paid (the 2025 figure's paid cut-off), aug (another same-cut
    membership), season (the final 2025 members' own January to August figure in place of the re-run's) and complete
    (the interim measure with the completion factors); version and cap are the claims' reading and the member cap."""
    fp = f_paid or FINAL_PAID[2025]
    f25 = run_members(p, "final2025")
    r26 = run_members(p, "run2026")
    if aug is None:
        aug = attribute(p, 2025, D(2025, 8, 31), D(2025, 9, 30) if cut_paid else FINAL_PAID[2025], first_paid=first_paid)
    if season:
        aug = f25

    def Ff(mem):
        return figure(p, mem, 2025, 12, D(2025, 12, 31), fp, version=version, cap=cap)

    def Af(mem):
        if a_reported:
            return figure(p, mem, 2025, 8, D(2025, 8, 31), D(2025, 9, 30), complete=True, version=version, cap=cap)
        return figure(p, mem, 2025, 8, D(2025, 8, 31), FINAL_PAID[2025], version=version, cap=cap)

    def If(mem):
        return figure(p, mem, 2026, 8, D(2026, 8, 31), D(2026, 9, 30), complete=complete, version=version, cap=cap)

    F, A, I = Ff(f25), Af(aug), If(r26)
    o25 = open_stays(p, 2025, stay_rule) if (stays and stays25) else {}
    o26 = open_stays(p, 2026, stay_rule) if stays else {}
    drop = lambda mem, o: {mk: v for mk, v in mem.items() if mk not in o}
    Fr, Ar, Ir = Ff(drop(f25, o25)), Af(drop(aug, o25)), If(drop(r26, o26))
    mm26 = member_months(p, 2026, 12)
    if stay_rule != "cap":
        day_amt = stay_day_amounts(p)
        sub = claims_at(p, 2026, D(2026, 8, 31), D(2026, 9, 30), version)
        so_far = sub.groupby(["payer", "member"]).allowed.sum().to_dict()
    if per_payer:
        sub = lambda mem, py: {mk: v for mk, v in mem.items() if mk[0] == py}
        parts = {py: (Ff(sub(drop(f25, o25), py)), Af(sub(drop(aug, o25), py)), If(sub(drop(r26, o26), py))) for py in PAYERS}
    Fn = sum(v[0] for v in Fr.values()) / sum(v[1] for v in Fr.values())
    An = sum(v[0] for v in Ar.values()) / sum(v[1] for v in Ar.values())
    out = {}
    for k in p["practices"]:
        bench = round(round(pm(F, k), 2) * TREND, 2)        # the standard's section 3.4, to the cent
        R = Fn / An if pooled else pm(Fr, k) / pm(Ar, k)
        interim = pm(I, k)
        rest = pm(Ir, k) * R
        months = Ir[k][1] * Fr[k][1] / Ar[k][1]
        if per_payer:
            num = den = 0.0
            for py in PAYERS:
                Fk, Ak, Ik = parts[py]
                if k not in Fk or k not in Ak or k not in Ik or not Ak[k][1] or not Ik[k][1]:
                    continue
                mmk = Ik[k][1] * Fk[k][1] / Ak[k][1]
                num += pm(Ik, k) * pm(Fk, k) / pm(Ak, k) * mmk
                den += mmk
            rest, months = num / den, den
        held = [mk for mk in o26 if r26.get(mk) == k]
        add_m = sum(mm26.get(mk, 0) for mk in held) if stay_months else 0
        if stay_rule == "cap":
            carried = cap * len(held)
        else:
            carried = sum(min(cap, o26[mk][2] * day_amt.get(o26[mk][0], 0.0) + so_far.get(mk, 0.0)) for mk in held)
        proj = (rest * months + carried) / (months + add_m)
        out[k] = dict(f2025=pm(F, k), benchmark=bench, threshold=bench * (1 - MSR), interim=interim, runout=R, projected=proj,
                      enters=proj <= bench * (1 - MSR), members2025=sum(1 for v in f25.values() if v == k),
                      members_aug=sum(1 for v in aug.values() if v == k), members_run=sum(1 for v in r26.values() if v == k),
                      mm2025=F[k][1], mm_aug=A[k][1], mm_run=I[k][1], open_at_cut=len(held),
                      open_2025=sum(1 for mk in o25 if aug.get(mk) == k))
    return out


def proxy_members(p):
    """The 2025 same-cut membership read off the final run's own fields, without re-running the attribution: a final 2025
    member counts unless the one qualifying day the run records falls after August."""
    det = p["att_detail"]
    return {mk: v for mk, v in run_members(p, "final2025").items()
            if not (det[mk + ("final2025",)][0] == 1 and det[mk + ("final2025",)][1] > "2025-08-31")}


def dilution(p, basis="members"):
    """The shortcut that reads the October run's short counts as members still to come who cost nothing: the interim
    measure scaled by the run's members over the 2025 final run's ('members'), or by the 2025 same-cut member months,
    carried to twelve months, over the final run's ('months')."""
    g = golden(p)
    out = {}
    for k, v in g.items():
        f = v["members_run"] / v["members2025"] if basis == "members" else v["mm_aug"] * 12 / 8 / v["mm2025"]
        proj = v["interim"] * f
        out[k] = dict(v, projected=proj, enters=proj <= v["threshold"])
    return out


def enters(route):
    return [k for k in route if route[k]["enters"]]


def default(p):
    """The default path: the interim run's figure carried to the year as it stands."""
    g = golden(p)
    return {k: dict(v, projected=v["interim"], enters=v["interim"] <= v["threshold"]) for k, v in g.items()}


# ---- asks ----

def paid_levels(p, rule="golden"):
    """The paid level of every established-patient visit by the practices' clinicians, January to August 2026, at the
    claim's current version: [(practice, payer, code, level)]. rule 'golden': the level of the payer's 2026 rate for the
    visit's setting (its place-of-service rule) that the claim's allowed amount reflects, every line of the claim
    counted (a Kesselcrest claim adjusted at the claim carries the adjustment on a line with no code), the rate itself,
    or half of it for a Merrinlake E&M billed with modifier 25 beside a minor procedure by the same clinician that day;
    'code': the code on the claim; 'line': the level whose rate the E&M line's own allowed equals, a line matching no
    rate read at its code; 'line_mlh': 'line' with Merrinlake's halved visits found (round 1's cracker); 'halve_all':
    'line' with every Merrinlake modifier 25 line read at twice its allowed; 'claim_only': the claim's allowed with
    Merrinlake's halved visits read at the level they match."""
    c = p["claims"]
    cur = c[(c.ctype == "P") & (c.year == 2026) & (c.svc <= _ts(D(2026, 8, 31))) & c.current]
    claim_total = cur.groupby("clm").allowed.sum().to_dict()
    v = cur[cur.code.isin(EM)]
    other = cur[~cur.code.isin(EM) & ~cur.code.isin(list(p["qualifying"])) & (cur.code != "")]
    proc_days = set(zip(other.payer, other.member, other.npi, other.svc))
    out = []
    for r in v[["payer", "member", "code", "mod", "pos", "npi", "svc", "allowed", "clm"]].itertuples(index=False):
        prac = npi_practice(p, r.npi, r.svc.date())
        if prac is None:
            continue
        lvl = EM.index(r.code) + 1
        if rule != "code":
            fac = r.pos in ("19", "22") or (r.payer == "PMH" and r.pos in ("02", "10"))
            rates = [p["fees"][(r.payer, e)][1 if fac else 0] for e in EM]
            amt = claim_total[r.clm] if rule in ("golden", "claim_only") else r.allowed
            if r.payer == "MLH" and r.mod == "25" and (rule == "halve_all" or (
                    rule in ("golden", "line_mlh") and (r.payer, r.member, r.npi, r.svc) in proc_days)):
                amt = 2 * amt
            hit = [i + 1 for i, x in enumerate(rates) if abs(x - amt) < 0.005]
            lvl = hit[0] if hit else lvl
        out.append((prac, r.payer, r.code, lvl))
    return out


def ask_a(p, rule="golden"):
    """Each practice's share of its clinicians' 2026 January to August established-patient visits (99211 to 99215) that
    the payers paid at level 5, per cent to one decimal, on paid_levels' rule."""
    out = {}
    for prac, payer, code, lvl in paid_levels(p, rule):
        o = out.setdefault(prac, [0, 0])
        o[0] += int(lvl == 5)
        o[1] += 1
    return {k: round(100.0 * a / b, 1) for k, (a, b) in out.items()}

