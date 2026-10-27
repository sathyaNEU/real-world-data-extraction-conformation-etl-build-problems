"""The files Sandpiper Mutual's own systems and its vendors would hold, cut from the world.

Each writer returns a DataFrame (or a dict of them) and build.py saves them. Everything here is deterministic given
the world and REC_SEED.
"""
import datetime as dt
import zlib

import numpy as np
import pandas as pd

import params as P
import world as W

REC_SEED = 30917
CUTOVER = dt.date(2012, 1, 1)


def _cat_code(code):
    y, n = code.split("-")
    return "%s-CAT-%s" % (y[2:], n)


def _legacy_storm(code):
    y, n = code.split("-")
    return "L%s%s" % (y[2:], n)


# Streets renamed for 911 addressing: county -> (street index today, the old name, the date the new name took effect).
# The policy master and the portfolios carry today's name; a permit or certificate keeps the name it was issued under.
RENAMES = {"MRS": (W.STREETS.index("Gulf Breeze"), "Tram", "2023-04-01"),
           "HRB": (W.STREETS.index("Marsh Hen"), "Boggy Creek", "2022-07-01"),
           "CLF": (W.STREETS.index("Laurel Hill"), "Sawmill", "2024-01-15"),
           "CYR": (W.STREETS.index("Fort Dale"), "Pinebarren", "2022-10-01")}


def street_on(w, b, day=None):
    """The street name a document dated `day` would carry for building b."""
    county = w["zips"][b["zi"]]["county"]
    r = RENAMES.get(county)
    if r and day is not None and b["street"] == r[0] and day.isoformat() < r[2]:
        return r[1]
    return W.STREETS[b["street"]]


def addr(b, upper=False, st=None):
    st, (full, ab) = (st or W.STREETS[b["street"]]), W.STYPES[b["stype"]]
    if upper:
        s = "%d %s %s" % (b["num"], st.upper(), ab)
        return s + (" COTTAGE" if b["bldg"] == 1 else "")
    s = "%d %s %s" % (b["num"], st, full)
    return s + (", Cottage" if b["bldg"] == 1 else "")


def addr_permit(b, st=None):
    """The county portals' form: upper case, street type abbreviated, a second building as BLDG 2."""
    st, (full, ab) = (st or W.STREETS[b["street"]]), W.STYPES[b["stype"]]
    s = "%d %s %s" % (b["num"], st.upper(), ab)
    return s + (" BLDG 2" if b["bldg"] == 1 else "")


def parcel_ids(w):
    """Each parcel's ten-digit id: county number, ZIP index, the parcel's serial within the ZIP."""
    if "_pids" in w:
        return w["_pids"]
    out, serial, count = {}, {}, {}
    cidx = {c[0]: i + 1 for i, c in enumerate(W.COUNTIES)}
    seen = set()
    for b in w["homes"]:
        if b["parcel"] not in seen:
            seen.add(b["parcel"])
            count[b["zi"]] = count.get(b["zi"], 0) + 1
    for b in w["homes"]:
        if b["parcel"] in out:
            continue
        z = w["zips"][b["zi"]]
        serial[b["zi"]] = serial.get(b["zi"], 0) + 1
        step = max(2, 9400 // count[b["zi"]])
        lad = _ladder("parcel-%d" % b["zi"], count[b["zi"]], 1, 2 * step - 1)
        out[b["parcel"]] = "%02d%04d%04d" % (cidx[z["county"]] + 30, b["zi"] + 100, int(lad[serial[b["zi"]] - 1]))
    w["_pids"] = out
    return out


_LADDERS = {}


def _ladder(tag, n, lo, hi):
    """A numbering series with the gaps a live system leaves (quotes not taken up, voided and test numbers)."""
    if tag not in _LADDERS or len(_LADDERS[tag]) < n:
        r = np.random.default_rng(zlib.crc32(tag.encode()))
        _LADDERS[tag] = np.cumsum(r.integers(lo, hi + 1, size=max(n, 1)))
    return _LADDERS[tag]


def _channel(p):
    """Written through an agent or direct; the direct share grew after the 2017 web quote launch."""
    u = (zlib.crc32(("channel-%d" % p["pno"]).encode()) % 10007) / 10007.0
    return "Direct" if u < (0.22 if p["incept"].year < 2017 else 0.41) else "Agency"


def policy_number(p):
    return "H%07d" % (1040000 + int(_ladder("policy", 200000, 1, 11)[p["seqno"]]))


def coverage(p, year):
    return round(p["val"] * (1.0 + 0.03 * (year - 2008)) / 1000.0) * 1000.0


def storm_register(w):
    rows = []
    for s in w["storms"]:
        rows.append(dict(storm_id=s["code"], storm_name=s["name"], landfall_date=s["date"].isoformat(),
                         claims_catastrophe_code=_cat_code(s["code"]) if s["year"] >= 2012 else "",
                         legacy_catastrophe_code=_legacy_storm(s["code"]) if s["year"] < 2012 else "",
                         saffir_simpson_at_landfall=_category(s["peak"])))
    return pd.DataFrame(rows)


def _category(peak_gust):
    sust = peak_gust / 1.25
    for lim, cat in ((157, "5"), (130, "4"), (111, "3"), (96, "2"), (74, "1")):
        if sust >= lim:
            return "Category " + cat
    return "Tropical storm"


def footprints(w):
    """One sheet per storm: the older analysis service in knots with a title block, the newer one in mph."""
    sheets = {}
    for s in w["storms"]:
        zips = sorted(s["gust"])
        name = "%s %d" % (s["name"].split()[-1], s["year"])
        if s["year"] < W.KNOT_UNTIL:
            g = [round(s["gust"][z] / W.KT, 1) for z in zips]
            df = pd.DataFrame({"ZIP": zips, "Peak gust (kt)": g, "Basis": ["analysis"] * len(zips)})
        else:
            g = [int(round(s["gust"][z])) for z in zips]
            df = pd.DataFrame({"zip_code": zips, "peak_gust_mph": g, "method": ["reanalysis 3-s gust, 10 m"] * len(zips)})
        sheets[name] = (s, df)
    return sheets


def inforce(w):
    rows = []
    pol = w["policies"]
    for s in w["storms"]:
        agg = {}
        for (i, fort, cov, gu, gross, g) in s["homes"]:
            key = (pol[i]["zip"], fort)
            a = agg.setdefault(key, [0, 0.0])
            a[0] += 1
            a[1] += cov
        for (z, fort), (n, cov) in sorted(agg.items()):
            thousands = s["year"] < 2019
            rows.append(dict(storm_id=s["code"], zip_code=z, roof_designation="FORTIFIED Roof" if fort else "Standard",
                             policies_in_force=n, coverage_a=round(cov / 1000.0, 1) if thousands else round(cov, 0),
                             coverage_unit="USD thousands" if thousands else "USD"))
    return pd.DataFrame(rows)


def claims(w, rng):
    """Payment lines from the claims system that went live on 1 January 2012: named-storm claims since 2012, the
    legacy storms' claims still open at the cut-over (carried over with their paid-to-date), wind and hail claims
    outside named storms, and the transfer book's open claims taken on in July 2024."""
    pol = w["policies"]
    rows = []
    seq = {}
    shut = {}

    def cno(year):
        seq[year] = seq.get(year, 0) + 1
        return "HC%02d%06d" % (year % 100, 100000 + int(_ladder("claim-%d" % year, 120000, 1, 6)[seq[year] - 1]))

    def credit(i, fort):
        if i not in shut:
            shut[i] = rng.random() < 0.16
        parts = (["FORT-R"] if fort else []) + (["SHUT"] if shut[i] else [])
        return ";".join(parts)

    def lines(claim, i, cat, peril, ld, rd, fort, total, legacy_ref="", first_date=None):
        """Split a claim's net paid into an indemnity line, supplements and a recovery."""
        p = pol[i]
        base = dict(policy_number=policy_number(p), catastrophe_code=cat, peril=peril, loss_date=ld.isoformat(),
                    reported_date=rd.isoformat(), zip_code=p["zip"], mitigation_credit=credit(i, fort),
                    legacy_claim_ref=legacy_ref)
        out = []
        if total <= 0:
            pdte = W.bday(rd + dt.timedelta(days=int(rng.integers(12, 90))))
            if pdte <= W.ASOF:
                out.append(dict(base, claim_number=claim, line_type="CLOSED_NIL", payment_date=pdte.isoformat(),
                                amount_usd=0.0))
            return out
        rec = 0.0
        if rng.random() < 0.012:
            rec = round(total * float(rng.uniform(0.05, 0.2)), 2)
        gross = total + rec
        parts = [gross]
        if rng.random() < 0.32:
            f = float(rng.uniform(0.55, 0.9))
            parts = [round(gross * f, 2), round(gross - round(gross * f, 2), 2)]
            if rng.random() < 0.15:
                f2 = float(rng.uniform(0.5, 0.8))
                parts = [parts[0], round(parts[1] * f2, 2), round(parts[1] - round(parts[1] * f2, 2), 2)]
        d0 = W.bday(first_date or rd + dt.timedelta(days=int(rng.integers(8, 75))))
        for k, amt in enumerate(parts):
            pdte = W.bday(d0 + dt.timedelta(days=int(0 if k == 0 else rng.integers(25, 260) * k)))
            if pdte > W.ASOF:
                continue
            out.append(dict(base, claim_number=claim if k == 0 else "%s-S%d" % (claim, k),
                            line_type="INDEMNITY" if k == 0 else "SUPPLEMENT",
                            payment_date=pdte.isoformat(), amount_usd=round(amt, 2)))
        if rec:
            pdte = W.bday(d0 + dt.timedelta(days=int(rng.integers(120, 540))))
            if pdte <= W.ASOF:
                out.append(dict(base, claim_number=claim, line_type="RECOVERY", payment_date=pdte.isoformat(),
                                amount_usd=-rec))
        return out

    # named storms since the cut-over
    for s in w["storms"]:
        if s["year"] < W.LEGACY_CUTOVER:
            continue
        cat = _cat_code(s["code"])
        for (i, fort, cov, gu, gross, g) in s["homes"]:
            if gross <= 0 and not (gu > 0.012 * cov and rng.random() < 0.55):
                continue
            ld = s["date"] + dt.timedelta(days=int(rng.random() < 0.18))
            rd = ld + dt.timedelta(days=int(rng.integers(1, 40)))
            rows += lines(cno(s["year"]), i, cat, "Wind - named storm", ld, rd, fort, round(gross, 2))
    # wind and hail outside named storms
    for (i, ld, sev, fort) in w["nonstorm"]:
        rd = ld + dt.timedelta(days=int(rng.integers(0, 30)))
        if rd > W.ASOF:
            continue
        peril = "Hail" if rng.random() < 0.45 else "Wind"
        rows += lines(cno(rd.year), i, "", peril, ld, rd, fort, sev if rng.random() < 0.86 else 0.0)
    for (i, ld, sev, fort) in w["assumed"]:
        rd = ld + dt.timedelta(days=int(rng.integers(0, 30)))
        rows += lines(cno(2024), i, "", "Hail" if rng.random() < 0.45 else "Wind", ld, rd, fort, sev,
                      first_date=dt.date(2024, 7, 1) + dt.timedelta(days=int(rng.integers(1, 60))))
    return rows


def legacy(w, rng):
    """The legacy system's quarterly valuations for the 2008, 2009 and 2011 storms (paid to date, cumulative), and
    the carried-over claims' lines in the new system."""
    pol = w["policies"]
    val_rows, carried = [], []
    seq = 0
    for s in w["storms"]:
        if s["year"] >= W.LEGACY_CUTOVER:
            continue
        lcode = _legacy_storm(s["code"])
        for (i, fort, cov, gu, gross, g) in s["homes"]:
            if gross <= 0 and not (gu > 0.012 * cov and rng.random() < 0.5):
                continue
            seq += 1
            claim = "%s-%05d" % (lcode, seq)
            p = pol[i]
            nq = int(rng.integers(1, 9)) if rng.random() > 0.07 else int(rng.integers(14, 24))
            total = round(gross, 2)
            # cumulative paid by quarter: instalments over nq quarters; a recovery may come later
            qend = []
            q = pd.Timestamp(s["date"]).to_period("Q")
            for k in range(nq + 3):
                qend.append((q + k).end_time.date())
            shares = np.sort(rng.uniform(0, 1, nq - 1)) if nq > 1 else np.array([])
            cum = [round(total * x, 2) for x in shares] + [total]
            rec = round(total * float(rng.uniform(0.05, 0.2)), 2) if (total > 0 and rng.random() < 0.02) else 0.0
            series = cum + ([round(total - rec, 2)] if rec else [])
            status = "OPEN"
            for k, c in enumerate(series):
                d = qend[k]
                if d > dt.date(2011, 12, 31):
                    break
                status = "CLOSED" if k == len(series) - 1 else "OPEN"
                val_rows.append(dict(legacy_claim_no=claim, policy_ref=policy_number(p), storm=lcode,
                                     zip=p["zip"], valuation_date=d.strftime("%m/%d/%Y"), status=status,
                                     paid_to_date=round(c, 2)))
            if total <= 0:
                val_rows.append(dict(legacy_claim_no=claim, policy_ref=policy_number(p), storm=lcode, zip=p["zip"],
                                     valuation_date=qend[0].strftime("%m/%d/%Y"), status="CLOSED", paid_to_date=0.0))
                continue
            # still open at the cut-over: carried into the new system with its paid-to-date as the first line
            done = [c for k, c in enumerate(series) if qend[k] <= dt.date(2011, 12, 31)]
            if len(done) < len(series):
                paid_at_cut = done[-1] if done else 0.0
                carried.append(dict(i=i, claim=claim, cat=_cat_code(s["code"]), ld=s["date"], fort=fort,
                                    at_cut=paid_at_cut, rest=[round(series[k] - series[k - 1] if k else series[0], 2)
                                                              for k in range(len(done), len(series))],
                                    rest_dates=[qend[k] for k in range(len(done), len(series))]))
    return pd.DataFrame(val_rows), carried


def carried_lines(w, carried, rng):
    pol = w["policies"]
    rows = []
    for n, c in enumerate(carried):
        p = pol[c["i"]]
        new = "HC12%06d" % (300000 + n * 17 % 99999)
        base = dict(policy_number=policy_number(p), catastrophe_code=c["cat"], peril="Wind - named storm",
                    loss_date=c["ld"].isoformat(), reported_date=c["ld"].isoformat(), zip_code=p["zip"],
                    mitigation_credit="", legacy_claim_ref=c["claim"])
        if c["at_cut"] > 0:
            rows.append(dict(base, claim_number=new, line_type="INDEMNITY", payment_date=CUTOVER.isoformat(),
                             amount_usd=round(c["at_cut"], 2)))
        for k, (amt, d) in enumerate(zip(c["rest"], c["rest_dates"])):
            rows.append(dict(base, claim_number=new if k == 0 and c["at_cut"] <= 0 else "%s-S%d" % (new, k + 1),
                             line_type="INDEMNITY" if amt > 0 else "RECOVERY",
                             payment_date=W.bday(d - dt.timedelta(days=int(rng.integers(5, 60)))).isoformat(),
                             amount_usd=round(amt, 2)))
    return rows


def in_force_on(p, day):
    return p["incept"] <= day < p["lapse"]


def policy_master(w):
    pids = parcel_ids(w)
    rows = []
    for p in w["policies"]:
        b = w["homes"][p["home"]]
        cancel = "" if p["lapse"] > W.ASOF else p["lapse"].isoformat()
        cov_year = 2026 if not cancel else p["lapse"].year
        rows.append(dict(policy_number=policy_number(p), parcel_id=pids[b["parcel"]], site_address=addr(b),
                         zip_code=p["zip"], county=P.COUNTY_NAME[p["county"]],
                         inception_date=p["incept"].isoformat(), cancellation_date=cancel,
                         coverage_a_usd=int(coverage(p, cov_year)),
                         channel="Transfer - Gulfway" if p["transfer"] else _channel(p)))
    return pd.DataFrame(rows).sort_values(["zip_code", "policy_number"]).reset_index(drop=True)


def _policy_on(w, h, day):
    for p in w["by_home"].get(h, []):
        if in_force_on(p, day):
            return p
    return None


def certificates(w, rng):
    pids = parcel_ids(w)
    rows = []
    # the program numbers certificates as it issues them
    order = sorted((c["issued"], h, k) for h, b in enumerate(w["homes"]) for k, c in enumerate(b["certs"])
                   if c["issued"] <= W.ASOF)
    lad = _ladder("cert", len(order) + 1, 1, 9)
    numbers = {(h, k): "FR%07d" % (2100000 + int(lad[n])) for n, (_, h, k) in enumerate(order)}
    for h, b in enumerate(w["homes"]):
        for k, c in enumerate(b["certs"]):
            if c["issued"] > W.ASOF:
                continue
            num = numbers[(h, k)]
            p = _policy_on(w, h, c["issued"])
            pid = pids[b["parcel"]]
            rows.append(dict(certificate_number=num, event="ISSUED", event_date=c["issued"].isoformat(),
                             expiry_date=c["expiry"].isoformat(), designation="FORTIFIED Roof",
                             evaluation=("Re-designation" if any(o["expiry"] >= c["issued"] and o is not c and o["issued"] < c["issued"] for o in b["certs"]) else "New roof"),
                             parcel_ref="%s-%s-%s" % (pid[:2], pid[2:6], pid[6:]),
                             property_address=addr(b, upper=True, st=street_on(w, b, c["issued"])),
                             policy_number_at_issue=policy_number(p) if p else ""))
            if c["void"] is not None and c["void"] <= W.ASOF and c["void"] < c["expiry"]:
                rows.append(dict(certificate_number=num, event="VOIDED", event_date=c["void"].isoformat(),
                                 expiry_date="", designation="FORTIFIED Roof", evaluation="Audit",
                                 parcel_ref="%s-%s-%s" % (pid[:2], pid[2:6], pid[6:]),
                                 property_address=addr(b, upper=True, st=street_on(w, b, c["issued"])),
                                 policy_number_at_issue=policy_number(p) if p else ""))
    df = pd.DataFrame(rows)
    return df.sort_values(["event_date", "certificate_number"]).reset_index(drop=True)


def permits(w, rng):
    """Roofing permits from the four candidate counties' permit portals since 2013, with the other trades the
    extract also carries."""
    rows = []
    other = ["ELECTRICAL", "PLUMBING", "POOL/SPA", "FENCE", "MECHANICAL", "WINDOW/DOOR"]
    for h, b in enumerate(w["homes"]):
        z = w["zips"][b["zi"]]
        if z["county"] not in P.CANDIDATES:
            continue
        for (d, cls) in b["events"]:
            if d.year < 2013 or d > W.ASOF:
                continue
            rows.append(dict(county=P.COUNTY_NAME[z["county"]], issue_date=d.isoformat(), work_class=cls,
                             address=addr_permit(b, street_on(w, b, d)), zip=z["zip"],
                             valuation_usd=int(round(float(rng.uniform(9000, 26000) if cls == "RE-ROOF" else rng.uniform(600, 5200)), -2))))
        if rng.random() < 0.25:
            d = W.bday(dt.date(int(rng.integers(2013, 2027)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))
            if d <= W.ASOF:
                rows.append(dict(county=P.COUNTY_NAME[z["county"]], issue_date=d.isoformat(),
                                 work_class=other[int(rng.integers(0, len(other)))], address=addr_permit(b, street_on(w, b, d)),
                                 zip=z["zip"],
                                 valuation_usd=int(round(float(rng.uniform(800, 30000)), -2))))
    df = pd.DataFrame(rows).sort_values(["county", "issue_date", "address"]).reset_index(drop=True)
    # each county numbers all its building permits in one series a year; the roofing permits are part of it
    k = df.groupby(["county", df.issue_date.str[:4]]).cumcount()
    df.insert(1, "permit_number", ["%s-%s-%05d" % (c[:3].upper(), d[2:4], int(_ladder("permit-%s-%s" % (c, d[:4]), 9000, 1, 7)[i]))
                                   for c, d, i in zip(df.county, df.issue_date, k)])
    return df


def roof_year_true(b, day):
    yrs = [b["roof0"]] + [d.year for d, c in b["events"] if c == "RE-ROOF" and d <= day]
    return max(yrs)


def portfolios(w):
    """Each candidate county's 1,500 homes the round would re-roof: in force at 30 September 2026 without a valid
    certificate, the oldest roofs on the underwriting record first."""
    out = []
    for c in P.CANDIDATES:
        cand = []
        for p in w["policies"]:
            if p["county"] != c or not in_force_on(p, W.ASOF):
                continue
            b = w["homes"][p["home"]]
            if W.certified(b, W.ASOF):
                continue
            recorded = roof_year_true(b, p["incept"])
            cand.append((recorded, p["pno"], p, b))
        cand.sort(key=lambda t: (t[0], t[1]))
        for recorded, _, p, b in cand[:P.ROUND_HOMES]:
            out.append(dict(portfolio=P.PORTFOLIO_CODE[c], county=P.COUNTY_NAME[c], policy_number=policy_number(p),
                            site_address=addr(b), zip_code=p["zip"], coverage_a_usd=int(coverage(p, 2026)),
                            roof_year_on_record=recorded, _home=p["home"]))
    return pd.DataFrame(out)


_LS = {}


def ls(g):
    k = round(float(g), 1)
    if k not in _LS:
        _LS[k] = W.expected_gross(W.gu_mean, k)
    return _LS[k]


def event_ids():
    """The 9,000 events' numbers in the vendor's catalog, which also holds events that never reach this coast."""
    return [27000000 + int(x) for x in _ladder("hu27-events", W.VENDOR_EVENTS, 1, 9)]


def vendor(w, pf):
    """The vendor's event loss table on each county's modeled portfolio (standard roofs, gross of reinsurance, after
    the 2 percent named-storm deductible) and its hazard summary (each event's peak-gust class at the portfolio)."""
    V = W.vendor_set()
    elt, haz = [], []
    for j, c in enumerate(P.CANDIDATES):
        tiv = float(pf[pf.county == P.COUNTY_NAME[c]].coverage_a_usd.sum())
        g = V["counties"][c]["gust"]
        for e in range(len(g)):
            gg = round(float(g[e]), 1)
            mean = tiv * ls(gg) * float(V["noise"][j][e])
            if mean < 5000:
                continue
            eid = event_ids()[e]
            elt.append(dict(event_id=eid, portfolio_id=P.PORTFOLIO_CODE[c], annual_rate=round(float(V["rate"][e]), 9),
                            mean_loss_usd=round(mean, 0), sd_loss_usd=round(mean * float(0.9 + 0.6 * min(1, mean / tiv * 4)), 0),
                            exposed_value_usd=round(tiv, 0)))
            lo = int(gg // 10 * 10)
            haz.append(dict(event_ref="HU27-%07d" % eid, county=P.COUNTY_NAME[c], peak_gust_class="%d-%d mph" % (lo, lo + 9),
                            landfall_segment="S%02d" % int(np.clip((V["x0"][e] + 70) // 25, 0, 14))))
    return pd.DataFrame(elt), pd.DataFrame(haz).sort_values(["event_ref", "county"]).reset_index(drop=True)
