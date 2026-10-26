"""The asks for task270, read from the shipped pack.

Ask F: each schedule's share of the 18 to 34 universe reached at least once (the brief's reading, as the call).
Ask R: the April 2025 campaign's response, from the Portal do Dador's booking extract under the rule in its
extraction notes: each person counted once, at the date of the first first-donation booking they made, aged 18 to 34
that day, whatever the outcome; the four weeks before the campaign's weekly average, each campaign week's bookings
above it, and the weeks' sum above it per thousand adults 18 to 34 the campaign reached three or more times as
Meridiano Media's report gives them.
Ask X: each schedule's expected first-donation bookings at that response.

route "golden" takes a person to be the identity document (documento_hash); the other routes are the same code with
one reading changed: "donor" (a person is a donor number, so a re-registration after the portal's go-live opens a
second person), "donor_open" (the same, cancelled bookings dropped) and "document_open" (the identity document,
cancelled bookings dropped)."""
import csv
import datetime as dt
import os

import common as K
import side2025 as S

REPORT_REACHED3 = 547.8          # Pessoas (milhares), 3 ou mais, as the 2025 report prints it


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def age_on(born, day):
    return day.year - born.year - ((day.month, day.day) < (born.month, born.day))


def weekly(days, start, weeks=4):
    out = [0] * weeks
    for d in days:
        k = (d - start).days // 7
        if 0 <= k < weeks:
            out[k] += 1
    return out


def response(target, route="golden"):
    key = "documento_hash" if route in ("golden", "document_open") else "id_dador"
    drop = route in ("donor_open", "document_open")
    first = {}
    for r in rows(os.path.join(target, K.FILES["portal"])):
        if r["tipo_dadiva"] != "primeira" or (drop and r["estado"] == "cancelada"):
            continue
        made = dt.datetime.strptime(r["criada_em"], "%Y-%m-%d %H:%M:%S")
        if r[key] not in first or made < first[r[key]][0]:
            first[r[key]] = (made, dt.date.fromisoformat(r["data_nascimento"]))
    days = [m.date() for m, b in first.values() if 18 <= age_on(b, m.date()) <= 34]
    base, camp = weekly(days, S.BASELINE[0]), weekly(days, S.CAMPAIGN[0])
    avg = sum(base) / 4.0
    above = [c - avg for c in camp]
    return dict(base=base, camp=camp, avg=avg, above=above, extra=sum(above),
                per_thousand=sum(above) / REPORT_REACHED3)


def universe_young(target):
    return sum(int(r["populacao"]) for r in rows(os.path.join(target, K.FILES["universe"]))
               if r["escalao_etario"] in K.YOUNG)


def expected_bookings(per_thousand, reach3, universe):
    return {s: per_thousand * reach3[s] * universe / 1000.0 for s in K.SCHED}


def all_asks(target, pack, route_main="golden", route_resp="golden"):
    """every ask figure, unrounded"""
    E = {s: pack.exposures(s, route_main) for s in K.SCHED}
    reach1 = {s: pack.reach(E[s], 1) for s in K.SCHED}
    reach3 = {s: pack.reach(E[s], 3) for s in K.SCHED}
    resp = response(target, route_resp)
    uni = universe_young(target)
    return dict(reach1=reach1, reach3=reach3, response=resp, universe=uni,
                bookings=expected_bookings(resp["per_thousand"], reach3, uni))
