"""task170 records: the county's operating files as their systems hold them, with the Layer 1 mess each system
writes. Each function takes its own RNG stream and returns rows; nothing here reads another component's draws."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import world as W

D = dt.date

# ---------------------------------------------------------------------------------------------------- sentinel villages
VILLAGES = [
    ("RTN", "Kamwala", "Kamwala Beach"), ("RTN", "Bondo Gate", "Ogwedhi"),
    ("MWR", "Siala", "Siala Kogalo"), ("MWR", "Kadero", "Kadero East"),
    ("KDG", "Ombogo", "Ombogo"), ("KDG", "Kitere", "Kitere Mumbo"),
    ("OYM", "Lwala", "Lwala Beach"), ("OYM", "Masala", "Masala Kanyango"),
    ("NDR", "Ugowe", "Ugowe Bay"), ("NDR", "Kalanya", "Kalanya"),
    ("KBR", "Rabondo", "Rabondo"), ("KBR", "Wiga", "Wiga Oboke"),
    ("WKL", "Sirongo", "Sirongo"), ("WKL", "Ndhuru", "Ndhuru Pier"),
]
# monthly abundance of An. ruvariensis (long rains April to June, short rains October to December)
SEASON = {1: 0.55, 2: 0.48, 3: 0.70, 4: 1.30, 5: 1.75, 6: 1.45, 7: 0.95, 8: 0.70, 9: 0.62, 10: 0.88, 11: 1.20,
          12: 0.95}


def village_code(i):
    sc, ward, name = VILLAGES[i]
    return "SV-%s-%02d" % (sc, i + 1)


def hlc(rng):
    """Human landing catches: two nights a month at each sentinel village, two houses a night, one collector
    indoors and one outdoors at each house, every hour from 18:00 to 06:00, 45 minutes catching in each hour.
    Counts are drawn by inverse distribution functions on a fixed stream of uniforms, so the stream does not depend
    on the means."""
    from scipy.stats import gamma as G_, poisson as P_
    b_in, b_out = W.vector_profile(**W.COUNTY_VECTOR)
    # a sibling anopheline that does not carry the fever and bites on the same clock; culicines bite later
    t_in, t_out = W.vector_profile(peak=3.2, width=2.35, out_ratio=1.72)
    cx_in, cx_out = W.vector_profile(peak=5.5, width=3.0, out_ratio=0.9)
    dens = np.exp(rng.normal(0, 0.45, len(VILLAGES)))
    collectors = {vi: ["C%03d" % (100 + vi * 6 + k) for k in range(6)] for vi in range(len(VILLAGES))}
    cells = []
    for vi, (sc, ward, vname) in enumerate(VILLAGES):
        for (y, m) in C.months((2024, 1), (2026, 9)):
            days = sorted(rng.choice(np.arange(3, 27), 2, replace=False))
            for d in days:
                night = D(y, m, int(d))
                n_eff = float(np.exp(rng.normal(0, 0.35)))
                for house in (1, 2):
                    h_eff = float(np.exp(rng.normal(0, 0.20)))
                    pair = rng.choice(collectors[vi], 2, replace=False)
                    for pos, coll in (("IN", pair[0]), ("OUT", pair[1])):
                        for h in C.HOURS:
                            cells.append((vi, night, house, pos, coll, h, dens[vi] * SEASON[m] * n_eff, h_eff, SEASON[m] * n_eff))
    n = len(cells)
    u = rng.random((n, 4))
    u = np.clip(u, 1e-12, 1 - 1e-12)
    pos_in = np.array([c[3] == "IN" for c in cells])
    hh = np.array([c[5] for c in cells])
    lvl = np.array([c[6] for c in cells])
    heff = np.array([c[7] for c in cells])
    seas = np.array([c[8] for c in cells])
    mean_v = 11.0 * lvl * heff * np.where(pos_in, b_in[hh], b_out[hh]) * 0.75
    k = 1.6
    lam = G_.ppf(u[:, 0], k, scale=mean_v / k)
    n_v = P_.ppf(u[:, 1], lam).astype(int)
    n_t = P_.ppf(u[:, 2], 4.2 * lvl * np.where(pos_in, t_in[hh], t_out[hh]) * 0.75).astype(int)
    n_c = P_.ppf(u[:, 3], 9.0 * seas * np.where(pos_in, cx_in[hh], cx_out[hh]) * 0.75).astype(int)
    rows = []
    for i, c in enumerate(cells):
        rows.append(dict(vi=c[0], night=c[1], house=c[2], position=c[3], collector=c[4], h=c[5], minutes=45,
                         an_ruv=int(n_v[i]), an_ten=int(n_t[i]), culex=int(n_c[i])))
    return rows


def survey(rng):
    """The county's human behaviour survey: round 1 in April 2025 (long rains), round 2 in August 2025, a
    two-stage sample of households in the sentinel villages' wards; round 2 revisits about a third of round 1's
    households and adds new ones."""
    r1 = W.survey_people(rng, 360, 1)
    for r in r1:
        r["round"] = 1
        r["vi"] = int(rng.integers(len(VILLAGES)))
    # one household one village
    hh_v = {}
    for r in r1:
        hh_v.setdefault(r["hh"], int(rng.integers(len(VILLAGES))))
        r["vi"] = hh_v[r["hh"]]
    revisit = sorted(rng.choice(sorted(hh_v), 120, replace=False).tolist())
    r2 = []
    for r in r1:
        if r["hh"] in revisit:
            t_in = r["t_in"] + rng.normal(0, 0.25)
            t_bed = max(r["t_bed"] + rng.normal(0, 0.25), t_in + 0.05)
            r2.append(dict(hh=r["hh"], person=r["person"], group=r["group"], t_in=t_in, t_bed=t_bed,
                           t_rise=r["t_rise"] + rng.normal(0, 0.15), round=2, vi=r["vi"], revisit=True))
    new = W.survey_people(rng, 200, 2)
    base = max(hh_v) + 1
    for r in new:
        r["hh"] += base
        hh_v.setdefault(r["hh"], int(rng.integers(len(VILLAGES))))
        r["vi"] = hh_v[r["hh"]]
        r["round"] = 2
        r["revisit"] = False
        r2.append(r)
    for r in r1:
        r["revisit"] = False
    return r1 + r2


# ---------------------------------------------------------------------------------------------------- plan
POP = {"RTN": 168420, "MWR": 151873, "KDG": 129506, "OYM": 162214, "NDR": 118739, "KBR": 157962, "WKL": 131586}
# expected cases per 1,000 residents a month without the campaign, the county's planning model, 2027
RATE = {"RTN": 4.645, "MWR": 6.242, "KDG": 5.571, "OYM": 7.036, "NDR": 5.255, "KBR": 6.135, "WKL": 4.793}
MONTH_SHAPE = {4: 1.18, 5: 1.46, 6: 1.31, 7: 0.92, 8: 0.70, 9: 0.63, 10: 0.86, 11: 1.12, 12: 0.97}
USAGE = {4: 0.80, 5: 0.79, 6: 0.77, 7: 0.75, 8: 0.73, 9: 0.71, 10: 0.69, 11: 0.67, 12: 0.65}


def baseline(rng):
    out = {}
    for sc in C.SC_CODES:
        for (y, m) in C.WINDOW:
            v = POP[sc] / 1000 * RATE[sc] * MONTH_SHAPE[m] * float(np.exp(rng.normal(0, 0.03)))
            out[(sc, m)] = int(round(v))
    return out


# ---------------------------------------------------------------------------------------------------- names
def name_pools(seed):
    from faker import Faker
    fk = Faker("en_KE")
    Faker.seed(seed)
    firsts_m = sorted({fk.first_name_male() for _ in range(4000)})
    firsts_f = sorted({fk.first_name_female() for _ in range(4000)})
    lasts = sorted({fk.last_name() for _ in range(6000)})
    return firsts_m, firsts_f, lasts


# ---------------------------------------------------------------------------------------------------- registration
VILLAGE_STEMS = ["Kanyango", "Kogalo", "Oboke", "Mumbo", "Kamser", "Ochuna", "Kadem", "Nyagoro", "Kawuor", "Ogada",
                 "Kanyibok", "Rapogi", "Kogweno", "Nyabera", "Kawere", "Odienya", "Kamwania", "Gongo", "Kodumo",
                 "Nyatwori", "Rambusi", "Kaminjo", "Ojola", "Kobala", "Rangwe", "Kamagak", "Simbi", "Dago", "Kanam",
                 "Asego", "Kopiyo", "Nyalgunga", "Kolwa", "Rakwaro", "Kanyamwa", "Oyugis", "Kotieno", "Ramba",
                 "Kandiege", "Nyakwere", "Kamato", "Ongeti", "Okok", "Nyangoma", "Kagan", "Kojwang", "Rachar"]


def registration(rng, pools):
    """Community health volunteers' household registration for the campaign: the main round in September 2026 and
    the October mop-up. Returns the rows as the registration app exports them, and the truth (which mop-up rows are
    households already registered in the main round)."""
    fm, ff, ln = pools
    rows = []
    truth_rereg = []
    serial = {sc: 0 for sc in C.SC_CODES}
    vill_of = {}
    vstem = list(VILLAGE_STEMS)
    k = 0
    for sc in C.SC_CODES:
        for wi, ward in enumerate(C.WARDS[sc]):
            n_v = int(rng.integers(6, 11))
            vill_of[(sc, ward)] = []
            for j in range(n_v):
                stem = vstem[k % len(vstem)]
                suffix = ["", " A", " B", " East", " West", " Central", " Beach", " Upper"][(k // len(vstem)) % 8]
                vill_of[(sc, ward)].append(stem + suffix)
                k += 1

    def head(rng):
        if rng.random() < 0.62:
            return "%s %s" % (fm[int(rng.integers(len(fm)))], ln[int(rng.integers(len(ln)))]), "M"
        return "%s %s" % (ff[int(rng.integers(len(ff)))], ln[int(rng.integers(len(ln)))]), "F"

    def counts(rng):
        m = int(rng.choice(np.arange(1, 12), p=[.07, .12, .15, .17, .16, .12, .08, .06, .04, .02, .01]))
        u5 = int(min(m - 1 if m > 1 else 0, rng.binomial(m, 0.17)))
        sp = int(max(1, min(m, round(m / rng.uniform(1.6, 2.6)))))
        return m, u5, sp

    def chv(sc, wi, rng):
        return "CHV-%s-%02d%02d" % (sc, wi + 1, int(rng.integers(1, 30)))

    for sc in C.SC_CODES:
        n_hh = int(round(POP[sc] / 4.62))
        wards = C.WARDS[sc]
        wshare = rng.dirichlet(np.ones(len(wards)) * 6)
        for wi, ward in enumerate(wards):
            n_w = int(round(n_hh * wshare[wi]))
            vills = vill_of[(sc, ward)]
            prefix = ward.replace(" ", "")[:3].upper()
            dwell_no = 0
            hh = 0
            while hh < n_w:
                dwell_no += 1
                n_in = 1 if rng.random() < 0.885 else int(rng.choice([2, 3], p=[0.8, 0.2]))
                village = vills[int(rng.integers(len(vills)))]
                dwelling = "%s/%04d" % (prefix, dwell_no)
                seen = set()
                for _ in range(n_in):
                    while True:
                        m, u5, sp = counts(rng)
                        if (m, u5, sp) not in seen:
                            seen.add((m, u5, sp))
                            break
                    name, sex = head(rng)
                    missed = rng.random() < 0.026
                    serial[sc] += 1
                    d0, d1 = (C.REG_MOPUP if missed else C.REG_MAIN)
                    day = d0 + dt.timedelta(days=int(rng.integers(0, (d1 - d0).days + 1)))
                    r = dict(reg_no="RV/%s/%d/%06d" % (sc, wi + 1, serial[sc]), round="MOPUP" if missed else "MAIN",
                             reg_date=day, chv=chv(sc, wi, rng), sub_county=sc, ward=ward, village=village,
                             dwelling=dwelling, head=name, sex=sex,
                             id_no=("%08d" % int(rng.integers(10000000, 39999999))) if rng.random() < 0.63 else "",
                             phone=("07%08d" % int(rng.integers(0, 99999999))) if rng.random() < 0.58 else "",
                             members=m, under5=u5, spaces=sp, remarks="")
                    rows.append(r)
                    hh += 1
                    # a main-round household registered again in the mop-up under a new number
                    if not missed and rng.random() < 0.034:
                        serial[sc] += 1
                        d0, d1 = C.REG_MOPUP
                        day = d0 + dt.timedelta(days=int(rng.integers(0, (d1 - d0).days + 1)))
                        same_head = rng.random() < 0.35
                        nm, sx = (name, sex) if same_head else head(rng)
                        if same_head and rng.random() < 0.5:
                            parts = nm.split(" ")
                            nm = parts[-1] + " " + " ".join(parts[:-1])
                        r2 = dict(r)
                        r2.update(reg_no="RV/%s/%d/%06d" % (sc, wi + 1, serial[sc]), round="MOPUP", reg_date=day,
                                  chv=chv(sc, wi, rng), head=nm, sex=sx,
                                  id_no=(r["id_no"] if (same_head and r["id_no"] and rng.random() < 0.7) else
                                         (("%08d" % int(rng.integers(10000000, 39999999))) if rng.random() < 0.5 else "")),
                                  phone=(r["phone"] if (same_head and r["phone"] and rng.random() < 0.5) else
                                         (("07%08d" % int(rng.integers(0, 99999999))) if rng.random() < 0.5 else "")),
                                  remarks="")
                        rows.append(r2)
                        truth_rereg.append(r2["reg_no"])
    # occasional free-text remarks
    notes = ["slip lost", "head away, spouse registered", "new dwelling", "relocated within village",
             "phone not reachable", "disabled member", "elderly head", "twins under 1"]
    for r in rows:
        if rng.random() < 0.012:
            r["remarks"] = notes[int(rng.integers(len(notes)))]
    # the app's sync replayed some records twice, byte for byte
    replay = [dict(r) for r in rows if rng.random() < 0.003]
    out = rows + replay
    order = rng.permutation(len(out))
    out = [out[i] for i in order]
    out.sort(key=lambda r: (r["sub_county"], r["reg_date"], r["chv"]))
    return out, set(truth_rereg)


# ---------------------------------------------------------------------------------------------------- facilities
def facilities(rng, pools):
    """The master facility list as of the pull: current sub-county under the July 2026 realignment."""
    out = []
    code = 15200
    for sc in C.SC_CODES:
        wards = C.WARDS[sc]
        base_ward = wards[0]
        code += int(rng.integers(3, 9))
        hosp = dict(mfl=str(code), name="%s Sub-County Hospital" % C.SC_NAME[sc], level="Level 4", sub_county=sc,
                    ward=base_ward, opened=D(1998 + int(rng.integers(0, 12)), int(rng.integers(1, 13)), 1),
                    reporting_since=D(2014, 1, 1), parent="")
        out.append(hosp)
        for wi, ward in enumerate(wards):
            n_hc = 1 if wi == 0 else int(rng.integers(1, 3))
            for j in range(n_hc):
                code += int(rng.integers(2, 11))
                kind = "Health Centre" if (j == 0 and wi % 2 == 0) else "Dispensary"
                out.append(dict(mfl=str(code), name="%s %s" % (ward if j == 0 else ward + " " + ["Kati", "Pier", "Market"][j % 3], kind),
                                level="Level 3" if kind == "Health Centre" else "Level 2", sub_county=sc, ward=ward,
                                opened=D(2002 + int(rng.integers(0, 15)), int(rng.integers(1, 13)), 1),
                                reporting_since=D(2014, 1, 1), parent=""))
        code += int(rng.integers(40, 90))
        sat_name = "%s Outreach Clinic" % ["Kamagak", "Kanyibok", "Ombogo Market", "Got Oyuga Stage", "Ugowe Pier", "Rabondo Market", "Sirongo Stage"][C.SC_CODES.index(sc)]
        out.append(dict(mfl=str(code), name=sat_name, level="Level 2", sub_county=sc, ward=wards[min(1, len(wards) - 1)],
                        opened=D(2019, int(rng.integers(1, 13)), 1), reporting_since=D(*C.SAT_START, 1), parent=hosp["mfl"]))
    return out


def khis(rng, facs):
    """Monthly MOH 705 returns for Ombeni fever: tested, confirmed and clinically diagnosed, by age group (under 5,
    5 and over), January 2024 to September 2026, as the county's KHIS export holds them."""
    rows = []
    sats = {f["parent"]: f for f in facs if f["parent"]}
    vol = {}
    for f in facs:
        base = {"Level 4": 260, "Level 3": 120, "Level 2": 48}[f["level"]] * float(np.exp(rng.normal(0, 0.35)))
        vol[f["mfl"]] = base * RATE[f["sub_county"]] / 5.8
    truth = {}
    for (y, m) in C.months(C.KHIS_START, C.KHIS_END):
        seas = SEASON[m]
        for f in facs:
            if f["parent"] and (y, m) < C.SAT_START:
                continue
            for age, share in (("<5", 0.31), ("5+", 0.69)):
                conf = int(rng.poisson(vol[f["mfl"]] * seas * share))
                tested = int(conf / rng.uniform(0.28, 0.42)) + int(rng.integers(0, 9))
                clin = int(rng.poisson(conf * 0.12))
                truth[(f["mfl"], y, m, age)] = conf
                rows.append(dict(mfl=f["mfl"], y=y, m=m, age=age, tested=tested, confirmed=conf, clinical=clin,
                                 comment=""))
    # the parents' January to March 2026 returns still carried their satellites' OPD
    for r in rows:
        if r["mfl"] in sats and C.SAT_START <= (r["y"], r["m"]) <= C.SAT_PARENT_UNTIL:
            s = sats[r["mfl"]]
            sat_row = next(q for q in rows if q["mfl"] == s["mfl"] and q["y"] == r["y"] and q["m"] == r["m"] and q["age"] == r["age"])
            r["confirmed"] += sat_row["confirmed"]
            r["tested"] += sat_row["tested"]
            r["clinical"] += sat_row["clinical"]
            r["comment"] = "incl. outreach OPD"
    return rows, truth
