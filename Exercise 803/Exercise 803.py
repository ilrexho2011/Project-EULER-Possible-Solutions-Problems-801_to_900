"""
Project Euler 803 - Pseudorandom Sequence (Rand48)

Ideja:
1. Nga 9 shkronjat e njohura ("PuzzleOne") rindërtojmë gjendjen a0.
   - b_n mod 4 = bitët 16..17 të a_n, të cilët varen vetëm nga 18 bitët e ulët
     të a0 (LCG mod 2^k është e mbyllur) -> provojmë 2^18 vlera.
   - Për 30 bitët e lartë h: kushti i parë jep h mod 13, pra mbeten ~2^30/13
     kandidatë, që i filtrojmë me numpy.
2. Në të njëjtën mënyrë gjejmë të gjitha gjendjet x që prodhojnë "LuckyText".
3. Indeksi n me a_n = x gjendet me logaritëm diskret 2-adik:
   y = (A-1)*a + C  =>  y_n = A^n * y_0  (mod 2^50), dhe n gjendet bit pas biti.
"""
import numpy as np

A = 25214903917
C = 11
M48 = (1 << 48) - 1
ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def char_vals(s):
    return [ALPHA.index(ch) for ch in s]


def gen_string(a, n):
    out = []
    for _ in range(n):
        out.append(ALPHA[(a >> 16) % 52])
        a = (A * a + C) & M48
    return "".join(out)


def find_states(pattern):
    """Të gjitha a (48 bit) ku vargu c fillon me 'pattern'."""
    b = char_vals(pattern)
    L = len(b)

    # Hapi 1: 18 bitët e ulët (kontrollojmë b mod 4)
    M18 = np.uint64((1 << 18) - 1)
    lows = np.arange(1 << 18, dtype=np.uint64)
    x = lows.copy()
    mask = np.ones(len(lows), dtype=bool)
    for i in range(L):
        mask &= ((x >> np.uint64(16)) & np.uint64(3)) == np.uint64(b[i] % 4)
        x = (x * np.uint64(A) + np.uint64(C)) & M18
    lows = [int(v) for v in lows[mask]]

    # Hapi 2: 30 bitët e lartë
    results = []
    MASK = np.uint64(M48)
    CHUNK = 1 << 22
    for l in lows:
        # (4h + (l>>16)) mod 52 == b0  ->  h mod 13 i fiksuar
        h0 = ((b[0] - (l >> 16)) // 4) % 13
        total = ((1 << 30) - h0 + 12) // 13
        for start in range(0, total, CHUNK):
            k = np.arange(start, min(start + CHUNK, total), dtype=np.uint64)
            a = ((np.uint64(h0) + np.uint64(13) * k) << np.uint64(18)) | np.uint64(l)
            cur = a
            for i in range(1, L):
                cur = (cur * np.uint64(A) + np.uint64(C)) & MASK
                ok = ((cur >> np.uint64(16)) % np.uint64(52)) == np.uint64(b[i])
                a, cur = a[ok], cur[ok]
                if len(a) == 0:
                    break
            results.extend(int(v) for v in a)
    return sorted(results)


def lcg_index(a0, target):
    """n më i vogël >= 0 i tillë që a_n = target (periudha 2^48)."""
    MOD = 1 << 50
    y0 = ((A - 1) * a0 + C) % MOD
    yt = ((A - 1) * target + C) % MOD
    t = yt * pow(y0, -1, MOD) % MOD          # t = A^n mod 2^50
    Ainv = pow(A, -1, MOD)
    n = 0
    for i in range(48):
        # A^(2^i) ≡ 1 + 2^(i+2)*tek  (mod 2^(i+3))
        if (t * pow(Ainv, n, MOD)) % (1 << (i + 3)) != 1:
            n |= 1 << i
    return n


def first_occurrence(a0, pattern):
    return min(lcg_index(a0, x) for x in find_states(pattern))


if __name__ == "__main__":
    # Teste nga teksti i problemit
    assert gen_string(123456, 9) == "bQYicNGCY"
    assert first_occurrence(123456, "RxqLBfWzv") == 100
    assert find_states("EULERcats") == [78580612777175]

    a0_list = find_states("PuzzleOne")
    print("a0 =", a0_list)
    print("Pergjigja:", min(first_occurrence(a0, "LuckyText") for a0 in a0_list))
