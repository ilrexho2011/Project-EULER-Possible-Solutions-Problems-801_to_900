def rwh_primes2(n):
	""" Input n>=6, Returns a list of primes, 2 <= p < n """
	correction = (n%6>1)
	n = {0:n, 1:n-1, 2:n+4, 3:n+3, 4:n+2, 5:n+1}[n % 6]
	sieve = [True]*(n//3)
	sieve[0] = False
	for i in range(int(n**0.5)//3+1):
		if sieve[i]:
			k = 3*i+1|1
			sieve[      ((k*k)//3)          : : 2*k]=[False]*((n//6 -(k*k)//6 -1)//k+1)
			sieve[(k*k + 4*k -2*k*(i&1))//3 : : 2*k]=[False]*((n//6 -(k*k + 4*k -2*k*(i&1))//6 -1)//k+1)
	return [2, 3] + [3*i+1|1 for i in range(1, n//3-correction) if sieve[i]]

def makeMu(MMax, primes):
	mu = [1]*(MMax+1)
	mu[0] = 0
	for p in primes:
		pp = p*p
		if pp >= len(mu): break
		for i in range(pp, len(mu), pp):
			mu[i] = 0
	for i in range(2, len(mu), 4):
		mu[i] = -mu[i]
	for j in range(1, len(primes)):
		if primes[j] >= len(mu): break
		for i in range(primes[j], len(mu), primes[j]):
			mu[i] = -mu[i]
	return mu

def func(n):
	primes = rwh_primes2(max(n,6)+1)
	mu = makeMu(n, primes)
	P = 1020340567
	S = 0
	for d in range(1, n+1):
		S = (S + mu[d]*pow(2, n//d, P)) % P
	return S

print(func(10**7))
