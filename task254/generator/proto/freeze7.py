import numpy as np, json
import importlib.util
spec=importlib.util.spec_from_file_location('s6','search6.py'); s6=importlib.util.module_from_spec(spec)
src=open('search6.py').read().split("best=None; rng0")[0]
exec(compile(src,'s6','exec'),s6.__dict__)
P={'nschool': 178, 'summer': 0.654287064354632, 'dsd': 0.25661493747548575, 'jit': 8.007689541612194, 'onset': 25.372436212669186, 'oslope': 34.06724490267454, 'peak': 57.18403016686682, 'qmax': 2576.305524230817, 'dthr': 0.5017961982227336, 'shape': 1.0168772150974978, 'lag': 0.09917884329259773, 'art': 109.75051128777693, 'segsd': 0.2027488763807732, 'pinc': 0.15528319330550072}
DAYS,INC=s6.gen(25403,P)
A=np.stack(DAYS); P90=np.percentile(A,90,axis=0); P50=np.percentile(A,50,axis=0)
deps=[6*60+m for m in range(30,85,5)]
acc=7.0; ACC=8*60
def cnt(f,days): return [int(sum(d+acc+f(tt,d)<=ACC for tt in days)) for d in deps]
sub=[tt for tt,m in zip(DAYS,INC) if not m]
walk=s6.walk; inst=s6.inst; mid=s6.midread
rows={'R0 instantaneous per day':cnt(inst,DAYS),'slip: incident days dropped, instantaneous':cnt(inst,sub),
 'R2 midpoint read':cnt(mid,DAYS),'GOLD walk (epoch at entry)':cnt(lambda a,d:walk(a,d),DAYS),
 'walk, interpolated between epochs':cnt(lambda a,d:walk(a,d,'interp'),DAYS),'walk, epoch at segment midpoint':cnt(lambda a,d:walk(a,d,'mf'),DAYS),
 'slip: incident days dropped, walk':cnt(lambda a,d:walk(a,d),sub)}
print('n days',len(DAYS),'incident days',int(INC.sum()))
print('slot',[f'{d//60}:{d%60:02d}' for d in deps])
for k,v in rows.items(): print(f'{k:45s}',v)
prof={'R1 90th-percentile profile, instantaneous':[d+acc+P90[s6.ix(d)].sum()/60 for d in deps],
      'R3 90th-percentile profile, walked':[d+acc+walk(P90,d) for d in deps],
      'median profile, walked':[d+acc+walk(P50,d) for d in deps]}
for k,v in prof.items(): print(f'{k:45s}',[f'{int(x//60)}:{x%60:04.1f}' for x in v])
# p90 of walked and instantaneous trip times at each slot
for d in deps:
    w=[walk(tt,d)+acc for tt in DAYS]; i=[inst(tt,d)+acc for tt in DAYS]
    print(f'{d//60}:{d%60:02d} walked p50 {np.percentile(w,50):5.1f} p90 {np.percentile(w,90):5.1f} | instantaneous p50 {np.percentile(i,50):5.1f} p90 {np.percentile(i,90):5.1f}')
