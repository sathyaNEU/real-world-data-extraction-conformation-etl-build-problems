"""Assemble the evidence pack: the world, the League's files, the vendor's files, the club's files, the documents and
the close-file index, every file stamped with the pull time."""
from __future__ import annotations

import os

import common as K
import docs as DOC
import names as NM
import records as R
import world as WD


def build_world():
    L = WD.run()
    R.club_people(L)            # the club's pitching staffs exist before the league is named
    NM.rename_league(L, WD.DESIGNED, K.rng("league names"))
    return L


def write_pack(L, out):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    rows = {}
    ids = R.club_ids()
    n, lc = R.write_legacy(L, out)
    rows[R.F_LEGACY] = n
    rows[R.F_BAT] = R.write_platform(L, out, ids)
    rows[R.F_XWALK] = R.write_crosswalk(L, out, lc)
    rows[R.F_CLUBS] = R.write_clubs(out, ids)
    rows[R.F_CAL] = R.write_calendar(out)
    rows[R.F_TRANS] = R.write_transactions(L, out, ids)
    rows[R.F_ILREP] = R.write_il_report(L, out)
    rows[R.F_SCHED27] = R.write_schedule_2027(out, ids)
    n, hv = R.write_depth_charts(L, out)
    rows[R.F_DC] = n
    rows[R.F_PROJ] = R.write_projections(L, out, hv)
    rows[R.F_DC27] = R.write_depth_chart_2027(L, out)
    n, legacy, new, people, migrated = R.write_payroll(L, out)
    rows[R.F_PAY] = n
    rows[R.F_HRIS] = R.write_hris_map(L, out, legacy, new, migrated)
    rows[R.F_CODES] = R.write_earning_codes(out)
    rows[R.F_REG] = R.write_register(L, out, legacy, new, people, migrated)
    DOC.write_fin14(out)
    DOC.write_working_paper(out)
    DOC.write_term_sheets(L, out)
    DOC.write_il_rules(out)
    DOC.write_feed_notes(out)
    DOC.write_manifest(out, rows)
    t = K.PULL_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (t, t))
    L.rows = rows
    L.ids = ids
    return L
