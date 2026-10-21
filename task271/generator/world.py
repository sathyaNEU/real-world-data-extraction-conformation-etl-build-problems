"""The world: the families referred to the Inherited Cancer Risk Service through a breast cancer proband since universal
panel testing began, every relative's carrier status by descent, breast cancer onset from age-specific hazards, other
cancers, deaths, who is a patient of the system, cascade testing over calendar time, and the date each family's
history was last brought up to date. Nothing here is written to the pack; records.py does that."""
import datetime as dt

import numpy as np

import common as K
import core as C

EDGES = np.arange(0, 101, 5)
EXPORT_Y = None   # set below


def yfrac(d):
    start = dt.date(d.year, 1, 1)
    days = (dt.date(d.year + 1, 1, 1) - start).days
    return d.year + (d - start).days / days


def ydate(y):
    yr = int(np.floor(y))
    start = dt.date(yr, 1, 1)
    days = (dt.date(yr + 1, 1, 1) - start).days
    return start + dt.timedelta(days=int(np.floor((y - yr) * days)))


EXPORT_Y = yfrac(K.EXPORT)
HOLIDAYS = {(1, 1), (7, 4), (12, 25)}


def workday(d):
    """The next weekday that is not New Year's Day, Independence Day or Christmas."""
    while d.weekday() >= 5 or (d.month, d.day) in HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def cum_haz(h, a):
    a = np.asarray(a, float)
    full = np.minimum(np.maximum(a[..., None] - EDGES[:-1], 0), 5)
    return (full * h).sum(-1)


def risk_by(h, a=70.0):
    return float(1 - np.exp(-cum_haz(h, np.array([a]))[0]))


def carrier_hazard(target):
    ages = EDGES[:-1] + 2.5
    shape = C.POP * np.exp(-C.RR_DECLINE * (ages - 45))
    lo, hi = 0.1, 400.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if risk_by(shape * mid) < target:
            lo = mid
        else:
            hi = mid
    return shape * lo


def draw_onset(rng, h):
    e = rng.exponential(1.0)
    H = np.concatenate([[0.0], np.cumsum(h * 5)])
    k = int(np.searchsorted(H, e, side="right") - 1)
    if k >= len(h) or h[k] <= 0:
        return np.inf
    return float(EDGES[k] + (e - H[k]) / h[k])


def other_death_age(rng, male):
    b = 0.093
    a = np.exp(-10.25) if male else np.exp(-10.6)
    return float(np.log(1 - b * np.log(rng.random()) / a) / b)


# other cancers on the pedigree (per person-year at age 60, a rough age slope), and the genes that raise them
OTHER = {"Colorectal": 6e-4, "Lung": 7e-4, "Melanoma": 3e-4, "Uterus": 2.5e-4, "Ovary": 1.2e-4, "Pancreas": 1.4e-4,
         "Prostate": 1.6e-3, "Kidney": 2e-4, "Bladder": 2.5e-4, "Lymphoma": 2e-4, "Thyroid": 1e-4, "Stomach": 8e-5,
         "Leukemia": 1.2e-4}
OTHER_RR = {("RAD51C", "Ovary"): 5.0, ("RAD51D", "Ovary"): 6.0, ("BRIP1", "Ovary"): 3.0, ("PALB2", "Ovary"): 2.5,
            ("PALB2", "Pancreas"): 2.4, ("ATM", "Pancreas"): 3.5, ("ATM", "Prostate"): 1.8, ("CHEK2", "Prostate"): 1.6,
            ("PALB2", "Prostate"): 1.5}
SEX_ONLY = {"Uterus": "F", "Ovary": "F", "Prostate": "M"}


def other_cancers(rng, sex, carrier, gene, death_age):
    """At most one cancer per site, onset from a hazard that rises 6 per cent a year of age from 30, drawn by
    inverting its cumulative hazard."""
    out = []
    for site, r60 in OTHER.items():
        if SEX_ONLY.get(site, sex) != sex:
            continue
        rr = OTHER_RR.get((gene, site), 1.0) if carrier else 1.0
        e = rng.exponential(1.0)
        a = 60 + np.log(e * 0.06 / (r60 * rr) + np.exp(0.06 * (30 - 60))) / 0.06
        if a < min(death_age, 95):
            out.append((site, float(a)))
    out.sort(key=lambda x: x[1])
    return out


# ------------------------------------------------------------------------------------------------- the variants
TRANSCRIPT = {"PALB2": ("NM_024675.4", 1186), "ATM": ("NM_000051.4", 3056), "CHEK2": ("NM_007194.4", 543),
              "BARD1": ("NM_000465.4", 777), "RAD51C": ("NM_058216.3", 376), "RAD51D": ("NM_002878.4", 328),
              "BRIP1": ("NM_032043.3", 1249)}
AA3 = ["Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile", "Leu", "Lys", "Met", "Phe", "Pro", "Ser",
       "Thr", "Trp", "Tyr", "Val"]
ONE = dict(Ala="A", Arg="R", Asn="N", Asp="D", Cys="C", Gln="Q", Glu="E", Gly="G", His="H", Ile="I", Leu="L",
           Lys="K", Met="M", Phe="F", Pro="P", Ser="S", Thr="T", Trp="W", Tyr="Y", Val="V")
MISSENSE_DOMAIN = {"PALB2": (853, 1186), "ATM": (2712, 2962), "CHEK2": (92, 510)}


def variants_for(rng, code):
    """A group's recurrent variants: HGVS c. and p., the reference laboratory's legacy name, and a recurrence
    weight. Truncating groups mix nonsense, frameshift and canonical splice variants; missense groups sit in the
    gene's functional domain."""
    gene, kind = K.GENE[code], K.KIND[code]
    tx, length = TRANSCRIPT[gene]
    n = {"protein-truncating": 14, "missense": 7}[kind]
    seen, out = set(), []
    while len(out) < n:
        u = rng.random()
        if kind == "missense":
            lo, hi = MISSENSE_DOMAIN[gene]
            aa = int(rng.integers(lo, hi))
            ref, alt, base = ("Leu", "Pro", "T>C") if u < 0.35 else (("Gly", "Arg", "G>C") if u < 0.6 else
                                                                      (("Arg", "Trp", "C>T") if u < 0.8 else
                                                                       ("Tyr", "Cys", "A>G")))
            pos = 3 * aa - (1 if base in ("T>C", "A>G") else 2)
            c = "c.%d%s" % (pos, base)
            p = "p.(%s%d%s)" % (ref, aa, alt)
            legacy = "%s%d%s" % (ONE[ref], aa, ONE[alt])
        else:
            aa = int(rng.integers(20, int(length * 0.92)))
            if u < 0.45:
                ref = "Arg" if rng.random() < 0.6 else "Gln"
                pos = 3 * aa - 2
                c = "c.%dC>T" % pos
                p = "p.(%s%dTer)" % (ref, aa)
                legacy = "%s%dX" % (ONE[ref], aa)
            elif u < 0.85:
                pos = 3 * aa - int(rng.integers(0, 3))
                nb = "ACGT"[int(rng.integers(0, 4))]
                dup = rng.random() < 0.3
                ref = AA3[int(rng.integers(0, 20))]
                new = AA3[int(rng.integers(0, 20))]
                fs = int(rng.integers(2, 40))
                c = "c.%d%s%s" % (pos, "dup" if dup else "del", nb)
                p = "p.(%s%d%sfs*%d)" % (ref, aa, new, fs)
                legacy = "%d%s%s" % (pos, "ins" if dup else "del", nb)
            else:
                exon_end = int(rng.integers(60, int(length * 2.7)))
                c = "c.%d+1G>A" % exon_end if rng.random() < 0.6 else "c.%d-2A>G" % exon_end
                p = "p.?"
                legacy = "IVS%d%s" % (int(rng.integers(2, 25)), "+1G>A" if "+1" in c else "-2A>G")
        if c in seen:
            continue
        seen.add(c)
        out.append(dict(gene=gene, transcript=tx, c=c, p=p, legacy=legacy))
    w = 1.0 / np.arange(1, n + 1) ** 1.1
    rng.shuffle(out)
    return out, w / w.sum()


# --------------------------------------------------------------------------------------------- one family
FIRST = ("MOTHER", "FATHER", "SISTER", "BROTHER", "DAUGHTER", "SON")
FDR_FEMALE = ("MOTHER", "SISTER", "DAUGHTER")


def _ident_date(rng, code):
    late = K.LATE[code]
    if late == "panel 2023":
        return yfrac(K.PANEL_2023) + rng.uniform(0.08, 0.5)
    if late == "reclassified 2024":
        return yfrac(K.RECLASS_2024) + rng.uniform(0.0, 0.35)
    return None


def family(rng, code, hc, hn, var_list, var_w):
    gene = K.GENE[code]
    P = []

    def add(role, sex, birth, car, mother=None, father=None, degree="second"):
        P.append(dict(lid=len(P), role=role, sex=sex, birth=float(birth), car=int(bool(car)), mother=mother,
                      father=father, degree=degree))
        return len(P) - 1

    # the proband: a woman who carries the family's variant, diagnosed in the universal-testing era
    lo, hi = yfrac(K.UNIVERSAL_START), EXPORT_Y - 0.3
    while True:
        birth = rng.uniform(1936, 2002)
        on = draw_onset(rng, hc)
        if 24 <= on <= 86 and lo <= birth + on <= hi:
            break
    pb = add("PROBAND", "F", birth, 1, degree="proband")
    dx = birth + on
    from_mother = rng.random() < 0.5
    mb = birth - float(np.clip(rng.normal(28, 5), 17, 44))
    fb = mb - float(np.clip(rng.normal(2.5, 3.5), -6, 14))
    mo = add("MOTHER", "F", mb, from_mother, degree="first")
    fa = add("FATHER", "M", fb, not from_mother, degree="first")
    P[pb]["mother"], P[pb]["father"] = mo, fa
    sibs = []
    nsis, nbro = rng.poisson(1.15), rng.poisson(1.15)
    for s in range(nsis + nbro):
        sb = birth + float(np.clip(rng.normal(0, 5.5), -16, 16))
        if not (16 <= sb - mb <= 46) or sb > EXPORT_Y - 0.5:
            continue
        sex = "F" if s < nsis else "M"
        i = add("SISTER" if sex == "F" else "BROTHER", sex, sb, rng.random() < 0.5, mo, fa, "first")
        sibs.append(i)
    # half-siblings: a parent's child with another partner
    if rng.random() < 0.09:
        via_mother = rng.random() < 0.5
        sb = birth + float(np.clip(rng.normal(0, 8), -18, 18))
        par_trans = from_mother if via_mother else (not from_mother)
        sex = "F" if rng.random() < 0.5 else "M"
        role = ("HALF_SISTER" if sex == "F" else "HALF_BROTHER") + ("_MAT" if via_mother else "_PAT")
        if sb < EXPORT_Y - 0.5:
            add(role, sex, sb, par_trans and rng.random() < 0.5, mo if via_mother else None,
                None if via_mother else fa, "second")
    partner = None
    kids = []
    nk = rng.poisson(1.0) + rng.poisson(1.0)
    if nk or rng.random() < 0.6:
        partner = add("PARTNER", "M", birth - float(np.clip(rng.normal(2, 4), -8, 12)), 0, degree="partner")
    for s in range(nk):
        kb = birth + float(np.clip(rng.normal(28, 5), 17, 44))
        if kb > EXPORT_Y - 0.3:
            continue
        sex = "F" if rng.random() < 0.5 else "M"
        kids.append(add("DAUGHTER" if sex == "F" else "SON", sex, kb, rng.random() < 0.5, pb, partner, "first"))
    # grandparents, aunts and uncles on both sides
    gm_carries = rng.random() < 0.5
    for side, par, trans in (("MAT", mo, from_mother), ("PAT", fa, not from_mother)):
        pbirth = P[par]["birth"]
        gmb = pbirth - float(np.clip(rng.normal(28, 5), 17, 44))
        gfb = gmb - float(np.clip(rng.normal(2.5, 3.5), -6, 14))
        gm = add(side + "_GRANDMOTHER", "F", gmb, trans and gm_carries)
        gf = add(side + "_GRANDFATHER", "M", gfb, trans and not gm_carries)
        P[par]["mother"], P[par]["father"] = gm, gf
        for s in range(rng.poisson(1.5)):
            ab = pbirth + float(np.clip(rng.normal(0, 6), -17, 17))
            if not (16 <= ab - gmb <= 46):
                continue
            sex = "F" if rng.random() < 0.5 else "M"
            add(side + ("_AUNT" if sex == "F" else "_UNCLE"), sex, ab, trans and rng.random() < 0.5, gm, gf)
    for s in sibs:
        for _ in range(rng.poisson(1.1)):
            nb = P[s]["birth"] + float(np.clip(rng.normal(28, 5), 17, 44))
            if nb > EXPORT_Y - 0.3:
                continue
            sex = "F" if rng.random() < 0.5 else "M"
            m, f = (s, None) if P[s]["sex"] == "F" else (None, s)
            add("NIECE" if sex == "F" else "NEPHEW", sex, nb, P[s]["car"] and rng.random() < 0.5, m, f)
    for k in kids:
        for _ in range(rng.poisson(0.9)):
            gb = P[k]["birth"] + float(np.clip(rng.normal(28, 5), 17, 44))
            if gb > EXPORT_Y - 0.3:
                continue
            sex = "F" if rng.random() < 0.5 else "M"
            m, f = (k, None) if P[k]["sex"] == "F" else (None, k)
            add("GRANDDAUGHTER" if sex == "F" else "GRANDSON", sex, gb, P[k]["car"] and rng.random() < 0.5, m, f)

    # phenotypes: breast cancer (women), other cancers, death
    for p in P:
        male = p["sex"] == "M"
        if p["role"] == "PROBAND":
            p["breast"] = on
        elif male:
            p["breast"] = np.inf
        else:
            p["breast"] = draw_onset(rng, hc if p["car"] else hn)
        od = other_death_age(rng, male)
        bcd = np.inf
        if np.isfinite(p["breast"]) and rng.random() < 0.22:
            bcd = p["breast"] + rng.exponential(5.0) + 0.3
        if p["role"] == "PROBAND":
            od = max(od, on + 0.6)            # alive at her test and first course
            bcd = max(bcd, on + 0.6)
        p["death"] = float(min(od, bcd))
        p["bc_death"] = bool(bcd < od)
        p["other"] = other_cancers(rng, p["sex"], p["car"], gene, p["death"])
        p["variant"] = None
    v = int(rng.choice(len(var_list), p=var_w))
    for p in P:
        if p["car"]:
            p["variant"] = v

    # patients of the system: everyone the service tests becomes one; others by degree
    for p in P:
        alive_after = p["birth"] + p["death"] > 2012.0
        pr = {"proband": 1.0, "first": C.PATIENT["first"], "partner": C.PATIENT["partner"]}.get(
            p["degree"], C.PATIENT["second"])
        p["patient"] = bool(alive_after and rng.random() < pr)

    intake = min(dx + rng.uniform(0.08, 0.5), EXPORT_Y - 0.05)
    ident = _ident_date(rng, code)
    late = ident is not None and dx < ident
    letters = (ident + rng.uniform(0.05, 0.45)) if late else (intake + rng.uniform(0.04, 0.3))
    a_rate, u_rate = (C.A_LATE, C.U_LATE) if late else (C.A_DIRECT, C.U_DIRECT)
    for p in P:
        p["test"], p["test_kind"] = np.nan, ""
    P[pb]["test"], P[pb]["test_kind"] = dx + 0.04, "panel"
    # first-degree relatives: own-care panels after a diagnosis, the service's invitation after the letter
    for p in P:
        if p["degree"] != "first":
            continue
        yo, yd = p["birth"] + p["breast"], p["birth"] + p["death"]
        cands = []
        if p["sex"] == "F" and p["patient"] and intake < yo <= EXPORT_Y and rng.random() < C.OWN_CARE:
            cands.append((yo + rng.uniform(0.03, 0.15), "panel"))
        if letters < EXPORT_Y and letters - p["birth"] >= 18:
            if yo <= letters:
                if rng.random() < a_rate:
                    cands.append((letters + rng.exponential(C.TAU_AFFECTED), "familial"))
            elif rng.random() < u_rate:
                cands.append((letters + rng.exponential(C.TAU_UNAFFECTED), "familial"))
        cands = [c for c in cands if c[0] < min(yd, EXPORT_Y) and c[0] - p["birth"] >= 18]
        if cands:
            c = min(cands)
            p["test"], p["test_kind"] = c
            p["patient"] = True
    # second-degree relatives: tested after the relative who connects them tests positive
    link = {}
    for i, p in enumerate(P):
        if p["degree"] == "second" and p["role"] not in ("MAT_GRANDMOTHER", "MAT_GRANDFATHER", "PAT_GRANDMOTHER",
                                                         "PAT_GRANDFATHER"):
            if p["role"].startswith("MAT_"):
                link[i] = mo
            elif p["role"].startswith("PAT_"):
                link[i] = fa
            elif p["role"].startswith("HALF_"):
                link[i] = mo if p["role"].endswith("_MAT") else fa
            else:
                link[i] = p["mother"] if p["mother"] is not None and P[p["mother"]]["degree"] == "first" else p["father"]
    for i, j in link.items():
        p, q = P[i], P[j] if j is not None else None
        if q is None or not np.isfinite(q["test"]) or not q["car"]:
            continue
        if rng.random() < 0.25:
            t = q["test"] + rng.exponential(1.5)
            if t < min(p["birth"] + p["death"], EXPORT_Y) and t - p["birth"] >= 18:
                p["test"], p["test_kind"] = t, "familial"
                p["patient"] = True
    # the family's history is brought up to date at intake, at a late result, at every test and when the tumor
    # registry links a patient's new diagnosis
    marks = [intake] + ([ident + rng.uniform(0.0, 0.25)] if late else [])
    for p in P:
        if p["role"] != "PROBAND" and np.isfinite(p["test"]):
            marks.append(p["test"])
        yo = p["birth"] + p["breast"]
        if p["role"] != "PROBAND" and p["patient"] and intake < yo <= EXPORT_Y and yo < p["birth"] + p["death"]:
            marks.append(yo + 0.05)
    hist = min(max(marks), EXPORT_Y)
    P = [p for p in P if p["birth"] <= hist - 0.05 or p["role"] == "PROBAND"]
    for p in P:
        last = min(hist, p["birth"] + p["death"]) - p["birth"]
        p["alive_at_hist"] = p["birth"] + p["death"] > hist
        p["last_age"] = float(last)
    return dict(code=code, persons=P, proband=pb, dx=dx, intake=intake, ident=ident, late=late, letters=letters,
                history=hist, variant=v, from_mother=from_mother)


def world(seed=C.SEED):
    hn = C.POP.copy()
    fams = []
    variants = {}
    for gi, code in enumerate(K.CODES):
        rng = np.random.default_rng([seed, gi])
        vr = np.random.default_rng([seed, 900 + gi])
        var_list, var_w = variants_for(vr, code)
        variants[code] = var_list
        target, nfam = C.TRUTH[code]
        hc = carrier_hazard(target)
        for _ in range(nfam):
            fams.append(family(rng, code, hc, hn, var_list, var_w))
    return dict(families=fams, variants=variants, seed=seed)


# ------------------------------------------------------------------------- the analysis view of one group
def fdr_female(W, code):
    """(time, event, carrier, tested, alive at history) for the probands' mothers, sisters and daughters: age at a
    first breast cancer before 70, else age at the family's history date or at death; ages in completed years as the
    pedigree carries them."""
    out = []
    for f in W["families"]:
        if f["code"] != code:
            continue
        for p in f["persons"]:
            if p["role"] not in FDR_FEMALE:
                continue
            last = int(np.floor(p["last_age"]))
            ev = np.isfinite(p["breast"]) and p["breast"] <= p["last_age"]
            t = int(np.floor(p["breast"])) if ev else last
            out.append((t, int(ev), p["car"], int(np.isfinite(p["test"])), int(p["alive_at_hist"])))
    return np.array(out, float)
