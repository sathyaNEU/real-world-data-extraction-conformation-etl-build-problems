"""The clean truth: every fiscal 2026 index stay at the 14 network hospitals (the member, the identifier class the
enrollment file gives the linkage, the expected mortality from the plan's risk model, whether and when the member died
within 30 days of admission, and where), the linkage's true and false links, the later stays and claims each member
had, and the stays the measure leaves out (obstetric deliveries, children, discharges against medical advice). The
claim files, the enrollment file and the linkage file are all written from here."""
import datetime as dt

import numpy as np

import world as W

SIMPLE_SURNAMES = ["NGUYEN", "TRAN", "LE", "PHAM", "HUYNH", "VO", "CHEN", "WANG", "LI", "ZHANG", "LIU", "KIM", "LEE",
                   "PARK", "GARCIA", "HERNANDEZ", "LOPEZ", "MARTINEZ", "GONZALEZ", "RODRIGUEZ", "PEREZ", "SANCHEZ"]
SIMPLE_WEIGHTS = [38, 11, 9, 7, 5, 4, 6, 5, 5, 4, 3, 7, 6, 3, 6, 5, 4, 4, 3, 3, 2, 2]
COMPOUND_FIRST = ["GARCIA", "HERNANDEZ", "LOPEZ", "MARTINEZ", "GONZALEZ", "RODRIGUEZ", "PEREZ", "SANCHEZ", "RAMIREZ",
                  "FLORES", "TORRES", "RIVERA", "CRUZ", "MORALES", "REYES", "JIMENEZ", "MENDOZA", "VARGAS", "CASTILLO"]
COMPOUND_SECOND = ["LOPEZ", "RAMIREZ", "TORRES", "DIAZ", "MORALES", "ORTIZ", "GUTIERREZ", "CHAVEZ", "RAMOS", "RUIZ",
                   "AGUILAR", "MEDINA", "DE LA CRUZ", "DE LEON", "SOTO", "VEGA", "ROJAS", "NAVARRO", "SALAZAR"]
SSN_SURNAMES = ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "MILLER", "DAVIS", "WILSON", "ANDERSON", "TAYLOR",
                "THOMAS", "MOORE", "JACKSON", "MARTIN", "THOMPSON", "WHITE", "HARRIS", "CLARK", "LEWIS", "ROBINSON",
                "WALKER", "YOUNG", "ALLEN", "KING", "WRIGHT", "SCOTT", "GREEN", "BAKER", "ADAMS", "NELSON", "HILL",
                "CAMPBELL", "MITCHELL", "ROBERTS", "CARTER", "PHILLIPS", "EVANS", "TURNER", "GARCIA", "MARTINEZ",
                "HERNANDEZ", "LOPEZ", "GONZALEZ", "NGUYEN", "PATEL", "COLLINS", "STEWART", "MORRIS", "MURPHY", "COOK"]
FIRST_F = ["MARIA", "ANA", "THI", "LINH", "MEI", "JENNIFER", "LINDA", "PATRICIA", "ELIZABETH", "SUSAN", "MARGARET",
           "ROSA", "CARMEN", "LUZ", "HOA", "LAN", "YUN", "SARAH", "KAREN", "NANCY", "BETTY", "DOROTHY", "GLORIA"]
FIRST_M = ["JOSE", "JUAN", "LUIS", "CARLOS", "VAN", "MINH", "WEI", "JAMES", "JOHN", "ROBERT", "MICHAEL", "WILLIAM",
           "DAVID", "RICHARD", "JOSEPH", "THOMAS", "MIGUEL", "JESUS", "HUNG", "DUC", "CHARLES", "GEORGE", "FRANK"]
# risk multipliers within a hospital by identifier class (the dialysis and heart-failure members of Mercy Valley are
# sicker; Varden's members without a number are young workers in for surgery or an injury)
CLASS_RISK = {"Mercy Valley Medical Center": {"compound": 1.45}, "Varden Surgical Hospital": {"simple": 0.35}}


def rng(k):
    return np.random.default_rng([W.SEED, 4, k])


def day(d0, k):
    return d0 + dt.timedelta(days=int(k))


def simulate(theta=None):
    """Every index stay and what followed it. Each hospital draws from its own stream, and each stay's decisions read a
    fixed row of uniforms, so a change to one hospital's mortality moves only the stays near its margin."""
    theta = theta or {}
    stays, members, links, activity, extra = [], [], [], [], []
    n_days = (W.FY_END - W.FY_START).days + 1
    simple_p = np.array(SIMPLE_WEIGHTS) / sum(SIMPLE_WEIGHTS)
    for hi, (name, npi, npi2, n, s_simple, s_comp, risk, th0, in_stay, later_stay, delegated) in enumerate(W.HOSPITALS):
        th = theta.get(name, th0)
        r = rng(100 + hi)
        U = r.random((n, 28))
        G = r.gamma(2.0, 1.0, n)
        LOS = r.gamma(1.6, 1.0, n)
        PO = r.poisson(1.0, (n, 4))
        for i in range(n):
            u = U[i]
            mid = hi * 100000 + i + 1
            cls = "simple" if u[0] < s_simple else ("compound" if u[0] < s_simple + s_comp else "ssn")
            sex = "F" if u[1] < 0.5 else "M"
            first = (FIRST_F if sex == "F" else FIRST_M)[int(u[2] * len(FIRST_F))]
            if cls == "simple":
                last = SIMPLE_SURNAMES[int(np.searchsorted(np.cumsum(simple_p), u[3]))]
            elif cls == "compound" or u[4] < 0.06:
                last = COMPOUND_FIRST[int(u[3] * len(COMPOUND_FIRST))] + " " + COMPOUND_SECOND[int(u[5] * len(COMPOUND_SECOND))]
            else:
                last = SSN_SURNAMES[int(u[3] * len(SSN_SURNAMES))]
            mult = CLASS_RISK.get(name, {}).get(cls, 1.0)
            p = float(min(0.85, G[i] * risk * mult / 2.0))
            age = int(np.clip(52 + 160 * p + 14 * (u[6] * 2 - 1) * 1.7, 18, 96))
            dob = W.FY_START - dt.timedelta(days=int(age * 365.25 + u[7] * 364))
            adm = day(W.FY_START, int(u[8] * n_days))
            los = int(max(1, LOS[i] * (2.6 + 30 * p)))
            dies = u[9] < min(0.95, p * th)
            death, place = None, None
            if dies:
                if u[10] < in_stay or los >= W.WINDOW - 1:   # a stay reaching day 29 can only end in the death
                    los = int(u[11] * min(los, W.WINDOW))   # died on day los of the stay, the bill closing that day
                    death, place = day(adm, los), "stay"
                else:
                    lo = los + 1
                    death = day(adm, lo + int(u[11] * (W.WINDOW + 1 - lo)))
                    place = "later_stay" if u[12] < later_stay else "home"
            disch = day(adm, los)
            transfer = (not dies or place != "stay") and u[13] < 0.025
            if transfer and dies and place == "home" and (death - disch).days < 2:
                place = "later_stay"              # died in the receiving hospital, not at home after it
            members.append(dict(member=mid, cls=cls, sex=sex, first=first, last=last, dob=dob, hosp=name,
                                delegated=bool(delegated and u[14] < 0.32)))
            stays.append(dict(member=mid, hosp=name, adm=adm, disch=disch, los=los, p=p, dies=dies, death=death,
                              place=place, transfer=transfer, cls=cls, index=True))
            rec, fp = W.CLASS_RATES[cls]
            if dies and u[15] < rec:
                links.append(dict(member=mid, adm=adm, death=death, true=True))
            elif not dies and u[15] < fp:
                links.append(dict(member=mid, adm=adm, death=day(adm, 1 + int(u[16] * W.WINDOW)), true=False))
            if transfer:
                other = W.HOSPITALS[(hi + 1 + int(u[17] * 13)) % 14][0]
                l2 = int(max(1, 1 + u[18] * 8))
                if dies and place == "home":
                    l2 = min(l2, (death - disch).days - 1)   # home from the receiving hospital before the death
                d2 = death if (dies and place == "later_stay") else None
                extra.append(dict(member=mid, hosp=other, adm=disch, disch=d2 if d2 else day(disch, l2),
                                  status="20" if d2 else "01", kind="transfer_in"))
            if dies and place == "later_stay" and not transfer:
                h2 = name if u[19] < 0.7 else W.HOSPITALS[int(u[20] * 14)][0]
                gap = max(1, (death - disch).days)
                a2 = min(day(disch, 1 + int(u[21] * gap)), death)
                extra.append(dict(member=mid, hosp=h2, adm=a2, disch=death, status="20", kind="later_death"))
            if not dies and u[22] < 0.14:
                a2 = day(disch, 3 + int(u[23] * 117))
                if a2 <= W.CLAIMS_THROUGH:
                    extra.append(dict(member=mid, hosp=name if u[24] < 0.75 else W.HOSPITALS[int(u[25] * 14)][0],
                                      adm=a2, disch=day(a2, 1 + int(u[26] * 6)), status="01", kind="readmit"))
            lam = {"ssn": 3.0, "simple": 1.2, "compound": 1.6}[cls]
            rr = np.random.default_rng([W.SEED, 9, mid])
            for _k in range(int(rr.poisson(lam))):
                activity.append((mid, day(adm, -int(rr.integers(1, 180)))))
            end_alive = death if dies else day(adm, W.WINDOW)
            for _k in range(int(rr.poisson(0.9 if cls == "ssn" else 0.5))):
                d = day(disch, rr.integers(1, 30))
                if d < end_alive and d <= day(adm, W.WINDOW):
                    activity.append((mid, d))
            if not dies and u[27] < W.LATER[cls]:
                horizon = (W.CLAIMS_THROUGH - day(adm, W.WINDOW)).days
                for _k in range(1 + int(rr.poisson(2.5))):
                    activity.append((mid, day(adm, W.WINDOW + 1 + int(rr.integers(0, max(1, horizon))))))
    return dict(stays=stays, members=members, links=links, activity=activity, extra=extra)


def truth(x):
    """Each hospital's index stays, expected deaths and true deaths within 30 days of admission."""
    out = {h: [0, 0.0, 0] for h in W.CANDIDATES}
    for s in x["stays"]:
        o = out[s["hosp"]]
        o[0] += 1
        o[1] += s["p"]
        o[2] += int(s["dies"])
    return out


# ------------------------------------------------------------------------------------------- the rest of the record
HIGH = (["871", "291", "190", "193", "064", "682", "853", "207", "870", "314"], [22, 18, 10, 12, 10, 8, 4, 4, 4, 8])
MID = (["872", "292", "194", "065", "683", "378", "189", "308", "280"], [18, 16, 14, 10, 8, 12, 8, 9, 5])
LOW = (["470", "392", "603", "638", "313", "312", "641", "690", "247", "885"], [12, 14, 12, 10, 10, 8, 9, 10, 8, 7])
SURG = (["343", "419", "481", "493", "470", "460", "603", "392"], [16, 16, 14, 14, 16, 8, 8, 8])
DIALYSIS = (["682", "683", "291", "292", "314"], [30, 25, 20, 15, 10])
DELIV = (["807", "806", "805", "788", "787", "786", "798", "797", "768"], [55, 8, 2, 22, 7, 2, 2, 1, 1])
NEWBORN = (["795", "794", "793", "792", "791", "790"], [78, 12, 4, 3, 2, 1])
PEDS = (["203", "195", "392", "343", "690", "603"], [26, 20, 18, 14, 12, 10])
ELECTIVE = {"470": 0.85, "460": 0.8, "247": 0.5, "419": 0.35}


def pick(r, table):
    codes, w = table
    w = np.asarray(w, float)
    return codes[int(np.searchsorted(np.cumsum(w / w.sum()), r.random()))]


def drg_for(p, hosp, cls, r):
    if hosp == "Varden Surgical Hospital" and r.random() < 0.8:
        return pick(r, SURG)
    if hosp == "Mercy Valley Medical Center" and cls == "compound":
        return pick(r, DIALYSIS)
    return pick(r, HIGH if p >= 0.12 else (MID if p >= 0.04 else LOW))


def adm_type(drg, r):
    if r.random() < ELECTIVE.get(drg, 0.0):
        return "3"
    return "1" if r.random() < 0.8 else "2"


def person(r, hosp_row, adult=True, sex=None, age=None, last=None):
    """A member who is not one of the index admissions' members: identifier class from the hospital's mix, a name, a
    date of birth (age on 1 July 2025 unless given) and whether Carrisford Medical Group holds the member."""
    name, npi, npi2, n, s_simple, s_comp, risk, th, in_stay, later_stay, delegated = hosp_row
    u = r.random(8)
    cls = "simple" if u[0] < s_simple else ("compound" if u[0] < s_simple + s_comp else "ssn")
    sex = sex or ("F" if u[1] < 0.5 else "M")
    first = (FIRST_F if sex == "F" else FIRST_M)[int(u[2] * len(FIRST_F))]
    if last is None:
        if cls == "simple":
            last = SIMPLE_SURNAMES[int(np.searchsorted(np.cumsum(np.array(SIMPLE_WEIGHTS) / sum(SIMPLE_WEIGHTS)), u[3]))]
        elif cls == "compound" or u[4] < 0.06:
            last = COMPOUND_FIRST[int(u[3] * len(COMPOUND_FIRST))] + " " + COMPOUND_SECOND[int(u[5] * len(COMPOUND_SECOND))]
        else:
            last = SSN_SURNAMES[int(u[3] * len(SSN_SURNAMES))]
    dob = W.FY_START - dt.timedelta(days=int(age * 365.25 + u[6] * 364)) if age is not None else None
    return dict(cls=cls, sex=sex, first=first, last=last, dob=dob, hosp=name,
                delegated=bool(delegated and u[7] < W.CARRISFORD_SHARE))


def extend(x):
    """Everything the measure leaves out or never reads, on streams of its own so that the index stays, their deaths,
    links and claims activity (and so the calibration) are untouched: each stay's DRG, admission type, payer and
    payment; the later stays' risk scores; the deliveries, newborns, pediatric stays, discharges against medical advice,
    the stays that began before July 2025 and those that began after June 2026; the linkage's returns on the adult
    admissions that are not index admissions; and the non-index members' claims activity."""
    if "nonindex" in x:
        return x
    mem = {m["member"]: m for m in x["members"]}
    by_hosp = {h[0]: h for h in W.HOSPITALS}
    idx = {s["member"]: s for s in x["stays"]}
    linked_true = {l["member"] for l in x["links"] if l["true"]}
    r = rng(201)
    for s in x["stays"]:
        s["drg"] = drg_for(s["p"], s["hosp"], s["cls"], r)
        s["adm_type"] = adm_type(s["drg"], r)
        s["status"] = "20" if s["place"] == "stay" else ("02" if s["transfer"] else "01")
    for e in x["extra"]:
        s = idx[e["member"]]
        if e["status"] == "20":
            e["p"] = float(min(0.85, max(0.18, s["p"] * (1.6 + r.random()))))
            e["drg"] = pick(r, HIGH)
        else:
            e["p"] = float(min(0.85, s["p"] * (0.7 + 0.7 * r.random())))
            e["drg"] = drg_for(e["p"], e["hosp"], s["cls"], r)
        e["adm_type"] = "1" if e["kind"] != "readmit" or r.random() < 0.85 else "2"
    nonindex, newm, xlinks, xact = [], [], [], []
    n_days = (W.FY_END - W.FY_START).days + 1
    nid = 2_000_000

    def add_member(d):
        nonlocal nid
        nid += 1
        d["member"] = nid
        newm.append(d)
        return nid

    for hi, row in enumerate(W.HOSPITALS):
        name, n = row[0], row[3]
        rr = rng(300 + hi)
        for _k in range(int(round(n * W.DELIVERIES[name]))):
            age = int(rr.integers(16, 43)) if rr.random() < 0.97 else int(rr.integers(16, 18))
            mom = person(rr, row, sex="F", age=age)
            m = add_member(mom)
            adm = day(W.FY_START, int(rr.random() * n_days))
            drg = pick(rr, DELIV)
            los = int(rr.integers(1, 4)) if drg in ("807", "806", "805", "798", "797", "768") else int(rr.integers(2, 6))
            nonindex.append(dict(member=m, hosp=name, adm=adm, disch=day(adm, los), status="01", drg=drg,
                                 adm_type="1" if rr.random() < 0.7 else "3", p=float(0.0002 + 0.0012 * rr.random()),
                                 kind="delivery", adult=age >= 18))
            for _t in range(2 if rr.random() < 0.02 else 1):
                nb = dict(cls="ssn", sex="F" if rr.random() < 0.49 else "M", last=mom["last"], hosp=name,
                          delegated=mom["delegated"], dob=adm)
                nb["first"] = "BABY GIRL" if nb["sex"] == "F" else "BABY BOY"
                b = add_member(nb)
                ndrg = pick(rr, NEWBORN)
                nlos = los if ndrg == "795" else int(rr.integers(5, 46 if ndrg in ("790", "791") else 15))
                nonindex.append(dict(member=b, hosp=name, adm=adm, disch=day(adm, nlos), status="01", drg=ndrg,
                                     adm_type="4", p=None, kind="newborn", adult=False))
                for _v in range(int(rr.integers(2, 6))):
                    xact.append((b, day(adm, int(rr.integers(3, 150)))))
            for _v in range(int(rr.integers(2, 7))):
                xact.append((m, day(adm, -int(rr.integers(10, 220)))))
            for _v in range(int(rr.integers(1, 4))):
                xact.append((m, day(adm, int(rr.integers(5, 70)))))
            if age >= 18 and rr.random() < W.CLASS_RATES[mom["cls"]][1]:
                xlinks.append(dict(member=m, adm=adm, death=day(adm, 1 + int(rr.random() * W.WINDOW)), true=False))
        for _k in range(int(round(n * W.PEDIATRIC[name]))):
            kid = person(rr, row, age=int(rr.integers(1, 17)))
            kid["cls"] = "ssn" if rr.random() < 0.9 else kid["cls"]
            m = add_member(kid)
            adm = day(W.FY_START, int(rr.random() * n_days))
            nonindex.append(dict(member=m, hosp=name, adm=adm, disch=day(adm, int(rr.integers(1, 6))), status="01",
                                 drg=pick(rr, PEDS), adm_type="1", p=None, kind="pediatric", adult=False))
            for _v in range(int(rr.integers(1, 5))):
                xact.append((m, day(adm, int(rr.integers(-200, 200)))))
        for _k in range(int(round(n * W.AMA))):
            ama = person(rr, row, age=int(rr.integers(19, 70)))
            m = add_member(ama)
            adm = day(W.FY_START, int(rr.random() * n_days))
            p = float(0.005 + 0.045 * rr.random())
            nonindex.append(dict(member=m, hosp=name, adm=adm, disch=day(adm, int(rr.integers(0, 4))), status="07",
                                 drg=drg_for(p, name, ama["cls"], rr), adm_type="1", p=p, kind="ama", adult=True))
            for _v in range(int(rr.integers(1, 4))):
                xact.append((m, day(adm, -int(rr.integers(1, 180)))))
            if rr.random() < W.LATER[ama["cls"]]:
                for _v in range(int(rr.integers(1, 4))):
                    xact.append((m, day(adm, int(rr.integers(31, 300)))))
            if rr.random() < W.CLASS_RATES[ama["cls"]][1]:
                xlinks.append(dict(member=m, adm=adm, death=day(adm, 1 + int(rr.random() * W.WINDOW)), true=False))
        for _k in range(int(round(n * 5 / 365.0))):
            sp = person(rr, row, age=int(rr.integers(25, 85)))
            m = add_member(sp)
            adm = day(W.FY_START, -int(rr.integers(1, 8)))
            p = float(0.01 + 0.08 * rr.random())
            nonindex.append(dict(member=m, hosp=name, adm=adm, disch=day(W.FY_START, int(rr.integers(0, 9))),
                                 status="01", drg=drg_for(p, name, sp["cls"], rr), adm_type="1", p=None,
                                 kind="before_fy", adult=True))
        for _k in range(int(round(n * (1 + W.DELIVERIES[name] * 2 + W.PEDIATRIC[name]) * 0.2))):
            later = person(rr, row, age=int(rr.integers(1, 85)))
            m = add_member(later)
            adm = day(W.FY_END, int(rr.integers(1, 82)))
            p = float(0.002 + 0.06 * rr.random())
            nonindex.append(dict(member=m, hosp=name, adm=adm, disch=day(adm, int(rr.integers(1, 7))), status="01",
                                 drg=drg_for(p, name, later["cls"], rr), adm_type="1", p=None, kind="after_fy",
                                 adult=True))
            for _v in range(int(rr.integers(1, 4))):
                xact.append((m, day(adm, -int(rr.integers(1, 200)))))
    # the linkage's returns on the adult admissions that are not index admissions: a later stay of a member who died
    # within the index window carries the same death when the index admission's record linked to it; any other record
    # of a living member may draw a false link inside its own 30 days
    r2 = rng(202)
    for e in x["extra"]:
        s = idx[e["member"]]
        if e["adm"] > W.FY_END:
            continue
        if s["dies"] and s["death"] <= day(e["adm"], W.WINDOW) and s["death"] >= e["adm"]:
            if e["member"] in linked_true:
                xlinks.append(dict(member=e["member"], adm=e["adm"], death=s["death"], true=True))
        elif not s["dies"] and r2.random() < W.CLASS_RATES[s["cls"]][1]:
            xlinks.append(dict(member=e["member"], adm=e["adm"], death=day(e["adm"], 1 + int(r2.random() * W.WINDOW)),
                               true=False))
    x["nonindex"], x["newmembers"], x["xlinks"], x["xactivity"] = nonindex, newm, xlinks, xact
    return x
