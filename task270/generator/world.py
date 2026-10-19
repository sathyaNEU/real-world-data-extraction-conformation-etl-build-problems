"""The clean truth of the task270 world: the Memory Assessment Service's patients from each clinic's opening to
30 September 2026, their referrals, assessments, diagnoses, ACE-III sittings, reviews, discharges, transfers and
deaths, before any export is written.

A patient's cognition falls at their own steady rate from the first assessment. A sitting's total is that cognition,
the test's own error and, once the patient has completed a sitting before, the gain a patient carries from having
met the test, which comes once and stays. Nothing below writes that gain anywhere; it is only in the scores."""
import datetime as dt
import numpy as np
import common as K

SEED = 521
GAIN = 2.5          # the one-time gain from the second completed sitting on
NOISE = 2.0         # a sitting's own error, ACE-III points

# per clinic: new Alzheimer's or MCI patients a year, the Alzheimer's share among them, the mean yearly decline of
# each, the level below which the clinic discharges a patient at review, the share of stable MCI patients it
# discharges to the GP after two to three and a half years
PARAM = {
    "Thurlwick":   dict(inscope=150, ad=0.705, r_ad=6.471, r_mci=2.949, disch=28.208, mstab=0.31),
    "Penwardine":  dict(inscope=140, ad=0.687, r_ad=6.096, r_mci=2.56, disch=41.219, mstab=0.26),
    "Swinholt":    dict(inscope=130, ad=0.598, r_ad=5.547, r_mci=2.186, disch=50.0, mstab=0.40),
    "Brindlemere": dict(inscope=120, ad=0.561, r_ad=4.909, r_mci=2.404, disch=51.9, mstab=0.40),
    "Ravensfold":  dict(inscope=115, ad=0.562, r_ad=5.256, r_mci=2.474, disch=45.4, mstab=0.45),
    "Corvale":     dict(inscope=115, ad=0.532, r_ad=5.370, r_mci=2.543, disch=49.2, mstab=0.47),
    "Mosswick":    dict(inscope=110, ad=0.546, r_ad=5.293, r_mci=2.654, disch=51.8, mstab=0.31),
    "Quarndale":   dict(inscope=175, ad=0.590, r_ad=6.477, r_mci=2.814, disch=46.3, mstab=0.45, iv=1.2),
}
# referrals from the start of 2022 at four clinics: the GP practices around Thurlwick and Penwardine began screening
# their older patients' memory that year and refer earlier; Mosswick and Swinholt took referrals from the two care
# home groups that opened in their districts
D22 = dt.date(2022, 1, 1)
SHIFT = {"Thurlwick": (D22, dict(ad=0.509, r_ad=5.352, r_mci=2.535)),
         "Penwardine": (D22, dict(ad=0.485, r_ad=5.252, r_mci=2.456)),
         "Mosswick": (D22, dict(ad=0.634, r_ad=5.608)),
         "Swinholt": (D22, dict(ad=0.568, r_ad=5.617))}
SHRINK = {"Corvale": 0.62, "Mosswick": 0.60}     # their intake once Quarndale took four of their districts
INSCOPE_SHARE = 0.68
OTHER_MIX = [("VAS", 0.32), ("DLB", 0.12), ("PDD", 0.05), ("FTD", 0.05), ("UNS", 0.06), ("NOD", 0.30), ("DEP", 0.10)]
OTHER_PROFILE = {"VAS": (74, 7, 3.2), "DLB": (70, 7, 5.0), "PDD": (68, 7, 4.5), "FTD": (72, 8, 6.0),
                 "UNS": (70, 8, 4.0), "NOD": (90, 4, 0.4), "DEP": (86, 5, 0.3)}
END = K.WINDOW[1]
YEAR = 365.25
# the share of diagnoses each clinic's doctors put on the record the day they give them; the rest go on when the
# clinic letter is done
SAME_DAY_ENTRY = {"Thurlwick": 0.52, "Penwardine": 0.44, "Swinholt": 0.47, "Brindlemere": 0.40, "Ravensfold": 0.50,
                  "Corvale": 0.43, "Mosswick": 0.46, "Quarndale": 0.38}


def yrs(a, b):
    return (b - a).days / YEAR


def weekday(d, rng=None):
    """Clinics run Monday to Friday."""
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def add_days(d, n):
    return d + dt.timedelta(days=int(round(n)))


def nhs_number(rng, used):
    """Ten digits with a valid modulus 11 check digit, from a range the NHS does not issue."""
    while True:
        body = [9] + list(rng.integers(0, 10, 8))
        s = sum((10 - i) * d for i, d in enumerate(body))
        chk = 11 - (s % 11)
        if chk == 11:
            chk = 0
        if chk == 10:
            continue
        n = "".join(str(x) for x in body) + str(chk)
        if n not in used:
            used.add(n)
            return n


def split_domains(total, dx, rng, completed=True):
    """The five domain scores of a sitting with the given total (each within its maximum, summing to the total)."""
    imp = max(0.0, (100.0 - total) / 100.0)
    load = {"AD": (0.8, 1.45, 1.15, 0.65, 0.7), "MCI": (0.8, 1.5, 1.1, 0.6, 0.6)}.get(dx, (1.0, 1.1, 1.2, 0.8, 0.9))
    mx = np.array([m for _, _, m in K.DOMAINS], float)
    lost = mx * np.minimum(1.0, imp * np.array(load) * rng.uniform(0.85, 1.15, 5))
    want = 100.0 - total
    if lost.sum() > 0:
        lost = lost * want / lost.sum()
    sc = np.clip(mx - lost, 0, mx)
    fl = np.floor(sc).astype(int)
    rem = int(total) - fl.sum()
    order = np.argsort(-(sc - fl))
    i = 0
    while rem != 0 and i < 50:
        j = order[i % 5]
        if rem > 0 and fl[j] < mx[j]:
            fl[j] += 1
            rem -= 1
        elif rem < 0 and fl[j] > 0:
            fl[j] -= 1
            rem += 1
        i += 1
    return [int(x) for x in fl]


def intake_per_month(clinic, month_start):
    p = PARAM[clinic]
    rate = p["inscope"] / INSCOPE_SHARE / 12.0
    opened = K.OPENED[clinic]
    months_open = (month_start.year - opened.year) * 12 + month_start.month - opened.month
    if months_open < 12:
        rate *= 0.55 + 0.45 * months_open / 12.0
    if clinic in SHRINK and month_start >= K.OPENED["Quarndale"]:
        rate *= SHRINK[clinic]
    return rate


def months(start, end):
    d = dt.date(start.year, start.month, 1)
    while d <= end:
        yield d
        d = dt.date(d.year + (d.month // 12), d.month % 12 + 1, 1)


def par(clinic, reg):
    p = PARAM[clinic]
    if clinic in SHIFT and reg >= SHIFT[clinic][0]:
        p = dict(p, **SHIFT[clinic][1])
    return p


def draw_type(clinic, rng, reg=None):
    p = par(clinic, reg) if reg else PARAM[clinic]
    if rng.random() < INSCOPE_SHARE:
        return "AD" if rng.random() < p["ad"] else "MCI"
    u, acc = rng.random(), 0.0
    for t, w in OTHER_MIX:
        acc += w
        if u < acc:
            return t
    return "NOD"


def ad_code(rng):
    u = rng.random()
    return "AD" if u < 0.50 else ("AD_LATE" if u < 0.85 else "AD_MIXED")


def world(seed=SEED):
    """Referrals month by month from one stream; each patient's own course from a stream of their own, so a change to
    one clinic's parameters moves only that clinic's patients."""
    rng = np.random.default_rng(seed)
    used = set()
    pats = []
    hpn_next = 100231
    for ci, clinic in enumerate(K.NAMES):
        opened = K.OPENED[clinic]
        crng = np.random.default_rng([seed, 1000 + ci])
        for m0 in months(opened, END):
            m1 = dt.date(m0.year + (m0.month // 12), m0.month % 12 + 1, 1) - dt.timedelta(days=1)
            lo = max(m0, opened)
            span = (m1 - lo).days + 1
            for _ in range(crng.poisson(intake_per_month(clinic, m0) * span / ((m1 - m0).days + 1))):
                reg = weekday(lo + dt.timedelta(days=int(crng.integers(0, span))))
                if reg > END:
                    continue
                prng = np.random.default_rng([seed, ci, len(pats)])
                pats.append(new_patient(len(pats), clinic, reg, prng, used, hpn_next))
                pats[-1]["_rng"] = prng
                hpn_next += int(rng.integers(1, 40))
    for p in pats:
        follow(p, p.pop("_rng"))
    handovers(pats, seed)
    duplicates(pats, np.random.default_rng([seed, 99]))
    return dict(patients=pats, seed=seed)


HANDOVER = 0.06     # a year, among patients with dementia or MCI between their last review and the end of follow-up


def handovers(pats, seed):
    """A patient who moves into a care home has their care passed to the care home liaison team. It comes after the
    last review the clinic held, so no sitting moves; the episode ends on the day of the handover."""
    for p in pats:
        if not p["sittings"] or p["typ"] in ("NOD", "DEP"):
            continue
        ep = p["episodes"][-1]
        last = p["sittings"][-1]["date"]
        if ep["reason"] and not ep["reason"].startswith("Died") and ep["reason"] != "Moved out of area":
            continue
        stop = min(ep["end"] or END, END)
        lo = max(last, K.EPR_GO_LIVE)
        if stop <= lo:
            continue
        r = np.random.default_rng([seed, 55, p["pid"]])
        span = (stop - lo).days
        t = r.exponential(YEAR / HANDOVER)
        if t < span:
            h = weekday(lo + dt.timedelta(days=int(max(1, t))))
            if lo < h < stop:
                ep.update(end=h, reason="Care passed to care home liaison team")
                p["events"].append(dict(kind="handover", date=h, clinic=ep["clinic"]))


def new_patient(pid, clinic, reg, rng, used, hpn):
    typ = draw_type(clinic, rng, reg)
    pp = par(clinic, reg)
    age = float(np.clip(rng.normal(79.0, 6.5), 56, 97))
    dob = reg - dt.timedelta(days=int(age * YEAR + rng.integers(-180, 180)))
    if typ == "AD":
        rate = max(0.3, rng.normal(pp["r_ad"], 1.5))
        base = min(97.0, rng.normal(71.0, 6.0))
    elif typ == "MCI":
        rate = max(0.3, rng.normal(pp["r_mci"], 1.0))
        base = min(97.0, rng.normal(84.0, 4.0))
    else:
        mu, sd, r = OTHER_PROFILE[typ]
        rate = max(0.1, rng.normal(r, 1.0 if r > 1 else 0.3))
        base = min(98.0, rng.normal(mu, sd))
    district = K.DISTRICTS[clinic][int(rng.integers(0, len(K.DISTRICTS[clinic])))]
    if clinic in K.QUARNDALE_FROM and reg >= K.OPENED["Quarndale"]:
        keep = [d for d in K.DISTRICTS[clinic] if d not in K.QUARNDALE_FROM[clinic]]
        district = keep[int(rng.integers(0, len(keep)))]
    receipt = reg - dt.timedelta(days=int(rng.choice([0, 0, 0, 1, 1, 2, 3])))
    return dict(pid=pid, hpn="H%07d" % hpn, nhs=nhs_number(rng, used), dob=dob, sex="F" if rng.random() < 0.58 else "M",
                district=district, clinic0=clinic, receipt=receipt, registered=reg, typ=typ, rate=rate, base=base,
                code=ad_code(rng) if typ == "AD" else typ, sittings=[], dx=[], episodes=[], events=[],
                death=None, hpn2=None, source="GP" if rng.random() < 0.86 else ("Acute hospital" if rng.random() < 0.6
                                                                                 else "Community mental health"))


def entered(given, clinic, rng):
    if rng.random() < SAME_DAY_ENTRY[clinic]:
        return given
    d = given
    for _ in range(min(15, 1 + int(rng.geometric(0.28)))):
        d = weekday(d + dt.timedelta(days=1))
    return d


def add_dx(p, given, code, status, clinic, rng):
    p["dx"].append(dict(given=given, entered=entered(given, clinic, rng), code=code, status=status, clinic=clinic))


def cognition(p, d):
    return p["base"] - p["rate"] * yrs(p["first"], d)


def sitting(p, d, clinic, completed_before, rng, abandoned=False):
    cog = cognition(p, d)
    score = cog + (GAIN if completed_before >= 1 else 0.0) + rng.normal(0.0, NOISE)
    total = int(np.clip(round(score), 0, 100))
    dx = "AD" if p["typ"] == "AD" else ("MCI" if p["typ"] == "MCI" else "OTHER")
    doms = split_domains(total, dx, rng)
    s = dict(date=d, clinic=clinic, total=total, domains=doms, completed=True, k=completed_before, cog=cog)
    if abandoned:
        stop = int(rng.integers(2, 5))          # the sitting stopped after two, three or four domains
        part = [doms[i] if i < stop else None for i in range(5)]
        s.update(completed=False, domains=part, total=int(sum(x for x in part if x is not None)))
    return s


def follow(p, rng):
    """Assessment, diagnosis, reviews and the end of follow-up."""
    clinic = p["clinic0"]
    par = PARAM[clinic]
    first = weekday(add_days(p["registered"], rng.uniform(14, 45)))
    p["first"] = first
    if first > END:
        p["first"] = None
        p["episodes"].append(dict(clinic=clinic, start=p["registered"], end=None, reason=None))
        return
    typ = p["typ"]
    hazard = {"AD": 0.10, "MCI": 0.04}.get(typ, 0.08)
    p["death"] = add_days(first, rng.exponential(1.0 / hazard) * YEAR)
    moved = add_days(first, rng.exponential(1.0 / 0.012) * YEAR)
    transfer = add_days(first, rng.exponential(1.0 / 0.012) * YEAR)
    level = par["disch"] + rng.normal(0.0, 3.0)
    stable_at = (add_days(first, rng.uniform(2.0, 3.5) * YEAR) if (typ == "MCI" and rng.random() < par["mstab"])
                 else None)
    p["stable_at"] = stable_at
    other_end = add_days(first, rng.uniform(0.8, 3.0) * YEAR) if typ not in ("AD", "MCI", "NOD", "DEP") else None
    six = typ == "MCI" and rng.random() < 0.15
    ep = dict(clinic=clinic, start=p["registered"], end=None, reason=None)
    p["episodes"].append(ep)
    done = 0
    # the first assessment
    s = sitting(p, first, clinic, 0, rng)
    p["sittings"].append(s)
    done += 1
    same_day = rng.random() < 0.12
    given = first if same_day else weekday(add_days(first, rng.uniform(7, 35)))
    p["events"].append(dict(kind="assessment", date=first, clinic=clinic, dx_given=same_day))
    working = typ in ("AD", "VAS") and rng.random() < 0.08
    first_code = "UNS" if working else p["code"]
    add_dx(p, given, first_code, "Provisional" if working else "Confirmed", clinic, rng)
    if not same_day:
        p["events"].append(dict(kind="feedback", date=given, clinic=clinic))
    if typ in ("NOD", "DEP"):
        ep.update(end=given, reason="Discharged to GP")
        p["events"].append(dict(kind="discharge_at_feedback", date=given, clinic=clinic))
        return
    if typ == "AD":
        p["events"].append(dict(kind="nurse_call", date=weekday(add_days(given, rng.uniform(35, 56))), clinic=clinic))
    interval = (0.5 if six else 1.0) * par.get("iv", 1.0)
    d = first
    converted = False
    while True:
        step = interval * rng.uniform(0.85, 1.25) + (rng.uniform(0.2, 0.6) if rng.random() < 0.06 else 0.0)
        nd = weekday(add_days(d, step * YEAR))
        # what ends follow-up before the next review
        stops = [(p["death"], "Died"), (moved, "Moved out of area")]
        stop = min(stops, key=lambda x: x[0])
        if stop[0] <= min(nd, END):
            ep.update(end=stop[0], reason=stop[1])
            if stop[1] == "Died":
                pass
            return
        if nd > END:
            return
        # a move within the trust's area hands the patient to another clinic before this review
        if transfer <= nd and transfer > d:
            dest = transfer_clinic(clinic, transfer, rng)
            if dest:
                ep.update(end=transfer, reason="Transferred to %s" % dest)
                clinic = dest
                ep = dict(clinic=clinic, start=transfer, end=None, reason=None)
                p["episodes"].append(ep)
            transfer = add_days(transfer, 99 * YEAR)
        cog = cognition(p, nd)
        abandon = done >= 1 and ((cog < 45 and rng.random() < 0.15) or (45 <= cog < 55 and rng.random() < 0.08))
        s = sitting(p, nd, clinic, done, rng, abandoned=abandon)
        p["sittings"].append(s)
        ev = dict(kind="review", date=nd, clinic=clinic, sitting=len(p["sittings"]) - 1)
        p["events"].append(ev)
        if s["completed"]:
            done += 1
        # a working diagnosis is confirmed at the first review
        if working and not any(x["status"] == "Confirmed" for x in p["dx"]):
            add_dx(p, nd, p["code"] if typ == "AD" else "VAS", "Confirmed", clinic, rng)
        # MCI that has become dementia is re-diagnosed at the review
        if typ == "MCI" and not converted and cog < 76.0 + rng.normal(0, 2.0):
            u = rng.random()
            new = ad_code(rng) if u < 0.75 else ("VAS" if u < 0.90 else "DLB")
            add_dx(p, nd, new, "Confirmed", clinic, rng)
            converted = True
            interval = par.get("iv", 1.0)
            if new not in K.AD_CODES:
                p["typ_after"] = new
        # discharge at this review
        reason = None
        if cog < level:
            reason = "Discharged to community mental health team"
        elif stable_at and nd >= stable_at and not converted:
            reason = "Discharged to GP"
        elif other_end and nd >= other_end:
            reason = "Discharged to GP"
        if reason:
            ep.update(end=nd, reason=reason)
            ev["discharged"] = True
            return
        if abandon and rng.random() < 0.5:
            # tried again a few weeks later
            rd = weekday(add_days(nd, rng.uniform(28, 63)))
            if rd <= END and rd < p["death"] and rd < moved:
                s2 = sitting(p, rd, clinic, done, rng, abandoned=cognition(p, rd) < 45 and rng.random() < 0.3)
                p["sittings"].append(s2)
                p["events"].append(dict(kind="review", date=rd, clinic=clinic, sitting=len(p["sittings"]) - 1,
                                        retry=True))
                if s2["completed"]:
                    done += 1
                nd = rd
        d = nd


def transfer_clinic(clinic, day, rng):
    open_ = [c for c in K.NAMES if c != clinic and K.OPENED[c] <= day]
    if not open_:
        return None
    return open_[int(rng.integers(0, len(open_)))]


def duplicates(pats, rng):
    """About one CIS patient in 120 was registered twice; the master index merged the two numbers at migration."""
    for p in pats:
        if p["registered"] < K.EPR_GO_LIVE and rng.random() < 0.0085:
            p["hpn2"] = "H%07d" % (int(p["hpn"][1:]) + 500000 + int(rng.integers(0, 90000)))
