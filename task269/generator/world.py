"""The clean truth for task269, before any record is written: the single-family class (the main call), the
condominium class (Ask A) and the Board of Review's hearings (Ask B).

The single-family world is drawn in one stream (common.SEED) exactly as the draw screened it: each neighbourhood's
market grew by its own rate in 2025 while the Assessor trended it by a factor set on the older market; permits were
picked up, Board of Review reductions carried into the base and a few per cent of values corrected; and every parcel
sold at arm's length in 2025 was reviewed and its value moved toward its price. Everything the records add
(identifiers, addresses, dates, transfers, hearings, splits) comes from other streams, so it moves no value."""
import datetime as dt

import numpy as np

import common as K

NB, NA = 30, 6


def sf_core(seed, N=K.N_SF, chase=0.65, csd=0.07, srate=0.065, trend=0.35, sd25=0.21, pperm=0.025, papp=0.035,
            pcor=0.03):
    """The single-family class in the draw's own stream (scratch w4.world, seed 391)."""
    r = np.random.default_rng(seed)
    area_of = np.repeat(np.arange(NA), NB // NA)
    g_area = r.uniform(0.04, 0.13, NA)
    growth = np.clip(g_area[area_of] + r.normal(0, 0.02, NB), 0.01, 0.18)
    fac = np.round(1 + np.clip(growth * trend + r.normal(0, 0.008, NB), 0.0, 0.08), 3)
    w = r.dirichlet(np.full(NB, 8.0))
    nbi = r.choice(NB, N, p=w)
    mv25 = np.exp(r.normal(np.log(310000), 0.38, N) + 0.15 * (area_of[nbi] - 2.5) / 2.5)
    av25 = np.round(mv25 * 0.92 * np.exp(r.normal(0, sd25, N)), -2)
    mv26 = mv25 * (1 + growth[nbi]) * np.exp(r.normal(0, 0.035, N))
    s25 = r.random(N) < srate
    m = r.integers(0, 12, N)
    r.integers(1, 29, N)                          # the draw's sale-day column, unused: kept so the stream holds
    u = r.random(N)
    kind = np.zeros(N, int)
    kind[u < pperm] = 1
    kind[(u >= pperm) & (u < pperm + papp) & ~s25] = 2
    kind[(u >= pperm + papp) & (u < pperm + papp + pcor)] = 3
    mult = np.ones(N)
    mult[kind == 1] = 1 + r.uniform(0.10, 0.32, (kind == 1).sum())
    mv26 = mv26 * np.where(kind == 1, mult * 0.9 + 0.1, 1.0)
    bor_after = av25.copy()
    cut = r.uniform(0.05, 0.19, (kind == 2).sum())
    bor_after[kind == 2] = np.round(av25[kind == 2] * (1 - cut), -2)
    corr = np.ones(N)
    corr[kind == 3] = np.exp(r.normal(0, 0.10, (kind == 3).sum()))
    base = np.where(kind == 2, bor_after, av25)
    av26u = np.round(base * fac[nbi] * mult * corr, -2)
    idx = np.round(100 * (1 + 0.085 * m / 12), 1)
    mv_at_sale = np.where((kind == 1) & s25, mv26 / (mult * 0.9 + 0.1), mv26)
    price = np.round(mv_at_sale * (idx / K.INDEX_JAN2026) * np.exp(r.normal(0, 0.06, N)), -2)
    av26 = av26u.copy()
    pre = np.round(base * fac[nbi] * corr, -2)
    pj = price * K.INDEX_JAN2026 / idx
    av26[s25] = np.round((pre[s25] + chase * (pj[s25] - pre[s25])) * np.exp(r.normal(0, csd, s25.sum())), -2)
    pk = s25 & (kind == 1)
    av26[pk] = np.round(av26[pk] * mult[pk], -2)
    return dict(nbi=nbi, area=area_of[nbi], fac=fac, growth=growth, av25=av25, bor_after=bor_after, av26=av26,
                av26u=av26u, mv25=mv25, mv26=mv26, s25=s25, kind=kind, mult=mult, month=m, price=price, idx=idx)


def _month_day(rng, month, lo=1, hi=28):
    return dt.date(2025, int(month) + 1, int(rng.integers(lo, hi + 1)))


class World:
    def __init__(self, seed=K.SEED):
        self.sf = sf_core(seed)
        self.rec = np.random.default_rng(K.SEED_REC)
        self._sf_records()
        self._condo(np.random.default_rng(K.SEED_CONDO))
        self._hearings()
        self._transfers()
        self._index()
        self._condo_permits()
        self._petitions()

    # ---- the single-family class: identifiers, attributes, splits, combinations, permits -------------------------
    def _sf_records(self):
        s, r = self.sf, self.rec
        N = len(s["av25"])
        order = np.lexsort((r.random(N), s["nbi"]))       # parcels laid out neighbourhood by neighbourhood
        ids = np.empty(N, object)
        book_of_nb = {}
        nxt_book = 101
        for k in range(NB):
            members = order[s["nbi"][order] == k]
            book_of_nb[k] = []
            pos = 0
            while pos < len(members):
                b = nxt_book
                nxt_book += 1
                book_of_nb[k].append(b)
                page = 1
                while pos < len(members) and page <= 49:
                    per = int(r.integers(18, 27))
                    num = int(r.integers(1, 4))
                    for _ in range(per):
                        if pos >= len(members):
                            break
                        ids[members[pos]] = (b, page, num)
                        pos += 1
                        num += int(1 + (r.random() < 0.12))
                    page += 1
            assert pos == len(members)
        self.sf_id = ids
        self.book_of_nb = book_of_nb
        lv = s["mv25"]
        self.sf_sqft = np.clip(np.round(1650 * (lv / 310000) ** 0.72 * np.exp(r.normal(0, 0.13, N)), -1), 620, 5200)
        self.sf_year = np.clip(np.round(1968 + 18 * r.standard_normal(N) + 6 * (s["area"] - 2.5)), 1890, 2023).astype(int)
        self.sf_land_share = np.clip(r.normal(0.24, 0.05, N), 0.11, 0.42)
        self._addresses()
        # sale dates: the draw's month; the deed's day, and the recording a few days on, inside 2025
        self.sf_deed = {}
        self.sf_recorded = {}
        for i in np.where(s["s25"])[0]:
            hi = 10 if (s["kind"][i] == 1 and s["month"][i] >= 10) else 27
            d = _month_day(r, s["month"][i], 1, hi)
            self.sf_deed[i] = d
            lag = int(r.integers(1, 15))
            rec_d = d + dt.timedelta(days=lag)
            if rec_d.year > 2025:
                rec_d = dt.date(2025, 12, 31) - dt.timedelta(days=int(r.integers(0, 3)))
                rec_d = max(rec_d, d)
            self.sf_recorded[i] = rec_d
        # free parcels: unsold, untouched by permits, appeals and corrections
        free = np.where((~s["s25"]) & (s["kind"] == 0))[0]
        r.shuffle(free)
        self.free = list(free)
        self.split_parents = sorted(self._take(K.N_SPLIT))
        pairs = []
        for _ in range(K.N_COMBINE):
            a = self.free.pop()
            nbrs = [j for j in self.free if s["nbi"][j] == s["nbi"][a] and self.sf_id[j][0] == self.sf_id[a][0]
                    and self.sf_id[j][1] == self.sf_id[a][1]]
            b = nbrs[0] if nbrs else self.free[-1]
            self.free.remove(b)
            a, b = sorted((a, b), key=lambda i: self.sf_id[i])
            pairs.append((a, b))
        self.combine_pairs = pairs
        self.split_share = {i: float(r.uniform(0.72, 0.86)) for i in self.split_parents}
        self.split_lot_no = {}
        # permits: work finaled in 2025 on every kind-1 parcel (after the deed where the parcel sold), plus open and
        # expired permits on untouched parcels that moved no value
        self.permits = []
        for i in np.where(s["kind"] == 1)[0]:
            if s["s25"][i]:
                iss = self.sf_deed[i] + dt.timedelta(days=int(r.integers(4, 16)))
                fin = iss + dt.timedelta(days=int(r.integers(9, 75)))
                if fin > dt.date(2025, 12, 30):
                    fin = dt.date(2025, 12, 30) - dt.timedelta(days=int(r.integers(0, 6)))
                    fin = max(fin, iss + dt.timedelta(days=2))
            else:
                iss = dt.date(2025, 1, 2) + dt.timedelta(days=int(r.integers(0, 280)))
                fin = iss + dt.timedelta(days=int(r.integers(21, 150)))
                if fin.year > 2025:
                    fin = dt.date(2025, 12, 19) - dt.timedelta(days=int(r.integers(0, 40)))
                    fin = max(fin, iss + dt.timedelta(days=14))
            pick = s["mult"][i] - 1
            work = WORK_TYPES[int(np.searchsorted([0.15, 0.21, 0.27, 1.0], pick))]
            valuation = int(round(s["av25"][i] * pick * float(r.uniform(0.85, 1.25)), -2))
            self.permits.append(dict(i=i, issued=iss, finaled=fin, status="FINALED", work=work, valuation=valuation))
        for i in self._take(int(round(0.011 * N))):
            iss = dt.date(2025, 1, 2) + dt.timedelta(days=int(r.integers(30, 350)))
            st = "OPEN" if r.random() < 0.7 else "EXPIRED"
            work = str(r.choice(["Re-roof", "Deck", "Window replacement", "Kitchen remodel", "Fence"]))
            self.permits.append(dict(i=i, issued=iss, finaled=None, status=st, work=work,
                                     valuation=int(round(float(r.uniform(4000, 38000)), -2))))
        self.permits.sort(key=lambda p: (p["issued"], int(p["i"])))

    def _addresses(self):
        """Each assessment page is one block of one street, house numbers rising along it; the neighbourhood's
        streets drawn from the county's street list (its own stream, so it moves nothing else)."""
        s = self.sf
        r = np.random.default_rng(K.SEED_REC + 31)
        N = len(s["av25"])
        self.sf_street = [None] * N
        by_page = {}
        for i in range(N):
            b, p, n = self.sf_id[i]
            by_page.setdefault((b, p), []).append((n, i))
        streets_of_nb = {k: list(r.choice(len(STREETS), 9, replace=False)) for k in range(NB)}
        for (b, p), members in sorted(by_page.items()):
            k = int(s["nbi"][members[0][1]])
            st = STREETS[streets_of_nb[k][(b * 7 + p) % 9]]
            house = int(r.integers(1, 60)) * 100 + int(r.integers(1, 40))
            for n, i in sorted(members):
                self.sf_street[i] = "%d %s" % (house, st)
                house += int(r.choice([2, 2, 4, 6]))

    def _take(self, n):
        out = [self.free.pop() for _ in range(n)]
        return out

    # ---- the condominium class ------------------------------------------------------------------------------------
    def _condo(self, r):
        units = []
        big = len(K.CONDO_PROJECTS) - 1
        self.condo_fac, self.condo_growth, self.condo_pps = [], [], []
        for pj, (name, nb, n, street) in enumerate(K.CONDO_PROJECTS):
            g = float(r.uniform(0.03, 0.12))
            fac = round(1 + 0.75 * g + float(r.normal(0, 0.006)), 3)
            self.condo_fac.append(fac)
            self.condo_growth.append(g)
            self.condo_pps.append(float(r.uniform(185, 340)))
            if pj == big:
                per_floor, floors = 14, 15
                for tower in ("A", "B"):
                    for f in range(floors):
                        for pos in range(per_floor):
                            area = r.uniform(500, 820) if tower == "A" else r.uniform(1060, 1620)
                            units.append(dict(pj=pj, tower=tower, floor=f + 2, pos=pos, area=float(area)))
            else:
                floors = max(3, int(round(n / 12)))
                for k in range(n):
                    units.append(dict(pj=pj, tower="", floor=2 + k % floors, pos=k // floors,
                                      area=float(r.uniform(560, 1700))))
        for u in units:
            g = self.condo_growth[u["pj"]]
            u["mv25"] = u["area"] * self.condo_pps[u["pj"]] * (1 + 0.012 * u["floor"]) * float(np.exp(r.normal(0, 0.07)))
            u["av25"] = round(u["mv25"] * 0.945 * float(np.exp(r.normal(0, 0.075))), -2)
            u["mv26"] = u["mv25"] * (1 + g) * float(np.exp(r.normal(0, 0.025)))
            u["kind"] = 0
        # old numbering (the 2016 declaration): tower A floor by floor, then tower B; other projects in order
        counters = {}
        for u in units:
            counters.setdefault(u["pj"], 0)
            counters[u["pj"]] += 1
            u["old"] = counters[u["pj"]]
        wex = [u for u in units if u["pj"] == big]
        # combinations (amended declaration): eight pairs of side-by-side tower B units on the top floors
        combos = []
        tops = [u for u in wex if u["tower"] == "B" and u["floor"] >= 12 and u["pos"] % 2 == 0 and u["pos"] < 12]
        pick = sorted(r.choice(len(tops), 8, replace=False))
        for j in pick:
            a = tops[j]
            b = [v for v in wex if v["tower"] == "B" and v["floor"] == a["floor"] and v["pos"] == a["pos"] + 1][0]
            combos.append((a, b))
        self.wex_combos = combos
        merged = {id(b) for a, b in combos}
        # new numbering: floor by floor across both towers, a combined pair taking one number
        new_order = sorted([u for u in wex if id(u) not in merged], key=lambda u: (u["floor"], u["tower"], u["pos"]))
        for k, u in enumerate(new_order):
            u["new"] = k + 1
        for a, b in combos:
            b["new"] = a["new"]
            b["merged_into"] = a
        for u in units:
            if u["pj"] != big:
                u["new"] = u["old"]
        # 2026 values: the project's factor; a combined pair carries the two units' values as one
        for u in units:
            u["av26"] = round(u["av25"] * self.condo_fac[u["pj"]], -2)
        # Board of Review reductions of 2025 condominium values, outside Wexley Commons
        others = [u for u in units if u["pj"] != big]
        self.condo_bor = []
        for j in r.choice(len(others), 31, replace=False):
            u = others[int(j)]
            cutv = float(r.uniform(0.05, 0.16))
            u["kind"] = 2
            u["bor_after"] = round(u["av25"] * (1 - cutv), -2)
            u["av26"] = round(u["bor_after"] * self.condo_fac[u["pj"]], -2)
            self.condo_bor.append(u)
        # sales: one market in 2025, smaller units in tower A changing hands most
        sales = []
        for j, (a, b) in enumerate(combos):
            if j % 8 in (0, 2, 3, 5, 6):      # the neighbour bought the unit next door before the two were joined
                sales.append(dict(u=b, month=int(r.integers(0, 6)), partner=None, joined=True))
        for u in units:
            if u.get("merged_into") is not None:
                continue
            t = (0.22 if u["tower"] == "A" else 0.055) if u["pj"] == big else 0.085
            if u["kind"] == 2:
                t = 0.0
            if r.random() < t:
                month = int(r.integers(0, 12))
                partner = [b for a, b in combos if a is u]
                sales.append(dict(u=u, month=month, partner=partner[0] if partner else None))
        for sale in sales:
            u = sale["u"]
            m = sale["month"]
            idx = round(100 * (1 + 0.085 * m / 12), 1)
            mv = u["mv26"] + (sale["partner"]["mv26"] if (sale["partner"] is not None and m >= 6) else 0.0)
            sale["price"] = round(mv * (idx / K.INDEX_JAN2026) * float(np.exp(r.normal(0, 0.05))), -2)
            sale["deed"] = dt.date(2025, m + 1, int(r.integers(1, 28)))
            sale["recorded"] = min(sale["deed"] + dt.timedelta(days=int(r.integers(1, 13))), dt.date(2025, 12, 31))
            if u["pj"] == big and sale["deed"] >= K.REDECLARED and sale["partner"] is not None:
                sale["combined"] = True          # the combined unit sold under its new number after July
            elif u["pj"] == big and sale["deed"] < K.REDECLARED and (sale["partner"] is not None or
                                                                     sale.get("joined")):
                sale["combined_after"] = True    # one of a pair combined after this sale
        for a, b in combos:
            a["av26"] = round((a["av25"] + b["av25"]) * self.condo_fac[a["pj"]], -2)
            a["partner_area"] = b["area"]
        self.condo_units = units
        self.condo_sales = sorted(sales, key=lambda x: (x["deed"], x["u"]["pj"], x["u"]["old"]))
        self.condo_ids()

    def condo_ids(self):
        """Condominium parcel numbers: one book per project, the unit number in the parcel's place."""
        self.condo_book = {pj: 201 + pj for pj in range(len(K.CONDO_PROJECTS))}
        self.condo_page = {pj: 10 + (pj * 3) % 7 for pj in range(len(K.CONDO_PROJECTS))}

    # ---- the Board of Review's 2025 hearings ----------------------------------------------------------------------
    def _hearings(self):
        s, r = self.sf, self.rec
        rows = []
        case = 18406
        # appeals of the 2024 roll still open at the turn of the year, heard January to May 2025
        carry = self._take(176)
        for i in carry:
            v24 = int(round(s["av25"][i] / float(r.uniform(1.025, 1.065)) * float(r.uniform(0.985, 1.015)), -2))
            if v24 == int(s["av25"][i]):
                v24 -= 300
            u = r.random()
            if u < 0.56:
                dec, after = "REDUCED", int(round(v24 * (1 - float(r.uniform(0.04, 0.17))), -2))
            elif u < 0.86:
                dec, after = "SUSTAINED", v24
            else:
                dec, after = "WITHDRAWN", None
            heard = dt.date(2025, 1, 7) + dt.timedelta(days=int(r.integers(0, 133)))
            rows.append(dict(i=int(i), cls="R1", case=None, heard=heard, decision=dec, before=v24, after=after,
                             roll=2024))
        # appeals of the 2025 roll: every Board of Review reduction in the world, then sustained and withdrawn ones
        for i in np.where(s["kind"] == 2)[0]:
            heard = dt.date(2025, 7, 14) + dt.timedelta(days=int(r.integers(0, 150)))
            rows.append(dict(i=int(i), cls="R1", case=None, heard=heard, decision="REDUCED", before=int(s["av25"][i]),
                             after=int(s["bor_after"][i]), roll=2025))
        for i in self._take(612):
            u = r.random()
            heard = dt.date(2025, 7, 14) + dt.timedelta(days=int(r.integers(0, 150)))
            if u < 0.82:
                rows.append(dict(i=int(i), cls="R1", case=None, heard=heard, decision="SUSTAINED",
                                 before=int(s["av25"][i]), after=int(s["av25"][i]), roll=2025))
            else:
                rows.append(dict(i=int(i), cls="R1", case=None, heard=None, decision="WITHDRAWN",
                                 before=int(s["av25"][i]), after=None, roll=2025))
        for u in self.condo_bor:
            heard = dt.date(2025, 7, 14) + dt.timedelta(days=int(r.integers(0, 150)))
            rows.append(dict(i=None, cu=u, cls="R2", case=None, heard=heard, decision="REDUCED", before=int(u["av25"]),
                             after=int(u["bor_after"]), roll=2025))
        # carried-over condominium appeals of the 2024 roll
        big = len(K.CONDO_PROJECTS) - 1
        pool = [u for u in self.condo_units if u["pj"] != big and u["kind"] == 0]
        for j in r.choice(len(pool), 22, replace=False):
            u = pool[int(j)]
            v24 = int(round(u["av25"] / float(r.uniform(1.02, 1.06)), -2))
            dec = "REDUCED" if r.random() < 0.6 else "SUSTAINED"
            after = int(round(v24 * (1 - float(r.uniform(0.04, 0.14))), -2)) if dec == "REDUCED" else v24
            heard = dt.date(2025, 1, 7) + dt.timedelta(days=int(r.integers(0, 133)))
            rows.append(dict(i=None, cu=u, cls="R2", case=None, heard=heard, decision=dec, before=v24, after=after,
                             roll=2024))
        # case numbers in the order the petitions were filed: 2024-roll petitions first
        rows.sort(key=lambda x: (x["roll"], x["heard"] or dt.date(2025, 12, 31), x.get("i") or 0))
        for x in rows:
            x["case"] = case
            case += int(1 + (r.random() < 0.18) + (r.random() < 0.05))
        # rehearings: twelve 2025-roll reductions heard a second time in December, the first decision less favourable
        red = [x for x in rows if x["roll"] == 2025 and x["decision"] == "REDUCED" and x["cls"] == "R1"]
        reh = []
        for j in r.choice(len(red), 12, replace=False):
            x = red[int(j)]
            first = dict(x)
            gap = x["before"] - x["after"]
            if r.random() < 0.5:
                first["decision"], first["after"] = "SUSTAINED", x["before"]
            else:
                first["after"] = int(round(x["after"] + gap * float(r.uniform(0.35, 0.65)), -2))
            first["heard"] = x["heard"] if x["heard"] <= dt.date(2025, 10, 31) else \
                dt.date(2025, 9, 15) + dt.timedelta(days=int(r.integers(0, 40)))
            x["heard"] = dt.date(2025, 12, 2) + dt.timedelta(days=int(r.integers(0, 10)))
            x["rehearing"] = True
            reh.append(first)
        rows.extend(reh)
        rows.sort(key=lambda x: (x["heard"] or dt.date(2026, 1, 1), x["case"]))
        self.hearings = rows

    # ---- transfers that are not arm's-length sales ------------------------------------------------------------------
    def _transfers(self):
        s, r = self.sf, self.rec
        N = len(s["av25"])
        out = []
        kinds = [("U1", "Quitclaim Deed", 0.33, 0.82), ("U2", "Sheriff's Deed", 0.48, 0.76),
                 ("U3", "Personal Representative's Deed", 0.0, 0.0), ("U4", "Warranty Deed", 0.28, 0.55)]
        counts = {"U1": 171, "U2": 58, "U3": 117, "U4": 36}
        for code, dtype, lo, hi in kinds:
            for _ in range(counts[code]):
                i = int(r.integers(0, N))
                if i in self.split_parents or any(i in p for p in self.combine_pairs):
                    continue
                d = dt.date(2025, 1, 2) + dt.timedelta(days=int(r.integers(0, 352)))
                cons = 0 if hi == 0 else int(round(s["mv26"][i] * float(r.uniform(lo, hi)), -2))
                if code == "U3" and r.random() < 0.4:
                    cons = int(round(s["mv26"][i] * float(r.uniform(0.6, 0.9)), -2))
                out.append(dict(i=[i], code=code, dtype=dtype, deed=d, cons=cons))
        # deeds conveying several parcels (U5): investors and builders buying neighbouring houses
        for _ in range(11):
            k = int(r.integers(0, NB))
            cand = [int(j) for j in self.free[-400:] if s["nbi"][j] == k][:4]
            if len(cand) < 2:
                continue
            n = int(r.integers(2, min(4, len(cand)) + 1))
            parcels = cand[:n]
            for j in parcels:
                self.free.remove(j)
            d = dt.date(2025, 1, 2) + dt.timedelta(days=int(r.integers(0, 352)))
            cons = int(round(sum(s["mv26"][j] for j in parcels) * float(r.uniform(0.78, 0.93)), -2))
            out.append(dict(i=parcels, code="U5", dtype="Special Warranty Deed", deed=d, cons=cons))
        self.sf_transfers = out

    # ---- interior work on condominium units, in its own stream ----------------------------------------------------------
    def _condo_permits(self):
        """Buyers who remodelled after their purchase, sellers who remodelled before their sale, owners who did not
        sell, and permits still open. Finaled work is picked up in the unit's 2026 value. A permit carries the unit's
        parcel number as it stood on the day it was issued, and the unit in its description."""
        r = np.random.default_rng(K.SEED_CPERMIT)
        big = len(K.CONDO_PROJECTS) - 1
        times = {}
        for sale in self.condo_sales:
            times[id(sale["u"])] = times.get(id(sale["u"]), 0) + 1
        plain = [s for s in self.condo_sales if not s.get("joined") and not s.get("combined_after")
                 and not s.get("combined") and s["u"].get("merged_into") is None
                 and not any(a is s["u"] for a, b in self.wex_combos) and times[id(s["u"])] == 1]
        wex = [s for s in plain if s["u"]["pj"] == big]
        oth = [s for s in plain if s["u"]["pj"] != big]
        june = dt.date(2025, 6, 12)
        early = [s for s in wex if s["deed"] <= june]
        late = [s for s in wex if s["deed"] >= K.REDECLARED and s["deed"] <= dt.date(2025, 10, 15)]
        used = set()

        def pick(pool, n):
            pool = [s for s in pool if id(s["u"]) not in used]
            out = [pool[int(j)] for j in sorted(r.choice(len(pool), min(n, len(pool)), replace=False))]
            used.update(id(s["u"]) for s in out)
            return out

        self.condo_permits = []

        def add(u, issued, finaled, status):
            work = str(r.choice(["Kitchen remodel", "Bathroom remodel", "Kitchen and bath remodel",
                                 "Interior alterations", "Flooring and kitchen remodel"]))
            val = int(round(float(r.uniform(16000, 78000)), -2))
            self.condo_permits.append(dict(u=u, issued=issued, finaled=finaled, status=status, work=work,
                                           valuation=val))
            return val

        def pickup(u, val):
            inc = val * float(r.uniform(0.55, 0.85))
            if u.get("partner_area") is not None:
                return inc
            u["av26"] = round((u.get("bor_after", u["av25"]) + inc) * self.condo_fac[u["pj"]], -2)
            return inc

        # bought, then remodelled: the work finaled after the deed and before the assessment date
        before_july = pick(early, 7)
        after_july = pick([s for s in wex if s["deed"] < K.REDECLARED and s["deed"] >= dt.date(2025, 3, 1)], 6)
        after_sale = before_july + after_july + pick(late, 2) + pick(oth, 5)
        for s in after_sale:
            if s in before_july:
                iss = s["deed"] + dt.timedelta(days=int(r.integers(6, 19)))
            elif s in after_july:
                iss = K.REDECLARED + dt.timedelta(days=int(r.integers(2, 75)))
            else:
                iss = s["deed"] + dt.timedelta(days=int(r.integers(8, 45)))
            fin = iss + dt.timedelta(days=int(r.integers(24, 88)))
            fin = min(fin, dt.date(2025, 12, 22) - dt.timedelta(days=int(r.integers(0, 9))))
            fin = max(fin, iss + dt.timedelta(days=14))
            val = add(s["u"], iss, fin, "FINALED")
            pickup(s["u"], val)
        # remodelled, then sold: the work finaled before the deed, the price paying for it
        for s in pick([x for x in plain if x["deed"] >= dt.date(2025, 4, 15)], 5):
            fin = s["deed"] - dt.timedelta(days=int(r.integers(12, 40)))
            iss = max(fin - dt.timedelta(days=int(r.integers(25, 70))), dt.date(2025, 1, 6))
            val = add(s["u"], iss, fin, "FINALED")
            inc = pickup(s["u"], val)
            s["price"] = round(s["price"] * (1 + inc / 0.945 / s["u"]["mv26"]), -2)
        # owners who did not sell: work finaled, and permits still open or lapsed
        sold_units = {id(s["u"]) for s in self.condo_sales}
        idle = [u for u in self.condo_units if id(u) not in sold_units and u.get("merged_into") is None
                and u.get("partner_area") is None]
        for j in sorted(r.choice(len(idle), 30, replace=False)):
            u = idle[int(j)]
            iss = dt.date(2025, 1, 6) + dt.timedelta(days=int(r.integers(0, 300)))
            if r.random() < 0.72:
                fin = min(iss + dt.timedelta(days=int(r.integers(21, 95))), dt.date(2025, 12, 19))
                val = add(u, iss, fin, "FINALED")
                pickup(u, val)
            else:
                add(u, iss, None, "OPEN" if r.random() < 0.7 else "EXPIRED")
        for p in self.condo_permits:
            u = p["u"]
            p["number"] = u["new"] if (u["pj"] == big and p["issued"] >= K.REDECLARED) else u["old"]
            p["label"] = ("%s-%d%02d" % (u["tower"], u["floor"], u["pos"] + 1)) if u["tower"] else \
                ("%d%02d" % (u["floor"], u["pos"] + 1))
        self.condo_permits.sort(key=lambda p: (p["issued"], p["u"]["pj"], p["number"]))

    # ---- petitions listing several parcels, and more rehearings, in their own stream --------------------------------
    def _petitions(self):
        """An owner's or an agent's petition for several houses, and a condominium association's for units in its
        building: each parcel keeps its own decision and values, and the petition's parcels share its case number
        and its hearing. Rehearings in every market area."""
        r = np.random.default_rng(K.SEED_PETITION)
        s = self.sf
        rows = self.hearings
        cases = {}
        for x in rows:
            cases.setdefault(x["case"], []).append(x)
        area = lambda x: int(s["nbi"][x["i"]]) // 5
        single = [x for x in rows if x["roll"] == 2025 and x["cls"] == "R1" and x["heard"] is not None
                  and len(cases[x["case"]]) == 1]
        # rehearings: at least two reductions heard again in every market area
        reh_first = {}
        for c, xs in cases.items():
            if len(xs) == 2 and xs[0]["cls"] == "R1":
                a = area(xs[0])
                first = min(xs, key=lambda x: x["heard"])
                reh_first.setdefault(a, []).append(first["decision"])
        taken = set()
        for a in range(NA):
            have = sum(1 for d in reh_first.get(a, []) if d == "REDUCED")
            pool = [x for x in single if area(x) == a and x["decision"] == "REDUCED" and id(x) not in taken]
            for j in sorted(r.choice(len(pool), max(0, 2 - have) + 1, replace=False)):
                x = pool[int(j)]
                taken.add(id(x))
                first = dict(x)
                gap = x["before"] - x["after"]
                first["after"] = int(round(x["after"] + gap * float(r.uniform(0.35, 0.65)), -2))
                first["heard"] = x["heard"] if x["heard"] <= dt.date(2025, 10, 31) else \
                    dt.date(2025, 9, 15) + dt.timedelta(days=int(r.integers(0, 40)))
                x["heard"] = dt.date(2025, 12, 2) + dt.timedelta(days=int(r.integers(0, 10)))
                x["rehearing"] = True
                rows.append(first)
        # rehearings the Assessor asked for, the Board restoring the certified value: one in every market area
        for a in range(NA):
            pool = [x for x in single if area(x) == a and x["decision"] == "SUSTAINED" and id(x) not in taken]
            x = pool[int(r.integers(0, len(pool)))]
            taken.add(id(x))
            first = dict(x)
            first["decision"] = "REDUCED"
            first["after"] = int(round(x["before"] * (1 - float(r.uniform(0.04, 0.12))), -2))
            first["heard"] = x["heard"] if x["heard"] <= dt.date(2025, 10, 31) else \
                dt.date(2025, 9, 15) + dt.timedelta(days=int(r.integers(0, 40)))
            x["heard"] = dt.date(2025, 12, 2) + dt.timedelta(days=int(r.integers(0, 10)))
            x["rehearing"] = True
            rows.append(first)
        # an owner's or an agent's petition for several houses in one neighbourhood
        free = [x for x in single if id(x) not in taken]
        by_nb = {}
        for x in free:
            by_nb.setdefault(int(s["nbi"][x["i"]]), []).append(x)
        self.petitions = []
        for k in range(NB):
            pool = by_nb.get(k, [])
            r.shuffle(pool)
            for _ in range(3 + int(r.integers(0, 2))):
                n = int(r.choice([2, 2, 3, 3, 4, 5, 6]))
                if len(pool) < n:
                    break
                members = [pool.pop() for _ in range(n)]
                lead = min(members, key=lambda x: x["case"])
                for x in members:
                    x["case"], x["heard"] = lead["case"], lead["heard"]
                self.petitions.append(members)
        # a condominium association's petition for units in its building, the Board deciding unit by unit
        big = len(K.CONDO_PROJECTS) - 1
        by_pj = {}
        for x in rows:
            if x["cls"] == "R2" and x["roll"] == 2025 and x["decision"] == "REDUCED":
                by_pj.setdefault(x["cu"]["pj"], []).append(x)
        appealed = {id(x["cu"]) for x in rows if x["cls"] == "R2"}
        for pj, reduced in sorted(by_pj.items()):
            lead = min(reduced, key=lambda x: x["case"])
            members = list(reduced)
            idle = [u for u in self.condo_units if u["pj"] == pj and id(u) not in appealed and u["kind"] == 0]
            for j in sorted(r.choice(len(idle), min(len(idle), int(r.integers(1, 6))), replace=False)):
                u = idle[int(j)]
                appealed.add(id(u))
                x = dict(i=None, cu=u, cls="R2", case=None, heard=None, decision="SUSTAINED", before=int(u["av25"]),
                         after=int(u["av25"]), roll=2025)
                members.append(x)
                rows.append(x)
            for x in members:
                x["case"], x["heard"] = lead["case"], lead["heard"]
            self.petitions.append(members)
        assert big not in by_pj

        def pkey(x):
            if x["cls"] == "R1":
                return tuple(int(v) for v in self.sf_id[x["i"]])
            u = x["cu"]
            return (self.condo_book[u["pj"]], self.condo_page[u["pj"]], u["old"])
        rows.sort(key=lambda x: (x["heard"] or dt.date(2026, 1, 1), x["case"], pkey(x)))
        self.hearings = rows

    # ---- the county's monthly residential price index -----------------------------------------------------------------
    def _index(self):
        r = np.random.default_rng(K.SEED_REC + 7)
        vals = {}
        for m in range(13):
            y, mo = 2025 + m // 12, m % 12 + 1
            vals[(y, mo)] = round(100 * (1 + 0.085 * m / 12), 1)
        v = 100.0
        y, mo = 2025, 1
        yearly = {2024: 0.071, 2023: 0.052, 2022: 0.118, 2021: 0.143, 2020: 0.067, 2019: 0.041}
        while (y, mo) > (2019, 1):
            mo -= 1
            if mo == 0:
                y, mo = y - 1, 12
            g = yearly[y] / 12 + float(r.normal(0, 0.0012))
            v = v / (1 + g)
            vals[(y, mo)] = round(v, 1)
        v = vals[(2026, 1)]
        for mo in range(2, 7):
            v = v * (1 + 0.046 / 12 + float(r.normal(0, 0.0009)))
            vals[(2026, mo)] = round(v, 1)
        self.index = dict(sorted(vals.items()))


STREETS = ["Ash St", "Beacon Ave", "Calvert Rd", "Dillard Ln", "Elkhorn Dr", "Fairmont Ave", "Gable St", "Holloway Rd",
           "Ingram Ave", "Jessup St", "Keel Ct", "Lowell St", "Mason Rd", "Nolan Ave", "Oakmont Dr", "Parrish Ln",
           "Quincy St", "Redfield Rd", "Sutter Ave", "Talbot St", "Underhill Rd", "Vance Ave", "Walden Dr", "Yates St",
           "Abernathy Ln", "Bramble Way", "Cortland Ave", "Delmar St", "Everly Rd", "Finch Ln", "Grover Ave",
           "Hyde Park Dr", "Ivy Ln", "Juniper Dr", "Kerrigan St", "Larch Ave", "Merritt Rd", "Northgate Dr",
           "Overlook Rd", "Primrose Ln", "Ridgeview Dr", "Sheridan Ave", "Tolliver St", "Upton Rd", "Valley View Dr",
           "Whitcomb St", "Brandt Ave", "Coyle St", "Driscoll Rd", "Emmet St", "Fowler Ave", "Garnet St", "Hester Ln",
           "Ironwood Dr", "Kimball Ave", "Lennox St", "Mayfield Rd", "Newell St", "Orchard St", "Pickett Ave",
           "Royce St", "Sumner Ave", "Trent St", "Vickers Rd", "Wardell Ave", "Bexley Rd", "Coburn St", "Dunham Ave",
           "Ellery St", "Farrow Rd", "Gilchrist Ave", "Hampden St", "Kellogg Ave", "Langley Rd", "Morrow St",
           "Prentice Ave", "Rowan St", "Shelby Rd", "Thatcher Ave", "Wilder St"]
WORK_TYPES = ["Bathroom/kitchen remodel", "Finished basement", "Garage addition", "Room addition"]
