"""Everything the pack and the golden are cut from, computed once: the truth, the census's identifiers, the miles, the
laboratory's specimens, the crash records system's reports, and every graded figure from the generator's own state.
The CSV writers are here; the documents and workbooks are in docs.py."""
import csv
import io

import census as C
import crs as R
import geo as G
import lab as L
import methods as M
import truth as T
import vmt as V
import world as W


def everything():
    crashes = T.build()
    order, numbers = C.assign(crashes)
    obs = T.observe(crashes)
    vmt3, bounds = V.place(obs)
    tab = V.tables(vmt3)
    vmt = {f: sum(V.annual(tab, f).values()) for f in vmt3}
    arrests = L.arrests(order, vmt)
    kits = L.specimens(order, arrests, numbers)
    lab_rows = L.rows(kits)
    xs = R.universe(order)
    rep_rows, unit_rows = R.reports(xs, numbers)
    x = dict(crashes=crashes, order=order, obs=obs, vmt=vmt, tab=tab, bounds=bounds, arrests=arrests, kits=kits,
             lab_rows=lab_rows, crs=xs, rep_rows=rep_rows, unit_rows=unit_rows)
    x["census23"] = C.rows_2023(order)
    x["census25"] = C.rows_2425(order)
    x["prelim"] = C.prelim_2026_rows()
    x["fig"] = figures(x)
    return x


def ask_a(arrests, attribute=None):
    """Each county's 2025 impaired-driving arrests with a blood specimen at the laboratory and the per cent whose first
    specimen's whole-blood ethanol was .15 or more. attribute(arrest) gives the county (the arrest's own by default)."""
    n = {c["fips"]: 0 for c in W.COUNTIES}
    hi = dict(n)
    for a in arrests:
        if a.kind != "DUI" or a.when.year != 2025:
            continue
        f = attribute(a) if attribute else a.fips
        n[f] += 1
        if not a.drug_only and not a.cancel and a.bac >= 0.150:
            hi[f] += 1
    return {f: (n[f], 100.0 * hi[f] / n[f]) for f in n}


def figures(x):
    """Every graded figure and the call, from the generator's state."""
    obs, vmt = x["obs"], x["vmt"]
    g = M.route(obs, "G")
    rates = M.rate(g, vmt)
    a = ask_a(x["arrests"])
    b = R.ask_b(x["crs"])
    rows = []
    for c in W.COUNTIES:
        f = c["fips"]
        rows.append(dict(fips=f, county=c["name"], deaths=g.get(f, 0.0), vmt=vmt[f], rate=rates[f],
                         high=rates[f] >= W.THRESHOLD, arrests=a[f][0], pct15=a[f][1], crashes=b[f]))
    catch = M.catch_rates(obs)
    return dict(rows=rows, high=[r["county"] for r in rows if r["high"]], catch=catch)


# ---------------------------------------------------------------------------------------------------------------
def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


def site_rows():
    return [[s.code, s.name, s.kind, s.city, s.fips] for s in sorted(G.SITES, key=lambda s: s.code)]


SITE_COLS = ["site_code", "facility", "facility_type", "city", "county_fips"]


INDEX_COLS = ["file_name", "provided_by", "as_of", "contents"]


def index_rows():
    """The Center's index of the certification package: each file, who provided it, its date, what it holds."""
    C, L, D, M = W.CENTER_SHORT, W.LAB, "%s, Transportation Planning Division" % W.DOT, \
        "Department of Revenue, Motor Vehicle Division"
    F = W.FILES
    rows = [
        (F["guidelines"], W.GHSO, "2027-02-09", "FY2028 County Impaired Driving Task Force Grants, program guidelines"),
        (F["manual"], C, "2024-03-15", "Fatal Crash Census reference manual, 2024 edition"),
        (F["crash23"], C, "2025-02-27", "Fatal Crash Census, 2023 crash file as closed (2011 report form layout)"),
        (F["person23"], C, "2025-02-27", "Fatal Crash Census, 2023 person file as closed (2011 report form layout)"),
        (F["crash2425"], C, "2027-02-25", "Fatal Crash Census, 2024 and 2025 crash file as closed (2024 report form "
                                          "layout)"),
        (F["person2425"], C, "2027-02-25", "Fatal Crash Census, 2024 and 2025 person file as closed (2024 report "
                                           "form layout)"),
        (F["prelim26"], C, "2027-03-01", "Fatal Crash Census, 2026 preliminary crash file"),
        (F["agencies"], C, "2027-01-04", "Agency directory: agency numbers, former codes, State Patrol posts"),
        (F["reports"], C, "2027-03-08", "Crash Records System, 2025 injury and fatal crash reports, every version"),
        (F["units"], C, "2027-03-08", "Crash Records System, units on the 2025 report versions"),
        (F["crs_notes"], C, "2027-03-08", "Crash Records System extract notes"),
        (F["vmt"], D, "2027-01-30", "County daily vehicle miles traveled by functional class, 2023 to 2025"),
        (F["lab"], L, "2027-03-12", "Specimen extract, kits received 1 January 2023 to 15 January 2026"),
        (F["lab_notes"], L, "2027-03-12", "Specimen extract field notes"),
        (F["sites"], L, "2027-03-12", "Collection site codes"),
        (F["lab_annual"], L, "2027-03-06", "Annual Report 2025, statistical tables"),
        (F["licensed"], M, "2026-01-15", "Licensed drivers by county of residence, 31 December 2025"),
    ]
    return [list(r) for r in rows]
