import numpy as np, itertools
# 16 segments: 13 freeway TMCs + 3 arterial; free-flow seconds
ff = np.array([62,74,58,81,95,77,66,70,56,88,72,64,90, 75,95,110], float)
K = len(ff)
E0 = 5*60; NE = 72                      # epochs 05:00..10:55
ep = E0 + 5*np.arange(NE)
BN = 9                                  # bottleneck segment index (0-based)
QSEG = [4,5,6,7,8]                      # queue spills back over these
def gen_day(rng, demand, incident, school):
    tt = np.tile(ff, (NE,1))
    # bottleneck queue: onset earlier/stronger with demand; school days heavier
    d = demand * (1.0 if school else 0.82)
    t0 = 6*60+50 - 25*(d-1)/0.25
    tp = 7*60+50 + 10*(d-1)/0.25
    tc = 8*60+45 + 30*(d-1)/0.25
    peak = max(0.0, 1500*(d-0.55))       # seconds of queue delay at peak
    for i,t in enumerate(ep):
        tm = t+2.5
        if t0 < tm < tc:
            f = (tm-t0)/(tp-t0) if tm <= tp else max(0.0,1-(tm-tp)/(tc-tp))
            q = peak*f
            # tail grows backward: upstream segments join later
            for j,k in enumerate(reversed(QSEG)):
                share = [0.34,0.26,0.19,0.13,0.08][j]
                lag = 0.16*j
                g = 0.0 if f < lag else (f-lag)/(1-lag) if tm <= tp else f
                tt[i,k] += q*share*g
            tt[i,BN] += 0.25*q
        # downtown arterial peak 07:35-08:25
        if 7*60+35 <= tm <= 8*60+25:
            w = 1-abs(tm-(8*60))/25.0
            tt[i,13] += 70*d*w; tt[i,14] += 95*d*w; tt[i,15] += 60*d*w
    if incident:
        k = int(rng.integers(1,13)); s = int(rng.integers(6*60+30, 8*60+10)); L = int(rng.integers(20,55))
        extra = float(rng.integers(240,780))
        for i,t in enumerate(ep):
            if s <= t < s+L: tt[i,k] += extra
    tt *= rng.lognormal(0,0.03,size=tt.shape)   # measurement noise
    return tt
def ix(m): return int((m-E0)//5)
def walk(tt, dep, mode='floor'):
    t = dep*60.0
    for k in range(K):
        m = t/60.0
        if mode=='floor': v = tt[ix(m),k]
        elif mode=='interp':
            x=(m-E0-2.5)/5.0; i0=int(np.floor(x)); w=x-i0; v=(1-w)*tt[i0,k]+w*tt[i0+1,k]
        elif mode=='exitfix':   # iterate to use the epoch at the segment midpoint
            v=tt[ix(m),k]
            for _ in range(3): v=tt[ix(m+v/120.0),k]
        t += v
    return (t-dep*60)/60.0
def inst(tt, dep): return tt[ix(dep)].sum()/60.0
def midread(tt, dep):   # all segments read at departure + half the free-flow time
    m = dep + ff.sum()/120.0
    return tt[ix(m)].sum()/60.0
rng = np.random.default_rng(25403)
N = 250; DAYS=[]; INC=[]
for dd in range(N):
    school = dd < 178
    demand = float(np.clip(rng.lognormal(0,0.11),0.78,1.38))
    inc = rng.random() < 0.075
    DAYS.append(gen_day(rng,demand,inc,school)); INC.append(inc)
INC=np.array(INC); A=np.stack(DAYS)
P90=np.percentile(A,90,axis=0); P50=np.percentile(A,50,axis=0)
ACC = 8*60   # on time if arrival <= 08:00 ; fixed access legs 3 min out + 4 min in
acc = 7.0
deps=[6*60+m for m in range(30,100,5)]
def share(f):
    return np.array([np.mean([d + acc + f(tt,d) <= ACC for tt in DAYS]) for d in deps])
def share_sub(f, mask):
    sub=[tt for tt,m in zip(DAYS,mask) if m]
    return np.array([np.mean([d + acc + f(tt,d) <= ACC for tt in sub]) for d in deps])
rows = {
 'inst_day': share(inst),
 'inst_noinc': share_sub(inst, ~INC),
 'mid_read': share(midread),
 'walk_floor(golden)': share(lambda tt,d: walk(tt,d,'floor')),
 'walk_interp': share(lambda tt,d: walk(tt,d,'interp')),
 'walk_midfix': share(lambda tt,d: walk(tt,d,'exitfix')),
 'walk_noinc': share_sub(lambda tt,d: walk(tt,d,'floor'), ~INC),
}
prof = {'walk_p90prof': [d+acc+walk(P90,d) <= ACC for d in deps],
        'inst_p90prof': [d+acc+P90[ix(d)].sum()/60 <= ACC for d in deps],
        'walk_p50prof': [d+acc+walk(P50,d) <= ACC for d in deps]}
hdr = 'slot  ' + ' '.join(f'{d//60}:{d%60:02d}' for d in deps)
print(hdr)
for k,v in rows.items():
    print(f'{k:20s}', ' '.join(f'{x:4.2f}' for x in v), ' latest>=0.90:', [f'{d//60}:{d%60:02d}' for d,x in zip(deps,v) if x>=0.9][-1:])
for k,v in prof.items():
    print(f'{k:20s}', ' '.join(' yes' if x else '  no' for x in v), ' latest:', [f'{d//60}:{d%60:02d}' for d,x in zip(deps,v) if x][-1:])
