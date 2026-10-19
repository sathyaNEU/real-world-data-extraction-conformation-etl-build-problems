"""The truth behind task269's 2026 marks: 84 candidates, twelve stations, the same two examiners at each station.

Each examiner's mark for a candidate at a station is built in marks out of 20 from five sources: the candidate's
clinical performance, the station's difficulty, the candidate's performance on that case beyond their level
(case specificity), the examiner's own stringency (fixed for the examiner, so every candidate at that station
meets it), and the examiner's own reading of the encounter. The mark is turned into checklist points over the
items the simulated patient opened, and the points into item marks of 0, 1 or 2 that sum to them."""
import math
import numpy as np

import common as K

SEED = 11822
# variance components of one examiner's station mark, in marks out of 20 squared
SIG = {"p": 1.0, "pd": 0.9, "d": 0.8, "s": 1.0, "ps": 1.4, "rs": 1.2, "e": 1.0}
MU = 13.2
NA_SHARE = 0.10           # candidates at an NA station whose simulated patient did not give the cue


def _items(rng, points, n_items, ease):
    """Item marks of 0, 1 or 2 over n_items summing to points: the expected score of each item under a common
    location, solved so the expectations sum to points, then integerised by the largest remainders (jittered)."""
    if points <= 0:
        return [0] * n_items
    if points >= 2 * n_items:
        return [2] * n_items
    lo, hi = -12.0, 12.0
    for _ in range(60):
        mid = (lo + hi) / 2
        tot = sum(2.0 / (1.0 + math.exp(-1.3 * (mid + e))) for e in ease)
        lo, hi = (mid, hi) if tot < points else (lo, mid)
    exp_ = [2.0 / (1.0 + math.exp(-1.3 * ((lo + hi) / 2 + e))) for e in ease]
    base = [min(2, int(math.floor(x))) for x in exp_]
    rem = points - sum(base)
    frac = [(x - math.floor(x)) + rng.uniform(-0.15, 0.15) for x in exp_]
    order = sorted(range(n_items), key=lambda k: -frac[k])
    for k in order:
        if rem <= 0:
            break
        if base[k] < 2:
            base[k] += 1
            rem -= 1
    k = 0
    while rem > 0:                      # every remainder spent once each item can take no more
        if base[order[k % n_items]] < 2:
            base[order[k % n_items]] += 1
            rem -= 1
        k += 1
    return base


def marks(seed=SEED):
    """The 2026 sitting's truth: per candidate, station and examiner role the mark out of 20 the examiner meant,
    the points and item marks recorded, the withdrawn item's day-1 marks and each examiner's global grade."""
    r = np.random.default_rng([seed, 1])
    n, S = K.N_CAND26, len(K.STATIONS26)
    p = r.normal(0, math.sqrt(SIG["p"]), n)
    s = r.normal(0, math.sqrt(SIG["s"]), S)
    ps = r.normal(0, math.sqrt(SIG["ps"]), (n, S))
    rs = r.normal(0, math.sqrt(SIG["rs"]), (S, 2))
    e = r.normal(0, math.sqrt(SIG["e"]), (n, S, 2))
    # each candidate's strength in each of the blueprint's four domains, beyond their general level
    pd = r.normal(0, math.sqrt(SIG["pd"]), (n, len(K.DOMAINS)))
    dom = [K.DOMAINS.index(st[3]) for st in K.STATIONS26]
    dd = r.normal(0, math.sqrt(SIG["d"]), len(K.DOMAINS))      # how hard each domain's stations run
    true = (MU + p[:, None, None] + pd[:, dom][:, :, None] + dd[dom][None, :, None] + s[None, :, None]
            + ps[:, :, None] + rs[None, :, :] + e)
    ri = np.random.default_rng([seed, 2])
    ease = {}
    for st in K.STATIONS26:
        ease[st[0]] = list(ri.normal(0.3, 1.0, st[4]))
    na = {}
    rn = np.random.default_rng([seed, 3])
    for sno in K.NA_ITEMS:
        na[sno] = rn.random(n) < NA_SHARE
    rr = np.random.default_rng([seed, 4])
    rec = {}
    for i in range(n):
        for si, st in enumerate(K.STATIONS26):
            sno, n_items = st[0], st[4]
            items = list(range(1, n_items + 1))
            if sno == K.WITHDRAWN[0]:
                items = [k for k in items if k != K.WITHDRAWN[1]]
            if sno in K.NA_ITEMS and na[sno][i]:
                items = [k for k in items if k != K.NA_ITEMS[sno]]
            for ro in (0, 1):
                m = float(np.clip(true[i, si, ro], 1.5, 19.6))
                pts = int(round(m * 2 * len(items) / 20.0))
                eas = [ease[sno][k - 1] + float(rr.normal(0, 0.9)) for k in items]
                im = _items(rr, pts, len(items), eas)
                rec[(i, sno, ro)] = {"intended": m, "points": pts, "items": dict(zip(items, im)),
                                     "available": len(items)}
    # the withdrawn item: day-1 candidates were marked on it; examiners read its wording two ways
    rw = np.random.default_rng([seed, 5])
    wd = {}
    for i in range(n):
        for ro in (0, 1):
            wd[(i, ro)] = int(rw.choice([0, 1, 2], p=[0.35, 0.3, 0.35]))
    # global grades: the examiner's overall judgement, read off the mark they meant with their own noise
    rg = np.random.default_rng([seed, 6])
    gg = {}
    cuts = [9.5, 11.6, 14.2, 16.4]
    for key, v in rec.items():
        z = v["intended"] + rg.normal(0, 0.9)
        gg[key] = int(sum(z > c for c in cuts))
    return {"n": n, "p": p, "pd": pd, "s": s, "ps": ps, "rs": rs, "e": e, "true": true, "rec": rec, "withdrawn": wd,
            "global": gg, "na": na}


def station_marks(w, include_withdrawn=False, na_as_zero=False):
    """Each examiner's station mark out of 20 as the marking guide computes it: checklist points over the points
    the available items carry, scaled to 20 (the variants the fork table asserts are switches)."""
    n, S = w["n"], len(K.STATIONS26)
    y = np.zeros((n, S, 2))
    for i in range(n):
        for si, st in enumerate(K.STATIONS26):
            sno, n_items = st[0], st[4]
            for ro in (0, 1):
                v = w["rec"][(i, sno, ro)]
                pts, avail = v["points"], v["available"]
                if sno in K.NA_ITEMS and na_as_zero and K.NA_ITEMS[sno] not in v["items"]:
                    avail += 1
                if include_withdrawn and sno == K.WITHDRAWN[0] and i < 48:
                    pts += w["withdrawn"][(i, ro)]
                    avail += 1
                y[i, si, ro] = 20.0 * pts / (2.0 * avail)
    return y


# ---------------------------------------------------------------------------------------------------------------
# The case bank and its sitting history (the eligible-cases check)

TITLES = {
    "History taking": [
        "Chest pain: history", "Shortness of breath: history", "Palpitations: history", "Headache: history",
        "Tiredness in a young woman: history", "Altered bowel habit: history", "Weight loss: history",
        "Abdominal pain: history", "Low back pain: history", "Painful joints: history",
        "Cough and haemoptysis: history", "Dizziness: history", "Collapse: history",
        "Fever in a returning traveller: history", "Itchy rash: history", "Urinary symptoms in an older man: history",
        "Bleeding in early pregnancy: history", "Postmenopausal bleeding: history", "Breast lump: history",
        "Low mood: history", "Panic attacks: history", "Alcohol use: history", "Memory problems: history",
        "Falls in an older woman: history", "Diarrhoea: history", "Vomiting in a toddler: history",
        "Febrile infant: history", "Speech delay: history", "Poor sleep: history", "Swollen leg: history",
        "Calf pain after a flight: history", "Blurred vision: history", "Hearing loss: history",
        "Sore throat: history", "Difficulty swallowing: history", "Jaundice: history", "Blood in the urine: history",
        "Thirst and frequency: history", "Night sweats: history", "First seizure: history",
        "Numb hands: history", "Heavy periods: history", "Hoarse voice: history", "Groin swelling: history"],
    "Physical examination": [
        "Cardiovascular examination", "Respiratory examination", "Abdominal examination",
        "Cranial nerve examination", "Upper limb neurological examination", "Lower limb neurological examination",
        "Knee examination", "Hip examination", "Shoulder examination", "Hand examination", "Spine examination",
        "Thyroid examination", "Lymph node examination", "Breast examination", "Peripheral vascular examination",
        "Diabetic foot examination", "Cerebellar examination", "Examination for parkinsonism", "Fundoscopy",
        "Ear examination", "Newborn check", "Respiratory examination of a child", "Hernia examination",
        "Scrotal examination", "Digital rectal examination", "Speculum examination", "Gait and screening (GALS)",
        "Skin lesion examination", "Ankle examination", "Elbow examination", "Varicose vein examination",
        "Stoma examination", "Cardiovascular examination of a child", "Mental state examination",
        "Examination of a neck lump", "Examination of the visual fields", "Examination of a swollen leg",
        "Examination of a red eye", "Abdominal examination in pregnancy", "Examination of a transplant kidney"],
    "Communication": [
        "Explaining a new diagnosis of type 2 diabetes", "Breaking bad news: biopsy result",
        "Consent for a lumbar puncture", "Consent for an endoscopy", "Starting warfarin", "Inhaler technique",
        "Stopping smoking", "Brief alcohol intervention", "An angry relative", "Disclosing a medication error",
        "Resuscitation decisions with a family", "An abnormal smear result", "Planning a discharge home",
        "Handing over a deteriorating patient", "Explaining a statin", "Starting insulin",
        "A request for antibiotics", "Explaining a colonoscopy result", "Telephone advice to a parent",
        "A patient who wants to leave against advice", "Explaining epilepsy and driving", "Explaining a CT finding",
        "Discussing a DNA test result", "A complaint about waiting times", "Explaining HbA1c",
        "Explaining asthma action plans", "Talking with an interpreter", "Explaining a stroke diagnosis",
        "Explaining a miscarriage", "Discussing weight with a teenager", "Explaining a referral to psychiatry",
        "Explaining an MRI scan", "Consent for a blood transfusion", "Explaining contraception options",
        "Explaining a cancelled operation", "Discussing a frail parent's care", "Explaining osteoporosis treatment",
        "Explaining a positive pregnancy test"],
    "Procedural skills": [
        "Venepuncture and blood cultures", "Peripheral cannulation", "Male urinary catheterisation",
        "Female urinary catheterisation", "Adult basic life support", "Recording a 12-lead ECG",
        "Arterial blood gas sampling", "Simple interrupted suturing", "Intramuscular injection",
        "Nasogastric tube insertion", "Capillary blood glucose", "Peak flow measurement",
        "Prescribing insulin", "Prescribing intravenous fluids", "Checking a blood transfusion", "Urinalysis",
        "Skin closure with staples", "Bag-valve-mask ventilation", "Subcutaneous injection",
        "Wound dressing", "Taking a throat swab", "Paediatric basic life support", "Setting up a nebuliser",
        "Removing a cannula", "Measuring visual acuity", "Interpreting a chest radiograph", "Interpreting an ECG",
        "Measuring blood pressure", "Using an automated defibrillator", "Prescribing for pain",
        "Preparing an infusion", "Blood pressure in a child", "Applying a back slab", "Knee aspiration",
        "Taking a wound swab", "Prescribing anticoagulation"],
}
SPECIALTY = ["Cardiology", "Respiratory", "Gastroenterology", "Endocrinology", "Neurology", "Musculoskeletal",
             "Obstetrics and gynaecology", "Paediatrics", "Psychiatry", "General practice", "Emergency medicine",
             "Surgery", "Renal", "Dermatology", "Older people", "ENT", "Ophthalmology", "Haematology"]
SP_NEED = {"SP", "SP and task trainer"}

# the resources a station on each title runs with, the usual one first; a title not listed runs with a simulated patient
RESOURCES_OF = {
    "Fundoscopy": ("Manikin", "SP"), "Ear examination": ("Manikin", "SP"), "Newborn check": ("Manikin",),
    "Respiratory examination of a child": ("Manikin", "Video"), "Cardiovascular examination of a child": ("Manikin", "Video"),
    "Digital rectal examination": ("Task trainer",), "Speculum examination": ("Task trainer",),
    "Breast examination": ("Task trainer", "SP"), "Scrotal examination": ("Task trainer",),
    "Skin lesion examination": ("SP", "Video"), "Examination of a red eye": ("SP", "Video"),
    "Abdominal examination in pregnancy": ("SP", "Task trainer"), "Mental state examination": ("SP", "Video"),
    "Venepuncture and blood cultures": ("Task trainer", "SP and task trainer"),
    "Peripheral cannulation": ("Task trainer", "SP and task trainer"),
    "Male urinary catheterisation": ("Manikin", "Task trainer"), "Female urinary catheterisation": ("Manikin", "Task trainer"),
    "Adult basic life support": ("Manikin",), "Recording a 12-lead ECG": ("SP", "Manikin"),
    "Arterial blood gas sampling": ("Task trainer",), "Simple interrupted suturing": ("Task trainer",),
    "Intramuscular injection": ("Task trainer", "SP and task trainer"), "Nasogastric tube insertion": ("Manikin",),
    "Capillary blood glucose": ("SP and task trainer", "Task trainer"), "Peak flow measurement": ("SP",),
    "Prescribing insulin": ("Paper case",), "Prescribing intravenous fluids": ("Paper case",),
    "Checking a blood transfusion": ("SP and task trainer", "Manikin"), "Urinalysis": ("Task trainer",),
    "Skin closure with staples": ("Task trainer",), "Bag-valve-mask ventilation": ("Manikin",),
    "Subcutaneous injection": ("Task trainer", "SP and task trainer"),
    "Wound dressing": ("Task trainer", "SP and task trainer"), "Taking a throat swab": ("SP",),
    "Paediatric basic life support": ("Manikin",), "Setting up a nebuliser": ("SP", "Manikin"),
    "Removing a cannula": ("SP and task trainer", "Task trainer"), "Measuring visual acuity": ("SP",),
    "Interpreting a chest radiograph": ("Paper case",), "Interpreting an ECG": ("Paper case",),
    "Measuring blood pressure": ("SP",), "Using an automated defibrillator": ("Manikin",),
    "Prescribing for pain": ("Paper case",), "Preparing an infusion": ("Task trainer",),
    "Blood pressure in a child": ("Manikin",), "Applying a back slab": ("SP",), "Knee aspiration": ("Task trainer",),
    "Taking a wound swab": ("SP and task trainer", "Task trainer"), "Prescribing anticoagulation": ("Paper case",),
}


def resources_of(title):
    return RESOURCES_OF.get(title, ("SP",))

# each title's specialty, and the other specialty a different case of the same title is written for
SPECIALTY_OF = {
    "Chest pain: history": ("Cardiology", "Emergency medicine"),
    "Shortness of breath: history": ("Respiratory", "Cardiology"),
    "Palpitations: history": ("Cardiology", "Endocrinology"),
    "Headache: history": ("Neurology", "General practice"),
    "Tiredness in a young woman: history": ("General practice", "Haematology"),
    "Altered bowel habit: history": ("Gastroenterology", "Surgery"),
    "Weight loss: history": ("Gastroenterology", "Oncology"),
    "Abdominal pain: history": ("Surgery", "Gastroenterology"),
    "Low back pain: history": ("Musculoskeletal", "General practice"),
    "Painful joints: history": ("Musculoskeletal", "General practice"),
    "Cough and haemoptysis: history": ("Respiratory", "Oncology"),
    "Dizziness: history": ("Older people", "ENT"),
    "Collapse: history": ("Emergency medicine", "Cardiology"),
    "Fever in a returning traveller: history": ("Infectious diseases", "Emergency medicine"),
    "Itchy rash: history": ("Dermatology", "General practice"),
    "Urinary symptoms in an older man: history": ("Urology", "General practice"),
    "Bleeding in early pregnancy: history": ("Obstetrics and gynaecology", "Emergency medicine"),
    "Postmenopausal bleeding: history": ("Obstetrics and gynaecology", "Oncology"),
    "Breast lump: history": ("Surgery", "General practice"),
    "Low mood: history": ("Psychiatry", "General practice"),
    "Panic attacks: history": ("Psychiatry", "General practice"),
    "Alcohol use: history": ("Psychiatry", "Gastroenterology"),
    "Memory problems: history": ("Older people", "Neurology"),
    "Falls in an older woman: history": ("Older people", "Emergency medicine"),
    "Diarrhoea: history": ("Gastroenterology", "Infectious diseases"),
    "Vomiting in a toddler: history": ("Paediatrics", "Emergency medicine"),
    "Febrile infant: history": ("Paediatrics", "Emergency medicine"),
    "Speech delay: history": ("Paediatrics", "ENT"),
    "Poor sleep: history": ("General practice", "Psychiatry"),
    "Swollen leg: history": ("General practice", "Cardiology"),
    "Calf pain after a flight: history": ("Emergency medicine", "Haematology"),
    "Blurred vision: history": ("Ophthalmology", "Neurology"),
    "Hearing loss: history": ("ENT", "Older people"),
    "Sore throat: history": ("ENT", "General practice"),
    "Difficulty swallowing: history": ("Gastroenterology", "ENT"),
    "Jaundice: history": ("Gastroenterology", "Surgery"),
    "Blood in the urine: history": ("Urology", "Renal"),
    "Thirst and frequency: history": ("Endocrinology", "General practice"),
    "Night sweats: history": ("Haematology", "Infectious diseases"),
    "First seizure: history": ("Neurology", "Emergency medicine"),
    "Numb hands: history": ("Neurology", "Musculoskeletal"),
    "Heavy periods: history": ("Obstetrics and gynaecology", "Haematology"),
    "Hoarse voice: history": ("ENT", "Oncology"),
    "Groin swelling: history": ("Surgery", "General practice"),
    "Cardiovascular examination": ("Cardiology", "General practice"),
    "Respiratory examination": ("Respiratory", "General practice"),
    "Abdominal examination": ("Gastroenterology", "Surgery"),
    "Cranial nerve examination": ("Neurology", "Ophthalmology"),
    "Upper limb neurological examination": ("Neurology", "Musculoskeletal"),
    "Lower limb neurological examination": ("Neurology", "Endocrinology"),
    "Knee examination": ("Musculoskeletal", "Emergency medicine"),
    "Hip examination": ("Musculoskeletal", "Older people"),
    "Shoulder examination": ("Musculoskeletal", "General practice"),
    "Hand examination": ("Musculoskeletal", "Surgery"),
    "Spine examination": ("Musculoskeletal", "Emergency medicine"),
    "Thyroid examination": ("Endocrinology", "Surgery"),
    "Lymph node examination": ("Haematology", "Oncology"),
    "Breast examination": ("Surgery", "General practice"),
    "Peripheral vascular examination": ("Surgery", "Endocrinology"),
    "Diabetic foot examination": ("Endocrinology", "Surgery"),
    "Cerebellar examination": ("Neurology", "Older people"),
    "Examination for parkinsonism": ("Neurology", "Older people"),
    "Fundoscopy": ("Ophthalmology", "Endocrinology"),
    "Ear examination": ("ENT", "Paediatrics"),
    "Newborn check": ("Paediatrics", "General practice"),
    "Respiratory examination of a child": ("Paediatrics", "Respiratory"),
    "Hernia examination": ("Surgery", "General practice"),
    "Scrotal examination": ("Urology", "Surgery"),
    "Digital rectal examination": ("Surgery", "Urology"),
    "Speculum examination": ("Obstetrics and gynaecology", "General practice"),
    "Gait and screening (GALS)": ("Musculoskeletal", "Older people"),
    "Skin lesion examination": ("Dermatology", "Surgery"),
    "Ankle examination": ("Musculoskeletal", "Emergency medicine"),
    "Elbow examination": ("Musculoskeletal", "Emergency medicine"),
    "Varicose vein examination": ("Surgery", "General practice"),
    "Stoma examination": ("Surgery", "Gastroenterology"),
    "Cardiovascular examination of a child": ("Paediatrics", "Cardiology"),
    "Mental state examination": ("Psychiatry", "Emergency medicine"),
    "Examination of a neck lump": ("ENT", "Surgery"),
    "Examination of the visual fields": ("Ophthalmology", "Neurology"),
    "Examination of a swollen leg": ("General practice", "Surgery"),
    "Examination of a red eye": ("Ophthalmology", "Emergency medicine"),
    "Abdominal examination in pregnancy": ("Obstetrics and gynaecology", "General practice"),
    "Examination of a transplant kidney": ("Renal", "Surgery"),
    "Explaining a new diagnosis of type 2 diabetes": ("Endocrinology", "General practice"),
    "Breaking bad news: biopsy result": ("Oncology", "Surgery"),
    "Consent for a lumbar puncture": ("Neurology", "Emergency medicine"),
    "Consent for an endoscopy": ("Gastroenterology", "Surgery"),
    "Starting warfarin": ("Haematology", "Cardiology"),
    "Inhaler technique": ("Respiratory", "General practice"),
    "Stopping smoking": ("General practice", "Respiratory"),
    "Brief alcohol intervention": ("General practice", "Emergency medicine"),
    "An angry relative": ("Older people", "Emergency medicine"),
    "Disclosing a medication error": ("Surgery", "Older people"),
    "Resuscitation decisions with a family": ("Older people", "Oncology"),
    "An abnormal smear result": ("Obstetrics and gynaecology", "General practice"),
    "Planning a discharge home": ("Older people", "Surgery"),
    "Handing over a deteriorating patient": ("Emergency medicine", "Surgery"),
    "Explaining a statin": ("Cardiology", "General practice"),
    "Starting insulin": ("Endocrinology", "General practice"),
    "A request for antibiotics": ("General practice", "Infectious diseases"),
    "Explaining a colonoscopy result": ("Gastroenterology", "Surgery"),
    "Telephone advice to a parent": ("Paediatrics", "General practice"),
    "A patient who wants to leave against advice": ("Emergency medicine", "Psychiatry"),
    "Explaining epilepsy and driving": ("Neurology", "General practice"),
    "Explaining a CT finding": ("Emergency medicine", "Oncology"),
    "Discussing a DNA test result": ("Oncology", "Paediatrics"),
    "A complaint about waiting times": ("General practice", "Emergency medicine"),
    "Explaining HbA1c": ("Endocrinology", "General practice"),
    "Explaining asthma action plans": ("Respiratory", "Paediatrics"),
    "Talking with an interpreter": ("General practice", "Obstetrics and gynaecology"),
    "Explaining a stroke diagnosis": ("Neurology", "Older people"),
    "Explaining a miscarriage": ("Obstetrics and gynaecology", "Emergency medicine"),
    "Discussing weight with a teenager": ("Paediatrics", "General practice"),
    "Explaining a referral to psychiatry": ("Psychiatry", "General practice"),
    "Explaining an MRI scan": ("Neurology", "Musculoskeletal"),
    "Consent for a blood transfusion": ("Haematology", "Surgery"),
    "Explaining contraception options": ("General practice", "Obstetrics and gynaecology"),
    "Explaining a cancelled operation": ("Surgery", "Anaesthetics"),
    "Discussing a frail parent's care": ("Older people", "General practice"),
    "Explaining osteoporosis treatment": ("Older people", "Musculoskeletal"),
    "Explaining a positive pregnancy test": ("General practice", "Obstetrics and gynaecology"),
    "Venepuncture and blood cultures": ("Emergency medicine", "Infectious diseases"),
    "Peripheral cannulation": ("Emergency medicine", "Anaesthetics"),
    "Male urinary catheterisation": ("Urology", "Surgery"),
    "Female urinary catheterisation": ("Urology", "Obstetrics and gynaecology"),
    "Adult basic life support": ("Emergency medicine", "Cardiology"),
    "Recording a 12-lead ECG": ("Cardiology", "Emergency medicine"),
    "Arterial blood gas sampling": ("Respiratory", "Emergency medicine"),
    "Simple interrupted suturing": ("Surgery", "Emergency medicine"),
    "Intramuscular injection": ("General practice", "Psychiatry"),
    "Nasogastric tube insertion": ("Gastroenterology", "Surgery"),
    "Capillary blood glucose": ("Endocrinology", "Paediatrics"),
    "Peak flow measurement": ("Respiratory", "General practice"),
    "Prescribing insulin": ("Endocrinology", "Surgery"),
    "Prescribing intravenous fluids": ("Surgery", "Renal"),
    "Checking a blood transfusion": ("Haematology", "Surgery"),
    "Urinalysis": ("Renal", "General practice"),
    "Skin closure with staples": ("Surgery", "Emergency medicine"),
    "Bag-valve-mask ventilation": ("Anaesthetics", "Emergency medicine"),
    "Subcutaneous injection": ("Haematology", "General practice"),
    "Wound dressing": ("Surgery", "General practice"),
    "Taking a throat swab": ("ENT", "Infectious diseases"),
    "Paediatric basic life support": ("Paediatrics", "Emergency medicine"),
    "Setting up a nebuliser": ("Respiratory", "Paediatrics"),
    "Removing a cannula": ("Surgery", "Emergency medicine"),
    "Measuring visual acuity": ("Ophthalmology", "General practice"),
    "Interpreting a chest radiograph": ("Respiratory", "Emergency medicine"),
    "Interpreting an ECG": ("Cardiology", "Emergency medicine"),
    "Measuring blood pressure": ("General practice", "Cardiology"),
    "Using an automated defibrillator": ("Emergency medicine", "Cardiology"),
    "Prescribing for pain": ("Anaesthetics", "Surgery"),
    "Preparing an infusion": ("Anaesthetics", "Surgery"),
    "Blood pressure in a child": ("Paediatrics", "Renal"),
    "Applying a back slab": ("Musculoskeletal", "Emergency medicine"),
    "Knee aspiration": ("Musculoskeletal", "Emergency medicine"),
    "Taking a wound swab": ("Infectious diseases", "Surgery"),
    "Prescribing anticoagulation": ("Haematology", "Cardiology"),
}
SITTINGS = []                                          # (label, date, year, n stations)
for _y in range(2021, 2027):
    SITTINGS.append(("Final OSCE May %d" % _y, None, _y, 12))
    SITTINGS.append(("Final OSCE Supplemental Aug %d" % _y, None, _y, 8))



# a pending revision completed at the cut-over sometimes renamed the case in the new bank
REVISED_TITLE = {
    "Blood in the urine: history": "Visible haematuria: history",
    "Thirst and frequency: history": "Polyuria and polydipsia: history",
    "Calf pain after a flight: history": "A painful swollen calf: history",
    "Fever in a returning traveller: history": "Fever after travel abroad: history",
    "Difficulty swallowing: history": "Dysphagia: history",
    "Numb hands: history": "Tingling fingers: history",
    "Hoarse voice: history": "A change in the voice: history",
    "Collapse: history": "Transient loss of consciousness: history",
    "Memory problems: history": "Forgetfulness in an older adult: history",
    "Thyroid examination": "Examination of a goitre",
    "Lymph node examination": "Lymphadenopathy: examination",
    "Peripheral vascular examination": "Arterial examination of the legs",
    "Cerebellar examination": "Coordination and gait: examination",
    "Examination for parkinsonism": "Tremor: examination",
    "Ear examination": "Otoscopy",
    "Fundoscopy": "Ophthalmoscopy",
    "Hernia examination": "Groin examination",
    "Starting warfarin": "Anticoagulation counselling",
    "Inhaler technique": "Teaching an inhaler",
    "Stopping smoking": "Smoking cessation advice",
    "An angry relative": "A distressed relative",
    "Explaining a statin": "Lipid-lowering treatment: explanation",
    "A request for antibiotics": "Antibiotics for a viral illness",
    "Explaining HbA1c": "A raised blood sugar result",
    "Talking with an interpreter": "Consultation through an interpreter",
    "Discussing a frail parent's care": "Planning care for a frail parent",
    "Peripheral cannulation": "Intravenous cannulation",
    "Recording a 12-lead ECG": "Performing an electrocardiogram",
    "Arterial blood gas sampling": "Radial arterial puncture",
    "Capillary blood glucose": "Finger-prick glucose testing",
    "Peak flow measurement": "Measuring expiratory flow",
    "Urinalysis": "Dipstick urine testing",
    "Bag-valve-mask ventilation": "Airway support with a bag and mask",
    "Wound dressing": "Dressing a surgical wound",
    "Taking a throat swab": "Pharyngeal swab",
    "Measuring blood pressure": "Manual sphygmomanometry",
}
for _old, _new in REVISED_TITLE.items():
    SPECIALTY_OF[_new] = SPECIALTY_OF[_old]
    if _old in RESOURCES_OF:
        RESOURCES_OF[_new] = RESOURCES_OF[_old]


def bank(seed=SEED):
    """The case bank as it stood at the 30 November 2026 export, every final OSCE sitting's cases since 2021, and
    the records the November 2025 migration re-created. A case whose revision was pending at the cut-over was
    re-created under a new code at the next version and its old record retired; the assessment group signed the
    revision off on the new record in 2026, so its review date is that sign-off. Its sitting history stays under the
    old code. Retired records of the same specialty sit beside each old record, and a case retired outright at the
    migration may have a newer case of the same title that is a different case. Legacy codes run in the order the
    cases were written; the new bank numbers its records as it creates them."""
    import datetime as dt
    r = np.random.default_rng([seed, 21])
    rc = np.random.default_rng([seed, 24])     # the codes
    rs = np.random.default_rng([seed, 25])     # the sign-offs in the new bank and the retired records beside them
    day = lambda a, b: a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
    wday = lambda a, b: _weekday_on_or_after(a + dt.timedelta(days=int(rs.integers(0, (b - a).days + 1))))
    mig = K.BANK_MIGRATION
    cases, usage, recreated = [], [], []
    nxt = {"CV-25": 100, "CV-26": 0}

    def cv_codes(prefix, n):
        out = []
        for _ in range(n):
            nxt[prefix] += int(rc.integers(1, 9))
            out.append("%s-%04d" % (prefix, nxt[prefix]))
        rc.shuffle(out)
        return iter(out)
    sit_dates = {("May", 2021): dt.date(2021, 5, 11), ("May", 2022): dt.date(2022, 5, 12),
                 ("May", 2023): dt.date(2023, 5, 16), ("May", 2024): dt.date(2024, 5, 14),
                 ("May", 2025): dt.date(2025, 5, 13), ("May", 2026): K.SIT26[0],
                 ("Aug", 2021): dt.date(2021, 8, 23), ("Aug", 2022): dt.date(2022, 8, 18),
                 ("Aug", 2023): dt.date(2023, 8, 22), ("Aug", 2024): dt.date(2024, 8, 20),
                 ("Aug", 2025): dt.date(2025, 8, 21), ("Aug", 2026): dt.date(2026, 8, 20)}
    spec = lambda t: SPECIALTY_OF[t][0]
    has_sp = lambda t: any(x in SP_NEED for x in resources_of(t))
    for d in K.DOMAINS:
        pre = K.DOMAIN_PREFIX[d]
        titles = list(TITLES[d])
        fixed = [st for st in K.STATIONS26 if st[3] == d]
        for st in fixed:
            titles.remove(st[2])
        r.shuffle(titles)
        nums = sorted(r.choice(np.arange(1, 70), size=60, replace=False).tolist())
        used_nums = {int(st[1].split("-")[1]) for st in fixed}
        nums = [x for x in nums if x not in used_nums]
        c25, c26 = cv_codes("CV-25", 7), cv_codes("CV-26", 3)

        def take(need_sp=None, revisable=False, sibling=None):
            """the next title whose station can (or cannot) need a simulated patient (and, for a case renamed at
            the cut-over, one the revision renamed; with sibling, one whose specialty has another title left, one
            that can need a simulated patient when sibling is "sp")"""
            for i in range(len(titles) - 1, -1, -1):
                t = titles[i]
                if revisable and t not in REVISED_TITLE:
                    continue
                if need_sp is not None and not any((x in SP_NEED) == need_sp for x in resources_of(t)):
                    continue
                if sibling and not any(x != t and spec(x) == spec(t) and (sibling == "any" or has_sp(x))
                                       for x in titles):
                    continue
                return titles.pop(i)
            raise AssertionError("no %s title left in %s" % (need_sp, d))

        def take_sib(t, need_sp=False, res=None):
            """a title left of t's specialty (one that can need a simulated patient when need_sp), one whose station
            can use res when there is one"""
            for strict in (True, False):
                for i in range(len(titles) - 1, -1, -1):
                    x = titles[i]
                    if spec(x) == spec(t) and (not need_sp or has_sp(x)) and (not strict or res is None
                                                                             or res in resources_of(x)):
                        return titles.pop(i)
            raise AssertionError("no title of %s's specialty left in %s" % (t, d))

        def res_pick(title, need_sp=None):
            opts = [x for x in resources_of(title) if need_sp is None or (x in SP_NEED) == need_sp]
            return opts[0] if len(opts) == 1 or r.random() < 0.7 else opts[1]

        def new_case(cat, title, code, res, created, reviewed, status, version, history, origin=None):
            r.choice(SPECIALTY)   # the draw the bank's stream was cut with; the title fixes the specialty
            c = {"code": code, "title": title, "domain": d, "specialty": SPECIALTY_OF[title][0], "resources": res,
                 "version": version, "created": created, "reviewed": reviewed, "status": status, "cat": cat,
                 "history": history, "origin": origin}
            cases.append(c)
            return c

        def recent_review():
            return day(dt.date(2024, 6, 3), dt.date(2026, 10, 30))

        def old_review():
            return day(dt.date(2021, 3, 1), dt.date(2024, 4, 26))

        def free_version(t, res, ver):
            """an old record's version, other than another old record's of the same specialty and resources"""
            taken = {c["version"] for c in cases if c["domain"] == d and c["cat"] == "recreated_old"
                     and c["specialty"] == spec(t) and c["resources"] == res}
            return ver if ver not in taken else min(v for v in range(1, 6) if v not in taken)

        def signed_off():
            return wday(dt.date(2026, 1, 13), dt.date(2026, 10, 22))

        # the three 2026 stations: legacy codes, set in May 2026
        for st in fixed:
            new_case("set_2026", st[2], st[1], st[5], day(dt.date(2014, 1, 1), dt.date(2021, 12, 31)),
                     day(dt.date(2024, 9, 1), dt.date(2026, 2, 27)), "Active", int(r.integers(2, 5)),
                     [("May", 2026)])
        # the August 2026 supplemental: two legacy cases under their own codes
        for _ in range(2):
            t = take()
            new_case("set_aug26", t, None, res_pick(t), day(dt.date(2014, 1, 1), dt.date(2022, 6, 30)),
                     recent_review(), "Active", int(r.integers(1, 4)), [("Aug", 2026)])
        # the August 2025 supplemental's unchanged case
        t = take()
        new_case("set_aug25", t, None, res_pick(t), day(dt.date(2014, 1, 1), dt.date(2022, 6, 30)),
                 recent_review(), "Active", int(r.integers(1, 4)), [("Aug", 2025)])
        # the device: three cases set in 2025 under their old codes and re-created at the migration, the revision
        # signed off on the new record in 2026; beside each old record, a retired record of the same specialty that
        # the assessment group retired at the cut-over after reviewing it later in 2025
        dev_sp = {"History taking": [True, True, True], "Physical examination": [True, True, False],
                  "Communication": [True, True, True], "Procedural skills": [True, False, False]}[d]
        for k, (mon, need_sp) in enumerate(zip(["May", "May", "Aug"], dev_sp)):
            renamed = k < 2                       # the revision renamed two of the three
            t = take(need_sp, revisable=renamed, sibling="any")
            res = res_pick(t, need_sp)
            ver = free_version(t, res, int(r.integers(1, 4)))
            old = new_case("recreated_old", t, None, res, day(dt.date(2014, 1, 1), dt.date(2021, 12, 31)),
                           day(dt.date(2024, 6, 3), dt.date(2025, 9, 30)), "Retired", ver, [(mon, 2025)])
            nc = new_case("device", REVISED_TITLE[t] if renamed else t, next(c25), res, mig, signed_off(),
                          "Active", ver + 1, [], origin=old)
            nc["specialty"] = old["specialty"]
            sib = take_sib(t, res=res)
            new_case("decoy", sib, None, res if res in resources_of(sib) else res_pick(sib),
                     day(dt.date(2013, 1, 1), dt.date(2020, 12, 31)),
                     wday(old["reviewed"] + dt.timedelta(days=14), dt.date(2025, 11, 6)), "Retired",
                     int(rs.choice([v for v in (1, 2, 3, 4, 5) if v != ver])), [])
        # two re-created cases not set in 2025 or 2026 (last set earlier or never): eligible
        cleans = []
        for k in range(2):
            t = take(True if k == 0 else None, sibling="sp" if k == 0 else None)
            res = res_pick(t, True if k == 0 else None)
            ver = free_version(t, res, int(r.integers(1, 4)))
            old = new_case("recreated_old", t, None, res, day(dt.date(2014, 1, 1), dt.date(2020, 12, 31)),
                           day(dt.date(2024, 6, 3), dt.date(2025, 10, 31)), "Retired", ver, [])
            old["clean"] = True
            new_case("recreated_clean", t, next(c25), res, mig, signed_off(), "Active", ver + 1, [], origin=old)
            cleans.append((t, res, ver))
        # a case of the first one's specialty retired outright at the migration after its May 2025 sitting, and a
        # newer case of the same title
        t0, res0, ver0 = cleans[0]
        t = take_sib(t0, need_sp=True, res=res0)
        new_case("retired_twin_old", t, None, res0 if res0 in resources_of(t) else res_pick(t, True),
                 day(dt.date(2014, 1, 1), dt.date(2020, 12, 31)), day(dt.date(2023, 1, 1), dt.date(2025, 3, 31)),
                 "Retired", int(rs.choice([v for v in (1, 2, 3, 4) if v != ver0])), [("May", 2025)])
        new_case("twin_new", t, next(c26), res_pick(t, True),
                 day(dt.date(2026, 2, 2), dt.date(2026, 6, 30)), None, "Active", 1, [])
        cases[-1]["reviewed"] = cases[-1]["created"] + dt.timedelta(days=int(r.integers(10, 50)))
        # cases authored in the new bank after the cut-over, in 2025 and in 2026
        for _ in range(2):
            t = take()
            c = new_case("new25", t, next(c25), res_pick(t),
                         day(dt.date(2025, 11, 20), dt.date(2025, 12, 19)), None, "Active", 1, [])
            c["reviewed"] = c["created"] + dt.timedelta(days=int(r.integers(10, 40)))
        for _ in range(2):
            t = take()
            c = new_case("new26", t, next(c26), res_pick(t),
                         day(dt.date(2026, 1, 12), dt.date(2026, 9, 25)), None, "Active", 1, [])
            c["reviewed"] = c["created"] + dt.timedelta(days=int(r.integers(10, 50)))
        # the rest of the legacy bank: earlier sittings, never set, under review, retired over the years
        while titles:
            t = titles.pop()
            u = r.random()
            if u < 0.10:
                status = "Retired"
            elif u < 0.18:
                status = "Under review"
            elif u < 0.30:
                status = "Active - edits pending"
            else:
                status = "Active"
            rev = recent_review() if r.random() < 0.62 else old_review()
            if status == "Retired" and rev >= mig:
                rev = old_review()
            new_case("legacy", t, None, res_pick(t), day(dt.date(2013, 1, 1), dt.date(2020, 12, 31)), rev,
                     status, int(r.integers(1, 5)), [])
        # legacy codes in the order the cases were written, the bank's unused and deleted numbers between them
        mine = [c for c in cases if c["domain"] == d and c["code"] is None]
        mine.sort(key=lambda c: (c["created"], c["title"]))
        pick = sorted(rc.choice(len(nums), size=len(mine), replace=False).tolist())
        for c, j in zip(mine, pick):
            c["code"] = "%s-%03d" % (pre, nums[j])
        # a re-created record's old record is the one retired record of its domain, specialty and resources at the
        # version before
        olds = [c["origin"] for c in cases if c["domain"] == d and isinstance(c["origin"], dict)]
        for o in olds:
            for x in cases:
                if (x is not o and x["domain"] == d and x["status"] == "Retired" and x["specialty"] == o["specialty"]
                        and x["resources"] == o["resources"] and x["version"] == o["version"]):
                    assert not any(x is y for y in olds), "two old records alike in %s" % d
                    x["version"] = [v for v in (1, 2, 3, 4, 5, 6) if v != o["version"]][int(rs.integers(0, 5))]
        for c in cases:
            if c["domain"] == d and isinstance(c["origin"], dict):
                o = c["origin"]
                c["origin"] = o["code"]
                recreated.append((o["code"], c["code"], o["title"]))
    # the assessment group reviews cases at its weekday meetings
    for c in cases:
        c["reviewed"] = _weekday_on_or_after(c["reviewed"])
    # the 2021 to 2024 sittings: three cases a domain in May and two in August, from the legacy cases (not the
    # ones under review), the re-created cases' old records and the cases retired since; never the same case in
    # consecutive years
    last = {}
    for y in range(2021, 2025):
        for mon, k in (("May", 3), ("Aug", 2)):
            for d in K.DOMAINS:
                pool = [c for c in cases if c["domain"] == d and c["cat"] in ("legacy", "recreated_old", "decoy")
                        and c["status"] != "Under review" and c["created"] < sit_dates[(mon, y)]
                        and not any(yy >= y - 1 for _, yy in c["history"])
                        and (c["cat"] in ("legacy", "decoy") or c.get("clean"))]
                pool = sorted(pool, key=lambda c: c["code"])
                pick = r.choice(len(pool), size=k, replace=False)
                for j in sorted(pick.tolist()):
                    pool[j]["history"].append((mon, y))
    # the usage rows, station numbers interleaving the domains as the circuit runs
    usage = []
    for y in range(2021, 2027):
        for mon in ("May", "Aug"):
            label = "Final OSCE May %d" % y if mon == "May" else "Final OSCE Supplemental August %d" % y
            per = {d: sorted([c for c in cases if c["domain"] == d and (mon, y) in c["history"]],
                             key=lambda c: c["code"]) for d in K.DOMAINS}
            if (mon, y) == ("May", 2026):
                for st in K.STATIONS26:
                    c = [x for x in per[st[3]] if x["code"] == st[1]][0]
                    usage.append({"sitting": label, "date": sit_dates[(mon, y)], "station": st[0], "code": c["code"],
                                  "title": c["title"]})
                continue
            n = 3 if mon == "May" else 2
            for d in K.DOMAINS:
                assert len(per[d]) == n, (mon, y, d, len(per[d]))
            sno = 0
            for k in range(n):
                for d in K.DOMAINS:
                    sno += 1
                    c = per[d][k]
                    usage.append({"sitting": label, "date": sit_dates[(mon, y)], "station": sno, "code": c["code"],
                                  "title": c["title"]})
    return {"cases": cases, "recreated": recreated, "sit_dates": sit_dates, "usage": usage, "seed": seed}


def bank_truth(b):
    """Per domain, the cases eligible for May 2027 and how many of them need a simulated patient: active (edits
    pending included), reviewed on or after 11 May 2024, and the case not set at a final OSCE sitting in 2025 or
    2026, a re-created case carrying its old record's sittings."""
    exposed_codes = {u["code"] for u in b["usage"] if u["date"].year in K.EXPOSURE_YEARS}
    origin = {new: old for old, new, _ in b["recreated"]}
    out = {}
    for d in K.DOMAINS:
        el = [c for c in b["cases"] if c["domain"] == d and c["status"] in ("Active", "Active - edits pending")
              and c["reviewed"] >= K.REVIEW_FROM and c["code"] not in exposed_codes
              and origin.get(c["code"]) not in exposed_codes]
        out[d] = (len(el), sum(1 for c in el if c["resources"] in SP_NEED))
    return out



# ---------------------------------------------------------------------------------------------------------------
# The examiner register, the training record and the 2027 availability form (the eligible-examiners check)

ELIGIBLE_GRADES = {"Professor", "Associate Professor", "Senior Lecturer", "Lecturer", "Consultant", "GP Trainer"}
VENUES = ["Clinical Skills Centre", "CUH Postgraduate Centre", "Fennabeg Clinical Skills Unit"]
HOME_VENUE = {"CUH": (VENUES[1], "H"), "Fennabeg": (VENUES[2], "F")}   # a base's own venue and its staff numbers
BASES = [("Callowfield", 82, ["Professor", "Associate Professor", "Senior Lecturer", "Lecturer", "Clinical Tutor"],
          [0.10, 0.15, 0.30, 0.33, 0.12]),
         ("CUH", 112, ["Consultant", "Specialist Registrar"], [0.84, 0.16]),
         ("Fennabeg", 96, ["Consultant", "Senior Lecturer", "Lecturer", "Specialist Registrar", "Clinical Tutor"],
          [0.40, 0.18, 0.22, 0.10, 0.10]),
         ("General practice", 46, ["GP Trainer", "GP"], [0.70, 0.30])]
SITE_OF_BASE = {"Callowfield": ["CSC", "CUH"], "CUH": ["CUH", "CSC"], "Fennabeg": ["FCS"],
                "General practice": ["FCS", "CSC", "CUH"]}
IRISH_FORE = ["Seán", "Siobhán", "Pádraig", "Niamh", "Aoife", "Órla", "Éanna", "Ciarán", "Máire", "Dónal",
              "Caoimhe", "Ruairí", "Sinéad", "Tomás", "Bríd", "Áine", "Eoghan", "Clíona"]
IRISH_SUR = ["Ó Briain", "Ní Cheallaigh", "Mac Giolla Phádraig", "Ó Súilleabháin", "Ní Bhriain", "Ó Dónaill",
             "Mac Cárthaigh", "Ó Ceallaigh", "Nic Aodha", "Ó Murchú", "Ní Mhurchú", "Ó Sé"]


IRISH_MALE = {"Seán", "Pádraig", "Éanna", "Ciarán", "Dónal", "Ruairí", "Tomás", "Eoghan"}
WEEKDAY_HOLIDAYS = {(1, 1), (3, 17), (12, 24), (12, 25), (12, 26), (12, 27), (12, 28), (12, 29), (12, 30), (12, 31)}


def _gender(fore):
    """M or F where the forename lists say one, else None."""
    from faker.providers.person.en_IE import Provider
    if fore in IRISH_FORE:
        return "M" if fore in IRISH_MALE else "F"
    m, f = fore in Provider.first_names_male, fore in Provider.first_names_female
    return "M" if m and not f else ("F" if f and not m else None)


def _weekday_on_or_after(d):
    """The first weekday on or after d that is not a holiday: when the assessment group signs revisions off."""
    import datetime as dt
    while d.weekday() > 4 or (d.month, d.day) in WEEKDAY_HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def _working_day(d):
    """The first Tuesday, Wednesday or Thursday on or after d that is not a holiday: when the training team runs
    its sessions."""
    import datetime as dt
    while d.weekday() not in (1, 2, 3) or (d.month, d.day) in WEEKDAY_HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def _names(seed, n):
    from faker import Faker
    f = Faker("en_IE")
    f.seed_instance(seed)
    r = np.random.default_rng([seed, 31])
    out, seen = [], set()
    avoid = set(K.PEOPLE.values())
    while len(out) < n:
        if r.random() < 0.16:
            fore, sur = str(r.choice(IRISH_FORE)), str(r.choice(IRISH_SUR))
            if sur.startswith("Ní") or sur.startswith("Nic"):
                if fore in ("Seán", "Pádraig", "Éanna", "Ciarán", "Dónal", "Ruairí", "Tomás", "Eoghan"):
                    continue
        else:
            fore, sur = f.first_name(), f.last_name()
        full = "%s %s" % (fore, sur)
        if full in seen or full in avoid or fore.split()[0] in {"Meghan", "Cillian"}:
            continue
        seen.add(full)
        out.append((fore, sur))
    return out


def _email_local(fore, sur):
    import unicodedata
    a = lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    return "%s.%s" % (a(fore).replace(" ", ""), a(sur).replace(" ", "").replace("'", "").replace("-", ""))


def examiners(seed=SEED):
    """The register as exported on 30 November 2026 (its last refresher field holds the latest refresher booked,
    attended or not, future bookings included), the training team's attendance record for every session since
    2021, and the availability form's responses (the latest response from an examiner replaces earlier ones)."""
    import datetime as dt
    r = np.random.default_rng([seed, 32])
    day = lambda a, b: a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
    total = sum(b[1] for b in BASES)
    names = _names(seed, total + 40)
    people, k = [], 0
    staff = iter(sorted(r.choice(np.arange(10000, 99999), size=total + 8, replace=False).tolist()))
    for base, n, grades, gw in BASES:
        for _ in range(n):
            fore, sur = names[k]
            k += 1
            u = r.random()
            status = "Active" if u < 0.88 else ("On leave" if u < 0.93 else "Inactive")
            people.append({"staff": "E%05d" % next(staff), "fore": fore, "sur": sur, "base": base,
                           "grade": str(r.choice(grades, p=gw)), "status": status,
                           "title": "Prof" if "Professor" in "" else "Dr",
                           "email": _email_local(fore, sur) + "@callowfield.ie"})
    for p in people:
        if p["grade"] in ("Professor", "Associate Professor"):
            p["title"] = "Prof"
        elif p["grade"] in ("Consultant",) and r.random() < 0.3:
            r.random()   # the draw the register's stream was cut with; the forename decides the title
            g = _gender(p["fore"])
            p["title"] = {"M": "Mr", "F": "Ms"}.get(g, "Dr")
    extra = names[k:]
    # training sessions: initial and refresher sessions from 2021, four to six a year
    sessions = []
    sid = iter(range(301, 999))
    for y in range(2021, 2027):
        for m in sorted(r.choice(np.arange(1, 13), size=int(r.integers(4, 7)), replace=False).tolist()):
            dd = _working_day(dt.date(y, int(m), int(r.integers(3, 27))))
            if dd >= dt.date(2026, 11, 30):
                continue
            sessions.append({"id": "ET%03d" % next(sid), "date": dd, "type": str(r.choice(["Initial", "Refresher"],
                                                                                       p=[0.4, 0.6]))})
    future = [{"id": "ET%03d" % next(sid), "date": dt.date(2027, 1, 19), "type": "Refresher"},
              {"id": "ET%03d" % next(sid), "date": dt.date(2027, 2, 23), "type": "Refresher"}]
    sessions += future
    sessions.sort(key=lambda s: s["date"])
    # where each session ran: the training team's own sessions at the Clinical Skills Centre, booked through the
    # university's booking system, and sessions run for their own staff by the hospital's postgraduate centre and by
    # Fennabeg, whose sign-in sheets take the hospital's or Fennabeg's staff number for their own staff
    rv = np.random.default_rng([seed, 35])
    for x in sessions:
        x["venue"] = VENUES[0]
    window = [x for x in sessions if x["type"] == "Refresher" and K.TRAINED_FROM <= x["date"] < dt.date(2026, 11, 1)]
    pick = sorted(rv.choice(len(window), size=3, replace=False).tolist())
    window[pick[0]]["venue"], window[pick[1]]["venue"], window[pick[2]]["venue"] = VENUES[1], VENUES[1], VENUES[2]
    for x in sessions:
        if x["date"] < K.TRAINED_FROM:
            u = rv.random()
            x["venue"] = VENUES[1] if u < 0.2 else (VENUES[2] if u < 0.32 else VENUES[0])
    used = set()
    for p in people:
        # the hospital's and Fennabeg's own staff numbers: everyone based there, and the university's academics who
        # hold an honorary consultant post at the hospital
        home = HOME_VENUE.get(p["base"])
        if home is None and p["base"] == "Callowfield":
            rv.random()   # the draw the stream was cut with; the University's own staff hold no hospital number
        if home:
            while True:
                no = "%s%05d" % (home[1], int(rv.integers(10000, 99999)))
                if no not in used:
                    used.add(no)
                    p["alt"] = (no, home[0])
                    break
    inits = [s for s in sessions if s["type"] == "Initial" and s["date"] < dt.date(2026, 12, 1)]
    refs = [s for s in sessions if s["type"] == "Refresher" and s["date"] < dt.date(2026, 12, 1)]
    attendance = []
    for p in people:
        # initial training: before the log (2010 to 2020) or at a logged session
        if r.random() < 0.55:
            p["initial"] = _working_day(day(dt.date(2010, 1, 1), dt.date(2020, 11, 30)))
        else:
            s = inits[int(r.integers(0, len(inits)))]
            p["initial"] = s["date"]
            attendance.append({"session": s, "staff": p["staff"], "att": "Attended"})
        # refreshers every two to four years after the initial training, from the log's start
        t = p["initial"]
        p["refreshers"] = []
        while True:
            t2 = t + dt.timedelta(days=int(r.integers(700, 1500)))
            cands = [s for s in refs if s["date"] >= max(t2, dt.date(2021, 1, 1))]
            if not cands or cands[0]["date"] >= dt.date(2026, 11, 30) or r.random() < 0.18:
                break
            s = cands[0]
            att = "Attended" if r.random() < 0.93 else str(r.choice(["Did not attend", "Cancelled by examiner"]))
            attendance.append({"session": s, "staff": p["staff"], "att": att})
            p["refreshers"].append((s["date"], att, s["venue"]))
            if att == "Attended":
                t = s["date"]
    att_by = {}
    for a in attendance:
        att_by.setdefault(a["staff"], []).append(a)
    # the availability form: about seven in ten active examiners respond, choosing one site and their sessions
    sess = [x[0] for x in K.SESSIONS]
    resp = []
    for p in people:
        q = {"Active": 0.74, "On leave": 0.30, "Inactive": 0.12}[p["status"]]
        if r.random() >= q:
            continue
        sites = SITE_OF_BASE[p["base"]]
        if p["base"] == "General practice":
            site = str(r.choice(sites, p=[0.5, 0.36, 0.14]))
        else:
            site = sites[0] if (len(sites) == 1 or r.random() < 0.8) else str(r.choice(sites[1:]))
        ticks = {x: bool(r.random() < 0.64) for x in sess}
        if not any(ticks.values()):
            ticks[sess[int(r.integers(0, 4))]] = True
        resp.append({"staff": p["staff"], "site": site, "ticks": ticks})
    by_staff = {x["staff"]: x for x in resp}
    # the device: at each site, two active examiners of an eligible grade whose last attended training is before
    # the window, with a refresher booked inside it that they did not attend, and one with a refresher booked for
    # 2027; each offers every session at their site (two with the booking not attended offer all four)
    elig_grade = lambda p: p["status"] == "Active" and p["grade"] in ELIGIBLE_GRADES
    def last_att(p):
        ds = [p["initial"]] + [d for d, a, v in p["refreshers"] if a == "Attended"]
        return max(ds)
    dev_refs = [s for s in refs if s["date"] >= dt.date(2024, 2, 1) and s["venue"] == VENUES[0]]
    device = {}
    for site in [x[0] for x in K.SITES27]:
        pool = [p for p in people if elig_grade(p) and site in SITE_OF_BASE[p["base"]][:1]
                and last_att(p) < dt.date(2023, 6, 1) and p["staff"] not in device]
        pool.sort(key=lambda p: p["staff"])
        pick = [pool[j] for j in sorted(r.choice(len(pool), size=2, replace=False).tolist())]
        for j, p in enumerate(pick):
            s = dev_refs[int(r.integers(0, len(dev_refs)))]
            attendance.append({"session": s, "staff": p["staff"], "att": "Did not attend"})
            p["refreshers"].append((s["date"], "Did not attend", s["venue"]))
            ticks = {x: True for x in sess}
            device[p["staff"]] = site
            if p["staff"] in by_staff:
                resp.remove(by_staff[p["staff"]])
            row = {"staff": p["staff"], "site": site, "ticks": ticks}
            resp.append(row)
            by_staff[p["staff"]] = row
    # the second device: at each site, four active examiners of an eligible grade whose initial training is before
    # the window and whose refreshers inside it were the hospital's or Fennabeg's own sessions, signed in under that
    # employer's staff number (the register's booking system never sees them); they offer their site's sessions,
    # the fourth all but one
    rd = np.random.default_rng([seed, 38])
    home_dev = {}
    for site in [x[0] for x in K.SITES27]:
        # the Clinical Skills Centre's: hospital consultants who offer to examine there
        pool = [p for p in people if elig_grade(p) and "alt" in p and p["staff"] not in home_dev
                and (p["base"] == "CUH" if site == "CSC" else site in SITE_OF_BASE[p["base"]][:1])
                and p["staff"] not in device and p["initial"] < K.TRAINED_FROM
                and any(a == "Attended" and d >= K.TRAINED_FROM for d, a, v in p["refreshers"])]
        pool.sort(key=lambda p: p["staff"])
        pick = [pool[j] for j in sorted(rd.choice(len(pool), size=4, replace=False).tolist())]
        for j, p in enumerate(pick):
            own = sorted([x for x in refs if x["venue"] == p["alt"][1] and x["date"] >= K.TRAINED_FROM],
                         key=lambda x: x["date"])
            for a in attendance:
                if a["staff"] == p["staff"] and a["session"]["date"] >= K.TRAINED_FROM and a["att"] == "Attended":
                    a["session"] = min(own, key=lambda x: abs((x["date"] - a["session"]["date"]).days))
            p["refreshers"] = [(d, a, v) for d, a, v in p["refreshers"] if not (d >= K.TRAINED_FROM and a == "Attended")]
            for a in attendance:
                if a["staff"] == p["staff"] and a["session"]["date"] >= K.TRAINED_FROM and a["att"] == "Attended":
                    p["refreshers"].append((a["session"]["date"], "Attended", a["session"]["venue"]))
            ticks = {x: True for x in sess}
            if j == 3:
                ticks[sess[int(rd.integers(0, 4))]] = False
            home_dev[p["staff"]] = site
            if p["staff"] in by_staff:
                resp.remove(by_staff[p["staff"]])
            row = {"staff": p["staff"], "site": site, "ticks": ticks}
            resp.append(row)
            by_staff[p["staff"]] = row
    # the third device: at each site an active GP trainer whose last training was before the window and who offers
    # every session there shares their name with someone the hospital or Fennabeg has newly appointed, not yet on
    # the register, who attended their employer's own refresher inside the window (the trainee rows below)
    rh = np.random.default_rng([seed, 39])
    namesake = {}
    for site, kind in (("CSC", "Fennabeg"), ("CUH", "Fennabeg"), ("FCS", "CUH")):
        pool = [p for p in people if p["status"] == "Active" and p["grade"] == "GP Trainer"
                and p["base"] == "General practice" and p["staff"] not in device and p["staff"] not in home_dev
                and p["staff"] not in namesake and last_att(p) < dt.date(2023, 6, 1)
                and not any(d >= dt.date(2023, 6, 1) for d, a, v in p["refreshers"])]
        pool.sort(key=lambda p: p["staff"])
        p = pool[int(rh.integers(0, len(pool)))]
        namesake[p["staff"]] = (site, kind)
        if p["staff"] in by_staff:
            resp.remove(by_staff[p["staff"]])
        row = {"staff": p["staff"], "site": site, "ticks": {x: True for x in sess}}
        resp.append(row)
        by_staff[p["staff"]] = row
    # some already-eligible examiners booked their next refresher for 2027 (the register shows the booking)
    for p in people:
        if p["staff"] in device or not elig_grade(p):
            continue
        if last_att(p) >= dt.date(2024, 3, 1) and r.random() < 0.06:
            s = future[int(r.integers(0, 2))]
            attendance.append({"session": s, "staff": p["staff"], "att": "Booked"})
            p["refreshers"].append((s["date"], "Booked", s["venue"]))
    for p in people:
        # the register takes the latest refresher booked from the booking system once its date has passed,
        # attended or not; a cancelled booking is taken off, a booking for a future session is not yet shown
        bookings = [d for d, a, v in p["refreshers"] if a != "Cancelled by examiner" and d <= K.REGISTER_EXPORT
                    and v == VENUES[0]]
        p["last_refresher"] = max(bookings) if bookings else None
        p["last_attended"] = last_att(p)
    # people the training record holds who are not on the register: the hospital's and Fennabeg's own trainees
    # (registrars and newly appointed staff not yet added) and university staff who have since left
    rt = np.random.default_rng([seed, 37])
    trainees = []
    past = [x for x in sessions if x["date"] < dt.date(2026, 11, 30)]
    for j, (fore, sur) in enumerate(extra[4:28]):
        kind = ["CUH", "CUH", "Fennabeg", "left"][j % 4]
        if kind == "left":
            pool = [x for x in past if x["venue"] == VENUES[0] and x["date"] < dt.date(2024, 6, 1)]
            no = "E%05d" % int(rt.integers(10000, 99999))
        else:
            pool = [x for x in past if x["venue"] == HOME_VENUE[kind][0]]
            no = "%s%05d" % (HOME_VENUE[kind][1], int(rt.integers(10000, 99999)))
        while no in used or any(p["staff"] == no for p in people):
            no = no[0] + "%05d" % int(rt.integers(10000, 99999))
        used.add(no)
        for x in sorted(rt.choice(len(pool), size=min(len(pool), 1 + int(rt.random() < 0.4)), replace=False).tolist()):
            trainees.append({"session": pool[x], "no": no, "name": (fore, sur),
                             "att": "Attended" if rt.random() < 0.92 else "Did not attend"})
    rn = np.random.default_rng([seed, 40])
    who = {p["staff"]: p for p in people}
    for st in sorted(namesake):
        site, kind = namesake[st]
        p = who[st]
        pool = [x for x in past if x["venue"] == HOME_VENUE[kind][0] and x["date"] >= dt.date(2024, 1, 15)]
        no = "%s%05d" % (HOME_VENUE[kind][1], int(rn.integers(10000, 99999)))
        while no in used:
            no = no[0] + "%05d" % int(rn.integers(10000, 99999))
        used.add(no)
        trainees.append({"session": pool[int(rn.integers(0, len(pool)))], "no": no, "name": (p["fore"], p["sur"]),
                         "att": "Attended", "namesake": st})
    return {"people": people, "sessions": sessions, "attendance": attendance, "extra": extra, "future": future,
            "trainees": trainees, "home_device": home_dev, "namesake": namesake,
            "responses": resp, "device": device, "seed": seed}


def examiners_truth(e):
    """Per site and session, the examiners eligible at the 7 December 2026 allocation who offered it in their
    latest response: active, of an eligible grade, with the examiner training or a refresher attended on or after
    7 December 2023."""
    ok = {p["staff"] for p in e["people"] if p["status"] == "Active" and p["grade"] in ELIGIBLE_GRADES
          and p["last_attended"] >= K.TRAINED_FROM}
    out = {}
    for site in [x[0] for x in K.SITES27]:
        for sess in [x[0] for x in K.SESSIONS]:
            out[(site, sess)] = sum(1 for x in e["responses"] if x["staff"] in ok and x["site"] == site
                                    and x["ticks"][sess])
    return out
