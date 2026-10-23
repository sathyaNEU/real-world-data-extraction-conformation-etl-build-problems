"""task176 pack writers for the licensing side: the licence extract, the 2019 number crosswalk, the capacity
worksheet children, the start-up grant awards and the county lookup. Every row is written from the world in
world.py; the mess is the licensing system's own (two numbering schemes, two code sets and two date formats
either side of the 2019 migration, children repeated at every renewal, newborns arriving at the next
worksheet)."""
from __future__ import annotations

import datetime as dt

import common as C
import world as W

CLOSE_REASONS = {
    "K": (("Voluntary - provider request", 0.58), ("Voluntary - other employment", 0.27),
          ("Voluntary - moved out of area", 0.09), ("Non-renewal", 0.06)),
    "RETIRE": (("Retired", 0.62), ("Voluntary - provider request", 0.22), ("Health", 0.11), ("Non-renewal", 0.05)),
    "BASE": (("Voluntary - provider request", 0.46), ("Voluntary - other employment", 0.16),
             ("Voluntary - moved out of area", 0.10), ("Non-renewal", 0.12), ("Insufficient enrollment", 0.08),
             ("Revoked", 0.04), ("Health", 0.04)),
}
REL_LEGACY = {"OWN": "OWN CHILD", "GRANDCHILD": "GRANDCHILD", "FOSTER": "FOSTER", "RELATIVE": "OTHER REL"}
REL_NEW = {"OWN": "C", "GRANDCHILD": "GC", "FOSTER": "FC", "RELATIVE": "R"}


class Identity:
    """licence numbers: a current number for every home in the extract, a legacy number for every home licensed
    before the migration, provider ids, zip codes"""

    def __init__(self, homes):
        r = C.stream("identity")
        self.cur, self.leg, self.prov, self.zip = {}, {}, {}, {}
        used = set()
        seqs = {}
        for h in sorted(homes, key=lambda x: (x.lic, x.hid)):
            while True:
                n = "FC%06d" % int(r.integers(100000, 999999))
                if n not in used:
                    used.add(n)
                    break
            self.cur[h.hid] = n
            if h.lic < C.MIGRATION:
                c = h.county[2:]
                seqs[c] = seqs.get(c, 1200 + int(r.integers(0, 400))) + int(r.integers(1, 4))
                self.leg[h.hid] = "F%s-%05d" % (c, seqs[c])
            while True:
                pv = "P%07d" % int(r.integers(1000000, 9999999))
                if pv not in used:
                    used.add(pv)
                    break
            self.prov[h.hid] = pv
            self.zip[h.hid] = "%05d" % (int(h.county[2:]) * 70 + 49000 + int(r.integers(0, 60)))


def in_extract(h):
    return h.close is None or h.close >= C.EXTRACT_FROM


def ref_on(ident, h, d):
    """the licence number a record dated d carries"""
    if d < C.MIGRATION and h.hid in ident.leg:
        return ident.leg[h.hid]
    return ident.cur[h.hid]


def licence_rows(homes, ident):
    r = C.stream("licence_rows")
    rows = []
    for h in sorted((h for h in homes if in_extract(h)), key=lambda x: (x.lic, x.hid)):
        status = "ACTIVE" if h.close is None else "CLOSED"
        reason = ""
        if h.close is not None:
            opts = CLOSE_REASONS[h.cause]
            u, acc = r.random(), 0.0
            for name, w in opts:
                acc += w
                if u <= acc:
                    reason = name
                    break
            reason = reason or opts[-1][0]
        # last renewal: the latest anniversary before the end of the record or the closure
        stop = h.close or C.RECORD_END
        lr = h.lic
        y = h.lic.year + 1
        while True:
            try:
                a = dt.date(y, h.lic.month, h.lic.day)
            except ValueError:
                a = dt.date(y, h.lic.month, 28)
            if a > stop:
                break
            lr = a
            y += 1
        by = h.pbirth.year
        by_s = "" if (h.lic < dt.date(2009, 1, 1) and r.random() < 0.11) else str(by)
        cty = C.COUNTY_NAME[h.county].upper()
        rows.append((ident.cur[h.hid], h.ltype, status, cty, ident.zip[h.hid], h.cap, h.lic.isoformat(),
                     h.close.isoformat() if h.close else "", reason, ident.prov[h.hid], by_s, lr.isoformat()))
    return rows


LIC_HEAD = ("licence_no", "licence_type", "status", "county", "zip", "licensed_capacity", "first_licensed_date",
            "closure_effective_date", "closure_reason", "provider_id", "provider_birth_year", "last_renewal_date")


def write_licences(path, homes, ident):
    return C.write_csv(path, LIC_HEAD, licence_rows(homes, ident))


def write_crosswalk(path, homes, ident):
    rows = []
    for h in sorted((h for h in homes if in_extract(h) and h.hid in ident.leg), key=lambda x: ident.leg[x.hid]):
        rows.append((ident.leg[h.hid], ident.cur[h.hid], C.MIGRATION.isoformat() if (h.close is None or h.close >= C.MIGRATION) else "archived"))
    return C.write_csv(path, ("legacy_licence_no", "licence_no", "migrated"), rows)


def anniversaries(h, start, stop):
    out = []
    y = h.lic.year + 1
    while True:
        try:
            a = dt.date(y, h.lic.month, h.lic.day)
        except ValueError:
            a = dt.date(y, h.lic.month, 28)
        if a > stop:
            break
        if a >= start:
            out.append(a)
        y += 1
    return out


def counted(h, d):
    """the children who count toward capacity on worksheet date d"""
    out = []
    for k in h.kids:
        if k["birth"] > d:
            continue
        age = (d - k["birth"]).days / 365.25
        if age >= 13:
            continue
        if k["rel"] == "OWN":
            out.append(k)
        elif k["start"] <= d and (k["end"] is None or d <= k["end"]):
            if k["rel"] == "GRANDCHILD" and age >= 6:
                continue
            out.append(k)
    out.sort(key=lambda k: k["birth"])
    return out


def worksheet_rows(homes, ident):
    r = C.stream("worksheets")
    rows = []
    for h in homes:
        if not in_extract(h):
            continue
        stop = min(h.close or C.RECORD_END, C.RECORD_END)
        dates = []
        if h.lic >= C.EXTRACT_FROM:
            dates.append((h.lic, "INITIAL"))
        dates += [(a, "RENEWAL") for a in anniversaries(h, C.EXTRACT_FROM, stop)]
        # an amendment after some births (a capacity change filed within two months)
        for k in h.kids:
            if k["rel"] == "OWN" and k["birth"] > h.lic and C.EXTRACT_FROM <= k["birth"] <= stop and r.random() < 0.3:
                d = k["birth"] + dt.timedelta(days=int(r.integers(10, 60)))
                if d <= stop:
                    dates.append((d, "AMENDMENT"))
        dates.sort()
        for d, kind in dates:
            kids = counted(h, d)
            legacy = d < C.MIGRATION
            for i, k in enumerate(kids, 1):
                if legacy:
                    bd = "%d/%d/%d" % (k["birth"].month, k["birth"].day, k["birth"].year)
                    rel = REL_LEGACY[k["rel"]]
                else:
                    bd = k["birth"].isoformat()
                    rel = REL_NEW[k["rel"]]
                lives = "Y" if k["rel"] in ("OWN", "FOSTER") else ("Y" if r.random() < 0.15 else "N")
                rows.append((ref_on(ident, h, d), d.isoformat(), kind, i, k["ini"], bd, rel, lives))
    rows.sort(key=lambda x: (x[1], x[0], x[3]))
    return rows


WS_HEAD = ("licence_ref", "worksheet_date", "worksheet_type", "line", "child_initials", "child_birth_date",
           "relationship", "lives_in_home")


def write_worksheets(path, homes, ident):
    return C.write_csv(path, WS_HEAD, worksheet_rows(homes, ident))


def write_lookup(path):
    rows = [(c[0], C.COUNTY_NAME[c[0]] + " County", c[2], C.REGIONS[c[2]]) for c in C.COUNTIES]
    return C.write_csv(path, ("county_fips", "county_name", "region_no", "region_name"), rows)


def grant_rows(homes, ident):
    r = C.stream("grants")
    rows = []
    n = 0
    for h in sorted((h for h in homes if h.grant), key=lambda x: (x.lic, x.hid)):
        n += 1
        award = h.lic + dt.timedelta(days=int(r.integers(5, 40)))
        p1 = award + dt.timedelta(days=int(r.integers(7, 21)))
        six = h.lic + dt.timedelta(days=183)
        p2d = ""
        p2 = ""
        if h.close is None or h.close > six:
            p2d = (six + dt.timedelta(days=int(r.integers(10, 45)))).isoformat()
            p2 = 3000
        rec, recd = "", ""
        if h.close is not None and h.close < h.lic + dt.timedelta(days=365):
            rec = 3000 if p2 == "" else 4500
            recd = (h.close + dt.timedelta(days=int(r.integers(30, 120)))).isoformat()
        rows.append(("SUG-23-%04d" % n, ident.cur[h.hid], C.COUNTY_NAME[h.county], award.isoformat(), 6000,
                     p1.isoformat(), 3000, p2d, p2, recd, rec))
    return rows


GRANT_HEAD = ("award_no", "licence_no", "county", "award_date", "award_amount", "first_payment_date",
              "first_payment", "second_payment_date", "second_payment", "recovery_date", "recovery_amount")
