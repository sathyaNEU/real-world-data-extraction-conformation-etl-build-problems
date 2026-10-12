import numpy as np
rng = np.random.default_rng(2541)
# 14 segments, free-flow seconds
ff = np.array([70, 85, 60, 95, 110, 90, 75, 80, 65, 100, 120, 90, 140, 160], float)  # ~22 min free flow
nseg = len(ff)
epochs = np.arange(5*60, 11*60, 5)   # minutes from midnight, 05:00..10:55
def day_profile(demand, incident):
    # bottleneck at segment 9 (index 8); queue builds from onset t0, peaks at tp, clears at tc
    t0 = 7*60 + 20 - 15*(demand-1)/0.2
    tp = 8*60 + 15
    tc = 9*60 + 15 + 25*(demand-1)/0.2
    tt = np.tile(ff, (len(epochs), 1))
    for i, t in enumerate(epochs):
        if t0 < t < tc:
            # queue delay at bottleneck (seconds), triangular in time, scaled by demand
            if t <= tp: frac = (t - t0) / (tp - t0)
            else: frac = max(0.0, 1 - (t - tp) / (tc - tp))
            qdelay = 1100 * demand * frac   # seconds of queue delay at peak
            # spread the queue over segments 5..9 (indices 4..8) growing backward
            spread = [0.10, 0.15, 0.20, 0.25, 0.30]
            for k, s in zip(range(4, 9), spread):
                tt[i, k] += qdelay * s * (1 if frac > 0.15*(8-k) else 0.4)
        # arterial school-run delay on last two segments 08:15-08:55
        if 8*60 + 15 <= t <= 8*60 + 55:
            tt[i, 12] += 90 * demand
            tt[i, 13] += 120 * demand
    if incident:
        k = rng.integers(2, 12); s = rng.integers(7*60, 8*60+40); d = rng.integers(20, 50)
        for i, t in enumerate(epochs):
            if s <= t < s + d: tt[i, k] += rng.integers(300, 900)
    return tt
def walk(tt, dep):
    t = dep*60.0
    for k in range(nseg):
        m = t/60.0
        i = int((m - epochs[0]) // 5)
        t += tt[i, k]
    return (t - dep*60.0)/60.0
def inst(tt, dep):
    i = int((dep - epochs[0]) // 5)
    return tt[i].sum()/60.0
days = 190
res = {}
for dep_h, dep_m in [(7,20),(7,30),(7,40),(7,50),(8,0)]:
    dep = dep_h*60 + dep_m
    W, I = [], []
    rng = np.random.default_rng(2541)
    for d in range(days):
        demand = float(np.clip(rng.lognormal(0, 0.12), 0.75, 1.45))
        inc = rng.random() < 0.08
        tt = day_profile(demand, inc)
        W.append(walk(tt, dep)); I.append(inst(tt, dep))
    W, I = np.array(W), np.array(I)
    print(f"dep {dep_h}:{dep_m:02d}  walked p50 {np.percentile(W,50):5.1f} p90 {np.percentile(W,90):5.1f} | inst p50 {np.percentile(I,50):5.1f} p90 {np.percentile(I,90):5.1f}")
