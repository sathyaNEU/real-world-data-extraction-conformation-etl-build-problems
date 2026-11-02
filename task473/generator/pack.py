"""Everything the pack and the golden are cut from, computed once: the truth, the census's identifiers, the miles, the
impaired-driving arrests and the county courts' cases, and every graded figure from the generator's own state. The CSV
writers are here; the documents and workbooks are in docs.py."""
import csv

import census as C
import court as CT
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
    cases = CT.cases(arrests, vmt)
    x = dict(crashes=crashes, order=order, obs=obs, vmt=vmt, tab=tab, bounds=bounds, arrests=arrests, cases=cases,
             court_rows=CT.rows(cases))
    x["census23"] = C.rows_2023(order)
    x["census25"] = C.rows_2425(order)
    x["prelim"] = C.prelim_2026_rows()
    x["fig"] = figures(x)
    return x


def figures(x):
    """Every graded figure and the call, from the generator's state."""
    obs, vmt = x["obs"], x["vmt"]
    g = M.route(obs, "G")
    rates = M.rate(g, vmt)
    a = CT.ask(x["cases"])
    rows = []
    for c in W.COUNTIES:
        f = c["fips"]
        rows.append(dict(fips=f, county=c["name"], deaths=g.get(f, 0.0), vmt=vmt[f], rate=rates[f],
                         high=rates[f] >= W.THRESHOLD, prosecuted=a[f][0], pct_conv=a[f][1]))
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
