"""figures.json and submission.md, both emitted from the golden computed on the shipped pack."""
import json

import solve as S

HOSP = {"CM": "Presidio di Castelmarne", "RB": "Presidio di Rivobello", "VD": "Presidio di Valdarena"}
QNAME = {1: "first quarter", 2: "second", 3: "third", 4: "fourth"}
WARD_ORDER = ["TIN", "NIDO", "TI", "DIAB", "PS", "MED", "CHIR", "PED", "OST", "MEDR", "PSR", "MEDV", "LUN"]


def _r1(x):
    return round(float(x) + 0.0, 1)


def figures(target):
    g = S.solve(target)
    D, P, e, listed = g["D"], g["P"], g["errors"], g["listed"]
    reg = D["reg"].set_index("matricola")
    sel = P["sched"] & P["since"] & P["num"].notna()
    n = P[sel].groupby("matricola").size()
    e1, l1 = S.call(D, P=P, population="all")
    unl = max((m for m in e if m not in listed), key=lambda m: abs(e[m]))
    lst = min(listed, key=lambda m: abs(e[m]))
    fig = {
        "call": {"listed": listed, "count": len(listed), "meters": len(e), "stay": len(e) - len(listed),
                 "error_listed_pct": {m: _r1(e[m]) for m in listed},
                 "ward": {m: reg.loc[m, "reparto"] for m in listed},
                 "hospital": {m: reg.loc[m, "presidio"] for m in listed},
                 "range_listed_pct": [_r1(min(e[m] for m in listed)), _r1(max(e[m] for m in listed))]},
        "components": {"scheduled_pairings": int(sel.sum()), "pairings_per_meter": [int(n.min()), int(n.max())],
                       "a_over_b": S.A_OVER_B,
                       "nearest_unlisted": {"meter": unl, "error_pct": _r1(e[unl])},
                       "nearest_listed": {"meter": lst, "error_pct": _r1(e[lst])}},
        "steps": {"pairings": int(len(P)), "pooled_list": l1,
                  "pooled_drops": sorted(set(listed) - set(l1)), "pooled_adds": sorted(set(l1) - set(listed)),
                  "pooled_error_pct": {m: _r1(e1[m]) for m in sorted(set(listed) ^ set(l1))},
                  "scheduled_error_pct": {m: _r1(e[m]) for m in sorted(set(listed) ^ set(l1))},
                  "window": ["6:00", "7:30"], "critical": [50, 400], "switch": "2027-09-13", "late_minutes": 120},
        "asks": {"late_share_pct": {h: {str(q): _r1(g["ask1"][(h, q)]) for q in (1, 2, 3, 4)} for h in HOSP},
                 "tests_2027": {w: int(g["ask2"][w]) for w in WARD_ORDER}},
    }
    fig["_golden"] = {"errors": e, "listed": listed, "reg": reg, "pairs_used": n, "ask1": g["ask1"], "ask2": g["ask2"],
                      "pooled": e1}
    return fig


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def _pct(x):
    return ("%+.1f" % x).replace("-", "−") if False else "%+.1f" % x


def submission(fig):
    c, comp, st, a = fig["call"], fig["components"], fig["steps"], fig["asks"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: bedside "
             "glucose meters' systematic error against the laboratory, read from meter and laboratory pairings).  ")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    L.append("## 1. Final Recommendation\n")
    lst = ", ".join("%s (%s)" % (m, c["ward"][m]) for m in c["listed"])
    drop, add = st["pooled_drops"], st["pooled_adds"]
    L.append("**Send %d of the %d meters to the 17 to 21 January 2028 recalibration: %s; the other %d stay on their "
             "wards.** On the pairings the plan drew on the morning round since each meter's January 2027 "
             "calibration, each listed meter's systematic error lies beyond 5 per cent, from %.1f to %+.1f per cent, "
             "and no other meter's is beyond %.1f per cent. Not the list from every pairing since the calibration: "
             "it counts the confirmations of critical readings, drawn because the meter itself read under 50 or "
             "over 400 mg/dL, which carry that reading's own error, so on the nursery it drops %s (%+.1f per cent on "
             "the scheduled pairings, %+.1f on all) and adds %s (%+.1f against %+.1f).\n"
             % (c["count"], c["meters"], lst, c["stay"], c["range_listed_pct"][0], c["range_listed_pct"][1],
                abs(comp["nearest_unlisted"]["error_pct"]), drop[0], st["scheduled_error_pct"][drop[0]],
                st["pooled_error_pct"][drop[0]], add[0], st["scheduled_error_pct"][add[0]],
                st["pooled_error_pct"][add[0]]))
    L.append("## 2. Critical Components\n")
    L.append("1. The pairings the plan drew, on the meter's planned day with the laboratory's draw between 6:00 and "
             "7:30, after each meter's last calibration: **%s pairings**, %d to %d per meter."
             % (format(comp["scheduled_pairings"], ","), comp["pairings_per_meter"][0], comp["pairings_per_meter"][1]))
    L.append("2. The laboratory's values drawn before 13 September 2027 divided by **%.3f**, the C600 against the "
             "C900." % comp["a_over_b"])
    L.append("3. The margin: the nearest listed meter, %s, at **%+.1f per cent**; the nearest unlisted, %s, at "
             "**%+.1f per cent**.\n" % (comp["nearest_listed"]["meter"], comp["nearest_listed"]["error_pct"],
                                       comp["nearest_unlisted"]["meter"], comp["nearest_unlisted"]["error_pct"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read the %s pairings in GlyLink_abbinamenti_laboratorio_2026-2027.xlsx, each a meter result and the "
             "laboratory's result on the tube whose barcode the meter read (POCT-GLU-02 sections 5 and 6)."
             % format(st["pairings"], ","))
    L.append("2. Kept the pairings the plan drew: the meter's days in piano_abbinamenti_glucometri_2026-2027.xlsx, a "
             "holiday moved to the next working day, with data_ora_prelievo between 6:00 and 7:30 (section 5); every "
             "other pairing is the confirmation of a reading under 50 or over 400 mg/dL (section 6), drawn because of "
             "the meter's own result, so it carries that result's error and does not measure the meter's bias.")
    L.append("3. Kept those after each meter's ultima_taratura in anagrafica_glucometri.xlsx with a numeric meter "
             "value, and divided the laboratory's values drawn before 13 September 2027 by 1.035 "
             "(nota_laboratorio_cambio_analizzatore_glicemia.pdf): %s pairings." % format(comp["scheduled_pairings"], ","))
    L.append("4. Took each meter's systematic error as the mean of its meter over laboratory ratios less one, the "
             "factor section 7 defines: %d meters lie beyond 5 per cent." % c["count"])
    L.append("5. Read GlyLink_risultati_2026-2027.csv's patient results once per matricola and n_memoria, keeping the "
             "first reception (a docking the meter never saw acknowledged re-sends its results under new "
             "id_risultato), each at data_ora_test less one hour (the meters' clocks keep solar time all year: in "
             "summer the scheduled pairings show the meter an hour before the laboratory's draw).")
    L.append("6. Placed each result on the ward and hospital where its meter stood on the test's date "
             "(anagrafica_glucometri.xlsx, Storico ubicazioni; the export's presidio and reparto are the meter's "
             "current assignment), and dated it in Italian civil time.")
    L.append("7. For 2027, took per hospital and quarter the share of results whose data_ora_ricezione came more than "
             "120 minutes after the test, and counted the results per ward (POCT-GLU-02 section 8).")
    L.append("8. Send the %d meters to the January 2028 visit; the other %d stay.\n" % (c["count"], c["stay"]))
    L.append("## 4. Deliverable Answers\n")
    L.append("### ritiro_glucometri_gennaio_2028.xlsx\n")
    L.append("1. The meters to recalibrate, %d (matricola, ward, hospital, systematic error):" % c["count"])
    for m in c["listed"]:
        L.append("   - %s, %s, %s: %+.1f per cent" % (m, c["ward"][m], c["hospital"][m], c["error_listed_pct"][m]))
    L.append("2. Share of 2027 patient results that reached the clinical record more than two hours after the test:")
    for h, name in HOSP.items():
        q = a["late_share_pct"][h]
        L.append("   - %s: first quarter %.1f per cent, second %.1f per cent, third %.1f per cent, fourth %.1f per "
                 "cent" % (name, q["1"], q["2"], q["3"], q["4"]))
    L.append("3. Patient tests performed in 2027, by ward:")
    for w in WARD_ORDER:
        L.append("   - %s: %s" % (w, format(a["tests_2027"][w], ",")))
    L.append("\n### errore_sistematico_glucometri_2027.png\n")
    L.append("4. Each of the %d meters' systematic error on the scheduled pairings since its last calibration, by "
             "hospital and ward, against the band from -5 to +5 per cent, the %d listed meters marked and labelled."
             % (c["meters"], c["count"]))
    return "\n".join(L) + "\n"
