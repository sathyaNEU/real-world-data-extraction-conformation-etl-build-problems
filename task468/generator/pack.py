"""The pack's data files, written from the clean truth: Halbrook's inpatient claims extract, Carrisford Medical Group's
inpatient encounter submissions, the member enrollment extract, the members' service activity, the Office of Vital
Records' linkage returns, the plan's mortality risk scores and the network hospital list."""
import csv
import datetime as dt

import numpy as np

import sim as S
import world as W

CLAIM_COLS = ["claim_number", "type_of_bill", "original_claim_number", "member_id", "billing_npi", "admission_date",
              "statement_from_date", "statement_thru_date", "admission_type", "patient_status", "drg", "principal_dx",
              "paid_date", "paid_amount"]
ENROLL_COLS = ["member_id", "last_name", "first_name", "birth_date", "sex", "ssn_last4", "aid_category",
               "cmg_member_no"]
ACT_COLS = ["member_id", "service_date", "service_category", "source"]
LINK_COLS = ["HCHP_MEMBER_ID", "ADMIT_DATE", "STATE_FILE_NUMBER", "DATE_OF_DEATH", "MATCH_PASS"]
SCORE_COLS = ["member_id", "admission_date", "facility_npi", "model_version", "p_death_30d"]
ROSTER_COLS = ["hospital_name", "npi", "npi_effective_from", "npi_effective_to", "county", "delegated_group_contract"]
COUNTY = {"Saint Brendan Medical Center": "Halbrook", "Westover Regional Hospital": "Westover",
          "Calloway Memorial Hospital": "Halbrook", "Varden Surgical Hospital": "Halbrook",
          "Mercy Valley Medical Center": "Tamsin", "Northgate Community Hospital": "Halbrook",
          "Tamsin General Hospital": "Tamsin", "Pinecrest Hospital": "Westover", "Brannock Medical Center": "Tamsin",
          "Lakeshore Hospital": "Ardmoor", "Corbel Falls Hospital": "Ardmoor", "Quayside Hospital": "Halbrook",
          "Marlow Ridge Medical Center": "Ardmoor", "Fairhaven Community Hospital": "Westover"}
CATEGORIES = (["PHARMACY", "OFFICE VISIT", "LABORATORY", "OUTPATIENT HOSPITAL", "EMERGENCY DEPARTMENT",
               "HOME HEALTH", "DURABLE MEDICAL EQUIPMENT", "NON-EMERGENCY TRANSPORTATION", "BEHAVIORAL HEALTH",
               "DENTAL", "VISION"], [40, 24, 12, 8, 4, 3, 2, 3, 2, 1, 1])
# the DRG a stay's first bill carried when a corrected bill later changed it, by the final DRG's family
FAMILY = [["871", "872", "870", "853"], ["291", "292", "314"], ["190", "189", "207"], ["193", "194", "195"],
          ["064", "065"], ["682", "683"], ["378", "392", "641"], ["308", "312", "313", "280", "247"],
          ["470", "481", "493", "460"], ["343", "419", "603", "690", "638", "885", "203"],
          ["807", "806", "805", "798", "797", "768"], ["788", "787", "786"], ["795", "794", "793", "792", "791", "790"]]


def rng(k):
    return np.random.default_rng([W.SEED, 31, k])


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def iso(d):
    return d.isoformat()


def money(v):
    return "%.2f" % v


def hosp_npi(hosp, disch):
    row = next(h for h in W.HOSPITALS if h[0] == hosp)
    return row[2] if (row[2] and disch >= W.NPI_CHANGE) else row[1]


def everything():
    """The truth with every stay, member and identifier the files need, built once."""
    x = S.simulate()
    S.extend(x)
    r = rng(1)
    mem = {m["member"]: m for m in x["members"]}
    for m in x["newmembers"]:
        mem[m["member"]] = m
    x["mem"] = mem
    for s in x["stays"]:
        m = mem[s["member"]]
        s["kind"], s["adult"], s["payer"] = "index", True, "cmg" if m["delegated"] else "plan"
    for e in x["extra"]:
        e["payer"] = "cmg" if mem[e["member"]]["delegated"] else "plan"
        e["adult"] = True
    for s in x["nonindex"]:
        s["payer"] = "cmg" if mem[s["member"]]["delegated"] else "plan"
    ids = sorted(mem)
    nums = r.choice(np.arange(900_000_000, 999_999_999), len(ids), replace=False)
    for k, v in zip(ids, nums):
        mem[k]["id"] = str(int(v))
    cmg = [k for k in ids if mem[k]["delegated"]]
    for k, v in zip(cmg, r.choice(np.arange(1_000_000, 9_999_999), len(cmg), replace=False)):
        mem[k]["cmg"] = "CM%07d" % int(v)
    for k in ids:
        m = mem[k]
        m["ssn4"] = "%04d" % int(r.integers(1, 10000)) if m["cls"] == "ssn" and "BABY" not in m["first"] else ""
        if " " in m["last"] and r.random() < 0.12:
            m["last_enrolled"] = m["last"].replace(" ", "-", 1)
        else:
            m["last_enrolled"] = m["last"]
    x["all_stays"] = ([dict(s, src="index") for s in x["stays"]] + [dict(e, src="extra") for e in x["extra"]] +
                      [dict(s, src="nonindex") for s in x["nonindex"]])
    for s in x["all_stays"]:
        s["npi"] = hosp_npi(s["hosp"], s["disch"])
    bills(x)
    return x


# ------------------------------------------------------------------------------------------ claims and encounters
def bills(x):
    """Each stay's bills. A Halbrook stay is billed once (type of bill 0111), sometimes corrected by a replacement bill
    (0117) that changes its DRG, and now and then submitted twice, the second copy later voided (0118). Each line is
    adjudicated on its paid date: before 1 January 2026 by the former claims system, which wrote a replacement as the
    change in payment and a void as the payment it reversed; from that day by the new platform, which writes a
    replacement as the stay's full payment and a void as a negative payment. A Carrisford stay is submitted as an
    encounter, sometimes replaced and now and then submitted twice and the copy deleted."""
    r = rng(2)
    plan, enc = [], []
    seq_legacy, seq_new, seq_enc = 0, 0, 0
    fam = {c: f for f in FAMILY for c in f}

    def weight(code):
        return W.DRG[code][0]

    def claim_no(paid):
        nonlocal seq_legacy, seq_new
        if paid < W.SYSTEM_CHANGE:
            seq_legacy += 1
            return "1%s%03d%07d" % (paid.strftime("%y"), paid.timetuple().tm_yday, 1_000_000 + seq_legacy * 7 % 8_999_999)
        seq_new += 1
        return "HC%010d" % (2_600_000_000 + seq_new * 13)

    for s in sorted(x["all_stays"], key=lambda s: (s["disch"], s["adm"], s["member"], s["src"])):
        base = W.BASE_RATE[s["hosp"]]
        final = s["drg"]
        paid0 = S.day(s["disch"], int(r.integers(8, 46)))
        u = r.random(6)
        corrected = u[0] < 0.065 and len(fam.get(final, [])) > 1
        first_drg = final
        if corrected:
            others = [c for c in fam[final] if c != final]
            up = [c for c in others if weight(c) < weight(final)]
            down = [c for c in others if weight(c) > weight(final)]
            pool = up if (u[1] < 0.7 and up) or not down else down
            first_drg = pool[int(u[2] * len(pool))]
        dup = u[3] < 0.015
        if s["payer"] == "cmg":
            if paid0 > W.CLAIMS_THROUGH:
                continue
            k = dict(stay=s, first_drg=first_drg, final=final)
            s["billed"] = True
            seq_enc += 1
            eid = "E%09d" % (400_000_000 + seq_enc * 17)
            pay_rate = 0.93 * base
            enc.append(dict(k, enc_id=eid, freq="1", orig="", submit=paid0, drg=first_drg,
                            paid=round(weight(first_drg) * pay_rate, 2)))
            if corrected:
                when = S.day(paid0, int(r.integers(20, 101)))
                if when <= W.CLAIMS_THROUGH:
                    seq_enc += 1
                    enc.append(dict(k, enc_id="E%09d" % (400_000_000 + seq_enc * 17), freq="7", orig=eid, submit=when,
                                    drg=final, paid=round(weight(final) * pay_rate, 2)))
            if dup:
                seq_enc += 1
                did = "E%09d" % (400_000_000 + seq_enc * 17)
                d1 = S.day(paid0, int(r.integers(2, 13)))
                d8 = min(S.day(d1, int(r.integers(15, 60))), W.CLAIMS_THROUGH)
                seq_enc += 1
                if d1 <= W.CLAIMS_THROUGH:      # a copy sent after September is not in the file
                    enc.append(dict(k, enc_id=did, freq="1", orig="", submit=d1, drg=first_drg,
                                    paid=round(weight(first_drg) * pay_rate, 2)))
                    enc.append(dict(k, enc_id="E%09d" % (400_000_000 + seq_enc * 17), freq="8", orig=did,
                                    submit=d8, drg=first_drg, paid=0.0))
            continue
        if paid0 > W.CLAIMS_THROUGH:
            continue
        s["billed"] = True
        p_first = round(weight(first_drg) * base, 2)
        p_final = round(weight(final) * base, 2)
        k = dict(stay=s)
        c0 = claim_no(paid0)
        plan.append(dict(k, claim=c0, tob="0111", orig="", paid_date=paid0, drg=first_drg, amount=p_first,
                         system="legacy" if paid0 < W.SYSTEM_CHANGE else "new"))
        s["truth_paid"] = p_first
        if corrected:
            when = S.day(paid0, int(r.integers(20, 101)))
            if when <= W.CLAIMS_THROUGH:
                legacy = when < W.SYSTEM_CHANGE
                plan.append(dict(k, claim=claim_no(when), tob="0117", orig=c0, paid_date=when, drg=final,
                                 amount=round(p_final - p_first, 2) if legacy else p_final,
                                 system="legacy" if legacy else "new"))
                s["truth_paid"] = p_final
        d1 = S.day(paid0, int(r.integers(2, 13)))
        if dup and d1 <= W.CLAIMS_THROUGH:
            c1 = claim_no(d1)
            plan.append(dict(k, claim=c1, tob="0111", orig="", paid_date=d1, drg=first_drg, amount=p_first,
                             system="legacy" if d1 < W.SYSTEM_CHANGE else "new"))
            when = min(S.day(d1, int(r.integers(15, 60))), W.CLAIMS_THROUGH)
            legacy = when < W.SYSTEM_CHANGE
            plan.append(dict(k, claim=claim_no(when), tob="0118", orig=c1, paid_date=when, drg=first_drg,
                             amount=p_first if legacy else -p_first, system="legacy" if legacy else "new"))
    x["plan_bills"], x["enc_bills"] = plan, enc


def claim_rows(x):
    mem = x["mem"]
    rows = []
    for b in sorted(x["plan_bills"], key=lambda b: (b["paid_date"], b["claim"])):
        s = b["stay"]
        rows.append([b["claim"], b["tob"], b["orig"], mem[s["member"]]["id"], s["npi"], iso(s["adm"]), iso(s["adm"]),
                     iso(s["disch"]), s.get("adm_type", "1"), s["status"], b["drg"], W.DRG[b["drg"]][1],
                     iso(b["paid_date"]), money(b["amount"])])
    return rows


def encounter_lines(x):
    """Carrisford's file: a header record, one D record per submission and a trailer with the count and the total
    paid; dates MM/DD/YY."""
    mem = x["mem"]
    out = []
    recs = sorted(x["enc_bills"], key=lambda b: (b["submit"], b["enc_id"]))
    total = 0.0
    for b in recs:
        s = b["stay"]
        total += b["paid"]
        out.append("|".join(["D", b["enc_id"], b["freq"], b["orig"], mem[s["member"]]["cmg"], s["npi"],
                             s["adm"].strftime("%m/%d/%y"), s["disch"].strftime("%m/%d/%y"), s["status"], b["drg"],
                             W.DRG[b["drg"]][1], b["submit"].strftime("%m/%d/%y"), "%.2f" % b["paid"]]))
    head = "H|CARRISFORD MEDICAL GROUP|HALBROOK COMMUNITY HEALTH PLAN|IP ENCOUNTERS|07/01/25|09/30/26|10/06/26"
    tail = "T|%d|%.2f" % (len(recs), total)
    return [head] + out + [tail]


def write_encounters(path, x):
    lines = encounter_lines(x)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        fh.write("\r\n".join(lines) + "\r\n")
    return len(lines) - 2


# ---------------------------------------------------------------------------------------------- members and the rest
def aid(m):
    if "BABY" in m["first"]:
        return "NEWBORN DEEMED"
    if m.get("dob") and (W.FY_START - m["dob"]).days < 18 * 365.25:
        return "CHILD"
    if m["cls"] != "ssn":
        return "STATE-FUNDED ADULT"
    return "ADULT EXPANSION"


def enrollment_rows(x):
    rows = []
    for k in sorted(x["mem"], key=lambda k: x["mem"][k]["id"]):
        m = x["mem"][k]
        dob = m["dob"]
        rows.append([m["id"], m["last_enrolled"], m["first"], dob.strftime("%m/%d/%Y"), m["sex"], m["ssn4"], aid(m),
                     m.get("cmg", "")])
    return rows


def activity_rows(x):
    r = rng(3)
    mem = x["mem"]
    dialysis = {s["member"] for s in x["stays"] if s["hosp"] == "Mercy Valley Medical Center" and s["cls"] == "compound"}
    lo, hi = dt.date(2025, 1, 1), W.CLAIMS_THROUGH
    seen = set()
    rows = []
    for k, d in sorted(x["activity"] + x["xactivity"], key=lambda t: (mem[t[0]]["id"], t[1])):
        if d < lo or d > hi:
            continue
        m = mem[k]
        cat = "DIALYSIS" if (k in dialysis and r.random() < 0.6) else S.pick(r, CATEGORIES)
        src = "RX" if cat == "PHARMACY" else ("CMG" if m["delegated"] else "HCP")
        key = (m["id"], d, cat)
        if key in seen:
            continue
        seen.add(key)
        rows.append([m["id"], iso(d), cat, src])
    return rows


def link_rows(x):
    """The Office's return: one row per record it linked, the record being the member and admission date the plan
    sent (every admission of a member aged 18 or older from 1 July 2025 to 30 June 2026 at a network hospital)."""
    r = rng(4)
    mem = x["mem"]
    sent = {(s["member"], s["adm"]) for s in x["all_stays"] if s.get("billed") and W.FY_START <= s["adm"] <= W.FY_END
            and mem[s["member"]]["dob"] is not None and (s["adm"] - mem[s["member"]]["dob"]).days >= 18 * 365.25}
    certs = {}
    rows = []
    base = [l for l in x["links"] if not l.get("fix")]
    for l in base + x["xlinks"] + [l for l in x["links"] if l.get("fix")]:
        if (l["member"], l["adm"]) not in sent:
            continue
        m = mem[l["member"]]
        key = (l["member"], l["death"]) if l["true"] else (l["member"], l["adm"], "f")
        if key not in certs:
            certs[key] = "%d-%06d" % (l["death"].year, int(r.integers(10_000, 999_999)))
        pas = "1" if (m["cls"] == "ssn" and l["true"] and r.random() < 0.95) else "2"
        rows.append([m["id"], l["adm"].strftime("%Y%m%d"), certs[key], l["death"].strftime("%Y%m%d"), pas])
    rows.sort(key=lambda t: (t[1], t[0]))
    return rows, len(sent)


def score_rows(x):
    mem = x["mem"]
    rows = []
    for s in x["all_stays"]:
        m = mem[s["member"]]
        if s.get("p") is None or not s.get("billed") or not (W.FY_START <= s["adm"] <= W.FY_END):
            continue
        if (s["adm"] - m["dob"]).days < 18 * 365.25:
            continue
        rows.append([m["id"], iso(s["adm"]), s["npi"], "HIMM 3.2", round(s["p"], 4)])
    rows.sort(key=lambda t: (t[1], t[0], t[2]))
    return rows


def roster_rows():
    rows = []
    for h in W.HOSPITALS:
        name, npi, npi2, delegated = h[0], h[1], h[2], h[10]
        if npi2:
            rows.append([name, npi, "2014-03-01", "2025-12-31", COUNTY[name], "Carrisford" if delegated else ""])
            rows.append([name, npi2, "2026-01-01", "", COUNTY[name], "Carrisford" if delegated else ""])
        else:
            rows.append([name, npi, "2011-07-01", "", COUNTY[name], "Carrisford" if delegated else ""])
    return rows


def readmission_rows(x):
    """The quality dashboard's preliminary readmission measure: each hospital's adult discharges alive (deliveries,
    transfers out and discharges against medical advice left out) to July 31, 2026, and those readmitted anywhere within
    30 days, against the dashboard model's expected rate."""
    later = {}
    for e in x["extra"]:
        if e["kind"] != "transfer_in":
            later.setdefault(e["member"], []).append(e["adm"])
    exp = {h: 0.038 + 0.0015 * ((i * 7) % 9) for i, h in enumerate(W.CANDIDATES)}
    rows = []
    for h in W.CANDIDATES:
        el = [s for s in x["stays"] if s["hosp"] == h and s["status"] == "01" and s["disch"] <= dt.date(2026, 6, 30)]
        re = sum(1 for s in el if any(0 < (a - s["disch"]).days <= 30 for a in later.get(s["member"], [])))
        obs = re / len(el)
        rows.append([h, len(el), re, round(obs, 4), round(exp[h], 4), round(obs / exp[h], 2)])
    med = sorted(r[5] for r in rows)
    m = (med[6] + med[7]) / 2.0
    return [r + [round(m, 2)] for r in rows]


PROFILES = {
    "Saint Brendan Medical Center": ("412", "48", "Medical and surgical, cardiac catheterization, obstetrics, NICU level "
                                     "III, psychiatric unit, level II trauma", "Nonprofit, Saint Brendan Health"),
    "Westover Regional Hospital": ("356", "36", "Medical and surgical, obstetrics, NICU level II, stroke center",
                                   "Nonprofit, independent"),
    "Calloway Memorial Hospital": ("288", "26", "Medical and surgical, obstetrics, NICU level II, inpatient dialysis",
                                   "County hospital district"),
    "Varden Surgical Hospital": ("96", "10", "Orthopedic, spine and general surgery; no emergency obstetrics",
                                  "Physician-owned"),
    "Mercy Valley Medical Center": ("324", "40", "Medical and surgical, regional dialysis and nephrology program, "
                                    "heart failure clinic, obstetrics", "Nonprofit, Mercy Valley Health"),
    "Northgate Community Hospital": ("204", "18", "Medical and surgical, obstetrics, NICU level II",
                                     "Nonprofit, independent"),
    "Tamsin General Hospital": ("186", "16", "Medical and surgical, obstetrics, NICU level II", "Nonprofit, Saint Brendan Health"),
    "Pinecrest Hospital": ("172", "14", "Medical and surgical, obstetrics, geriatric psychiatry", "For-profit, Pinecrest "
                           "Healthcare"),
    "Brannock Medical Center": ("238", "22", "Medical and surgical, obstetrics, NICU level II, outpatient dialysis "
                                 "partner", "Nonprofit, independent"),
    "Lakeshore Hospital": ("148", "12", "Medical and surgical, obstetrics", "Nonprofit, independent"),
    "Corbel Falls Hospital": ("120", "10", "Medical and surgical, obstetrics, swing beds", "County hospital district"),
    "Quayside Hospital": ("276", "24", "Medical and surgical, women's and infants' center, NICU level III",
                             "Nonprofit, Quayside Health"),
    "Marlow Ridge Medical Center": ("110", "10", "Medical and surgical, obstetrics, rehabilitation unit",
                                    "For-profit, Marlow Health Partners"),
    "Fairhaven Community Hospital": ("98", "8", "Medical and surgical, obstetrics", "Nonprofit, independent"),
}


def profile_rows():
    return [[h, COUNTY[h], PROFILES[h][0], PROFILES[h][1], PROFILES[h][2], PROFILES[h][3]] for h in W.CANDIDATES]


# ------------------------------------------------------------------------------------------------ the linkage, C1
def converge_links(x, target):
    """Every hospital's index admissions in an identifier class that the bills neither record as a death nor show
    alive after day 30 carry at least the links that class's false-link share expects among them, so no class's
    corrected count at a hospital falls below zero and the estimate never needs a floor. Where a class falls short,
    the Office's return finds one more of its members: a death at home that no bill records where the class has one,
    else a living member linked to another person's death. Returns the links added."""
    import bundle as B
    import methods as M
    f = B.Pack(target).frame()
    R = M.rates(f, "cls")
    key = {m["id"]: k for k, m in x["mem"].items()}
    idx = {(s["member"], s["adm"]): s for s in x["stays"]}
    r = rng(5)
    added = []
    U = f[~f["known_death"] & ~f["alive_after"]]
    for (h, c), g in sorted(U.groupby(["hosp", "cls"]), key=lambda t: t[0]):
        if g["linked"].sum() >= R[c][1] * len(g):
            continue
        cand = sorted((m, a) for m, a, l in zip(g["member"], g["adm"], g["linked"]) if not l)
        stays = [s for s in (idx.get((key[m], a)) for m, a in cand) if s is not None]
        home = [s for s in stays if s["dies"] and s["place"] == "home" and not s["transfer"]]
        s = home[0] if home else next(s for s in stays if not s["dies"])
        death = s["death"] if home else S.day(s["adm"], 1 + int(r.random() * W.WINDOW))
        lk = dict(member=s["member"], adm=s["adm"], death=death, true=bool(home), fix=True)
        x["links"].append(lk)
        added.append(lk)
    return added


# ------------------------------------------------------------------------------------------- the dispute log
DISPUTE_COLS = ["PDR No.", "Received", "Provider", "Provider NPI", "Claim No.", "Member ID", "Admit Date",
                "Discharge Date", "Dispute Type", "Amount Disputed", "Determination", "Determination Date",
                "Additional Payment", "Payment Date"]


def dispute_rows(x):
    """Provider Disputes' log of the network hospitals' disputes of inpatient payments, received January 1, 2025 to
    September 30, 2026 and run October 1, 2026: each with its determination and, where the determination found for the
    hospital, the additional payment and the day it was made. An overturned DRG dispute is paid by reprocessing the
    bill at the hospital's DRG, so its additional payment is the replacement bill already in the claims extract (paid
    that day, its change in payment the award); a settled DRG dispute and every outlier and rate award are paid by
    Finance outside the claims system and appear nowhere else."""
    r = rng(6)
    mem = x["mem"]
    run = W.DISPUTE_RUN
    fam = {c: f for f in FAMILY for c in f}
    by_claim = {b["claim"]: b for b in x["plan_bills"]}
    reps = {b["orig"]: b for b in x["plan_bills"] if b["tob"] == "0117"}
    dups = {id(b["stay"]) for b in x["plan_bills"] if b["tob"] == "0118"}
    firsts = [b for b in x["plan_bills"] if b["tob"] == "0111" and b["orig"] == ""]
    seen, origs = set(), []
    for b in sorted(firsts, key=lambda b: (b["paid_date"], b["claim"])):
        if id(b["stay"]) in seen:
            continue                            # a stay's first bill, not the copy sent twice
        seen.add(id(b["stay"]))
        origs.append(b)
    out, taken = [], set()

    def add(b, kind, disputed, det, det_date, award, pay_date, received, grp="finance"):
        if received > W.CLAIMS_THROUGH:        # the log holds the disputes received through September
            return False
        s = b["stay"]
        taken.add(b["claim"])
        out.append(dict(received=received, hosp=s["hosp"], npi=s["npi"], claim=b["claim"], member=mem[s["member"]]["id"],
                        adm=s["adm"], disch=s["disch"], kind=kind, disputed=disputed, det=det, det_date=det_date,
                        award=award, pay=pay_date, grp=grp))
        return True

    def w(code):
        return W.DRG[code][0]

    for h in W.CANDIDATES:
        mine = [b for b in origs if b["stay"]["hosp"] == h]
        base = W.BASE_RATE[h]
        up = [b for b in mine if b["claim"] in reps and w(reps[b["claim"]]["drg"]) > w(b["drg"])]
        plain = [b for b in mine if b["claim"] not in reps and id(b["stay"]) not in dups]
        # overturned DRG disputes, paid by reprocessing the bill
        for b in up:
            u = r.random(4)
            if u[0] >= W.DISPUTE_SHARE["reprocessed"]:
                continue
            rp = reps[b["claim"]]
            gap = (rp["paid_date"] - b["paid_date"]).days
            rec = S.day(b["paid_date"], 6 + int(u[1] * max(1, gap - 18)))
            det = max(S.day(rec, 3), S.day(rp["paid_date"], -(1 + int(u[2] * 6))))
            change = round(rp["amount"] if rp["system"] == "legacy" else rp["amount"] - b["amount"], 2)
            add(b, "DRG assignment", change, "Overturned", det, change, rp["paid_date"], rec, "reprocessed")
        # the disputes Finance pays: a settled DRG dispute, outliers and rates
        fin = 0.0
        for b in plain:
            u = r.random(8)
            if u[0] >= W.DISPUTE_SHARE["finance"]:
                continue
            hi = [c for c in fam.get(b["drg"], []) if w(c) > w(b["drg"])]
            if u[1] < 0.40 and hi:
                kind = "DRG assignment"
                disputed = round(round(w(hi[int(u[2] * len(hi))]) * base, 2) - b["amount"], 2)
                det, award = "Partially overturned", round(disputed * (0.45 + 0.35 * u[3]), 2)
            elif u[1] < 0.75:
                kind = "Outlier payment"
                disputed = round(b["amount"] * (0.08 + 0.22 * u[2]), 2)
                full = u[3] < 0.6
                det, award = ("Overturned", disputed) if full else ("Partially overturned",
                                                                    round(disputed * (0.35 + 0.45 * u[4]), 2))
            else:
                kind = "Contract rate"
                disputed = round(b["amount"] * (0.02 + 0.05 * u[2]), 2)
                full = u[3] < 0.7
                det, award = ("Overturned", disputed) if full else ("Partially overturned",
                                                                    round(disputed * (0.4 + 0.4 * u[4]), 2))
            rec = S.day(b["paid_date"], 20 + int(u[5] * 130))
            ddate = S.day(rec, 25 + int(u[6] * 55))
            pay = S.day(ddate, 5 + int(u[7] * 16))
            if ddate > run:
                det, ddate, award, pay = "Pending", None, None, None
            elif pay > W.CLAIMS_THROUGH:
                pay = None
            if add(b, kind, disputed, det, ddate, award, pay, rec) and pay is not None and \
                    W.FY_START <= b["stay"]["disch"] <= W.FY_END:
                fin += award
        # a hospital whose outlier disputes ran heavier than the rest's
        more = [b for b in plain if b["claim"] not in taken and W.FY_START <= b["stay"]["disch"] <= W.FY_END
                and b["paid_date"] <= dt.date(2026, 5, 15)]
        for j in r.permutation(len(more)):
            if fin >= W.DISPUTE_FLOOR:
                break
            b, u = more[j], r.random(4)
            disputed = round(b["amount"] * (0.12 + 0.2 * u[0]), 2)
            rec = S.day(b["paid_date"], 20 + int(u[1] * 40))
            ddate = S.day(rec, 25 + int(u[2] * 30))
            add(b, "Outlier payment", disputed, "Overturned", ddate, disputed, S.day(ddate, 5 + int(u[3] * 12)), rec)
            fin += disputed
        # disputes decided for Halbrook or withdrawn
        for b in mine:
            u = r.random(5)
            if u[0] >= W.DISPUTE_SHARE["denied"] or b["claim"] in taken:
                continue
            kind = ("DRG assignment", "Outlier payment", "Contract rate")[int(u[1] * 3)]
            disputed = round(b["amount"] * (0.04 + 0.2 * u[2]), 2)
            rec = S.day(b["paid_date"], 15 + int(u[3] * 140))
            ddate = S.day(rec, 20 + int(u[4] * 60))
            if ddate > run:
                add(b, kind, disputed, "Pending", None, None, None, rec, "none")
            elif u[4] < 0.3:
                add(b, kind, disputed, "Withdrawn", ddate, None, None, rec, "none")
            else:
                add(b, kind, disputed, "Upheld", ddate, 0.0, None, rec, "none")
    # disputes on stays discharged before July 2025, whose bills predate the claims extract
    seq = 0
    for h in W.CANDIDATES:
        hrow = next(t for t in W.HOSPITALS if t[0] == h)
        adults = sorted(k for k, m in mem.items() if m["hosp"] == h and m.get("dob") and
                        (W.FY_START - m["dob"]).days >= 20 * 365.25 and not m.get("delegated"))
        for _k in range(W.DISPUTE_OLD[h]):
            u = r.random(9)
            m = adults[int(u[0] * len(adults))]
            adm = S.day(dt.date(2025, 1, 2), int(u[1] * 165))
            disch = S.day(adm, 1 + int(u[2] * 7))
            paid = S.day(disch, 10 + int(u[3] * 30))
            seq += 1
            claim = "1%s%03d%07d" % (paid.strftime("%y"), paid.timetuple().tm_yday, 3_000_000 + seq * 131)
            amount = round(W.BASE_RATE[h] * (0.7 + 2.3 * u[4]), 2)
            kind = ("DRG assignment", "Outlier payment", "Contract rate")[int(u[5] * 3)]
            disputed = round(amount * (0.06 + 0.25 * u[6]), 2)
            rec = S.day(paid, 20 + int(u[7] * 100))
            ddate = S.day(rec, 30 + int(u[8] * 60))
            pay = S.day(ddate, 6 + int(u[8] * 14))
            stay = dict(hosp=h, npi=hrow[1], member=m, adm=adm, disch=disch)
            add(dict(stay=stay, claim=claim), kind, disputed, "Overturned", ddate, disputed, pay, rec, "old")
    out.sort(key=lambda d: (d["received"], d["claim"]))
    x["disputes_truth"] = out
    rows = []
    for i, d in enumerate(out, 1):
        rows.append(["PDR-%s-%05d" % (d["received"].strftime("%y"), 410 + i * 3), d["received"], d["hosp"], d["npi"],
                     d["claim"], d["member"], d["adm"], d["disch"], d["kind"], d["disputed"], d["det"], d["det_date"],
                     d["award"], d["pay"]])
    return rows
