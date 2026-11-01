"""The clean truth: every index lumbar operation, its patient, case-mix, complication, follow-up
answer and later spells, before any system writes a record or any mess is applied."""
import datetime as dt
import numpy as np
import pandas as pd
from common import *

FY_ORDER = ["2022-23", "2023-24", "2024-25", "2025-26"]


def stream(*keys):
    return np.random.default_rng(np.random.SeedSequence([SEED] + [int(k) for k in keys]))


def weekdays(start, end):
    d, out = start, []
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


BANK = {dt.date(2022, 4, 15), dt.date(2022, 4, 18), dt.date(2022, 5, 2), dt.date(2022, 6, 2), dt.date(2022, 6, 3),
        dt.date(2022, 8, 29), dt.date(2022, 9, 19), dt.date(2022, 12, 26), dt.date(2022, 12, 27), dt.date(2023, 1, 2),
        dt.date(2023, 4, 7), dt.date(2023, 4, 10), dt.date(2023, 5, 1), dt.date(2023, 5, 8), dt.date(2023, 5, 29),
        dt.date(2023, 8, 28), dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
        dt.date(2024, 4, 1), dt.date(2024, 5, 6), dt.date(2024, 5, 27), dt.date(2024, 8, 26), dt.date(2024, 12, 25),
        dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
        dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}


def odi_sections(total, rng):
    """Ten section answers (0-5) whose total is close to the ODI total (0-100 -> 0-50)."""
    target = int(round(total / 2.0))
    target = max(0, min(50, target))
    base = np.full(10, target // 10)
    rem = target - base.sum()
    idx = rng.permutation(10)[:rem]
    base[idx] += 1
    # spread: move single points between sections without changing the total
    for _ in range(int(rng.integers(2, 7))):
        a, b = rng.integers(0, 10, 2)
        if base[a] > 0 and base[b] < 5 and a != b:
            base[a] -= 1
            base[b] += 1
    return base


def build_world():
    ops = []
    pid = 0
    for pi, p in enumerate(PROVIDERS):
        for fi, fy in enumerate(FY_ORDER):
            n = int(round(1.15 * p["vol"][fi - 1])) if fi > 0 else int(round(1.07 * p["vol"][0]))
            r = stream(p["key"], fi, 1)
            days = [d for d in weekdays(*FY[fy]) if d not in BANK]
            if p["kind"] == "IS":
                sat = [d for d in [FY[fy][0] + dt.timedelta(days=k) for k in range(366)]
                       if d.weekday() == 5 and d <= FY[fy][1]]
                days = days + sat[::3]
            opd = sorted(r.choice(len(days), size=n, replace=True))
            for j in range(n):
                pid += 1
                op_date = days[opd[j]]
                age = float(np.clip(r.normal(56 + 4 * p["sev"], 13.5), 19, 91))
                female = bool(r.random() < 0.53)
                stenosis = bool(r.random() < 1 / (1 + np.exp(-(age - 60) / 7.0)))
                smoker = bool(r.random() < 0.19 - 0.04 * (age > 65))
                prev = bool(r.random() < 0.10 + 0.05 * p["sev"])
                symp12 = bool(r.random() < 0.44 + 0.08 * stenosis)
                pre = float(np.clip(r.normal(44 + 3.5 * p["sev"] + 3.0 * stenosis, 13.5), 8, 90))
                ops.append(dict(pid=pid, prov=p["key"], fy=fy, op_date=op_date, age=age, female=female,
                                stenosis=stenosis, smoker=smoker, prev=prev, symp12=symp12, pre_true=pre,
                                rkey=(p["key"], fi, j)))
    w = pd.DataFrame(ops)
    w["disc"] = ~w["stenosis"]
    # filed case-mix model on the true pre-operative score
    E = (CASEMIX["intercept"] + CASEMIX["pre_odi_minus_45"] * (w.pre_true - 45) + CASEMIX["age_minus_55"] * (w.age - 55)
         + CASEMIX["female"] * w.female + CASEMIX["smoker"] * w.smoker + CASEMIX["previous_lumbar_surgery"] * w.prev
         + CASEMIX["symptoms_over_12_months"] * w.symp12 + CASEMIX["disc_herniation"] * w.disc)
    w["E_true"] = E
    pmap = {p["key"]: p for p in PROVIDERS}
    comp, imp, drop, resp, death, los, tr, pre_done = [], [], [], [], [], [], [], []
    emerg, inj = [], []
    for row in w.itertuples():
        p = pmap[row.prov]
        r = stream(row.rkey[0], row.rkey[1], row.rkey[2] + 1000, 2)
        mult = 1 + 0.45 * (row.age > 70) + 0.35 * row.smoker + 0.45 * row.prev
        c = bool(r.random() < min(0.9, p["c"] * mult / 1.18))
        comp.append(c)
        d = float(np.clip(r.normal(17.5, 2.5), 10, 25)) if c else 0.0
        drop.append(d)
        # later emergency admissions: every complication within 30 days of leaving hospital;
        # unrelated emergencies anywhere in the year after the operation
        ev = []
        if c:
            ev.append(("comp", int(min(29, 1 + r.exponential(8.0)))))
        if r.random() < 0.013 + 0.010 * (row.age > 70):
            ev.append(("other", int(r.integers(1, 365))))
        emerg.append(ev)
        # planned spinal injections in the year (day cases), patients with persisting pain
        j = bool((not c) and r.random() < 0.011)
        inj.append(j)
        imp.append(float(row.E_true + p["u"] + r.normal(0, 9.0) - d))
        pd_ = 0.004 + (0.012 if c else 0.0) + 0.004 * (row.age > 78)
        death.append(bool(r.random() < pd_))
        pr = p["r"] * (1 + 0.006 * (row.age - 55))
        pr = pr * (0.48 if ev else 1.0)
        resp.append(bool(r.random() < min(0.95, pr)))
        base_los = 0 if (row.disc and r.random() < 0.45) else int(r.choice([1, 1, 2, 2, 2, 3, 4]))
        if row.age > 72 and r.random() < 0.3:
            base_los += int(r.integers(1, 4))
        los.append(base_los)
        tr.append(bool(p["kind"] == "NHS" and row.age > 70 and r.random() < 0.035))
        pre_done.append(bool(r.random() < 0.885))
    w["emerg"] = emerg
    w["inj"] = inj
    w["comp"] = comp
    w["drop"] = drop
    w["imp_true"] = imp
    w["died_12m"] = death
    w["resp_12m"] = resp
    w["los"] = los
    w["transfer"] = tr
    w["pre_done"] = pre_done
    w["post_true"] = np.clip(w.pre_true - w.imp_true, 0, 100)
    return w


# =============================================================================================
# The rest of the truth, each drawn from its own streams so the tuned core above never moves.
EXTRACT_FROM = dt.date(2022, 4, 1)
EXTRACT_TO = dt.date(2026, 9, 30)
NEW_PLATFORM = dt.date(2025, 4, 1)
D = dt.timedelta


def practices():
    r = stream(9100)
    out = {}
    used = set()
    for d in DISTRICTS:
        k = int(r.integers(2, 5))
        codes = []
        while len(codes) < k:
            c = "W8%04d" % int(r.integers(1000, 9999))
            if c not in used:
                used.add(c)
                codes.append(c)
        out[d] = codes
    return out


GP = practices()


def hexid(r, n):
    return "".join("0123456789ABCDEF"[int(x)] for x in r.integers(0, 16, n))


def ukeys(r, n, fmt, lo, hi):
    out, seen = [], set()
    while len(out) < n:
        for v in r.integers(lo, hi, size=max(16, 2 * (n - len(out)))):
            v = int(v)
            if v not in seen:
                seen.add(v)
                out.append(fmt % v)
                if len(out) == n:
                    break
    return out


def odi_from(sections, n_answered, rng):
    s = np.array(sections, dtype=float)
    keep = np.ones(10, bool)
    if n_answered < 10:
        keep[rng.permutation(10)[:10 - n_answered]] = False
    ans = [int(v) if k else None for v, k in zip(s, keep)]
    tot = sum(v for v in ans if v is not None)
    score = tot / (5.0 * n_answered) * 100.0
    return ans, tot, score


def n_sections(r):
    u = r.random()
    if u < 0.93:
        return 10
    if u < 0.97:
        return 9
    if u < 0.985:
        return 8
    return int(r.integers(5, 8))


def provider_at(key, day):
    if key == RENAME["old_key"] and day >= RENAME["date"]:
        return RENAME["new_key"]
    return key


def extras(w):
    """Per-operation attributes the systems record: identifiers, residence, booking, questionnaires."""
    pmap = {p["key"]: p for p in PROVIDERS}
    rid = stream(9200)
    w["pseudo"] = [hexid(rid, 10) for _ in range(len(w))]
    assert w.pseudo.is_unique
    recs = []
    for row in w.itertuples():
        p = pmap[row.prov]
        rx = stream(row.rkey[0], row.rkey[1], row.rkey[2] + 3000, 5)
        if p["kind"] == "NHS" and rx.random() < 0.7:
            dist = CATCH[row.prov][int(rx.integers(0, len(CATCH[row.prov])))]
        else:
            dist = DISTRICTS[int(rx.integers(0, len(DISTRICTS)))]
        gp = GP[dist][int(rx.integers(0, len(GP[dist])))]
        adm_off = 1 if (p["kind"] == "NHS" and row.age > 65 and rx.random() < 0.25) else 0
        res_rate = 0.09 if p["kind"] == "NHS" else 0.14
        booked = row.op_date
        if rx.random() < res_rate:
            if rx.random() < 0.4:
                booked = row.op_date + D(days=int(rx.integers(3, 26)))      # brought forward
            else:
                booked = row.op_date - D(days=int(rx.integers(10, 121)))    # postponed
        lead = int(rx.integers(14, 71))
        reg = booked - D(days=lead)
        pre_c = min(reg + D(days=int(rx.integers(0, 10))), booked)
        gap = (row.op_date - pre_c).days
        if 89 <= gap <= 91:
            pre_c = row.op_date - D(days=87 if gap == 89 else 93)
        n_pre = n_sections(rx)
        rs = stream(row.rkey[0], row.rkey[1], row.rkey[2] + 4000, 6)
        pre_secs = odi_sections(row.pre_true, rs)
        pre_ans, pre_tot, pre_score = odi_from(pre_secs, n_pre, rs)
        n_m12 = n_sections(rx)
        late = int(np.floor(rx.exponential(19.0)))
        dd12 = 357 + late
        if 446 <= dd12 <= 456:
            dd12 = 444 if dd12 <= 450 else 458
        m12_c = row.op_date + D(days=dd12)
        post_secs = odi_sections(row.post_true, rs)
        post_ans, post_tot, post_score = odi_from(post_secs, n_m12, rs)
        if row.symp12:
            dur = 3 if rx.random() < 0.55 else 4
        else:
            dur = 1 if rx.random() < 0.25 else 2
        unl = rx.random()
        rn = stream(row.rkey[0], row.rkey[1], row.rkey[2] + 6000, 8)
        ni_u = rn.random()
        not_invited = bool(reg >= NEW_PLATFORM and ni_u < NOT_INVITED[row.prov])
        recs.append(dict(district=dist, gp=gp, adm_off=adm_off, booked=booked, reg=reg, pre_c=pre_c,
                         n_pre=n_pre, pre_ans=pre_ans, pre_tot=pre_tot, pre_score=pre_score,
                         n_m12=n_m12, m12_c=m12_c, post_ans=post_ans, post_tot=post_tot, post_score=post_score,
                         dur=dur, unl_u=unl, ni_u=ni_u, not_invited=not_invited, sex_code=2 if row.female else 1,
                         yob=(row.op_date.year - int(row.age) - (1 if rx.random() < 0.5 else 0))))
    x = pd.DataFrame(recs, index=w.index)
    w = pd.concat([w, x], axis=1)
    w["platform"] = np.where(w.reg >= NEW_PLATFORM, "new", "old")
    return w


NOT_INVITED = {40117: 0.0058, 40152: 0.0048, 40188: 0.0074, 41206: 0.0150, 41231: 0.0078, 41274: 0.0158, 41309: 0.0190, 41355: 0.0166, 41388: 0.0124, 41402: 0.0036}
UNLINKED = {40117: 0.068, 40152: 0.058, 40188: 0.085, 41206: 0.105, 41231: 0.094, 41274: 0.118,
            41309: 0.082, 41355: 0.10, 41388: 0.094, 41402: 0.094}


def make_spells(w):
    """Every admitted patient care spell the board's cohort extract holds."""
    pmap = {p["key"]: p for p in PROVIDERS}
    rows = []
    for row in w.itertuples():
        p = pmap[row.prov]
        rs = stream(row.rkey[0], row.rkey[1], row.rkey[2] + 5000, 7)
        adm = row.op_date - D(days=row.adm_off)
        dis = row.op_date + D(days=int(row.los))
        if row.stenosis:
            diag = "M480" if rs.random() < 0.8 else "M544"
            proc = INDEX_STENOSIS[int(rs.choice(4, p=[0.30, 0.42, 0.18, 0.10]))]
        else:
            diag = "M511" if rs.random() < 0.7 else "M512"
            proc = INDEX_DISC[int(rs.choice(3, p=[0.12, 0.18, 0.70]))]
        meth = ["11", "12", "13"][int(rs.choice(3, p=[0.8, 0.15, 0.05]))]
        cls = "2" if (int(row.los) == 0 and row.adm_off == 0) else "1"
        dest = "51" if row.transfer else "19"
        prov = provider_at(row.prov, adm)
        rows.append(dict(pid=row.pid, pseudo=row.pseudo, prov=prov, adm=adm, dis=dis, meth=meth, cls=cls,
                         diag=diag, proc=proc, opdate=row.op_date, age=int(row.age), sex=row.sex_code,
                         dest=dest, district=row.district, kind="index"))
        cont_end = dis
        if row.transfer:
            ch = 40231 if row.prov == 40152 else 40244
            cont_end = dis + D(days=int(rs.integers(3, 22)))
            rows.append(dict(pid=row.pid, pseudo=row.pseudo, prov=ch, adm=dis, dis=cont_end,
                             meth="81", cls="1", diag=diag, proc="", opdate=None, age=int(row.age), sex=row.sex_code,
                             dest="19", district=row.district, kind="transfer"))
        for kind, t in row.emerg:
            if kind == "comp":
                a = cont_end + D(days=int(t))
                if p["kind"] == "NHS":
                    pv = row.prov if rs.random() < 0.85 else [k for k in NHS_KEYS if k != row.prov][int(rs.integers(0, 2))]
                else:
                    pv = LOCAL_TRUST[row.prov]
                dg = COMP_DIAG[int(rs.choice(len(COMP_DIAG), p=[q for _, q in COMP_DIAG]))][0]
                pr = REVISION[int(rs.integers(0, 2))] if (dg in ("T814", "T810", "M541", "M511", "G970") and rs.random() < 0.45) else ""
                m = ["21", "22", "28"][int(rs.choice(3, p=[0.75, 0.10, 0.15]))]
                rows.append(dict(pid=row.pid, pseudo=row.pseudo, prov=pv, adm=a, dis=a + D(days=int(rs.integers(1, 13))),
                                 meth=m, cls="1", diag=dg, proc=pr, opdate=a + D(days=int(rs.integers(0, 2))) if pr else None,
                                 age=int(row.age + (a - row.op_date).days / 365.25), sex=row.sex_code, dest="19",
                                 district=row.district, kind="comp"))
            else:
                a = max(row.op_date + D(days=int(t)), cont_end + D(days=1))
                pv = (row.prov if p["kind"] == "NHS" else LOCAL_TRUST[row.prov]) if rs.random() < 0.8 else 40099
                rows.append(dict(pid=row.pid, pseudo=row.pseudo, prov=pv, adm=a, dis=a + D(days=int(rs.integers(0, 10))),
                                 meth="21", cls="1", diag=OTHER_EM_DIAG[int(rs.integers(0, len(OTHER_EM_DIAG)))], proc="",
                                 opdate=None, age=int(row.age + t / 365.25), sex=row.sex_code, dest="19",
                                 district=row.district, kind="other"))
        if row.inj:
            a = row.op_date + D(days=int(rs.integers(60, 331)))
            pv = provider_at(row.prov, a) if p["kind"] == "IS" else row.prov
            rows.append(dict(pid=row.pid, pseudo=row.pseudo, prov=pv, adm=a, dis=a, meth="11", cls="2",
                             diag="M544" if rs.random() < 0.5 else "M545", proc=INJECTION[int(rs.integers(0, 2))],
                             opdate=a, age=int(row.age + (a - row.op_date).days / 365.25), sex=row.sex_code, dest="19",
                             district=row.district, kind="injection"))
        # unrelated planned day cases anywhere in the extract window
        span = (EXTRACT_TO - EXTRACT_FROM).days
        n_el = int(rs.poisson(0.085 * span / 365.25))
        busy = [(x["adm"], x["dis"]) for x in rows if x["pid"] == row.pid]
        for _ in range(n_el):
            a = EXTRACT_FROM + D(days=int(rs.integers(0, span)))
            pr, dg = UNRELATED_EL[int(rs.integers(0, len(UNRELATED_EL)))]
            pool = [40117, 40152, 40188, 40099, 41206, 41309, 41388]
            pv = provider_at(pool[int(rs.integers(0, len(pool)))], a)
            day = rs.random() < 0.85
            if any(b0 - D(days=2) <= a <= b1 + D(days=2) for b0, b1 in busy):
                continue
            busy.append((a, a + D(days=3)))
            rows.append(dict(pid=row.pid, pseudo=row.pseudo, prov=pv, adm=a, dis=a if day else a + D(days=int(rs.integers(1, 4))),
                             meth="11", cls="2" if day else "1", diag=dg, proc=pr, opdate=a,
                             age=int(row.age + (a - row.op_date).days / 365.25), sex=row.sex_code, dest="19",
                             district=row.district, kind="elective"))
    s = pd.DataFrame(rows)
    s = s[(s.adm >= EXTRACT_FROM) & (s.adm <= EXTRACT_TO)].copy()
    s.loc[s.dis > EXTRACT_TO, "dis"] = None      # still in hospital at the extract cut: not yet submitted
    s = s.sort_values(["pid", "adm", "kind"]).reset_index(drop=True)
    # submission dates and re-submissions under a new spell number
    r = stream(9300)
    s["spell_id"] = ukeys(r, len(s), "%010d", 1_000_000_000, 9_999_999_999)
    sub = []
    for i, row in enumerate(s.itertuples()):
        base = row.dis if row.dis is not None else row.adm
        sub.append(base + D(days=int(r.integers(3, 41))))
    s["submitted"] = sub
    s["version"] = 1
    extra = []
    for i, row in enumerate(s.itertuples()):
        pr_ = 0.022 if row.kind == "index" else 0.01
        if r.random() < pr_:
            d = row._asdict()
            d.pop("Index")
            d["submitted"] = row.submitted + D(days=int(r.integers(20, 81)))
            d["version"] = 2
            if row.kind == "index" and row.proc == "V254" and r.random() < 0.3:
                d["proc"] = "V253"
            if row.dis is not None and r.random() < 0.2:
                d["dis"] = row.dis + D(days=1)
            extra.append(d)
    e = pd.DataFrame(extra)
    e["spell_id"] = ukeys(r, len(e), "%010d", 1_000_000_000, 9_999_999_999)
    clash = set(e.spell_id) & set(s.spell_id)
    assert not clash
    s = pd.concat([s, e], ignore_index=True)
    # only what reached the warehouse by the cut: finished spells submitted on or before 30 September 2026
    s = s[s.dis.notna() & (s.submitted <= EXTRACT_TO)].reset_index(drop=True)
    return s


def make_proms(w):
    """Registrations, questionnaires and the supplier-to-board link."""
    rows, regs = [], []
    r = stream(9400)
    old_refs = ukeys(r, len(w), "P%07d", 1_000_000, 9_999_999)
    new_refs = ukeys(r, len(w), "N%08d", 10_000_000, 99_999_999)
    for i, row in enumerate(w.itertuples()):
        new = row.platform == "new"
        ref = new_refs[i] if new else old_refs[i]
        site = {p["key"]: p["site"] for p in PROVIDERS}[row.prov]
        sup_op = row.booked if new else row.op_date
        unlinked = bool(new and row.booked == row.op_date and row.unl_u < UNLINKED[row.prov])
        regs.append(dict(ref=ref, pseudo="" if unlinked else row.pseudo, site=site, pid=row.pid, new=new,
                         linked_on=row.reg + D(days=3)))
        if row.pre_done and not row.not_invited and row.pre_c <= EXTRACT_TO:
            rows.append(dict(ref=ref, site=site, sup_op=sup_op, qtype="pre", completed=row.pre_c, yob=row.yob,
                             sex=row.sex_code, ans=row.pre_ans, tot=row.pre_tot, n=row.n_pre,
                             smoker=row.smoker, prev=row.prev, dur=row.dur, pid=row.pid))
        if row.resp_12m and not row.died_12m and row.m12_c <= EXTRACT_TO:
            rows.append(dict(ref=ref, site=site, sup_op=sup_op, qtype="m12", completed=row.m12_c, yob=row.yob,
                             sex=row.sex_code, ans=row.post_ans, tot=row.post_tot, n=row.n_m12,
                             smoker=None, prev=None, dur=None, pid=row.pid))
    # bookings that never reached theatre, and 2026-27 bookings, carry questionnaires with no operation
    rg = stream(9401)
    ghost_refs_o = ukeys(rg, 4000, "P%07d", 1_000_000, 9_999_999)
    ghost_refs_n = ukeys(rg, 4000, "N%08d", 10_000_000, 99_999_999)
    used = set(old_refs) | set(new_refs)
    ghost_refs_o = [g for g in ghost_refs_o if g not in used]
    ghost_refs_n = [g for g in ghost_refs_n if g not in used]
    gi = go = 0
    for p in PROVIDERS:
        for fy, (a, b) in list(FY.items()) + [("2026-27", (dt.date(2026, 4, 1), dt.date(2026, 9, 30)))]:
            n = int(round((0.03 if fy != "2026-27" else 0.55) * p["vol"][-1] * (1 if fy != "2026-27" else 1.15)))
            for _ in range(n):
                booked = a + D(days=int(rg.integers(0, (b - a).days + 1)))
                reg = booked - D(days=int(rg.integers(14, 71)))
                new = reg >= NEW_PLATFORM
                if new:
                    ref = ghost_refs_n[gi]; gi += 1
                else:
                    ref = ghost_refs_o[go]; go += 1
                pseudo = hexid(rg, 10)
                unlinked = bool(new and rg.random() < UNLINKED[p["key"]])
                regs.append(dict(ref=ref, pseudo="" if unlinked else pseudo, site=p["site"], pid=-1, new=new,
                                 linked_on=reg + D(days=3), gpseudo=pseudo))
                age = float(np.clip(rg.normal(56, 13.5), 19, 91))
                yob = booked.year - int(age) - int(rg.integers(0, 2))
                pre = float(np.clip(rg.normal(45, 13.5), 8, 90))
                secs = odi_sections(pre, rg)
                ans, tot, sc = odi_from(secs, n_sections(rg), rg)
                c = min(reg + D(days=int(rg.integers(0, 10))), booked)
                if c <= EXTRACT_TO and rg.random() < 0.85:
                    rows.append(dict(ref=ref, site=p["site"], sup_op=booked, qtype="pre", completed=c, yob=yob,
                                     sex=1 + int(rg.random() < 0.53), ans=ans, tot=tot, n=sum(v is not None for v in ans),
                                     smoker=bool(rg.random() < 0.18), prev=bool(rg.random() < 0.1),
                                     dur=int(rg.integers(1, 5)), pid=-1))
    q = pd.DataFrame(rows)
    reg = pd.DataFrame(regs)
    reg = settle_unlinked(w, q, reg)
    return q, reg


def match_candidates(ops, site_prov, booked, yob, sex, lo=-30, hi=120):
    """Operations a questionnaire with no NHS number could belong to: same provider, same sex, a birth year the
    age on admission allows, the operation within the given days of the booked date, nearest first."""
    c = ops[(ops.mprov == site_prov) & (ops.sex_code == sex) & (ops.yob_lo <= yob) & (ops.yob_hi >= yob)]
    dd = (c.op_date - booked).apply(lambda x: x.days)
    c = c[(dd >= lo) & (dd <= hi)].copy()
    c["gap"] = (c.op_date - booked).apply(lambda x: abs(x.days))
    return c.sort_values(["gap", "pid"])


def settle_unlinked(w, q, reg):
    site_key = {p["site"]: p["key"] for p in PROVIDERS}
    ops = w[["pid", "prov", "op_date", "sex_code", "age", "adm_off"]].copy()
    ops["mprov"] = ops.prov
    adm = [o - D(days=int(a)) for o, a in zip(ops.op_date, ops.adm_off)]
    ops["yob_lo"] = [a.year - int(g) - 1 for a, g in zip(adm, ops.age)]
    ops["yob_hi"] = [a.year - int(g) for a, g in zip(adm, ops.age)]
    linked_pids = set(reg[(reg.pseudo != "") & (reg.pid >= 0)].pid)
    free = ops[~ops.pid.isin(linked_pids)]
    pre = q[q.qtype == "pre"].set_index("ref")
    flip = set()
    for r in reg[reg.pseudo == ""].itertuples():
        if r.ref not in pre.index:
            continue                       # no questionnaire: nothing to place
        qq = pre.loc[r.ref]
        c = match_candidates(ops, site_key[r.site], qq.sup_op, qq.yob, qq.sex, lo=-120, hi=120)
        if r.pid < 0:
            ok = len(c) == 0
        else:
            ok = (len(c) >= 1 and int(c.iloc[0].pid) == r.pid and c.iloc[0].gap == 0
                  and (len(c) == 1 or c.iloc[1].gap > 3))
        if not ok:
            flip.add(r.ref)
    pseudo_of = dict(zip(w.pid, w.pseudo))
    gh = stream(9402)
    newp = []
    for r in reg.itertuples():
        if r.ref in flip:
            newp.append(pseudo_of[r.pid] if r.pid >= 0 else hexid(gh, 10))
        else:
            newp.append(r.pseudo)
    reg["pseudo"] = newp
    return reg


def make_deaths(w):
    r = stream(9500)
    out = []
    causes = ["I219", "C349", "J449", "I64X", "C509", "F03X", "J189", "I500", "C189", "G309"]
    for row in w.itertuples():
        if row.died_12m:
            d = row.op_date + D(days=int(r.integers(5, 361)))
        else:
            start = row.op_date + D(days=380)
            span = (EXTRACT_TO - start).days
            hz = 0.009 + 0.0009 * max(0, row.age - 60)
            d = None
            if span > 0 and r.random() < hz * span / 365.25:
                d = start + D(days=int(r.integers(0, span)))
        if d is not None and d <= EXTRACT_TO:
            out.append(dict(pseudo=row.pseudo, dod=d, cause=causes[int(r.integers(0, len(causes)))]))
    return pd.DataFrame(out)


def build_all():
    w = build_world()
    w = extras(w)
    spells = make_spells(w)
    q, reg = make_proms(w)
    deaths = make_deaths(w)
    from waits import make_waits
    waits = make_waits()
    return dict(ops=w, spells=spells, q=q, reg=reg, deaths=deaths, **waits)


if __name__ == "__main__":
    import time
    t = time.time()
    A = build_all()
    print({k: len(v) for k, v in A.items() if hasattr(v, "__len__")}, round(time.time() - t, 1), "s")
