import numpy as np
src=open('search6.py').read().split("best=None; rng0")[0]
s6={}; exec(compile(src,'s6','exec'),s6)
P={'nschool': 178, 'summer': 0.654287064354632, 'dsd': 0.25661493747548575, 'jit': 8.007689541612194, 'onset': 25.372436212669186, 'oslope': 34.06724490267454, 'peak': 57.18403016686682, 'qmax': 2576.305524230817, 'dthr': 0.5017961982227336, 'shape': 1.0168772150974978, 'lag': 0.09917884329259773, 'art': 109.75051128777693, 'segsd': 0.2027488763807732, 'pinc': 0.15528319330550072}
DAYS,INC=s6['gen'](25403,P)
walk=s6['walk']; inst=s6['inst']
deps=[6*60+m for m in range(30,85,5)]
def latest(cnts,n):
    ok=[d for d,c in zip(deps,cnts) if c>=0.9*n]; return f'{ok[-1]//60}:{ok[-1]%60:02d}' if ok else None
for acc in [0.0,7.0]:
    # walked: the access leg delays entry to the first segment
    def walk_acc(tt,d,acc=acc):
        # lot to ramp is 4 of the 7 minutes, ramp exit to stop 3
        a1=acc*4/7; a2=acc*3/7
        return a1+walk(tt,d+a1/60*60/60) + a2 if False else None
    cw=[int(sum(d+acc+walk(tt,d)<=480 for tt in DAYS)) for d in deps]
    ci=[int(sum(d+acc+inst(tt,d)<=480 for tt in DAYS)) for d in deps]
    print('acc',acc,'walk',cw,latest(cw,250),'| inst',ci,latest(ci,250))
# access leg placed before the freeway: the shuttle enters segment 1 four minutes after departure
cw=[]
for d in deps:
    c=0
    for tt in DAYS:
        t=d*60.0+4*60
        for k in range(s6['K']):
            v=tt[s6['ix'](t/60.0),k]; t+=v
        t+=3*60
        c+= (t/60.0)<=480
    cw.append(c)
print('walk with the first access leg delaying entry', cw, latest(cw,250))
# strict vs inclusive 8:00
cs=[int(sum(d+7+walk(tt,d)<480 for tt in DAYS)) for d in deps]
print('strict', cs)
# nearest arrival to 8:00 at 7:05 and 7:10 (seconds)
for d in [7*60+5,7*60+10]:
    arr=np.array([(d+7+walk(tt,d)-480)*60 for tt in DAYS])
    print(d, 'closest arrivals to 8:00 (s):', np.sort(np.abs(arr))[:5].round(1))
