"""What each rebuild left in the city's systems: the permits (new building, demolition, revisions, cancelled and
expired applications), the buildings, occupancies, strata plans and folios; and the permits that are not rebuilds
(suites, laneway houses, alterations). Everything here is downstream of the simulation and never moves it."""
import datetime as dt

import numpy as np

import sim as S
import world as W

PHASED_MIN_GFA = 42000.0


def folio_maker():
    nxt = {d: 1000 + 37 * k for k, d in enumerate(sorted(set(W.DISTRICT.values())))}
    newblk = {d: 30000 + 53 * k for k, d in enumerate(sorted(set(W.DISTRICT.values())))}

    def parcel(area):
        d = W.DISTRICT[area]
        nxt[d] += 1 + (nxt[d] * 7) % 3
        return "%s-%05d-000" % (d, nxt[d])

    def block(area):
        d = W.DISTRICT[area]
        newblk[d] += 1 + (newblk[d] * 5) % 4
        return "%s-%05d" % (d, newblk[d])
    return parcel, block


def address_maker():
    used = set()
    rng = S.rng_for("addresses")

    def addr(area, group, tier):
        ave, st = W.GRID[area]
        for _ in range(200):
            if group in ("TOD_C", "TOD_R", "CORR_C", "CORR_R", "CORR_H") or (group in ("CC_C", "CC_R") and rng.random() < 0.5):
                street = W.ARTERIAL[area]
                num = int(rng.integers(ave * 100 - 900, ave * 100 + 900)) if "Avenue" in street or "Way" in street else \
                    int(rng.integers(st * 100 - 900, st * 100 + 900))
            else:
                span = {1: 2, 2: 4, 3: 8}.get(tier, 10)
                if rng.random() < 0.5:
                    a = ave + int(rng.integers(-span // 2, span // 2 + 1))
                    street = "%d Avenue" % a
                    num = int(rng.integers(st * 100 - span * 50, st * 100 + span * 50))
                else:
                    s_ = st + int(rng.integers(-span // 2, span // 2 + 1))
                    street = "%d Street" % s_
                    num = int(rng.integers(ave * 100 - span * 50, ave * 100 + span * 50))
            num = max(1000, num - num % 2 + (1 if rng.random() < 0.5 else 0))
            key = (num, street)
            if key not in used:
                used.add(key)
                return num, street
        raise RuntimeError("address space exhausted")
    return addr


def registry():
    parcel, block = folio_maker()
    return dict(parcel=parcel, block=block, addr=address_maker())


def build_projects(lots, rebuild, reg):
    """every rebuild's permits, buildings and timeline; folios assigned; strata plans drawn"""
    parcel, block, addr = reg["parcel"], reg["block"], reg["addr"]
    for lot in lots:
        lot["folio"] = parcel(lot["area"])
        lot["civic"], lot["street"] = addr(lot["area"], lot["group"], lot["tier"])
    projects = {}
    plan_no = [1180]
    for i in sorted(rebuild):
        ev = rebuild[i]
        lot = lots[i]
        r = S.rng_for("project", i)
        y = ev["year"]
        issue = S.business_day(r, y)
        gfa = lot["a"] * ev["far"]
        units = ev["homes"]
        if lot["kind"] == "rental":
            tenure = "rental" if r.random() < 0.8 else "strata"
        else:
            tenure = "rental" if r.random() < 0.3 else "strata"
        nb = 1
        if gfa >= PHASED_MIN_GFA and r.random() < 0.35:
            nb = 3 if gfa >= 80000 and r.random() < 0.5 else 2
        if nb == 1:
            split = [units]
        elif nb == 2:
            u1 = int(round(units * r.uniform(0.48, 0.62)))
            split = [u1, units - u1]
        else:
            u1 = int(round(units * r.uniform(0.34, 0.42)))
            u2 = int(round(units * r.uniform(0.28, 0.34)))
            split = [u1, u2, units - u1 - u2]
        done = []
        t = S.add_months(issue, float(r.uniform(22, 34)))
        for k in range(nb):
            if k:
                t = S.add_months(t, float(r.uniform(9, 15)))
            done.append(t)
        done = [S.working(d) for d in done]
        occ = []
        for k in range(nb):
            if r.random() < 0.18:
                fin = S.working(S.add_months(done[k], float(r.uniform(1, 4))))
                occ.append((k + 1, "Interim", done[k]))
                occ.append((k + 1, "Final", fin))
            else:
                occ.append((k + 1, "Final", done[k]))
        demo = S.working(max(dt.date(y, 1, 3), issue + dt.timedelta(days=int(r.integers(-45, 61)))))
        clear = issue + dt.timedelta(days=int(r.integers(25, 95)))
        u_demo = S.units_on_roll(lot, y) if lot["kind"] != "comm" else 0
        if lot["kind"] == "house" and lot.get("add_done") and lot["add_done"] <= issue:
            u_demo = lot["u0"] + 1
        p = dict(lot_id=i, year=y, issue=issue, btype=ev["btype"], far=ev["far"], gfa=gfa, units=units, split=split,
                 tenure=tenure, done=done, occ=occ, demo_permit=demo, cleared=clear, units_demolished=u_demo,
                 storeys=W.BTYPES[ev["btype"]]["storeys"] or int(round(ev["far"] * 4.2)),
                 value=round(gfa * W.cost(ev["btype"], y) * float(r.uniform(0.52, 0.61)), -3),
                 demo_value=round(float(r.uniform(9, 16)) * (lot.get("gfa0") or (lot["a"] * float(r.uniform(0.25, 0.45)) if lot["kind"] == "comm" else float(r.uniform(1500, 2800)))), -2))
        # a revision of the permit for some projects; an earlier application that lapsed for a few
        p["revised"] = None
        if r.random() < 0.010:
            rev = S.working(S.add_months(issue, float(r.uniform(3, 8))))
            p["revised"] = dict(issue=rev, units_first=units + int(r.choice([-3, -2, -1, 1, 2])))
        p["lapsed"] = None
        if r.random() < 0.008 and y >= 2016:
            ly = y - int(r.integers(1, 3))
            ld = S.business_day(r, ly)
            p["lapsed"] = dict(issue=ld, status="Expired" if r.random() < 0.5 else "Cancelled",
                               units=units + int(r.integers(-4, 5)))
        # strata plans: one per building, registered at the building's first occupancy
        p["plans"] = []
        if tenure == "strata":
            has_stalls = r.random() < 0.45
            for k in range(nb):
                plan_no[0] += int(r.integers(3, 29))
                n_home = split[k]
                n_stall = int(round(n_home * r.uniform(0.4, 1.0))) if has_stalls else 0
                p["plans"].append(dict(plan="EPS%04d" % plan_no[0], building=k + 1, registered=done[k],
                                       homes=n_home, stalls=n_stall, block=block(lot["area"])))
            if nb > 1:
                p["remainders"] = [parcel(lot["area"]) for _ in range(nb - 1)]
        projects[i] = p
    ensure_phasing(lots, projects, reg, plan_no)
    number_plans(projects)
    return projects


def number_plans(projects):
    """strata plans take the land title office's numbers in the order they are deposited"""
    r = S.rng_for("plan-numbers")
    plans = sorted((pl["registered"], i, pl["building"], pl) for i, p in projects.items() for pl in p["plans"])
    n = 2160
    for _, _, _, pl in plans:
        n += int(r.integers(2, 10))
        pl["plan"] = "EPS%d" % n


def phased_cells(lots, projects):
    cells = set()
    for i, p in projects.items():
        lot = lots[i]
        if not lot["tier"] or len(p["split"]) < 2:
            continue
        for k in range(len(p["split"])):
            first = min(d for (b, t, d) in p["occ"] if b == k + 1)
            cells.add((lot["area"], first.year))
    return cells


def ensure_phasing(lots, projects, reg, plan_no):
    """every station area has a project built in phases among each year's completions, 2022 to 2026 (the permit
    system records each phase's occupancy against the project's permit)"""
    r = S.rng_for("phasing")
    have = phased_cells(lots, projects)
    for st in W.STATIONS:
        for y in range(2022, 2027):
            if (st, y) in have:
                continue
            cands = [i for i, p in sorted(projects.items()) if lots[i]["area"] == st and lots[i]["tier"]
                     and len(p["split"]) == 1 and p["done"][0].year == y and p["gfa"] >= 30000]
            if not cands:
                raise RuntimeError("no project to phase at %s %d" % (st, y))
            i = cands[int(r.integers(0, len(cands)))]
            p = projects[i]
            lot = lots[i]
            u1 = int(round(p["units"] * r.uniform(0.5, 0.62)))
            p["split"] = [u1, p["units"] - u1]
            d2 = S.working(S.add_months(p["done"][0], float(r.uniform(9, 15))))
            p["done"] = [p["done"][0], d2]
            p["occ"] = [o for o in p["occ"] if o[0] == 1] + [(2, "Final", d2)]
            if p["tenure"] == "strata":
                pl = p["plans"][0]
                ratio = pl["stalls"] / max(pl["homes"], 1)
                pl["homes"] = u1
                pl["stalls"] = int(round(u1 * ratio))
                plan_no[0] += int(r.integers(3, 29))
                p["plans"].append(dict(plan="EPS%04d" % plan_no[0], building=2, registered=d2, homes=p["units"] - u1,
                                       stalls=int(round((p["units"] - u1) * ratio)), block=reg["block"](lot["area"])))
                p["remainders"] = [reg["parcel"](lot["area"])]
            have.add((st, y))


def other_permits(lots, rebuild, projects):
    """suites, laneway houses and alterations on standing buildings"""
    out = []
    r = S.rng_for("other-permits")
    for lot in lots:
        i = lot["lot_id"]
        if lot.get("add_date"):
            out.append(dict(lot_id=i, type="Secondary Suite" if lot["add_kind"] == "suite" else "Laneway House",
                            issue=lot["add_date"], units=1, units_demolished=0,
                            gfa=round(float(r.uniform(520, 880)) if lot["add_kind"] == "suite" else float(r.uniform(560, 900))),
                            value=round(float(r.uniform(45000, 95000)) if lot["add_kind"] == "suite" else float(r.uniform(190000, 310000)), -2),
                            status="Completed"))
        last = rebuild[i]["year"] if i in rebuild else 2027
        for y in W.YEARS:
            if y >= last:
                break
            if r.random() < 0.012:
                out.append(dict(lot_id=i, type="Alteration/Repair", issue=S.business_day(r, y), units=0,
                                units_demolished=0, gfa=0, value=round(float(r.uniform(8000, 160000)), -2),
                                status="Completed" if y < 2026 else "Issued"))
    return out


def existing_strata(reg):
    """strata plans standing in the station areas before the record opens (one per station and band)"""
    r = S.rng_for("old-strata")
    addr = reg["addr"]
    plans = []
    k = 0
    for st in W.STATIONS:
        for tier in (1, 2, 3):
            k += 1
            homes = int(r.integers(24, 81))
            town = r.random() < 0.4
            stalls = int(round(homes * r.uniform(0.4, 0.9))) if r.random() < 0.5 else 0
            built = int(r.integers(1987, 2012))
            prefix = "LMS" if built < 2003 else "BCS"
            civic, street = addr(st, "TOD_H", tier)
            plans.append(dict(station=st, tier=tier, plan="%s%04d" % (prefix, int(r.integers(1200, 4800))), homes=homes,
                              stalls=stalls, townhouse=town, built=built, block="%s-%05d" % (W.DISTRICT[st], 20000 + 97 * k),
                              civic=civic, street=street, land=float(r.uniform(260, 330)) * homes * 950,
                              home_value=float(r.uniform(330000, 520000)), seed=k))
    return plans
