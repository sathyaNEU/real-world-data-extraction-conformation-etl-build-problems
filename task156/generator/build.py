"""Builds task156 from the seed: the world, the pack under target/, the golden deliverables, figures.json and
metadata.json. python3 task156/generator/build.py [outdir]  (outdir defaults to the task folder)."""
import csv
import datetime as dt
import io
import json
import os
import sys

import numpy as np
from reportlab.platypus import Spacer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A          # noqa: E402
import estim as ES        # noqa: E402
import officepdf          # noqa: E402
import pack as PK         # noqa: E402
import parse as PA        # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
EDGE = 0.012     # every graded energy figure at least this far (MWh) from its rounding edge
SEP_WH = 160000  # the tests' energy and the gaps' energy at least this far apart at every hub, so they never cancel,
#                  and the tests alone carry every hub's figure across a rounding step


def clean_asks(H, charges):
    hubs = [h["code"] for h in H["hubs"]]
    n = {h: 0 for h in hubs}
    e = {h: 0 for h in hubs}
    for c in charges:
        if c["model"] != "HX150" or c["failed"] or c["auth"] == "test" or c["m1"] <= c["m0"]:
            continue
        if A.WIN_A <= c["start"] < A.WIN_B:
            n[c["hub"]] += 1
            e[c["hub"]] += c["m1"] - c["m0"]
    return n, e


def edge_dist(wh):
    v = wh / 1e6
    return 0.05 - abs(v - round(v, 1))


def device_wh(H, charges):
    """Per hub, January to October 2026: the energy the load bank tests put on the registers, and the energy left
    between a dropped record's closing register and its resumption's opening one."""
    hubs = [h["code"] for h in H["hubs"]]
    test = {h: 0 for h in hubs}
    gap = {h: 0 for h in hubs}
    for c in charges:
        if c["model"] != "HX150" or c["failed"] or not (A.WIN_A <= c["start"] < A.WIN_B):
            continue
        if c["auth"] == "test":
            test[c["hub"]] += c["m1"] - c["m0"]
        for i in range(1, len(c["recs"])):
            gap[c["hub"]] += max(0, c["recs"][i]["m0"] - c["recs"][i - 1]["m1"])
    return test, gap


def charges_clear(H):
    salt = {}
    for _ in range(16):
        ch = W.charges_2026(H, salt=salt)
        n, e = clean_asks(H, ch)
        test, gap = device_wh(H, ch)
        bad = [h for h in e if edge_dist(e[h]) < EDGE or abs(test[h] - gap[h]) < SEP_WH or n[h] % 100 == 0
               or round((e[h] + test[h]) / 1e6, 1) == round(e[h] / 1e6, 1) or edge_dist(e[h] + test[h]) < EDGE / 2]
        if not bad:
            return ch, salt
        for h in bad:
            salt[h] = salt.get(h, 0) + 1
    raise SystemExit("energy figures not clear of their rounding edges or their devices cancel: %s" % bad)


def write_golden_csv(path, H, sides, n, e):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["hub_code", "hub", "below_99_per_cent_2027", "charges_jan_oct_2026", "energy_jan_oct_2026_mwh"])
    for h in sorted(H["hubs"], key=lambda h: h["code"]):
        w.writerow([h["code"], h["name"], "Yes" if h["code"] in sides else "No", n[h["code"]], "%.1f" % e[h["code"]]])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def write_letter(path, H, gold_set, F):
    P, T, BODY, SMALL, H2 = PK.P, PK.T, PK.BODY, PK.SMALL, PK.H2
    names = {h["code"]: h["name"] for h in H["hubs"]}
    long = [c for c in gold_set if c in F["already_codes"]]
    prog = [c for c in gold_set if c not in F["already_codes"]]
    rows = [["Hub code", "Hub", "Why it is listed", "Action proposed"]]
    for c in sorted(long, key=lambda c: names[c]):
        rows.append([c, names[c], "HX150 units hang two or three times a year on the record; each hang waits for a technician",
                     "Planned restart of each HX150 within 60 days of its last power-up"])
    for c in sorted(prog, key=lambda c: names[c]):
        rows.append([c, names[c], "RC50 removed under the programme; the HX150 units will run months between power-ups",
                     "Planned restart of each HX150 within 60 days of its last power-up"])
    story = [P("Ardvane Charge DAC", PK.LEAF_H),
             P("Network Operations, Unit 4 Lissane Business Park, Mullingar, Co. Westmeath  |  Registered in Ireland, no. 641127", SMALL),
             Spacer(1, 6),
             P("6 November 2026<br/>Our ref: ARV/NP/2026/114", BODY),
             P("Ailis Fee<br/>Concession Manager<br/>North Midlands Charging Partnership", BODY),
             Spacer(1, 4),
             P("<b>Availability Plan for the 2027 Contract Year (Schedule 4, paragraph 4.6)</b>", BODY),
             P("Dear Ailis,", BODY),
             P("Please find our Availability Plan for 2027 and the Schedule 6 return attached (hub_availability_2027.csv). On the "
               "asset base the Asset Renewal Programme 2027 sets, we forecast that a high-power charge point will fall below the 99 "
               "per cent standard at the %d hubs below, and the Plan lists them under paragraph 4.6." % len(gold_set), BODY),
             T(rows, [17, 40, 62, 55]),
             P("Source: back-office status history 1 January 2023 to 31 October 2026; planned maintenance schedule, 2027 plan "
               "sheet; Asset Renewal Programme 2027. Availability as Schedule 4, paragraph 4.3 defines it, with notified visits "
               "and supply interruptions excluded.", SMALL),
             P("The forecast reads each HX150's controller hangs on the days since the unit last powered up. On the 2023 to 2026 "
               "record no HX150 hung before %d days without a power-up, and every unit at a hub restarts when its supply pillar is "
               "isolated. Where an RC50 shares the HX150 units' pillar, its monthly cabinet service has kept those spells to a few "
               "weeks; at the five hubs where the HX150 units have a pillar of their own, they run for months and hang. Once the "
               "programme takes the RC50 out, the seven standard hubs above keep only two planned visits a year and few supply "
               "interruptions, so their HX150 units will run as long." % F["first_hang_day"], BODY),
             P("The programme's three motorway hubs are not listed: their two-monthly planned visits restart the HX150 units well "
               "inside that span. Annagh Cross and Cloonfin Crossroads are not listed either, because supply interruptions on their "
               "rural spurs restart the units several times a year.", BODY),
             P("We would welcome the chance to agree the restart arrangements at the December review. The return gives each hub's "
               "high-power charges and energy for January to October 2026 under Schedule 6.", BODY),
             P("The new HX150 units at the ten programme hubs that receive one are forecast from their commissioning on the "
               "works date, the first power-up they will have.", SMALL),
             P("Yours sincerely,", BODY),
             Spacer(1, 10),
             P("Sorcha Jackman<br/>Network Performance Lead, Ardvane Charge DAC", BODY)]
    officepdf.build(path, story, "Availability Plan 2027", "Sorcha Jackman", "Availability Plan for the 2027 Contract Year",
                    "Ardvane Charge DAC, Availability Plan 2027", dt.datetime(2026, 11, 6, 15, 12, 40, tzinfo=dt.timezone.utc),
                    dt.datetime(2026, 11, 6, 15, 31, 9, tzinfo=dt.timezone.utc), producer="LibreOffice 24.8", font="Carlito",
                    body_pt=10, page_of=True)


def metadata(info):
    files = {
        PK.F_STATUS: "The operator's back-office status export for every charge point, 1 January 2023 to 31 October 2026, UTC.",
        PK.F_SESS: "The back office's session export for 1 January to 31 October 2026, UTC.",
        PK.F_DSO: "The operator's log of supply interruptions notified by the distribution system operator, Irish time.",
        PK.F_REG: "The operator's asset register: charge points with current and previous IDs, and hubs.",
        PK.F_WO: "The two maintenance contractors' work orders, compiled by the operator, Irish time.",
        PK.F_PPM: "The maintenance contractor's planned visit schedule, 2023 to 2026 and the 2027 plan.",
        PK.F_SURVEY: "The operator's spring 2026 customer survey responses.",
        PK.F_SCHED: "Schedules 4 and 6 of the concession agreement, consolidated text of March 2024.",
        PK.F_PROG: "The partnership's Asset Renewal Programme 2027, approved 21 October 2026.",
        PK.F_TARIFF: "The operator's public charging tariff from 1 March 2026."}
    return {
        "task": "task156",
        "decision": "the hubs a rapid-charging operator lists in its 2027 availability plan, and each hub's January to "
                    "October 2026 high-power charges and energy",
        "deliverables": ["hub_availability_2027.csv", "availability_plan_2027.pdf"],
        "distractor_files": ["target/" + f for f in PK.DISTRACTORS],
        "files": [{"path": "target/" + f, "source": "constructed for this task; no real dataset", "date": "2026-11-02",
                   "licence": "CC0 1.0 (constructed)", "covers": files[f]} for f in PK.FILES],
        "rows": {"status_history": info["status_rows"], "sessions": info["session_rows"], "supply_interruptions": info["dso_rows"]},
    }


def main(out=TASK):
    target = os.path.join(out, "target")
    golden_dir = os.path.join(out, "golden")
    os.makedirs(golden_dir, exist_ok=True)
    H = W.history()
    T27 = W.truth_2027(H, reps=300)
    truth_set = ES.side_set(T27)
    charges, salt = charges_clear(H)
    info = PK.build_pack(H, charges, target)
    R = PA.read_pack(target)
    G = ES.golden(R)
    assert G["set"] == truth_set, (G["set"], truth_set)
    naive = ES.side_set(ES.route_rates(R, G["C"], G["E"]))
    n, e_mwh, e_wh = A.golden(target)
    hubs = {h["code"]: h for h in H["hubs"]}
    already = [c for c in G["set"] if c in naive]
    first_day = int(np.nonzero(G["ev"])[0].min())
    F = dict(call=sorted(hubs[c]["name"] for c in G["set"]), call_codes=G["set"], call_count=len(G["set"]),
             naive=sorted(hubs[c]["name"] for c in naive), naive_count=len(naive),
             already_codes=already, programme_listed=sorted(hubs[c]["name"] for c in G["set"] if c not in already),
             first_hang_day=first_day, hangs_on_record=int(G["ev"].sum()),
             sides={hubs[c]["name"]: ("Yes" if c in G["set"] else "No") for c in hubs},
             charges={hubs[c]["name"]: n[c] for c in hubs}, energy_mwh={hubs[c]["name"]: e_mwh[c] for c in hubs},
             standard_per_cent=99, salt=salt, pack=info,
             hub_rows=[[c, hubs[c]["name"]] for c in sorted(hubs)])
    write_golden_csv(os.path.join(golden_dir, "hub_availability_2027.csv"), H, G["set"], n, e_mwh)
    write_letter(os.path.join(golden_dir, "availability_plan_2027.pdf"), H, G["set"], F)
    os.makedirs(os.path.join(out, "generator"), exist_ok=True)
    json.dump(F, open(os.path.join(out, "generator", "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(info), open(os.path.join(out, "metadata.json"), "w"), indent=1)
    __import__("writeup").main(out)
    stamp = PK.EXPORT.timestamp()
    for f in ("hub_availability_2027.csv", "availability_plan_2027.pdf"):
        os.utime(os.path.join(golden_dir, f), (stamp + 4 * 86400, stamp + 4 * 86400))
    print("call", len(G["set"]), F["call"])
    print("naive", len(naive), F["naive"])
    print("pack", info)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else TASK)
