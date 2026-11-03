#!/usr/bin/env python3
"""Build task188's bundle from a fixed seed.

    python3 task188/generator/build.py

Writes target/ (the pack), golden/ (the deliverables), metadata.json, generator/figures.json and
target.zip, then normalises every mtime inside target/ to the pack's export date, so two consecutive
runs give identical bytes.
"""
import json
import os
import shutil
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import common as C
import docs
import ledger
import pack
import world as W

TARGET = os.path.join(TASK, "target")


def truth_of(members, sim):
    t = {m.number: {"cash": 0.0, "credits": 0.0} for m in members}
    a2m = {a: m.number for m in members for a in m.accounts}
    for p in sim.postings:
        if p["effective_date"].year != C.YEAR:
            continue
        mn = a2m[p["account_number"]]
        if p["credit"] != "":
            t[mn]["credits"] += p["credit"]
        if p["cash_portion"] != "":
            t[mn]["cash"] += p["cash_portion"]
    return t


def make_pack():
    members, by_role, _ = W.build()
    sim = ledger.Sim(members).run()
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    n_post = pack.postings(TARGET, sim)
    pack.register(TARGET, members)
    truth = truth_of(members, sim)
    profile = pack.cdd(TARGET, members, sim, truth)
    pack.lctr_log(TARGET, members, sim)
    pack.directory(TARGET, sim)
    pack.cit(TARGET, sim)
    pack.bags(TARGET, sim)
    pack.str_log(TARGET, members, by_role)
    pack.case_register(TARGET, members, by_role)
    pack.wires(TARGET, members)
    docs.write_all(TARGET)
    return members, by_role, sim, truth, profile, n_post


SOURCES = {
    "core_banking/hrcu_business_postings_2026.csv": ("Harlow Reach Credit Union, core banking, business account postings, effective dates in 2026 and the first business days of January 2027, cash-intensive business segment", "2027-01-08"),
    "membership/member_register_2026-12-31.xlsx": ("Harlow Reach Credit Union, member register, cash-intensive business segment at 31 December 2026, members and accounts", "2027-01-04"),
    "membership/cdd_profiles_extract_2027-01-06.csv": ("Harlow Reach Credit Union, client due diligence profiles, business members, extract", "2027-01-06"),
    "compliance/lctr_submissions_2026.csv": ("Harlow Reach Credit Union, FINTRAC reporting module, large cash transaction report submissions", "2027-01-08"),
    "compliance/str_submissions_2025_2026.csv": ("Harlow Reach Credit Union, Financial Intelligence Unit, suspicious transaction report submissions 2025 and 2026", "2027-01-05"),
    "compliance/fiu_case_register_2026.xlsx": ("Harlow Reach Credit Union, Financial Intelligence Unit, case register 2026", "2027-01-05"),
    "compliance/hrcu_aml_atf_compliance_programme_v6-1.pdf": ("Harlow Reach Credit Union, AML/ATF compliance programme, version 6.1, approved by the Board 24 March 2026", "2026-03-24"),
    "compliance/aml_compliance_committee_terms_of_reference.docx": ("Harlow Reach Credit Union, AML Compliance Committee terms of reference, approved 14 November 2025", "2025-11-14"),
    "branch_network/branch_atm_depository_directory.xlsx": ("Harlow Reach Credit Union, facilities, branches, ATMs and night depositories", "2027-01-04"),
    "cash_services/cit_pickup_manifests_2026.csv": ("Blueline Armoured Transport for Harlow Reach Credit Union Regional Cash Services, night deposit pickup manifests 2026", "2027-01-05"),
    "cash_services/night_deposit_bag_register.csv": ("Harlow Reach Credit Union, Regional Cash Services, night deposit bag register", "2027-01-05"),
    "payments/international_wires_2026.csv": ("Harlow Reach Credit Union, payments operations, international wire transfers 2026", "2027-01-06"),
}
DISTRACTORS = ["target/compliance/str_submissions_2025_2026.csv", "target/compliance/fiu_case_register_2026.xlsx",
               "target/payments/international_wires_2026.csv"]


def write_metadata():
    files = []
    for rel in sorted(SOURCES):
        path = os.path.join(TARGET, rel)
        rows = None
        if rel.endswith(".csv"):
            with open(path, encoding="utf-8") as f:
                rows = sum(1 for _ in f) - 1
        src, date = SOURCES[rel]
        files.append({"file": rel, "source": src + " (fictional, synthetic records)", "date": date,
                      "license": "CC0-1.0 (synthetic, generated for this task)", "rows": rows})
    meta = {
        "task": "task188",
        "title": "Harlow Reach Credit Union's January 2027 review of its cash-intensive business members",
        "setting": "A fictional credit union in the Lower Mainland of British Columbia and its financial intelligence "
                   "unit's January review of the business members it classes as cash-intensive; the credit union, "
                   "its members, card acquirers, delivery platforms, carriers and people are fictional, and every "
                   "record is synthetic.",
        "as_of": "2027-01-08",
        "deliverables": ["fiu_referral_slate_2027q1.docx", "member_cash_review_2026.xlsx", "cash_review_2026.png"],
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["calendar 2026", "the first quarter of 2027", "each quarter of 2026",
                          "CAD to the nearest thousand and the nearest twenty-five thousand"],
        "files": files,
        "generator": "generator/build.py (seed %d)" % C.SEED,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")


def normalise_mtimes(root):
    stamp = time.mktime((2027, 1, 8, 7, 40, 0, 0, 0, -1))
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            os.utime(os.path.join(dirpath, f), (stamp, stamp))
        os.utime(dirpath, (stamp, stamp))


def zip_target():
    path = os.path.join(TASK, "target.zip")
    files = []
    for dirpath, dirnames, filenames in os.walk(TARGET):
        for f in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, f), TASK))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in sorted(files):
            zi = zipfile.ZipInfo(rel.replace(os.sep, "/"), date_time=C.EXPORT_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, open(os.path.join(TASK, rel), "rb").read())
    return path


def main():
    t0 = time.time()
    members, by_role, sim, truth, profile, n_post = make_pack()
    import golden
    golden.run(TARGET, TASK, members, by_role)
    write_metadata()
    normalise_mtimes(TARGET)
    zp = zip_target()
    print("postings %d; built in %.1fs; %s" % (n_post, time.time() - t0, zp))


if __name__ == "__main__":
    main()
