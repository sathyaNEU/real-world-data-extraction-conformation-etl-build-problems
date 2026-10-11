"""Bin-centring adjustments written by tune.py: (member index, first date of service, event kind, claim component,
original allowed in cents) -> change in cents. Each moves one clean claim by a few per cent at most."""
TUNE = {
    (978, '2025-08-11', 'fill', 0, 2520188): -31038,
    (1318, '2025-07-30', 'chemo', 0, 1743668): 6,
    (1569, '2026-06-29', 'fill', 0, 781801): -4986,
    (1885, '2025-07-21', 'img_us', 0, 51659): 263,
    (2236, '2025-07-17', 'op_hospital', 0, 18873): 616,
    (2558, '2025-08-06', 'fill', 0, 2484273): -28525,
    (2666, '2025-08-05', 'fill', 0, 2485085): -25120,
    (2670, '2025-07-27', 'admit', 0, 2416794): -6879,
    (3131, '2025-06-26', 'fill', 0, 1504152): -16069,
    (4109, '2026-07-10', 'fill', 0, 687308): -8816,
    (5415, '2026-05-22', 'admit', 0, 796147): 12257,
}
