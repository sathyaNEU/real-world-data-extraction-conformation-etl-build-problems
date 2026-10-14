"""The systems' records: the assessment roll by year, the permit system (permits, buildings, occupancies), the
folio history and Schedule A, built from the truth in one neutral schema; the writers in build.py lay them out."""
import datetime as dt

import numpy as np

import sim as S
import world as W

PULL = dt.date(2027, 1, 11)              # the permit and occupancy extracts were pulled this day
HOME_VALUE_FACTOR = 0.92                 # assessed value of a new home against its sale value

COMM_USES = [("210", "STORE(S) AND OFFICES"), ("220", "NEIGHBOURHOOD STORE"), ("230", "SERVICE STATION"),
             ("214", "RETAIL STRIP"), ("260", "PARKING (LOT ONLY, PAVED OR GRAVEL)")]


def zone_code(code, d):
    """the zone's code as the city wrote it on a date (renamed in the 2020 consolidation)"""
    return code if d < W.CONSOLIDATION else W.ZONES[code]["new"]


def lot_area_cols(a):
    if a >= 43560:
        return round(a / 43560.0, 3), "AC"
    return int(round(a)), "SF"


def comm_use(lot):
    r = S.rng_for("comm-use", lot["lot_id"])
    return COMM_USES[int(r.integers(0, len(COMM_USES)))]


def construction_imp(p, lot, C, y):
    """improvements on a cleared site: the new building's value as work proceeds"""
    first = p["done"][0]
    months = (C - p["cleared"]).days / 30.44
    total = (first - p["cleared"]).days / 30.44
    if months < 6:
        return 0.0
    frac = min(0.9, months / max(total, 1.0))
    return float(round(p["gfa"] * W.cost(p["btype"], y) * 0.55 * frac, -3))


def home_floor_areas(plan, nsf, seed):
    r = S.rng_for("floor", seed, plan["plan"])
    f = np.clip(r.normal(nsf, 140, plan["homes"]), 430, 1350)
    f = f * plan["homes"] * nsf * float(r.uniform(0.97, 1.03)) / f.sum()
    return [int(round(x)) for x in f]


def unit_numbers(n, storeys):
    per = int(np.ceil(n / max(storeys - 1, 1)))
    out = []
    for k in range(n):
        fl = 2 + k // per if storeys > 2 else 1 + k // per
        out.append("%d%02d" % (fl, 1 + k % per))
    return out


def roll(lots, projects, old_plans, area_value):
    """one record per folio per roll year, as the assessor holds it at the roll's condition date"""
    rows = []
    strata_index = {}
    for y in W.YEARS:
        C = W.ROLL_CONDITION[y]
        V = dt.date(y - 1, 7, 1)
        for lot in lots:
            i = lot["lot_id"]
            p = projects.get(i)
            zc = zone_code(S.zone_on_date(lot["group"], V), V)
            nb = W.AREA_NAME[lot["area"]].upper()
            base = dict(roll_year=y, neighbourhood=nb, zone=zc, station=lot["area"] if lot["tier"] else "",
                        tier=lot["tier"], lot_id=i, group=lot["group"])
            land, imp = S.roll_values(lot, y, None)
            if p is None or C < p["cleared"]:
                use = {"house": "house_suite" if (lot["suite0"] or (lot.get("add_done") and lot["add_done"] <= C)) else "house",
                       "comm": "comm", "rental": "rental"}[lot["kind"]]
                if use == "house_suite" and lot.get("add_kind") == "laneway" and lot["add_done"] <= C:
                    use = "house_laneway"
                units = S.units_on_roll(lot, y) if lot["kind"] != "comm" else 0
                rows.append(dict(base, folio=lot["folio"], civic=lot["civic"], street=lot["street"], unit_no="",
                                 use=use, area=lot["a"], land=land, imp=imp, units=units, floor=None,
                                 built=lot["built"], plan="", state="standing"))
                continue
            if p["tenure"] == "rental":
                done = [k for k, d in enumerate(p["done"]) if d <= C]
                if not done:
                    rows.append(dict(base, folio=lot["folio"], civic=lot["civic"], street=lot["street"], unit_no="",
                                     use="vacant", area=lot["a"], land=land, imp=construction_imp(p, lot, C, y),
                                     units=None, floor=None, built=None, plan="", state="construction"))
                else:
                    u = sum(p["split"][k] for k in done)
                    share = u / p["units"]
                    imp_new = p["gfa"] * W.cost(p["btype"], p["year"]) * 0.62 * share * W.IP[y] / W.IP[p["year"]]
                    if len(done) < len(p["split"]):
                        imp_new += construction_imp(p, lot, C, y) * (1 - share)
                    rows.append(dict(base, folio=lot["folio"], civic=lot["civic"], street=lot["street"], unit_no="",
                                     use="rental_new", area=lot["a"], land=land, imp=float(round(imp_new, -3)),
                                     units=u, floor=None, built=p["done"][0].year, plan="", state="rebuilt"))
                continue
            # strata: the parent until the first plan registers; then each registered plan's lots, and a remainder
            reg = [pl for pl in p["plans"] if pl["registered"] <= C]
            if not reg:
                rows.append(dict(base, folio=lot["folio"], civic=lot["civic"], street=lot["street"], unit_no="",
                                 use="vacant", area=lot["a"], land=land, imp=construction_imp(p, lot, C, y),
                                 units=None, floor=None, built=None, plan="", state="construction"))
                continue
            nb_ = len(p["plans"])
            if len(reg) < nb_:
                rem = p["remainders"][len(reg) - 1]
                left = sum(pl["homes"] for pl in p["plans"][len(reg):]) / p["units"]
                rows.append(dict(base, folio=rem, civic=lot["civic"] + 10 * len(reg), street=lot["street"], unit_no="",
                                 use="vacant", area=lot["a"] * left, land=float(round(land * left, -3)),
                                 imp=construction_imp(p, lot, C, y) * left, units=None, floor=None, built=None, plan="",
                                 state="construction"))
            for pl in reg:
                k = pl["building"]
                key = (i, pl["plan"])
                if key not in strata_index:
                    strata_index[key] = strata_lots(lot, p, pl)
                for s in strata_index[key]:
                    if lot["tier"] == 0:
                        continue
                    vy = area_value(lot["area"], "conc" if p["btype"] == "HR" else "wood", y)
                    if s["home"]:
                        tot = s["floor"] * vy * HOME_VALUE_FACTOR * s["vf"]
                    else:
                        tot = s["stall_value"] * W.IP[y] / W.IP[2026]
                    landv = float(round(tot * s["land_share"], -3))
                    rows.append(dict(base, folio=s["folio"], civic=lot["civic"] + 10 * (k - 1), street=lot["street"],
                                     unit_no=s["unit"], use="strata", area=None, land=landv,
                                     imp=float(round(tot - landv, -3)), units=None,
                                     floor=s["floor"] if (s["home"] and pl["registered"] < dt.date(2023, 1, 1)) else None,
                                     built=pl["registered"].year, plan=pl["plan"], state="strata", home=s["home"]))
                if lot["tier"] == 0:
                    homes = pl["homes"]
                    tot = sum(s["floor"] for s in strata_index[key] if s["home"]) * area_value(
                        lot["area"], "conc" if p["btype"] == "HR" else "wood", y) * HOME_VALUE_FACTOR
                    tot += sum(s["stall_value"] for s in strata_index[key] if not s["home"])
                    rows.append(dict(base, folio=pl["block"] + "-000", civic=lot["civic"] + 10 * (k - 1),
                                     street=lot["street"], unit_no="", use="plan_summary", area=lot["a"] / nb_,
                                     land=float(round(tot * 0.25, -3)), imp=float(round(tot * 0.75, -3)), units=None,
                                     floor=None, built=pl["registered"].year, plan=pl["plan"], state="strata",
                                     strata_lots=homes + pl["stalls"]))
        for op in old_plans:
            for s in old_strata_lots(op):
                vy = area_value(op["station"], "wood", y) * 0.58
                if s["home"]:
                    tot = s["floor"] * vy * s["vf"]
                else:
                    tot = s["stall_value"] * W.IP[y] / W.IP[2026]
                landv = float(round(tot * s["land_share"], -3))
                V = dt.date(y - 1, 7, 1)
                rows.append(dict(roll_year=y, neighbourhood=W.AREA_NAME[op["station"]].upper(), zone=zone_code("RM-5", V),
                                 station=op["station"], tier=op["tier"], lot_id=-1, group="OLD_STRATA",
                                 folio=s["folio"], civic=s["civic"], street=op["street"], unit_no=s["unit"], use="strata",
                                 area=None, land=landv, imp=float(round(tot - landv, -3)), units=None, floor=s["floor"],
                                 built=op["built"], plan=op["plan"], state="strata", home=s["home"],
                                 townhouse=op["townhouse"]))
    return rows, strata_index


def strata_lots(lot, p, pl):
    """the strata lots of one plan: the homes, then any parking and storage stalls"""
    r = S.rng_for("strata", lot["lot_id"], pl["plan"])
    nsf = W.BTYPES[p["btype"]]["nsf"]
    fl = home_floor_areas(pl, nsf, lot["lot_id"])
    units = unit_numbers(pl["homes"], p["storeys"])
    out = []
    n = 0
    for k in range(pl["homes"]):
        n += 1
        out.append(dict(folio="%s-%03d" % (pl["block"], n), unit=units[k], floor=fl[k], home=True,
                        vf=float(r.uniform(0.94, 1.06)), land_share=float(r.uniform(0.21, 0.28)), stall_value=0.0))
    for k in range(pl["stalls"]):
        n += 1
        out.append(dict(folio="%s-%03d" % (pl["block"], n), unit="", floor=None, home=False, vf=1.0,
                        land_share=float(r.uniform(0.28, 0.36)), stall_value=float(r.uniform(22000, 65000))))
    return out


_OLD = {}


def old_strata_lots(op):
    if op["plan"] in _OLD:
        return _OLD[op["plan"]]
    r = S.rng_for("old-strata-lots", op["plan"])
    out = []
    n = 0
    fl = np.clip(r.normal(1250 if op["townhouse"] else 860, 160, op["homes"]), 520, 1900)
    units = unit_numbers(op["homes"], 4) if not op["townhouse"] else [""] * op["homes"]
    for k in range(op["homes"]):
        n += 1
        civic = op["civic"] + 2 * k if op["townhouse"] else op["civic"]
        out.append(dict(folio="%s-%03d" % (op["block"], n), unit=units[k], floor=int(round(fl[k])), home=True,
                        vf=float(r.uniform(0.9, 1.1)), land_share=float(r.uniform(0.25, 0.34)), stall_value=0.0,
                        civic=civic))
    for k in range(op["stalls"]):
        n += 1
        out.append(dict(folio="%s-%03d" % (op["block"], n), unit="", floor=None, home=False, vf=1.0,
                        land_share=float(r.uniform(0.3, 0.38)), stall_value=float(r.uniform(18000, 52000)),
                        civic=op["civic"]))
    _OLD[op["plan"]] = out
    return out


def permits(lots, projects, others):
    """the permit system's records: every permit issued 2014 to 2026, as the extract of 11 January 2027 holds it"""
    out = []
    for i in sorted(projects):
        p = projects[i]
        lot = lots[i]
        addr = "%d %s" % (lot["civic"], lot["street"])
        last_final = max(d for (_, t, d) in p["occ"] if t == "Final")
        status = "Completed" if last_final <= PULL else "Issued"
        if p["lapsed"]:
            lp = p["lapsed"]
            out.append(dict(lot_id=i, folio=lot["folio"], address=addr, type="NEW", issue=lp["issue"], status=lp["status"],
                            units=lp["units"], units_demolished=p["units_demolished"], gfa=p["gfa"] * 0.97,
                            value=p["value"] * 0.95, buildings=len(p["split"]), project=i, role="lapsed",
                            storeys=p["storeys"], btype=p["btype"]))
        if p["revised"]:
            rv = p["revised"]
            out.append(dict(lot_id=i, folio=lot["folio"], address=addr, type="NEW", issue=p["issue"], status="Superseded",
                            units=rv["units_first"], units_demolished=p["units_demolished"], gfa=p["gfa"], value=p["value"],
                            buildings=len(p["split"]), project=i, role="original", storeys=p["storeys"], btype=p["btype"]))
            out.append(dict(lot_id=i, folio=lot["folio"], address=addr, type="NEW", issue=rv["issue"], status=status,
                            units=p["units"], units_demolished=p["units_demolished"], gfa=p["gfa"], value=p["value"],
                            buildings=len(p["split"]), project=i, role="active", revises=True, storeys=p["storeys"],
                            btype=p["btype"]))
        else:
            out.append(dict(lot_id=i, folio=lot["folio"], address=addr, type="NEW", issue=p["issue"], status=status,
                            units=p["units"], units_demolished=p["units_demolished"], gfa=p["gfa"], value=p["value"],
                            buildings=len(p["split"]), project=i, role="active", storeys=p["storeys"], btype=p["btype"]))
        demo_units = p["units_demolished"]
        out.append(dict(lot_id=i, folio=lot["folio"], address=addr, type="DEMOLITION", issue=p["demo_permit"],
                        status="Completed", units=0, units_demolished=demo_units, gfa=0,
                        value=p["demo_value"], buildings=1, project=i, role="demolition"))
    for o in others:
        lot = lots[o["lot_id"]]
        out.append(dict(lot_id=o["lot_id"], folio=lot["folio"], address="%d %s" % (lot["civic"], lot["street"]),
                        type={"Secondary Suite": "SUITE", "Laneway House": "LANEWAY", "Alteration/Repair": "ALTERATION"}[o["type"]],
                        issue=o["issue"], status=o["status"], units=o["units"], units_demolished=0, gfa=o["gfa"],
                        value=o["value"], buildings=1, project=None, role="other"))
    out = [r for r in out if dt.date(2014, 1, 1) <= r["issue"] <= W.ASOF]
    out.sort(key=lambda r: (r["issue"], r["lot_id"], r["type"]))
    seq = {}
    for r in out:
        yy = r["issue"].year % 100
        seq[yy] = seq.get(yy, 0) + 1 + (seq.get(yy, 0) * 13 + r["lot_id"]) % 3
        r["permit_no"] = "BP%02d-%05d" % (yy, seq[yy])
    # revisions name the permit they revise
    by_proj = {}
    for r in out:
        if r.get("project") is not None:
            by_proj.setdefault(r["project"], []).append(r)
    for proj, rs in by_proj.items():
        orig = [r for r in rs if r["role"] == "original"]
        for r in rs:
            r["revises_no"] = orig[0]["permit_no"] if (r.get("revises") and orig) else ""
    return out


def occupancies(lots, projects, active_no):
    out = []
    for i in sorted(projects):
        p = projects[i]
        lot = lots[i]
        for (k, typ, d) in p["occ"]:
            if d > W.ASOF or d < dt.date(2018, 1, 1):
                continue
            out.append(dict(lot_id=i, permit_no=active_no[i], building_no=k, type=typ, issued=d,
                            address="%d %s" % (lot["civic"] + 10 * (k - 1), lot["street"]),
                            units=p["units"], building_units=p["split"][k - 1], station=lot["area"] if lot["tier"] else "",
                            tier=lot["tier"]))
    out.sort(key=lambda r: (r["issued"], r["permit_no"], r["building_no"]))
    seq = {}
    for r in out:
        yy = r["issued"].year % 100
        seq[yy] = seq.get(yy, 100) + 1
        r["occupancy_no"] = "OC%02d-%04d" % (yy, seq[yy])
    return out


def schedule_a(lots, projects, old_plans, strata_index):
    """Schedule A: every folio in the four transit-oriented areas on the order's date"""
    D = W.ORDER_DATE
    out = []
    for lot in lots:
        if not lot["tier"]:
            continue
        i = lot["lot_id"]
        p = projects.get(i)
        base = dict(station=lot["area"], tier=lot["tier"], street=lot["street"])
        if p is None or p["tenure"] == "rental":
            out.append(dict(base, folio=lot["folio"], civic=lot["civic"], unit=""))
            continue
        reg = [pl for pl in p["plans"] if pl["registered"] <= D]
        if not reg:
            out.append(dict(base, folio=lot["folio"], civic=lot["civic"], unit=""))
            continue
        if len(reg) < len(p["plans"]):
            out.append(dict(base, folio=p["remainders"][len(reg) - 1], civic=lot["civic"] + 10 * len(reg), unit=""))
        for pl in reg:
            key = (i, pl["plan"])
            if key not in strata_index:
                strata_index[key] = strata_lots(lot, p, pl)
            for s in strata_index[key]:
                out.append(dict(base, folio=s["folio"], civic=lot["civic"] + 10 * (pl["building"] - 1), unit=s["unit"]))
    for op in old_plans:
        for s in old_strata_lots(op):
            out.append(dict(station=op["station"], tier=op["tier"], street=op["street"], folio=s["folio"], civic=s["civic"],
                            unit=s["unit"]))
    out.sort(key=lambda r: (W.STATIONS.index(r["station"]), r["tier"], r["street"], r["civic"], r["unit"], r["folio"]))
    return out


def folio_history(lots, projects, strata_index):
    out = []
    for i in sorted(projects):
        p = projects[i]
        lot = lots[i]
        if p["tenure"] != "strata":
            continue
        prev = lot["folio"]
        for n, pl in enumerate(p["plans"]):
            if pl["registered"] > W.ASOF:
                break
            news = [s["folio"] for s in strata_index.get((i, pl["plan"]), [])] if lot["tier"] else [pl["block"] + "-000"]
            if not news:
                news = [s["folio"] for s in strata_lots(lot, p, pl)]
            for nf in news:
                out.append(dict(date=pl["registered"], event="Strata plan deposited", old=prev, new=nf, plan=pl["plan"]))
            if n < len(p["plans"]) - 1:
                rem = p["remainders"][n]
                out.append(dict(date=pl["registered"], event="Strata plan deposited (remainder parcel)", old=prev, new=rem,
                                plan=pl["plan"]))
                prev = rem
    out.sort(key=lambda r: (r["date"], r["old"], r["new"]))
    return out
