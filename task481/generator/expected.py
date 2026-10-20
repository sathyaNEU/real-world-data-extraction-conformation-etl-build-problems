"""The clean truth for the analyst test: the world's expected victims by kind and month, scored by the two systems'
rules, with no sampling noise. Returns the change from 2024 to 2025 on the NIBRS basis under the per-line conversion
and under the conversion with other assaults split by domestic and other victims."""
import world as W

AGG = ("4A", "4B", "4C", "4D")


def month(year, m):
    L = {k: 0.0 for k in AGG + ("4E_dv", "4E_non", "rob", "hom")}
    F = dict(L)
    for kind in W.STREET_KINDS + W.DV_KINDS:
        n = W.expected(kind, year, m)
        if kind in ("fire_hit", "fire_miss"):
            shares = {"4A": 1.0}
        elif kind == "knife":
            shares = {"4B": 1.0}
        elif kind == "other_weapon":
            shares = {"4C": 1.0}
        elif kind == "dv_weapon":
            shares = {"4A": 0.40, "4B": 0.35, "4C": 0.25}
        else:
            shares = W.LEGACY[kind]
        for line, sh in shares.items():
            key = line if line != "4E" else ("4E_dv" if kind in W.DV_KINDS else "4E_non")
            L[key] += n * sh
            if W.NIBRS[kind] == "13A":
                F[key] += n * sh
    L["rob"] = W.BASE["robbery"] * W.season("robbery", m) * W.level("robbery", year, m)
    F["rob"] = L["rob"] * W.ROB_EXTRA * 1.1
    L["hom"] = W.BASE["homicide"] * W.season("homicide", m) * W.level("homicide", year, m) * 1.06
    F["hom"] = L["hom"] / 1.06 * W.HOM_EXTRA * 1.45
    return L, F


def ladder():
    y24 = [month(2024, m) for m in range(1, 13)]
    y25 = [month(2025, m) for m in range(1, 13)]
    n25 = sum(sum(F.values()) for _, F in y25)
    q4 = y24[9:]
    q4n = sum(sum(F.values()) for _, F in q4)
    rate = lambda k: sum(F[k] for _, F in q4) / sum(L[k] for L, _ in q4)
    p4e = sum(F["4E_dv"] + F["4E_non"] for _, F in q4) / sum(L["4E_dv"] + L["4E_non"] for L, _ in q4)
    base = q4n
    for L, _ in y24[:9]:
        base += sum(rate(k) * L[k] for k in AGG) + rate("rob") * L["rob"] + rate("hom") * L["hom"]
    per_line = base + sum(p4e * (L["4E_dv"] + L["4E_non"]) for L, _ in y24[:9])
    golden = base + sum(rate("4E_dv") * L["4E_dv"] + rate("4E_non") * L["4E_non"] for L, _ in y24[:9])
    return {"per_line": n25 / per_line - 1, "golden": n25 / golden - 1}
