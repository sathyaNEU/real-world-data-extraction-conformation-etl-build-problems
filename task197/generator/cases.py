"""The network's case export for the watched products, one row per substance line of a case."""
import datetime as dt
import numpy as np
import sim
import world

MIGRATION = dt.date(2023, 7, 10)    # the network moved its member centers onto one case-management system
COLUMNS = ["case_id", "member_center", "call_received_local", "caller_site", "patient_age_years", "patient_age_months",
           "patient_sex", "substance_seq", "substance_reported", "product_code", "reason", "route", "management_site",
           "medical_outcome"]

OTHER_SUBSTANCES = ["Household bleach", "Laundry detergent pod", "Dishwasher detergent", "Hand sanitizer",
                    "Diaper cream (zinc oxide)", "Unknown white tablet", "Melatonin gummies (store brand)",
                    "Diphenhydramine tablets (store brand)", "Grandparent's metoprolol", "Cough drops (menthol)",
                    "Toothpaste", "Button battery", "Topical hydrocortisone", "Silica gel packet", "Cigarette butt",
                    "Antacid chewable tablets", "Children's loratadine (store brand)"]
OUTCOMES_MAIN = [("No effect", 0.31), ("Not followed, judged as nontoxic exposure", 0.33),
                 ("Not followed, minimal clinical effects possible", 0.17), ("Minor effect", 0.13),
                 ("Moderate effect", 0.035), ("Major effect", 0.004), ("Unable to follow, judged as potentially toxic exposure", 0.021)]
SITES_MAIN = [("Own residence", 0.885), ("Other residence", 0.072), ("Public area", 0.016),
              ("School or daycare", 0.009), ("Unknown", 0.018)]
MGMT = [("Managed on site (non-HCF)", 0.79), ("Referred to HCF by poison center", 0.12),
        ("Already in or en route to HCF when poison center called", 0.09)]
AGES_MAIN = [(0, 0.085), (1, 0.39), (2, 0.31), (3, 0.12), (4, 0.06), (5, 0.035)]
HOURS = np.array([0.6, 0.4, 0.3, 0.2, 0.2, 0.4, 1.4, 3.1, 4.6, 5.4, 5.8, 5.9, 5.7, 5.4, 5.3, 5.6, 6.2, 7.0, 7.6,
                  7.4, 6.4, 4.8, 3.1, 1.5])
HOURS = HOURS / HOURS.sum()

# non-main populations per product: (reason, share of the product's main daily rate, age sampler)
OTHER_POP = {
    "liquid": [("Unintentional - therapeutic error", 0.16, "child"), ("Unintentional - general", 0.035, "older"),
               ("Adverse reaction - drug", 0.012, "child"), ("Intentional - suspected suicidal", 0.010, "teen"),
               ("Unintentional - misuse", 0.006, "older"), ("Unknown reason", 0.004, "any")],
    "tablet": [("Unintentional - therapeutic error", 0.11, "adult"), ("Unintentional - general", 0.05, "older"),
               ("Intentional - suspected suicidal", 0.09, "teen"), ("Intentional - misuse", 0.02, "teen"),
               ("Adverse reaction - drug", 0.01, "adult"), ("Unknown reason", 0.006, "any")],
    "other": [("Unintentional - therapeutic error", 0.07, "adult"), ("Unintentional - general", 0.06, "older"),
              ("Adverse reaction - drug", 0.02, "adult"), ("Unintentional - misuse", 0.01, "older"),
              ("Unknown reason", 0.005, "any")],
}
KIND = {"FKJ": "liquid", "IBC": "liquid", "CGH": "liquid", "FKI": "liquid", "ALC": "liquid", "DOZ": "tablet",
        "IBT": "tablet", "FER": "tablet", "NIC": "tablet", "GUM": "other", "EYE": "other", "VAP": "other"}


def _pick(rng, pairs, n):
    labels = [p[0] for p in pairs]
    w = np.array([p[1] for p in pairs], dtype=float)
    return [labels[i] for i in rng.choice(len(labels), size=n, p=w / w.sum())]


def _age(rng, kind):
    if kind == "child":
        return int(rng.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                              p=np.array([10, 14, 15, 13, 11, 9, 7, 6, 5, 4, 3, 3]) / 100))
    if kind == "older":
        return int(rng.choice([6, 7, 8, 9, 10, 11, 12, 14, 16, 19, 25, 34, 45, 58, 70, 81]))
    if kind == "teen":
        return int(rng.choice([12, 13, 14, 15, 16, 17, 18, 19, 21, 24, 29, 35, 44, 52],
                              p=np.array([4, 8, 13, 15, 15, 13, 9, 6, 5, 4, 3, 2, 2, 1]) / 100))
    if kind == "adult":
        return int(rng.choice([19, 23, 28, 33, 38, 44, 51, 58, 64, 70, 76, 83, 88]))
    return int(rng.choice([1, 2, 4, 9, 15, 27, 41, 66]))


def _route(code, reason, rng):
    if code == "EYE" and reason != "Unintentional - general":
        return "Ocular" if rng.random() < 0.8 else "Ingestion"
    if code == "VAP" and reason in ("Unintentional - therapeutic error", "Adverse reaction - drug"):
        return "Dermal" if rng.random() < 0.7 else "Inhalation/nasal"
    return "Ingestion"


def build(truth, seed):
    """Return the export rows (list of lists) in case order."""
    rng = np.random.default_rng(seed)
    centers = [c[0] for c in world.CENTERS]
    cshare = np.array([c[4] for c in world.CENTERS])
    cases = []          # (date, minute_of_day, center, product, reason, age_years, age_months, sex, extra)
    d0 = sim.day_index(sim.EXPORT_FROM)
    for p in sim.PRODUCTS:
        code = p["code"]
        main = truth[code]["expo"]
        rate = truth[code]["lam"]
        for i in range(d0, sim.NDAYS):
            n = int(main[i])
            for _ in range(n):
                cases.append([i, None, None, code, "Unintentional - general", "main"])
        for reason, share, ages in OTHER_POP[KIND[code]]:
            lam = rate[d0:] * share
            counts = rng.poisson(lam)
            for j in np.nonzero(counts)[0]:
                for _ in range(int(counts[j])):
                    cases.append([d0 + j, None, None, code, reason, ages])
    # order the cases in time, then give each a time of day and a center
    rng.shuffle(cases)
    cases.sort(key=lambda c: c[0])
    rows = []
    seq_legacy = {}
    seq_new = {}
    for c in cases:
        i, _, _, code, reason, ages = c
        day = sim.DAYS[i]
        hour = int(rng.choice(24, p=HOURS))
        minute = int(rng.integers(0, 60))
        if day.month == 3 and day.weekday() == 6 and 8 <= day.day <= 14 and hour == 2:
            hour = 3          # the skipped hour on the day clocks go forward
        center = centers[int(rng.choice(len(centers), p=cshare / cshare.sum()))]
        stamp = "%s %02d:%02d" % (day.isoformat(), hour, minute)
        if day < MIGRATION:
            k = (center, day.year)
            seq_legacy[k] = seq_legacy.get(k, 0) + 1
            cid = "%s-%02d-%06d" % (center, day.year % 100, seq_legacy[k])
        else:
            k = (day.year, day.month)
            seq_new[k] = seq_new.get(k, 0) + int(rng.integers(1, 4))
            cid = "MP%02d%02d%06d" % (day.year % 100, day.month, seq_new[k])
        if ages == "main":
            age = int(rng.choice([a for a, _ in AGES_MAIN], p=np.array([w for _, w in AGES_MAIN]) / sum(w for _, w in AGES_MAIN)))
            site = _pick(rng, SITES_MAIN, 1)[0]
            outcome = _pick(rng, OUTCOMES_MAIN, 1)[0]
        else:
            age = _age(rng, ages)
            site = "Own residence" if rng.random() < 0.8 else _pick(rng, SITES_MAIN, 1)[0]
            outcome = _pick(rng, OUTCOMES_MAIN, 1)[0]
        months = ""
        if age < 2:
            months = str(age * 12 + int(rng.integers(0, 12)))
            if age == 0 and months == "0":
                months = "1"
        sex = "Female" if rng.random() < 0.48 else ("Male" if rng.random() < 0.985 else "Unknown")
        mg = _pick(rng, MGMT, 1)[0]
        text = world.META[code]["text"][int(rng.integers(0, len(world.META[code]["text"])))]
        base = [cid, center, stamp, site, str(age), months, sex]
        rows.append(base + ["1", text, world.PRODUCT_CODE[code], reason, _route(code, reason, rng), mg, outcome])
        if rng.random() < 0.055:
            other = OTHER_SUBSTANCES[int(rng.integers(0, len(OTHER_SUBSTANCES)))]
            rows.append(base + ["2", other, "", reason, "Ingestion", mg, outcome])
    return rows
