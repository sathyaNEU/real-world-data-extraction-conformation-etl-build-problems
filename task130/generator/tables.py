"""Deed extract, cadastre extract, register and group-code table, as row lists ready to write."""
import datetime as dt
import random

from common import D, SEED, AS_OF, DEED_FROM, add_workdays
from world import MUNIS, MEMBER, LINK_ENTERED, GROUP_CODE, GROUP_LIFE, GROUP_WORD
from plan import SECTIONS

WATCH = {s["code"] for s in SECTIONS}
OFFICE = {"46250": ["València 1", "València 3", "València 7", "València 14"], "03014": ["Alacant 1", "Alacant 3"],
          "12040": ["Castelló 1", "Castelló 2"], "46131": ["Gandia 1"], "46244": ["Torrent 2"], "03065": ["Elx 1"],
          "46220": ["Sagunt"], "46190": ["Paterna"], "03031": ["Benidorm 2"], "12135": ["Vila-real"]}
GENERIC_STREETS = ["C/ Major", "Av. del País Valencià", "C/ de Sant Vicent", "C/ de la Pau", "Av. de la Constitució",
                   "C/ de Sant Josep", "C/ Nou", "C/ de la Mar", "Av. d'Alacant", "C/ de València",
                   "C/ del Raval", "C/ de l'Església", "Pl. Major", "C/ de Colom", "C/ de Sant Francesc"]
DEED_HEADER = ["num_entrada", "registre", "protocol", "data_atorgament", "data_inscripcio",
               "referencia_cadastral", "nif_transmitent", "nif_adquirent", "titol", "preu"]
CAD_HEADER = ["referencia_cadastral", "parcela", "carrec", "seccio_censal", "codi_municipi", "municipi", "adreca",
              "planta", "porta", "us", "superficie_m2", "any_construccio"]


def scope_refs(W, rendered_refs):
    sections, buildings, dwellings = W["stock"]
    return {r for r, d in dwellings.items() if d["section"] in WATCH} | set(rendered_refs)


def deeds(W, scope):
    rng = random.Random(SEED * 43 + 1)
    sections, buildings, dwellings = W["stock"]
    nif = W["nif"]
    out = []
    seq = {}
    for e in sorted(W["book"].events, key=lambda e: (e["date"], e["refs"][0])):
        if not (DEED_FROM <= e["date"] <= AS_OF):
            continue
        refs = [r for r in e["refs"] if r in scope]
        if not refs:
            continue
        muni = dwellings[refs[0]]["section"][:5]
        office = OFFICE[muni][int(refs[0][3]) % len(OFFICE[muni])]
        notary = rng.randrange(400, 3900)
        reg = add_workdays(e["date"], rng.randrange(2, 8))
        assert reg <= AS_OF or e["date"] > AS_OF, (e["date"], reg)
        for r in refs:
            seq[e["date"].year] = seq.get(e["date"].year, 0) + rng.randrange(3, 40)
            out.append([f"{e['date'].year}/{seq[e['date'].year]:06d}", f"Registre de la Propietat de {office}",
                        f"{notary}/{e['date'].year}", e["date"].isoformat(), reg.isoformat(), r,
                        nif(e["before"][r]), nif(e["after"][r]), e["title"], str(e["price"]) if e["price"] else ""])
    return out


def cadastre(W, scope):
    rng = random.Random(SEED * 47 + 3)
    sections, buildings, dwellings = W["stock"]
    rows = []
    for p in sorted(buildings):
        b = buildings[p]
        muni = b["section"][:5]
        street = b["street"] or GENERIC_STREETS[int(p[:7]) % len(GENERIC_STREETS)]
        addr = f"{street}, {b['num']}"
        for r in b["units"]:
            if r not in scope:
                continue
            d = dwellings[r]
            rows.append([r, p, str(d["unit"]), d["section"], muni, MUNIS[muni][0], addr, d["floor"], d["door"],
                         "Residencial", str(d["area"]), str(d["year"])])
        for x in b.get("nonres", []):
            rows.append([x["ref"], p, str(x["unit"]), b["section"], muni, MUNIS[muni][0], addr, x["floor"], x["door"],
                         x["us"], str(x["area"]), str(b["year"])])
    rows.sort(key=lambda r: (r[3], r[1], int(r[2])))
    return rows


def register(W):
    holders = W["holders"]
    tit = []
    for h in sorted(holders, key=lambda k: holders[k]["nif"]):
        o = holders[h]
        tit.append([o["nif"], o["name"], o["kind"], o["registered"].isoformat(),
                    o.get("left").isoformat() if o.get("left") else ""])
    links = []
    for h in sorted(MEMBER):
        if h not in holders:
            continue
        for g, a, b in MEMBER[h]:
            start = max(a, holders[h]["registered"])
            entered = LINK_ENTERED.get((h, g)) or (start + dt.timedelta(days=9))
            if (h, g) in LINK_ENTERED and b is not None and LINK_ENTERED[(h, g)] > a:
                entered = LINK_ENTERED[(h, g)]
            links.append([holders[h]["nif"], GROUP_CODE[g], start.isoformat(), b.isoformat() if b else "",
                          entered.isoformat()])
    links.sort(key=lambda r: (r[0], r[2]))
    return tit, links


def group_codes():
    rows = []
    for g in sorted(GROUP_CODE, key=lambda g: GROUP_CODE[g]):
        if g in ("K1", "K2"):
            continue
        a, b = GROUP_LIFE[g]
        rows.append([GROUP_CODE[g], f"Grup {GROUP_WORD[g]}", a.isoformat(), b.isoformat() if b else ""])
    rows.append(["GT0099", "Grup Sòtera", "2018-04-03", "2023-06-30"])
    rows.sort()
    return rows


def group_name(g):
    return f"Grup {GROUP_WORD[g]}"
