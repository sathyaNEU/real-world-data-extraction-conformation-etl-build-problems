"""Scales each city's 2020 housing units (world.CITIES) until the golden population on the cut pack lands at
world.DESIRED, then prints every route.     python3 tune.py [iterations]"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")


def run(code):
    return subprocess.run([sys.executable, "-c", code], cwd=HERE, capture_output=True, text=True).stdout


def main(it):
    for _ in range(it):
        subprocess.run([sys.executable, "build.py", "--pack-only"], cwd=HERE, capture_output=True)
        out = run("import bundle as B, world as W, json\ng=B.population(%r)\na=B.acs(%r)\nc=B.census(%r)\n"
                  "print(json.dumps({k:[g[k],a[k],c[k]['pph']] for k in g}))" % (TARGET, TARGET, TARGET))
        import json
        g = json.loads(out)
        src = open(os.path.join(HERE, "world.py")).read()
        import importlib
        import world as W
        importlib.reload(W)
        for k, (hu, *_r) in W.CITIES.items():
            pop, occ, pph = g[k]
            nh = int(round(hu + (W.DESIRED[k] - pop) / (occ * pph)))
            src = re.sub(r'("%s":\s+\()\d+' % re.escape(k), r"\g<1>%d" % nh, src)
        open(os.path.join(HERE, "world.py"), "w").write(src)
    subprocess.run([sys.executable, "build.py", "--pack-only"], cwd=HERE, capture_output=True)
    print(run("import bundle as B, sources as S, pack as P\nt=%r\nr={n:B.population(t,n) for n in "
              "('golden','textbook','census')}\nr['truth']=S.truth(P.everything()['x'])\n"
              "for c in sorted(r['golden']): print('%%-15s '%%c + ' '.join('%%s %%6d'%%(n,r[n][c]) for n in r))\n"
              "for n in r: print(n, B.tier(r[n]))" % TARGET))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
