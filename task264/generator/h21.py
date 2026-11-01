"""H21: invented names clear of real United Kingdom places and NHS organisations, and of other cards' names."""
import json
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
GEN = set("""the and of on upon in by at under over st saint north south east west great little upper lower new old
nhs trust trusts foundation hospital hospitals university teaching general district royal county city town
network region regional health board care critical adult unit units review clinical services service ltd limited
llp bridge vale hill hills green park street road lane cross heath common end wood moor dale mere water infirmary
integrated community clinic clinics centre surgical treatment spine spinal healthcare outcomes house msk triage
musculoskeletal data commissioner""".split())


def norm_name(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z ]", " ", s)
    return "".join(w for w in s.split() if w not in GEN)


def lev2(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def references(own="task264"):
    ref = [l.strip() for l in open(HERE / "h21_reference_places.txt") if l.strip()]
    ref += [l.strip() for l in open(HERE / "h21_reference_nhs.txt") if l.strip()]
    rems = [(r, norm_name(r)) for r in ref]
    rems = [(r, m) for r, m in rems if len(m) >= 4]
    for p in sorted((REPO / ".claude/skills/fingerprint/cards").glob("*.json")):
        if p.stem == own:
            continue
        try:
            c = json.loads(p.read_text())
        except ValueError:
            continue
        for n in ((c.get("world") or {}).get("invented_names") or []):
            m = norm_name(n)
            if len(m) >= 4:
                rems.append(("card %s: %s" % (p.stem, n), m))
    return rems


def clashes(names, rems=None):
    rems = rems or references()
    out = []
    for name in names:
        m = norm_name(name)
        if len(m) < 4:
            continue
        for r, rm in rems:
            if lev2(m, rm) <= 2 or (len(rm) >= 5 and rm in m) or (len(m) >= 5 and m in rm):
                out.append((name, r))
                break
    return out


if __name__ == "__main__":
    import sys
    rems = references()
    for n in sys.argv[1:]:
        print(n, clashes([n], rems) or "clear")
