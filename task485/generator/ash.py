"""Boiler ash: each site's bottom ash bunker and fly ash silo fill with its coal's ash and are emptied by three ash
contractors. Whinmoss Waste Haulage collects at every site; in its busy weeks it passes about a third of its jobs to
the local contractor (Carnhope Skips for the eight western sites, Pellrigg and Sons for the eight eastern ones), and
invoices the customer for each such job at its own standard load, dated when the local docket reaches it, with the
local job number in the invoice line's reference. The local's job sheet records the same collection on its day at
its weighbridge weight and where it actually went."""
import numpy as np

import world as W

LOCAL = {s: ("Carnhope Skips" if int(s[1:]) <= 8 else "Pellrigg and Sons Haulage") for s, *_ in W.SITES}
RECEIVERS = {"landfill": "Galscar Landfill", "cement": "Velthwaite Cement Works", "blocks": "Yarrdale Blocks"}
BUSY = set(range(3, 13)) | set(range(44, 52))           # ISO weeks
CEMENT_SHUT = (4, 46)                                   # the kiln's winter shutdown, days
CLOSED = {0, 358, 359, 365}                             # 1 January, 25 and 26 December 2026, 1 January 2027
# where each site sends its bottom ash and its fly ash
POLICY = {"S01": ("blocks", "cement"), "S02": ("blocks", "landfill"), "S03": ("blocks", "landfill"),
          "S04": ("landfill", "cement"), "S05": ("blocks", "landfill"), "S06": ("blocks", "cement"),
          "S07": ("landfill", "cement"), "S08": ("blocks", "landfill"), "S09": ("blocks", "cement"),
          "S10": ("landfill", "cement"), "S11": ("blocks", "landfill"), "S12": ("blocks", "cement"),
          "S13": ("blocks", "landfill"), "S14": ("landfill", "cement"), "S15": ("blocks", "landfill"),
          "S16": ("landfill", "cement")}


def produce(w, lots):
    """daily bottom and fly ash per site, t, from each site's receipts' tonne-weighted ash; a boiler's split between
    the grate or furnace bottom and the fly ash it carries to the precipitator is its own"""
    rng = np.random.default_rng(W.SEED + 62)
    for b in w.B:
        b["bottom_share"] = float(rng.uniform(0.72, 0.86) if b["type"] == "stoker" else rng.uniform(0.10, 0.20))
    for site in sorted(w.sites):
        w.sites[site]["overflow"] = float(rng.uniform(0.02, 0.10))
        w.sites[site]["condition"] = float(rng.uniform(1.08, 1.16))
    out = {}
    for site in sorted(w.sites):
        xs = [x for x in lots if x["site"] == site and 0 <= x["received"] <= 364]
        ash = sum(x["t"] * x["ash"] for x in xs) / sum(x["t"] for x in xs) / 100
        bottom = np.zeros(W.DAYS)
        fly = np.zeros(W.DAYS)
        for b in w.B:
            if b["site"] != site:
                continue
            fb = b["bottom_share"]
            bottom += b["coal_day"] * ash * fb
            fly += b["coal_day"] * ash * (1 - fb)
        out[site] = dict(bottom=bottom, fly=fly, ash=ash)
    return out


def collections(w, prod):
    jobs = []
    for site in sorted(prod):
        rng = W.stream(61, int(site[1:]))
        for kind in ("bottom", "fly"):
            series = prod[site][kind]
            if series.sum() < 1:
                continue
            load = (18.0, 24.0) if kind == "bottom" else (23.5, 28.0)
            cap = float(np.round(series[series > 0].mean() * rng.uniform(4, 7), 0)) + 30
            level = float(rng.uniform(0.2, 0.6) * cap)
            for d in range(W.DAYS + 10):
                level += series[d] if d < W.DAYS else series[W.DAYS - 1]
                if W.day(d).weekday() == 6 or d in CLOSED:
                    continue                        # no collections on Sundays or the holidays
                while level >= 0.7 * cap:
                    t = float(np.round(min(level, rng.uniform(*load)), 2))
                    dest = POLICY[site][0 if kind == "bottom" else 1]
                    if dest == "cement" and CEMENT_SHUT[0] <= d <= CEMENT_SHUT[1]:
                        dest = "landfill"
                    if dest == "blocks" and rng.random() < w.sites[site]["overflow"]:
                        dest = "landfill"           # block yard full: tipped at the landfill instead
                    cond = w.sites[site]["condition"]
                    if kind == "fly" and dest == "landfill":
                        t = float(np.round(t * cond, 2))     # conditioned with water for the landfill
                    week = W.day(min(d, 364)).isocalendar()[1]
                    direct_local = rng.random() < 0.22
                    if direct_local:
                        who = LOCAL[site]
                        sub = False
                    else:
                        who = "Whinmoss Waste Haulage"
                        sub = week in BUSY and d < W.DAYS and rng.random() < 0.34
                    jobs.append(dict(site=site, kind=kind, day=d, t=t, dest=dest, who=who, sub=sub,
                                     ordered=POLICY[site][0 if kind == "bottom" else 1]))
                    level -= t / (cond if (kind == "fly" and dest == "landfill") else 1.0)
    w.ash_jobs = jobs
    return jobs


def golden(jobs):
    """each site's ash taken off site in 2026 (collected 1 January to 31 December), t, and the share to recovery"""
    out = {}
    for site in sorted(set(j["site"] for j in jobs)):
        js = [j for j in jobs if j["site"] == site and j["day"] <= 364]
        tot = sum(j["t"] for j in js)
        rec = sum(j["t"] for j in js if j["dest"] != "landfill")
        out[site] = dict(t=tot, rec_pct=100 * rec / tot)
    return out


MOORSIDE_NAMES = {"S01": "Quarholt Paperboard Ltd", "S02": "Eskfold Sugar Refiners", "S03": "Dremstead Chemical Co",
                  "S04": "Ulvdale Dyers Ltd", "S05": "Kirlgate Malt", "S06": "Vornfield Brewing Co",
                  "S07": "Yeldholt Hospitals Trust (Energy Centre)", "S08": "Haskmouth Paper Ltd",
                  "S09": "Nethstead Tissue Products", "S10": "Pridwold Starch Ltd", "S11": "Lathgarth Fibres Ltd",
                  "S12": "Candrigg Alkali Ltd", "S13": "Thalwold Food Group", "S14": "Sellhope Polymers",
                  "S15": "Umbgarth Heat Network", "S16": "Wendscar Leather"}
SERVICE = {("bottom", "landfill"): "Bottom ash, tipper, to Galscar Landfill",
           ("bottom", "blocks"): "Bottom ash, tipper, to Yarrdale Blocks",
           ("fly", "landfill"): "Fly ash (conditioned), tipper, to Galscar Landfill",
           ("fly", "cement"): "Fly ash (dry), tanker, to Velthwaite Cement Works"}
STANDARD = {"bottom": 20.0, "fly": 26.0}


def exports(w, jobs):
    """the three contractors' 2026 exports as rows: Whinmoss's invoice lines (its own jobs at the weighbridge weight
    on the collection date; a subcontracted job at its standard load and the destination ordered, dated when the
    local docket reaches it, the local job number in the reference), Carnhope's job sheet (net kilograms) and
    Pellrigg's dockets (net tonnes), plus each contractor's other work"""
    rng = np.random.default_rng(W.SEED + 71)
    moor, tol, gre = [], [], []
    tno, gno, mno = 41250, 8800, 26001
    for j in sorted(jobs, key=lambda x: (x["day"], x["site"], x["kind"])):
        local = LOCAL[j["site"]]
        if j["who"] == "Whinmoss Waste Haulage" and not j["sub"]:
            moor.append(dict(day=j["day"], site=j["site"], service=SERVICE[(j["kind"], j["dest"])], qty=j["t"],
                             unit="t", ref="WM-%05d" % mno, kind=j["kind"], dest=j["dest"], own=True))
            mno += 1
            continue
        if local == "Carnhope Skips":
            jobno = "CS%06d" % tno
            tno += 1
            tol.append(dict(job=jobno, day=j["day"], site=j["site"], material="Bottom ash" if j["kind"] == "bottom" else "Fly ash",
                            dest=RECEIVERS[j["dest"]], net_kg=int(round(j["t"] * 1000)), kind=j["kind"], destk=j["dest"]))
        else:
            jobno = "P&S/26/%04d" % gno
            gno += 1
            gre.append(dict(job=jobno, day=j["day"], site=j["site"], material="Boiler bottom ash" if j["kind"] == "bottom" else "PFA / fly ash",
                            dest=RECEIVERS[j["dest"]], net_t=float(np.round(j["t"], 2)), kind=j["kind"], destk=j["dest"]))
        if j["sub"]:
            lag = int(rng.integers(3, 11))
            moor.append(dict(day=j["day"] + lag, site=j["site"], service=SERVICE[(j["kind"], j["ordered"])],
                             qty=STANDARD[j["kind"]], unit="t", ref=jobno, kind=j["kind"], dest=j["ordered"], own=False))
    # each contractor's other work at the same sites: general waste, scrap, effluent screenings
    for site in sorted(w.sites):
        for _ in range(int(rng.integers(6, 14))):
            d = int(rng.integers(0, 375))
            svc = str(rng.choice(["General waste, 1100 litre bin exchange", "Skip hire, 12 cubic yard, mixed waste",
                                  "Scrap metal collection"]))
            if svc.startswith("General"):
                qty, unit = float(rng.integers(1, 7)), "lift"
            elif svc.startswith("Skip"):
                qty, unit = 1.0, "each"
            else:
                qty, unit = float(np.round(rng.uniform(0.4, 6.0), 2)), "t"
            moor.append(dict(day=d, site=site, service=svc, qty=qty, unit=unit, ref="WM-%05d" % mno, kind="other",
                             dest="other", own=True))
            mno += 1
        for _ in range(int(rng.integers(2, 6))):
            d = int(rng.integers(0, 375))
            if LOCAL[site] == "Carnhope Skips":
                tol.append(dict(job="CS%06d" % tno, day=d, site=site, material=str(rng.choice(["General waste", "Scrap metal"])),
                                dest="Carnhope transfer station", net_kg=int(rng.integers(400, 5200)), kind="other", destk="other"))
                tno += 1
            else:
                gre.append(dict(job="P&S/26/%04d" % gno, day=d, site=site, material=str(rng.choice(["Effluent screenings", "General waste"])),
                                dest="Pellrigg yard", net_t=float(np.round(rng.uniform(0.5, 4.8), 2)), kind="other", destk="other"))
                gno += 1
    w.ash_exports = dict(moorside=sorted(moor, key=lambda x: (x["day"], x["ref"])),
                         tolland=sorted(tol, key=lambda x: x["job"]), greave=sorted(gre, key=lambda x: x["job"]))
    return w.ash_exports
