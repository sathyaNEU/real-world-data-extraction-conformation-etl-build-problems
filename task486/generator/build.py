"""Builds task486's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task486/generator/build.py          # the whole build
    python3 task486/generator/build.py pack     # the pack only
"""
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import numpy as np         # noqa: E402

import distractors as DS   # noqa: E402
import filler as F         # noqa: E402
import timeline as TL      # noqa: E402
import world as W          # noqa: E402

SEED = 490
NAMES = dict(
    paye22="paye_returns_m12_2021-22.csv", paye26="paye_returns_m12_2025-26.csv",
    spec="paye_extract_specification_v4.pdf", list17="rating_list_2017_extract_20220404.csv",
    list23="rating_list_2023_extract_20260413.csv", codes="valuation_description_codes.json",
    guide="rating_list_extract_guide.pdf", accounts="business_rates_accounts_2017-2026.xlsx",
    companies="companies_register_extract_20260501.csv", schedule="town_centre_schedule_2026.csv",
    prospectus="town_centre_renewal_fund_2027_prospectus.pdf", sic="sic2007_subclasses.csv",
    footfall="town_centre_footfall_daily_2021-2026.csv", lfs="labour_force_survey_employment_by_industry_2022_2026.xlsx")
GOLD = dict(workbook="town_centre_fund_2027_eligibility.xlsx", chart="town_centre_retail_employment_2022_2026.png")
OWNERS = {
    "accounts": dict(creator="Torvasay Statistics", last_by="Economic Statistics", created="2026-05-07T09:41:00Z",
                     modified="2026-05-12T15:06:00Z", company="Torvasay Statistics"),
    "lfs": dict(creator="Labour Market Statistics", last_by="Labour Market Statistics", created="2026-05-21T08:57:00Z",
                modified="2026-06-11T10:30:00Z", company="Torvasay Statistics"),
}
STAMPS = {"prospectus": b"D:20260907101500+00'00'", "spec": b"D:20260511143000+00'00'",
          "guide": b"D:20260413090000+00'00'"}


def t(k):
    return os.path.join(TARGET, NAMES[k])


def truth(seed=SEED):
    """the clean truth: the retail world planned and tuned, the rest of the island, and the records over time"""
    w = W.retail_world(seed)
    F.add(w, seed + 1)
    TL.build(w, seed + 2)
    return w


def pack(w=None):
    import docs as DOC
    import pack as PK
    import postprocess as PP
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = w or truth()
    rng = np.random.default_rng(SEED + 9)
    n = {}
    n["paye"] = PK.paye(w, t("paye22"), t("paye26"))
    n["lists"] = PK.lists(w, t("list17"), t("list23"), t("codes"))
    n["accounts"] = PK.accounts(w, t("accounts"), rng)
    n["companies"] = PK.companies(w, t("companies"), rng)
    n["schedule"] = PK.schedule(w, t("schedule"))
    n["sic"] = PK.sic_lookup(w, t("sic"))
    n["footfall"] = DS.footfall(w, t("footfall"), SEED + 11)
    n["lfs"] = DS.lfs(w, t("lfs"), SEED + 12)
    DOC.prospectus(t("prospectus"))
    DOC.paye_spec(t("spec"))
    DOC.list_guide(t("guide"))
    for k in OWNERS:
        PP.normalize_ooxml(t(k), excel=True, **OWNERS[k])
    for k, stamp in STAMPS.items():
        PP.normalize_pdf(t(k), stamp, stamp)
    return w, n


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    w, n = pack()
    import goldfiles as GF
    import postprocess as PP
    figs = GF.write(gpath, w)
    PP.normalize_ooxml(gpath("workbook"), "Frances Davies", "Frances Davies", "2026-10-29T09:14:00Z",
                       "2026-11-04T16:22:00Z", title="Town Centre Renewal Fund 2027: eligibility schedule",
                       excel=True, company="Torvasay Statistics")
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))
    return w


def cut_zip():
    """Each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own."""
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[nm][1].split("-"))
            h = int(hashlib.md5(nm.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(nm, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, nm), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        w, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
