"""Bin-centring adjustments written by tune.py: (member index, first date of service, event kind, claim component,
original allowed in cents) -> change in cents. Each moves one clean claim by a few dollars."""
TUNE = {
    (364, '2025-07-01', 'admit', 1, 895378): -6264,
    (1057, '2026-07-23', 'fill', 0, 811846): -8591,
    (2179, '2025-08-26', 'fill', 0, 683471): -10659,
    (3334, '2025-08-07', 'fill', 0, 375262): -9410,
    (3837, '2025-08-05', 'fill', 0, 4445): -190,
    (4053, '2025-08-03', 'er', 0, 111491): -8043,
    (4208, '2025-08-01', 'dialysis', 0, 1469864): -5658,
    (4542, '2025-08-07', 'fill', 0, 97649): -2959,
    (4553, '2026-07-16', 'fill', 0, 65409): -4870,
    (4982, '2026-07-17', 'fill', 0, 77131): -3346,
    (4996, '2025-08-01', 'dialysis', 1, 55959): -750,
    (5052, '2026-06-25', 'postacute_facility', 1, 86777): -2823,
    (5484, '2026-06-03', 'admit', 0, 2710819): -9356,
}
