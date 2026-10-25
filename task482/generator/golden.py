"""The golden for task482 (architecture 13), read from the cut pack alone.

Conform the three payers' feeds (claims at their current version, eligibility spans, attribution runs) into the network
measure of the performance standard: each practice's total cost of care per attributed member month, pooled across the
payers. The benchmark is the 2025 figure on the final 2025 attribution times 1.052; a practice enters the two-sided track
when its 2026 figure on the final 2026 attribution comes in at least 2 per cent under. The year is open at the extract,
so the 2026 figure is the October interim run's figure carried to the year by the practice's own run-out: its 2025
attribution re-run at the same cut (qualifying services incurred through 31 August and paid by 30 September), the 2025
final figure over the figure of the members that cut attributes. Every rung of the ladder is a function here."""
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
CCF = {"MLH": 3.25, "KBP": 2.80, "PMH": 4.10}     # the standard's care coordination fee a member month (section 5.1)
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
                            code=m.PROC_CD, mod=m.PROC_MOD, pos=m.POS_CD, npi=m.REND_NPI, allowed=m.allowed,
                            reversal=m.ADJ_TYP == "VOID", superseded=m.CLM_ID.isin(m.ORIG_CLM_ID[m.ADJ_TYP == "VOID"]),
                            grp=m.grp, ver=np.where(m.ADJ_TYP == "REPL", 2, 1)))
    k = pd.read_csv(pick(r"^KBP_CLAIMS"), sep="|", dtype=str, keep_default_na=False)
    k["base"] = "K" + k.CLAIM_NO.str.replace(r"-\d+$", "", regex=True)
    k["fp"] = pd.to_datetime(k.PAID_DATE, format="%m/%d/%Y")
    k["first_paid"] = k.groupby("base").fp.transform("min")
    kbp = pd.DataFrame(dict(payer="KBP", member=k.MEMBER_NO, ctype=k.CLAIM_FORM.map({"1500": "P", "UB04": "O", "NCPDP": "R"}),
                            svc=pd.to_datetime(k.FIRST_DOS, format="%m/%d/%Y"), end=pd.to_datetime(k.LAST_DOS, format="%m/%d/%Y"),
                            paid=k.fp, first_paid=k.first_paid,
                            code=k.PROCEDURE, mod=k.MODIFIER, pos=k.PLACE_OF_SVC, npi=k.RENDERING_PROV_NPI,
                            allowed=k.ALLOWED_CENTS.astype(int) / 100.0, reversal=False, superseded=k.CLAIM_STATUS == "A",
                            grp=k.base, ver=np.where(k.CLAIM_NO.str.contains("-"), 2, 1)))
    kbp.loc[(k.CLAIM_FORM == "UB04") & (k.REVENUE == "0120"), "ctype"] = "I"
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
                            npi=t.get("renderingNpi", pd.Series([""] * len(t))).fillna(""), allowed=t.allowed.astype(float),
                            reversal=False, superseded=~t.latest, grp="P" + t.claimId, ver=t.version.astype(int)))
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
    p["practices"] = sorted({r["practice"] for r in ros}, key=lambda n: min(r["tin"] for r in ros if r["practice"] == n))
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
    # --- care coordination remittances (ask B) ---
    rem = []
    r = pd.read_csv(pick(r"^mlh_care_coordination"), dtype=str)
    rem += [("MLH", x.PRACTICE_TIN, int(x.COV_MO[4:6]), float(x.PMT_AMT), x.PMT_DT, int(x.MBR_CNT)) for x in r.itertuples()]
    wb = openpyxl.load_workbook(pick(r"^KBP_CCF_REMIT"), read_only=True)
    for i, row in enumerate(wb.active.iter_rows(values_only=True)):
        if i == 0 or row[0] is None:
            continue
        rem.append(("KBP", str(row[2]).replace("-", ""), int(str(row[3])[5:7]), float(row[5]), _d(row[0]).isoformat(), int(row[4])))
    r = pd.read_csv(pick(r"^pmh_ccf_payments"), dtype=str)
    rem += [("PMH", x.tin.replace("-", ""), int(x.paymentRef.split("-")[3][4:6]), float(x.amount), x.period + "-01",
             int(x.memberCount)) for x in r.itertuples()]
    p["remit"] = rem
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


def golden(p, pooled=False, per_payer=False, first_paid=True, cut_paid=True, a_reported=False, f_paid=None, aug=None,
           season=False, complete=True, version="current", cap=CAP):
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
    if per_payer:
        sub = lambda mem, py: {mk: v for mk, v in mem.items() if mk[0] == py}
        parts = {py: (Ff(sub(f25, py)), Af(sub(aug, py)), If(sub(r26, py))) for py in PAYERS}
    Fn = sum(v[0] for v in F.values()) / sum(v[1] for v in F.values())
    An = sum(v[0] for v in A.values()) / sum(v[1] for v in A.values())
    out = {}
    for k in p["practices"]:
        bench = round(round(pm(F, k), 2) * TREND, 2)        # the standard's section 3.4, to the cent
        R = Fn / An if pooled else pm(F, k) / pm(A, k)
        interim = pm(I, k)
        proj = interim * R
        if per_payer:
            num = den = 0.0
            for py in PAYERS:
                Fk, Ak, Ik = parts[py]
                if k not in Fk or k not in Ak or k not in Ik or not Ak[k][1] or not Ik[k][1]:
                    continue
                mmk = Ik[k][1] * Fk[k][1] / Ak[k][1]
                num += pm(Ik, k) * pm(Fk, k) / pm(Ak, k) * mmk
                den += mmk
            proj = num / den
        out[k] = dict(f2025=pm(F, k), benchmark=bench, threshold=bench * (1 - MSR), interim=interim, runout=R, projected=proj,
                      enters=proj <= bench * (1 - MSR), members2025=sum(1 for v in f25.values() if v == k),
                      members_aug=sum(1 for v in aug.values() if v == k), members_run=sum(1 for v in r26.values() if v == k),
                      mm2025=F[k][1], mm_aug=A[k][1], mm_run=I[k][1])
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

def ask_a(p, rule="golden"):
    """Each practice's share of its clinicians' 2026 January to August established-patient visits (99211 to 99215) that
    the payers paid at level 5. rule 'golden': the paid level is the one whose rate for the visit's setting (the payer's
    place-of-service rule) the allowed amount equals, or half of which it equals where the payer halved an E&M billed
    with a same-day minor procedure; 'code': the code on the claim; 'rate': the full level-5 rate only."""
    c = p["claims"]
    v = c[(c.ctype == "P") & (c.year == 2026) & (c.svc <= _ts(D(2026, 8, 31))) & c.code.isin(EM) & c.current]
    out = {}
    for r in v[["payer", "code", "pos", "npi", "svc", "allowed"]].itertuples(index=False):
        prac = npi_practice(p, r.npi, r.svc.date())
        if prac is None:
            continue
        if rule == "code":
            lvl5 = r.code == "99215"
        else:
            fac = r.pos in ("19", "22") or (r.payer == "PMH" and r.pos in ("02", "10"))
            rate5 = p["fees"][(r.payer, "99215")][1 if fac else 0]
            lvl5 = r.code == "99215" and (abs(r.allowed - rate5) < 0.005 or (rule == "golden" and abs(2 * r.allowed - rate5) < 0.01))
        o = out.setdefault(prac, [0, 0])
        o[0] += int(lvl5)
        o[1] += 1
    return {k: round(100.0 * a / b, 1) for k, (a, b) in out.items()}


def ask_b(p, pmh_by_period=False, keep_other_programs=False):
    """The care coordination fees the three payers paid under the standard for each practice's members, by coverage
    quarter of 2026, January to September, on the March to October runs: a line counts where its amount is its members
    times the payer's fee in section 5.1. With pmh_by_period, Pemberglen's lines by the period they were posted to; with
    keep_other_programs, every line of the remittances whatever its fee."""
    out = {}
    for payer, tin, cov, amt, pdate, members in p["remit"]:
        if not keep_other_programs and abs(members * CCF[payer] - amt) > 0.005:
            continue
        m = int(pdate[5:7]) if (pmh_by_period and payer == "PMH") else cov
        if not 1 <= m <= 9:
            continue
        prac = p["tin2prac"][tin]
        q = (m - 1) // 3 + 1
        out[(prac, q)] = out.get((prac, q), 0.0) + amt
    return {k: round(v, 2) for k, v in out.items()}
