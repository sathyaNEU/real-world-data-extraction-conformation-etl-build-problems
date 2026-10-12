"""The county recorders' documents and the vendor's purchase-money file. Every closing's deed and mortgage, the
quitclaim refinances, the seller-carried notes and the re-recordings are numbered in their county's series day by
day among the office's other documents; the vendor's file holds the mortgages it paired with a conveyance."""
import datetime as dt

import numpy as np
import pandas as pd

import sim as S
import world as W

REMARKS = ["RE-RECORDED TO CORRECT LEGAL DESCRIPTION", "RERECORDED - CORRECTED LEGAL DESC", "RE-RECORDED TO ATTACH RIDER",
           "RE-RECORDED TO CORRECT VESTING", "RE-RECORD: SCRIVENER ERROR"]
MERS = ["MORTGAGE ELECTRONIC REGISTRATION SYSTEMS INC AS NOMINEE FOR {n}",
        "MERS AS NOMINEE FOR {n} ITS SUCCESSORS AND ASSIGNS",
        "MORTGAGE ELECTRONIC REGISTRATION SYSTEMS, INC., AS NOMINEE FOR {n}"]


def strings(x):
    """The ways a lender's name is indexed as mortgagee, with weights: as written, without punctuation, with
    'THE', city suffixes, abbreviations, and MERS nominee phrasing for the lenders that register with MERS."""
    up = x["name"].upper()
    bare = up.replace(",", "").replace(".", "")
    own = [(bare, 0.55), (up, 0.25)]
    if x["ch"] == "CB" or x["ch"] == "RB":
        own.append(("THE " + bare, 0.08))
        if x["hq"][1] == "KS":
            own.append(("%s %s KS" % (bare, x["hq"][0].upper()), 0.07))
        else:
            own.append((bare.replace(" NA", " N A").replace(" BANK", " BK"), 0.07))
    if x["ch"] == "CU":
        own.append((bare.replace("FEDERAL CREDIT UNION", "FCU").replace("CREDIT UNION", "CU"), 0.12))
    if x["ch"] == "NB":
        own.append((bare.replace(" LLC", "").replace(" INC", "").replace(" CORPORATION", " CORP")
                    .replace(" COMPANY", " CO"), 0.12))
    own = [(s[:80], w) for s, w in own]
    out = []
    for s, w in own:
        out.append((s, w * (1 - x["mers"])))
    if x["mers"]:
        for k, t in enumerate(MERS):
            out.append((t.format(n=bare if k != 2 else up)[:80], x["mers"] * (0.5, 0.3, 0.2)[k]))
    agg = {}
    for s, w in out:
        if w > 0:
            agg[s] = agg.get(s, 0.0) + w
    tot = sum(agg.values())
    return [(s, w / tot) for s, w in agg.items()]


def deed_type(rng, seller):
    u = rng.random()
    if u < 0.74:
        return "WD", seller
    if u < 0.80:
        return "JTWD", seller
    if u < 0.87:
        return "SWD", rng.choice(["FEDERAL NATIONAL MORTGAGE ASSOCIATION", "SECRETARY OF HOUSING AND URBAN DEVELOPMENT",
                                  "%s HOMES LLC" % seller.split()[0], "%s PROPERTIES LLC" % seller.split()[0],
                                  "%s CONSTRUCTION INC" % seller.split()[0]])
    if u < 0.93:
        return "TRD", rng.choice(["%s FAMILY TRUST" % seller.split()[0], "%s REVOCABLE TRUST" % seller.split()[0],
                                  "%s %s TRUSTEE" % (seller.split()[0], " ".join(seller.split()[1:3]))])
    return "EXD", "ESTATE OF %s %s" % (seller.split()[0], seller.split()[1])


def consideration(rng, kind):
    u = rng.random()
    if kind == "QCD":
        return "" if u < 0.6 else ("0.00" if u < 0.85 else "1.00")
    return "" if u < 0.7 else ("10.00" if u < 0.9 else ("1.00" if u < 0.96 else "0.00"))


def parcel(rng, county, rural):
    apn = "%03d-%03d-%02d-0-%02d-%02d-%03d.00-0" % (W.KSNO[county], int(rng.integers(1, 200)), int(rng.integers(1, 37)),
                                                     int(rng.choice([10, 20, 30, 40])), int(rng.integers(1, 9)),
                                                     int(rng.integers(1, 60)))
    legal = "%s %d-%d-%dW" % (rng.choice(["NE4", "NW4", "SE4", "SW4", "S2", "N2", "E2", "W2"]), int(rng.integers(1, 37)),
                              int(rng.integers(12, 21)), int(rng.integers(1, 11)))
    return apn, legal


def build(w):
    """Every recorded document as one row: (doc key, county, recording date, package), with each package's documents
    numbered consecutively; then the vendor's file."""
    M, Q, SN, LX = w["M"], w["Q"], w["S"], w["LX"]
    by = {x["id"]: x for x in LX}
    pk = []                      # (county, date, [doc keys in order])

    def package(county, date, keys):
        pk.append((county, date, keys))

    # closings
    land = {}
    for r in M.itertuples():
        if r.route == "P":
            package(r.county, r.deed_rec, [("D", r.rid), ("M", r.rid)] + ([("2", r.rid)] if r.second_amt else []))
        else:
            package(r.county, r.deed_rec, [("D", r.rid)])
            package(r.county, r.mtg_rec, [("M", r.rid)])
    for r in M[M.land_county != ""].itertuples():
        rng = S.stream("land", r.lender, r.close)
        dl = S.next_bday(r.deed_rec + dt.timedelta(days=int(rng.integers(0, 4))))
        if r.route == "P":
            package(r.land_county, dl, [("DL", r.rid), ("ML", r.rid)])
            ml = dl
        else:
            ml = S.next_bday(r.mtg_rec + dt.timedelta(days=int(rng.integers(0, 4))))
            package(r.land_county, dl, [("DL", r.rid)])
            package(r.land_county, ml, [("ML", r.rid)])
        land[r.rid] = (dl, ml) + parcel(rng, r.land_county, True)
    # quitclaim refinances: route as the lender records
    Q["route"], Q["deed_rec"], Q["mtg_rec"] = "", None, None
    for lid, g in Q.groupby("lender", sort=True):
        rng = S.stream("qrec", lid)
        for i in g.index.values:
            r = Q.loc[i]
            rt = by[lid]["route"]
            if rt == "S" and r.close >= W.SWITCH:
                rt = "P"
            dr = S.next_bday(r.close + dt.timedelta(days=int(rng.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1]))))
            mr = dr if rt == "P" else S.next_bday(dr + dt.timedelta(days=1 + int(min(43, rng.gamma(1.6, 7.0)))))
            Q.at[i, "route"], Q.at[i, "deed_rec"], Q.at[i, "mtg_rec"] = rt, dr, mr
    for r in Q.itertuples():
        if r.route == "P":
            package(r.county, r.deed_rec, [("QD", r.rid), ("QM", r.rid)])
        else:
            package(r.county, r.deed_rec, [("QD", r.rid)])
            package(r.county, r.mtg_rec, [("QM", r.rid)])
    cap = np.zeros(len(Q), bool)
    yr = Q.close.map(lambda d: d.year)
    for (lid, rt, y), g in Q.groupby(["lender", "route", yr], sort=True):
        g = g.sort_values(["county", "close", "rid"], kind="mergesort")
        x = by[lid]
        cap[g.index.values] = S.systematic(len(g), W.CAPTURE[rt] + (x["off"] if rt == x["route"] else 0.0),
                                           S.stream("qcap", lid, rt, y).random())
    Q["captured"] = cap
    # seller-carried notes: recorded with the deed
    rng = S.stream("snrec")
    SN["deed_rec"] = [S.next_bday(d + dt.timedelta(days=int(rng.choice([0, 1, 2], p=[0.4, 0.4, 0.2])))) for d in SN.close]
    SN["mtg_rec"] = SN.deed_rec
    SN["captured"] = S.systematic(len(SN), W.CAPTURE["P"], rng.random())
    for r in SN.itertuples():
        package(r.county, r.deed_rec, [("SD", r.rid), ("SM", r.rid)])
    # re-recordings of mortgages the vendor holds
    rr = {}
    for (lid, rt), g in M[M.captured].groupby(["lender", "route"], sort=True):
        g = g.sort_values(["close", "rid"], kind="mergesort")
        rng = S.stream("rr", lid, rt)
        sel = S.systematic(len(g), W.RERECORD[rt], rng.random())
        for i in g.index.values[sel]:
            r = M.loc[i]
            d = S.next_bday(r.mtg_rec + dt.timedelta(days=int(rng.integers(24, 150))))
            if d <= W.FEED_LAST:
                rr[r.rid] = d
                package(r.county, d, [("RM", r.rid)])
    # number every county's documents day by day
    by_day = {}
    for c, d, keys in pk:
        by_day.setdefault((c, d), []).append(keys)
    doc, nrng = {}, np.random.default_rng(W.SEED + 23)
    for c in W.REGION:
        for y in (2023, 2024, 2025, 2026):
            days = [d for d in S.all_bdays(y) if (y > 2023 or d >= dt.date(2023, 10, 2)) and d <= dt.date(2026, 12, 31)]
            n = int(W.DOCS_PER_DAY[c] * 186 * 0.97) if y == 2023 else 0
            for d in days:
                pkgs = by_day.get((c, d), [])
                order = nrng.permutation(len(pkgs))
                other = int(nrng.poisson(W.DOCS_PER_DAY[c] * (0.8 + 0.4 * W.MONTH_W[d.month - 1] / W.MONTH_W.mean())))
                gaps = nrng.multinomial(other, np.ones(len(pkgs) + 1) / (len(pkgs) + 1))
                for k, j in enumerate(order):
                    n += int(gaps[k])
                    for key in pkgs[j]:
                        n += 1
                        doc[key] = W.DOC_FORMAT[c].format(y=y, yy=y % 100, n=n)
                n += int(gaps[-1])
    return dict(doc=doc, land=land, rr=rr)


def feed(w, R):
    """The vendor's purchase-money rows: one per mortgage it paired with a conveyance recorded in the eight counties."""
    M, Q, SN, LX = w["M"], w["Q"], w["S"], w["LX"]
    by = {x["id"]: x for x in LX}
    doc, land, rr = R["doc"], R["land"], R["rr"]
    rng = np.random.default_rng(W.SEED + 31)
    pick = {x["id"]: strings(x) for x in LX}

    def lender_string(lid):
        opts = pick[lid]
        return opts[rng.choice(len(opts), p=np.array([p for _, p in opts]))][0]

    rows = []
    for r in M[M.captured].itertuples():
        dtp, grantor = deed_type(rng, r.seller)
        ms = lender_string(r.lender)
        base = dict(src="M", rid=r.rid, lender=r.lender, county=r.county, instr=r.close, amount=r.amount,
                    mortgagee=ms, mortgagor=r.buyer, deed_type=dtp, consideration=consideration(rng, dtp),
                    grantor=grantor, grantee=r.buyer, ltype=r.ltype)
        rows.append(dict(base, mtg_doc=doc[("M", r.rid)], mtg_rec=r.mtg_rec, deed_doc=doc[("D", r.rid)],
                         deed_rec=r.deed_rec, apn=r.apn, addr=r.addr, city=r.city, zip=r.zip, legal=r.legal,
                         remarks="", kind="purchase"))
        if r.second_amt:
            rows.append(dict(base, amount=r.second_amt, mtg_doc=doc[("2", r.rid)], mtg_rec=r.mtg_rec,
                             deed_doc=doc[("D", r.rid)], deed_rec=r.deed_rec, apn=r.apn, addr=r.addr, city=r.city,
                             zip=r.zip, legal=r.legal, remarks="", kind="second"))
        if r.land_county:
            dl, ml, apn, legal = land[r.rid]
            rows.append(dict(base, county=r.land_county, mtg_doc=doc[("ML", r.rid)], mtg_rec=ml,
                             deed_doc=doc[("DL", r.rid)], deed_rec=dl, apn=apn, addr="", city="", zip="", legal=legal,
                             remarks="", kind="land"))
        if r.rid in rr:
            rows.append(dict(base, mtg_doc=doc[("RM", r.rid)], mtg_rec=rr[r.rid], deed_doc=doc[("D", r.rid)],
                             deed_rec=r.deed_rec, apn=r.apn, addr=r.addr, city=r.city, zip=r.zip, legal=r.legal,
                             remarks="%s; ORIG DOC %s" % (REMARKS[int(rng.integers(len(REMARKS)))], doc[("M", r.rid)]),
                             kind="rerecord"))
    for r in Q[Q.captured].itertuples():
        rows.append(dict(src="Q", rid=r.rid, lender=r.lender, county=r.county, instr=r.close, amount=r.amount,
                         mortgagee=lender_string(r.lender), mortgagor=r.buyer, deed_type="QCD",
                         consideration=consideration(rng, "QCD"), grantor=r.seller, grantee=r.buyer, ltype="",
                         mtg_doc=doc[("QM", r.rid)], mtg_rec=r.mtg_rec, deed_doc=doc[("QD", r.rid)], deed_rec=r.deed_rec,
                         apn=r.apn, addr=r.addr, city=r.city, zip=r.zip, legal=r.legal, remarks="", kind="quitclaim"))
    for r in SN[SN.captured].itertuples():
        rows.append(dict(src="S", rid=r.rid, lender="", county=r.county, instr=r.close, amount=r.amount,
                         mortgagee=r.seller, mortgagor=r.buyer, deed_type="WD", consideration=consideration(rng, "WD"),
                         grantor=r.seller, grantee=r.buyer, ltype="", mtg_doc=doc[("SM", r.rid)], mtg_rec=r.mtg_rec,
                         deed_doc=doc[("SD", r.rid)], deed_rec=r.deed_rec, apn=r.apn, addr=r.addr, city=r.city,
                         zip=r.zip, legal=r.legal, remarks="", kind="seller"))
    F = pd.DataFrame(rows)
    F = F[(F.mtg_rec >= W.FEED_FIRST) & (F.mtg_rec <= W.FEED_LAST)].copy()
    F["load"] = [S.next_bday(d + dt.timedelta(days=int(rng.integers(2, 8)))) for d in F.mtg_rec]
    F = F.sort_values(["load", "county", "mtg_rec", "mtg_doc"], kind="mergesort").reset_index(drop=True)
    F["rec_key"] = ["VR%s%07d" % (W.FIPS[c][2:], 1180000 + i * 3 + int(rng.integers(0, 3))) for i, c in enumerate(F.county)]
    return F
