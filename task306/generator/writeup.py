"""submission.md, generator/figures.json and metadata.json, every figure emitted from the computed results."""
import json
import os

import golden as GD
import pack as P
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def m(x):
    return "£%dm" % GD.m1(x)


def m1(x):
    return "£%.1fm" % GD.m01(x)


def k(x):
    return "£{:,}".format(GD.k1(x))


def label(o):
    s, e = o["start"], o["end"]
    if s == e:
        return "%d %s" % (s.day, s.strftime("%B"))
    if s.month == e.month:
        return "%d to %d %s" % (s.day, e.day, s.strftime("%B"))
    return "%d %s to %d %s" % (s.day, s.strftime("%B"), e.day, e.strftime("%B"))


def figures(G):
    nf = sum(G["record_follow"])
    return {
        "call": "add the second-event cover",
        "capital_gbp_m": {"gross": GD.m1(G["gross"]), "net_occurrence": GD.m1(G["net_base"]),
                          "net_both": GD.m1(G["net_both"]), "release": GD.m1(G["release_sec"])},
        "cover_gbp_m": {"margin": GD.m01(G["margin_sec"]), "value": GD.m01(G["value"]),
                        "capital_cost": GD.m01(W.COC * G["release_sec"]), "premium": GD.m01(W.SEC["premium"]),
                        "expected_reinstatement": GD.m01(G["rp_sec"]), "expected_recoveries": GD.m01(G["rec_sec"])},
        "record": {"storms": len(G["record"]), "within_six_weeks": nf, "load_follow": round(G["load_follow"], 2),
                   "load_other": round(G["load_lone"], 2), "pooled": round(G["pooled"], 2),
                   "gap_in_train_max_days": W.GAP_IN[1], "gap_between_trains_min_days": W.GAP_TRAINS},
        "occurrences_2026": [{"days": label(o), "home": GD.k1(o["home"]), "farm": GD.k1(o["farm"]),
                              "incurred": GD.k1(o["incurred"])} for o in G["occ2026"]],
        "recovery_2026": GD.k1(G["recovery2026"]), "reinstatement_2026": GD.k1(G["reinstatement2026"]),
        "farm_si_gbp_m": {c: {"buildings": GD.m01(b), "farm_contents": GD.m01(ct)} for c, (b, ct) in G["farm_si"].items()},
        "constants": {"base_limit": int(W.BASE["limit"]), "base_retention": int(W.BASE["retention"]),
                      "sec_limit": int(W.SEC["limit"]), "sec_retention": int(W.SEC["retention"]),
                      "coc_per_cent": int(W.COC * 100), "worst_years": W.RANK_1IN200, "years": W.N_YEARS,
                      "hours": W.HOURS, "floor_m": 1, "per_cent": 100},
    }


def submission(G):
    nf = sum(G["record_follow"])
    F = P.FILES
    occ = G["occ2026"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Actuarial Science & Insurance (reinsurance and capital: a county farm-and-home mutual's 2027 "
        "windstorm reinsurance, a cover bought when the capital it releases is worth more than it costs).",
        "**Analytical objective:** Opportunity Sizing & Decision Support.",
        "",
        "## 1. Final Recommendation",
        "",
        "**We should add Penwarden's second-event cover to the 2027 windstorm programme.**",
        "It releases %s of 1-in-200 windstorm capital, worth %s a year at 12 per cent against a margin of %s, so it "
        "adds %s a year. Not on one incurred-over-hindcast ratio for every storm of record, which undercosts the "
        "storms that strike within weeks of the one before and leaves the cover looking dearer than its release is "
        "worth. Not on each storm's place in its year or season, which the record's later storms on quiet seasons, "
        "costing what the model says, rule out." % (m(G["release_sec"]), m1(W.COC * G["release_sec"]),
                                                     m1(G["margin_sec"]), m1(G["value"])),
        "",
        "## 2. Critical Components",
        "",
        "1. Storms of record that struck within six weeks of the storm before cost **%.2f** times their hindcast, "
        "every other storm **%.2f** times." % (G["load_follow"], G["load_lone"]),
        "2. The 1-in-200 annual windstorm loss is **%s** gross, **%s** net of the occurrence cover and **%s** net of "
        "both covers." % (m(G["gross"]), m(G["net_base"]), m(G["net_both"])),
        "3. The second-event cover's margin is **%s** a year: its premium of **%s** and expected reinstatement "
        "premium of **%s**, less expected recoveries of **%s**." % (m1(G["margin_sec"]), m1(W.SEC["premium"]),
                                                                    m1(G["rp_sec"]), m1(G["rec_sec"])),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Linked each storm in %s to the storm in %s whose peak falls on its first damage date or the day after, "
        "all %d storms of record, and classed each by the days since the storm before it (every gap is %d days or "
        "less, or %d or more): the %d within six weeks cost %.2f times their hindcast and the rest %.2f, incurred over "
        "hindcast for the storms like it per CP-04 section 2." % (
            F["experience"], F["hindcast"], len(G["record"]), W.GAP_IN[1], W.GAP_TRAINS, nf, G["load_follow"],
            G["load_lone"]),
        "2. Classed each storm of %s the same way against the storm before it in its simulated year and costed it at "
        "its class's ratio." % F["ylt"],
        "3. Netted each simulated year of the occurrence cover (quotation A, 18,000,000 xs 12,000,000 each loss "
        "occurrence, one reinstatement at 100 per cent pro rata as to amount), each storm one loss occurrence per "
        "CP-04: the 1-in-200, the average of the 50 worst of the 10,000 years, is %s gross and %s net." % (
            m(G["gross"]), m(G["net_base"])),
        "4. Added the second-event cover (quotation B, 7,500,000 xs 4,000,000 of the loss retained under the "
        "occurrence cover on each year's second and later loss occurrences, one reinstatement): the 1-in-200 falls to "
        "%s, a release of %s." % (m(G["net_both"]), m(G["release_sec"])),
        "5. Took the cover's margin per CP-04 section 3 over the 10,000 years: %s." % m1(G["margin_sec"]),
        "6. Dated each 2026 storm claim line in %s by date_of_damage in %s (insurer_ref without its spaces), a "
        "reopened claim's lines in notification order against its instructions in instruction order, and grouped the "
        "days into the 72-hour loss occurrences that maximise the expiring cover's recovery (wording clause 3): "
        "it recovers %s and calls %s of reinstatement premium." % (
            F["claims"], F["adjusters"], k(G["recovery2026"]), k(G["reinstatement2026"])),
        "7. Summed the Holdings sheet of %s by each holding's county, each coinsured policy at its share in %s, "
        "matched on its main holding's CPH or, for a renumbered holding, its previous_cph, and applied to every "
        "holding on the policy." % (F["farm"], F["coins"]),
        "8. Valued the cover at 12 per cent of the release, %s, less the margin: it adds %s a year, so it is added "
        "to the programme." % (m1(W.COC * G["release_sec"]), m1(G["value"])),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % GD.PDF,
        "",
        "1. Recommendation: add the second-event cover to the 2027 programme.",
        "2. Bar chart on page 1 of the 1-in-200 annual windstorm loss: %s gross, %s net of the occurrence cover, %s "
        "net of both covers." % (m(G["gross"]), m(G["net_base"]), m(G["net_both"])),
        "3. Capital the second-event cover releases: %s." % m(G["release_sec"]),
        "4. The cover's margin %s; its worth to us a year %s." % (m1(G["margin_sec"]), m1(G["value"])),
        "5. 2026 loss occurrences of £1 million or more, home and farm policies:",
    ]
    for o in occ:
        lines.append("   - %s: home %s, farm %s" % (label(o), k(o["home"]), k(o["farm"])))
    lines += [
        "6. The expiring cover recovers %s on 2026 and calls a reinstatement premium of %s." % (
            k(G["recovery2026"]), k(G["reinstatement2026"])),
        "7. Our share of the farm sums insured, buildings and farm contents:",
    ]
    for c in W.COUNTIES:
        b, ct = G["farm_si"][c]
        lines.append("   - %s: buildings %s, farm contents %s" % (c, "£{:,.1f}m".format(GD.m01(b)),
                                                                  "£{:,.1f}m".format(GD.m01(ct))))
    lines += [
        "",
        "### %s" % GD.XLSX,
        "",
        "1. The same figures: sheet Capital 2027 carries the call, the three 1-in-200 losses, the release, the margin "
        "and the worth; Storms 2026 each occurrence's home and farm cost, the recovery and the reinstatement premium; "
        "Farm sums insured each county's buildings and farm contents; Record the storms of record with their ratios.",
        "",
    ]
    return "\n".join(lines)


def metadata(target):
    files = []
    for key, f in P.FILES.items():
        p = os.path.join(target, f)
        rows = (sum(1 for _ in open(p, encoding="utf-8")) - 1) if f.endswith(".csv") else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed (seeded generator)", "date": "2026-11-02",
                      "license": "CC0-1.0 (original work)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task306",
        "title": "Whether a county farm-and-home mutual adds a second-event windstorm cover to its 2027 reinsurance "
                 "programme, and the 1-in-200 capital it releases under the mutual's capital policy",
        "domain": "Actuarial Science & Insurance",
        "subdomain": "reinsurance-capital (a catastrophe cover bought when the capital it releases is worth more than "
                     "it costs, with the year's claims against the expiring cover and the farm book by county)",
        "objective": "Opportunity Sizing & Decision Support",
        "prompt_shape": "other: a buy-or-not call with the capital released and its worth, the year's loss "
                        "occurrences by line, and the farm sums insured by county and section",
        "as_of": "2026-11-02",
        "deliverables": [GD.PDF, GD.XLSX],
        "distractor_files": [P.FILES[x] for x in P.DISTRACTORS],
        "context_artifacts": [],
        "stated_inputs": ["the 1-in-200 annual windstorm loss, the costing of each simulated storm, the release and "
                          "the value at the cost of capital (capital policy CP-04, sections 2 and 3)",
                          "the covers quoted for 2027 (the broker's quotation) and the expiring cover's terms (the "
                          "2026 wording)"],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated by task306/generator/build.py (seeded, deterministic) around a fictional "
                               "mutual insurer in the south-west of England, its fictional catastrophe model vendor, "
                               "broker, reinsurers, co-insurers and loss adjusters; every organisation, storm and "
                               "person is invented and no real dataset is reproduced.",
                     "date": "2026-11-02", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-31",
        "generator": "task306/generator/build.py",
        "files": files,
    }


def write(task, G):
    target = os.path.join(task, "target")
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(submission(G))
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(figures(G), fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(task, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(metadata(target), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
