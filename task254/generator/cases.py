"""Assemble individual case safety reports from the course-level truth: versions, coding, people,
laboratory samples, registry (study) cases, background reactions and duplicate reports."""
import datetime as dt
import math

import numpy as np

import core as C
import shapes as S
import world as W

TD = dt.timedelta
LOCK, EXPORT = W.LOCK, W.EXPORT
Seq = C.Seq
Rng = C.Rng
frac = C.frac

BG_PTS = [
    ("Drug ineffective", 0.10, 100, 0.7), ("Headache", 0.09, 10, 1.2), ("Nausea", 0.08, 6, 1.2),
    ("Acne", 0.07, 45, 0.8), ("Upper respiratory tract infection", 0.06, 60, 1.0), ("Nasopharyngitis", 0.06, 70, 1.0),
    ("Diarrhoea", 0.05, 10, 1.3), ("Fatigue", 0.04, 20, 1.3), ("Blood creatine phosphokinase increased", 0.04, 35, 0.9),
    ("Sinusitis", 0.03, 90, 0.9), ("Oral herpes", 0.03, 90, 1.0), ("Hypercholesterolaemia", 0.03, 60, 0.7),
    ("Weight increased", 0.03, 120, 0.7), ("Rash", 0.03, 20, 1.1), ("Arthralgia", 0.03, 60, 1.0),
    ("Off label use", 0.03, 1, 0.01), ("Pruritus", 0.02, 25, 1.1), ("Abdominal pain upper", 0.02, 15, 1.2),
    ("Dizziness", 0.02, 12, 1.2), ("Alopecia", 0.02, 90, 0.8), ("Anaemia", 0.02, 60, 0.9), ("Lymphopenia", 0.02, 50, 0.9),
    ("Product dose omission issue", 0.02, 40, 1.0), ("Cough", 0.02, 40, 1.0), ("Influenza like illness", 0.02, 80, 1.0),
    ("Pyrexia", 0.02, 30, 1.2), ("Hypertension", 0.02, 90, 0.9), ("Folliculitis", 0.01, 60, 1.0),
    ("Urticaria", 0.01, 15, 1.2), ("Insomnia", 0.01, 20, 1.2),
]
POTENTIAL = [
    ("Myocardial infarction", "mace", 0.25), ("Acute myocardial infarction", "mace", 0.10), ("Ischaemic stroke", "mace", 0.20),
    ("Cerebrovascular accident", "mace", 0.10), ("Breast cancer", "malig", 0.08), ("Lung adenocarcinoma", "malig", 0.05),
    ("Prostate cancer", "malig", 0.04), ("Lymphoma", "malig", 0.03), ("Colorectal cancer", "malig", 0.03),
    ("Basal cell carcinoma", "nmsc", 0.05), ("Squamous cell carcinoma of skin", "nmsc", 0.03),
    ("Pulmonary tuberculosis", "tb", 0.02), ("Latent tuberculosis", "tb", 0.02),
]
POT_ONSET = {"mace": (300, 0.8), "malig": (350, 0.7), "nmsc": (300, 0.7), "tb": (200, 0.6)}
REGISTRY = {"DE": 0.60, "NL": 0.15, "DK": 0.10, "SE": 0.10, "FI": 0.05}
REGISTRY_FROM = dt.date(2024, 12, 2)
REGISTRY_WEEKLY = 52.0


def versions_for(receipt, u):
    n_fu = 0 if u[0] < 0.42 else 1 if u[0] < 0.78 else 2 if u[0] < 0.94 else 3
    out, d = [receipt], receipt
    for j in range(n_fu):
        d = d + TD(days=6 + int(u[1 + j] * 140))
        if d > EXPORT:
            break
        out.append(d)
    return out


def demographics(case, risk, u1, u2, u3):
    case["sex"] = "F" if u1 < C.SEX_F[risk] else "M"
    if u3 < 0.06:
        case["age"] = None
    else:
        z = C.S._ninv(u2)
        case["age"] = int(min(91, max(18, round(C.AGE_MU[risk] + 12.5 * z))))


def report_source(case, sq):
    k = case["rec_kind"]
    if k == "PSP":
        case["report_type"], case["qual"] = "SO", 3
    elif k == "LI":
        case["report_type"], case["qual"] = "LI", 1
    elif k == "ST":
        case["report_type"], case["qual"] = "ST", 1
    else:
        u = sq()
        psp_market = case["market"] in C.PSP_MARKETS
        if psp_market and u < 0.22:
            case["report_type"], case["qual"] = "SO", 3 if sq() < 0.7 else 5
        else:
            case["report_type"] = "SP"
            case["qual"] = C.pick([(1, 0.47), (2, 0.06), (3, 0.14), (5, 0.33)], sq())


def risk_cases(seed_cases):
    """Risk reaction-courses in the database at the extraction run, as cases."""
    out = []
    for r in W.RISKS:
        recs, dist = C.build_risk(r)
        C.report_and_delay(recs, r)
        P = C.RISK_PARAMS[r]
        sv = Rng(21, P["salt"])
        sdem = Rng(22, P["salt"])
        ssrc = Rng(23, P["salt"])
        for rec in recs:
            if rec["receipt"] > EXPORT:
                continue
            vers = versions_for(rec["receipt"], [sv() for _ in range(4)])
            rec["info_until"] = vers[-1]
            case = dict(kind="risk", risk=r, rec=rec, market=rec["market"], versions=vers,
                        rec_kind=rec["kind"])
            demographics(case, r, sdem(), sdem(), sdem())
            report_source(case, ssrc)
            out.append(case)
        C.structure([c["rec"] for c in out if c["risk"] == r], r)
    return out


def registry_starts():
    """Start dates of patients enrolled in the post-authorisation safety registry."""
    out, cum, prev, k = [], 0.0, 0, 0
    for w in W.weeks():
        if w < REGISTRY_FROM:
            continue
        kweeks = (w - REGISTRY_FROM).days // 7
        tot = REGISTRY_WEEKLY * min(1.0, (kweeks + 1) / 26.0)
        for c, sh in REGISTRY.items():
            cum += tot * sh
            n = int(round(cum)) - prev
            prev += n
            for _ in range(n):
                off = int(7 * frac((k + 0.5) * W.SQ2 + 0.37))
                k += 1
                out.append((w + TD(days=off), c))
    return out


def study_cases():
    """Reactions reported from the registry (report type ST), for every risk and for background terms."""
    starts = registry_starts()
    out = []
    for j, r in enumerate(W.RISKS):
        P = C.RISK_PARAMS[r]
        dist = S.Dist(P["months"], P["maxd"])
        su, sd, sdem, sv, sk = (Seq(W.PHI, 0.29 + j / 7), Rng(31, j), Rng(32, j), Rng(33, j), Rng(34, j))
        for (s, c) in starts:
            if sk() >= P["inc"] * 1.15:
                continue
            x = dist.q(su())
            rec = dict(risk=r, market=c, start=s, T=(LOCK - s).days + 1, x=x, partial_onset=False,
                       partial_start=False, psp_mon=False, psp_dated=False, kind="ST", study=True)
            d = C.delay_days(sd(), "GEN")
            rec["delay"] = d
            rec["onset_date"] = s + TD(days=x - 1)
            rec["receipt"] = rec["onset_date"] + TD(days=d)
            rec["at_lock"] = rec["receipt"] <= LOCK
            rec["post_lock"] = LOCK < rec["receipt"] <= EXPORT
            if rec["receipt"] > EXPORT:
                continue
            vers = versions_for(rec["receipt"], [sv() for _ in range(4)])
            rec["info_until"] = vers[-1]
            case = dict(kind="study", risk=r, rec=rec, market=c, versions=vers, rec_kind="ST")
            demographics(case, r, sdem(), sdem(), sdem())
            report_source(case, sdem)
            out.append(case)
        C.structure([cc["rec"] for cc in out if cc["risk"] == r], r)
    # registry patients' other reactions
    mix = [(pt, w) for pt, w, _, _ in BG_PTS]
    par = {pt: (m, sd) for pt, _, m, sd in BG_PTS}
    sx, sp, sd, sdem, sv, sk = (Seq(W.PHI, 0.93), Rng(41), Rng(42), Rng(43), Rng(44), Rng(45))
    for (s, c) in starts:
        if sk() >= 0.128:
            continue
        pt = C.pick(mix, sp())
        m, sdv = par[pt]
        x = 1 if pt == "Off label use" else S.lognormal_days(sx(), m, sdv, lo=1, hi=1300)
        onset = s + TD(days=x - 1)
        rec = dict(risk=None, market=c, start=s, T=(LOCK - s).days + 1, x=x, partial_onset=False, partial_start=False,
                   psp_mon=False, psp_dated=False, onset_date=onset, receipt=onset + TD(days=C.delay_days(sd(), "GEN")),
                   kind="ST", study=True, main_pt=pt, concern=None, action="DOSE NOT CHANGED",
                   lines=[dict(start=s, stop=None, dose=15, end="ONGOING")])
        if rec["receipt"] > EXPORT:
            continue
        rec["at_lock"] = rec["receipt"] <= LOCK
        rec["post_lock"] = LOCK < rec["receipt"] <= EXPORT
        vers = versions_for(rec["receipt"], [sv() for _ in range(4)])
        rec["info_until"] = vers[-1]
        case = dict(kind="study", risk=None, rec=rec, market=c, versions=vers, rec_kind="ST")
        demographics(case, None, sdem(), sdem(), sdem())
        report_source(case, sdem)
        out.append(case)
    return out


def background_cases():
    """Reactions that map to no identified risk (and the important potential risks), on single courses."""
    out = []
    mix = [(pt, w) for pt, w, _, _ in BG_PTS]
    par = {pt: (m, sd) for pt, _, m, sd in BG_PTS}
    sx, sp, sd, sdem, sv, sk, sq2 = (Seq(W.PHI, 0.09), Rng(51), Rng(52), Rng(53), Rng(54), Rng(55), Rng(56))
    alloc_bg = C.allocate(0.128, 0.05)
    alloc_pot = C.allocate(0.0045, 0.15)
    for kind, alloc in (("bg", alloc_bg), ("pot", alloc_pot)):
        for (s, c) in alloc:
            T = (LOCK - s).days + 1
            if kind == "bg":
                pt = C.pick(mix, sp())
                m, sdv = par[pt]
                concern = None
            else:
                pt = C.pick([(p, w) for p, _, w in POTENTIAL], sp())
                concern = [k for p, k, _ in POTENTIAL if p == pt][0]
                m, sdv = POT_ONSET[concern]
            x = 1 if pt == "Off label use" else S.lognormal_days(sx(), m, sdv, lo=1, hi=1300)
            d = C.delay_days(sd(), "LI" if sq2() < 0.025 else "GEN")
            onset = s + TD(days=x - 1)
            rec = dict(risk=None, market=c, start=s, T=T, x=x, partial_onset=sq2() < 0.07 and x > 31,
                       partial_start=sq2() < 0.02, psp_mon=False, psp_dated=False, onset_date=onset,
                       receipt=onset + TD(days=d), kind="GEN", main_pt=pt, concern=concern)
            if rec["receipt"] > EXPORT:
                continue
            rec["at_lock"] = rec["receipt"] <= LOCK
            rec["post_lock"] = LOCK < rec["receipt"] <= EXPORT
            vers = versions_for(rec["receipt"], [sv() for _ in range(4)])
            rec["info_until"] = vers[-1]
            u = sk()
            act = ("WITHDRAWN" if pt == "Drug ineffective" and u < 0.6 else
                   C.pick([("DOSE NOT CHANGED", 0.55), ("UNKNOWN", 0.30), ("NOT APPLICABLE", 0.05), ("WITHDRAWN", 0.10)], u))
            rec["action"] = act
            lines = []
            if act == "WITHDRAWN":
                stop = max(onset, min(onset + TD(days=int(sk() * 20)), rec["receipt"]))
                lines.append(dict(start=s, stop=stop, dose=15, end="DISCONTINUED"))
            else:
                lines.append(dict(start=s, stop=None, dose=15, end="ONGOING" if act != "UNKNOWN" else "UNKNOWN"))
            rec["lines"] = lines
            case = dict(kind="bg", risk=None, rec=rec, market=c, versions=vers, rec_kind="GEN")
            demographics(case, None, sdem(), sdem(), sdem())
            report_source(case, sdem)
            if rec["kind"] == "GEN" and d >= 40 and sq2() < 0.03:
                case["report_type"], case["qual"] = "LI", 1
            out.append(case)
    return out


# ---------------------------------------------------------------- coding and version states

OUTCOMES = [("RECOVERED", 0.55), ("RECOVERING", 0.15), ("NOT RECOVERED", 0.12), ("RECOVERED WITH SEQUELAE", 0.03),
            ("UNKNOWN", 0.15)]


def code_case(case, sq):
    rec = case["rec"]
    r = case["risk"]
    u = [sq() for _ in range(12)]
    rx = []
    onset = rec["onset_date"]
    lab = bool(rec.get("psp_dated"))
    nv = len(case["versions"])
    if r is not None:
        main = C.pick(C.LAB_TERMS[r] if lab else C.TERMS[r], u[0])
        rx.append(dict(pt=main, risk=r, date=None if lab else onset, added=0))
        second = None
        if r == "ild" and u[1] < 0.07:
            second = C.pick([(t, w) for t, w in C.TERMS["ild"] if t != main], u[2])
        elif r == "zoster" and main == "Herpes zoster" and u[1] < 0.09:
            second = C.pick([(t, 1.0 / 3) for t, _ in C.V4_ADDED["zoster"]], u[2])
        elif r == "infection" and main in ("Urinary tract infection", "Pneumonia") and u[1] < 0.15:
            second = [a for a, b in C.V4_ADDED["infection"] if b == main][0]
        elif r == "infection" and main == "Pneumonia" and u[1] < 0.23:
            second = "Sepsis"
        elif r == "vte" and main == "Deep vein thrombosis" and u[1] < 0.12:
            second = "Pulmonary embolism"
        elif r == "hepatic" and u[1] < 0.12:
            second = "Aspartate aminotransferase increased"
        if second:
            rx.append(dict(pt=second, risk=r, date=None if lab else onset, added=0, multi=True))
        for t, w in C.CO_TERMS[r]:
            if t == "Aspartate aminotransferase increased":
                continue
            if sq() < w:
                added = 1 if (nv > 1 and sq() < 0.3) else 0
                d = None if lab else onset
                if t == "Post herpetic neuralgia" and not lab:
                    room = (case["versions"][-1] - onset).days
                    if room < 25:
                        continue
                    d = onset + TD(days=20 + int(sq() * min(60, room - 20)))
                    added = len(case["versions"]) - 1 if d > case["versions"][0] else added
                rx.append(dict(pt=t, risk=None, date=d, added=added))
    else:
        rx.append(dict(pt=rec["main_pt"], risk=None, date=onset, added=0, concern=rec.get("concern")))
        if u[3] < 0.35:
            other = C.pick([(pt, w) for pt, w, _, _ in BG_PTS if pt != rec["main_pt"]], u[4])
            d2 = min(onset + TD(days=int(u[5] * 10)), rec["receipt"])
            rx.append(dict(pt=other, risk=None, date=d2, added=1 if (nv > 1 and u[6] < 0.3) else 0))
    case["rx"] = rx
    # seriousness, outcome and fate
    ser, crit, p_fatal = C.seriousness(r if r else ("pot" if rec.get("concern") else None), u[7], u[8])
    if r is None and rec.get("concern"):
        ser, crit = "Y", ("OMI" if rec["concern"] in ("malig", "nmsc", "tb") else "H")
    case["serious"], case["criteria"] = ser, crit
    case["ser_upgrade"] = (ser == "Y" and r in ("zoster", "hepatic", "neutropenia") and nv > 1 and u[9] < 0.15)
    fatal = u[10] < p_fatal
    final = "FATAL" if fatal else C.pick(OUTCOMES, u[11])
    case["final_outcome"] = final
    case["outcome_date"] = (onset + TD(days=7 + int(sq() * 110))) if final in ("RECOVERED", "FATAL", "RECOVERED WITH SEQUELAE") else None
    if fatal:
        case["criteria"] = "D" if "D" not in crit else crit
    # partial onset strings: partial at the lock, or partial at receipt and completed before the lock
    case["onset_partial"] = bool(rec.get("partial_onset"))
    case["complete_from"] = None
    if (not case["onset_partial"]) and not lab and r != "ild" and nv > 1 and case["versions"][1] <= LOCK and sq() < 0.05 \
            and (onset.year, onset.month) != (rec["start"].year, rec["start"].month):
        case["complete_from"] = 1
    case["start_partial"] = bool(rec.get("partial_start"))


def onset_string(case, rxi, vi):
    rx = case["rx"][rxi]
    d = rx["date"]
    over = case.get("onset_override", {}).get((rxi, vi))
    if over is not None:
        return over
    if d is None:
        return ""
    if case["onset_partial"] or (case["complete_from"] is not None and vi < case["complete_from"]):
        if rx.get("risk") or rxi == 0 or rx["date"] == case["rec"]["onset_date"]:
            return "%04d-%02d" % (d.year, d.month)
    return d.isoformat()


def outcome_at(case, vi):
    rcpt = case["versions"][vi]
    final = case["final_outcome"]
    od = case["outcome_date"]
    if final in ("RECOVERED", "FATAL", "RECOVERED WITH SEQUELAE"):
        if od is not None and od <= rcpt and (vi > 0 or final == "FATAL"):
            return final, od.isoformat()
        return ("NOT RECOVERED" if final == "FATAL" else "RECOVERING"), ""
    if vi == 0 and final == "NOT RECOVERED":
        return "UNKNOWN", ""
    return final, ""


# ---------------------------------------------------------------- duplicates, laboratory samples, numbering

def make_duplicate(case, sq):
    rec = case["rec"]
    u = sq()
    if case["report_type"] == "SP" and case["qual"] in (1, 3) and u < 0.55:
        rt, q, lag, reason = "SP", 5, 3 + int(sq() * 50), "Same patient and event reported by the patient after the physician's report"
    elif case["report_type"] == "SP" and case["qual"] == 5 and u < 0.85:
        rt, q, lag, reason = "SP", 1, 5 + int(sq() * 60), "Same patient and event reported by the treating physician"
    elif case["report_type"] in ("SP", "SO"):
        rt, q, lag, reason = "LI", 1, 70 + int(sq() * 230), "Published case report of a case already received"
    else:
        rt, q, lag, reason = "SP", 1, 10 + int(sq() * 40), "Same patient and event reported by the treating physician"
    receipt = case["versions"][0] + TD(days=lag)
    if receipt > EXPORT:
        return None
    dup = dict(kind="dup", risk=case["risk"], rec=rec, market=case["market"], versions=[receipt],
               rec_kind=rt, report_type=rt, qual=q, sex=case["sex"], age=case["age"] if sq() < 0.8 else None,
               master=case, link_reason=reason)
    dup["rx"] = [dict(rx, added=0) for rx in case["rx"] if rx["added"] == 0]
    for k in ("serious", "criteria", "final_outcome", "outcome_date", "onset_partial", "start_partial"):
        dup[k] = case[k]
    dup["complete_from"] = None
    dup["ser_upgrade"] = False
    if case["complete_from"] is not None:
        dup["onset_partial"] = False
    dup["linked_on"] = min(EXPORT, max(receipt, case["versions"][0]) + TD(days=1 + int(sq() * 25)))
    return dup


def course_end_day(rec):
    on = rec["onset_date"]
    for ln in rec["lines"]:
        if ln["start"] <= on and (ln["stop"] is None or ln["stop"] >= on):
            if ln["stop"] is None:
                return None
            return (ln["stop"] - rec["start"]).days + 1
    return None


def lab_samples(case, sq, lab):
    """PSP laboratory results transferred for a linked case: ALT and neutrophils at every sample, other
    analytes at some, inside the transfer window around the case."""
    rec = case["rec"]
    rec["course_end_day"] = course_end_day(rec)
    days, grade1 = C.psp_schedule(rec, sq)
    lo = rec["x"] - 120
    hi = (case["versions"][0] - rec["start"]).days + 1 + 60
    rows = []
    sex = case["sex"]
    r = case["risk"]
    lab_dated = rec.get("psp_dated")
    for d in days:
        if d < max(1, lo) or d > hi:
            continue
        date = rec["start"] + TD(days=d - 1)
        if date > EXPORT:
            continue
        alt = 0.35 + sq() * 0.6
        neut = 2.1 + sq() * 3.9
        if r == "hepatic" and lab_dated:
            if d == rec["x"]:
                alt = 3.3 + sq() * 4.2
            elif d in grade1:
                alt = 1.2 + sq() * 1.6
            elif d > rec["x"]:
                alt = 1.1 + sq() * 1.6
        elif r == "hepatic" and d > rec["x"]:
            alt = 0.5 + sq() * 1.7
        if r == "neutropenia" and lab_dated:
            if d == rec["x"]:
                neut = 0.45 + sq() * 0.52
            elif d in grade1:
                neut = 1.08 + sq() * 0.37
            elif d > rec["x"]:
                neut = 0.9 + sq() * 0.9
        elif r == "neutropenia" and d > rec["x"]:
            neut = 1.15 + sq() * 1.5
        rows.append((date, "ALT", C._fmt_alt(alt, lab, sex), C.LABS[lab][3], lab))
        rows.append((date, "NEUT", C._fmt_neut(neut, lab), C.LABS[lab][6], lab))
        if sq() < 0.35:
            ly = 0.9 + sq() * 1.8
            rows.append((date, "LYMPH", C._fmt_neut(ly, lab), C.LABS[lab][6], lab))
    return rows


def number_cases(cases):
    order = sorted(range(len(cases)), key=lambda i: (cases[i]["versions"][0], W.MARKET_ORDER.index(cases[i]["market"]), i))
    seq = {}
    for i in order:
        y = cases[i]["versions"][0].year
        seq[y] = seq.get(y, 0) + 1
        cases[i]["case_no"] = "%dRAV%05d" % (y, seq[y])


def assemble():
    rc = risk_cases(None)
    sc = study_cases()
    bg = background_cases()
    cases = rc + sc + bg
    sq = Rng(61)
    for case in cases:
        code_case(case, sq)
    return cases


# ---------------------------------------------------------------- the follow-ups received after the lock

BATCH_DAY = dt.date(2026, 10, 2)   # PSP vendor's quarterly reconciliation, processed the second day after the lock


def _golden(cases, r):
    g = [c for c in cases if c["kind"] == "risk" and c["risk"] == r and c["rec"]["at_lock"]
         and not c["rec"]["partial_onset"] and not c["rec"]["partial_start"]]
    return g


def _post_version(case, day):
    """Index of a version received after the lock, appended if the case has none."""
    for vi, v in enumerate(case["versions"]):
        if v > LOCK:
            return len(case["versions"]) - 1
    case["versions"].append(day)
    return len(case["versions"]) - 1


def _lb_F(xs, Ts, t):
    import estimators as E
    s, F = E.reverse_km(np.array(xs, float), np.array(Ts, float))
    return E.cdf_at(s, F, t)


def apply_h1(cases):
    """Post-lock follow-ups that correct the onset of reactions of the five other risks (the PSP vendor's
    reconciliation batch dates laboratory-only reactions too): enough of them cross the lower edge of each
    answer month that the latest delivered version files every cell a month short, and others move both ways
    by 3 to 40 days, away from every month edge."""
    g = C.Rng(81)
    for r in W.RISKS:
        if r == "ild":
            continue
        gold = _golden(cases, r)
        xs = {id(c): c["rec"]["x"] for c in gold}
        Ts = {id(c): c["rec"]["T"] for c in gold}
        moved = set()
        tm = C.TARGET_MONTHS[r]
        for p, m in ((0.95, tm[1]), (0.80, tm[0])):
            edge = 30 * (m - 1)
            # laboratory-only reactions are reconciled too: the nurse's follow-up gives the date symptoms began
            cands = [c for c in gold if id(c) not in moved
                     and edge + 1 <= c["rec"]["x"] <= edge + 30 and c["rec"]["T"] >= c["rec"]["x"] + 30]
            cands.sort(key=lambda c: (c["rec"]["x"], c["versions"][0]))
            order = sorted(range(len(cands)), key=lambda i: C.frac((i + 0.5) * W.PHI))
            k = 0
            while _lb_F(list(xs.values()), list(Ts.values()), edge) < p + 0.004:
                if k >= len(order):
                    raise SystemExit("H1: not enough onsets to move %s %s" % (r, p))
                c = cands[order[k]]
                k += 1
                x0 = c["rec"]["x"]
                new = edge - int(g() * 10)
                delta = x0 - new
                if delta < 3 or delta > 40:
                    continue
                xs[id(c)] = new
                moved.add(id(c))
                c["h1"] = (x0, new)
        # background corrections in both directions, away from every edge
        edges = [30 * (m - 1) for m in C.TARGET_MONTHS[r]] + [30 * m for m in C.TARGET_MONTHS[r]]
        pool = [c for c in gold if not c["rec"].get("psp_dated") and id(c) not in moved]
        for c in pool:
            if g() >= 0.012:
                continue
            x0 = c["rec"]["x"]
            d = (3 + int(g() * 38)) * (1 if g() < 0.5 else -1)
            new = x0 + d
            if new < 1 or new > c["rec"]["T"] - 20 or any(min(x0, new) <= e < max(x0, new) for e in edges) \
                    or any(abs(new - e) < 8 or abs(x0 - e) < 8 for e in edges):
                continue
            c["h1"] = (x0, new)
    for c in cases:
        if "h1" not in c:
            continue
        x0, new = c["h1"]
        day = BATCH_DAY if c["report_type"] == "SO" else LOCK + TD(days=1 + int(g() * 5))
        vi = _post_version(c, day)
        nd = c["rec"]["start"] + TD(days=new - 1)
        ov = c.setdefault("onset_override", {})
        for i, rx in enumerate(c["rx"]):
            if rx.get("risk") == c["risk"] or (rx["date"] is not None and rx["date"] == c["rec"]["onset_date"]):
                ov[(i, vi)] = nd.isoformat()


ADDED_TERM = {"zoster": "Herpes zoster", "infection": "Pneumonia", "vte": "Deep vein thrombosis",
              "hepatic": "Drug-induced liver injury", "neutropenia": "Neutropenia"}


def apply_added_reactions(cases, per_risk=10):
    """Post-lock follow-ups that add a reaction of another risk to a case received in the interval."""
    g = C.Rng(82)
    bg = [c for c in cases if c["kind"] == "bg" and c["rec"]["at_lock"] and c["versions"][0] >= W.INTERVAL_START
          and not c["rec"]["partial_onset"] and c["rec"]["x"] <= 120 and "h1" not in c]
    used = set()
    for r in ("zoster", "infection", "vte", "hepatic", "neutropenia"):
        n = 0
        for c in bg:
            if id(c) in used or g() >= 0.02:
                continue
            used.add(id(c))
            day = BATCH_DAY if c["report_type"] == "SO" else LOCK + TD(days=1 + int(g() * 5))
            vi = _post_version(c, day)
            c["rx"].append(dict(pt=ADDED_TERM[r], risk=r, date=c["rec"]["onset_date"], added=vi, late=True))
            c["added_risk"] = r
            n += 1
            if n >= per_risk:
                break
