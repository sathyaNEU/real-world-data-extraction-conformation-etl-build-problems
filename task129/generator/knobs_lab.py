"""task129 generator: tuning knobs for the deterministic asks (lab weight and image delivery), set
so every graded figure sits inside its one-decimal bin. LAB_ADJ is kB added to each title's own
asset for that change; IPV and KBPR are the image CDN's requests per view and kB per request."""
LAB_ADJ = {'KD': {'A': 0.046,
        'B': -0.008,
        'C': -0.023,
        'D': 0.019,
        'E': -0.008},
 'LA': {'A': -0.025,
        'B': 0.022,
        'C': -0.027,
        'D': -0.025,
        'E': 0.002},
 'ST': {'A': 0.028,
        'B': 0.049,
        'C': -0.012,
        'D': -0.006,
        'E': -0.004}}
IPV = {2: 11.07,
 3: 11.40577,
 4: 12.21626,
 5: 12.34238,
 6: 12.489,
 7: 12.30042,
 8: 12.49249}
KBPR = {2: 45.9,
 3: 46.32034,
 4: 58.52997,
 5: 61.28914,
 6: 61.80769,
 7: 62.34749,
 8: 62.93784}
