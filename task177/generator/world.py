"""task177 world: the clean truth before any file is written.

Public side: Coopservir's payroll-deduction loans to public servants, 2017 to 2026, simulated month by month. A loan
is paid at source by the Tesoreria's central payroll; it falls behind almost only when the borrower leaves that
payroll with the loan open (about half of those loans reach 90 days past due a few months later), and a little through
a persistent loss of deduction margin. Temporary staff hold loans capped to mature before their contracts end.

Private side: the 38 employers that signed deduction agreements in 2025, their staff month by month, their payroll
registers, the members who joined and saved, and the 2,400 launch loans. Each employer's staff leave at its own rate.

The truth of the call: each launch loan's chance of being 90 days past due by 31 January 2028, from the true hazards.
"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as C

T0 = C.mi(*C.HIST_FROM)
TEND = C.mi(*C.DATA_END)
LAG_P = {3: 0.55, 4: 0.35, 5: 0.10}          # months from the first absent payroll to 90 days past due
FIRST_YEAR_MULT = 1.00                       # leaving is a little likelier in the first twelve months of service
RESID_EMBARGO = 0.00030                      # monthly start of a persistent margin loss (a court order takes priority)
EMBARGO_CONV = 0.75
UNPAID_LEAVE = 0.00010
SPORADIC_MARGIN = 0.0015
BUYOUT = 0.0060
TEMP_EARLY = 0.0035


def conv_prob(rem_ratio):
    """P(90 days past due | the borrower left the payroll with the loan open), rising gently with the balance still
    owed in months of net pay"""
    z = math.log(0.55 / 0.45) + 0.12 * (rem_ratio - 6.0) / 3.0
    return 1.0 / (1.0 + np.exp(-z))


# ----------------------------------------------------------------------------------------------------- public side
PLACES = ("Sorana", "Cumbrera", "Tamarales", "Piedralta", "Nuevo Cauzal", "Lomaverde", "San Telmo del Llano",
          "Vallehondo", "Arenisca", "Puerto Celeste", "Monteralto", "Las Garzas", "Rionegro Alto", "Bocachica",
          "Santa Ines", "Altovalle", "Cerro Pardo", "La Ensenada", "Mirasol", "Campoalegre")
MINISTRIES = ("Ministerio de Hacienda y Credito Publico", "Ministerio de Salud", "Ministerio de Educacion Nacional",
              "Ministerio de Transporte", "Ministerio de Agricultura", "Ministerio de Justicia", "Ministerio del Interior",
              "Ministerio de Trabajo", "Ministerio de Ambiente", "Ministerio de Comercio", "Registraduria Nacional",
              "Direccion de Impuestos y Aduanas", "Instituto Geografico Nacional", "Servicio Nacional de Aprendizaje",
              "Instituto de Bienestar Familiar", "Policia Civil de Transito", "Defensoria del Pueblo",
              "Contraloria General", "Superintendencia Financiera", "Instituto Nacional de Vias")


def agencies():
    rng = C.stream("agencies")
    out = []
    code = 1100
    plan = (("national", 20), ("territorial", 18), ("health", 12), ("education", 10))
    terr_i, hosp_i, edu_i = 0, 0, 0
    for typ, n in plan:
        for j in range(n):
            code += int(rng.integers(3, 40))
            if typ == "national":
                name = MINISTRIES[j]
            elif typ == "territorial":
                p = PLACES[terr_i % len(PLACES)]
                name = ("Gobernacion de " if terr_i % 3 == 0 else "Alcaldia de ") + p
                terr_i += 1
            elif typ == "health":
                p = PLACES[(hosp_i * 7 + 3) % len(PLACES)]
                name = ("Hospital Departamental de " if hosp_i % 2 == 0 else "ESE Hospital Regional de ") + p
                hosp_i += 1
            else:
                p = PLACES[(edu_i * 11 + 5) % len(PLACES)]
                name = ("Universidad Publica de " if edu_i % 3 == 0 else "Secretaria de Educacion de ") + p
                edu_i += 1
            h = float(rng.uniform(0.0013, 0.0045))
            if typ in ("territorial", "health") and rng.random() < 0.55:
                temp = float(rng.uniform(0.20, 0.55))
            elif rng.random() < 0.15:
                temp = float(rng.uniform(0.15, 0.35))
            else:
                temp = float(rng.uniform(0.0, 0.08))
            size = float(rng.lognormal(0, 0.7)) * (2.2 if typ == "education" else 1.0)
            out.append(dict(code="UE-%04d" % code, name=name, type=typ, h=h, temp=temp, size=size))
    return out


def public_loans():
    """every public loan disbursed January 2017 to December 2026 with its monthly history"""
    A = agencies()
    rng = C.stream("public_loans")
    w = np.array([a["size"] for a in A])
    w = w / w.sum()
    months = np.arange(T0, TEND + 1)
    per = (360 + 6.0 * (months - T0) / 12.0) * (1 + 0.08 * np.sin(2 * np.pi * (months % 12) / 12.0))
    counts = rng.poisson(per)
    n = int(counts.sum())
    disb = np.repeat(months, counts)
    ag = rng.choice(len(A), n, p=w)
    temp = rng.random(n) < np.array([A[i]["temp"] for i in ag])
    ten0 = np.where(temp, 3 + rng.gamma(1.5, 10, n), 6 + rng.gamma(2.0, 55, n)).astype(int)
    age = np.clip(rng.normal(43, 9, n), 22, 62).astype(int)
    pay = np.round(np.exp(rng.normal(np.log(4_300_000), 0.36, n) + 0.006 * (age - 43)), -3)
    to_end = rng.integers(9, 37, n)
    term = rng.choice([24, 36, 48, 60, 72, 84], n, p=[0.10, 0.18, 0.22, 0.22, 0.16, 0.12])
    term = np.where(temp, np.minimum(term, to_end - 1), term)
    term = np.maximum(term, 6)
    rate = np.round(rng.uniform(0.0105, 0.0145, n) / 0.0005) * 0.0005
    inst = np.round(pay * rng.uniform(0.12, 0.30, n), -3)
    principal = np.round(inst * (1 - (1 + rate) ** -term) / rate, -3)
    inst = np.round(principal * rate / (1 - (1 + rate) ** -term), 0)
    h_ag = np.array([A[i]["h"] for i in ag])

    # monthly histories
    status = np.zeros(n, int)        # 0 open on payroll, 1 matured, 2 bought out, 3 default, 4 direct billing
    end_m = np.full(n, -1)           # month the loan closed or defaulted or moved to direct billing
    left_m = np.full(n, -1)          # first month absent from the payroll with the loan open
    dflt_m = np.full(n, -1)
    dflt_route = np.full(n, "", dtype=object)
    returns = []                     # (loan index, month, code)
    for k in range(1, 85):
        cal = disb + k
        alive = (status == 0) & (k <= term) & (cal <= TEND) & (dflt_m < 0)
        idx = np.where(alive)[0]
        if len(idx):
            u = rng.random((len(idx), 6))
            bo = u[:, 0] < BUYOUT
            hz = np.where(temp[idx], TEMP_EARLY,
                          h_ag[idx] * np.where(ten0[idx] + k < 12, FIRST_YEAR_MULT, 1.0))
            lv = (~bo) & (u[:, 1] < hz)
            emb = (~bo) & (~lv) & (u[:, 2] < RESID_EMBARGO)
            ul = (~bo) & (~lv) & (~emb) & (u[:, 3] < UNPAID_LEAVE)
            sp = (~bo) & (~lv) & (~emb) & (~ul) & (u[:, 4] < SPORADIC_MARGIN)
            for j in np.where(bo)[0]:
                i = idx[j]
                status[i] = 2
                end_m[i] = cal[i]
            for j in np.where(lv)[0]:
                i = idx[j]
                c = cal[i]
                left_m[i] = c
                rem = (term[i] - k + 1) * inst[i] / pay[i]
                if rng.random() < conv_prob(rem):
                    L = int(rng.choice([3, 4, 5], p=[LAG_P[3], LAG_P[4], LAG_P[5]]))
                    for t in range(c, min(c + 3, TEND + 1)):
                        returns.append((i, t, "SIN SALARIO"))
                    dflt_m[i] = c + L
                    dflt_route[i] = "left"
                    status[i] = 3
                    end_m[i] = c + L
                else:
                    for t in range(c, min(c + 2, TEND + 1)):
                        returns.append((i, t, "SIN SALARIO"))
                    status[i] = 4
                    end_m[i] = c + 2
            for j in np.where(emb)[0]:
                i = idx[j]
                c = cal[i]
                if rng.random() < EMBARGO_CONV:
                    L = int(rng.choice([3, 4], p=[0.7, 0.3]))
                    for t in range(c, min(c + 3, TEND + 1)):
                        returns.append((i, t, "SIN CUPO"))
                    dflt_m[i] = c + L
                    dflt_route[i] = "margin"
                    status[i] = 3
                    end_m[i] = c + L
                else:
                    for t in range(c, min(c + 2, TEND + 1)):
                        returns.append((i, t, "SIN CUPO"))
            for j in np.where(ul)[0]:
                i = idx[j]
                c = cal[i]
                D = int(rng.choice([1, 2, 3], p=[0.5, 0.35, 0.15]))
                for t in range(c, min(c + D, TEND + 1)):
                    returns.append((i, t, "SIN SALARIO"))
            for j in np.where(sp)[0]:
                i = idx[j]
                returns.append((i, int(cal[i]), "SIN CUPO"))
        mat = (status == 0) & (k == term) & (disb + k <= TEND) & (dflt_m < 0)
        status[mat] = 1
        end_m[mat] = disb[mat] + k
    # defaults scheduled beyond the data end did not happen inside the record
    beyond = (dflt_m > TEND)
    dflt_obs = np.where(beyond, -1, dflt_m)
    status_obs = np.where(beyond, 0, status)
    # members: national ids, some members hold a second loan later
    ids = rng.choice(np.arange(10_000_000, 99_999_999), n, replace=False)
    hire = disb - ten0
    birth = (disb // 12) - age
    return dict(A=A, n=n, disb=disb, ag=ag, temp=temp, ten0=ten0, age=age, pay=pay, term=term, rate=rate, inst=inst,
                principal=principal, status=status_obs, end_m=end_m, left_m=left_m, dflt_m=dflt_obs,
                dflt_route=dflt_route, returns=returns, member=ids, hire=hire, birth=birth, h_ag=h_ag)


# ---------------------------------------------------------------------------------------------------- private side
EMPLOYERS = (
    # name, sector, pay frequency, staff at agreement, monthly leaving hazard, group
    ("Telnova Servicios de Contacto S.A.S.", "contact centres", "F", 907, 0.0639, ""),
    ("Interlaza BPO S.A.S.", "contact centres", "F", 669, 0.0594, ""),
    ("Atencion Integral del Caribe S.A.", "contact centres", "F", 400, 0.0532, "G3"),
    ("Conecta Cumbrera S.A.S.", "contact centres", "M", 302, 0.0576, ""),
    ("Voxpunto Andina S.A.S.", "contact centres", "F", 496, 0.0550, ""),
    ("Callmar Soluciones S.A.S.", "contact centres", "M", 259, 0.0505, ""),
    ("Almacenes La Garza S.A.", "retail chains", "F", 380, 0.0254, "G1"),
    ("Supertiendas Mirasol S.A.", "retail chains", "F", 300, 0.0243, ""),
    ("Droguerias Piedralta S.A.S.", "retail chains", "M", 165, 0.0213, ""),
    ("Calzado Velasquez y Cia. S.A.S.", "retail chains", "M", 110, 0.0231, ""),
    ("Hogar y Ferreteria El Puente S.A.S.", "retail chains", "F", 140, 0.0249, ""),
    ("Comercializadora Tamarales S.A.", "retail chains", "M", 175, 0.0219, ""),
    ("Moda Urbana Sorana S.A.S.", "retail chains", "F", 95, 0.0274, ""),
    ("Autoservicio Lomaverde S.A.S.", "retail chains", "M", 130, 0.0237, ""),
    ("Seguridad Atalaya Ltda.", "security services", "F", 476, 0.0287, ""),
    ("Vigilancia La Garza Ltda.", "security services", "F", 210, 0.0274, "G1"),
    ("Proteccion Privada del Llano S.A.S.", "security services", "F", 308, 0.0306, ""),
    ("Escoltas y Custodia Monteralto Ltda.", "security services", "M", 133, 0.0253, ""),
    ("Centinela Servicios Integrales S.A.S.", "security services", "F", 252, 0.0293, ""),
    ("Guardianes de Altovalle Ltda.", "security services", "M", 161, 0.0268, ""),
    ("Transportes Rapido Cumbrera S.A.", "logistics and courier", "M", 260, 0.0226, "G2"),
    ("Mensajeria Expressa del Valle S.A.S.", "logistics and courier", "F", 210, 0.0260, ""),
    ("Logistica Puerto Celeste S.A.S.", "logistics and courier", "M", 190, 0.0211, ""),
    ("Envios Ya Valdemora S.A.S.", "logistics and courier", "F", 150, 0.0274, ""),
    ("Bodegas y Distribucion Arenisca S.A.", "logistics and courier", "M", 130, 0.0197, ""),
    ("Carga Segura Vallehondo S.A.S.", "logistics and courier", "M", 105, 0.0233, ""),
    ("Lacteos Rionegro Alto S.A.", "food processing", "M", 290, 0.0201, "G2"),
    ("Frigorifico Las Garzas S.A.", "food processing", "M", 240, 0.0226, ""),
    ("Panificadora San Telmo S.A.S.", "food processing", "F", 160, 0.0247, ""),
    ("Conservas del Mar Bocachica S.A.", "food processing", "M", 200, 0.0209, ""),
    ("Avicola Campoalegre S.A.S.", "food processing", "M", 175, 0.0216, ""),
    ("Molinos Cerro Pardo S.A.", "food processing", "M", 120, 0.0186, ""),
    ("Bebidas La Ensenada S.A.S.", "food processing", "F", 140, 0.0240, ""),
    ("Clinica Santa Ines S.A.", "private clinics", "M", 310, 0.0161, "G3"),
    ("Centro Medico Altamira de Sorana S.A.S.", "private clinics", "M", 180, 0.0153, ""),
    ("Clinica Oftalmologica del Norte S.A.S.", "private clinics", "M", 95, 0.0143, ""),
    ("Laboratorio Clinico Vallehondo S.A.S.", "private clinics", "F", 120, 0.0171, ""),
    ("Unidad Renal Piedralta S.A.S.", "private clinics", "M", 85, 0.0153, ""),
)
GROUP_PARENT = {"G1": "Almacenes La Garza S.A.", "G2": "Lacteos Rionegro Alto S.A.", "G3": "Clinica Santa Ines S.A."}


def employers():
    rng = C.stream("employers")
    out = []
    used = set()
    for j, (name, sector, freq, staff, h, grp) in enumerate(EMPLOYERS):
        while True:
            base = int(rng.integers(800_100_000, 901_999_999))
            if base not in used:
                used.add(base)
                break
        start = C.mi(2025, int(rng.choice([1, 1, 2, 2, 3, 3, 4, 5, 6])))
        out.append(dict(i=j, name=name, sector=sector, freq=freq, staff=staff, h=h, group=grp, nit_base=base,
                        nit=C.fmt_nit(base), start=start,
                        pay_day=int(rng.choice([25, 28, 30])) if freq == "M" else 0,
                        salary_mu=float({"contact centres": 1.75, "retail chains": 1.80, "security services": 1.95,
                                         "logistics and courier": 2.15, "food processing": 2.05,
                                         "private clinics": 2.70}[sector])))
    return out


def private_staff():
    """each employer's staff month by month from twelve months before its agreement to December 2026"""
    E = employers()
    rng = C.stream("private_staff")
    people = []          # dict per employment spell
    pid = 0
    used_ids = set()

    def new_id():
        while True:
            x = int(rng.integers(1_000_000_000, 1_299_999_999)) if rng.random() < 0.55 else int(rng.integers(20_000_000, 99_999_999))
            if x not in used_ids:
                used_ids.add(x)
                return x

    for e in E:
        t_first = e["start"] - 12
        staff = []
        for _ in range(e["staff"]):
            ten = int(6 + rng.gamma(1.4, 24))
            staff.append(dict(pid=pid, emp=e["i"], id=new_id(), hire=t_first - ten, leave=None, unpaid=[],
                              base=float(np.round(np.exp(rng.normal(np.log(e["salary_mu"] * 1_000_000), 0.22)), -3))))
            pid += 1
        for t in range(t_first, TEND + 1):
            cur = [s for s in staff if s["leave"] is None]
            for s in cur:
                hz = e["h"] * (FIRST_YEAR_MULT if t - s["hire"] < 12 else 1.0)
                if rng.random() < hz:
                    s["leave"] = t            # last month worked (settlement paid in this month)
                elif rng.random() < UNPAID_LEAVE:
                    s["unpaid"].append((t + 1, int(rng.choice([1, 2]))))
            n_now = sum(1 for s in staff if s["leave"] is None)
            target = e["staff"] * (1 + 0.04 * (t - t_first) / 12)
            hires = int(rng.poisson(max(0.0, target - n_now) * 0.8 + 0.2))
            for _ in range(hires):
                staff.append(dict(pid=pid, emp=e["i"], id=new_id(), hire=t, leave=None, unpaid=[],
                                  base=float(np.round(np.exp(rng.normal(np.log(e["salary_mu"] * 1_000_000), 0.20)), -3))))
                pid += 1
        people.extend(staff)
    return E, people


def membership(E, people):
    """who joined the cooperative and when, their monthly savings, and the launch borrowers"""
    rng = C.stream("membership")
    for s in people:
        e = E[s["emp"]]
        s["join"] = None
        first = max(e["start"], s["hire"] + 3)
        last = s["leave"] if s["leave"] is not None else TEND
        if first > last:
            continue
        p0 = 0.62 if s["hire"] < e["start"] else 0.50
        if rng.random() < p0:
            j = first + int(rng.integers(0, 4)) if s["hire"] < e["start"] else first + int(rng.integers(1, 8))
            if j <= last:
                s["join"] = j
                s["saving"] = float(max(20_000, np.round(s["base"] * rng.choice([0.02, 0.03, 0.04]), -3)))
    elig = [s for s in people if s["join"] is not None and s["leave"] is None and s["join"] <= C.mi(2026, 1)]
    quota = {"contact centres": 385, "retail chains": 505, "security services": 355, "logistics and courier": 400,
             "food processing": 465, "private clinics": 290}
    borrowers = []
    for sec in C.SECTORS:
        pool = [s for s in elig if E[s["emp"]]["sector"] == sec]
        sel = rng.choice(len(pool), quota[sec], replace=False)
        sel.sort()
        borrowers.extend(pool[i] for i in sel)
    borrowers.sort(key=lambda s: s["pid"])
    for s in borrowers:
        s["term"] = int(rng.choice([12, 24, 36, 48, 60], p=[0.08, 0.22, 0.30, 0.25, 0.15]))
        rng.uniform(0.0135, 0.0175)
        s["rate"] = {12: 0.0149, 24: 0.0149, 36: 0.0159, 48: 0.0165, 60: 0.0172}[s["term"]]
        net = s["base"] * 0.88
        inst = round(net * float(rng.uniform(0.10, 0.29)), -3)
        s["principal"] = round(inst * (1 - (1 + s["rate"]) ** -s["term"]) / s["rate"], -3)
        s["inst"] = round(s["principal"] * s["rate"] / (1 - (1 + s["rate"]) ** -s["term"]), 0)
        s["net"] = net
    return borrowers


def launch_truth(E, borrowers):
    """each launch loan's chance of 90 days past due at a month-end up to 31 January 2028 under the true hazards.
    Month 1 is February 2027 (the first deduction); a borrower whose last month worked is m misses the deduction of
    month m + 1 first and reaches 90 days past due L months after that; a margin loss starting in month c reaches it
    L months later."""
    out = []
    for s in borrowers:
        e = E[s["emp"]]
        h = e["h"]
        surv = 1.0
        p = 0.0
        for m in range(1, 13):
            c = m + 1
            rem = (s["term"] - c + 1) * s["inst"] / s["net"]
            lagok = sum(v for L, v in LAG_P.items() if c + L <= 12)
            p += surv * h * conv_prob(rem) * lagok
            emb = sum(v for L, v in ((3, 0.7), (4, 0.3)) if m + L <= 12)
            p += surv * (1 - h) * RESID_EMBARGO * EMBARGO_CONV * emb
            surv *= (1 - h) * (1 - RESID_EMBARGO)
        out.append(p)
    return np.array(out)


_CACHE = {}


def world():
    if "w" not in _CACHE:
        P = public_loans()
        E, people = private_staff()
        B = membership(E, people)
        tr = launch_truth(E, B)
        _CACHE["w"] = dict(P=P, E=E, people=people, B=B, truth=tr)
    return _CACHE["w"]


if __name__ == "__main__":
    W = world()
    P = W["P"]
    print("public loans", P["n"], "returns", len(P["returns"]))
    d12 = (P["dflt_m"] >= 0) & (P["dflt_m"] <= P["disb"] + 12)
    ok = P["disb"] <= TEND - 12
    print("public 12m default", d12[ok].mean())
    print("people", len(W["people"]), "launch", len(W["B"]), "truth", W["truth"].sum())
    for sec in C.SECTORS:
        v = [p for p, s in zip(W["truth"], W["B"]) if W["E"][s["emp"]]["sector"] == sec]
        print("  %-24s n=%4d  %.1f" % (sec, len(v), sum(v)))
