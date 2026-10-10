"""task129 generator: tuning knobs for the deterministic asks (lab weight and image delivery), set
so every graded figure sits inside its one-decimal bin. LAB_ADJ is kB added to each title's own
asset for that change; IPV and KBPR are the image CDN's requests per view and kB per request."""
LAB_ADJ = {t: {c: 0.0 for c in "ABCDE"} for t in ["ST", "LA", "KD"]}
IPV = {2: 11.07, 3: 11.41, 4: 12.18, 5: 12.36, 6: 12.47, 7: 12.29, 8: 12.52}
KBPR = {2: 45.9, 3: 46.3, 4: 58.7, 5: 61.2, 6: 61.9, 7: 62.4, 8: 62.8}
