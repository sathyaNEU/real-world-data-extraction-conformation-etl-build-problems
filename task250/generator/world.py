"""task250 architecture 4: the clean truth of the IEIF 2026 household survey programme.

Sampled addresses, the households at them, who in each household answered and in which mode, the web sessions,
refusals and the letters the postal service returned. Nothing here is mess: pack.py writes the files the way the
institute's systems write them. Each component draws from its own stream, so a later change to one leaves the
others' draws where they were."""
import datetime as dt
import numpy as np

import params as P

DAYS = 365


def stream(name):
    h = sum((i + 1) * ord(ch) for i, ch in enumerate(name))
    return np.random.default_rng([P.SEED, h])


def birthday_density():
    x = np.arange(DAYS)
    d = (1 + P.BDAY_A1 * np.cos(2 * np.pi * (x - P.BDAY_P1) / DAYS)
         + P.BDAY_A2 * np.cos(4 * np.pi * (x - P.BDAY_P2) / DAYS))
    return d / d.sum()


_MD = [(dt.date(2025, 1, 1) + dt.timedelta(days=i)) for i in range(DAYS)]   # a non-leap calendar


def month_day(doy):
    d = _MD[doy]
    return d.month, d.day


def next_birthday_days(bmonth, bday, letter):
    """Days from the letter date to the adult's next birthday strictly after it (1 to 366). A 29 February
    birthday falls on 1 March in a year without that day."""
    def on(year):
        if bmonth == 2 and bday == 29:
            try:
                return dt.date(year, 2, 29)
            except ValueError:
                return dt.date(year, 3, 1)
        return dt.date(year, bmonth, bday)
    b = on(letter.year)
    if b <= letter:
        b = on(letter.year + 1)
    return (b - letter).days


def build():
    W = {}
    dens = birthday_density()
    rs_addr = stream("addresses")
    # ---------------------------------------------------------------- addresses
    rows = []
    reg_codes = [r[0] for r in P.REGIONS]
    reg_p = np.array([r[2] for r in P.REGIONS])
    reg_p = reg_p / reg_p.sum()
    st_names = [s[0] for s in P.ADDRESS_STATUS]
    st_p = np.array([s[1] for s in P.ADDRESS_STATUS])
    st_p = st_p / st_p.sum()
    for si, (code, en, pt, letter, reserve, n_main, base, prof) in enumerate(P.SURVEYS):
        releases = [(0, letter, n_main)]
        if reserve:
            releases.append((1, reserve[0], reserve[1]))
        for rel, ldate, n in releases:
            reg = rs_addr.choice(len(reg_codes), size=n, p=reg_p)
            sta = rs_addr.choice(len(st_names), size=n, p=st_p)
            for i in range(n):
                rows.append((si, rel, ldate, int(reg[i]), int(sta[i])))
    n_addr = len(rows)
    W["addr_survey"] = np.array([r[0] for r in rows])
    W["addr_release"] = np.array([r[1] for r in rows])
    W["addr_letter"] = [r[2] for r in rows]
    W["addr_region"] = np.array([r[3] for r in rows])
    W["addr_status"] = np.array([r[4] for r in rows])
    W["status_names"] = st_names
    W["region_codes"] = reg_codes
    # municipality codes inside each region (four digits, the district pair first)
    rs_mun = stream("municipalities")
    mun_by_region = {}
    district = {"NOR": ["01", "03", "04", "13", "16", "17", "18"], "CEN": ["05", "06", "09", "10"],
                "LVT": ["11", "14", "15"], "ALE": ["02", "07", "12"], "ALG": ["08"], "ACO": ["41", "42", "43",
                "44", "45", "46", "47", "48", "49"], "MAD": ["31", "32"]}
    for rc in reg_codes:
        codes = []
        for dcode in district[rc]:
            k = int(rs_mun.integers(4, 19))
            for m in sorted(rs_mun.choice(np.arange(1, 25), size=k, replace=False)):
                codes.append(dcode + "%02d" % m)
        mun_by_region[rc] = codes
    W["mun_by_region"] = mun_by_region
    W["addr_mun"] = [mun_by_region[reg_codes[r]][int(rs_mun.integers(len(mun_by_region[reg_codes[r]])))]
                     for r in W["addr_region"]]
    # ---------------------------------------------------------------- households at occupied addresses
    rs_hh = stream("households")
    occ = np.where(W["addr_status"] == st_names.index("occupied"))[0]
    W["occ"] = occ
    hh_k = rs_hh.choice(np.arange(1, 6), size=len(occ), p=np.array(P.K_PROBS) / sum(P.K_PROBS))
    members = []          # per household: list of (female, age_at_letter, bmonth, bday, byear)
    children = rs_hh.poisson(0.42, size=len(occ))
    for j, a in enumerate(occ):
        k = int(hh_k[j])
        letter = W["addr_letter"][a]
        ages, sexes = [], []
        if k == 1:
            ages.append(int(np.clip(rs_hh.gamma(5.2, 10.6) + 18, 18, 96)))
            sexes.append(bool(rs_hh.random() < 0.58))
        else:
            head = int(np.clip(rs_hh.normal(52, 15), 22, 92))
            ages.append(head)
            sexes.append(bool(rs_hh.random() < 0.5))
            if rs_hh.random() < 0.88:
                ages.append(int(np.clip(head + rs_hh.integers(-7, 5), 19, 95)))
                sexes.append((not sexes[0]) if rs_hh.random() < 0.93 else bool(rs_hh.random() < 0.5))
            else:
                ages.append(int(np.clip(rs_hh.normal(40, 16), 18, 90)))
                sexes.append(bool(rs_hh.random() < 0.5))
            for _ in range(k - 2):
                if head >= 42 and rs_hh.random() < 0.78:
                    ages.append(int(np.clip(head - rs_hh.integers(22, 36), 16, 70)))
                elif rs_hh.random() < 0.5:
                    ages.append(int(np.clip(head + rs_hh.integers(22, 32), 50, 99)))
                else:
                    ages.append(int(rs_hh.integers(18, 80)))
                sexes.append(bool(rs_hh.random() < 0.5))
        mem = []
        for f, ag in zip(sexes, ages):
            doy = int(rs_hh.choice(DAYS, p=dens))
            bm, bd = month_day(doy)
            this_year = dt.date(letter.year, bm, bd)
            byear = letter.year - ag if this_year <= letter else letter.year - ag - 1
            if bm == 2 and bd == 28 and (byear % 4 == 0) and rs_hh.random() < 0.5:
                bd = 29
            mem.append((f, ag, bm, bd, byear))
        members.append(mem)
    W["hh_k"] = hh_k
    W["hh_members"] = members
    W["hh_children"] = children
    # ---------------------------------------------------------------- response, mode and selection
    rs_resp = stream("response")
    rs_sel = stream("selection")
    resp = np.zeros(len(occ), bool)
    mode = np.full(len(occ), -1)
    respondent = np.full(len(occ), -1)
    compliant = np.zeros(len(occ), bool)
    is_min = np.zeros(len(occ), bool)
    confirm = np.full(len(occ), -1)          # 1 yes, 2 no but I answer, 0 blank (paper)
    day = np.zeros(len(occ), int)            # days after the letter the kept return was received
    for j, a in enumerate(occ):
        si = W["addr_survey"][a]
        code, en, pt, _main_letter, reserve, n_main, base, prof = P.SURVEYS[si]
        letter = W["addr_letter"][a]      # the household's own first letter: the reserve release's for its addresses
        mem = members[j]
        oldest = max(m[1] for m in mem)
        k = len(mem)
        p = base * P.REGION_RESP[reg_codes[W["addr_region"][a]]] * (0.78 + 0.0062 * min(oldest, 85))
        p *= 1.0 if k > 1 else 0.93
        if rs_resp.random() >= min(p, 0.9):
            continue
        resp[j] = True
        p_paper = float(np.clip(0.10 + 0.0095 * (oldest - 30), 0.08, 0.82))
        mode[j] = 1 if rs_resp.random() < p_paper else 0
        # selection
        D = [next_birthday_days(m[2], m[3], letter) for m in mem]
        dmin = min(D)
        mins = [i for i, d in enumerate(D) if d == dmin]
        if k == 1:
            r = 0
            comp = True
        else:
            c = P.COMPLIANCE[(code, P.MODES[mode[j]])]
            comp = bool(rs_sel.random() < c)
            if comp:
                r = int(mins[int(rs_sel.integers(len(mins)))])
            else:
                strength = P.PROFILE_STRENGTH[prof]
                if rs_sel.random() < strength:
                    idx = list(range(k))
                    if prof == "oldest_woman":
                        w = [i for i in idx if mem[i][0]] or idx
                        r = max(w, key=lambda i: (mem[i][1], -i))
                    elif prof == "youngest":
                        r = min(idx, key=lambda i: (mem[i][1], i))
                    elif prof == "oldest":
                        r = max(idx, key=lambda i: (mem[i][1], -i))
                    elif prof == "woman":
                        w = [i for i in idx if mem[i][0]] or idx
                        r = int(w[int(rs_sel.integers(len(w)))])
                    elif prof == "man":
                        w = [i for i in idx if not mem[i][0]] or idx
                        r = int(w[int(rs_sel.integers(len(w)))])
                    else:
                        r = int(rs_sel.integers(k))
                else:
                    r = int(rs_sel.integers(k))
        respondent[j] = r
        compliant[j] = comp
        is_min[j] = D[r] == dmin
        # the confirmation item
        if is_min[j]:
            confirm[j] = 1 if (mode[j] == 0 or rs_sel.random() > 0.05) else 0
        else:
            u = rs_sel.random()
            if mode[j] == 0:
                confirm[j] = 2 if u < 0.12 else 1
            else:
                confirm[j] = 2 if u < 0.08 else (0 if u < 0.18 else 1)
        # when the kept return arrived
        if mode[j] == 0:
            v = rs_resp.random()
            if v < 0.47:
                day[j] = int(rs_resp.integers(1, 7))
            elif v < 0.80:
                day[j] = int(rs_resp.integers(7, 21))
            else:
                day[j] = int(rs_resp.integers(21, 49))
        else:
            day[j] = int(np.clip(rs_resp.gamma(2.4, 5.5) + 24, 24, 55))
    W["resp"], W["mode"], W["respondent"] = resp, mode, respondent
    W["compliant"], W["is_min"], W["confirm"], W["day"] = compliant, is_min, confirm, day
    W["dens"] = dens
    return W


if __name__ == "__main__":
    import time
    t = time.time()
    W = build()
    print("addresses", len(W["addr_survey"]), "occupied", len(W["occ"]), "responding", int(W["resp"].sum()),
          "%.1fs" % (time.time() - t))
