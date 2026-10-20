"""Everything the pack and the golden are cut from, computed once, and the CSV and text writers. Documents and
workbooks are in docs.py."""
import csv
import datetime as dt

import acs as A
import asks as K
import geo as G
import methods as M
import world as W

SUMLEV_TRACT, SUMLEV_BG = "1400000US", "1500000US"


def everything():
    ts = G.tracts()
    blks = G.blocks(ts)
    bge = A.bg_estimates(ts)
    tre = A.tract_estimates(ts, bge)
    place_estimates(ts, bge, tre)
    ps = K.parcels(ts, blks)
    cs = K.cases(ps)
    K.reopen(cs)
    place_days(cs)
    js = K.journal(ps)
    x = dict(ts=ts, blks=blks, bge=bge, tre=tre, parcels=ps, cases=cs, journal=js)
    x["fig"] = figures(x)
    return x


def _edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def place_estimates(ts, bge, tre, floor=0.004):
    """Each graded rate and margin sits clear of its one-decimal edge: where one does not, a block group's estimate
    under it moves by one person (its tract's sum with it) or the margin it is read from by one."""
    for _ in range(300):
        bad = None
        for t in ts:
            if not t.nbhd or bad:
                continue
            split = len(t.children) > 1
            for code, bgs in t.children:
                cur = tre[(2, code)]
                figs = [("cur", M.proportion(cur.x, cur.mx, cur.u, cur.mu), [bge[(2, b.geoid20)] for b in bgs], cur)]
                if split:
                    figs.append(("bg", M.proportion(*M.summed([bge[(1, b.geoid10)] for b in bgs])),
                                 [bge[(1, b.geoid10)] for b in bgs], tre[(1, t.code10)]))
                else:
                    p = tre[(1, t.code10)]
                    figs.append(("par", M.proportion(p.x, p.mx, p.u, p.mu), [bge[(1, b.geoid10)] for b in t.bgs], p))
                for kind, (r, m), ests, tract in figs:
                    if _edge(100 * r, 0.1) < floor:
                        bad = ("x", kind, ests, tract)
                    elif _edge(100 * m, 0.1) < floor:
                        bad = ("m", kind, ests, tract)
                    if bad:
                        break
                if bad:
                    break
        if not bad:
            return
        what, kind, ests, tract = bad
        if what == "x":
            ests[0].x += 1
            tract.x += 1
        elif kind == "bg":
            ests[0].mx += 1
        else:
            tract.mx += 1
    raise RuntimeError("estimates not placed")


def place_days(cs, floor=0.08):
    """Each neighbourhood's average days open sits clear of a half day: where it does not, one of its open cases
    opened a day earlier."""
    for _ in range(100):
        a = K.ask_a(cs)
        bad = [nb for nb, (n, d) in a.items() if _edge(d, 1.0) < floor]
        if not bad:
            return
        nb = bad[0]
        c = next(c for c in cs if c.parcel.nbhd == nb and c.ctype == "HOUSING" and c.parcel.use in K.RES and
                 K.open_on(c, K.END))
        c.opened = c.opened - dt.timedelta(days=1)
        c.events[0] = (c.opened, c.events[0][1])
    raise RuntimeError("days not placed")


def tract_rows(x):
    """Each candidate 2020 tract: neighbourhood, code, both periods' rate and margin, z and verdict (golden)."""
    rows = []
    for t in x["ts"]:
        if not t.nbhd:
            continue
        for code, bgs in t.children:
            cur = x["tre"][(2, code)]
            c = M.proportion(cur.x, cur.mx, cur.u, cur.mu)
            if len(t.children) > 1:
                e = M.proportion(*M.summed([x["bge"][(1, b.geoid10)] for b in bgs]))
            else:
                p = x["tre"][(1, t.code10)]
                e = M.proportion(p.x, p.mx, p.u, p.mu)
            zz = M.z(*e, *c)
            rows.append(dict(nbhd=t.nbhd, tract=code, geoid=G.PREFIX + code.replace(".", ""), split=len(t.children) > 1,
                             parent=t.code10, r18=e[0], m18=e[1], r23=c[0], m23=c[1], z=zz,
                             rise=zz > M.Z, high=c[0] >= W.THRESHOLD, qual=zz > M.Z and c[0] >= W.THRESHOLD))
    return rows


def figures(x):
    rows = tract_rows(x)
    n = {nb: sum(1 for r in rows if r["nbhd"] == nb and r["qual"]) for nb in W.NEIGHBOURHOODS}
    des = [nb for nb in W.NEIGHBOURHOODS if n[nb] >= W.MIN_TRACTS]
    return dict(rows=rows, count=n, designated=des, ask_a=K.ask_a(x["cases"]), ask_b=K.ask_b(x["journal"]))


def write_csv(path, cols, rows, crlf=False, extra_header=None, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=delim, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        if extra_header:
            w.writerow(extra_header)
        for r in rows:
            w.writerow(r)
    return len(rows)


# ------------------------------------------------------------------------------------------------- the Bureau
def acs_tract(x, period):
    """B17001 for every tract in the county, the layout of the release: 2014-18 labels without colons, 2019-23 with
    colons and semicolons in the names."""
    ests = sorted(((code, e) for (p, code), e in x["tre"].items() if p == period), key=lambda t: t[0])
    cols = ["GEO_ID", "NAME", "B17001_001E", "B17001_001M", "B17001_002E", "B17001_002M"]
    if period == 1:
        lab = ["id", "Geographic Area Name", "Estimate!!Total", "Margin of Error!!Total",
               "Estimate!!Total!!Income in the past 12 months below poverty level",
               "Margin of Error!!Total!!Income in the past 12 months below poverty level"]
        name = lambda c: "Census Tract %s, %s" % (tract_name(c), W.COUNTY)
    else:
        lab = ["Geography", "Geographic Area Name", "Estimate!!Total:", "Margin of Error!!Total:",
               "Estimate!!Total:!!Income in the past 12 months below poverty level:",
               "Margin of Error!!Total:!!Income in the past 12 months below poverty level:"]
        name = lambda c: "Census Tract %s; %s" % (tract_name(c), W.COUNTY)
    rows = [[SUMLEV_TRACT + G.PREFIX + c.replace(".", ""), name(c), e.u, e.mu, e.x, e.mx] for c, e in ests]
    return cols, lab, rows


def tract_name(code):
    a, b = code.split(".")
    return str(int(a)) if b == "00" else "%d.%s" % (int(a), b)


def acs_bg(x, period):
    """B17021 for every block group (its total is the poverty universe; line 2 is below poverty)."""
    cols = ["GEO_ID", "NAME", "B17021_001E", "B17021_001M", "B17021_002E", "B17021_002M"]
    if period == 1:
        lab = ["id", "Geographic Area Name", "Estimate!!Total", "Margin of Error!!Total",
               "Estimate!!Total!!Income in the past 12 months below poverty level",
               "Margin of Error!!Total!!Income in the past 12 months below poverty level"]
    else:
        lab = ["Geography", "Geographic Area Name", "Estimate!!Total:", "Margin of Error!!Total:",
               "Estimate!!Total:!!Income in the past 12 months below poverty level:",
               "Margin of Error!!Total:!!Income in the past 12 months below poverty level:"]
    rows = []
    for t in sorted(x["ts"], key=lambda t: t.code10):
        for b in t.bgs:
            gid = b.geoid10 if period == 1 else b.geoid20
            tr = b.tract10 if period == 1 else b.tract20
            num = b.num if period == 1 else b.num20
            e = x["bge"][(period, gid)]
            sep = ", " if period == 1 else "; "
            rows.append([SUMLEV_BG + gid, sep.join(["Block Group %d" % num, "Census Tract %s" % tract_name(tr),
                                                     W.COUNTY]), e.u, e.mu, e.x, e.mx])
    rows.sort(key=lambda r: r[0])
    return cols, lab, rows


TRACTREL_COLS = ["OID_TRACT_20", "GEOID_TRACT_20", "NAMELSAD_TRACT_20", "AREALAND_TRACT_20", "AREAWATER_TRACT_20",
                 "MTFCC_TRACT_20", "FUNCSTAT_TRACT_20", "OID_TRACT_10", "GEOID_TRACT_10", "NAMELSAD_TRACT_10",
                 "AREALAND_TRACT_10", "AREAWATER_TRACT_10", "MTFCC_TRACT_10", "FUNCSTAT_TRACT_10", "AREALAND_PART",
                 "AREAWATER_PART"]


def tractrel_rows(x):
    land10, water10, land20, water20, part = {}, {}, {}, {}, {}
    for blk in x["blks"]:
        t10 = blk.bg.tract10
        land10[t10] = land10.get(t10, 0) + blk.land
        water10[t10] = water10.get(t10, 0) + blk.water
        for g20, l, w in blk.parts:
            t20 = g20[5:9] + "." + g20[9:11]
            land20[t20] = land20.get(t20, 0) + l
            water20[t20] = water20.get(t20, 0) + w
            k = (t20, t10)
            a, b = part.get(k, (0, 0))
            part[k] = (a + l, b + w)
    rows = []
    for (t20, t10), (l, w) in sorted(part.items()):
        oid20 = 20790000000000 + int(t20.replace(".", "")) * 7
        oid10 = 20790000000000 - int(t10.replace(".", "")) * 11
        rows.append([oid20, G.PREFIX + t20.replace(".", ""), "Census Tract %s" % tract_name(t20), land20[t20],
                     water20[t20], "G5020", "S", oid10, G.PREFIX + t10.replace(".", ""),
                     "Census Tract %s" % tract_name(t10), land10[t10], water10[t10], "G5020", "S", l, w])
    return rows


BLOCKREL_COLS = ["STATE_2010", "COUNTY_2010", "TRACT_2010", "BLK_2010", "BLKSF_2010", "AREALAND_2010",
                 "AREAWATER_2010", "BLOCK_PART_FLAG_O", "STATE_2020", "COUNTY_2020", "TRACT_2020", "BLK_2020",
                 "BLKSF_2020", "AREALAND_2020", "AREAWATER_2020", "BLOCK_PART_FLAG_R", "AREALAND_INT",
                 "AREAWATER_INT"]


def blockrel_rows(x):
    land20, water20, n20 = {}, {}, {}
    for blk in x["blks"]:
        for g20, l, w in blk.parts:
            land20[g20] = land20.get(g20, 0) + l
            water20[g20] = water20.get(g20, 0) + w
            n20[g20] = n20.get(g20, 0) + 1
    rows = []
    for blk in x["blks"]:
        for g20, l, w in blk.parts:
            rows.append([W.STATE_FIPS, W.COUNTY_FIPS, blk.bg.tract10.replace(".", ""), blk.code10, "",
                         blk.land, blk.water, "p" if len(blk.parts) > 1 else "", W.STATE_FIPS, W.COUNTY_FIPS,
                         g20[5:11], g20[11:], "", land20[g20], water20[g20], "p" if n20[g20] > 1 else "", l, w])
    rows.sort(key=lambda r: (r[2], r[3], r[10], r[11]))
    return rows


def pl2010_rows(x):
    cols = ["GEO_ID", "NAME", "P1_001N"]
    lab = ["Geography", "Geographic Area Name", " !!Total:"]
    rows = []
    for blk in x["blks"]:
        rows.append(["1000000US" + blk.geoid10, "Block %s; Block Group %d; Census Tract %s; %s" % (
            blk.code10, blk.bg.num, tract_name(blk.bg.tract10), W.COUNTY), blk.pop10])
    rows.sort(key=lambda r: r[0])
    return cols, lab, rows


# ------------------------------------------------------------------------------------------------- the city
PARCEL_COLS = ["parcel_id", "prior_parcel_id", "situs_address", "land_use_code", "land_use_desc", "census_block_2020"]


def parcel_rows(x):
    rows = []
    for p in x["parcels"]:
        desc = K.RES.get(p.use) or K.OTHER.get(p.use)
        rows.append([p.pid, p.old, p.addr.upper(), p.use, desc, p.block])
    rows.sort(key=lambda r: r[0])
    return rows


CASE_COLS = ["case_number", "parcel_number", "address", "case_type", "status", "opened_date", "closed_date",
             "inspector"]
EVENT_COLS = ["case_number", "event_date", "event", "entered_by"]


def case_rows(x):
    rows, ev = [], []
    for c in x["cases"]:
        status, closed = K.header(c)
        pn = c.parcel.old if c.opened < K.REKEY else c.parcel.pid
        rows.append([c.no, pn, c.parcel.addr.upper(), c.ctype, status, c.opened.strftime("%m/%d/%Y"),
                     closed.strftime("%m/%d/%Y") if closed else "", c.inspector])
        for d, e in c.events:
            ev.append([c.no, d.isoformat(), e, c.inspector])
    ev.sort(key=lambda r: (r[1], r[0]))
    return rows, ev


def journal_rows(x):
    """Per fiscal year (July to June): entry, posting date, grant, parcel, payee, check, amount, reference, memo."""
    by = {}
    for e in x["journal"]:
        fy = e.date.year + (1 if e.date.month >= 7 else 0)
        pn = e.parcel.old if e.date < K.REKEY else e.parcel.pid
        by.setdefault(fy, []).append([e.no, e.date, e.grant, pn, e.payee, e.check, e.amount, e.ref or None, e.desc])
    return by
