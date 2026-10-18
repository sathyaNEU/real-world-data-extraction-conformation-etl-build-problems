"""Writes the data files of target/ from the simulated seasons (documents are in docs.py)."""
import csv
import datetime as dt
import io
import os
import sqlite3

import numpy as np

import world as W
import sim
from records import route_list, BLOCKS

UTC = sim.UTC
ROME = sim.ROME


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def iso_utc(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def dep_time_of(L, i):
    times = W.OUT_TIMES[L.freq] if L.outbound_ else W.RET_TIMES[L.freq]
    return times[L.rot[i]]


# ------------------------------------------------------------------ the new RM system's S25 booking build
def rm_build_s25(S, path):
    legs = S.legs("S25")
    rows = []
    for L in legs:
        snap = L.snapshot(W.DCP_NEW)
        for i in range(L.n):
            so = L.sellout_local(i)
            rows.append((L.dep_date[i], dep_time_of(L, i), L.flt[i], L, i, snap[i], so))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    header = (["extract_ts", "leg_key", "flight_no", "dep_date", "std_local", "orig", "dest", "equip", "cap",
               "sold_out_utc"] + ["bkd_d%03d" % t for t in W.DCP_NEW])
    out = []
    for k, (d, std, flt, L, i, snap, so) in enumerate(rows):
        key = "%s%s%04d" % (d.strftime("%y%m%d"), std.replace(":", ""), flt)
        out.append(["2025-12-01T04:38:12Z", key, flt, d.isoformat(), std, L.orig, L.dest, L.equip_code(i),
                    int(L.seats[i]), iso_utc(so) if so is not None else ""] + [int(x) for x in snap])
    _w(path, header, out)
    return len(out)


# ------------------------------------------------------------------ the old RM system's S24 archive
def ym3_archive_s24(S, path):
    """The archive, keyed by YM3's leg id (departure date yymmdd and flight number)."""
    from fileio import binary_is_clean
    n = _ym3_write(S, path)
    assert binary_is_clean(path), "the archive's bytes spell a swept token"
    return n


def _ym3_write(S, path):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.executescript("""
        PRAGMA page_size=4096;
        CREATE TABLE ym3_extract (k TEXT PRIMARY KEY, v TEXT);
        CREATE TABLE legs (leg_id TEXT PRIMARY KEY, flt INTEGER, dep_dt TEXT, std TEXT, orig TEXT, dest TEXT,
                           typ TEXT, cap INTEGER) WITHOUT ROWID;
        CREATE TABLE bkg (leg_id TEXT, dcp INTEGER, bkd INTEGER, avl TEXT, PRIMARY KEY (leg_id, dcp)) WITHOUT ROWID;
        CREATE TABLE flown (leg_id TEXT PRIMARY KEY, pax INTEGER, inf INTEGER) WITHOUT ROWID;
    """)
    cur.executemany("INSERT INTO ym3_extract VALUES (?, ?)", [
        ("system", "YM3 yield management, leg inventory archive"),
        ("season", "IS24 (31/03/2024 - 26/10/2024)"),
        ("extracted", "2024-11-18 22:05"),
        ("dcp_set", ",".join(str(t) for t in W.DCP_OLD)),
        ("note", "archive frozen at the migration to the new revenue management system; legs as flown"),
    ])
    legs = S.legs("S24")
    rows = []
    for L in legs:
        snap = L.snapshot(W.DCP_OLD)
        for i in range(L.n):
            rows.append((L.dep_date[i], dep_time_of(L, i), L.flt[i], L, i, snap[i]))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    leg_rows, bkg_rows, flown_rows = [], [], []
    for k, (d, std, flt, L, i, snap) in enumerate(rows):
        lid = "%s%04d" % (d.strftime("%y%m%d"), flt)
        leg_rows.append((lid, flt, d.strftime("%d/%m/%Y"), std.replace(":", ""), L.orig, L.dest, L.equip_code(i),
                         int(L.seats[i])))
        for t, b in zip(W.DCP_OLD, snap):
            bkg_rows.append((lid, t, int(b), "C" if b >= L.seats[i] else "O"))
        flown_rows.append((lid, int(L.flown[i] + L.inf[i]), int(L.inf[i])))
    cur.executemany("INSERT INTO legs VALUES (?,?,?,?,?,?,?,?)", leg_rows)
    cur.executemany("INSERT INTO bkg VALUES (?,?,?,?)", bkg_rows)
    cur.executemany("INSERT INTO flown VALUES (?,?,?)", flown_rows)
    con.commit()
    cur.execute("VACUUM")
    con.close()
    return len(leg_rows), len(bkg_rows)


# ------------------------------------------------------------------ departure control close-out, S25
def tails_for(S):
    """The registrations behind the DCS file's tail column: one register, every mark unique across types."""
    letters = "ABCDEFGHJKLMNPRSTUVWZ"
    rng = sim.stream("tails")
    used = set()
    regs = {}
    for typ, n in (("319", 24), ("320", 5), ("32N", 14), ("321", 6)):
        out = []
        while len(out) < n:
            reg = "I-N" + "".join(letters[int(x)] for x in rng.integers(0, len(letters), 3))
            if reg in used or reg.startswith("I-NQA"):
                continue
            used.add(reg)
            out.append(reg)
        regs[typ] = sorted(out)
    return regs


def dcs_close_s25(S, path, regs):
    legs = S.legs("S25")
    rows = []
    for L in legs:
        for i in range(L.n):
            rows.append((L.dep_date[i], dep_time_of(L, i), L.flt[i], L, i))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = []
    for d, std, flt, L, i in rows:
        typ = L.equip_code(i)
        pool = regs[typ]
        tail = pool[(flt * 7 + d.toordinal()) % len(pool)]
        out.append([flt, d.isoformat(), L.orig, L.dest, std, tail, typ, int(L.seats[i]), int(L.sold[i]),
                    int(L.flown[i]), int(L.inf[i]), int(L.noshow[i])])
    _w(path, ["flight_no", "dep_date", "orig", "dest", "std_local", "tail", "equip", "seats", "pax_booked",
              "pax_flown", "inf_flown", "no_show"], out)
    return len(out)


# ------------------------------------------------------------------ the booking engines' refusals log
def refusals_log(S, path):
    ev = []
    for L in S.legs("S25"):
        ev.extend(sim.turnaway_events(L, L.flt))
    ev.sort(key=lambda e: (e[0], e[1], e[2], e[3]))
    # contact-centre call references run in call order; agency booking references are unique per booking
    cc_ref = {}
    gds_ref = {}
    used = set()
    rng = sim.stream("references")
    for e in ev:
        ch, pid = e[1], e[10]
        if ch == "CC" and pid not in cc_ref:
            cc_ref[pid] = "CC%07d" % (4317000 + len(cc_ref) * 3 + int(rng.integers(0, 3)))
        elif ch == "GDS" and pid not in gds_ref:
            ref = e[2]
            while ref in used:
                ref = "".join(sim._SESS[int(x)] for x in rng.integers(10, len(sim._SESS), 6))
            used.add(ref)
            gds_ref[pid] = ref
    out = []
    truth = []
    for k, e in enumerate(ev):
        t, ch, sess, flt, dep, o, d, fam, pax, after, pid, size, lo, ld = e
        sess = cc_ref.get(pid, sess) if ch == "CC" else (gds_ref.get(pid, sess) if ch == "GDS" else sess)
        eid = 51000000 + 3 * k + (flt % 3)
        out.append([eid, iso_utc(t), ch, sess, flt, dep.isoformat(), o, d, fam, pax, "NO_AVAIL"])
        truth.append((eid, after, pid, size, lo, ld))
    _w(path, ["event_id", "logged_utc", "channel", "session_ref", "flight_no", "dep_date", "orig", "dest",
              "fare_family", "pax", "result"], out)
    return len(out), truth, ev
