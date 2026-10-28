"""Where each centre meets, and the 2025 gram panchayat (GP) reorganisation.

Every centre meets in one village; its members live there. The member KYC records the village, GP and block as they
stood when the member enrolled. Odisha's Panchayati Raj department redrew some coastal GPs with effect from 1 April
2025: a split GP keeps its name with its headquarters village and the villages listed as staying, and the listed
villages form a new GP; a renamed GP keeps all its villages. The state's declaration of severely affected GPs after
the cyclone names GPs as they stand now, so a member enrolled before 1 April 2025 in a moved village carries the old
GP's name, which still exists and is still a GP."""
from __future__ import annotations

import numpy as np

import params as P

BRANCH_BLOCKS = {
    "KND": ["Kendrapara", "Derabish"], "PTM": ["Pattamundai", "Aul"], "RJN": ["Rajnagar", "Mahakalapada"],
    "JSP": ["Jagatsinghpur", "Raghunathpur"], "TRT": ["Tirtol", "Balikuda"], "ERS": ["Ersama", "Kujang"],
    "BDK": ["Bhadrak", "Tihidi"], "CHB": ["Chandbali", "Basudevpur"], "BLS": ["Balasore", "Remuna"],
    "BST": ["Basta", "Baliapal"], "JJR": ["Korei", "Dharmasala"], "BNJ": ["Binjharpur", "Dasarathpur"],
    "SLP": ["Salepur", "Mahanga"], "NIA": ["Niali", "Kantapada"],
}
# the blocks the declaration covers in full, and the share of GPs declared elsewhere in the coastal districts
EXPOSED = {"Rajnagar", "Mahakalapada", "Ersama", "Kujang", "Chandbali", "Basudevpur", "Baliapal", "Pattamundai"}
COASTAL = {"Kendrapara", "Jagatsinghpur", "Bhadrak", "Balasore"}
PRE = ["Bada", "Sana", "Nua", "Gopi", "Kusu", "Tala", "Bali", "Rama", "Hari", "Jagan", "Kanti", "Patta", "Sri",
       "Gopal", "Narayan", "Basanta", "Chandra", "Kalia", "Bhuban", "Raghu", "Madhu", "Ananta", "Dhenu", "Kanak",
       "Biswa", "Parama", "Sundar", "Lakshmi", "Govinda", "Krishna", "Bhagaba", "Nimai", "Damodar", "Benu", "Jambu",
       "Kusuma", "Baula", "Champa", "Kendu", "Amba", "Tentuli", "Bahada", "Haldi", "Kaitha", "Panasa", "Kadali"]
SUF = ["pur", "pada", "gaon", "patana", "nagar", "sahi", "kud", "chhak", "kote", "garh", "dihi", "bindha",
       "khandi", "mundai", "pali", "palli", "deuli", "khunta", "sasan", "bania", "jodi", "bari", "pokhari", "danda"]


def _names(rng, n, used):
    out = []
    while len(out) < n:
        nm = str(rng.choice(PRE)) + str(rng.choice(SUF))
        if nm not in used:
            used.add(nm)
            out.append(nm)
    return out


def build(centres, seed):
    """Returns (villages, gps, reorg, declared): villages maps centre index -> dict(village, gp_old, gp_now, block,
    district); gps lists GP dicts as they stand now; reorg lists the 2025 changes; declared is the set of GP names
    (now) the state declared severely affected."""
    rng = np.random.default_rng(seed)
    used = set()
    by_branch = {}
    for ci, c in enumerate(centres):
        by_branch.setdefault(c["branch"], []).append(ci)
    gps_old = []      # dicts: name, block, district, villages, hq
    centre_v = {}
    for b in sorted(by_branch):
        cis = by_branch[b]
        blocks = BRANCH_BLOCKS[b]
        dist = centres[cis[0]]["district"]
        n_gp = max(8, len(cis) // 7)
        names = _names(rng, n_gp, used)
        branch_gps = [dict(name=nm, block=blocks[i % len(blocks)], district=dist, villages=[], hq=None)
                      for i, nm in enumerate(names)]
        gps_old.extend(branch_gps)
        for ci in cis:
            g = branch_gps[int(rng.integers(0, len(branch_gps)))]
            if g["villages"] and rng.random() < 0.40:
                v = g["villages"][int(rng.integers(0, len(g["villages"])))]
            else:
                v = _names(rng, 1, used)[0]
                g["villages"].append(v)
                if g["hq"] is None:
                    g["hq"] = v
            centre_v[ci] = (v, g)
    # the reorganisation, coastal districts only: splits (the listed villages leave for a new GP) and renames
    coastal = [g for g in gps_old if g["district"] in COASTAL and len(g["villages"]) >= 3]
    order = rng.permutation(len(coastal))
    splits = [coastal[i] for i in order[:22]]
    renames = [coastal[i] for i in order[22:28]]
    now = {}          # village -> current GP name
    reorg = []
    gp_now = {}       # current GP name -> dict(block, district)
    for g in gps_old:
        for v in g["villages"]:
            now[v] = g["name"]
        gp_now[g["name"]] = dict(block=g["block"], district=g["district"])
    for g in splits:
        stay = [g["hq"]]
        rest = [v for v in g["villages"] if v != g["hq"]]
        k = max(1, len(rest) // 2 + int(rng.integers(0, 2)))
        move = list(rng.choice(rest, size=min(k, len(rest)), replace=False))
        new = _names(rng, 1, used)[0]
        for v in move:
            now[v] = new
        gp_now[new] = dict(block=g["block"], district=g["district"])
        reorg.append(dict(kind="split", old=g["name"], new=new, block=g["block"], district=g["district"],
                          moved=sorted(move), stayed=sorted(v for v in g["villages"] if v not in move)))
    for g in renames:
        new = g["name"] + " " + str(rng.choice(["Sasan", "Patana", "Khas"]))
        if new in used:
            continue
        used.add(new)
        for v in g["villages"]:
            now[v] = new
        gp_now[new] = dict(block=g["block"], district=g["district"])
        del gp_now[g["name"]]
        reorg.append(dict(kind="rename", old=g["name"], new=new, block=g["block"], district=g["district"],
                          moved=sorted(g["villages"]), stayed=[]))
    # the declaration: every GP now in an exposed block, and about a third of the other coastal GPs; a split GP's two
    # halves are declared independently, so a moved village can sit in a declared GP while its old GP is not, and the
    # reverse
    declared = set()
    for name, info in sorted(gp_now.items()):
        if info["district"] not in COASTAL:
            continue
        if info["block"] in EXPOSED or rng.random() < 0.33:
            declared.add(name)
    for r in reorg:
        if r["kind"] == "split":
            if rng.random() < 0.6:
                declared.add(r["new"])
                declared.discard(r["old"])
            else:
                declared.add(r["old"])
                declared.discard(r["new"])
    villages = {}
    for ci, (v, g) in centre_v.items():
        villages[ci] = dict(village=v, gp_old=g["name"], gp_now=now[v], block=g["block"], district=g["district"])
    return villages, gp_now, reorg, declared
