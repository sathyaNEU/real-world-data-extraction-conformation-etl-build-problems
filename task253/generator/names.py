"""Invented localities and school names, and the real-name check (reduce-house-fixes H21).

Localities are built from English place-name morphemes and kept only when their distinctive part sits at
least three edits from every Australian locality, statistical-area, local-government and electorate name in
ref/au_place_names.txt (derived from the public Australian postcode and locality table), and neither
contains nor sits inside one."""
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GENERIC = {"north", "south", "east", "west", "upper", "lower", "mount", "mt", "port", "point", "creek", "river",
           "bay", "beach", "hill", "hills", "heights", "park", "vale", "valley", "plains", "plain", "flat",
           "flats", "junction", "lake", "lakes", "springs", "island", "head", "heads", "bridge", "gully", "the",
           "of", "st", "saint", "new", "old", "central", "city", "council", "shire", "regional", "region",
           "and", "-", "outer", "inner", "greater", "rural", "surrounds", "district", "town", "village"}
PRE = ["Ard", "Bel", "Bran", "Cal", "Carra", "Del", "Dun", "Ell", "Fal", "Fern", "Gar", "Glen", "Hal", "Har",
       "Kel", "Kil", "Lan", "Lis", "Mar", "Mel", "Mor", "Nor", "Pel", "Pen", "Quar", "Ran", "Rath", "Sel",
       "Tal", "Tam", "Tre", "Val", "Wal", "Wes", "Yar", "Brack", "Cran", "Fen", "Hol", "Lind", "Ock", "Strath",
       "Thorn", "Whin", "Bram", "Corr", "Dray", "Elder", "Ferris", "Gilder", "Harl", "Lorr", "Marl", "Nether",
       "Ashen", "Beck", "Birch", "Bram", "Brin", "Carn", "Coll", "Crom", "Dalby", "Darn", "Drum", "Eddy", "Esk",
       "Farr", "Fox", "Gale", "Gorm", "Hask", "Heath", "Hind", "Iver", "Jarr", "Kin", "Kirk", "Lam", "Lark",
       "Leven", "Lynd", "Mab", "Mill", "Moss", "Netter", "Oak", "Orr", "Pask", "Pim", "Quill", "Red", "Rook",
       "Rush", "Sand", "Shel", "Skel", "Sorr", "Stan", "Stoke", "Swin", "Tarn", "Tidd", "Tull", "Ulls",
       "Wend", "Wether", "Whit", "Wil", "Wold", "Wyn", "Yew"]
SUF = ["anby", "ardine", "avon", "bourne", "brae", "bury", "combe", "dale", "dene", "don", "field", "ford",
       "gate", "grove", "haven", "holme", "hurst", "ington", "leigh", "lowe", "mere", "minster", "more",
       "ock", "rigg", "shaw", "stead", "stone", "thorpe", "ton", "wick", "wood", "worth", "yard", "ridge",
       "brook", "cliffe", "court", "hay", "low"]
SAINTS = ["St Joseph's", "St Mary's", "St Patrick's", "St Brigid's", "Sacred Heart", "St Michael's",
          "Holy Family", "St Columba's", "Our Lady of Mercy", "St Francis Xavier's", "St John's", "St Anne's",
          "St Thomas More", "Holy Cross", "St Kevin's", "St Monica's", "St Catherine's",
          "Our Lady of the Rosary", "St Bernadette's", "St Mark's", "St Luke's", "St Peter's", "St Paul's",
          "St Therese's", "St Clare's", "St Dominic's", "St Benedict's", "St Brendan's", "St Gerard's",
          "St Agnes'", "Corpus Christi", "Good Shepherd", "St Vincent's", "St Augustine's", "St Cecilia's",
          "St Raphael's", "St Ambrose's", "St Finbar's", "St Mel's", "St Canice's"]


# drawn once with localities(140, seed=253) and curated for spelling; checks.py re-runs clashes() on each
LOCALITIES = ['Quillton', 'Gilderworth', 'Lyndstead', 'Dunminster', 'Farrmore', 'Wethercliffe', 'Galecliffe', 'Stanrigg', 'Haskwick', 'Ardanby', 'Branbrae', 'Collminster', 'Sanddene', 'Orrhay', 'Brackdene', 'Stokecourt', 'Skelanby', 'Carnbrae', 'Darnthorpe', 'Penlow', 'Cromstead', 'Lisgate', 'Tiddstead', 'Birchbrook', 'Selardine', 'Wilcourt', 'Wendcombe', 'Morcliffe', 'Levenwick', 'Galeminster', 'Tullgate', 'Swingate', 'Whinstead', 'Ferriscombe', 'Wetherwood', 'Sorrardine', 'Swincliffe', 'Gilderminster', 'Quillworth', 'Stokemore', 'Kirkmere', 'Kirkanby', 'Orrthorpe', 'Carracourt', 'Tiddbury', 'Gormyard', 'Cromcliffe', 'Oakbrae', 'Gormbourne', 'Pasklowe', 'Haskrigg', 'Lisardine', 'Stananby', 'Netterlowe', 'Skellowe', 'Fenrigg', 'Yewworth', 'Birchbourne', 'Levenbrook', 'Drumhurst', 'Ockcliffe', 'Lyndcliffe', 'Oakbourne', 'Drumbourne', 'Tullcombe', 'Hindbrae', 'Yewlowe', 'Nethercourt', 'Foxington', 'Ullsrigg', 'Ashenhurst', 'Drayminster', 'Beckanby', 'Woldhurst', 'Wynlowe', 'Ullsminster', 'Darnbourne', 'Dunanby', 'Eddyford', 'Shelstead', 'Ashenwick', 'Rookworth', 'Marminster', 'Rathbrae', 'Sorrbrook', 'Whinhurst', 'Ockardine', 'Quarthorpe', 'Foxardine', 'Iverworth', 'Ivercombe', 'Shelthorpe', 'Calrigg', 'Brinrigg', 'Beckbury', 'Lamyard', 'Harlardine', 'Morhurst', 'Corrlowe', 'Corrworth', 'Hindbourne', 'Lindlowe', 'Falthorpe', 'Eskhay', 'Belminster', 'Cranhurst', 'Trebrook', 'Redbrae', 'Kilstead', 'Pimrigg', 'Farrbury', 'Tarndene', 'Cranlowe', 'Kilcliffe', 'Valdene', 'Eskyard', 'Brinminster', 'Holanby', 'Wendanby', 'Lamanby', 'Treardine', 'Lindminster', 'Wynmere']


def _lev(a, b, cap=3):
    if abs(len(a) - len(b)) >= cap:
        return cap
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        lo = cur[0]
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
            lo = min(lo, cur[j])
        if lo >= cap:
            return cap
        prev = cur
    return min(prev[-1], cap)


def remainder(name):
    s = re.sub(r"[^a-z ]", " ", name.lower().replace("'", ""))
    return " ".join(w for w in s.split() if w not in GENERIC)


def reference():
    with open(os.path.join(HERE, "ref", "au_place_names.txt")) as f:
        names = [remainder(x) for x in f.read().splitlines() if x.strip()]
    return sorted(set(n for n in names if n))


def clashes(name, ref):
    r = remainder(name)
    if not r:
        return []
    out = []
    for x in ref:
        if abs(len(x) - len(r)) >= 3 and not (len(x) >= 4 and x in r) and not (len(r) >= 4 and r in x):
            continue
        if len(x) >= 4 and (x in r or (len(r) >= 4 and r in x)):
            out.append(x)
        elif _lev(r, x) < 3:
            out.append(x)
    return out


def localities(k, seed=253):
    rng = np.random.default_rng(seed)
    ref = reference()
    cands = sorted({p + s for p in PRE for s in SUF if not (p[-1] == s[0] and p[-1] in "aeiou")})
    cands = [c[0] + c[1:].lower() for c in cands]
    order = rng.permutation(len(cands))
    out, stems = [], set()
    for i in order:
        c = cands[i]
        stem = c[:3]
        if sum(1 for x in out if x[:3] == stem) >= 2:
            continue
        if clashes(c, ref):
            continue
        if any(_lev(c.lower(), o.lower()) < 3 for o in out):
            continue
        out.append(c)
        stems.add(stem)
        if len(out) == k:
            break
    assert len(out) == k, len(out)
    return out


# Parish dedications for the register, weighted the way a state Catholic system's list runs: a handful of
# dedications carried by many parishes, a long tail carried by one or two. Secondary colleges draw from their
# own list. Neither carries a locality that exists, so no school here is a real school (H21).
DEDICATIONS = [
    ("St Joseph's", 14), ("St Mary's", 11), ("St Patrick's", 9), ("Sacred Heart", 7), ("St Brigid's", 5),
    ("Holy Family", 4), ("St Michael's", 4), ("St John's", 3), ("St Francis Xavier's", 3), ("Our Lady of Mercy", 2),
    ("St Anne's", 2), ("Holy Cross", 2), ("St Columba's", 2), ("Our Lady of the Rosary", 2), ("St Peter's", 2),
    ("St Thomas More", 2), ("St Kevin's", 2), ("St Monica's", 2), ("Mary MacKillop", 2), ("Our Lady of Lourdes", 2),
    ("St Mary MacKillop", 1), ("Holy Spirit", 2), ("St Catherine's", 1), ("St Bernadette's", 1), ("St Mark's", 1),
    ("St Luke's", 1), ("St Paul's", 1), ("St Therese's", 1), ("St Clare's", 1), ("St Dominic's", 1),
    ("St Benedict's", 1), ("St Brendan's", 1), ("St Gerard's", 1), ("St Agnes'", 1), ("Corpus Christi", 1),
    ("Good Shepherd", 1), ("St Vincent's", 1), ("St Augustine's", 1), ("St Cecilia's", 1), ("St Raphael's", 1),
    ("St Ambrose's", 1), ("St Finbar's", 1), ("St Canice's", 1), ("Our Lady Help of Christians", 1),
    ("Our Lady Star of the Sea", 1), ("Our Lady of the Assumption", 1), ("Our Lady Queen of Peace", 1),
    ("Christ the King", 1), ("Holy Trinity", 1), ("Immaculate Conception", 1), ("Infant Jesus", 1),
    ("Guardian Angels", 1), ("Mater Dei", 1), ("Sts Peter and Paul", 1), ("St Thomas Aquinas", 1),
    ("St Francis of Assisi", 1), ("St Mary of the Angels", 1), ("St John Vianney's", 1), ("St Margaret Mary's", 1),
    ("St Ignatius'", 1), ("St Bernard's", 1), ("St Oliver Plunkett", 1), ("St Anthony's", 1), ("St Martin's", 1),
    ("St Rita's", 1), ("St Joachim's", 1), ("St Philomena's", 1), ("St Aidan's", 1), ("St Fiacre's", 1),
    ("Our Lady of Fatima", 1), ("St Laurence's", 1), ("Holy Rosary", 1), ("St Damian's", 1),
]
COLLEGES = ["St Joseph's", "St Mary's", "St Patrick's", "Marist", "Mercy", "Mary MacKillop", "MacKillop",
            "Trinity", "Emmanuel", "John Paul", "Xavier", "Holy Spirit", "St Francis Xavier", "Sacred Heart",
            "St Clare's", "St Paul's", "Corpus Christi", "Lumen Christi", "St John's", "Good Samaritan"]


def retitle(W, seed):
    """Primary dedications (unique inside a locality; a few parishes carry their town's name instead) and the
    secondary colleges' names, on a stream of their own so no other draw moves."""
    rng = np.random.default_rng([seed, 41])
    names = [d for d, _ in DEDICATIONS]
    wts = np.array([w for _, w in DEDICATIONS], float)
    loc = W["loc"]
    title = np.empty(len(loc), dtype=object)
    for L in sorted(set(loc)):
        idx = np.where(loc == L)[0]
        picks = rng.choice(len(names), size=len(idx), replace=False, p=wts / wts.sum())
        for m, p in zip(idx, picks):
            title[m] = names[p]
        if len(idx) == 1 and rng.random() < 0.06:
            title[idx[0]] = L
    W["title"] = title
    used = set()
    for s in W["sec"]:
        while True:
            nm = _college(s, rng)
            ded = nm.split(" College")[0].replace(" Catholic", "").replace(" Regional", "")
            if nm not in used and sum(1 for u in used if u.startswith(ded + " ")) < 2:
                break
        used.add(nm)
        s["name"] = nm


def _college(s, rng):
    if rng.random() < 0.42:
        base = s["locality"]
        for v in ("North ", "South ", "East ", "West ", "Upper ", "Lower "):
            base = base.replace(v, "")
        base = base.replace(" Heights", "").replace(" Park", "").split(" ")[0]
        return "%s Catholic College" % base
    t = COLLEGES[int(rng.integers(len(COLLEGES)))]
    kinds = ["College", "College", "Catholic College"] + ([] if s["region"] in ("MN", "MS") else ["Regional College"])
    return "%s %s" % (t, kinds[int(rng.integers(len(kinds)))])
