"""The office's disclosure system: its entity list, every annual disclosure for 2021 to 2026 with each submitted
version's items, and the submission history.

A faculty member holding an appointment on 31 December files an annual disclosure for that calendar year by
15 January, 11:59 p.m. Eastern; the system opens on 1 December and keeps its clock in UTC. Each version reports what
each company had paid by the day it was submitted (people.lines_at). Items name an entity picked from the office's list
(the list keeps each entity's id, its present name and, for manufacturers, their Open Payments ID) or typed by the
faculty member. The 2024 edition of the form changed the relationship types. Faculty amend disclosures (some December
filers in January, once the year's last payments are in), and the office returns some for correction; every submitted
version's items stay in the export. The system keys a disclosure to the employee number it knew when the faculty
member's record was created."""
import datetime as dt

import numpy as np

import people as PE
import world as W

D = dt.date
UTC = dt.timezone.utc
DEADLINE_UTC = PE.DEADLINE_UTC
PULL_UTC = dt.datetime(2027, 1, 21, 9, 0, tzinfo=UTC)


def entity_list(mfrs):
    """The office's list: every manufacturer with its Open Payments ID and present name, and the companies outside
    Open Payments that faculty have named often enough for the office to add them (the two that began reporting for
    2025 still among them, as the office entered them in 2022)."""
    r = np.random.default_rng([W.SEED, 21])
    out = []
    eid = 10200
    for m in mfrs:
        if m.get("now_reporting"):
            continue
        eid += int(r.integers(1, 40))
        out.append({"entity_id": "ENT-%05d" % eid, "name": m["name"], "op_id": m["id"], "state": m["state"],
                    "type": "Applicable manufacturer", "mfr": m})
    listed = [c for c, _ in W.NONREPORTING[:7]] + list(W.NOW_REPORTING)
    for c in listed:
        eid += int(r.integers(1, 40))
        out.append({"entity_id": "ENT-%05d" % eid, "name": c, "op_id": "",
                    "state": W.NOW_REPORTING_STATE.get(c) or str(r.choice(["OH", "NY", "MA", "CA", "IL"])),
                    "type": "Other company", "mfr": None})
    return out


def _secs(r, lo_h, hi_h):
    return dt.timedelta(seconds=int(r.integers(int(lo_h * 3600), int(hi_h * 3600))))


def build(fac, mfrs):
    """Disclosures, items and the submission history; returns (disclosures, items, events, entities)."""
    ents = entity_list(mfrs)
    by_op = {e["op_id"]: e for e in ents if e["op_id"]}
    by_company = {e["name"]: e for e in ents if not e["op_id"]}
    renamed = {m["id"]: W.former_name(m) for m in mfrs if m["index"] in W.RENAMED}
    nowrep = {m["id"]: m["name"] for m in mfrs if m.get("now_reporting")}
    nr_names = {c for c, _ in W.NONREPORTING}
    rel_of = {}
    disclosures, items, events = [], [], []
    seq = {}
    equity = _equity_holders(fac)
    for f in fac:
        rr = np.random.default_rng([W.SEED, 23, int(f.emp_id)])
        bg = f.group == "bg"
        typist = bg and rr.random() < 0.18          # types entity names rather than picking them
        amender = bg and rr.random() < 0.09
        rels = {PE.key_of(rel): rel for rel in f.rels}
        for y in W.YEARS:
            if not f.owes(y) or f.filing.get(y) is None:
                continue
            seq[y] = seq.get(y, 4000 + 37 * (y - 2020)) + int(rr.integers(1, 9))
            did = "COI-%d-%05d" % (y, seq[y])
            t1 = f.filing[y]
            names = {}                                 # each company's entry, chosen once for the disclosure

            def entry(key):
                if key in names:
                    return names[key]
                rel = rels[key]
                if rel["mfr"] is not None and rel["mfr"] in nowrep:
                    names[key] = (by_company[nowrep[rel["mfr"]]]["entity_id"], nowrep[rel["mfr"]])
                elif rel["mfr"] is not None:
                    e = by_op[rel["mfr"]]
                    shown = W.former_name(e["mfr"]) if (rel["mfr"] in renamed and D(y + 1, 1, 10) < W.RENAMED_ON) else e["name"]
                    if y == 2026 and rel["mfr"] in renamed and bg and (rel.get("typed_former") or rr.random() < 0.8):
                        names[key] = ("", renamed[rel["mfr"]])           # typed under the former name
                    elif typist and rr.random() < 0.35:
                        names[key] = ("", e["name"])                     # typed, the present name
                    else:
                        names[key] = (e["entity_id"], shown)
                else:
                    c = rel["company"]
                    if c in by_company and not (typist and rr.random() < 0.5):
                        names[key] = (by_company[c]["entity_id"], c)
                    else:
                        names[key] = ("", c)
                return names[key]

            extra = []
            if bg and rr.random() < 0.015:
                extra.append(("", "Royalty income, Marrowfield University technology license", "Royalties or licensing",
                              float(rr.integers(2, 30)) * 500.0))
            for c in equity.get((f.emp_id, y), []):
                extra.append((by_company[c]["entity_id"], c, "Equity", None))

            def version_lines(t, perturb=None):
                got = PE.lines_at(f, y, t)
                out = []
                for key in sorted(got, key=str):
                    e, nm = entry(key)
                    out.append((e, nm, W.form_type(rels[key]["kind"], y), got[key], key))
                if perturb is not None and out:
                    k, fac_ = perturb
                    k = k % len(out)
                    e, nm, ty, d, key = out[k]
                    out[k] = (e, nm, ty, max(100.0, round(d * fac_ / 100) * 100), key)
                return out + [(e, nm, ty, d, None) for e, nm, ty, d in extra]

            lines = version_lines(t1)
            versions = [(1, "Submitted", t1, lines)]
            dec = PE.eastern_day(t1).year == y
            has_nr = any((not e and nm in nr_names) or (e and e in {x["entity_id"] for x in ents if not x["op_id"]})
                         for e, nm, ty, d, key in lines if ty not in ("Equity", "Royalties or licensing"))
            if y == 2026 and bg and t1 <= DEADLINE_UTC and rr.random() < 0.075:
                # the office's review after the deadline returns a disclosure for correction; the faculty member
                # resubmits it a day or two later
                t_ret = DEADLINE_UTC + _secs(rr, 8, 72)
                t2 = min(t_ret + _secs(rr, 6, 48), PULL_UTC - _secs(rr, 0.1, 5))
                if t2 > t_ret:
                    pert = (int(rr.integers(0, 50)), float(rr.uniform(0.7, 1.3))) if rr.random() < 0.5 else None
                    events.append((did, 1, "Returned for correction", t_ret, "Office"))
                    versions.append((2, "Resubmitted", t2, version_lines(t2, pert)))
            elif bg and dec and rr.random() < 0.12:
                # a December filer amends in January, once the year's last payments are in
                t2 = PE.filing_time(rr, y, "jan")
                if y == 2026:
                    t2 = min(t2, PULL_UTC - _secs(rr, 0.1, 20))
                if t2 > t1:
                    versions.append((2, "Amended", t2, version_lines(t2)))
            elif bg and (amender or rr.random() < 0.03 or (y == 2026 and has_nr and rr.random() < 0.35)) and rr.random() < 0.55:
                # an amendment, or a return for correction and a resubmission, some time after the first filing
                gap = _secs(rr, 20, 6 * 24) if y == 2026 else dt.timedelta(days=int(rr.integers(2, 120)), seconds=int(rr.integers(0, 86400)))
                t2 = t1 + gap
                if t2 > PULL_UTC + dt.timedelta(hours=6):
                    t2 = PULL_UTC - _secs(rr, 0.1, 15)
                if t2 > t1:
                    cand = version_lines(t2)
                    nr = [k for k, (e, nm, ty, d, key) in enumerate(cand)
                          if key is not None and rels[key]["mfr"] is None]
                    if nr and y == 2026:
                        k = nr[int(rr.integers(len(nr)))]
                        e, nm, ty, d, key = cand[k]
                        cand[k] = (e, nm, ty, max(100.0, round(d * float(rr.choice([0.5, 0.75, 1.5, 2.0])) / 100) * 100), key)
                    elif cand and rr.random() < 0.6:
                        movable = [k for k, row in enumerate(cand) if row[4] is not None]
                        if movable:
                            k = movable[int(rr.integers(len(movable)))]
                            e, nm, ty, d, key = cand[k]
                            cand[k] = (e, nm, ty, max(100.0, round(d * float(rr.uniform(0.6, 1.4)) / 100) * 100), key)
                    returned = rr.random() < 0.35
                    if returned:
                        events.append((did, 1, "Returned for correction", t1 + (t2 - t1) / 2, "Office"))
                    versions.append((2, "Resubmitted" if returned else "Amended", t2, cand))
            for v, ev, t, ls in versions:
                events.append((did, v, ev, t, "Faculty"))
                for k, (e, nm, ty, d, key) in enumerate(ls, start=1):
                    items.append({"disclosure_id": did, "version": v, "item_no": k, "entity_id": e, "entity_name": nm,
                                  "relationship_type": ty, "amount": d})
            last = versions[-1]
            disclosures.append({"disclosure_id": did, "emp_id": f.emp_id, "year": y,
                                "edition": "2024" if y >= W.FORM_CHANGE else "2021", "version": last[0],
                                "status": last[1], "last_submitted": last[2], "f": f})
    events.sort(key=lambda e: (e[3], e[0], e[1]))
    return disclosures, items, events, ents


def _equity_holders(fac):
    """Faculty who have held equity in the two companies since 2022 and disclose it each year:
    {(emp_id, year): [company]}."""
    r = np.random.default_rng([W.SEED, 24])
    pool = [f for f in fac if f.group == "bg" and f.cred in ("MD", "DO") and f.owes(2022) and f.owes(2026)
            and f.dept in ("IMED", "NEUR", "PSYC", "HEON", "GAST")]
    out = {}
    for c in W.NOW_REPORTING:
        for k in r.choice(len(pool), size=4, replace=False):
            f = pool[int(k)]
            for y in range(2022, 2027):
                out.setdefault((f.emp_id, y), []).append(c)
    return out
