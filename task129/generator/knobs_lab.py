"""task129 generator: tuning knobs for the image delivery ask, set so every graded figure sits inside
its bin. IPV and KBPR are the image CDN's requests per page view and kB per request; NATIVE_RPV is the
app's native image requests per mobile page view and NATIVE_KB their size against a page image."""
IPV = {2: 11.07,
 3: 11.39335,
 4: 12.1997,
 5: 12.40659,
 6: 12.50117,
 7: 12.33729,
 8: 12.57483}
KBPR = {2: 45.9,
 3: 46.4798,
 4: 58.20068,
 5: 60.51539,
 6: 61.61504,
 7: 61.78819,
 8: 62.66332}
NATIVE_RPV = {2: 2.878, 3: 2.987, 4: 3.148, 5: 3.274, 6: 3.238, 7: 3.272, 8: 3.289}
NATIVE_KB = 0.65
