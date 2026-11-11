from math import isqrt
from sympy import factorint, primerange

def get_tot(n, pf):
    for p, r in pf:
        n //= p
        n *= (p-1)
    return n

def sig0(pf):
    res = 1
    for p, r in pf:
        res *= r+1
    return res

def sig1(pf):
    res = 1
    for p, r in pf:
        res *= (pow(p, r+1) - 1) // (p - 1)
    return res

def H0(k, pf):
    res = 1
    for p, r in pf:
        res *= pow(p, r-1) * (p*(r+1) - r)
    """
    res = 2*k - 1
    for d, pf_d in get_divisors(pf):
        if d == 1 or d == k:
            continue
        pf_kd = []
        for q, r in pf:
            s = r - (0 if q not in pf_d else pf_d[q])
            if s>0:
                pf_kd.append((q, s))
        res += (d-1) * get_tot(k//d, pf_kd)
    """
    return res

# Get divisors of n, 1 < d < n
def get_divisors(pf):
    divisors = [(1, {})]
    for p, r in pf:
        i_max = len(divisors)
        ppow = 1
        for s in range(1, r+1):
            ppow *= p
            for i in range(i_max):
                d, pf_d = divisors[i]
                new_pf_d = {a:b for a, b in pf_d.items()}
                new_pf_d[p] = s
                divisors.append((d*ppow, new_pf_d))
    return divisors

def H(n, pf_n, pf):
    res = 1
    for p, r in pf:
        pr = p**r
        s = 0 if p not in pf_n else pf_n[p]
        if s == r:
            res *= H0(pr, [(p, r)])
            continue
        res *= (s+1)*pow(p, r-1)*(p-1)
    return res

def f(p):
    if p == 2:
        return 2
    res = (p-1)**2

    pf = list(factorint(p-1).items())
    # print("pf", pf)

    tot = get_tot(p-1, pf)
    res += tot**3

    res += H0(p-1, pf)**2

    # print(0, H0(p-1, pf))
    # print("coprime", tot)

    for d, pf_d in get_divisors(pf):
        if d == 1 or d == p-1:
            continue
        pf_pd = []
        for q, r in pf:
            s = r - (0 if q not in pf_d else pf_d[q])
            if s>0:
                pf_pd.append((q, s))
        # print("pf_pd", pf_pd, (p-1)//d)
        # print("d=%d, multiples=%d, H=%d" % (d, get_tot((p-1)//d, pf_pd), H(d, pf_d, pf)))
        res += H(d, pf_d, pf)**2 * get_tot((p-1)//d, pf_pd)
    return res

def S(M, N):
    res = 0
    count = 0
    for p in primerange(M, N):
        count += 1
        if count%10**3 == 0:
            print(p)
        res += f(p)
    print(count)
    return res

MOD = 993353399
print(S(2, 10**2))
print(S(2, 10**5) % MOD)
print(S(10**16, 10**16 + 10**6) % MOD)
