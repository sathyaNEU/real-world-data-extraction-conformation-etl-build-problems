"""The large holders' quarterly dwelling returns, 2024T3 to 2026T2, as the portal holds them: every
version of every lodgement, building rows for lodgements before 1 April 2026 and dwelling rows from
then, scheduled sales on held rows, option and reservation rows, and the references as typed.
"""
import datetime as dt
import random

from common import D, SEED, QUARTERS, FORMAT_CHANGE, qlabel, workday
from history import CARRIED
from plan import SECTIONS
from world import GROUP_CODE, group_of

WATCH = {s["code"] for s in SECTIONS}
LAST_LODGED = {}
for _i, _h in enumerate(CARRIED):
    LAST_LODGED[_h] = D(2025, 12, 31) if _i % 2 else D(2025, 9, 30)
LAST_LODGED["Y1"] = D(2025, 12, 31)
LAST_LODGED["Y2"] = D(2025, 9, 30)


class Timeline:
    def __init__(self, own0, events):
        self.own0 = own0
        self.ev = sorted(events, key=lambda e: (e["date"], e["refs"][0]))

    def state(self, day):
        st = dict(self.own0)
        for e in self.ev:
            if e["date"] > day:
                break
            for r in e["refs"]:
                assert st.get(r) == e["before"][r], (r, e["date"], st.get(r), e["before"][r])
                st[r] = e["after"][r]
        return st


def next_workday(d):
    while not workday(d):
        d += dt.timedelta(days=1)
    return d


def units_text(units):
    units = sorted(units)
    out, i = [], 0
    while i < len(units):
        j = i
        while j + 1 < len(units) and units[j + 1] == units[j] + 1:
            j += 1
        out.append(f"{units[i]:04d}" if i == j else f"{units[i]:04d}-{units[j]:04d}")
        i = j + 1
    return ",".join(out)


def malform(ref, rng, kind=None):
    kind = kind or rng.choice(["space", "nodc", "dash"])
    if kind == "space":
        return (ref[:14] + " " + ref[14:]).lower()
    if kind == "nodc":
        return ref[:18]
    return f"{ref[:14]}-{ref[14:18]}-{ref[18:]}"


def build(holders, stock, timeline, book, people_nif):
    """Returns (rows, lodgements). people_nif maps an owner id to its NIF."""
    rng = random.Random(SEED * 19 + 2)
    sections, buildings, dwellings = stock
    watch = {s["code"]: s for s in SECTIONS}
    ids = sorted(h for h in holders if not h.startswith("old"))
    states = {q: timeline.state(q) for q in QUARTERS}
    held = {q: {} for q in QUARTERS}
    for q in QUARTERS:
        for r, o in states[q].items():
            if o in holders:
                held[q].setdefault(o, []).append(r)
    by_seller = {}
    for a in book.agreements:
        by_seller.setdefault(a["seller"], []).append(a)

    def scheduled(h, q, r):
        hit = [a for a in by_seller.get(h, []) if r in a["refs"] and a["made"] <= q < a["agreed"]]
        assert len(hit) <= 1, (h, q, r)
        if not hit:
            return None
        a = hit[0]
        b = a["buyers"][a["refs"].index(r)]
        return (a["agreed"].isoformat(), people_nif(b), str(a["price"]))

    # exposure rows: options and reservations, on privately owned watch dwellings and others' dwellings elsewhere
    expo = {}
    committed = {c["ref"] for c in book.commitments}
    for s in SECTIONS:
        code = s["code"]
        if s["role"] == "O4":
            h = "OPH"
        else:
            h = sorted(k for k in s["hold"] if k not in s["carried"] and k not in ("Y1", "Y2")
                       and not any(f[0] == "tk" and f[2] == k for f in s["flows"])
                       and (s["crow"] is None or k != s["crow"][0]))[0]
        pool = sorted(r for r, o in states[QUARTERS[-1]].items() if dwellings[r]["section"] == code
                      and o.startswith("p:") and r not in committed)
        rng.shuffle(pool)
        pick = pool[:s["oprs"]]
        for q in QUARTERS[-2:]:
            n = len(pick) if q == QUARTERS[-1] else max(1, len(pick) // 2)
            expo.setdefault((h, q), []).extend((r, "OP" if i % 3 else "RS") for i, r in enumerate(pick[:n]))
    nw_holders = [h for h in ids if h.startswith("nw") or h[0] in "GN"]
    for h in sorted(rng.sample(nw_holders, 12)):
        others = sorted(r for r, o in states[QUARTERS[0]].items() if o in holders and o != h
                        and dwellings[r]["section"] not in watch)
        pick = rng.sample(others, rng.randrange(2, 7))
        for qi, q in enumerate(QUARTERS):
            if rng.random() < 0.7 and h not in CARRIED:
                expo.setdefault((h, q), []).extend((r, rng.choice(["OP", "RS"])) for r in pick[: 1 + qi % len(pick)])

    def content(h, q):
        rows = []
        for r in sorted(held[q].get(h, [])):
            rows.append((r, "PD") + (scheduled(h, q, r) or ("", "", "")))
        for r, c in sorted(expo.get((h, q), [])):
            rows.append((r, c, "", "", ""))
        return rows

    lodgements = []
    seq = {q: 0 for q in QUARTERS}
    crow = {s["crow"][0]: (s["code"], s["crow"][1]) for s in SECTIONS if s["crow"]}
    watch_holders = {h for s in SECTIONS for h in s["hold"]}
    last_content = {}
    for qi, q in enumerate(QUARTERS):
        for h in ids:
            if h in LAST_LODGED and q > LAST_LODGED[h]:
                assert content(h, q) == last_content[h], f"carried holder {h} changed after its last return"
                continue
            rows = content(h, q)
            if not rows:
                continue
            if h.startswith("nw") and last_content.get(h) == rows and rng.random() < 0.5:
                continue
            last_content[h] = rows
            o_date = next_workday(q + dt.timedelta(days=rng.randrange(4, 31) if rng.random() < 0.93 else rng.randrange(31, 44)))
            if q == D(2026, 3, 31):
                o_date = max(o_date, D(2026, 4, 7))
            if q == QUARTERS[-1] and h in watch_holders:
                o_date = next_workday(q + dt.timedelta(days=rng.randrange(4, 30)))
            kind = None
            if q == QUARTERS[-1] and h in crow:
                kind = "C"
            elif q == QUARTERS[-1] and h in watch_holders:
                kind = "S" if rng.random() < 0.05 and h not in ("X1", "X2", "X3", "X4", "X5") else None
            else:
                x = rng.random()
                kind = "C" if x < 0.05 else ("S" if x < 0.09 else None)
            seq[q] += 1
            o_id = f"DGT-{qlabel(q)}-{seq[q]:05d}"
            held_rows = [x for x in rows if x[1] == "PD"]
            if kind == "C":
                if h in crow and q == QUARTERS[-1]:
                    code, c_rows = crow[h]
                    sec_rows = [x for x in held_rows if dwellings[x[0]]["section"] == code]
                    other = [x for x in held_rows if dwellings[x[0]]["section"] != code]
                    add = sec_rows[len(sec_rows) - c_rows:] if c_rows else []
                    add += other[:2]
                else:
                    add = rng.sample(held_rows, min(len(held_rows) - 1, rng.randrange(1, 5))) if len(held_rows) > 1 else []
                if not add:
                    kind = None
            if kind == "C":
                o_rows = [x for x in rows if x not in add]
                lodgements.append({"id": o_id, "h": h, "q": q, "type": "O", "ref": "", "date": o_date, "rows": o_rows})
                seq[q] += 1
                c_date = next_workday(o_date + dt.timedelta(days=rng.randrange(8, 35)))
                if q.month == 6:
                    c_date = min(c_date, D(q.year, 8, 28))
                lodgements.append({"id": f"DGT-{qlabel(q)}-{seq[q]:05d}", "h": h, "q": q, "type": "C",
                                   "ref": o_id, "date": c_date, "rows": sorted(add)})
            elif kind == "S":
                prev = states[QUARTERS[qi - 1]] if qi else states[q]
                stale = sorted(r for r, o in prev.items() if o == h and states[q].get(r) != h)
                wrong = [x for x in rows if x[1] == "PD"]
                drop = rng.sample(wrong, min(len(wrong) - 1, rng.randrange(1, 4))) if len(wrong) > 1 else []
                o_rows = [x for x in rows if x not in drop] + [(r, "PD", "", "", "") for r in stale[:2]]
                lodgements.append({"id": o_id, "h": h, "q": q, "type": "O", "ref": "", "date": o_date,
                                   "rows": sorted(o_rows)})
                seq[q] += 1
                s_date = next_workday(o_date + dt.timedelta(days=rng.randrange(8, 40)))
                if q.month == 6:
                    s_date = min(s_date, D(q.year, 8, 28))
                lodgements.append({"id": f"DGT-{qlabel(q)}-{seq[q]:05d}", "h": h, "q": q, "type": "S",
                                   "ref": o_id, "date": s_date, "rows": rows})
            else:
                lodgements.append({"id": o_id, "h": h, "q": q, "type": "O", "ref": "", "date": o_date, "rows": rows})
    # two late substitutive returns for 2025T4 lodged after the format change (holders outside the watch list)
    late = [l for l in lodgements if l["q"] == D(2025, 12, 31) and l["type"] == "O" and l["h"].startswith("nw")
            and l["h"] not in CARRIED][:2]
    for l in late:
        seq[l["q"]] += 1
        lodgements.append({"id": f"DGT-2025T4-{seq[l['q']]:05d}", "h": l["h"], "q": l["q"], "type": "S",
                           "ref": l["id"], "date": D(2026, 4, 14 + 2 * late.index(l)), "rows": l["rows"]})
    return lodgements, expo


def render(lodgements, holders, stock, people_nif, plan_mal):
    """CSV rows of the spine. plan_mal: section -> malformed reference count on the 2026T2 picture."""
    rng = random.Random(SEED * 23 + 4)
    sections, buildings, dwellings = stock
    # which 2026T2 dwelling rows carry a malformed reference (the effective picture only)
    eff = {}
    for l in sorted(lodgements, key=lambda l: (l["date"], l["id"])):
        if l["q"] != QUARTERS[-1]:
            continue
        if l["type"] in ("O", "S"):
            eff[l["h"]] = (l["id"], l["rows"])
    mal_rows = set()
    committed = set()
    for s in SECTIONS:
        cands = []
        for h, (lid, rows) in sorted(eff.items()):
            if h in s["carried"] or (s["crow"] and h == s["crow"][0]):
                continue
            for x in rows:
                if x[1] == "PD" and dwellings[x[0]]["section"] == s["code"] and not x[2]:
                    cands.append((lid, x[0]))
        cands.sort()
        rng.shuffle(cands)
        mal_rows.update(cands[:s["mal"]])
        plan_mal[s["code"]] = cands[:s["mal"]]
    out = []
    for l in sorted(lodgements, key=lambda l: (l["date"], l["id"])):
        h = holders[l["h"]]
        g = group_of(l["h"], l["date"])
        gcode = GROUP_CODE[g] if g else ""
        base = [l["id"], h["nif"], h["name"], qlabel(l["q"]), l["type"], l["ref"], l["date"].isoformat(), gcode]
        if l["date"] >= FORMAT_CHANGE:
            for x in l["rows"]:
                ref = x[0]
                if (l["id"], ref) in mal_rows:
                    ref = malform(ref, rng)
                elif dwellings[x[0]]["section"] not in WATCH and rng.random() < 0.003:
                    ref = malform(ref, rng)
                out.append(base + [ref, ""] + list(x[1:]))
        else:
            groups = {}
            for x in l["rows"]:
                d = dwellings[x[0]]
                groups.setdefault((d["parcel"],) + tuple(x[1:]), []).append(d["unit"])
            for key in sorted(groups):
                parcel = key[0]
                if buildings[parcel]["section"] not in WATCH and rng.random() < 0.006:
                    parcel = parcel.lower() if rng.random() < 0.5 else parcel[:7] + " " + parcel[7:]
                out.append(base + [parcel, units_text(groups[key])] + list(key[1:]))
    return out


HEADER = ["id_declaracio", "nif_declarant", "nom_declarant", "trimestre", "tipus_declaracio",
          "declaracio_referida", "data_presentacio", "codi_grup", "referencia_cadastral", "unitats",
          "codi_tinenca", "data_transmissio_prevista", "nif_adquirent_previst", "preu_convingut"]
