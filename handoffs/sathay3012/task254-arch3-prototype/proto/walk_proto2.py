import numpy as np
ff = np.array([70, 85, 60, 95, 110, 90, 75, 80, 65, 100, 120, 90, 140, 160], float)
nseg = len(ff)
E0 = 5*60
epochs = np.arange(E0, 11*60, 5)
def day_profile(rng, demand, incident):
    t0 = 7*60 + 0 - 15*(demand-1)/0.2
    tp = 7*60 + 55
    tc = 8*60 + 50 + 25*(demand-1)/0.2
    tt = np.tile(ff, (len(epochs), 1))
    for i, t in enumerate(epochs):
        tm = t + 2.5
        if t0 < tm < tc:
            frac = (tm - t0)/(tp - t0) if tm <= tp else max(0.0, 1-(tm-tp)/(tc-tp))
            qdelay = 1300*demand*frac
            spread = [0.10, 0.15, 0.20, 0.25, 0.30]
            for k, s in zip(range(4, 9), spread):
                # queue tail reaches upstream segments later
                lag = 0.18*(8-k)
                f2 = max(0.0, (frac - lag)/(1-lag)) if tm <= tp else frac
                tt[i, k] += qdelay*s*f2*1.6
        if 7*60+40 <= t <= 8*60+20:
            tt[i, 12] += 80*demand; tt[i, 13] += 110*demand
    if incident:
        k = rng.integers(2, 12); s = rng.integers(6*60+40, 8*60); d = rng.integers(20, 50)
        for i, t in enumerate(epochs):
            if s <= t < s+d: tt[i, k] += rng.integers(300, 900)
    return tt
def idx(m): return int((m - E0)//5)
def walk(tt, dep, mode='floor'):
    t = dep*60.0
    for k in range(nseg):
        m = t/60.0
        if mode == 'floor':
            v = tt[idx(m), k]
        elif mode == 'interp':  # linear between epoch midpoints
            x = (m - E0 - 2.5)/5.0; i0 = int(np.floor(x)); w = x - i0
            v = (1-w)*tt[i0, k] + w*tt[i0+1, k]
        elif mode == 'mid':  # epoch at segment midpoint (iterate once)
            v0 = tt[idx(m), k]; v = tt[idx(m + v0/120.0), k]
        t += v
    return (t - dep*60.0)/60.0
def inst(tt, dep): return tt[idx(dep)].sum()/60.0
days = 185
rng = np.random.default_rng(2541)
DAYS = []
for d in range(days):
    demand = float(np.clip(rng.lognormal(0, 0.13), 0.72, 1.5))
    inc = rng.random() < 0.08
    DAYS.append(day_profile(rng, demand, inc))
deadline = 8*60
deps = [7*60 + m for m in range(0, 46, 5)]
P = np.percentile(np.stack(DAYS), 90, axis=0)   # p90 profile by epoch x segment
P50 = np.percentile(np.stack(DAYS), 50, axis=0)
print('dep   inst  walkF  walkI  walkM  p90prof_inst  p90prof_walk  (share on time by 08:00)')
for dep in deps:
    s_inst = np.mean([dep + inst(tt, dep) <= deadline for tt in DAYS])
    s_wf = np.mean([dep + walk(tt, dep, 'floor') <= deadline for tt in DAYS])
    s_wi = np.mean([dep + walk(tt, dep, 'interp') <= deadline for tt in DAYS])
    s_wm = np.mean([dep + walk(tt, dep, 'mid') <= deadline for tt in DAYS])
    pi = dep + P[idx(dep)].sum()/60.0 <= deadline
    pw = dep + walk(P, dep, 'floor') <= deadline
    print(f"{dep//60}:{dep%60:02d}  {s_inst:5.3f} {s_wf:5.3f} {s_wi:5.3f} {s_wm:5.3f}   {pi!s:6}        {pw!s:6}")
