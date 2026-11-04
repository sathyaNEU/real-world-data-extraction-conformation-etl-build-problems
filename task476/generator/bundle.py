"""Read the pack under target/ the way a solver must: every figure the golden, the checks and the ceiling use comes
from these parsers, never from the simulation."""
import csv
import os
import re
import sqlite3

import pdfplumber
from openpyxl import load_workbook

import world as W


def _p(target, key):
    return os.path.join(target, W.FILES[key])


def _rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def species(target):
    rows = _rows(_p(target, "species"))
    return {int(r["fia_code"]): r for r in rows}


def register(target):
    wb = load_workbook(_p(target, "register"), read_only=True)
    ws = wb["Plots"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    out = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        if d["Plot"] is None:
            continue
        out[int(d["Plot"])] = d
    return out


def cond_stand(reg, plot, cond):
    r = reg[plot]
    return r["Stand"] if int(cond) == 1 else r["Cond 2 stand"]


def areas(reg):
    """Acres of plot condition mapped to each stand."""
    a = {}
    for p, r in reg.items():
        a[r["Stand"]] = a.get(r["Stand"], 0.0) + W.PLOT_AC * float(r["Cond 1 share"])
        if r["Cond 2 stand"]:
            a[r["Cond 2 stand"]] = a.get(r["Cond 2 stand"], 0.0) + W.PLOT_AC * float(r["Cond 2 share"])
    return a


def database(target):
    con = sqlite3.connect("file:%s?mode=ro" % _p(target, "db"), uri=True)
    cur = con.cursor()
    trees = {r[0]: dict(tag=r[0], plot=r[1], spp=r[2], az=r[3], dist=r[4], first=r[5])
             for r in cur.execute("SELECT tag, plot_no, spp, azimuth, dist_ft, first_cycle FROM tree")}
    live21 = {}
    for tag, dbh, status, cond in cur.execute(
            "SELECT tag, dbh_in, status, cond FROM tree_meas WHERE cycle_yr = 2021"):
        if status == "L":
            live21[tag] = dict(trees[tag], dbh21=dbh, cond=cond)
    nmeas = cur.execute("SELECT COUNT(*) FROM tree_meas").fetchone()[0]
    con.close()
    return trees, live21, nmeas


def remeasurement(target):
    out = []
    for r in _rows(_p(target, "t2026")):
        out.append(dict(plot=int(r["plot_id"]), tag=int(r["tag"]), fia=int(r["species_fia"]),
                        dbh=float(r["dbh_in"]) if r["dbh_in"] else None,
                        az=int(r["azimuth_deg"]) if r["azimuth_deg"] else None,
                        dist=float(r["dist_ft"]) if r["dist_ft"] else None, status=r["status"], cond=int(r["cond_id"]),
                        merch=int(r["merch_ht_ft"]) if r["merch_ht_ft"] else None,
                        cull=int(r["cull_pct"]) if r["cull_pct"] else None, damage=r["damage"], crew=r["crew"],
                        date=r["meas_date"]))
    return out


def revisit(target):
    return {(int(r["plot_id"]), int(r["tag"])): int(r["merch_ht_ft"]) for r in _rows(_p(target, "revisit"))}


def volume_table(target):
    """Table 1 of the field manual: tens of board feet by 2-inch DBH class and 16-foot logs."""
    txt = pdf_text(_p(target, "manual"))
    lines = txt.splitlines()
    head = next(l for l in lines if l.strip().startswith("DBH ") and "1.5" in l)
    logs = [float(v) for v in head.split()[1:]]
    tab = {}
    for l in lines:
        m = re.match(r"^\s*(\d{2})((?:\s+\d+){%d})\s*$" % len(logs), l)
        if m:
            vals = [int(v) for v in m.group(2).split()]
            tab[int(m.group(1))] = dict(zip(logs, vals))
    return tab


def load(target):
    trees, live21, nmeas = database(target)
    d = dict(target=target, trees=trees, live21=live21, nmeas=nmeas, t26=remeasurement(target), rev=revisit(target),
             reg=register(target), spp=species(target), vol=volume_table(target),
             stands=_rows(_p(target, "stands")))
    d["areas"] = areas(d["reg"])
    return d
