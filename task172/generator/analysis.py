"""The reader's side: everything the golden states, recomputed from the files in target/ alone. The checks, the
golden writer and the ceiling script call these functions; the verifier has its own."""
import csv
import datetime as dt
import json
import math
import os
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import load_workbook

import survival as S

N_TARGET, FINAL_EVENTS, INTERIM_EVENTS = 450, 330, 165
SCHEDULE_WEEKS = [6, 12, 18, 24] + list(range(32, 400, 8))
GOLDEN_BREAK = 105          # days: between the week-12 and week-18 assessments
NSIM = 20000
SOCS = ("Infections and infestations", "Hepatobiliary disorders", "Gastrointestinal disorders",
        "Blood and lymphatic system disorders")


def rd(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pdate(s):
    s = s.strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"):
        try:
            return dt.datetime.strptime(s.title() if fmt == "%d-%b-%Y" else s, fmt).date()
        except ValueError:
            pass
    raise ValueError(s)


def xl(path, sheet):
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


def todate(v):
    if v is None:
        return None
    return v.date() if isinstance(v, dt.datetime) else v


class Pack:
    def __init__(self, target):
        self.t = target
        f = lambda n: os.path.join(target, n)
        self.sites = {s["site"]: s for s in json.load(open(f("talon2_sites.json")))["sites"]}
        self.rand = rd(f("talon2_irt_randomisation_export.csv"))
        self.bicr = rd(f("talon2_bicr_timepoint_reads.csv"))
        self.deaths = xl(f("talon2_edc_subject_status.xlsx"), "Deaths")
        self.disp = xl(f("talon2_edc_subject_status.xlsx"), "Disposition")
        self.base = xl(f("talon2_edc_subject_status.xlsx"), "Baseline")
        self.screening = rd(f("talon2_screening_log.csv"))
        self.pv = xl(f("talon2_pv_sae_line_listing.xlsx"), "SAE line listing")
        self.central = rd(f("talon2_central_lab_transfer.csv"))
        self.local = rd(f("talon2_edc_local_labs.csv"))
        self.samples = rd(f("talon2_edc_central_lab_kit_log.csv"))
        self.exposure = rd(f("talon2_edc_exposure.csv"))
        self.irt = rd(f("talon2_irt_drug_administration.csv"))
        self.cut = None


# ------------------------------------------------------------------------------------------------ the main call
def rand_table(P, local=True):
    out = {}
    for r in P.rand:
        utc = dt.datetime.strptime(r["Randomisation Date/Time (UTC)"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
        tz = ZoneInfo(P.sites[r["Site"]]["time_zone"])
        d = utc.astimezone(tz).date() if local else utc.date()
        ds = 0 if r["Stratum: Disease Status"].startswith("Initially") else 1
        ps = {"Intrahepatic": 0, "Extrahepatic": 1, "Gallbladder": 2}[r["Stratum: Primary Tumour Site"].split()[0]]
        out[r["Randomisation Number"]] = dict(date=d, arm=1 if r["Treatment Arm"].startswith("Ravolimab") else 0,
                                              stratum=ds * 3 + ps, screening_no=r["Screening Number"], site=r["Site"])
    return out


def pfs_table(P, cut, local=True, strata="irt", gap_rule=True, ne_rule=True):
    R = rand_table(P, local)
    if strata == "ecrf":
        for b in P.base:
            ds = 0 if b["Disease status (eCRF)"].startswith("Initially") else 1
            ps = {"Intrahepatic": 0, "Extrahepatic": 1, "Gallbladder": 2}[b["Primary tumour site (eCRF)"].split()[0]]
            R[b["Subject"]]["stratum"] = ds * 3 + ps
    reads = {}
    for b in P.bicr:
        reads.setdefault(b["SUBJID"], []).append((int(b["TPT"].split()[1]), pdate(b["SCANDT"]), b["BICR_OVRL_RESP"]))
    death = {d["Subject"]: todate(d["Date of death"]) for d in P.deaths}
    wd = {d["Subject"]: todate(d["Date of withdrawal or loss to follow-up"]) for d in P.disp}
    rows = []
    for sid, r in R.items():
        if r["date"] > cut:
            continue
        rs = sorted(x for x in reads.get(sid, []) if x[1] <= cut)
        last = r["date"]
        run = 0
        ev = None
        for wk_, d, resp in rs:
            if resp == "NE":
                run += 1
                continue
            if resp == "PD":
                ev = ("censor", last) if (run >= 2 and gap_rule) else ("PD", d)
                break
            last, run = d, 0
        dd = death.get(sid)
        if ev is None and dd is not None and dd <= cut:
            run2 = 0
            for wk_, d, resp in rs:
                if d > last and d < dd:
                    run2 = run2 + 1 if resp == "NE" else 0
            ev = ("censor", last) if (run2 >= 2 and gap_rule) else ("Death", dd)
        if ev is None:
            ev = ("censor", last)
        withdrawn = wd.get(sid) is not None and wd[sid] <= cut
        atrisk = ev[0] == "censor" and not withdrawn and not (dd is not None and dd <= cut) and \
            not any(x[2] == "PD" for x in rs)
        rows.append(dict(sid=sid, rday=(r["date"] - cut).days, time=(ev[1] - r["date"]).days, event=ev[0] != "censor",
                         arm=r["arm"], stratum=r["stratum"], atrisk=atrisk, rdate=r["date"]))
    rows.sort(key=lambda x: x["sid"])
    a = lambda k, t=float: np.array([x[k] for x in rows], dtype=t)
    return dict(rday=a("rday"), time=a("time"), event=a("event", bool), arm=a("arm", int), stratum=a("stratum", int),
                atrisk=a("atrisk", bool), cut_rel=0.0, rows=rows)


def find_cut(P):
    """The date of the 165th BICR-confirmed event, counted the SAP's way."""
    far = dt.date(2027, 12, 31)
    d = pfs_table(P, far)
    R = rand_table(P)
    dates = sorted(R[x["sid"]]["date"] + dt.timedelta(days=int(x["time"])) for x in d["rows"] if x["event"])
    return dates[INTERIM_EVENTS - 1], (dates[INTERIM_EVENTS] if len(dates) > INTERIM_EVENTS else None)


def interim(P, cut, **kw):
    d = pfs_table(P, cut, **kw)
    z, U, V = S.logrank(d["time"], d["event"], d["arm"], d["stratum"])
    hr, se = S.cox_hr(d["time"], d["event"], d["arm"], d["stratum"])
    frac = INTERIM_EVENTS / FINAL_EVENTS
    out = dict(d=d, n=len(d["time"]), events=int(d["event"].sum()), z=z, U=U, V=V, hr=hr, se=se,
               ci=(math.exp(math.log(hr) - 1.959964 * se), math.exp(math.log(hr) + 1.959964 * se)),
               cp_trend=S.cp_bvalue(z, frac, z / math.sqrt(frac)),
               cp_design=S.cp_bvalue(z, frac, -math.log(0.70) * math.sqrt(FINAL_EVENTS / 4.0)))
    rows = S.interval_rates(d["time"], d["event"], d["arm"], [0, GOLDEN_BREAK, 1e9])
    out["hr_early"] = (rows[0][4] / rows[0][5]) / (rows[0][2] / rows[0][3])
    out["hr_late"] = (rows[1][4] / rows[1][5]) / (rows[1][2] / rows[1][3])
    out["cp_late"] = S.cp_bvalue(z, frac, -math.log(out["hr_late"]) * math.sqrt(FINAL_EVENTS / 4.0))
    out["by_visit"] = S.interval_rates(d["time"], d["event"], d["arm"], [0, 63, 105, 147, 196, 1e9])
    return out


def projection_inputs(P, cut, d):
    n = len(d["time"])
    rdates = [x["rdate"] for x in d["rows"]]
    recent = sum(1 for x in rdates if x > cut - dt.timedelta(days=91))
    rate = max(recent, 1) / 91.0
    wd = sum(1 for x in P.disp if x["Date of withdrawal or loss to follow-up"] is not None
             and todate(x["Date of withdrawal or loss to follow-up"]) <= cut)
    fu = float(np.sum(np.maximum(d["time"], 0)))
    drop = wd / fu
    mix = np.bincount(d["stratum"], minlength=6) / n
    return rate, drop, mix


def conditional_power(P, cut, kind="pw", breaks=(GOLDEN_BREAK,), nsim=NSIM, seed=20261209, drop=True,
                      stratified=True, hr=None, **kw):
    I = interim(P, cut, **kw)
    d = I["d"]
    rate, dr, mix = projection_inputs(P, cut, d)
    if kind == "ph":
        hz = S.Hazard("ph", d["time"], d["event"], d["arm"], breaks=breaks, hr=I["hr"] if hr is None else hr)
    elif kind == "weibull":
        hz = S.Hazard("weibull", d["time"], d["event"], d["arm"])
    else:
        hz = S.Hazard("pw", d["time"], d["event"], d["arm"], breaks=breaks)
    cp, zs = S.project_cp(d, hz, nsim, seed, N_TARGET, FINAL_EVENTS, rate, dr if drop else 0.0, mix, stratified=stratified)
    return cp, I


def band(cp):
    return "stop" if cp < 0.20 else ("extend" if cp < 0.80 else "continue")


# ------------------------------------------------------------------------------------------------ ask A: SAEs
def screening_links(P):
    """Re-screened patients: the earlier screen-failure attempt at the same site, sex, year of birth and initials."""
    R = rand_table(P)
    by_no = {s["Screening No"]: s for s in P.screening}
    key = lambda s: (s["Site"], s["Sex"], s["Year of Birth"], s["Initials"])
    rand_by_sno = {r["screening_no"]: sid for sid, r in R.items()}
    link = {}
    for sno, sid in rand_by_sno.items():
        k = key(by_no[sno])
        for s in P.screening:
            if s["Screening No"] != sno and key(s) == k and s["Outcome"] == "Screen failure" and \
                    pdate(s["Screening Date"]) < pdate(by_no[sno]["Screening Date"]):
                link[s["Screening No"]] = sid
    return link


def ask_sae(P, cut, rescreen=True):
    R = rand_table(P)
    sno_to = {r["screening_no"]: sid for sid, r in R.items()}
    if rescreen:
        sno_to.update(screening_links(P))
    latest = {}
    order = {}
    for x in P.pv:
        v = 0 if x["Report version"] == "Initial" else int(x["Report version"].split()[-1])
        if x["Case number"] not in latest or v > order[x["Case number"]]:
            latest[x["Case number"]], order[x["Case number"]] = x, v
    out = {(a, k): 0 for a in (0, 1) for k in ("patients", "events") + SOCS}
    pts = {0: set(), 1: set()}
    for case, x in latest.items():
        if x["Case status"] == "Nullified":
            continue
        sid = sno_to.get(x["Patient (screening number)"])
        if sid is None:
            continue
        onset = todate(x["Onset date"])
        if onset < R[sid]["date"] or onset > cut:
            continue
        a = R[sid]["arm"]
        out[(a, "events")] += 1
        pts[a].add(sid)
        if x["MedDRA system organ class"] in SOCS:
            out[(a, x["MedDRA system organ class"])] += 1
    for a in (0, 1):
        out[(a, "patients")] = len(pts[a])
    return out


# ------------------------------------------------------------------------------------------------ ask B: liver tests
def first_doses(P, irt=True):
    first = {}
    for x in P.exposure:
        d = pdate(x["Date administered"])
        first[x["Subject"]] = min(first.get(x["Subject"], d), d)
    if irt:
        for x in P.irt:
            if x["Kit Status"] == "Administered":
                d = pdate(x["Transaction Date"])
                first[x["Randomisation Number"]] = min(first.get(x["Randomisation Number"], d), d)
    return first


def ask_liver(P, cut, collection=True, irt=True):
    R = rand_table(P)
    sno_to = {r["screening_no"]: sid for sid, r in R.items()}
    sno_to.update(screening_links(P))
    first = first_doses(P, irt=irt)
    coll = {s["Kit accession number"]: pdate(s["Date sample collected"]) for s in P.samples}
    hit = {(a, t): set() for a in (0, 1) for t in ("ALT", "AST", "TBIL")}
    for x in P.central:
        if x["TEST_CODE"] not in ("ALT", "AST", "TBIL"):
            continue
        sid = sno_to.get(x["SCREENING_NO"])
        if sid is None or sid not in first:
            continue
        d = coll[x["ACCESSION"]] if collection else pdate(x["COLLECTION_DATE"])
        if d <= first[sid] or d > cut:
            continue
        mult = 3.0 if x["TEST_CODE"] == "TBIL" else 5.0
        if float(x["RESULT"]) > mult * float(x["REF_HIGH"]):
            hit[(R[sid]["arm"], x["TEST_CODE"])].add(sid)
    names = {"Alanine aminotransferase": "ALT", "Aspartate aminotransferase": "AST", "Bilirubin, total": "TBIL"}
    for x in P.local:
        sid = x["Subject"]
        if sid not in first:
            continue
        d = pdate(x["Sample date"])
        if d <= first[sid] or d > cut:
            continue
        t = names[x["Test"]]
        mult = 3.0 if t == "TBIL" else 5.0
        if float(x["Result"]) > mult * float(x["Upper limit of normal"]):
            hit[(R[sid]["arm"], t)].add(sid)
    return {k: len(v) for k, v in hit.items()}


# ------------------------------------------------------------------------------------------------ ask C: exposure
def ask_exposure(P, cut, irt=True, edc=True):
    R = rand_table(P)
    given = set()
    patients = set()
    if edc:
        for x in P.exposure:
            d = pdate(x["Date administered"])
            if d <= cut:
                patients.add(x["Subject"])
                if x["Treatment"] == "Ravolimab/placebo":
                    given.add((x["Subject"], d))
    if irt:
        for x in P.irt:
            d = pdate(x["Transaction Date"])
            if x["Kit Status"] == "Administered" and d <= cut:
                patients.add(x["Randomisation Number"])
                given.add((x["Randomisation Number"], d))
    out = {}
    for a in (0, 1):
        out[(a, "safety_population")] = sum(1 for s in patients if R[s]["arm"] == a)
        out[(a, "doses")] = sum(1 for s, d in given if R[s]["arm"] == a)
    return out
