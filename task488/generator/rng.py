"""A small deterministic PRNG in pure integer arithmetic (SplitMix64), so every draw is the same on any CPU,
Python version or library build. No floats leave this module."""

MASK = (1 << 64) - 1


class Rng:
    def __init__(self, seed):
        self.seed = seed & MASK
        self.state = seed & MASK

    def next64(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)

    def below(self, n):
        """Uniform integer in [0, n) by rejection, no modulo bias."""
        if n <= 0:
            raise ValueError(n)
        limit = (1 << 64) - ((1 << 64) % n)
        while True:
            x = self.next64()
            if x < limit:
                return x % n

    def between(self, lo, hi):
        """Uniform integer in [lo, hi] inclusive."""
        return lo + self.below(hi - lo + 1)

    def choice(self, seq):
        return seq[self.below(len(seq))]

    def chance(self, num, den):
        """True with probability num/den."""
        return self.below(den) < num

    def shuffle(self, seq):
        for i in range(len(seq) - 1, 0, -1):
            j = self.below(i + 1)
            seq[i], seq[j] = seq[j], seq[i]
        return seq

    def fork(self, tag):
        """An independent stream keyed by the root seed and a string tag; it does not advance this stream, so
        the order in which streams are forked never changes what any of them draws."""
        h = 1469598103934665603
        for ch in tag.encode():
            h = ((h ^ ch) * 1099511628211) & MASK
        r = Rng(self.seed ^ h)
        r.next64()
        return r
