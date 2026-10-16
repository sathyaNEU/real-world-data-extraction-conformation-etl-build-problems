"""Write the evidence pack into a folder: every record, document, ask file and distractor, with fixed file times."""
from __future__ import annotations

import os
import shutil

import asks_records as AR
import asks_world as AW
import common as K
import distract as DS
import docs as DOC
import records as R
import world as WD

PACK_MTIME = 1793630820   # 2026-11-02 14:07:00 UTC-ish, the folder's build time in the fiction


class Built:
    pass


def build_world():
    B = Built()
    B.W = WD.simulate()
    B.C = R.case_frame(B.W)
    B.I = AW.items()
    return B


def write_pack(B, out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    W, C = B.W, B.C
    B.n_legacy = R.write_legacy(W, C, out)
    B.n_platform = R.write_platform(W, C, out)
    B.wfm = R.write_wfm(W, out)
    B.wms = R.write_wms(W, out)
    R.write_standards(W, out)
    R.write_plan(W, out)
    R.write_register(W, out)
    R.write_ita(W, C, out)
    DOC.write_procedure(W, out)
    DOC.write_agreement(W, out)
    DOC.write_notes(out)
    B.rtw_rows, B.rtw_cases = AR.write_rtw(W, C, out)
    B.items_cur = AR.write_items(W, B.I, out)
    B.picks_raw, B.picks = AR.write_picks(W, B.I, out)
    DS.write_wc(W, C, out)
    DS.write_bbs(W, out)
    DOC.write_manifest(out, manifest_rows())
    for fn in sorted(os.listdir(out)):
        os.utime(os.path.join(out, fn), (PACK_MTIME, PACK_MTIME))
    return B


def manifest_rows():
    return [
        [R.F_LEGACY, "Legacy incident database", "2026-11-02", "Cases with a date of injury 12/27/2020 to 06/30/2024", "EHS"],
        [R.F_PLATFORM, "EHS platform", "2026-11-02", "Cases from 07/01/2024 and cases migrated at go-live", "EHS"],
        [R.F_WFM, "Workforce management", "2026-11-02", "Hours by DC, fiscal week and department, FY2021 wk 1 to FY2026 wk 44", "HR Systems"],
        [R.F_WMS, "WMS", "2026-11-02", "Cases shipped by location, fiscal week and category, FY2021 wk 1 to FY2026 wk 44", "Operations"],
        [R.F_STD, "Industrial Engineering", "2026-11-02", "Engineered labor standards and site factors", "Industrial Engineering"],
        [R.F_PLAN, "FP&A", "2026-10-23", "FY2027 operating plan v3: volume and labor by DC and period", "Operations Planning"],
        [R.F_REG, "Real estate and operations", "2026-11-02", "DC register", "Operations"],
        [R.F_ITA, "OSHA Injury Tracking Application", "2026-11-02", "Form 300A submissions, calendar 2021 to 2025", "EHS"],
        [DOC.F_PROC, "EHS policy library", "2026-11-02", "OSHA recordkeeping procedure, rev 7", "EHS"],
        [DOC.F_AGREE, "Procurement", "2026-11-02", "Lindqvist agreement, draft for signature", "Procurement"],
        [AR.F_RTW, "Case management system", "2026-11-02", "Return-to-work status log, files opened from 12/28/2025", "Return-to-work program"],
        [AR.F_ITEM, "WMS", "2026-11-01", "Item master, active and discontinued items", "Operations"],
        [AR.F_ITEMH, "WMS", "2026-11-01", "Item master history", "Operations"],
        [AR.F_PICKS, "WMS", "2026-11-02", "Program DCs' cases picked by SKU and fiscal period, FY2026 P1 to wk 44", "Operations"],
        [DS.F_WC, "Workers' compensation TPA", "2026-10-07", "Loss run valued 09/30/2026", "Risk Management"],
        [DS.F_BBS, "Safety observation app", "2026-11-02", "Behavior-based safety observations FY2025 to FY2026 wk 44", "EHS"],
        [DOC.F_NOTES, "Safety Analytics", "2026-11-02", "Field notes for this folder", "EHS"],
    ]
