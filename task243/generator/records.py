"""task243 records: the civil registry system's death and birth extracts, the two censuses' household population
tables, the 2020 census's special tabulation of residence five years earlier, the LGU directory, the provincial health
office's roster of health officers, and the two files the review does not use (the FHSIS mortality reports and the
LCRO staffing survey). Every row comes from the simulated province (sim.py); the registration process, the mess the
offices' systems produce and the asks' records are drawn here, each from its own seeded stream."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

PROV = "KALINAWAN"
PSGC = {c: "1049%02d000" % (i + 1) for i, c in enumerate(P.CODES)}
UPPER = {
    "KLW-01": "KALINAWAN CITY", "KLW-02": "CITY OF SANTA CRUZ", "KLW-03": "SAN ISIDRO", "KLW-04": "ESPERANZA",
    "KLW-05": "MAGSAYSAY", "KLW-06": "MABINI", "KLW-07": "LIBERTAD", "KLW-08": "SAN LUIS", "KLW-09": "DEL CARMEN",
    "KLW-10": "QUEZON", "KLW-11": "RIZAL", "KLW-12": "SAN MIGUEL"}
# the residence as informants give it and offices encode it
VARIANTS = {
    "KLW-01": ["KALINAWAN CITY", "CITY OF KALINAWAN", "Kalinawan City", "KALINAWAN CITY "],
    "KLW-02": ["CITY OF SANTA CRUZ", "STA. CRUZ", "SANTA CRUZ", "Sta Cruz", "SANTA CRUZ CITY"],
    "KLW-03": ["SAN ISIDRO", "San Isidro", "SN. ISIDRO"],
    "KLW-04": ["ESPERANZA", "Esperanza"],
    "KLW-05": ["MAGSAYSAY", "Magsaysay"],
    "KLW-06": ["MABINI", "Mabini", "MABINI "],
    "KLW-07": ["LIBERTAD", "Libertad"],
    "KLW-08": ["SAN LUIS", "San Luis", "SN LUIS"],
    "KLW-09": ["DEL CARMEN", "Del Carmen", "DEL CARMEN "],
    "KLW-10": ["QUEZON", "Quezon"],
    "KLW-11": ["RIZAL", "Rizal"],
    "KLW-12": ["SAN MIGUEL", "San Miguel", "SN. MIGUEL"]}
OUTSIDE_LCRO = [("104305000", "CITY OF CAGAYAN DE ORO"), ("112402000", "DAVAO CITY"), ("101312000", "CITY OF MALAYBALAY")]
OTHER_PROVINCES = ["BUKIDNON", "AGUSAN DEL SUR", "DAVAO DEL NORTE", "LANAO DEL NORTE", "MISAMIS ORIENTAL", "COTABATO"]
OTHER_TOWN = dict(zip(OTHER_PROVINCES, ["VALENCIA CITY", "PROSPERIDAD", "PANABO CITY", "KAPATAGAN", "GINGOOG CITY",
                                        "KIDAPAWAN CITY"]))
BARANGAYS = ["POBLACION", "SAN JOSE", "BAGONG SILANG", "MABUHAY", "MALIGAYA", "SAN ROQUE", "SANTO NINO", "KAUSWAGAN",
             "LUMBIA", "TAGUMPAY", "MAHAYAG", "BALINTAWAK", "SAN VICENTE", "NEW VISAYAS", "CAMANSI", "DALIPUAN",
             "LUNOCAN", "MALINGON", "PANADTARAN", "SIOCON", "TIGBAO", "BACOLOD", "CAPITOL", "LAPUZ", "MANAPA"]
MALE = ["JOSE", "JUAN", "PEDRO", "ANTONIO", "RICARDO", "RODRIGO", "EDUARDO", "FERNANDO", "ROBERTO", "ROGELIO", "ROMEO",
        "RAMON", "ERNESTO", "DANILO", "REYNALDO", "ROLANDO", "ARNEL", "JOEL", "MARK", "JOHN", "CHRISTIAN", "JEROME",
        "JAYSON", "RONALD", "MICHAEL", "JEFFREY", "NOEL", "ALLAN", "EDGAR", "VIRGILIO", "ALFREDO", "BENJAMIN", "CARLOS",
        "EMILIO", "FRANCISCO", "GREGORIO", "ISMAEL", "LEONARDO", "MANUEL", "NESTOR", "OSCAR", "PABLO", "RAFAEL",
        "SANTIAGO", "TEODORO", "VICENTE", "WILFREDO", "BERNARDO", "RUBEN", "DOMINGO", "FELIPE", "LORENZO", "MARCELO",
        "ORLANDO", "RENATO", "SALVADOR", "TOMAS", "VICTOR", "ARTURO", "CELSO", "DIONISIO", "ELMER", "FLORENCIO",
        "GERARDO", "IGNACIO", "JAIME", "MARIO", "NILO", "ALBERTO", "BONIFACIO", "CRISPIN", "DEMETRIO", "ROMULO"]
FEMALE = ["MARIA", "ANA", "ROSA", "TERESITA", "LOURDES", "CORAZON", "REMEDIOS", "ERLINDA", "GLORIA", "LEONORA",
          "MILAGROS", "NENITA", "PERLA", "ROSARIO", "SOCORRO", "TRINIDAD", "VIRGINIA", "ZENAIDA", "MARITES", "MARICEL",
          "JENNIFER", "MICHELLE", "KRISTINE", "ANGELICA", "JOY", "GRACE", "MARY ANN", "ROWENA", "LORNA", "MARILYN",
          "JOSEPHINE", "EVELYN", "CRISTINA", "ROSALINDA", "IMELDA", "FELICIDAD", "NATIVIDAD", "CONCEPCION", "DOLORES",
          "LUZVIMINDA", "MERLINDA", "NORA", "OFELIA", "PACITA", "REBECCA", "SUSANA", "VILMA", "AMELIA", "BELEN",
          "CARMELITA", "DINA", "ELENA", "GEMMA", "HELEN", "IRENE", "JOCELYN", "LETICIA", "MERCEDES", "NORMA", "PURITA",
          "RHEA", "SHEILA", "THELMA", "VANESSA", "AILEEN", "CHERRY", "DAISY", "EDNA", "FLORDELIZA", "JULIETA"]
SURNAMES = ["SANTOS", "REYES", "CRUZ", "BAUTISTA", "OCAMPO", "GARCIA", "MENDOZA", "TORRES", "ANDRADA", "CASTILLO",
            "FLORES", "VILLANUEVA", "RAMOS", "CASTRO", "RIVERA", "AQUINO", "NAVARRO", "SALAZAR", "MERCADO", "AGUILAR",
            "GONZALES", "LOPEZ", "HERNANDEZ", "FERNANDEZ", "DELA CRUZ", "DE LEON", "DEL ROSARIO", "PASCUAL", "DOMINGO",
            "SORIANO", "VALDEZ", "GUTIERREZ", "MORALES", "MANALO", "LIM", "TAN", "DIZON", "JAVIER", "MEDINA", "DIAZ",
            "PANGANIBAN", "MACARAEG", "DIMACULANGAN", "YLAGAN", "CABRERA", "PADILLA", "VELASCO", "ROSALES",
            "SARMIENTO", "VALENCIA", "ESPIRITU", "ABAD", "AGUSTIN", "ALVAREZ", "BELMONTE", "CALDERON", "DELA PENA",
            "ENRIQUEZ", "ESTRADA", "EVANGELISTA", "GALANG", "JACINTO", "LACSON", "LEGASPI", "LUCERO", "MAGBANUA",
            "MALONZO", "MARQUEZ", "MONTEMAYOR", "NEPOMUCENO", "ONG", "PINEDA", "QUIAMBAO", "ROBLES", "SAMONTE",
            "TOLENTINO", "UMALI", "VERGARA", "YAP", "ZAMORA", "ABELLA", "BALUYOT", "CABANILLA", "DALISAY", "EBARLE",
            "GABRIEL", "HILARIO", "ILAGAN", "LABRADOR", "MABANTA", "OLIVEROS", "PALMA", "RAYMUNDO", "SABADO", "TABORA",
            "UBALDO", "VILLAREAL", "LAGUNDI", "SUMALINOG", "BANAYO", "CAGAS", "DUMALAGAN", "TAMPUS", "OMANDAM"]
AGE_GROUPS = ["0 - 4", "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49",
              "50 - 54", "55 - 59", "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 and over"]


def D(x):
    return sim.EPOCH + dt.timedelta(days=int(x))


def iso(d):
    return d.isoformat() if d else ""


class Records:
    def __init__(self, W):
        self.W = W
        self.truth = {}
        self._names()
        self._officers()

    # ------------------------------------------------------------------ people's names
    def _names(self):
        W = self.W
        r = np.random.default_rng([P.SEED, 1])
        n = W.n
        self.first = np.where(W.sex[:n] == 1, r.integers(0, len(MALE), n), r.integers(0, len(FEMALE), n))
        self.last = r.integers(0, len(SURNAMES), n)
        self.middle = r.integers(0, len(SURNAMES), n)
        self.brgy = r.integers(0, len(BARANGAYS), n)
        # a child takes its father's surname and its mother's surname as middle name
        kids = np.nonzero(W.mother[:n] >= 0)[0]
        m = W.mother[kids]
        self.middle[kids] = self.last[m]
        self.last[kids] = r.integers(0, len(SURNAMES), kids.size)
        self.brgy[kids] = self.brgy[m]

    def fname(self, p):
        return MALE[self.first[p]] if self.W.sex[p] == 1 else FEMALE[self.first[p]]

    def _officers(self):
        """each LGU's health officer and, where the post was vacant in 2022, the nurse in charge"""
        r = np.random.default_rng([P.SEED, 2])
        self.officer = {}
        for c in P.CODES:
            phys = "%s %s %s" % (MALE[r.integers(len(MALE))] if r.random() < 0.5 else FEMALE[r.integers(len(FEMALE))],
                                 SURNAMES[r.integers(len(SURNAMES))][0] + ".", SURNAMES[r.integers(len(SURNAMES))])
            nurse = "%s %s %s" % (FEMALE[r.integers(len(FEMALE))], SURNAMES[r.integers(len(SURNAMES))][0] + ".",
                                  SURNAMES[r.integers(len(SURNAMES))])
            nxt = "%s %s %s" % (MALE[r.integers(len(MALE))], SURNAMES[r.integers(len(SURNAMES))][0] + ".",
                                SURNAMES[r.integers(len(SURNAMES))])
            self.officer[c] = dict(phys=phys, nurse=nurse, next=nxt)
        self.doctors = ["%s %s %s" % (MALE[r.integers(len(MALE))] if r.random() < 0.5 else FEMALE[r.integers(len(FEMALE))],
                                      SURNAMES[r.integers(len(SURNAMES))][0] + ".", SURNAMES[r.integers(len(SURNAMES))])
                        for _ in range(64)]
        # each health office's nurses and midwives, who sign some certificates made in the office's name
        self.staff = {}
        for c in P.CODES:
            people = []
            for pos, k in (("Nurse II", 3), ("Rural Health Midwife", 4)):
                for _ in range(k):
                    nm = "%s %s %s" % (FEMALE[r.integers(len(FEMALE))] if r.random() < 0.8 else MALE[r.integers(len(MALE))],
                                       SURNAMES[r.integers(len(SURNAMES))][0] + ".", SURNAMES[r.integers(len(SURNAMES))])
                    people.append((nm, pos))
            self.staff[c] = people
        self.mayor = {c: "%s %s %s" % (MALE[r.integers(len(MALE))], SURNAMES[r.integers(len(SURNAMES))][0] + ".",
                                       SURNAMES[r.integers(len(SURNAMES))]) for c in P.CODES}

    def health_officer(self, c, when):
        """who certified an unattended death in LGU c on a date, and whether that person is a physician"""
        o = self.officer[c]
        if c in P.VACANT:
            a, b = P.VACANT[c]
            if a <= when <= b:
                return o["nurse"], False
            if when > b:
                return o["next"], True
        return o["phys"], True

    # ------------------------------------------------------------------ the registration of deaths
    def deaths(self):
        if hasattr(self, "_deaths"):
            return self._deaths
        W = self.W
        r = np.random.default_rng([P.SEED, 3])
        lo, hi = sim.days(dt.date(2015, 1, 1)), sim.days(P.END)
        ev = [(p, d, l) for p, d, l in W.deaths if lo <= d <= hi and l < 12]
        u = r.random((len(ev), 12))
        rows, truth = [], []
        for k, (p, d, l) in enumerate(ev):
            c = P.CODES[l]
            when = D(d)
            age = (d - W.birth[p]) / 365.2425
            creg = P.C_TRUE[c] * (P.INFANT_REG_FACTOR if age < 1 else (0.9 if age < 5 else 1.0))
            reg = u[k, 0] < creg
            truth.append((p, when, c, age, reg))
            if not reg:
                continue
            kind = P.KIND[c]
            x = u[k, 1]
            if x < P.HOSPITAL_CITY[kind]:
                pod, place = "HOSPITAL", "KLW-01"
            elif x < P.HOSPITAL_CITY[kind] + 0.10 and c != "KLW-01":
                pod, place = "HOSPITAL", c
            elif x < P.HOSPITAL_CITY[kind] + 0.12:
                pod, place = "HOSPITAL", "OUT"
            elif x < P.HOSPITAL_CITY[kind] + 0.15:
                pod, place = "OTHERS", c
            else:
                pod, place = "HOME", c
            lockdown = P.LOCKDOWN[0] <= when <= P.LOCKDOWN[1]
            timely = u[k, 2] < (0.35 if lockdown else P.TIMELY)
            delay = 1 + int(u[k, 3] * 29) if timely else 31 + int(-np.log(1 - u[k, 4]) * (120 if lockdown else 170))
            dreg = when + dt.timedelta(days=delay)
            if dreg > P.END:
                continue
            if place == "OUT":
                j = int(u[k, 5] * len(OUTSIDE_LCRO))
                lcro, lname = OUTSIDE_LCRO[j]
                pdeath = lname
            else:
                lcro, lname = PSGC[place], self.lcro_name(place, dreg)
                pdeath = self.res_text(place, dreg, u[k, 6], formal=True)
            att, cname, ctitle, phys = self.certifier(c, pod, when, u[k, 7], u[k, 8])
            base = dict(person=p, lcro=lcro, lcro_name=lname, dreg=dreg, cert="DEATH", dod=when, age=age, l=c,
                        pod=pod, pdeath=pdeath, att=att, cname=cname, ctitle=ctitle, phys=phys, resident=True,
                        resv=u[k, 9], dobu=u[k, 10])
            rows.append(base)
            # the same death registered again at the residence office
            if lcro == PSGC["KLW-01"] and pod == "HOSPITAL":
                rate = P.DEATH_DOUBLE_2022 if when >= dt.date(2021, 1, 1) else P.DEATH_DOUBLE_WINDOW
                if c == "KLW-01":
                    rate = rate * 0.15
                if u[k, 11] < rate:
                    d2 = dreg + dt.timedelta(days=28 + int(u[k, 11] * 1000) % 190)
                    if d2 <= P.END:
                        rows.append(dict(base, lcro=PSGC[c], lcro_name=self.lcro_name(c, d2), dreg=d2, dup_of=True,
                                         resv=(u[k, 9] + 0.37) % 1.0))
        self.truth["deaths"] = truth
        rows += self._nonresident_deaths(r)
        rows += self._fetal_deaths(r)
        df = self._death_frame(rows, r)
        self._deaths = df
        return df

    def lcro_name(self, c, when):
        if c == "KLW-02" and when < P.CITYHOOD:
            return "LCRO SANTA CRUZ"
        return "LCRO " + UPPER[c]

    def res_text(self, c, when, u, formal=False):
        v = VARIANTS[c]
        if c == "KLW-02" and when < P.CITYHOOD:
            v = ["SANTA CRUZ", "STA. CRUZ", "Sta Cruz", "SANTA CRUZ"]
        if formal or u < 0.84:
            return v[0]
        return v[1 + int((u - 0.84) / 0.16 * (len(v) - 1)) % (len(v) - 1)]

    def certifier(self, c, pod, when, u1, u2):
        if pod == "HOSPITAL":
            doc = self.doctors[int(u2 * len(self.doctors))]
            return (3 if u1 < 0.7 else 1), doc, ("MD" if u1 < 0.55 else "ATTENDING PHYSICIAN"), True
        if u1 < P.ATTENDED_HOME:
            return 1, self.doctors[int(u2 * len(self.doctors))], "MD", True
        office = "CHO" if c == "KLW-01" else "MHO"
        att = 4 if u1 < 0.92 else 5
        if u1 > 1 - P.MAYOR_CERT[P.KIND[c]]:
            return att, self.mayor[c], ("CITY MAYOR" if c in ("KLW-01", "KLW-02") else "MUNICIPAL MAYOR"), False
        name, phys = self.health_officer(c, when)
        title = office
        if phys and u2 > P.OFFICER_SIGNS[P.KIND[c]]:
            name, pos = self.staff[c][int(u2 * 997) % len(self.staff[c])]
            phys = False
            if (u2 * 7919) % 1.0 < 0.25:
                title = "NURSE" if pos.startswith("Nurse") else "MIDWIFE"
        return att, name, title, phys

    def _nonresident_deaths(self, r):
        rows = []
        y0, y1 = dt.date(2015, 1, 1), P.END
        n = int(P.NONRES_PER_YEAR * ((y1 - y0).days / 365.25))
        days = r.integers(0, (y1 - y0).days, n)
        for k in range(n):
            when = y0 + dt.timedelta(days=int(days[k]))
            age = float(np.clip(r.normal(62, 18), 0.1, 98))
            delay = 1 + int(r.random() * 29) if r.random() < 0.85 else 31 + int(r.exponential(120))
            dreg = when + dt.timedelta(days=delay)
            if dreg > P.END:
                continue
            rows.append(dict(person=-1, lcro=PSGC["KLW-01"], lcro_name=self.lcro_name("KLW-01", dreg), dreg=dreg,
                             cert="DEATH", dod=when, age=age, l=None, prov=OTHER_PROVINCES[r.integers(len(OTHER_PROVINCES))],
                             pod="HOSPITAL", pdeath="KALINAWAN CITY", att=3, cname=self.doctors[r.integers(64)],
                             ctitle="MD", phys=True, resident=False, sex=int(r.random() < 0.55),
                             fn=int(r.integers(0, 70)), ln=int(r.integers(len(SURNAMES))), mn=int(r.integers(len(SURNAMES))),
                             resv=r.random(), dobu=r.random()))
        return rows

    def _fetal_deaths(self, r):
        """fetal deaths, registered on the certificate of fetal death at the office of the place of delivery"""
        W = self.W
        rows = []
        lo, hi = sim.days(dt.date(2015, 1, 1)), sim.days(P.END)
        for k_, m_, b_, l_ in W.births:
            if not (lo <= b_ <= hi) or l_ >= 12:
                continue
            if r.random() < 0.0085 and r.random() < 0.7:
                c = P.CODES[l_]
                when = D(b_)
                place = "KLW-01" if r.random() < P.BIRTH_HOSP_CITY[P.KIND[c]] else c
                dreg = when + dt.timedelta(days=1 + int(r.random() * 40))
                if dreg > P.END:
                    continue
                rows.append(dict(person=-2, mother=m_, lcro=PSGC[place], lcro_name=self.lcro_name(place, dreg), dreg=dreg,
                                 cert="FETAL DEATH", dod=when, age=None, l=c, pod="HOSPITAL" if place == "KLW-01" else "HOME",
                                 pdeath=UPPER[place], att=3 if place == "KLW-01" else 4,
                                 cname=self.doctors[r.integers(64)] if place == "KLW-01" else self.health_officer(c, when)[0],
                                 ctitle="MD" if place == "KLW-01" else ("CHO" if c == "KLW-01" else "MHO"), phys=True,
                                 resident=True, sex=int(r.random() < 0.5), resv=r.random(), dobu=r.random()))
        return rows

    def _death_frame(self, rows, r):
        W = self.W
        out = []
        for x in rows:
            p = x["person"]
            when = x["dod"]
            if p >= 0:
                sex = int(W.sex[p])
                fn, ln, mn = self.fname(p), SURNAMES[self.last[p]], SURNAMES[self.middle[p]]
                bd = D(W.birth[p])
                brgy = BARANGAYS[self.brgy[p]]
            elif p == -1:
                sex = x["sex"]
                fn = (MALE if sex == 1 else FEMALE)[x["fn"] % len(MALE if sex == 1 else FEMALE)]
                ln, mn = SURNAMES[x["ln"]], SURNAMES[x["mn"]]
                bd = when - dt.timedelta(days=int(x["age"] * 365.2425))
                brgy = BARANGAYS[int(x["resv"] * len(BARANGAYS))]
            else:
                sex = x["sex"]
                m = x["mother"]
                fn, ln, mn = ("BABY BOY" if sex == 1 else "BABY GIRL"), SURNAMES[self.last[m]], ""
                bd = None
                brgy = BARANGAYS[self.brgy[m]]
            age = x["age"]
            if x["cert"] == "FETAL DEATH":
                av, au, dob = "", "", ""
            elif age is not None and age >= 1:
                # a hospital's certificate is filled from its admission record, which always carries the date of birth
                hosp = x["pod"] == "HOSPITAL"
                av, au = str(int(age)), "YEARS"
                dob = iso(bd) if (hosp or x["dobu"] < 0.80 or age < 15) else ""
                if age >= 15 and x["dobu"] > 0.989 and not hosp:
                    av, au, dob = "", "", ""
            else:
                days_ = int(age * 365.2425) if age is not None else 0
                if days_ >= 30:
                    av, au = str(min(11, days_ // 30)), "MONTHS"
                elif days_ >= 1:
                    av, au = str(days_), "DAYS"
                else:
                    av, au = str(max(1, int(age * 365.2425 * 24))), "HOURS"
                dob = iso(bd)
            if x["resident"]:
                res = self.res_text(x["l"], x["dreg"], x["resv"])
                prov = PROV if x["resv"] < 0.93 else "Kalinawan"
            else:
                res = OTHER_TOWN[x["prov"]]
                prov = x["prov"]
            if age is None:
                cs = ""
            elif age < 18:
                cs = "SINGLE"
            else:
                cs = ["SINGLE", "MARRIED", "WIDOWED"][0 if x["resv"] < 0.12 else (1 if age < 65 or x["resv"] < 0.45 else 2)]
            out.append(dict(
                REGISTRY_NO="", LCRO_CODE=x["lcro"], LCRO_NAME=x["lcro_name"], DATE_REGISTERED=iso(x["dreg"]),
                CERT_TYPE=x["cert"], LAST_NAME=ln, FIRST_NAME=fn, MIDDLE_NAME=mn, SEX="MALE" if sex == 1 else "FEMALE",
                DATE_OF_DEATH=iso(when), DATE_OF_BIRTH=dob, AGE=av, AGE_UNIT=au, CIVIL_STATUS=cs,
                RES_BARANGAY=brgy, RES_CITY_MUN=res, RES_PROVINCE=prov, PLACE_OF_DEATH=x["pod"],
                PLACE_OF_DEATH_CITY_MUN=x["pdeath"], ATTENDANT=x["att"], CERTIFIED_BY=x["cname"],
                CERTIFIER_TITLE=x["ctitle"], LATE_REGISTRATION="Y" if (x["dreg"] - when).days > 30 else "N",
                _l=x["l"] if x["resident"] else "", _phys=x["phys"], _dup=x.get("dup_of", False), _person=p))
        df = pd.DataFrame(out)
        df = df.sort_values(["LCRO_CODE", "DATE_REGISTERED", "LAST_NAME", "FIRST_NAME"], kind="mergesort").reset_index(drop=True)
        seq = {}
        nos = []
        for lc, d_ in zip(df["LCRO_CODE"], df["DATE_REGISTERED"]):
            key = (lc, d_[:4])
            seq[key] = seq.get(key, 0) + 1
            nos.append("%s-%05d" % (d_[:4], seq[key]))
        df["REGISTRY_NO"] = nos
        # a batch re-sent from two offices' systems: the same rows again
        extra = []
        for c, a, b in P.EXTRACT_DUP_BATCHES:
            m = (df["LCRO_CODE"] == PSGC[c]) & (df["DATE_REGISTERED"] >= a.isoformat()) & (df["DATE_REGISTERED"] <= b.isoformat())
            extra.append(df[m])
        df = pd.concat([df] + extra, ignore_index=True)
        df = df.sort_values(["LCRO_CODE", "DATE_REGISTERED", "REGISTRY_NO"], kind="mergesort").reset_index(drop=True)
        return df

    def death_extract(self):
        return self.deaths().drop(columns=[c for c in self.deaths().columns if c.startswith("_")])

    # ------------------------------------------------------------------ the registration of births (ask A)
    def births(self):
        if hasattr(self, "_births"):
            return self._births
        W = self.W
        r = np.random.default_rng([P.SEED, 4])
        lo, hi = sim.days(dt.date(2021, 6, 1)), sim.days(P.END)
        w0, w1 = dt.date(2022, 1, 1), P.END
        ev = [(k_, m_, b_, l_) for k_, m_, b_, l_ in W.births if lo <= b_ <= hi and l_ < 12]
        u = r.random((len(ev), 10))
        group = {}
        for i, (k_, m_, b_, l_) in enumerate(ev):
            group.setdefault((m_, b_), []).append(i)
        rows, truth = [], []
        for i, (k_, m_, b_, l_) in enumerate(ev):
            c = P.CODES[l_]
            when = D(b_)
            grp = group[(m_, b_)]
            lead = grp[0]
            reg = u[lead, 0] < P.BIRTH_REG
            timely = u[lead, 1] < P.BIRTH_TIMELY[c]
            delay = 1 + int(u[lead, 2] * 29) if timely else 31 + int(-np.log(1 - u[lead, 3]) * 95)
            dreg = when + dt.timedelta(days=delay)
            truth.append((k_, when, c, reg and dreg <= w1, delay <= 30))
            if not reg or not (w0 <= dreg <= w1):
                continue
            hosp = u[lead, 4] < P.BIRTH_HOSP_CITY[P.KIND[c]]
            place = "KLW-01" if hosp else c
            twin = len(grp) > 1
            base = dict(child=k_, mother=m_, dob=when, dreg=dreg, lcro=PSGC[place], lcro_name=self.lcro_name(place, dreg),
                        l=c, place=place, hosp=hosp, twin=twin, order=grp.index(i), resv=u[i, 5], att=u[lead, 8],
                        resident=True)
            rows.append(base)
            if hosp:
                rate = P.BIRTH_DOUBLE if c != "KLW-01" else P.BIRTH_DOUBLE_SAME
                if u[lead, 6] < rate:
                    d2 = dreg + dt.timedelta(days=35 + int(u[lead, 7] * 295))
                    if d2 <= w1:
                        rows.append(dict(base, lcro=PSGC[c], lcro_name=self.lcro_name(c, d2), dreg=d2, dup=True,
                                         resv=(u[i, 5] + 0.41) % 1.0))
        self.truth["births"] = truth
        rows += self._nonresident_births(r, w0, w1)
        rows += self._old_births(r)
        df = self._birth_frame(rows, r)
        self._births = df
        return df

    def _nonresident_births(self, r, w0, w1):
        rows = []
        n = int(P.NONRES_BIRTHS_PER_YEAR * 1.8)
        for k in range(n):
            when = dt.date(2021, 6, 1) + dt.timedelta(days=int(r.integers(0, (P.END - dt.date(2021, 6, 1)).days)))
            delay = 1 + int(r.random() * 29) if r.random() < 0.85 else 31 + int(r.exponential(80))
            dreg = when + dt.timedelta(days=delay)
            if not (w0 <= dreg <= w1):
                continue
            rows.append(dict(child=-1, mother=-1, dob=when, dreg=dreg, lcro=PSGC["KLW-01"],
                             lcro_name=self.lcro_name("KLW-01", dreg), l=None, place="KLW-01", hosp=True, twin=False,
                             order=0, resv=r.random(), att=r.random(), resident=False,
                             prov=OTHER_PROVINCES[r.integers(len(OTHER_PROVINCES))], sex=int(r.random() < 0.512),
                             fn=int(r.integers(0, 70)), ln=int(r.integers(len(SURNAMES))), mn=int(r.integers(len(SURNAMES))),
                             mfn=int(r.integers(len(FEMALE))), mage=int(r.integers(17, 42))))
        return rows

    def _old_births(self, r):
        """births of earlier years registered in 2022 in the provincial late registration drive"""
        rows = []
        w = np.array([P.POP2020[c] for c in P.CODES], float)
        for k in range(P.LATE_OLD_BIRTHS_2022):
            c = P.CODES[int(r.choice(12, p=w / w.sum()))]
            dob = dt.date(2004, 1, 1) + dt.timedelta(days=int(r.integers(0, 17 * 365)))
            dreg = dt.date(2022, 1, 1) + dt.timedelta(days=int(r.integers(0, 365)))
            rows.append(dict(child=-1, mother=-1, dob=dob, dreg=dreg, lcro=PSGC[c], lcro_name=self.lcro_name(c, dreg),
                             l=c, place=c, hosp=False, twin=False, order=0, resv=r.random(), att=r.random(),
                             resident=True, sex=int(r.random() < 0.512), fn=int(r.integers(0, 70)),
                             ln=int(r.integers(len(SURNAMES))), mn=int(r.integers(len(SURNAMES))),
                             mfn=int(r.integers(len(FEMALE))), mage=int(r.integers(17, 42)) + (2022 - dob.year)))
        return rows

    def _birth_frame(self, rows, r):
        W = self.W
        out = []
        for x in rows:
            k = x["child"]
            if k >= 0:
                m = x["mother"]
                sex = int(W.sex[k])
                fn, mn, ln = self.fname(k), SURNAMES[self.middle[k]], SURNAMES[self.last[k]]
                mfn, mln = FEMALE[self.first[m]], SURNAMES[self.last[m]]
                mage = int((sim.days(x["dob"]) - W.birth[m]) / 365.2425)
                brgy = BARANGAYS[self.brgy[m]]
                ffn = MALE[(self.first[k] * 7 + self.last[k]) % len(MALE)]
            else:
                sex = x["sex"]
                fn = (MALE if sex == 1 else FEMALE)[x["fn"] % len(MALE if sex == 1 else FEMALE)]
                mn, ln = SURNAMES[x["mn"]], SURNAMES[x["ln"]]
                mfn, mln, mage = FEMALE[x["mfn"]], SURNAMES[x["mn"]], x["mage"]
                brgy = BARANGAYS[int(x["resv"] * len(BARANGAYS))]
                ffn = MALE[(x["fn"] * 7 + x["ln"]) % len(MALE)]
            if x["resident"]:
                res, prov = self.res_text(x["l"], x["dreg"], x["resv"]), PROV
            else:
                res, prov = OTHER_TOWN[x["prov"]], x["prov"]
            a = x["att"]
            if x["hosp"]:
                att, pob = ("PHYSICIAN" if a < 0.7 else "NURSE"), "HOSPITAL"
            else:
                att = "MIDWIFE" if a < 0.55 else ("PHYSICIAN" if a < 0.7 else ("NURSE" if a < 0.8 else "HILOT"))
                pob = "HOME" if att == "HILOT" or a > 0.9 else "LYING-IN / BIRTHING HOME"
            out.append(dict(
                REGISTRY_NO="", LCRO_CODE=x["lcro"], LCRO_NAME=x["lcro_name"], DATE_REGISTERED=iso(x["dreg"]),
                CHILD_FIRST_NAME=fn, CHILD_MIDDLE_NAME=mn, CHILD_LAST_NAME=ln, SEX="MALE" if sex == 1 else "FEMALE",
                DATE_OF_BIRTH=iso(x["dob"]), TYPE_OF_BIRTH="TWIN" if x["twin"] else "SINGLE",
                BIRTH_ORDER=("FIRST", "SECOND", "THIRD")[min(x["order"], 2)] if x["twin"] else "",
                PLACE_OF_BIRTH=pob, PLACE_OF_BIRTH_CITY_MUN=UPPER[x["place"]] if x["place"] in UPPER else "",
                MOTHER_FIRST_NAME=mfn, MOTHER_MAIDEN_LAST_NAME=mln, MOTHER_AGE=mage, MOTHER_RES_BARANGAY=brgy,
                MOTHER_RES_CITY_MUN=res, MOTHER_RES_PROVINCE=prov, FATHER_FIRST_NAME=ffn, FATHER_LAST_NAME=ln,
                ATTENDANT=att, LATE_REGISTRATION="Y" if (x["dreg"] - x["dob"]).days > 30 else "N",
                _l=x["l"] if x["resident"] else "", _dup=x.get("dup", False), _child=k))
        df = pd.DataFrame(out)
        df = df.sort_values(["LCRO_CODE", "DATE_REGISTERED", "CHILD_LAST_NAME", "CHILD_FIRST_NAME"],
                            kind="mergesort").reset_index(drop=True)
        seq, nos = {}, []
        for lc, d_ in zip(df["LCRO_CODE"], df["DATE_REGISTERED"]):
            key = (lc, d_[:4])
            seq[key] = seq.get(key, 0) + 1
            nos.append("%s-%05d" % (d_[:4], seq[key]))
        df["REGISTRY_NO"] = nos
        c, a, b = P.EXTRACT_DUP_BATCHES[1]
        m = (df["LCRO_CODE"] == PSGC[c]) & (df["DATE_REGISTERED"] >= a.isoformat()) & (df["DATE_REGISTERED"] <= b.isoformat())
        df = pd.concat([df, df[m]], ignore_index=True)
        df = df.sort_values(["LCRO_CODE", "DATE_REGISTERED", "REGISTRY_NO"], kind="mergesort").reset_index(drop=True)
        return df

    def birth_extract(self):
        return self.births().drop(columns=[c for c in self.births().columns if c.startswith("_")])

    # ------------------------------------------------------------------ the censuses
    def census_counts(self):
        """enumerated household population by LGU, sex and five-year age group, each census; coverage uniform by age"""
        if hasattr(self, "_census"):
            return self._census
        W = self.W
        r = np.random.default_rng([P.SEED, 5])
        out = {}
        for key, cd, K in (("2015", P.CENSUS1, P.K2015), ("2020", P.CENSUS2, P.K2020)):
            idx, lg, sx, ag = W.census[cd]
            enum = np.zeros(idx.size, bool)
            for i, c in enumerate(P.CODES):
                m = lg == i
                enum[m] = r.random(m.sum()) < K[c]
            out[key] = dict(idx=idx, lg=lg, sx=sx, ag=ag, enum=enum)
        self._census = out
        return out

    def census_table(self, year):
        C = self.census_counts()[year]
        g = np.minimum(C["ag"] // 5, 16)
        rows = []
        for i, c in enumerate(P.CODES):
            m = (C["lg"] == i) & C["enum"]
            male = np.bincount(g[m & (C["sx"] == 1)], minlength=17)
            fem = np.bincount(g[m & (C["sx"] == 0)], minlength=17)
            rows.append((c, male, fem))
        return rows

    def residence_tab(self):
        """the 2020 census's special tabulation: persons five years old and over by city or municipality of residence
        on 1 May 2020 and on 1 May 2015, age group and sex, for the province's residents and for persons enumerated
        elsewhere in the country who lived in the province in 2015"""
        W = self.W
        r = np.random.default_rng([P.SEED, 6])
        C = self.census_counts()["2020"]
        idx, lg, sx, ag, enum = C["idx"], C["lg"], C["sx"], C["ag"], C["enum"].copy()
        out_m = lg == sim.OUT
        enum[out_m] = r.random(out_m.sum()) < 0.982
        res = W.res2015[idx].astype(int)
        foreign = r.random(idx.size) < 0.08
        notstated = r.random(idx.size) < 0.009
        rows = {}
        for j in np.nonzero(enum & (ag >= 5))[0]:
            now, then = int(lg[j]), int(res[j])
            if now == sim.OUT:
                if not (0 <= then < 12):
                    continue
                where2020, where2015 = "ELSEWHERE IN THE PHILIPPINES", UPPER[P.CODES[then]]
            else:
                where2020 = UPPER[P.CODES[now]]
                if notstated[j]:
                    where2015 = "NOT STATED"
                elif then == now:
                    where2015 = "SAME CITY/MUNICIPALITY"
                elif 0 <= then < 12:
                    where2015 = UPPER[P.CODES[then]]
                elif then == sim.OUT:
                    where2015 = "OTHER PROVINCE"
                else:
                    where2015 = "FOREIGN COUNTRY" if foreign[j] else "OTHER PROVINCE"
            key = (where2020, where2015, AGE_GROUPS[min(int(ag[j]) // 5, 16)], "MALE" if sx[j] == 1 else "FEMALE")
            rows[key] = rows.get(key, 0) + 1
        df = pd.DataFrame([dict(CITY_MUN_2020=k[0], RESIDENCE_1MAY2015=k[1], AGE_GROUP=k[2], SEX=k[3], PERSONS=v)
                           for k, v in rows.items()])
        order2020 = {UPPER[c]: i for i, c in enumerate(P.CODES)}
        order2020["ELSEWHERE IN THE PHILIPPINES"] = 99
        df["_a"] = df["CITY_MUN_2020"].map(order2020)
        df["_g"] = df["AGE_GROUP"].map({g: i for i, g in enumerate(AGE_GROUPS)})
        df["_r"] = df["RESIDENCE_1MAY2015"].map(lambda s: (0 if s == "SAME CITY/MUNICIPALITY" else
                                                           (order2020.get(s, 50) + 1)))
        df = df.sort_values(["_a", "_r", "RESIDENCE_1MAY2015", "_g", "SEX"]).drop(columns=["_a", "_g", "_r"])
        return df.reset_index(drop=True)

    # ------------------------------------------------------------------ reference files
    def directory(self):
        inc = {"KLW-01": "1st", "KLW-02": "1st", "KLW-03": "1st", "KLW-04": "2nd", "KLW-05": "2nd", "KLW-06": "2nd",
               "KLW-07": "4th", "KLW-08": "3rd", "KLW-09": "3rd", "KLW-10": "1st", "KLW-11": "2nd", "KLW-12": "2nd"}
        nb = {"KLW-01": 44, "KLW-02": 36, "KLW-03": 31, "KLW-04": 28, "KLW-05": 27, "KLW-06": 25, "KLW-07": 22,
              "KLW-08": 26, "KLW-09": 29, "KLW-10": 33, "KLW-11": 24, "KLW-12": 30}
        rows = []
        for c in P.CODES:
            cls = "COMPONENT CITY" if c in ("KLW-01", "KLW-02") else "MUNICIPALITY"
            rows.append(dict(PSGC_CODE=PSGC[c], CITY_MUNICIPALITY=UPPER[c], CLASS=cls, INCOME_CLASS=inc[c],
                             BARANGAYS=nb[c], LCRO_CODE=PSGC[c], LCRO="LCRO " + UPPER[c],
                             CITYHOOD_EFFECTIVE=("1998-08-21" if c == "KLW-01" else
                                                 (P.CITYHOOD.isoformat() if c == "KLW-02" else "")),
                             FORMER_NAME=("SANTA CRUZ (MUNICIPALITY)" if c == "KLW-02" else "")))
        return pd.DataFrame(rows)

    def roster(self):
        rows = []
        for c in P.CODES:
            o = self.officer[c]
            off = "CITY HEALTH OFFICE" if c in ("KLW-01",) else "RURAL HEALTH UNIT"
            des = "City Health Officer" if c == "KLW-01" else "Municipal Health Officer"
            if c in P.VACANT:
                a, b = P.VACANT[c]
                rows.append(dict(CITY_MUN=UPPER[c], HEALTH_OFFICE=off, NAME=o["phys"], POSITION=des + " (physician)",
                                 FROM="2019-07-01", TO=(a - dt.timedelta(days=1)).isoformat(), REMARKS="resigned"))
                rows.append(dict(CITY_MUN=UPPER[c], HEALTH_OFFICE=off, NAME=o["nurse"], POSITION="Nurse III, officer-in-charge",
                                 FROM=a.isoformat(), TO=b.isoformat(), REMARKS="health officer post vacant"))
                if b < dt.date(2023, 3, 31):
                    rows.append(dict(CITY_MUN=UPPER[c], HEALTH_OFFICE=off, NAME=o["next"], POSITION=des + " (physician)",
                                     FROM=(b + dt.timedelta(days=1)).isoformat(), TO="", REMARKS="appointed"))
            else:
                rows.append(dict(CITY_MUN=UPPER[c], HEALTH_OFFICE=off, NAME=o["phys"], POSITION=des + " (physician)",
                                 FROM="2019-07-01", TO="", REMARKS=""))
            for nm, pos in self.staff[c]:
                rows.append(dict(CITY_MUN=UPPER[c], HEALTH_OFFICE=off, NAME=nm, POSITION=pos, FROM="2019-07-01", TO="",
                                 REMARKS=""))
        return pd.DataFrame(rows)

    def fhsis(self):
        """the health offices' monthly mortality reports (FHSIS): deaths the facilities and barangay health workers
        reported, a different and incomplete count; not used by the review"""
        W = self.W
        r = np.random.default_rng([P.SEED, 7])
        rate = {c: 0.55 + 0.35 * r.random() for c in P.CODES}
        cnt = {}
        lo, hi = sim.days(dt.date(2015, 1, 1)), sim.days(dt.date(2022, 12, 31))
        for p, d, l in W.deaths:
            if lo <= d <= hi and l < 12:
                when = D(d)
                infant = (d - W.birth[p]) < 365.2425
                k = (when.year, when.month, P.CODES[l])
                a = cnt.setdefault(k, [0, 0])
                a[0] += 1
                a[1] += int(infant)
        rows = []
        for (y, m, c), (n, ni) in sorted(cnt.items()):
            rows.append(dict(YEAR=y, MONTH=m, CITY_MUN=UPPER[c], DEATHS_REPORTED=int(r.binomial(n, rate[c])),
                             INFANT_DEATHS_REPORTED=int(r.binomial(ni, min(0.95, rate[c] + 0.05)))))
        return pd.DataFrame(rows)

    def staffing(self):
        r = np.random.default_rng([P.SEED, 8])
        rows = []
        for c in P.CODES:
            rows.append(dict(LCRO="LCRO " + UPPER[c], PERMANENT_STAFF=int(r.integers(2, 9)), JOB_ORDER_STAFF=int(r.integers(0, 6)),
                             COMPUTERS=int(r.integers(1, 7)), INTERNET=("FIBER" if r.random() < 0.6 else "MOBILE DATA"),
                             DOCUMENTS_AWAITING_ENCODING=int(r.integers(0, 900)),
                             BARANGAY_REGISTRATION_POINTS=int(r.integers(0, 12))))
        return pd.DataFrame(rows)
