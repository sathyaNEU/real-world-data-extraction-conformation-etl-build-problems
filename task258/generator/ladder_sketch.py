"""The ladder sketched on paper before any row: each rung's count of page loads moved, by property, from lognormal paint parts.
The generator replaces it; kept so a resumed design starts from the settled parameters."""
import numpy as np
L=240; rU=0.48; rD=0.48; rT=0.70
N=120000
def run(P,seed=1,show=False):
    rng=np.random.default_rng(seed)
    ln=lambda m,s: m*np.exp(rng.normal(0,s,N))
    res={}
    for k,(tot,own,t,d,u,r) in P.items():
        T=ln(*t);D=ln(*d);U=ln(*u);R=ln(*r)
        lcp=T+D+U+R; w=tot*own/N; slow=lcp>2500
        res[k]=dict(R1=slow.sum()*w,R2=(slow&(rT*lcp<=2500)).sum()*w,R3=(slow&(T+rD*D+rU*U+R<=2500)).sum()*w,G=(slow&(T+L+rU*U+R<=2500)).sum()*w)
    out={}
    for key in ['R1','R2','R3','G']:
        s=sorted(res,key=lambda k:-res[k][key]); out[key]=(s[0],res[s[0]][key]/res[s[1]][key])
    if show:
        for k,v in res.items(): print(k,{a:round(b,2) for a,b in v.items()})
        print(out)
    return out,res
P={
 'Courier':  (62,0.20,(700,.5),(500,.7),(700,.6),(450,.6)),
 'Matchday': (38,0.30,(1000,.45),(650,.7),(650,.6),(600,.6)),
 'Hearth':   (26,0.85,(1700,.35),(400,.6),(900,.55),(550,.5)),
 'Ledger':   (34,0.60,(1150,.22),(150,.3),(420,.4),(900,.25)),
 'Trailhead':(17,0.72,(1300,.4),(700,.6),(1300,.5),(350,.5)),
 'Pantry':   (24,0.70,(400,.45),(3200,.5),(900,.5),(220,.5)),
}
run(P,show=True)
