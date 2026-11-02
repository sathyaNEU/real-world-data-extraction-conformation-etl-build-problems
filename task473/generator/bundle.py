"""Reading the cut pack the way a solver must: every file through its own format, no generator state. The census in
both layouts, the agency directory, the DOT's miles, the county courts' case extract, the documents' text. verify.py
and checks.py read the bundle only through here."""
import csv
import datetime as dt
import os
import subprocess
import zipfile
from zoneinfo import ZoneInfo

CENTRAL = ZoneInfo("America/Chicago")
NAMES = {}


def path(target, name):
    return os.path.join(target, name)


def find(target, prefix):
    hits = [f for f in os.listdir(target) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(target, hits[0])


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdf_text(p):
    return subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True, check=True).stdout


def xlsx_sheets(p):
    from openpyxl import load_workbook
    wb = load_workbook(p, read_only=True, data_only=True)
    return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


# ------------------------------------------------------------------------------------------------- the directory
def directory(target):
    sh = xlsx_sheets(find(target, "fcc_agency_directory"))
    rows = sh["Agencies"]
    head = rows[0]
    ag = [dict(zip(head, r)) for r in rows[1:]]
    posts = [dict(zip(sh["State Patrol posts"][0], r)) for r in sh["State Patrol posts"][1:]]
    by_id = {a["agency_id"]: a for a in ag}
    by_old = {str(a["former_code"]): a for a in ag if a["former_code"] not in (None, "")}
    counties = {}
    for a in ag:
        counties[str(a["county_fips"])] = a["county"]
    return dict(agencies=by_id, by_old=by_old, posts={int(p["post"]): p for p in posts}, counties=counties)


def complete_agencies(dr):
    """Manual 4.2: the State Patrol (its posts) and the Corwin County and Ossian County sheriffs."""
    out = set()
    posts = {p["agency_id"] for p in dr["posts"].values()}
    for aid, a in dr["agencies"].items():
        if a["agency_type"] == "State Patrol" and aid in posts:
            out.add(aid)
        if a["agency_type"] == "Sheriff" and a["county"] in ("Corwin", "Ossian"):
            out.add(aid)
    return out


# ------------------------------------------------------------------------------------------------- the census
def codes(target):
    """The 2011 report form's code table: {element: {code: label}}."""
    out = {}
    for r in read_csv(find(target, "fcc_2011_form_codes")):
        out.setdefault(r["element"], {})[r["code"]] = r["label"]
    return out


def census(target, dr=None):
    """Every 2023 to 2025 crash as {case, year, date, fips, agency, report, deaths, persons: [...]}, both layouts
    read into one structure (the 2011 form's codes through its code table); agencies on the 2024 numbers."""
    dr = dr or directory(target)
    cd = codes(target)
    out = []
    c23 = read_csv(find(target, "fcc_2023_crash"))
    p23 = read_csv(find(target, "fcc_2023_person"))
    per = {}
    for r in p23:
        per.setdefault(r["CASE_NUM"], []).append(r)
    for r in c23:
        m, d, y = (int(v) for v in r["ACC_DATE"].split("/"))
        date = dt.date(y, m, d)
        ag = dr["by_old"][r["AGCY"]]["agency_id"]
        ps = []
        for q in per.get(r["CASE_NUM"], []):
            role = cd["PER_TYP"][q["PER_TYP"]].lower()
            dd = None
            if q["DTH_DATE"]:
                mm, dd_, yy = (int(v) for v in q["DTH_DATE"].split("/"))
                dd = dt.date(yy, mm, dd_)
            test = cd["ALC_TST"][q["ALC_TST"]]
            tested = test != "NOT TESTED"
            ps.append(dict(role=role, unit=int(q["VEH_NUM"]), killed=cd["INJ"][q["INJ"]] == "FATAL INJURY", death=dd,
                           identified=not (role == "driver" and cd["HIT_RUN"].get(q["HIT_RUN"]) == "YES"),
                           tested=tested, test=q["ALC_TST"], bac=int(q["ALC_RES"]) / 1000.0 if tested else None,
                           arrested=cd["DWI_ARR"].get(q["DWI_ARR"]) == "YES", body=q["BODY"]))
        out.append(dict(case=r["CASE_NUM"], year=y, date=date, fips=r["CNTY"], agency=ag, report=r["RPT_NUM"],
                        deaths=sum(1 for p in ps if p["killed"]), persons=ps, time=r["ACC_TIME"]))
    c25 = read_csv(find(target, "fcc_2024_2025_crash"))
    p25 = read_csv(find(target, "fcc_2024_2025_person"))
    per = {}
    for r in p25:
        per.setdefault(r["crash_id"], []).append(r)
    for r in c25:
        date = dt.date.fromisoformat(r["crash_date"])
        ps = []
        for q in per.get(r["crash_id"], []):
            role = q["person_type"].lower()
            tested = q["alcohol_test"] in ("BLOOD", "VITREOUS")
            ps.append(dict(role=role, unit=int(q["unit"]), killed=q["injury"] == "K",
                           death=dt.date.fromisoformat(q["date_of_death"]) if q["date_of_death"] else None,
                           identified=not (role == "driver" and q["hit_and_run"] == "Y"), tested=tested,
                           test=q["alcohol_test"], bac=float(q["alcohol_result"]) if tested else None,
                           arrested=q["arrested_at_scene"] == "Y", body=q["unit_type"]))
        out.append(dict(case=r["crash_id"], year=date.year, date=date, fips=r["county_fips"], agency=r["agency_id"],
                        report=r["report_number"], deaths=sum(1 for p in ps if p["killed"]), persons=ps,
                        time=r["crash_time"], road=r["road_name"]))
    return out


def observed(crashes, complete, roles=("driver",), unidentified=False, late_deaths=False):
    """The structure methods.py reads: each crash's drivers with killed, identified, tested, bac, arrested and
    complete. The keywords read the census another way: other person types as drivers, the unidentified drivers
    as untested ones, a death recorded after 30 days as a death."""
    obs = []
    for cr in crashes:
        ds = []
        for p in cr["persons"]:
            if p["role"] not in roles:
                continue
            ident = p["identified"] or unidentified
            ds.append(dict(killed=p["killed"], identified=ident, tested=p["tested"] and p["identified"],
                           bac=p["bac"], arrested=p["arrested"],
                           complete=(not p["killed"]) and cr["agency"] in complete,
                           agency="SP" if cr["agency"].startswith("SP") else cr["agency"]))
        deaths = cr["deaths"] + (sum(1 for p in cr["persons"] if p["death"] and not p["killed"]) if late_deaths else 0)
        obs.append(dict(fips=cr["fips"], year=cr["year"], deaths=deaths, drivers=ds, cid=cr["case"]))
    return obs


# ------------------------------------------------------------------------------------------------- the miles
def dvmt_sheets(target):
    """Each year's DVMT sheet from its header row on (the sheet's title row above it carries the unit)."""
    sh = xlsx_sheets(find(target, "dot_county_dvmt"))
    out = {}
    for y in (2023, 2024, 2025):
        rows = sh["DVMT %d" % y]
        k = next(i for i, r in enumerate(rows) if r and r[0] == "County FIPS")
        out[y] = rows[k:]
    return out


def vmt(target, days=None):
    """Each county's 2023 to 2025 vehicle miles: each year's DVMT (thousands a day, all classes) times its days."""
    days = days or {2023: 365, 2024: 366, 2025: 365}
    out = {}
    for y, rows in dvmt_sheets(target).items():
        head = rows[0]
        for r in rows[1:]:
            rec = dict(zip(head, r))
            if not rec["County FIPS"]:
                continue
            tot = sum(float(rec[h]) for h in head[2:-1])
            out[str(rec["County FIPS"])] = out.get(str(rec["County FIPS"]), 0.0) + tot * 1000.0 * days[y]
    return out


def golden_g(obs, miles):
    """The golden completion on its own code path: the catch rate at each band where every surviving driver is
    tested, each arrest-only positive counted as one over it, the excess spread over the county's untested
    surviving drivers, each crash's deaths times the chance a driver was at .08 or more."""
    rows = [d for cr in obs for d in cr["drivers"] if d["complete"] and d["tested"] and not d["killed"]]
    catch = {}
    for b, lo, hi in ((0, 0.080, 0.150), (1, 0.150, 9.9)):
        r = [d for d in rows if lo <= d["bac"] < hi]
        catch[b] = sum(1 for d in r if d["arrested"]) / float(len(r))
    missed, untested = {}, {}
    for cr in obs:
        for d in cr["drivers"]:
            if d["killed"] or d["complete"] or not d["identified"]:
                continue
            if d["tested"] and d["bac"] >= 0.080:
                b = 0 if d["bac"] < 0.150 else 1
                missed[cr["fips"]] = missed.get(cr["fips"], 0.0) + 1.0 / catch[b] - 1.0
            elif not d["tested"]:
                untested[cr["fips"]] = untested.get(cr["fips"], 0) + 1
    q = {f: missed.get(f, 0.0) / n for f, n in untested.items()}
    deaths = {}
    for cr in obs:
        ds = [d for d in cr["drivers"] if d["identified"]]
        if any(d["tested"] and d["bac"] >= 0.080 for d in ds):
            p = 1.0
        else:
            keep = 1.0
            for d in ds:
                if not d["tested"]:
                    keep *= 1.0 - q.get(cr["fips"], 0.0)
            p = 1.0 - keep
        deaths[cr["fips"]] = deaths.get(cr["fips"], 0.0) + cr["deaths"] * p
    rates = {f: deaths.get(f, 0.0) / miles[f] * 1e8 for f in miles}
    return dict(catch=catch, missed=missed, untested=untested, deaths=deaths, rates=rates)


def backtest(obs):
    """The State Patrol posts test every surviving driver, so each post's arrests can be completed as if it were an
    arrest-only agency and checked against its own unarrested drivers at .08 or more. Each post is held out: the
    catch rates (and the one unarrested share) come from every other complete agency. Returns each post's actual
    count, the catch-rate completion and the pooled share's, and the two root mean squared errors."""
    rows = [(cr["fips"], d) for cr in obs for d in cr["drivers"]
            if d["complete"] and d["tested"] and not d["killed"]]
    out = {}
    for f in sorted({f for f, d in rows if d["agency"] == "SP"}):
        mine = [d for g, d in rows if g == f and d["agency"] == "SP"]
        rest = [d for g, d in rows if not (g == f and d["agency"] == "SP")]
        catch = {}
        for b, lo, hi in ((0, 0.080, 0.150), (1, 0.150, 9.9)):
            r = [d for d in rest if lo <= d["bac"] < hi]
            catch[b] = sum(1 for d in r if d["arrested"]) / float(len(r))
        un = [d for d in rest if not d["arrested"]]
        share = sum(1 for d in un if d["bac"] >= 0.080) / float(len(un))
        actual = sum(1 for d in mine if not d["arrested"] and d["bac"] >= 0.080)
        ipw = sum(1.0 / catch[0 if d["bac"] < 0.150 else 1] - 1.0 for d in mine if d["arrested"] and d["bac"] >= 0.080)
        pooled = share * sum(1 for d in mine if not d["arrested"])
        out[f] = (actual, ipw, pooled)
    rmse = lambda k: (sum((v[k] - v[0]) ** 2 for v in out.values()) / len(out)) ** 0.5
    return out, rmse(1), rmse(2)


# ------------------------------------------------------------------------------------------------- the courts
def court(target):
    return read_csv(find(target, "aoc_criminal_traffic_cases"))


def impaired(r):
    """an impaired-driving charge, by the charge's own words"""
    return "UNDER THE INFLUENCE" in r["lead_charge"]


def prosecutions(rows, how="relation", year=2025, agency=True, slack=0, by="offense", same_charge=False):
    """The county courts' impaired-driving prosecutions of the year's offenses as lists of cases. how: "relation" (a
    case dismissed on the day its court opened another for the same offense date and arresting agency is one
    prosecution with that case; agency=False drops the agency, slack allows that many days), "cases" (each case its
    own), "cell" (one per court, offense date and agency), "later" (a dismissed case one prosecution with any case of its
    court and offense date opened on or after its dismissal). same_charge=True links only cases with one lead charge.
    by="filed" reads the year on the filing date."""
    col = "offense_date" if by == "offense" else "filed_date"
    cs = [r for r in rows if impaired(r) and r[col][:4] == str(year)]
    if how == "cases":
        return [[r] for r in cs]
    cells = {}
    for r in cs:
        cells.setdefault((r["county_fips"], r["offense_date"]) + ((r["arresting_agency"],) if agency else ()),
                         []).append(r)
    if how == "cell":
        return list(cells.values())
    out = []
    for g in cells.values():
        parent = list(range(len(g)))

        def root(i):
            while parent[i] != i:
                i = parent[i]
            return i
        for i, x in enumerate(g):
            if x["disposition"] != "DISMISSED":
                continue
            for j, y in enumerate(g):
                gap = (dt.date.fromisoformat(y["filed_date"]) - dt.date.fromisoformat(x["disposition_date"])).days
                near = gap >= 0 if how == "later" else abs(gap) <= slack
                if j != i and near and (not same_charge or y["lead_charge_code"] == x["lead_charge_code"]):
                    parent[root(j)] = root(i)
        groups = {}
        for i, r in enumerate(g):
            groups.setdefault(root(i), []).append(r)
        out += list(groups.values())
    return out


GUILTY = ("GUILTY PLEA", "GUILTY VERDICT")


def convicted(pros, guilty=GUILTY, impaired_only=True, last=True):
    """the prosecution's last case convicted on an impaired-driving charge (guilty widens the dispositions read as a
    conviction, impaired_only=False any convicted charge, last=False any of its cases)"""
    cases = [max(pros, key=lambda r: (r["filed_date"], r["case_number"]))] if last else pros
    return any(r["disposition"] in guilty and ("UNDER THE INFLUENCE" in r["convicted_charge"] or not impaired_only)
               for r in cases)


def ask_court(target_or_rows, how="relation", conv=None, **kw):
    rows = court(target_or_rows) if isinstance(target_or_rows, str) else target_or_rows
    out = {}
    for g in prosecutions(rows, how, **kw):
        f = g[0]["county_fips"]
        n, h = out.get(f, (0, 0))
        out[f] = (n + 1, h + (conv or convicted)(g))
    return {f: (n, 100.0 * h / n) for f, (n, h) in out.items()}


def golden_csv(gdir):
    return read_csv(find(gdir, "county_impaired_driving_rates"))
