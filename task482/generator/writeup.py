"""task482 architecture 16: submission.md and metadata.json, every figure from figures.json and the golden run."""
import json

import golden as G
import params as P

NAME = {"BIL6063": "6063 extrusion billet", "BIL6082": "6082 extrusion billet", "INGLM25": "LM25 foundry ingot",
        "CSTLM25": "LM25-TF sand castings"}
GRADE = {"CST": "old cast aluminium", "EXT": "extrusion offcuts", "TRN": "turnings and swarf",
         "UBC": "used beverage cans"}


def t(x):
    return "{:,}".format(x)


def submission(fig, res, path):
    pr, co = fig["produced_t"], fig["calloff_t"]
    hours, tonnes = res["parts"]["hours"], res["parts"]["tonnes"]
    n82 = sum(1 for ld in res["d"]["h1"] if ld["family"] == "BIL6082")
    n63 = sum(1 for ld in res["d"]["h1"] if ld["family"] == "BIL6063")
    h_share = 100 * hours["BIL6082"] / sum(hours.values())
    t_share = 100 * tonnes["BIL6082"] / sum(tonnes.values())
    a, b = fig["ask_a"], fig["ask_b"]
    L = ["## Tags", "",
         "**Domain:** Physical & Environmental Sciences (emissions inventory: a secondary aluminium works' product "
         "carbon intensities under a car maker's supplier carbon requirement).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
         "## 1. Final Recommendation", "",
         "**Velden pays Brackwell Alloys EUR %s in low-carbon premium on its 2027 call-offs: EUR 38 a tonne on "
         "%s t of 6063 extrusion billet and %s t of LM25 foundry ingot, the two families at or under SCR-2's 0.235 "
         "t CO2/t in 2026.**" % (t(fig["call"]["premium_eur"]), t(co["BIL6063"]), t(co["INGLM25"])),
         "6082 extrusion billet and the LM25-TF sand castings are over the limit and earn nothing on their %s t and "
         "%s t. The homogenizing furnace burns gas by the hours its loads soak, and a 6082 load soaks about %.0f "
         "hours against about %.0f for 6063; shared by tonnes, the two billet alloys come out level and 6082 would "
         "wrongly qualify." % (t(co["BIL6082"]), t(co["CSTLM25"]), hours["BIL6082"] / n82, hours["BIL6063"] / n63),
         "",
         "## 2. Critical Components", "",
         "1. 2026 specific direct emissions against SCR-2's 0.235 t CO2 per tonne produced: 6063 billet and LM25 "
         "ingot **at or under it**; 6082 billet and LM25-TF castings **over it**.",
         "2. The homogenizing furnace's gas follows its firing hours, not its tonnes: 6082 loads take **%.0f per "
         "cent** of its hours on %.0f per cent of its billet." % (h_share, t_share),
         "3. 2026 production, tonnes that passed final inspection (each lot at its last result): 6063 billet %s, "
         "6082 billet %s, LM25 ingot %s, LM25-TF castings %s." % (t(pr["BIL6063"]), t(pr["BIL6082"]),
                                                               t(pr["INGLM25"]), t(pr["CSTLM25"])),
         "4. 2027 call-offs: 6063 billet %s t, 6082 billet %s t, LM25 ingot %s t, castings %s t; premium EUR 38 x "
         "%s t = EUR %s." % (t(co["BIL6063"]), t(co["BIL6082"]), t(co["INGLM25"]), t(co["CSTLM25"]),
                            t(co["BIL6063"] + co["INGLM25"]), t(fig["call"]["premium_eur"])), "",
         "## 3. Step-by-Step Solution", "",
         "1. Gas: the 15-minute export moved from UTC to local time, hundreds of cubic feet x 2.83 to cubic metres "
         "before the 14 April 10:30 meter exchange, and each interval converted at the volume correction factor and "
         "calorific value of the invoice period it falls in (kWh = m3 x 1.02264 x CV / 3.6).",
         "2. Logs: one row kept per furnace and heat (re-keyed rows dropped), each heat's tonnes spread from charge to "
         "melt-out, tower melter charges in kg, homogenizing furnace and solution oven hours from door closed or start "
         "to door opened or end, all local time.",
         "3. Regressed each local day's kWh on casthouse tonnes melted, tower melter tonnes, homogenizing furnace "
         "hours, solution oven hours and heating degree days (base 15.5 C on the daily mean), with a constant.",
         "4. Each family carries its casthouse heats' tonnes melted at the melting rate and its homogenizing loads' "
         "hours at the furnace's hourly rate; the castings carry the tower melter and the solution oven; the rest of "
         "the year's gas (pilot flames, heating) is shared by tonnes produced.",
         "5. Production from the lots file at each lot's last result, PASS only; CO2 at 0.18296 kg/kWh over each "
         "family's production.",
         "6. Premium: EUR 38 on the 2027 schedule's call-offs (months summed) of each family at or under 0.235.",
         "7. Scrap: accepted goods-in lines joined to the weighbridge on ticket and date (tickets restart on 29 June); "
         "a one-grade load is in-weigh less out-weigh, a two-grade load's grades are the drops across its two tips, "
         "matched to the lines by their declared weights; summed by quarter of the goods-in date.",
         "8. Dross: Midland's waste-out tickets, the out-weigh less the weighing just before the skip was lifted (the "
         "second weighing where returned metal came off first); summed by quarter.", "",
         "## 4. Deliverable Answers", "", "### %s" % P.DELIVERABLES[0], "",
         "1. Premium on the 2027 call-offs: EUR %s." % t(fig["call"]["premium_eur"]),
         "2. Families earning it: 6063 extrusion billet (%s t) and LM25 foundry ingot (%s t)." % (
             t(co["BIL6063"]), t(co["INGLM25"])),
         "3. Each family's 2026 emissions per tonne against the 0.235 t CO2/t limit: 6063 extrusion billet and LM25 "
         "foundry ingot at or under it; 6082 extrusion billet and LM25-TF sand castings over it.",
         "4. Chart of each family's 2026 emissions per tonne against the 0.235 limit.", "",
         "### %s" % P.DELIVERABLES[1], "",
         "1. Scrap bought in, tonnes as weighed, by grade and quarter of 2026:"]
    for g in G.GRADES:
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % ((GRADE[g],) + tuple(t(a[g][q]) for q in G.QUARTERS)))
    L.append("2. Dross sent off for recovery, tonnes as weighed: Q1 %s, Q2 %s, Q3 %s, Q4 %s." % tuple(
        t(b[q]) for q in G.QUARTERS))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


SOURCES = {
    "meter": ("synthetic: the gas supplier's 15-minute interval export for the works' one site meter", "2027-01-12"),
    "invoices": ("synthetic: the gas supplier's VAT invoices by meter-read period, with calorific values",
                 "2027-01-10"),
    "furnaces": ("synthetic: the casthouse and foundry melting furnaces' charge logs as kept by the works office",
                 "2027-01-19"),
    "h1": ("synthetic: the homogenizing furnace's load log", "2027-01-18"),
    "t1": ("synthetic: the solution and ageing oven's batch log", "2027-01-18"),
    "lots": ("synthetic: the inspection system's export of production lots and results", "2027-01-15"),
    "scr2": ("synthetic: the car maker's supplier carbon requirement, Revision 2", "2025-12-08"),
    "calloff": ("synthetic: the car maker's 2027 call-off schedule for the supplier", "2026-12-14"),
    "email": ("synthetic: the supplier's cover email for its 2026 data package", "2027-01-21"),
    "weather": ("synthetic: the works' roof weather station, daily summary", "2027-01-05"),
    "weighbridge": ("synthetic: the works' weighbridge export, one row per weighing", "2027-01-08"),
    "goodsin": ("synthetic: the scrap goods-in register", "2027-01-08"),
    "elec": ("synthetic: the electricity supplier's half-hourly settlement data for the works' import meter",
             "2027-01-11"),
    "assets": ("synthetic: the works' plant asset register with rated inputs", "2026-09-22"),
    "roster": ("synthetic: the casthouse and foundry crew roster", "2025-12-15"),
}
WHY = {"elec": "electricity is not fuel the works burned (SCR-2 section 2), so it carries no direct emissions",
       "assets": "rated burner inputs say what a burner can fire, not the gas it burned; SCR-2 takes billed energy",
       "roster": "crew rotations say who was on shift, not what the processes burned"}


def metadata(path):
    files = []
    for k, name in P.FILES.items():
        src, date = SOURCES[k]
        files.append({"name": name, "role": "distractor" if k in P.DISTRACTORS else "evidence", "source": src,
                      "date": date, "license": "CC0 1.0 (synthetic, authored for this task)"})
    meta = {"task": "task482", "architecture": 16, "setting": "2027-01-28",
            "files": sorted(files, key=lambda f: f["name"]),
            "distractors": [P.FILES[k] for k in P.DISTRACTORS],
            "distractor_reasons": {P.FILES[k]: WHY[k] for k in P.DISTRACTORS},
            "stated_inputs": ["0.235", "0.18296", "1.02264", "2.83"],
            "deliverables": list(P.DELIVERABLES)}
    json.dump(meta, open(path, "w"), indent=1)
