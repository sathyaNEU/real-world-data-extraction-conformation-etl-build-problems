"""The pack read back, and every route computed from it: the golden replay of each building's flood record on the
building as it stands, the ladder's wrong routes, each Layer 1 item mishandled, and the asks with their wrong paths.
Reads only target/."""
import csv
import datetime as dt
import os
from collections import defaultdict

AS_OF = dt.date(2026, 9, 30)
PULL = dt.date(2026, 10, 2)
WIN0, WIN1 = dt.date(2001, 1, 1), dt.date(2026, 1, 1)      # the window, end exclusive
YEAR = 365.25
FILES = {
    "policies": "nfip_dsa_policy_history_2026-10-02.csv",
    "claims1": "nfip_dsa_claims_2001-2019.csv",
    "claims2": "nfip_dsa_claims_2020-2026.csv",
    "register": "tsrfa_hma_grants_export_2026-09-30.xlsx",
    "crosswalk": "tsrfa_property_building_crosswalk.csv",
    "offsets": "tsrfa_vertical_datum_offsets.csv",
    "members": "tsrfa_member_counties.csv",
}
_CACHE = {}


def rows(target, key):
    path = os.path.join(target, FILES[key])
    if not os.path.exists(path):          # a file left out of a subset (the separation checks)
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def day(s):
    return dt.date.fromisoformat(s) if s else None


def mdy(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").date() if s else None


def local_day(stamp):
    """A UTC timestamp of the 2023 layout to its Central time date."""
    if not stamp:
        return None
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S.000Z")
    d0 = t.date()
    for off in (5, 6):
        loc = t - dt.timedelta(hours=off)
        if _dst(loc.date()) == (off == 5):
            return loc.date()
    return d0


def _dst(d):
    mar = dt.date(d.year, 3, 1)
    s = mar + dt.timedelta(days=(6 - mar.weekday()) % 7 + 7)
    nov = dt.date(d.year, 11, 1)
    e = nov + dt.timedelta(days=(6 - nov.weekday()) % 7)
    return s <= d < e


def fl(s):
    return float(s) if s not in ("", None) else None


# ---------------------------------------------------------------------------------------------- reading
def load(target):
    if target in _CACHE:
        return _CACHE[target]
    off = {r["county_fips"]: float(r["navd88_minus_ngvd29_ft"]) for r in rows(target, "offsets")}
    names = {r["county_fips"]: r["county"] for r in rows(target, "members")}
    comm = {}
    for r in rows(target, "members"):
        for c in r["nfip_communities"].split(";"):
            comm[c] = r["county_fips"]
    pols = []
    for r in rows(target, "policies"):
        s = day(r["original_effective_date"])
        if r["policy_status"] == "ACTIVE":
            e = None
        elif r["policy_status"] == "EXPIRED":
            e = day(r["term_expiration_date"])
        else:
            e = day(r["cancellation_date"])
        lfe, bfe = fl(r["lowest_floor_elevation"]), fl(r["base_flood_elevation"])
        if r["elevation_datum"] == "NGVD29":
            lfe = None if lfe is None else lfe + off.get(r["county_fips"], 0.0)
            bfe = None if bfe is None else bfe + off.get(r["county_fips"], 0.0)
        pols.append(dict(number=r["policy_number"], prior=r["prior_policy_number"], bid=r["nfip_building_id"],
                         fips=r["county_fips"], form=r["policy_form"], condo=r["condo_indicator"],
                         bcov=int(r["building_coverage"]), start=s, end=e, lfe=lfe, bfe=bfe,
                         lfe_raw=fl(r["lowest_floor_elevation"]), bfe_raw=fl(r["base_flood_elevation"]),
                         datum=r["elevation_datum"], zone=r["flood_zone"], ec=day(r["elevation_certificate_date"]),
                         status=r["policy_status"], reason=r["cancellation_reason"], company=r["company_code"]))
    claims = []
    for r in rows(target, "claims1"):
        claims.append(dict(number=r["CLAIM_NO"], policy=r["POLICY_NO"], bid=r["BLDG_ID"], fips=r["COUNTY_FIPS"],
                           dol=mdy(r["DATE_OF_LOSS"]), dol_utc=mdy(r["DATE_OF_LOSS"]), reported=mdy(r["DATE_REPORTED"]),
                           status={"C": "Closed", "CWOP": "Closed without payment", "O": "Open"}[r["CLAIM_STATUS"]],
                           condo=r["CONDO_IND"], lfe_raw=fl(r["LOWEST_FLR_ELEV"]), bfe_raw=fl(r["BFE"]),
                           datum=r["ELEV_DATUM"], depth=int(r["WATER_DEPTH_IN"]), bdmg=int(r["BLDG_DAMAGE_AMT"]),
                           bpay=float(r["BLDG_PAID_AMT"]), cpay=float(r["CNTS_PAID_AMT"]), icc=float(r["ICC_PAID_AMT"]),
                           cat=r["CAT_NO"], layout=1))
    for r in rows(target, "claims2"):
        claims.append(dict(number=r["claimNumber"], policy=r["policyNumber"], bid=r["buildingId"], fips=r["countyCode"],
                           dol=local_day(r["dateOfLoss"]), dol_utc=day(r["dateOfLoss"][:10]),
                           reported=local_day(r["originalReportDate"]), status=r["claimStatus"],
                           condo=r["condominiumIndicator"], lfe_raw=fl(r["lowestFloorElevation"]),
                           bfe_raw=fl(r["baseFloodElevation"]), datum=r["verticalDatum"], depth=int(r["waterDepthInches"]),
                           bdmg=int(r["buildingDamageAmount"]), bpay=float(r["amountPaidOnBuildingClaim"]),
                           cpay=float(r["amountPaidOnContentsClaim"]), icc=float(r["amountPaidOnIccClaim"]),
                           cat=r["catastropheNumber"], layout=2))
    for c in claims:
        o = off.get(c["fips"], 0.0)
        c["lfe"] = None if c["lfe_raw"] is None else (c["lfe_raw"] + o if c["datum"] == "NGVD29" else c["lfe_raw"])
        c["bfe"] = None if c["bfe_raw"] is None else (c["bfe_raw"] + o if c["datum"] == "NGVD29" else c["bfe_raw"])
    by_number = {p["number"]: p for p in pols}
    out = dict(off=off, names=names, comm=comm, pols=pols, claims=claims, by_number=by_number)
    _CACHE[target] = out
    return out


def building_policy(p, units=False, contents=False):
    """A building policy (guidelines 2.1): a dwelling, general property or association policy with building
    coverage; unit owners' and contents policies are not."""
    if p["condo"] == "U" and not units:
        return False
    if p["bcov"] <= 0 and not contents:
        return False
    return True


def in_force(p, d):
    return p["start"] <= d and (p["end"] is None or d < p["end"])


def spans_days(spans, a=WIN0, z=WIN1):
    """Days in [a, z) covered by any span, each counted once."""
    iv = sorted((max(s, a), min(e or PULL, z)) for s, e in spans if (e or PULL) > a and s < z)
    tot, cur_s, cur_e = 0, None, None
    for s, e in iv:
        if e <= s:
            continue
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                tot += (cur_e - cur_s).days
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        tot += (cur_e - cur_s).days
    return tot


# ---------------------------------------------------------------------------------------------- the population
def population(target, units=False, contents=False, zone_x=False, datum=True, active=False):
    """The elevated insured buildings (guidelines 2.2): building policy in force on 30 September 2026 with its
    lowest floor at or above its base flood elevation. Returns {bid: dict(fips, lfe, policy, years)}."""
    D = load(target)
    by_b = defaultdict(list)
    for p in D["pols"]:
        if building_policy(p, units, contents):
            by_b[p["bid"]].append(p)
    pop = {}
    for bid, ps in by_b.items():
        cur = [p for p in ps if (p["status"] == "ACTIVE" if active else in_force(p, AS_OF))]
        if not cur:
            continue
        p = max(cur, key=lambda q: q["start"])
        lfe, bfe = (p["lfe"], p["bfe"]) if datum else (p["lfe_raw"], p["bfe_raw"])
        if bfe is None:
            if not zone_x:
                continue
            bfe = -99.0
        if lfe < bfe - 1e-9:
            continue
        pop[bid] = dict(fips=p["fips"], lfe=lfe, lfe_raw=p["lfe_raw"], datum=p["datum"], policy=p["number"],
                        days=spans_days([(q["start"], q["end"]) for q in ps]))
    return pop


def building_claims(target, pop, units=False, contents=False, layout2=True, utc=False):
    """Claims under each population building's building policies with a date of loss in 2001 to 2025."""
    D = load(target)
    out = defaultdict(list)
    for c in D["claims"]:
        if c["bid"] not in pop:
            continue
        if c["layout"] == 2 and not layout2:
            continue
        p = D["by_number"].get(c["policy"])
        if p is None or not building_policy(p, units, contents):
            continue
        dd = c["dol_utc"] if utc else c["dol"]
        if not (WIN0 <= dd < WIN1):
            continue
        out[c["bid"]].append(c)
    return out


def replay_counts(c, b, datum=True, feet=False, bfe_rule=False, threshold=1 / 12.0):
    """Would this claim's flood bring a paid building claim to the building as it stands: the water's elevation on
    the day (the floor the claim was rated on plus the depth above it) against the floor the building has now."""
    lfe_then = c["lfe"] if datum else c["lfe_raw"]
    now = b["lfe"] if datum else b["lfe_raw"]
    depth_ft = c["depth"] if feet else c["depth"] / 12.0
    wse = lfe_then + depth_ft
    if bfe_rule:
        bfe_then = c["bfe"] if datum else c["bfe_raw"]
        if lfe_then < now - 0.45:
            return wse >= (bfe_then or 0) + 1 / 12.0 - 1e-9 and c["bpay"] > 0
        return c["bpay"] > 0
    if threshold <= 0:
        return wse - now > 1e-9
    return wse - now >= threshold - 1e-9


CALL_ROUTES = ("golden", "E0", "E1", "E1r", "E2", "E3", "E7")
MESS_ROUTES = ("datum_raw", "units_in", "contents_in", "zone_x", "cwop_in", "contents_claims", "utc_dol", "depth_feet",
               "policies_not_buildings", "active_status", "any_water")


def raised_from_register(target):
    """Buildings the register shows elevated, with the date: final inspections passed, through the crosswalk."""
    R = register(target)
    xw = {}
    for r in rows(target, "crosswalk"):
        xw[r["property_id"]] = r["nfip_building_id"]
    full = {}
    D = load(target)
    for p in D["pols"]:
        full[p["bid"][:-1]] = p["bid"]
    out = {}
    for pid, pr in R["props"].items():
        if pr["measure"] != "Elevation":
            continue
        done = R["final"].get(pid)
        if done is None or done > AS_OF:
            continue
        bid = xw.get(pid)
        if bid is None:
            continue
        bid = full.get(bid, bid) if len(bid) == 11 else bid
        out[bid] = max(out.get(bid, done), done)
    return out


def rates(target, route="golden"):
    """Each county's expected claim rate under a route: {fips: (claims, building-years, rate per 1,000)}."""
    kw = dict(units=route == "units_in", contents=route == "contents_in", zone_x=route == "zone_x",
              datum=route != "datum_raw", active=route == "active_status")
    pop = population(target, **kw)
    cl = building_claims(target, pop, units=route in ("units_in",), contents=route in ("contents_in", "contents_claims"),
                         layout2=route != "v2_dropped", utc=route == "utc_dol")
    D = load(target)
    raised = raised_from_register(target) if route == "E1r" else None
    res = {}
    for f in D["names"]:
        ids = [b for b, v in pop.items() if v["fips"] == f]
        n, days = 0, 0
        cls_n, cls_d = 0, 0
        for bid in ids:
            b = pop[bid]
            cs = cl.get(bid, [])
            if route in ("E1", "E3", "E2", "E7"):
                pre = [c for c in cs if c["lfe"] is not None and c["lfe"] < b["lfe"] - 0.45]
                last = max((c["dol"] for c in pre), default=None)
            if route == "E0":
                n += sum(1 for c in cs if c["bpay"] > 0)
                days += b["days"]
            elif route == "E1":
                n += sum(1 for c in cs if c["bpay"] > 0 and not (c["lfe"] is not None and c["lfe"] < b["lfe"] - 0.45))
                days += b["days"]
            elif route == "E1r":
                done = raised.get(bid)
                n += sum(1 for c in cs if c["bpay"] > 0 and (done is None or c["dol"] >= done))
                days += b["days"]
            elif route == "E3":
                kept = [c for c in cs if c["bpay"] > 0 and not (c["lfe"] is not None and c["lfe"] < b["lfe"] - 0.45)]
                n += len(kept)
                if pre:
                    # building-years after the elevation: the first post-elevation day is after the last claim on the
                    # old floor; the record's own policies carry the date the floor changed
                    days += _days_after(D, bid, b, last)
                else:
                    days += b["days"]
            elif route == "E2":
                if pre:
                    days += b["days"]
                else:
                    cls_n += sum(1 for c in cs if c["bpay"] > 0)
                    cls_d += b["days"]
                    days += b["days"]
            elif route == "E7":
                n += sum(1 for c in cs if replay_counts(c, b, bfe_rule=True))
                days += b["days"]
            elif route == "cwop_in":
                n += sum(1 for c in cs if replay_counts(c, b) or (c["status"] == "Closed without payment"))
                days += b["days"]
            elif route == "contents_claims":
                n += sum(1 for c in cs if replay_counts(c, b))
                days += b["days"]
            elif route == "depth_feet":
                n += sum(1 for c in cs if replay_counts(c, b, feet=True) and c["depth"] >= 1)
                days += b["days"]
            elif route == "any_water":
                n += sum(1 for c in cs if replay_counts(c, b, threshold=0))
                days += b["days"]
            else:
                n += sum(1 for c in cs if replay_counts(c, b, datum=route != "datum_raw"))
                days += b["days"]
        if route == "E2":
            rate = 1000.0 * cls_n / (cls_d / YEAR) if cls_d else 0.0
            res[f] = (cls_n, days / YEAR, rate)
        else:
            res[f] = (n, days / YEAR, 1000.0 * n / (days / YEAR) if days else 0.0)
    if route == "policies_not_buildings":
        return _policy_count_route(target)
    return res


def _days_after(D, bid, b, last):
    """A raised building's days of cover from the first policy term rated on its present floor."""
    first = None
    for p in D["pols"]:
        if p["bid"] == bid and building_policy(p) and p["lfe"] is not None and abs(p["lfe"] - b["lfe"]) < 0.05 \
                and p["ec"] is not None and p["ec"] > last:
            first = p["ec"] if first is None else min(first, p["ec"])
    if first is None:
        first = last + dt.timedelta(days=1)
    spans = [(max(p["start"], first), p["end"]) for p in D["pols"] if p["bid"] == bid and building_policy(p)
             and (p["end"] or PULL) > first]
    return spans_days(spans)


def _policy_count_route(target):
    """Exposure counted in policy-years rather than building-years (a building's policies summed, overlaps twice)."""
    D = load(target)
    pop = population(target)
    cl = building_claims(target, pop)
    res = {}
    by_b = defaultdict(list)
    for p in D["pols"]:
        if p["bid"] in pop and building_policy(p):
            by_b[p["bid"]].append(p)
    for f in D["names"]:
        n, days = 0, 0
        for bid, b in pop.items():
            if b["fips"] != f:
                continue
            n += sum(1 for c in cl.get(bid, []) if replay_counts(c, b))
            days += sum(spans_days([(p["start"], p["end"])]) for p in by_b[bid])
        res[f] = (n, days / YEAR, 1000.0 * n / (days / YEAR))
    return res


def slate(res):
    order = sorted(res, key=lambda f: res[f][2])
    return order[:5], order[5]


def r1(v):
    return float("%.1f" % (v + 1e-9))


# ---------------------------------------------------------------------------------------------- ask A, 2026 losses
A_ROUTES = ("golden", "naive", "bdol_latest", "bdol_sum", "validity", "chain_sum", "utc", "with_icc")


def losses_2026(target, route="golden"):
    """Each county's paid building claims on losses in 2026 and the building payments made on them as of the extract:
    {fips: (claims, payments)}."""
    D = load(target)
    pols = D["by_number"]
    cs = []
    for c in D["claims"]:
        dd = c["dol_utc"] if route == "utc" else c["dol"]
        if dd.year != 2026:
            continue
        cs.append(c)
    res = {f: [0, 0.0] for f in D["names"]}
    pay = (lambda c: c["bpay"] + c["icc"]) if route == "with_icc" else (lambda c: c["bpay"])
    if route in ("naive", "utc", "with_icc"):
        for c in cs:
            if pay(c) > 0:
                res[c["fips"]][0] += 1
                res[c["fips"]][1] += pay(c)
        return {f: (v[0], v[1]) for f, v in res.items()}
    if route in ("bdol_latest", "bdol_sum"):
        grp = defaultdict(list)
        for c in cs:
            if c["bpay"] > 0:
                grp[(c["bid"], c["dol"])].append(c)
        for k, g in grp.items():
            res[g[0]["fips"]][0] += 1
            res[g[0]["fips"]][1] += (max(g, key=lambda c: c["reported"])["bpay"] if route == "bdol_latest"
                                     else sum(c["bpay"] for c in g))
        return {f: (v[0], v[1]) for f, v in res.items()}
    if route == "validity":
        for c in cs:
            p = pols.get(c["policy"])
            if c["bpay"] > 0 and p is not None and in_force(p, c["dol"]):
                res[c["fips"]][0] += 1
                res[c["fips"]][1] += c["bpay"]
        return {f: (v[0], v[1]) for f, v in res.items()}
    # the golden and chain_latest: a claim entered under a policy not yet in force on its date of loss continues the
    # claim on the policy that policy replaced, where one exists for the same building and date of loss
    merged = {}
    for c in cs:
        p = pols.get(c["policy"])
        key = c["number"]
        if p is not None and not in_force(p, c["dol"]) and p["prior"]:
            twin = [t for t in cs if t["policy"] == p["prior"] and t["bid"] == c["bid"] and t["dol"] == c["dol"]]
            if twin:
                key = twin[0]["number"]
        merged.setdefault(key, []).append(c)
    for k, g in merged.items():
        if route == "chain_sum":
            b = sum(c["bpay"] for c in g)
        else:
            b = max(g, key=lambda c: c["reported"])["bpay"]     # the record continuing the claim carries its payments
        if b > 0:
            res[g[0]["fips"]][0] += 1
            res[g[0]["fips"]][1] += b
    return {f: (v[0], v[1]) for f, v in res.items()}


# ---------------------------------------------------------------------------------------------- ask B, the pipeline
B_ROUTES = ("golden", "status", "status_true_share", "inspection_shown_share", "lead_county", "with_withdrawn")


def register(target):
    if ("register", target) in _CACHE:
        return _CACHE[("register", target)]
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, FILES["register"]), read_only=True, data_only=True)

    def sheet(name):
        it = wb[name].iter_rows(values_only=True)
        head = next(it)
        return [dict(zip(head, r)) for r in it]
    projects = {r["project_number"]: r for r in sheet("Projects")}
    props = {}
    for r in sheet("Properties"):
        props[r["property_id"]] = dict(project=r["project_number"], measure=r["measure"], cost=r["approved_cost"],
                                       share=r["federal_share"], status=r["property_status"], community=r["community_number"],
                                       status_date=_d(r["status_date"]))
    final = {}
    for r in sheet("Inspections"):
        if r["inspection"] == "Final" and r["result"] == "Pass":
            final[r["property_id"]] = _d(r["inspection_date"])
    out = dict(projects=projects, props=props, final=final)
    _CACHE[("register", target)] = out
    return out


def _d(v):
    if v is None:
        return None
    return v.date() if isinstance(v, dt.datetime) else v


def pipeline(target, route="golden"):
    """Each county's buildings in elevation or acquisition projects not completed on 30 September 2026 and the
    federal share obligated to them: {fips: (buildings, dollars)}."""
    D = load(target)
    R = register(target)
    lead = {}
    for n, q in R["projects"].items():
        nm = q["applicant"].replace(" County", "")
        lead[n] = [f for f, v in D["names"].items() if v == nm][0]
    res = {f: [0, 0] for f in D["names"]}
    for pid, p in R["props"].items():
        q = R["projects"][p["project"]]
        if route in ("status", "status_true_share"):
            pending = p["status"] in ("Approved", "Under construction")
        elif route == "with_withdrawn":
            pending = R["final"].get(pid) is None or R["final"][pid] > AS_OF
        else:
            pending = p["status"] != "Withdrawn" and (R["final"].get(pid) is None or R["final"][pid] > AS_OF)
        if not pending:
            continue
        true_share = int(round(p["cost"] * q["federal_cost_share_pct"] / 100.0))
        share = p["share"] if route in ("status", "inspection_shown_share") else true_share
        f = lead[p["project"]] if route == "lead_county" else D["comm"][p["community"]]
        res[f][0] += 1
        res[f][1] += share
    return {f: (v[0], v[1]) for f, v in res.items()}
