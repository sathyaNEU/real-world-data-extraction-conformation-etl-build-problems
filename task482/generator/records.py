"""The records the organisation's systems hold about the world: identifiers, diagnoses, the Medicare benefit periods,
the two EMR exports, the levels of care and claims for FY2026, and the remittances. Every draw here comes from its own
stream (world.SEED and a stream number), so the world's own draws are untouched."""
import datetime as dt

import numpy as np

import world as W

CONVERSION = (dt.date(2025, 3, 1) - W.DAY0).days       # Fallowmere's change of ownership, 3073
MBI_FROM = (dt.date(2018, 4, 1) - W.DAY0).days         # admissions from here carry the MBI
LAST_DAY = W.CLOSE - 1                                 # 2026-12-31, the data date of every extract

CCN = {"BRK": "361791", "COR": "361792", "DUN": "361793", "LIN": "361794", "PEN": "361795", "SAL": "361796",
       "WEX": "361797", "FAL": "361798"}
PROGRAM = {"BRK": "Brindlemoor", "COR": "Corvelfield", "DUN": "Darrelbrook", "LIN": "Marrellford", "PEN": "Rennickdale",
           "SAL": "Varrowmere", "WEX": "Farrinridge", "FAL": "Fallowmere Hospice"}
OUTSIDE = ["X%05d" % k for k in (104, 117, 125, 139, 142, 158, 163, 171, 186, 190, 207, 214, 229, 236)]

DX = {"C": [("C34.90", 18), ("C34.11", 6), ("C50.919", 9), ("C61", 8), ("C18.9", 8), ("C25.9", 9), ("C22.0", 5),
            ("C71.9", 4), ("C16.9", 3), ("C56.9", 4), ("C67.9", 3), ("C91.10", 2), ("C92.00", 3), ("C80.1", 3),
            ("C64.9", 3), ("C15.9", 2)],
      "D": [("G30.9", 44), ("G30.1", 20), ("G31.1", 8), ("G31.83", 10), ("G31.09", 4), ("G30.8", 6), ("G31.84", 3)],
      "P": [("I50.9", 22), ("I50.22", 10), ("I50.32", 8), ("I50.42", 5), ("I11.0", 7), ("I13.0", 4), ("J44.9", 20),
            ("J44.1", 10), ("J84.10", 5), ("J96.11", 6), ("I42.9", 3)],
      "O": [("I63.9", 16), ("N18.6", 12), ("K74.60", 10), ("G12.21", 6), ("G20.A1", 9), ("G35", 3), ("I61.9", 6),
            ("E43", 4), ("N18.5", 5), ("K72.10", 3), ("I69.354", 4), ("G93.1", 4), ("J69.0", 3)]}

MBI_LET = "ACDEFGHJKMNPQRTUVWXY"
MBI_ALNUM = "0123456789" + MBI_LET


def stream(n):
    return np.random.default_rng([W.SEED, n])


def mbi(rng):
    p = [str(rng.integers(1, 10)), MBI_LET[rng.integers(len(MBI_LET))], MBI_ALNUM[rng.integers(len(MBI_ALNUM))],
         str(rng.integers(0, 10)), MBI_LET[rng.integers(len(MBI_LET))], MBI_ALNUM[rng.integers(len(MBI_ALNUM))],
         str(rng.integers(0, 10)), MBI_LET[rng.integers(len(MBI_LET))], MBI_LET[rng.integers(len(MBI_LET))],
         str(rng.integers(0, 10)), str(rng.integers(0, 10))]
    return "".join(p)


def served(bens):
    """Beneficiaries with a day of care at one of the eight provider numbers on or after 2016-10-01."""
    return [b for b in bens if any(e[2] in W.CODES and e[1] > 0 and e[0] < W.CLOSE for e in b[2])]


class Ben:
    __slots__ = ("idx", "home", "g", "eps", "dod", "mbi", "hicn", "mrn", "facct", "dob", "sex", "dx", "out_ccn",
                 "stays", "periods", "residence")


def identities(sv):
    rng = stream(1)
    seen = set()
    hicns = set()
    out = []
    for i, (home, g, eps, dod) in enumerate(sv):
        b = Ben()
        b.idx, b.home, b.g, b.eps, b.dod = i, home, g, eps, dod
        while True:
            m = mbi(rng)
            if m not in seen:
                seen.add(m)
                break
        b.mbi = m
        while True:
            h = "9%08dA" % rng.integers(0, 10 ** 8)
            if h not in hicns:
                hicns.add(h)
                break
        b.hicn = h
        b.mrn = "WG%07d" % (1000000 + i * 3 + int(rng.integers(0, 3)))
        b.facct = "%06d" % (400000 + i)
        first = eps[0][0]
        age = float(np.clip(rng.normal(74.0 if g == "C" else 84.0, 8.0), 58, 104))
        b.dob = W.date_of(first) - dt.timedelta(days=int(age * 365.25))
        b.sex = "F" if rng.random() < 0.58 else "M"
        codes, wts = zip(*DX[g])
        w = np.array(wts, float)
        b.dx = codes[rng.choice(len(codes), p=w / w.sum())]
        b.residence = "Q5003" if rng.random() < (0.42 if g == "D" else 0.22) else ("Q5002" if rng.random() < 0.12 else "Q5001")
        b.out_ccn = [OUTSIDE[rng.integers(len(OUTSIDE))] if e[2] == "OUT" else None for e in eps]
        out.append(b)
    return out


def stays_of(b):
    """Episodes chained across transfers into stays: (start, end, why, [episode indexes])."""
    stays, cur = [], None
    for i, e in enumerate(b.eps):
        if cur is not None and b.eps[i - 1][3] == "transfer" and e[0] == b.eps[i - 1][1]:
            cur[1], cur[2] = e[1], e[3]
            cur[3].append(i)
        else:
            cur = [e[0], e[1], e[3], [i]]
            stays.append(cur)
    return [tuple(s) for s in stays]


def provider_of(b, i):
    e = b.eps[i]
    return CCN[e[2]] if e[2] in W.CODES else b.out_ccn[i]


def benefit_periods(b):
    """Rows of the Medicare benefit periods extract: (period number, provider number, start, end or None, days,
    end kind), each stay split at its benefit period boundaries and at each change of hospice, cut at the data date."""
    rows, n = [], 0
    for s0, s1, why, idxs in b.stays:
        if s0 >= W.CLOSE:
            break
        n += 1
        bp_start, bp_len = s0, (90 if n <= 2 else 60)
        bounds = []
        t = s0
        while t < s1:
            bp_end = bp_start + bp_len
            cut = min(bp_end, s1)
            bounds.append((n, bp_start, cut, cut == s1))
            t = cut
            if cut == bp_end and cut < s1:
                n += 1
                bp_start, bp_len = cut, (90 if n <= 2 else 60)
        elect = s0
        for num, a, z, final in bounds:
            for i in idxs:
                e0, e1 = b.eps[i][0], b.eps[i][1]
                lo, hi = max(a, e0), min(z, e1)
                if lo >= hi or lo >= W.CLOSE:
                    continue
                prov = provider_of(b, i)
                if hi > W.CLOSE:
                    rows.append((num, prov, lo, None, W.CLOSE - lo, "open", elect))
                    continue
                if hi == e1 and (i != idxs[-1] or final):
                    kind = b.eps[i][3]                    # the episode ended here
                else:
                    kind = "period"                       # a benefit period boundary inside the episode
                rows.append((num, prov, lo, hi, hi - lo, kind, elect))
    return rows


def build(bens):
    sv = served(bens)
    people = identities(sv)
    for b in people:
        b.stays = stays_of(b)
        b.periods = benefit_periods(b)
    return people


# ---------------------------------------------------------------------------------------------------------------
# The EMR exports

EMR_REASON = {"death": "Expired", "revoked": "Revoked", "nlti": "No longer terminally ill",
              "moved": "Moved out of service area", "transfer": "Transferred to another hospice"}


def end_date(e):
    """The EMR's discharge date: the day of death, or the day a live discharge or transfer took effect."""
    return W.date_of(e[1] - 1) if e[3] == "death" else W.date_of(e[1])


def medicare_id(b, day):
    return b.hicn if day < MBI_FROM else b.mbi


def emr_rows(people):
    """Wendleglen's EMR: every episode at its seven programs with a day on or after 2016-10-01, and Fallowmere's from the
    change of ownership (its patients on service then carried over with their own admission dates)."""
    rows = []
    for b in people:
        for i, e in enumerate(b.eps):
            if e[2] not in W.CODES or e[0] >= W.CLOSE or e[1] <= 0:
                continue
            if e[2] == "FAL" and e[1] <= CONVERSION:
                continue
            if e[2] == "FAL" and e[0] < CONVERSION:
                atype = "Conversion"
            elif i > 0 and b.eps[i - 1][3] == "transfer" and b.eps[i - 1][1] == e[0]:
                atype = "Transfer in"
            else:
                atype = "New election"
            open_ = e[1] > W.CLOSE or (e[3] == "death" and e[1] - 1 > LAST_DAY)
            id_day = max(e[0], CONVERSION) if atype == "Conversion" else e[0]
            rows.append(dict(mrn=b.mrn, medicare_id=medicare_id(b, id_day), provider_number=CCN[e[2]],
                             program=PROGRAM[e[2]], admission_type=atype, admit_date=W.date_of(e[0]),
                             discharge_date=None if open_ else end_date(e),
                             discharge_reason="" if open_ else EMR_REASON[e[3]], primary_dx=b.dx,
                             birth_date=b.dob, sex=b.sex, payer="Medicare", _b=b.idx, _i=i))
    return rows


UB04 = {"revoked": "01", "nlti": "01", "moved": "01", "transfer": "50"}


def legacy_rows(people):
    """Fallowmere's seller's system, exported at the change of ownership: its admissions with a day on or after
    2016-10-01 and before 1 March 2025; a patient still on service has status 30 and no discharge date."""
    rng = stream(2)
    rows = []
    for b in people:
        for i, e in enumerate(b.eps):
            if e[2] != "FAL" or e[0] >= CONVERSION or e[1] <= 0:
                continue
            if e[1] > CONVERSION or (e[3] == "death" and e[1] - 1 >= CONVERSION):
                status, ddate = "30", None
            elif e[3] == "death":
                status, ddate = ("40", "41", "42")[int(rng.choice(3, p=[0.62, 0.33, 0.05]))], end_date(e)
            else:
                status, ddate = UB04[e[3]], end_date(e)
                if e[3] == "transfer" and rng.random() < 0.3:
                    status = "51"
            rows.append(dict(acct=b.facct, medicare_no=medicare_id(b, e[0]), dob=b.dob, sex=b.sex,
                             admit=W.date_of(e[0]), disch=ddate, status=status, dx=b.dx.replace(".", ""),
                             payer="MCR", _b=b.idx, _i=i))
    return rows


def other_payer_rows(people):
    """Patients of other payers in the EMR (Medicaid only, commercial, VA, self pay): the cap does not reach them."""
    rng = stream(4)
    rows = []
    n = int(len(people) * 0.055)
    codes = [c for c in W.CODES]
    for k in range(n):
        c = codes[int(rng.integers(len(codes)))]
        lo = CONVERSION if c == "FAL" else 0
        s = int(rng.integers(lo, W.CLOSE - 5))
        L = max(1, int(rng.lognormal(np.log(30), 1.2)))
        open_ = s + L > W.CLOSE
        g = W.GRP[int(rng.integers(4))]
        codes_g, wts = zip(*DX[g])
        dob = W.date_of(s) - dt.timedelta(days=int(rng.uniform(52, 96) * 365.25))
        rows.append(dict(mrn="WG%07d" % (5000000 + k), medicare_id="", provider_number=CCN[c], program=PROGRAM[c],
                         admission_type="New election", admit_date=W.date_of(s),
                         discharge_date=None if open_ else W.date_of(s + L - 1),
                         discharge_reason="" if open_ else "Expired", primary_dx=codes_g[int(rng.integers(len(codes_g)))],
                         birth_date=dob, sex="F" if rng.random() < 0.55 else "M",
                         payer=["Medicaid", "Commercial", "VA", "Self pay"][int(rng.choice(4, p=[0.45, 0.35, 0.15, 0.05]))],
                         _b=None, _i=None))
    return rows


# ---------------------------------------------------------------------------------------------------------------
# Levels of care, claims and remittances for FY2026

RATES = {"RHC_HI": 230.83, "RHC_LO": 181.94, "CHC_HR": 69.76, "IRC": 532.48, "GIP": 1199.86}
RETURN_AGE = 125        # a returned replacement was submitted at least this many days before the close
REVIEW_SHARE = 0.0016   # inpatient days paid at the routine rate after review, as a share of a provider number's days
SEPARATION = 0.0010     # the least gap, as a share of days, between the routine-paid days and the returned replacements' days
LABOR = {"R": 0.660, "C": 0.752, "I": 0.610, "G": 0.635}
F_GIP = {"BRK": 4.0, "COR": 2.6, "DUN": 2.0, "LIN": 1.2, "PEN": 2.4, "SAL": 1.8, "WEX": 1.9, "FAL": 2.4}
F_CHC = {"BRK": 0.6, "COR": 0.8, "DUN": 0.8, "LIN": 0.6, "PEN": 0.8, "SAL": 0.7, "WEX": 0.6, "FAL": 30.0}
CHARGE = {"0651": 312.00, "0652": 24.50, "0655": 640.00, "0656": 1480.00}
MONTHS = [(dt.date(2025 + (m >= 3), (m + 9) % 12 + 1, 1)) for m in range(12)]   # October 2025 .. September 2026


def month_bounds(first):
    nxt = dt.date(first.year + (first.month == 12), first.month % 12 + 1, 1)
    return (first - W.DAY0).days, (nxt - W.DAY0).days


def levels(b, i):
    """One level per billed day of episode i: R routine home care, C continuous home care (with hours), I inpatient
    respite, G general inpatient. Drawn from the episode's own stream."""
    e = b.eps[i]
    code = e[2]
    L = e[1] - e[0]
    rng = np.random.default_rng([W.SEED, 3, b.idx, i])
    lv = ["R"] * L
    hours = {}
    home = b.residence != "Q5003"
    if e[3] == "death":
        if rng.random() < min(0.9, 0.18 * F_GIP[code]):
            k = min(L, 1 + int(rng.geometric(0.3)))
            for d in range(L - k, L):
                lv[d] = "G"
        elif home and rng.random() < min(0.9, 0.05 * F_CHC[code]):
            k = min(L, 1 + int(rng.geometric(0.5)))
            for d in range(L - k, L):
                lv[d] = "C"
    for blk in range(0, max(0, L - 10), 30):
        if rng.random() < 0.02 * F_GIP[code]:
            k = int(rng.integers(2, 7))
            d0 = blk + int(rng.integers(0, 24))
            if d0 + k < L - 3 and all(x == "R" for x in lv[d0:d0 + k + 1]):
                for d in range(d0, d0 + k):
                    lv[d] = "G"
        if home and rng.random() < 0.012 * F_CHC[code]:
            k = int(rng.integers(1, 4))
            d0 = blk + int(rng.integers(0, 26))
            if d0 + k < L - 2 and all(x == "R" for x in lv[d0:d0 + k + 1]):
                for d in range(d0, d0 + k):
                    lv[d] = "C"
    if home:
        for blk in range(10, max(10, L - 10), 45):
            if rng.random() < 0.05:
                d0 = blk + int(rng.integers(0, 30))
                if d0 + 6 < L - 3 and all(x == "R" for x in lv[d0:d0 + 6]):
                    for d in range(d0, d0 + 5):
                        lv[d] = "I"
    for d, x in enumerate(lv):
        if x == "C":
            hours[d] = float(rng.integers(32, 97)) / 4.0
    return lv, hours


def rhc_index(b):
    """Day -> position in the beneficiary's routine home care count (days 1 to 60 at the higher rate), the count
    running on across any gap of 60 days or fewer between stays, at any hospice."""
    idx, cnt, prev = {}, 0, None
    for s0, s1, why, idxs in b.stays:
        if prev is not None and s0 - prev > 60:
            cnt = 0
        for day in range(s0, s1):
            cnt += 1
            idx[day] = cnt
        prev = s1
    return idx


def claim_days(b, i, first):
    """The billed days of episode i inside the calendar month beginning `first`."""
    e = b.eps[i]
    m0, m1 = month_bounds(first)
    return max(e[0], m0), min(e[1], m1)


def price(days):
    """A claim's payment at the levels of its days, split into a wage-index-free part and a labor part (payment =
    fixed + labor * wage index): routine home care at the higher rate for days 1 to 60 of the count, continuous home
    care by the hour, respite and general inpatient by the day."""
    fixed = labor = 0.0
    for day, x, hi, q in days:
        if x == "C":
            pay = RATES["CHC_HR"] * q / 4.0
        elif x == "R":
            pay = RATES["RHC_HI"] if hi else RATES["RHC_LO"]
        else:
            pay = RATES["IRC" if x == "I" else "GIP"]
        fixed += pay * (1 - LABOR[x])
        labor += pay * LABOR[x]
    return fixed, labor


def refresh(c):
    """Units, continuous care lines and the price from the claim's billed days, and the paid days' price."""
    c["units"] = {k: sum(1 for d in c["days"] if d[1] == k) for k in ("R", "I", "G")}
    c["chc"] = [(W.date_of(d[0]), d[3]) for d in c["days"] if d[1] == "C"]
    c["fixed"], c["labor"] = price(c.get("paid_days") or c["days"])


def paid_units(c, lv):
    return sum(1 for d in (c.get("paid_days") or c["days"]) if d[1] == lv)


def build_claims(people):
    """The original claim for each episode-month of FY2026 at the eight provider numbers, with its days (level, the
    routine care tier, continuous care quarter hours) and its payment split into a wage-index-free part and a labor
    part (payment = fixed + labor * wage index)."""
    claims = []
    for b in people:
        ri = None
        for i, e in enumerate(b.eps):
            if e[2] not in W.CODES or e[0] >= W.FY[1] or e[1] <= W.FY[0]:
                continue
            if ri is None:
                ri = rhc_index(b)
            lv, hours = levels(b, i)
            for first in MONTHS:
                a, z = claim_days(b, i, first)
                if a >= z:
                    continue
                m0, m1 = month_bounds(first)
                admit_here = e[0] >= m0
                disch_here = e[1] <= m1 and e[3] != "period"
                if e[3] == "death" and e[1] - 1 >= m1:
                    disch_here = False
                freq = {(True, True): "1", (True, False): "2", (False, True): "4", (False, False): "3"}[(admit_here, disch_here)]
                thru = (W.date_of(e[1] - 1) if e[3] == "death" else W.date_of(min(e[1], m1 - 1))) if disch_here else W.date_of(m1 - 1)
                days = []
                for day in range(a, z):
                    x = lv[day - e[0]]
                    q = int(hours[day - e[0]] * 4) if x == "C" else 0
                    days.append((day, x, ri[day] <= 60, q))
                c = dict(b=b.idx, i=i, code=e[2], mbi=b.mbi, frm=W.date_of(a), thru=thru, freq=freq, days=days,
                         loc=b.residence, gip_loc="Q5006" if e[2] == "BRK" else "Q5005", month=first)
                refresh(c)
                claims.append(c)
    return claims


def versions(claims):
    """Claim keys, submission dates and the versions each claim went through. Every original is submitted and paid.
    About one in forty is replaced and the replacement paid (the original reversed); one in two hundred is voided and
    billed again; and at every provider number some claims carrying inpatient days were replaced to rebill those days
    as routine home care, and the contractor returned those replacements, so they were never paid. The files are cut
    at 31 December 2026, so a correction is drawn only on a claim paid early enough for it to have run its course by
    then, each step's lag drawn within the room the cut leaves."""
    rng = stream(5)
    cut = W.date_of(LAST_DAY)

    def lag(base, lo, hi, end):
        room = (end - base).days
        return base + dt.timedelta(days=int(rng.integers(lo, min(hi, room + 1))))
    seq_no = 0
    for c in sorted(claims, key=lambda c: (c["month"], c["code"], c["mbi"], c["frm"])):
        seq_no += 1
        c["key"] = "%s%07d" % (CCN[c["code"]][-3:], 1000000 + seq_no * 7 + int(rng.integers(0, 7)))
        m0, m1 = month_bounds(c["month"])
        thru_day = (c["thru"] - W.DAY0).days
        c["submitted"] = W.date_of(max(m1 - 1, thru_day) + int(rng.integers(3, 19)))
        c["paid_on"] = c["submitted"] + dt.timedelta(days=int(rng.integers(12, 27)))
        if rng.random() < 0.015:
            c["paid_on"] = c["submitted"] + dt.timedelta(days=int(rng.integers(38, 66)))
        c["kind"] = "original"
    out = list(claims)
    by_code = {}
    for c in claims:
        by_code.setdefault(c["code"], []).append(c)
    extra = []
    for code, cs in sorted(by_code.items()):
        cs = sorted(cs, key=lambda c: c["key"])
        rep_end = cut - dt.timedelta(days=RETURN_AGE)
        inpatient = [c for c in cs if (c["units"]["G"] >= 3 or c["units"]["I"] >= 3) and (rep_end - c["paid_on"]).days >= 40]
        n_ret = max(4, int(round(0.06 * len(inpatient))))
        pick = set(rng.choice(len(inpatient), size=min(n_ret, len(inpatient)), replace=False).tolist())
        resp = [k for k, c in enumerate(inpatient) if c["units"]["I"] >= 3]
        for k in resp[:2]:
            pick.add(k)
        for k in sorted(pick):
            c = inpatient[k]
            moved = "G" if c["units"]["G"] >= 3 and (c["units"]["I"] < 3 or rng.random() < 0.7) else "I"
            rep = dict(c, days=[(d, "R" if x == moved else x, hi, q) for d, x, hi, q in c["days"]], kind="returned",
                       prior=c["key"])
            refresh(rep)
            rep["key"] = c["key"][:3] + "%07d" % (9000000 + int(rng.integers(0, 999999)))
            rep["submitted"] = lag(c["paid_on"], 40, 160, rep_end)
            extra.append(rep)
            c["returned_rep"] = rep["key"]
        rest = [c for c in cs if "returned_rep" not in c and (cut - c["paid_on"]).days >= 42]
        for c in [rest[k] for k in rng.choice(len(rest), size=int(0.025 * len(rest)), replace=False)]:
            days = list(c["days"])
            first_c = next((k for k, d in enumerate(days) if d[1] == "C"), None)
            if first_c is not None and rng.random() < 0.6:
                d, x, hi, q = days[first_c]
                days[first_c] = (d, x, hi, max(32, q + int(rng.choice([-4, -2, 2, 4]))))
            rep = dict(c, days=days, kind="replacement", prior=c["key"], loc="Q5002" if c["loc"] != "Q5002" else "Q5001")
            refresh(rep)
            rep["key"] = c["key"][:3] + "%07d" % (8000000 + int(rng.integers(0, 999999)))
            rep["submitted"] = lag(c["paid_on"], 30, 150, cut - dt.timedelta(days=12))
            rep["paid_on"] = lag(rep["submitted"], 12, 27, cut)
            extra.append(rep)
            c["replaced_by"] = rep["key"]
        rest = [c for c in rest if "replaced_by" not in c and (cut - c["paid_on"]).days >= 46]
        for c in [rest[k] for k in rng.choice(len(rest), size=max(2, int(0.005 * len(rest))), replace=False)]:
            void = dict(c, kind="void", prior=c["key"], units=dict(c["units"]), chc=list(c["chc"]))
            void["key"] = c["key"][:3] + "%07d" % (7000000 + int(rng.integers(0, 999999)))
            void["submitted"] = lag(c["paid_on"], 20, 90, cut - dt.timedelta(days=26))
            void["paid_on"] = lag(void["submitted"], 12, 27, cut - dt.timedelta(days=14))
            again = dict(c, kind="rebill", prior=None, chc=list(c["chc"]))
            again["key"] = c["key"][:3] + "%07d" % (6000000 + int(rng.integers(0, 999999)))
            again["submitted"] = lag(void["paid_on"], 2, 20, cut - dt.timedelta(days=12))
            again["paid_on"] = lag(again["submitted"], 12, 27, cut)
            extra += [void, again]
            c["voided_by"] = void["key"]
        moved = {"G": 0, "I": 0}
        for r in extra:
            if r["kind"] == "returned" and r["code"] == code:
                orig = next(o for o in cs if o["key"] == r["prior"])
                for lv in ("G", "I"):
                    moved[lv] += orig["units"][lv] - r["units"][lv]
        review(rng, cs, cut, moved)
    out += extra
    for c in out:
        c.setdefault("prior", None)
    return out


def review(rng, cs, cut, moved):
    """The contractor's prepayment review of inpatient levels of care: claims carrying general inpatient or respite days
    are held for records (paid 75 to 118 days after submission, no interest, not being clean claims) and on most of
    them some of those days are paid at the routine home care rate, the last days of the claim's inpatient level. The
    claim stays as billed; only the payment shows it. Claims are reviewed until the routine-paid days reach a share of
    the provider number's days of care, with general inpatient and respite days among them in counts other than the
    days the returned replacements move, so no pair of readings cancels."""
    total = sum(len(c["days"]) for c in cs if c["kind"] == "original")
    need = REVIEW_SHARE * total
    pool = [c for c in cs if c["kind"] == "original" and "returned_rep" not in c and "replaced_by" not in c
            and "voided_by" not in c and (c["units"]["G"] >= 2 or c["units"]["I"] >= 2)
            and len({d[2] for d in c["days"]}) == 1 and (cut - c["submitted"]).days >= 118]
    pool.sort(key=lambda c: c["key"])
    order = rng.permutation(len(pool))
    got, seen = 0, {"G": 0, "I": 0}
    for k in order:
        c = pool[int(k)]
        if (got >= need and seen["G"] and seen["I"] and seen["G"] != moved["G"] and seen["I"] != moved["I"]
                and abs(got - moved["G"] - moved["I"]) >= SEPARATION * total):
            break
        cut_g = cut_i = 0
        if rng.random() < 0.72:
            if c["units"]["G"] >= 2:
                cut_g = int(rng.integers(1, c["units"]["G"] + 1))
            if c["units"]["I"] >= 2:
                cut_i = int(rng.integers(1, c["units"]["I"] + 1))
        paid = list(c["days"])
        for lv, n in (("G", cut_g), ("I", cut_i)):
            idx = [j for j, d in enumerate(paid) if d[1] == lv][-n:] if n else []
            for j in idx:
                d, x, hi, q = paid[j]
                paid[j] = (d, "R", hi, q)
        c["paid_days"] = paid
        c["review"] = {"G": cut_g, "I": cut_i}
        c["paid_on"] = c["submitted"] + dt.timedelta(days=int(rng.integers(75, 119)))
        refresh(c)
        got += cut_g + cut_i
        seen["G"] += cut_g
        seen["I"] += cut_i


def tob(c):
    if c["kind"] in ("replacement", "returned"):
        return "0817"
    if c["kind"] == "void":
        return "0818"
    return "081" + c["freq"]


def payment(c, wi):
    return round(c["fixed"] + c["labor"] * wi[c["code"]], 2)


def paid_versions(allc):
    """The versions Medicare paid and did not reverse: originals not replaced or voided, accepted replacements and
    rebills. (Returned replacements were never paid; voids were paid as reversals.)"""
    return [c for c in allc if (c["kind"] == "original" and "replaced_by" not in c and "voided_by" not in c)
            or c["kind"] in ("replacement", "rebill")]


def remittances(allc, wi):
    """The remittance register: a row per claim payment and per reversal, the contractor's 2 per cent sequestration
    on its own column, and a provider-level interest row for each clean claim paid after 30 days."""
    rng = stream(6)
    rows = []
    icn = {}
    for c in sorted(allc, key=lambda c: (c.get("paid_on") or dt.date(2099, 1, 1), c["key"])):
        if c["kind"] == "returned":
            continue
        pay = payment(c, wi) if c["kind"] != "void" else 0.0
        if c["kind"] == "void":
            orig = next(o for o in allc if o["key"] == c["prior"])
            p0 = payment(orig, wi)
            rows.append(("reversal", c, orig, p0))
            continue
        if c["kind"] == "replacement":
            orig = next(o for o in allc if o["key"] == c["prior"])
            rows.append(("reversal", c, orig, payment(orig, wi)))
        rows.append(("payment", c, c, pay))
    out = []
    for kind, c, ref, pay in rows:
        if ref["key"] not in icn:
            icn[ref["key"]] = "%d%012d" % (2 if ref["paid_on"].year == 2025 else 3, int(rng.integers(10 ** 11, 10 ** 12)))
        paid = round(pay * (1 - W.SEQ), 2)
        seqa = round(pay - paid, 2)
        sign = -1 if kind == "reversal" else 1
        out.append(dict(remit_date=c["paid_on"], icn=icn[ref["key"]] if kind == "payment" else icn[ref["key"]],
                        patient_control_no=ref["key"], provider_number=CCN[c["code"]], mbi=c["mbi"],
                        stmt_from=c["frm"], stmt_thru=c["thru"], tob=tob(ref), claim_status="22" if kind == "reversal" else "1",
                        paid=sign * paid, sequestration=sign * seqa, record="CLP"))
        if kind == "payment" and (c["paid_on"] - c["submitted"]).days > 30 and "review" not in c:
            days_late = (c["paid_on"] - c["submitted"]).days - 30
            out.append(dict(remit_date=c["paid_on"], icn=icn[ref["key"]], patient_control_no=ref["key"],
                            provider_number=CCN[c["code"]], mbi=c["mbi"], stmt_from=None, stmt_thru=None, tob="",
                            claim_status="", paid=round(paid * 0.045 * days_late / 365.0, 2), sequestration=0.0,
                            record="PLB L6"))
    return out
