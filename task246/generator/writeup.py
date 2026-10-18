"""task246 figures and write-up: every figure the goldens, figures.json and submission.md carry, computed once from the
shipped pack (solve.py), and the write-up drafted from them."""
import json

import numpy as np
import pandas as pd

import estim as E
import params as P
import solve

WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve"}
ZNAME = {code: name for code, name, *_r in P.ZONES}
ZSUB = {code: sub for code, name, sub, *_r in P.ZONES}


def band(x):
    out = P.BANDS[0][1]
    for lo, name in P.BANDS:
        if round(x, 1) >= lo:
            out = name
    return out


def device_evidence(target, F):
    """what makes the dictionary's version 4 codes wrong before 21 June: who was visited again, and who left"""
    day4 = solve.form_v4_day(target, F)
    v = pd.read_csv(solve._p(target, F, "visits"))
    v["day"] = [solve._dmy(d) for d in v.date]
    again = set((int(r.cluster), int(r.hh_no)) for r in v[v.visit == 2].itertuples())
    out = {"switch_day": day4.isoformat()}
    for per, sel in (("before", v.day < day4), ("from", v.day >= day4)):
        f = v[(v.visit == 1) & sel]
        for code in (3, 4):
            g = f[f.outcome == code]
            out["%s_outcome%d" % (per, code)] = [len(g), int(sum((int(r.cluster), int(r.hh_no)) in again
                                                                for r in g.itertuples()))]
    m = solve._members(target, F)
    yrs = m.age / np.where(m.age_unit == "months", 12.0, 1.0)
    for per, sel in (("before", m.day < day4), ("from", m.day >= day4)):
        for code in (3, 4):
            g = sel & (m.left_reason == code)
            out["%s_reason%d" % (per, code)] = [int(g.sum()), int((yrs[g] >= 15).sum()), int((yrs[g] < 5).sum())]
    return out


def figures(target, F):
    A = solve.answer(target, F)
    ZF, T, df = A["ZF"], A["T"], A["df"]
    call = A["noted"]
    resp, mort = solve.response(target, F), solve.mortality(target, F)
    zones = []
    for z in P.ZCODES:
        Z = ZF[z]
        d = df[df.zone == z]
        own = Z[E.REFERENCE]
        rec = dict(code=z, name=ZNAME[z], sub_county=ZSUB[z], children=int(len(d)), oedema=int(d.oedema.sum()),
                   anthropometrists=sorted(set(d.measurer)),
                   readings=round(Z["readings"], 1), own=round(own, 1),
                   own_range=[round(A["lo"][z], 1), round(A["hi"][z], 1)],
                   points=E.points(Z, E.REFERENCE), points_size=abs(E.points(Z, E.REFERENCE)), note=z in call,
                   published=round(own if z in call else Z["readings"], 1),
                   band=band(own if z in call else Z["readings"]), readings_band=band(Z["readings"]),
                   response=round(resp[z], 1), cdr=round(mort[z][0], 2), u5dr=round(mort[z][1], 2))
        zones.append(rec)
    test = []
    order = [P.MEASURERS[k][2] for k in P.MEASURERS]
    for a in sorted(T, key=order.index):
        t = T[a]
        test.append(dict(name=a, offset=round(t["b"], 1), tem=round(float(np.sqrt(t["tem2"])), 1),
                         departure_sd=round(float(np.sqrt(t["fe"])), 1), readings=2 * t["n"]))
    rungs = {k: E.noted(ZF, k) for k in E.RUNGS}
    constants = dict(cut_mm=P.CUT, note_points=P.NOTE_POINTS, ages_months=[6, 59], muac_valid_mm=[75, 220],
                     resent_june=22, switch_june=21, refresher_june=P.REFRESHER.day, rate_per=10000, adult_years=15,
                     cm_to_mm=10, protocol_sections=[2, 5, 6, 7, 9, 10])
    return dict(call=call, zones=zones, test=test, rungs=rungs, reference=E.REFERENCE, variants=len(E.VARIANTS),
                evidence=device_evidence(target, F), note_points=P.NOTE_POINTS, constants=constants)


def _rows(fig):
    return {s["code"]: s for s in fig["zones"]}


def _signed(x):
    return "0.0" if abs(x) < 0.05 else "%+.1f" % x


def _list(vals):
    return ", ".join(vals[:-1]) + " and " + vals[-1] if len(vals) > 1 else vals[0]


def _test(fig, names):
    t = {r["name"]: r for r in fig["test"]}
    return [t[n] for n in names]


SCATTER = ["Steve Abdikadir", "Joan Bashir", "Cosmas Kibet"]     # North Lakeshore, West Pastoral, West Riverine


def golden_content(fig):
    S = _rows(fig)
    noted = [S[c] for c in fig["call"]]
    k, rest = WORD[len(noted)], WORD[len(S) - len(noted)]
    sc = _test(fig, SCATTER)
    off = [r for r in fig["test"] if abs(r["offset"]) >= 1.0]
    paras = [
        "<b>%s of the twelve zones' long-rains wasting figures carry the measurement note: %s.</b> In each, the figure "
        "from the MUAC readings and the figure from the children's own arm circumference differ by 2.0 points or more "
        "(%s), so under protocol section 7 the zone goes into the bulletin at its children's own figure, marked with the "
        "note. The other %s zones go in at their readings' figure, without the note." % (
            k.capitalize(), _list([s["name"] for s in noted]),
            _list(["%s %+.1f" % (s["name"], s["points"]) for s in noted]), rest),
        "Two kinds of error move the readings. %s anthropometrists read %.1f to %.1f mm off the supervisor at the "
        "standardisation sessions (a tight or loose pull), which shifts the whole zone; three others (%s) repeat their "
        "own reading of a child closely (repeat error %s mm) but depart from the supervisor child to child by %s mm, which widens the "
        "zone's spread and puts more children on either side of 125 mm. Each reading is corrected by its "
        "anthropometrist's offset, and the spread by the variance of its single readings' departures from the "
        "supervisor about that offset; the test's repeat error alone would miss the second kind and note four zones." % (
            WORD[len(off)].capitalize(), min(abs(r["offset"]) for r in off), max(abs(r["offset"]) for r in off),
            _list([r["name"] for r in sc]), _list(["%.1f" % r["tem"] for r in sc]),
            _list(["%.1f" % r["departure_sd"] for r in sc])),
        "Central Pastoral's anthropometrist pulls the tape loose, so its readings understate wasting: its children's "
        "own figure is %.1f per cent against %.1f from the readings. The response and death rates for the annex are in "
        "the workbook." % (S["CP"]["own"], S["CP"]["readings"]),
    ]
    return dict(zones=fig["zones"], call=fig["call"],
                title="%s zones' wasting figures carry the measurement note" % k.capitalize(),
                chart_title="Figures from the readings and from the children's own arm circumference",
                paras=paras,
                footnote="Acute malnutrition by MUAC, children 6 to 59 months: MUAC below 125 mm read from the normal "
                         "distribution, bilateral oedema counted (protocol sections 6 and 7). Own arm circumference: each "
                         "reading less its anthropometrist's offset against the supervisor, the spread less the variance "
                         "of the anthropometrist's departures from the supervisor about that offset; ranges in the "
                         "workbook.")


def write_figures(path, fig):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")


def submission(fig):
    S = _rows(fig)
    noted = [S[c] for c in fig["call"]]
    others = [s for s in fig["zones"] if not s["note"]]
    k, rest = WORD[len(noted)], WORD[len(S) - len(noted)]
    sc = _test(fig, SCATTER)
    ev = fig["evidence"]
    r2 = [S[c] for c in fig["rungs"]["R2_offset_repeat"]]
    r5 = [S[c] for c in fig["rungs"]["R5_offset_mse"] if c not in fig["call"]]
    lines = []
    w = lines.append
    w("# task246 submission")
    w("")
    w("## Tags")
    w("")
    w("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a county nutrition "
      "surveillance round's MUAC readings, each zone's wasting prevalence net of its anthropometrists' offset and error "
      "against the supervisor).")
    w("**Analytical objective:** Data Quality Monitoring & Alerting (which zones' 2027 long-rains wasting figures carry "
      "the measurement note into the early warning bulletin, with each zone's household response and death rates for "
      "the annex).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    lower = [s["name"] for s in noted if s["points"] < 0]
    w("**%s of the twelve zones' figures carry the measurement note: %s, whose figures from the readings and from their "
      "children's own arm circumference differ by %s points; the other %s zones carry no note.**" % (
          k.capitalize(), _list([s["name"] for s in noted]), _list(["%.1f" % s["points_size"] for s in noted]), rest))
    w("")
    w("In %s the readings' figure is the lower one; in the other %s it is the higher." % (
        _list(lower), WORD[len(noted) - len(lower)]))
    w("")
    w("The children's own figure takes each anthropometrist's offset against the supervisor out of its readings and the "
      "variance of its single readings' departures from the supervisor about that offset out of the zone's spread. Not "
      "the %s zones the test's repeat error gives (%s), which misses %s: their anthropometrists' repeat error (TEM) is "
      "%s mm but they depart from the supervisor child to child by %s mm. Not the %s zones the mean squared departure gives, "
      "which counts the offset twice and adds %s." % (
          WORD[len(r2)], _list([s["name"] for s in r2]),
          _list([s["name"] for s in noted if s not in r2]), _list(["%.1f" % r["tem"] for r in sc]),
          _list(["%.1f" % r["departure_sd"] for r in sc]), WORD[len(fig["rungs"]["R5_offset_mse"])],
          _list([s["name"] for s in r5])))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Each anthropometrist's offset against the supervisor, in mm: **%s**." % "; ".join(
        "%s %s" % (r["name"], _signed(r["offset"])) for r in fig["test"]))
    w("2. Each anthropometrist's departure from the supervisor about its offset, standard deviation in mm: **%s**." %
      "; ".join("%s %.1f" % (r["name"], r["departure_sd"]) for r in fig["test"]))
    w("3. The %s noted zones' figures from the readings and from the children's own arm circumference (accepted "
      "range), per cent: **%s**." % (k, "; ".join("%s %.1f and %.1f (%.1f to %.1f)" % (
          s["name"], s["readings"], s["own"], s["own_range"][0], s["own_range"][1]) for s in noted)))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    steps = [
        "Children from the two anthropometry exports: NCHA's MUAC in mm with the age in completed months from dob to "
        "today, team 2's rows of 22 June sent twice taken once (each child once, protocol section 6); PRK's MUAC in cm "
        "times ten with Age (months); children 6 to 59 months, MUAC from 75 to 220 mm or oedema; each cluster's zone "
        "from the cluster sample; the anthropometrist on duty from the teams workbook (PRK team 4's from the cluster of "
        "28 June).",
        "Each zone's figure from the readings (section 6): oedema counted, the rest's share below 125 mm read from the "
        "normal with the readings' mean and standard deviation.",
        "The standardisation test (section 5): each anthropometrist's readings of the test children against the "
        "supervisor's mean of her two readings, both sessions together: the offset is the mean departure, and the "
        "random error the variance of the single readings' departures about it; the scattered three depart by %s mm "
        "with a repeat error (TEM) of %s mm." % (_list(["%.1f" % r["departure_sd"] for r in sc]),
                                           _list(["%.1f" % r["tem"] for r in sc])),
        "Each zone's figure from the children's own arm circumference (sections 6 and 7): each reading less its "
        "anthropometrist's offset, the variance of those values less the mean random error of the readings' "
        "anthropometrists, the share below 125 mm read the same way; the accepted range runs over the standard "
        "variants (the correction made by zone, sessions apart, divisors n, the reference's own error, only offsets "
        "that stand out, the error through the children's means), %s readings that give the same notes." % WORD[fig["variants"]],
        "The note (section 7): the two figures to one decimal differ by 2.0 points or more in %s (the readings' figure "
        "less the children's own)." % _list(["%s (%+.1f)" % (s["name"], s["points"]) for s in noted]),
        "Household response (section 10) from the county's household visits: each selected household's last visit, "
        "interviewed over selected less empty dwellings; before 21 June the form coded an absent household 3 and an "
        "empty dwelling 4, the dictionary's version 4 the other way round (all %d households coded 3 at a first visit "
        "before 21 June were visited again and none of the %d coded 4; from 21 June none of %d coded 3 and all %d coded "
        "4, section 2)." % (ev["before_outcome3"][0], ev["before_outcome4"][0], ev["from_outcome3"][0],
                            ev["from_outcome4"][0]),
        "Death rates (section 9) from the member rosters and the births module: each member once (one cluster's forms "
        "were sent twice); a death is status D, a member who left because they died away from home, or a newborn who "
        "died on the births module; before 21 June the reasons 3 and 4 also ran the other way round (%d of the %d "
        "members coded 3 then are 15 or older, and none coded 3 from 21 June is); the mid-point population times the "
        "recall days from the sub-county's start event (Annex B), per 10,000 a day; under-fives are the members aged in "
        "months." % (ev["before_reason3"][1], ev["before_reason3"][0]),
    ]
    for j, st in enumerate(steps, 1):
        w("%d. %s" % (j, st))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### lr2027_muac_measurement_review.xlsx")
    w("")
    w("1. Zones, 12 rows in the protocol's order: figure from the MUAC readings, figure from the children's own arm "
      "circumference (accepted range), per cent to one decimal, and the measurement note:")
    for s in fig["zones"]:
        w("   - %s: %.1f; %.1f (%.1f to %.1f); %s" % (s["name"], s["readings"], s["own"], s["own_range"][0],
                                                  s["own_range"][1], "note" if s["note"] else "no note"))
    w("2. Household response rate, per cent to one decimal:")
    for s in fig["zones"]:
        w("   - %s %.1f" % (s["name"], s["response"]))
    w("3. Crude death rate, deaths per 10,000 people per day to two decimals:")
    for s in fig["zones"]:
        w("   - %s %.2f" % (s["name"], s["cdr"]))
    w("4. Under-five death rate, deaths per 10,000 children under five per day to two decimals:")
    for s in fig["zones"]:
        w("   - %s %.2f" % (s["name"], s["u5dr"]))
    w("")
    w("### lr2027_gam_measurement_note.pdf")
    w("")
    w("- One page for the bulletin desk: %s zones carry the note (%s), and a chart of each zone's figure from the "
      "readings and from its children's own arm circumference against the Normal, Alert, Alarm and Emergency bands, "
      "the noted zones marked." % (k, _list([s["name"] for s in noted])))
    w("")
    return "\n".join(lines)
