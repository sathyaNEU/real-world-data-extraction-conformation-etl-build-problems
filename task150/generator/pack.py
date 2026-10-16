"""Assemble the evidence pack: the world, the records, the capacity report (rated capacities from Facilities' room
plans), the fall 2026 sections and preschool files, the policy, the notes, the two unused files and the manifest."""
from __future__ import annotations

import os

import numpy as np

import asks as AS
import calc
import common as K
import docs as DOC
import records as R
import world as WD


def build_world():
    return WD.simulate()


def centred_capacities(out):
    """Facilities' rated capacities, fixed so that each school's five-year excess under the gross-flow constructions
    sits mid-bin (the world's target excess; see the design note's Ladder)."""
    D = calc.load(out)
    F = calc.flows(D)
    C = calc.constructions(D, F)
    av = np.array([calc.avg5(D, P) for P in C.values()])
    mid = (av.max(axis=0) + av.min(axis=0)) / 2
    return {z: int(round(mid[D.codes.index(K.SCHOOLS[z]["state"])] - K.PAR["target"][z])) for z in K.ZONES}


def write_pack(W, out):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    rows = {}
    rows[R.F_LEGACY] = R.write_legacy(W, out)
    rows[R.F_MEMBERS] = R.write_members(W, out)
    rows[R.F_XWALK] = R.write_crosswalk(W, out)
    rows[R.F_CODES] = R.write_codes(out)
    rows[R.F_BIRTHS] = len(R.write_births(W, out))
    W.caps = centred_capacities(out)
    W.plans = {z: AS.room_plan(z, W.caps[z]) for z in K.ZONES}
    W.A = AS.build_homerooms(W, W.plans)
    W.cap_rows = DOC.write_capacity(out, W.caps, W.plans, W.A.portables_used)
    rows[AS.F_SECTIONS] = AS.write_sections(W, W.A, out)
    rows[AS.F_SECT_ENR] = AS.write_section_enrollment(W, W.A, out)
    W.P = AS.build_preschool(W)
    rows[AS.F_PRESCHOOL] = AS.write_preschool(W, W.P, out)
    AS.write_ecse(W, W.P, out)
    DOC.write_policy(out)
    DOC.write_sis_notes(out, [K.COUNT_DAY[y] for y in K.YEARS])
    DOC.write_birth_notes(out)
    DOC.write_fca(out)
    W.meals = DOC.write_meals(W, out)
    rows[DOC.F_MEALS] = len(W.meals)
    DOC.write_manifest(out, rows)
    t = K.PULL_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (t, t))
    W.rows = rows
    return W
