"""Write the evidence pack: the appraiser's roll, the two permit systems, the plat index, the utility's premise,
account, meter and receipt extracts, the lookup and dictionary files and the two distractors. Documents are in
docs.py."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np

import common as C
from world import AREAS, World
from utility import Utility, FEE

SUFFIX = ["St", "Ter", "Pl", "Ln", "Ct", "Way"]
SUFFIX_LONG = {"St": "STREET", "Ter": "TERRACE", "Pl": "PLACE", "Ln": "LANE", "Ct": "COURT", "Way": "WAY"}


def _ord(n):
    return "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def plat_records(w):
    """plat book, page and recording date of each unit: the land company recorded its units in order, 1958 to
    1971, each plat running to several pages of the county's plat books"""
    g = C.stream("platbooks")
    out = {}
    book, page = 12, int(g.integers(20, 60))
    day = dt.date(1958, 3, 11)
    n = len(w.unit_no)
    for k, u in enumerate(sorted(w.unit_no)):
        pages = int(g.integers(9, 31))
        if page + pages > 100:
            book += 1
            page = 1
        out[u] = (book, page, day)
        page += pages
        span = (dt.date(1971, 9, 30) - day).days
        day = day + dt.timedelta(days=int(max(20, g.normal(span / max(n - k - 1, 1), 25))))
        if day > dt.date(1971, 11, 30):
            day = dt.date(1971, 11, 30)
    return out


class Identity:
    """Street names, addresses, straps and legal descriptions for every lot."""

    def __init__(self, w: World):
        self.w = w
        g = C.stream("identity")
        L = w.L
        counters = {}
        unit_prefix = {}
        for u, ai in zip(w.unit_no, w.unit_area):
            nm = AREAS[ai][0]
            if nm == "Core":
                p = ["SE", "SW", "SE", "SW", "NE", "SE"][u % 6]
            elif nm.startswith("Southwest"):
                p = "SW"
            elif nm.startswith("Central"):
                p = "SE" if u % 2 else "NE"
            elif nm.startswith("Northwest"):
                p = "NW"
            else:
                p = "NE" if u % 2 else "N"
            unit_prefix[u] = p
        # each unit's E-W streets in grid order
        seg_unit = np.array(w.seg_unit)
        seg_row_key = {}
        for sid, (sname, hb, u) in enumerate(zip(w.seg_street, w.seg_hblock, w.seg_unit)):
            seg_row_key.setdefault((u, sname), []).append(sid)
        self.seg_name = [None] * w.nseg
        for (u, sname) in sorted(seg_row_key, key=lambda k: (k[0], min(seg_row_key[k]))):
            p = unit_prefix[u]
            k = counters.get(p, 0)
            counters[p] = k + 1
            ordn = 1 + k // len(SUFFIX)
            suf = SUFFIX[(k * 5) % len(SUFFIX)]
            name = "%s %d%s %s" % (p, ordn, _ord(ordn), suf)
            for sid in seg_row_key[(u, sname)]:
                self.seg_name[sid] = name
        names = np.array(self.seg_name, dtype=object)
        self.street = names[L["seg"]]
        self.hnum = L["hnum"]
        self.addr = np.array(["%d %s" % (h, s) for h, s in zip(self.hnum, self.street)], dtype=object)
        self.addr_uc = np.array([a.upper() for a in self.addr], dtype=object)
        unit_sec = {u: 1 + (u * 7) % 36 for u in w.unit_no}
        unit_twp = {u: 43 + (u % 3 == 0) for u in w.unit_no}
        unit_rng = {u: 22 + u % 3 for u in w.unit_no}
        self.strap = np.array(["%02d-%d-%d-P%02d-%05d.%04d" % (unit_sec[u], unit_twp[u], unit_rng[u], u, b + 1, ln * 10)
                               for u, b, ln in zip(L["unit"], L["block"], L["lotno"])], dtype=object)
        recs = plat_records(w)
        book = {u: (recs[u][0], recs[u][1]) for u in w.unit_no}
        self.legal = np.array(["PORT ARDELL UNIT %d BLK %d PB %d PG %d LOT %d" % (u, b + 1, book[u][0], book[u][1], ln)
                               for u, b, ln in zip(L["unit"], L["block"], L["lotno"])], dtype=object)
        assert len(set(self.addr)) == w.N and len(set(self.strap)) == w.N
        self.unit_prefix = unit_prefix


BUILDER_STEMS = ["Kessler", "Marlowe", "Dunbar", "Halvorsen", "Pruitt", "Castellano", "Whitcomb", "Barrera", "Lindgren",
                 "Okafor", "Ruiz", "Sorensen", "Gallagher", "Thibodeaux", "Nakamura", "Pellegrino", "Ashby", "Montoya",
                 "Fairweather", "Delacroix", "Hargrove", "Quintero", "Beckwith", "Stavros", "Mulcahy", "Ferrante",
                 "Ochoa", "Brannigan", "Vukovich", "Esposito", "Calloway", "Draper", "Iverson", "Lombardi", "Pacheco",
                 "Rinaldi", "Tremblay", "Waddell", "Zielinski", "Abernathy", "Cardenas", "Holloway", "Jankowski",
                 "Kowalczyk", "Mancuso", "Navarro", "Petrakis", "Sandoval", "Vasquez", "Whitaker"]
BUILDER_FORMS = ["%s Homes LLC", "%s Construction Inc", "%s Custom Homes", "%s & Sons Builders Inc", "%s Building Group LLC",
                 "%s Contracting Corp", "%s Residential LLC", "%s Homes of SWFL Inc"]
PRODUCTION = ["Pemberton-Lyle Homes LLC", "Varga Residential Inc", "Holtzclaw Communities LLC", "Dunmore & Reyes Homes Inc",
              "Abrego Building Co", "Kittredge Homes Inc", "Moravec Residential LLC", "Okonkwo Builders Inc",
              "Strand-Pell Homes LLC", "Brannock Homebuilders Inc", "Corwin Vance Homes LLC", "Quarles Residential Group"]


def builder_names():
    g = C.stream("builders")
    out = list(PRODUCTION)
    used = set(out)
    while len(out) < 140:
        nm = BUILDER_FORMS[int(g.integers(0, len(BUILDER_FORMS)))] % BUILDER_STEMS[int(g.integers(0, len(BUILDER_STEMS)))]
        if nm not in used:
            used.add(nm); out.append(nm)
    return out


class Pack:
    def __init__(self, w: World, u: Utility):
        self.w, self.u = w, u
        self.idn = Identity(w)
        self.builders = builder_names()
        self._permits()

    # ------------------------------------------------------------------ permits
    def _permits(self):
        w, u, idn = self.w, self.u, self.idn
        g = C.stream("permits")
        L = w.L
        rows = []   # (issue date, kind, lot, applied, co, valuation, builder, desc)
        sf = np.where(~np.isnat(w.issued))[0]
        for i in sf:
            iss = C.to_date(w.issued[i]); co = C.to_date(w.co[i])
            if co is not None and co > C.RECORDS_END:
                co = None
            yr = iss.year
            val = int(round(g.normal(205000 + 9000 * (yr - 2008), 38000) / 100.0) * 100)
            rows.append([iss, "SFR", int(i), iss - dt.timedelta(days=int(g.integers(9, 75))), co, max(val, 120000),
                         int(u.builder[i]), "NEW SINGLE FAMILY RESIDENCE"])
        # other permits on standing homes: pools, re-roofs (hurricane years), screen enclosures, additions, solar
        done = np.where((w.yb0 > 0) | (w.co <= np.datetime64("2026-12-31")), np.where(w.yb0 > 0, w.yb0, w.co.astype("datetime64[Y]").astype(int) + 1970), 0)
        rate = {"POOL": 0.011, "ROOF": 0.009, "SCRN": 0.006, "ADDN": 0.002, "SOLR": 0.002}
        wave = {2017: 1.0, 2018: 3.2, 2019: 1.4, 2022: 1.2, 2023: 4.1, 2024: 2.0}
        homes = np.where(done > 0)[0]
        for y in range(2008, 2027):
            standing = homes[done[homes] < y]
            for kind, r in rate.items():
                rr = r * (wave.get(y, 1.0) if kind == "ROOF" else 1.0) * (0.6 + 0.4 * min(1.0, (y - 2007) / 8))
                hit = standing[g.random(len(standing)) < rr]
                for i in hit:
                    day = dt.date(y, 1, 1) + dt.timedelta(days=int(g.integers(0, 365)))
                    fin = day + dt.timedelta(days=int(g.integers(20, 120)))
                    val = {"POOL": 42000, "ROOF": 16000, "SCRN": 9000, "ADDN": 38000, "SOLR": 24000}[kind]
                    rows.append([day, kind, int(i), day - dt.timedelta(days=int(g.integers(3, 30))),
                                 fin if fin <= C.RECORDS_END else None, int(round(val * g.lognormal(0, 0.3), -2)),
                                 int(g.integers(12, 140)), {"POOL": "IN-GROUND POOL & SPA", "ROOF": "RE-ROOF SHINGLE",
                                                            "SCRN": "SCREEN ENCLOSURE", "ADDN": "RESIDENTIAL ADDITION",
                                                            "SOLR": "ROOF MOUNT PV SYSTEM"}[kind]])
        # permit numbers in issue order
        rows.sort(key=lambda r: (r[0], r[2], r[1]))
        seq_leg, seq_new = {}, {}
        for r in rows:
            y = r[0].year
            if y <= 2018:
                seq_leg[y] = seq_leg.get(y, 0) + int(g.integers(1, 4))
                r.append("B%02d-%05d" % (y % 100, seq_leg[y]))
            else:
                seq_new[y] = seq_new.get(y, 0) + int(g.integers(1, 3))
                r.append("BLD%d-%05d" % (y, seq_new[y]))
        self.permit_rows = rows
        # migrated: legacy permits still open at the 2019 cutover move to the new system under a new number
        cut = dt.date(2019, 1, 1)
        self.migrated = {}
        mseq = 0
        for r in rows:
            if r[0].year == 2018 and (r[4] is None or r[4] >= cut) and r[0] >= dt.date(2018, 4, 1):
                mseq += int(g.integers(1, 3))
                self.migrated[r[8]] = "BLD2019-M%04d" % mseq
        self.sf_permit_no = {r[2]: (self.migrated.get(r[8]) or r[8]) for r in rows if r[1] == "SFR"}

    def write_permits(self, out):
        idn = self.idn
        g = C.stream("permit_text")
        leg_rows, new_rows = [], []
        tl = {"SFR": "RES NEW SFR", "POOL": "RES POOL", "ROOF": "RES REROOF", "SCRN": "RES SCREEN ENCL",
              "ADDN": "RES ADDITION", "SOLR": "RES SOLAR PV"}
        wc = {"SFR": "Residential New Single Family", "POOL": "Pool / Spa", "ROOF": "Re-Roof", "SCRN": "Screen Enclosure",
              "ADDN": "Residential Addition", "SOLR": "Solar Photovoltaic"}
        cut = dt.date(2019, 1, 1)
        for (iss, kind, lot, applied, co, val, b, desc, num) in self.permit_rows:
            addr = idn.addr_uc[lot]
            if g.random() < 0.08:
                last = addr.rsplit(" ", 1)
                addr = last[0] + " " + SUFFIX_LONG.get(last[1].title(), last[1])
            bname = self.builders[b]
            if iss.year <= 2018:
                mig = num in self.migrated
                status = "MIGRATED" if mig else ("CO ISSUED" if (kind == "SFR" and co) else ("FINALED" if co else "EXPIRED"))
                leg_rows.append([num, C.mdy(applied), C.mdy(iss), addr, tl[kind], desc, val, bname.upper(), status,
                                 "" if mig else C.mdy(co)])
            if iss.year >= 2019 or num in self.migrated:
                pn = self.migrated.get(num, num)
                status = ("Finaled" if co else ("Issued" if (C.RECORDS_END - iss).days < 180 else "Inspections"))
                new_rows.append([pn, num if num in self.migrated else "", idn.strap[lot], idn.addr[lot], "Building",
                                 wc[kind], desc.title(), applied, iss, iss + dt.timedelta(days=365), status, val, bname,
                                 co if kind == "SFR" else None, co if kind != "SFR" else None])
        n1 = C.write_csv(os.path.join(out, C.F_PLEG),
                         ["PERMIT_NBR", "APPLIED_DT", "ISSUE_DT", "SITE_ADDR", "PERMIT_TYPE", "DESCRIPTION", "VALUATION",
                          "CONTRACTOR", "STATUS", "FINAL_DT"], leg_rows)
        new_rows.sort(key=lambda r: (r[8], r[0]))
        import xlsx_writer as XW
        n2 = XW.write_table(os.path.join(out, C.F_PNEW), "Permits",
                            ["Permit Number", "Legacy Permit #", "Parcel ID", "Address", "Permit Type", "Work Class",
                             "Description", "Applied Date", "Issued Date", "Expiration Date", "Status", "Valuation",
                             "Contractor", "CO Issued", "Final Date"], new_rows,
                            widths=[16, 13, 24, 26, 10, 28, 30, 12, 12, 14, 12, 11, 34, 12, 12],
                            title=None)
        return n1, n2

    # ------------------------------------------------------------------ roll
    def write_roll(self, out):
        w, idn = self.w, self.idn
        g = C.stream("roll")
        L = w.L
        jan26 = np.datetime64("2026-01-01")
        on_roll = (w.yb0 > 0) | (w.co < jan26)
        yb = np.where(w.yb0 > 0, w.yb0, np.where(w.co < jan26, w.co.astype("datetime64[Y]").astype(int) + 1970, 0))
        rows = []
        area = L["area"]
        for i in np.argsort(idn.strap, kind="stable"):
            ai = int(area[i])
            canal = bool(L["canal"][i])
            land = int(round((9000 + 2600 * (ai < 16) + 1500 * (ai == 0)) * (2.6 if canal else 1.0) * g.lognormal(0, 0.18), -2))
            sf = int(g.choice([10000, 10000, 10000, 10000, 11250, 12500, 9600]))
            if on_roll[i]:
                living = int(round(g.normal(1650 + 14 * max(yb[i] - 1975, 0), 280), -1))
                bldg = int(round(living * (118 + 2.2 * max(yb[i] - 1975, 0)) * g.lognormal(0, 0.12), -2))
                rows.append([idn.strap[i], idn.addr_uc[i], idn.legal[i], "0100", "SINGLE FAMILY RESIDENTIAL", "R1",
                             sf, "Y" if canal else "", int(yb[i]), living, land + bldg,
                             "FL" if g.random() < 0.78 else str(g.choice(["NY", "OH", "MI", "IL", "NJ", "PA", "MA", "ON", "QC"])), 2026])
            else:
                rows.append([idn.strap[i], idn.addr_uc[i], idn.legal[i], "0000", "VACANT RESIDENTIAL", "R1", sf,
                             "Y" if canal else "", "", "", land,
                             "FL" if g.random() < 0.44 else str(g.choice(["NY", "OH", "MI", "IL", "NJ", "PA", "MA", "ON", "QC", "DE", "XX"])), 2026])
        return C.write_csv(os.path.join(out, C.F_ROLL),
                           ["STRAP", "SITE_ADDR", "LEGAL_DESC", "DOR_CD", "DOR_DESC", "ZONING", "LAND_SF", "WATERFRONT",
                            "YR_BUILT", "LIVING_SF", "JUST_VALUE", "OWNER_STATE", "ROLL_YR"], rows)

    def write_plat(self, out):
        w = self.w
        recs = plat_records(w)
        rows = []
        for u in sorted(w.unit_no):
            sel = w.L["unit"] == u
            blks = w.L["block"][sel]
            bk, pg, rec = recs[u]
            rows.append([u, "PORT ARDELL UNIT %d" % u, bk, pg, C.iso(rec), int(blks.min()) + 1, int(blks.max()) + 1,
                         int(sel.sum())])
        return C.write_csv(os.path.join(out, C.F_PLAT), ["UNIT", "PLAT_NAME", "PLAT_BOOK", "PAGE", "RECORDED", "BLOCK_FROM",
                                                          "BLOCK_TO", "LOTS"], rows)

    # ------------------------------------------------------------------ utility extracts
    def premise_ids(self):
        if hasattr(self, "_pid"):
            return self._pid
        w, u = self.w, self.u
        g = C.stream("premise")
        idx = np.where(u.has_premise)[0]
        order = idx[np.lexsort((self.idn.strap[idx], u.created[idx]))]
        pid = {}
        k = 1003000
        for i in order:
            k += int(g.integers(1, 6))
            pid[int(i)] = "%07d" % k
        self._pid = pid
        return pid

    def write_premises(self, out):
        w, u, idn = self.w, self.u, self.idn
        g = C.stream("premise_rows")
        pid = self.premise_ids()
        rows = []
        for i, p in sorted(pid.items(), key=lambda kv: kv[1]):
            cr = C.to_date(u.created[i])
            parcel = idn.strap[i] if cr >= dt.date(1998, 1, 1) else ""
            phase = u.phase_stored[i]
            ph = "00" if phase == "Core" else "%02d" % int(phase)
            active = not np.isnat(u.meter_set[i]) and C.to_date(u.meter_set[i]) <= C.RECORDS_END
            rows.append([p, idn.addr_uc[i], parcel, ph, C.iso(cr), "RES-SF", "ACTIVE" if active else "STUB"])
        return C.write_csv(os.path.join(out, C.F_PREM), ["PREMISE_ID", "SVC_ADDR", "PARCEL_ID", "UEP_PHASE", "CREATED_DT",
                                                          "PREMISE_TYPE", "STATUS"], rows)

    def write_accounts(self, out):
        u = self.u
        g = C.stream("accounts")
        pid = self.premise_ids()
        rows = []
        acc = sorted(u.accounts, key=lambda r: (r[1], pid[r[0]]))
        k = 4400000
        for (i, s, e) in acc:
            k += int(g.integers(1, 4))
            rows.append(["%08d" % k, pid[i], C.iso(C.to_date(s)), C.iso(C.to_date(e)) if e is not None else "",
                         "RES1", "%02d" % (1 + int(g.integers(0, 20)))])
        return C.write_csv(os.path.join(out, C.F_ACCT), ["ACCOUNT_NO", "PREMISE_ID", "SVC_START", "SVC_STOP", "RATE_CLASS",
                                                          "BILL_CYCLE"], rows)

    def install_rows(self):
        w, u = self.w, self.u
        g = C.stream("ami")
        pid = self.premise_ids()
        lo, hi = np.datetime64("2024-10-01"), np.datetime64("2026-10-01")
        ev = []
        new = np.where(u.has_premise & ~np.isnat(u.meter_set) & (u.meter_set >= lo) & (u.meter_set < hi) & (w.yb0 == 0))[0]
        for i in new:
            ev.append((C.to_date(u.meter_set[i]), int(i), "new"))
        for i, day in zip(*u.changeouts):
            ev.append((C.to_date(day), int(i), "exch"))
        for i, day in zip(*u.resets):
            ev.append((C.to_date(day), int(i), "reset"))
        ev.sort(key=lambda r: (r[0], pid[r[1]]))
        rows = []
        ser = 25030000
        eid = 81100000
        for (day, i, kind) in ev:
            ser += int(g.integers(1, 40)); eid += int(g.integers(1, 30))
            hh = int(g.integers(7, 16)); mm = int(g.integers(0, 60))
            if kind == "exch":
                size = "5/8X3/4" if g.random() < 0.83 else "1"
            else:
                size = "1" if u.size1[i] else "5/8X3/4"
            rows.append(["%d" % eid, "%dA" % ser, pid[i], C.iso(day), "%02d:%02d" % (hh, mm), size,
                         "C%02d" % int(g.integers(1, 15))])
        self.ami_events = ev
        return rows

    def write_ami(self, out):
        rows = self.install_rows()
        return C.write_csv(os.path.join(out, C.F_AMI), ["ENDPOINT_ID", "METER_SERIAL", "PREMISE_ID", "INSTALL_DATE",
                                                         "INSTALL_TIME", "METER_SIZE", "CREW"], rows)

    def receipt_rows(self):
        u = self.u
        rows = []
        for (rno, rdate, lot, amt, total, nlines, drawer) in u.receipts:
            d = C.to_date(rdate)
            fy, q = C.fq(d)
            if fy != 2026:
                continue
            pn = self.sf_permit_no[lot]
            rows.append([rno, d, self.builders[int(u.builder[lot])], pn, "CAPWS", total,
                         ["CHECK", "ACH", "CARD", "CHECK", "ACH"][(int(rno[-3:]) + lot) % 5]])
        rows.sort(key=lambda r: (r[1], r[0], r[3]))
        return rows

    def write_fees(self, out):
        import xlsx_writer as XW
        rows = self.receipt_rows()
        return XW.write_table(os.path.join(out, C.F_FEES), "Receipts FY2026",
                              ["Receipt No", "Receipt Date", "Payer", "Permit No", "Fee Code", "Amount", "Tender"],
                              rows, widths=[12, 12, 34, 16, 9, 12, 8], title=None, money_cols=[5])

    # ------------------------------------------------------------------ distractors
    def write_acs(self, out):
        g = C.stream("acs")
        rows = []
        w = self.w
        for t in range(1, 33):
            hu = int(g.integers(1800, 4200)); occ = hu - int(hu * g.uniform(0.09, 0.27))
            rows.append(["12139%06d" % (100100 + 100 * t + int(g.integers(0, 3))), hu, int(hu * 0.04 * g.uniform(0.6, 1.4)), occ,
                         hu - occ, int(g.integers(1979, 2009)), round(g.uniform(2.05, 2.75), 2), int(g.integers(88, 210)) * 1000 + 500])
        return C.write_csv(os.path.join(out, C.F_ACS), ["GEOID", "HU_EST", "HU_MOE", "OCC_HU_EST", "VAC_HU_EST",
                                                         "MED_YR_BUILT", "AVG_HH_SIZE", "MED_VALUE"], rows)

    def write_sar(self, out):
        u, idn, w = self.u, self.idn, self.w
        g = C.stream("sar")
        rows = []
        for i in np.argsort(idn.strap, kind="stable"):
            ai = int(w.L["area"][i])
            if ai == 0 or w.area_acc[ai] is None or w.area_acc[ai] > dt.date(2026, 12, 31):
                continue
            acc = w.area_acc[ai]
            amt = int(round(14800 + 620 * (acc.year - 2010), -1))
            paid_off = g.random() < 0.18 + 0.03 * (2026 - acc.year)
            yrs = 2026 - acc.year
            bal = 0 if paid_off else max(0, int(round(amt * (1 - yrs / 20.0) * g.uniform(0.97, 1.0), -1)))
            rows.append([idn.strap[i], AREAS[ai][0].upper(), acc.year, amt, bal, "PAID" if paid_off else "INSTALLMENT"])
        return C.write_csv(os.path.join(out, C.F_SAR), ["STRAP", "ASSESSMENT_AREA", "LEVY_YR", "ASSESSMENT_AMT",
                                                         "BALANCE_20261231", "STATUS"], rows)
