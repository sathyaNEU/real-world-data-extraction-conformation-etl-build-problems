"""Build the pack, compute every owed figure from it, write the goldens, figures.json, submission.md and metadata.json,
run the checks, rebuild into a scratch folder and require byte-identical output, cut target.zip and run the
independent verifier on it.

    python3 task304/generator/make.py            (full: two builds, the zip, the verifier)
    python3 task304/generator/make.py --once     (one build, no zip)
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import solve as SV  # noqa: E402
import world  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 10, 7, 8, 40, 0)        # the morning the planning folder was handed over

SOURCES = {
    "van": "a find-and-treat van's tablet export of contacts and point-of-care results",
    "register": "an NHS operational delivery network's hepatitis C treatment register (in the manner of the national "
                "HCV patient registry), across a clinical system migration",
    "dispensing": "hospital and clinic pharmacy dispensing records of direct-acting antiviral packs",
    "lab": "a regional virology laboratory's hepatitis C result feed",
    "census": "two supported housing providers' resident lists",
    "hostel_returns": "local authority supported housing occupancy returns",
    "ap_returns": "probation approved premises occupancy returns",
    "ds_episodes": "a drug and alcohol treatment provider's monthly new treatment episodes (in the manner of NDTMS)",
    "nsp_reg": "a community pharmacy needle and syringe programme system's registrations (in the manner of "
               "PharmOutcomes)",
    "pharmacies": "a list of community pharmacies providing needle and syringe exchange",
    "clinics": "the network's clinic list with the codes before and after the migration",
    "plan": "a charity's operational plan for its trustees",
    "pathway": "an operational delivery network's testing and treatment pathway",
    "intentions": "an integrated care board's commissioning intentions",
    "fibroscan": "liver stiffness scans taken on the van",
    "costs": "the van's monthly running costs",
}


def figures(S, target):
    o = S["order"]
    R = S["R"]
    rates = {s: {"A": "%.2f" % R[s]["A"], "F": "%.3f" % R[s]["F"], "ST": "%.2f" % S["ST"][s]} for s in P.SETTINGS}
    cs = SV.courses(target)
    t = SV.rna(target)
    rows = []
    for c in sorted(cs, key=lambda c: (c["clinic"], c["last"], c["ref"])):
        half = "H1" if SV.H1[0] <= c["last"] <= SV.H1[1] else ("H2" if SV.H2[0] <= c["last"] <= SV.H2[1] else None)
        if not half:
            continue
        lo = c["last"] + dt.timedelta(days=84)
        ok = sorted(d for d, res in t.get(c["pid"], []) if d >= lo and (c["next"] is None or d < c["next"])
                    and res == "Not detected")
        rows.append(dict(ref=c["ref"], clinic=c["clinic"], last=c["last"], half=GD.HALF[half],
                         confirm=ok[0] if ok else None))
    F = dict(call=P.LABEL[o[0]], order=o, found10=S["found10"], starts10=S["starts10"],
             gap10=S["starts10"][o[0]] - S["starts10"][o[1]],
             found={s: "%.1f" % S["found"][s] for s in P.SETTINGS}, starts={s: "%.1f" % S["starts"][s] for s in P.SETTINGS},
             rates=rates, pilot_found=S["Rp"]["found"], pilot_tested=S["Rp"]["tested"], F_pilot="%.3f" % S["Rp"]["F"],
             F_nonpilot="%.3f" % S["Rn"]["F"], pilots=sorted(S["pilots"]), census=S["census"], hh_tested=S["T"],
             hh_untested=S["U"], hh_found=S["Tpos"], hh_negative=S["T"] - S["Tpos"],
             hh_arrivals=S["pools"]["hh_arrivals"], ap_residents=S["pools"]["ap_residents"],
             ap_arrivals=S["pools"]["ap_arrivals"], ds_arrivals=S["pools"]["ds_arrivals"], nsp_regs=S["nsp_regs"],
             inc_events=S["inc_events"], inc_py=int(round(S["inc_py"])), inc="%.4f" % S["inc"],
             cures=SV.cures(target), course_rows=rows,
             pack_tail=int(SV.rows(target, "dispensing")[0]["days_supply"]) - 1,
             ladder={k: {s: round(v, 1) for s, v in d.items()} for k, d in S["ladder"].items()})
    return F


def write_figures(F, path):
    out = {k: v for k, v in F.items() if k not in ("course_rows",)}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")


def metadata(target):
    files = []
    for k, f in P.FILES.items():
        p = os.path.join(target, f)
        rows = sum(1 for _ in open(p, encoding="utf-8")) - 1 if f.endswith(".csv") else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed (seeded generator) in the layout of %s" % SOURCES[k], "date": "2026-10-07",
                      "license": "CC0-1.0 (original work)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task304",
        "title": "Which of four settings Brannock Trust's find-and-treat van works full-time in 2027, sized by the "
                 "people it would start on hepatitis C treatment, with the network's confirmed cures by clinic and "
                 "half-year, October 2024 to September 2025",
        "domain": "Epidemiology & Public Health",
        "subdomain": "screening-diagnostic-policy-evaluation (a screening yield carried to the pool a programme will "
                     "meet: a competing test-and-treat service from a fixed date, and a first round of a standing "
                     "population)",
        "objective": "Opportunity Sizing & Decision Support",
        "prompt_shape": "09: the setting, each of four settings' people found and started in 2027 (8), the chart, and "
                        "five clinics by two half-years of confirmed cures (10)",
        "as_of": "2026-09-30",
        "deliverables": [GD.DOCX, GD.XLSX],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "stated_inputs": ["the plan's decision, operating rule, counting rules and 2027 pools "
                          "(find_and_treat_van_2027_plan.pdf)",
                          "the pathway's end of a course and confirmed cure (fenwold_hcv_pathway_2026.pdf)",
                          "PH-12, pharmacist test and treat at every needle exchange pharmacy from 1 April 2027 "
                          "(fenwold_icb_commissioning_intentions_2027-28.pdf)"],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated by task304/generator/make.py (seeded, deterministic) around a fictional "
                               "English city: a charity's outreach van and its 2026 rota of four settings, an NHS "
                               "hepatitis C network's register, dispensing and laboratory results, two housing "
                               "providers' resident lists and returns, probation and drug service returns, and a "
                               "pharmacy needle exchange system; layouts follow the public files named, every "
                               "organisation, place and person is invented, and no real dataset is reproduced.",
                     "date": "2026-10-07", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-28",
        "generator": "task304/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def stamp(folder):
    t = dt.datetime(*STAMP, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def fresh(folder):
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
    os.makedirs(folder, exist_ok=True)


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp


def build(target, golden_dir):
    fresh(target)
    pack.write_all(world.build(), target)
    stamp(target)
    S = SV.solve(target)
    F = figures(S, target)
    fresh(golden_dir)
    GD.write(golden_dir, F)
    stamp(golden_dir)
    return S, F


def main(second=True, checks=True):
    S, F = build(TARGET, GOLDEN)
    write_figures(F, os.path.join(HERE, "figures.json"))
    WU.write(os.path.join(TASK, "submission.md"), F)
    metadata(TARGET)
    if checks:
        import checks as C
        assert not C.main(TARGET)
    if second:
        tmp = tempfile.mkdtemp()
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        build(t2, g2)
        d1, d2 = digest(TARGET), digest(t2)
        assert d1 == d2, [f for f in d1 if d1[f] != d2.get(f)]
        assert digest(GOLDEN) == digest(g2), [f for f in digest(GOLDEN) if digest(GOLDEN)[f] != digest(g2).get(f)]
        shutil.rmtree(tmp)
        zp = cut_zip()
        print("byte-identical; target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
        import verify as V
        assert not V.main(zp)
    return S, F


if __name__ == "__main__":
    main(second="--once" not in sys.argv, checks="--nochecks" not in sys.argv)
