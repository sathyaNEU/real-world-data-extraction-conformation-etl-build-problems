import numpy as np
src=open('search6.py').read().split("best=None; rng0")[0]
s6={}; exec(compile(src,'s6','exec'),s6)
P={'nschool': 178, 'summer': 0.654287064354632, 'dsd': 0.25661493747548575, 'jit': 8.007689541612194, 'onset': 25.372436212669186, 'oslope': 34.06724490267454, 'peak': 57.18403016686682, 'qmax': 2576.305524230817, 'dthr': 0.5017961982227336, 'shape': 1.0168772150974978, 'lag': 0.09917884329259773, 'art': 109.75051128777693, 'segsd': 0.2027488763807732, 'pinc': 0.15528319330550072}
DAYS,INC=s6['gen'](25403,P)
ff=s6['ff']; K=s6['K']; E0=s6['E0']; ix=s6['ix']
A1,A2=4.0,3.0
deps=[6*60+m for m in range(30,85,5)]
def walk(tt,d,mode='floor'):
    t=(d+A1)*60.0
    for k in range(K):
        m=t/60.0
        if mode=='floor': v=tt[ix(m),k]
        elif mode=='interp':
            x=(m-E0-2.5)/5.0; i0=int(np.floor(x)); w=x-i0; v=(1-w)*tt[i0,k]+w*tt[i0+1,k]
        else:
            v=tt[ix(m),k]
            for _ in range(3): v=tt[ix(m+v/120.0),k]
        t+=v
    return t/60.0+A2   # arrival clock minutes
def inst(tt,d,at=0.0): return d+A1+tt[ix(d+at)].sum()/60.0+A2
def mid(tt,d): return d+A1+tt[ix(d+A1+ff.sum()/120.0)].sum()/60.0+A2
def cnt(f,days): return [int(sum(f(tt,d)<=480 for tt in days)) for d in deps]
def latest(c,n):
    ok=[d for d,x in zip(deps,c) if x>=0.9*n]; return f'{ok[-1]//60}:{ok[-1]%60:02d}' if ok else None
sub=[tt for tt,m in zip(DAYS,INC) if not m]
A=np.stack(DAYS); P90=np.percentile(A,90,axis=0); P50=np.percentile(A,50,axis=0)
rows={'R0 instantaneous at departure':(lambda a,d:inst(a,d),DAYS),
 'R0b instantaneous at freeway entry':(lambda a,d:inst(a,d,A1),DAYS),
 'R1 midpoint read':(mid,DAYS),
 'GOLD walk per day':(lambda a,d:walk(a,d),DAYS),
 'walk interp':(lambda a,d:walk(a,d,'interp'),DAYS),
 'walk midpoint-epoch':(lambda a,d:walk(a,d,'mf'),DAYS),
 'slip incidents dropped inst':(lambda a,d:inst(a,d),sub),
 'slip incidents dropped walk':(lambda a,d:walk(a,d),sub)}
print('slots',[f'{d//60}:{d%60:02d}' for d in deps])
for k,(f,days) in rows.items():
    c=cnt(f,days); print(f'{k:36s}',c,latest(c,len(days)), len(days))
for k,PP in [('p90 profile instantaneous',P90),('p90 profile walked',P90),('p50 profile walked',P50)]:
    if 'instantaneous' in k: arr=[inst(PP,d) for d in deps]
    else: arr=[walk(PP,d) for d in deps]
    ok=[d for d,a in zip(deps,arr) if a<=480]
    print(f'{k:36s}',[f'{int(a//60)}:{a%60:04.1f}' for a in arr], f'{ok[-1]//60}:{ok[-1]%60:02d}')
for d in [7*60+5,7*60+10]:
    arr=np.array([(walk(tt,d)-480)*60 for tt in DAYS])
    print(f'{d//60}:{d%60:02d}', 'closest arrivals to 8:00 (s):', np.sort(np.abs(arr))[:4].round(1))
# means for cost ask
Ew={d:np.mean([walk(tt,d)-d for tt in DAYS]) for d in deps}
Ei={d:np.mean([inst(tt,d)-d for tt in DAYS]) for d in deps}
print('mean trip walked',[round(Ew[d],2) for d in deps]); print('mean trip inst  ',[round(Ei[d],2) for d in deps])
np.save('Ew.npy',np.array([Ew[d] for d in deps])); np.save('Ei.npy',np.array([Ei[d] for d in deps]))
