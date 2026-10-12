"""task129 generator: tuning knobs for the image delivery ask, set so every graded figure sits inside
its bin. IPV and KBPR are the image CDN's requests per page view and kB per request; NATIVE_RPV is the
app's native image requests per mobile page view and NATIVE_KB their size against a page image."""
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
NATIVE_RPV = {2: 1.21, 3: 1.24, 4: 1.27, 5: 1.29, 6: 1.31, 7: 1.36, 8: 1.33}
NATIVE_KB = 0.27
