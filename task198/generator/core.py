"""task198 generating process: the clean truth the pack is cut from.

One row per member-service case.
Waits come from the standard G/G/s heavy-traffic delay formula at each queue-quarter's own
offered load and staffed positions, so the pack's service levels are what a queue of that size
at that load produces."""
import hashlib
import math
from datetime import date, timedelta
import numpy as np

AVAIL = 0.88
MINS_PER_DAY = 420.0
EXTRACT = date(2026, 4, 30)
HSIG = 0.55

_RAW = {
 2022:["01-03","03-17","03-18","04-18","05-02","06-06","08-01","10-31","12-25","12-26","12-27"],
 2023:["01-02","02-06","03-17","04-10","05-01","06-05","08-07","10-30","12-25","12-26"],
 2024:["01-01","02-05","03-18","04-01","05-06","06-03","08-05","10-28","12-25","12-26"],
 2025:["01-01","02-03","03-17","04-21","05-05","06-02","08-04","10-27","12-25","12-26"],
 2026:["01-01","02-02","03-17","04-06","05-04","06-01","08-03","10-26","12-25","12-28"],
}
HOL = {date(y, int(d[:2]), int(d[3:])) for y, ds in _RAW.items() for d in ds}
WD = []
_d = date(2022, 4, 1)
while _d <= date(2026, 12, 31):
    if _d.weekday() < 5 and _d not in HOL:
        WD.append(_d)
    _d += timedelta(days=1)
WD_IX = {d: i for i, d in enumerate(WD)}
EX_IX = max(i for i, d in enumerate(WD) if d <= EXTRACT)

# positions and volume multiplier by fiscal year FY2023..FY2026
QUEUES = {
 "RQ":dict(nm="Retirement quotations",   tgt=12,mpc=430,hmed=2.6,cv2=3.2,pos=[12,12,12,12],vol=[1,1,1,1],
           occ=.9175,amp=.017,k26=.30,p_am=.18,am_med=3.0),
 "RS":dict(nm="Retirement settlements",  tgt=20,mpc=660,hmed=4.4,cv2=2.4,pos=[9,9,9,9],vol=[1,1,1,1],
           occ=.9220,amp=.013,k26=.35,p_am=.26,am_med=5.0),
 "TO":dict(nm="Transfers out",           tgt=15,mpc=560,hmed=4.2,cv2=2.4,pos=[11,11,11,11],vol=[1,1,1,1],
           occ=.9270,amp=.022,k26=.95,p_am=.30,am_med=6.0),
 "TI":dict(nm="Transfers in",            tgt=15,mpc=640,hmed=3.2,cv2=2.4,pos=[5,5,5,5],vol=[1,1,1,1],
           occ=.9060,amp=.026,k26=.95,p_am=.56,am_med=10.5),
 "DB":dict(nm="Death benefits",          tgt=25,mpc=980,hmed=6.5,cv2=1.8,pos=[5,5,5,5],vol=[1,1,1,1],
           occ=.9070,amp=.014,k26=.25,p_am=.46,am_med=11.0),
 "LO":dict(nm="Leaver options",          tgt=10,mpc=300,hmed=2.2,cv2=3.6,pos=[13,13,13,13],vol=[1,1,1,1],
           occ=.9160,amp=.013,k26=.30,p_am=.15,am_med=2.5),
 "DC":dict(nm="Member data corrections", tgt=8, mpc=360,hmed=1.9,cv2=3.2,pos=[5,14,14,5],vol=[1.0,2.8,2.8,1.0],
           occ=.9295,amp=.011,k26=.10,p_am=.12,am_med=2.0),
 "IS":dict(nm="Investment switches",     tgt=6, mpc=240,hmed=1.3,cv2=3.2,pos=[4,4,4,4],vol=[1,1,1,1],
           occ=.9110,amp=.028,k26=.95,p_am=.08,am_med=1.5),
 "CQ":dict(nm="Contribution queries",    tgt=6, mpc=215,hmed=1.4,cv2=4.0,pos=[16,16,16,16],vol=[1,1,1,1],
           occ=.9275,amp=.012,k26=.92,p_am=.10,am_med=2.0),
}
# Process drift from FY2026 Q1: elapsed days the queue's cases spend that its own offered load
# and staffed positions do not account for.
ANOM = dict(code="CQ", from_q=12, extra_med=2.05, share=0.44)
ANOM2 = None
PAT = [0.10,-0.95,-0.40,0.98, 0.18,-0.88,-0.30,1.00, 0.14,-0.92,-0.34,0.96]
P26 = [0.04,-0.06,0.00,0.05]

def wq(s, rho, m, cv2):
    return cv2 / 2.0 * rho ** (math.sqrt(2.0 * (s + 1.0)) - 1.0) / (s * (1.0 - rho)) * m

def qbounds(qi):
    y = 2022 + qi // 4; q = qi % 4
    sm, em, last = [4,7,10,1][q], [6,9,12,3][q], [30,30,31,31][q]
    yy = y + (1 if q == 3 else 0)
    return date(yy, sm, 1), date(yy, em, last)

def add_wd(d0, n):
    return WD[min(WD_IX[d0] + int(math.ceil(n)), len(WD) - 1)]

def build(seed=19980417):
    rng = np.random.default_rng(seed)
    cases, panel = [], []
    for code, q in QUEUES.items():
        m = q["mpc"] / (MINS_PER_DAY * AVAIL)
        for qi in range(16):
            fy = qi // 4
            pos = q["pos"][fy]
            occ = q["occ"] + q["amp"] * (PAT[qi] if qi < 12 else (q["k26"] + P26[qi - 12]))
            s_, e_ = qbounds(qi)
            wdays = [d for d in WD if s_ <= d <= e_]
            load = occ * pos                      # offered load in positions-equivalents
            n = int(round(load * len(wdays) / m))  # cases received
            w_mean = wq(pos, occ, m, q["cv2"])
            idx = rng.integers(0, len(wdays), n)
            wait = rng.gamma(0.9, w_mean / 0.9, n)
            hand = q["hmed"] * np.exp(HSIG * rng.standard_normal(n))
            extra = np.zeros(n)
            for A in (A_ for A_ in (ANOM, ANOM2) if A_):
                if code == A["code"] and qi >= A["from_q"]:
                    extra = np.where(rng.random(n) < A["share"],
                                     A["extra_med"] * np.exp(0.6 * rng.standard_normal(n)), 0.0)
            am = np.where(rng.random(n) < q["p_am"],
                          q["am_med"] * np.exp(0.7 * rng.standard_normal(n)), 0.0)
            net = wait + hand + extra
            for k in range(n):
                rec = wdays[idx[k]]
                ans = add_wd(rec, net[k] + am[k])
                op = ans > EXTRACT
                clock = (EX_IX - WD_IX[rec] - am[k]) if op else net[k]
                cases.append(dict(code=code, qi=qi, rec=rec, net=net[k], am=am[k],
                                  gross=net[k] + am[k], ans=None if op else ans,
                                  tgt=q["tgt"], open=op, late=bool(clock > q["tgt"])))
            panel.append(dict(code=code, qi=qi, fy=2023 + fy, pos=pos, occ=occ, load=load,
                              m=m, cases=n, tgt=q["tgt"], w_mean=w_mean))
    return cases, panel


# --------------------------------------------------------------------------------------
# Ask-side truth: scheme assignment, the scheme billing extract and the schemes register.
# None of this is read by the main call, which uses only the case record, the roster, the
# work-measurement study, the standard, the framework, the queue reference and the holidays.
# --------------------------------------------------------------------------------------

FY26 = (12, 15)
CHARGEABLE = ["RQ", "RS", "TO", "TI", "DB", "DC"]
FEE = {           # per chargeable case, EUR: (to 2025-09-30, from 2025-10-01)
    "RQ": (46.00, 48.50), "RS": (88.00, 92.50), "TO": (74.00, 78.00),
    "TI": (62.00, 65.00), "DB": (155.00, 162.50), "DC": (29.00, 30.50),
}
RATE_SWITCH = date(2025, 10, 1)
TRUST = "RMT-000"
TRUST_SUBS = ["MT-CEN", "MT-S01", "MT-S02", "MT-S03", "MT-S04"]
TRUST_MEMBERS = 41789          # active members of the whole trust at 31 March 2026
CONSOLIDATED = 3               # the participating schemes billed on one consolidated statement


def schemes():
    """(code, name, weight, participating_code, active_members or None) for every case-log code."""
    out = []
    sub_w = [0.062, 0.043, 0.040, 0.038, 0.036]
    sub_nm = ["Rathbroe Master Trust - Central Section",
              "Castlerea Dairies Pension Plan Section",
              "Lissanure Textiles Pension Plan Section",
              "Ballyhale Freight Pension Plan Section",
              "Glennamona Foods Pension Plan Section"]
    for c, w, nm in zip(TRUST_SUBS, sub_w, sub_nm):
        out.append((c, nm, w, TRUST, None))
    names = ["Shanakill Industries", "Drumacool Engineering", "Kilbaylet Retail", "Monavalley Plastics",
             "Carrowbeg Hotels", "Tullowmore Printing", "Ardnacrusha Metals", "Rossanure Haulage",
             "Clonmacken Chemicals", "Derrygonnelly Timber", "Inchicronan Glass", "Knockaderry Dairy",
             "Lisnageer Packaging", "Moyvalley Components", "Nurneyboro Foods", "Oughterard Marine",
             "Portumna Joinery", "Rathduff Paper", "Shillelagh Tooling", "Templemartin Fabrics",
             "Urlingford Electrics", "Ventry Shipping", "Woodfordbridge Care", "Aghavannagh Mills",
             "Bunlahinch Stores", "Cahermurphy Pumps", "Doonbeg Coaches", "Emlaghmore Bakery",
             "Fenagh Instruments", "Gortnahoe Seating", "Hollymount Signs", "Inagh Valves",
             "Kinnegad Ropes", "Lackamore Boards", "Mullinahone Tanks", "Newtowncashel Pipes",
             "Oylegate Blinds", "Pollagh Castings", "Raheenagh Linens", "Stradbally Gears",
             "Taghmon Lifts", "Upperchurch Doors", "Villierstown Frames", "Whitegate Looms"]
    mem = [9402, 7101, 5904, 5197, 4598, 4098, 3698, 3298, 2993, 2700, 2450, 2200, 2000, 1850,
           1700, 1560, 1440, 1330, 1230, 1140, 1055, 980, 910, 845, 790, 735, 685, 640, 600, 560,
           525, 495, 465, 435, 410, 385, 365, 345, 325, 305, 290, 275, 260, 245]
    w = [0.071, 0.055, 0.045, 0.038, 0.033, 0.029, 0.026, 0.023, 0.021, 0.0163, 0.0152, 0.014,
         0.0148, 0.0137, 0.0127, 0.0118, 0.0110, 0.0102, 0.0095, 0.0089, 0.0083, 0.0077, 0.0072,
         0.0067, 0.0063, 0.0059, 0.0055, 0.0051, 0.0048, 0.0045, 0.0042, 0.0039, 0.0037, 0.0034,
         0.0032, 0.0030, 0.0028, 0.0026, 0.0025, 0.0023, 0.0022, 0.0020, 0.0019, 0.0018]
    for i, nm in enumerate(names):
        out.append(("SC-%03d" % (i + 1), nm + " Pension Scheme", w[i], "SC-%03d" % (i + 1), mem[i]))
    return out


def assign_schemes(cases, seed=4180029):
    """Attach a scheme code to every case. Deterministic, independent of the queue draw."""
    rng = np.random.default_rng(seed)
    sch = schemes()
    codes = [s[0] for s in sch]
    w = np.array([s[2] for s in sch], dtype=float)
    w = w / w.sum()
    pick = rng.choice(len(codes), size=len(cases), p=w)
    for c, i in zip(cases, pick):
        c["scheme"] = codes[i]
    return sch


def fee_for(queue, d):
    lo, hi = FEE[queue]
    return hi if d >= RATE_SWITCH else lo


def billing_lines(cases, sch):
    """One row per billing line. Lines for the three largest participating schemes are the
    consolidated monthly statement: one line per case type per month covering every chargeable
    case completed for that scheme in the month. Every other scheme is billed a line per case."""
    part = {}
    for code, nm, w, pc, mem in sch:
        part[code] = pc
    size = {}
    for c in cases:
        if FY26[0] <= c["qi"] <= FY26[1]:
            size[part[c["scheme"]]] = size.get(part[c["scheme"]], 0) + 1
    big = {p for p, _ in sorted(size.items(), key=lambda kv: -kv[1])[:CONSOLIDATED]}
    bundles, singles = {}, []
    for c in cases:
        if not (FY26[0] <= c["qi"] <= FY26[1]) or c["code"] not in CHARGEABLE or c["open"]:
            continue
        p = part[c["scheme"]]
        if p in big:
            key = (p, c["code"], c["ans"].year, c["ans"].month)
            bundles.setdefault(key, []).append(c)
        else:
            singles.append(c)
    rows = []
    for (p, q, y, mo), grp in sorted(bundles.items()):
        d = max(x["ans"] for x in grp)
        rows.append(dict(scheme=p, queue=q, billed=d, cases=len(grp),
                         fee=round(fee_for(q, d) * len(grp), 2), consolidated=True))
    for c in sorted(singles, key=lambda x: (x["ans"], x["scheme"], x["code"])):
        rows.append(dict(scheme=part[c["scheme"]], queue=c["code"], billed=c["ans"], cases=1,
                         fee=round(fee_for(c["code"], c["ans"]), 2), consolidated=False))
    rows.sort(key=lambda r: (r["billed"], r["scheme"], r["queue"]))
    return rows, big


def fiscal_quarter(d):
    q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[d.month]
    fy = d.year + (1 if d.month >= 4 else 0)
    return fy, q


# Sponsor groups: where one sponsoring employer returns for more than one of its schemes, the
# register carries the group's total active members against each of that sponsor's schemes.
# The trustee membership statement carries the true per-scheme figure at 31 March 2026.
SPONSOR_GROUPS = [
    ("Shanakill Group", ["SC-001", "SC-007", "SC-013"]),
    ("Drumacool Holdings", ["SC-002", "SC-009"]),
    ("Kilbaylet Group", ["SC-003", "SC-011", "SC-018"]),
    ("Monavalley Industries", ["SC-004", "SC-015"]),
    ("Carrowbeg Leisure", ["SC-005", "SC-021"]),
    ("Tullowmore Group", ["SC-006", "SC-026"]),
    ("Ardnacrusha Group", ["SC-008", "SC-031"]),
    ("Rossanure Group", ["SC-010", "SC-036"]),
]


def register_and_trustee():
    """(register rows, trustee rows). register.active_members is the figure as returned by the
    sponsor, which for a grouped return is the group's total; trustee rows carry the true
    per-scheme active members at 31 March 2026."""
    sch = schemes()
    true_mem = {code: mem for code, nm, w, pc, mem in sch if mem is not None}
    true_mem[TRUST] = TRUST_MEMBERS
    names = {pc: nm for code, nm, w, pc, mem in sch if mem is not None}
    names[TRUST] = "Rathbroe Master Trust"
    grp_of, grp_total = {}, {}
    for gname, members in SPONSOR_GROUPS:
        tot = sum(true_mem[c] for c in members)
        grp_total[gname] = tot
        for c in members:
            grp_of[c] = gname
    reg, tru = [], []
    for code in sorted(true_mem):
        g = grp_of.get(code)
        # the master trust's membership is returned by its own trustees rather than by a
        # sponsoring employer, so the participating scheme register carries no figure for it
        reg.append(dict(scheme_code=code, scheme_name=names[code],
                        sponsor=g or ("Rathbroe Master Trust, trustee return" if code == TRUST
                                      else names[code].replace(" Pension Scheme", "")),
                        active_members=("" if code == TRUST
                                        else (grp_total[g] if g else true_mem[code])),
                        return_basis=("trustee return" if code == TRUST
                                      else ("group return" if g else "scheme return"))))
        # the trustee statement reports active membership split by contribution status, as a
        # scheme return does; the active total is the two parts together
        h = int(hashlib.sha1(code.encode()).hexdigest()[:8], 16)
        susp = int(round(true_mem[code] * (0.07 + (h % 90) / 1000.0)))
        tru.append(dict(scheme_code=code, scheme_name=names[code],
                        active_contributing=true_mem[code] - susp,
                        active_suspended=susp,
                        active_members_31mar2026=true_mem[code]))
    return reg, tru


def april_tail(seed=77310441):
    """Cases received 1 to 30 April 2026: inside the 30 April 2026 extract, outside the FY2026
    window and outside the FY2023-FY2025 comparison pool. Drawn on its own stream so the
    sixteen fiscal quarters of build() are byte-identical with or without it."""
    rng = np.random.default_rng(seed)
    out = []
    wdays = [d for d in WD if date(2026, 4, 1) <= d <= date(2026, 4, 30)]
    for code, q in QUEUES.items():
        m = q["mpc"] / (MINS_PER_DAY * AVAIL)
        pos = q["pos"][3]
        occ = q["occ"] + q["amp"] * (q["k26"] + P26[3])
        n = int(round(occ * pos * len(wdays) / m))
        w_mean = wq(pos, occ, m, q["cv2"])
        idx = rng.integers(0, len(wdays), n)
        wait = rng.gamma(0.9, w_mean / 0.9, n)
        hand = q["hmed"] * np.exp(HSIG * rng.standard_normal(n))
        extra = np.zeros(n)
        for A in (A_ for A_ in (ANOM, ANOM2) if A_):
            if code == A["code"]:
                extra = np.where(rng.random(n) < A["share"],
                                 A["extra_med"] * np.exp(0.6 * rng.standard_normal(n)), 0.0)
        am = np.where(rng.random(n) < q["p_am"],
                      q["am_med"] * np.exp(0.7 * rng.standard_normal(n)), 0.0)
        net = wait + hand + extra
        for k in range(n):
            rec = wdays[idx[k]]
            ans = add_wd(rec, net[k] + am[k])
            op = ans > EXTRACT
            clock = (EX_IX - WD_IX[rec] - am[k]) if op else net[k]
            out.append(dict(code=code, qi=16, rec=rec, net=net[k], am=am[k],
                            gross=net[k] + am[k], ans=None if op else ans,
                            tgt=q["tgt"], open=op, late=bool(clock > q["tgt"])))
    return out


MIGRATION = date(2024, 4, 1)      # Gemini to Orbit cutover
EXPORT_STAMP = (2026, 4, 30, 18, 0, 0)


def integerise(cases):
    """Re-express each case on the quantities the pack actually ships: whole working days from
    receipt to answer, and whole clock-stop days. `late` is then recomputed from those, so every
    graded figure is reproducible from the shipped dates and columns rather than from a float the
    generator holds. Mutates and returns `cases`."""
    for c in cases:
        c["stop"] = int(round(c["am"]))
        if c["ans"] is None:
            c["elapsed_wd"] = None
            clock = (EX_IX - WD_IX[c["rec"]]) - c["stop"]
        else:
            c["elapsed_wd"] = WD_IX[c["ans"]] - WD_IX[c["rec"]]
            clock = c["elapsed_wd"] - c["stop"]
        c["clock_wd"] = max(0, clock)
        c["late"] = bool(c["clock_wd"] > c["tgt"])
    return cases
